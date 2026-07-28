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

## 5. After saving — one thing to report back

Copy the widget's **embed code or loader ID** and send it over.

As of child theme **v1.0.10** the ID is a single constant near the top of
`functions.php`, so swapping it is a one-line change:

    define( 'CFI_TRUSTINDEX_ID', '1e9552d4458412053506ba969a9' );

That is currently the production widget's ID. Replace it with the duplicate's ID when
it exists. Setting the constant to `''` renders the section with the rating block and a
plain "read our reviews on Google" link instead of the live feed — useful if the widget
is ever unavailable.

## 5a. Why duplicate rather than edit the live widget

The widget that production serves (`1e9552d4458412053506ba969a9`) is doing ~3,000
views/30 days. Launch is still weeks out, so editing it in place would degrade the live
homepage now for no benefit. Duplicate it, configure the copy, leave the original alone.

A widget ID is a **display configuration**, not a review source. Duplicating one does not
split, copy, or divide the 932 reviews — both widgets read the same connected Google
Business Profile.

## 5b. Both brands share one review pool

CaliforniaFloodInsurance.com and StatewideFloodInsurance.com are the same parent company
and share a single Google Business Profile. This is intentional. Consequences:

- The Statewide build needs **no second Trust Index connection**. It can reuse this same
  widget ID, or take its own styled copy of the same feed if the palette needs to differ.
- Reviews earned under either brand count for both.
- Nothing about the Trust Index account organization needs changing.

## 6. Verification

1. Load `https://new.californiafloodinsurance.com/` in a logged-out/private window.
2. Scroll to the reviews section — real Google reviews should appear in a rotating slider.
3. Confirm the rating appears **once** (our block above the widget), not twice.
4. Confirm cards are readable, stars are gold, and nothing overflows on a phone width.
5. Purge the hosting cache.
