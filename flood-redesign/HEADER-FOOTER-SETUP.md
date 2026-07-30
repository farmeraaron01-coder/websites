# CFI Staging — Kadence Header & Footer Setup

Site: https://new.californiafloodinsurance.com/wp-admin/ → Appearance → **Customize**
Every value below is exact. Publish once at the end, then purge the hosting cache.

---

## Step 0 — one leftover setting (not in Customizer)

Settings → General → **Timezone: Los Angeles** → Save.

---

## Step 1 — Global Palette

Customize → **Colors & Fonts → Colors** (Global Palette). Set the nine swatches:

| Slot | Hex | Role |
|---|---|---|
| 1 | `#25C1EE` | Action cyan (buttons/links-accent) |
| 2 | `#0891C7` | Pacific blue (link hover) |
| 3 | `#0A2540` | Harbor navy (dark grounds, button text) |
| 4 | `#12283F` | Ink (headings) |
| 5 | `#44607A` | Ink-2 (body/nav text) |
| 6 | `#6E8AA3` | Ink-3 (captions) |
| 7 | `#D5E3EC` | Line (borders) |
| 8 | `#E7F0F6` | Mist (alt background) |
| 9 | `#F7FAFC` | Paper (page background) |

## Step 2 — Header (Customize → Header)

### 2a. Top Bar (drag elements in the builder's top row)

- **Left slot:** HTML element →
  `CA Lic. #0L75450 &nbsp;·&nbsp; Independent agency specializing in flood since 2012`
- **Right slot:** not used. Kadence Free permits only **one** HTML element per header, and it
  is spent on the left slot. (Had this been added it would also have needed the hours
  corrected to 7:30am — see the GBP data in PLUGIN-PLAN.md.)
- Top Bar **Design** tab: Background `#0A2540` · Text color `#9FBDD4` · Link color `#38C6F4` · Min height **36px** · Bottom border: none.
- HTML element font size: **13px**.

### 2b. Main Row

- **Left slot: Logo.** Upload `logo.png` from the child theme
  (`wp-content/themes/cfi-kadence-child/assets/img/logo.png` — or Media → Add New and pick it
  from your computer; it's the round badge). Logo max height **48px**. Site Title: **hide**
  (logo only). Tagline: hide.
- **Center/right slot: Primary Navigation.** (The menu named "Primary" already exists with
  Residential, Commercial, Condo & HOA, Guides, Get a Quote.)
  - Nav typography: size **14.5px**, weight **600**.
  - Link color `#44607A`, hover `#0891C7`, active `#12283F`.
- **Right slot: Button.**
  - Label: `Start My Quote`
  - Link: `/get-a-quote/`
  - Style: Filled. Background `#25C1EE`, hover background `#0FAAD8`.
  - Text color `#0A2540` (both states). Font weight **600**, size **14.5px**.
  - Border radius **8px**. Padding roughly 10px top/bottom, 18px sides.
- Main Row **Design**: Background `#FFFFFF` · Min height **74px** · Bottom border **1px solid `#D5E3EC`**.

### 2c. Behavior

- **Sticky Header: ON** for the Main Row only (top bar not sticky). "Shrink" off.
- **Transparent Header: OFF** everywhere (the hero supplies its own dark ground).

### 2d. Mobile header

- Mobile row: Logo left, Trigger (hamburger) right, plus the same Button if it fits.
- Mobile menu = Primary menu. Popup background `#0A2540`, link color `#EAF4FB`.

## Step 3 — Footer (Customize → Footer)

Launch-simple version now; the four-column link footer comes with content migration.

- **Bottom Row only** (remove/leave empty other rows):
  - Left slot: HTML element →
    `© 2026 California Flood Insurance. All rights reserved. CA License #0L75450.`
  - Right slot: HTML element →
    `Coverage is subject to underwriting, policy terms, conditions, and exclusions. &nbsp; <a href="https://www.statewidefloodinsurance.com/">Outside California? Statewide Flood Insurance</a>`
- Bottom Row **Design**: Background `#0A2540` · Text `#9FBDD4` · Link color `#38C6F4` · font size **13px** · padding ~20px top/bottom.

## Step 4 — Additional CSS

Customize → **Additional CSS** → paste this block (harmonizes Kadence's header/footer with the
theme fonts and keeps the button crisp):

```css
#masthead, #colophon { font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; }
#masthead .site-branding img { width: auto; }
#masthead .header-button { box-shadow: 0 2px 0 rgba(0,0,0,.10); }
#masthead .main-navigation .menu-item > a { letter-spacing: .01em; }
#colophon a:hover { color: #ffffff; }
```

## Changing the top-bar text later

Appearance → **Customize → Header**. In the Header Builder grid under the preview, click the
**HTML 1** chip in the Top Row's left slot (or **Header → Elements → HTML 1**). Edit the
**Content** box, then **Publish**.

Note the `&nbsp;` entities are intentional — they hold the spacing around the middot.

## Step 5 — Finish

1. Click **Publish** (top of Customizer).
2. wp-admin toolbar → **Purge Cache**.
3. Tell Claude — verification (screenshots vs. the design mock + Lighthouse re-run) happens from the other side.
