# The California Flood Insurance Cost Report — plan

Aaron's proposal, 13 Aug 2026: two years of policies written across California — city, state, premium — turned
into a real analysis of what flood insurance actually costs. Then the same for the Statewide book.

**This is the highest-value content project on either site**, for reasons the Search Console pull made concrete:

- `/how-much-does-flood-insurance-cost/` already draws **19,311 impressions at position 17.4** — the largest
  impression pool on the site, stuck on page two. Cost intent is where the demand is.
- **LendingTree ranks on the head term with generic county averages.** First-party placement data from a real
  book is strictly better information, and it is the one asset an aggregator cannot copy or scrape.
- Answer engines disproportionately cite pages carrying **original statistics**. A named, dated, methodologically
  explicit report is the shape of thing that becomes the citation.

---

## TWO RULES THAT DECIDE WHETHER THIS IS PUBLISHABLE AT ALL

### Rule 1 — a minimum cell size, enforced in code, not by eye

Every published figure must be derived from **at least 10 policies**, and I would prefer 20 for anything shown at
city level. Below that threshold the cell is suppressed and shown as "insufficient data".

**Why this is not optional.** "Average premium in Alpine County: $1,240 (based on 2 policies)" discloses, to a
close approximation, what two identifiable people pay. Small-cell aggregates are re-identifiable, and the whole
point of publishing is that the numbers get read carefully. The threshold goes in the pipeline so no future
refresh can quietly cross it.

**Never published, in any form:** names, street addresses, policy numbers, dates of birth, or any free-text
field. City and county only, and only where the cell survives the threshold.

### Rule 2 — normalise for coverage, or the numbers get dismissed

**An average premium with no coverage limit attached is not a statistic, it is a number.** A $1,100 premium on
$250,000 of building coverage and a $1,100 premium on $1,000,000 are completely different facts, and any
knowledgeable reader — an underwriter, a journalist, a competitor — will say so immediately.

So the published unit is one of:

- **premium per $100,000 of building coverage**, or
- **medians within coverage bands** ($0–250k, $250–500k, $500k–1M, $1M+)

And **medians with interquartile ranges, not means.** Premiums are right-skewed; a handful of large commercial
placements will drag an average somewhere no residential reader recognises. A median plus a 25th–75th percentile
range is both more honest and more useful — "half of policies fell between $X and $Y" is a sentence people quote.

---

## The data extract I need — de-identified, not the raw policy file

`policies-master.csv` and anything like it stays out of this repo; `.gitignore` already enforces that. What I need
is an extract with these columns and nothing else:

| Column | Notes |
|---|---|
| `effective_month` | `YYYY-MM`. Month is enough; day adds re-identification risk for nothing |
| `state` | for the Statewide version |
| `county` | the primary geographic cut |
| `city` | published only where the cell clears the threshold |
| `zip` | **useful internally, not for publication.** Keep it for zone joins and QA |
| `flood_zone` | **the single most valuable field — see below** |
| `property_type` | residential / commercial / condo unit / RCBAP / renter contents |
| `market` | NFIP or private. **Nobody publishes this comparison and it is our best angle** |
| `building_coverage` | required for Rule 2 |
| `contents_coverage` | |
| `deductible` | |
| `annual_premium` | the dependent variable |
| `new_or_renewal` | renewals price differently; mixing them muddies the trend |

**Explicitly excluded:** insured name, street address, policy number, agent, commission, carrier name.

### `flood_zone` is the field that makes or breaks the report

Zone is the strongest predictor of flood premium and the thing every reader actually wants — "what does AE cost
versus X?" is the question behind most of the traffic. If NowCerts carries it, that is the extract. If not, it can
be derived from address by joining to FEMA's National Flood Hazard Layer, which is a one-off geocoding job on data
that never leaves your side. **Tell me which, because it changes the plan's ambition significantly.**

### Two fields worth checking before we commit

- **Commission must not appear.** Not because of privacy — because it is nobody's business and its presence in a
  file invites the wrong conversation.
- **Carrier name is a judgement call.** Premium by *carrier* would be the most linkable table on the site and also
  the most likely to breach an appointment agreement. Default is to publish **NFIP versus private** only, and to
  hold carrier-level detail internally.

