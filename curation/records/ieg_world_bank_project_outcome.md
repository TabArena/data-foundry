---
unique_name: ieg_world_bank_project_outcome
name: IEG World Bank Project Performance Ratings
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: finance
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://financesone.worldbank.org/d/DS00053
- https://datacatalog.worldbank.org/search/dataset/0038059
- https://ieg.worldbankgroup.org/ieg-data-world-bank-project-ratings-and-lessons
- https://doi.org/10.1016/j.jdeveco.2013.06.003
- https://datacatalog.worldbank.org/search/dataset/0038059/ieg-world-bank-project-performance-ratings
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the World Bank IEG's latest outcome rating for 12,643 evaluated projects (evaluation FY 1974 on, data as of 2026-10-29) with region, country, practice, instrument, agreement type and approval year; an official, open target whose prediction the Bank's economists studied (Geli, Kraay and Nobakht 2014), but with only a handful of approval-time columns, and four other IEG ratings from the same evaluation must go.
- Source: the Independent Evaluation Group (IEG) of the World Bank. Finances One DS00053 (link 1): "This dataset contains all independent assessments and validations of World Bank projects", 12,643 rows x 21 columns, CC BY 4.0, only the latest rating when a project was evaluated more than once, data as of 2026-10-29. The Data Catalog entry 0038059 carries older metadata ("more than 11,300 project assessments of more than 9,600 completed projects", coverage 1964-2014). Columns (an API preview of three rows): project_id, project_name, wb_region, country, country_fcs_status, country_fcs_lending_group, country_lending_group, global_practice, practice_group, lending_instrument_type, agreement_type (IBRD, IDA, GEF, ...), approval_fy, final_closing_fy, evaluation_fy, evaluation_type (ICRR, PPAR), outcome, bank_performance, quality_at_entry, quality_of_supervision, me_quality, as_of_date. Target `outcome`, six levels from Highly Satisfactory to Highly Unsatisfactory, usually split at Moderately Satisfactory or better; "Not Rated" values to check.
- Use case: Bank management predicting at or soon after approval which projects will end up rated unsatisfactory, to focus supervision and restructuring. Geli, Kraay and Nobakht, "Predicting World Bank Project Outcome Ratings", Policy Research Working Paper 7001 (2014): models of outcomes on characteristics observed early in a project's life, used to predict the eventual IEG ratings of active projects, beat the staff's self-assessments (abstract on RePEc; the full text returned 403). Fit approximate: their inputs include early implementation ratings and project details this table lacks. Regime temporal by approval_fy (fit on evaluated projects, used on newly approved ones); the country is a grouping candidate inside it (SPLIT-13).
- Siblings and duplicates: no other record of the IEG ratings; `worldbank_ida_statement_of_credits`, `loan_ibrd` (`TBD -> Yes`) and `ibrd_loans_historical_snapshots` (`TBD -> 2nd Tier`) hold loans that join by project id; `worldbank_fif_funding_decisions` carries the old id DS00053, which now opens this dataset (noted there). External collections: none (STRABLE holds other World Bank tables, not this one).
- Better data: found through the dead-link check of the curator's Zotero collection (item 138, World Bank Open Data); no search for better data in this run.
- Papers and pages: Denizer, Kaufmann and Kraay, "Good countries or good projects? Macro and micro correlates of World Bank project performance", J Dev Econ (2013), https://doi.org/10.1016/j.jdeveco.2013.06.003 (not read); Geli, Kraay and Nobakht 2014 (abstract read).
- Metric: none found (the WPS 7001 abstract names "in-sample and out-of-sample predictive performance" without a measure, its full text was not reachable, and the dataset pages name none), so the fallback: `roc_auc` for satisfactory against unsatisfactory, or `log_loss` on the six levels (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: bank_performance, quality_at_entry, quality_of_supervision and me_quality are rated by IEG in the same evaluation and go (LEAK); evaluation_fy, evaluation_type and final_closing_fy are known only at the end and go (USE-3); country_fcs_status and the lending groups may be today's classification rather than the one at approval (to check); the latest rating replaces earlier ones (a PPAR over an ICR review), so the label's source varies by row; few approval-time inputs without a join to the Projects API (commitment, sectors, themes, borrower, environmental category); a binary or a six-level target to choose.
- Priority: gap 0 (finance and binary are not thin), use case 0 (named by Bank economists, but approximate on this table), source + (the IEG's own open release with an API), shape + (12,643 projects, categorical inputs, five decades), risk - (four evaluation-time ratings to drop and few approval-time columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the dead-link check of the curator's Zotero collection; the curator's Zotero collection, item 138: "World Bank Open Data".
- as published: 12,643 evaluated World Bank projects x 21 columns (latest evaluation per project): project id and name, region, country, FCS status, lending group, global practice, practice group, lending ...; target: IEG outcome rating (6-point scale, Highly Satisfactory to Highly Unsatisfactory; usually binarised at Moderately Satisfactory or better); access: open.
- Why: Real, official, open (CC BY 4.0) and maintained; it is the Bank's own performance measure, published by its first publisher with an API. | An official, open project-level outcome with a decision at approval; studied in the literature (Denizer, Kaufmann and Kraay 2013).
- Adds: Development-finance project outcomes, next to loan_ibrd (which scout_16 said this would complement). Caveats: few approval-time features (region, country, FCS status, practice, instrument, agreement type, approval FY). Joining the Projects API (commitment, sectors, themes, borrower, environmental category) or country ...
