# Repo and infrastructure notes

This repo holds website assets — email signatures (`signatures/`, `img/`) and
SEO working files (`seo/`). It is **not** the source of any live website; the
sites are WordPress installs on cPanel hosting.

---

## californiafloodinsurance.com — READ THIS BEFORE TOUCHING HOSTING

Host: InMotion, cPanel account **`mrtaco5`** (`secure234.inmotionhosting.com`).

### The folder names are misleading. Verify before any destructive action.

| Folder | What it is |
|---|---|
| `/home/mrtaco5/`**`new.californiafloodinsurance.com`**`/` | **LIVE PRODUCTION.** Serves `californiafloodinsurance.com`. |
| `/home/mrtaco5/`**`californiafloodinsurance.com`**`/` | **GONE.** Was the old Divi site; uninstalled 16 Aug 2026 after backup. Softaculous's Uninstall removed the directory itself, so this path no longer exists. |

On 6 Aug 2026 the domain's document root was pointed at the staging folder and
that folder became production. The names were never swapped, so **the live site
lives in a directory named `new.californiafloodinsurance.com`** — every other
site on this account has a directory matching its domain; this one is the sole
exception.

Until 16 Aug 2026 a second directory named `californiafloodinsurance.com` also
existed, holding the old Divi site, and the misleading pair cost about two days
of debugging. That directory is now gone. Do **not** rename the live directory
to fill the gap: it is the vhost document root for `californiafloodinsurance.com`,
`new.`, `ipv6.`, and `californiafloodinsurance.mrtacoshop.com`, so renaming it
takes the site down until every docroot is repointed, and Wordfence stores
absolute paths that break on a move. Verify docroots in cPanel → Domains.

Live install facts:
- DB: `mrtaco5_wp441`
- Theme: `cfi-kadence-child` (parent: `kadence`)
- SEO plugin: Rank Math
- A note recording this lives on the server at
  `/home/mrtaco5/new.californiafloodinsurance.com/READ-ME-WHICH-SITE-IS-THIS.txt`

Ways to confirm which folder is live, from outside, without shell access:
1. Live site's theme path in page HTML — production is `cfi-kadence-child`; the
   old site is Divi (`et_pb_`, `elegantthemes`).
2. `curl -s https://californiafloodinsurance.com/feed/ | grep 'wordpress.org/?v='`
   and compare to the version each install reports in Softaculous.
3. Compare the byte size of `https://californiafloodinsurance.com/llms.txt`
   against the `llms.txt` in each folder. Exact match identifies the docroot.

Softaculous lists both installs with the **same** Website URL, so the URL column
cannot distinguish them. Only **Website Path** can. WP Toolkit lists only one of
them and labels it "California Flood Insurance - Staging", which is wrong — that
is production.

### Backups live in Dropbox, not on the server

UpdraftPlus runs on the live install with **Dropbox as a remote destination and
local copies deleted after upload**. So `wp-content/updraft/` holds only logs and
config — that is normal, not a missing backup. A server-side search will find
nothing; look in Dropbox:

`/Aaron Farmer/Apps/UpdraftPlus.Com/`

Filenames are `backup_<date>-<time>_California_Flood_Insurance_<hash>-{db.gz,uploads.zip,plugins.zip,themes.zip,others.zip}`.

**Telling the old Divi site from the current one by size:** pre-cutover sets have
a ~101 MB uploads archive and ~92 MB plugins; post-cutover sets are ~16 MB and
~34 MB. The live site's media library holds only 21 items, which is what the
small archives reflect. The **2026-08-06** set is the last Divi backup and is the
rollback for the pre-cutover site — the server directory it came from was deleted
16 Aug 2026, so that archive is the only copy.

Check the backup cadence periodically. As of 16 Aug 2026 CFI's newest set was
three days old while the other sites on the account had run within 24 hours.

### Caching: two layers, both have bitten us

**1. nginx page cache** (cPanel → Cache Manager, and the Nginx Helper plugin).

