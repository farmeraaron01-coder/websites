# cheapearthquakeinsurance.com — Spam Link Injection Incident (found July 15, 2026)

## ✅ STATUS UPDATE — Phase A complete, both sites certified clean (July 15)
All three injections removed via WP admin (template Code module deleted from the "Stone Factory all posts template"; hidden image-links stripped from both service pages; site-wide search of Pages/Posts/Divi Library/Media found no stragglers). Post-cleanup verification: full 104-URL rescan of both sites = **0 spam hits**, and a Googlebot user-agent check on the three previously infected URLs = clean (no cloaking).

**Key forensic finding:** revision history on /commercial-earthquake/ shows NO trace of the spam in any revision (2022 → present). The injection was never saved through the WordPress editor — it was written directly to the database (wp_posts). Root cause is therefore server/DB-level: compromised credentials (DB, FTP, cPanel), an SQL-injection-vulnerable plugin, or a rogue script. **Phase B (below) is not optional** — the write path may still be open. Host access logs are the place to establish when/how.

## 🔴 WORDFENCE SCAN — malware located (July 16, High Sensitivity, 16,998 files)

The visible spam was only the output. Wordfence found the mechanism: **~63 malware files across 11 fake plugin folders** in `wp-content/plugins/`, all flagged Critical as `IOC:TXT/b64.fakeimage` (image header followed by base64-encoded code — the signature of rogue WP plugins). Hosting account path: `/home/mrtaco5/cheapearthquakeinsurance.com/`.

**Rogue plugin folders to remove (entire directory each):**
`ytydomice` · `ygopyt` · `tusuzeqo` · `omifat` · `lecovybym` · `hisubajy` · `egajow` · `apoleco` · `achykythuti` · `achaqes` · `OFF.lotafoxa`

Notes:
- `OFF.lotafoxa` — the `OFF.` prefix means someone previously tried to neutralize it by renaming; the payload files are still on disk.
- These are almost certainly the write-path that injected spam straight into `wp_posts` (matches the "no revision history" forensic finding). Random-word folder names + fake-image base64 files = malware, no legitimate function.
- Also flagged **High**: `wp-content/plugins/hello.php` "core file modified" — Hello Dolly, a common injection target. Useless plugin; delete it rather than repair.

**Remediation status: NOT clean.** Phase A removed the visible spam; the malware files that regenerate it are still on the server. Reinfection is likely until every rogue folder is removed AND the entry point is closed.

## 🌐 ACCOUNT-WIDE SCOPE (July 16) — this is bigger than one site

The cPanel account **`mrtaco5`** hosts **7 WordPress installs**, all sharing one filesystem:
mrtacoshop.com · restaurant-insurance.com · californiafloodinsurance.com · cheapearthquakeinsurance.com · cheapsoberlivinginsurance.com · topdogpetinsurance.com · statewidefloodinsurance.com
(plus stale copies: cheapsoberlivinginsurance.com.old, restaurant-insurance.com.old, statewidefloodinsurance.com.old, dev.californiafloodinsurance.com, dev.cheapearthquakeinsurance.com, dev.statewidefloodinsurance.com — stale/dev installs are prime entry points and must be scanned or deleted too.)

**jumpins.com is NOT on this account** (separate hosting) — consistent with its clean crawl.

Visible-content crawl of the other 6 sites (363 URLs, July 16):
- **californiafloodinsurance.com — CONFIRMED infected**: replica-watch spam links (watchesbuy.pl, tomfordreplica.ru, bestreplicawatch) in `/faqs/` content. Only 1 of 130 pages shows visible spam, but see the caveat below.
- restaurant-insurance.com, cheapsoberlivinginsurance.com, topdogpetinsurance.com, statewidefloodinsurance.com, mrtacoshop.com — no visible spam found (2 earlier "hits" were false positives: legit featured-image links whose responsive `sizes="(min-width: 0px)…"` tripped the hidden-pixel pattern; and a Nevada-flood page's legit "Las Vegas casinos" editorial text).

⚠️ **Caveat that drives the remediation:** a content crawl only sees the *visible output*, which the malware emits intermittently and per-page. It does NOT prove a site is clean. Because all 7 sites share the `mrtaco5` filesystem, the fake-plugin malware folders are very likely present on ALL of them regardless of what's currently rendered. **The definitive per-site check is Wordfence (or a File Manager look at each site's `wp-content/plugins/` for the same random-name folders), or — most efficient — the InMotion account-level scan.**

## Summary
While editing `/commercial-earthquake/`, hidden spam backlinks were discovered in the page content. A full crawl of all 104 sitemap URLs across both sites (July 15) confirmed a spam SEO injection compromise on **cheapearthquakeinsurance.com only** — **jumpins.com is clean** (its two flagged pages were a false positive: "cialis" inside the word "specialists").

## Confirmed injections (verified in live server-rendered HTML, served to both normal browsers and Googlebot)

### 1. Divi Theme Builder post template — SITE-WIDE, ACTIVE
A Code module (`et_pb_code_0_tb_body`) in the Theme Builder's post body template contains:
```html
<a href="https://www.replicaautomaticwatch.com/">mens replica watches automatic</a>
<a href="https://www.fendireplica.re/product-category/clothing/fendi-bathing-suits/">fendi bathing suits replications for sale</a>
```
Because it's in the template, it renders on EVERY post — including the brand-new commercial earthquake article published July 15. Affected: all 8 posts in the post sitemap.

