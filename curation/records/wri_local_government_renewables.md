---
unique_name: wri_local_government_renewables
name: Local Government Renewable Action
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
original_source: Website
year: '2022'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.wri.org/data/local-government-renewables-action-tracker
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/local-government-renewable-action
- https://arxiv.org/abs/2605.12292
- https://cityrenewables.org/local-government-renewables-action-tracker/
- '# December 2022 release on the WRI data portal (XLSX; sheets Metadata, Transaction Data, Engagement Data)'
- https://datasets.wri.org/private-admin/dataset/a2c1721a-8be6-49af-836f-48f0779dff49/resource/428b5649-5208-4197-bd09-238e17b699d7/download/local_government_renewables_action_tracker_dec_2022.xlsx
- https://www.wri.org/research/accc-local-government-renewables-action-tracker-summary-methods-and-data
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a documented RMI and WRI catalogue of 1,333 US local-government renewable electricity deals (2015 to mid-2022), compiled so peers can learn from each other; the deal size STRABLE predicts has no decision behind it, and a generation column copies it.
- Source: RMI and WRI, American Cities Climate Challenge Renewables Accelerator; Abbott et al. 2022, "Local Government Renewables Action Tracker" (citation in the file's Metadata sheet), methods in Shaver, Abbott and House, technical note of June 2020 (https://www.wri.org/research/accc-local-government-renewables-action-tracker-summary-methods-and-data). The file on the WRI data portal is `local_government_renewables_action_tracker_dec_2022.xlsx`, "Dataset last updated: December 21, 2022", temporal coverage "January 1, 2015 - June 30, 2022", update frequency "Semi-annual", CC BY 4.0; `year` is set to that snapshot, 2022 (PROV-9). As published: three sheets, Metadata, Transaction Data (1,333 deals x 29 columns: buyer, state, city coordinates, ISO or FERC region, announcement year and date, technology, transaction type, Size of Purchase (MW), DC/AC, contract length, year-1 energy price, utility, developer, project name, location and state, operation start year, Estimated Annual Generation (MWh), five source URLs, notes) and Engagement Data (62 advocacy actions). STRABLE takes the transaction sheet as published, target ln(MW). The record's first link (wri.org/data) returns 404 on 2026-10-31; the portal file and https://cityrenewables.org/local-government-renewables-action-tracker/ work.
- Use case: none stated: the Tracker's goals are "to help local governments learn from what others have accomplished" and to let others "assess the range of local government actions on renewables and the cumulative impact" (Metadata sheet); its cautions say it rests on "press releases, statements from parties within a transaction, or local media coverage" and is not comprehensive. No actor predicts a deal's MW from these columns before it is signed; a listing without a predictive target (`No Good Target (yet)`). Regime temporal by announcement year if a use case is found; jointly bought projects then need care.
- Siblings and duplicates: no record links the Tracker or cityrenewables.org; `wri_global_power_plant_database` and `wri_china_overseas_finance_inventory` are other WRI energy tables, distinct data. External collections: STRABLE (config `local-government-renewable-action`, paper row 69: "The task is to predict project capacity").
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the technical note above; the online tool on cityrenewables.org; STRABLE, Blayer et al. 2026 (https://arxiv.org/abs/2605.12292), App. C.4. The Metadata sheet names the EPA Green Power Partnership's list of long-term power purchases as one input.
- Metric: none found (the Metadata sheet, the WRI data portal, the technical note page); STRABLE's R^2 on its transformed scale (App. D.1, "Evaluation metrics") is a benchmark-wide choice, so the fallback `rmse` on log MW; inputs none (MET-1, MET-5).
- Risks for /add-dataset: `Estimated Annual Generation (MWh)` is filled for 343 deals and its log correlates 0.94 with log MW (size times a capacity factor), so it goes (LEAK-10); 170 rows share one of 55 project names (the two Florida Municipal Solar Power Project phases have 12 buyers each, with different shares), so a project spans folds (LEAK-17); `Operation Start Year` and the generation estimate may postdate the announcement (LEAK-10); the source URLs and notes are free text.
- Priority: gap 0, use case 0, source + (RMI and WRI, with a methods note), shape 0 (1,333 rows, not comfortably above the floor), risk - (a target no decision rests on, and a column that copies it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,333 rows x 29 columns incl. target (STRABLE parquet); target: Size of Purchase (MW).
- Why: Predict the size (MW) of a US local government's renewable energy purchase
- Notes: Raw file local_government_renewables_action_tracker_dec_2022.xlsx (WRI).
