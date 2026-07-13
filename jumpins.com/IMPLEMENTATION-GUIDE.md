# jumpins.com — SEO/GEO Fix Implementation Guide

Everything referenced below lives in this folder:

```
jumpins.com/
├── seo-geo-content-assessment.md   ← why we're doing this
├── IMPLEMENTATION-GUIDE.md         ← this file (do fixes in order)
├── fixes/
│   ├── robots.txt                  ← replacement robots.txt (crawl-delay removed, AI bots allowed)
│   ├── llms.txt                    ← upload to site root
│   ├── schema-homepage.json        ← InsuranceAgency JSON-LD for homepage
│   ├── schema-san-diego.json       ← for /contact-us/san-diego-office/
│   ├── schema-palm-desert.json     ← for /palm-desert-office/ (fill in street address)
│   ├── schema-faq-earthquake-example.json ← FAQPage template
│   ├── meta-descriptions.md        ← copy/paste titles + meta descriptions
│   ├── functions-snippet.php       ← WPCode snippet (viewport, xmlrpc, security headers)
│   └── nginx-snippet.conf          ← for hosting admin (redirects, HSTS, caching)
└── content/blog/                   ← 3 publish-ready posts with checklists
```

**Site:** WordPress + Divi 4.27.5 + Yoast SEO (free)
**Baseline (June 23, 2026 audit):** overall health 43/100 · content 52 · schema 22 · GEO/AI 28 · performance 42

---

## ✅ LIVE VERIFICATION — July 13, 2026

The live site was re-checked after network access was restored. **Most of the June audit's fixes are already deployed** — the site has moved substantially since the crawl. Verified status of each fix:

| Fix | Status | Verified detail |
|-----|--------|-----------------|
| 1. robots.txt | ✅ **DONE** | No `Crawl-delay` — clean Yoast-style file, sitemap declared |
| 2. Noindex utility pages | ❓ Unconfirmed | Couldn't verify robots meta on utility pages — spot-check in WP admin |
| 3. Titles + metas | ✅ Largely done | `/business-insurance/` has a strong drafted-style meta description; spot-check the rest against `fixes/meta-descriptions.md` |
| 4. H1 rendering | 🟡 **Partial** | Homepage now renders `<h1>` + H2/H3/H4 in crawlable HTML ✅ — but **blog posts still have no `<h1>`** (only H2s); fix the Divi blog template |
| 5. Schema | ✅ Largely done | Homepage: 2 JSON-LD blocks incl. Organization, local business data, **AggregateRating (live)**, GeoCoordinates, hours. San Diego office page has InsuranceAgency schema. **FAQPage schema still missing everywhere** |
| 6. llms.txt | ✅ **DONE** | https://jumpins.com/llms.txt serves the file (HTTP 200) and lists key pages incl. the new posts |
| 7. PHP snippet | ✅ Mostly done | `user-scalable=0` gone from viewport ✅ · xmlrpc.php returns 405 ✅ · but **no `X-Content-Type-Options: nosniff` header yet** |
| 8. Hosting fixes | 🟡 **Partial** | www/HTTP redirect is now single-hop ✅ — but **no HSTS header** and `server: nginx/1.31.1` still exposes version (give `nginx-snippet.conf` to hosting admin) |
| 9. Publish 3 posts | 🟡 **Published, needs E-E-A-T** | All 3 live since June 25 (`/earthquake-insurance-california-2026/`, `/wildfire-home-insurance-california-2026/`, `/california-home-insurance-non-renewal-crisis-2026/`) — but author shows **"Admin"** (older posts correctly show Aaron Farmer), no CA license # visible, no FAQPage schema, and the earthquake post **doesn't link to CheapEarthquakeInsurance.com** |

Also confirmed: `/seo-geo` returns 404 — it was never a page on the site.

### Remaining punch list (in priority order)

