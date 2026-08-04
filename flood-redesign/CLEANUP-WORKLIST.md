# Cleanup worklist — seven sessions, in order

Each session is one sitting, one paste into Claude in Chrome, and one thing to report back.
Do them in this order. `ACCOUNTS.md` holds the reasoning; this file is just the work.

**One sequencing rule that matters:** the old Divi sites do **not** emit the `cfi_form_submit`
event — only the new theme does. So the new conversion triggers get *built* now (they sit dormant,
harmless), and the *old* click triggers get switched off during the cutover, not before. Session 2
covers the build; the switch-off is step 8 of the flip in `LAUNCH.md`.

| # | Session | Risk | Time | When |
|---|---|---|---|---|
| 0 | Export a dated baseline | None | 15 min | Before session 2 |
| 1 | Remove stale access | None | 15 min | Now |
| 2 | Build the new conversion tracking | None (dormant until cutover) | 45 min | Before cutover |
| 3 | Search Console domain properties | None | 15 min | Before cutover |
| 4 | Delete 14 empty GA4 accounts | None | 10 min | Any time |
| 5 | GA4 renames, moves, and dead duplicates | Low | 45 min | Any time |
| 6 | GTM tidy-up | Low | 30 min | Any time |
| 7 | Google Ads goal cleanup | Resets bidding | 45 min | **Not** in cutover week |

Sessions 4, 5 and 6 are hygiene. They are genuinely optional and they do not improve bidding — do
them when there is a quiet hour, not before sessions 2 and 7.

---

## Go / no-go gate — before any conversion tag is published or any campaign goal changes

Five things documented, from a second review's list. All five are answerable from sessions 0–2; none
requires guessing.

| # | Evidence | Where it comes from | Status |
|---|---|---|---|
| 1 | Exact trigger logic for the California and Statewide Google Ads **and** Bing conversion tags | Session 2 read-backs | Google side confirmed (click triggers, "Click Text contains SUBMIT"); **Bing side unknown** |
| 2 | One valid quote = one lead event; staff = zero; failed validation = zero | Test A above | Not yet run |
| 3 | Proof the test cannot send a live conversion to either platform | Test A runs with no container loaded; plus the staging-hostname exception | Design settled |
| 4 | Campaign-to-goal map for every flood campaign | Delivered 4 Aug — 46 flood campaigns, 44 on Account-default, 2 Demand Gen campaign-specific | **Closed** |
| 5 | Current Search Console verification method for both launch sites | Session 3 step 1 | Unknown for statewide |

Evidence 1 and 5 are the two remaining unknowns, both cheap reads. Item 4 arrived on 4 Aug and
surfaced a finding of its own — see *What the map showed* below.


---

## Session 0 — Export a dated baseline

Added on a second review's suggestion, and it was a good one. Before changing any measurement, take a
snapshot so "did this help?" is answerable later and a rollback has something to compare against.

```
Read-only export. From Google Ads (account 890-760-9729) and Microsoft Ads (X2012441),
export or copy into plain tables, all for the last 30 days, and label everything with
today's date:

  - every campaign: name, status, bid strategy, budget, spend, conversions, cost/conv
  - every campaign's conversion goal setting (account-default vs campaign-specific, and
    which actions if specific)
  - every conversion action / goal: name, type, source, category, primary or secondary,
    count setting, and whether it has recorded anything in the last 30 days
  - the account-level conversions and cost-per-conversion totals

Save it somewhere I can find it later. Do not change anything.
```

**Report back:** confirmation it is saved, plus the account totals so we have them written down.

---

## Session 1 — Remove stale access

Why first: anyone with GTM publish rights can inject JavaScript into every page of the site,
including code that reads form fields as they are typed. Six external identities hold it, one a
freelancer address last used in 2022 across ten containers.

Two passes, on a second review's advice: **list first, then remove what I approve.** Removing an
account's last administrator, or a user who is the sole link owner on an integration, is not something
to discover afterwards.

**Pass 1 — read only:**

