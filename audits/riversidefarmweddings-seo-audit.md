# SEO Audit — riversidefarmweddings.com

**Audit date:** 28 July 2026
**Site:** https://riversidefarmweddings.com (www → non-www, 301, correct)
**Business:** Riverside Farm — wedding & events venue, 57 Tweed River Drive, Pittsfield, VT 05762
**Stack:** WordPress · Avala 1.1.5 theme · Bold Page Builder · Rank Math PRO · Cloudflare
**Scope crawled:** 24 sitemap URLs + 51 internal link targets + archives, feeds, and technical endpoints

---

## Executive summary

The site's foundations are sound — HTTPS, clean canonical/redirect handling, a valid Rank Math sitemap, no broken internal links, no accidental `noindex` on money pages. Nothing is catastrophically wrong.

The gap is that a **local venue business is running with no local signals and no rich-result markup**, on top of a page-builder theme that ships ~435 KB of HTML per page. Three things account for most of the recoverable opportunity:

1. **No `LocalBusiness`/`EventVenue` schema anywhere**, and Rank Math is misconfigured as a *Person*.
2. **No `FAQPage` or `Review`/`AggregateRating` markup**, despite a genuinely strong 10-question FAQ page and five on-page testimonials.
3. **343 KB of inline CSS on every single page** plus 14 render-blocking stylesheets and 2.67 MB of unoptimised homepage imagery.

Below that sit a sitewide broken heading hierarchy (20 of 24 pages have no `<h2>` at all), ~23 thin archive pages diluting a 12-post blog, and money pages that are too thin to compete.

### Scorecard

| Area | Grade | Note |
|---|---|---|
| Indexability & crawl | B | Clean, but archive bloat and a stray `?page_id=5` |
| Canonicalisation & redirects | A− | Correct; 5 internal links point at redirects |
| Structured data | **D** | No local/FAQ/review schema; wrong entity type |
| On-page (titles, headings) | **D+** | Broken heading hierarchy sitewide; 9 over-length titles |
| Content depth | C− | 10 pages under 500 words; blog stale and 2025-framed |
| Performance | **D** | 435 KB avg HTML, 14 blocking CSS files, 2.67 MB images |
| Internal linking | C | Flat and template-driven; no editorial cross-linking |
| Local SEO | **D** | No schema, no NAP markup, no location pages |

---

## Critical — fix first

### 1. No `LocalBusiness` / `EventVenue` structured data

Every page emits the same graph: `Organization|Person`, `WebSite`, `ImageObject`, `WebPage`, `Person`, `Article`. There is **no address, no geo-coordinates, no telephone, no opening hours, no price range** in structured data anywhere on the site.

For a physical venue competing on "wedding venue near me" style intent, this is the single highest-value missing item.

Additionally, the entity is declared as:

```json
{"@type": ["Organization", "Person"], "@id": ".../#person", "name": "Riverside Farm"}
```

`Organization` and `Person` on one node is a Rank Math misconfiguration — someone set **Titles & Meta → Local SEO → Person** instead of **Organization**. Google will not treat this as a business entity.

