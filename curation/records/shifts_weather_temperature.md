---
unique_name: shifts_weather_temperature
name: Shifts Weather Prediction dataset (full and canonical release)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Github
year: '2021'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://arxiv.org/abs/2107.07455
- https://github.com/yandex-research/shifts
- https://storage.yandexcloud.net/yandex-research/shifts/weather/full-dataset.tar
- https://storage.yandexcloud.net/yandex-research/shifts/weather/canonical-partitioned-dataset.tar
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: Yandex Weather's Shifts release (10M station records, September 2018 to September 2019, all five climate types, 123 forecast-model and climate features, air temperature at 2 m), the same task as the shipped `climate_model_weather_forecasting`, which is a later Yandex extract (2022-2023), not a cut of these rows; a second, older but wider version of a task we ship.
- Source: Malinin et al. (Yandex Research and co-authors), "Shifts: A Dataset of Real Distributional Shift Across Multiple Large-Scale Tasks", arXiv 2107.07455, 2021 (NeurIPS 2021 Datasets and Benchmarks track); data listed in GitHub yandex-research/shifts, CC BY-NC-SA 4.0 (a note, no criterion, EV-4). As published (Sec. 3, App. C.1): "10 million 129-column entries: 123 meteorological features, 4 meta-data attributes (time, latitude, longitude and climate type) and 2 targets" (temperature for regression, a 9-class precipitation class), "distributed uniformly between September 1st, 2018, and September 1st, 2019"; targets from "about 8K weather stations"; features are GFS, CMC and WRF model outputs plus climate and topography values; "The climate type is not used as a training feature". Canonical partition (Table 8): train 3,129,592 rows (Tropical, Dry, Mild Temperate, September 2018 to 8 April 2019), dev 100,000, eval 1,137,731 (eval_out: Snow and Polar, 14 May to 8 July 2019). Files (HEAD request, 2026-10-31): `full-dataset.tar` 17.0 GB and `canonical-partitioned-dataset.tar` 7.5 GB on Yandex Cloud storage; not opened. A TIB catalogue DOI the run linked (10.57702/frs56elo) resolves to a bot check and holds no data; moved here from the links.
- Use case: Yandex Weather serves a temperature for a place and hour from the forecast-model outputs available then: "This data is used by Yandex for real-time weather forecasts and represents a real industrial application" (Sec. 3); fit direct for the forecast service. Regime temporal (the source's time-shifted evaluation; test windows of one to two weeks, SPLIT-18), with the station as a possible group and the climate type as the shift the source studies.
- Siblings and duplicates: `climate_model_weather_forecasting` (`Yes`, shipped in BeyondArena as a 1M cut) is TabReD's Weather: its preprocessing README splits 2022-07-01 to 2023-07-30 and keeps only the "A (Tropical)" zone ("a 2.5% random sample of the original year+ of data"), and the TabReD paper (App. B) calls it "a dataset similar to the one introduced in (Malinin et al., 2021), except it is larger, and the time-based split is available" (6.0M rows full, 98 features). So the run's reading that TabReD Weather is a cut of these rows does not hold: both are extracts of the same Yandex Weather production logs for different years, one task in two versions (PROV-6), and the curator decides which one enters. External collections: TabReD's review of earlier benchmark datasets (App. A) lists "Shifts Weather (in-domain-subset)", 397,099 rows and 123 features, used with an IID split, and flags it: "Samples from the future used for prediction".
- Better data: found as better data for `climate_model_weather_forecasting`; no further search this round. Against it: about 1.7 times the full rows (10M against 6.0M) and all five climate types, but four years older and with no newer release.
- Papers and pages: the Shifts paper; the Shifts Challenge page (https://research.yandex.com/shifts/weather); Rubachev et al., TabReD (arXiv 2406.19380).
- Metric: the Shifts Challenge ranked teams by R-AUC of the MSE (the area under the error-retention curve, challenge page), which needs a per-row uncertainty that a point model does not return (MET-2); the paper reports RMSE and MAE side by side (Table 1), and the sibling declares `rmse` (TabReD). So `rmse` as a stand-in for the challenge metric (MET-1, MET-2, MET-5); inputs none.
- Risks for /add-dataset: which rows to ship (a 1M cap over 10M; one zone like the sibling, or all zones with the climate type kept out of the features as the source does); the lead time of the forecast-model features against the target hour is not stated, so check that each feature is issued before the target time (LEAK-10, USE-3); no station id is listed among the 129 columns (latitude and longitude stand in, SPLIT-24 if grouped); the curator's note on the sibling that a 1-month refit horizon is too long for weather (SPLIT-18).
- Priority: gap 0 (environmental science, regression and temporal are not thin), use case + (the source names the forecast service that uses the data), source + (a data paper with a datasheet), shape + (10M rows, temporal), risk - (a second version of a shipped task, PROV-6).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `climate_model_weather_forecasting`.
- as published: 10M records x 129 columns (123 meteorological features from GFS, CMC, WRF), uniformly 2018-09-01 to 2019-09-01, all Koppen climate types; canonical partition train 3,129,592, dev 100,000, eval ...; target: air temperature at 2 m at a location and time; access: open (CC BY-NC-SA 4.0, Yandex Cloud tar archives listed in the repo; links not tested).
- Why: the TabReD Weather record is this source: TabReD's preprocessing takes 'a 2.5% random sample of the original year+ of data' of the tropical climate zone only; the full Shifts release has the same target and features
- Adds: about 40x the rows and all climate zones (TabReD keeps one zone to isolate temporal shift); TabReD's 'year+' may extend past the Shifts year, to check
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
