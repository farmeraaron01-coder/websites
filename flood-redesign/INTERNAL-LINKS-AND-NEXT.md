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
