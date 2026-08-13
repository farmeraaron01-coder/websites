# Cost page rebuild — plan, after the competitive research

Sources: Kimi's three research reports (13 Aug 2026), independently spot-checked
against FEMA and against our own Search Console data. Supersedes the traffic
figures used earlier — see the correction at the bottom.

## Two findings that change the approach

### 1. Zone letter does NOT set the price. It sets whether you have a choice.

I previously called the Hiscox zone result (AE $476 vs X $547) "sampling noise
that inverts the risk ordering." That was too quick. FludZone's much larger
measured OpenFEMA figures for California show the same inversion:

| Zone | CA policies | avg premium |
|---|---|---|
| Zone X | 69,510 | **$812** |
| Zone A | 55,133 | **$759** |
| Zone AE | 46,651 | $1,334 |
| Zone AO | 23,882 | $954 |
| Zone AH | 8,269 | $1,117 |
| Zone VE | 2,942 | $1,337 |

Zone X ($812) is dearer than Zone A ($759) at scale, in independent data. So the
inversion is not a small-sample artefact, and the reason is structural: **under
Risk Rating 2.0, FEMA does not rate by flood zone at all.** FEMA says so in its
own words — *"The previous methodology set rates based on geographic zones and
elevation"* — and ValuePenguin puts it plainly: *"the zones are no longer used to
calculate rates."*

Consequences for the page, and they are significant:

- **"Average cost by zone" is descriptive, not causal.** It describes who happens
  to buy in each zone, not a rate table. Any wording implying "you are in Zone X
  therefore you pay less" is wrong and a competent reader will catch it.
- **The honest mechanism is: zone determines the mandate; risk characteristics
  determine the price.** Elevation, construction, distance to water, first-floor
  height. That is also a better sales conversation, because those are the things a
  quote actually turns on.
- Aaron's commercial point survives completely intact. An X-zone visitor still
  needs a number that applies to them, and still needs to know they have a choice.
  Only the *explanation* changes.
- **"A-zone" is not one price.** Zone A $759 against Zone AE $1,334 is a 76% gap
  inside the supposedly-high-risk group. Zone A (no base flood elevation
  determined) and Zone AE (BFE established) behave completely differently. Almost
  no competitor separates them.

### 2. We already rank well on California cost queries. The bad positions are national.

Kimi's SERP check puts our cost page at **#4 / #2 / #7** on three of the four
California-qualified cost queries, and the rates page at **#3** on the fourth.
That contradicted the "stuck on page two" story, so I checked our own data. Both
are true, of different queries:

| query | impressions | position |
|---|---|---|
| how much is flood insurance in california | 41 | **3.39** |
| flood insurance cost | 184 | 24.21 |
| how much is flood insurance | 151 | 22.85 |
| how much does flood insurance cost | 96 | 21.44 |
| flood insurance rates | 94 | 26.96 |
| cost of flood insurance | 83 | 21.43 |

**77% of the page's impressions sit at position 21 or worse, and every one of
those is an unqualified national query.** We rank top-5 whenever "California" is
in the query and nowhere otherwise.

That reframes the work. A California-branded page will not win "how much is flood
insurance" — but **statewidefloodinsurance.com exists precisely for that query**,
and is currently not competing for it. The national pool is going to the wrong
brand, or to nobody.

### And a third: the zone pages already outrank the cost pages

| page | impressions | position |
|---|---|---|
| `/which-flood-zone-requires-flood-insurance/` | 2,306 | **7.93** |
| `/navigating-flood-zone-x/` | 1,976 | **7.83** |
| `/flood-zone-ae/` | 1,686 | 14.56 |
| `/how-much-does-flood-insurance-cost/` | 2,866 | 18.15 |
| `/flood-insurance-rates/` | 1,445 | 25.50 |

Our zone content is on page one; our cost content is not. That is a strong
argument for bringing the cost data **into** the zone pages rather than only
building a better standalone cost page. `/navigating-flood-zone-x/` at 7.83 is the
single best home for an X-zone price the site has.

