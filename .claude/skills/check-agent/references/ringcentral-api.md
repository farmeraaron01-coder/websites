# RingCentral reference for missed-call diagnosis

Contents:
1. Auth
2. Endpoints that matter
3. Leg types and reasons
4. Worked example: AI agent placed last in ring order
5. Fixing ring order in the admin UI
6. AI voice-agent providers
7. Rate limits and permission errors

---

## 1. Auth

JWT bearer flow. Client id/secret go in a Basic header; the JWT goes in the body as
`assertion`. Access tokens last ~1 hour.

```
POST {server}/restapi/oauth/token
Authorization: Basic base64(client_id:client_secret)
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={JWT}
```

- Production: `https://platform.ringcentral.com`
- Sandbox: `https://platform.devtest.ringcentral.com`

The response's `scope` field tells you what you can actually do — check it before
concluding an endpoint is broken. Account-wide call log needs `ReadCallLog` plus admin
rights on the JWT's user.

---

## 2. Endpoints that matter

```
GET /restapi/v1.0/account/~/extension?perPage=1000
    -> id, name, extensionNumber, type (User|Department|Site|Announcement...), status

GET /restapi/v1.0/account/~/call-log
    ?view=Detailed&direction=Inbound&dateFrom=<ISO>&dateTo=<ISO>&perPage=1000&page=N
    -> account-wide. view=Detailed is required for the `legs` array.

GET /restapi/v1.0/account/~/extension/{id}/call-log?...
    -> one extension only. Beware: an AI agent's extension can be empty while the
       agent is busy answering on a provider number.

GET /restapi/v1.0/account/~/extension/{id}/phone-number
GET /restapi/v1.0/account/~/phone-number?perPage=1000
    -> usageType: DirectNumber | CompanyNumber | MainCompanyNumber | CompanyFaxNumber
       Company/main numbers report no `extension` because they land on an IVR.

GET /restapi/v1.0/account/~/extension/{id}/forwarding-number
GET /restapi/v1.0/account/~/extension/{id}/business-hours
GET /restapi/v1.0/account/~/extension/{id}/device
    -> device status Online/Offline

GET /restapi/v1.0/account/~/extension/{id}/presence?detailedTelephonyState=true
    -> needs ReadPresence; dndStatus DoNotAcceptAnyCalls / DoNotAcceptDepartmentCalls
```

Paginate by following `navigation.nextPage` until absent.

Date format: `2026-07-29T00:00:00.000Z`.

---

## 3. Leg types and reasons

`record.legs` is the ordered story of the call. Read it top to bottom.

| legType | Meaning |
|---|---|
| `Accept` | Arrival at number / site / queue |
| `PstnToSip` | Ringing an internal extension's device |
| `FindMe` | FindMe/FollowMe forwarding, including to external numbers |
| `RingDirectly` | Straight to target, no hunt |
| `SipForwarding` | Handoff to an external SIP endpoint (bridge/PBX) |
| `Transfer`, `Park`, `Pickup` | Self-explanatory |

Results: `Accepted`, `Call connected`, `Missed`, `Voicemail`, `No Answer`,
`Stopped`, `IP Phone Offline`, `Call Failed`, `Rejected`, `Busy`.

Reasons worth knowing:

- **`No Digital Line`** (with `IP Phone Offline`, `duration=0`) — a device slot with no
  digital line assigned. Zero seconds, costs the caller nothing. Extensions frequently
  emit one real ring leg plus one of these. **Never count these as wasted ring time**;
  they are noise, not the bug.
- **`Resource Error`** (with `SipForwarding`) — the external SIP endpoint refused or was
  unreachable. Real breakage of that bridge. Before blaming it for a current complaint,
  check whether any calls still traverse that path — a dead route nobody dials explains
  nothing about today's missed calls.
- **`Not Answered`** with a real duration — a genuine ring nobody picked up. This is the
  dead air that costs you callers.
- **`Stopped`** — leg abandoned because the caller hung up or the hunt moved on.

---

## 4. Worked example: AI agent placed last in ring order

Real case. Complaint: "calls are being missed, Sarah should be answering them."

Sarah is an ElevenLabs voice agent. Her RingCentral extension (106) showed **zero calls
in 10 days** and, before that, only failures — which looks like a dead agent. It wasn't.
She was answering all day on the Twilio number `+18588284747`; her RingCentral DID had
simply fallen out of use. Confirming on the provider side prevented a wrong conclusion.

The actual losses were on `+18555867467` (Jump Trucking Sales): **124 calls / 30 days,
23 missed**.

An answered call:

```
Accept        Accepted         dur=245  -> +18555867467 Jump Trucking Sales
PstnToSip     No Answer        Not Answered  dur=20  -> ext 212
PstnToSip     IP Phone Offline No Digital Line dur=0 -> ext 212
PstnToSip     Stopped          dur=10   -> ext 215
FindMe        Call connected   Accepted dur=206 -> +18588284747   <- agent, last
```

A missed call, same number, same day:

```
Accept        Missed           dur=13   -> +18555867467 Jump Trucking Sales
PstnToSip     Stopped          dur=6    -> ext 212
PstnToSip     IP Phone Offline No Digital Line dur=0 -> ext 212
                                          (caller hung up at 13s — never reached agent)
```

Diagnosis: the agent sat **last** in the sequence, behind ~30s median dead air. Half the
calls never reached her because callers hung up first.

Two mistakes made while diagnosing this, both worth avoiding:

1. **Judging the agent's health from her RingCentral extension alone.** Reported her as
   broken; she was working normally on the provider number.
