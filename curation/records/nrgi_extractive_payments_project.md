---
unique_name: nrgi_extractive_payments_project
name: Industry Payments Project
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
original_source: Website
domain: finance
problem_type: Regression
original_data_state: One Table
source_links:
- https://energydata.info/dataset/ei-payments-to-governments
- https://resourceprojects.org/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/industry-payments-project
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: payments that oil, gas and mining companies disclose to governments by project under mandatory-disclosure laws, a documented release, but no decision is named that predicts a payment's amount, the features are who, where and when, and free-text notes quote amounts.
- Source: Natural Resource Governance Institute (NRGI), ResourceProjects.org, mirrored on the World Bank's energydata.info as "World - Extractive Industry Payments to Governments" (created 2019-04-24, last modified 2020-12-14, CC BY 4.0; CKAN metadata read 2026-10-31): "Project-level payments to governments disclosed by extractive industry companies. The data covers payments related to the extraction of petroleum or mineral resources made by over 700 companies to governments in 150+ countries. [...] Since 2014, the EU, Canada, UK and Norway have passed mandatory disclosure laws [...] Companies disclose this data annually, which is scraped and cleaned". Three files: `project.csv`, `entity.csv`, `source.csv`. As published by STRABLE (`industry-payments-project`): 32,327 rows x 9 columns, target `projectPayment` (transformed by STRABLE; negative payments exist), features report id, reporting company (872), report year (2014-2020; 2014 and 2020 with 110 and 188 rows), project country, project name (7,398), payment type (fees, taxes, royalties and 5 more), `nrgiNotes`, `notes`.
- Use case: none named. STRABLE's App. C (item 64) describes CMS Open Payments ("Payments related to specific research projects or clinical trials", source cms.gov/openpayments), not this data. The nearest decision is a revenue authority or a civil-society monitor flagging a reported payment far from what the project, company and payment type lead one to expect: anomaly screening, not a decision on the predicted amount. Fit none as framed, approximate at best; regime temporal by report year (grouped by project for a new project).
- Siblings and duplicates: `nrgi_extractive_payments_entity` is the entity-level table of the same reports (same release, payments per government entity instead of per project): a cut of one dataset (PROV-6), so at most one of the two should enter. `global_dams_database` matched the keyword search only. No duplicate. External collections: STRABLE (config `industry-payments-project`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run. ResourceProjects.org is the maintained source; the energydata.info mirror stops at 2020-12.
- Papers and pages: https://energydata.info/dataset/ei-payments-to-governments; https://resourceprojects.org/; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C items 63-64 (which name the wrong source).
- Metric: none from NRGI (a transparency release with no task). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: `notes` (79% empty) quotes amounts ("Royalties include $3,840,000 of royalties paid-in-kind [...]") and `nrgiNotes` logs NRGI's edits, so drop or check them (LEAK-10); the reporting currency and the conversion to USD must be traced in `project.csv` (USE-5); a project recurs over years and payment types (SPLIT-13, SPLIT-29); the use case is the open question (USE-1, USE-2), hence `No Good Target (yet)` as on the CARTE tables without a task; STRABLE's target is transformed, rebuild from `project.csv` (MET-3).
- Priority: gap 0 (finance, regression), use case 0 (none named), source + (NRGI documents the release and the laws behind it), shape 0 (32,327 rows, but the features are only company, project, country, year and payment type), risk - (amounts in free-text notes; one release cut into the project and entity tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 32,327 rows x 9 columns incl. target (STRABLE parquet); target: projectPayment.
- Why: Predict the payment to a government reported for an extractive project (project level)
- Notes: Same mismatch as row 63 (paper says CMS Open Payments; data is NRGI project-level extractive payments on energydata.info). Same source as row 63.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two cuts of the same payment reports (`nrgi_extractive_payments_entity`; PROV-6). The curator keeps one, or both as distinct tasks.
