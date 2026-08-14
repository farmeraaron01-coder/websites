# Statewide's Zone X page is redirected to the wrong page — 14 Aug 2026

**This is the largest single defect found in this project, and it is not a slow
page. It is a page that has been switched off.**

## What is happening

`statewidefloodinsurance.com/navigating-flood-zone-x/` returns **301 to
`/high-risk-flood-insurance/`**.

Zone X is the zone **outside** the Special Flood Hazard Area. It is the low-risk
designation. The redirect target is titled *"Flood Insurance for High-Risk &
Hard-to-Place Homes"*, runs 883 words, and mentions:

| term | mentions on the target page |
|---|---:|
| "Zone X" | **0** |
| "shaded" | 0 |
| "X500" | 0 |
| "optional" | 0 |
| "not required" | 0 |

So every visitor asking what the low-risk zone means is being sent to a page about
hard-to-place high-risk homes that never mentions their zone.

## The scale of it

Search Console, statewide, twelve months, that URL:

- **360 queries, 10,055 impressions, 10 clicks.**
- That is **seven times** California's zone-X traffic.
- Average position **46.7** — page five.

The queries it is failing on:

| query | impressions | position |
|---|---:|---:|
| flood zone x | 1,112 | 46.7 |
| fema zone x | 426 | 25.0 |
| flood insurance zone x | 416 | 55.7 |
| what is flood zone x | 362 | 52.6 |
| what is fema zone x | 337 | **10.9** |
| zone x flood insurance | 313 | 46.2 |
| flood zone x shaded | 237 | 59.3 |
| is flood insurance required for zone x | 212 | 55.7 |
| what is flood zone x500 | 185 | 82.7 |
| does flood zone x require flood insurance | 184 | 63.8 |
| does zone x500 require flood insurance | 164 | 79.6 |

A page ranking 10.9 on 337 impressions while redirecting to unrelated content is
Google still holding a position it is about to lose.

## Where the redirect came from

Not the child theme — checked. It is a migration decision: `CONTENT-AUDIT.md`
records 125 links repointed during the Divi-to-Kadence move, consolidating
`/which-flood-zone-requires-flood-insurance/` into `/high-risk-flood-insurance/`.
That consolidation was reasonable. Sending **Zone X** to the same target was not,
and it looks like the same rule applied one slug too far.

The redirect itself is not in code I can see. It is in Rank Math redirections,
`.htaccess`, or the statewide database.

## The fix

1. **Remove the redirect.** Zone X must not point at a high-risk page.
2. **Give statewide a real Zone X page.** California's version is 1,428 words,
   ranks **7.8**, and already covers shaded versus unshaded properly. Statewide has
   seven times the demand and no page at all.
3. **Cover Zone X500 explicitly.** 349 impressions on X500 queries at positions 80+
   and 237 on "flood zone x shaded". X500 is the older FIRM designation for shaded
   Zone X — the 0.2% annual chance floodplain. People search the code; pages explain
   the concept without ever printing the term.
4. **Answer the requirement question in one sentence.** 396 impressions across "is
   flood insurance required for zone x" and "does flood zone x require flood
   insurance", at positions 55 to 64. The answer is one line and belongs at the top.
5. **Add the lookup tool.** The shortcode is already deployed on statewide.

## Already done on California, same diagnosis

California's Zone X page explained shaded versus unshaded well and ranked 3rd to
6th for those phrasings — but **never printed "X500"**, and
"does zone x500 require flood insurance" sat at 34.7. Fixed: the designation is now
named in the text, a direct one-sentence answer to the requirement question was
added at the top of that section, and the page links to the lookup tool.

## Blocked

**I cannot edit statewide.** The California application password returns 401 there —
separate WordPress install, separate credentials. Everything above is analysis;
none of the statewide work can proceed without access.
