---
unique_name: wildfire_prediction_challenge
name: wildfire-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://zindi.africa/competitions/wildfire-prediction-challenge/data
source_row: 933
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi wildfire prediction challenge typically asks for forecasting burned area per spatial cell across future months using historical climate/satellite time-series. This is spatio-temporal forecasting over a horizon, which is out of scope for the benchmark. Source modality leans toward gridded/satellite-derived features rather than a natural cross-sectional tabular task. A human should verify whether any fixed cross-sectional framing exists, but as known it is forecasting, so No.
