# Task probes of the v0.2 build

Generated on 2026-10-01 by `.claude/skills/verify-dataset/scripts/task_probes.py --all --built` on the built containers: dummy baselines against
three untuned model families (regularised linear, random forest, LightGBM) on each dataset's first 5 shipped splits
(train and test capped at 50,000 rows), scored per group for a group-unit task with `mean`, `any` or `last`. Skill
is 0 for the dummy and 1 for a perfect model (`2 AUC - 1`, `1 - log loss / dummy log loss`, `1 - MSE / dummy MSE`).
Text columns are left out (their count is shown), so a text-heavy task scores low here. The flags are questions for
the curator, not verdicts (`check-candidate/references/leak_checks.md`, the verify-dataset rubric item 13):

- `no_signal`: no model beats the dummy by more than the noise over the splits;
- `solved`: ROC AUC, macro ROC AUC or R^2 of at least 0.995;
- `no_spread`: the three families score the same within their noise;
- `one_feature`: one feature alone has at least 95% of the best skill;
- `drift_baseline`: for a temporal task, a constant from the newest data is as good as the models;
- `unstable`: the best skill varies by more than 0.1 (standard deviation) over the splits.

| dataset | unit | best model | best score | skill (std) | best single feature (skill) | flags |
|---|---|---|---|---|---|---|
| `5g_energy_consumption` | row | lightgbm | R^2 0.921 | +0.922 (0.006) | `RUType` (+0.59) |  |
| `acquire_valued_shoppers_challenge` | row | lightgbm | AUC 0.640 | +0.279 (0.076) | `has_bought_category` (+0.18) | no_spread |
| `airfoil_self_noise` | row | lightgbm | R^2 0.931 | +0.931 (0.008) | `frequency` (+0.19) |  |
| `allstate_claims_severity` | row | lightgbm | R^2 0.551 | +0.551 (0.002) | `cat80` (+0.24) |  |
| `amazon_employee_access` | row | random_forest | AUC 0.851 | +0.702 (0.014) | `ROLE_DEPTNAME` (+0.41) |  |
| `amex_non_iid_1m` | group (last) | lightgbm | AUC 0.954 | +0.907 (0.007) | `P_2` (+0.82) | no_spread |
| `anes_voting_2026` | row | lightgbm | AUC 0.872 | +0.744 (0.010) | `VCF0713` (+0.44) |  |
| `aps_failure` | row | lightgbm | AUC 0.991 | +0.982 (0.004) | `ck_000` (+0.94) | one_feature |
| `asp_potassco_classification` | row | random_forest | macro AUC 0.648 | +0.025 (0.062) | `Frac_Choice_Rules` (-0.67) | no_signal |
| `audiology_diagnosis` | row | linear | macro AUC 0.910 | +0.355 (0.191) | `air` (+0.10) | no_spread, unstable |
| `bad_customer_detection` | row | random_forest | AUC 0.740 | +0.479 (0.027) | `product_type` (+0.32) |  |
| `bank_customer_churn` | row | random_forest | AUC 0.853 | +0.706 (0.012) | `age` (+0.49) |  |
| `bank_marketing` | row | lightgbm | AUC 0.759 | +0.518 (0.014) | `pdays` (+0.23) |  |
| `biogeographical_ancestry_prediction` | row | random_forest | macro AUC 0.778 | +0.172 (0.008) | `rs6754311` (+0.11) |  |
| `biomechanical_orthopaedic_prediction` | row | linear | macro AUC 0.957 | +0.661 (0.040) | `degree_spondylolisthesis` (+0.31) |  |
| `bioresponse` | row | lightgbm | AUC 0.868 | +0.736 (0.017) | `D27` (+0.48) |  |
| `blood_tests_drink_prediction` | row | linear | R^2 0.129 | +0.136 (0.023) | `mcv` (+0.08) |  |
| `blood_transfusion` | row | linear | AUC 0.754 | +0.508 (0.030) | `MonthsSinceLastDonation` (+0.35) |  |
| `body_density_prediction` | row | linear | R^2 0.668 | +0.672 (0.029) | `Abdomen` (+0.59) |  |
| `california_house_prices_2020` (+19 text) | row | lightgbm | R^2 0.937 | +0.938 (0.004) | `Listed Price` (+0.92) | one_feature |
| `cardiotocography` | row | random_forest | macro AUC 0.969 | +0.625 (0.057) | `MSTV` (+0.20) |  |
| `churn` | row | lightgbm | AUC 0.922 | +0.843 (0.003) | `total_day_minutes` (+0.32) |  |
| `cirrhosis_patient_survival_prediction` | row | random_forest | R^2 0.301 | +0.356 (0.070) | `Edema` (+0.13) |  |
| `climate_model_weather_forecasting_1m` | row | lightgbm | R^2 0.846 | +0.847 (0.005) | `cmc_0_0_0_2_interpolated` (+0.74) |  |
| `clock_protein_toxicity` | row | lightgbm | AUC 0.512 | +0.025 (0.093) | `MDEC-23` (+0.28) | no_signal |
| `coffee_rating_prediction` (+6 text) | row | lightgbm | R^2 0.241 | +0.253 (0.103) | `price_per_gram_in_usd` (+0.16) | unstable |
| `coil_2000` | row | lightgbm | AUC 0.731 | +0.461 (0.027) | `contributionCarPolicies` (+0.33) | no_spread |
| `concrete_compressive_strength` | row | lightgbm | R^2 0.927 | +0.927 (0.006) | `Age` (+0.38) |  |
| `consumer_complaints_1m` (+3 text) | row | lightgbm | macro AUC 0.729 | +0.075 (0.034) | `Issue` (+0.10) |  |
| `cooking_time_1m` | row | lightgbm | R^2 0.489 | +0.490 (0.010) | `num_184` (+0.42) |  |
| `covertype` | row | random_forest | macro AUC 0.986 | +0.710 (0.001) | `Elevation` (+0.37) |  |
| `credit_approval` | row | random_forest | AUC 0.934 | +0.868 (0.011) | `A9` (+0.73) |  |
| `credit_card_clients_default` | row | lightgbm | AUC 0.778 | +0.557 (0.006) | `PAY_0` (+0.42) |  |
| `credit_g` | row | random_forest | AUC 0.774 | +0.548 (0.024) | `checking_status` (+0.41) |  |
| `delivery_eta_1m` | row | lightgbm | R^2 0.451 | +0.451 (0.019) | `num_10` (+0.38) |  |
| `dementia_prediction` | row | linear | macro AUC 0.859 | +0.330 (0.038) | `MMSE` (+0.28) |  |
| `diabetes_130_us` | row | lightgbm | AUC 0.651 | +0.302 (0.012) | `discharge_disposition_id` (+0.18) |  |
| `diamonds` | row | lightgbm | R^2 0.992 | +0.992 (0.000) | `carat` (+0.94) |  |
| `drug_induced_autoimmunity_prediction` (+1 text) | row | lightgbm | AUC 0.817 | +0.633 (0.035) | `SMR_VSA10` (+0.30) |  |
| `early_learning_predictors` | row | lightgbm | R^2 0.310 | +0.311 (0.011) | `child_age` (+0.13) |  |
| `early_stage_diabetes_risk_prediction` | row | random_forest | AUC 0.968 | +0.935 (0.028) | `Polyuria` (+0.67) |  |
| `ecoli_proteins` | row | linear | macro AUC 0.966 | +0.715 (0.028) | `alm1` (+0.29) |  |
| `electric_motor_temperature_prediction` | row | linear | R^2 0.970 | +0.975 (0.003) | `i_s_omega_ewma_4000` (+0.66) |  |
| `emscad` (+8 text) | row | lightgbm | AUC 0.866 | +0.732 (0.033) | `has_company_logo` (+0.47) |  |
| `eryhemato_squamous_disease` | row | linear | macro AUC 0.999 | +0.953 (0.007) | `thinning of the suprapapillary epidermis` (+0.32) | solved |
| `fiat_500` | row | random_forest | R^2 0.854 | +0.854 (0.003) | `age_in_days` (+0.79) |  |
| `fitness_club` | row | linear | AUC 0.814 | +0.628 (0.017) | `months_as_member` (+0.63) | one_feature |
| `food_delivery_time` | row | lightgbm | R^2 0.377 | +0.377 (0.003) | `Delivery_person_Ratings` (+0.19) |  |
| `forensic_glass_identification` | row | random_forest | macro AUC 0.934 | +0.505 (0.097) | `Mg` (+0.12) |  |
| `forest_fires` | row | linear | R^2 -0.043 | -0.030 (0.027) | `X` (-0.01) | no_signal |
| `gallstone_disease` | row | linear | AUC 0.859 | +0.719 (0.054) | `C-Reactive Protein (CRP)` (+0.54) | no_spread |
| `garments_worker_productivity` | row | random_forest | R^2 0.447 | +0.454 (0.162) | `targeted_productivity` (+0.24) | unstable |
| `give_me_some_credit` | row | lightgbm | AUC 0.859 | +0.717 (0.002) | `RevolvingUtilizationOfUnsecuredLines` (+0.55) |  |
| `healthcare_insurance_expenses` | row | random_forest | R^2 0.823 | +0.823 (0.045) | `smoker` (+0.44) |  |
| `heart_disease_cleveland` | row | random_forest | AUC 0.897 | +0.794 (0.077) | `thal` (+0.51) | no_spread |
| `heart_disease_hungary` | row | linear | AUC 0.899 | +0.798 (0.068) | `cp` (+0.61) |  |
| `heart_disease_va_long_beach` | row | random_forest | AUC 0.696 | +0.392 (0.089) | `cp` (+0.26) |  |
| `heart_failure_followup_survival` | row | random_forest | AUC 0.797 | +0.594 (0.064) | `ejection_fraction` (+0.40) |  |
| `heloc` | row | random_forest | AUC 0.792 | +0.584 (0.008) | `ExternalRiskEstimate` (+0.52) |  |
| `hepatitis_c_prediction` | row | random_forest | macro AUC 0.961 | +0.587 (0.031) | `AST` (+0.15) |  |
| `hepatitis_survival_prediction` | row | random_forest | AUC 0.878 | +0.757 (0.086) | `protime` (+0.47) |  |
| `hiva_agnostic` | row | random_forest | AUC 0.818 | +0.636 (0.060) | `molecule_structure_property_307` (+0.21) |  |
| `home_credit_default_risk` | row | lightgbm | AUC 0.768 | +0.536 (0.006) | `NEW_EXT_SOURCES_MEAN` (+0.42) |  |
| `home_credit_default_stability_1m` | row | lightgbm | AUC 0.839 | +0.678 (0.018) | `avgdpdtolclosure24_3658938P` (+0.20) |  |
| `homesite_quote_conversion` | row | lightgbm | AUC 0.962 | +0.925 (0.001) | `SalesField5` (+0.53) |  |
| `horse_colic_survival` | row | random_forest | macro AUC 0.790 | +0.200 (0.020) | `pain` (+0.08) |  |
| `hotel_booking_demand` | row | lightgbm | AUC 0.809 | +0.617 (0.009) | `Country` (+0.31) |  |
| `houses` | row | lightgbm | R^2 0.830 | +0.830 (0.005) | `MedianIncome` (+0.42) |  |
| `hr_analytics` | row | lightgbm | AUC 0.784 | +0.567 (0.011) | `city_development_index` (+0.44) |  |
| `ieee_fraud_detection` | row | lightgbm | AUC 0.861 | +0.723 (0.028) | `C4` (+0.39) |  |
| `immoscout_german_house_prices` (+4 text) | row | lightgbm | R^2 0.544 | +0.544 (0.006) | `Living_space` (+0.29) |  |
| `in_vehicle_coupon_recommendation` | row | lightgbm | AUC 0.763 | +0.525 (0.019) | `coupon` (+0.29) |  |
| `indian_liver_patient_dataset` | row | linear | AUC 0.749 | +0.498 (0.054) | `Sgot` (+0.33) | no_spread |
| `jm1` | row | random_forest | AUC 0.715 | +0.431 (0.021) | `loc` (+0.35) |  |
| `kdd_cup_09_appetency` | row | lightgbm | AUC 0.802 | +0.604 (0.015) | `Var126` (+0.50) |  |
| `kick` | row | lightgbm | AUC 0.711 | +0.422 (0.033) | `VehicleAge` (+0.28) |  |
| `kickstarter` (+4 text) | row | lightgbm | AUC 0.851 | +0.702 (0.026) | `main_category` (+0.44) |  |
| `labour_inspection_compliance` (+4 text) | row | lightgbm | AUC 0.664 | +0.328 (0.006) | `Payroll cost` (+0.22) |  |
| `lending_club` (+5 text) | row | lightgbm | AUC 0.681 | +0.363 (0.007) | `fico_n` (+0.20) |  |
| `ljubljana_breast_cancer` | row | linear | AUC 0.713 | +0.426 (0.067) | `deg-malig` (+0.32) |  |
| `ljubljana_primary_tumor` | row | random_forest | macro AUC 0.866 | +0.367 (0.032) | `sex` (+0.08) |  |
| `lung_cancer` | row | linear | macro AUC 0.993 | +0.799 (0.053) | `39266_at` (+0.23) |  |
| `lung_cancer_epithelial_genexp` | row | linear | AUC 0.773 | +0.545 (0.073) | `206628_at` (+0.42) |  |
| `maps_router_eta_1m` | row | lightgbm | R^2 0.809 | +0.811 (0.001) | `num_18` (+0.77) |  |
| `marketing_campaign` | row | lightgbm | AUC 0.899 | +0.797 (0.022) | `MntMeatProducts` (+0.30) | no_spread |
| `mercari_price_suggestion` (+4 text) | row | random_forest | R^2 0.060 | +0.060 (0.001) | `shipping` (+0.05) | no_spread |
| `mercedes_benz_greener_manufacturing` | row | linear | R^2 0.562 | +0.569 (0.074) | `X314` (+0.39) | no_spread |
| `miami_housing` | row | lightgbm | R^2 0.934 | +0.934 (0.002) | `TOT_LVG_AREA` (+0.51) |  |
| `mic` | row | random_forest | macro AUC 0.831 | +0.227 (0.016) | `K_SH_POST` (+0.09) |  |
| `micro_mass` | row | lightgbm | macro AUC 0.978 | +0.730 (0.055) | `peak_list_spectra_bin_684` (+0.04) |  |
| `musk` | group (any) | lightgbm | AUC 0.860 | +0.720 (0.106) | `feature_34` (+0.28) | no_spread, unstable |
| `mutual_funds_india` (+3 text) | row | random_forest | R^2 0.778 | +0.778 (0.011) | `category` (+0.68) |  |
| `naticusdroid_android_permissions_dataset` | row | lightgbm | AUC 0.984 | +0.968 (0.003) | `android.permission.READ_PHONE_STATE` (+0.59) | no_spread |
| `obesity_estimation` | row | random_forest | R^2 0.149 | +0.150 (0.047) | `Age` (+0.06) |  |
| `online_shoppers_purchasing_intention_dataset` | row | random_forest | AUC 0.872 | +0.745 (0.016) | `PageValues` (+0.61) |  |
| `otto_group_product_classification_challenge` | row | lightgbm | macro AUC 0.975 | +0.752 (0.001) | `feat_11` (+0.11) |  |
| `pancreatic_cancer_mouse_detection` | row | linear | AUC 0.625 | +0.249 (0.182) | `M/Z:1708.9949` (+0.06) | unstable |
| `parkinsons_biomedical_voice_measurements` | group (mean) | lightgbm | AUC 0.833 | +0.667 (0.253) | `spread1` (+0.83) | no_spread, one_feature, unstable |
| `physiochemical_protein` | row | random_forest | R^2 0.655 | +0.655 (0.002) | `FracExposedNonPolarResidue` (+0.15) |  |
| `polish_companies_bankruptcy` | row | lightgbm | AUC 0.950 | +0.899 (0.020) | `operating_profit_to_financial_expenses` (+0.62) |  |
| `porto_seguro` | row | linear | AUC 0.616 | +0.232 (0.019) | `ps_car_13` (+0.10) |  |
| `predict_students_dropout_and_academic_success` | row | random_forest | macro AUC 0.887 | +0.428 (0.015) | `Curricular_units_2nd_sem_approved` (+0.30) |  |
| `pva_revenue_prediction_kddcup98` (+27 text) | row | linear | AUC 0.598 | +0.195 (0.011) | `LASTGIFT` (+0.16) |  |
| `qsar_aquatic_toxicity` | row | random_forest | R^2 0.542 | +0.545 (0.026) | `MLOGP` (+0.24) |  |
| `qsar_biodeg` | row | random_forest | AUC 0.934 | +0.868 (0.018) | `Weighted_LeadingEigenvalue_Burden_Matrix` (+0.60) |  |
| `qsar_fish_toxicity` | row | random_forest | R^2 0.640 | +0.643 (0.024) | `MLOGP` (+0.43) |  |
| `qsar_tid_11` | row | lightgbm | R^2 0.743 | +0.743 (0.009) | `FCFP6_1024_867` (+0.12) |  |
| `regensburg_pediatric_appendicitis` (+3 text) | row | random_forest | AUC 0.911 | +0.822 (0.036) | `CRP` (+0.60) |  |
| `rossmann_store_sales` | row | random_forest | R^2 0.741 | +0.746 (0.021) | `Promo` (+0.15) |  |
| `santander_customer_satisfaction` | row | lightgbm | AUC 0.828 | +0.656 (0.009) | `saldo_var30` (+0.41) |  |
| `santander_customer_transaction_prediction` | row | lightgbm | AUC 0.874 | +0.748 (0.005) | `var_81` (+0.13) |  |
| `santander_transaction_value` | row | random_forest | R^2 0.417 | +0.417 (0.008) | `median_48df886f9_4991` (+0.30) |  |
| `sat11_hand_algo_runtime` | row (select_min) | random_forest | R^2 0.693 | +0.702 (0.042) | `gsat_BestSolution_Mean` (+0.31) |  |
| `sberbank_housing_market_forecasting` | row | lightgbm | R^2 0.560 | +0.576 (0.049) | `cafe_count_3000` (+0.44) |  |
| `sdss_17` | row | lightgbm | macro AUC 0.957 | +0.627 (0.002) | `z` (+0.14) |  |
| `sepsis_prediction_1m` | row | random_forest | AUC 0.761 | +0.522 (0.007) | `ICULOS` (+0.33) |  |
| `sepsis_survival_minimal_clinical_records` | row | linear | AUC 0.706 | +0.412 (0.003) | `age_years` (+0.40) | one_feature |
| `sf_permit_time` (+14 text) | row | random_forest | R^2 0.255 | +0.267 (0.034) | `Permit Type Definition` (+0.23) |  |
| `south_africa_coronary_heart_disease` | row | linear | AUC 0.773 | +0.546 (0.027) | `age` (+0.36) |  |
| `splice` | row | lightgbm | macro AUC 0.993 | +0.816 (0.031) | `position_-1` (+0.26) |  |
| `student_portuguese_performance` | row | random_forest | R^2 0.287 | +0.293 (0.026) | `failures` (+0.18) |  |
| `superconductivity` | row | random_forest | R^2 0.922 | +0.922 (0.001) | `range_atomic_radius` (+0.60) |  |
| `taiwanese_bankruptcy_prediction` | row | lightgbm | AUC 0.946 | +0.892 (0.016) | `Persistent_EPS_Last_4_Seasons` (+0.74) |  |
| `telemonitoring_parkinsons_biomedical_voice_measurements` | row | random_forest | R^2 -0.181 | -0.021 (0.051) | `sex` (-0.03) | no_signal (retired 2026-10-02) |
| `thyroid_discordant` | row | random_forest | AUC 0.981 | +0.962 (0.014) | `FTI` (+0.79) |  |
| `tour_travels_churn` | row | lightgbm | AUC 0.962 | +0.924 (0.011) | `AnnualIncomeClass` (+0.51) |  |
| `video_transcoding_time_prediction` | row | lightgbm | R^2 0.963 | +0.963 (0.009) | `o_width` (+0.40) |  |
| `website_phishing` | row | random_forest | macro AUC 0.976 | +0.684 (0.012) | `SFH` (+0.34) |  |
| `wids_diabetes_mellitus` (+2 text) | row | lightgbm | AUC 0.859 | +0.718 (0.002) | `d1_glucose_max` (+0.56) |  |
| `wine_quality` | row | random_forest | R^2 0.389 | +0.389 (0.013) | `alcohol` (+0.21) |  |
| `wine_world_cost` (+8 text) | row | random_forest | R^2 0.523 | +0.526 (0.034) | `Style` (+0.29) |  |
