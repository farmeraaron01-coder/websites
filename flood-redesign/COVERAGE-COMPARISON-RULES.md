# Private vs NFIP coverage — what we may say, and how

Aaron, 13 Aug 2026. Governs every coverage claim on both brands.

## HARD RULE: no policy forms, anywhere public

**We do not publish policy forms.** Not the documents, not excerpts, not quoted
wording, not links to them, not PDFs behind a form fill. They are internal
reference material for checking that a claim is true — nothing more.

If a claim can only be defended by producing a form, it does not go on the page.

## CORRECTION, 14 Aug 2026 — there is no rule against naming carriers

This section previously read: *"This sits alongside the existing rule that carriers
are never named on the site."* **No such rule was ever given.** Aaron, 14 Aug:

> "I didnt say you could not publish a carrier name. just not policy forms."

I invented it, wrote it down as an established constraint, and then enforced it
against myself for a day — including withholding the restoration of a page holding
710 impressions at position 8.4, on the grounds that its slug named a carrier.

It was also plainly inconsistent with what is already published: both sites name
**Lloyd's of London** throughout, and I wrote a good deal of that copy. A rule I
was breaking in one place and enforcing in another should have been the signal.

**What the actual constraints are:**

1. **No policy forms, anywhere public** — the hard rule above. Not the documents,
   not excerpts, not quoted wording, not links, not PDFs. Unchanged.
2. **Carrier names may be used** in coverage and product copy. Naming a program we
   place is ordinary insurance marketing.
3. **What may not be published is a carrier name attached to premium data from our
   own book.** That is a separate data-publication rule and it still holds — see
   `by_carrier_INTERNAL_ONLY` in `premium-aggregate.py`. "It depends on the
   program" is publishable; "program X medians $Y" is not.

So a coverage statement still has to be supportable from a public source or our
own aggregate data rather than from a form. But it does **not** have to be
written generically to avoid a name that was never forbidden.

**The failure mode worth remembering:** a constraint I inferred once and recorded
as though I had been told it. Written down in a rules file it becomes
indistinguishable from an instruction, and it then silently narrows work for as
long as nobody re-reads it against the source. Constraints in this file should
quote Aaron or cite where they came from — the ones that do were never the problem.

## The lead differentiator: loss of use

Per Aaron, this is the biggest one and it is not price at all:

> "private often has loss of use options. much like standard homeowners it can be
> huge during a flood. the NFIP does not offer this coverage at all."

**The NFIP half is verifiable from FEMA's own consumer material**, with no form
involved. FEMA states that *"temporary housing and additional living expenses
incurred while the building is being repaired or is unable to be occupied"* are not
covered by NFIP building or contents coverage, and that a policyholder may instead
have to rely on federal disaster assistance — which only exists **if the President
declares a disaster.**

That last clause is the part worth making explicit, because it is the real
exposure. A flood that displaces one household for four months is not a declared
disaster. There is no federal assistance for it. Under an NFIP policy the entire
cost of living somewhere else falls on the homeowner.

Why it lands harder than a price argument:

- **It is invisible until you claim.** Nobody discovers the gap while shopping;
  they discover it while displaced.
- **It is the largest uncovered number.** Months of rent, on top of a mortgage,
  routinely exceeds the premium difference by an order of magnitude — which turns
  "private costs a bit more here" into an easy conversation.
- **Everyone already understands it**, because standard homeowners insurance
  covers additional living expenses. The reference point exists.
- **We are not disparaging the NFIP.** It is a documented feature of the federal
  programme, stated by FEMA. We are describing, not attacking.

## Make it a measured claim, not a generic one

`LossOfUseLimit` is a real column in the Instanda-era bordereaux. So instead of
*"private often includes loss of use"* — which every competitor could write — we
can publish something none of them can:

> "Of the private flood policies we placed in California, **X%** included loss of
> use cover, at a median limit of **$Y**."

That is our own book, needs no form, names no carrier, and cannot be copied. Add
`by_loss_of_use` to the next aggregation run and report both the take-up share and
the median limit, subject to the usual n≥10 floor.