---

## What gets computed

1. **Headline medians** — statewide, with IQR, per coverage band.
2. **By flood zone** — AE, A, X, VE, AH/AO. The centrepiece.
3. **By county**, and by city where cells allow. This is what wins the city pages.
4. **NFIP versus private**, same cuts. The genuinely novel table.
5. **By property type** — residential, commercial, condo, RCBAP.
6. **Trend by year** — 2024 / 2025 / 2026. This captures the **Risk Rating 2.0 phase-in**, which is the one thing
   in here that is arguably *news* rather than reference, and news is what earns links.
7. **Premium per $100k of coverage** as the normalised comparator throughout.
8. **Sample counts published beside every figure.** Stating n is what separates a report from a marketing claim,
   and it is also what makes the suppression rule visible rather than suspicious.

---

## The artifact

**A named, dated report, not a blog post.** "California Flood Insurance Cost Report 2026" with a methodology
section, an explicit sample size, a stated date range, and an annual refresh. Named reports get cited and linked;
"How much does flood insurance cost?" posts do not.

- **`Dataset` schema** on the report page. It is the correct type, it is uncommon in this vertical, and it tells
  answer engines the page contains original data.
- The existing `/how-much-does-flood-insurance-cost/` becomes the **plain-English explainer** that links up to the
  report — so the 19,311 impressions get a better destination without losing the page that earns them.
- **A short methodology page**, linked from every table. This is what a journalist checks before citing.
- **Charts as static images with data tables beneath.** The table is what gets scraped and quoted; the chart is
  what gets screenshotted. Both matter, and a JavaScript-only chart delivers neither.

### Disclaimers that have to be on it

- **This is what policies cost, not a quote.** Historical placements, not an offer of insurance or a rate filing.
- Coverage, deductible, zone and construction drive individual pricing.
- No implication that any figure is available to a given reader today.

---

## Risks that are Aaron's call, not mine

1. **Carrier appointment agreements.** Some restrict publishing rate or premium information. Worth a read of the
   agreements before the NFIP-versus-private table goes public — that is the table most likely to be objected to,
   and also the most valuable.
2. **CDI advertising rules.** Reporting historical premiums is not advertising a rate, but the line is close
   enough that it belongs in the same conversation as the outstanding Terms of Service item already with counsel.
3. **Competitive intelligence.** Publishing what you place at tells competitors what you place at. Probably worth
   it, and the aggregation blunts it, but it should be a decision rather than an oversight.

---

## Sequencing

**California first, and prove it before porting.** Statewide averages 36.3 in desktop position against
California's 17.9 and carries a fifth of the impressions — the same report there will not perform the same way
yet, and per-state cells outside California are likely to be too thin to clear the threshold. Build once,
validate, then extend with whatever states have the volume.

1. Aaron confirms whether `flood_zone` exists in the export, and decides the carrier-name question.
2. Aaron produces the de-identified extract with the columns above.
3. I write `tools/premium-aggregate.py` — validation, suppression threshold, medians and IQRs, emits CSV/JSON.
   Runs on his machine; the raw extract never enters this repo.
4. We review the aggregates together for anything that looks wrong or discloses too much.
5. I draft the report page, methodology page, and the rewritten explainer.
6. Ship, add `Dataset` schema, then pitch it — floodplain managers, realtor and escrow associations, local press.

**The pipeline is the deliverable, not the page.** Written properly it reruns next year in a minute, and an
annually updated dataset compounds in a way a one-off post never does.

---

# DATA SURVEY — 13 Aug 2026, after Aaron pointed at `RBIA Bordereaux`

**There is far more here than "two years."** Monthly bordereaux from **2017 through 2026** — nine years.
Structure is `<year> BDX Files / <NN Month> BDX <year> /` with per-state subfolders plus master and
carrier-specific workbooks.

**Aaron's clarification: these are all private policies** — surplus lines, not NFIP. That makes the report *more*
differentiated, because FEMA publishes NFIP rates while private flood pricing is opaque. It also means an
NFIP-versus-private table cannot come from this data alone; the NFIP half would have to come from FEMA's published
figures, normalised the same way.

## The surplus-lines master file is the wrong source. The carrier bordereaux are the right one.