2. **Summing every leg to ext 212 to compute "wasted ring time."** That produced
   "12,812 seconds / 3.5 hours," but it included calls where that salesperson answered
   and talked for minutes. Excluding `Accepted` / `Call connected` legs gives the real
   figure: ~20s of unanswered ring per affected call.

The hang-up distribution is what made the fix actionable:

```
1, 1, 1, 1, 1, 1, 1, 2, 6, 7, 7, 8, 13, 13, 17, 18, 19, 24, 31, 32, 36, ...
```

About half gave up within 15 seconds. Removing a *later* member of the sequence would
not have saved a single one of them — only shortening the first ring would.

---

## 4b. Worked example: the misconfigured queue wasn't the one named after the problem

Same account, second investigation. Complaint: "check the dropped calls from flood."

`+18552253566` (California Flood) was losing **218 of 678 calls in 10 days (32%)** — five times
the volume of the first case. Unlike the impatient Jump Trucking callers, these people waited
**49, 61, 83, 91, 107 seconds** and still ended in voicemail. Patient, motivated callers getting
nothing.

The obvious suspects were the two queues named **Flood Sales** and **Flood Service**. Both turned
out to be configured correctly — 30s cap, overflow to the Brooke AI agent, Simultaneous ring.
Reporting "the flood line has no AI backstop" was wrong, and checking only the obviously-named
queues would have ended the investigation with nothing found.

What resolved it was a duration argument. **Flood Service hands off at 30 seconds, but the lost
calls ran 49–107 seconds — so they were never in Flood Service.** They were in a third queue,
`RB Operator Control`, named after the agency's operator desk and easy to overlook:

| Queue | Max wait | Overflow destination |
|---|---|---|
| Flood Service | 30s | external → AI agent ✅ |
| Flood Sales | 30s | external → AI agent ✅ |
| **RB Operator Control** | **3 minutes** | **voicemail** ❌ |

Six times the timer, and a mailbox at the end of it instead of an agent. Callers held for up to
three minutes, then dropped into a queue voicemail box accumulating ~400 messages a month.

Some flood calls also bypassed queues entirely and terminated on individual users' extensions
(`Accept → Chandra Taft`, then `PstnToSip → ext 331`, then `FindMe → Stopped`), dying in personal
voicemail where no queue rule could help them.

Transferable lessons:

- Enumerate **every** destination in a number's traces before reading any config. Use
  `analyze_routing.py --number <n>`, which prints the destination table for exactly this.
- Compare max-wait and overflow **across all of them**. The outlier is the leak.
- Trust the duration arithmetic over the naming. A lost-call duration exceeding a queue's cap is
  proof of absence from that queue, and eliminates candidates faster than reading settings.
- A queue's name reflects org history, not call flow. Check staffing to judge whether an AI
  backstop suits it — here all nine `RB Operator Control` agents were on the California Flood
  site, which made the flood agent the right destination despite the name.

## 5. Fixing ring order in the admin UI

On accounts with `NewCallHandlingAndForwarding`, the answering-rule API is read-blocked
(403 `CMN-468`), so changes happen in the UI. At **service.ringcentral.com** as admin:

For a call queue / department:

```
Phone System -> Groups -> Call Queues -> <queue name>
  -> Call Handling -> Business Hours
     - ring order (Sequential / Rotating / Simultaneous)
     - ordered member list       (reorder or remove members here)
     - ring duration per member  (shorten to cut dead air)
```

An **external** number (an AI agent's provider number, a cell) cannot be a plain queue
member. If the traces show a `FindMe` leg to an external number, it's configured as
forwarding on the extension instead:

```
Users (or Groups) -> <extension> -> Call Handling & Forwarding -> Business Hours
  -> ordered forwarding list (desk phones first, then external numbers)
```

Guidance worth giving the user: put the always-available answerer (usually the AI agent)
**early enough that callers reach it before they give up** — informed by the hang-up
distribution, not by intuition. Trimming the first human's ring from ~20s to ~12–15s
typically recovers more calls than reordering anything further down.

---

## 6. AI voice-agent providers

Look for these in the `.env`: `EL_*` / `ELEVENLABS_*` (ElevenLabs), `TWILIO_*`,
`VAPI_*`, `RETELL_*`.

ElevenLabs conversational agents:

```
GET https://api.elevenlabs.io/v1/convai/agents
GET https://api.elevenlabs.io/v1/convai/conversations?agent_id={id}&page_size=100
GET https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}
Header: xi-api-key: {EL_API_KEY}
```

The single-conversation response carries `metadata.phone_call`:

```json
{"direction":"inbound","agent_number":"+18588284747",
 "external_number":"+13608192124","type":"twilio","call_sid":"CA..."}
```

`agent_number` is where the agent truly answers, and `type` names the carrier. Cross-check
this against the RingCentral DID — when they differ, RingCentral's view of the agent is
incomplete by design.

---

## 7. Rate limits and permission errors

- Call log is in the **Heavy** group, ~10 requests/minute. Sleep ~7s between pages and
  honor `Retry-After` on 429 (`CMN-301 Request rate exceeded`). Long pulls otherwise die
  halfway with confusing partial data.
- Media/recording downloads are in a more generous group.
- `403 CMN-468` on `answering-rule` — `NewCallHandlingAndForwarding` is enabled; no read
  path exists. Infer ring order from legs and send the user to the UI.
- `403 InsufficientPermissions` on `presence` — missing `ReadPresence`. Non-fatal, skip.
- Company-level numbers legitimately return no `extension`; they land on an IVR.
