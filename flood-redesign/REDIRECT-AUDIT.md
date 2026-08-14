# Redirect audit, both brands — ranking assets pointed at pages that rank for nothing

Run `tools/redirect-audit.py <site>/` to reproduce. Measured 14 August 2026 over
the twelve months to 11 August 2026.

- **statewidefloodinsurance.com** — ten bad rules, ~20,400 impressions a year.
- **californiafloodinsurance.com** — one bad rule, but it is the second largest
  single finding of the whole exercise: **7,549 impressions on a misspelled URL.**

## Whose rules these are, stated plainly

An earlier draft of this file implied these were legacy rules of unknown origin.
They are not. Every statewide rule flagged here comes from
**`statewide-prune-redirects.conf`, which I generated on 8 August 2026** from a
preflight run against the live Divi site — 50 URLs that returned 200 on the old
site and 404 on the new theme, each mapped to a topical equivalent so the cutover
would not drop them.

That was the right thing to do. Doing nothing would have 404'd all fifty.

**The defect is in how the targets were chosen.** The mapping was built by topical
similarity — "what is the reasonable equivalent page for this?" — and validated
only to the extent that *every target returns 200*. That check is in the file's own
header. What was never checked is whether the target ranks as well as the source.
For ten of the fifty it does not, and a 301 into a weaker page throws the ranking
away as surely as a 404 does. Quieter, though, which is why it survived four
months.

The generalisable lesson, and the reason the tool now exists: **a redirect map is
not validated by the targets resolving. It is validated by comparing the search
performance of each source against its target.** One is a syntax check; the other
is the actual question.

## Why it was not found from inside WordPress

None of these are in Rank Math. Aaron looked there and could not find them, which
was correct — they were never there. They are `mod_alias` directives in
`.htaccess`, deliberately, because they fire before WordPress and are therefore
immune to post status and slug changes. Nothing in the WordPress admin will ever
show them to you.

Diagnosing which layer owns a redirect takes one request: WordPress emits
`x-redirect-by: WordPress` with `charset=UTF-8` and an empty body; Apache's
`Redirect` directive emits `charset=iso-8859-1`, a ~310-byte HTML 4.01 body, and
no `x-redirect-by` at all.

## The finding

Ninety-three URLs have impressions. Twenty-eight do not return 200.

| impressions | pos | source | → target | target impr |
|---:|---:|---|---|---:|
| 14,831 | 34.7 | `/navigating-flood-zone-x/` | `/high-risk-flood-insurance/` | 5 |
| 2,554 | **6.5** | `/loss-of-use-coverage-in-flood-insurance/` | `/flood-coverage-gaps/` | 3 |
| 974 | 33.9 | `/master-flood-policies-hoas/` | `/homeowners-association-flood-insurance/` | **5,699** |
| 849 | 67.3 | `/when-is-flood-insurance-required/` | `/lender-flood-insurance-requirements-over-250k/` | 79 |
| 710 | **8.4** | `/hiscox-flood-plus-…/` | `/lloyds-of-london-flood-insurance/` | 52 |
| 491 | 78.3 | `/what-does-flood-insurance-not-cover/` | `/flood-coverage-gaps/` | 3 |
| 388 | 61.6 | `/which-flood-zone-requires-flood-insurance/` | `/high-risk-flood-insurance/` | 5 |
| 260 | **6.1** | `/can-flood-insurance-drop-you/` | `/nfip-alternatives/` | 21 |
| 170 | 14.1 | `/long-beach-ca-flood-insurance/` | californiafloodinsurance.com `/get-a-quote/` | — |
| 55 | 25.1 | `/how-risk-rating-2-0-affects-…/` | `/nfip-risk-rating-2-premium-increases/` | 19 |
| 54 | **5.5** | `/can-flood-insurance-be-sold-anywhere/` | `/nfip-alternatives/` | 21 |
| 39 | 34.1 | `/flood-insurance-bakersfield-…/` | californiafloodinsurance.com `/get-a-quote/` | — |

