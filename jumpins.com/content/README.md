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

### RESOLVED 20 Aug 2026

Two published posts had their Q&As **only** in the JSON-LD. Both are now fixed and verified
against the live pages (raw HTML fetched and parsed, not a self-report):

| Live post | FAQPage blocks | Schema Qs | Visible `h3` | Questions visible | Answers visible | Order matches |
|---|---|---|---|---|---|---|
| `earthquake-insurance-california-2026` | 1 | 4 | 4 | 4/4 | 4/4 | yes |
| `san-diego-flood-insurance-flood-zones` | 1 | 5 | 5 | 5/5 | 5/5 | yes |

Before the fix: earthquake had 3 of 4 questions and 4 of 4 answers missing; flood-zones had all
5 of each missing. Neither rendered any `<h3>`. The single earthquake question that did appear
matched an existing H2 by coincidence of wording, not because a FAQ section existed.

Exactly one FAQPage block per post — the pre-existing JSON-LD was left untouched, so there is no
duplicate schema.

**Known cosmetic difference, deliberately not "fixed":** `wptexturize` converts straight
apostrophes to curly ones in visible copy, so two strings differ from the schema by one character
(`CEA’s` vs `CEA's` on earthquake Q3, `don’t` vs `don't` on flood Q3). Leave them. Google's
requirement is that marked-up content be **present and visible** to users, not byte-identical, and
typographic variants normalise. Editing live JSON-LD to chase character parity carries real risk
(a stray character invalidates the block) for no benefit, and wptexturize would reintroduce the
difference on the next content edit anyway. For AI-citation purposes the engines read rendered
text, where the apostrophe form is irrelevant.

That breaks Google's structured-data policy, which requires marked-up content to be visible to
users. More importantly, Google retired FAQ rich results on **7 May 2026**, so the value of FAQ
content now is being quotable by AI Overviews and ChatGPT — and those read rendered text. A
schema-only Q&A is invisible to the exact thing it is now for.

**Applied.** The source blocks are kept for reference:

| File | For post | Pairs | Status |
|---|---|---|---|
| `../fixes/faq-visible-earthquake-post.html` | `/earthquake-insurance-california-2026/` | 4 | **applied 20 Aug** |
| `../fixes/faq-visible-flood-zones-post.html` | `/san-diego-flood-insurance-flood-zones/` | 5 | **applied 20 Aug** |

Each was generated directly from the JSON-LD live on that post, so visible copy and schema match
word for word. Standing rule: **if either side is ever reworded, reword both**, or the mismatch
returns.

`../fixes/schema-faq-earthquake-example.json` matches the deployed earthquake schema exactly —
confirmed against the live page, not assumed.

### Editor note — these posts are NOT Divi Builder

Established while applying the fix: both posts are **classic-editor HTML**, with Divi theming only
the page shell. Raw `<h2>`/`<h3>` markup renders correctly as-is; no Divi Text or Code module is
involved. Guidance elsewhere in this repo that says to paste markup "via a Divi Code module"
applies to **Divi-built pages** (the homepage and service pages), not to posts. Check which kind of
editor a given URL uses before assuming.

## Outstanding security item (from Dropbox READ-ME-FIRST, 7 Aug 2026)

Four WordPress application passwords issued during the August work still need revoking —
**`jumpins.com` / `Admin` first**, since jumpins is a live production site with no staging in front
of it. The other three cover the two flood sites. Two Dropbox `.env` files holding live secrets also
need rotating. Not actioned here; flagged because it is the top item on that list and still open as
of 20 Aug.
