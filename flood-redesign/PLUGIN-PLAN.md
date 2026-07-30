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
| **Rank Math (free)** | **Decision (July 28): switch from AIOSEO.** The AIOSEO Pro license has lapsed, and Rank Math's free tier includes what AIOSEO charges for: redirections, 404 monitor, full schema types (FAQPage, Article, LocalBusiness, Person), multiple focus keywords. | Installed ✓. Do NOT run two SEO plugins at once. URLs are not changing, so no redirect mapping needed. **The AIOSEO importer cannot run yet — see sequencing note below.** |
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

## Rank Math after the wizard (July 28) — 4 schema defects to fix

Wizard run in Advanced mode. Verified good: exactly one robots meta, still
`noindex, nofollow`, no `X-Robots-Tag`; homepage title 58 chars and description 157 chars,
both live; OG and Twitter tags now present; no savings-claim patterns anywhere on the page;
`meta-description` now passes in Lighthouse, leaving `is-crawlable` (intentional) as the
only SEO failure. Performance unaffected — 97 mobile across two runs, CLS 0, TBT 20–30ms.

The schema graph it now emits is `[LocalBusiness, Organization]`, `WebSite`, `WebPage`,
`Person`, `Article`. Four things are wrong with it:

1. **`Article` on the homepage.** The homepage is not an article. This is Rank Math's
   default schema type for Pages. **See the correction below — do not simply set this to
   None.** WebPage is a Rank Math PRO schema type and is not selectable on the free tier.
2. **`Person` publishing the login handle.** The `Article` node's author resolved to
   `AJFarmer` — a WordPress username — with a Gravatar image and `sameAs` pointing at the
   site root. Fixed the underlying cause: the user's display name is now **Aaron J. Farmer**
   with first/last name and a factual bio set via REST. The `Person` node should disappear
   entirely once `Article` is removed, since it exists only as the article's author.
3. **`openingHours` are wrong.** Rank Math defaulted to
   `Monday–Sunday 09:00-17:00`. The site's own quote page states **Mon–Fri 8am–5pm PT**.
   Publishing seven-day 9–5 hours contradicts the site and misleads visitors.
4. **The LocalBusiness node is thin** — no `telephone`, no `address`, no `priceRange`. Add
   the phone (`+1-855-225-3566`) at minimum. Address only if a physical location should be
   published; do not invent one.

Also worth aligning: Business Type is set to **Local Business**, but Rank Math offers
**Insurance Agency** as a nested subtype — which is what production's hardcoded JSON-LD
already uses. `InsuranceAgency` is a schema.org subtype of `LocalBusiness`, so it inherits
everything and is strictly more specific. Recommend switching.

Minor: Rank Math HTML-escapes inside the JSON-LD script, so the title reads
`NFIP &amp; Private Flood Policies` rather than `&`. Common plugin behaviour, low priority.

### Correction — `Schema Type: None` strips schema from every interior page

Setting **Titles & Meta → Pages → Schema Type = None** fixed the homepage but emptied
everything else. Verified in served HTML, July 28 2026:

| Page | `ld+json` blocks |
|---|---|
| `/` | 1 — `[InsuranceAgency, Organization]`, `WebSite`, `WebPage` |
| `/residential/` | **0** |
| `/commercial/` | **0** |
| `/guides/` | **0** |
| `/hoa-master-flood-policies/` | **0** |
| `/get-a-quote/` | **0** |

No `BreadcrumbList` anywhere on the site either. Rank Math emits its core graph
(`Organization`, `WebSite`, `WebPage`) on the **front page only**; with `None` set, interior
pages get nothing at all — losing the sitewide entity nodes as well as the page type.

**`Article` was never the wrong type — it was wrong on a homepage.** And the author node
was only wrong because the display name was a login handle, which is now fixed. An `Article`
node authored by *Aaron J. Farmer* on a 4,000-word city page or zone guide is precisely the
E-E-A-T signal the design is built around.

Target configuration:

| Scope | Schema type |
|---|---|
| Pages default (Titles & Meta → Pages) | **Article** |
| Homepage — page id 7, slug `home` | **None** (per-page Schema tab override) |
| Quote landing page — page id 8, slug `get-a-quote` | **None** (a conversion LP is not an article) |
| Guides / zone pages / city pages / articles | Article, inherited from the default |

Plus **enable breadcrumbs** so `BreadcrumbList` is emitted — valuable on deep zone and city
pages.

