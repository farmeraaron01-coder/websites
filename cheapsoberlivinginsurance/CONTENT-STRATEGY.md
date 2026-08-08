# Content strategy — cheapsoberlivinginsurance.com

Drafted 7 Aug 2026. Supersedes the NARR-heavy content map proposed earlier the same day, which was wrong
and is explained below.

---

## 1. The reader

Not a commercial insurance buyer. In Aaron's words:

> Many sober living operators were themselves in treatment, and there was such a profound change in their
> life that they want to give back, so they open sober living homes. In many cases, that doesn't make them
> business owners.

Everything on this site follows from that sentence. The reader is:

- **Mission-driven, not commercially trained.** They opened a home because recovery worked for them. They
  did not open it because they wanted to run a small business, and nobody handed them a manual.
- **Probably wrongly insured right now**, not uninsured on purpose. A homeowners or landlord policy that
  excludes business activity, multiple unrelated occupants and professional services is the common
  starting point — and they do not know it until a claim.
- **Genuinely price-sensitive.** Margins are thin and often personal. The "cheap" domain is not a cynical
  hook for this audience; it is accurate targeting.
- **Facing a vocabulary problem before a price problem.** A landlord or lender asks for a certificate of
  insurance naming them as additional insured with a waiver of subrogation, and the operator has no idea
  what was just requested. That confusion, not premium, is often what stalls the deal.

**So the content's job is to teach, then quote.** Not to sell coverage to someone who already knows what
they want.

### The positioning this produces

> Competitive on price because we know the margins are thin. Serious about coverage because an operator
> has more at stake than a landlord does — the home, the business, and the people living in it.

That is the honest version of a "cheap" domain, and it is defensible: the reason to care about exclusions
is not upsell, it is that an uncovered claim ends the mission.

### The site's thesis, in one sentence

> Operators believe they are providing housing. They are providing housing **and guidance**. Insurance
> priced for housing does not cover guidance.

Every page is an instance of that gap. It is why a homeowners policy fails, why general liability is not
enough, why professional liability costs more, and why abuse and misconduct is written separately. State it
once on the start-here page and let the other pages inherit it rather than repeating it.

---

## 2. Voice rules

Binding on every page. The landlord plan's jargon rule, extended for this audience.

- **Never assume commercial insurance literacy.** No page may open with a term the reader has to already
  know.
- **Define terms in the sentence, not in a parenthesis.** "A certificate of insurance — the one-page proof
  your landlord is asking for —" reads better than "a certificate of insurance (COI)".
- **Plain English first, the industry term second**, and only where the industry term earns SEO value.
- **Never imply the operator is naive.** They are not; they are new to one specific domain. The tone is a
  specialist explaining their own field, not an expert correcting an amateur.
- **Acknowledge the mission without sentimentality.** One clear sentence beats a paragraph of warmth. The
  reason coverage matters is that the mission is fragile, and that point lands better stated plainly.
- **Banned:** leverage, solutions, robust, best-in-class, peace of mind, "we've got you covered."
- **Claims stay factual.** No implication that every coverage or carrier is available in every state —
  carried over from the flood sites, and doubly important where markets are genuinely limited.

---

## 3. What changed from the earlier proposal, and why

I proposed `/narr-levels-and-insurance/` as the spine, plus `/narr-certification-and-insurance/`, plus
NARR-derived state pages. That was over-built. Aaron's correction:

> some of our customers belong to NARR as it gives some credibility and shows the owner is engaged in the
> business. however, not all are members or will be. its just to be used as a guide for how some of these
> operations could and should be run like a business… we don't want to overdo it on NARR.

I rotated toward the taxonomy because it was intellectually tidy — four levels mapping cleanly onto four
exposure profiles. But NARR is **a guide, not a gatekeeper**, and most readers are not members. Building
the site's architecture on a standard the reader may never have heard of would fail the reader to satisfy
a framework.

