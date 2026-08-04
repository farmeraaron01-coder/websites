# Work package 1 — reads, plus Search Console setup

**For whoever picks this up (ChatGPT or Claude in Chrome). Self-contained; no prior context needed.**

## Context, in brief

Two insurance websites are being rebuilt and are about to be cut over from an old WordPress/Divi build
to a new coded theme:

- `californiafloodinsurance.com` — staged at `new.californiafloodinsurance.com`
- `statewidefloodinsurance.com` — staged at `staging.statewidefloodinsurance.com`

The cutover changes which directory on the server answers each domain. **Anything that lives in the
current web root disappears at that moment** — which is why task 1 matters.

Accounts involved: Google Ads `890-760-9729` (under manager `909-487-9776`), Microsoft Ads `X2012441`
(under manager `C222031356`), GTM account `6003744403` (18 containers), and ~21 GA4 properties.

## Ground rules

1. **Tasks 1 and 2 are the only ones that change anything, and both are additive.** Everything else is
   read-only. Do not rename, delete, pause, publish, or alter permissions anywhere.
2. **Do not touch Google Ads or Microsoft Ads bids, budgets, campaign settings, or conversion goals.**
   The account is performing well and is deliberately frozen. Nothing in this package needs them.
3. **Do not add, edit, or publish any GTM tag, trigger, or variable.** A later package covers that; it
   depends on task 4's answer.
4. If any step needs a decision not written here, stop and report rather than choosing.

---

## Task 1 — Add a DNS-verified Domain property (Search Console)

Neither site has a Domain property today. `statewidefloodinsurance.com`'s https property is verified by
**HTML file**, which the cutover will delete.

1. Add a **Domain** property (not URL-prefix) for `statewidefloodinsurance.com`, and another for
   `californiafloodinsurance.com`.
2. Search Console will display a **TXT record** for each. **Report both TXT values verbatim** — the
   site owner adds them at the DNS registrar; you do not need registrar access.
3. Do **not** delete any existing URL-prefix property.

**Output:** the two TXT record values, exactly as shown.

## Task 2 — Preserve the existing HTML-file verification

Belt-and-braces alongside task 1, in case DNS verification is slow.

1. Open the `https://statewidefloodinsurance.com/` property → Settings → Ownership verification → the
   **HTML file** method. It shows the exact filename (a hash, like `google1a2b3c4d.html`).
2. Report that filename.
3. Confirm it is live: `https://statewidefloodinsurance.com/<filename>` should load. Report whether it
   does.

**Output:** the filename, and whether it currently loads.

## Task 3 — Read CFI's verification methods

For **both** `californiafloodinsurance.com` URL-prefix properties (the `https://` one and the
`http://www.` one), open Settings → Ownership verification and list every method shown as **verified**,
verbatim.

Answer explicitly: **is an HTML file listed as verified on either?** If yes, it needs the same
treatment as task 2.

**Output:** the verified methods per property, and a yes/no on HTML file.

## Task 4 — What fires the Statewide Bing conversion? (most important read)

Container `GTM-PJQ72VK` contains only a base page-load Bing UET tag (ID `5318855`) — **no UET event
tag**. But Microsoft Ads reports a Statewide flood conversion goal that is recording. So something
outside GTM is firing it, and if that something lives in the old theme it will vanish at cutover,
silently ending Bing conversion tracking for that site.

1. In Microsoft Ads (`X2012441`), open the Statewide flood conversion goal and report:
   - its exact **type** as the interface states it (Event / Destination URL / Duration / Pages viewed)
   - if Event type: the exact **Category / Action / Label** it matches on
   - if Destination URL type: the exact URL rule
   - whether it is recording, and how many conversions in the last 30 days
   - which UET tag it is attached to
2. Then check for UET code **outside** GTM. View the page source of the **live**
   `https://statewidefloodinsurance.com/get-a-quote/` and look for `uetq`, `bat.bing.com`, or a UET
   snippet that the GTM container does not account for. Report exactly what you find and where in the
   page it sits.
3. If you can reach WordPress admin on the live statewide site, also copy out anything in
   **Divi → Theme Options → Integration** (the head and body code boxes). That is where hand-placed
   tracking code lives on this build.

**Output:** the goal's type and matching rule, plus any UET code found outside GTM.

## Task 5 — Access inventory (read-only; removals come later, with approval)

GTM publish rights allow arbitrary JavaScript on every page of a live site, and the publish history
shows several external identities holding them. This task only **lists** who has access — no changes.

1. **GTM** (Admin → User Management): the account-level user list, then each container's list. For
   every user: email, account-level role, container-level permission (None / Read / Edit / Approve /
   Publish).
2. **GA4** (Admin → Account access management, plus Property access management for the
   californiafloodinsurance.com and statewidefloodinsurance.com properties): every user, their role,
   and who is marked as account creator.
3. **Google Ads** (Admin → Access and security), including manager account `909-487-9776`: every user,
   access level, status.
4. **Microsoft Ads** (Settings → Account access): every user and role.

For each platform also report **how many users hold the highest role** — needed to be sure no removal
would leave an account without an administrator.

**Output:** one table per platform.

---

## What happens next

Tasks 3–5 come back to the site owner for review before anything is removed or built. The GTM tagging
work is a separate package that depends on task 4's answer, and the Google/Microsoft Ads accounts stay
frozen throughout.
