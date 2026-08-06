# California cutover — pre-flip checks, 6 Aug 2026

Run immediately before the California flip. Four things were checked; two were real defects
now fixed, one was a false alarm from my own tool, and one is a decision for Aaron.

---

## FIXED — two redirect rules would have destroyed the video posts

Covered in full in the header of `california-prune-redirects.conf`. Short version: ten of the 48
rules pointed at URLs that return 404 on production in every form, so they were never production
URLs — they were slugs that lived briefly on the new site during the redesign and got swept into
the prune list.

`.htaccess` runs before WordPress. Two of those dead rules were
`/flood-insurance-carrier-ratings/` and `/private-flood-insurance-vs-fema/` — two of the four
video posts built this morning. Left in, both pages would have been 301'd away at cutover,
unreachable, taking the one video Google has indexed with them.

All ten removed. **38 rules now: 20 301s, 18 410s.** Verified every source is live on production
and zero sources resolve to a real page on the new site.

**Re-run the collision check before installing the file** — it is in the file header. Anything
added to the new site after 6 Aug could hit the same trap.

## FIXED — /media/ was an unbuilt Divi demo template

Six "Your Title Goes Here" headings, six copies of Elegant Themes' demo podcast audio. The
migration copied it faithfully from production, where the same template has been emitting
VideoObject schema for `FkQuawiGWUw` — Elegant Themes' own Divi advert. Production has been
telling Google it hosts a Divi commercial.

New page trashed (reversible), and `/media/` now 301s to `/video/`. The orphaned `.m4a` is still
in the media library as id 336, unreferenced; delete it when convenient.

## FALSE ALARM — /get-a-quote/ is fine, and the tool was wrong

`preflight.py` reported the quote page 43% thinner. It is not, and this mattered because that page
carries the ad spend.

The cause was in my own tool. `visible_words()` counted the entire document, so it was comparing
navigation and footers rather than content — Divi ships a long nav and a four-column footer, the
Kadence child ships less. Fixed by stripping `nav`/`header`/`footer`/`aside` from **both** sides.
Extracting `<main>` instead would have been worse: production emits no `<main>` at all, so the new
site would have been measured on content while production was measured on content plus all its
chrome.

After the fix, `/get-a-quote/` reads **33 words live vs 48 new** — the new page has more.

Then verified by actually rendering both in Chromium at a mobile viewport:

| | Production | New |
|---|---|---|
| Cognito key / form | `8nmcIcFF1k6xZNCBaOzZxQ` / form 5 | **identical** |
| form fields rendered | 48 | **48** |
| JS errors | none | none |
| `<details>` foundation helper | 0 (Divi JS popup) | 1 |
| `tel:` links | 1 | 2 |
| `<noscript>` phone fallback | no | yes |
| `dataLayer` afterSubmit hook | no | yes |

Same form, same field count, plus a noscript fallback and a conversion hook production lacks.

## NOT a pre-flip blocker — emptying the Trash

I told Aaron twice that the pruned posts had to be deleted out of the Trash before the redirects
would take effect. **That is wrong**, and it is worth writing down because it sounds plausible.

**WordPress frees the slug the moment a post is trashed**, by appending `__trashed` to it. Verified
on the new site: 46 of 46 trashed posts carry the suffix, and all 38 redirect sources return 404
there. Separately, the redirects are Apache `Redirect` directives — they fire before WordPress is
involved at all, so the trash state cannot affect them either way.

So emptying the Trash is **optional hygiene, not a launch step.** There is one real reason to do it:
if anyone later restores a trashed post it reclaims its original slug, and the `.htaccess` redirect
would then shadow it — a page that exists but redirects, which is miserable to debug six months on.
Emptying removes that trap.

It is safe. 45 of the 46 trashed posts are backed up in `pruned-content-backup-pass1.json` and
`pass2.json`; the 46th is `hello-world`, WordPress's sample post. The 25 trashed **pages** are
mostly `-2` duplicates from a re-migration (`video-2`, `claims-2`, `staff-form-2`).

To do it: **Posts → Trash → Empty Trash**, then **Pages → Trash → Empty Trash**. Permanent.