**Fix:** In Rank Math, switch the site entity to **Organization**, enable the **Local SEO** module, and populate the full NAP. Target markup:

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "EventVenue"],
  "@id": "https://riversidefarmweddings.com/#organization",
  "name": "Riverside Farm Weddings & Events",
  "url": "https://riversidefarmweddings.com/",
  "telephone": "+1-802-746-8822",
  "email": "events@riversidefarm.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "57 Tweed River Drive",
    "addressLocality": "Pittsfield",
    "addressRegion": "VT",
    "postalCode": "05762",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 43.7730, "longitude": -72.8132 },
  "maximumAttendeeCapacity": 500,
  "sameAs": [
    "https://www.facebook.com/riversideweddings/",
    "https://www.instagram.com/riversidefarm/",
    "https://www.pinterest.com/riversidefarmvt/",
    "https://www.theknot.com/marketplace/riverside-farm-vermont-pittsfield-vt-220784",
    "https://www.weddingwire.com/biz/riverside-farm-amee-farm-lodge-pittsfield/e75f97883fff5f26.html"
  ]
}
```

Also confirm the Google Business Profile is claimed, categorised as *Wedding venue*, and that its NAP matches the above character-for-character.

### 2. No `FAQPage` schema on `/faqs/`

`/faqs/` carries ~846 words across roughly ten substantive questions — venue capacities per barn, peak season, transportation requirements, required vendors, driving distances from six cities. This is exactly the content Google rewards with FAQ rich results, and it is marked up as a generic `Article`.

**Fix:** Add `FAQPage` + `Question`/`acceptedAnswer` markup. The driving-distance answer ("Burlington 1.5 hours, Boston 2.5–3 hours…") is also a strong AI-overview and featured-snippet candidate.

### 3. No `Review` / `AggregateRating` markup

The homepage renders five named testimonials (Kathleen, Ali, Caoimhe, Devon, Marika) as plain HTML, and the venue holds 71 WeddingWire reviews off-site. None of it is marked up. Star ratings in the SERP are one of the largest CTR levers available to a venue.

**Fix:** Mark up on-page testimonials as `Review` nodes attached to the `LocalBusiness` entity. Only aggregate ratings that are genuinely collected and displayed on the site — do not import off-site averages into `aggregateRating`, which violates Google's review snippet policy.

### 4. Page weight and render-blocking resources

Measured on the homepage:

| Metric | Value |
|---|---|
| HTML document | 555 KB uncompressed / 56 KB gzipped |
| **Inline `<style>` in that HTML** | **343 KB across 12 blocks — 62% of the document** |
| Render-blocking stylesheets | 14 files, 1.4 MB uncompressed / 160 KB over the wire |
| JavaScript files | 24 files, ~646 KB (GTM alone 515 KB) |
| Images | **2.67 MB across 24 files**, zero WebP/AVIF |
| Average across all 24 pages | 435 KB HTML uncompressed / 42 KB gzipped |

Specific offenders:

- **`avala/style.css` — 769 KB uncompressed.** The theme ships its entire stylesheet on every page.
- **One inline `<style>` block of 251 KB** injected by Bold Page Builder. Because it's inline it is re-downloaded on every page view and can never be cached across pages. This is the single biggest structural performance problem on the site.
- **`bw-hug.jpg` (480 KB)** is the likely LCP element and is **not preloaded**. `inspire.jpg` is 555 KB, `20221022_rice-306.jpg` is 481 KB. All full-size JPEG.
- **The 121 KB logo PNG is rendered in four separate `<img>` tags** in the header markup.
- **20 of 33 homepage images lack `loading="lazy"`.**
- No `preconnect` to `fonts.gstatic.com` (only a `dns-prefetch` to `fonts.googleapis.com`, which is not the host that actually serves the font files). No resource preloads of any kind.

**Fix, in order of payoff:**
1. Convert the uploads library to WebP (a plugin such as Converter for Media, or Cloudflare Polish, which is already in front of the site). Expect roughly a 60–70% reduction on 2.67 MB.
2. Resize hero and testimonial JPEGs to their actual display dimensions and add `srcset`.
3. `<link rel="preload" as="image">` the LCP hero; add `loading="lazy"` to everything below the fold.
4. Add `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`.
5. Investigate whether Bold Page Builder can write its 251 KB block to an external cached stylesheet rather than inlining it.
6. Deduplicate the four header logo `<img>` tags.

*Note:* I was unable to obtain Core Web Vitals field or lab data — the PageSpeed Insights API daily quota was exhausted, and browser egress from this sandbox is blocked by the proxy, so a local Lighthouse run could not load the page. Server TTFB measured 0.25–0.35 s behind Cloudflare, which is healthy; the risk is concentrated in LCP and CLS, not server response. **Run PageSpeed Insights directly on `/`, `/riverside-farm-wedding-lodging/`, and `/riverside-farm-wedding-barns/` to get real numbers before and after the image work.**

---

## High priority

### 5. Index bloat: ~23 thin archive pages for a 12-post blog

All category and tag archives are `index, follow`:

- **9 category archives:** bridal, design, dresses, landscape, photography, planning, tips-tricks, vermont, wedding
- **14 tag archives:** budgeting, colors, culture, events, hiking, ideas, nature, photography, planning, recommendations, tips, trends, vermont, wedding-planning

That's 23 near-duplicate listing pages generated from 12 posts — several tags apply to a single post, so the archive is a verbatim duplicate of one excerpt. They are also *not* in the sitemap, which sends Google a contradictory signal: indexable, but not declared.

**Fix:** `noindex, follow` all tag archives. Keep at most 3–4 genuinely useful category archives (Planning, Vermont, Real Weddings), give each a unique intro paragraph, and add those to the sitemap. `noindex` the rest.

### 6. `?page_id=5` is indexable and duplicates the blog listing

`https://riversidefarmweddings.com/?page_id=5` returns 200, is `index, follow`, **self-canonicalises to the ugly parameter URL**, and is listed in `post-sitemap.xml`. It duplicates `/riverside-farm-wedding-blog/`. It also has **zero `<h1>`** and shares its meta description verbatim with `/top-2025-trends-to-elevate-your-wedding-day-celebration/`.

