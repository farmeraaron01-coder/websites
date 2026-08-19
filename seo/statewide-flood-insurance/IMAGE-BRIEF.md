# Image brief — four state pages + the hub

Every one of these pages ships a data table and zero in-content imagery. Our own
CFI audit flagged that twice (*"the image gap is the one thing a patch can't
fix"*) and we then repeated it across five new pages. This closes it.

All five currently share one generic `og:image`
(`coastal-homes-golden-hour.webp`) and carry one image apiece — the author
headshot, which has an **empty `alt`** on all four state pages. Fix that at the
same time: it should read `Aaron J. Farmer, licensed flood insurance agent`,
matching the CFI pattern.

**Charts are a separate deliverable.** Generate those as SVG from the data, not
through an image model — bar heights and axis labels must be exact. This file
covers photography only.

---

## Generation prompts

Prepend this to every prompt:

```
Editorial documentary photograph for an insurance information article.
Natural daylight, realistic, photojournalistic. Shot on 35mm, medium
depth of field. Muted natural color, no HDR, no dramatic filters.
Absolutely no text, lettering, signage, numbers, logos or watermarks
anywhere in the image. No recognizable faces. Not a disaster scene —
calm, ordinary, documentary. 16:9 landscape.
```

**Arizona**
```
A dry desert wash cutting between ordinary stucco single-family homes on
the outskirts of a Phoenix suburb, shallow monsoon runoff moving through
the channel, desert scrub and a saguaro at the edge, late afternoon light,
clearing monsoon clouds behind the mountains.
```

**Oklahoma**
```
A modest creek running high and muddy after heavy rain, at the edge of a
flat Midwestern neighborhood of single-story brick homes, wide open sky
with storm clouds breaking apart, mature shade trees, early evening light.
```

**Texas**
```
A flat suburban street in the Houston area after heavy rain, a bayou
drainage channel running alongside it, live oaks, one-story brick ranch
homes set low to the ground, standing water at the curb, humid overcast
light.
```

**Florida**
```
A low-lying Florida residential neighborhood beside a drainage canal,
single-story homes with tile roofs, palms and saw palmetto, flat terrain
barely above the waterline, warm late-afternoon light with an afternoon
thunderstorm receding in the distance.
```

**Hub**
```
An elevated wide view of a river bending past an ordinary American
suburban development, mixed housing and green space, flat floodplain
terrain, soft overcast daylight, calm and neutral in mood.
```

Generate at **1600×900**. Re-crop each to **1200×630** for the social image.

---

## Metadata — in-content images (1600×900)

### Arizona — `/arizona-flood-insurance/`
- **Filename:** `arizona-desert-wash-flooding-phoenix.webp`
- **Title:** Arizona Desert Wash Flooding Near Phoenix Homes
- **Alt:** Desert wash running behind suburban homes near Phoenix after monsoon rain
- **Caption:** Most Arizona flood exposure is monsoon flash flooding through desert washes like this one, not river rise. Zone AO — shallow sheet flow — is the least expensive cover we write in the state, at a median of $464 a year.

### Oklahoma — `/oklahoma-flood-insurance/`
- **Filename:** `oklahoma-creek-flooding-after-heavy-rain.webp`
- **Title:** Oklahoma Creek Running High After Heavy Rain
- **Alt:** Creek running high beside a flat Oklahoma neighborhood after heavy rainfall
- **Caption:** Oklahoma's hazard is intense, short-duration rainfall over creeks and urban drainage rather than seasonal river rise. Exposure varies street to street: the state median is $465, but one property in ten prices above $1,109.

### Texas — `/texas-flood-insurance/`
- **Filename:** `texas-houston-bayou-drainage-street.webp`
- **Title:** Houston Bayou Drainage Beside a Residential Street
- **Alt:** Bayou drainage channel alongside a low-lying Houston-area residential street
- **Caption:** Fifty-eight percent of the Texas properties we quote sit in Zone X, outside the mapped high-risk floodplain. Harvey flooded tens of thousands of homes on streets like this one regardless.

### Florida — `/florida-flood-insurance/`
- **Filename:** `florida-canal-neighborhood-low-elevation.webp`
- **Title:** Low-Elevation Florida Neighborhood Beside a Canal
- **Alt:** Low-elevation Florida neighborhood beside a drainage canal
- **Caption:** Florida's flood exposure is statewide rather than concentrated in one basin. Inland Zone X neighbourhoods and coastal AE properties sit a few miles apart, and premiums run from under $472 to past $1,643.

### Hub — `/flood-insurance-cost-by-state/`
- **Filename:** `flood-insurance-cost-by-state-river-floodplain.webp`
- **Title:** River Floodplain Bordering a Suburban Development
- **Alt:** River floodplain bordering an American suburban development
- **Caption:** Median all-in private flood premiums across 7,165 properties in 27 states range from $369 in Michigan to $869 in Connecticut.

---

## Metadata — social images (1200×630)

| Page | Filename | Title |
|---|---|---|
| Arizona | `arizona-flood-insurance-og.webp` | Arizona Flood Insurance — Social Preview |
| Oklahoma | `oklahoma-flood-insurance-og.webp` | Oklahoma Flood Insurance — Social Preview |
| Texas | `texas-flood-insurance-og.webp` | Texas Flood Insurance — Social Preview |
| Florida | `florida-flood-insurance-og.webp` | Florida Flood Insurance — Social Preview |
| Hub | `flood-insurance-cost-by-state-og.webp` | Flood Insurance Cost by State — Social Preview |

Social images need no caption and no alt — they are never rendered in the page.
Set each in **Rank Math → Social tab → Facebook Image** on the individual page.

---

## Placement

Put the in-content image **immediately above the cost table**, so the reader
meets the terrain before the numbers. On the four state pages that is directly
under the opening paragraph; on the hub, directly under the `Key Findings`
section.

Caption goes in the WordPress caption field, not typed as a paragraph — that
renders it inside `<figcaption>`, which is what makes it an extraction signal
rather than loose body text.

---

## Rules that matter

- **Rename the file before uploading.** An image model will hand you something
  like `Gemini_Generated_Image_a7f3k2.png`. Once it is in the media library the
  URL is fixed, and renaming later breaks every reference to it.
- **Filename is a stronger signal than the Title field.** Google reads it
  directly.
- **Title is not alt.** WordPress uses alt for accessibility and search, title
  for the media library and hover tooltip. Identical text in both wastes a
  field.
- **Convert to WebP and keep each under ~200 KB.** These pages already load
  114–121 KB of HTML; do not undo that with a 2 MB hero.
- **Set explicit width and height** so the image does not cause layout shift,
  and lazy-load everything except the topmost image on the page.
- **Verify with a cache-busting query string** (`?cb=$(date +%s%N)`) — a plain
  anonymous fetch on this account has returned pre-edit content while reporting
  `x-proxy-cache: MISS`.
