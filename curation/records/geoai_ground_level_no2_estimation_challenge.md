---
unique_name: geoai_ground_level_no2_estimation_challenge
name: geoai-ground-level-no2-estimation-challenge
checked_by:
- Myunghwan
data_foundry_status:
- WIP (Triage)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Grouped)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge
- https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/geoai_ground_level_no2_estimation_challenge/dataset.py
source_row: 878
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: estimate daily ground-level NO2 at monitoring stations in Lombardy and Veneto from public satellite and weather data, scored on stations held out, a grouped task.
- Source: Zindi competition "GeoAI Ground-level NO2 Estimation Challenge" (ITU AI for Good with the GEOAIR project, 2024-05-22 to 2024-11-15, 370 on the leaderboard); "develop ML models to estimate surface NO2 concentrations using only public remote sensing data as predictor variables"; data: "Ground-truth data from air quality monitoring stations in the continental part of Lombardy and Veneto regions", Sentinel-5P TROPOMI NO2, CHIRPS precipitation and NOAA land surface temperature from Google Earth Engine; Train.csv, Test.csv, DataDescription.pdf. Rows not checked (Zindi login).
- Use case: an environmental agency estimates surface NO2 where no station measures it (exposure maps, monitoring); fit direct for estimation at unmonitored sites; regime grouped by station, because the source scores "in-situ data from selected ground stations not provided to participants" and states "The ground truth data used for evaluation are independent from the training data set" (`required_split` changed from Temporal to Grouped; a temporal component remains: models must hold "regardless of season").
- Siblings and duplicates: `geoai_challenge_for_air_pollution_susceptibility_mapping` (same series, Milan AQI maps, a different task); `no2` (OpenML, Norwegian road traffic NO2, a different dataset). External collections: none found; related paper on dense NO2 estimation from sparse stations and satellite data (arXiv 2504.17039).
- Papers and pages: https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge (Zindi API read 2026-10-22); discussions 21512, 22132, 23436 (an unofficial third place: features from longitude and latitude, three towns removed as outliers, ensembles); GEOAIR outputs https://www.cirgeo.unipd.it/geoair/index.php?id=outputs.
- Metric: RMSE on `GT_NO2`, the Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error"); leaderboard metric (MET-4); the jury also reported Pearson r and MAE. Inputs: none for the metric; the station id is needed for the grouped split (check it ships).
- Risks for /add-dataset: the satellite columns are retrieved physical quantities at the station point (TROPOMI NO2 column), which reads as a measurement (SEL-15) rather than image descriptors (SEL-13), to confirm; satellite gaps (clouds); whether the Zindi Test.csv holds other stations or other days of the same stations; coordinates and station identity as features under a grouped split (LEAK).
- Priority: gap + (grouped regime thin), use case 0 (the actor is not named by the source), source + (ITU, GEOAIR, a data description), shape + (daily station series over two regions, assumed thousands of rows), risk - (SEL-13 reading and the held-out design to confirm).

GeoAI Zindi challenge to estimate ground-level NO2 concentrations, tagged Non-IID (temporal). Unlike a pure horizon forecast this is an estimation/regression mapping task (predicting NO2 from satellite-column, meteorological and geospatial features), which could be a legitimate tabular regression if the inputs are tabularized. However it is geospatial/satellite-derived and may carry raster modality and heavy wrangling, and the split likely needs to be temporal or spatial. A human must inspect whether the features are genuinely tabular vs. raw raster, the target definition, and the appropriate split regime; place in 2nd tier pending that.

CC (2026-10-30, Myunghwan): Supplied the original GeoAI archive and instructed placement followed by review-added-datasets after screening. Accepted for add-stage qualification of station-held-out daily ground-level NO2 estimation. This is not final shipping, build or publication approval. Read-only claims inspection separately authorized; ownership and claim stage were not changed.

**Consistency check (AI, 2026-10-30):** Independent precedent review found the qualification instruction and proposed task consistent with SEL-15 (physical measurements), SPLIT-1/3/24 (unseen stations), and CLEAN-2/11/15 (missing labels excluded, input missingness and unproven extremes retained). Earlier image/forecasting concerns remain historical hypotheses superseded by the original codebook and measured station structure.

**Assessment (AI, 2026-10-30):** Original curator-supplied release checked: 82,051 labeled station-days, 79 stations, 11 predictors; daily ground-level NO2 in micrograms/m3. Keep source RMSE and whole-station 3x3 folds, with no station/coordinate overlap. The task is retrospective estimation using the complete 2019-2021 archive at other stations, not forecasting. Fold-safe untuned LightGBM RMSE is 10.257 across nine folds versus 11.400 for coordinates/date only; all target values and input missingness are retained except missing-label rows. Two stations have about 72% missing labels, so scores cover observed days. Approximate fit records limited regional/site coverage, unverified ground-label quality control and extraction/latency details. Independent evidence roles and advocate/critic agree after documentation corrections; final scientific inclusion awaits curator review. Upstream task/group probe scores are indicative due to full-frame median imputation; supplementary fits avoid it. Original CC BY-SA 4.0 terms are stated on the Zindi challenge page. Priority 3: gap 0 (no thin category among current accepted definitions), use case 0 (actor inferred; approximate fit), source +1 (original challenge and codebook), shape +1 (82,051 rows, 11 predictors and station groups), risk 0 (no demonstrated likely leak or damaged target).

