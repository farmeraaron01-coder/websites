# Statewide flip — the runbook for today

8 Aug 2026. Decisions taken: **cross-domain geo redirects**, **Option A folder handling** (flip, verify,
then rename in the same session). Read `FLIP-LOG-CALIFORNIA.md` for the mechanics that are identical;
this is the ordered list to work through.

**Two things are already done.** The GA4 baseline is captured (below) and the redirect file is validated.

---

## The GA4 baseline — recorded before the flip, do not lose this

GA4 `G-FH3Q6GKNHH`, **31 July – 6 Aug 2026**, the last seven complete days:

| Metric | Count |
|---|---|
| Pageviews | **6,887** |
| Sessions | **2,731** |
| Total users | **2,352** |
| `page_view` events | **6,887** |

**One homepage load produces 2 `page_view` events** — verified live in Realtime (10 → 12).

**The cause is not Site Kit.** Site Kit is not connected; the stream (ID `3558222836`) reports 0
connected site tags. The real cause, confirmed in the served HTML: statewide production carries **a
hardcoded `gtag/js` snippet for `G-FH3Q6GKNHH` in the Divi header** *and* the container's Google tag
configures the same ID. Two configurations, two hits. `LAUNCH.md:309` named Site Kit and was wrong.

**So expect pageviews to roughly halve — about 6,887/week down to ~3,400 — with no real traffic loss.**
The new theme prints no hardcoded gtag (`CFI_GA4_ID` is deliberately empty; the container supplies GA4),
verified: 0 occurrences of `gtag/js` and 0 of `G-FH3Q6GKNHH` in staging's HTML.

**Judge this migration on Search Console impressions, Ads conversions and phone calls. Not GA4 sessions
across the cutover line.**

---

## PHASE 0 — before touching the docroot

### 0a. Tag 56 paused — ✅ DONE 8 Aug, verified at the wire

Version 14 (`Remove wrong California Google tag from Statewide`) had it unpaused. **Version 15**,
`Pause tag 56 - duplicate Ads conversion on quote submit`, contains exactly one change.

**Verified from the published `gtm.js`, not from the UI** — the count method, which is what makes this
provable:

| | v14 | v15 |
|---|---|---|
| `I0VbCLiCgoQYENeo0OID` occurrences | 2 (tags 46 + 56) | **1** (tag 46 only, click-triggered, correctly left alone) |
| `COU0CK2O12cQ16jQ4gM` occurrences | 2 | **2** (tags 45 + 57 both live) |
| `__awct` tags | 4 | **3** |

`GTM-MZ6RZ94` does not appear anywhere in this container.

**Tag 56's exception was `BLOCK - staging hostnames`** — the blocking trigger conditioned on
`e eq gtm.js`. That can only block tags firing on container load; it could never have stopped a tag
firing on `cfi_form_submit`. It was false comfort, and pausing was the only real fix. Rollback if ever
needed: Versions → 14 → Publish.

### 0a-bis. The two "Urgent" container-quality issues — read, and deliberately NOT applied

`LAUNCH.md` item 7c, finally answered.

**1. "Missing Google tags" → `Google Tag AW-1012143191`, suggested *Added*.** Correct on the facts:
`AW-1012143191` appears in the container **only** inside `productSettings` as a `preAutoPii` flag, never
as a Google tag destination. The single configured destination is `G-FH3Q6GKNHH`. Conversions still
record through the legacy `__awct` path — that action booked 344.50 in 30 days.

**Not applied, and this is the reason: California's container is identical.** Only a `__googtag` for
`G-3YMN51H7LE`, with `AW-1012143191` again confined to `productSettings`. **Both brands fire into the same
Ads conversion ID, 1012143191.** So this is systemic, not statewide-specific, and adding the Google tag is
a measurement change across both brands on an account spending ~$24,771/mo. Doing it alongside the flip
and the pending tag 27 / `quote_form_lead` work would make any change in conversion volume
unattributable. **It belongs after that work, in its own change window.** Filed in `OPEN-ITEMS.md` Tier 3.

