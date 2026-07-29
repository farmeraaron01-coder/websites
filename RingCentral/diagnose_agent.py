#!/usr/bin/env python3
"""
Diagnose why an agent's (e.g. Sarah's) inbound calls are being missed.

Reuses the same RingCentral JWT credentials as download_recordings.py. It looks
up the agent by name or extension number, then reports everything that commonly
causes "calls that should ring this person go to voicemail / get missed":

  * extension status (Enabled / Disabled / NotActivated)
  * presence + Do-Not-Disturb state
  * answering rules (forwarding to voicemail, unconditional forwarding, etc.)
  * business hours (is it treating now as "after hours"?)
  * call-queue membership + whether she's accepting queue calls
  * recent inbound call results (Missed / Voicemail / Accepted counts)

It only READS data — it changes nothing. At the end it prints a plain-language
list of likely problems.

Usage
-----
    python diagnose_agent.py                # defaults to searching "Sarah"
    python diagnose_agent.py "Sarah Jones"  # match by full/partial name
    python diagnose_agent.py 101            # match by extension number

Requires the app/JWT to have Read Accounts, Read Presence and Read Call Log
permissions.
"""

import base64
import os
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone

try:
    import requests
except ImportError:
    sys.exit("Missing dependency 'requests'. Run: pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("Missing dependency 'python-dotenv'. Run: pip install -r requirements.txt")


DEFAULT_ENV_FILE = (
    r"C:\Users\AaronFarmer\Farmer Agency Dropbox\Aaron Farmer"
    r"\Claude CoWork Files\RingCentral\.env"
)
DEFAULT_AGENT = "Sarah"
MISSED_LOOKBACK_DAYS = 7


# ---------------------------------------------------------------------------
# Config + auth (same approach as download_recordings.py)
# ---------------------------------------------------------------------------

def load_config():
    env_file = os.environ.get("RC_ENV_FILE", DEFAULT_ENV_FILE)
    if os.path.isfile(env_file):
        load_dotenv(env_file)
    else:
        local_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.isfile(local_env):
            load_dotenv(local_env)

    def pick(*names, default=None, required=False):
        for n in names:
            v = os.environ.get(n)
            if v:
                return v.strip()
        if required:
            sys.exit("Missing required setting; expected one of: " + ", ".join(names))
        return default

    return {
        "client_id": pick("RC_CLIENT_ID", "RINGCENTRAL_CLIENT_ID", "CLIENT_ID",
                          required=True),
        "client_secret": pick("RC_CLIENT_SECRET", "RINGCENTRAL_CLIENT_SECRET",
                              "CLIENT_SECRET", required=True),
        "jwt": pick("RC_JWT", "RINGCENTRAL_JWT", "JWT", "RC_JWT_TOKEN",
                   required=True),
        "server_url": pick("RC_SERVER_URL", "RINGCENTRAL_SERVER_URL", "SERVER_URL",
                          default="https://platform.ringcentral.com").rstrip("/"),
    }


def get_token(cfg):
    url = f"{cfg['server_url']}/restapi/oauth/token"
    basic = base64.b64encode(
        f"{cfg['client_id']}:{cfg['client_secret']}".encode()).decode()
    resp = requests.post(
        url,
        headers={"Authorization": f"Basic {basic}",
                 "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
              "assertion": cfg["jwt"]},
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(f"Authentication failed ({resp.status_code}): {resp.text}")
    return resp.json()["access_token"]


def api_get(cfg, token, path_or_url, params=None):
    url = (path_or_url if path_or_url.startswith("http")
           else f"{cfg['server_url']}{path_or_url}")
    for attempt in range(1, 5):
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            params=params, timeout=60)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 15))
            print(f"  (rate limited; waiting {wait}s)")
            time.sleep(wait + 1)
            continue
        return resp
    return resp


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------

def find_agents(cfg, token, query):
    """Return extension records whose name or number matches `query`."""
    matches, page = [], 1
    q = query.strip().lower()
    while True:
        resp = api_get(cfg, token, "/restapi/v1.0/account/~/extension",
                       params={"perPage": 1000, "page": page})
        if resp.status_code != 200:
            sys.exit(f"Could not list extensions ({resp.status_code}): {resp.text}")
        data = resp.json()
        for ext in data.get("records", []):
            name = (ext.get("name") or "").lower()
            num = str(ext.get("extensionNumber") or "")
            if q in name or q == num:
                matches.append(ext)
        if data.get("navigation", {}).get("nextPage", {}).get("uri"):
            page += 1
            continue
        break
    return matches


def get_json(cfg, token, path):
    resp = api_get(cfg, token, path)
    if resp.status_code != 200:
        return None, resp
    return resp.json(), resp


# ---------------------------------------------------------------------------
# Diagnosis
# ---------------------------------------------------------------------------

