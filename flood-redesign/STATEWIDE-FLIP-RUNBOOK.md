# Statewide flip — the runbook for today

7 Aug 2026. Decisions taken: **cross-domain geo redirects**, **Option A folder handling** (flip, verify,
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

### 0a. Tag 56 paused — ✅ DONE 7 Aug, verified at the wire

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

**DONE 7 Aug — but it needed a second step, and this is the part that generalises.** After the setting
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

Verified 7 Aug: themes folder holds `cfi-kadence-child`, `kadence`, and three twenty-* defaults, no Divi.
**`DB_NAME` is `mrtaco5_wp_rbanj`**, table prefix `8DjxVi_`.

From here the staging URL stops working. That is expected — but **not uniformly, and the difference will
confuse you if you do not expect it.** Measured immediately after the edit, 7 Aug:

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

**That filename is misdated and the file on disk carries it** — the flip was **7 Aug 2026**, not the 8th.
I stamped "8 Aug" across every document and commit message during this session and dictated that filename
too; an agent checking its own backup against the system clock caught it. Every date in this folder has
been corrected to 7 Aug, but the filename above is left as-is because it is what actually exists on the
server. The `.htaccess` backup, named by that agent from the system clock rather than from my prose, is
correctly `.htaccess.pre-prune-2026-08-07.bak`.

**Prefer the machine's clock to a date carried forward in prose.** Mine was wrong for a whole session and
nothing internal to the documents could reveal it.

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

### ⚠ 3b. FIRST: the database still holds staging URLs. Fix before purging, before noindex.

**Found 7 Aug immediately after the docroot moved.** The flip itself was clean — cache-busted apex showed
12 `cfi-kadence-child` refs, **0** Divi markers, `GTM-PJQ72VK` present, `GTM-MZ6RZ94` absent, **0**
hardcoded `gtag/js` and **0** inline `G-FH3Q6GKNHH` (confirming the duplicate `page_view` died with Divi),
noindex still on. But:

**Every page carried 37–44 `staging.statewidefloodinsurance.com` URLs.**

```
/                              37      /claims/                39
/residential/                  38      /faqs/                  38
/commercial-flood-insurance/   38      /insights/              44
/contact-us/                   37      /get-a-quote/            1
```

Two sources, neither fixed by `WP_HOME`:

1. **The nav is `menu-item-type-custom`** — Custom Links storing absolute URLs verbatim in the database.
   Nothing rewrites those.
2. **Rank Math schema** — `Organization.url`, and the logo's `url` and `contentUrl`.

**This is a Phase 3 blocker, not a cosmetic one.** Step 13 deletes the `staging.` subdomain; at that
moment every nav link on every page stops resolving. Before then they merely bounce through a redirect.

Also: **`og:site_name` and the schema logo caption still read `Statewide Flood Insurance - Staging`.** Any
social share would carry the word Staging.

**This is NOT Settings → General, and I sent Aaron to the wrong screen first.** The apex login page renders
`<title>Log In ‹ Statewide Flood Insurance — WordPress</title>`, which is built from `blogname` — so
`blogname` is already correct and editing it would have been the wrong fix. The string is **Rank Math's own
Website Name field** (Titles & Meta → Global Meta), which falls back to `blogname` only when empty. Both
bad strings trace to that one field, which is what makes a single source the right conclusion.

The general form of the mistake: two settings can render the same-looking string, so **find a surface that
renders only one of them** before deciding which to edit. The login page renders `blogname` and nothing
else, which is what settled it.

**The nginx cache was the only thing hiding this** — the bare apex still served Divi on three consecutive
requests with `x-proxy-cache: HIT`, so no visitor saw the broken nav. Had the cache been purged first, it
would have gone public. **This is why the fix goes before the purge.**

**All of it is doable from cPanel → Terminal with no WordPress login**, which matters because Aaron could
not recall the staging password and **this domain cannot reliably deliver a reset email** — checked 7 Aug:
TXT holds only the Google verification, so there is **no SPF**, there is **no DMARC**, and MX points at the
host itself. `OPEN-ITEMS.md` item 30 confirmed as live, not theoretical.

WP-CLI runs as the system user and does not authenticate through WordPress, so it sidesteps the login
entirely. The admin username is **`AJFarmer`** (California production is `farmeraaron` — a different
account). Application passwords do **not** work for browser login; they only authenticate REST and XML-RPC.

```
cd /home/mrtaco5/staging.statewidefloodinsurance.com
wp --info                                                   # confirm WP-CLI exists
wp user list --role=administrator --fields=ID,user_login,user_email
wp user update AJFarmer --prompt=user_pass                  # --prompt keeps it out of shell history
```

**A.** The Website Name field, no login needed. **The option name uses HYPHENS, not underscores** — I got
this wrong first and `wp option patch` errored with `No data exists for key "website_name"`, which reads
like a missing key but was a missing *option*. Found with
`wp db query "SELECT option_name FROM 8DjxVi_options WHERE option_value LIKE '%Staging%'"`:

```
wp option pluck rank-math-options-titles website_name
wp option patch update rank-math-options-titles website_name 'Statewide Flood Insurance'
```

`pluck` first, always — a `patch` against a guessed name either errors or writes a key nothing reads.

**B.** The URLs. **Name the three tables explicitly. Do NOT use `--all-tables-with-prefix` here:**

```
wp db export ~/statewide-preflip-db.sql
wp search-replace 'staging.statewidefloodinsurance.com' 'statewidefloodinsurance.com' 8DjxVi_options 8DjxVi_postmeta 8DjxVi_posts --skip-columns=guid --report-changed-only
```

Searching for the bare hostname rather than `https://staging…` is deliberate — it is shorter to paste into
cPanel's terminal and it also catches `http://` and protocol-relative `//` forms.

**Why not `--all-tables-with-prefix`, which is what I first told Aaron to run.** The dry run reported
**12,867** replacements. Only **43** were URLs:

| Table | Column | Count | What it is |
|---|---|---|---|
| `wfknownfilelist` | `path` | **6,408** | **filesystem paths** |
| `wffilemods` | `real_path` | **6,407** | **filesystem paths** |
| `options` | `option_value` | 7 | real URLs (incl. all Rank Math settings) |
| `postmeta` | `meta_value` | 18 | real URLs — the nav's `_menu_item_url` |
| `posts` | `post_content` | 18 | real URLs |
| `users` | `user_email` / `user_url` | 1 / 1 | an email address, and a profile field |
| `wfhits`, `wfnotifications` | | 7 | Wordfence log noise |

**12,815 of them were Wordfence rows holding paths on disk**, like
`/home/mrtaco5/staging.statewidefloodinsurance.com/wp-content/…`. The directory is still *named*
`staging.statewidefloodinsurance.com` until Phase 3, so rewriting those would have pointed Wordfence's
file-integrity baseline at a nonexistent directory and made it report all ~6,400 files as changed or
missing. Wordfence rebuilds both tables on its next scan regardless, so there was nothing to gain either.

**`users` is excluded from the table list on purpose** — one account's **email address** contains the
staging hostname, and a hostname search-replace is the wrong instrument for an email address. Check it with
`wp user list --fields=ID,user_login,user_email` and set it deliberately in the UI.

**But `user_url` in that same table must be fixed**, and excluding the whole table missed it. It is the
author profile's Website field, and it renders as the byline link (`<a class="url fn n" href="…">`, once
per post — so `/insights/` showed 7) and as `Person.sameAs` in the schema. Scope by **column**, so the
email address stays structurally unreachable:

```
wp search-replace 'staging.statewidefloodinsurance.com' 'statewidefloodinsurance.com' 8DjxVi_users --include-columns=user_url --report-changed-only
```

Result after the 43-replacement run: homepage **0** staging references, nav and schema `Organization.url`
and logo `contentUrl` all correct, and exactly **1 residual per page** — this row.

**The lesson, and it is the general one:** a search-replace scoped by *table set* replaces a string
everywhere it appears, but the same string can mean different things in different columns — a URL in
`postmeta`, a **path** in `wffilemods`, an **identity** in `user_email`. `--all-tables-with-prefix` is
convenient and, for a hostname that is also a directory name, actively dangerous. **Read the
`--report-changed-only` dry run and scope to named tables.** `--report-changed-only` is what made this
legible: the full dry run buried the two 6,400-row tables in pages of zero-hit output.

Also: **take the `wp db export` first, to `~/` and never inside the docroot** — a dump under the web root is
a downloadable copy of the whole database. Restore is `wp db import ~/statewide-preflip-db.sql`.

**Never do this with phpMyAdmin SQL.** Menus, widgets and theme options are stored as **PHP-serialized
arrays**, which embed the byte length of every string. Dropping `staging.` shortens the string by 8
characters, so a raw `REPLACE()` leaves every length prefix wrong and silently corrupts those rows.
`wp search-replace` unserializes, replaces, and re-serializes. Fallback if WP-CLI is missing: the Better
Search Replace plugin, removed afterwards.

