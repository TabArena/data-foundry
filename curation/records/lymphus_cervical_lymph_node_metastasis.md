---
unique_name: lymphus_cervical_lymph_node_metastasis
name: 'LymphUs: multicenter open-access lymph node ultrasound database in papillary thyroid carcinoma (images plus 16 radiologist-recorded features)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: Website
year: '2026'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.1016/j.dib.2026.112694
- https://qamebi.com/cervical-lymph-node
- https://www.kaggle.com/datasets/aliabbasianardakani/a-multicenter-lymph-node-ultrasound-image-database
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 338 papillary-thyroid-cancer patients from two centres, one cervical lymph node each with radiologist-recorded ultrasound features and an FNA-confirmed label; a real pre-operative staging decision, but tiny, an image database first, and the features are a reader's view of the image.
- Source: Mohammadi, Abbasian Ardakani et al., "LymphUs: A multicenter open-access database ...", Data in Brief 2026:112694 (doi 10.1016/j.dib.2026.112694; ScienceDirect returned 403, not read), and Abbasian Ardakani et al., Journal of Ultrasound in Medicine 2023, 42(6):1211-21 (doi 10.1002/jum.16131, the earlier study of the data, not read). Download page https://qamebi.com/cervical-lymph-node (read): "Ultrasound imaging was performed on PTC patients at two independent clinical centers using standardized acquisition protocols"; Center 1: 180 patients (81 malignant, 99 benign), Center 2: 158 (82 malignant, 76 benign); ultrasound images with segmentation masks, "semantic features and expert annotations"; CC BY-NC 4.0 (the Kaggle copy says CC BY 4.0 and holds only two preview JPGs). The 16 features the run's note lists (maximum and minimum diameter, aspect ratio, echogenicity, ...) were not seen.
- Use case: a radiologist or thyroid surgeon decides before surgery whether a suspicious node is metastatic (FNA, neck dissection); the source names "preoperative LN staging and treatment planning" (Kaggle description); fit approximate: the label is FNA-confirmed, but only nodes already suspected were included. Regime: grouped by centre would leave two groups; IID within the pooled set is the likely call (the add stage decides).
- Siblings and duplicates: `lymphography` (Lennart `No`: `Outdated`, `Trivial`, `Tiny Data`; 148 lymphograms of 1988, four classes); thyroid records (`differentiated_thyroid_cancer_recurrence`, a recurrence task; `new_thyroid`, `thyroid_discordant`): other tasks. No duplicate. External collections: none found.
- Better data: found as better data for `lymphography`; no further search this round.
- Papers and pages: the Data in Brief article (its summary in the Kaggle description), the JUM 2023 study (not read), the download page.
- Metric: none found (the download page and the Kaggle description; the papers not read), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the semantic features are a radiologist's reading of an ultrasound image: in scope only under SEL-14 if lymph-node reporting criteria use them as tabular inputs in practice, otherwise `Image` (SEL-13); 338 patients with 163 malignant, so a few dozen positives per test fold (TP-5 holds, `Tiny Data`); the run's note reads large class gaps in centre 1 in the paper's Table 1 (minimum diameter 10.6 against 3.4 mm, hyperechoic 57% against 1%), the `Trivial` call of `lymphography` to probe (TP-4); centre differences in reading (LEAK-13); the layout of the feature file is unknown.
- Priority: gap 0 (medical not thin), use case + (the source names pre-operative staging and treatment planning), source + (a data paper and an earlier clinical study), shape 0 (338 patients, 16 features), risk - (image-derived features, tiny, possibly trivial).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `lymphography`.
- as published: 338 patients, one lymph node each, two centres: 180 (81 malignant, 99 benign) and 158 (82 malignant, 76 benign); 16 imaging features in Excel (max/min diameter, aspect ratio, echogenicity, ...; target: lymph node malignant (metastatic) or benign/reactive, confirmed by fine-needle aspiration; access: open (free for research; Kaggle copy by the first author).
- Why: the modern form of lymphography's task: diagnose a lymph node from an imaging reader's coded findings (lymphography itself is obsolete)
- Adds: newer (2026 against 1988), more patients (338 against 148), biopsy-confirmed label, a centre-grouped split; but binary instead of 4 classes, still tiny, and Table 1 shows wide gaps (min diameter 10.6 vs 3.4 mm, hyperechoic 57% vs 1% in centre 1), so it may be as easy as the record (Trivial)
