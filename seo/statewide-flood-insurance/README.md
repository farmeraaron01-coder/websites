# Statewide Flood Insurance — data-backed content plan

Analysed 16 Aug 2026 from the same inception-to-date quote export used for the
California work (`../california-flood-insurance-cost-by-zone/data-analysis.md`).
Same method: bound policies only, deduplicated to one per property by hashed
street+ZIP, all-in cost = premium + policy fee + surplus lines taxes and fees.

**No prior Statewide deliverable exists in this repo.** If an earlier audit was
done, it was in another session and isn't recorded here — this is the first.

---

## The headline correction

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
