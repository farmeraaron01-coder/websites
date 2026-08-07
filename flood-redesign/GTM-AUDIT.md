# `GTM-MZ6RZ94` — read-only container audit

Written 7 Aug 2026. **Nothing was changed.** The published container definition is embedded in
`gtm.js` itself, so this was produced by fetching and parsing that file — no GTM access, no writes,
no risk to anything live.

Container **version 9**: **39 tags, 22 triggers, 33 conditions, 29 variables.**

---

> # RETRACTION, same night — tag 10 must NOT be removed
>
> **The largest recommendation in the first version of this document was wrong. It has been removed.**
>
> This audit found no `__awct` tags in the container and concluded from that absence that the 155 KiB
> `gtag/destination?id=AW-1012143191` was carrying remarketing only, and was therefore removable.
>
> **Checked in the Google Ads UI: `AW-1012143191` has an active Primary Website conversion action with
> Enhanced Conversions.** That conversion is measured through the Ads destination this tag loads.
> Removing tag 10 would stop a Primary conversion and cut Smart Bidding's signal — on an account
> spending ~$24,771/mo. Not a degradation. A break.
>
> **The reasoning error is worth naming**, because it is the kind that survives being technically
> correct: "no `__awct` tag exists" is true, and "therefore no conversion depends on the Ads
> destination" does not follow. A Website conversion action can be measured through the Google
> Ads destination loaded by *any* gtag-family tag, `__sp` included. Absence of a conversion *tag* is
> not absence of conversion *measurement*. The container alone could never have answered this — only
> the Ads UI could, which is why Step 1 was written as a gate. **The gate worked and it caught this.**
>
> Consequence for the numbers: realistic savings drop from ~250–270 KiB to **~95–115 KiB**, and the
> "mid 80s mobile" extrapolation goes with it. Corrected throughout below.
>
> Tag 10 now sits in category C — **do not touch** — alongside the Google tag and Conversion Linker.

---

## Desktop and mobile have different bottlenecks — do not treat them as one problem

Established 7 Aug from PSI on the live site. This matters for choosing what to cut:

| | Mobile | Desktop |
|---|---|---|
| Bottleneck | **LCP** (0/25 and 2/25 across two runs) | **TBT / main-thread JS** |
| FCP | 3.9–4.1 s | **0.4 s** |
| LCP | 6.9–9.3 s | **1.9 s** |
| TBT | 160–310 ms | **1,330 ms** |
| CLS (lab) | 0 | 0 |
| Main-thread work | — | 2.7 s, JS execution 1.5 s, **14 long tasks** |

**Desktop rendering is already excellent** — 0.4 s FCP, 1.9 s LCP, zero CLS. Its score is almost
entirely third-party JavaScript execution. **Mobile is the opposite**: blocking time is nearly fine
and LCP is starved of bandwidth.

So the two form factors want different things from this container. Mobile wants **fewer bytes**.
Desktop wants **less code executing at startup**. Clarity is the only safe removal that helps both,
and it helps desktop out of proportion to its 25 KiB because session recording instruments the DOM.

**A correction to this document's own earlier reasoning:** the 1/2/5-minute timer tags were listed as
main-thread contributors. They are not, for a Lighthouse run — **the run finishes long before a
one-minute timer fires.** Registering the listeners at init is nearly free. Removing them is still
right (they duplicate GA4 native measurement and add container weight), but **it will not move TBT**
and should not be sold as if it would.

Read `PERFORMANCE.md` first for why this matters. Short version: the theme measures **95** on mobile
with the tag scripts blocked and **~62–71** with them, so the container is where the remaining
performance is. This document is about doing that safely.

---

## The container in six categories

The detail is in the numbered sections below. This is the classification, because the single most
common mistake in this kind of cleanup is treating all six as one list.

### A. Direct GTM tags — configured in this container, visible in the UI

39 of them. Only these can be edited or deleted in GTM.

| | Count | Tag IDs |
|---|---|---|
| GA4 event | 13 | 21, 23, 25, 27, 31, 32, 34, 36, 38, 40, 42, 56, 57 |
| Event listeners (click / link / form / timer / scroll) | 18 | 58–75 |
| Custom HTML | 4 | 14 (UET base), 43 (UET event), 45 (Cognito prefill), 49 (internal cookie) |
| Google tag | 1 | 13 |
| Ads remarketing | 1 | 10 |
| Conversion Linker | 2 | 11, 19 |

