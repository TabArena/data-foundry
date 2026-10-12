---
unique_name: ashrae_great_energy_predictor_iii
name: ASHRAE - Great Energy Predictor III
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2019'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/competitions/ashrae-energy-prediction/leaderboard
v2_path: datasets/_dev/tabarena-v0pt2/ashrae_great_energy_predictor_iii_1m/dataset.py
source_row: 701
type_adapter_id: curation-record-v1
---

## Comments

Solutions used IID version of the data, unclear if this is still the case but this is a forecasting-as-tabular task

But all solutions also used additional data that had a leak. Leak should not be a problem for our benchmarking efforts

I think we can make this a nice split / use it for our setting

A lot of notes on this data....see data foundry. Split must be temporal/grouped. But also we only have 1 year but data was used to forecast 2 years....

**Assessment (AI, 2026-10-07):** Valid; added as `ashrae_great_energy_predictor_iii_1m` (temporal, log1p reading, RMSE = the competition's RMSLE). The "only 1 year" gap closes with the competition team's own 2017 release: BDG2's `data/meters/kaggle/kaggle.csv`, "the data for the validation data set (2017) that matches seamlessly with the training data" (Miller et al. 2020, Sci Data, p. 8). We train on 2016 and test three 4-month windows of 2017. Scope: "regression-based machine learning to predict the energy savings of a retrofit" (GEPIII overview, Sec. 2.2); no lagged readings. Licence note: Kaggle rule 7B bars redistribution to non-participants; BDG2 is MIT at the pinned commit, CC BY 4.0 on Zenodo, CC BY-SA in its LICENSE since 2023.

## Reference

Addison Howard, Chris Balbach, Clayton Miller, Jeff Haberl, Krishnan Gowri, and Sohier Dane. ASHRAE - Great Energy Predictor III. https://kaggle.com/competitions/ashrae-energy-prediction, 2019. Kaggle.
