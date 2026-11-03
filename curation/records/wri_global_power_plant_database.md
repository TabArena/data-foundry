---
unique_name: wri_global_power_plant_database
name: Global Power Plant
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
year: '2021'
problem_type: Regression
original_data_state: One Table
source_links:
- https://datasets.wri.org/dataset/globalpowerplantdatabase
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/global-power-plant
- https://arxiv.org/abs/2605.12292
- https://github.com/wri/global-power-plant-database
- '# v1.3.0 release on the WRI data portal (CSV in a zip, CC BY 4.0)'
- https://datasets.wri.org/private-admin/dataset/53623dfd-3df6-4f15-a091-67457cdb571f/resource/66bcdacc-3d0e-46ad-9271-a5a76b1853d2/download/globalpowerplantdatabasev130.zip
- https://files.wri.org/d8/s3fs-public/global-power-plant-database-technical-note-v1.0.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a well-documented global listing of 34,936 power plants (WRI, v1.3.0), but STRABLE's target, a plant's installed capacity, is a listed attribute no decision is made on; the source's own model task is annual generation, reported almost only for US plants.
- Source: World Resources Institute with Google, KTH, Enipedia and the Global Energy Observatory; first released in April 2018 with the technical note Byers et al., "A Global Database of Power Plants" (https://files.wri.org/d8/s3fs-public/global-power-plant-database-technical-note-v1.0.pdf; about 30,000 plants in 164 countries); v1.3.0 (2021, CC BY 4.0) is the last release (GitHub README: "This project is not currently maintained by WRI ... The last version of this database is version 1.3.0"), so `year` is set to the snapshot, 2021 (PROV-9). As published: one CSV of 34,936 plants in 167 countries x 36 columns (country, name, gppd_idnr, capacity_mw, latitude, longitude, primary_fuel, other_fuel1-3, commissioning_year, owner, source, url, geolocation_source, wepp_id, year_of_capacity_data, generation_gwh_2013 to 2019, generation_data_source, estimated_generation_gwh_2013 to 2017 with five note columns). STRABLE keeps the first 18 columns and generation_data_source, drops the generation values and ships capacity as ln(MW) (Kajaki, 33 MW, is 3.4965).
- Use case: none stated for capacity: WRI built the database to "make it easier to navigate, compare, and draw insights for one's own analysis" (WRI data page). For example, an analyst estimating the size of a plant a source lists without capacity; a fill-in of a listing, fit approximate at best (`No Good Target (yet)`). The source's own model task is generation: WRI and Microsoft AI for Earth estimated "plant-level annual generation in the form of annual capacity factor" for plants without reported values (https://github.com/wri/gppd-ai4earth-api), but a generation source is named for only 11,400 plants, 9,715 of them the US EIA, so a generation target would be mostly the EIA data `hifld_electric_generating_plants` already holds. Regime IID for a listing, or grouped by country if the use is a country without a capacity source.
- Siblings and duplicates: `hifld_power_plants` (HIFLD/EIA-860, US plants, target nameplate capacity: the same quantity, and GPPD's 9,789 EIA-sourced US rows overlap it, though the two are different publications, PROV-4); `hifld_electric_generating_plants` (US net generation from the EIA); `wri_china_overseas_finance_inventory` (installed capacity of Chinese-financed overseas power projects, another WRI table). No other record links the GPPD. External collections: STRABLE (config `global-power-plant`; its paper row 51 says "The task is to predict annual electricity generation" while the config's target is capacity_mw, a mismatch of that copy, PROV-15); Kaggle re-uploads (mathurinache, eshaan90, dianaddx and others, 2019 to 2026).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the technical note above; https://github.com/wri/global-power-plant-database (build code and data lineage per source); https://github.com/wri/gppd-ai4earth-api (the generation estimates); STRABLE, Blayer et al. 2026 (https://arxiv.org/abs/2605.12292), App. C.4.
- Metric: none found from the source (the WRI data page, the technical note page, the GitHub README); STRABLE scores every regression by R^2 "reported on the transformed scale" after a skewness-minimising target transform (App. D.1, "Evaluation metrics"), a benchmark-wide choice rather than one for this decision, so the fallback `rmse` on log capacity; inputs none (MET-1, MET-5).
- Risks for /add-dataset: the release's generation_gwh_* and estimated_generation_gwh_* columns scale with capacity (the estimates are a modelled capacity factor times capacity), so they go for a capacity target (LEAK-10); wepp_id links the commercial WEPP database and year_of_capacity_data is a source detail, to be read column by column (LEAK-2); owner, url and source are high-cardinality strings; take the raw MW from WRI's CSV rather than STRABLE's log copy (MET-3). Only 12 of the 34,936 names state a capacity in MW or kW, so the names give little away.
- Priority: gap 0 (no thin domain; regression and IID not thin), use case 0 (none stated for capacity), source +, shape + (34,936 plants, mixed types), risk - (a target no decision rests on, and generation columns that copy it).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 34,936 rows x 19 columns incl. target (STRABLE parquet); target: capacity_mw.
- Why: Predict a power plant's installed capacity (MW)
- Notes: WRI Global Power Plant Database. Paper says 'annual electricity generation'; config target is capacity_mw. The wri.org link in the paper returned 404 on 2026-10-30; the datasets.wri.org page works.
