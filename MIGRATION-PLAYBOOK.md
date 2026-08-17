# Divi → Kadence migration playbook

Written 16 Aug 2026, after the California Flood Insurance migration and the two
days of debugging that followed it. Updated 17 Aug 2026 after reading the
content package and re-checking the live site. Next target:
**cheapsoberlivinginsurance.com**.

Sources: the CFI cutover (6 Aug 2026) and everything it broke; the
`cheapsoberlivinginsurance.com` SEO audit of 26 June 2026; the Kadence content
package of 8 Aug 2026. All three in Dropbox under
`/Aaron Farmer/Claude CoWork Files/`.

---

# PART 0 — The content package, and what it does not settle

The build spec already exists. It is
`cheapsoberlivinginsurance.com-build/cheapsoberlivinginsurance-kadence-package.zip`
(8 Aug 2026), and it is the newest file in that folder — newer than everything
else in it, including the `site/` prototype. Four things inside:

| File | What it is |
|---|---|
| `KADENCE-BUILD-GUIDE.md` | Global settings: palette, type scale, header/footer, six named Kadence patterns, SEO rules, performance rules |
| `content/PAGE-BLUEPRINTS.md` | Ten pages with final copy, SEO title, meta description, hero image and FAQs |
| `css/kadence-site.css` | 85 lines of finishing CSS, including a `prefers-reduced-motion` block |
| `assets/images/` | Ten images with prescribed alt text |

**The `site/` folder beside it is a Next.js prototype**, deployed at
`sober-living-insurance.farmeraaron01.chatgpt.site`. The build guide is explicit:
it is a visual reference, **do not import it**. Nothing in `site/` ships.

## The package is good. These are the gaps it leaves.

Six things the blueprints do not resolve. All of them are cheaper to settle now
than after the pages are built.

### 1. www vs non-www — the package contradicts the live site

The build guide specifies canonicals and `InsuranceAgency` schema on
`https://www.cheapsoberlivinginsurance.com/`. **The live site is the opposite**:
verified 17 Aug, `www` returns a 301 to the apex, and the homepage canonical is
`https://cheapsoberlivinginsurance.com/`. Pick one and make canonical, schema,
`robots.txt`, the sitemap and WordPress siteurl/home all agree. Changing to www
means redirecting every existing URL a second time — apex is the cheaper choice
and the one already earning links.

### 2. `/quote/` is already taken by a redirect

The blueprint puts the quote page at `/quote/`. Live, **`/quote/` already 301s to
`/quote-now/`**. Build the new page and that redirect either shadows it or loops.
Delete the old rule and reverse it: `/quote-now/` → `/quote/`.

### 3. The homepage and `/sober-living-home-insurance/` compete with each other

Homepage H1: *"Insurance built for the business of sober living."*
`/sober-living-home-insurance/` H1: *"Insurance built for the business of sober
living"* — the same sentence minus the full stop. The SEO titles are near-twins
too (`Sober Living Home Insurance | Property & Business Coverage` against
`Sober Living Home Insurance | Specialized Business Coverage`).

Two pages, one query. Give one of them a distinct angle before building, or fold
the coverage page into the homepage. This is the same cannibalization problem we
worked to avoid between the California and Statewide sites — cheaper to fix in a
draft than in a live index.

### 4. The three existing blog posts have nowhere to go

Live and indexed today:

- `/coping-with-challenges-in-sober-living-operations-top-ten-concerns-and-solutions/`
- `/essential-checklist-to-safeguard-your-sober-living-home-from-liability-claims/`
- `/why-professional-liability-insurance-is-crucial-for-operators-of-sober-living-homes/`

The blueprint's `/resources/` page lists six resource cards but never says
whether a card links to one of these posts or to something new. Two cards
overlap the existing posts almost exactly — "When professional liability becomes
important" and "Reducing everyday liability exposures". **Decide per card:
link to the existing post, or rewrite and 301 the old URL to the new one.**
Building both leaves duplicates.

