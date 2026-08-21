# Step 1 — Set up the staging build correctly

**Approach (Aaron, 21 Aug 2026):** build the new site fresh on
`staging.cheapsoberlivinginsurance.com`, install **Rank Math from the start**,
and **never install All in One SEO** on it.

This is the better plan. There is no import, no plugin reconciliation on a live
site, no AIOSEO leftovers, and the production site is untouched until cutover.
It replaces the earlier "swap AIOSEO for Rank Math in place" work order.

But it moves the risk somewhere else, and the new risk is live right now.

---

## 🔴 Do this first: staging is currently open to Google

Verified 21 Aug 2026 by anonymous request:

| Check | Actual |
|---|---|
| `<meta name='robots'>` | `max-image-preview:large` — **no `noindex`** |
| `/robots.txt` | `Disallow: /wp-admin/` only — **no `Disallow: /`** |
| `/wp-login.php` | **200**, publicly reachable |
| homepage | 200, Kadence theme, real content |
| sitemap advertised | `wp-sitemap.xml` (WordPress core) |

A crawlable staging copy of a site you are about to launch is a duplicate-content
problem that outlives the migration: Google can index staging, then treat the
real launch as the duplicate.

### Use HTTP Basic Auth, not the WordPress setting

cPanel → **Directory Privacy** → `/home/mrtaco5/staging.cheapsoberlivinginsurance.com`
→ tick "Password protect this directory" → create a user.

Why not the alternatives:

- **Settings → Reading → "Discourage search engines"** is advisory only. It adds
  a `noindex` meta tag and a robots rule; it does not stop anything that ignores
  them, and it is a single checkbox that is trivially forgotten at launch.
- **`Disallow: /` in robots.txt** blocks *crawling*, not *indexing*. Google will
  still list a URL it has been told not to crawl if it finds a link to it, and
  it will show it with no snippet.

Basic Auth returns **401** to everything. Nothing gets indexed, because nothing
gets served.

