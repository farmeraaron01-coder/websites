---
name: check-agent
description: Diagnose why inbound calls are being missed, dropped, or sent to voicemail on a RingCentral phone system — for a specific person, AI voice agent, extension, call queue, or phone number. Use this whenever someone says calls are being missed, that a person or agent "isn't answering", that callers are landing in voicemail, that a line "might be broken", or asks you to "check on" someone's phone or extension. Also use it for any RingCentral call-routing, ring-order, queue, forwarding, or dead-air investigation, even when the user doesn't say "RingCentral" explicitly.
---

# Diagnosing missed calls on RingCentral

Someone reports "calls are being missed and X should be answering them." Your job is to find
the actual mechanism losing the calls and report it with numbers, then propose a fix.

The instinct is to check the person's extension settings and stop there. Resist it. In practice
the extension is usually fine and the loss happens somewhere in the routing *path* — in what
order things ring, how long dead air lasts before the call reaches whoever can answer, and
whether callers hang up before that point. The whole job is finding where in the chain callers
give up.

## Setup

Credentials live in a `.env` file. Ask the user for the path if you don't have it. Required:

```
RC_CLIENT_ID, RC_CLIENT_SECRET, RC_JWT (or RC_JWT_TOKEN), RC_SERVER_URL
```

`scripts/rc_client.py` handles JWT auth and rate-limited GETs. Import it rather than rewriting
auth — RingCentral's call-log API is in the "Heavy" throttle group (~10 requests/minute) and
returns `429` with a `Retry-After` header that must be honored, which is easy to get wrong.

Everything here is **read-only**. Never change live call routing without explicit permission,
even if the token has `EditExtensions` scope — you'd be silently editing a production phone
system. Recommend changes and let the user apply them.

Treat the credentials as secrets: don't echo them, don't write them into the repo, and delete
any scratch copies when you're done.

## Step 1: Establish what the "agent" actually is

Before anything else, find out whether the thing that should be answering is a **human** or an
**AI voice agent** (ElevenLabs, Twilio, or similar). This single fork changes the entire
diagnosis, and getting it wrong sends you down a dead end.

```
GET /restapi/v1.0/account/~/extension?perPage=1000
```

Match on name or `extensionNumber`. Names like "Sarah AI" are a strong hint, but confirm it —
check the `.env` for AI provider keys (`EL_*`, `ELEVENLABS_*`, `TWILIO_*`), and look for agent
or dashboard entries naming the same person.

**Why this matters so much:** an AI voice agent usually answers on a number belonging to its own
provider, *not* on its RingCentral extension. So its RingCentral extension can look completely
dead — zero calls, or nothing but failures — while the agent is in fact answering calls
normally all day through the other path. If you judge health from the RingCentral extension log
alone you will confidently report a working agent as broken.

So when the target is an AI agent, always check the provider side too before drawing any
conclusion:

```bash
curl -H "xi-api-key: $EL_API_KEY" \
  "https://api.elevenlabs.io/v1/convai/conversations?agent_id=$AGENT_ID&page_size=100"
```

Look at conversation counts per day, and pull one conversation's `metadata.phone_call` to see
which number calls actually arrive on (`agent_number`) and via which provider (`type`). That
number — not the RingCentral DID — is where the agent really lives.

If the user says "she answered a call this morning," believe them and reconcile. A contradiction
between your data and their lived experience means you're reading the wrong path, not that
they're mistaken.

## Step 2: Find the number the lost calls actually arrive on

Callers dial a published number, not an extension. Get the account-wide inbound log and build a
per-number scorecard, because the number with the losses is often not the one anyone expected:

```
GET /restapi/v1.0/account/~/call-log
    ?view=Detailed&direction=Inbound&dateFrom=<ISO>&perPage=1000&page=N
```

`view=Detailed` is essential — it returns the `legs` array, which is the entire diagnosis. Page
until `navigation.nextPage` is absent. Count `Missed`, `Voicemail`, `Rejected`, `Busy` and
`Call Failed` as lost; `Accepted` and `Received` as answered.

If the user provides a specific missed-call notification (email, screenshot), use the number and
timestamp on it to anchor the investigation on the right line — it's the strongest signal you'll
get about which line they actually care about.

`scripts/analyze_routing.py` produces the scorecard and the per-call leg traces:

```bash
python scripts/analyze_routing.py --env <path-to-.env> --days 30
python scripts/analyze_routing.py --env <path-to-.env> --number +18555867467 --days 30
```

## Step 3: Read the leg traces