### Why `None` collapsed the graph (root cause, confirmed)

In Rank Math Free the sitewide `Organization`, `WebSite` and `WebPage` nodes on an interior
page are emitted **as part of the content schema's graph, not independently**. Remove the
content schema and the entire graph goes with it. The homepage is the exception — it emits
the sitewide nodes unconditionally, which is why `/` looked healthy while every interior page
was empty.

So the global `None` setting and a per-page `None` override are the same defect at different
scales. A page needs *some* content schema attached to carry the sitewide nodes.

### Verified state, July 28 2026

| Page | Graph |
|---|---|
| `/` | `[InsuranceAgency, Organization]`, `WebSite`, `WebPage` — no BreadcrumbList, correct for the trail root |
| `/residential/` | `[InsuranceAgency, Organization]`, `WebSite`, `BreadcrumbList`, `WebPage`, `Person`, `Article` |
| `/commercial/` | same as above |
| `/guides/` | same as above |
| `/get-a-quote/` | **`BreadcrumbList` only** → set to **Service** (decided; accurate for a quote-request page, restores the core nodes) |

**Breadcrumb schema does not require the theme to render a trail.** Confirmed: `BreadcrumbList`
is present on every interior page with zero `rank-math-breadcrumb` markup in the served HTML.
The `rank_math_the_breadcrumbs()` / `[rank_math_breadcrumb]` calls the settings screen
mentions govern the *visible* trail only. Add them to interior templates only if visitors
should see a trail. Kadence is not a competing source — the only breadcrumb reference in the
output is a dormant CSS rule (`.entry-hero .kadence-breadcrumbs`) with no markup behind it,
consistent with Kadence Pro being inactive. One source, no duplication.

### Verification protocol — a single post-save read of this site is not trustworthy

Hit twice now, from two different caching layers, and it will recur constantly during content
migration:

1. **WordPress/nginx page cache.** Immediately after saving page 8, three consecutive fetches
   of the same URL returned three *different* schema graphs — five nodes with `Service`, then
   four without it, then `Service` absent — despite unique cache-busting query strings and
   `cache: 'reload'`. It settled once the page cache finished writing.
2. **Trust Index CDN.** Saving a widget warns that propagation takes about a minute; a stale
   `content.html` replayed the old autoplay timeout and produced a false CLS reading of
   0.0486 with visible rotation.

**Protocol: never conclude from one read after a write.** Sample the same URL 3–5 times,
confirm the result is stable, and only then record it. For markup checks, normalise the
cache-buster before diffing — otherwise the `cb=` parameter echoes into the page and every
sample looks different for no reason.

### The Trust Index plugin does inject one thing (correction)

Earlier note said it "enqueues nothing on the front end." Precisely: it enqueues no script and
no CSS, but it does emit a `<meta name="ti-site-data">` tag on **every** page — roughly 300
bytes of base64 containing a `_wpnonce` and a `ti-online-users-google=1` URL. Measured: it
fires **zero** requests on pages without the widget, so it is inert rather than costly.

Two notes. A WordPress nonce baked into cached HTML goes stale when the nonce window rotates,
which is untidy though harmless while nothing consumes it. And the tag appears on the quote
landing page, which shows no reviews at all. Neither is a problem today; both add to the case
for deleting the plugin once migration confirms no content depends on its shortcode.

### Refinement for when content lands (not now)

`Article` is right for the zone pages, city pages and guides — the bulk of the site. But
`/residential/`, `/commercial/` and `/hoa-master-flood-policies/` are service pages, not
articles. Override those three to **Service** once their real content exists. Doing it now,
against empty shells, would be churn with nothing to verify against.

### Migration consequence — Rank Math owns schema now

Production's homepage carries a **hardcoded** `InsuranceAgency` JSON-LD block containing the
self-serving `aggregateRating` and the "rates 30–50% lower" claim. Do **not** carry that
block across during migration. Rank Math is now the single schema source, so leaving the
hardcoded block behind disposes of both defects at once and avoids the duplicate-schema
problem that put 44 `SiteNavigationElement` nodes on the live homepage.

### Sequencing correction — the AIOSEO importer can't run on staging yet

The order of operations below says "install Rank Math → run the AIOSEO importer". That step
is not executable as written: **AIOSEO has never been installed on staging**, so there is no
AIOSEO data to import. Its importer reads AIOSEO's `postmeta` rows, which only exist
wherever AIOSEO ran — production.

Two viable paths, and the choice belongs with the content migration:

