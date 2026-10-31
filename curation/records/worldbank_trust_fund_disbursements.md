---
unique_name: worldbank_trust_fund_disbursements
name: Disbursements in Trust Funds
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
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Disbursements-in-Trust-Funds/DS00074
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/disbursements-in-trust-funds
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: cash disbursements of World Bank trust funds by fund and fiscal year, described only by the fund's names and classes; a yearly flow per fund, no decision named, and STRABLE ships a 75,000-row sample.
- Source: "Disbursements in Trust Funds" on the World Bank's Finances One (old id DS00074; run notes: export 2025-07-13); the year of the first release is not stated on the pages read. As published in STRABLE (schema read; the rows did not load in time): 75,000 rows x 11 columns, after STRABLE "sub-sampled large tables (12/108) to a maximum of 75,000 rows" (Sec. 3): trust fund id, name and status, trustee id, status and name, fund classification, program group, execution type, fiscal year, the target `Cash Disbursements (US$)`. The full table is larger (its row count was not read). One table.
- Use case: none named; a fund's cash disbursement in a fiscal year, predicted from its names and the year, is a yearly series per fund (SEL-10; in scope only if it passes TP-10), flagged `Time-series (Forecasting)` as a concern to test. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime temporal by fiscal year, with funds recurring.
- Siblings and duplicates: `worldbank_trust_fund_commitments`, this record and `worldbank_recipient_executed_grants` are cuts of the World Bank's trust-fund ledger (commitments and disbursements by fund and year, and by grant and year), `worldbank_trust_fund_contributions` its donor side, and `worldbank_fif_commitments`, `worldbank_fif_cash_transfers`, `worldbank_fif_contributions` and `worldbank_fif_funding_decisions` (batch 21) the same ledgers of the financial intermediary funds: processing variants or cuts of one source (PROV-6), so at most one should enter unless the curator finds distinct tasks (PROV-7). External collections: STRABLE (`disbursements-in-trust-funds`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "Disbursements in Trust Funds", with the disbursement amount as the task; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: `Trust Fund status` and `Trustee Status` are today's states, not known in the fiscal year (LEAK-10); no column describes the row beyond the fund and the year; the unit (one row per fund and year, or per payment) is to be checked on the full table, not on STRABLE's sample; STRABLE ships the target transformed; the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0, use case 0 (none named), source + (the World Bank's own release), shape + (75,000 or more rows, a panel by fund and year), risk - (a forecasting-like panel with an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 11 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: Cash Disbursements (US$).
- Why: Predict the cash disbursement amount of a World Bank trust fund payment
- Notes: World Bank Finances One DS00074, export 2025-07-13. Subsampled by STRABLE to 75,000 rows.
