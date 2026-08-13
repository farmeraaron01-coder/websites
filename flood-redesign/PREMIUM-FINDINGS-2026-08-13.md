# What private flood insurance actually costs — first full run

Run 13 Aug 2026 by `tools/premium-aggregate.py` over the RBIA bordereaux,
2023–2026. Sources were read locally and shredded; only the aggregates in
`premium-aggregates/` are committed.

## What went in

90 carrier bordereaux, four years, every carrier — **QBE, Brit, Hiscox** and the
newer Instanda-platform files. 9,149 raw rows became **7,732 policies** and
**5,632 California policies** after the filtering below.

Including every carrier was not a formality. On a like-for-like basis (same
$250,000 median building limit) the per-$100,000 medians are:

| Carrier | n (CA) | per $100k | median total |
|---|---|---|---|
| QBE | 4,171 | $327 | $809 |
| Brit | 786 | $289 | $637 |
| **Hiscox** | **185** | **$212** | **$510** |

Hiscox writes about **a third below** the pooled book at identical coverage.
A QBE-only analysis would have overstated the market's floor and understated
what shopping is worth — the whole point of a price page.

## The headline numbers

**The benchmark policy — $250,000 building limit, $5,000 deductible.** 91% of
the book sits at these terms, so this is not a contrivance; it is what the
agency actually writes. Holding it fixed removes coverage and deductible as
explanations for any price difference, and gives FEMA a directly quotable
equivalent.

| | n | median | IQR |
|---|---|---|---|
| **California** | **3,645** | **$824** | **$770 – $891** |
| Owner-occupied | 2,467 | $828 | $770 – $889 |
| Rental / non-owner-occupied | 1,139 | $822 | $780 – $894 |

**34 California counties** clear the n≥10 floor at benchmark terms; 49 clear it
on the unrestricted cut. Largest cells: Marin 370, Orange 366, Los Angeles 342,
Santa Clara 314, San Diego 248.

Pooled across all terms: California median **$796** (IQR $637–$866), **$337 per
$100,000** of building coverage.

Other states, benchmark terms: WA $815 (n=317), OR $841 (n=177), AZ $843
(n=132), CT $1,130 (n=45), MA $949 (n=30).

**Prices are drifting down**, not up: California medians run $810 (2023), $806
(2024), $785 (2025), $706 (2026).

## The finding worth building a page on

Owner-occupied $828 against rental $822 — **the private market barely
distinguishes them.** The NFIP charges a **$250 HFIAA surcharge** on
non-primary residences. That surcharge has no private equivalent, so for a
landlord it is $250 of pure additional NFIP cost before a single rating factor
is compared. This is the cleanest, most defensible version of the savings
argument on the site, and it needs no quote data to stand up.

## Five decisions that changed the numbers

Each of these was a way to be confidently wrong.

**1. Endorsements and cancellations are excluded (273 rows).** An endorsement is
a mid-term change carrying a partial premium — the 2023 files alone hold 52 of
them, down to **−$1,065**. A cancellation carries a return premium. Both drag a
median toward zero. They are dropped *before* deduplication, because an
endorsement usually shares its Certificate Ref with the original policy, so
deduping first would have kept the endorsement and thrown the real premium away.

**2. Deduplication removed 1,144 rows — 13% of the book.** The folders hold
revised files (`REV 07-09-25`, `REV 09-02-25`), `Old` copies, a Dropbox
*conflicted copy*, and `QBE BDX June 2025.xlsx` filed under **both** June and
July. The Instanda monthly files restate earlier months: 206 of 795 certificate
refs there repeat, some four times. Two September Hiscox files are byte-identical.
Summing them would have inflated every count by an eighth with nothing visible
to show it had happened.

**3. Surplus lines tax is modelled, from this book's own recorded rate.** No
legacy carrier layout has a tax column at all — only the Instanda-era files
carry `surpluslinestax` / `stampingfee`. Measured on the 595 rows that do record
them: surplus lines tax runs **3.59% of premium** (above the 3% statutory rate
because the taxable base includes the policy fee) and the stamping fee **0.21%**.
Those rates are applied to the rows whose layout omitted the columns. `total` is
the loaded figure, `total_recorded` the unloaded one — the unloaded California
median is $770 against $796 loaded.

This matters because FEMA's `policyCost` is fully loaded. Comparing an unloaded
private total against it flatters the private side, which is the same error as
comparing a bare premium to `policyCost`, just smaller.

**4. County and city cells use risk-location rows only.** The legacy layouts
carry `City`/`County` for the risk. The Instanda layout carries only
`Insured Mailing Address (City)` and **no county at all** — for a landlord that
is a different place entirely. 5,203 California rows have a true risk location;
429 are mailing-only and are excluded from geography cells while still counting
toward state and coverage cuts.

**5. `Tenant` means landlord, not renter — verified, not assumed.** Aaron said
the owner/tenant field distinguishes rentals from owner-occupied. The
counter-reading matters: in flood insurance "tenant" usually means a renter
buying contents-only cover, which would have made the rental cut meaningless.
**99.7% of `Tenant` rows carry a $250,000 *building* limit**, and renters do not
insure buildings. Confirmed.

## What is not publishable, and why

**The flood-zone cut. Do not use it.** `Flood Zone` exists only in the Hiscox
layout and is populated on 11 of 1,894 rows in the 2023 sample. Both surviving
cells sit at the n floor, and they come out **AE $476 / X $547** — a Special
Flood Hazard Area cheaper than land outside one, which inverts the actual risk
ordering. That is sampling noise from one carrier's appetite, not a market
signal. `aggregates.json` carries a `DO_NOT_PUBLISH` key on that node.

Zone-stratified pricing is the single most valuable missing cut, and it requires
geocoding the risk addresses against FEMA's NFHL. Until that exists, no
zone-level claim on the site can be sourced to this data.

**Carrier-level pricing is computed but never committed.** It is a data-quality
check — a carrier that silently failed to parse would otherwise hide inside a
pooled median. `.gitignore` excludes `internal-carrier-check.json`.

**Commercial schedules share these files with homeowner policies** (premiums
reach $248,650 against a median near $600). Every figure is a median with an
interquartile range, never a mean.

## On the "30–50%" claim

Nothing here yet supports a specific savings percentage, because the NFIP side
has not been computed at benchmark terms. What this run provides is the private
half of that comparison, at a defined policy, per county, with n attached.

The known-solid component is the **$250 non-primary surcharge**, which is a
published NFIP fee rather than an estimate. The rest needs FEMA `policyCost` for
$250,000/$5,000 policies in the same counties.

One caveat that survives any amount of data, and belongs on the page: this book
records policies the agency *placed*, which happens when private beat the NFIP.
It is the outcome of shopping both, not a sample of private pricing, so the gap
against the full NFIP population is an **upper bound** on any individual's
saving, not an estimate of it. Stated that way it is still the most useful
number a buyer can get — and a reader who works it out unaided will distrust
everything else on the page.

## Next

1. **FEMA comparator at benchmark terms** — `policyCost` for $250,000/$5,000 by
   California county, owner vs non-primary, so the two sides are like-for-like.
2. **Geocode risk addresses against FEMA NFHL** to derive zone. This is the
   critical path for the zone cut and has to run locally against the bordereaux.
3. **Verify FEMA's owner/rental field** before publishing that cut — the earlier
   `tenantIndicator` probe returned n=15 against 7,398, so it flags contents-only
   tenants, not landlords.
4. Rebuild `/how-much-does-flood-insurance-cost/` around the county table. It
   holds 19,311 impressions at position 17.4 because it answers generically.
