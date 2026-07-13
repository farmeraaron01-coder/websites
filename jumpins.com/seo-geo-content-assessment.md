# jumpins.com — SEO / GEO Content Assessment

**Date:** July 13, 2026
**Source data:** June 23, 2026 site crawl (56 pages) + audit findings stored in Dropbox (`/Claude CoWork Files/jumpins.com-audit/`)
**Verdict:** The instinct is correct — the site has volume, but almost none of it is content that can rank or get cited by AI engines. It's generic category copy that every agency site in America already has.

---

## 1. What the content actually is today

| Page | Word count | Problem |
|------|-----------|---------|
| Home Insurance | 9,947 | Generic "what is homeowners insurance" explainer |
| Business Insurance | 9,367 | Generic coverage-type descriptions |
| Auto Insurance | 7,142 | Generic, incl. filler headings ("Other Coverages Might be Available") |
| About | 10,427 | Long but no license numbers, credentials, or proof points |
| Blog | 4 posts | Last published **Feb 2025** — 17 months stale |

The word counts look healthy, but the copy answers questions like "what does auto insurance cover?" — questions NerdWallet, Bankrate, Progressive, and 10,000 other agency sites already answer with more authority. Google has no reason to rank it, and AI engines (ChatGPT, Perplexity, Google AI Overviews) have no reason to cite it. Content Quality scored **52/100**; AI Search Readiness scored **28/100**.

## 2. Why generic content can't win here

Insurance is a YMYL (Your Money / Your Life) category — Google and AI engines weight expertise, authorship, and specificity heavily. The site currently has:

- **No E-E-A-T signals** — no author bylines, no CA insurance license numbers, no agent credentials anywhere
- **No citable specifics** — no California data points, cost figures, carrier comparisons, or first-hand claims/market observations that an AI answer could quote
- **No question-structured content** — AI engines preferentially cite Q&A-formatted pages; only auto/home pages have question H2s, and none carry FAQPage schema
- **Technical blockers that mute whatever content exists:**
  - `Crawl-delay: 30` in robots.txt throttles Googlebot **and** GPTBot/ClaudeBot/PerplexityBot to ~2 pages/min
  - Homepage and all blog posts render **zero H1/H2 in server HTML** (Divi builder issue)
  - No llms.txt, no Article schema, no LocalBusiness/InsuranceAgency schema
  - 13+ pages missing meta descriptions

No amount of new content pays off until the crawl-delay and H1 issues are fixed — they're both < 1 hour of work.

## 3. The unfair advantage nobody is using

Jump has angles that commodity content sites *cannot* replicate. This is what "strong content to rank" means here:

1. **Independent agency, real market access** — side-by-side CEA vs. private earthquake carrier comparisons, admitted vs. surplus lines options. NerdWallet can't quote a live market; Jump can.
2. **California crisis expertise** — non-renewals, FAIR Plan migration, wildfire market exits. Homeowners are desperately searching this and getting national-generic answers.
3. **Flood / surplus lines depth** — flood zone and lender-requirement content specific to San Diego and Riverside counties.
4. **Two physical locations** — San Diego + Palm Desert local pages with local specificity (fire zones, quake faults, desert-specific risks) can own local pack + "near me" AI answers.
5. **First-person agent observations** — "what we're seeing in 2026 renewals" content is unfakeable E-E-A-T and exactly what AI engines quote.

## 4. Fastest win: three strong posts are already written and (as of the June audit) unpublished

Sitting in Dropbox at `jumpins.com-audit/blog-posts/`:

- `earthquake-insurance-california-2026.md` — CEA vs. private carrier comparison, deductible math, who should buy/skip. This is genuinely differentiated content.
- `california-non-renewal-crisis-2026.md`
- `wildfire-home-insurance-california-2026.md`

Publishing these with author byline + CA license number, visible dates, meta descriptions, FAQPage/Article schema, and internal links to quote pages is the single highest-leverage content action available.

## 5. Recommended content program (priority order)

1. **Unblock (Week 1):** remove `Crawl-delay: 30`, fix H1 rendering, deploy the drafted `llms.txt` and meta descriptions (all pre-written in the Dropbox `fixes/` folder).
2. **Publish the 3 drafted posts** with full E-E-A-T dressing (byline, license #, dates, schema).
3. **Restructure the 3 money pages** (auto, home, business) around explicit questions with concise answers directly under each H2, marked up with FAQPage schema. Cut filler sections; add California-specific cost ranges and carrier-access proof points.
4. **Build 4 local landing pages:** `/san-diego/auto-insurance/`, `/san-diego/home-insurance/`, `/palm-desert/home-insurance/`, `/palm-desert/earthquake-insurance/` — 800+ words each of genuinely local content, InsuranceAgency schema.
5. **Pipeline (2 posts/month):** SR-22 California · Mexico auto insurance day trips · FAIR Plan explained · San Diego flood zone maps & lender requirements · condo vs. renters · what a BOP actually covers in California · "what we're seeing in 2026 renewals" (recurring first-person series).

Every piece should follow the same formula: **a question a Californian actually asks + a specific answer with numbers + proof only an independent agent can offer + schema that lets machines quote it.**

---

*Note: this assessment was originally based on the June 23 crawl. On **July 13, 2026** network access was restored and the live site was re-verified — most technical blockers are already fixed (no crawl-delay, homepage H1s + schema live, llms.txt deployed, single-hop redirects) and **the 3 drafted posts were published June 25**. See the LIVE VERIFICATION section in `IMPLEMENTATION-GUIDE.md` for the current punch list: blog author bylines (show "Admin"), blog H1s, FAQPage schema, the CheapEarthquakeInsurance.com cross-link, and hosting security headers. The content-program recommendations in §5 are unchanged and are now the main opportunity.*

## 6. CheapEarthquakeInsurance.com — quick live check (July 13, 2026)

- ~1,200 words on the homepage; clear residential/commercial split, quote CTAs, phone 858-295-7242
- **Good trust signals already**: CA License #0F09648 visible, "A-rated carriers," 20+ years claims
- Clean robots.txt (Yoast default), sitemap present, proper H1 + 9 H2s, 2 JSON-LD blocks
- Weaknesses: thin technical depth (no CEA vs. private comparison, no deductible math — exactly what the jumpins.com earthquake post now has), no reviews on page, no individual author names
- **Strategy stands:** keep unique copy on each domain, cross-link them. The jumpins.com earthquake post should link here for quotes (still missing as of this check), and this site would benefit from its own deeper content — e.g. a CEA vs. private carrier explainer written differently from the jumpins.com post.
