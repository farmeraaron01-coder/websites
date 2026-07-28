# SEO Audit — www.kevingillotti.com

**Date:** 28 July 2026
**Scope:** Full technical + on-page audit. 303 URLs discovered via `wp-sitemap.xml`; 263 crawled successfully.
**Platform:** WordPress 7.0.2 · KingSize theme · WPBakery Page Builder 8.7.4 · Apache / PHP 7.4.33 · GoDaddy shared cPanel (`p3plzcpnl507852.prod.phx3.secureserver.net`)

---

## Executive summary

The site is comprehensively indexed (263 live pages of race galleries going back to 2015) but is held back by four structural problems, any one of which would meaningfully cap organic performance:

1. **HTTPS is completely broken.** The certificate is a self-signed GoDaddy host default that expired **19 July 2025**. Chrome refuses the connection outright.
2. **The homepage contains no indexable content** — 140 characters of rendered text, all of it navigation.
3. **Every page is missing an H1 and a meta description** — 263 out of 263.
4. **Analytics has been dead for roughly three years** — the site still runs Classic Google Analytics (`ga.js`), retired long ago.

The content asset is genuinely strong: 238 race pages, a decade of results, and real media coverage. The technical foundation is what is not letting it rank.

### Priority ranking

| # | Issue | Severity | Effort |
|---|---|---|---|
| 1 | HTTPS broken / expired self-signed certificate | Critical | Low |
| 2 | Homepage has zero indexable content | Critical | Medium |
| 3 | No H1 on any page | Critical | Low–Medium |
| 4 | No meta descriptions on any page | High | Medium |
| 5 | Google Analytics dead since 2023 | High | Low |
| 6 | Title tags bloated / duplicated | High | Medium |
| 7 | Duplicate `/races-YYYY/` vs `/portfolio-category/races-YYYY/` | High | Low |
| 8 | No Open Graph / Twitter Card tags | High | Low |
| 9 | No structured data (JSON-LD) | Medium | Medium |
| 10 | Server returns 503/415 under crawl load | Medium | Low |
| 11 | Thin content (94% of pages under 300 words) | Medium | High |
| 12 | Image alt text, sizing, caching | Medium | Medium |

---

## 1. Critical — HTTPS is broken

The single most damaging issue on the site.

```
subject = CN = p3plzcpnl507852.prod.phx3.secureserver.net
issuer  = CN = p3plzcpnl507852.prod.phx3.secureserver.net   (self-signed)
notAfter = Jul 19 15:46:00 2025 GMT                          (expired)
```

Observed behaviour:

| Request | Result |
|---|---|
| `https://www.kevingillotti.com/` in Chrome | `ERR_CONNECTION_RESET` — page will not load |
| `https://kevingillotti.com/` in Chrome | Same |
| `https://…` ignoring cert errors | Serves a **"Coming Soon" placeholder page**, not the site |
| `http://www.kevingillotti.com/` | 200 OK, serves the real site |
| `http://kevingillotti.com/` | 301 → `http://www.kevingillotti.com/` (correct) |

So there are two separate faults stacked: the certificate is invalid *and* the HTTPS vhost points at a different document root than the HTTP vhost.

**Consequences**

- HTTPS has been a confirmed Google ranking signal since 2014. The entire site is on `http://`.
- Chrome marks every page **"Not secure"** in the address bar. The contact form and the Athlete Card order form both collect user input over plaintext.
- Any inbound link, social share, or citation written as `https://` is a dead link today. That link equity is being lost entirely.
- All 263 indexed URLs, all 238 canonical tags, and the `robots.txt` sitemap reference are `http://`.

**Fix**

