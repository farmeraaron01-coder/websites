#!/usr/bin/env python3
"""
Download all call recordings from a RingCentral account.

What it does
------------
1. Authenticates with RingCentral using a JWT credential (JWT bearer flow).
2. Pulls the *account-level* call log (every extension/user) and keeps only
   records that have a recording.
3. Downloads each recording and saves it organized as:

       <OUTPUT_DIR>/<Agent Name (ext 101)>/<YYYY-MM-DD>/<file>.mp3

   where "Agent" is the internal RingCentral extension that handled the call.
4. Writes a manifest CSV (recordings_manifest.csv) describing every download.

The script is *resumable*: files that already exist on disk are skipped, so you
can stop and re-run it safely (handy because RingCentral rate-limits heavily).

Setup
-----
1. Install dependencies:
       pip install -r requirements.txt
2. Create a JWT credential in the RingCentral developer console
   (https://developers.ringcentral.com) and copy the JWT string.
3. Fill in your .env file (see .env.example). By default the script looks for
   the .env path below; override with the RC_ENV_FILE environment variable.

Run
---
       python download_recordings.py

See README.md for full details.
"""

import base64
import csv
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    sys.exit("Missing dependency 'requests'. Run: pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Missing dependency 'python-dotenv'. Run: pip install -r requirements.txt")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Default location of your .env file. Override by setting the RC_ENV_FILE
# environment variable, or just edit this path.
DEFAULT_ENV_FILE = (
    r"C:\Users\AaronFarmer\Farmer Agency Dropbox\Aaron Farmer"
    r"\Claude CoWork Files\RingCentral\.env"
)

# How far back to pull call records, in days. RingCentral retains call-log
# data for ~90 days, so anything older than that won't be available. We default
# to 60 days; override per-run with RC_LOOKBACK_DAYS in your .env (max useful
# value is ~90).
DEFAULT_LOOKBACK_DAYS = 60

# We request the call log in chunks to stay within RingCentral's per-request
# date-range and record-count limits. One month per chunk is safe.
CHUNK_DAYS = 31

# RingCentral throttles the call-log API (the "Heavy" rate-limit group, ~10
# requests/minute). Pause between API calls to stay under the limit. Increase
# if you see frequent 429 responses.
SECONDS_BETWEEN_CALLS = 7

# Pause between media downloads (the "Media" rate-limit group is more generous).
SECONDS_BETWEEN_DOWNLOADS = 1

PER_PAGE = 1000  # max records per page for the account call log
RETENTION_SAFETY_RETRIES = 4  # retries for transient/network errors


def load_config():
    """Read configuration from the .env file and environment."""
    env_file = os.environ.get("RC_ENV_FILE", DEFAULT_ENV_FILE)
    if os.path.isfile(env_file):
        load_dotenv(env_file)
        print(f"Loaded credentials from: {env_file}")
    else:
        # Fall back to a .env next to this script, then plain environment vars.
        local_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.isfile(local_env):
            load_dotenv(local_env)
            print(f"Loaded credentials from: {local_env}")
        else:
            print(
                f"WARNING: .env file not found at {env_file!r}. "
                "Falling back to existing environment variables."
            )

    def pick(*names, default=None, required=False):
        for n in names:
            val = os.environ.get(n)
            if val:
                return val.strip()
        if required:
            sys.exit(
                "Missing required setting. Expected one of these in your .env: "
                + ", ".join(names)
            )
        return default

    cfg = {
        "client_id": pick("RC_CLIENT_ID", "RINGCENTRAL_CLIENT_ID", "CLIENT_ID",
                          required=True),
        "client_secret": pick("RC_CLIENT_SECRET", "RINGCENTRAL_CLIENT_SECRET",
                              "CLIENT_SECRET", required=True),
        "jwt": pick("RC_JWT", "RINGCENTRAL_JWT", "JWT", "RC_JWT_TOKEN",
                   required=True),
        "server_url": pick("RC_SERVER_URL", "RINGCENTRAL_SERVER_URL", "SERVER_URL",
                          default="https://platform.ringcentral.com"),
        "output_dir": pick("RC_OUTPUT_DIR", "OUTPUT_DIR",
                          default=os.path.join(
                              os.path.dirname(os.path.abspath(__file__)),
                              "Recordings")),
        "lookback_days": int(pick("RC_LOOKBACK_DAYS", default=str(DEFAULT_LOOKBACK_DAYS))),
    }
    cfg["server_url"] = cfg["server_url"].rstrip("/")
    return cfg


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def get_access_token(cfg):
    """Exchange the JWT credential for an OAuth access token (JWT bearer flow)."""
    url = f"{cfg['server_url']}/restapi/oauth/token"
    basic = base64.b64encode(
        f"{cfg['client_id']}:{cfg['client_secret']}".encode()
    ).decode()
    headers = {
        "Authorization": f"Basic {basic}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": cfg["jwt"],
    }
    resp = requests.post(url, headers=headers, data=data, timeout=30)
    if resp.status_code != 200:
        sys.exit(
            "Authentication failed "
            f"({resp.status_code}): {resp.text}\n"
            "Check that RC_CLIENT_ID / RC_CLIENT_SECRET match the app that issued "
            "the JWT, that the JWT hasn't expired, and that RC_SERVER_URL points "
            "to the right environment (production vs sandbox)."
        )
    token = resp.json()
    print(
        f"Authenticated. Access token valid for ~{token.get('expires_in', '?')}s."
    )
    return token["access_token"]


