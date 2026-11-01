---
unique_name: ocha_fts_requirements_and_funding
name: FTS Requirements and Funding
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://fts.unocha.org/
- https://data.humdata.org/dataset/global-requirements-and-funding-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/fts-requirement-and-funding
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the funding each cluster of a humanitarian response plan received against its stated requirement, 1999-2025, from OCHA's FTS: a real outcome with a plausible planning use, but nobody names the decision, the features are few, the same country-clusters recur every year, and the current year's funding was still coming in.
- Source: UN OCHA Financial Tracking Service (FTS), via HDX "Global - Requirements and Funding Data" (CC BY-IGO, updated daily, https://data.humdata.org/dataset/global-requirements-and-funding-data), file `fts_requirements_funding_globalcluster_global.csv`; FTS "presents all humanitarian funding to a country and funding that is specifically reported or that can be specifically mapped against funding requirements stated in humanitarian response plans". As published by STRABLE (`fts-requirement-and-funding`): 7,009 rows x 11 columns (776 plans, 84 countries, 21 global clusters, 1999-2025, 391 rows of 2025), target `funding` (cube-root transformed by STRABLE; 1.8% zero), features country code, plan id, name and code, start and end date, year, cluster code and name, `requirements`.
- Use case: when an appeal is launched, OCHA, a cluster lead or a pooled fund (such as CERF's window for underfunded emergencies) anticipates which clusters will stay underfunded and steers advocacy or allocations. Neither FTS nor STRABLE names this decision (STRABLE App. C item 48: "predict funding gap"), so the fit is approximate; regime temporal by plan year (this year's plans from earlier years), with each country-cluster recurring (SPLIT-13).
- Siblings and duplicates: `ocha_fts_funding_flows` comes from the same database at flow level, a distinct task (PROV-7). No duplicate. External collections: STRABLE (config `fts-requirement-and-funding`; the config spells the source "OHCA").
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the HDX page above; https://fts.unocha.org/; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 48.
- Metric: none from OCHA (a tracking database with no task). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6). The coverage (funding over requirements) is the other framing of the same signal (CLEAN-18).
- Risks for /add-dataset: STRABLE took its snapshot in mid-2025, so the 2025 funding was still accruing: unmatured labels, cut the current year at build (SPLIT-9); `requirements` is the figure at the snapshot, revised during the year, while only the original requirement is known at launch: check whether FTS gives the original requirement per cluster (LEAK-10, USE-3); a panel of the same country-clusters can look like forecasting, so TP-10 (beat each series' naive profile; SEL-11); few features besides the requirement.
- Priority: gap 0 (finance, regression, temporal), use case 0 (the decision is ours), source + (OCHA documents FTS), shape + (7,009 rows over 27 years), risk - (unmatured 2025 funding; revised requirements).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,009 rows x 11 columns incl. target (STRABLE parquet); target: funding.
- Why: Predict the funding received by a humanitarian response plan cluster
- Notes: Raw file fts_requirements_funding_globalcluster_global.csv (OCHA FTS via HDX). Paper says 'funding gap'; config target is funding.
