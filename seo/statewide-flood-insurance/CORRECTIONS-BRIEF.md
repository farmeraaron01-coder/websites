# Corrections brief — statewidefloodinsurance.com

**Five pages. All corrections to already-published content.** Publish as one
batch so the site is never internally inconsistent.

You are given five HTML files. Each replaces a specific region of a specific
page. Nothing else on any page changes, and no Rank Math metadata, title, slug
or meta description changes anywhere in this job.

---

## Ground rules

1. **Paste the attached files byte for byte.** Do not retype, reformat, reflow
   or "tidy" the HTML. Do not convert `&#8217;` or `&mdash;` back to characters.
2. **Never put an apostrophe, quotation mark, en dash, em dash or ellipsis in a
   search string.** WordPress converts these on render, so text copied from the
   live page will not match what is stored. Anchor searches on plain words.
3. **Prefer single-line searches.** WordPress normalises whitespace between
   tags, so multi-line blocks containing tables rarely match verbatim.
4. **Stop and report rather than guess.** Each task lists what you should find
   before editing. If it does not match, change nothing and say what you saw.
5. **Verify logged out, with a cache-busting query string.** Logged-in requests
   bypass the cache, and on this host a plain anonymous request has returned
   stale content while reporting `x-proxy-cache: MISS`. Append `?cb=12345` with
   a different number each time.

---

## Why these changes

The Florida table published **Zone X at $617 above Zone A at $562** — low-risk
flood zone apparently costing more than high-risk. That is backwards, and it is
a sampling artifact: the Zone A figure came from 24 properties, the Zone X
figure from 198.

Across all 27 states, Zone X prices below Zone A in 14 of the 17 states where
both are reported, and California settles it at X $516 from 455 properties
against A $711 from 480. The rule now applied everywhere:

> **A zone median is published only where at least 50 properties were quoted in
> that zone** — the same threshold a state must clear to appear in the hub.

Two false claims were also found and are corrected below.

---

## Task 1 — Florida cost section

**Page:** `https://statewidefloodinsurance.com/florida-flood-insurance/`
**File:** `florida-cost-section.html` (5,442 bytes)

**Replace from** the heading `How much does flood insurance cost in Florida?`
**down to but not including** the heading `Private flood insurance vs. the NFIP
in Florida`.

**Before editing, confirm the region contains:** a four-row zone table with rows
`Zone AE`, `Zone AH`, `Zone X`, `Zone A`, and the figures `895`, `824`, `617`,
`562`.

**After:** the table has **two rows only** — Zone AE `$895` (103 properties) and
Zone X `$617` (198 properties). The caption explains that Zones A and AH are
excluded for having 24 and 13 properties. Everything after the replaced region
is untouched.

---

## Task 2 — Texas cost section

**Page:** `https://statewidefloodinsurance.com/texas-flood-insurance/`
**File:** `texas-cost-section.html` (4,664 bytes)

**Replace from** the heading `How much does flood insurance cost in Texas?`
**down to but not including** the next heading.

**Before editing, confirm:** a three-row zone table containing `892`, `614` and
`582`.

**After:** two rows — Zone AE `$892` (108) and Zone X `$614` (212). Zone A is
gone.

---

## Task 3 — Arizona, whole page body

**Page:** `https://statewidefloodinsurance.com/arizona-flood-insurance/`
**File:** `arizona-flood-insurance.html` (7,417 bytes)

**Replace the entire page body.** There are too many separate changes to patch
safely. Keep the page title, slug and all Rank Math fields exactly as they are.

**Before editing, confirm the current page contains:** a zone table with `581`,
`558`, `568` and `464`, and the phrase `Arizona is the cheapest state in our
book`.

**After, the page should:**

- open `Arizona is one of the least expensive states in our book` — it is eighth
  of 27, not first
- show a **percentile spread** table (10th `$398`, 25th `$464`, median `$547`,
  75th `$800`) in place of the zone table
- carry the heading `The Arizona pattern: your address, not your zone`
- **no longer contain** `558`, `568`, or the claims about a `$23` range between
  zones or a saving of about `$13` a year
- still contain `581` once — Zone AE clears the 50-property threshold at 107

---

## Task 4 — Oklahoma, whole page body

**Page:** `https://statewidefloodinsurance.com/oklahoma-flood-insurance/`
**File:** `oklahoma-flood-insurance.html` (7,566 bytes)

**Replace the entire page body.** Keep title, slug and Rank Math fields as they
are.

**Before editing, confirm:** a zone table with `519`, `470` and `372`, and the
phrase `Oklahoma is the least expensive state in our book`.

**After, the page should:**

- open `Oklahoma is the second least expensive state in our book, behind only
  Michigan`
- show a percentile spread table (10th `$302`, 25th `$350`, median `$465`, 75th
  `$675`, 90th `$1,109`)
- **no longer contain** `519`, `470` or `372`, including in the FAQ

---

## Task 5 — Hub private-market table

**Page:** `https://statewidefloodinsurance.com/flood-insurance-cost-by-state/`
**File:** `hub-cost-table.html` (8,781 bytes)

The hub has **two tables**. The first is the NFIP table — **do not touch it.**

**Replace the second table only**, the private-market one. It begins with the
heading `What private flood insurance actually costs, by state` and ends with
the paragraph beginning `The pattern worth noticing`. Replace from that heading
through that paragraph.

**Before editing, confirm** the second table's rightmost column currently lists
several zone medians per state, for example a Michigan row reading roughly
`AE $369 · X $367 · A $469`.

**After:**

- the **By Flood Zone** column lists only zones with 50 or more quotes
- **eight states** read `Not enough quotes per zone to report`
- the caption says zone medians are shown only where **at least 50 properties**
  were quoted, replacing the old wording `at least 10 properties`
- the NFIP table above is unchanged, still showing Florida at `~$700 – $1,363`

---

## Verification — run logged out

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CB="?cb=$(date +%s%N)"
S=https://statewidefloodinsurance.com

for u in florida-flood-insurance texas-flood-insurance arizona-flood-insurance oklahoma-flood-insurance; do
  echo "== $u"
  curl -sSL -A "$UA" "$S/$u/$CB" | grep -oE '\$(562|582|558|568|519|470|372|824)' | sort -u
done

curl -sSL -A "$UA" "$S/flood-insurance-cost-by-state/$CB" | grep -c "Not enough quotes per zone"
curl -sSL -A "$UA" "$S/flood-insurance-cost-by-state/$CB" | grep -c "at least 50 properties"
```

| Check | Expected |
|---|---|
| Florida `$562` and `$824` | gone |
| Texas `$582` | gone |
| Arizona `$558` and `$568` | gone |
| Arizona `$464` | **still present** — it is now the 25th percentile |
| Arizona `$581` | **still present** — Zone AE clears the threshold |
| Oklahoma `$519`, `$470`, `$372` | all gone |
| Hub `Not enough quotes per zone` | **8** |
| Hub `at least 50 properties` | **1** |
| Hub tables | still **2** |
| Hub `~$700 – $1,363` | **still present** — it belongs to the NFIP table |
| Every page | exactly one `<h1>` |

The last two rows matter. `~$700 – $1,363` proves only that the NFIP table
survived; it says nothing about the private table. And a hub with one table
means the replacement overwrote the wrong one — revert and retry.

---

## Stop conditions

Stop, change nothing further, and report if:

- a before-state above does not match what is on the page
- the hub ends up with anything other than two tables
- an `<h1>` count on any page is not exactly 1
- a replacement boundary is ambiguous — for example the Florida heading appears
  more than once outside the on-page contents list
