---
unique_name: worldbank_fif_contributions
name: Contributions to FIFs
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
- https://financesone.worldbank.org/d/DS00977
- '# old id; on 2026-10-31 it opened another dataset (member countries'' votes)'
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Contributions-to-Financial-Intermediary-Funds/DS00051
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/contributions-to-financial-intermediary-funds
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a frozen ledger (1991-2013, "No further updates are planned") of 2,990 donor receipts into 21 Financial Intermediary Funds; a receipt's amount follows the donor's pledge, which the table lacks, and no decision is named.
- Source: World Bank, Finances One "Contributions to Financial Intermediary Funds", now DS00977 (https://financesone.worldbank.org/api-explorer?id=DS00977): Receipt Type "Indicates whether a contribution was received as cash or a promissory note/letter of credit", Contribution Type "Capital, Grant or Loan", Sub Account "A window or program within the Fund", Amount in USD "calculated using historical rates"; "Data is provided as of 12/31/2013. No further updates are planned for this particular dataset." The record's link (DS00051) now opens another dataset (member countries' votes, read 2026-10-31). As published by STRABLE (export 2025-07-12): 2,990 rows x 11 columns, 1991-2013, target `Amount in USD` (cube-root transformed by STRABLE), features fund name, donor name (85) and country code, receipt type, receipt quarter, calendar year, receipt currency (31), contribution type, sub account (65% empty), sector/theme; 2 exact duplicate rows.
- Use case: none named (STRABLE App. C item 21: "predict donor contribution levels"). A fund's treasury plans with the donors' pledged schedules, not with a model of the receipt amount. Fit none as framed, hence `No Good Target (yet)` as on the CARTE tables without a task; regime temporal by year.
- Siblings and duplicates: `worldbank_fif_cash_transfers`, `worldbank_fif_commitments` and `worldbank_fif_funding_decisions` are the other FIF tables of the same trustee ledger, frozen at the same date: a governing body's funding decision, the commitment the Trustee records from it, the cash transfer that pays it, and the donors' contributions on the inflow side. They are cuts of one source (PROV-6), so at most one should enter. `worldbank_trust_fund_commitments`, `worldbank_trust_fund_disbursements` and `worldbank_trust_fund_contributions` are the World Bank's maintained trust-fund ledgers (STRABLE, not screened yet), a possible home for the same kind of data after 2013. External collections: STRABLE (config `contributions-to-financial-intermediary-funds`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the DS00977 page; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 21.
- Metric: none from the Bank (a ledger). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: the data ends in 2013 and will not be updated (`Outdated` not set: the curator's call); the same donor-fund pairs recur by quarter and instalment (SPLIT-13, SPLIT-29); the receipt currency and the pledge schedule drive the amount (USE-5); 2,990 rows over 23 years make thin temporal windows (SPLIT-14, SPLIT-17); the use case is the open question (USE-1, USE-2).
- Priority: gap 0 (finance, regression), use case 0 (none named), source + (field definitions published), shape 0 (2,990 rows of donor, fund, currency and period codes), risk - (a frozen 2013 ledger; one source cut into four tables).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 2,990 rows x 11 columns incl. target (STRABLE parquet); target: Amount in USD.
- Why: Predict the amount of a donor contribution to a Financial Intermediary Fund
- Notes: World Bank Finances One DS00051, export 2025-07-12.
