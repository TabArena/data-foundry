---
unique_name: worldbank_fif_funding_decisions
name: FIF Funding Decisions
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
problem_type: Regression
original_data_state: One Table
source_links:
- '# old id; on 2026-10-31 it opened another dataset (IEG project ratings)'
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Financial-Intermediary-Funds-Funding-Decisions/DS00053
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/financial-intermediary-funds-funding-decisions
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a ledger (1991-2013 in STRABLE's table) of the amounts that the governing bodies of 19 Financial Intermediary Funds approved per recipient; the approved amount follows the proposal, which the table lacks, and the commitments table restates these decisions.
- Source: World Bank, Finances One "Financial Intermediary Funds Funding Decisions". Its current page was not found: the record's link (DS00053) now opens another dataset (IEG project ratings, read 2026-10-31), and the web search budget ran out before a second search. Its three sibling FIF tables state "No further updates are planned" with data as of 12/31/2013, and this one also ends in 2013. As published by STRABLE (export 2025-07-12): 14,750 rows x 10 columns, 1991-2013, 55% of rows from the Global Environment Facility, target `Amount in USD` (log-transformed by STRABLE), features fund name, use code (projects, project preparation, supervision fees and others), country beneficiary (50% empty), recipient (459), sub account, approval quarter, calendar year, financial product, sector/theme.
- Use case: none named; STRABLE App. C item 40 calls the task "predict decision outcome", but the config's target is the amount, a regression. A fund secretariat sizes a grant from the proposal and the fund's rules, not from a model of this table. Fit none as framed, hence `No Good Target (yet)` as on the CARTE tables without a task; regime temporal by year.
- Siblings and duplicates: `worldbank_fif_commitments` records the commitment of each decision (the Global Fund has 2,534 decision rows against 2,533 commitment rows), so the two are close to one table (PROV-6); `worldbank_fif_cash_transfers` and `worldbank_fif_contributions` are the other FIF tables of the same trustee ledger, frozen at the same date: a governing body's funding decision, the commitment the Trustee records from it, the cash transfer that pays it, and the donors' contributions on the inflow side. They are cuts of one source (PROV-6), so at most one should enter. `worldbank_trust_fund_commitments`, `worldbank_trust_fund_disbursements` and `worldbank_trust_fund_contributions` are the World Bank's maintained trust-fund ledgers (STRABLE, not screened yet), a possible home for the same kind of data after 2013. External collections: STRABLE (config `financial-intermediary-funds-funding-decisions`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 40.
- Metric: none from the Bank (a ledger). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: a frozen 2013 ledger (`Outdated` not set: the curator's call); a near-copy of the commitments table (PROV-6); recipients recur across quarters and project stages (preparation, project, supervision fee) of one project (SPLIT-13, SPLIT-29); the current source page is to be found; the use case is the open question (USE-1, USE-2).
- Priority: gap 0 (finance, regression), use case 0 (none named), source 0 (the publisher's page for this table was not found), shape + (14,750 rows, nine features), risk - (a frozen ledger; near-copy of the commitments).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 14,750 rows x 10 columns incl. target (STRABLE parquet); target: Amount in USD.
- Why: Predict the amount of a Financial Intermediary Fund funding decision
- Notes: World Bank Finances One DS00053, export 2025-07-12. Paper says 'decision outcome'; config target is Amount in USD (regression).
