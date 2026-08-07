# California flip — what actually happened, 6 Aug 2026

Written during the cutover. **Statewide will hit every one of these**, which is the whole reason
for doing California first. Read this before flipping statewide.

---

## The docroot edit worked exactly as documented

cPanel → Domains → Manage → **New Document Root**. Result:
`/home/mrtaco5/californiafloodinsurance.com` → `/home/mrtaco5/new.californiafloodinsurance.com`.
Kadence child serving immediately, zero Divi markup. Nothing moved on disk.

**Two details the runbook did not have and should have:**

1. **The field takes a path relative to the home directory, with no leading slash.** The `🏠/`
   icon is the prefix. The field contained `californiafloodinsurance.com`, not
   `/californiafloodinsurance.com`. The runbook showed leading slashes because that is how the
   Document Root *displays* on the right-hand panel.
2. **A red "Remove Domain" button sits directly below the blue Update button**, and it
   permanently deletes the domain from the account with no undo. Worth knowing before you are
   clicking quickly.

Also worth doing first: read the target path off the **staging subdomain's own row** in List
Domains and copy it, rather than assuming the folder is named after the subdomain. cPanel does not
always name it that way, and a path that does not exist gets you a blank site rather than an error.

## Then the site 301'd everything to the staging hostname

Expected, not a fault — WordPress redirects to `home_url` to match itself. But it means **the
public domain hands every visitor to a noindexed staging URL** until the site address is fixed, so
step 3 is genuinely urgent rather than merely next.

`x-redirect-by: WordPress` in the response headers is what proves it is WordPress and not the
cache or a plugin. Check that header before assuming anything.

## The mistake that cost a round trip: the wrong wp-config.php

The docroot swap means the file WordPress loads is now
`/home/mrtaco5/new.californiafloodinsurance.com/wp-config.php`. Editing the one in the
`californiafloodinsurance.com` folder — the natural habit — changes the **old Divi install** and
does nothing. It is harmless (that site is not being served, and the values are right for it
anyway), but it looks like the fix failed.

**Positive check before editing:** the new install's `DB_NAME` is `mrtaco5_wp441`, and the old
one's differs. Confirm the database name, not just the path.

## A real gotcha: REST `settings.url` is `siteurl`, NOT `home`

Worth stating flatly because I got it wrong live. The WordPress REST settings endpoint exposes a
field called `url`. **It maps to `siteurl`.** `home` is not exposed at all.

So `POST /wp/v2/settings {"url": "..."}` sets `siteurl` and leaves `home` alone, producing a split
state where the site still redirects (because the redirect follows `home_url`) even though the
write reported success. One useful side effect: with `siteurl` correct, `wp-login.php` becomes
reachable on the production domain, which is convenient mid-flip.

**There is no REST route to `home`.** It has to be `WP_HOME` in `wp-config.php`, WP-CLI, or
Settings → General.

Setting both constants is the right move regardless — it pins the URLs somewhere a bad
search-replace cannot reach, so the site cannot lock you out.

## Step 3b: there was no search-replace plugin installed

Only five plugins on the live install: EWWW, Nginx Helper, Rank Math, Widgets for Google Reviews,
Wordfence. **No Better Search Replace.** Rather than install one mid-cutover, the 15 stray URLs
were fixed surgically over REST, because there were only three sources:

| Source | Count | Fixed by |
|---|---|---|
| 6 nav menu items (custom links, claims cluster) | 12 rendered (nav renders twice) | `POST /wp/v2/menu-items/<id>` |
| 6 pages with absolute URLs in content | 12 stored | `POST /wp/v2/pages/<id>` |
| Rank Math Organization URL + logo | 3 per page | **Rank Math settings — not REST-reachable** |

Being surgical beat a blanket replace here: fewer rows touched, and every change verifiable
individually.

**For statewide, check the plugin list first.** If Better Search Replace is present there, use it
with *all tables selected* and a dry run — the menu items live in `wp_postmeta`, which a
posts-only replace would miss.

## Four sources of stray hostname, not one — and two were unexpected

`new.californiafloodinsurance.com` appeared **47 times** across the site after the database was
clean. It came from four places, and only the first two were the obvious ones:

| # | Source | Where it lives | Fix |
|---|---|---|---|
| 1 | 6 nav menu items (custom links, claims cluster) | `wp_postmeta` | REST `menu-items` |
| 2 | 6 pages with absolute URLs in content | `wp_posts` | REST `pages` |
| 3 | **Rank Math Organization URL + logo** | Rank Math options | Titles & Meta → Local SEO |
| 4 | **Rank Math breadcrumb "Homepage Link"** | Rank Math options | General Settings → Breadcrumbs |
| 5 | **The WordPress user's "Website" profile field** | `wp_users.user_url` | REST `users/<id>` |

