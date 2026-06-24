---
unique_name: carbon_dioxide_prediction_challenge
name: carbon-dioxide-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/carbon-dioxide-prediction-challenge
- https://zindi.africa/competitions/data-journey-nairobi
- https://zindi.africa/competitions/indabax-zambia-2023
- https://zindi.africa/competitions/ey-carbon-prediction-hackathon/data
- https://zindi.africa/competitions/umojahack-africa-2023-beginner-challenge
source_row: 967
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi CO2/carbon-emissions prediction challenge (several linked competition variants, including an EY carbon hackathon). Such challenges frequently derive features from satellite products (e.g. Sentinel-5P) over geographic locations and time, which raises both a remote-sensing/geospatial modality concern and a possible spatio-temporal/forecasting framing rather than a clean IID tabular regression. The underlying task could still be a fixed regression on engineered tabular features, so it is not an automatic reject. A human must determine which competition variant is intended, whether the features are tabular engineered covariates versus raw imagery, and whether the split is IID, temporal, or spatial.
