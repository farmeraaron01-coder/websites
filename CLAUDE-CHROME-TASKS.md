# Step-by-Step Fix Tasks — for Claude in Chrome (inside WordPress admin)

Written July 13, 2026, from a live verification of both sites. Do tasks in order; each has a **Verify** step — don't move on until it passes. Palm Desert items are dropped per Aaron — everything here is San Diego + the two websites.

Content referenced below lives in this repo:
- `jumpins.com/content/blog/` — 3 new San Diego posts (each file contains the meta description, slug, and a ready-to-paste FAQ schema block at the bottom)
- `jumpins.com/fixes/schema-faq-earthquake-example.json` — FAQ schema for the existing earthquake post
- `cheapearthquakeinsurance.com/content/` — homepage FAQ section + commercial earthquake article

---

## PART A — jumpins.com (WP Admin: jumpins.com/wp-admin)

### Task A1 — Fix authorship on the 3 new posts (10 min) 🔴 top priority

The three posts published June 25 show author **"Admin"**. Older posts correctly show Aaron Farmer.

1. Go to **Posts → All Posts**. Find these three:
   - Earthquake Insurance in California 2026
   - Wildfire Home Insurance California 2026
   - California Home Insurance Non-Renewal Crisis 2026
2. For each: hover → **Quick Edit** → change **Author** dropdown to **Aaron Farmer** → Update.
   - If Aaron Farmer isn't in the dropdown: **Users → All Users** — confirm his account exists and its role can author posts; if his display name is wrong, edit the user and set **Display name publicly as** to "Aaron Farmer".
