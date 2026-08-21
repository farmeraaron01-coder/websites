# cheapsoberlivinginsurance.com — live recon before the Kadence build

Captured 21 Aug 2026 by anonymous curl with a cache-busting query string on
every request. This is the **before-state** the playbook's Part 9 contract
requires. Nothing had been changed on the site when this was taken.

---

## Platform

| | |
|---|---|
| Theme | `Divi` + `Divi-child` (264 lines of `et_pb_` markup on the homepage) |
| SEO plugin | **All in One SEO 4.9.10** — *not* Rank Math |
| Canonical host | apex, `https://cheapsoberlivinginsurance.com/` |
| nginx page cache | active, **no bypass rules** — sitemap served `x-proxy-cache: HIT` |

The AIOSEO finding matters more than it looks. Every sitemap, schema, redirect
and meta-description procedure in `CLAUDE.md` and the migration playbook is
written against Rank Math and **does not transfer to this site as written.**

## Host resolution — decision 1 is settled

Every variant lands on the apex in a single hop. No chains.

```
http://cheapsoberlivinginsurance.com/       301 -> https://cheapsoberlivinginsurance.com/
http://www.cheapsoberlivinginsurance.com/   301 -> https://cheapsoberlivinginsurance.com/
https://www.cheapsoberlivinginsurance.com/  301 -> https://cheapsoberlivinginsurance.com/
https://cheapsoberlivinginsurance.com/      200
```

**Build to the apex.** The content package specifies `www` in its canonicals and
`InsuranceAgency` schema; the package is wrong. Moving to `www` would redirect
every URL a second time for no gain.

## URL inventory — the entire indexable site is 9 URLs

| URL | Type | Title | Meta description |
|---|---|---|---|
| `/` | page | Sober Living Home Insurance California \| Cheap Sober Living Insurance | hand-written |
| `/quote-now/` | page | Get a Sober Living Insurance Quote \| … | **none** |
| `/coping-with-challenges-in-sober-living-operations-top-ten-concerns-and-solutions/` | post | matches H1 | auto-fill |
| `/essential-checklist-to-safeguard-your-sober-living-home-from-liability-claims/` | post | matches H1 | auto-fill (`Introduction Liability risks are…`) |
| `/why-professional-liability-insurance-is-crucial-for-operators-of-sober-living-homes/` | post | matches H1 | **none** |
| `/category/resources/` | archive | Resources \| … | none, **no H1** |
| `/tag/sober-living-insurance/` | archive | sober living insurance \| … | none, **no H1** |
| `/tag/sober-insurance/` | archive | sober insurance \| … | none, **no H1** |
| `/tag/halfway-house-insurance/` | archive | halfway house insurance \| … | none, **no H1** |

All nine return 200. All carry `<meta name="robots" content="max-image-preview:large">`
and nothing else — i.e. **all nine are indexable**, including the four empty
archives.

Two things follow:

- **There is almost no SEO metadata to preserve.** Seven of nine URLs have no
  description, and the two that do are AIOSEO auto-fill rather than authored
  copy. An SEO-plugin swap here risks nearly nothing.
- **Four of nine indexable URLs are empty archives.** One category and three
  tags, each with no H1 and no description, on a site with five real pages.
  Noindex them during the rebuild.

## Slug collisions

```
/quote/                       301 -> /quote-now/
/quote-now/                   200
/sober-living-home-insurance/ 404
/get-a-quote/  /contact/  /about/   404
```

`/quote-now/` is the live, indexed, sitemap-listed URL. See DECISIONS below.

## Sitemaps and robots — a landmine for the Rank Math swap

```
/sitemap_index.xml  302 (x-redirect-by: WordPress) -> /sitemap.xml
/sitemap.xml        200, AIOSEO-generated, x-proxy-cache: HIT
```

`robots.txt` advertises `/sitemap.xml` and `/sitemap.rss`, both AIOSEO artifacts.

**Rank Math serves its sitemap at `/sitemap_index.xml` — the exact URL that
currently 302s away.** That redirect is AIOSEO's Yoast-compatibility rule and
should disappear when AIOSEO is deactivated. If it was ever hardcoded into
`.htaccess` instead, it will silently shadow Rank Math's sitemap forever. Check
`.htaccess` before concluding the sitemap is broken.

## Image weight — not a problem on the live site

22 distinct images on the homepage, **1.1 MB total**, largest single file 163 KB.

This is worth stating plainly because playbook Part 0 item 5 flags a 1.89 MB
`og.png` — **that file is in the new content package, not on the live site.**
Do not go looking for it here. The live images are fine; the package's are not.

---

# DECISIONS

Playbook Part 0 listed six decisions gating the build. Recon settles three of
them outright and reframes two. One still needs you.

### 1. www vs apex — SETTLED: apex
Live site already does this correctly in one hop. Build to apex; correct the
package's canonicals and schema.

### 2. `/quote/` collision — RECOMMEND: keep `/quote-now/`
The playbook said to reverse the redirect (`/quote-now/` → `/quote/`). Recon
argues against it. `/quote-now/` is the indexed URL, it is in the sitemap, and
`quote` vs `quote-now` is not a ranking factor. Reversing means deleting the
existing rule and adding its mirror — and if the old rule survives the edit you
get `/quote/ → /quote-now/ → /quote/`, an infinite loop on the site's only
conversion page.

**Build the new quote page at `/quote-now/`. Leave the existing 301 alone.**
Nothing to break, nothing to verify.

### 3. Homepage vs `/sober-living-home-insurance/` — RECOMMEND: do not build it
The conflict is between two pages *in the package*, both of which propose the
H1 "Insurance built for the business of sober living". Live, `/sober-living-home-insurance/`
does not exist and the homepage already owns that exact topic with H1
"Sober Living Home Insurance".

A site with five real pages and no measurable authority should not split its
single money query across two URLs. That is the cannibalization we spent last
week unwinding on Statewide. **Let the homepage be the money page.** Fold the
package's coverage content into it, and drop the separate URL from the build.

### 4. The three blog posts — RECOMMEND: keep and re-template
They are the only topical depth the site has and the only thing feeding
`/category/resources/`. Their URLs stay exactly as they are; only the theme
changes around them. No redirects needed.

Separately: noindex the one category and three tag archives. Four empty
archives against five real pages is a bad ratio.

### 5. Image weight — REFRAMED
Not a live-site problem (1.1 MB, largest 163 KB). It is a **package** problem:
`og.png` 1.89 MB, `recovery-residence-exterior.jpg` 543 KB. Convert to WebP at
upload and get `og.png` under 300 KB. Keep the package's alt text verbatim —
it is written and it is good.

### 6. Identity fields — STILL OPEN, NEEDS YOU
The blueprint leaves the agency licence number, physical address and phone
blank. These feed `InsuranceAgency` schema and cannot be guessed or inferred.
Nothing else in the build is blocked on them, so they can be supplied any time
before schema goes in.
