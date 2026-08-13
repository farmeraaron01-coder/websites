"""Aggregate the NFIP benchmark pull into publishable cells.

Same suppression floor as the private side (n>=10), same benchmark terms, and
policyCost is FEMA's fully-loaded figure -- so these cells are directly
comparable to the private CA cells at loaded_pct 100.
"""
import json, statistics as st, collections

rows = json.load(open("fema-raw-snapshot.json"))
print(f"rows: {len(rows):,}")

def q(vals, p):
    vals = sorted(vals)
    if not vals: return None
    i = min(int(p * len(vals)), len(vals) - 1)
    return vals[i]

def cell(vals, min_n=10):
    v = [x for x in vals if x is not None]
    if len(v) < min_n: return None
    return {"n": len(v), "p25": q(v, .25), "median": q(v, .50), "p75": q(v, .75)}

MIN_N = 10
out = {"_meta": {
    "source": "FEMA OpenFEMA FimaNfipPolicies, pulled 13 Aug 2026",
    "terms": "California, $250,000 building coverage, $5,000 deductible "
             "(buildingDeductibleCode '5'), occupancyType 11 (single-family residential)",
    "cost_field": "policyCost — FEMA's own total: calculated premium + reserve fund "
                  "assessment + federal policy fee + HFIAA surcharge",
    "zone_field": "ratedFloodZone — the zone the policy was actually rated on, and "
                  "more complete than floodZoneCurrent",
    "min_n": MIN_N,
    "comparability": "Fully loaded, so directly comparable to the private California "
                     "cells, which are 100% tax-loaded at the same terms.",
    "rows": len(rows),
}}

costs = [r.get("policyCost") for r in rows]
out["overall"] = cell(costs)

byzone = collections.defaultdict(list)
for r in rows:
    z = (r.get("ratedFloodZone") or "").strip().upper()
    if z: byzone[z].append(r.get("policyCost"))
out["by_rated_zone"] = {}
supp = 0
for z, v in sorted(byzone.items(), key=lambda kv: -len(kv[1])):
    c = cell(v)
    if c: out["by_rated_zone"][z] = c
    else: supp += 1
out["by_rated_zone_suppressed"] = supp

# SFHA grouping: A* and V* are Special Flood Hazard Areas (mandatory purchase with a
# federally backed mortgage); X, B, C, D are not.
def sfha(z):
    if not z: return None
    if z[0] in ("A", "V"): return "SFHA (A/V zones) — purchase mandatory with a federally backed mortgage"
    if z[0] in ("X", "B", "C"): return "Outside SFHA (X/B/C) — purchase optional"
    if z[0] == "D": return "Zone D — undetermined risk"
    return None
g = collections.defaultdict(list)
for r in rows:
    k = sfha((r.get("ratedFloodZone") or "").strip().upper())
    if k: g[k].append(r.get("policyCost"))
out["by_mandate"] = {k: cell(v) for k, v in g.items() if cell(v)}

# Primary residence vs not — the $250 HFIAA surcharge cut.
p = collections.defaultdict(list)
for r in rows:
    k = r.get("primaryResidenceIndicator")
    if k is None: continue
    p["primary residence" if k in (True, "true", 1, "1") else "non-primary residence"].append(r.get("policyCost"))
out["by_primary_residence"] = {k: cell(v) for k, v in p.items() if cell(v)}

# Surcharge check: does the non-primary group really carry $250 more in HFIAA?
h = collections.defaultdict(list)
for r in rows:
    k = r.get("primaryResidenceIndicator")
    s = r.get("hfiaaSurcharge")
    if k is None or s is None: continue
    h["primary" if k in (True, "true", 1, "1") else "non-primary"].append(s)
out["hfiaa_surcharge_observed"] = {
    k: {"n": len(v), "median": q(v, .5), "min": min(v), "max": max(v)}
    for k, v in h.items() if v}

# Zone x mandate-relevant zones crossed with primary residence
c2 = collections.defaultdict(list)
for r in rows:
    z = (r.get("ratedFloodZone") or "").strip().upper()
    k = r.get("primaryResidenceIndicator")
    if not z or k is None: continue
    lab = "primary" if k in (True, "true", 1, "1") else "non-primary"
    c2[f"{z} / {lab}"].append(r.get("policyCost"))
out["by_zone_and_residence"] = {k: v2 for k, v in sorted(c2.items()) if (v2 := cell(v))}

json.dump(out, open("fema-benchmark.json", "w"), indent=2, default=str)

print(f"\nOVERALL  n={out['overall']['n']:,}  median ${out['overall']['median']:,}"
      f"  IQR ${out['overall']['p25']:,}-${out['overall']['p75']:,}")
print("\nBY RATED ZONE")
for z, c in out["by_rated_zone"].items():
    print(f"  {z:6s} n={c['n']:6,}  median ${c['median']:6,}  IQR ${c['p25']:,}-${c['p75']:,}")
print(f"  ({out['by_rated_zone_suppressed']} zones suppressed below n={MIN_N})")
print("\nBY MANDATE")
for k, c in out["by_mandate"].items():
    print(f"  {k}\n      n={c['n']:6,}  median ${c['median']:6,}  IQR ${c['p25']:,}-${c['p75']:,}")
print("\nBY PRIMARY RESIDENCE")
for k, c in out["by_primary_residence"].items():
    print(f"  {k:26s} n={c['n']:6,}  median ${c['median']:6,}")
print("\nHFIAA SURCHARGE OBSERVED")
for k, v in out["hfiaa_surcharge_observed"].items():
    print(f"  {k:14s} n={v['n']:6,}  median ${v['median']}  range ${v['min']}-${v['max']}")