3. Add the license number to the author profile: **Users → Profile (Aaron's)** → in **Biographical Info** enter:
   > Aaron Farmer is the principal agent at Jump Insurance Services, an independent insurance agency with a San Diego office. CA License #0F09648.
4. **Verify:** open each post logged-out (incognito). Byline shows "Aaron Farmer", and View Source shows `"author":{"name":"Aaron Farmer"` in the Yoast schema block — not "Admin".

### Task A2 — Make blog post titles render as H1 (20 min) 🔴

Live posts currently render only H2s — no `<h1>` in the HTML. This is the Divi blog template.

1. Go to **Divi → Theme Builder**. Look for a template assigned to **All Posts** (or Post templates).
2. Open its body layout. Find the **Post Title** module → settings → **Design → Title Text → Title Heading Level** → set to **H1** → save layout, save Theme Builder changes.
3. If there is **no** post template in Theme Builder (posts use the default Divi template): go to **Divi → Theme Options** and check the Blog settings; if no H1 option exists, the fallback is to open each of the 6 blog posts and make the first text element inside the content an H1 matching the title — but try the Theme Builder route first, it fixes all posts at once.
4. **Verify:** open `/earthquake-insurance-california-2026/` logged-out → View Source → exactly one `<h1>` containing the post title. Spot-check one older post too.

**A2 addendum (July 13) — Divi builder times out and won't open the All Posts template.** Verified blocker: the visual builder fails in the Theme Builder modal, standalone layout URL, and per-post builder; the timeout dialog cites the pending WordPress 7.0.1 update and Divi 4.27.5 → 4.27.7. Titles are injected by the template's Post Title module (as H2), so per-post edits can't fix it. Do this instead:

- **A2-alt (do now, no builder needed):** install the snippet `fixes/post-title-h1-snippet.php` via WPCode (Code Snippets → Add New → PHP Snippet → paste → Auto Insert / Frontend Only → Activate). It rewrites only the `<h2 class="entry-title">` on single posts to `<h1>`, skips pages that already have an H1 title, and touches nothing else. If a caching plugin is active, clear the cache after activating. **Verify** as in step 4 above.
- **A2-proper (needs Aaron's go-ahead — do NOT run updates unprompted):** with a full backup/snapshot first (host panel or UpdraftPlus), update Divi to 4.27.7 (Dashboard → Updates or Divi theme update; requires the Elegant Themes license to be active), then WordPress 7.0.1. These updates should be run soon regardless — an outdated core/theme on a lead-gen site is a security exposure, and the Divi patch very likely clears the builder timeout. Once the builder opens: All Posts template → Post Title module → Design → Title Text → Title Heading Level → H1, save — then **deactivate the WPCode snippet** so the fix lives in one place.

### Task A3 — Add FAQ schema to the existing earthquake post (10 min) 🟠

1. **Posts → Earthquake Insurance in California 2026 → Edit** (with Divi builder).
2. Add a **Code module** at the very bottom of the post body.
3. Paste the entire contents of `jumpins.com/fixes/schema-faq-earthquake-example.json` wrapped in:
   `<script type="application/ld+json"> … </script>`
4. Update/publish.
5. **Verify:** run the post URL through https://search.google.com/test/rich-results → FAQ detected, no errors.

### Task A4 — Add the CheapEarthquakeInsurance.com link to the earthquake post (5 min) 🟠

The live post has **no link** to cheapearthquakeinsurance.com.

1. Same post as A3. Find the closing section (the "get a quote" call-to-action near the end).
2. Add this sentence (or edit the existing CTA to include it):
   > For a fast online earthquake quote, visit our dedicated earthquake insurance site, [CheapEarthquakeInsurance.com](https://www.cheapearthquakeinsurance.com/).
3. Do **not** paste any article text from this post onto cheapearthquakeinsurance.com — unique copy per domain, links only.
4. **Verify:** logged-out view of the post contains a working link to cheapearthquakeinsurance.com.

### Task A5 — Publish the 3 new San Diego posts (45 min each) 🟠

Repo files (in `jumpins.com/content/blog/`):
1. `san-diego-flood-insurance-flood-zones.md`
2. `san-diego-home-insurance-wildfire-neighborhoods.md`
3. `mexico-auto-insurance-san-diego.md`

For **each** post:

1. **Posts → Add New.** Title = the H1 line at the top of the file (without the `#`).
2. **Slug:** set to the `Slug:` value from the file's header block (Document settings → Permalink).
3. **Body:** paste everything between the `---` after the checklist and the `## FAQPage schema` section. Preserve the H2 headings as H2s and keep all internal links.
4. **Author:** Aaron Farmer. **Category:** Insights (same as existing posts).
5. **Byline line:** ensure the theme shows author + date (after A1/A2 this is automatic).
6. **Yoast:** paste the file's `Meta description:` into the meta description field; use the title as SEO title.
7. **FAQ schema:** add a Code module at the bottom of the body, paste the `<script type="application/ld+json">…</script>` block from the end of the file.
8. **Featured image:** pick something appropriate from the Media Library (flood/border/wildfire themed). Set alt text.
9. Publish.
10. **Verify:** logged-out — byline shows Aaron Farmer, one `<h1>`, internal links work, Rich Results Test detects FAQ.

After all three are live: **Yoast should auto-update the sitemap.** Then in **Google Search Console** → URL Inspection → paste each new URL → Request Indexing.

### Task A6 — Confirm noindex on utility pages (15 min) 🟡

For each of these pages, open **Edit → Yoast box → Advanced → "Allow search engines to show this page?" = No**:
`/slide-anything-popup-preview/` · `/agent-entered-commercial-fast-app/` · `/agent-entered-personal-fast-app/` · `/life-simple-form/` · `/life-changes-survey/` · `/commercial-fast-app/` · `/commercial-renewal-fast-app/` · `/personal-insurance/home-insurance/home-quote-form/`

**Verify:** logged-out View Source on 2–3 of them shows `<meta name="robots" content="noindex`.

---

## PART B — cheapearthquakeinsurance.com (WP Admin: cheapearthquakeinsurance.com/wp-admin)

### Task B1 — Add the FAQ section + schema to the homepage (30 min) 🔴

Source: `cheapearthquakeinsurance.com/content/homepage-faq.md`

1. Edit the homepage. Below the "Why use CheapEarthquakeInsurance.com?" section and above "Latest News," add a new section:
   - H2: **Earthquake Insurance Questions, Answered**
   - The 6 questions as **H3** headings, each with its answer paragraph, exactly as in the file.
2. Add a Code/Custom HTML module at the bottom of the page with the FAQPage JSON-LD block from the end of the file.
3. **Verify:** Rich Results Test on the homepage → FAQ detected, no errors.

### Task B2 — Publish the commercial earthquake article (45 min) 🟠

Source: `cheapearthquakeinsurance.com/content/commercial-earthquake-insurance-california.md`
Same procedure as Task A5: title, slug from header, body without the schema section, byline **Aaron Farmer / CA License #0F09648**, Yoast meta description from the header, FAQ schema in a Code module at the bottom. Keep the outbound link to `https://jumpins.com/business-insurance/`.
**Verify:** logged-out — H1 renders, byline + license visible, jumpins.com link works, FAQ passes Rich Results Test.

### Task B3 — E-E-A-T block: name the humans (30 min) 🟠

The site claims "70+ years collective experience" with zero named people.

1. Add an "About the Agency" section (homepage or its own page): name **Aaron Farmer** as principal agent, CA License #0F09648, years in the business, and one line connecting the site to **Jump Insurance Services** (San Diego office) with a link to https://jumpins.com/about-our-agency/.
2. If the site supports the same Google reviews plugin used on jumpins.com, add the reviews widget to the homepage. (Only after real reviews display on-page may AggregateRating schema be added — not before.)
3. **Verify:** logged-out homepage shows the named agent + license.

### Task B4 — Yoast titles/metas sweep (20 min) 🟡

**Yoast SEO → check each published page** has a unique SEO title and meta description (the homepage already has one; residential/commercial/quote pages should each get their own). Pattern: benefit + "California" + CTA, ≤155 characters.

---

## PART C — Not doable from the browser (hand to hosting support)

These require server access — send `jumpins.com/fixes/nginx-snippet.conf` to the hosting admin/support ticket:

1. **HSTS header** (`Strict-Transport-Security`) — currently missing on jumpins.com
2. **`X-Content-Type-Options: nosniff`** — currently missing
3. **`server_tokens off`** — response headers currently expose `nginx/1.31.1`

(The redirect chain is already fixed — single-hop — so only the headers remain.)

---

## Final verification sweep (after everything above)

- [ ] All 6 jumpins.com posts show Aaron Farmer byline + render one `<h1>`
- [ ] 3 new San Diego posts live, indexed request submitted in GSC
- [ ] Earthquake post links to CheapEarthquakeInsurance.com
- [ ] FAQ rich results pass on: earthquake post, 3 new posts, CEI homepage, CEI commercial article
- [ ] CEI homepage names Aaron Farmer + CA License #0F09648
- [ ] Utility pages noindexed
- [ ] Hosting ticket submitted for the 3 headers
