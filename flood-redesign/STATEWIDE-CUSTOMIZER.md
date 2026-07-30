# Statewide Staging — Kadence Customizer Setup (Chrome Claude runbook)

Site: https://staging.statewidefloodinsurance.com/wp-admin/ → Appearance → **Customize**
This is the statewide equivalent of CFI's HEADER-FOOTER-SETUP.md — same structure, teal
palette, and it includes the footer **widget-area placement** step CFI got later (the
four-column link footer already exists as widgets; it renders nothing until the footer
builder places its widget area).

Publish once at the end. Cache purge note at the bottom.

---

## Step 1 — Global Palette (Customize → Colors & Fonts → Colors)

| Slot | Hex | Role |
|---|---|---|
| 1 | `#35CFC9` | Action teal (buttons/accents) |
| 2 | `#0E8E8A` | Sea teal (link hover) |
| 3 | `#092C35` | Deep sea navy (dark grounds, button text) |
| 4 | `#12283F` | Ink (headings) |
| 5 | `#44607A` | Ink-2 (body/nav text) |
| 6 | `#6E8AA3` | Ink-3 (captions) |
| 7 | `#D2E5E3` | Line (borders) |
| 8 | `#E5F2F1` | Mist (alt background) |
| 9 | `#F7FAFC` | Paper (page background) |

## Step 2 — Header (Customize → Header)

### 2a. Top Bar
The HTML element with the `.cfi-topbar` markup is already in the top row. Set the Top Bar
**Design** tab: Background `#092C35` · Text color `#9CCFD1` · Link color `#35CFC9` ·
Min height **36px** · No bottom border. HTML element font size **13px**.

### 2b. Main Row
- **Logo:** already set (the round badge). Set Logo max height **56px** (the badge is dense;
  48px like CFI's makes it unreadable). **Hide Site Title** (logo only) and hide tagline —
  right now the title text renders next to the badge.
- **Primary Navigation:** menu already assigned. Nav typography size **14.5px**, weight
  **600**. Link color `#44607A`, hover `#0E8E8A`, active `#12283F`.
- **Button element** (drag into the right slot):
  - Label: `Start My Quote` · Link: `/get-a-quote/`
  - Filled. Background `#35CFC9`, hover `#1FB5AF`. Text `#092C35` both states.
  - Weight **600**, size **14.5px**, radius **8px**, padding ~10px/18px.
  - (The old "Same Day Quote!" menu item is already removed — the button replaces it.)
- Main Row **Design**: Background `#FFFFFF` · Min height **74px** · Bottom border
  **1px solid `#D2E5E3`**.

### 2c. Behavior
- Sticky Header **ON**, Main Row only (top bar not sticky), Shrink off.
- Transparent Header **OFF**.

### 2d. Mobile header
- Logo left, hamburger right. Mobile menu = same Primary menu.
- Popup background `#092C35`, link color `#EAF7F6`.

## Step 3 — Footer (Customize → Footer) — THE IMPORTANT ONE

The four-column link footer + legal row already exist as two Custom HTML widgets in
**Footer Area 1**. They render nothing until placed:

1. In the footer builder grid, drag **Widget Area — Footer 1** (may be labeled
   "Footer - 1" / "Footer Area 1") into the **Bottom Row**, single column.
2. Bottom Row **Design**: Background `#0D3944` · Text `#9CCFD1` · Link color leave —
   the theme CSS styles the links (`--cfi-foot-link`) · padding ~24px top/bottom.
3. Remove/leave empty every other footer row, including the default copyright bar
   ("WordPress Theme by Kadence WP" must not ship).

The theme's CSS already handles the column grid inside (`.cfi-foot`), including the
Kadence two-column row quirk — no width fiddling needed.

## Step 4 — Additional CSS (Customize → Additional CSS)

```css
#masthead, #colophon { font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; }
#masthead .site-branding img { width: auto; }
#masthead .header-button { box-shadow: 0 2px 0 rgba(0,0,0,.10); }
#masthead .main-navigation .menu-item > a { letter-spacing: .01em; }
#colophon a:hover { color: #ffffff; }
```

## Step 5 — Nginx Helper purge switch (NOT Customizer — Settings → Nginx Helper)

Check **Enable Purge**. Caching method: **nginx FastCGI cache**. Purge method:
**Delete local server cache files**. Leave default purge-on-edit/publish boxes checked.
Save. (Without this, every edit takes up to a day to appear on live URLs — this is also
why PSI graded a stale page earlier today.)

## Step 6 — Finish

1. **Publish** the Customizer.
2. Admin bar → **Purge Cache** (appears once Nginx Helper purge is enabled).
3. Report back; visual verification happens from the other side.
