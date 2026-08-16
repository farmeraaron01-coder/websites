# SEO patch — California Flood Insurance Costs by Zone

Target page: <https://californiafloodinsurance.com/california-flood-insurance-cost-by-zone/>
WordPress post ID **460** · category *Flood Insurance Guides* · Rank Math
Audit date: 2026-08-15 · Baseline SEO health score: **68/100**

The site is WordPress, not tracked in this repo, so these are drop-in artifacts
rather than a diff against source. Each file below is either paste-ready or a
unified diff you can apply by hand.

---

## Files

| File | What it is | Where it goes |
|---|---|---|
| `post-body.original.html` | The page's current post content, exactly as served (inner HTML of `div.cfi-prose`) | reference / rollback |
| `post-body.revised.html` | The corrected post content | paste into the post's Code editor |
| `post-body.patch` | Unified diff between the two | review before applying |
| `dataset-schema.jsonld` | `Dataset` schema for the rate table | Rank Math → post → Schema → Custom Schema, or a `wp_head` snippet on post 460 |
| `llms.txt.patch` | One-line addition to `/llms.txt` | apply to the live `llms.txt` |
| `theme-byline-alt.patch` | Author photo `alt` fix + Gravatar note | `cfi-kadence-child` theme |

## Apply order

1. **Regenerate the sitemap first.** This is the critical finding and nothing
   else matters until it's done — see *Not patched, item A* below.
2. Post body (`post-body.revised.html`), then re-save the post.
3. `dataset-schema.jsonld`.
4. `llms.txt.patch`.
5. `theme-byline-alt.patch`.
6. Validate: Rich Results Test on the URL, then GSC → URL Inspection → Request
   Indexing.

---

## What the post-body patch changes

**Removed the leftover build comment.** The post opened with
`<p><!-- PAGE META (add to <head>): ... --></p>`. To be precise: this is a
well-formed HTML comment and it does **not** render to users or to Google —
verified with a real HTML parser. It's removed because it documents an intended
canonical of `/flood-insurance-cost-by-zone/`, which **404s**, while the live
canonical is `/california-flood-insurance-cost-by-zone/`. Anyone who acts on
that note in future will canonicalize the page to a dead URL.

**Removed the duplicate `<h1>`.** The Kadence template already renders
`<h1>California Flood Insurance Costs by Zone – Median Rates 2024-2026</h1>`;
the post body opened with a second one. The sibling page
`/how-much-does-flood-insurance-cost/` has exactly one H1, so this was a
content-entry slip on this page, not a theme bug. The body H1 is deleted
outright rather than demoted — the template H1 already carries the term, and
the intro paragraph reads fine as the opener.

**Fixed three CTAs that told users to do something the page can't do.** The
copy said *"Enter your address **above**"*, *"Enter your address and we'll
quote you"*, and *"enter your address and get a quote"* — but the page has
**zero** `<input>`, `<select>` or `<form>` elements. "Above" pointed at
nothing. All three now point at `/get-a-quote/` in language that matches
reality. If you'd rather embed a real address field inline above the table,
do that instead and revert this part — it would convert better than a link.

**Added 16 in-content internal links, up from 2.** Every zone named in the
table now links to its own zone page, every city with a location page now
links to it, and the page connects to the pillar cost guide. All 18 link
targets were checked and return HTTP 200.

- Table rows → `/flood-zone-ae/`, `/navigating-flood-zone-x/`,
  `/flood-zone-ah-and-ao/` (AO and AH), `/flood-zone-a/`
- New line under the table → `/flood-zone-v-and-ve/`
- Cities → `/sacramento-flood-insurance/`, `/stockton-flood-insurance/`,
  `/los-angeles-flood-insurance/`, `/san-diego-flood-insurance/`,
  `/riverside-flood-insurance/`, plus a line linking
  `/san-jose-flood-insurance/`, `/long-beach-flood-insurance/`,
  `/fresno-flood-insurance/` and `/areas-we-serve/`
- Body → `/how-much-does-flood-insurance-cost/`,
  `/understanding-base-flood-elevation-bfe/`,
  `/which-flood-zone-requires-flood-insurance/`

