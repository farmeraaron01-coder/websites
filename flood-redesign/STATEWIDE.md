# StatewideFloodInsurance.com — production audit & migration plan

Recon date: July 30 2026. Full crawl of all 108 published URLs (60 pages, 48 posts) in
`statewide-production-seo-audit.csv`. Same method as the CFI audit: served HTML is ground
truth, not database exports.

## What the site is

The sister brand of CaliforniaFloodInsurance.com, running the same cloned Divi stack
(AIOSEO, Redirection, Wordfence, Trustindex, Schema & Structured Data for WP, ea11y,
Limit Login Attempts, Site Kit, Divi). Same phone (855-225-3566), same license
(#0L75450), same YouTube channel, same "The Flood Insurance Experts" h1.

Where CFI's money pages are **city pages**, Statewide's are **state pages** — 30 of them
(Alabama → Washington, 684–1,193 words each) plus a private-flood topic cluster
(`/private-flood-insurance-vs-nfip/` 1,517w, `/nfip-alternatives/`, `/lloyds-of-london-
flood-insurance/`, `/flood-insurance-cost-by-state/`, `/flood-insurance-glossary/`, …).

Page overlap with CFI: only 18 of 60 pages share a slug (the operational set:
`/get-a-quote/`, `/claims/`, `/service-center/`, `/residential/`, `/insights/`, …).
**Post overlap: 47 of 48** — the blog was cloned wholesale.

## Brand facts for the theme swap

| Fact | Value |
|---|---|
| Canonical host | `https://statewidefloodinsurance.com` — **non-www**, opposite of CFI |
| Phone | 855-225-3566 (no CAL-FLOOD vanity — that's California branding) |
| License | CA License #0L75450 (same DBA parent) |
| Logo | Badge crest: Coronado bridge, palms, sunset. Navy `#374464` on white |
| Palette cues | Slate navy `#374464`, indigo `#4054B2`, sunset orange accent |
| Trustindex widget | `1e9552d4458412053506ba969a9` (prod; rich snippet already off) |
| Tagline (site option) | "Nationwide flood insurance insurance broker" — **doubled word, fix** |
| sameAs | facebook.com/FloodInsuranceOnline + same YouTube channel as CFI |
| Sister-note direction | Reverses: Statewide links *to* CFI for California-specific business |

Theme architecture already supports this: swap the constants at the top of
`functions.php` and the palette block in `tokens.css`. `CFI_SISTER_NOTE` flips direction;
`CFI_QUOTE_URL` and canonical host change; everything else is shared.

## Audit findings (vs CFI's)

1. **Zero missing h1s** — the clone is *cleaner* than CFI was (CFI had 19).
2. **43 pages have no meta description at all** (CFI: 19) — the single biggest gap.
   19 more descriptions run over 165 chars. Homepage description is keyword-stuffed:
   "Flood Insurance | Private Flood Insurance | Cheap Flood Insurance Rates".
3. **Homepage title is just "Statewide Flood Insurance"** — 26 chars, no keywords, no
   claim. Unlike CFI there is no proven title here; this one is simply weak.
4. **40 titles over 62 chars** (worst 127) — same legacy ` - suffix` pattern as CFI.
5. **The duplicate-content problem, the biggest finding:** 47/48 posts are word-for-word
   CFI posts. Only 8 carry a cross-domain canonical pointing at CFI; **40 self-canonicalize
   on statewide**, so ~39 duplicate posts compete against CFI in Google. At migration:
   either don't carry the shared posts, or carry them with canonicals to CFI. The state
   pages and private-flood cluster are the unique content worth ranking.
6. Same five near-empty form/video stubs as CFI (`/claims/` 10w, `/video/`, `/agent-
   appointment/`, `/staff-form/`, `/service-center/`) — the Cognito shortcode + video hub
   solution ports directly.
7. `/floodguru/` — 25 words, already noindexed. Decide: drop or keep.
8. `/how-much-does-flood-insurance-cost-2/` is a "-2" duplicate canonicalizing to
   `/which-flood-zone-requires-flood-insurance/` (which looks like a mis-set canonical —
   cost page pointing at a zone page). Verify before migrating.
9. Sitewide 30–50% claim appears on 40 URLs (body copy, not just schema this time —
   distribution differs from CFI's 86/86 schema-driven pattern). Title-tag/copy claims are
   the owner's call per the CFI decision; schema claims stay retired.
10. Thin pages: 32 under 300 words, including `/homeowners-association-flood-insurance/`
    (194w — CFI's HOA page is far deeper; consider porting it), `/media/` (60w),
    `/flood-zone-map/` (117w).

## Migration approach

Same pipeline as CFI, in this order:

1. **Staging environment** — need the statewide staging URL + an application password
   (same InMotion account or separate?).
2. **Theme variant — DONE (v1.3.0), pending review.** One theme now serves both brands:
   `functions.php` detects the statewide domain from `home_url()` and swaps the constants;
   `assets/css/brand-swfi.css` overrides the `:root` palette tokens (appended to the inlined
   CSS only on statewide). No second theme copy to drift. Two things are **drafts for Aaron**:
   - Palette: deep sea-teal (`#0E8E8A` accent / `#092C35` navy / `#35CFC9` CTA), all pairings
     AA-verified. Alternative reading of the badge logo: slate navy `#374464` + sunset-orange
     CTA. Decide on a staging render.
   - Statewide hero copy: "It floods everywhere. / Overpaying is *optional*." with eyebrow
     "Nationwide · Flood-focused · Est. 2012". Reviews heading: "What our clients nationwide
     say." All keyed off `CFI_BRAND` in `front-page.php`.
   Statewide logo assets shipped in the theme (`assets/img/logo-swfi*.png/webp`) for the
   quote landing page bar; the main header logo is set per-site in the Customizer as usual.
3. **Content migration — DONE July 30.** 51 pages migrated, 0 failures, verified clean on
   staging (single h1, no Divi artifacts). Zero posts migrated — all 48 were CFI duplicates
   (including `how-much-does-flood-insurance-cost-2`, a mangled-slug clone). Pipeline:
   `tools-sw-migrate.py`; results in `sw-migration-report.json`. Notable handling:
   - `/faqs/` — production keeps its 35-question FAQ in native `<details>` blocks *after* an
     `<aside>`, which the slicer treats as a hard stop. Converter now keeps details/summary;
     the FAQ section was extracted separately and merged (100w → 3,138w on staging).
   - `/insights/` — migrated content was a dead blog-feed teaser; page is now assigned as
     the posts index (empty until statewide-original articles exist).
   - `/media/` — NOT migrated: pure Divi demo placeholder ("Your Title Goes Here by Artist
     Name" + Elegant Themes demo audio). Needs a redirect decision at launch.
   - `/floodguru/` — NOT migrated (25w, noindexed on production). Redirect decision at launch.
   - 18 pages had no meta description; drafts written from each page's own opening copy
     (`sw-desc-drafts.json`), six hand-written (legal pages, glossary, insights, two
     truncation fixes). **Aaron should skim these.**
   - **Legal pages are CFI's text verbatim** — privacy policy and terms both name
     "California Flood Insurance Services" and the CFI domain throughout, on statewide
     production today. Possibly correct (same operating entity/DBA) but that is an
     owner/attorney call. Left at production parity; flagged.
   - `/contact-us/` carries the Escondido *mailing* address in body copy (production parity,
     fine there) — it must still never enter schema NAP. "Phyiscal" typo fixed.
4. **Plugins/SEO — DONE July 30, verified live.** Rank Math configured (wizard Advanced,
   Insurance Agency, name "Statewide Flood Insurance", shared-GBP NAP: Silverton Ave, +1-855-
   225-3566, Mon–Fri 07:30–17:00, foundingDate 2012-01-01, sameAs Facebook + YouTube + CFI
   domain). Verified in served JSON-LD on home/get-a-quote/texas: the theme filter emits
   areaServed=United States and openingHoursSpecification on the statewide brand; Service
   node on get-a-quote with the Offers/InStock group deleted (again required the hidden-
   delete-button DOM workaround, same Rank Math builder quirk as CFI); BreadcrumbList on
   interior pages; robots noindex untouched. Homepage meta set: "Statewide Flood Insurance:
   NFIP & Private Flood Quotes" + 50-states description (drafts, one-field change).
   Homepage Article node deleted per-page (July 30, verified live twice — wp-admin and a
   cache-busted fetch from here): final homepage graph is Place, InsuranceAgency/Organization,
   WebSite, WebPage. Trust Index live via the shared tuned widget (v1.3.2 installed).
5. **Redirects** — pull from production Redirection when credentials exist.

## Decisions (July 30)

- **Shared posts: statewide stands on its own content.** The 47 duplicated CFI posts do not
  migrate; the two sites cross-link instead (sister-note in the theme, plus editorial links
  where relevant). Statewide's ranking surface is the 30 state pages + private-flood cluster.
- **No separate GBP.** Statewide uses the California Flood Insurance Services profile —
  reviews come through both sites, same company. Rank Math local SEO on statewide therefore
  carries the same NAP as CFI; the Organization node is named Statewide Flood Insurance with
  sameAs linking both domains and the shared GBP surfaces.
- Staging: Aaron is creating it now (URL + application password to follow).

## PSI — July 30 2026 (homepage, Google-run)

| | Mobile | Desktop |
|---|---|---|
| Performance | **100** | **100** |
| FCP / LCP | 0.8s / 1.5s | 0.3s / 0.5s |
| TBT / CLS | 0ms / 0 | 0ms / 0.006 |

Best result of the whole project — statewide's homepage outscores CFI's (93 mobile), mostly
because it has no hero video. Footnotes:

- **SEO showed 91 with "no meta description" and no indexing block — both false.** PSI
  measured a stale nginx-cached copy (`x-proxy-cache: HIT`) predating the day's SEO work;
  the live page (cache-busted) serves both the description and `noindex, nofollow`.
  Root cause: statewide staging had no purge-on-update at all. Nginx Helper is now
  installed+activated via REST, but its purge switch is wp-admin-only —
  Settings → Nginx Helper → "Enable Purge" (see cut-paste in chat). `/purge/` is 403
  (IP-restricted) here exactly as on production.
- **"Font display 240–450ms" insight is the deliberate font-display:optional trade** —
  accepting it is what bought CLS 0 (see tokens.css header comment). Do not "fix".
- **Desktop a11y 95** ("lists contain non-li children") is the Trust Index carousel's own
  markup, third-party. Mobile scores 100 because the widget lazy-loads below the fold and
  the mobile run never renders it. Not actionable from this side.

## Customizer pass — July 30, complete and verified visually

Full runbook in STATEWIDE-CUSTOMIZER.md, executed by Chrome Claude, verified here by
headless-browser screenshot: teal top bar (36px), badge-only logo 56px, nav + Start My
Quote header button, four-column footer + legal row live, Kadence credit gone, guides
section shows the four curated private-flood pages (v1.3.3), canonical URL serves fresh
content post-purge (noindex + meta description both present without cache-busters).

Incidents worth remembering:
- **Customizer sessions clobber REST-created widgets.** Chrome Claude's session, loaded
  before the API created the footer widgets, published its stale widget map and orphaned
  both to Inactive. Fix: move back via REST, then RELOAD the Customizer before its next
  publish. Rule: never run REST widget writes and an open Customizer session in parallel.
- Kadence Free has no row padding control (Pro feature) — bottom row uses default padding;
  visually fine.
- Nginx Helper's "Purge Method" field only appears after saving with Enable Purge checked.

## Content upgrades — July 30

`/residential/` and `/commercial-flood-insurance/` were the two coverage pages thin enough
(317w/375w) to fall below the guide-template threshold: default title band, raw production
copy with literal `\` bullet separators, a wrong vanity number (225-FLOOD), and Divi-era
clipart. Both rewritten (~600w each, structured h2s, takeaways, standfirst, internal links,
proven claims kept: 10–50% lower premiums, 10-day vs 30-day wait, $50M/$10M/$1M limits),
set to template-guide.php explicitly, clipart dropped. Owner decision: no stock
illustrations anywhere — real photography only if supplied; parallax rejected on
performance/CLS grounds.

**NEW: `/excess-flood-insurance/` (page 111)** — Aaron flagged excess flood as a major
under-served topic for coastal states. Net-new ~700w guide (NFIP caps, the self-insurance
gap, who needs it, layer-vs-single-policy, cost drivers), linked from the footer Private
Flood column and the commercial page. First statewide-original content asset; more coastal
topics (storm surge vs wind, Florida-specific excess) are natural follow-ups for /insights/.

## Still open

- Homepage title: no incumbent to protect here — propose
  `Statewide Flood Insurance: NFIP & Private Flood Quotes` or a claim variant if desired.
- Palette + hero copy drafts (above) — review on the staging render.
- `/staff-form/` equivalent exists on statewide production too; same treatment as CFI
  (Cognito quote form on its own URL, noindex) if statewide's office flow needs it.
