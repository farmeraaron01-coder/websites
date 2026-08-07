# Performance — what the numbers actually are, and why

Written 7 Aug 2026, the night California went live. It exists because the scores we quoted for two
weeks were measured with tagging switched off, and because two attempts to recover them made things
worse. Both belong on the record.

---

## The headline correction

> **Read "The controlled experiment — 7 Aug" first.** It is the section that actually answers the
> question, and it supersedes the diagnosis in the two sections above it. Short version: **the theme
> measures 95 on mobile with the tag scripts blocked.** The pages are not what is slow.

**Staging measured 98–99 mobile. The live site measures 61 on PSI.** Nothing about the pages changed.

The theme's host gate (`inc/tags.php`) prints the GTM snippet only on the production hostname —
deliberately, so test submissions could never feed a real Ads conversion. On staging that meant
**no tags loaded during any Lighthouse run we did.** The moment the domain moved, the gate opened.

So the 98–99 was never the site's score with its own analytics attached. That should have been said
in week one, and was not.

## What the tags cost, measured

Live homepage, mobile Lighthouse:

Re-measured 7 Aug from the network log rather than the summary panel:

| | |
|---|---|
| — `gtag/js` (GA4 `G-3YMN51H7LE`) | **176.4 KiB** |
| — `gtm.js` (`GTM-MZ6RZ94` itself) | **158.8 KiB** |
| — `gtag/destination` (Ads `AW-1012143191`) | **155.3 KiB** |
| — Microsoft Clarity | 25.2 KiB |
| — Bing Ads UET | 15.5 KiB |
| **Total third-party tag load** | **531 KiB** |
| Whole page, tags included | 854 KiB |
| Whole page, tags blocked | **312 KiB** |
| Cognito Forms (`/get-a-quote/` only) | 379 KiB, 863 ms blocking |

PSI reports ~200 KiB of that as *unused* JavaScript on the homepage.

**Microsoft Clarity was a surprise** — session recording, not in the earlier tag inventory. Worth a
deliberate decision, on privacy grounds as much as weight.

## Two failed attempts at deferring the container

Recorded in full because the reasoning was plausible and wrong, and is easy to repeat.

### 1.5.1 — idle callback, 2,500 ms ceiling → mobile 54 → 66

Not enough. Lighthouse waits for network quiet, so a 2.5 s ceiling fires comfortably inside its
measurement window. The container still landed and still cost 491 KiB. Deferring had moved it later
without moving it out.

### 1.5.2 — interaction-only → **worse on three of four pages**

| mobile perf | 1.5.0 | 1.5.1 | 1.5.2 |
|---|---|---|---|
| home | 54 | 66 | **55** |
| get-a-quote | 62 | 59 | 73 |
| el-niño | 75 | 73 | **64** |
| video | 80 | 81 | **74** |
| PSI desktop | **82** | — | **72** |

Homepage TBT went **960 ms → 2,550 ms**.

**Why: Lighthouse scrolls the page itself** while gathering, to capture full-page screenshots and
trigger lazy content. That trips a `scroll` listener, so the container loads anyway — but it now
executes in the *middle of the trace* instead of before first paint, and mid-trace execution costs
more blocking time than early execution.

The only trigger set Lighthouse will not trip is `pointerdown` / `keydown` / `touchstart` with no
`scroll`. **Deliberately rejected.** A visitor who reads an article and scrolls but never taps would
record no pageview at all — that is most readers — and it games the metric rather than making the
page faster.

### Where it landed: 1.5.3 reverts to loading in the head

`CFI_TAGS_DEFER` defaults to `false`. The deferral code is kept, not deleted, because it may still
be right for **CrUX field metrics** — real visitors are not Lighthouse, and tags not competing with
the hero image is a genuine field-level gain. That cannot be judged until the new site has 28 days
of field data, so **revisit in early September**, with CrUX as the evidence rather than a lab score.

## Measurement method — two mistakes worth not repeating

**Warm the cache before measuring.** The 54 that started tonight's alarm was taken minutes after a
full cache purge and 26 page re-saves, so the homepage was an `x-proxy-cache: MISS` — a complete
WordPress render. Every run since has been a warm HIT. Same code, and the honest figure is **65**,
not 54. A cold-cache run overstates the problem by roughly ten points on this host.

**Run repeats before concluding anything.** Four consecutive local runs on identical code and page:

