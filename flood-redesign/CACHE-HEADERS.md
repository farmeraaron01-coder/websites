# Static asset cache headers — the largest single PageSpeed win available

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
