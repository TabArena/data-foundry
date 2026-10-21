---
unique_name: open_university_learning_analytics_dataset
name: Open University Learning Analytics dataset
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
collections:
- New (BeyondArena)
original_source: Website
year: '2015'
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.24432/C5KK69
- https://analyse.kmi.open.ac.uk/
- https://analyse.kmi.open.ac.uk/open-dataset
- https://doi.org/10.6084/m9.figshare.5081998.v1
v2_path: datasets/_dev/tabarena-v0pt2/open_university_learning_analytics_dataset/dataset.py
source_row: 738
type_adapter_id: curation-record-v1
---

## Comments

Could be transformed into a prediction task https://www.kaggle.com/code/devassaxd/student-performance-prediction-complete-analysis#Part-3:-Modeling

On the website they also talk about their predictive models

Use cases of the data (?):
https://dl.acm.org/doi/10.1145/3576050.3576061

https://www.sciencedirect.com/science/article/pii/S2666920X22000637?via%3Dihub (explains how to do feature selection for the task?)

We might follow the Kaggle notebook as it seems to know more of the data and use case. Seems reasonable in most cases for the task. Could be made for several tasks, unclear which one would be best

**Assessment (AI, 2026-10-07):** The task is final_result (four classes) on day 60 for the 26,395 registrations active then, using only what is known by day 60. The Kaggle notebook above uses the exam score, so it leaks the result. The OU trains on other presentations of a module (OULAD page: "the J presentation must be used to inform the B presentation or vice versa"). Four start dates cannot give three temporal windows, so the split holds out whole presentations. LightGBM log-loss skill: IID 0.193, grouped 0.141, 2014J hold-out 0.099. BBB 2014J marks its first TMA 1 or 100 (weight 0), and models score below the prior there. Data: figshare 10.6084/m9.figshare.5081998.v1 (CC BY 4.0); the OU link is dead.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape +, risk - (Issue 5: recurring students leak across folds, kept; features built from seven joined tables). Large, well-sourced education multiclass task with real grouped structure; its day-60 framing and multi-table features are our own choices.

**Assessment (AI, 2026-10-20):** Review panel (re-check): ship after changes, made in the definition. A per-fold train filter now drops the concurrent and later registrations of each fold's test students (LEAK-17; 577-901 train rows per split; its effect net of random removal is not distinguishable from zero), and weight-0 TMA marks are left out of score_mean/score_min (USE-6; 1,655 rows, 1,652 of BBB 2014J, whose first TMA is marked 1 or 100). Untuned LightGBM log-loss skill 0.167 (sd 0.015 over 9 splits, was 0.141 and 0.052); random forest, LightGBM and logistic regression now score alike (no_spread, TP-3: read the first tuned run). The figshare md5 matches and all seven CSVs are byte-identical. Open: the SPLIT-14 amendment for the three too-few-periods datasets, the day-60 marks against the LEAK-10 earlier-grades row, the assumed 14-day TMA marking delay, the scope of the weight-0 change and the dataset pending tuned results (REVIEW.md issues 1, 11, 4, 9, 12). Priority 3: gap + (problem_type multiclass_classification), use case - (fit approximate; day 60 and the four-class target are our framing), source + (OU page and Sci. Data paper), shape + (26,395 units, 40 features, grouped), risk - (seven joined tables; ships only after the SPLIT-14 amendment).

CC (2026-10-21, Lennart): ok on the cross-dataset item: LEAK-10's grades row now reads "earlier grades not yet known at the prediction point: drop them"; the day-60 assessment marks stay (Cases row in leak_checks.md).

CC (2026-10-21, Lennart): option (a) of the cross-dataset item on tasks with too few periods: the closest regime that keeps the rows, tagged as forced from temporal, with the cost measured against the valid windows (SPLIT-8 amended).

**Assessment (AI, 2026-10-21):** tagged `ForcedGroupedFromTemporal`. Cost: on the one valid window (test 2014J) untuned LightGBM log loss 1.205 grouped against 1.185 temporal, same ranking of three model families (review panel, 2026-10-20, before the train filter and the weight-0 change). REVIEW.md issue 1 settled.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The source is a data descriptor (OU Analyse open dataset) with no prediction task or metric; our day-60 four-class task is our construction.

## Reference

Kuzilek J., Hlosta M., Zdrahal Z. Open University Learning Analytics dataset Sci. Data 4:170171 doi: 10.1038/sdata.2017.171 (2017).
