"""Find redirects that throw a ranking asset into a weaker page.

THE BUG THIS FINDS
------------------
Someone consolidates content, adds `Redirect 301 /old/ /new/`, and moves on. It
looks tidy. But if `/old/` was the URL Google actually ranked, the redirect takes
a page-one asset and points it at a page nobody finds. Nothing in WordPress shows
you this: the rule is in .htaccess, the old page is gone from the database, and
the only symptom is a URL in Search Console with impressions and no clicks.

Measured on statewidefloodinsurance.com, 14 Aug 2026: ten such rules, together
carrying about 20,400 impressions a year into pages that rank for almost nothing.
The worst single one sent 14,831 impressions into a page with five.

WHY IT AUDITS FROM THE OUTSIDE
------------------------------
It never reads .htaccess. It takes every URL Search Console has impressions for,
requests each one, and compares the source's impressions with the destination's.
That catches rules in .htaccess, in Rank Math, in the theme, and in any plugin,
including ones nobody remembers installing -- and it catches 404s and 410s in the
same pass. Reading the config file only finds what you thought to look at.

READING THE OUTPUT
------------------
A flagged row is not automatically wrong. The comparison is the judgement:

    /master-flood-policies-hoas/          974 impr
      -> /homeowners-association-flood-insurance/   5,699 impr    KEEP

That redirect is correct -- the target is nearly six times stronger, which is
what a good consolidation looks like. The flag fires when the target is *weaker*.

Position matters as much as volume, and they point at different fixes:

  * Source at a good position (say under 15) is a rescue. The ranking already
    exists; restore the page and stop throwing it away.
  * Source at position 60+ with high volume is not a redirect problem. That URL
    never ranked. It is a content opportunity, and recreating the old page will
    not by itself fix it. Do not confuse the two -- it wastes the work.

BEFORE RECREATING A PAGE AT A FLAGGED URL
-----------------------------------------
Check the slug against the publishing rules. On this account one flagged URL
contains a carrier's name, and there is a standing instruction never to publish
carrier names -- so restoring that URL is a decision for the principal, not a
mechanical fix. The tool cannot know this. Read the slugs.

USAGE
    redirect-audit.py https://example.com/            # needs the GSC property
                                                      # in the trailing-slash form
Requires a Search Console service-account key with read access to the property.
Point GSC_KEY at it. Never commit the key.
"""
import concurrent.futures as cf
import json
import os
import subprocess
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = os.environ.get("GSC_KEY", ".gsc-sa.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
# A year, ending a few days back -- Search Console's most recent days are partial
# and would understate a URL that is currently ranking.
START, END = "2025-08-14", "2026-08-11"


def gsc(site):
    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    rows = svc.searchanalytics().query(siteUrl=site, body={
        "startDate": START, "endDate": END,
        "dimensions": ["page"], "rowLimit": 25000}).execute().get("rows", [])
    return {r["keys"][0]: r for r in rows}


def probe(url):
    """HEAD it and report the FIRST non-200 status, plus where it points.

    The first status is the one that matters: a 301 that eventually reaches a 200
    is still a 301, and reporting the final 200 would hide every rule we are
    looking for. x-redirect-by tells you which layer owns it -- WordPress sets it,
    Apache's Redirect directive does not."""
    out = subprocess.run(["curl", "-sSI", "-A", UA, url],
                         capture_output=True, text=True, timeout=45).stdout
    code, loc, by = "", "", ""
    for line in out.splitlines():
        l = line.strip()
        low = l.lower()
        if low.startswith(("http/2 ", "http/1.1 ")):
            c = l.split()[1]
            # Skip the proxy's own "200 Connection Established".
            if not code and c != "200":
                code = c
            elif not code:
                code = c
        if low.startswith("location:"):
            loc = l.split(":", 1)[1].strip()
        if low.startswith("x-redirect-by"):
            by = l.split(":", 1)[1].strip()
    return code or "?", loc, by


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip().split("\n\n")[0])
        print("\nusage:  redirect-audit.py https://example.com/")
        return 1
    site = sys.argv[1]
    pages = gsc(site)
    print(f"{len(pages)} URLs with impressions, {START} to {END}\n")

    with cf.ThreadPoolExecutor(12) as ex:
        res = dict(zip(pages, ex.map(lambda u: probe(u), pages)))

    imp = {u: r["impressions"] for u, r in pages.items()}
    bad = sorted(((u, v) for u, v in res.items() if v[0] != "200"),
                 key=lambda x: -imp[x[0]])

    flagged = keep = gone = 0
    for u, (code, loc, by) in bad:
        r = pages[u]
        src = "WordPress" if by else "Apache/.htaccess or upstream"
        short = u.replace(site.rstrip("/"), "")
        print(f"{code}  {short}")
        print(f"     clicks={r['clicks']} impr={r['impressions']} "
              f"pos={r['position']:.1f}   by: {src}")
        if not loc:
            gone += 1
            print()
            continue
        ti = imp.get(loc, 0)
        print(f"     -> {loc.replace(site.rstrip('/'), '')}   target impr={ti}")
        if ti < r["impressions"]:
            flagged += 1
            verdict = ("RESCUE -- source already ranks"
                       if r["position"] < 15 else
                       "source outranks target, but never ranked well itself; "
                       "this is a content gap, not a redirect fix")
            print(f"     *** {verdict}")
        else:
            keep += 1
            print("     ok -- target is stronger, this consolidation worked")
        print()

    print(f"{flagged} redirects to fix, {keep} correct, {gone} dead ends, "
          f"of {len(pages)} URLs checked")
    json.dump({u: {"code": v[0], "loc": v[1], "by": v[2], "impr": imp[u],
                   "pos": pages[u]["position"]} for u, v in res.items()},
              open("redirect-audit.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
