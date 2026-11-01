---
unique_name: fdic_community_banking
name: Community Banking
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: finance
original_data_state: One Table
source_links:
- https://www.fdic.gov/community-banking-research-program/reference-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/community-banking_wide
- https://arxiv.org/abs/2605.12292
- '# Notes to Users (the codebook)'
- https://www.fdic.gov/community-banking-research-program/community-banking-reference-data-combined-historical-and-current
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the STRABLE release and a preview of its files; a human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the FDIC's community-bank reference table, published "so that external analysts can build upon the FDIC's research"; STRABLE's target, an organization's loan-to-asset ratio from its Call Report, is a reported figure no decision rests on, and several of the kept columns are computed from it.
- Source: FDIC Division of Insurance and Research, Community Banking Reference Data (https://www.fdic.gov/community-banking-research-program/reference-data), updated quarterly, files from Q1-1984 on, behind the 2012 and 2020 Community Banking Studies. Notes to Users, Sec. 2: "Create data sets available to the public that contain community bank designations from Q1-1984 onward, as well as the demographic and financial data underlying those designations, for all FDIC-insured institutions." As published: one row per banking organization and quarter (CALLYM) with ID, holding company, CERT, name, address, YEAR, the CB flag, EXCL_* exclusion flags, ASSET, HCASSET, SIZE, FORASSET, LOANTOASSET, CORERATIO, MAX_DEPOSITS, OFFICE_COUNT, metro and state counts, BUSINESS_LINE and the MEETS_* tests. STRABLE read Historical_Community_Banking_Reference_Data_2019_To_2023.CSV and kept the last quarter of each organization: 5,253 rows x 31 columns (5,096 CERTs, 20 distinct quarters), target LOANTOASSET in percent, no column dropped.
- Use case: none named. The Notes say "This data is provided to the public to supplement existing FDIC research on community banks and encourage further academic and professional research" (Sec. 2); the ratio comes from the bank's own quarterly Call Report, so no actor needs it predicted from name, address and flags. Fit: none found. Regime: IID over organizations (one row each), temporal if the quarterly panel were used.
- Siblings and duplicates: `fdic_summary_of_deposits` (the FDIC's SOD, the source of MAX_DEPOSITS here; another table, another target); no other community-bank record (searched fdic, community bank). External collections: STRABLE ("Community Banking", App. C.2: "to predict bank asset sizes or performance ratios").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: Notes to Users (https://www.fdic.gov/community-banking-research-program/community-banking-reference-data-combined-historical-and-current, revised 2025-12-02); FDIC Community Banking Studies 2012 and 2020 (the definition); STRABLE (Blayer et al. 2026, arXiv 2605.12292, App. C.2 and D.1).
- Metric: none found (the FDIC page and the Notes define no prediction task), so the fallback `rmse`; STRABLE, a benchmark and not the source, scores R^2 (App. D.1) (MET-1).
- Risks for /add-dataset: the target leaks into the features: BUSINESS_LINE ("No Specialty: Total loans are less than 33% of assets", Notes Sec. 2b), CB (large organizations need a loan-to-asset ratio above 33%), EXCL_NOLOANS and, in the source file, MEETS_LTA (LEAK, SEL-5); percent strings to parse; a target to define first.
- Priority: gap 0 (finance), use case 0 (none), source + (the FDIC's Notes to Users), shape + (5,253 organizations, 30 mixed columns), risk - (no decision fits the target), risk - (columns computed from the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 5,253 rows x 31 columns incl. target (STRABLE parquet); target: LOANTOASSET.
- Why: Predict a community bank's loan-to-asset ratio from its reference data
- Notes: Raw file Historical_Community_Banking_Reference_Data_2019_To_2023.CSV (FDIC).
