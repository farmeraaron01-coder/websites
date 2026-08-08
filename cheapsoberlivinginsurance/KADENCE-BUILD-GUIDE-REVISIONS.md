# Kadence Build Guide — Revisions

**Applies to:** `cheapsoberlivinginsurance-kadence-package/KADENCE-BUILD-GUIDE.md` and
`content/PAGE-BLUEPRINTS.md`, from `cheapsoberlivinginsurance-kadence-package.zip` (7 Aug 2026, 01:12 UTC).

**What this document is.** Codex's package is approved on layout, block structure, copy voice and build
discipline — in particular its rule that the React prototype is a *visual reference* and not something to
import. That stands. This document replaces four sections outright, adds two, and lists a punch list. Where
a section here says REPLACES, use this version and ignore the original. Everything not mentioned is
unchanged and should be followed as written.

**Why anything changes at all:** the palette fails WCAG AA on text that appears on every page; the
canonical host contradicts the live site; two pages share an H1; and the package has no cost content, which
for an exact-match "cheap" domain is the omission that matters most.

---

## A. REPLACES §3 — Kadence global color palette

The original palette fails AA on three tokens. Measured ratios, not estimates:

| Original pair | Ratio | Needed | Where it appears |
|---|---:|---:|---|
| Accent 1 `#C56643` on Base 1 `#FBFAF7` | **3.76** | 4.5 | Eyebrow at 12px/850 — **every page** |
| Accent 1 on Base 2 `#F4F0E8` | **3.45** | 4.5 | Same, alternating sections |
| White on Accent 1 | **3.92** | 4.5 | **Primary button label** |
| Contrast 4 `#9AA6AC` on Base 1 | **2.39** | 4.5 | "Muted interface text" |

12px is not "large text" under WCAG (that is 18.66px bold or 24px normal), so the eyebrow fails. The button
label fails at any size below 18.66px bold, and at weight 800 in a 54px button it will be 16–17px.

**The fix keeps the clay identity.** Codex's own hover color already passes everything, so promote it to
the base and pick a darker hover. Reserve the original `#C56643` for large display type only, where 3.0 is
the threshold and it passes.

Assign in Customizer → Colors & Fonts → Colors. **Always select the palette token inside blocks, never
paste a hex** — that rule from the original guide is important and worth repeating.

| Kadence role | Value | Contrast | Use |
|---|---|---:|---|
| **Accent 1** | **`#A84E31`** | 5.30 on Base 1 · 4.86 on Base 2 · white on it 5.53 | Primary buttons, eyebrow text, links |
| **Accent 2** | **`#8E4026`** | 6.91 on Base 1 | Button and link hover |
| **Accent 3** | `#2E5A51` | 7.46 | Supporting sections, editorial links — unchanged, passes |
| **Accent 4 (display only)** | **`#C56643`** | 3.76 — large text only | Georgia numerals at 48–72px. **Never** for body, links, eyebrows or button labels |
| Contrast 1 | `#0D263C` | 14.80 | Dark hero, headings |
| Contrast 2 | `#152532` | 14.99 | Body text |
| Contrast 3 | `#607079` | 4.92 | Secondary copy, captions |
| **Contrast 4** | **`#66757E`** | **4.56** | Muted text. `#9AA6AC` may remain as a **border** color only |
| Base 1 | `#FBFAF7` | — | Page background |
| Base 2 | `#F4F0E8` | — | Alternating section background |
| Base 3 | `#FFFFFF` | — | Cards, form surface |
| Border | `#D8D4CB` | — | Dividers, card borders |

Dark-background text, both verified: supporting text `#D7E0E5` (11.54 on Contrast 1), light accent
`#E99A72` (6.86). Footer `#B8C5CC` on `#081C2B` is 9.82. All unchanged.

**Update `css/kadence-site.css` to match** — it hardcodes the old values:

```css
:root {
  --sli-navy: #0d263c;
  --sli-paper: #fbfaf7;
  --sli-bone: #f4f0e8;
  --sli-green: #2e5a51;
  --sli-clay: #a84e31;        /* was #c56643 — text/button use, now AA-compliant */
  --sli-clay-display: #c56643; /* large display numerals only */
  --sli-clay-hover: #8e4026;
  --sli-ink: #152532;
  --sli-muted: #66757e;      /* was #607079 in CSS but #9AA6AC in the guide; unify here */
  --sli-line: #d8d4cb;
}
```

and change `.sli-section-number { color: var(--sli-clay-display); }` while `.sli-eyebrow` uses
`var(--sli-clay)`. Those two are the only places the distinction matters.

**Do this before building a single page.** Re-theming after the blocks exist means touching every one of
them, because Kadence writes the chosen palette slot into each block.

---

## B. REPLACES §4 — Typography

Two changes: cap the H1, and use `clamp()` rather than three fixed breakpoint values.

**Why the cap.** The H1 is the LCP element on every page. At 96px, the homepage H1 — *"Insurance built for
the business of sober living."* — runs three to four lines inside a 46% column, pushing both buttons below
the fold on a laptop. 72px keeps the editorial weight and keeps the CTA visible.

**Why `clamp()`.** Three fixed values produce a step-change at each breakpoint. Anything that resizes text
after first paint is a CLS source, and CLS is the one Core Web Vital both flood sites currently hold at 0 —
worth not giving away here.

- Body: Inter, system-ui, sans-serif; **`clamp(17px, 1vw + 14px, 18px)`**; 1.6; weight 400
- Navigation: Inter; 14px; 650–700
- **H1: `clamp(40px, 5.2vw, 72px)`**; 1.03; weight 800; `-0.03em`
- **H2: `clamp(30px, 3.6vw, 52px)`**; 1.08; weight 750–800; `-0.03em`
- H3: Inter; `clamp(21px, 1.6vw, 26px)`; 1.18; weight 750
- Eyebrow: Inter; **13px** (up from 12 — helps the contrast margin and legibility at 850 weight uppercase);
  850; uppercase; `0.16em`; **Accent 1**
- Editorial numerals: Georgia, serif; 48–72px; **Accent 4 display token** or Contrast 1
- Keep important body copy to 55–72 characters per line — unchanged, and a good rule

Host Inter locally. Do not load it from Google Fonts: it is a third-party connection on the critical path,
and the flood sites already ship a self-hosted subset that can be reused.

---

## C. REPLACES §5 — Buttons and links

Primary button:

- Background **Accent 1 `#A84E31`**; white label
- **Label ≥17px at weight 800** — at 16px the contrast math only works because of the new darker accent;
  don't go smaller
- 54px minimum height; 24px horizontal padding; radius 0–2px
- Hover **Accent 2 `#8E4026`** with `translateY(-2px)`
- Visible focus ring, 2px, offset 2px, in Contrast 1 — the original guide asks for visible focus in §12 but
  never specifies it here

Secondary dark-background button: transparent, 1px white border at ~60% opacity, white label, same
dimensions.

Editorial text links: Accent 3 normally, **Accent 1** on hover, weight 800, 1px underline in `currentColor`
at 4px offset.

---

## D. NEW — the cost page. This is the reason the domain exists.

The package has **no cost content on any page**. Not a page, not a section, not a sentence. For an
exact-match domain built to capture "cheap sober living insurance", that is the central gap: a visitor
arriving on a price query finds nothing about price, and leaves.

The house pattern is already established — `cheaplandlordinsurance.com`'s SEO plan names the play
explicitly: *"Price intent | cheap landlord insurance, landlord insurance cost, how much is landlord
insurance | **Exact-match domain + real cost tables**"*, with a dedicated `/landlord-insurance-cost/`
cluster page. Mirror it.

### New page: `/sober-living-insurance-cost/`

