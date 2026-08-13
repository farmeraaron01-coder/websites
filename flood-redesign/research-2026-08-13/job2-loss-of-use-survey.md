# Loss-of-Use / ALE SERP Survey — Private Flood vs NFIP

**Prepared for:** californiafloodinsurance.com
**Date of data collection:** August 13, 2026
**Method:** `pplx_sdk.search.web` run separately for each of five queries, top 10 organic-style results captured per query (all five queries returned a full 10 results). Every unique URL then fetched in full with `pplx_sdk.content.fetch`. Ads, AI Overviews, and People-Also-Ask were not collected. Raw artifacts: `job2_serp_ranks.json`, `job2_fetch_status.json`, page text in `job2_pages/`, keyword extractions in `job2_dimensions.txt`.

Queries:
- **Q1** = `private flood insurance vs nfip`
- **Q2** = `does flood insurance cover temporary housing`
- **Q3** = `does flood insurance cover living expenses`
- **Q4** = `nfip vs private flood insurance california`
- **Q5** = `loss of use flood insurance`

**Fetch reliability:** 44/44 unique ranking URLs fetched successfully. Zero "not verified — fetch failed". One *control* URL failed (`https://www.floodsmart.gov/flood-insurance/what-covered` — 404) and one control returned only boilerplate (`https://www.floodsmart.gov/whats-covered` returned 385 characters of .gov banner text with no coverage content); both are noted in Section E.

---

## Section A — Executive finding

