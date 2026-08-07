# Post-launch audit — California, ~4 hours after cutover

Run 6 Aug 2026 ~22:45 PDT, against the live apex. Scoped deliberately to **things that can affect
Google ranking**, not performance — performance is in `PERFORMANCE.md` and is settled.

Went live at **18:41 PDT**. This audit is roughly four hours later.

---

## Clean — verified, not assumed

| Check | Result |
|---|---|
| Sitemap URLs, all fetched | **62/62 return 200** |
| Canonical tag on each | **62/62 self-referential** |
| `noindex` leaks on indexable pages | **0** |
| JSON-LD schema present | **62/62** |
| Meta description present | **62/62** |
| Stray staging hostname in rendered HTML | **0** |
| Prune redirects | **20/20 301s + 18/18 410s firing** |
| `www.` → apex | **301** |
| `http://` → apex | **301** |
| `new.californiafloodinsurance.com` | **301 → apex** |
| statewide staging still `noindex` | **confirmed** (`nofollow, noindex`) |
| `/sitemap.xml` (advertised in robots.txt) | **301 → `/sitemap_index.xml`** — resolves |

**The `new.` subdomain is not a duplicate-content risk.** It 301s to the apex, so there is no second
crawlable copy of the site. That was the thing most likely to cost ranking and it is fine. It should
still be removed on schedule (~6 Sept, `LAUNCH.md` item 10b) because the *name* will mislead someone
later — but it is not urgent and not an SEO problem.

---

## One real defect: production `robots.txt` is still the Divi-era file — **RESOLVED, see correction below**

> **CORRECTION, 8 Aug.** The diagnosis in this section was wrong and the fix in it should not be
> followed. **Rank Math was not the cause.** Its field was empty and its dynamic output was already
> correct, including the PDF rule. The served content came from a **stale nginx page-cache entry**
> holding the Divi site's robots.txt — verified: no physical `robots.txt` exists in the docroot, checked
> in File Manager with hidden files shown, in the folder confirmed by `DB_NAME mrtaco5_wp441`.
> **A cache purge fixed it**, and the correct output is now live and independently re-verified (PDF rule
> present, `sitemap.rss` gone, `farmerflood` gone, `sitemap_index.xml` returns 200).
>
> **Do not paste anything into Rank Math's box.** Leave it empty; purge instead.
>
> The reasoning error is worth keeping: my own wire test said "dynamic response" from the start — no
> `Last-Modified`, no `ETag`, no `Accept-Ranges`, `x-proxy-cache: HIT`, matching a WordPress page and not
> matching a static file on the same host. I had that measurement and talked myself out of it because
> Rank Math's settings screen carries a generic notice about physical `robots.txt` files. **A generic
> warning in a plugin UI is weaker evidence than a header you measured yourself.**
>
> The lasting lesson: **robots.txt is a cached page.** It served the old site's crawl directives for four
> hours after cutover because nobody thinks to purge or check it. Added to the statewide checklist.

Served on production:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-content/themes/farmerflood/flood_quote/ca-flood-backup.csv
Disallow: /commercial/

