---
unique_name: delivery_eta
name: Delivery ETA
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
- https://www.kaggle.com/datasets/pcovkrd84mejm/delivery-eta
- https://github.com/yandex-research/tabred/tree/main/preprocessing#delivery-eta
notebook_path: datasets/beyond_iid/temporal/delivery_eta/delivery_eta_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/delivery_eta_1m/dataset.py
source_row: 713
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in delivery_eta_1m (order time + delivery time, from the raw file after the under-one-minute filter): 0 train orders in each of the 3 weekly windows (starts 2024-01-01 04:02, 2023-12-25 00:03, 12-18 00:02) end after the window start, because orders pause overnight and the last train order of a window is delivered 57 minutes to 6 hours before it. No gap added; the counts are in splits_comment. Script local-data-warehouse/_runs/2026-10-21_crosscut/x21-0/late_labels.py.

**Assessment (AI, 2026-10-21):** Metric declared for `delivery_eta_1m` under MET-1..13: source rmse — TabReD (Rubachev et al., ICLR 2025) scores RMSE on the log minutes.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `lade_last_mile_delivery_eta` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (TabReD names the task, not who acts on it), source + (the TabReD paper), shape +, risk 0 (the 45 features that stop on 23 November 2023 are a data change, not a leak, issue 2).

CC (2026-11-10, Lennart): REVIEW issue 1 (which weeks to test), "Option B: Every other week.": the test windows are 1-7 January 2024, 18-24 December and 4-10 December 2023 instead of the last three weeks (18 December 2023 to 7 January 2024), under SPLIT-15 as amended on 2026-11-10.

CC (2026-11-10, Lennart): REVIEW issue 2, as implemented (A): the 45 features `num_76` to `num_121`, which stop being recorded on 23 November 2023 at 11:00, stay, with a `Kept on purpose` note: at each test window's prediction point a model gets what the service's own model got, and the block is still recorded for some orders of every test window, unlike anes_voting_2026's 327 dropped columns with no variation in any test year.

CC (2026-11-10, Lennart): the declared horizon (7 days, no gap, windows starting 2024-01-01, 2023-12-18 and 2023-12-04) is checked, kept: each window is one week, the length of TabReD's own validation and test periods; TabReD states no refit cadence.

**Assessment (AI, 2026-11-10):** applied in dataset.py: `temporal` with the three cutoffs; test 1,188,182, 1,485,323 and 1,444,992 orders before the 500k cap, train 15,469,869, 12,517,876 and 9,706,793 (92.9%, 75.1%, 58.3%); 0 late orders at each start (the last training order before 4 December is delivered at 22:58 on 3 December, before 18 December at 23:04, before 1 January at 21:55), so still no gap. Orders carrying `num_96` in the test windows, measured on the frame: 4,508 of 4-10 December (0.31%), 5,126 of 18-24 December (0.35%), 7,823 of 1-7 January (0.66%). The `Kept on purpose:` bullet of issue 2 is in the notes; "refit every week (TabReD)" is gone from the use case, the split and the fit reason. Horizon audit (split-auditor, model-free): TabReD (arXiv 2406.19380, its datasheet and preprocessing) trains on 20 October to 11 December, validates on 11-18 December and tests on 18-25 December 2023 and names no refit cadence (the median label delay is 5.5 minutes); one day gives 41 candidates without a source, two weeks 2 (fails SPLIT-14). `dataset check`: 0 errors, 0 warnings (README not regenerated).

## Reference

TabRed