### B. Scripts loaded automatically by vendor tags — **not configurable in GTM at all**

This is the category that had been missed entirely, and it is why "delete the Clarity tag" was never
going to work.

| Script | Size | Loaded by | Where it is actually controlled |
|---|---|---|---|
| `gtag/js?id=G-3YMN51H7LE` | 176.4 KiB | tag 13 (Google tag) | GTM tag 13 |
| `gtag/destination?id=AW-1012143191` | 155.3 KiB | tag 10 (Ads remarketing) | GTM tag 10 |
| `bat.bing.com/p/action/5318858.js` | 1.8 KiB | `bat.js` | Microsoft Advertising |
| `clarity.ms/tag/uet/5318858?insights=1` | 1.3 KiB | `action/5318858.js` | **Microsoft Advertising — UET/Clarity setting** |
| `scripts.clarity.ms/0.8.69/clarity.js` | **25.2 KiB** | the UET Clarity tag | **Microsoft Advertising** |
| `c.clarity.ms/c.gif`, `b.clarity.ms/collect`, `c.bing.com/c.gif` | ~2.0 KiB | clarity.js | **Microsoft Advertising** |
| `www.google.com/ccm/collect` ×2 | ~0.3 KiB | gtag | consent/conversion measurement |

**Nothing in GTM or WordPress can remove the Clarity subtree.** Confirmed absent from the container
JSON, the served HTML, and the WordPress side. Only the Microsoft Advertising UET/Clarity setting
switches it off — and only after confirming nobody is relying on the session recordings.

### C. Required for bidding or conversion attribution — do not touch

| Tag | Role |
|---|---|
| **13** Google tag `G-3YMN51H7LE` | Every GA4 hit. If conversions are GA4-imported (see §1), Smart Bidding's entire signal runs through this. |
| **11** Conversion Linker | Reads `gclid`/`wbraid` into `_gcl_*`. Without it Ads cannot join click to conversion. |
| **56** `quote_form_lead` | The lead conversion itself. |
| **57** `form_submit_any` | Denominator for completion rate. |
| **45** Cognito prefill | Writes UTM / `gclid` / `msclkid` into the form. Removing it breaks lead-source attribution in the CRM — not in Ads, but in the place the office actually reads. |
| **14 / 43** Bing UET base + `request_quote` | $12,607/mo of Microsoft spend depends on these. |
| **10** Ads remarketing `AW-1012143191` | **Moved here from category D after verification.** Loads the Ads destination that carries an active **Primary Website conversion with Enhanced Conversions**. Removing it breaks that conversion and Smart Bidding. |

### D. Diagnostic only — no bidding or conversion dependency

*(Tag 10 was here in the first draft. It is now in category C — see the retraction. It does build audiences,
but it also carries a Primary conversion, so its byte cost is not recoverable.)*

| Item | Size | Function |
|---|---|---|
| Clarity *(category B)* | ~28 KiB | Session recording and heatmaps. Diagnostic only. |
| **36** + listener **72** | — | Scroll depth |
| **38, 40, 42** + listeners **73–75** | — | Time on page at 1 / 2 / 5 min |

### E. Duplicates

| What | Detail | Cost |
|---|---|---|
| **Conversion Linker ×2** | Tag 11 (All Pages, correct) and tag 19 (clicks + form submits, pointless) | No bytes; redundant work per click |
| **Triple form event** | Tags 27 *(click-based, Divi-era)*, 56 and 57 *(dataLayer-based, new theme)* can all fire on one quote submission | **No bytes — but duplicate conversion signal if more than one is a key event imported to Ads** |
| **GA4 page_view** | **No duplicate.** One `__googtag`, and the theme's `CFI_GA4_ID` is deliberately empty for California. Verified: exactly one `gtag/js` request in the served page. | — |
| **Bing UET base** | **No duplicate.** One base (14), one event (43). | — |
| Scroll / engagement events | Duplicate GA4 **native** Enhanced Measurement, not each other | — |

### F. Potential savings, each with its measurement risk

