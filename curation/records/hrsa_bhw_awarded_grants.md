---
unique_name: hrsa_bhw_awarded_grants
name: Awarded Grants IMLS
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.hrsa.gov/data/reports
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/awarded-grants
- https://arxiv.org/abs/2605.12292
- https://data.hrsa.gov/DataDownload/DD_Files/FS_EHB_AWARD_GRANT_FA_AGR_MVX.csv
- https://data.hrsa.gov/DataDownload/DD_Files/Awarded_Grants_Data_Download_Metadata.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: HRSA's register of awarded grant transactions (all bureaus, FY2015-2025), where STRABLE predicts the award amount from program, grantee and place; HRSA sets the amounts by program and continuation, no decision predicts them, and STRABLE's paper names and links IMLS for this table by mistake.
- Source: HRSA Data Warehouse, "Awarded Grants" download (`FS_EHB_AWARD_GRANT_FA_AGR_MVX`, CSV and XLSX on https://data.hrsa.gov/data/download; dictionary `Awarded_Grants_Data_Download_Metadata.xlsx`): "Financial Assistance ... represents the value of grant dollars HRSA has awarded to a grantee ... an aggregation of the financial assistance dollars extracted from the transactions in the HRSA Electronic Handbooks (EHB)"; the file holds awards issued "no later than ten fiscal years from HDW processing date" and is refreshed daily. As used by STRABLE (HF parquet, previewed): 63,815 rows x 42 columns, Award Year 2015-2025, 28,688 grant numbers (continuations repeat, up to 12 rows), target log-scaled with 45 rows at or below zero (de-obligations); program areas Primary Health Care 45%, Health Workforce 20%, HIV/AIDS 12%, Maternal and Child Health 11%, Rural Health 8%, so not the Bureau of Health Workforce alone, as the record's name suggests.
- Use case: none in the source; a grantee budgeting a continuation already holds its notice of award. Fit none; regime temporal (award years), grouped by grant number.
- Siblings and duplicates: no duplicate (grep for HRSA, awarded grants, the file name); `hrsa_uds_hypertension_control` (STRABLE joined these award fields onto it); `imls_awarded_grants` and `imls_discretionary_grants` (the IMLS grant tables, whose labels STRABLE also mixed up). External collections: STRABLE (Table C.4 row 5: "Awarded Grants IMLS ... Grants awarded by the Institute of Museum and Library Services. The task is to predict the specific grant amount.", linked to imls.gov, while `config.json` says source HRSA and the columns are HRSA's).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19), Sec. 3 and Table C.4; the HRSA data dictionary.
- Metric: none found (HRSA defines no task; STRABLE's R², App. D.1, is benchmark-wide, MET-5), so the fallback `rmse` on the dollars; inputs none.
- Risks for /add-dataset: no task (`No Good Target (yet)`); continuations of one grant across years make a random split a lookup (LEAK-17, SPLIT-13: group by grant number or split by award year); grantee address, representative and senator names are as of the latest refresh, not the award date (LEAK-10 under a temporal split); negative amounts; the record's `name` ("Awarded Grants IMLS") is STRABLE's mislabel.
- Priority: gap 0, use case 0, source + (HRSA data dictionary), shape + (63,815 awards, mixed columns, temporal), risk - (no task, repeated grants).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 63,815 rows x 42 columns incl. target (STRABLE parquet); target: Financial Assistance.
- Why: Predict the financial assistance amount of an awarded grant
- Notes: Mismatch: the paper names and links IMLS awarded grants, but the config source is HRSA and the raw file is HRSA's FS_EHB_AWARD_GRANT_FA_AGR_MVX.xlsx (HRSA/BHW awarded grants); IMLS awarded grants are row 52 ('Grant').
