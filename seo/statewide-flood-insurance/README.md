# Statewide Flood Insurance — data-backed content plan

Analysed 16 Aug 2026 from the same inception-to-date quote export used for the
California work (`../california-flood-insurance-cost-by-zone/data-analysis.md`).
Same method: bound policies only, deduplicated to one per property by hashed
street+ZIP, all-in cost = premium + policy fee + surplus lines taxes and fees.

**No prior Statewide deliverable exists in this repo.** If an earlier audit was
done, it was in another session and isn't recorded here — this is the first.

---

> ## ⚠️ REVISED 16 Aug 2026 — read this before the sections below
>
> The analysis below counts **bound policies only**, and on that basis concluded
> the book is too thin outside California to support much. Aaron pointed out the
> obvious gap: quotes carry zones and premiums too, and Texas and Florida hold
> the most flood policies in the country regardless of how many we bind there.
>
> He was right, and it changes the conclusion substantially.
>
> | Threshold | Viable states on **bound** | Viable states on **quoted** |
> |---|---|---|
> | n ≥ 30 | 16 | **28** |
> | n ≥ 50 | 7 | **27** |
> | n ≥ 100 | 3 | **18** |
>
> **The selection effect is small enough to publish through.** Comparing quoted
> against bound medians in every state where both are measurable, the median gap
> is **+$20** — quoted runs marginally higher, as expected when people bind at
> prices they accept. Where the bound sample is large enough to trust, the gap
> nearly vanishes: CA −$3, AZ $0, OH $0, PA $0, TX −$9, MI +$3. The wild deltas
> (NJ +$240, MS +$187, NM −$212) all sit on bound samples under 25, so they are
> small-n noise on the *bound* side, not evidence against the quotes.
>
> **Texas and Florida now carry real zone tables:**
>
> | | Zone X | Zone AE | Zone A | Zone AH |
> |---|---|---|---|---|
> | **Texas** (367 properties) | $614 (212) | $892 (108) | $582 (32) | — |
> | **Florida** (342 properties) | $617 (198) | $895 (103) | $562 (24) | $824 (13) |
>
> Both are X-dominant, which fits their geography, and both price AE around $890
> — well above California's $765. That is a publishable contrast.
>
> Also newly viable: SC (197), NC (168), NY (167), GA (152), NJ (134).
> **27 states now carry a zone table**, against 7 on bound data.
>
> **Publishing rules this creates:**
> - Label them **"median quoted premium"**, never "what our customers pay".
>   The California pages say "bound" and must keep saying it.
> - State the sample as *properties quoted*, deduplicated one per property.
> - Where both exist and bound n ≥ 30, prefer bound — it is the stronger claim.
>   Use quoted to reach the states bound cannot.
> - Say plainly that quoted medians run slightly above bound. It costs nothing
>   and pre-empts the obvious objection.
>
> New files: `data/state-medians-quoted.csv` (27 states),
> `data/state-zone-medians-quoted.csv` (81 state-zone rows).
>
> The bound-only analysis below stays as written — it remains the right basis
> for anything phrased as "what our customers actually pay", and for California.

## The bound-only picture (still true, but not the whole story)

The book is **thinner outside California than it looks**, and the plan has to be
built around that rather than around the raw quote count.

| | |
|---|---|
| Bound policies nationwide, deduplicated | **2,820** |
| Of which California | **1,665 (59%)** |
| States with **≥30** bound policies | **16** (15 excluding CA) |
| States with ≥50 | 7 |
| Non-CA **cities** with ≥10 bound policies | **5** |

So: **a page per state is not supportable, and city pages outside California are
not supportable at all.** The five non-CA cities that do clear n≥10 are Hoquiam
(26), Aberdeen (22), Tucson (17), Grants Pass (16) and Wenatchee (14) — small
towns, not metros. Publishing a median off 4 policies for Houston or Miami would
be the kind of thin, scaled location content the 2026 spam systems target.

What *is* supportable is strong: 16 states with real medians, and 7 of them deep
enough to carry their own flood-zone table.

---

## What the site already has

`statewidefloodinsurance.com` runs ~26 state pages plus a
**`/flood-insurance-cost-by-state/` hub** — which is the natural home for the
master table and the direct analogue of the California cost-by-zone page.

Mapping the pages against the data gives three groups.

### Group 1 — pages with real data (do these first)

| State | Policies | Median | Typical range | Bind rate |
|---|---|---|---|---|
| Washington | 210 | $665 | $474–$793 | 48% |
| Oregon | 104 | $749 | $567–$880 | 47% |
| Texas | 73 | $679 | $511–$865 | 20% |
| Connecticut | 57 | $817 | $606–$1,011 | 42% |
| Massachusetts | 53 | $649 | $478–$850 | 34% |
| Ohio | 47 | $620 | $506–$745 | 31% |
| New York | 46 | $685 | $467–$1,024 | 26% |
| Pennsylvania | 45 | $534 | $353–$785 | 32% |
| North Carolina | 39 | $614 | $476–$927 | 22% |
| Michigan | 39 | $366 | $359–$464 | 31% |
| Florida | 38 | $669 | $478–$877 | **11%** |
| Illinois | 37 | $456 | $362–$720 | 32% |
| Georgia | 34 | $468 | $364–$699 | 22% |