**Fix:** 301 `?page_id=5` → `/riverside-farm-wedding-blog/` and remove it from the sitemap.

### 7. `robots.txt` does not declare the sitemap

Current contents, in full:

```
User-Agent: *
Disallow:
```

**Fix:** append `Sitemap: https://riversidefarmweddings.com/sitemap_index.xml`.

### 8. Heading hierarchy is broken sitewide

**20 of 24 pages have zero `<h2>` elements** and jump straight from `<h1>` to `<h3>`. This is a page-builder default, and it costs you: `<h2>` is the primary signal Google uses to understand a page's sub-topics and to select featured-snippet content.

The homepage runs `H1 → H3 → H2 → H4 → H2 → H4 → H3 → H2 → H3 → H4` — out of order throughout.

Individual defects:

- **`/?page_id=5`** — no `<h1>` at all.
- **`/contact-riverside-farm/`** — two `<h1>`s. The second is an empty `<h1 class="formFooterLogo">` wrapping a *commented-out* agency credit link to systematicrevenue.com. It is dead markup emitting a second top-level heading on the page.
- **`/wedding-events/`** — two `<h1>`s ("From First Dance to Send-Off" and "Seeing Is believing"; note also the lowercase "believing").

**Fix:** convert section headings on each page from `<h3>` to `<h2>`; delete the `formFooterLogo` `<h1>`; demote the second `<h1>` on `/wedding-events/` to `<h2>`.

### 9. Text concatenation bugs inside headings

Two headings render two separate strings jammed together with no space:

- `/riverside-farm-vermont-wedding-venues/` — `<h1>` reads **"ABOUT USUNRIVALED SCENERY. UNFORGETTABLE EXPERIENCE."**
- Homepage `<h3>` reads **"THE FARMNatural Beauty. Modern Elegance."**

The `<h1>` case is the more damaging: the primary heading of your main "About / Venue" page — the one targeting *Vermont wedding venue* — is a garbled string. It appears to be an eyebrow label and a headline merged in the page-builder element.

**Fix:** separate the eyebrow text into its own element. Make the `<h1>` something targeted, e.g. *"Riverside Farm — A 700-Acre Vermont Wedding Venue in Pittsfield"*.

### 10. Title tags

Nine titles exceed the ~60-character SERP display limit, and several spend their most valuable opening words on filler adjectives rather than keywords:

| Chars | Current title | Problem |
|---|---|---|
| 96 | Capturing the Magic: Wedding Photography Tips, Musts, Do's and Don'ts - Riverside Farm | Truncated by ~36 chars |
| 80 | Experience the Best Vermont Wedding Venue: Riverside Farm's Rustic Elegance | Keyword pushed past the fold |
| 75 | 2025 Color trends for a stunning Spring Wedding in Vermont - Riverside Farm | Over length; stale year |
| 66 | **Explosive** Wedding Planning Details for Your Riverside Farm Wedding | "Explosive" is wrong-register for weddings |
| 50 | **Intriguing Weddings:** Contact Riverside Farm Today! | 20 chars wasted before the intent word |
| 50 | **Exciting Highlights of** Riverside Farm in the Media | Same |
| 46 | Your FAQs Answered! **Delight in** Riverside Farm. | Same |

Duplicates:

- **Duplicate title + description:** `/portfolio/` and `/portfolio/riverside-farm-gallery/` are byte-identical. (`/portfolio/` correctly canonicalises to the gallery — but it is still listed in the sitemap, which should only contain canonical URLs. Remove it.)
- **Duplicate description:** `?page_id=5` and `/top-2025-trends-.../` share the same meta description.
- **Over-length description:** `/riverside-farm-wedding-lodging/` at 183 characters (limit ~155).

The homepage title — *"Riverside Farm - Vermont Weddings and Events Venue"* — is decent but omits **"Barn"** and **"Pittsfield"**, the two modifiers that actually appear in high-intent queries for this venue type. Consider *"Vermont Barn Wedding Venue in Pittsfield | Riverside Farm"*.

---

## Medium priority

### 11. Thin money pages

| Page | Words | Comment |
|---|---|---|
| `/portfolio/riverside-farm-gallery/` | 240 | Gallery with almost no text |
| `/riverside-farm-wedding-blog/` | 247 | Blog index |
| `/riverside-farm-in-the-media/` | 337 | 29 images, 337 words |
| `/riverside-farm-wedding-barns/` | **417** | **Core money page** |
| `/riverside-farm-wedding-lodging/` | **475** | **Core money page** |
| `/riverside-farm-vermont-wedding-venues/` | **495** | **Main "About/Venue" page** |

