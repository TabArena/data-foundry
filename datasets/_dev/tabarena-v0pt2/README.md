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

The 128 datasets were built on 2026-10-06 from the definitions in this folder (the UUIDs below), as container
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
| [`5g_energy_consumption`](5g_energy_consumption/) | grouped | 92,629 | 21 | 3 x 3 | `01a11191-233a-7c01-9cf4-45515d30cb4b` |  |
| [`acquire_valued_shoppers_challenge`](acquire_valued_shoppers_challenge/) | temporal | 160,057 | 111 | 5 x 1 | `01a11191-02e4-76aa-a95c-8d4406216b18` |  |
| [`airfoil_self_noise`](airfoil_self_noise/) | IID | 1,503 | 5 | 10 x 3 | `01a11191-5cbe-7b83-90ce-4f445afb2a34` |  |
| [`allstate_claims_severity`](allstate_claims_severity/) | IID | 188,317 | 130 | 3 x 3 | `01a11191-0c86-7fe9-9fb2-11530080c5fe` |  |
| [`amazon_employee_access`](amazon_employee_access/) | IID | 32,769 | 9 | 3 x 3 | `01a11191-6319-7a2c-9c0e-86a6675fc98a` | `dataset_pure_feature_value` |
| [`amex_non_iid_1m`](amex_non_iid_1m/) | grouped (per group: last) | 1,500,000 | 190 | 1 x 3 | `01a11190-c510-7fc4-9dad-f976c0ff79f1` | `dataset_missing_value_sentinel` |
| [`anes_voting_2026`](anes_voting_2026/) | temporal | 48,587 | 261 | 9 x 1 | `01a11190-6c97-7d29-a0ff-963610741e1f` |  |
| [`aps_failure`](aps_failure/) | IID | 76,000 | 170 | 3 x 3 | `01a11190-cd17-7165-bd1e-ebb933111320` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`asp_potassco_classification`](asp_potassco_classification/) | grouped | 1,212 | 137 | 10 x 3 | `01a11191-64f1-7d15-aa6f-cea6847b7147` | `dataset_constant_column` |
| [`audiology_diagnosis`](audiology_diagnosis/) | IID | 195 | 65 | 20 x 3 | `01a11191-6752-703a-9930-a7583503a5c4` |  |
| [`bad_customer_detection`](bad_customer_detection/) | IID | 1,723 | 13 | 10 x 3 | `01a11191-6770-7227-bdc9-3d761133971c` |  |
| [`bank_customer_churn`](bank_customer_churn/) | IID | 10,000 | 10 | 3 x 3 | `01a11191-6944-7875-b29c-110e9289d253` |  |
| [`bank_marketing`](bank_marketing/) | IID | 45,211 | 13 | 3 x 3 | `01a11191-6ab7-7d07-98ae-00bf39d2a4d9` | `dataset_missing_value_sentinel` |
| [`biogeographical_ancestry_prediction`](biogeographical_ancestry_prediction/) | IID | 607 | 102 | 20 x 3 | `01a11191-30d1-7005-851d-272125d77ffe` |  |
| [`biomechanical_orthopaedic_prediction`](biomechanical_orthopaedic_prediction/) | IID | 310 | 6 | 20 x 3 | `01a11191-6a8b-7d1a-b794-2f9e4c70ad19` |  |
| [`bioresponse`](bioresponse/) | IID | 3,751 | 1,776 | 3 x 3 | `01a11190-e899-7c60-a82f-3c93d11ecbd9` |  |
| [`blood_tests_drink_prediction`](blood_tests_drink_prediction/) | IID | 345 | 5 | 20 x 3 | `01a11191-94e7-75a4-b189-60dea33df5d2` | `dataset_duplicate_rows` |
| [`blood_transfusion`](blood_transfusion/) | IID | 748 | 4 | 20 x 3 | `01a11191-9b9b-73e7-8a35-dca35228c2e7` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`body_density_prediction`](body_density_prediction/) | IID | 252 | 13 | 20 x 3 | `01a11191-a189-75d7-a082-b1d97c4153f5` |  |
| [`california_house_prices_2020`](california_house_prices_2020/) | temporal | 41,528 | 41 | 3 x 1 | `01a11191-2ff0-779a-a11a-f21d778c64c9` |  |
| [`cardiotocography`](cardiotocography/) | grouped | 2,126 | 23 | 10 x 3 | `01a11191-7d99-7aa5-960c-b1e675f56a39` | `dataset_constant_column` |
| [`churn`](churn/) | IID | 5,000 | 19 | 3 x 3 | `01a11191-a193-7bd1-a5f2-7593eb389b3c` |  |
| [`cirrhosis_patient_survival_prediction`](cirrhosis_patient_survival_prediction/) | IID | 161 | 17 | 20 x 3 | `01a11191-a18b-73c8-829a-81687d227f5c` |  |
| [`climate_model_weather_forecasting_1m`](climate_model_weather_forecasting_1m/) | temporal | 2,115,283 | 99 | 3 x 1 | `01a11190-ed52-7cd5-8181-40b82de9d20b` |  |
| [`clock_protein_toxicity`](clock_protein_toxicity/) | IID | 171 | 1,117 | 20 x 3 | `01a11191-3659-71fd-8010-d2cd4db33cc3` |  |
| [`coffee_rating_prediction`](coffee_rating_prediction/) | temporal | 2,369 | 12 | 13 x 1 | `01a11191-9ce9-7ae4-b341-107ad5bb22f4` | `dataset_constant_column` |
| [`coil_2000`](coil_2000/) | IID | 9,822 | 85 | 3 x 3 | `01a11191-8081-71c6-99f9-15801ed5bc63` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`concrete_compressive_strength`](concrete_compressive_strength/) | IID | 1,030 | 8 | 10 x 3 | `01a11191-a206-7b43-8326-902a99f9493a` | `dataset_duplicate_rows` |
| [`consumer_complaints_1m`](consumer_complaints_1m/) | temporal | 1,811,452 | 12 | 3 x 1 | `01a11191-c5be-7cbf-bcdc-6dfb1ffd743c` |  |
| [`cooking_time_1m`](cooking_time_1m/) | temporal | 2,500,000 | 196 | 3 x 1 | `01a11191-5eeb-7752-b2a6-0e285f9ec0aa` |  |
| [`covertype`](covertype/) | IID | 581,012 | 14 | 1 x 3 | `01a11191-1459-73b7-a8d7-bf59bc25d895` |  |
| [`credit_approval`](credit_approval/) | IID | 690 | 15 | 20 x 3 | `01a11191-a23f-7268-8ff9-23cea2bac0ea` |  |
| [`credit_card_clients_default`](credit_card_clients_default/) | IID | 30,000 | 23 | 3 x 3 | `01a11191-3c35-718e-a11e-f177b87a1883` |  |
| [`credit_g`](credit_g/) | IID | 1,000 | 20 | 10 x 3 | `01a11191-a33d-7475-a7b5-a4ed12dc1ef1` |  |
| [`delivery_eta_1m`](delivery_eta_1m/) | temporal | 2,500,000 | 221 | 3 x 1 | `01a11192-a6a7-7372-8220-f0b5c52cc3ae` |  |
| [`dementia_prediction`](dementia_prediction/) | grouped | 370 | 9 | 20 x 3 | `01a11191-820a-7ba8-8b75-3ff9248bfa5f` |  |
| [`diabetes_130_us`](diabetes_130_us/) | IID | 69,973 | 44 | 3 x 3 | `01a11191-412c-7bdf-acc4-6e6734fc9a8a` |  |
| [`diamonds`](diamonds/) | IID | 53,940 | 9 | 3 x 3 | `01a11191-80c2-7f3f-a583-03f519bc26f7` |  |
| [`drug_induced_autoimmunity_prediction`](drug_induced_autoimmunity_prediction/) | IID | 597 | 177 | 20 x 3 | `01a11191-812d-7dce-a917-1e0cc8a5fe14` | `dataset_identifier_column` |
| [`early_learning_predictors`](early_learning_predictors/) | grouped | 18,874 | 744 | 3 x 3 | `01a11190-f36c-76ca-a386-b00582a71674` | `dataset_duplicate_columns` |
| [`early_stage_diabetes_risk_prediction`](early_stage_diabetes_risk_prediction/) | IID | 251 | 16 | 20 x 3 | `01a11191-a382-7a42-8d1a-12466e7af801` |  |
| [`ecoli_proteins`](ecoli_proteins/) | IID | 327 | 6 | 20 x 3 | `01a11191-a850-76e9-8b59-f560a2b09472` |  |
| [`electric_motor_temperature_prediction`](electric_motor_temperature_prediction/) | grouped | 1,296,316 | 110 | 1 x 3 | `01a1118f-c6ee-7076-ae66-f2ac19eee8f2` |  |
| [`emscad`](emscad/) | grouped | 16,116 | 18 | 3 x 3 | `01a11191-33bc-74d2-ac80-3e98063d23c2` |  |
| [`eryhemato_squamous_disease`](eryhemato_squamous_disease/) | IID | 366 | 12 | 20 x 3 | `01a11191-aadc-7e12-a102-e16562cee512` |  |
| [`fiat_500`](fiat_500/) | IID | 1,538 | 7 | 10 x 3 | `01a11191-b66b-7b06-9b21-e264518558cf` | `dataset_duplicate_rows` |
| [`food_delivery_time`](food_delivery_time/) | IID | 45,451 | 9 | 3 x 3 | `01a11191-8267-77d0-a45f-9739ff3b3340` |  |
| [`forensic_glass_identification`](forensic_glass_identification/) | IID | 214 | 9 | 20 x 3 | `01a11191-b7ee-7a77-a0f1-4300ba47f8c3` |  |
| [`forest_fires`](forest_fires/) | IID | 517 | 12 | 20 x 3 | `01a11191-b856-721f-a0f5-4aba02658649` | `dataset_conflicting_duplicate_rows` |
| [`gallstone_disease`](gallstone_disease/) | IID | 319 | 38 | 20 x 3 | `01a11191-833d-73c6-97e1-0643fc2d6b6c` |  |
| [`garments_worker_productivity`](garments_worker_productivity/) | temporal | 1,197 | 15 | 30 x 1 | `01a11191-afba-78de-84e3-7bb317cd8665` |  |
| [`give_me_some_credit`](give_me_some_credit/) | IID | 150,000 | 10 | 3 x 3 | `01a11191-430b-73b9-a4dd-59db60e76e6d` |  |
| [`healthcare_insurance_expenses`](healthcare_insurance_expenses/) | IID | 1,338 | 6 | 10 x 3 | `01a11191-b87f-7df8-a15e-1b5a3346a2b5` |  |
| [`heart_disease_cleveland`](heart_disease_cleveland/) | IID | 303 | 13 | 20 x 3 | `01a11191-b920-7b63-a4b0-be6d1b4f0c6e` |  |
| [`heart_disease_hungary`](heart_disease_hungary/) | IID | 294 | 13 | 20 x 3 | `01a11191-bab5-71bb-9274-51e984826b93` | `dataset_constant_column` |
| [`heart_disease_va_long_beach`](heart_disease_va_long_beach/) | IID | 200 | 13 | 20 x 3 | `01a11191-bc4f-7be5-a9b6-979ab150bccb` | `dataset_constant_column` |
| [`heart_failure_followup_survival`](heart_failure_followup_survival/) | IID | 299 | 11 | 20 x 3 | `01a11191-be7f-7bca-87e5-6fca817d30ba` |  |
| [`heloc`](heloc/) | IID | 10,459 | 23 | 3 x 3 | `01a11191-c354-7c3d-8afd-a026d562a375` | `dataset_missing_value_sentinel`, `dataset_duplicate_rows` |
| [`hepatitis_c_prediction`](hepatitis_c_prediction/) | IID | 608 | 11 | 20 x 3 | `01a11191-c997-7386-a391-8dfcaae5b97a` |  |
| [`hepatitis_survival_prediction`](hepatitis_survival_prediction/) | IID | 155 | 19 | 20 x 3 | `01a11191-ca0b-7550-a0fe-720cad11b70a` |  |
| [`hiva_agnostic`](hiva_agnostic/) | IID | 3,845 | 1,518 | 3 x 3 | `01a11190-d968-7f4c-9a3c-c7d1cae62a30` | `dataset_pure_feature_value` |
| [`home_credit_default_risk`](home_credit_default_risk/) | IID | 307,507 | 504 | 3 x 3 | `01a11190-911e-76ab-bc64-f291692f39f7` |  |
| [`home_credit_default_stability_1m`](home_credit_default_stability_1m/) | temporal | 1,224,927 | 710 | 3 x 1 | `01a11190-62b3-7529-b8fd-e5ea5439dfa5` |  |
| [`homesite_quote_conversion`](homesite_quote_conversion/) | IID | 260,753 | 295 | 3 x 3 | `01a11191-1593-7081-be0a-df66953b5c15` | `dataset_constant_column`, `dataset_missing_value_label` |
| [`horse_colic_survival`](horse_colic_survival/) | IID | 344 | 20 | 20 x 3 | `01a11191-ca60-7384-910a-019da61288a4` |  |
| [`hotel_booking_demand`](hotel_booking_demand/) | temporal | 81,418 | 28 | 9 x 1 | `01a11191-43de-75d1-8d55-d1ef2a848559` |  |
| [`houses`](houses/) | IID | 19,675 | 8 | 3 x 3 | `01a11191-cc2d-7228-bde0-03602ae96471` |  |
| [`hr_analytics`](hr_analytics/) | IID | 19,158 | 12 | 3 x 3 | `01a11191-cb27-7668-968c-d8e83b66db19` |  |
| [`ieee_fraud_detection`](ieee_fraud_detection/) | temporal | 590,540 | 435 | 3 x 1 | `01a11190-4892-7cab-b756-7367b919e0ad` |  |
| [`immoscout_german_house_prices`](immoscout_german_house_prices/) | IID | 10,317 | 23 | 3 x 3 | `01a11191-85a4-7680-83c3-0a898f32a9e2` |  |
| [`in_vehicle_coupon_recommendation`](in_vehicle_coupon_recommendation/) | grouped | 12,684 | 25 | 3 x 3 | `01a11191-87c5-7fd4-96b7-34fd5eb7d14b` |  |
| [`indian_liver_patient_dataset`](indian_liver_patient_dataset/) | IID | 583 | 10 | 20 x 3 | `01a11191-cad0-710a-89c9-546914224a18` | `dataset_duplicate_rows` |
| [`jm1`](jm1/) | IID | 8,736 | 21 | 3 x 3 | `01a11191-8bdf-7139-8a99-998e81bb1596` |  |
| [`kdd_cup_09_appetency`](kdd_cup_09_appetency/) | IID | 50,000 | 212 | 3 x 3 | `01a11191-0b04-751e-a24a-ce768651f100` | `dataset_constant_column`, `dataset_pure_feature_value` |
| [`kick`](kick/) | temporal | 72,983 | 32 | 9 x 1 | `01a11191-2bb7-7949-83a9-f40803cf6445` |  |
| [`kickstarter`](kickstarter/) | temporal | 187,117 | 12 | 3 x 1 | `01a1118f-d3e3-72e7-9fb5-50e718ae3b68` |  |
| [`labour_inspection_compliance`](labour_inspection_compliance/) | IID | 63,634 | 376 | 3 x 3 | `01a1118f-c85a-73f9-a1d9-90f43014e947` | `dataset_constant_column` |
| [`lending_club`](lending_club/) | temporal | 609,544 | 81 | 3 x 1 | `01a11190-2301-71d2-ae57-df0b516eed79` |  |
| [`ljubljana_breast_cancer`](ljubljana_breast_cancer/) | IID | 286 | 9 | 20 x 3 | `01a11191-ce34-7502-a02e-67d7f690a32f` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`ljubljana_primary_tumor`](ljubljana_primary_tumor/) | IID | 302 | 17 | 20 x 3 | `01a11191-ce7c-7717-b17f-8bdaccc0c10c` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`lung_cancer`](lung_cancer/) | IID | 197 | 12,600 | 20 x 3 | `01a11190-3f18-74de-9a6d-4bc2f4b76280` | `dataset_missing_value_sentinel` |
| [`lung_cancer_epithelial_genexp`](lung_cancer_epithelial_genexp/) | IID | 187 | 22,215 | 20 x 3 | `01a1118f-9e32-777e-a5f6-b3e5c8cfa841` |  |
| [`maps_router_eta_1m`](maps_router_eta_1m/) | temporal | 2,500,000 | 988 | 3 x 1 | `01a11197-6655-7db4-8dce-0dfd1dc76ed1` |  |
| [`marketing_campaign`](marketing_campaign/) | IID | 2,240 | 25 | 10 x 3 | `01a11191-d064-7c27-abcd-bcb947e441d0` | `dataset_duplicate_rows` |
| [`mercari_price_suggestion`](mercari_price_suggestion/) | IID | 1,482,486 | 6 | 1 x 3 | `01a1118f-ba40-79d1-9973-7b496d476785` |  |
| [`mercedes_benz_greener_manufacturing`](mercedes_benz_greener_manufacturing/) | temporal | 4,204 | 371 | 9 x 1 | `01a11191-8766-7fd7-9a98-43cdfad5cdde` | `dataset_constant_column`, `dataset_duplicate_columns`, `meta_tags_missing_regime` |
| [`miami_housing`](miami_housing/) | IID | 13,776 | 15 | 3 x 3 | `01a11191-d44a-7743-bf8c-37ae22da6115` |  |
| [`mic`](mic/) | IID | 1,699 | 102 | 10 x 3 | `01a11191-4e6f-765b-bd8a-3259484499b0` |  |
| [`micro_mass`](micro_mass/) | grouped | 571 | 1,083 | 20 x 3 | `01a11191-3093-7c9c-b3e6-49b688d785c7` |  |
| [`musk`](musk/) | grouped (per group: any) | 6,598 | 167 | 20 x 3 | `01a11191-8f43-7a2b-a6b8-0b77bfadaa43` | `dataset_missing_value_sentinel` |
| [`mutual_funds_india`](mutual_funds_india/) | IID | 793 | 11 | 10 x 3 | `01a11191-de4b-7f3f-bc36-f88469de0c2a` |  |
| [`naticusdroid_android_permissions_dataset`](naticusdroid_android_permissions_dataset/) | IID | 7,491 | 85 | 3 x 3 | `01a11191-8f6c-7e4d-96d2-5e05c9552aa7` | `dataset_conflicting_duplicate_rows`, `dataset_pure_feature_value` |
| [`obesity_estimation`](obesity_estimation/) | IID | 498 | 14 | 20 x 3 | `01a11191-deea-7d9a-97d1-984916c2e8c0` | `dataset_duplicate_rows` |
| [`online_shoppers_purchasing_intention_dataset`](online_shoppers_purchasing_intention_dataset/) | IID | 6,875 | 16 | 3 x 3 | `01a11191-df61-7834-8ecd-112fdac6fd13` |  |
| [`otto_group_product_classification_challenge`](otto_group_product_classification_challenge/) | IID | 61,878 | 93 | 3 x 3 | `01a11191-5070-7595-b2ba-bd1ac13a1add` |  |
| [`pancreatic_cancer_mouse_detection`](pancreatic_cancer_mouse_detection/) | grouped | 181 | 6,772 | 20 x 3 | `01a11190-ecff-777c-948d-fdf9eaa1ab6d` | `dataset_missing_value_sentinel` |
| [`physiochemical_protein`](physiochemical_protein/) | IID | 45,730 | 9 | 3 x 3 | `01a11191-e0d0-7b45-a12e-0e5a658aaa0d` | `dataset_duplicate_rows` |
| [`polish_companies_bankruptcy`](polish_companies_bankruptcy/) | IID | 5,790 | 64 | 3 x 3 | `01a11191-9039-755b-aded-211521c0c8e3` |  |
| [`porto_seguro`](porto_seguro/) | IID | 595,206 | 37 | 1 x 3 | `01a11190-6bf9-7ab9-8c04-044ef7b9de7f` |  |
| [`predict_students_dropout_and_academic_success`](predict_students_dropout_and_academic_success/) | IID | 4,424 | 36 | 3 x 3 | `01a11191-e1c1-7a1e-a6c0-27b25c8071d3` |  |
| [`pva_revenue_prediction_kddcup98`](pva_revenue_prediction_kddcup98/) | IID | 144,095 | 477 | 3 x 3 | `01a11190-b582-7779-8ee6-9f3d4b55825c` | `dataset_constant_column`, `dataset_missing_value_label`, `meta_license_unknown` |
| [`qsar_aquatic_toxicity`](qsar_aquatic_toxicity/) | IID | 546 | 8 | 20 x 3 | `01a11191-e1e8-7c64-adc5-ec401f8db2ba` | `dataset_conflicting_duplicate_rows` |
| [`qsar_biodeg`](qsar_biodeg/) | IID | 1,054 | 41 | 10 x 3 | `01a11191-e259-79b9-879f-f763ddd3adcb` |  |
| [`qsar_fish_toxicity`](qsar_fish_toxicity/) | IID | 908 | 6 | 10 x 3 | `01a11191-e247-78ec-a1f9-e8047c36a3e7` | `dataset_conflicting_duplicate_rows` |
| [`qsar_tid_11`](qsar_tid_11/) | IID | 5,741 | 1,024 | 3 x 3 | `01a11191-154c-7ef3-bd80-3a1f5320c067` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`regensburg_pediatric_appendicitis`](regensburg_pediatric_appendicitis/) | IID | 763 | 51 | 10 x 3 | `01a11191-9112-73da-a73b-344ee1bad337` |  |
| [`rossmann_store_sales`](rossmann_store_sales/) | temporal | 844,392 | 15 | 3 x 1 | `01a11191-13c6-7e9a-aeaa-a7b867670695` |  |
| [`santander_customer_satisfaction`](santander_customer_satisfaction/) | IID | 71,080 | 307 | 3 x 3 | `01a11190-d5de-76c1-83a9-89de35e4df67` | `dataset_pure_feature_value` |
| [`santander_customer_transaction_prediction`](santander_customer_transaction_prediction/) | IID | 200,000 | 200 | 3 x 3 | `01a1118f-ab8b-7c47-afa5-3e4431f35d32` |  |
| [`santander_transaction_value`](santander_transaction_value/) | IID | 4,447 | 540 | 3 x 3 | `01a11190-1039-7bc7-bb74-934aa1ddd446` |  |
| [`sat11_hand_algo_runtime`](sat11_hand_algo_runtime/) | grouped (per group: select_min) | 1,840 | 170 | 10 x 3 | `01a11191-900c-7cf7-8cb0-bbfcac7e5fde` | `dataset_constant_column` |
| [`sberbank_housing_market_forecasting`](sberbank_housing_market_forecasting/) | temporal | 27,195 | 386 | 5 x 1 | `01a11191-0a4d-72af-b626-cd5e836831dd` |  |
| [`sdss_17`](sdss_17/) | IID | 99,999 | 8 | 3 x 3 | `01a11191-91bd-707a-b90e-0f40954d2006` |  |
| [`sepsis_prediction_1m`](sepsis_prediction_1m/) | grouped | 1,499,997 | 43 | 1 x 3 | `01a11190-cd8f-7034-8557-b9c3eee9a4b1` |  |
| [`sepsis_survival_minimal_clinical_records`](sepsis_survival_minimal_clinical_records/) | IID | 110,204 | 3 | 3 x 3 | `01a11191-e6bd-755d-ab95-f7f61733b3c8` | `dataset_duplicate_rows` |
| [`sf_permit_time`](sf_permit_time/) | temporal | 99,847 | 37 | 9 x 1 | `01a11190-95a2-75c7-a40c-ed4f679cf6d7` |  |
| [`south_africa_coronary_heart_disease`](south_africa_coronary_heart_disease/) | IID | 462 | 9 | 20 x 3 | `01a11191-eb28-7861-bd1e-cda4bb9e5d76` |  |
| [`splice`](splice/) | IID | 3,190 | 60 | 10 x 3 | `01a11191-f475-7106-8cea-f03ce0050611` | `dataset_duplicate_rows` |
| [`student_portuguese_performance`](student_portuguese_performance/) | IID | 649 | 30 | 20 x 3 | `01a11191-f43b-7725-a911-16f5c99ddbba` |  |
| [`superconductivity`](superconductivity/) | IID | 21,263 | 81 | 3 x 3 | `01a11191-5066-7ef7-98e7-d2acd6d6cd57` | `dataset_conflicting_duplicate_rows` |
| [`taiwanese_bankruptcy_prediction`](taiwanese_bankruptcy_prediction/) | IID | 6,819 | 92 | 3 x 3 | `01a11191-927b-78b3-adb9-d2ccd442bac0` |  |
| [`thyroid_discordant`](thyroid_discordant/) | IID | 3,711 | 26 | 10 x 3 | `01a11191-f4f3-74a8-b9f7-c72224504edf` |  |
| [`tour_travels_churn`](tour_travels_churn/) | IID | 954 | 6 | 10 x 3 | `01a11191-f52c-7f5a-b894-97cc1b4601a6` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows`, `meta_bibtex_latex_hazard` |
| [`video_transcoding_time_prediction`](video_transcoding_time_prediction/) | grouped | 68,784 | 19 | 3 x 3 | `01a11191-6402-776f-9b72-c4f0a99fda74` |  |
| [`website_phishing`](website_phishing/) | IID | 1,353 | 9 | 10 x 3 | `01a11191-f562-7b40-89cc-dfd32c48ec62` | `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows` |
| [`wids_diabetes_mellitus`](wids_diabetes_mellitus/) | IID | 127,358 | 181 | 3 x 3 | `01a11190-c732-79a0-9535-32a4f762da86` |  |
| [`wine_quality`](wine_quality/) | IID | 5,320 | 12 | 3 x 3 | `01a11191-f6e8-77a9-ae34-4a2480023fc7` |  |
| [`wine_world_cost`](wine_world_cost/) | IID | 1,279 | 14 | 10 x 3 | `01a11191-f722-7eb4-be31-88370169ae88` |  |
<!-- datasets:end -->
