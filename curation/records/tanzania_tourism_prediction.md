---
unique_name: tanzania_tourism_prediction
name: Tanzania Tourism Prediction
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
original_source: Zindi
year: '2020'
domain: business & marketing
problem_type: Regression
source_links:
- https://zindi.africa/competitions/tanzania-tourism-prediction
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-05, Lennart): `No` / `Duplicate` of `ai4d_lab_tanzania_tourism_classification_challenge` (its Review issue 4, B; PROV-6). The 2020 Pycon / Zindi "Tanzania Tourism Prediction" competition (6,476 rows, regression on `total_cost`, "The total tourist expenditure in TZS", MAE) is an earlier cut of the same NBS exit survey: 72.3% of its 4,809 training rows match a row of the 2022 release, against 23.4% by chance and about 75% if all of it sat inside the 24,675. A swapped target with added rows is a duplicate version, not a distinct task. The canonical record keeps the 2022 multiclass version; its notes use the 2020 costs to reconstruct the band edges.
