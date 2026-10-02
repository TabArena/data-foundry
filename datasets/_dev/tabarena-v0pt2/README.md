# TabArena-v0.2  Curation Overview

Working setup towards TabArena-v0.2

- **New here?** [`GETTING_STARTED.md`](GETTING_STARTED.md): set-up, the two workflows (settling a record, adding a
  dataset) and the large-data candidates to start with.
- **Every change is logged** in [`CHANGELOG.md`](CHANGELOG.md): edits, added or removed files, re-runs that change a container.
- The leak audit of September-October 2026 (removed and changed datasets, with severity) is summarised in [`LEAK_AUDIT.md`](LEAK_AUDIT.md).
- Changes the benchmark harness (TabArena) needs for these datasets, for example scoring grouped tasks per group, are in [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).
- Each dataset folder has a `README.md` that `.venv/bin/python -m data_foundry.curation.cli dataset check` generates from its `dataset.py`: the folder's files, links to the curation record and the source, how to rebuild, the evidence and the build record.
- Open decisions and later work are in [`TODO.md`](TODO.md).

## Rebuild

All 130 datasets were built on 2026-10-02 from the definitions in this folder (the UUIDs below), as container
format 2 (`container.format_version == 2`). To rebuild one, from
the repository root:

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/<name>   # no save; rewrites README.md
.venv/bin/python -m data_foundry.curation.cli dataset build datasets/_dev/tabarena-v0pt2/<name>   # saves a new container and UUID
```

- The raw files come from `local-data-warehouse/` (or `$DATA_FOUNDRY_WAREHOUSE`); each `README.md` gives the download
  command. The rebuild read 435 raw files (67 GB, traced per dataset); rebuilding every dataset from a warehouse that
  holds only those files gives the same checksums. The two `_prepare_raw_files` steps read 33 more (4.4 GB). A backup
  of these 468, with a manifest, is kept outside the repository (it also holds the input of the retired
  telemonitoring dataset).
- To rebuild the whole folder, with the comparison against the previous build, the check from the traced inputs, the
  backup and this table, follow the `/rebuild-working-copy` skill
  ([`.claude/skills/rebuild-working-copy/SKILL.md`](../../../.claude/skills/rebuild-working-copy/SKILL.md)).
- Build in the locked environment (pandas 2.3.3). The rows and splits are the same on every machine; a numpy log or
  exp can differ in its last bit between CPUs, so a dataset with a log-scaled target may get another checksum
  elsewhere.
- `.claude/skills/verify-dataset/scripts/task_probes.py --all --built` sweeps the built containers against dummy baselines ([`TASK_PROBES.md`](TASK_PROBES.md) holds the sweep of this build), and
  `.claude/skills/verify-dataset/scripts/group_probes.py <name>` probes a grouped task.

## Datasets

The v0.2 build of 2026-10-02: regime (with the group-level unit where a task is scored per group), size, outer
splits (repeats x folds; temporal tasks have one fold per window), the container's UUID, and the warnings that are
not accepted in the definition.

<!-- datasets:start -->
| dataset | regime | rows | features | splits | UUID | open warnings |
|---|---|---|---|---|---|---|
| [`5g_energy_consumption`](5g_energy_consumption/) | grouped | 92,629 | 21 | 3 x 3 | `01a0fc60-13f7-7fc9-94b5-ed7745caef30` |  |
| [`acquire_valued_shoppers_challenge`](acquire_valued_shoppers_challenge/) | temporal | 160,057 | 111 | 5 x 1 | `01a0fc5f-fcbd-7748-869f-f93a81d661b5` |  |
| [`airfoil_self_noise`](airfoil_self_noise/) | IID | 1,503 | 5 | 10 x 3 | `01a0fc60-90f7-740e-8e9c-3d56033ca7d3` |  |
| [`allstate_claims_severity`](allstate_claims_severity/) | IID | 188,317 | 130 | 3 x 3 | `01a0fc5f-f972-7ece-bbf2-2fb7fc4cd87a` |  |
| [`amazon_employee_access`](amazon_employee_access/) | IID | 32,769 | 9 | 3 x 3 | `01a0fc60-551f-7f99-a617-e2a8acf507e5` | `dataset_pure_feature_value` |
| [`amex_non_iid_1m`](amex_non_iid_1m/) | grouped (per group: last) | 1,500,000 | 190 | 1 x 3 | `01a0fc5f-7742-7959-83ac-cc9b0380700b` | `dataset_missing_value_sentinel` |
| [`anes_voting_2026`](anes_voting_2026/) | temporal | 48,587 | 261 | 9 x 1 | `01a0fc5f-83b9-7961-9d36-00c8578fcb0f` |  |
| [`aps_failure`](aps_failure/) | IID | 76,000 | 170 | 3 x 3 | `01a0fc5f-b6c6-7d65-ba46-d09bde319498` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`asp_potassco_classification`](asp_potassco_classification/) | grouped | 1,212 | 137 | 10 x 3 | `01a0fc60-5052-733b-a2b3-4a45a1e7a301` | `dataset_constant_column` |
| [`audiology_diagnosis`](audiology_diagnosis/) | IID | 199 | 68 | 20 x 3 | `01a0fc60-6901-7055-8704-c2226b646470` |  |
| [`bad_customer_detection`](bad_customer_detection/) | IID | 1,723 | 13 | 10 x 3 | `01a0fc60-95a5-74e0-91dd-5e766e8b24fd` |  |
| [`bank_customer_churn`](bank_customer_churn/) | IID | 10,000 | 10 | 3 x 3 | `01a0fc60-97f7-749c-8dfa-e48acb8ab268` |  |
| [`bank_marketing`](bank_marketing/) | IID | 45,211 | 13 | 3 x 3 | `01a0fc60-809e-7fdf-a16f-b1bd66824a57` | `dataset_missing_value_sentinel` |
| [`biogeographical_ancestry_prediction`](biogeographical_ancestry_prediction/) | IID | 607 | 102 | 20 x 3 | `01a0fc60-3ad9-7338-9076-03a005cfe236` |  |
| [`biomechanical_orthopaedic_prediction`](biomechanical_orthopaedic_prediction/) | IID | 310 | 6 | 20 x 3 | `01a0fc60-9963-7a6f-bb80-1e4eba9607c5` |  |
| [`bioresponse`](bioresponse/) | IID | 3,751 | 1,776 | 3 x 3 | `01a0fc5f-ec15-7de6-8a4d-9cbf4207c582` |  |
| [`blood_tests_drink_prediction`](blood_tests_drink_prediction/) | IID | 345 | 5 | 20 x 3 | `01a0fc60-8cc3-7555-9222-50db3938b132` | `dataset_duplicate_rows` |
| [`blood_transfusion`](blood_transfusion/) | IID | 748 | 4 | 20 x 3 | `01a0fc60-9787-7a1a-b452-2060af900230` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`body_density_prediction`](body_density_prediction/) | IID | 252 | 13 | 20 x 3 | `01a0fc60-8e90-78cf-9051-e298b9487067` |  |
| [`california_house_prices_2020`](california_house_prices_2020/) | temporal | 41,528 | 41 | 3 x 1 | `01a0fc60-1800-7329-88dd-e4bf1a8c1a73` |  |
| [`cardiotocography`](cardiotocography/) | grouped | 2,126 | 23 | 10 x 3 | `01a0fc60-4871-7a30-b1d9-6d6150de7a20` | `dataset_constant_column` |
| [`churn`](churn/) | IID | 5,000 | 19 | 3 x 3 | `01a0fc60-816a-780f-9da9-cf33df8d6045` |  |
| [`cirrhosis_patient_survival_prediction`](cirrhosis_patient_survival_prediction/) | IID | 161 | 17 | 20 x 3 | `01a0fc60-6ebe-7eb5-8202-0d4b00011049` |  |
| [`climate_model_weather_forecasting_1m`](climate_model_weather_forecasting_1m/) | temporal | 2,115,283 | 99 | 3 x 1 | `01a0fc5f-1cba-7405-8f1b-1e165ab60d71` |  |
| [`clock_protein_toxicity`](clock_protein_toxicity/) | IID | 171 | 1,117 | 20 x 3 | `01a0fc60-371d-7054-8c4a-a2b1a4ce72b5` |  |
| [`coffee_rating_prediction`](coffee_rating_prediction/) | temporal | 2,369 | 12 | 13 x 1 | `01a0fc60-89e4-7e07-b681-3db0f2cd368d` | `dataset_constant_column` |
| [`coil_2000`](coil_2000/) | IID | 9,822 | 85 | 3 x 3 | `01a0fc60-7b4a-79ea-9389-6d93c544377d` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`concrete_compressive_strength`](concrete_compressive_strength/) | IID | 1,030 | 8 | 10 x 3 | `01a0fc60-9801-7be5-a7ef-e3e66812974d` | `dataset_duplicate_rows` |
| [`consumer_complaints_1m`](consumer_complaints_1m/) | temporal | 1,811,452 | 12 | 3 x 1 | `01a0fc60-96e8-7d64-801f-0d2241496bdd` |  |
| [`cooking_time_1m`](cooking_time_1m/) | temporal | 2,500,000 | 196 | 3 x 1 | `01a0fc5f-64ce-700b-be10-558e01d744c1` |  |
| [`covertype`](covertype/) | IID | 581,012 | 14 | 1 x 3 | `01a0fc5f-e75a-7013-a0ea-b491f4910b26` |  |
| [`credit_approval`](credit_approval/) | IID | 690 | 15 | 20 x 3 | `01a0fc60-947c-78c4-8703-470535ccafb6` |  |
| [`credit_card_clients_default`](credit_card_clients_default/) | IID | 30,000 | 23 | 3 x 3 | `01a0fc60-27a8-7af0-9d04-d3623053a72e` |  |
| [`credit_g`](credit_g/) | IID | 1,000 | 20 | 10 x 3 | `01a0fc60-9847-7d24-bfc4-08a252ee1b97` |  |
| [`delivery_eta_1m`](delivery_eta_1m/) | temporal | 2,500,000 | 221 | 3 x 1 | `01a0fc5f-dea9-790a-8847-60e27e90befe` |  |
| [`dementia_prediction`](dementia_prediction/) | grouped | 370 | 9 | 20 x 3 | `01a0fc60-682b-77b1-bc3e-dd1fe07452bc` |  |
| [`diabetes_130_us`](diabetes_130_us/) | IID | 69,973 | 44 | 3 x 3 | `01a0fc60-1e89-78c1-8d68-28a9de9a9585` |  |
| [`diamonds`](diamonds/) | IID | 53,940 | 9 | 3 x 3 | `01a0fc60-421d-7a66-96d8-6aa8b67ffadb` |  |
| [`drug_induced_autoimmunity_prediction`](drug_induced_autoimmunity_prediction/) | IID | 597 | 177 | 20 x 3 | `01a0fc60-386c-7860-9aff-a5e19479be7e` | `dataset_identifier_column` |
| [`early_learning_predictors`](early_learning_predictors/) | grouped | 18,874 | 744 | 3 x 3 | `01a0fc5f-f286-75ad-98a3-27aa42fd59fe` | `dataset_duplicate_columns` |
| [`early_stage_diabetes_risk_prediction`](early_stage_diabetes_risk_prediction/) | IID | 251 | 16 | 20 x 3 | `01a0fc60-8a23-7b51-aa7a-665371deeddb` |  |
| [`ecoli_proteins`](ecoli_proteins/) | IID | 327 | 6 | 20 x 3 | `01a0fc60-8917-7087-9551-ec700f738d69` |  |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/) | grouped | 1,296,316 | 110 | 1 x 3 | `01a0fc5e-edda-747f-9c5f-3aefa165b459` |  |
| [`emscad`](emscad/) | grouped | 16,116 | 18 | 3 x 3 | `01a0fc60-1da1-7adb-be53-5e67c3c0b798` |  |
| [`eryhemato_squamous_disease`](eryhemato_squamous_disease/) | IID | 366 | 34 | 20 x 3 | `01a0fc60-5622-772d-b079-ece2927b2dba` |  |
| [`fiat_500`](fiat_500/) | IID | 1,538 | 7 | 10 x 3 | `01a0fc60-8cd2-76fe-84ea-0b9c2ed166ca` | `dataset_duplicate_rows` |
| [`fitness_club`](fitness_club/) | IID | 1,500 | 6 | 10 x 3 | `01a0fc60-8d6c-7ecd-b3c9-b7d7ff38885c` |  |
| [`food_delivery_time`](food_delivery_time/) | IID | 45,451 | 9 | 3 x 3 | `01a0fc60-49df-7f8b-86d9-a1bd2a5ad746` |  |
| [`forensic_glass_identification`](forensic_glass_identification/) | IID | 214 | 9 | 20 x 3 | `01a0fc60-4dcc-70ca-a8f3-136bd4bb004a` |  |
| [`forest_fires`](forest_fires/) | IID | 517 | 12 | 20 x 3 | `01a0fc60-8175-7e7c-9ec8-322f32e214e7` | `dataset_conflicting_duplicate_rows` |
| [`gallstone_disease`](gallstone_disease/) | IID | 319 | 38 | 20 x 3 | `01a0fc60-3cde-7165-95d3-00c53504785c` |  |
| [`garments_worker_productivity`](garments_worker_productivity/) | temporal | 1,197 | 15 | 30 x 1 | `01a0fc60-8243-7a49-9cef-961cf380a456` |  |
| [`give_me_some_credit`](give_me_some_credit/) | IID | 150,000 | 10 | 3 x 3 | `01a0fc60-0ac2-79b7-8900-5b13abc509c4` |  |
| [`healthcare_insurance_expenses`](healthcare_insurance_expenses/) | IID | 1,338 | 6 | 10 x 3 | `01a0fc60-95fe-7561-ab1b-3726140fec78` |  |
| [`heart_disease_cleveland`](heart_disease_cleveland/) | IID | 303 | 13 | 20 x 3 | `01a0fc60-987f-75e1-a76a-50bcbac426aa` |  |
| [`heart_disease_hungary`](heart_disease_hungary/) | IID | 294 | 13 | 20 x 3 | `01a0fc60-493f-77a6-9992-0bb3843007fa` | `dataset_constant_column` |
| [`heart_disease_va_long_beach`](heart_disease_va_long_beach/) | IID | 200 | 13 | 20 x 3 | `01a0fc60-8e35-7162-97c9-b06057bddb98` | `dataset_constant_column` |
| [`heart_failure_followup_survival`](heart_failure_followup_survival/) | IID | 299 | 11 | 20 x 3 | `01a0fc60-8c62-7d5d-af04-b396601d6137` |  |
| [`heloc`](heloc/) | IID | 10,459 | 23 | 3 x 3 | `01a0fc60-74ac-7a86-b360-95cc96b51c90` | `dataset_missing_value_sentinel`, `dataset_duplicate_rows` |
| [`hepatitis_c_prediction`](hepatitis_c_prediction/) | IID | 608 | 11 | 20 x 3 | `01a0fc60-758d-7571-b119-112ac68c4761` |  |
| [`hepatitis_survival_prediction`](hepatitis_survival_prediction/) | IID | 155 | 19 | 20 x 3 | `01a0fc60-4730-7378-afef-efbb149e3ddf` |  |
| [`hiva_agnostic`](hiva_agnostic/) | IID | 3,845 | 1,518 | 3 x 3 | `01a0fc5f-d0c9-7748-a28f-bfaa223669cc` | `dataset_pure_feature_value` |
| [`home_credit_default_risk`](home_credit_default_risk/) | IID | 307,507 | 504 | 3 x 3 | `01a0fc5f-9149-7b30-8caf-80ceaf0609c8` |  |
| [`home_credit_default_stability_1m`](home_credit_default_stability_1m/) | temporal | 1,224,927 | 710 | 3 x 1 | `01a0fc5f-32a9-7c9d-8a01-13068f6a7589` |  |
| [`homesite_quote_conversion`](homesite_quote_conversion/) | IID | 260,753 | 295 | 3 x 3 | `01a0fc5f-c1b7-7d56-bab5-76daaf9c5079` | `dataset_constant_column`, `dataset_missing_value_label` |
| [`horse_colic_survival`](horse_colic_survival/) | IID | 344 | 20 | 20 x 3 | `01a0fc60-4d8b-7581-8794-9c1299951b90` |  |
| [`hotel_booking_demand`](hotel_booking_demand/) | temporal | 81,418 | 28 | 9 x 1 | `01a0fc60-2a9c-79d6-8132-e7cbd2de59a7` |  |
| [`houses`](houses/) | IID | 19,675 | 8 | 3 x 3 | `01a0fc60-6926-76c5-a660-115db0d40ff0` |  |
| [`hr_analytics`](hr_analytics/) | IID | 19,158 | 12 | 3 x 3 | `01a0fc60-54ae-7610-bf92-be667616e935` |  |
| [`ieee_fraud_detection`](ieee_fraud_detection/) | temporal | 590,540 | 435 | 3 x 1 | `01a0fc5e-d5a6-76dd-8c3f-7c432b148db5` |  |
| [`immoscout_german_house_prices`](immoscout_german_house_prices/) | IID | 10,317 | 23 | 3 x 3 | `01a0fc60-401b-76a3-af45-73b26eff210d` |  |
| [`in_vehicle_coupon_recommendation`](in_vehicle_coupon_recommendation/) | grouped | 12,684 | 25 | 3 x 3 | `01a0fc60-3878-785b-8732-1585571026d6` |  |
| [`indian_liver_patient_dataset`](indian_liver_patient_dataset/) | IID | 583 | 10 | 20 x 3 | `01a0fc60-81d3-7387-b2a1-a75d12f77f21` | `dataset_duplicate_rows` |
| [`jm1`](jm1/) | IID | 8,736 | 21 | 3 x 3 | `01a0fc60-73dc-7c20-98c8-f02cdc786331` |  |
| [`kdd_cup_09_appetency`](kdd_cup_09_appetency/) | IID | 50,000 | 212 | 3 x 3 | `01a0fc5f-becd-74e0-8d97-59a1b01cf9ef` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`kick`](kick/) | temporal | 72,983 | 32 | 9 x 1 | `01a0fc60-1965-734a-954e-9bafda35dff1` |  |
| [`kickstarter`](kickstarter/) | temporal | 187,117 | 12 | 3 x 1 | `01a0fc5f-ce7d-78d2-9291-6eba96feb93c` |  |
| [`labour_inspection_compliance`](labour_inspection_compliance/) | IID | 63,634 | 376 | 3 x 3 | `01a0fc5e-f5a5-7c73-83cb-12df88f8575d` | `dataset_constant_column` |
| [`lending_club`](lending_club/) | temporal | 609,544 | 81 | 3 x 1 | `01a0fc5f-427a-7b9a-810a-0d730ffdc5cf` |  |
| [`ljubljana_breast_cancer`](ljubljana_breast_cancer/) | IID | 286 | 9 | 20 x 3 | `01a0fc60-7067-7a1f-befe-84639546dfce` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`ljubljana_primary_tumor`](ljubljana_primary_tumor/) | IID | 302 | 17 | 20 x 3 | `01a0fc60-55ba-74f5-883c-486d25b92cff` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`lung_cancer`](lung_cancer/) | IID | 197 | 12,600 | 20 x 3 | `01a0fc5f-429c-7b6b-97d7-1e21076585ea` | `dataset_missing_value_sentinel` |
| [`lung_cancer_epithelial_genexp`](lung_cancer_epithelial_genexp/) | IID | 187 | 22,215 | 20 x 3 | `01a0fc5e-cbe8-7301-be74-6054b4388211` |  |
| [`maps_router_eta_1m`](maps_router_eta_1m/) | temporal | 2,500,000 | 988 | 3 x 1 | `01a0fc60-72f1-7e16-a26f-e75844fbe2a2` |  |
| [`marketing_campaign`](marketing_campaign/) | IID | 2,240 | 25 | 10 x 3 | `01a0fc60-47fb-7887-8e5a-530f31ce2d21` | `dataset_duplicate_rows` |
| [`mercari_price_suggestion`](mercari_price_suggestion/) | IID | 1,482,486 | 6 | 1 x 3 | `01a0fc5e-e059-7a50-8ee8-b7f29dd2b509` |  |
| [`mercedes_benz_greener_manufacturing`](mercedes_benz_greener_manufacturing/) | temporal | 4,204 | 371 | 9 x 1 | `01a0fc60-2978-72c3-9766-5d7f273e1f59` | `dataset_constant_column`, `dataset_duplicate_columns`, `meta_tags_missing_regime` |
| [`miami_housing`](miami_housing/) | IID | 13,776 | 15 | 3 x 3 | `01a0fc60-70e2-72d6-bff6-1e23ddfd1341` |  |
| [`mic`](mic/) | IID | 1,699 | 102 | 10 x 3 | `01a0fc60-6eca-7f68-b3b9-98662f1ecb70` |  |
| [`micro_mass`](micro_mass/) | grouped | 571 | 1,083 | 20 x 3 | `01a0fc60-18a5-7bad-baeb-244e1a127772` |  |
| [`musk`](musk/) | grouped (per group: any) | 6,598 | 167 | 20 x 3 | `01a0fc60-3d6d-7a61-ab17-8558431952b9` | `dataset_missing_value_sentinel` |
| [`mutual_funds_india`](mutual_funds_india/) | IID | 793 | 11 | 10 x 3 | `01a0fc60-82e4-7bf3-a2cf-8e37a069fce0` |  |
| [`naticusdroid_android_permissions_dataset`](naticusdroid_android_permissions_dataset/) | IID | 7,491 | 85 | 3 x 3 | `01a0fc60-4104-72c4-9c10-bdf97e3066d9` | `dataset_conflicting_duplicate_rows`, `dataset_pure_feature_value` |
| [`obesity_estimation`](obesity_estimation/) | IID | 498 | 14 | 20 x 3 | `01a0fc60-8862-7bf6-81ae-3727e184a312` | `dataset_duplicate_rows` |
| [`online_shoppers_purchasing_intention_dataset`](online_shoppers_purchasing_intention_dataset/) | IID | 6,875 | 16 | 3 x 3 | `01a0fc60-9358-7bc1-ad5e-84fa3e717179` |  |
| [`otto_group_product_classification_challenge`](otto_group_product_classification_challenge/) | IID | 61,878 | 93 | 3 x 3 | `01a0fc5f-ed64-79b3-b4fc-d4e93da131a0` |  |
| [`pancreatic_cancer_mouse_detection`](pancreatic_cancer_mouse_detection/) | grouped | 181 | 6,772 | 20 x 3 | `01a0fc5f-b8a8-765c-af91-f81f5b3d7357` | `dataset_missing_value_sentinel` |
| [`parkinsons_biomedical_voice_measurements`](parkinsons_biomedical_voice_measurements/) | grouped (per group: mean) | 195 | 24 | 20 x 3 | `01a0fc60-75e3-7d52-b24a-89f4dee142f9` |  |
| [`physiochemical_protein`](physiochemical_protein/) | IID | 45,730 | 9 | 3 x 3 | `01a0fc60-70dd-7f0b-9011-6f3e92981c89` | `dataset_duplicate_rows` |
| [`polish_companies_bankruptcy`](polish_companies_bankruptcy/) | IID | 5,790 | 64 | 3 x 3 | `01a0fc60-5389-78a6-98bb-5a4894e808b6` |  |
| [`porto_seguro`](porto_seguro/) | IID | 595,206 | 37 | 1 x 3 | `01a0fc5f-8b62-78bf-9350-b702f9318885` |  |
| [`predict_students_dropout_and_academic_success`](predict_students_dropout_and_academic_success/) | IID | 4,424 | 36 | 3 x 3 | `01a0fc60-49ac-710c-9608-9722ea297c68` |  |
| [`pva_revenue_prediction_kddcup98`](pva_revenue_prediction_kddcup98/) | IID | 144,095 | 477 | 3 x 3 | `01a0fc5f-8eeb-737d-aac0-63ea9cff8929` | `dataset_constant_column`, `dataset_missing_value_label`, `meta_license_unknown` |
| [`qsar_aquatic_toxicity`](qsar_aquatic_toxicity/) | IID | 546 | 8 | 20 x 3 | `01a0fc60-8ae1-702f-a4a7-913b6cc593ba` | `dataset_conflicting_duplicate_rows` |
| [`qsar_biodeg`](qsar_biodeg/) | IID | 1,054 | 41 | 10 x 3 | `01a0fc60-7f2f-70ef-ae6b-41f291d9c4de` |  |
| [`qsar_fish_toxicity`](qsar_fish_toxicity/) | IID | 908 | 6 | 10 x 3 | `01a0fc60-530d-71eb-9e17-a7a093e3eab4` | `dataset_conflicting_duplicate_rows` |
| [`qsar_tid_11`](qsar_tid_11/) | IID | 5,741 | 1,024 | 3 x 3 | `01a0fc60-0a98-7ec4-9ce5-f4bdcf8be91a` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`regensburg_pediatric_appendicitis`](regensburg_pediatric_appendicitis/) | IID | 763 | 51 | 10 x 3 | `01a0fc60-2a7d-7d20-b3a3-5f2630395883` |  |
| [`rossmann_store_sales`](rossmann_store_sales/) | temporal | 844,392 | 15 | 3 x 1 | `01a0fc5f-efec-72a0-bd33-384ab0679c27` |  |
| [`santander_customer_satisfaction`](santander_customer_satisfaction/) | IID | 71,080 | 307 | 3 x 3 | `01a0fc5f-b6cc-7ca2-8954-ecb4a6bea136` | `dataset_pure_feature_value` |
| [`santander_customer_transaction_prediction`](santander_customer_transaction_prediction/) | IID | 200,000 | 200 | 3 x 3 | `01a0fc5e-d6ad-757b-8c39-ddbff7c4dd7f` |  |
| [`santander_transaction_value`](santander_transaction_value/) | IID | 4,447 | 540 | 3 x 3 | `01a0fc5f-30b7-7b6a-ba6e-f28fa7830f86` |  |
| [`sat11_hand_algo_runtime`](sat11_hand_algo_runtime/) | grouped (per group: select_min) | 1,840 | 170 | 10 x 3 | `01a0fc60-48b6-761f-8677-d7dfa4e94b03` | `dataset_constant_column` |
| [`sberbank_housing_market_forecasting`](sberbank_housing_market_forecasting/) | temporal | 27,195 | 386 | 5 x 1 | `01a0fc5f-e899-753c-9593-305f988ab8a3` |  |
| [`sdss_17`](sdss_17/) | IID | 99,999 | 8 | 3 x 3 | `01a0fc60-0aec-78a1-9c84-603f8bd7c951` |  |
| [`sepsis_prediction_1m`](sepsis_prediction_1m/) | grouped | 1,499,997 | 43 | 1 x 3 | `01a0fc5f-643a-74da-8f73-28e36c3b0443` |  |
| [`sepsis_survival_minimal_clinical_records`](sepsis_survival_minimal_clinical_records/) | IID | 110,204 | 3 | 3 x 3 | `01a0fc60-1df5-70ee-ae63-c3826d15073c` | `dataset_duplicate_rows` |
| [`sf_permit_time`](sf_permit_time/) | temporal | 99,847 | 37 | 9 x 1 | `01a0fc5f-96a0-79d1-bbf3-a0e71eeb806d` |  |
| [`south_africa_coronary_heart_disease`](south_africa_coronary_heart_disease/) | IID | 462 | 9 | 20 x 3 | `01a0fc60-7d88-7a8e-8d06-01a1a2156167` |  |
| [`splice`](splice/) | IID | 3,190 | 60 | 10 x 3 | `01a0fc60-7d6b-7130-a04d-dcd231722181` | `dataset_duplicate_rows` |
| [`student_portuguese_performance`](student_portuguese_performance/) | IID | 649 | 30 | 20 x 3 | `01a0fc60-4f43-776b-afe9-2b1b77b5ad98` |  |
| [`superconductivity`](superconductivity/) | IID | 21,263 | 81 | 3 x 3 | `01a0fc60-25d6-7c34-9784-808210facf83` | `dataset_conflicting_duplicate_rows` |
| [`taiwanese_bankruptcy_prediction`](taiwanese_bankruptcy_prediction/) | IID | 6,819 | 92 | 3 x 3 | `01a0fc60-6ad7-792d-9b5a-a27d5cb2b03a` |  |
| [`thyroid_discordant`](thyroid_discordant/) | IID | 3,711 | 26 | 10 x 3 | `01a0fc60-81f3-7930-9897-9dc9aceaea25` |  |
| [`tour_travels_churn`](tour_travels_churn/) | IID | 954 | 6 | 10 x 3 | `01a0fc60-82e1-7734-a58d-bfe1316f6bf4` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows`, `meta_bibtex_latex_hazard` |
| [`video_transcoding_time_prediction`](video_transcoding_time_prediction/) | grouped | 68,784 | 19 | 3 x 3 | `01a0fc60-1cf9-7c39-a6a5-db1dd7a841f0` |  |
| [`website_phishing`](website_phishing/) | IID | 1,353 | 9 | 10 x 3 | `01a0fc60-9908-7417-92f7-d60b4f0332a8` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`wids_diabetes_mellitus`](wids_diabetes_mellitus/) | IID | 127,358 | 181 | 3 x 3 | `01a0fc5f-b011-7c24-b294-7e6357ace5f1` |  |
| [`wine_quality`](wine_quality/) | IID | 5,320 | 12 | 3 x 3 | `01a0fc60-9ca3-7220-ada0-cea14cb4e0f3` |  |
| [`wine_world_cost`](wine_world_cost/) | IID | 1,279 | 14 | 10 x 3 | `01a0fc60-7ae3-773b-9871-80f4185eb988` |  |
<!-- datasets:end -->
