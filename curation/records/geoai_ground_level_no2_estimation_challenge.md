---
unique_name: geoai_ground_level_no2_estimation_challenge
name: geoai-ground-level-no2-estimation-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
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
- https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge
source_row: 878
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

GeoAI Zindi challenge to estimate ground-level NO2 concentrations, tagged Non-IID (temporal). Unlike a pure horizon forecast this is an estimation/regression mapping task (predicting NO2 from satellite-column, meteorological and geospatial features), which could be a legitimate tabular regression if the inputs are tabularized. However it is geospatial/satellite-derived and may carry raster modality and heavy wrangling, and the split likely needs to be temporal or spatial. A human must inspect whether the features are genuinely tabular vs. raw raster, the target definition, and the appropriate split regime; place in 2nd tier pending that.
