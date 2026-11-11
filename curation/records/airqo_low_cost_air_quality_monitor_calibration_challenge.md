---
unique_name: airqo_low_cost_air_quality_monitor_calibration_challenge
name: airqo-low-cost-air-quality-monitor-calibration-challenge
checked_by:
- Myunghwan
- Lennart
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
- Temporal (NON-IID)
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

CC (2026-11-04, Lennart): the 500 hours where both sensor-2 channels read exactly 0 (all at USEmbassy, 2019-11-18 to 2019-12-17) have both channels set missing; the rows stay (CLEAN-11).

**Assessment (AI, 2026-11-04):** 15 more hours of the same outage have sensor 2 at 0.02-2.9, under 10% of sensor 1, while elsewhere the ratio is at least 0.63 (its 0.1% quantile); extending the rule to them is open (settled 2026-11-05: set missing by one symmetric rule, issue 4 B). The raw files come from a public GitHub mirror (otoosakyidavid, commit 2ec3e256) whose Train.csv matches the definition's SHA-256 and the byte count Zindi's API lists. (superseded 2026-11-04: the review panel measured sensor 2 at 0.0014 to 1.37 in those hours; elsewhere the ratio's 0.1% quantile is 0.618 and its minimum 0.107)

CC (2026-11-04, Lennart): the reference's single-hour spikes are set missing by a rule, a reference hour above 3 times both low-cost PM2.5 channels and above 3 times both neighbouring hours, and their rows leave ("yes follow the recommendaiton ... mark it well in the dataset notes"; CLEAN-11, CLEAN-15): 5 hours, four at Nakawa in October 2020 and one at Makerere in February 2021. `landform_90m` is decoded into the ALOS catalogue's words ("decode and do as you recommend"; CLEAN-12). The metric is checked as declared.

CC (2026-11-04, Lennart): the split is temporal, three monthly windows over the newest season (December 2020 to February 2021), each trained on every earlier hour ("ok (a)"): AirQo corrects new readings with models retrained periodically, by season, and random folds gave the model the neighbouring reference hours. It replaces the site-balanced random folds of 2026-10-28. (superseded 2026-11-05: five monthly windows from October 2020, issue 1 A; the paper names seasonal retraining as future work, not as AirQo practice)

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled. Train sides 8,207-10,093 hours, test months 834-1,049; `dataset check` passes. (superseded 2026-11-04: the full review panel ran in a second pass, and REVIEW.md issues 1-4 are open)

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (stale retrospective text fixed in the definition; widen the test windows to five months, keep the Makerere test-window spike as a label, drop the 92-hour Nakawa reference outage, one dead-channel rule for both sensors); disputed: SPLIT-20 (widen the windows or record an exception), CLEAN-11 (clause and rank of the Nakawa outage); for the curator: issues 1-4. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (no thin domain, problem type or regime; AirQo names the use but the fit is approximate, network transfer cannot be tested with three sites; Zindi codebook and Adong et al. 2022; 10,927 hourly rows, 16 features, temporal; no leak, the open issues are repairable cleaning and window choices).

**Assessment (AI, 2026-11-04):** text corrections of the second-pass panel applied (Lennart's go-ahead on the review page): the outage-hour figures above, and `splits_comment` now gives the panel's LightGBM RMSE 12.94 against 18.26 instead of the pre-temporal 14.05 against 18.39. No data, split, feature or metric change. (superseded 2026-11-05: 12.30 against 16.69 on the five windows)

CC (2026-11-05, Lennart): five monthly windows from October 2020 instead of the three dry-season months (issue 1, A; SPLIT-20, as aeolus and perth_house_prices). The test covers October 2020 to February 2021, both seasons, and October and November score all three sites; train sides 6,204-10,001 hours (57-92%), test months 599-1,312. Nakawa enters October with 63 hours of history (2020-09-19 to 2020-09-23), close to a new-site test (USE-10). Untuned LightGBM mean RMSE 16.69 (27.5 / 16.8 / 12.5 / 13.0 / 13.6, February first) against 36.70 for the training mean and 21.82 for raw sensor 1; random folds score 12.30 on the same test months.

CC (2026-11-05, Lennart): the 92-hour Nakawa reference outage leaves (issue 3, A; CLEAN-11 impossible-value clause, then CLEAN-15; as qsar_tid_11 and 2024_lusaka_mobility_prediction_hackathon): Nakawa hours of 2020-11-10 to 2020-11-23 with the reference below 0.3 times both PM2.5 channels (reference 0.1 to 11.2 against channels of 12 to 190) get a missing target and leave; the definition raises unless they number 92. They were November 2020 test labels under issue 1 A. 10,835 of 10,932 rows ship.

CC (2026-11-05, Lennart): one symmetric dead-channel rule at 0.27 (issue 4, B; CLEAN-11; as heart_disease, ashrae and protein_model_quality_rf_pcp): a sensor whose PM2.5 is below 0.27 times the other sensor's has both channels set missing and the row stays; 16 more sensor-2 hours and 18 sensor-1 hours, all USEmbassy training rows, guarded at 16 and 18. The live Makerere 2020-12-05 06:00 hour at 0.294 stays a reading.

CC (2026-11-05, Lennart): `required_split` takes the definition's value, Temporal (NON-IID).

CC (2026-11-05, Lennart): the declared metric (RMSE on original reference PM2.5, the source's) is checked and stays as declared.

CC (2026-11-05, Lennart): the spike rule stays and drops its hours in every window (issue 2, (a) of the consistency check; CLEAN-11 impossible-value clause, then CLEAN-15; as the Nakawa outage, qsar_tid_11 and 2024_lusaka_mobility_prediction_hackathon): collocated instruments sample the same air, so a reference hour several times both sensors and the hours around it is an instrument error ("we think the value is wrong"). Rule: reference above 3 times both PM2.5 channels and above 3 times the same site's reference in each neighbouring hour present, with at least one present (an outage hour counts as absent); guarded at 12. It adds the four look-alikes with a missing neighbour (Nakawa 2020-10-29 17:00, 2020-11-02 18:00, 2021-01-01 22:00; Makerere 2020-12-08 14:00) and three more (Nakawa 2020-10-13 05:00, 36.2 against channels of 11 and 12, the weakest; Nakawa 2020-11-04 13:00; USEmbassy 2020-11-06 02:00). All 12 are test labels; 10,828 of 10,932 rows ship. USEmbassy 2021-02-10 07:00 (459.0) stays at 2.84 times sensor 2. Untuned LightGBM mean RMSE 15.34 over the five windows (27.4 / 14.7 / 12.2 / 9.3 / 13.2, February first; 16.69 before) against 36.42 for the training mean and 21.01 for raw sensor 1.

CC (2026-11-05, Lennart): Nakawa 2020-10-13 05:00 (3.06 times the sensors before a morning rise) is dropped with the other 11 single-hour reference errors (REVIEW.md issue 5, A).

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

CC (2026-11-11, Lennart): REVIEW issue 6 (a sixth test month), "Reply (c): Six months with August 2020" to the consistency check: the test windows are October 2020 to February 2021 and August 2020, the end of the June-August dry season that no other test month holds; September 2020 stays out, as Nakawa has no hour before it. August 2020 trains on 47.7% of the hours, the one window under half beside the five months at 57.3% to 92.3%, signed off (SPLIT-14 as amended on 2026-11-11); all its 576 hours are at Makerere.

CC (2026-11-11, Lennart): the declared horizon (one month, no gap, windows starting 2021-02-01, 2021-01-01, 2020-12-01, 2020-11-01, 2020-10-01 and 2020-08-01) is checked, as the monthly refit is the curator's judgment of 2026-11-04, between the hourly feed and a season, and no source gives a cadence.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` declares the cutoffs 2021-02-01, 2021-01-01, 2020-12-01, 2020-11-01, 2020-10-01 and 2020-08-01 (one month, no gap; read in the column's UTC+3 zone); test 834, 1,048, 836, 596, 1,310 and 576 hours, train 9,994, 8,946, 8,110, 7,514, 6,204 and 5,166 (92.3%, 82.6%, 74.9%, 69.4%, 57.3%, 47.7% of 10,828). August's mean reference is 41.4 (58.8 on its train side), and Makerere has 306 earlier hours (15-31 July 2020). `task_summary.split` and `splits_comment` are rewritten (the six months and why, the counts, the shares, September's reason, the horizon's reason); in `curation_comments` the RMSE, copy-share and leak-probe bullets are dated to the five windows of 2026-11-05 (not measured again with August), the CC bullet of 2026-11-05 is marked superseded and a CC bullet of 2026-11-11 is added; `accepted_check_warnings` accepts `splits_train_under_half` with the sign-off. `dataset check`: 0 errors, 0 warnings (README not regenerated).