# ---------------------------------------------------------------------------
# HTTP helper with rate-limit / retry handling
# ---------------------------------------------------------------------------

def api_get(url, token, params=None, stream=False):
    """GET with retry on 429 (rate limit) and transient 5xx/network errors."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = requests.get(url, headers=headers, params=params,
                                stream=stream, timeout=120)
        except requests.RequestException as exc:
            if attempt > RETENTION_SAFETY_RETRIES:
                raise
            wait = 2 ** attempt
            print(f"  Network error ({exc}); retrying in {wait}s...")
            time.sleep(wait)
            continue

        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 30))
            print(f"  Rate limited (429). Waiting {wait}s as instructed...")
            time.sleep(wait + 1)
            continue

        if resp.status_code >= 500 and attempt <= RETENTION_SAFETY_RETRIES:
            wait = 2 ** attempt
            print(f"  Server error {resp.status_code}; retrying in {wait}s...")
            time.sleep(wait)
            continue

        return resp


# ---------------------------------------------------------------------------
# Extension directory (to label folders by agent name)
# ---------------------------------------------------------------------------

def build_extension_directory(cfg, token):
    """Map extension id -> friendly 'Name (ext 101)' label."""
    directory = {}
    url = f"{cfg['server_url']}/restapi/v1.0/account/~/extension"
    params = {"perPage": 1000, "page": 1, "status": "Enabled"}
    while url:
        resp = api_get(url, token, params=params)
        if resp.status_code != 200:
            print(f"  Could not load extension directory ({resp.status_code}); "
                  "agent folders will fall back to call-log names.")
            break
        data = resp.json()
        for ext in data.get("records", []):
            name = (ext.get("name")
                    or ext.get("contact", {}).get("firstName", "")
                    + " " + ext.get("contact", {}).get("lastName", "")).strip()
            ext_num = ext.get("extensionNumber", "")
            directory[str(ext.get("id"))] = label_for(name, ext_num)
        nxt = data.get("navigation", {}).get("nextPage", {}).get("uri")
        url, params = (nxt, None) if nxt else (None, None)
        if url:
            time.sleep(SECONDS_BETWEEN_CALLS)
    print(f"Loaded {len(directory)} extensions into the directory.")
    return directory


def label_for(name, ext_num):
    name = (name or "").strip()
    if name and ext_num:
        return f"{name} (ext {ext_num})"
    if name:
        return name
    if ext_num:
        return f"ext {ext_num}"
    return "Unknown"


# ---------------------------------------------------------------------------
# Call log
# ---------------------------------------------------------------------------

def iter_call_log_with_recordings(cfg, token):
    """Yield call-log records that have a recording, walking month-by-month."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=cfg["lookback_days"])
    chunk_start = start
    while chunk_start < now:
        chunk_end = min(chunk_start + timedelta(days=CHUNK_DAYS), now)
        date_from = chunk_start.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        date_to = chunk_end.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        print(f"\nFetching call log {date_from[:10]} .. {date_to[:10]}")

        url = f"{cfg['server_url']}/restapi/v1.0/account/~/call-log"
        params = {
            "view": "Detailed",
            "withRecording": "true",
            "dateFrom": date_from,
            "dateTo": date_to,
            "perPage": PER_PAGE,
            "page": 1,
        }
        while url:
            resp = api_get(url, token, params=params)
            if resp.status_code != 200:
                print(f"  Call-log request failed ({resp.status_code}): "
                      f"{resp.text[:300]}")
                break
            data = resp.json()
            records = data.get("records", [])
            with_rec = [r for r in records if r.get("recording")]
            print(f"  Page returned {len(records)} records, "
                  f"{len(with_rec)} with recordings.")
            for rec in with_rec:
                yield rec
            nxt = data.get("navigation", {}).get("nextPage", {}).get("uri")
            url, params = (nxt, None) if nxt else (None, None)
            if url:
                time.sleep(SECONDS_BETWEEN_CALLS)

        chunk_start = chunk_end
        time.sleep(SECONDS_BETWEEN_CALLS)


# ---------------------------------------------------------------------------
# Record helpers
# ---------------------------------------------------------------------------

def sanitize(text, fallback="Unknown"):
    """Make a string safe to use as a Windows/macOS/Linux file or folder name."""
    text = (text or "").strip()
    if not text:
        return fallback
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", text)
    text = text.rstrip(" .")  # Windows dislikes trailing dots/spaces
    return text or fallback


