# Brief for ChatGPT — two reference tables

Paste everything below the line. Both are factual lookups. Neither needs access to
our data, and both are things I can validate the moment they come back — so
accuracy matters far more than speed.

---

## Context

I am building a table of average flood insurance costs for every California
county, using FEMA's public NFIP policy data. FEMA identifies counties by **FIPS
code** (a five-digit number like `06037`), not by name. To publish a table a human
can read, I need a complete and correct code-to-name mapping. Getting one row wrong
means mislabelling a whole county's insurance costs on a public page, so this needs
to be right rather than quick.

## Job 1 — All 58 California county FIPS codes

Give me **every one of California's 58 counties** with its 5-digit FIPS code.

**Output format — please follow it exactly**, because I am pasting this straight
into a script:

```
06001	Alameda
06003	Alpine
06005	Amador
```

That is: five-digit code, a single TAB, then the county name **without** the word
"County". One county per line, sorted by code ascending. No numbering, no bullets,
no markdown table, no commentary between lines.

Requirements:

- **All 58.** Not a sample, not the largest ones. If you output fewer than 58 rows
  you have made an error — count them before sending.
- California FIPS codes run from 06001 to 06115 and are **odd-numbered only**
  (06001, 06003, 06005 …). If you produce an even code after 06001, something has
  gone wrong.
- Use the **official spelling**, including accents and abbreviations exactly as the
  Census Bureau writes them (for example `San Luis Obispo`, `Del Norte`,
  `Contra Costa`).
- Tell me your **source** with a URL — ideally the Census Bureau's FIPS/ANSI county
  file, or `census.gov` geography documentation.
- After the list, state the **row count** you produced so I can check it at a
  glance.

## Job 2 — Group those counties into regions Californians actually recognise

A county table with 58 rows is hard to scan. I want to group them into regions a
reader recognises — "Bay Area", "Central Valley", "Southern California" and so on —
so someone can find themselves quickly.

The catch: these groupings are often invented casually and disagree with each other.
So please use an **official or well-established published definition** rather than
your own judgement.

Give me:

- The **grouping you used and its source**, with a URL. Something like the
  California Department of Finance's regional definitions, Cal OES mutual aid
  regions, the Governor's Office regional groupings, or a comparable official
  scheme. Name which one you chose.
- Then every county assigned to a region, in this format:

```
Alameda	Bay Area
Alpine	Sierra
```

County name, TAB, region name. Same spelling as Job 1 so the two tables join
cleanly.

- If your chosen source does not cover all 58 counties, say which ones it omits
  rather than filling the gaps yourself.
- If two credible official schemes disagree materially about a county, flag that
  county and tell me both answers. I would rather know a boundary is contested than
  have it silently picked for me.

## Ground rules

- **Accuracy over completeness of explanation.** I do not need the history of FIPS
  codes; I need 58 correct rows.
- If you are unsure about a specific county's code or region, **mark it** rather
  than guessing. One flagged row I can check is far better than one wrong row I
  cannot spot.
- Give the **URL for every source**. I will be verifying against the FEMA data
  itself, so a mismatch will surface immediately.
- Please do not add commentary inside the code blocks — keep them clean so they
  paste directly.
