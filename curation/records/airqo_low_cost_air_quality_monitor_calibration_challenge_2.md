---
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge_2
name: AirQo Low-Cost Air Quality Monitor Calibration Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/airqo-air-sensor-calibration-challenge/data
source_row: 1021
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi AirQo sensor-calibration challenge: learn a regression mapping from low-cost air-quality sensor readings (plus context) to a reference PM2.5 value. This is a genuine real-world tabular regression task (sensor calibration), not a forecast of future values over a horizon, so it is in scope despite 'air quality' often implying time series. Likely needs a temporal split because measurements are collocated time series. A human must verify the feature set is tabular (not raw spectra/time windows), the number of usable rows after cleaning, and that the target is a continuous reference PM2.5.

---

predict pm2_5