```
Read-only access inventory across four platforms. Change nothing.

1. GTM (tagmanager.google.com → Admin → User Management). Report the account-level user
   list, then each container's user list. For every user: email, account-level role, and
   container-level permission (None / Read / Edit / Approve / Publish).

2. GA4 (Admin → Account access management, and Property access management for the
   californiafloodinsurance.com and statewidefloodinsurance.com properties). Every user,
   their role, and whether they are marked as the account creator.

3. Google Ads (Admin → Access and security). Every user, access level, and status.
   Also list users on the manager account "Aaron Manager Account" (909-487-9776).

4. Microsoft Ads (Settings → Account access). Every user and role.

For each platform, also tell me: how many users hold the highest role. I need to know
whether removing anyone would leave an account with no administrator.

Report as one table per platform. Change nothing.
```

**Report back:** the four tables. I will mark which to remove and which to downgrade, and you approve
that list before pass 2 runs. The expected candidates are the three 2022 Gmail addresses
(`aliofficialfiverr@`, `zainarshad866@`, `yas17sheikh@`) for removal, and the two agency addresses
(`info@excellero.com`, `kylewaters@max-conversion.com`) for downgrade from Publish to Edit, scoped to
the one container each works on. But that is a prediction, not an instruction — the tables decide.

---

## Session 2 — Build the new conversion tracking

This is the one that stops your staff form counting as a paid lead. It is currently doing that on
**both** Google Ads and Bing.

The new tags will not fire until the new sites are live, so this is safe to publish today.

```
I need to add new conversion tracking to two GTM containers. The websites now push a
custom dataLayer event on a genuinely successful form submission, and I want conversions
to fire from that instead of from click triggers.

The event looks like this:
  event: 'cfi_form_submit'
  cfi_form_role: 'quote' | 'staff' | 'claims' | 'service' | 'appointment'
  cfi_is_lead: true (only for real quote leads; false for staff phone intake)

There is also a page-level variable available on every page: cfi_page_role.

DO THIS IN BOTH CONTAINERS — GTM-MZ6RZ94 (californiafloodinsurance.com) and
GTM-PJQ72VK (statewidefloodinsurance.com):

A. Create these Data Layer Variables (Variables → User-Defined → New → Data Layer Variable):
   - cfi_is_lead
   - cfi_form_role
   - cfi_page_role

B. Create a trigger: Custom Event
   - Name: cfi_form_submit — is_lead true
   - Event name: cfi_form_submit
   - Fire on: Some Custom Events, where cfi_is_lead equals true

C. Create a second trigger: Custom Event
   - Name: cfi_form_submit — all roles
   - Event name: cfi_form_submit
   - Fire on: All Custom Events

D. Add a GA4 event tag on trigger B:
   - Name: GA4 — quote form lead
   - Event name: quote_form_lead
   - Parameter: form_role = {{cfi_form_role}}
   - Uses the existing GA4 configuration/Google tag in the container

E. Add a GA4 event tag on trigger C (so I can still see staff volume in GA4, it just
   never reaches Ads):
   - Name: GA4 — form submit (all roles)
   - Event name: form_submit_any
   - Parameter: form_role = {{cfi_form_role}}

F. (Nothing for Microsoft Ads in this step — deliberately. CFI's container already has a
   "Bing UET - request_quote (California)" tag and Microsoft already has matching Event
   goals recording. Adding another would double-count California. The Bing work is a
   repoint of what exists, handled separately below.)

G. In GTM-PJQ72VK ONLY, there are two existing Google Ads Conversion Tracking tags
   ("G. ads - statewidefloodinsurance.com - Contact_Form_Submission" and
   "G. ads statewidefloodinsurance.com - Submit_Online_Quote_Form"). COPY each one,
   name the copy with a " (event)" suffix, and set the copy's trigger to trigger B.
   Leave the originals and their click triggers exactly as they are.

IMPORTANT: do NOT delete, pause, or change any existing tag or trigger. The old
click-based triggers must keep working until the websites are switched over. We are only
ADDING the new path alongside.

Then publish, with version name "Add cfi_form_submit conversion path".

Finally, tell me: in GTM-MZ6RZ94, list the existing GA4 event tags and their current
triggers (I need to know which ones to retire later), and open the container quality
warnings on GTM-PJQ72VK and tell me exactly what the two "Urgent" issues are.
```

**Report back:** the list of CFI's existing GA4 event tags with their triggers, and what
statewide's two Urgent issues are.