```
perf : 64, 67, 64, 68     spread 4 points    median 65.5
LCP  : 4.1, 3.8, 4.1, 3.9 s
TBT  : 746, 754, 752, 662 ms
```

So the harness is stable to about ±2 points — stable enough to trust a 10-point delta, not a
3-point one. Mid-session I claimed the opposite, that it swung ±10; that was wrong and was itself
the result of comparing single runs taken at different cache temperatures.

PSI reads lower than a local run (63 vs 65 mobile) because it throttles harder — Moto G Power on
Slow 4G against the local default. The two are consistent, not contradictory.

## The honest numbers

PSI, 6 Aug **21:22**, `www.californiafloodinsurance.com` — after the site icon fix:

| | Mobile | Desktop |
|---|---|---|
| Performance | ~61 | **88** |
| Accessibility | **100** | **100** |
| Best Practices | **100** | **100** |
| SEO | **100** | **100** |
| CLS (lab) | **0** | **0** |

Best Practices is **confirmed back at 100 by Google's own run**, from 96 — the site icon was the last
console error. Verified externally, not just in the local harness.

**Desktop has exactly one weakness left.** Point contribution at 21:22: FCP 9/10, **LCP 15/25**,
TBT **30/30**, CLS 25/25, SI 9/10. Blocking time is at full marks and rendering is fast; the whole
gap is a 2.1 s LCP — **which still has the `www.` redirect inside it.** An apex run should land in the
low 90s. That is a prediction, not a measurement, and it is the cheapest remaining test.

**Three consecutive PSI desktop runs settle the outlier question:** 87 (20:36) → 61 (21:09) →
88 (21:22), on effectively identical code. The 61 with 1,330 ms TBT was one bad sample, and treating
it as a JavaScript problem was wrong. Three local apex runs agreed: TBT median 64 ms.

### The score composition is the whole story

PSI publishes the per-metric point contribution, and it says something different from what
everything above this line assumed:

| Metric | Mobile | pts | Desktop | pts |
|---|---|---|---|---|
| FCP | 3.9 s | 3 / 10 | 1.0 s | 9 / 10 |
| **LCP** | **9.3 s** | **0 / 25** | 2.1 s | 15 / 25 |
| **TBT** | **160 ms** | **28 / 30** | 60 ms | **30 / 30** |
| CLS | 0 | 25 / 25 | 0 | 25 / 25 |
| SI | 6.1 s | 5 / 10 | 1.4 s | 9 / 10 |

**Total blocking time is effectively solved** — 28/30 mobile, full marks desktop. Every conclusion
earlier in this file that treats TBT as the problem is out of date, including the recommendation at
the bottom of the old "what is left" list. The entire remaining gap on both form factors is **LCP**,
and on mobile it scores a flat zero.

That matters because it changes the mechanism. TBT is main-thread execution; LCP at this TTFB is
**bandwidth**. Half a megabyte of third-party script does not have to block the main thread to hurt
— on Slow 4G it simply consumes the throughput the hero image needs. Which is also the retrospective
explanation for why 1.5.1 and 1.5.2 failed: both deferred *execution*. Neither deferred the
*download*.

## The controlled experiment — 7 Aug, and it settles the argument

Four Lighthouse runs, same night, same harness, caches warmed first, mobile. The only variable is
which hosts are allowed to load:

| Scenario | Perf | LCP | TBT | Transfer |
|---|---|---|---|---|
| `www.` + full tags — **what every PSI report used** | **48** | 5.5 s | 810 ms | 854 KiB |
| apex + full tags | **62** | 3.9 s | 920 ms | 854 KiB |
| apex + `gtm.js` only (GA4, Ads, Clarity, Bing blocked) | **82** | 3.9 s | 180 ms | 471 KiB |
| apex + no tags at all | **95** | 2.9 s | **0 ms** | **312 KiB** |

**The theme is a 95.** The tag stack costs 39 points and 542 KiB. Nothing in the pages is slow.

### Two separate findings in that table

**1. The `www.` redirect is worth ~18 points, and it was inside every measurement.**

The first version of this section said 411 ms and 14 points, from one run each. Both were wrong.
Re-measured with 5 interleaved TTFB samples and **5 interleaved Lighthouse runs per hostname**, all
post-1.5.4 so the theme is constant:

| | apex | `www.` |
|---|---|---|
| Perf, 5 runs | 68, 70, 71, 73, 77 | 48, 50, 53, 53, 56 |
| **Median** | **71** | **53** |
| Spread | 9 pts | 8 pts |
| LCP median | **2.7 s** | 4.5 s |
| TTFB median (unthrottled curl) | 0.478 s | 0.632 s |

**The distributions do not overlap**: apex's worst run (68) beats `www.`'s best (56). Across ten runs
the only variable was the hostname, so the 18-point gap is a real effect and not variance.

**But do not explain it with the TTFB number.** 154 ms unthrottled cannot account for 18 points or a
1.8 s LCP difference, and it should not be expected to — they measure the same cause at different
throttling levels. Under Lighthouse's simulated Slow 4G, `www.` and apex are **separate origins**, so
the redirect costs a fresh DNS + TCP + TLS handshake *and* a round trip before the critical chain
begins, after which the chain restarts. That compounds; the unthrottled TTFB delta does not.

**The variance floor is ±4–5 points per hostname** (spread 8–9 over 5 runs). Nothing smaller than
about a 10-point difference is interpretable from single runs. Two of my own conclusions tonight
violated that before this table existed.

Apex is the canonical hostname and that is correct — visitors arriving from search go straight there,
so **field data is unaffected**. But every lab number in this file taken against `www.` is
understated. **All future comparisons use `https://californiafloodinsurance.com/`.**

### Desktop is not the main-thread problem one bad sample made it look like

A PSI desktop run at 21:09 reported TBT **1,330 ms** with 14 long tasks, which read as a standing
JavaScript problem. It was not. Three local desktop runs on apex, same code:

| Desktop, apex | Perf | TBT median | Main-thread median |
|---|---|---|---|
| Baseline | 83, 83, 95 → **83** | **64 ms** | 0.64 s |
| Clarity blocked | 80, 87, 97 → 87 | 50 ms | 0.52 s |
| Clarity + Bing blocked | 79, 82, 82 → 82 | 48 ms | 0.51 s |

The 20:36 PSI run also showed 60 ms. So **1,330 ms was an outlier** and desktop on apex sits around
**83**. Note also that Clarity+Bing scored *lower* than Clarity alone — causally impossible, and a
plain demonstration that a 12–17 point spread at n=3 swamps the effect being measured.

What survives: main-thread work drops a consistent ~120 ms with Clarity blocked. Real, small, and
**not** a demonstrated score gain.

### The font change is not measurable, and that should be said plainly

1.5.4 took 50.7 KiB off the wire. Apex median before: **71**. Apex median after: **71**.

| | pre-1.5.4 (n=3) | post-1.5.4 (n=5) |
|---|---|---|
| apex median | 71 | **71** |
| apex LCP median | 3.4 s | 2.7 s |
| apex TBT median | 763 ms | 1,031 ms |

LCP moved the right way, TBT moved the wrong way, and both moves are inside the ±4–5 point noise
floor established above. **51 KiB less on the wire is real; a score improvement from it is not
demonstrated.** The change stays — it is strictly less data over the network with no rendering
difference — but it buys nothing that can be measured at this sample size, which is exactly what was
predicted when it shipped. Anyone re-reading this later should not count it as a win.

**2. Trimming the container is worth ~20 points**, from 62 to 82 — and it gets there by freeing
bandwidth, not main thread. `gtm.js` itself is 158 KiB; what it *pulls in* is the cost:

| | |
|---|---|
| `gtag/js` — GA4 `G-3YMN51H7LE` | 176 KiB |
| `gtag/destination` — Ads `AW-1012143191` | 155 KiB |
| Microsoft Clarity | 25 KiB |
| Bing UET | 15 KiB |

The 82 run is not a shippable configuration — it has no analytics and no conversion tracking. It is
the ceiling that container work is aiming at, and the gap between 62 and 82 is how much of it is
recoverable without giving up data.

## What Divi actually scored — the comparison that matters

The field data in any PSI report run this week is a **28-day rolling window**, so it is almost
entirely the *Divi* site. That makes it the baseline, and it is worth stating plainly because the
assumption in the room was that Divi scored better:

| Real users, 28 days (= Divi) | Mobile | Desktop |
|---|---|---|
| LCP | 3.3 s | 2.9 s |
| TTFB | 2.5 s | 2.1 s |
| CLS | 0.04 | **0.2** |
| **Core Web Vitals** | **Failed** | **Failed** |