`Aug 1st-31st 2025.xlsx` (246 transactions across 5 weekly sheets) is a **regulatory filing** — built for surplus
lines tax, not analysis. It carries premium, city, state, ZIP, carrier and an Intermap risk score, but:

- **no coverage limits, no deductible** — which breaks the normalisation rule outright;
- geography is the **insured's mailing address**, not the risk location, so a Los Angeles landlord insuring a
  Stockton duplex lands in Los Angeles and corrupts any county table;
- every row is `New or Renewal = New`, so renewals are not in it.

**The carrier bordereaux have everything.** `QBE BDX Aug 2025.xlsx` (headers on row 2, not row 1) carries:

```
Certificate Ref · New Renewal Endt · Location No · No of Buildings
Street Address · City · State · Zip code · COUNTY · Community Name
Construction Type · Year Built · Occupancy · No of Stories · Sq ft
Bdx Building TIV · Contents TIV · BUILDING LIMIT · CONTENTS LIMIT
Property deductible · Content Deductible · Intermap score
Gross Premium · Policy Fee · Risk Inception / Expiry · Policy Type
```

That is the risk location with a county, full property characteristics, and **both limits and deductibles** — every
field the plan asked for except a literal FEMA zone, and `Community Name` plus a street address makes zone
derivable.

## Proof of concept — QBE, August 2025 alone, 200 policies

| Measure | p25 | **median** | p75 |
|---|---|---|---|
| Gross premium | $566 | **$674** | $740 |
| Building limit | $180,000 | **$250,000** | $250,000 |
| **Premium per $100k of building cover** | $267.80 | **$286.00** | $312.45 |
| Year built | 1953 | 1965 | 1979 |
| Intermap score | 28 | 36 | 47 |

**`$286 per $100,000 of building coverage` is the number this whole report should be built on.** It is normalised,
it is defensible, it survives the "for how much coverage?" question, and nobody else can publish it.

### County tables are viable, and that was the open question

California, one month, one carrier — **six counties already clear n≥10**:

| County | n | Median premium | Per $100k |
|---|---|---|---|
| Santa Cruz | 17 | $438 | $308.00 |
| San Diego | 16 | $665 | $274.77 |
| Marin | 15 | $712 | $295.74 |
| Orange | 12 | $715 | $288.26 |
| Santa Clara | 12 | $728 | $291.40 |
| Lake | 10 | $596 | $298.70 |

Los Angeles at n=9 was suppressed, which is the rule working as designed. **Across three carriers and nine years,
essentially every California county will clear the threshold, and the large cities will too.** The suppression
rule stops being a constraint and becomes a footnote.

## The commercial finding, stated carefully

The homepage claims **"Save 30–50% on Flood Quotes."** A median of $674 for $250,000 of building coverage sits
against the roughly **$942/year** NFIP California average that LendingTree ranks with — about a 28% gap, and
wider at the lower quartile.

**That comparison is not yet rigorous**, because the published NFIP average carries no stated coverage limit. The
honest version normalises both sides to premium per $100k using FEMA's own published data. Done properly, **this
turns an unsubstantiated marketing claim into an evidenced one** — which is worth more than the ranking.

## What I need from Aaron

1. **Confirm the carrier bordereaux are the source of truth**, not the SL master. Three carriers appear —
   **Hiscox (110), QBE (97), Brit (39)** in Aug 2025 — and each likely has its own column layout, so all three
   need profiling before the pipeline is written.
2. **What do `Occupancy = Tenant` and `Owner` mean?** 137 tenant against 61 owner is a striking split and it
   changes how the report is framed.
3. **`Property deductible` was populated on only 4 of 200 rows** in the QBE file. Is deductible captured
   elsewhere, or genuinely sparse?
4. **Confirm `Street Address` is the risk location** in the carrier files. The presence of `Location No`,
   `No of Buildings` and `County` says yes, but it is worth stating.

## Handling — what was done with the files just read

Four workbooks were downloaded to the container's scratchpad via temporary Dropbox links, profiled, and
**shredded**. They contain `Insured (Full Name)` and `Street Address`, so nothing was printed but column names and
aggregates, and nothing entered this repo. Only the derived figures above did.

