---
unique_name: zindi_weekendz_layerai_air_quality_prediction_challenge
name: zindi-weekendz-layerai-air-quality-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/zindi-weekendz-layerai-air-quality-prediction-challenge/data
source_row: 991
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 2: estimating PM2.5 at AirQo sensor sites from same-day Sentinel-5P retrievals, so not a forecast (the old `No` with `Time-series (Forecasting)` is refuted by the page); the first release of the data that the rerun record `layerai_air_quality_prediction_challenge` also carries.
- Source: #ZindiWeekendz hackathon "Layer.ai Air Quality Prediction Challenge" with AirQo (Makerere University) and Layer, 2022-07-01 to 2022-07-03 (https://zindi.africa/competitions/zindi-weekendz-layerai-air-quality-prediction-challenge, read through Zindi's page API); as published: `train.csv` (with the target), `test.csv` ("without the target-related columns"); target `pm2_5` from AirQo's sensors; features "extracted from google earth engine": SO2, CO, NO2, HCHO, UV aerosol index, O3 (NRTI L3) and cloud (OFFL L3).
- Use case: "The use of satellite data could expand air quality predictions to areas without air quality sensor devices"; "predict air quality readings from AirQo's sensors using Sentinel 5P data" (Description): AirQo estimates PM2.5 where it has no sensor; fit direct; regime grouped by site for new places (the use case), or temporal as the release split; one regime to pick (USE-10).
- Siblings and duplicates: `layerai_air_quality_prediction_challenge` is the rerun (2022-07-04 to 2022-10-02, MAE, `TBD -> Yes`, priority 3): the same task and publisher, keep one record (PROV-4); this page is the first publication (PROV-8). Related but distinct: `airqo_african_air_quality_prediction_challenge`, `urban_air_pollution_challenge`, `airqo_ugandan_air_quality_forecast_challenge` (a forecast). External collections: none found.
- Papers and pages: the competition page; the rerun's 1st-place write-up (Zindi discussion 13525) treated it as a time series.
- Metric: MAE ("The evaluation metric for this challenge is Mean Absolute Error", Evaluation tab), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the Sentinel-5P columns are retrieved atmospheric quantities (SEL-15), not image descriptors (SEL-13), to confirm; heavy missingness in the satellite columns; any lagged PM2.5 of the device would be a forecasting input (TP-10); duplicate with the rerun record.
- Priority: gap 0 (environmental not thin; grouped only if chosen), use case + (AirQo and the gap it fills named), source + (AirQo, the GEE products listed), shape 0 (size not checked), risk - (duplicate with the rerun, forecasting-like solutions).

The LayerAI air quality challenge (Zindi Weekendz) concerns PM2.5 air-quality prediction, typically forecasting pollutant concentrations over time/locations from satellite (e.g. Sentinel-5P) and meteorological time-series. This is a spatio-temporal forecasting task over a horizon, which is excluded from scope, and the features are largely satellite-derived rather than a natural cross-sectional tabular table. A human could confirm framing, but as known this is forecasting, so No.

---

pm2,5 air quality prediction
