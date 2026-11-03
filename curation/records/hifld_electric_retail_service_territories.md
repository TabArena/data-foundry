---
unique_name: hifld_electric_retail_service_territories
name: Electric Retail Service Territories
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
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::electric-retail-service-territories/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/electric-retail-service-territories
- https://arxiv.org/abs/2605.12292
- '# origin of the utility data: EIA-861, yearly'
- https://www.eia.gov/electricity/data/eia861/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: one row per US electric retail utility territory with annual retail sales as STRABLE's target; no decision named, and STRABLE's paper and config name different targets.
- Source: the HIFLD Open layer "Electric Retail Service Territories" (ORNL, LANL, INL with the NGA HSIP team): "This feature class/shapefile represents electric power retail service territories. These are areas serviced by electric power utilities responsible for the retail sale of electric power to local customers, whether residential, industrial, or commercial" (copy HSEMA_PPD, ArcGIS item 1dfcc95256fa4ba5821d1025e556f24d); the sales and customer fields follow EIA-861 (the run's note; SOURCE values also name FERC Form 714 and the California Energy Commission); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 2,909 utilities x 20 columns; target TOTAL_MWH (log); the other MWh columns, NET_GEN, PURCHASED, CUSTOMERS, the winter and summer peaks and capacities dropped as leaking or "Highly related" (preprocess_HIFLD-Electric_Retail_Service_Territories.py). STRABLE Appendix C.2 (item 35): "The task is to predict the utility ownership type."
- Use case: none named; every utility reports its retail sales to EIA-861. Fit approximate at best; regime IID (one row per utility). Precedent: registry tables with a target picked by a benchmark went to `TBD -> 2nd Tier` with `No Good Target (yet)` (museums, journal_score_sjr, ai_jobs_net_salaries; Lennart).
- Siblings and duplicates: hifld_electric_generating_plants and hifld_power_plants (EIA plant data, other units and targets); no record holds EIA-861 itself. External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. EIA-861 (https://www.eia.gov/electricity/data/eia861/) is the yearly origin, with sales, revenue and customers by sector.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-Electric_Retail_Service_Territories.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on MWh, with target_transform log; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: NET_EX (filled for 1,182 of 2,909 rows; by its name the net energy exchange of the same balance, to confirm) can give part of the sales away (LEAK-10); the paper's target, the ownership TYPE, is a feature here (USE-5: settle the target first); Shape__Area and Shape__Length describe the territory polygon; HOLDING_CO, PLAN_AREA and CNTRL_AREA are names of high cardinality; which EIA-861 year the sales are from is not in the file; the HIFLD file is offline, so a rebuild goes to EIA-861 (PROV-13).
- Priority: gap -, use case -, source + (EIA-861 through ORNL, documented), shape + (2,909 utilities, 19 mixed columns), risk - (NET_EX and an unsettled target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 2,909 rows x 20 columns incl. target (STRABLE parquet); target: TOTAL_MWH.
- Why: Predict a utility's total retail sales (MWh) from its service-territory record
- Notes: HIFLD layer (EIA-861-based). Paper says 'utility ownership type'; config target is TOTAL_MWH (regression).
