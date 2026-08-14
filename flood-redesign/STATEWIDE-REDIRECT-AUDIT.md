# Statewide redirect audit — 20,400 impressions a year pointed at pages that rank for nothing

Run `tools/redirect-audit.py https://statewidefloodinsurance.com/` to reproduce.
Measured 14 August 2026 over the twelve months to 11 August 2026.

## How this was found, and why it was not found earlier

Two bad rules turned up by reading the `.htaccess` file Aaron pasted. That was
luck — reading a config file only finds what you thought to look at. Auditing from
the outside instead (take every URL Search Console has impressions for, request
it, compare the source's impressions against the destination's) found **ten**.

None of them are in Rank Math. Aaron looked there and could not find them, which
was correct — they were never there. They are all in `.htaccess`, where nothing
inside WordPress will ever show them to you.

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

### The carrier-name conflict — Aaron's call, not mine

`/hiscox-flood-plus-comprehensive-flood-insurance-coverage/` holds 710
impressions at position 8.4 and eight clicks. Its demand is purely the carrier's
brand:

| query | impressions | position |
|---|---|---|
| flood plus | 40 | 8.9 |
| hiscox flood insurance | 32 | 10.7 |
| hiscox flood plus | 19 | 10.2 |
| hiscox flood insurance reviews | 15 | **6.3** |

There is a standing instruction on this account never to publish a carrier name.
Restoring this URL would publish one in the slug, the title and the body — that is
the whole point of the page. So this is not a mechanical fix and I have not made
it. The options, for Aaron to pick from:

1. **Leave the redirect.** Costs 710 impressions a year of high-intent traffic.
2. **Restore it as written.** Highest recovery, breaks the standing rule.
3. **Something in between** — a page about the coverage features that program
   offers, without naming it. This keeps the rule but almost certainly loses the
   rankings, because the rankings *are* the brand name.

Option 3 sounds like the safe middle and probably is not: nothing on that page
would match the queries. Worth deciding deliberately rather than defaulting.

### Cross-brand, and the wrong kind of target

`/long-beach-ca-flood-insurance/` (170 impr, pos 14.1 — `best long beach flood
insurance policy` sits at 9.1) and `/flood-insurance-bakersfield-…/` (39 impr)
both 301 across to **californiafloodinsurance.com/get-a-quote/**.

Sending California city intent to the California brand is a reasonable commercial
decision. Sending an informational query to a quote form is not — Google treats a
form as a poor match for "what is flood insurance like in Long Beach", which is
the likeliest reason a position-9 query earns zero clicks. If these stay
cross-brand they should land on California *content*, not the form.

### Tag archives, ~69 impressions, all 404

Thirteen `/tag/…` URLs 404, the largest being `/tag/long-beach-flood-insurance/`
at 27 impressions. Zero clicks across all of them. Tag archives were presumably
dropped in the Divi migration. Not worth work; noted so it is not rediscovered as
a mystery later.

## What is ready to go right now

Two of the ten have their replacement page written and published, waiting behind
the redirect that hides them:

```apache
# Redirect 301 /navigating-flood-zone-x/ /high-risk-flood-insurance/
# Redirect 301 /loss-of-use-coverage-in-flood-insurance/ /flood-coverage-gaps/
```

Comment those two out in `/home/mrtaco5/statewidefloodinsurance.com/.htaccess`,
then cPanel → Cache Manager → Purge Full Cache. Comment rather than delete, so
the undo is removing one character and the evidence of what was there survives.

Neither page has had a front-end render check yet, because Apache answers before
WordPress and both are unreachable at their own URLs until those lines go.
`?p=266` canonical-redirects straight back into the same rule. Both were checked
through `content.rendered` from the REST API, which runs the same `the_content`
filters the front end does — that is the check that catches wpautop damage on a
draft that looks clean in the editor.

## Then

1. Confirm both URLs return 200 and render correctly.
2. Request Indexing on both in Search Console.
3. Decide the Hiscox question.
4. Work the remaining rescues, then the content gaps.
5. Re-run the audit against californiafloodinsurance.com. The same migration
   produced both sites and there is no reason to assume only one has this.