Cities are linked only where the page name genuinely matches the city already
named in the copy. San Francisco Bay, Marin, Sonoma/Napa, Modesto, Orange
County, San Bernardino and Kern are left unlinked because no matching page
exists — adding zone claims for cities you haven't published on would be
inventing content.

**Added a "Zones V and VE" note.** You own `/flood-zone-v-and-ve/` but coastal
high-hazard zones were absent from the table entirely. The added line links
the page and states plainly that the dataset holds too few V/VE policies to
publish a median — which is honest and still captures the internal link.

**Table accessibility and machine-readability.** Added a `<caption>`,
`scope="col"` on header cells, and converted the zone cells to `<th scope="row">`.
This is what lets a screen reader and an AI extractor read "$650" as *Zone AE's
median annual cost* rather than as a loose number.

---

## Decisions — resolved 16 Aug 2026 via quote-book analysis

See `data-analysis.md` for the full findings. The patch now uses the real
numbers computed from the quoting-system export, approved by Aaron.

### The 299 / 291 discrepancy — moot

The old hand-counted table is replaced entirely. The table now reports **763
California new-business policies bound Feb 2025 – Aug 2026**, deduplicated to
one per property, with medians and 25th–75th percentile ranges per zone from
`data/zone-medians-ca-bound-nb.csv`.

### The FAQ answer text changed — keep the schema in sync

The patch adds the FEMA citation to the "Is Zone X flood insurance worth it?"
answer. That page's `FAQPage` JSON-LD is a **separate, hand-maintained block** —
it does not auto-generate from the post body. Structured data must match visible
content, so update that question's `acceptedAnswer.text` to the new wording:

> Yes, for most California homeowners. At a median of $509/year in our current
> book, it's an affordable way to cover a real risk — and FEMA's own data shows
> 29% of NFIP claims from 2014 to 2024 came from outside high-risk zones. We've
> filed claims on Zone X properties in every region of California — the official
> map is conservative. The question isn't "Do I need it?" but "Can I afford NOT
> to have it?"

(The "What's the difference between Zone A, AE, and AO?" answer also changed —
copy its new text from `post-body.revised.html` the same way.)

### The date window — resolved: 2025-2026

The quote-book export showed the current system's data begins Feb 2025, so
neither of the page's old windows (2024-2026, 2020-2026) matched any dataset.
Aaron approved publishing the honest window: **bound Feb 2025 - Aug 2026**.

Applied in the patch:

- H2 now reads *"California Flood Insurance Costs by Zone (2025-2026)"*; its
  anchor ID is `...-2025-2026`. The TOC generates from headings and will
  follow — **spot-check the TOC links after saving**.
- All dependent numbers updated: Zone X mentions are now $509 (was $465), the
  FEMA average-claim comparison recomputed (~160 years of premium), the FAQ
  zone-difference answer uses the new medians, the deductible list matches the
  real book ($1,000 / $2,000 / $5,000 / $10,000 - 91% choose $5,000).

**The `<title>` tag and meta description now REQUIRE updating** - they cite
"2024-2026" and the old $650/$465 figures, which no longer appear on the page.
Recommended:

> Title: California Flood Insurance Costs by Zone - Median Rates 2025-2026
> Meta: Real median flood insurance costs by FEMA zone, from 763 California
> policies we bound in 2025-2026. Zone AE $722, Zone X $509. Free quote.

