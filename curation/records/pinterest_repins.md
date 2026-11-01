---
unique_name: pinterest_repins
name: Pinterest Repins
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- NLP (Text)
- Image
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.kaggle.com/datasets/andreacombette/pinterest-analysis-using-nlp-and-image-analysis
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`NLP (Text)`, `Image`, SEL-12): the published table holds a pin's id, description, title and repin count, plus a 64x64 thumbnail; there is no tabular feature, and MulTaBench's 15 "structured" columns are E5 embedding components of the text.
- Source: Kaggle upload by andreacombette, "Pinterest analysis using NLP and Image analysis" (2024-02-13, MIT), an extension of Oneli Wickramasinghe's "Top Pinterest Influencers" upload. As published: `pinterest_finalised_2.csv`, 1,504 rows x 5 columns (an index, `id`, `description`, `title`, `repin_count`), the pin images "resized to 64x64 pixels", and `graph_pinterest.pickle` (word2vec similarities between titles and descriptions, image statistics). The page's column descriptors: "ID", "Description", "Title", "Repin Count".
- Use case: the page lists content analysis, popularity metrics and trend identification; a candidate would be a creator predicting a pin's reach before posting, an engagement task on text and image alone. MulTaBench (extended, https://huggingface.co/datasets/multabench/extended-img-cls-pinterest-popular) builds `widely repinned` from "a median split of the repin count".
- Siblings and duplicates: none (grep for pinterest and the Kaggle slug). External collections: MulTaBench (extended image release).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page; MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix F.1 (Table 8: structured, i.e. text embeddings, AUC 0.622, image 0.638, joint 0.659), Table 9 (1,504 rows; 15 structured, 1 image).
- Metric: not needed for a reject.
- Why `No`: SEL-12 (Must): the data is text and images only; with both removed nothing is left but the target, so there is no tabular task. The pins of top influencers are also a selected sample (no reason on its own).
- Reject check (AI, 2026-10-31): stands. The page's column descriptors are only ID, Description, Title and Repin Count, with images 'resized to 64x64 pixels' (https://www.kaggle.com/datasets/andreacombette/pinterest-analysis-using-nlp-and-image-analysis): with text and image removed only the target remains. MulTaBench's 15 structured columns are its own E5 embeddings of the text, as on hateful_memes (batch 01).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,504 rows; 15 structured, 0 text, 1 image features (MulTaBench Table 9); target: Repin count above the median (binary).
- Why: Predict whether a pin is widely repinned
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Target binned by MulTaBench, not the source's own target. The 15 structured ...
