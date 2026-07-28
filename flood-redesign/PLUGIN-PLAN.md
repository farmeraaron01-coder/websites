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
| **Rank Math (free)** | **Decision (July 28): switch from AIOSEO.** The AIOSEO Pro license has lapsed, and Rank Math's free tier includes what AIOSEO charges for: redirections, 404 monitor, full schema types (FAQPage, Article, LocalBusiness, Person), multiple focus keywords. | Install on staging → run Rank Math's built-in **AIOSEO importer** (brings titles, descriptions, settings). Do NOT run two SEO plugins at once. URLs are not changing, so no redirect mapping needed. |
| **Trust Index** | The reviews section on the new homepage embeds widget `bcdff9477ef19568e30684fd16d`, set by the `CFI_TRUSTINDEX_ID` constant in `functions.php`. | Done as of child theme v1.0.11. Both sister sites share one Google Business Profile (same parent company), so there is one review pool and no second connection to make. The staging widget is a duplicate; production's is untouched. The theme lazy-loads the script, so it costs nothing until scrolled into view. See TRUSTINDEX-SETUP.md. |
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
- **A second SEO plugin.** Rank Math *or* AIOSEO, never both — duplicate meta and canonical conflicts.
- **A page builder.** Designed pages are coded PHP templates by decision.

## Target final stack (7 active)

Kadence + CFI child theme · Wordfence · Rank Math · Trust Index ·
Nginx Helper · EWWW Image Optimizer · (Site Kit, after launch)

That's a deliberately short list. Plugin count is the single biggest predictor of a slow
WordPress site, and the 98/100 desktop score depends on keeping it short.

## Status — verified July 28 2026

Fingerprinted by requesting plugin directories directly (no auth needed):

| Plugin | State |
|---|---|
| Wordfence | installed ✓ |
| Rank Math (`seo-by-rank-math`) | installed ✓ — **but not configured, see below** |
| EWWW Image Optimizer | installed ✓ |
| Nginx Helper | present ✓ |
| Trust Index (`wp-reviews-plugin-for-google`) | installed — **redundant, see below** |
| Akismet, FormLayer, FormLayer Pro, Hello Dolly | gone ✓ |
| AIOSEO | never on staging ✓ |

### The three new plugins cost nothing

| | Perf | A11y | BP | LCP | CLS | TBT | Requests |
|---|---|---|---|---|---|---|---|
| Mobile | **97** | 100 | 100 | 2.6s | 0 | 10ms | 15 |
| Desktop | **100** | 100 | 100 | 0.6s | 0.001 | 0ms | 16 |

Mobile went 96 → 97 and TBT 100ms → 10ms; request count unchanged. That is the expected
result and confirms the picks: Wordfence is admin-side, Rank Math emits meta tags only, and
EWWW works at upload time. None of them add front-end weight.

Desktop transfer reads 2.1MB against mobile's 359KB — that is the 1.8MB hero video, which
is gated to desktop by design and does not touch LCP (0.6s).

### Rank Math is installed but unconfigured

The homepage emits **no meta description, no OG tags, and no JSON-LD schema**. The setup
wizard has not been run. Consequences:

- Lighthouse SEO sits at 61: `meta-description` missing (real) plus `is-crawlable`
  (intentional — staging noindex, resolves at launch).
- Core WordPress is still emitting the noindex meta itself
  (`<meta name='robots' content='noindex, nofollow' />`, single quotes). Rank Math has not
  taken over robots output yet. Re-check this after running the wizard — an SEO plugin
  assuming control of robots meta is exactly the moment a staging site can become
  indexable by accident.

To do: run the setup wizard, then set the homepage title and description. The title is
currently just site name + tagline. It does **not** carry production's "Save 30–50%" claim,
which is the correct outcome per DECISIONS.md — do not reintroduce it.

### The Trust Index plugin is redundant here

Verified: it enqueues **nothing** on the front end. The only two references to
`cdn.trustindex.io` on the homepage are the theme's own — the `data-src` container and the
IntersectionObserver loader. There is no plugin-injected `trustindex-loader-js-js` script
of the kind production carries.

The widget's configuration lives in Trust Index's dashboard and its content is served from
their CDN, so the plugin adds no capability the theme does not already have. It can be
deleted, taking the target stack to 5 active plugins. Optional, not urgent — it costs
nothing while it sits there inactive on the front end.

## Order of operations on staging

1. Deactivate + delete FormLayer, FormLayer Pro, Hello Dolly, Akismet.
2. Install Trust Index → connect Google profile → verify reviews render on the homepage.
3. Install Rank Math (free) → run the AIOSEO importer → then audit titles/descriptions/canonicals page by page (see SEO findings below).
4. Install Wordfence → basic scan settings, live traffic OFF.
5. Install EWWW → WebP + lazy-load on.
6. Confirm Nginx Helper purge-on-update is enabled.
7. Re-run Lighthouse; confirm mobile hasn't regressed (each plugin costs something —
   if a score drops noticeably, that plugin needs justifying).


## SEO findings from the live site (fix during migration)

Detected while inspecting current output:

1. **City page canonicals are mismatched.** `/san-diego/` sets its canonical to
   `/san-diego-california-flood-insurance-resort-floods/` — a different URL. Google may be
   treating one as a duplicate of the other. Audit every city page: the canonical must
   match the URL that is actually linked and indexed.
2. **City page titles are weaker than zone page titles.** Compare
   "San Diego California Flood Insurance: Your Only Resort During Floods" against
   "Flood Zone AE: What It Means & Insurance Rules | CA". Rewrite city titles in the
   zone-page style: keyword-first, benefit-clear, under ~60 characters.
3. **Homepage title still claims "Save 30–50%"** — conflicts with the qualified-claims
   decision in DECISIONS.md. Rewrite at migration.
4. **Duplicate schema.** The live site runs both AIOSEO and Schema & Structured Data for WP,
   producing 44 `SiteNavigationElement` blocks on the homepage. One schema source only.
