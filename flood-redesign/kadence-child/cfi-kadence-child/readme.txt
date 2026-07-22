=== California Flood Insurance — Kadence Child Theme ===
Version: 1.0.0

Kadence child theme implementing the approved homepage design as a coded PHP
template (owner decision: no page builder for designed pages). Regular posts
and pages use the normal WordPress editor, unchanged.

== Install ==
1. Install and activate the free Kadence theme (Appearance > Themes > Add New > search "Kadence").
2. Zip the cfi-kadence-child folder and upload it via Appearance > Themes > Add New > Upload Theme. Activate.
3. Set a static front page: Settings > Reading > "A static page" > pick any page titled Home
   (the template ignores the page content; front-page.php renders the homepage).
4. Header: use the Kadence Header Builder (Appearance > Customize > Header):
   - Top row: HTML element left = "CA Lic. #0L75450 · Independent flood-only agency since 2012",
     right = hours + phone. Background #0A2540, text #9FBDD4, links #38C6F4.
   - Main row: logo left, primary menu center-right, button "Start My Quote" -> /get-a-quote/
     (button background #25C1EE, text #0A2540). Enable sticky header.
5. Footer: Kadence Footer Builder, background #0A2540. Include the license line, the
   qualified-coverage disclaimer, and the Statewide cross-link (see REVIEW.md).
6. Typography (Appearance > Customize > Typography): the child theme self-hosts
   Bricolage Grotesque + Public Sans and applies them on the front page. For sitewide use,
   select the same families in Kadence and enable "Load Google Fonts Locally", or leave
   Kadence's defaults for interior pages.
7. Performance (Appearance > Customize > General > Performance): enable CSS per-page
   loading and disable emoji/dashicons where offered.

== Edit checklist ==
- Phone, quote URL, license: constants at the top of functions.php.
- Zone chip URLs: $zones array in front-page.php — set to the real guide slugs.
- Reviews: replace the three placeholders with current verified Google reviews (or a
  reviews plugin capped at three).
- Statewide variant: copy this theme, change the five constants in functions.php and
  the :root palette block in assets/css/tokens.css (teal values are commented inline).

== Assets ==
- assets/media/raindrops-hero.mp4 — owner's raindrop loop (720p H.264). Consider adding a
  WebM encode alongside for smaller delivery.
- assets/media/hero-poster.jpg — real frame from the video; shown on mobile/reduced-motion.
- assets/fonts/*.woff2 — latin subsets, self-hosted (no Google CDN calls).
- assets/img/logo.png, aaron.png — from the existing brand asset library.
