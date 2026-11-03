---
unique_name: worldbank_fif_cash_transfers
name: FIF Cash Transfers
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
- https://financesone.worldbank.org/d/DS00987
- '# old id; on 2026-10-31 its Finances One page did not show this dataset'
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Financial-Intermediary-Funds-Cash-Transfers/DS00029
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/financial-intermediary-funds-cash-transfers
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a frozen ledger (1991-2013, "No further updates are planned") of transfers the World Bank, as trustee of 20 Financial Intermediary Funds, made to recipients, with five columns of who and when; no decision predicts the amount of a ledger line.
- Source: World Bank, Finances One "Financial Intermediary Funds Cash Transfers", now DS00987 (https://financesone.worldbank.org/api-explorer?id=DS00987): "This dataset provides data on FIFs cash transfers at the transaction detail level"; "Data is updated as of 12/31/2013. No further updates are planned for this particular dataset"; fields Fund Name, Principal Recipient ("Organization that receives the funds"), Transfer Quarter, Calendar Year, Sector/Theme, Amount in USD ("Amount in USD equivalent calculated using historical rates"). The record's link (DS00029) redirects to financesone.worldbank.org/d/DS00029, whose page did not show this dataset on 2026-10-31. As published by STRABLE (export 2025-07-13): 16,630 rows x 6 columns, 1991-2013, 64% of rows from the Global Fund, target `Amount in USD` (transformed by STRABLE; its maximum, 42.7 against a median of 4.0, needs a look at the raw amounts).
- Use case: none named (STRABLE App. C item 38: "predict transfer amount"). A fund's treasury forecasts its disbursements per recipient over time, a time series (SEL-10), not this table. Fit none as framed, hence `No Good Target (yet)` as on the CARTE tables without a task; regime temporal by year.
- Siblings and duplicates: `worldbank_fif_commitments`, `worldbank_fif_funding_decisions` and `worldbank_fif_contributions` are the other FIF tables of the same trustee ledger, frozen at the same date: a governing body's funding decision, the commitment the Trustee records from it, the cash transfer that pays it, and the donors' contributions on the inflow side. They are cuts of one source (PROV-6), so at most one should enter. `worldbank_trust_fund_commitments`, `worldbank_trust_fund_disbursements` and `worldbank_trust_fund_contributions` are the World Bank's maintained trust-fund ledgers (STRABLE, not screened yet), a possible home for the same kind of data after 2013. External collections: STRABLE (config `financial-intermediary-funds-cash-transfers`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the DS00987 page; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 38. The FIF Trustee site (https://fiftrustee.worldbank.org/) offers fund pages and PDF reports; no tables found.
- Metric: none from the Bank (a ledger). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: the data ends in 2013 and will not be updated (`Outdated` not set: the curator's call); each fund-recipient pair recurs by quarter, so a row's amount is close to its neighbours in the same series (SPLIT-13, SPLIT-29); only five features; the raw amounts need a scale check (PROV-13); the use case is the open question (USE-1, USE-2).
- Priority: gap 0 (finance, regression), use case 0 (none named), source + (field definitions published), shape 0 (five columns, all fund, recipient, sector and period), risk - (a frozen 2013 ledger; one source cut into four tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 16,630 rows x 6 columns incl. target (STRABLE parquet); target: Amount in USD.
- Why: Predict the amount of a cash transfer from a Financial Intermediary Fund to an implementing agency
- Notes: World Bank Finances One DS00029, export 2025-07-13. Only 6 columns.
