# Substantiation record — the loss-of-use pages, both brands

Companion to `SUBSTANTIATION-cost-page.md`, same standard and the same reason for
existing: Cal. Ins. Code § 790.03(b) turns on whether a public statement about
insurance is untrue, deceptive or misleading and whether reasonable care should
have caught it. Reasonable care for a published figure means being able to show,
on request, exactly where it came from.

Two live pages are covered:

| brand | URL | words |
|---|---|---|
| California Flood Insurance | `/loss-of-use-coverage-in-flood-insurance/` (post 93) | 1,992 |
| Statewide Flood Insurance | `/loss-of-use-coverage-in-flood-insurance/` (post 266) | 2,419 |

They are deliberately **not** the same page. California's table is California
counties; statewide's is fourteen metros across the twenty-eight states it has
pages for. Both are drawn from the same schedule.

---

## The displacement-cost table

**Source: HUD Fair Market Rent, fiscal year 2026, effective 1 October 2025.**
Reproduce with `tools/hud-fmr-pull.py`, which downloads the schedule and prints
the exact rows on both pages.

FMR is the 40th-percentile gross rent for a standard-quality unit in the area.
It was chosen over listing-site asking rents for three reasons: it is a published
population statistic with a stated effective date rather than a snapshot of
current listings, the methodology is documented and stable, and — the deciding
reason — **it is the same schedule FEMA uses to calculate disaster rental
assistance**, so the figure on the page is the figure the federal government
would itself use if it were paying for the housing.

### Self-check, and why it is worth the lines of code

The four California figures were sourced before the tool existed. The tool
re-derives them from the workbook and fails loudly if any drifts:

```
[ok ] CA San Joaquin    published 1742/2423  workbook 1742/2423
[ok ] CA Sacramento     published 2255/3002  workbook 2255/3002
[ok ] CA Monterey       published 2684/3623  workbook 2684/3623
[ok ] CA Santa Clara    published 3483/4602  workbook 3483/4602
```

HUD reissues the schedule mid-year. Without this check the pages would quietly
stop matching the source they cite, which is the exact failure § 790.03(b)'s
"reasonable care" language is about.

### What the table is NOT allowed to claim

FMR benchmarks an ordinary **unfurnished long-term** rental. A displaced family
needs furnished, short-term, available-this-week accommodation — a different and
more expensive market. No reliable published figure for the gap was found, so
both pages state the caveat in the body text and label FMR **a floor for
planning, not a quote**. Do not promote it to an estimate of displacement cost.

### Statewide's fourteen rows, 14 August 2026

Mobile AL $1,083/$1,414 · Gulfport–Biloxi MS $1,140/$1,471 · St. Louis MO
$1,218/$1,568 · New Orleans LA $1,331/$1,701 · Houston TX $1,573/$2,116 ·
Wilmington NC $1,659/$2,178 · Virginia Beach–Norfolk VA $1,713/$2,376 ·
Nashville TN $1,730/$2,211 · Charleston SC $1,787/$2,222 · Tampa FL
$1,977/$2,527 · Monmouth–Ocean NJ $2,328/$3,043 · Miami FL $2,436/$3,127 ·
Seattle WA $2,501/$3,272 · New York NY $2,910/$3,644.

Quoted in prose as the extremes of the same schedule: **Perry County, KY $959**
(2BR) and **Boston, MA $2,941** (2BR). Perry County is named because it flooded
catastrophically in July 2022, not picked for being cheap.

---

## Coverage and limit statements

| statement | basis |
|---|---|
| NFIP covers no loss of use / ALE / temporary housing | Statutory scope of the program; long-established and uncontested. FEMA's own consumer pages no longer carry a coverage-detail page — floodsmart.gov was rebuilt and `/flood-insurance/what-covered` now 404s, and fema.gov returns 403 to automated requests. Cited from the program's terms, not from a marketing page. |
| $250,000 building / $100,000 contents residential maximum | **42 U.S.C. § 4013(b)** sets the statutory limits. Cite the statute, not a web page — it does not move. |
| Contents settled at actual cash value | Program terms. Also the basis of published NFIP claim-appeal decisions on ACV, which floodsmart.gov does still host under `/recover/how-to-write-your-appeal/`. |
| $500,000 / $500,000 commercial maximum | Same statutory section. |
| 29% of NFIP flood claims come from moderate- to low-risk areas | floodsmart.gov, checked directly. Same figure as the cost page. |

