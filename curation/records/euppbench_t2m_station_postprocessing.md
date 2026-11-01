---
unique_name: euppbench_t2m_station_postprocessing
name: EUPPBench postprocessing benchmark dataset v1.0 (station data)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2023'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://doi.org/10.5194/essd-15-2635-2023
- https://doi.org/10.5281/zenodo.7708362
- '# the gridded part of EUPPBench (Part III), not the station data'
- https://doi.org/10.5281/zenodo.7429916
- https://eupp-benchmark.github.io/EUPPBench-doc/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: EUMETNET's station benchmark for postprocessing ECMWF 2 m temperature forecasts at 234 stations in six countries, with 20 years of reforecasts for training and a published protocol; the `bias_correction` task at scale, but the release is an 18 GB Zarr store of ensemble members to turn into a table.
- Source: Demaeyer et al., "The EUPPBench postprocessing benchmark dataset v1.0", Earth System Science Data 15, 2635-2653, 2023 (doi:10.5194/essd-15-2635-2023); station data on Zenodo, doi:10.5281/zenodo.7708362 (v1.0, 2023-03-08, `EUPPBench-stations.zip`, 18.3 GB, Zarr, "You need at least 35Gb of free space on your disk"), documentation https://eupp-benchmark.github.io/EUPPBench-doc/, download through the climetlab plugin. As published: 234 stations (mainly Belgium, France, Germany, Switzerland, Austria and the Netherlands) with observations 1997-2018; ECMWF IFS forecasts of 2017-2018 (51 members) and the matching reforecasts (11 members) for the 20 years before, 6-hourly lead times to 120 h; surface and pressure-level forecast fields per station (documentation, section 2); observed 2 m temperature, cloud cover, visibility, precipitation and wind gust (Sect. 2.3). The Swiss observations "are not presently freely available" (registration with MeteoSwiss IDAWEB).
- Use case: a national weather service, when the ensemble forecast is issued, corrects the 2 m temperature forecast for each station before publishing it (the benchmark's first experiment, Sect. 3.1); fit direct; regime temporal: the source trains on the reforecasts and tests on the 2017-2018 forecasts (Sect. 3.1; SPLIT-19), with short weather windows (SPLIT-18).
- Siblings and duplicates: `bias_correction_r_bias_correction_r_2` (`Yes`, shipped; 25 Seoul stations, LDAPS, summers 2013-2017, the record this was found for); `ppnn_ecmwf_t2m_postprocessing_germany` (Rasp and Lerch 2018: 537 DWD stations, 2007-2016, 1.8M rows with 42 summarised predictors; also found as better data for `bias_correction`). The same task from other sources (PROV-7); the curator decides which one enters. External collections: EUPPBench is itself a benchmark (EUMETNET).
- Better data: found as better data for `bias_correction_r_bias_correction_r_2` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the ESSD paper (Sect. 2.3 stations, 3.1 protocol, 3.2 metrics, Appendix A significance tests); the EUPPBench documentation.
- Metric: CRPS, the main accuracy measure among the four the paper uses (bias, CRPS, spread, spread-error ratio; Sect. 3.2) and the basis of its skill score (Sect. 5); it scores a predictive distribution, which a point regression does not give, and its deterministic limit is the absolute error (the paper: it "generalizes the mean absolute error to probabilistic forecasts"), so `mae` as a stand-in or the fallback `rmse`, the curator's call (MET-2); inputs none.
- Risks for /add-dataset: build the table (ensemble mean and spread of each field per station, issue date and lead time; one lead time, or lead time as a feature); training on 11-member reforecasts and testing on 51-member forecasts changes the spread features (the source's protocol); the Swiss stations need a registration (drop or request them); an 18 GB download. The second Zenodo link (doi:10.5281/zenodo.7429916) is the gridded data, Part III, not the station data.
- Priority: gap 0 (environmental science, regression and temporal are not thin), use case + (operational postprocessing named by the source), source + (ESSD paper, Zenodo DOI), shape + (234 stations, two years of forecasts and 20 years of reforecasts, temporal), risk - (heavy wrangling from Zarr ensembles; `ppnn_ecmwf_t2m_postprocessing_germany` is a ready table of the same task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `bias_correction_r_bias_correction_r_2`.
- as published: 234 stations (BeNeLux, Germany, France, Austria, Switzerland); ECMWF IFS forecasts (51 members) for 2017-2018 and reforecasts (11 members) back to 1997; station observations 1997-2018 of 2 m ...; target: observed 2 m temperature at the station (the benchmark's first experiment); access: open (attribution licence); Swiss station observations only on request from MeteoSwiss.
- Why: same task as bias_correction: correct an NWP 2 m temperature forecast at a station from forecast fields and static station metadata (elevation, land use) known at issue time
- Adds: newer (forecasts 2017-2018), 234 stations over six countries, 20 years of reforecasts for training, a published evaluation protocol; raw ensemble members must be summarised into tabular predictors
