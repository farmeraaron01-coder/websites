# Cleanup worklist — six sessions to do, one deferred

Each session is one sitting, one paste into Claude in Chrome, and one thing to report back.
Do them in this order. `ACCOUNTS.md` holds the reasoning; this file is just the work.

**One sequencing rule that matters:** the old Divi sites do **not** emit the `cfi_form_submit`
event — only the new theme does. So the new conversion triggers get *built* now (they sit dormant,
harmless), and the *old* click triggers get switched off during the cutover, not before. Session 2
covers the build; the switch-off is step 8 of the flip in `LAUNCH.md`.

| # | Session | Risk | Time | When |
|---|---|---|---|---|
| 0 | ~~Export a dated baseline~~ — **done 4 Aug**, in `baseline-2026-08-04/` | None | — | ☑ |
| 1 | Remove stale access | None | 15 min | Now |
| 2 | Build the new conversion tracking | None (dormant until cutover) | 45 min | Before cutover |
| 3 | Search Console domain properties | None | 15 min | Before cutover |
| 4 | Delete 14 empty GA4 accounts | None | 10 min | Any time |
| 5 | GA4 renames, moves, and dead duplicates | Low | 45 min | Any time |
| 6 | GTM tidy-up | Low | 30 min | Any time |

Sessions 4, 5 and 6 are hygiene. They are genuinely optional and they do not improve bidding — do
them when there is a quiet hour.

**Session 7 (Google Ads goal cleanup) is deliberately not in that table.** It is the only session
that touches a working system, and it is now **deferred with no date** — see *Deferred* at the end.

### Nothing in sessions 0–6 changes a bid, a budget, or a campaign goal

Worth stating plainly, because it is the thing to be sure of before starting: sessions 0 and 3 are
read-only, session 1 touches user permissions only, session 2 adds dormant tags that cannot fire
until the new sites are live, and sessions 4–6 rename and delete things no campaign references. None
of them can affect what Google Ads or Microsoft Ads bids on.

---

## Go / no-go gate — before any conversion tag is published or any campaign goal changes

Five things documented, from a second review's list. All five are answerable from sessions 0–2; none
requires guessing.

| # | Evidence | Where it comes from | Status |
|---|---|---|---|
| 1 | Exact trigger logic for the California and Statewide Google Ads **and** Bing conversion tags | Read 4 Aug from the GTM trigger fields | **Closed for California** — its Bing event tag fires on `Click – All Elements`, condition `Click Text contains Submit Application`. **Statewide has no Bing event tag at all** — a narrower new question, below |
| 2 | One valid quote = one lead event; staff = zero; failed validation = zero | Test A above | Not yet run |
| 3 | Proof the test cannot send a live conversion to either platform | Test A runs with no container loaded; plus the staging-hostname exception | Design settled |
| 4 | Campaign-to-goal map for every flood campaign | Delivered 4 Aug — 46 flood campaigns, 44 on Account-default, 2 Demand Gen campaign-specific | **Closed** |
| 5 | Current Search Console verification method for both launch sites | Read 4 Aug | **Closed for statewide: `HTML file` → Successfully verified.** The risk is confirmed, not hypothetical. CFI still unread |

All five are now answered, or resolved into a narrower question. Two of the answers change the work —
see *Bing, resolved* below and the confirmed verification method in Session 3.


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

**Done 4 Aug.** Both platform exports are committed to `baseline-2026-08-04/` in raw and readable
form, with the analysis in that folder's README. Headline: **$37,378 spend, 953.6 reported conversions,
$39.20 blended CPA** across Google ($24,771 / 612.6) and Microsoft ($12,607 / 341.0).

Three things the baseline surfaced that were not visible before, all recorded as observations rather
than actions:

- **38% of Microsoft's conversions come from the Audience network** (130 of 341, $27.56 CPA, 860k
  impressions). That is the network where the June work found and excluded 21 fraud placements, after
  which conversions fell 21%. The June recommendation to reduce or exclude Audience on search
  campaigns does not appear to have been applied.
- **Same-state CPAs disagree between platforms in both directions** — Massachusetts is $399 on Google
  and $69 on Microsoft; California is $56 on Google and $96 on Microsoft. So it is not a simple
  one-platform bias, and no cross-platform budget decision can be supported until both count the same
  validated submission.
- **Google's Massachusetts Max Conversions campaign spent $399 for one conversion** and is not
  budget-limited — a 2.63% conversion rate against a 20–35% norm. Worth opening on its own merits,
  separately from anything else on this list.

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