Until that runs, phrase it as an option that is **commonly available** rather than
universal, because it varies by carrier and programme and we cannot cite the forms
that would prove otherwise.

## The second differentiator that needs no form either

The NFIP's caps are public and fixed: **$250,000 building / $100,000 contents** for
a residential policy. Any home worth more than $250,000 is underinsured by
construction under an NFIP policy. Private markets commonly write above that.

Both facts are publishable from public sources. Note the interaction with our own
data: 91% of our book sits at exactly $250,000 building limit, which is the NFIP
cap — evidence that the cap is shaping what gets bought, not what people need.

## What still may NOT be claimed

- Anything about deductible options, waiting periods, replacement cost on contents,
  or basement treatment **until each is checked against a public source or our own
  data.** These differ by carrier and programme — Hiscox alone runs four — and a
  claim that is true of one programme and false of another is a claim we cannot
  make generically.
- Any comparison implying every private policy is broader than the NFIP. It is not.
  Some are narrower, which is exactly why we quote both.
- The claims-handling advantage stays written as twelve years of agency
  experience, never dressed up as a statistic.

## The real framing: most people were never told they had a choice

Aaron, 13 Aug:

> "customers who chose the NFIP may have no idea they could even buy private and
> or even buy Loss of Use. many would have had they known it was only available on
> private policies."

This is a better argument than "private is cheaper," and it is the one that should
carry the page. The competitor here is not the NFIP. **It is the absence of a
conversation.**

Most NFIP policies are sold by agents who only sell the NFIP. A lender says "you
need flood insurance," the agent writes the policy they have, and nobody mentions
that another market exists — or that it can cover something the federal policy
cannot cover at all. The customer did not weigh loss of use and decline it. They
were never shown it.

That changes the tone of every sentence on the page:

- **Not** "the NFIP is worse." It is not worse; it is a federal programme with a
  fixed form and a statutory duty to insure everyone.
- **Instead**: here is what exists, here is what each one can and cannot do, and
  here is the coverage you cannot buy from the federal programme at any price.
- The call to action is not "switch." It is **"find out what your options actually
  are"** — which is also the honest description of what the agency does, since we
  quote both and place whichever wins.

It also explains, without blaming anyone, why a reader's existing agent never
raised this. It is not incompetence, it is appointment: an agent who is not
appointed with private flood markets has nothing to offer but the NFIP. Same
structural point as the sober living work — the adviser's limits quietly become
the customer's blind spot.

**This is the strongest thing on the page and it needs no data at all.** It should
be written and shipped ahead of any premium table.

### "My lender requires the NFIP" — verified, and it is not true

Checked against the regulators rather than taken on trust. Five federal agencies
issued a joint final rule implementing the private-flood provisions of the
**Biggert-Waters Flood Insurance Reform Act of 2012**, effective **1 July 2019**.
It **requires** regulated lending institutions to accept a private flood policy
that meets the statutory definition of private flood insurance, and separately
permits them to accept policies that do not meet it, at their discretion, if
certain criteria are met.

