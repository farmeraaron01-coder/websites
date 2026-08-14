# Statewide's loss-of-use page: a page-one URL redirected into a dead one

**Status: page written and published (post 266). One `.htaccess` line still has
to come out before anyone can see it.**

This is the second instance of the same defect found on statewide, and it was
found the same way — by reading the `.htaccess` file rather than by trusting the
redirect list in Rank Math, which does not contain either rule.

## What the rule was doing

```apache
Redirect 301 /loss-of-use-coverage-in-flood-insurance/ /flood-coverage-gaps/
```

Twelve months of Search Console, 14 Aug 2025 – 11 Aug 2026:

| URL | clicks | impressions | avg position |
|---|---|---|---|
| `/loss-of-use-coverage-in-flood-insurance/` | 17 | **2,554** | **6.5** |
| `/flood-coverage-gaps/` | 0 | 3 | 5.0 |

The redirect source is a page-one asset. The destination has three impressions in
a year and **not one ranking query** — the query breakdown for it comes back
empty.

It is worse than the totals suggest, because the source ranks on exactly the
queries this agency sells against:

| query | impressions | position |
|---|---|---|
| private flood insurance loss of use coverage | 68 | **3.6** |
| does flood insurance cover loss of use | 49 | 5.7 |
| does private flood insurance include loss of use coverage | 29 | **2.8** |
| does private flood insurance cover loss of use | 28 | 3.8 |
| nfip does not cover additional living expenses loss of use | 15 | 4.9 |

Top-four on four separate buying-intent queries about the single coverage
difference Aaron identifies as the most important thing he sells. Every click on
them landed on `/flood-coverage-gaps/` — 806 words that use the phrase "loss of
use" **zero times** and "additional living" once, in a passing heading.

17 clicks on 2,554 impressions is a 0.67% click-through rate at an average
position of 6.5, where several percent would be normal. Some of that is the
redirect showing Google a mismatched destination; the rest is that the people who
did click found a page that did not answer them.

## Why the redirect could not simply be deleted

The page did not exist any more. Searched posts and pages on statewide with
`status=any`: nothing at that slug. Removing the rule first would have turned a
page-one URL into a 404, which is worse than the redirect.

So the order matters, and it is the same two-step already used for Zone X:

1. **Create the page at the exact slug.** Done — post 266, published.
2. **Then remove the redirect.** Aaron's step, below.

## The page

`/loss-of-use-coverage-in-flood-insurance/`, 2,419 words, published 14 Aug 2026.
Substantiation in `SUBSTANTIATION-loss-of-use.md`.

It is **not** a copy of the California page. Statewide has state pages for
twenty-eight states, so:

- the displacement-cost table is fourteen metros across that footprint — Mobile
  at $1,083 a month for a two-bedroom through New York at $2,910 — rather than
  California counties;
- the California-specific IA declaration count is left off, because it does not
  hold nationally;
- the one California example that stayed (the Pajaro shelter) is named as
  California rather than presented as typical.

Structure follows the query cluster rather than a template. The direct answer is
the first sentence, before any heading, because that is what gets extracted:
*"No. A standard NFIP flood policy from FEMA covers no loss of use, no additional
living expenses and no temporary housing of any kind."*

Two sections earn their place beyond the obvious:

- **The take-up mechanism.** Some programs include loss of use automatically at a
  percentage of the building limit; others make it an optional flat amount that
  somebody has to add. Two private policies on the same house can differ tenfold
  on this one coverage. This is the genuinely useful thing on the page and
  nothing else ranking for these queries says it. It ends on an instruction a
  reader can act on — ask for the limit in dollars, and ask whether it was
  included or added.
- **What else a standard policy excludes.** The URL already picks up
  `flood insurance replacement cost coverage` (26 impressions) and
  `standard flood insurance policy exclusions include` (17) at positions in the
  fifties. Those are the same "the federal policy pays less than you think"
  story, so they now have a section instead of an accidental keyword match.

All nine internal links were checked against the live database before publishing,
which is the lesson from shipping California-only slugs to both brands in 1.6.3.

## Verification done, and what is still blocked

Checked before publishing:

- `content.rendered` from the REST API, which runs the same `the_content`
  filters as the front end: 2,419 words in, 2,419 out, table intact, no `<p>`
  injected into cells, no `&#038;` mangling. This is the check that would have
  caught the zone-tool disaster, where a clean-looking draft rendered broken.
- Every internal link resolves to a published statewide page.
- All fourteen table figures re-derived from the HUD workbook by
  `tools/hud-fmr-pull.py`, including the four already live on California.

**Cannot be checked until the `.htaccess` line goes:** the front-end render.
Apache answers before WordPress, so the published page is unreachable at its own
URL, and `?p=266` canonical-redirects back into the same rule. Same position the
Zone X page has been in since it was published.

## Aaron's step — both lines, one pass

In cPanel → File Manager → `/home/mrtaco5/statewidefloodinsurance.com/.htaccess`,
put a `#` in front of these two lines:

```apache
# Redirect 301 /navigating-flood-zone-x/ /high-risk-flood-insurance/
# Redirect 301 /loss-of-use-coverage-in-flood-insurance/ /flood-coverage-gaps/
```

Then cPanel → Cache Manager → **Purge Full Cache**.

Do not delete the lines — commenting them out means the undo is deleting one
character, and it leaves the evidence of what was there.

The Zone X rule is the same defect: `/navigating-flood-zone-x/` carries **14,831
impressions** at position 34.7 and was being redirected into
`/high-risk-flood-insurance/`, which has five impressions — and semantically
backwards, since Zone X is the low-risk zone. Its replacement page (page 264) is
already published and waiting behind the same wall.

## After the purge

1. Confirm both URLs return **200**, not 301.
2. Confirm both render correctly — the front-end check neither page has had yet.
3. In Search Console, Request Indexing on both.
4. Watch position on `private flood insurance loss of use coverage` (currently
   3.6) and click-through on the URL as a whole (currently 0.67%). Position was
   never the problem; the destination was.

## The generalisable finding

Both bad rules are in `.htaccess`, neither is in Rank Math, and both were
invisible from inside WordPress. Aaron looked for them in Rank Math and could not
find them, which is exactly right — they were never there.

Diagnosing which layer owns a redirect takes one request. WordPress emits
`x-redirect-by: WordPress`, `charset=UTF-8` and a zero-length body. Apache emits
`charset=iso-8859-1`, a ~310-byte HTML 4.01 body, and **no** `x-redirect-by`
header at all. Both of these were plainly Apache.

**And the two were not the only two.** Rather than recommend a sweep, I ran one —
from the outside, so it does not depend on having read the config file: every URL
with Search Console impressions, requested, source impressions compared against
destination impressions. That found **ten** such rules carrying about 20,400
impressions a year, and one redirect that is correct and should stay.

Findings and triage in `STATEWIDE-REDIRECT-AUDIT.md`; the audit is re-runnable via
`tools/redirect-audit.py`. One of the ten cannot be fixed mechanically — the URL
contains a carrier's name, which there is a standing instruction never to publish,
so it is written up as a decision rather than a task.