**SEO title:** How Much Does Sober Living Home Insurance Cost?
**Meta description:** What sober living home insurance costs, what drives the premium, and how operators
keep it competitive without giving up coverage.
**Hero image:** `operator-planning.jpg`
**Hero eyebrow:** Cost and value
**H1:** What sober living home insurance costs

**Lead:** Operators ask about price first, and that is a fair question. The honest answer is that premium
depends on a handful of specific things about your residence — and that the cheapest quote and the right
coverage are not always the same policy.

**§1 — What actually drives the premium.** A table, not prose. This is the passage AI engines and featured
snippets extract, and it is what makes the page rank for cost queries:

| Factor | Why it moves the premium |
|---|---|
| Number of residents | Occupancy density affects both liability and property exposure |
| Services provided | Structure and recovery support can shift the risk from residential toward professional |
| Staffing | Live-in managers, employees and contractors affect liability and workers' compensation |
| Property value and construction | Replacement cost, age, roof, systems |
| Location | Catastrophe exposure, local claims history, state regulation |
| Claims history | Prior losses, and how they were handled |
| Limits and deductibles | The single biggest lever the operator controls |
| Ownership structure | Whether the property owner and operating entity are the same |

**§2 — Typical ranges.** ⚠ **Aaron or underwriting supplies the figures. Do not invent premium numbers.**
Publishing a fabricated range on an insurance site is both a compliance problem and a credibility problem
the first time a quote lands nowhere near it. Structure to fill in:

```
Small residence, N residents, [coverage set]      $X – $Y annually
Mid-size, N residents, [coverage set]             $X – $Y annually
Larger operation, N+ residents, [coverage set]    $X – $Y annually
```

Each row needs a one-line note on what is included, and the block needs a dated "ranges as of [month
year]" line plus: *"These are illustrative ranges, not quotes. Your premium depends on the factors above."*

**§3 — Competitive without cutting coverage.** This is the reframe, and it is the whole point of the page.
Approximate copy:

> We will work hard on price. What we will not do is win on premium by quietly removing the coverage that
> makes the policy worth having.
>
> The cheapest sober living quote is often cheap because it excludes something — business activity,
> professional services, loss of income, abuse and misconduct. Those exclusions do not show up until a
> claim. We would rather show you where a lower premium is coming from, and let you decide.

**§4 — Where operators genuinely save.** Deductible selection, bundling property with liability, risk
controls and documentation, accurate payroll classification, and being well-prepared for underwriting.
That last one is real: a complete, well-organized submission gets better pricing than a vague one, which
also justifies the Resources content.

**FAQs** — these are cost-intent queries and belong on this page:

- How much does sober living home insurance cost?
- Why are quotes for the same home so different?
- Can I get cheaper coverage with a higher deductible?
- Does the number of residents change the price?
- Is it cheaper to insure the building and the business together?

**Internal linking:** homepage → this page from the price-intent path; this page → each of the five coverage
pages and → `/quote/`. Every coverage page → this page.

### Also add a cost mention on the homepage

One short section, between the Coverage Index and the green distinction section:

- Eyebrow: Straight answer on price
- H2: Competitive pricing, without hollowing out the policy.
- Body: two sentences acknowledging price matters, then the coverage reframe
- Link: *What sober living insurance costs →*

Without this, a visitor who searched a price query has to hunt for the answer.

---

## E. REPLACES §10 — SEO and AIEO implementation

Five corrections and three additions.

**1. Canonical host: apex, no `www`.** The original specifies `https://www.cheapsoberlivinginsurance.com/`.
The live site currently answers on the **apex with no redirect to www**, and both flood sites are apex.
Canonicals pointing at a hostname the site does not serve is the failure mode we spent a day chasing on
statewide. Use:

```
https://cheapsoberlivinginsurance.com/
```

and make sure `www` 301s to apex at the server, in one hop.

**2. Resolve the duplicate H1.** As written, two pages carry the same H1 and near-identical titles:

