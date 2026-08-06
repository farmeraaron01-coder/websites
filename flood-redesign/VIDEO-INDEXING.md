# Video indexing — the GSC report, and what was actually wrong

Search Console flagged a video indexing failure on the production homepage. Investigating it
found a much larger problem pointing the other way: **the new site had no videos at all**, and
cutover would have dropped the one video Google has successfully indexed.

---

## 1. The reported issue, and a correction to the diagnosis

**Reported:** `https://californiafloodinsurance.com/` — video
`/wp-content/uploads/2026/07/Raindrops-flood-site-720p.mp4` not indexed, reason *"No thumbnail
URL provided."* Last crawled 2 Aug 2026.

The write-up that came with it said the cause was *"the VideoObject structured data on this page
is missing a valid `thumbnailUrl`"* and the fix was to *"locate the VideoObject JSON-LD on the
homepage template and add `thumbnailUrl`."*

**There is no VideoObject on the production homepage.** Verified by parsing every JSON-LD block
on the page — 13 schema types are present (`InsuranceAgency`, `WebPage`, `Person`,
`AggregateRating`, `SiteNavigationElement`, and so on) and `VideoObject` is not among them.
Following that instruction means hunting for markup that does not exist.

**Actual cause.** Google detects `<video>` elements directly, independently of schema. The
production hero video is:

```html
<video preload="none" data-lazy-autoplay="1" loop="loop" playsinline muted width="1920" height="1080">
  <source type="video/mp4" src="…/2026/07/Raindrops-flood-site-720p.mp4" />
</video>
```

No `poster` attribute, and no VideoObject anywhere on the page. Those are the only two places
Google can get a thumbnail from, so there was none — hence the exact error string. Nothing is
misconfigured; a thumbnail was simply never provided.

## 2. Recommendation for the homepage: leave it unindexed

**Do not add VideoObject to the homepage video.** It is a decorative, muted, autoplaying
raindrops loop sitting inside `aria-hidden="true"`. It carries no information anybody would
search for. Marking it up as an indexable video puts a raindrops thumbnail into video search
results where it can only disappoint, and it asserts content value the file does not have.

"Not indexed" is the correct outcome for this video. The Search Console entry is a report of a
fact, not a penalty — video indexing failures do not affect page ranking.

**The new site already removes the cause anyway.** `front-page.php` carries:

```html
<video muted loop playsinline preload="none"
       poster="…/assets/media/hero-poster.jpg"
       data-src="…/assets/media/raindrops-hero.mp4"></video>
```

`hero-poster.jpg` is 1280 × 720, publicly accessible, 200 on staging — far above Google's
160 × 90 minimum. So even if Google detects the video it now has a valid thumbnail, and the
"No thumbnail URL provided" error cannot recur.

It is likely not detected at all. There is no `src` in the HTML; the inline script sets it only
when the viewport is ≥ 721px and the visitor has not asked for reduced motion. Googlebot
smartphone crawls at a mobile viewport, so it sees an empty `<video>` with a poster and nothing
to index. That is the outcome we want, reached without pretending the loop is content.

**Do not "fix" production either.** It is being replaced within weeks, the error is cosmetic,
and editing the live Divi hero for no ranking gain is risk without return.

## 3. The real problem: the new /video/ page was empty

Production `/video/` carries **four** YouTube videos and four complete Rank Math–generated
`VideoObject` nodes, each with a valid `i.ytimg.com` thumbnail:

| YouTube ID | Title |
|---|---|
| `vdslGDfJgIQ` | Private Flood Insurance VS FEMA — **the one GSC reports as indexed** |
| `eigEkEsPljA` | Flood Insurance Carrier Rating |
| `6dMwWQh0ENU` | What is the Mortgage Clause |
| `vAe5wcwwuGY` | How Much Flood Coverage Do I Need |

The new site's `/video/` was **303 rendered bytes** — one intro paragraph and a `[cfi_videos]`
shortcode that output nothing.

The shortcode was not broken. `inc/video.php` implements it correctly: it renders a grid of
posts in the "videos" category, and returns empty for non-admins when that category has none.
The category existed (id 5, "Videos") with **count 0**. The hub was wired and the content behind
it was never created.

So cutover would have shipped a site with no videos, silently dropping the only successfully
indexed video on the domain. This is the kind of gap `preflight.py` looks for; it did not catch
this one because both sites have a `/video/` URL returning 200, and the missing piece was inside
a shortcode's output rather than a broken link.

## 4. What was built

Four posts in the "videos" category, one per video, following the design already documented in
`inc/video.php`: **one video per URL with real supporting text**, because that is what earns a
video result rather than a wall of embeds on one page.

| URL | Video | Words | Meta desc |
|---|---|---|---|
| `/private-flood-insurance-vs-fema/` | `vdslGDfJgIQ` | ~560 | 153 |
| `/flood-insurance-carrier-ratings/` | `eigEkEsPljA` | ~580 | 151 |
| `/flood-insurance-mortgage-clause/` | `6dMwWQh0ENU` | ~560 | 136 |
| `/setting-flood-insurance-coverage-limits/` | `vAe5wcwwuGY` | ~545 | 143 |

Verified after publishing:

- `/video/` renders **4 cards** with all four thumbnails, plus the `i.ytimg.com` preconnect hint.
- Each post emits **exactly one** `VideoObject`, with `name`, `description`, `thumbnailUrl`,
  `uploadDate` all populated — no required field missing.
- All four `maxresdefault.jpg` thumbnails return **200** (86–151 KB). Worth checking explicitly:
  the shortcode points schema at `maxresdefault`, which does not exist for every YouTube video,
  and a 404 there would reproduce the original "no thumbnail" error. The visible `<img>` has an
  `onerror` fallback to `hqdefault`; the schema URL does not, so it has to be right.
- **0 iframes** load before a click — the facade ships one thumbnail instead of ~1 MB of YouTube
  JavaScript per video.
- **0 broken internal links** across the 4 posts and the hub (11 unique targets checked).

Slug note: `/setting-flood-insurance-coverage-limits/` deliberately avoids
`how-much-flood-coverage-do-i-need`, which would compete with the existing
`/how-much-flood-insurance-do-i-need/` page for the same intent. The post links to that page as
the longer written treatment.

## 5. Two things still open

**`uploadDate` is wrong on all four, and it needs Aaron.** The shortcode's `upload` attribute
was left unset, so it falls back to the post date — today. YouTube rate-limited the requests
that would have retrieved the real publish dates. Production's current schema is no better: it
claims `2026-06-25` for all four, which is that page's modified date, not when the videos went
up (the Divi page dates from 2022).

Google uses `uploadDate`. Get the real dates from YouTube Studio and add them:

```
[cfi_video id="vdslGDfJgIQ" title="Private Flood Insurance vs FEMA" upload="2022-03-14" desc="…"]
```

Adding `duration="PT4M12S"` at the same time is worth it — Google uses it for the video result's
runtime badge.

**The indexed video changes pages at cutover.** Google currently associates `vdslGDfJgIQ` with
`/video/`. After cutover that video lives on `/private-flood-insurance-vs-fema/` and `/video/`
becomes a hub that links to it. Expect the existing video result to drop and re-establish on the
new URL over a few weeks. That is the right trade — a dedicated page with supporting text is a
stronger video home than a four-embed page — but it is a temporary dip, not a mistake.

Request indexing for all four new URLs in Search Console at cutover. `/video/` itself keeps the
same URL, so no redirect is needed.
