# Substantiation record — published cost figures

**Why this file exists.** Cal. Ins. Code § 790.03(b) turns on whether a public
statement about insurance is untrue, deceptive or misleading, and whether it
"by the exercise of reasonable care should be known" to be so. Reasonable care for
a published premium figure means being able to show, on request, exactly where the
number came from. "We have a book of business" is not an answer to a regulator.

Every figure on `/how-much-does-flood-insurance-cost/` is reproducible from what
follows. Update this file whenever the page's numbers change; never change a
published figure without adding a row here.

---

## Published figures, 14 August 2026

| figure on the page | value | source |
|---|---|---|
| NFIP median, matched terms | $1,244 | FEMA OpenFEMA, query A below |
| NFIP interquartile range | $845 – $2,007 | same |
| NFIP p10 / p90 | $623 / $2,836 | same |
| NFIP policies measured | 10,545 | same |
| Private median, matched terms | $822 | agency book, query B below |
| Private interquartile range | $769 – $888 | same |
| Private policies measured | 3,645 | same |
| A zones median | $1,246 (n=9,810) | query A, grouped by rated zone |
| X/B/C median | $1,082 (n=572) | same |
| V zones median | $2,849 (n=118) | same |
| Primary vs non-primary | $1,205 / $1,438 | query A, split on primaryResidenceIndicator |
| HFIAA surcharge $25 / $250 | — | confirmed empirically in the same data |
| HUD FMR 2BR San Joaquin / Santa Clara | $1,742 / $3,483 | HUD FY2026 FMR schedule, effective 1 Oct 2025 |
| CA disaster declarations with IA, 10 yrs | 13, of which 4 flood-related | OpenFEMA, query C below |
| Claims from moderate-to-low-risk areas | 29% | floodsmart.gov, checked directly |

## Query A — the NFIP figures

Dataset: OpenFEMA **FimaNfipPolicies v2**.
Reference date (`REF`): **2026-08-14**. Pulled 14 August 2026.

```
propertyState eq 'CA'
and totalBuildingInsuranceCoverage eq 250000
and buildingDeductibleCode eq '5'
and occupancyType eq 11
and policyEffectiveDate le 'REF'
and policyTerminationDate gt 'REF'
and cancellationDateOfFloodPolicy eq null
```

Partitioned by `countyCode` across all 58 California FIPS codes; every county
returned a clean termination status, none truncated. Tooling:
`tools/fema-nfip-county-pull.py`, aggregated by `tools/fema-nfip-county-aggregate.py`.
Output retained at `premium-aggregates/nfip-benchmark/ca-benchmark.json`.

**Why the date filter matters.** FEMA's policy file is transactional: an annual
policy renewing five times is five rows. An earlier pull without this filter
returned 2,073 rows for Alameda against 388 actually in force — a 5.3x
overstatement, blended across the Risk Rating 2.0 phase-in. Any figure produced
without the in-force filter is wrong and must not be published.

**Cost definition.** `policyCost` = premium + reserve fund assessment + federal
policy fee + HFIAA surcharge. This is the all-in figure, chosen so it compares
like-for-like against our own premium-plus-fees total. Comparing it to a bare
private premium would overstate the NFIP.

## Query B — the private figures

Source: agency bordereaux, aggregated by `tools/premium-aggregate.py`.
Cut: `benchmark_250k_5000ded` — building limit exactly $250,000, deductible
$5,000. Output at `premium-aggregates/california/aggregates.json`.

Total includes gross premium + policy fee + surplus lines tax + stamping fee
(+ fire marshal tax where applicable). California surplus lines tax 3.0% and
stamping fee 0.18%, applied to premium + policy fee — verified against 250 rows
carrying a recorded `TaxableAmount`, where the ratios matched the statutory rates
exactly.

**Exclusions, and why:**

- **Endorsements, cancellations and return transactions dropped before dedupe.**
  They share a Certificate Ref with the original, so deduplicating first would
  keep the endorsement and discard the real premium.
- **Duplicate certificate references** removed.
- **Zero and negative premiums** excluded.
- **Medians, not means** — commercial schedules share these files with homeowner
  policies and range past $200,000 against a median near $600.

