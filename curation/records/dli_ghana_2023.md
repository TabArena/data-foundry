---
unique_name: dli_ghana_2023
name: dli-ghana-2023
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
year: '2023'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/dli-ghana-2023/data
source_row: 985
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Wrong Domain / Source Modality`, SEL-12): each row is a raw 1,000-base-pair DNA string, the label whether its middle 200 bp overlaps an enhancer; the competition is built around a DNA language model's embeddings, so sequence models are the tool, not tabular ones.
- Source: Zindi "Unveiling Cassava's Secrets: AI Hackathon for Accelerating African Agrigenomics" (slug dli-ghana-2023), InstaDeep, from 5 September 2023 (https://zindi.africa/competitions/dli-ghana-2023); as published: Train.csv with `ID`, `Sequence` (1,000 letters A/C/G/T), `Chromosome`, `Region`, `Target`; 13,225 training sequences (6,464 positive), 5,668 test, split by chromosome; plus 1,500-dimensional mean-pooled AgroNT embeddings (Train_embeddings.npy, Test_embeddings.npy).
- Why not vectorised-and-fine (SEL-12's exception): the only non-sequence columns are the chromosome and the region; the embeddings are a pre-trained model's hidden states, and the page frames the task as NLP on DNA ("natural language processing (NLP) and its concept of attention have successfully been applied to similar challenges in genomics").
- Siblings and duplicates: none in `curation/records/` (no cassava or AgroNT record).
- Metric: accuracy (Zindi Evaluation page).
- Previous markers `TBD` and `Missing source information` dropped: the source is known (InstaDeep, the Zindi page).
- Reject check (AI, 2026-10-22): stands. Zindi lists data_type ['Unstructured'] and type_of_problem ['Classification', 'Natural Language Processing']; each row is "a 1000-base pair (bp) DNA sequence ... represented as a string of 1000 letters", and the only vectors are a DNA language model's embeddings (https://zindi.africa/competitions/dli-ghana-2023). SEL-12, consistent with the AI's No on instadeep_enzyme/kinase and snakes_and_sequences.

Zindi 'dli-ghana-2023' competition with no description, comments, or metadata in the record, so the task, target, domain, modality, and size are all unknown. The 'DLI' (deep learning indaba) framing slightly raises the chance of an image/text task, but this is unverified. Insufficient information to assess, which on its own is not a rejection. A human must open the competition page to determine modality, task, target, size, and split.
