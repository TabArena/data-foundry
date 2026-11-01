---
unique_name: hifld_historic_wildfire_perimeters
name: Historic Perimeters Wildfires
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
domain: environmental science & climate
problem_type: Regression
original_data_state: One Table
source_links:
- https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::historic-perimeters-wildfires/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/historic-perimeters-wildfires
- https://arxiv.org/abs/2605.12292
- '# first release: NIFC''s historic GeoMAC perimeters 2000-2018 (file geodatabase, NIFC_Admin, created 2019-11-14)'
- https://www.arcgis.com/home/item.html?id=5b3ff19978be49208d41a9d9a461ecfb
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: GeoMAC fire perimeters of 2000-2018 with the mapped area as target, but the features are the incident's administrative record rather than conditions at ignition, several perimeters belong to one fire, and the same target with ignition-time covariates already has a record (fpa_fod_attributes_wildfire_size).
- Source: GeoMAC, released by NIFC as "Historic_Geomac_Perimeters_All_Years_2000_2018" (owner NIFC_Admin, ArcGIS item 5b3ff19978be49208d41a9d9a461ecfb, created 2019-11-14) and redistributed by HIFLD Open as "Historic Perimeters Wildfires" (STRABLE's raw file Historic_Geomac_Perimeters_Combined_2000_2018_7623284232327154878.csv); the start link no longer resolves to a dataset (the ArcGIS Hub API returns none for its slug and the HIFLD organisation's feature services no longer list the layer, 2026-10-31; a PEMA backup item says "This data is being discontinued by HIFLD", ArcGIS item 18fb153120624222a96b4d7aade54e0e, 2025-08-25). As published in STRABLE: 23,776 perimeters x 21 columns; target gisacres (log1p); shape__Area and shape__Length dropped as leakage (preprocess_HIFLD-Historic-perimeters-wildfires.py); 19,545 distinct uniquefireidentifier values and fireyear 2000-2018 (preview). STRABLE Appendix C.2 (item 54): "Historical boundaries of major wildfires in the US. The task is to predict total acres burned."
- Use case: a fire manager, when a new fire is reported, estimates its final size to staff the initial attack; here the inputs are agency, unit, incident and complex names, map method and the perimeter's date, not the weather, fuel or terrain at ignition, so the fit is approximate at best; regime grouped by fire (uniquefireidentifier) and temporal by fireyear.
- Siblings and duplicates: fpa_fod_attributes_wildfire_size (FPA FOD Plus: about 2.3M fires 1992-2020 with covariates at the ignition point, the same target quantity), wildfireia_initial_attack_failure, fpa_fod_wildfire_cause, forest_fires, predict_fire_extent; no duplicate. External collections: STRABLE. Also the other HIFLD tables of STRABLE in this run: hifld_prison_boundaries, hifld_public_schools, hifld_transmission_lines, hifld_transmission_towers, fcc_antenna_structure_registration and the NCEI copies ncei_significant_earthquakes, ncei_significant_volcanic_eruptions.
- Better data: a candidate of the benchmark STRABLE (the run's find); no search for better data. The same task with ignition-time features and about a hundred times more fires already has a record: fpa_fod_attributes_wildfire_size.
- Papers and pages: STRABLE (Blayer et al., arXiv 2605.12292, v1 2026-05-12, v2 2026-10-19; a benchmark of tables with strings, Lennart a co-author); preprocessing per table in github.com/soda-inria/strable, scripts/script_preprocess_data/preprocess_HIFLD-Historic-perimeters-wildfires.py; no paper using the layer for prediction looked for (the run's web-search budget was used up).
- Metric: none from the first publisher (HIFLD and its sources define no task); STRABLE scores every table with "R² for regression; AUROC for classification" (Appendix D.1), a benchmark-wide default rather than a choice for this task (MET-5), so the fallback rmse on acres, with target_transform log1p; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: perimeterdatetime and datecurrent date a perimeter mapped while or after the fire grew (USE-3, LEAK-10); comments hold mapping notes, a few with acreage ("64 acres on FRA, 54 acres on SRA"; 2 of 13,343 filled mention acres); the perimeters of one fire must stay in one fold (SPLIT); the target is the polygon's GIS area, not the reported final size, and later perimeters of one fire can supersede earlier ones.
- Priority: gap -, use case -, source + (GeoMAC through NIFC), shape + (23,776 perimeters, grouped and temporal), risk - (better data in fpa_fod_attributes_wildfire_size; post-ignition columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 23,776 rows x 21 columns incl. target (STRABLE parquet); target: gisacres.
- Why: Predict the acres burned of a wildfire perimeter
- Notes: Raw file Historic_Geomac_Perimeters_Combined_2000_2018 (HIFLD/GeoMAC, 2000-2018).
