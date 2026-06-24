---
unique_name: cardiac_arrhythmias_prediction_challenge_by_lifeq
name: Cardiac Arrhythmias Prediction Challenge by LifeQ
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Time-series (Classification)
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: medical & healthcare
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/cardiac-arrhythmias-prediction-challenge/leaderboard
source_row: 1007
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Zindi/LifeQ challenge to predict cardiac arrhythmias from sleep data. 'Sleep data' from a wearables company is typically physiological time-series (PPG/heart-rate/actigraphy signals), so the raw modality is likely sequential signal data rather than representative tabular features, and per-night arrhythmia detection is closer to time-series classification. If the provided data are aggregated per-record summary features it could be salvageable as tabular. A human must inspect whether the released features are raw signals/windows or engineered per-subject tabular aggregates, and the sample size.

---

Predict cardiac arrhythmias from sleep data.