**The pipeline will read the source on Aaron's machine and emit aggregates**, which keeps insured names and
addresses off this repo permanently. The engineering cost is real — nine years of inconsistent folder naming and
three carrier layouts to normalise — and it is worth paying once for a dataset that reruns annually in a minute.

---

# THE NFIP COMPARATOR — and Aaron's correction that changes the report's thesis

## Do not crawl the Selective portal. FEMA publishes the whole thing, free.

Aaron suggested having a browser agent crawl Selective (his NFIP writer) for comparable rate data. **There is a
far better source and it needs no portal.**

`NfipPolicies` v3 on OpenFEMA — **74,349,525 policy records**, public API, no key, verified 13 Aug. 87 fields per
record, including every dimension the bordereaux carry:

| What we need | NFIP field |
|---|---|
| **Flood zone** — the field I called make-or-break | `ratedFloodZone`, `floodZoneCurrent` |
| Building / contents coverage | `totalBuildingInsuranceCoverage`, `totalContentsInsuranceCoverage` |
| Premium | `policyCost`, `totalInsurancePremiumOfThePolicy`, `fullRiskPremium` |
| Deductibles | `buildingDeductibleCode`, `contentsDeductibleCode` |
| **Owner vs rental** — matches Aaron's Tenant/Owner split | `tenantIndicator`, `rentalPropertyIndicator`, `primaryResidenceIndicator`, `occupancyType` |
| Geography | `reportedCity`, `reportedZipCode`, `censusGeoid`, `latitude`, `longitude` |
| Property characteristics | `construction`, `originalConstructionDate`, `foundationType`, `numberOfFloorsInInsuredBuilding` |
| Elevation | `baseFloodElevation`, `lowestFloorElevation`, `elevationDifference` |
| Community | `nfipCommunityName`, `crsClassCode` |
| Pre/post-FIRM | `preFIRMConstructionIndicator`, `postFIRMConstructionIndicator` |

**Three reasons this beats crawling**, beyond it being free:

1. **It is policy-level**, so it normalises identically to the bordereaux — premium per $100k, same coverage
   bands, same zones, same counties. Averages could never support that.
2. **It covers every NFIP policy in California**, not just the ones Aaron wrote. The comparison becomes
   authoritative rather than anecdotal.
3. **Carrier portals prohibit automated access** in their terms, and lock accounts when they detect it. Risking
   an appointment the agency depends on, to obtain worse data than a public API already gives, is a bad trade.
   If NFIP figures from his own book are wanted later, the portal's own **book-of-business export** is the
   sanctioned route.

## ⚠ AARON'S CORRECTION — WHY A MEDIAN-VS-MEDIAN COMPARISON WOULD BE DISHONEST

His words, and they are the most consequential input to this project so far:

> *"The NFIP must quote every person where private does not. They get to underwrite each risk individually, and
> many times they may decline the risk. The NFIP does not decline the risk. They have to take everyone, and so
> their rates must reflect that."*

> *"They include such factors as equity and inclusiveness for areas that have lower-income people, which is not
> an underwriting technique for most standard carriers. There are times that the NFIP rates are ridiculously
> low, and that's why we always quote them both."*

**This is selection bias, and it would have invalidated the headline.** Private carriers decline risks they do
not want, so the private book is a *selected* population — better risks by construction. Publishing "private is
28% cheaper than NFIP" would have been comparing a filtered pool against an unfiltered one and calling the
difference a price. A competent analyst or journalist would take that apart, and they would be right to.

### So the thesis changes, and the honest version is commercially stronger

**Not:** "Private flood insurance is X% cheaper than the NFIP."

**Instead:** *"We quote both on every policy. Here is how often each one wins, and for which properties."*

That reframing is better on every axis:

- **It is true**, and it survives scrutiny including the equity-factor anomalies Aaron describes.
- **It is unique.** Nobody else holds both halves of this comparison, and nobody publishes "how often does NFIP
  win" because nobody knows.
- **It argues for the business model.** "Neither wins every time, so you need someone who quotes both" is exactly
  the case for using a broker over going direct — which is the real commercial objective, and it beats a discount
  claim that invites disbelief.
