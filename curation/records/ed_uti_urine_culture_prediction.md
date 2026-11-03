---
unique_name: ed_uti_urine_culture_prediction
name: Predicting urinary tract infections in the emergency department with machine learning (Taylor et al. 2018), minimal dataset S1 File
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2018'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1371/journal.pone.0194085
- https://api.figshare.com/v2/articles/5959417
- https://ndownloader.figshare.com/files/10679215
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 80,387 adult ED visits with a urine culture from four EDs of one US health system, a measured target, features known in the ED and the full minimal dataset in the paper's supplement; the ED diagnosis and treatment columns that ship with it have to go.
- Source: Taylor, Moore, Cheung and Brandt, "Predicting urinary tract infections in the emergency department with machine learning", PLOS ONE 13(3):e0194085, 2018 (doi:10.1371/journal.pone.0194085); S1 File, the minimal de-identified dataset (CSV, 85.7 MB on figshare, https://ndownloader.figshare.com/files/10679215). Data availability: "All relevant data are within the paper and its Supporting Information files." As published: 80,387 visits of 55,365 patients, March 2013 to May 2016, adults with a urine culture and symptoms that may be due to UTI; 220 columns (header read from a preview): `ID`, `PATID`, target `UCX_abnormal`, urinalysis (`ua_*`), symptom and exam flags, `chief_complaint`, demographics, `arrival` (mode), vitals (`Temp_First` to `GCS_Last`), labs, past history groups, outpatient medication classes, and `disposition`, `abx`, `dispo`, `UTI_diag`, `split`, `abxUTI`, `alt_diag`. Target: "The primary outcome for all analyses was the presence of a positive urine culture" (above 10^4 CFU; "Mixed flora results were only considered positive if there was the presence of Escherichia coli").
- Use case: the ED clinician, before admission or discharge and while the culture is pending, decides whether to diagnose and treat a UTI (the paper compares the models with the clinicians' diagnosis); fit direct: "Only data available during the ED visit until the time of admission or discharge were used as prediction variables"; regime grouped by patient (`PATID` ships, 1.45 visits per patient, no visit date); the paper split visits at random, 80/20.
- Siblings and duplicates: `acute_inflammations` (`TBD -> 2nd Tier`, 120 rows, likely generated, the record this was found for); `southern_denmark_hospital_uti` (infection during a hospital admission, Danish region) and `amr_uti_antibiotic_resistance` (resistance of a positive culture, MGH and BWH): other tasks and cohorts (PROV-7); `nigeria_febrile_disease_diagnosis` names UTI among other diagnoses. External collections: none found.
- Better data: found as better data for `acute_inflammations` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the PLOS ONE paper (Methods; Results: XGBoost AUC 0.904 with all variables, 0.877 with the reduced set of 10).
- Metric: ROC AUC, by which the paper compares and ranks its models (Abstract, Results), with sensitivity, specificity and likelihood ratios at a chosen cut-off beside it; a deliberate choice (MET-5); inputs none.
- Risks for /add-dataset: drop the post-decision columns `UTI_diag`, `alt_diag`, `abxUTI`, `abx`, `disposition` and `dispo` (the paper excluded ED medications and the ED diagnosis from its predictors; LEAK-10), the paper's `split`, and `PATID` as a feature (LEAK-33); the vitals look coded (small integers in `Temp_First` in the preview): read the S1 codebook before use (LEAK-2); repeat visits per patient (SPLIT-26); the cohort is visits with a culture sent, which is how the label exists (no `Selection Bias` marker).
- Priority: gap 0 (medical and binary are not thin), use case + (the ED diagnosis named by the paper, direct fit), source + (peer-reviewed paper with the data in its supplement), shape + (80k visits, 200+ mixed features, patient groups), risk - (diagnosis and treatment columns in the release).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `acute_inflammations`.
- as published: Adult ED visits: 80,387 visits of 55,365 patients (from 560,515 ED visits), four EDs of one US health system, March 2013 to May 2016; S1 File.csv is 85.7 MB (figshare file listing); column count not ...; target: Positive urine culture (the gold standard for UTI), binary; the paper also compares the models with the ED provider's UTI diagnosis; access: open.
- Why: The task acute_inflammations stands for (presumptive diagnosis of a urinary tract inflammation from symptoms and simple findings) with a measured label instead of the rule-like, likely generated one; features of the same kind (symptoms, temperature and vitals, urinalysis and dipstick, history) known in the ED before ...
- Adds: Real, traceable patient data instead of a suspected generated table (the record's AHDS and Trivial markers); 80,387 visits against 120 rows; a culture label; data paper states all data are in the supplement
