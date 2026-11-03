---
unique_name: rain_in_australia
name: Rain_in_Australia
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: GOV Website
year: '2026'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package
- https://rattle.togaware.com/weatherAUS.csv
- https://www.bom.gov.au/climate/dwo/
v2_path: datasets/_dev/tabarena-v0pt2/rain_in_australia/dataset.py
source_row: 724
type_adapter_id: curation-record-v1
---

## Comments

Predict whether it will rain tomorrow. Time-series data, but target is lagged. Might work as a task.

**Assessment (AI, 2026-10-07):** The data first appeared as weatherAUS in the R package rattle (Graham Williams),
built from Bureau of Meteorology daily observations; the Kaggle upload is a snapshot to 2017-06-25, rattle's file runs
to 2026-01-30. RISK_MM is the rain of the station's next row in the file (RainTomorrow = RISK_MM > 1 mm), which is 29-401
days later before four missing periods (184 rows, dropped). BoM records rain "in the 24 hours to 9am", and MaxTemp ("in
the 24 hours from 9am"), sunshine, gust and the 3 pm observations fall inside the label's window. The definition
predicts at 9 am with those ten columns from D-1 (LightGBM ROC AUC 0.846 against 0.900 as published), on two-week
temporal windows.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 4: forecasting scope still open (next value of a station's rain series)). Large temporal climate classification with a strong government source, held back mainly by the open forecasting-scope question.

**Assessment (AI, 2026-10-20):** The review panel recommends shipping after changes. On the 9 shipped 14-day windows LightGBM reaches ROC AUC 0.849, against 0.902 with the ten after-9 am columns of the same day put back (what the D-1 lag removes). The location's 9 am rain reading (Rainfall, RainToday; the label of the day before) adds 0.0027 (0.8495 against 0.8467), and the model beats persistence (0.661) and the location-by-month climatology (0.672) in 9 of 9 windows, so the skill does not come from the lagged target (SEL-11, TP-10 leg 1 holds; the wording of leg 2 is open in REVIEW.md). A blank Cloud9am is mostly a clear sky at 9 am, not a later fill. The fit is approximate (no weather-model forecast, USE-8); calm wind and RH 0% are now cleaned. The original publisher is rattle's weatherAUS from BoM's Daily Weather Observations (links added); Kaggle is the 2017 snapshot. Priority 3: gap -, use case -, source +, shape +, risk 0 (gap: no thin domain, problem type or regime; use case: written by the curation and the fit is approximate; risk: the scope question is the wording of a rule, the measured facts show no leak).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The data is a Kaggle dataset / rattle example file built from BoM observations with no task description or metric; no paper defines one. Binary fallback roc_auc.

CC (2026-10-26, Lennart): the year is the definition's 2026: we ship rattle's weatherAUS as captured on 2026-10-05, a file that grows with BoM's daily observations.

CC (2026-10-26, Lennart): issue 5: drop the 2,571 rows without their own 9 am rain reading and the 201 rows whose next row is far later; their label covers 48 hours or more, another quantity than the 24-hour call (USE-5).

**Assessment (AI, 2026-10-26):** answers on the review page: 26 contiguous 14-day windows over the last year triple the test rows (16,457) and halve the standard error of the mean ROC AUC (0.008 against 0.016) without an exception to SPLIT-15 (issue 2); a naive forecast of the rain amount with a > 1 mm rule reaches ROC AUC 0.75 against 0.849 for the full model, ahead in 9 of 9 windows (issue 4); under TP-10 as amended on 2026-10-22 `RainToday` (the target of the day before) fails leg 2 and `Rainfall` is allowed (issue 4); patching the 2016-17 gap from the Kaggle snapshot adds 19,003 training rows with no measurable gain (-0.0009, SE 0.0022) from the period where the copies disagree most (issue 3); the neighbours' 9 am readings add +0.020 ROC AUC (SE 0.0045) with a time-zone guard but are a feature build CLEAN-19 does not admit as written (issue 6).

CC (2026-10-26, Lennart): issue 2: "Do so": 26 contiguous 14-day test windows over the last year instead of 9 spaced six weeks apart (follows SPLIT-15; no exception needed).

CC (2026-10-26, Lennart): issue 3: "keep the rattle file as it is now"; no patch of the 2016-17 gap from the Kaggle snapshot.

CC (2026-10-26, Lennart): issue 4: keep Rainfall and RainToday. TP-10's leg 2 as amended on 2026-10-22 is "not quite right": "we are allowed to keep this if we can compute it and it makes sense to know the last observation". TP-10 amended accordingly: the last observation of the target column may stay when it is known at the prediction point and the actor reads it.

CC (2026-10-26, Lennart): issue 6: "add the features to do this task as it looks good with only 9am is not later setting": the other locations' 9 am Rainfall, Pressure9am and Humidity9am of the same day, where that location's 9 am comes no later than the row's own (CLEAN-19 amended).

CC (2026-10-26, Lennart): the declared metric, ROC AUC (the fallback; the source defines none), is checked as declared.

**Assessment (AI, 2026-10-26):** applied: 26 contiguous 14-day windows (2025-02-01 to 2026-01-30, 16,457 test rows, 619-642 per window, train at least 93.8% of the rows); 143 columns of the other locations' 9 am Rainfall, Pressure9am and Humidity9am of the same day, each kept only where that location's 9 am comes no later than the row's own under both clock and standard time (a row reads 32 other locations on average); Rainfall and RainToday kept under TP-10 as amended. `dataset check` clean (166 columns). Task probes (5 of 26 windows): LightGBM ROC AUC 0.853, linear 0.832, no flag. Leak probes: no single feature or missing pattern stands out (own Humidity9am alone 0.807 of 0.899; the neighbours' missing pattern, 0.586 at most, follows the row's time zone, which Location already holds); no exact copies. No open issue is left, so the folder's REVIEW.md is removed; the record keeps `WIP (DF)` until the curator's ship verdict.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `WindDir9am` (a partial order); `WindGustDir_prev_day` (a partial order); `WindDir3pm_prev_day` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 calendar or compass cycles ordered; cloud cover 9 (sky obscured, 3 rows) set to missing (CLEAN-10).

## Reference

Kaggle
