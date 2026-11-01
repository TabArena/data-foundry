---
unique_name: medicaid_mlr_summary_reports
name: MLR Summary Reports
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
year: '2024'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.medicaid.gov/dataset/medical-loss-ratio
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/mlr-summary-reports
- https://arxiv.org/abs/2605.12292
- '# MLR Summary Reports by catalog id (the STRABLE link above returns 404 on 2026-10-31)'
- https://data.medicaid.gov/dataset/743f9f04-4473-41e2-9da2-9a89db65ee55
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: CMS's summary of the medical loss ratios that Medicaid managed care plans report; the target is computed from the numerator and denominator that ship in the same row, and without them no decision fits.
- Source: CMS, data.medicaid.gov, "MLR Summary Reports" (https://data.medicaid.gov/dataset/743f9f04-4473-41e2-9da2-9a89db65ee55, issued 2024-11-01, updated 2026-06-26): "plan-specific MLRs for Medicaid managed care programs. The MLR summary report data include MLRs for MCOs, PIHPs, and PAHPs submitted by states under 42 CFR § 438.74", with plan name, reporting period, report year, "MLR numerator", "MLR denominator", member months, "Adjusted MLR" and "Remittance amount owed by plan". STRABLE (mlr-public-use-file-07302024final.csv; parquet previewed 2026-10-31): 1,665 rows x 14 columns, report years 2017-2020; target `Adjusted MLR` (percent, log); inputs state, program name and type, eligibility group, plan name, reporting period start and end, report year, MLR numerator, MLR denominator, member months, remittance (66% missing).
- Use case: none named; states and CMS use the reported MLR to hold plans to the minimum standard and to collect remittances, so the ratio is computed, not predicted. Fit none as published. Regime temporal by report year.
- Siblings and duplicates: `medicaid_managed_care_enrollment` (the same plans' enrollment) and the other STRABLE Medicaid tables share the publisher, not the task. Not a duplicate. External collections: STRABLE (arXiv 2605.12292), "MLR Summary Reports": "Medical Loss Ratio data for healthcare plans. The task is to predict the MLR percentage"; its link (https://data.medicaid.gov/dataset/medical-loss-ratio) returns 404 (2026-10-31).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the data.medicaid.gov page; 42 CFR 438.8 (the MLR formula) not read; STRABLE's script `preprocess_medicaid-MLR-Summary-Reports.py` and its feature-engineering variant, which parses the numerator, denominator and remittance into numbers (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the data.medicaid.gov page, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` (MET-8); inputs none.
- Risks for /add-dataset: a deterministic target (SEL-5): on the preview, 72% of the rows have the adjusted MLR within 0.1 percentage point of 100 x numerator / denominator (the rest differ by the credibility adjustment; correlation 0.97), so the two inputs must go; the remittance follows from an MLR below the state's minimum (post-outcome, LEAK checks); what is left (state, program, plan name, member months) makes no task we could name (SEL-3, `No Good Target (yet)`).
- Priority: gap 0 (medical & healthcare, regression not thin), use case 0 (none named), source + (CMS page naming the rule), shape + (1,665 plan-years, mixed inputs), risk - (target computed from shipped columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,665 rows x 14 columns incl. target (STRABLE parquet); target: Adjusted MLR.
- Why: Predict a Medicaid managed care plan's adjusted medical loss ratio
- Notes: Raw file mlr-public-use-file-07302024final.csv. The adjusted MLR is computed from reported claims and premium components; check for those among the features.
