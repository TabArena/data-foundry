---
unique_name: camels_hydrological_signatures
name: CAMELS catchment attributes and hydrological signatures (671 US basins)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
year: '2017'
domain: environmental science & climate
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5065/D6G73C3Q
- https://zenodo.org/records/15529996
- https://doi.org/10.5194/hess-21-5293-2017
- https://doi.org/10.1029/2018WR022606
- https://arxiv.org/abs/2610.35464
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 671 US catchments with about 60 static attributes (climate, topography, soil, geology, vegetation) and hydrological signatures from their streamflow; predicting a signature for an ungauged basin is a real regionalisation task, but 671 rows, a source that frames it as signature selection and a choice among related signatures make it secondary.
- Source: Addor, Newman, Mizukami and Clark 2017, "The CAMELS data set: catchment attributes and meteorology for large-sample studies", HESS 21:5293-5313 (doi 10.5194/hess-21-5293-2017, 2017-10-20); data at NCAR/UCAR (doi 10.5065/D6G73C3Q, "Catchment attributes for large-sample studies") and a Zenodo copy (15529996, v1.2, 2022-06-24) with camels_topo, camels_clim, camels_hydro, camels_soil, camels_vege, camels_geol and camels_name text files joined on the gauge id, beside the forcing and streamflow time series. As published: 671 minimally impacted basins of the contiguous US; the signatures (13 in camels_hydro.txt per the run's note, not counted) such as q_mean, q95, baseflow_index, runoff_ratio.
- Use case: a hydrologist or engineer estimates a streamflow characteristic (mean flow, a high- or low-flow quantile, the baseflow index) at an ungauged site from mapped catchment attributes, for water-resource planning or design; the source frames the prediction as signature selection ("exploring the predictability of signatures in space ... is hence useful for signature selection", Addor et al. 2018, abstract), so the decision is our reading; fit approximate; regime IID over basins (one row per basin), or grouped by HUC-02 region for an actor predicting in an unmonitored region; nested basins to check (SPLIT-29).
- Siblings and duplicates: none (grep camels, catchment, hydrolog); `global_dams_database` and `2030_vision_flood_prediction_in_malawi` are other hydrology records. External collections: EvoBench (arXiv 2610.35464) per the Zotero item.
- Better data: from the curator's Zotero collection (item 311); no further search this round.
- Papers and pages: Addor et al. 2017 (the data); Addor, Nearing, Prieto, Newman, Le Vine and Clark 2018, "A Ranking of Hydrological Signatures Based on Their Predictability in Space", Water Resources Research (doi 10.1029/2018WR022606): random forests predict 15 signatures from the attributes in 600+ catchments (abstract through Crossref; the full text returned 403).
- Metric: not read: the predictability measure of Addor et al. 2018 sits in the paywalled text, and the 2017 data paper defines no task; so the fallback `rmse` on the chosen signature; inputs none.
- Risks for /add-dataset: ship one signature; the other signatures come from the same streamflow record, are unknown at an ungauged site and go (LEAK-10; runoff_ratio is q_mean over p_mean); the climate indices come from the forcing record, which exists at an ungauged site; camels_name holds names and HUC codes (groups, not features); 671 rows is small for a regression; larger collections of the same kind of attributes (the CAMELS datasets of other countries, Caravan) were not searched this round.
- Priority: gap 0 (environmental, regression not thin), use case 0 (our reading), source +, shape 0 (671 basins), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 311: "EvoBench: An Evolving, Diagnostic Benchmark Framework for Environmental Modeling".
- as published: 671 HCDN-2009 basins (contiguous US) x about 60 static attributes (climate, topography, soil, geology, vegetation in camels_clim/topo/soil/geol/vege.txt) plus 13 signatures in camels_hydro.txt, ...; target: one hydrological signature per basin, e.g. q_mean (mean daily discharge, mm/day) or q95 / baseflow_index (regression); access: open.
- Why: a published predictive task (Addor et al. 2018 rank 15 signatures by how well random forests predict them from attributes), real gauged data with a documented source, and environmental hydrology is thin in the benchmark; caveats: small (671 basins, under the ~1,000-unit first guess), one signature must be chosen as ...
- Adds: a hydrology regression on static catchment attributes, with a natural grouped or spatial split by region