CC (2026-10-30, Myunghwan): "thse limits are fine". Accepted GeoAI as implemented following the final review: retain observed source labels with undocumented daily aggregation/quality control, limited regional same-period station transfer, and uneven observed-label coverage. Scientific inclusion approved; these uncertainties remain documented. No build or commit requested.

**Assessment (AI, 2026-10-30):** Independent acceptance consistency check found no rule departure or conflicting precedent. USE-8 and EV-7 allow the explicit approximate fit without claiming source QC was verified; CLEAN-11/15 support unchanged observed labels and missing-target removal. Issue 1 closed as implemented; the full panel and exact decision are preserved in review history.

CC (2026-10-30, Myunghwan): Invoked tabarena-build-commit on the accepted GeoAI dataset. Build and local commits authorized; the accepted scientific definition and limitations remain unchanged.

**Build verification (AI, 2026-10-30):** Built the accepted definition as format 2, UUID `01a18eeb-f85e-72fe-90a9-e5ae0e7817e7`, from clean source commit `7b2837be9b83e8ea46a5130a9152b42182fb004f`. Zero bundle errors or warnings; saved-container reload verified. A check using only the traced Train.csv (10,000,397 bytes) reproduced the full checksum, which also equals the accepted pre-build checksum. Rows and splits are unchanged, so the completed task and group probes remain applicable. Raw-input backup retained locally. Local build and commits do not mark upstream integration complete.

CC (2026-11-05, Myunghwan): Requested add-dataset, review-added-datasets and build-commit against updated main, reusing the previous decisions; ask only if new input is needed. The 2026-10-30 acceptance, source RMSE, station holdout and documented limitations remain in force unless new evidence contradicts them.

CC (2026-11-05, Myunghwan): the declared metric, source RMSE on the original NO2 concentration scale, is checked by reuse of the accepted 2026-10-30 implementation under the explicit instruction to repeat the cycle "using our past decision". This records the existing metric choice and reuse instruction, not a newly supplied metric mark.

**Assessment (AI, 2026-11-05):** review panel (focused): ship the previously accepted task; disputed: none after clarifying existing row-only context; for the curator: no new issues, issue 1 remains resolved. Fresh claim/split, column and precedent audits plus isolated participant attacks support reuse of the prior full panel and acceptance. All 82,051 rows, dtypes, 11 features, target, exact nine folds and RMSE scorer match the accepted artifact; only metadata serialization and the explanatory context note change the checksum. Current checks: 27 passed, zero errors/warnings; dtype zero flags; task probe no flags; zero full-feature copies across all folds. Raw-order autocorrelation reflects same-day cross-station observations, not repeated test labels. Other-station label blending is legitimate training information; held-out-station archive summaries are outside context=none. No change to labels, inputs or split is warranted. Priority 3: gap 0 (no thin accepted domain/regime), use case 0 (approximate actor and coverage), source +1 (original challenge/codebook), shape +1 (82,051 rows and 11 predictors), risk 0 (no demonstrated material defect).

**Build verification (AI, 2026-11-05):** The requested build completed from clean definition commit `2687a3ae2ebd33135af563cf9605e3adbc2897b6`: format 2, UUID `01a1adf0-eb77-7e00-8228-2b3c1bc263db`, checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. All 27 checks passed with zero errors or warnings. Saved-container reload verified; a check with only the traced Train.csv (10,000,397 bytes) reproduced the checksum. Rows, nine splits and raw-input selection are unchanged from the October build. The raw-input backup passed ZIP CRC and source SHA-256 checks. The October container is retained because the preserved historical checkout still names it as its current build; no obsolete unreferenced container was deleted. The fresh full group probe completed with the same printed results as October (ridge 0.396, random forest 0.631, LightGBM 0.634, kNN 0.554 R2); indicative preprocessing limitations remain documented. No new decision is needed.

CC (2026-11-05, Myunghwan): Requested another add-dataset, review-added-datasets and build-commit cycle after the internal skills were updated, using the past decisions and asking only if new input is needed. The October acceptance and previously clarified task contract remain the starting constraints.

**Assessment (AI, 2026-11-05):** review panel (focused, internal-skill refresh): ship (independent mediator); disputed: none; for the curator: no new issues, issue 1 remains resolved. The installed pin now matches the 9048f36a source already used in the preceding cycle. Independent audits verify all 32 recorded procedures and 168 tracked source files unchanged, and exact dataframe, dtype, metadata, feature, scorer, checksum and nine-fold identity against the previous November container. Current checks: 27 passed, zero errors/warnings; dtype zero flags; 2,017 tests passed and 286 skipped after an exact 18-case localhost retry. One current LightGBM fold reproduces all 27,659 saved predictions exactly. Full previous model/probe and source evidence is explicitly reused under unchanged conditions, retaining methodological and accepted scientific limits; no new human marks were created. Priority 3: gap 0 (no thin accepted domain/regime), use case 0 (approximate actor and coverage), source +1 (original challenge/codebook), shape +1 (82,051 rows and 11 predictors), risk 0 (no demonstrated material defect). Editor presentation repairs are applied; the requested new build remains pending.