**Divi was failing Core Web Vitals on both form factors**, with a desktop CLS of 0.2 against our lab
0. Google ranks on field data, not lab scores. So on the measure that counts, the new site is
replacing a failing one — and its own field data will not exist until roughly 4 September.

### Divi's lab score, since the recollection is that it was higher

It was measured during this project and written down twice — `CACHE-HEADERS.md` (twice) and
`TRUSTINDEX-SETUP.md`, all three against the live Divi California homepage with the same
`GTM-MZ6RZ94` container hand-placed in the Divi header:

| Live Divi, californiafloodinsurance.com | Mobile | Desktop |
|---|---|---|
| Performance | **58** | **79** |
| Mobile LCP | **12.6 s** | |

Against 61 / 87 today. The new site is ahead on both form factors and its mobile LCP is a third of
Divi's. The 90-and-96 figures that feel like the "before" number were **this theme on staging with
tagging switched off** — not Divi.

### But statewide, still on Divi, scored 60 tonight — worth understanding why

A live control was available: `statewidefloodinsurance.com` is still Divi, on the same server, same
host stack, same plugin load. Run alongside California on the same night:

| Mobile, 7 Aug | Statewide (Divi) | California (new) |
|---|---|---|
| Performance | **60** | 62 |
| LCP | **2.0 s** | 3.9 s |
| TBT | 1,430 ms | **920 ms** |
| CLS | **0.231** — fails | **0** |
| Transfer | **3,338 KiB** | **854 KiB** |

