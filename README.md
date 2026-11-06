# Dataset claims

Who is working on which dataset right now. A claim covers the dataset's curation record and its dataset folder. One file per claim under `claims/`, written by `data-foundry-curation claims` (claim, release, renew); do not edit by hand. An expired claim can be taken over.

As of 2026-11-06 00:54 UTC: 45 claim(s) (Andrej 16, Lennart 6, Myunghwan 23).

## Andrej

| Dataset | Stage | Since | Until | Note |
|---|---|---|---|---|
| `allstate_claim_prediction_challenge` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `australian_vehicle_insurance_2004_2005` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `boreal_postfire_lichen_biomass` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `frempl_french_motor_personal_line` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `liberty_mutual_fire_peril_loss_cost` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `loan_default_prediction_imperial_college` | add | 2026-11-01 | 2026-11-08 | add-dataset, zero-inflated batch |
| `noaa_afsc_bottom_trawl_survey_cpue` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `noaa_storm_events_damage` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `pricing_game_2016_french_fleet` | add | 2026-11-01 | 2026-11-08 | add-dataset, zero-inflated batch |
| `pricing_game_2017_french_mtpl` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `spanish_homeowners_motor_insurance_2010_2014` | add | 2026-11-02 | 2026-11-09 | add-dataset |
| `spanish_motor_insurance_2015_2018` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `spanish_motor_insurance_coverage_level_2022_2024` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `wadden_sea_sibes_macoma_abundance` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `walmart_sales_in_stormy_weather` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |
| `wisconsin_local_government_property_insurance_fund` | add | 2026-10-30 | 2026-11-06 | add-dataset, zero-inflated batch |

## Lennart

| Dataset | Stage | Since | Until | Note |
|---|---|---|---|---|
| `1000_cameras` | triage | 2026-10-31 | 2026-11-07 | data-scouting run: Better data lines and cleanup notes |
| `facebook_recruiting_human_or_robot` | triage | 2026-10-31 | 2026-11-07 | screening (data-scouting run 2026-10-30/31) |
| `fl2000` | triage | 2026-10-31 | 2026-11-07 | data-scouting run: Better data lines and cleanup notes |
| `secom_semiconductor_yield` | triage | 2026-10-31 | 2026-11-07 | screening (data-scouting run 2026-10-30/31) |
| `zeosyn_zeolite_synthesis` | triage | 2026-10-31 | 2026-11-07 | screening (data-scouting run 2026-10-30/31) |
| `zindi_weekendz_laduma_analytics_football_league_winners_prediction_challenge` | triage | 2026-10-31 | 2026-11-07 | data-scouting run: Better data lines and cleanup notes |

## Myunghwan