1. Install a valid certificate covering both `kevingillotti.com` and `www.kevingillotti.com`. GoDaddy cPanel includes free AutoSSL — enabling it is usually a single toggle.
2. Point the HTTPS vhost at the same document root as HTTP so it stops serving the "Coming Soon" page.
3. Update the WordPress Site Address and Home URL to `https://`.
4. Add a site-wide 301 from `http://` to `https://www.` in `.htaccess`.
5. Run a search-replace across the database for `http://www.kevingillotti.com` → `https://…` (there are **53,889** hard-coded `http://` self-references across the site, a median of 198 per page).
6. Once stable, add HSTS.
7. Resubmit the sitemap in Search Console under the `https://` property.

---

## 2. Critical — The homepage has no indexable content

Measured in a real Chromium render (iPhone 13 viewport, after full load plus an 8-second settle):

| Metric | Homepage | `/about/` for comparison |
|---|---|---|
| Rendered body text | **140 characters** | 4,329 characters |
| Body scroll height | **45 px** | 5,489 px |
| `<h1>` elements | 0 | 0 |
| `<h2>` elements | **0** | 1 |

The entire rendered text of the homepage is:

> `HOME GALLERIES 15 RACE RESULTS 7 ATHLETE CARD SUPER⑧SLINGSHOT MEDIA COVERAGE SPARTAN UP PODCAST ABOUT KG 2 CONTACT Search for: Search Button`

That is the navigation menu and nothing else. The page is a full-screen Vimeo background video (`player.vimeo.com/video/168363687`) with a nav overlay. There is no headline, no paragraph copy, no name in a heading — nothing describing who Kevin Gillotti is or what he does.

This is the site's most authoritative URL and the one that accumulates the most links. Google has essentially nothing to work with on it.

**Fix.** Keep the video hero, but add real content beneath it: an H1 with the name and primary positioning (e.g. *"Kevin Gillotti — Elite Obstacle Course Racer & Endurance Athlete"*), two or three paragraphs of biography, current-season highlights, key career achievements, and internal links to Race Results, About, and Media. Aim for 400–600 words of genuine copy.

---

## 3. Critical — No H1 on any page

**263 of 263 pages have zero `<h1>` elements.** Verified in both raw HTML and the rendered DOM.

The KingSize theme renders page titles as `<h2>` (e.g. `/about/` → `<h2>ABOUT KG</h2>`). The homepage has no heading at all. The only other headings site-wide are the `<h5>` navigation labels, so the document outline runs H5 → H2 with no H1 — which is also why Lighthouse fails `heading-order`.

**Fix.** Change the theme's page-title output from `<h2>` to `<h1>` (single template edit in the KingSize theme, applies site-wide), and add a proper H1 to the homepage.

---

## 4. High — No meta descriptions anywhere

**263 of 263 pages have no meta description.** Google is auto-generating every snippet, which for gallery pages means scraped nav text or image captions.

There is also no SEO plugin installed (no Yoast, Rank Math, or AIOSEO markers in the HTML) — which is why descriptions, Open Graph, and schema are all absent together.

**Fix.** Install Rank Math or Yoast. Hand-write descriptions for the ~25 pages that matter (homepage, About, Contact, Media, Athlete Card, Race Results, each `/races-YYYY/`), and set a template for the 238 portfolio pages, e.g. *"Photos and results from %title% — Kevin Gillotti, elite obstacle course racer."*

---

## 5. High — Analytics has been dead since 2023

The site runs **Classic Google Analytics**:

```js
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-131382-11']);
_gaq.push(['_trackPageview']);
```

`ga.js` with a `UA-` property. Universal Analytics stopped processing data on 1 July 2023 and UA properties were deleted in July 2024. There is no `gtag.js` and no GA4 property anywhere in the markup.

**No traffic data has been collected for roughly three years**, which means there is currently no way to measure the impact of any fix in this report.

**Fix.** Install GA4 and verify the site in Google Search Console (as an `https://` property, after the certificate is fixed). This should be done *first* so there is a baseline before other changes land.

---

## 6. High — Title tags

