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
⚠️ **Do not add an AggregateRating block** unless the page visibly displays real reviews with a matching count/score (e.g., via a Google Reviews widget). Fabricated review markup risks a Google manual action. Add it later, from the widget, with real numbers.

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
