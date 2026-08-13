# Open items — one index, ordered by risk

Built 7 Aug 2026 by re-reading all 27 documents in this folder, because items were scattered across
files and some had been open since June. Every entry cites where it came from.

**Ordered by consequence, not by chronology.** The single most serious item here is not website work at all.

---

## TIER 0 — ~~BROKEN~~ FIXED 13 Aug. California's sitemap 404 (found and closed same day)

**All three sitemap URLs 404 on `californiafloodinsurance.com`**: `/sitemap_index.xml`,
`/page-sitemap.xml`, `/post-sitemap.xml`. Statewide's are all 200. Confirmed real rather than cached — a
`wordpress_logged_in_*` cookie forces `x-proxy-cache: BYPASS` and it still 404s.

**It is a rewrite-rule problem, not a Rank Math problem, and that is why the fix is trivial:**

| URL | Result |
|---|---|
| `/?sitemap=1` | **200, valid XML, 2 `<loc>` entries** — Rank Math is generating it fine |
| `/sitemap.xml` | 301 → `/sitemap_index.xml` — Rank Math is hooked in |
| `/sitemap_index.xml` | **404 from WordPress**, not from Apache |
| every normal page, `robots.txt`, `/feed/` | 200 |

Rank Math registers a WordPress rewrite rule mapping `sitemap_index.xml` to `index.php?sitemap=1`. The
generator works and the query-string form works, so the rule itself is missing from the rewrite table.
Requests therefore reach WordPress, match nothing, and get the 404 template.

**THE FIX, AND IT WORKED:** Settings → Permalinks → **Save Changes** on California. Nothing else. Verified
immediately after:

| URL | Status | Entries |
|---|---|---|
| `/sitemap_index.xml` | 200 | 2 |
| `/page-sitemap.xml` | 200 | **42** |
| `/post-sitemap.xml` | 200 | **20** |

42 and 20 match the counts taken before it broke, so it is fully restored rather than partially rebuilt. Then a
full sweep: **62/62 sitemap URLs 200, 0 noindex leaks**, and every change made during the day still holding —
`/page/2/` 404 on both brands, `/wp-includes/` 403, the Rank Math plugin directory 403, `readme.html` 403 on
both, homepage and `/get-a-quote/` 200.

**Aaron's report was "I hit save but I don't think that did anything."** He was right to doubt it — WordPress
says only "Permalink structure updated" and gives no indication it rebuilt anything. **A flush that works looks
identical to a flush that does nothing.** Verify from outside; never take the admin notice as confirmation.

**LIKELY TRIGGER, AND THE LESSON:** the theme was replaced three times on 13 Aug (1.5.7, 1.5.8, 1.5.9) and
"Replace current with uploaded" re-activates the theme, which flushes rewrite rules. The sitemap worked earlier
the same session and 404s after. Statewide came through intact, so it is not deterministic — which is exactly
why it needs checking rather than assuming.

**ADD TO THE POST-DEPLOY CHECK: after any theme upload, fetch `/sitemap_index.xml` and confirm 200.** It is one
request. Without it this would have sat broken for weeks while Search Console quietly reported "Couldn't
fetch" — on the site carrying the ad spend.

### CLOSED at the same time — 1.5.9's deny IS live on California

Reported as not working earlier on 13 Aug. That reading was taken before an admin page load had triggered the
installer. Re-verified now, all 403:

```
/readme.html                                     403
/license.txt                                     403
/wp-content/plugins/seo-by-rank-math/readme.txt  403   <- the version leak, closed
/wp-includes/ID3/readme.txt                      403
```

So step 3 is done on both brands and Rank Math's exact version is no longer public. **The lesson is the
theme's own installer runs on `admin_init`** — it cannot have run during the upload request itself, so a check
immediately after uploading will always read stale. Load an admin page first, then verify.

---

## TIER 1 — Credentials. Nothing else on this list can cost as much.

