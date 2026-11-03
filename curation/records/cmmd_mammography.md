---
unique_name: cmmd_mammography
name: Mammography CMMD
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
- https://doi.org/10.7937/tcia.eqde-4b16
- https://www.kaggle.com/datasets/nguynththanhho/cmmd-mammography
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12): CMMD is a mammography image database "for machine diagnosis of breast"; besides the image, MulTaBench's table holds age, side, the abnormality type read from the image and its own cropping method, so the image is the task.
- Source: Cui, Li, Cai, Fan, Zhang, Dan, Li and Wang, "The Chinese Mammography Database (CMMD): An online mammography database with biopsy confirmed types for machine diagnosis of breast", The Cancer Imaging Archive, 2021 (https://doi.org/10.7937/tcia.eqde-4b16): "we built a database conducted on 1,775 patients from China with benign or malignant breast disease who underwent mammography examination between July 2012 and January 2016. The database consists of 3,728 mammographies from these 1,775 patients, with biopsy confirmed type of benign or malignant tumors"; the TCIA page lists 5,202 images and clinical data in an XLSX (classification, molecular subtype for 749 patients, demographics). The Kaggle copy nguynththanhho/cmmd-mammography has no description. As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-cls-mammography-cmmd): 5,202 rows, `LeftRight`, `Age`, `Abnormality`, `Method_crop`, the lesion crop, target `Classification` (benign or malignant).
- Why out: the source's task is detection and diagnosis on the mammograms ("(1) Computer-aided detection for locating suspect lesions ... (2) Computer-aided diagnosis for characterizing the suspicious region of lesion ..."; SEL-8, SEL-12). Unlike `breast_cancer_prediction` (SEL-14), no BI-RADS reading ships, so nothing a tabular model would take remains: age, side and the lesion type (calcification, mass or both) are the whole table, and `Method_crop` is MulTaBench's processing.
- Siblings and duplicates: none (grep over the records for cmmd, chinese mammography). Siblings: `cbis_ddsm` (this run), `breast_cancer_prediction` (`Yes`, SEL-14), `mammography` (`No`, `Image`). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the TCIA collection page and its DataCite record; MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Table 11 (AUROC 0.770 frozen, 0.780 task-aware).
- Reject check (AI, 2026-10-31): stands. CMMD is 'an online mammography database with biopsy confirmed types for machine diagnosis of breast' for computer-aided detection and diagnosis (https://doi.org/10.7937/tcia.eqde-4b16), and TCIA lists its clinical data only as 'Classification, Molecular Test, Demographic' (https://www.cancerimagingarchive.net/collection/cmmd/): no BI-RADS reading ships, so the `breast_cancer_prediction` exception (SEL-14) and the `cbis_ddsm` route do not apply. Age, side and lesion type are the whole table; the molecular subtype is post-biopsy.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 5,202 rows; 4 structured, 0 text, 1 image features (MulTaBench Table 3); target: Malignant vs benign (binary).
- Why: Classify a cropped mammography lesion as malignant or benign from the crop, age, laterality and abnormality type
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. The Chinese Mammography Database (CMMD) on TCIA (Cui et al. 2021); Kaggle copy without description or licence.
