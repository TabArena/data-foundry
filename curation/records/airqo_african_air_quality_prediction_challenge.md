---
unique_name: airqo_african_air_quality_prediction_challenge
name: airqo-african-air-quality-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/airqo-african-air-quality-prediction-challenge/data
- https://zindi.africa/competitions/airqo-african-air-quality-prediction-challenge
source_row: 883
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: same-day PM2.5 estimation from Sentinel-5P products for cities without ground monitors, deployed by AirQo, with a train/test split by city.
- Source: Zindi competition by AirQo (Makerere University) with Mozilla Foundation, 2024-03-15 to 2024-06-16 ($3,000, 1,042 participants); as published: Train.csv and Test.csv (row count not stated on the page), target `pm2_5` from ground observations, features Sentinel-5P L3 products "extracted from Google Earth Engine" (SO2, CO, NO2, HCHO, UV aerosol index, O3, cloud), with city and date; one table.
- Use case: AirQo estimates PM2.5 "for eight cities in seven African countries" where ground networks are thin, and "the models you create will be deployed through AirQo's user-friendly digital platform"; fit direct; regime grouped: "Train set contains the cities, Kampala, Lagos, Nairobi and Bujumbura. The test contains the cities Kisumu, Gulu, Accra and Yaoundé" (deploy to unmonitored cities). The old `Time-series (Forecasting)` marker is refuted: the target is the same-day level, not a future value (SEL-10 does not apply), so it was dropped.
- Siblings and duplicates: `urban_air_pollution_challenge` (Zindi, Sentinel-5P + weather to PM2.5, TBD -> 2nd Tier), `layerai_air_quality_prediction_challenge` and `zindi_weekendz_layerai_air_quality_prediction_challenge` (TBD -> Yes), the other AirQo records (calibration, forecast); different cities and years, so no duplicate by provenance, but a curator may want one Sentinel-5P PM2.5 task, not several. External collections: none found.
- Papers and pages: <https://zindi.africa/competitions/airqo-african-air-quality-prediction-challenge>; no paper found.
- Metric: RMSE, the Zindi evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"); deliberate (leaderboard, MET-4); inputs none.
- Risks for /add-dataset: the inputs are satellite retrievals (SEL-13 names remote-sensing spectra as image-derived; these are retrieved gas columns, closer to SEL-15 measurements, so `Wrong Domain / Source Modality` stays as a concern for the curator); many missing retrievals under cloud; only 8 cities, so a grouped split by city gives few groups per fold (SPLIT); check whether the date and the city coordinates are needed as features.
- Priority: gap + (grouped regime thin), use case + (AirQo names the deployment), source + (AirQo's data page lists every product), shape + (several thousand rows likely, many numeric features, grouped), risk - (modality question, few groups).

Estimate PM2.5 levels from satellite observations (AirQo). Reliance on satellite/remote-sensing inputs suggests features derived from imagery rather than a naturally tabular table, and air-quality estimation from satellite data is often spatio-temporal, raising both modality and forecasting concerns. The task could still be a fixed per-observation regression if the satellite signals are pre-extracted to tabular features. A human must verify whether the provided features are genuinely tabular (pre-extracted) versus raw rasters, and whether the target is a fixed estimate or a temporal forecast.

---

estimate PM2.5 levels from satellite observations
