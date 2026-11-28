---
unique_name: geoai_ground_level_no2_estimation_challenge
name: geoai-ground-level-no2-estimation-challenge
checked_by:
- Myunghwan
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- Panel Data
collections:
- New (BeyondArena)
original_source: Zindi
year: '2024'
collection_period: 1 Jan 2019 - 31 Dec 2021
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

CC (2026-11-05, Myunghwan): Requested another add-dataset, review-added-datasets and build-commit cycle after the review procedures were updated, using the past decisions and asking only if new input is needed. The October acceptance and previously clarified task contract remain the starting constraints.

**Assessment (AI, 2026-11-05):** review panel (focused, qualification refresh): ship (independent mediator); disputed: none; for the curator: no new issues, issue 1 remains resolved. The reviewed source remains 9048f36a, as in the preceding cycle. Independent audits verify all 32 recorded procedures and 168 tracked source files unchanged, and exact dataframe, dtype, metadata, feature, scorer, checksum and nine-fold identity against the previous November container. Current checks: 27 passed, zero errors/warnings; dtype zero flags; 2,017 tests passed and 286 skipped after the initial run and targeted rerun. One current LightGBM fold reproduces all 27,659 saved predictions exactly. Full previous model/probe and source evidence is explicitly reused under unchanged conditions, retaining methodological and accepted scientific limits; no new human marks were created. Priority 3: gap 0 (no thin accepted domain/regime), use case 0 (approximate actor and coverage), source +1 (original challenge/codebook), shape +1 (82,051 rows and 11 predictors), risk 0 (no demonstrated material defect). Editor presentation repairs and the requested new build verification are complete.

**Build verification (AI, 2026-11-05):** The qualification refresh build is complete: format 2, UUID `01a1ae48-7d06-76ac-9741-a58d8233b176`, from clean review commit `a40b46997a5bb7b08a2bac87187c74c109512466`. All 27 checks passed with zero errors or warnings. Saved-container reload verified. A check using only the traced Train.csv (10,000,397 bytes) reproduced checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`, exactly equal to the preceding November build. Rows, all nine splits, metadata and raw-input selection are unchanged. The new input backup passed ZIP CRC and source SHA-256 checks. Earlier containers remain retained as referenced audit baselines; no raw files or containers were removed.

**Assessment (AI, 2026-11-21):** collection facts set from the split audit: 79 fixed monitoring stations read daily on one calendar over 1,096 dates (unit x occasion); the reading arrives with its day, so no `Target:` fact.

**Assessment (AI, 2026-11-21):** review panel (full re-check, without blind review and task gamer: the curator's archive is not on this machine; nothing re-measured): ship after changes; disputed: the siting gap's direction (EV-7, settled: mechanism only), the satellite timing notes (USE-3, settled: written into `known` and a bullet); for the curator: issues 2-3. Wording fixes applied to the definition, build 01a1ae48 stale until rebuilt. Priority 3: gap 0, use case 0 (approximate), source +, shape +, risk 0.

CC (2026-11-24, Andrej): issue 2, change, "Option B: Declare the time basis and the leaf." The definition declares `time_basis = TimeBasis("RetrospectiveFillIn", ...)` (stations outside the network, the 2019-2021 period; not tested: a later year or another region) and `split_leaf = "L-FILL.whole"`; `data_tags` stays ("Spatial",), the build adds the tag and the `Time basis:` line. Rows, folds and score unchanged; the build is stale until rebuilt from Myunghwan's archive.

CC (2026-11-24, Andrej): issue 3, discuss, "Agree." with the latest answer (2026-11-24, recommendation b): option b, the use case drops "identify areas needing monitoring" and ends "to map daily exposure between monitors", a decision the station-held-out daily RMSE tests. Fit stays approximate for the monitoring-site gap.

**Assessment (AI, 2026-11-24):** code-only checks, since the Zindi archive is not on this machine (no data check, README not regenerated): the definition loads with the time basis validated; record collection facts against the definition: 0 problems; `L-FILL.whole` is a grouped leaf with `RetrospectiveFillIn` and the definition ships station groups with that tag: 0 placement problems; split-tree tests 18 passed, 1 skipped; ruff check and format clean.

CC (2026-11-24, Andrej): the declared split (grouped on the station ID, whole stations held out with all their days, time basis `RetrospectiveFillIn`, leaf L-FILL.whole) is checked, as implemented.

CC (2026-11-24, Andrej): verdict ship. Open before a build: README.md and the container are stale until rebuilt from the source archive, which is not on this machine.

## Review

**Outcome:** added. Ship: on 2026-11-24 Andrej declared the time basis `RetrospectiveFillIn` and the split-tree leaf `L-FILL.whole` (issue 2, B) and dropped "identify areas needing monitoring" from the use case, which now ends "to map daily exposure between monitors" (issue 3, b); rows, target, inputs, whole-station split and source RMSE are unchanged. Validity: whole stations are held out as in the source challenge, and copying the nearest station's same-day reading scores worse than the model on 9 of 9 folds. Value: all inputs reach RMSE 10.26 against 11.40 for place and date alone. The numbers come from the panels of 2026-10-30 and 2026-11-05, on the same rows, folds and scorer; nothing was re-measured since, because Myunghwan's archive is not on this machine, and the 2026-11-24 changes were checked on the code only.

**Main points:** No open decision. Not a decision: the build and README.md stay stale until rebuilt from Myunghwan's archive, which also allows the measurements the mediator lists.

**Record judgment:** source, year, regression target and grouped regime agree with the definition. Priority 3: source and shape positive; use case approximate; no thin accepted domain or regime and no demonstrated material leak.

**Issues for Myunghwan:**

1. **Retain the source labels while daily aggregation and quality control remain undocumented?**

   - **Problem:** The source codebook identifies ground-station NO2 measurements but does not document the daily aggregation or quality-control procedure.
   - **Effect on the task:** Scores measure agreement with observed released labels; they cannot establish performance on missing monitor days or verify every zero or extreme against sensor flags.
   - **Experiments:** Original-source comparisons preserved all observed target values, including seven zeros and the maximum; only 4,533 rows without targets were removed. No specific invalid-label mechanism was demonstrated.
   - **Consistency:** Preserve faithful source measurements and disclose unverified processing rather than inventing repairs.[^geoai-labels]
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retain with caveats (implemented) | Keep observed source labels and documented limits | Faithful to the published estimation task | Daily label processing remains unverified |
     | B | Defer for owner clarification | Wait for source aggregation and QC details | May resolve the source uncertainty | Delays the task without demonstrated label corruption |

   - **Recommendation:** A. **Decision:** retained under Myunghwan's recorded acceptance.

**Myunghwan (2026-10-30, ok):** "thse limits are fine".

**Resolved (2026-10-30, Myunghwan):** Accepted as implemented with undocumented daily label aggregation/quality control, regional same-period station transfer and uneven observed-label coverage explicitly retained. On 2026-11-05 Myunghwan requested the updated-main cycle "using our past decision"; this preserves the historical acceptance, not a new answer to a new scientific issue.

[^geoai-labels]: USE-8 and EV-7 require honest scope and uncertainty; CLEAN-11/15 retain unproven extremes and omit missing targets. [Original challenge and data description](https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge/data).

3. **Drop "identify areas needing monitoring" from the use case?**

   - **Problem:**
     - The use case ends with "to map exposure and identify areas needing monitoring".
     - Deciding where to monitor acts on annual means and limit exceedances, while the target and RMSE score daily station values.
   - **Background:** the EU air-quality directive assesses zones on annual means and on the count of days and hours above limit values ([Directive 2008/50/EC](https://eur-lex.europa.eu/eli/dir/2008/50/oj)), and network design follows those; the domain practitioner (2026-11-21) raised it.
   - **Effect on the task:** none on the data; the stated use promises a decision the score does not measure.
   - **Consistency:** none decided on this point; the use case names a decision the target and the score serve[^x21g2].
   - **Panel:** no disagreement; the domain practitioner, critic, advocate and mediator agree.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | No change | keeps the text Myunghwan accepted | promises a decision the score does not measure |
     | B | Drop the clause | The use case ends "to map daily exposure between monitors" | the use matches what is scored | changes text Myunghwan accepted |

   - **Recommendation:** B: deciding where to place monitors works from annual means, which a daily station score does not test. **Decision:** keep the clause (A), or drop it (B)?

   **Notes for the AI:** On B, `use_case` becomes "An air-quality analyst reconstructs daily pollution at unmonitored locations within the observed region, using the complete 2019-2021 archive from other stations after all daily products are available, to map daily exposure between monitors."

   [^x21g2]: **USE-1** (Must): the use case names an actor, a moment and a decision the target serves.

   **Andrej (2026-11-23, discuss):** But is this still a valid use case then? Also, what did the source do?

   **Answer (AI, 2026-11-23):** Yes: daily exposure between monitors is a real use, and it is what the station-held-out daily RMSE tests. Neither source names deciding where to monitor; the clause came from the screening's guess ("exposure maps, monitoring").

   * **Problem:**
     - What the sources state and score:

       | Source | Stated aim | Task | How it is scored |
       |---|---|---|---|
       | [Zindi challenge](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge) (2024, this data) | "develop ML models to estimate surface NO2 concentrations using only public remote sensing data as predictor variables"; "explore innovative approaches to NO2 monitoring and modelling"; winners hand in "a model file ... that can be used to estimate surface NO2 levels" | daily NO2 at stations in Lombardy and Veneto, 2019-2021 | leaderboard: "Root Mean Squared Error"; jury: "in-situ data from selected ground stations not provided to participants" with r, RMSE and MAE, "regardless of season and location in the study area"; "The ground truth data used for evaluation are independent from the training data set" |
       | [Cedeno Jimenez, Pugliese Viloria and Brovelli 2023](https://doi.org/10.3390/ijgi12030107), IJGI 12, 107 | "an alternative to ground sensor measurements"; "relevant for regions where no NO2 ground sensors are present, which in most cases, is a limitation for LMICs" | one daily mean over the 16 stations of the Metropolitan City of Milan (12:00-15:00), 2019 to September 2022, from Sentinel-5P and ground weather stations | first 80% of the days for training, last 20% for test, "the way in which the algorithm is planned to be used (i.e., daily consecutive estimations)"; best RMSE 2.89 µg/m3 |

     - "Monitoring" on the Zindi page means estimating concentrations ("NO2 monitoring and modelling"), not siting stations. The paper aims at the reverse of siting: estimates where no station exists, in other countries.
     - The paper is the precursor, not the same task: one city mean, no station held out, ground weather as input. Its future work ("replacing the use of meteorological ground sensors with only satellite-based data") is the challenge's "only public remote sensing data". The [GEOAIR outputs page](https://www.cirgeo.unipd.it/geoair/index.php?id=outputs) lists the challenge as run by Politecnico di Milano (the paper's group) and Padova.
   * **Background:** who uses daily NO2 at places without a monitor:

     | User | Decision | Source | Tested by the station-held-out daily RMSE? |
     |---|---|---|---|
     | Epidemiologists | assign daily exposure to addresses or areas for short-term health studies | [de Hoogh et al. 2019](https://pubmed.ncbi.nlm.nih.gov/31415154/) (daily NO2 for Switzerland, made available "to facilitate health research"); [ISPRA with the Lazio epidemiology department](https://www.isprambiente.gov.it/en/news/new-high-resolution-maps-of-air-pollution-in-italy) (1 km maps of NO2, PM10 and PM2.5 for "population exposure" and "epidemiological research") | yes: a daily value at a place without a monitor, in the period the network covers |
     | Air-quality agencies | supplement fixed stations with modelling when assessing zones under [Directive (EU) 2024/2881](https://eur-lex.europa.eu/eli/dir/2024/2881/oj), which ISPRA names for its maps | ISPRA page above | partly: assessment acts on annual means and counts of exceedances, which daily estimates feed but the score does not test |
     | Health-impact and exposure-inequality studies | burden by area or population group | ISPRA page above | partly: these usually work from annual means |
     | Daily alerts | warn the public on the day | none of the sources | no: the satellite inputs arrive days late and final CHIRPS about seven weeks (the definition's fit reason) |

     - Holding out whole stations over the same days is the leave-sites-out validation of daily exposure models, the domain practitioner's point of 2026-11-21, and the source jury's design.
     - Gaps that stay with any wording, already in the fit reason (fit approximate): the test points are monitoring sites, which are chosen (traffic sites among them); the inputs are satellite only; the region and period are those of training.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the clause (implemented) | No change | text Myunghwan accepted | promises a siting decision that neither source states and the score does not test |
     | b | Drop it, lead with daily exposure | use case ends "to map daily exposure between monitors" (the Notes for the AI above) | names a decision practitioners take with these estimates and the score tests[^x23g3] | changes text Myunghwan accepted |
     | c | The source's wording | use case ends "to estimate surface NO2 where no ground station measures it" | closest to the Zindi text | names no decision; the paper's "where no sensors are present" means other countries, a transfer this split does not test |

   * **Recommendation:** b. The fit stays approximate for the monitoring-site gap. **Decision:** a, b or c?

   [^x23g3]: **USE-1** (Must): the use case names an actor, a moment and a decision. **USE-9** (Should): data that mirror another use practitioners have take that use; b removes a promise rather than rephrasing to excuse a gap.

   **Answer (AI, 2026-11-24):** The new split rules change no option and no recommendation here. The split tree reads this use case at its first panel question: a station not in the network, within the period the data covers, is a fill-in. Options a and b keep "unmonitored locations within the observed region" and the 2019-2021 archive, so both reach the leaf of issue 2 (whole stations held out, time basis `RetrospectiveFillIn`). Option c also estimates inside the covered period, so it reaches the same leaf; its con stands, since the paper's "regions where no NO2 ground sensors are present" is a transfer the time basis of issue 2 names as untested. Recommendation b stands. **Decision:** a, b or c?

   **Andrej (2026-11-24, discuss):** Agree.

   **Resolved (2026-11-24, Andrej):** b, as the latest answer recommends: `use_case` drops "identify areas needing monitoring" and ends "to map daily exposure between monitors", the Notes for the AI's text; the fit stays approximate for the monitoring-site gap. Code-only checks pass (definition loads, ruff clean); no data check and no README regeneration, since the Zindi archive is not on this machine.

2. **Declare the time basis `RetrospectiveFillIn` and the split-tree leaf, as the other datasets with this split do?**

   - **Problem:**
     - The split tree, walked from how the data was collected (fixed stations read every day), ends at "Grouped · `RetrospectiveFillIn` (whole units, areas or groups)", which is the split this definition ships.[^x21g1]
     - The two other datasets that reach this leaf (5g_energy_consumption, fraud_detection_in_electricity_and_gas_consumption_1m) declare `time_basis = TimeBasis("RetrospectiveFillIn", ...)` and `split_leaf = "L-FILL.whole"` on the open split PRs; this definition declares neither and has only `data_tags = ("Spatial",)`.
     - Nobody chose the difference: the definition was written before the split rules.
   - **Background:** the tree reads the use case "unmonitored locations within the observed region, using the complete 2019-2021 archive" as filling in the covered period, with whole stations missing that the station ID keys. The leaf's same-time check holds: the target is each station's own reading, not a value all stations share on a day, and copying the nearest station's same-day reading scores worse than the model on 9 of 9 folds (2026-11-05 panel).
   - **Effect on the task:** none on rows, folds or scores. The build adds the `RetrospectiveFillIn` tag and renders the `Time basis:` line into the curation comments, which says what the split tests (stations outside the network, the same period) and what it cannot (a later year, another region); the checksum moves.
   - **Experiments:** none needed. Code checks on 2026-11-24 (no data): the current definition passes with the note that the split is not temporal and does not say why; option B, written as in the Notes for the AI, passes the definition check, the record's collection facts and the leaf check (it ships the grouped split and the tag that leaf names).
   - **Consistency:** 5g_energy_consumption and fraud_detection_in_electricity_and_gas_consumption_1m declare this time basis and leaf; A departs from them, B follows.
   - **Panel:** no disagreement; the precedent checker, advocate, critic and mediator agree (2026-11-21, under the old tag name `Retrospective`).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | no time basis and no leaf; the splits comment says the split tests neither forecasting nor other regions | no rebuild | departs from the two other datasets with this split, with no fact that sets it apart |
     | B | Declare the time basis and the leaf | `time_basis = TimeBasis("RetrospectiveFillIn", ...)` and `split_leaf = "L-FILL.whole"`; `data_tags` stays `("Spatial",)`, the build adds the tag and the line | the same metadata as the two other datasets; states that other stations' same-day readings are the use | the checksum moves, so a rebuild from Myunghwan's archive |

   - **Recommendation:** B: nothing sets this dataset apart from the two others with its split, and the change touches no row, fold or score. **Decision:** keep as is (A), or declare the time basis and the leaf (B)?

   **Notes for the AI:** On B: import `TimeBasis` from `data_foundry.time_basis`; add `split_leaf = "L-FILL.whole"` and `time_basis = TimeBasis("RetrospectiveFillIn", "daily readings of 79 ground monitors of ARPA Lombardia and ARPAV (Veneto), 2019-01-01 to 2021-12-31, with same-day satellite and precipitation inputs; the use case reconstructs daily NO2 at locations without a monitor in that period, while the other stations of the same days are measured (date and coordinates are features), so their same-day readings are the use, not a leak (copying the nearest same-day station scores worse than the model on 9 of 9 folds). Not tested: a later year, or a region outside the network.")`; do not add the tag to `data_tags` or a `Time basis:` bullet to `curation_comments` by hand (the definition check refuses both beside a `TimeBasis`); add to the splits comment "The split tree gives Grouped · RetrospectiveFillIn (whole units, areas or groups), L-FILL.whole"; the record says the build is stale until rebuilt from the archive.

   [^x21g1]: **SPLIT-32** (Should): a definition that follows a use-case prototype declares it as its time basis, with the fact behind it and what the split cannot test; `RetrospectiveFillIn` fills in what is missing for the time the data covers, and no row of a test row's time may carry its target. **SPLIT-36** (Should): the split comes from walking the split tree from the record's collection type, and the definition names the leaf it reaches in `split_leaf`. The walk: [PAN.when] fill in the covered period, [FILL.later] no (the labels arrive with their day), [FILL.scattered] whole units (stations not in the network), [FILL.key] yes (station ID), leaf [L-FILL.whole].

   **Andrej (2026-11-24, change):** Option B: Declare the time basis and the leaf.

   **Resolved (2026-11-24, Andrej):** B: `dataset.py` imports `TimeBasis` and declares `split_leaf = "L-FILL.whole"` and `time_basis = TimeBasis("RetrospectiveFillIn", ...)` with the reason from the Notes for the AI; `data_tags` stays ("Spatial",); the splits comment names the leaf and the split-walk bullet says the time basis is declared. Code-only checks (no data on this machine): the definition loads with the time basis validated, the record's collection facts agree with it (0 problems), the leaf check finds 0 placement problems (grouped split, `RetrospectiveFillIn`), split-tree tests 18 passed and 1 skipped, ruff clean. The data check did not run and README.md was not regenerated; the build is stale until rebuilt from Myunghwan's archive.

**Review panel:** ship after changes (mediator, 2026-11-21, full re-check without blind review and task gamer: data not available). Applied without a decision: the known and fit_reason wording, the satellite overpass and processor bullet, both agencies named, the unmeasured one-vote-per-station note. Disputed and settled: the siting gap is named as a mechanism, not a direction of bias (no station-type data); the satellite timing and quality filters go into `known` and a notes bullet. For the curator: issues 2 and 3. Issue 1 stays resolved. Earlier panels (2026-10-30, 2026-11-05): ship; their reports below are history.

<details><summary>Mediator (2026-11-21)</summary>

**Mediator: geoai (geoai_ground_level_no2_estimation_challenge), 2026-11-21**

Inputs read: claim auditor, domain practitioner, precedent checker, advocate and critic openings and rebuttals, column
audit (`pr59_columns/findings/geoai.md`), `dataset.py`, the record (Comments and `## Review`). Not available this
round: data, `check.log`, probes, blind review, task gamer (geoai's archive is not on this machine). No experiment run:
every open fact needs the archive. Data-backed numbers below are from the 2026-10-30 and 2026-11-05 reports in the
record, measured on rows, folds and scorer verified identical to the current definition (checksum `v2:79bbb806…`).

**Judgment record**

```text
Verdict: ship after changes (text and one tag; no change to rows, target, inputs, split or metric).
Validity: USE-1 holds (source task: stations withheld, "ground truth ... independent from the training data set");
  SPLIT-1/3 hold (whole stations out, 3x3, 26-27 test stations per fold, no shared station or coordinate);
  LEAK-16 holds (0 cross-fold copies; nearest-station copy 12.47 vs 10.37, worse 9/9);
  SPLIT-32 q2 holds (other stations' same-day labels are the use, not the target);
  USE-3 holds in substance, `known` text incomplete (fix below); USE-5/EV-7: bullet 4 names one "ARPA" (fix below);
  USE-8 holds (fit approximate), gaps not named (fix below).
Value: TP-4 holds (coords+date 11.40 vs all inputs 10.26 RMSE; no single rule reaches it); TP-2 spread
  ridge 0.396 to LightGBM 0.634 R² (untuned, indicative).
Quality: SPLIT-32/36 departure (no `Retrospective` tag, no `Time basis:` line) not chosen, timing of PR #59;
  MET-17 note half missing (inequality stated, ranking effect unmeasured).
Weighed: source + (ITU/Zindi, codebook, CC BY-SA 4.0), shape + (82,051 rows, 79 stations), use case 0 (actor
  inferred, approximate), risk 0. Priority 3 unchanged.
For the curator: N1 (time basis tag + line), N2 (use-case clause); request: the archive for the rebuild and four
  pending measurements.
```

Advocate and critic agree on the verdict and on every remedy. Two details were disputed; both are settled by the rules
(below), so neither goes to the curator.

**Disputed points, settled**

| Point | Advocate | Critic | Settled | Rule |
|---|---|---|---|---|
| `fit_reason` says the held-out sites "over-represent hotspots" | Direction unmeasured; state the mechanism only | Include the effect | **Advocate.** No one has joined the station IDs to the ARPA registries; the traffic/background mix of the 79 stations is unknown. Name the mechanism (no input encodes siting; a TROPOMI pixel is about 3.5 x 5.5 km), not a direction. | EV-7 (Must) |
| Processor change and QA thresholds: "fit note" without a text fix | Called it a fit note, listed no edit | Write it into `known` and a comments bullet | **Critic.** USE-3 asks the point to say what is known and when; the definition says only "for that day" and nothing on QA or processor versions. Wording fix. | USE-3 (Must) |
| Order of work: tag now or with the rebuild | Edit `dataset.py` now, record build `01a1ae48` as stale | Wait for the archive, one rebuild | **Edit now, rebuild later.** Rows and folds do not change, so the 11-05 evidence still applies (EV-8); the record must say the build is stale and this round re-measured nothing (EV-7). Logistics, not a curator call, unless Andrej prefers to hold all edits until the archive is back. | EV-7, EV-8 |

**Changes to make now (no decision needed)**

1. `task_summary.known` (USE-3): the column audit's text: "The location and date; that day's CHIRPS precipitation;
   daytime land-surface temperature, aerosol index, cloud fraction, satellite nitrogen dioxide columns and tropopause
   pressure from single early-afternoon satellite overpasses on that day."
2. `fit_reason` (USE-8): column audit's second sentence (latency: days for Sentinel-5P, about seven weeks for final
   CHIRPS; daily QC undocumented) plus one clause: "satellite-only inputs by the source's design (no meteorology or land
   use); held-out monitoring sites, whose traffic or background siting no input encodes, stand in for unmonitored
   places." No direction of bias.
