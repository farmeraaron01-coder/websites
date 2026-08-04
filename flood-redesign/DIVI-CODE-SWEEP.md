# What the Divi code-module sweep found — 4 August 2026

The FAQ schema loss was not a one-off. This is the systematic check: **every `et_pb_code` module on both
production sites, enumerated and classified.** 100 modules — 45 on California, 55 on statewide.

The failure mode is always the same. A Divi code module has no Kadence equivalent, so anything
hand-placed in one carried its *visible prose* across the migration and left its *code* behind.

| Category | Modules | Status |
|---|---:|---|
| FAQPage schema | 66 | **Fixed** in 1.4.2 / 1.4.3 |
| Cognito form embeds | 13 | Mostly fine; two gaps below |
| Iframes (maps, legacy embeds) | 8 | One real loss, three already dead |
| Inline SVG / Trustindex / misc HTML | 9 | Fine |
| Person / Article JSON-LD | 2 | **One fixed** in 1.4.3, one needs nothing |
| Loose JS | 1 | Lost — the foundation-type helper |

---

## Fixed in the theme

### 1. FAQPage schema — now broader than Divi ever had it

1.4.2 covered 77 pages. The sweep then found a **third** Q&A markup shape —
`<p><strong>Question?</strong></p>` followed by a separate `<p>Answer</p>`, no `<br>` — used by eight
California city and flood-zone pages. Those were exactly the set that had FAQPage on production and
lost it. 1.4.3 reads all three shapes.

**85 pages, 342 question-and-answer pairs**, verified against raw content on both sites.

### 2. Author authority schema — restored, and better placed than the original

Statewide's Divi bio page carried a hand-written `Person` node: jobTitle, eight `knowsAbout` topics,
`memberOf`, three social profiles, and a description citing the Lloyd's coverholder status since 2016 and
40,000+ homeowners helped. Rank Math emits a `Person` too, but a thin one — display name, a **Gravatar
default placeholder image**, and the site itself as its only `sameAs`.

So the migration traded a rich author entity for a bare one. For E-E-A-T and the AI answer engines,
author authority is close to the whole point.

**The Divi version had a flaw worth not reproducing.** Its `@id` was `/aaron-farmer/#person`, which
nothing else referenced — every Article's author pointed at the author archive instead. All that
authority sat in an orphaned node attached to a single page. 1.4.3 emits the same properties under the
**author-archive `@id` Rank Math already uses**, so they merge into the entity the articles actually
cite. Better than either version alone, and **California gets it for the first time** — it never had any.

### 3. Cognito form 57 declared

`/contact-us/` uses form 57 on both brands, which was not in the theme's role map. It would have fallen
through to `role=other`. Now declared as `role=contact`, `is_lead=false`.

**One decision for you:** Google Ads has a historical `Contact_Form_Submission` action on both brands. I
set contact enquiries **not** to count as leads, because that is the reversible direction. If they should
count, it is a one-word change — but make it deliberately.

### 4. Article schema needs nothing

`flood-insurance-cost-by-state` had a hand-written `Article` node. Rank Math's replacement is **better** —
it carries `datePublished` and a working author reference, both of which the Divi version lacked. The Divi
one also pointed its author at `/about/aaron-farmer/`, a path that does not exist. No action.

---

## Not fixed — these need you

### A. Eight hot-linked assets that break the moment the docroot swaps

**This is the most consequential finding and it is unrelated to schema.**

Nine pages across the two sites reference uploads by **absolute production URL** rather than relative
path. Tested every one: all eight distinct files return **200 on production and 404 in the new install.**
After the swap those URLs resolve to the new docroot, where the files are not present.

