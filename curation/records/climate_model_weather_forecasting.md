---
unique_name: climate_model_weather_forecasting
name: Weather
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
- tabular-dl-more-data
original_source: Kaggle
year: '2024'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/tabred-weather
- https://github.com/yandex-research/tabred/tree/main/preprocessing#weather
notebook_path: datasets/beyond_iid/temporal/climate_model_weather_forecasting/climate_model_weather_forecasting_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/climate_model_weather_forecasting_1m/dataset.py
source_row: 715
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing

Maybe not a super relevant task for tabular models.... need to make a judgment call. Given it was used in TabRed, I would say we can go for it now but might need to remove it later

TabRed uses 1 month refit horizon. For weather this is a bit much. I would argue for one or two weeks at most?

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE, Rubachev et al. 2025, TabReD (ICLR), https://arxiv.org/abs/2406.19380; Shifts weather (Malinin et al. 2021) also uses RMSE.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `shifts_weather_temperature` (TBD -> 2nd Tier, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (written by the curation, 'for example'), source + (the TabReD paper), shape +, risk 0 (the open issue is the choice of windows).

## Reference

TabRed