### Bing, resolved — and the two brands need different things

**Read 4 Aug from the trigger fields.** Both reviews were right about different layers, which is why
we disagreed: the Microsoft *goals* are Event-type and recording (ChatGPT's point, correct), but the
*GTM tag firing the event* sits on a click trigger (my concern, also correct).

| Container | Tag | UET ID | Trigger | Condition | Pushes |
|---|---|---|---|---|---|
| CFI | `Bing UET Tag` | 5318858 | Page View / All Pages | — | `pageLoad` only |
| CFI | `Bing UET - request_quote (California)` | 5318858 | **Click – All Elements** | **`Click Text contains Submit Application`** | UET event action **`request_quote`** |
| Statewide | `Bing UET Tag` | 5318855 | Page View / All Pages | — | `pageLoad` only |
| Statewide | *(none)* | — | — | — | **no Bing event tag exists** |

**California — a one-line repoint, and do NOT rename the action.** Run this only when instructed; the
click trigger keeps working until the new sites are live.

```
In GTM container GTM-MZ6RZ94, open the tag "Bing UET - request_quote (California)".
Change ONLY its trigger: remove "Submit_Online_Quote_Form_Submission" (the
Click - All Elements trigger) and set it to the Custom Event trigger
"cfi_form_submit — is_lead true".

Do NOT touch the tag's code. It must keep pushing the UET event action exactly as
`request_quote` — that string is what the existing Microsoft goal matches on, so
keeping it means the goal and all its history carry on working untouched.

Leave the base "Bing UET Tag" (Page View / All Pages) exactly as it is.
```

> **This corrects a snippet I gave earlier.** I proposed a new Custom HTML tag pushing
> `quote_form_lead`. That would have been wrong twice: a second tag would double-count California, and
> a new action string would not match the existing goal. Keep `request_quote`.

**Statewide — nothing to repoint, which is a different problem.** An Event-type goal with no event tag
anywhere cannot be firing from GTM, so find out what it is actually matching on before building a
replacement:

```
Read-only. In Microsoft Ads (account X2012441), open the Statewide flood conversion
goal and report:
  - its exact TYPE as the interface states it
  - if Event type: the exact Category / Action / Label it matches on
  - if Destination URL type: the exact URL rule
  - whether Microsoft reports it recording conversions, and how many in the last 30 days
  - which UET tag it is attached to

Then separately: is there any Bing/UET code on statewidefloodinsurance.com that is NOT
in the GTM container — a snippet in the Divi theme header or integration settings? Check
the live /get-a-quote/ page source for uetq or bat.bing.com code GTM does not account for.

Change nothing.
```

**Proven, not inferred — and one report of hardcoded UET code is wrong.** A third review reported that
statewide's live quote page hard-codes the UET base snippet outside GTM. It does not, and the test that
settles it is blocking GTM:

| | Bing network requests | `window.uetq` | `bat.bing.com` script tags |
|---|---:|---|---:|
| Normal load | 10 | object | 2 |
| **GTM blocked** | **0** | **undefined** | **0** |

Every trace of UET disappears when `googletagmanager.com` is blocked, so **all of it comes from GTM's
base UET tag.** Nothing Bing-related is hardcoded anywhere.

Why it looked hardcoded, because this is an easy trap: inspect the live page in devtools and you see
`<script src="https://bat.bing.com/bat.js">` sitting in `<head>` with no GTM comment beside it, which
reads as hand-placed. But that is the **rendered DOM**, and GTM injected it. The tells are that it is
absent from view-source — `uetq`, `bat.bing`, `5318855` and even the word "bing" return zero hits in
the served HTML, including inside base64 blobs and escaped forms — and that it vanishes when GTM is
blocked. **DOM ≠ source.** I nearly made the mirror-image error earlier by trusting a plain-text
search alone; both checks are needed.

(Incidentally, the UET tag is also pulling `clarity.ms/tag/uet/5318855` — Microsoft Clarity riding
along on UET. Harmless, just worth knowing it is there.)

**So the launch question is settled: nothing Bing-related dies at cutover.** Original finding below
stands.

**The middle case is ruled out — traced 4 Aug from the live page source.** There is **no hardcoded
UET code on statewide**: `uetq`, `bat.bing.com`, `5318855`, `5318858` and `request_quote` all return
zero hits in the raw HTML of the live `/get-a-quote/` page. So nothing Bing-related lives in the Divi
theme, and **nothing about Bing tracking dies at cutover.** That was the launch-relevant worry and it
is closed.

Also ruled out, and it was a plausible theory: California's container is **not** running on statewide.
Both container IDs appear on the page, but only `GTM-PJQ72VK` has a live script loader (placed by the
GTM4WP plugin); `GTM-MZ6RZ94` appears **only as a `<noscript>` iframe** with no loader, so it never
executes for a normal visitor. California's click-triggered event tag therefore cannot be firing on
statewide's form.

What remains is a data-quality question rather than a launch risk — and with hardcoded code ruled out,
there is now a leading hypothesis worth testing first:

**The goal is probably a Destination URL goal, not an Event goal.** That would explain everything with
no event tag anywhere: the base UET tag fires on every page, and a URL rule turns a *page view* into a
recorded conversion. If the rule matches something like `/get-a-quote/`, then statewide's Bing
"conversions" are **visits to the quote page, not submissions** — which would make its conversion count
and its $95.66 CPA measure something entirely different from California's, and would explain part of
why the same-state CPAs disagree so wildly between platforms. The goal being *named* "STATEWIDE Submit
Form Click" does not make it an event goal; we already learned once in this project not to infer type
from name.

Two other candidates if that is not it:

1. **A differently-named GTM tag pushes the event.** The search was done by tag *name* — anything
   matching "Bing" or "UET". A Custom HTML tag called something else entirely could contain a `uetq`
   push. Statewide's container has 18 tags.
2. **Microsoft is tracking it server-side or by auto-detection**, in which case nothing in GTM is
   involved and it will keep counting whatever it currently counts.

Or the goal simply is not recording, and the earlier report of it recording was wrong.

The narrow read that separates these:

```
Read-only, in GTM container GTM-PJQ72VK (statewidefloodinsurance.com).

Do NOT search by tag name this time — search by CONTENT. Open every Custom HTML tag
in the container and tell me which ones contain the string "uetq" or "bat.bing.com",
whatever the tag is called. There are about 18 tags; I need the ones whose CODE
touches Bing, not the ones whose NAME does.

For any you find: the tag name, the exact uetq line, and its trigger.

Then in Microsoft Ads, for the Statewide flood goal, tell me its exact goal TYPE as
the interface states it, and its conversion count for the last 30 days. If it is an
Event goal, the exact Action string it matches.

Change nothing.
```

Whatever the answer, it is no longer blocking: statewide's Bing tracking is not going to break at
cutover, because there is nothing in the theme to break.

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

**Confirmed 4 Aug, and it is the bad case.** `https://statewidefloodinsurance.com/` → Settings →
Ownership verification reads **`HTML file` → Successfully verified.** That file sits in the current web
root, so a docroot swap deletes it and un-verifies the property exactly when the sitemap needs
submitting. Still not a blocker for the flip itself — but no longer hypothetical.

**Two fixes; do both, they barely cost anything:**

1. **Copy the file** (the belt). No DNS access required, and it preserves the existing verification
   exactly as it stands. How to find it, since the filename is a hash:
   - Search Console → the statewide https property → Settings → Ownership verification → the **HTML
     file** method shows the exact filename and offers it for re-download.
   - Confirm it is live now: `curl -I https://statewidefloodinsurance.com/google<hash>.html` should
     return 200.
   - Copy it into the new install's web root, and **re-run that same curl immediately after the
     docroot swap.** If it 404s, verification is gone — that is the check, not "I copied the file".
2. **Add a DNS-verified Domain property** (the braces). Permanent, filesystem-independent, and covers
   www, non-www, http and https at once — the fix that means this never comes up again.

**CFI, read 4 Aug: no file dependency at all.** Both URL-prefix properties — `https://` and
`http://www.` — are verified by **"Domain name provider"**, and HTML file is verified on neither. So
CFI's Search Console verification is entirely unaffected by the docroot swap, and nothing needs doing
for it.

That result also predicts statewide's outcome: CFI's *URL-prefix* properties read "Domain name
provider", which proves DNS ownership propagates down to URL-prefix properties on this account. So once
statewide's Domain property verifies by DNS, its URL-prefix property should show the same method — at
which point its HTML file becomes redundant and the copy step can be dropped from the cutover.

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

## Deferred — Session 7, Google Ads goal cleanup

**Deferred with no date, on Aaron's judgement, 4 Aug — and the judgement is right.**

The account moved to a Maximize-Conversions-heavy structure recently and both conversions and real
business are up. That is ground truth from the person who sees the leads and the bound policies, and
it outranks anything visible in the Ads interface. The theoretically-correct cleanup is not worth
risking a structure that is demonstrably working.

Three specific reasons the caution is technically justified, not just prudent:

1. **Narrowing goals reduces signal volume per campaign.** Smart Bidding learns from conversion
   count. Today's campaigns feed on a broad, messy, *high-volume* goal set. Restricting each campaign
   to only its own brand's lead actions cuts that volume — and for the thinner states it could drop a
   campaign below the data threshold Maximize Conversions needs to work at all. Right in principle,
   possibly worse in practice for low-volume campaigns.
2. **Measurement changes will make the reported number fall on their own.** Once staff intake and
   failed validations stop counting, conversions drop without a single lead being lost. Stacking a
   goal change on top of that makes the two effects impossible to separate.
3. **The staff-form problem does not need this session** — but it does not fix itself either, and
   my earlier wording said so. Correcting that, because it matters: it takes **four** things, and
   only the first is done.
   - v1.4.0 installed on both sites, so the clean event is emitted ✅
   - **Session 2** — the new triggers and tags built in GTM ❌
   - **Step 7 of the flip** — the old Click Text triggers removed ❌
   - **The post-flip check** — a staff-form submission recording no conversion ❌

   Skip Session 2 and nothing improves at cutover: the new staff form still has a "Submit
   Application" button in the page, so the old click trigger still fires on it. What is true is
   narrower and still useful — **all four steps can be done without touching a bid, a budget, or a
   campaign goal.**

**Revisit when** there is a deliberate performance review with real data behind it — not on a
calendar. The trigger is not "a month has passed"; it is being able to answer *this*: for each flood
campaign, how many CRM-qualified leads and bound policies did it produce, and would a narrower goal
set still leave that campaign enough conversion volume for Maximize Conversions to function? Until
that question is answerable, deferring is the correct answer rather than the cautious one.

Or never. The cost of leaving this alone is imperfect attribution. The cost of getting it wrong is
lead volume.

### The measurement that would make this decidable — and it is nearly built

Tracking bound policies by campaign is the missing piece, and most of it already exists. The June
attribution work put `GCLID`, `MSCLKID`, and the UTM set into hidden fields on Cognito form 5, and
those values reach the rater webhook on every entry.

**One checkbox is in the way.** Form 5 has `IncludeHiddenFields: false` on its two integration
emails, so the click IDs never arrive at Zapier or InsuredMine — captured on the entry, invisible to
the CRM. Turn that on for the emails to `floodcognito@robot.zapier.com` and `data@insuredmine.com`,
map the fields in the Zap, and every lead lands in InsuredMine carrying the campaign and keyword that
produced it.

That unlocks two things: bound-policy counts by campaign and state, which is the number that decides
this whole question — and later, **offline conversion import**, where a stored GCLID lets you feed
*bound policies* back to Google Ads instead of form submissions. That is the version of this cleanup
that would actually be worth doing, because it optimises toward customers rather than toward leads.

It is already on the loose-ends list below. It is worth more than its position there suggests.

### The volume constraint on all of this (Aaron, 4 Aug: ~250 policies bound last month)

Roughly **250 policies bound in the last month** — but that is a **blended** figure covering PPC
leads, referrals, and policies written by other agents through the MGA. Recorded here because it is
the only real business number in this entire document, and because two things follow from it.

**1. It cannot validate PPC by itself, and the MGA share is the reason.** Policies written by other
agents through the MGA are not marketing-attributable at all. A strong MGA month would mask a weak
PPC month and vice versa, so the blended total is exactly the wrong number to judge an ads change by.
What is needed is not precision — just a rough monthly split into three buckets: **web/PPC,
referral, MGA/other agents.** Even an approximate split, tracked monthly, is enough to detect whether
a measurement change cost real business. That is a report out of InsuredMine, not a tracking project,
and it is worth having *before* anything in Session 7 is contemplated.

**2. It reveals why "just optimise to bound policies" does not work, and shapes the design.** Offline
conversion import is the right long-term idea, but Smart Bidding needs roughly 30 conversions per
campaign per 30 days to bid reliably. If the PPC-attributable slice of 250 is, say, 60–90 policies
spread across 46 flood campaigns, that is one or two per campaign — nowhere near enough to bid on
directly, however clean the signal.

So the correct architecture is two-tier, and it resolves the tension in this whole document:

- **Bid on validated lead submissions.** High enough volume for the algorithm to learn from, and now
  clean — no staff intake, no failed validations. This is what Session 2 delivers.
- **Review on bound policies.** Too thin to bid on, but the right number for judging campaigns and
  states periodically, by hand, with the GCLID plumbing supplying the attribution.

That is why Session 7's question is "would a narrower goal set leave enough conversion volume" rather
than "which goal is most accurate". Accuracy that starves the algorithm is not an improvement.

**If it is ever run:** not in the cutover week, on a stable budget, one brand at a time, with the
Session 0 baseline as the comparison, and a written condition for putting it back.

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

### The duplicate-state question — corrected, and now closed as a factual matter

**My "thirteen states are currently bidding against themselves" was wrong, and the error is
instructive.** The campaign map listed each campaign's goal setting and bid approach but **not its
enabled/paused status**. I read 26 rows and treated the absence of a status column as evidence of
activity. A structural review then checked: eleven of those Manual CPC campaigns are **already
paused**.

The accurate statement: **13 historical pairs exist; two are live — California and Michigan.**

What survives, with 90-day numbers (May 7 – Aug 4):

| State | Manual CPA | Automated CPA | Status |
|---|---:|---:|---|
| California | $66.43 | $53.17 | **Both live, overlap confirmed** |
| Michigan | $77.16 | $50.48 | **Both live, overlap confirmed** |
| Virginia | $163.21 | $62.22 | Manual already paused |
| Massachusetts | $149.00 | $80.03 | Manual already paused |
| Illinois | $121.28 | $50.07 | Manual already paused |
| Florida | $119.69 | $26.63 | Manual already paused |
| Louisiana | $116.89 | $35.95 | Manual already paused |
| Missouri | $115.55 | $44.11 | Manual already paused |
| Tennessee | $103.29 | $64.26 | Manual already paused |
| South Carolina | $94.99 | $50.59 | Manual already paused |
| North Carolina | $79.31 | $33.84 | Manual already paused |
| Ohio | $77.57 | $52.45 | Manual already paused |
| Georgia | no conversions | $54.98 | Manual already paused |

The automated side wins in every pair that recorded a Manual conversion — so the directional claim
holds, and someone has already acted on it in eleven states. The overlap on the two live pairs is
now proven rather than inferred: identical location targeting, shared core keywords, and the same
search terms appearing in both 90-day reports.

**But the two live pairs are the two closest cases on the table.** California is $66 against $53 and
Michigan $77 against $50 — nothing like Florida's $120 against $27. These are exactly the pairs where
a pause is least obviously correct, which is probably why they are the two still running.

**And a consolidation caution the CPA numbers hide:** the Manual campaigns carry far more keywords —
359 versus 77 in California, 161 versus 43 in Michigan. Pausing the Manual half may drop query
coverage the automated campaign has no keywords for, so the CPA comparison is not the whole decision.
Before any pause, compare the two search-term reports and confirm which queries only the Manual
campaign is reaching, and whether they convert.

Sequence unchanged: measurement first, then goals, then structure — one state at a time against the
Session 0 baseline.

### The Demand Gen goal set is not a template — and that is a finding

I suggested copying `Statewide Flood - Quote & Contact Leads` rather than inventing a goal set.
Withdrawn: it holds two Website actions and **one of them is dead.**
`statewidefloodinsurance.com - Submit_Online_Quote_Form` is active and recording;
`statewidefloodinsurance.com - Contact_Form_Submission` is reported by Google Ads as **tag inactive**.

That is worth more than the template idea was — though it is a configuration issue, not proof the
campaign is impaired, and my first wording ("effectively running on one goal") implied more than the
evidence supports. The accurate statement: **one of the two actions contributes nothing, so the
campaign optimises on the quote action alone.** Whether that is a problem depends on whether
contact-form submissions were ever meant to count as conversions for it. The active quote action may
well be doing the whole job perfectly adequately.

It also connects to an earlier count nobody had attached to anything specific: the account shows 5
tag-inactive and 4 unverified conversion actions, and this is one of them, sitting inside a live
campaign's goals. Worth asking which campaigns the other four appear in — same question, same read.

The fix is already on this list: that contact-form action is exactly what Session 2's
`cfi_form_submit` path is built to feed. Reconcile it there rather than copying it anywhere.

---


---

## After all six

Two things that are not account cleanup but are on the same list:

- **Move `google-ads-project/Google Ads/.env` out of Dropbox and rotate the Google Ads refresh
  token.** A refresh token is durable access to the whole Ads account, sitting in a synced folder.
### Lead-source attribution into the CRM — five steps, not one checkbox

I earlier called this a two-minute checkbox. That was wrong: it modifies a **live lead-delivery path**,
so it needs an order and a test.

The situation: Cognito form 5 already captures `GCLID`, `MSCLKID` and the UTM set into hidden fields
(the June work did that, and the GTM prefill tag populates them). The entry has them and the rater
webhook receives them. But the form's integration emails have **`IncludeHiddenFields: false`**, so the
values never appear in the emails that Zapier and InsuredMine read. Captured, invisible to sales.

Form 5 delivers four ways: a webhook to `cfi.insuranceclouds.com/Raters/Flood/JSONSubmit.aspx`, and
emails to `quote@californiafloodinsurance.com`, `floodcognito@robot.zapier.com` (a Zapier Email Parser)
and `data@insuredmine.com` (InsuredMine's email-to-lead ingestion).

**Step 1 — Turn hidden fields on for the human inbox only.** Enable "Include hidden fields" on the
`quote@` email first, submit a test entry, and look at what arrives. Nothing automated reads that
address, so this is genuinely risk-free, and it shows you the new format before anything depends on it.

**Step 2 — Do NOT simply enable it on the Zapier email.** `floodcognito@robot.zapier.com` is a Zapier
**Email Parser**, and parser templates are anchored to the email's structure. Adding new lines can
cause it to mis-parse or stop matching — which would break lead delivery to the CRM, the opposite of
the goal.

**Step 3 — Replace the email path with a webhook instead.** This is the actual recommendation. Cognito
supports webhooks natively and already posts one to the rater, so add a second: a Zapier **Catch Hook**
trigger, with Cognito posting the full entry JSON to it. That delivers every field including the hidden
ones, needs no parsing, and cannot break when the form changes. It replaces a fragile text-matching
step with a structured one, permanently. Keep the Email Parser Zap running until the webhook Zap is
proven, then turn the old one off.

**Step 4 — Create the destination fields in InsuredMine** (Settings → Custom Fields), or the Zap has
nowhere to write: map `UTM Source` → the built-in **Lead Source** field, and add custom fields for UTM
Medium, Campaign, Keyword, Ad/Creative, Google Click ID, Bing Click ID, and Source Website.

**Step 5 — Test end to end and confirm in InsuredMine.** Submit a test with a known query string, e.g.
`/get-a-quote/?utm_source=test&utm_campaign=verify&gclid=TESTABC123`, and confirm those exact values
land on the InsuredMine record. Then delete the test lead.

Why it is worth the five steps: this is what makes **bound policies attributable by campaign**, which is
the number that turns the deferred Session 7 decision from a judgment call into a measurement. It is
also the prerequisite for offline conversion import later — feeding *bound policies* back to the ad
platforms rather than form fills.

---

## Decided: no new access provisioned (4 Aug)

Asked and answered, recorded so it does not get re-litigated.

**No account access is provisioned for Claude, because no task on this list is blocked on it.**
Sessions 0–3 need no account data — Session 0's baseline is a Chrome Claude export, and everything
else is site-side or permissions. Provisioning credentials speculatively adds exposure and buys
nothing this month.

**Honest accounting of what access would have bought:** two of my three errors in this project came
from reading relayed tables rather than source data. The "thirteen live pairs" claim came from a table
with no status column; an API query returns status. The "Bing goals are click goals" claim came from
goal names; an API query returns type. So direct reads have real value — this is not modesty.

**When account data is next needed** (the Session 7 review, months out), the answer is already built:
the June scripts in `Claude CoWork Files/google-ads-project/Google Ads/` —
`pull_conversion_goals.py`, `diagnose_conversions.py`, `google_growth_audit.py`,
`google_tracking_health.py` — query the Ads API directly and produce structured output. Aaron or
Chrome Claude runs them, pastes the output. Zero new credentials, better data than screenshots.

**If standing read access is ever wanted:** a Google Ads user at the **Read only** access level, with
a refresh token generated for *that* user rather than Aaron's own, held in a secret store and never
pasted into chat. Write access: no, at any point. Every change on this list is executed by a human
after a read-back, and that is the check that caught all three of my errors.

**Unrelated and still outstanding:** the existing Ads refresh token sits in a synced Dropbox folder
(`google-ads-project/Google Ads/.env`). That is the real access problem in front of us, and it is not
mine. Move it out and rotate it.
