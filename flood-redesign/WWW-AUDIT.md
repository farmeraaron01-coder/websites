# The `www` audit — stop publishing `www`, keep supporting it

Started 13 Aug 2026, after Aaron ran PSI on `https://www.statewidefloodinsurance.com/` and it scored mobile 65
with a **Failed** Core Web Vitals assessment and a field TTFB of **3 s**.

## Why this is worth doing at all

Measured, five runs each, same moment:

| | redirects | TTFB median |
|---|---|---|
| `www.statewidefloodinsurance.com` | 1 | **1.88 s** |
| `statewidefloodinsurance.com` | 0 | **0.52 s** |

**`www` costs roughly 1.35 s before a byte of the real page arrives.** A second DNS lookup, a second TLS
handshake, the 301, and only then the request that matters. Slow-4G multiplies it.

**The score is not the point.** CrUX only publishes a URL when real Chrome users load it, so field data existing
for `www` proves **real visitors land there and pay that penalty every time.** This is a user-experience defect
that happens to also depress a score.

## THE RULE

**Keep the `www` → apex 301 forever.** People type `www`, old links exist, and removing the redirect would
break them. The goal is to stop *publishing* `www`, not to stop *supporting* it. Every redirect that fires is a
link somebody should have written as apex.

---

## Confirmed sources — found 13 Aug

### 1. The Google Business Profile website field. Highest value on this list.

`PLUGIN-PLAN.md:433`, recorded from the GBP itself:

```
| Website | `http://www.californiafloodinsurance.com/` |
```

**Wrong twice — `http` *and* `www`.** For a local insurance agency, GBP is a major share of non-paid clicks, and
every one of them takes the redirect. This was already half-flagged as item 27 in `OPEN-ITEMS.md` ("set the GBP
website URL to `https://`"); the `www` half was missed.

**Fix:** GBP → Edit profile → Contact → Website → `https://californiafloodinsurance.com/`. Also check the
appointment/booking link if one is set.

### 2. Email signatures — 41 files in `signatures/`

| Count | URL |
|---|---|
| 23 | `http://www.californiafloodinsurance.com/` |
| 16 | `http://www.jumpins.com/` |
| 2 | `https://www.jumptruckinginsurance.com/` |

Every staff email sends recipients through a redirect, and email clicks are among the highest-intent traffic
there is. Measured: `http://www.californiafloodinsurance.com/` takes 1.00 s to land versus 0.74 s for apex;
`http://www.jumpins.com/` takes 1.4–2.2 s versus 0.8–1.3 s.

**Two parts to this fix, and the second is the real work.** Correcting the repo files is one command. The
signatures already pasted into 40-odd people's mail clients do not change until each person re-pastes, so this
needs a decision about how to roll out, not just an edit.

### 3. A stale document that would reintroduce it

`HEADER-FOOTER-SETUP.md:78` contains footer HTML using `https://www.statewidefloodinsurance.com/`. The live
sites are clean, so this is only a landmine for whoever pastes from that doc next.

### 4. Search Console has a `www` property

`LAUNCH.md:468`: `http://www.californiafloodinsurance.com/` exists as a URL-prefix property. Not a traffic
source — but useful, because its Performance report shows exactly how many clicks are still arriving on `www`.

---

## Verified clean — do not spend time here

- **Both live sites' HTML.** Zero `www` self-references on either homepage; canonical and `og:url` both apex.
- **Both sitemaps.** Apex only.
- **Theme constants.** `CFI_QUOTE_URL` and `CFI_SISTER_NOTE` are apex on both brands.
- `tools/cfi_home2.html` has a `www` footer link but it is an archived Divi export, not served.

---

## What only Aaron can check, in value order

1. **Google Ads** — final URLs, sitelink/callout/promotion extensions, tracking template, final URL suffix.
2. **Microsoft Ads** — the same fields. Carries ~$12,607/mo, so it is not a rounding error.
3. **Bing Places.**
4. **Facebook, LinkedIn, YouTube** page "website" fields.
5. **Directory, association and license listings** — DOI/NAIC profile, any agency directories.
6. **Print** — cards, wraps, flyers. Cannot be fixed retroactively; note it for the next reprint.

### ⚠ Diagnose before editing Google Ads

**Editing an ad's final URL in Google Ads is treated as creating a new ad, which resets that ad's stats and
learning.** So do not bulk-edit final URLs to fix `www` — first establish whether the ads even use `www`. They
may already be apex, in which case the entire `www` problem is GBP plus email signatures and there is nothing to
risk.

### The report that answers it in one look

GA4 → Explore → blank exploration:

- Dimension: **Hostname**
- Second dimension: **Session source / medium**
- Metric: **Sessions**
- Range: last 28 days, to match CrUX

That gives the share of sessions landing on `www` **and where they came from**, so the fix targets the sources
that actually carry traffic rather than every place a URL was ever typed. Search Console's `www` property
Performance report is the cross-check.

---

## Order of work

1. **GA4 hostname report** — 10 minutes, tells you whether this is a big problem or a small one, and which
   sources matter. Everything else depends on it.
2. **GBP website field** — one edit, likely the largest single share.
3. **Signatures** — repo fix is trivial; decide how to redeploy.
4. **Ads**, only if the GA4 report shows paid traffic on `www`, and knowing the stats-reset cost.
5. **Re-run PSI on `https://statewidefloodinsurance.com/`** for a real baseline, and note in
   `PERFORMANCE.md` that any score compared against the 12 Aug `www` run is not comparable.
