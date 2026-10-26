---
unique_name: protein_location_prediction_challenge
name: protein-location-prediction-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- NLP (Text)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/protein-location-prediction-challenge/data
source_row: 993
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Wrong Domain / Source Modality`, `NLP (Text)`, SEL-12): predict a protein's subcellular location "using only its amino acid sequence"; the input is a raw sequence string, a modality where protein language models are the tool.
- Source: Zindi "Protein Location Prediction Challenge" (an AI Hack Tunisia hackathon, 2022-08-29 to 2022-08-30, 133 participants, secret code required); data "extracted from UniProtKB/Swiss-Prot", 18,206 sequences; as published: train.csv (~18,000) and test.csv (~6,500) with ID, Sequence, Kingdom, Seq_length and the target among Nucleus, Cytoplasm, Membrane, Cell membrane, Extracellular; plus sequence_esm1b_cls_embeddings_df.zip and sequence_esm1b_mean_embeddings_df.zip (ESM-1b embeddings, 160 MB each).
- Use case: annotating proteins in research; the only inputs besides the sequence are the kingdom and the length.
- Siblings and duplicates: `instadeep_kinase_classification_challenge` (`No`, the same pattern: a class from the amino-acid sequence); `antigen_avida_hil6` (`No`, `Wrong Domain / Source Modality`, `NLP (Text)`, Lennart: "NLP task / data"). The data is a cut of UniProt, where DeepLoc and similar sequence models are the field's tools.
- Metric: Log Loss over five classes (the Evaluation page).
- Reject check (AI, 2026-10-22): stands. Zindi API (https://zindi.africa/competitions/protein-location-prediction-challenge): 'predict the location in the cell where this protein is likely to be located, using just the amino acid sequence'. The inputs are ID, Sequence, Kingdom and Seq_length, and the organisers ship ESM-1b embeddings, which are the output of a protein language model. Sequence models are the field's tool here (SEL-12). This matches Lennart's 'NLP task / data' No on antigen_avida_hil6.

Zindi competition to predict the subcellular location of a protein, a classic bioinformatics multiclass classification task that is typically solved on engineered tabular sequence-derived features. If the released data is genuinely tabular (per-protein feature rows) it is a real predictive task with a clear target and likely a random split. A human must verify the feature representation (engineered tabular vs raw sequences), dataset size, number of location classes, and the data license/terms on Zindi.

---

predict the location in the cell where this protein is likely to be located