def internal_party(rec):
    """Return the (name, ext_number) of the internal extension on this call.

    Outbound calls originate from the internal party (`from`); inbound calls
    terminate at the internal party (`to`).
    """
    direction = rec.get("direction", "")
    party = rec.get("from") if direction == "Outbound" else rec.get("to")
    party = party or {}
    return party.get("name", ""), party.get("extensionNumber", "")


def other_party_label(rec):
    """A short label for the external party, used in the file name."""
    direction = rec.get("direction", "")
    party = rec.get("to") if direction == "Outbound" else rec.get("from")
    party = party or {}
    return sanitize(party.get("name") or party.get("phoneNumber"), "Unknown")


def agent_folder(rec, directory):
    """Folder name for the internal agent/extension that handled the call."""
    ext = rec.get("extension") or {}
    ext_id = str(ext.get("id")) if ext.get("id") is not None else None
    if ext_id and ext_id in directory:
        return sanitize(directory[ext_id])
    name, ext_num = internal_party(rec)
    return sanitize(label_for(name, ext_num))


def parse_start(rec):
    raw = rec.get("startTime", "")
    try:
        # e.g. 2026-06-23T14:32:05.000Z
        return datetime.strptime(raw[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

EXT_BY_CONTENT_TYPE = {
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/x-wav": ".wav",
    "audio/wav": ".wav",
    "audio/vnd.wave": ".wav",
}


def download_recording(cfg, token, rec, directory):
    """Download one recording. Returns a manifest row dict, or None if skipped."""
    recording = rec.get("recording") or {}
    content_uri = recording.get("contentUri")
    rec_id = recording.get("id", "unknown")
    if not content_uri:
        return None

    start = parse_start(rec)
    date_str = start.strftime("%Y-%m-%d") if start else "unknown-date"
    time_str = start.strftime("%H%M%S") if start else "000000"
    direction = rec.get("direction", "Unknown")
    other = other_party_label(rec)

    folder = os.path.join(cfg["output_dir"], agent_folder(rec, directory), date_str)
    os.makedirs(folder, exist_ok=True)

    base_name = f"{date_str}_{time_str}_{direction}_{other}_{rec_id}"
    # Look for an already-downloaded file (any audio extension) to support resume.
    for ext in (".mp3", ".wav"):
        existing = os.path.join(folder, base_name + ext)
        if os.path.exists(existing) and os.path.getsize(existing) > 0:
            print(f"  Skip (exists): {existing}")
            return manifest_row(rec, existing, "skipped")

    resp = api_get(content_uri, token, stream=True)
    if resp.status_code != 200:
        print(f"  FAILED ({resp.status_code}) recording {rec_id}: {resp.text[:200]}")
        return manifest_row(rec, "", f"error {resp.status_code}")

    content_type = resp.headers.get("Content-Type", "").split(";")[0].strip().lower()
    ext = EXT_BY_CONTENT_TYPE.get(content_type, ".mp3")
    target = os.path.join(folder, base_name + ext)

    tmp = target + ".part"
    with open(tmp, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if chunk:
                fh.write(chunk)
    os.replace(tmp, target)
    print(f"  Saved: {target}")
    return manifest_row(rec, target, "downloaded")


def manifest_row(rec, path, status):
    name, ext_num = internal_party(rec)
    return {
        "status": status,
        "startTime": rec.get("startTime", ""),
        "direction": rec.get("direction", ""),
        "agent_name": name,
        "agent_extension": ext_num,
        "from": (rec.get("from") or {}).get("phoneNumber", ""),
        "to": (rec.get("to") or {}).get("phoneNumber", ""),
        "duration_sec": rec.get("duration", ""),
        "result": rec.get("result", ""),
        "recording_id": (rec.get("recording") or {}).get("id", ""),
        "file_path": path,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cfg = load_config()
    os.makedirs(cfg["output_dir"], exist_ok=True)
    print(f"Saving recordings under: {cfg['output_dir']}")
    print(f"Looking back {cfg['lookback_days']} days.")

    token = get_access_token(cfg)
    directory = build_extension_directory(cfg, token)

    manifest_path = os.path.join(cfg["output_dir"], "recordings_manifest.csv")
    fields = ["status", "startTime", "direction", "agent_name", "agent_extension",
              "from", "to", "duration_sec", "result", "recording_id", "file_path"]

    downloaded = skipped = errors = total = 0
    with open(manifest_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for rec in iter_call_log_with_recordings(cfg, token):
            total += 1
            row = download_recording(cfg, token, rec, directory)
            if row:
                writer.writerow(row)
                fh.flush()
                if row["status"] == "downloaded":
                    downloaded += 1
                elif row["status"] == "skipped":
                    skipped += 1
                else:
                    errors += 1
            time.sleep(SECONDS_BETWEEN_DOWNLOADS)

    print("\n" + "=" * 60)
    print(f"Done. {total} recordings found.")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped (already on disk): {skipped}")
    print(f"  Errors: {errors}")
    print(f"Manifest written to: {manifest_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Re-run to resume (already-downloaded files are skipped).")
        sys.exit(1)
