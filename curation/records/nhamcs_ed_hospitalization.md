---
unique_name: nhamcs_ed_hospitalization
name: National Hospital Ambulatory Medical Care Survey (NHAMCS), emergency department public-use visit files
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHAMCS/
- https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/readme2022.txt
- https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/doc22-ed-508.pdf
- https://doi.org/10.1186/s13054-019-2351-7
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: NCHS's national sample of emergency department visits, open yearly files 1992-2022 with triage vitals, reasons for visit and the disposition; Raita et al. 2019 used 135,470 adult visits of 2007-2015 to predict hospitalization and critical care at triage, a direct use case on a strong source.
- Source: NCHS, National Hospital Ambulatory Medical Care Survey, emergency department public-use files (ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHAMCS/: one ED file per year 1992-2022; ed2022.zip is 37.3 MB unzipped, documented in doc22-ed-508.pdf). The 2022 readme: the data are for "statistical reporting and analysis only", may not be linked to identifiable data, and "the application of weights to the sample data is REQUIRED" for national estimates. As published: one row per sampled ED visit (the count per year not checked).
- Use case: a triage nurse at arrival assigns the priority and anticipates admission; Raita et al. 2019 frame exactly this, against the Emergency Severity Index as the reference; fit direct for the triage items; regime temporal by survey year (or grouped by hospital, if a masked hospital code ships: to check).
- Siblings and duplicates: `mimic_iv_ed_triage` (unscreened; one Boston hospital 2011-2019, credentialed access): the same task from another source; `hospital_patient_data` (`TBD -> 2nd Tier`, unknown source), the record it was found next to; `ed_uti_urine_culture_prediction`, `curial_covid_ed_triage`, `pecarn_pediatric_head_trauma_citbi`: other ED tasks. No duplicate. External collections: none found.
- Better data: found as a related task next to `hospital_patient_data`; no further search this round.
- Papers and pages: Raita, Goto, Faridi, Brown, Camargo and Hasegawa, "Emergency department triage prediction of clinical outcomes using machine learning models", Crit Care 23:64, 2019 (doi 10.1186/s13054-019-2351-7; abstract read): adults, 2007-2015; critical care (ICU admission or in-hospital death) 2.1%, hospitalization (direct admission or transfer) 16.2%; predictors "routinely available triage data" (demographics, triage vital signs, chief complaints, comorbidities); a 70/30 split; AUC 0.86 and 0.82 for a deep network against 0.74 and 0.69 for the ESI reference.
- Metric: Raita et al. report the AUC and the net benefit of decision curves, two criteria (MET-5), so the fallback `roc_auc`, which is also their headline; inputs none.
- Risks for /add-dataset: keep only triage-time items (drop diagnoses, tests, procedures, medications, providers, wait and visit times; LEAK-10, USE-3); the triage level is a nurse's reading and the study's reference model, a call whether it is an input; build the target from the disposition items (admit, transfer, ICU, died); items and codes change over the years, so pick a span and harmonise; the 2020-2022 pandemic years; the survey design (weights, hospitals sampled in clusters); the terms forbid re-identification (no criterion, EV-4).
- Priority: gap 0, use case + (a published triage-prediction study with the ESI as its reference), source + (NCHS, documentation per year), shape + (tens of thousands of visits a year, mixed types, many years), risk - (post-triage columns to drop, yearly files to harmonise).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `hospital_patient_data`.
- as published: one row per sampled ED visit, roughly 15,000-35,000 visits per survey year (count not checked per year); Raita et al. 2019 (Critical Care 23:64) used 135,470 adult ED visits from 2007-2015 with ...; target: hospitalization (direct admission or transfer; 16.2% in Raita et al.) or critical care (ICU admission or in-hospital death; 2.1%); the files also carry the ...; access: open.
- Why: A strong federal source in the record's domain (patient flow in a hospital) with a decision-linked target known only after the visit and predictors known at triage; the record itself has no good target and an unknown source.
- Adds: A traceable, national, multi-year visit-level dataset; a temporal split by survey year is natural. Checks for screening: the survey weights and sampling design, the 2020-2022 pandemic years, and NCHS terms of use (statistical use only, no re-identification).
