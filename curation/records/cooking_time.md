---
unique_name: cooking_time
name: Cooking Time
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
decision_markers:
- Anonymized
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
- tabular-dl-more-data
original_source: Kaggle
year: '2024'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/cooking-time
- https://github.com/yandex-research/tabred/tree/main/preprocessing#cooking-time
notebook_path: datasets/beyond_iid/temporal/cooking_time/cooking_time_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/cooking_time_1m/dataset.py
source_row: 712
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing. Need to see what we want to resample

TabRed uses 1 week refit horizon. 36 days in train data

Tasks look reasonable even if missing all semantic information. Given that the data is from various restaurants and that it is unclear which restaurant this is from, there might be group-based leakage.

Note: numerical features are normalized with a noisy-quantile transform QuantileTransformer(X_num + 1e-5 * randn)

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in cooking_time_1m (order time + cooking time, from the raw file after the under-one-minute filter): without a gap 172, 126 and 108 train orders per weekly window (newest first; starts 2023-12-28, 12-21, 12-14) end after the window start; with a gap of one day (TemporalSplits(..., gap=1)) none. The gap removes 280k, 264k and 239k of the 11.1M, 9.1M and 7.2M earlier orders (2.5 to 3.3%); each train side is still a random 1M. Gap set in dataset.py, counts in splits_comment; script local-data-warehouse/_runs/2026-10-21_crosscut/x21-0/late_labels.py.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE (TabReD regression tasks), Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380), Sec. 4 / App.: RMSE for regression, ROC AUC for classification.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (TabReD names the task, not who acts on it), source + (the TabReD paper), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-10, Lennart): REVIEW issue 1, "Option B: Keep, state why and the limit.": the three weeks from 14 December 2023 to 3 January 2024 stay as the test windows; the splits comment says they are the only weekly windows above the 50% floor and that all three lie in the weeks before and over New Year.

CC (2026-11-10, Lennart): the declared horizon (7 days, a one-day gap, windows starting 2023-12-28, 2023-12-21 and 2023-12-14) is checked, kept: one week is TabReD's own validation and test length (the two newest windows are its validation and test weeks); a week holds every weekday once, and cooking times follow a weekly cycle.

**Assessment (AI, 2026-11-10):** applied in dataset.py: the windows declared as cutoffs, which build the same splits as `n_windows=3` (test 1,662,794, 2,040,512 and 1,921,331 orders before the 500k cap, train 10,856,304, 8,832,570 and 6,935,762: 84.8%, 69.0%, 54.2%); `splits_comment` and `task_summary.split` give the reason, the floor (the earliest start that keeps half the orders for training is 11 December, 51.9% with the gap; no orders on 11-12 December) and the limit (mean log minutes 2.548, 2.554 and 2.599 in the windows against 2.527 to 2.532 in the weeks from 16 November to 6 December); "refit every week (TabReD)" is gone from the use case, the split and the fit reason, and from the issue's Background in REVIEW.md. Horizon audit (split-auditor, model-free): TabReD (arXiv 2406.19380) trains on 15 November to 20 December, validates on 21-27 December and tests on 28 December to 3 January and names no refit cadence; Friday and Saturday orders cook 2.57 to 2.64 mean log minutes against 2.46 to 2.51 on Monday to Thursday; two weeks give 1 candidate above the floor; the one-day gap is 12 times the longest cooking time (2 hours) and stays by the family rule of 2026-10-21. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-11, Lennart): REVIEW issue 2 (every other week), "Option B: Every other week.": the test windows are the newest week and every other week before it, 28 December 2023 to 3 January 2024, 14-20 December and 4-10 December 2023 (7 days, a one-day gap), as for delivery_eta_1m; 4-10 December, a week before the holiday run-up, trains on 37.5% of the orders, the one window under half beside 84.8% and 54.2%, signed off (SPLIT-14 as amended on 2026-11-11). It supersedes the three newest weeks decided on 2026-11-10 (issue 1, B), which stays resolved; the 7-day length and the one-day gap of the horizon check of 2026-11-10 stay.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` declares the cutoffs 2023-12-28, 2023-12-14 and 2023-12-04 (7 days, gap 1 day); test 1,662,794, 1,921,331 and 1,861,029 orders before the 500k cap, train 10,856,304, 6,935,762 and 4,797,156 (84.8%, 54.2%, 37.5% of 12,799,474). Every day of 4-10 December holds orders (208,774 to 326,051); its mean log minutes are 2.533, against 2.548 and 2.599 in the two newer windows. Without the gap 155 of its train orders would end after its start; the gap removes 277,577 of its 5,074,733 earlier orders (5.5%). `task_summary.split` and `splits_comment` (the windows and why, the counts, the shares, the gap figures) are rewritten; `accepted_check_warnings` accepts `splits_train_under_half` with the sign-off. `dataset check`: 0 errors, 0 warnings (README not regenerated).

## Reference

TabRed
