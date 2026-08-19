# Apply round 2 — zone reporting threshold, and two false claims

Five pages. All of this is a **correction to already-published content**, so it
should go up as one batch rather than trickling out.

---

## Why

The published Florida table showed **Zone X $617 above Zone A $562** — low risk
apparently costing more than high risk. Checked against all 81 state-zone rows:

- Zone X prices **below** Zone A in **14 of the 17** states where both are
  reported. California is decisive — X $516 from 455 properties against A $711
  from 480.
- It inverts in exactly three states, **Florida, Texas and Arizona**, and in all
  three the Zone A sample is tiny against Zone X: **24 vs 198**, 32 vs 212,
  36 vs 32.
- Zone AE above Zone X holds in **25 of 25** states.

The inversions are sampling noise. The fix is a reporting threshold:

> **A zone median is published only where at least 50 properties were quoted in
> that zone** — the same threshold a state already has to clear to appear in the
> hub at all.

That drops 51 of 81 zone rows and leaves 8 states with no zone detail. That is
the correct outcome: those medians were never stable enough to publish.

## Two factual errors found while fixing this

Both are live right now and both are mine:

- **Arizona page opened "Arizona is the cheapest state in our book."** It is
  eighth cheapest of 27. Michigan is $369, Oklahoma $465, Arizona $547.
- **Oklahoma page opened "Oklahoma is the least expensive state in our book, and
  by a clear margin."** It is second, behind Michigan.

Corrected to "one of the least expensive states in our book" and "the second
least expensive state in our book, behind only Michigan."

---

## What to change, page by page

### 1. Florida — `/florida-flood-insurance/`
Replace the cost section again with `pages/florida-cost-section.html`.
Same boundary as last time: from the **How much does flood insurance cost in
Florida?** heading down to but not including **Private flood insurance vs. the
NFIP in Florida**.

Table goes from four zone rows to two: **Zone AE $895 (103)** and **Zone X $617
(198)**. Zones A and AH are removed and the caption now says why. Everything else
in the section is unchanged.

### 2. Texas — `/texas-flood-insurance/`
Replace the cost section with `pages/texas-cost-section.html`. Boundary: from
**How much does flood insurance cost in Texas?** down to but not including the
next heading.

Table goes from three rows to two: **Zone AE $892 (108)** and **Zone X $614
(212)**. Zone A removed.

### 3. Arizona — `/arizona-flood-insurance/`
**Replace the whole page body** with `pages/arizona-flood-insurance.html`. Too
many separate changes to patch safely.

Only Zone AE clears 50 in Arizona, so the zone table is replaced by a
**percentile spread** table (10th $398, 25th $464, median $547, 75th $800). The
section built on the old zone figures is rewritten: the "$23 range between
zones" and "about $13 a year" claims are gone — those were differences well
inside the sampling error of samples of 23 to 36. The heading changes from
*"The Arizona pattern: the zones barely separate"* to *"The Arizona pattern:
your address, not your zone."* The Zone X FAQ no longer quotes a zone price.

### 4. Oklahoma — `/oklahoma-flood-insurance/`
**Replace the whole page body** with `pages/oklahoma-flood-insurance.html`.

No Oklahoma zone clears 50, so the zone table becomes a percentile spread (10th
$302, 25th $350, median $465, 75th $675, 90th $1,109). The claim *"Zone X at
$372 is the cheapest single figure anywhere in our national book"* is removed —
it rested on 23 properties. The Zone X FAQ is rewritten around the FEMA
out-of-zone claims statistic and the statewide median instead.

### 5. Hub — `/flood-insurance-cost-by-state/`
Replace the **private-market table only** — the second table, the one added last
round. Use `hub-cost-table.html`. The original NFIP table above it is untouched.

The **By Flood Zone** column now lists only zones with 50+ quotes; eight states
read *"Not enough quotes per zone to report."* The caption's methodology
sentence changes from "at least 10 properties" to the 50 threshold, with the
reason.

---

## Verify — cache-busted

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CB="?cb=$(date +%s%N)"
S=https://statewidefloodinsurance.com

# no page should contain a Zone A or Zone AH median any more
for u in florida-flood-insurance texas-flood-insurance arizona-flood-insurance oklahoma-flood-insurance; do
  echo "== $u"; curl -sSL -A "$UA" "$S/$u/$CB" | grep -oE '\$(562|582|558|568|464|519|470|372|824)' | sort -u
done

# hub: expect the threshold sentence and eight "Not enough quotes" cells
curl -sSL -A "$UA" "$S/flood-insurance-cost-by-state/$CB" | grep -c "Not enough quotes per zone"
curl -sSL -A "$UA" "$S/flood-insurance-cost-by-state/$CB" | grep -c "at least 50 properties"
```

| Check | Expected |
|---|---|
| Florida `$562`, `$824` | gone |
| Texas `$582` | gone |
| Arizona `$558`, `$568` | gone — `$464` stays, it is now the 25th percentile |
| Oklahoma `$519`, `$470`, `$372` | all gone |
| Arizona `$581` | **stays** — Zone AE clears 50 at n=107 |
| Hub "Not enough quotes per zone" | 8 |
| Hub "at least 50 properties" | 1 |
| Arizona opening line | no longer says "the cheapest state" |
| Oklahoma opening line | says "second least expensive… behind only Michigan" |

---

## Charts

`charts/` already reflects this threshold. Florida and Texas keep an AE-vs-X bar
chart; Arizona and Oklahoma have no chartable zone and get a percentile spread
instead. If the charts go up in the same pass, they will agree with the tables.
