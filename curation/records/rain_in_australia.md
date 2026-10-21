---
unique_name: rain_in_australia
name: Rain_in_Australia
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: GOV Website
year: '2017'
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

## Reference

Kaggle
