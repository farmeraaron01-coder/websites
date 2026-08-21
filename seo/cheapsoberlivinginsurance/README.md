# cheapsoberlivinginsurance.com — Divi → Kadence rebuild

Working files for the sober living site rebuild. Read in this order.

| File | What it is | Who acts |
|---|---|---|
| `RECON.md` | Live before-state captured 21 Aug 2026, and the six Part 0 decisions adjudicated against it | read first |
| `STEP-1-RANKMATH.md` | Operator work order: All in One SEO → Rank Math, as its own change before the theme rebuild | operator, ~1 hour |

The migration procedure itself lives in `/MIGRATION-PLAYBOOK.md` at the repo
root. This folder holds only what is specific to this site.

## What still needs a human decision

**Agency identity fields.** Licence number, physical address and phone. The
content package leaves them blank; they feed `InsuranceAgency` schema and cannot
be inferred. Nothing is blocked on them until schema goes in.

## What was decided, and why it differs from the playbook

Three Part 0 items resolved differently once the live site was measured. All
three are argued in `RECON.md`:

- **`/quote/` → keep `/quote-now/`.** The playbook said reverse the redirect.
  Recon says don't: reversing risks a redirect loop on the only conversion page,
  and the slug is not a ranking factor.
- **`/sober-living-home-insurance/` → do not build it.** The homepage already
  owns the topic. Two URLs, one query, on a five-page site is cannibalization.
- **Image weight → a package problem, not a live-site one.** The live homepage
  is 1.1 MB across 22 images. The 1.89 MB `og.png` the playbook flags is in the
  new content package.

## The finding that reshapes the work

This site runs **All in One SEO**, not Rank Math. Every sitemap, schema, redirect
and meta-description procedure in `CLAUDE.md` and the playbook is Rank Math
shaped and does not transfer as written. Hence Step 1.
