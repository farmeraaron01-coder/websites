# Who produced what, 13 Aug 2026

Aaron ran the briefs through outside models and pasted the results back. The two
batches came from **different models**, which matters when weighing a claim that
turns out to be wrong: an error pattern in one batch says nothing about the other.

| File | Brief | Model |
|---|---|---|
| `task1-serp-teardown.md` | `KIMI-BRIEF-cost-page.md` task 1 | Kimi |
| `task2-zone-segmentation-survey.md` | `KIMI-BRIEF-cost-page.md` task 2 | Kimi |
| `task3-fema-claims-statistic.md` | `KIMI-BRIEF-cost-page.md` task 3 | Kimi |
| `job1-statutory-definition.md` | `KIMI-BRIEF-2-lender-and-loss-of-use.md` job 1 | **Grok 4.6** |
| `job2-loss-of-use-survey.md` | `KIMI-BRIEF-2-lender-and-loss-of-use.md` job 2 | **Grok 4.6** |

The second brief is named `KIMI-BRIEF-2-…` because it was written for Kimi. It was
answered by Grok 4.6. The filename is left alone so it still matches the references
to it elsewhere in these notes; this table is the authority on who answered it.

## Verification status

Nothing in either batch was accepted on the model's say-so.

- **Kimi's task 3** (the 29%-of-claims-outside-high-risk-zones figure) was checked
  against floodsmart.gov directly and confirmed.
- **Kimi's task 1** contained a wrong impressions figure for the cost page
  (19,311 at position 17.4). The real figures from Search Console are **2,866
  impressions at 18.15, 20 clicks**. Corrected across five files; the origin of the
  wrong number was never reconstructed.
- **Grok's job 1** quotations were spot-checked against uscode.house.gov, govinfo
  and Cornell LII, all three agreeing word-for-word. It also caught an overstatement
  in my own draft about the 2019 compliance aid, which I corrected.
- **Grok's job 2** is a survey of public pages; the two dollar figures it found
  ($7,500 USI/Chubb, $25,000 Flood Insurance Guru) are competitor claims recorded as
  such, not figures we adopt.

The standing rule from both briefs holds: a model's finding is a lead, not a source.
Anything published gets checked against the primary document first.
