---
unique_name: phoenix_ke_analytics_hackathon
name: phoenix-ke-analytics-hackathon
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
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/phoenix-ke-analytics-hackathon/data
source_row: 959
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Duplicate`, PROV-4): a 2024 learning hackathon by the Phoenix KE Analytics community that re-uses the data of the Zindi Sendy Logistics Challenge (2019), recorded as `sendy_logistics_challenge`.
- Source: Zindi "Phoenix Ke Analytics Data Science Project" (2024-04-26 to 2024-05-19, 41 participants, no prizes); its Description and Data pages repeat the Sendy challenge word for word ("Sendy, in partnership with insight2impact facility, is hosting a Zindi challenge to predict the estimated time of delivery of orders"; "The dataset provided by Sendy includes order details and rider metrics"); its files have the same sizes as the 2019 Sendy Logistics Challenge's: Train.csv 4,094,263 bytes, Test.csv 1,209,061, Riders.csv 29,751, VariableDefinitions.csv 2,661, SampleSubmission.csv 117,450 (Zindi API, both competitions).
- Use case: Sendy's delivery ETA from pickup to arrival (the canonical record's task); no distinct task.
- Siblings and duplicates: `sendy_logistics_challenge` (TBD -> Yes, the first publication, 2019-08-23 to 2019-11-26, 2,201 participants), `sendy_logistics_challenge_2` (marked `Duplicate`, the mentorship and EDSA re-runs).
- Metric: Root Mean Squared Error (the Evaluation page, identical to Sendy's).
- Reject check (AI, 2026-10-22): stands. I checked the Zindi API myself. phoenix-ke-analytics-hackathon and sendy-logistics-challenge (https://zindi.africa/competitions/sendy-logistics-challenge) have byte-identical file sizes: Train.csv 4094263, Test.csv 1209061, Riders.csv 29751, VariableDefinitions.csv 2661, SampleSubmission.csv 117450. The Description is the same Sendy text, so this is the same source and task (PROV-4), and the canonical sendy_logistics_challenge is TBD -> Yes.

A Zindi 'Phoenix KE analytics hackathon' with no description, target, size, or modality given in the record. There is not enough information to determine the task or whether the data is tabular. Insufficient info is not by itself grounds for rejection. Suggest TBD -> 2nd Tier; a human must open the competition data page to determine the predictive target, data layout, and size.
