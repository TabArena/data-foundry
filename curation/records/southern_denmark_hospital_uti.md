---
unique_name: southern_denmark_hospital_uti
name: Prediction of hospital-acquired urinary tract infection at admission, Region of Southern Denmark
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2021'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.6djh9w107
- https://doi.org/10.1371/journal.pone.0248636
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and papers, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 301,932 adult admissions to the four public somatic hospital trusts of the Region of Southern Denmark (January 2017 to May 2018), released CC0 on Dryad with a PLOS ONE paper, to predict at admission whether a UTI is detected during the stay; a large, documented early-warning task, with the admission-day labs and text-mined flags to check against community-acquired cases.
- Source: Møller, Sørensen and Hardahl, "Prediction of risk of acquiring urinary tract infection during hospital stay based on machine-learning: A retrospective cohort study", PLOS ONE 16(3):e0248636 (2021-03-31); data on Dryad (doi 10.5061/dryad.6djh9w107, published 2021-03-14, CC0 per the Dryad API): `UTIEntryModel2017to2018Dataset.xlsx` (18.1 MB) and `UTIEntryModel2017to2018readme.txt` (5 KB; not readable here, Dryad's file download refused the request). As published (Dryad page): the entry model's data, target "any urinary tract infection (UTI) detected during admission" (yes = 1, no = 0); the only usage note says the hospital id is missing for 240 of 301,932 admissions. The paper: outcomes from the region's HAIR surveillance system ("The algorithms for UTI are based on modified CDC definitions", combining clinical features, a significant urine culture and UTI-specific antibiotics, Sec. 2.3); a UTI found within 48 h of admission is community-acquired, later hospital-acquired; ICU admissions excluded; predictors are demographics, laboratory results, antibiotics, past ICD-10 diagnoses, the infection registry and UTI signs text-mined from the clinical narrative with negation handling (Sec. 2.4; Table 2 is an image, not read); 284,293 admissions in training and validation, 17,768 (6.3%) with a UTI.
- Use case: ward staff flag patients at admission for preventive measures: the aim is "a real-time early warning system for individualized prevention of UTI in hospitalized patients" (Introduction) that lets staff "identify patients at high risk of acquiring a UTI during admission" (Discussion), with a prospective pilot (72% of hospital-acquired cases scored 0.15 or more at admission); fit direct for the entry model (t = 0). Regime: the paper splits January 2017 to April 2018 at random (60/40, stratified) and tests on May 2018; temporal if an admission date ships, and grouped by patient if a patient id ships and patients return within the 16 months (neither checked: the readme was not read).
- Siblings and duplicates: `ed_uti_urine_culture_prediction` (emergency-department urine culture), `amr_uti_antibiotic_resistance` (resistance of a diagnosed UTI), `nigeria_febrile_disease_diagnosis`: other sources and tasks (PROV-7). No record of this source (grep: urinary tract, hospital-acquired, nosocomial, Southern Denmark, the Dryad DOI). External collections: none found.
- Better data: from the curator's Zotero collection (item 155, the Dryad record); no further search this round.
- Papers and pages: Møller et al. 2021 (the data and the task); the Dryad record.
- Metric: "The primary assessment metric used is average squared error on validation data" (Sec. 2.5, the champion-model criterion of SAS Enterprise Miner), with the ROC index (AUC 0.82 to 0.84 for the entry model) and cumulative lift also reported. On a 0/1 target the average squared error is the Brier score, a strictly proper rule named as the primary criterion (MET-5); the v2 metric module has no Brier scorer, so the add stage either adds one (MET-13) or declares `roc_auc`, which the paper also reports: a call for the curator. Inputs none.
- Risks for /add-dataset: the entry target counts community-acquired UTIs found within 48 h, so admission-day laboratory results (a urine culture or dipstick) and text-mined UTI signs from admission notes may be part of the work-up of exactly those cases: check what each column holds and when it is recorded (USE-3, LEAK); the paper's second model (hospital-acquired UTI, predicted at 48 h) is another framing that this file may not support (USE-5); the column list, a date and a patient id are unread (the readme); the HAIR algorithm (S1 Table) defines the label.
- Priority: gap 0 (medical & healthcare and binary classification are not thin), use case + (the paper names ward staff and the preventive action, with a pilot), source + (a peer-reviewed paper and a CC0 release with a readme), shape + (301,932 admissions with labs, history, antibiotics and text flags), risk - (admission-day columns may carry the work-up of community-acquired cases).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 155: "Dryad | Publish and preserve your data".
- as published: 301,932 adult admissions at the region's four public somatic hospital trusts over 16 months from January 2017; one 18 MB xlsx (UTIEntryModel2017to2018Dataset) with a readme; target: any urinary tract infection detected during the admission (binary); access: open.
- Why: Large, CC0 and real, from a regional data warehouse. The entry model uses only data known at admission: demographics, labs, antibiotics, past ICD-10 codes, an infection registry and text-mined EMR flags.
- Adds: A public hospital-acquired infection task at scale; the comparable MIMIC and eICU tasks are credentialed. Check the text-mined flags and the 'during admission' timing for leakage.
