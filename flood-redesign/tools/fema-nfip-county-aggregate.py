"""Aggregate the county-partitioned NFIP pull into a publishable benchmark.

Reads the per-county JSON written by fema-nfip-county-pull.py and produces the
NFIP side of the private-vs-NFIP comparison, at the same terms as our own book:
$250,000 building limit, $5,000 deductible, single-family owner-occupied.

THREE THINGS THIS GUARDS AGAINST
--------------------------------
1. TRUNCATED COUNTIES. The puller only writes counties that finished cleanly,
   but a file could still be stale from an older run. Every county is re-checked
   here and anything not "complete" is refused, not averaged in.

2. ZONE AS A CAUSE. Risk Rating 2.0 does not rate by flood zone at all. Zone
   determines whether insurance is MANDATORY, not what it costs. So a by-zone
   table is descriptive of who happens to live where, and saying "Zone X costs
   $N because it is Zone X" inverts the causation. The output carries that
   warning on the zone block itself, where whoever publishes it will see it.

3. SMALL CELLS. Same floor as our own aggregates: nothing below n=10 is emitted.

policyCost is FEMA's all-in figure -- premium plus reserve fund assessment,
federal policy fee and HFIAA surcharge -- which is the right comparator for our
own premium+fee+tax total, and the wrong one for a bare premium.
"""
import json
import os
import statistics
import sys
from collections import defaultdict

IN = "nfip_county"
MIN_N = 10

# Zone families. The numbered A zones (A01-A30, AE, AH, AO, AR, A99) are all
# Special Flood Hazard Areas where cover is mandatory with a federally backed
# mortgage. V zones are coastal SFHAs. X/B/C are outside the SFHA, where cover
# is optional -- which is the distinction that actually matters to a reader,
# and the one the pricing question turns on.
def family(zone):
    if not zone:
        return "unknown"
    z = zone.strip().upper()
    if z.startswith("V"):
        return "V (coastal high risk, mandatory)"
    if z.startswith("A"):
        return "A (high risk, mandatory)"
    if z[0] in "XBC":
        return "X/B/C (outside high-risk, optional)"
    if z == "D":
        return "D (undetermined)"
    return "other"


def cell(vals):
    """Suppress below the floor. Report percentiles, not just the middle: the
    interquartile range excludes the bottom quartile by construction, which is
    exactly where the cheap cohort lives."""
    v = sorted(x for x in vals if x is not None)
    if len(v) < MIN_N:
        return None
    def pct(p):
        return round(float(statistics.quantiles(v, n=100)[p - 1]), 2) if len(v) > 2 else None
    return {
        "n": len(v),
        "median": round(float(statistics.median(v)), 2),
        "p10": pct(10), "p25": pct(25), "p75": pct(75), "p90": pct(90),
        "min": round(float(v[0]), 2), "max": round(float(v[-1]), 2),
    }


def main():
    if not os.path.isdir(IN):
        print(f"no {IN}/ directory -- run fema-nfip-county-pull.py first")
        return 1

    rows, counties, refused = [], {}, []
    for fn in sorted(os.listdir(IN)):
        if not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(IN, fn)))
        if d.get("ended") != "complete":
            refused.append(f"{d.get('county')} ({d.get('ended')})")
            continue
        counties[d["fips"]] = d["county"]
        for r in d["rows"]:
            r["_county"] = d["county"]
            rows.append(r)

    if refused:
        print("REFUSED (not complete):", "; ".join(refused))
    print(f"{len(counties)} counties, {len(rows):,} policies")
    if len(counties) < 58:
        print(f"WARNING: {58 - len(counties)} California counties missing -- "
              f"a statewide median from a partial set is not statewide")

    def cost(r):
        c = r.get("policyCost")
        return float(c) if isinstance(c, (int, float)) else None

    by_zone, by_fam, by_county, by_cz = (defaultdict(list) for _ in range(4))
    primary, nonprimary = [], []
    for r in rows:
        c = cost(r)
        if c is None:
            continue
        z = (r.get("ratedFloodZone") or "").strip().upper()
        by_zone[z or "unknown"].append(c)
        by_fam[family(z)].append(c)
        by_county[r["_county"]].append(c)
        by_cz[(r["_county"], family(z))].append(c)
        (primary if r.get("primaryResidenceIndicator") else nonprimary).append(c)

    out = {
        "_meta": {
            "source": "OpenFEMA FimaNfipPolicies v2, pulled by county",
            "terms": "CA, $250,000 building limit, deductible code 5 ($5,000), "
                     "occupancyType 11 (single-family residential)",
            "cost_definition": ("policyCost = premium + reserve fund assessment + "
                                "federal policy fee + HFIAA surcharge. This is the "
                                "all-in figure and is the correct comparator for our "
                                "own premium + policy fee + surplus lines tax total. "
                                "Comparing it to a bare premium would overstate the NFIP."),
            "counties_complete": len(counties),
            "counties_refused": refused,
            "policies": len(rows),
            "min_n": MIN_N,
            "comparison_note": ("Our own book is the outcome of shopping both markets -- "
                                "we place private only when it wins -- so the gap against "
                                "the full NFIP population is an UPPER BOUND on any one "
                                "person's saving, never a promise."),
            "adverse_selection_note": ("Private carriers choose which properties to write; "
                                       "the NFIP must accept every applicant. NFIP rates "
                                       "therefore carry risks private declined. That is a "
                                       "statutory duty, not inefficiency, and the page "
                                       "should not imply otherwise."),
        },
        "statewide": cell([c for c in map(cost, rows) if c is not None]),
        "by_zone_family": {k: v for k, v in
                           ((k, cell(v)) for k, v in sorted(by_fam.items())) if v},
        "by_county": {k: v for k, v in
                      ((k, cell(v)) for k, v in sorted(by_county.items())) if v},
        "by_primary_residence": {
            "primary": cell(primary),
            "non_primary": cell(nonprimary),
            "note": ("The HFIAA surcharge is $25 on a primary residence and $250 "
                     "otherwise, so this split is largely that surcharge and should "
                     "not be read as a risk difference."),
        },
    }

    out["by_zone_RAW"] = {
        "WARNING": ("DESCRIPTIVE ONLY -- DO NOT PUBLISH AS CAUSATION. Risk Rating 2.0 "
                    "does not rate by flood zone. Zone determines whether cover is "
                    "MANDATORY; it does not set the price. Any inversion here (an A "
                    "zone cheaper than an X zone) is a fact about who lives where and "
                    "what their buildings are like, not about zones being mispriced."),
        "cells": {k: v for k, v in
                  ((k, cell(v)) for k, v in sorted(by_zone.items())) if v},
    }

    cz = {}
    for (county, fam), vals in sorted(by_cz.items()):
        c = cell(vals)
        if c:
            cz.setdefault(county, {})[fam] = c
    out["by_county_and_zone_family"] = cz

    json.dump(out, open("ca-benchmark.json", "w"), indent=1)
    print("\nwritten ca-benchmark.json")
    if out["statewide"]:
        s = out["statewide"]
        print(f"  statewide NFIP median all-in: ${s['median']:,.0f}  "
              f"(p10 ${s['p10']:,.0f} / p90 ${s['p90']:,.0f}, n={s['n']:,})")
    for k, v in out["by_zone_family"].items():
        print(f"  {k:38s} median ${v['median']:8,.0f}  n={v['n']:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
