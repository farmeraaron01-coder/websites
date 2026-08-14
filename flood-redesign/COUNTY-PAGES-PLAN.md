# County cost content — the plan, 14 Aug 2026

Aaron's question: *"what pages are we adding with all the costs per county etc.
isn't that the magic that will propel us to page 1?"*

Short answer: the **data** is the magic. Fifty-eight pages is the wrong container
for it. This sets out what to build instead, and — more importantly — what could
make it fail.

---

## 1. What we actually have

Three per-county datasets, which together nobody else can assemble:

| dataset | coverage | uniqueness |
|---|---|---|
| **Our own private premiums** | 41 CA counties at n≥10; **31 counties** at like-for-like benchmark terms | Nobody else has this. It cannot be copied, scraped or bought. |
| **NFIP policy cost** (OpenFEMA) | all 58 counties (pull in progress) | Public, but almost nobody segments it by county at fixed terms |
| **HUD Fair Market Rents** | all 58 counties | Public, unused by any competitor in this context |

The private book at benchmark terms ($250,000 building / $5,000 deductible),
merged across county-name variants:

| county | benchmark n | | county | benchmark n |
|---|---:|---|---|---:|
| Marin | 382 | | Solano | 96 |
| Orange | 366 | | Butte | 75 |
| Los Angeles | 342 | | Santa Barbara | 50 |
| Santa Clara | 326 | | Sonoma | 43 |
| San Diego | 248 | | Sacramento | 32 |
| Santa Cruz | 184 | | Tulare | 29 |
| Contra Costa | 167 | | Monterey | 28 |
| San Mateo | 161 | | Kern | 26 |
| Lake | 119 | | Merced | 23 |
| San Bernardino | 118 | | Shasta | 22 |
| Alameda | 111 | | Tehama, SLO, Napa | 21 each |
| Riverside | 103 | | San Joaquin | 19 |
| Ventura | 103 | | El Dorado, Placer | 15 each |
| | | | Yolo 12, Yuba 11 | |

## 2. THE PROBLEM WITH THIS PLAN — read before the plan

**Our data is strongest where flooding is least famous.**

Marin has 382 benchmark policies. **Sacramento has 32.** Sacramento is the county
most associated with California flood risk, sits behind the most discussed levee
system in the state, and is where a large share of the search volume for
"flood insurance sacramento" will be. We are data-rich in coastal, affluent,
Bay-Area-adjacent counties and data-poor in the Central Valley.

That means the counties we can write most authoritatively about may not be the
counties people are searching for. **This is the single biggest risk in the plan
and I cannot resolve it without search volume data** — GSC credentials are not in
this environment, and I have not seen per-county impression data.

Three ways it could go:
- If demand tracks our data (coastal counties), the plan works as written.
- If demand concentrates in Sacramento / San Joaquin / Fresno, we can still write
  those pages, but the private-premium section — the only genuinely unique part —
  will be thin or suppressed exactly where it matters most.
- If demand is mostly statewide rather than county-level, the county pages are
  the wrong build entirely and the flagship page is the whole answer.

**Nothing should be built until this is checked against Search Console.**

## 3. What I recommend building

### Tier 1 — one flagship page (do this first, regardless)

Rebuild `/how-much-does-flood-insurance-cost/`, currently position 18 with 2,866
impressions and 20 clicks. It carries the **full county table**: private median,
NFIP equivalent at identical terms, and monthly displacement cost, per county.

Why this and not the county pages:

- It is already targeting the money query and already ranks, just badly.
- A data table is the thing other sites cite. Fifty county pages are not.
- It concentrates the unique data into one asset instead of diluting it across
  fifty-eight, which is the opposite of our current problem.

**Non-negotiables on this page**, from `COST-PAGE-ZONE-RULE.md`: never publish a
single blended average as the headline. Segment, or publish no number.

### Tier 2 — county pages for a shortlist, not the state

Build only where **both** conditions hold: real search demand (to be confirmed)
**and** benchmark n≥50, so the private figure is defensible.

On current data that shortlist is **sixteen counties**: Marin, Orange, Los
Angeles, Santa Clara, San Diego, Santa Cruz, Contra Costa, San Mateo, Lake, San
Bernardino, Alameda, Riverside, Ventura, Solano, Butte, Santa Barbara.

Each page must carry something only we have:

1. Private premium at benchmark terms for that county, with n disclosed
2. The NFIP figure at identical terms — the like-for-like comparison
3. HUD rent for that county — an official long-term unfurnished benchmark, NOT a displacement quote
4. Local flood history and geography, written not generated

If a county page would be items 1–3 with the numbers swapped and nothing else, it
should not exist.

