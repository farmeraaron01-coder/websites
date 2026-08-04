# Lead-to-policy attribution — the monthly process

The goal: **bind rate and cost per bound policy, by campaign.** That is the number neither Google nor
Microsoft can see, and the one that would make the deferred goal-cleanup decision straightforward.

## The lag is the whole problem, and it breaks the obvious method

Some leads bind in days. Some take a month or two. Anything in escrow takes longer still. So the
intuitive comparison — *August leads against August policies* — is wrong in two directions at once:

- August's policies include binds from June and July leads, so they get credited to August's campaigns.
- August's leads that will bind in October are counted as failures, so August looks worse than it is.

Run that way, **every recent month looks bad and every campaign looks worse than it is**, and the newest
campaigns — the ones you most want to judge — look the worst of all, purely because their leads have had
the least time to close.

## The method: cohorts, not months

A **cohort** is all the leads that arrived in one month. You follow that cohort forward and ask how many
of *those* leads eventually bound, whenever the bind happened.

```
July cohort:  312 paid leads  →  binds in Jul: 41   Aug: 33   Sep: 12   Oct: 4   = 90 bound (28.8%)
```

That gives a true bind rate per cohort, and per campaign within the cohort. It also means recent months
are **incomplete on purpose** — not bad, just not finished yet.

### Maturity: which numbers are decision-grade

| Cohort age | Status | Use it for |
|---|---|---|
| 0–30 days | Very incomplete | Lead volume only. Never judge a campaign on this. |
| 30–90 days | Filling in | Directional. Watch, do not act. |
| **90–150 days** | **Mostly mature** | **Decision-grade for normal binds.** |
| 150+ days | Complete including escrow tail | Final. Use for benchmarks. |

**These windows are a starting assumption and should be replaced with your real numbers.** After two or
three cohorts have matured, the data itself will show the distribution of lead-to-bind days — at which
point set the maturity line where, say, 90% of binds have landed. That is a one-off calculation and then
the thresholds are yours rather than guessed.

## The design point that matters: one growing file, not monthly snapshots

Because a June lead can bind in October, **the leads table must keep every lead, forever.** If each
month replaces the last, you lose the ability to match a late bind back to the lead that produced it.

Two master files, both append-only:

**`leads-master.csv`** — one row per Cognito form 5 entry, ever:

`Entry ID | Submitted | First | Last | Email | Phone | State | Zip | Site | Source | Medium | Campaign | Keyword | GCLID | MSCLKID | Lead type | LeadMethod | TakenBy`

**`policies-master.csv`** — one row per policy written, ever:

`Policy # | Bound date | Effective date | First | Last | Email | Phone | Premium | Carrier | State | Written by`

Then matching is a join, and the analysis is a group-by. Nothing is ever recomputed from scratch or
lost.

## The monthly run

Fifteen minutes once the first one is set up.

1. **Export new leads** — Cognito form 5, entries since the last run. Append to `leads-master.csv`.
   (Or ask Claude to pull them through the Cognito API, which is how the first 749 were produced.)
2. **Export policies written** — from the CRM, all policies bound since the last run, with the columns
   above. Append to `policies-master.csv`.
3. **Match.** On `Email` first, then `Phone`, then `Last name + Zip` as a fallback. Expect 70–90% match
   rates; record the unmatched count as a data-quality figure rather than discarding it.
4. **Report**, per lead-cohort month and per campaign:
   - leads, bound, bind rate
   - spend for that campaign in that month (from the Ads export)
   - **cost per bound policy** = spend ÷ bound
   - median days from lead to bind
5. **Only act on cohorts 90+ days old.** Everything newer is monitoring.

## The output worth having

One table, and it is the only table in this whole project that measures the actual business:

| Campaign | Leads | Bound | Bind rate | Spend | CPA (lead) | **Cost per bound policy** | Median days to bind |
|---|---:|---:|---:|---:|---:|---:|---:|

**The two right-hand columns are where the decisions live.** A campaign with an attractive lead CPA and a
poor bind rate is worse than it looks, and one with an expensive lead CPA and a strong bind rate may be
your best campaign. Neither Google nor Microsoft can see that distinction, because neither knows which
leads became customers.

## Practical notes

- **Match on email first.** It is the most reliable key. Phone formatting varies; names get misspelled.
- **Keep the click IDs.** `GCLID` and `MSCLKID` are what would later allow **offline conversion import**
  — feeding bound policies back to the ad platforms so bidding optimises toward customers rather than
  form fills. Google accepts GCLIDs up to 90 days old, so that option expires if the data is not kept.
- **Staff and organic leads matter to this too.** 35% of flood leads arrive with no paid attribution.
  Their bind rate is worth knowing — if phone leads bind at three times the rate of paid web leads, that
  is a finding about where to spend attention, not just budget.
- **PII lives outside the repo.** Both master files contain customer names, emails and phone numbers.
  Keep them in Dropbox or the CRM, never in version control. The sample built on 4 Aug was deliberately
  sent directly and not committed.
- **First run is retrospective.** Pull as much lead history as Cognito will give (form 5 holds 47,830
  entries) and as much policy history as the CRM will export. Cohorts from 4+ months ago are already
  mature, so the first run can produce decision-grade numbers immediately rather than waiting a quarter.

## Making it recurring

Three ways, in increasing order of automation:

1. **A calendar reminder.** First business day of the month: export, append, match, report. Nothing to
   maintain.
2. **A Todoist recurring task** with these steps as the description, so the checklist travels with the
   task and nothing gets skipped.
3. **A scheduled Claude session** (a Routine) that fires monthly, pulls the new Cognito entries through
   the API itself, and produces the report — leaving you only the CRM policy export to drop in. This is
   the least work per month, and the piece it cannot do is the CRM export, because that lives behind a
   login Claude has no access to.

Option 3 is worth it if this becomes a standing report. Option 1 is enough to prove the method first.

### Two things needed before the first real run

1. **Your actual typical lead-to-bind window.** The 90–150 day maturity line above is my assumption, not
   your data. If most binds land inside 45 days with an escrow tail out to 120, the thresholds move and
   decisions can be made sooner.
2. **Confirmation the CRM can export these columns:**
   `Policy # | Bound date | Effective date | First | Last | Email | Phone | Premium | Carrier | State | Written by`
   Bound date and email are the two that the method genuinely depends on. If email is not reliably
   captured on the policy record, matching falls back to phone and name+zip, and the match rate drops.
