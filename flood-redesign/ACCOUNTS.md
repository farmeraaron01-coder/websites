# Account cleanup — naming standard and order of operations

The confusion is structural, not accidental: **one Google Ads account, one GTM account, and one
Cognito org serve at least six brands**, and they were named as they were created rather than to a
convention. Nothing here is broken. It is just unreadable, which is how the staff-form conversion
problem survived for months without anyone spotting it.

Two rules for everything below:

1. **Renaming is free. Deleting is not.** Container IDs, measurement IDs, and conversion action IDs
   are permanent. Friendly names are cosmetic and change nothing about tracking. So all renaming can
   happen today with zero risk; anything that removes or re-points a tag waits for its section.
2. **Never delete a conversion action or a GA4 property.** Set it Secondary, archive it, or rename it
   to say "do not use". Deleting destroys history you cannot get back.

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

**GTM.** Account `6003744403` still carries a legacy name from the earthquake site. Rename the
account, then rename every container to its domain. Known mapping:

| Container | Serves |
|---|---|
| `GTM-MZ6RZ94` | californiafloodinsurance.com |
| `GTM-PJQ72VK` | statewidefloodinsurance.com |
| `GTM-T49RSMT` | cheapearthquakeinsurance.com |
| `GTM-PRRWDV4` | cheapsoberlivinginsurance.com |
| `GTM-PBH839BH` | lp.jumptruckinginsurance.com |

There are more containers than these five — the inventory step below is what finds them.

**GA4.** Rename each property to `<domain> (<measurement ID>)`. Two specific fixes:

- Statewide has **two properties with the identical name** `statewidefloodinsurance.com - GA4`.
  Rename the live one (`314831122` / `G-FH3Q6GKNHH`) to the convention, and rename the dead one
  (`371465506` / `G-NCF8CTTSQS`, no data, no Ads link) to
  **`ZZ DO NOT USE — orphaned (G-NCF8CTTSQS)`**, then archive it. Do not delete it.
- Both live data streams have `http://` stream URLs. Set them to the `https://` non-www canonical.

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
solves. A single operator with one shared budget does not benefit from the separation.

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