3. Comments bullet on the satellite inputs (USE-3, EV-7): one overpass; NO2_trop QA ≥ 0.75 (40.7% missing) vs ≥ 0.5 for
   the other five (14.8%, same 12,118 rows); TROPOMI processor v1.4 (Dec 2020) and v2.2 (Jul 2021) inside the period,
   shared by train and test because folds share all dates. Do not name the LST product until DataDescription.pdf is
   read (the 0.02 K grid is an inference from 13 README values; the source says "NOAA").
4. Comments bullet 4 (USE-5, EV-7): the codebook says "ARPA"; the source page says Lombardy and Veneto, which have
   separate agencies (ARPA Lombardia, ARPAV). Name both, and say the daily-mean rule may differ between them and is
   unmeasured (integer-looking Veneto values vs decimal Lombardy values in the README sample; rounding alone costs at
   most about 0.29 RMSE). This stays inside resolved issue 1 (undocumented aggregation, accepted by Myunghwan); it does
   not reopen it.
5. Metric bullet (MET-17, Should): score stays per row (each station-day is its own estimate on a daily map). The
   inequality is stated (298 to 1,093 labelled days, two stations at about 72% missing); add "how far one vote per
   station moves the ranking: not yet measured" until the Kendall tau exists. Precedent: asp_potassco and
   video_transcoding (per row, with the note).
6. Record (EV-7): the 2026-11-21 Assessment says this round re-measured nothing on the data, lists what waits for the
   archive (below), and that the 11-05 evidence was verified on identical rows, folds and scorer.

**Issues for the curator (ranked)**

**N1. Add `Retrospective` and a `Time basis:` line?** (SPLIT-32 Should, SPLIT-36 Should) — NEW
- Problem: the tree leaf (Panel data → fill in the covered period → whole units missing) is Grouped · `Retrospective`
  (whole units). Both v0.2 definitions there carry the tag and the line (5g_energy_consumption `("Retrospective",)`;
  fraud_detection_in_electricity_and_gas_consumption_1m `("Spatial", "Retrospective")`). geoai has `("Spatial",)`
  only. Nobody chose this: PR #59 predates the split rules.
- Effect: the same-time check is in prose but not where the validator reads it. The split itself is right.
- Evidence: all panel members agree; the same-time reading rests on the 11-05 gamer (closest pair 7 km, r = 0.968,
  equal labels on 0.094% of days; copying the nearest same-day station worse on 9/9 folds).
- Options: A add the tag and the precedent checker's line (checksum moves; rebuild needs the archive); B keep and
  explain the departure in `splits_comment`.
- Recommendation: **A**. It could be applied as plain rule compliance; it is an item only because it moves the
  checksum of a curator-accepted build and the split PRs own time-basis tags. geoai is on no `splits/*` branch and not
  on main (only PR #59), so the edit goes into PR #59.

**N2. Drop "and identify areas needing monitoring" from the use case?** (USE-1 Must) — NEW
- Problem: network design under Directive 2008/50/EC acts on annual means and exceedance counts per zone; the target
  and RMSE score station-day estimates.
- Effect: the use case claims a second decision the metric does not score.
- Evidence: practitioner finding 5; advocate and critic both concede.
- Options: A drop the clause, lead with daily exposure reconstruction and gap-filling; B keep.
- Recommendation: **A**. An item because the use case text was accepted by Myunghwan (2026-10-30).

**Request (not a decision): the archive.** Rebuild after N1 and the edits above, and measure:

| Item | Measure |
|---|---|
| MET-17 sentence | Per-row vs 1/n_station weighted RMSE ranking of 2-3 models over 9 folds, Kendall tau |
| Two-agency labels | Share of integer `GT_NO2` by ID prefix (`X…` vs province codes); fractional parts × 24 and × 240 |
| Siting (optional) | Join station IDs to ARPA registries; RMSE by station type |
| Column-audit leftovers | NO2_trop missing share and median by month (processor steps); LST mod 0.02; DataDescription.pdf collection IDs; second ~72%-missing station |

None of these can change validity: the worst case (integers from a different daily rule) would add a note, and a low
tau would add a sentence, not a weight (each row is a decision of its own).

**Open issues already in the record**

- Issue 1 (labels with undocumented aggregation/QC): resolved 2026-10-30 by Myunghwan. **Keep as resolved.** Change 4
  refines its note; it does not reopen it.
- Horizon block "H" and 2026-11-21 split-audit issues: **none exist in the record.** The split audit left only the
  2026-11-21 Assessment line (facts). N1 covers what a Horizon block would have raised. Nothing to keep, revise or
  withdraw.

**Agreed facts**

- 82,051 labelled station-days, 79 stations (unique coordinates), 1,096 dates 2019-01-01 to 2021-12-31; 4,533
  rows without target dropped; 7 zeros and max 188.23 kept; inputs not imputed.
- Source task: daily NO2 at stations withheld from participants, same period; leaderboard RMSE on the original scale
  (Pearson r and MAE jury-only). Six Zindi test stations cover the full period (file-size arithmetic).
- Shipped split: whole stations, 3x3, 26-27 test stations per fold, `context="none"`.
- Satellite NO2 columns are column densities (mol/m²), not the surface target. All inputs exist at the retrospective
  point; latency days (S5P) to about seven weeks (CHIRPS final).
- Signal: dummy 15.9-19.0 RMSE per fold; coords+date 11.40; all inputs 10.26; group probe R² 0.396 / 0.554 / 0.631 /
  0.634 (ridge / kNN / RF / LightGBM, untuned, median-imputed).
- Last checks: 27 passed, 0 errors, 0 warnings (11-05); none ran this round.
- Licence CC BY-SA 4.0; login-only download is a note (EV-4), not a verdict reason.

**Consistency with precedent**

- Split, `context="none"` and same-day other-station labels: same leaf and same reading as 5g_energy_consumption.
- S5P retrievals as physical inputs (SEL-15): as airqo_african_air_quality_prediction_challenge (Myunghwan, 11-05);
  geoai's 79 stations set it apart from airqo's 4-city deferral.
- Source RMSE (MET-4): as 5g and airqo.
- MET-17 per row with a note: as asp_potassco_classification and video_transcoding_time_prediction.
- The only departure (no time-basis tag) is N1, unchosen. No drift; no third exception of a kind.
- Observation, no item: the screening banner "AI-FILLED — UNVERIFIED … NOT from inspecting the data" at the top of
  Comments predates the 10-30 data checks; the editor may want to scope it to the screening paragraph.

</details>

<details><summary>Advocate (2026-11-21)</summary>

**Advocate opening: geoai (geoai_ground_level_no2_estimation_challenge), 2026-11-21**

Position: ship as defined, with three text fixes and one metadata fix. No change to rows, target, inputs, split or
metric. Nothing ran this round (the data is not on this machine; no check.log, probe, blind-review or task-gamer
output). Every number below is from earlier data-backed reports in the record's `## Review` (2026-10-30 and 11-05) or
from this round's claim audit, domain practitioner, precedent check and column audit. None of this round's agents
refuted a claim.

**1. The task is the source's own task, scored the source's way (USE-1 Must, SPLIT-1 Must, MET-4 Should)**

- Zindi/ITU scores estimates "in-situ data from selected ground stations not provided to participants"; "the ground
  truth data used for evaluation are independent from the training data set" (claim audit 11-21, claims 1, 15, 21).
- The definition holds whole stations out over all dates: 3x3 folds, 26-27 test stations per fold, zero shared
  stations or coordinates in all nine folds (claim audit 11-05; README 11-21).
- RMSE on the original µg/m³ scale is the leaderboard metric. The practitioner keeps it: it is the field's first number,
  and FAIRMODE's quality objective is an RMSE (domain practitioner 11-21, question 5).
- The precedent check walks the split tree to Panel data -> fill in the covered period -> Grouped · `Retrospective`
  (whole units). The shipped split is that leaf (SPLIT-36). 5g_energy_consumption is the same decision.
- Answers: any claim that the split or metric is wrong. The source, the tree and the field agree.

**2. Same-day labels at other stations are the use, not a leak (SPLIT-32 question 2 Should, LEAK-16 Must)**

- SPLIT-32 asks whether any training sample of a test sample's time carries its target. The 11-05 gamer measured it:
  - the closest pair (X5607/X10452, 7 km, r = 0.968) has equal labels on 0.094% of days, interstation RMSE 4.89;
  - copying the nearest same-day station: RMSE 12.47 against the 10.37 baseline (worse on 9/9 folds);
  - the same-day mean of all training stations: 11.84 (worse on 9/9);
  - a half blend gains 0.24 (7/9). That is kriging-style signal, which the practitioner uses daily.
- Zero exact covariate copies across folds; zero duplicate station-days (LEAK-16).
- So no day needs to be grouped. 5g's time-basis line makes the same reading ("while the other stations of the same
  hours are measured"; precedent check 11-21).

**3. The task has signal beyond place and calendar, and models spread (TP-4 Must, TP-2 Should)**

| Model (untuned, 9 station folds) | Score |
|---|---|
| Train-mean dummy | RMSE 15.9-19.0 per fold (target sd 17.1) |
| LightGBM on coordinates and date only | RMSE 11.40 |
| LightGBM on all 11 inputs | RMSE 10.26 (10.37 in the 11-05 kit) |
| Group probe R²: ridge / kNN / random forest / LightGBM | 0.396 / 0.554 / 0.631 / 0.634 |

- No single feature or published rule reaches the methods (TP-4 step 1 not met). The satellite inputs add 1.1 RMSE over
  place and date.
- Ridge to LightGBM spans 0.24 R². The probe is untuned and median-imputes the whole frame, so I claim spread, not
  TP-3's tuned spread. It is enough to rule out `Trivial` and `No Signal`.

**4. The inputs are known at the declared point; the date is a fair input (USE-3 Must, LEAK-10, time-column actor test)**

- Column audit 11-21: all 11 inputs exist at the retrospective point. Nothing is post-outcome, lagged or fitted on the
  whole release. Sentinel-5P arrives within days, final CHIRPS in about 7 weeks. The use case is after the fact.
- The satellite NO2 columns are column densities in mol/m², not the surface target (GEE catalogue; claim 8; LEAK-2).
- The analyst holds the date and place when mapping a past day, so both are inputs (time-column actor test).
- The NO2 processor changes (v1.4 Dec 2020, v2.2 Jul 2021) hit train and test alike, because every fold shares all
  dates. That is a fit note, not a split problem (column audit 11-21).

**5. The label limits are real, small, and already accepted (USE-8 Must, CLEAN-11/15, curator decision)**

- Myunghwan accepted the undocumented daily aggregation and QC on 2026-10-30 ("thse limits are fine"; issue 1,
  resolved). He kept that on 11-05.
- This round's new hypothesis (two agencies, ARPAV integer means vs ARPA Lombardia decimals; claim audit N2,
  practitioner finding 3) refines that accepted limit. Rounding to whole µg/m³ costs at most about 0.29 RMSE against
  ~10.
- Mildest remedy: name both ARPAs in the codebook bullet. Measure the integer share by ID prefix when the archive is back
  on NFS. No data change unless the integers turn out to come from a different daily rule.
- Monitoring sites stand in for unmonitored places, and station type is missing (practitioner finding 1). That is
  why fit is `approximate` already. Remedy: name the mechanism (traffic vs background siting) in `fit_reason`, and say
  "satellite-only by design" (finding 2). Wording only. USE-8 asks for a named gap, not an exclusion.

**6. The two process gaps have cheap fixes that keep the dataset (SPLIT-32/36 Should, MET-17 Should)**

- **Time basis** (precedent check finding 1, NEW). The `Retrospective` tag and `Time basis:` line are missing because
  PR #59 predates the split rules. No one chose to depart. Fix (option a): add the tag and the precedent checker's
  sketched line. It is metadata only. The checksum moves, so a rebuild follows when the data is available.
- **MET-17 note** (claim audit N1, NEW). Each station-day is its own estimate on a daily map, so the score correctly
  stays per row. MET-17 then asks one sentence on how far one vote per station moves the ranking. Only about 2 of 79
  stations are short (298 vs median 1,068 rows), so the effect should be small. Fix: measure Kendall tau when the data
  is back, and add the sentence. The metric does not change.
- Use-case wording (practitioner finding 5): drop "identify areas needing monitoring". Network design works on annual
  means, not daily station-day error. Lead with daily exposure reconstruction.

**7. Access and this round's missing data are no verdict reasons (PROV-1 Must, EV-4 Must)**

- The source is known: Zindi/ITU AI for Good with GEOAIR, a codebook (DataDescription.pdf), CC BY-SA 4.0 (claim 24).
  PROV-1 holds.
- The login-only download is a "request-only download" under EV-4: a one-line note, never a reason for a verdict. The
  definition pins the archive and Train.csv SHA-256. Three builds reproduced their checksums from the traced Train.csv
  alone (10-30; and two on 11-05, both `v2:79bbb806…`; the October checksum differs only by a serialized empty
  metadata field). Zindi's "private property of the client" terms belong on the release
  checklist (EV-4), not here.
- That this round could not re-measure is a gap in our evidence, not a defect in the dataset. The 11-05 evidence was
  verified bit-identical against the current rows, folds and scorer (claim audit 11-05). The open measurements (N1,
  N2, column-audit leftovers) are listed and none can change validity.

**What I concede now**

- The time-basis tag and line, the MET-17 sentence, the use-case wording and the `fit_reason` sharpening are real gaps.
  All of them are fixes inside the dataset, not reasons to hold it.
- The second ~72%-missing station is not visible in the summaries (claim 5). The two-agency label hypothesis is
  untested.

</details>

<details><summary>Advocate rebuttal (2026-11-21)</summary>

**Advocate rebuttal: geoai, 2026-11-21**

We agree on the verdict: ship, no exclusion, keep RMSE, the whole-station split, the inputs and the cleaning. All six
of the critic's points are fixes to text or metadata. I concede all six in substance and dispute two details.

| # | Critic's point | Answer | Why |
|---|---|---|---|
| 1 | `fit_reason` leaves out siting, satellite-only inputs and input latency (USE-8) | **Concede the remedy. Dispute one effect sentence.** | My opening (point 5) proposed the same wording. But "a siting mix that over-represents hotspots" is a hypothesis: nobody has joined the station IDs to the ARPA registries, so the traffic/background mix of the 79 stations is unmeasured. The wording should state the mechanism (no input encodes station siting; a TROPOMI pixel is about 3.5 x 5.5 km) and leave out the direction of the bias until it is measured (EV-7). The practitioner gave the measurement: join station type and report RMSE by type. |
| 2 | Use case names network design, which the daily target does not score (USE-1) | **Concede.** | The same as my opening point 6. Drop "and identify areas needing monitoring" and lead with daily exposure reconstruction. |
| 3 | The label is called one agency's; the values suggest two pipelines (USE-5, EV-7) | **Concede.** | Name ARPA Lombardia and ARPAV in bullet 4. Say the daily rule may differ between them and that this is unmeasured. Measure the integer share by ID prefix when the archive is available. Rounding costs at most about 0.29 RMSE, so this stays a note inside resolved issue 1 unless the integers come from a different daily rule. |
| 4 | No `Retrospective` tag and no `Time basis:` line (SPLIT-32/36) | **Concede. Dispute only the order of work.** | Add option (a) now; the precedent checker's sketch is ready. The edit does not have to wait for the archive. Make it in `dataset.py` and record that build `01a1ae48` is stale until a rebuild from the curator-supplied archive. The rows and folds do not change, so the 11-05 evidence still applies (EV-8). |
| 5 | MET-17 note missing (MET-17) | **Concede.** | The score stays per row. The Kendall tau measurement and its one sentence wait for the data. Until then, the notes can say the measurement is pending. |
| 6 | `known` and the comments omit the overpass, the QA thresholds and the processor change; LST is "NOAA" on a 0.02 K grid (USE-3) | **Concede.** | Use the column audit's `known` text and add one bullet on QA 0.75 vs 0.5 and processor v1.4/v2.2. I agree that the LST product should not be named until DataDescription.pdf confirms it: the 0.02 K grid is an inference from 13 README values (claim 25). |
| Closing | The record should say the 11-21 round verified nothing on the data (EV-7) | **Concede, with one addition.** | The note should also say that the data-backed evidence comes from 11-05, measured on rows, folds and a scorer verified identical to the current definition (11-05 claim audit). That keeps "not re-measured" apart from "unverified". |