Divi is four times the weight, 55% more blocking time, and fails CLS outright — and still wins on
LCP. The reason is the container, not the theme: **`GTM-PJQ72VK` holds no Google tag** (it reports
GTM's "Missing Google tags" warning — the whole reason `CFI_GA4_ID` had to be set for statewide).
So statewide never loads the 176 KiB GA4 script or the 155 KiB Ads script. It is 3.3 MB of theme
bloat with a light tag load, against 312 KiB of clean theme with a heavy one.

Which is the same finding as the table above, arrived at from the other direction: **the variable is
the container, both times.** It is also a warning for statewide's own cutover — the moment it gets a
Google tag, it inherits this exact problem.

## 1.5.4 — the font instancing, and its honest size

Both webfonts are variable and both shipped with their **full factory weight axes**. The design uses
Source Serif at 600/640/700/800 and Inter at 400/500/600/620/650/700; everything outside those ranges
was outline data nothing renders.

| | Before | After |
|---|---|---|
| `sourceserif4.woff2` | 119.3 KiB | **80.8 KiB** |
| `inter.woff2` | 47.3 KiB | **35.1 KiB** |
| Total, both preloaded at high priority | 166.6 KiB | **115.9 KiB** |

**51 KiB off the critical path with no rendering change.** All 231/230 codepoints are retained and
Source Serif's `opsz` axis is deliberately **kept**, so the browser's default
`font-optical-sizing: auto` still adjusts stroke contrast by size.

Pinning `opsz` as well would have taken Source Serif to **32.7 KiB** — another 48 KiB — and was
declined: it would flatten the optical adaptation on the 84 px `.cfi-bignum` and the clamp(56,7vw,84)
display headings, which is exactly where a serif shows it. Available if the trade is ever wanted.

**Versioned filenames — `sourceserif4-v2.woff2`, `inter-v2.woff2`.** The first cut of 1.5.4
overwrote the files in place, which was wrong: a changed file at an unchanged URL never reaches a
browser that already holds the old one. New visitors and Lighthouse would have got the fix while
existing visitors kept the old bytes — and the narrowed `font-weight` range in the CSS would then
have described a file they did not have. New bytes now always mean a new filename, and the reasoning
is written into `tokens.css` and `functions.php` so it does not get undone.

**While fixing that, the cache header we had documented turned out not to be real.** Measured on the
live site:

| Asset | Served `Cache-Control` |
|---|---|
| `hero-poster.webp` | `public, max-age=31536000, immutable` — as designed |
| `inter-v2.woff2` | `max-age=604800` **and** `public, must-revalidate` |
| `tokens.css` | `max-age=604800` **and** `public, must-revalidate` |

`x-proxy-cache: STATIC/TYPE` is the explanation: **nginx serves fonts and CSS itself and never hands
them to Apache**, so the `mod_headers` rule in `inc/htaccess.php` only ever applied to the image
types. Two consequences:

1. `CACHE-HEADERS.md` records a 1-year immutable header on `woff2`. That is true for webp and **false
   for woff2 and css**. Corrected there.
2. The stranding window for an in-place font overwrite was therefore **7 days with revalidation**,
   not a year. Smaller than feared — but the versioned filename is still the right fix, because it
   makes deployment deterministic instead of dependent on host behaviour we had mis-recorded.

Two conflicting `Cache-Control` headers on one response is also a defect in its own right. Worth an
InMotion ticket: the theme cannot fix it from `.htaccess` because Apache is not in the path.

**Do not oversell this.** 51 KiB against a 542 KiB tag stack is worth a point or two, not ten. It is
in this file because it is real, measured, and the last thing in the theme worth doing — not because
it closes the gap.

## What is actually left, in order of value

Re-ordered 7 Aug against the measured ladder rather than against a guess.

1. **Trim `GTM-MZ6RZ94` — but far less than first thought.** → **`GTM-AUDIT.md`** holds the full
   read-only audit and its retraction. The audit found no `__awct` conversion tags and inferred the
   155 KiB Ads script was removable. **Checked in the Ads UI: `AW-1012143191` carries an active
   Primary Website conversion with Enhanced Conversions, so tag 10 must stay.** Recoverable weight
   falls from ~250 KiB to **~95–115 KiB**, or about 12% of the page — expect **single-digit**
   movement, not a jump to the 80s. What remains: Clarity (~28 KiB), container pruning (15–35 KiB),
   and the fonts already shipped.
2. **Decide about Microsoft Clarity — and note it is not where anyone thought it was.** Clarity is
   loaded *by Bing UET*, keyed to UET tag `5318858`, because the integration is enabled in the
   Microsoft Advertising account. It is in neither GTM nor WordPress; verified in all three. So it is
   switched off in the Microsoft Ads UI. ~28 KiB and three extra origins. Bing UET itself carries
   $12,607/mo of spend and is not optional.
3. **Test the apex URL, not `www`.** Worth ~20 lab points and it costs nothing — a measurement
   correction, not an optimisation. `https://californiafloodinsurance.com/`.
4. **Set the site icon.** `/favicon.ico` 404s, `site_icon` is `0`, zero icon tags in the served head
   (re-verified 7 Aug). Not a performance item at all — Google shows a favicon beside every mobile
   search result. `assets/media/cfi-site-icon-512.png` is in the theme; Appearance → Customize →
   Site Identity.
5. **Revisit deferral in September** against CrUX, not against Lighthouse — and revisit it knowing
   the mechanism is download, not execution. A deferral that does not delay the *fetch* cannot help.

Nothing on this list is a theme change. That is the conclusion: the theme measures 95 with the tags
blocked, and the pages are not what is slow.

## The site icon, and one host behaviour behind three separate bugs

**Done 7 Aug.** Site Icon published; `<link rel="icon">` at 32/192, `apple-touch-icon` 180, and
`msapplication-TileImage` 270 all render. Verified after: **`errors-in-console` scores 1 with zero
errors, and no 4xx request anywhere in the page.** Best Practices returns to 100.

Two notes worth keeping.

**`/favicon.ico` still 404s on a direct request, and that is fine.** WordPress's favicon handler only
runs when a request reaches WordPress; nginx answers `/favicon.ico` itself and 404s before PHP is
involved. It does not matter, because a browser only falls back to `/favicon.ico` when no icon `<link>`
is present — confirmed by measurement: **Chrome did not request it at all.** If a crawler that ignores
icon tags ever matters, the fix is a physical `favicon.ico` in the docroot, not a WordPress setting.

**That is the third bug tonight with the same root cause.** Worth stating as a rule for this host:

| Symptom | Same underlying cause |
|---|---|
| Fonts and CSS served `max-age=604800` instead of the theme's 1-year immutable | nginx serves them; Apache `mod_headers` never runs |
| Nginx Helper's purge returning 403 (found earlier in the project) | `proxy_cache`, not `fastcgi_cache` |
| `/favicon.ico` 404 despite `site_icon` being set | nginx answers it; WordPress never sees the request |

**On this UltraStack stack, anything WordPress or `.htaccess` tries to do to a static path may simply
not happen.** Verify at the wire with `curl -I`, never from the WordPress side. Three separate hours
were lost tonight to variations of this.

**An unexplained detail, recorded rather than guessed at:** the REST index at `/wp-json/` still reports
`site_icon: 0` and an empty `site_icon_url` on an uncached (`x-proxy-cache: MISS`) response, while the
rendered page carries all four icon tags. The rendered output is authoritative and correct. I did not
chase the discrepancy and do not have a confirmed explanation for it.

## 1.5.6 — the hidden video poster, and a baseline I contaminated myself

**The fix is real and verified.** The hero `<video>` carried `poster="hero-poster.jpg"` — 50,002 bytes
fetched on every load, on every form factor, for an image nobody ever saw: `preload="none"` does not
cover a poster, the element is `display:none` below 721px, and the `<picture>` resolves to the WebP
everywhere that matters. Found by Aaron from a live trace; it had been sitting unexamined in my own
network log as "49.1 KiB Image" for hours.

Verified three ways after deploy, on the anonymous non-cache-busted path:

| Scenario | WebP | MP4 | JPEG |
|---|---|---|---|
| Mobile | 34 KB | none | **none** |
| Desktop, normal motion | 34 KB | 152 KB (206) | **none** |
| Desktop, reduced motion | 34 KB | none | **none** |

**But the score comparison is worthless, and the reason is my own 1.5.4 bug.** The only five-run apex
baseline I had was taken *inside the font-404 window*:

| | before (n=5) | after (n=5) |
|---|---|---|
| `sourceserif4` | **404** | 200 — 81.1 KiB |
| `inter` | **404** | 200 — 35.4 KiB |
| `hero-poster.jpg` | 49.1 KiB | **absent** |
| `/favicon.ico` | 404 | absent (icon set) |
| transfer | 687 KiB | 757 KiB |
| **perf median** | **71** | **70** |

The baseline page was rendering in Georgia and Arial with 116 KiB of webfonts never downloaded.
+116.5 fonts − 49.1 JPEG + 2.6 icon = **+70 KiB**, matching the observed delta exactly. Three
variables moved between the two measurements; only one of them was 1.5.6.

**So 1.5.6's effect on score is unmeasured and will stay that way.** A clean baseline would mean
re-breaking the fonts. The bytes are gone and that is sufficient justification; no score claim is
made.

### The accident did produce one useful number

The page absorbed **+70 KiB net for roughly 1 point** (71 → 70, inside an 8–9 point spread). If that
ratio held, the ~43–63 KiB still available from container cleanup would be worth **under a point**.

It also shows the byte theory is incomplete. Blocking the whole tag stack removed 531 KiB and gained
**24 points** (71 → 95) — far more than 531/70 ≈ 7.6 points would predict. So the tags cost more than
their bytes: connection setup to four extra origins, and main-thread execution. Byte-count alone is
not the model, and anyone reasoning from KiB → points on this page will be wrong in both directions.

## The decisive experiment — 8 Aug, and it names the cause

A local harness at `--throttling.cpuSlowdownMultiplier=8` reproduces PSI almost exactly (60 against
PSI's 61), which finally makes lab work here comparable to what Google reports. Three runs each, apex,
**identical CSS, identical fonts, identical images** — the only variable is whether the tag scripts
are allowed to load:

| 8x CPU, n=3 | Perf | LCP | TBT |
|---|---|---|---|
| Tags live | **60** | 3,299 ms | **1,702 ms** |
| Tags blocked | **92** | **2,430 ms** | **287 ms** |

### What this rules out

**The five render-blocking Kadence stylesheets are not the bottleneck.** They are present, unchanged,
in the run that scores 92. Consolidating them cannot be worth much.

**Font-dependent paint is not the bottleneck either.** Both fonts load normally in both runs.

One measurement disposes of both hypotheses. Neither had been eliminated before, and both were
plausible enough to have cost a day.

**The blocked-tags LCP is 2,430 ms across three runs with zero variance** — which is the page's floor.
An LCP breakdown circulating separately summed to 2,450 ms; that is within 20 ms of this floor, and
supports the reading that it came from a run where the tags barely landed rather than describing the
9.0 s headline.

### What it confirms

**Main-thread contention from tag execution.** TBT 1,702 ms -> 287 ms with nothing else changed.

### Two of my own claims this corrects

**"The container hurts through bandwidth."** Wrong mechanism. It is execution. Same conclusion about
what to do, but it matters, because byte-shaving cannot fix execution — and most of this file's
earlier reasoning was byte-based. The +70 KiB / -1 point measurement recorded above is the clue I had
already collected and misread: 531 KiB of tags cost 24 points where 70 KiB cost 1, because payload
was never the dominant term.

**"Pruning the 11 dead tags will not move TBT."** Right about the timers *firing* — a Lighthouse run
ends before a one-minute timer does — but wrong about *initialisation*. Eighteen listener
registrations and 33 predicates evaluated on every dataLayer push are startup work, and startup is
exactly where the damage is. Pruning may cut TBT measurably. **Untested**, and now testable on the 8x
harness once the container is pruned.

### The uncomfortable implication

At PSI-equivalent throttling the page scores **92 with the tags not executing** and **60 with them
executing**. Mobile therefore stays in the 60s while the full stack loads during page load. The only
lever that reaches 90 is not loading the tags during initial page load — which was offered and
declined, deliberately and for good reasons about data completeness. **Recording that as a decision
taken, not an oversight.** Everything else measured tonight moves single digits at best.

## The settled answer — interleaved, n=5 each, 8 Aug

This supersedes every partial conclusion above it. Five interleaved pairs (live, blocked, live,
blocked...) on the apex URL, identical CSS, fonts, images, cache state, viewport and Lighthouse
settings. The only variable is whether `googletagmanager.com` may load.

| Median | Tags live | GTM blocked | delta |
|---|---|---|---|
| **Score** | **66** | **97** | **+31** |
| FCP | 2,361 ms | 1,379 ms | -982 |
| LCP (simulated, scored) | 3,345 ms | 2,430 ms | -915 |
| **TBT** | **900 ms** | **0 ms** | **-900** |
| Speed Index | 3,447 ms | 2,279 ms | -1,168 |
| observed **load delay** | **20 ms** | **19 ms** | **-1** |
| observed render delay | 161 ms | 194 ms | +33 |

### Three findings

**1. Execution is the mechanism. Confirmed, not inferred.** TBT falls from 900 ms to **exactly zero**.
Every millisecond of blocking time on this page comes from GTM's subtree. Load delay does not move at
all, so request scheduling is not affected — the tags do not get in front of the hero image, they
occupy the main thread.

**2. GTM is also the entire source of run-to-run variance.**

```
blocked : 96, 97, 97, 97, 97     spread 1
live    : 53, 66, 66, 68, 74     spread 21
```

The page is stable to about half a point. The +/-10 variance this file spent all night working around
is injected by the tag stack, not by the harness or the host. Any future A/B on this page should block
GTM to get a usable signal, then unblock to get the real score.

**3. There is no hero-delivery problem, and a "3.7 s load delay" reading is a harness artifact.**

A separate five-run baseline reported load delay as the dominant LCP phase at ~3,658 ms median. That
does not survive contact with the observed trace. Every one of the eight diagnostics comes back clean:

| Check | Result |
|---|---|
| Preload URL vs LCP request URL | **byte-for-byte identical** |
| Hero WebP requests | **exactly 1** — no double download |
| Priority | **High** |
| Request start | 799 ms, against a TTFB of 784 ms — **15 ms later** |
| Request end | 1,050 ms — **251 ms of transfer** |
| Unused-preload warning | none |
| Navigation final URL | apex, **no `www` redirect paid** |
| Redirects in run | 2, both third-party (Clarity + Bing beacons) |

**Observed load delay is 20 ms with tags and 19 ms without.** The confusion comes from mixing two
different clocks: `lcp-breakdown-insight` reports **observed** trace timings, which sum to ~1,195 ms,
while the **scored** LCP is Lantern-simulated at ~3,298 ms. A harness that spreads that ~2,100 ms of
simulator scaling across the four phases will make load delay look like the whale. It is not.

**Rule for future work on this page: never mix observed phases with a simulated metric.** State which
clock a number came from, or the diagnosis will point at the wrong subsystem — as it did here, at a
preload that is working perfectly.

## Things deliberately not done

**No click-to-load facade on the Cognito form.** It is 379 KiB and 863 ms, and it is the largest
single cost on `/get-a-quote/`. But the form's first field sits **398 px** down a 844 px mobile
viewport — above the fold, the first thing a visitor sees on the page carrying the ad spend.
Delaying it trades conversions for a score. Measured, then rejected.

**No hiding tags from Lighthouse.** See 1.5.2 above.