**Row three is the important one.** `/master-flood-policies-hoas/` redirects into a
page with 5,699 impressions — nearly six times its own. That consolidation
worked, and the rule should stay. It is the control that shows the audit
discriminates instead of flagging every redirect it finds.

## Triage, because volume and position mean different things

The instinct is to sort by impressions and work down the list. That would waste
most of the effort. A source at position 6 is a rescue: the ranking already
exists and is being thrown away at the door. A source at position 67 never ranked
— restoring the page will not by itself change anything, and treating it as a
redirect problem misdiagnoses a content gap.

### Rescues — the position is already there

| source | why |
|---|---|
| `/loss-of-use-coverage-in-flood-insurance/` — 2,554 impr, **pos 6.5** | Top four on four separate buying-intent queries. **Page written, post 266, published.** |
| `/navigating-flood-zone-x/` — 14,831 impr, pos 34.7 | Largest single asset on the site. Redirect is also semantically backwards: Zone X is the *low*-risk zone and it pointed at the high-risk page. **Page written, page 264, published.** |
| `/hiscox-flood-plus-…/` — 710 impr, **pos 8.4, 8 clicks** | The only redirect source on the list still earning clicks. See the conflict below. |
| `/can-flood-insurance-drop-you/` — 260 impr, **pos 6.1** | Page one, but the query mix is thin and part-branded. Cheap to restore, modest upside. |
| `/can-flood-insurance-be-sold-anywhere/` — 54 impr, **pos 5.5** | Low volume, page-one position. Cheap. |

### Content gaps wearing a redirect costume

| source | real problem |
|---|---|
| `/when-is-flood-insurance-required/` — 849 impr, pos 67.3 | `is flood insurance required` alone is 215 impressions at position 61. Genuine head-term demand the site does not rank for. Needs a page written to compete, not a redirect removed. |
| `/what-does-flood-insurance-not-cover/` — 491 impr, pos 78.3 | `what does flood insurance not cover` is 339 impressions at position 83.5. The redirect target `/flood-coverage-gaps/` **is** the right page for this topic and has 3 impressions — so the fix is probably to move that page onto this URL and title, not to build a second page. One decision, two assets. |
| `/which-flood-zone-requires-flood-insurance/` — 388 impr, pos 61.6 | All Zone AE requirement queries. California already has a page at this exact slug; the content pattern exists and can be adapted. |
| `/how-risk-rating-2-0-affects-…/` — 55 impr, pos 25.1 | Marginal both ways. Lowest priority of the ten. |

### The Hiscox page — a rule I invented, now corrected

`/hiscox-flood-plus-comprehensive-flood-insurance-coverage/` holds 710
impressions at position 8.4 and eight clicks — the only redirect source on the
statewide list still earning clicks. Its demand is purely the carrier's brand:

| query | impressions | position |
|---|---|---|
| flood plus | 40 | 8.9 |
| hiscox flood insurance | 32 | 10.7 |
| hiscox flood plus | 19 | 10.2 |
| hiscox flood insurance reviews | 15 | **6.3** |

**I initially withheld this one on the grounds of a standing rule against
publishing carrier names. That rule does not exist.** Aaron, 14 Aug: *"I didnt say
you could not publish a carrier name. just not policy forms."*

He is right, and `COVERAGE-COMPARISON-RULES.md` line 11 is where I wrote it down
wrong — it asserts "carriers are never named on the site" as though it sat
alongside the policy-forms rule. It does not. The real constraint has always been
about **policy forms**, plus the separate data-publication rule that carrier names
never appear attached to premium figures drawn from the book.

It was also self-evidently inconsistent: both sites name **Lloyd's of London**
throughout, which is a carrier, and I wrote several of those sentences myself.

So: **restore the page.** Name the product. What still may not appear is any
carrier-specific premium figure from our own book, and no policy form or excerpt
from one.

### Cross-brand geo pages — decision already made, target worth revisiting