- **It explains Risk Rating 2.0 to an audience nobody serves.** That NFIP pricing now embeds affordability
  factors most carriers do not use, and therefore undercuts private insurance in some lower-income areas, is a
  genuinely interesting, publishable, uncovered fact.

### What this means methodologically

1. **Stratify every comparison.** Same flood zone, same coverage band, same occupancy type, same construction
   era, same county. Comparing unstratified medians is the error to avoid.
2. **Report the win rate, not just the gap** — "NFIP was the cheaper option in N% of comparable cases" is the
   statistic that gets quoted.
3. **Show the distribution.** Aaron's "sometimes ridiculously low" is a real tail, and a median hides it. Publish
   the spread and say plainly that the tails are where the surprises live.
4. **Disclose the selection effect in the methodology, prominently.** State that private carriers underwrite and
   decline while the NFIP cannot, that this makes the two books different populations, and that stratification
   reduces but does not eliminate the difference. **Saying this is what makes the rest credible** — and no
   competitor's marketing page will ever say it.

---

# FIRST REAL RESULT — 13 Aug 2026. Both halves computed, same unit.

## The comparator works

| Source | Median per $100k of building coverage | n |
|---|---|---|
| **NFIP** — OpenFEMA, California, Jan–Feb 2025 effective | **$414.00** | 7,413 |
| **Private** — QBE bordereau, August 2025 | **$286.00** | 200 |

**Private is 31% lower at the median.** The homepage claims "Save 30–50%." That claim, presumably made on
instinct, lands at the bottom edge of the measured range.

Sanity check on the NFIP side: median NFIP premium **$994** against the roughly **$942** California average
LendingTree ranks with. Close enough to confirm the public data and the aggregator agree.

## NFIP cost per $100k by rated flood zone, California

| Zone | n | Median per $100k |
|---|---|---|
| X | 2,974 | $414.40 |
| A99 | 1,721 | $316.80 |
| AE | 1,196 | $576.80 |
| AO | 567 | $461.34 |
| A | 526 | $574.60 |
| AH | 232 | $582.80 |
| VE | 72 | $679.20 |
| C | 58 | $288.48 |
| D | 32 | $549.69 |

**This table alone is publishable and I have not found anyone publishing it.** Note zone **X at $414 costs more
per $100k than A99 at $317** — counterintuitive, and counterintuitive facts backed by 74 million records are what
get cited.

## Four caveats, and the third is the critical path

1. **The private figure is one carrier, one month, n=200.** Directional only. The full pipeline across three
   carriers and nine years replaces it.
2. **The NFIP figure covers Jan–Feb 2025 effective dates**, because the API pull stopped early. Trivially
   extended.
3. **⚠ THE 31% IS NOT YET STRATIFIED, so it is not yet a price difference.** Per Aaron's selection-bias point,
   and compounded by mix: if the private book skews toward zone X at $414 while NFIP carries proportionally more
   AE at $577, part of that gap is *which properties*, not *what price*. **Stratifying by zone requires a flood
   zone on the private book, and the carrier bordereaux do not carry one** — only `Intermap score`. So the
   critical path is deriving zone for the private policies by geocoding their addresses against FEMA's National
   Flood Hazard Layer. Until that exists, the honest published number is per-zone NFIP data plus an
   *unstratified, disclosed* private comparison.
4. **The owner-versus-rental mapping is wrong and needs redoing.** NFIP `tenantIndicator` returns n=15 against
   7,398 owner-occupied, which is implausible for rentals — it evidently flags a tenant who bought contents-only
   cover, not a landlord-owned property. Aaron's Tenant/Owner split means landlord versus owner-occupied, so the
   NFIP equivalent is likely `rentalPropertyIndicator` or an `occupancyType` code. Do not publish this cut until
   the mapping is verified against FEMA's data dictionary.

## The "win rate" thesis needs a different dataset

The strongest framing — *"we quote both on every policy; here is how often each wins"* — **cannot be computed from
these two sources.** Bordereaux record what was **bound**; FEMA records what was **written**. Neither contains a
quote pair on the same property.

That needs Aaron's **quote** records — both prices for the same risk on the same day, which is what Instanda or
NowCerts may hold. **Worth asking for, because it is the difference between a good report and a unique one.**
Absent it, a zone-and-coverage-matched comparison is the closest honest proxy.