**2. "Additional domains detected for configuration" → `Conversion Linker`, suggested *Modified*.** Tag 16
has `enableCrossDomain: false`, `enableUrlPassthrough: false`, `enableCookieOverrides: false` — no domains
configured at all. The extra hostname is almost certainly `staging.statewidefloodinsurance.com`, which
**ceases to exist after Phase 3**. **Recheck in a week; it may clear itself.**

On the 7 cross-domain redirects and this tag: Apache's `Redirect` preserves the query string, so a
`?gclid=` survives the hop, and both sites report to the same Ads conversion ID — so Ads attribution is
not broken by the domain change. GA4 sees a new session on the other property. Those are seven dead blog
posts. The decision stands.

### 0b. Noindex the category archives — statewide has 6 that California doesn't

Statewide's sitemap has **three** children (post, page, **category**); California's has two. Six thin
archive pages would enter the index competing with their own posts.

Rank Math → Titles & Meta → Categories → turn on **Category Archives Robots Meta**, then check
**No Index**. Rank Math drops them from the sitemap automatically.

The six: `hurricanes-storm-surge`, `excess-flood`, `lenders-closings`, `flood-basics`, `nfip-pricing`,
`claims`.

**DONE 8 Aug — but it needed a second step, and this is the part that generalises.** After the setting
saved, the setting was live in PHP while the *public* URLs still served the old XML:

| URL | bare | with `?cb=` |
|---|---|---|
| `sitemap_index.xml` | 3 children, still listing `category-sitemap.xml` | 2 children |
| `category-sitemap.xml` | 200 with all 6 URLs | 404 |

**This is not the nginx page cache.** Both responses came back `x-proxy-cache: MISS` with
`cache-control: no-cache`, and there are no cache-plugin fingerprints. It is **Rank Math's own sitemap
cache**, which is bypassed when a query string is present. Cleared via Rank Math → Status & Tools →
**Database Tools → Delete Sitemap Cache**.

Two lessons, both already paid for once on California's robots.txt:

1. **A Rank Math setting being correct in the admin does not mean the served file changed.** Sitemaps and
   robots.txt are generated output with their own caches in front of them.
2. **Verify logged out, with no query string.** A logged-in browser and a `?cb=` fetch both bypass the
   cache, so both show the correct answer while crawlers get the stale one. That is the same mistake that
   made the 1.5.4 font 404s invisible for half an hour.

California was checked for the same condition and is clean — bare and cache-busted agree on its index and
its 42-URL page sitemap.

### 0c. Set the site icon

Staging renders **zero** icon tags, so statewide would inherit California's `/favicon.ico` 404 and the
Best Practices ding. Appearance → Customize → Site Identity → Site Icon, upload the 512×512 PNG, then
**Publish** — California's failed the first time because Publish was not clicked.

**Not a flip blocker.** It is a database setting and carries through, so it can be done at any point
during Phase 2. Do it before Phase 4 or the Lighthouse Best Practices score will show the ding.

### 0d. Read `GTM-PJQ72VK`'s two "Urgent" container-quality issues — ✅ DONE, see §0a-bis

---

## Phase 0 status — CLEAR TO FLIP

| | | |
|---|---|---|
| 0a tag 56 paused | ✅ done, verified in the published container | was the only real blocker |
| 0b category noindex | ✅ setting saved; **cache purge folded into Phase 2 step 7** | not a blocker — every sitemap URL changes hostname at the flip anyway, so it has to be purged after |
| 0c site icon | ⏳ needs a 512×512 PNG from Aaron | not a blocker; do it during Phase 2 |
| 0d Urgent issues | ✅ read, neither applied, both justified above | no action |

---

## PHASE 1 — the flip

### 1. wp-config on the NEW install

