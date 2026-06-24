---
unique_name: predict_fire_extent
name: predict-fire-extent
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
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/predict-fire-extent/data
source_row: 884
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi competition to predict the burned area of wildfires in Zimbabwe, i.e. a regression target. Such challenges often supply geospatial/satellite-derived features which may be raster imagery (out of scope) or pre-extracted tabular covariates per location-time. There is also a risk this is a forecasting task over time. Suggest TBD -> 2nd Tier; a human must verify whether inputs are tabular features versus imagery, whether the task is a fixed predictive (temporal-split) regression rather than forecasting, and the dataset size.

---

predict the burned area of wildfires in Zimbabwe
