# Search Console report — California, pulled 13 Aug 2026 via API

Pulled with `tools/gsc-pull.py` against `sc-domain:californiafloodinsurance.com` using the service account
Aaron created (`sc-domain-californiafloodinsur@fluted-reporter-499120-j4`, `siteRestrictedUser`, read-only).

**The key never entered a chat transcript.** It was written straight from Dropbox to a temporary download URL
to disk with `curl -o`, outside the repository, then deleted after the pull. Only its non-secret fields were
ever printed: type, project id, client email.

---

## ⚠ THE FINDING THAT REFRAMES EVERY NUMBER EITHER ANALYSIS PRODUCED

**The Domain property holds nine days of data. Not ninety.**

Requesting a full year returns nine rows:

```
requested 2025-08-01 .. 2026-08-11  ->  9 days returned
earliest day with data: 2026-08-03
latest  day with data:  2026-08-11
```

So the property was verified around 3 Aug and **did not backfill**. Everything below is **3–11 Aug**.

### This resolves the 15,479-versus-1,245 argument completely, and neither side was wrong

| Figure | Scope | Verdict |
|---|---|---|
| **15,479** impressions | `http://www…` **URL-prefix** property, "Last 3 months" | correct for that property |
| **1,245** impressions | **Domain** property — which only has 9 days | correct for that window |
| **1,406** impressions (this pull) | Domain property, 3–11 Aug, the `www` page row | agrees with 1,245 |

**Both numbers were real. The window label was wrong** — Kimi's table was presented as "May 12–Aug 11" when the
property cannot serve data before 3 Aug. An hour of disagreement traceable to a date range, which is why
`gsc-pull.py` now stamps site and range into every CSV header.

**Consequence: nobody has long-window per-page data yet.** To get it, add the same service account email to the
**`https://californiafloodinsurance.com/` URL-prefix property**, which does hold full history.

---

## The head terms, 3–11 Aug

### "flood insurance california"

| Position | Impr | Clicks | Page |
|---|---|---|---|
| **3.8** | 445 | 10 | apex `/` |
| **8.7** | 290 | 4 | **`www` `/`** |
| 18.5 | 74 | 1 | `/flood-insurance-rates/` |
| **1.1** | 29 | **0** | **`/mobile/contact.php`** |
| 9.1 | 9 | 0 | `/contact-us/` |
| **99.5** | 2 | 0 | `/california-flood-insurance-quotes/` |

### "california flood insurance"

| Position | Impr | Clicks | Page |
|---|---|---|---|
| **1.1** | 139 | 8 | apex `/` |
| **6.4** | 137 | 7 | **`www` `/`** |
| **4.4** | **130** | **0** | **`/contact-us/`** |
| 2.4 | 66 | 0 | `/residential/` |
| **2.6** | 53 | **0** | **`/mobile/contact.php`** |
| **85.0** | 2 | 0 | `/california-flood-insurance-quotes/` |

### Scorecard against the two analyses

**Kimi was right, I was wrong:** the homepage outranks `/contact-us/` on both terms — 1.1 vs 4.4 and 3.8 vs 9.1.
My claim came from a single live SERP snapshot, which is personalised and volatile. A 90-day average beats a
snapshot and I should not have asserted a ranking from one.

**Kimi was right and I under-called it: `/mobile/contact.php` is ranking.** Positions **1.1 and 2.6**, 82
impressions across the two head terms, zero clicks. I called a 301 "optional, low value" — the data says do it
promptly. Both facts hold at once: the URL **404s** (confirmed in headless Chromium) *and* Google still shows it,
because recently-removed URLs linger in the index. **301 it to `/contact-us/`** — the redirect fires from
`.htaccess` before the file lookup, so the missing file is irrelevant.

**My findings that the data confirms:**

- **`/contact-us/` holds position 4.4 with 130 impressions and zero clicks.** A page-1 slot returning nothing.
- **`/california-flood-insurance-quotes/` sits at 85.0 and 99.5 with 2 impressions.** 3,885 words, 2 internal
  links, effectively not in the index. The orphan diagnosis was right and is now quantified.

**The `www` split — both figures were right, different denominators:**

| Measure | Value |
|---|---|
| `www` share of **all** impressions | **7%** (1,177 of 16,154) |
| `www` share of **"flood insurance california"** | **39%** (290 of 735) |
| `www` share of **"california flood insurance"** | **50%** (137 of 276) |

