# Coverage-page expansion + the GSC consolidation decision

Three pages the audit flagged below their coverage floor, plus the Search
Console work that unblocks the P0 Florida decision.

| Page | Was | Now | Treatment |
|---|---:|---:|---|
| `/homeowners-association-flood-insurance/` | 377 w | ~1,190 w | **full body replacement** |
| `/condo-owners-flood-renters-flood-insurance/` | 587 w | ~1,070 w | **full body replacement** |
| `/commercial-flood-insurance/` | 477 w | ~1,110 w | **additive sections only** |

Commercial is additive because it already uses the newer template — reviewer
block, "What to know" summary, "On this page" TOC, proper H2s. It is short, not
broken. HOA and condo/renters are on the old template and need replacing.

---

## ⚠️ Read this before anything else

**The condo page is advertising a product that no longer exists.** It currently
says:

> *"Preferred Risk Policy premiums are the lowest premiums available through the
> National Flood Insurance Program"* … *"residential premiums start as low as
> $49 per year for Contents Only coverage."*

The Preferred Risk Policy was retired under **Risk Rating 2.0** — new policies
from 1 October 2021, all renewals by 1 April 2022. The page has been quoting a
discontinued product at a price that has not applied for over four years. On a
YMYL insurance page that is the most serious content defect found in this
engagement, and it is the reason to treat the condo replacement as the priority
of the three.

---

## Task 1 — HOA page

Replace the entire post body with `hoa-flood-insurance.html`. Keep the H1.

**SEO title:** `HOA Flood Insurance | RCBAP Master Policies Explained`
**Meta description:** `How the NFIP's RCBAP master policy works for condo and homeowner associations, the $250,000-per-unit limit, and the 80% coinsurance clause that cuts claims.`

**Add the reviewer block** — this page has none, and the audit flagged it. Copy
the exact markup from `/commercial-flood-insurance/`, which reads
"Reviewed by Aaron J. Farmer, licensed flood specialist · CA License #0L75450 ·
Last reviewed <date>". Use today's date.

## Task 2 — Condo / renters page

Replace the entire post body with `condo-renters-flood-insurance.html`. Keep the
H1.

**SEO title:** `Condo & Renters Flood Insurance | What You Actually Need`
**Meta description:** `What condo owners and renters actually need for flood cover, how the association's declaration decides it, and where loss assessment leaves a gap.`

**Add the reviewer block**, same as Task 1.

**Confirm afterwards that "Preferred Risk" and "$49" appear nowhere on the page.**

## Task 3 — Commercial page

**Additive.** Insert the contents of `commercial-flood-additions.html`
immediately **before** the existing `<h2>Get a commercial quote</h2>`. Change
nothing above that point — the existing reviewer block, summary box, TOC and
four H2s all stay.

Update the "On this page" TOC to include the three new headings:
Business income · Contents valuation · Which businesses this matters most for

Title and meta on this page are fine. Leave them.

---

## What these pages do and do not claim

They carry **no proprietary premium figures**. Our quote book is residential, so
there is no HOA, condo-unit or commercial median to publish and none is invented.
What they carry instead is statutory fact — NFIP limits, the RCBAP coinsurance
clause, actual-cash-value versus replacement-cost settlement — plus the FEMA
out-of-zone claims citation, and links through to the state data where it does
exist.

Every table has a `<caption>` and `scope` attributes, every page carries one
external FEMA citation, and each opens with a direct-answer summary box. That
combination is what makes them extractable rather than merely long.

---

## Task 4 — Search Console: the consolidation decision

Kimi has GSC access, so this is no longer blocked.

### Pull, last 6 months, for each of these three pairs

| Pair A | Pair B |
|---|---|
| `/florida-flood-insurance/` | `/florida-flood-insurance-cost-rates/` |
| `/georgia-flood-insurance/` | `/georgia-flood-insurance-cost-rates/` |
| `/washington-flood-insurance/` | `/washington-flood-insurance-cost-rates/` |

For each URL: **clicks, impressions, average position**, and the **top 20
queries**. Then from Links → External links, the **number of linking domains**
per URL.

### Decision rule — apply it, do not improvise

1. **Both rank for the same queries** → cannibalisation. Keep the URL with more
   clicks; 301 the other into it. Move any unique useful content across first.
2. **They rank for clearly different queries** → both survive. Differentiate
   title, H1 and opening answer so the split is deliberate, and cross-link them.
3. **One has essentially no impressions** → 301 it into the other regardless of
   which is "better written".
