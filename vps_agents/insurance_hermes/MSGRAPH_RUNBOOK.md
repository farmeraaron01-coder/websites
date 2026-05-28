# Microsoft Graph auth troubleshooting (hermes + Outlook)

When Telegram/hermes can't fetch Outlook email and the error contains
**`IDX14121: JWT is not a well formed JWE, there must be four dots`**,
this runbook is the fastest path to root cause.

## TL;DR

Run this on the VPS:

```bash
python3 /opt/insurance_hermes/diagnose_msgraph.py --env-file /opt/data/.env
```

(Path of the script depends on where you've cloned the repo — adjust as
needed. The script lives at `vps_agents/insurance_hermes/diagnose_msgraph.py`
in the `farmeraaron01-coder/websites` repo.)

It walks through nine checks and stops at the first failure with a
verdict. It never prints the client secret or the full access token.

## What IDX14121 actually means

Graph received a token whose **shape** it doesn't accept. A normal JWT
has 3 segments (2 dots). An encrypted JWE has 5 segments (4 dots). Graph
is saying: this isn't either.

That happens for three reasons, in descending order of frequency:

### 1. Secret ID was copied instead of secret Value

In **Entra ID -> App registrations -> [your app] -> Certificates & secrets**,
each client secret has two columns:

| Column     | Looks like                                | Use as `MSGRAPH_CLIENT_SECRET`? |
| ---------- | ----------------------------------------- | ------------------------------- |
| **Value**  | `xQ8~AbC.De12fGh-iJk_LmNoPqRs.TuVwXy_z`   | YES                             |
| **Secret ID** | `7c4f1234-1234-1234-1234-1234abcd5678`  | No (this is just an identifier) |

The Value is shown **once**, at creation time. If you navigate away and
come back, it's masked as `***` forever. The Secret ID stays visible.
People come back for the secret, see the Secret ID, and copy that. OAuth
accepts it just well enough to return a degraded token, and Graph rejects
the token with IDX14121.

**Fix:** create a new client secret, copy the **Value** column the moment
it's shown, paste into `/opt/data/.env`, restart hermes.

### 2. Wrong scope in token request

For app-only (client credentials) flow, the scope must be the literal
string:

```
https://graph.microsoft.com/.default
```

Not `Mail.Read`, not `User.Read`, not bare `.default`. If hermes config
has the wrong scope, OAuth returns a token aimed at a different
audience and Graph rejects it.

Check `MSGRAPH_SCOPE` (or equivalent) in `/opt/data/config.yaml` or
`/opt/data/.env`.

### 3. Wrong tenant ID

`MSGRAPH_TENANT_ID` must be a tenant GUID. Client-credentials flow does
**not** work against `common`, `organizations`, or `consumers` endpoints.

Get it from **Entra ID -> Overview -> Tenant ID**.

## App registration checklist

In Entra ID -> App registrations -> [your app]:

- **Overview**: confirm Application (client) ID matches `MSGRAPH_CLIENT_ID`
  and Directory (tenant) ID matches `MSGRAPH_TENANT_ID`.
- **Certificates & secrets**: at least one secret with an unexpired
  expiry date. Copy the **Value** column. Note expiry on a calendar.
- **API permissions**: needs *Application* permissions (not Delegated)
  for what hermes does. Typically:
  - `Mail.Read` or `Mail.ReadWrite` (for inbox)
  - `User.Read.All` (to look up users)
  - **Click "Grant admin consent"** — without this, the token has no
    `roles` claim and every Graph call returns 403.
- **Authentication**: client-credentials flow doesn't need redirect URIs.

## Manual decode (no script)

If you want to verify by hand:

1. On the VPS, request a token with curl:
   ```bash
   source /opt/data/.env
   curl -s -X POST \
     "https://login.microsoftonline.com/$MSGRAPH_TENANT_ID/oauth2/v2.0/token" \
     -d "client_id=$MSGRAPH_CLIENT_ID" \
     -d "client_secret=$MSGRAPH_CLIENT_SECRET" \
     -d "scope=https://graph.microsoft.com/.default" \
     -d "grant_type=client_credentials" | jq -r .access_token
   ```
2. Paste the token at **https://jwt.ms** (processes locally in your
   browser, doesn't transmit). Treat it as a secret until it expires (~1h).
3. Look at `aud`. It must be `https://graph.microsoft.com` or
   `00000003-0000-0000-c000-000000000000`. Anything else = wrong scope.

## Once it's fixed

After updating `/opt/data/.env`, restart hermes so it picks up the new
env vars:

```bash
docker restart <hermes-container-name>
# or via your Docker manager UI
```

Then re-run `hermes doctor` and ask hermes via Telegram to fetch an
email as a smoke test.
