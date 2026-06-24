---
unique_name: airqo_african_air_quality_prediction_challenge
name: airqo-african-air-quality-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Time-series (Forecasting)
- Wrong Domain / Source Modality
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
- https://zindi.africa/competitions/airqo-african-air-quality-prediction-challenge/data
source_row: 883
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Estimate PM2.5 levels from satellite observations (AirQo). Reliance on satellite/remote-sensing inputs suggests features derived from imagery rather than a naturally tabular table, and air-quality estimation from satellite data is often spatio-temporal, raising both modality and forecasting concerns. The task could still be a fixed per-observation regression if the satellite signals are pre-extracted to tabular features. A human must verify whether the provided features are genuinely tabular (pre-extracted) versus raw rasters, and whether the target is a fixed estimate or a temporal forecast.

---

estimate PM2.5 levels from satellite observations