```
Homepage                        H1: Insurance built for the business of sober living.
/sober-living-home-insurance/   H1: Insurance built for the business of sober living
```

That is cannibalisation — two URLs competing for one head term with the same intent. Pick one owner. The
recommendation:

- **Homepage owns the head term.** H1 stays. Title: `Sober Living Home Insurance | Coverage for Operators`
- **`/sober-living-home-insurance/` takes a different angle** — what the policy actually covers, line by
  line. New H1: **What sober living home insurance covers**. New title:
  `What Sober Living Home Insurance Covers | Policy Breakdown`. New meta description accordingly

If instead you want the coverage page to own the head term, then the homepage becomes a brand/hub page with
its own distinct H1. Either is defensible; having both is not.

**3. FAQPage schema on every page that renders FAQs**, not conditionally. The original hedges with "only
when the SEO plugin is not already outputting the same FAQ schema" — correct instinct, wrong instruction.
Decide once: **the SEO plugin owns all schema, Kadence's block-level FAQ schema stays off.** One owner, no
duplication, no case-by-case judgment during a build.

**4. Definitional passages, 40–60 words, near the top of every coverage page.** House practice from the
landlord plan, and it is what AI Overviews and ChatGPT actually quote. Format: a direct answer to the
page's implied question in one self-contained paragraph that makes sense lifted out of context.

**5. `llms.txt` at the root.** House practice. List the canonical URLs with a one-line description each.

**6. Schema entity — the real values, which the original correctly refused to invent:**

```
legalName   Rebecca Byrom Insurance Agency, Inc.
brand       Cheap Sober Living Insurance
@type       InsuranceAgency
url         https://cheapsoberlivinginsurance.com/
areaServed  United States
```

Still to confirm before launch: phone (see punch list), physical/mailing address, states licensed,
license numbers. **Do not put the Escondido mailing address in schema** — that constraint carries over
from the flood sites.

**7. SEO plugin: Rank Math, not Yoast.** The landlord plan named Yoast; both live flood sites run Rank Math
and every piece of documentation we have — sitemap behavior, robots.txt generation, the category-noindex
control, the sitemap cache and where it hides — is written against Rank Math. Standardise on it. The cost
of one team knowing two plugins' quirks is paid on every future site.

**8. Unchanged and good:** one H1 per page, H2s for topics with H3s beneath, `Service` schema on coverage
pages, `BreadcrumbList` on internal pages, descriptive anchor text, factual claims with no implication that
every coverage is available in every state.

---

## F. Corrections to §9 — Images

**The homepage hero is the lowest-resolution photo in the set.** That is inverted priority — it is the LCP
image on the most important page:

| File | Dimensions | Assigned use |
|---|---:|---|
| `sober-living-community.jpg` | **980×653** | **Homepage hero** ← too small |
| `communal-kitchen.jpg` | 1600×1066 | internal |
| `recovery-residence-exterior.jpg` | 1600×1066 | internal |
| `operator-planning.jpg` | 1600×1066 | internal |
| `sober-living-support.jpg` | 1080×675 | internal |
| `sober-living-home.jpg` | 980×653 | supporting |

In a 54% column of a 1240px container the hero renders about 670 CSS px, so 980px is only 1.46× — visibly
soft on any retina display. **Either re-export it at 1600px or move one of the 1600px images to the
homepage.**

**`og.png` is 1731×909 at 1.85 MB.** Aspect ratio is fine; the weight is roughly six times what it should
be. Re-export **1200×630 under 300 KB**. Some social scrapers time out on large cards and silently fall
back to no image at all.

**`favicon.png` is 170×65 and byte-identical to `logo-original.png`.** It is the wordmark, not an icon.
WordPress needs a **square ≥512×512** for the Site Icon, and a 170×65 wordmark will not crop into one
legibly — this needs designing, not resizing. Until it exists the site will serve a `/favicon.ico` 404,
which costs a Lighthouse Best Practices point via `errors-in-console`; that is measured, not theoretical.

