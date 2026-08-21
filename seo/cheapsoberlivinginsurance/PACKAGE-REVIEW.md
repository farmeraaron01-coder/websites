# Review of the Kadence content package

Source: Dropbox → `Claude CoWork Files/01 Websites/cheapsoberlivinginsurance.com/`

| Path | What it is |
|---|---|
| `build/cheapsoberlivinginsurance-kadence-package.zip` | **The production spec.** 3,371,052 b, dated 8 Aug 2026 |
| `build/site/` | Next.js/Cloudflare prototype — the *visual reference*, not the build |
| `build/PROJECT-HANDOFF.md` | Overview, live prototype URL, Cognito form ID |
| `audit/` | June 2026 SEO audit — **stale**, see below |
| `build/research/google-ads-30-day-campaign-baseline-2026-08-04.md` | Ads baseline |

Visual reference: `https://sober-living-insurance.farmeraaron01.chatgpt.site`

**The package is good.** The build guide is specific and correct about the things
that usually go wrong — global palette tokens rather than pasted hex, Kadence
controls before custom CSS, no icon library, WebP with explicit dimensions,
eager hero and lazy everything else, `prefers-reduced-motion`, 44px tap targets,
and a warning not to import Divi layouts or the React prototype. Six named
reusable patterns with CSS classes. Alt text written for every image.

Follow it. The notes below are corrections, not a rewrite.

---

## The site is ten pages, hub-and-spoke

| URL | SEO title | Role |
|---|---|---|
| `/` | Sober Living Home Insurance \| Property & Business Coverage | brand + conversion |
| `/sober-living-home-insurance/` | Sober Living Home Insurance \| Specialized Business Coverage | **pillar** |
| `/commercial-property-business-income/` | Property & Business Income Insurance for Sober Living Homes | spoke |
| `/general-liability/` | General Liability Insurance for Sober Living Homes | spoke |
| `/professional-liability/` | Professional Liability for Sober Living Operators | spoke |
| `/workers-compensation/` | Workers' Compensation for Sober Living Homes | spoke |
| `/who-we-insure/` | Insurance for Recovery Residences & Sober Living Homes | audience |
| `/resources/` | Sober Living Insurance Resources for Operators | hub for the 3 posts |
| `/about/` | About Cheap Sober Living Insurance | trust |
| `/quote/` | Request a Sober Living Insurance Quote | conversion |

Nav groups the four spokes plus the pillar under a **Coverage** dropdown. Every
page has an authored SEO title and meta description. None of these URLs exists
today, so all ten are new — nothing to redirect.

---

## ⚠️ Correction to my earlier recommendation on the pillar page

**I previously said do not build `/sober-living-home-insurance/`** because it
competes with the homepage. **That was wrong, and it was wrong because I argued
it from the playbook's summary instead of reading the package.**

`/sober-living-home-insurance/` is the pillar for four coverage spokes and the
parent of the Coverage nav group. Deleting it orphans the four spokes from their
natural parent — worse than the duplication it avoids.

The conflict is real, though. Both pages target the same query:

| | Homepage | Pillar |
|---|---|---|
| SEO title | Sober Living Home Insurance \| Property & Business Coverage | Sober Living Home Insurance \| Specialized Business Coverage |
| H1 | Insurance built for the business of sober living**.** | Insurance built for the business of sober living |

Near-identical titles, and H1s differing by a full stop.

**Fix the homepage, keep the pillar.** The homepage should sell the agency and
route to the quote; the pillar should own "sober living home insurance" as the
coverage explainer that links down to the spokes. Give the homepage a distinct
H1 and a title that leads on the brand rather than the query. That is a copy
change to one page, made before anything is published.

---

## 🔴 The `/quote/` decision needs an answer I cannot get

The package puts the quote page at `/quote/`. Live, `/quote-now/` is the indexed
URL and `/quote/` 301s to it. I earlier recommended keeping `/quote-now/`.

**There is a live Google Ads campaign on this site.** If its final URLs point at
`/quote-now/`, changing the slug breaks paid landing pages — which costs real
money immediately, unlike any SEO consideration here.

**Check the Ads final URLs before choosing.** Then:

- **Ads point at `/quote-now/`** → build at `/quote-now/`. Change the CTA target
  throughout the build (the blueprint sets `Start a Quote → /quote/` globally on
  line 3, so this is one find-and-replace, done before building, not after).
- **Ads point somewhere else** → either slug is fine. Prefer `/quote/`, and 301
  `/quote-now/` → `/quote/` so the indexed URL is not lost.

Do not build at `/quote/` and leave `/quote-now/` 404ing. It is the only quote
URL Google currently knows.

Note the package already disagrees with itself: `llms.txt` uses `/quote-now/`
while the blueprints use `/quote/`.

---

## Package corrections to make before building

| # | Issue | Fix |
|---|---|---|
| 1 | **`www` canonicals** in 7 files (`layout.tsx`, `robots.ts`, `sitemap.ts`, `home-page.tsx`, `slug-page.tsx`, `PAGE-BLUEPRINTS.md`, `KADENCE-BUILD-GUIDE.md`) | apex — live site already 301s `www` → apex in one hop |
| 2 | **`llms.txt` phone is `855-225-3566`** — the flood brands' number | `858-295-7242` |
| 3 | **`llms.txt` email is `afarmer@californiafloodinsurance.com`** | use a sober-living address, or drop the line |
| 4 | `og.png` is **1.89 MB** | WebP, under 300 KB |
| 5 | `recovery-residence-exterior.jpg` 543 KB, `communal-kitchen.jpg` 359 KB, `operator-planning.jpg` 297 KB | WebP at upload, per the guide's own instruction |
| 6 | Schema block leaves address/licence blank *by design* — "Do not invent these fields" | fill from `IDENTITY.md` |
| 7 | Homepage/pillar title + H1 collision | rewrite the homepage's, above |

The phone is otherwise **correct** throughout — `site-data.ts` and the blueprints
both carry `858-295-7242`. Only `llms.txt` is wrong.

---

## Two notes on the build guide's SEO section

**FAQ schema no longer earns rich results.** Google retired FAQPage rich results
in May 2026. The guide's advice to add it only for visibly rendered FAQs, and to
avoid duplicating it between Kadence and the SEO plugin, is still right — it
remains useful for AI answer extraction. Just do not expect SERP features from
it. The live Divi homepage already emits an `FAQPage` node.

**Verify `Service` schema is available before promising it.** The guide asks for
Service schema on coverage pages "when supported by the SEO plugin". Confirm
whether Rank Math Free exposes it; if it is Pro-gated, the coverage pages simply
go without rather than acquiring a hand-coded second schema source. One source
of structured data — that is the lesson from production's two conflicting
organization nodes.

---

## New plugin dependency

The guide requires **Kadence Blocks** in addition to the Kadence theme. It is not
on the flood sites. Kadence Pro is explicitly *not* required.

---

## The audit in `audit/` is stale — do not action it

Dated June 2026. Its headline finding is "zero schema markup — no
InsuranceAgency, no LocalBusiness, nothing for Google to parse." Untrue as of
21 Aug: the live site emits three JSON-LD blocks. The real problem is the
opposite of the one the audit describes — too many organization entities, not
none. See `IDENTITY.md`.