| Action | Saving | Confidence | Measurement risk |
|---|---|---|---|
| Disable Clarity *(Microsoft Ads UI)* | **~28 KiB** + 3 origins | Measured | **None.** Not a bidding or conversion source. Loses session recordings. |
| ~~Remove tag 10~~ | ~~155.3 KiB~~ | **RETRACTED** | **Breaks an active Primary Website conversion with Enhanced Conversions.** Not available at any price. |
| Delete tag 19 (duplicate linker) | ~0 | Measured | None. |
| Prune 8 engagement + 3 orphaned tags | 15–35 KiB | **Estimated** — needs a publish to measure | None. Verify the 3 orphans in Preview first. **Will not move TBT** — the timers never fire inside a Lighthouse run. |
| Fonts (**shipped, theme 1.5.4**) | **50.7 KiB** | Measured | None. |
| Fix the triple form event | 0 KiB | — | **This one reduces risk.** But reported conversions will *drop*. Not a regression — note the date. |

Sum after the retraction: **~95–115 KiB of 854** — Clarity ~28, container pruning 15–35, fonts 50.7.
That is roughly 12% of page weight, so **expect single-digit movement on mobile, not a jump to the 80s.**
Desktop may do better than that ratio suggests, because Clarity's cost there is execution rather than
bytes.

## 1. The tag-type census — and the inference I drew from it, which was wrong

**There are no Google Ads conversion tags in this container.** Not one `__awct`. That part is a fact;
I checked all 39 tags by function type:

| Type | Count | What it is |
|---|---|---|
| `__gaawe` | 13 | GA4 event |
| `__lcl` | 7 | listener: link clicks |
| `__cl` | 4 | listener: all clicks |
| `__html` | 4 | custom HTML |
| `__fsl` | 3 | listener: form submit |
| `__tl` | 3 | listener: timer |
| `__gclidw` | 2 | Conversion Linker |
| `__sp` | 1 | **Google Ads remarketing** |
| `__googtag` | 1 | **Google tag (GA4)** |
| `__sdl` | 1 | listener: scroll depth |
| **`__awct`** | **0** | **Ads conversion tracking — absent** |

**From that absence I inferred that Ads conversions must be GA4-imported and the 155 KiB Ads script
was therefore carrying remarketing only. That inference was wrong** — see the retraction at the top.
`AW-1012143191` has an active **Primary Website conversion with Enhanced Conversions**, measured
through the Ads destination that tag 10 loads.

The census stays because it is still useful — it is how you know there are only three
byte-bearing tags. But it establishes what is *in the container*, and conversion configuration lives
in the **Ads account**. A container audit cannot settle it. The check below is the one that can.

> **Confirm this before acting on it.** In Google Ads → Goals → Conversions, check the *source*
> column of each active conversion action. If it reads "Google Analytics 4 (property)", the finding
> holds. If any active conversion reads "Website" with a Google tag source, stop and re-plan — that
> would mean conversions ride the tag this document proposes removing.

---

## 2. Every tag that downloads an external script

Only **three** of the 39 tags cause a third-party download. Everything else is either a listener or
an event that piggybacks on a script already loaded.

| Tag ID | Type | Trigger | Downloads | Size |
|---|---|---|---|---|
| **13** | Google tag `G-3YMN51H7LE` | All Pages (`gtm.js`) | `gtag/js` | **176.4 KiB** |
| **10** | Ads remarketing `AW-1012143191` | All Pages (`gtm.js`) | `gtag/destination` | **155.3 KiB** |
| **14** | custom HTML — Bing UET `ti:5318858` | All Pages (`gtm.js`) | `bat.bing.com/bat.js` | **15.5 KiB** |
| — | the container itself | — | `gtm.js` | **158.8 KiB** |

Plus what tag 14 pulls in behind it, which is the part nobody had accounted for:

```
bat.bing.com/bat.js                      15.5 KiB
 └─ bat.bing.com/p/action/5318858.js      1.8 KiB
     └─ www.clarity.ms/tag/uet/5318858    1.3 KiB
         └─ scripts.clarity.ms/clarity.js 25.2 KiB
             └─ c.clarity.ms/c.gif, b.clarity.ms/collect, c.bing.com/c.gif  ~2.0 KiB
                                          ─────────
                                          ~45.8 KiB across SIX new origins
```

**This is where Microsoft Clarity comes from, and it explains the mystery in `PERFORMANCE.md`.**
Clarity is not in this container, not in the WordPress database, and not in the page HTML — I checked
all three. It is loaded *by UET*, keyed to the UET tag ID, because Clarity integration is switched on
in the Microsoft Advertising account. The URL says so itself: `clarity.ms/tag/uet/5318858`.

**Therefore: Clarity is disabled in the Microsoft Advertising UI, not in GTM and not in WordPress.**
Every previous plan to "remove the Clarity tag" was looking in the wrong place.

