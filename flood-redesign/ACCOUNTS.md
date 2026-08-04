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

One container per domain. One GA4 property per domain. If two exist for the same domain, that is a
finding to report, not something to merge on the spot.

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
   name, property ID, and for each data stream the measurement ID and configured
   stream URL. Flag any two properties that serve the same domain, and any
   property with no data in the last 48 hours.

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
