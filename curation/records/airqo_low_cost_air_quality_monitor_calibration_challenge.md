---
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge
name: airqo-low-cost-air-quality-monitor-calibration-challenge
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data
- https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge
- https://zindi.africa/competitions/airqo-air-sensor-calibration-challenge
- https://doi.org/10.1002/ail2.76
v2_path: datasets/_dev/tabarena-v0pt2/airqo_low_cost_air_quality_monitor_calibration_challenge/dataset.py
source_row: 906
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: calibrate AirQo's low-cost PM2.5 monitors to collocated reference monitors in Kampala, a fixed same-hour regression that AirQo uses on its network.
- Source: Zindi competition by AirQo (Makerere University), 2021-04-30 to 2021-06-06 ($1,000, 318 participants), "orignally launch as a hackathon at DataFest Kampala" (`airqo-air-sensor-calibration-challenge`, 2021-04-29/30, the same data and text); as published: Train.csv and Test.csv, hourly rows at three sites (US Embassy, Makerere, Nakawa, "approx 4:2:1") over about two years; target `ref_pm2_5` (reference monitor); features two low-cost PM2.5 and two PM10 sensors, temperature, humidity, `created_at`, `site`, and site metadata (latitude, longitude, altitude, terrain, greenness, distance to a major road), constant per site; one table.
- Use case: AirQo transforms low-cost readings "as accurately as possible to the reference value" so its network is shared "as reference grade"; fit direct; regime temporal or grouped by site: the readings are an hourly stream, the target is the same hour (calibration, not a forecast, so the old `Time-series (Forecasting)` and `Missing source information` markers are refuted and dropped).
- Siblings and duplicates: `airqo_low_cost_air_quality_monitor_calibration_challenge_2` is the DataFest hackathon of the same data (proposed `Duplicate`); `air_quality_prediction_from_low_cost_iot_devices` (TBD -> 2nd Tier, other data); `faulty_air_quality_sensor_challenge` (AirQo, a different task). External collections: none found.
- Papers and pages: <https://zindi.africa/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge>; Adong, Bainomugisha, Okure, Sserunjogi (2022), "Applying machine learning for large scale field calibration of low-cost PM2.5 and PM10 air pollution sensors", Applied AI Letters, doi:10.1002/ail2.76 (AirQo; random forest cut PM2.5 RMSE from 18.6 to 7.2 µg/m³ against BAM references, cross-unit and cross-site validation; not confirmed to be the same rows).
- Metric: RMSE, the Zindi evaluation page ("The evaluation metric for this challenge is the Root Mean Squared Error"); deliberate (leaderboard, MET-4); inputs none.
- Risks for /add-dataset: only three sites, so a grouped split has three groups (a temporal split is the likelier protocol, SPLIT); the site metadata is constant per site (an identifier in disguise); the raw sensor reading may carry most of the signal (TP-4 probe; the paper's 18.6 to 7.2 suggests not); the Zindi test rows may hold no target, so the train file alone may be the data.
- Priority: gap - (environmental, regression, temporal not thin), use case + (AirQo names it), source + (AirQo data page with variable definitions, a paper), shape + (thousands of hourly rows, a temporal structure), risk 0.

An AirQo challenge to calibrate low-cost air-quality monitors (no comments in the record). Sensor-calibration tasks predict a reference pollutant value from raw low-cost sensor readings, which can be a legitimate fixed tabular regression, but the data is time-stamped and may be framed as forecasting or require a temporal split. The exact target, table structure, and size are unverified. A human must confirm whether the task is a fixed calibration regression (acceptable) versus a temporal forecast, and assess the post-cleaning row count.

**CC (2026-10-27, Myunghwan):** Requested add-dataset work for Low-Cost Monitor Calibration and supplied the original Train_LowCost.csv, Test_LowCost.csv and SampleSubmission_LowCost.csv files for qualification. Proceed with actual-data qualification for this distinct2021 same-hour calibration task. This is stage authorization, not a final ship/build verdict or a settled temporal-versus-grouped evaluation choice.

**Assessment (AI, 2026-10-27), source access recovered:** User-supplied files are archived unchanged with suffixes and copied as Train.csv/Test.csv/SampleSubmission.csv into the dedicated warehouse. Byte counts and SHA-256 are retained in the source-verification evidence; no agent-authenticated download or publisher checksum comparison is claimed. This supersedes the historical HTTP401 access prerequisite. Raw-data verification, split choice, qualification and independent panel remain actual work, not established by file presence.

**CC (2026-10-27, Myunghwan), conditional application clarification:** "how does this calbiration work? do we have measurement reading and ground truth? if the task setup is valuable for the past data calibration as well, then the original setup is useful". The condition is met by same-hour paired cheap/reference measurements and the organizer's explicit initial retrospective-correction use. Proceed with the source-style retrospective setup for represented historical sites/devices, retaining source RMSE; this does not approve arbitrary new-device transfer or final ship/build.

**Assessment (AI, 2026-10-27), application implementation:** Historical correction is meaningful because collocated training pairs learn the relation from cheap readings to reference PM2.5, which can be applied to reference-missing archived hours. Keep all10932 labels/rows and16 source predictors after dropping opaqueID. Source-created_at is an observation timestamp; correction happens after the archive is recorded. The original contest has interleaved dates and an unlabeled2733-row Test, so CV is a source-style counterpart rather than an exact leaderboard replay. Main random-fold qualification and full panel remain unfinished. The source's90m landform is categorical,270m mTPI numeric; unverified sensor2zero states and greenness scale are preserved.

**Assessment (AI, 2026-10-27), completed actual-data qualification:** The supplied original-download bytes are preserved and verified by SHA-256; no publisher checksum or authenticated new download is claimed. Added 10,932 labeled site-hours with 16 predictors after dropping only ID, original-scale ref_pm2_5 and source RMSE. Historical correction of archived readings at represented collocations is meaningful and source-supported. This explicitly supersedes the earlier unverified screening's direct/network-deployment fit and temporal-or-grouped preference: fit is approximate, and the implemented site-balanced random 3 x 3 CV tests archive interpolation only. The related paper's scores/preprocessing and exact hackathon sibling-byte identity are not qualification evidence.

Fixed untuned qualification on the nine exact native folds: mean fold RMSE 35.568 dummy, 21.048 raw sensor1, 20.296 two-sensor linear, 16.424 Ridge, 14.204 forest, 13.237 LightGBM and 19.298 training-selected single feature. All three model families beat the dummy on all nine folds. Task probes cover five of nine folds with no flags; native hidden-group probes have no hits. The unchanged native leak CLI failed on a timezone selector; a retained local compatibility run performs its intended 15-predictor date-excluded checks on three folds. Separate full-feature qualification includes the timestamp. No hyperparameter search or container build was performed.

All rows and unverified sensor2-zero states remain. Two isolated reference disagreements contribute 14.13% of the model's repeated out-of-fold squared error; corruption is not proved, so they are retained with a prominent quality note. Site context is valid for the stated archive scope; no future or new-device capability follows. Exact upstream reference aggregation, metadata vintage and device history remain cannot-verify. The one regression/site-stratification warning is proposed for curator acceptance, not silently accepted. Independent evidence audits, debate and mediation are retained in the direct run; no final curator ship/build verdict is inferred. Priority 3: gap 0 (measured domain/problem/regime not thin), use case 0 (real source use, but fit approximate rather than the required direct fit), source + (publisher documents paired instruments and variables), shape + (10,932 rows, 16 inputs including categories/time), risk 0 (no demonstrated leak, destructive join or proven damaged release; the two reference anomalies remain explicitly unverified).

**CC (2026-10-28, Myunghwan):** "ship Low-cost calibration". Approved the presented retrospective calibration definition for shipping, retaining all source rows, reference PM2.5, source RMSE and site-balanced random 3 x 3 folds. In the presented review this accepts issue 1's discrete-site stratification warning acknowledgment. Source-quality and represented-site limitations remain. Build and repository integration require a separate request.

**Assessment (AI, 2026-10-28):** The independent consistency check found no unexplained rule departure or new exception. Accepted the discrete non-target site-balancing warning without changing rows, predictors, target, metric or fold memberships. Closed review issue 1; its original wording and full panel reports remain preserved in the review history. Scientific ship acceptance does not grant data redistribution rights.
