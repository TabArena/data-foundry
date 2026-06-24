---
unique_name: hospital_ratings
name: Hospital ratings
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/center-for-medicare-and-medicaid/hospital-ratings
- Medicare.gov
source_row: 835
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

Kaggle dataset of CMS/Medicare.gov hospital ratings, already tagged 2nd Tier / Scientific Discovery. Predicting a hospital star rating is plausible as a tabular task, but the overall rating is computed deterministically from the same quality-measure columns, creating a strong leakage risk, and much of the file is administrative/descriptive metadata rather than predictive features. A human must determine whether a non-leaky target and adequate clean feature set exist (and how to join the multiple measure tables). Keep in 2nd tier pending that inspection.
