# Paste-ready fixes — Risk Rating 2.0, Hiscox FloodPlus, Flood Zone X

Second-pass audit, 16 Aug 2026, after the cost-by-zone page went live. Every
change below is a surgical find-and-replace against the live post body in the
WordPress **Code editor**. Do not replace these bodies wholesale — they're good
pages.

Scores held from the first pass: Risk Rating 2.0 **84**, Hiscox **80**, Zone X
**76**. What the second pass added: quote-book figures none of them carry, and
three defects that repeat across all three.

## What repeats on all three pages

| Issue | RR2 | Hiscox | Zone X |
|---|---|---|---|
| Zero external links (5,748 words of YMYL, no primary sources) | ✗ | ✗ | ✗ |
| Zero links to the new cost-by-zone page | ✗ | ✗ | ✗ |
| Only image is the author headshot — no in-content visual | ✗ | ✗ | ✗ |
| Heading hierarchy | ✓ clean | ✓ clean | ✓ clean |
| Single H1, canonical, index/follow | ✓ | ✓ | ✓ |

The author photo now carries correct alt text on all three (that fix was
theme-level and propagated automatically).

**The image gap is the one thing a patch can't fix.** Each page has exactly one
image and it's the byline. Risk Rating 2.0 in particular publishes a three-row
zone table and a percentile spread with no chart. That needs an asset, not
markup — flagged, not patched.

---

## 🔴 ZONE X — the one correctness bug

The page understates its own price by ~11%.

**Find:**
```
<strong>29% of NFIP flood claims come from moderate- to low-risk areas.</strong> And Zone X is where cover is cheapest: we typically place private policies here at around <strong>$450 a year</strong>, all in.
```

**Replace:**
```
<strong>From 2014 to 2024, 29% of NFIP flood insurance claims came from outside high-risk flood areas</strong> — the zones FEMA labels B, C and X (<a href="https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk" target="_blank" rel="noopener">FEMA, FloodSmart.gov</a>). And Zone X is where cover is cheapest: across the 101 Zone X policies we bound in California in 2025&#8211;2026, the median all-in cost was <strong>$509 a year</strong> (<a href="/california-flood-insurance-cost-by-zone/">see every zone</a>).
```

That single edit closes four things at once: the wrong price, the uncited 29%,
the missing external link, and the missing link to the cost page.

**Why the price matters more than the percentage suggests.** $450 sits near the
25th percentile of your Zone X book, not the middle — so roughly three in four
Zone X buyers pay more than the page promises. A prospect anchors on $450, gets
quoted $509+, and the gap reads as bait. It now also contradicts the cost-by-zone
page directly.

### Zone X — second edit, optional but strong

The page argues Zone X cover is worth buying but has no evidence about behaviour.
Your book has it: **Zone X binds at 26% against 59% in Zone AE.** People shop
voluntary cover and walk away. Add after the pricing paragraph:

```
<p>The behaviour bears that out. Across our California book, Zone X quotes convert to bound policies about a quarter of the time, against nearly six in ten in high-risk Zone AE — people treat &#8220;not required&#8221; as &#8220;not needed&#8221; and walk away from a $509 decision. That is exactly the calculation this page exists to reopen.</p>
```

---

## 🟠 RISK RATING 2.0 — strongest page, three gaps

### 1. Cite the 29% (appears once, mid-sentence, no trailing period)

**Find:**
```
<strong>29% of NFIP flood claims come from moderate- to low-risk areas</strong>
```

**Replace:**
```
<strong>from 2014 to 2024, 29% of NFIP flood insurance claims came from outside high-risk flood areas</strong> (<a href="https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk" target="_blank" rel="noopener">FEMA, FloodSmart.gov</a>)
```

### 2. Close the comparison the page sets up and never finishes

The page publishes NFIP medians at a specific cut — California, $250,000
building, $5,000 deductible, single-family — then stops. Your own book sits
almost exactly on those terms: 70% of bound policies are at $250k building and
91% at a $5,000 deductible. Filtered to the same terms, **n=1,121**:

| | NFIP (OpenFEMA, in force) | Your book (bound 2025–26) |
|---|---|---|
| Median all-in | $1,244 | **$773** |
| A zones | $1,246 | $774 |
| X / B / C zones | $1,082 | $670 |

**Find** the paragraph beginning `That single number is the clearest evidence`
and insert this as a new paragraph **immediately after** it:

```
<p><strong>So what does the private market charge at those same terms?</strong> Across the 1,121 California policies we bound in 2025&#8211;2026 at $250,000 of building coverage with a $5,000 deductible &mdash; the same cut measured above &mdash; our median all-in cost was <strong>$773 a year against the NFIP&#8217;s $1,244</strong>. Two caveats belong with that: the federal figures are policies in force while ours are newly bound, and &#8220;all-in&#8221; carries different fees on each side &mdash; the NFIP adds the reserve fund assessment, federal policy fee and HFIAA surcharge, while ours adds a policy fee and California surplus lines taxes. Our <a href="/california-flood-insurance-cost-by-zone/">full cost breakdown by flood zone</a> has the per-zone detail.</p>
```

