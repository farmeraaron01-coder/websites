# The policy side is solved: Momentum AMP has a working API

Written 4 Aug 2026. **This is the handoff note for the separate lead-to-policy project** — it records
what was proven here so that work does not start cold. No analysis was run in this session.

## The short version

There is no need for a manual CRM export. Momentum AMP (NowCerts) has a REST/OData API, and a working
Python client for it already exists — you built it in June for the call-intelligence project. It is at
`/Aaron Farmer/Claude CoWork Files/call-intelligence/nowcerts.py` in Dropbox, and the repo is
`farmeraaron01-coder/call-intelligence` on GitHub.

That module only does two things today: find an insured by phone, and write call logs and notes. It does
not touch policies. But it establishes the auth pattern, and the policy endpoint works.

## Verified working

Authentication is an API-key-for-JWT exchange. The JWT lasts ~24 hours.

```
POST https://api.momentumamp.com/api/token/exchange-api-key?apiKey=<MOMENTUM_API_KEY>
→ 200 {"accessToken": "...", "expiresIn": "2026-08-05T21:48:18Z", ...}
```

Then `Authorization: Bearer <accessToken>` on every request.

The credential authenticates as **California Flood Insurance Services API**
(`API@californiafloodinsurance.com`, agency owner). The key itself lives in the `.env` beside
`nowcerts.py` in Dropbox as `MOMENTUM_API_KEY` — **see the security note at the bottom, it should not stay
there.**

### The endpoint that matters

`GET /api/PolicyDetailList` — 109 fields per policy.

It rejects a bare request: *"Either one of the filters needs to be selected or these three
parameters (Top, Skip, OrderBy) are required."* So always send `$top`, `$skip` and `$orderby`, or a
`$filter`. This request returned 200:

```
GET /api/PolicyDetailList
  ?$filter=bindDate ge 2026-07-01T00:00:00Z and bindDate le 2026-08-04T23:59:59Z
  &$top=500&$skip=0&$orderby=bindDate desc
```

**`$top` caps at 500**, so anything larger has to page with `$skip`. Results come back under `value`.

`InsuredDetailList` also exists and behaves the same way. `PolicyList`, `InsuredList`, `QuoteList` and
`OpportunityList` all 404 — they are not endpoints.

## Every column the method needs is present

The open question in `LEAD-TO-POLICY.md` was whether the CRM could produce `Bound date` and `Email`. It
can, and considerably more:

| Needed | Field | Notes |
|---|---|---|
| Bound date | `bindDate` | Filterable, as above. The key to cohort assignment. |
| Email | `insuredEmail` | **497 of 500 populated.** Email matching will work well. |
| Name | `insuredFirstName`, `insuredLastName`, `insuredCommercialName` | |
| Phone | `insuredPhoneNumber`, `insuredCellPhone`, `insuredSMSPhone` | Three fields — check all, as `nowcerts.py` already does |
| Zip / State | `insuredZipCode`, `insuredState` | Fallback match key |
| Premium | `totalPremium`, `totalAgencyCommission` | Commission enables revenue-per-lead, not just count |
| Policy number | `number` | |
| Carrier / MGA | `carrierName`, `mgaName` | |
| Written by | `lastChangeUserName` | |
| Dates | `effectiveDate`, `createDate`, `inceptionDate`, `expirationDate`, `cancellationDate` | |
| Status | `status`, `active`, `additionalPolicyStatus` | |
| Line of business | `lineOfBusinesses` | Nested array of objects, needs unpacking to filter to flood |

### Three findings that change the plan

**1. `isQuote` — quotes live in the same endpoint as policies.** 132 of the 500 records in the July
sample had `isQuote: true`. **Any count that does not filter these out is inflated by roughly a
quarter.** This is the single easiest way to get the whole analysis wrong.

**2. `leadSources` is empty on all 500 records.** The CRM has a lead-source field and it is unused —
exactly the same pattern as the unused `LeadMethod` and `TakenBy` fields in Cognito form 5. So the
Cognito UTM data remains the only real attribution source, which is what `LEAD-TO-POLICY.md` assumes.
Nothing to reconcile against.

