# Charts — five pages

Generated from the quote book, not drawn by an image model. Every bar length and
every label is computed from the same figures already published in each page's
table, so the chart and the table cannot disagree.

| File | Page | Form |
|---|---|---|
| `florida-flood-insurance-cost-by-zone.svg` | `/florida-flood-insurance/` | Horizontal bar, AE vs X |
| `texas-flood-insurance-cost-by-zone.svg` | `/texas-flood-insurance/` | Horizontal bar, AE vs X |
| `arizona-flood-insurance-premium-spread.svg` | `/arizona-flood-insurance/` | Percentile spread |
| `oklahoma-flood-insurance-premium-spread.svg` | `/oklahoma-flood-insurance/` | Percentile spread |
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

## Why these do not chart every zone

A first draft charted all four Florida zones and put **Zone X ($617) above Zone
A ($562)** — low-risk apparently costing more than high-risk. That is backwards
against everything known about flood zones, and it is an artifact.

Checked across all 81 state-zone rows:

- **Zone X prices below Zone A in 14 of the 17 states** where both are reported.
  California, our largest book by far, is unambiguous: X $516 from 455
  properties against A $711 from 480.
- **It inverts in exactly three states — Florida, Texas and Arizona** — and in
  all three the Zone A sample is tiny against the Zone X sample: 24 vs 198 in
  Florida, 32 vs 212 in Texas, 36 vs 32 in Arizona.
- **Zone AE prices above Zone X in 25 of 25 states.** That comparison is solid
  everywhere and is what the charts show.

So the rule applied here: **a zone is only charted when it clears 50 quoted
properties.** That leaves Florida and Texas with a clean AE-vs-X comparison and
leaves Arizona and Oklahoma with no chartable zone at all.

Arizona would fail on a second count anyway — its zone medians are AE $581, X
$568, A $558, a $23 total spread on samples of 107, 32 and 36. Those differences
are inside the noise, and a bar chart would draw visible distinctions that the
data does not support. Arizona and Oklahoma therefore get a **percentile spread**
instead, which is well supported at n=203 and n=93 and makes the stronger point:
the variation within a state dwarfs the variation between zones.

> **Open item for the live pages.** The published tables on Florida, Texas and
> Arizona still show the inverted Zone A row, and the hub's methodology note sets
> the reporting threshold at "at least 10 properties" — too low for a figure a
> reader will treat as a price. Raising that to 50 and dropping the thin rows is
> a content decision, not a chart fix.

## Captions

**Arizona** — Half of Arizona quotes land between $464 and $800, against a
median of $547. Zone AE, the only Arizona zone with enough quotes to publish,
sits just $34 above that median.

> The earlier version of this caption said Arizona's zone medians sit within $23
> of each other. That $23 is derived from the Zone A, X and AO medians which the
> 50-quote threshold suppresses — we cannot call them too thin to publish and
> then publish a conclusion drawn from them. It is also wrong: Zone AO is $117
> below Zone AE, not $23.

**Oklahoma** — Half of Oklahoma quotes land between $350 and $675, against a
median of $465. But one property in ten prices above $1,109, which is what a
flash-flood state looks like in pricing data.

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
