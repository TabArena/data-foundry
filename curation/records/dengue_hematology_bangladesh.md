---
unique_name: dengue_hematology_bangladesh
name: Bangladesh dengue haematology datasets (Jamalpur 2024, Mendeley 6fsrsk3mb8; Dhaka 2025, Mendeley jsbmtk8hty)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17632/6fsrsk3mb8.2
- https://doi.org/10.1016/j.dib.2025.111664
- https://doi.org/10.17632/jsbmtk8hty.4
- http://arxiv.org/abs/2610.14813
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: two small, separate Bangladeshi hospital releases (1,523 patients in Jamalpur 2024, 1,329 in Dhaka 2025) of a full blood count with a dengue test result; the test behind the 2024 label and who was tested are not described, and the 2024 red-cell indices do not agree with each other in a preview (a PROV-3 check first).
- Source: (a) Nirob, Siam, Bishshash, Assaduzzaman, "Dengue Fever Hematological Dataset: Clinical Insights for Improved Diagnosis and Patient Management", Mendeley Data doi 10.17632/6fsrsk3mb8 (v2 published 2025-02-04, CC BY 4.0): "Data were collected from 1,523 patients at Jamalpur 250-Bedded General Hospital in Jamalpur, Bangladesh, from February 10, 2024, to September 27, 2024"; one CSV, 1,523 x 19 (header read 2026-10-31: gender, age, haemoglobin, neutrophils, lymphocytes, monocytes and eosinophils in %, RBC, HCT, MCV, MCH, MCHC, RDW-CV, platelet count per cumm, MPV, PDW, PCT, WBC per cumm, Result positive/negative). Data paper: Nirob et al., "A comprehensive hematological dataset for dengue incidence in Bangladesh", Data in Brief 60:111664 (2025; PMC12159883): "Data were collected from 1523 Dengue patients admitted to Jamalpur Medical College Hospital" (Specifications Table), the result was found "using standardized diagnosis tests" with the test unnamed. (b) Thakur, Nasrin, "Comprehensive Dengue Hematology and Clinical Dataset from Bangladesh for Machine Learning and Diagnostic Research", Mendeley Data doi 10.17632/jsbmtk8hty (v4 published 2025-11-17, CC BY 4.0): "1,329 Dengue patients across several medical institutions in Dhaka", July to November 2025, 12 columns (SN, age, sex, Dengue NS1 as the class label, PLT, WBC, HCT, RBC, lymphocyte and neutrophil %, ALT, AST; ALT and AST mostly empty in the preview).
- Use case: a clinician at a district hospital, with a febrile patient's full blood count, decides whether to manage the patient as dengue before or without an NS1 or serology result (the data paper: "create and validate predictive models" that could "facilitate the early identification of dengue infection", Value of the data); fit approximate (an unnamed test in (a), NS1 misses later-stage infections in (b), and the tested population is not described); regime IID within a set; the two sets allow a cross-site, cross-year check, as arXiv 2610.14813 does (per the run's first pass).
- Siblings and duplicates: `sinan_dengue_case_screening` (Brazil's SINAN notifications with symptoms and comorbidities, another source and feature kind; from the same Zotero item). The two releases here have different authors, hospitals and years: two sources in one record, not versions of one (PROV-4). No other record of either set (grep: dengue). External collections: none found.
- Better data: from the curator's Zotero collection (item 303); no further search this round.
- Papers and pages: the Data in Brief paper (t and z tests of each index against the result); arXiv 2610.14813 (2026, the Zotero item; AUC 0.90 on the 2025 set against 0.66 on the 2024 set per the run's first pass, not re-read).
- Metric: none found from the source (the data paper reports significance tests only; the arXiv paper was not re-read), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: PROV-3 first: in the first 15 rows of (a), MCHC differs from haemoglobin / HCT x 100 by up to 5.6 g/dL (14.5 g/dL and HCT 41.06% give 35.3, the file says 29.7), though an analyser computes it from those two, and RBC is given in whole numbers (5, 5, 5, 4, ...); described as "dengue patients" yet with 31.5% negatives (run's first pass), so the selection and the label are undocumented (USE-5, PROV-2); one record holds two sources: split them or pick one (PROV-4); units differ between the sets (per cumm against K/µL); both are small (TP-5 is not at risk, but the signal may be weak, as the 0.66 suggests).
- Priority: gap 0 (medical, binary not thin), use case 0 (the data paper's aim is general), source + (a data paper for (a), Mendeley descriptions for both), shape + (1,523 and 1,329 patients, 17 and 10 inputs), risk - (an undocumented label and selection, and internal inconsistencies to check against PROV-3).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 303: "Machine Learning-Based Prediction of Dengue Infection Using Clinical and Hematological ...".
- as published: 1,523 patients x 19 at Jamalpur, Feb-Sep 2024: age, sex, full blood count with 16 indices, Result. The hospital is named 'Jamalpur 250-Bedded General Hospital' on Mendeley and 'Jamalpur Medical ...; target: dengue test result, positive or negative (NS1 in the 2025 set; the 2024 description does not name the test); access: open.
- Why: Real hospital data, with a data paper for the 2024 set; two hospitals and years allow external validation, which is what the paper does.
- Adds: Small, with quality questions. The 2024 set is described as 'patients diagnosed with dengue fever' yet 31.5% are negative. The 2025 set has unit inconsistencies and RBC outliers, and the paper reaches AUC 0.90 on it vs 0.66 on 2024. Two separate sources, not versions. A third set (Assaduzzaman 2024, Mendeley ...