Keep the two `wp-config.php` defines. Redundant once the database agrees, but a useful guard.

**C.** Rank Math → Status & Tools → Database Tools → Delete Sitemap Cache. **D.** Purge the host cache.
**Then re-verify before touching the noindex.**

**The general lesson:** `WP_HOME`/`WP_SITEURL` change what WordPress *generates*. They do nothing to
absolute URLs already *stored* — custom menu links, content, plugin options, schema. Any hostname change
needs a search-replace as well as a config change, and the check for it is a count of the old hostname in
the rendered HTML of several pages, not just the homepage.

### 4. Remove the staging noindex — then PURGE AGAIN before verifying

Rank Math → Titles & Meta, or Settings → Reading. **Then purge the host cache a second time.** Cached
copies keep serving the old `noindex` header, so verifying before the purge shows failure where there is
none — and, worse, verifying with `?cb=` shows success while crawlers still get `noindex`.

```
curl -s https://statewidefloodinsurance.com/ | grep -i "noindex"
```

Expect **nothing**, on the **bare** URL. This is the single most damaging thing to forget.

Verified state before removal, 7 Aug: `noindex` present on **70/70** sitemap URLs, all returning 200, with
**0** staging hostnames anywhere and `www`/`http://`/`staging.` all 301ing to the apex.

**The noindex was NOT in Rank Math.** Its Global Meta screen had Index checked and No Index unchecked the
whole time. It was WordPress core's `blog_public` option — Settings → Reading, "Discourage search engines".
The tell is `nofollow` in the served string: Rank Math's own No Follow box was unchecked, so something
outside Rank Math was adding it. `wp option get blog_public` returned `0`; `wp option update blog_public 1`
fixed it. **Check `blog_public` before touching Rank Math's settings.**

### ⚠ The false alarm that followed, and the method change it forced

Measured right after the change, the sweep read **46/70 indexable, 24/70 still noindex** — including
`/get-a-quote/` and all seven state landing pages. I reported that as pages being excluded from Google and
proposed clearing per-post `rank_math_robots` meta in bulk.

**All of it was wrong.** The query showed only **one** post carries that key — `staff-form`, set to
`noindex,nofollow`, which is correct and should stay. **The bulk `DELETE` I proposed would have removed a
legitimate protection on the staff intake form while fixing nothing.** The 24 were stale cache entries
written before `blog_public` changed. Re-measured cache-busted: **70/70 indexable, 70/70 canonical, 0
noindex.** Bare at the same moment still read 46/24 — the identical split, which is what proves it was the
cache.

A second error inside the same investigation: I claimed California deliberately noindexes
`/flood-insurance-glossary/`. It **404s** on California, and I had read its 404 page's robots tag.
**Check the status code before comparing robots meta across sites.**

