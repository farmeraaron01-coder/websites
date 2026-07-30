# Voice Agent Intake Checklists — DRAFT for review

Working draft for Emma / Sarah / Brooke. **Edit the field lists to match how you actually
work** — especially the vehicle swap section, since you said your parameters differ. Once you've
marked it up, I'll write it into each agent's prompt.

Legend:
- **[R]** Required — do not close the call without it
- **[A]** Ask if applicable / conditional
- **[O]** Nice to have, don't push

---

## Global rules (apply to every call)

These are the guardrails, and the first one is the bug from the 7/30 test call.

1. **Never construct or guess digits.** If the caller gives a partial phone number, policy
   number, VIN, or address, ask for the missing part. Never fill a gap from the knowledge base,
   the website, or the agency's own numbers. Read back only digits the caller actually said.
   *(On 7/30 the agent had "6465" and produced 760-610-6465 — the Palm Desert office prefix.)*

2. **Caller ID is a suggestion, not a fact.** Offer it once — "is the number you're calling from,
   ending in ####, the best callback?" — and if the caller corrects it, capture the full ten
   digits from scratch and confirm once.

3. **Existing policyholders: always get the policy number.** If they don't have it, capture full
   name + property address or vehicle so the team can locate the policy.

4. **Always capture an effective date** for any coverage change. "When do you need this
   effective?" A swap with no date is a coverage-gap risk.

5. **Confirm contact info once, not twice.** One readback per field.

6. **Never bind, change, cancel, or confirm coverage.** Existing compliance language stays as-is.

7. **One question at a time.** Don't stack.

---

## Escalation — flag as URGENT

Route these for immediate attention rather than a routine callback:

- Vehicle or property needs coverage **today** (just purchased, closing today)
- Caller mentions a **cancellation or non-renewal notice**, or a lapse
- **Payment may have been misapplied or lost** *(cf. the Suzanne Jackson voicemail)*
- **Claim in progress**, or a loss that just occurred
- **Lender / escrow / title** needs evidence of insurance to close
- Caller says they are **uninsured right now**

---

## 1. Vehicle swap / add / remove  ← YOU SAID YOUR PARAMETERS DIFFER, EDIT THIS

**Vehicle being ADDED**
- [R] Year, make, model
- [R] VIN
- [R] Effective date — when coverage must start
- [A] Lienholder or lessor name and address (financed or leased → loss payee required)
- [A] Purchased from dealer or private party
- [O] Approximate mileage
- [O] Garaging address, if different from the policy address
- [O] Primary driver of this vehicle
- [O] Use — commute, pleasure, business; one-way commute miles
- [O] Coverage requested — same as the removed vehicle, or different limits/deductibles

**Vehicle being REMOVED**
- [R] Year, make, model
- [R] Removal date
- [A] What happened to it — sold, traded, totaled, stored, kept without coverage
- [A] If keeping it uninsured, warn that a lapse may affect registration and future rates

**Both**
- [R] Policy number
- [R] Full name
- [R] Callback number (ten digits, confirmed)
- [R] Email
- [O] Best time to reach

> Fields to reconsider: do you want VIN mandatory on the call, or is a photo/text of the
> registration easier for callers? Should the agent ask about **rideshare/delivery use**? Any
> vehicles you won't write that she should flag early?

---

## 2. Driver add / remove

- [R] Policy number
- [R] Driver full name
- [R] Date of birth
- [R] Driver's license number and issuing state
- [R] Effective date
- [A] Relationship to the named insured
- [A] Which vehicle they primarily drive
- [A] Removing — reason (moved out, no longer driving, deceased, own policy)
- [O] Accidents or violations in the last 3–5 years
- [O] Student — away at school, good-student discount

---

## 3. Address change

- [R] Policy number
- [R] Current address
- [R] New address, including unit and ZIP
- [R] Effective date / move date
- [A] Is this a garaging change, a mailing change, or both
- [A] Does the new location change the insured property (home policies)
- [O] New phone number

---

## 4. Certificate of insurance / Evidence of insurance

Split by who's asking — this is a big share of your call volume.

**Commercial COI**
- [R] Policy number or insured business name
- [R] Certificate holder — exact legal name and address
- [R] Required limits, and any additional insured or waiver of subrogation wording
- [R] Where to send it, and deadline
- [A] Project name, contract number, or description of work
- [A] Primary and non-contributory / completed-operations wording

**Lender or escrow EOI (auto or property)**
- [R] Policy number, or insured name and property address
- [R] Loan number
- [R] Lender name and mailing address, plus loss-payee wording
- [R] Where to send, and closing date
- [A] Whether the lender needs the mortgagee clause added or changed

> These callers often show as *Possible spam call* because they dial from call centers. Treat
> them as legitimate business callers.

---

## 5. Billing / payment

- [R] Policy number
- [R] What they're asking — amount due, due date, confirm receipt, change method, set up autopay
- [A] Check number and date mailed, if asking whether a payment landed
- [A] Where it was sent, if they think it went to the wrong place
- [A] Cancellation notice received? → **URGENT**
- [O] Preferred payment method

*Direct callers to the carrier portal for card payments; never take card numbers on the call.*

---

## 6. Cancellation request

- [R] Policy number
- [R] Effective cancellation date
- [R] Reason
- [A] Replacement carrier and whether new coverage is already in force
- [A] Vehicle sold or property sold — date
- [A] Lienholder still on the vehicle? (may not be cancellable)

*Never confirm a cancellation. Always route to a licensed agent.*

---

## 7. Claim reporting / claim status

- [R] Policy number
- [R] Date and time of loss
- [R] What happened — brief description
- [R] Injuries? — if yes, **URGENT**
- [A] Vehicle drivable / property habitable
- [A] Police or fire report number
- [A] Other party's name, insurance, contact
- [A] Existing claim number, for status calls
- [O] Photos available

*If the loss is in progress or unsafe, direct them to the carrier's 24-hour claims line.*

---

## 8. New quote — personal

- [R] Full name, callback number, email
- [R] Line — auto, home, renters, condo, umbrella, flood, earthquake, motorcycle, boat, RV, classic
- [R] Address of the risk
- [A] Auto — vehicles (year/make/model), drivers (name/DOB), current carrier and expiry
- [A] Home — year built, square footage, roof age, construction, current carrier
- [A] Prior losses in the last 5 years
- [O] Currently insured, and what they're paying now
- [O] Bundling interest

## 9. New quote — commercial

- [R] Legal business name and DBA
- [R] Contact name, callback number, email
- [R] Type of business / operations
- [R] Coverage needed — BOP, GL, property, commercial auto, workers comp, cyber, professional, EPLI, umbrella
- [A] Trucking or transportation → **note as a trucking request and route to the trucking division**
- [A] Annual revenue, payroll, employee count
- [A] Years in business
- [A] Current carrier and renewal date
- [O] Loss history

## 10. General message for the team

- [R] Full name
- [R] Callback number
- [R] Who or which department it's for
- [R] The message
- [O] Email, best time to reach

---

## Agency facts still needed

I can't source these — they're operational. Once you provide them I'll build a knowledge base
document and enable RAG so the agents can actually answer instead of taking a message:

- Office hours per location, and holiday closures
- Carriers you place business with (so she can confirm "yes, we work with X")
- Direct claims phone numbers per carrier
- Payment portal URL, and which carriers accept what
- Realistic turnaround: same-day vs 24–48 hours, for COIs, endorsements, EOIs
- What the service team can do without a licensed agent
- Which lines you do **not** write, so she can decline early rather than take a dead-end message
- Named staff and specialties, for warm transfers or accurate routing