Edit `/home/mrtaco5/staging.statewidefloodinsurance.com/wp-config.php`, immediately above
`/* That's all, stop editing! */`:

```php
define( 'WP_HOME',    'https://statewidefloodinsurance.com' );
define( 'WP_SITEURL', 'https://statewidefloodinsurance.com' );
```

**Positive check before editing** — California's near-miss was editing the wrong `wp-config.php`. Confirm
this file's folder contains `wp-content/themes/cfi-kadence-child/` and **no `Divi` folder**. Note its
`DB_NAME` and keep it somewhere; you will need it for the READMEs in Phase 3. It must **differ** from the
Divi install's `DB_NAME`.

Verified 8 Aug: themes folder holds `cfi-kadence-child`, `kadence`, and three twenty-* defaults, no Divi.
**`DB_NAME` is `mrtaco5_wp_rbanj`**, table prefix `8DjxVi_`.

From here the staging URL stops working. That is expected — but **not uniformly, and the difference will
confuse you if you do not expect it.** Measured immediately after the edit, 8 Aug:

| Request | Result |
|---|---|
| `staging.../` bare | **200**, `x-proxy-cache: HIT` — nginx serving a page cached *before* the edit, still full of staging URLs |
| `staging.../?cb=…` | **301 → `https://statewidefloodinsurance.com/`**, `x-proxy-cache: MISS` |
| `staging.../wp-admin/` | **302 → `https://statewidefloodinsurance.com/wp-login.php?redirect_to=…`** |

**Already-cached staging pages keep serving stale 200s until they expire.** Staging appearing to still work
is not evidence the edit failed. I checked the bare URL first and briefly doubted a correct edit because of
it — the third time in this project that testing the cached path produced a wrong conclusion. The
uncached path is the only one that tells you anything.

That last row is the back-to-back rule proven at the wire, not assumed: staging's admin now bounces to the
apex login, which until step 2 is the **Divi** site's login.

### ⚠ Do steps 1 and 2 back to back. Do no admin work between them.

Between the wp-config edit and the docroot repoint, `staging.statewidefloodinsurance.com` redirects to the
apex — which is **still the Divi docroot**, including `/wp-admin`. So in that window, navigating to
"staging" lands you in the **live Divi admin**. That is California's two-installs-one-URL confusion
reappearing for a few minutes. Have the Domains tab already open before editing wp-config.

**Rollback never depends on browser access to the site**, which is what makes this safe: `wp-config.php`
is edited through cPanel File Manager, so removing the two lines is always available no matter what any
hostname resolves to.

**If you want a backup of `wp-config.php`, do NOT name it `wp-config.php.bak` in the docroot.** PHP does
not execute `.bak`, so `https://statewidefloodinsurance.com/wp-config.php.bak` would be served as
**plaintext** — DB password and every auth salt. Scanners probe that exact path. Put backups above all
docroots instead: `/home/mrtaco5/wp-config-statewide-preflip-2026-08-08.php`.

### What the wp-config edit does and does not do

It changes `home_url()` / `site_url()`. **It does not switch tagging on.** The gate is
`inc/tags.php:46-50`, and it reads the request's `Host` header, not any config value:

```php
$host = strtolower( (string) ( $_SERVER['HTTP_HOST'] ?? '' ) );
$host = preg_replace( '/^www\./', '', $host );
$host = preg_replace( '/:\d+$/', '', $host );
return $host === CFI_PROD_HOST;
```

So tags begin printing at **step 2**, when requests start arriving with `Host: statewidefloodinsurance.com`.
The admin banner's phrase "once the site answers on `statewidefloodinsurance.com`" means the hostname on
the wire — it is easy to misread as the config value, and one agent did.

`CFI_BRAND` *is* derived from `home_url()`, but `staging.statewidefloodinsurance.com` already contains the
`statewidefloodinsurance` substring, so brand and container are already `swfi` / `GTM-PJQ72VK` and do not
change. The gate strips `www.`, so `www.` fires tags too.