**NARR keeps one page**, framed as what it actually is: a credible reference for running the home like a
business. The levels remain useful *internally* — as an underwriting shorthand and a quote-form question —
without becoming the site's public organizing idea.

### Book of business, confirmed

- **Core: the levels that are not treatment centers.** Peer-run, monitored and supervised homes.
- **Clinical/treatment settings can be placed**, but need a higher-level program. Worth one honest
  paragraph rather than silence: it captures the search traffic and it is true.
- Codex's line *"More than a rental. Not a treatment center."* stays — it describes the core book
  accurately. Add the clinical note nearby rather than softening the line.

---

## 4. Page map, in build order

Priority is by reader intent, not by coverage taxonomy.

### Tier 1 — build these first

**1. `/what-insurance-does-a-sober-living-home-need/`**
The start-here page, and the highest-intent page on the site for a new operator. Plain-English walkthrough
of what a home actually needs and why, in the order a person would ask. Links to every coverage page.
This is also the strongest AI-citation candidate on the site — it answers a question asked in exactly
those words.

**2. `/sober-living-insurance-cost/`** — already specified in `KADENCE-BUILD-GUIDE-REVISIONS.md` §D.
Ranges still need real figures from Aaron or underwriting.

**3. `/is-my-current-policy-enough/`**
The "you may be uninsured and not know it" page. The homeowners and landlord policy gap: business activity
exclusions, multiple unrelated occupants, professional services, loss of income. Written as a checklist
the reader can run against their own declarations page. This page converts, because it creates urgency
from a fact rather than a scare.

**4. `/abuse-and-molestation-coverage/`** — **DRAFTED**, see `pages/abuse-and-molestation-coverage.md`
The catastrophic exposure in residential recovery, commonly excluded from general liability and available
standalone. Aaron supplied carrier-side source copy written for brokers; rewritten for the operator and made
specific to this class.

**The framing trap on this page:** written as "protect yourself from accusations" it would repel a
mission-driven reader, and deserve to. It is written protecting residents first and the home second — the
coverage exists because a real incident is catastrophic for the people living there, and because a home doing
everything right can still face an allegation. Nowhere does it imply residents are likely to make false
claims.

Two additions not in the source material, both worth keeping:

- **Resident-to-resident is the claim shape operators least expect.** If one resident harms another, the
  claim against the home alleges failure in supervision, room assignment, house rules or response — not
  direct wrongdoing. The home can face a claim with no member of staff having done anything wrong. This is
  specific to communal living and generic copy misses it entirely.
- **The standard "screen your employees" advice is wrong for this industry.** Many of the best house managers
  are people in recovery and some have records; hiring them is often *why* the home works. So the advice is
  consistency and documentation rather than exclusion — a written process applied identically every time, a
  reasoned standard for what disqualifies, boundaries training that is documented, and employment-law
  questions pushed to an attorney rather than answered by a broker or a website.

**5. `/professional-liability/`** — **DRAFTED**, see `pages/professional-liability.md`
Aaron: *"as important as any."* Operators say "I'm not doing anything other than giving them a place to
stay", and the refutation is on their own website — they market lived experience and knowledge of what it
takes to recover, which is precisely holding yourself out as having expertise. The claim that arrives is not
a slip and fall; it is a relapse, a discharge dispute, a referral or advice given sincerely and outside
their training. General liability covers bodily injury and property damage and excludes professional
services, so it does not respond. It costs more than general liability, correctly, and this is the page that
has to earn that. Replaces the three-section stub in Codex's blueprints.

**6. `/how-to-get-approved-for-sober-living-insurance/`** — **DRAFTED**, see `pages/how-to-get-approved.md`
The submission page. Aaron's brief: one carrier specifically asks for a résumé or CV, association membership
helps, and a written business plan is the document operators skip and the one that most often changes the
outcome. Framed so it cannot read as gatekeeping — the underwriter never meets you and only reads the file,
so the job is getting what is already true about you onto paper. Recovery experience is treated as
experience rather than as biography, because a lot of these operators have a decade in this world and a
blank employment page. The business-plan outline in §2 is the artifact readers will actually use and is a
candidate for a gated download later. Step 5 — "send it to us before it goes to market" — is the conversion
mechanism, and it is a real offer rather than a form fill.

