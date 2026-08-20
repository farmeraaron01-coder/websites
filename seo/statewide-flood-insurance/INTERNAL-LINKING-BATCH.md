# Internal linking batch — statewidefloodinsurance.com

Closes the audit's P1 "internal-link authority is distributed unevenly".
Measured baseline, 20 Aug 2026, from a crawl of all 83 sitemap URLs:

- **3 orphans** — `/kentucky-flood-insurance/`, `/maryland-flood-insurance/`,
  `/agent-appointment/`
- **29 pages with exactly one inbound source page**, 22 of them state pages

## Why the distribution is what it is

Not a link-graph problem — a template problem.

| Inbound | Pages | Cause |
|---:|---|---|
| 81 | Commercial, HOA, Excess, High-Risk, Lloyd's | global nav menu |
| 73 | Texas, Florida, Indiana, Colorado | the **same four** hardcoded into every state page's Related guides rail |
| 1 | the other 22 state pages | their hub table row, and nothing else |
| 0 | Kentucky, Maryland | no quote data, so no hub row exists to link them |

The rail is `<aside class="cfi-doc-rail">` in the child theme — `cfi-rail-card`,
`cfi-rail-h`, `cfi-rail-links`, the same `cfi-` convention as `cfi-byline` and
`cfi-doc`. **PHP template, not post content**, so this is one edit per docroot,
not 30 post edits. Remember the theme is copied, not symlinked: apply twice and
compare md5.

**It is a sidebar rail, not body copy.** That fixes crawl paths and
distribution. It does not fully deliver the audit's phrase "contextual inbound
links" — rail links weigh less than in-content ones. Worth being straight about
when judging whether the finding is closed.

---

## Task A — Extend the Related guides rail

**Extend, do not replace.** Keep the existing hub + Texas + Florida + Indiana +
Colorado links exactly as they are. Removing them would drop those four from 73
inbound to roughly 6 — a real hit on the pages currently ranking best, for no
gain. Add 3–4 hazard neighbours *below* the existing links. Rail goes from 5
links to 8–9.

Grouping is by **flood hazard type**, not by shared border. For this book the
two mostly coincide, but the rule is hazard: New Mexico is Southwest not Plains,
Michigan is Great Lakes not "Ohio and Indiana", Colorado is Front Range flash
flood and gets neither Nebraska nor Wyoming.

| State | Hazard group | Add these neighbours |
|---|---|---|
| Alabama | Gulf surge | Mississippi, Louisiana, Florida, Georgia |
| Arizona | SW monsoon / arroyo | New Mexico, Nevada, Colorado |
| Colorado | Front Range flash | New Mexico, Oklahoma, Arizona |
| Connecticut | NE coastal / nor'easter | New York, Massachusetts, New Jersey |
| Florida | Gulf + S Atlantic | Georgia, Alabama, South Carolina, Louisiana |
| Georgia | S Atlantic | South Carolina, Florida, Alabama, North Carolina |
| Hawaii | Island / tropical | *(none — see Task C)* |
| Illinois | Miss. basin + Great Lakes | Missouri, Indiana, Michigan, Ohio |
| Indiana | Ohio basin + Great Lakes | Illinois, Ohio, Kentucky, Michigan |
| Kentucky | Ohio basin | Tennessee, Indiana, Ohio, Missouri |
| Louisiana | Gulf surge | Mississippi, Texas, Alabama, Florida |
| Maryland | Mid-Atlantic tidal | Virginia, Pennsylvania, New Jersey |
| Massachusetts | NE coastal | Connecticut, New York, New Jersey |
| Michigan | Great Lakes | Ohio, Indiana, Illinois |
| Mississippi | Gulf surge | Louisiana, Alabama, Tennessee, Texas |
| Missouri | Miss. basin | Illinois, Kentucky, Tennessee, Oklahoma |
| Nevada | SW monsoon | Arizona, New Mexico, Colorado |
| New Jersey | NE coastal | New York, Connecticut, Massachusetts, Pennsylvania |
| New Mexico | SW monsoon / arroyo | Arizona, Colorado, Nevada, Oklahoma |
| New York | NE coastal | New Jersey, Connecticut, Massachusetts, Pennsylvania |
| North Carolina | S Atlantic | South Carolina, Virginia, Georgia, Tennessee |
| Ohio | Ohio basin + Great Lakes | Indiana, Kentucky, Michigan, Pennsylvania |
| Oklahoma | Plains flash flood | Texas, Missouri, Colorado, New Mexico |
| Oregon | Pacific NW atmospheric river | Washington |
| Pennsylvania | Mid-Atlantic + Ohio basin | New York, New Jersey, Ohio, Maryland |
| South Carolina | S Atlantic | North Carolina, Georgia, Florida |
| Tennessee | Miss./Ohio basin | Kentucky, Missouri, Mississippi, North Carolina |
| Texas | Gulf surge + plains flash | Louisiana, Oklahoma, Mississippi, New Mexico |
| Virginia | Mid-Atlantic + S Atlantic | Maryland, North Carolina, Pennsylvania |
| Washington | Pacific NW atmospheric river | Oregon |