1. **Import content with its meta, then convert.** Migrate production content via
   WordPress export/import (or a database-level migration) so AIOSEO's `postmeta` rows come
   across, *then* run Rank Math's AIOSEO importer on staging to convert them. Preserves
   titles and descriptions for 100+ pages without retyping them.
2. **Set meta during migration.** Write titles and descriptions as content lands. Total
   control, but a lot of manual work across the zone pages, city pages, and articles.

Recommended: path 1, then selectively rewrite. The import preserves everything, and the
rewrites are then limited to the defects already identified — the `/san-diego/` canonical
homepage "Save 30–50%" title, the 19 missing h1s, and the over-long legacy post titles. Doing it the other
way round means retyping meta that was already fine.

### Rank Math cannot be configured remotely

Its REST namespace is not registered (`/wp-json/rankmath/v1` → 404) and its meta fields
(`rank_math_title`, `rank_math_description`) are not exposed on the pages endpoint. Only
Kadence's `_kad_post_*` meta is. So the setup wizard and per-page SEO fields have to be
done in wp-admin — they cannot be scripted from here.

### Site defaults corrected (July 28)

`default_comment_status` and `default_ping_status` were both `open`. Every existing page
already had comments closed, but the defaults apply to *new* content — so the content
migration would have created dozens of pages with comment forms and pingbacks enabled, on a
site with no comment UI and with Akismet deliberately removed. Both set to `closed` via
REST. Timezone was already `America/Los_Angeles`, closing an earlier open item.

### Wordfence and REST auth — cause not established

Authenticated REST requests returned `rest_not_logged_in` — indistinguishable from
anonymous — immediately after Wordfence was installed, and worked again after Aaron
intervened on the Wordfence side.

**The responsible setting was never identified, and should not be guessed.** A read-only
audit found `Firewall → Brute Force Protection → Additional Options → "Disable WordPress
application passwords"` **unchecked**, which is Wordfence's default and permits app
passwords — so that switch was not the blocker.

Most likely explanation, unconfirmed: a Wordfence **brute-force lockout** on the account or
the requesting IP rather than a configuration setting. A lockout causes Wordfence to reject
the authentication attempt, so WordPress sees no valid user and returns exactly
`rest_not_logged_in`. This is testable — Wordfence → Tools → Live Traffic, filtered to
blocked logins around the time it started, and Wordfence → Blocking for an IP entry.

Other auth-related states, all at defaults and untouched: 2FA Administrator "Optional",
grace period 10 days, remember-device off, `"Disable XML-RPC authentication"` unchecked, and
**`"Require 2FA for XML-RPC call authentication"` = REQUIRED**. That last one governs
XML-RPC only and does not affect `/wp-json/` — but any migration tooling that speaks XML-RPC
instead of REST will fail against it.

### Wordfence launch checklist

- Free license active now; **activate the paid license at cutover**.
- Turn **Live Traffic OFF** — the one Wordfence feature with a real performance cost.
- Change 2FA for Administrator from **Optional** to **Required**. It is currently optional
  with a 10-day grace period; Aaron has enrolled, but future admin accounts would not be
  required to.

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


## SEO findings from the live site — full audit, July 30 2026

**Superseded by a real audit.** The earlier version of this section was written from spot
checks of a few URLs and got two of its four findings wrong. All 86 published URLs have now
been crawled with title, description, canonical, robots, h1 and word count extracted
(`cfi-production-seo-audit.csv`).

### Two earlier findings were WRONG — retracted

1. ~~City page canonicals are mismatched~~ — **false, and the method caused it.** `/san-diego/`
   is a **301 redirect** to `/san-diego-california-flood-insurance-resort-floods/`. Fetching
   the redirecting URL and comparing the pre-redirect address against the post-redirect
   canonical produced a mismatch that does not exist. Across all 86 URLs: **zero canonical
   mismatches**, host form consistent (non-www everywhere), zero missing canonicals.
2. ~~City page titles are weaker than zone page titles~~ — **false.** The actual city landing
   pages are already well optimised, 46–51 characters, keyword-first:
   `San Diego Flood Insurance | Private & NFIP Quotes` (49),
   `Sacramento Flood Insurance | Private & NFIP Quotes` (50). Fully comparable to
   `Flood Zone AE: What It Means & Insurance Rules | CA` (51). The 97-character example
   quoted before — "San Diego California Flood Insurance: Your Only Resort During Floods" — is
   a legacy blog **post**, not a city page. Confusing the two produced the wrong conclusion.

