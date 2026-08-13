#!/usr/bin/env python3
"""
Pull Search Console data for the flood properties and write CSVs.

WHY THIS EXISTS
Two sessions on 13 Aug 2026 spent hours disagreeing about impression counts and
page positions that a single query would have settled. Manual UI exports cap at
1,000 rows and cannot express a filtered cut (the address-query regex, for
instance), so the exports kept arriving in scopes neither side could reconcile.
This removes "run the export" as a bottleneck.

The Search Console API is OAuth-only — it does not accept API keys at all — so
the identity is a service account that has been added as a *user* on the
property. That last step is the one everybody misses: the API identity must be a
verified property user exactly like a human.

SETUP, ONCE (about 15 minutes)
  1. Google Cloud Console -> create or reuse a project -> enable the
     **Google Search Console API**.
  2. Create a **service account**. Download its JSON key.
  3. Search Console -> Settings -> Users and permissions -> Add user -> paste the
     service account's email -> **Restricted** is enough for read-only pulls.
     Grant it on the **Domain** property (`sc-domain:...`), which is the only
     scope that captures every host and protocol variant, including `www`.
  4. Store the JSON key in **1Password**. See below for where NOT to put it.

⚠ WHERE THE KEY MUST NOT GO — this is the whole point of the guard in this file
  - **NOT in this repo.** It would be committed and pushed to GitHub. The script
    refuses to run if the key path is inside the repository, rather than trusting
    anyone to remember.
  - **NOT in synced Dropbox.** As of 13 Aug there are already five plaintext
    credential stores there (`OPEN-ITEMS.md` Tier 1). A GCP service account
    private key does not expire, and every machine that ever synced the folder
    keeps a copy on disk.
  - **NOT pasted into a chat with an agent, including me.** A private key in a
    transcript cannot be un-seen.

  Two safe ways to run it:
    A. Locally or on the server, key injected from 1Password at runtime:
         op run --env-file=.env -- python3 gsc-pull.py
       The CSVs it writes are data, not secrets, and can be committed.
    B. In a Claude Code cloud session, with the key set as an environment
       variable in the *environment's* secret configuration — never as a file in
       the repo.

USAGE
  export GSC_SA_JSON=/secure/path/gsc-sa.json
  python3 gsc-pull.py                                  # last 90 days, California
  python3 gsc-pull.py --site sc-domain:statewidefloodinsurance.com
  python3 gsc-pull.py --days 28 --out ../gsc-2026-08
  python3 gsc-pull.py --query "flood insurance california"   # one query, by page

WHAT IT WRITES
  pages.csv          page                      — which URLs earn what
  queries.csv        query                     — the term list
  query-page.csv     query + page              — THE cut that settles arguments:
                                                 which URL ranks for which term
  devices.csv        device                    — desktop vs mobile split
  dates.csv          date                      — trend, for before/after checks
  addresses.csv      query + page, filtered    — the address cluster: queries
                                                 starting with a street number
                                                 and mentioning a flood zone/map

Every file carries the site, date range and row count in a comment header, so a
CSV can never again be quoted without its scope attached — which is exactly how
the 15,479-versus-1,245 confusion happened.
"""

import argparse
import csv
import datetime as dt
import os
import re
import sys

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
API_MAX_ROWS = 25000  # per request; paged with startRow beyond this

# Queries that look like "700 wilshire ... flood zone" — a street number followed
# by a flood-zone or flood-map phrase. These are escrow officers, lenders and
# brokers mid-transaction, which is the highest-intent traffic on the site.
ADDRESS_RE = re.compile(r"^\s*\d+\s+.*(flood\s*zone|flood\s*map)", re.I)


