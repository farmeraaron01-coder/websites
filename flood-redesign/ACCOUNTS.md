# Account cleanup — naming standard and order of operations

The confusion is structural, not accidental: **one Google Ads account and one GTM account serve
18 websites across a dozen unrelated businesses**, named as they were created rather than to a
convention. That unreadability is how the staff-form conversion problem survived for months.

**The 4 Aug inventory changed the priority.** Naming is not the biggest issue in these accounts —
access is. Jump to *Findings from the inventory* at the bottom; step zero there comes before
anything else in this document.

Two rules for everything below:

1. **Renaming is free. Deleting is not.** Container IDs, measurement IDs, and conversion action IDs
   are permanent. Friendly names are cosmetic and change nothing about tracking. So all renaming can
   happen today with zero risk; anything that removes or re-points a tag waits for its section.
2. **Never delete anything holding history.** Conversion actions go Secondary or Hidden, never
   deleted. GA4 properties that have *received data* get renamed to say "do not use" and archived.
   The exception, which the inventory found several of: a property or container that has **never**
   received a hit holds no history, so deleting it loses nothing — rename it `ZZ DELETE` and leave it
   a week first, so a mistake stays recoverable.

---

## The standard

| Layer | Convention | Example |
|---|---|---|
| GTM account | Agency-level, not a brand | `Farmer Agency — All Web Properties` |
| GTM container | The exact domain it serves, lowercase, nothing else | `californiafloodinsurance.com` |
| GTM tag | `<platform> — <what it measures>` | `GA4 — page_view`, `Ads — quote form lead` |
| GTM trigger | `<event> — <condition>` | `cfi_form_submit — is_lead true` |
| GA4 property | `<domain> (<measurement ID>)` | `californiafloodinsurance.com (G-3YMN51H7LE)` |
| GA4 data stream | The `https://` canonical URL, non-www | `https://californiafloodinsurance.com` |
| Ads account | Agency-level, not one brand | `Farmer Agency — Search & PMax` |
| Ads conversion action | `<domain> — <action>` | `californiafloodinsurance.com — quote form lead` |
| Ads campaign | `<brand> — <geo/product> — <bid strategy>` | `Flood CA — search — MaxConv` |
| Search Console | Domain property, DNS-verified | `californiafloodinsurance.com` |

**One property per business, not per domain.** The distinction matters. Two domains that are the same
business belong in one property with cross-domain measurement configured — `lp.jumptruckinginsurance.com`
and `jumptruckinginsurance.com` are one business, and splitting them would break the visitor journey
from landing page to site, showing a self-referral instead of one session. Two domains that are
separate brands with separate budgets and separate reporting belong in separate properties. Flood and
statewide flood are already separate, which is correct: you want to compare them.

If two properties serve the same domain, that is a finding to report, not something to merge on the
spot.

---

## Properties that hold more than one website

> **The inventory found none of this.** Every property has exactly one stream; the nesting was one
> level up, in accounts holding two properties — which is much cheaper to fix, because a property can
> be *moved* between accounts with its measurement ID and history intact. This section is kept for the
> case where a blended property does turn up later, and because the Ads-cost reasoning in it still
> governs any future split.

A GA4 property can carry several data streams, and by default the reports **blend** them. That is the
"hard to find" problem: one property named after one brand, quietly reporting on three, so every
number in it is a sum nobody asked for.

The target is one property per business. Getting there has one cheap part and one expensive part, and
the difference decides the order.

**What splitting cannot do.** A data stream cannot be moved between properties, and history cannot be
divided. A new property starts empty, with a new measurement ID, and there is no backfill. The old
blended property stays as the only record of everything before the split — so **never delete it**,
rename it to say what it is.

**The history loss is smaller than it feels.** On the free tier GA4 retains event-level data for at
most 14 months. Whatever is in the blended property ages out on that clock either way, so the argument
for postponing a split gets weaker every month, not stronger. This is not Universal Analytics, where
years of history sat in one place.

**The expensive part is Google Ads, not reporting.** If a property feeds Ads conversions as imported
key events — which is exactly how CFI's conversions work — then a new property means importing new
conversion actions, and those start with **no conversion history for Smart Bidding**. Bidding
re-learns. That is a real cost, it lands on spend, and it is the reason this is sequenced rather than
just done.

### The decision rule

