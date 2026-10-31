---
unique_name: worldbank_recipient_executed_grants
name: Recipient Executed Grants
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Time-series (Forecasting)
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
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Recipient-executed-grants-commitments-disbursement/DS00075
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/recipient-executed-grants-commitments-disbursements
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 7,390 grant-by-fiscal-year rows of trust-fund grants that recipients execute; the target is one year's disbursement of a grant, a yearly flow of a series, and no decision is named.
- Source: "Recipient executed grants commitments disbursements" on the World Bank's Finances One (old id DS00075; run notes: export 2025-07-12); the year of the first release is not stated on the pages read. As published in STRABLE (schema and first rows previewed): 7,390 rows x 15 columns: beneficiary code and name, trustee fund number and name, grant fund number and name, program code and name, fiscal year, `Grant Commitments USD`, the target `Disbursements USD (Trust funds)`, grant agreement date, status, project id and description. The same grant appears in several fiscal years (TF010024 in FY2012 and twice in FY2013 in the first rows). One table.
- Use case: none named. A trust-fund manager forecasting a grant's disbursement in the coming fiscal year would be a forecast of a series per grant, out of scope unless it passes TP-10 (SEL-10, SEL-11); flagged `Time-series (Forecasting)` as a concern to test, not a finding. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime temporal by fiscal year, with grants recurring.
- Siblings and duplicates: `worldbank_trust_fund_commitments`, `worldbank_trust_fund_disbursements` and this record are cuts of the World Bank's trust-fund ledger (commitments and disbursements by fund and year, and by grant and year), `worldbank_trust_fund_contributions` its donor side, and `worldbank_fif_commitments`, `worldbank_fif_cash_transfers`, `worldbank_fif_contributions` and `worldbank_fif_funding_decisions` (batch 21) the same ledgers of the financial intermediary funds: processing variants or cuts of one source (PROV-6), so at most one should enter unless the curator finds distinct tasks (PROV-7). External collections: STRABLE (`recipient-executed-grants-commitments-disbursements`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "Recipient Executed Grants: Commitments and disbursements for grants executed by recipients. The task is to predict grant value." (the config predicts the year's disbursements, not the grant's value); no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: the target is unclear (USE-5); the same row's `Grant Commitments USD` and the grant's status are recorded in or after the year of the disbursement (LEAK-10); several rows per grant and fiscal year, so check the unit; STRABLE ships the target transformed (16.10 in the first row looks like the log of about US$9.8 million); the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0, use case 0 (none named), source + (the World Bank's own release), shape + (7,390 rows, mixed columns, a panel by grant and year), risk - (a forecasting-like panel with an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,390 rows x 15 columns incl. target (STRABLE parquet); target: Disbursements USD (Trust funds).
- Why: Predict the trust-fund disbursements of a recipient-executed grant
- Notes: World Bank Finances One DS00075, export 2025-07-12. Disbursements may be close to commitments in the same row; check.