Six extra origins matters as much as the bytes. On Slow 4G each new host costs a DNS lookup and a TLS
handshake before a single byte arrives.

---

## 3. Duplicate and redundant loading

**Duplicate Conversion Linker — tags 11 and 19.** Tag 11 fires on All Pages, which is correct and
sufficient: Conversion Linker's job is to read `gclid`/`wbraid` off the landing URL and write the
`_gcl_*` cookies, which only needs to happen once per page. Tag 19 fires again on link clicks, all
clicks, and form submits. **Tag 19 is redundant.** It costs no download, but it is a small amount of
work on every click and it is a thing that can go wrong.

**No duplicate GA4 configuration — this is good and worth stating.** One `__googtag` (tag 13) with
`G-3YMN51H7LE`, and the theme's own `CFI_GA4_ID` is deliberately **empty** for California precisely to
avoid a second config. Verified in the served HTML: exactly one `gtag/js` request. The double-counting
failure mode documented in `inc/tags.php` did not happen.

**No duplicate Bing UET base.** One base tag (14), one event push (43).

**Possible duplicate *conversion counting* — this is the real risk, and it is not a performance
issue.** Four tags respond to a quote submission, and they use two different mechanisms:

| Tag | Event name | Fires on |
|---|---|---|
| 27 | `Submit_Online_Quote_Form_Submission` | `gtm.click` where element text contains "Submit Application" |
| 43 | Bing UET `request_quote` | the same click condition |
| 56 | `quote_form_lead` | `cfi_form_submit` dataLayer push **and** `cfi_is_lead = true` |
| 57 | `form_submit_any` | `cfi_form_submit` dataLayer push |

Tags 56 and 57 come from the new theme's own `cfi_form_submit` push (`inc/cognito.php`). Tag 27 is the
old click-based method inherited from the Divi site. **A single quote submission can therefore produce
three GA4 events.** That is harmless in reporting but serious if more than one is marked a key event
*and* imported into Ads as a conversion — it would inflate conversion counts and feed Smart Bidding
duplicate signal.

> **Check this regardless of any performance work.** GA4 → Admin → Events → Key events. If both
> `quote_form_lead` and `Submit_Online_Quote_Form_Submission` are key events and both are imported to
> Ads, conversions are being counted twice.

---

## 4. Essential vs removable

### Essential — do not touch

| Tag | Why |
|---|---|
| **13** Google tag `G-3YMN51H7LE` | All GA4 measurement. If conversions are GA4-imported, Smart Bidding depends on this tag. |
| **11** Conversion Linker | Attribution. Without it `gclid` never reaches the cookie and Ads loses click-to-conversion joining. |
| **56** `quote_form_lead` | The lead conversion. |
| **57** `form_submit_any` | Denominator for form completion rate. |
| **21, 31** Phone / Email clicks | Real intent signals on an agency site. |
| **45** Cognito prefill | First-party, no download, and it is what stamps UTM/`gclid`/`msclkid` into the form so leads can be attributed in the CRM. Removing it breaks lead-source reporting. |
| **14, 43** Bing UET base + `request_quote` | Carrying $12,607/mo of Microsoft Ads spend. Not optional. |

### Removable with a real but bounded cost

| Tag | Bytes saved | What is actually lost |
|---|---|---|
| **10** Ads remarketing | **155.3 KiB** | Remarketing/RLSA audiences built by the on-page tag. **Recoverable** — GA4 audiences can be shared to Ads through the GA4↔Ads link with personalised advertising enabled, which serves the same purpose without a second 155 KiB script. Requires the link to be configured and audiences rebuilt there. |
| Clarity *(via Microsoft Ads, not GTM)* | **~28 KiB + 3 origins** | Session recordings and heatmaps. A privacy call as much as a performance one — it records visitor sessions on a page that collects personal information. |
| **19** duplicate Conversion Linker | ~0 | Nothing. It is redundant. |

### Removable with no cost worth naming

| Tags | What they do | Why they can go |
|---|---|---|
| **36** + listener **72** | Scroll Depth event | GA4 Enhanced Measurement already records `scroll` natively at 90% depth. This is a second, worse copy. |
| **38, 40, 42** + listeners **73, 74, 75** | Time Tracking 1 / 2 / 5 min | GA4 measures `engagement_time_msec` on every event natively. These three timers run on every pageview to produce a metric GA4 already has. |
| **23, 25, 34** | Button-click events on "INSTANT ONLINE QUOTE!", "Get Quote Now!", "See More Reviews!" | These match **button text from the Divi site**. The new theme's buttons do not carry those strings, so these tags almost certainly no longer fire at all. Verify in GTM Preview before deleting — but if they are dead, they are dead weight in `gtm.js` and in seven link-click listeners. |

