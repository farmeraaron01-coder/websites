#!/usr/bin/env python3
"""
Aggregate the RBIA flood bordereaux into publishable cost statistics.

Reads the carrier bordereaux locally and writes ONLY aggregates, so no personal
data lands in the websites repo. The source workbooks carry `Insured (Full Name)`
and `Street Address`; those columns are never mapped, and a FORBIDDEN sweep drops
anything that slips through.

    python3 premium-aggregate.py --root ./bdx --out ./premium-aggregates
    python3 premium-aggregate.py --root ./bdx --out ./out-all --state ALL

Needs: pip install pandas openpyxl xlrd

WHY THE OUTPUT IS SHAPED THIS WAY
`/how-much-does-flood-insurance-cost/` draws 2,866 impressions at position 18.15
— the largest pool on the site, stuck on page two — because it answers the
question generically. The fix is a real number for the reader's own county and
coverage level. Everything here exists to produce those numbers defensibly.

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

BUT THE TAX COLUMNS ONLY EXIST ON THE NEWER FILES. The legacy carrier layouts
(QBE / Brit / Hiscox monthly bordereaux, 2023 through most of 2025) carry
`Gross Premium` and `Policy Fee` and nothing else. Only the Instanda-era files
carry `surpluslinestax` / `stampingfee` (and 2026 adds `FireMarshalTax`). So the
total is fully loaded for some rows and premium+fee for others. `_meta` reports
what fraction of rows carried each component under `fee_coverage`; any published
figure has to be labelled with that, because a partly-loaded private total
understates private cost and therefore FLATTERS the private-vs-NFIP gap.

The missing tax is therefore added back — but PER STATE, from each state's own
STATUTORY rate, never blended and never inferred from this book. Surplus lines tax
and stamping fees are set state by state; some states levy both, some one, some
neither, and one of them (Oregon) charges a flat dollar fee rather than a
percentage. A single book-wide average silently inflates the low-tax states and
deflates the high-tax ones, and since the recorded rows are not spread evenly it
amounts to imposing the dominant state's rate on everybody else — which is exactly
what an earlier version of this script did.

Rates live in statutory_tax(), one state at a time, each with a primary source. A
state that is not listed there is left AS RECORDED and flagged, because inventing
a rate for an unverified state is how a wrong number reaches a page. Every cell
carries `loaded_pct`; only a cell at 100 is comparable to FEMA's `policyCost`.

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

ALL CARRIERS, NOT JUST THE BIGGEST ONE
Per Aaron: Hiscox writes very competitively in particular California areas. The
new-system files confirm the scale — QBE 428, Hiscox 308, Brit 192 — so a
QBE-only book would drop roughly a third of the policies and would misstate the
low end of the market, which is exactly the part a price page is about. Every
carrier is pooled. The per-carrier breakdown is computed only as a data-quality
check and is written to a separate gitignored file, never to the published
aggregates: carrier-level pricing is not ours to publish.
"""

import argparse
import json
import os
import re
import sys

MIN_N = 10          # suppression floor for any published cell
MIN_N_CITY = 20     # stricter for city level, where cells are smaller

