# call-intelligence pipeline — two fixes

Apply in the `call-intelligence` repo. This session can't reach that repo, so this is the spec
plus working code; paste it into desktop Claude Code or apply by hand.

Airtable schema is already updated (base `appRhpJhmEFtj9dlf`):

| Table | New field | Type | ID |
|---|---|---|---|
| Calls | `Answering Extension` | singleLineText | `fldFKAmqIrrB8RTvD` |
| Calls | `Call Party` | singleSelect | `fldSRIqnKtaI5ylb8` |
| Customer Questions | `Call Party` | singleSelect | `fld8XuCh4A39LrFtQ` |
| Customer Questions | `Direction` | singleSelect | `fld4BGToP3CnqLvrt` |

`Call Party` choices: `Customer`, `Carrier`, `Lender`, `Internal`, `Vendor/Other`, `Unknown`.

---

## Why these two

**Fix 1 — inbound calls have no agent.** All 852 inbound records land as `Agent: Unknown`, while
every named agent is 100% outbound. Inbound arrives through a queue, so the queue owns the
recording and the answering person is only visible in the call-log `legs` array. Without this you
cannot tell who handled 60% of your calls.

**Fix 2 — outbound "customer questions" are mostly carrier calls.** Spot-checking Diane
Morataya's transcripts: a 20-minute Travelers agent-services hold queue to request an SR-22, and
a GeoVera payment-reminder voicemail. Questions mined from those are *the agency asking a
carrier*, not customers asking you — e.g. "Can we get an SR-22 sent to the client?" and "Can the
insured enroll in AutoPay before renewal?". The third-person "the insured" is the tell. These
pollute the content-mining set.

---

## Fix 1 — attribute the answering extension

`view=Detailed` must be set on the call-log request (the existing spec already does this). Each
record then carries `legs[]`. The answering party is the **last** leg that both targets an
internal extension and actually connected.

```js
/**
 * Identify which extension answered a call.
 * Returns { extensionNumber, name } or null.
 *
 * Leg shapes worth knowing:
 *   legType Accept        -> arrival at the number / site / queue (no extension)
 *   legType PstnToSip     -> ringing an internal extension's device
 *   legType FindMe        -> FindMe/FollowMe, may target an EXTERNAL number
 *   legType RingDirectly  -> straight to a target
 *   result  'Accepted' | 'Call connected' -> this leg is the one that connected
 *
 * Zero-duration legs with reason 'No Digital Line' are device slots with no line.
 * They are noise; never treat them as the answering party.
 */
function findAnsweringExtension(record) {
  const legs = record.legs || [];
  const CONNECTED = new Set(['Accepted', 'Call connected']);

  const candidates = legs.filter(l => {
    const ext = l.to && l.to.extensionNumber;
    if (!ext) return false;                          // external or queue-level leg
    if (l.reason === 'No Digital Line') return false; // 0-second phantom leg
    return CONNECTED.has(l.result);
  });

  // Last connected internal leg = final answering party (transfers land here).
  const leg = candidates[candidates.length - 1];
  if (leg) {
    return { extensionNumber: String(leg.to.extensionNumber), name: leg.to.name || null };
  }

  // Fallback: the extension whose log this record came from, when it's a real user.
  if (record.extension && record.extension.id) {
    const ext = extensionDirectory.get(String(record.extension.id)); // build this once, see below
    if (ext && ext.type === 'User') {
      return { extensionNumber: String(ext.extensionNumber), name: ext.name };
    }
  }
  return null;
}
```

Build the directory once per run so extension numbers resolve to names, and so departed staff
still resolve for historical records:

```js
// GET /restapi/v1.0/account/~/extension?perPage=1000  (paginate on navigation.nextPage)
const extensionDirectory = new Map();   // id -> { extensionNumber, name, type, status }
const extensionByNumber  = new Map();   // extensionNumber -> { name, type, status }
```

Then when writing the Airtable row:

```js
const answered = findAnsweringExtension(record);
fields['Answering Extension'] = answered ? answered.extensionNumber : '';
// Keep Agent authoritative but stop writing 'Unknown' when we can do better:
if ((!fields['Agent'] || fields['Agent'] === 'Unknown') && answered) {
  fields['Agent'] = answered.name
    || (extensionByNumber.get(answered.extensionNumber) || {}).name
    || `ext ${answered.extensionNumber}`;
}
```

### Backfill

Existing 852 inbound rows can be repaired without re-downloading audio — the call log is the only
source needed. Re-fetch the log for the same window, match on `recording.id` against the
`Recording ID` column, and patch `Answering Extension` + `Agent`. Note RingCentral retains call
log for ~90 days, so anything older than that can't be backfilled.

---

## Fix 2 — classify who was on the call

Two signals, deterministic first.

### 2a. Phone-number list (authoritative)

