# GA4 — delete the 14 empty accounts (paste-ready)

Safe to run during the cutover. These accounts hold **no properties**, so no measurement ID, no
tag, and no live site depends on any of them. Nothing here can affect the flood sites.

Deletion is reversible: GA4 moves a deleted account to the **trash can for 35 days**, and it can
be restored from Admin → Trash can within that window. After 35 days it is permanent.

---

## The paste

```
You are helping me clean up a Google Analytics 4 account structure. I am logged in
to analytics.google.com as the owner.

GOAL: delete 14 GA4 ACCOUNTS that contain zero properties. These are empty
containers left over from old projects.

THE 14 ACCOUNTS TO DELETE (match the name exactly):
  1.  4S Ranch
  2.  ApartmentInsuranceOnline
  3.  ATPinsuranceprograms
  4.  Carlsbad
  5.  contractorsinsurancepros
  6.  Del Mar
  7.  Encinitas
  8.  Escondido
  9.  floridafloodinsurance.net
  10. Mira Mesa
  11. New Mexico Flood
  12. Oregon Flood
  13. Rancho Bernardo
  14. Scripps Ranch

CRITICAL SAFETY RULE — do this for EVERY account before deleting it:
Open the account and confirm it has ZERO properties. If an account shows even one
property, STOP. Do not delete it. Add it to a "skipped" list, tell me the account
name and the property name, and move on to the next one. An account deletion also
deletes every property inside it, and those properties may hold data history that
cannot be recovered or rebuilt.

DO NOT TOUCH these accounts under any circumstances. They hold live properties:
  - californiafloodinsurance.com
  - statewidefloodinsurance.com
  - jumpins.com
  - arizonafloodinsurance.net
  - cheapearthquakeinsurance.com
  - cheapsoberlivinginsurance
  - farmerinsurance
  - vacanthomeinsurance.com
  - Mrtacoshop.com
  - restaurant-insurance
  - texas / washington / sacramento / san diego
  - anything not on the numbered list of 14 above

Also: do not delete, rename, or modify any PROPERTY, any DATA STREAM, any
measurement ID, or any Google Ads link. Accounts only, and only the 14 named.

HOW TO DELETE ONE ACCOUNT:
  1. Admin (gear icon, bottom left)
  2. Account column → use the account picker to select the account by name
  3. Confirm the Property column shows no properties  ← the safety gate
  4. Account settings
  5. Move to trash can
  6. Confirm

WORK ONE AT A TIME and after each one report: the account name, whether it had
zero properties, and whether the deletion succeeded.

WHEN FINISHED, give me a summary table with three sections:
  - Deleted (should be up to 14)
  - Skipped because it was not empty (with the property names you found)
  - Not found / name did not match

Do not delete anything that is not on the list of 14, even if it looks unused or
empty. If you are unsure about an account, skip it and ask me.
```

---

## After it reports back

**Check the "skipped" section first.** Any account that turned out to hold a property is a
finding — the inventory said all 14 were empty, so a skip means the inventory was wrong and the
rest of it deserves a second look before the next cleanup stage.

**Check "not found" too.** A name mismatch is more likely than a missing account; GA4 account
names in the inventory were transcribed from the admin list.

**Verify the count.** 29 accounts before, so expect 15 after if all 14 went.

---

## What this does NOT cover — deliberately

Three other GA4 cleanup items exist and none of them should be handed to an agent:

**The four dead duplicate properties** (`cheapearthquakeinsurance.com-GA4` / `G-NT5FM4Q85H`,
`statewidefloodinsurance.com-GA4` / `G-NCF8CTTSQS`, `jumpins.com-GA4` / `G-H4XXCW8HT4`,
`TEMP - placeholder` / `G-LBMCGFX7GC`). These are *properties*, not accounts, and each sits inside
an account that also holds a live property. Rename them to `ZZ DELETE — never received data`, leave
them a week, then delete. Doing it by hand is the point: a mis-click here deletes a live property.

**The two property moves** (`Mrtacoshop.com` out of the arizonafloodinsurance.net account,
`vacanthomeinsurance.com` out of the californiafloodinsurance.com account). A property move
preserves the measurement ID and all history, but it is a structural change worth doing
deliberately.

**Unmarking `purchase` as a key event on CFI.** Small but do it before the Ads work, not after — if
it ever gets imported into Ads it becomes a phantom conversion.

Full context for all three in `ACCOUNTS.md`.
