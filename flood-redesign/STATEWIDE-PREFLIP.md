# Statewide — what to settle before the flip

Written 8 Aug 2026, after California went live. Read `FLIP-LOG-CALIFORNIA.md` for the mechanics; this
covers only what is **different about statewide**, found by auditing rather than assuming.

---

## 1. Search Console verification — NOT an issue. My warning was unfounded.

I flagged this as "the one thing that could genuinely hurt," on the theory that statewide relied on
HTML-file verification that dies with the docroot swap. **It does not.** Resolved over DNS-over-HTTPS
(no `dig` on this box — that absence is why the first attempt returned empty and looked like "no
records"):

```
statewidefloodinsurance.com   TXT  google-site-verification=JXdoRp-ycIhoLLHRe8hdbMyUOUQG2nT80mmR7Dy44Bk
californiafloodinsurance.com  TXT  google-site-verification=JyoiyhKquy3cvMUyk3pzlIswwlBCYX9N13JruGic6a0
```

Verification is **DNS-based, so it survives the docroot swap with no action.** Both records confirmed
present; both stay untouched, as always.

Incidental observation, not SEO and not verified further: statewide's TXT response carried **no SPF
record**, while California and jumpins both do (`v=spf1 ... include:spf.protection.outlook.com -all`).
Worth someone checking, because it affects whether quote emails land in inboxes.

---

## 2. THE BLOCKER — statewide's container will multiply Ads conversions at the flip

`GTM-PJQ72VK`, container **version 14**, 41 tags. Unlike California's `GTM-MZ6RZ94`, which holds
**zero** `__awct` tags, statewide holds **four**:

| tag_id | Conversion label | Fires on |
|---|---|---|
| 45 | `COU0CK2O12cQ16jQ4gM` | `gtm.click` where element text contains **"Submit Application"** — Divi-era |
| 46 | `I0VbCLiCgoQYENeo0OID` | `gtm.click` where element text contains **"SUBMIT"** — Divi-era |
| **56** | `I0VbCLiCgoQYENeo0OID` | **`cfi_form_submit` AND `cfi_is_lead = true`** — new theme |
| **57** | `COU0CK2O12cQ16jQ4gM` | **`cfi_form_submit` AND `cfi_is_lead = true`** — new theme |

**Tags 56 and 57 fire on the byte-identical trigger and send two different conversion labels.** So one
lead produces **two Ads conversions** the moment the new theme starts pushing `cfi_form_submit`. Tags
45 and 46 may fire on top of that if the Cognito button text still matches, taking it to as many as
four.

This does not happen today, because Divi never pushes `cfi_form_submit` — only 45/46 can fire. **It
starts happening at the flip.**

And it lands on **`AW-1012143191`, the same Ads account California uses.** Corrupted conversion counts
would feed Smart Bidding for *both* brands, on ~$24,771/mo of spend.

### What to check, in the Ads UI, before flipping

Look up the two conversion actions behind labels `COU0CK2O12cQ16jQ4gM` and `I0VbCLiCgoQYENeo0OID`.

- **If both are Primary** — this is straight double-counting. Pick one, set the other to Secondary or
  pause its tag.
- **If one is Primary and one Secondary** — firing both may be intentional (one bids, one observes).
  Confirm that is the design rather than an accident, then leave it.

Either way, **45 and 46 are Divi-era click-based tags and should be deleted at the flip** — they
depend on button text a theme change can break, which is the same fragility that produced California's
triple-event problem. Verify in GTM Preview that they no longer fire, then remove them.

**Do this before the flip, not after.** A week of doubled conversions is a week of mis-trained bidding.

---

## 3. A staging safety net that does not cover what it looks like it covers

All four conversion tags carry a blocking trigger with the condition:

```
e eq gtm.js AND u re ^(new|staging)\.
```

Because it requires `e eq gtm.js`, GTM can only apply it on the container-load event. A tag firing on
`cfi_form_submit` is evaluated against `e = cfi_form_submit`, which does not match — so **the block
does not protect form-submit conversions on a staging hostname.**

It has not mattered, because the real protection is the theme's host gate in `inc/tags.php`:
`cfi_tags_active()` returns false unless the hostname is `CFI_PROD_HOST`, so GTM never prints on
staging at all.

**But the documented administrator override `?cfi_tags=1` bypasses that gate.** So: **never submit the
quote form on `staging.statewidefloodinsurance.com` while using `?cfi_tags=1`.** That combination would
fire real Google Ads conversions on the live shared account. Use GTM Preview mode for tag verification
instead — it does not need the override.

---

## 4. Expect the same performance as California. Not better.

I previously explained statewide-Divi's respectable LCP by saying `GTM-PJQ72VK` holds no Google tag.
**That was wrong** — corrected in `PERFORMANCE.md`. It holds `__googtag` for `G-FH3Q6GKNHH`, and
statewide production loads the full stack:

```
gtag/js?id=G-FH3Q6GKNHH            176.6 KiB
gtm.js?id=GTM-PJQ72VK              158.9 KiB
gtag/destination?id=AW-1012143191  155.4 KiB
bat.bing.com/bat.js                 15.5 KiB
scripts.clarity.ms/clarity.js       25.2 KiB   via UET tag 5318855
```

~**535 KiB**, within 4 KiB of California's 531 KiB. **Identical tag burden.**

So the honest forecast for statewide after the flip is **what California got: ~66–70 mobile, ~88
desktop on the apex URL.** The theme is worth the measured **40 → 69** jump, and the tag stack caps it
there. Nobody should expect statewide to land higher, and nobody should go looking for a theme fault
when it does not.

**`CFI_GA4_ID` must stay empty for statewide.** It is empty and the reason is written out at
`functions.php:33–58`: the container already configures `G-FH3Q6GKNHH`, so printing gtag from the theme
as well would double-count every session. This was set wrongly in 1.4.7 and reverted in 1.4.9.

---

## 5. Clarity is on statewide too, via its own UET tag

`clarity.ms/tag/uet/5318855` — statewide's UET tag is **5318855**; California's is 5318858. Same
arrangement: Clarity is pulled by Bing UET because the integration is enabled in Microsoft Advertising,
and it is switched off **there**, not in GTM or WordPress. ~28 KiB and three extra origins.

If the Clarity decision goes ahead for California, do both at once.

---

## 6. robots.txt — fix at the flip, same as California

Statewide production today:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://statewidefloodinsurance.com/sitemap.xml
Sitemap: https://statewidefloodinsurance.com/sitemap.rss
```

Cleaner than California's (no `farmerflood`, no `/commercial/`), but two things break at the flip:

- **`/sitemap.rss` currently returns 200 and will 404** once Rank Math takes over, exactly as it now
  does on California. Remove the line.
- The theme's claim-PDF `Disallow` will be missing for the same reason it is missing on California —
  Rank Math's robots.txt editor replaces the output. Set it there.

Target content:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# Claim PDFs are deliverables, not search results — the pages hold the same content.
Disallow: /wp-content/uploads/*.pdf

Sitemap: https://statewidefloodinsurance.com/sitemap_index.xml
```

Note `/sitemap_index.xml` currently **302s to `/sitemap.xml`** on Divi; after the flip that reverses.

---

## 7. Still true from before

- **Statewide staging must stay `noindex` until launch.** Verified today: `nofollow, noindex` present.
- **Purge and then VERIFY `robots.txt` after the flip.** On California it served the Divi site's crawl
  directives from the page cache for four hours, because nobody thinks of robots.txt as a cached page.
  Check for the claim-PDF `Disallow` line and the absence of `sitemap.rss`.
- **Do not trust any button in the hosting WordPress manager during the duplicate-URL window.** On
  California, `Login` on the dead install's row opens the **live** site's dashboard, because the manager
  routes by stored URL and both installs report the same one. Identify installs by Website Path or by
  `DB_NAME` read from `wp-config.php`, never by URL, thumbnail, or which row you clicked.
- Run `preflight.py --live https://statewidefloodinsurance.com --new https://staging.statewidefloodinsurance.com`
  before the flip for URL parity and asset checks.
- The `x-proxy-cache` behaviour applies here too: **verify without a cache-buster**, and remember nginx
  serves fonts, CSS and `/favicon.ico` itself, so `.htaccess` cannot touch them.
- Statewide will need its own **site icon** set in Customize → Site Identity, or it inherits
  California's `/favicon.ico` 404 and a Best Practices ding.

## 8. preflight.py run — 50 URLs would 404 at cutover

Run 8 Aug against live production vs staging. **108 live URLs discovered, 50 of them 404 on the new
site.** Every one loses its traffic and accumulated ranking the moment DNS moves.

`statewide-prune-redirects.conf` handles all 50. It was validated before shipping, because
California's first draft had ten dead rules and two that collided with new post slugs:

| Check | Result |
|---|---|
| Missing URLs covered | **50 / 50**, each exactly once |
| Rules pointing at a URL that is not missing | **0** |
| Distinct 301 targets returning 200 | **18 / 18** |
| Source paths that prefix-collide | **0** |

Breakdown: **31 topic 301s**, **7 California geo pages needing a decision**, **12 × 410 Gone**.

Some of the matches are unusually good, because the new site happens to carry the modern version of
the old article:

| Old URL | New target |
|---|---|
| `/how-risk-rating-2-0-affects-federal-flood-insurance-policy-holders/` | `/nfip-risk-rating-2-premium-increases/` |
| `/understanding-base-flood-elevation-bfe/` | `/elevation-certificates-2026/` |
| `/master-flood-policies-hoas/` | `/homeowners-association-flood-insurance/` |
| `/when-is-flood-insurance-required/` | `/lender-flood-insurance-requirements-over-250k/` |
| `/hiscox-flood-plus-comprehensive-flood-insurance-coverage/` | `/lloyds-of-london-flood-insurance/` |

### The one block that needs your decision

Seven California city/region pages — Sacramento ×3, San Diego ×2, Long Beach, and a Central Valley
multi-city page. **The new statewide site is national and has no California page at all**, because
California is now the sister site's job.

- **Active default:** same-domain 301 to `/get-a-quote/`. Safe, keeps everything on one domain, loses
  topical relevance.
- **Commented alternative, and my recommendation:** cross-domain 301 to
  `californiafloodinsurance.com`. Better for a visitor actually searching for Sacramento flood
  insurance, and passes ranking signal to the site that should hold it.

Left commented because moving traffic between brands is a business decision. Pick one; do not enable
both.

### Two other preflight findings, neither blocking

**Schema loss on 4 pages** — types present live and absent on the new site:

| Page | Missing |
|---|---|
| `/` | `AboutPage`, `ContactPoint` |
| `/contact-us/` | `ContactPage` |
| `/get-a-quote/` | `Article` |
| `/insights/` | `Article`, `Organization`, `Person`, `WebPage` |

`ContactPoint` was already on the post-launch list for California. The `Article` types on `/get-a-quote/`
and `/insights/` are Divi artefacts — an Article schema on a quote form is wrong and losing it is an
improvement, not a regression. `AboutPage` / `ContactPage` are worth adding.

**`/terms-of-service/` 5,593 words live vs 3,148 new.** Same as California, and the cause there was the
new text using plain English rather than boilerplate — six keyword "losses" turned out to be false
positives, with arbitration the only real difference. Expect the same, but it is a lawyer's call, not
mine.

## 9. Do NOT repeat California's folder-naming mistake

California is now in a state Aaron predicted and disliked, correctly: the hosting WordPress manager
lists **two installs both reporting `https://californiafloodinsurance.com`**, and the folder names are
inverted — `new.californiafloodinsurance.com/` is production, `californiafloodinsurance.com/` is the
corpse. The only reliable discriminator is `DB_NAME` (`mrtaco5_wp441` = live). That is a live risk
every time someone uses the manager's checkboxes to bulk-update or bulk-delete.

Statewide has the identical trap set: `staging.statewidefloodinsurance.com/` would become production
while `statewidefloodinsurance.com/` holds the dead Divi site.

### Option A — repeat California's method, then tidy up the SAME DAY (recommended)

1. Add `WP_HOME` / `WP_SITEURL` = `https://statewidefloodinsurance.com` to the **new** install's
   `wp-config.php`.
2. Repoint the domain's document root to `staging.statewidefloodinsurance.com/`. **Live on the new
   theme** — this is the proven path, identical to California.
3. Verify everything: redirects, robots.txt, purge, GTM, sitemap.
4. **Then, same session — do not defer this by a month:**
   - rename `statewidefloodinsurance.com/` → `archive-divi-statewide-2026/`
   - rename `staging.statewidefloodinsurance.com/` → `statewidefloodinsurance.com/`
   - repoint the document root back to `statewidefloodinsurance.com/`
   Downtime is the gap between the renames — under a minute with both tabs open.
5. Delete the `staging.` subdomain. Its folder is gone, so cPanel will no longer grey out Remove.

Rollback stays available throughout: point the document root at `archive-divi-statewide-2026/`.

**Why the same day.** California deferred this to ~6 Sept and the consequence is a month of two
identically-named installs in a manager with delete checkboxes. Deferring is what created the problem,
not the method.

### Option B — rename first, never touch the document root

Because the domain's document root is *already* `statewidefloodinsurance.com/`, renaming the folders
swaps which install serves the domain with no docroot edit at all:

1. `WP_HOME` / `WP_SITEURL` on the new install.
2. Rename Divi `statewidefloodinsurance.com/` → `archive-divi-statewide-2026/` — **site down.**
3. Rename `staging.statewidefloodinsurance.com/` → `statewidefloodinsurance.com/` — **site up, new
   theme, correct name, no docroot change.**

Fewer moving parts and the names are right from the first second.

**The unknown that makes this Option B and not Option A:** cPanel may refuse to rename a folder that
is an active document root. It already greys out Remove on the `new.` subdomain for that reason. If
the rename at step 2 is blocked, the site is down at that moment with no quick fix except recreating
the name. **Test the rename mechanic on a throwaway folder first.** If cPanel allows it, Option B is
cleaner; if not, fall back to Option A.

### Either way, write the folder READMEs at flip time

Two files, `LIVE-SITE--DO-NOT-DELETE.txt` and `ARCHIVE-DIVI--NOT-THE-LIVE-SITE.txt`, naming which
install is which and quoting its `DB_NAME`. California's versions were written 8 Aug and can be copied
with the names changed. Write them **during** the flip, while the knowledge is in your head — this is
the cheaper half of the whole fix by a wide margin.

## What this audit could not check

Whether the two conversion labels are Primary or Secondary. That lives in the Ads account and is
**the one open question gating the flip.**
