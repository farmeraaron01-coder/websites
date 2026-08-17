# Apply: Florida cost section + hub private-market table

Two edits that did not land on the first attempt, plus one settings fix.
Verified against the live site 17 Aug 2026. Everything below is on
**statewidefloodinsurance.com**.

Nothing here touches Arizona, Oklahoma or Texas — those are applied and correct.
Do not re-edit them.

---

## Why these two failed last time

The hub instruction named a file that does not exist (`hub-cost-by-state.html`)
while two hub files sat in the folder. That is fixed — **there is now exactly one
hub file**, `hub-cost-table.html`.

The Florida instruction described a replacement boundary that was ambiguous
about where the section ended. That is fixed below by naming both edges
explicitly.

**Both target pages currently serve the original content.** Verified with
`x-proxy-cache: MISS`, so this is what WordPress generates, not a cached copy.
If a previous attempt left a draft or an unsaved revision, discard it and work
from the published version.

---

## Edit 1 — Florida cost section

**Page:** `https://statewidefloodinsurance.com/florida-flood-insurance/`
**Paste in:** `pages/florida-cost-section.html` (6,045 bytes, 30 non-blank lines)

### The boundary

Delete everything from the heading

> **How much does flood insurance cost in Florida?**

down to **but not including** the next heading

> **Private flood insurance vs. the NFIP in Florida**

The block you are deleting is the **already-updated section, about 5,576
bytes**. It should contain:

1. the `How much does flood insurance cost in Florida?` H2
2. a paragraph citing `342 Florida properties` and a `$681` median
3. a four-row zone table (Zone X, AE, AH, A) with a `<caption>`
4. three H3s: `Where the federal programme runs out`, `The widest spread in the
   country`, `Most Florida buyers are outside the floodplain`
5. a closing paragraph beginning `Compare Florida against every state we track`

It should **not** contain the old risk-profile table (`~$400 – $1,200`,
`~$2,000 – $15,000+`) — that is already gone.

If what you are about to delete does not match, stop and report what you see.

### Then paste the replacement file in its place

Paste the **entire** contents of `pages/florida-cost-section.html`.

- First line is `<h2 id="how-much-does-flood-insurance-cost-in-florida">How much does flood insurance cost in Florida?</h2>`
- Last line is `<p>Compare Florida against every state we track in our <a href="/flood-insurance-cost-by-state/">flood insurance cost by state</a> table.</p>`

This swap changes exactly two things:

- **Restores the `/private-flood-insurance-cost/` in-body link.** The current
  live section dropped it. It survives only in the site navigation, which is not
  a contextual link. The revised file reproduces the paragraph verbatim, second
  from the end.
- **Softens the Zone AE claim.** `$895` in Florida against `$892` in Texas is a
  $3 gap on samples of 103 and 108, which does not support calling Florida the
  most expensive AE median in the book. It now reads as effectively tied.

The next heading, `Private flood insurance vs. the NFIP in Florida`, and every
section after it stay exactly as they are.

---

## Edit 2 — Hub private-market table — ✅ ALREADY DONE, SKIP

Verified 17 Aug: the hub serves **two tables**, and `$681`, `$670` and `$465`
are all live. It matches `hub-cost-table.html`. **Do not re-apply it** — a second
paste would duplicate the table.

The instructions below are kept only as a record of where it was placed.

<details><summary>Original instruction (do not run)</summary>

**Page:** `https://statewidefloodinsurance.com/flood-insurance-cost-by-state/`
**Paste in:** `hub-cost-table.html` (8,555 bytes, 47 non-blank lines)

### This is an ADDITION. Delete nothing.

The existing NFIP table and its `Flood insurance cost & risk by state (2026)`
heading stay exactly where they are. The new table goes **after** them, as a
second table.

### The insertion point

Scroll to the end of the existing NFIP table. Immediately after the table there
is one italic paragraph beginning:

> *Private flood insurance is frequently 30–50% below these NFIP figures*

Paste **immediately after that italic paragraph** and **immediately before** the
heading:

> **The hidden coverage gap**

Nothing between those two markers should be removed — there is nothing between
them today.

### What you are pasting

The whole of `hub-cost-table.html`.

- First line is `<h2 id="what-private-flood-insurance-actually-costs-by-state">What private flood insurance actually costs, by state</h2>`
- It contains one H2, one 27-row table, a `A note on California.` paragraph and
  a closing `The pattern worth noticing:` paragraph
