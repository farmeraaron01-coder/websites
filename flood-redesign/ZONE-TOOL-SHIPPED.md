# Flood zone lookup — shipped 14 Aug 2026

Live: `/flood-zone-lookup/`. Theme 1.6.4, `[cfi_flood_zone_lookup]`.

## What it does

Address in, and it returns the flood zone, whether the property is in a Special
Flood Hazard Area, whether a federally backed lender will require cover, and the
base flood elevation where FEMA publishes one. Two free government endpoints, no
key, no cost: the US Census geocoder for address-to-coordinates, FEMA's National
Flood Hazard Layer for coordinates-to-zone.

Runs entirely in the visitor's browser. Property addresses never reach our server,
which is stated on the page because it is true.

## Verified live in Chromium

| case | result | routing |
|---|---|---|
| 915 I Street, Sacramento | Zone X, minimal hazard | `/get-a-quote/` + `/navigating-flood-zone-x/` |
| 250 Main St, Pajaro | Zone AH, in SFHA | `/get-a-quote/` + `/flood-zone-ah-and-ao/` |
| fabricated address | "could not be matched" | `/get-a-quote/` |

No console errors. No horizontal overflow at 390px.

## Two things that would have shipped broken

**1. WordPress silently destroyed the JavaScript.** The first version went in as
page content and the published page threw "Invalid or unexpected token" three
times, doing nothing at all. `wpautop` had injected **38 `<p>` and `</p>` tags
inside the `<script>` block** and `wptexturize` had turned every `&&` into
`&#038;&#038;`. Nothing in the editor hints at this. It was only caught by driving
a real browser at the live URL — reading the draft showed clean code. The page was
reverted to draft within minutes and rebuilt as a shortcode, whose output is not
passed back through `wpautop`.

**Standing rule: interactive markup goes in the theme, never in post content.**

**2. A California decision silently bound statewide.** Both brands share this child
theme, so uploading 1.6.3 to both put California's rates/cost merge live on
statewide, where none of the evidence applied. It turned statewide's
`/flood-insurance-rates/` into a two-hop chain. Host-gating in 1.6.4 fixed it, and
revealed the underlying fact: that URL **404s natively on statewide** — the page
never existed there, and the redirect had been masking a 404 for the wrong reason.
Zero impressions in twelve months, so a 404 is the correct state.

**Standing rule: anything in this theme applies to both brands. Gate by host
unless the evidence covers both.**

## Why it is built to feed other pages

Every zone result links on to the page that already ranks for that zone — X to
`/navigating-flood-zone-x/`, AH/AO, AE, A, V/VE, and anything unexpected to
`/which-flood-zone-requires-flood-insurance/`. All six of those pages now link
back to the tool.

That is deliberate and it is the inverse of the mistake corrected earlier today:
the tool concentrates traffic into pages that already rank instead of competing
with them for the same definitional queries.

## Conversion is segmented by the answer

Not one CTA. The tool already knows which conversation the visitor is in:

- **Inside an SFHA** — the lender will require cover, but who writes it is still a
  choice, so we quote both markets, and private can cover temporary housing the
  federal policy never does.
- **Outside it** — "nobody is going to make you buy this, which is exactly why it
  is worth a minute," with the $450 Zone X figure and 29% of claims coming from
  moderate-to-low-risk areas.

## Content targets what is underserved

Not zone definitions — the six zone pages own those. Instead:

- **Base flood elevation by address.** Those queries rank 25th to 46th and the tool
  returns the BFE. The page explains which zones carry one and which do not, and
  why Zone A frequently needs a surveyor.
- **Commercial due diligence.** The address-level queries in Search Console are
  commercial buildings — 525 B Street San Diego, 700 Wilshire, 9725 Scranton Road —
  sitting at position 9. NFIP commercial caps at $500k with no business
  interruption, which is the private-market opening.

## Aaron's constraint, built in rather than footnoted

> "if there are map changes from FEMA then the zone can and will change"

Every result states it reflects the map in effect today. The page covers
preliminary maps that exist before taking effect, LOMA/LOMR changes to a single
property, and that revisions move cost in **both** directions — including out of a
mandate, which is how owners end up paying for cover a newer map no longer
requires.

## The bigger opportunity is on statewide

Statewide's `/navigating-flood-zone-x/` holds **14,961 impressions at position
34.9** — seven times California's zone traffic, on page four. Its loss-of-use page
holds 2,563 impressions at position 6.5. The shortcode is already deployed there;
it needs a page and the statewide-appropriate copy. **This is the largest single
opportunity found today.**

---

## AI retrieval — the gap Aaron caught, 14 Aug 2026

> "did you write seo content or aiseo content for the flood zone look up tool?"

**Traditional SEO only.** Keyword-targeted sections, internal links, title and
meta description. Nothing written for retrieval by an assistant. Audited the live
page and confirmed it: `Article`, `WebPage`, `InsuranceAgency`, `BreadcrumbList` —
**no FAQPage, no WebApplication, no HowTo** — and every H2 opened with narrative
rather than an extractable answer.

That gap matters more here than on a typical site. The Search Console work found
this site carrying large impression counts with almost no clicks, and AI Overviews
absorbing the answer is the standing explanation. Being the source an assistant
quotes is the same problem, approached from the other end.

### What changed

**Direct answers first.** Every H2 now opens with a declarative sentence that
stands alone if lifted out of context:

- *"To find the flood zone for any U.S. address, enter it below."*
- *"Use the lookup above: it returns the base flood elevation whenever FEMA
  publishes one for that zone."*
- *"Flood zones change when FEMA revises a map, and a property can move in either
  direction."*
- *"Your flood zone determines whether flood insurance is mandatory. It does not
  determine your premium."*

**A table instead of a list** for base flood elevation by zone. Tables extract
cleanly; prose lists do not. It also surfaces the fact most guides omit — Zone A
has **no** determined BFE, which is why it needs a surveyor.

**Seven FAQ pairs**, which the theme's existing generator turned into **FAQPage
schema automatically** — verified live, all seven questions present. They are
written as the questions people actually ask, not keyword variants: how do I find
my zone, is this the zone my lender uses, can my zone change, why does my address
show no zone.

**WebApplication schema** (v1.6.5). The page already declared itself an Article.
Nothing said *this is a tool*, which is exactly what an assistant needs when
someone asks how to check a flood zone. It now declares a free WebApplication with
a feature list and cites the FEMA NFHL as its data source. Emitted from PHP, not
page content — JSON-LD in the editor goes through the same filters that destroyed
the JavaScript.

### Still not done

- No `HowTo` schema. Arguably applicable, but the honest answer to "how do I find
  my flood zone" on this page is "type it in the box," and a HowTo with one step is
  schema for its own sake.
- No `Speakable`. Low value here.
- The same treatment has not been applied to the cost page or the loss-of-use page,
  both of which carry quotable measured figures and would benefit more.
