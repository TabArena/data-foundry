---
unique_name: chexpert_cardiomegaly
name: CheXpert
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
- https://arxiv.org/abs/1901.07031
- https://www.kaggle.com/datasets/ashery/chexpert
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-13): CheXpert was released "as a standard benchmark to evaluate performance of chest radiograph interpretation models", and MulTaBench's tabular columns besides sex, age and view are the other findings mined from the same radiology report as the target, a radiologist's reading of the same image.
- Source: Irvin et al., "CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison", AAAI 2019 (https://arxiv.org/abs/1901.07031, first version 2019-01-21): "We present CheXpert, a large dataset that contains 224,316 chest radiographs of 65,240 patients. We design a labeler to automatically detect the presence of 14 observations in radiology reports, capturing uncertainties inherent in radiograph interpretation." "We release the dataset to the public as a standard benchmark to evaluate performance of chest radiograph interpretation models." The Kaggle copy ashery/chexpert is "CheXpert-v1.0-small", downsampled. As used by MulTaBench (core image-tabular; https://huggingface.co/datasets/multabench/core-img-cls-chexpert): 46,437 images, `Sex`, `Age`, `Frontal/Lateral`, `AP/PA`, the 13 other labeler observations (`No Finding`, `Enlarged Cardiomediastinum`, `Lung Opacity`, `Edema`, `Pleural Effusion`, `Support Devices`, ...), the X-ray, target `Cardiomegaly` (positive, negative, uncertain).
- Why out: the task as published is reading the radiograph (SEL-8, SEL-12). The observation columns are the same report's reading of the same image (SEL-13), written at the same moment as the target, so no decision fits predicting one finding from the others (USE-2); SEL-14 does not apply, since no tabular model takes the other report findings to call cardiomegaly.
- Siblings and duplicates: none (grep over the records for chexpert, chest x-ray). External collections: MulTaBench (core image-tabular).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: Irvin et al. 2019 (abstract); the Stanford CheXpert page; MulTaBench (https://arxiv.org/abs/2605.10616), Table 3, Table 11.
- Reject check (AI, 2026-10-31): stands. Irvin et al.: 'We design a labeler to automatically detect the presence of 14 observations in radiology reports' and release the data 'as a standard benchmark to evaluate performance of chest radiograph interpretation models' (https://arxiv.org/abs/1901.07031): the 13 observation columns are the same report's reading of the same radiograph as the target. SEL-14 keeps readings that tabular models take in practice to make the call, and no cardiomegaly model takes the other report findings; sex, age and view are all that remain.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 46,437 rows; 17 structured, 0 text, 1 image features (MulTaBench Table 3); target: Cardiomegaly label: positive, negative or uncertain (3 classes).
- Why: Classify the Cardiomegaly finding of a chest X-ray from the image, sex, age and the other report labels
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Irvin et al. AAAI 2019; Kaggle copy is CheXpert-v1.0-small. Labels are mined from radiology reports by the CheXpert labeler; the co-occurring pathology features come ...