### Tier 3 — fix the cannibalization first

This is unglamorous and it is probably worth more than either tier above.

- `/california-flood-insurance-quotes/` and `/cheap-flood-insurance-california/`
  carry ~7,600 words of purpose-built commercial content with **2 internal links
  each**, while the contact page has 123.
- Five near-duplicate California pages are splitting the head-term signal.

Adding fifty pages to a site that cannot decide which of five pages is its
California page will make the confusion worse, not better. **Sequence: fix the
links, then flagship, then counties.**

## 4. What we will not do

- **No page for a county below the suppression floor.** No exceptions, no
  "estimated" figures, no borrowing the statewide number and calling it local.
- **No template with a swapped variable.** That is the pattern Google's
  scaled-content policy targets, and with genuine data for a third of the state we
  would be visibly doing it.
- **No zone-based pricing claims.** Risk Rating 2.0 does not rate by zone. Zone
  sets whether cover is mandatory, not what it costs.
- **No promise about rankings**, internally or externally. The data is the
  strongest lever we have; that is a different statement from a guarantee.

## 5. How we would know it worked

- Flagship page moves from position 18 into the top 10 for its head term
- The head term resolves to one page, not five
- The orphaned commercial pages start receiving impressions
- Referring domains to the flagship table — the citation test
- Quote-form starts from county pages, which is the only measure that pays

## 6. Open questions I cannot answer here

1. **Per-county search volume.** Needs GSC. Determines whether tier 2 is worth
   building at all.
2. **Whether Sacramento-type counties can be served honestly** with a thin private
   figure and a strong NFIP figure, or whether that is a page we should not write.
3. **Cannibalization sequencing** — whether consolidating the five near-duplicates
   means merging, redirecting, or deliberately differentiating them.

---

# RED-TEAM REVIEW — accepted and rejected, 14 Aug 2026

First independent review returned. Verdict: *"directionally sound as a staged
test, but not yet safe as a publication methodology."* That is a fair reading and
most of it is accepted. Recorded here so the plan is not quietly rewritten.

## ACCEPTED — and one of them was a live defect

### 1. The NFIP data was wrong, and I had already pulled hours of it

The reviewer said FEMA's policy file is transactional and that renewals create
separate records. **Verified and correct.** My first pull returned
policyEffectiveDate spanning 2021-2026 for an annual product — the same house
counted once per renewal, across the Risk Rating 2.0 phase-in.

Measured on Alameda:

| | rows |
|---|---:|
| original transactional pull | **2,073** |
| policies actually in force at 2026-08-14 | **388** |

A **5.3x overstatement** of the county's policy count, and a median blended
across five rate regimes that described no actual year. The pull now filters
`policyEffectiveDate <= REF < policyTerminationDate` with cancelled policies
excluded, and REF is recorded with the data. All previously pulled data was
discarded rather than kept.

This is the single most valuable thing the review produced.

### 2. "Median of our book" is not "average cost in the county"

Accepted without reservation. Sample size reduces noise; it does nothing about
selection bias. We place private only when it wins, so our book records the
outcome of shopping, not a market price.

**Standing label for any published private figure:**

> Median premium among qualifying policies placed by our agency, for the stated
> coverage, deductible and period.

Never "average cost of flood insurance in Marin County."

### 3. n>=10 is a confidentiality floor, not a reliability standard

Accepted. These are two different questions and I had one number doing both jobs.
CMS suppresses below 11; our floor was one observation *looser* than that.

New rule: **n>=11 to publish anything** (aligns with the common convention), and
**n>=30 minimum for a standalone county point estimate**, n>=50 preferred. Always
with n, period, and interquartile range shown.

### 4. HUD FMR is not "what displacement actually costs"

Accepted, and this one had already reached the live page. The loss-of-use page
said a furnished month-to-month rental "generally costs more than these figures"
— an unsourced directional claim, which is the same error as publishing a
percentage premium, just softer. **Fixed on the live page**: it now states that
HUD measures unfurnished long-term rent, that displaced families need a different
market, and that we have no reliable published comparison, so the table is a floor
for planning rather than a quote.

### 5. Cannibalization is asserted, not evidenced

Accepted. "Five pages get impressions" and "the contact page outranked the
homepage" are consistent with cannibalization but do not establish it — a contact
page can legitimately win navigational intent. Internal-link repair is low risk
and proceeds. **Merging or redirecting the five pages is on hold** until we have
query-level evidence: exact query, ranking URL by date, whether URLs alternate.

### 6. Sacramento should not be skipped for lacking our data

Accepted, and this corrects the plan's logic. Letting our book decide which
counties deserve a page optimises for where we happened to write business rather
than where readers need information. Sacramento gets a page built on public data,
local levee and map context, and the NFIP comparison — **with no private median**
until the sample supports one.

