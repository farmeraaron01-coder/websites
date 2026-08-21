# cheapsoberlivinginsurance.com — Divi → Kadence rebuild

Working files for the sober living site rebuild. Read in this order.

| File | What it is | Who acts |
|---|---|---|
| `RECON.md` | Live before-state captured 21 Aug 2026, and the six Part 0 decisions adjudicated against it | read first |
| `PACKAGE-REVIEW.md` | Review of the Dropbox Kadence package: the 10-page map, corrections to make before building, and two of my own recommendations reversed | read before building |
| `IDENTITY.md` | Licence, address, phone, and the live schema conflict confirming them exposed | read before schema |
| `STEP-1-STAGING.md` | Operator work order: lock staging out of the index, install Rank Math, reach URL parity, cut over | operator |

The migration procedure itself lives in `/MIGRATION-PLAYBOOK.md` at the repo
root. This folder holds only what is specific to this site.

## Approach

Build fresh on `staging.cheapsoberlivinginsurance.com` with **Rank Math from the
start** and **never install All in One SEO** on it. No import, no plugin
reconciliation on a live site, production untouched until cutover.

## 🔴 The one urgent item

**Staging is currently crawlable and indexable.** No `noindex`, no
`Disallow: /`, `wp-login.php` returns 200. Password-protect the directory before
any more build work — details in `STEP-1-STAGING.md`. A staging copy that gets
indexed can outlive the migration, with Google treating the real launch as the
duplicate.

## Nothing is blocked on a decision any more

All six Part 0 items are closed. Identity fields arrived 21 Aug and are in
`IDENTITY.md`.

## What was decided, and why it differs from the playbook

Three Part 0 items resolved differently once the live site was measured. All
three are argued in `RECON.md`:

- **`/quote/` → blocked on checking Google Ads final URLs.** Changing the slug
  could break paid landing pages, which costs money immediately.
- **`/sober-living-home-insurance/` → build it.** I first said not to; reading
  the package showed it is the pillar for four coverage spokes. Fix the
  homepage's title and H1 instead.
- **Image weight → a package problem, not a live-site one.** The live homepage
  is 1.1 MB across 22 images. The 1.89 MB `og.png` the playbook flags is in the
  new content package.

## The finding that reshapes the work

This site runs **All in One SEO**, not Rank Math. Every sitemap, schema, redirect
and meta-description procedure in `CLAUDE.md` and the playbook is Rank Math
shaped and does not transfer as written. Hence Step 1.