| Dataset | Stage | Since | Until | Note |
|---|---|---|---|---|
| `2024_lusaka_mobility_prediction_hackathon` | review | 2026-10-28 | 2026-11-06 | Curator accepted; build, reload and traced-input reproduction complete. Submitted in PR #33: https://github.com/TabArena/data-foundry/pull/33 . Accepted approximations and source/descriptor limits are documented. Awaiting PR review/merge; retain Myunghwan ownership until merged. |
| `ai4d_lab_tanzania_tourism_classification_challenge` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `airqo_african_air_quality_prediction_challenge` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `airqo_low_cost_air_quality_monitor_calibration_challenge` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `bemtpl97` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `chicago_traffic_crashes` | triage | 2026-10-29 | 2026-11-05 (expired) | Selected by Myunghwan as the next large-scale candidate (about 1.1 million crashes). Reservation for screening review; no scientific inclusion or build decision. |
| `chromophore_optical_properties_db` | triage | 2026-11-05 | 2026-11-12 | Curator-requested triage: priority-4 interaction datasets; scale, source and non-IID qualification pending. |
| `desi_dr1_star_galaxy_quasar` | add | 2026-11-04 | 2026-11-11 | Myunghwan requested DESI add-dataset; label accuracy and systematic class noise require investigation before inclusion. |
| `duolingo_spaced_repetition_recall` | triage | 2026-10-31 | 2026-11-13 | Updated installed workflow at9048f36a completed add/review/build with prior curator decisions retained. Local commits 90e77a7c and 3be188a7; container 01a1ae4b-07ce-7d55-b885-f6b11cb52d72. Same accepted checksum/data/splits; reload and traced-input reproduction pass, zero errors/warnings. Native review records explicit retention with original marks preserved. Train-only, own-row prediction protocol stays required; downstream method checks remain unverified. Not pushed or submitted; retain Myunghwan ownership pending integration, existing stage preserved. |
| `economic_well_being_prediction_challenge` | triage | 2026-10-28 | 2026-11-11 | Curator ship accepted. Local build, reload and traced-input reproduction verified (2026-11-03); temporal x unseen-country, 21,454 rows, 16 evaluations. Local branch prepared separately; intentionally not added to existing PR. Retain ownership pending separately authorized publication/integration. |
| `fannie_mae_single_family_loan_performance` | triage | 2026-10-31 | 2026-11-07 | Curator-requested triage of PR39 priority-4 candidates with 10M+ source observations. |
| `football_match_probability_prediction` | triage | 2026-11-05 | 2026-11-12 | Curator-requested triage: priority-4 interaction datasets; scale, source and non-IID qualification pending. |
| `fugaku_hpc_job_failure` | add | 2026-11-03 | 2026-11-13 | Curator decisions reused; maintained installation 9048f36a repeat add/review/build cycle complete. Built/reloaded/minimal-input reproduction and existing backup of 43 input files freshly reverified; unchanged task with 2,500,499 rows and 388 predictors. Local commits c84f9b39 and 6b4bea76 on fugaku-skill-refresh-20261106; not pushed. Retain ownership pending upstream integration. First tuned benchmark family, baseline, probability and maturity/latency recheck remains required; known diagnostic limits retained. |
| `geoai_ground_level_no2_estimation_challenge` | triage | 2026-10-28 | 2026-11-06 | Curator accepted as implemented with documented label-QC, regional and observed-day coverage limits. Built and verified: 82,051 rows, 11 predictors, station-held-out 3x3 folds; reload and traced-input reproduction passed with zero warnings. Local commits 7b2837b and 8cba4df on geoai-no2-curation; not pushed or submitted. Retain Myunghwan ownership pending upstream integration; existing stage preserved by gateway. |
| `loan_default_prediction_challenge` | triage | 2026-10-28 | 2026-11-11 | Myunghwan: requested single-candidate SuperLender source screening; no benchmark control plane |
| `lt_vehicle_loan_default_prediction` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `medical_facility_operational_data` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `meituan_food_delivery_time` | triage | 2026-11-05 | 2026-11-12 | Curator-requested triage: priority-4 interaction datasets; scale, source and non-IID qualification pending. |
| `open_soil_spectral_library` | review | 2026-10-23 | 2026-11-04 (expired) | Screening accepted; add-stage qualification completed. Added-dataset review or approved pre-build work; individual scientific verdicts remain separate. No build authorized. |
| `protein_model_quality_rf_pcp` | review | 2026-10-28 | 2026-11-06 | Curator accepted; build, reload and traced-input reproduction complete. Submitted in PR #33: https://github.com/TabArena/data-foundry/pull/33 . Accepted approximations and source/descriptor limits are documented. Awaiting PR review/merge; retain Myunghwan ownership until merged. |
| `sendy_logistics_challenge` | review | 2026-10-28 | 2026-11-06 | Curator ship accepted; build and verification complete. Submitted in PR #33: https://github.com/TabArena/data-foundry/pull/33 (commit 46e8b32). Placement-to-arrival RMSE; 21,199 rows, 13 predictors, random 3x3 folds. Awaiting PR review/merge; retain Myunghwan ownership until merged. |
| `tunisian_fraud_detection_challenge` | triage | 2026-10-28 | 2026-11-04 (expired) | Next Myunghwan curation batch: highest remaining eligible priority 3; existing screening dossiers await curator review. Reservation only; no scientific acceptance or build. |
| `xuetangx_mooc_dropout` | triage | 2026-11-05 | 2026-11-12 | Curator-requested triage: priority-4 interaction datasets; scale, source and non-IID qualification pending. |
