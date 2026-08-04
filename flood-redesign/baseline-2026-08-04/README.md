# Pre-change baseline — 4 August 2026

**This closes Session 0.** It is the comparison point for everything that follows. Nothing here is a
recommendation; it is what the accounts looked like before anyone touched them.

Files in this folder:

| File | What it is |
|---|---|
| `google-ads-campaigns-2026-07-08_to_08-04.tsv` | Raw Google Ads campaign export, 8 Jul – 4 Aug |
| `microsoft-ads-campaigns-2026-07-05_to_08-03.csv` | Raw Microsoft Ads campaign export, 5 Jul – 3 Aug |
| `google-ads-baseline.md` | The same Google data as a readable table |
| `microsoft-ads-baseline.md` | The same Microsoft data as a readable table |

Note the windows differ by three days (each platform's own "last 30 days"). Fine for a baseline;
worth remembering before comparing the two to each other.

## The headline numbers

| | Campaigns with spend | Spend | Reported conversions | Blended CPA |
|---|---:|---:|---:|---:|
| Google Ads | 43 | $24,771 | 612.6 | $40.43 |
| Microsoft Ads | 34 | $12,607 | 341.0 | $36.97 |
| **Combined** | **77** | **$37,378** | **953.6** | **$39.20** |

**Roughly $37,400 a month across both platforms, producing about 954 reported conversions.** Against
~250 policies bound in the same month, of which only a share came from PPC at all — the rest referral
and MGA. That gap is the whole reason the conversion count needs cleaning before it is used to make
decisions: not every lead binds, but a 4:1-or-worse ratio between "conversions" and *all* new business
from every source says the number is measuring something looser than leads.

## Microsoft: 38% of conversions come from the Audience network

| Network | Clicks | Impressions | Spend | Conversions | CPA |
|---|---:|---:|---:|---:|---:|
| Search | 1,329 | 45,609 | $8,728 | 167 | $52.27 |
| **Audience** | **1,959** | **860,202** | **$3,583** | **130** | **$27.56** |
| Performance Max | 639 | 25,356 | $295 | 44 | $6.71 |

The Audience network shows 860,000 impressions — nineteen times Search — and supplies **130 of
Microsoft's 341 conversions at a CPA that looks half of Search's.**

**This is the network where the June work found fraud.** The 29 June re-look records 21 fraud
placements excluded on 14 June, after which "conversions dropped ~21% … concentrated in the Audience
network / remarketing / big states = exactly the fake traffic," and it recommended reducing or
excluding the Audience network on search campaigns, explicitly overturning an earlier "leave it, it
converts" view as fraud-inflated. That recommendation does not appear to have been applied. Recorded
here as an observation with its history attached, not an action — but it is the first thing to look at
whenever Microsoft is revisited.

## The two live duplicate pairs, this period

| | Budget/day | Spend | Conv | CPA | Bid strategy |
|---|---:|---:|---:|---:|---|
| **Google** California Flood Insurance | $70 | $1,755 | 27.0 | $65.00 | CPC (enhanced) |
| **Google** California Flood Insurance – Max Conversions | $75 | $2,199 | 43.1 | $51.00 | Maximize Conversions |
| Microsoft California Flood Insurance | $50 | $1,148 | 12.0 | $95.66 | MaxConversions |
| **Google** Michigan Flood Insurance | $15 | $263 | 3.0 | $87.74 | CPC (enhanced) |
| **Google** Michigan Flood Insurance – Max Conversions | $15 | $404 | 11.0 | $36.75 | Maximize Conversions |
| Microsoft Michigan Flood Insurance | $20 | $401 | 4.0 | $100.25 | EnhancedCpc |

Both Google pairs are "limited by budget" on both halves — so they are not only competing in the
auction, they are each rationing spend while the other does the same. California alone is $3,954/month
across the pair, the largest single concentration in the account.

## Same state, both platforms — and the CPAs disagree in both directions

| State | Google CPA | Microsoft CPA | Combined spend |
|---|---:|---:|---:|
| Massachusetts | $399.49 | $69.23 | $676 |
| New Jersey | $186.62 | $30.03 | $974 |
| Alabama | $129.82 | $47.76 | $581 |
| Mississippi | $93.27 | $37.03 | $502 |
| Connecticut | $99.14 | $44.18 | $331 |
| Texas | $84.41 | $35.82 | $995 |
| Michigan | $47.68 | $100.25 | $1,068 |
| California | $56.39 | $95.66 | $5,102 |
| Colorado | $59.89 | $98.71 | $736 |

**Do not use this table to move budget.** The disagreement runs both ways, so it is not a simple
"one platform counts looser" bias — the two platforms are counting different things in different
places. Google's flood conversions are GA4-imported key events; Microsoft's are goals fired from
click-based triggers, and 38% of Microsoft's volume comes from the network that previously turned out
to be partly fraudulent. Until both platforms count the same validated submission, a cross-platform
CPA comparison cannot support a decision. That is the single strongest argument for doing the
measurement work before anything else.

## Outliers worth a look, in no particular order

**Expensive, spend ≥ $250:**

| | Campaign | Spend | Conv | CPA |
|---|---|---:|---:|---:|
| G | Massachusetts Flood Insurance Max Conversions | $399 | 1.0 | **$399.49** |
| G | Short term Rental Insurance | $653 | 2.0 | $326.56 |
| G | New Jersey Flood Insurance | $373 | 2.0 | $186.62 |
| G | Alabama Flood Insurance – Max Conversions | $389 | 3.0 | $129.82 |
| M | Michigan Flood Insurance | $401 | 4.0 | $100.25 |
| M | Max Conversion – General Truck Insurance | $2,345 | 24.0 | $97.71 |
| M | California Flood Insurance | $1,148 | 12.0 | $95.66 |

Massachusetts on Google is the standout: $399 spent, one conversion, and the campaign is *not*
budget-limited — 2.63% conversion rate against a 20–35% norm elsewhere in the account. Its Microsoft
twin returned $69.23. Something is wrong with that campaign specifically, and it is worth opening
before any structural work.

Also: **Google Oklahoma Flood Insurance spent $85.51 for 60 clicks and zero conversions**, and
Microsoft Pest Control spent $180.81 for zero. Small money, but zero-conversion campaigns are where
tracking faults hide.

**Cheap and capped — the campaigns rationed while performing:**

| | Campaign | Budget/day | Spend | Conv | CPA |
|---|---|---:|---:|---:|---:|
| M | Performance Max Bing Oct 2024 | $10 | $295 | 44.0 | $6.71 |
| M | Florida Flood Insurance | $20 | $622 | 60.0 | $10.37 |
| G | Demand Gen – Statewide Flood – 24 States | $20 | $350 | 26.0 | $13.44 |
| M | Louisiana Flood Insurance | $20 | $564 | 30.0 | $18.79 |
| G | Earthquake Insurance – Max Conversions | $30 | $775 | 37.0 | $20.96 |
| G | Physical Damage & Cargo Insurance | $50 | $1,800 | 80.0 | $22.50 |
| G | Florida Flood Insurance – Max Conversions | $25 | $721 | 26.0 | $27.73 |

Both Performance Max campaigns report single-digit CPAs on $10–20/day budgets. The June re-look
flagged exactly this and added the right caveat — "verify counting isn't loose" — because PMax
routinely takes credit for brand and remarketing traffic it did not originate. Treat those two CPAs as
unproven rather than as the account's best performers.

## What this baseline is for

Two jobs, and only two:

1. **When the measurement work lands and reported conversions fall, this is what they fell from.** The
   drop is expected — staff intake and failed validations stop counting. Compare bound policies, not
   this table, to decide whether anything real changed.
2. **If anything is ever changed and needs undoing,** these are the budgets, bid strategies, and
   statuses to put back.
