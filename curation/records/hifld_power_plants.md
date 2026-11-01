---
unique_name: hifld_power_plants
name: Power Plants
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
domain: industry & manufacturing
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::power-plants/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/power-plants
- https://arxiv.org/abs/2605.12292
- '# origin of the generator data: EIA-860, yearly'
- https://www.eia.gov/electricity/data/eia860/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: generator-level EIA-860 data through HIFLD with nameplate capacity as STRABLE's target; a rating every generator reports, no decision named, and it overlaps hifld_electric_generating_plants and wri_global_power_plant_database.
- Source: a HIFLD Open download named Power_Plants_gdb (STRABLE's raw file Power_Plants_gdb_1241944218131586886.xlsx), at the same start link as hifld_electric_generating_plants (geoplatform::power-plants), but one row per generator (ID = plant code and generator id; 23,093 generators of 11,310 plants after STATUS "OP" and NAMPLT_CAP > 0) with prime mover, fuels and their transport, operating month (RUN_DATE 1891 to 2022) and planned retirement (RET_DATE): EIA-860 generator fields. Which HIFLD layer this was could not be confirmed: the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 23,093 x 21; target NAMPLT_CAP (log); the other "CAP" columns dropped (preprocess_HIFLD-Power-plants.py). STRABLE Appendix C.2: "Details on fuel type and location of US power plants. The task is to predict the energy source."
- Use case: none named; nameplate capacity is the generator's rating, reported to EIA-860 before it operates. Fit approximate at best; regime grouped by PLANT_CODE (the generators of one plant share name, operator and often identical units). Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: hifld_electric_generating_plants (plant-level, 8,658 of its 8,849 plants are here; target net generation): two cuts of one EIA inventory, PROV-6 or PROV-7 for the curator; wri_global_power_plant_database (capacity_mw per plant, the same quantity at plant level, US rows from EIA). External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. EIA-860 (https://www.eia.gov/electricity/data/eia860/) is the yearly origin, with every generator and its attributes.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-Power-plants.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on MW, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: STRABLE's paper names another task (the energy source, USE-5); identical units of one plant leak across a random split (group by PLANT_CODE); NAME holds the generator id, PLANT the plant name; the HIFLD file is offline, so a rebuild goes to EIA-860 (PROV-13).
- Priority: gap -, use case -, source + (EIA-860 through HIFLD), shape + (23,093 generators, grouped by plant), risk - (an overlapping cut of hifld_electric_generating_plants; the HIFLD layer unconfirmed).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 23,093 rows x 21 columns incl. target (STRABLE parquet); target: NAMPLT_CAP.
- Why: Predict a US power plant's nameplate capacity
- Notes: HIFLD Power Plants layer. Paper says 'energy source'; config target is NAMPLT_CAP (regression). Same layer family as row 34.
