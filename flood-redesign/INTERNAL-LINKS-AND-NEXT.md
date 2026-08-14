# Internal links, measured — and what to do next. 14 Aug 2026

Crawled all 62 URLs in the sitemap and counted **body** links only, excluding
header, footer and nav. Then joined that to 12 months of Search Console.

## My notes were wrong about the linking

| page | inbound body links | claimed in old notes |
|---|---:|---|
| `/get-a-quote/` | 110 | 534 |
| `/how-much-does-flood-insurance-cost/` | **70** | — |
| `/loss-of-use-coverage-in-flood-insurance/` | 54 | — |
| `/contact-us/` | **38** | 123 |
| `/california-flood-insurance-quotes/` | **1** | 2 |
| `/cheap-flood-insurance-california/` | **1** | 2 |

The old 123 and 534 figures counted site-wide template navigation as internal
links. Counting only editorial body links, the contact page has 38 — still a lot,
but not the anomaly it looked like. **And the cost page already has 70 inbound
links, so "the flagship is under-linked" was never true.**

## The orphans are not worth rescuing

| page | 12-month impressions | clicks | position |
|---|---:|---:|---:|
| `/cheap-flood-insurance-california/` | **0** | 0 | — |
| `/california-flood-insurance-quotes/` | 283 | 1 | 49.8 |
| `/residential/` | 1,086 | 1 | 37.1 |

`/cheap-flood-insurance-california/` has earned **zero impressions in twelve
months.** Not few — none. Google has looked at it and declined to show it to
anybody. Adding internal links to a page in that state is pouring effort into
something the index has already judged.

**So the planned link repair is cancelled as scoped.** Both reviews endorsed it and
I was about to do it; the measurement says the premise was wrong.

## The real cannibalization is somewhere else entirely

| page | impressions | clicks | position |
|---|---:|---:|---:|
| `/how-much-does-flood-insurance-cost/` | 2,866 | 20 | 18.2 |
| `/flood-insurance-rates/` | 1,445 | 12 | 25.5 |

**Two pages, both about what flood insurance costs, 4,311 impressions between
them, neither on page one.** That is a genuine split of the same intent, and it is
evidenced rather than inferred — unlike the contact-page theory, which the data
mostly cleared. This is the consolidation candidate.

Now that the cost page carries measured figures and a methodology, it is clearly
the stronger of the two. The rates page should either merge into it or be narrowed
to a genuinely different question.

## The biggest opportunity is the zone cluster, and we are already winning it

| page | impressions | clicks | position |
|---|---:|---:|---:|
| `/navigating-flood-zone-x/` | 1,976 | 7 | **7.8** |
| `/flood-zone-ae/` | 1,686 | 6 | 14.6 |

Nearly **3,700 impressions at page-one and near-page-one positions** — the best
positions on the site outside the homepage. And it matches the query data exactly:
the flood-zone cluster is 31.4% of all impressions, larger than the cost cluster.

It also matches the *shape* of the demand. The top place-name queries are address
lookups — "525 b street san diego fema flood zone". People want to know what zone a
specific address is in. That is a tool, not an article, and it is what the NFHL
geocoding work was always pointing at.

## Recommended order

1. **Consolidate `/flood-insurance-rates/` into the cost page.** Evidenced, and the
   cost page is now the stronger asset. Redirect rather than delete.
2. **Build the zone/address lookup.** Biggest cluster, best existing positions,
   clearest unmet intent, and it is the one thing on this site a competitor cannot
   copy in an afternoon.
3. **Leave the orphans alone.** Revisit only if something changes.

## Still open elsewhere

- All-states aggregates predate the WA/OR/AZ tax rates (needs 90 workbooks).
- wp-includes PHP 404 hardening rule, due 18 Aug.
- Sober living start-here page.
- Softaculous install records on statewide.

---

# MERGE EXECUTED — `/flood-insurance-rates/` → cost page, 14 Aug 2026

## The evidence that justified it

Twelve months of Search Console, query-level:

- Rates page ranked for **132 queries**; cost page for **220**.
- **102 of the rates page's 132 queries also ranked on the cost page** — a 77%
  overlap of the same intent across two URLs.
- On nearly every shared query the cost page ranked **better**:

| query | rates page | cost page |
|---|---:|---:|
| cost of flood insurance | p70.0 | **p21** |
| how much does flood insurance cost per year | p72.4 | **p16** |
| flood insurance rates | p46.6 | **p27** |
| zone ae flood insurance rates | p58.0 | **p37** |

- Queries unique to the rates page: **30, worth 52 impressions in a year.**

So the rates page was not holding ground the cost page could not take. It was
ranking worse on the same terms and contributing almost nothing of its own.

## The reason it became urgent

The rates page was publishing figures that **contradicted the rebuilt cost page**:

| rates page claimed | cost page measures |
|---|---|
| "California overall average: about $780 per year" | NFIP median **$1,244** |
| Zone X "as low as roughly $350 per year" | X/B/C median **$1,082** |

Neither of the rates figures was sourced. Two live pages disagreeing about price,
on a site publishing premium data under a licence, is a worse problem than the
ranking split — and it is the exact failure mode § 790.03(b) describes.

## What was done

1. **Theme redirect, v1.6.2.** A second `template_redirect` hook, because the
   existing one fires only on `is_404()` and a published page never 404s. Carries
   a self-redirect guard. **Requires Aaron to upload the theme.**
2. **Contradicting figures removed from the live rates page immediately**, without
   waiting for the upload — the $780 and $350 claims are gone and the page now
   cites the measured medians. Verified live.
3. **Four internal body links repointed** to the cost page, so they do not route
   users through a redirect: `/excess-flood-insurance/`, `/residential/`,
   `/resources/`, `/before-a-flood/`. Verified at 0 remaining references in raw
   content.
4. **Menu items checked: none.** The remaining on-page links come from dynamically
   generated related-guides lists, which the 301 will handle.

## Not done, and deliberately

The `rank_math_canonical_url` meta did not store — it is not a registered REST
field. Left alone rather than worked around, because the 301 supersedes a
canonical entirely once the theme ships. If the upload is delayed more than a few
days, set the canonical by hand in Rank Math as an interim.

## Rollback

Delete the entry from `cfi_merged_redirect_map()` and the page returns
immediately. The pre-merge content is backed up session-locally; the figure
corrections should stand regardless, since they were wrong on their own terms.

## VERIFIED LIVE after upload of 1.6.2 — 14 Aug 2026

| check | result |
|---|---|
| `/flood-insurance-rates/` | **301 → /how-much-does-flood-insurance-cost/** |
| same without trailing slash | **301 → same target** |
| cost page itself | 200, zero redirects — no loop |
| 15 other pages (with trailing slash) | **all 200** |
| `/mobile/contact.php` (the older 404 map) | still 301 → `/` |
| a genuine missing URL | still 404 |
| the four repointed pages | all now link to the cost page |

**The check that actually mattered** was not the redirect — it was the fifteen
other pages. The new hook matches on the request path *before* the 404 test, so a
mistake in the map would take a working page down with no error anywhere. All
fifteen return 200, and the pre-existing 404-based map is untouched.

One thing worth recording so it is not misread later: probing those paths *without*
a trailing slash returns 301 for every one of them. That is WordPress's own
`redirect_canonical` adding the slash, not our redirect. Testing without the slash
and reading the 301s as collateral damage would have been an easy false alarm.

Merge complete.