| The property blends… | Feeds Ads conversions? | Do this |
|---|---|---|
| Separate brands | No | **Split now.** Cheap, no bidding impact. |
| Separate brands | Yes | **Split, but on its own week** — after the site cutover and after the stage 3 conversion work, never alongside either. Import the new key events, let bidding re-learn on a stable budget for 2–3 weeks. |
| Same business, several domains or subdomains | Either | **Do not split.** Configure cross-domain measurement and name the streams properly. Splitting breaks the journey between them. |

### Doing it without splitting, where splitting is not worth it

If a property blends brands but the reporting need is just "let me see one site at a time", these cost
nothing and lose no data:

- **Name every data stream after its exact domain.** Most of the confusion is streams named "Website"
  or after whichever brand was set up first.
- **Comparisons on Hostname.** Add a comparison for `hostname exactly matches <domain>` and every
  standard report filters to that site. Save it so it is one click next time.
- **A Looker Studio page per brand**, filtered on hostname, so each brand has a report that cannot
  accidentally show another's numbers.

These are worth doing *even where you do intend to split*, because they make the blended property
readable during the months the split is waiting its turn.

---

## Stage 1 — Renames only (zero risk, do any time)

Nothing in this stage touches a tag, trigger, or bid.

**GTM — mostly already done.** Account `6003744403` is named "Aaron Farmer Insurance Agency Websites
Account", which is fine, and sixteen of its eighteen containers are already named for their domain.
Only two renames remain; see *GTM — the short list* in the findings section.

**GA4 — this is where the work is.** Rename each property to `<domain> (<measurement ID>)`; fix nine
`http://` stream URLs; retire four dead duplicates; delete fourteen empty accounts. The itemised list
is in *GA4 — where the real work is* below.

**Google Ads.** The account is named `Aaron - www.CaliforniaFloodInsurance.com` while running flood,
statewide flood, trucking, earthquake, pet, landlord, apartment, pest, and sober living. Rename it to
something agency-level so nobody reads a CPA as "California's".

**Search Console.** Add a **DNS-verified Domain property** for each flood domain — this is already a
launch item, since statewide's HTML-file verification dies with the docroot swap. A Domain property
also collapses the `http`/`https`/`www` URL-prefix duplicates into one place to look.

---

## Stage 2 — Duplicates and orphans (low risk, report before removing)

Known items, all in `GTM-MZ6RZ94` unless noted:

- **Two Conversion Linker tags** — `Conversion Linker` and `Conversion Linker 1`. One is redundant.
  Compare their triggers, keep the one on Initialization/All Pages, delete the other.
- **The base Google tag for `AW-1012143191` is not on the Initialization → All Pages trigger.** Found
  in the June re-look, still true: conversions record anyway because the remarketing tag loads the AW
  gtag on every page, but it is the reason GTM shows a "missing Google tag" nag. Put a proper Google
  tag on Initialization — All Pages and the nag resolves.
- **Statewide production carries an orphaned `GTM-MZ6RZ94` `<noscript>` iframe** with no head loader,
  left from cloning CFI's Divi build. It only ever affected visitors with JavaScript off. The new
  theme does not emit it, so this fixes itself at cutover.
- **Two Bing UET tags on CFI** (`Bing UET Tag` and `Bing UET - request_quote (California)`). Confirm
  both use the correct UET tag ID — a rogue `5318855` was already removed once.
- **Containers with no tags, never published, or not installed anywhere.** Report as deletion
  candidates; decide per container.

---

## Stage 3 — Functional, and in this order

Order matters. Doing these out of sequence means optimising toward a feed you have not fixed yet.

**3a. Fix the signal (site side — done, pending install).** Theme v1.3.8 emits `cfi_form_submit` with
`cfi_is_lead` on a genuinely successful submission, and `cfi_page_role` for the CRM. See LAUNCH.md.

**3b. Repoint the tags that consume it.** On CFI, the **GA4 event tags** are the fix — its Ads
conversions are GA4-imported, so there is no Ads tag to repoint. On statewide, repoint the GA4 event
tags *and* the two native Ads conversion tags. Retire every Click Text trigger. Check statewide for
double-counting: it has native Ads conversions plus the same GA4 events CFI imports.

**3c. Then the July 15 conversion-tracking cleanup** (`conversion-tracking-cleanup-plan.md`). 60
conversion actions, dozens Primary across six brands, so flood campaigns bid partly toward trucking
and pet conversions. Its own plan covers it: pick canonical lead actions, set them ONE_PER_CLICK,
demote engagement actions to Secondary, and set **campaign-level conversion goals** per brand.