That last row is the interesting one: **8 of the 39 tags are engagement duplicates and 3 more look
orphaned by the theme change.** Eleven tags of 39, and each one contributes to the 158.8 KiB `gtm.js`
and to the 18 listener tags competing for the main thread.

---

## 5. Estimated byte savings — and the honest uncertainty

| Action | Saving | Confidence |
|---|---|---|
| ~~Remove tag 10 (Ads remarketing)~~ | ~~155.3 KiB~~ | **RETRACTED — carries a Primary conversion. Not available.** |
| Disable Clarity in Microsoft Ads | **~28 KiB** | **Measured** — clarity.js 25.2 + tag 1.3 + beacons |
| Prune 11 dead/duplicate tags + 8 listeners | **15–35 KiB** | **Estimated.** `gtm.js` is 158.8 KiB for 39 tags. It cannot be measured without publishing a container version, so treat the range as a range. |
| Fonts (**shipped, theme 1.5.4/1.5.5**) | **50.7 KiB** | Measured — but **no score benefit demonstrated**, see `PERFORMANCE.md` |
| **Total** | **~95–115 KiB** of 854 KiB | |

Landing around **740–760 KiB**, from 854. That is ~12% of page weight.

### Will that reach 90 on mobile?

**No.** Reference points, all measured on the apex URL:

| Page total | Mobile perf |
|---|---|
| 854 KiB (today) | 68–77, median **71** |
| ~750 KiB (after everything still available) | **mid 70s — extrapolated, single digits of movement** |
| 471 KiB (`gtm.js` only — *not shippable*, drops GA4 and Ads) | 82 |
| 312 KiB (no tags at all — *not shippable*) | 95 |

With tag 10 off the table, the recoverable weight is ~12% of the page, so **expect single-digit
movement, and remember the run-to-run spread is ±4–5 points.** The honest statement is that this
container cannot be cleaned into a 90 on mobile while carrying GA4, an Ads Primary conversion with
Enhanced Conversions, and Bing UET. Anything beyond the mid 70s needs a different approach —
server-side tagging, or a deliberate decision to measure less.

**Desktop is a better prospect than mobile**, because its bottleneck is execution rather than bytes,
and Clarity's cost there is disproportionate to its 25 KiB.

**But my earlier claim that 90 requires "giving up GA4 or Ads" was wrong and too absolute.** What the
list above gives up is Ads *remarketing via the on-page tag* — recoverable through the GA4↔Ads link —
and Clarity. Conversion measurement and Smart Bidding signal are untouched. Two further options exist
that I have **not tested** and will not assert numbers for:

- **Server-side / first-party tagging** (Google Tag Gateway via Cloudflare, or a sGTM container).
  Serves `gtag/js` from `californiafloodinsurance.com`, which removes cross-origin handshakes and
  improves cookie durability. It does **not** remove the bytes. Real infrastructure work, and its
  main argument is measurement quality, not speed.
- **Consent-mode gating**, where tags load only after interaction or consent. This is the same idea
  as theme 1.5.1/1.5.2, which failed twice — see `PERFORMANCE.md`. It would need to gate the
  *download*, not the execution, and it trades away pageviews from visitors who never interact.

Both require attribution testing against real conversion counts before anyone trusts them.

---

## 6. Conversion and Smart Bidding risk, per action

| Action | Conversion risk | Smart Bidding risk |
|---|---|---|
| Prune scroll/timer/dead-button tags (36, 38, 40, 42, 23, 25, 34 + 8 listeners) | **None.** None is a conversion. | **None.** | 
| Delete duplicate Conversion Linker (19) | **None** — tag 11 covers All Pages. | None. |
| **Remove Ads remarketing (10)** | **None** *if* section 1 holds and no active conversion action has a Google tag source. | **Indirect.** Audience lists stop growing from the on-page tag, so RLSA bid adjustments and audience targeting degrade until GA4-shared audiences replace them. Campaigns *observing* rather than *targeting* audiences lose reporting granularity. |
| **Disable Clarity** | None. | None. Clarity is not a measurement source for Ads. |
| Fix the triple form event (27 / 56 / 57) | **This one reduces risk.** If two are imported as conversions, Smart Bidding is currently being trained on inflated counts. | **Improves.** But expect reported conversions to *drop* once corrected — that is the fix working, not a regression. Note the date so the change is not mistaken for a performance decline. |