| # | Item | Source |
|---|---|---|
| 1 | **Two `.env` files in synced Dropbox folders hold many live API keys** — `google-ads-project/Google Ads/.env` (Google Ads developer token, client secret, refresh token, on the account spending ~$24,771/mo) and `call-intelligence/.env`. **This is deliberate**, not carelessness: Aaron uses Dropbox as his cross-device secrets store so the keys are reachable from any computer. So the fix is not "delete it" — see below. Flagged twice. | `LAUNCH.md:441`, `CLEANUP-WORKLIST.md:893` |
| 2 | **Three application passwords still live**: statewide staging `AJFarmer`, CFI staging `AJFarmer`, and **`jumpins Admin`**. Jumpins is live production with no staging in front of it, so revoke that one first. California production's was verified revoked (401). | this session |

**Why this is Tier 1:** a leaked refresh token is not a degradation, it is somebody else operating the
ad account. Everything else on this list is recoverable.

### The requirement is real, so the fix has to preserve it

The need is legitimate — reach the keys from any machine. Dropbox meets that but stores them as
plaintext in a folder that syncs. **1Password already covers the same requirement** and is already paid
for:

- **Simple:** the file's contents as a Secure Note, or the `.env` attached as a Document.
- **Better, if scripts consume these keys:** 1Password CLI injects at runtime, so the plaintext never
  lands on disk. The `.env` becomes a template of `op://Vault/Item/field` references — safe to sync, safe
  to commit — and `op run --env-file=.env -- <command>` supplies the real values in memory only.

**What the actual exposure is**, since it is not "Dropbox gets breached":

- every machine that ever synced the folder holds the plaintext on disk;
- Dropbox version history and Deleted Files retain earlier copies after any edit;
- anyone added to the folder, or handed a link, receives all of it at once;
- **a refresh token does not expire**, so an old synced copy on a retired laptop stays valid indefinitely.

**Rotation is a separate action from storage and still applies.** Moving the file protects the future; it
cannot undo exposure that already happened. Since neither of us can establish whether it was ever
exposed, the Ads refresh token is worth re-minting regardless — it is the one credential here that grants
standing control of ad spend.

**Never hand this item to an agent.** Any prompt about these files risks the values landing in a chat
transcript, which is the exact failure being closed.

---

## TIER 2 — Legal wording

| # | Item | Source |
|---|---|---|
| 4 | **Terms of Service arbitration decision.** Production compelled binding arbitration with a class-action waiver; the new §24 explicitly does not. That is a deliberate change to customers' legal rights and it is a lawyer's call, not ours. | earlier session |

### CLOSED 7 Aug — the 40,000+ / 900+ / 4.9 figures

**Verified by Aaron directly, as the owner who set up the underlying systems.** He confirmed the
numbers are real. `REVIEW.md:57` had carried this as an open pre-launch verification item; it is closed
and the source has been annotated so it is not re-raised.

Two smaller parts of that same `REVIEW.md` line were not addressed and may already be settled — the
exact private-market count, and the agency/coverholder wording with counsel. Mentioned once here so
they are not silently dropped; dismiss if they are done.

---

## TIER 3 — Ads measurement. Bigger than the migration, and predates it.

