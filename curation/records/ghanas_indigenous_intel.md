---
unique_name: ghanas_indigenous_intel
name: ghana-indigenous-intel-challenge
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Too Small
- Data Quality Issue
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ghana-indigenous-intel-challenge/data
notebook_path: datasets/beyond_iid/temporal/ghanas_indigenous_intel/ghanas_indigenous_intel.ipynb
source_row: 868
type_adapter_id: curation-record-v1
---

## Comments

Need to be African citizen to accept terms, but license is CC-BY SA 4.0. So technically it would be legal if an African citizen accepts the terms and shares the data with us...

10K samples are available, but for this kind of task a lot more data would be beneficial. Nevertheless, the data is still usable

CC (2026-10-01, Lennart): **Retired for now (No (Retired); Too Small, Data Quality Issue). Revisit if a cleaner or larger release appears, or if the organisers can say which rain-gauge readings are missing.**
- Task (Zindi): `Target` is the rain measured with the farmers' garden rain gauges (heavy / medium / small / no rain in the next 12-24 h); the farmers' own forecast is a feature (`predicted_intensity`, `confidence`, `indicator`). Only 503 of 10,928 rows (4.6%) carry an actual indigenous forecast with an indicator; the other rows have forecast 0 and no indicator.
- Not a leak: under the temporal split the same farmers are in train and test, so a farmer's reporting history is legitimate information. Dropping `user_id` would not remove it anyway (the most common reporter per community matches 86% of rows; 12 communities have a single reporter).
- Too small: each farmer submits in batches (55% of rows in batches of >= 5 within one minute), and every batch has one label. The 10,928 rows are 626 farmer-days with rain on 102. Each of the 6 shipped test windows holds rain from only 3-6 farmer-days by 1-4 farmers, so macro-F1 depends on a handful of batches. Macro-F1 (mean over the windows): always NORAIN 0.241, each farmer's most common training label 0.392, LightGBM 0.432, LightGBM without user/community/district 0.261. The indigenous indicators add almost nothing beyond who is reporting.
- Censoring bias in the label: "no rain" appears to mix "it did not rain" with "the farmer did not measure". 22 of 43 farmers (4,055 rows) never record rain from 30 May to 20 July 2025, the main rainy season, while farmer 23 records rain on 77% of rows; three of the never-rain farmers report no rain on district-days when most other farmers record rain (84 rows on 5 district-days). Rain can be very local, so this is a likely bias rather than a proven one.
- Removed from the TabArena v0.2 working copy; the shipped BeyondArena notebook is unchanged.

## Reference

-
