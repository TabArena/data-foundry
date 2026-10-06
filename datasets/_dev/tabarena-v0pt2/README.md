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

The 125 datasets were built on 2026-10-06 from the definitions in this folder (the UUIDs below), as container
format 2 (`container.format_version == 2`). To rebuild one, from the repository root:

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
| [`5g_energy_consumption`](5g_energy_consumption/) | grouped | 92,629 | 20 | 3 x 3 | `01a111fc-7d10-76f4-b97c-284becb386ec` |  |
| [`acquire_valued_shoppers_challenge`](acquire_valued_shoppers_challenge/) | temporal | 160,057 | 111 | 5 x 1 | `01a111fd-7588-73e4-bf55-26fb6336c1f4` |  |
| [`airfoil_self_noise`](airfoil_self_noise/) | grouped | 1,503 | 5 | 10 x 3 | `01a11312-37c8-7cae-b6c8-c0b883fea348` |  |
| [`allstate_claims_severity`](allstate_claims_severity/) | IID | 188,317 | 130 | 3 x 3 | `01a111fc-59f8-730c-b058-7264a71a29bc` |  |
| [`amazon_employee_access`](amazon_employee_access/) | IID | 32,769 | 9 | 3 x 3 | `01a111fc-c1ef-71ea-8931-5bb5679fad84` | `dataset_pure_feature_value` |
| [`amex_non_iid_1m`](amex_non_iid_1m/) | grouped (per group: last) | 1,500,000 | 189 | 1 x 3 | `01a111fb-d73e-711b-a490-c684c5c4635d` | `dataset_missing_value_sentinel` |
| [`anes_voting_2026`](anes_voting_2026/) | temporal | 48,587 | 261 | 9 x 1 | `01a111fb-cb34-797a-ba46-5305a0c33af4` |  |
| [`aps_failure`](aps_failure/) | IID | 76,000 | 170 | 3 x 3 | `01a111fc-0ce6-78ed-a870-52ce14ff98d0` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`asp_potassco_classification`](asp_potassco_classification/) | grouped | 1,212 | 136 | 10 x 3 | `01a111fc-9534-79ba-a1c0-efe7268f38e0` | `dataset_constant_column` |
| [`audiology_diagnosis`](audiology_diagnosis/) | IID | 195 | 65 | 20 x 3 | `01a111fc-c395-7cc5-9b60-91d8a7afaa20` |  |
| [`bad_customer_detection`](bad_customer_detection/) | IID | 1,723 | 13 | 10 x 3 | `01a111fc-c415-7ef4-a2b9-d98a1d4aa9f8` |  |
| [`bank_customer_churn`](bank_customer_churn/) | IID | 10,000 | 10 | 3 x 3 | `01a111fc-c45b-7b5e-b6fe-7f527899d692` |  |
| [`bank_marketing`](bank_marketing/) | IID | 45,211 | 13 | 3 x 3 | `01a111fc-7c2d-7441-b859-646c9bfbf380` | `dataset_missing_value_sentinel` |
| [`biogeographical_ancestry_prediction`](biogeographical_ancestry_prediction/) | IID | 607 | 102 | 20 x 3 | `01a111fc-9b9e-7d5b-bb54-5ba4424f3c12` |  |
| [`biomechanical_orthopaedic_prediction`](biomechanical_orthopaedic_prediction/) | IID | 310 | 6 | 20 x 3 | `01a111fc-c9b3-7a87-ad18-98510a3fb2b1` |  |
| [`bioresponse`](bioresponse/) | IID | 3,751 | 1,776 | 3 x 3 | `01a111fc-4c0b-76f4-b01d-a4db8e120e35` |  |
| [`blood_tests_drink_prediction`](blood_tests_drink_prediction/) | IID | 345 | 5 | 20 x 3 | `01a111fc-c9a3-7ff6-8480-be0052f38d83` | `dataset_duplicate_rows` |
| [`blood_transfusion`](blood_transfusion/) | IID | 748 | 4 | 20 x 3 | `01a111fc-c9d3-70c1-ba1b-e4fe45899e78` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`body_density_prediction`](body_density_prediction/) | IID | 252 | 13 | 20 x 3 | `01a111fc-caac-7d14-8929-e266415ab9cf` |  |
| [`california_house_prices_2020`](california_house_prices_2020/) | temporal | 41,528 | 41 | 3 x 1 | `01a111fc-8933-7ac4-8766-8038342d53f2` |  |
| [`cardiotocography`](cardiotocography/) | grouped | 2,126 | 22 | 10 x 3 | `01a111fc-7d1e-7b12-8cc7-298d2fc12820` | `dataset_constant_column` |
| [`cirrhosis_patient_survival_prediction`](cirrhosis_patient_survival_prediction/) | IID | 161 | 17 | 20 x 3 | `01a111fc-cd63-7ce2-90cc-a28712493bda` |  |
| [`climate_model_weather_forecasting_1m`](climate_model_weather_forecasting_1m/) | temporal | 2,115,283 | 99 | 3 x 1 | `01a111fb-bc63-7614-a137-a3fd390bc4f1` |  |
| [`clock_protein_toxicity`](clock_protein_toxicity/) | IID | 171 | 1,117 | 20 x 3 | `01a111fc-9673-778e-85dd-8d3026178022` |  |
| [`coffee_rating_prediction`](coffee_rating_prediction/) | temporal | 2,369 | 12 | 13 x 1 | `01a111fc-f020-7625-b0b4-3e15565c2a7b` | `dataset_constant_column` |
| [`coil_2000`](coil_2000/) | IID | 9,822 | 85 | 3 x 3 | `01a111fc-ceb4-7695-8b34-df7a285cfcb6` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`concrete_compressive_strength`](concrete_compressive_strength/) | IID | 1,030 | 8 | 10 x 3 | `01a111fc-cee4-7ba9-97fd-b7a0365aad44` | `dataset_duplicate_rows` |
| [`consumer_complaints_1m`](consumer_complaints_1m/) | temporal | 1,811,452 | 12 | 3 x 1 | `01a111fc-f194-75a8-92f0-489647625f28` |  |
| [`cooking_time_1m`](cooking_time_1m/) | temporal | 2,500,000 | 196 | 3 x 1 | `01a111fc-29b5-72ce-95a1-e99f6874a4ee` |  |
| [`covertype`](covertype/) | IID | 581,012 | 14 | 1 x 3 | `01a111fc-5b2f-72b3-983a-85ec312c2e8f` |  |
| [`credit_approval`](credit_approval/) | IID | 690 | 15 | 20 x 3 | `01a111fc-cedf-7a16-9575-fb28a8d57db5` |  |
| [`credit_card_clients_default`](credit_card_clients_default/) | IID | 30,000 | 23 | 3 x 3 | `01a111fc-a3c4-755e-b3fb-ad77ce7129a5` |  |
| [`credit_g`](credit_g/) | IID | 1,000 | 20 | 10 x 3 | `01a111fc-cf4e-7841-a626-e0358b0042c6` |  |
| [`delivery_eta_1m`](delivery_eta_1m/) | temporal | 2,500,000 | 221 | 3 x 1 | `01a111fc-e6b7-7547-8e7f-790705764eb1` |  |
| [`dementia_prediction`](dementia_prediction/) | grouped | 370 | 8 | 20 x 3 | `01a111fc-d5b5-7da4-8ffe-99dd2600b6e0` |  |
| [`diabetes_130_us`](diabetes_130_us/) | IID | 69,973 | 44 | 3 x 3 | `01a111fc-82d1-7838-bf50-fa314882cfef` |  |
| [`diamonds`](diamonds/) | IID | 53,940 | 9 | 3 x 3 | `01a111fc-d45e-7211-98d8-ee98e5da227f` |  |
| [`drug_induced_autoimmunity_prediction`](drug_induced_autoimmunity_prediction/) | IID | 597 | 177 | 20 x 3 | `01a111fc-d491-7412-a5c5-884df72be349` | `dataset_identifier_column` |
| [`early_learning_predictors`](early_learning_predictors/) | grouped | 18,874 | 743 | 3 x 3 | `01a111fc-59b5-7e83-8468-0ee2628e95b3` | `dataset_duplicate_columns` |
| [`early_stage_diabetes_risk_prediction`](early_stage_diabetes_risk_prediction/) | IID | 251 | 16 | 20 x 3 | `01a111fc-d514-780d-9d44-d5ec9c6d44d3` |  |
| [`ecoli_proteins`](ecoli_proteins/) | IID | 327 | 6 | 20 x 3 | `01a111fc-d4ff-7dda-987a-8119d986e5f1` |  |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/) | grouped | 1,296,316 | 109 | 1 x 3 | `01a111fb-0e27-7b57-8daa-3b40b8ba0e11` |  |
| [`emscad`](emscad/) | grouped | 16,116 | 17 | 3 x 3 | `01a111fc-7ebc-7346-942e-09517a07829e` |  |
| [`eryhemato_squamous_disease`](eryhemato_squamous_disease/) | IID | 366 | 12 | 20 x 3 | `01a111fc-a1c3-79c0-8d48-48221a6702fe` |  |
| [`fiat_500`](fiat_500/) | IID | 1,538 | 7 | 10 x 3 | `01a111fc-a2a5-7dc8-a4bd-97f6a8bb5780` | `dataset_duplicate_rows` |
| [`food_delivery_time`](food_delivery_time/) | IID | 45,451 | 9 | 3 x 3 | `01a111fc-d7f1-7b0c-9bd0-d3f8b8afcfae` |  |
| [`forensic_glass_identification`](forensic_glass_identification/) | IID | 214 | 9 | 20 x 3 | `01a111fc-a27d-7f21-999e-eb82f18aaf21` |  |
| [`forest_fires`](forest_fires/) | IID | 517 | 12 | 20 x 3 | `01a111fc-a4a0-72df-82ce-c3f0eed0000e` | `dataset_conflicting_duplicate_rows` |
| [`gallstone_disease`](gallstone_disease/) | IID | 319 | 38 | 20 x 3 | `01a111fc-d8af-7a12-816b-905e5085bf7f` |  |
| [`garments_worker_productivity`](garments_worker_productivity/) | temporal | 1,197 | 15 | 30 x 1 | `01a111fc-d4cc-702b-99bc-38e5c3ea0aa4` |  |
| [`give_me_some_credit`](give_me_some_credit/) | IID | 150,000 | 10 | 3 x 3 | `01a111fc-8c6a-7513-9b7c-cd856ad168b6` |  |
| [`heart_disease_cleveland`](heart_disease_cleveland/) | IID | 303 | 13 | 20 x 3 | `01a111fc-a515-7938-a082-7add803d38c2` |  |
| [`heart_disease_hungary`](heart_disease_hungary/) | IID | 294 | 13 | 20 x 3 | `01a111fc-a844-7407-8ace-a685fd00b279` | `dataset_constant_column` |
| [`heart_disease_va_long_beach`](heart_disease_va_long_beach/) | IID | 200 | 13 | 20 x 3 | `01a111fc-aa5f-797c-b591-225fad0157b7` | `dataset_constant_column` |
| [`heart_failure_followup_survival`](heart_failure_followup_survival/) | IID | 299 | 11 | 20 x 3 | `01a111fc-aabc-7a8e-a658-bf88e5751de1` |  |
| [`heloc`](heloc/) | IID | 10,459 | 23 | 3 x 3 | `01a111fc-afbf-7df2-bc38-76e6a79a64eb` | `dataset_missing_value_sentinel`, `dataset_duplicate_rows` |
| [`hepatitis_c_prediction`](hepatitis_c_prediction/) | IID | 608 | 11 | 20 x 3 | `01a111fc-da06-7344-b05c-32c0c4829da1` |  |
| [`hepatitis_survival_prediction`](hepatitis_survival_prediction/) | IID | 155 | 19 | 20 x 3 | `01a111fc-dbca-7d8e-ab0c-322d3d816ede` |  |
| [`hiva_agnostic`](hiva_agnostic/) | IID | 3,845 | 1,518 | 3 x 3 | `01a111fc-4ac0-7d5e-ace0-8fd1e51ccbd8` | `dataset_pure_feature_value` |
| [`home_credit_default_risk`](home_credit_default_risk/) | IID | 307,507 | 504 | 3 x 3 | `01a111fb-c9a4-79ac-b807-b4b9dffd8068` |  |
| [`home_credit_default_stability_1m`](home_credit_default_stability_1m/) | temporal | 1,224,927 | 710 | 3 x 1 | `01a111fc-2b8d-77ef-a922-3ea3b96a716e` |  |
| [`homesite_quote_conversion`](homesite_quote_conversion/) | IID | 260,753 | 295 | 3 x 3 | `01a111fc-15c3-7dfe-bf9e-39d8ab56f8f4` | `dataset_constant_column`, `dataset_missing_value_label` |
| [`horse_colic_survival`](horse_colic_survival/) | IID | 344 | 20 | 20 x 3 | `01a111fc-df0b-7d08-9ad5-3bfee18c9b55` |  |
| [`hotel_booking_demand`](hotel_booking_demand/) | temporal | 81,418 | 28 | 9 x 1 | `01a111fc-83ac-7d29-9b51-a07539b9d67c` |  |
| [`houses`](houses/) | IID | 19,675 | 8 | 3 x 3 | `01a111fc-e060-707f-b68e-7c2be9c5182f` |  |
| [`hr_analytics`](hr_analytics/) | IID | 19,158 | 12 | 3 x 3 | `01a111fc-e13c-73b1-a5b6-46586d1602ca` |  |
| [`ieee_fraud_detection`](ieee_fraud_detection/) | temporal | 590,540 | 435 | 3 x 1 | `01a111fa-fc65-735f-bcbe-b5845dbfe917` |  |
| [`immoscout_german_house_prices`](immoscout_german_house_prices/) | IID | 10,317 | 23 | 3 x 3 | `01a111fc-e1d2-7c5b-a5e9-bb8bb2b58ed9` |  |
| [`in_vehicle_coupon_recommendation`](in_vehicle_coupon_recommendation/) | grouped | 12,684 | 24 | 3 x 3 | `01a111fc-e38e-7ad4-90c9-b80013f7640e` |  |
| [`indian_liver_patient_dataset`](indian_liver_patient_dataset/) | IID | 583 | 10 | 20 x 3 | `01a111fc-e244-78f8-9686-1c2a0bf3b820` | `dataset_duplicate_rows` |
| [`jm1`](jm1/) | IID | 8,736 | 21 | 3 x 3 | `01a111fc-b2fb-721e-9fd2-4f7373b53bca` |  |
| [`kdd_cup_09_appetency`](kdd_cup_09_appetency/) | IID | 50,000 | 212 | 3 x 3 | `01a111fc-4f06-781e-a57e-d46ef749395b` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`kick`](kick/) | temporal | 72,983 | 32 | 9 x 1 | `01a111fc-8ab4-7b2f-9955-2cc583c9e979` |  |
| [`kickstarter`](kickstarter/) | temporal | 187,117 | 12 | 3 x 1 | `01a111fc-1005-78e7-8906-36e684a9081e` |  |
| [`labour_inspection_compliance`](labour_inspection_compliance/) | IID | 63,634 | 376 | 3 x 3 | `01a111fb-c91d-7b12-beaf-b56406cfc014` | `dataset_constant_column` |
| [`lending_club`](lending_club/) | temporal | 609,544 | 81 | 3 x 1 | `01a111fb-70c3-7e45-af56-3ed5e3a90f7f` |  |
| [`ljubljana_breast_cancer`](ljubljana_breast_cancer/) | IID | 286 | 9 | 20 x 3 | `01a111fc-e2f6-79bc-bc94-8e4779cb09a2` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`ljubljana_primary_tumor`](ljubljana_primary_tumor/) | IID | 302 | 17 | 20 x 3 | `01a111fc-e43e-74ec-8af2-b710f7045924` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`lung_cancer`](lung_cancer/) | IID | 197 | 12,600 | 20 x 3 | `01a111fa-f2d2-7673-a757-142728cdfd4c` | `dataset_missing_value_sentinel` |
| [`lung_cancer_epithelial_genexp`](lung_cancer_epithelial_genexp/) | IID | 187 | 22,215 | 20 x 3 | `01a111fa-e441-7be0-b4cb-2b1c80c2c167` |  |
| [`maps_router_eta_1m`](maps_router_eta_1m/) | temporal | 2,500,000 | 988 | 3 x 1 | `01a111ff-5cb6-76bc-bc05-231ccdac19d0` |  |
| [`marketing_campaign`](marketing_campaign/) | IID | 2,240 | 25 | 10 x 3 | `01a111fc-b058-7ad2-9e81-45d916a3052c` | `dataset_duplicate_rows` |
| [`mercari_price_suggestion`](mercari_price_suggestion/) | IID | 1,482,486 | 6 | 1 x 3 | `01a111fb-0462-74d5-bdd8-89846cb8d091` |  |
| [`mercedes_benz_greener_manufacturing`](mercedes_benz_greener_manufacturing/) | temporal | 4,204 | 371 | 9 x 1 | `01a111fc-ad75-71b3-a65b-bf31e51792f6` | `dataset_constant_column`, `dataset_duplicate_columns`, `meta_tags_missing_regime` |
| [`miami_housing`](miami_housing/) | IID | 13,776 | 15 | 3 x 3 | `01a111fc-b2f3-70cf-951c-6cf119716e45` |  |
| [`mic`](mic/) | IID | 1,699 | 102 | 10 x 3 | `01a111fc-88a2-7b7e-86e3-99576cde774e` |  |
| [`micro_mass`](micro_mass/) | grouped | 571 | 1,082 | 20 x 3 | `01a111fc-8b57-73f7-bb59-b6d7ab7a6881` |  |
| [`musk`](musk/) | grouped (per group: any) | 6,598 | 166 | 20 x 3 | `01a111fc-e484-7212-b264-ac00bcffbd4d` | `dataset_missing_value_sentinel` |
| [`mutual_funds_india`](mutual_funds_india/) | IID | 793 | 11 | 10 x 3 | `01a111fc-b2ce-7d31-a579-1f6e9371eade` |  |
| [`naticusdroid_android_permissions_dataset`](naticusdroid_android_permissions_dataset/) | IID | 7,491 | 85 | 3 x 3 | `01a111fc-e77d-7818-aca7-ffb8763af26a` | `dataset_conflicting_duplicate_rows`, `dataset_pure_feature_value` |
| [`obesity_estimation`](obesity_estimation/) | IID | 498 | 14 | 20 x 3 | `01a111fc-b36e-7939-b271-e858cafffee4` | `dataset_duplicate_rows` |
| [`online_shoppers_purchasing_intention_dataset`](online_shoppers_purchasing_intention_dataset/) | IID | 6,875 | 16 | 3 x 3 | `01a111fc-b5f1-748b-a755-99b0a7c15a25` |  |
| [`otto_group_product_classification_challenge`](otto_group_product_classification_challenge/) | IID | 61,878 | 93 | 3 x 3 | `01a111fc-7288-72b4-8ceb-e6f796d2a623` |  |
| [`pancreatic_cancer_mouse_detection`](pancreatic_cancer_mouse_detection/) | grouped | 181 | 6,771 | 20 x 3 | `01a111fc-4ee4-7a63-9a02-e4ac045fac79` | `dataset_missing_value_sentinel` |
| [`polish_companies_bankruptcy`](polish_companies_bankruptcy/) | IID | 5,790 | 64 | 3 x 3 | `01a111fc-ea70-7bb1-9ee9-8875a112b674` |  |
| [`porto_seguro`](porto_seguro/) | IID | 595,206 | 37 | 1 x 3 | `01a111fb-fc94-70f9-9598-6ab89e8b220d` |  |
| [`predict_students_dropout_and_academic_success`](predict_students_dropout_and_academic_success/) | IID | 4,424 | 36 | 3 x 3 | `01a111fc-b7bd-7c0b-a919-1a848957caf4` |  |
| [`pva_revenue_prediction_kddcup98`](pva_revenue_prediction_kddcup98/) | IID | 144,095 | 477 | 3 x 3 | `01a111fb-cc18-7704-b06a-adfc58623727` | `dataset_constant_column`, `dataset_missing_value_label`, `meta_license_unknown` |
| [`qsar_aquatic_toxicity`](qsar_aquatic_toxicity/) | IID | 546 | 8 | 20 x 3 | `01a111fc-b7f2-70ec-b160-9c69d2d62b73` | `dataset_conflicting_duplicate_rows` |
| [`qsar_biodeg`](qsar_biodeg/) | IID | 1,054 | 41 | 10 x 3 | `01a111fc-bbf4-7a48-86aa-22bfb52b8d59` |  |
| [`qsar_fish_toxicity`](qsar_fish_toxicity/) | IID | 908 | 6 | 10 x 3 | `01a111fc-ec16-7add-afb7-17f93dcaa3d4` | `dataset_conflicting_duplicate_rows` |
| [`qsar_tid_11`](qsar_tid_11/) | IID | 5,741 | 1,024 | 3 x 3 | `01a111fc-77d3-7128-8497-210288cab270` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`regensburg_pediatric_appendicitis`](regensburg_pediatric_appendicitis/) | IID | 763 | 51 | 10 x 3 | `01a111fc-ee89-74ad-b25b-309464691fe6` |  |
| [`rossmann_store_sales`](rossmann_store_sales/) | temporal | 844,392 | 15 | 3 x 1 | `01a111fc-4eab-762b-baa6-12fb81c7e2ee` |  |
| [`santander_customer_satisfaction`](santander_customer_satisfaction/) | IID | 71,080 | 307 | 3 x 3 | `01a111fc-12c0-72fc-95ab-3a7ad03daa2b` | `dataset_pure_feature_value` |
| [`santander_customer_transaction_prediction`](santander_customer_transaction_prediction/) | IID | 200,000 | 200 | 3 x 3 | `01a111fa-f277-7533-bac1-a15ddbf6a38d` |  |
| [`santander_transaction_value`](santander_transaction_value/) | IID | 4,447 | 540 | 3 x 3 | `01a111fb-c8c5-7b20-b3a0-528353375933` |  |
| [`sat11_hand_algo_runtime`](sat11_hand_algo_runtime/) | grouped (per group: select_min) | 1,840 | 169 | 10 x 3 | `01a111fc-eda8-7830-9b0d-905bf0c5bc1d` | `dataset_constant_column` |
| [`sberbank_housing_market_forecasting`](sberbank_housing_market_forecasting/) | temporal | 27,195 | 386 | 5 x 1 | `01a111fc-67ad-73f9-9657-30238d911c5b` |  |
| [`sdss_17`](sdss_17/) | IID | 99,999 | 8 | 3 x 3 | `01a111fc-9499-7f77-abbe-45c6b8ec8291` |  |
| [`sepsis_prediction_1m`](sepsis_prediction_1m/) | grouped | 1,499,997 | 42 | 1 x 3 | `01a111fc-109e-7d32-85ac-ecdf6eea551e` |  |
| [`sepsis_survival_minimal_clinical_records`](sepsis_survival_minimal_clinical_records/) | IID | 110,204 | 3 | 3 x 3 | `01a111fc-94f7-7c86-b795-2ecaea21d5dd` | `dataset_duplicate_rows` |
| [`sf_permit_time`](sf_permit_time/) | temporal | 99,847 | 37 | 9 x 1 | `01a111fb-de83-7f11-84c7-a33ce2f7887a` |  |
| [`south_africa_coronary_heart_disease`](south_africa_coronary_heart_disease/) | IID | 462 | 9 | 20 x 3 | `01a111fc-ed62-786a-ac41-9c1deb571902` |  |
| [`splice`](splice/) | IID | 3,190 | 60 | 10 x 3 | `01a111fc-bcd5-72b6-a429-8e9aea326bca` | `dataset_duplicate_rows` |
| [`student_portuguese_performance`](student_portuguese_performance/) | IID | 649 | 30 | 20 x 3 | `01a111fc-bd82-7068-93bd-0d20f8e4fea0` |  |
| [`superconductivity`](superconductivity/) | grouped | 21,263 | 81 | 3 x 3 | `01a11308-e9d1-7f71-b3e3-e172887ea0d9` | `dataset_conflicting_duplicate_rows` |
| [`taiwanese_bankruptcy_prediction`](taiwanese_bankruptcy_prediction/) | IID | 6,819 | 92 | 3 x 3 | `01a111fc-bec6-75e8-b645-262ad3c192c3` |  |
| [`thyroid_discordant`](thyroid_discordant/) | IID | 3,711 | 26 | 10 x 3 | `01a111fc-bea0-79f8-b0a4-5d00de089637` |  |
| [`tour_travels_churn`](tour_travels_churn/) | IID | 954 | 6 | 10 x 3 | `01a111fc-edc9-7641-b79f-dc54c06b0b31` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows`, `meta_bibtex_latex_hazard` |
| [`video_transcoding_time_prediction`](video_transcoding_time_prediction/) | grouped | 68,784 | 18 | 3 x 3 | `01a111fc-7b5a-7853-8e13-f42ccc0c3b03` |  |
| [`website_phishing`](website_phishing/) | IID | 1,353 | 9 | 10 x 3 | `01a111fc-ef84-7289-a58d-5a6ca10a3a3f` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`wids_diabetes_mellitus`](wids_diabetes_mellitus/) | IID | 127,358 | 181 | 3 x 3 | `01a111fc-032c-7d1f-a669-78dc5d1cd86b` |  |
| [`wine_quality`](wine_quality/) | IID | 5,320 | 12 | 3 x 3 | `01a111fc-f00a-7053-95dc-e278996515ca` |  |
| [`wine_world_cost`](wine_world_cost/) | IID | 1,279 | 14 | 10 x 3 | `01a111fc-bf3e-75e4-bd32-d489275dd877` |  |
<!-- datasets:end -->