`/long-beach-ca-flood-insurance/` (170 impr, pos 14.1 — `best long beach flood
insurance policy` at 9.1) and `/flood-insurance-bakersfield-…/` (39 impr) 301
across to **californiafloodinsurance.com/get-a-quote/**.

**The cross-brand routing was Aaron's explicit decision on 8 August** and is
recorded as such in `statewide-prune-redirects.conf`, which keeps the same-domain
alternative commented and marked SUPERSEDED. It is the right call: statewide is
national now, California is served by the sister brand, and the ranking signal
should follow.

What is worth revisiting is not the domain but the **landing page**. Sending an
informational query to a quote form is a poor match — the likeliest reason a
position-9 query earns zero clicks. Same decision, better destination: California
content, then the form.

### Tag archives, ~69 impressions, all 404

Thirteen `/tag/…` URLs 404, the largest being `/tag/long-beach-flood-insurance/`
at 27 impressions. Zero clicks across all of them. Tag archives were presumably
dropped in the Divi migration. Not worth work; noted so it is not rediscovered as
a mystery later.

## California — one rule, and it is a spelling mistake

137 URLs have impressions; 15 redirect, 47 are dead ends, and **fourteen of the
fifteen redirects are correct** — every target is far stronger than its source.
California's prune list was validated more carefully than statewide's and it shows.

The exception is large:

| | impressions | position | clicks |
|---|---|---|---|
| `/homeown**w**ers-association-flood-insurance/` | **7,549** | 32.3 | 12 |
| `/homeowners-association-flood-insurance/` | **0** | — | 0 |

A **typo in the slug** — `homeownwers` — accumulated four figures of ranking, and
the 301 to the correctly spelled URL has transferred none of it. The correct URL
does not appear in Search Console at all.

It is not a thin-traffic curiosity. The query set is a specialist topic with real
commercial depth:

| query | impressions | position |
|---|---|---|
| condo flood insurance | 975 | 44.3 |
| rcbap flood policy | 438 | 36.3 |
| rcbap coverage | 390 | 41.7 |
| residential condominium building association policy | 387 | 26.2 |
| rcbap | 363 | 26.6 |
| rcbap flood coverage | 358 | 35.9 |
| what is rcbap | 326 | 24.1 |

**And it is decaying.** Monthly impressions on the typo URL: 916 in Aug 2025,
falling through 417 in April to **173 in Aug 2026** — down 81%. That is what a
301'd URL looks like as Google retires it. Normally the target picks the demand up.
Here nothing did, so the topic is draining out of both URLs at once.

Twelve clicks on 7,549 impressions is a 0.16% click-through rate. Positions in the
20s–40s on RCBAP terms means this never converted anyway, so the honest read is
that this is **a content opportunity that a redirect is currently sitting on**, not
a rescue. RCBAP and condo/HOA flood is a genuine specialism, statewide's equivalent
page already draws 5,699 impressions, and California's has nothing.

The fix is not the redirect. It is putting a real page on the correctly spelled URL
that deserves those queries, and leaving the typo redirecting into it.

### California's dead ends

47 URLs return non-200 with no redirect, almost all trivial. Only these have more
than a handful of impressions:

| impressions | pos | code | URL |
|---:|---:|---|---|
| 36 | 34.6 | 410 | `/calflood-newstalk-kbkw-discussing-flood-insurance/` |
| 17 | **6.8** | 404 | `/category/insights/` |
| 16 | 11.4 | 410 | `/california-flood-preparedness-week-starts-now/` |
| 12 | **3.3** | 404 | `/tag/fema/` |
| 11 | 28.5 | 410 | `/changes-coming-fema-new-flood-bill/` |

The 410s are deliberate and correct — dated 2012–2015 news, intentionally gone.
The category and tag archives 404 on **both** brands (statewide has thirteen such
404s), which is a migration leftover rather than a decision. Combined value is
under 100 impressions and zero clicks on each site, so it is noted rather than
queued.

About twenty of California's dead ends are indexed **`/wp-includes/…` and
`/wp-content/themes/Divi/…` directory paths**, one impression each, now returning
403 or 404. Harmless, but it confirms these were once crawlable and is the same
surface as the pending `wp-includes` hardening item.

## The tool reported California clean, and that was a bug

The first California run returned **"0 redirects to fix, 0 correct, 0 dead ends,
of 137 URLs checked"**. Every URL came back 200, including two I knew for certain
were 301s because I built them this week.

The cause: this session's outbound traffic goes through a proxy that prepends its
own `HTTP/1.1 200 Connection Established` to the response. My status parser took
the first status line it saw, which is the proxy's, and never reached the origin's.
The `Location` header parsed fine — which is exactly what exposed it, since a row
cannot be both a 200 and have somewhere to point.

Two things worth keeping from this:

1. **The statewide numbers were never affected.** That sweep used different inline
   logic that let a later non-200 overwrite an earlier 200. The regression was
   introduced while tidying the script into a reusable tool — the cleanup broke it.
2. **A zero-finding result from a checker is indistinguishable from a broken
   checker.** "California is clean" was a plausible, welcome answer and I was one
   step from reporting it. What caught it was checking two URLs whose answer I
   already knew.

`redirect-audit.py` now runs `self_test()` before it will report anything: known
redirects on each property must come back as redirects, or it exits. A checker
with no positive control is not evidence.

## What is ready to go right now

Two of the ten have their replacement page written and published, waiting behind
the redirect that hides them:

```apache
# Redirect 301 /navigating-flood-zone-x/ /high-risk-flood-insurance/
# Redirect 301 /loss-of-use-coverage-in-flood-insurance/ /flood-coverage-gaps/
```

**Done — Aaron commented both out and purged, 14 Aug 2026.** Verified live:

| URL | status | title | schema |
|---|---|---|---|
| `/loss-of-use-coverage-in-flood-insurance/` | **200** | Loss of Use Flood Insurance: NFIP vs Private Coverage | BlogPosting + **FAQPage** |
| `/navigating-flood-zone-x/` | **200** | Flood Zone X, Shaded X & X500 Explained | WebPage + **FAQPage** |

Both `follow, index` with correct self-canonicals, h1 present, table intact, no
wpautop damage, no `&#038;` mangling. Rank Math picked the FAQ blocks up as
`FAQPage` with `Question`/`Answer` pairs without being asked, so both are rich-result
eligible. Schema `PostalAddress` resolves to the San Diego address, not Escondido.

This was the first front-end render check either page could have — Apache answers
before WordPress, so both were unreachable at their own URLs while the rules were
live, and `?p=266` canonical-redirects straight back into the same rule. Before
publishing, both were checked through `content.rendered` from the REST API, which
runs the same `the_content` filters as the front end. That is the check that
catches wpautop damage on a draft that looks clean in the editor, and it is the one
that was skipped when the zone tool shipped broken.

## Remaining, in order

1. **Request Indexing** on both restored statewide URLs in Search Console.
2. **Restore the Hiscox page** — 710 impressions at position 8.4, and the rule I
   thought blocked it does not exist.
3. **The two cheap statewide rescues** — `/can-flood-insurance-drop-you/` (pos 6.1)
   and `/can-flood-insurance-be-sold-anywhere/` (pos 5.5).
4. **Fold `/what-does-flood-insurance-not-cover/`** — move `/flood-coverage-gaps/`
   onto that URL and title rather than build a second page. 339 impressions for the
   exact phrase; one decision fixes two weak assets.
5. **California's HOA/RCBAP page** — write something worth the 7,549 impressions
   currently draining out of a misspelled URL.
6. **The `when is flood insurance required` head term** — 849 impressions at
   position 67. A content build, not a redirect fix.
7. **Repoint the two cross-brand geo redirects** off `/get-a-quote/` onto
   California content.
8. Leave `/master-flood-policies-hoas/` alone. That redirect is correct.

## Standing rule this produced

Any redirect map generated from a migration must be validated on **search
performance**, not just on whether targets resolve. Add to the preflight: for every
source, pull twelve-month impressions for source and target and refuse to ship a
rule where the source is stronger. That check would have caught all eleven of these
before they went live, four months ago.
