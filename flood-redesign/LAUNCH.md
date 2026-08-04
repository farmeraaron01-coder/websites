# Cutover runbook — both sites

Two sites go live: `californiafloodinsurance.com` (staged at `new.californiafloodinsurance.com`)
and `statewidefloodinsurance.com` (staged at `staging.statewidefloodinsurance.com`).

**Both production hosts canonicalise to the bare domain.** `www` 301s to non-www on both, and
production's canonical tags agree. Every URL below is non-www on purpose. Theme v1.3.6 fixed
three hardcoded `www` links that would otherwise have put a redirect hop in front of the quote
button.

**Timing.** Pre-flight is about half a day and touches nothing public. The flip is 15–30
minutes per site. Post-flip verification is another 30–45. Both sites can go the same day.
The two-week watch afterwards is where the real attention goes.

---

## Phase 0 — pre-flight (nothing public changes)

| # | Item | Owner | Done |
|---|------|-------|------|
| 1 | Install theme **v1.3.6** on both sites (both are on 1.3.4 — this also activates the PDF `noindex` header and the tag snippet) | Aaron | ☐ |
| 2 | Confirm whether the GTM containers already hold a GA4 configuration tag → see *Analytics* below | Aaron | ☐ |
| 3 | Verify tags fire on staging: any page + `?cfi_tags=1`, logged in as admin, with Tag Assistant | Claude | ☐ |
| 4 | Sign off content: 9 statewide articles, 10 claims pages, 18 drafted meta descriptions | Aaron | ☐ |
| 5 | Sign off statewide palette and hero copy | Aaron | ☐ |
| 6 | Correct the four "separate purchases" instances in the source PDFs (copy supplied; sites already fixed) | Aaron | ☐ |
| 7 | **Verify both domains in Search Console by DNS TXT record** — see *Site Kit* below | Aaron | ☐ |
| 8 | **Full backup of each production site — files + database — downloaded off the server** | Aaron | ☐ |
| 9 | Confirm the cutover method with InMotion (see *Rollback*) — docroot swap, not overwrite | Aaron | ☐ |

Not launch-blocking, decide later: the asymmetric-lanes / cross-domain canonical question for
the duplicated claims content.

---

## Phase 1 — the flip, per site (15–30 min)

Do CFI first; statewide gets the benefit of anything learned.

1. **Backup again**, immediately before. The Phase 0 backup is the safety net; this one is the
   restore point.
2. **Point the domain at the new install.** Preferred: change the document root, leaving the
   old install on disk untouched. Do NOT use a "push to live" that overwrites production —
   that is what makes rollback a restore instead of a click.
3. **Fix the site address.** WordPress `siteurl` and `home` → `https://californiafloodinsurance.com`
   (no `www`, no trailing slash). Then search-replace the staging hostname across the database:
   `new.californiafloodinsurance.com` → `californiafloodinsurance.com`. Statewide:
   `staging.statewidefloodinsurance.com` → `statewidefloodinsurance.com`.
   Check uploads URLs and the five PDF links in the claims cluster specifically.
4. **Remove the noindex.** Settings → Reading → uncheck "Discourage search engines", and clear
   the site-wide `noindex` in Rank Math. Leave the staff form page noindexed — that one is
   deliberate (`rank_math_robots = noindex,nofollow`).
5. **Install the redirects.** The 6 CFI redirects **with trailing slashes** (the defect noted in
   MIGRATION.md), plus `/media/` → `/video/`. Delete `/floodguru/` outright on statewide, no
   redirect (your call, recorded 30 July).
6. **Flush the nginx cache** (Nginx Helper → Purge Entire Cache).
7. **Verify before telling anyone** — the checklist below.

### Post-flip verification

- Render, don't just curl: homepage, a coverage page, a claims page, a guide, the quote page,
  the staff form, a blog post. Look at them.
- Submit **both** Cognito forms end to end and confirm the entry arrives.
- Confirm the phone links dial and the quote button lands with **no redirect hop**.
- Tag Assistant on the live homepage: GTM container loads, GA4 fires **once** (not twice).
- Google Ads: confirm a conversion registers from a real test submission, then note the time so
  you can identify the test row later.
- `curl -I` any claims PDF → `X-Robots-Tag: noindex, noarchive`.
- Spot-check 10 old URLs from the redirect map, following redirects, and confirm each lands on a
  200 with the intended page.
- View the served JSON-LD on the homepage: one Organization/InsuranceAgency node, no Article
  node, and **no Escondido mailing address**.

### Same day, after verification

- Submit the Rank Math sitemap in Search Console for both properties; request indexing on the
  homepage and top 5 pages.
- Google Business Profile: website URL → `https://californiafloodinsurance.com` (it is currently
  `http`).
- Wordfence: paid key, and 2FA set to Required.
- **Revoke the three application passwords pasted into chat**: staging `AJFarmer`, production
  `farmeraaron`, statewide staging `AJFarmer`.