1. **Blog post authorship** — change the 3 new posts' author from "Admin" to Aaron Farmer (Users → reassign author), and add CA License #0F09648 to the byline/author box. This is the top E-E-A-T item.
2. **Blog post `<h1>`** — Divi blog template doesn't output the post title as H1 (FIX 4, step 4).
3. **FAQPage schema** — none anywhere on the site; add `schema-faq-earthquake-example.json` (adapted per page) to the earthquake post and money pages.
4. **Earthquake post CTA** — add the CheapEarthquakeInsurance.com quote link (see FIX 9 note on avoiding duplicate content).
5. **Hosting headers** — HSTS, nosniff, `server_tokens off` (FIX 7 header portion + FIX 8).
6. **Confirm noindex** on the FIX 2 utility pages.
7. Then move to the content program (assessment §5): Q&A restructure of money pages (auto page verified: good H1/H2 structure, but 0 FAQ schema), 4 local pages, 2-posts/month pipeline.

---

## FIX 1 — robots.txt: remove Crawl-Delay (5 min) 🔴 CRITICAL

`Crawl-delay: 30` limits Googlebot **and** GPTBot/ClaudeBot/PerplexityBot to ~2 pages/minute. This single line suppresses everything else on this list.

1. WP Admin → **Yoast SEO → Tools → File Editor** → **robots.txt** tab
2. Delete everything in the box, paste in the contents of `fixes/robots.txt`
3. Save, then verify at https://jumpins.com/robots.txt — no `Crawl-delay` line, AI bots explicitly allowed

## FIX 2 — Noindex utility pages + archives (30 min) 🔴 HIGH

**2a.** Yoast SEO → Search Appearance → **Archives** → disable Author archives and Date archives → Save
**2b.** For each page below: Edit page → Yoast box → **Advanced** tab → "Allow search engines to show this page?" → **No**:
`/slide-anything-popup-preview/` · `/agent-entered-commercial-fast-app/` · `/agent-entered-personal-fast-app/` · `/life-simple-form/` · `/life-changes-survey/` · `/commercial-fast-app/` · `/commercial-renewal-fast-app/` · `/personal-insurance/home-insurance/home-quote-form/`
**2c.** Yoast SEO → Search Appearance → **Taxonomies** → Categories → Show in search results → **No**

## FIX 3 — Titles + meta descriptions (2 hrs) 🟠 HIGH

Work top-to-bottom through `fixes/meta-descriptions.md` (13 pages + 4 existing blog posts). For each: Edit page → Yoast box → SEO tab → paste SEO Title and Meta description → Update.
Priority: `/business-insurance/` hub first, then both office pages, then `/contact-us/`.

## FIX 4 — Fix homepage & blog H1s (1 hr) 🟠 HIGH

The homepage and all blog posts render **zero H1/H2 tags** in crawlable HTML (Divi issue).

1. Diagnose: Google Search Console → URL Inspection → Test Live URL → View Tested Page → check whether H1s appear in the rendered DOM
2. If missing: in Divi, set the first text module's heading to semantic H1 (module settings → heading tag), or add a static H1 above the builder content
3. Target homepage H1: **"Independent Insurance Agency in California | Jump Insurance Services"**
4. Check the Divi blog template so post titles output as `<h1>`, then verify in View Source

## FIX 5 — Schema JSON-LD (1.5 hrs) 🟠 HIGH

⚠️ **Before publishing:** replace the `REPLACE-WITH-…` placeholders in the schema files with the real Facebook / LinkedIn / Yelp / Google Business Profile URLs, and the Palm Desert street address + ZIP.
ℹ️ **AggregateRating:** the homepage schema includes the Google review rating (4.9 / 75 reviews, shown on-site via the reviews plugin). Before pasting, update `ratingValue` and `reviewCount` to match the current live Google numbers, and keep them roughly in sync going forward — Google requires the markup to reflect reviews actually displayed on the page. If the reviews plugin already outputs its own AggregateRating schema, remove the block from this file instead so the page doesn't declare it twice.

For each page, add a Divi Code module (or Custom HTML block) at the bottom containing:

```html
<script type="application/ld+json">
…paste the matching fixes/schema-*.json…
</script>
```

