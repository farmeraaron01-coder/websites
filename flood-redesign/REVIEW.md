# Design Review: ChatGPT Prototype vs. Claude Concept — and the Merge

Reviewed against the handoff in Dropbox (`Claude CoWork Files/California Flood Insurance - Kadence
Redesign Review/`): `DECISIONS.md`, the audit, and the full `prototype-source` (rendered and
screenshotted locally). `concept-homepage.html` in this folder is the **merged v2** that takes the
best of both.

## Where the ChatGPT prototype is stronger (adopted in v2)

1. **Compliance-correct copy.** "Start My Quote," "about 2 minutes, a specialist follows up,"
   "up to 9 private flood markets + NFIP," 40,000+/900+/4.9 proof set, and "we tell you honestly
   when the NFIP is the better fit." This follows DECISIONS.md exactly. **v2 adopts all of it.**
2. **The raindrop hero.** Owner decision: keep the video as the CFI signature. Their gradient
   overlay treatment protects contrast. **v2 adopts it** (poster embedded; 720p video desktop-only,
   static poster on mobile/reduced-motion).
3. **Interior templates.** The flood-zone template (zone badge, BFE diagram, key takeaways,
   related guides) and article template (reviewed-by byline, short-answer box, TOC, sources)
   are excellent and should be built as-is, restyled with the shared tokens.
4. **Statewide cross-link in the footer** — clean brand separation. **Adopted.**

## Where the ChatGPT prototype is weaker (fixed in v2)

1. **The private-vs-NFIP table carries no information** — every row is ✓ for both columns.
   v2 shows the actual differences (building-limit cap, waiting periods, loss of use,
   replacement-cost options) with qualified language.
2. **One anonymous review** ("JM, California homeowner") against a 900+-review asset. v2 shows
   three, with a note that production pulls the verified Google profile.
3. **No license number anywhere on the homepage**, and the homepage footer loses the nav columns
   its own interior pages have. v2 carries CA Lic. #0L75450 in the utility bar, hero chips,
   expert section, and footer legal line.
4. **No homepage path into the SEO library** — no zone chips, no guides row, no city links.
   For a site whose growth engine is zone/city/guide content, that is the biggest internal-linking
   miss. v2 has the zone-finder teaser + guide cards with bylines and review dates.
5. **Aaron is a monogram, not a person.** They shipped `aaron-farmer.png` but render "AF" on the
   homepage. YMYL trust wants the face and credentials.
6. **Georgia/Arial system type.** Zero-byte payload is smart, but Arial body reads dated —
   exactly what the migration is meant to escape. v2 uses Bricolage Grotesque + Public Sans
   (~100 KB self-hosted via Kadence) as a distinctive but trustworthy voice. This is the one
   deliberate style disagreement; both options are performance-safe.

## What v2 keeps from the original Claude concept

- Harbor-navy/Pacific-blue token system with **sunset-gold reserved for quote CTAs only**.
- The **base-flood-elevation waterline** motif (hero, zone badge, CTA band).
- The **hero quote card** — now reworded to DECISIONS.md language (secure form, ~2 min,
  specialist follow-up, no automated rates).
- The **CFI ↔ Statewide live brand toggle** demonstrating one design system, two sister brands
  (teal accent, swapped phone/copy/areas), honoring the "related but not duplicated" decision.
- Full footer with license, qualified-coverage disclaimer, and Statewide cross-link.
- Performance budget: text LCP, no carousels, two subset font files, poster-first video.

## Open items for Aaron

- The audit recommends national positioning for CFI, while DECISIONS.md keeps CFI
  California-only with Statewide owning national content. v2 follows DECISIONS.md; revisit only
  if the state-page strategy moves under one domain.
- Verify the 40,000+ / 900+ / 4.9 numbers and the exact private-market count before launch, and
  the agency/coverholder wording with counsel (audit §Trust and compliance risks).
- Final raindrop asset: compress to WebM+MP4 720p with an optimized poster and reserved height.

## v3 revisions (owner feedback, July 22)

1. **Gold dropped.** CTA color is now the brand cyan (`#25C1EE`, navy text for contrast),
   reserved exclusively for quote actions; supporting blues stay deeper so the CTA remains the
   brightest element. Review stars keep Google's amber by convention only.
2. **Real raindrop video embedded.** The hero now plays the actual `raindrops-hero.mp4`
   (720p H.264) with a real extracted frame as poster; video hides on mobile and under
   reduced-motion per DECISIONS.md. The earlier ChatGPT-generated rain photo is gone.
3. **Quote card is a pure click-through.** No embedded fields — benefits list + "Start My Quote"
   linking to the existing Cognito quote page, mirroring the current short-form flow. Copy leaves
   room to add online pricing later without a redesign.

## Build architecture note (cheaplandlordinsurance.com)

The owner wants "the same Kadence theme as cheaplandlord.com." The cheaplandlord build
(Dropbox: `Claude CoWork Files/cheaplandlordinsurance.com-build/`) is actually a
**dependency-free custom WordPress theme** (v1.1.1: front-page.php video hero, theme.json
palette, customizer contact settings) plus a **`cli-instant-quote` plugin** (Steadily rater
proxy with email lead-capture fallback when no API key is configured) — not Kadence.

**Decision (July 22): Kadence.** The owner is using Kadence on another current rebuild and
values it for the light, fast build. The flood sites will be built on Kadence + Kadence Blocks,
following the mapping table in the concept's appendix. Speed disciplines that made the
cheaplandlord build fast carry over regardless of theme:

- Local-hosted fonts (two subset woff2 files), no Google Fonts CDN calls
- Native `<video>` hero with poster + reserved height; no sliders/carousels
- Kadence settings: CSS loaded per-page, disable unused block CSS, minimal header scripts
- AVIF/WebP images with explicit dimensions; lazy-load everything below the hero
- Few plugins — the theme is rarely what makes a WordPress site slow; plugins and media are
- The `cli-instant-quote` plugin pattern (estimate now / agent follows up) remains available
  later as a standalone plugin — it is theme-agnostic and would work under Kadence unchanged.

## v4 revisions (owner feedback, July 22 — round 2)

1. **1-2-3 cards replaced.** "How it works" is now a single dark-navy timeline panel
   ("What happens after you click Start My Quote") with time markers — First 2 minutes /
   Same business day / When you say go — giving the section real contrast against the
   coverage cards below, which now sit on the tinted mist ground.
2. **Zone lookup tool cut.** Visitors arrive already knowing their zone; the section now
   sends them to the zone guides (internal links, nobody leaves the site) next to a
   plain-English "What actually decides your premium" card that ends on the reason to call:
   the same house prices differently carrier to carrier.
3. **BFE waterline motif removed everywhere.** No jargon graphics; the raindrop video is
   the signature element and the only thing that moves.
4. **Hero quote card slimmed and shifted** (narrower, lower, lighter gradient on the video
   side) so the raindrops are actually visible.

## Kadence child theme (kadence-child/)

`cfi-kadence-child/` implements the v4 homepage as a coded `front-page.php` under the
Kadence theme (owner decision: PHP templates, no page builder). Self-hosted fonts, the
raindrop video with poster fallback, guides pulled from real posts via WP_Query, and all
brand facts as constants in functions.php. Install steps and the edit checklist are in the
theme's readme.txt; `cfi-kadence-child-v1.0.0.zip` is ready to upload to WordPress.
