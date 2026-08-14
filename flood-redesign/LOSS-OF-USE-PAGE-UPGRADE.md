# Upgrading `/loss-of-use-coverage-in-flood-insurance/`

**Why this page and not the cost page.** It already ranks on 4 of the 5 loss-of-use
queries surveyed — the broadest-ranking single asset we have. Upgrading something
that already ranks is a far cheaper win than rebuilding the cost page, which ranks
at position 18. Do this one first.

Audited live 14 Aug 2026. Title, meta and structure are good; 1,617 words across
nine H2s. It does **not** claim all our policies include loss of use, which is a
relief given what the book actually shows. Two claims on it are wrong, and one
gap is worth filling.

---

## Correction 1 — the claims statistic is understated

**On the page now:**

> "Roughly 1 in 4 flood claims come from moderate- to low-risk areas"

**Verified figure: 29%**, from floodsmart.gov, checked directly. "Roughly 1 in 4"
reads as 25% and understates our own argument by four points, on the one statistic
that does the most work on the page.

This is also part of a known site-wide problem: **four different Zone X figures
appear across the two sites.** They should all become the same verified 29%, cited
the same way. Fixing it here without fixing it elsewhere just moves the
inconsistency around.

**Change to:** "More than 1 in 4 — 29% — of NFIP flood claims come from moderate-
to low-risk areas."

## Correction 2 — the "10% to 20% of dwelling" guidance does not match our book

**On the page now:**

> "Loss of use limits on private policies are usually expressed as a dollar cap or
> as a percentage of your dwelling coverage, often somewhere around 10% to 20%."

Measured against the Instanda bordereau (Aug 1–9 2026, 68 California rows), that is
misleading. Of the California policies written **with** the cover:

| limit | share of policies with cover |
|---|---|
| **$5,000** | **47%** |
| $50,000 | 26% |
| $25,000–$44,200 | 18% |
| $100,000–$120,000 | 9% |

At the $250,000 building limit that 91% of our book sits on, 10–20% means
$25,000–$50,000. That describes roughly half. **The single most common limit is
$5,000 — about 2% of dwelling.** A reader with the most common limit would conclude
from our page that they have five times the cover they actually have.

**Do not simply substitute our numbers.** This is nine days of one file, and limits
are set by programme rather than chosen freely. The honest fix is to stop asserting
a typical percentage:

> "Loss of use limits vary widely — some policies carry a few thousand dollars,
> others tens of thousands, and the limit is set by the programme the policy is
> written in rather than chosen freely. Ask what the limit actually is before
> assuming it will cover a long displacement."

That is true, checkable, and it converts better: it turns an assumption into a
reason to call.

## Correction 3 — do not let "many private policies include ALE" drift

Currently accurate. Keep it that way. **Never upgrade it to "all."** Our own book:
49% of policies carry a zero limit, and one large programme writes without the
cover on 71% of rows. A single customer's declarations page disproves "all."

## The gap: nobody prices a California displacement

Of 44 ranking pages surveyed, 41 mention the gap and only 5 quantify it. **Nobody
anywhere prices a California displacement.** This page currently says repairs "take
several months" and rentals are "not cheap" — true, and identical to what every
competitor says.

`BRIEF-3-california-displacement-cost.md` is out for exactly this: HUD Fair Market
Rents by county, a market-rent cross-check, and a sourced basis for displacement
duration. When it returns, this page gets the thing no competitor has:

> "A three-bedroom rental in Sacramento County runs about $X a month. Six months
> out of your home is about $Y — on top of the mortgage you are still paying. Your
> NFIP policy contributes nothing toward it."

Two constraints on that paragraph when it is written:

- **Every figure dated and sourced.** Rents change annually.
- **Do not present a duration as typical unless the research supports one.** If
  there is no published median, frame it as "here is what one month costs" and let
  the reader multiply. An invented duration is the sort of error that ends up
  quoted back at us.

## The displacement costing — RESEARCH IS IN, 14 Aug 2026

`research-2026-08-13/job3-displacement-and-fema-ia.md`. Nothing is blocked now.

### Write the monthly cost, never a total

There is **no reliable published median displacement duration** for California
residential floods. The studies measure incompatible things — evacuation orders,
neighbourhood reentry, time living elsewhere, repair completion — and the
distribution has a long tail (NIST Lumberton: mean 86 days against a median of 7,
and that excludes households still displaced at survey).

So the page states a **monthly** figure and lets the reader multiply. Inventing a
"typical six months" is exactly the kind of number that gets quoted back at us.

FY2026 HUD Fair Market Rents, effective 1 Oct 2025, 40th-percentile gross rent:

| County | 2BR | 3BR |
|---|---:|---:|
| San Joaquin (Stockton) | $1,742 | $2,423 |
| Sacramento | $2,255 | $3,002 |
| Monterey (Pajaro/Salinas) | $2,684 | $3,623 |
| Sonoma (Santa Rosa) | $2,827 | $3,887 |
| Los Angeles | $2,903 | $3,681 |
| San Diego | $3,001 | $3,998 |
| Orange | $3,236 | $4,393 |
| Santa Clara | $3,483 | $4,602 |

**Do not claim these are conservative.** I assumed they would be and asked a
leading question; the check says otherwise. Zillow's county index sits above the
2BR figure in only three of eight counties and below the 3BR figure in all eight,
because HUD and Zillow measure different rental populations with different utility
and unit-size assumptions. Present HUD as the official baseline, dated, full stop.

**No furnished-housing premium may be published.** No government or university
source establishes a California figure; the 10-30% and 40-75% numbers circulating
are industry marketing. If we want to show furnished costs more, use dated local
listings.

### The FEMA question — it does not sink us, but it changes the wording

The honest answer to "doesn't FEMA cover this?" is that FEMA sometimes does, and
we must stop short of saying otherwise.

**Verified directly against OpenFEMA:** in the ten years to Aug 2026, California
had 13 major disaster declarations carrying Individual Assistance. **Eight were
wildfires.** One was COVID-19. **Only four mention flooding at all** — DR-4353,
DR-4683, DR-4699 and DR-4758 — and DR-4758 designated a single county. The Feb
2019 Guerneville/Russian River flood (DR-4434) records Individual Assistance as
**"not requested."**

Also true, and it must not be got wrong: FEMA rental assistance carries **no
annual dollar cap** (the $43,600 IHP maximum applies to repair/replacement and
other needs, not rental assistance), normally runs up to 18 months, and starts as
a two-month award requiring re-documentation to continue.

**Never write "FEMA gives you nothing."** It is false and one counterexample
destroys the page's credibility. Write instead:

> "The NFIP does not cover additional living expenses. FEMA rental assistance may
> be available after certain presidentially declared disasters — but it is not
> automatic, it requires your area to be designated for Individual Assistance, and
> in the last ten years only four California disasters involving flooding
> qualified at all."

That is stronger than the overstatement, because it survives scrutiny.

## What is NOT blocked

Everything. Corrections 1-3 and the displacement section are all verified.

## Sequencing

1. Fix the 29% figure — here and on every other page carrying a conflicting version.
2. Replace the 10–20% guidance with the varies-by-programme wording.
3. Hold the "many, not all" line.
4. Add the displacement costing when Brief 3 returns.

Steps 1–3 are edits to a live ranking page and need Aaron's go-ahead before they
are made.
