---
unique_name: ppnn_ecmwf_t2m_postprocessing_germany
name: 'PPNN full data: ECMWF ensemble 2 m temperature forecasts and DWD station observations (Rasp and Lerch 2018)'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
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
v2_path: datasets/_dev/tabarena-v0pt2/ppnn_ecmwf_t2m_postprocessing_germany_1m/dataset.py
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 1,808,942 station-days x 40 numeric inputs (mean and spread of 18 ensemble variables, plus station latitude, longitude, altitude and model orography), with the station id and the date beside them; the call stands (priority 4). The screening's "21 forecast variables" and the 46 features of the large-datasets list do not match the paper or the file.
- As published: Rasp (2021), "PPNN full data (feather format)", figshare 10.6084/m9.figshare.13516301.v1, published 2021-01-04, CC BY 4.0 (figshare API), one file `data_RL18.feather` of 615,496,032 bytes (Feather V1). Its metadata, read from the file's last 3,512 bytes with no full download: 1,808,942 rows x 43 columns, namely `date`, `station` (integer), `obs` (the target), `*_mean` and `*_var` of 18 variables (t2m, cape, sp, tcc, u, v and q at 850 hPa, u, v and gh at 500 hPa, sshf, slhf, u10, v10, ssr, str, d2m, sm), and `lat`, `lon`, `alt`, `orog`. The rows equal the paper's 1,626,724 (2007-2015) plus 182,218 (2016) samples "After removing missing observations" (arXiv 1805.09091, Sect. 2.2). The paper's Table 1 lists the same 18 variables and 4 station features; its text gives "p = 42" predictors, two more than the table and the file. The lead time is 48 h (Sect. 2.1); the file has one target column, so the README's "36h and 48h" describes the data retrieval.
- The task's table: the release as it is, 1,808,942 rows x 40 inputs (rows stated by the paper and read from the file; inputs counted from the file's schema), with the station (537 stations, 499 in 2016) as a group or a categorical input and the date for the split (the paper's test year 2016: 182,218 rows). The replication notebook (github.com/slerch/ppnn, RL18_replication.ipynb) drops `sm_mean` and `sm_var` for missing values and splits by row position (training rows up to 1,626,723, test from row 1,626,724), so the rows are ordered by date.
- Access: open, no login; one 615 MB Feather file that pandas and pyarrow read; CC BY 4.0; the code is MIT.
- Changes the call: the Chen and Lerch (2022) temperature deposit (figshare 10.6084/m9.figshare.19453580.v2, CC BY 4.0, `temperature_data_cgm_std.feather`, 1,360,331,336 bytes, schema read the same way) holds the same 1,808,942 rows x 94 columns: 50 columns X1 to X50 (by the description, likely the raw ensemble members of 2 m temperature), mean and standard deviation of 17 variables (no soil moisture), the 4 station features and three day-of-year columns. It is a version of this dataset (PROV-6) with no distinct task, which settles the open question in the links; the curator picks one copy (this one is the first publication, the 2022 one adds the raw members and names the spread `_std`). This file names its spread columns `_var` while the paper says standard deviation; the build should check which one the values hold. Priority kept at 4.
- Not checked: the values (missing values per column, variance or standard deviation in `_var`); the rows of the wind-speed deposit; Jobst et al. (Zenodo 8127734).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-08):** review panel (full): ship after changes (made: a protocol line barring the later forecasts of the same station in other test rows, the measured MAE-CRPS closeness in the metric's reason, the year's evidence from the 2020 deposit, two impossible observations set missing and their 13 rows dropped, the soil-moisture, interpolation, unit and citation notes); disputed: LEAK-9 (a note or a protocol line; settled: the line), PROV-9 (2020 or 2021; settled: 2021), SPLIT-18 against SPLIT-19 with SPLIT-15 (the test windows); for the curator: issue 1. Priority 4: gap 0, use case +, source +, shape +, risk 0 (no thin domain, problem type or regime; the open issue is a weighing call between two valid split designs, not a leak or damage).
