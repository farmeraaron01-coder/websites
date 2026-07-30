# Content migration — CFI production → new Kadence build

Source of truth for the move. Built from a full crawl of production with admin REST access,
July 30 2026.

## Inventory

| | Count |
|---|---|
| Published pages | 38 |
| Published posts | 48 |
| **Total URLs to migrate** | **86** |
| `project` post type (Divi Portfolio) | 0 published — nothing to migrate |
| Managed redirects (Redirection plugin) | 6 |

Per-URL title, description, canonical, robots, h1 and word count: `cfi-production-seo-audit.csv`.
Full redirect export: `redirects-production.json` / `.csv`.

## Redirects — all 6, and a defect in three of them

| From | To | Hits |
|---|---|---|
| `/homeowners` | `/residential` | 519 |
| `/commercial/index.html` | `/commercial-flood-insurance/` | 383 |
| `/commercial-owners` | `/commercial-flood-insurance` | 162 |
| `/residenital` (typo) | `/residential` | 1 |
| `/how-much-does-flood-insurance-cost-2/` | `/when-is-flood-insurance-required/` | 0 |
| `/privacy-policy-2/` | `/terms-of-service/` | 0 |

All six targets resolve. **But three targets omit the trailing slash**, so they 301 a second
time: `/homeowners` → `/residential` → `/residential/`. That is a double hop on the single
most-used legacy URL on the site. **Add trailing slashes when recreating these** —
`/homeowners`, `/residenital` and `/commercial-owners` all need it.

Note `/san-diego/` also 301s, to `/san-diego-california-flood-insurance-resort-floods/`, but it
is **not** in the redirect table. That is WordPress core guessing a close match for an unknown
permalink. It works by accident, not by design. It will keep working on the new site as long as
the slug is unchanged, but it should not be relied on.

## Gaps the 404 log exposes

388 logged 404s, 63 distinct URLs; roughly a third is scanner noise. What is left is real
demand for pages that do not exist:

| Requested | Hits | Action |
|---|---|---|
| `/about/`, `/about-us/`, `/about`, `/about-us` | **21 combined** | No About page exists anywhere. `/aaron-farmer/` does (200) and carries the bio. Either build a proper About page or redirect these to it. Given the whole design leans on Aaron for E-E-A-T, building one is the better answer. |
| `/wp-content/themes/farmerflood/FloodApplication.pdf` | 6 | A flood application PDF, now 404. Restore the file or redirect to `/get-a-quote/`. Someone is still linking to it. |
| `/blog/` | 5 | 404, while `/insights/` returns 200 and holds the posts. Straight redirect. |
| `/make-a-payment/`, `/payments/`, `/pay`, `/billing`, `/checkout/` | ~5 combined | Customers looking to pay a premium. `/service-center/` exists but is a **13-word stub**. Real UX gap — decide whether the new site gets a payment path or an explicit "call us to pay" answer. |
| `/author/farmersdev/` + pages 2,3,4,8 | ~11 combined | Old author archive, now 404. Decide whether author archives are enabled on the new site; if not, redirect to `/insights/`. |
| `/2011/`, `/2012/`, `/2012/06/` etc. | ~13 combined | Date archives 404ing. Low value; redirect to `/insights/` or leave. |
| `/team`, `/careers`, `/help`, `/support`, `/contacts`, `/founders`, `/people`, `/our-staff`, `/meet-our-team` | 1 each | Mostly scanners guessing common paths. The clustering around team/about pages reinforces the About page case, but individually not worth redirects. |

### Checked and NOT a problem

`/tel:8552253566` and `/what-does-flood-insurance-not-cover/tel:8552253566` appear in the log,
which would indicate phone links resolving as relative URLs — a conversion bug. **Verified on
four live pages: every one has exactly one correctly-formed `href="tel:"` and no malformed
variant.** These entries are historical or crawler mis-parsing. No action.

## SEO meta migration

No AIOSEO database access is needed. All 86 titles and descriptions were captured from served
HTML — ground truth regardless of where AIOSEO stores them. To write them into Rank Math on
staging, `rank_math_title` and `rank_math_description` need
`register_post_meta( …, 'show_in_rest' => true )` in the child theme so REST can set them.

