# cheapearthquakeinsurance.com — Spam Link Injection Incident (found July 15, 2026)

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

### Phase B — Root cause & hardening (Aaron + host; needs approvals)
1. WP Admin → Users (on CEI): look for unknown administrator accounts — delete any not recognized (screenshot first).
2. Check post REVISIONS on /commercial-earthquake/ to date the injection and identify the user account that made it.
3. Install Wordfence (free) on CEI → full scan (compares core/plugin/theme files against wordpress.org originals; finds webshells). [Plugin install = Aaron's approval]
4. Ask InMotion support to run an account-level malware scan (covers both sites' files) — can go in the same ticket as the pending security-headers request.
5. Change passwords: all WP admin users on CEI, cPanel/InMotion, FTP, database. Enable 2FA on WP admin and InMotion.
6. Update everything on CEI (core, theme, all 15 plugins); delete any plugins/themes not in use.
7. Google Search Console (CEI property, verified July 13): check Security & Manual Actions → both sections; after cleanup, request re-indexing of the cleaned URLs.

### Phase C — Post-cleanup verification
- Re-run the full two-site crawl for spam patterns (Claude Code).
- Re-check key pages with Googlebot UA (cloaking check).
- Watch GSC for the cleaned pages being re-crawled.

## Scan details
- Method: fetched all URLs from both sites' sitemap indexes (104 URLs), grepped server HTML for hidden-link patterns (≤3px images inside external anchors) and spam keyword families (replica/vape/casino/pharma/essay/betting).
- jumpins.com: 0 real hits (2 false positives from "specialists").
- cheapearthquakeinsurance.com: 10 URLs affected (8 posts via template injection + 2 pages with direct content injection).
