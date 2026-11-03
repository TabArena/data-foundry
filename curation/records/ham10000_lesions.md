---
unique_name: ham10000_lesions
name: HAM10000 Lesions
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
- https://doi.org/10.1038/sdata.2018.161
- https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Image`, SEL-12): dermatoscopic images released because "Training of neural networks for automated diagnosis of pigmented skin lesions is hampered by the small size and lack of diversity of available datasets of dermatoscopic images"; MulTaBench's own numbers show the image decides (AUROC 0.949 from the image, 0.798 from age, sex and site).
- Source: Tschandl, Rosendahl and Kittler, "The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions", Scientific Data 5, 180161 (2018), <https://doi.org/10.1038/sdata.2018.161>; data on Harvard Dataverse (doi 10.7910/DVN/DBW86T) and as the ISIC 2018 Task 3 training set: "The final dataset consists of 10015 dermatoscopic images which are released as a training set for academic machine learning purposes". The metadata file has `lesion_id`, `image_id`, `dx` (7 classes), `dx_type` (how the diagnosis was confirmed), `age`, `sex`, `localization`. As MulTaBench ships it (extended release, Table 9): 7,470 rows (HAM10000 has 7,470 lesions, so one image per lesion, it seems), `age`, `sex`, `localization` and one image, target `dx`; it dropped `dx_type` "because it leaks the label".
- Use case: a dermatologist triages a pigmented lesion from its dermatoscopic image; the diagnosis is an image call, and age, sex and site are context; regime grouped by lesion (several images per lesion).
- Siblings and duplicates: `pad_ufes_20` (smartphone photos of skin lesions with clinical metadata, another MulTaBench record from another source, screened in another batch). External collections: MulTaBench (extended release); ISIC 2018 Task 3.
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: Tschandl et al. 2018; Codella et al. 2019 (ISIC 2018 challenge, arXiv 1902.03368); the Kaggle mirror (kmader); MulTaBench (arXiv 2605.10616, Appendix F.1, Table 8).
- Metric: ISIC 2018 Task 3 ranked by balanced multiclass accuracy (the challenge's choice; its page was not re-read); MulTaBench scores AUROC.
- Risks for /add-dataset: not applicable.
- Reject check (AI, 2026-10-31): stands. Tschandl et al. release HAM10000 because 'Training of neural networks for automated diagnosis of pigmented skin lesions is hampered by the small size and lack of diversity of available datasets of dermatoscopic images' (https://doi.org/10.1038/sdata.2018.161; arXiv 1803.10417): the diagnosis is made from the image, and age, sex and site alone make no clinical task. MulTaBench's 0.798 against 0.949 is another benchmark's score (EV-4), context only.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 7,470 rows; 3 structured, 0 text, 1 image features (MulTaBench Table 9); target: Diagnosis (7 classes).
- Why: Diagnose a pigmented skin lesion from a dermatoscopic image, age, sex and localization
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Tschandl et al. 2018 (Harvard Dataverse doi:10.7910/DVN/DBW86T, ISIC 2018). ...