- Homepage → `schema-homepage.json`
- `/contact-us/san-diego-office/` → `schema-san-diego.json`
- `/palm-desert-office/` → `schema-palm-desert.json` (also add the street address to the visible page content — it's currently missing)

Also: Yoast SEO → Search Appearance → General → Knowledge Graph: set Organization = Jump Insurance Services, upload logo, add the same social profile URLs.

## FIX 6 — llms.txt (10 min) 🟡 MEDIUM

Upload `fixes/llms.txt` to the site root (FTP / hosting file manager) so it resolves at https://jumpins.com/llms.txt. It currently returns homepage HTML instead of 404ing, so verify the file content actually loads.

## FIX 7 — PHP snippet: viewport, xmlrpc, security headers (15 min) 🟡 MEDIUM

1. Install **WPCode** plugin (free) → Code Snippets → Add New → PHP Snippet
2. Paste `fixes/functions-snippet.php` → Activate
3. Verify in DevTools → Network → response headers show `X-Content-Type-Options: nosniff`, and page source no longer has `user-scalable=0`

Do **not** edit the parent Divi theme's functions.php — it's overwritten on theme updates.

## FIX 8 — Hosting-level fixes (give `fixes/nginx-snippet.conf` to hosting admin) 🟡 MEDIUM

- Single-hop 301 for www/HTTP variants (currently a 2-hop chain)
- HSTS + security headers
- `server_tokens off`
- Enable caching: **WP Rocket** (easiest, also fixes the 17 render-blocking CSS files and 20 JS files) or nginx FastCGI cache. TTFB is currently 1.01s; target < 300ms
- While in WP admin: install **ShortPixel** or **Imagify** for WebP conversion, and fix alt text on the 7 homepage images missing it

## FIX 9 — Publish the 3 new blog posts (2 hrs) 🟠 HIGH (content)

The posts in `content/blog/` are publish-ready. Each has a header block with slug, meta description, tags, and a publish checklist. Non-negotiables for every post:

1. **Author byline with your name + CA license number** (this is the E-E-A-T signal the whole site is missing)
2. Visible publish date
3. Meta description pasted into Yoast
4. Title renders as `<h1>` (Fix 4 must be done first)
5. Earthquake post: keep the [CheapEarthquakeInsurance.com](https://www.cheapearthquakeinsurance.com/) link as the quote CTA — **do not copy the same article text onto both domains** (duplicate content splits ranking between the sites; each domain should have unique copy that links to the other)

## FIX 10 — Verify (30 min, one week later)

- [ ] https://jumpins.com/robots.txt — no Crawl-Delay
- [ ] https://jumpins.com/llms.txt — serves the text file
- [ ] Homepage source contains `<h1>` and `InsuranceAgency` schema
- [ ] Utility pages show `noindex` in source
- [ ] Rich Results Test (search.google.com/test/rich-results) passes on homepage + office pages
- [ ] Google Search Console: submit sitemap_index.xml, request indexing on homepage + 3 new posts
- [ ] Response headers include HSTS + nosniff
- [ ] PageSpeed Insights TTFB improved after caching enabled

---

## Effort summary

| Fix | Time | Impact |
|-----|------|--------|
| 1. robots.txt | 5 min | Critical — unblocks everything |
| 2. Noindex utility pages | 30 min | High |
| 3. Titles + metas | 2 hrs | High (+15-25% CTR) |
| 4. H1 rendering | 1 hr | High |
| 5. Schema | 1.5 hrs | High (local pack) |
| 6. llms.txt | 10 min | Medium (GEO) |
| 7. PHP snippet | 15 min | Medium |
| 8. Hosting/caching | 1-2 hrs | High (CWV) |
| 9. Publish 3 posts | 2 hrs | High (content/GEO) |
| **Total** | **~9 hrs** | Projected 68-72/100 in 60 days |

## After this: the content program

See `seo-geo-content-assessment.md` §5 — Q&A restructure of the auto/home/business pages with FAQPage schema, 4 local landing pages (San Diego ×2, Palm Desert ×2), and a 2-posts/month pipeline (SR-22, Mexico auto, FAIR Plan, San Diego flood zones, "what we're seeing in renewals" series).
