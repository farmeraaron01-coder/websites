# Emma — knowledge base entries to fill in

15 entries, ordered by how often the intent actually appears in your inbound calls
(n=1,595 customer questions). Triggers are **verbatim from your own transcripts**.

**Fill in `CAN SAY`.** I've pre-filled `CANNOT SAY`, `NEXT STEP` and `VARIES BY CARRIER`
from what I already know about her guardrail and your setup — correct anything that's wrong.

Rules for writing `CAN SAY`:
- Two or three sentences. It gets spoken aloud, not read.
- No bullets, tables, or URLs. Write numbers the way she should say them.
- End with what happens next, not with a definition.
- If you don't know or it varies, that's a valid answer: say so and hand off. An honest
  handoff sounds far more competent than a confident guess.

---

## 1. Lender / mortgagee / escrow — 165 questions, the biggest intent

Split into six entries. One combined entry would retrieve badly — an escrow caller would
pull a chunk mostly about faxing dec pages.

### 1A. Send documents to my lender — 27

```
TRIGGER
"Can you send the declaration page to the lender?"
"Are you able to fax the declarations page to my bank?"
"Did you send the declarations page to Bank of America?"
"Can you fax and email the documents to the lender?"
"Will someone send confirmation to me or the lender?"
"Did you send the renewal to our mortgage company?"

CAN SAY
[FILL IN — can she promise it will be sent? within what timeframe? fax and email both?]

CANNOT SAY
Don't confirm something was already sent unless she can see it. Don't state coverage
is in force.

NEXT STEP
Collect: policy number, lender name, where to send (fax number or email), loan
number, and any closing deadline.
[FILL IN — who owns lender requests? turnaround?]

URGENT IF
A closing date is named, or the lender needs it to fund.
```

### 1B. Add or correct the mortgagee / lienholder — 18

```
TRIGGER
"Do we need to list the mortgage holder on the policy?"
"What is a mortgagee clause and where can I find it?"
"Can you remove Wells Fargo as a lienholder from my policy?"
"Can you confirm FAY Servicing is listed as the first mortgagee?"
"How do I add a new lender to my policy for a home equity line of credit?"
"What information do you need to update the mortgagee clause?"

CAN SAY
[FILL IN — one plain sentence defining a mortgagee clause (safe to explain), plus
 exactly what you need to add or change one]

CANNOT SAY
Don't confirm who is currently listed unless she can see the policy. Don't confirm
the change is effective.

NEXT STEP
Collect: policy number, full lender name, mortgagee clause address, loan number,
whether they're replacing or adding.
[FILL IN — turnaround? who handles it?]
```

### 1C. Did my lender's payment arrive — 16

```
TRIGGER
"Did you receive payment for our two policies from our lender?"
"Can you confirm that you received my renewal payment from my lender?"
"Has my impound account with my mortgage paid my premium?"
"Did my mortgage company send the flood insurance payment?"
"Can my lender stop the payment on the check?"

CAN SAY
[FILL IN — she can't see the ledger. Phrase it so it doesn't feel like a brush-off:
 acknowledge, capture details, promise a real answer by when?]

CANNOT SAY
Never confirm or deny that a payment was received or applied.

NEXT STEP
Collect: policy number, who was expected to pay, amount, approximate date, and
whether they've had a notice.

URGENT IF
They mention a final notice, cancellation notice, or possible lapse.
```

### 1D. Who pays — escrow vs direct bill — 14

```
TRIGGER
"Do I have to pay the entire bill or is it included in my mortgage?"
"Is my policy being paid through my escrow account?"
"How does the billing through escrow work?"
"Why did I receive a final notice renewal bill if my escrow company said they paid it?"
"Can I pay the premium myself instead of through my mortgage company?"
"If I pay it up front in full now, can I contact my lender and have it added too?"

CAN SAY
[FILL IN — escrow vs direct bill in plain language. Give the "final notice but escrow
 says they paid" case its own sentence; that caller is worried about losing coverage.]

CANNOT SAY
Don't state whether THIS policy is escrow-billed unless she can see it.

NEXT STEP
[FILL IN — can she look up billing method, or always a handoff?]

URGENT IF
A final or cancellation notice is mentioned.
```