### The end-to-end test — corrected, because my first version was unsafe

A second review caught a real hole in the test I proposed, and it is worth being blunt about: I had
you open staging with `?cfi_tags=1`, which **loads the live container**. The existing click trigger
("Click Text contains Submit Application") would then have fired on the test submission and sent a
**real conversion** to Google Ads and Microsoft Ads — the exact pollution this whole exercise exists
to prevent. Do not run that version.

**The fix is simpler and completely safe: test without GTM at all.** The theme's dataLayer push is
not host-gated — only the container is. So the event can be proven with the container absent, which
means no tag can possibly fire.

**Test A — the event itself (no GTM, zero risk):**

1. Open `https://new.californiafloodinsurance.com/get-a-quote/` — **no `?cfi_tags=1`**. Confirm in
   the page source that there is no `googletagmanager.com/gtm.js` request (Network tab, filter "gtm").
2. Open the browser console and run `window.dataLayer` — note how many entries exist.
3. Fill the form with obvious test data and **submit it for real.**
4. When the confirmation appears, run in the console:
   `window.dataLayer.filter(e => e.event === 'cfi_form_submit')`
   Expect **exactly one** entry, `cfi_form_role: "quote"`, `cfi_is_lead: true`.
5. Repeat on `/staff-form/`. Expect exactly one entry with `cfi_form_role: "staff"`,
   `cfi_is_lead: false`.
6. Also confirm the negative: reload, click Submit with the form deliberately incomplete so
   validation rejects it, and confirm the filter returns **zero** entries.
7. Delete the two test entries from Cognito.

That establishes one valid quote = one lead event, staff = no lead event, failed validation = no
event, with no possibility of a conversion reaching either ad platform.

**Test B — that the tags respond correctly** can only be done where the container loads, which means
after cutover. It is already in the post-flip checklist in `LAUNCH.md`, using GTM Preview.

**And a permanent safeguard, worth adding while in the container** — so that no future test, and no
accidental `?cfi_tags=1`, can ever send a conversion from a staging hostname:

```
In BOTH containers (GTM-MZ6RZ94 and GTM-PJQ72VK), add a blocking exception to every
Google Ads Conversion Tracking tag, every Bing/Microsoft UET conversion-event tag, and
every GA4 event tag that Google Ads imports as a conversion.

Create the exception trigger with ONE condition, using a regex — because GTM combines
multiple conditions inside a single trigger with AND, so two "contains" rows would mean
"hostname contains new. AND contains staging.", which matches nothing and would block
nothing while looking correct:

  - Type: Page View
  - Name: BLOCK — staging hostnames
  - Fire on: Some Page Views
  - Condition: Page Hostname  matches RegEx  ^(new|staging)\.

That single condition matches new.californiafloodinsurance.com and
staging.statewidefloodinsurance.com and nothing else.

(If you would rather avoid regex: create TWO separate Page View triggers, one with
Page Hostname contains "new." and one with contains "staging.", and attach BOTH as
exceptions to each tag. Separate triggers are ORed; conditions within one trigger are
ANDed. What you must not do is put both hostname tests in one trigger.)

Add that trigger under "Exceptions" on each of those tags. Do not change their firing
triggers. Publish as "Block conversion tags on staging hostnames".

Then tell me which tags you added it to, and confirm by opening GTM Preview on
new.californiafloodinsurance.com/get-a-quote/?cfi_tags=1 that the conversion tags show
as BLOCKED rather than fired. A safeguard nobody verified is not a safeguard.
```

This is a keep-forever safeguard, not a temporary one: it means the staging sites can never report a
conversion no matter what anyone does to them.

---

## Session 3 — Search Console domain properties

Statewide's verification is the launch blocker: if it is an HTML file in the web root, the cutover
deletes it and un-verifies the property exactly when the sitemap needs submitting.

```
In Google Search Console:

1. First, tell me the verification method currently listed for
   statewidefloodinsurance.com (open the property → Settings → Ownership verification)
   and for californiafloodinsurance.com. I need the exact methods listed as verified.

2. Then add a new DOMAIN property for each of these two, if one does not already exist:
     - californiafloodinsurance.com
     - statewidefloodinsurance.com
   Choose "Domain" (not URL prefix). Google will give you a TXT record for each — give me
   the exact record values to add at the DNS host, and tell me which host the domains use
   if you can see it.

3. Do NOT delete the existing URL-prefix properties. They can stay.

Report the verification methods from step 1 and the TXT records from step 2.
```

