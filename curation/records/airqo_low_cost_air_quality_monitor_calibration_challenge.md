---
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge
name: airqo-low-cost-air-quality-monitor-calibration-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data
source_row: 906
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

An AirQo challenge to calibrate low-cost air-quality monitors (no comments in the record). Sensor-calibration tasks predict a reference pollutant value from raw low-cost sensor readings, which can be a legitimate fixed tabular regression, but the data is time-stamped and may be framed as forecasting or require a temporal split. The exact target, table structure, and size are unverified. A human must confirm whether the task is a fixed calibration regression (acceptable) versus a temporal forecast, and assess the post-cleaning row count.
