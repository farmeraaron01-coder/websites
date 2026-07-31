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

## Legal pages — 2026-edition documents (July 30)

Both sites now carry attorney-supplied 2026-edition Terms of Service and Privacy Policy,
converted from Aaron's Word documents (Dropbox: CaliforniaFloodInsurance_*_2026.docx /
StatewideFloodInsurance_*_2026.docx) and published to staging with the docx pipeline
(headings/lists preserved, manual TOC dropped in favor of the template's, guide template):

- CFI: terms (page 84, 3,116w/30 sections), privacy (page 3, 2,683w/18 sections)
- Statewide: terms (page 75, 3,098w/30), privacy (page 3, 2,670w/18)

Both name the real operator — **Rebecca Byrom Insurance Agency, Inc. (RBIA), CA License
#0L75450** — dba California Flood Insurance Services / dba Statewide Flood Insurance
respectively. Effective July 30 2026. Contacts: service@californiafloodinsurance.com (CFI)
and agency.services@jumpins.com (statewide). Verified on both sites: single h1, correct
entity, no cross-brand mentions in content, old February effective dates gone.

## ~~LAUNCH-CRITICAL~~ RESOLVED: CFI staging post permalinks (July 30)

CFI staging serves posts at `/2026/07/16/slug/` while production uses `/slug/` — the
Settings → Permalinks structure was never set to "Post name" on CFI staging (statewide's
was, day one). All 48 migrated posts 301 from their production-style URLs today, which is
why every verification passed (curl followed redirects). **FIXED July 30** (Settings → Permalinks → "Post name"). Verified from
here: all 59 published posts return `/slug/` links with zero date-based leftovers, and
spot-checked posts return 200 with no redirect hop — so production URLs, rankings, and
backlinks map 1:1 at cutover. Pages were unaffected throughout.

## Claims content cluster — CFI, July 31

Aaron produced five branded claim documents per brand (checklist one-pager, Before the Flood,
Homeowner's Guide to Flood Readiness, a 10-page Flood Claim Preparation Guide, and Preparing
for Your Flood Adjuster's Visit). Findings before building:

- **CFI and statewide versions are pixel-identical except the logo** (measured: 0.14%–0.77%
  of pixels differ). Publishing both verbatim as web pages would be textbook duplicate
  content, so the pages are forked editorially per brand; the PDFs stay identical.
- **All nine PDFs have NO text layer** — type is flattened to vector outlines (verified with
  two independent PDF engines, zero characters extracted). Consequences: invisible to Google
  and to AI engines, unreadable by screen readers, un-searchable with Ctrl+F. Content had to
  be transcribed from page renders. This is why the pages, not the PDFs, are the SEO asset.
- **Every statewide PDF carries CFI contact details** (`855-CAL-FLOOD` and
  `service@californiafloodinsurance.com`); only logo and URL were localised. Aaron is fixing
  the source files. The disclaimer WAS localised, so the omission was partial.
- **Each brand is missing one document:** no SW version of the 10-page guide, no CFI version
  of the adjuster guide.
- Filename typos fixed on upload: `Guild`→`Guide`, `Vistit`→`Visit`.

Built on CFI staging (pages, `template-guide.php`, standfirst + takeaways + GEO Q&A +
Aaron's disclaimer verbatim on each):
`/flood-claim-guide/` (310, hub, holds the During section inline), `/before-a-flood/` (311),
`/after-a-flood/` (312), `/flood-adjuster-visit/` (313), `/flood-coverage-gaps/` (314).
`/claims/` (68) keeps the Cognito intake form but gained context, next-steps, and links.
Four PDFs uploaded (media 306–309) and offered as downloads. Nav gained a "Claim Help" group;
footer Learn column links the hub.

**Theme v1.3.5** adds `X-Robots-Tag "noindex, noarchive"` for PDFs to the .htaccess block
(option bumped to `v2` so the installer re-runs). Keeps deliverable PDFs out of search so
they never outrank the pages holding the same content, and stops the two brands' identical
PDFs competing.

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
