---
unique_name: nhanes_liver_elastography_fibrosis
name: NHANES Liver Ultrasound Transient Elastography (P_LUX 2017-March 2020, LUX_L August 2021-August 2023) with the standard biochemistry profile
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
year: '2022'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_LUX.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/LUX_L.htm
- https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/LUX_J.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: FibroScan liver stiffness and CAP measured on every NHANES participant aged 12 and over in 2017-2023 (15,303 complete exams), with the routine liver panel; the label is a cut-off we choose, and the liver disease here is mostly fatty liver, not hepatitis.
- Source: CDC/NCHS NHANES Liver Ultrasound Transient Elastography files: P_LUX (2017-March 2020, first published January 2022) 10,409 records, 9,023 complete exams, 9,700 with median stiffness (LUXSMED, kPa) and 9,698 with median CAP (LUXCAPM, dB/m); LUX_L (August 2021-August 2023, first published September 2024) 7,199 records, 6,280 complete; "All participants 12 years and older ... were eligible". Joined by SEQN to the biochemistry profile (ALT, AST, GGT, ALP, bilirubin, albumin, total protein), the blood count (platelets), body measures and questionnaires.
- Use case: a primary-care physician with a routine liver panel decides whether to refer for elastography or to hepatology (the FIB-4 triage); fit approximate: the label is the elastography reading at a cut-off we pick, not a diagnosis; regime temporal by wave (2017-2020, then 2021-2023).
- Siblings and duplicates: `indian_liver_patient_dataset` (`Yes`, 583 hospital patients, Selection Bias), `hepatitis_c_prediction` (`Yes`, donors and patients collected apart), `hepatitis_c_egypt` (`No`, AHDS); `halt_c_hcv_cirrhosis_labs` and `gut_cirrhosis_metaml` (other liver tasks, not compared in detail); the NHANES III steatosis re-read noted on `nhanes_iii_gallstones` is an older fatty-liver sibling. External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `hepatitis_c_egypt`, `hepatitis_c_prediction` and `indian_liver_patient_dataset`; no further search this round.
- Papers and pages: the P_LUX, LUX_L and LUX_J pages; P_LUX cites the device's accuracy in the literature (AUC 0.89 for severe fibrosis, 0.81 for steatosis), not a prediction task; no paper defining the task on these files was looked up (search unavailable).
- Metric: none found, so the fallback `roc_auc` for a binary cut-off, or `rmse` on stiffness (MET-8); inputs none.
- Risks for /add-dataset: the target (stiffness of 8 kPa or more for significant fibrosis, or a CAP cut-off for steatosis; USE-5), with advanced fibrosis a few percent; filter on LUAXSTAT, since the file keeps exams that miss the quality criteria and "some extreme values may be present"; FIB-4 and the NAFLD fibrosis score are computed from the features, so a score baseline is cheap (TP-4 check); joins across four files per wave; survey weights not used.
- Priority: gap 0, use case 0 (a guideline pathway, but no source names it for this data), source + (NCHS documentation), shape + (15,303 complete exams, mixed features, two waves), risk - (a cut-off we choose, rare positives at the fibrosis cut-off).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `hepatitis_c_egypt`, `hepatitis_c_prediction`, `indian_liver_patient_dataset`.
- as published: participants aged 12 and over: 9,023 complete exams (10,409 in the file) in 2017-March 2020 and 6,280 complete (7,199 in the file) in 2021-2023; joins by SEQN to demographics, the standard ...; target: liver disease measured by FibroScan on every participant: liver stiffness (LUXSMED, kPa; e.g. at least 8 kPa for significant fibrosis) or steatosis (CAP, ...; access: open.
- Why: the same task as ILPD (is this person a liver patient, from age, sex and the liver panel: bilirubin, ALP, ALT, AST, total protein, albumin), with the liver disease measured by an exam instead of hospital case labels | Same task as hepatitis_c_prediction (no disease / fibrosis / cirrhosis from routine lab values, age ...
- Adds: more than 15,000 people against 583; a national probability sample instead of a hospital case series (the record carries Selection Bias); 2017-2023 against 2012, two waves for a temporal check; public domain. Caveats: the label depends on the stiffness or CAP cut-off chosen; advanced fibrosis is rare (a few percent); ...
