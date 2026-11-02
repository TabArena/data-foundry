---
unique_name: glaucoma_smdg
name: Glaucoma SMDG
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
- https://doi.org/10.34740/KAGGLE/DS/2329670
- https://www.kaggle.com/datasets/deathtrooper/multichannel-glaucoma-benchmark-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12): fundus photographs from 19 public glaucoma datasets, published as "the largest public repository of fundus images with glaucoma"; the tabular side is age, sex and eye for about 40% of the rows and intraocular pressure for 0.2%.
- Source: Riley Kiefer et al., SMDG-19 on Kaggle (DOI 10.34740/KAGGLE/DS/2329670, 2023): "a collection and standardization of 19 public datasets, comprised of full-fundus glaucoma images, associated image metadata like, optic disc segmentation, optic cup segmentation, blood vessel segmentation, and any provided per-instance text metadata like sex and age", "designed to be exploratory and open-ended with multiple use cases and no established training/validation/test cases"; papers Kiefer et al. (ICISDM 2023, a catalogue of public glaucoma datasets; ICIVC 2023, fundus standardisation). As MulTaBench ships it (core, Table 3): 12,449 rows, `sex`, `age`, `eye`, `left_right`, `sbp`, `dbp`, `hr`, `iop` and one fundus photo; target `types` (0: 7,549, 1: 4,767, -1 uncertain: 133). Missing shares in MulTaBench's `data.parquet` (a preview read 2026-10-31): sex 64%, age 60%, eye 54%, sbp, dbp, hr and iop 99.8%.
- Use case: glaucoma screening from a fundus photo, read by an ophthalmologist or an image model; the photo is the reading, and no clinical score derived from it is in the table, so SEL-14 does not apply. Regime grouped (19 source datasets, both eyes of one patient).
- Siblings and duplicates: none (searched glaucoma, smdg, airogs, fundus). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle page and the Kiefer et al. papers it cites; MulTaBench (arXiv 2605.10616, Appendix B.1; Table 11: AUROC 0.921 frozen, 0.934 target-aware).
- Metric: none in the source (no task, no splits); MulTaBench scores AUROC.
- Risks for /add-dataset: not applicable; besides, the labels follow 19 sources' definitions, with an "uncertain" class.
- Reject check (AI, 2026-10-31): stands. SMDG-19 is 'a collection and standardization of 19 public datasets, comprised of full-fundus glaucoma images' and 'the largest public repository of fundus images with glaucoma' (https://www.kaggle.com/datasets/deathtrooper/multichannel-glaucoma-benchmark-dataset). Without the image only age, sex and eye remain for about 40% of rows, and no clinical reading such as a cup-to-disc ratio is a column, so SEL-14 has nothing to keep.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 12,449 rows; 8 structured, 0 text, 1 image features (MulTaBench Table 3); target: Glaucoma: positive, negative or uncertain (3 classes).
- Why: Diagnose glaucoma from a fundus photograph and sparse clinical metadata
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. SMDG-19 (Kiefer et al. 2023) standardizes 19 public fundus datasets; source dataset is a natural group.
