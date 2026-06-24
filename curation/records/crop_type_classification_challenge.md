---
unique_name: crop_type_classification_challenge
name: Crop Type Classification Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Wrong Domain / Source Modality
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: environmental science & climate
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/geoai-hack-2022/data
source_row: 1012
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi GeoAI-Hack-2022 crop-type classification challenge. Crop-type mapping challenges are usually built on satellite remote-sensing data (e.g. Sentinel-2 multispectral pixels, often as time series of band reflectances), which is a geospatial/image modality and frequently spatio-temporal rather than a clean IID tabular task. If the released data are per-field tabular spectral/temporal aggregates with a categorical crop label it could be usable as tabular classification. A human must determine whether the features are raw imagery/time-series bands versus engineered tabular features, the label set, the size, and the appropriate (likely spatial) split.

---

classify crop type
