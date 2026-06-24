---
unique_name: data_science_zw_2022_fire_prediction
name: data-science-zw-2022-fire-prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Time-series (Regression)
- Time-series (Forecasting)
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

Zindi Zimbabwe competition to predict burned area, a regression target. Burned-area prediction is usually spatio-temporal (satellite/weather over time and locations), so this risks being a forecasting/time-series task (excluded) rather than a fixed tabular regression; it could be acceptable if it is a per-record regression needing only a temporal/grouped split. The record has no feature/structure detail, so the protocol is undetermined. A human must inspect whether the task is a horizon forecast (reject) or a fixed predictive regression with a temporal/spatial split, plus size and feature modality.

---

predict burned area in Zimbabwe