**Verdict: yes, there is a gap — not an empty field, but a shallow one.** Of 44 unique ranking pages, 41 mention loss of use / ALE / temporary housing at all, so the *fact* is not secret. But almost nobody sells it. On the private-vs-NFIP comparison pages that dominate Q1 and Q4, loss of use is a single unexplained row in a feature table — "Additional living expenses | Not covered | Available from select carriers" ([Flood Insurance Authority](https://floodinsuranceauthority.com/nfip-vs-private-flood-insurance)), "|Loss of use coverage|No|Yes|" ([Policygenius](https://www.policygenius.com/homeowners-insurance/private-flood-insurance-vs-nfip/)) — sandwiched between dwelling limits and waiting periods, with no dollar figure, no displacement math, and no emotional framing. The pages that *do* build a whole page around loss of use in a flood context are, with three exceptions, either your own network (californiafloodinsurance.com, statewidefloodinsurance.com, foreverfloridainsurance.com) or homeowners-insurance explainers that never mention flood at all (Farmers, Hippo, The Zebra, NAIC, TDI, III, Fox Business). The only genuine third-party competitors who make loss of use the headline argument in a flood context are **FloodPrice.com** and **The Flood Insurance Guru** (two posts). Everyone else who ranks for "loss of use flood insurance" is either a homeowners-ALE page, a 2015 geodata-vendor blog ([Intermap](https://www.intermap.com/risks-of-hazard-blog/2015/11/whats-loss-of-use-good-question)), or the raw SFIP policy form ([44 CFR Pt. 61 App. A(1)](https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61)).

**The four plain answers.** (1) **44 unique pages examined.** (2) **41 mention loss of use / ALE / temporary housing at all**; the three that do not are [Reddit r/Insurance](https://www.reddit.com/r/Insurance/comments/19fgw8m/why_is_private_flood_insurance_cheaper_than_nfip/) (Q1 #10), [Progressive's Flood 101](https://www.progressive.com/answers/flood-101/) (Q3 #8), and [FEMA's own /flood-insurance page](https://www.fema.gov/flood-insurance) (Q5 #1) — note that FEMA ranks #1 for `loss of use flood insurance` with a page that never uses the phrase. (3) **~26 make it prominently** (title/H2 or comparison-table row), but that number is misleading: only **10** are private-vs-NFIP comparison pages with an ALE row in the table, and only **6** are flood pages whose title is the loss-of-use argument (4 of those 6 are your own network or affiliated sites; the third-party ones are FloodPrice and Flood Insurance Guru ×2). Roughly **15 pages bury it** in a body paragraph, bullet list, or FAQ. (4) **30 state clearly that the NFIP does not offer it** — but 4 of those are government/policy-form sources (FEMA booklet, agents.floodsmart article, NC DOI Summary of Coverage, the CFR policy form) and several more are homeowners-insurance or news pages, so the number of *private-flood sellers* making the exclusion unmistakable is about **eleven**. **Nine pages fudge it** with "standard," "generally," or "most" — including two that are actively misleading: [1800insurance.com](https://www.1800insurance.com/guides/california-flood-insurance) contradicts itself inside one page ("something NFIP doesn't offer" … then "Neither NFIP nor most private policies cover temporary housing costs"), and [The Flood Insurance Guru's video post](https://www.floodinsuranceguru.com/floodvideoblog/whats-loss-of-use-in-flood-insurance) claims NFIP loss of use exists if "there should be a presidential declaration filed."

**Does anyone quantify it?** Barely — five pages, and none for California. The only hard private-flood ALE limits on any ranking page are **"$7,500"** ([USI comparison chart](https://www.usi.com/siteassets/images/insights/prs/q4-2022/flood-comparison-chart-2.pdf), and Chubb's base form per [Latent Insurance](https://www.latentinsure.com/blog/nfip-vs-private-flood-insurance)) and **"up to $25,000"** ([Flood Insurance Guru](https://www.floodinsuranceguru.com/the-flood-insurance-guru-blog/why-do-i-need-additional-living-expenses-on-my-flood-insurance)). The only worked displacement examples are Latent's **"pays $0"** over six months and Forever Florida's Sandy figure of **"$15,000 to $25,000 per household."** Nobody on any of the five SERPs prices a California displacement (rent differential in LA/Bay Area, 6–12 month rebuild) against an NFIP $0. That is the open lane: the exclusion is documented everywhere and monetized almost nowhere.

---

## Section B — Ranking table

`LoU?` = mentions loss of use / ALE / temporary housing at all. `NFIP-not?` = NFIP-does-not / fudges / private-only / unclear / not-stated. ⚑ = appears on 2+ queries.

| URL | Site | Type | Q1 | Q2 | Q3 | Q4 | Q5 | LoU? | NFIP-not? | Placement | Lender acceptance? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ⚑ https://californiafloodinsurance.com/loss-of-use-coverage-in-flood-insurance/ | California Flood Insurance | broker | – | 3 | 2 | 6 | 3 | Yes | NFIP-does-not | headline + H2 + FAQ | No |
| ⚑ https://www.insuranceclaimsinfo.com/resources/flood-insurance-nfip-vs-private | InsuranceClaimsInfo | other — claims/legal info | 9 | – | – | 2 | – | Yes | NFIP-does-not | table + bullets + FAQ | Yes |
| ⚑ https://www.nationalfloodinsurance.org/nfip-vs-private/ | National Flood Insurance (agency) | broker | 4 | – | – | 9 | – | Yes | private-only | body bullet list | No |
| ⚑ https://www.floodinsuranceguru.com/the-flood-insurance-guru-blog/why-do-i-need-additional-living-expenses-on-my-flood-insurance | The Flood Insurance Guru | broker | – | 8 | 5 | – | – | Yes | NFIP-does-not | headline + body | No |
| https://www.policygenius.com/homeowners-insurance/private-flood-insurance-vs-nfip/ | Policygenius | comparison site / lead-gen | 1 | – | – | – | – | Yes | NFIP-does-not (table) | comparison table + body | Yes |
| https://floodinsuranceauthority.com/nfip-vs-private-flood-insurance | Flood Insurance Authority | broker | 2 | – | – | – | – | Yes | NFIP-does-not | comparison table + body | Yes |
| https://statewidefloodinsurance.com/private-flood-insurance-vs-nfip/ | Statewide Flood Insurance | broker | 3 | – | – | – | – | Yes | NFIP-does-not | comparison table + bullet | Yes |
| https://floodprepare.com/knowledge/nfip-vs-private-flood-insurance-how-to-choose | FloodPrepare | broker / lead-gen | 5 | – | – | – | – | Yes | NFIP-does-not | spec list + table + body | No |
| https://www.usi.com/siteassets/images/insights/prs/q4-2022/flood-comparison-chart-2.pdf | USI Insurance Services | broker (commercial) | 6 | – | – | – | – | Yes | NFIP-does-not | comparison table row | No |
| https://neptuneflood.com/wp-content/uploads/2020/09/NFIP-vs-Private-Flood.pdf | Neptune Flood | carrier / MGA | 7 | – | – | – | – | Yes | NFIP-does-not | body bullets | Yes |
| https://www.latentinsure.com/blog/nfip-vs-private-flood-insurance | Latent Insurance | broker | 8 | – | – | – | – | Yes | NFIP-does-not | key-takeaways + table + FAQ | Yes |
| https://www.reddit.com/r/Insurance/comments/19fgw8m/why_is_private_flood_insurance_cheaper_than_nfip/ | Reddit r/Insurance | other — forum | 10 | – | – | – | – | **No** | n/a | not present | No |
| https://www.dicklawfirm.com/blog/2024/december/does-flood-insurance-cover-temporary-housing-/ | Dick Law Firm | other — law firm | – | 1 | – | – | – | Yes | NFIP-does-not | headline + body | No |
| https://www.tgiinsure.com/blog/does-flood-insurance-cover-temporary-housing-after-a-flood/ | TGI Insurance | broker | – | 2 | – | – | – | Yes | fudges | headline + body | No |
| https://www.shelteronsite.com/temporary-housing/temporary-housing-after-flood | Shelter On Site | other — temp-housing vendor | – | 4 | – | – | – | Yes | unclear | headline + body | No |
| https://www.foxbusiness.com/features/home-sweet-temporary-home | Fox Business | news | – | 5 | – | – | – | Yes | NFIP-does-not | body paragraph (buried) | No |
| https://neptuneflood.com/blog/what-does-flood-insurance-not-cover/ | Neptune Flood | carrier / MGA | – | 6 | – | – | – | Yes | fudges | body (myth list) + FAQ | No |
| https://www.curtismillerins.com/blog/does-flood-insurance-cover-temporary-living-expenses/ | Curtis Miller Insurance | broker | – | 7 | – | – | – | Yes | fudges | headline + body | No |
| https://insuranceindustryblog.iii.org/relocated-property-damaged-by-ida-you-may-be-eligible-for-additional-living-expenses/ | Insurance Information Institute | other — trade association | – | 9 | – | – | – | Yes | NFIP-does-not | body paragraph | No |
| https://content.naic.org/article/what-are-additional-living-expenses-and-how-can-insurance-help | NAIC | government / regulator body | – | 10 | – | – | – | Yes | not stated | headline + body (homeowners only) | No |
| https://www.allstate.com/resources/flood-insurance/what-does-flood-insurance-cover | Allstate | carrier | – | – | 1 | – | – | Yes | NFIP-does-not | not-covered bullet list | Yes (requirement only) |
| https://www.tdi.texas.gov/blog/additional-living-expenses.html | Texas Dept. of Insurance | government | – | – | 3 | – | – | Yes | NFIP-does-not | body (one line) | No |
| https://agents.floodsmart.gov/articles/what-covered-flood-insurance-policy-homeowners | FEMA / FloodSmart (agents) | government | – | – | 4 | – | – | Yes | NFIP-does-not | "What isn't covered?" bullet | No |
| https://www.consumer-action.org/english/articles/disaster_insurance_and_fema_assistance | Consumer Action | other — nonprofit | – | – | 6 | – | – | Yes | NFIP-does-not | buried in long FAQ | Yes (requirement only) |
| https://www.thezebra.com/homeowners-insurance/coverage/additional-living-expenses-coverage/ | The Zebra | comparison site | – | – | 7 | – | – | Yes | NFIP-does-not | FAQ subsection | No |
| https://www.progressive.com/answers/flood-101/ | Progressive | carrier | – | – | 8 | – | – | **No** | n/a | not present | Yes (requirement only) |
| https://www.ncdoi.gov/nfip-summarycoverage/open | NC Dept. of Insurance (NFIP Summary of Coverage) | government | – | – | 9 | – | – | Yes | NFIP-does-not | not-covered bullet list | No |
| https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-recovering-financially-after-a-flood-booklet-01-2025.pdf | FEMA / NFIP booklet | government | – | – | 10 | – | – | Yes | NFIP-does-not | dedicated "ALE" section | No |
| https://www.1800insurance.com/guides/california-flood-insurance | 1800Insurance | aggregator / lead-gen | – | – | – | 1 | – | Yes | fudges (self-contradictory) | body paragraphs | Yes |
| https://www.tsminsurance.com/resources/flood-insurance-california-options | TSM Insurance | broker | – | – | – | 3 | – | Yes | fudges | comparison table + FAQ | Yes (requirement only) |
| https://www.bollinsure.com/guides?g=flood-earthquake-insurance-california | Bollinsure | broker | – | – | – | 4 | – | Yes | NFIP-does-not | body bullet (one clause) | No |
| https://californiafloodinsurance.com/private-flood-insurance-vs-fema/ | California Flood Insurance | broker | – | – | – | 5 | – | Yes | NFIP-does-not | bolded body bullet | No |
| https://www.policygenius.com/homeowners-insurance/flood-insurance-california/ | Policygenius | comparison site / lead-gen | – | – | – | 7 | – | Yes | NFIP-does-not (table) | comparison table + body | Yes |
| https://www.aonedge.com/Resource-Center/Blog/What%E2%80%99s-the-Difference-Between-The-NFIP-and-PFI | Aon Edge | broker / program manager | – | – | – | 8 | – | Yes | NFIP-does-not | body (one line) | Yes — statutory definition |
| https://blakeinsurancegroup.com/best-flood-insurance-company-california/ | Blake Insurance Group | broker | – | – | – | 10 | – | Yes | fudges | comparison table rows | Yes |
| https://www.fema.gov/flood-insurance | FEMA | government | – | – | – | – | 1 | **No** | n/a | not present | Yes (requirement only) |
| https://www.floodinsuranceguru.com/floodvideoblog/whats-loss-of-use-in-flood-insurance | The Flood Insurance Guru | broker | – | – | – | – | 2 | Yes | fudges (inaccurate) | headline + body | No |
| https://www.intermap.com/risks-of-hazard-blog/2015/11/whats-loss-of-use-good-question | Intermap | other — geospatial data vendor | – | – | – | – | 4 | Yes | NFIP-does-not | headline + body | No |
| https://foreverfloridainsurance.com/private-flood-insurance-with-loss-of-use/ | Forever Florida Insurance | broker | – | – | – | – | 5 | Yes | NFIP-does-not | headline + table + body | Yes — "not narrower" |
| https://www.farmers.com/learn/insurance-questions/loss-of-use-coverage/ | Farmers Insurance | carrier | – | – | – | – | 6 | Yes | fudges | "What is not covered" section | No |
| https://www.hippo.com/learn-center/loss-of-use-coverage | Hippo | carrier | – | – | – | – | 7 | Yes | not stated | headline + body (homeowners only) | No |
| https://www.floodprice.com/post/what-is-loss-of-use-coverage | FloodPrice | aggregator / quoting platform | – | – | – | – | 8 | Yes | NFIP-does-not | headline + H2 | No |
| https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61 | Cornell LII (SFIP, 44 CFR Pt. 61 App. A(1)) | government / legal text | – | – | – | – | 9 | Yes | NFIP-does-not | policy exclusions section | No |
| https://statewidefloodinsurance.com/loss-of-use-coverage-in-flood-insurance/ | Statewide Flood Insurance | broker | – | – | – | – | 10 | Yes | NFIP-does-not | headline + body | No |

Multi-query URLs (⚑): **californiafloodinsurance.com/loss-of-use-coverage-in-flood-insurance/ (4 queries: Q2 #3, Q3 #2, Q4 #6, Q5 #3)** — your own page is the most broadly-ranking single asset in this survey; insuranceclaimsinfo.com (Q1 #9, Q4 #2); nationalfloodinsurance.org (Q1 #4, Q4 #9); floodinsuranceguru.com ALE post (Q2 #8, Q3 #5).

---

## Section C — Per-page dossier

#### Policygenius (private flood vs NFIP) — https://www.policygenius.com/homeowners-insurance/private-flood-insurance-vs-nfip/
- Query ranks: Q1=1, Q2=–, Q3=–, Q4=–, Q5=–
- Site type: comparison site / lead-gen
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Private flood policies also typically include coverage for additional living expenses to cover temporary expenses like hotel stays and restaurant meals if you're unable to live in your home after a flood." and "This includes payments for temporary living expenses — like hotel stays and restaurant meals — and coverage for personal belongings in your basement."
- NFIP exclusion stated: NFIP-does-not (table only) — "|Loss of use coverage|No|Yes|" (no prose sentence states the exclusion)
- Placement: comparison table row + body paragraph
- Other coverage comparisons: "The maximum building coverage limits for residential property is $250,000, which is often too low for more expensive homes."; "The maximum personal property coverage limit is $100,000."; "|Maximum home rebuild limit|$250,000|Typically up to $500,000 or higher|"; "|Waiting period|30 days|As little as two weeks|"; "|Replacement cost contents coverage|No|Yes|"; "Through Neptune, you have access to up to $4 million in building coverage, up to $500,000 in personal property coverage, and up to $10,000 in coverage for belongings stored in your basement"; "Chubb flood policies include up to $15 million in building and personal property coverage, as well as up to $15,000 in coverage for belongings stored in your basement."
- Lender acceptance: Yes — "But as of July 1, 2019, lenders are required to accept private flood insurance as long as the policy includes at least the same quality coverage as the NFIP option." (paraphrases the "at least as broad as" standard; no statutory-definition or compliance-aid language)
- Short note: The #1 result for the money query treats loss of use as one row among eight. No dollar limit, no displacement scenario.

#### Flood Insurance Authority — https://floodinsuranceauthority.com/nfip-vs-private-flood-insurance
- Query ranks: Q1=2
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Coverage limits in the private market frequently exceed NFIP caps — some carriers offer building coverage limits of $5 million or higher — and policy structures can include replacement cost value (RCV) settlement, business interruption coverage, and additional living expenses, none of which appear in the SFIP." and "|**Additional living expenses**|Not covered|Available from select carriers|"
- NFIP exclusion stated: NFIP-does-not — "…additional living expenses, none of which appear in the SFIP."
- Placement: comparison table row + body paragraph + checklist item ("Pay particular attention to basement coverage treatment, additional living expense provisions, and business interruption availability if applicable.")
- Other coverage comparisons: "|**Replacement cost value (RCV) settlement**|Not available for contents; structure RCV available under certain conditions|Available from many carriers|"; "|**Business interruption**|Not covered|Available from select carriers|"; "|**Standard waiting period**|30 days (exceptions apply)|Varies; often shorter|"; "the standard NFIP waiting period is 30 days under 44 C.F.R."; "Excess policies sit above the NFIP layer and are always private products." (note: the dwelling/contents cap cells render as the placeholder "amounts that vary by jurisdiction" rather than dollar figures)
- Lender acceptance: Yes — "Even when a private policy meets the regulatory standard under the 2019 joint final rule, individual lenders retain discretion on policy form acceptance." and "The Biggert-Waters Flood Insurance Reform Act of 2012 … qualifying private flood policies explicitly satisfy the mandatory purchase requirement for federally regulated lenders." Mentions the statutory/2019-rule framework; no "at least as broad as" phrase and no compliance-aid assurance clause.
- Short note: The most technically thorough comparison on Q1 and the only one to pair ALE with business interruption. Still one table row; no dollars.

#### Statewide Flood Insurance (private vs NFIP) — https://statewidefloodinsurance.com/private-flood-insurance-vs-nfip/
- Query ranks: Q1=3
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "|**Loss of use / living expenses**|❌ Not covered|✅ Often available|"; "- **Additional living expenses / loss of use** — hotel and living costs while your home is uninhabitable."; "- The NFIP caps coverage ($250k/$100k) and excludes living expenses; private goes well beyond."
- NFIP exclusion stated: NFIP-does-not — "The NFIP caps coverage ($250k/$100k) and excludes living expenses; private goes well beyond."
- Placement: comparison table row + summary bullet + body bullet
- Other coverage comparisons: "|**Building coverage limit**|Capped at **$250,000**|Up to **$1M+**|"; "|**Contents coverage limit**|Capped at **$100,000**|Higher limits available|"; "|**Replacement cost (contents)**|❌ Actual cash value only|✅ Often available|"; "|**Waiting period**|30 days (standard)|Often **7–14 days**|"; "|**Lender accepted**|✅ Yes|✅ Yes, if it meets federal standards|"
- Lender acceptance: Yes — "Under the Biggert-Waters Act, **federally regulated lenders are required to accept a qualifying private flood policy** — one that provides coverage at least equivalent to the NFIP, from a properly licensed carrier, with the required notice and cancellation terms." ("at least equivalent" ≈ "at least as broad as"; no compliance-aid clause)
- Short note: Same network/style as the client's site. Loss of use is row 1 of the table — the most prominent table placement in the survey — but again unquantified.

#### National Flood Insurance (agency) — https://www.nationalfloodinsurance.org/nfip-vs-private/
- Query ranks: Q1=4, Q4=9
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes (bare mention)
- Exact quote: "Other optional coverages available only through private flood are:" / "- Additional living expenses"
- NFIP exclusion stated: private-only — "Other optional coverages available only through private flood are: - Additional living expenses"
- Placement: body bullet list
- Other coverage comparisons: "Through the NFIP the maximum building coverage provided is $250,000."; "Private flood carriers can provide up to $1 million in building coverage, with some offering even higher limits."; "For replacement cost, this valuable coverage is only available for primary residences under the NFIP."; "Through the NFIP there is a mandatory 30-day waiting period from the date of payment to the date your coverage begins."; "The maximum waiting period under a private flood policy is only 15 days, with some companies allowing coverage to go into effect immediately."
- Lender acceptance: No — not mentioned
- Short note: Ranks on two queries with a three-word bullet. Zero explanation of what ALE is or costs.

#### FloodPrepare — https://floodprepare.com/knowledge/nfip-vs-private-flood-insurance-how-to-choose
- Query ranks: Q1=5
- Site type: broker / lead-gen
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "- **Additional living expenses:** Not covered"; "- **Additional living expenses.** Many private policies cover temporary housing costs while your home is repaired."; "|Additional living expenses|No|Often yes|"
- NFIP exclusion stated: NFIP-does-not — "- **Additional living expenses:** Not covered" (inside the NFIP specification list)
- Placement: NFIP spec list + body bullet + comparison table row
- Other coverage comparisons: "- **Structure coverage:** Up to $250,000"; "- **Waiting period:** 30 days (with mortgage requirement exceptions)"; "- **Basement contents:** Excluded"; "|Max structure coverage|$250,000|$500K–unlimited|"; "|Basement contents|Excluded|Often covered|"; "|Waiting period|30 days|10–14 days (some same-day)|"; "Most private carriers offer structure coverage up to $500,000 or higher, and some offer unlimited replacement cost."
- Lender acceptance: No — only "(with mortgage requirement exceptions)" regarding the waiting period
- Short note: Mentions ALE three times and still never says what it pays. Leads on the $250,000 cap instead ("For many homeowners, the $250,000 structure cap is now the binding constraint.").

#### USI Insurance Services (flood comparison chart, PDF) — https://www.usi.com/siteassets/images/insights/prs/q4-2022/flood-comparison-chart-2.pdf
- Query ranks: Q1=6
- Site type: broker (commercial/large brokerage)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Does the policy include loss of use? / Not available. / Private flood policies offer loss of use, resiliency and expanded replacement cost." and "Private flood insurance covers your dwelling, other structures, loss of use, resiliency, and their contents from water damage caused by flood."
- NFIP exclusion stated: NFIP-does-not — "Does the policy include loss of use? … Not available."
- Placement: comparison table row (a dedicated question row in a two-column chart)
- Other coverage comparisons: "The maximum limits available are $250,000 for dwelling and $100,000 for contents."; "(Coverage for a detached garage can be covered up to $25K, thus reducing the $250K for the building.)"; "Requires a 30-day waiting period." vs "No waiting period or up to 14 days, depending on the carrier."; worked claim example: "will be paid is $250,000 for the dwelling and $100,000 for contents. The client will pay $457,500 out of pocket plus deductibles." vs "they will be paid $500,000 for the building and $300,000 for the contents, plus the loss of use/rents of $7,500. The client will only need to pay the deductible out of pocket."
- Lender acceptance: No — not mentioned
- Short note: **The only page in the entire survey with a worked side-by-side claim example that includes a loss-of-use dollar figure** — and it's a 2022 PDF from a commercial brokerage, not a consumer page. The $7,500 is small enough to be a weak benchmark you can beat.

#### Neptune Flood (NFIP vs Private, PDF) — https://neptuneflood.com/wp-content/uploads/2020/09/NFIP-vs-Private-Flood.pdf
- Query ranks: Q1=7
- Site type: carrier / MGA
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "d. The NFIP has low coverage limits, no coverage for basement contents, external buildings, pools, replacement cost for contents, or temporary living expense, all common in other forms of insurance." and "3. Private insurers also offer coverages not available from the NFIP, such as for external buildings not attached to your house, pools, temporary living expenses in case you are forced out of your home due to a flood, and replacement cost on your contents."
- NFIP exclusion stated: NFIP-does-not — "The NFIP has low coverage limits, no coverage for … temporary living expense"
- Placement: body bullets (items d and 3 of two lists)
- Other coverage comparisons: "Whereas the NFIP only covers up to $250,000 of building loss and $100,000 of contents, private insurers can offer higher limits, for example Neptune provides coverage up to $2,000,000 for building and $500,000 for contents."; "The NFIP requires tons of paperwork, a 30-day delay to start a policy, an expensive home inspection…"; "Some properties have flooded up to 45 times under the NFIP…"
- Lender acceptance: Yes — "To qualify as a flood insurance provider with mortgage lenders including the FHA and VA as well as large banks, private flood insurance providers must meet the same or better policy terms and conditions as the NFIP." ("same or better" ≈ "at least as broad as"; no statutory-definition or compliance-aid clause)
- Short note: A carrier that sells ALE lists it fourth in a bullet about paperwork and pools. No limit disclosed.

#### Latent Insurance — https://www.latentinsure.com/blog/nfip-vs-private-flood-insurance
- Query ranks: Q1=8
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes — the strongest third-party treatment on Q1
- Exact quote: "> - **The NFIP pays nothing for temporary housing.** There is no additional living expenses or loss-of-use coverage on an NFIP policy, per FEMA's NFIP Summary of Coverage."; "- **No additional living expenses.** If a flood makes your home uninhabitable for six months, the NFIP pays $0 toward rent, hotels, or meals, per FEMA's Summary of Coverage."; "- **Additional living expenses.** Private policies routinely include loss-of-use coverage; Chubb's base flood form includes $7,500 with higher limits available."; "|Additional living expenses|None|Included or optional|"; "- **You need ALE or replacement-cost contents.** Families who cannot self-fund six months of temporary housing should not carry a policy that pays $0 for it."
- NFIP exclusion stated: NFIP-does-not — "There is no additional living expenses or loss-of-use coverage on an NFIP policy, per FEMA's NFIP Summary of Coverage."
- Placement: key-takeaways block near the top of the page + comparison table row + decision bullets + FAQ
- Other coverage comparisons: "The NFIP caps residential flood coverage at $250,000 for the building and $100,000 for contents, pays contents claims at actual cash value, includes no additional living expenses, and carries a 30-day waiting period."; "|Max building limit (residence)|$250K|$1M – $15M+ (carrier dependent)|"; "|Max contents limit|$100K|$500K – $1M+|"; "|Contents valuation|Actual cash value|Replacement cost (typical)|"; "|Waiting period|30 days (waived with mortgage)|0 – 14 days|"; "|Basement improvements|Excluded|Available on many forms|"; "Chubb writes flood coverage up to $15 million combined for home and contents, per Chubb."; "Specialist Neptune Flood writes building limits up to $7 million, per CNBC Select."; "Increased Cost of Compliance coverage, up to $30,000…"; "PURE writes up to $2 million dwelling / $1 million contents…"
- Lender acceptance: Yes — "- **Lender review friction.** Lenders must accept a qualifying private policy, and the 2019 rule's compliance aid (a policy statement that it meets the statutory definition) makes review nearly automatic, per the FDIC." and "A joint federal rule effective July 1, 2019 requires regulated lenders to accept private flood insurance that meets the Biggert-Waters Act definition, and most private policies include a compliance-aid statement that lets the lender approve it without a line-by-line review." — mentions both the statutory definition and the compliance-aid assurance clause.
- Short note: **This is your closest competitor on substance.** It is the only comparison page that puts "The NFIP pays nothing for temporary housing" in a top-of-page takeaway box, quantifies a private limit ($7,500 Chubb), and frames a six-month displacement. It does not price a California displacement or name a California market.

#### InsuranceClaimsInfo — https://www.insuranceclaimsinfo.com/resources/flood-insurance-nfip-vs-private
- Query ranks: Q1=9, Q4=2 (⚑ two queries)
- Site type: other — claims/legal information site (California-focused)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "- **No additional living expenses (ALE) or loss of use coverage**"; "- **Temporary housing:** No coverage for additional living expenses while your home is being repaired"; "|Additional Living Expenses|Not covered|May be covered|"; "- **Do you need additional living expenses coverage?** The NFIP does not provide it."; "- **Broader coverage:** Many private policies cover additional living expenses, pool and patio damage, basement contents, and other items excluded by the NFIP"
- NFIP exclusion stated: NFIP-does-not — "**Do you need additional living expenses coverage?** The NFIP does not provide it."
- Placement: exclusion bullet list + comparison-table row + decision-checklist question + FAQ; no dollar figure and no headline treatment
- Other coverage comparisons: "- **Dwelling (building) coverage:** Maximum $250,000 for residential properties"; "For many California homeowners — where even modest homes can exceed $500,000 in replacement cost — the $250,000 dwelling cap is a serious limitation."; "Personal property (contents) is **always** valued at actual cash value under the NFIP — there is no replacement cost option for contents."; "- **Basement improvements:** Finished walls, floors, ceilings, and other improvements in a basement are not covered under either building or contents coverage"; "|Max Dwelling Coverage|$250,000|Varies — can exceed $1M+|"; "|Basement Contents|Severely limited|May be covered (policy-dependent)|"; "|Statute of Limitations|1 year from denial (42 U.S.C."
- Lender acceptance: Yes — "- **Does your mortgage lender accept private flood insurance?** Federal banking regulators require lenders in flood zones to accept qualifying private flood insurance, but confirm with your lender before switching from NFIP to private coverage" (no statutory-definition or compliance-aid language)
- Short note: Ranks twice (Q1 #9, Q4 #2) and is explicitly California-framed, but treats ALE as one item in a long exclusion list — the strongest emphasis goes to the $250K dwelling cap and to NFIP litigation/bad-faith limits, not to displacement cost.

#### Reddit r/Insurance — https://www.reddit.com/r/Insurance/comments/19fgw8m/why_is_private_flood_insurance_cheaper_than_nfip/
- Query ranks: Q1=10
- Site type: other — user forum
- Mentions LoU/ALE/temp housing: No
- Exact quote: not mentioned
- NFIP exclusion stated: n/a
- Placement: not present
- Other coverage comparisons: thread discusses pricing/underwriting only; no coverage-dimension claims quoted
- Lender acceptance: No — not mentioned
- Short note: The discussion is entirely about why private is cheaper — the exact "price-only" framing the agency wants to move past.

#### Dick Law Firm — https://www.dicklawfirm.com/blog/2024/december/does-flood-insurance-cover-temporary-housing-/
- Query ranks: Q2=1
- Site type: other — plaintiff insurance law firm
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "However, the NFIP explicitly does not provide coverage for additional living expenses (ALE), such as hotel stays, rental costs, or other temporary housing needs while your home is being repaired."; "If you rely solely on NFIP policies, you must bear the costs of temporary housing out-of-pocket or seek alternative financial assistance."; "Certain private insurance companies have coverage for ALE, so they help with related costs, including temporary accommodation."; "Explore private flood insurance providers, as they are more likely to offer ALE coverage."
- NFIP exclusion stated: NFIP-does-not — "the NFIP explicitly does not provide coverage for additional living expenses (ALE)"
- Placement: headline (page title) + body
- Other coverage comparisons: none beyond ALE; only "### Standard Coverage and Its Limitations" framing
- Lender acceptance: No — not mentioned
- Short note: A Texas law firm owns rank #1 for the temporary-housing query with a clean, correct answer — and no quote, no California angle, no dollar figure.

#### TGI Insurance — https://www.tgiinsure.com/blog/does-flood-insurance-cover-temporary-housing-after-a-flood/
- Query ranks: Q2=2
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "A key point for homeowners to know is that standard flood insurance policies generally do not cover additional living expenses (ALE) or temporary housing costs."; "Although NFIP policies typically don't cover temporary housing following a flood that displaces a homeowner, additional options may be available."; "In recent years, an increasing number of private insurers have started offering flood insurance, which can often include higher policy limits and additional financial protections, such as ALE coverage."
- NFIP exclusion stated: fudges — "standard flood insurance policies **generally** do not cover" / "NFIP policies **typically** don't cover"
- Placement: headline + body
- Other coverage comparisons: only the general "higher policy limits" claim quoted above
- Lender acceptance: No — not mentioned
- Short note: Hedged with "generally" and "typically" where the exclusion is actually absolute. An accuracy opening.

#### California Flood Insurance (loss of use) — https://californiafloodinsurance.com/loss-of-use-coverage-in-flood-insurance/
- Query ranks: Q1=–, Q2=3, Q3=2, Q4=6, Q5=3 (4 of 5 queries)
- Site type: broker (the client)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "The National Flood Insurance Program (NFIP), run by FEMA, does not cover loss of use, additional living expenses, or temporary housing of any kind."; "If a flood forces you out of your house, who pays for the hotel, the rental, and the restaurant meals while contractors gut and rebuild?"; "An NFIP policy pays toward repairing your building (up to $250,000) and contents (up to $100,000, on an actual cash value basis), but it provides nothing toward a hotel, rental, or extra costs while you are displaced."; "Loss of use limits on private policies are usually expressed as a dollar cap or as a percentage of your dwelling coverage, often somewhere around 10% to 20%."
- NFIP exclusion stated: NFIP-does-not — "The National Flood Insurance Program (NFIP), run by FEMA, does not cover loss of use, additional living expenses, or temporary housing of any kind."
- Placement: headline/H1 + dedicated H2 ("Does the NFIP Cover Loss of Use or Living Expenses?") + FAQ
- Other coverage comparisons: "An NFIP residential policy is also capped at $250,000 for the building and $100,000 for contents, and it pays contents on an actual cash value basis — meaning depreciation is subtracted."; "Beyond ALE, private policies can offer building limits above $250,000, replacement-cost contents coverage, and add-ons the federal program doesn't write."; "…commercial flood insurance, where the NFIP caps at $500,000 building and $500,000 contents and private limits can go much higher."
- Lender acceptance: No — not mentioned
- Short note: Already the broadest-ranking asset in this data set (4 of 5 queries). It is also the only page that ties loss of use to California displacement length and Zone X claims.

#### Shelter On Site — https://www.shelteronsite.com/temporary-housing/temporary-housing-after-flood
- Query ranks: Q2=4
- Site type: other — temporary-housing/RV vendor
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Usually **covered by homeowners insurance**, which triggers Additional Living Expenses for temporary housing."; "Rising external floodwater is usually covered only by a separate flood policy, so check which applies before assuming ALE is available."; "That's why what looks like a two-week fix becomes a multi-month displacement, and why the length of ALE coverage matters here."
- NFIP exclusion stated: unclear — never states that the NFIP excludes ALE; only "check which applies before assuming ALE is available."
- Placement: headline + body
- Other coverage comparisons: none (no private-vs-NFIP dimensions)
- Lender acceptance: No — not mentioned
- Short note: Ranks #4 on the temporary-housing query while leaving the flood/NFIP question unanswered — pure competitive weakness.

#### Fox Business — https://www.foxbusiness.com/features/home-sweet-temporary-home
- Query ranks: Q2=5
- Site type: news
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "For that matter, flood insurance policies through the National Flood Insurance Program don't include additional living expenses either, although there are some privately sold flood policies that do."; "Standard home insurance includes coverage for additional living expenses, or loss of use, which pays for extra costs to live while your house is uninhabitable."; "Generally, home insurance caps additional living expenses to a portion of the dwelling coverage, typically 20%, Swerling says, and sets a time limit, such as 12 months."; "So if your home is insured for $200,000, then you have up to $40,000 to spend on additional living expenses."; "In California, home insurers must give policyholders at least 24 months to spend additional living expenses coverage."
- NFIP exclusion stated: NFIP-does-not — "flood insurance policies through the National Flood Insurance Program don't include additional living expenses either"
- Placement: buried body paragraph inside a homeowners-ALE feature
- Other coverage comparisons: none for flood; homeowners ALE percentages/time limits only
- Lender acceptance: No — not mentioned
- Short note: Correct but incidental. The 20%/$40,000/24-month California figures are homeowners, not flood — useful precedent language, not a flood benchmark.

#### Neptune Flood (what flood insurance doesn't cover) — https://neptuneflood.com/blog/what-does-flood-insurance-not-cover/
- Query ranks: Q2=6
- Site type: carrier / MGA
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "**Flood insurance will pay for my hotel if I have to evacuate.**" / "Most standard flood insurance policies, including those through the NFIP, don't cover temporary housing or hotel stays, even if your home is uninhabitable."; "Flood insurance typically excludes damage to items in basements (especially finished basements), outdoor property (pools, fences, landscaping), temporary living expenses, business interruption losses, and damage from earth movement or poor maintenance."; "Standard policies exclude temporary relocation, mold due to delayed cleanup, basement finishes…"
- NFIP exclusion stated: fudges — "**Most** standard flood insurance policies, **including those through the NFIP**, don't cover temporary housing or hotel stays"
- Placement: body (myth-busting list item) + FAQ
- Other coverage comparisons: "the NFIP caps structure coverage at $250,000 for residential buildings"; "It also caps structure and contents limits at $250,000 and $100,000, respectively."; "Unlike the NFIP, which has fixed limits and rules, private policies offer more flexibility."; "**Consider Excess Flood Insurance**"; basement/BFE exclusions as quoted
- Lender acceptance: No — not mentioned
- Short note: Striking omission — a private carrier writing about hotel exclusions never says "our private policy can cover it." It pivots to excess flood instead.

#### Curtis Miller Insurance — https://www.curtismillerins.com/blog/does-flood-insurance-cover-temporary-living-expenses/
- Query ranks: Q2=7
- Site type: broker (WV)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "However, the standard policy does not cover temporary living expenses while your home is being repaired."; "A standard flood insurance policy will not cover any damage caused by mold or other pollutants, nor will it cover costs related to temporary housing or relocation expenses."; "This additional coverage is available, however."
- NFIP exclusion stated: fudges — never names the NFIP or FEMA anywhere on the page; only "the standard policy does not cover temporary living expenses"
- Placement: headline + body
- Other coverage comparisons: none
- Lender acceptance: No — not mentioned
- Short note: A 300-word page ranks #7 on a commercially valuable query without naming the NFIP or the private market. Thin.

#### The Flood Insurance Guru (why do I need ALE) — https://www.floodinsuranceguru.com/the-flood-insurance-guru-blog/why-do-i-need-additional-living-expenses-on-my-flood-insurance
- Query ranks: Q2=8, Q3=5
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "While NFIP policies cover building and contents, they do not offer Additional Living Expenses."; "Additional Living Expenses provide extra funds to pay for temporary housing, rent, utilities, and other necessary costs while your home is being repaired after a flood."; "Most private flood insurance policies include Additional Living Expenses coverage up to $25,000, depending on the provider."; "In areas where flooding occurs but does not trigger a disaster declaration, homeowners without private flood insurance would be left without temporary housing support."; "A homeowner in Nebraska recently shared that without ALE in her private flood insurance policy, she wouldn't have known where to stay while her home was being repaired."
- NFIP exclusion stated: NFIP-does-not — "While NFIP policies cover building and contents, they do not offer Additional Living Expenses."
- Placement: headline + body throughout
- Other coverage comparisons: none quantified beyond the $25,000 ALE figure
- Lender acceptance: No — not mentioned
- Short note: **The single best third-party execution of this argument** — headline, exclusion, a dollar limit, and a human anecdote. It is not California-specific (Alabama/Tennessee/Nebraska/Iowa/Minnesota examples).

#### Insurance Information Institute (blog) — https://insuranceindustryblog.iii.org/relocated-property-damaged-by-ida-you-may-be-eligible-for-additional-living-expenses/
- Query ranks: Q2=9
- Site type: other — industry trade association
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "The National Flood Insurance Program (NFIP) covers physical damage from flood but does not include ALE. Some privately sold flood policies offer ALE following flood losses."; "Your homeowners policy's ALE coverage is usually equal to 20 percent of your home's insured value—a home insured for $200,000, for instance, may have ALE coverage of up to $40,000—or limited to a certain timeframe (e.g., no more than 12 months)."
- NFIP exclusion stated: NFIP-does-not — "The National Flood Insurance Program (NFIP) covers physical damage from flood but does not include ALE."
- Placement: body paragraph near the end of a Hurricane Ida post
- Other coverage comparisons: none for flood (homeowners ALE percentages only)
- Lender acceptance: No — not mentioned
- Short note: An authoritative, citable one-liner for your own copy: III says NFIP "does not include ALE." Buried in a 2021 storm post.

#### NAIC — https://content.naic.org/article/what-are-additional-living-expenses-and-how-can-insurance-help
- Query ranks: Q2=10
- Site type: government / regulator association
- Mentions LoU/ALE/temp housing: Yes (homeowners only)
- Exact quote: "If you can't stay in your home after a covered disaster, many homeowners policies will pay for additional living expenses (ALE)."; "Those are **temporary** housing costs if you move into a hotel or apartment while your home is being repaired or rebuilt."; "It will only pay **the difference** between your previous living expenses and your new temporary expenses."
- NFIP exclusion stated: not stated — flood and the NFIP are never mentioned on the page
- Placement: headline + body (homeowners context)
- Other coverage comparisons: none; only "Some policies have a dollar limit; some may also have a time limitation."
- Lender acceptance: No — not mentioned
- Short note: A regulator page ranks #10 for a flood query with no flood content — evidence that the flood-specific ALE intent is under-served.

#### Allstate — https://www.allstate.com/resources/flood-insurance/what-does-flood-insurance-cover
- Query ranks: Q3=1
- Site type: carrier
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Equally important is knowing what's not covered by flood insurance. Here are a few examples of the types of property and expenses that fall outside the scope of a basic flood insurance policy, according to the NFIP:" / "- Living expenses, like temporary housing (if flood damage deems your home uninhabitable)."
- NFIP exclusion stated: NFIP-does-not — the bullet sits under an explicitly NFIP-attributed "not covered" list
- Placement: not-covered bullet list (mid-page)
- Other coverage comparisons: "- Maximum coverage limit: $250,000"; "Replacement cost basis (what it would take to repair the home in today's dollars) for a primary residence and actual cash value (which factors in depreciation) for a vacation home."; "In addition, flood insurance provides limited, if any, coverage for below-ground rooms like crawl spaces and basements, and their contents, the NFIP says."
- Lender acceptance: Yes (requirement only) — "If you own a home on land that is at high risk of flooding, your mortgage lender may require you to purchase flood insurance, says the Federal Emergency Management Agency (FEMA)." No private-flood acceptance discussion.
- Short note: The #1 result for the living-expenses query is a carrier that doesn't sell private flood and offers no alternative — a wide-open competitive door.

#### Texas Department of Insurance — https://www.tdi.texas.gov/blog/additional-living-expenses.html
- Query ranks: Q3=3
- Site type: government (state regulator)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "But NFIP policies don't pay for additional living expenses."; "If your home policy includes flood coverage, it probably will pay for additional living expenses."; "Homeowners and renters policies may cover additional living expenses if you can't stay in your home because it was damaged by an event that's covered in your policy."
- NFIP exclusion stated: NFIP-does-not — "But NFIP policies don't pay for additional living expenses."
- Placement: body (single sentence in a short post)
- Other coverage comparisons: none
- Lender acceptance: No — not mentioned
- Short note: A state DOI states the exclusion in seven words. Citable third-party validation; no California equivalent appeared in these SERPs (no CDI page ranked).

#### FEMA / FloodSmart for agents — https://agents.floodsmart.gov/articles/what-covered-flood-insurance-policy-homeowners
- Query ranks: Q3=4
- Site type: government
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "**What isn't covered?** There are specific items not covered by a building or contents coverage policy. These include:" / "- Temporary housing and additional living expenses incurred while the building is being repaired or is unable to be occupied."
- NFIP exclusion stated: NFIP-does-not — the bullet above, under "What isn't covered?"
- Placement: "What isn't covered?" bullet list
- Other coverage comparisons: "This policy does include a coverage limit of $250,000 for damage caused to the building."; "The coverage limit for a personal content policy is $100,000."; "- Personal property kept in basements."
- Lender acceptance: No — not mentioned
- Short note: This is the cleanest FEMA-domain sentence to cite in sales collateral, and it is FEMA's own agent-facing talking-points page.

#### Consumer Action — https://www.consumer-action.org/english/articles/disaster_insurance_and_fema_assistance
- Query ranks: Q3=6
- Site type: other — consumer nonprofit
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Note that flood insurance policies through the National Flood Insurance Program (NFIP) don't cover additional living expenses either, but some privately sold flood policies do."; "Coverage for 'additional living expenses,' or loss of use, pays for the extra costs of living elsewhere while your home is uninhabitable."; "For example, if your home is insured for $300,000, and the limit for additional living expenses on your policy is 30 percent, then you would be allowed up to $90,000 to spend on hotel bills, rent, etc."; "In California, policyholders get at least 24 months to spend additional living expenses coverage, but other states set lower limits (12 months, in many cases)."
- NFIP exclusion stated: NFIP-does-not — "flood insurance policies through the National Flood Insurance Program (NFIP) don't cover additional living expenses either"
- Placement: buried inside a very long (28k-character) FAQ article
- Other coverage comparisons: "Maximum coverage for one- to four-family homes under the National Flood Insurance Program is $100,000 for contents (actual cash value) and $250,000 for buildings."; "…policyholders might consider purchasing 'excess' flood insurance to cover losses that exceed the limits of NFIP or Private Market Flood insurance."; FEMA grant limits "Up to $36,000 to replace the home (only offered under limited conditions)."
- Lender acceptance: Yes (requirement only) — "If you live in a flood zone and have a mortgage, your lender most likely requires flood insurance." No private-acceptance discussion.
- Short note: Contains the useful California 24-month ALE statute reference (homeowners) plus FEMA's $36,000 grant cap — good contrast material for a "FEMA aid is not a substitute" section.

#### The Zebra — https://www.thezebra.com/homeowners-insurance/coverage/additional-living-expenses-coverage/
- Query ranks: Q3=7
- Site type: comparison site
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "## Does flood insurance include additional living expenses coverage?" / "If you have a flood insurance plan through the NFIP, additional living expenses are **not covered**."; "Most homeowners policies provide ALE coverage at around **20 to 30%** of your dwelling coverage."; "Some premium home insurance companies — such as Chubb and AIG— do not cap the amount of money provided for additional living expenses."
- NFIP exclusion stated: NFIP-does-not — "If you have a flood insurance plan through the NFIP, additional living expenses are **not covered**."
- Placement: FAQ subsection deep in a homeowners-ALE page
- Other coverage comparisons: none for flood; homeowners percentages and 12–24-month time limits only
- Lender acceptance: No — not mentioned
- Short note: A high-authority comparison site answers the flood question in one FAQ line and never mentions private flood as the fix.

#### Progressive — https://www.progressive.com/answers/flood-101/
- Query ranks: Q3=8
- Site type: carrier
- Mentions LoU/ALE/temp housing: **No**
- Exact quote: not mentioned
- NFIP exclusion stated: n/a
- Placement: not present
- Other coverage comparisons: "The National Flood Insurance Program (NFIP) offers up to $250,000 in coverage for your home's structure and up to $100,000 for your belongings."; "Through the NFIP, homes are covered on a replacement cost basis while your personal property is insured for the actual cash value."; "If you choose a private insurer for flood insurance, they may cover your personal property at replacement cost."
- Lender acceptance: Yes (requirement only) — "As a condition of the loan, your mortgage lender may require you to purchase a flood policy if you live in a high-risk area."
- Short note: A national carrier ranks on the living-expenses query with a page that never mentions living expenses. Pure gap.

#### NC Department of Insurance (NFIP Summary of Coverage) — https://www.ncdoi.gov/nfip-summarycoverage/open
- Query ranks: Q3=9
- Site type: government (hosting FEMA's brochure)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "● Living expenses such as temporary housing." and "● Financial losses caused by business interruption or loss of use of insured property."
- NFIP exclusion stated: NFIP-does-not — the two bullets above appear in the SFIP "what is not covered" list
- Placement: official not-covered bullet list
- Other coverage comparisons: "Building Property, up to $250,000, and 2. …"; "General Guidance on Flood Insurance Coverage Limitations In Areas Below the Lowest Elevated Floor and Basements"; "● Drywall for walls and ceilings (in basements only)."; RCV vs ACV explanation ("It is not a guaranteed replacement cost policy.")
- Lender acceptance: No — only "or lender about raising or lowering deductibles."
- Short note: This is FEMA's Summary of Coverage text, hosted on a state DOI domain — a second citable government wording of the exclusion.

#### FEMA — Recovering Financially After a Flood (booklet PDF) — https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-recovering-financially-after-a-flood-booklet-01-2025.pdf
- Query ranks: Q3=10
- Site type: government
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "ADDITIONAL LIVING EXPENSES (ALE)" / "ALE coverage is not a separate service or insurance policy type but a standard part of many homeowners or renters insurance policies. It may provide money to cover lodging costs when you are unable to live in your home due to a disaster." / "**The NFIP does not cover ALE.** Review your homeowners or renters insurance policy to determine if this applies, or contact your insurance company."
- NFIP exclusion stated: NFIP-does-not — "The NFIP does not cover ALE."
- Placement: dedicated ALE section (page 10 of the booklet)
- Other coverage comparisons: "Form covers up to $250,000 for a building and up to $100,000 for…"; "Coverage limits are adjusted annually based on the U.S. …"; SBA disaster-loan and grant discussion
- Lender acceptance: No — not mentioned
- Short note: **The strongest possible citation for the agency's argument, in five words, from FEMA, dated January 2025.** Note it redirects the reader to homeowners/renters insurance and never mentions private flood — which is exactly the confusion your page can resolve.

#### 1800Insurance — https://www.1800insurance.com/guides/california-flood-insurance
- Query ranks: Q4=1
- Site type: aggregator / lead-gen
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Some private policies cover additional living expenses if you're displaced by flooding—something NFIP doesn't offer."; then later: "Neither NFIP nor most private policies cover temporary housing costs if flooding forces you out of your home—though some private insurers are starting to include this as additional living expense coverage."; "Ask specifically about basement coverage, additional living expenses, and whether the policy pays replacement cost or actual cash value."
- NFIP exclusion stated: fudges (self-contradictory) — first "something NFIP doesn't offer," then "Neither NFIP nor most private policies cover temporary housing costs"
- Placement: two separate body paragraphs
- Other coverage comparisons: "NFIP policies cover up to $250,000 for your home's structure and up to $100,000 for contents."; "coverage limits often reach $1 million or more"; "Private insurers offer shorter waiting periods—sometimes as little as 15 days, and occasionally immediate coverage for certain situations."; "Under NFIP rules, flood insurance doesn't cover personal belongings stored in basements—even if you have contents coverage."; "Private flood insurance costs average slightly more than NFIP at about $87 monthly versus $78…"
- Lender acceptance: Yes — "Private flood insurance has emerged as a real alternative in recent years, and since 2019, federal law requires mortgage lenders to accept qualifying private policies." (no "at least as broad as", no statutory definition, no compliance aid)
- Short note: **The #1 result for the California query actively misinforms** — it tells California homeowners private flood mostly doesn't cover temporary housing. That is the most attackable claim found in this survey.

#### TSM Insurance — https://www.tsminsurance.com/resources/flood-insurance-california-options
- Query ranks: Q4=3
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "|Temporary Living Expenses|Generally not covered|May be available with some policies|"; "### Does flood insurance cover temporary living expenses?" / "Standard NFIP policies generally do not include coverage for additional living expenses if a home becomes uninhabitable after a flood."; "- Additional living expense coverage."
- NFIP exclusion stated: fudges — "Generally not covered" / "generally do not include"
- Placement: comparison table row + FAQ
- Other coverage comparisons: "|Building Coverage|Up to $250,000|Often higher limits available|"; "|Personal Property Coverage|Up to $100,000|Higher limits may be available|"; "|Replacement Cost Options|Limited|May offer broader replacement cost coverage|"; "|Waiting Period|Typically 30 days|May vary by carrier|"
- Lender acceptance: Yes (requirement only) — "Flood insurance is generally required by mortgage lenders when a home is located in a designated Special Flood Hazard Area and the loan is backed by a federally regulated or insured lender." No private-acceptance rule cited.
- Short note: Everything hedged to the point of uselessness ("Generally," "May," "Often"). No dollar figures on either side of the private column.

#### Bollinsure — https://www.bollinsure.com/guides?g=flood-earthquake-insurance-california
- Query ranks: Q4=4
- Site type: broker (California)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "- **Private flood insurance** — increasingly available, often with higher limits, replacement cost on contents, and additional-living-expense coverage the NFIP doesn't provide."; "Coverage generally includes the dwelling, personal property, and loss of use (additional living expense), with options to tailor each." (the latter describes earthquake/DIC coverage)
- NFIP exclusion stated: NFIP-does-not — "additional-living-expense coverage the NFIP doesn't provide"
- Placement: body bullet (one subordinate clause)
- Other coverage comparisons: "**The National Flood Insurance Program (NFIP)**, administered by FEMA — the baseline market, but with limits capped at **$250,000 for the building and $100,000 for contents** on a residential policy."; "There's typically a **30-day waiting period** before coverage takes effect, so you can't buy it as a storm approaches."; "High-value homeowners typically secure meaningful flood and earthquake limits through **private-client carriers** and **Difference-in-Conditions (DIC)** policies"; "On a $1,000,000 dwelling limit, a 15% deductible is $150,000." (earthquake)
- Lender acceptance: No — not mentioned
- Short note: A California broker gets the NFIP exclusion right in half a sentence, then spends the page on earthquake deductible math. The ALE point is not developed at all.

#### California Flood Insurance (private flood vs FEMA) — https://californiafloodinsurance.com/private-flood-insurance-vs-fema/
- Query ranks: Q4=5
- Site type: broker (the client)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "**Loss of use.** The NFIP does not pay for you to live somewhere else while your home is repaired."; "Our guide to loss of use in flood insurance goes through how it is triggered."
- NFIP exclusion stated: NFIP-does-not — "The NFIP does not pay for you to live somewhere else while your home is repaired."
- Placement: bolded body bullet
- Other coverage comparisons: "**Building limits.** The NFIP caps residential building coverage at $250,000 and contents at $100,000."; "If you are already at the NFIP maximum and still underinsured, excess flood insurance is the other route to the same place."; "**Waiting period.** A new NFIP policy takes 30 days to take effect, counted from the day you buy it rather than the day the storm arrives."
- Lender acceptance: No — not mentioned
- Short note: Correct and crisp, but loss of use is listed after building limits — consider promoting it to the lead and adding a dollar example, since no competitor on this SERP has one.

#### Policygenius (California flood insurance) — https://www.policygenius.com/homeowners-insurance/flood-insurance-california/
- Query ranks: Q4=7
- Site type: comparison site / lead-gen
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "This includes loss of use coverage to help cover the cost of lodging or restaurant meals in the event your house is badly damaged and you're forced to evacuate; or replacement cost coverage for your personal belongings."; "|Loss of use coverage|No|Yes|"
- NFIP exclusion stated: NFIP-does-not (table) — "|Loss of use coverage|No|Yes|"
- Placement: comparison table row + body sentence
- Other coverage comparisons: "The maximum building property coverage limit with the NFIP is $250,000, meaning that's the most the NFIP will reimburse you for repairs, regardless of the damage amount."; "|Maximum home rebuild limit|$250,000|Typically up to $500,000 or higher|"; "|Waiting period|30 days|As little as two weeks|"; "|Replacement cost contents coverage|No|Yes|"; "|Availability|Every county except Mariposa|May be limited in high-risk areas|"
- Lender acceptance: Yes — "|Accepted by mortgage lenders|Yes|Yes|" and "your mortgage lender may require this coverage if you live in a high-risk flood zone according to Federal Emergency Management Agency (FEMA) maps." No statutory-definition or as-broad-as language.
- Short note: Highest-authority page on the California SERP with a loss-of-use row and a real California data point ("approximately 506,137 in California in a FEMA-designated high-risk flood zone") — but no ALE dollars.

#### Aon Edge — https://www.aonedge.com/Resource-Center/Blog/What's-the-Difference-Between-The-NFIP-and-PFI
- Query ranks: Q4=8
- Site type: broker / program manager
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Carriers may also include additional coverages, such as additional living expenses, which are not offered by the NFIP."
- NFIP exclusion stated: NFIP-does-not — "additional living expenses, which are not offered by the NFIP"
- Placement: body (single line)
- Other coverage comparisons: "Several insurance carriers have entered the market as risk takers, many of whom offer higher limits, additional coverages, and sometimes lower rates."; "Excess Flood"
- Lender acceptance: Yes — "Yes, per the Biggert-Waters Act, requires institutions to accept private flood insurance that meets both the statutory definition and the mandatory purchase requirement." and "…effective July 1, 2019, established the framework for institutions to evaluate whether a flood insurance policy meets the statutory definition of private flood insurance." — explicitly invokes the **statutory definition**; no compliance-aid assurance clause quoted.
- Short note: Best lender-compliance language on the California SERP, weakest loss-of-use development (one clause).

#### Blake Insurance Group — https://blakeinsurancegroup.com/best-flood-insurance-company-california/
- Query ranks: Q4=10
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "|**Additional living expense**|Not treated like a homeowners loss-of-use benefit|May be available as an optional private flood feature|Temporary housing and displacement costs after flood damage|"; "|**Loss of use / temporary living**|Whether additional living expense coverage is available|Flood damage can force you out while repairs are completed|Consider private flood options if displacement protection matters|"; "A private flood quote is especially important when … a homeowner wants to compare additional living expense options…"
- NFIP exclusion stated: fudges — "Not treated like a homeowners loss-of-use benefit" (never says the NFIP pays nothing)
- Placement: comparison table rows (two of them)
- Other coverage comparisons: "|**Building limit**|Standard residential NFIP building limits apply|Private flood may offer higher available building limits|…"; "|**Waiting period**|Often 30 days unless an exception applies|Private waiting periods can be shorter depending on carrier and rules|…"; "|**Basements / enclosures**|Special limitations can apply|Private terms vary by carrier and property design|…"; "|**Neptune Flood**|…Fast quote path, higher available limits, optional coverages…|"
- Lender acceptance: Yes — "|**Lender acceptance**|Widely accepted when compliant with lender and federal requirements|Often accepted when the policy meets lender requirements|Get lender approval before closing or replacing an NFIP policy|" (no statutory definition, no as-broad-as, no compliance aid)
- Short note: Two ALE table rows and still no clear statement of the exclusion — the vaguest treatment among pages that do mention it. Notably never states a single NFIP dollar limit.

#### FEMA — https://www.fema.gov/flood-insurance
- Query ranks: Q5=1
- Site type: government
- Mentions LoU/ALE/temp housing: **No**
- Exact quote: not mentioned
- NFIP exclusion stated: n/a
- Placement: not present
- Other coverage comparisons: "Plan ahead as there is typically a 30-day waiting period for an NFIP policy to go into effect, unless the coverage is mandated it is purchased as required by a government backed lender or is related to a community flood map change."; "- What Does Flood Insurance Cover In A Basement?"
- Lender acceptance: Yes (requirement only) — "Homes and businesses in high-risk flood areas with mortgages from government-backed lenders are required to have flood insurance."
- Short note: FEMA holds rank #1 for `loss of use flood insurance` with a page that never uses the term. The exclusion language lives one or two clicks deeper (agents.floodsmart.gov, Summary of Coverage) — an information-scent gap you can exploit.

#### The Flood Insurance Guru (video blog: what's loss of use) — https://www.floodinsuranceguru.com/floodvideoblog/whats-loss-of-use-in-flood-insurance
- Query ranks: Q5=2
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "When it comes to the National Flood Insurance Program's (NFIP) flood coverage, it's very unlikely that you have this included since there should be a presidential declaration filed in order for loss of use to be available."; "Loss of use coverage can be provided by the National Flood Insurance Program and Federal Emergency Management Agency (FEMA) through the disaster assistance or disaster relief program."; "On the other hand, the private market generally includes loss of use with their flood insurance coverage upon the purchase of flood policy."; "…you can't get in your home for five to six months since it's not a safe place to stay…"
- NFIP exclusion stated: fudges (and inaccurate) — "it's very unlikely that you have this included since there should be a presidential declaration filed in order for loss of use to be available" conflates FEMA disaster assistance with NFIP policy coverage
- Placement: headline + body
- Other coverage comparisons: none
- Lender acceptance: No — not mentioned
- Short note: The #2 result for the core query is factually muddled — it implies NFIP loss of use exists under a presidential declaration. A clean, correct page should outrank it.

#### Intermap — https://www.intermap.com/risks-of-hazard-blog/2015/11/whats-loss-of-use-good-question
- Query ranks: Q5=4
- Site type: other — geospatial risk-data vendor
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "National Flood Insurance Program policies do NOT cover loss of use."; "If your home floods, and you're one of the minority who actually has flood insurance, you will not be able to claim any loss-of-use expenses."; "Loss of use is an example of the coverage gap that needs to be filled by a responsive insurance industry."; "The American Insurance Association defines loss of use as the extra expenses incurred because of property damage."
- NFIP exclusion stated: NFIP-does-not — "National Flood Insurance Program policies do NOT cover loss of use."
- Placement: headline + body
- Other coverage comparisons: "Policies from the California Earthquake Authority offer loss of use for a little additional premium. The terms are okay, too, with no deductible and a standard limit of $25,000." (this $25,000 is **CEA earthquake**, not flood)
- Lender acceptance: No — not mentioned
- Short note: An 11-year-old vendor blog holds rank #4 with the most emphatic exclusion statement on the SERP — and it does not sell insurance. Strong evidence of how weak this SERP is.

#### Forever Florida Insurance — https://foreverfloridainsurance.com/private-flood-insurance-with-loss-of-use/
- Query ranks: Q5=5
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "That gap is where **private flood insurance with loss of use** becomes one of the most important policy features you can buy, and one of the least understood."; "|Loss of use|Often included|Standard policy excludes it|"; "Statewide Flood Insurance notes that private flood policies routinely include loss of use while NFIP policies exclude it, and after Hurricane Sandy, NFIP claimants faced uncompensated ALE costs averaging $15,000 to $25,000 per household."; "Verisk's flood market modeling assumes loss of use at 30% of insured value, with personal property at 50% and insured value at 80% of market value."; "- **Low caps for temporary housing** in markets where local housing is tight after a storm"
- NFIP exclusion stated: NFIP-does-not — "|Loss of use|Often included|Standard policy excludes it|" and "NFIP policies exclude it"
- Placement: headline + comparison table row + extensive body sections
- Other coverage comparisons: "|Lender acceptance|Can qualify if not narrower than NFIP|Accepted standard|"; "Moody's highlights that private policies may exclude business interruption for rentals unless specifically endorsed, potentially costing an owner in a prime Florida location $5,000 to $15,000 per month in lost revenue during peak season."; ALE fine-print checklist ("Any sub-limits for hotels, meals, or storage")
- Lender acceptance: Yes — "Consumer Compliance Outlook explains that under the 2024 federal rule, lenders must accept qualifying private flood policies if they are 'not narrower' than the NFIP, and compliant private policies can include loss of use that helps protect borrowers from displacement debt." — uses **"not narrower"** (a variant of "at least as broad as"); no compliance-aid clause. (Note: the "2024 federal rule" date is questionable; the joint rule is effective July 1, 2019.)
- Short note: The most complete loss-of-use sales page found anywhere in this survey — and it is Florida-specific and cites Statewide Flood Insurance. Its ALE fine-print checklist and the Sandy $15k–$25k figure are the two best assets on the SERP.

#### Farmers Insurance — https://www.farmers.com/learn/insurance-questions/loss-of-use-coverage/
- Query ranks: Q5=6
- Site type: carrier
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Even if you have flood insurance through FEMA's National Flood Insurance Program, loss of use coverage is not covered by your home policy, according to the III."; "Loss of use coverage on a homeowners insurance policy typically equals 20% of your dwelling coverage, according to the Insurance Information Institute (III). So if you insure your home for $200,000, your loss of use coverage limit would be $40,000."
- NFIP exclusion stated: fudges — the sentence is garbled ("loss of use coverage is not covered by your home policy") and never plainly says the NFIP itself pays nothing
- Placement: "What is not covered by loss of use coverage?" section
- Other coverage comparisons: none for flood; homeowners/condo/renters ALE math only ("Condo insurance typically provides loss of use coverage that adds up to 20% of your unit owner's building coverage and personal property coverage combined.")
- Lender acceptance: No — not mentioned
- Short note: The clearest homeowners ALE benchmark math on the SERP (20% / $40,000) attached to the muddiest flood sentence.

#### Hippo — https://www.hippo.com/learn-center/loss-of-use-coverage
- Query ranks: Q5=7
- Site type: carrier
- Mentions LoU/ALE/temp housing: Yes (homeowners only)
- Exact quote: "Loss of Use coverage, also known as Additional Living Expenses (ALE) coverage or coverage D, is a form of financial assistance for homeowners."; "Most providers limit the Loss of Use coverage to 20% of their dwelling coverage."; "In the event of damage to your house due to a natural disaster like a hurricane or wildfire, Loss of Use coverage helps cover costs for temporary accommodation, food, transportation, and clothing while your property is being repaired."
- NFIP exclusion stated: not stated — neither "flood," the NFIP, nor FEMA is addressed in relation to ALE
- Placement: headline + body (homeowners context)
- Other coverage comparisons: none
- Lender acceptance: No — not mentioned
- Short note: Ranks #7 for a flood query with zero flood content — again evidence the flood intent is unmet.

#### FloodPrice — https://www.floodprice.com/post/what-is-loss-of-use-coverage
- Query ranks: Q5=8
- Site type: aggregator / private-flood quoting platform
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "## Does an NFIP Policy cover Loss of Use?" / "**The National Flood Insurance Program does not offer additional living expense coverage on their policies.** If you have an __NFIP policy__ and your home becomes uninhabitable due to flood damage, overcrowded shelters may not be an option."; "**Yes, this coverage is an option with FloodPrice's private flood insurance!**"; "Our __online quoting system__ scans multiple private carriers who offer additional living expense coverage to make sure you are getting the best option."
- NFIP exclusion stated: NFIP-does-not — "The National Flood Insurance Program does not offer additional living expense coverage on their policies."
- Placement: headline + dedicated H2 ("Does an NFIP Policy cover Loss of Use?")
- Other coverage comparisons: none — the page compares nothing else
- Lender acceptance: No — not mentioned
- Short note: **The only true third-party competitor executing the exact play the agency is considering** — headline, NFIP exclusion in bold, immediate private-flood CTA. It is short (~2,900 characters), has no dollar figures, no state focus, and no displacement math. Beatable.

#### Cornell LII — SFIP, 44 CFR Pt. 61 App. A(1) — https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61
- Query ranks: Q5=9
- Site type: government / legal text (Dwelling Form of the Standard Flood Insurance Policy)
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Loss of use of the insured property or described location;" and "Any additional living expenses incurred while the insured building is being repaired or is unable to be occupied for any reason;" (both appear in the policy's list of losses not covered)
- NFIP exclusion stated: NFIP-does-not — the two exclusion clauses above are the operative policy language
- Placement: policy exclusions section (deep in a 75,000-character legal text)
- Other coverage comparisons: "However, no more than $250,000 may be paid in combined benefits for a single unit under the Dwelling Form policy and the RCBAP."; "Coverage is limited to no more than 10 percent of the limit of liability on the dwelling."; basement coverage limited to enumerated items ("(3) Drywall for walls and ceilings in a basement…"); "Increased Cost of Compliance coverage will not be included in the calculation to determine whether coverage meets the 80 percent insurance-to-value requirement…"
- Lender acceptance: No — not mentioned
- Short note: **This is the primary-source citation** — the actual SFIP exclusion wording. Nobody on any of the five SERPs quotes it. Quoting the policy form verbatim on your page would be a differentiator no competitor has.

#### Statewide Flood Insurance (loss of use) — https://statewidefloodinsurance.com/loss-of-use-coverage-in-flood-insurance/
- Query ranks: Q5=10
- Site type: broker
- Mentions LoU/ALE/temp housing: Yes
- Exact quote: "Unfortunately, the National Flood Insurance Program (NFIP) does not offer loss of use coverage, making private flood insurance policies a vital consideration for comprehensive protection."; "While NFIP flood insurance policies provide crucial support for repairing physical damage to your home and belongings, they fall short by not offering loss of use coverage."; "Without loss of use coverage, the financial impact of such extended displacements can be devastating, potentially leading to significant debt or even bankruptcy for affected homeowners."; "Cal Flood Insurance Services offers multiple carriers that offer loss of use coverage."
- NFIP exclusion stated: NFIP-does-not — "the National Flood Insurance Program (NFIP) does not offer loss of use coverage"
- Placement: headline + body throughout
- Other coverage comparisons: "Moreover, private insurers may provide more flexibility in coverage limits and terms…" (no figures)
- Lender acceptance: No — not mentioned
- Short note: Affiliated with the client ("Cal Flood Insurance Services"). Correct and prominent, but entirely qualitative — no dollar limits, no displacement duration, no California housing-cost data.

---

## Section D — Quantification inventory

**Flood-specific loss-of-use / ALE dollar figures (the only ones found — five pages):**

1. "the loss of use/rents of $7,500" — in a side-by-side claim example where the NFIP row reads "Not available." and the client "will pay $457,500 out of pocket plus deductibles." — [USI flood comparison chart (PDF)](https://www.usi.com/siteassets/images/insights/prs/q4-2022/flood-comparison-chart-2.pdf)
2. "Private policies routinely include loss-of-use coverage; Chubb's base flood form includes $7,500 with higher limits available." — [Latent Insurance](https://www.latentinsure.com/blog/nfip-vs-private-flood-insurance)
3. "Most private flood insurance policies include Additional Living Expenses coverage up to $25,000, depending on the provider." — [The Flood Insurance Guru](https://www.floodinsuranceguru.com/the-flood-insurance-guru-blog/why-do-i-need-additional-living-expenses-on-my-flood-insurance)
4. "after Hurricane Sandy, NFIP claimants faced uncompensated ALE costs averaging $15,000 to $25,000 per household" and "Verisk's flood market modeling assumes loss of use at 30% of insured value, with personal property at 50% and insured value at 80% of market value." — [Forever Florida Insurance](https://foreverfloridainsurance.com/private-flood-insurance-with-loss-of-use/)
5. "Loss of use limits on private policies are usually expressed as a dollar cap or as a percentage of your dwelling coverage, often somewhere around 10% to 20%." — [California Flood Insurance (client)](https://californiafloodinsurance.com/loss-of-use-coverage-in-flood-insurance/)

**Worked displacement examples (two):**

6. "- **No additional living expenses.** If a flood makes your home uninhabitable for six months, the NFIP pays $0 toward rent, hotels, or meals, per FEMA's Summary of Coverage." and "Families who cannot self-fund six months of temporary housing should not carry a policy that pays $0 for it." — [Latent Insurance](https://www.latentinsure.com/blog/nfip-vs-private-flood-insurance)
7. "your house has been flooded, and due to this major flooding you can't get in your home for five to six months since it's not a safe place to stay, you're most likely going to stay at another place — maybe an apartment or hotel." — [The Flood Insurance Guru](https://www.floodinsuranceguru.com/floodvideoblog/whats-loss-of-use-in-flood-insurance)

**Homeowners-insurance ALE benchmarks (NOT flood — do not present as flood figures):**

8. "Loss of use coverage on a homeowners insurance policy typically equals 20% of your dwelling coverage, according to the Insurance Information Institute (III). So if you insure your home for $200,000, your loss of use coverage limit would be $40,000." — [Farmers](https://www.farmers.com/learn/insurance-questions/loss-of-use-coverage/)
9. "Your homeowners policy's ALE coverage is usually equal to 20 percent of your home's insured value—a home insured for $200,000, for instance, may have ALE coverage of up to $40,000—or limited to a certain timeframe (e.g., no more than 12 months)." — [III](https://insuranceindustryblog.iii.org/relocated-property-damaged-by-ida-you-may-be-eligible-for-additional-living-expenses/)
10. "Most homeowners policies provide ALE coverage at around **20 to 30%** of your dwelling coverage." and "Some premium home insurance companies — such as Chubb and AIG— do not cap the amount of money provided for additional living expenses." — [The Zebra](https://www.thezebra.com/homeowners-insurance/coverage/additional-living-expenses-coverage/)
11. "For example, if your home is insured for $300,000, and the limit for additional living expenses on your policy is 30 percent, then you would be allowed up to $90,000 to spend on hotel bills, rent, etc." and "In California, policyholders get at least 24 months to spend additional living expenses coverage, but other states set lower limits (12 months, in many cases)." — [Consumer Action](https://www.consumer-action.org/english/articles/disaster_insurance_and_fema_assistance)
12. "Generally, home insurance caps additional living expenses to a portion of the dwelling coverage, typically 20%, Swerling says, and sets a time limit, such as 12 months." / "So if your home is insured for $200,000, then you have up to $40,000 to spend on additional living expenses." / "In California, home insurers must give policyholders at least 24 months to spend additional living expenses coverage." — [Fox Business](https://www.foxbusiness.com/features/home-sweet-temporary-home)
13. "Most providers limit the Loss of Use coverage to 20% of their dwelling coverage." — [Hippo](https://www.hippo.com/learn-center/loss-of-use-coverage)

**Adjacent figures worth knowing (not flood ALE):**

14. "Policies from the California Earthquake Authority offer loss of use for a little additional premium. The terms are okay, too, with no deductible and a standard limit of $25,000." — [Intermap](https://www.intermap.com/risks-of-hazard-blog/2015/11/whats-loss-of-use-good-question) (CEA earthquake, not flood)
15. "Moody's highlights that private policies may exclude business interruption for rentals unless specifically endorsed, potentially costing an owner in a prime Florida location $5,000 to $15,000 per month in lost revenue during peak season." — [Forever Florida Insurance](https://foreverfloridainsurance.com/private-flood-insurance-with-loss-of-use/)
16. "With a limit of $36,000, FEMA disaster grants may be insufficient to repair or rebuild your home." and "- A temporary housing unit (mobile home, manufactured home, etc.) for up to 18 months if rental properties are not available." — [Consumer Action](https://www.consumer-action.org/english/articles/disaster_insurance_and_fema_assistance)

**Bottom line for Section D:** across 44 pages, exactly **three** distinct private-flood ALE limits appear ($7,500 ×2 sources, $25,000, and "10%–20%"/"30% of insured value" as percentages), and **zero** pages price a California displacement (months × Bay Area/LA rent differential) against the NFIP's $0.

---

## Section E — FEMA / FloodSmart baseline

The agency's premise is correct, and FEMA states it in at least four separate official documents. Exact wording:

1. **FEMA, "Recovering Financially After a Flood" (NFIP booklet, Jan 2025)** — under the heading "ADDITIONAL LIVING EXPENSES (ALE)": "ALE coverage is not a separate service or insurance policy type but a standard part of many homeowners or renters insurance policies. It may provide money to cover lodging costs when you are unable to live in your home due to a disaster." followed by: **"The NFIP does not cover ALE. Review your homeowners or renters insurance policy to determine if this applies, or contact your insurance company."** — [agents.floodsmart.gov PDF](https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-recovering-financially-after-a-flood-booklet-01-2025.pdf) (this page ranked Q3 #10)

2. **FEMA / FloodSmart agent talking points, "What Is Covered by A Flood Insurance Policy for Homeowners?"** — under "**What isn't covered?** There are specific items not covered by a building or contents coverage policy. These include:" → **"- Temporary housing and additional living expenses incurred while the building is being repaired or is unable to be occupied."** — [agents.floodsmart.gov](https://agents.floodsmart.gov/articles/what-covered-flood-insurance-policy-homeowners) (ranked Q3 #4)

3. **FEMA, NFIP Summary of Coverage brochure (P-2144, Dec 2023)** — under "WHAT IS NOT COVERED BY MY FLOOD INSURANCE? … Examples of uncovered or excluded losses:" → **"• Additional living expenses such as temporary housing"** and **"• Financial losses caused by business interruption or loss of use of insured property"** — [agents.floodsmart.gov PDF](https://agents.floodsmart.gov/sites/default/files/media/document/2025-07/fema-nfip-summary-coverage-brochure-12-2023.pdf). The same FEMA text, in an older layout hosted by the NC Department of Insurance, reads: **"● Living expenses such as temporary housing."** and **"● Financial losses caused by business interruption or loss of use of insured property."** — [ncdoi.gov](https://www.ncdoi.gov/nfip-summarycoverage/open) (ranked Q3 #9)

4. **The policy form itself — Standard Flood Insurance Policy, Dwelling Form, 44 CFR Pt. 61 App. A(1)**, list of losses not covered: **"Loss of use of the insured property or described location;"** and **"Any additional living expenses incurred while the insured building is being repaired or is unable to be occupied for any reason;"** — [Cornell LII](https://www.law.cornell.edu/cfr/text/44/appendix-A(1)_to_part_61) (ranked Q5 #9). This is the strongest, most literal citation available and no commercial page in the survey quotes it.

**Control pages that did NOT contain the wording:**
- [https://www.floodsmart.gov/](https://www.floodsmart.gov/) — fetched (5,471 characters). No mention of loss of use, ALE, temporary housing, or living expenses. It says only: "In the event of a flood, your NFIP policy covers direct physical losses to your structure and belongings."
- [https://www.floodsmart.gov/whats-covered](https://www.floodsmart.gov/whats-covered) — fetched, but returned only 385 characters of .gov site boilerplate with no coverage content (the substantive lists are delivered client-side / via the linked Summary of Coverage PDFs). An LLM extraction over the fetched content confirmed: "No sentences or bullets mentioning additional living expenses, temporary housing, living expenses, or loss of use appear in the provided page content."
- `https://www.floodsmart.gov/flood-insurance/what-covered` — **not verified — fetch failed** (HTTP client error / 404).
- [https://www.fema.gov/flood-insurance](https://www.fema.gov/flood-insurance) — fetched (4,561 characters). No mention of loss of use, ALE, or temporary housing anywhere on the page, despite ranking #1 for `loss of use flood insurance`.

**Practical implication:** the citable FEMA sentence ("The NFIP does not cover ALE.") lives in a PDF and an agent-facing article, not on floodsmart.gov's consumer pages — so a consumer searching this question cannot easily find FEMA saying it. That is part of why the SERP is soft.

---

## Section F — Method notes and caveats

- All five queries returned 10 organic-style results; no query had fewer than 10. 50 result slots → 44 unique URLs (6 duplicate appearances across queries).
- Every one of the 44 was fetched successfully and every quote above was taken from the fetched text (stored in `/home/user/workspace/job2_pages/`). No claim in this report comes from memory or from a search snippet.
- Placement classifications are based on the fetched page structure (markdown table rows = comparison table; `#`/`##` lines = headline/section heading; FAQ headings = FAQ). Where a page mentions loss of use in more than one place, all placements are listed.
- Site-type calls: "broker" = licensed agency selling policies; "aggregator/lead-gen" = quote-engine or lead site; "comparison site" = editorial/insurtech comparison publisher; "carrier" = insurer/MGA; "other" = law firm, forum, nonprofit, trade body, or vendor.
- Three ranking sites in this data set are the client's own or affiliated with it (californiafloodinsurance.com ×2, statewidefloodinsurance.com ×2, and foreverfloridainsurance.com, which cites "Statewide Flood Insurance"). Excluding them, the third-party competitive field making a headline loss-of-use argument in a flood context is just FloodPrice.com and The Flood Insurance Guru.
