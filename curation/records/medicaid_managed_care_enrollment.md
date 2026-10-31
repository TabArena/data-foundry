---
unique_name: medicaid_managed_care_enrollment
name: Managed Care Enrollment
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
year: '2017'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.medicaid.gov/dataset/managed-care-enrollment-report
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/managed-care-enrollment
- https://arxiv.org/abs/2605.12292
- '# Managed Care Enrollment by Program and Plan by catalog id (the STRABLE link above returns 404 on 2026-10-31)'
- https://data.medicaid.gov/dataset/0bef7b8a-c663-5b14-9a46-0b5c2b86b0fe
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Table 5 of CMS's Medicaid Managed Care Enrollment Report, enrollment by state, program and plan; a reporting table whose target is each plan's reported count, with the same plan's count of other years in the same table.
- Source: CMS, data.medicaid.gov, "Managed Care Enrollment by Program and Plan" (https://data.medicaid.gov/dataset/0bef7b8a-c663-5b14-9a46-0b5c2b86b0fe, issued 2017-12-09; Table 5 of the yearly Enrollment Report): it "lists each managed care program's name and type by state. The data provides details such as the plan name, parent organization, geographic region, Medicaid-only enrollment, dual enrollment, and total enrollment by program", and "'0' may not truly represent 0 if a state opted to suppress data for enrollee confidentiality reasons". STRABLE (managed-care-enrollment-by-program-and-plan2022.csv; parquet previewed 2026-10-31): 2,726 rows x 8 columns, years 2016-2022 (876 and 878 rows for 2016 and 2017, about 200 a year after); target `Total Enrollment` (log1p); inputs state, notes (79% missing), program name, plan name, geographic region, year, parent organization (32% missing).
- Use case: none named; enrollment is counted, not predicted. A plan's next-year enrollment from this year's would be forecasting (SEL-10). Fit none as published. Regime temporal by year.
- Siblings and duplicates: `medicaid_mlr_summary_reports` (the loss ratios of the same managed care plans, another target) and the other STRABLE Medicaid tables share the publisher, not the task. Not a duplicate. External collections: STRABLE (arXiv 2605.12292), "Managed Care Enrollment": "Enrollment statistics for Medicaid managed care plans. The task is to predict the number of enrollees"; its link (https://data.medicaid.gov/dataset/managed-care-enrollment-report) returns 404 (2026-10-31).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the data.medicaid.gov page and the yearly Enrollment Report; STRABLE's script `preprocess_medicaid-Managed-Care-Enrollment.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the data.medicaid.gov page, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` on the count, shipped as log1p (MET-3, MET-8); inputs none.
- Risks for /add-dataset: no target (SEL-3, `No Good Target (yet)`); 31% of the rows repeat a state x program x plan of another year, so a random split leaks the plan's own count (SPLIT-3, SPLIT-6); zeros may be suppressed counts (the source's note); the inputs are names and regions only.
- Priority: gap 0 (medical & healthcare, regression not thin), use case 0 (none named), source + (CMS report with notes), shape + (2,726 plan-years, 7 inputs, a year axis), risk - (no target; the same plans repeat across years).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 2,726 rows x 8 columns incl. target (STRABLE parquet); target: Total Enrollment.
- Why: Predict the total enrollment of a Medicaid managed care plan
- Notes: Raw file managed-care-enrollment-by-program-and-plan2022.csv. Only 8 columns.
