---
unique_name: instadeep_kinase_classification_challenge
name: InstaDeep Kinase Classification Challenge
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
- https://zindi.africa/competitions/umojahack-tunisia
source_row: 1019
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Wrong Domain / Source Modality`, SEL-12): "UmojaHack Tunisia: InstaDeep Kinase Classification Challenge" (Zindi, 17 October 2020; the record's link https://zindi.africa/competitions/umojahack-tunisia is the right page): "Predict the class of a protein kinase enzyme using only its amino acid sequence".
- Source: as published: train.csv (197 MB), test.csv, an ID, the sequence ("up to 560 positions, and each position can take one of 20 values") and an EC class (8 classes, 2.7.13.3 with 634,731 rows the largest), plus 1024-dimensional per-amino-acid embeddings; the API tags the data type "Unstructured".
- Why out: the input is a raw amino-acid sequence, where sequence and protein language models are the tool (SEL-12); the page's own feature suggestions are per-position encodings of the sequence. The old `NLP (Text)` marker is dropped.
- Siblings: `instadeep_enzyme_classification_challenge` (its follow-up), `indabax_tunisia_2023`.
- Metric: multiclass log loss, Zindi Evaluation page.
- Reject check (AI, 2026-10-22): stands. 'Predict the class of a protein kinase enzyme using only its amino acid sequence'. Zindi API: data_type ['Unstructured'], type_of_problem ['Natural Language Processing', 'Classification'], with amino_acid_embeddings.csv and a DL starter notebook. https://zindi.africa/competitions/umojahack-tunisia

The task is to predict the class of a protein kinase using only its amino-acid sequence, a raw biological-sequence modality dominated by protein-sequence models rather than tabular learners. The input is a sequence string, not engineered tabular features, so it does not fit the representative-tabular criterion, and proper evaluation needs grouped/by-family splits. Recommend No; reconsider only if a genuine tabular feature table (not raw sequence) exists. Note the source_link points to umojahack-tunisia, so the link/name mapping should also be checked.

---

Predict the class of a protein kinase enzyme using only its amino acid sequence