### 1E. How much coverage does my lender require — from ungrouped

```
TRIGGER
"Will the lender be satisfied if I just do the loan amount?"
"What should I do if the lender sees two policies?"
"Do you have lender-placing permission for the policies?"
"Can the bank change our flood insurance?"

CAN SAY
[FILL IN — careful here. Loan amount vs replacement cost edges into licensed advice.
 Probably a short factual framing plus a handoff.]

CANNOT SAY
Never advise on how much coverage they should carry. Never say a limit will or won't
satisfy a lender.

NEXT STEP
Route to a licensed agent. Note duplicate or force-placed coverage as a flag.
```

### 1F. Loan number and identifiers — 6

```
TRIGGER
"Does the renewal email include the loan number?"
"Can you confirm the loan number associated with the policy?"
"Do you need the address of my mortgage person or just the account number?"

CAN SAY
[FILL IN — what identifiers you need from them; may she read a loan number back?]

CANNOT SAY
Never guess or reconstruct a loan or policy number from partial digits.

NEXT STEP
Collect the full loan number and lender name.
```

## 2. Renewal — 91

```
TRIGGER
"What do I need to do first to renew the policy?"
"Is there a renewal declaration page available yet?"
"Can you look up what's going on with the renewal document?"
"Is there any way you can mail the renewal documents to me?"
"Can I have the reason for non-renewal?"
"Would these coverage amounts have to go up at renewal?"

CAN SAY
[FILL IN — how far ahead renewals go out, whether they auto-renew, what a caller
 needs to do (usually nothing), how to get renewal docs]

CANNOT SAY
Don't state the renewal premium. Don't explain why a carrier is non-renewing —
that's a licensed conversation.

NEXT STEP
[FILL IN — who handles renewals? Non-renewal should probably escalate.]

VARIES BY CARRIER
[CONFIRM]

URGENT IF
Non-renewal or cancellation notice received.
```

## 3. Coverage questions — 75

```
TRIGGER
"Is the golf cart covered under personal property if it gets stolen?"
"Would a tree falling on a house be covered?"
"Can we raise the deductible to reduce the premium?"
"Are there any policies with lower deductibles?"
"What does 'loss of use 24 months' mean in my condo policy?"

CAN SAY
[FILL IN — how much general explanation is she allowed? Suggested shape: acknowledge
 the question, say coverage depends on the specific policy form, offer to have a
 licensed agent review it and call back.]

CANNOT SAY
Never say something IS or IS NOT covered. Never reinterpret policy language.
Never quote a premium change for a deductible change.

NEXT STEP
Collect policy number and the specific question. Route to a licensed agent.

VARIES BY CARRIER
Yes — always.
```

## 4. Quote requests — 56

```
TRIGGER
"Can I get a quote on a property I have?"
"How much would it be for a new auto policy?"
"Can you compare my current policy with the new quote?"
"When will the new policy be effective?"

CAN SAY
[FILL IN — she already collects intake well. What should she promise? "An agent will
 call you back" — within what timeframe?]

CANNOT SAY
No prices, rates, discounts, or savings. No effective date — that's binding.

NEXT STEP
Full intake per the request-type checklist, then route to sales.
[FILL IN — realistic callback window, and does it differ personal vs commercial?]

VARIES BY CARRIER
n/a

NOTE
A quote request must never trip the guardrail. This is the core purpose of the line.
```

## 5. Cancellation — 40