Legs are the ordered story of one call. Compare a lost call against an answered one on the same
number — the difference between them is your answer.

**One number often traverses several queues.** A published number may hit a site, then a
day/night rule, then land in any of a few queues, or bypass queues entirely and terminate on an
individual user's extension (where the call dies in that person's personal voicemail and no queue
rule applies). Enumerate every queue and destination that appears in the traces, then compare
their timers and overflow destinations side by side:

| Queue | Max wait | Overflow goes to |
|---|---|---|
| Flood Service | 30s | AI agent ✅ |
| RB Operator Control | **3 min** | **voicemail** ❌ |

The misconfigured one is rarely the one named after the problem. In the case above, both queues
named "Flood" were configured correctly and the losses were all in a queue named after the
agency's operator desk. Checking only the obviously-named queues would have found nothing wrong
and produced a dead end.

**A duration that exceeds a queue's cap is proof the call was never in that queue.** If a queue
hands off at 30s and your lost calls ran 49–107s, they were governed by some other rule. Use this
to eliminate queues quickly instead of guessing — it's the fastest way to find which of several
plausible paths a call actually took.

Leg types you'll see:

| `legType` | Meaning |
|---|---|
| `Accept` | Call arriving at the number / queue / site |
| `PstnToSip` | Ringing an internal extension's device |
| `FindMe` | FindMe/FollowMe forwarding, **including to external numbers** |
| `RingDirectly` | Straight to a target, no queue hunt |
| `SipForwarding` | Handoff to an external SIP endpoint (a bridge/PBX) |

Reasons worth recognizing:

- **`IP Phone Offline` / `No Digital Line`** with `duration=0` — a device slot with no digital
  line. Instant and harmless. It consumes no caller time, so do not report it as wasted ring
  time. Extensions commonly emit one real ring leg plus one of these zero-second legs.
- **`Resource Error`** on `SipForwarding` — the external SIP endpoint didn't accept the call.
  Genuine breakage of that bridge, but check whether that path is still in use before blaming it
  for current complaints; a dead path nobody dials anymore explains nothing.
- **`No Answer` / `Not Answered`** with a real duration — a legitimate ring nobody picked up.
  This is the dead air that matters.

## Step 4: Measure dead air correctly

This is where the analysis goes wrong most easily, so be deliberate.

**Dead air** = time a caller spends listening to ringing before reaching anyone who can answer.
To measure it, sum leg durations *before* the leg that finally connects — but **only on calls
where that earlier leg did not answer**.

The trap: if you sum every leg to an extension across all calls, you include calls where that
person *picked up and talked for four minutes*. Talk time is not wasted ring time. Doing this
inflates the number wildly and produces a confident, wrong accusation against a colleague who
is actually doing their job. Exclude legs whose result is `Accepted` or `Call connected` from
any "wasted time" figure.

Then get the hang-up distribution — the single most decision-relevant number in the whole
investigation:

```
sorted duration of every lost call
```

If many callers hang up in the first 10–15 seconds, then reordering anything *later* in the ring
sequence cannot save them; they were gone before that point. The only thing that helps those
callers is shortening the earlier ring so the handoff happens sooner. Say this explicitly,
because it's the difference between a fix that works and one that changes nothing.

Also split answered vs lost by hour of day. Losses concentrated in business hours point at ring
order or staffing; losses only outside them point at an after-hours rule.

## Step 5: Report

Lead with the mechanism in one or two sentences, then the numbers that prove it, then the fix.
Show the actual ring chain — it makes the problem self-evident:

```
Caller → queue greeting
       → ext 212   (rings ~20s, no answer)
       → ext 215   (offline, 0s)
       → FindMe → external cell (~10s)
       → agent finally answers
```

Include: total calls and losses over the window with a percentage; median and max dead air; the
hang-up distribution; and which specific step to change. Quantify the fix's expected effect, and
be honest when part of the loss is beyond its reach.

## Known API limitations

- **`answering-rule` returns 403 `CMN-468`** on accounts with `NewCallHandlingAndForwarding`
  enabled. There's no read path for ring order on these accounts — infer it from the leg traces
  instead, and route the user to the admin UI for changes. Don't burn time fighting this.
- **`presence` returns 403** without `ReadPresence` scope. Not fatal; skip it.
- Company/main numbers return no `extension` from `/account/~/phone-number` because they land on
  an IVR rather than an extension. Trace them through legs.

See `references/ringcentral-api.md` for endpoint details, the admin-UI click path for fixing
ring order, and worked examples of leg traces.
