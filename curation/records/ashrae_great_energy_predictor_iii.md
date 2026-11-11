---
unique_name: ashrae_great_energy_predictor_iii
name: ASHRAE - Great Energy Predictor III
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 4
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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSLE (Root Mean Squared Logarithmic Error) (https://www.kaggle.com/competitions/ashrae-energy-prediction/overview/evaluation).

**Assessment (AI, 2026-10-21):** metric now `Metric.source("rmsle", target_transform="log1p")` instead of rmse on the log1p target: the competition's RMSLE on the meter reading in kWh, computed after the inverse of the shipped log1p (MET-3); the score is the same number as before. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): cloud_coverage 9 (sky obscured, 9,905 rows) kept as recorded with a note, as rain_in_australia does (CLEAN-10)..

CC (2026-10-31, Lennart): marks on the review board of PR #37: cloud cover 9 (sky obscured, the amount cannot be estimated) set to missing (CLEAN-10).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `cbecs_2018_building_energy_use` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 4: gap 0, use case + (ASHRAE names the savings estimate after a retrofit), source + (ASHRAE's competition with its overview paper), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-10, Lennart): test windows (`ashrae_great_energy_predictor_iii_1m`, issue 1), marked discuss: "Is four month even the right time horizion here? I feel we oculd go to 2 or 3 months easily". The horizon audit keeps 4 months, so by his instruction ("if the current time horizon makes sense and is justifiable keep it and resolve them") the issue resolves as A: January-April, May-August and September-December 2017 stay, the oldest window (49.47% of the rows) admitted by SPLIT-14's amendment of 2026-11-08.

CC (2026-11-10, Lennart): the declared horizon (4 months, no gap, windows starting 2017-09-01, 2017-05-01 and 2017-01-01) is checked, as a savings baseline is fit once on the year before a retrofit and predicts the year or two after it without a refit, so the window is the longest that gives three windows inside 2017.

**Assessment (AI, 2026-11-10):** applied: `temporal` unchanged; `splits_comment` and `task_summary.split` now give the use case as the reason for the length and SPLIT-14's amendment of 2026-11-08 as the reason for the oldest window (two windows above the floor, every test meter's building in training, folds by entity would test unseen buildings) in place of "the competition's setting", and 49.47% (19,325,311 of 39,062,170 rows) in place of 49.12%. Horizon audit (model-free): the competition trained on 2016 "to predict the second and third years" and ranked on 2018 (Miller et al. 2020, arXiv 2007.06933, Sec. 2.2); CalTRACK fits the baseline "to baseline data in the 365 days immediately prior" and computes savings with "the coefficients ... from the final model" (Sec. 3.1.3, 3.6.1.1); LBNL's NMEC guidance v2.0 (p. 10) uses one year of baseline and performance periods; 3-month windows give 9 candidates above the floor, 2-month 10, 12-month one. The amendment's score: LightGBM (one seed, default parameters, 1,000 trees, early stopping on the last 10% in time order of the default 1M sample of the newest year, the date in skrub's recommended encoding) scores RMSLE 1.212, 1.342 and 1.213, newest first: 1.277 on the two valid windows, 1.256 on all three; without the absolute date features (year, total seconds) 1.240, 1.176 and 1.247 (1.208 and 1.221). Either way the oldest window scores like the newest and moves the mean by about 0.02; May-August decides the direction.

## Reference

Addison Howard, Chris Balbach, Clayton Miller, Jeff Haberl, Krishnan Gowri, and Sohier Dane. ASHRAE - Great Energy Predictor III. https://kaggle.com/competitions/ashrae-energy-prediction, 2019. Kaggle.
