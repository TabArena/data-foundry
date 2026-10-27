---
unique_name: air_quality_prediction_from_low_cost_iot_devices
name: air-quality-prediction-from-low-cost-iot-devices
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2025'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/air-quality-prediction-from-low-cost-iot-devices
source_row: 939
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a sensor-calibration regression (CO2 from low-cost sensor readings against a reference meter), not forecasting, but a short beginner hackathon with an undocumented company experiment and unknown size.
- Source: Zindi hackathon "Air Quality Prediction from Low-Cost IoT devices", hosted by Hackade (Nigeria), 2025-01-30 to 2025-02-02 (Zindi API, read 2026-10-22); "The dataset is sourced from an experiment conducted by Chemotronix. The company deployed three prototype devices - Alpha, Beta, and Charlie - to collect sensor readings alongside a high-accuracy reference meter." As published: Train.csv, test.csv, Variable Description.csv; "Training Data: Contains sensor readings and corresponding CO2 levels measured by the reference meter"; row and column counts not stated.
- Use case: Chemotronix "seeks to build machine learning models that can accurately map sensor readings to CO2 levels measured by reference meters" so it can "manufacture low-cost sensors that rival the performance of expensive reference meters": calibration at the time of a reading; fit direct; regime grouped by device (three devices only) or temporal if the readings carry time stamps (not known without the data).
- Siblings and duplicates: AirQo calibration records `airqo_low_cost_air_quality_monitor_calibration_challenge`, `airqo_low_cost_air_quality_monitor_calibration_challenge_2` (PM2.5, other data) and the forecast records `airqo_ugandan_air_quality_forecast_challenge`, `airqo_african_air_quality_prediction_challenge`: same kind of task, different source; no duplicate found. External collections: none found.
- Papers and pages: the Zindi page only; no paper or Chemotronix data documentation found.
- Metric: Root Mean Squared Error (Zindi Evaluation page); a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: a stream of readings (`Time-series (Regression)` if timestamps exist; SPLIT-7 when none survived); three devices make a grouped split coarse; size unknown (TP-5); a public/private 70-30 test split hints the test may be a time block. The old markers `Missing source information` (the page names Chemotronix and the setup) and `Time-series (Forecasting)` (the target is the concurrent reference reading, not a future value) are dropped.
- Priority: gap 0, use case + (Chemotronix's calibration decision, stated), source 0 (a hackathon page, no paper), shape 0 (unknown size), risk - (stream of readings, three devices).

A Zindi challenge to predict air quality from low-cost IoT sensor devices, with no descriptive comments. Such tasks are usually either sensor calibration/regression on tabular sensor readings (potentially viable) or temporal forecasting of pollutant levels (excluded), and they are inherently time-stamped so a temporal split is likely. The modality and exact target are unverified from the record. A human must determine whether the task is a fixed calibration/estimation (acceptable) or a forecast over a horizon, plus the table structure and size.
