---
unique_name: worldbank_trust_fund_commitments
name: Commitments in Trust Funds
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
- https://finances.worldbank.org/Trust-Funds-and-FIFs/Commitments-in-Trust-funds/DS00072
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/commitments-in-trust-funds
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 41,243 trust-fund-by-fiscal-year rows of new commitments, described only by the fund's names and classes; a yearly flow per fund, with negative values mixed in, and no decision named.
- Source: "Commitments in Trust funds" on the World Bank's Finances One (old id DS00072; run notes: export 2025-07-13); the year of the first release is not stated on the pages read. As published in STRABLE (schema and first rows previewed): 41,243 rows x 11 columns: trust fund id and name, trust fund status, execution type (Bank Execution, IFC, ...), trustee id, status and name, fund classification, program group, fiscal year, the target `New Commitments (US$)`. The first three rows (FY2012) are negative after STRABLE's signed-log transform, so the column holds reversals or cancellations too. One table.
- Use case: none named; a fund's commitments in a fiscal year, predicted from its names and the year, is a yearly series per fund (SEL-10; in scope only if it passes TP-10), flagged `Time-series (Forecasting)` as a concern to test. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime temporal by fiscal year, with funds recurring.
- Siblings and duplicates: this record, `worldbank_trust_fund_disbursements` and `worldbank_recipient_executed_grants` are cuts of the World Bank's trust-fund ledger (commitments and disbursements by fund and year, and by grant and year), `worldbank_trust_fund_contributions` its donor side, and `worldbank_fif_commitments`, `worldbank_fif_cash_transfers`, `worldbank_fif_contributions` and `worldbank_fif_funding_decisions` (batch 21) the same ledgers of the financial intermediary funds: processing variants or cuts of one source (PROV-6), so at most one should enter unless the curator finds distinct tasks (PROV-7). External collections: STRABLE (`commitments-in-trust-funds`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "Commitments in Trust Funds", with the commitment amount as the task; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: `Trust Fund status` and `Trustee Status` are today's states (LEGALLY CLOSED on the 2012 rows), not known in the fiscal year (LEAK-10); negative and positive commitments need a target definition (USE-5); no column describes the row beyond the fund and the year; STRABLE kept every fiscal year, unlike its own snapshot statement (Sec. 3); the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified, and the run found DS00072 answering 404 on 2026-10-30.
- Priority: gap 0, use case 0 (none named), source + (the World Bank's own release), shape + (41,243 rows, a panel by fund and year), risk - (a forecasting-like panel with an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 41,243 rows x 11 columns incl. target (STRABLE parquet); target: New Commitments (US$).
- Why: Predict the new commitment amount of a World Bank trust fund ledger entry
- Notes: World Bank Finances One DS00072, export 2025-07-13. The finances.worldbank.org links now redirect to financesone.worldbank.org (DS00072 returned 404 on 2026-10-30).
