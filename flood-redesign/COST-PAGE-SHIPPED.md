# `/how-much-does-flood-insurance-cost/` rebuilt and live — 14 Aug 2026

Post 92. Pre-edit content backed up session-locally. ~1,780 words.

## What it replaced

The old page invented its numbers and priced by zone:

| old claim | status |
|---|---|
| "generally runs $500 to $2,000 per year" | unsourced range, removed |
| "Zone X: often $400–$700/year" | contradicted by measurement (X/B/C median $1,082) |
| "Zone A/AE/V: commonly $1,500–$3,000+" | contradicted (A median $1,246) |
| "$40 and $170 per month" | unsourced, replaced with measured monthly equivalents |

The zone ranges were not merely imprecise — they described **pre-2021 rating**.
Risk Rating 2.0 does not rate by zone, and our measurement puts A and X about
$160 apart at the median rather than the $800–$2,300 the page implied.

## What it says now

Both sides measured at identical terms ($250,000 building, $5,000 deductible,
single-family), all-in:

| | median | middle half | n |
|---|---:|---|---:|
| NFIP in force 14 Aug 2026 | **$1,244** | $845–$2,007 | 10,545 |
| Private, policies we placed | **$822** | $769–$888 | 3,645 |

Plus: p10 $623 / p90 $2,836 spread; zone table with the causation warning;
primary vs non-primary ($1,205 / $1,438) explained as the HFIAA surcharge; the
loss-of-use gap integrated per the second review; and a full methodology section.

## Every review rule applied

- **Labelled as our book, never a market rate.** The gap is stated explicitly as
  "an upper bound on what shopping might save you, not a prediction," with the
  selection mechanism spelled out — we place private when it wins, so the cases the
  NFIP won are missing by construction.
- **Adverse selection stated, and stated fairly**: the NFIP must accept every
  applicant, so its rates carry risks private declined. Written as a design feature
  of a federal programme, not a criticism.
- **n, period and dispersion published** beside every median.
- **"These are not quotes"** disclaimer, mirroring CDI's own posture with its
  premium surveys.
- **Suppression rule disclosed** (nothing under 11 policies; no estimating or
  interpolation).
- **No county table** — the mix problem makes it indefensible and the GSC data says
  there is no demand for it.
- **No carrier named.** No policy form referenced.
- **29%** claims statistic, consistent with the loss-of-use page.
- **In-force snapshot**, not transactions, with the date on the page.

## The takeaways block nearly shipped stale

The "What to know" box is `_cfi_takeaways` post meta, not content, so the content
rewrite left the old "$500 to $2,000" sitting at the top of a page that spends
1,700 words explaining why that number is wrong. Caught on live verification.
**Rule: on this theme, rewriting a post means rewriting its meta too.**

## Also shipped

`/contact-us/` SEO title changed from "Contact California Flood Insurance |
855-225-3566" to "Contact Us | Talk to a Flood Specialist | 855-225-3566". It was
ranking **4.4 on "california flood insurance" with 130 impressions and zero
clicks** — a page-one slot returning nothing. Now evidenced from GSC rather than
asserted.

## Still open

- Watch whether the cost cluster (3,303 impressions, positions 20–35) moves. Give
  it 3–6 months, not weeks.
- The flood-zone cluster is larger still (3,863 impressions) and address-lookup
  shaped. Needs its own plan; it is a tool, not an article.
- No off-site citation outreach yet. The second review was right that a linkable
  asset needs promotion, not just internal links.

---

# CORRECTION — the X-zone figure was killing the sale, 14 Aug 2026

Aaron: *"we do NOT want to show x zones as close to 1,082. the average is around
$450 all in for most of california. that is what we sell every single day. people
do NOT think it will ever flood. we will sell no policies if we tell them its
nearly 1,000 which is not correct."*

He is right that the page was wrong in effect, and the reason is instructive.

## The $1,082 is accurate and was still misleading

I checked whether it was a coverage artefact — whether X-zone buyers take less
than the $250,000 benchmark. **They do not: 91.8% of NFIP Zone X policies in
California carry the full $250,000.** So $1,082 is genuinely what the NFIP charges
in Zone X, and the figure stays.

The failure was one of omission. The zone table showed **NFIP prices only**. An
X-zone reader — someone buying voluntarily, who mostly does not believe it will
flood — saw $1,082 and concluded flood insurance costs about a thousand dollars.
That is the most expensive option on the page presented as the answer, with the
thing we can actually sell them left out.

**A true number in a misleading frame is still a misleading page.** This is the
same failure as the blended zone average, arriving from the other direction.

## Aaron's $450 was already substantiated, earlier in this project

It is not an anecdote. From `COST-PAGE-PLAN.md`, with Aaron's own explanation of
the mechanism:

> "when we say 475, the premium may be 350 and then with the policy fee and tax
> its around 475"

- $350 premium + $95 policy fee + California's 3.18% surplus lines tax and
  stamping fee = **$459**
- Our book's **p10 all-in is $441**
- **10.5% of everything we place** lands in that band
- Between p10 and p25 the price jumps **$294** — a genuine cliff, not a tail

That is a **minimum-premium cohort**: carriers apply a floor, and once a home is
low-risk enough the rating stops falling and lands on it. The bimodality is
structural, which is why a median describes almost nobody at the cheap end.

## What went on the page

A new section, placed immediately after the zone table so it catches the reader
who has just seen $1,082: the federal median outside the high-risk zone, against
one policy in ten of ours coming in near $450 — with the minimum-premium mechanism
explained, the $294 cliff shown, and the honest close that which group a home
falls into cannot be read off a table and takes a quote to find out.

Also added to the summary box at the top, so it is visible before the reader
reaches any four-figure number.

## The one thing not adopted

Aaron said "$450 all in **for most of California**." Our book's median is **$794**
and p25 is $637, so "most" is not supportable and would be the same class of error
as the unsourced $780 removed from the rates page an hour earlier. What is
supportable, and is what the page says: **about one policy in ten**, concentrated
in exactly the low-risk homes an X-zone reader owns.

For an X-zone reader specifically the typical figure is probably well below the
book median — our 21 zone-tagged rows put X at $564 and AE at $491 — but n=11 and
n=10 are at or under the publishing floor. **Fixing that is the NFHL geocoding
task**: zone-tag the whole book and the X-zone figure becomes publishable at scale
instead of resting on a decile.