My 7% and Kimi's ~40% are the same data at different scopes. **The split is worst exactly where it matters
most** — the two most valuable queries on the site. The redirect and canonical are already correct, so the
remaining fix is the GBP signal (changed 13 Aug) plus time.

---

## Top pages, 3–11 Aug — 210 clicks on 29,915 impressions, CTR 0.70%

| Impr | Clicks | Pos | Page |
|---|---|---|---|
| 2,866 | 20 | 18.1 | `/how-much-does-flood-insurance-cost/` |
| 2,306 | 14 | **7.9** | `/which-flood-zone-requires-flood-insurance/` |
| 1,976 | 7 | **7.8** | `/navigating-flood-zone-x/` |
| 1,789 | 35 | 14.1 | `/` |
| 1,686 | 6 | 14.6 | `/flood-zone-ae/` |
| 1,445 | 12 | 25.5 | `/flood-insurance-rates/` |
| 1,406 | 17 | **7.0** | `http://www…/` |
| 1,272 | **0** | 28.3 | `/commercial-flood-insurance/` |
| 1,252 | 11 | **6.7** | `/how-much-flood-insurance-is-required-by-lender/` |
| 1,086 | 1 | 37.1 | `/residential/` |

**The CTR problem is now the main event.** Two pages sit at position ~7.9 with 2,306 and 1,976 impressions and
earn 14 and 7 clicks — around 0.6% and 0.35%. Titles are verified correct in source and rendered, so the title
theory is dead. **Kimi's remaining explanation is the live one: AI Overviews and featured snippets absorbing the
click on informational queries.** That makes the ranking work and the AI-citation work the same work, which is
the most useful conclusion of the whole exchange.

---

## The address cluster, precisely

**60 distinct queries, 673 impressions, ZERO clicks, positions ~5–10.**

| Impr | Pos | Query | Page that ranks |
|---|---|---|---|
| 70 | 9.1 | 525 b street san diego fema flood zone | `/san-diego-flood-insurance/` |
| 62 | 9.2 | 55 south market street san jose fema flood zone | `/san-jose-flood-insurance/` |
| 60 | 9.0 | 700 wilshire los angeles fema flood zone | `/los-angeles-flood-insurance/` |
| 42 | 9.9 | 9725 scranton road san diego flood zone | `/san-diego-flood-insurance/` |
| 41 | 7.9 | 4701 north first street san jose fema flood zone | `/san-jose-flood-insurance/` |
| 32 | 5.2 | 414 w bedford fresno fema flood zone | `/fresno-flood-insurance/` |
| 31 | 8.5 | 8915 complex drive san diego fema flood zone | `/san-diego-flood-insurance/` |

Absorbed by: San Diego 218, San Jose 189, Los Angeles 117, Fresno 45, `/flood-zone-ae/` 45,
`/which-flood-zone-requires-flood-insurance/` 40, Stockton 18.

**Every address is commercial** — 525 B Street and 1402 K Street in downtown San Diego, 55 S Market and 4701 N
First in San Jose, 700 Wilshire and 600 W 7th in downtown LA, 8915 Complex Drive and 9725 Scranton Road in
Kearny Mesa, 2030 Fortune Drive. Office towers and business parks, not houses. **Escrow officers, lenders and
commercial brokers with live transactions.**

### Why it earns zero clicks, and what that means for the product

The city pages rank but **do not answer the question asked.** Somebody wants the flood zone for *one specific
address*; the page offers a city overview. That is a content-match failure, not a ranking failure — which is
precisely why a lookup tool wins the cluster instead of more city copy.

**But one caution, or the tool underperforms too.** Zero clicks at position ~9 is also consistent with Google
answering in-SERP via its own map panels. If so, a tool that merely returns the zone competes with an answer the
searcher already has. **The tool's value has to be the thing the SERP cannot give a person mid-transaction:**

- a **lender-ready document** — zone determination with the map panel and date, as a PDF
- a **same-day quote** for that address
- a **certificate or elevation-certificate path** where one is needed

Escrow officers do not need to know the zone. They need documentation that closes the file. Build that and the
cluster converts; build a zone lookup alone and it may draw the same zero.

---

## What to do, in order

1. **301 `/mobile/contact.php` → `/contact-us/`.** Positions 1.1 and 2.6 currently pointing at a 404. Upgraded
   from "optional" on the strength of this data.
2. **Strip the flood content off `/contact-us/` and retitle it plainly.** Position 4.4, 130 impressions, zero
   clicks.