```
TRIGGER
"What do I need to cancel my policy due to a home sale?"
"Can I just cancel the policy even if I didn't sell the house?"
"Why can't I cancel the insurance over the phone?"
"Is it possible to provide the cancellation document?"
"What options does the client have to reinstate the policy?"

CAN SAY
[FILL IN — what's actually required (signed request? effective date?), and why it
 can't be done on the call. Callers get frustrated here — worth wording carefully.]

CANNOT SAY
Never confirm a cancellation is effective. Never state a refund amount.

NEXT STEP
Collect policy number, requested effective date, reason, whether replacement
coverage is in force. Route to service.

VARIES BY CARRIER
[CONFIRM]

URGENT IF
There's a lienholder, or they've already bought replacement coverage.
```

## 6. "Let me speak to a person" — 33

```
TRIGGER
"Can I speak to Craig?"
"Can I talk to the owner?"
"Is Amy available?"
"Can someone call me back?"

CAN SAY
[FILL IN — this needs a decision from you. Can she offer to transfer? Or only take
 a message? If she names people, she needs to know who's who.]

CANNOT SAY
Don't claim someone is or isn't available unless she actually knows.
Don't reference Gabriela Flores — no longer employed.

NEXT STEP
[FILL IN — can she transfer? To which extensions? Or message-only?]

VARIES BY CARRIER
n/a

NOTE
Callers asking for a named person are usually mid-issue and impatient. Getting this
one right prevents a lot of frustration.
```

## 7. Amount due / total — 29

```
TRIGGER
"What is the total premium amount for the policy?"
"How much is the payment?"
"What do I owe?"

CAN SAY
[FILL IN — can she look anything up, or is it always a handoff? If handoff, phrase it
 so it doesn't sound like a brush-off.]

CANNOT SAY
Never state an amount. This is a hard guardrail line.

NEXT STEP
Collect policy number and route to billing.
[FILL IN — same-day callback?]

VARIES BY CARRIER
Yes.
```

## 8. How / where to pay — 28

```
TRIGGER
"How do I pay this?"
"Where do I send the check?"
"Is the overnight remittance address on the invoice?"
"Can I give you a credit card?"

CAN SAY
[FILL IN — REMITTANCE ADDRESS, spoken out. Which carriers take online payment.
 Whether a payment link can be sent, and by whom.]

CANNOT SAY
Never take a card number over the phone. Never confirm a payment posted.

NEXT STEP
If she can give the address or send a payment link, that resolves the call.
Otherwise route to billing.

VARIES BY CARRIER
[CONFIRM — do payments come to you or go direct to the carrier?]

NOTE
A customer's premium check went to the wrong agency (voicemail we reviewed). Getting
this address right is worth real money.
```

## 9. Refunds — 26

```
TRIGGER
"What is the status of my refund for a double payment?"
"Does it usually take up to 30 days for the refund?"
"Will the refund check be sent to us, or has it gone to the wrong address?"
"Will the insured receive a refund?"

CAN SAY
[FILL IN — typical timeline, who issues it (you or the carrier), how it's sent]

CANNOT SAY
Never state a refund amount or promise a date.

NEXT STEP
Collect policy number and confirm the current mailing address — several callers
worried a refund went to an old address.

VARIES BY CARRIER
[CONFIRM]
```

## 10. Claims — 21

```
TRIGGER
"What is the process for filing a claim?"
"Should I contact Travelers' claims department?"
"Can I speak to an adjuster regarding a general question?"
"Has the claim receipt been sent to my lender?"

CAN SAY
[FILL IN — general process, and ideally the direct claims number for the caller's
 carrier so she can hand off immediately rather than take a message]

CANNOT SAY
Never promise a claim will be paid, denied, or handled a certain way.

NEXT STEP
[FILL IN — per-carrier claims numbers. This is the highest-value list on the page:
 it converts a message into a resolved call.]

VARIES BY CARRIER
Yes — needs the per-carrier list.

URGENT IF
Loss just occurred, anyone is injured, or property is uninhabitable.
```

## 11. "Did you get my payment?" — 20

