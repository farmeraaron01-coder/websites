# Quote-book analysis — ITD_Quote_Report_081626.xlsx

Analyzed 16 Aug 2026. Source: inception-to-date export from the API-connected
quoting system (carriers: Brit, Brit MVP, QBE, Aon Edge, Hiscox FullValue /
NFIP / Custom / Excess). Raw file contains PII (names, street addresses) and is
**not** committed to this repo; only aggregates are. Aggregation used a hashed
street+ZIP property key so repeat quotes on one property count once.

## Dataset shape

| | |
|---|---|
| Quote transactions | 9,141 (all unique QuoteRefs) |
| Unique properties | 7,049 |
| Sale dates | **27 Feb 2025 → 14 Aug 2026** (~18 months) |
| Geography | Nationwide book — CA 4,062 rows, then WA, TX, FL, OR, AZ… |
| Bound rows | 3,331 (SaleComplete + PolicyNumberGenerated) |
| **CA bound, deduped** | **1,665 properties** (763 new business + renewals) |
| Transaction types | ~100% "OP" — no endorsement deltas polluting premiums |

"All-in" here = TaxableAmount (premium + policy fee of $95/$100/$125) +
surplus-lines tax (3%) + stamping fee + fire-marshal tax — i.e., the customer's
actual annual outlay. Note this book is **surplus-lines private flood**; the
published page's "all-in" definition mentions NFIP fee components (reserve fund
assessment, federal surcharge), which don't exist here. The page's definition
needs rewording if these numbers replace the old ones.

## 1. Zone table — published vs. this dataset

CA · bound · new business · one row per property (n=763):

| Zone | Published (291-policy table) | This dataset median | n | p25–p75 |
|---|---|---|---|---|
| AE | $650 | **$722** | 375 | $574–$877 |
| X | $465 | **$509** | 101 | $464–$702 |
| AO | $625 | **$569** | 114 | $464–$719 |
| A | $625 | **$588** | 117 | $464–$764 |
| AH | $700 | **$733** | 30 | $542–$1,010 |
| D | $725 | $1,174 | **4** | — |
| A99 | $548 | *absent* | 0 | — |
| A (numbered, A1–A30) | — | $623 | 22 | $499–$847 |

The old table is directionally sound — five of seven zones within ±$75. The
current book prices AE and X somewhat higher, AO/A somewhat lower.

**Recommendations:** publish the new numbers with the honest window
("bound Feb 2025–Aug 2026"); drop the Zone D row (n=4 both then and now — a
median of 4 policies is noise); drop or footnote A99 (none in the current
system); fold numbered A-zones into Zone A or footnote them.

## 2. NFIP comparison — CORRECTED after Aaron's clarification

`HiscoxNFIPPurePremium` is **not** the customer's NFIP price. Per Aaron
(16 Aug 2026): it's a reference quote at the old NFIP Preferred Risk Policy
structure — a fixed **$250k building / $100k contents** — kept for customers
who remember that product (discontinued under Risk Rating 2.0).

That kills the first-pass stat ("private cheaper 78%, median saving $473"):
77% of the CA bound book is **building-only ($0 contents)**, so that comparison
pitted real building-only policies against a reference carrying $100k of
contents the customer never buys. Retracted; do not publish it.

Honest versions, from the same data:

| Comparison | n | Private cheaper | Median saving when it wins |
|---|---|---|---|
| True like-for-like ($250k/$100k both sides) | 90 | **48%** | **$1,380/yr** |
| $250k building, contents ≥ $50k | 185 | 65% | $849/yr |

The defensible claim is not "private is cheaper" — it's **"you can't know
which side wins without quoting both, and when the private side wins, it wins
big."** Coin-flip odds, fat-tailed payoff.

The page's existing "clients save $300–600/yr against the federal policy"
claim **cannot be verified from this export** — it contains no real NFIP
quotes, only the fixed-structure reference. It stands as Aaron's
experience-based claim from actual NFIP quoting; left on the page, flagged
here for awareness.

Also checked: the "NFIP caps building at $250k" angle is weak in this book —
only 7% of CA bound properties carry building limits above $250k, and 70% sit
at exactly $250k.

## 3. No single market wins — the case for shopping

Among CA bound rows where ≥2 markets returned a quote (n=1,857), the cheapest
market was:

| Market | Wins |
|---|---|
| Hiscox Custom | 26% |
| Brit | 26% |
| QBE | 21% |
| Hiscox FullValue | 12% |
| Brit MVP | 11% |
| Aon Edge | 4% |

No market wins even 3 in 10. This is the strongest new marketing stat in the
dataset: *"the cheapest flood market is different for every property — that's
why we quote them all."* (Caveat: Aon Edge only returned quotes on 27% of rows,
so its low share partly reflects participation, not just price.)

## 4. Zone X behavior

Property-level quote→bind: mandatory zones bind at 57–59%; **Zone X binds at
26%**. People shop voluntary coverage and walk away — consistent with the
page's whole Zone X argument, and a good retargeting insight (a Zone X quote
that didn't bind is a warm lead, not a lost one).

## 5. Other facts worth using

- **Deductible mix (CA bound):** $5,000 = 91%, $2,000 = 4%, $1,000 = 3%,
  $10,000 = 2%. The page lists "($1,000, $2,500, $5,000)" — $2,500 barely
  exists in the book; it's $2,000. Minor copy fix.
- **Occupancy (CA bound):** Primary 1,043 · Rental 536 · Secondary 42. Nearly a
  third of the book is landlord business — possible content angle
  (rental-property flood insurance page).
- **Renewals price higher than new business** (AE median $764 vs $722) —
  expected with rate change, worth watching, not publishing.
- **City medians** (CA bound, deduped, n≥10) in `data/city-medians-ca-bound.csv`
  — real local numbers for the city pages: Los Angeles $748 (n=71), San Rafael
  $751 (n=58), Huntington Beach $784 (n=53), San Jose $805 (n=47), San Diego
  $722 (n=45), Long Beach $748 (n=41), Sacramento $702 (n=21), plus 17 more.
  City = insured mailing city, which for homeowners ≈ property city; flag if a
  large mailing-elsewhere segment exists.

## Decisions — resolved 16 Aug 2026

1. **Date window:** Aaron approved publishing as "policies bound 2025–2026",
   n=763. Applied to `post-body.revised.html`. The 299-vs-291 question is moot.
2. **`HiscoxNFIPPurePremium`:** clarified — fixed $250k/$100k PRP-style
   reference, not the customer's NFIP price. Section 2 corrected accordingly.
3. **Zone D / A99 / V-VE rows:** dropped from the table; covered by a single
   "too few bound to publish" note that links the V/VE page.
4. **"All-in" definition:** rewritten to premium + policy fee + surplus lines
   taxes and fees. Aaron confirmed the NFIP carries its own federal fees that
   private policies don't (private has our policy fee instead).

## Files

| File | Contents |
|---|---|
| `data/zone-medians-ca-bound-nb.csv` | Zone medians + quartiles, CA bound new business, deduped |
| `data/zone-medians-ca-bound-all.csv` | Same incl. renewals |
| `data/city-medians-ca-bound.csv` | City medians, CA bound, deduped, n≥10 |

Raw export and the anonymized row-level working file live outside the repo.
Delete the uploaded XLSX from the session when done — it contains PII.