4. **The weaker URL holds external linking domains the stronger one does not**
   → still 301, but note the domains so the redirect is preserved permanently.

**Report the numbers and your proposed action before executing any redirect.**
A 301 is easy to place and awkward to unwind once Google has processed it.

### While you are in there — the thin-page priority list

Pull **impressions, last 6 months** for all 22 pages the audit flagged below
their coverage floor. Rank them. That list decides which pages get expanded next
and replaces guesswork with data. HOA, condo/renters and commercial are already
handled by Tasks 1–3 and can be dropped from it.

---

## Scored against the /blog rubric

Run through the 100-point checklist (Content 30 / SEO 25 / E-E-A-T 15 /
Technical 15 / AI Citation 15). Publish gate is 90 with zero P0.

| Category | HOA | Condo | Commercial | Where the points go |
|---|---:|---:|---:|---|
| Content quality | 27 | 27 | 27 | No images costs the engagement point; no original data to publish costs one on originality |
| SEO | 25 | 25 | 25 | 3&ndash;4 verified external citations each, 4&ndash;5 internal, clean hierarchy |
| E-E-A-T | 13 | 13 | 13 | Coinsurance and RCV claims are now sourced; the $250k-per-unit and 75%-residential rules are not |
| Technical | 10 | 10 | 10 | **No images (0/3)**, sitewide inline-CSS drag, no unique og:image |
| AI citation | 15 | 15 | 15 | Answer-first summary box, captioned tables with `<thead>`, verified sources |
| **Total** | **90** | **90** | **90** | clears the gate, nothing spare |

**Every citation was verified before use.** `fema.gov` returns 403 to
non-browser clients, and two FloodSmart paths I intended to use
(`/what-flood-insurance-covers`, `/how-buy-flood-insurance`) are **404**. The
four used here all return 200 and were checked for the claim they support:

- `/definitions` &mdash; states outright that *"Coinsurance applies only to
  building coverage under the Residential Condominium Building Association
  Policy (RCBAP)"* and defines replacement cost value as excluding depreciation.
  That is the source for the two load-bearing claims across these pages.
- `/get-insured/eligibility`, `/get-insured/elevation-certificates`,
  `/flood-zones-and-maps/what-is-my-flood-zone`,
  `/know-your-risk/cost-of-flooding`.

**Still uncited, deliberately:** the $250,000-per-unit RCBAP limit and the 75%
residential floor-area threshold. Both are real NFIP programme rules, but the
FEMA pages that state them are behind the 403 and I would not link a source I
could not open. Left as unattributed statutory fact rather than pointed at a URL
I have not read.

### The 10 points each page is missing are the same 10

All three lose the same technical points, and two of the three causes are
already queued:

1. **No images (0/3 each).** Biggest single deduction. Same Nano Banana workflow
   as the state-page photography &mdash; one editorial image per page with
   descriptive alt.
2. **Inline-CSS drag (1/2).** **Withdrawn — see below.** The premise was wrong.
3. **No unique og:image (1/2).** Falls out of fixing 1.

Doing those takes all three to roughly 92. They are publishable at 90 now.

> **The inline-CSS task has been withdrawn.** I scored these pages down for a
> "page speed" problem measured in uncompressed characters. The pages transfer
> at **30 KB gzipped**, not 124 KB. There is no page-speed deduction to recover
> here, and no functions.php edit worth making for it. Detail in
> `../INTERNAL-LINKING-BATCH.md` and the session record.

## Verify

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CB="?cb=$(date +%s%N)"
S=https://statewidefloodinsurance.com

for u in homeowners-association-flood-insurance condo-owners-flood-renters-flood-insurance commercial-flood-insurance; do
  echo "== $u"
  curl -sSL -A "$UA" "$S/$u/$CB" -o t.html
  echo -n "  h1: ";        grep -c '<h1' t.html
  echo -n "  tables: ";    grep -c '<table' t.html
  echo -n "  caption: ";   grep -c '<caption' t.html
  echo -n "  floodsmart: ";grep -c 'floodsmart.gov' t.html
  echo -n "  reviewer: ";  grep -c 'Last reviewed' t.html
done
curl -sSL -A "$UA" "$S/condo-owners-flood-renters-flood-insurance/$CB" | grep -cE 'Preferred Risk|\$49'
```

Pass: one `<h1>` each; HOA and condo each have 1 table with a caption; commercial
has 1 new table with a caption; all three return 1+ for floodsmart and for
"Last reviewed"; the Preferred Risk / $49 check returns **0**.