Note also that `/category/resources/` is live and indexed, and the new page is
`/resources/`. Noindex the archive (Part 7 says so anyway) so they don't compete.

### 5. Images are heavy and the OG image is enormous

`og.png` is **1.89 MB**; `recovery-residence-exterior.jpg` is 543 KB,
`communal-kitchen.jpg` 359 KB, `operator-planning.jpg` 297 KB. The build guide
already says convert to WebP — do it at upload, not later, and get `og.png`
under 300 KB. Preserve the prescribed alt text; it is written and it is good.

### 6. Facts the blueprint deliberately leaves blank

`PAGE-BLUEPRINTS.md` ends by saying the agency's complete legal name, physical
address, states served, licences and social profiles must be added before launch
and **"do not invent these fields."** That instruction is correct and it is
still outstanding. Same for the contact block: the quote page lists
`858-295-7242` and `aaron.farmer@jumpins.com` — a jumpins address on a
cheapsoberliving site. Fine if intended, but it is a decision, not a default.

---

# PART 1 — The trap that cost two days, and how to not repeat it

## The CFI cutover created a folder named after the wrong site

On 6 Aug the live domain's document root was pointed at the **staging** folder.
The folders were never renamed. The result:

| Folder | What it actually was |
|---|---|
| `/home/mrtaco5/new.californiafloodinsurance.com/` | **LIVE PRODUCTION** |
| `/home/mrtaco5/californiafloodinsurance.com/` | the dead old Divi site |

The directory named after the live domain was the dead one. Softaculous listed
both installs with the **same Website URL**, so only the Website Path could tell
them apart. WP Toolkit listed only one and labelled it "Staging" — which was
production. This cost roughly two days and nearly caused a wrong deletion.

## ⚠️ cheapsoberlivinginsurance.com is set up to repeat this exactly

`staging.cheapsoberlivinginsurance.com` already exists, with docroot
`/home/mrtaco5/staging.cheapsoberlivinginsurance.com`. If you cut over by
repointing the live domain at that folder — which is what happened to CFI — you
recreate the identical trap.

**Do it the other way round.** Two options, both fine, both better than what
happened to CFI:

**Option A (recommended).** Build in staging. When ready:
1. Rename the old live folder to `ZZ-OLD-divi-cheapsoberlivinginsurance-<date>`
2. Move/copy the staging build into the real docroot
   `/home/mrtaco5/cheapsoberlivinginsurance.com/`
3. Leave the domain's document root **unchanged**
4. Update WordPress siteurl/home to the live domain
5. Delete the staging subdomain once verified

**Option B.** Repoint the docroot as CFI did — but then **immediately** rename
folders so names match reality, before anything else. If you take this path,
write the marker file (below) the same hour.

Either way, the invariant is: **when you finish, no folder is named after a
site it does not contain.**

## Write a marker file, in the docroot, on cutover day

CFI has one and it is the single thing that resolved the confusion fastest.
Put this at the docroot root as `READ-ME-WHICH-SITE-IS-THIS.txt`:

```
THIS IS THE LIVE PRODUCTION SITE for cheapsoberlivinginsurance.com.
Cut over <date>. Docroot confirmed in cPanel → Domains.
DB_NAME: <db>
Theme: <child theme>
The folder named "<other folder>" is the OLD Divi site, kept only as rollback
until <date + 30 days>. Do not confuse them.
```

Verify from outside afterwards: fetch it over the public domain. If it returns
200 at the expected byte size, that folder is definitively the served docroot.
That byte-match test is what finally settled CFI.

---

# PART 2 — Pre-migration checklist

Run every item **before** touching the live site.

## Record the before-state (you will need it to prove nothing broke)

```bash
# baseline — save the output
curl -s -o before.html -w "%{http_code} %{size_download}\n" https://cheapsoberlivinginsurance.com/
curl -sSL https://cheapsoberlivinginsurance.com/sitemap.xml | grep -c "<loc>"
curl -sSI https://cheapsoberlivinginsurance.com/ | grep -iE "x-proxy-cache|server"
```

