---
unique_name: medicaid_child_adult_core_set_quality
name: Child Adult Healthcare Quality
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
year: '2016'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.medicaid.gov/dataset/quality-of-care-child-core-set
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/child-adult-healthcare-quality
- https://arxiv.org/abs/2605.12292
- '# the 2024 release by catalog id (the STRABLE link above returns 404 on 2026-10-31); one release per reporting year'
- https://data.medicaid.gov/dataset/a5023394-ab10-465b-bb4a-7de5ac98d90c
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the rates states report on the Medicaid/CHIP Child and Adult Core Set quality measures, a reporting table; the target is each state's published rate, which nobody predicts from the measure's name.
- Source: CMS, data.medicaid.gov, "<year> Child and Adult Health Care Quality Measures" (one release per reporting year since FFY 2015, the first issued 2016-12-01; 2024 release: https://data.medicaid.gov/dataset/a5023394-ab10-465b-bb4a-7de5ac98d90c): "Performance rates on publicly reported health care quality measures in the CMS Medicaid/CHIP Child and Adult Core Sets", from "Mathematica analysis of (1) Quality Measure Reporting (QMR) system reports, (2) Centers for Disease Control and Prevention Wide-ranging Online Data ..." (CDC WONDER). STRABLE (child-and-adult-health-care-quality-measures.csv; parquet previewed 2026-10-31): 29,367 rows x 15 columns, one row per state x measure x rate definition x population x Core Set year (2019-2024); target `State Rate`, untransformed; inputs state, domain, reporting program, measure name and abbreviation, measure type ("Higher rates are better" or "Lower rates are better"), rate definition, population, methodology, number of states reporting, the source note, the flag "Rate Used in Calculating State Mean and Median", year and free-text state comments.
- Use case: none named; CMS publishes the rates for public reporting and quality improvement. A state's rate is measured, not predicted; imputing a state that did not report would be a stand-in with no named actor. Fit none as published. Regime temporal by Core Set year (the same state and measure recur every year).
- Siblings and duplicates: the other STRABLE Medicaid tables (`medicaid_financial_management`, `medicaid_managed_care_enrollment`, `medicaid_mlr_summary_reports`, `medicaid_first_time_nadac_rates`, `aca_federal_upper_limits`) share the publisher, not the task; `hospital_ratings` (CMS Hospital Compare, `TBD -> 2nd Tier`, `No Good Target (yet)`) is the closest precedent. Not a duplicate. External collections: STRABLE (arXiv 2605.12292), "Child Adult Healthcare Quality": "Quality of care metrics for Medicaid and CHIP beneficiaries. The task is to predict healthcare performance scores"; its link (https://data.medicaid.gov/dataset/quality-of-care-child-core-set) returns 404 (2026-10-31).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the data.medicaid.gov releases; Mathematica's Core Set technical notes not read; STRABLE's script `preprocess_medicaid-Child-Adult-Healthcare-Quality.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the data.medicaid.gov descriptions, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` (MET-8); inputs none.
- Risks for /add-dataset: no target (SEL-3, `No Good Target (yet)`); one column mixes scales: percentages next to "Emergency Department Visits per 1,000 Beneficiary Months" and admissions "per 100,000 Beneficiary Months" (target up to 304), and 2,611 rows are measures where lower is better (USE-5); 33% of the rows repeat a state x rate definition x population x methodology of another year, so a random split leaks the state's own rate (SPLIT-3); `State Specific Comments` is free text; STRABLE's paper speaks of a one-year snapshot, but this table holds six Core Set years.
- Priority: gap 0 (medical & healthcare, regression not thin), use case 0 (none named), source + (CMS releases with their sources), shape + (29,367 rates, categorical and text inputs, a year axis), risk - (no target; mixed scales in the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 29,367 rows x 15 columns incl. target (STRABLE parquet); target: State Rate.
- Why: Predict a state's rate on a Medicaid/CHIP Child and Adult Core Set quality measure
- Notes: Raw file child-and-adult-health-care-quality-measures.csv (data.medicaid.gov). Rows are state x measure x year rates: an aggregate table.
