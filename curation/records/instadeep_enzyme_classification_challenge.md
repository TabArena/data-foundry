---
unique_name: instadeep_enzyme_classification_challenge
name: instadeep-enzyme-classification-challenge
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
- https://zindi.africa/competitions/instadeep-enzyme-classification-challenge/data
source_row: 921
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

This InstaDeep challenge classifies enzymes from raw amino-acid sequences, a biological-sequence (protein language) modality where sequence/embedding models dominate rather than generic tabular learners. The input is a single sequence string per example, not engineered tabular features, so it fails the representative-tabular criterion. It would also require grouped (by-family) splits to avoid leakage. Recommend No as a tabular candidate; a human could reconsider only if a meaningful pre-extracted tabular feature representation is provided.