Capture: every indexed URL from the sitemap, the homepage byte size, the current
title/meta on every page, and a full crawl of internal links. **The URL list is
the important one** — every live URL must either survive or 301.

## Confirm the backup actually exists, in Dropbox

Backups are **not** on the server. UpdraftPlus uploads to Dropbox and deletes
local copies, so `wp-content/updraft/` holding only logs is normal, not a
missing backup. Look in `/Aaron Farmer/Apps/UpdraftPlus.Com/`.

**Run a fresh backup on cutover day and confirm it lands.** CFI's most recent
backup at the time of the migration work was three days stale while every other
site on the account had run within 24 hours.

## Check the plugin and platform inventory

The June audit found: **Divi + AIOSEO 4.7.9**, caching disabled, zero schema.
CFI's target state is **Kadence + child theme + Rank Math**. Decide before you
start whether AIOSEO is being replaced by Rank Math — if so, plan the metadata
migration, because titles and descriptions do **not** transfer automatically.

---

# PART 3 — What the migration fixes for free, and what it does not

The June audit scored the site **32/100**. **Roughly half of that audit is now
out of date** — the site was partly remediated between June and August, and
AIOSEO went 4.7.9 → 4.9.10. Everything below was re-verified against the live
site on **17 Aug 2026**. Do not plan from the June PDF alone.

## Already fixed on the live Divi site — nothing to carry forward

| June audit finding | Verified state, 17 Aug 2026 |
|---|---|
| Title typo "Operartors" | **Gone.** Title is now `Sober Living Home Insurance California \| Cheap Sober Living Insurance` |
| `/sample-page/` indexed | **Gone.** Returns 404 and is out of the sitemap |
| Viewport blocks zoom | **Fixed.** `width=device-width, initial-scale=1.0`, no `maximum-scale` |
| Zero schema markup (0/100) | **No longer zero.** AIOSEO emits 6 types: BreadcrumbList, Organization, WebPage, WebSite, FAQPage, InsuranceAgency/LocalBusiness |
| Caching disabled, TTFB 1.0–1.3s | nginx page cache now returns `x-proxy-cache: HIT`; TTFB 0.49–0.89s |
| No `llms.txt` | **Exists**, 1,683 bytes — but see the defect below |

Two defects surfaced while checking the above, both worth carrying into the new
build rather than inheriting:

- The `Organization` schema `name` reads **"Cheap Sober Living Insurance for
  your"** — truncated mid-sentence. Set it deliberately in the new build.
- `/llms.txt` has every line after the first indented with tabs, so a markdown
  reader treats the whole file as one preformatted code block. Rewrite it flush
  left.

## Solved by moving to Kadence

| Finding | Why it goes away |
|---|---|
| Divi bloat — 280 KB homepage, 5,865 `et_pb_` occurrences | CFI's Kadence build serves one async script and GTM as the only third party |
| Google Fonts from external CDN | The CFI child theme self-hosts WOFF2 with `<link rel=preload>`. Copy that pattern |
| AIOSEO generator tag exposed | Different plugin, if you switch to Rank Math. Check its equivalent setting |

## NOT solved — still true today, and content migrates with you

| Finding | Verified state, 17 Aug 2026 |
|---|---|
| **Three `<h1>` on the homepage** | "Sober Living Home Insurance", "Reach Us", "Want a Quote? start here". The blueprint gives one H1 per page — build to it |
| **9 of 13 images have empty alt text** | Unchanged since June. The package ships prescribed alt text for all ten new images; use it |
| **Blog stale since Feb 2024** | `post-sitemap.xml` lastmod is still 2024-02-20. The migration is the moment to publish |
| **No About page** | `/about/` 404s. The blueprint has one written and ready |
| No author bylines with credentials | CFI's byline pattern (name, CA licence #, "last reviewed" date) is worth copying wholesale |

---

# PART 3b — The redirect map

Small site, so this is the whole of it. Every live URL, and where it goes.

