# Open items — one index, ordered by risk

Built 8 Aug 2026 by re-reading all 27 documents in this folder, because items were scattered across
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

### CLOSED 8 Aug — the 40,000+ / 900+ / 4.9 figures

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

**Item 5 is the umbrella.** Tonight's contamination finding is one instance of it. Cleaning individual
signals on top of a feed that counts six brands together is, in the words of that doc, *"optimising
toward cleaner garbage."*

---

## TIER 4 — Before the statewide flip

| # | Item | Source |
|---|---|---|
| 11 | **Note a baseline week of GA4 pageviews BEFORE flipping**, and check DebugView for two `page_view` events on one load. GA4 sessions will fall after cutover with no real traffic loss — that is the Site Kit duplicate going away. Without a baseline the drop is unexplainable after the fact. **This is a do-it-now item.** | `LAUNCH.md:309` |
| 12 | **Read `GTM-PJQ72VK`'s two "Urgent" container-quality issues** in the GTM UI. Still unchecked. I audited the container's contents but never read what GTM itself is complaining about. | `LAUNCH.md:41` item 7c |
| 13 | Pause tag 56 — duplicate Ads conversion on quote submit. **In progress.** | `STATEWIDE-PREFLIP.md:2` |
| 14 | Install `statewide-prune-redirects.conf` (50 rules) **at** the flip, after re-running its collision check. | `STATEWIDE-PREFLIP.md:8` |
| 15 | **Decide the 7 California geo redirects**: same-domain (active default) or cross-domain to `californiafloodinsurance.com` (my recommendation). | `statewide-prune-redirects.conf` |
| 16 | **Decide the folder-naming approach** — Option A (flip then rename same session) or Option B (rename only, no docroot edit; test whether cPanel allows renaming an active docroot first). | `STATEWIDE-PREFLIP.md:9` |
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
| 30 | Statewide appears to have **no SPF record** while California and jumpins do. Affects whether quote emails reach inboxes. |
| 31 | Delete the superseded `READ-ME-FIRST.md` in Dropbox `Flood Site Cutover/` (2.69 KB, 4:58 pm). The current one is a level up. |
| 32 | Decide on **Microsoft Clarity** — a Microsoft Advertising setting on UET `5318858` (CFI) and `5318855` (statewide). Privacy call as much as performance. |
| 33 | Decide **core auto-updates** on California — currently *Do not Auto Upgrade* with plugins and themes disabled. Suggest core minor/security only. |
| 34 | Post-launch schema additions: licence `PropertyValue` (`0L75450`), `ContactPoint`, `worksFor` by `@id`. |
| 35 | Cognito **form 5** issue, open since June. | 
| 36 | Ask InMotion to set the static-asset cache header in **nginx** — the theme cannot, because Apache never sees those requests. |

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