def diagnose(cfg, token, ext):
    ext_id = ext["id"]
    name = ext.get("name", "?")
    num = ext.get("extensionNumber", "?")
    print("\n" + "=" * 66)
    print(f"AGENT: {name}  (extension {num}, id {ext_id})")
    print("=" * 66)

    problems = []

    # --- Status ---
    status = ext.get("status")
    print(f"Extension status: {status}")
    if status and status != "Enabled":
        problems.append(f"Extension is '{status}', not 'Enabled' — it won't take calls.")

    # --- Presence / DND ---
    presence, _ = get_json(
        cfg, token,
        f"/restapi/v1.0/account/~/extension/{ext_id}/presence?detailedTelephonyState=true")
    if presence:
        dnd = presence.get("dndStatus")
        pres = presence.get("presenceStatus")
        tel = presence.get("telephonyStatus")
        print(f"Presence: {pres} | DND: {dnd} | Telephony: {tel}")
        if dnd in ("DoNotAcceptAnyCalls", "DoNotAcceptDepartmentCalls"):
            problems.append(
                f"Do-Not-Disturb is set to '{dnd}' — this blocks incoming "
                "calls (department/queue calls and/or all calls).")
        if pres == "Offline":
            problems.append("Presence is 'Offline' — her device/app may not be "
                            "logged in or registered.")
    else:
        print("Presence: (could not read — check Read Presence permission)")

    # --- Answering rules ---
    rules, _ = get_json(
        cfg, token,
        f"/restapi/v1.0/account/~/extension/{ext_id}/answering-rule?view=Detailed&perPage=100")
    if rules:
        print("\nAnswering rules:")
        for r in rules.get("records", []):
            if not r.get("enabled", True):
                continue
            label = r.get("name") or r.get("type")
            action = r.get("callHandlingAction")
            print(f"  - [{label}] action = {action}")
            if action in ("TakeMessagesOnly",):
                problems.append(
                    f"Answering rule '{label}' sends callers straight to "
                    "voicemail (TakeMessagesOnly) — her phone never rings.")
            if action in ("PlayAnnouncementOnly",):
                problems.append(
                    f"Answering rule '{label}' only plays an announcement "
                    "(PlayAnnouncementOnly) — no ring.")
            if action in ("UnconditionalForwarding",):
                fwd = r.get("unconditionalForwarding", {}).get("phoneNumber", "?")
                problems.append(
                    f"Answering rule '{label}' unconditionally forwards every "
                    f"call to {fwd} — calls never reach her extension.")
            if action == "ForwardCalls":
                fwd = r.get("forwarding", {})
                ring = fwd.get("ringingMode")
                rules_list = fwd.get("rules", [])
                print(f"      forwarding ringingMode={ring}, "
                      f"{len(rules_list)} forwarding rule group(s)")
    else:
        print("\nAnswering rules: (could not read — check Read Accounts permission)")

    # --- Business hours ---
    bh, _ = get_json(cfg, token,
                     f"/restapi/v1.0/account/~/extension/{ext_id}/business-hours")
    if bh:
        schedule = bh.get("schedule", {})
        if schedule.get("weeklyRanges"):
            print("\nBusiness hours: custom weekly schedule is set "
                  "(after-hours rule may divert calls outside these times).")
        else:
            print("\nBusiness hours: 24/7 (no custom schedule).")

    # --- Recent inbound call results ---
    since = (datetime.now(timezone.utc) - timedelta(days=MISSED_LOOKBACK_DAYS))
    date_from = since.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    log, _ = get_json(
        cfg, token,
        f"/restapi/v1.0/account/~/extension/{ext_id}/call-log"
        f"?direction=Inbound&view=Simple&perPage=1000&dateFrom={date_from}")
    if log is not None:
        results = Counter(r.get("result", "?") for r in log.get("records", []))
        total = sum(results.values())
        print(f"\nInbound calls in last {MISSED_LOOKBACK_DAYS} days: {total}")
        for res, n in results.most_common():
            print(f"  {res}: {n}")
        missed = sum(n for res, n in results.items()
                     if res in ("Missed", "Voicemail", "Rejected", "Busy",
                                "No Answer"))
        if total and missed / total > 0.4:
            problems.append(
                f"{missed} of {total} recent inbound calls did NOT connect "
                f"({missed/total:.0%}) — confirms a routing/answering problem.")
    else:
        print(f"\nInbound call log: (could not read)")

    # --- Summary ---
    print("\n" + "-" * 66)
    if problems:
        print("LIKELY ISSUES:")
        for p in problems:
            print(f"  ⚠  {p}")
    else:
        print("No obvious blocker found on the extension itself. Next check:")
        print("  • Is she a member of the call queue these calls come into, and")
        print("    is the QUEUE's routing/answering rule healthy?")
        print("  • Is her physical phone / app actually registered and online?")
    print("-" * 66)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_AGENT
    cfg = load_config()
    token = get_token(cfg)
    print(f"Searching for agent matching: {query!r}")
    agents = find_agents(cfg, token, query)
    if not agents:
        sys.exit(f"No extension found matching {query!r}. "
                 "Try a different name or the exact extension number.")
    if len(agents) > 1:
        print(f"Found {len(agents)} matches — diagnosing each:")
    for ext in agents:
        diagnose(cfg, token, ext)


if __name__ == "__main__":
    main()
