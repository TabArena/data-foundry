---
unique_name: medicaid_financial_management
name: Financial Management Medicaid
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
year: '? (2018)'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.medicaid.gov/dataset/state-expenditures
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/financial-management
- https://arxiv.org/abs/2605.12292
- '# the dataset by catalog id (the STRABLE link above returns 404 on 2026-10-31)'
- https://data.medicaid.gov/dataset/5b19d1d4-ae43-5fcd-ba14-3cecd99f473f
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: CMS-64 expenditure lines by state and service category, an accounting report; the target is the state's part of each line, which follows from the federal share that ships beside it and the line's matching rate.
- Source: CMS, data.medicaid.gov, "Medicaid Financial Management Data" (https://data.medicaid.gov/dataset/5b19d1d4-ae43-5fcd-ba14-3cecd99f473f, issued 2018-04-10, modified 2024-12-11): "summary state-by-state total expenditures by program for the Medicaid Program, Medicaid Administration and CHIP programs. These state expenditures are tracked through the automated Medicaid Budget and Expenditure System/State Children's Health Insurance Program Budget and Expenditure System (MBES/CBES)"; the reports themselves are older (medicaid.gov, state expenditure reporting), so the year is the catalog's. STRABLE (medicaid-financial-management-data.csv; parquet previewed 2026-10-31): 15,511 rows x 9 columns, one row per state (56) x program (Medical Assistance Program, Administration) x service category (273), no year column (STRABLE keeps the latest year); target `State Share`, arcsinh-transformed; inputs state, program, service category, `Federal Share` and its Medicaid, ARRA and BIPP parts, location.
- Use case: none named; the states report these amounts and CMS publishes them. Fit none as published. Regime IID within one year; temporal across the years of the full release.
- Siblings and duplicates: the other STRABLE Medicaid tables (`medicaid_child_adult_core_set_quality`, `medicaid_managed_care_enrollment`, `medicaid_mlr_summary_reports`, `medicaid_first_time_nadac_rates`, `aca_federal_upper_limits`) share the publisher, not the task. Not a duplicate. External collections: STRABLE (arXiv 2605.12292), "Financial Management Medicaid": "State expenditures on Medicaid programs and services. The task is to predict total program costs" (the config's target is `State Share`, not a total); its link (https://data.medicaid.gov/dataset/state-expenditures) returns 404 (2026-10-31).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the data.medicaid.gov page; STRABLE's script `preprocess_medicaid-Medicaid_Financial_Management.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the data.medicaid.gov page, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` (MET-8); inputs none.
- Risks for /add-dataset: a near-deterministic target (SEL-5): on the 4,377 lines where both shares are positive, the federal fraction federal / (federal + state) runs from 0.40 to 1.00 (quartiles 0.57 and 0.87, median 0.70), the federal matching rates by state and category, so the shipped `Federal Share` columns nearly give the target away; without them the task is a spending line from its state and category name, which no actor predicts (`No Good Target (yet)`). 68% of the targets are 0; 391 lines are totals (such as "T-Total Net Expenditures") that sum other lines of the same state; negative adjustments occur.
- Priority: gap 0 (medical & healthcare, regression not thin), use case 0 (none named), source + (CMS page naming the reporting system), shape + (15,511 lines, mixed inputs), risk - (target near-deterministic from the federal share; no task without it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 15,511 rows x 9 columns incl. target (STRABLE parquet); target: State Share.
- Why: Predict the state share of a Medicaid expenditure line
- Notes: Raw file medicaid-financial-management-data.csv. State x service x year aggregate lines; the state share is largely an accounting split (FMAP) of the total, so check for a near-deterministic target.