**Verify:**

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://staging.cheapsoberlivinginsurance.com/
# expect 401
```

**Then check whether damage is already done** — search Google for
`site:staging.cheapsoberlivinginsurance.com`. If anything is listed, request
removal in Search Console (Removals → Temporary removals) once the 401 is up.

### Also add the nginx cache bypass for the staging host

Same rules as the production domain:

```
.*sitemap.*
/robots.txt
```

This is not optional housekeeping. Staging is currently serving
`x-proxy-cache: HIT`, and a plain fetch of `/robots.txt` returned a stale
**"Maintenance"** HTML page while WordPress was generating a perfectly valid
robots.txt. You will chase ghosts for an afternoon without this. Purge does not
work on this account.

---

## Step 2 — Rank Math on staging, configured once

Install **Rank Math SEO**, current version from the repository. Do not install
AIOSEO. Do not clone CFI's older build — its Redirections page never renders its
"Add New" form, which is why redirects there have to go straight into the
database.

In the setup wizard, when it offers to import from another plugin: **there is
nothing to import.** Skip it. The production site's AIOSEO data is 9 URLs of
which 7 have no meta description and 2 have auto-fill. Nothing is worth carrying.

Then configure the entity **once**, in
**Rank Math → Titles & Meta → Local SEO** — values are in `IDENTITY.md`:

| Field | Value |
|---|---|
| Person or Company | Company |
| Business type | `InsuranceAgency` (fall back to `LocalBusiness` if Free does not offer it) |
| Name | Cheap Sober Living Insurance |
| Street | 7960 Silverton Ave. #202 |
| City / Region / Postcode / Country | San Diego / CA / 92126 / US |
| Phone | +1-858-295-7242 |
| Hours | Mon–Fri 09:00–17:00 |

**Do not paste hand-written JSON-LD into a Code module.** That is exactly what
production did, and it now emits two organization entities with two different
phone numbers. One source of organization data, and it is Rank Math.

---

## Step 3 — URL parity before cutover

Cutover needs **zero redirects** if the new site reproduces these slugs exactly.
Right now staging has none of them — `/quote-now/` returns 404 there.

| Must exist on staging | Status today |
|---|---|
| `/` | ✅ exists |
| `/quote-now/` | ❌ 404 — **build at this slug, not `/quote/`** |
| `/coping-with-challenges-in-sober-living-operations-top-ten-concerns-and-solutions/` | ❌ |
| `/essential-checklist-to-safeguard-your-sober-living-home-from-liability-claims/` | ❌ |
| `/why-professional-liability-insurance-is-crucial-for-operators-of-sober-living-homes/` | ❌ |
| `/category/resources/` | ❌ |

The three posts keep their existing URLs. Migrate the content, do not re-slug it.

Noindex the category and the three tag archives in Rank Math — four empty
archives against five real pages is a bad ratio, and it is free to fix now.

---

## Step 4 — Cutover

Follow playbook Part 1 **Option A** — build in staging, then move the build into
the real docroot and leave the domain's document root unchanged. Unlike CFI, the
real directory `/home/mrtaco5/cheapsoberlivinginsurance.com/` still exists, so
Option A is available and clean.

The invariant: **when you finish, no folder is named after a site it does not
contain.** Write the `READ-ME-WHICH-SITE-IS-THIS.txt` marker file the same hour.

### The folder never stays called "staging"

This is the CFI trap, and it is avoidable here. On CFI the domain's document
root was *repointed* at the staging folder, so the staging folder became
production and kept its wrong name. **Do not repoint anything.** Move the
content instead and leave the document root exactly where cPanel already has it.

Confirm the real docroot first in **cPanel → Domains** — it should be
`/home/mrtaco5/cheapsoberlivinginsurance.com/`, since CFI is the only site on
this account whose directory does not match its domain. Verify rather than
assume.

Then cutover is two renames, back to back, in cPanel Terminal:

```bash
cd /home/mrtaco5
mv cheapsoberlivinginsurance.com          ZZ-OLD-divi-csli-2026-08-21
mv staging.cheapsoberlivinginsurance.com  cheapsoberlivinginsurance.com
```

Both are same-filesystem renames, so they are instant. Downtime is the gap
between the two commands — seconds. Afterwards:

- the document root in cPanel is **unchanged**
- the live site sits in a folder named after the live site
- there is no folder called `staging.` any more
- the old Divi site is clearly labelled as old, with a date

Delete the `staging.` **subdomain** in cPanel afterwards, or it will point at a
path that no longer exists. Keep `ZZ-OLD-…` for 30 days as rollback, then delete
it — and put that date in the marker file so it is not kept forever or binned
early.

### 🔴 Basic Auth travels with the folder

cPanel's Directory Privacy writes `AuthType Basic` and an `AuthUserFile` path
into the `.htaccess` **inside** the protected directory. When you rename that
directory into the live docroot, the `.htaccess` comes with it — so the live
site will demand a password the moment it goes up. Worse, `AuthUserFile` holds
an **absolute path** that no longer exists after the move, which can produce a
500 rather than a clean login prompt.

**Turn Directory Privacy off before the rename, not after.** Untick it in cPanel
for the staging directory, confirm the site returns 200 to an anonymous request,
and only then run the two `mv` commands. Grep the `.htaccess` afterwards to be
sure nothing is left:

```bash
grep -iE 'AuthType|AuthUserFile|Require valid-user' /home/mrtaco5/cheapsoberlivinginsurance.com/.htaccess
# expect no output
```

The same absolute-path problem applies to **Wordfence** if it is installed on
staging — it stores absolute paths and they break on a move. Check whether it is
active there before cutover; if it is, either deactivate it before the rename
and reactivate after, or do not install it on staging in the first place.

### The four cutover-day items that are easy to forget

**1. Remove the Basic Auth — before the rename.** See above: it travels with
the folder and its `AuthUserFile` path breaks on the move. The site will
otherwise be perfectly built, perfectly invisible, and returning 401 or 500 to
Google.

**2. Search-replace the staging URLs out of the database.** The database will be
full of `staging.cheapsoberlivinginsurance.com`. Use
**`wp search-replace 'staging.cheapsoberlivinginsurance.com' 'cheapsoberlivinginsurance.com' --all-tables`**
via cPanel Terminal — run it with `--dry-run` first.

> **Never do this with a SQL find-and-replace or a text editor on a dump.**
> WordPress stores widget and theme settings as PHP-serialized arrays with
> byte-length prefixes. Changing the string without fixing the prefix corrupts
> them, and the breakage shows up later as silently missing settings.

**3. Redirect the old sitemap URL.** Production serves AIOSEO's `/sitemap.xml`
today and that URL is in GSC and in the current robots.txt. Rank Math serves
`/sitemap_index.xml`. Add a 301 `/sitemap.xml` → `/sitemap_index.xml` in
Rank Math → Redirections, and resubmit the new sitemap in Search Console.

Also confirm the old AIOSEO 302 from `/sitemap_index.xml` → `/sitemap.xml` is
gone. It should die with the old install; if it was hardcoded into `.htaccess`
it will shadow Rank Math's sitemap silently. Check before concluding the sitemap
is broken.

**4. Delete the Cognito test entries.** Staging submissions land in the real
form. Clear them before launch so the operator's entry list is clean.

---

## Pass conditions at cutover

| Check | Expected |
|---|---|
| `https://cheapsoberlivinginsurance.com/` | 200, Kadence, apex canonical |
| Basic Auth | **removed** — no 401 anywhere |
| `noindex` anywhere on production | **none** |
| all 5 content URLs | 200, same slugs as before |
| `/quote/` | still 301 → `/quote-now/` |
| `/sitemap_index.xml` | 200, Rank Math |
| `/sitemap.xml` | 301 → `/sitemap_index.xml` |
| organization nodes on homepage | exactly **1**, phone `+1-858-295-7242` |
| `staging.` in page source or DB | **0 occurrences** |
| marker file in docroot | present, returns 200 over the public domain |
| `.htaccess` auth directives | **none** |
| folder named `staging.` | **gone** |
| live docroot folder name | matches the domain |

Verify everything anonymously **and** with `?cb=$(date +%s%N)`. On this account a
plain anonymous curl has returned pre-edit content while reporting
`x-proxy-cache: MISS`, which produced a confident, wrong verdict on 17 Aug.
