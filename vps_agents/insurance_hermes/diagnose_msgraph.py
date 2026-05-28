#!/usr/bin/env python3
"""
Diagnose Microsoft Graph auth issues for the hermes agent.

Reads MSGRAPH_TENANT_ID, MSGRAPH_CLIENT_ID, MSGRAPH_CLIENT_SECRET from
the environment (or from /opt/data/.env if --env-file is passed), runs
through the three most common failure modes for the
"IDX14121: JWT is not a well formed JWE" error, and prints a clear
verdict.

USAGE on the VPS:
    python3 diagnose_msgraph.py --env-file /opt/data/.env

Never prints the secret, never prints the full token.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.parse
import urllib.request


GUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
GRAPH_AUDIENCE_GUID = "00000003-0000-0000-c000-000000000000"
GRAPH_AUDIENCE_URL = "https://graph.microsoft.com"


def load_env_file(path: str) -> None:
    if not os.path.exists(path):
        print(f"  (env file {path} not found, using process env only)")
        return
    with open(path) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def b64url_decode(segment: str) -> bytes:
    pad = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + pad)


def inspect_secret_shape(secret: str) -> str | None:
    """Return a problem string if the secret looks wrong, else None."""
    if not secret:
        return "MSGRAPH_CLIENT_SECRET is empty."
    if GUID_RE.match(secret):
        return (
            "MSGRAPH_CLIENT_SECRET is GUID-shaped. This is almost certainly the\n"
            "  'Secret ID' column from Entra, not the 'Value' column.\n"
            "  Fix: Entra ID -> App registrations -> your app -> Certificates & secrets ->\n"
            "       New client secret -> copy the VALUE column immediately."
        )
    if len(secret) < 20:
        return f"MSGRAPH_CLIENT_SECRET is only {len(secret)} chars; real secrets are ~40."
    return None


def request_token(tenant_id: str, client_id: str, client_secret: str) -> dict:
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": f"{GRAPH_AUDIENCE_URL}/.default",
        "grant_type": "client_credentials",
    }).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        return {"_http_error": e.code, "_body": body}


def decode_jwt_claims(token: str) -> dict | None:
    parts = token.split(".")
    if len(parts) not in (3, 5):
        return {"_malformed": True, "_segment_count": len(parts)}
    try:
        return json.loads(b64url_decode(parts[1]))
    except Exception:
        return None


def call_graph_users(token: str) -> tuple[int, str]:
    req = urllib.request.Request(
        "https://graph.microsoft.com/v1.0/users?$top=1",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, "ok"
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--env-file", default="/opt/data/.env")
    args = p.parse_args()

    print("=== Microsoft Graph auth diagnostic for hermes ===\n")
    load_env_file(args.env_file)

    tenant = os.environ.get("MSGRAPH_TENANT_ID", "")
    client = os.environ.get("MSGRAPH_CLIENT_ID", "")
    secret = os.environ.get("MSGRAPH_CLIENT_SECRET", "")

    print("Step 1: Environment variable presence")
    print(f"  MSGRAPH_TENANT_ID   : {'present' if tenant else 'MISSING'}")
    print(f"  MSGRAPH_CLIENT_ID   : {'present' if client else 'MISSING'}")
    print(f"  MSGRAPH_CLIENT_SECRET: {'present' if secret else 'MISSING'}")
    if not (tenant and client and secret):
        print("\nFAIL: one or more required vars missing. Fix /opt/data/.env first.")
        return 1
    print()

    print("Step 2: Tenant ID shape")
    if tenant in ("common", "organizations", "consumers"):
        print(f"  FAIL: MSGRAPH_TENANT_ID='{tenant}'. Client-credentials flow requires")
        print("        a specific tenant GUID, not a generic endpoint.")
        print("        Get it from Entra ID -> Overview -> Tenant ID.")
        return 1
    if not GUID_RE.match(tenant):
        print(f"  WARN: MSGRAPH_TENANT_ID is not GUID-shaped (got {tenant!r}).")
    else:
        print("  OK (GUID-shaped)")
    print()

    print("Step 3: Client ID shape")
    if not GUID_RE.match(client):
        print(f"  WARN: MSGRAPH_CLIENT_ID is not GUID-shaped.")
    else:
        print("  OK (GUID-shaped)")
    print()

    print("Step 4: Client secret shape")
    problem = inspect_secret_shape(secret)
    if problem:
        print(f"  FAIL: {problem}")
        return 1
    print("  OK (looks like a real secret Value, not a Secret ID)")
    print()

    print("Step 5: Request access token (scope=.default, client_credentials)")
    tok = request_token(tenant, client, secret)
    if "_http_error" in tok:
        print(f"  FAIL: HTTP {tok['_http_error']} from token endpoint.")
        print("  Body (first 500 chars):")
        print("   ", tok["_body"][:500])
        return 1
    access_token = tok.get("access_token")
    if not access_token:
        print(f"  FAIL: no access_token in response. Got keys: {list(tok)}")
        return 1
    print(f"  OK (token acquired, length={len(access_token)}, segments={len(access_token.split('.'))})")
    print()

    print("Step 6: Decode token claims (no secrets printed)")
    claims = decode_jwt_claims(access_token)
    if claims is None:
        print("  FAIL: token is not decodeable as JWT.")
        return 1
    if claims.get("_malformed"):
        print(f"  FAIL: token has {claims['_segment_count']} segments (expected 3 or 5).")
        print("        This is the IDX14121 cause.")
        return 1
    aud = claims.get("aud", "<missing>")
    iss = claims.get("iss", "<missing>")
    roles = claims.get("roles", [])
    appid = claims.get("appid", "<missing>")
    print(f"  aud   : {aud}")
    print(f"  iss   : {iss}")
    print(f"  appid : {appid}")
    print(f"  roles : {roles}")
    print()

    print("Step 7: Audience check")
    if aud in (GRAPH_AUDIENCE_URL, GRAPH_AUDIENCE_GUID, GRAPH_AUDIENCE_URL + "/"):
        print("  OK (token audience is Microsoft Graph)")
    else:
        print(f"  FAIL: token aud={aud!r} but Graph expects {GRAPH_AUDIENCE_URL!r}.")
        print("        Wrong scope was requested. Fix the scope in hermes config to")
        print(f"        '{GRAPH_AUDIENCE_URL}/.default' (literal string, not a permission name).")
        return 1
    print()

    print("Step 8: Permission roles check")
    if not roles:
        print("  WARN: token has no 'roles' claim. Application permissions probably")
        print("        not admin-consented yet. In Entra ID -> your app -> API permissions,")
        print("        confirm Mail.Read / Mail.ReadWrite (Application, not Delegated) are")
        print("        listed and 'Grant admin consent' has been clicked.")
    else:
        wanted = {"Mail.Read", "Mail.ReadWrite", "User.Read.All"}
        have = wanted & set(roles)
        if have:
            print(f"  OK (has {sorted(have)})")
        else:
            print(f"  WARN: roles {roles} present but none of {sorted(wanted)} are.")
    print()

    print("Step 9: Live call to GET /users?$top=1")
    status, body = call_graph_users(access_token)
    if status == 200:
        print("  OK (Graph accepted the token)")
        print("\nVERDICT: auth is healthy. If hermes still can't fetch email, the bug")
        print("is in hermes' use of the token (wrong user UPN, wrong endpoint, etc.),")
        print("not in the credentials.")
        return 0
    print(f"  FAIL: HTTP {status}")
    print("  Body (first 500 chars):")
    print("   ", body[:500])
    return 1


if __name__ == "__main__":
    sys.exit(main())