**Report back:** the two verification methods, and the TXT record values. Add those at your DNS
host, then have it confirm verification.

---

## Session 4 — Delete 14 empty GA4 accounts

Zero properties means zero data means nothing to lose. This removes half the clutter on its own.

```
In Google Analytics (analytics.google.com → Admin), I want to delete GA4 ACCOUNTS that
contain no properties at all. Here is the list:

  4S Ranch Insurance
  ApartmentInsuranceOnline.com
  ATPinsuranceprograms
  Carlsbad Insurance
  contractorsinsurancepros.com
  Del Mar Insurance
  Encinitas Insurance
  Escondido Insurance
  floridafloodinsurance.net
  Mira Mesa Insurance
  New Mexico Flood
  Oregon Flood
  Rancho Bernardo Insurance
  Scripps Ranch Insurance

For EACH one: first open it and confirm it has zero properties. If it has zero, move the
account to trash (Admin → Account Settings → Move to trash). If it has ANY property, skip
it and tell me — do not delete it.

Report which you deleted and which you skipped, and why.
```

**Report back:** deleted vs skipped.

---

## Session 5 — GA4 renames, moves, and dead duplicates

```
Three jobs in Google Analytics. Nothing here deletes anything that holds data.

JOB 1 — Rename properties to "<domain> (<measurement ID>)" so they are identifiable in
the switcher. Current name → new name:

  Cali Flood Insurance - GA4                → californiafloodinsurance.com (G-3YMN51H7LE)
  statewidefloodinsurance.com-GA4 (314831122) → statewidefloodinsurance.com (G-FH3Q6GKNHH)
  cheap earth quake insurance               → cheapearthquakeinsurance.com (G-LDG2DGK9BE)
  Arizona Flood Ins - GA4                   → arizonafloodinsurance.net (G-QHXQEYL237)
  Farmers Insurance - GA4                   → farmerinsurance.com (G-K6FT0WCEEX)
  Texas Flood - GA4                         → texasfloodinsurance.net (G-JG0D145RBQ)
  Washington Flood Insurance-GA4            → washingtonfloodinsurance.com (G-G54S6F6N7F)
  Restaurant-Insurance - GA4                → restaurant-insurance.com (G-DE01249V0H)
  property 314801581 (currently unnamed)    → cheapsoberlivinginsurance.com (G-B5M0MYQ0QQ)
  CheapLandlordInsurance                    → cheaplandlordinsurance.com (G-PK2G20NR6D)
  sandiegofloodinsurance.com                → sandiegofloodinsurance.com (G-6SDDPL7N6B)
  pestcoverage.com                          → pestcoverage.com (G-L34P627B0Y)
  TopDogPetInsurance                        → topdogpetinsurance.com (G-7TJ6DKERLW)
  jumpins.com property 314345658            → jumpins.com (G-KSYS0430MS)
  homeownersassociationinsurance.net-GA4    → homeownersassociationinsurance.net (G-R2R8DL1JY9)

JOB 2 — Fix data stream URLs that are still http://. For each of these properties, open
Admin → Data streams → the web stream, and change the stream URL to the https:// version
of the same domain (keep www or non-www exactly as it is now, just change the protocol):
  arizonafloodinsurance.net, californiafloodinsurance.com, cheapsoberlivinginsurance.com,
  farmerinsurance.com, homeownersassociationinsurance.net, statewidefloodinsurance.com,
  restaurant-insurance.com, texasfloodinsurance.net, washingtonfloodinsurance.com

JOB 3 — Mark four dead duplicate properties for deletion. Each has never received data.
For each: FIRST confirm in Reports that it shows no data ever received. If confirmed,
RENAME it (do not delete yet) to "ZZ DELETE — never received data":
  - cheapearthquakeinsurance.com-GA4, property 389773239 (G-NT5FM4Q85H)
  - statewidefloodinsurance.com-GA4, property 371465506 (G-NCF8CTTSQS)
  - jumpins.com - GA4, property 371490137 (G-H4XXCW8HT4)
  - TEMP - placeholder, property 545006633 (G-LBMCGFX7GC)
If any one of them HAS received data, leave it alone and tell me.

JOB 4 — One more fix on californiafloodinsurance.com (property 314823941): go to Admin →
Key events. There are three marked: Contact_Form_Submission, purchase, and
Submit_Online_Quote_Form_Submission. UNMARK "purchase" as a key event — it is a GA4
default with no meaning on an insurance site. Leave the other two alone.

Report what you renamed, which stream URLs you fixed, whether all four duplicates were
confirmed empty, and confirmation that "purchase" is unmarked.
```