def build_service(creds_path):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit(
            "Missing dependencies. Install with:\n"
            "  pip install google-api-python-client google-auth"
        )
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    # cache_discovery=False avoids a noisy warning and a needless file write.
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def query_all(svc, site, start, end, dimensions, filters=None):
    """searchanalytics.query, paged until exhausted."""
    rows, start_row = [], 0
    while True:
        body = {
            "startDate": start,
            "endDate": end,
            "dimensions": dimensions,
            "rowLimit": API_MAX_ROWS,
            "startRow": start_row,
        }
        if filters:
            body["dimensionFilterGroups"] = [{"filters": filters}]
        resp = svc.searchanalytics().query(siteUrl=site, body=body).execute()
        batch = resp.get("rows", [])
        rows.extend(batch)
        if len(batch) < API_MAX_ROWS:
            return rows
        start_row += API_MAX_ROWS


def write_csv(path, dimensions, rows, site, start, end):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        # The scope travels with the data. A number without its scope is what
        # caused the whole 13 Aug argument.
        fh.write(f"# site={site} start={start} end={end} rows={len(rows)}\n")
        w = csv.writer(fh)
        w.writerow(list(dimensions) + ["clicks", "impressions", "ctr", "position"])
        for r in rows:
            w.writerow(
                list(r.get("keys", []))
                + [
                    r.get("clicks", 0),
                    r.get("impressions", 0),
                    round(r.get("ctr", 0) * 100, 2),
                    round(r.get("position", 0), 2),
                ]
            )
    print(f"  {len(rows):6d} rows  ->  {path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="sc-domain:californiafloodinsurance.com")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--out", default=".")
    ap.add_argument("--creds", default=os.environ.get("GSC_SA_JSON", ""))
    ap.add_argument(
        "--query",
        help="Pull the page breakdown for one exact query and nothing else.",
    )
    a = ap.parse_args()

    if not a.creds:
        sys.exit("No credentials. Set GSC_SA_JSON or pass --creds. See the header.")
    if not os.path.isfile(a.creds):
        sys.exit(f"Credentials file not found: {a.creds}")

    # THE GUARD. A service account key inside the repo gets committed and pushed.
    # Refuse rather than rely on anyone remembering, and rather than relying on
    # .gitignore, which only helps if the pattern happens to match.
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo = os.path.dirname(repo)  # up from flood-redesign/ to the repo root
    if os.path.abspath(a.creds).startswith(repo + os.sep):
        sys.exit(
            "REFUSING TO RUN: the credentials file is inside the repository at\n"
            f"  {os.path.abspath(a.creds)}\n"
            "A service account private key committed to GitHub is a live, "
            "non-expiring credential in public history. Move it outside the repo "
            "(1Password, then a path under /secure or your home directory) and "
            "re-run."
        )

    end = dt.date.today() - dt.timedelta(days=2)  # GSC data lags ~2 days
    start = end - dt.timedelta(days=a.days)
    s, e = start.isoformat(), end.isoformat()
    os.makedirs(a.out, exist_ok=True)
    svc = build_service(a.creds)

    print(f"\n{a.site}   {s} .. {e}\n")

    if a.query:
        rows = query_all(
            svc, a.site, s, e, ["page"],
            [{"dimension": "query", "operator": "equals", "expression": a.query}],
        )
        safe = re.sub(r"[^a-z0-9]+", "-", a.query.lower()).strip("-")
        write_csv(os.path.join(a.out, f"query-{safe}.csv"), ["page"], rows, a.site, s, e)
        return

    for name, dims in (
        ("pages", ["page"]),
        ("queries", ["query"]),
        ("query-page", ["query", "page"]),
        ("devices", ["device"]),
        ("dates", ["date"]),
    ):
        rows = query_all(svc, a.site, s, e, dims)
        write_csv(os.path.join(a.out, f"{name}.csv"), dims, rows, a.site, s, e)
        if name == "query-page":
            hits = [r for r in rows if ADDRESS_RE.match(r.get("keys", [""])[0])]
            write_csv(
                os.path.join(a.out, "addresses.csv"),
                ["query", "page"], hits, a.site, s, e,
            )
            uniq = len({r["keys"][0] for r in hits})
            imp = sum(r.get("impressions", 0) for r in hits)
            clicks = sum(r.get("clicks", 0) for r in hits)
            print(
                f"\n  ADDRESS CLUSTER: {uniq} distinct queries, "
                f"{imp} impressions, {clicks} clicks\n"
            )


if __name__ == "__main__":
    main()
