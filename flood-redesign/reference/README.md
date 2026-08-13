# County reference tables

## `ca-county-fips.tsv` — 58 California counties, FIPS code to name

Source: US Census Bureau TIGERweb, California counties, data as of 1 Jan 2025.
Supplied by ChatGPT, 13 Aug 2026, then validated here.

**Validation performed** (all passed):
- 58 rows exactly
- every code 5 digits, `06` prefixed, odd-numbered
- the complete sequence 06001–06115 with no gaps, duplicates or extras
- strictly ascending
- **joined against live FEMA `countyCode` values** for California — 54 distinct
  codes appeared in a 2,999-row sample and every one mapped

### One thing FEMA returns that is NOT a county: `06000`

The live data contains `countyCode = 06000`, which is not a county at all — `000`
is the placeholder for state-level or unreported geography. It is absent from the
Census list because it should be, not because the list is short.

**Handle it explicitly.** Any county aggregation must drop `06000` or label it
"county not reported"; silently joining it away would quietly discard policies,
and mapping it to a county would invent one. This is the sort of value that
produces a plausible-looking table with a missing row nobody notices.

## `ca-county-regions.tsv` — county to region

Source: California Department of Health Care Services' nine Geographic Region
Categories (Access Monitoring Plan, Appendix E, Table 63). Covers all 58 counties.

Validated: 58 rows, joins to the FIPS table with no orphans on either side.

### Two overrides to consider before publishing

The DHCS scheme is built for **Medi-Cal access monitoring**. It is official and
complete, which is why it was chosen, but its purpose has nothing to do with how a
flood insurance buyer thinks about where they live. ChatGPT flagged the boundary
disputes against the Caltrans economic scheme rather than picking silently, which
was the right call. Two of them matter for us:

1. **Ventura → "Central Coast" (DHCS) or "Southern California" (Caltrans).**
   Caltrans is right for our audience. Nobody in Oxnard or Thousand Oaks describes
   themselves as Central Coast, and Ventura carries real policy volume.
2. **El Dorado and Placer → "Sierra Range/Foothills" (DHCS) or "Sacramento Valley"
   (Caltrans).** Folsom and Roseville read as Sacramento suburbs to anyone
   local, and Sacramento is where the flood exposure is.

Also worth knowing about the shape of the data: DHCS puts 13 counties in
Sierra Range/Foothills — the largest region — but those are Alpine, Sierra, Mono
and similar, which will hold almost no flood policies. Meanwhile **Sacramento
County alone is the single largest NFIP county in California** (593 of 2,999 in the
validation sample, ahead of Los Angeles at 314), which is the Sacramento–San
Joaquin Delta showing up in the numbers. A region grouping that buries Sacramento
in a valley bucket while giving thirteen empty mountain counties their own heading
is optimised for the wrong thing.