The critic raised no new fact against validity or value, so my opening points 1 to 4 and 7 stand: the source task and
split, no same-day leak, signal and spread beyond place and date, inputs known at the prediction point, and a known
source. Agreed result: ship after the wording and tag fixes. The rebuild, the MET-17 sentence and the two-agency check
follow when the archive is available.

</details>

<details><summary>Critic (2026-11-21)</summary>

**Critic opening brief: geoai (geoai_ground_level_no2_estimation_challenge), 2026-11-21**

Position: ship only after the changes below. None of them is an exclusion reason. The task is real (unseen-station
daily NO2, source RMSE, whole-station folds), and no audit found a leak or a wrong label. What is wrong is that the
definition's text says less than the evidence now shows, and one Should of the split rules is not met.

Ground for all points: the data is not on this machine. This round ran no check, probe, blind review or task gamer
(claim auditor: no check.log, leak/, task/, dtype/ or group.log). Every data fact below comes from the README of build
`01a1ae48` or from the 11-05 panels in the record's `## Review`.

**1. fit_reason does not name the gaps that make the fit approximate (USE-8, Must; USE-5)**

- Problem: fit_reason says only "Monitoring-site coverage approximates unmonitored locations" and that latency and
  label QC are not established. Three concrete gaps are known and unnamed:
  - Held-out points are monitoring sites, chosen and classed by the agencies (traffic, background, industrial). A
    TROPOMI pixel (about 3.5 x 5.5 km) cannot see a street canyon, and no input encodes station type. Part of the
    target is siting variance no input explains (domain practitioner, finding 1).
  - Satellite-only inputs by the source's design: no meteorology (wind, boundary-layer height) and no land use, which
    every operational model uses (practitioner, finding 2; Zindi page "only public remote sensing data").
  - Inputs arrive within days (Sentinel-5P) to about seven weeks (final CHIRPS) after the day (column audit 11-21).
- Effect: a reader takes the score as error at unmonitored places. It is error at other monitors, with a siting mix
  that over-represents hotspots.
- Remedy (wording, no rebuild of data): fit_reason = the column audit's text plus one clause: "satellite-only by the
  source's design; held-out monitoring sites, whose traffic or background siting no input encodes, stand in for
  unmonitored places."

**2. The use case names a decision the daily target does not serve (USE-1, Must)**

- Problem: use_case ends "to map exposure and identify areas needing monitoring". Network design under Directive
  2008/50/EC acts on annual means and exceedance counts per zone, not on station-day accuracy (practitioner,
  finding 5).
- Effect: the benchmark claims a second decision its target and metric do not score.
- Remedy: drop "and identify areas needing monitoring"; lead with daily exposure reconstruction and gap-filling.

**3. The label is called one agency's daily mean; the values point to two pipelines (USE-5, Must; EV-7, Must)**

- Problem: comments bullet 4 says "ARPA" in the singular. Station IDs come in two forms: Veneto province codes (PD04,
  VI04, RO03, VE03, ARPAV) and `X…` sensor IDs (ARPA Lombardia). In the README sample, PD04 is an integer (16), the
  `X` stations carry decimals; the ten most frequent targets are integers; the maximum 188.2333333 fits a mean of
  one-decimal hourly values (claim auditor N2, practitioner finding 3; both NEW, unmeasured).
- Effect: likely small (rounding costs at most about 0.29 RMSE against about 10), but the daily-validity rules of the
  two agencies are undocumented, and the notes state one source.
- Remedy: when the archive is on NFS, measure the share of integer targets by ID prefix. Until then, bullet 4 names
  both agencies and says the daily rule may differ between them. Do not state the single-agency reading as checked
  (EV-7).

**4. No `Retrospective` tag and no `Time basis:` line (SPLIT-32, Should; SPLIT-36, Should)**

- Problem: the tree leaf is Grouped · `Retrospective` (whole units). Both v0.2 definitions in that leaf carry the
  tag and the line (5g_energy_consumption; fraud_detection_in_electricity_and_gas_consumption_1m). geoai has
  `("Spatial",)` only. Nobody chose this; PR #59 predates the split rules (precedent checker, finding 1, NEW).
- Effect: the same-time check (other stations' same-day readings are the use, not a leak; nearest pair 7 km,
  r = 0.968, copying a neighbour gains only 0.008 per the 11-05 gamer) is in prose but not where the validator reads it.
- Remedy: precedent checker's option (a): add `Retrospective` and the sketched `Time basis:` line. The checksum moves,
  so this needs a rebuild, which needs the curator-supplied archive on NFS.

**5. Unequal stations, and the notes do not say how far one vote per station moves the ranking (MET-17, Should)**

- Problem: per-row scoring is right (each station-day is its own estimate on a daily map). But stations range from 298
  to 1,093 labelled days. MET-17 then asks the notes for how unequal the units are (bullet 3 has it) and how far one
  vote per unit moves the ranking (missing) (claim auditor N1, NEW).
- Effect: small; only about two stations are short.
- Remedy: no metric change. Once the data is on NFS, score two or three models per row and with 1/n_station weights
  over the nine folds, report Kendall tau, add one sentence to the metric bullet.

**6. Known inputs and the processor change are not written down (USE-3, Must; quality)**

- Problem: `known` says "for that day". The six satellite columns are one early-afternoon Sentinel-5P overpass;
  NO2_trop uses QA >= 0.75 (40.7% missing) against QA >= 0.5 for the rest (14.8%). The TROPOMI NO2 processor changes
  inside the period (v1.4 Dec 2020, v2.2 Jul 2021), a likely step in level and missingness. LST is said to be "NOAA"
  but sits on a 0.02 K grid, the MODIS scaling (column audit 11-21, claim auditor claim 25).
- Effect: none on the split (grouped, all dates shared); a reader cannot tell when an input exists or why NO2_trop is
  missing more often.
- Remedy: the column audit's `known` text; one comments bullet on the QA thresholds and the processor change; the LST
  product confirmed against DataDescription.pdf before it is named. No data change.

**What I do not argue**

- No exclusion: every point is a note, a wording fix or a tag. Validity holds on all tested claims (claim auditor:
  nothing refuted).
- Keep RMSE, the whole-station split, the inputs and the cleaning. A spatial-block split or added covariates would be
  our own task (practitioner; minimal preprocessing).

**Order of work**

Points 1, 2, 3 (wording part) and 6 need no measurement and can be written now. Points 3 (measurement), 4 and 5
need the archive on NFS. Every one of them edits the definition's metadata, so the shipped container moves only with
one rebuild from the curator-supplied archive. Until then the record should say the 11-21 round verified nothing on
the data (EV-7).

</details>

<details><summary>Critic rebuttal (2026-11-21)</summary>

**Critic rebuttal: geoai, 2026-11-21**

We agree on the verdict: ship after text and metadata fixes, no change to rows, target, inputs, split or metric. Two
differences remain: one fix the advocate leaves out (the `known` text and the processor note), and how the
two-agency label is written down while it is unmeasured.

| Advocate point | Reply | Why |
|---|---|---|
| 1. Source task, source metric, tree leaf | Concede | Claim audit 11-21 claims 1, 15, 21; the precedent check walks the tree to this leaf. I never disputed the split or RMSE. |
| 2. Same-day labels at other stations are the use | Concede | The 11-05 gamer numbers (copying the nearest station 12.47 against 10.37, worse on 9/9 folds; the closest pair has equal labels on 0.094% of days) settle SPLIT-32 question 2. My point 4 asks only that this reading go into the `Time basis:` line. |
| 3. Signal beyond place and date, models spread | Concede | Coordinates and date alone give 11.40, all inputs 10.26. Ridge to LightGBM spans 0.24 R². I never argued `Trivial` or `No Signal`. |
| 4. Inputs known at the retrospective point; processor change is a fit note | Concede the substance; dispute the remedy | The advocate calls the processor change "a fit note" but lists no fix that writes it. The definition does not mention it, and `known` still says only "for that day". USE-3 (Must) asks that the prediction point say what is known and when. The column audit's `known` text and one comments bullet (one early-afternoon overpass, QA thresholds for NO2_trop of 0.75 against 0.5 for the rest, processor v1.4 in Dec 2020 and v2.2 in Jul 2021) belong in the same edit as the others. My point 6 stands as a wording fix. |
| 5. Label limits real, small, already accepted | Concede in part | Myunghwan accepted the undocumented daily aggregation and QC (issue 1). He did not accept a single-agency statement: comments bullet 4 says "ARPA" in the singular, and that is an unchecked claim of its own (EV-7, Must). We agree on the remedy: name both agencies now, and measure the share of integer targets by ID prefix later. The siting mechanism and "satellite-only by design" go into `fit_reason`. We agree there too. |
| 6. Time basis, MET-17 note, use-case wording | Concede | Same remedies as my points 2, 4 and 5. |
| 7. Access and missing data are no verdict reasons | Concede, with one condition | EV-4 makes the login-only download a note, not a verdict. The 11-05 evidence matched the current rows and folds. The condition: the record's 11-21 entry must say that this round re-measured nothing and which items wait for the archive (N1, N2, the second station at about 72% missing, the column-audit leftovers), so no later reader takes them as checked (EV-7). |

**No new points**

**Joint list for the mediator**

- **Wording (no measurement):**
  - `fit_reason`: the siting mechanism, satellite-only by design, and the input latency.
  - `use_case`: drop "identify areas needing monitoring".
  - `known`: the column audit's text.
  - A comments bullet on the QA thresholds and the processor change.
  - Bullet 4: name both ARPAs.
- **Metadata:** the `Retrospective` tag and a `Time basis:` line.
- **When the archive is on this machine:**
  - The integer share by ID prefix.
  - The Kendall tau with one vote per station, and its sentence.
  - The LST product, checked against DataDescription.pdf.
- **One rebuild covers all of these.** Until then, the record states what this round could not verify.

</details>

<details><summary>Claim audit (2026-11-21)</summary>

**Claim audit: geoai (geoai_ground_level_no2_estimation_challenge), 2026-11-21**

**What I could test**

- The data is not on this machine. I searched once more for a public copy of `Train.csv` (web search on its column
  names `GT_NO2` and `NO2_trop`, for GitHub, Kaggle and Hugging Face). I found none. A direct call to the Zindi API was
  blocked by the session's permission policy, so I did not try it again.
- I tested what I could against four things: the README's built summaries (build `01a1ae48`, checksum `v2:79bbb806…`,
  the same as the current definition according to the record), the Zindi challenge page and data page (both read
  2026-11-21 on zindi.world), the Google Earth Engine catalogue page for Sentinel-5P OFFL L3 NO2, and the file sizes
  on the Zindi data page.
- Probe outputs: there is no check.log, README_check.md, leak/, task/, dtype/ or group.log in
  the run folder. Only `precedent/register.json` and the
  other agents' reports are there. Nothing ran this round because there is no data.
- Earlier data-backed evidence in the record (the 2026-11-05 claim audit, column audit and task gamer, run on the
  curator-supplied archive) is reused only where I cross-checked it for consistency. I did not re-measure it.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Question: estimate daily NO2 at a station held out of training | task_summary.question; grouping.definition | Read the challenge page | Holds | Jury scores "in-situ data from selected ground stations not provided to participants"; "ground truth data used for evaluation are independent from the training data set" | USE-1, SPLIT-1 |