There is also unmet demand: **523 impressions across 83 zone-plus-price queries**
("how much is flood insurance in zone a" 33 @ 22.8, "flood zone ve insurance cost"
27 @ 13.0, "how much is flood insurance in zone ae" 26 @ 22.9, "zone ae flood
insurance rates" 24 @ 37.1), all at poor positions with zero clicks. People are
asking the zone-price question and nobody on our site answers it with a number.

## Our own pages contradict each other

Four different Zone X figures across four of our pages, none sourced, none from
our book:

| page | Zone X | overall |
|---|---|---|
| `/how-much-does-flood-insurance-cost/` | $400–$700 | $500–$2,000 |
| `/flood-insurance-rates/` | "as low as ~$350" | "about $780" |
| `/faqs/` | $400–$900 | — |
| `/flood-zone-ae/`, `/flood-zone-a/` | "much lower" | "about $780" |

The FAQ also prices Zone AE at $1,200–$3,000+ and gives a worked "$250K building,
Zone AE" example at ~$1,850/yr. **This must be reconciled before anything new
ships** — a visitor comparing two of our own pages currently gets two different
answers, and Google is choosing between them for us.

Encouragingly, the `/flood-insurance-rates/` figure of **"about $780 per year for
$250,000 of building coverage"** is close to my measured benchmark of **$822** at
$250,000 / $5,000 deductible (n=3,645). The editorial estimate was sound; it just
had no data behind it. Now it does.

## SOLVED: where the $475 comes from, and why I could not see it

Aaron, 13 Aug: *"private cherry picks the best properties and rates them
accordingly where the NFIP must take all properties… when we say 475, the premium
may be 350 and then with the policy fee and tax its around 475. BRIT QBE and
HISCOX all have low minimum premiums and X zones often all in that minimum
premium threshold."*

Both halves check out against the book, measured on 1,240 California policies.

**The policy fee is flat, not proportional.** $95 on 80.4% of rows and $65 on
18.8% — seven distinct values in total. At the median premium that is 13.6%, but on
a $350 premium it is 27%, which is why a small premium grosses up so much. So
$350 + $95 = $445, plus 3.18% California tax = **$459**. Aaron's $475 is the same
calculation with a slightly larger fee or premium. The arithmetic is right.

**There is a hard minimum premium of $250, and it is common to every carrier.**
QBE, Brit, RBIA and CFIS all show `min = $250.00` exactly. Who actually lands on it
differs sharply: **12.5% of Brit's rows sit at exactly $250** and its median is
$522, against QBE's $689 with no floor spike at all (its most common premium is
$715 at 4.2% — a smooth risk-rated distribution). So the floor is universal; the
low-risk business that reaches it is concentrated in Brit and Hiscox. That is
precisely what Aaron said.

**The California distribution is bimodal, and the low cohort is real:**

| percentile | premium | all-in |
|---|---|---|
| p1 | $250 | **$325** |
| p5 | $275 | **$351** |
| **p10** | **$362** | **$441** |
| p25 | $620 | $735 |
| p50 | $689 | $809 |
| p75 | $747 | $869 |

Note the shape. p5 → p10 climbs $90; p10 → p25 jumps **$294**. That gap is the
break between a minimum-premium cohort and the risk-rated mass. **10.5% of the
California book has a premium of $375 or less**, which is $475 or less all-in.

**Aaron's $475 is almost exactly the 11th percentile of our own book.** It is not a
guess and it is not an outlier — it is a real, sizeable tier we write constantly.

### The error this exposes in my earlier reading

I argued the book could not contain a $475 cohort because the benchmark IQR was a
tight $769–$888. That was wrong for an embarrassing reason: **the interquartile
range excludes the bottom quartile by construction.** I was looking at the middle
half of the distribution and concluding the whole thing was uniform. The low cohort
was sitting below p25 the entire time, exactly where an IQR cannot see it.

Lesson for anything published from this data: **report the low percentiles
explicitly, not just the median and IQR.** For a price page the bottom decile is
arguably the most commercially important number on the page, and it is the one an
IQR hides.

### The mechanism, which is the real argument

Aaron's first sentence is the strongest thing on this page and it is not about
price at all: **private carriers select which properties to write; the NFIP must
take every applicant.** Everything else follows from that.

- Private can decline a bad risk, so its book is better than average and it can
  price a preferred risk at a floor.
- The NFIP cannot decline anyone, so its rates must carry the risks private
  declined. That is not inefficiency, it is the statutory job.
- Which is why the honest version of the savings claim is *"we shop both and place
  whichever wins"* rather than *"private is cheaper"*. For a property private
  declines, the NFIP is not merely the better deal — it is the only deal.

This is publishable as-is, needs no data, and explains the gap without
disparaging the NFIP. It also sets up the "sometimes the NFIP is the right call"
section rather than contradicting it.

### What is now publishable without geocoding

- The bottom-decile all-in figure (**~$441**, p10) as *"about one in ten policies
  we place costs under $450 a year"* — a measured statement of fact.
- The **$250 minimum premium** as the structural floor, and the flat **$95 policy
  fee**, both of which explain why the cheapest policies cluster.
- What is still NOT publishable: calling that cohort *"Zone X"*. The floor is a
  pricing artefact, and whether the properties sitting on it are in X zones is
  exactly what the NFHL geocoding must confirm. Strong hypothesis, not a finding.

## An open question the data raises

