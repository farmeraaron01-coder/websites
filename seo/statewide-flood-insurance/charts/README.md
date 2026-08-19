# Charts — five pages

Generated from the quote book, not drawn by an image model. Every bar length and
every label is computed from the same figures already published in each page's
table, so the chart and the table cannot disagree.

| File | Page | Form |
|---|---|---|
| `arizona-flood-insurance-cost-by-zone.svg` | `/arizona-flood-insurance/` | Horizontal bar, 4 zones |
| `oklahoma-flood-insurance-cost-by-zone.svg` | `/oklahoma-flood-insurance/` | Horizontal bar, 3 zones |
| `texas-flood-insurance-cost-by-zone.svg` | `/texas-flood-insurance/` | Horizontal bar, 3 zones |
| `florida-flood-insurance-cost-by-zone.svg` | `/florida-flood-insurance/` | Horizontal bar, 4 zones |
| `flood-insurance-cost-by-state-range.svg` | `/flood-insurance-cost-by-state/` | Range plot, 27 states |

## How to embed

**Use a Custom HTML block and paste the SVG source inline.** Do not upload these
as `.svg` files — WordPress blocks SVG upload by default for security reasons,
and inline SVG keeps the labels as real text, which is what makes the numbers
readable to screen readers and extractable by AI answer engines. A PNG of a
chart is opaque to both.

Wrap each one like this, directly **above** the existing data table:

```html
<figure style="margin:28px 0;">
  <!-- paste the entire contents of the .svg file here -->
  <figcaption style="font-size:14px;color:#555;padding-top:10px;">
    CAPTION GOES HERE
  </figcaption>
</figure>
```

The chart goes above the table, not instead of it. The table stays — it is the
accessible alternative view and the better source for AI extraction.

## Captions

**Arizona** — Arizona zone medians sit within roughly $120 of each other, from
$464 in Zone AO to $581 in Zone AE. Under Risk Rating 2.0 the zone letter
determines whether your lender requires cover; it does not determine your price.

**Oklahoma** — Oklahoma Zone X at $372 is the least expensive figure anywhere in
our national book. The state median is $465, but one property in ten prices
above $1,109.

**Texas** — Texas Zone AE at $892 prices $278 above Zone X at $614, one of the
widest zone gaps in our book — Texas coastal and bayou AE zones carry genuine
surge and deep-riverine exposure.

**Florida** — Florida Zone AE at $895 sits at the top of our national book
alongside Texas. Fifty-eight percent of the Florida properties we quote are in
Zone X, where no federal rule requires cover at all.

**Hub** — Median private flood premiums across 27 states, with the middle half
of quotes shown as a bar. Medians run from $369 in Michigan to $869 in
Connecticut, and the spread within a state is often wider than the gap between
states.

That last caption is the honest headline of the whole dataset and worth keeping
verbatim — it is the argument for getting a quote rather than trusting an
average.

## Design notes

- **One hue, not one hue per bar.** These show a single measure across
  categories, so colouring each bar differently would be decoration, not
  encoding.
- **Colour is `#0A9B95`** — a half-step off the site's brand teal `#0E8E8A`,
  chosen because the brand value fails the chroma floor (it reads grey) while
  this one passes lightness band, chroma and contrast against a light surface.
  Validated, not eyeballed.
- **Text never wears the series colour.** Labels and values use ink tones so
  they stay legible independently of the bars.
- **The hub plots the median as a dot in its own labelled column**, not at the
  end of the range bar. A first draft put the value at the bar end, where
  Alabama's `$782` sat beside the $1,592 endpoint and read as if it labelled it.
- **Accessibility** is carried by `role="img"` plus `<title>` and `<desc>` on
  each SVG, which spell out every value in prose.
- Charts scale to their container via `viewBox` and `width:100%`, so they stay
  sharp on any screen and add zero HTTP requests.

## Regenerating

`scratchpad/gen_charts.py` builds all five from inline data. If a median
changes, edit the data at the bottom of that script and re-run — do not hand-edit
the SVG, or the bar length and the label will drift apart.
