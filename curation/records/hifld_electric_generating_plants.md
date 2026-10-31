---
unique_name: hifld_electric_generating_plants
name: Electric Generating Plants
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
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::power-plants/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/electric-generating-plants
- https://arxiv.org/abs/2605.12292
- '# origin of the plant data: EIA-860 (generators) and EIA-923 (generation and fuel), yearly'
- https://www.eia.gov/electricity/data/eia860/
- https://www.eia.gov/electricity/data/eia923/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: plant-level EIA data through HIFLD with annual net generation as STRABLE's target; the same plants as hifld_power_plants, no decision named, and the same year's fuel consumption among the features.
- Source: the HIFLD Open layer "Power Plants" (ORNL, LANL, INL with the NGA HSIP team): "This feature class/shapefile represents electric power plants ... Included are the following plant types: hydroelectric dams, fossil fuel (coal, natural gas, or oil), nuclear, solar, wind, geothermal, and biomass" (copy in FEMA Region 9's ArcGIS item f94815f3967e4277ab3315c81142f15c), built from EIA-860 and EIA-923 (SOURCE "EIA 860", plus state sources such as the California Energy Commission; SOURCEDATE 2011-2023); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 8,849 operating plants (STATUS "OP", NET_GEN > 0) x 38 columns; target NET_GEN (log); every column with "CAP" in its name dropped as "Highly related" (preprocess_HIFLD-electric-generating-plants.py, raw file Power_Plants_gdb_-7934110650112012255.xlsx). STRABLE Appendix C.2 (item 34): "Operational characteristics of power plants in the US. The task is to predict net generation capacity."
- Use case: none named; net generation is reported to EIA-923 for every plant. An analyst estimating the output of a plant without a reported figure would start from its capacity, which STRABLE removed; fit approximate at best; regime IID (one row per plant, one snapshot), temporal if rebuilt from the EIA-923 years. Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: hifld_power_plants (a generator-level file from a HIFLD download also named Power_Plants_gdb, at the same start link; 8,658 of these 8,849 plant codes are among its 11,310 plants; target nameplate capacity): two cuts of one EIA inventory with different targets, PROV-6 or PROV-7 for the curator; wri_global_power_plant_database (capacity and generation per plant, US rows from EIA); hifld_electric_retail_service_territories (EIA utility data). External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. EIA-860 and EIA-923 are the yearly origin, for every plant and year.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-electric-generating-plants.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on MWh, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: COAL_USED, NGAS_USED and OIL_USED are fuel consumption, likely of the same year as NET_GEN (EIA-923), which fixes generation for fossil plants through the heat rate (LEAK-10); the year of NET_GEN is not in the file; without capacity, solar and wind plants keep few size signals; SOURCE_LAT/SOURC_LONG and x/y repeat the coordinates; the HIFLD file is offline, so a rebuild goes to EIA (PROV-13).
- Priority: gap -, use case -, source + (EIA through ORNL, documented), shape + (8,849 plants, 37 mixed columns), risk - (same-period fuel consumption; an overlapping cut of hifld_power_plants).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 8,849 rows x 38 columns incl. target (STRABLE parquet); target: NET_GEN.
- Why: Predict a US power plant's net generation
- Notes: HIFLD Power Plants layer (EIA-based). Same HIFLD layer family as 'Power Plants' (row 87), different file and target.
