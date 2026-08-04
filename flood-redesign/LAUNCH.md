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
| 1 | ~~Install theme v1.3.8~~ — **done 4 Aug, verified on both sites.** Page role, submit event, and the host gate all confirmed live | — | ☑ |
| 1b | ~~Install v1.3.9~~ — installed, but its approach cannot work: **nginx serves `/wp-content/uploads/` directly**, so no `.htaccess` rule reaches the PDFs | — | ☑ |
| 1c | Install **v1.4.0** — keeps the PDFs out of search via robots.txt instead, the one mechanism that works without the host | Aaron | ☐ |
| 2 | ~~Confirm whether the GTM containers hold a GA4 config tag~~ — **done 4 Aug: they do. `CFI_GA4_ID` stays empty.** | — | ☑ |
| 2b | **GTM pass**: repoint the **GA4 event tags** (and statewide's native Ads tags) to `cfi_form_submit` / `cfi_is_lead`, retire the Click Text triggers | Aaron | ☐ |
| 2g | **Same pass, Bing**: the flood UET goals are click goals too (`CALIFORNIA Submit Button Click`, `STATEWIDE Submit Form Click`), so staff intake inflates Bing as well. Add a UET event tag on `cfi_form_submit` and switch the goals to Event type — snippet in ACCOUNTS.md | Aaron | ☐ |
| 2c | ~~Resolve where CFI's Ads conversions come from~~ — **done 4 Aug: GA4-imported key events.** Confirm the Source column when convenient | — | ☑ |
| 2e | Decide whether to apply the **July 15 conversion-tracking cleanup plan** (60 actions, dozens Primary across six brands) — still marked DRAFT. Sequenced in ACCOUNTS.md stage 3c: after the GTM repoint, and **not in the same week as the cutover** so the two effects stay separable | Aaron | ☐ |
| 2f | Optional: point the flood ads at **/get-a-quote/** instead of the homepage — the new landing page puts the form on the page the click lands on | Aaron | ☐ |
| 2d | Copy out Divi → Theme Options → Integration head/body code before the theme goes (low risk — every tag was found arriving through GTM) | Aaron | ☐ |
| 3 | Verify tags fire on staging: any page + `?cfi_tags=1`, logged in as admin, with Tag Assistant | Claude | ☐ |
| 4 | Sign off content: 9 statewide articles, 10 claims pages, 18 drafted meta descriptions | Aaron | ☐ |
| 5 | Sign off statewide palette and hero copy | Aaron | ☐ |
| 6 | Correct the four "separate purchases" instances in the source PDFs (copy supplied; sites already fixed) | Aaron | ☐ |
| 7 | **Add a DNS-verified Domain property for each site in Search Console** — neither flood site has one today (CFI has `https://` + `http://www.` URL-prefix only; statewide `https://` + `http://`), and statewide's HTML-file verification dies with the docroot swap | Aaron | ☐ |
| 7c | **Open `GTM-PJQ72VK`'s two "Urgent" container-quality issues** and read what they are — statewide's container, unexamined, before launch | Aaron | ☐ |
| 7d | Remove stale GTM publish access (2022 freelancer Gmail addresses); downgrade the two active agencies to Edit — see ACCOUNTS.md step zero | Aaron | ☐ |
| 7b | Note a baseline week of GA4 pageviews — the number legitimately drops when Site Kit's duplicate tag goes | Aaron | ☐ |
| 8 | **Full backup of each production site — files + database — downloaded off the server** | Aaron | ☐ |
| 9 | Confirm the cutover method with InMotion (see *Rollback*) — docroot swap, not overwrite | Aaron | ☐ |

Not launch-blocking, decide later: the asymmetric-lanes / cross-domain canonical question for
the duplicated claims content.

Account naming and structure cleanup — the GTM/GA4/Ads/Search Console tidy-up — is in **ACCOUNTS.md**.
Its stage 1 (renames) is zero-risk and can happen any time. Its stage 3 overlaps this runbook's GTM
pass and should not run in the cutover week.

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
- **Submit the staff form as a test and confirm NO conversion is recorded — on Google Ads AND Bing.**
  In GTM Preview the push should read `cfi_form_role: "staff"`, `cfi_is_lead: false`, with both the
  Ads and UET tags showing as not fired. This is the regression that was live on both platforms
  before v1.3.7.
- Confirm the quote submission fires **one** conversion action, not two — the old `Click Text
  contains "SUBMIT"` trigger could also match "Submit Application".
- **PDF exclusion:** `curl /robots.txt` → contains `Disallow: /wp-content/uploads/*.pdf` inside the
  `User-agent: *` group. Do **not** expect an `X-Robots-Tag` header on the PDFs — nginx serves that
  directory off disk and Apache never sees the request. This check earned its place twice: it caught
  the original rule landing in the root `.htaccess`, then caught the per-directory version being
  equally unreachable.
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
- Ask InMotion for two nginx changes in one ticket:
  1. Exclude `/wp-json/` from the nginx cache (authenticated REST responses are currently cached,
     which is why purges needed a REST write to trigger — and why a theme-version check read stale).
  2. Add `add_header X-Robots-Tag "noindex, noarchive";` to the `/wp-content/uploads/` location for
     `.pdf` files. This is the complete version of what robots.txt approximates: robots.txt stops
     crawling, the header stops indexing. Neither is urgent; together they close it properly.

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

Theme v1.3.6+ prints the GTM snippet **only on the production hostname**, so staging cannot send
data. That matters less for GA4 pageviews than for Ads conversion tags, where one test
submission counts as a real lead and feeds Smart Bidding a fake conversion. At cutover the
hostname becomes the production one and tagging starts by itself — there is no step to forget.
To test before then: `?cfi_tags=1` on any page while logged in as an administrator.

**`CFI_GA4_ID` stays empty — settled 4 Aug.** Both containers already hold a Google Tag named
"GA4 - Page Views" firing on All Pages: `G-3YMN51H7LE` in `GTM-MZ6RZ94`, `G-FH3Q6GKNHH` in
`GTM-PJQ72VK`, each matching its property's data stream. GA4 therefore runs through GTM and the
theme must not print gtag as well.

**Which means production is double-counting GA4 today.** The GTM Google Tag configures the
measurement ID *and* Site Kit prints its own gtag config for the same ID on every page. Dropping
Site Kit removes the duplicate.

> **Expect GA4 sessions and pageviews to fall after cutover, with no real traffic loss.** This is
> the duplicate going away, not the new site underperforming. Before flipping, note a baseline
> week of GA4 pageviews and check DebugView for two `page_view` events on one load so the size of
> the drop is known in advance. Judge the migration on Search Console impressions, Ads conversion
> volume, and phone calls — not on GA4 session counts across the cutover line.

Also: statewide production carries an orphaned `GTM-MZ6RZ94` `<noscript>` iframe with no head
loader — a leftover from when the site was cloned from CFI's Divi build. It only ever affected
visitors with JavaScript off. Deliberately not carried over.

### Conversion tracking — what the container audit found (4 Aug)

Three problems, all live on production now. Theme v1.3.7 fixes the site half; the GTM half needs
one pass in Tag Manager.

**1. The staff form is being counted as a paid lead.** `/staff-form/` embeds **form 5 — the same
Cognito form as the public quote page** — and its button carries the same "Submit Application"
label. Statewide's Ads conversion `Submit_Online_Quote_Form` triggers on *All Elements → Click
Text contains "Submit Application"*, so it cannot tell the two apart: every phone call the office
types into the staff form registers as a Google Ads conversion. That is exactly the pollution the
staff form was given its own noindexed URL to prevent. Verified in the DOM — the seamless embed
renders in the parent document with no iframe, so the click listener does see it.

**2. The triggers count clicks, not submissions.** A click trigger fires when the button is
pressed, including when validation rejects the form and no entry is created. Conversions inflate
and Smart Bidding optimises toward people who never finish.

**3. Two conversion actions may fire on one submission.** `Contact - Form Submission` triggers on
*Click Text contains "SUBMIT"*. `innerText` reflects CSS `text-transform`, so an uppercase-styled
button can report `SUBMIT` — and "Submit Application" contains "Submit". Whether both fire depends
on the trigger's case sensitivity. Check it in GTM Preview on the quote page.

#### The site half — theme v1.3.7

`[cfi_cognito]` now emits one explicit event on a genuinely successful submission:

```js
dataLayer.push({
  event: 'cfi_form_submit',
  cfi_form_id: '5',
  cfi_form_role: 'quote',   // quote | staff | service | claims | appointment | other
  cfi_is_lead: true         // false for staff intake, service, claims, appointments
})
```

Detected two ways, both verified to exist in Cognito's own bundle: `Cognito.on('afterSubmit')`,
and a MutationObserver watching for the `cog-confirmation` node that replaces the form after an
entry is accepted. Whichever fires first wins and a flag stops the other reporting twice. Tested
against the live staging form: the confirmation path fires and dedupes correctly, and neither DOM
churn nor a submit click that fails validation produces an event.

Fail-safe: role comes from the form id, but **any page whose slug contains "staff" is forced to
`role=staff`, `cfi_is_lead=false`** regardless of the shortcode. Forgetting an attribute cannot
turn staff intake into a paid conversion. The PPC landing page was also switched from a hardcoded
embed to the shortcode, so the page the Ads spend points at emits the same event.

#### The GTM half — Aaron, before cutover

1. Create a Custom Event trigger: event name `cfi_form_submit`, condition `cfi_is_lead` **equals**
   `true`. (Register `cfi_is_lead`, `cfi_form_role`, and `cfi_form_id` as dataLayer variables.)
2. Repoint the Ads conversion tags to it and **remove the Click Text triggers.**
3. Add a second GA4 event on `cfi_form_submit` *without* the is_lead condition, with
   `cfi_form_role` as a parameter — staff and service volume stays measurable in GA4 while never
   reaching Ads.
4. Do the same for the Bing UET tags (`Bing UET - request_quote` is Custom HTML and likely carries
   the same click fragility).
5. **CFI's conversions come from GA4, so the GA4 event tags are what must be repointed.**
   Resolved 4 Aug from the June/July Ads project files plus a runtime check. There is no rogue
   page-level Ads tag: `AW-1012143191` loads *through* GTM, from the Google Ads Remarketing tag
   firing on All Pages, which is also why GTM shows a "missing Google tag" nag. And CFI has no
   Ads conversion tag in the container — but the Ads account does hold conversion actions named
   `californiafloodinsurance.com - Contact_Form` (Submit Lead Form) and
   `californiafloodinsurance.com - Submit_Online…` (Request Quote). That `<domain> - <event>`
   naming, plus the GA4↔Ads link in place since Nov 2022, plus GA4 event tags in the container
   with exactly those names, means these are **GA4 key events imported into Ads**.

   Consequence for the GTM pass: on CFI, repointing only the Ads tags would change nothing,
   because there are none. **Repoint the GA4 event tags** (`Submit_Online_Quote_Form_Submission`,
   `Contact - Form Submission`) to `cfi_form_submit` — that is the whole fix for CFI. On statewide,
   repoint the GA4 event tags *and* the two native Ads conversion tags. While there, check whether
   statewide double-counts: it has native Ads conversions *and* the same GA4 events that CFI
   imports, so the same submission may be landing twice.

   Confirm in **Google Ads → Goals → Conversions** — the Source column should read Google
   Analytics 4 for the CFI pair.
6. Divi's Integration boxes are worth a glance, but the runtime check found **every tag arriving
   through GTM** (`AW-1012143191`, `G-3YMN51H7LE`, Bing UET via `bat.bing.com`) with no
   independent page-level tag on either site. So the only thing known to live in Divi's header is
   the GTM snippet itself, which the theme now replaces. Copy the boxes out anyway before the
   theme goes — cheap, and it is the last chance to see them.

Untouched, noted for completeness: statewide GA4 has a **second, orphaned property** (371465506 /
`G-NCF8CTTSQS`, stream `https://statewidefloodinsurance.com`, no data, no Ads link). Leave it
alone — just never point anything at that measurement ID. Both live streams also have `http://`
stream URLs; cosmetic, worth updating to `https://` while you are in there.

### What the Ads project files established (Dropbox, read 4 Aug)

From `/Aaron Farmer/Claude CoWork Files/google-ads-project/` — the June UTM work and the 15 July
account audit. Everything here was already known; it just was not written down anywhere the
migration could see it.

**Lead delivery does not touch WordPress.** Cognito form 5 posts to a webhook at
`cfi.insuranceclouds.com/Raters/Flood/JSONSubmit.aspx` plus three emails: `quote@…`, the Zapier
parser (`floodcognito@robot.zapier.com`), and InsuredMine (`data@insuredmine.com`). So the runbook's
claim that submissions survive any cutover or rollback is not just true of the entries — the whole
delivery path is external. **Nothing about the migration can break lead delivery.**

**Form 5 is shared four ways.** CFI's quote page, statewide's quote page, and *both* staff forms all
submit the same form (org key `8nmcIcFF1k6xZNCBaOzZxQ`). The prefill tag stamps `SourceWebsite` with
the hostname, which separates California from Statewide — but **not** staff intake from a real web
lead. Theme v1.3.8 publishes `cfi_page_role` early in the head so the existing prefill tag can write
it into a hidden "Lead Type" field on form 5, giving the CRM the same separation v1.3.7 gives Ads.
Worth doing at the same time as the GTM pass.

**Still open from June, unrelated to the migration but worth closing:** form 5 has
`IncludeHiddenFields: false`, so the captured UTM/GCLID values never appear in the emails Zapier and
InsuredMine read. They are on the entry and in the rater webhook, invisible to sales. Fix is a
checkbox on each of the two integration emails.

**The Cognito prefill tag survives cutover unchanged.** It carries UTMs across pages in
`sessionStorage` because ads land on the homepage while the form lives on `/get-a-quote/`. Nothing
about it depends on the theme — which is also the argument for pointing the ads at `/get-a-quote/`
instead: the new landing page puts the form on the page the click lands on, so the cross-page carry
stops being load-bearing at all.

**The 15 July audit's headline finding is still open and still bigger than anything here.** 60
conversion actions, dozens Primary across six unrelated brands, so flood campaigns bid partly toward
non-flood conversions and every CPA is directional. Its plan is still marked DRAFT. That fix and
this one are complementary: the cleanup plan decides *which signals count*, v1.3.7/v1.3.8 fix
*whether the signals are true*. Doing the cleanup on top of a feed that counts staff intake and
failed validations would just optimise toward cleaner garbage.

> **Security, unrelated to launch:** `google-ads-project/Google Ads/.env` holds the Google Ads
> developer token, client secret, and refresh token in a synced Dropbox folder. I did not open it.
> A refresh token is a durable credential to the whole Ads account — worth moving out of Dropbox
> and rotating.

### Site Kit — decided: not carried over (4 Aug)

Asked and answered. It is not reinstalled on either new site.

Why: its main job on these sites is inserting the GA4 tag, which GTM now does from the theme —
running both double-counts every session. What remains is a read-only dashboard of tools we open
directly anyway. It is the largest plugin in the old stack, it ships releases every couple of
weeks, and it stores an OAuth token to the Google account in the WordPress database, which is a
worse prize for an attacker than the site itself (Site Kit ≤1.24 had a privilege-escalation bug
that let any subscriber become a Search Console owner). The rebuild's whole premise is that the
theme does this work with no plugin layer.

Leave Site Kit installed on the old production site until after cutover — removing it early has
no upside.

### Search Console verification — statewide is the exposure (checked 4 Aug)

Verification is **not** anchored to Site Kit on either site, so dropping the plugin is safe. But
the two sites are anchored differently, and one of them breaks at cutover:

| | CFI | Statewide |
|---|---|---|
| Properties | `https://californiafloodinsurance.com/` and `http://www.californiafloodinsurance.com/`, URL-prefix only | `http://statewidefloodinsurance.com/` and `https://statewidefloodinsurance.com/`, URL-prefix only |
| Verified by | **DNS TXT** ("Domain name provider") | **HTML file upload** |
| Survives a docroot swap? | Yes — DNS is independent of the filesystem | **No** |

**Statewide's verification lives in a file in the production docroot.** Swap the docroot and the
file is gone, which un-verifies the property at the moment the sitemap needs submitting. Two ways
to fix, do the first:

1. **Add a Domain property for each site, verified by DNS TXT** (Add property → Domain → TXT
   record at the DNS host). Permanent, filesystem-independent, and covers www, non-www, http and
   https in one property. CFI already has the DNS record proving ownership — Search Console even
   shows the banner about it — so adding the Domain property there is a click plus a record.
2. Failing that, copy the `google*.html` verification file into the new install's docroot before
   flipping, and keep it out of any cleanup.

Also worth doing while there: **CFI's www property is `http://`, not `https://`.** For a site that
canonicalises to `https://` non-www, that property is the wrong shape to be reading data from — a
Domain property replaces both and is the cleaner answer. Submit the sitemap to the Domain property
once it exists.

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
fixed within an hour; Ads conversions read zero for a full day (check first that the GTM container
was published — an unpublished container looks identical to a broken site); a material share of top pages
404; or Search Console reports a coverage collapse rather than the normal post-migration
wobble. Anything cosmetic gets fixed forward, not reverted.

**Watch daily for two weeks:** Search Console coverage and Core Web Vitals, Ads conversion volume
and cost per conversion, phone call volume, and the 404 log.

**Do not use GA4 session counts as the health check across the cutover line.** They will drop
because production currently double-counts every pageview (GTM's Google Tag plus Site Kit's gtag,
same measurement ID) and the duplicate goes away with Site Kit. Compare GA4 to itself only after
the first full post-cutover week. Conversion *rate* will also appear to improve for the same
reason — the denominator was inflated.
