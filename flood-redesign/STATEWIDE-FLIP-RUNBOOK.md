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

### 0a. Confirm tag 56 is actually paused ⚠ BLOCKER

Codex reached the confirmation gate and I approved it, but then moved on to the GA4 work. **Confirm it
published.** In `GTM-PJQ72VK` → Versions, there should be a version **above 14** named for pausing tag 56.

If it did not publish: **stop and do it before flipping.** Unpaused, one submitted quote fires two Ads
conversions with different labels the moment the new theme goes live. Details in
`STATEWIDE-PREFLIP.md` §2.

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

Do it on staging now; it is a database setting and carries through the flip.

### 0d. Read `GTM-PJQ72VK`'s two "Urgent" container-quality issues

`LAUNCH.md` item 7c, never done. I audited the container's *contents* but never read what GTM itself is
complaining about. Read them and tell me what they say before flipping.

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
this file's folder contains `wp-content/themes/cfi-kadence-child/`. Note its `DB_NAME` and keep it
somewhere; you will need it for the READMEs in Phase 3. It must **differ** from the Divi install's
`DB_NAME`.

From here the staging URL stops working. That is expected.

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
`Sitemap: .../sitemap_index.xml`. **Leave Rank Math's robots.txt box empty** — do not paste anything into
it.

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
