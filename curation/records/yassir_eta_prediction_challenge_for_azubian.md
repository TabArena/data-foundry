---
unique_name: yassir_eta_prediction_challenge_for_azubian
name: yassir-eta-prediction-challenge-for-azubian
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
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
- https://zindi.africa/competitions/yassir-eta-prediction-challenge-for-azubian
source_row: 963
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a knowledge-competition rerun of the UmojaHack Yassir ETA hackathon, the same data as `yassir_eta_prediction_challenge`.
- Source: Zindi knowledge competition "Yassir ETA Prediction Challenge For Azubian", 2022-11-07 to 2024-06-06 (https://zindi.africa/competitions/yassir-eta-prediction-challenge-for-azubian, read through Zindi's page API); Zindi's API names its parent: `umojahack-algeria-yassir-eta-prediction-challenge` (2020-07-25); the Data Description is word for word the UmojaHack one: "The data contains details for 119,549 trips (train and test are split by date)", the same variables (`Timestamp`, origin and destination coordinates, `Trip_distance`, target `ETA`) and `Weather.csv`; "This is a learning competition. Aside from knowledge, there are no prizes".
- Siblings and duplicates: `yassir_eta_prediction_challenge` (UmojaHack South Africa, the same day and the same data as UmojaHack Algeria) is the canonical record; this rerun adds no task.
- Metric: RMSE, as in the original.
- Why it fails: two records that end at the same original source (the UmojaHack Yassir ETA data of 2020-07-25) are duplicates (PROV-4); the first publication is the hackathon (PROV-8).
- Reject check (AI, 2026-10-22): stands. PROV-4/PROV-5 (Must), source confirmed. Zindi API: parent = umojahack-algeria-yassir-eta-prediction-challenge (2020-07-25). The Data Description is word for word the UmojaHack one: "The data contains details for 119,549 trips (train and test are split by date)". It has the same files (Train, Test, Weather.csv, starter notebook) and the same target ETA. It says "This is a learning competition. Aside from knowledge, there are no prizes". The task is the same, so it is a duplicate of yassir_eta_prediction_challenge, whose source_links already hold the Algeria page; add this link there. https://zindi.africa/competitions/yassir-eta-prediction-challenge-for-azubian

This is a Yassir ETA prediction challenge variant (the 'for Azubian' edition), the same trip-duration regression task as the other Yassir ETA challenge. As a regression with a clear continuous target it is in scope, but it is very likely a re-run on overlapping or identical data, so it may duplicate yassir_eta_prediction_challenge. A human must verify whether the underlying data differs from the other Yassir record and, if not, keep only one. Provisionally Yes if unique, otherwise drop as duplicate.
