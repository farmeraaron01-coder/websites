# Performance — what the numbers actually are, and why

Written 7 Aug 2026, the night California went live. It exists because the scores we quoted for two
weeks were measured with tagging switched off, and because two attempts to recover them made things
worse. Both belong on the record.

---

## The headline correction

**Staging measured 98–99 mobile. The live site measures 60.** Nothing about the pages changed.

The theme's host gate (`inc/tags.php`) prints the GTM snippet only on the production hostname —
deliberately, so test submissions could never feed a real Ads conversion. On staging that meant
**no tags loaded during any Lighthouse run we did.** The moment the domain moved, the gate opened.

So the 98–99 was never the site's score with its own analytics attached. That should have been said
in week one, and was not.

## What the tags cost, measured

Live homepage, mobile Lighthouse:

| | |
|---|---|
| Google Tag Manager | **490 KiB**, ~198 KiB of it unused |
| — `gtm.js` | 158 KiB |
| — `gtag/js` (GA4 `G-3YMN51H7LE`) | 176 KiB |
| — `gtag/destination` (Ads `AW-1012143191`) | 155 KiB |
| Microsoft Clarity | 28 KiB |
| Bing Ads UET | 18 KiB |
| Cognito Forms (`/get-a-quote/` only) | 379 KiB, 863 ms blocking |

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

## The honest numbers

| | Mobile | Desktop |
|---|---|---|
| Performance | **60** | **82** |
| Accessibility | **100** | **100** |
| Best Practices | **100** | **100** |
| SEO | **100** | **100** |
| CLS (lab) | **0** | **0** |

The three 100s are the hard ones and they hold on every run.

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

## What is actually left, in order of value

1. **Trim `GTM-MZ6RZ94`.** 490 KiB against ~100 KiB for a lean container, ~198 KiB unused. This is
   the only change that improves lab *and* field together, loses no data, and needs no cleverness in
   the theme. `ACCOUNTS.md` already lists the dead tags — eight of fourteen Ads tags carry zero
   goals. **Nothing in the code beats this.**
2. **Decide about Microsoft Clarity.** 28 KiB and it records sessions.
3. **Set the site icon.** `/favicon.ico` 404s, `site_icon` is `0`, zero icon tags. Google shows a
   favicon beside every mobile search result. `assets/media/cfi-site-icon-512.png` is in the theme;
   upload it at Appearance → Customize → Site Identity.
4. **Test the bare domain, not `www`.** Every PSI run this week used
   `www.californiafloodinsurance.com`, which 301s. That redirect sits inside the measurement and on
   Slow 4G a round trip is not free.
5. **Revisit deferral in September** against CrUX, not against Lighthouse.

## Things deliberately not done

**No click-to-load facade on the Cognito form.** It is 379 KiB and 863 ms, and it is the largest
single cost on `/get-a-quote/`. But the form's first field sits **398 px** down a 844 px mobile
viewport — above the fold, the first thing a visitor sees on the page carrying the ad spend.
Delaying it trades conversions for a score. Measured, then rejected.

**No hiding tags from Lighthouse.** See 1.5.2 above.
