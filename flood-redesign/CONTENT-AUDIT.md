# Final pre-launch audit of both new sites — 5 August 2026

Prompted by Aaron: *"should you do another look inside both Divi sites and make sure nothing is missing
in the new sites or that we have all the new content and not the old thin content that did not rank."*

Everything before this checked one direction — **what is missing from the new sites.** This checks the
other, which turned out to matter more: **what came across that should not have.**

---

## First, the distinction that reframes the question

Aaron's question bundled thin content with PageSpeed and Lighthouse. They are unrelated, and the
measurements say so plainly. Lighthouse run locally against real Chromium, mobile emulation:

| Page | Perf | A11y | Best prac. | SEO | LCP | CLS | TBT |
|---|---:|---:|---:|---:|---:|---:|---:|
| Statewide `/faqs/` (21 accordions) | **99** | 100 | 100 | 66 | 2.1 s | 0 | 0 ms |
| Statewide `/tennessee-flood-insurance/` | **99** | 100 | 100 | 66 | 2.1 s | 0.001 | 0 ms |
| California home | **98** | 100 | 100 | 66 | 2.4 s | 0 | 60 ms |
| California `/flood-zone-map/` — **a 4-word post** | **99** | 100 | 100 | 66 | 1.4 s | 0.002 | 40 ms |

Two things follow.

**Performance is not a problem anywhere.** 98–99 mobile, perfect accessibility and best practices,
essentially zero layout shift and blocking time. The SEO 66 is one audit — *"Page is blocked from
indexing"* — which is the deliberate staging `noindex`. Every other SEO audit passes, so **SEO becomes
100 the moment the noindex comes off at launch.** Nothing to fix.

**And Lighthouse cannot see the actual problem.** A post containing four words scores 99. Thin content is
invisible to Lighthouse, because Lighthouse measures delivery, not substance. It is a Google *ranking*
issue, not a performance one. So "did not rank with PageSpeed and Lighthouse" conflates a solved problem
with an unsolved one — the theme fixed speed comprehensively, and pruning is a separate job Lighthouse
will never prompt you to do.

---

## The real finding: California's new site carries 29 near-empty posts

Statewide is clean — 7 posts, all newly written, 455–578 words. California kept its whole legacy blog.

**59 posts. 34 under 400 words. 29 under 150.** The bottom of the range is not "thin", it is empty:

| Words | Slug |
|---:|---|
| 1 | `flash-flooding-problems-homeowners-businesses` |
| 4 | `flood-zone-map` |
| 13 | `changes-coming-fema-new-flood-bill` |
| 15 | `flood-insurance-mandatory-flood-zones` |
| 24 | `assess-private-flood-insurance` |
| 27 | `valet-parking-flood-zone` |
| 30–63 | eighteen more |
| 68–121 | five more |

**These were always empty — the migration did not lose anything.** Checked against California production
directly: the same pages render 15–47 words there. They have been sitting on the live site for years.

Full list and a verified redirect map: `california-prune-redirects.tsv`.

### Against that, the 14 worth keeping

`comparing-the-admitted-vs-non-admitted-insurance-markets` (1,490 words),
`understanding-base-flood-elevation-bfe` (1,480), `which-flood-zone-requires-flood-insurance` (1,466),
`when-is-flood-insurance-required` (1,447), `master-flood-policies-hoas` (1,421),
`loss-of-use-coverage-in-flood-insurance` (1,393), `how-much-flood-insurance-is-required-by-lender`
(1,378), `what-does-flood-insurance-not-cover` (1,329), `do-you-need-flood-insurance` (1,322),
`can-flood-insurance-drop-you` (1,243), `how-much-does-flood-insurance-cost` (1,240),
`navigating-flood-zone-x` (1,159), plus two around 650.

These are the strongest content on either site. **Half of California's blog is excellent and half is
close to blank** — which is exactly why an average would have hidden it.

---

## Fixed already

### Three pages would have launched saying "content migrates here from the live site"

`/commercial/`, `/guides/` and `/hoa-master-flood-policies/` on California are **unfilled migration
scaffolding.** The visible body text reads *"Commercial Flood Insurance — content migrates here from the
live site."* It also reaches the meta description, the Open Graph description, and the schema
`description`.

`/guides/` and `/hoa-master-flood-policies/` do not exist on production at all (both 404), and
`/commercial/` 301s there — so all three are new pages that were scaffolded and never written. Real
equivalents already exist: `/commercial-flood-insurance/` and the 1,421-word
`/master-flood-policies-hoas/`. **Recommend deleting all three and redirecting** — they are in the prune
map. Statewide has no placeholders at all.

### California's ad landing page had the placeholder as its search snippet

**This was the worst single item found.** `/get-a-quote/` is rendered by `page-get-a-quote.php`, so the
placeholder never appeared on screen — but the page had no meta description, so Rank Math generated one
from the page content. The result, live in the `<head>`:

```
<meta name="description" content="Get a Quote — content migrates here from the live site.">
<meta property="og:description" content="Get a Quote — content migrates here from the live site.">
<meta name="twitter:description" content="Get a Quote — content migrates here from the live site.">
```

That is the search snippet and the social preview for **the page all the Google and Microsoft spend
points at.** Invisible on the page itself, which is why nobody would have caught it by looking.

Fixed 5 Aug, with real descriptions written and verified live on four pages:

| Page | Was |
|---|---|
| California `/get-a-quote/` | the placeholder above |
| Statewide `/get-a-quote/` | no description |
| Statewide `/agent-appointment/` | no description |
| Statewide `/service-center/` | no description |

---

## Confirmed sound

- **Statewide's 64 pages**: no placeholders, no thin pages beyond templates and utility pages.
- **All 29 statewide state pages**: 721–1,078 words, meta on every one.
- **Nothing valuable is missing.** Both directions of the parity check are now closed: statewide's 48
  legacy URLs are handled by redirects, California shows zero missing URLs, and the reverse sweep found
  no absent content — only surplus.

## What needs your decision

1. **Prune California's 29 near-empty posts** using `california-prune-redirects.tsv`. Every target
   verified 200. This is the one item with real upside left: it removes half a blog of thin pages from a
   site whose other half is genuinely strong.
2. **Delete the three placeholder pages** and let the redirects cover them.
3. **Optional, post-launch:** 16 California posts sit between 150 and 599 words — the judgement band.
   Worth revisiting once the site is live and Search Console can say which of them earn anything.