- Configure the domain **`californiafloodinsurance.com`**. The dropdown also
  offers `new.californiafloodinsurance.com` and `ipv6.` variants; rules set on
  those do nothing for public traffic. Apply rules to the apex, and to `new.`
  as well so a wrong pick is harmless.
- Sitemap and robots XML must be bypassed. WordPress already sends
  `Cache-Control: no-cache, no-store, must-revalidate` on them and the host's
  nginx overrides it. Bypass URL entries (regex supported):
  ```
  .*sitemap.*
  /robots.txt
  ```
  **Status:** applied 16 Aug 2026 to both `californiafloodinsurance.com` and
  `new.californiafloodinsurance.com`. Sitemap and robots responses now return
  `x-proxy-cache: BYPASS`. If that header ever reads `HIT` again, the rules were
  lost — re-add them.
- **Cache purging does not work on this account — assume you cannot purge.**
  Nginx Helper's "Purge Entire Cache" returns a privileges error; cPanel →
  Cache Manager's single-URL purge and "Purge Full Cache" both complete
  silently with no effect (verified 16 Aug 2026 across several attempts, with
  a cached object still serving a three-day-old `last-modified`). Design around
  it: put anything that must be fresh into the Bypass URL list rather than
  relying on a purge. HTML pages self-heal on the 4-hour Default Refresh Time.
  Worth an InMotion ticket — a site you cannot purge is a problem waiting for
  the next urgent edit.
- **A new Bypass URL rule is not applied immediately.** Adding `/llms.txt` took
  several minutes to start returning `BYPASS`; it saved and persisted the whole
  time. Wait and re-check before concluding a rule failed.
- **Logged-in requests bypass the cache.** Always verify sitemaps and robots in
  an incognito window or via curl. Checking while logged into wp-admin shows you
  what WordPress thinks, not what Googlebot receives.
- **`x-proxy-cache: MISS` does NOT prove you got a fresh response.** On 17 Aug
  2026 a plain anonymous curl of two statewidefloodinsurance.com pages returned
  pre-edit content and reported `MISS`, while the origin already had the edits.
  That produced a confident, wrong "the edit did not apply" verdict.
  **Append a unique query string to every verification fetch**
  (`?cb=$(date +%s%N)`). It changes the cache key, so the request reaches PHP.
  Cross-check by comparing byte sizes with and without the query string — if
  they differ, the plain URL is serving a stale copy and only the query-string
  response is real. Remember that a query-string URL rules out the *nginx* layer
  only; both URLs still execute PHP.

**2. Rank Math's internal sitemap cache.**

Rank Math can serve a frozen sitemap even when nothing is misconfigured — no
exclusions, no noindex, post published and live. Symptom: recent posts missing
and `sitemap_index.xml` lastmod disagreeing with the child sitemap.

"Remove transients" (Status & Tools → Database Tools) does **not** clear it.
The fix is to save Sitemap Settings with a value genuinely changed:

> Sitemap Settings → General → change Links Per Sitemap 200 → 199 → Save,
> then 199 → 200 → Save.

Saving with nothing altered may be a no-op. Same trap as clicking Update on a
WordPress post with no edits — the handler short-circuits and the cache
invalidation never fires.

---

## Other WordPress installs on the `mrtaco5` account

`statewidefloodinsurance.com`, `restaurant-insurance.com` (Jump Insurance
Services), `cheapearthquakeinsurance.com`, `cheapsoberlivinginsurance.com`,
`topdogpetinsurance.com`, `mrtacoshop.com`.

They share the same nginx cache layer, so any running Rank Math has the same
sitemap-caching exposure. As of Aug 2026, `restaurant-insurance.com` showed a
10.0 security risk and `topdogpetinsurance.com` was several major versions
behind.

---

## Conventions

- Do not commit diagnostic dumps (sitemap XML, curl output) to this repo.
- SEO deliverables go in `seo/<page-slug>/` with a README explaining what to
  apply and what still needs a human decision.
