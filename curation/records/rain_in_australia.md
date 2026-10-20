---
unique_name: rain_in_australia
name: Rain_in_Australia
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
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

## Reference

Kaggle