### 3. The zone table has no `<caption>` or `scope`

Same defect the cost-by-zone table had. This is what lets a screen reader and an
AI extractor bind "$1,246" to *A zones* rather than reading it as a loose number.

**Find:**
```
<table>
<thead>
<tr>
<th>Rated zone</th>
<th>Median annual cost</th>
<th>Policies measured</th>
</tr>
</thead>
```

**Replace:**
```
<table>
<caption style="caption-side: bottom; padding-top: 10px; font-size: 14px; text-align: left; color: #555;">Median annual all-in NFIP cost by rated zone, from 10,545 in-force California policies at $250,000 building coverage, $5,000 deductible, single-family residential. Source: FEMA OpenFEMA NFIP policy file.</caption>
<thead>
<tr>
<th scope="col">Rated zone</th>
<th scope="col">Median annual cost</th>
<th scope="col">Policies measured</th>
</tr>
</thead>
```

Then change each first cell in the body from `<td>A zones (high risk, inland)</td>`
to `<th scope="row">A zones (high risk, inland)</th>`, and the same for the X/B/C
and V rows.

### 4. Link OpenFEMA

The page analyses OpenFEMA data across 2,282 words without linking it once.
Wherever the methodology paragraph names the source, link it:
`https://www.fema.gov/openfema-data-page/fima-nfip-redacted-policies-v2`

**Verify that URL in a browser first** — fema.gov blocks this environment, so I
could not confirm it resolves. If it has moved, search fema.gov for "OpenFEMA
NFIP redacted policies" rather than dropping the citation.

---

## 🟠 HISCOX FLOODPLUS — good page, zero evidence

1,920 words about a product you place constantly, with **no data at all**. Your
book has plenty.

### 1. Quantify the $250k cap argument — honestly

The page's lead argument is the federal $250,000 building cap. True, and worth
making — but your book shows it binds on a **minority**: 116 of 1,665 California
bound properties (7%) carry building limits above $250,000. The largest you
wrote is **$1.2M**. Understating that is safer than overstating it, and the real
numbers are more persuasive than the abstract point.

**Find:**
```
The NFIP&#8217;s residential building limit is <strong>$250,000</strong>, and it is statutory — no underwriter can raise it, because Congress sets it. Any home that costs more than that to rebuild is underinsured by construction under a federal policy.
```

**Replace:**
```
The NFIP&#8217;s residential building limit is <strong>$250,000</strong>, and it is statutory — no underwriter can raise it, because Congress sets it. Any home that costs more than that to rebuild is underinsured by construction under a federal policy. In our own California book that applies to about one property in fourteen, but when it applies it matters enormously: the largest building limit we have placed is <strong>$1.2 million</strong>, nearly five times what a federal policy could have covered.
```

### 2. Add the market-share evidence

Nothing on the page says how FloodPlus actually performs against its rivals.
Across CA bound rows where at least two markets returned a quote (n=1,857), a
Hiscox program was the cheapest **38%** of the time, and Hiscox FullValue
returned a quote on 83% of rows — the broadest participation of any market.

Add near the top, after the opening description:

```
<p>That is not a theoretical preference. Across the California policies we bound in 2025&#8211;2026 where at least two markets returned a quote, a Hiscox program came in cheapest about <strong>38% of the time</strong> &mdash; more than any other single market we shop, though still well short of a majority. That is the whole argument for quoting all of them rather than defaulting to one: see our <a href="/california-flood-insurance-cost-by-zone/">cost breakdown by flood zone</a> for what that actually costs.</p>
```

### 3. Link FEMA for the statutory cap

The $250,000 figure is the page's load-bearing claim and it's uncited. Link
FEMA's NFIP coverage-limits page where the cap is first stated — **verify the URL
in a browser first**, same caveat as above.

---

## Verify after applying

Logged out or cache-busted, for each page:

- Zone X: `$509` present, `$450` absent, FloodSmart link resolves
- RR2: new comparison paragraph reads correctly in context; table shows a caption
- Hiscox: `38%` and `$1.2 million` present
- All three: one link to `/california-flood-insurance-cost-by-zone/`
- Rich Results Test: schema types unchanged, no new errors
- GSC → URL Inspection → Request Indexing on each

## Not patched — needs assets or decisions

- **No in-content images on any of the three.** RR2 most acutely: it publishes a
  zone table and a percentile spread with no chart. A bar chart of the three zone
  medians, or of the $845–$2,007 interquartile band, would earn its place.
- **Hiscox has no table at all** despite comparing NFIP and private across four
  dimensions. A comparison table would suit it and is extractable by AI.
- **RR2 `dateModified` is 28 seconds after `datePublished`** — it has never been
  substantively updated. Once these edits land, that becomes a genuine
  modification and the date will reflect real maintenance.