- Ask InMotion to exclude `/wp-json/` from the nginx cache (authenticated REST responses are
  currently cached, which is why purges needed a REST write to trigger).

---

## Analytics — moving what already exists

Nothing new gets created. The containers below are the ones already running on production; a
GTM container ID is not tied to a domain, so the same snippet works on the new site with all
tags, triggers, and Ads conversions intact.

| | CFI | Statewide |
|---|---|---|
| GTM container | `GTM-MZ6RZ94` | `GTM-PJQ72VK` |
| GA4 property | `G-3YMN51H7LE` | `G-FH3Q6GKNHH` |
| How it loads today | GTM hand-placed in the Divi header; **GA4 via the Site Kit plugin** | same |
| How it loads on the new site | theme, `inc/tags.php` | theme, `inc/tags.php` |

Theme v1.3.6 prints the GTM snippet **only on the production hostname**, so staging cannot send
data. That matters less for GA4 pageviews than for Ads conversion tags, where one test
submission counts as a real lead and feeds Smart Bidding a fake conversion. At cutover the
hostname becomes the production one and tagging starts by itself — there is no step to forget.
To test before then: `?cfi_tags=1` on any page while logged in as an administrator.

**The one open question: `CFI_GA4_ID` is intentionally empty.** Site Kit is not in the new
plugin stack, so GA4 needs a home — either as a configuration tag inside GTM (preferred: one
tag system) or printed directly by the theme. If the container already has a GA4 tag and the
theme prints gtag as well, every session is counted twice: page_view doubled, users inflated,
conversion rate halved. Open the container, check for a GA4 configuration tag, and:

- **Tag exists in GTM** → leave `CFI_GA4_ID` empty. Nothing more to do.
- **No tag in GTM** → either add one there, or set `CFI_GA4_ID` to the measurement ID in
  `functions.php`.

Also: statewide production carries an orphaned `GTM-MZ6RZ94` `<noscript>` iframe with no head
loader — a leftover from when the site was cloned from CFI's Divi build. It only ever affected
visitors with JavaScript off. Deliberately not carried over.

### Site Kit — decided: not carried over (4 Aug)

Asked and answered. It is not reinstalled on either new site.

Why: its main job on these sites is inserting the GA4 tag, which GTM now does from the theme —
running both double-counts every session. What remains is a read-only dashboard of tools we open
directly anyway. It is the largest plugin in the old stack, it ships releases every couple of
weeks, and it stores an OAuth token to the Google account in the WordPress database, which is a
worse prize for an attacker than the site itself (Site Kit ≤1.24 had a privilege-escalation bug
that let any subscriber become a Search Console owner). The rebuild's whole premise is that the
theme does this work with no plugin layer.

**The dependency this creates, and the fix.** Neither production site emits a
`google-site-verification` meta tag, so Search Console verification is currently anchored to DNS,
an uploaded HTML file, or the GA/GTM tag — possibly to the Site Kit connection itself. If it is
the last of those, dropping the plugin costs verification exactly when the sitemap needs
submitting.

So before cutover: **add a DNS TXT verification for each domain as a Domain property.** It is
permanent, independent of every plugin and tag, and covers www, non-www, and subdomains at once.
Confirm the existing method under Search Console → Settings → Ownership verification first;
leave Site Kit installed on the old production site until after cutover, since removing it early
has no upside.

---

## Rollback

**Choose the reversible cutover method and rollback is minutes, not a restore.** If the domain's
document root is repointed and the old install is left on disk, reverting means pointing it back
— the Divi site is still sitting there, untouched, with its own database. That is the whole
reason to avoid "push to live", which overwrites production and makes the backup the only way
home.

What is genuinely safe either way:

- **Form submissions.** Cognito stores entries on its servers. Nothing is lost regardless of
  which site is live.
- **URLs.** They match production 1:1 — that is what the permalink fix was for — so a revert
  does not create a second round of URL changes.
- **Content.** Everything new lives in this repo and in the new install's database.

What a revert does not undo:

- **Crawling that already happened.** Minor when URLs are identical: the old pages return and
  Google re-crawls what it already knows.
- **Time.** Reverting in the first few days is close to a non-event. Reverting after a month
  means the site has been through two rounds of change instead of none, and rankings settle
  twice. Decide inside the first week or two.

**Trigger conditions — revert rather than debug live** if: forms stop delivering and are not
fixed within an hour; Ads conversions read zero for a full day; a material share of top pages
404; or Search Console reports a coverage collapse rather than the normal post-migration
wobble. Anything cosmetic gets fixed forward, not reverted.

**Watch daily for two weeks:** Search Console coverage and Core Web Vitals, GA4 sessions against
the same week last month, Ads conversion volume and cost per conversion, and the 404 log.