Why this order: 3c decides *which signals count*, 3a/3b fix *whether the signals are true*. Running
3c first would tune bidding against a feed that still counts staff intake and failed validations.

Expect reported conversions to **fall** through 3b and 3c, and CPA to look higher but truer. Smart
Bidding needs 2–3 weeks to recalibrate — do it on a stable budget, not alongside budget moves, and
not in the same week as the site cutover so the two effects stay separable.

---

## One structural decision

**Keep one Ads account, or split per brand?**

**Recommendation: keep one account and use campaign-level conversion goals.** Splitting means new
accounts with no conversion history, re-learning on every campaign, separate billing, and lost shared
audiences — real cost, to solve a readability problem that naming plus campaign-level goals already
solves. A single operator with one shared budget does not benefit from the separation. This still
holds at the inventory's real scale: `AW-1012143191` in 15 of 18 containers is a bigger mess than
expected, but campaign-level goals fix the bidding contamination without any re-learning, and a split
does not.

Worth revisiting only if you sell a brand, take on a partner who needs access to one brand and not
the others, or hand a brand to an outside agency. At that point the split is about permissions, which
naming cannot fix. If you want brand-level reporting without splitting, an MCC over the one account
plus consistent campaign naming gets you most of the way.

---

## Step 1 is an inventory, not an edit

The known mapping above is incomplete — the June brief noted "there are more" containers, and nobody
has listed them. Run the inventory first so the renames are applied once, against the real list.

Paste this into Claude in Chrome, signed in:

```
Read-only inventory. Change nothing — no renames, no deletes, no publishing.

1. GTM (tagmanager.google.com → Admin). List every account you can see with its
   exact current name and ID. Then for EVERY container in each account, give me a
   table: public ID (GTM-XXXXXXX) | current container name | which domain it
   serves (infer from its tags — GA4 measurement ID, UET tag ID, Ads conversion
   ID) | number of tags | last published version, date, and by whom | does it look
   active or orphaned (no tags / never published / no matching live site).

2. GA4 (analytics.google.com → Admin). List every account and property: property
   name, property ID, and for each data stream the stream name, measurement ID,
   and configured stream URL. Then answer these three specifically, because they
   decide what we do next:
   a. Which properties contain MORE THAN ONE data stream, and what domain is each
      stream? (A property holding several websites is the thing we are hunting.)
   b. For each of those properties, is a Google Ads account linked (Admin →
      Product links → Google Ads links), and are any of its key events imported
      into Ads as conversion actions?
   c. Which properties have received no data in the last 48 hours?
   Also flag any two properties serving the same domain, and any stream whose
   configured URL is http:// rather than https://.

3. Google Ads (Goals → Conversions → Summary). List every conversion action:
   name, source, category, status, primary or secondary, and the count setting
   (one vs every). Also tell me whether the account sits under a manager account
   (MCC) and what that manager account is named.

4. Search Console. List every property, whether it is a Domain or URL-prefix
   property, its exact URL form (http/https, www/non-www), and its verification
   method.

5. Microsoft Ads / Bing UET. List every UET tag ID and its name, and which
   conversion goals reference each one.

Report as plain-text tables. Flag anything that looks duplicated, orphaned, or
inconsistently named, but do not fix it.
```

With that back, the Stage 1 renames become a single mapping table I can write out for you, and
Stage 2's deletion candidates stop being guesses.

---

# Findings from the inventory — 4 Aug

18 GTM containers, 29 GA4 accounts holding 21 properties, one Google Ads account under a manager
account, and — confirmed 4 Aug — **one** Microsoft Ads account holding all 14 UET tags, across a dozen
unrelated businesses. All five platforms are now inventoried.

**Two corrections to what this document said before the inventory.**

*The multi-site nesting is one level up from where I looked.* No GA4 property holds several streams.
Instead **six accounts hold two properties each**, and twice the second property is an unrelated
business: `Mrtacoshop.com` sits inside the arizonafloodinsurance.net account, and
`vacanthomeinsurance.com` sits inside the californiafloodinsurance.com account. So the concern was
real, the level was wrong. The good news is that this is *far* cheaper to fix than a stream split:
moving a property between GA4 accounts is a supported operation that keeps the property, its
measurement ID, and all of its history. No re-tagging, no Ads relink, no bidding reset. The expensive
scenario I described does not apply to anything actually found.

