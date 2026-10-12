# TabArena-v0.2  Curation Overview

Working setup towards TabArena-v0.2

- **New here?** [`GETTING_STARTED.md`](GETTING_STARTED.md): set-up, the two workflows (settling a record, adding a
  dataset) and the large-data candidates to start with.
- **Every change is logged** in [`CHANGELOG.md`](CHANGELOG.md): edits, added or removed files, re-runs that change a container.
- The leak audit of September-October 2026 (removed and changed datasets, with severity) is summarised in [`LEAK_AUDIT.md`](LEAK_AUDIT.md).
- Changes the benchmark harness (TabArena) needs for these datasets, for example scoring grouped tasks per group, are in [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).
- Each dataset folder has a `README.md` that `.venv/bin/python -m data_foundry.curation.cli dataset check` generates from its `dataset.py`: the folder's files, links to the curation record and the source, how to rebuild, the evidence and the build record.
- Open decisions are in the curation records (`curation/records/<name>.md`) and in the newest `CHANGELOG.md` entries.
- 59 definitions added on 2026-10-07 from the curation backlog are not built yet; their issues and the decisions they
  need are in [`NEW_DATASETS_ISSUES.md`](NEW_DATASETS_ISSUES.md).

## Rebuild

The 125 datasets were built on 2026-10-06 from the definitions in this folder (the UUIDs below), as container
format 2 (`container.format_version == 2`). The 59 definitions added on 2026-10-07 are not built yet ("not built"
in the table). To rebuild one, from the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/<name>   # no save; rewrites README.md
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/<name>   # saves a new container and UUID
```

- The raw files come from `local-data-warehouse/` (or `$DATA_FOUNDRY_WAREHOUSE`); each `README.md` gives the download
  command. The rebuild read 433 raw files (67 GB, traced per dataset); rebuilding every dataset from a warehouse that
  holds only those files gives the same checksums. The two `_prepare_raw_files` steps read 33 more (4.4 GB). A backup
  of these, with a manifest, is kept outside the repository (made on 2026-10-02; it also holds the inputs of the
  retired telemonitoring, fitness_club and parkinsons datasets).
- To rebuild the whole folder, with the comparison against the previous build, the check from the traced inputs, the
  backup and this table, follow the `/rebuild-working-copy` skill
  ([`.claude/skills/rebuild-working-copy/SKILL.md`](../../../.claude/skills/rebuild-working-copy/SKILL.md)).
- Build with the `build` extra installed (the repository's `.venv` has it). pandas 2.3 and pandas 3 give the same
  containers (checked on all datasets on 2026-10-06), and scikit-learn must stay below 1.8, which changes the grouped
  splits. The rows and splits are the same on every machine; a numpy log or exp can differ in its last bit between
  CPUs, so a dataset with a log-scaled target may get another checksum elsewhere.
- `.claude/skills/verify-dataset/scripts/task_probes.py --all --built` sweeps the built containers against dummy baselines (answer its flags with
  `.claude/skills/verify-dataset/references/task_probes.md`; the decisions on this build are in the records and
  `CHANGELOG.md`), and
  `.claude/skills/verify-dataset/scripts/group_probes.py <name>` probes a grouped task.

## Datasets

The v0.2 build of 2026-10-02: regime (with the group-level unit where a task is scored per group), size, outer
splits (repeats x folds; temporal tasks have one fold per window), the container's UUID, and the warnings that are
not accepted in the definition.

<!-- datasets:start -->
| dataset | regime | rows | features | splits | UUID | open warnings |
|---|---|---|---|---|---|---|
| [`2_month_survival_rate_prediction`](2_month_survival_rate_prediction/) | IID | 8,967 | 25 | 3 x 3 | not built |  |
| [`5g_energy_consumption`](5g_energy_consumption/) | grouped | 92,629 | 20 | 3 x 3 | not built |  |
| [`account_debt_south_africa`](account_debt_south_africa/) | IID | 101,871 | 7 | 3 x 3 | not built |  |
| [`acquire_valued_shoppers_challenge`](acquire_valued_shoppers_challenge/) | temporal | 160,057 | 111 | 5 x 1 | `01a111fd-7588-73e4-bf55-26fb6336c1f4` |  |
| [`aeolus_1m`](aeolus_1m/) | temporal | 1,387,518 | 18 | 3 x 1 | not built |  |
| [`african_credit_scoring_challenge`](african_credit_scoring_challenge/) | temporal | 58,953 | 11 | 9 x 1 | not built |  |
| [`airfoil_self_noise`](airfoil_self_noise/) | grouped | 1,503 | 5 | 10 x 3 | not built |  |
| [`alfa_battle_2_0_task_2`](alfa_battle_2_0_task_2/) | temporal | 963,811 | 127 | 3 x 1 | not built |  |
| [`allstate_claims_severity`](allstate_claims_severity/) | IID | 188,317 | 130 | 3 x 3 | `01a111fc-59f8-730c-b058-7264a71a29bc` |  |
| [`alvin_smart_money_management_classification_challenge`](alvin_smart_money_management_classification_challenge/) | temporal | 350 | 9 | 3 x 1 | not built |  |
| [`amazon_employee_access`](amazon_employee_access/) | IID | 32,769 | 9 | 3 x 3 | not built | `dataset_pure_feature_value` |
| [`amex_non_iid_1m`](amex_non_iid_1m/) | grouped (per group: last) | 1,500,000 | 189 | 1 x 3 | `01a111fb-d73e-711b-a490-c684c5c4635d` | `dataset_missing_value_sentinel` |
| [`analcatdata_supreme`](analcatdata_supreme/) | IID | 4,052 | 7 | 3 x 3 | not built |  |
| [`anes_voting_2026`](anes_voting_2026/) | temporal | 48,587 | 261 | 9 x 1 | `01a111fb-cb34-797a-ba46-5305a0c33af4` |  |
| [`apistox`](apistox/) | temporal | 1,035 | 205 | 4 x 1 | not built |  |
| [`aps_failure`](aps_failure/) | IID | 76,000 | 170 | 3 x 3 | `01a111fc-0ce6-78ed-a870-52ce14ff98d0` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`ashrae_great_energy_predictor_iii_1m`](ashrae_great_energy_predictor_iii_1m/) | temporal | 2,500,000 | 15 | 3 x 1 | not built |  |
| [`asp_potassco_classification`](asp_potassco_classification/) | grouped | 1,212 | 136 | 10 x 3 | `01a111fc-9534-79ba-a1c0-efe7268f38e0` | `dataset_constant_column` |
| [`audiology_diagnosis`](audiology_diagnosis/) | IID | 195 | 65 | 20 x 3 | `01a111fc-c395-7cc5-9b60-91d8a7afaa20` |  |
| [`bad_customer_detection`](bad_customer_detection/) | IID | 1,723 | 13 | 10 x 3 | `01a111fc-c415-7ef4-a2b9-d98a1d4aa9f8` |  |
| [`bank_customer_churn`](bank_customer_churn/) | IID | 10,000 | 10 | 3 x 3 | `01a111fc-c45b-7b5e-b6fe-7f527899d692` |  |
| [`bank_marketing`](bank_marketing/) | IID | 45,211 | 13 | 3 x 3 | `01a111fc-7c2d-7441-b859-646c9bfbf380` | `dataset_missing_value_sentinel` |
| [`bias_correction_r_bias_correction_r_2`](bias_correction_r_bias_correction_r_2/) | temporal | 7,723 | 23 | 9 x 1 | not built |  |
| [`biogeographical_ancestry_prediction`](biogeographical_ancestry_prediction/) | IID | 607 | 102 | 20 x 3 | not built |  |
| [`biomechanical_orthopaedic_prediction`](biomechanical_orthopaedic_prediction/) | IID | 310 | 6 | 20 x 3 | `01a111fc-c9b3-7a87-ad18-98510a3fb2b1` |  |
| [`bioresponse`](bioresponse/) | IID | 3,751 | 1,776 | 3 x 3 | `01a111fc-4c0b-76f4-b01d-a4db8e120e35` |  |
| [`blood_tests_drink_prediction`](blood_tests_drink_prediction/) | IID | 345 | 5 | 20 x 3 | not built | `dataset_duplicate_rows` |
| [`blood_transfusion`](blood_transfusion/) | IID | 748 | 4 | 20 x 3 | `01a111fc-c9d3-70c1-ba1b-e4fe45899e78` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`body_density_prediction`](body_density_prediction/) | IID | 252 | 13 | 20 x 3 | not built |  |
| [`brazilian_ecommerce`](brazilian_ecommerce/) | temporal | 88,721 | 24 | 5 x 1 | not built |  |
| [`brca_breast_cancer`](brca_breast_cancer/) | IID | 381 | 5,864 | 20 x 3 | not built |  |
| [`breast_cancer_prediction`](breast_cancer_prediction/) | grouped | 39,998 | 10 | 3 x 3 | not built |  |
| [`california_house_prices_2020`](california_house_prices_2020/) | temporal | 41,528 | 41 | 3 x 1 | not built |  |
| [`caracas_cervical_cancer`](caracas_cervical_cancer/) | IID | 750 | 30 | 10 x 3 | not built |  |
| [`cardiotocography`](cardiotocography/) | grouped | 2,126 | 22 | 10 x 3 | `01a111fc-7d1e-7b12-8cc7-298d2fc12820` | `dataset_constant_column` |
| [`cdc_diabetes_health_indicators`](cdc_diabetes_health_indicators/) | IID | 253,680 | 21 | 3 x 3 | not built |  |
| [`central_international_medical_college_and_hospital_health_risk_prediction`](central_international_medical_college_and_hospital_health_risk_prediction/) | IID | 1,000 | 8 | 10 x 3 | not built |  |
| [`churn_telco_south_asia`](churn_telco_south_asia/) | IID | 2,000 | 13 | 10 x 3 | not built |  |
| [`cirrhosis_patient_survival_prediction`](cirrhosis_patient_survival_prediction/) | IID | 161 | 17 | 20 x 3 | not built |  |
| [`climate_model_weather_forecasting_1m`](climate_model_weather_forecasting_1m/) | temporal | 2,115,283 | 99 | 3 x 1 | `01a111fb-bc63-7614-a137-a3fd390bc4f1` |  |
| [`clock_protein_toxicity`](clock_protein_toxicity/) | IID | 171 | 1,117 | 20 x 3 | not built |  |
| [`coad_colon_adenocarcinoma`](coad_colon_adenocarcinoma/) | IID | 256 | 36,355 | 20 x 3 | not built |  |
| [`coffee_rating_prediction`](coffee_rating_prediction/) | temporal | 2,369 | 12 | 13 x 1 | not built | `dataset_constant_column` |
| [`coil_2000`](coil_2000/) | IID | 9,822 | 85 | 3 x 3 | `01a111fc-ceb4-7695-8b34-df7a285cfcb6` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`college_scorecard`](college_scorecard/) | temporal | 34,431 | 89 | 4 x 1 | not built |  |
| [`concrete_compressive_strength`](concrete_compressive_strength/) | IID | 1,030 | 8 | 10 x 3 | not built | `dataset_duplicate_rows` |
| [`consumer_complaints_1m`](consumer_complaints_1m/) | temporal | 1,811,452 | 12 | 3 x 1 | not built |  |
| [`cooking_time_1m`](cooking_time_1m/) | temporal | 2,500,000 | 196 | 3 x 1 | `01a111fc-29b5-72ce-95a1-e99f6874a4ee` |  |
| [`corporate_credit_rating`](corporate_credit_rating/) | grouped | 2,020 | 28 | 10 x 3 | not built |  |
| [`corporate_credit_rating_cat_data_set_ratings_raitings`](corporate_credit_rating_cat_data_set_ratings_raitings/) | IID | 197 | 6 | 20 x 3 | not built |  |
| [`covertype`](covertype/) | IID | 581,012 | 14 | 1 x 3 | `01a111fc-5b2f-72b3-983a-85ec312c2e8f` |  |
| [`credit_approval`](credit_approval/) | IID | 690 | 15 | 20 x 3 | `01a111fc-cedf-7a16-9575-fb28a8d57db5` |  |
| [`credit_card_clients_default`](credit_card_clients_default/) | IID | 30,000 | 23 | 3 x 3 | not built |  |
| [`credit_card_customers`](credit_card_customers/) | IID | 10,127 | 19 | 3 x 3 | not built |  |
| [`credit_g`](credit_g/) | IID | 1,000 | 20 | 10 x 3 | `01a111fc-cf4e-7841-a626-e0358b0042c6` |  |
| [`dataorg_financial_health_prediction_challenge`](dataorg_financial_health_prediction_challenge/) | IID | 7,674 | 37 | 3 x 3 | not built |  |
| [`delivery_eta_1m`](delivery_eta_1m/) | temporal | 2,500,000 | 221 | 3 x 1 | `01a111fc-e6b7-7547-8e7f-790705764eb1` |  |
| [`dementia_prediction`](dementia_prediction/) | grouped | 370 | 8 | 20 x 3 | not built |  |
| [`diabetes_130_us`](diabetes_130_us/) | IID | 69,973 | 44 | 3 x 3 | `01a111fc-82d1-7838-bf50-fa314882cfef` |  |
| [`diabetes_3`](diabetes_3/) | IID | 442 | 10 | 20 x 3 | not built |  |
| [`diamonds`](diamonds/) | IID | 53,940 | 9 | 3 x 3 | not built |  |
| [`differentiated_thyroid_cancer_recurrence`](differentiated_thyroid_cancer_recurrence/) | IID | 383 | 14 | 20 x 3 | not built |  |
| [`digicow_farmer_training_adoption_challenge`](digicow_farmer_training_adoption_challenge/) | temporal | 13,536 | 11 | 4 x 1 | not built |  |
| [`distribution_transformers_at_cauca_department`](distribution_transformers_at_cauca_department/) | IID | 15,873 | 14 | 3 x 3 | not built |  |
| [`drug_induced_autoimmunity_prediction`](drug_induced_autoimmunity_prediction/) | IID | 597 | 177 | 20 x 3 | `01a111fc-d491-7412-a5c5-884df72be349` | `dataset_identifier_column` |
| [`early_learning_predictors`](early_learning_predictors/) | grouped | 18,874 | 743 | 3 x 3 | not built | `dataset_duplicate_columns` |
| [`early_stage_diabetes_risk_prediction`](early_stage_diabetes_risk_prediction/) | IID | 251 | 16 | 20 x 3 | not built |  |
| [`ecoli_proteins`](ecoli_proteins/) | IID | 327 | 6 | 20 x 3 | `01a111fc-d4ff-7dda-987a-8119d986e5f1` |  |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/) | grouped | 1,296,316 | 109 | 1 x 3 | `01a111fb-0e27-7b57-8daa-3b40b8ba0e11` |  |
| [`emscad`](emscad/) | grouped | 16,116 | 17 | 3 x 3 | not built |  |
| [`eryhemato_squamous_disease`](eryhemato_squamous_disease/) | IID | 366 | 12 | 20 x 3 | not built |  |
| [`expresso_churn_prediction_1m`](expresso_churn_prediction_1m/) | IID | 1,500,000 | 15 | 1 x 3 | not built |  |
| [`fiat_500`](fiat_500/) | IID | 1,538 | 7 | 10 x 3 | `01a111fc-a2a5-7dc8-a4bd-97f6a8bb5780` | `dataset_duplicate_rows` |
| [`food_delivery_time`](food_delivery_time/) | IID | 45,451 | 9 | 3 x 3 | `01a111fc-d7f1-7b0c-9bd0-d3f8b8afcfae` |  |
| [`force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`](force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/) | grouped | 1,429,591 | 26 | 1 x 3 | not built |  |
| [`forensic_glass_identification`](forensic_glass_identification/) | IID | 214 | 9 | 20 x 3 | `01a111fc-a27d-7f21-999e-eb82f18aaf21` |  |
| [`forest_fires`](forest_fires/) | IID | 517 | 12 | 20 x 3 | `01a111fc-a4a0-72df-82ce-c3f0eed0000e` | `dataset_conflicting_duplicate_rows` |
| [`framingham_heart_study_fhs`](framingham_heart_study_fhs/) | IID | 4,224 | 15 | 3 x 3 | not built |  |
| [`fraud_detection_in_electricity_and_gas_consumption_1m`](fraud_detection_in_electricity_and_gas_consumption_1m/) | grouped (per group: mean) | 1,500,000 | 18 | 1 x 3 | not built |  |
| [`g_research_crypto_forecasting_1m`](g_research_crypto_forecasting_1m/) | temporal | 2,501,039 | 27 | 3 x 1 | not built |  |
| [`gallstone_disease`](gallstone_disease/) | IID | 319 | 38 | 20 x 3 | not built |  |
| [`garments_worker_productivity`](garments_worker_productivity/) | temporal | 1,197 | 15 | 30 x 1 | not built |  |
| [`give_me_some_credit`](give_me_some_credit/) | IID | 150,000 | 10 | 3 x 3 | `01a111fc-8c6a-7513-9b7c-cd856ad168b6` |  |
| [`glioblastoma`](glioblastoma/) | IID | 274 | 5,534 | 20 x 3 | not built |  |
| [`glioma_grading_clinical_and_mutation_features`](glioma_grading_clinical_and_mutation_features/) | IID | 862 | 23 | 10 x 3 | not built |  |
| [`heart_disease_cleveland`](heart_disease_cleveland/) | IID | 303 | 13 | 20 x 3 | not built |  |
| [`heart_disease_hungary`](heart_disease_hungary/) | IID | 294 | 13 | 20 x 3 | not built | `dataset_constant_column` |
| [`heart_disease_va_long_beach`](heart_disease_va_long_beach/) | IID | 200 | 13 | 20 x 3 | not built | `dataset_constant_column` |
| [`heart_failure_followup_survival`](heart_failure_followup_survival/) | IID | 299 | 11 | 20 x 3 | not built |  |
| [`heloc`](heloc/) | IID | 10,459 | 23 | 3 x 3 | not built | `dataset_missing_value_sentinel`, `dataset_duplicate_rows` |
| [`hepatitis_c_prediction`](hepatitis_c_prediction/) | IID | 608 | 11 | 20 x 3 | not built |  |
| [`hepatitis_survival_prediction`](hepatitis_survival_prediction/) | IID | 155 | 19 | 20 x 3 | not built |  |
| [`hiva_agnostic`](hiva_agnostic/) | IID | 3,845 | 1,518 | 3 x 3 | `01a111fc-4ac0-7d5e-ace0-8fd1e51ccbd8` | `dataset_pure_feature_value` |
| [`home_credit_default_risk`](home_credit_default_risk/) | IID | 307,507 | 504 | 3 x 3 | `01a111fb-c9a4-79ac-b807-b4b9dffd8068` |  |
| [`home_credit_default_stability_1m`](home_credit_default_stability_1m/) | temporal | 1,224,927 | 710 | 3 x 1 | not built |  |
| [`homesite_quote_conversion`](homesite_quote_conversion/) | IID | 260,753 | 295 | 3 x 3 | `01a111fc-15c3-7dfe-bf9e-39d8ab56f8f4` | `dataset_constant_column`, `dataset_missing_value_label` |
| [`horse_colic_survival`](horse_colic_survival/) | IID | 344 | 20 | 20 x 3 | `01a111fc-df0b-7d08-9ad5-3bfee18c9b55` |  |
| [`hotel_booking_demand`](hotel_booking_demand/) | temporal | 81,418 | 28 | 9 x 1 | not built |  |
| [`house_prices_nominal`](house_prices_nominal/) | temporal | 2,919 | 78 | 13 x 1 | not built |  |
| [`house_sales`](house_sales/) | temporal | 20,967 | 19 | 9 x 1 | not built |  |
| [`houses`](houses/) | IID | 19,675 | 8 | 3 x 3 | not built |  |
| [`hr_analytics`](hr_analytics/) | IID | 19,158 | 12 | 3 x 3 | not built |  |
| [`huntprohibited_1m`](huntprohibited_1m/) | IID | 1,500,000 | 9 | 1 x 3 | not built |  |
| [`ieee_fraud_detection`](ieee_fraud_detection/) | temporal | 590,540 | 435 | 3 x 1 | not built |  |
| [`immoscout_german_house_prices`](immoscout_german_house_prices/) | IID | 10,317 | 23 | 3 x 3 | `01a111fc-e1d2-7c5b-a5e9-bb8bb2b58ed9` |  |
| [`in_vehicle_coupon_recommendation`](in_vehicle_coupon_recommendation/) | grouped | 12,684 | 24 | 3 x 3 | not built |  |
| [`indian_liver_patient_dataset`](indian_liver_patient_dataset/) | IID | 583 | 10 | 20 x 3 | `01a111fc-e244-78f8-9686-1c2a0bf3b820` | `dataset_duplicate_rows` |
| [`infrared_thermography_temperature`](infrared_thermography_temperature/) | IID | 1,018 | 35 | 10 x 3 | not built |  |
| [`jm1`](jm1/) | IID | 8,736 | 21 | 3 x 3 | not built |  |
| [`kdd_cup_09_appetency`](kdd_cup_09_appetency/) | IID | 50,000 | 212 | 3 x 3 | not built | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`kick`](kick/) | temporal | 72,983 | 32 | 9 x 1 | `01a111fc-8ab4-7b2f-9955-2cc583c9e979` |  |
| [`kickstarter`](kickstarter/) | temporal | 187,117 | 12 | 3 x 1 | not built |  |
| [`labour_inspection_compliance`](labour_inspection_compliance/) | IID | 63,634 | 376 | 3 x 3 | not built | `dataset_constant_column` |
| [`lending_club`](lending_club/) | temporal | 609,544 | 81 | 3 x 1 | not built |  |
| [`lgd`](lgd/) | grouped | 2,545 | 2 | 10 x 3 | not built |  |
| [`lgg_low_grade_glioma`](lgg_low_grade_glioma/) | IID | 247 | 21,076 | 20 x 3 | not built |  |
| [`ljubljana_breast_cancer`](ljubljana_breast_cancer/) | IID | 286 | 9 | 20 x 3 | `01a111fc-e2f6-79bc-bc94-8e4779cb09a2` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`ljubljana_primary_tumor`](ljubljana_primary_tumor/) | IID | 302 | 17 | 20 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`lung_cancer`](lung_cancer/) | IID | 197 | 12,600 | 20 x 3 | `01a111fa-f2d2-7673-a757-142728cdfd4c` | `dataset_missing_value_sentinel` |
| [`lung_cancer_epithelial_genexp`](lung_cancer_epithelial_genexp/) | IID | 187 | 22,215 | 20 x 3 | `01a111fa-e441-7be0-b4cb-2b1c80c2c167` |  |
| [`maps_router_eta_1m`](maps_router_eta_1m/) | temporal | 2,500,000 | 988 | 3 x 1 | `01a111ff-5cb6-76bc-bc05-231ccdac19d0` |  |
| [`marketing_campaign`](marketing_campaign/) | IID | 2,240 | 25 | 10 x 3 | not built | `dataset_duplicate_rows` |
| [`melbourne_housing_market`](melbourne_housing_market/) | temporal | 21,266 | 19 | 9 x 1 | not built |  |
| [`mercari_price_suggestion`](mercari_price_suggestion/) | IID | 1,482,486 | 6 | 1 x 3 | not built |  |
| [`mercedes_benz_greener_manufacturing`](mercedes_benz_greener_manufacturing/) | temporal | 4,204 | 371 | 9 x 1 | not built | `dataset_constant_column`, `dataset_duplicate_columns`, `meta_tags_missing_regime` |
| [`miami_housing`](miami_housing/) | IID | 13,776 | 15 | 3 x 3 | not built |  |
| [`mic`](mic/) | IID | 1,700 | 102 | 10 x 3 | not built |  |
| [`micro_mass`](micro_mass/) | grouped | 571 | 1,082 | 20 x 3 | `01a111fc-8b57-73f7-bb59-b6d7ab7a6881` |  |
| [`mobile_churn`](mobile_churn/) | IID | 54,207 | 57 | 3 x 3 | not built |  |
| [`mortgage`](mortgage/) | temporal | 622,177 | 17 | 3 x 1 | not built |  |
| [`musk`](musk/) | grouped (per group: any) | 6,598 | 166 | 20 x 3 | not built | `dataset_missing_value_sentinel` |
| [`mutual_funds_india`](mutual_funds_india/) | IID | 793 | 11 | 10 x 3 | `01a111fc-b2ce-7d31-a579-1f6e9371eade` |  |
| [`naticusdroid_android_permissions_dataset`](naticusdroid_android_permissions_dataset/) | IID | 7,491 | 85 | 3 x 3 | not built | `dataset_conflicting_duplicate_rows`, `dataset_pure_feature_value` |
| [`nba_players_2016_2019`](nba_players_2016_2019/) | grouped | 1,408 | 34 | 10 x 3 | not built |  |
| [`numerai_v5_2_1m`](numerai_v5_2_1m/) | temporal | 2,025,745 | 781 | 3 x 1 | not built |  |
| [`nyc_taxi_trip_duration`](nyc_taxi_trip_duration/) | temporal | 1,451,706 | 7 | 3 x 1 | not built |  |
| [`obesity_estimation`](obesity_estimation/) | IID | 498 | 14 | 20 x 3 | `01a111fc-b36e-7939-b271-e858cafffee4` | `dataset_duplicate_rows` |
| [`online_shoppers_purchasing_intention_dataset`](online_shoppers_purchasing_intention_dataset/) | IID | 6,875 | 16 | 3 x 3 | not built |  |
| [`onlinenewspopularity`](onlinenewspopularity/) | temporal | 39,643 | 40 | 9 x 1 | not built |  |
| [`open_university_learning_analytics_dataset`](open_university_learning_analytics_dataset/) | grouped | 26,395 | 40 | 3 x 3 | not built |  |
| [`otto_group_product_classification_challenge`](otto_group_product_classification_challenge/) | IID | 61,878 | 93 | 3 x 3 | `01a111fc-7288-72b4-8ceb-e6f796d2a623` |  |
| [`ov_ovarian_cancer`](ov_ovarian_cancer/) | IID | 284 | 48,279 | 20 x 3 | not built |  |
| [`pancreatic_cancer_mouse_detection`](pancreatic_cancer_mouse_detection/) | grouped | 181 | 6,771 | 20 x 3 | `01a111fc-4ee4-7a63-9a02-e4ac045fac79` | `dataset_missing_value_sentinel` |
| [`perth_house_prices`](perth_house_prices/) | temporal | 33,090 | 18 | 9 x 1 | not built |  |
| [`phiusil_phishing`](phiusil_phishing/) | IID | 235,370 | 49 | 3 x 3 | not built |  |
| [`pkdd_15_taxi_trip_time_prediction_ii_1m`](pkdd_15_taxi_trip_time_prediction_ii_1m/) | temporal | 1,436,885 | 8 | 3 x 1 | not built |  |
| [`polish_companies_bankruptcy`](polish_companies_bankruptcy/) | IID | 5,790 | 64 | 3 x 3 | not built |  |
| [`porto_seguro`](porto_seguro/) | IID | 595,206 | 37 | 1 x 3 | `01a111fb-fc94-70f9-9598-6ab89e8b220d` |  |
| [`predict_students_dropout_and_academic_success`](predict_students_dropout_and_academic_success/) | IID | 4,424 | 36 | 3 x 3 | `01a111fc-b7bd-7c0b-a919-1a848957caf4` |  |
| [`pva_revenue_prediction_kddcup98`](pva_revenue_prediction_kddcup98/) | IID | 144,095 | 477 | 3 x 3 | not built | `dataset_constant_column`, `dataset_missing_value_label`, `meta_license_unknown` |
| [`qsar_aquatic_toxicity`](qsar_aquatic_toxicity/) | IID | 546 | 8 | 20 x 3 | `01a111fc-b7f2-70ec-b160-9c69d2d62b73` | `dataset_conflicting_duplicate_rows` |
| [`qsar_bioconcentration`](qsar_bioconcentration/) | IID | 776 | 10 | 10 x 3 | not built |  |
| [`qsar_biodeg`](qsar_biodeg/) | IID | 1,054 | 41 | 10 x 3 | `01a111fc-bbf4-7a48-86aa-22bfb52b8d59` |  |
| [`qsar_fish_toxicity`](qsar_fish_toxicity/) | IID | 908 | 6 | 10 x 3 | `01a111fc-ec16-7add-afb7-17f93dcaa3d4` | `dataset_conflicting_duplicate_rows` |
| [`qsar_oral_toxicity`](qsar_oral_toxicity/) | IID | 8,493 | 1,024 | 3 x 3 | not built |  |
| [`qsar_tid_11`](qsar_tid_11/) | IID | 5,741 | 1,024 | 3 x 3 | `01a111fc-77d3-7128-8497-210288cab270` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`rain_in_australia`](rain_in_australia/) | temporal | 264,562 | 22 | 9 x 1 | not built |  |
| [`regensburg_pediatric_appendicitis`](regensburg_pediatric_appendicitis/) | IID | 763 | 51 | 10 x 3 | not built |  |
| [`rosbank1`](rosbank1/) | temporal | 4,791 | 347 | 3 x 1 | not built |  |
| [`rossmann_store_sales`](rossmann_store_sales/) | temporal | 844,392 | 15 | 3 x 1 | not built |  |
| [`santander_customer_satisfaction`](santander_customer_satisfaction/) | IID | 71,080 | 307 | 3 x 3 | `01a111fc-12c0-72fc-95ab-3a7ad03daa2b` | `dataset_pure_feature_value` |
| [`santander_customer_transaction_prediction`](santander_customer_transaction_prediction/) | IID | 200,000 | 200 | 3 x 3 | `01a111fa-f277-7533-bac1-a15ddbf6a38d` |  |
| [`santander_transaction_value`](santander_transaction_value/) | IID | 4,447 | 540 | 3 x 3 | `01a111fb-c8c5-7b20-b3a0-528353375933` |  |
| [`sarcoma`](sarcoma/) | IID | 201 | 25,971 | 20 x 3 | not built |  |
| [`sat11_hand_algo_runtime`](sat11_hand_algo_runtime/) | grouped (per group: select_min) | 1,840 | 169 | 10 x 3 | `01a111fc-eda8-7830-9b0d-905bf0c5bc1d` | `dataset_constant_column` |
| [`sberbank_housing_market_forecasting`](sberbank_housing_market_forecasting/) | temporal | 27,195 | 386 | 5 x 1 | not built |  |
| [`sdss_17`](sdss_17/) | IID | 99,999 | 8 | 3 x 3 | not built |  |
| [`sepsis_prediction_1m`](sepsis_prediction_1m/) | grouped | 1,499,997 | 42 | 1 x 3 | not built |  |
| [`sepsis_survival_minimal_clinical_records`](sepsis_survival_minimal_clinical_records/) | IID | 110,204 | 3 | 3 x 3 | not built | `dataset_duplicate_rows` |
| [`sf_permit_time`](sf_permit_time/) | temporal | 99,847 | 37 | 8 x 1 | not built |  |
| [`south_africa_coronary_heart_disease`](south_africa_coronary_heart_disease/) | IID | 462 | 9 | 20 x 3 | not built |  |
| [`splice`](splice/) | IID | 3,190 | 60 | 10 x 3 | not built | `dataset_duplicate_rows` |
| [`stroke_prediction`](stroke_prediction/) | IID | 43,400 | 9 | 3 x 3 | not built |  |
| [`student_portuguese_performance`](student_portuguese_performance/) | IID | 649 | 30 | 20 x 3 | not built |  |
| [`superconductivity`](superconductivity/) | grouped | 21,263 | 81 | 3 x 3 | not built | `dataset_conflicting_duplicate_rows` |
| [`taiwanese_bankruptcy_prediction`](taiwanese_bankruptcy_prediction/) | IID | 6,819 | 92 | 3 x 3 | not built |  |
| [`thyroid_discordant`](thyroid_discordant/) | IID | 3,711 | 26 | 10 x 3 | not built |  |
| [`tour_travels_churn`](tour_travels_churn/) | IID | 954 | 6 | 10 x 3 | `01a111fc-edc9-7641-b79f-dc54c06b0b31` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows`, `meta_bibtex_latex_hazard` |
| [`video_transcoding_time_prediction`](video_transcoding_time_prediction/) | grouped | 68,784 | 18 | 3 x 3 | `01a111fc-7b5a-7853-8e13-f42ccc0c3b03` |  |
| [`website_phishing`](website_phishing/) | IID | 1,353 | 9 | 10 x 3 | not built | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`wids_diabetes_mellitus`](wids_diabetes_mellitus/) | IID | 127,358 | 181 | 3 x 3 | `01a111fc-032c-7d1f-a669-78dc5d1cd86b` |  |
| [`wine_quality`](wine_quality/) | IID | 5,320 | 12 | 3 x 3 | `01a111fc-f00a-7053-95dc-e278996515ca` |  |
| [`wine_world_cost`](wine_world_cost/) | IID | 1,279 | 14 | 10 x 3 | `01a111fc-bf3e-75e4-bd32-d489275dd877` |  |
| [`zillow_prize`](zillow_prize/) | temporal | 153,108 | 56 | 9 x 1 | not built |  |
<!-- datasets:end -->