**Report back:** all four job results.

There are also two properties filed under the wrong account. These need a **property move**, which
keeps the measurement ID and all history:

```
Two GA4 properties are sitting inside another business's account. Move each to its own
new account (Admin → Property → Property change history / Move property, or Admin →
Property Settings → Move property):

1. "Mrtacoshop.com" (property 545014697) is inside the arizonafloodinsurance.net account.
   Move it to a new account named "Mr Taco Shop".
2. "vacanthomeinsurance.com" (property 545039395) is inside the
   californiafloodinsurance.com account. Move it to a new account named
   "vacanthomeinsurance.com".

A property move preserves the measurement ID and all historical data — confirm that is
what the interface tells you before you confirm each move. If GA4 warns about anything
other than access changes, stop and tell me.
```

---

## Session 6 — GTM tidy-up

```
Housekeeping in Google Tag Manager. Nothing here should change how any live site tracks.

1. RENAME two containers (drop the www prefix so they match the convention):
   - "www.cheaplandlordinsurance.com" → cheaplandlordinsurance.com
   - "www.vacanthomeinsurance.com"    → vacanthomeinsurance.com

2. DELETE two empty containers. First confirm each has zero tags and only an
   "Empty Container" version, then delete:
   - GTM-53H3GF24 (mytruckinginsurance.ai)
   - GTM-W8F3276K (www.vacanthomeinsurance.com)
   If either has any tag at all, skip it and tell me.

3. In GTM-MZ6RZ94 (californiafloodinsurance.com) there are TWO Conversion Linker tags:
   "Conversion Linker" and "Conversion Linker 1". Open both and tell me their triggers.
   Do not delete either yet — just report what each is set to.

4. Also in GTM-MZ6RZ94: the container shows a "missing Google tag" warning about
   AW-1012143191. DO NOT add a tag and DO NOT use GTM's automatic fix — a second Ads
   configuration could double-count. Instead, document it: list every tag in the container
   that references AW-1012143191 or loads a Google tag, with its type and trigger, and
   tell me what the warning says verbatim. We decide after reading it.

5. Rename Microsoft Ads UET tag 295027961 from "Lp.JunpTruckingInsurance" to
   "lp.jumptruckinginsurance.com" (fixing the "Junp" typo).

Publish GTM changes with version name "Housekeeping — naming and initialization tag".
Report the two Conversion Linker triggers from step 3.
```

**Report back:** the two Conversion Linker triggers, so we can decide which to drop.

---

## Session 7 — Google Ads goal cleanup

**Not in the cutover week.** This resets Smart Bidding learning, and if it runs alongside the site
migration you will not be able to tell which change moved your numbers. Give it 2–3 weeks on a
stable budget afterwards.

Do this only after Session 2 is live and the sites are switched over — it decides *which* signals
count, and Session 2 is what makes the signals true.

