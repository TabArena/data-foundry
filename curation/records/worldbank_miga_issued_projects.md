---
unique_name: worldbank_miga_issued_projects
name: MIGA Issued Projects
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
- '# 404 on 2026-10-31 after the redirect to financesone.worldbank.org (ids renumbered there); the table''s current Finances One id is not verified'
- https://finances.worldbank.org/Guarantees/MIGA-Issued-Projects/DS00030
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/miga-issued-projects
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 619 MIGA guarantee projects; the gross issued amount is MIGA's own underwriting decision, not an outcome anyone predicts, STRABLE's paper names another target, and the table is small.
- Source: "MIGA Issued Projects" on the World Bank's Finances One (old id DS00030; run notes: export 2025-07-13), compiled from MIGA's project pages (miga.org links in the table); the year of the first release is not stated on the pages read. As published in STRABLE (schema and first rows previewed): 619 rows x 14 columns: issued fiscal year (2012 in the first rows), project id and name, host country and region with codes, business sector, product line (PRI, NH), the target `Gross Issued Amount (US$)`, project start and expiration dates, project links, `Issued_Proj_Count`. One table.
- Use case: none named; MIGA decides how much cover to issue, and the amount is published with the project. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime, if a task is found, temporal by issued fiscal year.
- Siblings and duplicates: the other World Bank Finances records of this run (`worldbank_ida_statement_of_credits`, `worldbank_ifc_advisory_projects`, `worldbank_ifc_investment_projects`, `worldbank_ipf_contract_awards`, `worldbank_corporate_procurement_contracts`, the trust-fund and FIF records); none is the same table. External collections: STRABLE (`miga-issued-projects`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 entry "MIGA Issued Projects: Projects supported by MIGA investment guarantees. The task is to predict the maximum gross exposure." (the config predicts the gross issued amount); no paper that models this table was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (a ledger release with no task; nothing on the dataset pages we could read); STRABLE scores every regression table by R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice, not one made for this task; so the fallback `rmse` on the amount, with the shipped scale settled at /add-dataset (MET-1, MET-3, MET-5); inputs none.
- Risks for /add-dataset: the target is unclear (maximum gross exposure in the paper, gross issued amount in the config, USE-5); `Project Links` point to the pages that state the amount; `Issued_Proj_Count` is undocumented; STRABLE ships the target transformed (529.55 in the first row, about US$148.5 million if it is a cube root); 619 rows with few informative columns; the STRABLE link (finances.worldbank.org/<category>/<title>/<id>) answers 404 after its redirect to financesone.worldbank.org, which renumbered its ids and answers 200 for any single-slug URL, so the table's current id is not verified.
- Priority: gap 0, use case 0 (none named; the actor sets the amount), source + (the World Bank Group's own release), shape 0 (619 rows), risk - (unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 619 rows x 14 columns incl. target (STRABLE parquet); target: Gross Issued Amount (US$).
- Why: Predict the gross issued guarantee amount of a MIGA project
- Notes: World Bank Finances One DS00030, export 2025-07-13. Small: 619 rows.