| # | Item | Source |
|---|---|---|
| 5 | **The 15 July audit's headline finding is still open: ~60 conversion actions, dozens Primary, across six unrelated brands** — so flood campaigns bid partly toward non-flood conversions and every CPA is directional. **Its plan is still marked DRAFT.** | `LAUNCH.md:434` |
| 6 | **Cross-site contamination**: California's `GTM-MZ6RZ94` runs on `jumptruckinginsurance.com` with tag 27 unscoped, so Jump Trucking's clicks count as California's quotes. **Blocked on importing `quote_form_lead` first** — scoping tag 27 before that leaves California with no conversion at all. | `POST-LAUNCH-AUDIT.md` |
| 7 | **Statewide production carries an orphaned `GTM-MZ6RZ94` `<noscript>` iframe** with no head loader — another instance of the same cross-brand leakage, from when statewide was cloned off CFI's Divi build. | `LAUNCH.md:313` |
| 8 | **Statewide's `G-FH3Q6GKNHH` is hardcoded on Jump Trucking's pages**, so statewide's GA4 property takes Jump Trucking traffic too. | this session |
| 9 | 13 Primary actions with **zero** conversions in 30 days; duplicate `Earthquake Insurance - Residential` / `Earthquake - Residential` pairs (same for Commercial); **five** Jump Trucking actions, four Primary. | this session |
| 10 | GA4 cleanup: 14 empty accounts (paste ready at `GA4-DELETE-PASTE.md`), 4 dead duplicate properties, 2 property moves. | `ACCOUNTS.md` |
| 10b | **No Google tag configured for `AW-1012143191` in either container.** GTM flags it Urgent in both. Verified from the published `gtm.js` of each: `AW-1012143191` appears only inside `productSettings` as a `preAutoPii` flag, never as a Google tag destination — the sole destination is the GA4 ID (`G-FH3Q6GKNHH` statewide, `G-3YMN51H7LE` California). Conversions still record via the legacy `__awct` path. **Both brands share Ads conversion ID 1012143191**, so this is one change affecting both. **Do it after item 6, never alongside it** — two simultaneous measurement changes on a ~$24,771/mo account make any volume change unattributable. | this session |

### Container audit, 7 Aug — `GTM-PRRWDV4` (cheapsoberlivinginsurance.com) is CLEAN

Read from the published `gtm.js`. Its only GA4 destination is its own `G-B5M0MYQ0QQ`, and **none** of the
other brands' IDs appear — no `GTM-MZ6RZ94`, `GTM-PJQ72VK`, `GTM-PBH839BH`, `GTM-KHPR4LW`,
`G-FH3Q6GKNHH`, `G-3YMN51H7LE` or `G-KSYS0430MS`. It uses the shared Ads account `1012143191` with three
of its own conversion labels, which is expected — one Ads account spans all brands.

