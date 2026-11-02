---
unique_name: wri_china_overseas_finance_inventory
name: China Overseas Finance Inventory
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
original_source: Other
year: '2022'
problem_type: Regression
original_data_state: One Table
source_links:
- '# 404 on 2026-10-31; the data is on datasets.wri.org (link below)'
- https://www.wri.org/data/china-overseas-finance-inventory-database
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/china-overseas-finance-inventory
- https://arxiv.org/abs/2605.12292
- https://datasets.wri.org/dataset/cofi
- https://doi.org/10.46830/writn.21.00003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 550 rows of a documented inventory of Chinese-financed overseas power investments; STRABLE's target, installed capacity, is a design fact of the plant that a shipped id links to the Global Power Plant Database, and its paper names another target.
- Source: the China Overseas Finance Inventory (COFI) of WRI with Boston University's Global Development Policy Center, the Inter-American Dialogue and the China-Africa Research Initiative at Johns Hopkins: technical note by Zhou, Ma, Liu, Ma, Acker, Myers, Brautigam and Gallagher, 2022-02-22, doi 10.46830/writn.21.00003 ("655 investments in 575 power plants", merged from nine source databases). Versions 1, 2, 2.1 and 2.2 are on https://datasets.wri.org/dataset/cofi, which says "This version omits all equity investment amounts" and "Our database records the loan commitment for a certain year and not actual disbursement"; the run's notes name v2.2 (Oct 2023). As published in STRABLE (schema read): 550 rows x 51 columns: plant name, country, region, subregion, province, city, the target `installed_capacity`, commissioning year, primary fuel, latitude and longitude, investment type, debt, equity and total investment amounts, investor names and amounts, investment years, SOE or POE, number of lenders, one column per Chinese bank, and the ids of the source databases (`gppd_id`, `cgp_id`, `sais_id`, `iad_id`, ...). One table.
- Use case: none named. STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19) App. C.1 says "The task is to predict the total investment amount", while the config predicts installed capacity. A plant's capacity is set in its design, before any financing is recorded, and `wri_global_power_plant_database` records the same quantity (`capacity_mw`) for 34,936 plants; estimating an undisclosed financing amount would be a real need, but it is not what the config ships. Fit none as shipped (`No Good Target (yet)`, USE-1, USE-2); regime grouped by plant if several investments share a plant.
- Siblings and duplicates: `wri_global_power_plant_database` (WRI's GPPD: another source, the same target quantity, linked through `gppd_id`; PROV-7, not a duplicate); `wri_local_government_renewables` and `wri_us_school_bus_fleets` are other WRI tables in STRABLE with unrelated tasks. External collections: STRABLE (`china-overseas-finance-inventory`).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the COFI technical note (https://doi.org/10.46830/writn.21.00003; page https://www.wri.org/research/china-overseas-finance-inventory-database); STRABLE App. C.1; no paper that models COFI as a prediction task was found (the run's web-search budget was used up during this batch).
- Metric: none from the publisher (an inventory, no task); STRABLE scores R² "reported on the transformed scale" (App. D.1), one benchmark-wide choice; so the fallback `rmse` (MET-1, MET-5); inputs none.
- Risks for /add-dataset: the target is unclear (the paper's investment amount against the config's capacity, USE-5); `gppd_id` indexes the capacity in GPPD, a lookup of the target (LEAK-10 in kind); STRABLE has equity amount columns while the WRI page says the release omits equity amounts, so check which version STRABLE used; 550 rows against 655 investments in 575 plants: check the unit; the record's wri.org/data link answers 404 (the data moved to datasets.wri.org).
- Priority: gap 0, use case 0 (none named), source + (a technical note with a DOI), shape 0 (550 rows), risk - (unclear target, a lookup id).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 550 rows x 51 columns incl. target (STRABLE parquet); target: installed_capacity.
- Why: Predict the installed capacity of a Chinese-financed overseas power project
- Notes: WRI/Boston University COFI v2.2 (Oct 2023). Paper says 'total investment amount'; config target is installed_capacity. Small: 550 rows.