## FIXED — breadcrumbs said "Uncategorized" on 13 of 19 posts

Spotted from Aaron's Posts screen on 6 Aug. It was not only the trashed posts: 13 of the 19
**published** posts sat in Uncategorized, and it surfaced in the rendered HTML and in the
BreadcrumbList schema, so Google would read `Home › Uncategorized › El Niño and California Flood
Risk`.

Renamed the default category to **Flood Insurance Guides** (slug `flood-insurance-guides` — not
`guides`, which the real hub page already holds). One change, all 13 breadcrumbs fixed, no new URLs,
and future uncategorised posts now land somewhere sensible. Verified: `Uncategorized` no longer
appears in the HTML.

Assigning the 13 to the site's real topic categories would be better, but that is content
architecture rather than a launch step.

### Check this at step 4, when the noindex comes off

Whether `/category/…/` archives are indexable after launch **cannot be read on staging** — every
page type there returns `nofollow, noindex` from the site-wide "Discourage search engines" setting,
which masks whatever Rank Math would do on its own. Thin category archives on a 19-post site are a
liability worth ruling out, so check Rank Math → Titles & Meta → Categories once the site-wide
noindex is lifted.

## FOR AARON TO DECIDE — the new Terms of Service drops mandatory arbitration

Not a migration defect. The new Terms is a **rewrite**, not a truncation: 47 headings against
production's 32, and far more specific to the actual business — quotes and underwriting, surplus
lines, waiting periods, flood maps and models, AI/chat, E-SIGN.

**A correction to my own first pass:** I ran a keyword check that reported seven clauses missing.
Six of those were my check failing, not real gaps. Section 27 carries severability, no-waiver,
assignment, force majeure and entire-agreement in plain English rather than by those names, and
section 17 has the full DMCA notice-and-takedown elements without using the letters "DMCA".
Children's privacy is in the new Privacy Policy at section 14, which the Terms incorporate by
reference.

**One real difference remains.** Production section 16 compels binding arbitration after a 30-day
informal period, with a class-action waiver. The new section 24 says the opposite, explicitly:

> "These Terms do not create a mandatory arbitration agreement."

That is a deliberate choice by whoever drafted it, not an omission — but it reverses the legal
posture of the live site, and the new page replaces the old one at cutover. Dropping compelled
arbitration and a class-action waiver on a consumer-facing insurance site is a change in exposure.

**This is a lawyer's call, not mine, and it does not block the flip** — nothing about it affects
traffic, rankings or function. But Aaron should know it is changing, and decide deliberately rather
than by default.

## POST-LAUNCH, not now — three small schema additions

Preflight flagged `schema-loss` on ~50 pages. Most of it is noise worth losing:

- **`AboutPage` on the homepage** — wrong type for a homepage, and its `description` is empty.
  Rank Math mis-assigning. Do not restore.
- **`Article` on `/get-a-quote/`** — a quote form is not an Article; `author.name` is empty. Its
  absence is an improvement.
- **The second `InsuranceAgency` node** my checker reported is not a duplicate entity — it is the
  nested `worksFor` inside the author Person node, flattened by my walker.

Three are genuine, all small, and none justifies installing a theme version an hour before a
cutover:

1. **`PropertyValue` — the license number.** Production emits
   `{"name":"California Insurance License","value":"0L75450"}`. Publishing a licence as structured
   data on a regulated insurance agency is a real trust signal, and `CFI_LICENSE` is already a
   theme constant. Best of the three.
2. **`ContactPoint`** — `contactType: customer support` with the phone. Production's has a leading
   space in the telephone value; do not reproduce that.
3. **`worksFor` should reference `#organization` by `@id`** rather than restating name and url, so
   consumers merge it into the existing Organization instead of seeing a parallel one.

Ship as 1.5.1 in the first post-launch week.

### One difference that is deliberate, not a regression

`areaServed` is `Country: United States` on the new site and `State: California` on production.
That is intentional and documented at `functions.php:117` — the DBA registered with the California
DOI writes nationwide, so both sister sites claim the same area. Narrowing California's site to the
state would understate the business. Left as-is; noted here so it is not "fixed" later by someone
reading the production value as correct.