**So the contamination is not universal**, and that matters for planning: it is specific to Jump Trucking,
where the served HTML carries `GTM-MZ6RZ94` (California's container), `GTM-PBH839BH` (its own) **and**
`G-FH3Q6GKNHH` (statewide's GA4 property) — items 6, 7 and 8 confirmed at the wire rather than inferred.

**Sequencing constraint that follows:** rebuilding Jump Trucking is the natural moment to strip those, but
California's Ads conversions currently depend on tag 27 firing from Jump Trucking's clicks. Removing the
container before California has a working `quote_form_lead` conversion would leave California with no
conversion feed. **Item 6 must land before any Jump Trucking rebuild**, or a website project silently
becomes an Ads outage.

Note it also carries **5 `__html` custom-HTML tags**, which are worth reading before that flip — custom HTML
is where hardcoded IDs and hostnames hide.

**Item 5 is the umbrella.** Tonight's contamination finding is one instance of it. Cleaning individual
signals on top of a feed that counts six brands together is, in the words of that doc, *"optimising
toward cleaner garbage."*

---

## TIER 4 — Before the statewide flip

**Work this tier from `STATEWIDE-FLIP-RUNBOOK.md`, not from this table.** The runbook puts these in
execution order with the commands; this table is only the index. Items 11, 15 and 16 are settled as of
7 Aug — 12, 13 and 19 are the remaining Phase 0 blockers.

| # | Item | Source |
|---|---|---|
| 11 | ~~Note a baseline week of GA4 pageviews before flipping~~ **DONE 7 Aug.** 31 Jul–6 Aug: 6,887 pageviews / 2,731 sessions / 2,352 users, and 2 `page_view` per load confirmed in Realtime. Recorded in `STATEWIDE-FLIP-RUNBOOK.md`. **The cause was not Site Kit** — Site Kit is not connected; statewide production carries a hardcoded `gtag/js` for `G-FH3Q6GKNHH` in the Divi header alongside the container's Google tag. `LAUNCH.md:309` was wrong and the duplicate dies with Divi. Expect ~6,887/wk → ~3,400 with no real traffic loss. | `LAUNCH.md:309`, this session |
| 12 | ~~Read `GTM-PJQ72VK`'s two "Urgent" container-quality issues~~ **DONE 7 Aug, neither applied.** "Missing Google tags → AW-1012143191" is real but systemic across both containers → moved to item 10b. "Additional domains detected → Conversion Linker" is the `staging.` hostname, which ceases to exist after the flip; recheck in a week. Reasoning in `STATEWIDE-FLIP-RUNBOOK.md` §0a-bis. | `LAUNCH.md:41` item 7c |
| 13 | ~~Pause tag 56~~ **DONE 7 Aug, published as version 15 and verified in the published `gtm.js`**: `I0VbCLiCgoQYENeo0OID` went from 2 occurrences to 1, `__awct` from 4 to 3, tags 45/46/57 untouched. Its `BLOCK - staging hostnames` exception was conditioned on `e eq gtm.js` and could never have blocked a `cfi_form_submit` tag. Rollback: version 14. | `STATEWIDE-PREFLIP.md:2` |
| 14 | Install `statewide-prune-redirects.conf` **at** the flip. Collision check re-run 7 Aug: 50 rules, all 50 sources 404 on the new site, 0 duplicates, 0 uncovered, 0 extras, all 18 targets 200, 0 prefix collisions. | `STATEWIDE-PREFLIP.md:8` |
| 15 | ~~Decide the 7 California geo redirects~~ **DECIDED 7 Aug: cross-domain** to `californiafloodinsurance.com/get-a-quote/`. The `.conf` is swapped; the same-domain lines are retained commented and marked SUPERSEDED. | `statewide-prune-redirects.conf` |
| 16 | ~~Decide the folder-naming approach~~ **DECIDED 7 Aug: Option A** — flip the docroot, verify, then rename both folders in the same session. Phase 3 of the runbook. | `STATEWIDE-PREFLIP.md:9` |
| 17 | Purge **and verify** robots.txt after the flip. Leave Rank Math's box empty. | `STATEWIDE-PREFLIP.md:6` |
| 18 | Remove statewide staging's `noindex` **at** launch. | `STATEWIDE-PREFLIP.md:7` |
| 19 | Set statewide's **site icon**, or it inherits a `/favicon.ico` 404 and a Best Practices ding. | `STATEWIDE-PREFLIP.md:7` |
| 20 | Add `AboutPage` / `ContactPage` schema to the 4 pages that lost types. The `Article` types on `/get-a-quote/` and `/insights/` were Divi artefacts — losing those is an improvement. | `STATEWIDE-PREFLIP.md:8` |
| 21 | Review statewide's **voice and claims**, and whether more pages deserve the 2026-edition treatment. | `STATEWIDE.md:113`, `:211` |

---

## TIER 5 — Around 6 September

| # | Item | Source |
|---|---|---|
| 22 | **Extract Divi's Custom CSS and Integration code before the archive is deleted.** The generated file was lost to an agent sandbox; retrieval path is recorded (`mrtaco5_wp_2b1xy`, prefix `F01Hh8gh_`, `et_divi` option, mirrored at post ID 6). Losing it is defensible — it should be a choice, not an accident. | `POST-LAUNCH-AUDIT.md` |
| 23 | Rename both California folders so the names stop lying, repoint the docroot, then delete the `new.` subdomain. | `FLIP-LOG-CALIFORNIA.md` |
| 24 | **Cancel the Elegant Themes subscription** once Divi is gone — `et_core_version 4.27.7` on a theme running nothing. Check the renewal date first. | this session |
| 25 | Revisit GTM deferral against **CrUX field data**, not Lighthouse. `CFI_TAGS_DEFER` is still in the theme. | `PERFORMANCE.md` |
| 26 | Check field Core Web Vitals once the new site has its own 28-day window (~4 Sept). Divi was **failing** on both form factors. | `PERFORMANCE.md` |

---

## TIER 6 — Housekeeping, real but small

| # | Item |
|---|---|
| 27 | GBP posts written and never posted: El Niño, FAIR Plan. Also set the GBP website URL to `https://`. |
| 28 | Wordfence licence key + 2FA. |
| 29 | Add a description to the *Private Flood Insurance VS FEMA* YouTube video — the only one of four without. |
| 30 | **Statewide has no SPF and no DMARC — confirmed at DNS 7 Aug, not just suspected.** TXT holds only `google-site-verification=JXdoRp-…`; `_dmarc` returns nothing; MX is `0 statewidefloodinsurance.com.`, so the hosting server sends its own mail unauthenticated. This already bit us: the WordPress password-reset email could not be relied on during the flip, and it affects **quote notification emails reaching inboxes** — a lead-loss path, not just a nuisance. Promote out of housekeeping when the flip is done. |
| 31 | Delete the superseded `READ-ME-FIRST.md` in Dropbox `Flood Site Cutover/` (2.69 KB, 4:58 pm). The current one is a level up. |
| 32 | Decide on **Microsoft Clarity** — a Microsoft Advertising setting on UET `5318858` (CFI) and `5318855` (statewide). Privacy call as much as performance. |
| 33 | Decide **core auto-updates** on California — currently *Do not Auto Upgrade* with plugins and themes disabled. Suggest core minor/security only. |
| 34 | Post-launch schema additions: licence `PropertyValue` (`0L75450`), `ContactPoint`, `worksFor` by `@id`. |
| 35 | Cognito **form 5** issue, open since June. | 
| 36 | Ask InMotion to set the static-asset cache header in **nginx** — the theme cannot, because Apache never sees those requests. |
| 37 | ~~Upload theme 1.5.8 to both installs~~ **CLOSED 10 Aug — 1.5.8 live and verified on both, with a forced cache bypass.** |
| 38 | ~~Export the Search Console URL lists~~ **DONE 10 Aug, all three read and every URL tested live. Root cause found — see below.** |
| 39 | ~~CALIFORNIA SERVES DIRECTORY LISTINGS~~ **CLOSED 10 Aug — listings off on the live docroot, purged and verified. 290 of 529 URLs now correct.** Original note kept for the folder trap: **CALIFORNIA SERVED DIRECTORY LISTINGS AND STATEWIDE DID NOT.** cPanel -> Advanced -> Indexes -> **`new.californiafloodinsurance.com`** -> No Indexing. **The live docroot is the `new.`-named folder; the domain-named folder is the dead Divi install.** The first attempt on 10 Aug hit the dead folder, reported success, and changed nothing. This is the whole fix for 69 live URLs, stops Google finding more, and closes a version-disclosure hole. Full detail and the two optional follow-ups in `california-hardening.conf`. |
| 40 | Theme **1.5.9** — fixes the `inc/htaccess.php` version-gate bug AND auto-installs the readme/license deny (step 3 of `california-hardening.conf`), so that step needs no manual .htaccess edit on either site. |
| 41 | **Step 2** of `california-hardening.conf` — the only remaining manual server change. Deliberately not automated: it rewrites `/wp-includes/**.php` to 404, which interacts with WordPress's own rewrite block and needs the `wp-tinymce.php` exception. **Todoist, due 18 Aug.** |

### Reminders set in Todoist, 10 Aug — "Things to Do Soon", label `websites`

Set because three items here are date-bound and easy to lose, and each carries the trap that already caught us:

| Due | Task | The trap it names |
|---|---|---|
| 18 Aug | Finish the wp-includes hardening (step 2) | live docroot is the `new.` folder; keep the `wp-tinymce.php` exception |
| 1 Sept | Check the Search Console soft-404 count dropped | barely-moved numbers at 3 weeks are normal, not a reason to act |
| 8 Sept | California folder rename + delete the Divi archive | **extract Divi's `et_divi` CSS and Integration code from the DB first — it is the only copy** |

The 8 Sept item is the one that matters most, and not for tidiness: until the rename happens, every server-side
change on California has a wrong answer that looks right and reports success. It has already happened twice.

### Search Console page-indexing report, 10 Aug — one live bug, the rest is history

Aaron surfaced California's Page indexing report: **1,455 URLs not indexed** across ten reasons. Read cold that
is alarming. Measured, it mostly is not.

**The arithmetic that frames it.** California has **62 URLs** in its sitemap. Its Divi predecessor had **86** in
`cfi-production-seo-audit.csv`, and the prune added **38** rules. No combination of real pages reaches four
figures, so the overwhelming majority of that 1,455 is URL space Google accumulated over the old site's life —
and the report is **cumulative and lagging**, holding the last verdict on every URL Google has ever seen,
including verdicts formed years before the Kadence build existed.

**Everything probed on the live site is configured correctly** (all cache-busted, 10 Aug):

| Shape | Result | Verdict |
|---|---|---|
| Nonexistent slug, `?p=`, `?page_id=`, `?attachment_id=`, `?m=`, `?author=` | 404 + noindex | correct |
| Date, author, and non-existent tag/category archives | 404 + noindex | correct |
| Categories that do exist | 200 + noindex | correct, by design |
| Search results, `?replytocom=` | 200 + noindex | correct |
| `/insights/page/2/`, `/category/…/page/2/` | 200 | correct |
| `/insights/page/9/` — over range | 404 | correct, WP handles it |
| **`/page/2/`, `/page/99/`, `/page/500/`** | **200 + `index`** | **BUG** |

**The one real defect: the static front page had unbounded pagination.** Every `/page/<N>/` returned 200,
served the homepage and said `index` — an infinite set of distinct indexable URLs with identical content, which
is exactly what earns a Soft 404 verdict. Fixed in **1.5.8**, scoped to the front page only because archive
pagination was verified working first and a broader `max_num_pages` guard would have broken `/insights/`.

#### 1.5.7 shipped broken, and both wrong turns are worth keeping

**The guard checked the wrong query var.** On an archive, `/page/2/` sets `paged`. On a **static front page** it
sets **`page`** — the var normally associated with `<!--nextpage-->` — and leaves `paged` at 0. 1.5.7 tested only
`paged`, so it never fired. Its own docblock had described `page` as the thing being deliberately left alone.
1.5.8 takes `max()` of both, which is safe because `front-page.php` never calls `the_content()`, so no
post-internal pagination exists on that page for either var to legitimately describe.

**Then the failure was misdiagnosed as cache.** The live URL returned 200 with `x-proxy-cache: HIT`, which is
exactly the stale-cache trap this project has hit repeatedly — and this time it was not that. The check that
settled it, worth reusing:

```
curl -sD - -o /dev/null -H "Cookie: wordpress_logged_in_test=bypass" https://<host>/page/2/
```

A `wordpress_logged_in_*` cookie makes nginx report `x-proxy-cache: BYPASS`. It still returned 200, which proved
PHP rather than nginx. **Force a BYPASS before blaming the cache — and before trusting a pass.** A cache-busting
query string is not equivalent; the cookie is what changes nginx's decision.

Deployment itself was fine and was confirmed independently, by fetching the theme's own stylesheet and reading
its version header — `/wp-content/themes/cfi-kadence-child/style.css` returned `Version: 1.5.7` on both hosts.
That check separates "not installed" from "installed and not working" in one request, and should be step one
next time.

**Triage of the ten rows.** Three deserve attention, seven do not:

- **Soft 404 — 440. ANSWERED 10 Aug by the export: none of it is content, and the pagination hole was not the
  cause.** See the section below.
- **Crawled, currently not indexed — 823.** Google's quality judgment, **not a configuration error**, and not
  fixable from the server. Against 62 real pages this is old thin content Google has declined to keep. No action
  beyond continuing to publish pages worth indexing.
- **Excluded by noindex — 29.** Consistent with categories, search and `staff-form` being deliberately noindex.
  **Verify from the export, do not assume** — a false alarm was raised on exactly this bucket on 6 Aug, where 24
  URLs looked deindexed and were stale cache entries, and the proposed fix would have stripped legitimate
  protection.
- Not found 404 (58) is the prune working. Duplicate without canonical (89) is almost certainly legacy parameter
  URLs. Redirect (4), robots.txt (2), other 4xx (1) and Discovered-not-indexed (9) are noise.

**VERIFIED 10 Aug, 1.5.8 on both hosts.** Every check run twice — once with a `wordpress_logged_in_*` cookie to
force `x-proxy-cache: BYPASS` (is PHP right?) and once bare (is that what the public gets?). Both agreed
everywhere, which is the only condition under which a pass means anything here.

| URL | California | Statewide |
|---|---|---|
| `/` | 200 | 200 |
| `/page/2/`, `/page/3/`, `/page/99/`, `/page/500/` | **404** | **404** |
| `/insights/` | 200 | 200 |
| `/insights/page/2/` | 200 | 404 — correct, see below |
| `/insights/page/9/` | 404 | 404 |
| `/get-a-quote/` | 200 | 200 |

**Statewide's `/insights/page/2/` 404 is not a regression.** Statewide has **8 posts**; California has **20**.
Eight fit on one page, so page 2 has never existed there and `/insights/` renders no pagination links at all.
The guard could not have caused it either way — it is scoped to `is_front_page()`. The test expectation was
wrong, not the site: **one site's correct value is not the other's**, even on a shared theme. Confirm the
underlying data before recording a cross-site difference as a fault.

### The exports, read — 10 Aug. Root cause: directory listings on California only

All three URL lists exported and **every one of the 529 URLs tested live**. The finding is unambiguous:
**not a single content page appears in either error bucket.** Every URL is under `/wp-includes/` or
`/wp-content/themes/`.

**The cause is a difference between the two sister sites, on the same cPanel account:**

```
californiafloodinsurance.com/wp-includes/   200, 54,507 bytes, "Index of"
statewidefloodinsurance.com/wp-includes/    403
```

California serves directory listings. Googlebot walked the tree and enumerated hundreds of core source files.

| Bucket | Live status | What it is | Action |
|---|---|---|---|
| Soft 404 | 206 -> **404** | `/wp-content/themes/Divi/**.php` — theme deleted | **none, already resolved** |
| Soft 404 | 214 -> **500** | nested `/wp-includes/**.php`, fatal outside WP | step 2 |
| Soft 404 | 20 -> **200** | top-level `/wp-includes/*.php` returning empty — the literal soft 404s | step 2 |
| Duplicate | 40 -> **404** | Divi again | **none, already resolved** |
| Duplicate | 49 -> **200** | directory listings + `readme.txt` / `license.txt` | step 1 |
| Noindex | 29 | categories, author, date archives, tag feeds | **none, all deliberate** |

**246 of 529 need nothing** — they are already correct and only waiting on Google to re-crawl.

**The front-page pagination hole was NOT the cause of the 440.** It was a real bug and worth fixing on its own
merit, but no `/page/N/` URL appears anywhere in the export. Fixing it was correct; attributing the 440 to it
would have been wrong, and this is exactly why the export was worth waiting for rather than acting on a theory.

**It is also a disclosure problem, not only an SEO one.** With listings on, any directory lacking its own
`index.php` is browsable. Verified on California and not on statewide:
`/wp-content/themes/cfi-kadence-child/` and `/wp-content/plugins/seo-by-rank-math/` are both browsable, and
Rank Math's `readme.txt` returns `Stable tag: 1.0.275` — an exact plugin version, which is the first step of a
targeted-exploit search. One change fixes both.

**Fix, verification and the two optional follow-ups are in `california-hardening.conf`.** Use the cPanel Indexes
toggle rather than hand-editing `Options -Indexes`: a bare `Options` line returns HTTP 500 for the whole site if
AllowOverride does not permit it, and a supported toggle does the same job with no such risk.

**DO NOT add `Disallow: /wp-includes/` to robots.txt.** WordPress serves block-library CSS and JS from that
path, so blocking it stops Google rendering the pages, and Disallow would not remove anything already indexed
anyway. The fix belongs at the HTTP layer, where the response itself changes.

#### CLOSED 10 Aug — final state after the fix

Directory indexing disabled on `/home/mrtaco5/new.californiafloodinsurance.com` (the live docroot, second
attempt — the first hit the dead Divi folder), followed by a full nginx purge. All 529 URLs retested:

| Bucket | Count | Status | Meaning |
|---|---|---|---|
| Divi theme files | **246** | 404 | already resolved before any change |
| Directory listings | **44** | 403 | **fixed by this change** |
| `wp-includes` PHP files | 214 | 500 | step 2, optional |
| Empty-200 PHP files + `/wp-includes/blocks/` | 20 | 200 | step 2, optional |
| `license.txt` / `readme.txt` | 5 | 200 | step 3, optional |

**290 of 529 are now correct**, and no content page was ever affected. Nothing broke: homepage,
`/get-a-quote/`, `/insights/`, `/insights/page/2/` all 200; `/page/2/` still 404 from 1.5.8; and every asset
verified loading — block-library CSS and JS from `/wp-includes/`, both self-hosted fonts, hero poster, site
icon, Kadence header CSS, an upload, and `wp-tinymce.php`.

**Two cache lessons, both already in this file's history and both re-earned today.** The purge did not appear
to work at first: two URLs (`/wp-includes/` and the Rank Math plugin directory) kept returning cached 200
listings while fresh query-string requests returned 403. Re-requesting a few seconds later returned 403 on
every attempt — they were the last stale entries clearing. **Do not diagnose a purge from a single request per
URL.** And the reverse of the same coin: fresh-URL 403s were correct for twenty minutes while the public was
still being served the listings, so **a config that is right is not the same as a site that is fixed.**

**One residue step 2 will not catch:** `/wp-includes/blocks/` returns an empty 200 because it contains its own
`index.php`, so it is not a listing and the `.php` rewrite does not match it. One URL, not worth a rule.

**Do not click "Validate Fix" on all ten rows.** Validation on a bucket whose URLs are stale starts a process
that fails and re-queues, and it tells you nothing you did not already know. Validate Soft 404 after 1.5.7 is
uploaded, and leave the rest until the export has been read.

---

## What is genuinely finished

California is live and verified: 62/62 sitemap URLs 200, all canonicals self-referential, 0 noindex
leaks, 20/20 301s and 18/18 410s firing, robots.txt correct, site icon set, Best Practices back to 100
confirmed by Google, Accessibility 100, SEO 100, lab CLS 0. Theme at 1.5.6 on both installs. The
performance question is settled and documented. The Divi Integration boxes were audited and held nothing
that needed migrating.

## The honest summary

**Tier 1 outranks the entire migration.** A refresh token in a synced folder is a larger exposure than
anything about themes, containers or Core Web Vitals, and it was flagged twice before launch and carried
forward anyway.

The claims item that sat beside it in Tier 2 is **closed** — Aaron verified the figures himself as the
owner who built the systems behind them.

**Tier 3 item 6 is the one that keeps generating new problems.** Tonight's contamination finding was a
symptom of it. It has been open since 15 July with its plan still in DRAFT.
