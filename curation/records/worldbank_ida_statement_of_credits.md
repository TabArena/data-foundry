---
unique_name: worldbank_ida_statement_of_credits
name: IDA Statement of Credits
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
original_data_state: One Table
source_links:
- '# 404 on 2026-10-31 after the redirect to financesone.worldbank.org (ids renumbered there); the table''s current Finances One id is not verified'
- https://finances.worldbank.org/Loans-and-Credits/IDA-Statement-of-Credits-and-Grants-Latest-Availabl/DS00048
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/ida-statement-credits-grants-guarantees
- https://arxiv.org/abs/2605.12292
- https://datacatalog.worldbank.org/search/dataset/0037714
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: an official World Bank ledger of 7,766 IDA credits, grants and guarantees, but STRABLE's target, the original principal, is the amount the Bank and the borrower agree at approval, and no decision rests on predicting it.
- Source: the World Bank's Finances One (formerly finances.worldbank.org), "IDA Statement of Credits, Grants and Guarantees - Latest Available Snapshot" (data catalog 0037714: monthly, CC BY 4.0; "IDs starting with IDAB or IDAG are guarantees", IDAD, IDAH or IDAE grants, the rest credits); the year of the first release is not stated on the pages read. The publisher also releases the monthly history from April 2011 (Finances One DS00976, catalog 0037713), the IDA counterpart of `ibrd_loans_historical_snapshots`; the run's notes say STRABLE's raw file was that historical export (2025-07-14). As published in STRABLE (parquet schema and first rows previewed): 7,766 rows x 19 columns: end of period, credit number, region, country code and name, borrower, credit status, service charge rate, currency of commitment, project id and name, the target `Original Principal Amount (US$)`, first and last repayment dates, agreement signing, board approval, effective, closing and last disbursement dates. STRABLE dropped the ledger's other amounts (cancelled, undisbursed, disbursed, repaid, due), so the accounting identity that sums them to the principal is not in the table. One table.
- Use case: none named. STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 says "The task is to predict the disbursement status", while its config predicts the original principal. The principal is the commitment fixed at approval, so when the features exist the amount is already set; a planning estimate of a credit's size before negotiation would be ours to write and would need inputs known then (the country's IDA allocation and terms), not the repayment schedule. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2). Regime, if a task is found: temporal by board approval date. STRABLE treats all tables as IID (Sec. 3: "we adopted a snapshot strategy—extracting only the most recent available year of data"), yet the first three rows carry end-of-period dates in 2014, 2017 and 2019, so how STRABLE cut the snapshot needs checking.
- Siblings and duplicates: `loan_ibrd` (IBRD statement of loans, TBD -> Yes by Lennart: "Unsure if this is a reasonable task") and `ibrd_loans_historical_snapshots` are the IBRD counterparts, another institution and table, so siblings, not duplicates (PROV-7); STRABLE carries the IBRD statement too, as a loan-status task. `ieg_world_bank_project_outcome` (IEG outcome ratings, a target with a decision) could be joined by project id. Also the other World Bank Finances records of this run (`worldbank_ifc_advisory_projects`, `worldbank_ifc_investment_projects`, `worldbank_miga_issued_projects`, `worldbank_ipf_contract_awards`, `worldbank_corporate_procurement_contracts`, the trust-fund and FIF records). External collections: STRABLE (`ida-statement-credits-grants-guarantees`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE App. C.1 entry "IDA Statement of Credits: Records of credits, grants, and guarantees issued by IDA."; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: the target is unclear (the paper's status task against the config's principal, USE-5); `Credit Status`, the effective, closing and last disbursement dates and `End of Period` describe the credit after approval (LEAK-10 for an approval-time task); STRABLE ships the target transformed (Sec. 3, the skewness-minimising transform; the first row's 501.99 looks like the cube root of about US$126.5 million), so take the raw amount from the source; the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0 (finance, regression and IID are not thin), use case 0 (none named, and the actor sets the amount), source + (the World Bank's own catalogued release), shape + (7,766 rows, 18 mixed columns), risk - (unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,766 rows x 19 columns incl. target (STRABLE parquet); target: Original Principal Amount (US$).
- Why: Predict the original principal amount of an IDA credit, grant or guarantee
- Notes: Raw file is the historical-data export (2025-07-14). Paper says 'disbursement status'; config target is Original Principal Amount. Sibling of loan_ibrd.
