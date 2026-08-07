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

## OPEN: does California still have a working Ads quote conversion?

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