**Explicit `width` and `height` on every image, including inside the hero pattern.** §12 asks for this;
the pattern spec in §8A does not carry it, and `object-fit: cover` with `height: 100%` and no intrinsic
dimensions is a CLS source.

**WebP:** convert and keep originals, as written. `recovery-residence-exterior.jpg` at 531 KB is the one
that most needs it.

---

## G. Corrections to §11 — the Cognito quote form

**Use Cognito's auto-resizing script embed, not the fixed-height iframe.** `height:1200px` leaves dead
space on mobile when the form is shorter and clips it when longer, and `loading="eager"` on a third-party
iframe below the hero makes it compete with the hero image for bandwidth on the page where conversion
matters most.

If the fixed iframe is kept as a fallback, set `loading="lazy"` unless the form is genuinely above the fold.

Keep the disclosure sentence exactly as written — it is good, and the instruction not to submit sensitive
resident information is the right call for this vertical.

**Add a thank-you page.** §12 says to fire Ads conversions on "a confirmed Cognito completion event or
thank-you page rather than a button click alone" — which is precisely correct, and precisely the defect
being unwound on California right now, where a button-click conversion has been counting another brand's
traffic for months. But no thank-you page is specified anywhere. Create `/quote-received/`, set Cognito to
redirect to it on submit, `noindex` it, and fire the conversion there. A redirect target is more reliable
than a JavaScript completion event and it survives form changes.

---

## H. Pages the build assumes but never specifies

| Page | Why |
|---|---|
| `/sober-living-insurance-cost/` | §D above. The EMD payoff page |
| `/privacy-policy/` | The footer links to it. Adapt `CheapLandlordInsurance_Privacy_Policy_2026.docx` |
| `/terms/` | Same. Adapt the landlord ToS — **and note the arbitration question that is still open on the flood ToS applies here too; that is a lawyer's call, not a build decision** |
| `/quote-received/` | Conversion tracking target, `noindex` |
| `/contact/` | Full NAP for entity and local signals, and for trust on a site asking operators to describe their business. `/quote/` alone is not a contact page |

**The six Resources cards describe articles that do not exist.** Six dead ends at launch, or six thin
anchors. They are also the best content opportunity in the package, because those six topics are exactly
the informational queries that feed the coverage pages and the cost page. Either commit to writing them or
cut the grid to the three that will actually ship. Do not launch with placeholder cards.

---

## I. Build order

1. Install Kadence Theme, Kadence Blocks, **Rank Math**
2. **Apply the corrected palette (§A) and typography (§B) first.** Everything downstream inherits them
3. Upload images to the Media Library, after the hero re-export and the `og.png` re-export
4. Set the Site Icon once a square ≥512×512 exists
5. Create the reusable patterns from the original §8
6. Build pages from `PAGE-BLUEPRINTS.md`, with the §E corrections to titles and H1s
7. Build the new cost page (§D) and the four missing pages (§H)
8. Add the corrected `css/kadence-site.css`
9. Configure Rank Math metadata and schema, `llms.txt`, sitemap, robots
10. Wire the Cognito redirect to `/quote-received/` and fire the Ads conversion there
11. Verify: contrast at real sizes, keyboard focus, accordions, the form on mobile, canonicals on apex,
    one H1 per page, no duplicate schema

---

## J. Still to confirm before launch

- **Phone number.** Blueprints use `858-295-7242`; the flood sites use `855-225-3566 x 208`. If the
  separate number is deliberate call tracking, fine — but it determines what Ads call conversions attach
  to, so confirm rather than assume
- **Email.** `aaron.farmer@jumpins.com` on a `cheapsoberlivinginsurance.com` site is an NAP inconsistency
  and a small trust wobble. A brand-domain address would be better
- **Cost ranges** for §D §2 — the one thing in this document that cannot be written without real data
- **Address, states licensed, license numbers** for schema
