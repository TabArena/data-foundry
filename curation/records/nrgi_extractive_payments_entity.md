---
unique_name: nrgi_extractive_payments_entity
name: Industry Payments Entity
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
original_source: Website
domain: finance
problem_type: Regression
original_data_state: One Table
source_links:
- https://energydata.info/dataset/ei-payments-to-governments
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/industry-payments-entity
- https://arxiv.org/abs/2605.12292
- '# the publisher, NRGI''s ResourceProjects.org (energydata.info above returns 403 to scripted access on 2026-10-31)'
- https://resourceprojects.org/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: payments that oil, gas and mining companies disclosed to governments under mandatory reporting laws, by recipient government entity; transparency data with no predictive target, and the project-level table is another cut of the same reports.
- Source: the Natural Resource Governance Institute (NRGI), ResourceProjects.org (https://resourceprojects.org/about): payments "over USD 100,000" of "taxes, royalties, fees or production entitlements", disclosed under laws in Canada, the European Union, Norway, the United Kingdom and Switzerland; companies first reported in 2015, NRGI paused collection in 2021 (latest data 2020); NRGI standardises names and converts amounts to USD; the purpose of the disclosure: to "improve accountability and deter corruption". STRABLE downloaded it from energydata.info, "World - Extractive Industry Payments to Governments" (that page returns 403 to us; not read). STRABLE (energyinfo/entity.csv; parquet previewed 2026-10-31): 31,448 rows x 9 columns, report years 2014-2020 (11,986 rows paid to Canadian entities); target `entityPayment` (log-type scale); inputs source report id, reporting company (914), report year, entity country, entity name, payment type, NRGI's cleaning notes and the company's notes (71% missing).
- Use case: none named; the payments are disclosed facts. A civil-society analyst flagging a company whose payments fall far below those of similar companies would be a stand-in (approximate at best). Regime temporal by report year, grouped by company.
- Siblings and duplicates: `nrgi_extractive_payments_project` (the same reports by project: 2,494 report ids shared, of 2,690 here and 2,575 there), a cut of the same data with the same kind of target (PROV-6): at most one of the two enters. External collections: STRABLE (arXiv 2605.12292), "Industry Payments Entity": the paper describes "Payments made by drug and device companies to teaching hospitals" and links CMS Open Payments, while STRABLE's config and data are NRGI's extractive payments (an error of the copy, PROV-15).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: ResourceProjects.org; STRABLE's script `preprocess_energyinfo-industry-payments-entity.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the NRGI page, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` on the USD amount, shipped on a log scale (MET-3, MET-8); inputs none.
- Risks for /add-dataset: no target (SEL-3, `No Good Target (yet)`); the company's `notes` sometimes restate amounts ("Royalties include $3,840,000 of royalties paid-in-kind ...", LEAK checks); `sourceID` is a report id; the entity and project cuts report the same payments twice (PROV-6); NRGI advises users "to check against original sources before making serious decisions".
- Priority: gap 0 (finance not thin), use case 0 (none named), source + (NRGI page describing its method), shape + (31,448 payments, a year axis), risk - (no target; a cut shared with the project table).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 31,448 rows x 9 columns incl. target (STRABLE parquet); target: entityPayment.
- Why: Predict the payment an extractive-industry company makes to a government (entity level)
- Notes: Mismatch: the paper describes and links CMS Open Payments, but the config source is energydata.info and the raw file energyinfo/entity.csv matches 'World - Extractive Industry Payments to Governments' (Natural Resource Governance Institute; resources 'Entity-level payments' and 'Project-level payments').

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: two cuts of the same payment reports (`nrgi_extractive_payments_project`; PROV-6). The curator keeps one, or both as distinct tasks.