3. **Fix the orphaned money pages' internal links.** `/california-flood-insurance-quotes/` at 85–99.5 with 2
   impressions is not in the race.
4. **Add the service account to the `https://` URL-prefix property** so long-window data exists. One click, and
   it stops both analyses guessing at windows.
5. **Build the address tool as a document generator, not a lookup.** Highest upside on the site.
6. **Investigate the CTR gap** on the two ~position-8 pages — check the live SERP for AI Overviews on those
   queries. If confirmed, the fix is citability, not on-page.

**Not** the `www`/`http` redirect rules. They already work; the split is consolidation lag.

---
---

# REAL 90-DAY DATA — the URL-prefix properties, pulled after access was granted

Aaron added the service account to `https://californiafloodinsurance.com/` and
`https://statewidefloodinsurance.com/`. **Both hold 468 days of history.** Everything above this line was nine
days; everything below is **13 May – 11 Aug 2026**. Where they disagree, this section wins.

**California: 835 clicks, 142,616 impressions, CTR 0.59%, 132 pages.**
**Statewide: 103 clicks, 24,955 impressions, 77 pages.**

## ⚠ THE CTR THEORY WAS BUILT ON A NINE-DAY ARTEFACT. Both of us were wrong.

Kimi proposed, and I endorsed, that AI Overviews were absorbing clicks because two pages sat at **position ~8
with 0.4–0.7% CTR** — anomalously low for page one. Over 90 days:

| Page | Impressions | Position (9d) | **Position (90d)** | CTR |
|---|---|---|---|---|
| `/navigating-flood-zone-x/` | 14,882 | 7.8 | **11.3** | 0.39% |
| `/which-flood-zone-requires-flood-insurance/` | 11,739 | 7.9 | **12.3** | 0.82% |

**They are on page two, not page one.** At position 11–12, sub-0.5% CTR is roughly what you would expect — the
anomaly that needed explaining does not exist. The nine-day window (3–11 Aug) simply flattered them.

That changes the action. **The fix is ranking, not citability** — move them from page two to page one. AI
Overviews may still compress clicks on informational queries, but there is no longer evidence of it here, and
"be the source AI quotes" is no longer justified *by this data*. It remains worth doing on its own merits; it is
just not the answer to a CTR problem that turns out not to be one.

## The single biggest opportunity, and Kimi identified it first

| Impressions | Clicks | Position | CTR | Page |
|---|---|---|---|---|
| **2,866** | 20 | **18.15** | 0.70% | `/how-much-does-flood-insurance-cost/` |
| 16,290 | 244 | 12.3 | 1.50% | `/` |
| 14,882 | 58 | 11.3 | 0.39% | `/navigating-flood-zone-x/` |
| 11,739 | 96 | 12.3 | 0.82% | `/which-flood-zone-requires-flood-insurance/` |
| **7,326** | 8 | **31.4** | 0.11% | `/commercial-flood-insurance/` |
| **7,268** | 6 | **43.6** | 0.08% | `/residential/` |
| 7,093 | 24 | 18.0 | 0.34% | `/flood-zone-ae/` |
| 5,382 | 30 | 11.7 | 0.56% | `/how-much-flood-insurance-is-required-by-lender/` |
| 4,711 | 37 | 36.0 | 0.79% | `/flood-insurance-rates/` |
| 3,888 | 40 | 19.6 | 1.03% | `/contact-us/` |

The cost page is the **largest impression pool on the site** and sits on page two. `/commercial-flood-insurance/`
and `/residential/` each draw over 7,000 impressions at positions 31 and 44 — enormous demand, no visibility.

## THE REDIRECT DECISION — answered, and the answer is "don't"

This is why the plan said not to redirect anything before pulling this report.

**`/california-flood-insurance-quotes/` — 90 queries, 1,505 impressions, 2 clicks.** It is not competing with the
homepage at all; it owns a **distinct quote-intent cluster** the homepage does not target:

| Impressions | Position | Query |
|---|---|---|
| 296 | 35.4 | flood insurance quotes |
| 141 | 60.4 | flood insurance quote |
| 119 | 85.4 | online flood insurance quote |
| 110 | 50.4 | private flood insurance quote |

**Do not merge it.** 1,505 impressions on a real cluster, held back by 2 inbound internal links and positions of
35–85. Differentiate the title toward quote intent and give it internal links. The orphan diagnosis is confirmed;
the merge is ruled out.

**`/cheap-flood-insurance-california/` — 0 queries, 0 impressions, 0 clicks.** 3,730 words earning literally
nothing, ranking for no query at all. *This* is the consolidation candidate, not the quotes page.

