# Static asset cache headers — the largest single PageSpeed win available

> ## CORRECTION, 7 Aug 2026 — read this before trusting anything below
>
> This file states that the theme's `.htaccess` rules put `max-age=31536000, immutable` on `woff2`.
> **That is true for the image types and false for fonts and CSS.** Measured on the live site:
>
> | Asset | Actual served `Cache-Control` |
> |---|---|
> | `assets/media/hero-poster.webp` | `public, max-age=31536000, immutable` — as intended |
> | `assets/fonts/inter-v2.woff2` | `max-age=604800` **and** `public, must-revalidate` |
> | `assets/css/tokens.css` | `max-age=604800` **and** `public, must-revalidate` |
>
> The responses carry `x-proxy-cache: STATIC/TYPE`: on this UltraStack stack **nginx serves fonts and
> CSS itself and never passes them to Apache**, so the `mod_headers` block in `inc/htaccess.php` never
> executes for those extensions. It reaches webp because webp falls through to Apache.
>
> Two consequences. Fonts and CSS get **7 days with revalidation**, not a year — so the repeat-visit
> saving claimed below is overstated for them. And two conflicting `Cache-Control` headers on one
> response is a defect in its own right; the theme cannot fix it from `.htaccess` because Apache is
> not in the path for these files. **Needs an InMotion ticket to set the header in nginx.**
>
> Practical fallout: font files must carry **versioned filenames** (`-v2`) rather than being
> overwritten in place, so deployment does not depend on host behaviour this file got wrong. Done in
> theme 1.5.4. See `PERFORMANCE.md`.

PageSpeed Insights, July 29 2026, on `https://new.californiafloodinsurance.com/`:

| | Est. savings from cache lifetimes |
|---|---|
| Mobile | **285 KiB** |
| Desktop | **2,065 KiB** |

Every asset it lists reports `Cache TTL: None`. Confirmed by request:

| Asset | Cache headers |
|---|---|
| `/wp-content/themes/cfi-kadence-child/assets/fonts/sourceserif4.woff2` | **none** |
| `/wp-content/themes/cfi-kadence-child/assets/media/hero-poster.webp` | **none** |
| `/wp-content/uploads/2026/07/logo.png` | `max-age=604800, public, must-revalidate` ✓ |

So `/wp-content/uploads/` **is** getting expires headers and `/wp-content/themes/` is **not**.
That is a server configuration gap, not a theme problem — nothing in PHP can set headers on
static files, because those requests never reach WordPress.

The desktop figure is much larger than mobile because of `raindrops-hero.mp4` (1.8MB), which
only loads above 720px. Without cache headers a returning desktop visitor re-downloads it
every single time.

## Fix

Add to the site's root `.htaccess`, **above** the `# BEGIN WordPress` block, or ask InMotion
support to extend whatever rule already covers `/wp-content/uploads/` to the whole of
`/wp-content/`:

```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp              "access plus 1 year"
  ExpiresByType image/jpeg              "access plus 1 year"
  ExpiresByType image/png               "access plus 1 year"
  ExpiresByType image/svg+xml           "access plus 1 year"
  ExpiresByType video/mp4               "access plus 1 year"
  ExpiresByType font/woff2              "access plus 1 year"
  ExpiresByType text/css                "access plus 1 month"
  ExpiresByType application/javascript  "access plus 1 month"
</IfModule>

<IfModule mod_headers.c>
  <FilesMatch "\.(webp|jpe?g|png|svg|mp4|woff2)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\.(css|js)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>
</IfModule>
```

A year is safe for fonts, images and video here because every one of them is either
version-stamped by WordPress (`?ver=`) or would be renamed on replacement. CSS and JS get a
month for the same reason — Kadence and the child theme both append `?ver=`.

**This must be applied to production at cutover too**, not only staging.

## Second finding, already fixed in the theme

The logo was a 61.4 KiB PNG at 250×227 being displayed at 84×76 — PSI estimated 60.4 KiB of
waste on every page load. An optimised WebP at 168×153 (2× the display size, for retina)
comes to **11.7 KiB**, an 81% reduction. Uploaded to the media library as attachment **263**:
`/wp-content/uploads/2026/07/cfi-logo-optimised.webp`

It still needs selecting: **Customize → Header → Logo** → choose that file. WordPress stores
the logo as a theme modification rather than a setting, so it cannot be set over the REST API.

## Third finding, fixed in v1.1.9

LCP breakdown on mobile was 70ms TTFB, **460ms resource load delay**, 530ms load, 210ms
render. The delay dominated because the hero image sits inside a `<picture>` the browser only
discovers after six render-blocking stylesheets resolve. v1.1.9 preloads the WebP on the front
page with `fetchpriority="high"`.

## Still open

**Render-blocking CSS: six stylesheets, ~550ms on mobile.** Four are Kadence's
(`global`, `header`, `content`, `footer`), plus `tokens.css` and `rankmath`. Kadence has a
per-page CSS / critical CSS option that would cut the unused portion; worth enabling and
re-measuring before launch.

**Desktop CLS 0.143.** PSI reported it; mobile was 0.001 on the same page. Not reproducible
here — the 1.8MB hero video never finishes loading through this environment's proxy chain
(`readyState` stays 0 after 32 seconds), so the desktop condition cannot be recreated.
Ruled out by inspection: Kadence's `--scrollbar-offset` inline script, which PSI flags for a
119ms forced reflow, only feeds `.kadence-scrollbar-fixer` — a class added when a drawer
opens, not on load. Re-run PSI desktop a second time before treating 0.143 as real; single
Lighthouse traces are noisy and CLS especially so.

