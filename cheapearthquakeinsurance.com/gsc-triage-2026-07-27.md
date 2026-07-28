# cheapearthquakeinsurance.com — GSC Indexing Triage

**Date:** July 28, 2026
**Source:** 5 GSC Coverage drill-down exports (2026-07-27) + GSC alert email of 2026-07-28

## Verdict

The "odd page names" are **spam product URLs in German** (161 of them) — fake e-commerce
pages like `/products/SpongeBob-SquarePants-Pyjama-Set-Herren-Langarm-Schlafanzug/1266335`,
`/products/Mercedes-ML-Klasse-1998-2005-Scheibenbremse-Mit-Zubeh-r/813615`, etc.
This is the classic **doorway-page spam pattern** (usually from a compromised plugin/theme
or a spam-link campaign pointing at fabricated URLs). Google crawled them repeatedly from
~July 2025 through April 2026.

**The mitigating news:** every one of them now returns **404 (Not found)** — the correct
response. Google is in the process of dropping them. There is no evidence in these exports
that spam pages are still being served.

## What each export showed

| Issue | Pages | Contents | Action |
|---|---|---|---|
| Not found (404) | 161 | German spam `/products/…` URLs + literal wildcard entries (`/wp-admin/*`, `/wp-content/themes/Divi/*`) | Leave as 404 (see below); investigate origin |
| Crawled – currently not indexed | 22 | Mix: feeds/author archive (fine) + **real content pages** incl. `/should-you-buy-earthquake-insurance-in-california/`, `/residential-earthquake-quote/`, `/service/faq/`, `/benefits-of-multiple-insurance-carriers/` | Content quality problem — real pages Google won't index |
| Excluded by 'noindex' (×2 duplicate exports) | 6 | `wp-login.php` variants + one `/feed/` | Intentional, no action |
| Blocked due to other 4xx | 1 | `/wp-admin/admin-ajax.php` | Normal, no action |
| **Blocked due to access forbidden (403)** | ? | **Export not received** — this was the headline issue in the GSC email | **Need this export** |

Notable: `/?wordfence_logHuman=…` appears in the crawl list → **Wordfence is installed**.
Wordfence (or its rate limiting) is the most likely cause of the "403 Forbidden" issue in
the GSC email — it sometimes blocks Googlebot after aggressive-crawl false positives.

## Immediate actions (security first)

1. **GSC → Security & Manual Actions → Security issues** for this property — if Google
   detected a hack it will say so here. Screenshot/report result.
2. **Wordfence → full scan** (high sensitivity). Look for modified core files, unknown
   files in `wp-content/uploads/`, and unfamiliar admin users (Users → Administrators).
3. **Update everything:** WordPress core, Divi, all plugins. The doorway-page hack usually
   enters through an outdated plugin.
4. **Check the sitemap** (`/sitemap_index.xml` or Yoast equivalent) — confirm no
   `/products/` URLs are listed in any sitemap.
5. **Wordfence → Firewall → check whether verified Googlebot is being blocked/throttled**
   (Live Traffic → filter by Googlebot; also Blocking log). If Googlebot appears there,
   allowlist verified Google crawlers. This is the fix for the 403 email.

## What NOT to do

- **Do not redirect the 404 spam URLs** to the homepage — that tells Google the spam URLs
  are real. 404 is correct; 410 (Gone) is marginally faster to drop but optional.
- Do not "Validate fix" in GSC for the 404 report — no fix is needed; they should 404.

## The quieter, bigger problem

"Crawled – currently not indexed" on the site's **actual money pages** (`/residential-earthquake-quote/`,
`/should-you-buy-earthquake-insurance-in-california/`, `/service/faq/`) means Google saw the
content and judged it not worth indexing. That's a content-quality/authority verdict, and it's
the same fix as the jumpins.com program: unique California-specific content, FAQ schema,
E-E-A-T signals, and interlinking with jumpins.com. Once the security items above are clear,
this site needs the same treatment.
