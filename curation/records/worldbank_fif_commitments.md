---
unique_name: worldbank_fif_commitments
name: FIF Commitments
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
- https://financesone.worldbank.org/d/DS00994
- https://datacatalog.worldbank.org/search/dataset/0041736/financial-intermediary-funds-commitments
- '# old id; on 2026-10-31 it opened another dataset (IBRD bond issues)'
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Financial-Intermediary-Funds-Commitments/DS00052
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/financial-intermediary-funds-commitments
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a frozen ledger (1991-2013, "No further updates are planned") of the commitments the World Bank recorded as trustee of 19 Financial Intermediary Funds, each restating a governing body's funding decision; no decision predicts a commitment's amount from the fund, recipient and quarter.
- Source: World Bank, Finances One "Financial Intermediary Funds Commitments", now DS00994 (https://financesone.worldbank.org/api-explorer?id=DS00994; World Bank data catalog 0041736, "Calendar year 1991 - 2013"): commitments are legal obligations to pay recipients, typically multilateral development banks or UN agencies; Approval Quarter is "the quarter in which the Trustee recorded a commitment, based on a decision by the relevant governing body"; "No further updates are planned for this particular dataset", with users sent to fiftrustee.worldbank.org. The record's link (DS00052) now opens another dataset (IBRD bond issues, read 2026-10-31). As published by STRABLE (export 2025-07-13): 12,875 rows x 7 columns, 1991-2013, half of the rows from the Global Environment Facility, target `Amount in USD` (log-transformed by STRABLE), features fund name, principal recipient (458), approval quarter, calendar year, financial product (grant, guarantee and others), sector/theme.
- Use case: none named (STRABLE App. C item 39: "predict commitment value"). The amount is set by the funding decision it records, which is not a feature. Fit none as framed, hence `No Good Target (yet)` as on the CARTE tables without a task; regime temporal by year.
- Siblings and duplicates: `worldbank_fif_funding_decisions` holds the decisions these commitments record (the Global Fund has 2,533 commitment rows against 2,534 decision rows), so the two are close to one table (PROV-6); `worldbank_fif_cash_transfers` and `worldbank_fif_contributions` are the other FIF tables of the same trustee ledger, frozen at the same date: a governing body's funding decision, the commitment the Trustee records from it, the cash transfer that pays it, and the donors' contributions on the inflow side. They are cuts of one source (PROV-6), so at most one should enter. `worldbank_trust_fund_commitments`, `worldbank_trust_fund_disbursements` and `worldbank_trust_fund_contributions` are the World Bank's maintained trust-fund ledgers (STRABLE, not screened yet), a possible home for the same kind of data after 2013. External collections: STRABLE (config `financial-intermediary-funds-commitments`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the DS00994 page; https://datacatalog.worldbank.org/search/dataset/0041736/financial-intermediary-funds-commitments; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 39.
- Metric: none from the Bank (a ledger). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: the data ends in 2013 and will not be updated (`Outdated` not set: the curator's call); a near-copy of the funding-decision table (PROV-6); the same fund-recipient pairs recur by quarter (SPLIT-13, SPLIT-29); six features, all codes of fund, recipient, product, sector and period; the use case is the open question (USE-1, USE-2).
- Priority: gap 0 (finance, regression), use case 0 (none named), source + (field definitions published), shape 0 (six columns of codes and periods), risk - (a frozen 2013 ledger; near-copy of the funding decisions).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 12,875 rows x 7 columns incl. target (STRABLE parquet); target: Amount in USD.
- Why: Predict the amount of a Financial Intermediary Fund commitment
- Notes: World Bank Finances One DS00052, export 2025-07-13.
