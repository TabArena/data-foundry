---
unique_name: layerai_air_quality_prediction_challenge
name: layerai-air-quality-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
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
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/layerai-air-quality-prediction-challenge/data
source_row: 905
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: AirQo's PM2.5 readings estimated from Sentinel-5P columns for places without a sensor, a clear use case; watch the forecasting-like setup of the top solution.
- Source: Zindi competition with AirQo (Makerere University) and Layer, 2022-07-04 to 2022-10-02, a rerun of the #ZindiWeekendz hackathon of 2022-07-01; as published: `train.csv` and `test.csv`, PM2.5 from AirQo sensors in Kampala as target, Sentinel-5P L3 products extracted from Google Earth Engine (SO2, CO, NO2, HCHO, aerosol index, O3, cloud) as features, with `date` and `device` columns (named in the 1st-place write-up). Rows not checked (Zindi data needs a login).
- Use case: AirQo estimates air quality "in areas without air quality sensor devices" from satellite data (description page); fit direct; regime grouped by device for new places, or temporal: the 1st-place team found train and test "come from different distributions" (adversarial AUC 0.9988), so the release split is likely by time; one regime to pick from the use case (USE-10).
- Siblings and duplicates: `zindi_weekendz_layerai_air_quality_prediction_challenge` is the same task in the weekend hackathon (AI `No`, forecasting, a claim this screening does not support: the target is the same-day reading, not a horizon), keep one record (PROV-4, PROV-8); related but distinct: airqo_african_air_quality_prediction_challenge (2024, several cities), urban_air_pollution_challenge, airqo_ugandan_air_quality_forecast_challenge (a forecast). External collections: none found.
- Papers and pages: competition page (https://zindi.africa/competitions/layerai-air-quality-prediction-challenge); 1st-place write-up (discussion 13525: imputation with BRITS and a Temporal Fusion Transformer).
- Metric: mean absolute error, the leaderboard metric ("The evaluation metric for this challenge is Mean Absolute Error"): deliberate (MET-4); inputs none.
- Risks for /add-dataset: the top solution treated it as a time series (TFT, possibly with the device's past PM2.5): check TP-10 and SEL-11, and drop any lagged target; Sentinel-5P columns are retrieved atmospheric quantities, read under SEL-15 rather than as image descriptors (SEL-13), to confirm; heavy missingness in the satellite columns.
- Priority: gap + (grouped regime thin, if grouped by device), use case + (the source names the actor and the gap it fills), source + (AirQo and the GEE product list), shape - (size not checked), risk - (forecasting-like solution, shift between train and test).

A Zindi competition (LayerAI) on air-quality prediction; the record has no comments or details beyond the source link. Air-quality challenges are usually tabular regression on sensor/meteorological features, which can be a valid IID or temporal predictive task, but some such challenges are forecasting future pollutant values over a horizon, which would be out of scope. There is too little info in the record to reject outright, so this is a TBD. A human must download the data to confirm it is a fixed predictive (not horizon-forecasting) task, identify the target pollutant, dataset size, and whether a temporal vs random split applies.
