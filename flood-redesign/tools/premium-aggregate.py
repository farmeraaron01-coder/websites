#!/usr/bin/env python3
"""
Aggregate the RBIA flood bordereaux into publishable cost statistics.

RUN THIS ON AARON'S MACHINE, against the local Dropbox folder. The bordereaux
contain insured names and street addresses; this script reads them locally and
writes ONLY aggregates, so no personal data transits anywhere or lands in the
websites repo.

    python3 premium-aggregate.py \
        --root "C:/Users/AaronFarmer/Farmer Agency Dropbox/Aaron Farmer/P Drive - Flood 2/RBIA Bordereaux" \
        --out  ./premium-aggregates

Needs: pip install pandas openpyxl xlrd

WHY THE OUTPUT IS SHAPED THIS WAY
`/how-much-does-flood-insurance-cost/` draws 19,311 impressions at position 17.4
— the largest pool on the site, stuck on page two — because it answers the
question generically. The fix is a real number for the reader's own county and
zone. Everything here exists to produce those numbers defensibly.

TWO RULES, ENFORCED IN CODE RATHER THAN BY EYE
  1. MIN_N. No cell is emitted below the threshold. "Average premium in Alpine
     County, based on 2 policies" discloses what two identifiable people pay.
  2. Normalisation. Premium is meaningless without the coverage it bought, so
     every figure is also expressed per $100,000 of building cover.

WHAT "TOTAL COST" MEANS HERE, per Aaron 13 Aug
  private total = gross premium + policy fee + surplus lines tax + stamping fee
  NFIP total    = premium + HFIAA surcharge + federal policy fee + ICC + reserve
                  fund assessment   (this is FEMA's own `policyCost` field)
Comparing a bare private premium against FEMA's `policyCost` overstates the
private advantage, because only one side carries its fees. Both sides are
totalled or neither is.

THE SELECTION EFFECT, AND WHY IT IS A FEATURE
Aaron: "we write the policies that generally have the lowest premium, so if NFIP
was lowest they would have gotten the business."

So this book is not a sample of private pricing. It is the subset where private
beat the NFIP. That makes the median a biased-LOW estimate of private pricing in
general, and it means the gap against the full NFIP population is an upper bound
on any individual's saving — NOT an estimate of it.

Stated correctly it is still the most useful number available, and it needs no
quote data: "clients who shopped both and placed privately paid a median of X."
That is the outcome of shopping, which is the thing a buyer actually wants. The
report must say this plainly; a reader who works it out unaided will distrust
everything else on the page.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

MIN_N = 10          # suppression floor for any published cell
MIN_N_CITY = 20     # stricter for city level, where cells are smaller

# Canonical field -> the many spellings seen across carriers and years.
# Matching is case-insensitive on a squashed form (non-alphanumerics stripped),
# so "Bdx Builidng TIV" (sic, real typo in the QBE file) still lands.
ALIASES = {
    "premium":      ["grosspremium", "grosspremiumpaidthistime", "premium",
                     "grosswrittenpremium", "annualpremium", "totalpremium"],
    "policy_fee":   ["policyfee", "fee", "mgafee", "inspectionfee"],
    "sl_tax":       ["surpluslinestax", "sltax", "surplustax", "tax"],
    "stamping_fee": ["stampingfee", "stampfee"],
    "bldg_limit":   ["buildinglimit", "bdxbuilidngtiv", "bdxbuildingtiv",
                     "buildingtiv", "buildingcoverage", "coveragea"],
    "cont_limit":   ["contentslimit", "contentstiv", "contentscoverage", "coveragec"],
    "bldg_deduct":  ["propertydeductible", "buildingdeductible", "deductible"],
    "cont_deduct":  ["contentdeductible", "contentsdeductible"],
    "state":        ["state", "insuredmailingaddressstate", "riskstate", "propertystate"],
    "county":       ["county", "riskcounty"],
    "city":         ["city", "insuredmailingaddresscity", "riskcity"],
    "zip":          ["zipcode", "zip", "postalcode"],
    "zone":         ["floodzone", "zone", "ratedfloodzone", "femazone"],
    "occupancy":    ["occupancy", "occupancytype"],
    "construction": ["constructiontype", "construction"],
    "year_built":   ["yearbuilt", "originalconstructiondate"],
    "sqft":         ["sqft", "squarefeet", "squarefootage"],
    "stories":      ["nofstories", "noofstories", "numberofstories", "stories"],
    "imap":         ["intermapscore", "intermapriskscore"],
    "community":    ["communityname", "nfipcommunityname"],
    "eff_date":     ["policyeffectivedate", "riskinceptiondate", "saledate",
                     "effectivedate", "policyissuancedate"],
    "new_renewal":  ["neworrenewal", "newrenewalendt", "newrenewal", "transactiontype"],
    "carrier":      ["carriername", "carrier", "programname", "contract"],
    "policy_type":  ["policytype", "typeofinsurance"],
    # INTERNAL ONLY — used to de-duplicate revised and duplicated files, then
    # dropped before any aggregation. Never emitted. See dedupe below.
    "_polid":       ["certificateref", "policynumber", "policyno"],
}

# Defence in depth. By construction the frame only ever holds the canonical keys
# above, so nothing identifying should reach this sweep — it exists in case a
# future alias is added carelessly.
#
# Tokens are deliberately specific. A bare "name" would match the legitimate
# `community` field (NFIP community name) and silently delete the geography that
# makes zone analysis possible, which is a worse failure than the one it guards
# against.
FORBIDDEN = ["insuredname", "insuredfull", "fullname", "companyname",
             "streetaddress", "certificateref", "quoteref",
             "uniquemarketreference", "policyno", "policynumber",
             "commission", "brokername", "licensenumber"]

COVERAGE_BANDS = [(0, 250_000, "up to $250k"), (250_000, 500_000, "$250k–500k"),
                  (500_000, 1_000_000, "$500k–1M"), (1_000_000, 10**12, "$1M+")]


def squash(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def build_map(columns):
    """Map canonical name -> actual column, by squashed alias match."""
    out, used = {}, set()
    sq = {c: squash(c) for c in columns}
    for canon, aliases in ALIASES.items():
        for a in aliases:
            for col, s in sq.items():
                if col in used:
                    continue
                if s == a or (len(a) > 6 and a in s):
                    out[canon] = col
                    used.add(col)
                    break
            if canon in out:
                break
    return out


def find_header(path, sheet, pd):
    """Bordereaux often carry a title row, so the header is not always row 0."""
    probe = pd.read_excel(path, sheet_name=sheet, header=None, nrows=12)
    best, best_hits = 0, -1
    for i in range(len(probe)):
        cols = [squash(x) for x in probe.iloc[i].tolist()]
        hits = sum(1 for canon, al in ALIASES.items()
                   if any(a in c for c in cols for a in al))
        if hits > best_hits:
            best, best_hits = i, hits
    return best


def band(v):
    for lo, hi, label in COVERAGE_BANDS:
        if v is not None and lo < v <= hi:
            return label
    return None


def main():
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        sys.exit("Install dependencies first:\n  pip install pandas openpyxl xlrd")

    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="RBIA Bordereaux folder")
    ap.add_argument("--out", default="./premium-aggregates")
    ap.add_argument("--state", default="CA", help="state filter, or ALL")
    ap.add_argument("--min-n", type=int, default=MIN_N)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    files = []
    for dirpath, _, names in os.walk(a.root):
        for n in names:
            if n.startswith("~$"):
                continue
            if n.lower().endswith((".xlsx", ".xls", ".csv")):
                files.append(os.path.join(dirpath, n))
    print(f"  {len(files)} candidate files under {a.root}")

    frames, skipped, log = [], 0, []
    for f in sorted(files):
        try:
            sheets = ([None] if f.lower().endswith(".csv")
                      else pd.ExcelFile(f).sheet_names)
            for sh in sheets:
                if f.lower().endswith(".csv"):
                    df = pd.read_csv(f, low_memory=False)
                else:
                    df = pd.read_excel(f, sheet_name=sh,
                                       header=find_header(f, sh, pd))
                df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
                m = build_map(df.columns)
                # A usable sheet needs at least a premium and a state. Sheets
                # without both are filing summaries, not policy listings.
                if "premium" not in m or "state" not in m:
                    skipped += 1
                    continue
                keep = {canon: df[col] for canon, col in m.items()}
                sub = pd.DataFrame(keep)
                sub["_src"] = os.path.relpath(f, a.root)
                frames.append(sub)
                log.append(f"OK   {os.path.relpath(f, a.root)} [{sh}] "
                           f"{len(sub)} rows, fields={sorted(m)}")
        except Exception as e:
            skipped += 1
            log.append(f"FAIL {os.path.relpath(f, a.root)}: {str(e)[:90]}")

    if not frames:
        sys.exit("  No parseable bordereaux found. Check --root.")
    d = pd.concat(frames, ignore_index=True)
    print(f"  parsed {len(d):,} rows from {len(frames)} sheets ({skipped} skipped)")

    # ── DE-DUPLICATE BEFORE ANYTHING ELSE ──────────────────────────────────
    # The folders contain revised and duplicated files: "May 2025 QBE BDX.xlsx"
    # alongside "May 2025 QBE BDX REV 07-09-25.xlsx", and "QBE BDX June 2025.xlsx"
    # filed under BOTH June and July. Summing those double-counts policies and
    # would quietly skew every published figure.
    #
    # Deduping on the policy identifier handles revisions and cross-folder copies
    # in one step, and removes the need to guess which filename is authoritative
    # — a guess that fails silently.
    before = len(d)
    if "_polid" in d:
        d["_polid"] = d["_polid"].astype(str).str.strip().str.upper()
        d = d[d["_polid"].notna() & (d["_polid"] != "") & (d["_polid"] != "NAN")]
        # keep the last occurrence: later files are revisions of earlier ones
        d = d.drop_duplicates(subset=["_polid"], keep="last")
        print(f"  deduped on policy id: {before:,} -> {len(d):,} rows "
              f"({before - len(d):,} duplicates or revisions removed)")
    else:
        d = d.drop_duplicates()
        print(f"  WARNING: no policy-identifier column found, so dedupe fell back "
              f"to whole-row matching: {before:,} -> {len(d):,}. Revised files may "
              f"still be double-counted — check parse-log.txt.")

    # Guarantee no identifying column survived the alias mapping. The internal
    # policy id goes too, now that dedupe has used it.
    for c in list(d.columns):
        if c == "_polid" or any(bad in squash(c) for bad in FORBIDDEN):
            d = d.drop(columns=[c])

    n = lambda c: pd.to_numeric(d[c], errors="coerce") if c in d else np.nan
    d["_prem"] = n("premium")
    for comp in ("policy_fee", "sl_tax", "stamping_fee"):
        d["_" + comp] = n(comp).fillna(0) if comp in d else 0.0
    # Total cost to the customer — both sides totalled, or neither.
    d["_total"] = d["_prem"] + d["_policy_fee"] + d["_sl_tax"] + d["_stamping_fee"]
    d["_bldg"] = n("bldg_limit")
    d["_per100k"] = np.where(d["_bldg"] > 0, d["_total"] / (d["_bldg"] / 100_000), np.nan)
    d["_band"] = d["_bldg"].apply(band)
    if "eff_date" in d:
        d["_year"] = pd.to_datetime(d["eff_date"], errors="coerce").dt.year

    d = d[d["_prem"] > 0]
    if a.state.upper() != "ALL" and "state" in d:
        st = d["state"].astype(str).str.strip().str.upper()
        d = d[st.isin([a.state.upper(), {"CA": "CALIFORNIA"}.get(a.state.upper(), "")])]
    print(f"  {len(d):,} rows after filters (state={a.state})")

    def stats(g, min_n):
        v = g["_total"].dropna()
        if len(v) < min_n:
            return None
        p = g["_per100k"].dropna()
        out = {"n": int(len(v)),
               "total_p25": round(float(v.quantile(.25)), 2),
               "total_median": round(float(v.median()), 2),
               "total_p75": round(float(v.quantile(.75)), 2)}
        if len(p) >= min_n:
            out.update({"per100k_p25": round(float(p.quantile(.25)), 2),
                        "per100k_median": round(float(p.median()), 2),
                        "per100k_p75": round(float(p.quantile(.75)), 2)})
        bl = g["_bldg"].dropna()
        if len(bl):
            out["median_building_limit"] = round(float(bl.median()), 0)
        return out

    results = {"_meta": {
        "rows_analysed": int(len(d)),
        "state": a.state,
        "min_n": a.min_n,
        "min_n_city": max(a.min_n, MIN_N_CITY),
        "total_cost_definition": "premium + policy fee + surplus lines tax + stamping fee",
        "selection_note": ("This book contains policies where private coverage was placed, "
                           "which happens when it beat the NFIP alternative. It is therefore "
                           "the outcome of shopping both, not a sample of private pricing."),
        "suppression_note": f"cells below n={a.min_n} are omitted, n={max(a.min_n, MIN_N_CITY)} for cities",
    }}
    results["overall"] = stats(d, a.min_n)

    for label, col, min_n in [("by_county", "county", a.min_n),
                              ("by_city", "city", max(a.min_n, MIN_N_CITY)),
                              ("by_zone", "zone", a.min_n),
                              ("by_coverage_band", "_band", a.min_n),
                              ("by_occupancy", "occupancy", a.min_n),
                              ("by_year", "_year", a.min_n),
                              ("by_construction", "construction", a.min_n)]:
        if col not in d:
            continue
        bucket, suppressed = {}, 0
        key = d[col].astype(str).str.strip().str.title()
        for name, grp in d.groupby(key):
            if name in ("", "Nan", "None"):
                continue
            s = stats(grp, min_n)
            if s:
                bucket[name] = s
            else:
                suppressed += 1
        results[label] = {"cells": bucket, "suppressed_cells": suppressed}

    with open(os.path.join(a.out, "aggregates.json"), "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    with open(os.path.join(a.out, "parse-log.txt"), "w") as fh:
        fh.write("\n".join(log))

    print(f"\n  wrote {a.out}/aggregates.json  and  parse-log.txt")
    o = results.get("overall")
    if o:
        print(f"\n  OVERALL  n={o['n']:,}   median total ${o['total_median']:,.0f}"
              + (f"   median per $100k ${o.get('per100k_median', float('nan')):,.2f}"
                 if o.get("per100k_median") else ""))
    for k in ("by_county", "by_zone", "by_year"):
        if k in results:
            c = results[k]
            print(f"  {k}: {len(c['cells'])} published, {c['suppressed_cells']} suppressed")
    print("\n  Review aggregates.json before anything is published. Check parse-log.txt "
          "for FAIL lines — a carrier layout that silently failed to parse is the most "
          "likely way this produces a wrong number.")


if __name__ == "__main__":
    main()