### Confirmed and quantified

3. **Homepage title claims "Save 30–50%".** Confirmed verbatim:
   `California Flood Insurance: Save 30–50% on Flood Quotes` (55 chars). Conflicts with the
   qualified-claims decision in DECISIONS.md. ~~Rewrite at migration.~~ **Resolved July 30:
   kept verbatim by owner decision** — years of conversion data outrank the style rule, and a
   title tag is sales copy, not schema. The claim stays out of JSON-LD (item 8) either way.
4. **19 pages have no `<h1>` at all** — the largest real finding, and 10 of them run over
   1,500 words: every city page (`/sacramento-flood-insurance/` 1,727w,
   `/san-jose-flood-insurance/` 1,700w, `/long-beach-flood-insurance/`,
   `/los-angeles-flood-insurance/`, `/fresno-flood-insurance/`, `/san-diego-flood-insurance/`,
   `/riverside-flood-insurance/`) plus `/flood-zone-ah-and-ao/`, `/flood-zone-ae/` and
   `/how-much-flood-insurance-do-i-need/`. They start at `<h2>`. These are the money pages.
   **The new interior templates must enforce a single h1** — this defect cannot be allowed to
   migrate.
5. **39 titles over 62 characters**, so truncated in results. Overwhelmingly legacy blog posts
   carrying a ` - California Flood Insurance` suffix; worst is 127 chars. Lower priority than
   the h1 problem, and largely fixable by dropping the suffix.
6. **19 pages have no meta description**, and 19 descriptions exceed 165 characters.
7. **33 pages under 300 words**, including five near-empty stubs: `/claims/` (11w),
   `/video/` (11w), `/agent-appointment/` (13w), `/staff-form/` (13w), `/service-center/` (13w).
   Decide per page whether to write real content or not migrate it. Median across the site is
   511 words; max 5,595.
8. **The "30–50%" claim is ONE sitewide element, not 86 pages of copy.** It appears on all 86
   URLs because it lives in the hardcoded `InsuranceAgency` JSON-LD description — the same block
   already marked "do not migrate". Removing that block removes the claim everywhere at once.
   An unqualified 86 would have badly overstated the work.
9. **Zero noindexed pages** on production, and zero missing canonicals. Both clean.

### Production plugin inventory was incomplete

The earlier inventory was built from rendered HTML. The REST namespace list reveals more:
`redirection/v1`, `simple-history/v1`, `llar/v1` (Limit Login Attempts Reloaded),
`elementor-one/v1`, `ea11y/v1` (accessibility widget), `omgf/v1`, `saswp-output`,
`google-site-kit/v1`, `divi/v1`, `wordfence/v1`, `trustindex/v1`, `aioseo/v1`.

**The Redirection plugin is a migration blocker nobody had accounted for.** Whatever 301s it
holds must come across, or previously-fixed URLs start 404ing at cutover. Export its rules
before migration. Also note Elementor is installed alongside Divi.

### AIOSEO meta extraction — solved, and the storage question is moot

No AIOSEO meta is exposed through the REST API (a sample page returns only Divi's
`_et_pb_*` keys and `footnotes`), and AIOSEO's own namespace offers admin/write routes rather
than a bulk read. Rather than resolve where it stores data, the audit sidesteps it: **all 86
titles, descriptions and canonicals have been captured from the served HTML**, which is ground
truth regardless of storage. The migration no longer needs AIOSEO's database, a WXR postmeta
export, or its importer.

To write them into Rank Math on staging, `rank_math_title` / `rank_math_description` need
`register_post_meta( …, show_in_rest => true )` in the child theme so REST can set them —
Rank Math reads its own keys normally either way.

### Content inventory

38 published pages, 48 published posts, 86 total. A `project` post type is registered
(Divi Portfolio) but holds **zero** published items — nothing to migrate there.

---

## Google Business Profile — authoritative NAP data (pulled July 29 2026)

Read from the GBP dashboard. **This is the source of truth for name, address, phone and
hours.** Everything else — site copy, schema, Yelp — must match it.

| Field | GBP value |
|---|---|
| Business name | **California Flood Insurance Services** |
| Primary category | **Insurance agency** (secondary: Insurance broker, Insurance company) |
| Address | **7960 Silverton Ave. #203, San Diego, CA 92126** (Silverton Business Center) |
| Phone | **(855) 225-3566** |
| Hours | **Mon–Fri 7:30 AM–5:00 PM**, Sat/Sun closed |
| Opening date | January 1, 2012 |
| Service area | United States |
| Website | `http://www.californiafloodinsurance.com/` |
| Social | LinkedIn, YouTube, Facebook |
| Short name | CaliforniafloodInsurance |