**The method fix, because this was the fifth cache-induced wrong conclusion in one day** (font 404s,
category sitemap, post-wp-config redirect, robots.txt, this):

> For **correctness** questions — is the setting right? — read **cache-busted**.
> For **"what does the public get"** — read **bare**.
> Never mix them in one table, and always say which one is being reported.

Both deliberate noindexes verified intact afterwards: the 6 category archives at `follow, noindex`, and
`staff-form` at `nofollow, noindex` **and absent from the sitemap**.

### 5. Install the redirects

### ⚠⚠ THE LIVE DOCROOT IS THE `staging.`-NAMED FOLDER. Write there, nowhere else.

```
/home/mrtaco5/staging.statewidefloodinsurance.com/.htaccess      ← LIVE. Write here.
/home/mrtaco5/statewidefloodinsurance.com/.htaccess              ← DORMANT old Divi copy.
```

Phase 1 step 2 pointed the apex **at the staging directory**; it did not move files into the directory
named after the domain. Until Phase 3 renames them, the folder named for the domain serves nothing and the
folder named `staging.` serves everything. **Confirm with cPanel → Domains → Document Root before writing,
not after.**

**This bit on 7 Aug.** An agent staged the block perfectly, wrote 15,441 bytes to the
`statewidefloodinsurance.com/` directory, verified the write byte-for-byte — and the live site was
unaffected, because that file is not served. It only surfaced because the agent spot-checked four
*redirects* afterwards rather than trusting that a successful write meant a working change. **I approved
that path having written this very step saying otherwise.**

Two tells that identify the right file without checking cPanel: the live one contains the theme's
`# BEGIN CFI static asset cache` block, and the dormant one contains Divi-era `# BEGIN WpFastestCache`.

`statewide-prune-redirects.conf` → paste into `.htaccess` in the docroot, **above** `# BEGIN WordPress`.
50 rules: **38 × 301** (31 same-domain, of which one is a topic page pointed at `/get-a-quote/`, plus
**7 cross-domain to californiafloodinsurance.com**) and **12 × 410**.

Paste the whole file including its comments — the `# SUPERSEDED` lines are inert and record the
same-domain option that was not chosen. Do not uncomment them.

Validated today: all 50 sources 404 on the new site, no collisions, no duplicates, every 301 target
returns 200.

### ⚠ There are TWO purges on this host, and only one of them works for a site-wide change

**This cost an hour on 7 Aug.** After removing the noindex, three separate purges left the *same 24* pages
serving `noindex` on bare URLs while cache-busted requests were correct. Headers showed why:

```
/get-a-quote/ bare   x-proxy-cache: HIT   nofollow, noindex   ← stale entry
/get-a-quote/?cb=    x-proxy-cache: MISS  follow, index       ← correct
/residential/ bare   x-proxy-cache: HIT   follow, index       ← entry written after the change
```

Both HITs. One stale. So the entries were surviving the purge, not being rewritten.

| Purge | Where | Scope |
|---|---|---|
| **Purge Cache** | WordPress admin bar | **Per-URL**, triggered on post save. Explains why `/residential/` was fresh — it had been edited — and 24 untouched pages were not. |
| **Purge Full Cache** | **cPanel → Cache Manager** (InMotion plugin) | **The nginx layer, all domains in the cPanel.** This is the one that works. |

The nginx flush fixed all 24 **and** robots.txt in one action — which also proves robots.txt was never a
separate problem, just the same cache layer.

**A site-wide setting change needs the cPanel-level flush.** The WordPress button cannot clear entries for
pages it has no reason to think changed. And note the client cannot force it: nginx here ignores
`Cache-Control: no-cache` from the requester, so this is only fixable server-side.

**The Purge Full Cache button is account-wide.** On this cPanel that is 14 entries including
`californiafloodinsurance.com` — live production. Harmless, but first hits rebuild slowly, so do not run a
PageSpeed test on California right after using it or the TTFB will read artificially badly.

### 6. Purge the cache — then verify robots.txt

