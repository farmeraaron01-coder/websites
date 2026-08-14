"""NFIP benchmark pull for California, partitioned by COUNTY.

WHY COUNTY AND NOT ZONE
-----------------------
Measured behaviour of FEMA's OpenFEMA API, not guesswork:

    $top=1000, $skip=0     -> 1,000 rows in 16s
    $top=5000, $skip=0     -> HTTP 503 after 60s
    $top=1000, $skip=2000  -> HTTP 503 (this is what killed the zone-partitioned run)

So the 503 is a SERVER-SIDE QUERY TIMEOUT, not rate limiting. Two things make a
query expensive: a large page, and a deep offset. A zone partition does not help
with the second -- Zone X alone has tens of thousands of qualifying rows, so
paging it always ends up deep, and it died at skip=2000 twice.

Partitioning by county keeps every partition small enough that the offset never
gets deep, and it produces the zone x county table we actually want. Zone comes
back as a field on each row and is grouped locally, which is free.

RESUME
------
Each county is written to disk the moment it completes. A restart skips
counties already on disk, so a crash costs one county rather than the run.

HONESTY ABOUT TRUNCATION
------------------------
Every county records how it ENDED: "complete" (short page, genuinely exhausted),
"CEILING" (hit the skip ceiling -- more data exists), or "TRUNCATED_BY_ERROR".
A truncated county biases its own median toward whatever the API returned first,
and a short partition is indistinguishable from a complete one unless the script
says which it was. Anything not "complete" is excluded from publication.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://www.fema.gov/api/open/v2/FimaNfipPolicies"
# IN-FORCE SNAPSHOT, not a transaction dump. Learned the hard way 14 Aug 2026:
# the first version of this pull returned five years of policyEffectiveDate
# (2021-2026) for the same benchmark. FEMA's policy file is TRANSACTIONAL -- an
# annual policy renewing five times is five rows, so the same house was counted
# five times, and those years straddle the Risk Rating 2.0 phase-in. Averaging
# them blends rate regimes into a median that never described any actual year.
#
# A policy is in force at REF if it had started and had not yet ended:
#     policyEffectiveDate <= REF < policyTerminationDate
REF = "2026-08-14"
BENCH = ("propertyState eq 'CA' and totalBuildingInsuranceCoverage eq 250000 "
         "and buildingDeductibleCode eq '5' and occupancyType eq 11 "
         f"and policyEffectiveDate le '{REF}' "
         f"and policyTerminationDate gt '{REF}' "
         "and cancellationDateOfFloodPolicy eq null")
SEL = ("ratedFloodZone,policyCost,primaryResidenceIndicator,hfiaaSurcharge,"
       "countyCode,policyEffectiveDate,policyTerminationDate,policyCount")
PAGE = 1000          # 5000 is a proven 503; do not raise this
CEILING = 20000      # skip ceiling per county
PAUSE = 2.0          # be polite between successful pages
OUT = "nfip_county"   # snapshot dir; REF is baked into the data, record it
FIPS = "/home/user/websites/flood-redesign/reference/ca-county-fips.tsv"


def get(url, tries=8):
    """Long backoff. The failure mode is a server-side timeout, so waiting
    genuinely helps -- unlike a 404, which no amount of waiting fixes."""
    delay, err = 5, "unknown"
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.loads(r.read().decode()), None
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            if e.code in (400, 404):          # malformed query; retrying is pointless
                return None, err
        except Exception as e:
            err = str(e)[:60]
        if attempt < tries - 1:
            time.sleep(delay)
            delay = min(delay * 2, 120)
    return None, err


def pull_county(fips):
    rows, skip, how = [], 0, "complete"
    while skip < CEILING:
        q = urllib.parse.urlencode({
            "$filter": f"{BENCH} and countyCode eq '{fips}'",
            "$select": SEL, "$top": PAGE, "$skip": skip,
        })
        d, err = get(f"{BASE}?{q}")
        if d is None:
            how = f"TRUNCATED_BY_ERROR ({err})"
            break
        batch = d.get("FimaNfipPolicies", [])
        rows.extend(batch)
        skip += PAGE
        if len(batch) < PAGE:
            break
        time.sleep(PAUSE)
    else:
        how = "CEILING"
    return rows, how


def api_up():
    """Cheapest possible query. If this fails the service is down, and grinding
    through 58 counties x 8 retries would just be a slow way to write 58 failure
    files."""
    q = urllib.parse.urlencode({"$filter": BENCH, "$select": "policyCost",
                                "$top": 1, "$skip": 0})
    d, _ = get(f"{BASE}?{q}", tries=1)
    return d is not None


def wait_for_api(max_wait_h=6):
    """FEMA's API goes down for stretches. Observed 14 Aug 2026: a query that
    returned 1,000 rows in 16s was 503ing forty minutes later. Waiting is the
    correct response -- there is nothing to fix on our side."""
    waited, step = 0, 300
    while waited < max_wait_h * 3600:
        if api_up():
            if waited:
                print(f"API recovered after {waited//60} min\n", flush=True)
            return True
        print(f"  API down, waited {waited//60} min...", flush=True)
        time.sleep(step)
        waited += step
    return False


def main():
    os.makedirs(OUT, exist_ok=True)
    if not wait_for_api():
        print("API still down after 6h -- giving up, nothing written", flush=True)
        return 1
    counties = []
    for line in open(FIPS):
        line = line.strip()
        if not line:
            continue
        code, name = line.split("\t")[:2]
        counties.append((code, name))
    print(f"{len(counties)} counties\n", flush=True)

    for code, name in counties:
        path = os.path.join(OUT, f"{code}.json")
        if os.path.exists(path):
            print(f"  {code} {name:22s} (already done)", flush=True)
            continue
        t = time.time()
        rows, how = pull_county(code)
        # Persist ONLY complete counties. Writing a truncated one would make the
        # resume logic skip it on the next run, quietly baking a partial county
        # into the published table -- exactly the failure this script exists to
        # avoid. A county left unwritten is retried; a county written wrong is not.
        if how == "complete":
            json.dump({"fips": code, "county": name, "ended": how, "rows": rows},
                      open(path, "w"))
        print(f"  {code} {name:22s} {len(rows):6,} rows  {time.time()-t:5.0f}s  "
              f"{how}{'' if how == 'complete' else '   <-- not saved, will retry'}",
              flush=True)
        if how != "complete" and not api_up():
            print("  API went down mid-run -- waiting for recovery", flush=True)
            if not wait_for_api():
                print("gave up waiting", flush=True)
                return 1

    print("\nALL COUNTIES WRITTEN", flush=True)


if __name__ == "__main__":
    sys.exit(main())
