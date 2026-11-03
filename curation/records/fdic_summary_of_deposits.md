---
unique_name: fdic_summary_of_deposits
name: Summary of Deposit
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: finance
problem_type: Regression
original_data_state: One Table
source_links:
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/summary-of-deposit_wide
- https://arxiv.org/abs/2605.12292
- https://www.fdic.gov/bank-financial-reports/summary-deposits
- https://banks.data.fdic.gov/bankfind-suite/SOD
- '# field definitions'
- https://api.fdic.gov/banks/docs/sod_variables_definitions.csv
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the STRABLE release and a preview of its files; a human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the FDIC's annual survey of branch-office deposits; STRABLE kept only the main-office rows and predicts the institution's total deposits, a figure the bank reports, while its paper names deposits per branch, the target with a plausible use (what an office at a location would hold).
- Source: FDIC Summary of Deposits, "the annual survey of branch office deposits as of June 30 for all FDIC-insured institutions" (https://www.fdic.gov/bank-financial-reports/summary-deposits; data in BankFind Suite, https://banks.data.fdic.gov/bankfind-suite/SOD; field list sod_variables_definitions.csv). As published: one row per office per year with branch, institution and holding-company fields; DEPSUMBR "Branch office deposits as of June 30"; DEPSUM "Total domestic deposits of the institution as of June 30. This amount is only reported for the main office locations." STRABLE read SOD_CustomDownload_ALL_2024_06_30.csv, kept the rows with DEPSUM > 0 (the main offices) and dropped ASSET, DEPDOM and DEPSUMBR "# Leakage": 4,546 rows (one per institution) x 62 columns, target log(DEPSUM).
- Use case: as STRABLE ships it, none: an institution's total deposits are on its Call Report. Re-targeted to DEPSUMBR over all offices, a bank planning an office estimates the deposits it would hold at a location; the FDIC page names no such use (it links the "Deposit Market Share Reports"), so the fit is approximate. Regime: grouped by institution (offices share the bank's columns), or temporal across survey years.
- Siblings and duplicates: `fdic_community_banking` (the FDIC's research table, another target); no other SOD record (searched fdic, summary of deposits). External collections: STRABLE ("Summary of Deposit", App. C.2: "The task is to predict total deposits per branch", while its config's target is DEPSUM).
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: the FDIC SOD page and its reporting instructions (https://www.fdic.gov/bank-financial-reports/summary-deposits-reporting-instructions.pdf); STRABLE (arXiv 2605.12292, App. C.2 and D.1).
- Metric: none found (the FDIC pages define no prediction task), so the fallback `rmse` on log deposits; STRABLE scores R^2 (App. D.1) (MET-1).
- Risks for /add-dataset: re-target to DEPSUMBR (unit $ thousands) and decide whether the bank-level ASSET and DEPDOM are known at the prediction point (LEAK); the main office's deposits include deposits not assigned to branches; the number of offices in the 2024 survey is to count; the link the run took from STRABLE (fdic.gov/bank/statistical/stats) is "FDIC Statistics at a Glance", replaced here by the SOD pages.
- Priority: gap 0 (finance), use case 0 (approximate, after a re-target), source + (the FDIC's field definitions), shape + (thousands of offices, mixed types, grouped by bank), risk - (the shipped target needs a re-target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 4,546 rows x 62 columns incl. target (STRABLE parquet); target: DEPSUM.
- Why: Predict a bank branch's total deposits
- Notes: Raw file SOD_CustomDownload_ALL_2024_06_30.csv (FDIC Summary of Deposits, June 2024); 4,546 rows, so a subset of the branches.
