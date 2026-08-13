# The flood-zone rule for anything that publishes a price

Aaron, 13 Aug 2026. This governs the cost page, the rates page, and every premium
figure on either brand. It is a commercial constraint, not a presentation
preference.

## The rule

**Never publish a single blended average as the headline price.** Segment by flood
zone, or do not publish a number at all.

## Why a blended average costs us business

The two zone groups are different products bought by different people.

**A zones (AE, A, AO, AH…)** — high risk. Coverage is **mandatory** for anyone
with a federally backed mortgage. The buyer has no choice; they arrive needing a
policy and shopping on price and service.

**X zones** — lower risk. Coverage is **entirely optional**. Nobody requires it.
The buyer is deciding whether to spend anything at all.

Those two prices are far apart. Our pooled California benchmark median is **$822**,
but that pool is dominated by mandatory A-zone business. Aaron's read from twelve
years of writing this book is that **an X-zone policy runs around the $475 mark**.

Now picture the actual visitor. Someone reads about El Niño, gets uneasy, searches
what flood insurance costs, and is in an X zone. A page headlining $822 tells them
a number roughly **double** what they would really pay. They are a voluntary buyer
with no mandate forcing them forward, so they leave. We have converted a warm
enquiry into a bounce with our own data.

That is the whole point: publishing one average does not merely lose precision, it
**actively repels the best customer we have** — the one who is buying because they
chose to rather than because a lender made them.

The A-zone visitor is harmed less by a blended figure, because they have to buy
regardless. So the error is asymmetric, and it runs against us.

## The honest second half

An X zone is lower risk. It is **not** no risk, and the page has to say so — this
is what makes the optional purchase worth making rather than a shrug.

A large share of flood claims come from outside high-risk zones. **Do not publish a
percentage until it is verified against a primary FEMA source.** Aaron's figure is
30%; numbers between 25% and 40% circulate everywhere, usually unsourced and
shaded by whoever is selling. This is Task 3 of `KIMI-BRIEF-cost-page.md`. Until it
comes back with a FEMA URL attached, phrase the point qualitatively.

The same standard applies to the **$475** X-zone figure. It is Aaron's experienced
estimate and it is almost certainly directionally right, but it is not yet a
number this book has produced. It must not appear on the page as a data-derived
figure until the private zone split exists.

## What we can and cannot compute today

**Cannot: private premiums by zone.** `Flood Zone` exists only in the Hiscox layout
and is populated on about 11 of 1,894 rows. The one zone cut that clears the n
floor is Hiscox-only and comes out AE $476 / X $547 — a high-risk zone cheaper than
a low-risk one, which inverts reality and is plainly sampling noise. It is flagged
`DO_NOT_PUBLISH` in the aggregates and must stay that way.

**Can: NFIP premiums by zone, immediately.** FEMA's public `FimaNfipPolicies`
dataset carries `floodZoneCurrent` and `ratedFloodZone` alongside `policyCost`,
`hfiaaSurcharge`, `federalPolicyFee`, `iccPremium`,
`totalBuildingInsuranceCoverage`, `buildingDeductibleCode`, `countyCode` and
`primaryResidenceIndicator`. That is a zone-stratified, fully-loaded, citable NFIP
price by California county at benchmark terms, available now and requiring no
permission.

Note `primaryResidenceIndicator` is the correct field for the non-primary /
$250 HFIAA surcharge cut. `tenantIndicator` is **not** — it returned n=15 against
7,398 and flags contents-only renters, not landlords.

## Consequences, in priority order

1. **Geocoding the risk addresses against FEMA's NFHL is now the top data task.**
   It was filed as a nice-to-have for stratification. It is not: it is what stops
   the page from repelling voluntary buyers. Until it is done we cannot state a
   private X-zone price from our own book.

2. **Build the NFIP-by-zone table first.** It is public, citable and already
   available, and it establishes the zone axis on the page even before the private
   side can be split. It also delivers the like-for-like NFIP comparator.

3. **Structure the page around the zone question, not around an average.** The
   reader's first decision is "which zone am I in", because it determines both
   whether they have a choice and what they will pay. An address or map lookup
   belongs high on the page, not in a footnote.

4. **Consider splitting the content.** "What does it cost in an X zone, and is it
   worth it" and "it is mandatory in an A zone, here is what it costs and how not
   to overpay" are different questions from different searchers with different
   intent. One page trying to serve both is how we ended up at position 18.15.

5. **Every published figure carries its terms**: the zone, the coverage amount,
   the deductible, and n. A number without its terms is what made the old page
   generic enough to ignore.
