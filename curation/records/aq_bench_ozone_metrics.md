---
unique_name: aq_bench_ozone_metrics
name: 'AQ-Bench: a benchmark dataset for machine learning on global air quality metrics'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2021'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.5194/essd-13-3013-2021
- https://doi.org/10.23728/b2share.30d42b5a87344e82855a486bf2123e9f
- https://gitlab.version.fz-juelich.de/esde/machine-learning/aq-bench
- https://essd.copernicus.org/articles/13/3013/2021/
- https://essd.copernicus.org/preprints/essd-2020-380/essd-2020-380.pdf
- https://gitlab.jsc.fz-juelich.de/esde/machine-learning/aq-bench
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 5,577 ozone monitoring stations worldwide, with ozone metrics averaged over 2010-2014 predicted from static station and land-surface metadata; a peer-reviewed ML benchmark with a spatial split.
- Source: Betancourt, Stomberg, Roscher, Schultz, Stadtler (Forschungszentrum Jülich), "AQ-Bench: a benchmark dataset for machine learning on global air quality metrics", Earth System Science Data 13:3013-3033, 2021, built from the TOAR database. As published: 5,577 stations; 135 inputs after one-hot encoding (coordinates, altitude, climatic zone, population density, nightlights, land cover and others); targets the ozone metrics of Table 2 (average values, percentiles, AOT40, nvgt070 and nvgt100 among them); "the input metadata are fixed and have no temporal evolution" (Sec. 6.2). The data DOI (B2SHARE 10.23728/b2share.30d42b5a87344e82855a486bf2123e9f) gave 404 on 2026-10-31; the GitLab repository (moved to gitlab.jsc.fz-juelich.de, MIT) keeps the data under `resources`.
- Use case: estimate long-term ozone at a place from its geography, for maps and for health and vegetation assessment ("to predict ground-level ozone around the world", Sec. 1); no actor or decision named, fit approximate; regime grouped: "stations are assigned to the same cluster if they are closer than 50 km to each other", and the clusters go at random to 60/20/20 training, validation and test (Sec. 5.2).
- Siblings and duplicates: `ozone_level_8hr` (`TBD -> Yes`, daily ozone days, a forecasting framing), `geoai_challenge_for_air_pollution_susceptibility_mapping` (`TBD -> 2nd Tier`), `urban_air_pollution_challenge` and `geoai_ground_level_no2_estimation_challenge` (`TBD -> Yes`): other sources and tasks, no duplicate. External collections: none found.
- Better data: found as better data for `geoai_challenge_for_air_pollution_susceptibility_mapping`, and as a related task for `ozone_level_8hr` and `urban_air_pollution_challenge`; no further search this round.
- Papers and pages: the ESSD paper and its preprint (essd-2020-380); the GitLab repository.
- Metric: R² per ozone metric, and "The overall score of the solution is the mean of all scores achieved on the test set for all ozone metrics" (Sec. 5.1): the benchmark's deliberate choice, so `r2` on the target we ship (MET-5); inputs none.
- Risks for /add-dataset: one target to pick among the metrics (the average is the natural one; the percentiles and exceedance counts are close framings of it), or a multi-target form the curator decides (`Multi-target`, CLEAN-18); keep the 50 km clusters as groups (SPLIT-3); check that no input is derived from the station's own ozone record; the data DOI does not resolve, so take the files from GitLab and compare them with the paper's counts.
- Priority: gap 0 (environmental science, regression and grouped are not thin), use case 0 (no actor in the source), source + (a peer-reviewed data paper), shape + (5,577 stations, 135 mixed inputs, a spatial structure).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `geoai_challenge_for_air_pollution_susceptibility_mapping`; a related task next to `ozone_level_8hr`, `urban_air_pollution_challenge`.
- as published: 5,577 air-quality monitoring stations worldwide; 135 input features after one-hot encoding (station metadata from the TOAR database: climatic zone, population density, nightlights, maximum ...; target: annual ozone metrics averaged over 2010-2014 at a station (average, percentiles, AOT40, days above 70 / 100 ppb), regression; access: open, open (B2SHARE; dataset licence not read).
- Why: same use case and kind of features as the Milan susceptibility challenge: estimate pollution levels at unmonitored locations from terrain, land cover and climate features; the pollutant differs (ozone metrics, not a multi-pollutant AQI class) | same use case as urban_air_pollution_challenge (air quality where no ...
- Adds: 5,577 stations from a peer-reviewed, documented source instead of the few Milan stations of one city, with a ready target (the Milan record's AQI has to be built from pollutants); open CSV | a published ML benchmark with baselines on 5,577 stations worldwide, static tabular features, a natural spatial grouped regime; ...
