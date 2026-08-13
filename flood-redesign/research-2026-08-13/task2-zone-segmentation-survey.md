# Task 2 — Flood Zone Price Segmentation Survey
### How California flood insurance cost pages handle A-zone vs. X-zone pricing

Research method: Google-style SERP queries for California flood insurance cost / rates / by flood zone / Zone X cost, plus broadening queries for carriers, government and calculator pages. Every page below was fetched in this session; all extracted text is archived at `/home/user/workspace/task2_fetches/`. Every dollar figure is quoted verbatim from the fetched page. No figure in this report comes from memory or from a search snippet.

---

## Section 1 — Executive summary

**Total unique URLs fetched: 40.** Two returned no usable content and are excluded from scoring:
- `https://www.insurance.ca.gov/01-consumers/105-type/9-flood/` — **not verified — page returned "Document Not Found"** ("You have reached this page because the document you were looking for was not found or may have been moved within the California Department of Insurance website", [CDI](https://www.insurance.ca.gov/01-consumers/105-type/9-flood/)).
- `https://www.floodsmart.gov/flood-insurance/price` — **not verified — fetch returned empty content** ([FloodSmart price page](https://www.floodsmart.gov/flood-insurance/price)).

**38 pages scored:**

| Verdict | Count |
|---|---|
| **Yes** — segments price by zone with explicit dollar figures per zone | **16** |
| **Partial** — segmentation language / risk-class framing but no dollar figure per zone | **9** |
| **No** — blended state or national average only | **13** |

### Pages that DO segment (Yes)

California-specific:
1. LendingTree — California flood insurance — https://www.lendingtree.com/home-insurance/california-flood-insurance/
2. Policygenius — How much is flood insurance in California — https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/
3. californiafloodinsurance.com — cost page — https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/
4. californiafloodinsurance.com — rates page — https://californiafloodinsurance.com/flood-insurance-rates/
5. californiafloodinsurance.com — California FAQs — https://californiafloodinsurance.com/faqs/
6. Insuranceopedia — Flood insurance California — https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california
7. FludZone — California flood zones — https://www.fludzone.com/flood-zones/california
8. Katz Insured — California flood insurance cost guide — https://www.katzinsured.com/california-flood-insurance-cost-guide
9. Express Financial — Flood insurance California — https://expressfinancial.net/p/flood-insurance-california
10. Coverforge — California flood — https://coverforgeusa.com/states/california/flood
11. StateCalc — California flood insurance calculator — https://statecalc.com/flood-insurance/california-flood-insurance-calculator/
12. Fluvenar / SmartTechInvest — Zone AE flood insurance in California's 2026 insurance crisis — https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium

National pages that rank for these queries and carry a California row or California example:
13. FludZone — Flood insurance cost guide — https://www.fludzone.com/guides/flood-insurance-cost
14. LendingTree — Flood insurance cost — https://www.lendingtree.com/home-insurance/flood-insurance-cost/
15. NerdWallet — Flood insurance cost — https://www.nerdwallet.com/insurance/homeowners/learn/flood-insurance-cost
16. HowMuchIsHomeInsurance — Flood insurance cost — https://howmuchishomeinsurance.com/flood-insurance-cost

### Overall verdict

**Zone-level pricing is not rare — but doing it *completely* is.** Roughly 42% of the pages examined (16 of 38) publish at least one dollar figure tied to a named zone or risk class, so the raw practice of splitting price by zone is now common among aggregators and independent-agency pages.

What is genuinely rare is the full trio a voluntary X-zone buyer needs on one page: **(1) per-zone dollar figures, (2) a way to find out which zone you are in, and (3) an explicit statement that coverage is mandatory in an SFHA with a federally backed mortgage and optional everywhere else.** Only **four** pages of 38 deliver all three — FludZone's California page, StateCalc's California calculator, californiafloodinsurance.com's FAQ page, and the Fluvenar/SmartTechInvest Zone AE article. Notably, **every large mainstream brand except LendingTree fails at least one leg**: Insurify, Insurance.com, FloodPrice, InsuredBetter, Kin, Out of the Storm News and Policygenius's California overview all publish only a blended California average, and Policygenius's cost page publishes a clean zone table with **no** mandatory-vs-optional explanation at all.

The specific trap in the brief is real and widespread: 13 of 38 pages show a single blended California number (ranging from "$779" to "$1,240.27" across sources) with no zone split, which is roughly double the X-zone figures the segmenting pages publish ("$400 – $900", "as low as ~$350 per year", "$400–$700").

Also worth flagging: **no carrier page found segments by zone.** Neptune's own cost article gives one blended national figure and a single starting price, and FEMA's own single-family cost page explicitly refuses to price by zone ("The previous methodology set rates based on geographic zones and elevation", [FEMA](https://www.fema.gov/flood-insurance/work-with-nfip/risk-rating/single-family-home)). That leaves an open competitive gap for an agency page that does it properly.

---

## Section 2 — Pages that segment by zone (detailed)

### 2.1 LendingTree — California flood insurance — **YES**
https://www.lendingtree.com/home-insurance/california-flood-insurance/

- **How it segments:** by zone letter. Section headings: **"California flood insurance costs by zone"** and **"Flood insurance rates by zone"** ([LendingTree CA](https://www.lendingtree.com/home-insurance/california-flood-insurance/)).
- **Figures per segment (monthly):** Zone A **$89**; Zone A99 **$53**; Zone AH **$90**; Zone AO **$78**; Zone VE **$111**; "B, C and X" **$66**. Headline: "FEMA flood insurance costs $111 a month in California's most expensive flood zone." ([LendingTree CA](https://www.lendingtree.com/home-insurance/california-flood-insurance/))
- **Zone-lookup help:** (c)/(a-partial) — link text **"Flood Map Service Center"**; no `msc.fema.gov` URL surfaced in the fetched content.
- **Mandatory vs optional: Yes.** Under **"Is flood insurance required in California?"** (middle of page): "Flood insurance is only required for mortgages in high-risk flood zones." and "No one can make you get flood insurance when you buy your home with cash or pay off your mortgage." ([LendingTree CA](https://www.lendingtree.com/home-insurance/california-flood-insurance/))
- **Genuinely useful:** the voluntary-buyer nudge — "According to FEMA, 32% of flood insurance claims are from low- and moderate-risk flood zones." ([LendingTree CA](https://www.lendingtree.com/home-insurance/california-flood-insurance/))

### 2.2 Policygenius — How much is flood insurance in California — **YES**
https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/

- **How it segments:** high-risk vs low-risk grouped by zone letter. Heading: **"Flood insurance rates by flood zone in California"** ([Policygenius](https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/)).
- **Figures per segment (annual):** High risk (A or V) **$1,161**; Moderate to low risk (B, C, or X) **$622**; Undetermined risk (D) **$1,121** ([Policygenius](https://www.policygenius.com/homeowners-insurance/how-much-is-flood-insurance-in-california/)).
- **Zone-lookup help:** (d) nothing found in fetched content.
- **Mandatory vs optional: No** — no mandatory/optional explanation located on this page.
- **Genuinely useful:** the ~$539/yr spread between high-risk and low-risk California figures is the cleanest single comparison found on a mainstream brand — but with no mandate context, an X-zone reader is left without the "you don't have to buy this" framing.

### 2.3 californiafloodinsurance.com — How much does flood insurance cost — **YES**
https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/

- **How it segments:** risk band plus zone letters.
- **Figures per segment:** "Low-to-moderate risk (Zone X): often **$400–$700/year**"; "Moderate risk near water or storm drains: roughly **$700–$1,500/year**"; "High-risk zones (Zone A/AE/V): commonly **$1,500–$3,000+/year**"; overall typical "**$500 to $2,000 per year**" ([californiafloodinsurance.com](https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/)).
- **Honesty note:** "These are ranges, not quotes." ([californiafloodinsurance.com](https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/))
- **Zone-lookup help:** (d) nothing in fetched content.
- **Mandatory vs optional: Vague** — only "may not be lender-required." ([californiafloodinsurance.com](https://californiafloodinsurance.com/how-much-does-flood-insurance-cost/))

### 2.4 californiafloodinsurance.com — Flood insurance rates — **YES**
https://californiafloodinsurance.com/flood-insurance-rates/

- **How it segments:** H2 **"How does flood zone change your rate?"** ([californiafloodinsurance.com rates](https://californiafloodinsurance.com/flood-insurance-rates/)).
- **Figures per segment:** "Low-risk Zone X: private flood rates can start as low as **~$350 per year**."; "California overall average: about **$780 per year**."; "High-risk zones (A, AE, AH, AO, V, VE): typically more than the ~$780 average" ([californiafloodinsurance.com rates](https://californiafloodinsurance.com/flood-insurance-rates/)).
- **Zone-lookup help:** (d) none on this page.
- **Mandatory vs optional:** not stated on this page in the fetched content.
- **Genuinely useful:** it is the only page found that pairs a private-market X-zone entry price with the statewide average, which is exactly the "you'd pay half" comparison the brief describes.

### 2.5 californiafloodinsurance.com — California FAQs — **YES** (strong)
https://californiafloodinsurance.com/faqs/

- **How it segments:** zone letter and property type, in a table under the heading **"How much does flood insurance cost in California?"** ([California FAQs](https://californiafloodinsurance.com/faqs/)).
- **Figures per segment:**
  - "**Zone X — standard residential**" — "**$400 – $900**" — note "Often 40–60% below NFIP equivalent"
  - "**Zone AE — standard residential**" — "**$1,200 – $3,000+**" — "Varies significantly with elevation data and state"
  - "**Zone AE — elevated on pilings**" — "**$600 – $1,400**" — "Elevation above base flood reduces premium sharply"
  - "**Coastal / Zone VE**" — "**$3,000 – $8,000+**" — "Wave action risk; high-value properties higher" ([California FAQs](https://californiafloodinsurance.com/faqs/))
  - Deductible worked example, "Example: Zone AE residential, $250K building coverage": "~$1,850/yr baseline" at $1,000 deductible; "~$1,600/yr" ("saves ~$250/yr") at $2,500; "~$1,380/yr" ("saves ~$470/yr") at $5,000; "~$1,100/yr" ("saves ~$750/yr") at $10,000 ([California FAQs](https://californiafloodinsurance.com/faqs/)).
- **Zone-lookup help:** (a)+(b) — "Enter your address at **FEMA's Flood Map Service Center (msc.fema.gov)**, or use our flood zone map lookup." Link/tool text: "FEMA's Flood Map Service Center (msc.fema.gov)" and "flood zone map lookup"; also "If you're unsure of your zone, check **msc.fema.gov** or ask us — we look this up as part of every quote." ([California FAQs](https://californiafloodinsurance.com/faqs/))
- **Mandatory vs optional: Yes**, in the FAQ body under **"Is flood insurance required by my mortgage lender?"** → sub-heading **"Which zones trigger the requirement"**: "Zones AE, AH, AO, AR, and VE are all Special Flood Hazard Areas. Zone X (minimal or moderate flood hazard) does *not* trigger a mandatory purchase requirement." Plus the heading **"No mortgage? No legal requirement."** and "There is no discretion for either you or your lender: the Flood Disaster Protection Act mandates it." ([California FAQs](https://californiafloodinsurance.com/faqs/))
- **Genuinely useful:** "But consider this: FEMA data consistently shows that 25–30% of all flood insurance claims are filed by properties outside high-risk zones." ([California FAQs](https://californiafloodinsurance.com/faqs/))

### 2.6 Insuranceopedia — Flood insurance California — **YES**
https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california

- **How it segments:** risk band with zone letters. Heading: **"Average Costs by Flood Zone"** ([Insuranceopedia](https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california)).
- **Figures per segment:** High Risk (AE, VE) **$1,000–$2,000/yr**; Moderate Risk (B, X) **$500–$1,000/yr**; Low Risk (C, X) **$450–$650/yr** ([Insuranceopedia](https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california)).
- **Zone-lookup help:** (d) none in fetched content.
- **Mandatory vs optional: Yes** — "California law does not require homeowners to have a flood insurance policy. However, if your property is located in a high-risk flood zone and you have a federally-backed mortgage, you are required to buy flood insurance." ([Insuranceopedia](https://www.insuranceopedia.com/homeowners-insurance/flood-insurance-california))

### 2.7 FludZone — California flood zones — **YES** (best in class)
https://www.fludzone.com/flood-zones/california

- **How it segments:** zone letter, using OpenFEMA policy data. Section: **"Policies by Flood Zone"** ([FludZone CA](https://www.fludzone.com/flood-zones/california)).
- **Figures per segment:** Zone X 69,510 policies (avg. **$812/yr**); Zone A 55,133 (**$759/yr**); Zone AE 46,651 (**$1,334/yr**); Zone AO 23,882 (**$954/yr**); Zone AH 8,269 (**$1,117/yr**); Zone VE 2,942 (**$1,337/yr**); Zone D 843 (**$1,230/yr**); Zone AOB 383 (**$447/yr**); state average **$952** across 207,675 policies ([FludZone CA](https://www.fludzone.com/flood-zones/california)).
- **Zone-lookup help:** (a) embedded address tool — heading "**Look Up Any California Address**", body "Enter your CA address in FludZone's free lookup tool. We query FEMA's National Flood Hazard Layer in real-time" ([FludZone CA](https://www.fludzone.com/flood-zones/california)).
- **Mandatory vs optional: Yes**, in the FAQ (bottom): "Properties in Zone X are not subject to the federal mandate but lenders may still require coverage" ([FludZone CA](https://www.fludzone.com/flood-zones/california)).
- **Genuinely useful:** the figures are actual in-force policy averages rather than editorial estimates, and the Zone A ($759) vs Zone AE ($1,334) split shows something most pages miss — that "A-zone" is not one price.

### 2.8 Katz Insured — California flood insurance cost guide — **YES**
https://www.katzinsured.com/california-flood-insurance-cost-guide

- **How it segments:** heading **"Typical NFIP premium ranges in California"** ([Katz Insured](https://www.katzinsured.com/california-flood-insurance-cost-guide)).
- **Figures per segment:** "Low-risk Zone X properties: Roughly **$500 to $900 per year**"; "Moderate-risk AE zone properties: Often **$1,000 to $2,500 per year**"; "High-risk or significantly below BFE: Premiums can reach **$3,000 to $6,000+ per year**" ([Katz Insured](https://www.katzinsured.com/california-flood-insurance-cost-guide)).
- **Honesty note:** "Under Risk Rating 2.0, FEMA no longer publishes a single rate table by zone, so exact quotes require running your specific address." ([Katz Insured](https://www.katzinsured.com/california-flood-insurance-cost-guide))
- **Zone-lookup help:** (d) no tool or msc.fema.gov link found.
- **Mandatory vs optional: Yes** — "If your federally backed mortgage is on a property in a FEMA-designated SFHA, flood insurance is not optional. It is a loan condition." ([Katz Insured](https://www.katzinsured.com/california-flood-insurance-cost-guide))

### 2.9 Express Financial — Flood insurance California — **YES**
https://expressfinancial.net/p/flood-insurance-california

- **How it segments:** heading **"What it costs by risk profile"** ([Express Financial](https://expressfinancial.net/p/flood-insurance-california)).
- **Figures per segment:** Low-risk (Zone X) "**~$350/year**" private; Moderate-risk (AE zone) "**$1,000–$2,500/year**"; High-risk / below BFE "**$3,000–$6,000+**" per year ([Express Financial](https://expressfinancial.net/p/flood-insurance-california)).
- **Zone-lookup help:** (d) none found.
- **Mandatory vs optional: No** — the fetched content never uses the words "mandatory" or "optional."

### 2.10 Coverforge — California flood — **YES**
https://coverforgeusa.com/states/california/flood

- **How it segments:** zone letter plus geography, and by policy form (Preferred Risk Policy vs standard).
- **Figures per segment:** "Zone X properties in lower-risk areas can qualify for Preferred Risk Policies starting around **$400–$600**."; "Bay Area properties in 100-year flood zones typically pay **$900–$1,800**."; "High-risk properties in the Sacramento-San Joaquin Delta or Central Valley floodplains may pay **$1,500–$3,000+ annually**."; state average "**$840 per year**"; "A 'Preferred Risk Policy' for moderate-/low-risk areas often costs only **$400–$700/year**" ([Coverforge](https://coverforgeusa.com/states/california/flood)).
- **Zone-lookup help:** (d) none found in fetched content.
- **Mandatory vs optional: Yes** — "Flood insurance is required for federally backed mortgages on properties in FEMA SFHAs throughout California" ([Coverforge](https://coverforgeusa.com/states/california/flood)).
- **Genuinely useful:** the only page found that ties zone pricing to named California geographies (Delta/Central Valley vs Bay Area).

### 2.11 StateCalc — California flood insurance calculator — **YES** (best in class)
https://statecalc.com/flood-insurance/california-flood-insurance-calculator/

- **How it segments:** interactive zone selector — "Moderate/Low Risk (Zone X/B/C)", "High Risk / Special Flood Hazard Area (Zone A)", "Coastal High-Hazard (Zone V)" — applied as multipliers **0.84x / 1.14x / 1.27x** ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/)).
- **Figures per segment:** worked example "**$833** in a low-risk zone (**$69/month**), versus **$1,105** in a high-risk zone" ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/)).
- **Zone-lookup help:** (b) — the only page in the survey that prints the FEMA URL: "California's FIRM maps are available free at FEMA's Flood Map Service Center (msc.fema.gov)." ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/))
- **Mandatory vs optional: Yes**, in the FAQ (bottom): "If your property is in a Special Flood Hazard Area (Zone A or V ...) and you have a federally-backed mortgage, flood insurance is legally required. Outside those zones, it's optional but often still worthwhile" ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/)).
- **Genuinely useful:** the calculator lets the X-zone visitor *self-select* into the cheaper number instead of reading a blended average — the single most directly transferable pattern for a rebuild.

### 2.12 Fluvenar / SmartTechInvest — Zone AE flood insurance in California's 2026 insurance crisis — **YES** (best in class for mandate framing)
https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium

- **How it segments:** a five-row zone table with a mandate column, under the heading **"Zone AE vs Zone X: What FEMA's Flood Map Is Actually Telling You"** ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium)).
- **Figures per segment (typical annual premium):** Zone VE "**$6,500–$9,000+**" (mandate: "Yes — federally backed loans"); Zone AE "**$3,200–$5,500**" ("Yes"); Zone AO/AH "**$2,500–$4,000**" ("Yes"); Zone X (shaded) "**$700–$1,200**" ("No — but recommended"); Zone X (unshaded) "**$500–$800**" ("No") ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium)).
- Worked California example: "For a $550,000 replacement cost home in Zone AE, sitting 1 foot above BFE in a Northern California river corridor: approximately **$4,200/year for building coverage** (up to NFIP's $250,000 structural cap) plus **$400/year for contents coverage** — totaling **$4,600/year in mandatory NFIP premiums**." and "The equivalent Zone X property typically pays **$700–$900/year on an optional basis**." with "That $3,700/year gap doesn't appear anywhere in the listing." ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium))
- **Zone-lookup help:** (b)+(a) — "When you look up a property on FEMA's Flood Map Service Center at msc.fema.gov, you'll see one of several zone designations."; "A FEMA flood zone lookup takes 5 minutes at msc.fema.gov."; plus a proprietary address tool: "This is the kind of zone-by-zone premium breakdown that Fluvenar runs automatically for any address" ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium)).
- **Mandatory vs optional: Yes**, stated at the very top: "If you're using a federally backed mortgage, that premium isn't optional. It's a line item your lender will require before you can close." ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium))
- **Caveat:** premium ranges run far above every other source in this survey (Zone AE $3,200–$5,500 vs FludZone's measured $1,334 average) and are not attributed to a data source in the fetched content. Treat as directional, not as a benchmark.

### 2.13 FludZone — Flood insurance cost guide (national, with CA rows) — **YES**
https://www.fludzone.com/guides/flood-insurance-cost

- **How it segments:** heading **"Average Costs by Flood Zone"** with a "Required?" column ([FludZone guide](https://www.fludzone.com/guides/flood-insurance-cost)).
- **Figures per segment:** Zone X **$400–$700** (Required? No); Zone A **$1,200–$3,500+** (Yes); Zone AE **$1,500–$3,000** (Yes); Zone VE **$3,000–$10,000+** (Yes). A second table, "Zone AE Premiums by State," lists California AE **$1,334** and X **$812** ([FludZone guide](https://www.fludzone.com/guides/flood-insurance-cost)).
- **Genuinely useful:** the "Required?" column adjacent to the price is the clearest single-glance mandate/price pairing found anywhere in the survey.

### 2.14 LendingTree — Flood insurance cost (national) — **YES**
https://www.lendingtree.com/home-insurance/flood-insurance-cost/

- **How it segments:** heading **"Cost of flood insurance by flood zone"**, annual figures: A **$1,147**; A99 **$1,128**; AE **$1,094**; AH **$1,112**; AO **$907**; AR **$813**; D **$1,253**; EMG **$535**; V **$1,718**; VE **$1,038**; X **$760**; California state row **$1,079** ([LendingTree](https://www.lendingtree.com/home-insurance/flood-insurance-cost/)).
- Not California-specific; the X ($760) vs V ($1,718) spread is the widest zone gap documented in the survey.

### 2.15 NerdWallet — Flood insurance cost (national) — **YES**
https://www.nerdwallet.com/insurance/homeowners/learn/flood-insurance-cost

- **How it segments:** heading **"Flood insurance cost by flood zone"** — High risk (A or V) **$1,114/yr ($93/mo)**; Low or moderate risk (all other zones) **$745/yr ($62/mo)**; California row **$1,015** ([NerdWallet](https://www.nerdwallet.com/insurance/homeowners/learn/flood-insurance-cost)).
- **Mandatory vs optional: No** dedicated explanation found on this page. Not California-specific.

### 2.16 HowMuchIsHomeInsurance — Flood insurance cost (national) — **YES**
https://howmuchishomeinsurance.com/flood-insurance-cost

- **How it segments:** two tables — **"NFIP 2026 pricing snapshot"** and **"Flood zones and what they mean"** (with a "Mortgage requirement" column) ([HowMuchIsHomeInsurance](https://howmuchishomeinsurance.com/flood-insurance-cost)).
- **Figures per segment:** "A / AE ... Required on federally-backed ... **$800 - $1,600**"; "V / VE ... Required on federally-backed ... **$2,800+**"; "AH / AO ... Required on federally-backed ... **$600 - $1,200**"; "X (shaded) ... Not required ... **$500 - $900**"; "X (unshaded) ... Not required ... **$400 - $700**"; "D ... Lender discretion ... **$600 - $1,200**" ([HowMuchIsHomeInsurance](https://howmuchishomeinsurance.com/flood-insurance-cost)).
- **Mandatory vs optional: Yes**, in the FAQ: "Legally required if you have a federally-backed mortgage (conforming, FHA, VA) on a property in a FEMA-designated Special Flood Hazard Area (Zone A, AE, V, or VE on the current FIRM)." and "Not legally required in Zone X or higher." plus "However, about 25 per cent of NFIP claims come from properties outside high-risk zones, per FEMA - so 'not required' does not mean 'not at risk.'" ([HowMuchIsHomeInsurance](https://howmuchishomeinsurance.com/flood-insurance-cost))
- **Zone-lookup help:** (d) "No `msc.fema.gov` link or text appears on the page." Not California-specific.
- **Genuinely useful:** the only page found that splits **shaded vs unshaded X** *and* prices them differently ($500–$900 vs $400–$700) — directly relevant to the X500 visitor problem.

### Partial pages (segmentation language, no dollar figure per zone)

**P1. ValuePenguin — California flood insurance** — https://www.valuepenguin.com/flood-insurance/california — state average **$811** plus a city table only; no zone prices. Best-in-survey mandate wording though, under **"Do you need flood insurance in California?"**: "Flood insurance isn't required for homeowners in California, but it's typically mandated by mortgage lenders if your house is in a high-risk flood zone." and "If your home is in an area labeled Zone B, X or C ... you generally won't be required to purchase flood insurance." ([ValuePenguin CA](https://www.valuepenguin.com/flood-insurance/california))

**P2. ValuePenguin — Flood zones & how they affect insurance** (national) — https://www.valuepenguin.com/flood-insurance/flood-zones-affect-insurance-premiums — a zone table with an insurance-requirement column ("V, VE, V1-V30 — Yes"; "AO, AH, A, AE, AR, A1-30, A99 — Yes"; "D — No"; "B, C and X — No") but **no per-zone dollars, by design**: "Although having a home in a flood zone starting with an A or V means you must buy flood insurance, the zones are no longer used to calculate rates." Instead it prints a two-property Risk Rating 2.0 comparison including a California home at "$4.42 per $1,000 of coverage for the building", "$2,365 per year", "$197" monthly. X-zone mandate line: "For homeowners in flood zone X, the law doesn't require you to purchase a flood policy, but your mortgage company might." ([ValuePenguin zones](https://www.valuepenguin.com/flood-insurance/flood-zones-affect-insurance-premiums))

**P3. californiafloodinsurance.com — Navigating flood zone X** — https://californiafloodinsurance.com/navigating-flood-zone-x/ — single-zone page, no comparison table: "Zone X is the least expensive flood zone to insure — often just a few hundred dollars a year." and "You are not federally required to buy it, but you should strongly consider it" ([Zone X page](https://californiafloodinsurance.com/navigating-flood-zone-x/)). Strongest shaded-vs-unshaded X explanation found.

**P4. californiafloodinsurance.com — Flood Zone AE** — https://californiafloodinsurance.com/flood-zone-ae/ — segments by zone narratively but gives only the statewide benchmark: premiums "generally run **higher than California's statewide average of about $780 per year** for $250,000 of building coverage" and "Lower-risk Zone X properties can start far below that; high-risk zones do not." Mandate is explicit — the requirement applies to "every high-risk SFHA ... including AE, A, AH and AO, and the coastal V and VE zones" ([Zone AE page](https://californiafloodinsurance.com/flood-zone-ae/)).

**P5. californiafloodinsurance.com — Flood Zone A** — https://californiafloodinsurance.com/flood-zone-a/ — same pattern: "Premiums are **typically higher than the California statewide average of about $780 per year for $250,000 of building coverage**." / "Actual rates vary by home, and a quote is required — there is no flat price for Zone A." / "By comparison, low-risk Zone X properties can start much lower." Mandate under **"Do you need flood insurance in Flood Zone A?"**: "Because Zone A is a high-risk SFHA, flood insurance is federally mandatory if you have a mortgage from a federally regulated or insured lender." ([Zone A page](https://californiafloodinsurance.com/flood-zone-a/))

**P6. Sacramento County Water Resources — Flood insurance rate examples** — https://waterresources.saccounty.gov/stormready/Pages/Flood-Insurance-Rate-Examples.aspx — segments by policy form rather than zone: Preferred Risk Policy from "**$129**" to "**$405**", and "a standard-rated Flood Zone X policy can range to a yearly high of **$1,717**" ([Sacramento County](https://waterresources.saccounty.gov/stormready/Pages/Flood-Insurance-Rate-Examples.aspx)). No mandatory/optional section.

**P7. californiafloodinsurance.org — FAQs** — https://www.californiafloodinsurance.org/faqs/ — Preferred Risk Policy "a few hundred dollars a year"; "The average flood insurance premium in California is under $700 a year."; instant estimate offered only "if the property is in flood zones B, C, or X" ([californiafloodinsurance.org](https://www.californiafloodinsurance.org/faqs/)). Contains stray Florida text — a quality tell.

**P8. FEMA — Low Risk Flood Zones? (FAQ)** — https://www.fema.gov/faq/low-risk-flood-zones — prices only the low-risk side: "You may qualify for the Preferred Risk Policy (a lower-cost flood insurance policy) that provides contents coverage beginning at **$39 per year** and building plus contents coverage beginning at **$119 a year**." with "About 25 percent of all flood insurance claims come from areas with low-to-moderate flood risk." ([FEMA FAQ](https://www.fema.gov/faq/low-risk-flood-zones)) No high-risk comparison figure, so no true segmentation.

**P9. FEMA — Facts and myths about flood insurance** — https://www.fema.gov/blog/facts-and-myths-about-flood-insurance — one low-risk figure only: "**MYTH: It doesn't make sense to pay for flood insurance if you are in a low-risk flood zone.**" / "The NFIP's Preferred Risk Policy is very affordable. A premium for a primary residence may cost about **$467 a year** for $200,000 of coverage for a home structure and $80,000 for contents. That is less than $40 a month." ([FEMA blog](https://www.fema.gov/blog/facts-and-myths-about-flood-insurance))

---

## Section 3 — Pages that DON'T segment (brief)

| # | URL | What they show instead |
|---|---|---|
| 1 | https://insurify.com/homeowners-insurance/california-flood-insurance/ | Blended "$779" California average plus a county table; its flood-zone table prices **home** insurance ($100 vs $167), not flood ([Insurify](https://insurify.com/homeowners-insurance/california-flood-insurance/)). |
| 2 | https://outofthestormnews.com/flood-insurance/costs/california | "$1,104" California average and a county table only; no mandate explanation and no zone lookup ([Out of the Storm News](https://outofthestormnews.com/flood-insurance/costs/california)). |
| 3 | https://www.floodprice.com/california-flood-insurance | "$1,240.27" average plus a city table; does offer "Use our FEMA Flood Zone Lookup tool" but never prices by zone ([FloodPrice](https://www.floodprice.com/california-flood-insurance)). |
| 4 | https://www.insuredbetter.com/l/california/flood-insurance/ | Single "$938/yr" figure; no zone figures at all ([InsuredBetter](https://www.insuredbetter.com/l/california/flood-insurance/)). |
| 5 | https://www.insurance.com/home-and-renters-insurance/flood-insurance/flood-insurance-in-california | "$940/yr" blended; mandate line only — "Flood insurance is not required by law in California. However, lenders can require you to obtain flood insurance." ([Insurance.com](https://www.insurance.com/home-and-renters-insurance/flood-insurance/flood-insurance-in-california)). |
| 6 | https://www.kin.com/blog/california-flood-insurance/ | Median "$779"; strong mandate wording ("flood insurance is only legally required if you have a federally backed mortgage ... and your property is located in a Special Flood Hazard Area (SFHA) ... SFHAs include Zones A, AE, and V") and step 1 "Use FEMA's Flood Map Service Center" — but no price per zone ([Kin](https://www.kin.com/blog/california-flood-insurance/)). |
| 7 | https://www.policygenius.com/homeowners-insurance/flood-insurance-california/ | California overview with no costs by zone; only "Just 4% of California homes are located in a high-risk flood zone" ([Policygenius CA](https://www.policygenius.com/homeowners-insurance/flood-insurance-california/)). |
| 8 | https://neptuneflood.com/blog/how-much-does-flood-insurance-cost/ | Carrier page, national: "flood insurance costs per month around $82", "$985 per year", "Neptune's residential flood coverage starts as low as $350 per year." — no zone figures and no mandate/lender explanation ([Neptune](https://neptuneflood.com/blog/how-much-does-flood-insurance-cost/)). |
| 9 | https://www.fema.gov/flood-insurance/work-with-nfip/risk-rating/single-family-home | Price-range buckets only ("37% of policies nationwide fall into the $0-1,000 range", "32% cost between $1,000 and $2,000 per year"); explicitly no zone pricing — "The previous methodology set rates based on geographic zones and elevation." ([FEMA](https://www.fema.gov/flood-insurance/work-with-nfip/risk-rating/single-family-home)) |
| 10 | https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk | Risk narrative with no prices: "Over the past 10 years (2014 - 2024), nearly one-third of NFIP flood insurance claims (29%) came from areas located outside of current high-risk flood areas" and "Moderate- to lower-risk flood areas are designated with the letters B, C and X on FEMA flood maps." ([FloodSmart](https://www.floodsmart.gov/flood-zones-and-maps/what-is-my-flood-risk)) |
| 11 | https://www.floodsmart.gov/ | Risk messaging only: "Almost one-third of NFIP flood insurance claims come from OUTSIDE high-risk flood areas." ([FloodSmart](https://www.floodsmart.gov/)) |
| 12 | https://www.fema.gov/press-release/20250407/fema-launches-direct-customer-flood-insurance-premium-quoting-tool | Press release; one stat, no prices: "On average, 40% of NFIP flood insurance claims occur outside high hazard areas." ([FEMA](https://www.fema.gov/press-release/20250407/fema-launches-direct-customer-flood-insurance-premium-quoting-tool)) |
| 13 | https://www.fema.gov/press-release/20210318/fact-sheet-flood-plain-management-insurance-and-rebuilding | Floodplain-management fact sheet; no California zone pricing ([FEMA](https://www.fema.gov/press-release/20210318/fact-sheet-flood-plain-management-insurance-and-rebuilding)). |

Not scored (no usable content): `https://www.insurance.ca.gov/01-consumers/105-type/9-flood/` (404 — "Document Not Found") and `https://www.floodsmart.gov/flood-insurance/price` (fetch returned empty).

---

## Section 4 — Best-in-class examples

Four pages clear the full bar. None is a mainstream insurance brand.

### 1. FludZone — California flood zones — https://www.fludzone.com/flood-zones/california
The only page combining **measured** per-zone California premiums, an **embedded address lookup**, and a mandate statement.
> "Look Up Any California Address" — "Enter your CA address in FludZone's free lookup tool. We query FEMA's National Flood Hazard Layer in real-time" ([FludZone CA](https://www.fludzone.com/flood-zones/california))
> Zone X 69,510 policies, avg. **$812/yr** · Zone A 55,133, **$759/yr** · Zone AE 46,651, **$1,334/yr** · Zone AO 23,882, **$954/yr** · Zone AH 8,269, **$1,117/yr** · Zone VE 2,942, **$1,337/yr** · Zone D 843, **$1,230/yr** · Zone AOB 383, **$447/yr** ([FludZone CA](https://www.fludzone.com/flood-zones/california))
> "Properties in Zone X are not subject to the federal mandate but lenders may still require coverage" ([FludZone CA](https://www.fludzone.com/flood-zones/california))

### 2. StateCalc — California flood insurance calculator — https://statecalc.com/flood-insurance/california-flood-insurance-calculator/
Best *interaction* model: the visitor picks their own zone instead of reading someone else's blend.
> Zone selector: "Moderate/Low Risk (Zone X/B/C)" 0.84x · "High Risk / Special Flood Hazard Area (Zone A)" 1.14x · "Coastal High-Hazard (Zone V)" 1.27x ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/))
> "$833 in a low-risk zone ($69/month), versus $1,105 in a high-risk zone" ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/))
> "If your property is in a Special Flood Hazard Area (Zone A or V ...) and you have a federally-backed mortgage, flood insurance is legally required. Outside those zones, it's optional but often still worthwhile" ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/))
> "California's FIRM maps are available free at FEMA's Flood Map Service Center (msc.fema.gov)." ([StateCalc](https://statecalc.com/flood-insurance/california-flood-insurance-calculator/))

### 3. californiafloodinsurance.com — California FAQs — https://californiafloodinsurance.com/faqs/
Best *table* on an agency site, and the only one that prices a **mitigation variant** (AE elevated on pilings) rather than just a zone letter.
> "Zone X — standard residential | **$400 – $900** | Often 40–60% below NFIP equivalent" · "Zone AE — standard residential | **$1,200 – $3,000+**" · "Zone AE — elevated on pilings | **$600 – $1,400** | Elevation above base flood reduces premium sharply" · "Coastal / Zone VE | **$3,000 – $8,000+**" ([California FAQs](https://californiafloodinsurance.com/faqs/))
> "Which zones trigger the requirement" — "Zones AE, AH, AO, AR, and VE are all Special Flood Hazard Areas. Zone X (minimal or moderate flood hazard) does *not* trigger a mandatory purchase requirement." ([California FAQs](https://californiafloodinsurance.com/faqs/))
> "No mortgage? No legal requirement." ([California FAQs](https://californiafloodinsurance.com/faqs/))
> "Enter your address at FEMA's Flood Map Service Center (msc.fema.gov), or use our flood zone map lookup." ([California FAQs](https://californiafloodinsurance.com/faqs/))

### 4. Fluvenar / SmartTechInvest — https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium
Best *mandate-and-price-in-one-cell* presentation, and the only page that quantifies the gap as a decision.
> "Zone X (shaded) | Moderate risk, 0.2% annual probability | **No — but recommended** | **$700–$1,200**" · "Zone X (unshaded) | Minimal risk | **No** | **$500–$800**" · "Zone AE | High hazard, 1% annual flood probability | **Yes — federally backed loans** | **$3,200–$5,500**" ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium))
> "The equivalent Zone X property typically pays $700–$900/year on an optional basis." / "That $3,700/year gap doesn't appear anywhere in the listing." ([Fluvenar](https://smarttechinvest.com/fluvenar/blog/zone-ae-flood-insurance-california-2026-insurance-crisis-nfip-mandatory-premium))
> Caveat repeated: its premium levels are far above every measured source here and are unattributed.

**Honourable mention (mainstream):** LendingTree's California page is the strongest big-brand execution — per-zone monthly figures plus "No one can make you get flood insurance when you buy your home with cash or pay off your mortgage." ([LendingTree CA](https://www.lendingtree.com/home-insurance/california-flood-insurance/)) — but it stops short of an address lookup tool.

**What nobody does:** not one page in the survey combines (a) an embedded address→zone lookup, (b) per-zone California dollar figures sourced to measured NFIP data, (c) shaded vs unshaded X priced separately, and (d) an explicit "optional for you" statement placed *next to* the X-zone price rather than buried in an FAQ. That combination is an open gap.
