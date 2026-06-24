---
unique_name: outsmarting_outbreaks_challenge
name: outsmarting-outbreaks-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
- TBD
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/outsmarting-outbreaks-challenge/data
source_row: 870
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi disease-outbreak challenge provided as multiple to-be-joined tables with temporal structure. Depending on framing it could be a legitimate temporal-split predictive task (e.g. predicting case counts/outbreak risk for a location-period) or a forecasting task, which would be out of scope. It needs substantial wrangling to join tables and define a fixed predictive target. Suggest TBD -> 2nd Tier; a human must verify whether the task is a fixed predictive classification/regression with a temporal split versus a forecasting-over-horizon problem, and assess size after joins.
