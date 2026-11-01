---
unique_name: seasfire_cube_burned_area
name: 'SeasFire Cube: A Global Dataset for Seasonal Fire Modeling in the Earth System'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Time-series (Regression)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
original_data_state: Other
source_links:
- https://doi.org/10.5281/zenodo.6834585
- https://zenodo.org/records/13834057
- https://github.com/SeasFire/seasfire-datacube
- https://doi.org/10.1038/s41597-025-04546-3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a global Earth-system datacube (0.25 degree cells, 8-day steps, 2001-2021, 54 variables) built for seasonal fire forecasting, with burned area per cell and period as the target. It has the same unit and target as `data_science_zw_2022_fire_prediction` and should be decided with it: a forecasting-like panel of drivers that TP-10 decides (SEL-11), and a 43.9 GB cube to cut into a table.
- Proposed reject (refuted): `No` (`Time-series (Forecasting)`, SEL-10 with SEL-8): the cube is published "for seasonal fire forecasting", so burned area per cell is a future value of a gridded series, and the project's models are spatiotemporal deep networks. Reject check (AI, 2026-10-31): refuted. The source leaves other tasks open: "Apart from seasonal fire forecasting, which is the aim of the SeasFire project, the datacube can be used for several other tasks" (Zenodo v0.4 description), and the data paper names "shifting from traditional segmentation to regression modeling" as another avenue (Karasante et al. 2025, "Other potential downstream applications"). So SEL-8 does not lock the cube to forecasting. The forecasting papers predict from drivers only. FireCastNet takes ten drivers (mslp, tp, vpd, sst, t2m_mean, ssrd, swvl1, lst_day, ndvi, pop_dens), the land-sea mask and the position, and the target is "Burned Areas (as binary)"; burned-area history is no input (Table 1, arXiv 2502.01550v2, re-read 2026-10-31). A panel driven by covariates is decided by measurement under SEL-11 and TP-10, as `rain_in_australia` and `ashrae_great_energy_predictor_iii` were. The parent waits for the same test, and the screener's USE-2 point against a same-period framing applies to the parent too.
- Open doubt: forecasting (SEL-10) and modality (SEL-12). Prapas et al. (2022) "treats global wildfire forecasting as an image segmentation task" (arXiv 2211.00534). FireCastNet compares GRU, Conv-LSTM, Conv-GRU, U-TAE, TeleViT and FireCastNet, and none of these is a tabular model. So TP-10's leg 2 (the source's top solutions are tabular models on point-in-time features) does not hold from the papers, and leg 1 has to carry the case by measurement. The framing is open too. Burned area h steps ahead from the drivers is the source's task. Burned area from the same period's drivers, the parent's framing, has no decision: that period's burned area is itself observed by satellite (USE-2). Markers `Time-series (Regression)` (as on the parent) and `Needs extensive data wrangling`.
- Source: Alonso, Gans, Karasante, Ahuja, Prapas, Kondylatos, Papoutsis, Panagiotou, Michail, Cremer, Weber and Carvalhais, "SeasFire Cube: A Global Dataset for Seasonal Fire Modeling in the Earth System", Zenodo, CC BY 4.0, from the ESA-funded SeasFire project ("Earth System Deep Learning for Seasonal Fire Forecasting"). Versions: v0.1 of 2022-07-15 (doi 10.5281/zenodo.6834585, SeasFireCube8daily.zip, 35.2 GB) and v0.4 of 2024-09-26 (doi 10.5281/zenodo.13834057, seasfire_v0.4.zip, 43.9 GB). Data paper: Karasante, Alonso, Prapas, Ahuja, Carvalhais and Papoutsis, "SeasFire cube - a multivariate dataset for global wildfire modeling", Scientific Data 12:368 (2025), doi 10.1038/s41597-025-04546-3; preprint arXiv 2312.07199 (2023). Its abstract says "59 variables", the v0.4 Zenodo page 54. As published: one zarr cube, global, 2001-2021, 8-day steps (966 periods), 0.25 deg. Variables:
  - ERA5 meteorology: mslp, tp, rel_hum, vpd, sst, skt, ws10, t2m mean, min and max, ssr, ssrd, swvl1 to swvl4, lsm;
  - CEMS fire danger: drought code and FWI, mean and max;
  - CAMS GFAS: fire CO2 emissions and fire radiative power;
  - FireCCI burned area with masks, number of patches, burnable and observed fractions;
  - MODIS: lst_day, LAI and NDVI;
  - GPW v4 population density;
  - GFED burned area ("large fires only") and the GFED regions;
  - GWIS burned area;
  - 11 NOAA climate indices;
  - ESA CCI land-cover fractions (9 classes), biomes and grid area.

  The burned areas are in hectares.