| Measure | Value |
|---|---|
| Pages carrying the boilerplate suffix `– Kevin Gillotti Multi-Sport Racer Endurance Athlete` | **263 / 263 (100%)** |
| Pages over 60 characters | **260 / 263 (99%)** |
| Median length | 80 characters |
| Longest | 152 characters |
| Pages sharing a duplicate title with another page | **74** (34 groups) |

The 50-character suffix on every title consumes most of the available SERP width, so titles truncate before the distinguishing part is visible.

Worst duplicate groups:

| Count | Title |
|---|---|
| 4× | `Spartan Super Arizona – Kevin Gillotti Multi-Sport Racer Endurance Athlete` |
| 3× | `2001 Accident – …` |
| 3× | `Duathlon – …` |
| 3× | `Spartan Sprint Utah – …` |
| 3× | `Kevin Gillotti Multi-Sport Racer Endurance Athlete` (bare) |
| 2× each | `Races 2015` … `Races 2026` (12 pairs — see §7) |

**Fix.** Shorten the site-name suffix to `| Kevin Gillotti` and add the year/location to repeated race names — `Spartan Super Arizona 2021 | Kevin Gillotti` rather than four identical titles. Target 50–60 characters.

---

## 7. High — Duplicate race-year listing pages

Every race year exists twice, as a page and as a taxonomy archive, with the same title and the same images:

| Year | `/races-YYYY/` | `/portfolio-category/races-YYYY/` |
|---|---|---|
| 2015 | 283 words, 28 images | 264 words, 28 images, **no canonical** |
| 2016 | 273 words, 28 images | 259 words, 28 images, **no canonical** |
| … | … | … |
| 2026 | 267 words, 26 images | 253 words, 26 images, **no canonical** |

All 12 pairs share an identical title tag. The taxonomy versions have no canonical tag, so nothing tells Google which to prefer — the two versions compete for the same query.

**Fix.** Either `noindex` the `/portfolio-category/` archives, or canonicalise each to its `/races-YYYY/` equivalent. The curated pages are the better landing pages, so pointing at those is the cleaner option.

---

## 8. High — No social sharing metadata

**0 of 263 pages** have Open Graph or Twitter Card tags.

When a race gallery is shared to Facebook, X, or in a WhatsApp/iMessage thread, the platform gets no title, no description, and no image — it will show a bare URL or scrape something arbitrary. For an athlete whose reach depends on race-day sharing, this is a direct loss.

**Fix.** An SEO plugin (§4) adds these automatically. Set a default share image, and use each race's hero photo as the `og:image` on portfolio pages.

---

## 9. Medium — No structured data

**0 of 263 pages** contain JSON-LD. There is no `Person` / `Athlete` schema, no `SportsEvent` markup on race pages, no `ImageObject` on galleries, no `BreadcrumbList`.

For a named individual, `Person` schema is what feeds the Google knowledge panel and entity understanding. Race pages are a natural fit for `SportsEvent` with date, location, and result.

**Fix.** Add `Person` schema on the homepage and About page (name, `sameAs` links to Instagram, Vimeo, Athlinks, and the Spartan profile, plus `award` entries for major results). Add `SportsEvent` to the 238 portfolio pages via a template.

---

## 10. Medium — Server capacity and crawl health

The origin degrades quickly under concurrent load:

- **10 simultaneous requests using a Googlebot user-agent → 4 returned `503`.**
- Sustained crawling at 2 concurrent connections → **40 of 303 URLs returned `415 Unsupported Media Type`**, an unusual WAF response that a crawler cannot interpret.
- Time to first byte: median **1.0–1.6 s** (Lighthouse: *"Root document took 1,570 ms"*).

Repeated 503s teach Googlebot to reduce crawl rate. With 303 URLs and a site that adds galleries every race weekend, that slows indexing of new content.