**Number 5 is the one to remember.** User 1's Website field held the staging homepage, and it fed
two things at once: the visible author byline link (`<a class="url fn n">`) on every post and
archive listing, and `sameAs` on the Person schema node. `/insights/` alone carried 10 of them,
one per listed post. Nothing about "search and replace the database" suggests looking in the users
table, and a posts-only replace would never have found it.

**Number 4 is the one that survives everything else.** The breadcrumb home link renders twice per
interior page — once in the visible `rank-math-breadcrumb` nav, once in the `BreadcrumbList`
JSON-LD — and it is invisible on the homepage, which is exactly where you would check first and
conclude you were done.

Diagnostic order that worked: fix, then re-scan **rendered pages** rather than the database, and
grep the surrounding 80 characters of every remaining hit. The context string names the culprit
immediately — `rank-math-breadcrumb`, `class="url fn n"`, `"logo"` — where a bare count tells you
nothing.

## The cache lied about the result, twice

Both times the fix was fine and the verification was wrong.

- A REST re-scan without a cache-buster reported **12 occurrences remaining** when the database
  actually had 0. InMotion's nginx caches authenticated `/wp-json/` responses. The individual
  `POST` responses were trustworthy because POSTs are not cached.
- Every read needs a **unique** cache-buster per request. A fixed token becomes its own cacheable
  URL — the same bug that made `preflight.py` report phantom broken links on 4 Aug.

Check `x-proxy-cache` on anything you are using to make a decision. `MISS` means you are reading
reality.

## A server-side purge left 41% of the site stale — and a re-save fixes it

After the noindex came off and Aaron purged server-side, **26 of 63 URLs were still serving
pre-purge HTML with `nofollow, noindex`**. Every one was an `x-proxy-cache: HIT`; every `MISS` was
correct. This is the 4 Aug behaviour again but far worse — that time it was 4 of 85, this time 26
of 63.

**A 21-URL spot check found only 7 of the 26.** Sampling is not good enough here. Enumerate every
published URL from the REST API and check them all, because the stale set is arbitrary — it is
whichever clean URLs happened to be requested and cached beforehand.

**The fix that worked, with no plugin and no server access:** write a post's *identical* content
back via `POST /wp/v2/<type>/<id>`. That fires WordPress's save hooks, Nginx Helper purges that
one URL, and the next request regenerates it. Verified: `/claims/` went `HIT/noindex` →
`MISS/index` in under three seconds.

```
GET  /wp/v2/pages/<id>?context=edit&_fields=content   → read raw
POST /wp/v2/pages/<id>  {"content": <same raw>}        → no-op save, purges that URL
```

**Its limit:** it only reaches things that are a post or page. The homepage, archives, category
pages and anything template-driven cannot be purged this way. Those need a working purge.

**Aaron's purge is partly broken and it should be fixed before statewide.** Two symptoms point at
one cause: there is no `Purge Cache` item in the admin toolbar, *and* Nginx Helper's own
"Purge Entire Cache" button returns "you do not have the necessary privileges" for an
administrator. With Nginx Helper's **Enable Purge** unchecked the toolbar item does not render at
all, which fits both symptoms. Check Settings → Nginx Helper first.

## Order that matters, confirmed by doing it

1. Docroot
2. **`WP_HOME` + `WP_SITEURL` in the correct wp-config.php** — before anything else, because the
   site is bouncing visitors to staging until this lands
3. Database hostname replace — nav menu items, page content
4. **Rank Math Organization URL + logo** — schema-only, but Google reads it
5. Only then take the noindex off
6. **Purge, then verify every URL — not a sample.** Expect a large stale set.
7. **Install the redirects immediately.** Between the flip and the `.htaccess` install, every
   pruned URL is a hard 404 on the live domain. On California that was 37 URLs that had been 200
   that morning. This gap is the one genuinely damaging interval in the whole procedure, and it is
   easy to leave open because the site looks finished.

Taking the noindex off before 3 and 4 would invite Google to index the staging hostname and to
read an Organization node pointing at it.

**One thing to schedule, not defer:** the moment the noindex comes off, the staging hostname
becomes an indexable duplicate — it still serves the same directory. Canonicals point at
production, which limits it, but delete the subdomain or add the hostname redirect the same day.

## Confirmed working the moment the domain moved

- `cfi-kadence-child` serving, no Divi markup anywhere
- **GTM-MZ6RZ94 started printing by itself** — the theme's host gate woke up on the production
  hostname exactly as designed, with no intervention. That was the single most uncertain piece of
  the theme and it worked.
- `noindex` still in place throughout, protecting the site while the URLs were being cleaned up