The three bolded pages are the ones you need to rank. Site average is 587 words; competitors ranking for *Vermont barn wedding venue* run 1,200–2,000 words with per-space detail.

Notably, **the richest venue content on the site is buried inside the FAQ** — the Stonewell Barn (200 guests), Red Barn (130–200), Stone Cellar (100), and The Meadow (500+) are each described there but have no page of their own.

**Fix:** promote each space to its own page under `/riverside-farm-wedding-barns/`, with capacity, dimensions, seasonality, photo set, and `EventVenue` schema. That converts one 417-word page into four strong ones and gives the FAQ something to link to.

### 12. The blog is stale and mis-dated

All 12 posts carry 2025 framing in mid-2026: *"2025 Color trends…"*, *"2025 Smart budgeting…"*, *"Top 2025 trends…"*. Anything with a year in the title decays hard once that year passes, and couples searching now are planning 2027 weddings.

There's also a typo in a URL slug: `/2025-smart-budgeting-for-a-a-stunning-vermont-wedding/` ("for a a").

**Fix:** refresh and retitle the three year-stamped posts to 2027, updating `dateModified`. Leave the slugs alone where possible — or 301 if you change them. Publishing cadence looks like a burst in July 2025 and nothing since; a monthly cadence would help.

### 13. Image markup

- **Unsized images → layout shift (CLS):** 28 of 30 images on `/riverside-farm-wedding-lodging/`, 15 of 17 on `?page_id=5`, 14 of 16 on `/riverside-farm-wedding-barns/`, 9 of 15 on `/wedding-events/` have no `width`/`height` attributes.
- **Alt text as a raw URL:** one homepage image has `alt="https://riversidefarmweddings.com/wp-content/uploads/2024/03/smile.jpg"`.
- **Empty alt** on the Instagram feed image; one `<img>` with no `src`.
- Instagram feed alt attributes are full multi-line caption dumps — harmless but not useful.

### 14. Internal links pointing at redirects

Five internal links hit a 301 instead of the destination:

| Link | Redirects to | Found on |
|---|---|---|
| `/riverside-farm-lodging/` | `/riverside-farm-wedding-lodging/` | `/riverside-farm-vermont-wedding-venues/` |
| `/the-barns-of-riverside-farm/` | `/riverside-farm-wedding-barns/` | `/riverside-farm-vermont-wedding-venues/` |
| `/riverside-farm-vermont-wedding-venues/services` | `/contact-riverside-farm/` | `/riverside-farm-vermont-wedding-venues/` |
| `/riverside-farm-vermont-wedding-venues/contact` | `/contact-riverside-farm/` | `/riverside-farm-vermont-wedding-venues/` |
| `/vermont-wedding-ceremony` *(no trailing slash)* | `/wedding-events/` | Homepage |

Four of the five are on the same page. Low severity individually, but they're a one-line fix each.

### 15. Internal linking is flat

Every page links to the same 12 template destinations (nav + footer), and almost nothing else. There is no editorial cross-linking — the FAQ describes four barns without linking to the barns page; blog posts don't link into lodging or the gallery.

**Fix:** add 2–4 contextual in-body links per page, pointing from informational blog content into the money pages.

---

## Low priority