Give the added group its own sub-heading in the rail so it reads as deliberate
rather than as a longer list — e.g. **"States with similar flood risk"**.

---

## Task B — "States we cover" directory on the hub

The hub's private-market table is a **dataset**, covering only the 27 states
with enough quoted properties. Kentucky, Maryland, Indiana and Nevada have pages
but no data, so no row exists to link them. That is why two of them are orphans.

Add a plain directory list of **every state page**, linking all 30.

**Placement: immediately after the private table's closing "The pattern worth
noticing" paragraph, before the "The hidden coverage gap" heading.**

Not between the two tables. The private table opens by explicitly referencing
*"The table above reports NFIP premiums… this one reports something
different"* — a 30-item link list wedged in there breaks a framing we built on
purpose. After the pair, the list is still main content, still around 40% down
the page, and reads as the natural "now go to your state" step.

---

## Task C — Topical routes for the three states the map cannot reach

Hawaii has no hazard neighbour in the book. Oregon and Washington are a genuine
pair of two; Idaho and Montana have no pages. Forcing a Pacific-facing group of
WA/OR/HI would be geography-as-bad-proxy — tropical cyclone and valley flash
flood is not atmospheric river.

Route the missing links through pages where the mention is genuine:

1. **`/high-risk-flood-insurance/`** — one sentence naming **Hawaii, Oregon and
   Washington** as states whose mapped high-risk areas are driven by hazards
   other than Gulf and Atlantic hurricane surge, linking each state page.
2. **`/excess-flood-insurance/`** — one sentence naming **Hawaii**, where high
   building values put a large share of properties above the NFIP's $250,000
   statutory cap, linking the Hawaii page.

Write both as real sentences that earn their place. Do not add a bare link list.

---

## Predicted outcome — check against this, do not accept "it looks better"

| Metric | Before | Predicted after |
|---|---:|---:|
| Orphans (0 inbound) | 3 | **0** |
| State pages with 1 inbound | 22 | **0** |
| State pages at 3+ inbound | 4 | **30** |
| Lowest state page | 0 | **3** (Hawaii, Maryland, Nevada, Virginia) |
| Texas / Florida / Indiana / Colorado | 73 | **76–77** (no loss) |

`/agent-appointment/` stays an orphan **on purpose**. It is a form-only utility.
Decide whether it should be indexable at all rather than inventing links to it —
that is a separate decision, not part of this batch.

---

## Verify

Re-run the full crawl and recount inbound source pages. Do not sample.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
curl -sSL -A "$UA" "https://statewidefloodinsurance.com/sitemap_index.xml?cb=$(date +%s%N)" \
  | grep -oE 'https://[^<]+\.xml' | while read s; do curl -sSL -A "$UA" "$s"; done \
  | grep -oE '<loc>[^<]+</loc>' | sed 's/<[^>]*>//g' | grep -v '\.xml' | sort -u > urls.txt
# then fetch each with a unique ?cb= and count, for every page, how many OTHER
# sitemap pages link to it.
```

Pass: 0 orphans besides `/agent-appointment/`; every state page at 3 or more;
Texas, Florida, Indiana and Colorado still above 70; all 83 URLs still 200.

## Rollback

Task A and C are content/template edits — back up the template file first
(`cp -p <file> <file>.bak-<date>`) and `php -l` after. Task B is an additive
block on one page; deleting the block reverts it.
