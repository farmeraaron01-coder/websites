"""Minimal RingCentral REST client: JWT auth + rate-limit-aware GET.

Import this instead of rewriting auth. The call-log API sits in RingCentral's "Heavy"
throttle group (~10 requests/minute) and answers 429 with a Retry-After header that
must be honored, which is the usual reason ad-hoc scripts fail partway through a pull.

Usage:
    from rc_client import RCClient
    rc = RCClient.from_env("/path/to/.env")
    data = rc.get("/restapi/v1.0/account/~/extension", perPage=1000)
    calls = rc.call_log(days=30)
"""

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

HEAVY_PAUSE = 7          # seconds between call-log pages
MAX_RETRIES = 4


def load_env(path):
    """Read a .env file into a dict. Tolerates comments, blank lines and CRLF."""
    out = {}
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8-sig") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out


class RCClient:
    def __init__(self, client_id, client_secret, jwt, server_url):
        self.server = server_url.rstrip("/")
        self._id, self._secret, self._jwt = client_id, client_secret, jwt
        self.token = None
        self.scopes = ""

    @classmethod
    def from_env(cls, env_path=None):
        env = load_env(env_path)

        def pick(*names, default=None, required=False):
            for n in names:
                v = env.get(n) or os.environ.get(n)
                if v:
                    return v.strip()
            if required:
                sys.exit(
                    "Missing credential. Expected one of: " + ", ".join(names)
                    + f"\nChecked env file: {env_path!r} and the environment."
                )
            return default

        c = cls(
            pick("RC_CLIENT_ID", "RINGCENTRAL_CLIENT_ID", "RC_APP_CLIENT_ID",
                 "CLIENT_ID", required=True),
            pick("RC_CLIENT_SECRET", "RINGCENTRAL_CLIENT_SECRET",
                 "RC_APP_CLIENT_SECRET", "CLIENT_SECRET", required=True),
            pick("RC_JWT", "RC_JWT_TOKEN", "RINGCENTRAL_JWT", "RC_USER_JWT",
                 "JWT", required=True),
            pick("RC_SERVER_URL", "RINGCENTRAL_SERVER_URL", "SERVER_URL",
                 default="https://platform.ringcentral.com"),
        )
        c.authenticate()
        return c

    def authenticate(self):
        basic = base64.b64encode(f"{self._id}:{self._secret}".encode()).decode()
        body = urllib.parse.urlencode({
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self._jwt,
        }).encode()
        req = urllib.request.Request(
            self.server + "/restapi/oauth/token", data=body,
            headers={"Authorization": "Basic " + basic,
                     "Content-Type": "application/x-www-form-urlencoded"})
        try:
            tok = json.load(urllib.request.urlopen(req, timeout=45))
        except urllib.error.HTTPError as e:
            sys.exit(
                f"Authentication failed ({e.code}): {e.read().decode()[:400]}\n"
                "Check that client id/secret belong to the app that issued the JWT, "
                "that the JWT hasn't expired, and that RC_SERVER_URL matches the "
                "environment (production vs sandbox)."
            )
        self.token = tok["access_token"]
        self.scopes = tok.get("scope", "")
        return self.token

    def get(self, path, **params):
        """GET a path (or absolute URL). Returns (json, error_string)."""
        url = path if path.startswith("http") else self.server + path
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        for attempt in range(1, MAX_RETRIES + 1):
            req = urllib.request.Request(
                url, headers={"Authorization": "Bearer " + self.token,
                              "Accept": "application/json"})
            try:
                return json.load(urllib.request.urlopen(req, timeout=90)), None
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = int(e.headers.get("Retry-After", 20))
                    time.sleep(wait + 1)
                    continue
                if e.code >= 500 and attempt < MAX_RETRIES:
                    time.sleep(2 ** attempt)
                    continue
                return None, f"{e.code} {e.read().decode()[:300]}"
            except urllib.error.URLError as e:
                if attempt < MAX_RETRIES:
                    time.sleep(2 ** attempt)
                    continue
                return None, f"network error: {e}"
        return None, "exhausted retries (429)"

    def paged(self, path, max_pages=8, pause=HEAVY_PAUSE, **params):
        """Follow navigation.nextPage, accumulating records."""
        out, page = [], 1
        while page <= max_pages:
            data, err = self.get(path, page=page, **params)
            if err:
                print(f"  [warn] {path} page {page}: {err}", file=sys.stderr)
                break
            out += data.get("records", [])
            if not data.get("navigation", {}).get("nextPage"):
                break
            page += 1
            time.sleep(pause)
        return out

    def extensions(self):
        return self.paged("/restapi/v1.0/account/~/extension", perPage=1000, pause=1)

    def call_log(self, days=30, direction="Inbound", extension_id=None, view="Detailed"):
        since = (datetime.now(timezone.utc) - timedelta(days=days)) \
            .strftime("%Y-%m-%dT%H:%M:%S.000Z")
        base = (f"/restapi/v1.0/account/~/extension/{extension_id}/call-log"
                if extension_id else "/restapi/v1.0/account/~/call-log")
        return self.paged(base, view=view, direction=direction,
                          dateFrom=since, perPage=1000)


LOST = {"Missed", "Voicemail", "Rejected", "Busy", "Call Failed", "No Answer"}


def is_lost(record):
    return record.get("result") in LOST
