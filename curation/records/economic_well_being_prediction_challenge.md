---
unique_name: economic_well_being_prediction_challenge
name: economic-well-being-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- Missing source information
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: social science
required_split:
- '?'
problem_type: Regression
source_links:
- https://zindi.africa/competitions/economic-well-being-prediction-challenge/data
source_row: 909
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi 'Economic Well-Being Prediction Challenge'; the record has no body, but the title strongly implies predicting a household/regional wealth or well-being index, typically a regression task over survey and/or geospatial covariates. This is a plausible real-world tabular task in the social-science domain. There is a risk the features are derived from satellite imagery (which would lean non-tabular) or require a grouped/spatial split. A human must check the feature set (tabular vs. imagery-derived), the exact continuous target, sample size, and whether a grouped/spatial split is needed.