**The selection criterion, stated plainly because it is the most important line
in this file:** these are policies the agency *placed*, and we place a private
policy when it beats the federal quote. Every case where the NFIP won is absent by
construction. This is disclosed on the page itself, in the table's own row label
rather than a footnote.

## Query C — FEMA disaster declarations

Dataset: OpenFEMA **DisasterDeclarationsSummaries v2**, pulled 14 August 2026.

```
state eq 'CA' and declarationType eq 'DR'
and ihProgramDeclared eq true
and declarationDate ge '2016-08-13T00:00:00.000z'
```

138 rows, 13 unique declarations. Flood-titled: DR-4353, DR-4683, DR-4699,
DR-4758. Eight of the thirteen are wildfires; one is COVID-19.

## Standing rules

1. **No published figure below n=11.** Aligns with the common federal
   confidentiality convention (CMS suppresses cells of 1–10). It is a
   confidentiality floor, **not** a reliability standard — no recognised standard
   for publishing a median exists; NCHS states its standards "were not developed to
   apply to other estimators, such as percentiles or means."
2. **n≥30 before any figure is presented as a headline** or used to compare one
   area against another.
3. **Never publish a median alone.** Sample size and spread accompany every figure.
4. **No estimating, interpolation or gap-filling.** A missing cell stays missing.
5. **No county-level private figures.** The benchmark cut represents 23.7% of
   Santa Clara's NFIP book but 1.8% of Sacramento's, so a county comparison at
   these terms would compare different slices of different markets.
6. **Our figures are labelled as our book**, never as a market rate.

## Review history

- **14 Aug 2026** — page rebuilt on measured data, replacing unsourced ranges.
- **14 Aug 2026** — compliance review returned. Four changes applied: the
  selection effect moved into the table's row label; the "flood zone does not set
  your price" heading softened where it appeared to contradict its own table; the
  not-a-quote disclaimer expanded to the three-part form the California Department
  of Insurance uses on its own premium surveys; and the NFIP characterisation
  reworded from "carries risks private insurers declined" to "accepts all
  applicants... reflects that broader risk pool," which states the same fact
  without implying federal rates are inflated.

## Open, and genuinely for a lawyer rather than a research pass

- Whether the side-by-side table remains acceptable now the selection effect sits
  in the row label. Two reviewers flagged the structure; one held that no caveat
  can undo what a two-row table implies. The label change is the honest middle, but
  it is a judgement call a California insurance attorney should confirm.
- **§ 1726 completeness.** The homepage carries the licence number, the agency name
  and the word "insurance". Whether "state of domicile and principal place of
  business" is satisfied has not been confirmed, and there is a standing
  instruction not to publish the Escondido mailing address. Resolve deliberately.
- Record-retention period for this substantiation file.

---

## The Zone X figure — sourced to the agency, not to the aggregate

**Published:** "In Zone X we typically place private policies at around $450 a
year, all in."

**Source: Aaron Farmer, CA Lic. #0L75450, as the Lloyd's coverholder placing the
business.** This is a statement about what this agency writes, made by the person
who writes it. It is not derived from the aggregate and must not be presented as
a measured median.

**Why it is not backed by an aggregate median.** Only 21 rows in the book carry a
flood zone at all (X n=11 at $564, AE n=10 at $491) — at or below the publishing
floor. The Intermap risk score was tested as a proxy and does not work: low-risk
scores still median $668–$780, though their p25 runs $417–$556.

**What the aggregate does independently corroborate:**

- p10 all-in of the whole book is **$441**
- **10.5%** of placements land in that band
- the jump from p10 to p25 is **$294** — a minimum-premium cliff, not a tail
- the mechanism reconciles arithmetically: $350 premium + $95 policy fee +
  California's 3.18% surplus lines tax and stamping fee = **$459**

**Why the statewide median is higher and does not contradict it.** The $794 book
median and the $822 benchmark median blend A/V zone homes, where cover is
mandatory, with X zone homes where it is optional. Segmenting is the whole point —
publishing a blended median as though it described an X-zone buyer is the error
this project has been correcting all along, and it applies to our own figures too.

**What would make it measurable at scale:** zone-tagging the book by geocoding
risk addresses against the FEMA NFHL. Until then this figure stands on the
agency's own placement record, which is a legitimate source for a statement about
the agency's own business — but it is a different kind of claim from the measured
medians elsewhere on the page, and the file records it as such.

