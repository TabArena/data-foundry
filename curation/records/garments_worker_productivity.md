---
unique_name: garments_worker_productivity
name: garments_worker_productivity
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
- 'Entities: Recur'
collections:
- TabArena Reject
original_source: UCI
year: '2020'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C51S6D
notebook_path: datasets/beyond_iid/temporal/garments_worker_productivity/garments_worker_productivity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/garments_worker_productivity/dataset.py
source_row: 716
type_adapter_id: curation-record-v1
---

## Comments

CC: "predict the productivity performance of the working teams in garment production. Date available, requires temporal split"

Ethical problems?
AT: Productivity is measured at team level, not individually, so there shouldn't be ethical concerns

The paper transforms it to a classification task, although regression is possible. Also, they apply models without consideration of time, after the target would already be collected. This makes sense for interpretable ML, to analyze drivers of lower productivity. However, to conceptualize the task for benchmarking predictive performance, we need to define at which point in time we want to predict and how far into the future we want to predict.

CC (2026-10-01, Lennart): Leak audit: **`incentive` leaks the same day's productivity; it is now lagged by one working day** (per department and team), like smv, wip, over_time, idle_time and idle_men.
- Paper (Al Imran, Rahim & Ahmed 2021, Int. J. Business Intelligence and Data Mining 19(3), 319-342; PDF from SciSpace): the rows come from the IE department's "daily line and factory efficiency report" (Sec. 3.1), written after the shift. The incentive is the structured incentive only: "Structured incentives help the employees directly through the form of higher pay for achieving the milestone or targeted performance ... a structured incentive depends on the performance, so it fluctuates with the change in performance level" (Sec. 3.1). The paper's conclusion that incentive is "the primary causation behind the productivity level" (Sec. 7) reads this relation the wrong way round.
- Data (sewing, 691 rows): the median incentive is 0 BDT below productivity 0.5, 45 at 0.7-0.8, 55 at 0.8-0.9 and 96 above 0.9 (Spearman 0.85). Within teams, day-to-day changes in incentive follow the same day's productivity (Spearman 0.53) and not the previous day's (0.07), so it is computed from the day's output. In finishing the incentive is almost always 0 (2% of rows non-zero).
- Same test for the other start-of-day features: no_of_workers and no_of_style_change show no same-day link. targeted_productivity does (0.46), but the paper defines it as "set by the authority for each team for each day", a plan the team works towards, so it stays.
- Effect (LightGBM, the 30 shipped one-day splits, mean RMSE; train-mean baseline 0.178): same-day incentive 0.134, previous-day incentive 0.140, no incentive 0.141.

CC (2026-10-06, Lennart): Kept after the task-probe review: the `unstable` flag measures the noise of single windows, not the task. Over the 30 one-day windows (17-24 rows each) random forest and LightGBM beat the train mean in 28 and 29 of them (mean skill +0.40 and +0.38, standard error 0.04); the linear model breaks down in a few windows (one at -2.9), which inflates the spread.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — the intro paper (Al Imran et al. 2021) reports six metrics without naming one; the authors' CoDIT 2019 paper headlines MAE; no unique metric (MET-5).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `quarter` (a partial order); `day` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 calendar or compass cycles ordered.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `thai_apparel_line_productivity` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the same-day incentive leak is in the BeyondArena data only (v0.2 lags it), and the team's previous-day productivity adds nothing beyond the lagged columns. Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-05, Andrej): ship as defined. The declared split (30 one-day windows, each trained on every earlier day) and the declared metric (RMSE on the productivity) checked and kept. `year` set to 2020, UCI's donation date of the rows (the paper is 2021), from the definition.

CC (2026-11-06, Andrej): the arrival facts of the temporal split accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on arrival notes of temporal splits) and written into `splits_comment`; the split is unchanged. A day's productivity is in the efficiency report after the shift, before the next day's prediction, so no gap is needed.

## Review

