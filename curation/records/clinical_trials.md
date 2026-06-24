---
unique_name: clinical_trials
name: Clinical Trials
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
- TBD
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Temporal)
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/thedevastator/a-quick-overview-of-clinical-trials
- https://www.aerodatalab.org/birds-eye-view-of-research-landscape
source_row: 849
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Kaggle 'overview of clinical trials' table (aggregated research-landscape data), already tagged 2nd Tier / Scientific Discovery and Non-IID (Temporal). It reads as a descriptive registry/overview table rather than a dataset built around a clear predictive target, which risks falling into the non-predictive/scientific-discovery exclusion. It could be reframed as a predictive task (e.g. predicting trial outcome/completion) if a sensible target and adequate clean rows exist. A human must define whether a real predictive target is available, the row count after cleaning, and confirm the temporal split regime.
