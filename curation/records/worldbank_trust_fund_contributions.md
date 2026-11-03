---
unique_name: worldbank_trust_fund_contributions
name: Total Contributions IBRD IDA IFC
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
- '# STRABLE links only the portal root; the table''s own Finances One page is not identified'
- https://finances.worldbank.org/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/total-contributions-ibrd-ida-ifc
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 7,826 donor contributions to IBRD, IDA and IFC trust funds by fiscal year of agreement; a pledge is the donor's own decision, one column is part of the target, and the table's own page is not identified.
- Source: the World Bank's Finances One; STRABLE links only the portal root (https://finances.worldbank.org/), and the run's notes give the raw file as `total_contributions_to_ibrd_ida_ifc_trust_funds_summary_based_on_fy_of_agreement_12-17-2025.csv` ("Total Contributions to IBRD, IDA and IFC Trust Funds, summary based on FY of agreement"); the table's own page and id were not identified, and the year of the first release is not known. As published in STRABLE (schema and first rows previewed): 7,826 rows x 10 columns: fund, trustee fund number and name, donor code, name and agency, fiscal year of agreement (2008 in the first rows), `Contributions Outstanding (USD)`, the target `Total Contribution (USD)`, status. One table.
- Use case: none named; the amount a donor pledges to a fund is the donor's decision, written in the agreement. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime, if a task is found, temporal by agreement year, with donors and funds recurring.
- Siblings and duplicates: `worldbank_trust_fund_commitments`, `worldbank_trust_fund_disbursements` and `worldbank_recipient_executed_grants` are cuts of the World Bank's trust-fund ledger (commitments and disbursements by fund and year, and by grant and year), this record its donor side, and `worldbank_fif_commitments`, `worldbank_fif_cash_transfers`, `worldbank_fif_contributions` and `worldbank_fif_funding_decisions` (batch 21) the same ledgers of the financial intermediary funds: processing variants or cuts of one source (PROV-6), so at most one should enter unless the curator finds distinct tasks (PROV-7); `worldbank_fif_contributions` is the FIF counterpart. External collections: STRABLE (`total-contributions-ibrd-ida-ifc`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "Total Contributions IBRD IDA IFC: Contributions to World Bank institutions by members. The task is to predict total contribution amounts.", linked to the portal root only; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: `Contributions Outstanding (USD)` is the unpaid part of the target at the export date (LEAK-10; drop it); `Status` is today's state; the table has to be found again on Finances One before anything is built (PROV-2); STRABLE ships the target transformed (15.05 in the first row, about US$3.4 million if it is a log).
- Priority: gap 0, use case 0 (none named; the actor sets the amount), source 0 (the table's own page not identified), shape + (7,826 rows, mixed columns), risk - (no decision fits the target, a column that is part of it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 7,826 rows x 10 columns incl. target (STRABLE parquet); target: Total Contribution (USD).
- Why: Predict a donor's total contribution to IBRD/IDA/IFC trust funds
- Notes: Raw file total_contributions_to_ibrd_ida_ifc_trust_funds_summary_based_on_fy_of_agreement_12-17-2025.csv; the paper links only the portal root.