### 7. Missing methodology governance

Accepted in full: observation window, snapshot date, dispersion, a stable
methodology URL, versioned tables, and a corrections policy. None of this was in
the plan. Nothing publishes without it.

### 8. Sixteen counties, not twelve

Plain arithmetic error in my own shortlist. Corrected above.

## NOTED, NOT YET ACTED ON

- **Cal. Ins. Code 790.03(b)** on untrue or misleading statements — cited as
  making claim wording a regulatory control rather than an SEO detail. Plausible
  and consistent with the direction we were already going, but **I have not read
  the section myself**, and it should be verified before being relied on.
- **The "like-for-like" comparison needs more controls** than coverage and
  deductible — contents, occupancy, primary vs secondary, new vs renewal, fee
  treatment. Correct in principle; needs working through against what both
  datasets actually carry.

## REJECTED / QUALIFIED

- **"Over-correcting from one bad experience" on page shape.** Partly fair, and
  the examples given (NerdWallet, ValuePenguin, EnergySage) do show large location
  sets working. But those are national brands with domain authority we do not
  have, and the reviewer also concedes the opposite shape works (Bankrate's
  single-state page, GAO's county interactive). The staged sequence — flagship
  first, prove demand, then build — already resolves this without committing
  either way. **No change.**
- **Traffic claims for those example page sets were explicitly "not verified"**
  by the reviewer, so they are illustrative, not evidence.

## What this changes about timing

The plan was already gated on Search Console data. It is now additionally gated on
rewriting the methodology. **Neither the flagship nor any county page publishes a
number until both are done.** The internal-link repair is unaffected and remains
the first thing to do.


---

# SECOND RED-TEAM REVIEW — 14 Aug 2026

Independent second read, five reports. Verified its load-bearing number directly
against OpenFEMA: **Sacramento 42,334 residential NFIP contracts in force, 30.1%
of California's entire residential book, 9.55% penetration, 81.13% inside SFHA.**
Exact match. Los Angeles 10,584; Santa Clara 8,141; Marin 4,542.

## THE FINDING NEITHER REVIEW MADE — our benchmark is not neutral across counties

Joining the second review's penetration data to my own in-force pull exposes a
defect in the comparison itself, not in the page plan:

| county | policies at our benchmark terms | all residential NFIP | benchmark as share of county book |
|---|---:|---:|---:|
| Santa Clara | 1,932 | 8,141 | **23.7%** |
| Marin | 666 | 4,542 | 14.7% |
| San Mateo | 452 | 3,346 | 13.5% |
| Alameda | 388 | 3,420 | 11.3% |
| Orange | 747 | 7,994 | 9.3% |
| Los Angeles | 654 | 10,584 | 6.2% |
| San Joaquin | 220 | 3,840 | 5.7% |
| **Sacramento** | **758** | **42,334** | **1.8%** |

**$250,000 is the NFIP's maximum building coverage.** Our benchmark therefore
selects the top-coverage tier — and the share of a county's market that sits there
varies more than thirteenfold. In Santa Clara nearly a quarter of buyers max out.
In Sacramento fewer than one in fifty do.

So a county-by-county table at benchmark terms would compare **the top 1.8% of
Sacramento's market against the top 23.7% of Santa Clara's** and present the result
as a like-for-like county comparison. It is like-for-like on the policy and wildly
un-like on the buyer. That is not a caveat to footnote; it is a reason not to build
that table in that form.

**Consequence for the flagship page:** the county table cannot be benchmark-only.
Either report each county on its own whole book (descriptive, and what NerdWallet
does — total written premium divided by policies in force), or keep benchmark terms
for the private-vs-NFIP comparison at **statewide** level where the mix effect is
bounded, and say plainly which is which. Probably both, clearly separated.

## ACCEPTED FROM REVIEW TWO

1. **My stated reason for avoiding 58 pages was the wrong policy.** The on-point
   one is doorway abuse, quoted verbatim from Google: *"Having multiple domain names
   or pages targeted at specific regions or cities that funnel users to one page"*
   and *"Creating substantially similar pages that are closer to search results than
   a clearly defined, browseable hierarchy."* Fifty-eight county pages funnelling to
   one quote form is that example almost literally, regardless of data richness.
   There is **no data-differentiation safe harbour** anywhere in Google's docs.

2. **The market already settled this for flood specifically.** NerdWallet runs 121
   location pages for auto insurance and **zero** county flood pages — it puts a
   county lookup on one page. ValuePenguin: ~11 state flood pages, no city ones.
   Insurify and LendingTree rank for county-modified flood queries with single
   *state* pages carrying full county tables. Our conclusion was right; the
   reasoning now has evidence behind it rather than one bad experience.

3. **County selection was backwards, and the correction is counter-intuitive.**
   Marin, Santa Clara County and San Joaquin County returned **zero dedicated broker
   pages** in their top-10. Sacramento has the densest commercial SERP in the state —
   three local agencies, city and county government, and a sitting member of
   Congress. So the highest-ROI pages are the data-rich, competition-empty coastal
   counties, not the famous flood county.

4. **We already run city pages.** San Diego, Fresno, Stockton and San Jose all
   surface in these SERPs. The plan was written as though county pages would be a
   new departure. They would not be — which raises the prior question of whether the
   existing city pages are working, before adding more.

5. **Query ambiguity is a real tactical trap.** "flood insurance orange county"
   currently returns Orange County, **Florida**. "Santa Clara County" splits between
   the county, the city, and the Santa Clara River in Ventura. Use city slugs where
   the county term is contaminated — San Jose over Santa Clara County, Stockton over
   San Joaquin County.

6. **n≥10 stands as a floor but needs a precision test.** There is no recognised
   standard for publishing a median: NCHS states its standards "were not developed
   to apply to other estimators, such as percentiles or means." Census publishes ACS
   medians at n=3. So we are already stricter than the closest federal precedent.
   Add an ACS-style test — suppress if the margin of error exceeds the estimate —
   and reserve n≥20–30 for any headline or county-to-county comparison. At n=10 the
   exact 95% interval spans the 2nd to the 9th of ten observations.

7. **Sacramento's claims history undercuts the intuition.** 42,334 policies have
   produced 3,863 lifetime claims and $38.7M paid. Sonoma has paid **$131.8M** on
   7,402 claims. Sacramento is a levee-protected, mandatory-purchase, rarely-floods
   market. The page should say so — it is more interesting than the cliché.

8. **Missing from the plan entirely:** a compliance/disclaimer architecture, the
   loss-of-use argument integrated into the cost page rather than siloed, a
   conversion baseline and call tracking before anything is built, and an off-site
   citation strategy — a linkable asset needs outreach, not just internal links.

9. **Sequencing should be parallel, not serial.** The internal-link repair is a
   week; the flagship is a month. Do not let the first gate the second.

## Where the two reviews disagree

Review one said build Sacramento on public data. Review two agrees but adds that
Marin should be built *first*, because it pairs our deepest data with an empty SERP.
Both agree Sacramento carries no private median. **Adopted: Marin first as the
proof of concept, Sacramento as the volume play on public data.**

## CORRECTION from Aaron, 14 Aug — the private/NFIP ratio is a misleading metric

> "my book is all over the country. if you took california only it would be spread
> out, that 42 is only in that one area"

Both halves check out, and together they invalidate how the second review framed
Sacramento.

**Our book was never built to saturate a county.** It is 7,692 policies across
**20 states**; California is 73% of it, spread over **49 county cells with the top
five accounting for only 43%**. There is no county where we are concentrated,
because we write where the quote wins rather than farming a territory. So the
review's "0.8 private policies per 1,000 NFIP contracts in Sacramento, against 84
in Marin" reads as a 100x failure in Sacramento when it is mostly a statement
about what kind of book this is. **Drop that ratio. It measures the wrong thing.**

**And the 42,334 is not a market of 42,334 shoppers.** Sacramento's SFHA
penetration is **81.13%**, against Marin's 38.01%. That is a saturated,
lender-compelled pool behind the levees — nearly everyone who must carry cover
already does. Demand there is compelled, not curious.

### What that changes — and the counterweight in our own data

The compelled reading actually makes Sacramento *more* interesting, not less: it is
42,334 households who are required to carry flood insurance, most of whom have
never been told private exists or that loss of use is only available there. That is
the site's whole thesis at maximum scale.

**But our own in-force pull is the check on that enthusiasm.** Sacramento's median
NFIP cost at benchmark terms is **$780 — the lowest of any large California
county**, against Marin's $2,102. Sacramento is the hardest county in the state to
beat on price, because heavy CRS discounts and levee accreditation have already made
the federal product cheap there.

So the honest Sacramento position is:

- **Not** a price argument. We will usually lose it, and saying otherwise would be
  the kind of claim that gets checked.
- **A coverage argument.** 42,334 compelled households, none of whom can buy loss of
  use at any price from the federal programme. Same for the $250,000 building cap.
- Written on public data, with **no private median**, because n=32 is n=32
  regardless of why.

Marin remains the first build — deepest data, empty SERP, and a price argument that
actually holds at $2,102.
