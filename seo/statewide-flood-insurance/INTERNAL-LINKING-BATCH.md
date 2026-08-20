# Internal linking batch — statewidefloodinsurance.com

**Revised 21 Aug 2026. This supersedes the 20 Aug version entirely — that one
was built on a wrong assumption and its predicted numbers were invalid.**

---

## What changed, and why the first version was wrong

The 20 Aug batch said the Related-guides rail hardcoded Texas, Florida, Indiana
and Colorado, and planned to *extend* it so those four kept their 73 inbound
links.

**Nothing is hardcoded.** The rail is a `WP_Query` over pages carrying the
`_cfi_badge` meta key, `orderby => modified`, `posts_per_page => 5`,
`post__not_in => [self]`. Confirmed two ways:

- 69 crawled pages show the identical set — hub, TX, FL, IN, CO
- 5 pages show Nevada substituted, and those 5 are exactly the members of the
  top-5 excluding themselves. Nevada is the sixth most recently modified.

Three consequences:

1. **The 73 inbound is a snapshot, not a structure.** Those four are there
   because they were most recently edited. The hub is at #1 because of *our own*
   Task 1 edit on 19 Aug.
2. **The graph churns on every save.** The 20 Aug batch would have edited ~30
   state pages, making whichever states were touched last the new top four. It
   would have shuffled the concentration, not removed it — and the verification
   numbers would have depended on edit order.
3. **"Extend, don't replace" no longer applies.** Protecting a deliberate
   editorial choice is sound. This is a rotating accident that moves on its own
   the next time anyone saves a page. There is nothing stable to protect.

**Is the rail deliberate?** The `_cfi_badge` gate is an editorial signal —
someone chose which pages are eligible. That part is intentional. But
`orderby => modified` is the generic "keep it fresh" default, not a decision
that those four specific pages belong everywhere. Read: **a curated freshness
sidebar, whose SEO side effect was not intended.** Changing the ordering on
state pages refines that intent rather than breaking it.

---

## Task A — Branch the rail: static neighbours on state pages, query elsewhere

**Skip the `WP_Query` on state pages. Do not run it and append.** Appending
keeps the churn.

```
if ( isset( $neighbour_map[ $slug ] ) ) {
    // state page: hub + hazard neighbours from the map
    // if fewer than 4 neighbours, top up the remaining slots from the
    // existing query so the rail still renders 5 items
} else {
    // everything else: existing WP_Query, completely unchanged
}
```

**Let the map be the state detector** — `isset( $neighbour_map[ $slug ] )`.
Do **not** match on a slug pattern: `commercial-flood-insurance`,
`high-risk-flood-insurance` and `excess-flood-insurance` all end in
`-flood-insurance` and are not states. Do not use a hardcoded ID list either;
with the map as detector, state #31 is one array line and nothing can drift.

**Change the heading on state pages** from "Related guides" to
**"States with similar flood risk."** The rail is no longer a mixed block, and
the old heading now over-promises.

**Touch only the 30 state pages.** The 44 non-state pages that also carry this
rail keep the recency query exactly as-is until that is an explicit decision.

### The neighbour map

Grouped by **flood hazard type**, not shared border. The two mostly coincide
here, but hazard is the rule: New Mexico is Southwest, Michigan is Great Lakes,
Colorado is Front Range flash flood and gets neither Nebraska nor Wyoming.

| Slug | Hazard group | Neighbours |
|---|---|---|
| alabama | Gulf surge | mississippi, louisiana, florida, georgia |
| arizona | SW monsoon / arroyo | new-mexico, nevada, colorado |
| colorado | Front Range flash | new-mexico, oklahoma, arizona |
| connecticut | NE coastal / nor'easter | new-york, massachusetts, new-jersey |
| florida | Gulf + S Atlantic | georgia, alabama, south-carolina, louisiana |
| georgia | S Atlantic | south-carolina, florida, alabama, north-carolina |
| hawaii | Island / tropical | *(none — top up from query; see Task C)* |
| illinois | Miss. basin + Great Lakes | missouri, indiana, michigan, ohio |
| indiana | Ohio basin + Great Lakes | illinois, ohio, kentucky, michigan |
| kentucky | Ohio basin | tennessee, indiana, ohio, missouri |
| louisiana | Gulf surge | mississippi, texas, alabama, florida |
| maryland | Mid-Atlantic tidal | virginia, pennsylvania, new-jersey |
| massachusetts | NE coastal | connecticut, new-york, new-jersey |
| michigan | Great Lakes | ohio, indiana, illinois |
| mississippi | Gulf surge | louisiana, alabama, tennessee, texas |
| missouri | Miss. basin | illinois, kentucky, tennessee, oklahoma |
| nevada | SW monsoon | arizona, new-mexico, colorado |
| new-jersey | NE coastal | new-york, connecticut, massachusetts, pennsylvania |
| new-mexico | SW monsoon / arroyo | arizona, colorado, **nevada**, texas |
| new-york | NE coastal | new-jersey, connecticut, massachusetts, pennsylvania |
| north-carolina | S Atlantic | south-carolina, virginia, georgia, tennessee |
| ohio | Ohio basin + Great Lakes | indiana, kentucky, michigan, pennsylvania |
| oklahoma | Plains flash flood | texas, missouri, colorado, new-mexico |
| oregon | Pacific NW atmospheric river | washington |
| pennsylvania | Mid-Atlantic + Ohio basin | new-york, new-jersey, ohio, maryland |
| south-carolina | S Atlantic | north-carolina, georgia, florida |
| tennessee | Miss./Ohio basin | kentucky, missouri, mississippi, north-carolina |
| texas | Gulf surge + plains flash | louisiana, oklahoma, mississippi, new-mexico |
| virginia | Mid-Atlantic + S Atlantic | maryland, north-carolina, pennsylvania |
| washington | Pacific NW atmospheric river | oregon |

