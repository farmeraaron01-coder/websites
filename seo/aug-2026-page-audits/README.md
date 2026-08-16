# SEO audit — Risk Rating 2.0, Hiscox FloodPlus, Flood Zone X

> **Second pass completed 16 Aug 2026 — see [`FIXES.md`](FIXES.md) for the
> paste-ready find-and-replace blocks.** This README holds the analysis; FIXES.md
> holds the edits. The NFIP comparison in the section below was recomputed after
> Aaron clarified that `HiscoxNFIPPurePremium` is a fixed $250k/$100k reference
> quote, not a customer's NFIP price — the matched-terms figures in FIXES.md
> ($773 vs $1,244, n=1,121) come from the OpenFEMA cut instead and are the ones
> to publish.


Audited 16 Aug 2026, after the cost-by-zone engagement. All three pages checked
against the live HTML and against the quote-book analysis in
`../california-flood-insurance-cost-by-zone/data-analysis.md`.

| Page | Post | Words | Score |
|---|---|---|---|
| [Risk Rating 2.0](https://californiafloodinsurance.com/how-risk-rating-2-0-affects-federal-flood-insurance-policy-holders/) | 456 | 2,282 | **84/100** |
| [Hiscox FloodPlus](https://californiafloodinsurance.com/hiscox-flood-plus-comprehensive-flood-insurance-coverage/) | 454 | 1,920 | **80/100** |
| [Flood Zone X](https://californiafloodinsurance.com/navigating-flood-zone-x/) | — | 1,546 | **76/100** |

**These are much better pages than the cost-by-zone one was (68).** None of the
cost-by-zone defects repeat: single H1 each, no leftover build comments, correct
self-referencing canonicals, `index,follow`, valid BlogPosting + FAQPage schema,
10–11 in-content internal links each, and no broken "enter your address"
instructions. The Risk Rating 2.0 page in particular is genuinely strong work —
a real OpenFEMA analysis with stated methodology and honest caveats.

So these need **surgical edits, not rebuilds.** Do not paste over the bodies.

---

## 🔴 The one real correctness problem

### Zone X page understates its own price by ~13%

The page says: *"we typically place private policies here at around **$450 a
year**, all in."*

Your actual Zone X book: **median $509** (new business, deduped, n=101) — and
$450 is close to the 25th percentile, not the middle. Roughly three in four
Zone X buyers pay more than the page promises.

Understating price is worse than overstating it: the prospect anchors on $450,
gets quoted $509+, and the gap reads as bait. It also contradicts the
cost-by-zone page, which will publish $509 the moment the other patch lands.

**Find:**
```
at around <strong>$450 a year</strong>, all in.
```
**Replace:**
```
at a median of <strong>$509 a year</strong>, all in.
```

---

## 🟠 High — applies to all three pages

### 1. The 29% claim is uncited on every page

All three carry *"29% of NFIP flood claims come from moderate- to low-risk
areas"* with no source, and with wording that doesn't match FEMA's. Verified
16 Aug 2026 against FloodSmart.gov (see the cost-by-zone README for the full
verification). FEMA's own framing is "outside current high-risk flood areas"
and the figure covers 2014–2024.

**Find (Zone X page — note trailing period):**
```
<strong>29% of NFIP flood claims come from moderate- to low-risk areas.</strong>
```
**Replace:**
```
<strong>From 2014 to 2024, 29% of NFIP flood insurance claims came from outside high-risk flood areas</strong> (<a href="https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk" target="_blank" rel="noopener">FEMA, FloodSmart.gov</a>).
```

**Find (Risk Rating 2.0 page — no trailing period):**
```
29% of NFIP flood claims come from moderate- to low-risk areas
```
**Replace:**
```
from 2014 to 2024, 29% of NFIP flood insurance claims came from outside high-risk flood areas (<a href="https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk" target="_blank" rel="noopener">FEMA, FloodSmart.gov</a>)
```

If either page's FAQPage schema repeats the sentence, sync it — but neither
appeared to on inspection.

### 2. None of the three link to the new cost-by-zone page

All three link to `/how-much-does-flood-insurance-cost/`; **zero** link to
`/california-flood-insurance-cost-by-zone/`. That page carries your proprietary
rate table and is the natural destination from all three. Add one contextual
link each — do this *after* the cost-by-zone patch is live.

- **Zone X**, after the corrected $509 sentence: link "see our
  [full cost breakdown by flood zone](/california-flood-insurance-cost-by-zone/)"
- **Risk Rating 2.0**, near its zone-comparison table: link to the private-market
  equivalent
- **Hiscox**, where it discusses pricing: same

### 3. Zero external links on any of the three

Not one outbound link across 5,748 words on YMYL financial topics. The Risk
Rating 2.0 page analyses OpenFEMA data without linking OpenFEMA; the Hiscox page
discusses the statutory $250,000 cap without linking FEMA; all three cite the
29% without a source. For E-E-A-T and for AI citation, outbound links to primary
sources are a positive signal, and their total absence is unusual.

Minimum additions: FloodSmart (above, covers all three), OpenFEMA on the Risk
Rating 2.0 page, and FEMA's NFIP coverage-limits page on Hiscox.

**Cite all of them — that is the recommendation.** One logistical note: the
FloodSmart link is confirmed live (HTTP 200, claim read verbatim), so it can go
in as-is. Every `www.fema.gov` URL returns 403 to this environment via both curl
and WebFetch, because fema.gov blocks datacenter traffic — that says nothing
about whether the pages are good, only that they can't be checked from here.
A real browser is not blocked, so verification is folded into the Chrome apply
task. This covers the OpenFEMA URL in `rr2-dataset-schema.jsonld` too: confirm
it loads, then publish. If a URL has moved, search fema.gov for the dataset name
rather than dropping the citation.

---

## 🟢 The big opportunity — you can now prove the NFIP comparison

The Risk Rating 2.0 page publishes NFIP medians from OpenFEMA at a specific
cut: **California, $250,000 building, $5,000 deductible, single-family**. Your
quote book turns out to sit almost exactly on those terms — 70% of bound
policies are at $250k building and 91% at a $5,000 deductible.

Filtering the book to the *same* terms (n=1,121 CA bound policies):

| | NFIP (OpenFEMA, in-force) | Your private book (bound 2025–26) |
|---|---|---|
| Median all-in | **$1,244** | **$773** |
| Middle half | $845 – $2,007 | $671 – $868 |
| A zones | $1,246 | $774 |
| X / B / C zones | $1,082 | $670 |

**Private runs about $471/year cheaper at the median, at matched terms.**

That independently corroborates the "$300–600/year" claim on the cost-by-zone
page — $471 lands mid-range — from two datasets that have nothing to do with
each other. It is the strongest, most defensible number produced in this entire
engagement, and it belongs on the Risk Rating 2.0 page (which sets up the
comparison and then never closes it) and on the Hiscox page.

**Honest caveats to state alongside it**, or the comparison isn't safe to
publish:

- OpenFEMA measures **in-force** policies; yours are **newly bound**. New
  business skews cheaper than a seasoned book.
- "All-in" differs by side: NFIP is premium + reserve fund assessment + federal
  policy fee + HFIAA surcharge; private is premium + policy fee + California
  surplus lines taxes.
- The OpenFEMA cut is single-family residential; the private book was not
  filtered to single-family (roughly a third is landlord business).
- Same coverage limit does not mean same coverage — private policies here often
  include loss of use, which the NFIP excludes entirely.

Suggested framing, which survives all four caveats:

> At matched terms — $250,000 of building coverage, a $5,000 deductible, in
> California — the NFIP's median all-in cost is $1,244 a year. Across the 1,121
> policies we bound on those same terms in 2025–2026, our median was $773. That
> is roughly $471 a year, for coverage that also includes loss of use the NFIP
> does not offer.

---

## 🟡 Medium

**Dataset schema belongs on the Risk Rating 2.0 page.** It publishes a genuine
dataset — 10,545 in-force policies, medians by zone family and county, with
stated methodology — and carries no `Dataset` markup. It is a better candidate
than the cost-by-zone page was. Draft in `rr2-dataset-schema.jsonld`.

**FAQPage schema on all three** — Google retired FAQ rich results for everyone
on 2026-05-07, so these earn no SERP feature. Informational only; **do not
remove them.** The answers stay quotable for AI engines and cost nothing.

**Hiscox page has the thinnest data.** Two dollar figures in 1,920 words, both
the same $250,000 statutory cap. It argues Hiscox beats the NFIP without a
single price. The matched-terms comparison above fixes this, and the
market-spread stat helps too: across your California book, **no single market
was cheapest more than 26% of the time** — which is the honest argument for
shopping rather than for any one carrier, Hiscox included.

**Zone X page is the thinnest overall** at 1,546 words and has the weakest
title-tag differentiation against `/which-flood-zone-requires-flood-insurance/`.
Worth watching in GSC for cannibalization between those two.

---

## Priority order

1. Fix the `$450` → `$509` correctness problem on Zone X *(5 min)*
2. Cite the 29% on all three *(10 min)*
3. Add the matched-terms NFIP comparison to Risk Rating 2.0 and Hiscox *(30 min)*
4. Link all three to the cost-by-zone page — **after** that patch is live *(10 min)*
5. Add `Dataset` schema to Risk Rating 2.0 *(10 min)*
6. Add outbound source links *(15 min)*

Items 1 and 2 are pure find-and-replace and can go in today. Item 3 is the one
with real upside.

## Falsifiability

If the matched-terms comparison is right, GSC should show the Risk Rating 2.0
page gaining impressions on "private flood insurance vs NFIP" style queries
within 6–8 weeks. If it doesn't move, the constraint is the page's authority,
not its content, and the next lever is links rather than more copy.