```
TRIGGER
"Did you receive the payment for my policy?"
"Did the policy payment go through?"
"How long does it take to confirm the payment?"
"Can you verify if all my policies are paid?"

CAN SAY
[FILL IN — she cannot see the ledger. How should she handle it so the caller feels
 taken seriously? Suggested: acknowledge, capture check number and date sent,
 promise a same-day answer.]

CANNOT SAY
Never confirm or deny receipt.

NEXT STEP
Capture policy number, check number, amount, date sent, where sent. Route to billing.

VARIES BY CARRIER
n/a

URGENT IF
They mention a cancellation notice, or think the payment went to the wrong place.
This exact situation was sitting unread in voicemail (Suzanne Jackson, check 905690).
```

## 12. Proof of insurance / EOI / COI — 19

```
TRIGGER
"How can I request a copy of the evidence of insurance?"
"How soon will I get the evidence of insurance?"
"Can you send me proof of insurance?"
"I need an ID card."

CAN SAY
[FILL IN — turnaround time, and whether she can promise an email]

CANNOT SAY
Don't promise specific wording or limits on a certificate.

NEXT STEP
For a plain EOI: policy number, where to send.
For a commercial COI: certificate holder's exact legal name and address, required
limits, additional-insured wording, deadline.
[FILL IN — turnaround for each]

VARIES BY CARRIER
[CONFIRM]
```

## 13. Grace period / late / lapse — 18

```
TRIGGER
"Is there any grace period for the policy?"
"Will I be covered for seven days through a grace period after my payment due date?"
"My payment is late — am I still insured?"
"What are my options to resolve the payment shortfall?"

CAN SAY
[FILL IN — likely: grace periods vary by carrier and policy, so she shouldn't state a
 number, but she must not leave them thinking they're uninsured either. Getting this
 wording right matters.]

CANNOT SAY
No day counts. Never state coverage is or isn't currently active.

NEXT STEP
Escalate — possible lapse. Collect policy number and callback, route same day.

VARIES BY CARRIER
Yes — never state a number.
```

## 14. Send me my policy documents — 14

```
TRIGGER
"Can you send a copy of my insurance policy to my email?"
"Can you send us a copy of the current declaration page?"
"Did you send the policy documents via email?"
"Can you send me the policy coverages and exclusions?"

CAN SAY
[FILL IN — can she promise an email? how fast? does she need to verify identity first?]

CANNOT SAY
Don't summarize or interpret what the documents say.

NEXT STEP
Confirm policy number and the email on file — never a new email address without
verification.
[FILL IN — what identity check is required before sending documents?]

VARIES BY CARRIER
n/a
```

## 15. "I don't have my policy number" — 3 (small but blocks everything)

```
TRIGGER
"Can I give you the address instead of the policy number?"
"Do you need my account number again?"
"I don't have my policy number with me."

CAN SAY
[FILL IN — what's the acceptable fallback? Property address plus name? Phone on file?]

CANNOT SAY
Never guess or construct a policy number from partial digits.

NEXT STEP
Capture full name plus property address or vehicle so the team can locate the policy.

VARIES BY CARRIER
n/a

NOTE
Low frequency but it gates every other request. Worth answering well.
```

---

## Also worth writing (no transcript examples yet — Emma is new)

Personal-lines intents that will show up once she's taking real calls. Same format:

- **Add / swap / remove a vehicle** — use the checklist fields already drafted
- **Add / remove a driver** — including teen drivers
- **Address change / moving**
- **New home purchase / closing** — usually urgent
- **Caller is angry or has been transferred repeatedly**
- **Wrong number / solicitor** — how to exit politely and fast

---

## When you send it back

I'll load these as **atomic knowledge-base entries** (one per intent, not one big
document — they retrieve far better that way), **enable RAG** so she pulls only the
relevant entry per turn, and put the cross-cutting rules — escalation triggers, never
guessing digits, identity verification before sending documents — into her **prompt**
so they apply on every call rather than only when retrieval happens to surface them.

Then we test her against these exact 15 questions and see where she still hesitates.
