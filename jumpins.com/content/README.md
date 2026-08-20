# jumpins.com content

Article and Google Business Profile source for Jump Insurance Services.

> **Scope: San Diego only.** Per Aaron's instruction of 6 Aug 2026, content for this site targets
> San Diego County and does not promote the Palm Desert office — no Coachella Valley geography, no
> `/palm-desert-office/` links. Statewide and county-wide framing is fine.

> **Git is authoritative.** Dropbox copies under `Claude CoWork Files/Content Deliverables/` are
> reference only. If they disagree with git, git wins.

## Status

| File | What it is | Status |
|---|---|---|
| `blog/fair-plan-rate-increase-october-2026.html` | FAIR Plan 29.1% increase, effective 15 Oct 2026 | **PUBLISHED 6 Aug 2026** (post 4553) — do not publish again |
| `gbp/GBP-POST-fair-plan.txt` | GBP post for the above, 1,494/1,500 chars | **Ready to post — not yet posted** |
| `gbp/fair-plan-gbp-photo.jpg` | Primary GBP image, 1200×900 | Ready to upload |
| `gbp/fair-plan-gbp-photo-alt.jpg` | Alternate GBP image, 1200×900 | Spare |
| `blog/earthquake-insurance-california-2026.md` | Draft; a version is live | Live post needs the FAQ fix below |
| `blog/california-non-renewal-crisis-2026.md` | Draft | Palm Desert reference removed 20 Aug |
| `blog/wildfire-home-insurance-california-2026.md` | Draft | — |

## Time-sensitive

The FAIR Plan increase takes effect **15 October 2026**. The article's own argument is that
starting in August beats an October renewal comfortably and starting in September is tight — so
the GBP post is the live item here. Its instructions said to post within a week of the article
(published 6 Aug); that window has passed but the October deadline has not.

## The FAQ markup rule for this site

`blog/fair-plan-rate-increase-october-2026.html` is the correct model and the reason its reference
copy is kept. It carries the FAQ **both ways** — visible `<h3>`/`<p>` pairs *and* JSON-LD mirroring
them word for word (verified 6 of 6).

Two already-published posts get this wrong, with their Q&As **only** in the JSON-LD:

| Live post | Schema Qs | Missing from visible copy |
|---|---|---|
| `earthquake-insurance-california-2026` | 4 | 3 |
| `san-diego-flood-insurance-flood-zones` | 5 | 4 |

That breaks Google's structured-data policy, which requires marked-up content to be visible to
users. More importantly, Google retired FAQ rich results on **7 May 2026**, so the value of FAQ
content now is being quotable by AI Overviews and ChatGPT — and those read rendered text. A
schema-only Q&A is invisible to the exact thing it is now for.

**Fix:** add a visible FAQ section to each post with the questions as `<h3>` and the answers as
`<p>`, worded identically to the existing JSON-LD. Do not change the JSON-LD; make the visible copy
match it.

**Blocked on:** the live JSON-LD for `earthquake-insurance-california-2026`. The flood post's schema
is recovered from branch `claude/jumpins-seo-geo-content-d70bek` (5 Q&As, in the post's own markdown
file). For the earthquake post, `../fixes/schema-faq-earthquake-example.json` has 4 Q&As and the
counts match, but it has not been confirmed against what is actually deployed — mirroring the wrong
wording would leave the mismatch in place. Needs either the live `<script type="application/ld+json">`
block pasted from view-source, or network access to jumpins.com.

## Outstanding security item (from Dropbox READ-ME-FIRST, 7 Aug 2026)

Four WordPress application passwords issued during the August work still need revoking —
**`jumpins.com` / `Admin` first**, since jumpins is a live production site with no staging in front
of it. The other three cover the two flood sites. Two Dropbox `.env` files holding live secrets also
need rotating. Not actioned here; flagged because it is the top item on that list and still open as
of 20 Aug.