**7. `/sober-living-insurance-specialist/`** — **DRAFTED**, see `pages/why-a-specialist.md`
The trust page, and the only page on the site a competitor cannot copy. Aaron's brief: most agents and brokers
treat a recovery residence as a normal rental, do not spend the time to understand the risk, and are not
specialists in this class.

**The origin story is the whole page.** One of the agency's first customers brought in an apartment building;
it was written as a standard habitational risk; only later did they learn it was a sober living home. That is
what set the agency on the path to becoming niche experts. Told as a self-incriminating story it does what no
claim of expertise can — it makes the argument without looking down on the reader or on the reader's current
agent, and it cannot be echoed by another agency.

Two hard rules on this page. **Nothing may be added to the story that Aaron did not supply** — no year, no
state, no claim, no customer name, no suggestion anything went wrong on that policy. And **§4 is framed as
structural rather than as competitors being lazy**: most agents see a handful of these in a career and fewer
have the appointments to place one, which is both truer and more credible than criticism.

§3 is the sharpest argument the site makes — a policy describing an apartment building can be contested if the
property turns out to be a recovery residence. Written as *can*, dependent on facts and state law, with no
promise either way. Needs Aaron's sign-off.

This page is the link target for every other page's "my agent would have told me" moment. Link to it rather
than repeating the argument.

**8. `/certificates-and-what-your-landlord-requires/`**
Translation page. Certificate of insurance, additional insured, waiver of subrogation, loss payee,
minimum limits — each defined in plain language with a note on why the other party wants it. Solves the
vocabulary problem that stalls deals, and no competitor writes this for this audience.

### Tier 2 — coverage gaps worth their own pages

**9. `/commercial-auto-and-transporting-residents/`** — driving residents to meetings, appointments and
work is a core operation at most homes, and personal auto excludes business use. Hired and non-owned auto
matters when staff use their own cars, which is the common arrangement.

**10. `/fair-housing-and-zoning-liability/`** — recovery residences fight occupancy caps, zoning objections
and reasonable-accommodation claims constantly. Real, frequent, under-served by every competitor, and
highly searched by operators in the middle of a dispute.

**11. `/employment-practices-liability/`** — house managers, staff, terminations. Referenced once on the
workers' comp page as an exposure with no coverage attached.

**12. `/directors-and-officers/`** — many homes are nonprofits with boards. Absent entirely today.

Cyber, umbrella and building-ordinance coverage do not need standalone pages yet. Cover them inside the
start-here page and the cost page's factor table.

### Tier 3 — reference and reach

**13. `/sober-living-insurance-terms-explained/`** — plain-English glossary. Definitional, quotable,
genuinely useful to the reader, and the kind of passage-level content AI engines cite.

**14. `/recovery-residence-terminology/`** — sober living home vs halfway house vs recovery residence vs
transitional housing. High-volume definitional queries, and it clears up the confusion that makes these
submissions hard to underwrite.

**15. `/running-a-sober-living-home-like-a-business/`** — the single NARR page. Framed as Aaron framed it:
a guide to operating well, useful whether or not the reader ever joins. Covers governance, house rules,
documentation, incident response, staffing clarity — and notes that certification signals engagement to
underwriters without claiming it guarantees anything.

**16. `/states/[state]-sober-living-insurance/`** — phase 2 only, and only with genuinely distinct content
per state: whether the state licenses or certifies recovery residences, local occupancy and zoning
posture, and market availability. The distinct-content rule from the landlord plan applies. **Do not ship
a template with the state name swapped.** A network of thin near-duplicates is a ranking liability, not an
asset.