Full table with quartiles in `data/state-medians-bound.csv`.

**Seven states can carry their own zone table** (n≥50 with zones at n≥10): CA,
WA, OR, AZ, TX, CT, MA — see `data/state-zone-medians.csv`. Washington is the
strongest: AE $687 (127), A $598 (31), AO $616 (18), numbered-A $644 (17),
X $673 (12). That's a California-grade page.

### Group 2 — two states with data and **no page at all**

- **Arizona — 97 bound policies, $547 median, 48% bind rate.** Your third-largest
  book outside California, and there is no `/arizona-flood-insurance/` page. It
  also has enough depth for a zone table.
- **Oklahoma — 33 bound, $448 median, 35% bind rate.**

These are the clearest wins on the list: real proprietary data, no page competing
for it, and no thin-content risk because the data is genuinely there.

### Group 3 — eleven pages the data cannot support

`CO · HI · IN · KY · LA · MD · MO · MS · NV · TN · VA` — all under 20 bound
policies, several near zero.

**Do not add invented or borrowed figures to these.** They are presumably
qualitative pages about state flood risk and requirements, which is legitimate;
what they cannot do is carry a "here's what it costs in your state" table. The
honest options are to leave them qualitative, or to have them link the national
hub for pricing rather than imply state-specific numbers.

Adding AZ and OK brings the location-page count to ~28, still under the 30-page
threshold where scaled-content quality gates start to bite. Do not push toward
50 state pages on this dataset.

---

## The business finding that isn't SEO

Bind rate varies more than price does, and it points at something worth knowing:

| Converting well | Converting badly |
|---|---|
| WA 48% · AZ 48% · OR 47% · CT 42% | **FL 11%** · SC 11% · NJ 17% · TX 20% |

**Florida: 352 properties quoted, 38 bound.** That is the largest flood insurance
market in the United States and roughly one in nine quotes converts — against
one in two in Washington. Texas is the same shape at 20% on 369 properties
quoted. Whether that's pricing, competition, or follow-up, it is a bigger lever
than any page edit on this list, and it isn't an SEO problem.

---

## Recommended order

1. **`/flood-insurance-cost-by-state/`** — publish the 16-state table with
   medians, quartiles and counts. Highest value, same play that worked on
   California, and the page already exists.
2. **Washington and Oregon** — deepest non-CA books, both with viable zone
   tables, both already have pages.
3. **Create Arizona**, then Oklahoma.
4. **The remaining nine data-backed states** — add each state's median and
   typical range to its existing page.
5. **Leave Group 3 alone** unless you want them consolidated.

## Methodology notes for whatever gets published

- Say "bound policies", not "quotes" — the distinction is load-bearing and the
  California pages already set that precedent.
- State the window: **Feb 2025 – Aug 2026**.
- Publish the count alongside every median. A median from 33 policies is honest
  when the 33 is visible; it is not when hidden.
- Do not publish a median below n=30 without labelling it clearly as indicative.
- "All-in" here is surplus-lines private flood: premium + policy fee + state
  surplus lines taxes. That differs from the NFIP fee stack — the California
  pages get this wrong if copied verbatim, so restate it per state where tax
  treatment differs.

## Files

| File | Contents |
|---|---|
| `data/state-medians-bound.csv` | 16 states: policies, median, p25, p75, properties quoted, bind rate |
| `data/state-zone-medians.csv` | Zone medians for the 7 states deep enough to carry one |
| `data/noncal-city-medians.csv` | The 5 non-CA cities clearing n≥10 |

---

## How California is handled across the two sites

**Decision: keep California in the hub table, link the row to
californiafloodinsurance.com, and never build a `/california-flood-insurance/`
page on Statewide.**

Cannibalization happens at the **page** level, not the data level. One row in a
27-row comparison table is not competing for "california flood insurance cost" —
it isn't targeting that query, isn't optimized for it, and carries no California
prose. A dedicated California page on Statewide *would* compete, directly and
badly. That page is the thing to never build.

Omitting California instead would cost more than it saves. A "cost by state"
table missing the largest flood market in the country reads as incomplete to a
human and thin to a crawler, and California is 44% of the underlying sample —
dropping it weakens the credibility of the whole dataset.

The outbound link is what actually prevents the overlap: it tells both readers
and Google that the California authority lives on the other domain. **Follow the
link — do not `nofollow` it.** It is a genuine editorial recommendation between
related properties; nofollowing your own specialist site passes no useful signal
and reads as hedging.

