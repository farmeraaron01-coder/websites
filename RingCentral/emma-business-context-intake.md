# Emma — business context intake

Everything Emma needs to sound confident about Jump Insurance Services. I pre-filled what I
could verify from jumpins.com, your RingCentral config, and 700 call transcripts. Your job is
the `[CONFIRM]` and `[FILL IN]` items.

Once filled, this becomes a knowledge-base document on her agent (with RAG enabled so she
retrieves the relevant part instead of carrying all of it in context every turn).

> **Why this matters more than the website.** The site gave her product *names*, so she can say
> "yes, we write pest control." It told her nothing about how you actually work — which is what
> callers ask about. 27% of inbound customer questions are billing and payments; the website has
> nothing to say about that.

---

## 1. Identity — verified

- **Agency:** Jump Insurance Services, an independent agency
- **Greeting:** "Thank you for calling Jump Insurance Services. This is Emma on a recorded line."
- **Number:** +1 858-304-7373
- **Sister brands she must not confuse herself with:**
  - Jump Trucking Insurance — Sarah, +1 858-828-4747
  - California Flood Insurance Services — Brooke, +1 858-299-2866
- `[CONFIRM]` Legal entity name for any documents: Rebecca Byrom Insurance Agency Inc.?
- `[CONFIRM]` License number(s) to state if asked

## 2. Locations & hours

Verified from the website:
- **San Diego:** 7960 Silverton Ave #202, San Diego, CA 92126 — 858-295-7242
- **Palm Desert / La Quinta:** 760-610-6145
- **Email:** agency.services@jumpins.com

- `[FILL IN]` Office hours per location, and time zone
- `[FILL IN]` Holiday closures
- `[FILL IN]` What happens after hours — Emma currently just says "the office is closed"
- `[CONFIRM]` Which location handles what, if it matters for routing

## 3. Products — verified from jumpins.com

**Personal:** Home, Auto, Motorcycle, Vacant Home, Flood, Boat, Condo, Landlord, Mexico Auto,
Renters, Umbrella, Earthquake, ATV, Recreational Vehicle, Classic Car
**Business:** Business Owners Policy, Business Property, EPLI, Trucking/Transportation,
Commercial Auto, Cyber, Workers Compensation, Umbrella/Excess Liability, Pest Control
**Life**

- `[FILL IN]` **Lines you do NOT write** — the most valuable item on this page. Right now Emma
  will take a message for anything, which sends the caller into a dead end and wastes your
  team's time. Let her decline early and politely.
