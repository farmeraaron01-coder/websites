# Open items — one index, ordered by risk

Built 7 Aug 2026 by re-reading all 27 documents in this folder, because items were scattered across
files and some had been open since June. Every entry cites where it came from.

**Ordered by consequence, not by chronology.** The single most serious item here is not website work at all.

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
| 37 | ~~Upload theme 1.5.7~~ **Upload theme 1.5.8 to both installs.** 1.5.7 was installed on both 10 Aug and its guard did not fire — see below. 1.5.8 is the working version. |
| 38 | **Export the Search Console "Soft 404" URL list for California** (440 rows) and send it over, so the 440 can be attributed instead of guessed at. Same for "Duplicate without user-selected canonical" (89) and "Excluded by noindex" (29). |

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

- **Soft 404 — 440.** Needs the export (item 38). The front-page hole fed it; whether it accounts for all 440 is
  unknown and should not be asserted. Note that `california-prune-redirects.conf` already documents the other
  mechanism: *a 301 to a page that is not a close equivalent is treated as a soft 404* — but California has only
  20 such 301s, so that is not the bulk either.
- **Crawled, currently not indexed — 823.** Google's quality judgment, **not a configuration error**, and not
  fixable from the server. Against 62 real pages this is old thin content Google has declined to keep. No action
  beyond continuing to publish pages worth indexing.
- **Excluded by noindex — 29.** Consistent with categories, search and `staff-form` being deliberately noindex.
  **Verify from the export, do not assume** — a false alarm was raised on exactly this bucket on 6 Aug, where 24
  URLs looked deindexed and were stale cache entries, and the proposed fix would have stripped legitimate
  protection.
- Not found 404 (58) is the prune working. Duplicate without canonical (89) is almost certainly legacy parameter
  URLs. Redirect (4), robots.txt (2), other 4xx (1) and Discovered-not-indexed (9) are noise.

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
