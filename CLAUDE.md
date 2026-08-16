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
| `/home/mrtaco5/`**`californiafloodinsurance.com`**`/` | **OLD Divi site.** Dormant, kept for rollback. No hostname routes to it. |

The directory named after the live domain is the **dead** one. On 6 Aug 2026 the
domain's document root was pointed at the staging folder, and that folder became
production. The names were never swapped.

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
- Nginx Helper's "Purge Entire Cache" button returns a privileges error on this
  install. Purge from cPanel → Cache Manager → Purge Cache instead.
- **Logged-in requests bypass the cache.** Always verify sitemaps and robots in
  an incognito window or via curl. Checking while logged into wp-admin shows you
  what WordPress thinks, not what Googlebot receives.

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
