---
unique_name: early_learning_predictors
name: early_learning_predictors
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Website
year: '2024'
domain: education
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/962
- https://zindi.africa/competitions/datadrive2030-early-learning-predictors-challenge
notebook_path: datasets/beyond_iid/grouped/early_learning_predictors/early_learning_predictors.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/early_learning_predictors/dataset.py
source_row: 742
type_adapter_id: curation-record-v1
---

## Comments

Very nice dataset. It was used in a Zindi challenge, where an additional focus next to predictive performance was on interpretability. I think they used random splits, but it should be either temporal or group based (by school). Needs some preprocessing since it doesn't make sense to use all ~1200 features. But we can follow the Zindi challenge, where a subset of features was provided

predict whether a child thrives by five

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: count_staff_unpaid_managers, pra_breadwinner, pra_letcee_club, practitioner, pri_funding_subsidy, quintile_used.

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: pra_breadwinner, pra_letcee_club, pri_funding_subsidy (yes/no questions by name). Reverted: count_staff_unpaid_managers (a count), practitioner and quintile_used (meaning not documented).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — the Zindi challenge's error metric, root mean squared error of the total ELOM score.

**Assessment (AI, 2026-10-26):** an open doubt under CLEAN-14, from the cross-dataset item of 2026-10-21: `practitioner` and `quintile_used` hold only 0 and 1 and stay numeric because no codebook gives their meaning; they become categorical if a codebook names them yes/no items.

## Reference

DataDrive2030. ELOM and Thrive by Five Index 2016-2023, Merged Data [dataset]. Version 1. Cape Town: DataDrive2030 [producer], 2024. Cape Town: DataFirst [distributor], 2024. DOI: https://doi.org/10.25828/WG0D-Y909
