---
unique_name: swan_sf_solar_flare
name: 'SWAN-SF: Multivariate time series dataset for space weather data analytics (SHARP active-region parameters with GOES flare labels)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Other
year: '2020'
domain: physics & astronomy
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://doi.org/10.1038/s41597-020-0548-x
- https://doi.org/10.7910/DVN/EBCFKM
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the SWAN-SF benchmark (Angryk et al. 2020): 51 SHARP magnetic-field parameters of 4,098 active regions from May 2010 to 2018 at a 12-minute cadence, labelled with the largest GOES flare in a prediction window after each observation window, in five time-segmented partitions; physics and astronomy has no accepted dataset, but the release is multivariate time series that we must cut into one row per forecast.
- Source: Angryk, Martens, Aydin, Kempton, Mahajan, Basodi, Ahmadzadeh, Cai, Filali Boubrahimi, Hamdi, Schuh and Georgoulis, "Multivariate time series dataset for space weather data analytics", Scientific Data 7:227, 2020 (doi 10.1038/s41597-020-0548-x; full text read through Europe PMC, PMC7351763); data on Harvard Dataverse, "SWAN-SF" (doi 10.7910/DVN/EBCFKM, version 1 released 2020-04-24, CC0): `partition1_instances.tar.gz` to `partition5_instances.tar.gz` (0.7 to 1.5 GB each, 5.7 GB together), `SWAN.tar.gz` (735 MB, the per-region series) and `addenda.tar.gz` (34 MB); not opened. As published (abstract, Methods): "4,098 MVTS data collections from active regions occurring between May 2010 and December 2018, includes 51 flare-predictive parameters, and integrates over 10,000 flare reports" (the SHARP series used runs 2010-05-01 to 2018-08-31); each instance is a slice with an observation window, a latency and a prediction window, "labeled with the magnitude of the largest flare (if any) that occurred in that HARP during the prediction window"; 730 M-class and 50 X-class flares, "Among 4,098 MVTS, only 27 contain X-class flares and 178 have M-class flares"; five partitions with "non-overlapping time segments" and about 90 M- and X-class flares each; the binary schema "M- or X-class flares (≥M1.0) are considered flaring".
- Use case: a space-weather forecast centre issues the chance of an M- or X-class flare from an active region over the next hours from the magnetograms seen so far; the paper: "Successful flare predictions via machine learning models trained and tested on this dataset intend to (1) tackle a central problem in space weather forecasting", with "operational (research-to-operations)" benefits; fit direct (features up to the issue time, the label in the window after it). Regime temporal (the source's time-segmented partitions, SPLIT-19), with the active region as a group inside it (SPLIT-13). Event prediction from current measurements, not future values of a series, so in scope by SEL-11.
- Siblings and duplicates: `solar_flare` (`TBD -> 2nd Tier`, Outdated and Data Quality Issue; UCI 1989, McIntosh classes, 1,389 rows): the same target from another source, no duplicate (PROV-4). No other flare record. External collections: none found.
- Better data: found as better data for `solar_flare`; no further search this round. The record's third link (Zenodo 15570399) is not SWAN-SF but another dataset, "Solar Flare Prediction Dataset: SHARP Magnetic Field Parameters for Machine Learning" (Žilinskas, Imperial College London, 2025: processed SHARP parameters for 2023-01-01 to 2025-05-31, normalisation parameters, a chronological 90/10 split); moved here from the links (PROV-12).
- Papers and pages: the Scientific Data paper and the Dataverse page; the paper's references 52 and 53 on under- and oversampling for flare prediction.
- Metric: none found in the data paper (its text discusses partitions, class imbalance and sampling and names no score), so the fallback `roc_auc` for M or X against the rest (MET-1, MET-8). The flare-forecasting field often reports the true skill statistic at a threshold; the source fixes none (MET-6); inputs none.
- Risks for /add-dataset: scope: each instance is a slice of time steps by 51 parameters; a tabular row takes the parameters at the end of the observation window or summaries of the window, and SEL-12 asks whether tabular models stay competitive with time-series models on it (judged per dataset; `Time-series (Classification)` to weigh); the window lengths of the released partitions to confirm from the files (the paper makes them user-defined); slices of one region overlap in time within a partition (SPLIT-29); rare positives (5% of the regions have an M or X flare); the addenda's undersampled set is not the population (keep the natural class mix); 5.7 GB of per-slice files (`Needs extensive data wrangling`).
- Priority: gap + (physics & astronomy has no accepted dataset), use case + (space-weather forecasting named by the source, direct fit), source + (a Scientific Data paper and a Dataverse release), shape + (thousands of regions over eight years, temporal and grouped), risk - (a time-series release to cut into rows, rare positives).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `solar_flare`.
- as published: 4,098 active-region (HARP) time series, May 2010 to Dec 2018, 51 flare-predictive SHARP magnetic-field parameters at 12-minute cadence (over 520,000 hours of activity), more than 10,000 ...; target: Largest GOES flare class produced by the active region in the next 24 h (X, M, C, B, flare-quiet); usually binarised as M/X vs rest; access: open.
- Why: Same target as solar_flare (flares of class C/M/X from one active region within the next 24 h) and use case; the features describe the same object at the prediction point, measured better: vector-magnetogram SHARP parameters instead of the McIntosh sunspot classification
- Adds: Thousands of active regions over a solar cycle instead of 1,389 rows (about 350 unique), real time order and region IDs for a temporal/grouped split, a published partition scheme, rare M/X labels from cross-checked GOES reports. Risks: delivered as multivariate time series; a tabular task takes the point-in-time ...