**Outcome:** added. The 1,197 team-days of the sewing and finishing departments of a garment factory, January to March
2015 (UCI; Al Imran, Rahim and Ahmed, International Journal of Business Intelligence and Data Mining 2021;19(3):319-342,
https://www.inderscience.com/filter.php?aid=118183): a team's productivity that day, predicted at the start of the day
from its target, team size and style changes and the previous recorded day's values. The AI recommends shipping it as
defined. Reviewed on 2026-11-04 without a review panel, from the gathered evidence (the record, the leak audit of
2026-10-01, one model run on the shipped BeyondArena data, and one check of today). Validity: the prediction point
is ours (the paper studied drivers), set at the start of the day; the end-of-day values, the incentive among them
(Lennart, 2026-10-01), enter lagged by one working day, and each of the 30 one-day test windows trains on every earlier
day. The teams recur on both sides by design: a manager predicts for the factory's own teams. The leak found earlier,
the same-day incentive that is paid for the day's output, is in the shipped BeyondArena data only; the definition lags
it. Value: untuned LightGBM RMSE 0.137 against 0.178 for the training mean over the 30 windows (today's check, 3 seeds);
the first train side holds 50% of the rows. Quality: nothing open. Weighed: a factory record with a published paper +, a
prediction point and leak fix tested on the data +, 17 to 24 test rows per window and one quarter of one factory -; a
richer sibling (`thai_apparel_line_productivity`) is screened in its own record.

**Main points:** Shipped as defined (issue 1, 2026-11-05), the record's year set from the definition; the arrival facts
(end-of-day report, lags, no gap) written into the split comment (issue 2, 2026-11-06). Nothing open.

**Record judgment:** valid. A known team's own history is a legitimate input under a temporal split, and the definition
carries it through the lagged columns: today's check added the team's previous-day productivity (and its gap to that
day's target) and it changed nothing (mean RMSE 0.1373 with and without, paired standard error 0.0018, better on 13 of
30 windows), because the lagged incentive already follows it (Spearman 0.85 in sewing). The year is UCI's donation date
of the rows (2020); the paper is 2021.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the same-day incentive is lagged, the team's own history is a legitimate input under the
       temporal split, and the record's year differed from the definition's (2021 against 2020).
     - Ship as defined?
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 30 one-day windows, RMSE | a factory record with a published paper; the leak fix tested | 17 to 24 test rows per window |
     | B | Retire | `No (Retired)`; the folder leaves the working copy | none found | no defect found |

   * **Recommendation:** A. **Decision:** ship (A) or retire (B)?

   **Resolved (2026-11-05, Andrej):** ship as defined (A); the declared split and metric checked and kept; the record's
   `year` set to 2020 from the definition.

2. **Time basis: keep the 30 one-day windows with no gap, as shipped, and write in `splits_comment` how a team-day's
   values arrive?**

   * **Problem:**
     - A team-day starts with its plan (target, workers, style changes) and ends with the efficiency report that holds
       its productivity, the label, and the other end-of-day values, which the definition lags to the team's previous
       recorded day; the next day's prediction comes after that report.
     - The record's facts fit (`Samples: Over Time`, `Time: Dated` by the day, `Target: Later` at the end of the shift),
       and the split is temporal by day, so no use-case prototype applies: a manager predicts today for known teams[^2a].
     - Keep the split as shipped (issue 1) and write these facts into the split comment?
   * **Background:**
     - No gap is needed: a day's labels are in the report before the next day starts, and each window is one day,
       trained on every earlier day[^2b].
     - Nothing crosses the cut beyond the team's own history, which is legitimate here: no team has two rows on one day
       (checked on the 1,197 rows), so a lag never reads a value of the test day; each window holds a whole factory day,
       so a shock shared by the day's teams is never in training.
     - The window size stays as decided on 2026-11-05 (17 to 24 test rows per day); this issue changes only the comment.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | 30 one-day windows, no gap; the comment gives the window count and sizes | no edit | why no gap is needed and why the lags are safe is in the curation notes only in part |
     | B | Arrival in the split comment | as A, and the comment states the end-of-day report, the lag and the whole-day windows | the reasons are where the split is | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, no `data_tags` change (a temporal split takes no time basis); append to `splits_comment`:
   "A day's productivity and its other end-of-day values are in the efficiency report written after the shift; the
   prediction is made at the start of the next day, so every training label is known and no gap is needed. The
   end-of-day values enter lagged to the team's previous recorded day (no team has two rows on one day), and each window
   is a whole factory day."

   [^2a]: **SPLIT-32** (Should): how the data was collected, when each sample, feature and target come into existence,
     is information for the split; the record carries the source's collection facts, and a split that is not temporal
     names a prototype or a forced tag; a temporal split needs neither.
   [^2b]: **SPLIT-10** (Should; amended 2026-11-04 and 2026-11-05): a gap of about the label's delay; no gap is needed
     where the collection covers what the gap guards against, such as a time column whose smallest step is longer than
     the delay. **LEAK-34** (Must): an entity's own history under a temporal split is legitimate.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the arrival notes on temporal
   splits with one mark?" The arrival text (the end-of-day report, the lags to the team's previous recorded day,
   whole-day windows) is appended to `splits_comment`. The split, its gap and `data_tags` are unchanged; a temporal
   split takes no time-basis tag.

## Reference

Mining the productivity data of the garment industry
By Abdullah Al Imran, Md Shamsur Rahim, Tanvir Ahmed. 2021

Published in International Journal of Business Intelligence and Data Mining
