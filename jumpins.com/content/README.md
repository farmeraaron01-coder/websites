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
| `gbp/GBP-POST-fair-plan.txt` | GBP post for the above, 1,494/1,500 chars | **POSTED** — live on the Jump Insurance GBP with the "Learn more" button |
| `gbp/fair-plan-gbp-photo.jpg` | Primary GBP image, 1200×900 | **Used** on the live post |
| `gbp/fair-plan-gbp-photo-alt.jpg` | Alternate GBP image, 1200×900 | Spare, unused |
| `blog/earthquake-insurance-california-2026.md` | Draft; a version is live | Live post needs the FAQ fix below |
| `blog/california-non-renewal-crisis-2026.md` | Draft | Palm Desert reference removed 20 Aug |
| `blog/wildfire-home-insurance-california-2026.md` | Draft | — |

## Time-sensitive

The FAIR Plan increase takes effect **15 October 2026**. Both the article and the GBP post are
live, so the launch work is done.

What remains is timing. The article's own argument is that starting in August beats an October
renewal comfortably while September is tight — which means the current post does its best work
*now* and progressively less as the deadline nears. GBP posts persist rather than expire, but
they lose surface prominence as they age, and this one is already several weeks old.

**Worth considering: a second, shorter GBP post in late September** — same link, reframed around
the closing window ("about three weeks left to test the market before your renewal reprices")
rather than the announcement. The alternate photo (`fair-plan-gbp-photo-alt.jpg`) is unused and
would keep it visually distinct from the first. Not required; just the highest-value follow-up
available on this topic.

## The FAQ markup rule for this site

`blog/fair-plan-rate-increase-october-2026.html` is the correct model and the reason its reference
copy is kept. It carries the FAQ **both ways** — visible `<h3>`/`<p>` pairs *and* JSON-LD mirroring
them word for word (verified 6 of 6).

Two already-published posts get this wrong, with their Q&As **only** in the JSON-LD.
**Verified against the live pages on 20 Aug 2026** (raw HTML, not a cached report):

| Live post | Schema Qs | Questions missing from visible copy | Answers missing |
|---|---|---|---|
| `earthquake-insurance-california-2026` | 4 | **3 of 4** | **4 of 4** |
| `san-diego-flood-insurance-flood-zones` | 5 | **5 of 5** | **5 of 5** |

The flood post is worse than previously recorded — the earlier note said 4 of 5 questions were
missing; the live page shows all 5 are, and neither post has a single answer paragraph rendered.
The one question that does appear on the earthquake post
("How much does earthquake insurance cost in California?") matches an existing H2 by coincidence
of wording, not because a FAQ section exists. Neither post has any `<h3>` at all.

That breaks Google's structured-data policy, which requires marked-up content to be visible to
users. More importantly, Google retired FAQ rich results on **7 May 2026**, so the value of FAQ
content now is being quotable by AI Overviews and ChatGPT — and those read rendered text. A
schema-only Q&A is invisible to the exact thing it is now for.

**Fix — written and ready to paste:**

| File | For post | Pairs |
|---|---|---|
| `../fixes/faq-visible-earthquake-post.html` | `/earthquake-insurance-california-2026/` | 4 |
| `../fixes/faq-visible-flood-zones-post.html` | `/san-diego-flood-insurance-flood-zones/` | 5 |

Each was generated directly from the JSON-LD live on that post, so the visible copy matches the
schema word for word. Paste each as a Divi Text module immediately before the post's closing CTA
section. **Do not touch the existing JSON-LD** — it is correct; only the visible copy was missing.
If either side is ever reworded, reword both, or the mismatch returns.

No longer blocked. `../fixes/schema-faq-earthquake-example.json` turned out to match the live
earthquake schema exactly, but that is now confirmed rather than assumed.

## Outstanding security item (from Dropbox READ-ME-FIRST, 7 Aug 2026)

Four WordPress application passwords issued during the August work still need revoking —
**`jumpins.com` / `Admin` first**, since jumpins is a live production site with no staging in front
of it. The other three cover the two flood sites. Two Dropbox `.env` files holding live secrets also
need rotating. Not actioned here; flagged because it is the top item on that list and still open as
of 20 Aug.