*Most GTM container naming is already done.* Sixteen of eighteen containers are already named for
their domain. Only two deviate, both by carrying a `www.` prefix. The stage 1 GTM work is nearly
finished — someone executed the June brief.

---

## Step zero — access, before any renaming

This is the finding that outranks everything else in this document, and it is not a tidiness problem.

**Anyone with GTM publish rights can inject arbitrary JavaScript into every page of the site it
serves.** That is script execution on the page: it can read form fields as they are typed, move the
phone number, or redirect the quote button. It is the single most powerful access anyone can hold over
these sites, and the publish history shows it spread across at least six external identities over the
years:

| Identity | Last seen publishing | Notes |
|---|---|---|
| `aliofficialfiverr@gmail.com` | 05/11/2022, ten containers | A Fiverr freelancer address, from a 2022 engagement |
| `zainarshad866@gmail.com` | 12/13/2022, two containers | Personal Gmail |
| `yas17sheikh@gmail.com` | seen in history | Personal Gmail |
| `info@excellero.com` | 05/24/2026 pestcoverage; linked statewide's GA4↔Ads | Outside agency |
| `kylewaters@max-conversion.com` | 04/23/2026, jumptruckinginsurance | Outside agency, still active |
| `aztecinsurance@gmail.com` | current, most containers | Aaron's own working account |

**Do this first, and it costs nothing to get wrong:** in GTM → Admin → User Management (at the account
level, then check each container), remove every identity that is not currently doing work. The 2022
freelancer addresses are the priority — a contractor from four years ago should not retain the ability
to publish JavaScript to a live insurance site. For the two agencies still working, downgrade from
Publish to **Edit** so changes need approval, and scope them to the one container they work on rather
than the account. Do the same review in GA4 (Admin → Account access management) and Google Ads
(Admin → Access and security).

**Also check pending invitations, not just active users.** Microsoft Ads was found to hold a *pending*
Max Conversion invite (4 Aug). An unaccepted invitation is standing access waiting to be claimed —
whoever controls that mailbox can accept it at any point, including long after the engagement ends, and
it does not show up in a list of current users. Aaron is revoking it. Re-inviting later takes thirty
seconds, so a pending invite of uncertain age should always be revoked rather than left open.

Nothing here suggests anything bad has happened. It is unused standing access, which is the ordinary
way this goes wrong.

---

## GTM — the short list

**Renames (2):** `www.cheaplandlordinsurance.com` → `cheaplandlordinsurance.com`, and
`www.vacanthomeinsurance.com` → `vacanthomeinsurance.com` (or delete it, below).

**Delete candidates (2):** `GTM-53H3GF24` mytruckinginsurance.ai and `GTM-W8F3276K`
vacanthomeinsurance.com — both are empty containers, zero tags, one "Empty Container" version, absent
from Search Console. Safe to delete; nothing references them.

**Ten skeleton containers** (arizona, farmerinsurance, jumpins, restaurant-insurance, sacramento, san
diego, texas, washington, and others) carry the same four tags published once in 2021–2022 and never
touched. Decide per domain whether the site is still a live business. If yes, leave them; if no, the
container and its GA4 property can retire together. They are not doing harm — they are just noise
making the real containers harder to find.

**Two quality flags to open and read**, since neither was itemised: `GTM-PJQ72VK` (statewide) shows
**"Urgent — 2 issues"**, and `GTM-PBH839BH` (jumptrucking, agency-run) also shows Urgent. Statewide's
is the one that matters for launch — find out what those two issues are before the cutover. CFI's
"Needs Attention" is already explained: the AW base tag missing its Initialization trigger.

---

## GA4 — where the real work is

**Delete the 14 empty accounts.** 4S Ranch, ApartmentInsuranceOnline, ATPinsuranceprograms, Carlsbad,
contractorsinsurancepros, Del Mar, Encinitas, Escondido, floridafloodinsurance.net, Mira Mesa, New
Mexico Flood, Oregon Flood, Rancho Bernardo, Scripps Ranch. No properties means no data means nothing
to lose. This alone removes half the clutter.

**Move the two misfiled properties** into their own accounts (or the right existing one):
`Mrtacoshop.com` out of the arizonafloodinsurance.net account, `vacanthomeinsurance.com` out of the
californiafloodinsurance.com account. A property move preserves the measurement ID and all history.

