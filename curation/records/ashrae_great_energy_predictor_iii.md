---
unique_name: ashrae_great_energy_predictor_iii
name: ASHRAE - Great Energy Predictor III
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2019'
domain: environmental science & climate
required_split:
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

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run): in scope as one regression task over all meter types and sites; a model beats the naive forecasts (issue 2).

CC (2026-10-15, Lennart): Temporal, not grouped: retrofit savings are measured on the same buildings after the cutoff (review page, issue 3). Clean the readings to the state an expert would ship, following the competition's top teams and the data owners (issue 4).

**Assessment (AI, 2026-10-15):** Cleaning: the readings come in kWh from BDG2's raw files (the competition kept each site's own unit: ton-hours, pounds of steam, mmBTU, kBTU; BDG2 paper, Table 4), and 1.70M hours (4.2%) are dropped as not recorded: electricity at 0, site 0's 2016 gap, a cooling or heating plant at 0 for 48 hours or more in its season, readings stuck for a week or more, building 1099's steam unit error. 94.5% of the 2016 hours dropped are on the 1st place team's hand-made list of bad readings (solution repository, `rank-1/input/bad_meter_readings.zip`). Task: the top five teams used no lagged readings (GEPIII overview, Table 2). The best naive forecast, each meter's hour-of-week profile from the same month a year earlier, scores RMSE 1.39 / 1.27 / 1.37 on the three windows; LightGBM with 1,000 trees on 1M training rows 1.26 / 1.18 / 1.22. One LightGBM per site scores about the same (1.24 / 1.18 / 1.22), one per building and meter worse (1.37 / 1.27 / 1.34). For unseen buildings (every fifth held out, January-April 2017) LightGBM without building_id scores 1.71, a site x use x meter profile 2.01, LightGBM with the buildings' 2016 history 1.43.

## Reference

Addison Howard, Chris Balbach, Clayton Miller, Jeff Haberl, Krishnan Gowri, and Sohier Dane. ASHRAE - Great Energy Predictor III. https://kaggle.com/competitions/ashrae-energy-prediction, 2019. Kaggle.
