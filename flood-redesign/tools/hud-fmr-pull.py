"""HUD Fair Market Rent -> the displacement-cost tables on the loss-of-use pages.

WHY FMR AND NOT SOMETHING ELSE
------------------------------
The loss-of-use pages need a defensible answer to "what does it cost to live
somewhere else for a few months". Two candidates were considered and one was
rejected:

  * Zillow / Rent.com asking rents. Rejected. They are a snapshot of what is
    currently listed, not a population statistic, the methodology changes without
    notice, and nothing about them is auditable a year from now.
  * HUD Fair Market Rent. Used. It is the 40th-percentile gross rent for a
    standard-quality unit in the area, published annually with an effective date,
    and -- the reason it is the right benchmark specifically here -- it is the
    same schedule FEMA uses to calculate disaster rental assistance. So the
    number on the page is the number the federal government itself would use if
    it were paying for your temporary housing.

WHAT THIS DOES NOT CLAIM
------------------------
FMR benchmarks an ordinary unfurnished long-term rental. A displaced family
usually needs furnished, short-term, available-this-week accommodation, which is
a different and more expensive market. No reliable published figure for that gap
was found, so both pages state the caveat and label FMR a planning floor rather
than a quote. Do not quietly promote it to an estimate of displacement cost.

THE SOURCE FILE MOVES EVERY OCTOBER
-----------------------------------
FY26 (effective 1 October 2025) is at

    https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY26_FMRs.xlsx

huduser.gov returns HTTP 202 with a zero-length body to a bare request and then
serves the file on a retry, so RETRY ON AN EMPTY 200/202 -- a single failed
attempt looks like a dead link and is not one. It also wants a browser
User-Agent.

SELF-CHECK
----------
The four California figures already published on
californiafloodinsurance.com/loss-of-use-coverage-in-flood-insurance/ were
sourced before this script existed. --verify reproduces them from the workbook,
which is what makes the whole table auditable rather than merely cited: if HUD
reissues the schedule (they publish revisions mid-year) the check fails loudly
instead of the pages drifting away from their stated source.
"""
import sys
import time
import urllib.request

URL = "https://www.huduser.gov/portal/datasets/fmr/fmr2026/FY26_FMRs.xlsx"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
LOCAL = "hud-fy26-fmr.xlsx"

# Already published on californiafloodinsurance.com. If any of these stops
# matching, a page is out of step with its own cited source -- fix the page.
PUBLISHED_CA = {
    "San Joaquin": (1742, 2423),
    "Sacramento": (2255, 3002),
    "Monterey": (2684, 3623),
    "Santa Clara": (3483, 4602),
}

# The statewide table. Keyed (state, county-name prefix) because HUD names
# counties, not metros, and prices them at the metro FMR area -- Harris and
# Galveston both carry the Houston figure, which is correct and worth knowing
# before someone "fixes" an apparent duplicate.
STATEWIDE = [
    ("AL", "Mobile"), ("MS", "Harrison"), ("MO", "St. Louis"), ("LA", "Orleans"),
    ("TX", "Harris"), ("NC", "New Hanover"), ("VA", "Virginia Beach"),
    ("TN", "Davidson"), ("SC", "Charleston"), ("FL", "Hillsborough"),
    ("NJ", "Ocean"), ("FL", "Miami-Dade"), ("WA", "King"), ("NY", "Kings"),
    # Quoted in prose as the extremes of the same schedule, not in the table.
    ("KY", "Perry"), ("MA", "Suffolk"),
]


def fetch(path=LOCAL, tries=4):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(URL, headers=UA), timeout=120) as r:
                blob = r.read()
            # An empty body is huduser's async-warmup response, not the file.
            if len(blob) > 100_000:
                open(path, "wb").write(blob)
                return path
        except Exception as e:
            print(f"  attempt {attempt + 1}: {str(e)[:70]}", file=sys.stderr)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError("could not download the FMR workbook after retries")


def load(path=LOCAL):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True)["FY26_FMRs"]
    it = ws.iter_rows(values_only=True)
    next(it)          # stusps state hud_area_code countyname county_town_name
                      # metro hud_area_name fips pop2023 fmr_0..fmr_4
    return [r for r in it]


def find(rows, state, county_prefix):
    p = county_prefix.lower()
    for r in rows:
        if r[0] == state and str(r[3]).lower().startswith(p):
            return {"county": r[3], "area": r[6],
                    "br2": r[11], "br3": r[12]}
    return None


def main():
    path = LOCAL
    try:
        open(path, "rb").close()
    except OSError:
        print("downloading FY26 FMR schedule...", file=sys.stderr)
        path = fetch()
    rows = load(path)
    print(f"{len(rows)} county rows loaded\n")

    bad = 0
    for county, (br2, br3) in PUBLISHED_CA.items():
        got = find(rows, "CA", county)
        ok = got and (got["br2"], got["br3"]) == (br2, br3)
        bad += 0 if ok else 1
        print(f"  [{'ok ' if ok else 'FAIL'}] CA {county:<14} "
              f"published {br2}/{br3}  workbook "
              f"{got['br2'] if got else '?'}/{got['br3'] if got else '?'}")
    print()

    for state, county in STATEWIDE:
        g = find(rows, state, county)
        if not g:
            print(f"  MISSING {state} {county}")
            continue
        print(f"  {state} {str(g['county'])[:24]:<24} "
              f"2BR=${g['br2']:>5}  3BR=${g['br3']:>5}   {str(g['area'])[:46]}")

    if bad:
        print(f"\n{bad} published California figure(s) no longer match the "
              "workbook. HUD may have reissued the schedule -- check before "
              "touching the pages.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
