---
unique_name: hrsa_clinician_dashboard
name: External Clinician Dashboard
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://data.hrsa.gov/data/reports
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/external-clinician-dashboard
- https://arxiv.org/abs/2605.12292
- https://data.hrsa.gov/topics/health-workforce/program/clinician-dashboard-alumni
- https://data.hrsa.gov/DataDownload/StaticDocuments/External_Clinician_Dashboard_Data_v2025.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: HRSA's records of National Health Service Corps and Nurse Corps alumni after their service obligation, with the retention outcome the programs track; STRABLE's target `Score` is not a clinician score but the HPSA score of the designation the alumnus works in now, a property of the place, so the task has to be re-targeted to retention.
- Source: HRSA Bureau of Health Workforce, Clinician Dashboards (https://data.hrsa.gov/topics/health-workforce/program/clinician-dashboard-alumni). The About PDF: the dashboards analyze "the post-service retention and distribution of BHW Program Alumni"; "HPSA Retention: Percentage of program alumni who currently work in a Health Professional Shortage Area"; "ranks 5-8 is known as 'HPSA Retention' and ranks 3-8 is known as 'Community Retention'"; "This analysis is run once annually on October 1st". Data file `External_Clinician_Dashboard_Data_v2025.xlsx` (STRABLE used v2024); its Alumni Data Dictionary (read from the file's dictionary sheet only): "Score | This attribute represents the score of the designation, if applicable, to which the alumni was matched. If no designation was matched to a current location of the alumni, a value of -1 is provided"; "CommunityRank | ... ranging from 1-8 ... whether the alumni is still working at the same site, same census tract, and same county, and whether they are still working in a HPSA". As used by STRABLE (HF parquet, previewed): 28,399 rows x 21 columns, `CommunityRank` only 5-8 (alumni not in a HPSA, score -1, are gone), obligation end FY2012-2023, NHSC loan repayment 82%, Nurse Corps loan repayment 10%.
- Use case: when an obligation ends, or when a site or award is approved, HRSA or a state primary care office estimates whether the clinician will stay in a shortage area or in the community; the source defines the outcome but names no prediction. Fit approximate (the status is read once a year on October 1 for every cohort, so the time since the obligation ended runs from about 1 to 12 years); regime temporal by obligation-end year.
- Siblings and duplicates: no duplicate (grep for clinician, NHSC, Nurse Corps); `hrsa_health_professional_shortage_areas` holds the HPSA scores STRABLE's target copies. External collections: STRABLE (Table C.4 row 37: "Performance metrics for clinicians in HRSA programs. The task is to predict clinician productivity scores.", a misreading of `Score`).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: the About PDF (https://data.hrsa.gov/Content/Documents/topics/About%20the%20Clinician%20Dashboards.pdf); STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19).
- Metric: none found (HRSA reports retention percentages, no model; STRABLE's R², App. D.1, is benchmark-wide and scores its own target, MET-5), so the fallback `roc_auc` for HPSA retention, or `log_loss` for the eight ranks; inputs none.
- Risks for /add-dataset: re-target from HRSA's file, not from STRABLE's cut, which lacks ranks 1-4 (USE-5, PROV-13); drop every column built from the current location (`Current*`, `HPSAID`, `DesignationType`, `DesignationTypeFinal`, `CurrentDesignationName`, `Score`, `PopTypeDescription`, `IsRural`, `InMCTA`; LEAK-10); one shared reading date for all cohorts (SEL-6): fix the horizon per cohort (yearly file versions, or one cohort per window) or keep `ObligationEndFiscalYear` and name the gap; the Unified sheet (CHGME, THCGME alumni) has other columns.
- Priority: gap 0 (binary; the eight ranks would be multiclass, thin), use case 0 (the source names the outcome, not a decision), source + (HRSA About PDF and data dictionary), shape + (28,399 alumni in a HPSA alone, categorical columns, yearly cohorts), risk - (re-target, label timing).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 28,399 rows x 21 columns incl. target (STRABLE parquet); target: Score.
- Why: Predict a score on HRSA's clinician dashboard metrics
- Notes: Raw file External_Clinician_Dashboard_Data_v2024.xlsx (HRSA). What 'Score' measures needs checking.