- Last line begins `<p><strong>The pattern worth noticing:</strong> Zone AE prices very differently by state.`

The file opens by explicitly framing itself against the table above it — *"The
table above reports NFIP premiums … This one reports something different"* —
so the two tables read as a deliberate pair rather than a contradiction. That
framing only works if it is placed after the NFIP table, not before it.

</details>

---

## Edit 3 — Release the Rank Math sitemap cache

Arizona and Oklahoma are live and indexable but appear in **neither** sitemap.
`page-sitemap.xml` still reports `lastmod` of **2026-08-05**, so it has not
regenerated since they were published. This is the Rank Math sitemap cache, not
a publishing error.

> Rank Math → Sitemap Settings → General → **Links Per Sitemap: 200 → 199 →
> Save**, then **199 → 200 → Save**

Two saves. A save with nothing genuinely changed is a no-op and will not clear
it. "Remove transients" does not clear it either.

---

## Editing traps that broke earlier attempts

- **Never put an apostrophe, quote, en dash, em dash or ellipsis in a FIND
  string.** `wptexturize` converts them on render, so a string copied from the
  live page will not match what is stored. Anchor on punctuation-free words.
  Entities are fine on the paste side — the files already use them.
- **Prefer single-line finds.** `wpautop` normalizes whitespace between tags, so
  multi-line blocks containing tables rarely match verbatim.
- **Do not retype or reflow the HTML.** Paste the files byte for byte.
- **Save, then verify logged out.** Logged-in requests bypass the page cache, so
  wp-admin will show you what WordPress thinks rather than what Google receives.

---

## Verification — anonymously AND with a cache-busting query string

**Anonymous is not enough on this account.** A plain `curl` of these URLs
returned pre-edit content while the origin already had the edits — and the
response header read `x-proxy-cache: MISS`, which normally means a fresh origin
fetch. It produced a confident, wrong "not applied" verdict on 17 Aug.

Always append a unique query string. It changes the cache key, so the request
reaches PHP and shows what WordPress is actually generating:

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CB="?cb=$(date +%s%N)"          # unique every run — this is the load-bearing part

# Florida: expect 342, 681, 895, 617, 1,643 and exactly one <h1>
curl -sSL -A "$UA" "https://statewidefloodinsurance.com/florida-flood-insurance/$CB" \
  | grep -oE '342|\$681|\$895|\$617|\$1,643|<h1' | sort | uniq -c

# Hub: expect TWO tables, and the private medians
curl -sSL -A "$UA" "https://statewidefloodinsurance.com/flood-insurance-cost-by-state/$CB" \
  | grep -oE '<table|\$681|\$670|\$465|\$547' | sort | uniq -c

# Sitemap: expect arizona and oklahoma to appear, and lastmod to move off 2026-08-05
curl -sSL -A "$UA" "https://statewidefloodinsurance.com/page-sitemap.xml$CB" \
  | grep -oE '<loc>[^<]*(arizona|oklahoma)[^<]*'
```

A useful cross-check: fetch the URL with and without the query string and
compare byte sizes. If they differ, the cached copy is stale and only the
query-string number reflects reality.

Pass conditions:

| Check | Expected |
|---|---|
| Florida `$681` | present |
| Florida `<h1>` | exactly 1 |
| Florida old figures `~$400 – $1,200`, `~$2,000 – $15,000+` | **gone** |
| Hub `<table` | exactly 2 |
| Hub `$681` `$670` `$465` `$547` | all present |
| Hub `~$700 – $1,363` | **still present** — it belongs to the NFIP table |
| page-sitemap arizona + oklahoma | both present |

That last row is the one that fooled the previous verification pass. `~$700 –
$1,363` being on the hub proves the **NFIP** table is there. It says nothing
about whether the private table was added. Check for `$681`.

---

## One judgement call left for a human

The preserved Florida paragraph claims private flood *"often runs 10–30% (and in
many cases 30–50%) below the NFIP rate."* Our own book does not clearly support
a number that specific: on a like-for-like comparison private wins about **48%**
of the time, at a median of **$1,380** when it does win.

The claim is pre-existing published copy, so this edit keeps it verbatim rather
than changing it as a side effect. But it is worth revisiting deliberately —
the same overstatement is on the hub, in the `frequently 30–50% below` italic
line above the insertion point.