- **`Article` schema on service pages.** `/faqs/`, `/wedding-events/`, `/riverside-farm-wedding-lodging/`, `/contact-riverside-farm/` and the homepage are all typed as `Article` with an author of "riversidefarm2024". These are service pages, not articles. Set Rank Math's post-type default for Pages to `WebPage`.
- **`twitter:data2` reads "Time to read 53 minutes"** on the homepage. Rank Math is counting the 343 KB of inline CSS as body copy — a useful symptom to watch as a proxy for whether the inline-CSS fix landed.
- **Footer carries dofollow outbound links** to the theme developer (boldthemes on Facebook, Instagram, Pinterest). Remove or `rel="nofollow"`.
- **Contact email is on a different domain** (`events@riversidefarm.com` vs. the site's `riversidefarmweddings.com`). Not an SEO defect — `riversidefarm.com` correctly 301s to the primary domain with a matching canonical — but worth aligning for brand consistency, and make sure the GBP and directory listings use one address consistently.
- **Address typo:** one instance renders as `57 Tweed River Dr.Pittsfield` (missing space).
- Correctly handled already, for the record: `author/` and internal search are `noindex, follow`; `/terms-and-conditions/` is `noindex, nofollow`; `www` and `riversidefarm.com` both 301 to the canonical host; 404s return a real 404; Cloudflare caching is active with a 31-day `max-age`.

---

## Content & keyword opportunities

The site has **no page at all** for several of the highest-intent queries in this category:

1. **Pricing / packages.** *"vermont wedding venue cost"* and *"barn wedding venue price"* are heavy-volume, bottom-of-funnel queries. The FAQ mentions site fees but there is no page. Even a ranged "investment" page with a starting price outperforms silence — and it pre-qualifies enquiries.
2. **Real weddings.** The Press page links **out** to eight photographer blogs that host Riverside Farm galleries (Chelsea Proulx, Ellen Sargent, Erin Covey, Love Buzz, Sabin Gratz, Susan Stripling, Dream Love, Wedding Chicks). Every one of those is a real wedding *at your venue* whose content lives on someone else's domain. Host your own real-wedding write-ups with vendor credits — it's the strongest content type in this vertical and it converts.
3. **Per-space pages** — Stonewell Barn, Red Barn, Stone Cellar, The Meadow (see item 11).
4. **Location intent** — *"Killington wedding venue"* (you're 15 minutes away and the FAQ says so), plus a *"Vermont destination wedding"* page aimed at the Boston / NYC / Hartford couples whose drive times you already list.
5. **Seasonal** — you note September–October is peak season. A dedicated *"Fall Wedding in Vermont"* page would capture leaf-season search, which is the strongest seasonal query cluster in the state.

Competitors ranking for these terms — [The Round Barn Farm](https://theroundbarn.com/spring-wedding-venues-in-vermont/), [The Barn at Smugglers' Notch](https://www.barnatsmuggs.com/vermont-wedding-venues) — win largely on dedicated guide content plus per-space detail pages, not on domain strength.

---

## Prioritised plan

### Weeks 1–2 — technical quick wins
1. Rank Math: switch entity Person → **Organization**, enable Local SEO, fill NAP.
2. Add `LocalBusiness`/`EventVenue` schema with address, geo, phone, capacity, `sameAs`.
3. Add `FAQPage` schema to `/faqs/`.
4. Add `Sitemap:` to `robots.txt`.
5. `noindex, follow` all 14 tag archives and the weakest category archives.
6. 301 `?page_id=5` → `/riverside-farm-wedding-blog/`; drop it and `/portfolio/` from the sitemap.
7. Delete the empty `formFooterLogo` `<h1>` on the contact page.
8. Fix the two concatenated headings ("ABOUT USUNRIVALED…", "THE FARMNatural…").
9. Repoint the five internal links that hit redirects.

### Weeks 3–6 — performance
10. WebP conversion across the uploads library (Cloudflare Polish is the fastest route, it's already in front of the site).
11. Resize and `srcset` the hero and testimonial JPEGs; preload the LCP image.
12. `loading="lazy"` on the 20 unlazy homepage images; add `width`/`height` everywhere.
13. `preconnect` to `fonts.gstatic.com`.
14. Investigate externalising Bold Page Builder's 251 KB inline stylesheet.
15. Re-run PageSpeed Insights and record before/after.

### Weeks 6–12 — content
16. Rewrite the nine over-length titles; strip the filler adjectives.
17. Convert `<h3>` section headings to `<h2>` sitewide.
18. Expand the three core money pages to 1,000+ words.
19. Build four per-space pages (Stonewell, Red Barn, Stone Cellar, Meadow).
20. Publish a pricing/investment page.
21. Launch a Real Weddings section; reclaim the eight off-site galleries.
22. Refresh the three 2025-titled blog posts to 2027.

---

## Methodology

Full crawl of all 24 sitemap URLs plus 51 discovered internal link targets and 45 external ones; status codes, redirect chains, canonicals, robots directives, titles, descriptions, heading trees, structured data, image attributes, and byte weights measured directly from raw HTML responses. `robots.txt`, all three sitemaps, feeds, author/search/tag/category archives, and 404 behaviour verified individually. CSS and JS payloads measured by fetching each asset; image payloads by `HEAD` request.

**Not measured:** Core Web Vitals field and lab data. The PageSpeed Insights API returned a daily quota error, and a local Lighthouse run against the pre-installed Chromium could not complete because browser HTTPS egress is blocked in this environment (`ERR_CONNECTION_RESET` at the proxy). Performance findings above are derived from static resource analysis and server timing, which is sufficient to identify the causes but not to state an LCP/CLS/INP score. Also outside this audit: Google Search Console and Analytics data, backlink profile, and Google Business Profile configuration — all of which need account access.