**Fix.** Add page caching (WP Super Cache or similar) — this alone should resolve most of it on shared hosting. Upgrade PHP from **7.4.33**, which reached end of life in November 2022 and no longer receives security patches; PHP 8.2+ is also substantially faster. If 503s persist, the shared plan is undersized.

---

## 11. Medium — Thin content

| Measure | Value |
|---|---|
| Median words per page | **241** |
| Pages under 300 words | **248 / 263 (94%)** |
| Pages under 250 words | 158 / 263 (60%) |
| Longest page | 1,584 words |

Most of that median is navigation and footer boilerplate — the 238 portfolio pages are image grids with a caption or two. Because the nav text is identical everywhere, the pages are near-duplicates of each other in Google's eyes.

**Fix.** This does not need to be done for all 238 pages. Prioritise the 20–30 most significant races (World Championships, OCRWC, national championships, Pikes Peak) and add 150–300 words each: finish time, placing, course conditions, what happened. That is content that can rank for `"[race name] [year] results"` queries and is the kind of first-hand account that generic race-listing sites cannot replicate.

---

## 12. Medium — Images

Across 263 pages, **9,659 images**:

| Issue | Count |
|---|---|
| Missing `alt` text | **1,558 (16%)** |
| Missing `width`/`height` attributes | 4,814 |
| Lazy-loaded | 4,021 (good) |

Specific problems:

- **`spain.jpg` — 1,636 KB at 1800×1075**, uploaded in 2016 and still served full-size on `/about/`. It is roughly two-thirds of that page's 2.44 MB total weight.
- Lighthouse: modern image formats would save **1,309 KiB**; correctly-sized images another **388 KiB**.
- **No `Cache-Control` or `Expires` headers on any static asset** — 73 resources flagged. Only `ETag`/`Last-Modified` are present, so returning visitors revalidate every file instead of serving from cache. Gzip *is* enabled, which is good.

**Fix.** Install an image optimisation plugin (ShortPixel, Imagify) with WebP conversion and bulk-optimise the media library. Add `Cache-Control: max-age=31536000` for `/wp-content/uploads/`, CSS, and JS in `.htaccess`. Add alt text to the ~1,558 images missing it, prioritising the ones on high-value pages.

---

## 13. Medium — Render-blocking resources and legacy dependencies

Median per page: **25 external scripts, 17 stylesheets, 21 KB of inline CSS, 134 KB of HTML.**

Lighthouse estimates **3,100 ms** of savings from eliminating render-blocking resources. The worst offenders:

| Blocking time | Resource |
|---|---|
| 2,046 ms | `foundation.min.js` (45 KB) |
| 1,766 ms | `fonts.googleapis.com` stylesheet |
| 1,296 ms | `jquery.fullwidthAudioPlayer.min.js` |
| 846 ms | `jquery.prettyPhoto.js` |
| 780 ms | `connect.soundcloud.com/sdk.js` |
| 780 ms | `netdna.bootstrapcdn.com/font-awesome/4.1.0/css` |

Several dependencies are long obsolete:

- **`html5shiv.googlecode.com/svn/trunk/html5.js`** — Google Code has been archived and read-only since 2016. This is a shim for Internet Explorer 8.
- **Font Awesome 4.1.0** from `netdna.bootstrapcdn.com` — released 2014; BootstrapCDN's NetDNA endpoint is a legacy alias.
- **SoundCloud SDK** (`connect.soundcloud.com/sdk.js`) — deprecated, blocking render for 780 ms.
- jQuery Migrate is loaded, indicating deprecated jQuery calls somewhere in the theme or plugins.

**Fix.** Remove the html5shiv and SoundCloud SDK entirely. Self-host Font Awesome and the Google Fonts CSS. Defer non-critical JavaScript. Load audio-player assets only on the pages that use them.

---

## 14. Lower priority

