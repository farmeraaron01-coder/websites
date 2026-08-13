# Flood Insurance SERP Teardown — Four California Cost Queries

Method: organic-style results pulled via `pplx_sdk.search.web` (one call per query, 10 results returned per query — all four queries returned a full 10, none short). Every page below was then fetched with `pplx_sdk.content.fetch` and all quotes are verbatim from the fetched content. Queries:

- **Q1** = `how much does flood insurance cost in california`
- **Q2** = `california flood insurance cost`
- **Q3** = `average cost of flood insurance california`
- **Q4** = `flood insurance rates california`

**Unique URLs across all four SERPs: 14.** Ads, AI Overview, and PAA boxes excluded.

---

## FLAG — URLs ranking on multiple queries (the real competitive set)

Seven URLs rank on **all four** queries. These are the pages to beat:

| URL | Queries | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|---|
| [LendingTree — California flood insurance](https://www.lendingtree.com/home-insurance/california-flood-insurance/) | 4/4 | 1 | 1 | 1 | 1 |
| [ValuePenguin — California](https://www.valuepenguin.com/flood-insurance/california) | 4/4 | 5 | 3 | 2 | 4 |
| [Policygenius — How much is flood insurance in California](https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/) | 4/4 | 6 | 4 | 4 | 5 |
| [Insuranceopedia — California](https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california) | 4/4 | 3 | 6 | 5 | 6 |
| [Out of the Storm News — CA costs](https://outofthestormnews.com/flood-insurance/costs/california) | 4/4 | 8 | 5 | 3 | 2 |
| [Insurify — California guide](https://insurify.com/homeowners-insurance/california-flood-insurance/) | 4/4 | 2 | 7 | 6 | 10 |
| [StateCalc — CA calculator](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/) | 4/4 | 9 | 9 | 10 | 7 |

LendingTree holds **#1 on all four queries**. The client's own cost page ([californiafloodinsurance.com/how-much-does-flood-insurance-cost/](https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/)) ranks on three of four (Q1 #4, Q2 #2, Q3 #7) and its sibling rates page takes Q4 #3 — so the site already owns two of the four intents but is absent from Q3's top 5.

---

## Section A — Ranking table (all 14 URLs)

| URL | Site | Type | Q1 | Q2 | Q3 | Q4 | # queries |
|---|---|---|---|---|---|---|---|
| https://www.lendingtree.com/home-insurance/california-flood-insurance/ | LendingTree | aggregator/lead-gen (marketplace) | 1 | 1 | 1 | 1 | 4 |
| https://www.valuepenguin.com/flood-insurance/california | ValuePenguin | comparison site (LendingTree-owned) | 5 | 3 | 2 | 4 | 4 |
| https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/ | Policygenius | aggregator/lead-gen (brokerage) | 6 | 4 | 4 | 5 | 4 |
| https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california | Insuranceopedia | other — editorial reference/wiki | 3 | 6 | 5 | 6 | 4 |
| https://outofthestormnews.com/flood-insurance/costs/california | Out of the Storm News | news / data publisher | 8 | 5 | 3 | 2 | 4 |
| https://insurify.com/homeowners-insurance/california-flood-insurance/ | Insurify | aggregator/lead-gen (comparison) | 2 | 7 | 6 | 10 | 4 |
| https://statecalc.com/flood-insurance/california-flood-insurance-calculator/ | StateCalc | other — calculator/tool site | 9 | 9 | 10 | 7 | 4 |
| https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/ | California Flood Insurance | broker (client) | 4 | 2 | 7 | — | 3 |
| https://www.floodprice.com/california-flood-insurance | FloodPrice | aggregator/lead-gen (agency quote tool) | 10 | 10 | 8 | — | 3 |
| https://coverforgeusa.com/states/california/flood | Cover Forge USA | comparison site | — | 8 | — | 8 | 2 |
| https://californiafloodinsurance.com/flood-insurance-rates/ | California Flood Insurance | broker (client) | — | — | — | 3 | 1 |
| https://www.insurance.com/home-and-renters-insurance/flood-insurance/flood-insurance-in-california | Insurance.com | comparison site | 7 | — | — | — | 1 |
| https://www.insuredbetter.com/l/california/flood-insurance/ | InsuredBetter | aggregator/lead-gen | — | — | 9 | — | 1 |
| https://expressfinancial.net/p/flood-insurance-california | Express Financial & Insurance Services | broker/agency | — | — | — | 9 | 1 |

Headline-figure spread across the set: **$779 → $1,240.27** for the "statewide average," plus range-based pages ($500–$2,000; ~$780; ~$840). No two top-ranked pages agree on the number.

---

## Section B — Per-page dossier

#### LendingTree — https://www.lendingtree.com/home-insurance/california-flood-insurance/
- Query ranks: Q1=1, Q2=1, Q3=1, Q4=1
- Site type: aggregator/lead-gen (lending & insurance marketplace)
- Dollar figure: Yes
- Exact quote: "**The average cost of flood insurance in California is $78 a month.**" and "Flood insurance in California costs $942 a year through the National Flood Insurance Program (NFIP), or $78 a month."
- Source attribution: "Flood insurance rates are based on FEMA data for existing policies as of April 30, 2025. Rates are shown for comparative purposes only. Your rates are likely to be different."
- Breakdown by: flood zone (A, A99, AH, AO, VE, B/C/X monthly rates); county (all 58 counties, annual + monthly); program/carrier type (NFIP $78/mo vs private $87/mo). Not by city, coverage amount, home value, or deductible.
- Word count (est): ~1,300 (plus a 58-row county table)
- Tables: 2
- FAQ: 0 questions (no FAQ block; one question-style H3, "How do flood insurance waiting periods work?")
- Calculator/quote form: No calculator; a repeated "Currently Insured? It's free, simple and secure." lead widget appears twice
- H2 headings (7 total):
  1. "How much does flood insurance cost in California"
  2. "California flood insurance costs by zone"
  3. "Is flood insurance required in California?"
  4. "What does flood insurance cover?"
  5. "How to get flood insurance quotes in California"
  6. "How to save money on California flood insurance"
  7. "Methodology"
- Last updated: Not shown as an "Updated" string; data-vintage string on page is "Flood insurance rates are based on FEMA data for existing policies as of April 30, 2025." (published_date in metadata: 2025-07-07)
- Short note: The strongest page in the set on data granularity — county-level rates for all 58 counties plus a zone table, both monthly and annual, with an explicit methodology and FEMA data date. It leads with a monthly figure ($78) rather than annual, which reads cheaper than every competitor's annual number. Weakness: no FAQ block and no interactive tool, so its win is pure data depth + domain authority.

#### ValuePenguin — https://www.valuepenguin.com/flood-insurance/california
- Query ranks: Q1=5, Q2=3, Q3=2, Q4=4
- Site type: comparison site (LendingTree-owned property)
- Dollar figure: Yes
- Exact quote: "The average cost of a National Flood Insurance Program policy in California is $811 per year." and "The average cost of flood insurance in California is $811 per year through the NFIP."
- Source attribution: "The average cost of flood insurance in California is $811 per year through the NFIP." — attributed only to the NFIP inline; no separate methodology or data-provider sentence (no Quadrant/LexisNexis citation)
- Breakdown by: city (10 cities, annual rate + % difference from state average); deductible (stated as a pricing factor, "NFIP flood insurance policies have deductibles between $1,000 and $10,000"); plus elevation, basement, proximity to water as narrative factors. No flood-zone or county pricing.
- Word count (est): ~1,000
- Tables: 1
- FAQ: 4 question prompts, but no explicit FAQ section heading ("How much does flood insurance cost in California?", "What does California flood insurance cover?", "Do you need flood insurance in California?", "Should I get flood insurance in California?")
- Calculator/quote form: None on page (only advice to compare NFIP vs private rates)
- H2 headings (5 total):
  1. "Find Cheap Homeowners Insurance Quotes in California"
  2. "How much does flood insurance cost in California?"
  3. "California flood insurance coverage"
  4. "Do you need flood insurance in California?"
  5. "About the Author"
- Last updated: Not shown
- Short note: Thin and old-bones (metadata published 2018) yet ranks top-5 on all four queries on domain strength plus one clean city table with % deltas — the % framing is its only real differentiator. Notably its own meta description says "$779 per year" while the body says "$811 per year," an internal inconsistency. No zone-level pricing at all, which is the gap a zone-segmented page can exploit.

#### Policygenius — https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/
- Query ranks: Q1=6, Q2=4, Q3=4, Q4=5
- Site type: aggregator/lead-gen (online brokerage, Zinnia-owned)
- Dollar figure: Yes
- Exact quote: "The average cost of flood insurance in California is $901 per year through the National Flood Insurance Program (NFIP), the federal government program that provides most flood insurance policies in the U.S."
- Source attribution: "Here are the average flood insurance rates in areas with a high risk, moderate to low risk, and undetermined risk, according to an analysis of NFIP premium data." — plus "Of the 50 California cities and towns with the most NFIP policyholders, these areas have the cheapest average flood insurance premiums in the state, according to our analysis." and a third-party risk citation: "…and as low as $458 per year in Elk Grove, a city with relatively minor flood risk, according to Risk Factor."
- Breakdown by: city (10 cheapest + 10 most expensive), flood zone (High risk A/V $1,161; Moderate-to-low B/C/X $622; Undetermined D $1,121), single blended state average. No county, home value, or carrier pricing.
- Word count (est): ~620
- Tables: 3
- FAQ: 0 questions (no FAQ section; one question-style H3, "How do FEMA and the NFIP set flood insurance rates?")
- Calculator/quote form: None; soft human CTA — "Our team of licensed insurance agents at Policygenius can help you compare policies and find the best option for you."
- H2 headings (3 total):
  1. "10 cheapest cities in California for flood insurance"
  2. "10 most expensive cities in California for flood insurance"
  3. "Flood insurance rates by flood zone in California"
- Last updated: Not shown
- Short note: The shortest page in the entire top-10 set (~620 words) and it still ranks 4th–6th on every query — proof that word count is not the ranking lever here. Its whole value proposition is three tight tables, including the cleanest zone-level average table in the set (A/V vs B/C/X vs D). The Malibu $3,533 outlier makes it the most quotable page for "expensive California city" angles.

#### Insuranceopedia — https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california
- Query ranks: Q1=3, Q2=6, Q3=5, Q4=6
- Site type: other — editorial reference/definitions site with insurance content
- Dollar figure: Hedged (a range, not a point estimate)
- Exact quote: "Flood insurance in California is not included in standard homeowners policies and must be purchased separately, with premiums currently ranging from around $811 to $901 or more per year depending on your property's flood zone and elevation."
- Source attribution: "The average cost of flood insurance in California ranges from around $811 to $901 per year, depending on the source and specific location within the state." Page-level source list: "FEMA – California Risk Rating", "FEMA – Cost Of Flood Insurance For Single-Family Homes", "California Department Of Insurance – Flood Insurance Resources"
- Breakdown by: flood zone (High Risk AE/VE $1,000–$2,000; Moderate Risk B/X $500–$1,000; Low Risk C/X $450–$650), city (three separate tables: average, cheapest, most expensive), partial county (Imperial County $2,247 appears inside a "cities" table). No coverage amount, deductible, home value, or carrier pricing.
- Word count (est): ~2,300
- Tables: 4
- FAQ: 3 questions ("What is the average cost of flood insurance in California?", "Is flood insurance legally required in California?", "Does homeowners insurance cover floods in California?")
- Calculator/quote form: No on-page calculator or form; refers out — "You can use online quote tools like the one offered by Insuranceopedia or consult with insurance brokers who deal with multiple insurance carriers, such as California Flood Insurance."
- H2 headings (8 total):
  1. "Key Takeaways"
  2. "How Much Is Flood Insurance In California?"
  3. "What does flood insurance cover in California?"
  4. "What does flood insurance not cover in California?"
  5. "How to Buy Flood Insurance in California"
  6. "Do I need flood insurance in California?"
  7. "FAQs"
  8. "About Bob Phillips"
- Last updated: "Updated: 16 March 2026"
- Short note: Openly synthesizes other publishers' numbers into an $811–$901 range rather than running its own data, and one table mixes a county (Imperial, $2,247) into a city list — a visible data-quality tell. Its ranking edge is breadth (~2,300 words, 4 tables, key-takeaways + FAQ + author bio) and a fresh visible update date. It also already links to the client by name, which is a live referral/relationship signal.

#### Out of the Storm News — https://outofthestormnews.com/flood-insurance/costs/california
- Query ranks: Q1=8, Q2=5, Q3=3, Q4=2
- Site type: news / data publisher (policy-news outlet publishing an NFIP data series)
- Dollar figure: Yes
- Exact quote: "**Average premium** $1,104" and "**Avg total cost (with fees)** $1,440" (dashboard-style key-facts block; also "+7.3%" year over year and "+12.4%" vs national average)
- Source attribution: "Source: FEMA OpenFEMA NFIP policy transaction data (FimaNfipPolicies)."
- Breakdown by: county (average premium, average total cost, policy count), month (13-month trend, May 2025–May 2026), premium vs premium-plus-fees. No flood zone, city, coverage amount, deductible, or carrier.
- Word count (est): ~1,000 (mostly table content; very little prose)
- Tables: 2
- FAQ: 0 questions
- Calculator/quote form: None. Offers a data download instead — "Download California CSV (california.csv) — free to reuse with attribution."
- H2 headings (6 total):
  1. "Key facts — May 2026"
  2. "California trend, last 13 months"
  3. "County breakdown — May 2026"
  4. "Use this data"
  5. "Related guides"
  6. "Nearby states"
- Last updated: Not shown as an update string; the page is dated by data period, "Key facts — May 2026"
- Short note: The only page in the set that reports a *premium-plus-fees* total ($1,440) and a year-over-year change, and the only one with a monthly time series — that recency signal is likely why it climbs to #2–#3 on the rate/average queries. It is pure data with almost no advice, no FAQ, and no conversion path, and it explicitly warns "Watch the policy count before reading much into small-county averages." Its $1,104 average sits far above LendingTree's $942 and Insurify's $779 because it averages newly written/renewed policies only.

#### Insurify — https://insurify.com/homeowners-insurance/california-flood-insurance/
- Query ranks: Q1=2, Q2=7, Q3=6, Q4=10
- Site type: aggregator/lead-gen (quote comparison marketplace)
- Dollar figure: Yes
- Exact quote: "The average cost of flood insurance in California is $779 per year, according to FEMA's National Flood Insurance Program."
- Source attribution: "The average cost of flood insurance in California is $779 per year, according to data from FEMA's National Flood Insurance Program (NFIP)." and for the county table: "Below are sample costs based on FEMA's "Cost of Flood Insurance for Single-Family Homes" data from the NFIP pricing approach."
- Breakdown by: county (56-row annual table, Merced $650 low to Sierra $1,987 high), flood zone (only as *home* insurance premium: "Not in flood zone" $100 vs "In flood zone" $167), carrier (home-insurance monthly quotes by company, not flood). Flood price itself is a single blended average plus county detail; no city, coverage-amount, or deductible pricing.
- Word count (est): ~2,900
- Tables: 3
- FAQ: 5 questions (section titled "California flood insurance FAQs", rendered as bullets: need for coverage, homeowners coverage of flood damage, checking flood zone, the 80/20 rule, filing a claim)
- Calculator/quote form: No calculator; two quote-comparison widgets — "Shop for Home Insurance in California" / "Check quotes from 120+ top insurance companies" and "Compare California Home Insurance Quotes"
- H2 headings (9 total):
  1. "Do you need flood insurance in California?"
  2. "Does homeowners insurance cover flooding?"
  3. "Cost of flood insurance in California"
  4. "What flood insurance covers in California"
  5. "How to buy flood insurance in California"
  6. "Tips for filing a flood insurance claim in California"
  7. "Average cost of home insurance in California"
  8. "California flood insurance FAQs"
  9. "Methodology"
- Last updated: The page shows the label "Updated" with no date after it — effectively "Not shown"
- Short note: Longest page in the set (~2,900 words) and the lowest headline figure ($779), directly cited to FEMA's single-family-home dataset. It dilutes flood intent by folding in a full *home* insurance cost section and a carrier quote table, which is why it wins Q1 (#2) but slides to #10 on the rates query. Only page here that offers an explicit methodology block plus a 5-question FAQ plus county data together.

#### StateCalc — https://statecalc.com/flood-insurance/california-flood-insurance-calculator/
- Query ranks: Q1=9, Q2=9, Q3=10, Q4=7
- Site type: other — programmatic calculator/tool site
- Dollar figure: Yes
- Exact quote: "This calculator starts from California's typical NFIP flood insurance premium of $964/year -- the median of the 1,000 most-recent real NFIP policies in California, computed directly from FEMA's own public OpenFEMA policy dataset."
- Source attribution: "California's typical NFIP premium is pre-filled from real, recent FEMA OpenFEMA policy data — the median of the most recent policies written in California." Data-source block: "FEMA OpenFEMA NFIP Redacted Policies (FimaNfipPolicies)" / "View Original Source | Verified | Updated annually"
- Breakdown by: flood zone (as multipliers — Moderate/Low ~0.84x, SFHA ~1.14x, coastal high-hazard ~1.27x of the blended median), coverage amount (building/contents vs the "$250,000/$100,000 statutory maximums"), deductible, residence type (HFIAA surcharge $25 primary / $250 non-primary), single blended median. No county, city, home value, or carrier.
- Word count (est): ~1,650
- Tables: 0
- FAQ: 5 questions ("How much is flood insurance in California?", "Do I need flood insurance in California?", "Does homeowners insurance cover flood damage?", "What is the HFIAA surcharge?", "What is the maximum NFIP flood insurance coverage?")
- Calculator/quote form: Yes — interactive NFIP premium calculator (inputs: typical state premium, building coverage, contents coverage, flood zone, deductible, residence type). Explicitly "This is a planning estimate, not a quote."
- H2 headings (11 total):
  1. "How This Calculator Works"
  2. "How to Use This Flood Insurance Calculator"
  3. "Example Calculation"
  4. "What Affects Your Results"
  5. "Tips for California Residents"
  6. "Frequently Asked Questions"
  7. "People Also Calculate"
  8. "Related Calculators"
  9. "More Flood Insurance (NFIP) Calculators"
  10. "More Calculators for California"
  11. "Compare California With Other States"
- Last updated: No date string; page shows "Updated annually"
- Short note: The only genuine interactive tool ranking on all four queries, and the only page that publishes explicit zone multipliers (0.84x / 1.14x / 1.27x) plus fee mechanics ($47 Federal Policy Fee, HFIAA surcharge) — a level of pricing transparency no editorial page matches. Zero tables; the value is the calculator plus a worked "Example Calculation." Its median-based $964 sits between the FEMA-average pages and the newly-written-policy averages.

#### California Flood Insurance (client) — https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/
- Query ranks: Q1=4, Q2=2, Q3=7, Q4=—
- Site type: broker (independent agency; the client)
- Dollar figure: Hedged (ranges only, explicitly disclaimed)
- Exact quote: "For a typical California home, flood insurance generally runs **$500 to $2,000 per year**." Supporting bands: "**Low-to-moderate risk (Zone X):** often **$400–$700/year**, sometimes less through a private policy."; "**Moderate risk near water or storm drains:** roughly **$700–$1,500/year**."; "**High-risk zones (Zone A/AE/V):** commonly **$1,500–$3,000+/year**, especially for older or low-elevation homes." Hedging language: "These are ranges, not quotes." and "Two homes on the same street can pay very different premiums based on elevation and construction."
- Source attribution: "None cited"
- Breakdown by: flood zone (X; A/AE/V; three risk bands), coverage amount (NFIP $250,000 building / $100,000 contents), deductible, carrier (private markets vs NFIP, multiple Lloyd's of London markets). No county, city, or home value. No single blended average.
- Word count (est): ~1,300
- Tables: 0
- FAQ: 5 questions ("How much does flood insurance cost per month in California?", "Why is my flood insurance so expensive in California?", "Is private flood insurance cheaper than the NFIP?", "Does Risk Rating 2.0 make flood insurance more expensive?", "How can I lower my flood insurance premium?")
- Calculator/quote form: No calculator; quote CTA — "Get your free flood insurance quote," with a licensed specialist comparing private markets and the NFIP
- H2 headings (8 total):
  1. "How much does flood insurance cost in California?"
  2. "What factors determine your flood insurance premium?"
  3. "What is Risk Rating 2.0 and how does it affect cost?"
  4. "Is private flood insurance cheaper than the NFIP in California?"
  5. "How can California homeowners lower their flood insurance cost?"
  6. "Do I even need flood insurance if I'm not in a high-risk zone?"
  7. "Frequently Asked Questions"
  8. "Get a flood quote for your property"
- Last updated: Not shown
- Short note: The only page in the top set that segments price by *risk band with dollar ranges* while refusing a false precision average — good for trust, weak for snippet capture, since Google's box prefers a single number with a source. It is the sole ranking page with zero tables and zero cited data source, a clear gap against LendingTree, Insurify, Out of the Storm and StateCalc, all of which name FEMA/OpenFEMA datasets. Strongest conversion architecture (quote CTA + private-vs-NFIP framing) of any page here.

#### California Flood Insurance (client) — https://californiafloodinsurance.com/flood-insurance-rates/
- Query ranks: Q1=—, Q2=—, Q3=—, Q4=3
- Site type: broker (independent agency; the client)
- Dollar figure: Yes (hedged with "about"/"~")
- Exact quote: "**California overall average:** about **$780 per year**." Also: "The California average is about $780 per year for $250,000 of building coverage, which is the maximum the NFIP offers." and "**Low-risk Zone X:** private flood rates can start **as low as ~$350 per year**."
- Source attribution: "None cited" — the only framing sentence is "Here's a simple "typical rates" snapshot for **$250,000 of building coverage** — the maximum the NFIP offers and the amount usually required if you're in a high-risk zone with a federally backed mortgage:"
- Breakdown by: flood zone (X; A, AE, AH, AO, V, VE), coverage amount ($250,000 building benchmark), deductible ("A higher deductible lowers your rate; a lower deductible raises it."), single blended average (~$780). No county, city, home value, or carrier-level pricing.
- Word count (est): ~1,500
- Tables: 0
- FAQ: 5 questions ("What is the average flood insurance rate in California?", "How much are flood insurance rates in a high-risk zone?", "What determines my flood insurance rate?", "Are private flood insurance rates lower than NFIP rates?", "How can I lower my flood insurance rate?")
- Calculator/quote form: No calculator or on-page form fields; quote service CTA — "**Want your real rate?** We'll shop your home across the NFIP and multiple private markets and show you the lowest rate side by side — usually the same day. Get your free flood insurance quote or call us at **855-225-3566**."
- H2 headings (8 total):
  1. "What are typical flood insurance rates in California?"
  2. "What determines your flood insurance rate?"
  3. "How does flood zone change your rate?"
  4. "How does Risk Rating 2.0 affect your rate?"
  5. "Is private flood insurance cheaper than the NFIP?"
  6. "How can you lower your flood insurance rate?"
  7. "Frequently Asked Questions"
  8. "Get a flood quote for your property"
- Last updated: Not shown
- Short note: Ranks #3 on the "rates" query only, and it is the one page that anchors its average to a stated coverage level ("about $780 per year for $250,000 of building coverage") — a genuinely better framing than competitors' unqualified averages. But $780 here versus the sibling page's "$500 to $2,000" range creates an internal inconsistency across the client's own two cost pages. No tables, no cited source, no update date.

#### FloodPrice — https://www.floodprice.com/california-flood-insurance
- Query ranks: Q1=10, Q2=10, Q3=8, Q4=—
- Site type: aggregator/lead-gen (agency quote-comparison platform)
- Dollar figure: Yes
- Exact quote: "The average cost of an NFIP policy in California is $1,240.27, but rates can vary substantially depending on where you live."
- Source attribution: "Source: FEMA" (plus table footnote "*NFIP Average Prices as of November 30th, 2025.")
- Breakdown by: city (10 cities, average cost per policy), single blended average ($1,240.27). Not by county, flood zone, coverage amount, home value, deductible, or carrier.
- Word count (est): ~820
- Tables: 1
- FAQ: 6 questions ("How do I Save Money on Flood Insurance in California?", "Do I Need Flood Insurance in California?", "Does My Homeowners Insurance Cover Flooding?", "When Should I Buy Flood Insurance?", "Do I Need a Flood Elevation Certificate?", "Can I Get Coverage for My Basement?") — presented as H2s rather than under an "FAQ" label
- Calculator/quote form: Yes — a "quick online quote tool" comparing NFIP and private flood quotes, costs and coverages side-by-side; also references a FEMA Flood Zone Lookup tool
- H2 headings (14 total):
  1. "Average Costs through the NFIP"
  2. "Check Out Our Customer Reviews"
  3. "NFIP vs. Private Flood Insurance"
  4. "Our Private Flood Insurance Prices Are Often Lower!"
  5. "Not Sure Whether to Choose an NFIP Policy or Private Flood Insurance?"
  6. "How do I Save Money on Flood Insurance in California?"
  7. "Do I Need Flood Insurance in California?"
  8. "Does My Homeowners Insurance Cover Flooding?"
  9. "When Should I Buy Flood Insurance?"
  10. "Do I Need a Flood Elevation Certificate?"
  11. "Can I Get Coverage for My Basement?"
  12. "Flood Insurance Pricing Changes in California"
  13. "Why Did the NFIP Implement Risk Rating 2.0?"
  14. "Compare NFIP with Private Flood Insurance Premiums Online"
- Last updated: Not shown ("*NFIP Average Prices as of November 30th, 2025." is the only date string)
- Short note: Highest headline number in the set ($1,240.27, quoted to the cent) and the most transactional structure — reviews, a private-vs-NFIP savings pitch, a live quote tool, and a phone number (866-503-5663). Its differentiator against the client is a shorter waiting period claim ("can be as short as 10 days") and an actual online quote comparison, not a callback. Thin on segmentation: one city table, no zone or county data.

#### Cover Forge USA — https://coverforgeusa.com/states/california/flood
- Query ranks: Q1=—, Q2=8, Q3=—, Q4=8
- Site type: comparison site (educational/state-data insurance site)
- Dollar figure: Yes
- Exact quote: "California has about ~190,000 active NFIP flood insurance policies, with an average annual premium of $840/yr under FEMA's Risk Rating 2.0 methodology." and "The average NFIP premium in California is approximately $840 per year under Risk Rating 2.0."
- Source attribution: "Data sourced from FEMA NFIP statistics and state Department of Insurance filings for California, April 2026." and "NFIP statistics from FEMA's national insurance data; premium averages reflect Risk Rating 2.0 phase-in."
- Breakdown by: flood zone / geographic risk profile (Zone X foothills "under $500"; Bay Area 100-year zones "$900–$1,800"; Delta/Central Valley "$1,500–$3,000+ annually"; Preferred Risk Policies "$400–$600" or "$400–$700/year"), single blended average ($840/yr). No county, city, coverage amount, deductible, home value, or carrier pricing.
- Word count (est): ~1,350
- Tables: 1
- FAQ: 3 questions ("Do I need flood insurance in California?", "How much does flood insurance cost in California?", "What floods are covered by flood insurance in California?")
- Calculator/quote form: No calculator or quote form; an email capture — "Get Insurance Rate Alerts" (state rate-change alerts, enrollment deadlines, premium tips, new coverage options)
- H2 headings (6 total):
  1. "California Flood Insurance Quick Facts"
  2. "Atmospheric Rivers, Delta Infrastructure, and California's Expanding Flood Risk"
  3. "What to Know About Flood Insurance in California"
  4. "Flood Insurance FAQs — California"
  5. "Related Guides"
  6. "Get Insurance Rate Alerts"
- Last updated: "Updated April 2026" (also "Fact-checked April 2026" and "Reviewed April 2026")
- Short note: The only page that segments price by named California *geography* rather than administrative units — Delta reclaimed land, Central Valley floodplains, Bay Area 100-year zones, foothill Zone X — which is far more persuasive to a local reader than a county table. It pairs that with policy-count context (~190,000 active policies) and visible Updated/Fact-checked/Reviewed stamps. No quote path at all, so it competes purely on editorial trust.

#### Insurance.com — https://www.insurance.com/home-and-renters-insurance/flood-insurance/flood-insurance-in-california
- Query ranks: Q1=7, Q2=—, Q3=—, Q4=—
- Site type: comparison site
- Dollar figure: Yes
- Exact quote: "The average cost of flood insurance in California for an NFIP policy is **$940 per year.** This means California flood insurance costs over $200 more annually than the national average."
- Source attribution: "None cited" for the $940 figure. Page-level sources listed: "National Flood Insurance Program. 'Do I need flood insurance?' Accessed August 2025" and "National Flood Insurance Program. 'Flood insurance providers.' Accessed August 2025"
- Breakdown by: flood zone (narratively — "high-risk areas — Zone V or A — being more expensive to insure"), coverage amount, deductible, carrier (NFIP vs private), single blended average. No county, city, or home value.
- Word count (est): ~740
- Tables: 0
- FAQ: 0 questions
- Calculator/quote form: None; CTA text only — "Get flood insurance quotes to see what works best for you."
- H2 headings (4 total):
  1. "Is flood insurance required in California?"
  2. "How much is flood insurance in California?"
  3. "Where to buy California flood insurance"
  4. "What companies offer flood insurance in California?"
- Last updated: Not shown (only source access strings "Accessed August 2025")
- Short note: The most generic page in the set — ~740 words, zero tables, zero FAQ, no data attribution for its $940 figure, and it ranks on only one of four queries. Its one distinctive move is framing California against the national average ("over $200 more annually"). This is the profile of a page vulnerable to displacement.

#### InsuredBetter — https://www.insuredbetter.com/l/california/flood-insurance/
- Query ranks: Q1=—, Q2=—, Q3=9, Q4=—
- Site type: aggregator/lead-gen (independent-agent network)
- Dollar figure: Yes
- Exact quote: "**The average cost of flood insurance in California is $938 per year,** or approximately $78 per month." and "This is a bit more expensive than the current national average flood insurance rate of $899 per year, or approximately $75 per month."
- Source attribution: "Local flood insurance rates are set by FEMA and the NFIP using the California flood insurance rate map." — the $938 figure is not directly attributed; the page lists sources `https://www.nerdwallet.com/insurance/homeowners/learn/flood-insurance-cost` and `https://firststreet.org/neighborhood/california-ca/188631_fsid/flood` without tying either to the figure
- Breakdown by: flood zone (as a stated factor, "Your home's flood zone designation"), coverage amount and deductible ("The deductible and amount of coverage you need"), single blended average. No county, city, home value, or carrier pricing.
- Word count (est): ~1,900
- Tables: 0
- FAQ: 4 questions ("What is the average cost of flood insurance in California?", "What is the best flood insurance company in California?", "Do you need flood insurance in California?", "Why work with an independent agent in California when shopping for flood insurance?")
- Calculator/quote form: No calculator or form; CTAs "Save on Flood Insurance" and "Our independent agents shop around to find you the best coverage"
- H2 headings (13 total):
  1. "Find the Best Flood Insurance Rates and Companies in California"
  2. "Key Takeaways - California Flood Insurance"
  3. "The Best Flood Insurance Companies in California"
  4. "How to buy flood insurance in California"
  5. "Is Flood Insurance Required in California?"
  6. "What Does Flood Insurance Cover in California?"
  7. "What's Not Covered by Flood Insurance in California?"
  8. "How Much Does Flood Insurance Cost in California?"
  9. "California Flood Zones"
  10. "The Best Flood Insurance Discounts in California"
  11. "How to Apply for Flood Insurance in California"
  12. "How to File a Flood Insurance Claim in California"
  13. "FAQs About California Flood Insurance"
- Last updated: Not shown
- Short note: ~1,900 words and 13 H2s with zero tables — breadth without data, and it only surfaces on one query (Q3 #9). Its distinctive angles are a "best flood insurance companies" list and a discounts section, both of which serve the independent-agent pitch rather than the pricing question. Cites a competitor (NerdWallet) and First Street as sources without attributing its own $938 figure.

#### Express Financial & Insurance Services — https://expressfinancial.net/p/flood-insurance-california
- Query ranks: Q1=—, Q2=—, Q3=—, Q4=9
- Site type: broker/agency (independent brokerage, Santa Monica, CA)
- Dollar figure: Yes, with an explicit hedge on the spread
- Exact quote: "California has roughly **190,000 active NFIP policies**, with an average premium around **$840 per year** under FEMA's Risk Rating 2.0 pricing." and "Public estimates for the state average range from about **$811 to $1,240** depending on the source and the mix of properties counted."
- Source attribution: "California has roughly **190,000 active NFIP policies**, with an average premium around **$840 per year** under FEMA's Risk Rating 2.0 pricing." — attribution is to FEMA Risk Rating 2.0 pricing and "public sources"; no named dataset, study, or data provider
- Breakdown by: flood zone / risk profile ("**Low-risk (Zone X):** private flood policies starting near **$350/year**"; "**Moderate-risk (AE zone):** commonly **$1,000–$2,500/year**, lower for properties well above base flood elevation"; "**High-risk / below base flood elevation:** **$3,000–$6,000+/year**"), program (NFIP vs private), single blended average ($840). No county, city, coverage amount, deductible, home value, or carrier pricing.
- Word count (est): ~750
- Tables: 0
- FAQ: 5 questions ("Does homeowners insurance cover flooding in California?", "How much is flood insurance in California?", "Do I need flood insurance if I am not in a flood zone?", "Is there a waiting period for flood insurance?", "Is private flood insurance better than NFIP?")
- Calculator/quote form: No calculator or form; "We quote both sides and compare them honestly." / "We quote both and show you the comparison." plus "call 310-453-5736 for a no-obligation review."
- H2 headings (5 total):
  1. "What Risk Rating 2.0 changed"
  2. "What it costs by risk profile"
  3. "The two California traps"
  4. "Related pages"
  5. "Find out what flood coverage would actually cost you"
- Last updated: Not shown; page states "figures shown are typical ranges as of mid-2026 from public sources."
- Short note: The single most intellectually honest page on the pricing disagreement — it names the spread ("about $811 to $1,240 depending on the source and the mix of properties counted"), which no editorial competitor does. Only ~750 words and 5 H2s, and it converts through a phone review rather than a form. Its "What it costs by risk profile" band structure is nearly identical to the client's own page, and it outranks nothing else — evidence that band-only pricing alone caps you around #9.

---

## Section C — Overlap summary (sorted by breadth)

**4 of 4 queries (7 URLs):**
1. https://www.lendingtree.com/home-insurance/california-flood-insurance/ — ranks 1, 1, 1, 1 (avg 1.0)
2. https://www.valuepenguin.com/flood-insurance/california — ranks 5, 3, 2, 4 (avg 3.5)
3. https://outofthestormnews.com/flood-insurance/costs/california — ranks 8, 5, 3, 2 (avg 4.5)
4. https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/ — ranks 6, 4, 4, 5 (avg 4.75)
5. https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california — ranks 3, 6, 5, 6 (avg 5.0)
6. https://insurify.com/homeowners-insurance/california-flood-insurance/ — ranks 2, 7, 6, 10 (avg 6.25)
7. https://statecalc.com/flood-insurance/california-flood-insurance-calculator/ — ranks 9, 9, 10, 7 (avg 8.75)

**3 of 4 queries (2 URLs):**
8. https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/ — Q1 4, Q2 2, Q3 7 (missing Q4, where the sibling rates page ranks #3)
9. https://www.floodprice.com/california-flood-insurance — Q1 10, Q2 10, Q3 8 (missing Q4)

**2 of 4 queries (1 URL):**
10. https://coverforgeusa.com/states/california/flood — Q2 8, Q4 8

**1 of 4 queries (4 URLs):** californiafloodinsurance.com/flood-insurance-rates/ (Q4 #3), insurance.com (Q1 #7), insuredbetter.com (Q3 #9), expressfinancial.net (Q4 #9)

### Patterns worth acting on
- **Every page ranking on all four queries carries either county/city data, zone data, or an interactive tool.** The four single-query pages (Insurance.com, InsuredBetter, Express Financial, and the client's rates page) are all table-free.
- **Zone-level dollar figures are surprisingly rare at the top.** Only LendingTree (zone monthly rates), Policygenius (A/V, B/C/X, D averages), Insuranceopedia (AE/VE, B/X, C/X ranges), and StateCalc (zone multipliers) publish them. Out of the Storm, ValuePenguin, Insurify and FloodPrice have no zone pricing at all.
- **County vs city split:** county tables (LendingTree, Insurify, Out of the Storm) trend to the top of the "rates/average" queries; city tables (ValuePenguin, Policygenius, Insuranceopedia, FloodPrice) dominate the mid-pack.
- **Data attribution is the credibility line.** FEMA/OpenFEMA is named by LendingTree, Insurify, Out of the Storm, StateCalc, FloodPrice and Cover Forge. The two client pages and Insurance.com cite nothing for their headline figure.
- **Only two pages show a real, visible update date** — Insuranceopedia ("Updated: 16 March 2026") and Cover Forge ("Updated April 2026"). Insurify shows the word "Updated" with no date. This is a cheap differentiator.

---

## Sources (all pages fetched during this analysis)
- LendingTree — https://www.lendingtree.com/home-insurance/california-flood-insurance/
- Insurify — https://insurify.com/homeowners-insurance/california-flood-insurance/
- Insuranceopedia — https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california
- California Flood Insurance (cost) — https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/
- California Flood Insurance (rates) — https://californiafloodinsurance.com/flood-insurance-rates/
- ValuePenguin — https://www.valuepenguin.com/flood-insurance/california
- Policygenius — https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/
- Insurance.com — https://www.insurance.com/home-and-renters-insurance/flood-insurance/flood-insurance-in-california
- Out of the Storm News — https://outofthestormnews.com/flood-insurance/costs/california
- StateCalc — https://statecalc.com/flood-insurance/california-flood-insurance-calculator/
- FloodPrice — https://www.floodprice.com/california-flood-insurance
- Cover Forge USA — https://coverforgeusa.com/states/california/flood
- InsuredBetter — https://www.insuredbetter.com/l/california/flood-insurance/
- Express Financial — https://expressfinancial.net/p/flood-insurance-california
