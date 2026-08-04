# The real lead numbers, from Cognito — 4 August 2026

Read directly from Cognito form 5 ("Online Flood Application"), the form both flood sites use.
**Sample: the 250 most recent entries, 26 July – 4 August (10 days).** Form 5 holds 47,830 entries
in total.

## The headline: attribution is working, and nobody knew

The June work is fully live. Every paid lead carries source, medium, campaign, **keyword**, and the
platform's click ID. Two real entries from 4 August:

| | Entry 47836 | Entry 47835 |
|---|---|---|
| Source / medium | `google` / `cpc` | `bing` / `cpc` |
| Campaign | `search_hawaii_maxconv` | `search_hawaii` |
| **Keyword** | `buy flood insurance` | `low cost flood insurance` |
| Click ID | GCLID `Cj0KCQjwm8bTBhDW…` | MSCLKID `4467336b4f521b30…` |
| Site | statewidefloodinsurance.com | statewidefloodinsurance.com |

**So the "we have no ground truth for lead source" problem does not exist.** It has been solved since
June and accumulating quietly ever since. Nothing needs building — the data needs *using*.

The fields are hidden (`Show This Field → Never`), which is why they never appear in the form, the
notification emails, or the entry summary. That is by design and it is why they looked absent.

## Volume, by source (250 entries / 10 days)

| | Count | Share | Extrapolated / month |
|---|---:|---:|---:|
| Google (`cpc`) | 88 | 35% | ~264 |
| Bing (`cpc`) | 60 | 24% | ~180 |
| **Paid total** | **148** | **59%** | **~444** |
| No attribution (organic, direct, staff phone intake) | 102 | 41% | ~306 |
| **All flood form submissions** | **250** | | **~750** |

By site: statewide 140, California 64, no `SourceWebsite` recorded 46.

Click IDs are present on **145 of 148** paid leads (85 GCLID, 60 MSCLKID) — so offline conversion
import is available whenever it is wanted, with no new work.

## Reported conversions vs actual form submissions — flood campaigns only

This is the comparison that matters, and it is now apples to apples: only flood-named campaigns on
each platform, against only flood form submissions attributed to that platform.

| | Reported conversions (30d) | Actual form submissions (30d) | Ratio |
|---|---:|---:|---:|
| Google flood campaigns | 356.6 | ~264 | **1.35×** |
| Microsoft flood campaigns | 264.0 | ~180 | **1.47×** |
| **Combined** | **620.6** | **~444** | **1.40×** |

**A correction to something I said earlier.** I compared 954 reported conversions against ~250 bound
policies and implied roughly 4× inflation. That was apples to oranges — the 954 covered every brand on
the account and every conversion type, while the 250 was bound policies from all sources including
referrals and the MGA. The honest figure for flood is **1.35–1.47×**, which is far healthier than I
implied and closer to normal.

**What plausibly makes up that gap**, in likely order of size:

1. **Phone-call conversions.** Google counts `Calls from ads` and `Calls from website`; Microsoft has
   its own. Those are **real leads** that never touch the form, so they belong in the gap and are not
   inflation at all.
2. **Failed-validation clicks.** The click-text triggers fire when the button is pressed, including
   when the form rejects the submission. This is genuine inflation, and it is what the
   `cfi_form_submit` work removes.
3. **View-through and engaged-view credit** on Demand Gen and Performance Max.
4. Staff form submissions firing the click trigger — though these carry no click ID, so Ads has
   nothing to attribute them to at campaign level, and the campaign-level effect is probably smaller
   than feared.

**The practical read: Aaron's instinct that the account is performing was right, and better supported
than my caution implied.** A 1.4× gap between reported conversions and form submissions, with phone
calls explaining much of it, is an ordinary and defensible measurement setup — not a broken one.

## The staff-intake fields exist and are never used

Form 5 has two fields built for exactly this:

- `LeadMethod` — a choice field: `Phone`, `Email`, `Referal`, `Mail`, `SMS/Text`
- `TakenBy` — free text

**Both are empty on all 250 entries.** So a staff-entered phone lead is currently distinguishable only
by the *absence* of UTM values, which also describes every organic and direct lead. The office cannot
separate its own phone intake from web leads in any report.

Two ways to fix, and this is a decision rather than a recommendation:

1. **Process:** have whoever works the staff form fill `LeadMethod` and `TakenBy`. That is what they
   are for, and it costs two clicks per lead.
2. **Structure:** add a `Web` option to the `LeadMethod` choice list and default it, so web leads are
   positively labelled rather than inferred from blanks. Then anything marked `Phone` is genuinely
   phone intake.

Worth noting this is the CRM-side twin of the Google Ads problem: v1.4.0 stops staff intake counting as
a paid conversion, and these two fields would stop it looking like a web lead in your own reports.

## What this unlocks, with no build

Answering "which campaigns produce bound policies" is now an **export and a match**, not a project:

1. Export form 5 entries from Cognito (all fields, including the hidden ones).
2. Filter to `UTMMedium = cpc` for the period.
3. Match against bound policies on name or email.
4. Group by `UTMCampaign` — and `UTMTerm` if you want keyword-level.

That is the measurement that turns the deferred Session 7 goal-cleanup decision from a judgement call
into a number. It requires no webhook, no Zapier change, no InsuredMine involvement, and no vendor.
