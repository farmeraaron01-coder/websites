# Divi → Kadence migration playbook

Written 16 Aug 2026, after the California Flood Insurance migration and the two
days of debugging that followed it. Next target:
**cheapsoberlivinginsurance.com**.

Sources: the CFI cutover (6 Aug 2026) and everything it broke; the
`cheapsoberlivinginsurance.com` SEO audit of 26 June 2026, in Dropbox at
`/Aaron Farmer/Claude CoWork Files/cheapsoberlivinginsurance.com-audit/`.

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

The June audit scored the site **32/100** and listed 4 phases of work. Migrating
to Kadence resolves some of it automatically. Do not re-do those; do not assume
it resolves the rest.

## Solved by moving to Kadence + Rank Math

| June audit finding | Why it goes away |
|---|---|
| Zero schema markup (0/100) | Rank Math generates Organization, Person, Breadcrumb, Article and FAQPage automatically. CFI emits 7 valid schema items with no manual work. |
| Viewport blocks zoom (`maximum-scale=1.0`) | A Divi output. Kadence does not do this. |
| Google Fonts from external CDN | The CFI child theme self-hosts WOFF2 with `<link rel=preload>`. Copy that pattern. |
| AIOSEO generator tag exposed | Different plugin. Check Rank Math's equivalent setting. |
| Divi bloat / TTFB 1.0–1.3s | CFI's Kadence build serves one async script and GTM as the only third party. |

## NOT solved — content migrates with you

| June audit finding | Still true after migration |
|---|---|
| **Title typo: "Operartors"** | Content. Fix it during the rebuild, not after. |
| `/sample-page/` indexed and in the sitemap | Delete it before migrating so it never enters the new sitemap. |
| Blog 2.5 years stale (last post Feb 2024) | Content. The migration is the moment to publish. |
| 9 of 13 images have empty alt text | Media library carries over. Fix during rebuild. |
| No About page, no FAQ page | Both are E-E-A-T requirements for a YMYL-adjacent insurance site. |
| No author bylines with credentials | CFI's byline pattern (name, CA licence #, "last reviewed" date) is worth copying wholesale. |
| No `llms.txt` | Both CFI and Statewide have one. Write it during the build. |

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

Always verify anonymously — incognito, or:
```bash
curl -sSI https://site.com/sitemap.xml | grep -i x-proxy-cache   # want BYPASS
curl -sSL https://site.com/sitemap.xml | grep -c "<loc>"
```

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
