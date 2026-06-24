---
unique_name: urban_air_pollution_challenge
name: Urban Air Pollution Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
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
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/urban-air-pollution-challenge
source_row: 1024
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi challenge to predict air quality (PM2.5) in cities worldwide using engineered features derived from Sentinel-5P satellite data plus weather, provided as a tabular feature table. While the underlying source is satellite imagery, the competition exposes aggregated tabular features, so it could be a valid regression task; however it has a strong temporal/forecasting character (predicting daily pollution levels). A human must verify whether the released data is genuinely tabular features (not raw imagery), the exact target and temporal-split protocol, and dataset size, so a provisional 2nd-tier hold is appropriate.

---

predict air quality in cities around the world using satellite data