Sitemap: https://californiafloodinsurance.com/sitemap.xml
Sitemap: https://californiafloodinsurance.com/sitemap.rss
```

What the new theme intends, confirmed by fetching statewide staging, which runs the same code:

```
User-agent: *
Disallow: /wp-admin/
# Claim PDFs are deliverables, not search results — the pages hold the same content.
Disallow: /wp-content/uploads/*.pdf
Allow: /wp-admin/admin-ajax.php

Sitemap: .../sitemap_index.xml
```

The theme adds the PDF rule through a `robots_txt` filter in `inc/htaccess.php:127`. **That filter is
running on staging and not reaching production output**, which means something later in the chain is
replacing the whole file — almost certainly **Rank Math's robots.txt editor holding custom content
carried over from the Divi site.** Rank Math replaces the output rather than appending to it.

### Why it matters, in order

1. **The claim-PDF exclusion is not in effect.** That was a deliberate SEO decision — a PDF result
   carries no navigation, no CTA and no phone number, so it converts far worse than the page holding
   the same content. Right now those PDFs are crawlable on production and competing with their own
   pages. This is the only item here with a real ranking consequence.
2. **`Sitemap: .../sitemap.rss` returns 404.** Search Console will log a sitemap fetch error against
   the property. Cosmetic in ranking terms, but it is a red error in a report someone will read.
3. Two dead `Disallow` lines. `farmerflood` is the **old Divi theme** and that path 404s;
   `/commercial/` only 301s. Neither does anything. The `farmerflood` line also advertises the
   historical existence of a lead-backup CSV to anyone who reads robots.txt — worth removing on
   hygiene grounds alone.

### The fix

**Rank Math → General Settings → Edit robots.txt.** Replace the stored content with:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# Claim PDFs are deliverables, not search results — the pages hold the same content.
Disallow: /wp-content/uploads/*.pdf

Sitemap: https://californiafloodinsurance.com/sitemap_index.xml
```

If the field is empty, the file is physical — look for `robots.txt` in the docroot and delete it so
WordPress serves the virtual one.

Verify with `curl -s https://californiafloodinsurance.com/robots.txt`. Expect the PDF line present
and no `sitemap.rss`.

---

## A false positive from my own audit script, recorded so it is not re-raised

The first pass reported `/commercial-flood-insurance/` as "in the sitemap but blocked by robots.txt."
**That was wrong.** My check used a substring match; robots.txt uses **prefix** matching, and
`/commercial-flood-insurance/` does not start with `/commercial/`. The page is crawlable and fine.

Same class of error as the `preflight.py` nav/footer bug and the missing `re.S` earlier in this
project: the tool was wrong, not the site. **Confirm a finding against the actual matching rules
before reporting it.**

---

## What this audit did not cover

**Search Console's own reports.** Index coverage, the video indexing issue, and any manual actions
can only be read in GSC. Worth a look once Google has recrawled — give it a few days.

**Field Core Web Vitals.** The 28-day CrUX window is still almost entirely Divi. The new site's own
field data lands around **4 September**. Divi was **failing** CWV on both form factors with a desktop
CLS of 0.2; new-site lab CLS is 0 on every run.

**Whether the 62 sitemap URLs are the *right* 62.** This checked that everything in the sitemap works,
not that nothing is missing from it. `preflight.py` covers URL parity and was run before the flip.


---

# The Divi archive rescue, and an open conversion question — 8 Aug

## The Integration boxes held nothing that needed migrating

Extracted read-only from the dead Divi install (`DB_NAME mrtaco5_wp_2b1xy`, table prefix
**`F01Hh8gh_`** — not `wp_`, worth remembering). All four Integration toggles were `on`;
`single_top` and `single_bottom` were enabled but empty.

| Box | Bytes | What is actually in it |
|---|---|---|
| `divi_integration_head` | 2,849 | GTM loader **424 B** + font preloads 371 B + a CLS `<style>` 860 B + an a11y `<script>` 1,146 B |
| `divi_integration_body` | 1,134 | GTM `<noscript>` **245 B** + a second a11y `<script>` 794 B |

**Tracking is ~15% of it.** The container is exactly `GTM-MZ6RZ94` in both, one container, no second
measurement ID of any kind. Pattern-matched for `GTM-`, `G-`, `AW-`, `UA-`, `DC-`, Bing UET, Facebook,
Clarity, Hotjar, LinkedIn, TikTok, Twitter, Pinterest and HubSpot: **the only hit across all 3,983 bytes
was that single GTM container.** No hardcoded gtag. Nothing non-Google. The only two hosts referenced
are `googletagmanager.com` and the site's own domain.

**So nothing was lost at cutover from the Integration boxes.** That was the question the rescue existed
to answer, and it could not have been answered without doing it.

### Where the Divi custom code lives, if it is ever wanted again

An extracted text file was built by an agent and "downloaded", but it never reached Aaron's machine —
almost certainly into the agent's own sandbox. **It was not worth recovering**, because the source is
still on disk and the content turned out to be non-portable. Retrieval details, so September is not a
hunt:

| | |
|---|---|
| Install | `/home/mrtaco5/californiafloodinsurance.com/` (the **dead Divi** folder) |
| Database | `mrtaco5_wp_2b1xy` |
| Table prefix | **`F01Hh8gh_`** — not `wp_` |
| Custom CSS | `F01Hh8gh_options`, `option_name = 'et_divi'`, key `divi_custom_css` (8,661 bytes, MD5 `b848daf7922aba626faa9d9173e1c2f2`) |
| Same CSS, mirrored | `F01Hh8gh_posts`, **post ID 6**, `post_type = 'custom_css'` — byte-identical |
| Integration code | same `et_divi` option, keys `divi_integration_head` / `_body` |

Reaching it needs phpMyAdmin, **not** the WordPress admin — the hosting manager's Login button on that
install opens the *live* site instead. Read `option_value` as binary (`CONVERT(... USING binary)`);
character-offset extraction is silently 2 bytes short because the CSS contains multi-byte characters,
and it is stored with CRLF line endings.

**Extract it before the install is deleted, or accept losing it.** Given none of it is portable, losing
it is a defensible choice — but it should be a choice, not an accident.

## The rest of it is obsolete by construction

The other ~3,200 bytes are patches, two of them tagged as AI-authored (`claude-a11y-fixes v10`, and an
"Agentic browsing a11y fix"). They are:

- a fixed-header CLS reservation forcing `#page-container{padding-top:176px !important}` so Divi's late
  JS setting the same value caused no shift;
- `aria-label` repair on "Read More" links and a `tabindex` fix on a Pojo accessibility skip link;
- preloads for two self-hosted OMGF fonts (Open Sans, Montserrat).

**None of it is portable and none of it should be copied.** The CSS targets `#page-container`,
`#et-top-navigation`, `#top-menu`, `.et_pb_section_0`; the JS keys off `et-main-area` and Pojo markup.
None exist in Kadence. The fonts are not the new fonts (Inter / Source Serif 4).

More to the point, **the new theme scores Accessibility 100 and lab CLS 0 without any of it.** These
patches are a record of problems the rebuild solved outright, not work to carry forward. Read them as
documentation, then leave them in the archive.

## RESOLVED IN PART, 8 Aug — and my proposed fix would have broken something

**The "Get a Quote" action is not California's. It is Jump Trucking's.**

Its Webpages report attributes recent conversions to `jumptruckinginsurance.com`, on
`/commercial-auto-liability`, `/owner-operator-insurance` and `/small-fleet-trucking-insurance`. **No
California URL appears in it.** Setup is "Manual event", Enhanced Conversions on, managed through the
Google tag, and there is **no element-click or URL rule inside Google Ads** — so nothing in Ads was
firing it for California either.

**My proposed fix was dangerous and was stopped at the gate.** I had suggested reusing label
`juS4CKXmyYUcENeo0OID` in a new `__awct` tag in `GTM-MZ6RZ94`, to "repair California's conversion and
preserve its history". That would have pointed California's quote form at a **working Jump Trucking
conversion action**, corrupting a live conversion on a third brand. The agent declined to act on it
without confirmation and was right to.

**The lesson:** an action's *name* is not evidence of what fires it, and neither is its label. The
Webpages report is. I reasoned from the name ("Click the Get a Quote button on Homepage... We dont have
subdomain") and built a plan on it.

### So California has exactly one quote conversion: the GA4 import

`californiafloodinsurance.com - Submit_Online_Quote_Form` imports the GA4 event
**`Submit_Online_Quote_Form_Submission`**, which is a key event.

### RESOLVED 8 Aug — and it refutes my own prediction

Daily GA4 counts across the boundary:

| Date | `Submit_Online_Quote_Form_Submission` | `quote_form_lead` | `form_submit_any` |
|---|---|---|---|
| Jul 30 – Aug 5 | 17, 13, 5, 8, 18, 19, 9 = **89** | 0 | 0 |
| **Aug 6 — cutover 18:41** | **8** | **2** | **2** |
| Aug 7 (partial) | 0 | 0 | 0 |

**The arithmetic settles it.** Baseline is 89/7 = **12.7 events/day**. Cutover at 18:41 left 5h19m of new
site on 6 Aug — **0.22 of a day**. Expected new-theme events at the old rate: **2.8**. Observed: **2**.
The old event's own 8 that day, across its 18.7 pre-cutover hours, is **10.3/day** — its own baseline.
And 8 + 2 = 10 against a 12.7 average.

**One continuous stream of submissions**, measured by the old event before 18:41 and the new events after.
Rates match.

**So the 8:1 click-inflation theory recorded above was wrong.** It should have been obvious: on a
single-step Cognito form the submit button is clicked **once per submission**, so a click trigger and a
submit trigger count the same event. There was never an inflation ratio to find. **The predicted "90%
drop" is withdrawn.**

**The real problem is worse, not better.** The site is fine and the measurement is fine, but **Ads imports
the old event**, and the old event appears to have stopped at cutover. That is not a decline in a noisy
number — it is California's Ads conversion signal going to **zero** while leads keep arriving at the
normal rate.

One reservation: 7 Aug reads zero across **all four** events including the legacy one, which looks like
reporting lag rather than truth. One further day resolves it. The direction is clear enough to act on.

### Why statewide is safe and California never was

| | California `GTM-MZ6RZ94` | Statewide `GTM-PJQ72VK` |
|---|---|---|
| `__awct` Ads conversion tags | **0** | **4** |
| How the Ads conversion is fed | GA4 **import** of a click-based event | **direct label** from the container |
| Continuity across the flip | **none** | tag 45 (click) and tag 57 (`cfi_form_submit`) send the **same label** |

At statewide's flip the signal simply hands off from one tag to another on the same conversion label.
**Statewide's 344.50/month will not collapse** — that earlier prediction is withdrawn too. California
had no such continuity because its container carries no conversion tag at all.

### The Jump Trucking action, confirmed completely

The full Webpages report for "Click the Get a Quote button on Homepage" is **four of four rows on
`jumptruckinginsurance.com`** — the homepage (56 conversions, 2 tags), `/commercial-auto-liability` (2),
`/owner-operator-insurance` (3), `/small-fleet-trucking-insurance` (2). **No California hostname or path
appears at all.** All 63 conversions are Jump Trucking's. The California-sounding name is legacy
mislabelling and nothing more — worth renaming for hygiene, but it is not California's conversion and must
not be repurposed as one.

### Superseded discrepancy note, kept for the reasoning trail

GA4 property `G-3YMN51H7LE`, last 7 days:

| Event | Count | Key event? |
|---|---|---|
| `Submit_Online_Quote_Form_Submission` | **80** | Yes |
| `quote_form_lead` | **2** | **No** |
| `form_submit_any` | **2** | **No** |
| `Contact_Form_Submission` | 0 | Yes |

80 over 7 days is ~11/day. The theme's own events have produced 2 apiece since 6 Aug. Both cannot be
counting form submissions.

**Reading 1 (likely): the old event is click-inflated.** It fires on `gtm.click` where element text
contains "Submit Application" — intent, not completion. An 8:1 click-to-completion ratio on a quote form
is unremarkable. The equal 2/2 supports it: every submission qualified as a lead, which is what
`inc/cognito.php` should produce.

**Reading 2: the new events are under-firing** and there is a real defect.

**The resolving evidence is DAILY event counts across the 6 Aug boundary.** Requested, not yet answered.

**If Reading 1 holds, California's reported Ads conversions will fall by roughly 90%** when the old
click-based event stops. That is the number becoming honest, not a regression — **written down here in
advance so nobody reads it as a failed cutover.**

**And the same applies to statewide.** Its `Submit_Online_Quote_Form` runs 344.50/month, also ~11/day,
also click-triggered by tag 45. The flip substitutes real-lead counting for click counting, so expect the
same drop. Predicted here in advance.

### Safe regardless of which reading is right

**`quote_form_lead` is not a key event.** Until it is marked as one in GA4 it cannot be imported into
Ads, so the theme is firing the correct event into a dead end. Marking it is additive and reversible, and
it is the prerequisite for any proper fix.

## SUPERSEDED: does California still have a working Ads quote conversion?

Unresolved, and it is the most consequential open item — ahead of anything on the statewide list.

California has **two Primary conversion actions** in the same `Request quotes` goal:

| Action | Source | Label | 30 days |
|---|---|---|---|
| Click the "Get a Quote" button on Homepage | Website | `juS4CKXmyYUcENeo0OID` | **63** |
| californiafloodinsurance.com - Submit_Online_Quote_Form | Website (GA4) | n/a | **143.12** |

**Neither has a confirmed firing mechanism on the new site.**

`juS4CKXmyYUcENeo0OID` is **not in `GTM-MZ6RZ94`** (0 occurrences; the container holds **zero** `__awct`
tags, against statewide's four) and **not inline** on `/`, `/get-a-quote/` or `/contact-us/` — 0 hits for
`juS4CK`, `send_to` or `AW-1012143191`. It is also **not in the Divi Integration code**, which is what
this rescue established. The remaining candidate is an **Ads-side click rule measured by the Google
tag**, configured in Google Ads rather than GTM — the action's own name supports that reading ("Best way
to track Quote form. We dont have subdomain"). If so it rides the Google tag the new site still loads
and may be unaffected; if its click rule keys off Divi markup, it stopped on 6 Aug.

The GA4-imported action is a separate risk. The GTM tag that fires
`Submit_Online_Quote_Form_Submission` triggers on `gtm.click` where element text contains **"Submit
Application"** — Divi-era button text. The theme's own events are `quote_form_lead` and
`form_submit_any`, and **neither appears in the 39-action inventory**, so neither is imported into Ads.
Mitigating factor: the Cognito button text comes from the shared form, not the theme, so that trigger
may still match.

**The decisive test is conversions by day, 30 July to now, per action.** A flatline on or after 7 Aug
confirms it. Requested; not yet answered.

**If it did stop, the fix is small and the theme needs no change** — it is already pushing
`cfi_form_submit`. Either import `quote_form_lead` from GA4 as an Ads conversion, or add one `__awct`
tag to `GTM-MZ6RZ94` triggered on `cfi_form_submit` + `cfi_is_lead`.

## Two account-level problems found on the way

**Statewide will double-count at the flip — confirmed.** Both labels are Primary, both in
account-default goals used by 54 of 60 campaigns. `Submit_Online_Quote_Form` runs **344.50** conversions
while `Contact_Form_Submission` sits at **zero / "Needs attention"**, so tag 46 is not firing today. At
the flip, tag 56 starts firing that dormant label on every lead, so reported statewide quote conversions
roughly **double with no change in real leads.** Fix first: set `Contact_Form_Submission` to Secondary,
or pause tag 56.

**California is already double-counting, today.** A Primary *button click* (63) and a Primary *completed
form* (143.12) feed the same bidding goal. Those are different funnel stages, and Smart Bidding is being
trained as if a click on a homepage button were worth the same as a submitted quote.

Also: **13 Primary actions recorded zero conversions in 30 days**, and there are visible duplicate pairs
outside the flood brands (`Earthquake Insurance - Residential` vs `Earthquake - Residential`, same for
Commercial; three Jump Trucking call actions). Out of scope here, worth a separate pass.


---

# CROSS-SITE CONTAMINATION — California's container runs on Jump Trucking's site

Found 8 Aug while chasing the conversion question. **This is the most consequential finding in the file**
and it changes how every California GA4 number above should be read.

## Confirmed by fetching the pages

`jumptruckinginsurance.com` serves:

```
GTM-MZ6RZ94      <- CALIFORNIA'S container
GTM-PBH839BH     <- Jump Trucking's own container
G-FH3Q6GKNHH     <- STATEWIDE'S GA4 measurement ID, hardcoded in the HTML
```

And `GTM-PBH839BH` contains `juS4CKXmyYUcENeo0OID`, which finally answers what fires the 63 conversions
on the renamed action. It carries four Ads labels and `AW-1012143191`.

## The defect: California's tags are not hostname-scoped

```
tag 27  Submit_Online_Quote_Form_Submission
        e eq gtm.click AND aev cn "Submit Application"
        BLOCK: e eq gtm.js AND u re ^(new|staging)\.
        hostname-restricted (non-block): FALSE
```

The only condition is a block on staging **subdomains** — nothing scopes it to a brand. So a click
anywhere on Jump Trucking's site whose element text contains "Submit Application" fires **California's**
GA4 quote event. That event is a key event and is imported into Ads as
`californiafloodinsurance.com - Submit_Online_Quote_Form`.

Tag 13 (`__googtag` `G-3YMN51H7LE`) fires on All Pages, so **Jump Trucking pageviews also land in
California's GA4 property.**

## This re-explains the 80-vs-2 gap better than either earlier theory

Both of my explanations were wrong. It was not click inflation (withdrawn above) and not the new events
under-firing. It is **contamination**: if most of the ~12.7/day legacy event is Jump Trucking, and
California's honest lead rate is the ~1.3/day the new theme reports, the numbers reconcile exactly.

**Falsifiable prediction, recorded before the data exists.** When 7–8 Aug finishes processing,
`Submit_Online_Quote_Form_Submission` should **still** run 8–19/day, because Jump Trucking has not
changed, while `quote_form_lead` runs 1–3/day. If the legacy event keeps its old rate after California's
theme swap, contamination is proved.

## What is safe, and why

**`quote_form_lead` and `form_submit_any` are uncontaminated by construction.** They fire on
`cfi_form_submit`, which only the new Kadence theme pushes, and only California runs it. So the intended
fix — importing `quote_form_lead` as California's Ads conversion — is clean without any further work.

**Tag 27 is the contaminated one**, and it is the one Ads currently depends on.

## Not fixed here, and needs a decision

Three separate questions, none urgent enough to act on tonight:

1. **Why is California's container on Jump Trucking's site at all?** Either deliberate (one container
   reused across brands) or a copy-paste from a shared header. If deliberate, every non-scoped tag in it
   needs a hostname condition.
2. **How much of California's historical GA4 data is Jump Trucking?** Answerable with a Hostname
   secondary dimension in GA4. Worth knowing before anyone quotes a year-on-year figure.
3. **Statewide's `G-FH3Q6GKNHH` is hardcoded on Jump Trucking's pages**, so statewide's property is
   taking Jump Trucking traffic too — a separate instance of the same problem.

## Correction to ACCOUNTS.md: `purchase` cannot be unmarked

`ACCOUNTS.md` carries an item to unmark `purchase` as a key event on California's property "before the
Ads work". **That is impossible.** GA4 hard-codes a small set of events as permanent key events —
`purchase` among them — and the toggle renders disabled. Verified: 0 events in 30 days, absent from
Realtime.

It is harmless as it stands. The real safeguard is **never importing it into Ads**, not trying to
unmark it. Item withdrawn.
