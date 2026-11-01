---
unique_name: worldbank_ipf_contract_awards
name: Contract Awards IPF
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Free Text (Short)
collections:
- STRABLE
original_source: GOV Website
domain: finance
problem_type: Regression
original_data_state: One Table
source_links:
- '# 404 on 2026-10-31 after the redirect to financesone.worldbank.org (ids renumbered there); the table''s current Finances One id is not verified'
- https://finances.worldbank.org/Procurement/Contract-Awards-in-Investment-Project-Financing/DS00073
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/contract-awards-investment-project-financing
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: contracts awarded by borrowers under World Bank investment project financing, with the contract amount, the winning price, as target; a price task like a sale price, large and from the Bank's own release, but the source names no use case and STRABLE ships a 75,000-row sample.
- Source: "Contract Awards in Investment Project Financing" on the World Bank's Finances One (old id DS00073): the contracts that borrowers sign under IPF projects and report to the Bank; the year of the first release is not stated on the pages read. As published in STRABLE (schema and first rows previewed): 75,000 rows x 21 columns, as of 07/12/2025, after STRABLE "sub-sampled large tables (12/108) to a maximum of 75,000 rows" (Sec. 3): as-of date, fiscal year, region, borrower country and code, project id and name, project global practice, procurement category (Goods, Works, ...), procurement method (Request for Quotations, ...), contract number, contract description (free text, in several languages), borrower contract reference, contract signing date, supplier, supplier country and code, WB contract number, review type (Prior or Post), supplier id, the target `Supplier Contract Amount (USD)`. The full table is larger (its row count was not read). One table.
- Use case: for example a project implementation unit, when it plans a procurement, estimates the contract's cost from the category, method, country and description (the estimate decides the procurement method and whether the Bank reviews the contract before or after award); or the Bank's procurement staff flag an award far from the expected amount. Neither is named by the source, so the fit is approximate until the curator settles it (USE-8). Regime temporal by signing date (a model prices contracts not yet tendered), with projects and borrowers recurring (SPLIT-3).
- Siblings and duplicates: `worldbank_corporate_procurement_contracts` (the Bank's own corporate purchases: another table, PROV-7); `ted_public_procurement_single_bid` (EU TED award notices: another source, with an award-value target among its framings); the other World Bank Finances records of this run (`worldbank_ida_statement_of_credits`, `worldbank_ifc_advisory_projects`, `worldbank_ifc_investment_projects`, `worldbank_miga_issued_projects`, `worldbank_corporate_procurement_contracts`, the trust-fund and FIF records). External collections: STRABLE (`contract-awards-investment-project-financing`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "Contract Awards IPF", with the award amount as the task; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: the supplier, its country and id, the signing date and the contract numbers exist only after the award (LEAK-10 for a pre-tender task; an audit framing would keep them); `Review type` and `Procurement Method` follow thresholds on the estimated value: legitimate pre-tender inputs, but measure how much of the target they carry; one contract may list several suppliers or lots, so check the unit; build from the full source table, not STRABLE's sample, whose target is log-transformed (12.46 in the first row, about US$257,000); the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0, use case 0 (ours, not the source's), source + (the Bank's procurement release), shape + (75,000 or more rows, 20 mixed columns with free text), risk - (post-award columns to drop).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 21 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: Supplier Contract Amount (USD).
- Why: Predict the supplier contract amount of a World Bank-financed procurement contract
- Notes: World Bank Finances One DS00073. Subsampled by STRABLE to 75,000 rows.
