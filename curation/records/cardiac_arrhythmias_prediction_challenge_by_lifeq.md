---
unique_name: cardiac_arrhythmias_prediction_challenge_by_lifeq
name: Cardiac Arrhythmias Prediction Challenge by LifeQ
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Time-series (Classification)
- TBD
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: medical & healthcare
required_split:
- '?'
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://zindi.africa/competitions/cardiac-arrhythmias-prediction-challenge/leaderboard
source_row: 1007
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: raw RR-interval series per night (515 sessions), a time-series classification that needs feature extraction before it is a table.
- Source: Zindi private hackathon for IndabaX South Africa, hosted by LifeQ, 2021-11-12 to 2021-11-22 (secret code required); as published: one CSV per sleep study (`rr_xxxxxx.csv`, RR intervals in ms with relative timestamps, from 200 Hz ECG in a sleep laboratory, awake periods included), `training_target.csv` with "expertly hand-labelled arrhythmia class labels"; 349 training and 166 test sessions. Not one table: `original_data_state` changed from One Table (AI-filled) to Other.
- Use case: a wearable warns a person of chronic atrial fibrillation or another arrhythmia from a normal night's sleep "and allow for early treatment" (the source's words); fit approximate (polysomnography ECG, not a wearable); regime IID over sessions, unless one person has several sessions (not stated).
- Siblings and duplicates: `arrhythmia` (UCI, ECG features, a different dataset); none other found. External collections: none found.
- Papers and pages: https://zindi.africa/competitions/cardiac-arrhythmias-prediction-challenge (Description, Data Description, Evaluation).
- Metric: Accuracy on the leaderboard (Zindi Evaluation page), but "Your 2 selected submissions will be scored against a different error metric by the LifeQ team. Prizes will be distributed according to this private validation", which is not named; so the leaderboard's accuracy is a weak choice and the fallback is likely (MET-4, MET-10).
- Risks for /add-dataset: a table has to be built from the series (HRV features of our own, CLEAN; `Time-series (Classification)`, SEL-12 judged per dataset: RR-interval features with tabular models are standard for AF detection, so not a clear out); 349 labelled sessions with an unknown class balance (TP-5); access through a private hackathon.
- Priority: gap - (medical not thin), use case + (actor and decision named by the host), source - (only the Zindi page), shape - (515 series, no table), risk - (series to featurise).

Zindi/LifeQ challenge to predict cardiac arrhythmias from sleep data. 'Sleep data' from a wearables company is typically physiological time-series (PPG/heart-rate/actigraphy signals), so the raw modality is likely sequential signal data rather than representative tabular features, and per-night arrhythmia detection is closer to time-series classification. If the provided data are aggregated per-record summary features it could be salvageable as tabular. A human must inspect whether the released features are raw signals/windows or engineered per-subject tabular aggregates, and the sample size.

---

Predict cardiac arrhythmias from sleep data.
