# TabArena-v0.2 Curation Overview

Working setup towards TabArena-v0.2: one v2 folder (`dataset.py` and a generated `README.md`) per dataset.

- **New here?** [`GETTING_STARTED.md`](GETTING_STARTED.md): set-up, the two workflows (settling a record, adding a
  dataset) and the large-data candidates to start with.
- **Every change is logged** in [`CHANGELOG.md`](CHANGELOG.md): edits, added or removed files, re-runs that change a
  container.
- Changes the benchmark harness (TabArena) needs for these datasets, for example scoring grouped tasks per group, are
  in [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).
- Each dataset folder has a `README.md` that `.venv/bin/python -m data_foundry.curation.cli dataset check` generates
  from its `dataset.py`: links to the curation record and the source, how to rebuild, and the evidence.
- Open questions for the curator are in a folder's `REVIEW.md` while they are open (the review page of
  `/review-added-datasets` is built from them); settled decisions are in the curation records
  (`curation/records/<name>.md`), the definitions and the `CHANGELOG.md` entries. How curation works here: the
  knowledge skills [`knowledge-curation`](../../../.claude/skills/knowledge-curation/SKILL.md) and
  [`knowledge-data-foundry`](../../../.claude/skills/knowledge-data-foundry/SKILL.md).

## Rebuild

- Publication metadata refresh, 2026-10-29: beMTPL97, Tanzania tourism and CPS88 wages were rebuilt after removing acquisition/process details from descriptions. Reload and single-input reproduction pass for each. Every row, target, scoring semantics and all nine folds remain identical; only metadata changes their checksums. The table points to the new UUIDs; previous versions and the other nine dataset builds are preserved.

- Scoped build, 2026-10-29: Sendy Logistics adds 21,199 rows, 13 predictors and 3 x 3 random folds as format-2 UUID `01a18a16-1f77-7fc2-b293-c8d8ca2eeefc`, built from clean source `b58e9ac9185941edb42d19f681fe534aad8ec734`. Reload and reproduction from its single traced `Train.csv` (4,094,263 bytes) pass with the accepted checksum. Reviewed rows and all nine folds match exactly, with zero build errors or warnings. Raw-input backup remains local.

- Scoped build, 2026-10-29: Chicago Traffic Crashes adds a format-2 container, UUID `01a18a0b-6aa8-726f-a33a-75044860edbf`, with 1,097,209 rows, 21 predictors and nine quarterly tests. Saved reload and reconstruction from its single frozen CSV reproduce the accepted checksum, with no unaccepted warnings. Its native build records the original uncommitted working tree; the exact source snapshot is retained locally. The existing ten dataset build records below are preserved.

- Scoped build, 2026-10-28 (2026-10-29 UTC): ten Myunghwan-accepted datasets built as format-2 containers from clean source `6d189a922994ddb0221c8249d07552d4df8af88b`. All ten saved containers verified on reload, and checks from a warehouse containing only the 15 traced raw files (1,303,769,410 bytes) reproduced every checksum. These ten retain the exact accepted data and splits; the other definitions were not rebuilt. The local raw-input backup `tabarena-v0pt2-ten-raw-inputs-2026-10-28.zip` stays outside Git.

- The raw files come from `local-data-warehouse/` (or `$DATA_FOUNDRY_WAREHOUSE`); each folder's `README.md` gives the
  download command.
- To rebuild, ask Claude; it follows
  [`rebuild.md`](../../../.claude/skills/knowledge-data-foundry/references/rebuild.md).
