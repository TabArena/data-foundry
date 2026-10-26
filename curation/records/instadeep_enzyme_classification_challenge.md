---
unique_name: instadeep_enzyme_classification_challenge
name: instadeep-enzyme-classification-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
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

**Screening (AI, 2026-10-22):** `No` (`Wrong Domain / Source Modality`, SEL-12): "InstaDeep Enzyme Classification Challenge" (Zindi, 17 November 2020 to 21 February 2021): "Can you predict the class of an enzyme using only its amino acid sequence?"
- Source: https://zindi.africa/competitions/instadeep-enzyme-classification-challenge; as published: Train.csv (374 MB) and Test.csv with sequence ID, amino-acid sequence, organism and one of 20 labels; 8 organisms in train, 2 in test; plus unlabelled_data.zip (633 MB) "for language modelling or other unsupervised learning tasks".
- Why out: the only input is a raw biological sequence, where protein language models are the tool (SEL-12); the page builds the task around pre-training on unlabelled sequences. The old `NLP (Text)` marker is dropped: the modality is a biological sequence, not language.
- Siblings: `instadeep_kinase_classification_challenge` (its predecessor, UmojaHack Tunisia 2020), `indabax_tunisia_2023` (sequence ddG, same sponsor).
- Metric: accuracy, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. 'Can you predict the class of an enzyme using only its amino acid sequence?'; unlabelled_data.zip (633 MB) is supplied 'for language modelling'. The only input is a raw protein sequence, where protein LMs dominate (SEL-12). https://zindi.africa/competitions/instadeep-enzyme-classification-challenge

This InstaDeep challenge classifies enzymes from raw amino-acid sequences, a biological-sequence (protein language) modality where sequence/embedding models dominate rather than generic tabular learners. The input is a single sequence string per example, not engineered tabular features, so it fails the representative-tabular criterion. It would also require grouped (by-family) splits to avoid leakage. Recommend No as a tabular candidate; a human could reconsider only if a meaningful pre-extracted tabular feature representation is provided.
