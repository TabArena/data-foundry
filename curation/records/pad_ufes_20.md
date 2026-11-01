---
unique_name: pad_ufes_20
name: PAD-UFES Lesions
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Class-dependent Recording
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Other
year: '2020'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.dib.2020.106221
- https://www.kaggle.com/datasets/mahdavi1202/skin-cancer
- https://arxiv.org/abs/2605.10616
- https://data.mendeley.com/datasets/zr7vgbcyr2/1
- https://huggingface.co/datasets/multabench/extended-img-cls-pad-ufes-lesion
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: PAD-UFES-20 (Pacheco et al. 2020), 1,641 skin lesions of 1,373 patients of a Brazilian public dermatology programme, with up to 21 clinical features, a smartphone photo and a six-class diagnosis; the clinical features score at least as well as the photo (MulTaBench Table 8), partly through a class-dependent recording that has to be fixed: the patient features are missing only for the three benign classes.
- Source: Pacheco et al., "PAD-UFES-20: A skin lesion dataset composed of patient data and clinical images collected from smartphones", Data in Brief 32:106221 (2020, doi:10.1016/j.dib.2020.106221; PMC7479321), data on Mendeley (doi:10.17632/zr7vgbcyr2.1, 7 July 2020, CC BY 4.0). Collected "during 2018 and 2019" (Sec. 2.3) in 11 cities of Espírito Santo by the PAD programme of UFES, which "provides free skin lesion treatment, in particular, to low-income people who cannot afford private treatment" (Sec. 2); patients see "a group of up to three senior dermatologists" (Sec. 2.2). As published: `metadata.csv`, 2,298 rows (one per image) x 26 columns (patient and lesion ids, smoking, drinking, parents' background, age, pesticide, gender, skin cancer and cancer history, piped water, sewage, Fitzpatrick type, region, two diameters, itch, grew, hurt, changed, bleed, elevation, image id, `biopsed`, `diagnostic`) and the photos; images per class BCC 845, ACK 730, NEV 244, SEK 235, SCC 192 (Bowen's disease merged into it), MEL 52. MulTaBench (extended, https://huggingface.co/datasets/multabench/extended-img-cls-pad-ufes-lesion) keeps one row per lesion (1,641) and drops `biopsed` as a leak.
- Use case: the source aims at "new tools to assist clinicians to detect skin cancer" from smartphone data where dermatologists are scarce: at the appointment a clinician decides whether a lesion is a cancer that needs a biopsy. Fit approximate for a table without the photo the clinician also sees. Regime grouped by patient ("A patient may have one or more skin lesions and a skin lesion may have one or more images", Sec. 1.2).
- Siblings and duplicates: none for this data (grep for pad-ufes, skin, lesion, the Kaggle slug and the Mendeley DOI). `ham10000_lesions` (HAM10000, dermatoscopic images with age, sex and body site only; MulTaBench) is another dataset of a related task. External collections: MulTaBench (extended image release).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Data in Brief paper (no model results; Sec. 2.4 validates the biopsy share); Pacheco & Krohling, "The impact of patient clinical information on automated skin cancer detection", Comput. Biol. Med. 116:103545 (2020, doi:10.1016/j.compbiomed.2019.103545), abstract: "an improvement of approximately 7% in balanced accuracy" from the clinical data (full text paywalled, not read); MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix F.1, Table 8 (structured AUC 0.921, image 0.896, joint 0.950), Table 9.
- Metric: none in the data paper; the companion study's headline is balanced accuracy, a threshold metric with no threshold or costs fixed and, from the abstract, one of several (MET-5, MET-6; full text not read), so the fallback `log_loss` on the six classes; no extra inputs beyond the patient id for the split.
- Risks for /add-dataset: class-dependent recording, measured on the published `metadata.csv`: the 13 patient columns (smoking to the diameters) are missing, in whole or in part, for 824 of 2,298 images (36%; 507 of 1,641 lesions), all of them ACK, NEV or SEK, while BCC, SCC and MEL have none missing (the paper: these "depend on the patient's answers during the appointment", Sec. 1.2.2), so missingness gives "benign" away (LEAK-13: keep complete rows or drop those columns); `biopsed` marks every cancer ("all samples diagnosed as skin cancer are proved by biopsy", Sec. 2.3; drop); ACK, NEV and SEK labels are mostly a dermatologists' consensus (USE-5); several images per lesion collapse to one row; split by `patient_id`; the photo is dropped (SEL-12).
- Priority: gap + (multiclass, 24 accepted datasets, thin), use case 0 (the source's actor also has the photo; fit approximate), source + (a data paper and a Mendeley DOI), shape + (1,641 lesions, 21 mixed features, grouped by patient), risk - (class-dependent missingness, the dropped photo).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,641 rows; 21 structured, 0 text, 1 image features (MulTaBench Table 9); target: Diagnosis (6 classes).
- Why: Diagnose a skin lesion from a smartphone photo and patient clinical data
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. PAD-UFES-20 (Pacheco et al. 2020, Data in Brief, CC BY); several images per ...