- Build with the `build` extra installed (the repository's `.venv` has it). scikit-learn must stay below 1.8, which
  changes the grouped splits. Rows and splits are the same on every machine, but a numpy log or exp can differ in its
  last bit between CPUs, so compare checksums on one machine.
- `.claude/skills/knowledge-data-foundry/scripts/task_probes.py --all --built` sweeps the built containers against
  dummy baselines (answer its flags with
  [`task_probes.md`](../../../.claude/skills/knowledge-curation/references/task_probes.md)), and
  `.claude/skills/knowledge-data-foundry/scripts/group_probes.py <name>` probes a grouped task.

<!-- datasets:start -->
| dataset | regime | rows | features | splits | UUID | open warnings |
|---|---|---|---|---|---|---|
| [`2_month_survival_rate_prediction`](2_month_survival_rate_prediction/) | IID | 8,967 | 22 | 3 x 3 | not built |  |
| [`5g_energy_consumption`](5g_energy_consumption/) | grouped | 92,629 | 20 | 3 x 3 | not built |  |
| [`account_debt_south_africa`](account_debt_south_africa/) | IID | 101,686 | 7 | 3 x 3 | not built |  |
| [`acquire_valued_shoppers_challenge`](acquire_valued_shoppers_challenge/) | temporal | 160,057 | 111 | 5 x 1 | not built |  |
| [`aeolus_rebuilt_1m`](aeolus_rebuilt_1m/) | temporal | 1,799,254 | 34 | 3 x 1 | not built |  |
| [`african_credit_scoring_challenge`](african_credit_scoring_challenge/) | temporal | 52,826 | 8 | 6 x 1 | not built |  |
| [`ai4d_lab_tanzania_tourism_classification_challenge`](ai4d_lab_tanzania_tourism_classification_challenge/) | IID | 18,506 | 19 | 3 x 3 | `01a18ad4-f6a0-759d-a526-da34a2568066` |  |
| [`airfoil_self_noise`](airfoil_self_noise/) | grouped | 1,503 | 5 | 10 x 3 | not built |  |
| [`airqo_low_cost_air_quality_monitor_calibration_challenge`](airqo_low_cost_air_quality_monitor_calibration_challenge/) | IID | 10,932 | 16 | 3 x 3 | `01a18629-ab5f-784f-9679-a007fd54c98a` |  |
| [`alfa_battle_2_0_task_2`](alfa_battle_2_0_task_2/) | temporal | 963,811 | 510 | 3 x 1 | not built |  |
| [`allstate_claims_severity`](allstate_claims_severity/) | IID | 188,317 | 130 | 3 x 3 | not built |  |
| [`amazon_employee_access`](amazon_employee_access/) | IID | 32,769 | 9 | 3 x 3 | not built | `dataset_pure_feature_value` |
| [`ames_housing`](ames_housing/) | temporal | 2,837 | 78 | 13 x 1 | not built |  |
| [`amex_non_iid_1m`](amex_non_iid_1m/) | grouped (per group: last) | 1,500,000 | 189 | 1 x 3 | not built | `dataset_missing_value_sentinel` |
| [`anes_voting_2026`](anes_voting_2026/) | temporal | 48,587 | 261 | 9 x 1 | not built |  |
| [`apistox`](apistox/) | temporal | 1,035 | 204 | 4 x 1 | not built |  |
| [`aps_failure`](aps_failure/) | IID | 76,000 | 170 | 3 x 3 | not built | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`ashrae_great_energy_predictor_iii_1m`](ashrae_great_energy_predictor_iii_1m/) | temporal | 2,500,000 | 15 | 3 x 1 | not built |  |
| [`asp_potassco_classification`](asp_potassco_classification/) | grouped | 1,212 | 136 | 10 x 3 | not built | `dataset_constant_column` |
| [`audiology_diagnosis`](audiology_diagnosis/) | IID | 195 | 65 | 20 x 3 | not built |  |
| [`bad_customer_detection`](bad_customer_detection/) | IID | 1,723 | 13 | 10 x 3 | not built |  |
| [`bank_customer_churn`](bank_customer_churn/) | IID | 10,000 | 10 | 3 x 3 | not built |  |
| [`bank_marketing`](bank_marketing/) | IID | 45,211 | 13 | 3 x 3 | not built | `dataset_missing_value_sentinel` |
| [`bemtpl97`](bemtpl97/) | IID | 163,212 | 13 | 3 x 3 | `01a18ad7-0bb6-7938-bc7e-98a4b50a8804` |  |
| [`bias_correction_r_bias_correction_r_2`](bias_correction_r_bias_correction_r_2/) | temporal | 7,648 | 23 | 9 x 1 | not built |  |
| [`biogeographical_ancestry_prediction`](biogeographical_ancestry_prediction/) | IID | 607 | 102 | 20 x 3 | not built |  |
| [`biomechanical_orthopaedic_prediction`](biomechanical_orthopaedic_prediction/) | IID | 310 | 6 | 20 x 3 | not built |  |
| [`bioresponse`](bioresponse/) | IID | 3,751 | 1,776 | 3 x 3 | not built |  |
| [`blood_tests_drink_prediction`](blood_tests_drink_prediction/) | IID | 345 | 5 | 20 x 3 | not built | `dataset_duplicate_rows` |
| [`blood_transfusion`](blood_transfusion/) | IID | 748 | 4 | 20 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`body_density_prediction`](body_density_prediction/) | IID | 252 | 13 | 20 x 3 | not built |  |
| [`brazilian_ecommerce`](brazilian_ecommerce/) | temporal | 88,721 | 24 | 5 x 1 | not built |  |
| [`breast_cancer_prediction`](breast_cancer_prediction/) | IID | 36,714 | 10 | 3 x 3 | not built |  |
| [`california_house_prices_2020`](california_house_prices_2020/) | temporal | 39,060 | 41 | 3 x 1 | not built |  |
| [`caracas_cervical_cancer`](caracas_cervical_cancer/) | IID | 750 | 30 | 10 x 3 | not built |  |
| [`cardiotocography`](cardiotocography/) | grouped | 2,126 | 22 | 10 x 3 | not built | `dataset_constant_column` |
| [`chicago_traffic_crashes_1m`](chicago_traffic_crashes_1m/) | temporal | 1,097,209 | 21 | 9 x 1 | `01a18a0b-6aa8-726f-a33a-75044860edbf` |  |
| [`churn_telco_south_asia`](churn_telco_south_asia/) | IID | 2,000 | 13 | 10 x 3 | not built |  |
| [`cirrhosis_patient_survival_prediction`](cirrhosis_patient_survival_prediction/) | IID | 304 | 17 | 20 x 3 | not built |  |
| [`climate_model_weather_forecasting_1m`](climate_model_weather_forecasting_1m/) | temporal | 2,115,283 | 99 | 3 x 1 | not built |  |
| [`clock_protein_toxicity`](clock_protein_toxicity/) | IID | 171 | 1,117 | 20 x 3 | not built |  |
| [`coffee_rating_prediction`](coffee_rating_prediction/) | temporal | 2,369 | 12 | 13 x 1 | not built | `dataset_constant_column` |
| [`coil_2000`](coil_2000/) | IID | 9,822 | 85 | 3 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`college_scorecard`](college_scorecard/) | temporal | 34,431 | 92 | 4 x 1 | not built |  |
| [`concrete_compressive_strength`](concrete_compressive_strength/) | grouped | 1,030 | 8 | 10 x 3 | not built | `dataset_duplicate_rows` |
| [`consumer_complaints_1m`](consumer_complaints_1m/) | temporal | 1,811,452 | 12 | 3 x 1 | not built |  |
| [`cooking_time_1m`](cooking_time_1m/) | temporal | 2,527,113 | 196 | 3 x 1 | not built |  |
| [`covertype`](covertype/) | IID | 581,012 | 14 | 1 x 3 | not built |  |
| [`cps88wages`](cps88wages/) | IID | 28,155 | 6 | 3 x 3 | `01a18ad7-7905-7c46-8544-db56a44113a9` |  |
| [`credit_approval`](credit_approval/) | IID | 690 | 15 | 20 x 3 | not built |  |
| [`credit_card_clients_default`](credit_card_clients_default/) | IID | 30,000 | 23 | 3 x 3 | not built |  |
| [`credit_g`](credit_g/) | IID | 1,000 | 20 | 10 x 3 | not built |  |
| [`dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction`](dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction/) | grouped | 2,431 | 266 | 10 x 3 | `01a18629-c3f0-7652-a9e8-57307772b909` |  |
| [`delivery_eta_1m`](delivery_eta_1m/) | temporal | 2,500,000 | 221 | 3 x 1 | not built |  |
| [`dementia_prediction`](dementia_prediction/) | grouped | 370 | 8 | 20 x 3 | not built |  |
| [`diabetes_130_us`](diabetes_130_us/) | IID | 69,973 | 44 | 3 x 3 | not built |  |
| [`diabetes_3`](diabetes_3/) | IID | 442 | 10 | 20 x 3 | not built |  |
| [`diamonds`](diamonds/) | IID | 53,940 | 9 | 3 x 3 | not built |  |
| [`differentiated_thyroid_cancer_recurrence`](differentiated_thyroid_cancer_recurrence/) | IID | 383 | 15 | 20 x 3 | not built |  |
| [`distribution_transformers_at_cauca_department`](distribution_transformers_at_cauca_department/) | IID | 15,873 | 12 | 3 x 3 | not built |  |
| [`drug_induced_autoimmunity_prediction`](drug_induced_autoimmunity_prediction/) | grouped | 587 | 176 | 20 x 3 | not built |  |
| [`early_learning_predictors`](early_learning_predictors/) | grouped | 18,874 | 743 | 3 x 3 | not built | `dataset_duplicate_columns` |
| [`early_stage_diabetes_risk_prediction`](early_stage_diabetes_risk_prediction/) | IID | 251 | 16 | 20 x 3 | not built |  |
| [`ecoli_proteins`](ecoli_proteins/) | IID | 327 | 6 | 20 x 3 | not built |  |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/) | grouped | 1,296,316 | 109 | 1 x 3 | not built |  |
| [`emscad`](emscad/) | grouped | 16,116 | 17 | 3 x 3 | not built |  |
| [`eryhemato_squamous_disease`](eryhemato_squamous_disease/) | IID | 366 | 12 | 20 x 3 | not built |  |
| [`eucalyptus`](eucalyptus/) | IID | 667 | 19 | 20 x 3 | `01a18629-c71c-7a73-af7a-c2b232f2a873` |  |
| [`expresso_churn_prediction_1m`](expresso_churn_prediction_1m/) | IID | 1,500,000 | 15 | 1 x 3 | not built |  |
| [`fiat_500`](fiat_500/) | IID | 1,434 | 7 | 10 x 3 | not built |  |
| [`food_delivery_time`](food_delivery_time/) | IID | 45,451 | 9 | 3 x 3 | not built |  |
| [`force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`](force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/) | grouped | 1,429,591 | 26 | 1 x 3 | not built |  |
| [`forensic_glass_identification`](forensic_glass_identification/) | IID | 214 | 9 | 20 x 3 | not built |  |
| [`forest_fires`](forest_fires/) | IID | 517 | 12 | 20 x 3 | not built | `dataset_conflicting_duplicate_rows` |
| [`framingham_heart_study_fhs`](framingham_heart_study_fhs/) | IID | 4,199 | 14 | 3 x 3 | not built |  |
| [`fraud_detection_in_electricity_and_gas_consumption_1m`](fraud_detection_in_electricity_and_gas_consumption_1m/) | grouped (per group: mean) | 1,500,000 | 17 | 1 x 3 | not built |  |
| [`g_research_crypto_forecasting_1m`](g_research_crypto_forecasting_1m/) | temporal | 2,499,998 | 27 | 3 x 1 | not built |  |
| [`gallstone_disease`](gallstone_disease/) | IID | 319 | 38 | 20 x 3 | not built |  |
| [`garments_worker_productivity`](garments_worker_productivity/) | temporal | 1,197 | 15 | 30 x 1 | not built |  |
| [`give_me_some_credit`](give_me_some_credit/) | IID | 150,000 | 10 | 3 x 3 | not built |  |
| [`heart_disease`](heart_disease/) | grouped | 796 | 13 | 1 x 3 | not built |  |
| [`heart_failure_followup_survival`](heart_failure_followup_survival/) | IID | 299 | 11 | 20 x 3 | not built |  |
| [`heloc`](heloc/) | IID | 10,459 | 23 | 3 x 3 | not built | `dataset_missing_value_sentinel`, `dataset_duplicate_rows` |
| [`hepatitis_c_prediction`](hepatitis_c_prediction/) | IID | 608 | 11 | 20 x 3 | not built |  |
| [`hepatitis_survival_prediction`](hepatitis_survival_prediction/) | IID | 155 | 19 | 20 x 3 | not built |  |
| [`hiva_agnostic`](hiva_agnostic/) | IID | 4,229 | 1,429 | 3 x 3 | not built |  |
| [`home_credit_default_risk`](home_credit_default_risk/) | IID | 307,507 | 709 | 3 x 3 | not built |  |
| [`home_credit_default_stability_1m`](home_credit_default_stability_1m/) | temporal | 1,224,927 | 710 | 3 x 1 | not built |  |
| [`homesite_quote_conversion`](homesite_quote_conversion/) | IID | 260,753 | 295 | 3 x 3 | not built | `dataset_constant_column`, `dataset_missing_value_label` |
| [`horse_colic_survival`](horse_colic_survival/) | IID | 344 | 20 | 20 x 3 | not built |  |
| [`hotel_booking_demand`](hotel_booking_demand/) | temporal | 81,418 | 28 | 9 x 1 | not built |  |
| [`house_sales`](house_sales/) | temporal | 20,499 | 20 | 9 x 1 | not built |  |
| [`houses`](houses/) | IID | 19,675 | 8 | 3 x 3 | not built |  |
| [`hr_analytics`](hr_analytics/) | IID | 18,359 | 12 | 3 x 3 | not built |  |
| [`huntprohibited_1m`](huntprohibited_1m/) | IID | 1,500,000 | 9 | 1 x 3 | not built |  |
| [`ieee_fraud_detection`](ieee_fraud_detection/) | temporal | 590,540 | 435 | 3 x 1 | not built |  |
| [`immoscout_german_house_prices`](immoscout_german_house_prices/) | IID | 10,317 | 23 | 3 x 3 | not built |  |
| [`in_vehicle_coupon_recommendation`](in_vehicle_coupon_recommendation/) | grouped | 12,684 | 24 | 3 x 3 | not built |  |
| [`indian_liver_patient_dataset`](indian_liver_patient_dataset/) | IID | 583 | 10 | 20 x 3 | not built | `dataset_duplicate_rows` |
| [`infrared_thermography_temperature`](infrared_thermography_temperature/) | IID | 1,001 | 35 | 10 x 3 | not built |  |
| [`jm1`](jm1/) | IID | 8,736 | 21 | 3 x 3 | not built |  |
| [`kdd_cup_09_appetency`](kdd_cup_09_appetency/) | IID | 50,000 | 212 | 3 x 3 | not built | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`kick`](kick/) | temporal | 72,983 | 28 | 9 x 1 | not built |  |
| [`kickstarter`](kickstarter/) | temporal | 187,117 | 12 | 3 x 1 | not built |  |
| [`labour_inspection_compliance`](labour_inspection_compliance/) | IID | 63,634 | 376 | 3 x 3 | not built | `dataset_constant_column` |
| [`lending_club`](lending_club/) | temporal | 609,544 | 81 | 3 x 1 | not built |  |
| [`ljubljana_breast_cancer`](ljubljana_breast_cancer/) | IID | 286 | 9 | 20 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`ljubljana_primary_tumor`](ljubljana_primary_tumor/) | IID | 302 | 17 | 20 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`lt_vehicle_loan_default_prediction`](lt_vehicle_loan_default_prediction/) | temporal | 233,154 | 38 | 9 x 1 | `01a18629-d0b7-7fd8-822e-8e4ecd7e315f` |  |
| [`lung_cancer`](lung_cancer/) | IID | 197 | 12,600 | 20 x 3 | not built | `dataset_missing_value_sentinel` |
| [`lung_cancer_epithelial_genexp`](lung_cancer_epithelial_genexp/) | IID | 187 | 22,215 | 20 x 3 | not built |  |
| [`maps_router_eta_1m`](maps_router_eta_1m/) | temporal | 2,535,166 | 988 | 3 x 1 | not built |  |
| [`marketing_campaign`](marketing_campaign/) | IID | 2,240 | 25 | 10 x 3 | not built | `dataset_duplicate_rows` |
| [`medical_facility_operational_data`](medical_facility_operational_data/) | temporal | 130,431 | 88 | 9 x 1 | `01a18629-f249-7ee4-b713-033fd2de1d79` |  |
| [`melbourne_housing_market`](melbourne_housing_market/) | temporal | 21,266 | 19 | 9 x 1 | not built |  |
| [`mercari_price_suggestion`](mercari_price_suggestion/) | IID | 1,482,486 | 6 | 1 x 3 | not built |  |
| [`mercedes_benz_greener_manufacturing`](mercedes_benz_greener_manufacturing/) | temporal | 4,204 | 371 | 9 x 1 | not built | `dataset_constant_column`, `dataset_duplicate_columns` |
| [`miami_housing`](miami_housing/) | IID | 13,776 | 15 | 3 x 3 | not built |  |
| [`mic`](mic/) | IID | 1,700 | 102 | 10 x 3 | not built |  |
| [`micro_mass`](micro_mass/) | grouped | 571 | 1,082 | 20 x 3 | not built |  |
| [`mobile_churn`](mobile_churn/) | IID | 54,207 | 57 | 3 x 3 | not built |  |
| [`mortgage`](mortgage/) | temporal | 621,653 | 21 | 3 x 1 | not built |  |
| [`musk`](musk/) | grouped (per group: any) | 6,598 | 166 | 20 x 3 | not built | `dataset_missing_value_sentinel` |
| [`naticusdroid_android_permissions_dataset`](naticusdroid_android_permissions_dataset/) | IID | 7,491 | 85 | 3 x 3 | not built | `dataset_conflicting_duplicate_rows`, `dataset_pure_feature_value` |
| [`numerai28_6`](numerai28_6/) | IID | 96,320 | 21 | 3 x 3 | not built |  |
| [`numerai_v5_2_1m`](numerai_v5_2_1m/) | temporal | 2,025,745 | 2,377 | 3 x 1 | not built |  |
| [`nyc_taxi_trip_duration_1m`](nyc_taxi_trip_duration_1m/) | temporal | 1,165,967 | 7 | 3 x 1 | not built |  |
| [`obesity_estimation`](obesity_estimation/) | IID | 488 | 14 | 20 x 3 | not built |  |
| [`online_shoppers_purchasing_intention_dataset`](online_shoppers_purchasing_intention_dataset/) | IID | 6,875 | 16 | 3 x 3 | not built |  |
| [`onlinenewspopularity`](onlinenewspopularity/) | temporal | 39,643 | 39 | 9 x 1 | not built |  |
| [`open_soil_spectral_library`](open_soil_spectral_library/) | grouped | 75,929 | 1,701 | 3 x 3 | `01a1862b-1d5c-7d64-a5ce-76cc983104eb` |  |
| [`open_university_learning_analytics_dataset`](open_university_learning_analytics_dataset/) | grouped | 26,395 | 40 | 3 x 3 | not built |  |
| [`otto_group_product_classification_challenge`](otto_group_product_classification_challenge/) | IID | 61,878 | 93 | 3 x 3 | not built |  |
| [`pancreatic_cancer_mouse_detection`](pancreatic_cancer_mouse_detection/) | grouped | 181 | 6,771 | 20 x 3 | not built | `dataset_missing_value_sentinel` |
| [`perth_house_prices`](perth_house_prices/) | temporal | 33,090 | 19 | 9 x 1 | not built |  |
| [`pkdd_15_taxi_trip_time_prediction_ii_1m`](pkdd_15_taxi_trip_time_prediction_ii_1m/) | temporal | 1,429,426 | 8 | 3 x 1 | not built |  |
| [`polish_companies_bankruptcy`](polish_companies_bankruptcy/) | IID | 5,790 | 64 | 3 x 3 | not built |  |
| [`porto_seguro`](porto_seguro/) | IID | 595,206 | 37 | 1 x 3 | not built |  |
| [`predict_students_dropout_and_academic_success`](predict_students_dropout_and_academic_success/) | IID | 4,424 | 36 | 3 x 3 | not built |  |
| [`predictive_insights_youth_income_prediction_challenge`](predictive_insights_youth_income_prediction_challenge/) | IID | 4,017 | 18 | 3 x 3 | `01a1862a-0d79-7de6-a2a3-5d6010bcefe5` |  |
| [`pva_revenue_prediction_kddcup98`](pva_revenue_prediction_kddcup98/) | IID | 191,769 | 477 | 3 x 3 | not built | `dataset_constant_column`, `dataset_missing_value_label`, `meta_license_unknown` |
| [`qsar_aquatic_toxicity`](qsar_aquatic_toxicity/) | IID | 546 | 8 | 20 x 3 | not built | `dataset_conflicting_duplicate_rows` |
| [`qsar_bioconcentration`](qsar_bioconcentration/) | grouped | 776 | 195 | 10 x 3 | not built |  |
| [`qsar_biodeg`](qsar_biodeg/) | IID | 1,055 | 41 | 10 x 3 | not built |  |
| [`qsar_fish_toxicity`](qsar_fish_toxicity/) | IID | 908 | 6 | 10 x 3 | not built | `dataset_conflicting_duplicate_rows` |
| [`qsar_oral_toxicity`](qsar_oral_toxicity/) | grouped | 11,105 | 1,232 | 3 x 3 | not built |  |
| [`qsar_tid_11`](qsar_tid_11/) | IID | 5,704 | 1,024 | 3 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`rain_in_australia`](rain_in_australia/) | temporal | 264,562 | 165 | 26 x 1 | not built |  |
| [`regensburg_pediatric_appendicitis`](regensburg_pediatric_appendicitis/) | IID | 763 | 51 | 10 x 3 | not built |  |
| [`rosbank1`](rosbank1/) | temporal | 4,791 | 695 | 3 x 1 | not built |  |
| [`rossmann_store_sales`](rossmann_store_sales/) | temporal | 844,392 | 15 | 3 x 1 | not built |  |
| [`santander_customer_satisfaction`](santander_customer_satisfaction/) | IID | 71,080 | 307 | 3 x 3 | not built | `dataset_pure_feature_value` |
| [`santander_customer_transaction_prediction`](santander_customer_transaction_prediction/) | IID | 200,000 | 200 | 3 x 3 | not built |  |
| [`santander_transaction_value`](santander_transaction_value/) | IID | 4,447 | 540 | 3 x 3 | not built |  |
| [`sarcoma`](sarcoma/) | IID | 201 | 25,910 | 20 x 3 | not built |  |
| [`sat11_hand_algo_runtime`](sat11_hand_algo_runtime/) | grouped (per group: select_min) | 1,840 | 169 | 10 x 3 | not built | `dataset_constant_column` |
| [`sberbank_housing_market_forecasting`](sberbank_housing_market_forecasting/) | temporal | 28,321 | 386 | 5 x 1 | not built |  |
| [`sdss_17`](sdss_17/) | IID | 99,999 | 8 | 3 x 3 | not built |  |
| [`sendy_logistics_challenge`](sendy_logistics_challenge/) | IID | 21,199 | 13 | 3 x 3 | `01a18a16-1f77-7fc2-b293-c8d8ca2eeefc` |  |
| [`sepsis_prediction_1m`](sepsis_prediction_1m/) | grouped | 1,499,997 | 42 | 1 x 3 | not built |  |
| [`sepsis_survival_minimal_clinical_records`](sepsis_survival_minimal_clinical_records/) | IID | 110,204 | 3 | 3 x 3 | not built | `dataset_duplicate_rows` |
| [`sf_permit_time`](sf_permit_time/) | temporal | 99,847 | 37 | 8 x 1 | not built |  |
| [`south_africa_coronary_heart_disease`](south_africa_coronary_heart_disease/) | IID | 462 | 9 | 20 x 3 | not built |  |
| [`splice`](splice/) | IID | 3,190 | 60 | 10 x 3 | not built | `dataset_duplicate_rows` |
| [`student_portuguese_performance`](student_portuguese_performance/) | IID | 649 | 30 | 20 x 3 | not built |  |
| [`superconductivity`](superconductivity/) | grouped | 21,263 | 81 | 3 x 3 | not built | `dataset_conflicting_duplicate_rows` |
| [`taiwanese_bankruptcy_prediction`](taiwanese_bankruptcy_prediction/) | IID | 6,819 | 92 | 3 x 3 | not built |  |
| [`thyroid_discordant`](thyroid_discordant/) | IID | 3,711 | 26 | 10 x 3 | not built |  |
| [`tour_travels_churn`](tour_travels_churn/) | IID | 954 | 6 | 10 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows`, `meta_bibtex_latex_hazard` |
| [`video_transcoding_time_prediction`](video_transcoding_time_prediction/) | grouped | 68,784 | 18 | 3 x 3 | not built |  |
| [`website_phishing`](website_phishing/) | IID | 1,250 | 9 | 10 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`wids_diabetes_mellitus`](wids_diabetes_mellitus/) | IID | 127,358 | 181 | 3 x 3 | not built |  |
| [`wine_quality`](wine_quality/) | IID | 5,320 | 12 | 3 x 3 | not built |  |
| [`wine_world_cost`](wine_world_cost/) | IID | 1,279 | 14 | 10 x 3 | not built |  |
| [`zillow_prize`](zillow_prize/) | temporal | 153,108 | 55 | 9 x 1 | not built |  |
<!-- datasets:end -->
