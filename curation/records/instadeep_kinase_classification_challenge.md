---
unique_name: instadeep_kinase_classification_challenge
name: InstaDeep Kinase Classification Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/umojahack-tunisia
source_row: 1019
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The task is to predict the class of a protein kinase using only its amino-acid sequence, a raw biological-sequence modality dominated by protein-sequence models rather than tabular learners. The input is a sequence string, not engineered tabular features, so it does not fit the representative-tabular criterion, and proper evaluation needs grouped/by-family splits. Recommend No; reconsider only if a genuine tabular feature table (not raw sequence) exists. Note the source_link points to umojahack-tunisia, so the link/name mapping should also be checked.

---

Predict the class of a protein kinase enzyme using only its amino acid sequence
