---
unique_name: ocha_fts_funding_flows
name: FTS Funding
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
domain: finance
problem_type: Regression
source_links:
- https://fts.unocha.org/
- https://data.humdata.org/dataset/global-requirements-and-funding-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/fts-funding
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: humanitarian funding flows from OCHA's Financial Tracking Service, a strong and well-documented source, but predicting one flow's USD amount serves no named decision, a fifth of the flows appear twice, and the free-text description often states the amount.
- Source: UN OCHA Financial Tracking Service (FTS), via HDX "Global - Requirements and Funding Data" (CC BY-IGO, updated daily, https://data.humdata.org/dataset/global-requirements-and-funding-data): "FTS publishes data on humanitarian funding flows as reported by donors and recipient organizations." STRABLE stacked the three flow files `fts_incoming_funding_global.csv`, `fts_internal_funding_global.csv` and `fts_outgoing_funding_global.csv` (its column `funding_type`). As published by STRABLE (`fts-funding`): 13,153 rows x 35 columns, flows of the current year at its snapshot (budget year mostly 2025, 2024 and 2023), target `amountUSD` (transformed by STRABLE), features donor and recipient organisations and their types, plan, cluster, locations, emergency, project, status (paid 7,175, commitment 5,931, pledge 47), contribution type (financial, in kind), method, original currency, exchange rate, description, reported and decision dates.
- Use case: none named; STRABLE's App. C item 47 says "predict funding per crisis", but a row is one flow, not a crisis. A reporting officer estimating the USD value of an in-kind contribution is the closest decision, and the data does not record that estimate. Fit none as framed, approximate at best; regime temporal by decision date.
- Siblings and duplicates: `ocha_fts_requirements_and_funding` uses the same FTS database at another unit (plan x global cluster totals, whose funding sums such flows): a distinct task (PROV-7). `hdx_conflict_events` is another HDX table in STRABLE, unrelated. No duplicate. External collections: STRABLE (config `fts-funding`; the config spells the source "OHCA").
- Better data: a candidate of the benchmark STRABLE; no new search in this run. STRABLE kept one year; FTS serves earlier years through its API.
- Papers and pages: the HDX page above; https://fts.unocha.org/; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 47.
- Metric: none from OCHA (a tracking database with no task). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: 2,827 of the 10,326 flow ids appear under two funding types (incoming and outgoing or internal), so one amount sits in two rows: keep one boundary or group on `id` (PROV-6 within the table, SPLIT-24); `description` often states the amount ("Dec.2024 Pledging Conference for 2025. total amount CHF 34m. RESERVE Part CHF 16m"), a leak (LEAK-10); `exchangeRate` turns an original amount into the target, so check that the raw files' original amount stays out; pledge, commitment and payment are stages of one flow (USE-5); the use case is the open question (USE-1, USE-2), hence `No Good Target (yet)` as on the CARTE tables without a task.
- Priority: gap 0 (finance, regression), use case 0 (none named), source + (OCHA documents FTS), shape + (13,153 rows, 34 mixed features with text and dates), risk - (flows duplicated across boundaries; amounts in the description).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 13,153 rows x 35 columns incl. target (STRABLE parquet); target: amountUSD.
- Why: Predict the USD amount of a humanitarian funding flow
- Notes: OCHA Financial Tracking Service; STRABLE aggregates three funding-flow types into one table.
