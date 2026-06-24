---
unique_name: postoperative_patient_data
name: postoperative_patient_data
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
original_source: Github
year: '?'
domain: medical & healthcare
required_split:
- '?'
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/postoperative_patient_data/metadata.yaml
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The UCI/PMLB post-operative patient dataset (predicting discharge decision) has only 88 samples. Prior TabArena verdict and both Lennart and Andrej flagged it as too small for the 3-fold CV protocol. With under 90 rows it is unsuitable for reliable benchmarking. Suggest No on size grounds.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

88 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