**3. The maturity thresholds no longer need guessing.** Because both `createDate` and `bindDate` are
available on every policy, the real lead-to-bind distribution can be computed from history rather than
assumed. The 90–150 day line in `LEAD-TO-POLICY.md` was my estimate; it should be replaced with the
measured number in the first run of the new project.

### One thing NOT established

`mgaName` broke down as: California Flood Insurance Services 156, Superior Flood 106, Poulton
Associates 98, Neptune Flood 59, AON Edge 42, none 28. That is *which MGA the business was placed
through* — it is **not** confirmed to be the same thing as "policies written by other agents via our
MGA," which was the caveat on the ~250/month figure. Separating own-agency production from other agents'
production still needs working out; `primaryOfficeDatabaseId`, `lastChangeUserName`, or the
`parentAgencyId` on the auth response are the candidates. **Do not assume `mgaName` answers it.**

## What this means for the monthly process

`LEAD-TO-POLICY.md` assumed a manual CRM export each month, and concluded the automated option would
"still need you once a month regardless" because the policy side was behind a login. **That is no longer
true.** Both sides are now API-reachable:

- Leads — Cognito Forms API (already used to pull 749 entries on 4 Aug)
- Policies — Momentum `PolicyDetailList`

So the monthly run can be fully automated, with no manual export step. That makes a scheduled monthly
job genuinely worth setting up rather than marginal.

## Running this from a cloud session

**Cloud works. Verified from a cloud session on 4 Aug**, which is where all of the above was proven:

- `api.momentumamp.com` is reachable from the container, so the environment's network policy already
  permits it. Nothing to request.
- Dropbox is reachable through the **connector**, not the filesystem. There is no `G:\` drive and no
  synced folder — `mcp__Dropbox__fetch` with a path returns file contents directly. That is how the
  `.env` above was read.

So there is no reason to work locally. Two things to set up properly, though.

### 1. Put the API key in the environment, not in Dropbox or chat

Fetching the key out of Dropbox on every run works, but it means the credential passes through the
session each time. Cloud environments support configured environment variables — set `MOMENTUM_API_KEY`
there once and any session can use it without a Dropbox round-trip and without it appearing in a
transcript. Do this **as part of rotating the key**, so the new value never lands in Dropbox at all.

### 2. The master files cannot live in the container or the repo

This is the real design constraint, and it follows from things already decided elsewhere:

- **Not the container** — cloud containers are ephemeral. The repo is cloned fresh at session start and
  the container is reclaimed afterwards. Anything written to disk and not pushed is gone.
- **Not the repo** — `leads-master.csv` and `policies-master.csv` carry customer names, emails and phone
  numbers. `LEAD-TO-POLICY.md` rules out committing them, and that stands.

Both files are append-only and must survive between monthly runs, so they need a home outside both.
**Dropbox is the right one**: already backed up weekly, already outside version control, and reachable
from a cloud session through the connector.

The monthly run therefore becomes: read both master files from Dropbox → pull new leads from Cognito and
new policies from Momentum → append → write both files back to Dropbox → produce the report. The report
itself has no PII once it is aggregated by campaign, so that part can be committed or published freely.

## Security note, and it is not minor

The Dropbox `.env` at `/Aaron Farmer/Claude CoWork Files/call-intelligence/.env` contains, in plaintext:

- `MOMENTUM_API_KEY` — full agency-owner access to the CRM, **including write access**
- `RC_JWT` / `RC_CLIENT_SECRET` — RingCentral, on a JWT that does not expire until 2094
- `OPENAI_API_KEY` — billable
- `AIRTABLE_API_KEY` — personal access token
- `CF_TUNNEL_TOKEN` — Cloudflare tunnel install token

This is the same class of exposure as the Google Ads refresh token in
`google-ads-project/Google Ads/.env`, already flagged. Dropbox is not a secret store: anything with a
share link or a compromised Dropbox login exposes all five at once, and the Momentum key can write to
live customer records.

**None of these values are in this repository and none should be.** They are referenced here by name
only. Rotating the Momentum key and moving these into a password manager is worth doing regardless of
whether the lead-to-policy project proceeds.
