# InMotion support ticket — paste this

Three requests in one ticket. The first is the important one and needs a conversation; the other two
are one-line config changes.

---

**Subject:** Cutover method for two WordPress sites, plus two nginx config requests

Hello,

I have two WordPress sites on this account that I am migrating to rebuilt versions, and I have three
requests — one question about method, and two small nginx config changes.

**1. Cutover method — I want a docroot swap, not an overwrite.**

The sites and their staging installs:

- `californiafloodinsurance.com` → rebuilt at `new.californiafloodinsurance.com`
- `statewidefloodinsurance.com` → rebuilt at `staging.statewidefloodinsurance.com`

Each staging site is a separate, complete WordPress install, not a plugin-based clone. When I go live,
I want the production domain to start serving the staging install's directory, **with the current
production install left intact on disk and its database untouched.**

Specifically, I do *not* want a "push to live" or any process that copies the staging site over the
production files, because that destroys the thing I would need to roll back to.

Please confirm:

- Can you repoint each domain's document root to the staging install's directory?
- If yes, what is the exact process and roughly how long does the change take to be live?
- Is the rollback simply repointing the document root back to the original directory?
- Are there any account-level constraints I should know about — for example whether the primary domain
  can be repointed as freely as an addon domain, or whether the staging subdomains need to be removed
  first?
- Anything about the nginx cache I should expect during the switch, and the correct way to purge it
  afterwards?

If a docroot swap is not possible on this account, please tell me what the closest reversible
equivalent is, so I can plan a rollback that does not depend on restoring a backup.

**2. Please exclude `/wp-json/` from the nginx proxy cache on both sites.**

The UltraStack nginx cache is currently caching authenticated REST API responses. I have confirmed
this: a `GET` to `/wp-json/wp/v2/themes?status=active` with valid credentials and a
`Cache-Control: no-cache` request header returns stale data, and only returns current data when a
random query string is appended to bust the cache. That makes automated checks and any tooling that
reads the REST API unreliable.

Please add an exclusion so requests to `/wp-json/` are never served from or stored in the proxy cache,
on both `californiafloodinsurance.com` and `statewidefloodinsurance.com`.

**3. Please add an `X-Robots-Tag` header for PDFs under `/wp-content/uploads/`.**

I have a set of downloadable PDF guides in the media library that I do not want appearing in search
results — the web pages holding the same content are the versions I want indexed.

I established that nginx serves `/wp-content/uploads/` directly rather than passing those requests to
Apache: a request for a nonexistent file in that directory returns nginx's own 404 page, and files
there carry `Cache-Control: max-age=604800` from your configuration rather than the headers set in my
`.htaccess`. So an `.htaccess` rule cannot reach them.

Please add, for `.pdf` files under `/wp-content/uploads/` on both sites:

```
add_header X-Robots-Tag "noindex, noarchive";
```

The existing week-long cache on that directory is fine — no change needed there, only the additional
header.

Thank you.

---

## Why each of these matters, for your own reference (not part of the ticket)

**Request 1 is the one that decides your rollback story.** If they can repoint the docroot, reverting
is minutes and the old Divi site is still sitting there. If they cannot, rollback becomes a database
and file restore, and the pre-cutover backup stops being a precaution and becomes the only way home.
Their answer determines how much of the runbook's rollback section still applies, so it is worth asking
before you schedule the flip rather than during it.

**Request 2 is quality-of-life, but it has already cost us once.** A theme-version check read stale and
I briefly concluded an install had not happened. Any future automated verification is unreliable while
this cache behaviour stands.

**Request 3 is the complete version of what robots.txt currently approximates.** Theme v1.4.0 blocks
crawling of those PDFs via robots.txt, which is effective but not the same as `noindex` — a disallowed
URL can still appear as a bare result if something links to it. The header closes that gap properly.
Not urgent; bundling it here just saves a second ticket.