| File | Referenced by |
|---|---|
| `2026/06/Aaron-Headshot-Edit-4.png` | **both** `/aaron-farmer/` pages — California hot-links statewide's copy |
| `2022/02/insurance-21.png`, `insurance-31.png` | statewide `/condo-owners-flood-renters-flood-insurance/`, `/homeowners-association-flood-insurance/` |
| `2022/04/flood-4.jpg`, `flood-ins3.jpg` | statewide `/facts-about-floods/`, `/resources/` |
| `2025/09/MapChart_Map_Updated09-30-25-scaled.png` | statewide `/contact-us/` |
| `2022/02/Residential_Home_Flood_001.jpg` | California `/california-flood-glossary/` |
| `2022/04/Podcast-Landing-Elegant-Themes.m4a` | California `/media/` — a **podcast audio file**, not an image |

**Fix, in this order:** copy the eight files into the new installs' `wp-content/uploads/` preserving
their year/month paths, then rewrite the references to relative paths so this cannot recur. Copying alone
fixes the breakage; rewriting stops the next migration inheriting it.

Once the headshot exists, define `CFI_AUTHOR_IMAGE` in `functions.php` per brand and the author schema
picks up a real image instead of omitting one.

**Add to the flip checklist:** after cutover, load `/aaron-farmer/` on both sites and confirm the
headshot renders. It is the single quickest proof this class of problem is closed.

### B. `/faqs/` lost its content — 60 KB down to 526 bytes

Production's FAQ page is a substantial accordion: **~60 KB on California, ~63 KB on statewide**, with
FAQPage schema, its own CSS and JS. The staging version is a **526-byte stub** — the heading, an intro
paragraph, and the "Reviewed by Aaron Farmer, CA License #0L75450" line. **Every question is gone.**

This is genuine content loss, not a parser gap, which is why the FAQ work above does not touch it. It is
also the one page whose entire purpose is questions — and per the production intro, they were pulled from
real call recordings, so they are not reproducible from a template.

Recover the content from production before launch. Once the Q&A is back on the page in any of the three
shapes the theme reads, its schema returns automatically.

### C. `/contact-us/` has no form and no map

Both production contact pages carry a Cognito form (57) and a Google Maps embed of the San Diego office.
Staging has **neither** — and still ends with the words "Our Location:" where the map used to be.

The page does keep every phone number, email and address, so it is not broken, just diminished. Add
`[cfi_cognito form="57"]` and the map embed back.

### D. `/get-a-quote/` lost the foundation-type helper

Production's quote page includes *"Not sure about your foundation type? Click here to see Foundation Type
examples"*, opening a reference image in a popup. It is gone from both staging quote pages.

**This is on the highest-value page on either site**, helping people past a question that plausibly stalls
applications. Worth restoring on conversion grounds alone.

Two notes if it is rebuilt: statewide's original markup is malformed — `<pee>` tags instead of `<p>`, and
a doubled `</a>` — so copy California's version, not statewide's. And the popup image is one of the
hot-linked assets in section A, so it needs copying too.

### E. `/floodguru/` does not exist on staging

Statewide production has a `/floodguru/` page running **Cognito form 68** — a form the theme does not
know about. The page was not migrated.

Not necessarily a problem: it may be deliberately retired. But it is a live URL today, so if it is not
coming across it wants a redirect rather than a 404. **Your call whether it returns.**

---

## Checked and fine

- **Trustindex reviews widget** renders on both home pages.
- **Inline SVG** on the home pages is present.
- **Claims, service-centre, agent-appointment and staff forms** all resolve through the theme's shortcode
  with the right roles.
- **The three iframes on `/calflood-newstalk-kbkw-discussing-flood-insurance/`** point at
  `/commercial/blog-post*.html`. Those files return **404 on California production and 301 on
  statewide** — they were already dead. Dropping them removed three broken embeds rather than losing
  anything. No action.

## What this exercise says about the migration

The FAQ schema was found because Aaron remembered it. Nothing else on this list would have been noticed
before launch, and most of it would have surfaced as slow, causeless decay — rankings drifting, a
headshot quietly missing, a helper nobody remembers.

**The general lesson: content migrated, code did not.** Any future Divi-to-block migration should
enumerate `et_pb_code` modules *first* and treat each as an explicit port-or-drop decision, rather than
assuming a content migration carried everything.
