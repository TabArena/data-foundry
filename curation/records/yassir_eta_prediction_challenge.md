---
unique_name: yassir_eta_prediction_challenge
name: Yassir ETA Prediction Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-south-africa-yassir-eta-prediction-challenge
source_row: 1026
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Yassir ETA prediction (Zindi/UmojaHack) is a ride-hailing estimated-time-of-arrival regression: trip-level features (origin/destination, distance, time of day, etc.) map to trip duration. This is a representative real-world tabular regression with a clear continuous target, not forecasting a future-value series. A temporal split is likely appropriate given trips occur over time. A human must verify dataset size, feature columns, and that geospatial coordinates do not constitute the dominant signal; provisionally Yes.

---

Predict the estimated time of arrival for Algerian ride-hailing business Yassir
