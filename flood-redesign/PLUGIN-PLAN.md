# CFI Staging — Plugin Plan

Detected on the live production site (from rendered output, July 2026):
AIOSEO Pro · Site Kit by Google · Trust Index · EWWW Image Optimizer ·
Schema & Structured Data for WP · Pojo Accessibility (toolbar) · OMGF (local fonts) ·
Google Tag Manager · Wordfence (paid — admin-only, not visible in page source) ·
Cognito Forms (embed script, no plugin needed)

Currently on staging: FormLayer + FormLayer Pro (active), Nginx Helper (active),
Akismet (inactive), Hello Dolly (inactive).

---

## Tier 1 — install before launch (required)

| Plugin | Why | Notes |
|---|---|---|
| **Wordfence** (your paid plan) | Security. This site takes payments-adjacent traffic and personal property data. | Paid license usually allows more than one install; if it's single-site, activate the key on the live domain at cutover and run free on staging until then. Turn OFF the "live traffic" feature — it's the one part that costs real performance. |
| **All in One SEO Pro** (AIOSEO) | Already runs the live site; owns titles, meta, sitemaps, redirects. Migrating its settings keeps rankings stable. | Export settings from live (AIOSEO → Tools → Import/Export) and import on staging. Do NOT also install Yoast or Rank Math — two SEO plugins fight over meta tags and canonicals. |
| **Trust Index** | The reviews section on the new homepage embeds widget `1e9552d4458412053506ba969a9`. | Install, connect the same Google profile. The theme lazy-loads the widget script, so it costs nothing until scrolled into view. |
| **Nginx Helper** | Already active — this is what purges the server-level cache when content is saved. | Keep. Settings → Nginx Helper → enable "Purge on post/page update." |
| **EWWW Image Optimizer** | Compresses and WebP-converts every image the content migration brings over. Your live library is unoptimized JPEGs. | Enable WebP + lazy-load; skip its "exactdn/CDN" upsell. |

## Tier 2 — install, with a decision attached

| Plugin | Recommendation |
|---|---|
| **Google Site Kit** | Install *after* launch, not on staging. It connects Search Console/Analytics to a live property; pointing it at a noindexed staging site creates noise. Tag Manager continues to carry Ads/Analytics tags. |
| **Schema & Structured Data for WP** | Optional now. AIOSEO Pro already outputs Organization, WebPage, Breadcrumb, Person and FAQ schema. The live site runs both, which is why 44 `SiteNavigationElement` blocks appear in its source — duplicated, low-value markup. Recommend: launch with AIOSEO schema only, add this back only if a specific schema type is missing. |
| **Pojo Accessibility** (the toolbar widget) | Recommend leaving it off. The new site scores **100/100 Lighthouse accessibility** natively — the toolbar's value was compensating for a site that didn't. It also adds JS on every page. Keep it only if a client or contract requires a visible accessibility widget. |
| **OMGF** (local Google Fonts) | Not needed. The child theme self-hosts Source Serif 4 + Inter and makes zero font CDN calls. Skip unless Kadence's own Google-font loader gets enabled later. |

## Tier 3 — remove / don't carry over

| Plugin | Why |
|---|---|
| **FormLayer + FormLayer Pro** (active on staging) | Nothing uses them — the quote flow is Cognito Forms via embed script. Two active form builders for zero forms. Deactivate and delete. |
| **Hello Dolly** | Novelty plugin. Delete. |
| **Akismet** | Only needed if comments are open. The new site has no comment forms; delete unless comments get enabled later. |
| Any Divi-specific plugins on the live site | Do not migrate. They die with Divi. |

## Explicitly NOT recommended

- **A caching plugin** (WP Rocket, W3TC, LiteSpeed, WP Fastest Cache). The host's nginx
  cache is faster and already verified working on this account. Two page caches fight
  over purges — that's what broke caching on several of the other sites.
- **A second SEO plugin.** Yoast/Rank Math alongside AIOSEO = duplicate meta and canonical conflicts.
- **A page builder.** Designed pages are coded PHP templates by decision.

## Target final stack (7 active)

Kadence + CFI child theme · Wordfence · AIOSEO Pro · Trust Index ·
Nginx Helper · EWWW Image Optimizer · (Site Kit, after launch)

That's a deliberately short list. Plugin count is the single biggest predictor of a slow
WordPress site, and the 98/100 desktop score depends on keeping it short.

## Order of operations on staging

1. Deactivate + delete FormLayer, FormLayer Pro, Hello Dolly, Akismet.
2. Install Trust Index → connect Google profile → verify reviews render on the homepage.
3. Install AIOSEO Pro → import settings export from the live site.
4. Install Wordfence → basic scan settings, live traffic OFF.
5. Install EWWW → WebP + lazy-load on.
6. Confirm Nginx Helper purge-on-update is enabled.
7. Re-run Lighthouse; confirm mobile hasn't regressed (each plugin costs something —
   if a score drops noticeably, that plugin needs justifying).
