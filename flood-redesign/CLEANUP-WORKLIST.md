# Cleanup worklist — seven sessions, in order

Each session is one sitting, one paste into Claude in Chrome, and one thing to report back.
Do them in this order. `ACCOUNTS.md` holds the reasoning; this file is just the work.

**One sequencing rule that matters:** the old Divi sites do **not** emit the `cfi_form_submit`
event — only the new theme does. So the new conversion triggers get *built* now (they sit dormant,
harmless), and the *old* click triggers get switched off during the cutover, not before. Session 2
covers the build; the switch-off is step 8 of the flip in `LAUNCH.md`.

| # | Session | Risk | Time | When |
|---|---|---|---|---|
| 1 | Remove stale access | None | 15 min | Now |
| 2 | Build the new conversion tracking | None (dormant until cutover) | 45 min | Before cutover |
| 3 | Search Console domain properties | None | 15 min | Before cutover |
| 4 | Delete 14 empty GA4 accounts | None | 10 min | Any time |
| 5 | GA4 renames, moves, and dead duplicates | Low | 45 min | Any time |
| 6 | GTM tidy-up | Low | 30 min | Any time |
| 7 | Google Ads goal cleanup | Resets bidding | 45 min | **Not** in cutover week |

---

## Session 1 — Remove stale access

Why first: anyone with GTM publish rights can inject JavaScript into every page of the site,
including code that reads form fields as they are typed. Six external identities hold it, one a
freelancer address last used in 2022 across ten containers.

```
I need to clean up user access across Google Tag Manager, Google Analytics, Google Ads,
and Microsoft Ads. Work through them one at a time and tell me what you changed.

1. GTM (tagmanager.google.com → Admin → User Management). Check BOTH the account level
   and each individual container's user list.
   REMOVE these users entirely wherever they appear:
     - aliofficialfiverr@gmail.com
     - zainarshad866@gmail.com
     - yas17sheikh@gmail.com
   CHANGE these two from Publish to Edit, and if they have account-level access,
   remove that and give them container-level access only:
     - info@excellero.com  → container: pestcoverage.com
     - kylewaters@max-conversion.com → container: jumptruckinginsurance.com
   Leave aztecinsurance@gmail.com and my own account untouched.

2. GA4 (analytics.google.com → Admin → Account access management). List everyone with
   access at the account level, and remove the same three Gmail addresses above if
   present. Do not remove anyone else without telling me first.

3. Google Ads (Tools → Admin → Access and security). List every user and their access
   level. Remove the same three addresses if present. Tell me about any other
   non-obvious address before removing it.

4. Microsoft Ads (Settings → Account access). Same: list everyone, remove those three.

Report a table of what you removed or changed, per platform. If you find any address
you are unsure about, stop and ask me rather than removing it.
```

**Report back:** the table of removals, plus any address you were unsure about.

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

F. Add a Custom HTML tag on trigger B, for Microsoft Ads:
   - Name: Bing UET — quote form lead
   <script>
     window.uetq = window.uetq || [];
     window.uetq.push('event', 'quote_form_lead', {
       event_category: 'form',
       event_label: {{cfi_form_role}}
     });
   </script>

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

Then in Microsoft Ads, one more small job:

```
In Microsoft Ads (one account: Aaron J. Farmer Insurance Agency, X2012441), create two
new conversion goals. Do not delete or pause anything.

1. Name: California — quote form lead
   Type: Event
   Action equals: quote_form_lead
   UET tag: 5318858 (Californiafloodinsurance.com)
   Count: one per click
   Category: Submit lead form

2. Name: Statewide — quote form lead
   Type: Event
   Action equals: quote_form_lead
   UET tag: 5318855 (Statewidefloodinsurance)
   Count: one per click
   Category: Submit lead form

Leave the existing click goals ("CALIFORNIA Submit Button Click", "STATEWIDE Submit Form
Click") running for now — we switch over later.

Also tell me: there is a "Smart goal [X2012441]" attached to tag 5318858. Which campaigns
currently include it as a conversion goal?
```

**Report back:** which campaigns use the Smart goal.

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

4. Also in GTM-MZ6RZ94: the container shows a "missing Google tag" warning because the
   Google Ads tag for AW-1012143191 is not on the Initialization – All Pages trigger.
   Add a Google tag with tag ID AW-1012143191 on the "Initialization - All Pages"
   trigger. Do not remove the existing Google Ads Remarketing tag.

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

2. DEMOTE TO SECONDARY: these are engagement events, not leads, and should never be a
   bidding goal. Set each to Secondary:
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

Before you change any campaign goals, give me the list of flood campaigns you found and
what their goals are set to now, and wait for me to confirm.

Report step 1 and 2 as done/not-done lists, and stop for confirmation before step 3.
```

**Report back:** steps 1 and 2 complete, plus the campaign list for step 3 — then confirm before it
proceeds.

---

## After all seven

Two things that are not account cleanup but are on the same list:

- **Move `google-ads-project/Google Ads/.env` out of Dropbox and rotate the Google Ads refresh
  token.** A refresh token is durable access to the whole Ads account, sitting in a synced folder.
- **Turn on "Include hidden fields" on Cognito form 5's two integration emails** (to
  `floodcognito@robot.zapier.com` and `data@insuredmine.com`). The UTM and GCLID values you capture
  are on the entry but invisible to Zapier and InsuredMine, so sales cannot see where a lead came
  from.