### Discrepancies this exposes

1. **Hours were wrong everywhere.** GBP opens at **7:30**, not 8:00. The schema was set to
   `08:00-17:00` and the theme said "8am–5pm" in two places. Both theme strings fixed in
   **v1.0.14** (`page-get-a-quote.php`, `front-page.php`); the schema still needs changing to
   `07:30-17:00`. Worth noting the schema value came from the site's own copy — which was
   itself wrong — so verifying against the site was verifying against the wrong source.
2. **Business name differs.** GBP says "California Flood Insurance **Services**"; the WordPress
   site title, the schema `name`, and production's hardcoded JSON-LD all say "California Flood
   Insurance". Name is the most heavily cross-checked NAP field. Fix: set Rank Math's Local SEO
   business name to the GBP string exactly, and leave the WordPress site title alone for
   display and page titles.
3. **Primary category confirms the schema type.** "Insurance agency" — `InsuranceAgency` was
   the right call.
4. **Address confirmed as San Diego.** Escondido (`1835A S. Centre City Parkway #404`) is a
   mailing address only and must **never** appear in schema — a mailbox in LocalBusiness markup
   risks a GBP suspension. The contact page may keep both, labelled as it already is.
5. **`sameAs` is incomplete.** Production's schema lists Facebook, Yelp and YouTube but omits
   **LinkedIn**, which GBP carries. Add it.
6. **GBP's website URL is `http://`, not `https://`.** Every click from Search or Maps eats a
   redirect hop. One-field fix in GBP, worth doing.
7. **Service area says United States, and the GBP description claims "leading nationwide
   provider".** Decide whether the CFI site's schema `areaServed` should say California (matching
   the site's content and brand) or the US. Recommend **California** for this site — Statewide
   is the multi-state brand — and note that `areaServed` is not a field Google cross-checks the
   way it does name/address/phone. Separately, "leading nationwide provider" is the same class of
   unqualified superlative as the "Save 30–50%" claim retired in DECISIONS.md; it is GBP copy
   rather than site copy, but the reasoning applies equally.

### NAP chain verified July 29 2026

GBP, schema and site copy now agree. Confirmed across three stable cache-busted samples:

| Field | Value (identical in GBP and schema) |
|---|---|
| name | California Flood Insurance Services |
| telephone | +1-855-225-3566 |
| openingHours | Monday–Friday 07:30-17:00 |
| address | 7960 Silverton Ave. #203, San Diego, CA 92126, US |
| sameAs | Facebook, LinkedIn, YouTube |

No `aggregateRating`. Zero occurrences of the Escondido mailing address anywhere in the page.
The `Place` node carries only `@id`, `@type` and `address` and is referenced by `location` —
Rank Math's normal output shape, not a duplicate entity.

### Open schema items the free UI cannot express

Rather than fighting the free UI field by field, note that a single `rank_math/json_ld` filter
in the child theme's `functions.php` can add anything the UI cannot. **Deferred deliberately** —
nothing below is urgent, and coupling our PHP to another plugin's graph shape is a maintenance
cost worth paying once, for a batch, rather than four times for singles.

Candidates for that batch, if it ever ships:

- `openingHoursSpecification` objects instead of the free tier's comma-joined string. Google
  parses the string form, so this is a robustness improvement, not a fix.
- `areaServed` — pending the California-vs-nationwide decision.
- `alternateName` on the **Organization** node. The UI's only alternate-name field attaches to
  the `WebSite` node instead, where it currently duplicates `name` exactly and therefore carries
  no signal — **blank that field**.
- `provider` edge on the `/get-a-quote/` `Service` node, batched with the Service overrides for
  `/residential/`, `/commercial/` and `/hoa-master-flood-policies/` when their content lands.

### Two small enrichments worth taking now

- **`foundingDate: 2012-01-01`** via Local SEO → Additional Info. GBP records the opening date
  as January 1 2012 and the site says "since 2012", so it is verifiable rather than decorative.
- **`legalName`** only if the registered entity name genuinely differs from
  "California Flood Insurance Services". Do not duplicate the GBP name into it — `name` already
  holds that, and a `legalName` identical to `name` is noise of the same kind as the WebSite
  `alternateName`.