### 2. /commercial-earthquake/ page content
Hidden links disguised as 1–2px invisible images (reusing the site's own legit images as the img src):
```html
<a href="https://es.wellreplicas.is/"><img alt="browse around this website" style="height:2px; width:1px;" src=".../CommercialEarthquake.jpg"></a>
<a href="https://www.vapes-pens.com/product-category/brands/elf-bar/elf-bar-lux-2000-puff/"><img alt="elf bar lux 2000" style="height:2px; width:1px;" ...></a>
```

### 3. /residential-earthquake/ page content
Same pattern:
```html
<a href="https://www.watchesbuy.to/"><img alt="replica watches under $30" style="height:2px; width:1px;" ...></a>
```
(There may be additional links on this page — inventory it fully before editing.)

## Impact
- Google penalizes/deindexes sites carrying hidden spam links; this has likely been suppressing the site's rankings for some time.
- Injections in database content (page content + Theme Builder layout) indicate the site was compromised at some point — a backdoor (rogue admin user, malicious plugin/theme file, or webshell) may still exist.
- Both sites share the same InMotion hosting account: jumpins.com's PAGES are clean, but its FILES share the filesystem — include it in malware scans.

## Cleanup plan

### Phase A — Remove the injections (Claude Chrome, content edits)
1. Divi → Theme Builder → post template (body layout) → find the Code module containing the replica links → DELETE that module. ⚠️ Do not confuse it with legitimate Code modules added July 13–15 (FAQ JSON-LD on the homepage and in post content — those contain `application/ld+json`, the spam one contains `<a href` to replica sites).
2. Edit /commercial-earthquake/ (raw text panel): remove both hidden `<a ...><img ...></a>` blocks (search for "wellreplicas" and "vapes-pens"). Then complete the planned title fix + internal link while in there.
3. Edit /residential-earthquake/: search content for "watchesbuy", "replica", and any other 1-2px img links; remove all.
4. Search ALL other pages/posts in WP admin (Posts/Pages list → search "replica", "vapes", "watchesbuy", "wellreplicas") for further instances.
5. Clear cache; verify with fresh crawl (Claude Code re-runs the 104-URL scan).

### Phase B — Malware removal (needs Aaron's go-ahead; filesystem-level)
Wordfence "Delete"/"Repair" buttons act one file at a time and won't remove whole rogue folders cleanly — do this at the filesystem level via **cPanel → File Manager** (or FTP/SSH):
1. **Back up first** — UpdraftPlus is installed on CEI. Take a full backup and download it locally before deleting anything (so removal is reversible). Note: the backup will contain the malware — it's a rollback safety net, not a clean image.
2. cPanel → File Manager → `/home/mrtaco5/cheapearthquakeinsurance.com/wp-content/plugins/` → delete each of the 11 rogue folders listed above, entirely. Also delete `hello.php`.
3. Do NOT click Wordfence "Repair" on hello.php (repair restores a file; we want it gone).
4. Re-run Wordfence scan → expect 0 Critical. Then Claude Code re-runs the 104-URL crawl to confirm no spam regenerates over the next day.
5. ⚠️ Persistence: spam malware usually plants a re-infector (a mu-plugin, a wp-config/functions.php snippet, a cron job, or a modified core file) that recreates deleted folders. If the folders come back after deletion, the entry point is still open — go straight to professional remediation (below).

### Phase B2 — Root cause & hardening (Aaron + host)
1. **Confirm blast radius:** the cPanel account is `mrtaco5`. List every domain/addon under that one account (they share the filesystem — likely includes mrtacoshop.com and possibly others). Every site on that account needs scanning. Verify whether jumpins.com is on this same account or a separate one.
2. **Scan jumpins.com with Wordfence too** — its pages are clean, but if it shares the `mrtaco5` filesystem the malware files may be present there as well.
3. **Change all credentials:** every WP admin user, cPanel/InMotion, FTP, and database password. Enable 2FA on WP admin + InMotion.
4. WP Admin → Users: delete any admin account not recognized (screenshot first).
5. InMotion support ticket: request an account-level malware scan + ask them to review access logs to date the intrusion — same ticket as the pending security-headers request.
6. Update WordPress core, theme, and all 15 plugins; delete unused plugins/themes (stale/nulled plugins are the most common entry point).
7. GSC (CEI property): check **Security & Manual Actions** → both sections; request re-indexing of cleaned URLs once verified clean.

### Professional-remediation option (recommended given a live, persistent compromise)
DIY cleanup that misses one backdoor file = reinfection within days. Given this is a business lead-gen site, strongly consider paying for expert cleanup rather than chasing files manually:
- **Wordfence Care** (~$490/yr) — already have Wordfence installed; their team cleans the site and finds the entry point.
- **InMotion malware removal** — the host can clean at the server level and check logs.
- **Sucuri** — alternative, includes a cleanup SLA.
Any of these will be faster and more certain than manual folder-deletion whack-a-mole.

### Phase C — Post-cleanup verification
- Re-run the full two-site crawl for spam patterns (Claude Code).
- Re-check key pages with Googlebot UA (cloaking check).
- Watch GSC for the cleaned pages being re-crawled.

## Scan details
- Method: fetched all URLs from both sites' sitemap indexes (104 URLs), grepped server HTML for hidden-link patterns (≤3px images inside external anchors) and spam keyword families (replica/vape/casino/pharma/essay/betting).
- jumpins.com: 0 real hits (2 false positives from "specialists").
- cheapearthquakeinsurance.com: 10 URLs affected (8 posts via template injection + 2 pages with direct content injection).
