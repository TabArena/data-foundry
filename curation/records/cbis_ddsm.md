---
unique_name: cbis_ddsm
name: CBIS-DDSM
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Other
year: '2016'
domain: medical & healthcare
source_links:
- https://doi.org/10.1038/sdata.2017.177
- https://www.kaggle.com/datasets/awsaf49/cbis-ddsm-breast-cancer-image-dataset
- https://arxiv.org/abs/2605.10616
- https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY
- https://huggingface.co/datasets/multabench/core-img-cls-cbis-ddsm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: MulTaBench's target, breast density from the mass descriptors, is a reading no decision rests on; the source's own diagnosis label, biopsy-verified pathology from the BI-RADS descriptors, may be a tabular task under SEL-14 (`breast_cancer_prediction`), with the image dropped.
- Source: CBIS-DDSM on The Cancer Imaging Archive (https://doi.org/10.7937/K9/TCIA.2016.7O02S9CY, 2016): "an updated and standardized version of the Digital Database for Screening Mammography (DDSM)", "a subset of the DDSM data selected and curated by a trained mammographer"; paper Lee et al., "A curated mammography data set for use in computer-aided detection and diagnosis research", Sci Data 4:170177, 2017 (https://pmc.ncbi.nlm.nih.gov/articles/PMC5735920/): 753 calcification and 891 mass cases (Table 3: 970 mass and 1,045 calcification abnormalities); CSV columns patient id, breast density, side, view (CC or MLO), abnormality number, mass shape and margin, calcification type and distribution, BI-RADS assessment, pathology ("Benign, Benign without call-back, or Malignant"), subtlety ("Radiologists' rating of difficulty in viewing the abnormality in the image"), image paths; a 20% test split balanced by BI-RADS category. Mass and calcification cases are separate tables with different descriptor columns. As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-cls-cbis-ddsm): 1,696 mass rows, one per image, so the CC and MLO views of one lesion are two rows with the same descriptors; target `breast_density` (4 classes); features side, view, abnormality id, mass shape, margins, assessment, pathology, subtlety and the crop.
- Use case: MulTaBench's density target has none: the radiologist reads density from the same mammogram at the same time as the mass descriptors. The source's diagnosis label fits a radiologist deciding on biopsy from the BI-RADS reading, as decision-support models on BI-RADS descriptors do; fit approximate (DDSM cases were selected as normal, benign and malignant, and the descriptors are readings of the image). Regime grouped by woman (1,566 participants per the TCIA page, several abnormalities each, two views per lesion).
- Siblings and duplicates: no duplicate (grep over the records for cbis, ddsm). Siblings: `breast_cancer_prediction` (`Yes`; CC 2026-10-15, Lennart: "The BI-RADS readings are valid tabular inputs: screening programmes run tabular risk models on them"), `bcsc_risk_estimation` (this run), `breast_w` (`No`, a pathologist's grades of a slide, SEL-13), `mammography` (`No`, `Image`), `cmmd_mammography` (this run, an image task). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: Lee et al. 2017 (above, read through PMC); the TCIA collection page; MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Table 11 (AUROC 0.858 frozen, 0.893 task-aware, for the density target).
- Metric: none found for a tabular task (Lee et al. release the data for the evaluation of image CADe and CADx systems; their baselines were not read; MulTaBench's AUROC is benchmark-wide and for density), so the fallback `roc_auc` for pathology (MET-1, MET-5); inputs none, the patient id ships as the group.
- Risks for /add-dataset: the target moves from MulTaBench's density to the source's pathology (USE-5, TP-7); the descriptors are a radiologist's reading of the image and stay in scope only under SEL-14, the open point as for `breast_w` (SEL-13); the BI-RADS assessment nearly decides the biopsy and so the label (TP-4: check the assessment alone); "Benign without call-back" as a class; one row per lesion rather than per view; the mass and calcification tables have different columns; DDSM's case selection (`Selection Bias`).
- Priority: gap 0 (medical & healthcare has 44 accepted datasets, binary is not thin), use case 0 (the source's use is image CAD), source + (a TCIA collection and a Sci Data paper), shape + (about 2,000 abnormalities in 1,566 women, mixed categorical and ordinal columns, grouped), risk - (the SEL-13 boundary, a re-framed target, the assessment as a near-label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,696 rows; 8 structured, 0 text, 1 image features (MulTaBench Table 3); target: BI-RADS breast density (4 classes).
- Why: Classify breast density of a cropped mammography mass from the crop and the lesion annotations
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Lee et al. 2017 (TCIA doi 10.7937/K9/TCIA.2016.7O02S9CY). Structured features are radiologist annotations (shape, margins, assessment, pathology, subtlety).
