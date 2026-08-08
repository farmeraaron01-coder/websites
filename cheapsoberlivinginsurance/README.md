# cheapsoberlivinginsurance.com — build corrections

The build package itself lives in Dropbox at
`Claude CoWork Files/cheapsoberlivinginsurance.com-build/cheapsoberlivinginsurance-kadence-package.zip`
(Codex, 7 Aug 2026). It is approved on layout, block structure, copy voice and build discipline.

This folder holds the corrections to it.

| File | What it is |
|---|---|
| `KADENCE-BUILD-GUIDE-REVISIONS.md` | Replaces §3 palette, §4 typography, §5 buttons, §10 SEO. Adds the cost page and the missing pages. Applies on top of Codex's guide. |
| `kadence-site.css` | Drop-in replacement for the package's `css/kadence-site.css`, with the accessible tokens. |

## Why the palette changed

Three tokens failed WCAG AA on text that appears on every page. Measured, not estimated:

| Original | Ratio | Needed | Where |
|---|---:|---:|---|
| `#C56643` on `#FBFAF7` | 3.76 | 4.5 | eyebrow 12px/850 — every page |
| `#C56643` on `#F4F0E8` | 3.45 | 4.5 | same, alternating sections |
| white on `#C56643` | 3.92 | 4.5 | primary button label |
| `#9AA6AC` on `#FBFAF7` | 2.39 | 4.5 | "muted interface text" |

The fix promotes Codex's own hover colour `#A84E31` to the base (5.30 / 4.86 / 5.53 — all pass), darkens
the hover to `#8E4026`, keeps `#C56643` for large display numerals only where 3.0 applies, and replaces
`#9AA6AC` with `#66757E` for text while allowing the original as a border colour.

All 11 corrected pairs verified passing at their intended sizes.

## The substantive gap

The package has **no cost content on any page** — no page, no section, no sentence. For an exact-match
"cheap" domain that is the omission that matters most, because a visitor arriving on a price query finds
nothing about price.

The house pattern already exists at `cheaplandlordinsurance.com`, whose SEO plan names it directly:
*"Price intent | cheap landlord insurance, landlord insurance cost, how much is landlord insurance |
Exact-match domain + real cost tables"*, served by a dedicated cost cluster page. §D of the revisions
mirrors it: a `/sober-living-insurance-cost/` page whose job is to acknowledge price honestly and then
reframe on coverage — competitive on premium, unwilling to win by quietly removing coverage.

**The cost ranges themselves are the one thing in that document that cannot be written without real data.**
They are marked for Aaron or underwriting to supply. Publishing invented premium figures on an insurance
site is both a compliance problem and a credibility problem the first time a quote lands nowhere near them.
