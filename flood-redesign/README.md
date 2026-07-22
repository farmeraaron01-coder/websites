# Flood Insurance — Divi → Kadence Redesign Concept (Claude)

Design concept for modernizing **CaliforniaFloodInsurance.com** and **StatewideFloodInsurance.com**,
produced as a counterpart to the ChatGPT prototype referenced in the review handoff.

## Files

- `concept-homepage.html` — fully self-contained homepage concept (fonts, logo, and photos
  embedded as data URIs — just open it in a browser). A **Preview toggle** at the bottom-right
  switches the entire design system between the California and Statewide brands.
  Design-system notes (tokens, type, interior-page templates, Kadence mapping) are appended
  below the footer, clearly marked "not part of the site."

## Design system in one paragraph

Harbor navy `#0A2540` grounds the hero and footer; the brand cyan is evolved into an
accessible Pacific blue `#0891C7` (bright tint `#38C6F4` on dark); a single warm accent,
sunset gold `#F2A93B` (from the logo's sunset), is reserved exclusively for quote CTAs so the
conversion action is always the warmest pixel on screen. Statewide swaps the blues for deep
teal — same system, two brands. Type is Bricolage Grotesque (display) + Public Sans (body),
both Google Fonts that Kadence can self-host locally (~100 KB total). The one decorative motif
is a dashed **base-flood-elevation waterline** borrowed from elevation certificates — it anchors
the hero, the zone badge, and the CTA band, and it is literally what flood pricing is about.

## Key conversion changes vs. the current Divi sites

1. **Quote card in the hero** — the current sites have a single "Get Quote Now!" button in an
   empty flat-color hero. The concept puts a 60-second quote form (address + property type)
   above the fold, with a same-day-coverage ribbon.
2. **Trust made visible** — 4.9★ Google, 12,000+ policyholders, CA Lic. #0L75450, Est. 2012
   as hero chips and repeated in the quote card; carrier/market bar under the hero;
   licensed-expert section with author/byline E-E-A-T signals.
3. **Savings proof** — an NFIP-vs-private sample rate table (clearly footnoted as illustrative)
   plus one big average-savings number, replacing unsubstantiated exclamation points.
4. **Flood-zone finder teaser** — surfaces the zone/BFE story that drives both SEO and pricing,
   linking to the existing zone guide library.
5. **Performance-first** — no sliders, no video, text LCP, two subset font files; targets 95+
   mobile PageSpeed on Kadence.

## Status

The ChatGPT prototype (california-flood-insurance-kadence.farmeraaron01.chatgpt.site) requires
the owner's ChatGPT sign-in and could not be reviewed from this session; only `HANDOFF.md` from
the handoff folder was received. The side-by-side "best of both" comparison is pending access
to `prototype-source/`, `audit/`, and `DECISIONS.md`.