| Live URL | Disposition |
|---|---|
| `/` | Stays. New homepage |
| `/quote-now/` | **301 → `/quote/`**, and delete the existing `/quote/` → `/quote-now/` rule first |
| `/coping-with-challenges-in-sober-living-operations…/` | Keep or 301 into a Resources article — decide, don't leave it orphaned |
| `/essential-checklist-to-safeguard-your-sober-living-home…/` | Overlaps Resources card 6. Keep or 301 |
| `/why-professional-liability-insurance-is-crucial…/` | Overlaps Resources card 3. Keep or 301 |
| `/category/resources/` | Noindex. Do not let it compete with the new `/resources/` page |
| `/tag/halfway-house-insurance/`, `/tag/sober-insurance/`, `/tag/sober-living-insurance/` | Noindex |
| `/llms.txt`, `/robots.txt` | Rewrite for the new structure |

New URLs with no predecessor — all ten are net-new except `/` and the quote
page: `/sober-living-home-insurance/`, `/commercial-property-business-income/`,
`/general-liability/`, `/professional-liability/`, `/workers-compensation/`,
`/who-we-insure/`, `/resources/`, `/about/`.

`/quote/` is currently a redirect, so it needs the extra step in the table
above. Nothing else in the new set collides with a live URL.

---

# PART 4 — The two caching layers, and why purge will not save you

Both bit CFI hard. Both apply to every site on the `mrtaco5` account.

## 1. The host's nginx page cache

- **Purging does not work on this account.** Nginx Helper's "Purge Entire Cache"
  returns a privileges error; cPanel → Cache Manager's single-URL purge and
  "Purge Full Cache" both complete silently with no effect. Verified repeatedly
  on 16 Aug 2026.
- **Design around it.** Anything that must be fresh goes in the **Bypass URL**
  list, not behind a purge:
  ```
  .*sitemap.*
  /robots.txt
  /llms.txt
  ```
- Apply those to the **apex domain**, and to every subdomain variant too, so a
  wrong pick from the dropdown is harmless.
- **A new bypass rule takes several minutes to apply.** It saves and persists
  the whole time. Wait and re-check before concluding it failed.
- HTML pages self-heal on the Default Refresh Time (4 hours on CFI).

## 2. Rank Math's internal sitemap cache

Rank Math can serve a frozen sitemap with nothing misconfigured — no exclusions,
no noindex, posts published and live. CFI lost three posts to this for over a
week.

- "Remove transients" does **not** clear it.
- The fix: **Sitemap Settings → General → change Links Per Sitemap 200 → 199 →
  Save, then 199 → 200 → Save.** A save with nothing changed may be a no-op.

## Verification rule, non-negotiable

**Logged-in requests bypass the cache.** Checking a sitemap or a page while
logged into wp-admin shows you what WordPress thinks, not what Googlebot
receives. CFI looked fine to an admin for days while Google was served a
frozen copy.

Always verify anonymously — incognito, or curl.

**And anonymous alone is still not enough.** `x-proxy-cache: MISS` does not
prove the response came from the origin. On 17 Aug 2026 a plain anonymous curl
of two pages returned pre-edit content while reporting `MISS`, and the origin
already had the edits — a confident, wrong "not applied" verdict that cost a
round trip. Append a unique query string so the request gets a fresh cache key:

```bash
CB="?cb=$(date +%s%N)"
curl -sSI "https://site.com/sitemap.xml$CB" | grep -i x-proxy-cache   # want BYPASS
curl -sSL "https://site.com/page/$CB" | grep -c "<loc>"

# stale-cache check: differing sizes mean the plain URL is lying to you
curl -sS -o /dev/null -w "plain %{size_download}\n" "https://site.com/page/"
curl -sS -o /dev/null -w "bust  %{size_download}\n" "https://site.com/page/$CB"
```

A query-string URL rules out the **nginx** layer only — both URLs still execute
PHP, so this tells you what WordPress generates, not what a plugin cached.

---

# PART 5 — Post-cutover verification

Run all of this **anonymously**, within an hour of going live.