```
Google Ads account 890-760-9729. This is conversion-tracking cleanup. Do not delete any
conversion action — only change primary/secondary, counting, and campaign goals.

1. COUNTING: These TopDogPetInsurance actions are set to count "Every"; every other
   business on the account uses "One". Change all TopDog web actions to count ONE per
   click. List them for me as you go.

2. DEMOTE TO SECONDARY — but REPORT FIRST, then wait for my confirmation. For each action
   below, tell me which campaigns currently count it before changing anything. These are
   engagement events rather than leads, so the intent is Secondary, but a global demotion
   without knowing which campaigns depend on each one is how a campaign ends up with no
   primary goal at all:
     - Local actions - Website visits
     - Local actions - Menu views
     - Local actions - Directions (Get directions)
     - Local actions - Other engagements
     - Clicks to call
     - YouTube channel subscriptions
     - YouTube follow-on views
   If any of these is currently the ONLY primary action on a campaign, stop and tell me
   before changing it.

3. CAMPAIGN-LEVEL GOALS: this account runs a dozen unrelated businesses that all share
   one conversions column, so flood campaigns have been bidding partly toward other
   brands' conversions. For every FLOOD campaign (California, Statewide, and each state),
   go to Settings → Goals → "Use campaign-specific goals" and include ONLY:
     - californiafloodinsurance.com - Contact_Form
     - californiafloodinsurance.com - Submit_Online... (Request Quote)
     - the equivalent Statewide actions, on Statewide campaigns
     - the new "quote form lead" actions once they are recording
   Do the same per brand for trucking, earthquake, pest, sober living, landlord and pet
   campaigns — each counting only its own brand's lead actions.

4. ONE MORE READ, no changes: I count thirteen states running TWO flood campaigns each —
   one Manual CPC and one Maximize Conversions — sharing the same account-default goals:
   California, Florida, Georgia, Illinois, Louisiana, Massachusetts, Michigan, Missouri,
   North Carolina, Ohio, South Carolina, Tennessee, Virginia.
   For each of those 26 campaigns, give me last-90-day spend, conversions, cost per
   conversion, and impression share lost to rank and to budget. Change nothing.

Before you change any campaign goals, give me the list of flood campaigns you found and
what their goals are set to now, and wait for me to confirm.

Report step 1 and 2 as done/not-done lists, and stop for confirmation before step 3.
```

**Report back:** steps 1 and 2 complete, plus the campaign lists for steps 3 and 4 — then confirm
before step 3 proceeds.

### What the map showed — thirteen states, not two

The 4 Aug campaign map closes gate item 4, and reading down it turns up something bigger than the
goal-governance point it was built to answer.

**Thirteen states run two flood campaigns each** — one Manual CPC and one Maximize Conversions —
on the same account-default goals: California, Florida, Georgia, Illinois, Louisiana, Massachusetts,
Michigan, Missouri, North Carolina, Ohio, South Carolina, Tennessee, Virginia.

The July audit found this pattern in **two** states and priced the self-competition at roughly
$11,600/month. The full map says it is thirteen. Two things follow, and the second is the one that
matters:

1. They bid against each other in the same auction for the same geography, inflating their own CPCs.
2. **They split the conversion signal.** Because both halves share the account-default goal set,
   every conversion the Manual half takes is a conversion the Maximize Conversions half never learns
   from — so the automated campaign is being starved by its own duplicate.

The June re-look already measured what this costs in one of these very states: **Florida, Manual CPC
at $203 CPA and 2% conversion rate, against the same state's Maximize Conversions campaign at $29 and
23%.** Seven times better, same state, same product.

That is why step 4 above only *reads*. The pattern is strong and the mechanism is clear, but which
half to keep is a per-state question with real money attached, and the second review is right that a
one-size-fits-all bid change would be reckless. Get the 26-campaign spend table first.

Sequence note: this is a **campaign structure** change, which is a third category after measurement
(sessions 2 and 7 steps 1–2) and goals (step 3). Do it last, one or two states at a time, with the
Session 0 baseline as the comparison — not as a batch of thirteen.

### One useful thing to copy rather than invent

The two Demand Gen campaigns already carry campaign-specific goals, and one is named **"Statewide
Flood - Quote & Contact Leads"**. So a brand-scoped goal set already exists in this account. Open it
before building anything in step 3 — if it is well-formed, the flood search campaigns can point at
the same pattern rather than a new one invented from scratch.

---

## After all seven

Two things that are not account cleanup but are on the same list:

- **Move `google-ads-project/Google Ads/.env` out of Dropbox and rotate the Google Ads refresh
  token.** A refresh token is durable access to the whole Ads account, sitting in a synced folder.
- **Turn on "Include hidden fields" on Cognito form 5's two integration emails** (to
  `floodcognito@robot.zapier.com` and `data@insuredmine.com`). The UTM and GCLID values you capture
  are on the entry but invisible to Zapier and InsuredMine, so sales cannot see where a lead came
  from.