The **FAQPage JSON-LD** must also sync to the two revised FAQ answers ("Is
Zone X flood insurance worth it?" and "What's the difference between Zone A,
AE, and AO?") - copy the new visible text from `post-body.revised.html` into
the matching `acceptedAnswer.text` fields.

The **table anchor changed** (`...-2020-2026` was never live; the live page
still has `...-2024-2026`) - after pasting, verify the "On this page" links
resolve. The Dataset schema's `contentUrl` fragment matches the new anchor.

---

## Not patched — needs your facts, not mine

**A. The page is missing from the XML sitemap. This is the critical item.**
`post-sitemap.xml` holds 20 URLs, newest `lastmod` `2026-08-11`. This page
published `2026-08-14` and is absent. `sitemap_index.xml` still reports
`2026-08-07`. Rank Math auto-appends new posts, so this is a stale sitemap
cache or a per-post exclusion.

Fix: Rank Math → Sitemap Settings → clear cache. Then verify:

```
curl -s https://californiafloodinsurance.com/post-sitemap.xml | grep cost-by-zone
```

If that still returns nothing, check the post's own "Exclude from sitemap"
toggle and Rank Math → Sitemap → Posts.

**B. The 29% statistic — RESOLVED, now patched.** Verified 16 Aug 2026 against
the primary source. FloodSmart.gov (the NFIP's official consumer site) states
verbatim: *"Over the past 10 years (2014 - 2024), nearly one-third of NFIP flood
insurance claims (29%) came from areas located outside of current high-risk
flood areas."* Source:
<https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk>

The patch now cites it inline and tightens the wording, which was imprecise in
three ways: it said "flood claims" (the figure is NFIP claims specifically),
gave no date window (it's a rolling 2014–2024 measure), and said "moderate- and
low-risk areas" (FEMA's own framing is "outside current high-risk flood areas",
i.e. Zones B, C and X). The patch also adds FEMA's average claim payment of
$82,614 (2020–2024) from the same page, which replaces the previously
unsupported "a single claim pays for decades of premiums."

Note on other figures in circulation: FEMA's older FAQ says ~25% and is tied to
the discontinued Preferred Risk Policy; ~40% appears in 2026 news coverage as
expert commentary, not a published FEMA statistic. 29% is the number FEMA itself
currently publishes — use it for anything compliance-sensitive.

**C. "Licensed in California since 1989" vs `foundingDate: 2012-01-01`.** The
body copy and the Organization schema disagree. Likely both are true of
different things (Aaron's licensure vs. the entity's founding) — if so, say
which is which. Left unchanged because only you know the answer.

**D. The sitewide `aggregateRating: 4.9 / 900 reviews`.** This sits on the
Organization node on every page. Self-serving aggregate ratings about your own
business — not tied to independently collected reviews displayed on-site — are
the classic trigger for a structured-data manual action. Worth confirming those
900 reviews are collected and surfaced somewhere on the site.

**E. Zero in-content images.** The page has three images total: the logo twice
and the author headshot. The declared `og:image`
(`coastal-homes-golden-hour.webp`) never appears on the page. A cost-by-zone
page is the most chartable page on the site — a bar chart of the seven zone
medians, or a FEMA zone map of California, would earn its place. Not patched
because it needs an asset, not markup.

**F. `/flood-insurance-rates/` is a 301 but is still published as a live URL.**
It redirects to `/how-much-does-flood-insurance-cost/`, yet it is still listed
in `page-sitemap.xml` and in `llms.txt`. Redirected URLs should be dropped from
both. Not part of this page's patch, but it's a five-minute cleanup — and it
means the cost-page cannibalization is a two-page problem (this page vs. the
cost guide), not three.

---

## Verify after applying

| Check | How | Expect |
|---|---|---|
| Page in sitemap | `curl -s .../post-sitemap.xml \| grep cost-by-zone` | one match |
| Single H1 | view-source, count `<h1` | 1 |
| No stray comment | search source for `PAGE META` | none |
| TOC anchors resolve | click every "On this page" link | all 11 land |
| Dataset schema valid | Google Rich Results Test | Dataset detected, no errors |
| Internal links live | click the zone and city links | all 200 |

## Leading indicators (no re-audit needed)

- **GSC → Pages**: this URL should leave "Discovered – currently not indexed"
  within 72h of the sitemap fix.
- **GSC → Performance**, query `california flood insurance cost`: if this page
  and `/how-much-does-flood-insurance-cost/` keep swapping as the ranking URL
  week to week, cannibalization is live and the two need a harder intent split.
- **GA4**: click-through rate from this page to `/get-a-quote/`, measured
  before and after the CTA fix. If it doesn't move, the CTA copy wasn't the
  bottleneck — embed the real address field.
- **GSC → Links**: the five zone pages should pick up internal-link counts from
  this URL. If their impressions don't move within six weeks, the links weren't
  their constraint and their own content depth is the thing to look at.