**robots.txt is a cached page.** On California it served the Divi site's crawl directives for four hours
because nobody thought to check it.

```
curl -s https://statewidefloodinsurance.com/robots.txt
```

Expect `Disallow: /wp-content/uploads/*.pdf` present, **no** `sitemap.rss`, and
`Sitemap: https://statewidefloodinsurance.com/sitemap_index.xml` on the **apex** hostname. **Leave Rank
Math's robots.txt box empty** — do not paste anything into it.

Both versions were captured 7 Aug so the diff is unambiguous. Staging currently serves:

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

**What actually happened, 7 Aug.** After the host cache purge, every page came good — bare homepage on the
Kadence child, 0 Divi markers, 0 staging refs — but **robots.txt kept serving Divi's version and flapped**:

| Request | Content |
|---|---|
| `robots.txt` bare | Divi's old one |
| `robots.txt?cb=…` | correct |
| via the `staging.` 301 | correct |

Origin was right; a stale cache entry survived the purge. **I first called this urgent and that was wrong.**
Reading the stale content settles it: there is **no `Disallow: /`** — only two dead `Sitemap:` lines and a
missing PDF rule. **Nothing is blocked from crawling**, and Google takes the sitemap from the Search Console
submission anyway. Fix it, but it gates nothing.

The general point: **"the wrong file is being served" is a severity question, not just a correctness one.**
Read what the wrong version actually says before deciding what it costs. A stale robots.txt with
`Disallow: /` is an emergency; this one was an untidiness.

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

### ⚠⚠ THE `staging.`-NAMED FOLDER IS THE LIVE SITE. Order is not optional.

`/home/mrtaco5/staging.statewidefloodinsurance.com/` currently holds **the live production site**. Until
step 9 renames it:

- **Do NOT delete the `staging.` subdomain** — step 13 comes after step 9 for exactly this reason. cPanel
  normally leaves files when removing a domain, but any prompt offering to remove the document root, or
  any cleanup that treats a folder named "staging" as disposable, **takes statewide down and destroys the
  install.** The database survives; the files do not.
- **Do NOT let anything else "clean up staging."**

Between steps 9 and 10 the apex's document root points at a folder that no longer exists, so the site is
down. That is the expected gap, and step 10 closes it.

8. Rename `statewidefloodinsurance.com/` → **`archive-divi-statewide-2026/`**  *(site stays up — this
   folder serves nothing)*
9. Rename `staging.statewidefloodinsurance.com/` → **`statewidefloodinsurance.com/`**  *(site down)*
10. Document Root → `statewidefloodinsurance.com`  *(site back up, correct name)*

**8a. Empty the archive's `.htaccess` of prune rules before or right after renaming it.** On 7 Aug the
50 rules were written into that dormant file by mistake. Leaving them there is not harmless: **the
documented rollback for this whole flip is to point the Document Root at
`archive-divi-statewide-2026`**, and on the old Divi site all 50 source URLs are live — so a rollback
would 301 away 38 real pages and 410 twelve more. The rollback would look like it worked and be quietly
broken. Restore that file from its `.htaccess.pre-prune-2026-08-07.bak`.
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
- **a count of `staging.statewidefloodinsurance.com` in every page's rendered HTML — must be 0 everywhere.**
  Checking only the homepage is what would have let the `user_url` residual through; the homepage hit 0
  while every inner page still had 1.

**⚠ The canonical tag is a hard gate.** Before the noindex came off, statewide emitted **no**
`<link rel="canonical">` at all, while California — identical theme and Rank Math install — emitted
`<link rel="canonical" href="https://californiafloodinsurance.com/" />`. The difference is the robots meta:
California is `follow, index`, statewide was `nofollow, noindex`, and **Rank Math suppresses the canonical
on noindexed pages**. `og:url` and the schema `@id` were already correct on the apex, which is consistent.