Fix during the write, do not carry across:

1. ~~Homepage title `California Flood Insurance: Save 30–50% on Flood Quotes` → drop the claim.~~
   **Overruled July 30:** the title has converted for years and stays verbatim (owner's call —
   "this is sales"). Restored on staging (page 7 `rank_math_title`) after a brief run with the
   claim-free variant. The production meta description ("California's flood insurance experts.
   Compare the lowest… instant quote in 2 minutes.", 150 chars) was restored the same day for
   the same reason. Note it remains a title-tag claim only; the JSON-LD version of the claim
   (item 6 below) is still retired.
2. 19 pages with **no `<h1>`**, ten over 1,500 words including every city page. The new interior
   templates enforce a single h1, so this is fixed structurally rather than page by page.
3. 39 titles over 62 characters, mostly legacy posts carrying a ` - California Flood Insurance`
   suffix. Drop the suffix.
4. 19 pages with no meta description; 19 descriptions over 165 characters.
5. 33 pages under 300 words, including five 11–13 word stubs (`/claims/`, `/video/`,
   `/agent-appointment/`, `/staff-form/`, `/service-center/`). Decide per page: write real
   content, merge, or do not migrate. **All five resolved:** `/claims/` (form 31),
   `/service-center/` (form 12), `/agent-appointment/` (form 34) carry their Cognito embeds;
   `/video/` became the video hub. **`/staff-form/` (July 30):** kept — it is the office's
   phone-intake copy of quote form 5, deliberately on its own URL so staff entries never touch
   the Google Ads conversion tracking tied to `/get-a-quote/`. Staging page 71 now embeds
   form 5 and gets `rank_math_robots = noindex,nofollow` (meta registered in theme v1.3.1);
   never link to it from public pages.
6. Do **not** migrate the hardcoded `InsuranceAgency` JSON-LD block. It carries the
   self-serving `aggregateRating` and the "30–50% lower" claim, and Rank Math now owns schema.

## Plugins on production that must not follow

Beyond Divi itself: Elementor (installed alongside Divi), OMGF, Schema & Structured Data for WP,
Pojo/ea11y accessibility widget, Simple History, Limit Login Attempts Reloaded. The new stack is
five plugins and is documented in PLUGIN-PLAN.md.


## Cache purge behaviour — matters for the batch

Discovered while verifying v1.1.1, and it invalidated a verification I had already
run. After installing the new theme and purging, the homepage served the new
stylesheet but **interior pages did not**:

| URL | Cached page referenced | Cache |
|---|---|---|
| `/` | `tokens.css?ver=1.1.1` ✓ | HIT |
| `/flood-zone-ae/` | `tokens.css?ver=1.1.0` ✗ | HIT |
| `/residential/` | `tokens.css?ver=1.1.0` ✗ | HIT |

The same URLs with a cache-buster returned 1.1.1, which is exactly how the trap
works: **a cache-busted fetch proves the file is correct and proves nothing about
what visitors get.** Lighthouse requests the canonical URL, so it was scoring a
page built against the old stylesheet — reporting an accessibility failure that
had already been fixed, and a CLS of 0.052 that did not really exist.

Two things resolve it:

- `https://…/purge/<path>/` returns **403** — that path is IP-restricted, so it
  cannot be triggered remotely.
- **A REST write to the page fires Nginx Helper's purge-on-update and works.**
  Touching pages 46 and 9 flipped both to `ver=1.1.1` with `x-proxy-cache: MISS`
  immediately.

**Consequence for the migration: no manual purging is needed.** Every page the
batch writes purges itself as a side effect of the write. The manual/global purge
is the unreliable path, not the automatic one — which also explains the earlier
"you do not have the necessary privileges" error being more of a nuisance than a
blocker.

Verified after the purge landed:

| Page | a11y | perf | best practices | LCP | CLS |
|---|---|---|---|---|---|
| `/flood-zone-ae/` | **100** | 98 | 100 | 2.1s | **0** |
| `/residential/` | **100** | 99 | 100 | 2.2s | **0** |
