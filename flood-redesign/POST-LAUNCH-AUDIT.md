# Post-launch audit — California, ~4 hours after cutover

Run 6 Aug 2026 ~22:45 PDT, against the live apex. Scoped deliberately to **things that can affect
Google ranking**, not performance — performance is in `PERFORMANCE.md` and is settled.

Went live at **18:41 PDT**. This audit is roughly four hours later.

---

## Clean — verified, not assumed

| Check | Result |
|---|---|
| Sitemap URLs, all fetched | **62/62 return 200** |
| Canonical tag on each | **62/62 self-referential** |
| `noindex` leaks on indexable pages | **0** |
| JSON-LD schema present | **62/62** |
| Meta description present | **62/62** |
| Stray staging hostname in rendered HTML | **0** |
| Prune redirects | **20/20 301s + 18/18 410s firing** |
| `www.` → apex | **301** |
| `http://` → apex | **301** |
| `new.californiafloodinsurance.com` | **301 → apex** |
| statewide staging still `noindex` | **confirmed** (`nofollow, noindex`) |
| `/sitemap.xml` (advertised in robots.txt) | **301 → `/sitemap_index.xml`** — resolves |

**The `new.` subdomain is not a duplicate-content risk.** It 301s to the apex, so there is no second
crawlable copy of the site. That was the thing most likely to cost ranking and it is fine. It should
still be removed on schedule (~6 Sept, `LAUNCH.md` item 10b) because the *name* will mislead someone
later — but it is not urgent and not an SEO problem.

---

## One real defect: production `robots.txt` is still the Divi-era file

Served on production:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-content/themes/farmerflood/flood_quote/ca-flood-backup.csv
Disallow: /commercial/

Sitemap: https://californiafloodinsurance.com/sitemap.xml
Sitemap: https://californiafloodinsurance.com/sitemap.rss
```

What the new theme intends, confirmed by fetching statewide staging, which runs the same code:

```
User-agent: *
Disallow: /wp-admin/
# Claim PDFs are deliverables, not search results — the pages hold the same content.
Disallow: /wp-content/uploads/*.pdf
Allow: /wp-admin/admin-ajax.php

Sitemap: .../sitemap_index.xml
```

The theme adds the PDF rule through a `robots_txt` filter in `inc/htaccess.php:127`. **That filter is
running on staging and not reaching production output**, which means something later in the chain is
replacing the whole file — almost certainly **Rank Math's robots.txt editor holding custom content
carried over from the Divi site.** Rank Math replaces the output rather than appending to it.

### Why it matters, in order

1. **The claim-PDF exclusion is not in effect.** That was a deliberate SEO decision — a PDF result
   carries no navigation, no CTA and no phone number, so it converts far worse than the page holding
   the same content. Right now those PDFs are crawlable on production and competing with their own
   pages. This is the only item here with a real ranking consequence.
2. **`Sitemap: .../sitemap.rss` returns 404.** Search Console will log a sitemap fetch error against
   the property. Cosmetic in ranking terms, but it is a red error in a report someone will read.
3. Two dead `Disallow` lines. `farmerflood` is the **old Divi theme** and that path 404s;
   `/commercial/` only 301s. Neither does anything. The `farmerflood` line also advertises the
   historical existence of a lead-backup CSV to anyone who reads robots.txt — worth removing on
   hygiene grounds alone.

### The fix

**Rank Math → General Settings → Edit robots.txt.** Replace the stored content with:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# Claim PDFs are deliverables, not search results — the pages hold the same content.
Disallow: /wp-content/uploads/*.pdf

Sitemap: https://californiafloodinsurance.com/sitemap_index.xml
```

If the field is empty, the file is physical — look for `robots.txt` in the docroot and delete it so
WordPress serves the virtual one.

Verify with `curl -s https://californiafloodinsurance.com/robots.txt`. Expect the PDF line present
and no `sitemap.rss`.

---

## A false positive from my own audit script, recorded so it is not re-raised

The first pass reported `/commercial-flood-insurance/` as "in the sitemap but blocked by robots.txt."
**That was wrong.** My check used a substring match; robots.txt uses **prefix** matching, and
`/commercial-flood-insurance/` does not start with `/commercial/`. The page is crawlable and fine.

Same class of error as the `preflight.py` nav/footer bug and the missing `re.S` earlier in this
project: the tool was wrong, not the site. **Confirm a finding against the actual matching rules
before reporting it.**

---

## What this audit did not cover

**Search Console's own reports.** Index coverage, the video indexing issue, and any manual actions
can only be read in GSC. Worth a look once Google has recrawled — give it a few days.

**Field Core Web Vitals.** The 28-day CrUX window is still almost entirely Divi. The new site's own
field data lands around **4 September**. Divi was **failing** CWV on both form factors with a desktop
CLS of 0.2; new-site lab CLS is 0 on every run.

**Whether the 62 sitemap URLs are the *right* 62.** This checked that everything in the sitemap works,
not that nothing is missing from it. `preflight.py` covers URL parity and was run before the flip.