## The head terms, 90 days

**"flood insurance california"** — 6,724 impressions, 40 clicks

| Position | Impr | Clicks | Page |
|---|---|---|---|
| **4.8** | 5,540 | 35 | `/` |
| 19.3 | 175 | 4 | `/flood-insurance-rates/` |
| **1.4** | 170 | **0** | **`/mobile/contact.php`** |
| 7.1 | 119 | 0 | `/contact-us/` |

**"california flood insurance"** — 4,876 impressions, 73 clicks

| Position | Impr | Clicks | Page |
|---|---|---|---|
| **1.2** | 1,333 | 69 | `/` |
| **6.0** | **1,158** | **1** | **`/contact-us/`** |
| 11.2 | 395 | 1 | `/how-much-does-flood-insurance-cost/` |
| **9.8** | 395 | **0** | **`/mobile/contact.php`** |

**Confirmed: the homepage is page one on both — 4.8 and 1.2.** My "getting to page 1" framing was wrong, and
Kimi was right to reject it.

**`/contact-us/` is the real waste, and larger than the nine-day view suggested:** position 6.0 with **1,158
impressions and 1 click** on the head term. Sitewide it is a healthy page (19.6, 1.03% CTR) — the problem is
specific to that query.

**`/mobile/contact.php`: Kimi was right and I was wrong twice.** 565 impressions across the two head terms, zero
clicks, **position 1.4** on one of them, pointing at a 404. I called the 301 "optional, low value" on two separate
occasions. **Do it.**

## The address cluster — three times bigger than the nine-day estimate

**107 distinct queries, 2,034 impressions, ZERO clicks, positions ~7–10.**

| Impressions | Position | Query |
|---|---|---|
| 235 | 9.9 | 525 b street san diego fema flood zone |
| 199 | 7.5 | 3807 coronado ave stockton ca fema flood zone |
| 96 | 7.4 | 4701 north first street san jose fema flood zone |
| 85 | 9.1 | 55 south market street san jose fema flood zone |
| 81 | 8.9 | 9530 towne centre drive san diego fema flood zone |

Absorbed by: San Diego 667, San Jose 336, Fresno 296, Stockton 270, Los Angeles 205,
`/which-flood-zone-requires-flood-insurance/` 150.

**Statewide has zero address queries.** The cluster is California-only.

### The device split confirms who these people are

| Device | Impressions | Clicks | CTR | Position |
|---|---|---|---|---|
| **Desktop** | **91,214** | 491 | 0.54% | 17.9 |
| Mobile | 28,123 | 327 | 1.16% | 13.0 |

**76% desktop**, and desktop converts at half the mobile rate from worse positions. That is consistent with
Kimi's escrow-desk thesis: commercial address lookups happen at a desk, mid-transaction, during business hours.
It also means the address tool is a **desktop** product — wide layout, printable output, copy-paste address entry
— not a mobile-first one.

## Statewide, for contrast

103 clicks on 24,955 impressions, desktop average position **36.3**. Top pages:
`/navigating-flood-zone-x/` 3,209 impressions at **43.2**, `/texas-flood-insurance/` 2,329 at 24.8,
`/commercial-flood-insurance/` 1,482 at **72.6**. A freshly flipped site with little authority — real demand
reaching it, almost no visibility. Not tonight's problem, but it argues against spreading effort thin: California
has 5.7× the impressions and a far better position profile.

## Revised order of work

1. **301 `/mobile/contact.php` → `/contact-us/`.** Position 1.4 pointing at a 404.
2. **Fix `/contact-us/` for the head term** — strip the flood content, retitle plainly. 1,158 impressions at
   position 6 earning one click.
3. **Push `/how-much-does-flood-insurance-cost/` from 18.15 toward page one.** 2,866 impressions is the largest
   pool on the site. This is now the top content priority, above the head terms themselves.
4. **Internal links to `/california-flood-insurance-quotes/`** and differentiate it toward quote intent. Do NOT
   redirect it.
5. **Decide what `/cheap-flood-insurance-california/` is for** — 3,730 words, zero impressions.
6. **Build the address tool as a desktop document generator.** 2,034 impressions, zero clicks, 76% desktop.
7. **Investigate `/commercial-flood-insurance/` and `/residential/`** — 7,326 and 7,268 impressions at positions
   31 and 44.

**Dropped from the plan:** the AI-Overview CTR remedy, as an answer to *this* data. The pages are on page two.
