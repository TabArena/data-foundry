---
unique_name: mercedes_benz_greener_manufacturing
name: Mercedes_Benz_Greener_Manufacturing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
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

## Reference

https://www.kaggle.com/competitions/mercedes-benz-greener-manufacturing