New Mexico lists **Nevada** rather than Oklahoma. Arizona ↔ New Mexico ↔ Nevada
is one arid Southwest flash-flood group; Oklahoma is Plains and belongs with
north Texas and Missouri. That is a better map on its own merits, not a fix to
hit a number.

Validated programmatically: every neighbour resolves to a real slug in the map,
no state lists itself.

---

## Task B — "States we cover" directory on the hub

The hub's private-market table is a **dataset** — only the 27 states with enough
quoted properties. Kentucky, Maryland, Indiana and Nevada have pages but no
data, so no row exists to link them. That is why two of them are orphans.

Add a plain directory list linking **all 30 state pages**.

**Placement: immediately after the private table's closing "The pattern worth
noticing" paragraph, before the "The hidden coverage gap" heading.** Not between
the two tables — the private table opens by referring to *"The table above"*,
and a 30-item list wedged in there breaks a framing we built deliberately.

---

## Task C — Topical routes for the three states the map cannot reach

Hawaii has no hazard neighbour in the book. Oregon and Washington are a genuine
pair of two; Idaho and Montana have no pages. Forcing WA/OR/HI into a
"Pacific-facing" group would be geography-as-bad-proxy — tropical cyclone and
valley flash flood is not atmospheric river.

1. **`/high-risk-flood-insurance/`** — one sentence naming **Hawaii, Oregon and
   Washington** as states whose mapped high-risk areas are driven by hazards
   other than Gulf and Atlantic hurricane surge, linking each state page.
2. **`/excess-flood-insurance/`** — one sentence naming **Hawaii**, where high
   building values put a large share of properties above the NFIP's $250,000
   statutory cap, linking the Hawaii page.

Real sentences that earn their place. Not a bare link list.

---

## Predicted outcome — check against this

State-to-state inbound, excluding the recency rail on non-state pages:

| Metric | Before | After |
|---|---:|---:|
| Orphans | 3 | **0** |
| State pages at exactly 1 inbound | 22 | **0** |
| State pages at 3+ | 4 | **30 of 30** |
| Lowest | 0 | **3** (hawaii, maryland, nevada, oregon, virginia, washington) |
| Highest, excluding recency | — | **6** (new-jersey, new-mexico, ohio, pennsylvania) |
| Texas / Florida / Indiana / Colorado | 73 | **44–49** |

**Why 44–49 and not a single number.** The 44 non-state pages keep the recency
rail, so whoever is top-5 by modified still collects ~44 sitewide links. 49 is
the ceiling, when all four are still top-5. The moment anyone edits a different
badge page one drops out and the figure drifts toward 44. Quote the range.

**Residual churn, deliberately left in place.** The 44 non-state pages still
rotate their five links by recency. The meaningful consequence: **if a state
page ever climbs into the top-5 badge-modified list, it will appear on all 44
non-state pages until the next badge edit.** That is the argument for eventually
switching the non-state rail to a topical query too — but that is a separate
decision about 44 pages, not part of this batch.

`/agent-appointment/` stays an orphan **on purpose**. It is a form-only utility;
whether it should be indexable at all is a separate call.

---

## Verify

Re-crawl every sitemap URL and recount inbound source pages. Do not sample, and
use a unique `?cb=` on each fetch.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
curl -sSL -A "$UA" "https://statewidefloodinsurance.com/sitemap_index.xml?cb=$(date +%s%N)" \
  | grep -oE 'https://[^<]+\.xml' | while read s; do curl -sSL -A "$UA" "$s"; done \
  | grep -oE '<loc>[^<]+</loc>' | sed 's/<[^>]*>//g' | grep -v '\.xml' | sort -u > urls.txt
```

Pass:
- 0 orphans besides `/agent-appointment/`
- every state page at 3 or more inbound source pages
- Texas, Florida, Indiana, Colorado between 44 and 49
- state-page rails show the hazard neighbours, not TX/FL/IN/CO
- non-state page rails **unchanged** — still hub + the four most recent
- rail heading reads "States with similar flood risk" on state pages only
- all 83 URLs still 200

**Re-crawl last, after all edits are saved.** Every save moves the recency
window, so a mid-batch measurement is meaningless.

## Rollback

Task A is a template edit — back up the file (`cp -p <file> <file>.bak-<date>`),
`php -l` after, and remember the theme is **copied, not symlinked**: apply to
both docroots and compare md5. Task B is an additive block on one page. Task C
is two sentences.