**⚠ From step 2 onward, do not test-submit the quote form on the apex.** Tags are live; tag 57 fires a real
Ads conversion. Use GTM Preview instead.

### 2. Repoint the document root

cPanel → Domains → `statewidefloodinsurance.com` → Manage → Document Root.

Set it to `staging.statewidefloodinsurance.com` — **home-relative, no leading slash.** The field shows a
`🏠/` prefix already. There is a red **Remove Domain** button below Update; do not touch it.

### 3. Verify it answers

```
curl -sI https://statewidefloodinsurance.com/ | head -1
curl -s https://statewidefloodinsurance.com/ | grep -c "cfi-kadence-child"
```

Expect `200` and a non-zero count. **Tell me at this point and I will run the full verification sweep.**

---

## PHASE 2 — immediately after, in this order

### 4. Remove the staging noindex

Rank Math → Titles & Meta, or Settings → Reading. Verify:

```
curl -s https://statewidefloodinsurance.com/ | grep -i "noindex"
```

Expect **nothing**. This is the single most damaging thing to forget.

### 5. Install the redirects

`statewide-prune-redirects.conf` → paste into `.htaccess` in the docroot, **above** `# BEGIN WordPress`.
50 rules: **38 × 301** (31 same-domain, of which one is a topic page pointed at `/get-a-quote/`, plus
**7 cross-domain to californiafloodinsurance.com**) and **12 × 410**.

Paste the whole file including its comments — the `# SUPERSEDED` lines are inert and record the
same-domain option that was not chosen. Do not uncomment them.

Validated today: all 50 sources 404 on the new site, no collisions, no duplicates, every 301 target
returns 200.

### 6. Purge the cache — then verify robots.txt

**robots.txt is a cached page.** On California it served the Divi site's crawl directives for four hours
because nobody thought to check it.

```
curl -s https://statewidefloodinsurance.com/robots.txt
```

Expect `Disallow: /wp-content/uploads/*.pdf` present, **no** `sitemap.rss`, and
`Sitemap: https://statewidefloodinsurance.com/sitemap_index.xml` on the **apex** hostname. **Leave Rank
Math's robots.txt box empty** — do not paste anything into it.

Both versions were captured 8 Aug so the diff is unambiguous. Staging currently serves:

```
Disallow: /wp-admin/
Disallow: /wp-content/uploads/*.pdf
Allow: /wp-admin/admin-ajax.php
Sitemap: https://staging.statewidefloodinsurance.com/sitemap_index.xml
```

Live Divi currently serves `sitemap.xml` **and** `sitemap.rss` and no PDF rule. **Neither has
`Disallow: /`**, which was worth confirming — a blanket disallow would have stopped Google ever seeing the
noindex removal. The `staging.` sitemap line is the stale-cache tell: if you still see it here after the
purge, robots.txt has not regenerated.

### 7. Re-clear the sitemap cache, verify it logged out, THEN submit to Search Console

**Clear Rank Math's sitemap cache again after the flip**, not just before it. Every URL inside the
sitemap changes hostname at the flip (`staging.` disappears), so whatever Rank Math cached on staging is
wrong the moment the docroot moves. Rank Math → Status & Tools → Database Tools → **Delete Sitemap Cache**.

Then verify **logged out and with no query string** — see §0b for why anything else proves nothing:

```
curl -s https://statewidefloodinsurance.com/sitemap_index.xml | grep -o '<loc>[^<]*</loc>'
curl -sI https://statewidefloodinsurance.com/category-sitemap.xml | head -1
```

Expect exactly `post-sitemap.xml` and `page-sitemap.xml` on the **apex** hostname, and 404 on the
category sitemap. **Any `staging.` URL inside the sitemap means the cache is still stale — do not submit
it to Google in that state.**