My California benchmark is $822 with a **tight** IQR of $769–$888. A book genuinely
mixing $475 X-zone policies with $1,850 AE policies would be far more spread out
than that. Two possible explanations:

1. **The private market prices flatter across zones than the NFIP does** — private
   carriers rate on their own models (Intermap scores), so FEMA's zone boundaries
   matter much less to them. Our published zone ranges may be NFIP-shaped
   inherited knowledge, not descriptions of our own book.
2. **Hiscox is the low-risk book.** Hiscox's median is $507 / $212 per $100k —
   strikingly close to Aaron's ~$475 X-zone figure. "Hiscox is competitive in
   certain areas" may literally mean *low-risk areas*.

Both are testable, and the NFHL geocoding settles it. Until then neither goes on a
page. Worth knowing that if (1) holds, the private pitch is *stronger* in A zones
than in X zones, which is the opposite of the intuitive story.

## What nobody does — our opening

Kimi surveyed 38 pages. 16 price by zone, but only **four** combine per-zone
dollars, a zone lookup, and the mandate explanation. And **not one page anywhere**
combines all of:

1. an embedded address → zone lookup
2. per-zone California figures from **measured** data
3. **shaded vs unshaded X priced separately**
4. an explicit "this is optional for you" placed *next to* the X-zone price rather
   than buried in an FAQ

No carrier page segments by zone at all. FEMA's own cost page refuses to.

We can do all four, and we have something none of them have: **real private-market
premiums** rather than NFIP averages recycled from OpenFEMA.

## Build order

1. **Reconcile our own figures.** One number per cell, sourced, consistent across
   the cost page, rates page, FAQ and the zone pages. Nothing else ships first.
2. **NFIP zone × county table from FEMA.** Public, citable, immediately available.
   Gives every zone a defensible number and the like-for-like comparator.
3. **Put the X-zone price on `/navigating-flood-zone-x/`** (position 7.83). Fastest
   route to a page-one answer for the voluntary buyer.
4. **Cite the data.** Every top competitor names FEMA/OpenFEMA; our two pages cite
   nothing and carry no update date. Kimi's read is that attribution is the
   credibility line, and it is the cheapest thing on this list.
5. **Add tables.** Every page ranking on all four queries has county data, zone
   data, or a tool. Both our pages have zero tables.
6. **Split A from AE.** A $759 vs AE $1,334 is a real distinction almost nobody
   draws, and we have dedicated pages for both already ranking at 14.56.
7. **Decide the national queries.** 77% of the cost page's impressions are
   unqualified national terms a California brand cannot win. Either build the
   equivalent on statewidefloodinsurance.com or stop chasing them.
8. **Address → zone lookup**, once the desktop generator exists. This is the
   fourth leg nobody has.

## The claims statistic — verified, use this wording

Independently confirmed on FEMA's own site, not taken on trust:

> "Over the past 10 years (2014 - 2024), nearly one-third of NFIP flood insurance
> claims (29%) came from areas located outside of current high-risk flood areas"
> — [floodsmart.gov, What is My Flood Risk](https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk)

Aaron's 30% recollection was right. Corroborated by FEMA's F-435 brochure (Aug
2025) and NFIP Media Toolkit (Jul 2025), both saying "almost one-third, 2014–2024."

**Do not use "40%."** It was a **2015–2019 snapshot**, which FEMA's own TMAC annual
report confirms while its brochures still reprint it as "on average" with no period
attached. FEMA simultaneously publishes 20%, 25%, 29% and 40% on live pages, which
is why every number in that range can be "sourced to FEMA" — cite the 29% *with its
year range attached* and we are the ones who got it right.

Also drop the vague *"FEMA data consistently shows that 25–30%…"* currently on our
FAQ page in favour of the exact figure and URL.

Two FEMA pages we should never cite: the [low-risk zones FAQ](https://www.fema.gov/faq/low-risk-flood-zones)
and the [facts-and-myths blog](https://www.fema.gov/blog/facts-and-myths-about-flood-insurance).
Both still quote Preferred Risk Policy pricing that predates Risk Rating 2.0 — they
are stale on their face.

## Correction to my earlier figures

I had been citing the cost page as **19,311 impressions at position 17.4**. The
page-level truth from `gsc-2026-08-13/pages.csv` (13 May – 11 Aug 2026) is **2,866
impressions at 18.15, with 20 clicks**. Site-wide is 29,915 impressions, so the
19,311 was not the site total either; I cannot reconstruct where it came from and
have corrected it in all five files that carried it, plus the tool docstring.

The strategy is unaffected — at 2,866 the cost page is still the site's single
largest impression pool, which was the reason for prioritising it. But the number
was inflated nearly sevenfold and anything built on its magnitude should be
re-checked.