**Retire the four dead duplicates.** Each is a www/non-www twin of a live property that has never
received data: `cheapearthquakeinsurance.com-GA4 (389773239 / G-NT5FM4Q85H)`,
`statewidefloodinsurance.com-GA4 (371465506 / G-NCF8CTTSQS)`, `jumpins.com-GA4 (371490137 /
G-H4XXCW8HT4)`, and `TEMP - placeholder (545006633 / G-LBMCGFX7GC)`. A property that has never
received a hit holds no history, so these are safe to delete — but rename each to
`ZZ DELETE — never received data` first and leave it a week. Costs nothing, and makes a mistake
recoverable.

**Rename the survivors** to `<domain> (<measurement ID>)`. Current names are inconsistent enough that
two properties are indistinguishable in a switcher: `Cali Flood Insurance - GA4`, `cheap earth quake
insurance`, and one property with no name at all (`314801581`, cheapsoberlivinginsurance).

**Fix nine `http://` stream URLs**: arizona, Cali Flood, sober living, farmerinsurance, HOA, statewide
(the live one), restaurant-insurance, texas, washington.

**Unmark `purchase` as a key event on CFI.** Three key events are marked — `Contact_Form_Submission`,
`purchase`, `Submit_Online_Quote_Form_Submission` — and only the last has data. `purchase` is a
GA4 default with no meaning on an insurance site; if it is ever imported into Ads it becomes a
phantom conversion. Unmark it.

---

## Google Ads — the shared-account problem, quantified

`AW-1012143191` is wired into **15 of the 18 containers**. This is not sloppiness, it is the
architecture: one Ads account is the conversion home for flood, statewide flood, earthquake, sober
living, pest, trucking, landlord, apartment, and pet insurance. That is the root cause of the July
audit's finding, and it is why flood CPAs have been directional at best.

**The recommendation still holds: campaign-level conversion goals, not an account split.** It fixes
the bidding contamination for free and without re-learning. Three specifics the inventory adds:

- **The TopDog actions count "Every" while every other business counts "One."** Six of them, at least
  one Primary. On engagement events, "Every" inflates the conversions column that Smart Bidding
  reads — so flood bidding has been partly chasing repeated button clicks on a pet insurance site.
- **Engagement actions are Primary and should not be.** `Local actions - Website visits`, `Local
  actions - Menu views`, `Get directions`, `Clicks to call`, `YouTube channel subscriptions`, and
  `YouTube follow-on views` are all Primary, most counting "Every." These are the July plan's
  "demote to Secondary" list, now with names.
- **Earthquake and pest have no GA4↔Ads link** but their containers fire Ads conversion tags straight
  to `AW-1012143191`. That path bypasses the GA4 link entirely, so those conversions arrive in the
  shared column without ever appearing in a GA4 property. Worth knowing before anyone concludes a
  number is missing.

**One genuine split candidate: jumptruckinginsurance.com.** It is run by an outside agency that
currently has Publish rights in GTM and whose conversions land in the account holding every other
brand's data. That is a permissions problem, which is the one thing naming and campaign goals cannot
solve — the case I flagged earlier for when a split is actually worth its cost. Its own Ads account
and its own GTM container access would be cleaner for both sides.

Also note the account already sits under a manager account, **"Aaron Manager Account" (909-487-9776)**
— so brand-level separation is available whenever it is wanted without rebuilding anything.

---

## Search Console