Only then submit. Domain property, **full URL** — `sc-domain:` properties reject relative paths:
`https://statewidefloodinsurance.com/sitemap_index.xml`

"Discovered pages: 0" alongside "Success" is normal async lag.

---

## PHASE 3 — the rename, SAME SESSION. Do not defer this.

Deferring is what left California with two installs reporting one URL and a Login button that opens
production. Have both cPanel tabs open before starting; downtime is the gap between 8 and 9.

8. Rename `statewidefloodinsurance.com/` → **`archive-divi-statewide-2026/`**  *(site down)*
9. Rename `staging.statewidefloodinsurance.com/` → **`statewidefloodinsurance.com/`**
10. Document Root → `statewidefloodinsurance.com`  *(site back up, correct name)*
11. Verify again with the Phase 1 step 3 commands.
12. **Write the two READMEs** while the knowledge is in your head — one in each folder, naming which
    install it is and quoting its `DB_NAME`. Copy California's and change the names. Add the line that
    California's lacked: *the hosting manager's Login button on the other row opens THIS site.*

    Both values are already confirmed, so no lookup is needed:

    | Folder after Phase 3 | Install | `DB_NAME` |
    |---|---|---|
    | `statewidefloodinsurance.com/` | **new** Kadence child, live | `mrtaco5_wp_rbanj` (prefix `8DjxVi_`) |
    | `archive-divi-statewide-2026/` | old Divi, archived | `mrtaco5_wp_zpezw` |

    Separate databases, as required. For reference, California's Divi archive is a third database again,
    `mrtaco5_wp_2b1xy` (prefix `F01Hh8gh_`) — so no two installs share one.
13. Delete the `staging.` subdomain. cPanel will now allow it — its folder is gone.

**Rollback at any point:** set the Document Root to `archive-divi-statewide-2026`.

---

## PHASE 4 — verification, mine

Tell me when Phase 3 is done and I will run, against the live apex:

- every sitemap URL for status, canonical, noindex, schema, meta description
- all 50 redirects, checking 301 vs 410 individually
- `www.` → apex, `http://` → apex, and the `staging.` hostname
- stray staging hostnames in rendered HTML
- Lighthouse on the apex, 5 runs, all four categories

Forecast, so nothing is misread: **~66–70 mobile, ~88 desktop.** Statewide carries the same ~535 KiB tag
load as California, so it lands where California landed. Any lower and something is wrong; any higher is
a bonus, not the expectation.

---

## Deliberately NOT part of today

- **The cross-site contamination fix.** California's container runs on Jump Trucking's site with tag 27
  unscoped. Blocked on importing `quote_form_lead`, which is blocked on GA4 propagation. Independent of
  this flip — statewide's container is not shared.
- **Deleting tags 45 and 46.** After the flip, confirm in GTM Preview that they no longer fire, *then*
  remove them. Not before.
- **The `.env` secrets work.** Unrelated and higher priority than anything here, but not today's task.

## What can go wrong, in order of likelihood

1. **Forgetting the noindex removal.** Costs the most, hardest to notice. Step 4.
2. **robots.txt still cached.** Google gets the old crawl rules. Step 6.
3. **The sitemap still cached with `staging.` hostnames**, then submitted to Search Console in that
   state. Step 7. This one already happened once today at §0b, in a different cache layer.
4. **Tag 56 unpaused.** Doubles reported Ads conversions from the first lead. Step 0a.
5. **cPanel refusing a folder rename** because it is an active document root. If Phase 3 step 8 is
   blocked, the site is briefly down: recreate the folder name, repoint, and fall back to deferring the
   rename — then tell me.

---

## Noted, not a blocker

Statewide runs the **same child theme folder** as California, so its `style.css` header still reads
"California Flood Insurance (Kadence Child)" in Appearance → Themes. Admin-only — verified that no
"California Flood Insurance" string reaches statewide's public HTML. Cosmetic; fix whenever the theme is
next touched, not today.
