---
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge
name: airqo-low-cost-air-quality-monitor-calibration-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data
- https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge
- https://zindi.africa/competitions/airqo-air-sensor-calibration-challenge
- https://doi.org/10.1002/ail2.76
source_row: 906
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: calibrate AirQo's low-cost PM2.5 monitors to collocated reference monitors in Kampala, a fixed same-hour regression that AirQo uses on its network.
- Source: Zindi competition by AirQo (Makerere University), 2021-04-30 to 2021-06-06 ($1,000, 318 participants), "orignally launch as a hackathon at DataFest Kampala" (`airqo-air-sensor-calibration-challenge`, 2021-04-29/30, the same data and text); as published: Train.csv and Test.csv, hourly rows at three sites (US Embassy, Makerere, Nakawa, "approx 4:2:1") over about two years; target `ref_pm2_5` (reference monitor); features two low-cost PM2.5 and two PM10 sensors, temperature, humidity, `created_at`, `site`, and site metadata (latitude, longitude, altitude, terrain, greenness, distance to a major road), constant per site; one table.
- Use case: AirQo transforms low-cost readings "as accurately as possible to the reference value" so its network is shared "as reference grade"; fit direct; regime temporal or grouped by site: the readings are an hourly stream, the target is the same hour (calibration, not a forecast, so the old `Time-series (Forecasting)` and `Missing source information` markers are refuted and dropped).
- Siblings and duplicates: `airqo_low_cost_air_quality_monitor_calibration_challenge_2` is the DataFest hackathon of the same data (proposed `Duplicate`); `air_quality_prediction_from_low_cost_iot_devices` (TBD -> 2nd Tier, other data); `faulty_air_quality_sensor_challenge` (AirQo, a different task). External collections: none found.
- Papers and pages: <https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge>; Adong, Bainomugisha, Okure, Sserunjogi (2022), "Applying machine learning for large scale field calibration of low-cost PM2.5 and PM10 air pollution sensors", Applied AI Letters, doi:10.1002/ail2.76 (AirQo; random forest cut PM2.5 RMSE from 18.6 to 7.2 µg/m³ against BAM references, cross-unit and cross-site validation; not confirmed to be the same rows).
- Metric: RMSE, the Zindi evaluation page ("The evaluation metric for this challenge is the Root Mean Squared Error"); deliberate (leaderboard, MET-4); inputs none.
- Risks for /add-dataset: only three sites, so a grouped split has three groups (a temporal split is the likelier protocol, SPLIT); the site metadata is constant per site (an identifier in disguise); the raw sensor reading may carry most of the signal (TP-4 probe; the paper's 18.6 to 7.2 suggests not); the Zindi test rows may hold no target, so the train file alone may be the data.
- Priority: gap - (environmental, regression, temporal not thin), use case + (AirQo names it), source + (AirQo data page with variable definitions, a paper), shape + (thousands of hourly rows, a temporal structure), risk 0.

An AirQo challenge to calibrate low-cost air-quality monitors (no comments in the record). Sensor-calibration tasks predict a reference pollutant value from raw low-cost sensor readings, which can be a legitimate fixed tabular regression, but the data is time-stamped and may be framed as forecasting or require a temporal split. The exact target, table structure, and size are unverified. A human must confirm whether the task is a fixed calibration regression (acceptable) versus a temporal forecast, and assess the post-cleaning row count.
