---
unique_name: hubmap_hpa_donor_age
name: HubMAP HPA
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
source_links:
- https://www.kaggle.com/competitions/hubmap-organ-segmentation
- https://www.kaggle.com/datasets/miquel0/hubmaphba-tiled-dataset-512x512
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12; SEL-8): tiles of histology images from the HuBMAP + HPA "Hacking the Human Body" competition, whose task was to "Segment multi-organ functional tissue units" (Dice); MulTaBench re-targets the donor's age in ten quantile bins, to be read from the tissue tile.
- Source: HuBMAP and the Human Protein Atlas on Kaggle (<https://www.kaggle.com/competitions/hubmap-organ-segmentation>, a research competition, June to September 2022, 1,174 teams): tissue images of five organs with organ, donor sex and age, image size and the tissue-unit masks as run-length encodings. MulTaBench (core, Table 3) takes 512x512 tiles from a Kaggle user's copy (miquel0/hubmaphba-tiled-dataset-512x512): 12,581 rows, `organ`, `img_height`, `img_width`, `sex`, `rle` (the competition's mask), `idxs_tile`, one tile; target `age` in 10 bins.
- Use case: none: a donor's age is known; "whether tissue morphology encodes biological age" (MulTaBench) is a research question (USE-2). Regime grouped: many tiles per biopsy share the donor's age.
- Siblings and duplicates: none (searched hubmap). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle competition; MulTaBench (arXiv 2605.10616, Appendix B.1 and D.2; Table 11: AUROC 0.959 frozen, 0.968 target-aware).
- Metric: Dice (the competition's `evaluationMetric` from the Kaggle API), a segmentation metric; MulTaBench scores AUROC.
- Risks for /add-dataset: not applicable; the AUROC of 0.959 likely comes from tiles of one biopsy in both train and test, so the image identifies the donor (SPLIT, grouped).
- Reject check (AI, 2026-10-31): stands. The rows are 512x512 histology tiles from the HuBMAP + HPA segmentation competition (https://www.kaggle.com/competitions/hubmap-organ-segmentation, Dice), and MulTaBench says the age target asks 'whether tissue morphology encodes biological age', a question about the image. Without the tile, organ, sex and tile geometry carry no task, and the donor's age is known to anyone who could act on it.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 12,581 rows; 5 structured, 1 text, 1 image features (MulTaBench Table 3); target: Donor age in 10 equal-frequency bins.
- Why: Predict donor age band from a histology tissue tile, organ, sex and tile metadata
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Target binned by MulTaBench, not the source's own target. Tiles of the HuBMAP+HPA 2022 Kaggle segmentation competition images; many tiles per donor/slide (grouped). The ...
