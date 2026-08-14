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

On current data that shortlist is about **twelve counties**: Marin, Orange, Los
Angeles, Santa Clara, San Diego, Santa Cruz, Contra Costa, San Mateo, Lake, San
Bernardino, Alameda, Riverside, Ventura, Solano, Butte, Santa Barbara.

Each page must carry something only we have:

1. Private premium at benchmark terms for that county, with n disclosed
2. The NFIP figure at identical terms — the like-for-like comparison
3. HUD rent for that county — what displacement actually costs there
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
