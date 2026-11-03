---
unique_name: worldbank_ifc_advisory_projects
name: IFC Advisory Projects
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
- https://finances.worldbank.org/Advisory-Services/IFC-Advisory-Services-Projects/DS00010
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/ifc-advisory-services-projects
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 1,885 disclosed IFC advisory projects with their estimated budget; the budget is IFC's own figure, published together with the project, so no decision rests on predicting it.
- Source: IFC's project disclosures (disclosures.ifc.org, one page per project, linked in the table), compiled as "IFC Advisory Services Projects" on the World Bank's Finances One (old id DS00010; run notes: export 2025-07-13); the year of the first release is not stated on the pages read. As published in STRABLE (schema and first rows previewed): 1,885 rows x 13 columns: disclosure date, project number, name and URL, country, IFC and WB country codes, IFC region, business line, the target `Estimated Total Budget ($)`, status (Active, Hold, Completed), IFC approval date, projected start date. One table.
- Use case: none named. IFC sets an advisory project's budget when it designs the project and discloses it on the project page; nobody predicts it from the country and business line. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime, if a task is found, temporal by approval date.
- Siblings and duplicates: `worldbank_ifc_investment_projects` (IFC's investment disclosures: another table and target, PROV-7); the other World Bank Finances records of this run (`worldbank_ida_statement_of_credits`, `worldbank_ifc_investment_projects`, `worldbank_miga_issued_projects`, `worldbank_ipf_contract_awards`, `worldbank_corporate_procurement_contracts`, the trust-fund and FIF records). External collections: STRABLE (`ifc-advisory-services-projects`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "IFC Advisory Projects: Metadata on advisory services provided by the IFC. The task is to predict the project budget."; no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: `Project URL` repeats the number and name and points to the page that states the budget (drop it); `Status` is today's state, not the state at approval (LEAK-10); few informative columns (country, region, business line, name, dates); STRABLE ships the target transformed (144.22 in the first row, about US$3.0 million if it is a cube root); the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0, use case 0 (none named; the actor sets the amount), source + (IFC's disclosure portal documents each project), shape + (1,885 rows, mixed and dated columns), risk - (no decision fits the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,885 rows x 13 columns incl. target (STRABLE parquet); target: Estimated Total Budget ($).
- Why: Predict the estimated total budget of an IFC advisory services project
- Notes: World Bank Finances One DS00010, export 2025-07-13.