# Canonical field -> the many spellings seen across carriers and years.
# Matching is case-insensitive on a squashed form (non-alphanumerics stripped),
# so "Bdx Builidng TIV" (sic, real typo in the QBE file) still lands.
ALIASES = {
    "premium":      ["grosspremium", "grosspremiumpaidthistime", "premium",
                     "grosswrittenpremium", "annualpremium", "totalpremium"],
    "policy_fee":   ["policyfee", "mgafee", "inspectionfee"],
    "sl_tax":       ["surpluslinestax", "sltax", "surplustax"],
    "stamping_fee": ["stampingfee", "stampfee"],
    "fire_tax":     ["firemarshaltax", "firemarshalltax"],
    "bldg_limit":   ["buildinglimit", "bdxbuilidngtiv", "bdxbuildingtiv",
                     "buildingtiv", "buildingcoverage", "coveragea"],
    "cont_limit":   ["contentslimit", "contentstiv", "contentscoverage", "coveragec"],
    # Instanda-era layouts ONLY. The RBIA-era carrier bordereaux (QBE, Hiscox and
    # Brit through Feb 2026) have no loss-of-use column at all -- verified by
    # reading their header rows. So absence here means "this layout does not
    # report it", never "this policy has no loss of use," and the two must not be
    # pooled. See loss_of_use below.
    "loss_of_use":  ["lossofuselimit", "lossofuse", "additionallivingexpense",
                     "alelimit", "lossofuseamount"],
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
    # Three separate transaction signals, because no single one is present in
    # every layout and they disagree about vocabulary. See TXN_EXCLUDE.
    "new_renewal":  ["neworrenewal", "newrenewalendt", "newrenewal", "renewalflag"],
    "txn_type":     ["transactiontype"],
    "sale_stage":   ["salestage"],
    # NOT "contract": the later legacy files carry a `Contract` column holding the
    # Lloyd's binder reference (B1230YA000470Z), which is a binding authority
    # reference and not a carrier at all. Mapping it produced a carrier breakdown
    # of meaningless codes.
    "carrier":      ["carriername", "programname", "carrier"],
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
# makes the area analysis possible, which is a worse failure than the one it
# guards against.
FORBIDDEN = ["insuredname", "insuredfull", "fullname", "companyname",
             "streetaddress", "certificateref", "quoteref",
             "uniquemarketreference", "policyno", "policynumber",
             "commission", "brokername", "licensenumber"]

# Rows that are not a policy's annual cost. Endorsements are mid-term changes
# carrying a partial (often negative) premium; cancellations carry a return
# premium. Including either drags the median toward zero. In the 2023 files alone
# there are 52 endorsement rows with premiums down to -$1,065.
TXN_EXCLUDE = ("end", "endt", "endorse", "endorsement", "cancel", "cancelled",
               "cancellation", "xln", "return", "flatcancel", "reinstate")

# Full names appear alongside codes in the same column ("CA" 1369, "CALIFORNIA"
# 19). Left unnormalised they split into two cells and both may fall below MIN_N.
STATE_MAP = {
    "CALIFORNIA": "CA", "WASHINGTON": "WA", "ARIZONA": "AZ", "OREGON": "OR",
    "TEXAS": "TX", "NEVADA": "NV", "FLORIDA": "FL", "ILLINOIS": "IL",
    "OHIO": "OH", "CONNECTICUT": "CT", "MASSACHUSETTS": "MA",
    "PENNSYLVANIA": "PA", "NEW JERSEY": "NJ", "NEW YORK": "NY",
    "COLORADO": "CO", "UTAH": "UT", "IDAHO": "ID", "MONTANA": "MT",
    "GEORGIA": "GA", "VIRGINIA": "VA", "MARYLAND": "MD", "MISSOURI": "MO",
    "MICHIGAN": "MI", "MINNESOTA": "MN", "TENNESSEE": "TN", "ALABAMA": "AL",
    "LOUISIANA": "LA", "SOUTH CAROLINA": "SC", "NORTH CAROLINA": "NC",
    "OKLAHOMA": "OK", "ARKANSAS": "AR", "KANSAS": "KS", "IOWA": "IA",
    "WISCONSIN": "WI", "INDIANA": "IN", "KENTUCKY": "KY", "NEW MEXICO": "NM",
    "HAWAII": "HI", "ALASKA": "AK", "MAINE": "ME", "VERMONT": "VT",
    "NEW HAMPSHIRE": "NH", "RHODE ISLAND": "RI", "DELAWARE": "DE",
    "WEST VIRGINIA": "WV", "MISSISSIPPI": "MS", "NEBRASKA": "NE",
    "WYOMING": "WY", "SOUTH DAKOTA": "SD", "NORTH DAKOTA": "ND",
}

COVERAGE_BANDS = [(0, 250_000, "up to $250k"), (250_000, 500_000, "$250k-500k"),
                  (500_000, 1_000_000, "$500k-1M"), (1_000_000, 10**12, "$1M+")]


def statutory_tax(state, year):
    """Statutory surplus lines tax for a state, as (pct_of_taxable_base, flat_dollars).

    Returns None for any state whose rate has not been verified — those rows are
    left as recorded rather than filled with a borrowed rate. Adding a state here
    is the ONLY way to make its cells comparable to FEMA policyCost, and it
    requires a primary source, not an inference from this book.

    THE TAXABLE BASE IS PREMIUM PLUS FEES, NOT PREMIUM ALONE, and every source
    below says so independently:
      CA — measured: on 250 rows carrying TaxableAmount, tax/TaxableAmount is
           exactly 3.0000% and stamping/TaxableAmount exactly 0.1800%, with
           TaxableAmount at 117.86% of premium.
      WA — Surplus Line Association of Washington, verbatim: "State tax and
           stamping fee are based on the sum of all premiums and fees, including
           but not limited to policy, broker and/or inspection fees."
      OR — Surplus Line Association of Oregon: premium tax "2% of premium and
           fees/charges", fire marshal tax "0.3% of premium and fees/charges".
      AZ — A.R.S. 20-416: "three percent of the gross premiums, including policy
           fees other than stamping fees".

    Each state's observed ratio against premium alone lands at almost exactly the
    statutory rate x 1.20, which is the policy fee as a share of premium — CA 3.59%
    against 3%, WA 2.41% against 2%, OR 2.42% against 2%. Three states agreeing on
    the same uplift is what makes the base credible rather than fitted.
    """
    if state == "CA":
        # 3% surplus lines tax + 0.18% stamping fee (Aaron, 13 Aug 2026).
        return 0.03 + 0.0018, 0.0
    if state == "WA":
        # 2% state tax, plus a stamping fee that DEPENDS ON POLICY INCEPTION DATE:
        # the WSLA board raised it from 0.10% to 0.30% effective 1 Jan 2025, and
        # later transactions keep the rate from the original inception date. This
        # book spans 2023-2026, so roughly half of it predates the increase and a
        # single rate would be wrong for one half or the other.
        #
        # Where the year is unknown the newer, higher rate is used: that overstates
        # private cost slightly, and overstating our own side is the safe direction
        # for a savings claim.
        stamping = 0.0030 if (year is None or year >= 2025) else 0.0010
        return 0.02 + stamping, 0.0
    if state == "OR":
        # 2% premium tax + 0.3% fire marshal tax, both on premium and fees, plus a
        # FLAT $10 Surplus Lines Service Charge per policy — not a percentage. The
        # book agrees: Oregon's recorded stamping fees have a median of exactly
        # $10.00. The charge applies to new and renewal transactions and not to
        # endorsements, which is automatically satisfied here because endorsements
        # were dropped before this point.
        return 0.02 + 0.003, 10.00
    if state == "AZ":
        # 3% of gross premiums including policy fees (A.R.S. 20-416), plus a 0.20%
        # stamping fee. The 3% is statutory and verified; the stamping figure comes
        # from a secondary source and is worth ~$1.60 on a $800 policy, so it moves
        # nothing material either way — flagged rather than relied upon.
        return 0.03 + 0.0020, 0.0
    return None


TAX_SOURCES = {
    "CA": "3% SL tax + 0.18% stamping (Aaron, 13 Aug 2026); base confirmed against "
          "the TaxableAmount column at exactly 3.0000%/0.1800%",
    "WA": "2% state tax + stamping 0.10% pre-2025 / 0.30% from 1 Jan 2025 (Surplus "
          "Line Association of Washington); base is premiums plus policy, broker "
          "and inspection fees, per WSLA verbatim",
    "OR": "2% premium tax + 0.3% fire marshal tax on premium and fees, plus a flat "
          "$10 Surplus Lines Service Charge per policy (Surplus Line Association "
          "of Oregon)",
    "AZ": "3% of gross premiums including policy fees (A.R.S. 20-416); 0.20% "
          "stamping fee is from a secondary source and is immaterial (~$1.60)",
}


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
    ap.add_argument("--root", required=True, help="bordereaux folder")
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
                # without both are filing summaries or tax registers, not policy
                # listings (the SLIP invoice register is correctly skipped here).
                if "premium" not in m or "state" not in m:
                    skipped += 1
                    log.append(f"SKIP {os.path.relpath(f, a.root)} [{sh}] "
                               f"no premium+state; cols={len(df.columns)}")
                    continue
                keep = {canon: df[col] for canon, col in m.items()}
                sub = pd.DataFrame(keep)
                sub["_src"] = os.path.relpath(f, a.root)
                # Whether the geography is the RISK location or merely the
                # insured's MAILING address. The legacy carrier layouts carry
                # City/County for the risk; the Instanda layout carries only
                # "Insured Mailing Address (City)" and no county at all. For a
                # landlord those are different places, so mailing-derived rows
                # must never feed a city or county cell.
                city_col = squash(m.get("city", ""))
                sub["_geo"] = "mailing" if "mailing" in city_col else "risk"
                frames.append(sub)
                log.append(f"OK   {os.path.relpath(f, a.root)} [{sh}] "
                           f"{len(sub)} rows, geo={sub['_geo'].iloc[0] if len(sub) else '-'}, "
                           f"fields={sorted(m)}")
        except Exception as e:
            skipped += 1
            log.append(f"FAIL {os.path.relpath(f, a.root)}: {str(e)[:90]}")

    if not frames:
        sys.exit("  No parseable bordereaux found. Check --root.")
    d = pd.concat(frames, ignore_index=True)
    print(f"  parsed {len(d):,} rows from {len(frames)} sheets ({skipped} skipped)")

    # ── DROP NON-POLICY TRANSACTIONS FIRST ─────────────────────────────────
    # This has to happen BEFORE the dedupe. An endorsement usually shares its
    # Certificate Ref with the original policy, so deduping first would keep the
    # endorsement (it sorts last) and throw the real premium away.
    before = len(d)
    txn_dropped = {}
    for col in ("new_renewal", "txn_type", "sale_stage"):
        if col not in d:
            continue
        v = d[col].astype(str).map(squash)
        bad = v.isin(TXN_EXCLUDE) | v.str.contains(
            "endorse|cancel|return|reinstate", regex=True, na=False)
        txn_dropped[col] = int(bad.sum())
        d = d[~bad]
    print(f"  dropped non-policy transactions (endorsements/cancellations): "
          f"{before:,} -> {len(d):,}  {txn_dropped}")

    # ── DE-DUPLICATE ───────────────────────────────────────────────────────
    # The folders contain revised and duplicated files: "May 2025 QBE BDX.xlsx"
    # alongside "May 2025 QBE BDX REV 07-09-25.xlsx", "Old" copies, a Dropbox
    # "conflicted copy", and "QBE BDX June 2025.xlsx" filed under BOTH June and
    # July. The Instanda-era monthly files also restate earlier months: 206 of
    # 795 certificate refs there repeat, some up to four times. Concatenating
    # them double-counts policies and would quietly skew every published figure.
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

    # Keep the carrier for an internal-only quality check. Only the Instanda-era
    # layout has a CarrierName column, so fall back to the source filename, which
    # names the carrier reliably across the whole book ("2024-08-QBE.xlsx"). This
    # is what makes the check able to catch a carrier that silently failed to
    # parse — the pooled median would otherwise hide it.
    if "carrier" in d:
        carrier = d["carrier"].astype(str).str.strip()
    else:
        carrier = pd.Series("", index=d.index)
    from_name = d["_src"].astype(str).str.extract(
        r"(?i)(QBE|BRIT|Hiscox|Instanda|H2Quoter|RBIA|CFIS)", expand=False)
    blank = carrier.isin(["", "nan", "NaN", "None"]) | carrier.isna()
    carrier = carrier.mask(blank, from_name).fillna("unknown").str.title()

    # Guarantee no identifying column survived the alias mapping. The internal
    # policy id goes too, now that dedupe has used it.
    for c in list(d.columns):
        if c == "_polid" or any(bad in squash(c) for bad in FORBIDDEN):
            d = d.drop(columns=[c])

    n = lambda c: pd.to_numeric(d[c], errors="coerce") if c in d else np.nan
    d["_prem"] = n("premium")
    fee_cov = {}
    for comp in ("policy_fee", "sl_tax", "stamping_fee", "fire_tax"):
        if comp in d:
            vals = n(comp)
            fee_cov[comp] = int(vals.notna().sum())
            d["_" + comp] = vals.fillna(0)
        else:
            fee_cov[comp] = 0
            d["_" + comp] = 0.0
    # As recorded in the files. For most rows this is premium + policy fee only,
    # because the legacy carrier layouts have no tax columns at all.
    d["_total_recorded"] = (d["_prem"] + d["_policy_fee"] + d["_sl_tax"]
                            + d["_stamping_fee"] + d["_fire_tax"])

    # Year has to exist before the tax model, because Washington's stamping fee
    # depends on the policy inception date.
    if "eff_date" in d:
        d["_year"] = pd.to_datetime(d["eff_date"], errors="coerce").dt.year
    else:
        d["_year"] = np.nan

    # State has to be normalised BEFORE the tax model, because the tax model is
    # per-state. "CALIFORNIA" and "CA" are the same jurisdiction and must share a
    # measured rate.
    if "state" in d:
        st = d["state"].astype(str).str.strip().str.upper()
        d["state"] = st.map(lambda x: STATE_MAP.get(x, x))

    # ── LOAD THE MISSING TAXES, PER STATE ───────────────────────────────────
    # Comparing a private total that omits surplus lines tax against FEMA's
    # fully-loaded `policyCost` would flatter the private side — the same error as
    # comparing a bare premium to policyCost, just smaller. So the missing tax has
    # to be added back. But it CANNOT be added back at one blended rate.
    #
    # Per Aaron: surplus lines tax is state-specific, and so is the stamping fee.
    # Every state sets its own; some levy both, some only one, some neither. A
    # single book-wide average therefore inflates the low-tax states and deflates
    # the high-tax ones — and because the recorded-tax rows are not evenly spread
    # across states, that blended rate is really whichever state dominates them.
    # An earlier version of this script did exactly that and pushed a
    # California-weighted rate onto Washington, Arizona, Oregon and Texas rows.
    #
    # So: measure a rate SEPARATELY FOR EACH STATE, from that state's own recorded
    # rows, and only where there are enough of them. Where a state has too few, do
    # not model at all — leave the total as recorded and mark the row unloaded, so
    # a partly-loaded cell can never be silently compared against policyCost.
    # Refusing to fill a gap is the correct behaviour here; inventing a rate for a
    # state we have not measured is how a wrong number gets published.
    # ONLY states with an authoritative rate are modelled, and the rate is never
    # borrowed across state lines. California's rates come from Aaron: 3% surplus
    # lines tax and 0.18% stamping fee.
    #
    # The base is the TAXABLE AMOUNT — premium plus the other charges billed to the
    # insured — not premium alone. That is verified, not assumed: on the 250 CA rows
    # carrying a `TaxableAmount` column, tax/TaxableAmount is 3.0000% and
    # stamping/TaxableAmount is 0.1800%, exactly the statutory pair, and
    # TaxableAmount runs 117.86% of premium. Against premium alone the same rows
    # read 3.56% and 0.213% — inflated by precisely that ~17.9% of extra charges,
    # which the legacy layouts record as `Policy Fee`. So (premium + policy fee) is
    # the right base and the modelled figure is a real calculation.
    #
    # Everywhere else is left alone. The observed ratios in other states span 2.4%
    # (WA) to 7.4% (SC) on as few as one row, no authoritative rate is in hand, and
    # the taxable base cannot be reconstructed where the fee columns are missing.
    # Filling those gaps with a blended or borrowed rate is how a wrong number gets
    # published, so those rows stay AS RECORDED and are flagged unloaded. Refusing
    # to model is the correct behaviour, not a shortfall.
    d["_taxbase"] = d["_prem"] + d["_policy_fee"]
    has_tax = d["_sl_tax"] > 0
    d["_loaded"] = has_tax.copy()
    d["_modelled_tax"] = 0.0
    modelled_states, observed = {}, {}
    if "state" in d:
        for state_code, grp in d.groupby(d["state"]):
            rec = grp[grp["_sl_tax"] > 0]
            # Report what this state's own rows imply, as a CROSS-CHECK on the
            # statutory rate — not as the thing driving the model. Where a state is
            # modelled, the observed figure should land near the statutory rate
            # times ~1.20 (the policy fee as a share of premium); if it does not,
            # the base or the rate is wrong and this is where that shows up.
            if len(rec):
                observed[state_code] = {
                    "recorded_rows": int(len(rec)),
                    "observed_sl_tax_pct_of_premium": round(
                        100 * float((rec["_sl_tax"] / rec["_prem"]).median()), 3),
                    "observed_stamping_pct_of_premium": round(
                        100 * float((rec["_stamping_fee"] / rec["_prem"]).median()), 3),
                    "observed_median_stamping_dollars": round(
                        float(rec["_stamping_fee"].median()), 2),
                    "used_to_model": False,
                }
            # Model row by row, because Washington's stamping rate depends on the
            # policy's own inception year.
            fill = grp.index[grp["_sl_tax"] <= 0]
            if not len(fill):
                continue
            rates = {}
            for idx in fill:
                yr = d.at[idx, "_year"]
                yr = None if pd.isna(yr) else int(yr)
                st_rate = statutory_tax(state_code, yr)
                if st_rate is None:
                    continue
                pct, flat = st_rate
                d.at[idx, "_modelled_tax"] = d.at[idx, "_taxbase"] * pct + flat
                d.at[idx, "_loaded"] = True
                rates.setdefault((round(100 * pct, 4), flat), 0)
                rates[(round(100 * pct, 4), flat)] += 1
            if rates:
                modelled_states[state_code] = {
                    "rows_modelled": int(sum(rates.values())),
                    "rates_applied": [
                        {"total_pct_of_taxable_base": pct,
                         "flat_dollars_per_policy": flat, "rows": n}
                        for (pct, flat), n in sorted(rates.items())
                    ],
                    "applied_to": "premium + policy fee",
                    "source": TAX_SOURCES.get(state_code, "see statutory_tax()"),
                }
                if state_code in observed:
                    observed[state_code]["used_to_model"] = (
                        "no — statutory rate used; this is the cross-check")
    d["_total"] = d["_total_recorded"] + d["_modelled_tax"]
    tax_model = {
        "method": ("statutory rate per state, applied only to states where that rate is "
                   "known, on a base of premium + policy fee"),
        "base_verification": ("On 250 CA rows carrying TaxableAmount, tax/TaxableAmount = "
                              "3.0000% and stamping/TaxableAmount = 0.1800%, matching the "
                              "statutory rates exactly; TaxableAmount = 117.86% of premium."),
        "states_modelled": modelled_states,
        "observed_ratios_as_cross_check": observed,
        "rows_with_recorded_tax": int(has_tax.sum()),
        "rows_modelled": int((d["_modelled_tax"] > 0).sum()),
        "rows_left_unloaded": int((~d["_loaded"]).sum()),
        "note": ("Surplus lines tax and stamping fees are set state by state — some states "
                 "levy both, some one, some neither — so no rate is ever averaged across "
                 "states or carried from California to anywhere else. Only states with a "
                 "known statutory rate are loaded. Rows in every other state are left AS "
                 "RECORDED and marked unloaded. `loaded_pct` on each cell gives the share "
                 "carrying tax; only a cell at loaded_pct 100 is comparable to FEMA "
                 "policyCost, and a multi-state cell must not be compared at all."),
    }
    d["_bldg"] = n("bldg_limit")

    # ── NORMALISE THE CATEGORICAL KEYS ─────────────────────────────────────
    # Deductible arrives as "5,000", "$5,000", "5000" and "5000.0" — four spellings
    # of one value, which split into four cells and can each fall below MIN_N.
    if "bldg_deduct" in d:
        dd = pd.to_numeric(d["bldg_deduct"].astype(str)
                           .str.replace(r"[^0-9.]", "", regex=True), errors="coerce")
        # A deductible equal to the building limit, or below $250, is a data entry
        # error rather than a real term.
        dd = dd.where((dd >= 250) & (dd < d["_bldg"].fillna(np.inf)))
        d["_deduct"] = dd.map(lambda v: f"${v:,.0f}" if pd.notna(v) else None)

    # Occupancy uses two vocabularies: the legacy files say Owner / Tenant, the
    # Instanda files say Primary Home / Property Rented To Others / Secondary.
    # Aaron: "tenant vs owner means that some are landlord or rental properties vs
    # owner occupied." Verified empirically before trusting it — 99.7% of `Tenant`
    # rows carry a $250,000 BUILDING limit, so `Tenant` is the landlord of a rental,
    # not a renter insuring contents only. That distinction matters because the
    # NFIP's $250 HFIAA surcharge falls on exactly this group.
    OCC_GROUP = {
        "owner": "owner-occupied", "primary": "owner-occupied",
        "primaryhome": "owner-occupied", "owneroccupied": "owner-occupied",
        "tenant": "rental / non-owner-occupied",
        "propertyrentedtoothers": "rental / non-owner-occupied",
        "rental": "rental / non-owner-occupied",
        "secondaryseasonalhome": "secondary / seasonal",
        "secondary": "secondary / seasonal",
    }
    if "occupancy" in d:
        d["_occ_group"] = d["occupancy"].astype(str).map(
            lambda v: OCC_GROUP.get(squash(v)))
    d["_per100k"] = np.where(d["_bldg"] > 0, d["_total"] / (d["_bldg"] / 100_000), np.nan)
    d["_band"] = d["_bldg"].apply(band)
    # Loss of use is reported as a LIMIT, and 0 is a real, meaningful value --
    # it means the policy was written without the cover, not that the field was
    # left blank. Blank means the layout does not carry the column at all. Those
    # two are different facts and collapsing them would manufacture a take-up
    # rate out of the older files' silence.
    if "loss_of_use" in d:
        lou = n("loss_of_use")
        d["_lou"] = lou
        d["_lou_reported"] = lou.notna()
        d["_lou_has"] = lou.fillna(0) > 0
    else:
        d["_lou"] = np.nan
        d["_lou_reported"] = False
        d["_lou_has"] = False
    # `_year` is already set, above the tax model — Washington's stamping rate
    # depends on it, so it cannot be computed here.

    d = d[d["_prem"] > 0]
    if a.state.upper() != "ALL" and "state" in d:
        d = d[d["state"] == a.state.upper()]
    if carrier is not None:
        carrier = carrier.reindex(d.index)
    print(f"  {len(d):,} rows after filters (state={a.state})")
    if not len(d):
        sys.exit("  Nothing left after filtering. Check --state.")

    def stats(g, min_n):
        v = g["_total"].dropna()
        if len(v) < min_n:
            return None
        p = g["_per100k"].dropna()
        out = {"n": int(len(v)),
               "total_p25": round(float(v.quantile(.25)), 2),
               "total_median": round(float(v.median()), 2),
               "total_p75": round(float(v.quantile(.75)), 2)}
        rec = g["_total_recorded"].dropna()
        if len(rec):
            out["total_recorded_median"] = round(float(rec.median()), 2)
        # What share of this cell carries surplus lines tax, recorded or modelled
        # from its own state's rate. Anything below 100 is NOT comparable to FEMA
        # policyCost, and the number travels with the cell so that cannot be
        # overlooked.
        if "_loaded" in g:
            out["loaded_pct"] = round(100 * float(g["_loaded"].mean()), 1)
        if len(p) >= min_n:
            out.update({"per100k_p25": round(float(p.quantile(.25)), 2),
                        "per100k_median": round(float(p.median()), 2),
                        "per100k_p75": round(float(p.quantile(.75)), 2)})
        bl = g["_bldg"].dropna()
        if len(bl):
            out["median_building_limit"] = round(float(bl.median()), 0)
        return out

    # ── MINIMUM-PREMIUM STRUCTURE ──────────────────────────────────────────
    # Aaron, 13 Aug: "BRIT QBE and HISCOX all have low minimum premiums and X
    # zones often all fall in that minimum premium threshold."
    #
    # If that holds it explains the one thing the benchmark could not: why the CA
    # median sits at $822 with a tight IQR while an X-zone policy is said to run
    # nearer $475. A minimum-premium regime is not risk pricing at all — it is a
    # floor — so the low-risk business piles up on a single value instead of
    # spreading out. That shows up as a spike in the premium distribution, which
    # means the low-risk cohort can be identified WITHOUT geocoding: it is the
    # policies sitting at the floor.
    #
    # This block only measures and reports. It publishes no cell, because whether
    # "at the floor" is a fair proxy for "X zone" is exactly what the NFHL
    # geocoding has to confirm.
    prem_struct = {}
    if carrier is not None:
        for name, grp in d.groupby(carrier):
            p = grp["_prem"].dropna()
            if len(p) < 20:
                continue
            counts = p.round(0).value_counts().head(6)
            prem_struct[name] = {
                "n": int(len(p)),
                "min": round(float(p.min()), 2),
                "p1": round(float(p.quantile(.01)), 2),
                "p5": round(float(p.quantile(.05)), 2),
                "median": round(float(p.median()), 2),
                "most_common_premiums": [
                    {"premium": float(v), "rows": int(c),
                     "share_pct": round(100 * c / len(p), 1)}
                    for v, c in counts.items()
                ],
            }
    # Is the policy fee flat or proportional? Aaron's $475 arithmetic implies flat:
    # $350 premium + ~$110 fee = $460, times 1.0318 CA tax = ~$475. It matters,
    # because a flat fee is a much larger share of a small premium, which is why
    # the observed tax/premium ratio came to ~1.20x statutory at the median.
    fee_struct = {}
    if "_policy_fee" in d:
        fv = d.loc[d["_policy_fee"] > 0, "_policy_fee"]
        if len(fv):
            vc = fv.round(2).value_counts().head(8)
            fee_struct = {
                "rows_with_a_fee": int(len(fv)),
                "distinct_values": int(fv.round(2).nunique()),
                "most_common": [{"fee": float(v), "rows": int(c),
                                 "share_pct": round(100 * c / len(fv), 1)}
                                for v, c in vc.items()],
                "median": round(float(fv.median()), 2),
                "as_pct_of_premium_median": round(
                    100 * float((fv / d.loc[fv.index, "_prem"]).median()), 2),
                "verdict": ("flat" if fv.round(2).nunique() <= 5 else
                            "varies — check whether it scales with premium"),
            }

    risk_geo = int((d["_geo"] == "risk").sum()) if "_geo" in d else 0
    results = {"_meta": {
        "rows_analysed": int(len(d)),
        "state": a.state,
        "min_n": a.min_n,
        "min_n_city": max(a.min_n, MIN_N_CITY),
        "total_cost_definition": "gross premium + policy fee + surplus lines tax "
                                 "+ stamping fee + fire marshal tax, where present",
        "fee_coverage": fee_cov,
        "tax_model": tax_model,
        "premium_floor_by_carrier": prem_struct,
        "policy_fee_structure": fee_struct,
        "premium_floor_note": ("Measurement only, publishes nothing. If the low-risk book "
                              "sits at a carrier minimum premium, it appears as a spike on one "
                              "premium value rather than a spread -- which would identify the "
                              "low-risk cohort without geocoding. Whether 'at the floor' is a "
                              "fair proxy for 'X zone' is what the NFHL work has to confirm."),
        "fee_coverage_note": ("The legacy carrier layouts carry only Gross Premium and "
                             "Policy Fee; surplus lines tax and stamping fee appear only "
                             "in the Instanda-era files. Where they are absent the total "
                             "is premium+fee, which UNDERSTATES private cost and therefore "
                             "flatters any private-vs-NFIP comparison. Label accordingly."),
        "rows_with_risk_location": risk_geo,
        "rows_with_mailing_location_only": int(len(d)) - risk_geo,
        "geo_note": ("City and county cells are built ONLY from rows whose geography is the "
                     "risk location. The Instanda layout carries the insured's mailing "
                     "address instead, which for a landlord is a different place."),
        "selection_note": ("This book contains policies where private coverage was placed, "
                           "which happens when it beat the NFIP alternative. It is therefore "
                           "the outcome of shopping both, not a sample of private pricing."),
        "suppression_note": f"cells below n={a.min_n} are omitted, "
                            f"n={max(a.min_n, MIN_N_CITY)} for cities",
        "outlier_note": "Commercial schedules share these files with homeowner policies "
                        "(premiums range past $200,000 against a median near $600), so every "
                        "figure is a median with an interquartile range, never a mean.",
    }}
    results["overall"] = stats(d, a.min_n)

    # ── LOSS OF USE ────────────────────────────────────────────────────────
    # The NFIP does not offer this cover at any price, so it is the strongest
    # coverage argument we have. It is also the one most easily overstated.
    #
    # Measured on the Aug 1-9 2026 file before writing this: take-up is NOT
    # universal and it is NOT random -- it tracks the programme. Hiscox Custom
    # and Full Value carried a limit on every row; QBE carried none on 71%.
    # So "all our policies include loss of use" is false as a claim about
    # policies and roughly true as a claim about certain programmes. Anything
    # published has to say which.
    #
    # Denominator is rows whose layout REPORTS the field. Older carrier
    # bordereaux have no such column, and counting their silence as "no cover"
    # would halve the take-up rate for free.
    rep = d[d["_lou_reported"]]
    lou_block = {
        "rows_reporting": int(len(rep)),
        "rows_not_reporting": int(len(d) - len(rep)),
        "coverage_note": ("Denominator is rows from layouts that carry a loss-of-use "
                          "column. The RBIA-era carrier bordereaux do not, and their "
                          "absence is not evidence of no cover."),
        "publishable": bool(len(rep) >= a.min_n),
    }
    if len(rep):
        withc = rep[rep["_lou_has"]]
        lou_block["with_cover_n"] = int(len(withc))
        lou_block["with_cover_pct"] = round(100 * len(withc) / len(rep), 1)
        if len(withc) >= a.min_n:
            lv = withc["_lou"]
            lou_block["limit_when_present"] = {
                "median": round(float(lv.median()), 2),
                "p25": round(float(lv.quantile(0.25)), 2),
                "p75": round(float(lv.quantile(0.75)), 2),
                "min": round(float(lv.min()), 2),
                "max": round(float(lv.max()), 2),
                "distinct_values": int(lv.nunique()),
            }
        # By carrier, because the take-up rate is a property of the programme
        # rather than of the customer. A pooled percentage hides that entirely.
        if "carrier" in rep:
            bycar = {}
            for name, grp in rep.groupby(rep["carrier"].astype(str).str.strip().str.title()):
                if name in ("", "Nan", "None") or len(grp) < a.min_n:
                    continue
                g = grp[grp["_lou_has"]]
                bycar[name] = {
                    "n": int(len(grp)),
                    "with_cover_pct": round(100 * len(g) / len(grp), 1),
                    "median_limit_when_present": (round(float(g["_lou"].median()), 2)
                                                  if len(g) >= a.min_n else None),
                }
            lou_block["by_carrier_INTERNAL_ONLY"] = bycar
            lou_block["carrier_note"] = ("Carrier names are never published. This cut "
                                         "exists to show that take-up is programme-driven, "
                                         "so the site says 'depends on the programme' "
                                         "rather than quoting one blended percentage.")
    results["loss_of_use"] = lou_block

    # City and county come only from risk-location rows. Everything else may use
    # the whole frame.
    risk_only = d[d["_geo"] == "risk"] if "_geo" in d else d
    for label, col, min_n, src in [
            ("by_state", "state", a.min_n, d),
            ("by_county", "county", a.min_n, risk_only),
            ("by_city", "city", max(a.min_n, MIN_N_CITY), risk_only),
            ("by_zone", "zone", a.min_n, d),
            ("by_coverage_band", "_band", a.min_n, d),
            ("by_occupancy", "occupancy", a.min_n, d),
            ("by_year", "_year", a.min_n, d),
            ("by_construction", "construction", a.min_n, d),
            ("by_deductible", "_deduct", a.min_n, d),
            ("by_owner_vs_rental", "_occ_group", a.min_n, d),
            ("by_intermap_score", "imap", a.min_n, d)]:
        if col not in src or not len(src):
            continue
        bucket, suppressed = {}, 0
        key = src[col].astype(str).str.strip()
        # Two-letter state codes and flood zones are initialisms — title-casing
        # turns CA into "Ca" and AE into "Ae". Everything else (county, city,
        # occupancy) reads better title-cased.
        key = key.str.upper() if col in ("state", "zone") else key.str.title()
        # Carriers write the same county two ways -- "Marin" and "Marin County" --
        # and untreated they become two cells. Measured 14 Aug 2026: EIGHT
        # California counties were split this way, so every affected median was
        # computed on part of its data, and a county sitting just under the
        # suppression floor could be wrongly withheld. Strip the suffix so the
        # two spellings collapse into one county.
        if col == "county":
            key = key.str.replace(r"\s+County$", "", regex=True).str.strip()
        for name, grp in src.groupby(key):
            if name in ("", "Nan", "None"):
                continue
            s = stats(grp, min_n)
            if s:
                bucket[name] = s
            else:
                suppressed += 1
        results[label] = {"cells": bucket, "suppressed_cells": suppressed}

    # ── THE LIKE-FOR-LIKE BENCHMARK ────────────────────────────────────────
    # 91% of this book is a $250,000 building limit with a $5,000 deductible, so
    # that combination is not a contrivance — it is what the agency actually
    # writes, and holding it fixed removes coverage and deductible as
    # explanations for any price difference. This is the only cut a
    # private-vs-NFIP comparison should be built on: quote FEMA for the same
    # $250,000 / $5,000 policy in the same county and the two numbers mean the
    # same thing. Anything comparing pooled medians is comparing coverage mixes.
    bm = d[(d["_bldg"] == 250_000)]
    if "_deduct" in d:
        bm = bm[bm["_deduct"] == "$5,000"]
    benchmark = {"definition": "$250,000 building limit, $5,000 deductible",
                 "n": int(len(bm)),
                 "why": ("91% of the book sits at these terms, so fixing them removes "
                         "coverage mix as an explanation for price differences and gives "
                         "FEMA a directly quotable equivalent."),
                 "overall": stats(bm, a.min_n)}
    for label, col, min_n in [("by_owner_vs_rental", "_occ_group", a.min_n),
                              ("by_county", "county", a.min_n),
                              ("by_state", "state", a.min_n)]:
        srcb = bm[bm["_geo"] == "risk"] if col == "county" else bm
        if col not in srcb or not len(srcb):
            continue
        key = srcb[col].astype(str).str.strip()
        key = key.str.upper() if col == "state" else key.str.title()
        cells, supp = {}, 0
        for name, grp in srcb.groupby(key):
            if name in ("", "Nan", "None"):
                continue
            s = stats(grp, min_n)
            if s:
                cells[name] = s
            else:
                supp += 1
        benchmark[label] = {"cells": cells, "suppressed_cells": supp}
    results["benchmark_250k_5000ded"] = benchmark

    # ── THE ZONE CUT IS NOT PUBLISHABLE, AND SAYS SO IN THE FILE ────────────
    # `Flood Zone` exists only in the Hiscox layout and is populated on a tiny
    # fraction of rows. Whatever clears MIN_N here is a Hiscox-only sliver, and
    # Hiscox prices about a third below the pooled book — so these cells describe
    # one carrier's appetite, not the market. The tell is that AE (a Special Flood
    # Hazard Area) comes out CHEAPER than X (outside it), which inverts the actual
    # risk ordering and can only be sampling noise.
    #
    # Zone-stratified pricing needs the risk addresses geocoded against FEMA's
    # NFHL. Until that exists, this stays flagged rather than quietly available.
    if "by_zone" in results and results["by_zone"]["cells"]:
        results["by_zone"]["DO_NOT_PUBLISH"] = (
            "Hiscox-only sub-sample; n is at the floor and the AE-vs-X ordering is "
            "inverted against known risk. Derive zone by geocoding against FEMA NFHL "
            "before publishing anything zone-stratified.")

    with open(os.path.join(a.out, "aggregates.json"), "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    with open(os.path.join(a.out, "parse-log.txt"), "w") as fh:
        fh.write("\n".join(log))

    # Per-carrier cut: a data-quality check only, so that a carrier which failed
    # to parse cannot hide inside a pooled median. Written to its own file, which
    # .gitignore excludes — carrier-level pricing is not ours to publish.
    if carrier is not None:
        cc = {}
        for name, grp in d.groupby(carrier.str.title()):
            if name in ("", "Nan", "None"):
                continue
            s = stats(grp, a.min_n)
            cc[name] = s if s else {"n": int(len(grp)), "suppressed": True}
        with open(os.path.join(a.out, "internal-carrier-check.json"), "w") as fh:
            json.dump(cc, fh, indent=2, default=str)
        print("\n  CARRIER CHECK (internal only, not for publication):")
        for k, v in sorted(cc.items(), key=lambda kv: -(kv[1].get("n") or 0)):
            med = v.get("total_median")
            print(f"    {k:22s} n={v.get('n'):5d}" +
                  (f"  median ${med:,.0f}" if med else "  (suppressed)"))

    print(f"\n  wrote {a.out}/aggregates.json  and  parse-log.txt")
    o = results.get("overall")
    if o:
        print(f"\n  OVERALL  n={o['n']:,}   median total ${o['total_median']:,.0f}"
              f"   (IQR ${o['total_p25']:,.0f}-${o['total_p75']:,.0f})"
              + (f"   median per $100k ${o.get('per100k_median'):,.2f}"
                 if o.get("per100k_median") else ""))
    for k in ("by_state", "by_county", "by_city", "by_zone", "by_year"):
        if k in results:
            c = results[k]
            print(f"  {k}: {len(c['cells'])} published, {c['suppressed_cells']} suppressed")
    print("\n  Review aggregates.json before anything is published. Check parse-log.txt "
          "for FAIL lines — a carrier layout that silently failed to parse is the most "
          "likely way this produces a wrong number.")


if __name__ == "__main__":
    main()