So the canonical is *expected* to appear once the noindex is removed. **If it does not, that is a real
defect and the sitemap must not be submitted until it is fixed.** Do not read its earlier absence as a
problem, and do not read its absence *after* the noindex removal as normal.
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
3. **Staging URLs left in the database** — nav, schema, `og:site_name`. **This one actually happened.**
   Step 3b. Fatal at Phase 3 step 13 when the subdomain is deleted, because every nav link stops
   resolving. The nginx cache is what hid it.
4. **The sitemap still cached with `staging.` hostnames**, then submitted to Search Console in that
   state. Step 7. This one already happened once today at §0b, in a different cache layer.
5. **Tag 56 unpaused.** Doubles reported Ads conversions from the first lead. Step 0a. *(Closed.)*
6. **cPanel refusing a folder rename** because it is an active document root. If Phase 3 step 8 is
   blocked, the site is briefly down: recreate the folder name, repoint, and fall back to deferring the
   rename — then tell me.

---

## Noted, not a blocker

Statewide runs the **same child theme folder** as California, so its `style.css` header still reads
"California Flood Insurance (Kadence Child)" in Appearance → Themes. Admin-only — verified that no
"California Flood Insurance" string reaches statewide's public HTML. Cosmetic; fix whenever the theme is
next touched, not today.

---

## PHASE 2 — VERIFIED COMPLETE, 7 Aug 2026

Measured on **bare** URLs after the final cPanel → Cache Manager → Purge Full Cache, so this is what
crawlers get, not what a cache-buster shows:

| Check | Result |
|---|---|
| Sitemap URLs returning 200 | **70 / 70** |
| noindex leaks | **0** |
| Missing canonical | **0** |
| `staging.` hostname references | **0** |
| robots.txt | PDF rule present, `sitemap_index.xml`, no `sitemap.rss` |
| Sitemap index children | 2, both on the apex |
| 6 category archives | `follow, noindex` — deliberate, intact |
| `staff-form` | `nofollow, noindex`, absent from the sitemap |

**Redirects: 50 / 50**, verified by parsing the rules out of `statewide-prune-redirects.conf` rather than
from anyone's summary of it, with redirect-following disabled:

- 37 × `Redirect 301` — **status *and* exact `Location` header** matched. Checking status alone would let a
  302, or a 301 to the wrong target, pass.
- 12 × `Redirect 410` — 410, not 404.
- Rule 50, the anchored `RedirectMatch`: `/media` and `/media/` → 301 to `/video/`; `/media/test.pdf` and
  `/media/2013/photo.jpg` **404 rather than being rewritten**; `/media-kit/` also unaffected, so the anchor
  does not over-match a sibling slug.
- All 19 distinct targets return 200, including the cross-domain
  `californiafloodinsurance.com/get-a-quote/`.
- Controls unchanged: `/`, `/faqs/`, `/get-a-quote/`, `/insights/`, `/resources/` all 200; `/blog/` 404;
  `/wp-content/uploads/` 403; no 500s.

**Remaining in Phase 2:** submit `https://statewidefloodinsurance.com/sitemap_index.xml` in Search Console.
The gate for that — canonicals present, noindex gone, no staging hostnames in the sitemap — has passed.

### Still open, neither blocking nor ranking-relevant

- `og:site_name` and the schema logo caption still read `Statewide Flood Insurance - Staging`. The string
  lives in `rank-math-options-titles` (hyphens): `wp option pluck rank-math-options-titles website_name`,
  then `wp option patch update rank-math-options-titles website_name 'Statewide Flood Insurance'`.
- `wp option update admin_email 'afarmer@californiafloodinsurance.com'` — the **site** admin email is a
  separate setting from the user's and still points at the dead
  `admin@staging.statewidefloodinsurance.com` mailbox. User 1's own email is already fixed.
- The site icon (0c) — still needs a 512×512 PNG, still only a Best Practices point.
- A redundant `.htaccess.pre-prune-2026-08-07.bak` sits in the dormant Divi directory; the reverted
  `.htaccess` there is byte-identical to the original, so the backup can go whenever.