| Check | Pass condition |
|---|---|
| Homepage | 200, byte size sane vs baseline |
| Every URL from the pre-migration list | 200 or a 301 to its new home — zero 404s |
| `<h1>` count on key pages | exactly 1 |
| Sitemap URL count | matches published post + page count |
| Sitemap header | `x-proxy-cache: BYPASS` |
| `robots.txt` | correct, and declares the sitemap |
| Canonical on 3 sample pages | self-referencing, correct host |
| Rich Results Test | schema detected, no critical errors |
| Marker file over HTTP | 200 at expected byte size |

Then: Search Console → submit the sitemap → URL Inspection → Request Indexing on
the homepage and the top 5 pages.

---

# PART 6 — Content editing gotchas (learned the hard way)

## WordPress transforms content between storage and render

A find-and-replace string copied from the **rendered page** will often match
zero times in the editor. This cost two failed attempts on CFI.

- **`wptexturize`** converts straight apostrophes, quotes, em-dashes and
  ellipses to HTML entities on render. `NFIP's` is stored plain, served as
  `NFIP&#8217;s`. **Never put an apostrophe, quote, dash or ellipsis in a FIND
  string.**
- **`wpautop`** normalizes whitespace between tags, so multi-line blocks
  (tables, lists) rarely match verbatim. **Prefer single-line finds.**

Anchor on plain words. Put entities only on the REPLACE side.

## Read the target page's structure before drafting anything

Made this mistake twice in one day. New pages get standalone drafts. Existing
pages get a **section replacement anchored on a heading already present**, or a
clearly framed addition — never an unlabelled swap.

## Other traps

- **The post title and the SEO title are separate fields.** Changing the Rank
  Math snippet leaves the visible `<h1>` and breadcrumb untouched. CFI shipped
  a page whose H1 and body disagreed on the year.
- **cPanel's file editor defaults to `euc-jp` encoding.** Set it to UTF-8 before
  editing `llms.txt` or anything with non-ASCII, or it corrupts on save.
- **Rank Math Free paywalls custom schema.** Do not plan on adding a Dataset or
  custom JSON-LD block through it.
- **Author schema may point at a noindexed archive.** Rank Math uses the WP
  user's author archive for `Person.url`. Set the user's Website field to the
  real About page instead.

---

# PART 7 — Build it right the first time

Things CFI now has that were retrofitted painfully. Build them in from day one.

- **Author byline block** — name, credential (licence #), "Last reviewed" date,
  headshot **with alt text**, linked to a real About page.
- **`llms.txt`** at the docroot, sectioned, listing every substantive page.
- **Self-hosted fonts** with `<link rel=preload>`, not a CDN.
- **Security headers** — `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Permissions-Policy`. CFI has all four.
- **Tables with `<caption>` and `scope`** on every data table. This is what lets
  a screen reader and an AI extractor bind a number to its row.
- **Archives handled** — category, author and search results `noindex`; date
  archives redirected. CFI gets all of this right and it keeps the index clean.
- **At least one external citation per substantive page.** CFI had 5,748 words
  of YMYL content across three pages with zero outbound links. Primary sources
  are an E-E-A-T signal and their absence is conspicuous.

---

# PART 8 — Do not repeat these process mistakes

Honest list from this engagement.

1. **I called a finding "critical" that wasn't blocking.** The missing sitemap
   entry was real, but internal links had already got all three posts indexed.
   Check whether a problem is actually causing harm before ranking it.
2. **Documentation went stale mid-engagement and misdirected an agent.** An
   apply agent proposed re-clearing a cache that had been fixed the day before,
   because the README still said it was broken. Update findings the moment they
   resolve.
3. **A backup was assumed rather than verified.** The Divi rollback existed, but
   nobody had confirmed where. Verify before the deletion, not after.
4. **Two find-and-replace blocks were written from rendered HTML.** See Part 6.
5. **Content was drafted before reading the target page.** Twice.

The common thread: **verify the current state before acting on a belief about
it.** Every one of these was cheap to check and expensive to get wrong.
