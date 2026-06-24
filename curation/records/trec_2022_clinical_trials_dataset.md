---
unique_name: trec_2022_clinical_trials_dataset
name: TREC 2022 Clinical Trials Dataset
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
- NLP (Text)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
year: '2022'
domain: medical & healthcare
problem_type: Other
original_data_state: Other
source_links:
- https://catalog.data.gov/dataset/trec-2022-clinical-trials-dataset
source_row: 837
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The TREC 2022 Clinical Trials track is an information-retrieval / ranking task: given a patient case description (free text), rank/match eligible clinical trials. This is a text-based IR/ranking problem, not an IID/temporal/grouped tabular predictive classification or regression task. It falls under out-of-scope (ranking/IR) and NLP. No clear tabular target exists, so this should be rejected.
