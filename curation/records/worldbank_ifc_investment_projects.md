---
unique_name: worldbank_ifc_investment_projects
name: IFC Investment Projects
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
- https://finances.worldbank.org/Investment-Services/IFC-Investment-Services-Projects/DS00011
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/ifc-investment-service-projects
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 6,328 disclosed IFC investment projects; the target, the investment the Board approved, is IFC's own decision and is stated in the same disclosure as the features, so no decision rests on predicting it.
- Source: IFC's Summary of Investment Information pages (disclosures.ifc.org, linked in the table), compiled as "IFC Investment Services Projects" on the World Bank's Finances One (old id DS00011; run notes: export 2025-07-12); the year of the first release is not stated on the pages read. As published in STRABLE (schema and first rows previewed): 6,328 rows x 19 columns: date disclosed, project name, document type, project number and URL, product line (Loan, Equity, ...), company name, country, IFC and WB country codes, industry, environmental category, department, status, projected board date, IFC approval, signed and invested dates, the target `Total IFC investment as approved by Board(Million - USD)`. One table.
- Use case: none named. The project page of the first row (BOP EU Tchad, 45483) lists the IFC investment as "1.03 million (USD)", marks the figures as indicative, and says the summary "is distributed in advance of IFC Board of Directors' consideration": the amount is IFC's proposal, published with the project, not an outcome anyone predicts. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime, if a task is found, temporal by disclosure date.
- Siblings and duplicates: `worldbank_ifc_advisory_projects` (IFC's advisory disclosures: another table and target, PROV-7); the other World Bank Finances records of this run (`worldbank_ida_statement_of_credits`, `worldbank_ifc_advisory_projects`, `worldbank_miga_issued_projects`, `worldbank_ipf_contract_awards`, `worldbank_corporate_procurement_contracts`, the trust-fund and FIF records). External collections: STRABLE (`ifc-investment-service-projects`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "IFC Investment Projects: Records of investment projects undertaken by the IFC. The task is to predict the investment amount."; the IFC project page https://disclosures.ifc.org/project-detail/SII/45483/bop-eu-tchad; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: `Project Url` points to the page that states the amount (drop it); the signed and invested dates and `Status` come after approval (LEAK-10); STRABLE ships log1p of the target (0.708 in the first row is log1p(1.03), the BOP EU Tchad amount), so take the raw amount from the source; the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0, use case 0 (none named; the actor sets the amount), source + (IFC's disclosure portal documents each project), shape + (6,328 rows, 18 mixed and dated columns), risk - (no decision fits the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 6,328 rows x 19 columns incl. target (STRABLE parquet); target: Total IFC investment as approved by Board(Million - USD).
- Why: Predict the board-approved IFC investment of a project
- Notes: World Bank Finances One DS00011, export 2025-07-12.
