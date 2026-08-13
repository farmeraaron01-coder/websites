"""Partitioned by rated flood zone so no query needs a deep $skip offset --
FEMA's API stalls past a few thousand rows of skip. Each zone is pulled
independently and capped, which also guarantees every zone gets a usable sample
rather than whichever zones happen to sort first."""
import json, urllib.request, urllib.parse

BASE = "https://www.fema.gov/api/open/v2/FimaNfipPolicies"
BENCH = ("propertyState eq 'CA' and totalBuildingInsuranceCoverage eq 250000 "
         "and buildingDeductibleCode eq '5' and occupancyType eq 11")
SEL = "ratedFloodZone,policyCost,primaryResidenceIndicator,hfiaaSurcharge"
ZONES = ["X","A99","AE","A","AO","AH","VE","D","B","C","AR","V","AHB","AOB"]
CAP, PAGE = 6000, 1000

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if i == tries-1: print(f"    fail: {str(e)[:70]}", flush=True); return None
    return None

rows = []
for z in ZONES:
    got, skip = 0, 0
    while got < CAP:
        q = urllib.parse.urlencode({"$filter": f"{BENCH} and ratedFloodZone eq '{z}'",
                                    "$select": SEL, "$top": PAGE, "$skip": skip})
        d = get(f"{BASE}?{q}")
        if d is None: break
        b = d.get("FimaNfipPolicies", [])
        rows.extend(b); got += len(b); skip += PAGE
        if len(b) < PAGE: break
    print(f"  {z:4s} {got:6,}", flush=True)
print(f"\ntotal {len(rows):,}")
json.dump(rows, open("fema-raw.json","w"))