| 2 | Use case: an analyst maps exposure at unmonitored locations, retrospectively; the actor is our interpretation | task_summary.use_case; comments bullet 1 | Read the challenge page | Holds as an interpretation | The page states the goal ("estimate surface NO2 … using only public remote sensing data") but names no actor. The record labels the actor as inferred. | USE-1, USE-8 |
| 3 | Row: 79 northern Italian stations, 2019-2021, 82,051 rows | task_summary.row | README: n_rows, n_groups, LAT/LON ranges, Date n_unique | Holds | 82,051 rows; 79 groups; LAT 44.92–45.89, LON 8.74–12.59 (Lombardy/Veneto); 1,096 dates = 365+366+365 | EV-1 |
| 4 | 86,584 raw = 79 × 1,096; 4,533 missing targets dropped | comments bullet 3 | Arithmetic | Holds (arithmetic only) | 79 × 1,096 = 86,584; 86,584 − 4,533 = 82,051. Also 10,000,397 B / 86,584 rows = 115.5 B/row, a plausible CSV row | CLEAN-15 |
| 5 | Coverage 298–1,093 days per station; two stations lack about 72% | comments bullet 3 | README group table | Partly holds | min 298, max 1,093. 298/1,096 = 27.2% labelled, so 72.8% missing for one station. The second station is not visible in the summaries. | USE-8 |
| 6 | Seven zero targets; maximum 188.2333333 kept | comments bullet 3 | README target table | Consistent | non_positive_pct 0.01 (7/82,051 = 0.0085%, which rounds to 0.01); max 188.233 | CLEAN-11/15 |
| 7 | Target is ARPA daily ground NO2 in µg/m³ | comments bullet 4; task_summary.predicted | DataDescription.pdf is not on this machine; checked the README values | Untested here (earlier audit read the PDF) | Values 0–188, mean 24.5, in the normal range for daily NO2 in the Po valley in µg/m³ | USE-5 |
| 8 | Satellite NO2 columns are column densities in mol/m², not the surface quantity | comments bullet 4 | GEE catalogue page | Holds | GEE: the NO2 bands are in mol/m²; README values about 1e-4 | LEAK-2 |
| 9 | Daily aggregation and QC of the labels are not supplied | comments bullet 4; fit_reason | Read the data page | Holds; see finding N2 | The page gives no aggregation. The value pattern points to two pipelines (finding N2). | EV-7 |
| 10 | Dates are day-first with mixed separators, 2019-01-01 to 2021-12-31; Test.csv is month-first | comments bullet 5; `_clean` | Code read; README Date n_unique 1,096 | Holds for train (code + count). Test.csv date format untested here | `_clean` parses `%d/%m/%y` and `%d-%m-%y` separately and asserts unique (ID, Date) | CLEAN-12 |
| 11 | ID is group-only; ID_Zindi is dropped; two ID_Zindi values repeat | comments bullet 6 | README: n_features 11 = 10 numeric inputs + Date; ID is the group column | First two hold; the repeat is untested here | dtypes: 1 category (ID), 1 datetime, 11 float64 (incl. target), so 11 features without ID | CLEAN-3 |
| 12 | All 8 physical predictors + LAT, LON, Date are kept; inputs are not imputed | comments bullet 7 | README feature summary | Holds | 8 physical columns + 3 = 11. Missingness preserved: LST 45.8%, NO2_trop 40.7%, five columns at 14.77% (12,118) | CLEAN-2 |
| 13 | Negative NO2 retrievals are ordinary noise; none below −0.001 mol/m²; cloud fraction exceeds 1 by 4.4e-8 | comments bullet 8 | GEE page; README minima | Holds | GEE: "negative vertical column values are often observed … not to filter … except … lower than -0.001 mol/m^2". README min NO2_total −1.19e-5, NO2_trop −2.53e-5. CloudFraction max prints as 1 (the 4.4e-8 comes from the earlier column audit) | CLEAN-11 |
| 14 | NO2_trop has more missing values because of a stricter QA filter | column audit 11-21 (not in the definition) | GEE page | Consistent | GEE: QA 75% for the tropospheric band, 50% for the others; 40.7% vs 14.8% missing | EV-2 |
| 15 | Leaderboard metric is RMSE on the original scale; correlation and MAE are jury metrics only | comments bullet 9; `Metric.source("rmse", original=…, reference=page)` | Read the evaluation section | Holds | "The evaluation metric for this competition is Root Mean Squared Error"; no transform; public 20% / private 80% of test rows. Jury: "Pearson correlation (r), Root Mean Square Error (RMSE) and Mean Absolute Error (MAE)" | MET-1, MET-3, MET-4, MET-11 |
| 16 | RMSE is computable per row on every fold; no scoring columns needed | README task block | README: scoring_columns null; 26,637–27,875 test rows and 26–27 stations per fold; target variance 292.7 | Holds (earlier audit's dummy RMSE 15.94–19.02 per fold, consistent with sd 17.1) | Unit = station-day, which exists; RMSE needs no extra input | MET-2 |
| 17 | RMSE means the same here as in the source | implied | Compare tasks | Holds | Same target, same scale and same regime (unseen stations, same period). Our test folds have 26–27 stations against the source's 6 | MET-2 |
| 18 | Score per row with no unit weight, while stations differ in size (298 vs about 1,068 rows) | implied by comments bullet 9 and the 298–1,093 coverage | Read MET-17 | Per-row holds (each station-day is a decision on its own map). The note MET-17 then asks for is missing; see finding N1 | Notes give the inequality but not how far one vote per station moves the ranking | MET-17 |
| 19 | The six Zindi test stations cover the same 2019-2021 dates; overlapping dates are as in the source | comments bullet 10; splits_comment | File-size arithmetic from the data page | Consistent (indirect) | Test.csv 705.1 KB / (6 × 1,096 = 6,576) = 107 B/row against 115.5 B/row for train with target. SampleSubmission 83.5 KB / 6,576 = 12.7 B/row, about one `ID_xxxxxx,value` line. Both fit 6 stations × the full period | SPLIT-1, EV-1 |
| 20 | Each station has a unique coordinate pair | grouping.definition | README n_unique | Holds | LAT 79 unique, LON 79 unique, ID 79 | SPLIT-24 |
| 21 | Split: whole stations held out across all dates; does not measure forecasting or extrapolation | task_summary.split; splits_comment | README split block | Holds | grouped_non_iid on ID, 3×3, 26–27 test groups per fold. The scope sentence is honest | SPLIT-1/3 |
| 22 | Known at prediction time: location, date and that day's products | task_summary.known | GEE page; column audit 11-21 | Holds for the declared retrospective point. Wording gap is KNOWN | Inputs arrive days (S5P) to about 7 weeks (CHIRPS final) after the day; the use case is retrospective | USE-3, LEAK-10 |
| 23 | Fit approximate: latency and label QC not established | fit_reason | Read the sources | Holds | Neither page gives latency or QC | USE-8, EV-7 |
| 24 | Licence CC BY-SA 4.0; year 2024; host ITU AI for Good | sources | Challenge page | Holds | "under a CC-BY SA 4.0 license"; 22 May–15 Nov 2024 (the timeline text says 11 Nov); "AI for Good is organized by ITU" | PROV-8/9/10 |
| 25 | Precipitation is CHIRPS; LST is "NOAA" | record screening; data page | README LST values | CHIRPS holds. For LST, the values sit on a 0.02 K grid (KNOWN, column audit) | 13 of 13 LST values shown in the README are even hundredths (chance on a 0.01 grid: 0.5^13 = 1e-4). That is the MODIS MOD11A1 scale factor; the source page says "NOAA". No definition text names the LST product, so no shipped claim is refuted | PROV-2 |
| 26 | Earlier model evidence: LightGBM about 10.26–10.37 RMSE; group-probe R² 0.634 | Assessments 10-30 and 11-05 | Consistency: sqrt(292.7 × (1 − 0.634)) | Consistent | 10.35, inside the reported 10.26–10.37 | EV-8 |
| 27 | No row copies across the split; near stations are signal, not copies | implied; gamer 11-05 | Not re-testable | Untested here (KNOWN, gamer: 0 exact copies; nearest pair 7 km, r = 0.968; copying a neighbour within 1 km gains only 0.008) | — | LEAK-16 |
| 28 | Priority 3, risk 0, gap 0 | Assessments | Judgement | No refuting evidence | — | — |
| 29 | Accepted warnings: none; 27 checks pass | accepted_check_warnings = {}; README | README bundle_checks | Holds for the last build. No check ran this round (no data) | ok: true, 0 errors and 0 warnings | EV-3 |

**Findings (none refuted; two NEW, both minor)**

**N1 (NEW, Should, MET-17): the notes do not say how far one vote per station moves the ranking.**
- The score stays per row correctly: each station-day is its own estimate on a daily map.
- Stations are unequal: one has 298 rows, against a median of 1,068. MET-17 then asks the notes to say how unequal
  the units are (bullet 3 does) and how far one vote per unit moves the ranking. The second part is missing.
- Expected effect is small: only about two of the 79 stations are short.
- Mildest remedy: once the data is on NFS, score the nine folds of two or three models per row and with station
  weights 1/n_station, report Kendall tau, and add one sentence to the metric bullet. No change to the metric.

**N2 (NEW, low, EV-7 / USE-5): the target probably comes from two agencies with different precision and daily rules.**
- Station IDs have two forms: Veneto province codes (PD04, VI04, RO03, VE03) and numeric `X…` sensor IDs (the ARPA
  Lombardia style).
- In the README sample rows, PD04 is an integer (16). The `X` stations carry decimals (53.2, 8.3, 26.55, 17.3).
  The maximum 188.2333333 is 45,176/240, which fits a mean of hourly 0.1-precision values with a varying number of
  valid hours.
- The ten most frequent target values are all integers (12, 13, 11, …).
- Comments bullet 4 says "ARPA" in the singular. There are two ARPAs (Lombardia and Veneto) with their own
  daily-validity rules.
- Rounding alone costs at most about 0.29 RMSE, so this is not a validity problem. It refines the accepted
  "aggregation not supplied" limit.
- Remedy: measure, then possibly name both agencies in bullet 4. No data change.

**Untested, with what to measure (when the archive is on NFS)**

| Claim | Measure |
|---|---|
| 5 (second station at about 72% missing) | Labelled days per ID, sorted; list the two smallest |
| 7 (ARPA, µg/m³) and LST product | Text of DataDescription.pdf Table 1: agency per region, LST collection ID |
| 10 (Test.csv month-first and dates) | Parse Test.csv Date; min/max; rows per test station (expect 6 × 1,096) |
| 11 (two ID_Zindi repeats) | `raw.ID_Zindi.duplicated().sum()`; check that no (ID, Date) repeats |
| 13 (cloud fraction 1 + 4.4e-8) | `CloudFraction.max() - 1` |
| 16 (dummy RMSE per fold) | Score the train-mean prediction with `data_foundry.v2.metrics.scorer` on all 9 folds |
| N1 | Per-row vs 1/n_station weighted RMSE ranking, Kendall tau over 9 folds |
| N2 | Share of integer GT_NO2 by ID prefix (`X` vs province code); fractional parts × 24 and × 240; days per station with non-integer values |
| Column-audit leftovers | NO2_trop missing share and median by month (processor v1.4 Dec 2020, v2.2 Jul 2021); LST values mod 0.02; satellite missingness by GT quintile |

**Ranked**

- Nothing is refuted. Every validity claim I could test holds: the source task, unseen-station holdout, target,
  inputs, cleaning, metric and licence.
- N1 is a missing sentence (Should).
- N2 is a provenance refinement.
- Neither changes the data, the split or the metric.

Sources: [Zindi challenge](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge),
[Zindi data page](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge/data),
[GEE S5P OFFL L3 NO2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2).

</details>

<details><summary>Domain practitioner (2026-11-21)</summary>

**Domain practitioner: geoai_ground_level_no2_estimation_challenge (2026-11-21)**

Actor: an air-quality analyst at a regional agency or in an exposure-assessment team. I reconstruct daily ground NO2 at places with no monitor, after the fact. I worked from `dataset.py`, the generated README, the record (Comments, Review, the 2026-11-21 column audit) and the sources listed at the end. I had no data, so I ran nothing. The panel run folder has only `precedent/`. `check.log`, the probe outputs and `REVIEW.md` are missing, as is a 2026-11-21 Horizon or split-issue block in the record's `## Review`. Only the Assessment line of the split audit is there.

**Verdict**

| question | answer |
|---|---|
| Fit | **approximate** (agrees with `fit="approximate"`). The task is the standard station-held-out reconstruction of daily NO2. But the held-out points are monitoring sites, not the unmonitored places I map. And the inputs are the challenge's satellite-only set, not the set I would always use. |
| Metric scores my decision | **partly yes, keep RMSE** (MET-4). RMSE in µg/m3 per station-day is what my field reports first. I would also look at each station's mean error. That view complements RMSE and does not replace it. |
| Would I use the model | Yes, as a satellite-only gap-filling layer for daily background exposure. No, for traffic hotspots or for compliance at a site. |

**The five questions, as the analyst**

1. **Inputs at prediction time.** For retrospective mapping I have every input: the coordinates, the date, CHIRPS precipitation, LST and the Sentinel-5P columns of that day. The column audit gives the latencies: days for the satellite products, about seven weeks for final CHIRPS. I always have the same-day readings of the surrounding monitoring network too. The benchmark gives them only implicitly: training stations share the date, so a model can learn each day's regional level. That is how kriging works in my practice, and it fits `context="none"`. The inputs I would always have that are missing are meteorology (wind speed, boundary-layer height from ERA5) and static covariates (road density, land use, population, emission inventories). The challenge leaves them out on purpose ("only public remote sensing data"), so this is the source's design, not our cut.
2. **Target.** A daily mean concentration in µg/m3 is a quantity I act on directly. I use it for short-term exposure in epidemiology and for filling gaps in the daily record. A number is the right output (regression). For network planning I would act on annual means and exceedance counts instead (finding 5).
3. **Row and test.** One row is one station-day, and that matches one estimate on my daily map. Holding out whole stations over the same dates matches retrospective reconstruction: the same period, other places. That is the leave-stations-out validation the literature uses. The test points are monitoring sites, though, and monitoring sites are chosen (finding 1).
4. **Trust.** I trust the model more because its error is measured at unseen stations and because it uses the same-day network. Three things make me trust it less. A TROPOMI pixel is about 3.5 x 5.5 km and cannot see the street canyon a traffic station measures. Wind and mixing height are not inputs. The NO2 processor changes during 2020-2021 (column audit, KNOWN).
5. **Metric.** RMSE on the concentration scale is the challenge's leaderboard metric (MET-4). It is also the first number in this literature, next to R² and MAE. The EU FAIRMODE model quality objective is an RMSE scaled by measurement uncertainty. Pooled RMSE weights winter peaks and high stations most, and those are the exposures that matter. I see no MET-2 failure: the unit (station-day) exists, and no input is missing. I would not change it (MET-1, MET-4, MET-10). MET-6 to MET-9 do not apply: this is not a classification task.

**Findings (ranked by how much they change the task)**

| # | finding | evidence | rule | status |
|---|---|---|---|---|
| 1 | **Monitoring sites are not unmonitored locations.** Agencies classify stations as traffic, background or industrial, and urban, suburban or rural. Traffic stations sit at hotspots and read much higher NO2 than a background grid cell, and the satellite pixel cannot resolve that. Station type is missing, and so is any proxy for it (road distance, land use). So part of the target is site-siting variance that no input can explain, and the held-out stations over-represent hotspots compared with the places I map. The fit_reason says this only generally ("Monitoring-site coverage approximates unmonitored locations"). Naming the mechanism would make the gap concrete. Measurable without changing the task: the station IDs look like public agency codes (`X5958`-style ARPA Lombardia sensor IDs; `PD04`, `VI04`, `VE03`, `RO03` ARPAV Veneto codes). Joining their public station type and reporting RMSE by type would show how much of the error is siting. Not a reason to change the data. | README sample rows; agency station registries (not fetched) | USE-8 (approximate, named gap), USE-5 | NEW (mechanism); the general gap is KNOWN |
| 2 | **The practitioner's standard inputs are absent by the source's design.** Meteorology (boundary-layer height, wind) and static land-use or traffic covariates drive NO2 in every operational model I know, including the Lombardy work behind this challenge (Cedeno Jimenez et al. 2023 used ground meteorology and kriging; its stated next step was satellite-only inputs, which this challenge implements). So this is a satellite-only variant of my task. Adding covariates would be our own feature engineering, against minimal preprocessing. Keep the inputs as they are, and say "satellite-only by design" in fit_reason. | Zindi overview ("only public remote sensing data"); Cedeno Jimenez et al. 2023 | USE-8, USE-9 (no better-fitting use case found) | NEW (as a fit statement) |
| 3 | **Label construction may differ between the two agencies.** The maximum, 188.2333333, equals 4517.6/24: a 24-hour mean of hourly values with one decimal (Lombardy, decimal values). The Veneto sample row (`PD04`, 16) and the most frequent values (12, 13, 11, ...) are integers. So ARPAV daily means may be rounded to whole µg/m3. The hourly coverage rule for a valid daily mean (the EU's 75%) is not documented. The effect is small (rounding of at most ±0.5 against an RMSE near 10), but it is a regional difference in labels, and only the data can confirm it. To measure: the share of integer targets by ID prefix (`X*` against Veneto codes). | README sample and top values; arithmetic | USE-5, CLEAN (keep labels) | NEW (hypothesis); aggregation undocumented is KNOWN (issue 1, resolved) |
| 4 | **Random station folds test interpolation inside the network.** Stations cluster around Milan, the Po plain cities and the Veneto cities. Many held-out stations have a close neighbour in training, which is easier than mapping a rural gap far from any station. This matches the challenge, and the notes already disclaim geographic extrapolation. No change. | README (LAT 44.92-45.89, LON 8.74-12.59, 79 stations); splits_comment | USE-8 | KNOWN |
| 5 | **"Identify areas needing monitoring" overstates the use case.** Network design under Directive 2008/50/EC rests on annual means and exceedances against assessment thresholds per zone, not on daily station-day accuracy. Daily estimates support it only after aggregation. The use case should lead with daily exposure reconstruction (short-term exposure, gap-filling of the daily record) and drop or soften the monitoring-design clause. Wording only. | task_summary.use_case | USE-1, USE-8 | NEW |
| 6 | Inputs arrive with a lag (satellite within days, final CHIRPS about seven weeks), and the NO2 processor changes in Dec 2020 and Jul 2021. I agree with the column audit's fit_reason and known rewrites. | column audit 2026-11-21 | USE-3, USE-8 | KNOWN |

**What an expert would change**

- Keep the task, the split and RMSE.
- Sharpen the use case (finding 5) and fit_reason (findings 1, 2 and 6): "satellite-only, monitoring sites stand in for unmonitored places, with traffic and background siting not represented".
- Measure findings 1 and 3 when the archive is on NFS. Neither changes the data unless the integer labels turn out to be a different aggregation, not just rounding.
- Do not add meteorology or land-use features, and do not move to a spatial-block split. The source defined this satellite-only, unseen-station question, and a random station split is the field's standard validation.

**Sources**

- Zindi challenge page: https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge (objective "only public remote sensing data", RMSE leaderboard, Pearson r and MAE for the jury, evaluation stations "not provided to participants")
- Cedeno Jimenez, Pugliese Viloria, Brovelli (2023), "Estimating Daily NO2 Ground Level Concentrations Using Sentinel-5P and Ground Sensor Meteorological Measurements", IJGI 12, 107: https://doaj.org/article/15234d30ec4c4ecf9c1cf2c3c386adb8
- Fania et al. (2024), Remote Sensing 16, 1206 (Sentinel-5P + ERA5, ARPA ground truth, Italy): https://mdpi.com/2072-4292/16/7/1206
- Apulia daily NO2 XGBoost preprint (meteorology and land-use as main drivers): https://www.preprints.org/frontend/manuscript/d31308a3b6061236ef9712be12f81219/download_pub
- EGU25-16433 (Italy-wide daily NO2 maps from 300+ stations with ERA5-Land): https://meetingorganizer.copernicus.org/EGU25/EGU25-16433.html
- Domain background (station classification, the 75% data-coverage rule, FAIRMODE MQO, Directive 2008/50/EC) from my own knowledge; not fetched this session.
- Repo: `datasets/_dev/tabarena-v0pt2/geoai_ground_level_no2_estimation_challenge/dataset.py` and `README.md`, `curation/records/geoai_ground_level_no2_estimation_challenge.md`, the run folder, `use_case.md`, `metrics.md`.

</details>

<details><summary>Precedent check (2026-11-21)</summary>

**Precedent check: geoai_ground_level_no2_estimation_challenge (2026-11-21)**

**What I checked**

- Decision register run on the login node (2 threads): 43 flags; none names geoai or a `Retrospective` panel. Output:
  the run folder.
- Definition: `datasets/_dev/tabarena-v0pt2/geoai_ground_level_no2_estimation_challenge/dataset.py`. Record: CC lines of
  2026-10-30 and 2026-11-05, issue 1 (resolved), Assessment of 2026-11-21.
- The record has **no 2026-11-21 issues and no Horizon block**. The only output of this round's split audit is the
  Assessment line that sets the facts. There are no check or probe logs for geoai under `pr59_panel/` (no data on NFS),
  so I read none.
- Precedents: the split tree's Panel data branch (`split_tree.md`). The leaf's examples, `5g_energy_consumption` and
  `fraud_detection_in_electricity_and_gas_consumption_1m`, read from `origin/splits/basis-panel`, because the split PRs
  for the dataset groups are not merged into this worktree. Also the Zindi Sentinel-5P sibling
  `airqo_african_air_quality_prediction_challenge`, `airqo_low_cost_air_quality_monitor_calibration_challenge`, and
  SPLIT-32 question 2 in `splits.md`.

**Walking the tree**

- Panel data, then "fill in the covered period". The use case maps unmonitored places within 2019-2021, and the
  challenge's test stations cover the same dates.
- Labels-arrive-later step ④: no. The Assessment of 11-21 says the reading arrives with its day. The missing targets
  are monitor downtime, not a label delay.
- Whole units missing → **Grouped · `Retrospective` (whole units)**. The shipped split matches this leaf.

**Per decision**

| Decision | Verdict | Closest precedent | Facts compared |
|---|---|---|---|
| Group by station, all dates on one side, test dates overlap training (SPLIT-1/3/32/36) | Consistent | 5g_energy_consumption (Retrospective, whole stations in one logged week); fraud_detection_in_electricity_and_gas_consumption_1m | Same leaf. Fill-in of units the network does not measure, over the covered period |
| Other stations' same-day labels in training; `context="none"` (SPLIT-32 q2: "no sample of a test sample's time carries its target") | Consistent in substance | 5g's `Time basis:` line: "while the other stations of the same hours are measured" | Same reading of the check: the other units at the same time are the use, not a leak. The 11-05 gamer found same-day neighbour blends gain only modestly and found no identical labels. So no row of the test day carries the target, and grouping by day is not called for. Not written down here (see finding 1) |
| `data_tags = ("Spatial",)`, no time basis, no `Time basis:` line (SPLIT-32, SPLIT-36) | **Departs, without a stated reason** | 5g: `("Retrospective",)` + line; fraud_detection: `("Spatial", "Retrospective")` + line | Same leaf, same kind of facts. The likely cause is that PR #59 predates the split work, not a curator's choice. **NEW**, finding 1 |
| Drop the 4,533 rows without a target, keep extremes and zeros (CLEAN-11/15) | Consistent | Issue 1, resolved 2026-10-30 (Myunghwan) | Unchanged |
| Date, latitude and longitude as inputs (time-column actor test) | Consistent | 5g keeps day and hour as features | The retrospective analyst holds the date and the place. Coordinates are unseen in test under the station split |
| Satellite and weather retrievals as tabular physical inputs (SEL-15) | Consistent | airqo_african CC 2026-11-05 (Myunghwan): S5P retrievals are physical measurements | Same curator, same product. airqo was deferred for 4 cities and unstable transfer. geoai has 79 stations, which sets it apart |
| Source RMSE (MET-4) | Consistent | 5g, airqo_african: Zindi RMSE | Unchanged |
| `required_split: Grouped`; facts Panel Data, Samples Over Time, Time Dated, Entities Recur, no Target fact | Consistent | `test_collection_types`: Panel Data needs a recorded occasion; Time: Dated satisfies it | Column audit 11-21 confirms the facts |
| Priority 3 | Consistent | 11-05 assessments | No new fact |

No drift by this curator. No third exception of a kind. The register flags (CLEAN-19 amendment, metric
exceptions, label maturity) concern other datasets and do not match these facts.

**Finding 1 (NEW): the definition does not name its time basis**

Should the definition carry `Retrospective` and a `Time basis:` line, like the other whole-unit fill-in panels?

- **Problem:**
  - The tree leaf is Grouped · `Retrospective` (whole units). Both v0.2 definitions under that leaf carry the tag and
    the line: 5g_energy_consumption `("Retrospective",)`, fraud_detection_in_electricity_and_gas_consumption_1m
    `("Spatial", "Retrospective")`. geoai has `("Spatial",)` only.
  - SPLIT-32 asks the line to name the time covered, the need, the same-time check ("no sample of a test sample's
    time carries its target"), and what the split cannot test. The `curation_comments` already hold all of that in
    prose: 2019-2021, unmonitored stations, other-station same-day data legitimate, no future-year or distant-region
    test. They just lack the tag and the line.
  - The likely cause is timing: PR #59 was written before the split rules. Nobody chose to depart.

| | Option | Pro | Con |
|---|---|---|---|
| a | Add `Retrospective` to `data_tags` and a `Time basis:` line (sketch below) | Matches 5g and fraud_detection. The time-basis validator then checks it | Changes the metadata, so the checksum moves. Needs a rebuild |
| b | Keep as is and write in `splits_comment` why no time basis is named | No rebuild | Leaves an unexplained departure from both leaf precedents |

Sketch for (a): "Time basis: Retrospective: 79 ARPA stations read daily, 2019-01-01 to 2021-12-31. The reading
arrives with its day, and the use case fills in places without a monitor over that period, while the other stations of
the same days are measured. Nearby stations correlate but no other station's same-day reading equals the target, so
days are not grouped. Not tested: a later year, or a station outside Lombardy and Veneto."

**Recommendation:** a.

Rule IDs: SPLIT-32 (time basis and its line, same-time check), SPLIT-36 (leaf decides, departures named).

**Not tested**

- I could not measure the same-time check (whether a training station's same-day NO2 nearly equals a test station's).
  geoai's data is not on NFS. The verdict rests on the 11-05 gamer result recorded in the record.
- Whether the missing targets cluster late in time (step ④). I rely on the documentation that the reading arrives with
  its day. The two stations missing ~72% of their labels could not be inspected.

</details>

<details><summary>Column audit (2026-11-21)</summary>

**geoai column audit (2026-11-21) — no decision; docs only; data not obtained (Zindi login)**
- All 11 inputs known at the retrospective prediction point; no post-outcome, lag, whole-release-fitted column. No ERA5; precip = CHIRPS.
- Six satellite columns = one Sentinel-5P L3 NO2 overpass (GEE): NO2_trop QA>=0.75 (40.7% missing), others QA>=0.5 (14.8%, same 12,118 rows).
- Facts hold (Panel Data, Samples Over Time, Time Dated, Entities Recur, 2019-2021). No Features: Read Later.
- Caveat: TROPOMI NO2 processor v1.4 (Dec 2020), v2.2 (Jul 2021) inside the period — level/missingness step; not a split problem (grouped, all dates shared).
Doc fixes:
- task_summary.known -> "The location and date; that day's CHIRPS precipitation; daytime land-surface temperature, aerosol index, cloud fraction, satellite nitrogen dioxide columns and tropopause pressure from single early-afternoon satellite overpasses on that day."
- fit_reason 2nd sentence -> "Monitoring-site coverage approximates unmonitored locations. Inputs arrive within days (satellite) to about seven weeks (CHIRPS final precipitation) after the day, which suits retrospective mapping but not same-day use. The ground-truth daily quality-control procedure is not documented."
- curation_comments bullet on the S5P bands/QA, processor change, LST 0.02 K grid (MODIS/VIIRS scaling; source says NOAA) — confirm vs DataDescription.pdf.
To measure when archive on NFS: NO2_trop missing/median by month (DJF 19/20 vs 20/21); trop-missing superset of total-missing; LST multiples of 0.02; same-cell precip identical; satellite missing by GT quintile; DataDescription.pdf collection IDs.

</details>


<details><summary>Current checksum reconciliation</summary>

**Current checksum reconciliation:** The final clarified definition has checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. Two metadata changes explain it completely: the new empty `special_features` field and the added curation-comment clarification of existing row-only context. Before that clarification, current serialization gave `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`; the October artifact stored `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. The earlier audit/mediator paragraphs below describe their preclarification snapshot; the claim audit's final documentation follow-up establishes exact equality of the final data, dtypes, features, target, folds and scorer. No scientific transformation changed.

</details>

<details><summary>Mediator (2026-11-05)</summary>

**GeoAI focused refresh — independent mediator**

Date: 2026-11-05. Current upstream: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`.

**Judgment record**

**Recommendation: ship the scientifically unchanged, previously accepted definition after the current build and verification finish. No new curator decision is needed.** This is an agent recommendation, not a new curator judgment or build authorization. The curator accepted the implemented limitations on October 30 (“thse limits are fine”) and explicitly requested this refresh using the past decisions on November 5. That instruction supports reusing the recorded acceptance; it does not turn new agent findings into human approvals.

The prior complete panel remains historical evidence. This focused panel addresses changes in upstream rules and serialization and tests whether those changes or fresh evidence undermine that accepted task. I read the current principles, applicable task/metric/cleaning and grouping guidance, focused review-panel contract, definition and REVIEW, claim-auditor, column-auditor, precedent-checker, and the participant task-gamer report. I assessed their evidence and inspected the context contract; I did not independently rerun every reported fit.

- **Validity:** the retained 82,051 labeled station-days, target, 11 model features, dtypes, missingness, and all nine whole-station fold assignments match the accepted version. Independent raw comparisons support the reconstruction. Complete training archives from other stations, including observations later than a particular query day, are intentional for retrospective spatial estimation. This is not an advance forecast or a claim of distant-region transfer.
- **Value:** fresh gamer results show useful, legitimate spatial and calendar signal. A calendar model improves mean RMSE from 10.3701 to 10.0299 across the nine existing folds. Same-day training-station target blends also improve performance modestly. Neither is evidence that the evaluation leaks held-out station labels. The completed historical grouped learnability results and the fresh split-gap result support retaining the station split. They do not establish broad operational deployment performance.
- **Quality:** the minimal reconstruction remains appropriate. Dropping missing targets, parsing Date and excluding row/station identifiers from model inputs have clear roles. No evidence justifies imputation, target transformations, station exclusions, new engineered columns, or altered folds. The column audit found no newly applicable ordinal/categorical recoding requirement.
- **Uncertainty:** the actor interpretation is approximate; source QC, daily aggregation details, product timing/versioning and regional station representativeness remain incompletely established. The source archive was not freshly authenticated and redownloaded. These are preserved limits, not newly verified facts. The curator already accepted this scope.

**Findings resolved by this review**

**Updated rules and checksum**

The new metric guidance permits justified case-specific metric choices; it does not require replacing the original RMSE here. Ground-level NO2 has a meaningful physical scale, and the source competition RMSE is consistent with this accepted task. No measured pathology in the current evidence requires a new metric decision. The precedent check identifies no GeoAI-specific adverse collection decision or new selection rule that changes this conclusion.

The checksum changed because current serialization emits `special_features: []`, which the historical metadata omitted. The claim audit reproduced the historical checksum by removing that one newly serialized empty field, and compared the actual tables and folds. Treat the old UUID and its verification as historical, and build/verify a new artifact with current code. Do not describe old serialized checksum compatibility as unchanged.

**Raw target autocorrelation**

The raw table is date-major, not station-major: each date has the 79 stations and adjacent rows never share a station. The target autocorrelation warning is therefore consistent with same-day cross-station signal. Whole-station splitting addresses station memorization. This raw-order flag alone does not justify temporal folds, row reordering as a scientific fix, or dropping observations.

**Participant context and gamer evidence**

The schema defines `Grouping.context='none'` as **the row only**, and the maintained definition guidance says each row stands alone. For a held-out station, this excludes borrowing its other unlabeled rows for group-level summaries or forward filling. It does not restrict the complete labeled training archive at other stations. A query's own Date, coordinates and supplied daily atmospheric/weather measurements remain available.

Accordingly, training-station same-day averages and nearest-training-station target blends are legitimate modeling strategies under the accepted retrospective task. No exact full-feature cross-fold copies were found. The very correlated nearby station pair does not have identical labels and is evidence of spatial dependence, not a demonstrated duplicate entity.

The gamer's `test_archive_stats` and `archive_ffill` variants require additional rows from the held-out station and are outside the row-only contract. Both worsened RMSE in these tests. Their inclusion in the probe is useful for identifying wording ambiguity, not grounds to broaden the declared context or to add those transformations. The participant kit's original broader archive wording should be preserved as historical probe input, accompanied by an explicit correction. The parent reports adding the clarification to curation comments and REVIEW and recording it in `participant-contract-clarification.md`, without changing features, folds or the context enum. That is the appropriate repair and clarifies the existing contract rather than introducing a new scientific task.

The gamer explored a finite collection of one-seed model variants and public suggestions, not all possible attacks or modeling approaches. Selecting improvements on these same folds gives optimistic estimates of the selected gains. Public write-up approximations are not exact reproductions of unpublished competition pipelines, and coefficients tuned to withheld labels are not legitimized by this review.

**Completion conditions and repairs**

1. Preserve the October 30 human decision and mark this as a November 5 refresh under the explicit reuse instruction. Do not reopen issue 1 or create a fictitious new curator response.
2. Keep the row-only held-out-station clarification in the definition notes and REVIEW; preserve the original gamer kit and its provenance with the separate clarification. This repair is reported applied by the parent.
3. Distinguish fresh checks from retained historical evidence. Fresh checks reported 27 passes and zero warnings; the full suite reports 2,016 passes and 286 skips. Existing repository-wide lint/format failures are baseline findings, not GeoAI regressions.
4. At this report's completion, the current group rerun has produced IID R² 0.788 ± 0.001 versus grouped R² 0.636 ± 0.042 (gap 0.152), but the remaining learnability section is still running. The historical full run remains available, and old/current group feature matrices were verified identical. Record the eventual fresh result or explicitly retain the prior result as historical; do not label unfinished work complete. Full-frame median imputation in this diagnostic limits its quantitative interpretation and does not alter the stored definition.
5. Complete the newly authorized current-code build and artifact verification and record its new UUID/checksum. This mechanical completion is distinct from the scientific ship recommendation.

**New curator questions: none.** A future change to permit all held-out-station rows, change the target/metric/split, broaden operational claims, or introduce target-derived feature construction would require its own explicit scientific review. This refresh does not make any of those changes.

</details>

<details><summary>Claim and split audit (2026-11-05)</summary>

**GeoAI focused claim and split audit, 2026-11-05**

Verdict: ship as previously accepted, subject to the remaining current-cycle probes and reviewer synthesis. This audit found no new scientific choice for Myunghwan. Validity: the source task, retained values, retrospective prediction point, group identity and all nine folds remain consistent with USE-1/8, SPLIT-1/3/23/24 and PROV-1/8. Value: source RMSE remains appropriate and computable on every fold (MET-1/2/3/4/11); previously measured nontrivial signal remains applicable under verified identical inputs. Quality: unchanged source values and missingness, exact date restoration and missing-target removal satisfy CLEAN-2/12/15. The already accepted regional, label-processing and observed-day coverage limits remain explicit rather than upgraded to verified facts.

The audit independently ran `claim_audit_current.py` against the current-main checkout at `9048f36a` and the accepted format-2 container `01a18eeb-f85e-72fe-90a9-e5ae0e7817e7`. Its results are in `claim-audit-current.json`; `checksum-cause.json` isolates the schema-related checksum change and `evidence-reuse.json` records a reproduced model check. No definition or curation record was edited.

**Decisive comparison**

All 82,051 rows, thirteen stored columns, column order, dtypes, category metadata, target values, input missingness and eleven model inputs are exactly equal to the accepted container. Every train/test index in all nine folds is equal. The three metadata objects are equal after loading through the current schema. Independent normalized-separator parsing and key-based comparison also reproduce every retained source value. The current bundle check ran 27 checks with zero errors or warnings.

The checksum changes solely because the current schema serializes the new empty `task_metadata.special_features: []` field. The saved October task JSON omitted it. Recomputing the old container with the current reader gives the new checksum `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`. Removing only that empty list from the canonical encoding recovers the old stored checksum `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. This is a schema compatibility difference, not a changed scientific dataset. Preserve the old artifact and its old-runtime verification evidence; the requested current-code build must establish a new UUID and checksum.

**Claims tested**

| Claim and source within the definition/record | Refutation test | Result and evidence | Rule |
|---|---|---|---|
| Question/use case: estimate daily surface NO2 at stations absent from training | Reopen official challenge and test fold station intersections | Holds; source describes withheld-station estimation; zero shared stations on all nine folds. Analyst/exposure-mapping role is explicitly an interpretation. | USE-1, SPLIT-1 |
| Row: 82,051 station-days, 79 stations, 2019–2021 | Count source rows, target availability, groups and independently parsed dates | Holds: 86,584 raw, 4,533 missing targets, 82,051 retained, 79 groups, 1,096 dates per raw station. | CLEAN-15, EV-1 |
| Target: daily ground NO2, micrograms per cubic metre | Read preserved original codebook Table 1 and compare target values exactly | Holds: codebook identifies ARPA and daily ground-level measurements; every retained target equals raw. | USE-5, MET-3 |
| Known inputs: date, coordinates and eight physical predictors | Compare model input API and original codebook | Holds: exactly eleven inputs; no group ID or target among features. Physical satellite column densities are distinct from the surface concentration. | LEAK-2, CLEAN-22 |
| Inputs and training archive are available at the prediction point | Read declared retrospective point and original source metadata | Supported only for the declared retrospective after-products-available point. Exact publication latency remains unverified; no claim of real-time availability is made. | USE-3/8, LEAK-1/10, EV-7 |
| Train/test dates overlap, but stations and coordinates do not | Check each exact shipped split | Holds: 1,096 shared dates, zero station overlap and zero coordinate overlap in all nine folds. | SPLIT-1/3/24 |
| Preparation only omits missing targets, removes ID_Zindi and restores Date | Independently normalize date separators and compare raw/prepared frames keyed by ID/date | Holds exactly for every retained value and NaN. | CLEAN-2/12/15 |
| Approximate fit acknowledges monitoring-site coverage and undocumented label processing | Read original codebook, current task description and accepted record | Holds as a limitation; representativeness and daily QC are not proven. Existing acceptance does not claim otherwise. | USE-8, EV-7 |
| Labeled coverage is 298–1,093 days and two stations lose about 72% | Fresh per-station counts; reuse exact-identical source audit for per-station breakdown | Holds. Scores concern observed labels, not missing-monitor days. | USE-8, CLEAN-15 |
| Seven zero targets and maximum 188.2333333 are retained | Count prepared values and compare all source values | Holds: seven zeros; exact maximum retained. No new proof of invalid measurements. | CLEAN-11/15 |
| Atmospheric columns and station target are different quantities | Read original codebook units/source rows | Holds: TROPOMI mol/m² versus ARPA micrograms/m³. No direct target-copy relationship is asserted. | USE-5, LEAK-2 |
| Daily aggregation/QC details were not supplied | Inspect original one-page codebook and historical source audit | Still cannot verify actual procedure; the codebook gives resolution and units, not its construction algorithm. | EV-7, PROV-2 |
| Raw training calendar is complete and day-first | Independent parse after normalizing slash/dash separators; within-ID day differences | Holds: 1,096 dates/station and one-day raw gaps. Cleaned labeled calendars have missing days, correctly distinguished. | CLEAN-12 |
| Test dates are month-first and Test.csv is excluded | Independently parse Test; inspect loader and compare exact retained data | Holds. Test is preserved for evidence and contributes no rows to the container. | EV-1, CLEAN-12 |
| ID is group-only; ID_Zindi is removed | Feature list and frame-column inspection | Holds; only category is ID and it is excluded from model inputs. | CLEAN-3, SPLIT-24 |
| Two submission identifiers repeat without duplicate station-days | Count raw ID_Zindi duplicates and station/date duplicates | Holds: ID_LMYYAX and ID_ZHFIGQ recur; zero duplicate station/day keys. | LEAK-16, CLEAN-3 |
| No imputation, smoothing, neighboring-target construction or performance-based station filter | Full raw/prepared equality and code inspection | Holds; all 79 stations retained and raw input NaNs preserved. | CLEAN-2/6/7 |
| Small negative satellite retrievals and negligible cloud excess are retained | Exact equality to the old accepted data/raw; inspect prior primary-product audit | Unchanged. Prior primary documentation supports retaining ordinary negative retrieval noise; no new release or value change invalidates that evidence. | CLEAN-11, EV-2/8 |
| Leaderboard metric is RMSE, distinct from jury assessment | Reopen official evaluation page | Holds: current page explicitly names Root Mean Squared Error; jury also considers correlation and MAE. | MET-1/4/11 |
| RMSE scores original concentration per row, on every fold | Current scorer against direct square-root mean error and historical old-runtime results | Exact equality on all nine folds; dummy RMSE ranges 15.9425–19.0181. Every test fold has positive target variance. | MET-2/3 |
| Six competition test stations differ from the 79 training stations | Fresh Test.csv station and coordinate intersections | Holds: six test stations, zero overlapping IDs and coordinate pairs. | SPLIT-1, EV-1 |
| Groups are real stations with unique coordinates | Exact split overlaps and prior verified source identity; all values unchanged | Holds. The grouped protocol preserves all days for each station on one side. | SPLIT-23/24/26 |
| Splits are 3 repeats × 3 folds, without future-year or distant-region claims | Compare exact memberships with accepted artifact and read scope wording | Holds: 26–27 test stations, 26,637–27,875 test rows. | SPLIT-1/3, USE-8 |
| Empty accepted-warning set; current check passes | Read current check output | Holds: 27 checks, zero errors/warnings/infos. No semantic completeness is inferred from the check count. | EV-3/7 |
| Source/year/citation/licence identify the original challenge | Reopen official page and inspect corrected BibTeX | Holds: ITU-hosted 2024 challenge; ITU AI for Good attribution; CC BY-SA 4.0 stated. Earlier unsupported research-group attribution was already corrected. | PROV-8/9/10 |
| Download recipe identifies the exact accepted source | Fresh SHA-256 and inspect loader | Holds for preserved input: Train.csv SHA-256 fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446. Fresh authenticated redownload remains untested. | PROV-1, EV-7 |
| Earlier screening's temporal/image concerns remain unresolved | Compare dated screening hypothesis with original codebook, accepted definition and current measurements | Refuted as a current claim: those are preserved historical hypotheses, superseded by the accepted physical-measurement spatial task. | EV-2, SEL-15, SPLIT-1 |
| Related paper/sibling candidates establish exhaustive uniqueness | Inspect historical record and prior audit | Not established as exhaustive; historical related-work notes are not scientific evidence of every possible duplicate. No new duplicate evidence found in this focused task. | PROV-4/7/16, EV-7 |
| Accepted model results remain relevant to this dataset | Exact data/fold/scorer comparison, same library versions and fresh one-fold rerun | Holds as historical results under unchanged conditions, with original diagnostic limitations retained. See next section. | EV-8 |

**Reuse of runtime evidence**

The environment remains pandas 3.1.0, numpy 2.5.4, scikit-learn 1.7.2 and LightGBM 4.6.0. The prior fold-safe supplement uses deterministic Date-to-integer-days conversion, native missing handling, 300 LightGBM trees, learning rate 0.05, random_state 0 and two threads. I reproduced its first exact shipped fold and obtained RMSE **10.64631402974271**, bit-for-bit equal to the stored result. Together with exhaustive data/fold/scorer identity, this supports reusing its remaining historical diagnostics; it is not a claim that all 36 ablations or all model families were rerun today.

The only change to the group probe's feature preparation changes missing categorical codes. I separately executed the old and current `features` functions on GeoAI and asserted exact matrix equality: ID is excluded, leaving only numbers and dates. The old group probe's all-row median imputation remains a diagnostic limitation, not a transformation in the shipped data. Prefer the fold-safe supplements when interpreting model quality. New leak and raw-state probes cover additional questions and should still run in the parent cycle.

**New rules and remaining limits**

The updated temporal-gap rules (SPLIT-9/10/14) do not change this accepted retrospective spatial application: it does not claim prospective prediction, and no station label is shared across train/test. The updated metric rules continue to support source RMSE on an unchanged continuous measurement scale; no costs, threshold, ranking-only use case or contradictory metric experiment has arisen. New dtype requirements are consistent with numeric measurements, datetime Date and group-only categorical ID; the independent column audit/probe should confirm this. Spectrum/molecule encoding rules do not apply. The new review-retention procedure requires restoring the resolved issue history, not reopening its accepted uncertainty automatically.

No new curator input is required by this audit. The mildest follow-through is documentation of the checksum cause, preservation of historical acceptance and completion of the remaining new mechanical probes. Ground-label daily aggregation/QC, exact product release latency, station representativeness, fresh authenticated redownload and exhaustive external duplicate search remain unverified at their previously stated scope.

Primary page reopened on 2026-11-05: [Zindi GeoAI challenge](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge), Evaluation section and challenge description. The short exact metric label is “Root Mean Squared Error.” The remaining source claims above are paraphrases. Original DataDescription.pdf Table 1 was read from the curator-supplied release; its preserved text is in the earlier source audit.


**Raw row-order flag: independently reconciled**

The current raw probe flags lag-one target autocorrelation near 0.603, with row-index Spearman -0.066. A fresh structural test in `raw-order-reconciliation.json` rejects the hypothesis that the file is ordered station by station: **zero adjacent rows share a station**. Instead, each of the 1,096 dates lists all 79 stations in the same order. Of 86,583 adjacent row pairs, 85,488 are within one date and only 1,095 cross to the next date. Among finite target pairs, same-day lag-one correlation is 0.60744 (all adjacent finite pairs 0.60411; the probe's preprocessing yields a slightly different 0.603).

Thus the flag primarily detects same-day dependence across nearby-region stations. This is expected structure in the accepted retrospective same-period spatial task, not evidence that the row order exposes a test station's labels. The model sees the actual Date and coordinates, all nine train/test station sets are disjoint, and adjacent station measurements at the same date are available in the declared historical training archive. There is no future-year claim to invalidate. The raw probe also finds zero raw copies; the dropped submission identifier has R² -0.0105, and all 4,533 removed rows lack the target. These observations do not justify removing date, changing the station split or dropping additional rows (SPLIT-1/3/4, LEAK-1/10/16, EV-1/3). They also do not prove every possible exploit harmless: the participant-style reviewer and expanded leak probes retain their own scope.


**Final documentation clarification: independent follow-up**

After mediator review, the definition gained one `curation_comments` bullet spelling out the already declared `grouping.context="none"`: each held-out-station prediction receives the query row only, with no other rows from that station for aggregation/filling; the complete training archive from other stations remains available. I independently compared the final definition with the accepted artifact again. `final-documentation-audit.json` enumerates the full changed metadata values and all nine fold results.

All data values, dtypes, category metadata, feature names/order, target and exact train/test indices remain equal. All nine fresh training-mean RMSE calculations equal both the accepted artifact and direct computation. After current-schema loading, **only `dataset_metadata.curation_comments` differs**; task metadata and experiment metadata have no differences. Its text diff contains exactly the one added context clarification bullet.

The final checksum is `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. Substituting only the earlier curation comments in the checksum encoding recovers the preclarification checksum `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`. Additionally omitting only the newly serialized empty `special_features` list recovers the original accepted checksum `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. These two changes fully explain the checksum difference. No model was rerun for this documentation follow-up; no new scientific choice or invalidation of reusable model evidence was found.

</details>

<details><summary>Column audit (2026-11-05)</summary>

**GeoAI current-main column audit**

Verdict: retain all implemented columns and cleaning. No new curator input is required by this audit. This is a focused recheck against main `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`; the existing acceptance of label-QC uncertainty, same-region same-period transfer and observed-day coverage remains in force.

I read the current column-auditor instructions, principles, use-case rules, cleaning/dtype rules, leakage rules, provenance and metric changes; the current definition; the original DataDescription.pdf text; and the previous column and acceptance reports. I ran current `dtype_probes.py --no-fetch`, then independently loaded the current definition and compared all stored values to the raw release by station/date. Outputs are `dtype/geoai_ground_level_no2_estimation_challenge.json`, `column_audit.py` and `column-measurements.json` in this run.

The current dtype probe examined ten numeric model columns and raised zero flags. Its automatic codebook lookup was intentionally disabled and matched zero codebook columns; this is not a codebook-coverage claim. The manual table below covers every stored column, including the date, station key and target. The source codebook supplies eight physical measurements and the target; station/date/coordinates are read from the actual release and independently checked.

| Column | Meaning and unit | Known at accepted prediction point? | Dtype, cleaning and fresh measured evidence | Verdict and rule |
|---|---|---|---|---|
| Date | Observation day | Yes: the day being retrospectively mapped | `datetime64[ns]`, 1,096 dates from 2019-01-01 to 2021-12-31. Independent separator-normalized day-first parsing agrees for every station/day. | Keep; CLEAN-12/14, USE-3. |
| ID | Ground monitoring station | Identifies the held-out entity; not supplied as a model input | Unordered category, 79 values, no missing. Excluded by `feature_columns`. No words or ordered levels are supplied to decode. | Keep for grouping only; CLEAN-3/12/14, USE-10. |
| LAT | Latitude, degrees | Yes, query location | `float64`, 44.92469405 to 45.88973369; no missing. | Keep measured numeric quantity; CLEAN-14, USE-6. |
| LON | Longitude, degrees | Yes, query location | `float64`, 8.736496578 to 12.59068235; no missing. | Keep measured numeric quantity; CLEAN-14, USE-6. |
| Precipitation | CHIRPS daily precipitation, mm/day | Yes after the relevant daily products are available | `float64`, 0 to 135.3968048; 65,219 zeros, no missing or negative values. Zero is dry weather, not a code. | Keep; CLEAN-10/11/14. |
| LST | NOAA daily land-surface temperature, K | Yes after daily retrieval is available | `float64`, 253.2 to 327.84; 37,594 missing. Surface temperature is distinct from air temperature. | Keep values and missingness; CLEAN-2/11/14. |
| AAI | TROPOMI aerosol index at 354/388 nm, dimensionless | Yes after retrieval is available | `float64`, -5.196266174 to 2.143020488; 12,118 missing, 66,275 negatives. It is a signed index, not an ordered response scale. | Keep numeric; CLEAN-10/11/14. |
| CloudFraction | TROPOMI effective cloud fraction | Yes after retrieval is available | `float64`, 0 to 1.000000044; 12,118 missing. Three microscopic overshoots of one remain as already accepted numerical precision. | Keep; CLEAN-11/14. |
| NO2_strat | Stratospheric vertical NO2 column, mol/m2 | Yes after satellite retrieval is available | `float64`, 1.34e-5 to 7.28e-5; 12,118 missing. Atmospheric column is physically different from ground concentration. | Keep; LEAK-2/10, CLEAN-14. |
| NO2_total | Total vertical NO2 column, mol/m2 | Yes after satellite retrieval is available | `float64`, -1.19e-5 to 0.002047452; 12,118 missing, six negatives. | Keep ordinary retrieval negatives; CLEAN-11/14, LEAK-2/10. |
| NO2_trop | Tropospheric vertical NO2 column, mol/m2 | Yes after satellite retrieval is available | `float64`, -2.53e-5 to 0.000985; 33,429 missing, six negatives. | Keep ordinary retrieval negatives and missingness; CLEAN-2/11/14. |
| TropopausePressure | TROPOMI tropopause pressure, Pa | Yes after retrieval is available | `float64`, 8,614.349685 to 24,449.00715; 12,118 missing. | Keep physical scale; CLEAN-14/21. |
| GT_NO2 | ARPA daily ground-level NO2, micrograms/m3 | Target unknown at the queried location | `float64`, 0 to 188.2333333; seven zeros; 4,533 missing-label raw rows omitted. Every retained value equals the source. | Keep original scale, zeros and extremes; CLEAN-11/15, USE-5, MET-3. |
| ID_Zindi (removed) | Submission identifier | Supplies no scientific quantity | Excluded from current frame; no label/feature reconstruction is based on it. | Drop; CLEAN-3. |

Fresh audit: 82,051 rows, 13 stored columns, exactly 11 features, zero station/day duplicates, zero numeric infinities, and no tested numeric sentinel among -999, -9999, 9999 and 99999. Each stored value and NaN equals the independently transformed source after alignment by station/date. The file SHA-256 is `fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446`. An initial positional comparison differed because the framework shuffles grouped rows; the corrected semantic-key comparison is the evidence, and it passes.

The amended CLEAN-12/14/25 rules require no recoding here: there are no measured values masquerading as categories, no coded response scales with source labels, no yes/no feature flags, and no classification target. The opaque station identifier correctly remains categorical. The date is restored from its actual encoding; no handcrafted seasonal feature is needed. The source table already represents station-days, so CLEAN-19 does not require turning it into an aggregated log or adding label-neighbour features.

The existing source-product and ground-label processing limits remain unverified. The codebook identifies daily physical quantities and their sources but does not establish operational release latency, complete extraction versions or ground-label daily QC. The accepted prediction point is after products are available and uses the historical archive; this audit makes no forecast or real-time claim. Negative satellite retrieval justification reuses the prior documented primary-catalog review; I did not independently refresh that website in this column pass.

No fresh data mechanism supports clipping the seven zero labels, removing extreme targets, deleting sparse-label stations, imputing predictors, or changing the source RMSE. A public competitor's improved score after deleting towns remains insufficient evidence of invalid rows under CLEAN-1/11/20. None of the new dtype rules contradicts the previous acceptance.

</details>

<details><summary>Precedent consistency (2026-11-05)</summary>

**GeoAI current-main precedent and decision consistency**

Verdict: the October 30 scientific acceptance and source-RMSE choice can be reused under current main. No rule exception or repeated human decision is required by this consistency review. This is a bounded focused check, not a new scientific verdict by the agent.

I generated the current decision register before selecting precedents: 4,030 entries, 176 defined rule IDs and 21 collection-wide flags. None of the flags names GeoAI. `register.json`, `register.log` and `precedent-selection.json` retain the inspected evidence. I compared applicable rule changes from `1964e1b2` to `9048f36a`, then read the rule text and relevant case/record lines. Register entries are navigation summaries; rules and attributed curator lines decide.

| Question | Relevant precedent / current rule | Applicability and conclusion |
|---|---|---|
| Keep documented ground-label construction uncertainty? | differentiated_thyroid_cancer_recurrence, Lennart 2026-10-21; USE-5/8 | The current rules still allow a named-source label with unresolved construction detail, case by case, with approximate fit and the actual gap named. GeoAI already names the daily-QC/aggregation uncertainty and Myunghwan accepted it on October 30. No evidence has converted uncertainty into a demonstrated wrong target. Reuse the decision. |
| Are physical satellite quantities excluded as image-derived descriptors? | infrared_thermography_temperature, 2026-10-21; SEL-15 | Its camera-derived temperatures are physical measurements. GeoAI's retrieved atmospheric columns, precipitation, pressure and temperature similarly have named physical units. The codebook and actual schema support the prior scope decision; no raster/image feature block appeared. |
| Does shared historical time imply a temporal forecast instead of station holdout? | 5g_energy_consumption, USE-9 case, 2026-10-14; airfoil_self_noise grouped setup, 2026-10-20 | The first precedent permits same-period spatial estimation at unmeasured stations; the second supports grouping at the real query entity. GeoAI explicitly estimates unseen stations using the observed archive. New as-of forecasting restrictions do not transform its accepted task into advance forecasting. Keep the station holdout and its limited transfer claim. |
| Replace RMSE because current MET-4 permits overruling some competition metrics? | zillow_prize (source MAE retained); african_credit_scoring_challenge (F1 overruled on specific gaming/probability evidence); loan_default_prediction_imperial_college (2026-11-05 amendment) | The amendment allows reasoned case-specific replacement; it does not require replacing valid leaderboard metrics. GeoAI predicts continuous concentration on its original scale, and source RMSE directly measures concentration error. No measured wrong-metric or gaming evidence was introduced in this review. Keep `Metric.source(rmse)`; no new scoring-only input is required under amended MET-2. |
| Recode every number after the new ordinal/label rules? | CLEAN-12/14 amended October 30-November 1; CLEAN-25 | These rules follow semantics. GeoAI has continuous physical measurements, coordinates, a true date, a grouping ID and a regression target. No source-labelled ordinal or nominal numeric levels were found. The ID has no label mapping to recover. Zero dtype flags and the full manual column audit support leaving the representation unchanged. |
| Does a selection marker force a new acceptance decision? | USE-8 and selection-bias guidance; lt_vehicle_loan_default_prediction, November 5 | Selection marker guidance is case-specific and does not itself reject a dataset. GeoAI's monitoring-site/observed-day coverage limits were explicitly accepted and remain named. This pass found no new measured outcome-dependent sampling or class-mix evidence comparable to the loan-approval selection. Do not manufacture a new scientific question from a changed example alone. Keep scope limited to the represented region and observed days; a future source showing preferential station selection by outcome would be new evidence. |
| Add neighbouring ground labels as new features? | CLEAN-19 expansion; rain_in_australia, October 26 | It permits practitioner aggregates when valid at prediction time; it does not authorize a global target-derived neighbour column. GeoAI's existing source table is usable directly, and an unseen test station provides no measured target. The accepted remote-sensing-feature task stays. Any participant finding of a specific legitimate or leaking cross-row mechanism should be judged on its own measured evidence by the mediator. |

Decision provenance is exact: Myunghwan's October 30 statement, "thse limits are fine", accepted the then-implemented task and its identified limits; the November 5 instruction explicitly asks to reuse past decisions while repeating the cycle against updated main. That authorizes preservation after checks, not relabelling the historical marks as newly made decisions. No old browser marks should receive a new fingerprint. Current review history should cite the original decision and the new reuse instruction, retain resolved issue 1, and reserve issue 2 for any genuinely new issue.

The current review workflow also adds an explicit metric acknowledgement and keeps resolved review files. The accepted implementation already declared source RMSE, and the newest instruction preserves that decision. Record its reuse transparently with the original date/context; do not fabricate a new verbatim "metric ok" quote or treat the panel as the curator. Resolved-history formatting and current runtime/probe checks are follow-through work, not grounds to reask accepted scientific limitations.

Limits: this report does not substitute for the separate fresh claim/split audit, current leak/task probes or task-gamer findings. A concrete new mechanism from those checks can reopen an affected decision. None was established by this column/precedent review.

</details>

<details><summary>Participant task gamer (2026-11-05)</summary>

**Independent participant task-gamer report**

**Verdict**

No demonstrated benchmark-breaking exploit in this bounded audit. The held-out-station regime is respected in all nine shipped splits. Best measured improvement is ordinary calendar engineering; nearest-station label blending also improves mean RMSE, but other-station labels are explicitly available at the stated retrospective prediction point. Neither is target leakage. Do not reinterpret this result as a prospective forecasting result or as prediction in a geographically isolated region.

An interface clarification is useful: `grouping.context=none` says no group context, while the prediction point grants the complete satellite/meteorological archive. Coordinates identify stations exactly. Full-archive feature aggregates and forward filling were tested as an aggressive diagnostic; both worsen mean RMSE here. State explicitly whether external archive retrieval at each prediction coordinate is allowed versus accessing other held-out rows. No measured gain establishes an exploit from this ambiguity.

**Reproducibility and baseline**

Only the supplied participant kit and public web sources were inspected. Baseline uses every feature returned by `score.features()` (11 columns), excludes ID and GT_NO2, converts Date to integer days since 2019-01-01, and keeps native numeric missing values. LightGBM is untuned: `LGBMRegressor(n_jobs=2, random_state=0, verbosity=-1)` (100 estimators, default remaining hyperparameters). All scores use the shipped `score()`; no test-label fitting, tuning, early stopping, per-town coefficients, or public raw-label lookup is used. Test labels are used only for scoring and post-hoc duplicate diagnostics.

Environment: Python 3.12.3, LightGBM 4.6.0, pandas 3.1.0, numpy 2.5.4. Models are sequential and n_jobs=2. Mean scores below are arithmetic means of nine fold RMSEs, not pooled RMSE. Baseline mean RMSE **10.370071**.

The participant analysis used the supplied inputs to test copy, same-time and transductive shortcuts; the measured results and controls are reported below.

**Ranked tests against the same baseline**

Positive gain = baseline RMSE minus method RMSE. Ordering includes legitimate improvements and unsuccessful attacks, not just alleged exploits.

| Method | Baseline | Method RMSE | Gain | Wins/9 | Deployment availability and fix |
|---|---:|---:|---:|---:|---|
| calendar | 10.3701 | 10.0299 | +0.3402 | 9/9 | Legitimate row features. Month/day-of-week/day-of-year; no fix. |
| near_blend_half | 10.3701 | 10.1301 | +0.2400 | 7/9 | Legitimate other-station labels. Fixed half blend with nearest same-day training-station label; no fix for stated task. |
| date_label_mean_weight_0.5 | 10.3701 | 10.1434 | +0.2266 | 7/9 | Legitimate other-station labels. Half blend baseline with all training-station labels on date; no fix. |
| near_copy_1 | 10.3701 | 10.3623 | +0.0078 | 2/9 | Legitimate other-station labels. Copy nearest training station if <1 km; no fix. |
| exact_copy | 10.3701 | 10.3701 | +0.0000 | 0/9 | No matches. All permitted features including location and date; no fix. |
| row_order | 10.3701 | 10.3720 | -0.0019 | 6/9 | Artifact unavailable in deployment. Added positional row number; no gain; preserve shuffling. |
| total_minus_strat | 10.3701 | 10.3978 | -0.0278 | 2/9 | Available row covariates. Add total-stratospheric NO2 and use difference to fill trop; no fix. |
| satellite_date_copy | 10.3701 | 10.4307 | -0.0607 | 2/9 | Available training-label lookup. Exact date+non-coordinate predictors with baseline fallback; shared/missing weather is not duplicated target. |
| test_archive_stats | 10.3701 | 10.4587 | -0.0887 | 4/9 | Archive available; batch contract ambiguous. Coordinate-group covariate means/missing rates across full archive; clarify context:none vs complete archive. |
| drop_three_anomalous | 10.3701 | 10.5250 | -0.1549 | 4/9 | Training-only filtering. Remove 3 stations with largest monthly-profile squared distance from training median; no evidence to remove. |
| archive_ffill | 10.3701 | 10.5375 | -0.1674 | 1/9 | Archive available; batch contract ambiguous. Chronological coordinate-group satellite forward fill; clarify archive access. |
| id_diagnostic | 10.3701 | 10.7902 | -0.4201 | 1/9 | Prohibited diagnostic. Numeric suffix and categorical prefix of ID, excluded by task; keep excluded. |
| near_copy_5 | 10.3701 | 10.9743 | -0.6042 | 0/9 | Legitimate other-station labels. Copy nearest training station if <5 km; no fix. |
| format_missing | 10.3701 | 11.0030 | -0.6330 | 1/9 | Available row covariates. Added missingness flags and rounded fractional part of 1000*x; no gain. |
| drop_missing_satellite | 10.3701 | 11.0147 | -0.6446 | 0/9 | Training-only filtering. Exclude rows with NO2_total missing; worsens all folds, retain these rows. |
| near_copy_20 | 10.3701 | 11.6644 | -1.2943 | 0/9 | Legitimate other-station labels. Copy nearest training station if <20 km; no fix. |
| date_label_mean_weight_1 | 10.3701 | 11.8393 | -1.4693 | 0/9 | Legitimate other-station labels. Predict mean of all training-station labels on date; no fix. |
| near_copy_inf | 10.3701 | 12.4661 | -2.0960 | 0/9 | Legitimate other-station labels. Unrestricted same-day nearest station; no fix. |

**Per-fold measured results**

| Fold | Baseline RMSE | Calendar RMSE | Calendar gain | Nearby half-blend RMSE | Blend gain |
|---|---:|---:|---:|---:|---:|
| r0f0 | 10.7401 | 10.4592 | +0.2809 | 11.1616 | -0.4216 |
| r0f1 | 10.6016 | 10.1883 | +0.4134 | 10.1652 | +0.4365 |
| r0f2 | 9.4560 | 9.0169 | +0.4391 | 9.2127 | +0.2433 |
| r1f0 | 10.7462 | 10.3092 | +0.4370 | 10.4238 | +0.3224 |
| r1f1 | 10.7765 | 10.6041 | +0.1724 | 10.3822 | +0.3943 |
| r1f2 | 9.3598 | 9.0645 | +0.2952 | 9.2241 | +0.1357 |
| r2f0 | 10.9788 | 10.7631 | +0.2157 | 11.4314 | -0.4526 |
| r2f1 | 10.0876 | 9.7261 | +0.3615 | 9.2249 | +0.8627 |
| r2f2 | 10.5839 | 10.1375 | +0.4464 | 9.9451 | +0.6389 |

Every method has all nine RMSEs in `per_fold_rmse.csv`, all nine paired gains in `per_fold_gains.csv`, and row-level baseline predictions in `r*f*_baseline.npz`. Full attack gains are also included below.

| Method | r0f0 | r0f1 | r0f2 | r1f0 | r1f1 | r1f2 | r2f0 | r2f1 | r2f2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| calendar | +0.2809 | +0.4134 | +0.4391 | +0.4370 | +0.1724 | +0.2952 | +0.2157 | +0.3615 | +0.4464 |
| near_blend_half | -0.4216 | +0.4365 | +0.2433 | +0.3224 | +0.3943 | +0.1357 | -0.4526 | +0.8627 | +0.6389 |
| date_label_mean_weight_0.5 | -0.8944 | +1.3117 | +0.1226 | +0.2198 | +0.0477 | +0.1417 | +0.8809 | -0.3338 | +0.5434 |
| near_copy_1 | +0.0000 | +0.0581 | +0.0122 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| exact_copy | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| row_order | +0.0072 | +0.0133 | -0.0159 | -0.0353 | +0.0291 | +0.0257 | +0.0089 | -0.0564 | +0.0064 |
| total_minus_strat | -0.0819 | +0.1609 | -0.0542 | -0.0094 | -0.0375 | -0.0995 | -0.2073 | -0.1962 | +0.2753 |
| satellite_date_copy | -0.1423 | +0.0902 | -0.0344 | -0.0549 | -0.0471 | -0.2246 | +0.0215 | -0.1142 | -0.0403 |
| test_archive_stats | -0.4297 | +0.2879 | -0.3750 | -0.0867 | +0.2682 | -0.8205 | +0.2768 | -0.1193 | +0.2004 |
| drop_three_anomalous | -1.4711 | +0.1063 | +0.1011 | -0.4421 | +0.0739 | -0.0181 | +0.4407 | -0.0772 | -0.1078 |
| archive_ffill | -0.3231 | +0.1076 | -0.1808 | -0.1609 | -0.1608 | -0.2645 | -0.2335 | -0.1482 | -0.1429 |
| id_diagnostic | -1.2389 | +0.1292 | -0.2219 | -0.6385 | -0.3191 | -0.2615 | -0.6173 | -0.1314 | -0.4816 |
| near_copy_5 | -0.9670 | -0.0049 | -0.3795 | -0.5666 | -0.1863 | -1.4618 | -1.2298 | -0.3397 | -0.3025 |
| format_missing | -1.7495 | +0.2393 | -0.3733 | -0.6376 | -0.2831 | -1.4785 | -0.2886 | -0.3690 | -0.7564 |
| drop_missing_satellite | -0.9829 | -0.3600 | -0.7170 | -0.6710 | -0.8036 | -0.7273 | -0.4503 | -0.6388 | -0.4507 |
| near_copy_20 | -1.8982 | -0.3087 | -1.5394 | -1.2549 | -0.6777 | -2.2650 | -2.3347 | -0.6212 | -0.7490 |
| date_label_mean_weight_1 | -3.1350 | -0.1548 | -1.3315 | -1.2714 | -1.8284 | -1.4995 | -0.5220 | -2.0367 | -1.4441 |
| near_copy_inf | -3.4236 | -2.0178 | -1.8525 | -1.4875 | -2.3811 | -2.2941 | -3.9292 | -0.6482 | -0.8299 |

**Public-source findings and reproduction limits**

The [official data description](https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge/data) identifies ground monitoring stations in Lombardy/Veneto and satellite/meteorological sources, and permits derived features and elevation. It does not establish that any feature contains the withheld station label. No public raw-label retrieval was attempted.

The participant-authored [unofficial third-place account](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge/discussions/23436) describes nearby-town copying, per-town and pre/post-2020 coefficients, removal of three anomalous towns, and forward fill. Reproduced applicable ideas as nearest same-day station copying at fixed 1/5/20 km thresholds, a fixed 50% blend, chronological covariate forward fill, and a training-only monthly-profile rule removing three stations. Pure copying mostly worsens; blending helps on 7/9 folds. The exact excluded towns, coefficients, notebook and selection method are not published in that account, so the anomaly rule is a transparent approximation, not an exact reproduction. Test-town coefficients calibrated from withheld labels would be inaccessible and impermissible here; no result based on such coefficients is claimed.

The [public time-series discussion](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge/discussions/21633) reports mixed generalization from date-derived features. This audit measures calendar features directly on the shipped station splits; they improve every fold. Searches for winner code, leakage and papers did not yield a reproducible, more specific magic feature within the bounded search. Elevation retrieval, land-use data and remote-sensing reprocessing were not attempted.

**Negative tests and observations**

- 82,051 rows, 79 station IDs and 79 distinct coordinate pairs. No station ID overlaps train/test in any split. Zero duplicate station/date rows and zero duplicate complete feature rows. Location coordinates are legitimate input for a new station, even though they identify station membership.
- Exact covariate copying matched zero test rows in all nine folds. Omitting coordinates gives 7.49–9.38% date/weather collisions; their labels differ (matched-subset RMSE 11.96–14.98). Full-fold copying results are recorded above, so collision counts alone are not treated as leakage.
- Pairwise aligned-date analysis flags nearby/highly correlated stations. Highest correlation is X5607/X10452, 0.96763 across 1,067 days and about 7.02 km; exact-label equality is 0.094%, with interstation RMSE 4.8898. This is evidence of available spatial signal, not a repeated target series. All flagged pairs are in near_pairs.csv; no near-perfect duplicate sensor labels were found.
- Row order adds essentially no mean benefit. ID numeric suffix/prefix (a deliberately prohibited diagnostic) worsens mean RMSE. Missingness and numerical fractional-format features also worsen. These are bounded probes, not a proof that every possible encoding is harmless.
- Removing the three most anomalous training stations worsens mean RMSE by 0.1549; excluding satellite-missing rows worsens by 0.6446 and hurts every fold. No evidence supports declaring those training rows unjustified. Seven zero targets exist but are not, by themselves, invalid measurements, and were retained.
- Full-archive means/missing rates and forward fill use no held-out labels; both perform worse on average. Total-minus-stratospheric reconstruction likewise fails to improve mean RMSE.

**Uncertainty and skipped scope**

These are cheap fixed experiments with one model seed; no neural models, broad hyperparameter search, external labels, original hidden competition test set, exact winning-code reproduction, geospatial raster download, or prospective temporal split was attempted. Multiple probes share the same nine repeated folds, so selection optimism and dependence apply; tiny differences are not statistically established. The source write-up alone cannot establish leakage, duplicated labels, or invalid training stations. Conclusions are specific to this prediction point and these supplied station splits.

**Artifact fingerprints**

- `task.md` SHA256 `ce7b241415cd1ef41a41054958962c41fe0fe32a75b32ab0a370f99eb0324b4d`
- `task.json` SHA256 `ce21beddbe4ded2dfb45ced54ccfb7320c14a9fb3e07d1bc0c883219fed6090c`
- `score.py` SHA256 `c16f6f7bfd37ff8ff3e9d9fc3e9a34f4113b07cf54fe0e52c5db9f597ca72067`
- `data.parquet` SHA256 `c870ad27a5d172968efe0ab19a39521319cd7c9fb7f15e8f0910bfa4639263d0`
- `splits.parquet` SHA256 `44f2786dabd2efa8e7347afb167623711bfdd41cc9974a8d623a5592d96fa3b9`
- `probe.py` SHA256 `8e74a176cb5baffbfedcdaf6394285cdbc25a7722b8b47d32c2c91b340f3a85b`
- `supplement.py` SHA256 `bdaf6a068107ab75399439d3406e7367daddb152f17df418f9bb8c9db2ffae36`
- `copy_diagnostics.py` SHA256 `568cf1e1ddaffff329c10c9adde19c1c94ef78765a527ad95972c9babfd21692`

</details>


<details><summary>Review editor (2026-11-05)</summary>

**Independent review editor, 2026-11-05**

Recommendation: retain the previous scientific acceptance and finish the authorized cycle after the documentation repairs below and pending verification. No new curator issue is warranted by this cold read. I read the current review-file format, writing and principles references, then REVIEW.md, dataset.py, the generated README and the curation record. This is an editorial/content consistency check; I did not rerun scientific experiments or verify the eventual build.

**Actionable documentation repairs**

- The embedded panel contains 25 Markdown headings beginning with `#`, including report titles and subsections. The current review-file contract expressly disallows headings inside the panel and requires bold text. Convert these headings to bold text while preserving the complete reports and their dated evidence limitations. Keep the dataset's single title. Run the current collector/page validation afterward; do not remove panel evidence merely to make parsing pass.
- The mediator's checksum paragraph and the first claim-audit checksum paragraph describe only the new empty `special_features` field. The later independent follow-up now correctly explains both changes, including the added context clarification in `curation_comments`, and matches the generated README checksum. Preserve the initial audit as historical, but preface it and the mediator report with an explicit statement that their initial checksum explanation predates that clarification; point to the final reconciliation. This avoids a reader mistaking the earlier word “solely” for a statement about the final artifact. No recomputation by this editor is claimed.

The final reconciliation already embedded during this review states the complete chain: final `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`; restoring the old curation comments gives `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`; additionally omitting the newly serialized empty field restores accepted `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. The independent auditor reports exact unchanged data, features and folds. This is sufficient explanation once the earlier scope is explicit.

**Decision provenance and task meaning**

The record and resolved issue preserve Myunghwan's actual October 30 words, “thse limits are fine”, and distinguish the November 5 instruction to repeat the updated-main cycle using past decisions. The metric CC line explicitly records reuse of the accepted source RMSE rather than inventing a new metric mark or quotation. Issue 1 remains resolved and no issue 2 has been fabricated. Earlier acceptance of limited regional transfer, observed-label coverage and unverified daily QC remains visible. I found no contradictory new scientific evidence that would require asking for these decisions again.

The definition and generated README now clearly separate held-out-station access from the training archive: a prediction may use its own query row, and may use the complete labeled archive at other training stations; it may not aggregate or fill from other rows at the held-out station. The mediator explains why the gamer's two broader archive variants fall outside this context contract. Their measured failures are retained as bounded diagnostics, with the original participant input preserved. Legitimate same-day training-station label blends are not misclassified as held-out target leakage. The definition's instruction not to add neighbouring target values describes curation of the stored feature table, consistent with leaving model strategies to participants.

**Evidence and completion boundaries**

Validity: the content consistently describes retrospective station transfer and an approximate use-case fit, without claiming verified daily label processing or future/distant-region prediction. Value: source RMSE and useful signal remain supported by the dated audits and explicit diagnostic limits. Quality: the documentation describes minimal unchanged source cleaning and states the new context clarification. The evidence does not support inventing a new exception, target filter or feature change.

At this read, REVIEW states that the full current group learnability rerun and build remain pending, and the README says not built. The mediator distinguishes a completed fresh split-gap result from the unfinished learnability section, and identifies prior complete results as historical with verified identical feature preparation. These are honest draft limitations. The parent must append actual completion results and update the current summary before presenting the whole cycle as finished; the dated panel reports should retain their original limitations. Build/commit is already authorized by the November 5 request and requires no repeated scientific confirmation absent a new material finding.

The generated README still describes REVIEW as “removed once they are settled”, contrary to the current retained-history rule. This is inherited generator prose, not a reason to delete REVIEW or hand-edit a generated file. Preserve REVIEW; any generator correction belongs to separate tooling scope. This does not change the dataset decision.

**Read identities**

At the final cold-read fingerprint, REVIEW.md SHA256 was `cf12ca8ae6019fe5b117480320f0a16c2513e86f1e8fea3b08b4bd2107bac27a`; dataset.py was `6c65a8a167e27fe433e216125cd81ce3d42eb4097704f02e5fd0221fb13f722a`; README.md was `a64396876ace985236ab19400347645089cfaa4afe43433b41626c5f4620fe75`; the record was `dc3215efc399f261980d7ad47196c3fd20402f4c9106cc1bee179379bc816d0f`. The parent is actively finalizing these artifacts, so these hashes identify the review inputs rather than asserting final build freshness. No project source file was edited by this reviewer.

**Repair verification, 2026-11-05**

I reread the parent's revision, REVIEW SHA256 `9b3733429ce5709321e21e53ed3c6b6d593ee002e8eaad0a4205217f6a3f899a`. The 25 panel headings have all been converted to bold, and the new current checksum reconciliation explicitly explains both metadata changes and scopes the older paragraphs to their preclarification snapshots. Both substantive repairs are satisfied.

One placement fix remained in that revision: the new reconciliation paragraph sits outside a details section after the panel summary. The format requires only details sections after the first summary paragraph. Wrap the reconciliation in its own details section or put it inside the mediator section, then validate collection/rendering. This is a mechanical format repair with no scientific effect. No further actionable content issue was found; the fresh group run and build remain explicitly pending.


**Application:** All three formatting/content fixes were applied: embedded headings use bold text; the two checksum causes are explicitly distinguished; the checksum reconciliation is enclosed in a details section. The generated collector/parser verifies the final structure.

</details>

<details><summary>Completion of verification (2026-11-05)</summary>

The current full group probe completed over 82,051 rows, 79 stations and all nine folds. IID versus grouped LightGBM R2 is 0.788 versus 0.636 (gap 0.152). Across-group R2 is ridge 0.396, random forest 0.631, LightGBM 0.634 and kNN 0.554, matching the historical printed results. These are indicative utility diagnostics with full-frame median preprocessing, not benchmark rankings. A group-label permutation test does not apply to per-sample labels.

The requested build completed from clean definition commit `2687a3ae2ebd33135af563cf9605e3adbc2897b6`: format 2, UUID `01a1adf0-eb77-7e00-8228-2b3c1bc263db`, checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. All 27 checks passed with zero errors or warnings. Saved-container reload verified; a check with only the traced Train.csv (10,000,397 bytes) reproduced the checksum. Rows, nine splits and raw-input selection are unchanged from the October build. The raw-input backup passed ZIP CRC and source SHA-256 checks. The October container is retained because the preserved historical checkout still names it as its current build; no obsolete unreferenced container was deleted.

The source panel reports above retain their original timing and qualifications. Their requested documentation repairs were applied and the current collector rendered one resolved issue, zero open issues, no cross-dataset items and the explicitly reused metric acknowledgement. No new scientific decision is required; the original acceptance and limitations remain in force.

</details>

<details><summary>Qualification refresh: mediator</summary>

**Independent mediator — qualification refresh, 2026-11-06 UTC**

**Verdict: ship.** Retain the previously accepted scientific definition and complete the authorized current-cycle review and build. This recommendation does not claim that the new build has completed. No new curator decision or scientific change is needed.

Validity: SEL-15, USE-1/3/5/8, SPLIT-1/3/24 and PROV-1 remain supported for retrospective, same-period estimation at withheld stations; unknown daily ground-label aggregation/QC and regional/observed-day coverage remain explicitly limited. No new Must violation is demonstrated. Value: retain source RMSE on the original concentration scale (MET-1/2/3/4); exact fold/scorer identity supports the historical utility evidence under EV-8. Quality: preserve faithful values, missingness and minimal date/identifier cleaning (CLEAN-2/3/11/12/15). Weighed: source and shape positive; approximate use case, no measured thin-category bonus and no newly demonstrated material defect; priority remains 3. For the curator: none.

**Changes and completion work requiring no new decision**

- Preserve the October 30 acceptance and resolved issue 1. Record this cycle as reuse under the explicit repeat-cycle instruction, without inventing a new human mark or rebinding old session fingerprints. This follows the principles' decision precedence and the review-history procedure.
- Clearly distinguish current measured checks from historical model/probe evidence (EV-7/8). The previous November artifact, rather than the October artifact, is the current comparison baseline. Its checksum already matches the fresh in-memory result. The older serialization/context-note checksum change must remain historical.
- Complete editor review and the requested build, saved-container reload and traced-input reproduction, then record their actual results. Until they finish, completion statements are pending (EV-7). The parent corrected the draft verification wording to keep editor/final completion pending; preserve that distinction through handoff.
- Preserve all existing scientific limitations and the query-row-only held-out-station context. No feature, target, metric, cleaning or split edit is warranted.

**Issues for the curator**

None. The fresh claim and precedent reports agree; there is no new disputed fact or weighing call. Acceptance is not being used to waive a Must. It applies because no contrary evidence or changed scientific condition was identified. Daily label QC/aggregation, precise product-release latency, station representativeness, authenticated current download availability and exhaustive duplicate coverage remain unverified; fresh mechanical checks do not establish those facts (USE-8, EV-7).

**Agreed facts and scope of evidence**

This is a focused recheck. Fresh roles are claim auditor, precedent checker and mediator, with editor review still required at this report's completion. The focused-panel procedure calls for a task gamer when features, target or split change; none changed. No new blind review, advocate/critic debate, column/split panel or gamer run is represented as having occurred. Prior full and focused panels remain historical evidence.

The claim auditor's fresh comparison establishes exact equality of every dataframe value, dtype, category metadata, row/column order, missing value, model input, all nine train/test index arrays and all three metadata objects against the previous November container. The checksum is unchanged. Independently parsed raw data retain 82,051 of 86,584 station-days after excluding 4,533 missing targets, with 79 stations and eleven model inputs. All folds have zero station, coordinate and complete-feature overlap, positive target variance, and identical manual/current-scorer RMSE. Their 1,096 shared dates are intentional under the retrospective task. These are measurements relevant to EV-1/2, SPLIT-1/3/24, LEAK-16 and MET-2/3, not a proof of all possible scientific claims.

The source-identity audit and reconciliation agree that all 32 selected procedures and 168 tracked source files match the preceding cycle. The upstream source is the same `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`; previous final head is `5eb90020ef7fad05bdf6f2f60bbca31ae0eb5b81`. Recorded core package versions match, including LightGBM 4.6.0. This supports reuse under unchanged measured conditions, without asserting binary-identical environments or a complete historical transitive-dependency inventory.

Current verification reports 27 bundle checks with zero errors/warnings, zero dtype flags, passing definition imports and dataset lint/format, and 2,017 tests passed: the initial run and targeted rerun; 286 skipped. These are the parent's execution results inspected through the supplied verification evidence, not tests independently rerun by this mediator.

The prior completed group, task, leak, raw-state, column and participant evidence is identified in reused-evidence.json. The completed November group log supersedes the old mediator's then-pending learnability note. The full heavy probe and participant sweeps were not rerun in this cycle. Full-frame median preprocessing limits the historical group diagnostics; fold-safe supplements and finite one-seed participant tests retain their own scope and selection optimism. Exact data, folds, metadata, source and scorer equality makes this reuse adequate for this unchanged-task refresh (EV-8); it does not turn the old numbers into fresh fits.

A supplementary fresh numerical checkpoint, runtime-model-check.json, reproduces all 27,659 predictions of the previous r0f0 LightGBM participant baseline exactly: maximum absolute difference 0.0, RMSE 10.740054356570974. This is one fold, not a new full participant or utility sweep. The initial kit comparison exposed a Parquet station-ID category-label dtype difference (str versus object); exact station strings, model-feature/target dtypes and values, and fold indices were then checked. ID is excluded from model inputs, and the separate direct-container comparison remains exact. This serialization detail does not change the scientific conclusion.

**Historical gamer findings mapped to the current contract**

The prior gamer is reused, not newly run. Its calendar improvement of mean nine-fold RMSE from 10.3701 to 10.0299 uses legitimate query-row information (USE-3/6, LEAK-10). Same-day training-station target blending is legitimate under the complete other-station training archive; its reported gains do not show access to held-out labels (SPLIT-1/3/24). Exact-copy attacks found no matches, consistent with the fresh zero-overlap check (LEAK-16). Nearby correlated stations were not identical target series.

Held-out-station archive aggregates and forward filling were outside `context="none"`; their historical mean RMSE worsened by 0.0887 and 0.1674 respectively. The previous cycle already clarified the row-only contract, so there is no remaining new ambiguity or task expansion (SPLIT-24/26, USE-3/6). Row-order, prohibited identifier and format/missingness probes showed no mean benefit; training-row/station removal also worsened scores. These bounded negative tests are not exhaustive proof (EV-3/6/7). The definition has no accepted-check-warning or `Potential leak, kept on purpose:` exception to reconcile; no measured new exploit requires adding one.

**Consistency with precedent**

The independent precedent report identifies no GeoAI-specific conflict or new drift. Physical quantities follow SEL-15, consistent with infrared thermography temperatures. Same-period station holdout follows the application, consistent with the missing-station use case of 5g_energy_consumption (SPLIT-1/3/24). Approximate named-source labels with explicit construction gaps remain consistent with USE-5/8 and the differentiated_thyroid_cancer_recurrence precedent. Source RMSE remains consistent with MET-4 and the source-metric precedent; no measured pathological incentive justifies replacement. The eight newly extracted register entries are previous-cycle history, including resolved text, rather than eight new decisions. No exception, amendment or reopened curator issue is required.

This mediator inspected the supplied reports, JSON evidence, current definition/README/record/review, relevant procedures and historical mediator/gamer reports. It did not independently rerun models, access remote sources or alter repository files. The scientific ship recommendation is complete; current-cycle editor/build verification remains separate pending work.

</details>

<details><summary>Qualification refresh: claim audit</summary>

**GeoAI focused claim audit — qualification refresh**

Observed 2026-11-06 UTC. Recommendation: retain the prior scientific acceptance and complete the authorized review/build. **No new curator input is needed.** No refuted current scientific claim was found. This focused audit does not claim that every possible exploit or external duplicate has been excluded.

Validity: exact raw reconstruction, station-disjoint folds and unchanged retrospective query-row contract satisfy the checks relevant to USE-1/8, SPLIT-1/3/23/24, PROV-1 and LEAK-16. Value: source RMSE remains appropriate on the unchanged physical target and is freshly computable on all nine folds (MET-1/2/3/4). Quality: dates, missing-target removal and faithful input/target preservation remain unchanged (CLEAN-2/12/15). Previously accepted limits remain limits.

**What was freshly tested**

`claim_audit_current.py` was adapted into this new panel directory and run through the dedicated capped runtime. It rebuilt the current definition in memory and loaded the previous **November 5** container `01a1adf0-eb77-7e00-8228-2b3c1bc263db`. It did not overwrite that artifact or prior evidence. Assertions passed for exact dataframe values, dtypes, category metadata, column and row order, missingness, eleven model inputs, all nine train/test index arrays, and all three metadata objects. The saved checksum, its fresh recomputation, and the new in-memory checksum are all:

`v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`

There is **no new checksum or scientific change** in this cycle. The older October-to-November schema/comment explanation remains historical; it must not be presented as a new difference from the November artifact.

`source_identity_audit.py` independently compared all 32 procedure hashes with the previous instruction manifest. It also compared 168 tracked files selected by `git ls-files src .claude tests pyproject.toml curation/vocabularies.yaml` against both upstream `9048f36a1bcf7da3687fde04b18ef79cd7a1201e` and the previous final commit `5eb90020ef7fad05bdf6f2f60bbca31ae0eb5b81`. All match the current files. This includes model/feature-preparation code, group/task/leak/dtype probes, scorer, container/schema code, role instructions and tests; per-file hashes are in `source-identity-audit.json`. The definition also matches the previous review fingerprint. No new workflow semantics were inferred merely from the integration-pin change.

**Claims and refutation tests**

| Claim (where written) | Test that could refute it | Result and evidence | Rule |
|---|---|---|---|
| “82,051 rows” from “79” stations, 2019–2021 (`task_summary.row`) | Independently parse and count raw and prepared rows/groups | Fresh: 86,584 raw; 4,533 missing targets removed; 82,051 retained; 79 stations; 1,096 raw dates/station and one-day gaps. | CLEAN-12/15, EV-1 |
| “Drop only the 4,533 missing targets” and preserve measurements/NaNs (`curation_comments`) | Compare complete retained raw/prepared frames keyed by independently parsed station/date | Fresh: every retained value and NaN equal; no imputation, filtering by score, smoothing or target-derived stored feature. | CLEAN-2/6/7/15 |
| “ID is a station grouping key and is excluded from model features”; ID_Zindi dropped (comments) | Inspect feature API, full dataframe and duplicate keys | Fresh: eleven inputs, no target or station/submission identifier; zero duplicate station-days; two repeated submission keys remain separate real station-days. | CLEAN-3, LEAK-16 |
| “Whole stations are held out across all dates” (`task_summary.split`, `grouping`) | Compare every fold and intersect stations, coordinates and full-feature row hashes | Fresh: all nine exact memberships match; zero station, coordinate or full-feature hash overlap; 26–27 test stations and 26,637–27,875 test rows/fold. | SPLIT-1/23/24, LEAK-16 |
| Test dates overlap training intentionally (`splits_comment`) | Count date intersections per fold | Fresh: 1,096 shared dates in every fold. Consistent with retrospective same-period spatial task; no forecast claim. | SPLIT-1/3, USE-8 |
| Six original unlabeled stations differ from training (comments) | Parse Test.csv and intersect station/coordinate sets | Fresh: six test stations; zero overlapping IDs or coordinates. Test.csv contributes no container rows. | SPLIT-1, CLEAN-12 |
| Labeled coverage 298–1,093 days; seven zeros, maximum 188.2333333 (comments) | Count coverage and target extremes; exact raw comparison | Fresh: all named counts/extrema match. This does not verify sensor QC or representativeness. | CLEAN-11/15, USE-8 |
| Negative satellite retrievals and cloud excess are retained (comments) | Exact raw equality and fresh extrema | Fresh: negative values unchanged, no NO2 minimum below -0.001 mol/m²; CloudFraction maximum 1.000000044. Product-document explanation is reused from prior audit. | CLEAN-11, EV-2/8 |
| “Root Mean Squared Error (RMSE)” is original metric (`Metric.source`, README) | Inspect current metric metadata and previous source reading | Holds as reused source evidence: previous auditor opened official challenge Evaluation section on November 5 and recorded explicit RMSE, distinct from jury correlation/MAE. No new page access is claimed. | MET-1/4/11, EV-7/8 |
| RMSE scores original ground concentration per row (metric/target) | Score a training-mean prediction with current scorer and previous container, compare manual RMSE on every fold | Fresh: all three exactly equal on all nine folds; each fold has positive target variance. No extra scoring columns required. Target values/scales unchanged. | MET-2/3 |
| Every feature is available at declared prediction point (`task_summary.known`, comments) | Inspect prediction-point wording and original source evidence | Supported for after-products-available retrospective estimation. Exact release latency is still unverified; real-time or as-of-day availability is not established. | USE-3/8, LEAK-1/10, EV-7 |
| “Each prediction uses only the query row” at held-out station; training archive remains available (comments/context) | Read current enum and clarification, compare metadata and old participant findings | Fresh metadata/text inspection: context remains `none`; old held-out archive aggregation variants remain outside contract. Training-station same-day signal is allowed. No new fitting performed. | SPLIT-24/26, EV-8 |
| Raw autocorrelation indicates leakage (possible reading of prior raw probe) | Freshly test raw adjacency and inspect prior decisive test | Fresh: zero adjacent rows share a station; 85,488 adjacent pairs share a date. Prior raw-order reconciliation explains same-day spatial dependence. This flag alone does not refute station holdout. | EV-1/3, SPLIT-1/3 |
| Empty accepted warnings and passing current checks (definition/check log) | Read current check output | Current parent-run check: 27 checks, zero errors/warnings/infos. It is mechanical evidence, not universal scientific assurance. | EV-3/7 |
| Historical model results still apply (record/review completion) | Exact inputs/folds/scorer/source and runtime core-version comparison | Reusable historical diagnostics under unchanged measured conditions; no fresh heavy-model rerun claimed. See below. | EV-8 |
| Original source/citation/year and atmospheric-vs-ground quantities (metadata/comments) | Inspect prior primary-source audit and unchanged raw/definition identity | Reused historical source evidence; no new source publication or raw change is identified. Ground-label aggregation/QC remains undocumented. | PROV-1/8, USE-5, EV-7/8 |

**Evidence reuse and limits**

Current pandas 3.1.0, numpy 2.5.4, scikit-learn 1.7.2 and LightGBM 4.6.0 match the explicitly recorded previous runtime. Build metadata also records the same Python, pyarrow and polars versions. This is package-version evidence, not a claim of identical installed binaries or a complete old transitive dependency inventory.

The November 5 full group log completes the earlier mediator's pending condition: IID/grouped LightGBM R² 0.788/0.636, gap 0.152; grouped ridge 0.396, random forest 0.631, LightGBM 0.634, kNN 0.554. These remain **historical untuned diagnostics** with full-frame median preprocessing; they are neither fresh fits nor tuned benchmark rankings. The prior fold-safe supplements and participant experiments also remain historical, with finite one-seed search and selected-gain optimism preserved. Current source and exact input identity support their reuse; they do not erase those methodological limits. Prior source/scorer/probe files are now hashed and compared against both relevant commits. Prior run files have fresh identifying hashes, without pretending that every old experiment-time byte had a cryptographic attestation.

The prior full panel, focused panel, original-source metric reading and accepted issue history remain applicable. Human acceptance is the October 30 decision, reused under the explicit repeat-cycle instruction; this audit does not create a new human mark or rebind old session fingerprints. Issue 1 remains resolved. A change of target, metric, split, query context or operational scope would need new review; this cycle made none.

**Unsupported or untested claims, ranked**

- P3/P4/P5: actual daily label aggregation/QC, exact product-release latency and station representativeness remain cannot-verify. The mildest remedy is the existing explicit limitations; no demonstrated new invalid-label mechanism requires reopening accepted issue 1.
- P5: a fresh authenticated redownload and exhaustive external duplicate search were not performed. Preserved Train.csv SHA-256 freshly matches `fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446`; the loader verifies it. This establishes local input identity, not present-day remote download availability or exhaustive uniqueness.
- P6: no claim is made that all historical model experiments were rerun, that every dependency binary is identical, or that the finite gamer search excludes all shortcuts. Preserve their measured, dated scope.

No new concrete curator choice follows from these unchanged accepted limits. The parent still owns the new cycle's final review/build verification and completion record. This reviewer made no repository edits and no transfers.

</details>

<details><summary>Qualification refresh: precedent consistency</summary>

**GeoAI precedent consistency — qualification refresh**

Verdict: **consistent; reuse the existing acceptance, source RMSE, priority 3 and row-only `context="none"` contract. No concrete new human decision is needed.** This is an independent consistency assessment, not a fresh curator mark or a new scientific acceptance. The current instruction explicitly repeats add → review → build while reusing past decisions.

**Scope and evidence identity**

Read the current precedent-checker role, review-added-datasets procedure, principles and applicable use-case, metric, priority and grouping rules; inspected the current definition, REVIEW and record, the October 30 decision session, previous decision-reuse receipt and previous precedent report. Current upstream pin is `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, the same upstream source already used in the previous cycle, whose final head is `5eb90020ef7fad05bdf6f2f60bbca31ae0eb5b81`.

Reconciliation records all 32 selected procedure hashes equal and zero differences among 168 tracked source files. Runtime resolves Data Foundry to this checkout; the lock adds `lightgbm==4.6.0` and removes nothing. That installation change does not itself change a scientific decision. Fresh runtime checks remain the parent cycle's responsibility.

I independently hashed `dataset.py`, `README.md`, `REVIEW.md` and the curation record: all four match the final snapshot in the previous decision-reuse receipt. No new dataset, source, metric, feature, grouping or review-history modification was identified in this round. The earlier October-to-November checksum change was already reconciled as empty `special_features` serialization plus explanatory row-only context prose; it is not a new change in this refresh.

**Current register, including apparent open issues**

The new register contains **4,038 entries**, against **4,030** in the previous register: **+8, −0**. Both define **176 rule IDs** and contain **21 collection-wide flags**. The complete flag arrays are equal, and **zero flags name GeoAI**. All eight added entries concern GeoAI's completed previous cycle: one metric-reuse CC line, one focused-panel assessment and six lines mechanically classified as `open_issue` from retained REVIEW text. Those six include resolved issue 1 and historical mediator completion instructions. Current REVIEW closes issue 1 and has a completion addendum reporting the finished group probe and build; these register labels are not evidence of six new unresolved decisions. Register flags and extracted lines are navigation candidates, not semantic findings (precedent-checker instructions and principles).

The unchanged `CLEAN-19` amendment-due flag concerns amex and electricity/gas invoice aggregation exceptions, not GeoAI. The unchanged metric exception flags concern within-group ranking/correlation tasks. Neither is a same-facts conflict with per-station-day concentration estimation. Temporal label-maturity flags concern prospective issued-loan outcomes; GeoAI deliberately uses complete other-station archives for retrospective same-period estimation. No new drift or third exception by this curator was identified.

**Per-decision consistency**

| Decision | Classification and rule basis | Closest precedent and distinguishing facts |
|---|---|---|
| Preserve October 30 acceptance with unknown daily ground-label QC/aggregation | **Consistent.** USE-5 expressly permits named-source labels with unverified construction to ship case by case with approximate fit and a named gap; USE-8 and EV-7 require honest limits. CLEAN-11/15 support retaining unproven extremes and excluding missing targets. | `differentiated_thyroid_cancer_recurrence`, Lennart 2026-10-21, is approximate because label breadth/horizon remains unverified (use-case Cases). GeoAI has a defined physical concentration target and source attribution; no evidence now establishes a different or corrupted target. Its curator accepted exactly the remaining uncertainty on 2026-10-30. |
| Retain regional same-period whole-station transfer and observed-label coverage limits | **Consistent.** USE-1/3/8/9/10 and SPLIT-1/3/24 align the split to unseen stations, not an advance forecast. | `5g_energy_consumption`, Lennart 2026-10-14, uses within-period station holdout for missing-station estimation; grouped `airfoil_self_noise` likewise matches the real query entity. GeoAI's complete 2019–2021 archive is intentionally available at other stations. Its 82,051 observed station-days at 79 stations do not establish future-year, distant-region or missing-monitor-day performance. No new measured selection mechanism changes the already approximate fit. |
| Keep physical satellite/weather measurements as tabular inputs | **Consistent.** SEL-15 follows physical measurement semantics. | `infrared_thermography_temperature`, Lennart 2026-10-21, keeps physical temperatures measured with a camera. GeoAI's atmospheric columns and weather measurements are named physical quantities; no new raster-descriptor block appeared. |
| Keep `Metric.source("rmse")` on original concentration scale | **Consistent.** MET-1/2/3/4/11 support a declared source metric at the station-day unit and physical target scale. | `zillow_prize`, Lennart 2026-10-21, keeps source MAE. The MET-4 amendment of 2026-11-05 permits case-specific replacement of weaker competition choices on evidence; it does not require replacement. Unlike `loan_default_prediction_imperial_college` or `african_credit_scoring_challenge`, no measured pathological metric incentive or wrong-use-case evidence is supplied here. RMSE requires no extra scoring column. The existing CC explicitly describes reuse, not a newly supplied metric mark. |
| Keep priority 3 | **Consistent.** The Priority procedure in selection.md starts at 1 and weighs factors; it is not itself a validity rule. PROV-1/8 support source +1; USE-1/8 do not earn a direct-use-case point for an inferred actor. | The measured October 30 and November 5 GeoAI assessments agree: 1 + source 1 + shape 1 + gap 0 + direct-use-case 0 − demonstrated-risk 0 = **3**. The earlier screening's conjectured thin grouped regime was superseded by accepted-definition counts. Nothing in this same-source, unchanged-record refresh supplies a new coverage or risk fact. QC uncertainty remains disclosed; it has not become a demonstrated unclear quantity or damaged target. |
| Preserve the row-only explanation of `context="none"` | **Consistent clarification, not an exception or task expansion.** The maintained definitions guidance says `none` means each row stands alone. USE-3/6/10, SPLIT-3 and LEAK-10 constrain information to the declared task. | The enum already was `none`; the previous mediator clarified it on November 5. Other rows of a held-out station cannot be used for its aggregates/filling. Complete labeled archives at other training stations remain legitimate. The CLEAN-19 `rain_in_australia` case (Lennart 2026-10-26) permits legitimate cross-location information available at prediction time; it does not authorize a global target-derived column or extra held-out-station context. The previous task-gamer results do not change this contract. |

Rules outrank precedents and Must violations cannot be waived just because the curator once accepted a task. Here no newly identified Must violation or unexplained departure was found. Therefore no reflection prompt or manufactured additional approval is appropriate.

**Decision provenance and handoff**

The preserved historical session records Myunghwan's October 30 ship verdict and issue-1 `ok`: “thse limits are fine”. The previous reuse receipt records the November 5 request and completed application. The current authorization again directs the same cycle using past decisions after the review-procedure update. These establish reuse authority, not new issue/metric marks. Do not rebind old browser marks to new fingerprints. Keep issue 1 resolved and reserve number 2 or above for an actually new finding. The current review-added-datasets procedure also applies ship when issues, field disagreements and metric are settled; it does not require repeated acceptance of unchanged limits.

The old REVIEW contains historical unfinished-work statements with a later completion addendum. Preserve that chronology. New runtime/build verification must be reported as new execution evidence, not silently substituted for the historical result. This report does not independently rerun models or authenticate a new source download. Ground-label aggregation/QC, operational product latency/versioning, regional representativeness and exhaustive external duplicate coverage remain incompletely established. The historical full-frame median preprocessing limitation in group diagnostics remains; finite participant attacks are not an exhaustive leak proof.


</details>

<details><summary>Qualification refresh: review editor</summary>

**Independent review editor, 2026-11-06 UTC**

Verdict: ready for completion after the small presentation edits below. No new scientific issue or curator decision is warranted. The requested new build remains pending at this read; this report is neither a build-verification result nor a new human acceptance.

I read the current editor role, writing guidance, principles and review-file format, then the complete REVIEW, current definition, generated README, curation record and new changelog entry. I checked the fresh claim, precedent and mediator reports against the summary. This was a cold editorial consistency check; I did not rerun experiments or authenticate external sources.

**Concrete edits, in priority order**

1. Make the opening judgment describe this repeat cycle and include its decisive validity, value and quality findings. The current outcome still leads with "after current-main verification" and ends "This clarifies the existing context contract without changing it", which can make the previous cycle's clarification sound newly applied. Replace the whole outcome paragraph with:

   > **Outcome:** added. Recommend shipping the previously accepted retrospective unseen-station task. The focused recheck found unchanged source values, target, inputs, whole-station folds and source RMSE; no new validity issue was identified. Historical probes still support useful predictive signal, and minimal cleaning preserves the released measurements and missing inputs. Source and dataset size support inclusion; ground-label processing, regional coverage and product timing remain documented limits. No new curator decision is needed; the requested new build remains pending.

   Once the new build is actually verified, remove the final pending clause and append its dated completion evidence separately. Do not change the dated earlier reports' pending statements.

2. Keep the main-points line about the curator's decision. Replace:

   > **Main points:** Myunghwan accepted the implemented task and its documented limits on 2026-10-30 and explicitly requested reuse of those decisions on 2026-11-05. Issue 1 is preserved as resolved; any new issue must use number 2 or higher.

   with:

   > **Main points:** No new decision. Myunghwan's 2026-10-30 acceptance and resolved issue 1 remain in force under the repeated instruction to use the past decisions.

   The issue-numbering instruction belongs in the working notes. Preserve the exact original acceptance and subsequent reuse CC entries already present in the record.

3. Omit execution-system status from the public review; retain only the scientific evidence and its limitations.

**Evidence and scope checks**

- Issue 1 has the required problem, options and recommendation, one implemented row, original quoted answer and explicit resolution. Its rule references are in a footnote. No unresolved record-field disagreement or separate metric choice was identified.
- The metric CC explicitly acknowledges source RMSE by reuse of the accepted implementation, without inventing a new metric mark. The current audit distinguishes the previous official-source reading from fresh scorer checks.
- The fresh reports support exact comparison with the November container: data, dtypes, metadata, inputs, nine fold memberships and checksum. The older October-to-November serialization/context explanation is clearly historical in the fresh reports. The historical full-frame preprocessing limitation, finite participant search and selected-gain optimism remain disclosed. The fresh one-fold LightGBM reproduction is not presented as a new nine-fold sweep.
- The mediator supplies validity, value, quality, weighed factors and the absence of a new decision. Accepted uncertainty is not treated as proof of label quality, real-time availability, broad regional transfer or exhaustive absence of shortcuts.
- The panel is last, uses one summary and closed, nonnested details sections. Public evidence links in REVIEW are portable; no absolute filesystem link or integration-specific link was found there. The new changelog entry has no link-scope problem. Its pending editor/build sentence must be replaced by actual completion evidence only after completion.
- README currently names the previous November build, consistent with the pending new build. Its generated generic description that REVIEW is "removed once they are settled" conflicts with the maintained history-retention procedure, but is an existing generator wording defect. Preserve REVIEW and its resolved issue; this dataset-only repeat cycle need not expand into a shared-generator change or a scientific issue.

The scientific recommendation remains unchanged. Complete the already authorized build and validation, record actual completion, and preserve the distinction between reused human decisions, current measurements and historical evidence.

Application: the opening outcome and main points were rewritten as requested, and the local host-status paragraph was removed only from the newly embedded precedent report. The complete original report remains in the local evidence. No scientific definition changed.

</details>

<details><summary>Qualification refresh: completed verification (2026-11-05 Pacific)</summary>

The qualification refresh build is complete: format 2, UUID `01a1ae48-7d06-76ac-9741-a58d8233b176`, from clean review commit `a40b46997a5bb7b08a2bac87187c74c109512466`. All 27 checks passed with zero errors or warnings. Saved-container reload verified. A check using only the traced Train.csv (10,000,397 bytes) reproduced checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`, exactly equal to the preceding November build. Rows, all nine splits, metadata and raw-input selection are unchanged. The new input backup passed ZIP CRC and source SHA-256 checks. Earlier containers remain retained as referenced audit baselines; no raw files or containers were removed.

The dated reports above retain their original pending statements. All of their requested follow-through is now complete: the summary repairs were applied, native review collection confirms one resolved issue and zero open decisions, and the refreshed runtime built and reproduced the accepted definition. Historical full model/probe results remain explicitly reused; the fresh numerical checkpoint covered one fold. No new scientific change or curator mark was introduced.

</details>
