# Live-site verification — 20 August 2026

First check against the live sites rather than the June 23 crawl. Method: raw HTML and headers
fetched directly (browser UA + Accept header; a bare `curl` UA gets a 406 from the site's bot
filter), then parsed. Everything below is measured, not inferred.

---

# jumpins.com — 7 of 10 guide items are already done

## Done ✅

| Fix | Verified state |
|---|---|
| **1. robots.txt Crawl-Delay** | **Gone.** The `Crawl-delay: 30` line that throttled Googlebot and the AI crawlers to ~2 pages/min is no longer present. This was the critical blocker. |
| **4. Homepage H1** | **Fixed.** 1 `<h1>` and 2 `<h2>` now render in server HTML (was zero of each). H1: "Jump into better Savings / Jump into better Service / Jump Insurance Agency". |
| **5. Schema** | **Live.** Homepage carries `InsuranceAgency`, `LocalBusiness`, `Organization`, `AggregateRating`, `PostalAddress`, `GeoCoordinates`, `OpeningHoursSpecification`, `ContactPoint`. |
| **6. llms.txt** | **Installed** and serving as a real text file at `/llms.txt` (509 bytes) — not homepage HTML. One content defect, see below. |
| **3. Meta descriptions** | **All 11 target pages now have one.** Every page also has a rewritten title. One defect, see below. |
| **7. Viewport** | **Fixed.** `<meta name="viewport" content="width=device-width, initial-scale=1.0">` — the `user-scalable=0` WCAG 1.4.4 violation is gone. |
| **8. Redirect chain** | **Fixed.** `http://www.`, `https://www.` and `http://` all reach `https://jumpins.com/` in **1 hop** (was a 2-hop chain leaking link equity). |
| **8. Caching** | **Working.** `x-proxy-cache: HIT` (was `DISABLED`). **TTFB 405 ms**, down from 1.01 s. |

## Outstanding ❌

**1. Utility pages are still indexable (Fix 2 not started).** All five sampled return 200 with
**no robots meta at all**: `/slide-anything-popup-preview/`, `/commercial-fast-app/`,
`/life-simple-form/`, `/life-changes-survey/`, `/agent-entered-personal-fast-app/`. ~30 min in
Yoast → per page → Advanced → "Allow search engines to show this page?" → No.

**2. Meta descriptions are all too long — and that was my error.** The first version of
`fixes/meta-descriptions.md` asserted character counts it never measured: **10 of 11 descriptions
were 162–181 characters** while the file claimed 148–155, and they went live at that length.
Google truncates around 155–160, so the tail of each is being cut. The file is now rewritten with
**measured** counts (all ≤160, range 139–153), including the four existing blog posts, which had
the same defect. **These need re-pasting into Yoast.**

**3. `/contact-us/` still carries the Palm Desert title.** Live title is
"Contact Jump Insurance Services | San Diego **& Palm Desert** CA" — a scope violation, from my
original file. Corrected in the repo; the live page needs the re-paste.

**4. Live `/llms.txt` says "San Diego and Palm Desert".** Same scope violation, one line:
`> Independent insurance agency in San Diego and Palm Desert, California.` Should read
`in San Diego, California`. The installed copy is also missing `condo-insurance`,
`boat-insurance`, and the CheapEarthquakeInsurance.com cross-link that `fixes/llms.txt` has.

**5. Security headers still absent (Fix 8, hosting-side).** No `Strict-Transport-Security`, no
`X-Content-Type-Options`, no `X-Frame-Options`, no `Referrer-Policy`. `server: nginx/1.31.1` is
still disclosed (`server_tokens off` not applied). `fixes/nginx-snippet.conf` covers all of it.

**6. xmlrpc pingback still in `<head>`** — Fix 7's WPCode snippet has not been applied.

**7. One page has no H1:** `/business-insurance/trucking-transportation/` returns 0 `<h1>`. The
other ten target pages all have exactly one.

**8. TTFB 405 ms** — a large improvement from 1.01 s, but still above the 300 ms target. Note
`cache-control: max-age=0, no-cache, no-store, must-revalidate` is being sent despite the proxy
cache hitting; worth a look if further gains are wanted.

## Also confirmed

Both FAQ fixes are live and correct — earthquake 4/4 questions and answers visible, flood-zones
5/5, exactly one `FAQPage` block each, heading order matching schema order. See
`jumpins.com/content/README.md`.

---

# cheapearthquakeinsurance.com — clean, no further action

The July GSC alerts are fully accounted for. **No evidence of an active compromise.**

| Check | Result |
|---|---|
| Spam `/products/` URLs (4 sampled + the parent) | **All 404**, zero redirects, identical 21,692-byte 404 page. Nothing spammy is being served. |
| `/products/` parent | 404 |
| Sitemaps | `post-sitemap.xml` 7 URLs, `page-sitemap.xml` 10 URLs — **zero** containing `/products/` |
| robots.txt | Clean Yoast block, `Disallow:` empty, sitemap declared |
| The 4 "403 Forbidden" URLs from the GSC email | 1 still 403, 2 now 301 — all are asset **directories** with browsing disabled. Benign, as diagnosed. |
| Real pages | `/`, `/residential-earthquake-quote/`, `/should-you-buy-earthquake-insurance-in-california/`, `/service/faq/` all 200 and healthy |

Do **not** redirect the 404s and do **not** click "Validate fix" on that GSC report — 404 is the
correct response and Google is dropping them. The remaining issue on this site is the one from the
original triage: real money pages sitting in "Crawled – currently not indexed", which is a
content-quality verdict, not a security problem.

---

# Priority order from here

1. **Revoke the four WordPress application passwords** — `jumpins.com / Admin` first. Outstanding
   since 7 Aug and unrelated to anything above. Also rotate the two Dropbox `.env` files.
2. **Re-paste the 15 meta descriptions** (11 pages + 4 posts) from the corrected file, which also
   clears the Palm Desert title on `/contact-us/`. ~1 hr.
3. **Noindex the 8 utility pages.** ~30 min, pure crawl-budget win.
4. **Fix the one line in the live `/llms.txt`** and add the three missing entries. ~5 min.
5. **Hand `fixes/nginx-snippet.conf` to hosting** for headers + `server_tokens off`, and apply the
   WPCode snippet for the pingback. ~45 min.
6. **Add an H1 to `/business-insurance/trucking-transportation/`.**