- Use case: the source names seasonal fire forecasting, and the data paper adds "developing early warning systems and enabling more proactive wildfire mitigation efforts" (Other potential downstream applications). It names no actor or decision. A use case would be ours, for example a fire agency that plans prevention and pre-positions crews per region weeks ahead (USE-1, "for example"). Fit approximate. Regime temporal: FireCastNet trains on 2002-2017, validates on 2018 and tests on 2019 ("using years 2002-2017, 2018 and 2019 for train, validation, and test"), with the same cells in every split (SPLIT-6).
- Siblings and duplicates:
  - `data_science_zw_2022_fire_prediction` (AI `TBD -> 2nd Tier`, priority 2, `Time-series (Regression)`, waiting for TP-10): monthly burned area per cell in Zimbabwe, 2001-2016, from Zindi; the same unit and target, with covariates of the same kind;
  - `predict_fire_extent` and `wildfire_prediction_challenge`: `No`, `Duplicate` of the former;
  - other units: per fire in `forest_fires` (`Yes`), `fpa_fod_attributes_wildfire_size`, `fpa_fod_wildfire_cause` and `wildfireia_initial_attack_failure`; per perimeter in `hifld_historic_wildfire_perimeters`; per basin and storm in `usgs_postfire_debris_flow`.

  No other record links SeasFire, GWIS, GFED or FireCCI. External collections: none found. The cube is used by deep-learning papers, not by tabular benchmarks.
- Better data: found as better data for `data_science_zw_2022_fire_prediction` (and its duplicates `predict_fire_extent`, `wildfire_prediction_challenge`) in the data-scouting run of 2026-10-30/31; no further search.
- Papers and pages:
  - the two Zenodo records;
  - the Scientific Data paper (PMC11876342), whose downstream demo is "framed as a segmentation task" with the GWIS target and reports no score;
  - Prapas et al., "Deep Learning for Global Wildfire Forecasting", NeurIPS 2022 workshop Tackling Climate Change with Machine Learning, arXiv 2211.00534 (8, 16, 32 and 64 days ahead);
  - FireCastNet, arXiv 2502.01550 (horizons of 1, 2, 4, 8, 16 and 24 steps of 8 days; global models and models per GFED region);
  - github.com/SeasFire/seasfire-datacube (tutorial).
- Metric: the data's own publications score nothing. The Zenodo pages state no metric, and the data paper's demo shows a confidence map only (Fig. 7). For the binary burned / not burned target, FireCastNet scores one metric: "the performance of the model is evaluated using the Area Under the Precision-Recall Curve (AUPRC)" (FireCastNet, arXiv 2502.01550v2). That is a deliberate choice (MET-5), threshold-free (MET-6 does not arise), and needs no extra inputs. Its values at horizon 1, global, on the 2019 test year (Table 2): FireCastNet 0.641, Conv-LSTM 0.635, GRU 0.558; the climatology baselines reach "0.174 (anyfire) and 0.3211 (majority)". For a target in hectares no metric was found, so the fallback (rmse).
- Risks for /add-dataset:
  1. The framing: burned area h steps ahead per cell from the drivers, or the parent's same-period framing; the latter needs a decision (USE-2, SEL-10).
  2. TP-10 leg 1 against each cell's seasonal profile. FireCastNet's majority seasonal baseline reaches 0.321 AUPRC.
  3. Leg 2 and SEL-12 by measurement: a gradient-boosting model on cell-period rows against the published AUPRC at horizon 1.
  4. A regional cut (Zimbabwe or Africa), and whether that cut is better data for the parent.
  5. Which burned-area product (GWIS, GFED "large fires only", FireCCI), and a binary or an area target (USE-5).
  6. The same period's fire outcomes are the target in other words: FRP, fire CO2, FireCCI patches and the other burned-area products. Drop them, or lag them past the prediction point (LEAK).
  7. Cell id and lat/lon carry the cell's history (LEAK, SPLIT).
  8. A temporal split by year, with the masks of valid burned area (fcci_ba_valid_mask, gwis_ba_valid_mask) applied to the target.
  9. 43.9 GB of zarr: preview the cube's chunks before any cut.
- Priority: gap 0 (environmental science & climate 7 accepted, regression 48, temporal 43; none thin), use case 0 (no actor named), source + (versioned Zenodo record with a variable table, and a Scientific Data paper), shape + (millions of cell-periods, about 50 drivers, a temporal structure), risk - (a forecasting-like target, SEL-10 and SEL-12, and a cube to cut).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `data_science_zw_2022_fire_prediction`, `predict_fire_extent`, `wildfire_prediction_challenge`.
- as published: Global grid cells x 8-day periods: 0.25 deg grid, 2001-2021 (966 periods), 54 variables, one zarr cube (seasfire_v0.4.zip, 43.9 GB). Zimbabwe alone is roughly 500-550 cells at 0.25 deg (my estimate ...; target: Burned area per cell and period (three products: GWIS gwis_ba, GFED gfed_ba, ESA FireCCI fcci_ba, in hectares; divided by the cube's grid `area` it is the ...; access: open.
- Why: Same unit (grid cell x period), same target (burned area of the cell) and covariates of the same kind and largely the same sources: ERA5 climate (temperature, precipitation, humidity, VPD, soil moisture) for TerraClimate/TRMM, ESA CCI land cover classes for MODIS MCD12Q1, NASA SEDAC GPW v4 population density (the ...
- Adds: 21 years (2001-2021) instead of 2001-2016, 8-day instead of monthly resolution, the whole of Africa and the globe instead of one country, three burned-area products instead of one, and a documented, versioned source (CC-BY-4.0) instead of an undocumented Google Earth Engine export with the 533-vs-3821-cells copy ...