Note the two sites publish California on different bases and this is a feature,
not a conflict: CFI publishes **$722 bound**, the Statewide hub shows **$719
quoted**. Nearly identical from independent cuts, which is good corroboration —
but the labels must stay distinct so they never look like two answers to the
same question.

### The real cross-site risk is duplicated structure, not the California row

The two sites share an address, a phone number, an author and a theme lineage
(Statewide was the clone source). Google will associate them trivially. That is
fine — provided the **content** does not duplicate. Which means state pages must
not be the California page with names swapped.

Each state page carries data no other page has: Arizona's zones separate by only
$23 where most states spread hundreds; Oklahoma's median building limit is
$190,000 against $250,000 everywhere else; Texas and Florida are Zone-X-dominant
while Arizona and Oklahoma are AE-dominant. That state-specific evidence is what
keeps these pages out of doorway territory, and it is not optional.

## Internal linking: hub-and-spoke, not a mesh

`references/internal-linking.md` caps contextual links at 8–12 even on a pillar
page, and names "same exact anchor everywhere" as an over-optimization signal.
Linking all 27 state pages to each other would mean 702 links and 26 near-
identical anchors per page — the exact doorway pattern the quality gates target.

- **Hub → all 27.** A data table with one row per state is an index, not link
  stuffing. This is the one page that links widely.
- **Each state → hub + 2–4 genuine neighbours.** Geographic or hazard-profile
  adjacency only. Arizona → Nevada, New Mexico. Oklahoma → Texas, Missouri.
  Texas → Louisiana, Oklahoma. Florida → Georgia, South Carolina.

Every page then clears "minimum 3 outbound, no orphans" without approaching the
cap, and the link graph reads as geography rather than as a scheme.

## Pages drafted

| File | Words | Internal links | Status |
|---|---|---|---|
| `hub-cost-by-state.html` | — | 24 + CFI | replaces the hub's cost section |
| `pages/arizona-flood-insurance.html` | 771 | 3 | **new page**, none exists |
| `pages/oklahoma-flood-insurance.html` | 761 | 3 | **new page**, none exists |
| `pages/texas-cost-section.html` | 470 | 1 | **section only** — replaces one H2 on the existing page |
| `pages/florida-cost-section.html` | 507 | 1 | **section only** — replaces one H2 on the existing page |

All four clear the 600-word location-page minimum, carry no `<h1>` (the theme
supplies it), have table captions and `scope` attributes, and link hub plus two
geographic neighbours — three outbound each, against a minimum of 3 and a cap
of 10.

**Differentiation check.** Pairwise vocabulary overlap across the four pages
runs **32–38%**, which is about what four articles on the same subject in
different states should share. Templated location pages typically run 80%+.
Each carries a finding the others cannot:

| State | The thing only this page can say |
|---|---|
| Arizona | Zones separate by just $23 — AE $581 against X $568 — because monsoon runoff ignores floodplain boundaries |
| Oklahoma | Cheapest in the book at $465, driven by a $190,000 median building limit; 3.7× spread from 10th to 90th percentile |
| Texas | 58% of quotes are Zone X — most Texas flood cover is voluntary — yet AE runs $892, a $278 zone gap |
| Florida | 21% of properties exceed the NFIP's $250,000 statutory cap, the highest anywhere; AE $895 is the most expensive in the book |

That state-specific evidence is what keeps these out of doorway-page territory.
It is not decoration and should not be trimmed for length.


---

## Texas and Florida are SECTION replacements, not page replacements

Corrected 16 Aug 2026 after the apply agent stopped on an ambiguous boundary —
correctly, because the instruction was wrong.

The first drafts were written as standalone pages, like Arizona and Oklahoma.
But Texas and Florida already exist and are well structured:

```
H1  [State] Flood Insurance — Private & NFIP Coverage
H2  What to know
H2  Why [State] homeowners need flood insurance
H2  How much does flood insurance cost in [State]?   ← replace ONLY this
H2  Private flood insurance vs. the NFIP in [State]
H2  What [State] flood insurance covers
H2  Which [State] flood zone are you in?
H2  Get your [State] flood insurance quote
H2  [State] flood insurance FAQ
```

A standalone draft duplicated the FAQ, the zone explainer and parts of the
private-vs-NFIP argument. Pasting it in would have created duplicate content;
pasting it over everything would have deleted useful sections it does not
replace.

**The section files are the fix.** Each opens with the existing H2 verbatim —
`How much does flood insurance cost in [State]?` — so any table of contents or
anchor pointing at it keeps working, then uses H3 subsections beneath. Nothing
else on the page is touched. The existing FAQ stays; ours is dropped.

Measured against the live pages, the new sections share **32% (Texas)** and
**34% (Florida)** of their vocabulary with what is already published — normal
for prose on the same subject, and far from duplication.

**Lesson for future state work:** check whether the target page exists and how
it is structured *before* drafting. New pages get standalone drafts; existing
pages get section replacements anchored on a heading that is already there.