---

## RESOLVED — July 30 2026, via the theme (v1.2.0)

Manual .htaccess editing was declined on the browser side, so the theme now installs the
rules itself: `inc/htaccess.php` uses core's `insert_with_markers()` (the WP Super Cache /
W3TC mechanism), marker-delimited, IfModule-wrapped, admin-only, one-time. It fired on the
first wp-admin load after the v1.2.0 install and Apache now serves:

- images / fonts / video: `public, max-age=31536000, immutable` + 1-year Expires
- CSS / JS: `public, max-age=2592000`

**Verification trap, hit twice:** the nginx proxy cache fronts static files too, and a cached
asset keeps whatever headers it was stored with. Post-install checks read "NONE" because the
entries predated the rules — only a cache-busted request (forced MISS) showed the truth.
Architecture confirmed by requesting a nonexistent theme file: it returns a WordPress-rendered
404, so Apache processes /wp-content/themes/ paths and per-directory .htaccess applies.

After a panel purge, a few pre-rule entries (sourceserif4.woff2, hero-poster.webp,
raindrops-hero.mp4 at their bare URLs) survived; they age out within the cache's 24h refresh.

**Cutover:** nothing to do. The routine travels with the theme and fires on the first
wp-admin visit on production. Confirm with:
`curl -sI https://www.californiafloodinsurance.com/wp-content/themes/cfi-kadence-child/assets/fonts/inter.woff2?cb=1 | grep -i cache-control`

---

## Final PSI results — July 30 2026 (Google-run, staging homepage)

| | Perf | A11y | Best Practices | FCP | LCP | TBT | CLS | SI |
|---|---|---|---|---|---|---|---|---|
| **Desktop** | **99** | 100 | 100 | 0.4s | 0.8s | 0ms | **0** | 0.8s |
| **Mobile** | **89** | 100 | 100 | 1.5s | 3.3s | 0ms | **0** | 4.3s |

(SEO 66 on both = the intentional staging noindex; resolves at launch.)

The desktop CLS fix (font-display:optional, v1.2.1) took CLS 0.143 → 0 and the score
94 → 99. Mobile CLS also 0. Divi baseline for comparison: 58 mobile / 79 desktop,
12.6s mobile LCP.

Mobile 89 vs the earlier 90: Speed Index moved 2.4s → 4.3s under simulated throttling
after the hero preload changed the resource graph — LCP simultaneously improved
3.6s → 3.3s. Lantern-simulated SI swings run to run; treat as variance unless it
repeats consistently, in which case removing the front-page hero preload is the lever.

Declined on purpose: further logo compression (11.7KB at 168×153 is an intentional 2×
retina asset for an 84×76 slot) and CSS minification (2KB against losing the comments
that documented three real bugs).

Last known lever for mobile: the six render-blocking stylesheets (~570ms). Kadence's
per-page / critical CSS option is the designed fix — enable, re-test, before launch.

---

## FINAL — July 30 2026, after v1.2.3 + Kadence CSS Preload

| | Perf | A11y | Best Practices | FCP | LCP | TBT | CLS | SI |
|---|---|---|---|---|---|---|---|---|
| **Desktop** | **100** | 100 | 100 | 0.4s | 0.7s | 0ms | 0 | 0.6s |
| **Mobile** | **90** | 100 | 100 | 1.6s | 3.2s | 0ms | 0 | 4.3s |

Google-run PSI on the staging homepage. SEO 66 on both is the intentional staging
noindex — one failing audit, eight passing — and becomes 100 when the noindex is
removed at launch. Divi baseline: desktop 79, mobile 58, 12.6s mobile LCP.

The delivery chain that got here: nginx page cache (TTFB 70ms) → static asset cache
headers via the theme (1yr immutable) → tokens.css inlined (~6.4KB gz) → Kadence CSS
Preload on (head chain six files → two) → hero poster preloaded → fonts self-hosted,
preloaded, font-display:optional → Cognito embeds reserved at 88vh → Trust Index
lazy-loaded with autoplay off.

CLS is 0 on every audited page type: home, zone/guide, city, article, and all three
Cognito form pages (0.016/0.001/0.002 measured live).

Mobile's remaining gap to 100 is round-trip-bound on simulated slow 4G (document +
global.min.css). Option recorded but not taken: inline the last two Kadence CSS files
for an estimated +2–4 points. Declined as simulator-chasing; every vital is green and
field data is what counts after launch.

---

## Video hub PSI — July 30 2026

`/video/` mobile (Google-run): **95 perf / 100 a11y / 100 BP**, FCP 1.5s, LCP 2.9s,
TBT 0ms, CLS 0 — with nine video thumbnails on the page. The click-to-play facade
architecture holds: zero YouTube player weight until a click; the hub outscores the
homepage (93) on mobile.

`/video/` desktop (Google-run, same day): **100 perf / 100 a11y / 100 BP**, FCP 0.4s,
LCP 0.5s, TBT 0ms, CLS 0. The remaining "render-blocking 350ms" insight is Kadence's
global.min.css (the one stylesheet left blocking by design) and the image-delivery
25 KiB is YouTube's mqdefault JPEGs — neither is actionable from this side.

The "cache lifetimes 70 KiB" insight is i.ytimg.com's own thumbnail headers — YouTube's
servers, not configurable from this side.

Local-Lighthouse footnote: this same page measured 62 perf / 8.7s LCP through this
environment's double proxy, with the trace showing everything loaded by 2.3s. External-
origin pages cannot be measured from here; PSI is the arbiter (third instance of the
instrument failing before the site did: font CLS, min-height harness, this).
