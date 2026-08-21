# Step 1 — Move cheapsoberlivinginsurance.com from All in One SEO to Rank Math

**Do this before the Divi → Kadence rebuild, as its own change.**

Two reasons. One variable at a time: if the sitemap breaks after doing both at
once you will not know which change did it. And the rebuild wants to be done
*on* Rank Math, not migrated onto it afterwards.

Scope is small — 9 URLs, and seven of them have no meta description to lose.
Budget under an hour.

---

## Order matters. Step 0 is not optional.

### Step 0 — nginx cache bypass FIRST

The sitemap on this domain currently serves `x-proxy-cache: HIT`, and **purging
does not work on this hosting account** (proven repeatedly — Nginx Helper
returns a privileges error, cPanel Cache Manager completes silently and does
nothing). If you swap SEO plugins before adding the bypass rule you will be
staring at a cached AIOSEO sitemap with no way to clear it, and no way to tell
whether Rank Math is working.

cPanel → **Cache Manager** → select **`cheapsoberlivinginsurance.com`** → add to
Bypass URLs:

```
.*sitemap.*
/robots.txt
```

Apply to the `www.` and `ipv6.` variants too if the dropdown offers them — a
wrong pick then costs nothing.

**A new bypass rule takes several minutes to take effect.** It saves instantly
and keeps working; it just is not live yet. Wait and re-check rather than
concluding it failed.

**Do not continue until this returns `BYPASS`:**

```bash
curl -sSI "https://cheapsoberlivinginsurance.com/sitemap.xml" | grep -i x-proxy-cache
```

### Step 1 — Confirm a backup exists

UpdraftPlus on this account uploads to Dropbox and deletes local copies, so
`wp-content/updraft/` holding only logs is normal, not a missing backup. Look in:

`/Aaron Farmer/Apps/UpdraftPlus.Com/`

If there is no recent set for this site, run a manual backup and wait for it to
finish uploading before touching anything.

### Step 2 — Install Rank Math

Plugins → Add New → **Rank Math SEO** → install and activate. Take the **current**
version from the repository.

> Do not clone the build running on californiafloodinsurance.com. CFI runs an
> older Rank Math whose Redirections page never renders its "Add New" form, which
> is why redirects there have to be inserted straight into the database. Start
> this site on a current build and it will not inherit that problem.

### Step 3 — Run the AIOSEO import

Rank Math's Setup Wizard detects All in One SEO and offers to import from it. If
you have already dismissed the wizard, it is at
**Rank Math → Status & Tools → Import & Export → Import from other plugins.**

Import settings, post meta and redirections. Then read the result against the
baseline below — there is very little to carry, so a thin import is expected,
not a failure.

### Step 4 — Deactivate All in One SEO

Immediately after the import. **Do not leave both plugins active**: two SEO
plugins emit two canonicals, two title tags and two schema graphs, and Google
picks one at random.

Deactivate, do not delete, until Step 6 passes. Deactivation is the rollback.

### Step 5 — Clear the two AIOSEO leftovers

**a. The sitemap redirect.** `/sitemap_index.xml` currently 302s to
`/sitemap.xml`. That is AIOSEO's Yoast-compat rule and should vanish when AIOSEO
is deactivated. Rank Math serves at `/sitemap_index.xml` — the exact URL being
redirected away. Confirm it is gone:

```bash
curl -sSI "https://cheapsoberlivinginsurance.com/sitemap_index.xml" | head -1
```

If that still shows 302, the rule was hardcoded. Check `.htaccess` in the docroot
via cPanel File Manager for a line mentioning `sitemap` and remove it. **Back the
file up first** (`cp -p .htaccess .htaccess.bak-2026-08-21`) — a bad `.htaccess`
takes the whole site down.

**b. robots.txt.** It currently advertises `/sitemap.xml` and `/sitemap.rss`,
both of which will 404 once AIOSEO is off. Check whether a *physical*
`robots.txt` exists in the docroot: if it does, edit it; if not, WordPress is
generating it virtually and Rank Math will take it over
(**Rank Math → General Settings → Edit robots.txt**). Either way it should end up
pointing at:

```
Sitemap: https://cheapsoberlivinginsurance.com/sitemap_index.xml
```

### Step 6 — Verify

Every check anonymous **and** cache-busted. On this account a plain anonymous
`curl` has returned pre-edit content while reporting `x-proxy-cache: MISS` — that
produced a confident, wrong verdict on 17 Aug and cost a day. The query string is
the load-bearing part.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CB="?cb=$(date +%s%N)"
BASE=https://cheapsoberlivinginsurance.com

# 1. Rank Math sitemap resolves and is Rank Math's, not AIOSEO's
curl -sSL -A "$UA" "$BASE/sitemap_index.xml$CB" | head -5

# 2. all 5 content URLs present across the child sitemaps
for s in page-sitemap post-sitemap; do
  curl -sSL -A "$UA" "$BASE/$s.xml?cb=$(date +%s%N)" | grep -oE '<loc>[^<]*'
done

# 3. exactly one canonical and one title per page — no doubled tags
for u in "$BASE/" "$BASE/quote-now/"; do
  echo "== $u"
  curl -sSL -A "$UA" "$u?cb=$(date +%s%N)" | sed -n '1,/<\/head>/p' \
    | grep -ocE '<title>|rel="canonical"'
done

# 4. no AIOSEO fingerprint left in the markup
curl -sSL -A "$UA" "$BASE/$CB" | grep -ci 'all in one seo\|aioseo'
```

Pass conditions:

| Check | Expected |
|---|---|
| `/sitemap_index.xml` | **200**, and the comment line names Rank Math |
| `/sitemap.xml` | 404 is fine and expected |
| content URLs in sitemaps | all 5 |
| `<title>` per page | exactly 1 |
| `rel="canonical"` per page | exactly 1 |
| `aioseo` fingerprint count | **0** |
| homepage title | unchanged from baseline below |
| all 9 URLs | still **200** — nothing 404s, nothing redirects |

---

## STOP conditions

Stop and report rather than working around it if:

- any of the 9 URLs changes status code
- `/sitemap_index.xml` still 302s after `.htaccess` has been checked
- any page emits two `<title>` or two canonical tags
- the homepage title or canonical differs from the baseline
- the import offers to change permalinks — **it must not**; decline

Rollback for everything up to Step 5 is: reactivate All in One SEO, deactivate
Rank Math. That is why AIOSEO is deactivated rather than deleted.

---

## Baseline — the before-state to check against

Captured 21 Aug 2026, anonymous and cache-busted. All nine returned 200. All
carried `<meta name="robots" content="max-image-preview:large">` and nothing
else, so **all nine were indexable**.

| URL | Title | Description |
|---|---|---|
| `/` | Sober Living Home Insurance California \| Cheap Sober Living Insurance | present |
| `/quote-now/` | Get a Sober Living Insurance Quote \| Cheap Sober Living Insurance | none |
| `/coping-with-challenges…solutions/` | Coping with Challenges in Sober Living Operations: Top Ten Concerns and Solutions \| … | auto-fill |
| `/essential-checklist…liability-claims/` | Essential Checklist to Safeguard Your Sober Living Home from Liability Claims \| … | auto-fill |
| `/why-professional-liability…sober-living-homes/` | Why Professional Liability Insurance is Crucial for Operators of Sober Living Homes \| … | none |
| `/category/resources/` | Resources \| Cheap Sober Living Insurance | none, no H1 |
| `/tag/sober-living-insurance/` | sober living insurance \| Cheap Sober Living Insurance | none, no H1 |
| `/tag/sober-insurance/` | sober insurance \| Cheap Sober Living Insurance | none, no H1 |
| `/tag/halfway-house-insurance/` | halfway house insurance \| Cheap Sober Living Insurance | none, no H1 |

Homepage H1: `Sober Living Home Insurance`
Homepage canonical: `https://cheapsoberlivinginsurance.com/`

---

## Leave for the rebuild, not now

- Noindexing the category and three tag archives — do it in Rank Math once the
  rebuild starts, so there is one indexation change to verify, not two.
- Writing real meta descriptions for the seven URLs that lack them. They have
  been missing for two years; another week costs nothing, and the copy should be
  written against the new pages rather than the Divi ones.