Sources: [FDIC FIL-19-2019](https://www.fdic.gov/news/financial-institution-letters/2019/fil19008.html),
[OCC Bulletin 2019-8](https://www.occ.gov/news-issuances/bulletins/2019/bulletin-2019-8.html),
[Federal Reserve](https://www.federalreserve.gov/newsevents/pressreleases/bcreg20190212a.htm),
[Federal Register, 20 Feb 2019](https://www.federalregister.gov/documents/2019/02/20/2019-02650/loans-in-areas-having-special-flood-hazards).

**The practical detail worth more than the rule itself.** The final rule contains a
*compliance aid* provision: a lender may conclude a policy qualifies **without
reviewing it further** if the policy or an endorsement carries the statement

> "This policy meets the definition of private flood insurance contained in
> 42 U.S.C. 4012a(b)(7) and the corresponding regulation."

That is the answer to Aaron's stragglers — the lenders, loan officers and agents
who still assume the NFIP is the only option. The objection is not argued with, it
is resolved by pointing at a line already printed on the policy. Worth saying on
the page in exactly those terms, because it converts a stalled closing into a
five-minute phone call.

**Aaron, 13 Aug: every policy this agency places already carries that line.** So
this stops being a legal argument and becomes a promise the page can make in the
first person:

> Every private flood policy we place carries the statement that lets your lender
> accept it without reviewing the policy at all.

**Correction to an earlier draft of this file.** I had written that the sentence is
"the end of the conversation." That overstates it, and the rule's own preamble says
why. Two limits, both from 84 FR 4953:

- The statement is **not mandatory** for an insurer to print, and **a lender may
  not reject a policy solely because it is missing.**
- A lender **may choose not to rely on it** and make its own determination anyway.

So the accurate claim is narrower and still strong: the sentence means a lender
*may accept without further review*. It removes the friction; it does not forbid a
lender from looking. Write it that way — an overstated legal claim on a page that
exists to be trustworthy is a bad trade.

That is concrete, verifiable by the customer the moment they hold the policy, and
it defuses the single biggest reason people default to the NFIP without ever asking
what else exists. It belongs next to the "you were never offered a choice"
section — the objection and its answer in the same breath.

Write it as **our** practice, which is what Aaron confirmed. Do not generalise it
into a claim about every private carrier in the market; we have not checked that
and it is not the claim we need.

**Still to check before quoting it:** Aaron's point that the statutory definition
requires private coverage to be *"at least as broad as"* an SFIP. That phrasing is
part of the definition at 42 U.S.C. 4012a(b)(7) but the regulators' summaries did
not quote it, so confirm against the statute or the regulation text before putting
those words on the page. The mandatory-acceptance substance above is confirmed and
can be used now.

Note how well this pairs with the loss-of-use argument: the law's floor is that
private must be **at least as broad** as the federal policy, and the coverage that
actually distinguishes them — loss of use — is something the federal policy does
not offer at all. "At least as broad, and often broader" is a defensible sentence,
and the second half is the reason to care.

Loss of use belongs **next to the price**, not in a features table further down.
The price section is where a reader decides whether the private option is worth
more money, and this is the answer to that question. Burying it below the fold
concedes the argument to whichever competitor shows a lower number.

---

# Verified 13 Aug 2026 — the statute, and where the loss-of-use gap actually is

Jobs 1 and 2, archived in `research-2026-08-13/`. Aaron ran these two through
**Grok 4.6**, not Kimi — the brief was written for Kimi but answered by Grok, so
the provenance differs from the three earlier reports the same day.

## The statute says exactly what Aaron said

42 U.S.C. § 4012a(b)(7)(B), quoted from uscode.house.gov and corroborated
word-for-word against govinfo and Cornell LII:

> "provides flood insurance coverage which is at least as broad as the coverage
> provided under a standard flood insurance policy under the national flood
> insurance program, including when considering deductibles, exclusions, and
> conditions offered by the insurer"

The comparator is the NFIP's Standard Flood Insurance Policy — not a homeowners
policy, not a state minimum. So **"at least as broad as" is quotable.**

**And the regulation explicitly contemplates broader.** 12 CFR 22.2(k)(2)(iv):

> "Any exclusions other than those in an SFIP may pertain only to coverage that is
> in addition to the amount and type of coverage that could be provided by an SFIP
> or have the effect of providing broader coverage to the policyholder"

That is the legal foundation for the whole argument: the law sets a floor of "at
least as broad," and the regulation anticipates private policies going beyond it.
"At least as broad, and often broader" is not marketing — it is the structure of
the rule.

## The loss-of-use gap: documented everywhere, monetised almost nowhere

Grok 4.6 surveyed 44 unique ranking pages across five queries. **41 mention loss of
use.** The fact is not a secret. But:

- Only about **six** pages make it the headline argument — and **four of those six
  are our own network**.
- Only **five pages quantify it at all.** The only hard private limits anywhere are
  **$7,500** (USI chart / Chubb base form) and **$25,000** (Flood Insurance Guru).
- **Nobody prices a California displacement.** No page anywhere sets a Bay Area or
  LA rent differential over a six-to-twelve month rebuild against the NFIP's $0.

That last line is the opening. The exclusion is common knowledge; the *cost of it*
is unclaimed ground.

### We already own the asset

`californiafloodinsurance.com/loss-of-use-coverage-in-flood-insurance/` **ranks on
four of the five queries** (Q2 #3, Q3 #2, Q4 #6, Q5 #3) — the single
broadest-ranking page in the entire survey, ours or anyone's. Statewide's
equivalent takes Q5 #10.

So this is not a build. It is an upgrade to a page already ranking, which is a far
cheaper win than the cost-page rebuild. **Do this first.** What it needs:

1. **California displacement maths.** Rent differential in the metro areas we
   actually write, over a realistic six-to-twelve month rebuild, against $0. This
   is the number nobody has published.
2. **A dollar limit.** Ours are commonly expressed as 10–20% of dwelling cover;
   competitors' only published figures are $7,500 and $25,000, both beatable.
3. **The `LossOfUseLimit` measurement** from our own book — what share of policies
   we placed carried it, at what median limit. Nobody else can produce that.

### Competitors' weak spots, all quotable

- **Allstate ranks #1** for "does flood insurance cover living expenses" — lists the
  exclusion, sells no private flood, offers no alternative.
- **Progressive ranks #8** on that query with a page that never mentions living
  expenses at all.
- **FEMA ranks #1** for "loss of use flood insurance" with a page that never uses
  the phrase.
- **Neptune**, a carrier that sells ALE, writes about hotel exclusions and never
  says its own policy can cover it.
- Nine pages **fudge** the exclusion with "standard", "generally" or "most" where it
  is absolute. Two are outright wrong. Being precise is itself a differentiator.

### Closest real competitor

**Latent Insurance** — puts "The NFIP pays nothing for temporary housing" in a
top-of-page takeaway, quantifies Chubb's $7,500, and frames a six-month
displacement. No California pricing and no book of its own. That is the standard to
beat, and the two gaps are exactly what we can fill.

### Government wordings we can cite (no policy form involved)

- **FEMA booklet, cleanest of all:** "The NFIP does not cover ALE."
- **FEMA agents.floodsmart:** "Temporary housing and additional living expenses
  incurred while the building is being repaired or is unable to be occupied."
- **Insurance Information Institute:** "The National Flood Insurance Program (NFIP)
  covers physical damage from flood but does not include ALE."
- **Texas Department of Insurance:** "But NFIP policies don't pay for additional
  living expenses."

### The California contrast worth building a paragraph on

California law gives homeowners policyholders **at least 24 months** to use their
ALE coverage — the strongest such protection in the country. On a flood claim under
an NFIP policy they get **nothing at all**, for any period.

Verify the 24-month provision against the Insurance Code before publishing; it
appeared in two secondary sources here, not a primary one. If it holds, the
sentence writes itself: California protects you for two years on your homeowners
policy and not one day on your federal flood policy.

---

# Loss of use, measured — 14 Aug 2026

**Correction first.** Earlier today I wrote that the bordereaux carry no
loss-of-use column and that the limit therefore could not be measured. That was
wrong, and wrong in a way worth naming: I read the header rows of three
**RBIA-era** files (QBE, Hiscox and Brit, April 2024), found nothing, and
generalised to the whole book without checking the **Instanda-era** layout — which
is the current one, and which carries `LossOfUseLimit` as column 52 of 55. The
earlier note above claiming the column exists was right; my correction to it was
the error. That section has been removed rather than left standing.

## What the column actually shows

Measured on the Aug 1–9 2026 Instanda file, 114 non-endorsement rows, 68 of them
California. **Take-up is not universal.** Aaron's understanding was that every
policy carries the line. At the policy level it does not:

| | share of rows |
|---|---|
| No loss-of-use limit (0) | **49%** |
| $5,000 | 24% |
| $50,000 | 11% |
| everything else ($10k–$146k) | 16% |

And the split is **not random — it tracks the programme**:

| programme | rows | written with no loss of use |
|---|---|---|
| Hiscox Custom | 23 | **0%** |
| Hiscox Full Value | 4 | 0% |
| Brit MVP | 15 | 27% |
| Brit | 13 | 77% |
| QBE | 58 | **71%** |

QBE is the largest part of the book and mostly writes without it. Hiscox Custom
always writes with it. So the honest statement is not "our policies include loss
of use" — it is **"loss of use is available, and which programme you end up in
determines whether you get it."** That is still a far stronger position than the
NFIP's, which is zero at any price, on any programme, for every applicant.

## What this changes

1. **Do not write "all our policies include loss of use."** It is not true of the
   book and it is the kind of claim that is trivially disproved by one customer's
   declarations page.
2. **The safe published form** is that the cover is commonly available on private
   policies and unavailable on the NFIP at any price — with the second half being
   the load-bearing part, and FEMA's own material being the source for it.
3. **A measured number is now possible** but not yet earned. What I have is nine
   days of one file. `by_loss_of_use` is wired into `premium-aggregate.py` and will
   report take-up and the limit distribution across the whole book on the next run,
   with the denominator restricted to layouts that actually carry the column — the
   older files' silence must never be counted as "no cover."
4. **Report the range, not a median.** The limits are bimodal — a $5,000 cluster
   and a $50,000 cluster — so a single median describes nobody. Same failure as the
   blended flood-zone average.
5. **Carrier-level take-up is internal only.** It is emitted under
   `by_carrier_INTERNAL_ONLY` so we can say "it depends on the programme" without
   naming programmes.

## The sales point hiding in this

Half our own customers are in a programme that does not include the cover. Some of
them presumably could have had it. That is the same "nobody told them" problem we
identified for private flood as a whole, one level down — and it is an argument for
the quote conversation existing at all, which is exactly what the site is for.

## Why half the book has no loss of use — it is the quote default, 14 Aug 2026

I recorded the take-up split as "programme-driven," which was mechanically true
and causally wrong. Aaron's explanation:

> "hiscox often offers it automatically in the quote and QBE someone must actually
> click to include it in the online quote and most dont... they are typically
> believing it will never flood and opt for the cheapest cost."

**The data confirms it exactly.** Limits actually written, Aug 1-9 2026:

| programme | with cover | distinct limit values | pattern |
|---|---|---|---|
| QBE | 17 of 58 | **1** — every one exactly $5,000 | opt-in checkbox, flat amount |
| Hiscox Custom | 23 of 23 | **10** — $30,000 to $146,400 | automatic, scaled to dwelling |

One distinct value across seventeen QBE policies is not seventeen people choosing
$5,000. It is a fixed checkbox. And Hiscox's odd values — $44,200, $47,200,
$146,400 — are percentages of the building limit ($146,400 is 20% of $732,000),
which is a system calculating a limit rather than a customer picking one.

So the 49% with no cover did not weigh it and decline. **They were shown a cheaper
number and a box they did not tick.**

### This is the site's whole thesis, one level down

We argue that most NFIP customers were never told private existed. The same
mechanism operates inside our own book: the default decides the outcome, not the
customer's preference. That makes the argument more honest, not less — we are not
claiming our customers are better informed, we are describing how insurance
actually gets bought.

### The business consequence, which is Aaron's call and not a website matter

41 QBE customers in nine days have no loss-of-use cover. If the flood that
displaces them happens, that gap is real money and they never knowingly declined
it. Whether QBE quotes should default it on, or the quote should present both
numbers side by side, is an operational decision — but the measurement says the
current default is making it for them.

### What it changes on the page

The "10% to 20% of dwelling" guidance I removed was in fact roughly right **for
Hiscox** and badly wrong for QBE. The replacement wording — limits vary widely and
are set by the program rather than chosen — remains correct and is now better
supported. Do not reinstate a percentage.