---

## 5. Where NARR is genuinely useful — internally

Not as public architecture, but as working tools:

**On the quote form.** A question about staffing and services — effectively "which level is this?" without
using the jargon — determines the coverage set before anything else is asked. Suggested phrasing:

> Which best describes the home?
> - Residents govern the house themselves; no paid staff
> - A house manager oversees the home
> - Trained or credentialed staff provide structured programming
> - Clinical treatment is provided on site

That is the NARR taxonomy in the reader's language, and it routes the submission correctly.

**In the cost factor table** (`REVISIONS.md` §D §1) — "services provided" and "staffing" are already rows;
this is what they mean in practice, and it is why two homes of the same size price differently.

---

## 6. AI/answer-engine specifics

- **A 40–60 word self-contained definitional passage near the top of every page**, phrased so it makes
  sense lifted out of context. House practice from the landlord plan, and the mechanism by which these
  pages get cited.
- **FAQPage schema on every page that renders FAQs.** Rank Math owns all schema; Kadence's block-level FAQ
  schema stays off. One owner, no duplication.
- **`llms.txt`** at the root listing canonical URLs with a one-line description each.
- **Question-shaped H2s** where the query is a question. "Does my homeowners policy cover a sober living
  home?" outperforms "Homeowners policy considerations."
- **Answer in the first sentence under the heading**, then explain. Answer engines and impatient readers
  want the same thing.

---

## 7. Market scarcity is a selling point, not a caveat

Aaron: *"Carrier appetite is a tricky one because there are not many carriers that write this type of
insurance… That is why people use us, because it's hard to find this coverage."*

So write scarcity as the reason a specialist matters, without naming carriers and without implying
guaranteed placement:

> There are not many markets for this class. That is the reason a specialist matters — not because we have a
> secret list, but because knowing which carriers actually understand a sober living risk saves you from
> collecting declinations.

**Answered:** abuse and molestation **is available as standalone coverage**, so the abuse page is written as
"here is a coverage to buy" *and* "check whether your general liability excludes it" — both, not one.

---

## 8. Still needed from Aaron

1. **Cost ranges** for the cost page — coming Monday, per Aaron.
2. **Carrier appetite, even by category** — which levels, which states, what disqualifies a submission. The
  copy stays honest only if it knows the boundaries.
3. ~~Whether abuse and molestation is standalone~~ **Answered: standalone is available.**
4. **Claims-made vs occurrence** on the professional liability forms these markets write, and whether
  defense sits inside or outside the limit. §5 of the drafted page currently hedges; it should be specific.
5. ~~How your markets treat an operator with a record~~ **Answered: go lightly.** Aaron: *"I don't want to get
  too deep into someone's records. We can go lightly over this. The idea is just to put in their head that
  they're going to need to submit something to us versus nothing."* Handled in three sentences in §4 of
  `pages/how-to-get-approved.md`. **This is now a standing rule for the site** — no page discusses specific
  offenses or how carriers weigh them. The reader is routed to a person, not to a rule.
6. **Phone number and email decision** — `858-295-7242` and `aaron.farmer@jumpins.com` are currently
  specified; the email in particular reads oddly on this domain.
7. **Sign-off on the origin story**, and permission to tell it publicly — the apartment building that turned
  out to be a sober living home. It carries `pages/why-a-specialist.md` and nothing in it may be embellished.
8. ~~How many years, specifically~~ **Answered: sober living "at least since 2008."** Public copy says
  **"since 2008"** — the conservative reading of Aaron's own words. **Always a year, never a count of years:**
  "since 2008" stays true forever, "eighteen years" is wrong next January and wrong in every AI answer that
  cached it. This is a site-wide fact — footer, About page, Organization schema. Still open: whether 2008 is
  also the agency's `foundingDate` or only the start of the specialty. Do not put it in schema as
  `foundingDate` until that is confirmed.
9. **The other resources** Aaron mentioned having.