The only entry with genuine downside is removing tag 10, and the downside is remarketing reach, not
measurement.

---

## 7. A safe sequencing plan

Ordered so that each step is independently reversible and nothing that could affect conversion
counting happens without a verification window. **GTM keeps every published version — the rollback for
any step is Versions → the previous version → Publish.**

**Step 0 — before touching anything.** Record today's baseline so a later change can be judged:
GA4 conversions for the last 14 days by event, Ads conversions by conversion action, and the current
mobile PSI score **on the apex URL**. Note the container version number (currently **9**).

**Step 1 — verify the premise. DONE 7 Aug, and it failed.** Ads → Goals → Conversions showed an active
**Primary Website conversion with Enhanced Conversions** on `AW-1012143191`. So Step 4 below is
cancelled, not deferred. Leaving the step here because the gate is the reusable part: it is what
stopped a $24,771/mo account from losing its Primary conversion to a plausible-looking inference.

**Step 2 — the free wins.** Delete tag 19 (duplicate Conversion Linker) and the engagement
duplicates: tags 36, 38, 40, 42 and their listeners 72, 73, 74, 75. Publish. Nothing here can affect
a conversion. Confirm in GTM Preview that `quote_form_lead` and `form_submit_any` still fire on a test
submission, then re-run PSI on the apex URL.

**Step 3 — the orphans, verified first.** In GTM Preview on the live site, try to trigger tags 23, 25
and 34. They match Divi button text that the new theme does not use. **Only delete the ones you can
confirm do not fire.** Publish.

**~~Step 4 — the 155 KiB.~~ CANCELLED.** Step 1 failed: tag 10's Ads destination carries an active
Primary Website conversion with Enhanced Conversions. **Do not pause, delete, or otherwise touch tag
10.** The 155 KiB stays. Every earlier version of this document that described removing it is
superseded by the retraction at the top.

**Step 5 — Clarity, in Microsoft Advertising, not GTM.** Microsoft Advertising → Tools → UET tag
`5318858` → turn off the Clarity integration. Verify with
`curl -s https://californiafloodinsurance.com/ | grep -c clarity` — expect `0` — and confirm in a
browser network panel that `scripts.clarity.ms` no longer loads. Independent of everything above;
can be done any time.

**Step 6 — the form-event overlap, deliberately last.** It is a measurement correction, not a
performance change, and doing it during the performance work would confound both. Decide which single
event is the canonical quote conversion (recommend `quote_form_lead` — it is dataLayer-driven, it
carries the `cfi_is_lead` qualifier, and it does not depend on button text that a theme change can
break). Un-mark the others as key events and remove them from the Ads import. Expect reported
conversions to fall. Note the date.

### What not to do

**Do not touch tag 13, tag 11, tag 45, or tags 14/43.** Google tag, Conversion Linker, Cognito
prefill, Bing UET. Between them they carry all GA4 measurement, all attribution, all lead source
data, and $12,607/mo of Microsoft spend.

**Do not delete anything in the same publish as a change to a conversion tag.** If numbers move you
want one variable to look at.

**Do not do Steps 2–6 in one evening.** Step 4 has a mandatory seven-day observation window and
Step 6 deliberately changes reported conversion counts. Rushing them together makes the resulting
numbers uninterpretable.

---

## What this audit did not cover

**Whether remarketing audiences are actually in use.** I can see the tag; I cannot see from `gtm.js`
whether any live campaign targets or observes the audiences it builds. If nothing does, Step 4's only
cost disappears and it becomes free. **Check this first — it may make the biggest single saving
consequence-free.**

**The eight Ads conversion actions with zero goals** listed in `ACCOUNTS.md`. Those live in the Ads
account, not this container, and — now that this audit shows no `__awct` tags — they cannot be the
GTM tags I previously implied they were. They are a separate cleanup with no performance effect.

**`GTM-PJQ72VK`** (statewide). Not audited here. It carries no Google tag today, which is exactly why
statewide still scores 60 on Divi. **Audit it before statewide's cutover**, because the moment it gets
a Google tag it inherits this entire problem.
