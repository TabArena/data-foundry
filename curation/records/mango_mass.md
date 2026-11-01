---
unique_name: mango_mass
name: Mango Mass
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
- https://ieeexplore.ieee.org/abstract/document/9918807
- https://www.kaggle.com/datasets/mypapit/mangomassnet552-dataset
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12): MangoMassNet-552 was published as an image dataset for estimating a mango's mass from its photo; the only other columns are a colour group and a grade, so without the image no tabular task is left.
- Source: Ismail & Wagimin, MangoMassNet-552 (Kaggle mypapit/mangomassnet552-dataset, files of 2022-07-26, CC BY-SA 4.0, doi:10.34740/KAGGLE/DSV/3987156), with the paper Ismail, Wagimin & Razak, "Estimating Mango Mass from RGB Image with Convolutional Neural Network", AiDAS 2022, pp. 105-110 (doi:10.1109/AiDAS56890.2022.9918807). As published: 552 JPEG images of 276 Harumanis mangoes (two photos each) from the FAMA collection centre in Perlis, `Harumanis_mango_weight_grade.xlsx` with four columns (`Fruit No` = the image file, `Color` K yellow or P green, `Fruit Grade` per MS 885:2012, `Mass` in kg) and `Harumanis_mango_weight.csv` (`no`, `weight`). README: "The dataset was created because there was no freely available Mango image dataset which includes mango images, its grade and mass/weight"; "the A4 paper is used as a visual cue for mass estimation".
- Use case: grading or sorting mangoes by mass from a photo; the decision rests on the image, which is the task as published.
- Siblings and duplicates: none (grep for mango and the Kaggle slug; `mango_dmc_nir`, NIR spectra for dry matter, is another task). External collections: MulTaBench (core image set; its Appendix B.1 names the Kaggle slug saurabhshahane/mango-varieties-classification, a different mango dataset, while the repository's source list and the Hugging Face card https://huggingface.co/datasets/multabench/core-img-reg-mango-mass name mypapit/mangomassnet552-dataset: a slip in the paper, PROV-15).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page and README; the AiDAS 2022 paper (title and citation; text not read); MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix B.1 (the image is "the dominant signal for weight prediction"), Table 3 (546 rows; 2 structured, 0 text, 1 image), Table 11 (frozen R² 0.533, task-aware 0.653).
- Metric: not needed for a reject.
- Why `No`: SEL-12 (Must), a non-tabular modality where image models are clearly the tool: the table without the photo is 276 fruits with two categorical columns, one of which, the MS 885:2012 grade, may itself follow the fruit's size (not checked).
- Reject check (AI, 2026-10-31): stands. The uploaders: 'The dataset was created because there was no freely available Mango image dataset which includes mango images, its grade and mass/weight' and 'the paper is used as visual cue for mass estimation'; the paper is 'Estimating Mango Mass from RGB Image with Convolutional Neural Network' (https://www.kaggle.com/datasets/mypapit/mangomassnet552-dataset). Without the photo, 276 fruits with a colour group and an MS 885:2012 grade remain: a size grade follows the mass (SEL-5), a quality grade is the grader's look at the fruit, so no tabular task either way.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 546 rows; 2 structured, 0 text, 1 image features (MulTaBench Table 3); target: Fruit mass (kg).
- Why: Estimate a Harumanis mango's mass from its photo, colour group and grade
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. MangoMassNet-552 (FAMA Perlis, Malaysia; Kaggle 2022, paper 'Mango Mass Estimation from RGB Image with CNN'). The image is the main signal; tiny.
