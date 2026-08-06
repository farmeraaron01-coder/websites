# jumpins.com content

Jump Insurance Services — the general P&C agency site (auto, home, business, life). Separate
from the flood redesign in `../flood-redesign/`; this folder holds article source only, since
I have no credentials for jumpins.com and cannot publish there.

**Site as found, 6 Aug 2026:** WordPress, Yoast SEO, Google Site Kit. 57 pages, 10 posts.
`/insights/` correctly renders the post archive (unlike California's, which had
`page_for_posts: 0`). Service pages are nested — `/personal-insurance/home-insurance/`, not
`/home-insurance/`, which 301s. Link to the nested URL to avoid a redirect hop.

Post cadence: six substantial posts in June–July 2026, then nothing. Newest was 12 July.

## fair-plan-rate-increase-october-2026.html

**Not yet published.** 1,868 words, 8 H2s, 6 FAQ pairs, 9 internal links (all verified 200
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