- **`robots.txt`** references `http://www.kevingillotti.com/wp-sitemap.xml` — update to `https://` after the certificate fix. Otherwise the file is correct.
- **25 pages have no canonical tag**: the homepage, all 20 `/portfolio-category/` archives, 3 `/portfolio-tags/` archives, and `/playlist/interviews/`. The other 238 pages have correct self-referencing canonicals (currently on `http://`).
- **`wp-login.php` is publicly reachable** (200) and `xmlrpc.php` is present. Not an SEO issue, but worth rate-limiting or restricting given the outdated PHP version.
- **404 handling is correct** — bogus URLs return a genuine 404, not a soft 200.
- **No redirect chains detected** — all 263 crawled URLs resolved directly with no intermediate hops. Clean.
- **`viewport` and `lang` attributes present on all pages** — correct.

---

## Lighthouse scores

Run against `/about/` (the homepage cannot be scored — see note below). Mobile emulation, simulated throttling.

| Category | Score |
|---|---|
| Performance | **64** |
| Accessibility | **82** |
| Best Practices | **69** |
| SEO | **77** |

| Metric | Value |
|---|---|
| First Contentful Paint | 4.3 s |
| Largest Contentful Paint | 4.7 s |
| Speed Index | 26.4 s |
| Total Blocking Time | 120 ms |
| Cumulative Layout Shift | **0** (excellent) |
| Server response time | 1,570 ms |
| Total page weight | 3,336 KiB |

Failing audits: `meta-description`, `crawlable-anchors`, `image-alt`, `color-contrast`, `heading-order`, `link-name`, `list`, `is-on-https` (**78 insecure requests**), `redirects-http`, `image-aspect-ratio`, `image-size-responsive`, `errors-in-console`.

CLS of 0 is genuinely good and worth preserving through any changes.

---

## Suggested sequence

**Week 1 — unblock**
1. Fix the SSL certificate and the HTTPS document root.
2. Force `http://` → `https://www.`, update WordPress URLs, database search-replace.
3. Install GA4 and verify Search Console on the `https://` property.
4. Submit the updated sitemap.

**Week 2 — on-page foundations**
5. Install an SEO plugin; configure title templates and Open Graph defaults.
6. Change the theme's page title from `<h2>` to `<h1>`.
7. Write homepage content with a real H1.
8. Write meta descriptions for the top ~25 pages.
9. `noindex` or canonicalise the `/portfolio-category/` duplicates.

**Week 3–4 — performance**
10. Page caching plugin; upgrade PHP to 8.2+.
11. `Cache-Control` headers for static assets.
12. Image optimisation and WebP conversion; replace `spain.jpg`.
13. Remove html5shiv and the SoundCloud SDK; self-host fonts and Font Awesome.

**Ongoing**
14. Add `Person` and `SportsEvent` structured data.
15. Expand the top 20–30 race pages with real race reports.
16. Backfill alt text.

---

## Method and caveats

- 303 URLs discovered from `wp-sitemap.xml`; 263 returned 200. The remaining 40 returned `415` due to the origin's rate limiting under crawl load (§10), not because the pages are broken — spot checks of those URLs individually returned 200.
- Rendering, heading, and content measurements were taken in headless Chromium (Playwright, iPhone 13 emulation) as well as from raw HTML, so JavaScript-injected content is accounted for.
- **PageSpeed Insights and CrUX field data were unavailable** (API quota). All performance figures are lab data from a local Lighthouse run, not real-user measurements. Once GA4 and Search Console are in place, re-check against field data.
- Raw paint timings from the direct Playwright runs (FCP ~14 s) are **not** reported as real-world figures — the audit environment blocks several third-party hosts, which inflated those numbers. The Lighthouse figures in the table above are the ones to rely on.
- Lighthouse only completed with Chrome's automatic HTTPS-upgrade feature disabled; with it enabled the run failed against the broken certificate. Ordinary Chrome does fall back to HTTP successfully, so this is a testing artefact rather than a user-facing failure — but it is a further sign of how the broken certificate interferes with tooling.
