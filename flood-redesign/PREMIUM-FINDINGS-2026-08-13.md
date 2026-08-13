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
| **California** | **3,645** | **$822** | **$769 – $888** |
| Owner-occupied | 2,467 | $826 | — |
| Rental / non-owner-occupied | 1,139 | $820 | — |

California figures are **100% tax-loaded** and so are directly comparable to
FEMA's `policyCost`. **34 California counties** clear the n≥10 floor at
benchmark terms; 49 clear it on the unrestricted cut. Largest cells: Marin 370,
Orange 366, Los Angeles 342, Santa Clara 314, San Diego 248.

Pooled across all terms: California median **$794** (IQR $637–$864), **$337 per
$100,000** of building coverage.

Other states at benchmark terms are **as-recorded and NOT tax-loaded** — see the
surplus lines section below. WA $789 (n=317, 5% loaded), OR $813 (n=177, 4%),
AZ $816 (n=132, 9%), CT $1,092 (n=45, 24%), MA $918 (n=30, 17%), TX $579
(n=11, 73%). None of these may be compared against `policyCost`, and the
all-states pooled figure is only 77% loaded, so it must not be either.

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

**3. Surplus lines tax is loaded for California only, at the statutory rate —
never blended across states.** No legacy carrier layout has a tax column at all;
only the Instanda-era files carry `surpluslinestax` / `stampingfee`, so 595 rows
of 7,732 record it.

The first version of this run got the method wrong. It measured one book-wide
rate (3.59% of premium) and applied it to every row. Aaron caught it: **surplus
lines tax and stamping fees are set state by state — some states levy both, some
one, some neither.** Because the rows that record tax are overwhelmingly
Californian, that "average" was really California's rate imposed on Washington,
Arizona, Oregon and Texas. It inflated those states by roughly 3.2% each: WA
benchmark read $815 when the correct as-recorded figure is $789.

The method now:

- **California** is loaded at the statutory **3% surplus lines tax + 0.18%
  stamping fee**, applied to the taxable base of premium + policy fee.
- **Every other state is left exactly as recorded** and flagged unloaded. No rate
  is borrowed from California or averaged across states.

The base is verified rather than assumed. On the 250 CA rows carrying a
`TaxableAmount` column, `tax / TaxableAmount` is **3.0000%** and
`stamping / TaxableAmount` is **0.1800%** — the statutory pair exactly — and
`TaxableAmount` is **117.86% of premium**. That ~17.9% of extra charges is why
measuring against premium alone read 3.56% instead of 3%, and it is what the
legacy layouts record as `Policy Fee`. So premium + policy fee is the right base.

Each state's own observed ratio is still reported in `_meta.tax_model
.observed_ratios_not_used`, marked `used_to_model: false`. They are not usable:
they span 2.4% (WA) to 7.4% (SC) on as few as one row, and the taxable base
cannot be reconstructed where the fee columns are missing. Getting those states
right needs each state's statutory rate, not more arithmetic on this book.

Every cell now carries **`loaded_pct`**. Only a cell at 100 is comparable to
FEMA's `policyCost`; comparing an unloaded private total against it flatters the
private side, which is the same error as comparing a bare premium to
`policyCost`, just smaller.

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

## The page is not a price comparison — positioning, per Aaron 13 Aug

Price is the hook, not the argument. Aaron's framing, which the page has to
carry:

> We are pushing private because the claims process is generally much better.
> The NFIP is effectively the government. Private offers many more options, has
> more bells and whistles than the government policy, and many times is a much
> better option for the customer. We want to paint a picture that private is not
> only less expensive but offers more — **and that there are times when the NFIP
> is the right call and we can use them too.**

Three consequences for how the numbers get used.

**1. Lead with "more for less", not "less".** A page that only argues price
invites the reader to assume they are buying a stripped-down policy — which is
the exact objection the data cannot answer. The county table is evidence for the
price half; the coverage comparison carries the other half and is what stops
"cheap" from reading as "worse". This is the price rule from CONTENT-STRATEGY
applied in the other direction: paying less for coverage that answers is the
goal, and here we can show the coverage is broader, not narrower.

**2. Recommending the NFIP when it wins is the credibility play.** Saying
plainly that we quote both and sometimes place the NFIP is what makes the savings
claim believable — and it is simply true of how the agency operates. It also
pre-empts the obvious challenge, because Risk Rating 2.0 does sometimes come back
implausibly low, and the NFIP cannot decline anyone. Concretely, the NFIP is
sometimes the right answer when a private carrier declines or non-renews the
risk, and its guaranteed availability has no private equivalent. Named honestly,
that is a reason to trust the rest of the page.

**3. Every coverage-feature claim needs verifying against the policy forms
before it ships.** This is the same discipline as the existing rule about never
asserting what a state requires without checking. Candidate differentiators that
are checkable in the forms rather than matters of opinion — building limits above
the NFIP's $250,000 cap, replacement cost on contents, additional living expenses
/ loss of use, and waiting-period length — must each be confirmed against the
actual QBE, Brit and Hiscox wordings before appearing, because they differ by
carrier and by program (Hiscox alone runs Custom, Full Value, Excess and NFIP
Maximum). "The claims process is generally better" is the agency's experience of
twelve years, and should be written as experience, not dressed up as a statistic
we cannot source.

Do not name carriers on the page; describe the private market generically. The
per-carrier medians in this run are a parse check, not publishable content.

## Next

1. **FEMA comparator at benchmark terms** — `policyCost` for $250,000/$5,000 by
   California county, owner vs non-primary, so the two sides are like-for-like.
   California only, because California is the only state whose cells are fully
   tax-loaded.
1b. **Get the statutory surplus lines tax and stamping fee for WA, OR and AZ**
   (the three states with enough volume to matter) so their cells can be loaded
   and compared too. Until then the statewide brand has as-recorded figures only.
2. **Geocode risk addresses against FEMA NFHL** to derive zone. This is the
   critical path for the zone cut and has to run locally against the bordereaux.
3. **Verify FEMA's owner/rental field** before publishing that cut — the earlier
   `tenantIndicator` probe returned n=15 against 7,398, so it flags contents-only
   tenants, not landlords.
4. **Build the private-vs-NFIP coverage comparison** from the actual QBE, Brit
   and Hiscox wordings — the "more, not just cheaper" half of the argument. Each
   row has to be sourced to a form, per carrier and program.
5. Rebuild `/how-much-does-flood-insurance-cost/` around the county table *and*
   that comparison. It holds 19,311 impressions at position 17.4 because it
   answers generically.
6. Write the "when the NFIP is the right call" section — guaranteed availability,
   no declinations, and Risk Rating 2.0 occasionally coming back very low. This
   is what makes the savings claim credible rather than a sales line.
