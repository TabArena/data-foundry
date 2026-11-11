---
unique_name: mercedes_benz_greener_manufacturing
name: Mercedes_Benz_Greener_Manufacturing
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
- TabSTAR
original_source: Kaggle
year: '2017'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
- https://www.openml.org/search?type=data&id=42570
notebook_path: datasets/beyond_iid/temporal/mercedes_benz_greener_manufacturing/mercedes_benz_greener_manufacturing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/mercedes_benz_greener_manufacturing/dataset.py
source_row: 708
type_adapter_id: curation-record-v1
---

## Comments

CC: "Using the index as a feature was predictive in the competition, might require a temporal split. But in general an interesting dataset, likely has groups of cars as multiple configurations could include the same car? Need to assess the impact of index as feature"

CC (2026-10-06, Lennart): Kept as a fine task after the task-probe review (flag `no_spread`: untuned skills +0.55 to +0.57; `X314` alone +0.39). Tuned methods spread: on BeyondArena TabPFN-2.6 reaches R^2 0.614, the median method 0.600 and the weakest about 0.47, with 10 of 29 methods tied with the best over the 9 windows of 320 test rows.

CC (2026-10-21, Lennart): CLEAN-11 amended: a row whose target the source names as not the task's quantity, or a single extreme target in the training period only, may leave, with the source's words.

**Assessment (AI, 2026-10-21):** the dropped testing time (265.3 s against a next highest of 169.9 s; mean 100.7, sd 12.7) is car 883 of 4,209 in ID order, inside the first 1,000 cars every test window trains on, so it meets the clause for a single extreme target in the training period only. The competition host does not name it, so no source's words exist; the reason is now in curation_comments.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `r2`, the competition's metric (Kaggle API: "R^2 score (coefficient of determination)"; was the default RMSE); within one test fold R² ranks models as RMSE does. Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): "no it also bind to what experts did by default, so again more complicated case by case": CLEAN-11 amended again: a single extreme target in the training period may leave with the source's words or where experts of the field drop such a value by default, decided case by case. The one testing time of 265.3 s leaves as the experts' default for a single extreme time.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source r2 — the competition's R^2 (Kaggle evaluation page).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `bosch_production_line_performance` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Mercedes-Benz's competition), shape +, risk 0 (the open issue is the window size and the floor).

CC (2026-11-11, Lennart): REVIEW issue 1 (which windows of cars to test), as implemented (A): the nine windows of 320 cars in ID order, from ID 2,628 on, stay, in place of the AI's nine windows of 233 cars over the newest half; SPLIT-14 as amended on 2026-11-11 admits the three oldest, which train on 46.7%, 39.1% and 31.5% of the cars (three windows under half, six at or above it).

CC (2026-11-11, Lennart): the declared horizon (320 cars, no gap, windows starting at the newest nine runs of 320 cars, IDs 7,801, 7,140, 6,487, 5,875, 5,223, 4,581, 3,920, 3,308 and 2,628) is checked, as the amended floor admits nine windows of 320, which test 2,880 cars against 2,097 at 233, and no source gives either length.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=320, unit="rows", n_windows=9`); test 320 cars each, train 3,884, 3,564, 3,244, 2,924, 2,604, 2,284, 1,964, 1,644 and 1,324 (92.4%, 84.8%, 77.2%, 69.6%, 61.9%, 54.3%, 46.7%, 39.1%, 31.5% of 4,204). `task_summary.split` no longer says the first 1,000 cars are always in training (the oldest window trains on 1,324); `splits_comment` replaces the `TimeSeriesSplit` description with the windows by car ID, the train sides, the three under half with their shares, the length's origin (the first curation's `TimeSeriesSplit` arithmetic) and the reason it is kept, and the absent gap; the outlier bullet no longer names the first 1,000 cars. `dataset check`: 0 errors, 2 warnings that predate this change (11 constant and 45 duplicated option columns; README not regenerated).

## Reference

https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