**CFI has no Domain property** — only `https://` URL-prefix and `http://www.` URL-prefix. Statewide
has `https://` and `http://` URL-prefix, no Domain property. Both need one, and for statewide it is a
launch blocker: its verification is an HTML file in the docroot that a docroot swap deletes. (That
finding came from the earlier pass; this pass spot-checked two other properties and found DNS. Confirm
statewide's specifically before cutover.)

Once a Domain property exists per site, the URL-prefix duplicates can stay — harmless — but the
sitemap and all reporting should move to the Domain property.

---

## Microsoft Ads — the same fragility, and the same fix

Manager **"Aaron J. Farmer Insurance Agency, Inc."** (C222031356) → one sub-account (X2012441). All 14
UET tags live here. The earlier guess that they clustered into three accounts was wrong.

**The important finding: the flood goals are click goals, exactly like Google's were.**

| UET tag | Site | The flood goal |
|---|---|---|
| `5318858` | californiafloodinsurance.com | **"CALIFORNIA Submit Button Click"** |
| `5318855` | statewidefloodinsurance.com | **"STATEWIDE Submit Form Click"** |

So everything established about the Google side applies here without change: `/staff-form/` embeds the
same Cognito form 5 with the same "Submit Application" button, so **office phone intake has been
inflating Bing conversions too**, and a click that fails validation counts as a lead on Bing as well.
The v1.4.0 `cfi_form_submit` event fixes the site half for both platforms at once; only the Bing
repoint was missing from the plan.

**How to repoint Bing** (belongs in the same GTM sitting as the Google repoint):

1. In the site's container, add a **Custom HTML** tag on the `cfi_form_submit` trigger with
   `cfi_is_lead` equal to `true`:
   ```html
   <script>
     window.uetq = window.uetq || [];
     window.uetq.push('event', 'quote_form_lead', {
       event_category: 'form',
       event_label: {{cfi_form_role}}
     });
   </script>
   ```
2. In Microsoft Ads, create a conversion goal of type **Event** matching Action `quote_form_lead`, on
   the site's UET tag.
3. Switch the campaigns to the new goal, then **pause** the old click goal rather than deleting it, so
   the historical numbers stay readable.

**Other findings:**

- **A "Smart goal" is counting on CFI** (`Smart goal [X2012441]`). Microsoft infers these from machine
  learning rather than a real action. Counting it alongside a genuine form goal both double-counts and
  gives bidding a signal nobody defined. Set it to secondary or remove it from the campaigns' goals.
- **Statewide has a paused "Recommended goal"** of Destination-URL type — an auto-suggestion nobody
  acted on, sitting next to the real event goal. Harmless while paused; delete it to stop it looking
  like a live goal.
- **jumptrucking has five goals that look like double counting**: `Jump Trucking - Form Submission`
  *and* `LP.JumpTruckingInsurance.com - Form Submission`; `Jump Trucking - Phone Call` *and*
  `LP.JumpTruckingInsurance.com - Phone Call` *and* `… - Phone Call Top of Page`. Two or three goals
  firing on one action, on one tag. This is the agency-managed property, and it is the most heavily
  instrumented tag in the account while its GTM container has no GA4 tag at all — worth confirming the
  campaign is even still running before anyone spends time on it.
- **Eight of the fourteen tags have zero goals** (jumpins, farmerinsurance, arizona, washington, san
  diego, texas, sacramento, restaurant-insurance). They fire on-site and collect remarketing audiences
  but track no conversions — the same eight-to-ten skeleton sites that show up in every platform. Not
  harmful; retire them with their sites, or leave them collecting audiences.
- Tag `295027961` is named "Lp.JunpTruckingInsurance" — a typo for "Jump". Free to fix.

---

## Decided: leave `mrtacoshop.com` as the account's main domain for now (4 Aug)

The cPanel account's Main Domain is `mrtacoshop.com`, holding `/public_html`. Every other site —
including both flood sites — is an addon domain. That is why cPanel auto-created
`californiafloodinsurance.mrtacoshop.com`, `statewidefloodinsurance.mrtacoshop.com` and the rest:
**those aliases are standard cPanel behaviour for addon domains, not something anyone configured.**

Aaron asked whether to disassociate it while things are already being cleaned up. **Recommendation: no,
and not before launch.** Three reasons:

1. **It needs WHM-level access, which means a support ticket** — and InMotion runs about a week on
   small tickets. It is the one change on any of these lists that cannot be self-served.
2. **It is disruptive in the wrong window.** Changing an account's primary domain touches SSL issuance,
   email accounts, and the auto-generated alias for *every* addon domain on the account. Doing that in
   the same period as two site cutovers means two large variables moving at once, and any problem
   afterwards would be ambiguous between them.
3. **The cost of leaving it is cosmetic.** It is a naming artifact visible in cPanel. It does not affect
   how either site functions, how they rank (canonicals point at the real domains), or anything in the
   ad accounts. The only *real* symptom is `statewidefloodinsurance.mrtacoshop.com` serving a live
   copy — and that is fixable directly by repointing or removing that one alias, without touching the
   main domain at all.

**So: fix the symptom, not the architecture.** Handle the two alias issues at cutover (see LAUNCH.md
Phase 1 step 2), and revisit the main-domain question later, on a quiet week, if it still bothers
anyone.

If it is ever revisited, the options in increasing order of effort: reassign the primary domain to
`californiafloodinsurance.com` via support; or move `mrtacoshop.com` to its own hosting account, which
is cleaner long-term since it is an unrelated business and its GA4 property currently shows no traffic.
Neither is urgent and neither should share a week with a migration.