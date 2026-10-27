---
unique_name: data_science_zw_2022_fire_prediction
name: data-science-zw-2022-fire-prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Regression)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/data-science-zw-2022-fire-prediction/data
- https://zindi.africa/competitions/fighting-fire-with-data-hackathon
- https://zindi.africa/competitions/cmu-africa-fighting-fire-with-data
source_row: 998
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: monthly burned area per grid cell in Zimbabwe with covariates, a 2022 rerun of the 2020 "Fighting Fire with Data" data; a forecasting-like panel that needs TP-10 before it is in scope.
- Source: first released in Zindi's "Fighting Fire with Data Hackathon" (2020-06-27, https://zindi.africa/competitions/fighting-fire-with-data-hackathon), reused for CMU-Africa (2020-10-31), this record's "Fire Extent Prediction Challenge" (Data Science Zimbabwe and Repliteq AI, 2022-11-23 to 2022-11-27, Zimbabwean residents only) and the 2024 "Wildfire Prediction Challenge" (slug `predict-fire-extent`); all four pages share the text, the files and the metric. So `year` 2022 is the rerun; the data was first published in 2020 (left as is, metadata is filled only where empty). As published: `Train.csv` (monthly rows per cell, 2001 to 2013), `Test.csv` (2014 to 2016, no target), `variable_definitions.csv`; target `burn_area`, "the percentage of the area that has been burned in a given month"; covariates from Google Earth Engine (TerraClimate climate, MODIS MCD12Q1 land cover, GPW population density, GMTED2010 elevation, TRMM precipitation) that "extends into the test period". The page says both 533 areas over Zimbabwe and "3821 area squares across the DRC": a copy error to check.
- Use case: "Figuring out the dynamics that influence where and when these fires occur ... predicting how these dynamics will play out in the future, under different climatic conditions" (Description); no actor or decision named; fit approximate (fire management planning, not stated); regime temporal (train to 2013, test 2014 to 2016, as the competition did), with cells repeated in both.
- Siblings and duplicates: `predict_fire_extent` and `wildfire_prediction_challenge` (both `AI (UNVERIFIED)`) point at reruns of the same data: one record should carry it and the others become `Duplicate` (PROV-4); this record already lists the 2020 first release. `forest_fires` is a different dataset (Portugal). External collections: none found.
- Papers and pages: the four Zindi pages (read through the Zindi API); no paper.
- Metric: RMSE, "The error metric for this competition is the Root Mean Squared Error" on the proportion 0 to 1 (Evaluation page of every run), the leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: a panel of future values of one series per cell, so SEL-10 against SEL-11: TP-10 (does a model on the covariates beat each cell's monthly profile?); cell id and lat/lon carry the history (LEAK, SPLIT); the 533 against 3821 cells.
- Priority: gap - (environmental, regression, temporal not thin), use case - (no actor), source + (the page names every covariate source), shape + (about 533 cells x some 190 months from 2000-2001 to 2016, a temporal structure), risk - (forecasting-like target, SEL-10). The old `Time-series (Forecasting)` marker is dropped as a verdict marker: forecasting is not settled from the page and waits for TP-10; `Time-series (Regression)` stays as the concern.

Zindi Zimbabwe competition to predict burned area, a regression target. Burned-area prediction is usually spatio-temporal (satellite/weather over time and locations), so this risks being a forecasting/time-series task (excluded) rather than a fixed tabular regression; it could be acceptable if it is a per-record regression needing only a temporal/grouped split. The record has no feature/structure detail, so the protocol is undetermined. A human must inspect whether the task is a horizon forecast (reject) or a fixed predictive regression with a temporal/spatial split, plus size and feature modality.

---

predict burned area in Zimbabwe
