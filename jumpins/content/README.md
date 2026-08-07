# jumpins.com content

Jump Insurance Services — the general P&C agency site (auto, home, business, life). Separate
from the flood redesign in `../flood-redesign/`; this folder holds article source. Aaron supplied a
jumpins.com application password on 6 Aug, so publishing is possible — **that credential is on the
revocation list in `../flood-redesign/LAUNCH.md` and should go first**, since jumpins is a live
production site with no staging in front of it.

**Site as found, 6 Aug 2026:** WordPress, Yoast SEO, Google Site Kit. 57 pages, 10 posts.
`/insights/` correctly renders the post archive (unlike California's, which had
`page_for_posts: 0`). Service pages are nested — `/personal-insurance/home-insurance/`, not
`/home-insurance/`, which 301s. Link to the nested URL to avoid a redirect hop.

Post cadence: six substantial posts in June–July 2026, then nothing. Newest was 12 July.

## Scope: San Diego only

**Content for this site targets San Diego County and does not promote the Palm Desert office.**
Aaron's instruction, 6 Aug 2026. Do not add Coachella Valley geography, do not link
`/palm-desert-office/`, and do not propose Palm Desert or Coachella Valley topics. An earlier
draft of the FAIR Plan article had a Coachella Valley section and a Palm Desert office link in
the CTA; both were removed. Statewide and county-wide framing is fine — it is the second
location specifically that stays out.

## fair-plan-rate-increase-october-2026.html

**PUBLISHED 6 Aug 2026** at https://jumpins.com/fair-plan-rate-increase-october-2026/ (post 4553,
author Aaron Farmer, category Insights). 1,882 words, 8 H2s, 6 FAQ pairs, 8 internal links (all verified 200
with no redirect hop), 1 cross-domain link to californiafloodinsurance.com.

### Suggested metadata

- **Slug:** `fair-plan-rate-increase-october-2026`
- **Title:** The FAIR Plan's 29% Increase Takes Effect 15 October — What to Do First
- **Meta description** (144 chars): *California approved a 29.1% FAIR Plan rate increase
  effective 15 October 2026. What it means for your renewal, and how to test the market first.*

Note on length: the existing posts' meta descriptions run 199–202 characters, which Google
truncates around 155–160. Worth trimming those six at some point; not urgent.

### Why this topic

The site already covers wildfire, earthquake, non-renewals, San Diego flood zones and Mexico
auto. The FAIR Plan increase is the sequel to the non-renewal post rather than a repeat: it has
a **date-certain deadline**, which is the same structure that makes a call to action work, and
it is squarely in this agency's lane rather than the flood sites'.

It also fixes a link problem. The three June posts carry **zero internal links** — nothing on
the site points into them. This post links to two of them, giving them their first inbound
links from a topically related page.

Deliberately not duplicated from the flood sites: El Niño gets one mention pointing at
California Flood Insurance, and nothing more. Two owned domains ranking for the same query
compete with each other.

### Sources — every figure is dated and attributable

- **CDI approved 29.1%** on the FAIR Plan's dwelling filing, effective **15 October 2026** on
  new and renewal business. The Plan had requested 35.8%. Filing built under the Sustainable
  Insurance Strategy, which permits CDI-approved catastrophe modelling and recovery of the net
  cost of reinsurance.
- **29.1% is a statewide average.** High-exposure homes exceed it, some wildfire premiums
  roughly double, lower-exposure homes see less or a decrease. This is the FAIR Plan's and
  CDI's own framing, and the article leads with it — a reader who thinks 29% is their number
  will disbelieve their renewal notice.
- **Jan 2025 LA wildfires:** ~$4bn in FAIR Plan losses, $1bn assessment on member insurers.
- **Exposure $160bn (2021) → $558bn (2025)**; policy count **+44%** autumn 2024 → end 2025, to
  **668,600+**.
- **Market reopening:** Mercury and CSAA took California's first two SIS rate approvals in
  Dec 2025; Farmers dropped its monthly new-business cap Nov 2025; Travelers announced a
  California homeowners expansion 24 Apr 2026, the first top-ten commitment since the LA fires.
  Still closed: State Farm General (since May 2023), Allstate (since Nov 2022).

A stale figure was avoided: some sources still cite ~350,000 FAIR Plan policies, which is a
2023 number.

### Two things deliberately not claimed

- **No carrier is described as one of ours.** The named carriers appear only as dated market
  facts. I do not know Jump's appointments, and an agency blog implying an appointment it does
  not hold is a real problem. Aaron should add the carriers actually held if he wants that.
- **No premium figures.** Unlike the $450 low-risk flood number, which came from Aaron's own
  book, I have no jumpins premium data. Inventing one here would be the worst kind of error on
  a page whose whole credibility rests on specificity.

### FAQ markup — a bug in the existing posts

Both jumpins posts that carry FAQ schema (`earthquake-insurance-california-2026`,
`san-diego-flood-insurance-flood-zones`) have their Q&As **only inside the JSON-LD, not in
visible page copy** — 3 of 4 and 4 of 5 questions respectively appear nowhere on the rendered
page.

That breaks Google's structured-data policy, which requires marked-up content to be visible to
users. More to the point now that Google retired FAQ rich results on 7 May 2026: the value of
FAQ content today is being quotable by AI Overviews and ChatGPT, and those read rendered text.
Schema-only Q&As are invisible to exactly the thing they are now for.

This post carries the FAQ **both ways** — six visible `<h3>`/`<p>` pairs and JSON-LD mirroring
them word for word. Verified programmatically: 6 of 6 schema questions present in visible copy.

Worth going back and fixing the two existing posts by pasting their schema answers into visible
copy. Cheap, and it is currently wasted content.

## GBP-POST-fair-plan.txt

The Google Business Profile version. **1,494 characters against GBP's 1,500 limit** — the first
draft measured 1,533 despite a stated 1,463, so re-measure rather than trusting the header if
the text is edited.

Deliberately narrower than the article in two ways. **No carrier names**: in 1,800 words with a
disclaimer attached, naming Mercury, CSAA, Farmers and Travelers as dated market facts is
defensible; in 1,500 characters above a quote button it reads as an appointment claim. **No
premium figure**, because there is no Jump premium data available to me — if Aaron supplies one
it would strengthen the post considerably, since a concrete number is what turns a news post
into a phone call.

## fair-plan-gbp-photo.jpg / -alt.jpg

1200 x 900 JPGs for the GBP post, ready to upload. Generated with nano banana (`nano_banana` is
the model ID in the Higgsfield MCP — `nano-banana` with hyphens is rejected), then centre-cropped
to exact 4:3 and saved at quality 88.

The primary shows an inland San Diego County home with dry chaparral hillside behind and
gravel-and-succulent landscaping set back from the walls — a wildland-urban-interface property
that has done the defensible-space work, which is the article's argument in one frame. The
alternate is a flatter street view with no hillside context.

**The media library's three wildfire images are the wrong choice and the post file says so.**
`altadena-wildfire-damage-california.jpg` is a photograph of real destroyed homes, and using it
to sell rate shopping is the kind of thing people notice and resent. The other two are dramatic
flame shots, one of which appears to be a fuel-fire training exercise rather than a wildfire.
Beyond the taste problem they argue the wrong case: this post is about a rate, a deadline and a
way out, and flame imagery says "be afraid" on a profile that is asking for a phone call.
