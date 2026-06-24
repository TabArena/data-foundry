---
unique_name: air_quality_prediction_from_low_cost_iot_devices
name: air-quality-prediction-from-low-cost-iot-devices
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
- https://zindi.africa/competitions/air-quality-prediction-from-low-cost-iot-devices
source_row: 939
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi challenge to predict air quality from low-cost IoT sensor devices, with no descriptive comments. Such tasks are usually either sensor calibration/regression on tabular sensor readings (potentially viable) or temporal forecasting of pollutant levels (excluded), and they are inherently time-stamped so a temporal split is likely. The modality and exact target are unverified from the record. A human must determine whether the task is a fixed calibration/estimation (acceptable) or a forecast over a horizon, plus the table structure and size.
