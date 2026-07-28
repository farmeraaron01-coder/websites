# Trust Index setup — new.californiafloodinsurance.com

Context: the homepage template already renders the widget container and lazy-loads the
Trust Index script when the reviews section nears the viewport. Only the plugin/widget
configuration is needed. The homepage also displays its own "4.9 / 900+ Google reviews"
summary block immediately above the widget.

## 1. Layout

Select **Slider I.** — three review cards, **no header/summary row**.

Reason: the page already shows a rating summary above the widget; a layout with its own
summary (Slider II, Slider V) would display the rating twice in a row. Slider I is also
on the free tier.

## 2. Content settings

| Setting | Value | Why |
|---|---|---|
| Source | Google Business Profile — **California Flood Insurance Services** | Same profile as the production site |
| Minimum rating | **4 stars and up** | Keeps the section on-message; do not hide legitimate criticism elsewhere on the site |
| Number of reviews | **15–20** | Enough for the slider to rotate without repeating |
| Sort order | **Newest first** | Freshness is a trust signal |
| Review text length | **Truncate with "Read more"** | Keeps card heights even; prevents layout shift |
| Empty/no-text reviews | **Hide** | Star-only reviews add nothing visually |
| Language filter | English | |

## 3. Style settings

| Setting | Value |
|---|---|
| Theme / color scheme | **Light** |
| Font | **Inherit from theme** if offered; otherwise **Inter** |
| Star color | Leave default gold/amber (matches the site's review-star color `#F2B01E`) |
| Card background | White (`#FFFFFF`) |
| Text color | `#44607A` |
| Name/heading color | `#12283F` |
| Border radius | ~10px if adjustable |
| "Powered by Trust Index" branding | **Off** if the plan allows |

## 4. Advanced / performance

| Setting | Value | Why |
|---|---|---|
| **Schema / rich snippet markup** | **OFF** | Important. Google's structured-data guidelines disallow self-serving review markup — a business marking up reviews about itself on its own site. Leaving this on risks a manual action; the reviews still display normally with it off. |
| Lazy load | **On** (or leave default) | The theme already defers the script; both together is harmless |
| Load CSS inline / minified | On if offered | Fewer requests |
| Cache reviews locally | **On** | Serves reviews from the site instead of calling Trust Index on every load |
| Open reviews in new tab | On | Keeps visitors on the page |

## 5. Widget ID — DONE (child theme v1.0.11)

The staging widget is **`CFI new site — homepage reviews`**, ID `bcdff9477ef19568e30684fd16d`,
created July 28 2026 as a duplicate of the production widget. It is wired into the theme
as a single constant near the top of `functions.php`:

    define( 'CFI_TRUSTINDEX_ID', 'bcdff9477ef19568e30684fd16d' );

Setting the constant to `''` renders the section with the rating block and a plain
"read our reviews on Google" link instead of the live feed — useful if the widget is
ever unavailable.

### Verified on the new widget (July 28 2026)

| Checked | Result |
|---|---|
| Header row | Gone (page renders its own `.cfi-rating` block) |
| Cards | 18, newest first (July 22 → June 30), all 5-star, no empty-text reviews |
| Truncation | "Read more" active |
| Name colour | `rgb(18, 40, 63)` = `#12283F` ✓ |
| Review text colour | `rgb(68, 96, 122)` = `#44607A` ✓ |
| Cards | White, 10px radius, transparent widget background |
| Font | Inherited from theme — `Inter, -apple-system, "Segoe UI", sans-serif`, not Trustindex Poppins |
| Rich snippet | **Off** — zero `ld+json`, zero microdata, `richsnippet.js` never requested |
| Source | Pinned to Google → California Flood Insurance Services (not "All platforms") |
| Network cost | 5 requests vs the old widget's 10; WebP sprite = 1 image for all 18 avatars |
| Stars | "Original" gold |
| Trustindex badge | Not present on this widget |

**Source pinning matters.** "All platforms" auto-adopts anything connected later, and that
domain entry already has a Trustindex platform attached. Keep it pinned to Google.

### Two settings to change

1. **Review photos — turn OFF.** *(Approved July 28.)* Inherited from production. A review
   with an attached photo renders taller than one without, which defeats the
   even-card-height goal that the truncation setting exists to serve.
2. **Delay load — turn OFF; keep lazy load ON.** Delay load waits for visitor
   interaction before displaying, and its stated benefit is keeping the widget out of
   PageSpeed results. The theme already gates the script with an IntersectionObserver at
   400px, so the performance work is done honestly — this second gate only adds a risk
   that the section looks empty on arrival. Hiding a widget from Lighthouse is not the
   same as it being fast.

### Review freshness

There is no "cache reviews locally" toggle; the equivalent is **Refresh: daily**, which is
correct and already set. Trustindex bakes the widget into a static `content.html` on its
CDN and re-fetches from Google once a day, so visitor page loads never hit a live API.

## 5a. Why duplicate rather than edit the live widget

Widget `1e9552d4458412053506ba969a9` is embedded on **both** production homepages —
verified in served HTML, July 28 2026:

- `californiafloodinsurance.com` — WP-enqueued, lazy (`data-type="lazy"`)
- `statewidefloodinsurance.com` — inside a Divi code module (`et_pb_code_1`)

Same ID on both. So editing that widget in place changes two live homepages at once,
covering their combined ~3,000 views/30 days. Launch is still weeks out. Duplicate it,
configure the copy, leave the original alone.

A widget ID is a **display configuration**, not a review source. Duplicating one does not
split, copy, or divide the 932 reviews — both widgets read the same connected Google
Business Profile.

## 5b. Both brands share one review pool

CaliforniaFloodInsurance.com and StatewideFloodInsurance.com are the same parent company
and share a single Google Business Profile. This is intentional, and production already
implements it — one widget, both sites. Consequences:

- The Statewide build needs **no second Trust Index connection**. It can reuse the same
  widget ID, or take its own styled copy of the same feed if the palette needs to differ.
- Reviews earned under either brand count for both.
- Nothing about the Trust Index account organization needs changing.
- Turning the rich snippet off on the shared widget fixes both sites in one action.
- Statewide's embed is a Divi code module, so it does not survive the Divi migration —
  the Kadence build carries it in the template via `CFI_TRUSTINDEX_ID` instead.

## 5c. Branding badge

The "Verified by Trustindex" badge renders on production today, so the current plan does
not allow hiding it. Expect it on the new homepage. Not worth upgrading to remove.

## 5d. STILL OPEN — rich snippet on the production widget

The duplicate has rich snippet off. **The production widget still has it on**, confirmed
July 28 2026: `1e9552d4458412053506ba969a9` requests both `richsnippet.js` and
`richsnippet.json` and injects a `Product`-typed block with `aggregateRating` and
individual `review` nodes at runtime.

That is self-serving review markup on a mistyped entity, live on both production
homepages, and Googlebot renders JS so it is being read. Turning the toggle off on that
one widget fixes both sites at once and changes nothing a visitor sees — Google stopped
displaying self-serving review stars for `LocalBusiness`/`Organization` types in 2019, so
they were never rendering in results.

This is the only remaining Trust Index action, and it is on production, not staging.

## 5e. Related, but not a Trust Index problem

The CFI homepage also serves a **hardcoded** `aggregateRating` (4.9 / 900) on its
`InsuranceAgency` JSON-LD node, from a source other than Trust Index. Same self-serving
review-markup guideline, and turning off the widget's rich snippet does not touch it.
That block additionally carries "rates 30–50% lower than the National Flood Insurance
Program" in its `description`, contradicting DECISIONS.md. Statewide's source has neither.

## 6. Verification

1. Load `https://new.californiafloodinsurance.com/` in a logged-out/private window.
2. Scroll to the reviews section — real Google reviews should appear in a rotating slider.
3. Confirm the rating appears **once** (our block above the widget), not twice.
4. Confirm cards are readable, stars are gold, and nothing overflows on a phone width.
5. Purge the hosting cache.