**No policy form is quoted, excerpted, linked or attached on either page.** That
is a standing rule and both pages comply — everything published is a statement
about program scope, not policy wording.

---

## The loss-of-use take-up mechanism

**Published on statewide as:** some programs include loss of use automatically and
set the limit as a percentage of the building limit; others treat it as an option
that must be added and cap it at a flat amount; the two can differ by a factor of
ten.

**Basis: the agency's own placed business, and it is a measured finding rather
than an impression.** In one program every policy carrying the coverage sits at
exactly the same round dollar figure — the signature of a checkbox with a fixed
limit. In another, every policy carries it, spread across ten distinct values
including several irregular five-figure amounts — the signature of a percentage
calculated off the building limit. Two mechanisms, visibly different in the data.

**Carrier names are not published, and the counts are not published**, both by
standing rule. The page states the mechanism, which is the part that helps a
buyer, and states it as something to ask about rather than as a statistic.

This was originally written up as "programme-driven" in a way that implied it was
an underwriting decision. It is not — it is a product-configuration difference,
and the correction came from Aaron, who places the business.

---

## Displacement duration — and why no number of months is published

Both pages say explicitly that they are **not** giving a multiplier. That is a
deliberate editorial choice, not an omission, and the pages say so in bold.

| finding | source |
|---|---|
| Mean 86 days, median 7 days, among households who had returned | Federal post-flood research following one major U.S. flood |
| Emergency shelter operated for more than two months after the 2023 Pajaro levee failure | Monterey County, CA |
| 12% of displaced households still out after one year, a further 5% after two | Study of severe flooding in England |

The mean-versus-median gap is the whole reason no multiplier is published: 86
against 7 is not a distribution any single number describes. Publishing "expect
three months" would be inventing a figure, and publishing "expect a week" would
understate the tail that actually bankrupts people.

---

## FEMA Individual Assistance claims

| statement | basis |
|---|---|
| Rental assistance requires a major disaster declaration **and** IA authorisation **and** county designation | FEMA IHP programme rules |
| "IHP assistance is not a substitute for insurance" | FEMA's own guidance, quoted verbatim |
| Awards calculated from HUD FMR, normally a two-month initial award, continuing need must be re-documented | FEMA IHP programme rules |
| Individual Assistance was never requested for the February 2019 Russian River flood at Guerneville | OpenFEMA DisasterDeclarationsSummaries — no matching IA declaration |
| California, ten years to Aug 2026: 13 IA declarations, 8 wildfire, 1 COVID, only 4 flood-related | OpenFEMA, query C in `SUBSTANTIATION-cost-page.md` |

**Corrected before publication:** an earlier draft applied FEMA's $43,600 IHP
financial maximum to rental assistance. It does not — rental assistance has no
financial maximum. The cap was removed rather than reworded. The California page
carries the county-declaration count; the statewide page does not, because that
count is California-specific and a national page must not imply it holds
elsewhere.

---

## Standing rules for these pages

1. **No premium figures on either loss-of-use page.** Cost claims live on the
   cost pages, where the substantiation and the disclaimers are.
2. **No carrier names, no policy counts, no limits attributed to a named
   programme.**
3. **FMR stays labelled a floor.** If a defensible short-term furnished-rental
   figure is ever found, it gets its own row in this file first.
4. **No month multiplier for displacement**, unless a genuine published
   distribution appears — not a mean.
5. Statewide's page must stay national. California examples may be *named as*
   California (the Pajaro shelter is), never generalised.

## Review history

- **14 Aug 2026** — California page upgraded: FMR table, displacement research,
  FEMA IA conditionality, the take-up mechanism.
- **14 Aug 2026** — statewide page written and published at post 266, restoring a
  URL that `.htaccess` had been redirecting into a page that never used the
  phrase. See `STATEWIDE-LOSS-OF-USE.md`.
- **14 Aug 2026** — `tools/hud-fmr-pull.py` added, making the table reproducible
  rather than merely cited.