- `[FILL IN]` Anything with special handling (e.g. does Flood always go to Brooke? Does
  Trucking always go to Sarah's team?)

## 4. Carriers — CONFIRM, do not assume

Mentions across 700 transcripts. **Frequency is not the same as appointment** — some of these
are callers naming their *prior* carrier. Please mark each as Appointed / Not appointed /
Customer's other carrier.

| Carrier | Mentions | Status |
|---|---|---|
| Travelers | 199 | `[CONFIRM]` |
| Progressive | 94 | `[CONFIRM]` |
| California FAIR Plan | 48 | `[CONFIRM]` |
| Mercury | 47 | `[CONFIRM]` |
| Neptune (flood) | 23 | `[CONFIRM]` |
| Bamboo | 23 | `[CONFIRM]` |
| Selective | 20 | `[CONFIRM]` |
| Berkshire | 19 | `[CONFIRM]` |
| Palomar | 17 | `[CONFIRM]` |
| Pacific Specialty | 11 | `[CONFIRM]` |
| Hiscox | 9 | `[CONFIRM]` |
| GeoVera | 9 | `[CONFIRM]` |
| Wright (flood) | 5 | `[CONFIRM]` |
| Markel | 5 | `[CONFIRM]` |
| Great American | 4 | `[CONFIRM]` |
| Safeco, Liberty Mutual, Nationwide, National General, Foremost, Kemper, Hartford | 1–4 each | `[CONFIRM]` |
| State Farm 15, Farmers 8, Allstate 5, USAA 5, AAA 5 | — | likely callers' prior carriers — `[CONFIRM]` |

Ignore "Next" (308) — that's the ordinary word, not Next Insurance.

- `[FILL IN]` Any appointed carrier missing from this list
- `[FILL IN]` **Direct claims number per carrier** — so Emma can hand off a caller with a loss
  in progress instead of taking a message
- `[FILL IN]` Which carriers accept online payment, and the portal URL for each

Emma must never say one carrier is better than another — that's already in her guardrail.

## 5. Systems — verified, needs detail

Seen in transcripts: **NowCerts / Momentum** (your AMS), **Applied**, Travelers `4agents`
portal, DocuSign, e-signature and payment links.

- `[FILL IN]` What system of record should Emma reference by name to callers, if any
- `[FILL IN]` Can she say "I'll send you a payment link" / "an e-signature request"? Who sends it?
- `[FILL IN]` Self-service portal for customers, if one exists

## 6. Billing & payments — HIGHEST PRIORITY

**27% of inbound customer questions.** These are verbatim from your own calls, and Emma
currently cannot answer any of them:

- *"Will I be covered for seven days through a grace period after my payment due date?"*
  → `[FILL IN]` grace period by carrier, or the general rule
- *"Do I have to pay the entire bill or is it included in my mortgage?"*
  → `[FILL IN]` how to explain escrow vs direct bill
- *"How would they pay it without a policy number?"*
  → `[FILL IN]` what a caller needs to make a payment
- *"Can the insured enroll in AutoPay before renewal?"*
  → `[FILL IN]` autopay enrollment rules and who does it
- *"What are my options to resolve the payment shortfall?"*
  → `[FILL IN]` short-payment process
- *"How long does it take to confirm the payment?"*
  → `[FILL IN]` realistic posting time
- *"Can I give you different credit cards to process the payment?"*
  → `[FILL IN]` policy on split payments — and confirm Emma must **never** take card numbers

- `[FILL IN]` Where payments should be mailed (remittance address) — a customer's check went to
  the wrong agency in a voicemail we reviewed
- `[FILL IN]` What to do when someone says a payment may have been lost or misapplied. Suggest
  this is an escalation, not a callback.

## 7. Documents & lender requests — second priority

11% documents, 7% mortgage/lender. Real questions:

- *"Can you send a copy of my insurance policy to my email?"*
- *"Can you send the declaration page to the lender?"*
- *"Do we need to list the mortgage holder on the policy?"*
- *"Did you send the renewal to our mortgage company?"*

- `[FILL IN]` Turnaround for a dec page / EOI / COI — same day, 24h, 48h?
- `[FILL IN]` Can Emma promise an emailed document, or only that a team member will send it?
- `[FILL IN]` What's needed to add or change a mortgagee / loss payee
- `[FILL IN]` Who handles lender and escrow requests

> Lenders often flag as *Possible spam call* because they dial from call centers. They are
> legitimate and frequently on a closing deadline.

## 8. Escalation — what interrupts someone

Draft list, `[CONFIRM]` and edit:

- Vehicle or property needs coverage **today**
- Caller has a **cancellation or non-renewal notice**, or is lapsed
- **Payment may be lost or misapplied**
- **Claim in progress**, or a loss that just occurred
- **Lender / escrow / title** needs EOI to close
- Caller says they are **uninsured right now**

- `[FILL IN]` Who to route each to, and by what channel

## 9. People & routing

From RingCentral. `[CONFIRM]` who Emma should name or route to:

Amy Bullington 304, Diane Morataya 252, Joe Aguila 256, Krista Zilke 330, Chandra Taft 331,
Craig Yost 324, Morgan Roddey 305, Crystalyn Post 335, Julieta Pobluchenco 341,
Tess Mendoza 323, Lynn Rocheleau 322, Carlos Pineda 342, Enzo Burgos 343, Lucia Lopez 344,
Joseph Readnack 212, Dania Merry 215, Ron Mullins 203, Michael Floyde 306,
Agustina Uzin 345, Jeremy Wilkins 351, Michelle Crothers 352, Valeria Cortez 369

- `[FILL IN]` Specialties — who owns personal lines, commercial, service, billing, claims
- `[FILL IN]` New staff not in this list
- Note: Gabriela Flores is no longer employed — Emma must not reference her

## 10. Things Emma must never do

Already enforced by prompt and guardrail; confirm nothing is missing:

- Bind, change, cancel, or confirm coverage
- Quote a specific price or premium
- Promise a claim outcome
- Give legal, regulatory, or tax advice
- Compare carriers or call one better
- Reinterpret policy language
- Take a credit card number over the phone
- **Guess digits** — never construct a phone number, policy number, or address from partial
  information *(she once produced 760-610-6465 by borrowing the Palm Desert prefix)*

---

## How to send this back

Fill in what you can — partial is fine, and billing (§6) alone would be the biggest single
improvement. Paste it back or drop it in Dropbox and I'll:

1. Build it into a structured knowledge-base document on Emma
2. Enable RAG so she retrieves the relevant section per turn instead of carrying all of it
3. Add the §1–3 hard facts directly to her prompt, since identity and scope should never
   depend on retrieval
4. Write the §8 escalation rules and the §10 no-guessing rule into her prompt as behavior

Then test with the real questions from §6 and §7 and see whether she answers confidently.
