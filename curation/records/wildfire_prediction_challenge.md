---
unique_name: wildfire_prediction_challenge
name: wildfire-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/wildfire-prediction-challenge/data
source_row: 933
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): the IndabaX Eswatini 2024 "Wildfire Prediction Challenge" re-runs Zindi's 2020 "Fighting Fire with Data" hackathon with the same files.
- Source: https://zindi.africa/competitions/wildfire-prediction-challenge (28 Aug to 30 Sept 2024, Deep Learning IndabaX Eswatini, read through Zindi's API). Its parent is "predict-fire-extent" (Jul-Aug 2024, record `predict_fire_extent`), whose parent is "fighting-fire-with-data-hackathon" (27 June 2020, the first publication). All three list Train.csv 19,531,802 bytes, Test.csv 5,802,277, SampleSubmission.csv 429,661 and variable_definitions.csv 2,344, with the same text: "We've aggregated data on burned areas across Zimbabwe for each month since 2001. You'll be given the burn area data up to the end of 2013", target `burn_area` per cell and month, test 2014 to 2016.
- Siblings and duplicates: the family's record is `data_science_zw_2022_fire_prediction` (its links include the 2020 hackathon and cmu-africa-fighting-fire-with-data, same byte sizes; `TBD -> 2nd Tier`, a forecasting-like panel that needs TP-10); `predict_fire_extent` is a further re-run of the same files (one for the main session to align).
- Metric: RMSE (Evaluation page), as in 2020.
- Reject check (AI, 2026-10-22): stands. Zindi API (https://zindi.africa/competitions/wildfire-prediction-challenge): parent 'predict-fire-extent'; files Train.csv 19,531,802, Test.csv 5,802,277, SampleSubmission.csv 429,661, variable_definitions.csv 2,344 bytes and the 'Fighting_Fire_with_Data_Starter_Notebook.ipynb', the same as the 2020 fighting-fire-with-data-hackathon; same task text ("burn area data up to the end of 2013", predict 2014 to 2016). Same task, same source: PROV-4 (Must); the family is carried by data_science_zw_2022_fire_prediction (TBD -> 2nd Tier, TP-10 pending), so no task is lost. Replace the record's old 'Time-series (Forecasting)' marker with 'Duplicate'.

Zindi wildfire prediction challenge typically asks for forecasting burned area per spatial cell across future months using historical climate/satellite time-series. This is spatio-temporal forecasting over a horizon, which is out of scope for the benchmark. Source modality leans toward gridded/satellite-derived features rather than a natural cross-sectional tabular task. A human should verify whether any fixed cross-sectional framing exists, but as known it is forecasting, so No.