```js
// Carrier and lender agent-service lines. E.164, no punctuation.
// SEED LIST — verify and extend from your own outbound call log.
const CARRIER_NUMBERS = new Map([
  // ['+18005551234', 'Travelers'],
  // ['+18005555678', 'GeoVera'],
]);

const LENDER_NUMBERS = new Map([
  // ['+18885550001', 'Wells Fargo'],
]);
```

To populate it, rank your outbound destinations by frequency — carriers will be the top repeat
numbers by a wide margin:

```js
// One-off: group recorded outbound calls by `to.phoneNumber`, sort desc, eyeball the top ~40.
```

### 2b. Transcript markers (fallback for unlisted numbers)

Carrier agent-service lines announce themselves, and agency staff speak in the third person about
the insured. Require **two** independent signals before classifying as Carrier, so a customer who
happens to say "Travelers" isn't misfiled.

```js
const CARRIER_PATTERNS = [
  /thank you for calling\s+(travelers|geovera|liberty mutual|bamboo|progressive|safeco|mercury|hartford|nationwide|chubb|kemper|foremost|aspen|palomar|swyfft|branch|openly)/i,
  /agent[- ]?services/i,
  /if you'?re not a[n]?\s+\w+\s+(insurance\s+)?agent/i,
  /(producer|agency|agent)\s+(code|number|id)/i,
  /for agents\b|\/4agents/i,
];

const THIRD_PARTY_INSURED = /\b(the insured|our client|my client|the client'?s policy|for the insured)\b/i;

const LENDER_PATTERNS = [
  /\b(loss payee|mortgagee clause|escrow (officer|account)|loan number|title company)\b/i,
  /evidence of insurance for (the )?(closing|loan)/i,
];

const INTERNAL_HINT = /\b(extension \d{3,5}|transfer(ring)? you to|internal)\b/i;

function classifyCallParty(record, transcript, answered) {
  const to   = (record.to   && record.to.phoneNumber)   || '';
  const from = (record.from && record.from.phoneNumber) || '';
  const t = transcript || '';

  // Both parties internal -> staff to staff.
  const fromExt = record.from && record.from.extensionNumber;
  const toExt   = record.to   && record.to.extensionNumber;
  if (fromExt && toExt) return 'Internal';

  // Authoritative number match.
  for (const n of [to, from]) {
    if (CARRIER_NUMBERS.has(n)) return 'Carrier';
    if (LENDER_NUMBERS.has(n))  return 'Lender';
  }

  // Heuristics only make sense on outbound; inbound is overwhelmingly customers.
  if (record.direction === 'Outbound') {
    const carrierHits = CARRIER_PATTERNS.filter(p => p.test(t)).length
                      + (THIRD_PARTY_INSURED.test(t) ? 1 : 0);
    if (carrierHits >= 2) return 'Carrier';
    if (LENDER_PATTERNS.filter(p => p.test(t)).length >= 2) return 'Lender';
  } else {
    if (LENDER_PATTERNS.filter(p => p.test(t)).length >= 2) return 'Lender';
  }

  if (record.direction === 'Inbound') return 'Customer';
  if (INTERNAL_HINT.test(t) && !to && !from) return 'Internal';
  return 'Unknown';
}
```

### 2c. Only mine questions from customer calls

This is the change that actually cleans the Customer Questions table:

```js
const party = classifyCallParty(record, transcript, answered);
fields['Call Party'] = party;

// Question mining: customers only. Carrier/internal calls produce questions the
// AGENCY asked, which are useless for content and misleading for agent training.
if (party === 'Customer') {
  const questions = await mineQuestions(transcript);
  for (const q of questions) {
    await createQuestionRow({
      Question: q.text,
      Topic: q.topic,
      Date: record.startTime.slice(0, 10),
      Agent: fields['Agent'],
      'Recording ID': recordingId,
      'Call Party': party,                 // denormalized for easy filtering
      Direction: record.direction,
    });
  }
}
```

### Backfill for existing rows

`Call Party` can be derived from stored transcripts already in Airtable — no re-transcription
needed. Run `classifyCallParty` over the 1,414 existing rows, write the field, then stamp
`Call Party` + `Direction` onto the 2,060 question rows via their `Recording ID`.

Once that's done, the honest customer-question set is
`Call Party = Customer AND Direction = Inbound`.

---

## Roster note

Two things invalidate the coverage table I produced earlier — regenerate it after this ships:

- **New staff have been added** since the extension list I pulled, so anyone new looked like a
  gap when they simply weren't in my snapshot.
- **Gabriela Flores is no longer employed** (19 historical recordings). Keep her rows — they're
  valid history — but she'll no longer appear in the live extension directory, which is exactly
  why `findAnsweringExtension` falls back to the stored extension number rather than requiring a
  current directory hit.

Build the coverage report from the live directory joined to recorded-call counts, rather than a
hardcoded roster, so it stays correct as people come and go.
