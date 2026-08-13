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
