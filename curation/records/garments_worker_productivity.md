---
unique_name: garments_worker_productivity
name: garments_worker_productivity
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: UCI
year: '2021'
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

## Reference

Mining the productivity data of the garment industry
By Abdullah Al Imran, Md Shamsur Rahim, Tanvir Ahmed. 2021

Published in International Journal of Business Intelligence and Data Mining
