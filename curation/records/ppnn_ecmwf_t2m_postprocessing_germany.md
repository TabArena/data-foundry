---
unique_name: ppnn_ecmwf_t2m_postprocessing_germany
name: 'PPNN full data: ECMWF ensemble 2 m temperature forecasts and DWD station observations (Rasp and Lerch 2018)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1175/MWR-D-18-0187.1
- https://doi.org/10.6084/m9.figshare.13516301.v1
- https://github.com/slerch/ppnn
- https://arxiv.org/abs/1805.09091
- '# Chen and Lerch (2022), Full data for temperature post-processing: a later deposit for a multivariate postprocessing study, maybe a re-cut of the same forecasts and stations (PROV-6, not checked)'
- https://doi.org/10.6084/m9.figshare.19453580.v2
- '# Chen and Lerch (2022), Full data for wind speed post-processing: another target (10 m wind speed), related data'
- https://doi.org/10.6084/m9.figshare.19453622.v2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: a ready table of ECMWF ensemble 2 m temperature forecasts and DWD observations at 537 German stations, 2007-2016 (about 1.8M station-days, mean and spread of 21 forecast variables plus station data), the standard benchmark of ML postprocessing; the `bias_correction` task at scale.
- Source: Rasp and Lerch, "Neural Networks for Postprocessing Ensemble Weather Forecasts", Monthly Weather Review 146(11):3885-3900, 2018 (doi 10.1175/MWR-D-18-0187.1; arXiv 1805.09091, text read); data: Rasp (2021), "PPNN full data (feather format)", figshare doi 10.6084/m9.figshare.13516301.v1 (licence not read: figshare returned 403); code github.com/slerch/ppnn (MIT). As published (Sect. 2.1-2.2, Table 1): ECMWF TIGGE 50-member forecasts initialised at 00 UTC, "available from 3 January 2007 to 31 December 2016", reduced to the ensemble mean and standard deviation of 21 variables (t2m, cape, surface pressure, cloud cover, heat and radiation fluxes, 10 m winds, dew point, soil moisture, 500 and 850 hPa fields), plus station altitude, model orography, latitude and longitude; observed 2 m temperature at 537 DWD stations; "the 2016 validation set contains 182218 samples, the 2007-2015 training set contains 1626724 samples". The README lists lead times of 36 h and 48 h; the scout read 48 h for the paper (not confirmed in the text).
- Use case: a weather service corrects the raw ensemble forecast at each station when the 00 UTC run is in, before it issues the forecast; the paper sets 2016 aside "To ensure our verification procedure mimics operational conditions" (Sect. 2.1); fit direct; regime temporal (the paper's test year, SPLIT-19; short weather windows, SPLIT-18), with all stations of one day in the same window.
- Siblings and duplicates: `bias_correction_r_bias_correction_r_2` (`Yes`: 25 Seoul stations, LDAPS, five summers; the record this was found for), `euppbench_t2m_station_postprocessing` (`TBD -> Yes`, priority 3: EUMETNET's 234 stations in six countries, 2017-2018 forecasts with 20 years of reforecasts, an 18 GB Zarr store); the same task from other sources (PROV-7), the curator decides which one enters. The two Chen and Lerch (2022) figshare deposits stay in the links with notes: the temperature one (the data of Chen et al., doi 10.1214/23-AOAS1784) may be a re-cut of these forecasts and stations (PROV-6, not checked); the wind-speed one is another target. External collections: none found.
- Better data: found as better data for `bias_correction_r_bias_correction_r_2`, and in the curator's Zotero collection (item 270), in the data-scouting run of 2026-10-30/31; no further search this round. The scout also named Jobst et al. (zenodo.org/records/8127734: 462 stations, 2015-2020, CC BY 4.0) as a newer release, not screened here.
- Papers and pages: the MWR paper (Table 2, mean CRPS for 2016 with 2007-2015 training: raw ensemble 1.16, global EMOS 1.00, local EMOS 0.90, boosted EMOS 0.80, QRF 0.81, NN-aux-emb 0.78); the GitHub README; the figshare deposit.
- Metric: CRPS, the paper's one ranking criterion (Table 2, "Mean CRPS"; "All network models are estimated by minimizing the CRPS", README), a deliberate choice (MET-5); it scores a predictive distribution and its deterministic limit is the absolute error, so `mae` as the stand-in or the fallback `rmse`, the curator's call (MET-2), as for `euppbench_t2m_station_postprocessing`; inputs none.
- Risks for /add-dataset: the ensemble-mean forecast alone explains most of the variance, so judge skill against the raw forecast (TP-4) and consider the forecast error as the target; a forecasting-like panel (SEL-11, TP-10), though the inputs are forecasts and station data, not lagged observations; about 1.8M rows (a `_1m` cap); stations with gaps (499 report in 2016); one lead time per dataset; the figshare licence.
- Priority: gap 0 (environmental science, regression and temporal are not thin), use case + (operational postprocessing, named by the source), source + (MWR paper, figshare DOI, code), shape + (537 stations over ten years, a ready table, temporal).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `bias_correction_r_bias_correction_r_2`; the curator's Zotero collection, item 270: "Statistical versus machine learning-based spatial interpolation of post-processed ...".
- as published: station x forecast day: 537 DWD stations in Germany, forecasts 2007-01-03 to 2016-12-31; 1,626,724 training samples (2007-2015) and 182,218 samples (2016); 42 predictors (ensemble mean and sd of 2 m ...; target: observed 2 m temperature at the station, 48 h lead (also 36 h in the data); access: open, open (figshare deposit; licence not read: the figshare page returned 403).
- Why: same task as bias_correction (correct an NWP temperature forecast at a station with the model's own outputs and station features known at forecast time); target is the observed 2 m temperature rather than next-day Tmin/Tmax, the same quantity | Same task as bias_correction_r_bias_correction_r_2 (correcting an NWP ...
- Adds: 537 stations instead of 25, ten full years instead of five summers, 1.8M rows instead of 7.6k; a standard ML post-processing benchmark with published baselines (EMOS, QRF, NN) | 537 stations and 10 years (1.8M rows) against 25 stations and 5 summers (7.6k rows). Newer alternative: Jobst et al. (Zenodo 8127734 and ...
