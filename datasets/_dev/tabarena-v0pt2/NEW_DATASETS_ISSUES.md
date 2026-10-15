# New candidates added to the working copy: issues (2026-10-07)

Lennart asked for `/add-dataset`, with all of its checks, on every curation record that matches the dashboard
filter `suggestion = Yes`, `data_foundry_status` without `DF: Yes`, `checked_by` without `AI (UNVERIFIED)`. That is
65 records, handled as 59 units (one unit per source; TCGA, MLOmics, Numerai and Alfa-Battle units hold several
records). For each unit:

1. One agent judged the record, downloaded the data, wrote the v2 definition and ran `dataset check`, the pandas 3
   checksum comparison and the probes (leak, task, generated data, hidden groups; group probes for grouped tasks).
2. A second agent verified the work against the `/verify-dataset` rubric.
3. The first agent then applied each finding, or rejected it with evidence.

The three datasets of the earlier request (`datasets/_maintenance/_out_of_scope/_too_late_to_add`) went through the
same steps and are at the end of this file.

**What changed in the repository:**

- 59 new folders under `datasets/_dev/tabarena-v0pt2/`: 56 from the 65 records and the 3 late ones.
- The records of all 68 now carry a dated `**Assessment (AI, 2026-10-07):**` comment.
- Every record with a folder has its `v2_path` and `WIP (DF)`. `DF: Suspended` was replaced on seven records: ASHRAE,
  whose v1 notebook gives the reason (open judgment calls, "takes too much time for now"), which the new definition
  settles; and the six TCGA records (brca, glioblastoma, sarcoma, coad, lgg, ov), whose suspension has no recorded
  reason. `DF: Much work` was replaced on apistox.
- `problem_type` and `required_split` were filled only where they read `TBD` or `?`. No suggestion, marker or other
  field was changed.
- Nothing was built: there is no container and no UUID, and the README table shows the new folders as "not built".

The per-dataset sections are the units' own reports with the verification rounds. Notes there addressed to the
orchestrator (`v2_path`, record comments) are done as described above; record fields are listed below.

The evidence (each unit's report, the verifier's `verify.md`, scripts and small outputs) is outside git, in the local
warehouse of the machine that ran this: `local-data-warehouse/_runs/2026-10-07_backlog/` (moved there from
`../_scratch_new65/` on 2026-10-12). `<scratch>` in a section means that unit's folder `_run_reports/new65/<unit>/`
there; a path `_scratch_new65/<name>/` below is now `evidence/<name>/` there (archived pages, other scrapes, unpacked
mirrors), and the follow-ups of 2026-10-12 are in `_crosscut_2026-10-12/`.

**Counts:**

- **Added:** 59 definitions. Some carry a recommendation not to ship, Lennart's call:
  - `central_international_medical_college_and_hospital_health_risk_prediction`;
  - `credit_card_customers`;
  - `g_research_crypto_forecasting_1m`;
  - `stroke_prediction`;
  - `alvin_smart_money_management_classification_challenge`;
  - `digicow_farmer_training_adoption_challenge`;
  - `lgg_low_grade_glioma`;
  - `phiusil_phishing`.
- **Not added:** 9 records.
  - Duplicates: `churn_telco_south_asia_duplicate`, `myocardial_infarction_complications`, `numerai28_6`,
    `sasol_customer_retention_recruitment_competition`.
  - Data gone: `alfa_battle_2_0_task_1`.
  - Generated or injected data: `hepatitis_c_egypt`, `high_storage_system_data_for_energy_optimization`.
  - A different recording of the classes plus personal data: `churn_telco_europa`.
  - A recommender task: `farm_to_feed_shopping_basket_recommendation_challenge`.

## Summary per record

| Record | Outcome | Main points for Lennart |
|---|---|---|
| [`2_month_survival_rate_prediction`](#2_month_survival_rate_prediction) | added | Both phases since 2026-10-12: SUPPORT2's phase II physiology sits in other patients' rows; moved back with ICPSR 2957, only support2's values shipped. |
| [`account_debt_south_africa`](#account_debt_south_africa) | added | Seven runs of the file (20% of rows) hold no recorded debt and are dropped by a rule on the file order: keep, drop or retire? The three label-rule columns and the payment totals of the label window are dropped. |
| [`aeolus`](#aeolus) | added as `aeolus_1m` | The target is the 15-minute delay flag, not the record's regression. All three test weeks fall in the Christmas peak. The weather is 4-10 hours older than the scheduled times (text corrected; no leak). |
| [`alfa_battle_2_0_task_1`](#alfa_battle_2_0_task_1) | not added | The task-1 files are gone from every source. `No` unless Alfa-Bank shares them. |
| [`alfa_battle_2_0_task_2`](#alfa_battle_2_0_task_2) | added | The products of a test window's clients are dropped from each training side. The features are the organizers' 127 baseline aggregates. Window length is open. |
| [`alvin_smart_money_management_classification_challenge`](#alvin_smart_money_management_classification_challenge) | added; `No` (`Too Small`) on 2026-10-12, folder removed | 350 rows, 27-41 test purchases per window. Payees who are private persons are masked (142 rows); `Ethical Issue` is the alternative to masking. |
| [`analcatdata_supreme`](#analcatdata_supreme) | added; `No` (Scientific Discovery) on 2026-10-14, folder removed | IID: a temporal split is invalid because the label window ends in 1988. Keep or retire; target scale. |
| [`apistox`](#apistox) | added | The molecule is only a SMILES string. Under the default pipeline (Qwen3 text embedding, 32 dimensions) a model learns from the agrochemical type and the year, not from the structure (ECFP4 or MACCS would add 0.03-0.05 AUC). Four 10-year windows on a noisy first-publication year; 8 windows are the alternative. |
| [`ashrae_great_energy_predictor_iii`](#ashrae_great_energy_predictor_iii) | added as `ashrae_great_energy_predictor_iii_1m` | The test year comes from a second source (BDG2 2017). Forecasting scope; temporal or grouped by building. |
| [`bias_correction_r_bias_correction_r_2`](#bias_correction_r_bias_correction_r_2) | added | One target (`Next_Tmin`) under the record's Multi-target tag. Per-station MOS is the baseline to beat: the mean of three models beats it on 7 of 9 windows. |
| [`brazilian_ecommerce`](#brazilian_ecommerce) | added | Delivery time at checkout, with a one-month label gap. Open: which task, where the review sample ends, labels that arrive late. |
| [`brca_breast_cancer`](#brca_breast_cancer) | added; `No` on 2026-10-12, folder removed | The PAM50 label is computed from the shipped expression values, so the expression block is dropped (methylation and miRNA remain). Alternative: retire as `Trivial`. |
| [`breast_cancer_prediction`](#breast_cancer_prediction) | added | The full BCSC file, grouped by woman (the record says IID). Does the image-scoring rule (breast_w) cover the BI-RADS readings? |
| [`caracas_cervical_cancer`](#caracas_cervical_cancer) | added | 108 patients who skipped the contraceptive question are dropped. Target: Biopsy. |
| [`cdc_diabetes_health_indicators`](#cdc_diabetes_health_indicators) | added; `No` (Scientific Discovery) on 2026-10-15, folder removed | Three classes; binary "ever told diabetes" is the alternative. The dropped blanks are partly a skip pattern. |
| [`central_international_medical_college_and_hospital_health_risk_prediction`](#central_international_medical_college_and_hospital_health_risk_prediction) | added; `No` (`Trivial`) on 2026-10-12, folder removed | The label is the NEWS2 band of the eight features, and the vital signs look generated. |
| [`churn_telco_europa`](#churn_telco_europa) | not added; `No` (`Data Quality Issue`, `Ethical Issue`) on 2026-10-12 | Active lines and churners were recorded differently (an irreversible leak, as in iranian_churn). The files hold Chilean national ids and phone numbers. |
| [`churn_telco_south_asia_duplicate`](#churn_telco_south_asia_duplicate) | not added; duplicate | The DSN files are the 2,000 rows of churn_telco_south_asia with renamed values. |
| [`churn_telco_south_asia`](#churn_telco_south_asia) | added | When churn was observed is open; the IntelliSys 2017 paper would settle it. The 50% base rate is artificial. |
| [`coad_colon_adenocarcinoma`](#coad_colon_adenocarcinoma) | added | Multiclass CIN/MSI/GS (the record says binary). 49,283 features, 2.2 times the widest dataset in the copy; mRNA only is the alternative. The label is not a rule on a shipped block. |
| [`college_scorecard`](#college_scorecard) | added | Are the institution's published outcomes (latest completion rate, retention) features? SAT columns are dropped at the 2017 scale change. The source should be the Scorecard, not OpenML 46674. |
| [`corporate_credit_rating`](#corporate_credit_rating) | added | Grouped by company (the shadow-rating use) instead of the record's temporal tag: on the temporal split, carrying a company's last rating forward beats the models. Which classes to predict is open. |
| [`corporate_credit_rating_cat_data_set_ratings_raitings`](#corporate_credit_rating_cat_data_set_ratings_raitings) | added | The book's 197 rows as a regression on the rating notch. OpenML 46372 (5,000 rows) is generated from them. |
| [`credit_card_customers`](#credit_card_customers) | added; recommended `No` (`AHDS`, `Missing source information`) | The data looks constructed: the 12-month transaction count equals Q1 + Q4 in every row, and months inactive are unrelated to activity. |
| [`dataorg_financial_health_prediction_challenge`](#dataorg_financial_health_prediction_challenge) | added | Lesotho (1,944 rows) is dropped: its label runs against the index (models trained on the other countries score it at AUC 0.46). The label is a rule on the 11 product columns plus a residual; dropping those columns is the alternative. |
| [`diabetes_3`](#diabetes_3) | added | The cohort may not be diabetic (glucose at most 124). The `Trivial` marker is not supported. |
| [`differentiated_thyroid_cancer_recurrence`](#differentiated_thyroid_cancer_recurrence) | added | `Response` (to therapy) and `Hx Radiotherapy` are dropped as after the prediction point. The label definition is unverified (the paper is paywalled). |
| [`digicow_farmer_training_adoption_challenge`](#digicow_farmer_training_adoption_challenge) | added; recommended `No` (`Too Small`, `Data Quality Issue`) | Adoption was recorded in waves, so a 0 often means "not recorded": 0% of 120-day adopters adopted within 7 days for Aug-Oct 2024 trainings, 95% for Feb 2025. The newest windows hold 5-19 adopters from one or two trainers. The stored dates have day and month swapped (fixed). |
| [`distribution_transformers_at_cauca_department`](#distribution_transformers_at_cauca_department) | added | `self_protected` is dropped (it marks replacement units). `power_kva` and `installation_type` may describe replacements too: kept, with dropping them as the alternative. |
| [`expresso_churn_prediction`](#expresso_churn_prediction) | added as `expresso_churn_prediction_1m` | REGION is dropped as most likely filled after the window. Two other records duplicate this data (`indabax_eswatini_2022`, sasol). |
| [`farm_to_feed_shopping_basket_recommendation_challenge`](#farm_to_feed_shopping_basket_recommendation_challenge) | not added; recommended `No` (`Out-of-scope Task (CTR/RecSys/Ranking)`) | The competition asks for a recommender system, and the data is the full customer x product grid of every week. |
| [`force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`](#force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition) | added | Grouped by well. Open: GROUP and FORMATION as features, depth context. Untuned LightGBM diverges on this data. |
| [`framingham_heart_study_fhs`](#framingham_heart_study_fhs) | added | The label is rebuilt: the MIT/Kaggle `TenYearCHD` counts 265 non-CHD events among its 644 positives. Competing deaths count as No. |
| [`fraud_detection_in_electricity_and_gas_consumption`](#fraud_detection_in_electricity_and_gas_consumption) | added as `fraud_detection_in_electricity_and_gas_consumption_1m` | History cut at 2013 (inspection footprints) instead of the challenge's full history. The per-client rule (`mean`, `any`, `last`) is open. |
| [`g_research_crypto_forecasting`](#g_research_crypto_forecasting) | added as `g_research_crypto_forecasting_1m`; recommended `No` (`Time-series (Forecasting)`) | The competition is forecasting, and the RMSE signal is near zero. |
| [`glioblastoma`](#glioblastoma) | added; `No` on 2026-10-12, folder removed | The label is an ssGSEA score of the shipped expression values, so the expression block is dropped. |
| [`glioma_grading_clinical_and_mutation_features`](#glioma_grading_clinical_and_mutation_features) | added | The TCGA-era histological grade; IDH1 and age carry most of the signal. Shares patients with the omics candidates. |
| [`hepatitis_c_egypt`](#hepatitis_c_egypt) | not added; recommended `No` (`AHDS`) | No column depends on another, the label included: generated or replaced data. |
| [`high_storage_system_data_for_energy_optimization`](#high_storage_system_data_for_energy_optimization) | not added; recommended `No` (`AHDS`) | The anomalies were injected by software into normal recordings. |
| [`house_prices_nominal`](#house_prices_nominal) | added | De Cock's full Ames file instead of the Kaggle half. Three partial-sale outliers are dropped. |
| [`house_sales`](#house_sales) | added | Each house's record is rebuilt as of its sale from the county's change log: a new 1.8 GB raw input that the county updates weekly. View and waterfront stay as in the file. |
| [`huntprohibited`](#huntprohibited) | added as `huntprohibited_1m` | IID, because the file has no time index (the record asks for temporal). Text carries most of the signal. |
| [`lgd`](#lgd) | added | A grouped regression on LGD (the record says binary and IID), with two features only. Whether `event` = 0 is a cure is unsettled. |
| [`lgg_low_grade_glioma`](#lgg_low_grade_glioma) | added; recommended `No` (`Data Quality Issue`) | The MLOmics files are defective: the methylation profiles belong to other patients, and the gene names do not describe their values. The label is close to a two-column rule: one CNV column gives codeletion at AUC 0.995. |
| [`melbourne_housing_market`](#melbourne_housing_market) | added | Only sale prices are kept (passed-in and vendor bids dropped). The scraped attributes are kept, checked against the auction sheets. `melbourne_housing_snapshot` is a duplicate. |
| [`mobile_churn`](#mobile_churn) | added | Never-activated SIM cards are dropped in every month (12,262 rows). The source and the churn definition are unknown. |
| [`mortgage`](#mortgage) | added | Three classes (active, default, payoff) in one-quarter windows. The book's balance and LTV record the event itself, and its macro columns are the quarter's own values (published after it): both lagged to what is known at the quarter's start. The windows mostly score the quarter's overall event rate; default-only AUC or four-quarter windows are the alternatives. |
| [`myocardial_infarction_complications`](#myocardial_infarction_complications) | not added; duplicate | The same file as `mic`, which also drops patient 1 through a header bug. |
| [`nba_players_2016_2019`](#nba_players_2016_2019) | added | The target is recomputed and matches the NBA's official scores in all 958 matched rows. The season statistics run past the vote, so the prediction point is the season's end. |
| [`numerai28_6`](#numerai28_6) | not added; duplicate | An older release of the data in `numerai_v5_2`, without eras. |
| [`numerai_v5_2`](#numerai_v5_2) | added as `numerai_v5_2_1m` | RMSE mostly ranks how far a model shrinks towards 0.5. The Faith features are kept as a potential leak. Numerai's terms are noted. |
| [`nyc_taxi_trip_duration`](#nyc_taxi_trip_duration) | added | The Kaggle sample or the TLC records; row filters that select on the target; the hour of day depends on the TabArena pipeline. |
| [`onlinenewspopularity`](#onlinenewspopularity) | added | A regression of log shares instead of the paper's binary task. The LDA columns are dropped; the keyword statistics are kept as a potential leak. |
| [`open_university_learning_analytics_dataset`](#open_university_learning_analytics_dataset) | added | Grouped by module presentation, not temporal; predictions on day 60. |
| [`ov_ovarian_cancer`](#ov_ovarian_cancer) | added; `No` on 2026-10-12, folder removed | The gene names do not describe their values, so the features are anonymised; accepting the repair is Lennart's call. The subtypes are clusters of the same tumours' microarray expression. 48,279 features. |
| [`perth_house_prices`](#perth_house_prices) | added | The upload holds no sale above $2.44M (a capped target). In 2019-2020 the house records are often older than the sale. |
| [`pkdd_15_taxi_trip_time_prediction_ii`](#pkdd_15_taxi_trip_time_prediction_ii) | added as `pkdd_15_taxi_trip_time_prediction_ii_1m` | The destination is a feature (an ETA once the destination is known), although the source's task has no destination. |
| [`qsar_bioconcentration`](#qsar_bioconcentration) | added | The three-class task. Three swapped chemical pairs are repaired from the authors' 2015 table. In TabSTAR's pretraining with two classes swapped. |
| [`qsar_oral_toxicity`](#qsar_oral_toxicity) | added | Parent-structure copies are dropped, unlike the source. The split is random, while the scores depend on close analogues. |
| [`rain_in_australia`](#rain_in_australia) | added | Predicted at 9 am; next-row labels dropped; 14-day windows every 6 weeks; the original rattle file. |
| [`rosbank1`](#rosbank1) | added | Periods from 2018 are cut, because their 3-month labels were incomplete at the extract. Cut B (keep January 2018) is the alternative. |
| [`sarcoma`](#sarcoma) | added | Labels from TCGA's expert review (pinned GDC file). DDLPS is defined by MDM2 (a one-feature class). Merge UPS and MFS? |
| [`sasol_customer_retention_recruitment_competition`](#sasol_customer_retention_recruitment_competition) | not added; duplicate | A renamed 70% sample of the Expresso data (regions renamed, money divided by 2.34). |
| [`stroke_prediction`](#stroke_prediction) | added; recommended `No` (`AHDS` or `Data Quality Issue`) | The file is partly generated or altered. bmi is dropped, because a missing BMI follows the stroke. |
| [`zillow_prize`](#zillow_prize) | added | RMSE instead of the competition's MAE (the adapter takes only RMSE). The signal is small. |
| [`african_credit_scoring_challenge`](#african_credit_scoring_challenge) (late) | added | The window scheme. Three leaks removed: the repay amounts, the zero-share lender rows and the unsettled labels. The record still says Grouped. |
| [`infrared_thermography_temperature`](#infrared_thermography_temperature) (late) | added | IID over subjects, with temporal or day-grouped splits as alternatives. The 17 retake rows are kept. The modality marker is open. |
| [`phiusil_phishing`](#phiusil_phishing) (late) | added; recommended exclusion (`Data Quality Issue`) | Solved by how the two classes were collected (URL template, page fetch timing). No version of the file is a valid task. |

## Record fields that disagree with the definition

These fields were left as they are; each disagreement is either a decision the definition took on evidence (see the
dataset's section) or a value to correct in the record. Record `original_source` values `Website` and `Company` count as
the schema's `Other`. Tags are listed when a `Non-IID` tag names another regime.

- `aeolus`: problem_type `Regression`, definition `Binary Classification`.
- `alfa_battle_2_0_task_2`: domain `business & marketing`, definition `finance`; tag `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.
- `alvin_smart_money_management_classification_challenge`: domain `business & marketing`, definition `finance`.
- `analcatdata_supreme`: required_split `Temporal (NON-IID)`, definition `Random (IID)`; tag `Non-IID (Temporal)`, definition `Random (IID)`.
- `apistox`: original_source `UCI`, definition source `Other`.
- `ashrae_great_energy_predictor_iii`: tag `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.
- `brazilian_ecommerce`: year `2019`, definition `2018`.
- `brca_breast_cancer`: problem_type `Binary Classification`, definition `Multiclass Classification`.
- `breast_cancer_prediction`: required_split `Random (IID)`, definition `Grouped (NON-IID)`; original_source `Kaggle`, definition source `GOV Website`; year `2020`, definition `2014`.
- `coad_colon_adenocarcinoma`: problem_type `Binary Classification`, definition `Multiclass Classification`; original_source `Github`, definition source `HuggingFace`.
- `college_scorecard`: tag `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.
- `corporate_credit_rating`: tag `Non-IID (Temporal)`, definition `Grouped (NON-IID)`.
- `corporate_credit_rating_cat_data_set_ratings_raitings`: problem_type `Multiclass Classification`, definition `Regression`.
- `dataorg_financial_health_prediction_challenge`: domain `business & marketing`, definition `finance`.
- `distribution_transformers_at_cauca_department`: tag `Non-IID (Temporal)`, definition `Random (IID)`.
- `framingham_heart_study_fhs`: original_source `Kaggle`, definition source `GOV Website`; year `2013`, definition `2004`.
- `fraud_detection_in_electricity_and_gas_consumption`: year `2020`, definition `2019`; tag `Non-IID (Temporal)`, definition `Grouped (NON-IID)`.
- `glioblastoma`: problem_type `Binary Classification`, definition `Multiclass Classification`.
- `house_sales`: original_source `Kaggle`, definition source `Other`; year `2016`, definition `2015`.
- `huntprohibited`: required_split `Temporal (NON-IID)`, definition `Random (IID)`; tag `Non-IID (Temporal)`, definition `Random (IID)`.
- `lgd`: problem_type `Binary Classification`, definition `Regression`; required_split `Random (IID)`, definition `Grouped (NON-IID)`.
- `lgg_low_grade_glioma`: problem_type `Binary Classification`, definition `Multiclass Classification`; original_source `Github`, definition source `HuggingFace`.
- `mortgage`: tag `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.
- `nba_players_2016_2019`: domain `Other`, definition `social science`.
- `nyc_taxi_trip_duration`: domain `Other`, definition `industry & manufacturing`; original_source `GOV Website`, definition source `Kaggle`.
- `open_university_learning_analytics_dataset`: tag `Non-IID (Temporal)`, definition `Grouped (NON-IID)`.
- `ov_ovarian_cancer`: problem_type `Binary Classification`, definition `Multiclass Classification`; original_source `Github`, definition source `HuggingFace`.
- `pkdd_15_taxi_trip_time_prediction_ii`: domain `Other`, definition `industry & manufacturing`.
- `rain_in_australia`: original_source `Kaggle`, definition source `Other`; year `2017`, definition `2026`.
- `sarcoma`: problem_type `Binary Classification`, definition `Multiclass Classification`.
- `stroke_prediction`: original_source `Kaggle`, definition source `Other`; year `2021`, definition `2018`.
- `phiusil_phishing`: original_source `UCI`, definition source `Other`; year `2024`, definition `2023`.
- `african_credit_scoring_challenge`: tag `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.

## Across datasets

### Datasets already in the working copy

- **`mic` drops patient 1.** `mic/dataset.py` line 48 reads `MI.data` without `header=None`, so the first patient
  becomes the header: 1,699 rows instead of 1,700. The fix gives a new container (new UUID). Found by the
  myocardial_infarction_complications unit and confirmed. Which outcome `mic` should predict is also open (that
  unit, issue 2).

  **Resolved (2026-10-12):** fixed (`header=None`); mic has 1,700 rows on its next build. Which outcome mic should predict stays open in its record.
- **`sf_permit_time` may need a label gap.** It trains on permits issued after its windows start, the problem
  brazilian_ecommerce fixed with a one-month gap (brazilian_ecommerce unit). Not checked.

  **Resolved (Lennart, 2026-10-12):** needed: training rows are now permits issued before each window starts, with a 6-month gap, over 8 windows (a 1-month gap would bias the labels by censoring). The task probes flag `no_spread`, kept. Rebuild pending.

- **`splits_comment` is stored with its code indentation.** `src/data_foundry/v2/dataset.py:677` sets
  `plan.comment = self.splits_comment` without `clean_text`, so every multi-line `splits_comment` (lending_club,
  kickstarter, emscad, coffee_rating_prediction, and several new folders) keeps its indentation in the README and the
  container. The fix changes those checksums, so it needs a rebuild of the affected datasets.

  **Resolved (2026-10-12):** `plan.comment = clean_text(self.splits_comment)`. The 26 unbuilt definitions it touches are re-checked; 19 built ones change their checksum on the next build (CHANGELOG, 2026-10-12).

### Records outside the 65

- `colleges` (OpenML 42727): a one-year College Scorecard snapshot. It duplicates `college_scorecard` if that ships.

  **Resolved (2026-10-12):** confirmed. OpenML names its original as beachpartyserver.azurewebsites.net/VueBigData/DataFiles/Colleges.txt (still online), which is the College Scorecard file of 2013-14: all 7,804 UNITIDs are in it, and faculty salary, size and admission rate agree for 97-99% of the colleges. Record set to `No` + `Duplicate`.
- `indabax_drc_2022`: the same STEG data as `fraud_detection_in_electricity_and_gas_consumption`, so a `Duplicate`.

  **Resolved (2026-10-12):** record set to `No` + `Duplicate` (name kept, so links stay valid).
- `indabax_eswatini_2022`: the same Expresso data as `expresso_churn_prediction`, so a `Duplicate`. The
  `sasol_customer_retention_recruitment_competition` record duplicates the same data, so the
  `<name>_duplicate` naming needs a second name.

  **Resolved (2026-10-12):** record set to `No` + `Duplicate`; the names stay as they are (no `_duplicate` rename), so the second name is not needed.
- `melbourne_housing_snapshot`: all 13,580 rows, and its earlier 18,396-row cut, are in the FULL file that
  `melbourne_housing_market` uses, so a `Duplicate`.

  **Resolved (2026-10-12):** record set to `No` + `Duplicate`.
- `nyc_taxi_trip_duration` lists the PKDD-15 (Porto) competition among its `source_links`;
  `melbourne_housing_market` lists two Airbnb links. Both belong to other datasets.

  **Resolved (2026-10-12):** both are related work, not sources: moved from `source_links` into a comment of each record.
- `infrared_thermography_temperature` and `african_credit_scoring_challenge` have no `notebook_path`: their v1
  notebooks are named `infrared_thermography_features` and `african_credit_scoring`, so `sync-notebooks` cannot match
  them. Renaming the notebooks would make each file name differ from the unique name inside it, so I left them.

  **Resolved (2026-10-12):** the two dev notebooks and their folders are renamed to the records' names; `sync-notebooks` set both `notebook_path`s. The records are unchanged otherwise.

### Framework (`src/data_foundry/v2/`)

- **`dataset new` leaves `domain` and `source` as `"TODO"`, which do not import.** One fresh scaffold then breaks
  `pytest` collection, `dataset list` and probe discovery for the whole working copy; most units of this run hit it and
  ran their probes on a private root. Proposal: fill both from the record when the record's value maps to a schema
  value (record `domain` maps one to one; `original_source` mostly does, e.g. Github to GitHub, Website to Other).

  **Resolved (2026-10-12):** `dataset new` fills both when the record's value names one schema value (`Github` becomes `GitHub`, `Website` becomes `Other`, `handcrafted/toy` becomes `handcrafted`); other values stay TODO. Test added.
- **A task cannot be grouped and temporal at once** (`dataset.py:1114`). Panels that repeat an entity over time
  (taxis, eras, loans, companies, clients) have to pick one.

  **Resolved (Lennart, 2026-10-12):** no change: in practice a task is grouped or temporal. Revisit when a dataset needs both.
- **`_prepare_code_hash` follows only functions**, so editing a module constant used by `_prepare_raw_files`
  (zillow_prize: `TEXT_COLUMNS`, `SALES_FILES`) does not re-run the preparation.

  **Resolved (2026-10-12):** the hash also covers the module-level assignments the preparation code reads, as written (and the constants they are built from); code without constants keeps its hash. Test added.
- **The README's feature-type summary** calls `_feature_types` on the already-cast frame, so a dtype-based list
  shows "0 categorical" there (house_prices_nominal).

  **Resolved (2026-10-12):** the README lists the types the standard steps applied (remembered in `_standardize`). Test added.

### Probes

- **`generated_probes.py` misses two generators**: columns drawn independently, label included (hepatitis_c_egypt,
  UCI 503), and values drawn uniformly within each class (OpenML 46372). For the first, a low share of correlated
  column pairs plus a uniform share of at least 0.5 over 5 or more columns flags UCI 503 and nothing else in the
  working copy.

  **Resolved (2026-10-12):** two new flags, `independent_columns` and `uniform_within_class` (pairs dependent at the 5% level at most 10%, uniform share at least 0.5 over at least 5 columns, classes of at least 50 rows). Each fires on its synthetic case (UCI 503; OpenML 46372) and on none of the 184 definitions (sweep of 13 minutes).

- **`leak_probes.py`** got two changes in this run, both uncommitted: `--n-jobs` (it hard-coded 8 threads per
  model, which stalled a shared machine) and dropping the grouping columns from the features (it kept `patient_id`,
  which hid exact copies across a grouped split: BCSC 0.0% before, 49.4% after). Still open:
  - it needs about 5 hours at 26k-50k columns (the omics units used a pre-screen wrapper);
  - it has no `--out` option, unlike the other probes;
  - it returns NaN macro AUC when a test fold lacks a class (FORCE 2020, alvin; `group_probes.py` too);
  - it skips string columns, so copies at the SMILES or text level go unchecked (apistox, qsar_bioconcentration).

  **Resolved (2026-10-12):** `--max-single-features` (default 300) screens wide data (coad: about 5 hours to 10 minutes, the same best features); `--out DIR`; macro ROC AUC over the classes present in the test fold (also in `group_probes.py`; FORCE 2020 and alvin no longer give NaN); string columns join the exact-copy check, with a per-column share of test values seen in train.

- **`hidden_groups.py`** finds nothing on all-binary data (qsar_oral_toxicity) and skips temporal tasks.

  **Resolved (Lennart, 2026-10-12):** a new candidate, clusters of near-identical rows (token Jaccard at least 0.85, at least 10 shared tokens), tested like a column; it finds qsar_oral_toxicity's compound families (11% of rows, no gap) and hits no IID dataset of the working copy, only the grouped control early_learning_predictors. Temporal tasks now report how often entities recur across the cutoff, without a flag.

- **`task_probes.py`'s `few_minority`** checks binary tasks only; alvin's windows hold 2-5 rows of some classes and
  raised no flag.

  **Resolved (Lennart, 2026-10-12):** the flag now applies the threshold to each class of a multiclass task and names the short classes; it flags alvin and eight other multiclass datasets (CHANGELOG), open for the curator.

- **`ruff check --fix` (rule C416)** rewrote a dict comprehension into `dict(...)` and broke the
  qsar_bioconcentration pair repair; `dataset check` caught it. Run `dataset check` after every `ruff --fix`.

  **Resolved (2026-10-12):** C416 is in ruff's ignore list (pyproject.toml, with the reason), and qsar_bioconcentration uses the dict comprehension again.

### Benchmark harness (`tabarena/`)

- **The regression adapter accepts only `rmse`** and falls back to it without a warning (numerai: Pearson
  correlation; zillow_prize: MAE).

  **Deferred (Lennart, 2026-10-12):** solved later, with the harness.
- **Hour of day**: the default `tabarena_default` pipeline keeps it (skrub's `DatetimeEncoder`, `bundle.py:763`);
  only the v0.1 `default` pipeline (`bundle.py:746`) drops it. nyc_taxi LightGBM RMSE is 0.42-0.44 without the hour
  and 0.36-0.38 with it. It matters only if v0.2 runs the old pipeline.

  **Resolved (Lennart, 2026-10-12):** v0.2 will run a new default pipeline like BeyondArena's, which keeps the hour.
- **String columns** are embedded with Qwen3-Embedding-8B at 32 dimensions. For SMILES (apistox,
  qsar_bioconcentration) that is not a chemistry representation; a pinned RDKit featurisation would need RDKit in the
  `build` extra.

  **Resolved (Lennart, 2026-10-12):** apistox, whose only structure is the SMILES, now ships RDKit's 2D descriptors next to it (RDKit 2026.03.6, pinned in the build extra; mean ROC AUC on its windows 0.79 / 0.71 without and 0.83 / 0.82 with them, LightGBM / random forest). qsar_bioconcentration keeps the paper's 9 descriptors (RDKit added 0.006).

  **Update (Lennart, 2026-10-14):** every SMILES dataset now ships RDKit's 2D descriptors (`data_foundry.v2.rdkit_descriptors`) and no SMILES string: apistox, qsar_bioconcentration (RDKit's descriptors added, LightGBM macro AUC 0.735 -> 0.752) and drug_induced_autoimmunity_prediction (the source's descriptors). See apistox, issue 1.

### Problems in third-party copies (worth telling the maintainers)

- OpenML 46372 (CORPORATE_CREDIT_RATING_CAT, 5,000 rows) is generated from the book's 197 rows: each ratio drawn
  uniformly within its rating's range, labels inverted. TabSTAR uses it as real data.

  **Resolved (2026-10-12):** recorded as `corporate_credit_rating_cat_data_set_ratings_raitings_duplicate` (`No`, `AHDS`, `Duplicate`); the canonical record keeps the book's real rows.
- OpenML 46585 (QSAR bioconcentration) is in TabSTAR's pretraining folds with classes 2 and 3 swapped.

  **Resolved (2026-10-12):** no effect on our decisions (Lennart). "Swapped": TabSTAR's annotation names class 2 "Metabolized/Eliminated" and class 3 "Additional Storage Sites", the reverse of the source; our labels follow the source's rule.
- TabSTAR's NBA dataset (OpenML 43653) uses `Rk`, basketball-reference's alphabetical row number, as its target.

  **Resolved (2026-10-12):** the problem: `Rk` is the row number of basketball-reference's season table, sorted by player name, so the target is an alphabetical rank that the features cannot predict. It is not our nba_players_2016_2019 task; no action.
- TALENT's published scores for bias_correction (UCI 514) come from random splits, where the 25 stations of a day
  share its weather (random folds RMSE 0.62, days kept together 1.00).

  **Resolved (2026-10-12):** not relevant to our decisions (Lennart). It was listed as support for the temporal split of bias_correction: random folds give a much lower error than folds that keep a day together.
- OpenML 43838 (account debt) ships the three columns that define the label as features.

  **Resolved (2026-10-12):** noted as a problem of that copy in the account_debt_south_africa record (`total90debt`, `totalwriteoff` and `debtbillingratio` next to `baddebt`, no default target).
- SUPPORT2 (UCI 880 and hbiostat's support2.csv): in about half the rows (phase II) the 14 day-3 physiology columns
  belong to another patient, at an offset that grows along the file. The study data (ICPSR 2957) confirm it; every
  patient's correct values are in the file at another row.

  **Resolved (2026-10-12):** fixed in the definition: both phases, with the physiology rows restored using ICPSR 2957.
- MLOmics on Hugging Face: in every revision, the LGG methylation profiles do not match the patients, and the LGG and
  OV gene names do not describe their values.

  **Resolved (Lennart, 2026-10-12):** the details are in the lgg_low_grade_glioma and ov_ovarian_cancer records (LGG methylation of other patients, placeholder gene names, a shared name column). No re-sourcing from TCGA for now; LGG stays `No` and OV is retired for its unsupervised label (next section).

- churn_telco_europa (Kaggle `raumonsa11/churn-telco-europa`, OpenML 44228) carries Chilean RUT national ids and
  mobile numbers.

  **Resolved (2026-10-12):** confirmed and flagged. `CNI_CUSTOMER` holds Chilean national ids (every RUT-shaped value has a valid check digit; 102,965 distinct) and `CETEL_NUMBER` mobile numbers (183,661 distinct), with the antennas' state and city; OpenML 44228 serves the same columns. The record carries `Ethical Issue` and the evidence.
- Aeolus: the weather is Meteostat's reading at the UTC hour equal to the local scheduled time (4-10 hours early),
  and March 2024 is missing.

  **Resolved (2026-10-12):** stated as problems of the release in the aeolus record (to report to the authors later); the aeolus_1m curation notes carry both as `Anomaly:` bullets.

### Conventions to settle

- **`year`**: the working copy mixes the collection year (cdc_diabetes_health_indicators 2015 for a 2021 Kaggle cut,
  amazon_employee_access 2010) and the publication year (pkdd_15 2015); the v2 docstring says "Year the data was
  published".

  **Resolved (Lennart, 2026-10-12):** the year the data was first published, at the publication `source_url` names. 49 definitions changed (43 built, 6 new) and 37 records aligned; the uncertain cases and the sources that grow over time are left as they are (CHANGELOG, 2026-10-12).

- **`source`**: the units followed "where the cut first appeared" (Kaggle for a Kaggle cut of a government survey,
  the sdss_17 precedent); some records name the original publisher instead.

  **Resolved (Lennart, 2026-10-12):** the first publication, not a re-upload; Kaggle only when the data first appeared there or no other source is found. Applied to 10 new and 16 built definitions and 23 records; five uncertain cases left as they are (CHANGELOG, 2026-10-12).

- **Labels computed from shipped features**: brca (PAM50 centroids), glioblastoma (ssGSEA scores), the MLOmics OV
  subtypes (clusters of the same tumours' expression), central_international (the NEWS2 chart) and
  account_debt_south_africa (a rule on three columns). One rule for all of them would settle five issues.

  **Resolved (Lennart, 2026-10-12):** a label from unsupervised learning is not a real predictive task, so brca_breast_cancer (PAM50), glioblastoma (expression subtypes) and ov_ovarian_cancer (NMF clusters) are `No`; a label the source computes with a deterministic rule keeps the dataset only when dropping the rule's inputs leaves a real task (account_debt_south_africa), and central_international_medical_college_and_hospital_health_risk_prediction (NEWS2 on the shipped vitals) is `No` + `Trivial`. The rule is in the curation guidelines. coad_colon_adenocarcinoma (genomic subtypes partly defined from copy number, which it ships) is left for Lennart.

- **`task_probes.md` cases**: several units propose rows for flags they answered (expresso `one_feature`, mortgage
  `drift_baseline` and `one_feature`, rosbank1 `no_spread`, apistox `no_spread` and `unstable`, bias_correction
  `no_spread`, african_credit_scoring_challenge `no_spread` and `drift_baseline`). They are in the units' sections
  below; none was added to the reference.

  **Resolved (2026-10-12):** the rows for expresso, mortgage, rosbank1, apistox, bias_correction and african_credit_scoring_challenge are in `verify-dataset/references/task_probes.md`.

### Housekeeping

- **Personal data on disk**: `local-data-warehouse/churn_telco_europa/` (21 MB) holds RUT ids and phone numbers;
  the Alvin raw file holds private persons' names (masked in the definition). Delete or keep?

  **Resolved (Lennart, 2026-10-12):** kept; it never leaves the local warehouse.
- **Raw copies of datasets not added**: `local-data-warehouse/` holds myocardial_infarction_complications (0.9 MB),
  churn_telco_europa (21 MB), churn_telco_south_asia_duplicate (0.2 MB), hepatitis_c_egypt (0.2 MB),
  high_storage_system_data_for_energy_optimization (7.2 MB) and numerai28_6 (35 MB).

  **Resolved (Lennart, 2026-10-12):** kept for now; `minimal_inputs.py` of the rebuild skill collects what the builds need.
- **Scratch**: `../_scratch_new65/` (about 4.7 GB, outside the repository) holds the run's reports
  (`_run_reports/`) and the agents' evidence copies (archived pages, other scrapes, unpacked mirrors). The evidence
  pointers in this file lead there; keep it while the decisions above are open.

  **Resolved (Lennart, 2026-10-12):** the reports, the review page's sources, the agents' outputs and the per-dataset evidence moved to `local-data-warehouse/_runs/2026-10-07_backlog/`; farm_to_feed's raw files to its own warehouse folder; the check environment, derived frames and temporary copies deleted, and the folder removed.

- **`catboost_info/`** at the repository root (188 KB, untracked) holds CatBoost training logs from this run.

  **Resolved (2026-10-12):** removed, and `catboost_info/` is in `.gitignore`.
- **A paper to get**: IntelliSys 2017, doi 10.1109/IntelliSys.2017.8324367, would settle when churn was observed in
  churn_telco_south_asia (closed access, no free copy found).

  **Resolved (2026-10-12):** in the churn_telco_south_asia record as an open item.
- **`GETTING_STARTED.md` line 172** lists the sasol record as a large candidate; it is a duplicate.

  **Resolved (2026-10-12):** GETTING_STARTED.md no longer lists datasets or counts; it points to the filtered curation log and to the add-dataset skill's reference definitions.

## Per dataset

### 2_month_survival_rate_prediction

**Outcome:** added and checked. Since 2026-10-12 both phases, with the phase II physiology moved back into the right
rows (issue 1; the phase I-only version of 2026-10-07 is described in the verification history below).

**Record judgment:** valid with concerns.
- SUPPORT (Study to Understand Prognoses and Preferences for Outcomes and Risks of Treatments): 9,105 seriously ill
  adults at five US teaching hospitals, phase I 1989-1991, phase II 1992-1994.
- The prediction task is the source's own: "To develop and validate a prognostic model that estimates survival over
  a 180-day period for seriously ill hospitalized adults" (Knaus et al. 1995, Ann Intern Med 122:191-203, abstract,
  Objective).
- Provenance is clear: the full study data is ICPSR 2957 (issued 2001, DOI 10.3886/ICPSR02957.v2); the 47-variable
  extract support2 is released by Vanderbilt Biostatistics at hbiostat.org/data; UCI 880 re-serves it.
- Unique: I searched `curation/records/` and the working copy for SUPPORT, support2, hbiostat, ICPSR 2957, UCI 880,
  Knaus, sfdm2, hospdead and right heart catheterization (another SUPPORT-derived dataset). No other record and no
  other record of this run matches.
- Concerns:
  - the public file's phase II physiology sits in other patients' rows (issue 1; fixed with ICPSR 2957);
  - the source has several outcomes and four model or physician estimates among its columns (handled);
  - the curator's `Outdated` marker (1989-1994 care) is accepted on the record and not overridden.

**Data:**
- Every value comes from `support2.csv` (hbiostat.org/data `repo/support2csv.zip`): 9,105 rows x 47 variables plus an
  unnamed row-number column, SHA-256 79621945edf2a5c8dc36359684ff356d3c6025e773ba4fefac26f865f7894c78.
- ICPSR 2957 V2, public-use parts 9 (physiology) and 10 (key analytical variables), ASCII with data maps, downloaded by
  Lennart on 2026-10-12 (login): read at build time only to find each patient's row; none of their values is in the
  dataset. 02957-0009-Data.txt SHA-256 96859cd2…56b7d, 02957-0010-Data.txt SHA-256 1a9a41ba…4fd86 (in full in
  `download_description`). Local in `local-data-warehouse/2_month_survival_rate_prediction/icpsr_2957/`, not in git.
- UCI's copy (`https://archive.ics.uci.edu/static/public/880/data.csv`) is the same table, with the same misplaced
  physiology, except for the rounding of `prg6m`.
- Licence: hbiostat.org/data: "Permission is granted to anyone wishing to use the data sets provided here. Please
  reference the original paper ... and note 'Data obtained from http://hbiostat.org/data courtesy of the Vanderbilt
  University Department of Biostatistics.'" ICPSR's terms of use forbid redistributing its data or other materials
  without written agreement and ask to cite the study (the definition's second BibTeX entry). Lennart's call
  (2026-10-12): use ICPSR only to restore the row order and ship only support2's values.

**Definition:**
- Folder `datasets/_dev/tabarena-v0pt2/2_month_survival_rate_prediction/`, class
  `Dataset2MonthSurvivalRatePrediction`. The CLI's `_class_name` puts `Dataset` in front of a name that starts with a
  digit; import, check, discovery and the tests work. No framework problem.
- Prediction point: the end of study day 3, for a patient still alive. Knaus 1995, abstract: "11 physiologic measures
  recorded on day 3 after study entry. Physicians were interviewed on day 3"; supportdesc: "most of the patient
  assessments are made on the patient's third study day".
- Restoring the physiology, in `_clean`:
  1. `_link`: each support2 row is matched to one ICPSR patient (PSEUDOID) on ten columns that both files hold on the
     patient's own row (length of stay, hospital death, days before entry, comorbidities, age in whole years, disease
     group, sex, sps, scoma, aps); all 9,105 rows match one patient each, and all 6,201 deaths have the same day in
     ICPSR (which follows survivors to 1997: 878 later deaths, the earliest on day 361).
  2. `_source_rows`: each patient's ICPSR day-3 values, with ICPSR's normal-value fills set missing as support2 has
     them, are found among the 14-column physiology blocks of support2.csv, exactly once each. Phase I rows hold their
     own; 431 of 4,804 phase II rows do, the others' block sits 1 to 90 rows further down (jumps at block ends).
  3. `_restored`: each row takes the block of the row that holds it.
- Cohort: both phases, minus the 138 patients who died on day 3: 8,967 patients.
- Target `death_within_2_months` (Yes/No): `death` = 1 and `d.time` < 60, the cut-off of the source's sfdm2 level 5.
  Survivors were followed at least 344 days, so no label is censored. 2,993 of 8,967 are positive (33.4%; phase I
  34.2%, phase II 32.7%).
- IID with the default splits: 3 repeats x 3 folds, train 5,978 and test 2,989 rows.
- 8,967 rows x 25 features (8 categorical, 17 numeric).
- Drops (22 columns):
  - outcomes: death, d.time, hospdead, slos, sfdm2;
  - recorded after day 3: the costs charges, totcst, totmcst and avtisst (days 3-25);
  - DNR: dnr, dnrday;
  - SUPPORT model outputs: sps, surv2m, surv6m;
  - the APACHE III score aps;
  - physician estimates: prg2m, prg6m;
  - bun, glucose, urine (not measured in phase I; with them 0.817 instead of 0.814, LightGBM 3 x 5-fold);
  - the surrogate interview adls and adlsc (issue 4).
- num.co is renamed to num_co.
- Zero vital signs stay as recorded: heart rate 0 in 30 patients, mean BP 0 in 16, respiration 0 in 30; 63-83% of
  them die within 2 months, which looks like arrests on day 3.
- `_decisions` renders seven tables:
  - the physiology as published and restored (rho with aps, ROC AUC alone) per column;
  - where each of the file's ten blocks took its physiology from (offsets);
  - the checks of the link to ICPSR;
  - the dropped columns with the reason for each;
  - the interview fields' missing shares for stays that ended by day 7 and longer stays;
  - all patients by day of death;
  - the candidate targets.
- Checksum `v2:12056202e362b4fb06ec43d52b932206008964f408d086b4df896e668d524ed7`, the same under pandas 2.3.3 and
  3.0.6.

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). Nothing accepted, ruff is clean.
`tests/test_v2_datasets.py -k 2_month_survival_rate_prediction` passes, with the data-check test
(DATA_FOUNDRY_V2_DATA_CHECKS=1, which compares the README checksum). The rebuild tracer now wraps `pd.read_fwf`, which
reads the ICPSR files.

**Probes** (both phases, restored, without adls and adlsc, 2026-10-12):
- Task, 5 of 9 splits: random forest ROC AUC 0.806, LightGBM 0.802; best single feature 0.646 (scoma on 4 splits).
  Random forest beats the dummy on every split (SE 0.005); the smallest class in a test fold has 997 rows. No flags.
- Leak, 3 splits: LightGBM 0.805; best single features dzgroup 0.667, adlp 0.662, scoma 0.646; dropping each of the
  top three costs at most 0.009; missing indicators alone: adlp 0.654; no exact copies; nearest-neighbour distance
  alone 0.680.
- Generated and hidden-group probes (before the adls and adlsc drop): no rule leaves, no hits.

**Issues for Lennart:**
1. **Resolved (2026-10-12): the phase II physiology is moved back into its rows with ICPSR 2957; both phases ship.**
   (Was: phase I only, or re-source the physiology from ICPSR 2957.) In `support2.csv` (and UCI 880) the 14 day-3
   physiology columns of most phase II patients belong to another patient.
   - Evidence: crea against aps (APACHE III, computed from the same day-3 values) has Spearman 0.522 in phase I and
     0.053 in phase II. In rows 4,351-5,700 it is -0.006 on the same row and 0.542 against the row 47 lines down.
   - The offset grows along the file, up to 73-87 rows near the end. Age, diagnosis, scoma, hday, ADL, sps, surv2m and
     the outcomes stay aligned.
   - In phase II, each physiology column alone scores ROC AUC 0.50-0.53, against 0.51-0.64 in phase I.
   - Implemented: phase I only. 4,232 patients, 34.2% positive, 27 features; LightGBM 0.801 (3 x 5-fold), random
     forest 0.796 in the task probes.
   - Alternative: re-source the correctly linked physiology from ICPSR 2957. Its access terms are unchecked (the page
     returns 403). That would give all 8,967 patients alive after day 3, with bun, glucose and urine for phase II.
   - Not recommended: realigning by offset. The offset changes inside blocks, and some rows have no match.
   - **How it was resolved (2026-10-12):** Lennart downloaded ICPSR 2957 parts 9 and 10. Every phase II patient's correct block is
     in support2.csv at another row; the definition finds it through ICPSR and moves it back, shipping only
     support2's values (Lennart's call). Both phases, 8,967 patients; LightGBM 0.814 (3 x 5-fold); a model fit on
     phase I scores 0.812 on phase II restored, 0.695 as published.
2. **Which target** (the record asks "binary or regression"). Same 4,232 patients and 27 features, LightGBM
   3 seeds x 3-fold:

   | framing | rows | positives or classes | score | why not shipped |
   |---|---|---|---|---|
   | death within 2 months (shipped) | 4,232 | 34.2% | ROC AUC 0.801 (surv2m 0.806) | |
   | death within 6 months, Knaus's primary endpoint | 4,232 | 47.1% | ROC AUC 0.787 (surv6m 0.788) | a nested version of the shipped label; the record is named after 2 months |
   | death in hospital (`hospdead`) | 4,232 | 25.5% | ROC AUC 0.862 | depends on discharge practice, not the source's survival question |
   | log total cost `totcst`, supportdesc's "Continuous (total hospital costs ...)" | 4,095 | 137 missing | R^2 0.608 | a resource-use task on the same rows; a candidate for its own folder |
   | log length of stay `slos` | 4,232 | | R^2 0.287 | a stay ends at death or discharge, so it mixes both |
   | sfdm2, ordinal 2-month function | 3,542 | 690 missing; "Coma or Intub" 12 | log loss 0.982 (prior 1.182) | its level 5 is the shipped label; missing for 16% of patients (survivors without an interview); one class of 12 |

   `death` (any time up to 1994) has no fixed horizon. The binary framings are nested versions of one signal, not a
   multi-output task, so the record's `Multi-target` tag does not describe the shipped task (your call; not stripped).
   The record's `problem_type` (TBD) would be Binary Classification.
3. **Cohort: the 69 phase I patients who died on study day 3 are dropped.** Their day-3 values include values at death:
   heart rate 0 in 42% and mean BP 0 in 30% of them, against at most 5.5% and 0.9% of the later deaths. Alternative:
   keep them, which gives 0.811 instead of 0.801 (3 x 5-fold).
   - Both phases (2026-10-12): 138 patients; heart rate 0 in 38% and mean BP 0 in 25% of them, against at most 7.1%
     and 3.4% of the later deaths; keeping them gives 0.822 instead of 0.814.
4. **Resolved (2026-10-12): adls and adlsc are dropped; adlp, edu and income stay** (Lennart's call after a context
   review). (Was: the interview fields are kept.) The ADL answers describe function two weeks before admission,
   but the interviews took place on study days 2-7 (median day 4): adls is missing for 46% of the patients whose
   stay ended by day 7 against 24% of longer stays, and adlsc's imputed values used the interview status ("Pt
   Death", "Pt Discharged"). adlp is missing mostly when the patient cannot answer; edu and income are missing as
   often for short as for long stays.
   - The codebook labels them "ADL Patient Day 3" and "ADL Surrogate Day 3", but some interviews came later: adls is
     missing for 65% of the day-4 deaths and 48% of the day-5 deaths, against 30% of survivors. The physicians'
     day-3 prg2m is missing for 41% of the day-4 deaths, against 21-22% from day 8 on.
   - The model does not use these gaps: without adls and adlsc, the AUC moves 0.916 → 0.915 for deaths on days 4-6
     against survivors and 0.780 → 0.779 for deaths on days 7-59.
   - All five fields add 0.006 (0.795 → 0.801). Alternative: drop them.
   - Both phases (2026-10-12): adls missing for 65% of the day-4 and 47% of the day-5 deaths, against 28% of the
     survivors; without adls and adlsc 0.925 → 0.920 (deaths on days 4-6) and 0.784 → 0.782 (days 7-59); the five
     fields add 0.010 (0.804 → 0.814). New: adlsc is set missing where it was imputed, since the imputation used the
     interview status, which includes "Pt Death" and "Pt Discharged" (codebook Appendix A); ROC AUC unchanged.
5. **dnr and dnrday are dropped** (record: "need to filter dnr"; supportdesc advises against both).
   - dnrday equals the days to discharge for all 2,785 patients without an order, and 793 of the 1,365 orders written
     after entry are dated after day 3.
   - Alternative: a flag for "DNR order by day 3" would be known at the prediction point (646 patients, 62.2% die
     within 2 months) and raises ROC AUC from 0.801 to 0.810. But the order is a care decision that carries the
     physician's prognosis.
   - Both phases (2026-10-12): 1,659 of the 2,865 orders after entry are dated after day 3; dnrday equals the days to
     discharge for all 5,842 patients without an order; a flag for an order by day 3 (1,437 patients, 61.6% die)
     raises ROC AUC from 0.814 to 0.822.
6. **No grouping by the ten blocks of the file.** The blocks alternate phase I and phase II, probably one pair per
   hospital (undocumented). The split stays IID:
   - the use case is new patients at the same hospitals (Knaus validated on later patients of the same five);
   - five groups would make a test of shift between hospitals;
   - two phases cannot give 3 temporal windows.
7. **Year** stays 1994 as in the record (end of accession). ICPSR issued the data in 2001, the hbiostat CSV is dated
   2003, and UCI gives 1995.

**Verification** (of the phase I version, 2026-10-07):
1. Phase II physiology misaligned (blocker): **applied.** I reproduced it with my own code.
   - crea against aps: 0.522 in phase I, 0.053 elsewhere; in rows 4,351-5,700, -0.006 on the same row and 0.542 at
     +47 rows.
   - A 150-row offset scan with a phase-I model predicting aps from the physiology: phase I segments match at offset
     0 (rho 0.96-0.99). Phase II segments match at 0 (rows 901-1,200), 14 (2,401-2,850), 47 (4,351-5,700 and
     6,751-7,200) and 73-87 near the end.
   - At +47, the physiology predicts the outcome and sps of the row above it; age, dzgroup, scoma, hday, adlsc and
     surv2m match only at offset 0.
   - UCI 880 is identical. Implemented phase I only; issue 1 for Lennart.
2. aps bullet and issue 5: **applied.** On phase I, adding aps changes ROC AUC from 0.801 to 0.801. The bullet is
   rewritten and the old issue 5 is removed.
3. Phase and hospital are in the file: **applied.** The note now says how phase I is identified (survivors followed
   1,301-2,029 days, all others at most 1,090) and why the ten blocks are not used as groups (issue 6).
4. Zero vital signs: **applied.** Restated for phase I: 10, 3 and 10 zeros, of which 80%, 100% and 60% die within
   2 months; kept as recorded.
5. Interview bullet: **applied.**
   - Added the codebook labels and the prg2m corroboration, recomputed on phase I: 41.3% missing for day-4 deaths,
     against 20.8-22.4% from day 8.
   - Replaced "kept on purpose" with "Note:".
   - Defined comatose as scoma > 0 (92.7%); dzgroup Coma is 99.1%.
   - Added the adls/adlsc drop check on phase I.
6. Target table: **applied** in issue 2: totcst, slos and sfdm2, with their numbers and why they were not taken.
7. Stale numbers: **applied.** Probes, decision tables, comments and checksum are recomputed on the phase I definition.

### account_debt_south_africa
**Outcome:** added and checked
**Record judgment:** valid with concerns. The data traces to an identifiable uploader: Dylan Rawlins of DMS Technologies (dmstechnologies.co.za, a South African software firm that lists a "Debt Risk Analysis" product), who extracted "approximately 20 million records" from "the billing systems of 8 Municipalities in South Africa over a 2 year period" and summarised them per account in PostgreSQL (Kaggle data card, "Context"; the uploader's notebook `dmsconsultingsa/municipal-debt-risk-analysis-v1`, "Methodology"). The municipalities are not named and the file has no account or municipality id; the record's comment ("Looks real enough and good") accepts this provenance. Unique: no record or working-copy folder cites the Kaggle slug, OpenML 43838 or the name, and no record of this run is the same data; OpenML 43838 is a copy of the Kaggle file (same 138,509 rows in the same order). The record's comments do not weigh three data problems, all fixed in the definition: the label is a rule of three shipped columns, 20% of the rows come from segments of the file without recorded debt, and the payment totals sum the window at whose end the label is read (issues 1-3).
**Data:** Kaggle dataset `dmsconsultingsa/municipal-debt-risk-analysis`, version 1 (the only one, 4 June 2020), pinned as `kaggle datasets download dmsconsultingsa/municipal-debt-risk-analysis/1`. One file, `MunicipalDebtAnalysis.csv`: 138,509 rows x 16 columns, md5 d5fa5aaf696e31a65eebb0532fa4568d, no missing values. Licence CC0-1.0 (Kaggle metadata `licenses`; OpenML 43838 says "CC0: Public Domain"). The dataset has no Kaggle discussions and two notebooks (the uploader's and an auto-generated starter).
**Definition:** `datasets/_dev/tabarena-v0pt2/account_debt_south_africa/`. Prediction point: an account at the date of the extract, with its account category, property value and size, whether an ID number is on file, and what the municipality billed it over the two years before (total, per billing line, electricity); the label is its bad-debt status at the extract, and neither the arrears and write-offs that set it nor the payments of the same two years are features. Target `BadDebt` (Yes 57,199 / No 44,672), binary, ROC AUC. IID, default 3 x 3 stratified folds (train 67,914, test 33,957). 101,871 rows x 7 features (1 categorical, 6 numeric). Cleaning: drop the 27,938 rows of seven runs of 1,185-8,762 consecutive file rows without any recorded debt (runs of at least 1,000 rows, found in file order before any other filter); drop 8,700 accounts outside the uploader's cohort (`totalbilling` <= 0 or `totalreceipting` < 0, as the notebook does); drop `total90debt`, `totalwriteoff`, `debtbillingratio` (they set the label) and `totalreceipting`, `avgreceipting`, `collectionratio` (payments of the window); drop `accountcategoryid` and `acccatabbr` (the category twice more); rename to the data card's field names; a `PropertyValue` or `PropertySize` of 0 becomes missing (none on file). Four `_decisions`: the label-rule table, the bad-debt rate by share of billing paid, the runs table, a figure of the runs along the file. Checksum v2:59a68296bb2376f78cfee37a2f83f3b59d326a9208de4f07b3c29b9ac6c33952, the same under pandas 2.3.3 and 3.0.6.
**Checks:** `dataset check`: 0 errors, 1 warning (accepted), 1 info. `dataset_duplicate_rows` (6,355 rows, 6.2%) accepted: plausibly distinct accounts with the same property record or flat charge (162 accounts billed R6 in six R1 lines), no account id to tell them apart, and without the copied test rows ROC AUC on split 0/0 falls only from 0.874 to 0.867. Info `dataset_conflicting_duplicate_rows`: 554 feature vectors (2,430 rows) with both labels, explained by the unobserved payments and opening balance; kept. `ruff` clean; `load_definition` imports; `pytest tests/test_v2_datasets.py -k account_debt_south_africa` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed (the scratch-root copy too).
**Probes** (revised definition, threads capped at 2; outputs in `probes2/` and `probes/variants.txt`):
- Before any fix, on the whole file (3-fold CV): LightGBM ROC AUC 0.999, 0.998 from the three debt columns alone; a depth-3 tree reaches 0.997 by splitting on `debtbillingratio` and `total90debt`. This is the label rule.
- `leak_probes.py` (3 splits): all features 0.872; depth-2 / depth-3 tree 0.780 / 0.803; alone: `PropertyValue` 0.787, `PropertySize` 0.750, `AverageBilling` 0.740, `TotalBilling` 0.706, `TotalElectricityBill` 0.670; missing indicators 0.513 and 0.506; without `PropertyValue` 0.859, without `AverageBilling` 0.862; exact feature copies for 7.3% of test rows (subsampled train); 1-NN agreement 0.833 / 0.731 / 0.508 (closest tenth / all / chance); nearest-neighbour distance alone 0.671. No column comes near the full model.
- `task_probes.py` (5 of 9 splits): no flags. ROC AUC / log loss: dummy 0.500 / 0.686, linear 0.752 / 0.635, random forest 0.874 / 0.438, LightGBM 0.871 / 0.444, single feature 0.787 / 0.550 (`PropertyValue` on all 5 splits, 77% of the best skill). The best family beats the dummy on 5 of 5 splits (standard error 0.001); random forest minus linear +0.244 (paired SE 0.004); smallest class per test fold 14,890 rows.
- `generated_probes.py`: rule leaves cover 0.0% of the minority rows; no flags.
- `hidden_groups.py`: no hits. Largest gaps: `TotalBilling` +0.020, `PropertyValue` +0.019 (accounts sharing a property record), `PropertySize` +0.006; no attributes.
- Feature-set variants (LightGBM, one 3-fold stratified CV with seed 4267 on the curated rows; AUC / log loss, class prior 0.686): shipped 7 columns 0.874 / 0.439; with the payment totals 0.952 / 0.279; without `TotalElectricityBill` 0.865 / 0.453; without `HasIDNo` 0.872 / 0.442; category, property value and size and `HasIDNo` only 0.832 / 0.500. With the seven runs kept: run membership predicted at AUC 0.988 from the 7 columns, run rows get a mean bad-debt probability of 0.15, and the other test rows score 0.854 (0.874 on the curated data).
**Issues for Lennart:**
1. **Segments without recorded debt (20% of the file): dropped by a rule on the file order. Keep that, keep the rows, or retire?** Seven runs of 1,185 to 8,762 consecutive rows (27,938 rows) hold no account with debt aged 90+ days or a write-off. Inside them 11,984 billed accounts paid nothing in two years and none is a bad debt (91.5% of the 40,984 such accounts elsewhere); the 2,282 that paid at most half of their billing are no bad debts either (89.6% of 6,631 elsewhere). They are not new accounts (non-payers with 24-100 billing lines: 0% bad inside, 97-98% outside); payments were recorded (56.6% of the billed accounts in the runs paid something); ID numbers 0-0.7% against 53% elsewhere. Debt was not recorded there. Kept, they are a learnable recording artefact (membership AUC 0.988). Implemented: drop runs of at least 1,000 rows; the next shorter runs (334 and 218 rows) are paying accounts whose zero debt is consistent, and a 186-row run of non-paying accounts with ID numbers stays in (an anomaly bullet). Alternative: retire as `Data Quality Issue`, following ghanas_indigenous_intel ("no event" mixed with "not recorded": retire unless the recording process can be recovered), if a rule on the raw file order is not acceptable; or ask DMS Technologies which municipalities lack debt data.
2. **The label is a rule of three shipped columns.** Every account with `total90debt` > 0 or `totalwriteoff` > 0 is a bad debt, and all but 371 of the 74,909 others are not (138,138 of 138,509 rows); AUC 0.999 with them. Dropped, as the uploader's notebook does ("These fields are used to determine whether a consumer is already a bad debt and not to predict whether they will become a bad debt"). OpenML 43838 ships them as features, so a benchmark that uses that copy unchanged scores a lookup (the record lists the dataset in TabSTAR; its preprocessing was not checked). No alternative proposed.
3. **The payment totals are dropped (prediction point).** `totalreceipting`, `avgreceipting` and `collectionratio` sum the payments of the two years at whose end the status is read; arrears are billing less payments plus the opening balance. The bad-debt rate falls from 91.5% for accounts that paid nothing (97% when billed over 24-100 lines) to 14.7% for those that paid 87.5-105% of their billing. Dropped by the mutual_funds_india rule (patterns §D.2). Implemented: dropped (AUC 0.874). Alternatives: keep them as the uploader does, whose notebook's main feature is the collection ratio (AUC 0.952); or keep only the static profile, category, property value and size and `HasIDNo` (0.832). A deployed model with them mostly flags accounts the municipality's age analysis already lists.
4. **`TotalElectricityBill` may reflect credit control.** The data card: the municipality "has the right to cut a consumer's electricity connection" when an amount is outstanding; bad debts have electricity billed less often in every property-value quintile (0.11-0.30 against 0.20-0.57). Implemented: kept with a `Potential leak, kept on purpose` bullet (AUC 0.874 with, 0.865 without). Alternative: drop it.

   **Resolved (Lennart, 2026-10-12):** kept. The signal is mostly whether the municipality bills electricity at all (in 12 of 52 file blocks of 2,500 rows most accounts get a bill; there 26.6% of billed accounts are bad debts against 51.0%); among billed accounts electricity is the same share of the bill for bad debts and others (median 0.33), so cut-offs within the window leave no trace. The bullet says so.

5. **`HasIDNo` may be captured during collection.** Accounts with an ID number are bad debts more often (63% against 48%), the opposite of what the data card implies, and capture follows the municipality (0% to 94% per 2,500 rows). Implemented: kept with a `Potential leak, kept on purpose` bullet (AUC 0.874 with, 0.872 without). Alternative: drop it.

   **Resolved (Lennart, 2026-10-12):** kept. The data card describes it as a property of the holder (useful in legal proceedings, marks a person, "often not captured properly or at all") and says nothing about when it is captured. The difference holds within Residential (64% against 47%), not for Business, Agricultural or Unknown. The bullet quotes the card.

6. **The uploader's cohort filter.** 8,700 accounts dropped: 903 not billed in the window, 7,722 with a net credit, 121 with negative payment totals (46 overlap); 77.8% are bad debts whose debt predates the window. Implemented as the notebook does. Alternative: keep them.
7. **Duplicates kept.** 6,355 exact duplicate rows (6.2%, groups up to 162); 8.1% of the test rows of split 0/0 have an exact copy in train, and ROC AUC there is 0.874 on all test rows, 0.867 without them. Implemented: kept, warning accepted. Alternative: drop exact copies (wine_quality precedent), which would remove plausible distinct accounts.
8. **Municipality structure and a weak residual.** The file is in blocks (bad-debt rate 0% to 98% per 2,500 rows), likely the 8 municipalities and account-number ranges; no column identifies them, so the split is IID (a municipality scoring its own accounts). In rows 134,000-138,499 (92% Unknown category) only 62% of the 1,511 billed never-payers are bad debts (93% elsewhere); debt may be recorded incompletely there too, but no boundary exists to cut at, so it is kept with an anomaly bullet.

   **Resolved (Lennart, 2026-10-12):** IID kept, tagged `ForcedIIDFromTemporal`: the file is one extract without dates, so the status at the extract stands in for the forecast the card aims at. A municipality scores its own accounts; held out by file position, LightGBM ROC AUC falls from 0.877 (random 3-fold) to 0.843 (blocks of 2,500 rows), 0.825 (10,000 rows) and 0.786 (thirds), which a bullet records; no column identifies the municipality. The tail is one run of category Unknown (rows 134,192-138,276; 2,396 curated rows), mostly billed 1-3 times in two years (never-payers with 1-3 bills: 53% bad debts, 86% elsewhere); debt is recorded there, so it stays, with the anomaly bullet rewritten.

**Verification:** (independent verifier, verdict "needs changes")
1. Payment totals cover the window that sets the label (blocker): applied. Checked first: never-payers billed over 24-100 lines are 97.3% bad debts (25,942 accounts), the bad-debt rate by share paid runs from 91.5% to 14.7%, and nothing shows the window does not define the target. The three columns are dropped; the prediction-point and drop bullets are rewritten; probes re-run (no flags). Keeping them, and also dropping `TotalElectricityBill`, are issues 3 and 4 with their numbers.
2. Run drop kept, wording: applied. "Debt was not recorded"; added the partial payers (2,282 inside, 0% bad; 6,631 outside, 89.6%) and that 56.6% of the 27,623 billed accounts in the runs paid something (recomputed). The run-segment numbers are recomputed for the 7 columns.
3. Exact-copy share: applied. Recomputed on the full first split of the revised frame: 8.1% (the probe's 7.3% subsamples train); ROC AUC 0.874 with the copied rows, 0.867 without.
4. Zero property value and size: applied. 0 becomes missing in both columns (8,943 and 8,849 rows, 6,129 both), with a bullet; the checksum is the same under pandas 2.3.3 and 3.0.6.
5. Rows 134,000-138,500: applied as an anomaly bullet with recomputed numbers (62% of 1,511 never-payers against 93% elsewhere); kept, issue 8.
6. Record comment: applied. It now names the payment-totals decision (118 words). The record's `v2_path` stays unset until `sync-notebooks` runs, which this run may not do.

### aeolus

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/aeolus_1m/`, `version_of = "aeolus"`). The verification fix round
changed only the text, one decision and the columns `_load_raw` reads. The frame and splits are identical (see Verification).

**Changed on 2026-10-12 (Lennart's review):** two-week test windows and the history from 2023 on (issues 3 and 4); the Definition, Checks and Probes below describe the definition of 2026-10-07.

**Record judgment:** valid with concerns.
- Source: Xu et al., "Aeolus: A Multi-structural Flight Delay Dataset", NeurIPS 2025 Datasets and Benchmarks
  (arXiv:2510.26616; https://neurips.cc/virtual/2025/poster/121793).
- Release: the authors published the data on Kaggle (flnny123/mfddmulti-modal-flight-delay-dataset, files dated 2025-10-17)
  and the code on GitHub (Flnny/Delay-data).
- Data: BTS on-time performance records 2016-2024 joined with hourly Meteostat weather. Sec. 3.1, p. 5: "spanning from 2016
  to 2024, with raw data containing 56,668,600 flight records". The rows per year match Table 8 exactly (total 54,674,003
  = Table 2). March 2024 is absent from the release.
- Uniqueness: the working copy holds no flight data.
  - `airlines` (OpenML 1169) comes from the 2009 Data Expo (flights up to 2008).
  - `airlines_depdelay_10m` (OpenML 42728) is "the first 10 million rows" of a 1987-2013 file.
  - `pnwflights14` covers 2014.
  - No other record of this run is flight data.
- Scope: delay prediction with a temporal split, which the guidelines name in scope ("e.g. delay/price regression ... is
  in-scope").
- Concerns: the target choice and the timing of the weather (issues 1 and 2).

**Data:**
- Source: the authors' Kaggle release, tabular modality only:
  `Aeolus/Flight_Tab/flight_with_weather_{2016..2024}.csv`, 9 files, 15.2 GB, 54,674,003 rows x 34 columns.
- Downloaded with `kaggle datasets download -f` into `local-data-warehouse/aeolus/`. The flight-chain (.pt) and network
  (.dgl) files are not downloaded.
- `_prepare_raw_files` streams the CSVs with polars into `aeolus_flights.parquet`. `_load_raw` reads 21 of its 34 columns.
- Licence: the Kaggle data card says "apache-2.0"; the paper says "CC BY-NC 4.0" (App. A.3, p. 18, "Our code and dataset
  follow the CC BY-NC 4.0 International License"; also checklist item 5). The GitHub repo has no licence file. Noted only.

**Definition:**
- Prediction point: shortly before the scheduled departure. Known then:
  - the schedule: date, carrier, flight number, route, scheduled times and block time;
  - the airport coordinates;
  - the weather at both airports. The release looked up Meteostat's hourly records, which are in UTC, by the local
    scheduled clock times. So the origin weather was observed a median 5.2 h before the departure and the destination
    weather a median 3.0 h before it.
- Target: `ARR_DEL15`, an arrival 15 minutes or more late (US DOT definition); binary, scored with ROC AUC. 18.5% positive
  overall; 16.5%, 25.1% and 26.5% in the three test weeks.
- Regime: temporal on `FL_DATE`, `TemporalSplits(window=7, unit="days", n_windows=3, gap=1)`.
  - Test weeks: 2024-12-25..31, 12-18..24 and 12-11..17, with 127,743, 130,808 and 128,644 flights.
  - The 1-day gap is there because a flight's label is known only once it lands.
  - `subsample_to_budget`: each train side is a random 1M of all earlier flights (TabReD sampling).
- Container: 1,387,518 rows x 18 features (4 categorical, 1 datetime, 13 numeric).
- Cleaning:
  - `_load_raw` skips 13 columns: the 7 recorded after departure, FLIGHTS (constant), the date parts of FL_DATE and the
    two airport indices.
  - `_clean` drops DEP_TIME and ARR_TIME (read only for decision 1), ARR_DELAY (the target's source) and the scheduled
    timestamps, which become minutes since midnight.
  - Precipitation of 213-257 mm/h is a missing-value code and is set to missing: 21,708 origin and 25,272 destination values,
    99.8% of them at EWR, LGA and JFK from November 2016 to October 2018.
  - CRS_ELAPSED_TIME below 15 min is set to missing (17 rows).
  - One flight recorded twice, with delays of 941 and 4 minutes: both rows dropped.
  - Categories are sorted.
- Four `_decisions` tables:
  1. The weather is looked up by the scheduled clock hours: 100% of the airport x scheduled-hour groups share one value,
     against 37-48% of the groups keyed by the actual times.
  2. The clock hour was read as UTC. Per airport, the coldest and warmest scheduled hours of summer 2024 fall at 4-6 h and
     12-17 h local time only when read as UTC. Read as local time, Honolulu is coldest at 15 h.
  3. The target's variance share.
  4. The precipitation code, with the JFK station-file check in the text.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). No accepted warnings.
- Final checksum under pandas 2.3.3 and pandas 3.0.6 (pd3 venv): `v2:8cb3546254438e84603740f1064d95469df95c5868a8566add4fb700830d0569`.
- `pytest -q tests/test_v2_datasets.py -k aeolus`: 1 passed, 1 skipped; with `DATA_FOUNDRY_V2_DATA_CHECKS=1`, 2 passed.
- ruff is clean.
- Peak RSS of a check: 35.0 GB, about 2 min 45 s (47 GB before `_load_raw` was narrowed).

**Probes** (run before the fix round, on the identical frame; frame hash `687341c4…` before and after):
- **task** (3 windows, default 50k rows):
  - ROC AUC: LightGBM 0.615, random forest 0.607, logistic 0.605, best single feature (CRS_ARR_TIME_MIN) 0.585.
  - Flag `no_spread` (0.020, paired SE 0.020). Answered by re-running with `--max-rows 300000`: the families spread (0.634,
    0.619, 0.607; +0.054, paired SE 0.023) and no flag remains. The benchmark trains on 1M rows.
- **generated:** rule leaves cover 0.0% of the minority; no flags.
- **leak** (200k rows per side, 3 windows):
  - All features 0.607; depth-2/3 tree 0.586/0.590; CRS_ARR_TIME_MIN alone 0.591, CRS_DEP_TIME_MIN alone 0.590.
  - Missing indicators 0.50. Exact copies across the split 0.0%. Label-free NN distance 0.529.
  - The time of day is the known core of the task. On the shipped splits with 1M training rows:
    - scheduled times alone: 0.618 / 0.580 / 0.592;
    - all features without them: 0.632 / 0.603 / 0.604;
    - all features: 0.673 / 0.640 / 0.639.
- **hidden_groups / group_probes:** not run, the task is temporal. Flight numbers and routes recur over time, so the
  temporal split matches deployment.

**Issues for Lennart:**
1. **Target: the 15-minute indicator, not the record's regression.**
   - Implemented: `ARR_DEL15` with ROC AUC.
   - Evidence:
     - The 1% longest delays hold 56-71% of ARR_DELAY's variance in every year.
     - LightGBM on the minutes reaches R² 0.009-0.024 in the test weeks, or 0.041-0.056 with the authors' 1st-99th
       percentile cut (a selection on the outcome).
     - The indicator reaches ROC AUC 0.635-0.667.
     - The paper reports the classification task in Tables 3-7, the regression only in Table 3.
   - Alternative: `aeolus_reg_1m` on ARR_DELAY.
   - The record's `problem_type` becomes Binary Classification; the orchestrator sets it together with `v2_path` (the
     verifier agrees).

   **Resolved (Lennart, 2026-10-12):** kept; the record's `problem_type` is Binary Classification.

2. **Weather timing (corrected in the fix round; the earlier "oracle forecast" reading was wrong).**
   - Implemented: the weather stays as released. The bullet "Potential leak, kept on purpose (small)" gives the numbers.
   - Evidence: the release looked up Meteostat's UTC hours by the local scheduled clock times, so the weather was observed
     hours before the scheduled times.
     - Origin weather: a median 5.2 h before the departure.
     - Destination weather: a median 3.0 h before the departure. It comes after the departure for 1.86% of the flights
       (1.0% in each test week), a median 0.75 h after it, mostly West Coast to East Coast flights.
     - Guam departures (3,243) get weather from after the departure.
     - Upper bound of what is at stake: the destination weather as a whole adds 0.010-0.016 AUC.
   - Alternatives:
     - set the 1.9% late readings to missing (needs a time-zone table per airport, a fix of our own);
     - re-join Meteostat at the local scheduled hours (our own fix; at the scheduled arrival it would add a perfect-forecast
       leak, so the verifier and I advise against it);
     - drop the destination weather (-0.010 to -0.016 AUC).

   **Resolved (Lennart, 2026-10-12):** kept as released, with the numbers recomputed for the 2023-2024 history (destination weather after the departure for 1.94% of the flights, 0.9-1.0% per test window; 686 Guam departures).

3. **History: all nine years in the train pool.**
   - Implemented: the whole release (TabReD sampling, as in delivery_eta_1m and consumer_complaints_1m). Each train side is a
     random 1M of 2016-2024 flights, which includes COVID-19 2020-21 and the change of carriers in 2018.
   - Evidence: LightGBM with 1M training flights drawn from 2016, 2022 or 2024 on; ROC AUC per training pool, test weeks
     newest first (Dec 25-31, 18-24, 11-17):
     - from 2016 on: 0.652 / 0.618 / 0.615;
     - from 2022 on: 0.628 / 0.624 / 0.625;
     - 2024 only: 0.648 / 0.617 / 0.643.
     No pool is consistently better.
   - Alternative: start in 2022 (19.3M flights) or in 2024 (6.3M).

   **Resolved (Lennart, 2026-10-12):** changed: flights from 2023-01-01 on (12,930,302), read only those. TabReD's random sample of all nine years put about 11.5% of each train side in 2024 and mixed in COVID-19 (2020: 9.7% late), while a model refit every two weeks trains on recent data that holds the previous holidays; the authors' own benchmarks use 2024 alone (June 1-15 for the tabular task, Sec. 4.1). The comparison above does not decide it: each pool is best in one week, and the winner follows the kind of week. The precipitation code (2016-2018) and the duplicated flight (2018) fall before the history, so their steps and the fourth decision are gone.

4. **All three test weeks are the Christmas peak.**
   - Implemented: the convention, walking back from the newest data with weekly windows (Lennart's one-to-two-week rule
     for weather tasks).
   - The test weeks have 16.5%, 25.1% and 26.5% late arrivals, against 20.8% for 2024.
   - Alternatives, late share per window, newest first (recomputed; they match the verifier's):

     | windows | late share per window, newest first |
     |---|---|
     | the next three weeks back | Dec 4-10: 16.8%; Nov 27-Dec 3: 17.5%; Nov 20-26: 17.2% |
     | two weeks | Dec 18-31: 25.8%; Dec 4-17: 16.7%; Nov 20-Dec 3: 17.3% |
     | months | Dec: 21.1%; Nov: 14.6%; Oct: 13.2% (563k-600k flights, capped to 500k) |

   - Lennart's call.

   **Resolved (Lennart, 2026-10-12):** two-week windows: 2024-12-18..31 (25.8% late), 12-04..17 (16.7%) and 11-20..12-03 (17.3%), 258,551, 256,013 and 269,272 flights. Only one window falls in the holiday peak. (The newest weekly windows were two peak weeks, 26.5% and 25.1%, and one ordinary week, 16.5%.)

5. **Licence conflict (noted only).** The Kaggle card says Apache-2.0, the paper says CC BY-NC 4.0. BTS data are US
   government works. Meteostat's page states CC BY 4.0 (dev.meteostat.net/license).
6. **No pinned version.** kaggle 2.2.2 refuses `owner/slug/versions/N` (the verifier tested it).
   - `download_description` lists SHA-256 prefixes of the nine CSVs; the verifier re-hashed all nine and they match.
   - A local backup of the 15.2 GB of CSVs is the safeguard.
7. **Memory.** `_load_raw` now skips the 13 columns `_clean` only dropped. A check peaks at 35.0 GB, down from 47 GB.
   - The frame is identical (Verification, finding 7).
   - This matters for parallel rebuilds.
8. **Upstream data problems, worth reporting to the authors:**
   - the weather join: Meteostat's UTC hours were matched to local clock times, so the weather is from 4-10 hours before
     the scheduled times;
   - March 2024 is missing, so the "full-year 2024" data of Sec. 4.2 lack March;
   - the precipitation code (213-257 mm/h at the New York airports, 2016-2018), which Meteostat's own JFK record shows as
     missing;
   - Table 9 gives Fahrenheit, inches and mph, but the data are degrees C, mm and km/h;
   - the tabular classifier labels `abs(ARR_DELAY) > 15` (exp/Tab_exp/Deep_Model_Classifier.py:18), which counts early
     arrivals as delays, and it fits its encoders and scaler separately on train, validation and test;
   - the checklist says the carrier codes were anonymized, but they are the real IATA codes.
   Only the precipitation code changes the definition (it is set to missing). The rest is noted in `curation_comments`.

   **Resolved (Lennart, 2026-10-12):** noted only, not reported.

9. **Flight number as a 7,096-level categorical** (minor).
   - The paper lists it as categorical. Untuned LightGBM is unchanged without it (0.675/0.640/0.639 against
     0.673/0.640/0.639).
   - Some models may handle a 7k-level category poorly.
   - Alternative: numeric, or drop it.

   **Resolved (Lennart, 2026-10-12):** kept as a categorical.

10. **Sibling records** (from the verifier). `airlines_depdelay_10m` (suggestion Yes, AI-unverified) and `airlines` hold BTS
    on-time data of earlier years. When one of them is processed, decide whether it is a second US flight-delay task or a
    duplicate of this one.


   **Resolved (Lennart, 2026-10-12):** a dated note in both records; decided when they are processed.

**Verification (fix round, 2026-10-07):** the verifier's verdict was "needs changes, text only". I re-checked each finding
with my own code (scripts in `fix/`):

| # | Finding | Response | My evidence |
|---|---|---|---|
| 1 | major: the weather is Meteostat's reading at the UTC hour equal to the local scheduled clock time, 4-10 h before the scheduled times | **accepted, fixed** | see below |
| 2 | March 2024 missing | **accepted**: `Anomaly:` bullet, upstream line (issue 8) | 3,257 of 3,288 days present; the 31 missing are 2024-03-01..31; 2024's 11 months sum to 6,284,841 |
| 3 | the cohort bullet credited the paper with the exclusion reason | **accepted, reworded** | no row lacks DEP_TIME, ARR_TIME or ARR_DELAY |
| 4 | test weeks in the Dec 11-31 peak | Lennart's call; the alternatives are in issue 4 | all late shares recomputed, all match |
| 5 | target stays; record `problem_type` | Lennart's call; noted in issue 1 | n/a |
| 6 | JFK precipitation code: no Meteostat value at the coded hours | **accepted, with corrected counts** | see below |
| 7 | optional: `_load_raw` reads 13 columns that are only dropped | **done** | see below |
| 8 | sibling BTS records | issue 10 | n/a |

- **Finding 1, re-checked three ways.**
  - Daily cycle, from the data alone: the coldest and warmest scheduled departure hours of summer 2024 sit at the
    UTC-shifted local hours (HNL 15 h and 0 h, PHX 12 h and 23 h, JFK 9 h and 17 h). This is now decision 2.
  - Meteostat station files (the verifier's downloads), exact match of the 2024 airport-hours, read as UTC against at the
    true offset:
    - JFK 6,308/6,320 against 529;
    - ORD 6,304/6,308 against 429;
    - DEN 7,021/7,033 against 207;
    - PHX 6,964/6,966 against 159;
    - LAX 7,176/7,190 against 423;
    - SEA 6,967/6,989 against 413;
    - HNL 6,247/6,247 against 243;
    - ATL 1,346/6,529 (another station, as the verifier noted).
  - Timing with IANA zones from OpenFlights:
    - origin reading: a median 5.15 h before departure, 1st-99th percentile 3.5-9.9 h; after departure only for Guam's
      3,243 departures;
    - destination reading: a median 3.0 h before departure; after it for 1.862% (1.01-1.05% per test week), a median
      0.75 h after, 99% within 2.17 h. Only 0.61% of all flights get it more than 1 h after departure. Of the 3,249
      cases beyond 3 h, 3,242 are Guam departures (all of them but one).
  - Changed: the prediction-point bullet; a new weather `Anomaly:` bullet; the potential-leak bullet (now "small", with
    the numbers above); decision 1's title and text; a new decision 2; the record comment; issue 2.
- **Finding 6, corrected counts.** The verifier's 37 coded hours and 19,575 matching hours count the origin side only.
  - Origin and destination together: 39 coded JFK hours in 2016-2018, all without a Meteostat value.
  - All 21,398 other hours where Meteostat has a value match exactly.
  - At 1,780 further hours the release has a value (1,338 of them 0.0) where Meteostat today has none.
  - The both-sides counts are in decision 4's text and the precipitation bullet.
- **Finding 7, frame unchanged.** I built the container from the verifier's copy of the pre-fix definition (md5
  `97bf4c90…`, all 34 columns read) and from the new one (21 columns).
  - Frame hash (`encode_dataset_v2`) `687341c4a6424e146578d9ac0b873d19` for both; `assert_frame_equal` exact; splits equal.
  - The checksum changed only through the metadata text: `v2:4a7eff43…` became `v2:df87326a…`.
  - Peak RSS fell from 47 to 35 GB.

### alfa_battle_2_0_task_1
**Outcome:** not added (data cannot be obtained)
**Record judgment:** do not add: the data cannot be obtained from any source I could find (criterion: data unobtainable).
- The task-1 files were hosted only on Boosters: `https://boosters.pro/api/ch/files/pub/alfabattle2_abattle_clickstream.zip`, `.../alfabattle2_abattle_train_target.csv`, `.../alfabattle2_prediction_session_timestamp.csv`, `.../alfabattle2_abattle_sample_prediction.csv` (names from pytorch-lifestream/ptls-experiments, `scenario_alpha_battle/bin/get-data1.sh`). On 2026-10-06 each returns HTTP 302 with `Location: 404`; the task-2 files on the same host do the same. The Wayback Machine has no snapshot of them (`archive.org/wayback/available` empty; the CDX index for `boosters.pro/api/ch/files/pub/*` holds only 404 redirects from March 2025).
- Kaggle (`kaggle datasets list -s` for alfabattle, "alfa battle", alfabattle2, alfabattle1, abattle, clickstream): the five AlfaBattle uploads (mrmorj/alfabattle-20, sokolovaleks/alfabattle2-sandbox, sokolovaleks/alfabattle2-sandbox-preproc-for-gru, agorinenko/dl-fintech-card-transactions, sokolovaleks/models-booster-alfabattle2-sandbox) hold only the task-2 card transactions. The record's Kaggle link (mrmorj/alfabattle-20) is the task-2 data.
- Hugging Face: no copy (pytorch-lifestream hosts `alfa-scoring-trx`, the task-2 data). GitHub code search for the file names: the four repositories that name them (Aindstorm/alfabattle2_1stproblem, dremovd/alfabattle-2, Samarov/parquet_to_hdf5, ptls-experiments) read a local copy or the dead Boosters URL; Aindstorm read it from a Kaggle input `alfabattle1` that is not public.
**Data:** none downloaded. From the solution notebooks: `alfabattle2_abattle_train_target.csv` has 5,065,350 sessions x 4 columns (client_pin, session_id, timestamp, multi_class_target; dremovd/alfabattle-2 `Final.ipynb`), the test file 79,268 clients with the timestamp of their next session; the clickstream has about a billion events (Samarov/parquet_to_hdf5 README), fields timestamp, application_id, client, session_id, event_type, event_category, event_name, event_label, device_screen_name, timezone, device_is_webview, page_urlhost, page_urlpath_full, net_connection_type, net_connection_tech (v010ch/AlfaBattle20_task1). Licence: not stated for task 1.
**Definition:** none (no folder created).
**Checks:** none.
**Probes:** none.
**Verification:** upheld by the verifier (Boosters API still lists the four files, all and the sandbox copies 302 -> 404; no Wayback capture; Kaggle, HF, GitHub and the 2022 ODS.ai competition hold only task-2 data). Record comment updated with the ODS.ai and sandbox points.
**Issues for Lennart:**
1. Data unobtainable. Question: can the files be obtained elsewhere? Evidence above. Implemented: nothing; a record comment is proposed. Alternative: ask Alfa-Bank (Evgeny Smirnov, github.com/smirnovevgeny, wrote the competition's Habr article) or the Top-6 author (Aindstorm) for the files; with the files, a scaffold can follow.
2. Scope, if the data turns up. The task is to predict the target action of a client's next app session (10 classes: card2card_transfer, card_recharge, chat, credit_info, invest, main_screen, mobile_recharge, own_transfer, phone_money_transfer, statement; macro F1; 7th place private 0.421, Dro1000/AlfaBattle_task1) from the client's earlier sessions and click events. Its use is to show the predicted action at app launch ("Предугадывание цели, с которой клиент открыл приложение", v010ch README quoting the task page), close to a next-action recommendation. Unlike task 2 the organizers published no tabular baseline I could find; the winners used ALBERT and RNNs (organizer's LinkedIn summary "Финал AlfaBattle 2.0"). A tabular version would be our own featurisation of the session sequence (dremovd's pipeline builds 146 history features per client and session). Implemented: nothing. Alternative: a grouped (by client) or temporal next-session task with history features, only if the curator accepts the featurisation as ours.
3. Record metadata: the record lists the task-2 Kaggle dataset as its source link, `problem_type: TBD` (it is multiclass) and the tags `Larger IID Data` and `Non-IID (Grouped)`; the source's test is the next session of known clients, i.e. temporal per client.

   **Resolved (Lennart, 2026-10-12):** `No` stands (data unobtainable). The record now has `problem_type` Multiclass Classification, `required_split` and tag Temporal, and no longer links the task-2 Kaggle dataset or tags `Larger IID Data`.

### alfa_battle_2_0_task_2
**Outcome:** added and checked (revised after verification, 2026-10-07)

**Changed on 2026-10-13 (Lennart's review):** the features of the top solutions replace the organizers' baseline (issue 2); the Definition, Checks and Probes below describe the definition of 2026-10-07.
**Record judgment:** valid with concerns: the tabular version is an aggregation of event sequences; the time axis is reconstructed; repeat clients are linked from the data only.
- Source: AlfaBattle 2.0, task 2, run by Alfa-Bank on Boosters.pro (Boosters timetable: "12 декабря 2020 - 18 января 2021 — чемпионат; 29 января 2021 — официальный финал"). Boosters task text: "оценить вероятность того, что клиент выйдет в дефолт, основываясь на истории потребительского поведения по карточным транзакциям"; metric ROC AUC. Habr (habr.com/ru/companies/alfa/articles/551130, "Описание данных"): 1.5M issued products, one year of card transactions each, train "выдачи за период в N дней", test "за последующий период в K дней".
- Scope: credit scoring at issue, binary, temporal: in scope. Tabular models are competitive: organizers' boosting baseline on aggregates 0.737 public AUC, their RNN baselines 0.750 and 0.760 (smirnovevgeny/AlfaBattle2.0 README); 9th place 0.776 private with LightGBM on aggregates, 0.781 blended with an RNN (aizakharov94/AlfaBattle_task2). Criterion 4A holds.
- Unique: no other record or working-copy folder uses this data. `rosbank1` (this run) is a different Boosters competition (Rosbank, 2018).
**Data:** Alfa-Bank's own re-upload for its 2022 ODS.ai competition (ods.ai/competitions/dl-fintech-card-transactions; storage.yandexcloud.net, no login; archive timestamps 21-22 Nov 2020): `train_target.csv` (963,811 x 3) and 50 parquet files `train_transactions_contest/part_*.parquet` (4,242,459,450 bytes, 270,450,065 transactions x 20 columns). All 51 files are byte-identical (sha256) to the Kaggle mirror mrmorj/alfabattle-20, now the fallback. Licence (noted only): Alfa Battle 2.0 Rules Sec. 3.10 ("Участники обязуются не передавать, не дублировать, не публиковать, не распространять ... данные") and 5.6 forbid passing on the data; Habr 2021 allows use "в научных публикациях, дипломных и курсовых работах"; Kaggle's CC0-1.0 is the uploader's label.
**Definition:** `datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2/`. Prediction point: a credit product is issued; known are its type and the client's card transactions of the preceding 359 days. Target `default` (Yes/No; Boosters: "1 - факт ухода в дефолт", no horizon stated; Kaggle card: within a year), 2.76% positive, roc_auc. Regime: temporal on `issue_month` (0-23), `_make_splits` = `TemporalSplits(window=2, unit="unique", n_windows=3)` minus, on each training side, the products of clients with a product in the test window; horizon 2 months. Test months 22-23 / 20-21 / 18-19: 120,428 / 107,844 / 121,390 rows; train 804,162 / 702,678 / 581,221 rows (39,221 / 32,861 / 32,928 removed). 963,811 rows x 127 features (organizers' baseline aggregates of mcc_category, day_of_week, operation_type; amount, hour_diff and days_before statistics; `product`; `issue_month`). Raw preparation: aggregates, two-pass issue months, issue-day calendar, client links (5 min, 8.3 GB peak).
**Checks:** `dataset check`: 0 errors, 0 warnings, 3 infos, 1 accepted (checksum `v2:0c6b4a384489844d...`). Accepted: `splits_rows_unused` (219 products of months 0-17 whose clients have a product in each of the three test windows; verified: 219 of 219). Infos: `dataset_duplicates_skipped`, `dataset_pure_feature_value_skipped` (size budget; clean when forced on 2026-10-06, the frame changed since only in `issue_month` of 292 rows and the row order), `meta_time_horizon_unit` (correct: `issue_month` counts calendar months). pandas 3.0.6 gives the same checksum, and `_prepare_raw_files` rerun under pandas 3.0.6 writes identical files (features with client keys, calendar). pytest `-k alfa_battle_2_0_task_2`: 1 passed, 1 skipped. ruff clean, no `TODO`.
**Probes:** rerun 2026-10-07 on the shipped (filtered) windows, 2 threads, 50k rows a side.
- `task_probes.py`: LightGBM ROC AUC 0.724 (log loss 0.133 vs 0.141 dummy and drift), linear 0.705, random forest 0.677, best single feature 0.594 (`mean_mcc_category_1` 2x, `mean_mcc_category_7` 1x); LightGBM beats the dummy in 3 of 3 windows (SE 0.010). Flags: none.
- `leak_probes.py`: all features 0.711, depth-2/3 tree 0.616/0.631, strongest single feature 0.601, missing indicators at most 0.559, drop-one at most -0.005, 0.0% exact copies, 1-NN agreement 0.953 (closest tenth) / 0.946 (all) vs chance 0.946, NN distance alone 0.504. Nothing to answer.
- `generated_probes.py`: 0 rule leaves; no flags. `hidden_groups.py` / `group_probes.py`: not applicable (temporal task).
- Client filter (own run, untuned LightGBM, 400 trees, newest window): AUC 0.7774 with all earlier products, 0.7729 shipped, 0.7775 with as many random products of months 12-21 removed; the 502 test products of a client whose earlier product defaulted (95.6% default) drop from the 84th to the 79th score percentile.
**Verification:**
1. (major, repeat clients) applied, option (a): `client_keys` links products by identical transactions in the 28 days before each issue date (>= 3 shared, >= 80% of the smaller side; 301,657 products in 132,561 clients, 4 clients with two products in one month); `_make_splits` drops the window's clients from each training side; duplicates bullet corrected. Option (b) and the 12-month gap are issue 1 below.
2. (minor, 297 misplaced months) applied: `calendar_months` (second pass, neighbours only, full-transaction calendars) moves 292 products (265 around months 7 and 16), 0 false positives against the verifier's list; the other 5 (`app_id` 0-4) fit month 11's calendar but come first in the published order and stay in month 0 (training rows of every window). The 2 products the verifier found across the 21|22 split edge now sit in month 22 (test), with the other 2 moves into window months (20->21, 22->23).
3. (minor, time axis evidence) applied: Boosters' "пронумерованы так, что более поздним заявкам соответствует более поздняя дата" cited; "one issue date per month"; the gaps 31, 28, 31, 30, ... are now derived in code (`issue_calendar`, agreement 1.0, next best <= 0.859, dominant-code share >= 0.994) and shown in the decisions; the Tuesday argument for Jan 2017 - Dec 2018 noted.
4. (minor, licence) applied: `license` and the record comment note Rules Sec. 3.10 and 5.6, Habr's research permission, the ODS.ai re-hosting and Kaggle's uploader label.
5. (minor, login-free copy) applied, as the primary source: ODS.ai archive (organizer-hosted, Nov 2020 timestamps), all 51 files sha256-identical to Kaggle; raw folder re-laid out to the ODS paths; Kaggle kept as fallback with the renames.
6. (minor, wording) applied: target and amount quotes now from Boosters ("1 - факт ухода в дефолт", "Нормированная сумма транзакции"); the one-year horizon attributed to the Kaggle card; bibtex note 12 Dec 2020 - 18 Jan 2021, final 29 Jan 2021; "11 of the 12 codes recur".
**Issues for Lennart:**
1. Repeat clients, keep or drop? Implemented: drop from each training side the products of the test window's clients (a training label not known at the prediction point; hotel_booking_demand rule). Alternative (b): keep them with a "Potential leak, kept on purpose" bullet: they add 0.0045 AUC for untuned LightGBM on the newest window (0.7774 vs 0.7729; random removal 0.7775), the competition had the same structure, and the ieee_fraud_detection precedent kept same-entity label history (but there a later transaction is labelled fraud because of an earlier reported chargeback, so the earlier label is known; here the earlier product's default most likely comes after the new issue). Alternative (c): a 12-month label-maturity gap, which also removes the general unmatured-label optimism, leaves 13.5-26.7% of the rows for training (below the 50% floor).
2. Which aggregates make the tabular version? Implemented: the organizers' boosting baseline (127 features). Alternative: counts and mean amounts of all code columns except `weekofyear` (1,176 columns): 0.733 vs 0.720 AUC on every fifth partition (198,387 products, train months 0-17, test 18-23).
3. Window length and gap. Implemented: 3 windows of 2 months, no gap (oldest train side 581,221 rows, 60% after the filter). Alternatives: `gap=1` like the competition's unreleased month, or 3 one-month windows (months 21-23).
4. Two deviations from the baseline code: `amnt` 0.0 and `hour_diff` -1 (documented codes) set to missing before aggregating, a mean over no known amount missing instead of 0.0, `mean_operation_type_20` dropped. Alternative: copy the baseline exactly.
5. Record metadata to align: `domain` (business & marketing in the record, finance here); the tag `Non-IID (Grouped)` (clients now exist only as a split filter, not as the regime); `required_split: ?` is temporal; source link: the ODS.ai copy.

   **Resolved (Lennart, 2026-10-13):** the features the top solutions share instead of the organizers' baseline: 513 aggregates over restored rubles (`exp(amnt * 17.8209) - 1`; 98.8% whole rubles): amount, gap and recency statistics; count share, amount share and mean amount per value of ten coded columns and the 30 most frequent `mcc` and `card_type` codes; distinct values, mode and last values; money in against out, salary-like inflows and twelve 30-day blocks; daily activity; a balance proxy; the last 30 and 90 days. Label-based encodings, embeddings and sequence-model scores stay out. Untuned LightGBM on the shipped windows: 0.787 / 0.771 / 0.772 against 0.774 / 0.757 / 0.763 with the 127. Sources (from the record): 1st place slides (boosting 0.774 single, 0.780 six models, 0.785 with the organizers' RNN), 4th private place slides, 9th place code. The notes' earlier "top teams 0.776 with aggregates alone" was 9th place; corrected.

   **Resolved (Lennart, 2026-10-13):** `domain` finance, the tag `Non-IID (Grouped)` removed, the ODS.ai page added to the source links; `required_split` was already temporal.



### alvin_smart_money_management_classification_challenge

**Outcome:** added and checked, with private-person payees masked (`datasets/_dev/tabarena-v0pt2/alvin_smart_money_management_classification_challenge/`). Retired as `Too Small` on 2026-10-12 (issue 2); the folder is removed and stays in git history at 86272ac.

**Record judgment:** valid with concerns.
- The source is clear: a Zindi competition by Alvin, a Kenyan budgeting app (22 June to 24 July 2022, 510 participants, metric log loss; Zindi API `api.zindi.world/v1/competitions/alvin-smart-money-management-classification-challenge`).
- No duplicate: no other record and no working-copy folder holds this data. `credrails_banking_transaction_categoriser_challenge` is different data.
- Concerns:
  - the size for a temporal task (issue 2), now the deciding question;
  - personal data, now masked (issue 1).

**Data:**
- Zindi needs a login. The GitHub repository The-Fantastics/Alvin-Smart-Money-Management-Classification-Challenge-Data (commit 65a25f5, 2022-07-01, during the competition) holds the five competition files with the exact byte sizes the Zindi API lists.
- Two other copies are byte-identical: GitHub emms204/Alvin-Smart-Money-Management-Classification-Challenge, and Kaggle harshbansal27/alvin-smart-money-management (versions 1 and 2).
- The definition reads only Train.csv (373 rows x 12 columns, sha256 12b4293e…0b13).
  - Test.csv (558 rows) has no labels.
  - extra_data.csv (10,000 rows) has an empty category and categorisation time in every row (discussion 12475 also calls it unlabelled).
- The warehouse folder holds Train.csv and the codebook, downloaded from pinned raw URLs; a fresh download gives the same sha256.
- Licence: the Zindi Rules page forbids redistribution, "including uploading the data to any public site such as Kaggle or GitHub" (noted only).
- I deleted the scratch copies of Test.csv, extra_data.csv and my early output files, because they show payee names.

**Definition:**
- Task: multiclass, target `MERCHANT_CATEGORIZED_AS`, log loss (the competition's metric).
- Prediction point: a purchase arrives from its M-PESA SMS receipt and the app proposes a category. Known then: payee name, amount, purchase time, the send-money flag, and the user's id and profile.
- Splits: temporal on `PURCHASED_AT`, with a custom `_make_splits`.
  - 3 windows of 21 days, 5 April to 6 June 2022, newest first; train/test 283/36, 264/27, 182/41.
  - A purchase trains only if its category was recorded (`MERCHANT_CATEGORIZED_AT`) before the cutoff. The column is dropped after the split.
- 350 rows x 9 features.
- Cleaning:
  - deduplication: kept the earliest record of 6 purchases recorded twice, and dropped both records of 1 purchase recorded with two categories;
  - dropped 4 categories with fewer than 10 rows, leaving 9 of the 13;
  - dropped Transaction_ID;
  - **new: payees who are private persons are masked as "private person"** (issue 1).
- `_decisions` tables: the label filter per window, the batch writes, the masked payees (counts only), and the class counts.
- Domain is `finance`; the record says business & marketing (issue 6).

**Checks:**
- `dataset check`: 0 errors. Two warnings are accepted with reasons:
  - `splits_rows_unused`: 18 purchases categorised on 31 May or 1 June 2022, after the newest cutoff;
  - `splits_test_class_missing`: each window lacks one class, and every train side holds all 9.
- pandas 2.3.3 and 3.0.6 give the same checksum, `v2:1ae3a01076bd219c58c7b9624fc779486eccee3f47f59ec06b15c9ee9eb6b98f`.
- `pytest tests/test_v2_datasets.py -k alvin` with data checks on: 2 passed.
- ruff is clean, no TODO is left, and `dataset list` shows the folder as checked.
- A scan of README.md, dataset.py and explore.ipynb for the 91 person names of Train.csv, and for every word of 3+ letters in those names, finds none.

**Probes (shipped, masked data):**
- `task_probes.py`: no flags. Dummy 2.044, linear 1.829, random forest 1.581 (skill +0.227, better on 3 of 3 windows, standard error 0.044), untuned LightGBM 3.315 (it overfits).
- `generated_probes.py`: no flags (0 rule leaves).
- The shared `leak_probes.py` gives NaN, the known bug: every window lacks one class. Its copy check finds that 19% of the newest window's test rows repeat a train row on the 7 tabular columns. These are a user's recurring payments of one amount, to other payees or at other times; it is 15% to 37% across the windows.
- My copy (`b2_leak_probes.py`, macro AUC over the classes present, name as TF-IDF):
  - all columns: log loss 1.483 (macro AUC 0.792);
  - shipped name alone: 1.691;
  - tabular columns alone: 1.818;
  - class shares: 2.044;
  - best single tabular column: AUC 0.609;
  - a depth-3 tree on the tabular columns: AUC 0.646;
  - no exact copy of a test row in train on all columns;
  - dropping USER_ID costs 0.135; dropping any other column at most 0.04.

**Issues for Lennart:**
1. **Personal data: now masked; `Ethical Issue` stays the alternative.**
   - What the data holds: 89 of the 207 shipped payee names (43%) are private persons, in 142 of 350 rows. Of them, 75 are among the 93 send-money names and 14 are unflagged; one is a medical fund named after a person, and one name held a phone number. 21 of the 25 users paid a person.
   - The mask, in `_clean`:
     - a payee is a business if its name holds one of 63 business words (`BUSINESS_WORDS`: legal forms, banks, operators, shops, restaurants, fuel stations, churches) or is one of 17 listed businesses (`BUSINESS_PAYEES`);
     - every other payee becomes "private person";
     - the rule matches my reading of all 218 names in Train.csv: 91 persons and 127 businesses.
   - Rows changed: 142 of 350.
   - The send-money flag alone would mark 42 business rows and miss 21 person rows, so it is not used as the rule.
   - The mask costs no signal on the shipped windows: logistic regression 1.483 masked vs 1.478 with the names; random forest 1.457 vs 1.529.
   - Alternative: `Ethical Issue` → `TBD -> 2nd Tier`, as for employee_salaries, employee_remuneration_and_expenses_earning_over_75000 and wineenthusiasts. The wineenthusiasts record notes its PII "could likely be fixed", which is what the mask does here.
   - The raw Train.csv in the local warehouse still holds the names, as it must for the rebuild.
2. **`Too Small`: Lennart's call. I recommend `TBD -> 2nd Tier`.**
   - Window sizes: the windows hold 36, 27 and 41 test purchases from 10, 5 and 12 users. One user makes 28%, 52% and 41% of a window.
   - Small classes: over all three windows, Shopping has 2 test rows, Transport & Fuel 3, Emergency fund 5 and Going out 5.
   - Loss concentration: in window 1 (26 Apr to 16 May), the 8 rows of classes with at most 2 rows there give:
     - 51% to 54% of the loss of the two probe models on the shipped data;
     - 43% to 48% with the real names;
     - 36% for the class shares.
   - No other design meets the guidelines:
     - 3 windows is the minimum;
     - 4-week windows leave the oldest train side 34% of the rows;
     - the drift rules out an IID fallback: Bills & Fees is 15% of the purchases before the windows and 39% of the test purchases.
   - `few_minority` checked only binary tasks then, so no probe flagged this.
   - The signal is real: random forest 1.581 against 2.044, on 3 of 3 windows.
   - Revisit if Zindi or Alvin release Test.csv's labels: it holds 64, 49 and 73 more verified purchases in the three windows, so about 100, 76 and 114 test rows (the verifier's 102/78/114 adds the raw Train.csv counts, before deduplication and the rare-class drop).

   **Resolved (Lennart, 2026-10-12):** `No` with `Too Small`, as parkinsons_biomedical_voice_measurements: the 8 rows of the rarest classes decide half of window 1's loss. The multiclass `few_minority` flag now catches it; the folder is removed, and the record notes the revisit if Test.csv's labels come out.

3. **Scope: the name works as a lookup of payees seen before.**
   - With the real names, the name as an exact id scores 1.609 against 1.571 for TF-IDF (logistic regression on the name alone).
   - Test purchases at a payee not seen in train are 12, 16 and 28 rows (33%, 59%, 68% of the windows). This is the source's "future merchants" use. On these rows:
     - logistic regression stays at the class shares (2.067 vs 2.088);
     - a random forest gains 0.16 (1.924; 1.947 to 1.974 over three seeds in a variant), mostly from the user and payment columns (1.961 without the name). With the masked names it gains 0.27 (1.815).
   - This corrects one verifier statement ("no model beats the class shares"): it holds for logistic regression only. A bullet in `curation_comments` records it.
4. **Label filter: kept.**
   - The codebook defines the column per merchant: "the time the merchant was categorized by the customer".
   - Without the filter, the shipped windows score 1.316 instead of 1.483 (logistic regression) and 1.353 instead of 1.457 (random forest); with the real names, 1.238 instead of 1.478.
   - The gain comes from labels written after the cutoff, in the same batches as the test labels (96% to 100% of the left-out rows).
5. **Comment wording, fixed as the verifier proposed:**
   - the codebook and the Data page explain a categorisation time before the purchase; only the multi-user batch writes are undocumented;
   - discussion 12519 is cited for merchants with several categories, and 12608 alone for the failed label copying;
   - the user statement now reads: 8 users appear only before the windows, 5 only inside them, 12 in both;
   - older purchases: 45 of the 350 shipped purchases (13%) were made before August 2021, back to December 2018. The verifier counted 39 with a cutoff it did not state; mine is August 2021, the month of the first categorisation;
   - discussion 12159 ("Downside of random split") is cited for the temporal split.
6. **Record, for the orchestrator:**
   - the record's `domain` should be finance, as in the definition and the other transaction datasets;
   - `v2_path` is unset (`sync-notebooks`);
   - the record comment is in `alvin_smart_money_management_classification_challenge.record_comment.md`.
7. **Tooling:**
   - `leak_probes.py` gives NaN when a test fold lacks a class, and skips string columns;
   - `few_minority` covers binary tasks only; a multiclass window with 0 to 2 rows of a class passes unflagged.

#### Verification (fix round, 2026-10-07)

- **Checked myself and confirmed:**
  - 89 of 207 names (75 flagged + 14 unflagged), 142 of 350 rows, 21 of 25 users. The flag marks 42 business rows and misses 21 person rows. In the old README, names were in sample rows 2-5 and at rank 3 of the top values;
  - windows 36/27/41 rows from 10/5/12 users; largest user 28%/52%/41%;
  - class totals: Shopping 2, Transport & Fuel 3, Emergency fund 5, Going out 5;
  - users: 8 only before the windows, 5 only inside, 12 both;
  - unseen-payee shares 33%/59%/68%;
  - name as id 1.609 (verifier 1.615) vs TF-IDF 1.571;
  - no-filter score 1.238 vs 1.478 (real names).
- **Differs from the verifier:**
  - on unseen payees a random forest does beat the class shares (issue 3);
  - the window-1 loss share depends on the model: 43% to 54%;
  - the count of old purchases depends on the cutoff: 45 before August 2021.
- **Changed in this round:**
  - the mask in `_clean`, which also covers the one name with a phone number, so the separate phone-number step is gone;
  - a `_decisions` table of masked payees (counts only);
  - new `curation_comments` bullets: the mask with its rule and counts, the scope note, the size note, and the split citing 12159 with the drift;
  - the wording fixes of issue 5;
  - updated probe numbers.
- **Re-run after the change:** `dataset check`, task, generated and leak probes, my leak-probe copy, the pandas-3 checksum, ruff, pytest, and the README name scan (0 names).

### analcatdata_supreme

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/analcatdata_supreme/`). After verification the regime
is IID: the temporal split the record asks for cannot be built validly (issue 1).

**Record judgment:** valid with concerns.
- Provenance traced. The file is `supreme.csv` from the data page of Simonoff, *Analyzing Categorical Data*
  (Springer 2003). The data was collected by Zorn (1998), *Sociological Methods & Research* 26(3):368-400,
  DOI 10.1177/0049124198026003004. Zorn's abstract (IDEAS/RePEc page): "using data on congressional responses to
  Supreme Court decisions from 1979 to 1988".
- Unique. No working-copy folder and no other record holds it (grep for supreme, OpenML 504/728/44040, Zorn,
  ANACALT). OpenML 504 (v1), 728 (v2) and 44040 (v3, Grinsztajn et al. 2022) are versions of the same table. No other
  record of the run is related.
- Concern: the record's temporal split cannot be built validly, and the IID signal is small (issue 1).
- Concern: the file's `Log exposure` leaks the outcome (fixed, issue 3).

**Data:**
- Source: `https://pages.stern.nyu.edu/~jsimonof/AnalCatData/Data/Comma_separated/supreme.csv` (sha256 `61c847ce…`).
  It is byte-identical to the copy in StatLib's `https://lib.stat.cmu.edu/datasets/analcatdata.zip` (file dated
  2002-01-17). OpenML 504 holds the same rows in the same order.
- Shape: 4,052 rows x 8 columns, no missing values, every value written with two decimals.
- Licence: "These data sets may be used freely for scientific, educational and/or noncommercial purposes, provided
  suitable acknowledgment is given (by citing the above-named reference)". This is the NOTICE in the README of the
  StatLib analcatdata submission (2003-07-03, also quoted on OpenML 504). OpenML's licence field says "Public".
- Warehouse: `local-data-warehouse/analcatdata_supreme/supreme.csv` (178 KB).

**Definition:**
- Prediction point: for a decision, the number of congressional actions it draws in the 1979-1988 window. Known when
  the decision is handed down (for a pre-1979 decision, in January 1979): the five 0/1 attributes, the year, and the
  years the decision has in the window. All labels become known together, at the end of 1988.
- Target: `log1p_actions_taken` (regression, RMSE). 95.8% of the decisions have no action; the counts run 0-11.
- Regime: IID, the default 3x3 splits (seed 4267): train 2,701-2,702 rows, test 1,350-1,351, 47-72 decisions with an
  action per test fold. Tag `ForcedIIDFromTemporal`. The `splits_comment` says why the split is not temporal.
- Shape: 4,052 rows x 7 features (five 0/1 attributes, the year, `log_potential_exposure`).
- Cleaning:
  - snake_case names; the indicators and the year cast to int;
  - the file's `Log exposure` replaced by the exposure the year implies, log(min(10, 1989 - year)) (leak);
  - the target log1p-transformed;
  - all rows kept: 86.0% are exact copies of another row, target included, which is natural with 446 distinct
    feature vectors for 4,052 decisions.
- Two `_decisions` tables: the file's exposure against the year, and the two-year periods a temporal split would
  test on (their exposures, the lowest exposure of all earlier decisions, the share with an action).
- pandas 2.3.3 and 3.0.6 give the same checksum (`v2:82d9cff5…`).

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 infos.
- Accepted warnings:
  - `dataset_duplicate_rows`: each row is a different decision.
  - `dataset_conflicting_duplicate_rows`: decisions with the same attributes draw different responses.
  - `task_target_low_cardinality`: a count from 0 to 11, which the source models as a count.
  - `task_target_value_dominant`: a zero-inflated count. The zeros are real outcomes and are what Zorn studies.
- `pytest tests/test_v2_datasets.py -k analcatdata_supreme` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed. ruff
  clean; `load_definition` imports.

**Probes** (IID outputs in `probes_iid/`; the earlier temporal ones in `probes/`; experiments in `experiments/`):
- Leak probes (untuned LightGBM R² on 3 folds):
  - all features -0.040; depth-2 / depth-3 tree +0.012 / +0.015; each single feature at most +0.008.
  - No missing values.
  - 96.4% of test rows have an exact feature copy in train. These are the natural repeats (446 vectors), and the
    copies do not share the label: 1-NN R² -0.35.
  - Nothing points to a leak in the shipped frame.
- The exposure leak, under IID (3x3 random folds, the same folds for both columns): with the file's `Log exposure`,
  untuned LightGBM scores skill +0.124 against -0.019 with ours, and LightGBM with 4 leaves +0.063 against +0.020
  (the file's column is better on 9 of 9 folds each). All 31 decisions whose file exposure is 2+ years shorter than
  their year allows, or longer, have an action (base rate 4.2%).
- Task probes: flag `no_signal`. Linear skill +0.016 ± 0.002 (skill is 1 - MSE / MSE of the train mean; ± is the
  standard error over the folds), above the dummy on 9/9 folds but under the 0.02 floor; random forest -0.028,
  LightGBM -0.024 (untuned, overfit).
  - Answered with regularised models on the shipped folds (no tuned results exist for a new dataset): LightGBM with
    4 leaves +0.021 ± 0.003 (9/9), ridge (alpha 100) +0.016 ± 0.002 (9/9), Zorn's hurdle form +0.022 ± 0.003
    (9/9), TabPFN (package 9.0.0, 4 estimators, CPU) +0.008 ± 0.002 (9/9); default CatBoost -0.036 (0/9, overfit).
  - "Any action" ROC AUC on the shipped folds: hurdle 0.702, logistic 0.700, LightGBM (4 leaves) 0.702, CatBoost
    0.707, TabPFN 0.706, all 9/9 above 0.5. The year alone scores 0.679 (each year's training share as the score),
    the five attributes alone 0.559.
  - A small but real signal: kept under rule 2 (forest_fires), written into `curation_comments`.
- Generated probe: no flags (0.0% exact fits, the same as for a shuffled target).
- Hidden-group probe (IID): no hits. The one candidate, `year_of_decision`, has a gap of +0.005 (random -0.031,
  grouped -0.035). The year is a feature known for every decision, not an entity. No action.

**Issues for Lennart:**
1. **Regime, and keep or retire** (Lennart's call; the record asks for a temporal split).
   - Implemented: IID 3x3 over all decisions, as the book models them ("We will attempt to stochastically model such
     action using the 4052 Supreme Court decisions ...", quoted in the record).
   - Why not temporal:
     - Every label counts actions over the same window, 1979-1988, and is known only at its end. No temporal window
       can train on labels that existed at its test decisions' prediction point; for 1975-76 and 1977-78 no label
       existed at all.
     - The exposure falls from 10 years (decisions up to 1979) to 1 (1988). In the four two-year windows from
       1981-82 on, every test decision's exposure is below every training decision's; in 1979-80 that holds for the
       1980 half (52%). The windows' mean moves by construction.
   - The temporal numbers (7 two-year windows, 1975-76 to 1987-88; the verifier's runs, of which I reproduced the
     count models, the constants and the attribute ranking exactly; TabPFN is the verifier's run):
     - The test mean as a constant scores skill +0.033 (7/7), above every model.
     - Count models in Zorn's form with the log exposure as an offset: Poisson +0.013 (6/7), hurdle +0.021 ± 0.011
       (6/7). These wins come only from the level: the offset model centred on the train mean wins 0 of 7 (-0.012).
     - TabPFN +0.006 ± 0.009 (3/7). Untuned LightGBM, random forest, ridge and CatBoost -0.058 to -0.118.
     - The five attributes alone rank the decisions with an action at pooled AUC 0.551 (95% CI 0.501-0.597).
   - Alternatives:
     - (b) `No`, with the label-window design as the reason: no deployable (temporal) version exists, and the IID
       signal is mostly the cohort the window favours. By task-probe rule 2 the small signal alone is no reason.
     - (c) The record's temporal split, with the numbers above. The probes flag `no_signal`, `drift_baseline` and
       `unstable` there.
   - My view: the IID version is valid by the source's design, and its signal is small but holds on 9/9 folds for
     every regularised model, so by rule 2 it stays. I withdraw the earlier `No` recommendation: it rested on the
     temporal no-signal result, which the label window explains.

   **Resolved (Lennart, 2026-10-14):** retired, `No` with `No Good Target / Scientific Discovery`. The label counts responses in one calendar window shared by all decisions, not in a fixed time after each decision, so the task stands for no forecast anyone makes, only a look back at which rulings drew responses. Folder removed (in git history at 86272ac); the rule is in criterion 3 of the curation guidelines.

2. **Target scale.**
   - Implemented: regression on log1p(count). The record says "Correct target seems to be regression number of
     actions taken. We could overrule to clf as well".
   - Alternatives:
     - "any action" (the first stage of Zorn's hurdle model): ROC AUC 0.70-0.71 on the IID folds; the task probes
       raise no flags on it (linear 0.696 on 3x3 folds);
     - the raw count with RMSE: the 29 decisions with 5-11 actions make up 63% of the sum of squares.
3. **The exposure fix.**
   - Implemented: the year-implied exposure for every row, named `log_potential_exposure`.
   - Open: 76 decisions sit one year below their year's exposure (6-12 per year, 1979-1987). 10 of them (13.2%) have
     an action, against 6.2% of the decisions of those years whose exposure matches their year (67 of 1,088). The
     verifier reads them as a mix: decisions handed down late in their year (0 of 9 in 1979, 0 of 12 in 1985, 0 of
     11 in 1987 have an action) and probable overturns (4 of 6 in 1983).
   - Alternatives: keep the file's value for those 76 rows (part of the leak stays), or drop the column. After the
     fix it is a function of the year, so a model only loses the log scale.
4. **Paywalled sources.**
   - Zorn (1998) was not read (closed access; SAGE returns 403). The book's supreme example (likely Sec. 5.4.2
     "Zero-Inflated Count Regression", pp. 162ff, from the book's table of contents) was not read either; the
     record's quotes are used.
   - Open questions:
     - What counts as an "action"?
     - How are `Liberal` and `Lower court disagreement` coded?
     - Was the exposure an offset or a covariate?
     - Do the counts end in 1988? The book says "96th through 101st Congress, 1979-1988" (the 101st sat in
       1989-90), and two 1988 decisions carry 2 years of exposure.
   - Hettinger & Zorn (2005, *Legislative Studies Quarterly* 30(1):5-28) may describe the same data.
   - Query to find the paper: Google `"An Analytic and Empirical Examination of Zero-Inflated and Hurdle Poisson
     Specifications" pdf`; the PDF can go into `../tmp_folder/`.
5. **Framework bug (not patched).**
   - `AbstractCuratedDataset.make_splits` stores `splits_comment` as written
     (`src/data_foundry/v2/dataset.py:677`, `plan.comment = self.splits_comment`), although the class docstring
     says text attributes are dedented.
   - Effect: a multi-line comment keeps its code indentation in the container, and the README renders its lines 2+
     as a code block. Seen in lending_club's README; the same goes for every definition with a multi-line
     `splits_comment` (consumer_complaints_1m, kickstarter, emscad, coffee_rating_prediction, ...).
   - Fix: `plan.comment = clean_text(self.splits_comment)`. It changes those containers' checksums, so they need a
     rebuild.
   - This definition writes the comment as one string and is not affected.
6. **Licence.** Free for scientific, educational and noncommercial use with citation (StatLib README NOTICE).
   Noted only, not a verdict reason.
7. **Record fields** (for the orchestrator, after Lennart decides).
   - `required_split: Temporal (NON-IID)` and the tag `Non-IID (Temporal)` no longer match the definition (IID,
     `ForcedIIDFromTemporal`).
   - `problem_type: TBD` becomes `regression`.
   - `source_links` list only OpenML 504 and 728, whose default targets are wrong (`Log_exposure`, and 728's
     binarised version of it, which equals "decided in 1982 or later" for 99.3% of the rows); 44040 is a third copy
     with the same target. The original is Simonoff's data page.
   - `v2_path` is unset (`sync-notebooks` fills it).
   - Proposed record comment: `analcatdata_supreme.record_comment.md`.

**Verification** (independent verifier, verdict "needs changes"; each finding):
1. major, the temporal regime: **applied.** IID implemented (default 3x3 splits, tag `ForcedIIDFromTemporal`, a
   `splits_comment` and a `_decisions` table giving the reason). `No` and the record's temporal split are the
   alternatives in issue 1, with the numbers. One correction to the finding: every test exposure lies below every
   training exposure in 4 windows (1981-82 to 1987-88), not 5. In 1979-80 it holds for the 1980 half (52%); written
   so. The verifier's censoring concern (rubric item 9) is handled as in the source: the count is defined over the
   window, and `log_potential_exposure` is a feature in every fold. On the shipped IID folds, TabPFN (package 9.0.0)
   scores +0.008 ± 0.002 (9/9), in line with the verifier's +0.009 on random folds.
2. minor, "no model beats the train mean": **applied.** The temporal numbers now name the level-only wins of the
   offset count models and TabPFN's +0.006 ± 0.009 (3/7). I reproduced `zorn_models.out`, `constant_artifact.out`
   and `attr_ranking.out` exactly (`experiments/reproduce/`). My earlier Poisson test was the wrong one (exposure as
   a scaled covariate, scored with log1p(E[y])); dropped.
3. minor, the `splits_comment` refit sentence: **applied.** The comment now describes the IID splits and why a
   temporal split is not valid.
4. minor, two numbers: **applied.** Now "6.2% of the decisions of those years whose exposure matches their year (67
   of 1,088)" (all others: 79 of 1,100, 7.2%), and "3,486 rows (86.0%) are exact copies of another row, target
   included; the feature vectors repeat in 3,606 rows (89.0%)". Both recomputed.
5. minor, OpenML 44040: **applied.** Confirmed with the OpenML API (default target `Log_exposure`, 4,052 rows); added
   to `download_description` and the target bullet. No record lists 44040.
6. minor, the record comment: **applied.** Rewritten around the label-window design, with the IID numbers and `No`
   as the alternative. Record fields are listed in issue 7 for the orchestrator.
7. no change, the leak fix: **agreed.** Added the leak's size under IID (untuned LightGBM +0.124 with the file's
   column against -0.019 with ours, 9/9 folds).
8. cannot verify, Zorn (1998): **kept** as an open point (issue 4).
- Rule on personal data: followed. No email or personal data went into any URL or API request (OpenML, IDEAS,
  StatLib, Simonoff's page, Europe PMC).

### apistox
**Outcome:** added and checked

**Record judgment:** valid with concerns.
- Provenance: Adamczyk, Poziemski and Siedlecki, "ApisTox: a new benchmark dataset for the classification of small molecules toxicity on honey bees", Scientific Data 12:5 (2025), doi 10.1038/s41597-024-04232-w; data on Zenodo (concept DOI 10.5281/zenodo.11062076; v1 11062077 of 2024-04-24, v2 13350981 of 2024-08-20) and GitHub j-adamczyk/ApisTox_dataset. The 1,035 compounds are merged by the authors from US EPA ECOTOX and the Hertfordshire PPDB and BPDB databases.
- Unique: no record or working-copy folder mentions ApisTox, honey bees, pesticides, ECOTOX or PPDB (grep of `curation/records/` and the working copy's `dataset.py` files). The other molecule datasets of the run and the working copy (qsar_oral_toxicity, qsar_bioconcentration, qsar_tid_11, drug_induced_autoimmunity_prediction, ...) are other endpoints.
- In scope: a fixed predictive task (toxic or not at the US EPA threshold) with a temporal split; no forecasting, no leak in the shipped columns. The concerns are the representation of the molecule (issue 1), the noisy time index (issue 2) and the split choice (issue 3).
- The record's `original_source: UCI` is not where the data first appeared: UCI 995 is a catalogue entry without a file (`data_url: None` in the UCI API), pointing to the Zenodo concept DOI.

**Data:** Zenodo record 13350981 (version 2), `dataset_final.csv`, 1,035 rows x 13 columns (name, CID, CAS, SMILES, source, year, toxicity_type, herbicide, fungicide, insecticide, other_agrochemical, label, ppdb_level), md5 61ad9ef27a80987105a4cdb074eb102f (as Zenodo lists it), sha256 de4b160a23601a44ac5ec5b23aae95973acba060135630a6df8f73d128baea9e. The file is byte-identical in Zenodo v1 and on GitHub master (git blob de2773e7). In `local-data-warehouse/apistox/`. Licence: CC BY-NC 4.0 (GitHub README: "Dataset and code are released under CC-BY-NC-4.0 license"; Zenodo v2 metadata); Zenodo v1 states CC BY 4.0 for the identical file. For checks only, the source tables of v2 (ecotox.csv, ppdb.csv, bpdb.csv, ecotox_cleaned_data.csv, excluded_data.csv, the split files) are in `../_scratch_new65/apistox/zenodo_v2/` (2.4 MB) with RDKit features in `features/` (5.7 MB); both can go after verification.

**Definition:** `datasets/_dev/tabarena-v0pt2/apistox/`
- Prediction point: a candidate agrochemical before its acute honey bee test (the authors' use case, Usage Notes: "ML-based filters for new agrochemical candidates"). Known: structure, intended use, year it enters the literature.
- Target `toxic_to_bees` (Yes = LD50 <= 11 µg/bee, the file's `label`): 296 Yes / 739 No; ROC AUC.
- Regime: temporal on `first_publication_year` (the file's `year`), `Temporal(on="first_publication_year", splits=TemporalSplits(window=10, unit="unique", cutoffs=(2014, 2004, 1994, 1984)), horizon=10, horizon_unit="years")`. Every year from 1950 on is present, so ten distinct years are ten calendar years. Windows 2014-2023 / 2004-2013 / 1994-2003 / 1984-1993 hold 54 / 106 / 118 / 173 compounds (12 / 22 / 19 / 33 toxic); train sides 981 / 875 / 757 / 584 (95% / 85% / 73% / 56%). Ten years is the shortest window with 50 compounds at the newest end (2016-2023: 37).
- Frame: 1,035 rows x 6 features: `SMILES` (string), the four agrochemical flags (0/1, missing for the 55 compounds the source marks unknown), `first_publication_year` (int).
- Dropped: `ppdb_level` (the same LD50 cut at 1 and 100 µg; level 0 never toxic, level 2 always), `toxicity_type` (route of the strongest measured toxicity; ECOTOX "Other" 11 of 12 toxic), `source` (database of the label; toxic 36% ECOTOX, 24% PPDB, 19% BPDB; labelling rule differs by database), identifiers `name`, `CID`, `CAS` (CID and CAS also track the year: Spearman 0.66 and 0.78).
- No deduplication needed: SMILES and CAS are unique. Salts and mixtures of one active stay separate rows as in the source (138 compounds share a parent structure with another; 56 parents, 5 with both classes).
- Two `_decisions` tables: the dropped columns' class shares; the windows.
- Container checksum v2:1c967b7f1d793768b671dd66d11439f13cdc794f4006f2b1c8d642b448bbee51, the same under pandas 2.3.3 and 3.0.6.

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info.
- Accepted: `dataset_identifier_column` (SMILES is the structure, the input of the task, unique because the authors removed duplicate structures; as qsar_bioconcentration).
- Info `meta_time_horizon_unit`: the int time column holds calendar years, so the 10-year horizon is right.
- `pytest tests/test_v2_datasets.py -k apistox` passes, also with `DATA_FOUNDRY_V2_DATA_CHECKS=1`. Import check passes. `dataset list` over the working copy exits 0. No TODO left.

**Probes:** (first round in `<scratch>/probes/`, after the fix round in `<scratch>/probes2/`; the numbers below are the fix-round ones)
- Leak (untuned LightGBM, 4 windows): no leak. The script skips string columns, so it saw only the flags and the year. ROC AUC 0.799; depth-2 / depth-3 tree 0.809 / 0.792; best single column `insecticide` 0.785 (0.798 without it); 0.0% exact copies across the split; 1-NN agreement 0.750 closest tenth / 0.685 all / 0.592 chance; label-free distance 0.512. The missing-value indicator of the flags scores 0.569: it marks the 55 unknown-type compounds (53% toxic against 27%), which the definition documents.
- Task (4 of 4 windows, SMILES as word TF-IDF + 16 SVD): flags `unstable` only. Linear 0.798, random forest 0.784, LightGBM 0.763, single feature (`insecticide`, all 4 windows) 0.716; all beat the dummy on 4 of 4 windows; spread 0.070 (paired SE 0.032, so `no_spread` no longer fires); best skill SE 0.117; per-window linear AUC 0.97 / 0.70 / 0.78 / 0.75 (newest first); smallest class 12. Answered as consumer_complaints_1m (above the dummy in every window, the SE is window-to-window variation of a small temporal task): kept. No tuned results exist for a new dataset.
- Generated: no flag (rule leaves 0.0% of the minority).
- Hidden groups / group probes: not run (temporal task). The parent-structure overlap is measured instead: 9 / 20 / 4 / 7 test compounds per window (newest first) have their parent structure on the training side.
- Own checks with the structure, on the shipped frame (RDKit 2026.03.6 for analysis only; `scripts/recheck_with_na_flags.py`): mean ROC AUC over the 4 windows, LightGBM / random forest. Flags + year 0.80 / 0.69; + the TabArena default Qwen embedding 0.79 / 0.83; + SMILES char 2-5-gram TF-IDF (64 SVD) 0.84 / 0.85; + ECFP4 1,024 bits 0.83 / 0.86; + MACCS 0.85 / 0.85. On the raw frame, adding `source` and `toxicity_type` to ECFP4 + flags + year moved LightGBM from 0.833 to 0.840.
- Label consistency: every label equals its source table's (PPDB 511, BPDB 84, ECOTOX 441 rows). PPDB and cleaned ECOTOX disagree for 41 of the 399 compounds in both (ppdb.csv has 860 rows but 859 distinct CAS: DDT twice); the file keeps PPDB's label.

**Issues for Lennart:**
1. **Resolved (2026-10-14): the SMILES becomes RDKit's descriptors and the string is dropped, as in every SMILES dataset.** (Was: MAJOR, Lennart's call: the default pipeline gets almost none of the structure out of the SMILES.)
   - Evidence (measured in the fix round, after the verifier raised it): `tabarena_default` lowercases a string column (`sanitize_text`) and encodes it with Qwen3-Embedding-8B truncated to 32 dimensions, with the n-gram text features off. Scored on the 4 shipped windows (mean ROC AUC, LightGBM / random forest / logistic regression; I re-ran the verifier's embeddings with my own scoring code, `scripts/recheck_embedding.py`, and reproduce its table): the embedding alone 0.58 / 0.59 / 0.54; the embedding with the flags and the year 0.78 / 0.81 / 0.81, which is not above 0.80 / 0.70 / 0.82 for the flags and the year alone. Keeping the case gives 0.80-0.82, and the untruncated 4,096 dimensions 0.66-0.78 (the wide block drowns the five informative columns). Structure-aware encodings do carry signal: ECFP4 bits with the flags and the year reach 0.83 / 0.85, character 2- to 5-grams 0.83 / 0.84, MACCS keys 0.85 / 0.84. The source names the structure as the input ("Predictive algorithms will most likely model the relation between structure of molecules (SMILES column) and either label or ppdb_level column as the target", Usage Notes), and on the authors' own time split ECFP + random forest reaches ROC AUC 0.78 against 0.73 for the best GNN and ChemBERTa (arXiv:2503.24305v4, Table 2). The two precedents for keeping a SMILES string (drug_induced_autoimmunity_prediction, qsar_bioconcentration) ship the source's descriptors next to it; here the SMILES is the only structure.
   - Implemented, option (b): the SMILES stays a string, and `curation_comments` now carries these numbers and says that under the default pipeline a model learns from the agrochemical type and the year, not from the molecule.
   - Alternative (a): compute MACCS keys (166 columns) or ECFP4 bits in `_clean` with a pinned RDKit, keeping the SMILES. That puts RDKit into the `build` extra, a framework change, and follows qsar_tid_11 and qsar_oral_toxicity, which ship fingerprints. The orchestrator ruled a new dependency out for this round.
   - Alternative (c): a benchmark-side SMILES encoder (a fingerprint step, or the character n-grams that reach 0.83-0.84 here), next to the other harness items in `BENCHMARK_CHANGES_TODO.md`. It would also serve melting_point and the two precedents, and would let this definition stay as it is.
   - Answer (2026-10-14, to Lennart's question how to handle SMILES in general): the string holds the structure (as character n-grams alone ROC AUC 0.69-0.77 on the three SMILES datasets), but next to descriptors it adds nothing. Untuned LightGBM, descriptors only / with the SMILES as character n-grams / with a Morgan fingerprint: drug_induced_autoimmunity_prediction 0.835 / 0.810 (worse on 15 of 15 splits) / 0.849; qsar_bioconcentration (macro AUC) 0.735 / 0.723 / 0.743; apistox 0.838 / 0.848 (standard error 0.023 over the windows) / 0.853. Lennart's call: one tool for every SMILES dataset, `data_foundry.v2.rdkit_descriptors` (RDKit's 2D descriptors with the pinned RDKit; apistox's function moved into the package), and the SMILES dropped in all three. No benchmark-side SMILES encoder and no fingerprints (0.01-0.015 for about 1,000 columns). apistox keeps its 199 descriptors without the string; qsar_bioconcentration gains RDKit's 193 (0.735 -> 0.752); drug_induced_autoimmunity_prediction keeps the source's descriptors and one row of each of 9 stereoisomer pairs that became copies (587 drugs). CHANGELOG, 2026-10-14.

2. **The time index is noisy.**
   - Evidence: `year` is the earliest PubChem article for the CID, or the PubChem record's creation date when there is none (`dataset_creation/pubchem.py`, `get_first_publication_date`; the paper does not mention the fallback). 43 of the 160 compounds dated 2004 or later have no PubChem literature today (PUG-View, 2026-10-07; 19 of them dated 2005, the creation year of most of the file's PubChem records). The fallback dates sit in the two newest windows only: 7 of 54 compounds in 2014-2023 and 36 of 106 in 2004-2013, none in the two older windows. Examples: picloram 1965 and its triethylammonium salt 2005; prochloraz 1980 and its manganese complex 2005. 31 compounds carry a CID whose structure differs from their SMILES (mostly PPDB's CIDs); the verifier classified them, and 6 point to unrelated compounds whose year is taken over: silthiofam has siduron's (1971), fthalide metominostrobin's (2000), iprobenfos that of oxpoconazole fumarate (2010). The noise dilutes the newest windows rather than biasing them: the toxic share of the affected compounds (23-33%) is close to the rest (19-20%), and dropping the same-parent and suspect-dated test compounds moves a window's ROC AUC by at most 0.044 (random forest on ECFP4 + flags + year: 2014-2023 0.923 to 0.879, 2004-2013 0.842 to 0.855; the two older windows within 0.01; `scripts/fix_round_checks.py`).
   - Implemented: the source's years, documented in `curation_comments`. A corrected year needs PubChem queries the raw file does not hold.
   - Alternative: drop those compounds through a list shipped next to `dataset.py` (an external, dated PubChem query becomes part of the definition). Not recommended, given the size of the effect.
3. **Window design: 4 ten-year windows (implemented) or 8 variable-length ones? Not IID.**
   - Evidence: the 4 windows meet the guidelines (at least about 50 test rows, enough positives, train at least 50%). The verifier checked an 8-window design cut at year boundaries with at least 50 compounds and 10 toxic each (2014-2023, 2007-2013, 2002-2006, 1997-2001, 1992-1996, 1989-1991, 1984-1988, 1979-1983; 54-83 compounds, train at least 51%): it lowers the standard error of the probes' mean skill from 0.117 / 0.091 / 0.083 to 0.071 / 0.060 / 0.057 (linear / random forest / LightGBM), which would answer the `unstable` flag. It needs variable-length windows, so a `_make_splits` instead of `TemporalSplits`.
   - Implemented: 4 ten-year windows through `TemporalSplits`, the declarative form.
   - Not an alternative: IID. I raised it in the first round; the verifier is right that it does not fit, since the use case is new compounds and the guidelines rule out falling back to IID for a non-stationary sequence. The authors' MaxMin recommendation (one split by ECFP4 diversity) also tests interpolation, not new compounds, and the v2 protocol needs repeated splits. For the record, IID 3 x 3 CV scores about 0.03-0.04 higher (ECFP4 + flags + year LightGBM 0.872 against 0.833).
4. **Task-probe flag `unstable`** (`no_spread` is gone since the flags became missing for the unknown type: spread 0.070 against a paired standard error of 0.032).
   - Evidence and answer: see Probes. Every family beats the dummy in every window, and the flag comes from 4 windows of 54-173 compounds. The newest window is nearly solved by the flags (flags + year: logistic regression 0.985, LightGBM 0.945) because 6 of its 7 insecticides and all 5 of its unknown-type compounds are toxic. Issue 3's 8-window design would lower the standard error.
   - Implemented: kept; re-check with tuned results once the benchmark has run on it.
5. **Training labels measured after a window's cutoff.**
   - Evidence: for the 132 ECOTOX compounds with a dated study, the first bee study comes a median of 21.5 years after the compound's year, and 18-41% of these training compounds per window were first tested in or after the window. PPDB and BPDB values carry no test date, and 309 of 441 ECOTOX compounds come only from EPA's 2020 "Pesticide Ecotoxicity Database: Bee Studies" compilation (ECOTOX reference 184644) without study dates.
   - Implemented: no filter, which this source cannot support. The acute LD50 is a property of the compound, so this is not the delivery-date kind of label leak.
   - Alternative: none from this source.
6. **Target: binary EPA label (implemented) or the 3-level PPDB toxicity?** `ppdb_level` has 177 / 687 / 171 compounds; the authors call it ordinal regression (Usage Notes). It would be a second folder (`apistox_level`, multiclass log loss). I do not recommend it: the binary label is the paper's main task and the record's problem type.
7. **Resolved (2026-10-14): the record follow-ups are done** (`original_source` Other, the reference is the Scientific Data descriptor, the licence history is noted; the SMILES question is answered by issue 1). (Was: Record follow-ups, I did not edit the record:)
   - `original_source` should say `Other` (Zenodo), not UCI: UCI 995 holds no file and points to the Zenodo concept DOI.
   - The reference is now the published descriptor, Scientific Data 12:5 (2025), doi 10.1038/s41597-024-04232-w, not the arXiv preprint. The definition's BibTeX already cites it.
   - Licence: CC BY-NC 4.0 now; CC BY 4.0 in Zenodo v1.
   - The comment "Unclear what to do with SMILES" is answered by issue 1; see the proposed record comment.
8. **Resolved (2026-10-14): the process notes are followed up.** `leak_probes.py` now fits each string column alone as text, the PubChem reCAPTCHA note is in the curation guidelines, RDKit is in the `build` extra, and option (c)'s SMILES encoder is not needed (issue 1). (Was: Process and framework notes.)
   - `leak_probes.py` skips string columns, so a SMILES-only structure is never leak-probed. I ran my own checks with ECFP4 and char n-grams.
   - PubChem's literature endpoint (`sdq/sdqagent.cgi`, which the authors' code uses) answered this machine with a reCAPTCHA page after a few automated requests. I stopped there and used PUG REST and PUG-View instead.
   - RDKit for the analysis came read-only from the uv cache (cp313 wheel, uv's Python 3.13, PYTHONPATH); no venv was created.
   - I wrote `splits_comment` as one line to avoid the known dedent gap in the README.
   - Issue 1's option (c), a SMILES encoder, belongs in `datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md` next to the other harness items. I did not edit that file, since the brief limits me to my own folder.

**Verification (fix round, 2026-10-07).** The verifier's report is `verify/verify.md`; it called the dataset "needs changes" on one decision (issue 1) and passed the rest. I re-checked its numbers with my own code before changing anything:
- Qwen3-Embedding-8B, 32 dimensions, lowercased: re-scored its saved embeddings with my own split and model code (`scripts/recheck_embedding.py`) and reproduce its table to within 0.005 (embedding alone 0.58 / 0.59 / 0.54; with flags and year 0.78 / 0.81 / 0.81; flags and year alone 0.80 / 0.70 / 0.82). Accepted; implemented option (b). Re-measured on the shipped frame, after the flags became missing for the unknown type (`scripts/recheck_with_na_flags.py`): embedding with flags and year 0.79 / 0.83 / 0.81 against 0.80 / 0.69 / 0.82 without it, ECFP4 0.83 / 0.86, MACCS 0.85 / 0.85, character n-grams 0.84 / 0.85. The conclusion is unchanged, and `curation_comments` carries these numbers.
- All-zero flags are the source's "unknown" type: 55 rows, all from ECOTOX, 29 toxic (53% against 27% for the compounds with a type); per window 5 / 9 / 2 / 1, of which 5 / 4 / 0 / 1 toxic, so all 5 in the newest window are toxic (`scripts/fix_round_checks.py`). Accepted; the four flags are now missing on those rows. The leak probe's missing-indicator now scores 0.569, which is that group and is documented.
- ppdb.csv has 860 rows but 859 distinct CAS numbers (DDT twice), so 399 compounds are in both PPDB and cleaned ECOTOX, 41 of them with disagreeing labels. Accepted; the comment says 399.
- Dilution by the noisy year: reproduced (at most 0.044 AUC, no label bias). Accepted; the per-window fallback counts are now in the year note.
- Five CIDs shared by two rows, chlormequat and chlormequat chloride one active: reproduced in the first round's CID check. Accepted; mentioned in the year note.
- 8-window design: not implemented (it needs `_make_splits`); raised as issue 3 for Lennart. IID dropped as an alternative, as the verifier argued.

After the changes: `dataset check` 0 errors, 0 warnings, 1 info (the same accepted warning); checksum `v2:1c967b7f1d793768b671dd66d11439f13cdc794f4006f2b1c8d642b448bbee51`, identical under pandas 2.3.3 and 3.0.6; ruff clean; `pytest -k apistox` passes with and without the data checks; `dataset list` exits 0. Probes re-run (`<scratch>/probes2/`): leak 0.799 with all columns, depth-2 / depth-3 tree 0.809 / 0.792, `insecticide` alone 0.785, no exact copies, missing-indicator 0.569; task probes now flag only `unstable` (linear 0.798, random forest 0.784, LightGBM 0.763, above the dummy on 4 of 4 windows, spread 0.070 against a paired SE of 0.032); generated-data probe no flag.

### ashrae_great_energy_predictor_iii

**Outcome:** added and checked, as `datasets/_dev/tabarena-v0pt2/ashrae_great_energy_predictor_iii_1m/` (`version_of = "ashrae_great_energy_predictor_iii"`; the cleaned frame has 40.1M rows, so there is no full-size folder).

**Record judgment:** valid with concerns.
- Provenance is clear: ASHRAE's Kaggle competition (2019), with the data and the task described by the competition's technical team (Miller et al. 2020, "The ASHRAE Great Energy Predictor III competition: Overview and results", arXiv 2007.06933; BDG2 data paper, Sci Data 7:368).
- Unique: no folder of the working copy and no other record of this run holds these buildings. `appliances_energy_prediction` (No) is a different house (Candanedo 2017). `buildingsbench` (No) is NREL's load-forecasting benchmark, which also loads BDG2 series (its README: `load_torch_dataset('bdg-2:panther')`); no conflict while it stays No.
- Scope: borderline forecasting. The curator's comments already accept it ("forecasting-as-tabular task", "I think we can make this a nice split"), so this is issue 2, not a reason to stop.
- Why it was suspended: the v1 notebook (`datasets/_maintenance/_suspended/ashrae_energy_predictor/`, commit ec93ef4, 2026-02-09) says "a very weird case of task and how to setup, we need to make some big judgment calls", "they really fit one model per type". The record adds "we only have 1 year but data was used to forecast 2 years". The definition settles these calls as follows: one model over all meter types, with the meter type as a feature. The second year comes from the competition team's own release (issue 1).

**Data:**
- Kaggle competition `ashrae-energy-prediction`, downloaded with `uvx --from kaggle==2.2.2 kaggle` (no 403):
  - `train.csv`: 2016, 20,216,100 rows;
  - `building_metadata.csv`: 1,449 buildings;
  - `weather_train.csv` and `weather_test.csv`: 2016-2018 in UTC, 417,016 rows.
  The md5 sums equal the curator's v1 copy in `local-data-warehouse/ashrae_energy_predictor/`.
- BDG2 repository, `data/meters/kaggle/kaggle.csv`, pinned to commit 9581aafe (Git LFS, sha256 67e6d3e8…): the competition's 2017 public-test readings in the Kaggle schema, 20,848,800 rows, of which 20,547,220 have a reading. All 2,380 meters are there, and the 2017 values continue the 2016 ones in the same units.
- Stacked: 41.06M rows. After cleaning: 40,067,642 rows x 16 columns (2016: 19.68M, 2017: 20.39M).
- Licences (noted, not a verdict reason):
  - Kaggle rules, section 7A: "You may access and use the Competition Data for any purpose, whether commercial or non-commercial". Section 7B: "You agree not to transmit, duplicate, publish, redistribute or otherwise provide or make available the Competition Data to any party not participating in the Competition."
  - BDG2 has three statements. At the pinned commit 9581aafe the LICENSE file is the MIT License (2020). The Zenodo release v1.0 (doi 10.5281/zenodo.3887306, 2020-06-10) says CC BY 4.0. Since commit 9b97ccbe (2023-10-14) the LICENSE file is headed "Attribution-ShareAlike 4.0 Unported" and holds CC BY-SA legal text.

**Definition:**
- Prediction point: after a cutoff, the model gives the hourly reading of a known meter from the building's metadata, the meter type, the local time and the weather observed in that hour. This is the competition's "counterfactual models ... based on historic usage rates and observed weather" for measurement and verification (M&V). No reading after the cutoff is an input.
- Target: `log1p_meter_reading`, so the default RMSE equals the competition's RMSLE.
- Regime: temporal on `timestamp` (local time), `TemporalSplits(window=4, unit="months", cutoffs=("2017-01-01", "2017-05-01", "2017-09-01"))`:
  - three windows tile 2017, and the oldest trains on exactly 2016 (50.07% of the hours, 49.12% of the rows), which is the competition's own setting;
  - `_1m`: each window keeps 500k of its 6.70-6.86M rows, and each train side is 1M random earlier rows;
  - the shipped frame has 2,500,000 rows x 15 features. Features: building_id, site_id, meter, primary_use (categories), square_feet, year_built, floor_count, timestamp (datetime) and 7 weather columns.
- Cleaning:
  - site 0's electricity is converted from kBTU to kWh (x0.2931, the host's factor in discussion 119261);
  - each site's weather is shifted from UTC to local standard time with the 1st place offsets. After the shift every site's mean day peaks at 14:00-16:00; before it the peak was at 19:00-23:00 at the 13 North American sites. 180,095 rows (0.45%) have no weather row for their hour;
  - dropped: 301,580 unlabelled 2017 hours, site 0's electricity before 2016-05-21 (348,560 rows, 98.9% zeros) and all other electricity readings of 0 (347,118 rows; BDG2's cleaned data drops these too);
  - thermal-meter zeros stay (2.68M rows, 6.7%) because they are seasonal;
  - other recording errors stay, for example building 1099's steam meter at about 1,000 times its level in March-June 2016;
  - three `_decisions` tables show the evidence: the time zones, the rows dropped per meter type, and the zero share by month.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). Nothing is accepted, and `accepted_check_warnings` is empty.
- Checksum `v2:858c1cad…`, after the verification edits. A check-only run under pandas 3.0.6 (the shared pd3 venv) gives the same checksum as pandas 2.3.3.
- `pytest tests/test_v2_datasets.py -k ashrae_great_energy_predictor_iii_1m`: 1 passed, 1 skipped (the opt-in data check).
- ruff is clean, there is no `TODO`, and `load_definition` imports the file.
- One run takes about 2-4 min and 12 GB of RAM: `_load_raw` reads 1.6 GB of CSV.

**Probes:** all run on a scratch root holding only this folder, because another agent's half-written folder broke `discover_datasets`. All ran with 2 threads; `leak_probes.py` ran as a scratch copy with LightGBM `n_jobs=2` instead of the hard-coded 8.
- Leak probes (3 windows, 50k rows a side, untuned LightGBM, timestamp left out):
  - R² 0.716 with all features; depth-2 / depth-3 trees 0.209 / 0.225;
  - single features: building_id 0.440, square_feet 0.278, site_id 0.113; R² 0.643 without building_id;
  - 0.2% of test rows have an exact copy in train; 1-NN R² 0.277 for the closest tenth.
  - No leak pattern. building_id is the meter's level, which is what a per-building baseline model is built from, and it is well below the full model.
- Task probes (3 of 3 windows):
  - R²: dummy -0.001, drift baseline -0.001, linear 0.179, random forest 0.647 (RMSE 1.242 on the log scale), LightGBM 0.640;
  - the single feature chosen on each split (square_feet, 3 of 3) reaches 0.278;
  - the best family beats the dummy on 3/3 windows (SE 0.012). Flags: none.
  - The probe encodes the timestamp as a number, so it has no hour of day. The scores are a lower bound.
- Generated probes: 1.5% of rows fit a formula exactly, against 1.5% for a shuffled target. Flags: none.
- `hidden_groups.py` and `group_probes.py` do not apply: the task is temporal. The repeated meters are the intended warm start (all 2,380 meters are in 2016 and in 2017).

**Verification:** the verifier's verdict was "ready with noted concerns" (`verify/verify.md`, 2026-10-07). It confirmed that the 2017 file matches the competition's `test.csv` on all 20,848,800 rows. I applied all five findings, each after recomputing it (`explore/e9_verifier_findings.log`):
- Finding 1 (licence), applied. At the pinned commit the BDG2 LICENSE is MIT. Zenodo v1.0 (10.5281/zenodo.3887306) says CC BY 4.0. The CC BY-SA header dates from commit 9b97ccbe (2023-10-14). Kaggle rule 7B forbids redistribution to non-participants. `license` and the record comment now list all four.
- Finding 2 (count), applied. 180,095 rows (0.45%) have no weather row. 196,649 was the count of rows missing `air_temperature`. I also changed "13 sites west of Greenwich" to "13 North American sites": BDG2 gives Europe/London for sites 1 and 5 and Europe/Dublin for site 12. The trace count is now 11,744 weather hours of 2016-2017; 18,051 was the count over 2016-2018.
- Finding 3 (DST), applied as wording, with no change to the data. The readings of sites 0, 3, 4, 6, 8, 9, 10 and 15 skip the spring-forward hour, which affects 33.79% of the rows. I cite the verifier's DST-aware rerun: RMSE moved by -0.007 to +0.005 per window. This closes issue 6.
- Finding 4 (citation), applied. The GEPIII overview is now in `bibtex`: Sci. Technol. Built Environ. 26(10):1427-1447, doi 10.1080/23744731.2020.1795514; the details are from Crossref.
- Finding 5 (window share), applied. `splits_comment` now says 50.07% of the hours (8,784 of 17,544) and 49.12% of the rows. Whether that meets the floor stays Lennart's call (issue 5).
- Hour of day: issue 7 is closed, because `tabarena_default` extracts the hour and the weekday.
- Re-run after the edits: `dataset check` 0/0/0, ruff clean, the pandas 3 checksum equals pandas 2 (`v2:858c1cad…`), and pytest gives 1 passed, 1 skipped. My private venv and the parquet intermediates are deleted.

**Issues for Lennart:**
1. **A second source for the test year. Accept it?**
   - Evidence: the competition team released its 2017 public-test readings in BDG2: "the data for the validation data set (2017) that matches seamlessly with the training data found on the competition website" (BDG2 paper, p. 8). The GEPIII overview, Sec. 8.2, says the same. The 2018 private-test readings stay unpublished.
   - Now: 2016 from Kaggle plus 2017 from BDG2, so the train side of the oldest window is the competition's training year. This answers the record's "we only have 1 year".
   - Alternative: Kaggle files only (19.68M rows). The windows would then sit inside 2016: Oct/Nov/Dec 2016 with train shares of 74%, 83% and 91%, or 2-month windows from July with train shares of 48%, 65% and 83%. No train side would hold a full year.
2. **Scope (forecasting).**
   - Evidence:
     - the GEPIII overview, Sec. 2.2, frames the task as "regression-based machine learning to predict the energy savings of a retrofit in the measurement and verification (M&V) process";
     - no lagged readings are inputs; across a panel of 2,380 meters, building and weather drive the reading;
     - in the copy, rossmann_store_sales is a precedent for in-scope; appliances_energy_prediction and combined_cycle_power_plant (single series) are precedents for No.
   - Now: in scope, as the record already accepts. Alternative: `Time-series (Forecasting)` and No.
   **Follow-up (AI, 2026-10-15):** Lennart asked whether a naive time-series model beats LightGBM and whether splitting the task helps. RMSE on log1p(kWh), full test windows W1 / W2 / W3, after the new cleaning (issue 4). Best naive forecast, each meter's hour-of-week profile from the same month a year earlier: 1.393 / 1.273 / 1.372 (the same hour 52 weeks earlier: 1.563 / 1.436 / 1.546). Default LightGBM (100 trees) loses to it: 1.444 / 1.403 / 1.448. LightGBM with 1,000 trees and 255 leaves wins: 1.265 / 1.177 / 1.235 on the full history, 1.261 / 1.176 / 1.223 on 1M rows (the shipped train size, where the naive profiles drop to 1.46-1.49). Split models: per site 1.238 / 1.178 / 1.222, per meter type 1.278 / 1.225 / 1.281, per building and meter (the 5th place approach) 1.368 / 1.265 / 1.337. The weather adds 0.01-0.05. Unseen buildings (every fifth held out, W1): LightGBM without building_id 1.709, a site x use x meter profile 2.012, LightGBM with their 2016 history 1.430. The top five teams used no lagged readings (GEPIII overview, Table 2). Recommendation: in scope as one task.
   **Resolved (Lennart, 2026-10-15):** in scope as one task; ship.
3. **Temporal or grouped.**
   - The record lists both regimes. The competition's test years hold the same buildings, and M&V predicts "the building's pre-retrofit energy use rate in the post-retrofit period" (Sec. 2.2).
   - Now: temporal, with building_id as a feature (warm start).
   - Alternative: hold out whole buildings (new buildings, a benchmarking use case the source does not pose), or grouped-temporal.
   **Resolved (Lennart, 2026-10-15):** temporal; the record's `tags` and `required_split` no longer list the grouped regime.
4. **How much to clean.**
   - Now: drop electricity zeros and site 0's recording gap; keep the thermal zeros and all other anomalies. The competition page itself calls this "real data with measurement error". The top teams removed anomalies by hand, building by building.
   - Alternative A: BDG2's full rule also removes zero runs of more than 24 h, which drops 1,766,800 thermal rows (4.4%; 882,158 in 2017). Most of these are seasonal shut-downs: chilled-water runs hold 158,774 rows in January and 20,009 in August.
   - Alternative B: keep the electricity zeros too, as the competition scored them.
   - Known unit errors stay (BDG2 p. 8: fixed in BDG2, "left as-is in the Kaggle data set"). Building 1099's steam is in train only (2016).
   **Resolved (Lennart, 2026-10-15):** clean to an expert state, as the top teams and the data owners did. Applied: readings in kWh from BDG2's raw files (the competition kept each site's own unit: 360 chilled-water meters in ton-hours, 312 steam meters in pounds of steam, 198 in mmBTU, 148 in kBTU, 27 at site 7 at 3,600 times kWh); dropped as not recorded, besides the electricity zeros and site 0's gap: a cooling or heating plant at 0 for 48 hours or more in its season (chilled water May-October, steam and hot water November-April; 383,406 hours), the repeats of a reading stuck for a week or more (618,666 hours, 365k of them site 5's electricity at about 0.0004 kWh from March to November 2017) and building 1099's steam above 10 times its median (3,332 hours). In all 1,701,150 hours (4.2%), 39,062,170 kept. Of the 2016 hours dropped, 94.5% are on the 1st place team's hand-made bad-reading list (`solutions/rank-1/input/bad_meter_readings.zip`); the rules cover 64% of that list. The rest of the list is mostly zeros of thermal meters outside their season (the team removed about a third of these by eye), which stay. Alternatives A (BDG2's 24-hour zero rule) and B are not taken. Not built.
5. **Window length.**
   - Now: 3 x 4 months. The oldest train side holds 50.07% of the hours (8,784 of 17,544) but 49.12% of the rows, 0.9 points under the 50% floor by rows. It is kept because it is the competition's setting; `splits_comment` now says both shares.
   - Alternative: 3 x 3 months (Apr-Jun, Jul-Sep, Oct-Dec 2017), with train shares of 61.7%, 74.4% and 87.2%.
6. **Daylight saving time: closed, no change to the data.** The meters of 8 sites (0, 3, 4, 6, 8, 9, 10, 15) skip the spring-forward hour, so 34% of the rows (33.79%) get weather one hour late. The verifier rebuilt the join with BDG2's per-site time zones and refit LightGBM with hour and weekday: RMSE moved by -0.007 to +0.005 per window, no consistent gain. The fixed offsets stay, and `curation_comments` now says so with these numbers.
7. **Hour of day in the harness: closed.** TabArena v0.2's `tabarena_default` preprocessing encodes `timestamp` with skrub's `DatetimeEncoder(add_weekday=True, periodic_encoding="circular")`, which keeps the hour and the weekday. With them LightGBM's RMSE is 3-6% lower (verifier). No extra column is needed. It would matter only if the v0.1 `default` pipeline ran this dataset.
8. **Housekeeping.** The record is `DF: Suspended` and points at the v1 notebook in `_maintenance/_suspended/`. Once the `_1m` folder is accepted, `sync-notebooks` should set `v2_path` to it, and the status and the suspended v1 notebook need updating. The download lives in `local-data-warehouse/ashrae_great_energy_predictor_iii/` (1.6 GB). The curator's v1 copy is in `ashrae_energy_predictor/` (2.6 GB).
   **Resolved (Lennart, 2026-10-15):** drop the suspended v1 copy; `v2_path` already points at the `_1m` folder and the record is `WIP (DF)`. `datasets/_maintenance/_suspended/ashrae_energy_predictor/` is removed (it stays in the git history), and so is the curator's local v1 copy of the raw files (`local-data-warehouse/ashrae_energy_predictor/`, the same files as the download).

### bias_correction_r_bias_correction_r_2

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/bias_correction_r_bias_correction_r_2/`); verifier:
"ready with noted concerns", all findings applied (see Verification).

**Record judgment:** valid.
- Provenance: the data first appeared at UCI (dataset 514, donated 2020-02-17 by the authors of Cho et al. 2020, Earth
  and Space Science 7(4) e2019EA000740).
- Task: a predictive one, post-processing (bias correction) of KMA's LDAPS next-day temperature forecasts at 25 Seoul
  weather stations. It is a fixed regression with a temporal split, not time-series forecasting: the main inputs are
  the NWP model's forecasts for the target day.
- Unique: no folder of the working copy and no other record holds it (grep for the DOI, UCI id, LDAPS and Seoul; the
  only Seoul record is the bike-sharing data). `climate_model_weather_forecasting_1m` (TabReD, Yandex stations) is a
  related task on other data.
- The record's two names are TALENT's two tasks from this one file: `Bias_correction_r` is `Next_Tmax` (TALENT dummy
  RMSE 3.04 against the target's standard deviation 3.12) and `Bias_correction_r_2` is `Next_Tmin` (2.42 against
  2.48).

**Data:**
- Source: the UCI static zip
  `https://archive.ics.uci.edu/static/public/514/bias+correction+of+numerical+prediction+model+temperature+forecast.zip`
  (one file, `Bias_correction_ucl.csv`, sha256 `c60150c3...cbf5ea`), in
  `local-data-warehouse/bias_correction_r_bias_correction_r_2/`.
- 7,752 rows x 25 columns: 7,750 station-days (25 stations x 62 days, June 30 to August 30 of 2013-2017) and two summary
  rows (column minimum and maximum, no station or date).
- Licence CC BY 4.0 (UCI dataset page); the paper is CC BY-NC-ND.
- The paper PDF (open access, UNIST repository) and its text are in `_scratch_new65/bias_correction_r_bias_correction_r_2/`.

**Definition:**
- Prediction point: the evening of the present day, once the LDAPS run started at 12 UTC (21 KST) is out. The paper
  uses the "data of LDAPS model produced at 21 KST (12 UTC) for the next-day forecast" (Sec. 2.2, p. 3), and the
  present-day extremes cover 0-21 KST (Sec. 2.3, p. 3).
- Target `Next_Tmin` (next day's minimum air temperature, AWS observation). `Next_Tmax` is dropped: it is observed after
  the prediction point (see issues 1 and 2).
- Temporal on `Date`: `TemporalSplits(window=7, unit="days", n_windows=9, gap=1)`. 9 weekly windows walk back from
  2017-08-30 and cover the whole last summer (62 test days), with 149-175 test rows (6-7 days of 25 stations) and train
  80-97% of the rows. The 1-day gap keeps out the day before each window: its label, the minimum of the window's first
  day, is complete only at midnight, after that evening's first prediction.
- 7,723 rows x 23 features: `station` categorical (25 levels), `Date` datetime, 21 numeric.
- Cleaning: drop the two summary rows; drop 27 rows without a target (12 in 2017). Missing inputs stay missing: LDAPS
  absent on 3 whole days (75 rows, all in train) and present-day observations absent on 60 station-days (32 in 2017).
- Four `_decisions` with tables: temporal split (variance within days); the target (raw forecast, station-mean
  correction and two per-station MOS fits for each target); the targets against the present-day columns; the window
  options (including explicit cutoffs over 2016-2017).
- Checksum `v2:41fdfb3c...`, the same under pandas 2.3.3 and 3.0.6.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 infos (26 checks); nothing accepted.
- `pytest -q tests/test_v2_datasets.py -k bias_correction`: 1 passed, 1 skipped. With `DATA_FOUNDRY_V2_DATA_CHECKS=1`
  both pass, including the rebuild that reproduces the README checksum.
- ruff check and format: clean.

**Probes:**
- **Leak** (3 newest windows): R² 0.745 with all features. `LDAPS_Tmin_lapse` alone gives 0.531, and dropping it
  leaves 0.512. Shallow trees give 0.19 and 0.46. No test row has an exact feature copy in train. 1-NN R² is 0.629 on
  the closest tenth and 0.135 overall: the nearest training rows are the same station on late-August days of 2013-2014
  with similar weather (analog days), not copies. No flag.
- **Task** (first 5 of 9 splits): RF RMSE 0.869, LightGBM 0.829, linear 0.903, single feature 1.102; flag `no_spread`.
- **Task** (all 9 splits): LightGBM 0.858, linear 0.902, RF 0.900, single feature 1.046 (`LDAPS_Tmin_lapse`, 9 of 9),
  dummy 2.177; flags `no_spread` (LightGBM - linear +0.012 skill, paired SE 0.066) and `unstable` (SE of the mean
  skill 0.088).
- Answers, recorded in `curation_comments`:
  - `unstable`: the best family beats the dummy on 9 of 9 windows. The dummy's error varies from RMSE 1.0 to 5.3
    between weeks: the last week of August 2017 averaged 18.2 degrees C against a training mean of 23.0. That is
    drift, not missing signal; on 5 windows the SE is 0.039.
  - `no_spread`: a window is 6-7 weather days and the day carries 82.5% of the target's variance, so windows separate
    strong methods little (paired SEs 0.028-0.042 RMSE between CatBoost, LightGBM and ridge).
  - Headroom above the standard correction: the mean of CatBoost, LightGBM and ridge beats a per-station MOS on 7 of 9
    windows (0.779 against 0.823, SE 0.020), while single untuned models only tie it. To re-check with tuned results;
    none exist yet, so `tuned_results.py` was skipped as the brief says.
- **Generated:** exact 5.0% against 2.6% shuffled; no flag. A good linear fit with residual SD of about 0.85 lands
  within the 0.1-degree rounding in about 5% of rows by chance.
- **Hidden-group / group probes:** not run (temporal task).

**Issues for Lennart:**
1. **One target under the `Multi-target` tag (your call).** The guidelines name next-day minimum and maximum as the
   `Multi-target` case, and a v2 task holds one target. As in `electric_motor_temperature_prediction` (tag kept, one
   target), the record keeps its tag and the folder ships one target, `Next_Tmin`. `Next_Tmax` cannot stay as a
   feature (observed on the next day). Two folders would count one file twice with correlated targets (r = 0.62).
2. **Which target: `Next_Tmin` (implemented) or `Next_Tmax`.** Shipped windows, untuned, my code and the verifier's
   agree:
   - `Next_Tmin`: per-station MOS on forecast and present-day minimum 0.823 (forecast-only 0.855). CatBoost 0.804 and
     LightGBM 0.807 only tie it (CatBoost -0.020, SE 0.037). The mean of CatBoost, LightGBM and ridge (0.779) beats it
     on 7 of 9 windows (-0.044, SE 0.020).
   - `Next_Tmax`: forecast-only per-station MOS (1.575) beats every untuned model (LightGBM 1.583, ridge 1.669,
     CatBoost 1.710) and their mean (1.601).
   - Nuance: on 14-day cutoffs over 2016-2017 the mean of the three also beats MOS on `Next_Tmax` (1.498 against 1.582,
     SE 0.078, 6 of 9). The maximum's verdict depends on the test summer; the minimum's margin over MOS holds in both
     designs (-0.050, SE 0.024 over 2016-2017).
   - Alternative: ship `Next_Tmax` instead (change the target and the drop: two lines). I recommend `Next_Tmin`.
3. **Window placement.**
   - Implemented: 9 contiguous weekly windows over summer 2017 (convention: roll back from the newest data; one to two
     weeks at most for weather).
   - Alternative 1: 14-day windows walking back give only 5 windows before the empty weeks before July 2017.
   - Alternative 2: explicit cutoffs over 2016-2017 give 9 fourteen-day windows (118 test days, train 62-95%) and test
     two summers, closer to the paper's 2015-2017 hindcast (the best model differs by year, Table 3, p. 10). They
     separate methods no better (paired SEs 0.023-0.047 against 0.028-0.042).
   - The 1-day gap changes the scores by at most 0.01 RMSE.
4. **Rows with missing inputs kept.** 75 rows on the three days without an LDAPS run (all on the training side) and 60
   rows without present-day observations (32 in the 2017 test windows) are kept as NaN. The paper does not say how it
   handled them (it mentions 135 complete days only for its maps, Sec. 4.3, p. 12). Alternative: drop the 75 LDAPS-less
   rows, which would not change any test row.
   **Resolved (Lennart, 2026-10-15):** the task corrects the LDAPS forecast, so a row without one has nothing to correct: the 75 rows of the three days without an LDAPS run are dropped (no test row changes; 7,648 rows remain). The 60 rows without present-day observations stay. The mean of untuned CatBoost, LightGBM and ridge still beats per-station MOS on 7 of 9 windows (0.785 against 0.823, paired SE 0.022). The probes now flag `unstable` again: LightGBM falls just below the training mean in the oldest window (2017-06-30 to 07-06, skill -0.07, dummy RMSE 1.11) and beats it on the other 8 (0.61-0.96); kept, as noted in `curation_comments`.
5. **TALENT's numbers for this dataset are inflated (information).** TALENT splits both tasks at random. Its best RMSEs
   (TabR 0.57 for the maximum, 0.45 for the minimum) are far below what folds that keep each day's stations together
   give (LightGBM 1.54 and 1.00), because the other stations of a test day are in train.
   **Answer (2026-10-15):** TALENT came up only because the record's two names are its task names; its random-split scores say nothing about this task and are not used anywhere.
6. **Framework notes.**
   - (a) Earlier in this run a fresh scaffold with `problem_type = "TODO"` (`perth_house_prices`) broke `pytest`
     collection for every folder. It is fixed now; `problem_type` belongs on the list with `domain` and `source`.
   - (b) I wrote `splits_comment` as one concatenated string to avoid the known dedent gap (ORCH_NOTES item 10).
   - (c) `task_probes.py` flags `unstable` on temporal tasks whose dummy error varies strongly between windows even when
     every window beats the dummy (here 9 of 9). A paired criterion would separate drift from instability, as in the
     consumer_complaints precedent.
   **Resolved (Lennart, 2026-10-15), applied:** (a) `tests/test_v2_datasets.py` discovers leniently and checks each folder's import in its own test, so a scaffold with a `TODO` in `problem_type`, `domain` or `source` fails one test, not the collection; (b) the dedent gap was fixed on 2026-10-12, so `splits_comment` is a text block again; (c) `task_probes.py` counts the standard-error part of `unstable` on a temporal task only when the best family loses to the dummy on a window, and its JSON now lists the skill and the dummy's loss per split.
7. **Pending (orchestrator):** the record's `v2_path` is unset (`sync-notebooks`); the container is not built.
   **Resolved (Lennart, 2026-10-15):** `v2_path` is set; the container is built with the next rebuild.

**Verification** (independent verifier, 2026-10-07: "ready with noted concerns"; no leak, no wrong split, no blocker;
report in `verify/verify.md`). Each finding and what I did:
1. **MOS baseline (evidence): applied.** I reproduced it with my own code (`mos_check.py` / `.out`): per-station MOS
   0.823 (verifier 0.824) and 0.855 for `Next_Tmin`, 1.575 and 1.625 for `Next_Tmax`. The mean of the three models is
   0.779, -0.044 (SE 0.020), 7 of 9 (verifier 0.782, -0.042, SE 0.017). Changes:
   - Decision 2 now has two per-station MOS rows for both targets, computed in the hook.
   - The target bullet uses MOS as the baseline, citing Sec. 1, p. 2 for the MOS definition.
   - The task-probe bullet replaces the station-correction and kNN/MLP argument with the ensemble-against-MOS numbers
     and a note to re-check with tuned results.
2. **Prediction point (wording): applied** in `curation_comments` ("the evening of the present day, once the LDAPS run
   started at 12 UTC (21 KST) is out; the present-day extremes cover 0-21 KST", with the exact Sec. 2.2 quote), in
   `splits_comment` ("after the first prediction that evening") and in the record comment.
3. **rain_in_australia (wording): applied.** `splits_comment` now cites only climate_model_weather_forecasting, phrased
   as the curator wrote it ("I would argue for one or two weeks at most?").
4. **Decision 4 (wording): applied.** The sentence now says the 14-day limit holds walking back, and that explicit
   cutoffs over 2016-2017 give 9 windows with 118 test days but separate methods no better. My run gives paired SEs of
   0.023-0.047 against 0.028-0.042; the verifier's were 0.025-0.041 against 0.020-0.035. The option is a row in the
   table, with test days and train share.
5. **Wording: applied.**
   - "0.31 degrees C on average among those" (0.25 is the mean over all pairs).
   - The `no_spread` reason is now 6-7 weather days per window, with the day carrying 82.5% of the variance; the splits
     comment says "149-175 station-days (6-7 days of the 25 stations)".
6. **Multi-target (Lennart's call): stated** as issue 1, no change.
7. **Pending:** record pointer and build are the orchestrator's steps.

**Resolved (Lennart, 2026-10-15):** ship.

### brazilian_ecommerce
**Outcome:** added and checked

**Record judgment:** valid with concerns. Olist (a Brazilian marketplace operator) released its own order data on Kaggle on 2018-09-21 ("This is real commercial data, it has been anonymised", data card); no other record and no folder of the working copy uses it (grep for olist / olistbr / marketing-funnel: only this record). Concerns: the source names several uses and no target, so the task is our choice (issue 1); the sample holds only orders with an answered review (uploader, Kaggle discussion 66466: "It's a simple random sample of all orders that received a customer review"), which censors the newest month (issue 2); building one row per order from nine tables takes several choices (issue 5).

**Data:** Kaggle `olistbr/brazilian-ecommerce`, version 2 (DOI 10.34740/KAGGLE/DSV/195341), downloaded with `uvx --from kaggle==2.2.2 kaggle datasets download` to `local-data-warehouse/brazilian_ecommerce/`: nine CSVs, eight read (orders 99,441 x 8, items 112,650 x 7, payments 103,886 x 5, reviews 99,224 x 7 (only the survey dates are read), customers 99,441 x 5, products 32,951 x 9, sellers 3,095 x 4, category translation 71 x 2; the geolocation file, 1,000,163 x 5, is not used). Licence CC BY-NC-SA 4.0 (Kaggle data card and its Croissant metadata).

**Definition:** `datasets/_dev/tabarena-v0pt2/brazilian_ecommerce/`. Prediction point: at checkout (what is known when the customer places the order, including the delivery date Olist promises then). Target `log_delivery_days` (log of the days from purchase to delivery; regression, RMSE). Temporal on `order_purchase_timestamp`, custom `_make_splits`: 5 monthly test windows, March to July 2018, train = orders placed at least one month before the window and delivered before it starts (train 49,981-76,876, test 5,828-6,913 rows; horizon 1 month). 88,721 rows x 24 features (23 plus the purchase timestamp). Cleaning: delivered orders only; orders placed before 2018-08-01 with a promised date on or before 2018-08-24 (end of the review sample, issue 2); one-seller orders only (1,155 dropped); one row per order with item counts, price and freight sums, the first item's product attributes, payment methods / installments / total; the promised date as `estimated_delivery_days`; post-checkout columns and ids dropped (seller_id kept as a category); categories translated; product weight 0 g set to missing.

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info. Accepted: `splits_rows_unused` (4 orders placed in January-February 2018 and delivered after 148-208 days, still in transit when the newest window starts). Info `dataset_conflicting_duplicate_rows`: 56 orders in 27 groups are one customer buying the same product from the same seller in the same second as separate orders (same customer_unique_id), delivered separately; kept. pandas 2.3.3 and 3.0.6 give the same checksum, v2:5e0a3d4e... after the verification edits (pandas 3 in a scratch venv). `tests/test_v2_datasets.py -k brazilian_ecommerce` passes, also with `DATA_FOUNDRY_V2_DATA_CHECKS=1` (2 passed); the import check with `load_definition` passes; no `TODO` left in `dataset.py`.

**Probes:** (run with `--root` on a scratch folder that links only this dataset, because other agents' half-written folders failed to import at the time)
- leak_probes (first 3 shipped windows; the datetime column is left out): all features R^2 0.233; depth-2/3 tree 0.151/0.178; best single feature `estimated_delivery_days` 0.132, next `customer_zip_code_prefix` 0.035; missing-value indicators all below 0; without the estimate 0.166; 0.0% of test rows have an exact copy in train; 1-NN R^2 -0.49 (closest tenth) / -0.55. No leak signal.
- task_probes (5 of 5 windows): dummy R^2 -0.197 (the mean shifts between months), drift baseline skill +0.039, linear +0.194, random forest +0.433, LightGBM +0.448 +- 0.076 (R^2 0.351), single feature +0.310 (the estimate in 3 of 5 windows); LightGBM beats the dummy in 5 of 5 windows; spread LightGBM - linear +0.254 (paired SE 0.103). Flags: none.
- generated_probes: 1.5% of rows fit exactly against 1.5% for a shuffled target; flags: none.
- hidden_groups / group_probes: not run (temporal task).

**Issues for Lennart:**
1. **Which task?** The record's problem type is TBD and names "predict future sales, optimize delivery times". Implemented: delivery time at checkout, the data card's "Delivery Performance: ... optimize delivery times". Sales prediction ("With purchase date information you'll be able to predict future sales") is time-series forecasting, out of scope. Alternatives, measured with untuned LightGBM on the same 5 windows and features: (a) late delivery (delivered after the promised date; binary): ROC AUC 0.62-0.70 (mean 0.663), late share per window 1.4% (June, 83 orders) to 21.6% (March, 1,491); it is a threshold of the shipped target against a feature, so it would be a `_clf` variant, not a new task. (b) review score 1-5, predicted after delivery and before the customer answers. This is the task the uploader framed: "Lets create a model to predict what's the score a customer will give for an order", with "data from each order up to delivery phase", and "we need to predict the score before a customer writes it" (Andre Sionek of Olist, kaggle.com/code/andresionek/predicting-customer-satisfaction, cells 0, 4 and 5, last run 2018-10-24, 299 votes; it reads the older single-table release `olist_public_dataset_v2.csv`, splits at random and scores on its training set; Kaggle keyword "multiclass classification"). The data card's "Delivery Performance" bullet is framed as analysis. Numbers with the delivery outcome as features (days to delivery, days late): a low score (1-2, 12.6% of orders) reaches ROC AUC 0.66-0.83 (mean 0.717; 0.596 from the checkout features alone); an untuned 5-class LightGBM loses to the class shares in 4 of 5 windows (log loss 1.11-1.25 against 1.05-1.34). With the review score as the target, the release's selection on answered surveys (issue 7) would be the task's own population, and the review text written with the score would be dropped. Kept as implemented: delivery time. Switching is your call.
   **Answer (AI, 2026-10-15):** the use case is the delivery date shown at checkout. Olist promises a date when the order is placed ("informed to customer at the purchase moment"); a better prediction of the actual days lets it promise a tighter date (its promise is 23.5 days at the median against 9.7 delivered; 6.9% of the shipped orders arrive late) and warn or expedite orders likely to be late. Late delivery is a threshold of the same target against the promise, so it would be a `_clf` variant of this task, not a second one. The review score is, as you say, closer to a satisfaction or recommender task driven by the delivery outcome and the product, and its signal is weak (a 5-class LightGBM loses to the class shares in 4 of 5 windows). Recommendation: keep the regression.
2. **End of the review sample.** The last survey in the reviews file was sent on 2018-08-31, and a survey goes out at delivery or at the promised date, so orders placed in August 2018 are only in the sample when they arrived by then (August p90 13.1 days against 16.0 in July; the last week's maximum 3.6 days). Implemented: orders placed before 2018-08-01 whose promised date is on or before 2018-08-24 (drops 6,351 August and 243 June/July orders, 78 of the 591 orders of 30-31 July). Alternative: cut at 2018-07-01 without the promise rule; that removes the July window (5,828 test rows).
3. **Training rows when labels arrive late.** A model refit on the first of the month only knows the deliveries made by then. Implemented: a one-month gap before each window plus dropping the 32-353 older orders still in transit (`_make_splits`, after the hotel_booking_demand rule). The delivered orders of the last month are the fast ones (27-53% of that month still in transit at the refit; for April, median 9.1 days delivered against 13.4 for all), and the bias matters for a model that sees the purchase time as a number. Mean R^2 of untuned LightGBM on the 5 shipped windows (verifier's run, `verify/v7_gap.log`, `v7b_gap_ag.log`), with the gap / without it (as-of labels) / without it, also training on later deliveries (a leak): purchase time as a number 0.353 / -0.054 (bias -0.26 to -0.62 in every window) / 0.429; number plus date parts as AutoGluon emits them 0.320 / 0.064 / -; date parts only 0.331 / 0.392 / 0.395; no time feature 0.310 / 0.347 / 0.349. So the gap protects the numeric-timestamp models that benchmark pipelines feed, and costs 0.04-0.06 R^2 for a model without a usable time axis. Question: is the gap the fix you want for duration targets with late labels? sf_permit_time (6-month windows on the filing date, durations of months) trains on permits issued after its windows start, so the same question applies there.
   **Answer (AI, 2026-10-15):** yes. The gap simulates a refit that knows only the deliveries completed by then; without it, a model that sees the purchase time as a number is biased (R^2 0.353 with the gap, -0.054 without). sf_permit_time has had the same treatment since 2026-10-12 (training rows are permits issued before each window starts, with a 6-month gap).
4. **Window count.** Monthly windows with the gap give 5 windows above the 50% floor, not the convention's 9. Alternative: 14-day windows with a 30-day gap give 9 windows (test 1,997-3,469 rows, oldest from 2018-03-28); 21-day windows give 8. Implemented: monthly, as a monthly refit is the plainer cadence.
   **Resolved (Lennart, 2026-10-15):** monthly windows stay.
5. **Order-level construction.** Implemented: drop orders with several sellers (one delivery date for several shipments; 1,155); the first item's product attributes (98.0% of the kept orders hold one distinct product); item and payment aggregates; shipping_limit_date not used (set at payment approval, after checkout); geolocation not joined (median lat/lng per zip prefix changes LightGBM R^2 from 0.366 to 0.367). Olist's promised date is kept as `estimated_delivery_days`: known at checkout ("informed to customer at the purchase moment"), single-feature R^2 0.132, removing it lowers R^2 from 0.366 to 0.332 (most in July: 0.35 to 0.06). Alternative: drop it, so the task is predicting without the company's own estimate.
   **Answer (AI, 2026-10-15):** it is the date Olist promised the customer at checkout; the release does not say how Olist computes it. It is not a fixed route table: seller state x customer state explains 38% of its variance, with the purchase month 58%, and it is padded (median 23.5 days against 9.7 delivered). It cannot leak, since it is fixed at checkout, before the label. Kept as an input known at checkout, as bias_correction keeps the LDAPS forecast it corrects: the model refines the company's own estimate. Dropping it makes the task "predict without the company's estimate" and lowers LightGBM's R^2 from 0.366 to 0.332.
6. **Record fields.** The record says year 2019; Kaggle's Croissant metadata gives datePublished 2018-09-21 (the uploader's Q&A thread opens the same day), so the definition uses 2018. `problem_type` becomes regression with this task. Licence CC BY-NC-SA 4.0, noted only.
   **Resolved (Lennart, 2026-10-15):** the record's year is now 2018 (Kaggle's datePublished 2018-09-21); its problem type was already Regression.
7. **Selection on answered reviews.** Every order in the release has an answered survey (646 delivered orders have no review row, which the release does not explain). If customers with slow deliveries answer more often, slow deliveries are over-represented. We assume the effect is the same in every month (the release holds no unanswered surveys to check it), so it is an `Anomaly:` bullet, not a fix. With the review score as the target (issue 1), this selection would be the task's own population.
   **Answer (AI, 2026-10-15):** the reviews file gives only its survey dates, to cut the end of the sample (issue 2); no review field is a feature. The selection decides which orders are in the data: Olist released only orders with an answered survey, so if customers with slow deliveries answer more often, slow deliveries are over-represented, in train and test alike. It changes the population, not the features, and cannot be checked (the release holds no unanswered orders), so it stays an `Anomaly:` bullet.

**Verification:** (independent verifier, verdict "ready with noted concerns"; `verify/verify.md`)
1. Review score is the source's own predictive task: applied as an issue for Lennart. I read the notebook (cells 0, 4, 5) and its date (`kaggle kernels list --user andresionek`: last run 2018-10-24); it is cited in issue 1, in a new "Task choice" bullet of `curation_comments` and in the record comment, with the note on the answered-survey selection. Delivery time stays implemented.
2. The gap matters because models see the purchase time as a number: applied. `splits_comment`, the decision text and the "Split:" bullet now say "as a number"; the bullet and issue 3 carry the verifier's 5-window numbers (I read its script and logs: shipped frame and splits, 300 trees).
3. "96.7% of the orders hold one distinct product": applied, recomputed on the shipped frame (86,903 of 88,721 = 97.95%) -> "98.0% of the kept orders" (in `curation_comments` and issue 5).
4. "the effect is the same in every month" stated as fact: applied -> "We assume ...; the release holds no unanswered surveys to check it."
After the edits: ruff clean; `dataset check` 0 errors, 0 warnings (same accepted warning and info); checksum now v2:5e0a3d4e... (the comment text is part of the metadata), the same under pandas 2.3.3 and 3.0.6; `pytest tests/test_v2_datasets.py -k brazilian_ecommerce` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed. Data, rows and splits unchanged.

**Resolved (Lennart, 2026-10-15):** ship as implemented: delivery time at checkout, the one-month gap, Olist's promised date as an input, the answered-review selection as an `Anomaly:` bullet (issues 1, 3, 5 and 7 as answered above).

### breast_cancer_prediction

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/breast_cancer_prediction/`). Revised after verification on 2026-10-07.

**Record judgment:** valid with concerns. The data is the BCSC Digital Mammography Dataset: "a random sample of 20,000 digital and 20,000 film-screen mammograms performed between January 2005 and December 2008 from women in the Breast Cancer Surveillance Consortium" (https://www.bcsc-research.org/index.php/datasets/mammography_dataset, Overview).
- First publication: the BCSC listed it in 2014 on its NCI site (breastscreening.cancer.gov/data/mammography_dataset/; Wayback from 2014-08-26, page "Last modified: 09 Jul 2014"). The BCSC's `dataset.csv` is dated 2014-06-04.
- Predictive task, as the source names it: "Construct a model to predict occurrence of any cancer using patient characteristics and mammography assessment. Which patient characteristics provide additional information beyond mammography assessment?" (https://www.bcsc-research.org/index.php/datasets/mammography_dataset/example_question, "Specific questions to answer", item 4).
- No duplicate: nothing in the working copy and no other record cites BCSC, OpenML 43687 or the Kaggle slug. `mammography` (OpenML 310, retired as Image) is different data.
- The concerns are issues 1-4.

**Data:**
- Source: the BCSC's own file. The download page that follows the BCSC's registration form links a zip (sha256 `182efaa1...f072`). Its single `dataset.csv` (2014-06-04, 40,000 rows x 13 columns, sha256 `5f7378e7...8c90`) is byte-identical to `local-data-warehouse/breast_cancer_prediction/mammography.csv`.
  - I first took the file from a GitHub copy (lintai666/mammography @ 2f35ca3b, pinned); the BCSC file was checked against it on 2026-10-07.
- Kaggle (haithemhermessi, 2020) and OpenML 43687 (and so TabSTAR) are the same file without the two exact duplicate rows, with decoded labels. All 39,998 rows match one to one.
- Licence as stated:
  - the BCSC page names no licence;
  - it requires an acknowledgement and says "These data are recommended for use as a teaching tool only; they should not be used to conduct primary research";
  - Kaggle states CC0-1.0 and OpenML "CC0: Public Domain".

**Definition:**
- Prediction point: the screening mammogram has just been read. The BI-RADS assessment and density, the intake answers and the exam facts are known. The label is a breast cancer diagnosis (DCIS or invasive) within one year, from registry linkage.
- Target and metric: `cancer_within_one_year` (259 of 39,998 exams, 0.65%), scored with ROC AUC.
- Regime: grouped by `patient_id` (the BCSC's `ptid`; 36,714 women; one label per exam; prediction unit row; context none).
- Splits: 3 repeats x 3 folds; train 26,634-26,689 rows, test 13,309-13,364 rows, 76-99 cancers per test fold.
- Shape: 39,998 rows x 10 features.
- Cleaning:
  - rename the codebook columns;
  - drop the 2 exact duplicate rows;
  - drop `CaTypeO`, which encodes the label;
  - make the assessment a category labelled with its BI-RADS number;
  - keep density 1-4 numeric;
  - set the codebook's 9 to NaN in the yes/no answers and -99 to NaN in BMI.
- pandas 2.3.3 and 3.0.6 give the same checksum, `v2:da175f31...cfc1` (shared pd3 venv).

**Checks:** `dataset check` gives 0 errors, 0 warnings, 2 accepted warnings and 1 info.
- `dataset_pure_feature_value`, accepted: BI-RADS 1 and 2 and density 1 are low-risk categories at a 99.35% base rate.
- `groups_labels_constant`, accepted: the 20 groups with two labels are the 20 multi-exam women with cancer.
- `groups_not_clustered` (info): the use case decides the split.
- pytest for the folder passes (2 tests, with `DATA_FOUNDRY_V2_DATA_CHECKS=1`), and ruff is clean.

**Probes:**
- Task probe: flag `one_feature`. The assessment alone gives AUC 0.907; regularised LightGBM 0.930, CatBoost 0.929 and random forest 0.925 beat it on 9 of 9 splits (+0.019-0.023, standard error 0.003-0.004). Not `Trivial` by rule 4. A depth-3 tree reaches 0.915.
- Leak probe (`leak_probes.py` as fixed, which leaves the group column out):
  - assessment alone 0.911;
  - every other feature at most 0.558, every missing-value indicator at most 0.524;
  - exact feature copies across the split: 49.4%. These are distinct women with identical coarse profiles. The grouped split keeps each woman on one side, and the 1-NN label agreement is 0.989 against 0.987 by chance.
- Generated-data probe: no flag.
- Group probe: random split 0.906 against grouped 0.914.
- Without the readings (correcting the first report): without the assessment, logistic regression reaches 0.587, regularised LightGBM 0.579-0.585 and CatBoost 0.560, above 0.5 on 9 of 9 splits. Without the assessment and the density: logistic regression 0.578, LightGBM 0.555-0.562 (9 of 9), CatBoost 0.530 (8 of 9). Sources: `probes/no_readings_check.txt` and `verify/feature_sets.txt`.

**Issues for Lennart:**

1. **Does the image-scoring rule (breast_w) cover the BI-RADS readings?**
   - For exclusion: the guidelines say "A human *scoring what they see in an image* is still an image feature" (breast_w). The assessment (suspicion) and the density (tissue) are a radiologist grading the mammogram, and they carry the task: assessment alone 0.907, all features 0.930.
   - For keeping:
     - the working copy keeps `heart_disease_cleveland` with `thal` (thallium scan) and `ca` (vessels coloured by fluoroscopy);
     - the BCSC published the file without images ("This dataset does not include images") for exactly this question: the risk beyond the assessment;
     - the assessment is the clinical result of the screen, not a description of image content that a vision model would replace.
   - Now: kept; the verifier leans the same way.
   - Fallback if you rule against the readings: the readings-free task (patient and exam facts only), close to the BCSC's risk-model framing. Logistic regression reaches 0.578 there, above 0.5 on 9 of 9 splits: a small, real signal (rule 2), not a `No`.
   - Either way a dated `CC` decision in the record would settle it.

   **Resolved (Lennart, 2026-10-15):** kept. The readings are valid tabular inputs: screening programmes run tabular risk models on BI-RADS readings and risk factors, so the image-scoring rule does not apply; the real-world use decides. The exception is now in the curation guidelines (and their dashboard copy).
2. **Grouped by woman, or IID as the record says?**
   - `ptid` is the source's patient id. 3,133 of 36,714 women have 2-4 exams, and only the 20 with cancer have a positive exam, their last.
   - A random split gains nothing (0.906 against 0.914 grouped).
   - Now: grouped. The exams are a random sample of the BCSC's screening mammograms, so a model is used for other women, and your comment flagged the repeated women.
   - Alternative: IID, with the same scores. The verifier agrees with grouped.

   **Resolved (Lennart, 2026-10-15):** IID with one exam per woman, her earliest in the sample (lowest age; two age ties keep the file's order): 36,714 rows, 239 of the 259 cancers (the 20 women with cancer and several exams are positive only on their last exam). Untuned LightGBM scores alike either way (ROC AUC 0.928 earliest, 0.923 latest, 0.925 all exams grouped; script in the run folder of 2026-10-15). Regularised LightGBM 0.929 and a random forest 0.927 beat the assessment alone (0.914) on 8 of 9 splits. The repeated feature vectors (52.2% of the rows, different women) are now an accepted `dataset_duplicate_rows` warning.
3. **Print the BCSC's direct download link?**
   - `https://www.bcsc-research.org/download_file/view/33/347` (HTTP 200 today; on the post-form page in Wayback 2021 and 2024) returns the original zip without the name / institution / e-mail form.
   - Now: `download_description` describes the form route (zip and CSV sha256, `unzip -p`), keeps the GitHub copy as a pinned mirror, and does not print the link.
   - Alternative: print it, which makes the original download scriptable.

   **Resolved (2026-10-15, Lennart left it open):** not printed. The BCSC asks users to register before downloading; the pinned GitHub copy (same sha256) already makes the download scriptable.
4. **Terms (noted, not a verdict reason).** "Recommended for use as a teaching tool only; they should not be used to conduct primary research". The P01CA154292 acknowledgement ("must be cited when reproducing this data") is now in the bibtex note, with the download date 10/07/2026.

5. **Target.** Now binary any-cancer (the source's question 4). The alternative is three classes from `CaTypeO` (none / DCIS 56 / invasive 203), about 19 DCIS per test fold.

6. **Record fields (the orchestrator's job).**
   - `year` 2020 → 2014;
   - `original_source` Kaggle → GOV Website;
   - the dead datahub link → the BCSC page;
   - `required_split` and `tags` per issue 2;
   - `v2_path`.

   **Resolved (Lennart, 2026-10-15):** applied: `year` 2014, the dead datahub link replaced by the BCSC page; `original_source` was already GOV Website; `required_split` and `tags` stay IID (issue 2); `v2_path` is set. The review page's labels now say what a mark does ("take definition's value" / "keep record's value"), and record fields go only into the field table, never into a numbered issue (review-added-datasets skill).
7. **For comparisons with TabSTAR.** TabSTAR's version (`BIN_HEALTHCARE_BREAST_CANCER_MAMMOGRAM.py`, `COLS_TO_DROP = []`) keeps `Cancer_Type`, which gives the label away.

   **Resolved (Lennart, 2026-10-15):** noted only; another collection's version of the data is no reference (now a rule in the skills).
8. **Framework.**
   - (a) `leak_probes.py` used the group column as a feature; the orchestrator has fixed it.
   - (b) `generated_probes.py --root` fails when any folder does not import.
   - (c) The task and group probes' linear models read categories as codes. With plain BCSC labels the linear probe scored 0.587; with the BI-RADS-number prefix it scores 0.80.
   **Resolved (Lennart, 2026-10-15), applied:** (a) fixed on 2026-10-07; (b) the probes load only the named folder, and `--all` skips folders that do not import; (c) the linear models of the task and group probes one-hot encode categories (at most 64 levels each): the linear probe now scores ROC AUC 0.922 here.

**Verification:** (verifier, 2026-10-07: needs changes, text only; container correct)
- Finding 1 (image rule, major): applied. Now issue 1, with both sides, the heart_disease_cleveland precedent and the readings-free fallback. A short pointer to the precedent is in the assessment bullet of `curation_comments`.
- Finding 2 (fallback mis-stated, major): applied. I checked it myself (`no_readings_check.py`): logistic regression 0.587 / 0.578, above 0.5 on 9 of 9. The comment now says the signal without the assessment is small but real, and that the untuned probe's 0.500 is overfitting. Issue 1 names the readings-free task as the fallback.
- Finding 3 (BCSC file, minor): applied. I fetched the link once myself: zip sha256 `182efaa1...f072`, `dataset.csv` sha256 `5f7378e7...8c90`, identical to ours. `download_description` now leads with the BCSC route, keeps GitHub as the mirror, and drops "We could not fetch it there". Printing the direct link is issue 3.
- Finding 4 (acknowledgement, minor): applied. The P01CA154292 sentence with "Downloaded 10/07/2026" is in the bibtex note, next to the HHSN261201100031C text.
- Finding 5 (record comment, minor): applied. It now says the 20 women with cancer are positive only on their last exam, and that the file is the BCSC's own.
- Finding 6 (record fields): left to the orchestrator (issue 6).
- Finding 7 (leak probe): re-ran the fixed `leak_probes.py`: 10 features, 49.4% exact copies. The leak-probes bullet now says what the copies are: distinct women with identical coarse profiles, never the same woman across the grouped split, 1-NN agreement at chance.

**Resolved (Lennart, 2026-10-15):** ship.

### caracas_cervical_cancer
**Outcome:** added and checked (revised after verification: 108 patients dropped, source fills set to NA)

**Record judgment:** valid with concerns. Source: UCI 383 (DOI 10.24432/C5Z310, CC BY 4.0), from the creators'
papers.
- Fernandes, Cardoso & Fernandes, IbPRIA 2017: the data serves "to predict the individual patient's risk when
  multiple screening strategies are available" (Sec. 3.1, p. 247).
- Fernandes, Chicco, Cardoso & Fernandes, PeerJ Comput. Sci. 4:e154, 2018: the biopsy predicted "where only
  behavioral and demographic information is observable" (Results). The cohort is "a random sampling of patients
  between 2012 and 2013 who attended the gynecology service at Hospital Universitario de Caracas" (Dataset).

Unique: no folder of the working copy and no other record holds this data; grep for cervical, Hinselmann, Schiller,
C5Z310, 46592 and risk_factors finds only this record. OpenML 46592 (2025) is a re-upload whose target ORs the four
tests. The paper's data page (vcmi.inescporto.pt) no longer resolves. Main concern: the 108 patients who skipped the
contraceptive question look unexamined (issue 1).

**Data:** one file from the UCI static zip
`https://archive.ics.uci.edu/static/public/383/cervical+cancer+risk+factors.zip`:
`risk_factors_cervical_cancer.csv`, 858 rows x 36 columns, md5 47f4cde87fb017ae0944847cb1c36fc4. The verifier found
the same md5 in the first author's GitHub. Unanswered questions are "?". Licence CC BY 4.0, stated on the UCI page.

**Definition:** `datasets/_dev/tabarena-v0pt2/caracas_cervical_cancer/`.
- Prediction point: risk assessed from the questionnaire, before any screening result is known (the 2018 paper's
  first setting).
- Target `biopsy`: 55 positive of 750 (7.3%).
- IID, default splits: 10 repeats x 3 folds, 500 train / 250 test rows, 18 positives in the smallest test fold.
- 750 rows x 30 features: 18 binary categorical, 12 numeric.
- Cleaning:
  - "?" becomes NaN.
  - The 108 patients who skipped the contraceptive question are dropped.
  - The source's 3 fill values (27 values in the kept rows) and the default 0 diagnoses of the 10 STD skippers are
    set to NaN.
  - Hinselmann, Schiller and Citology are dropped, as are the 2 never-positive STD flags.
  - Columns are renamed without colons; their order is kept.
  - The multi-hot STD and Dx flags are kept, and so are the repeated profiles.
- pandas 2.3.3 and 3.0.6 give the same checksum (v2:5a2da137...).
- Three `_decisions` with tables.

**Checks:** 0 errors, 0 warnings, 1 info (`dataset_conflicting_duplicate_rows`, 1 row). Accepted:
`dataset_duplicate_rows`, 21 exact copies (2.8%). They are 17 coarse profiles of patients aged 15-34, 5-439 rows apart
in the file. Recombining answers within the same age and history gives 20 repeats on average (16-25), against 22
observed. Pytest passes (2 passed with `DATA_FOUNDRY_V2_DATA_CHECKS=1`), the class imports, ruff is clean and no
TODO is left.

**Probes** (outputs in `probes_v2/`; the 858-row run is in `probes/`):
- Leak:
  - All features 0.661; depth-2 / depth-3 tree 0.523 / 0.542.
  - Best single feature `age` 0.621; best missing indicator 0.56.
  - Dropping any of the top 3 features costs at most 0.03.
  - 4.8% of test rows have an exact copy in train.
  - 1-NN label agreement 0.960 / 0.904 against chance 0.864.
  - The label-free NN distance scores 0.707, above the untuned models; answered in a `Note:` bullet. Positives are
    isolated (median 1.66 vs 0.67), their nearest neighbour is positive in 16% at a 7% base rate, the distance
    follows the number of nonzero answers (Spearman 0.57), it holds within age bands (0.63-0.79), and there are no
    rule leaves. This is the questionnaire's risk load.
- Task: no flags.
  - Random forest AUC 0.678 (skill 0.355, SE 0.014, above the dummy on 30 of 30 splits).
  - LightGBM 0.616, linear 0.564, single feature 0.558.
  - Spread RF - linear +0.227 (SE 0.020).
- Generated: no flags. Hidden groups: no hits (`age`, `age_first_sexual_intercourse` checked).

**Issues for Lennart:**
1. **Drop or keep the 108 patients who skipped the contraceptive question? Implemented: dropped.**
   - None of them has a positive biopsy, Hinselmann or Schiller result, where 8, 5 and 11 are expected (any of the
     three: 0 of 11.8, P = 4e-6). Cytology still finds 2 of 6 expected.
   - Their answers show no lower risk: 16.5% smokers vs 14.3%, first intercourse at 16.2 vs 17.1 years, and 6 of the
     13 who answered the STD questions report an STD.
   - The creators expected skipping to mean "risk behaviors" (PeerJ 2018, Dataset).
   - The 16 who answered this question but skipped IUD or STD have 4 positive biopsies.
   - When kept, these rows raise LightGBM from 0.60 to 0.65 on the shipped splits (30 of 30).
   - Alternative: keep the 858 rows. The bullet would then have to say that IbPRIA's answered-or-not indicator does
     not cover this question, and that the creators expected higher risk.
   - Open for the whole file: whether a 0 means "test not done". 6 positive biopsies have all three screening tests
     negative, so biopsies were not taken only after a positive screen. The first author (INESC TEC) could be asked.
   **Resolved (Lennart, 2026-10-15):** dropped, as implemented.
2. **Target: biopsy, as the record suggests.** The creators' own 2018 target, and the strongest signal from the
   questionnaire. Alternatives, as LightGBM / logistic AUC on 858 rows:
   - Schiller: 74 positives, 0.64 / 0.63.
   - Hinselmann: 0.55 / 0.60.
   - Citology: 0.55 / 0.58.
   - Any test positive: 0.62 / 0.67.
   **Resolved (Lennart, 2026-10-15):** the biopsy, as implemented.
3. **One-hot reversal not done.** The STD and Dx blocks are multi-label: 43 of 740 patients have 2-4 STD types, and
   16 of 18 previous cancer diagnoses carry HPV. Alternative: combination categoricals, with 14 STD levels (9 of them
   with 1-3 rows) and 5 Dx levels.
   **Answer (AI, 2026-10-15):** kept as one yes/no category per flag. Each flag is a question of the questionnaire, and they are multi-label: 9 patients have two or three STD types (the 43 above counted condylomatosis twice: `std_condylomatosis` is exactly the OR of the vaginal and vulvo-perineal types, and `stds_number` is the sum of all ten flags). A single category would need 14 levels, 9 of them with 1-3 patients (issue 3 above), and a string column would be read as free text. `stds` and `stds_number` are derived from the flags and stay as the source counts them.
4. **Repeated answer profiles kept** (21 exact copies plus 1 copy with the other label). The alternative, dropping
   them as in wine_quality, would leave 729 rows.
   **Resolved (Lennart, 2026-10-15):** kept, as implemented.
5. **Record fields.**
   - `problem_type: TBD` should become Binary Classification.
   - `v2_path` gets filled by `sync-notebooks`.
   - The `Multi-target` tag stays: the four tests can be modelled jointly (IbPRIA Table 2). The folder ships the
     biopsy only.
   **Resolved (Lennart, 2026-10-15):** the `Multi-target` tag is removed: the four results come from one work-up and the folder predicts the biopsy alone. `problem_type` was already Binary Classification and `v2_path` is set.
6. **Anomalies, kept as recorded.**
   - 2 patients report a first intercourse after their current age.
   - 2 patients report an STD diagnosis longer ago than their age.
   - 5 patients have a `dx_*` flag set while `dx` is 0.
   - 7 patients report an STD with no STD diagnosis counted.
   - `smokes_packs_per_year` keeps the source's name, although it reads as pack-years.
   **Answer (AI, 2026-10-15), applied:** impossible answers become missing, the rows stay: the 2 first intercourses after the current age (ages 23 and 14 with 27 and 16) and the 2 STD diagnoses longer ago than the patient's age (21 years at 20, 19 at 18); the age is the clinic's record. The other contradictions are not impossible and stay as recorded: `dx` (undefined by the source) is 0 for 5 patients with a `dx_*` flag, and 7 report an STD with 0 diagnoses counted, which may count clinical diagnoses where the flags are self-reports. Rows and splits are unchanged.

**Verification:**
- Finding 1 (major, drop the 108): applied. I re-checked the counts and P-values, the covariates and the 4 of 16, and
  the PeerJ quote. On the shipped splits I measured LightGBM 0.646 vs 0.603 and RF 0.684 vs 0.655, higher on 30 of
  30. Keeping the rows is now issue 1's alternative.
- Finding 2 (source fills): applied. These three values are the only answers with more than 3 decimals in their
  columns, and all sit in rows that answered "yes": 12, 13 and 2 of them in the kept rows. They are set to NA, with a
  bullet.
- Finding 3 (default 0 diagnoses): applied, with NA for the 10 remaining STD skippers. The 787 wording became 667
  reported none, 7 reported an STD without a diagnosis, and 10 skipped; the 7 are also in the Anomaly bullet.
- Finding 4 (PeerJ 2018): applied. It is in the bibtex, the opening, the prediction-point and target bullets, and the
  "?" quote. The hospital is now cited to PeerJ.
- Finding 5 (wording): applied. The expected counts are now "8, 5 and 11", and the record comment no longer claims
  an answered-or-not signal for this question.
- Finding 6 (Multi-target tag): applied. Issue 5 now keeps the tag and says the folder ships the biopsy only.

**Resolved (Lennart, 2026-10-15):** ship as implemented (issues 3 and 6 as answered above).

### cdc_diabetes_health_indicators

**Outcome:** added and checked. Retired as `No` (`No Good Target / Scientific Discovery`) on 2026-10-15: the task predicts a diagnosis the respondent already has (issues 1 and 4); the folder is removed and stays in git history at bb3baa3.

**Record judgment:** valid with concerns. The provenance is clear and verified. The file is Alex Teboul's Kaggle cut
(files of 2021-11-08, CC0) of the CDC's BRFSS 2015 telephone survey. His public notebook, run on the CDC's 2015.csv
(Kaggle `cdc/behavioral-risk-factor-surveillance-system`, 441,456 respondents), reproduces the published CSV row for
row, and the 253,680 rows are distinct respondents (unique `_STATE`, `SEQNO`).

The dataset is unique:
- No BRFSS-derived dataset is in the working copy, and no other record of this run uses BRFSS.
- `diabetes_2` (TableShift BRFSS diabetes) and `hypertension` (TableShift BRFSS) are already `No` + `Duplicate` of this
  record.
- UCI 891 and OpenML 46598 are mirrors of Teboul's binary file.
- Teboul's own "Heart Disease Health Indicators Dataset" (`alexteboul/heart-disease-health-indicators-dataset`,
  2022-03-10) is the same BRFSS 2015 cut with another target. It has no record; by the duplicate rule it would be
  `No` + `Duplicate`.

It is in scope: a published predictive task (Xie et al., Prev Chronic Dis 16:190109, 2019, on BRFSS 2014). The concerns
are the label and the cohort (issues 1 and 2); the record settles both for now.

**Data:**
- Source: Kaggle `alexteboul/diabetes-health-indicators-dataset` (one version, files of 2021-11-08).
- File: `diabetes_012_health_indicators_BRFSS2015.csv` (sha256 `a971809d0786d2d7…8f9861`), 253,680 rows x 22 columns,
  in `local-data-warehouse/cdc_diabetes_health_indicators/`.
- Licence: CC0-1.0 (Kaggle data card, `licenses` field). BRFSS data are CDC public-domain material
  (cdc.gov/other/agencymaterials.html, as cited in the `diabetes_2` record).
- Verification only: the raw 2015.csv (541 MB, Kaggle `cdc/...`) and the codebook (2015 Codebook Report, LLCP, 23 Aug
  2016, from the Wayback Machine because cdc.gov returns 403) are in my scratch folder. The definition does not read
  them.

**Definition:** `datasets/_dev/tabarena-v0pt2/cdc_diabetes_health_indicators/`
- Prediction point: a screening questionnaire. When an adult answers the BRFSS interview, the model estimates from the
  other answers of that interview whether they have been told they have diabetes or prediabetes. The cohort is the
  adults whose cholesterol was checked at least once and who answered all 22 selected questions.
- Target: `Diabetes`, three classes (the record's choice): No diabetes 213,703, Prediabetes 4,631, Diabetes 35,346
  (any type). Metric: log loss.
- Regime and splits: IID, 3 repeats x 3 folds, 169,120 train / 84,560 test rows.
- Size: 253,680 rows x 21 features.
- Cleaning: the file as published. Features are cast from float to int, `Sex` is mapped to Female/Male (categorical) and
  the label to names. The ordinal codes (GenHlth, Age, Education, Income) stay numeric, and duplicates are kept.
- `_decisions` gives two tables: the label versions, and the duplicates by class.
- The container checksum is the same under pandas 2.3.3 and 3.0.6 (`v2:926471ee…79e7806b` after the verifier's edits,
  checked in a scratch venv).

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 1 info.
- Accepted: `dataset_duplicate_rows` (23,899 rows, 9.4%). Each row is a different respondent (verified on the raw file),
  so identical answers to 21 coarse questions are natural.
- Info `dataset_conflicting_duplicate_rows`: 1,873 rows repeat a feature vector with another label. That is 1,834
  vectors, 6,120 rows in all: genuine ambiguity between different people.
- `pytest tests/test_v2_datasets.py -k cdc_diabetes_health_indicators`: 2 passed with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- ruff is clean, and no TODO is left.

**Probes:** all run at 2 threads after the coordinator's cap. The task probe uses 5 of 9 splits; the leak probe 3 splits
of at most 50k rows.
- Task probe, no flags:

  | model | log loss | skill |
  |---|---|---|
  | dummy | 0.491 | 0 |
  | LightGBM | 0.398 | 0.190 |
  | linear | 0.400 | 0.187 |
  | random forest | 0.407 | 0.171 |
  | single feature (GenHlth, all 5 splits) | 0.445 | 0.095 |

  The best family beats the dummy on 5 of 5 splits (standard error 0.001). The spread is 0.019 (paired SE 0.002). The
  smallest test class has 897 rows in the probe's capped folds.
- Leak probe, macro one-vs-rest AUC: all features 0.772. Depth-2 and depth-3 trees reach 0.714 and 0.738.
  - Single features: GenHlth 0.694, HighBP 0.660, BMI 0.659, Age 0.632, HighChol 0.629, Income 0.621.
  - Without GenHlth, HighBP or BMI the score is 0.760, 0.768 and 0.757.
  - There are no missing values.
  - 6.7% of test rows have an exact copy in train.
  - 1-NN label agreement: 0.915 for the closest tenth and 0.777 for all, against 0.729 chance.

  No column carries the label. The copies are common low-risk profiles: the 38,000 rows with repeated profiles are 94%
  No diabetes, which gives a chance agreement of 0.886 among them. They are not one person copied.
- Generated probe: 0 rule leaves, no flag.
- Hidden groups: one candidate, BMI (84 values, gap 0.033), no hit. BMI is a measurement every new respondent has, so no
  action.
- `tuned_results.py` was skipped as the brief says.

**Issues for Lennart:**

1. **The label: three classes, or binary "ever told diabetes"?** The record chose 3 classes over "0 = no diabetes, 1 =
   prediabetes & diabetes", as "more native to the real world problem and less biased". That binary is not the one on
   offer.
   - Teboul's binary files are diabetes against the rest, with prediabetes in class 0 (218,334 / 35,346 rows). Notebook
     cell 48: "Change the diabetics 2 to a 1 and pre-diabetics 1 to a 0".
   - The Kaggle card, UCI 891's variable table and the record say "1 = prediabetes or diabetes". UCI 891's CSV is that
     binary file with a row-number ID, row for row. OpenML 46598, imported from UCI 891, lists three class labels for a
     binary target.
   - TableShift's BRFSS target is the same binary, with pre-diabetes and gestational diabetes mapped to 0 (`diabetes_2`
     record, CC 2026-09-23). Xie et al. 2019 (Methods, Data analysis) is type-2 diabetes against the rest, with
     prediabetes and ages below 30 left out.
   - The Prediabetes class is a narrow, noisy subset. Code 4 is recorded only when the respondent volunteers it: "If
     Respondent says pre-diabetes or borderline diabetes, use response code 4" (2015 codebook, p. 21).
   - In the 15 states that asked PREDIAB1 (p. 50), only 1,072 of the 5,215 kept respondents told they have
     prediabetes are in the class; 4,143 are labelled No diabetes. Per state the share in the class is 14% to 23%
     (median 21%; reproduced by the verifier and by me).
   - Untuned LightGBM, 3 folds, one-vs-rest AUC: Prediabetes 0.700 (0.751 against No diabetes alone), Diabetes 0.830.
     The 3-class log loss is 0.393 against a prior of 0.492.
   - Implemented: 3 classes, as the record decided.
   - Alternative (my recommendation, the verifier's too): binary "ever told diabetes" against the rest, prediabetes
     counted as no diabetes. ROC AUC 0.829-0.830; one clean survey question. Or Xie's cohort: 235,826 rows, AUC 0.827.
   **Resolved (Lennart, 2026-10-15):** neither: retired as `No`, `No Good Target / Scientific Discovery` (Outcome). The label is a diagnosis the respondent already has, in either version.
2. **The cohort: the drop of blanks is partly a skip pattern, not refusals.** The record accepted the drop as keeping
   "only cases that answer the questions truthfully and fully".
   - TOLDHI2 is not asked when cholesterol was never checked (p. 17). All 49,673 never-checked respondents are
     excluded: 51% of the 97,850 rows the drop of blanks removes. 2.8% of them have diabetes, against 13.0% of all
     respondents.
   - The other blanks are mostly BMI (36,398, overlapping). Income "don't know/refused" then removes 34,251 more rows,
     and physical activity "don't know" 15,397.
   - Partial interviews go too: 23.7% of 66,397 are kept, against 63.4% of complete ones (DISPCODE 1200 and 1100).
   - Overall 441,456 → 253,680. The class shares move little: diabetes 13.0% → 13.9%.
   - Implemented: as published, with the cohort now named in the prediction-point bullet.
   - Alternative: a version rebuilt from 2015.csv, with "never checked" and "income unknown" as categories. The notebook
     reproduction makes this easy; the record wants a domain expert first.
   **Resolved (Lennart, 2026-10-15):** moot: retired (Outcome); a cohort rebuilt from the raw file keeps the same label.
3. **Duplicates kept (accepted warning).** 23,899 exact duplicate rows, all distinct respondents.
   - Precedent: sepsis_survival keeps natural repeats. wine_quality and jm1 drop copies, but theirs are one entity or an
     artifact. The verifier agrees (§D.4, "few features, plausible repeats: keep").
   - Dropping exact copies would remove 23,648 No diabetes rows and 249 Diabetes rows, which reweights the common healthy
     profiles.
   - Implemented: keep.
   - Alternative: drop exact copies and conflicting vectors.
   **Resolved (Lennart, 2026-10-15):** moot: retired (Outcome).
4. **The design is cross-sectional (note, no action proposed).** The label is a lifetime diagnosis.
   - Kept diabetics were told a median of 10 years before the interview (75% at least 5 years).
   - Without the care-contact, lifestyle or complication answers, the ROC AUC of diabetes against the rest drops by at
     most 0.0014 from 0.829. Without HighBP and HighChol it drops by 0.014, and without health status by 0.018.
   - Age, Sex, Education, Income, Smoker and BMI alone give 0.772.
   - Undiagnosed cases sit in No diabetes. The data card says "1 in 5 diabetics, and roughly 8 in 10 prediabetics are
     unaware".
   - The Kaggle notebook jabr1one/the-problems-of-this-dataset (2025) raises this. Xie et al. use the same
     cross-sectional design.
   **Resolved (Lennart, 2026-10-15):** this decides it: the task is retired (Outcome). The screening use needs the undiagnosed as positives, which BRFSS cannot identify; NHANES can (new candidate `nhanes_undiagnosed_diabetes`).
5. **Source convention (minor).** `source = "Kaggle"` stays, by §A ("where the data first appeared").
   - This table first appeared on Kaggle; the CDC publishes only the raw survey.
   - Same call as `sdss_17`: a Kaggle user's cut of the SDSS DR17 release, with source "Kaggle" and BibTeX citing the
     data release. Unchanged re-uploads take the original host instead (`sepsis_prediction_1m`, `emscad`: "Other").
   - By this rule, this run's `nyc_taxi_trip_duration` (Kaggle's sampled and cleaned cut of TLC records, now
     `"GOV Website"`) would be "Kaggle" too. That folder is not mine; one rule for both is Lennart's call.
   - BibTeX: Teboul's dataset, with BRFSS in the note. Alternative: the CDC's BRFSS 2015 citation, as sdss_17 cites
     DR17.
   **Resolved (Lennart, 2026-10-15):** moot: retired (Outcome).

**Verification:** the independent verifier found no blocker ("ready with noted concerns"), and every number
reproduces.
- Finding 1 (label, major): issue for Lennart. The 3 classes stay as the record decided. Merged into issue 1 with the
  per-state shares, which I reproduced (13.9-22.8%, median 21%). The curation_comments note now gives them.
- Finding 2 (cohort): applied. The prediction-point bullet names the cohort, and the Cohort bullet gives the 51% of the
  drop. The rebuild from 2015.csv stays issue 2.
- Finding 3 (post-diagnosis numbers): applied in the prediction-point bullet, after I re-ran the verifier's script (same
  numbers) and the years since diagnosis (median 10, 75.1% at least 5 years, 34,119 diabetics). No column change.
- Finding 4 (wording): applied. "the cross-sectional framing of Xie et al.", and "any type, as BRFSS does not ask
  which, 218 of them aged 18-29" (reproduced) in the target bullet.
- Finding 5 (source convention): applied as a decision. `source = "Kaggle"` is kept with a one-line comment on the
  attribute (the sdss_17 rule); the nyc_taxi_trip_duration inconsistency is in issue 5.
- After the edits: `dataset check` 0 errors / 0 warnings / 1 info, ruff clean, the same checksum under pandas 2.3.3 and
  3.0.6 (`v2:926471ee…`), and pytest 2 passed with the data checks on.

Framework notes (not for the record):
- `discover_datasets` in the probe scripts and in `tests/test_v2_datasets.py` imports every folder of the root. Another
  agent's half-written folder (`alfa_battle_2_0_task_2`, `fraud_detection_..._1m`) crashed my first probe and pytest
  runs. I ran the probes on a scratch root holding a symlink to my folder; pytest passed later.
- `leak_probes.py` hard-codes `n_jobs=8` for LightGBM, which the `OMP_NUM_THREADS` cap does not override.
  `OMP_THREAD_LIMIT=2` does. At 8 threads under load 300 the probes stalled for 30+ minutes; at 2 they took 2-4
  minutes.

### central_international_medical_college_and_hospital_health_risk_prediction

**Outcome:** added and checked, in `datasets/_dev/tabarena-v0pt2/central_international_medical_college_and_hospital_health_risk_prediction/`. It was added because the record accepted the triviality risk for now ("Target variable might be noisy/fake and thus the task might be trivial. We will see post hoc."). The evidence says it should not ship (Issue 1).

**Record judgment:** do not add. The label is a deterministic rule of the features, so the task is a lookup:
- Criterion 4C (Trivial): "one feature or a simple rule gives the score the best methods reach, or the task is solved perfectly".
- `leak_checks.md` §3: "Target is a lookup of the inputs → retire (`Trivial`, often `AHDS`)".

`Risk_Level` equals the NEWS2 band computed from the eight features in 1,000 of 1,000 rows. The rule comes from three Royal College of Physicians 2017 charts (downloaded from rcp.ac.uk):
- Chart 1, "The NEWS scoring system", gives the points per parameter.
- Chart 2, "NEWS thresholds and triggers", gives the bands: "Aggregate score 0–4 Low", "Score of 3 in any individual parameter Low–medium", "Aggregate score 5–6 Medium", "Aggregate score 7 or more High".
- Chart 4 adds a separate row for a total of 0.

The dataset's mapping is: total 0 is Normal, 1-4 is Low, a 3 in a single parameter or a total of 5-6 is Medium, and 7 or more is High. The match is exact when the SpO2 scale-2 points for 93% or more are also given on air. With Chart 1's "on oxygen" condition, 987 of 1,000 rows match.

The vital signs also look generated (criterion 4B, Issue 2). The record's comment accepted this risk, so the dataset is added and this is the counter-argument.

**Data:**
- Source: Kaggle `ludocielbeckett/health-risk-prediction-anonymized-real-data`, version 1, uploaded 2025-08-24. It is the only version; version 2 returns 404.
- File: `Health_Risk_Dataset.csv` (sha256 `def34f7c98d3c580be348052856ef494b8ffb690684af3fc5546eb94edee0cec`), 1,000 rows x 10 columns, no missing values, no duplicate rows. It is in `local-data-warehouse/central_international_medical_college_and_hospital_health_risk_prediction/`.
- Licence: Apache 2.0, from the Kaggle metadata "licenses".
- Provenance:
  - The only statement is one sentence in the data card's sources field: "This Data was collected from Central International Medical College and Hospital. The data is of patients who were admitted to the ICU and the Medical Ward."
  - There is no paper, collection period, ethics approval or description of how the labels were set.
  - The dataset has no discussion threads, and it is the uploader's only dataset (Rakibul Alam).
  - The home page of dcimch.com (a private 500-bed hospital in Shyamoli, Dhaka) mentions no data release.
- Uniqueness: no other record, run record or working-copy folder holds this data. The Kaggle slug, file name, NEWS2 and dcimch were all grepped. `maternal_health_risk` is the UCI maternal-vitals set, a different source.

**Definition:**
- Prediction point: a bedside observation round in the ICU or a medical ward, when the seven NEWS2 parameters have just been measured.
- Target: `Risk_Level` (Normal 160, Low 255, Medium 306, High 279). Multiclass, scored with log loss.
- Regime and splits: IID, the default 10 x 3-fold CV (train 666-667 rows, test 333-334). Each row is a different patient, and the file has no time or ward column.
- Size: 1,000 rows x 8 features.
- Cleaning:
  - `Patient_ID` is dropped. It is unique per row and numbered in blocks of the label (P0001-P0160 all Normal, P0161-P0415 Low, P0416-P0721 Medium, P0722-P1000 High), so it would give the label away.
  - `Consciousness` codes are mapped to the data card's words and kept as a category.
  - `O2_Scale` (1/2) and `On_Oxygen` (0/1) stay numeric.
- `_decisions`: three tables, which the README renders:
  1. the NEWS2 band against the label, under both readings of scale 2;
  2. the id blocks;
  3. the dependence of the vitals within each class.
- Same checksum under pandas 2.3.3 and 3.0.6: `v2:9eddf51a4025e3c5881e1188e4832a87f75f2b6c640fba955afbcabcd3b3626f`.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). Nothing needed accepting.
- `pytest -q tests/test_v2_datasets.py -k <folder>`: 2 passed, with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- `dataset list --root datasets/_dev/tabarena-v0pt2` exits 0, and the import check passes.
- ruff check and ruff format are clean. No `TODO` is left.

**Probes:**
- **task_probes** (30 of 30 splits). Log loss and macro AUC per model:

  | Model | Log loss | Skill | Macro AUC |
  |---|---|---|---|
  | linear | 0.157 | 0.885 ± 0.009 | 0.997 |
  | LightGBM | 0.168 | | 0.997 |
  | random forest | 0.213 | | 0.996 |
  | dummy | 1.360 | | |

  Flag `solved`. Answer: a lookup, not a leak (`task_probes.md`, the "solved" row). The NEWS2 band is exact on every row, so a fixed published rule scores log loss 0 on every test fold, below every model on every fold. That is rule 4's fold-by-fold test, passed by a rule rather than a raw feature. The source has no earlier stage to fall back to, because all features are measured together.
- **leak_probes** (3 splits):
  - All features: macro AUC 0.997.
  - Best single features: SpO2 0.887, pulse 0.864, respiration rate 0.849.
  - Depth-2 / depth-3 trees: 0.841 / 0.908.
  - Dropping one feature costs at most 0.017 (SpO2).
  - 0.0% of test rows have an exact copy in train.
  - 1-NN label agreement: 1.000 for the closest tenth, 0.955 for all, 0.262 by chance.
  - No leak column: the signal is the additive score.
- **generated_probes**: flag `rule_leaves`. Three pure leaves hold 23.7% of the minority rows. For comparison, churn (retired as generated) had 26%, and the highest real dataset in the 2026-10-06 calibration had 17.7%.
  - Answer: the threshold rule explains the flag. Beyond the probe, the data show the mark the probe documentation names, "dependence that the world would show but the data does not" (Issue 2).
  - The first run crashed on another agent's scaffold (`QsarBioconcentration`, domain still `TODO`). I reran it with `--root` on a private folder holding a symlink to this dataset only.
- **hidden_groups**: no hits. The candidates were SpO2, pulse and respiration rate, with gaps of 0.015, 0.001 and 0.004.
- **Extra check** (scratch `null_test.py`, output `null_test.txt`). The null draws every column independently within each class and keeps the draws whose NEWS2 band is still that class (200 permutations). 43 of the 47 within-class pairwise Spearman correlations lie inside its 95% band.

**Issues for Lennart:**

1. **Should the record become No (Trivial, AHDS) and the folder be deleted before any build?**
   - Evidence: the README's decision table 1 shows the rule matches all 1,000 rows. The data hold no outcome such as death or ICU transfer, only the score band.
   - Implemented now: the folder is added and checked, as the record's "We will see post hoc" asked. The finding is an `Anomaly:` bullet plus a decision table.
   - Alternative: No, with the markers `Trivial` and `AHDS (Artifical/Handmade/Deterministic/Simulated)`; remove the folder. It was never built, so there is no CHANGELOG entry to undo.
   - No rescue exists. Hiding parameters to make the band uncertain would be a task of our own invention (`task_probes.md`, rule 6). Proposed record comment: `central_international_medical_college_and_hospital_health_risk_prediction.record_comment.md`.

2. **The vital signs look generated, against the record's "looks like very real data".**
   - Patient_ID runs in four blocks of the label. Within a class, the id order is unrelated to the NEWS2 total (Spearman 0.00-0.03).
   - Across classes every pair of vitals correlates at |r| 0.59-0.68. Within a class they behave like independent draws:
     - pulse and temperature: r -0.07 to -0.03 in every class (High: -0.045, 95% bootstrap interval -0.15 to 0.06);
     - SpO2 on air and on oxygen: 87.5% and 87.8% in High;
     - SpO2 on scale 1 and scale 2: 87.8% and 87.5%;
     - the 77 High patients who are not alert have the vitals of the 202 alert ones (pulse 121.7 and 120.6);
     - 43 of 47 within-class correlations fit the independent-draws null.
   - There is no terminal-digit preference: even respiration rates are 52.7% of rows, a systolic pressure ending in 0 is 9.1%, and every temperature decimal holds 8-12%.
   - This is circumstantial (supporting AHDS, criterion 4B). Issue 1 does not depend on it.
   - Provenance is one unverifiable sentence. "Missing source information" would also fit, but the record accepted missing information ("Even if some information are missing"), so I do not use it as a reason.

3. **The label was computed by code from these exact values (minor; it supports Issues 1 and 2).**
   - The 13 rows that break the RCP chart are scale-2 patients on air with SpO2 93-96%. NEWS2 gives them 0 SpO2 points; the label gives them the on-oxygen scale-2 points, which makes them Medium instead of Low.
   - A charting system applies the chart, so this slip points to a script that labelled the rows.

4. **Two probe and framework notes:**
   - (a) `generated_probes.py` (and the other `--root` probes) load every definition under the root and abort the whole run when any folder fails to import. Here that was another agent's fresh scaffold. Loading by name would isolate the failure.
   - (b) `leak_probes.py` reports `Consciousness` alone at macro AUC 0.500, although all 86 patients who are not alert are Medium or High. Untuned LightGBM cannot split off a categorical group of fewer than `min_data_per_group=100` rows. With `min_data_per_group=1` or one-hot encoding the same splits give 0.571. The probe can therefore miss the signal of rare categories.

**Resolved (Lennart, 2026-10-12; confirmed on the review page 2026-10-15):** No, `Trivial`: the label is the NEWS2 chart applied to the vital signs the data ship. The folder is removed.

### churn_telco_europa
**Outcome:** not added (irreversible leak of the iranian_churn kind: active lines and churners were recorded on
different dates, with no follow-up after extraction and no dates to re-anchor them). No folder in the working copy.
A probe-only definition used for the checks and probes is in the scratch folder
(`probe_root/churn_telco_europa/dataset.py`). An independent verifier tried to refute this and upheld it
(`verify/verify.md`).

**Record judgment:** do not add: irreversible leak (leak_checks.md §3, "Features summarise a window that ends at the
outcome: retire when no common prediction point can be rebuilt"; precedent `curation/records/iranian_churn.md`,
CC 2026-10-01 Lennart). Proposed markers: `Data Quality Issue`, plus `Ethical Issue` for the personal data (issue 2,
Lennart's call). The curator accepted the missing source; the reasons here are new evidence from the data.
- What the file is: one row per phone line of WOM, Chile (issue 3). The uploader's earlier notebook
  (raumonsa11/leak-or-not-leak-classification-models, run 2019-03-18) reads the original extract, a private upload
  ("train .csv", "test.csv"). Its target is `FLAG_PARQUE`, membership of the active base ("parque") at extraction.
  Next to it are `VIDA_WOM` (days at WOM), `MOTIVO_FUGA` (churn reason) and `CIA_FUGA` (the operator a churner left
  for). The europa notebook's cell 19 also calls the target "Flag_parque". The label is "already left" against
  "still here at extraction". No line is followed after extraction, so the task has no prediction horizon.
- The train file holds 160,892 active lines (`CHURN` = 1) and 29,884 lines that had left (`CHURN` = 0, 15.7%). The
  test file is 86,907 more active lines from the same population. A LightGBM classifier separates them from the
  train stayers at AUC 0.503. Both groups start at exactly 92 days of tenure and share one weekday pattern (below).
  Its `CHURN` = 1 on every row means what the stayers' label means.
- Proof that the classes were recorded on different dates:
  - Weekday pattern of tenure. All active lines measured on one date keep the weekday pattern of their activations.
    Tenure mod 7 has one residue at 2.6% (stayers) and 2.5% (test lines), against 14.3% for a uniform spread. The
    daily tenure histograms of stayers and test lines correlate at 0.936. In the churners that residue holds 10.3%.
    Their histogram correlates with the stayers' at 0.27, and at most 0.30 over shifts of up to ±60 days. So each
    churner's tenure was taken on its own exit date. A common snapshot date, earlier or later, would keep the
    pattern, at most shifted.
  - `DEVICE_TECNOLOGY` codes 21, 22, 23, 24, 25 and 30 are not in the uploader's dictionary (1-5). They occur in 7,025
    rows, all churners, and in none of the 247,799 active lines. The undocumented code 0 covers 4,151 rows (98.0%
    churners). In the earlier notebook's cell 9, 0 and 21 are the most frequent churn reasons ("EL MOTIVO MAS
    FRECUENTE DE FUGA ES 0 Y 21"). These are also the two largest churner-only codes here. This hints at an exit
    code but does not prove it.
  - The tenure edge at 92 days holds for the active lines only: 3,763 churners are under 92 days, against 14 stayers
    and 7 test lines.
- Consistent with windows that end at the exit (circumstantial):
  - No outgoing call in the last month despite earlier usage (a positive 3-month average): 22.4% of churners, 2.1% of
    stayers and of test lines.
  - Location missing: 6.1% of churners against 2.4% of stayers. Of the churners without a location, 96.3% had no
    voice traffic that month.
- The weekday residue is a leak of its own. It cannot carry churn risk, yet on lines with 92 days or more, 39.4% of
  those at the rare residue are churners (base 14.0%). The residue alone gives AUC 0.566.
- No cleaned variant survives. On lines with 92 days or more, without `DEVICE_TECNOLOGY` (186,999 rows), LightGBM gives:
  - all remaining columns: 0.930;
  - tenure in whole weeks and plan: 0.883;
  - plan alone: 0.723;
  - plan, handset and location: 0.757.

  On plans 350/13,437 and 700/16,798, 75.8% and 75.5% of churners have a tenure below the 5th percentile of the active
  lines. Only plan and handset show no class artefact. They make a 2-3-column task on a label without a horizon.
  All features give AUC 0.956; iranian_churn had 0.986.

**Data:** Kaggle dataset raumonsa11/churn-telco-europa (uploader "Raul EMJ"; files dated 2019-10-21; the europa
notebook read the same data on 2019-04-10; after its `dropna` it counts 157,091 stayers and 28,064 churners, as the
current file does). Downloaded with `uvx --from kaggle==2.2.2 kaggle datasets download raumonsa11/churn-telco-europa`
into `local-data-warehouse/churn_telco_europa/` (21 MB):
- `train_churn_kg.csv`: 190,776 x 20, sha256 d007d259...;
- `test_churn_kg.csv`: 86,907 x 20, sha256 bb22d041....

OpenML 44228 is the train file, identical row by row in all 20 columns (checked against its parquet). Licence:
"unknown" on the Kaggle data card, "Unknown" on OpenML 44228. The data card has no description and the dataset has
no discussion threads. No upstream paper, competition or institution was found: a web search for the file and
column names finds only OpenML 44228. The original extract of the earlier notebook was a private upload and cannot be
obtained.

**Definition:** none in the working copy. The probe-only definition (scratch) uses the prediction point as the source
frames it: score each active line for churn from its tenure, plan, last-month and 3-month usage, handset and antenna
location. It reads the train file only, drops `CETEL_NUMBER` and `CNI_CUSTOMER`, and maps the target `churned` (Yes =
`CHURN` 0). IID with the default splits (3 x 3 folds); 190,776 rows x 17 features; codes as categories. No other
cleaning.

**Checks:** `dataset check` on the probe-only definition: 0 errors, 2 warnings, 1 info. Nothing accepted.
- `dataset_pure_feature_value`: `DEVICE_TECNOLOGY` = 21 (3,227 rows) and = 22 (3,103 rows) are 100% churned. This is
  the leak above.
- `dataset_duplicate_rows`: 3,768 exact copies (2.0%) once the two identifiers are dropped.
- `dataset_conflicting_duplicate_rows` (info): 115 rows.

**Probes:** all on the probe-only definition, `--n-jobs 2`.
- Leak:
  - all features 0.944; depth-2 / depth-3 tree 0.684 / 0.725;
  - alone: `DEVICE_TECNOLOGY` 0.689, `TOT_MIN_CALL_OUT` 0.678, `ROACETEL_LAST_MONTH` 0.674, `TOT_MIN_IN_ULT_MES`
    0.667, `MIN_PLAN` 0.664, `DAYS_LIFE` 0.649; missing location 0.519;
  - without `DEVICE_TECNOLOGY`: 0.924;
  - exact copies in train 1.8%; 1-NN agreement 0.889 / 0.876 against chance 0.736; label-free distance 0.513.
- Task: no flags. LightGBM AUC 0.952, random forest 0.942, linear 0.734, single feature 0.689 (`DEVICE_TECNOLOGY` on 5
  of 5 splits); smallest class per test fold 7,781 rows. These probes do not test the recording mismatch.
- Generated: rule leaves cover 14.0% of the churners (threshold 20%), no flag.
- Hidden groups: no hits. `DAYS_LIFE` was a candidate (gap 0.017), the `CITY_*` columns had gaps of 0.004-0.005. The
  definition drops the customer id, so I checked the customers by hand:
  - 102,965 customers (`CNI_CUSTOMER`) in the train file, up to 597 lines each;
  - 69% of the rows belong to customers with several lines;
  - LightGBM AUC 0.956 with a random split, 0.949 grouped by customer.
- By hand, AUCs on feature subsets: scripts and outputs in `explore/`, the verifier's in `verify/`.

**Issues for Lennart:**
1. Retire this candidate as No with `Data Quality Issue` (iranian_churn precedent)?
   - The extract compares lines that had left with lines still active at extraction (`FLAG_PARQUE`), and has no
     follow-up period.
   - Active lines were recorded on one date, churners on their own exit dates: the weekday proof above.
   - Churner-only device codes: 7,025 rows. Tenure edge at 92 days for the active lines only. AUC 0.956.
   - No dates or monthly series exist to rebuild one prediction point.
   - Implemented: nothing in the working copy. There is no working alternative. The fixed variant fails: without the
     device codes and short tenures, tenure in weeks and plan still give 0.883. Only plan and handset are clean, at
     0.72-0.76, on a label without a horizon.

   **Verification:** upheld. The verifier recomputed every number above, found the weekday proof, the earlier
   notebook and the cleaned-variant table, and found nothing that refutes the retirement. My recheck of the weekday
   test gives the same residue shares and the 0.936 correlation; the best churner correlation is 0.30 at a 42-day
   shift with my detrending (0.273 at lag 0 in the verifier's).
2. The personal data is real. Should `Ethical Issue` be added as a marker, and should the raw copy in
   `local-data-warehouse/churn_telco_europa/` be deleted? Whether to tell OpenML is Lennart's call; nothing has been
   deleted.
   - `CNI_CUSTOMER`: 99.2% of the 277,683 rows (both files) have the shape of a Chilean RUT. All but 4 of those
     carry a valid mod-11 check digit (a random check character passes 9%), and 8.7% end in K. 110,115 distinct ids
     are below 50 million, the range of personal RUTs; 14,544 are higher (companies).
   - `CETEL_NUMBER`: 99.91% are 569 followed by 8 digits, Chile's mobile format; 269,013 distinct numbers.
   - OpenML 44228 serves both columns as ordinary features. A definition would drop them, but its
     `download_description` would still point users to them.
   - Precedent: Lennart gave `employee_salaries` and `employee_remuneration_and_expenses_earning_over_75000`
     `Ethical Issue` for PII ("Again contains PII", "Contains PII"; both `TBD -> 2nd Tier` with `No Good Target
     (yet)`). Those are government data published by law. This file is an internal company extract posted by an
     individual.

   **Verification:** confirmed (verifier F5). It corrected my earlier "99.998% of rows", which holds only for the
   RUT-shaped values. The person count is the verifier's; my recheck gives the same 110,115 and 14,544.
3. Provenance. "Missing source information" stands; the curator accepted it. The company is WOM, Chile:
   - the earlier notebook's tenure column is `VIDA_WOM`;
   - the europa notebook concludes that customers "decide to leave WOM" and pay plans of "7,000 and 15,000 pesos"
     (cell 27);
   - the ids and phone numbers have Chilean formats (issue 2);
   - the data has 15 region codes (1-12, 14, 15 and 100; 100 holds 45.9% of the located rows) and commune codes up to
     346, Chile's number of communes.

   The record name ("Europa") is wrong, and so is the notebook's "a small telecommunications company in Oceania ...
   only 14 months of life" (cell 1). Tenure reaches 2,567 days. If the record stays, its name and comments could say
   WOM, Chile.

   **Verification:** the verifier added the earlier notebook. It reads the notebook's code only (no outputs, no
   data); the original files are a private upload.
4. The record's open question: OpenML 44228 does not use the test data. It is the train file, identical row by row.
   The test file is 86,907 more active lines from the same population as the train stayers (AUC 0.503, the same
   92-day edge). Its `CHURN` = 1 means "active at extraction", as it does for the 160,892 train stayers. No active
   line, in either file, has an outcome after extraction. Combining the files would add rows but no information. The
   missing horizon is the problem in issue 1, not the test file.

   **Verification:** reworded after verifier F3; the 0.503 is the verifier's (v03).
5. Customer structure, relevant only if the dataset were added. In 93% of multi-line customers every line carries the
   same label. A deployed model scores the current lines of known customers, so IID (warm start) fits the use case;
   grouping by customer costs 0.007 AUC. Phone numbers are recycled: 4,991 numbers appear in 12,106 rows, 2,895 of
   them with both labels and 2,529 under more than one customer. The phone number is no entity key.

   **Verification:** not checked by the verifier (moot without a definition).
6. Cross-check of the churn_telco records, asked by the orchestrator:
   - OpenML 44229 is also named "Churn_Telco_Europa" but holds the DSN 2018 rows (1,401 x 16, target `churn_status`),
     the same data as 44230.
   - The europa record links 44228 (creator "RAUL EMJ", 190,776 x 20, target `CHURN`). That link is right, and the
     data is not the SATO 2015 / DSN data.
   - Nothing to change. A search by name finds the wrong id.

   **Verification:** the verifier confirmed it (rubric item 2).
7. Tooling note, low priority: `generated_probes.py` exited 1 with no output while `hidden_groups.py` ran on the same
   dataset at the same time. Run alone it worked. I did not check the cause.

   **Verification:** not checked.

**Resolved (Lennart, 2026-10-12; confirmed on the review page 2026-10-15):** No, with `Missing source information`, `Ethical Issue` and `Data Quality Issue`: WOM Chile's customers under a European name, with personal data and no prediction point.

### churn_telco_south_asia_duplicate
**Outcome:** not added (duplicate of churn_telco_south_asia: the DSN files are the 2,000 rows of the SATO 2015 file with renamed values, and the DSN train/test cut is selected on the label and total spend)

**Record judgment:** do not add: the same underlying data as `churn_telco_south_asia` of this run, which is the original
source (criterion 1, "Unique"; curation guidelines, "Different versions / cuts of one underlying dataset are duplicates
too"). Neither the record's comments nor any other record weigh this.
- The competition's Description page (`kaggle competitions pages dsntelecomschurn2018 --content`): "An academic data
  has been used here to help participants classify potential customers who might churn. Please note that a balanced
  dataset has been used".
- TRAIN.csv (1,400 rows and a blank last line) and TEST.csv (600 rows) match the 2,000 rows of "South Asian Wireless
  Telecom Operator (SATO 2015).csv" (kaggle.com/datasets/mahreen/sato2015, uploaded on 2017-10-11 by the user
  mahreen with Ahmed et al. 2017 as its source) one to one on the nine numeric columns rounded to 2 decimals, with no repeated key
  on either side. All 1,400 train labels agree (700 churned, 700 active). The network types are identical, and the
  competitor networks are renamed one to one: mobilink → Mango, ptcl → PQza, telenor → ToCall, ufone → Uxaa,
  warid → Weematel, zong → Zintel (the Pakistani operators of the SATO file). DSN added `Customer tenure in month`
  (network_age / 30) and moved the stated period from August-September 2015 to July-August 2017. The competition ran
  in January-February 2018, after the SATO upload.
- `churn_telco_europa` is other data (raumonsa11/churn-telco-europa: 190,776 train rows, 20 different columns). No
  folder of the working copy and no other record holds the SATO or DSN data (grep of `curation/records/` and the
  working copy for the OpenML ids 44227/44229/44230, both Kaggle slugs, the operator names, "Data Science Nigeria").
- The DSN cut is also a distorted sample: TEST.csv holds exactly the SATO actives with total spend 1,281.7-3,491.1
  (300 of 300 such actives) and the SATO churners with total spend 225.9-603.6 (300 of 300). TRAIN.csv is the rest, so
  its 228 rows in the churner band are all active and its 112 rows in the active band are all churned (in SATO the
  same bands are 56.8% and 27.2% churned).
- Reproduce with `<scratch>/evidence_duplicate.py` (output in `evidence_duplicate.txt`).

**Data:** Kaggle InClass competition dsntelecomschurn2018 (`uvx --from kaggle==2.2.2 kaggle competitions download -c
dsntelecomschurn2018`): TRAIN.csv 1,400 x 16 (with `Customer ID` and `Churn Status`), TEST.csv 600 x 15 (labels not
published), sample submission.csv; in `local-data-warehouse/churn_telco_nigeria/` (deleted 2026-10-15). No licence is stated on the
competition's pages (rules page: base rules only). For the comparison, the SATO csv (2,000 x 14, CC0-1.0 in the Kaggle
metadata) sits in my scratch folder only. OpenML 44230 (this record's link) is TRAIN.csv with its blank line (1,401
rows); OpenML 44229, named "Churn_Telco_Europa" version 2, holds the same rows.

**Definition:** none in the working copy. Two probe vehicles in `<scratch>/root/`, not for shipping:
`churn_telco_south_asia_duplicate` (DSN TRAIN.csv without the blank line, `Customer ID` and the tenure copy: 1,400 x 13) and
`churn_telco_south_asia` (the SATO file as it is: 2,000 x 13); both IID with the default 10 x 3 splits.

**Checks:** scratch only: `dataset check` 0 errors, 0 warnings on both.

**Probes:** on the scratch definitions, `--n-jobs 2`; outputs in `<scratch>/probes/`.
- SATO, 2,000 rows, 30 splits: random forest ROC AUC 0.815, LightGBM 0.806, linear 0.781, best single feature 0.681
  (Aggregate_Total_Rev on 26 of 30 training sides); no task flag. Leak probes (3 splits): all features 0.803, depth-2 /
  depth-3 tree 0.723 / 0.754, best feature alone 0.684, no missing indicator above 0.51, no exact copies across the
  split, 1-NN agreement 0.640 (chance 0.500), label-free distance 0.635. Generated data: 0.0% rule leaves, no flag.
  Hidden groups: no hit.
- DSN TRAIN, 1,400 rows, 30 splits: LightGBM 0.897, random forest 0.891, linear 0.726, single feature 0.838 (total
  spend on 30 of 30); no flag; generated 7.6% rule leaves, no flag; hidden groups none. The tree models gain from the
  two pure spend bands: total spend alone reaches 0.838 here against 0.681 on SATO.
- The `Trivial` marker ("100% accuracy possible? 50/50 churn rate"): the task is not trivial on the underlying data
  (single feature 0.681 against 0.815 for the best family, no flag). The 1.00000 public scores (11 teams; 3 more at
  0.99761) come from the test cut: "total spend < 1000 → churned" scores 1.000 on TEST.csv. The discussions show the
  other side: a model fit on TRAIN scored 0.14 on the leaderboard against 71% on a random split of TRAIN (topic 49960),
  another 0.001 (topic 50019), because TRAIN's two bands carry the opposite labels.

**Issues for Lennart:**
1. Verdict. Question: which record ships the SATO data? Evidence above. Implemented: nothing added for
   churn_telco_south_asia_duplicate. Proposal: No + Duplicate for this record (by the convention it becomes
   `churn_telco_south_asia_duplicate`), and the data ships once, as `churn_telco_south_asia` (original source, all
   2,000 rows labelled, original operator names). Alternative: ship the DSN cut; not recommended: 1,400 labelled rows,
   340 of them (24%) in spend bands whose labels the test selection made pure.
2. The `Trivial` marker. Answered above: the 100% came from DSN's test cut, not from the data. Proposal: replace
   `Trivial` with `Duplicate` on this record; churn_telco_south_asia carries no marker and needs none for this.
3. The SATO questions belong to `churn_telco_south_asia`, whose definition (written in parallel by its agent) already
   records the DSN match and reads the label as churn after the August-September window. Ahmed et al. 2017 is behind
   the IEEE paywall and I found no free copy either, so the prediction point stays unverified there (iranian_churn
   precedent, leak_checks.md §3). My scratch probes on the SATO rows (above) can cross-check that unit's probes. One
   data point for that question: missing user types do not predict churn (47-48% churned when missing, indicator AUC
   0.50-0.51), while `sep_fav_a` = ufone splits the label (65% active against 68-76% churned for the other values).
4. OpenML naming: 44229 is named "Churn_Telco_Europa" (version 2) but holds the DSN TRAIN.csv (its original_data_url
   is the DSN competition). The europa record links 44228, so nothing to change there; a search by name finds the
   wrong data. Benchmarks on OpenML 44230 (this record's TabSTAR link) measure the distorted cut.
5. Housekeeping: `local-data-warehouse/churn_telco_nigeria/` (the DSN zip and its three csv files, 0.24 MB) can be
   deleted if the record goes to No (ask).

**Resolved (Lennart, 2026-10-15):** No + `Duplicate` (replacing `Trivial`); the data ship once, as `churn_telco_south_asia`. The record is renamed from `churn_telco_nigeria` to `churn_telco_south_asia_duplicate` (the `_duplicate` convention), and its local download is deleted.

### churn_telco_south_asia

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/churn_telco_south_asia/`), revised after verification.

**Record judgment:** valid with concerns. The data were made by the authors of Ahmed, Siddiqi, Afzal and Khan, "MCS:
Multiple classifier system to predict the churners in the telecom industry", IntelliSys 2017, pp. 678-683,
doi:10.1109/IntelliSys.2017.8324367. The abstract (read through OpenAlex; the paper is closed access) says: "a newly
created dataset from a South Asian wireless telecom operator ... MCS achieved accuracies of 97% and 86% on the UCI
churn dataset and private dataset". The Kaggle upload mahreen/sato2015 (2017-10-11, data card citing the paper; OpenML
44227 lists the creator as MAHREENAHMED) is where the data first became public. Uniqueness:
- Nothing in the working copy is this data (its two churn folders, bank_customer_churn and tour_travels_churn, are
  unrelated).
- churn_telco_south_asia_duplicate (DSN Telecoms Churn 2018, Kaggle InClass) is this file renamed (issue 2). That makes Nigeria
  the duplicate, not this one.
- churn_telco_europa (Kaggle raumonsa11, OpenML 44228) is different data: 190,776 + 86,907 rows and other columns.
- mobile_churn (OpenML 44231) is also different data: 66,469 rows and 66 columns.

The concerns are the unverified label window (issue 1) and how the two classes were drawn (issue 3).

**Data:** Kaggle dataset mahreen/sato2015, one file `South Asian Wireless Telecom Operator (SATO 2015).csv` (sha256
70f135b5...cda8fe), 2,000 rows x 14 columns (13 features + `Class`), 1,000 Churned and 1,000 Active. OpenML 44227 is
the same file (all values identical, checked on its parquet). The licence is CC0-1.0, as stated in the Kaggle
dataset metadata (`kaggle datasets metadata`); OpenML lists it as unknown. The raw file is in
`local-data-warehouse/churn_telco_south_asia/`.

**Definition:**
- The prediction point is the end of September 2015. The model scores each subscriber after two months of usage
  (August and September aggregates and monthly attributes).
- Target: `churn_status` (the source's `Class`; Churned / Active), binary, ROC AUC.
- IID, the default 10 x 3 folds: train 1,333-1,334 rows, test 666-667 rows. Each row is a different subscriber, all
  observed over the same two months; there is no id and no time index.
- 2,000 rows x 13 features. The four month columns `aug_user_type`, `sep_user_type`, `aug_fav_a` and `sep_fav_a` are
  categorical.
- Cleaning: the only step is renaming the target; every value is kept as published. The anomalies are documented
  in `curation_comments`:
  - the raw file is put together from extracts;
  - `network_age` is negative for some subscribers;
  - the `"0"` network code is undocumented;
  - the on-net and off-net columns are not in rupees;
  - every complaint count is at least 1.
- One `_decisions` table shows the August and September favourite networks by class.
- year = 2015 (issue 4); source = Kaggle; BibTeX is the IntelliSys paper.
- pandas 2.3.3 and pandas 3.0.6 (shared pd3 venv) give the same checksum, `v2:bae6b4eb...f61234`.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). No accepted warnings.
- `ruff check` and `ruff format` are clean, and `load_definition` imports.
- `pytest tests/test_v2_datasets.py -k churn_telco_south_asia` passes 2 of 2 with `DATA_FOUNDRY_V2_DATA_CHECKS=1`
  after the revision. For a while, collection failed on another agent's scaffold (`onlinenewspopularity`); in that
  window the same two assertions passed on this folder alone (`fix/test_one.py`).

**Probes (2026-10-07, untuned, outputs in `probes/` and `fix/`):**
- Task probes (all 30 splits): random forest ROC AUC 0.815 (accuracy 0.738), LightGBM 0.806, logistic regression
  0.781, and the best single feature, chosen per split, 0.681 (one-feature LightGBM; `Aggregate_Total_Rev` on 26
  splits, `Aggregate_SMS_Rev` on 4). No flags. The random forest beats the dummy on 100% of the splits.
  - The raw `Aggregate_Total_Rev`, its direction chosen on each training side, scores 0.729 (0.698-0.761). That is
    below the random forest on every split (0.779-0.839), so the task is not `Trivial`.
- Leak probes (LightGBM, 3 splits):
  - All features: 0.803.
  - Single features: `Aggregate_Total_Rev` 0.684, `sep_fav_a` 0.683, `Aggregate_Calls` 0.659.
  - Drop one: without `Aggregate_Total_Rev` 0.781, without `sep_fav_a` 0.797.
  - Missing-value indicators: 0.49-0.50.
  - Shallow trees: depth 2 0.723, depth 3 0.754.
  - No test row has an exact copy in train.
  - 1-NN label agreement: 0.672 for the closest tenth, against 0.640 overall.
  - Label-free nearest-neighbour distance: 0.635, against 0.803 for the full model. That is the ordinary range of
    heart_failure (0.64 / 0.73), not class-conditional generation.
  - No flag needs a decision.
- Generated-data probe: no rule leaves (0.0% of the minority), no flag.
- Hidden-group probe: no hit. The 2 candidates are `Aggregate_Calls` (gap -0.019) and `Aggregate_ONNET_REV` (gap
  +0.014).

**Verification:** the verifier's verdict was "ready with noted concerns". I re-checked every finding with my own
code (`fix/recheck.py`, `fix/blocks.py`, `fix/lobo.py`, `fix/years.py`, `fix/years_vs_records.py`).

1. **Churn timing (major).** Accepted, kept as implemented, and issue 1 now holds the numbers. My random forest
   (300 trees) gives ROC AUC 0.815 overall, 0.805 on test rows with more than 5 calls and 0.810 without both
   September columns; the verifier's 0.814 / 0.804 / 0.812 differ only by seed. 55 churners and 5 active subscribers
   have at most 2 calls. The September type is missing for 99 churners and 107 active subscribers.

   One point rejected: the verifier counted "active subscribers complain more (2+: 46% vs 26%)" as evidence against
   a window that ends at churn. A shorter window for churners would also lower their complaint counts, so this does
   not argue either way. Issue 1 states it as neutral.
2. **Overstated claim about September (minor).** Applied. All 26 subscribers with one call (24 churners) have the
   same network in both months (34% of all rows do). The comment now says the data do not settle the timing.
3. **The classes were not drawn as one random sample each (minor).** Applied as a new Anomaly bullet, and the
   random-sample premise was dropped from the cohort bullet.
   - Confirmed exactly: 52 runs of rising `network_age`, with 97% of rows in runs of 5 or more. The 8 runs of 100+
     rows have churn shares of 0.35-0.73.
   - 6 runs are churners only (54 rows, raw rows 1443-1665). Their medians against the other churners: revenue
     1,194 vs 332, calls 256 vs 43, complaints 3 vs 1.
   - Leave-one-run-out random forest AUC is 0.757-0.888 for the 10 runs of 60+ rows.
4. **`aug_fav_a` = "0" (minor).** Applied. All 59 such subscribers have off-net revenue (median 9,032 vs 5,039 for
   the file) and at least 8 calls. The code is now called undocumented.
5. **Raw single feature (minor).** Applied: 0.729 on the 30 splits, added to the probes bullet.
6. **Year (minor, Lennart's call).** Applied: year = 2015, the convention the working copy follows (issue 4).

**Issues for Lennart:**

1. **When was churn observed?** The question is whether the churners left after the August-September 2015 window,
   which makes a valid task, or inside it. In the second case the aggregates would summarise a window that ends at
   the outcome, the iranian_churn retirement reason.
   - Sources: the record's quotes and the data card do not say. The IntelliSys 2017 paper and the authors' 2018
     Neural Computing and Applications paper (doi 10.1007/s00521-018-3678-8) are closed access, with no free copy
     found, so I did not read their text.
   - The record's second quote keeps the PDF's line breaks, so the PDF was in hand at triage.
   - The data do not settle it:
     - The September subscription type is missing about equally often (99 churners, 107 active subscribers).
     - The September favourite network is filled even for the 26 one-call subscribers (the same network in both
       months), so it does not show September activity.
     - A near-inactive tail is almost all churners (at most 2 calls: 55 churners, 5 active subscribers), but the
       signal does not rest on it. Random forest ROC AUC is 0.815 overall, 0.805 on test rows with more than 5
       calls, and 0.810 without the two September columns.
     - The active subscribers complain more (2 or more complaints: 46% against 26%). Their higher usage, or a
       shorter window for churners, would both explain this.
   - Implemented: churn after the window.
   - Alternative: retire as iranian_churn if the paper's data section places the churn inside August-September.
   - Please read the paper's data section. A Google search for "MCS: Multiple classifier system to predict the
     churners in the telecom industry" pdf should find it; the data card links ResearchGate 320331663.
   **Follow-up (AI, 2026-10-15):** Lennart added Ahmed et al., Neural Computing and Applications 32:3237-3251 (online 2018, doi 10.1007/s00521-018-3678-8). It does not settle the timing: "The subscriber data is extracted from the time interval of two months, i.e., August and September 2015" (Sec. 3.1, p. 3241), and "class labeling (for SATO dataset)" is a preprocessing step without a definition (Sec. 3.2). The record's second quote is not in this paper, so it comes from the IntelliSys 2017 paper, the one source left. If that says nothing either: keep as implemented (fit `approximate`, the unknown timing named).
   **Follow-up (AI, 2026-10-15):** Lennart added the IntelliSys 2017 paper too. Its data section does not say it either: "The subscriber data was extracted from the time interval of two months, i.e. August and September 2015. To overcome the class imbalance problem in churn data sets, an equal amount of churners and active subscribers were collected from the carrier" (Sec. III, p. 680); "class labeling" is a preprocessing step (Sec. IV, p. 681). No source is left. Recommendation: keep as implemented, fit `approximate` with the unknown timing named.
   **Resolved (Lennart, 2026-10-15):** ship, kept for now as possibly problematic: the definition states the unknown timing as a potential leak kept on purpose (curation_comments, task summary), to revisit if the churn can be dated.
2. **churn_telco_south_asia_duplicate is this data.** The DSN 2018 files (TRAIN 1,400 + TEST 600) are these 2,000 rows:
   - all rows match one to one on the nine numeric columns;
   - all 1,400 TRAIN labels agree;
   - the networks are renamed one to one: mobilink Mango, ptcl PQza, telenor ToCall, ufone Uxaa, warid Weematel,
     zong Zintel;
   - DSN added a customer id and a tenure in months, and relabelled the period "Months 1 and 2 of 2017";
   - the orchestrator and the verifier each re-matched the files independently.

   The DSN description (OpenML 44230) says "An academic data has been used here", so the Nigeria record should
   become the duplicate of this record. Its `Trivial` marker ("100% accuracy possible?") is answered here: random
   forest AUC 0.815 against 0.729 for the raw total revenue, on 30 splits. Side note: OpenML 44229 is titled
   "Churn_Telco_Europa" (version 2) but holds the DSN data. The churn_telco_europa record links 44228, which is
   different data.
   **Resolved (Lennart, 2026-10-15):** marked: the DSN record is now `churn_telco_south_asia_duplicate`, `No` + `Duplicate` of this record.
3. **The 50% base rate is artificial, and the classes were drawn from several extracts.** The record quotes "an
   equal amount of churners and active subscribers were collected from the carrier".
   - ROC AUC does not depend on the class shares. Log loss and predicted probabilities do, and the operator's churn
     rate is not given.
   - The raw file was put together from about ten extracts, each sorted by `network_age`, with churn shares of
     0.35-0.73. Six short churner-only runs (54 rows) are heavy users (median revenue 1,194 against 332 for the
     other churners). So it is not known whether either class represents the operator's subscribers.
   - The base class shuffles the rows, and no extract id is shipped. Each held-out extract scores ROC AUC
     0.757-0.888, so no extract is out of line.
   - All but 6 subscribers have a network age of 91 days or more, so the sample looks restricted to subscribers of
     at least three months.
   - Implemented: kept as published, with bullets saying so.
   **Resolved (Lennart, 2026-10-15):** as implemented.
4. **Year: docstring against practice.** Implemented: `year = "2015"`, the collection year and the record's year.
   - Of the 125 committed definitions, 94 keep their record's year.
   - Those that move away from the publication year move to the data's year: amazon_employee_access 2010 for a
     2013 competition, kdd_cup_09_appetency 2008 for 2009, taiwanese_bankruptcy_prediction 2009 for a 2016 paper,
     cirrhosis_patient_survival_prediction 1984 for 1989.
   - The v2 docstring says "Year the data was published", which would give 2017 (the paper and the Kaggle upload).
     The working copy is mixed: airfoil_self_noise uses its UCI year, 2014, for a 1989 experiment.
   - The docstring or the practice should change. It is the same question as pkdd's (ORCH_NOTES).
   **Resolved (Lennart, 2026-10-15):** as implemented (`year = "2017"`).
5. **The paper's 86% accuracy is not reached.** The abstract reports 86% accuracy for MCS on this "private dataset".
   An untuned random forest reaches 0.738 (0.706-0.763) on the 30 splits here, and the public Kaggle notebooks
   report 0.74-0.76.
   - This may mean the published file differs from the paper's data, or that the paper's protocol was optimistic.
     It cannot be checked without the paper.
   - Implemented: nothing; noted in `curation_comments`. Low priority.
   **Resolved (Lennart, 2026-10-15):** as implemented. The papers explain part of the gap: "Package Name" is one of their features (IntelliSys 2017, Sec. III.A) and among the top five (Neural Computing and Applications, Sec. 4, p. 3249), and the public file lacks it.
6. **Anomalies kept as published** (low priority):
   - `Aggregate_ONNET_REV + Aggregate_OFFNET_REV` is a median 22 times `Aggregate_Total_Rev`, so these are not
     rupees. 206 of the 1,944 positive off-net values are multiples of 179 (179 alone: 65 rows), which suggests a
     per-call or per-minute charge. The unit is undocumented; a Kaggle discussion question about it has no answer.
   - `network_age` is negative for 5 churners (-8 to -2 days, consecutive raw rows 594-598) and 6 days for one
     active subscriber. The alternative is NaN, which carries the same information, since all 5 are churners.
   - `aug_fav_a` is "0" for 59 rows, an undocumented code: all have off-net revenue and at least 8 calls. It is
     kept as its own category.
   - `Aggregate_complaint_count` is at least 1 for every subscriber.
   - The favourite network shifts to ufone in September for both classes: active subscribers from 223 to 786,
     churners from 223 to 426. I read this as a month effect, not a recording that differs by class. Dropping
     `sep_fav_a` costs 0.006 AUC, and dropping both September columns 0.005.
   **Answer (AI, 2026-10-15):** Lennart asked which are natural and which a human should fix. Fixed, as caracas_cervical_cancer's impossible answers: the 5 negative `network_age` values become missing (days on the network cannot be negative), and `aug_fav_a` "0" becomes missing (an undocumented placeholder, absent in September, for subscribers who did call other networks: an unknown network). Natural, kept: the on-net and off-net unit (undocumented, the scale does not matter to the models), complaint counts from 1 (an offset or the cohort), and the September shift to ufone, which follows activity in both classes (share by fifth of calls, lowest to highest: 0.40 to 0.93 active, 0.18 to 0.80 churned; at equal calls both keep their August network equally often: 0.56/0.66 lowest fifth, 0.17/0.19 highest). `dataset check` 0 errors, 0 warnings; leak probes: all features 0.813, missing indicators 0.50-0.51; checksum `v2:28d5013a…`.
   **Resolved (Lennart, 2026-10-15):** as applied; ship.

### college_scorecard
**Outcome:** added and checked
**Record judgment:** valid with concerns. The source is traceable and official (U.S. Department of Education, College Scorecard). Rebuilt from that source, the task is a real predictive one, and nothing in the working copy uses this data. Concerns: (a) the record's first link, OpenML 46674 (TableShift's copy), is not usable as data. TableShift's preprocessing `df[target] = (df[target] > 0.5).astype(int)` (tableshift/datasets/college_scorecard.py) makes a missing completion rate class 0, and OpenML keeps all 124,699 rows (15,905 positives, 108,794 negatives). In the 2026 release, 35,099 of the 126,743 institution-years of 1996-2013 have a C150_4, so roughly 90,000 of those negatives have no completion rate. Its features are quantile-binned (values 0-99, -1 for missing) and it has no year column. (b) The official download is blocked from our servers (CloudFront 403), so the raw zip comes from the Internet Archive (identical MD5). (c) The `colleges` record (OpenML 42727) uses the same source (issue 7).
**Data:** College Scorecard "All Data Files" release of June 10, 2026, `College_Scorecard_Raw_Data_06102026.zip` (469,515,074 bytes, MD5 38f26ca8776518f77836ddfa1e219de8, equal to the ETag of the official file). It comes from https://web.archive.org/web/20260822105756id_/https://ed-public-download.scorecard.network/downloads/College_Scorecard_Raw_Data_06102026.zip, because the official URL and collegescorecard.ed.gov answer HTTP 403 (CloudFront "Request blocked") from this machine. The definition reads the 30 files MERGED1996_97_PP.csv to MERGED2025_26_PP.csv from the zip (6,273-7,869 rows x 3,308 columns each). Documentation: the data dictionary (sheet Institution_Cohort_Map) and InstitutionDataDocumentation.pdf (version September 2025), pinned as Internet Archive snapshots in `download_description`. Licence: the catalog.data.gov entry lists http://www.opendefinition.org/licenses/cc-by and data.ed.gov says "Creative Commons Attribution"; the Scorecard data page states none; Kaggle's 2015 copy says CC0-1.0.
**Definition:** folder `datasets/_dev/tabarena-v0pt2/college_scorecard/`.
- Prediction point: the fall a first-time, full-time cohort enters a four-year institution (ICLEVEL = 1). The model sees what the Scorecard file of that year holds about the institution and its entering class, including the institution's latest published outcomes: C150_4_LATEST (the 150% rate of the cohort six years older) and RET_FT4 (retention of the cohort one year older).
- Target: `completion_rate_150pct` = C150_4 from the file six years later (cohort map: C150_4 in MERGED_2024-25 is the fall 2018 cohort). Regression, scored with RMSE.
- Regime: temporal on `cohort_year` (2001-2018). `TemporalSplits(window=1, unit="unique", n_windows=9, gap=5, min_train_fraction=0.5)` gives 4 windows: test cohorts 2018, 2017, 2016 and 2015, with train 2001-2012 down to 2001-2009 (17,634-23,353 train and 1,842-1,858 test rows). The horizon is 1 year (one cohort per window); the 5-cohort gap is the label lag.
- Size: 34,431 rows x 89 features (+ target), 2,569 institutions.
- Cleaning:
  - cohorts of at least 30 students (D150_4; drops 3,926 of 38,357);
  - race shares summed over the old and new IPEDS categories (old-only reporters get NA for NHPI and 2MOR);
  - codes mapped to the dictionary's labels (CONTROL, PREDDEG, HIGHDEG, REGION, OPEFLAG, OPENADMP, ADMCON7);
  - ADMCON7 codes -1 and -2 set to missing.
- Dropped:
  - UNITID and D150_4;
  - the five SAT columns (scale change at the 2017 cohort);
  - columns the release holds only in its newest file or as one fixed year (LOCALE, CCBASIC, CCSIZSET, ACCREDAGENCY, HBCU, SCH_DEG);
  - series that end before 2018 (NSLDS student profile, zip-code census shares, SAT/ACT writing);
  - the other outcome series.
- pandas 3.0.6 gives the same checksum as pandas 2.3.3 (v2:457d0b36…).
**Checks:** `dataset check` gives 0 errors, 0 warnings and 1 info (`meta_time_horizon_unit`: the time column is an integer year, so the horizon cannot be cross-checked; fine for a year column). Accepted: `splits_rows_unused` (cohorts 2013 and 2014, 3,676 rows, lie in the five-cohort label gap of every window and before the oldest test window). ruff is clean. pytest cannot collect `tests/test_v2_datasets.py` while another agent's folder (caracas_cervical_cancer) fails to import; run directly, the test's assertions pass for this folder.
**Probes (revised data):** leak (3 splits, untuned LightGBM): all features R² 0.799; depth-2/3 tree 0.677/0.710; best single features C150_4_LATEST 0.749 and RET_FT4 0.586 (the institution's own published history, known at the prediction point), then ACTCM25 0.462; best missing indicator ADM_RATE 0.103; without C150_4_LATEST 0.787, without RET_FT4 0.785; 0.0% of test rows have an exact copy in train; 1-NN R² 0.635 (closest tenth 0.508), the same institutions' earlier cohorts, legitimate under a temporal split (leak_checks.md §4). No flag. Task (4 of 4 windows): dummy RMSE 0.198, drift skill 0.020, linear R² 0.747, random forest 0.803, LightGBM 0.805 (RMSE 0.085, beats the dummy on 4 of 4, SE 0.004), best single feature C150_4_LATEST (4 of 4) R² 0.745, skill 93% of LightGBM's, below the 95% `one_feature` threshold; LightGBM minus linear +0.055 (paired SE 0.004). Flags: none. Generated: exact 4.8% vs 4.8% shuffled (187 terms), no flag. Hidden-group and group probes not run (temporal task).
**Verification:** the independent verifier said "needs changes". Each finding and what was done:
1. **Race shares 0 for 2,808 rows of the 2008-2009 cohorts (blocker): applied, with a broader rule.** In the two transition files an institution reports in the old categories, the new ones, or partly in both. 271 four-year rows mix the two sets; their shares, with UGDS_NRA and UGDS_UNKN, add up to 1. Each share is now the sum of its new and old category, and NHPI and 2MOR are NA where only old categories are used. Afterwards the shares add up to 1.0 in every cohort and 23 rows have all race shares at 0 (2,829 before). Alabama A&M 2008/2009 UGDS_BLACK is 0.961/0.954.
2. **SAT scale change at the 2017 cohort (major): applied by dropping the five SAT columns.** The median within-institution jump from 2016 to 2017 is +45 SATVR25, +30 SATMT25 and +70 SAT_AVG, against at most 7 points between other years (re-measured). A conversion back to the old scale can only be done reliably for part of them, so it stays an issue (issue 2). Untuned LightGBM with the SAT columns as published scores 0.779 and 0.810 on the 2018 and 2017 windows against 0.797 and 0.814 without them (0.708 and 0.737 against 0.760 and 0.770 in the variant without outcome features).
3. **The published completion rate (major, Lennart's call): applied by including C150_4_LATEST and RET_FT4.** The record supports it: "we have (de facto) data from each institution at time point T", and an entity's own history is legitimate under a temporal split (leak_checks.md §4). The rate carried forward through a line fit on train scores 0.734/0.759/0.753/0.742 on the 2018/2017/2016/2015 windows; untuned LightGBM scores 0.797/0.814/0.805/0.810, so the rate does not settle the task (rule 4). The characteristics-only version is issue 1.
4. **Wording of the 30-student filter and D150_4 (minor): applied.** The one-year C150_4 is published for any cohort size, and 30 is the Scorecard's threshold for its pooled, consumer-facing rates. D150_4 is the entering cohort less IPEDS's allowable exclusions.
5. **ACT below 10, UG25ABV, URL pins (minor): applied.** The 56 rows with an ACT 25th percentile below 10 get an Anomaly note: the values lie on the 1-36 scale, so they are kept, and the SAT < 200 rule went away with the SAT columns. The bullet now says UG25ABV is blank for even cohorts. The dictionary and documentation are pinned to Internet Archive snapshots.
**Issues for Lennart:**
1. **Should the institution's published outcomes be features?** Implemented: yes, C150_4_LATEST and RET_FT4 (verification 3). Untuned LightGBM R² on the 2018/2017/2016/2015 windows:
   - all features: 0.797/0.814/0.805/0.810;
   - without RET_FT4: 0.781/0.801/0.790/0.796;
   - without both, the "expected completion from characteristics" task TableShift's feature list implies: 0.760/0.770/0.767/0.777;
   - the carried-forward rate alone: 0.734/0.759/0.753/0.742.

   Other history columns could be added as well and are not: C100_4 and C200_4 (other completion rates), TRANS_4 (transfer rate), and the 8-year outcome measures from 2015-16.
2. **SAT columns: drop (implemented) or convert?** The College Board publishes official concordance tables, new SAT to old SAT ("SAT Concordance Tables for Higher Education", 2016):
   - SATMT25/75 can go through the Math table and SAT_AVG through the total-score table;
   - SATVR25/75 (Evidence-Based Reading and Writing from 2017) have no one-to-one table to the old Critical Reading section.

   So a conversion would bring back four of the five columns, and SATVR would need an approximation.
3. **Target.** Implemented: C150_4 as a regression (the record notes that TableShift binarized it). Alternatives in the same files:
   - median earnings 10 years after entry (MD_EARN_WNE_P10: only 7 files, two-year pooled cohorts, measured 2007-2021);
   - the 3-year cohort default rate (CDR3: files 2011-12 to 2024-25);
   - TableShift's binary C150_4 > 0.5.
4. **Gap and number of windows.** Train ends six cohorts before the test cohort, because a cohort's rate is published six files after entry. Without the gap, untuned LightGBM reaches R² 0.86 instead of 0.81 (mean of 4 windows), because it trains on rates that are not yet published. With the gap and the 50% train rule there are 4 windows instead of 9. Alternative: start in 1996 instead of 2001, which adds 8,692 rows of cohorts 1996-2000 (without admissions or test scores) and gives 6 windows (2013-2018).
5. **Cohort-size filter.** Implemented: D150_4 >= 30, the Scorecard's suppression threshold for its pooled rates; it drops 3,926 of 38,357 institution-cohorts. Alternative: keep all cohorts, where a single student moves the rate of a 1-29 student cohort by 3-100 points.
6. **Download.** The official URL answers 403 from our servers; the definition downloads the Internet Archive snapshot (its MD5 equals the official ETag). Worth fetching the zip once from another network and keeping a backup.
7. **`colleges` record (OpenML 42727, TBD -> 2nd Tier, "cannot find origin").** It is a one-year College Scorecard snapshot: UNITID and Scorecard columns (admission_rate, sat_*_midrange, completion_rate, carnegie_*, earnings), "about 7800 different US colleges", target `percent_pell_grant`. It has the same source, so once college_scorecard ships it is a duplicate cut with a descriptive target (`Duplicate` / `No Good Target`).
8. **Selection of scored cohorts.** 15,900 of the 54,257 four-year institution-years (2001-2018) have no rate six files later. 6,980 have no row then (closed, merged, or out of the Scorecard), and most of the others enroll no first-time undergraduates (5,570 are graduate-only). Cohorts at institutions that close within six years cannot be scored, and the benchmark inherits that.
9. **Framework note (no action needed for the data).** The split metadata stores `time_horizon` (1 year here) but not the gap, so the 5-cohort label lag shows only in the splits themselves and in `splits_comment`.

### corporate_credit_rating
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/corporate_credit_rating/`). The fix round of 2026-10-07
switched the regime from temporal to grouped by company.

**Record judgment:** valid with concerns. The definition departs from the record's `Non-IID (Temporal)` tag (issue 1).
- Provenance traced. The Kaggle dataset agewerc/corporate-credit-rating (Alan Gewerc, 2020-07-24) is byte-identical to
  `data/corporate_rating.csv` in github.com/Agewerc/ML-Finance (commit 83411e2, 2020-07-07).
  - The repository's `generateCreditRatingDataset.py` built it from the opendatasoft ratings history
    (`data/ratings-history.csv`, 474,616 rating actions of nine agencies) and the Financial Modeling Prep ratios API.
  - Every one of the 2,029 rows traces back to a rating of that agency, company and date in the history.
- Unique. No working-copy folder or other record holds this data (grep for the slug, OpenML 43344 and the name). OpenML
  43344 is a re-upload of the same file (2,029 x 31, CC BY 4.0).
- The run's other credit-rating record, `corporate_credit_rating_cat_data_set_ratings_raitings` (OpenML 46372), is
  different data: anonymized bank ratios from Baesens et al. 2016 (spid, rating, commeqta, llploans, costtoincome, roe,
  liqassta, size). There is no overlap.

**Data:**
- Source: Kaggle `agewerc/corporate-credit-rating`, one file `corporate_rating.csv` (sha256 ba6bdd88...7409), 2,029 rows
  x 31 columns, no missing values.
- Licence: CC BY 4.0 (Kaggle data card; the same on OpenML 43344).
- Raw copy: `local-data-warehouse/corporate_credit_rating/`.
- Upstream files used only for verification (the repository's ratings history, us_stocks.csv, script and notebook;
  33 MB) are in `/home/.../_scratch_new65/corporate_credit_rating/`.

**Definition:**
- Prediction point: an analyst holds a company's financial statements for a fiscal year, its sector and the agency
  whose scale is wanted, and estimates the letter grade that agency would give a company without a rating of its own
  (a shadow rating).
- Target: `Rating`, multiclass, scored by log_loss. 6 classes: BBB 671, BB 490, A 398, B 302, AA 89, CCC/CC/C 70.
  - CCC, CC and C are merged, as in the uploader's rating table.
  - AAA (7 rows) and the two defaults (S&P D, Moody's C) are dropped, as the uploader did.
- Regime: `Grouping(on="Symbol", labels="per_sample", prediction_unit="row", context="none")`, with the shadow-rating
  definition citing the uploader's notebook (cell 47).
  - Splits: 10 repeats x 3 folds; 592 companies, 194-200 test companies per fold, train 1,320-1,383 rows, test 637-700.
- Frame: 2,020 rows x 28 features (agency, sector, date, 25 ratios); Symbol is the group column.
  - Name is dropped.
  - Zeros, ones and impossible ratio values are kept as reported, with a note.
- Decisions with evidence tables: the class mapping; grouped not temporal (72.0% of the 1,428 ratings with an earlier
  rating of the company repeat its class); agencies by year.
- Checksum `v2:b1d20b92...`, the same under pandas 2.3.3 and 3.0.6.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); nothing accepted.
- ruff is clean, the import works, and `pytest tests/test_v2_datasets.py -k corporate_credit_rating` passes 2 of 2,
  with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- The record's `v2_path` is still unset; `sync-notebooks` is the curator's step.

**Probes** (grouped definition, `fixround/probes/`):
- **Leak** (3 splits, macro AUC): all features 0.706 (untuned LightGBM). A depth-2 tree scores 0.682 and a depth-3 tree
  0.704. The best single feature is pretaxProfitMargin (0.632), then the agency (0.627). No missing values; 0.0% exact
  copies. 1-NN label agreement is 0.32, against 0.23 by chance.
  - The shallow tree comes close only to the untuned LightGBM. A random forest reaches 0.757-0.767 (task and group
    probes), so the label is not a rule over a few columns.
- **Task** (30 of 30 splits): no flags.
  - Random forest skill +0.154 +- 0.016 (SE 0.003); it beats the dummy in 100% of the splits, macro AUC 0.767.
  - Untuned LightGBM -0.581 (macro AUC 0.735, overconfident); linear -0.060.
  - The single feature (the agency in 28 of 30 splits) scores +0.018.
  - The smallest class in a test fold has 13 rows.
- **Generated:** no flag (rule leaves cover 0.0% of the minority rows).
- **Group:** LightGBM macro AUC 0.842 IID against 0.732 grouped (gap 0.110). Across companies: random forest 0.757,
  LightGBM 0.728, logistic regression 0.660, kNN 0.604. There is real signal across companies, and the methods spread.
- **Hidden groups** (`--include-grouped`): one hit, `Symbol`, the declared group (592 values, 3.41 rows each; gap +0.273
  between a random and a by-company split). No other entity column.

**Issues for Lennart:**
1. **The regime departs from the record's `Non-IID (Temporal)` tag: grouped by company is implemented.**
   - Evidence, on the first version's 9 quarterly windows (Oct 2014 to Dec 2016):
     - 86.6% of test ratings were of a company with a training row.
     - On those rows, carrying the company's latest training letter forward scores log-loss skill 0.39 (p = 0.72, the
       training side's persistence; accuracy 72.7%), against 0.305 for a random forest. It wins in 8 of 9 windows.
     - On new companies the forest scores 0.175.
     - The time order adds nothing over IID (forest 0.287 temporal, 0.273 IID).
   - So the temporal task without the prior rating matches no deployment: a rated company's rating is public. A model
     from financials alone serves unrated companies, which is a shadow rating.
   - Alternatives kept for your decision:
     - (a) The temporal version (the first definition, the record's tag): `TemporalSplits(window=3, unit="months",
       min_train_fraction=0.5)`, 9 windows of 75-145 rows, RF skill 0.287 (SE 0.010), no probe flags.
     - (b) A rating-migration variant: temporal, plus the company's previous rating and the days since it as features.
       RF skill 0.460 (SE 0.020) against 0.285 without them, better in 9 of 9 windows. This is the realistic
       monitoring task.
2. **Which classes to predict** (the record's "minor ones"). The file holds letter grades only, because the script
   strips the notches. The rare grades are AAA 7, CC 5, C 2 and D 1. Implemented: 6 letter classes, with CCC/CC/C
   merged and AAA plus the defaults dropped (2,020 rows); grouped RF skill 0.157 on the shipped splits.
   - Alternatives, scored by company (GroupKFold 3 x 2; RF):
     - (a) the uploader's 4 Investopedia risk tiers (Low 487 / Medium 671 / High 792 / Highest 70): skill 0.194
       (6 classes: 0.152 in the same run);
     - (b) investment vs speculative grade (1,158 / 862): ROC AUC 0.829 (LightGBM 0.835);
     - (c) notch level: this needs `ratings-history.csv` as a second input. 1,749 of 2,029 rows have a single long-term
       notch from that agency on that day. Moody's notches are biased by issue 5.
3. **The agency mix changes with the year** (a collection artifact of the ratings history).
   - S&P has 68 of the 69 rows up to 2011. Moody's has 251 of the 357 rows of 2012. Egan-Jones has 602 of its 603
     rows in 2013-2015. S&P and Moody's have 404 of the 428 rows of 2016.
   - Egan-Jones rates higher (A or above: 46% of its rows, against Moody's 19% and S&P 11%).
   - Under grouped CV the years are pooled, and the agency and date are features, so this matters less than it did
     for the temporal version.
   - Alternative: one consistent label source, S&P only (739 rows) or S&P + Moody's (1,315 rows).
4. **Label noise from instrument ratings.** In 171 rows (8.4%; 168 after our drops) the agency gave the company's debt
   2-3 letters that day, and the script kept the first in file order. Within the 12-month window, the verifier counts
   239 rows (11.8%), an upper bound.
   - Grouped RF skill: 0.157 with these rows, 0.152 without them.
   - Implemented: labels kept as published. Alternative: drop the rows, with `ratings-history.csv` (31 MB) as a second
     input.
5. **Data-quality quirks of the uploader's build** (informational; noted as Anomaly bullets, not fixable without
   rebuilding the file):
   - Moody's Aa3, Ba3, B3 and Caa3 are dropped by a tab and Unicode minus signs in the mapping;
   - the cohort is the June 2020 listing of us_stocks.csv, so companies rated in 2005-2016 and delisted by 2020 are
     missing (Sears Holdings, Windstream, Weatherford: 146, 256 and 523 history entries, no rows);
   - 223 rows dated 2012-06-15 are ratings outstanding when the Moody's and Fitch histories start;
   - the committed script cannot have produced the file as it stands (a missing comma in its drop list, a `rename`
     without `columns=`), though every row traces back.
6. **`source` = "Kaggle", although the identical file was on the uploader's GitHub 17 days earlier** (2020-07-07,
   against 2020-07-24 on Kaggle; an earlier version on 2020-07-05).
   - I chose Kaggle: it is the dataset release with the data card and licence, and the record's first link. The pinned
     GitHub URL is in `download_description`.
   - Alternative: `source = "GitHub"`.
7. **Framework (known):** the README renders `splits_comment` without dedenting it. This is the gap the orchestrator
   logged (`dataset.py:677`); I did not patch it.

**Verification (fix round, 2026-10-07):** the verifier's verdict was "ready with noted concerns", with one major
finding. I checked each finding before acting on it.
1. **Regime (major): confirmed and applied.**
   - My own carry-forward test estimates p on each training side instead of fixing it at 0.7. It scores 0.39 against
     RF's 0.305 on seen-company rows (the verifier: 0.348), accuracy 72.7%, and wins in 8 of 9 windows.
   - Changes: switched to `Grouping(on="Symbol", ...)`, dropped only Name, removed `temporal`, and added a
     shadow-rating `definition` (uploader's notebook, cell 47), a regime bullet, a splits comment and a decision table.
   - The new task, group and hidden-group probe numbers are above; they match the verifier's scratch variant (RF
     +0.154, SE 0.003, macro AUC 0.767, at least 13 rows per class).
2. **Statement timing (minor): reproduced and applied.**
   - The verifier's within-row test reproduces exactly: RF -0.018 [-0.046, +0.009] for 772 July-December ratings,
     against +0.047 [+0.004, +0.094] for 363 March-June ratings; LightGBM -0.012 for July-December.
   - Changes: the bullet is now a "Note:" with the verifier's text. Its training-side sentence is labelled as
     measured on the first version's temporal windows (0.289 against 0.287).
3. **How a row was picked (minor): reproduced and applied.**
   - All 2,029 rows are the first candidate in file order, and 59.6% of company-years had 2 or more candidates.
   - The Spearman correlation of file position with date is 0.002 over the whole history (the verifier: 0.001).
   - Changes: one sentence added to the build bullet.
4. **Survivorship (minor): confirmed and applied.** us_stocks.csv lists UBER, ZM, LYFT and PINS. Sears Holdings,
   Windstream and Weatherford have no row. Anomaly bullet added.
5. **2012-06-15 (minor): confirmed and applied.** 223 rows (189 Moody's, 34 Fitch). That day holds 24,520 Moody's and
   4,687 Fitch entries, against at most 1,219 and 81 on other days. One sentence added to the agency bullet.
6. **Placeholders (minor): confirmed and applied.** grossProfitMargin is exactly 1 in 403 rows (401 after the drops)
   and FCF/OCF is exactly 1 in 171. Both are added to the bullet and kept, like the zeros.
7. **Window length:** moot under the grouped split.

### corporate_credit_rating_cat_data_set_ratings_raitings

**Outcome:** added and checked, from the book's original 197-row `ratings.csv`, not from OpenML 46372 (the record's
first link), which is generated. The independent verifier's verdict: ready with noted concerns; nothing blocks
shipping. The fix round applied all 8 findings (see the **Verification:** lines).

**Record judgment:** valid with concerns.
- The data first appeared on the data page of Baesens, Rösch and Scheule, *Credit Risk Analytics* (Wiley 2016,
  doi:10.1002/9781119449560): "The ratings data set is an anonymized data set with corporate ratings where the ratings
  have been numerically encoded (1 = AAA, etc.)", with six named ratios
  (http://www.creditriskanalytics.net/datasets-private2.html, section "Data Set Ratings").
- The books use it in chapter 8, "Low Default Portfolios" (SAS book pp. 213-236, chapter title and pages from
  Crossref). In the R Companion code for that chapter, the part headed "Mapping to an external rating agency" fits an
  ordered logit, `polr(rating ~ COMMEQTA + ... + SIZE, method = "logistic")`, and scores
  `notchdiff <- abs(rating - prediction)` (both shortened). Source: Ch08_LowDefaultPortfolios.R in
  github.com/dpicone1/Credit-Risk-Anaytics-The-R-Companion, a reader's transcription of the book's code. This is a
  real predictive task: map an unrated bank to an agency scale.
- OpenML 46372 (5,000 rows) is not usable: it is simulated from the 197 rows (issue 1). The record already suspected
  "likely modified"; the evidence below shows how it was made.
- Unique:
  - No folder of the working copy holds these columns or this file.
  - No other record carries OpenML 46372 or the ratings file. The book's other data sets have their own records:
    `lgd`, `mortgage`, `homeq_default_prediction` (retired).
  - `corporate_credit_rating` (Kaggle agewerc, being added by another agent) is different data. It has 2,029 ratings
    of US listed firms (2010-2016) with names, agencies, dates and 25 other ratios, and no column in common with this
    file. 9 of the 197 ROE values match one of its values at 5 decimals. The verifier puts chance at 10.1, and the
    matched firms are non-banks.

**Data:**
- Source: http://www.creditriskanalytics.net/uploads/1/9/5/1/19511601/ratings.csv, the link on the book's data page.
  - 197 rows x 8 columns: `spid`, `rating`, COMMEQTA, LLPLOANS, COSTTOINCOME, ROE, LIQASSTA, SIZE.
  - sha256 7cabb6bb...6cfcc. It is byte-identical to the copies in three GitHub repositories
    (dpicone1/Credit-Risk-Anaytics-The-R-Companion, JLZml/Credit-Scoring-Data-Sets,
    RHDZMOTA/5056a4a4-c7c4-4514-9bd4-91035ed5f2c4).
  - The page's `ratings.sas7bdat` holds the same values; it is not kept in the warehouse.
- Licence, as stated in two places:
  - The download form (http://www.creditriskanalytics.net/datasets.html): "I agree to use the data only in
    conjuction with the Credit Risk Analytics textbooks ... Commercial use is prohibited."
  - The site's terms (http://www.creditriskanalytics.net/terms.html): "You must not: Republish material from Credit
    Risk Analytics ... Redistribute content from Credit Risk Analytics".
- OpenML 46372 says CC BY 4.0. It was uploaded on 2024-11-20, from
  github.com/Polanitz/Multiclass-Classification-for-Corporate-Credit-Ratings (2022-02-03).
- The Medium article returns 403 to direct fetches; its Wayback copy (2022-11-21) was read. It calls the file "The
  diabetes data set [sic] ... originated from a credit risk analytics book" and links the 5,000-row file. It never
  says the rows were generated.

**Definition:**
- Folder: `datasets/_dev/tabarena-v0pt2/corporate_credit_rating_cat_data_set_ratings_raitings/`.
- Prediction point: a bank whose financial statements are known and whose agency rating is not (an unrated
  counterparty, or a check of an internal rating). The model maps the bank to the agency scale from six ratios.
- Target: `rating_notch`, the code from 1 (AAA) to 10, as regression (RMSE). Accepted warning:
  `task_target_low_cardinality`.
- Split: IID, the default 20 x 3 folds (131-132 train / 65-66 test rows). Each row is a different institution.
- Size: 197 rows x 6 features.
- Cleaning:
  - `spid` dropped: an anonymised id whose two numbering ranges no source explains (numbers in issue 3).
  - The six ratios are renamed after the data page's definitions; the column order is kept.
  - Nothing else changes: no missing values and no duplicates.
  - One size outlier (code 8, ln total assets 10.59) is kept and documented.
- One `_decisions` table: rows and ratio medians per code.
- Checksum v2:a70f14a0...4c0e, the same under pandas 2.3.3 and 3.0.6.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 infos.
- One warning accepted: `task_target_low_cardinality`. Reason: a 10-notch rating code that the R Companion's chapter
  8 code scores by notch differences (wine_quality precedent); as 10 classes, three codes would hold 3-5 rows.
- pytest `-k` on the folder: 2 passed (with `DATA_FOUNDRY_V2_DATA_CHECKS=1`; collection works again).
- ruff clean, the import check passes, and `dataset list` shows the folder.

**Probes:** scratch `probes/`; the verifier reproduced every number.
- Task probes (30 of 60 splits): no flags.
  - Linear R² 0.299 (skill +0.319, above the dummy on 100% of the splits).
  - Random forest 0.254, LightGBM 0.158.
  - Best single feature chosen per split: skill +0.026.
- Leak probes (untuned LightGBM, 3 splits): all features R² 0.103, `log_total_assets` alone 0.184.
  - Untuned LightGBM overfits 6 features on 131 rows, so I checked size on all 60 splits. A linear fit on size alone
    gives R² 0.178, against 0.286 for ridge on all six ratios, which is better on 88% of the splits. Size is the
    strongest ratio and the others add to it. No flag.
  - Exact feature copies across the split: 0%.
  - 1-NN, closest tenth: R² 0.562 on the probe's first split, which has 7 rows. Over all 60 splits the closest tenth
    shares its neighbour's code in 25.5% of cases, against 22.4% for all rows (the verifier, with another scaling:
    25.0% and 22.8%). There are no near-copy clusters, the artefact that retired the same book's HMEQ data.
- Number formats do not differ by rating. COSTTOINCOME and ROE are written with 5 instead of 6 decimals in 40% and 35%
  of the rows, unrelated to the code (Mann-Whitney p 0.82 and 0.42).
- Generated probes: no flags (0.0% of rows fit exactly, the same as a shuffled target).
- hidden_groups: no candidate column.

**Issues for Lennart:**
1. **OpenML 46372 is generated.** The record's first link and TabSTAR's copy should not be used.
   - The evidence (scripts in scratch `scripts/uniform_check.py`, `box_check.py`, `smote_check.py`):
     - Its 5,000 rows (500 per code) draw every ratio independently and uniformly between the minimum and the maximum
       of the book's rows with the same code. All 30,000 values lie inside those ranges.
     - The class means sit at the range midpoints (within 3% of the range).
     - 57 of 60 code-ratio cells pass a KS test against that uniform (p > 0.05; the other 3 have p 0.031-0.039).
     - Within-code correlations between the ratios fall from mean |rho| 0.21-0.42 to 0.03-0.04.
     - No row is a book row. The ids look random: 4 of its 4,969 match a book id.
   - The verifier added three facts:
     - A KS test against the book's own rows of the same code rejects in 33 of 60 cells, so the rows were not
       resampled from them.
     - SIZE has 6 decimals in 4,547 of 5,000 rows, against 4 decimals in 182 of 197 book rows.
     - The Medium article never says the rows were generated.
   - The boxes make the classes separable: LightGBM reaches a 10-class macro ROC AUC of 0.974 on that file, against
     0.66-0.67 for logistic regression and a random forest on the book's rows.
   - OpenML also labels the codes 1 = "very_bad" to 10 = "outstanding", the reverse of the book's "1 = AAA".
   - Implemented: the book's file.
   - The record could get the book's file link as its first source, and a note that the TabSTAR / OpenML version is
     simulated.
2. **Target framing: regression on the notch (implemented) or classification (the record's leaning, "likely
   classification").**
   - Regression is the only framing with neither a Too Small class nor an assumed mapping.
   - Implemented: regression.
     - The R Companion's chapter 8 code scores the ordinal model in notches.
     - The codes move with the ratios as a 1 = AAA scale should: Spearman with size -0.50, liquid assets -0.39,
       equity +0.26 (small banks hold more equity), loan-loss provisions +0.20, ROE -0.17, costs to income +0.10.
     - Ridge R² 0.286 on the shipped splits; RMSE 1.57 against 1.88 for the mean. Per the verifier, ridge beats a random forest on 75%
       of the splits (paired SE 0.012).
     - Each test fold scores 65-66 institutions; a 161-row regression already ships.
     - Codes 1, 2 and 10 hold 1-7 test rows per fold (median 4): 6% of the test rows, but 29% of ridge's squared
       error.
     - The R code reports absolute notch differences; I kept RMSE, the collection's default (and the TabArena
       adapter's only regression metric).
   - Alternatives (logistic regression, 3-fold x 10 repeats, log loss against the class-prior baseline):
     - (a) 10 classes as shipped: 1.888 against 2.023, macro AUC 0.669. Codes 1, 2 and 10 hold 3, 5 and 4 rows, so
       the rarest class has 1 row per test fold: Too Small. The precedents drop classes under 10 rows
       (ecoli_proteins, lung_cancer).
     - (b) Drop codes 1, 2 and 10: 185 rows, 7 classes. 1.678 against 1.837, macro AUC 0.716. This drops the ends of
       the scale and still leaves codes 3 and 9 at 4 rows per test fold, near the parkinsons line.
     - (c) Letter grades under a notch reading, 1-4 (AA- or better) / 5-7 (A) / 8-10 (BBB): 54/109/34 rows, 11 of
       the smallest per fold. 0.830 against 0.986, macro AUC 0.762. This depends on an unverified mapping of the
       codes: only "1 = AAA" is given.
3. **Provenance gaps (cannot verify without the book).**
   - The data page names no agency, years, country or selection.
   - The book text was not read. The use case and the notch meaning come from the R Companion code transcription and
     Crossref.
   - The data favour notches over letter grades. Read as letters (AAA, AA, A, BBB, BB, B, CCC, CC, C, D), the 57
     institutions with codes 7-10 would be rated CCC or worse, while codes 7, 8 and 9 have median ROE of 11%, 8% and
     10%.
   - The two `spid` ranges (100,079-130,277 for 130 rows, 300,021-453,328 for 67) may mark two populations
     (regions, id systems or agencies).
     - They carry a little code information: mean code 6.24 against 5.36 (Mann-Whitney p 0.001); ridge residuals
       +0.36 against -0.19 (p 0.06).
     - A range flag lifts ridge R² from 0.286 to 0.299 on the 60 splits.
     - Kept dropped: no source says what the ranges are.
   - The file is two blocks of 98 and 99 rows, each sorted by rating, with no institution in both. A random forest
     separates the blocks at ROC AUC 0.52, so they may be estimation and validation halves, or two years.
   - The same book's HMEQ data was retired for generation artefacts, and its LGD data is "slightly modified and
     anonymized". The 197 rating rows pass the checks that caught HMEQ (near-copies, formats by class; the
     verifier's nearest-neighbour distance does not predict the code, R² -0.12) and have real within-code
     dependence.
   - Chapter 8 (pp. 213-236), if PriorLabs has the book, would settle four things: the scale (is 10 = BBB-?), the
     agency, period and sample, whether the data were modified, and what the id ranges are.
   - Implemented: kept, with `Note` / `Anomaly` bullets.
4. **Name.**
   - The `unique_name` carries TabSTAR's label of the generated file: the "raitings" typo, "cat", and "corporate" for
     what are bank ratios (loan-loss provisions to loans, liquid assets to total assets).
   - Implemented: the record's `unique_name`, as the brief requires.
   - Alternative: rename the record and the folder (for example `credit_risk_analytics_bank_ratings`) before the
     first build, while it is cheap. The verifier agrees.
5. **Licence note (not a verdict reason).**
   - The download form allows use "only in conjunction with the Credit Risk Analytics textbooks" and prohibits
     commercial use.
   - The site's terms.html says "You must not: Republish material ... Redistribute content from Credit Risk
     Analytics".
   - Both are in `license`. Whether a public collection may redistribute the file is your call.
6. **Probe gap.**
   - `generated_probes.py` does not flag the 5,000-row file. I ran it as a scratch definition under
     `_scratch_new65/.../probe_root`: rule leaves cover 1.2% of the minority rows, no flag.
   - Drawing each feature independently within its class's range leaves neither mark the probe tests.
   - A within-class correlation check would catch it: mean |rho| 0.03-0.04 against a noise band of 0.09, and 0.21-0.42
     in the real rows. This fits the hepatitis_c_egypt agent's proposal, applied per class.

**Verification:** the verifier's 8 findings, each applied after re-checking its numbers (scratch
`scripts/fix_round_checks.py`, `scripts/outlier_check.py`).
1. Wording. Applied:
   - "the collection's floor of 10 rows per class" now reads "the 10 rows per class that the precedents keep
     (ecoli_proteins and lung_cancer drop smaller classes)".
   - The Spearman lists in the Target bullet and in `_decisions` now include equity +0.26 (explained by size, -0.51)
     and costs to income +0.10 (p 0.16). The decision table gained an equity column.
   - The accepted-warning reason and `_decisions` credit "the R Companion's chapter 8 code (a reader's
     transcription)" instead of "the book".
   - The `polr` / `notchdiff` lines are marked as shortened from the transcription.
2. `spid` information. Applied: the numbers are in the `spid` bullet and issue 3, with the two-populations note, and
   the drop is kept.
   - My shipped-split numbers differ slightly from the verifier's 3-fold x 20: ridge 0.286 -> 0.299 with the flag
     (better on 73% of splits); residuals +0.36 / -0.19, p 0.06 (verifier: p 0.038).
3. Licence. Applied: the terms.html clause is quoted in `license` (checked on the page today) and in issue 5.
4. Framing. Applied to issue 2 and the Target bullet: regression is the only framing with neither a Too Small class
   nor an assumed mapping; (b) leaves codes 3 and 9 at 4 rows per fold; the end codes are 6% of test rows and 29% of
   ridge's squared error (reproduced: 0.061 and 0.286).
5. OpenML evidence. Applied to issue 1 and the OpenML bullet: the KS rejection against the book's own rows (33 of
   60), the SIZE decimals, and the Wayback copy of the Medium article, which I read: "The diabetes data set [sic] was
   originated from a credit risk analytics book ... downloaded from here", linking the 5k file. It says nothing about
   generation.
6. Outlier. Applied: an `Anomaly` bullet for the code-8 institution with ln total assets 10.59 (next smallest 15.33)
   and the highest equity to assets (0.318), with the row kept. On the shipped splits ridge fits it (squared error
   0.34); read as a unit slip (+ln 1000) it would fit worse (14.5).
7. Name. Kept as issue 4 (Lennart's call).
8. Provenance. Applied to issue 3 and the Target bullet: the letter-grade reading is implausible (57 institutions at
   CCC or worse with median ROE of 8-11% in codes 7-9). The scale, agency, period and the id ranges stay
   cannot-verify until chapter 8 is read.
   - One correction to the verifier's wording: "median total assets about 66 billion" is the median of all 197 rows
     (ln 18.0). The 57 institutions of codes 7-10 have median ln total assets 16.6, about 17 billion if the unit is
     thousands.

### credit_card_customers
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/credit_card_customers/`)

**Record judgment:** valid with concerns; after the fix round I recommend `No` + `AHDS` + `Missing source information` (Lennart's call). The curator accepted the unknown source ("We have no real source information, but I think it is good to use for now. We can filter later"), so the folder stays until Lennart decides; removing it is Lennart's step.
- **The data looks constructed (criterion 4B, issue 1).** The verifier's dependence tests, which I re-ran with my own code, show the columns were not measured from one account history.
- **Window and closure (criterion 4D, issue 2).** The 12-month activity window may end at the account closure, the iranian_churn mechanism. Under issue 1 the question has no answer, since no account timeline exists.

Provenance found in this run: LEAPS sample case 11, "Predict Customer Attrition Using Naïve Bayes Classification" (Banking & Finance, dated 2020-04-19).
- Source: the Wayback Machine copy of `https://leaps.analyttica.com/_next/data/ePfrq2bdPNt6bd6-QrPvi/sample_cases.json`, snapshot 20200723073638.
- The case's subject explains the file's two naive Bayes columns. Kaggle topic 210078 names `https://leaps.analyttica.com/sample_cases/11` as the source of the column descriptions.
- Neither the case page nor its material is archived. By 2022 it was a paid case: id 9549, INR 2,500, `locked`.

Uniqueness:
- No duplicate in the working copy. `bank_customer_churn` is a different file: gauravtopre's ABC bank, 10,000 rows, other columns.
- No other record names BankChurners, `Attrition_Flag`, the slug or Analyttica.
- No other record of this run is this data.

**Data:**
- Source: Kaggle `sakshigoyal7/credit-card-customers`, version 1 (2020-11-19), one file `BankChurners.csv`, 10,127 rows x 23 columns. sha256 `c91b525a…b779`.
- Zenodo 10.5281/zenodo.4322342 (2020-12-15, uploader zhyli) is byte-identical (md5 `c8c0eb26…dad8`, checked). It is the pinned fallback in `download_description`.
- Licence: CC0-1.0 on the Kaggle page (data card / Croissant `license`). The Zenodo copy says CC BY 4.0.

**Definition:**
- Folder: `credit_card_customers`. IID binary classification, target `Attrition_Flag` (Attrited Customer 1,627 = 16.1%, Existing Customer 8,500). 10,127 rows x 19 features. Default splits: 3 x 3 folds, train 6,751-6,752, test 3,375-3,376. Metric roc_auc.
- Prediction point: at a snapshot, the bank scores each card customer from the profile and the last 12 months of activity, to contact likely closers first.
- Dropped columns:
  - `CLIENTNUM`: a masked id, unique per row; every value is 25k + 8.
  - The two `Naive_Bayes_Classifier_*` columns: posteriors of a naive Bayes model fit with the label. The record says "Remove NB features".
- "Unknown" stays a category in Education_Level, Marital_Status and Income_Category: the data card lists it as a value, and it is not random (Income Unknown: 1,060 women vs 52 men).
- Kept as published, with Anomaly bullets:
  - the 36-month spike in Months_on_book (2,463 rows);
  - Credit_Limit clipped at 5% / 95% (507 / 508 rows);
  - Total_Revolving_Bal capped at 2,517 (508 rows);
  - Avg_Open_To_Buy and Avg_Utilization_Ratio, which are exact functions of limit and balance.
- No duplicate rows.
- Two `_decisions` (the naive Bayes AUC table was removed on 2026-10-12: the column names settle that drop):
  - a figure of tenure against age and of the amount clusters;
  - the gender x income table.
- `data_tags = ("2ndTierData",)`: the tag exists in `data_foundry.schema.DataTags` ("Data that is not of the highest quality but still a reasonable task"); coffee_rating_prediction uses it.
- `download_description` order: `mkdir`/`cd` first, then the Kaggle command, then `# or, pinned:` with the Zenodo `wget`.
- The container checksum is identical under pandas 2.3.3 and 3.0.6 (`v2:ea8c64d7…0dc5`, after the fix round).

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). Nothing accepted.
- `ruff check`, `ruff format`: clean. Import check: ok.
- `pytest tests/test_v2_datasets.py -k credit_card_customers` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed (import and data rebuild) on the final definition (fix round, 2026-10-07). Collection worked this time.

**Probes** (2026-10-07, untuned models, outputs in `probes/`):
- Task probes (5 of 9 splits): LightGBM AUC 0.994 (log loss 0.078, dummy 0.441), random forest 0.987, logistic regression 0.923. The best single feature per split is Total_Trans_Amt (5 of 5 splits), at 0.877. Spread LightGBM vs linear +0.141 (paired SE 0.003). Smallest class per test fold 542 rows. **No flag**: 0.994 sits just under the `solved` cutoff of 0.995.
- Leak probes (3 splits):
  - all features 0.993;
  - alone: Total_Trans_Amt 0.876, Total_Trans_Ct 0.835, Total_Revolving_Bal 0.772, Total_Ct_Chng_Q4_Q1 0.753;
  - without Total_Trans_Amt 0.971, without Total_Trans_Ct 0.989;
  - depth-2 / depth-3 tree 0.862 / 0.920;
  - no missing values, 0.0% exact copies;
  - 1-NN agreement 0.920 / 0.886 / chance 0.730; NN distance alone 0.559.
- Extra block test (LightGBM, all 9 splits):

  | Columns | ROC AUC |
  |---|---|
  | 6 activity columns of the 12-month window | 0.980 |
  | profile (10) | 0.625 |
  | profile + 3 balance columns | 0.803 |
  | all but the two Q4/Q1 changes | 0.987 |

- Fix round, my re-runs of the verifier's model checks on the 9 shipped splits:
  - CatBoost default: AUC 0.9943 (per split 0.9914-0.9958), 3 of 9 splits at or above the 0.995 `solved` cutoff;
  - the best 2/3/4 columns: 0.94/0.97/0.98 (LightGBM default, 3 splits; the verifier has 0.938/0.969/0.980). No column is the label in disguise.
- Generated-data probe: 0 rule leaves (0.0% of the minority). No flag. This misses the marks of issue 1, as for hepatitis_c_egypt.
- Hidden groups: 5 candidates, no hit. Top: Months_on_book gap +0.002, Total_Trans_Ct −0.000, Customer_Age −0.001.

**Issues for Lennart:**
1. **The data looks constructed. I recommend `No` + `AHDS` + `Missing source information` (Lennart's call).**
   - Verifier finding 1, which I accept after re-running its key numbers with my own code (scripts `explore/fix1_check.py`, `fix1_homecredit.py`, `fix1_c2st_ref.py`):
     - **Count identity.** The 12-month count equals the Q4 count plus the Q1 count. Total_Ct_Chng_Q4_Q1, their ratio to 3 decimals, splits Total_Trans_Ct into two whole counts in all 10,127 rows. One of them is a rounding tie (51/80 = 0.6375 given as 0.638); the verifier counts 10,126.
       - Controls: shuffled totals give 523-592 rows (verifier: 587). Home Credit's real card statements give 9 of 8,920 (reproduced).
       - Q1 and Q4 cannot both be quarters, since that leaves no Q2 or Q3 transactions for anyone. Read as halves, the 7 customers without a second-half transaction would have at least 6 inactive months; they have 2-4.
       - On its own, the identity would fit a half-year reading. The proof is the joint picture: the identity plus the independences below.
     - **Inactivity.** Months_Inactive_12_mon is unrelated to the count: Spearman −0.051, within class 0.012 and 0.025. Home Credit gives −0.601 (reproduced).
     - **Spend vs limit.** The 12-month amount is unrelated to the credit limit: Spearman 0.028. Home Credit gives 0.447 (reproduced).
     - **Education.** A classifier tells the real rows from rows with Education_Level permuted within each class at AUC 0.495 (verifier 0.492). The same test on two real credit tables gives 0.578 (Home Credit) and 0.613 (Taiwan); the verifier has 0.587 and 0.621. Months inactive: 0.530 (0.527).
   - My earlier marks, from the raw file (2026-10-07):
     - **Tenure is bounded by age.** Outside the 2,463 rows at 36 months, Months_on_book ≤ Customer_Age − 4 in all 7,664 rows, and ≥ Customer_Age − 20 in 7,622. That is a parallelogram band with slope 1.006 months per year of age (r 0.893), although tenure only spans 13-56 months for ages 26-73. The only 445 rows above the bound are under-40s at the filled-in 36, so the 36 was written after the tenure was derived.
     - **Gender and income.** No woman has an income above $60K: 0 of 5,358, against 3,664 of 4,769 men.
     - **Missing dependences.** Education is independent of income (Cramér's V 0.028, p = 0.23). The single share is flat over age: 45% at 26-35, 43% at 56-73.
     - **Clusters.** Total_Trans_Amt falls in separated clusters: 2 rows in 10,500-12,000, and 746 rows above 12,000 with no attriter.
     - **Context.** LEAPS is a training platform, and its 2021 list calls another case's data "a dummy dataset".
   - Against: the generated-data probe finds no rule leaves, and nothing shows how the label was made.
   - Implemented:
     - the folder stays, with the extended Anomaly bullet (all numbers above) and decision 2 (figure plus text);
     - `data_tags = ("2ndTierData",)`;
     - the record comment now recommends `No` + `AHDS` + `Missing source information`.
   - Alternative: retire and remove the folder, as for ecommerce_shipping, customer_satisfaction_in_airline, churn, and in this run stroke_prediction and hepatitis_c_egypt.
2. **Prediction point: does the 12-month window end at the account closure?** That would be the iranian_churn mechanism.
   - The source does not say. The data card has "Last 12 months" and "if the account is closed then 1 else 0".
   - Kaggle topic 203290 (2020-12-14, 3 votes, never answered) asks it: "Are the statistics of transection history for attired customers the history just before they cancel the cards?" It is now cited in the bullet.
   - Signs that it does:
     - all 7 customers with zero Q4 transactions, and all 54 with 6 contacts, are attrited;
     - 55% of attriters have a zero revolving balance, against 19% of existing customers;
     - the six activity columns alone reach AUC 0.980 and all 19 reach 0.994, against 0.7-0.85 for typical churn tasks (iranian_churn 0.986).
   - Against: most attriters still transact in Q4 (median Q4/Q1 count ratio 0.53 vs 0.72), so the window does not run months past the closure.
   - Implemented: kept, with a "Potential leak, kept on purpose" bullet and a revisit condition (if the LEAPS case material turns up).
   - Alternatives:
     - retire (the iranian_churn call needed the paper's statement, which does not exist here);
     - drop the activity block (profile + balance: AUC 0.803). That is a fix of our own invention, so I do not recommend it (task_probes rule 6).
   - Either way the task is near its ceiling: LightGBM log loss 0.078, and CatBoost default reaches 0.9943 with 3 of 9 splits at or above 0.995. Tuned methods may trip `solved` and tie.
3. **Provenance is a teaching case, not a bank release.** The curator's acceptance stands, so the dataset was added. Counter-argument: the guidelines' "Missing source information → No" fits.
   - The trace bottoms out at LEAPS case 11, whose material is gone. No bank, country or period is named anywhere. Kaggle topic 215382 "Country of research" (17 votes) has no answer.
   - The paper linked in the record only uses the data, as its comment says.
4. **Minor: two filled-in or ambiguous values kept as published.** Fix round: the 36-month bullet now says the age distribution is close, not equal (mean 46.2 vs 46.4, KS p = 0.015). The block bullet names Credit_Limit among the 10 profile columns. The source paragraph adds LEAPS case 2 (decision tree, the same day) and case 9574 (logistic regression, 2021-11-18), both credit card attrition, both checked in the archived lists.
   - Months_on_book = 36 in 2,463 rows. About 2,100 of them are filled in: the neighbours hold 317-358 rows each, and the 36s break the tenure-age bound. Alternative: set all 36s to NaN, losing about 340 true 36s.
   - "Unknown" kept as a category rather than NaN, following the data card and the pva precedent. Most pipelines treat the two alike.
5. **Pointer and build steps left to the orchestrator:**
   - the record's `v2_path` (`sync-notebooks`) is not set;
   - not built, so there is no UUID, CHANGELOG entry or README table row yet.
   - Raw data: `local-data-warehouse/credit_card_customers/BankChurners.csv` (1.5 MB).

### dataorg_financial_health_prediction_challenge

**Outcome:** added and checked, without the Lesotho rows (fix round, 2026-10-07).
Folder: `datasets/_dev/tabarena-v0pt2/dataorg_financial_health_prediction_challenge/`.

**Record judgment:** valid with concerns.

The data is real, unique and traceable. The rows are FinMark Trust's FinScope MSME surveys; Zindi does not name them. Train.csv plus Test.csv match these surveys:

| Country | Survey | Interviews in the report | Rows in the competition | Report location |
|---|---|---|---|---|
| Eswatini | FinScope MSME 2023 | 3,343 | 3,343 | PDF p. 15 |
| Lesotho | FinScope MSME 2023 | 2,430 | 2,430 | pp. 14-15 |
| Zimbabwe | FinScope MSME 2022 | 3,265 | 3,265 | methodology slides |
| Malawi | FinScope MSME 2019 | 2,993 (fieldwork 8 April to 17 May 2019) | 2,985 | p. 12 |

No folder of the working copy and no other record uses FinScope MSME data.

There are two concerns:
- Lesotho's label runs against the index. I implemented a drop of the Lesotho rows (issue 1).
- The label is a rule on the product columns plus a residual. I kept those columns (issue 2).

**Data:**
- Source: Zindi needs a login, so I used the Kaggle copy `muhammadbehroz/dataorg-financial-health-prediction-challenge`, pinned to version 1. It is the unzipped Zindi zip, including Zindi's manifest.
- Checks on the copy:
  - The byte sizes equal the Zindi API's `datafiles` field.
  - Train.csv has the same sha256 (`7e3ea585…48d5`) in 3 Kaggle uploads and 1 GitHub upload.
  - The verifier re-ran `download_description` verbatim and got equal hashes.
- Files read: Train.csv (9,618 × 39). VariableDefinitions.csv is kept as documentation.
- Licence: "Data Sharing: CC-BY SA 4.0 license" (Zindi rules page).

**Definition:**
- Prediction point: one owner interview. It covers the owner's profile and attitudes, the business's size and practices, and its financial products.
- Target: `financial_health` (Low / Medium / High). Metric: log loss; the competition scored weighted F1. Split: IID, 3 × 3 stratified folds of 5,116 train and 2,558 test rows.
- Shape: 7,674 rows × 37 features (32 categorical, 6 numeric). Classes: Low 5,106, Medium 2,104, High 464.
- Cleaning:
  - Dropped `ID` and Lesotho's 1,944 rows.
  - Unified the 7 spellings of "Don't know" and the curly apostrophes.
  - Eswatini `current_problem_cash_flow`: "0" → "No".
  - Malawi: business years NaN → 0 for 225 businesses under a year.
- Domain: now `finance`. The record says `business & marketing` (issue 3).
- The checksum `v2:fadd2101…dee4c` is the same under pandas 2.3.3 and 3.0.6.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info.
- `pytest -q tests/test_v2_datasets.py -k dataorg`: passes, also with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- ruff check, ruff format and the import check: clean.
- Not run: `sync-notebooks`, which sets the record's `v2_path`, and `build`. Both are curator steps.

**Probes (after the drop):** no flags anywhere.
- Leak probes, macro AUC:
  - All features 0.951; depth-2 / depth-3 trees 0.831 / 0.870.
  - `funeral_insurance` alone 0.790; all features without it 0.869.
  - No missing-value indicator above 0.623.
  - No test row has an exact copy in train.
  - 1-NN label agreement: 0.930 in the closest tenth and 0.776 overall, against 0.522 by chance. This is the product rule (issue 2).
- Task probes:

  | Model | Macro AUC | Log loss |
  |---|---|---|
  | Random forest | 0.957 | 0.288 |
  | LightGBM | 0.952 | 0.303 |
  | Linear | 0.922 | 0.412 |
  | `funeral_insurance` alone | 0.784 | 0.508 |
  | Class shares (dummy) | — | 0.796 |

  The smallest class in a test fold has 154 rows.
- Generated-data probe: no rule leaves.
- Hidden groups: no hits (gaps ≤ 0.008).

**Issues for Lennart:**

1. **Lesotho's label runs against the index. Implemented: drop the 1,944 Lesotho rows.**
   - The comparison is among Lesotho businesses asked the same question: share of Medium or High with the answer vs without it.

     | Answer | Lesotho, with vs without |
     |---|---|
     | Loan account | 0.17 vs 0.21 |
     | Debit card | 0.12 vs 0.34 |
     | Internet banking | 0.17 vs 0.21 |
     | Motor insurance | 0.19 vs 0.40 |
     | Income-tax compliance | 0.25 vs 0.40 |

   - In Eswatini, Malawi and Zimbabwe each of these answers goes with a higher class.
   - In Lesotho the class also falls with income (Spearman −0.12, −0.11 and −0.11 for income, expenses and turnover; +0.14 to +0.24 elsewhere).
   - Models trained on any two of the other countries score the third at AUC 0.63-0.68 and Lesotho at 0.46.
   - The FinScope Lesotho report says "formal MSMEs exhibit greater financial health" (p. 53), the opposite of what the released labels show.
   - The label is learnable within Lesotho (log loss 0.520 against 0.671 for the class shares). So it was built differently, not at random.
   - **Alternative A:** keep Lesotho as released. That needs an `Anomaly:` bullet saying the label looks inverted against formal finance and income. It also needs the Lesotho sentinel fixes from the first round restored: amounts of 97 and owner age 99 → missing. With Lesotho, LightGBM log loss is 0.317; without it, 0.260.
   - **Alternative B:** remap the labels. Not possible: I found no exact inversion.
     - Swapping Low and Medium leaves Lesotho at AUC 0.54 for a model trained on the other three countries.
     - Reversing the order would make 60% of Lesotho's businesses High.
   - The "Never had" ↔ "Used to have" swap I flagged in round 1 is harmless. The verifier's LightGBM log loss is 0.3167 either way; mine is 0.3177 vs 0.3176.
   - data.org or FinMark Trust could say how Lesotho's FHI was computed.

2. **The product columns are inputs of the index. Implemented: keep them.**
   - Results on the shipped splits after the drop:

     | Model | Log loss | Accuracy | vs LightGBM on all columns |
     |---|---|---|---|
     | Depth-3 tree, country + 11 product columns | 0.373 | 0.888 | worse on 9 of 9 splits |
     | Depth-5 tree, same columns | 0.301 | 0.910 | worse on 9 of 9 splits |
     | Depth-6 tree, same columns | 0.285 | 0.916 | worse on 9 of 9 splits |
     | LightGBM, all columns | 0.260 | 0.917 | — |
     | LightGBM, country + 11 product columns | 0.255 | — | better on 7 of 9 splits |
     | LightGBM, the 26 other columns | 0.695 (macro AUC 0.752) | — | — |
     | Class shares | 0.796 | — | — |

   - Within identical (country + 11 product) profiles, the majority class covers 0.938 of the rows. It was 0.899 with Lesotho.
   - The label is therefore a rule on the products plus a residual, not a deterministic function. It is not Trivial under rule 4: the depth-6 tree is worse on 9 of 9 splits.
   - **Alternative:** drop the 11 product columns (0.695 against 0.796 for the class shares), or answer No.

3. **Domain.**
   - The definition now uses `finance`. The record has `business & marketing`.
   - Reasons for `finance`:
     - Zindi's API tags the competition `industry: ["Financial Services"]`.
     - The label is a financial-health index.
     - The neighbouring sets use `finance`: african_credit_scoring_challenge, polish_companies_bankruptcy, taiwanese_bankruptcy_prediction.
   - The record should follow, or I revert.

4. **Year.**
   - `year = "2025"`, the competition and release year. The surveys are from 2019-2023.
   - This is the open year-convention question.

#### Verification (fix round, 2026-10-07)

The verifier said "needs changes". It upheld the IID split, the cleaning, the download, the licence and uniqueness. Each finding:

- **1 (major), Lesotho: accepted and implemented.**
  - I checked it with my own code: `b1_lesotho_check.py`, `b3_lesotho_more.py`, `b4_swap_check.py`.
  - I compared within the businesses asked each question; the verifier compared against all other rows. The direction is the same both ways.
  - My transfer test used the 10 columns every country asked, with amounts as within-country percentiles. Lesotho scores 0.46; the other countries score 0.63-0.68 among themselves.
  - Lesotho is dropped in `_clean`, with an evidence bullet and a `_decisions` table built from the raw file.
  - The Lesotho-only sentinel code and its two decisions are removed.
- **2 (minor), the label as a rule: accepted.**
  - The 24-cell lookup numbers are replaced by the tree numbers and the majority ceiling, recomputed after the drop.
  - The alternative of dropping the products is kept.
- **3 (minor), Malawi: accepted.**
  - FinScope MSME Survey Malawi 2019 report, p. 12: "n=2,993"; fieldwork 8 April to 17 May 2019.
  - This is now in the comments and in the bibtex note.
- **4 (minor), wording: accepted.**
  - The "Lesotho AUC 0.68" and "97 in Lesotho rows only" claims are gone with the Lesotho bullets.
  - The answer-spelling bullet now says "seven ways (up to three in one column)", verified per column and country.
- **5, domain:** I changed it to `finance` (issue 3).

### diabetes_3
**Outcome:** added and checked

**Record judgment:** valid with concerns. The data first appeared with Efron, Hastie, Johnstone & Tibshirani (2004),
"Least angle regression", Ann. Statist. 32(2), doi:10.1214/009053604000000067 (read in the arXiv reprint
math/0406456).
- Sec. 1 states a predictive task: "The statisticians were asked to construct a model that predicted response y from
  covariates x1, x2, ..., x10. Two hopes were evident here, that the model would produce accurate baseline predictions
  of response for future patients".
- Sec. 7 places the file on Hastie's Stanford page: "the diabetes data also appears there". The page has held it since
  2002.
- Unique: no folder of the working copy and no other record holds it (grep for 44223, 44187, var.select, Efron,
  "least angle", load_diabetes; the diabetes_* records are other datasets). No record of this run matches. OpenML
  44223 (and the test upload 44187) is scikit-learn's centred and scaled copy of the same 442 rows.
- The concern is the cohort (issue 1): the data does not look like the "442 diabetes patients" the paper describes,
  and no source documents the clinic, the units or the response.

**Data:** `diabetes.data` (tab-separated, 442 rows x 11 columns, headers AGE SEX BMI BP S1-S6 Y; md5
af0c583c28547d76cd2db5f5c67de7e8) in `local-data-warehouse/diabetes_3/`.
- The original is https://hastie.su.domains/Papers/LARS/diabetes.data. That host refused connections on 2026-10-07;
  the Wayback Machine last captured it live on 2026-08-04, with the same SHA-1 as our file.
- We download the Wayback capture of 2021-10-21, which is byte-identical to the 2010 and 2026 captures and to Dennis
  Boos's NCSU copy. `download_description` names the NCSU copy as the fallback for when the Internet Archive is
  offline (it was, intermittently, on 2026-10-07).
- `sklearn.datasets.load_diabetes(scaled=False)` returns the same values.
- Licence: none stated on the LARS page or in the paper. The R package lars (GPL-2) and scikit-learn (BSD-3-Clause)
  redistribute the data.

**Definition:** `datasets/_dev/tabarena-v0pt2/diabetes_3/`.
- Prediction point: the baseline visit; all ten features are baseline measurements, so no column is dropped.
- Target `disease_progression_one_year`, the paper's response on its own scale (25-346), regression with RMSE.
- IID, default splits: 20 repeats x 3 folds, train 294-295 and test 147-148 rows. 442 rows x 10 features.
- Cleaning: the columns are renamed to what they measure (age, sex, bmi, mean_arterial_pressure, total_cholesterol,
  ldl_cholesterol, hdl_cholesterol, total_cholesterol_hdl_ratio, log_triglycerides, glucose); `sex` is categorical
  (codes 1/2). Nothing is dropped or filtered: no missing values, duplicate rows or repeated feature vectors.
- The names spell out the authors' own headers in the 2002 version of the file (`age sex bmi map tc ldl hdl tch tg glu
  y`). The data confirms them row by row (decision 1):
  - Friedewald LDL within 0.1 in 438 of 442 rows and within 0.5 in all, so S5 = ln(triglycerides).
  - S4 = S1/S3 (rounded) in 429 rows.
  - 3 x BP is a whole number in all 442 rows, as for a mean arterial pressure.
- Anomaly (decision 2): S4 has decimals in 62 rows and BP is in thirds in 42 (39 both). This may be two recording
  batches, but it carries no target signal (R^2 0.0009). Kept as written.
- Row order: the raw file has no time order (lag-1 autocorrelation of Y 0.043, permutation 95% band -0.097 to 0.093),
  and there are no dates, so the split is IID.
- pandas 2.3.3 and 3.0.6 (the shared pd3 venv) give the same checksum (value in the final message and README).

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 accepted.
- `meta_license_unknown` (license = None) is accepted because neither the LARS page nor the paper states a licence;
  lars (GPL-2) and scikit-learn (BSD-3-Clause) redistribute it.
- `pytest tests/test_v2_datasets.py -k diabetes_3`: 2 passed, including the raw-data rebuild with
  DATA_FOUNDRY_V2_DATA_CHECKS=1.
- The import check and `dataset list` pass. No TODO is left.

**Probes:** no flags from any probe. Output is in `probes/` of this folder; the verifier re-ran them with the same
numbers.
- Leak (3 splits, LightGBM): all features R^2 0.406; shallow tree 0.343 / 0.321; bmi alone 0.273,
  log_triglycerides 0.272; dropping bmi gives 0.316. No missing values and 0.0% test rows with a copy in train.
- Task (30 of 60 splits): linear 0.480, random forest 0.450, LightGBM 0.371, single feature 0.234 (bmi 16, ltg 11,
  BP 3). Linear beats the dummy on 100% of splits (SE 0.010); spread linear - LightGBM 0.109 (paired SE 0.009).
- Generated: 7.2% exact fits against 6.8% for a shuffled target; no `formula` flag.
- Hidden groups: no hit. The top candidate, glucose (gap +0.107: random 0.385, by value 0.278), is a measurement
  that every new patient has, not an entity.
- Rule 4 by hand, all 60 shipped splits (`trivial_fold_by_fold.py`): the best single feature, chosen on each training
  side with a straight-line fit, scores R^2 0.300 (0.141-0.412); the best of OLS, ridge and a random forest scores
  0.485 (0.371-0.592). The single feature is below on 60 of 60 splits, by at least 0.097.

**Issues for Lennart:**
1. **The cohort may not be diabetes patients, and nothing documents it (major; criterion 4E against your recorded
   acceptance).**
   - Evidence: the paper's only cohort fact is "442 diabetes patients" (Sec. 1, Table 1). Read as fasting plasma glucose
     in mg/dL, `glucose` runs from 58 to 124 (mean 91, a smooth distribution with no cutoff). No patient reaches the
     126 mg/dL threshold, 94 are in 100-125 and 348 below 100. Median BMI is 25.7 and median triglycerides 102 mg/dL,
     which looks like a general adult population.
   - No source gives the units, the clinic, the inclusion rule or how "a quantitative measure of disease progression
     one year after baseline" is computed. So we cannot check what y measures or whom a model would serve.
   - "Missing source information" does not apply: the file traces to the authors' page (2002) and the paper.
   - Implemented: kept, with an `Anomaly, cohort:` bullet in `curation_comments`.
   - Alternative: retire for lack of information (4E), or ask Efron/Hastie where the data and y come from.
2. **The `Trivial` marker is not supported.** The question is whether the record should drop it. By rule 4, one feature
   would have to match the methods fold by fold; it does so on 0 of 60 splits (R^2 0.30 against 0.49). The verifier's
   independent check (line, spline or LightGBM on the CV-chosen feature) stays below OLS, ridge and a random forest on
   60 of 60 splits, by at least 0.080. Methods spread, and the paper's least-squares fits reach an in-sample R^2 of
   about 0.50 (Sec. 3.4). Implemented: an ordinary tiny-data IID regression.
3. **Column names: resolved, no decision needed.** The 2002 version of `diabetes.data` carries the authors' own
   headers `age sex bmi map tc ldl hdl tch tg glu y`. Its other nine columns and y equal ours, and ln(tg) = S5 within
   5e-5. The definition spells these headers out: `map` is `mean_arterial_pressure` (all non-whole BP values are
   thirds, (SBP + 2 DBP) / 3), and `tg` is `log_triglycerides`, since the 2003 file logs it as the paper's Table 1
   does. Alternative: the authors' short names as they are.
4. **Source link: resolved.** `source_url` is now the paper's DOI (the LARS host is down). The LARS page, the pinned
   2021 capture and the NCSU fallback are in `download_description`.
5. **The `sex` coding is undocumented.** Implemented: the codes 1 and 2 kept as categories (the 2002 file codes the
   same split 0/1). Code 1 has higher HDL (54.4 against 44.6 mg/dL) and lower blood pressure, which suggests
   1 = female. Alternative: label the codes female/male on that evidence (an inference, not a documented fact).
6. **The target is not logged.** The data check's distribution hint prefers lognormal (skew 0.44 raw, -0.33 logged;
   AIC 5221.9 lognormal against 5343.0 exponential). Implemented: raw scale, as the paper fits it by least squares.
   Alternative: `log_disease_progression_one_year`. The tail is short (25-346), so I see no need.

**Verification:**
1. Applied: the `Anomaly, cohort:` bullet with the glucose (58-124, 0 at 126+, 94 in 100-125), BMI and triglyceride
   numbers, which I recomputed. Made issue 1. The dataset stays.
2. Applied: confirmed the 2002 file (headers, sex 0/1 = 1/2, ln(tg) = S5 within 5e-5, nine identical columns), and
   that all 42 non-whole BP values end in .33 (24) or .67 (18). The file is cited in the renaming bullet and decision
   1. Renamed `average_blood_pressure` to `mean_arterial_pressure`, and added the 3 x BP row to decision 1.
3. No change needed: the verifier's independent Trivial check agrees. Issue 2 keeps the proposal to drop the marker.
4. Applied: `source_url` is the DOI. The date is fixed (last live capture 2026-08-04; same SHA-1 digest
   SICPCB3L... as our file), and the NCSU copy is the fallback in `download_description`.
5. Applied: the ratio is "given with decimals in 62 rows (59 to two decimals, 3 to one)"; the paper's R^2 0.50 is
   called in-sample.

### differentiated_thyroid_cancer_recurrence
**Outcome:** added and checked

**Record judgment:** valid with concerns. One row per patient: the 383 rows are the paper's 383 patients and the 383 differentiated cancers (papillary, micropapillary, follicular, Hurthle cell) of a 400-patient cohort followed after thyroidectomy at the endocrine clinic in Hamadan, 2008-2023 (Khazaei et al. 2024, J Res Health Sci 24(4):e00632, doi 10.34172/jrhs.2024.167, CC BY, PMC11492527, senior author Borzouei, the UCI creator; its Table 2 matches the file's pathology counts 287/48/28/20 with 90/0/12/6 recurrences and ATA risk counts 249/102/32 with 12/64/32). So the record's "might be panel / longitudinal data" does not apply: the follow-up is summarised in one label and IID is right. Unique: no other record or working-copy folder holds UCI 915 / DOI 10.24432/C5632J / OpenML 46605; `thyroid_discordant` and `new_thyroid` are the Garvan thyroid-disease data, a different cohort. Concerns: `Response` is a near-copy of the outcome (dropped, issue 1), the radiotherapy column is undefined (dropped, issue 6), and the paper's definition of recurrence could not be read (paywall, issue 2).

**Data:** UCI dataset 915, static zip `https://archive.ics.uci.edu/static/public/915/differentiated+thyroid+cancer+recurrence.zip` with one file, `Thyroid_Diff.csv` (sha256 a2c65f7c8fa0e78a65aa4946961aafd45218c92760d10375fe2c778045c97b44), 383 rows x 17 columns (16 features + `Recurred`), no missing values. Licence CC BY 4.0, stated in the "License" section of the UCI page. OpenML 46605 is a 2025 re-upload whose `original_data_url` points to UCI (same rows, same order per the verifier). The paper's own data statement says "available from the corresponding author on reasonable request"; the authors (UCI creators Borzooei, Tarokhian) donated it to UCI.

**Definition:** `datasets/_dev/tabarena-v0pt2/differentiated_thyroid_cancer_recurrence/`. Prediction point: after initial therapy, at the initial staging when the ATA risk is assigned; the model predicts recurrence over the follow-up of at least 10 years. Target `Recurred` (108 yes, 275 no; ROC AUC). IID, default splits 20 x 3 (train 255-256, test 127-128 rows). 383 rows x 14 features (`Age` numeric, 13 categorical). Cleaning: drop `Response` (response to therapy, assessed during follow-up; issue 1) and `Hx Radiothreapy` (undefined, undated, looks like treatment of advanced disease; issue 6); fix the typo "Hurthel cell" -> "Hurthle cell"; keep the duplicate rows (issue 4); keep `Stage` and `M` as recorded despite 12 stage mismatches and 2 M1 patients at intermediate risk (issue 5). Three `_decisions` tables: recurrence by response category, the radiotherapy rows, the duplicate counts.

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info (`dataset_conflicting_duplicate_rows`: one profile, three patients, both labels; kept and documented). Accepted: `dataset_duplicate_rows` (26 copies, 6.8%), reason: the 383 rows are the paper's 383 patients, the copies are women with a low-risk tumour who did not recur (the most common record of 14 coarse fields), chance gives 23 duplicate feature vectors (95% range 17-30) against 27 observed, and leaving the copied test rows out lowers ROC AUC by 0.002-0.003 on the 60 shipped splits. Same checksum under pandas 2.3.3 and 3.0.6 (`v2:7d8cc1ff95176206be097909ff1a66e6f1fd969152e21bd1b44032049582b829`, as in the README). `pytest tests/test_v2_datasets.py -k differentiated_thyroid_cancer_recurrence` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed. Imports; `dataset list` shows it as checked. ruff check and format clean. No `TODO` left. The record has no `v2_path` yet (`sync-notebooks` is the orchestrator's step).

**Probes:** (final version, 14 features; outputs in `probes_final/`)
- leak (3 splits, LightGBM): all features 0.914; depth-2 / depth-3 tree 0.892 / 0.886; alone: ATA `Risk` 0.896, `N` 0.823, `T` 0.789; without `Risk` 0.887; no missing values; 8.6% of test rows have an exact feature copy in train; 1-NN label agreement 0.923 (closest tenth), 0.844 (all), chance 0.595; label-free nearest-neighbour distance 0.804.
- task (30 of 60 splits): random forest 0.932, logistic 0.924, LightGBM 0.919, best single feature 0.878 (`Risk` on 25 splits, `T` 4, `N` 1), dummy log loss 0.595; best family beats the dummy on 100% of splits; smallest class per test fold 36 rows; **no flags**.
- generated: rule leaves 0.0% of the minority; no flags.
- hidden groups: one candidate (`Age`, gap +0.000: random 0.824, grouped 0.824); no hit.
- Rule 4 (`Trivial`), my own run on all 60 shipped splits: `Risk` alone (train-side rate per level) 0.896 against logistic regression 0.929, random forest 0.929 and untuned CatBoost 0.932, which beat it on 59, 59 and 60 of 60 splits (CatBoost's mean paired gain 0.036, SE 0.002). Best two-feature lookup `Risk` x `Gender` 0.917, beaten by the best of the three on 54 of 60. Depth-2/3 trees 0.890/0.896. Not trivial.
- The label-free distance score (0.804 against 0.914 for the full model) comes from the uniform low-risk records: 0.63 within the ATA low-risk group. No generated-data mark. No action.
- With `Response` kept (scratch copy of the earlier 16-column definition, outputs in `probes_with_response/`): leak all features 0.988, `Response` alone 0.973, without `Response` 0.909, depth-2 tree 0.952; task LightGBM 0.987, random forest 0.985, no flags; generated probe **flags `rule_leaves`**: two pure leaves hold 40.9% of the recurred patients. Answered by dropping `Response` (issue 1).

**Issues for Lennart:**
1. **`Response` (response to therapy) dropped: confirm the prediction point.** Evidence: the data creator's group says it "was determined based on the laboratory findings of thyroglobulin and antithyroglobulin and a whole-body scan" (Khazaei et al. 2024, Methods), i.e. a post-treatment assessment. Tuttle et al. 2010 (Thyroid 20:1341; cited by the source paper; abstract, Methods): ATA risk is assigned "as part of initial staging", and "Clinical data obtained during the first 2 years of follow-up (suppressed thyroglobulin [Tg], stimulated Tg, and imaging studies) were used to re-stage each patient based on response to initial therapy". ATA 2015 guidelines (Haugen et al. 2016, Thyroid 26:1), section [B29]: "Structural incomplete response: persistent or newly identified loco-regional or distant metastases", which is the outcome. In the file 89 of 91 structural-incomplete patients recurred, 1 of 208 with an excellent response. ROC AUC (10 x 3 folds, raw file): `Response` alone 0.978; `Response` + `Risk` 0.989 (logistic), above all 16 columns (0.983-0.987); without `Response` 0.911-0.932. Implemented: dropped; the task predicts at initial staging. Alternatives: (a) keep `Response` as a "dynamic risk at the first response assessment" task: near-trivial (two features beat all) and flagged by the generated probe; (b) keep `Response` but only patients without structural disease at that assessment: 292 patients with 19 recurrences, about 6 per test fold, `Too Small`. Supporting inference (not verified): the file uses the 2015 ATA categories (Tuttle 2010 still used excellent / acceptable / incomplete), while every patient was diagnosed at least 10 years before the 2023 paper, so the categories were probably assigned from the records with the follow-up known.
2. **The definition of the label is not verified (paper paywalled).** `Recurred` seems to include persistent disease: all 18 M1 patients and all 32 ATA high-risk patients are labelled recurred (Tuttle 2010: "Persistent structural disease or recurrence" in 68% of high-risk patients), and 89 of 91 structural-incomplete responses. Khazaei et al. do not define recurrence either ("mainly local involvement"). The task stays valid either way: the ATA initial risk system estimates "the risk of persistent/recurrent disease" (ATA 2015, [B19]); this is now in the `Note:` bullet. The Springer page, its Wayback snapshot (2025-12-29) and Europe PMC (PMID 37902840) show only the abstract; ORBi UMONS and ORBi ULiège serve "Request a copy". Please get the PDF (Google: `"Machine learning for risk stratification of thyroid cancer patients: a 15-year cohort study" pdf`) and check how recurrence, the response and the radiotherapy column were defined and when each variable was recorded, and which 13 features the paper used.
3. **`Trivial` marker:** without `Response` the task does not meet rule 4's test for `Trivial`. On the 60 shipped splits `Risk` alone gives 0.896; logistic regression 0.929, random forest 0.929 and untuned CatBoost 0.932 beat it on 59, 59 and 60 splits (CatBoost's mean gain 0.036, SE 0.002); the best two-feature lookup, `Risk` x `Gender`, gives 0.917 and is beaten by the best of the three methods on 54 of 60. No task-probe flags. The marker came from the paper's numbers, which probably include `Response` (issue 2). Proposal: remove the marker or note it as answered (record comment drafted).
4. **Duplicates kept.** 26 exact copies (22 profiles, 6.8%), all low-risk women who did not recur. Chance test: permuting `Age` within ATA risk x sex (2,000 draws) gives 23.2 duplicate feature vectors on average (95% range 17-30) against 27 observed (p = 0.16), so the copies are the repeats expected among distinct patients. 9.3% of test rows have a copy in train; dropping them from test lowers AUC by 0.002-0.003. Implemented: kept, warning accepted. Alternative: drop the copies (357 rows).
5. **`Stage` and `M` anomalies.** `Stage` follows AJCC 8th edition from `Age`, `T`, `N`, `M` in 371 of 383 rows; of the other 12, two match the 7th edition and ten match neither (e.g. age 26 with M1 recorded as stage I; 8th edition 371 matches, 7th 279). 2 of the 18 M1 patients (ages 26 and 37) are ATA intermediate risk although distant metastases are ATA high risk (Tuttle et al. 2010, Table 1), so their M1 may have been found after the initial staging. Dropping `M` and `Stage` changes logistic-regression AUC by +0.001. Implemented: kept as recorded (`Anomaly:` bullet). Alternative: recompute the stage from AJCC 8th, or drop `M` and `Stage`.
6. **`Hx Radiothreapy` dropped (new after verification).** No source defines or dates it (UCI variable table empty; Khazaei et al. do not list radiotherapy among the collected variables). 6 of its 7 "Yes" rows are ATA high-risk male smokers, 5 with M1, 5 aged 61-81, all recurred; the seventh is a 25-year-old low-risk woman who did not. That fits external-beam or palliative radiotherapy for advanced disease (possibly after the prediction point), though an earlier head-and-neck radiotherapy (e.g. for another cancer in older smokers) fits too. On the 60 splits of the version that kept it, logistic regression scores 0.930 with and without it (random forest 0.928 and 0.929). Implemented: dropped. Alternative: keep it with a `Potential leak, kept on purpose:` bullet and revisit once the paper's variable definitions are read.

**Verification:** (independent verifier: "ready with noted concerns", 6 minor findings; all applied)
1. Applied: Khazaei et al. 2024 read and checked myself (Methods quotes; Table 2 counts match the file); cited in the opening sentence, the `Response` bullet and the record comment.
2. Applied: `Hx Radiothreapy` dropped with a bullet and a `_decisions` table (6 of 7 "Yes" rows high-risk male smokers, 5 M1, all recurred; LR 0.930 with and without); keeping it as a potential leak is listed as the alternative (issue 6).
3. Applied: the `Anomaly:` bullet now names the 2 intermediate-risk M1 patients; recomputed on the final splits, dropping `M` and `Stage` changes LR AUC by +0.001 (the verifier had +0.0003 on the earlier splits).
4. Applied: chance test rerun on the final frame (23.2 on average, 95% range 17-30, observed 27, p = 0.16), added to the duplicates bullet and the accepted-warning reason.
5. Applied: the `Note:` bullet now says the task is valid whether or not `Recurred` counts persistent disease (ATA 2015 [B19], quote checked).
6. Applied: the numbers are recomputed on the final 14-feature splits (CatBoost 0.932 beats `Risk` on 60 of 60; `Risk` x `Gender` 0.917, beaten on 54) and added to issue 3 and the `Not trivial` bullet.

### digicow_farmer_training_adoption_challenge

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/`).
- Recommended for retirement after the independent verification: suggestion `No`, markers `Too Small` and
  `Data Quality Issue`.
- The folder stays for Lennart's decision, and its text carries the evidence.

**Record judgment:** do not ship.
- Data Quality Issue: the label records adoption only where and when DigiCow recorded it. A 0 therefore mixes "did
  not adopt" with "not recorded" (leak_checks.md §3, the ghanas_indigenous_intel precedent).
- Too Small: the temporal windows hold 9, 5, 19 and 103 adopters, from 3, 3, 8 and 52 sessions and 1, 1, 2 and 7
  trainers.
- No split design fixes either problem.
- The source itself is fine: the Zindi DigiCow challenge, 2026-01-28 to 2026-03-01, from DigiCow Africa and Digital
  Africa. It is the first appearance of the data, no other record or working-copy folder holds it, and the task is
  predictive.

**Data:**
- Train.csv (13,536 rows x 17 columns) and dataset_data_dictionary.csv, from the final release of 2026-02-10.
- Zindi needs a login. Two places confirm the sizes:
  - the Zindi API at `api.zindi.world/v1/competitions/<slug>` (`api.zindi.africa` now answers 308 and redirects
    there), field `datafiles`;
  - the zip manifest, dated 2026-02-10T12:40:23.
- Two participant copies are byte-identical:
  - Kaggle dataset `laban102/digicow-farmer-training-adoption-dataset`;
  - GitHub repository of the 9th-place solution, commit b736cc82.
- `download_description` uses the pinned GitHub commit. Train.csv sha256 4977559d... has been verified.
- Raw files kept for review: all of them, including Prior.csv and Test.csv, are in
  `_scratch_new65/digicow_farmer_training_adoption_challenge/raw_all/` (12 MB).
- Licence, from the rules: "You are allowed to access and, use and share challenge data ... for any commercial,
  non-commercial, research or education purposes, by open source"; "Data Sharing: Open source".

**Definition:**
- Prediction point: the end of a farmer's training day.
- Target: `adopted_within_07_days`, 153 adopters (1.13%).
- Regime: temporal on `training_day`, with day and month swapped back.
- Splits: 4 windows of 4 calendar months, train side at least 50% of the rows:

  | Window | Rows | Adopters |
  |---|---|---|
  | Sep-Dec 2025 | 718 | 9 |
  | May-Aug 2025 | 773 | 5 |
  | Jan-Apr 2025 | 727 | 19 |
  | Sep-Dec 2024 | 4,264 | 103 |

- Shape: 13,536 rows x 11 features.
- Dropped columns:
  - `ID` and `farmer_name`;
  - `has_topic_trained_on`;
  - the 90- and 120-day targets.
- Text columns: `trainer` and `topics_list` are written as text.
- Duplicates are kept.
- Prior.csv and Test.csv are not used.
- Checksum v2:844642c7..., the same under pandas 2.3.3 and 3.0.6.
- Decisions (5):
  - the date swap;
  - the flag;
  - the recording waves by month;
  - the label as recorded, by trainer and period;
  - the windows, with the sessions and trainers of their adopters.

**Checks:**
- `dataset check`: 0 errors, 1 info (51 conflicting duplicate groups).
- Three warnings are accepted, with reasons rewritten in the fix round:
  - `dataset_duplicate_rows`: distinct farmers of one session.
  - `dataset_pure_feature_value`: the label-recording issue. Accepted only so the folder checks clean for Lennart's
    decision.
  - `splits_test_minority_few`: the Too Small issue. Accepted for the same reason.
- `pytest -q tests/test_v2_datasets.py -k digicow`: 1 passed, 1 skipped.
- ruff is clean, the import check passes, and no TODO is left.
- I did not run `sync-notebooks` (`v2_path` unset). It should only be set if the dataset is kept.

**Probes:**
- Task probes:
  - linear AUC 0.829, random forest 0.782, LightGBM 0.704, single feature 0.551;
  - flag `unstable` (standard error 0.144);
  - every family's log loss is worse than the dummy's (0.096).
- Leak probes on all 4 windows:
  - all features 0.691, depth-2 / depth-3 trees 0.776 / 0.775;
  - `subcounty` 0.778, `ward` 0.775, `trainer` 0.762, `county` 0.760;
  - 25.3% exact copies;
  - 1-NN agreement at chance level.
  - Reading (reversed in the fix round): these hits are the label recording, not the task's core. A trainer-rate
    lookup scores 0.822, 0.892 and 0.901 on the 2025 windows and 0.433 on 2024.
- Generated-data probe: no flag.

**Issues for Lennart:**

1. **Retire as `No` with `Too Small` + `Data Quality Issue`.** Revisit if DigiCow documents when and for which
   trainers adoption was followed up.
   - Label recording, using Train.csv + Prior.csv in true dates:

     | Training month | 7-day adopters / 120-day adopters |
     |---|---|
     | Aug 2024 | 0 of 339 |
     | Sep 2024 | 0 of 237 |
     | Oct 2024 | 1 of 445 |
     | Nov 2024 | 147 of 326 (45%) |
     | Dec 2024 | 445 of 691 (64%) |
     | Feb 2025 | 112 of 118 (95%) |

   - 2024-12-12 lies inside the adoption interval of 1,028 of the 2,389 adopters. Three dates (2024-11-12,
     2024-12-12 and 2025-02-08) cover 1,972 of them (83%).
   - Mar-Oct 2024 has 21 7-day adopters in 36,664 rows (0.06%); Nov-Dec 2024 has 592 in 6,784 rows (8.7%).
   - TRA_gertumxc: 5-13% of its farmers adopted within 120 days for the Aug-Dec 2024 trainings. Then 0 of its 4,906
     rows from Mar-Jul 2025 adopted at any horizon, although those 120-day windows had closed before the release.
   - TRA_ubcgvofe: no 7-day adopter in 4,447 rows.
   - Too Small:
     - every adopter of the two newest windows is TRA_rkvyofbh's;
     - the 2024 window trains on 17 adopters, all of them TRA_hyodnntj's;
     - 1- to 3-month windows leave some windows without any adopter.
   - No other design fixes it:
     - IID: LightGBM 0.959 against a trainer x month lookup at 0.937;
     - grouped by `group_name`: 0.937 against 0.916;
     - leave one trainer out: one trainer with adopters per fold;
     - Prior.csv rebuild: the same waves (163 + 41 adopters in 2025, from TRA_rkvyofbh and TRA_kkzpfdtu).
2. **Date swap (confirmed by the verifier).** The stored `training_day` has day and month swapped, and the
   definition swaps them back.
   - Trainer-days:

     | | Mon-Thu | Fri | Sat | Sun |
     |---|---|---|---|---|
     | Swapped back | 16-20% each | 12.5% | 8.2% | 5.4% |
     | As stored | 13.3-15.8% on every weekday | | | |

   - Whole-week gaps between a group's sessions: 49.3% swapped back, against 14.7% as stored.
   - Swapped back, January holds almost no training (72 rows, none in Train.csv).
   - Timing-class coherence: 83% swapped back against 58% as stored.
   - Caveat: swapped back, 700 rows fall on Labour Day 2025 and 331 on Easter Monday 2024.
   - Only days 1-12 of each month survive. In true dates, the challenge's Train/Test cut splits 2025 by day of month,
     and 20.3% of the Train farmers' Prior rows come after their Train row.
   - Worth telling Zindi or DigiCow.
3. **Prior.csv is not used.**
   - As shipped, its history leaks later outcomes (the swap).
   - Rebuilt in true dates, history features add AUC -0.02 to +0.16 per window.
   - It carries the same recording waves.
4. **`has_topic_trained_on`: dropping it alone is incomplete. Drop both columns or keep both; Lennart's call, moot if
   retired.**
   - It goes with the adoption for two trainers: in mixed sessions, the 195 flagged farmers hold all 56 adopters.
   - It may simply mark the farmers whose adoption could be recorded at all (flag 0 never adopts, in 5,201 rows).
   - `topics_list` predicts the flag with AUC 0.870 in the two trainers' 4,195 rows (5-fold CV grouped by session),
     and 0.796 inside the 82 mixed sessions.
   - No code change: the definition drops the flag only.
5. **Target: 7 days.** Zindi's own scoring rubric (API field `benchmark_submission_private_scoring_rubric`) weights:
   - 7-day log loss 0.65;
   - 7-day AUC 0.15;
   - 90-day and 120-day log loss and AUC 0.05 each.

   The 90- and 120-day targets show the same waves.
6. **The record's comment is wrong.** It says "logloss (25%) and ROC-AUC (75%)"; the Evaluation page says Log Loss
   75% and ROC-AUC 25%.
   - Domain: I kept the record's "environmental science & climate"; its comment says "agriculture".
7. **Probe gaps.** `task_probes.py` prints no per-window scores, and `leak_probes.py` has no `--out`.

#### Verification (fix round, 2026-10-07)

The verifier said "should not ship": retire as `Too Small` + `Data Quality Issue`. I agree. I re-computed the key
numbers with my own scripts:
- `explore/f1_check_verifier.py`
- `explore/f2_check_windows_lookups.py`
- `explore/f3_grouped_lgb.py`
- `probes/leak_probes_4splits.txt`

| Finding | Status | My check |
|---|---|---|
| 1, label mixes "no adoption" and "not recorded" (blocker) | confirmed | Month shares 0% / 45% / 64% / 95% reproduced. 2024-12-12 is the best single date (1,028 of 2,389); three dates cover 1,972 (83%). TRA_gertumxc: 6.0 / 5.1 / 13.0 / 10.6 / 10.7% in Aug-Dec 2024, then 0 of 4,906 rows. Correction: those rows are Mar-Jul 2025, since TRA_gertumxc has no Feb 2025 rows. Train: 9 of 118 trainer-month cells hold 80% of the adopters (1,188 rows); 60 of the 72 cells with at least 50 rows hold none. Added as the "Label recording (Data Quality Issue)" bullet and Decision 4. Reversed the "natural core" reading of the probe hits. |
| 2, Too Small (major) | confirmed | Adopter sessions 3 / 3 / 8 / 52 and trainers 1 / 1 / 2 / 7 reproduced. Every adopter of windows 0 and 1 is TRA_rkvyofbh's; the 2024 train side holds 17 adopters, all TRA_hyodnntj's. Trainer lookup: 0.822 / 0.892 / 0.901 / 0.433. My IID run: LightGBM 0.959, trainer x month lookup 0.937. My `group_name` run: 0.937 and 0.916, with the lookup ahead on 1 of 3 folds. The verifier reports 0.957 / 0.952 and 0.939 / 0.926, with different folds and lookup details; the conclusion is the same. |
| 3, flag drop incomplete | confirmed | 0.870 (verifier 0.876) and 0.796 inside mixed sessions (verifier 0.805). TRA_hyodnntj: 10.2 topics for flagged farmers, 4.0 for the others. A sentence is added to the bullet; issue 4 above. |
| 4, date swap | confirmed, evidence added | Trainer-days: verifier's figures reproduced, with small differences in how two-trainer rows are counted. Gaps 49.3% vs 14.7%, January 72 rows, Labour Day 2025 700 rows, Easter Monday 2024 331 rows. On stored dates the splitter gives 2 windows (2,218 rows with 33 adopters; 4,155 rows with 64). |
| 5, wording and provenance | fixed | 1 to 20 sessions a day. "One main trainer" (two counties have a second one, with 10 and 6 rows). The rubric weights are Zindi's own, from the API field. `api.zindi.world` is now used in `download_description` and the comments. |

The curation comments now open with the recommendation bullet. The splits comment and the accepted-warning reasons
point to it.

### distribution_transformers_at_cauca_department
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/distribution_transformers_at_cauca_department/`). The independent verifier's verdict is "ready with noted concerns" (Verification section).

**Record judgment:** valid with concerns.
- **Source:** Mendeley Data "Dataset of Distribution Transformers at Cauca Department (Colombia)", version 4 (doi:10.17632/yzyj46xpmy.4, Bravo, Lozano, Alvarez, 2021-09-17). It is described in Data in Brief 38:107454 (doi:10.1016/j.dib.2021.107454; PMC8521452, CC BY).
- **Origin and task:** the data come from the grid operator Compañía Energética de Occidente ("Dataset was obtained through manual inspections", Specifications Table). They were published for a binary classification task ("From a Machine Learning point of view this is a binary classification problem", Sec. 2).
- **Uniqueness:** no duplicate in the working copy, the records or this run (grep for cauca, yzyj46xpmy, transformer, kva and the row count).
- **The record's link:** its "data proof" link (IEEE DataPort, doi:10.21227/qnt2-hy89, Julián López Hernández, June 2025, subscription) is a processed copy of the Mendeley release made for a later study.
- The concerns are the inventory date (issues 1 and 4) and the corrupted column (issue 3).

**Data:**
- **Files:** Mendeley Data version 4, downloaded through the public API by file id. The record's link was down for the curator, but the API and the file URLs work.
  - `Dataset_Year_2019.xlsx` and `Dataset_Year_2020.xlsx`, sha256 as the API lists (e7dd9283…, 22e0d23f…).
  - Location: `local-data-warehouse/distribution_transformers_at_cauca_department/`.
- **Shape:** each file is 15,873 rows x 16 columns (14 attributes, the burning rate, the year's label). Both hold the same transformers in the same row order.
- **Version 3:** (doi:10.17632/yzyj46xpmy.3) has the same numbers with Spanish labels, plus the authors' `Datos2019.mat` and a MATLAB script. I used the .mat only as evidence; a copy is in `_scratch_new65/distribution_transformers_at_cauca_department/v3/` (2.7 MB).
- **Licence:** CC BY 4.0 (Mendeley API `data_licence`; the article is CC BY 4.0 too).

**Definition:**
- **Prediction point:** the start of 2020. The operator ranks its transformers by the risk of burning during the year, for predictive maintenance (Sec. 2). Both files carry one inventory, taken after the 2020 burns.
- **Target:** `burned` (Yes / No), "Burned transformers 2020": 629 of 15,873 (4.0%). Metric roc_auc (default; the source fixes none).
- **Regime:** IID with the tag `ForcedIIDFromTemporal`, default 3 x 3 stratified folds (10,582 train / 5,291 test, at least 209 positives per test fold).
- **Size:** 15,873 rows x 14 features.
- **Cleaning:**
  - snake_case renames in source order;
  - `self_protected` dropped (issue 1);
  - `installation_type`: Spanish leftovers translated and a typo fixed;
  - `lv_network_km` repaired (issue 3);
  - duplicates kept (80 exact rows, 3 feature vectors with both labels); all 15,873 rows kept.
- **The 2019 file** is read only for the three evidence tables in `_decisions`, with a guard that the two files still align row by row.
- **Reproducibility:** the checksum is the same under pandas 2.3.3 and 3.0.6 (`v2:d65d18fc…`), and the download commands, re-run from scratch, reproduce both sha256 hashes.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 2 info (`dataset_duplicate_rows` 80, `dataset_conflicting_duplicate_rows` 3).
- One warning accepted: `dataset_pure_feature_value` for client_type = STRATUM 3 (1 of 427 burned in 2020). The reason: 90% of these transformers are urban, and urban units burn at 1.0% against 4.6% for rural ones.
- `pytest tests/test_v2_datasets.py -k distribution_transformers`: 2 passed, including the rebuild from raw data with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- ruff is clean, the import check passes, and no TODO is left.

**Probes:**
- **task_probes** (5 of 9 splits): LightGBM AUC 0.689, random forest 0.688, linear 0.667. The best family beats the dummy on 5 of 5 splits. Best single feature `power_kva` 0.667, which is 88% of the best skill. No flags.
- **leak_probes:** all features 0.686, depth-3 tree 0.665. 0.7% exact copies across the split; NN distance alone 0.512.
- **generated_probes:** no rule leaves.
- **hidden_groups:** no hit (`n_users` gap -0.002).
- **The verifier** re-ran all four with the same results (task probes on all 9 splits: 0.690 / 0.690 / 0.664).

**Issues for Lennart:**
1. **`self_protected` dropped as a post-outcome leak.**
   - **Question:** does the flag mark units installed after a burn?
   - **What the source says:** the flag is an internal low-voltage protection switch (Sec. 1, item C).
   - **What the data show:**
     - Share of self-protected units: 2.0% of the transformers never burned in 2015-2020, 25% of those burned in 2015-2018, and 46% and 37% of those whose first burn was in 2019 and in 2020.
     - Self-protected units without an earlier burn burned at 42% in 2019 and 42% in 2020 (of those not burned in 2019). Self-protected units with an earlier burn burned at 13% and 9%; units without the flag at 2.5-3.3%.
     - 86% of the self-protected units burned in 2015-2020, against 24% of the others.
     - Within 2020 the flag alone gives a log loss of 0.1540, against 0.1560 for all other features together; LightGBM AUC is 0.752 with it and 0.699 without.
   - **Implemented:** dropped.
   - **Alternative:** keep it as a genuine risk factor. The 42% against 13% contrast speaks against that reading. The authors could be asked for the inventory date.
2. **Year and framing.**
   - **Implemented:** 2020 only, IID within the year. Two years cannot give the three temporal windows v2 requires.
   - **The real use** (train on last year, predict the next year) is a single split, AUC 0.687 for 2019 -> 2020. A random split within 2020 gives 0.699, and a split grouped by lightning area within 2020 gives 0.669-0.678 (two fold assignments).
   - **Alternative, 2019:** 807 positives, AUC 0.767. It is more affected by the post-burn inventory (self-protected share 46% against 37%).
   - **Alternative, both years stacked and grouped by transformer:** AUC 0.745 (0.710 on the 2020 rows). Every unit appears twice, and it is not the use case.
   - **Alternative, a framework exception:** allow a one-window temporal task.
3. **`lv_network_km` repair.**
   - **The defect:** 5,395 of the 5,436 lengths of 1.1 km or more are stored as integers of 4 to 6 digits (1103-717125; Excel `#,##0` in the 2019 file, General in the 2020 file). The other 41 (1.13-3.56 km) kept their decimal point.
   - **Implemented:** divide each integer by 10^(digits-1). The authors' own table (Datos2019.mat, dataTest) confirms this for all 479 matched six-digit values.
   - **A second source bug:** the zeros right after the decimal point were dropped (1.04202 -> 14202, 0.05866 -> 0.5866).
     - It affects 178 of the 1,754 matched rows (103 of the 159 matched 4/5-digit values, 75 of the 1,116 values below 1.1 km).
     - The stored value is always too high, by under 1 km (median 0.53 km).
     - The stored value depends only on the true length, so the bug blurs the column without carrying the label. It cannot be undone row by row.
   - **Alternatives:** keep the values as stored (LightGBM AUC 0.696 against 0.699 repaired), or set the ambiguous 4/5-digit values to missing (0.694). The bug could be reported to the authors.
4. **`power_kva` and `installation_type`: major question, kept on purpose.**
   - **The concern:** both come from the inventory taken after the 2020 burns, so a transformer replaced in 2020 may show the size and mounting of its replacement. My first argument (2020 burns look like the 2015-2018 burns) could not separate risk from replacement, because those rows are replacements too. The verifier's evidence below replaces it.
   - **For a leak:**
     - The gain concentrates on the self-protected positives, the units where replacements show. Added to the site columns, `power_kva` raises LightGBM AUC by 0.107 for the 248 self-protected positives against all negatives, and by 0.023 for the other 381 positives.
     - `installation_type` on top adds 0.024 and 0.008.
     - 10 kVA units are 66.5% of the self-protected positives, 34.4% of the other positives and 21.1% of the negatives. H-structure mountings: 14.5%, 4.2%, 2.0%.
     - No 5 kVA unit is among the 163 self-protected first burns of 2020, against 25 among the 277 other first burns.
   - **Against:** kVA follows the load the same way in every group. 10 kVA units serve a median of 5-8 users whether never burned, burned in 2015-2018 or burned first in 2019 or 2020; 5 kVA units serve 3-4. So there is no sign of resizing on replacement.
   - **Implemented:** both kept, with these numbers in the "Potential leak, kept on purpose" bullet.
   - **Alternative:** drop `power_kva`, `installation_type` and `energy_not_supplied_kwh` (it carries kVA).
     - Without them, AUC is 0.628 within 2020 and 0.646 for 2019 -> 2020 (verifier: 0.626 and 0.650).
     - Keeping the outage hours EENS / (1.08 x kVA) gives 0.636 (verifier: 0.638).
5. **History markers in two columns (one marker).**
   - All 3,734 units burned in 2015-2018 have `removable_connectors` = 1 (34% of never-burned units). 99% have `energy_not_supplied_kwh` = 16.2 x kVA (36% of never-burned units).
   - EENS / (1.08 x kVA) is exactly 15 hours for 7,389 of the 7,719 units with connectors, and for 564 of the 8,154 without. EENS is a planning formula whose restoration time is set by the connectors, so the two are one marker.
   - Neither is raised for the burns of 2019 or 2020 (16-17% and 20-21%).
   - Kept as history, in an Anomaly bullet.
6. **`burn_rate` is history, not a leak.**
   - For every transformer, 5 x rate2020 - 4 x rate2019 equals its number of burns in 2019. 440 of the 629 burned in 2020 have rate 0.
   - A "failures in 2019" lag feature adds nothing (AUC 0.6985), so it is not added.
7. **Lightning period (cannot verify).** The article does not say which years the average and maximum ground discharge densities cover (Sec. 1, items D and E). They are one value per area, the same in both files. If they include 2020, they carry a little same-year information. This is noted in the lightning bullet.
8. **Source notes for the record.**
   - The IEEE DataPort link is a 2025 derivative, so the record should point to Mendeley v4 and the Data in Brief.
   - The paper says 15,869 transformers, the file holds 15,873: the authors' MATLAB table starts at the file's fifth row.
   - The authors' test table is a subset of their training table, so their reported accuracy is not a reference.
9. **Year convention.** `year = "2021"` (publication year); the data cover 2019-2020.

#### Verification (independent verifier, 2026-10-07; fix round done)
- **Verdict:** ready with noted concerns. No blocker.
- **What the verifier confirmed:**
  - The `self_protected` drop is right, and `burn_rate` holds only the years before 2020.
  - Every number in the comments reproduced, and the download reproduces both sha256 hashes.
  - The 2020 choice and the random split are right.
- **What I re-derived with my own code** (`fix_round_checks.py`, output in `fix_round_checks.txt`): the self-protection rates (0.419 / 0.424 against 0.127 / 0.093), the shares (66.5 / 34.4 / 21.1%), the users per kVA, the EENS outage hours (7,389 of 7,719), the km counts (5,395 of 5,436, 41 kept their point, formats per file) and the second km bug (178 of 1,754, always upward, median 0.53 km, max 0.98 km).
  - My AUC gains match the verifier's within 0.005.
  - My alternative scores are 0.628 / 0.646 / 0.636 against the verifier's 0.626 / 0.650 / 0.638.
  - The area-grouped split gives 0.678 with GroupKFold against the verifier's 0.669; both are quoted.
- **Findings and fixes:**
  - **Finding 1 (major):** the `power_kva` / `installation_type` bullet was rewritten with the verifier's evidence. Both columns are kept; the alternative is in issue 4.
  - **Finding 2:** the prediction-point bullet now says that both files carry one inventory, taken after the 2020 burns.
  - **Finding 3:** the self-protection bullet, the decision title and the record comment now give the source's definition (item C) and present the replacement reading as what the data show, with the 42% against 13% contrast.
  - **Finding 4:** the km bullet now says 5,395 of 5,436 (41 kept their point) and names the format per file. The second bug is described as always upward, under 1 km (median 0.53 km) and label-free.
  - **Finding 5:** the Anomaly bullet now says the connector and EENS markers are one marker (15 h for 7,389 of 7,719 connector units).
  - **Finding 6 (cannot verify):** the lightning period is in issue 7 and in the lightning bullet.
  - **Finding 7:** the grouped-by-area number is now in the regime bullet.
- **After the fixes:**
  - `dataset check`: 0 errors, 0 warnings, 2 info, 1 accepted.
  - `pytest -k distribution_transformers`: 2 passed. ruff is clean.
  - Same checksum under pandas 2.3.3 and 3.0.6 (`v2:d65d18fc…`).
- **Record pointer:** the verifier noted that `v2_path` is unset (sync-notebooks); that is for the orchestrator.

### expresso_churn_prediction

**Outcome:** added and checked: `datasets/_dev/tabarena-v0pt2/expresso_churn_prediction_1m/` (`version_of = "expresso_churn_prediction"`; the frame has 2,154,048 rows, above the 1.5M budget). REGION was dropped after verification (issue 1).

**Record judgment:** valid with concerns.
- Source: the data first appeared on Zindi for the UmojaHack Africa hackathons in Senegal and Ghana (27 June 2020). The Zindi API (`api.zindi.africa/v1/competitions/<slug>`, field `datafiles`) lists the same Train.csv (259,026,777 bytes) for those hackathons and for the public "Expresso Churn Prediction Challenge" (27 Aug to 28 Nov 2021, 1,430 participants, metric ROC AUC).
- Task, from the Description page: "predict the likelihood of each Expresso customer 'churning,' i.e. becoming inactive and not making any transactions for 90 days". It is a real customer-level prediction task, not forecasting.
- Uniqueness: no other Expresso folder is in the working copy, and no other record carries its columns or links. The other Zindi re-runs are subsets of this file (issue 2).
- Concerns:
  - The REGION column in the source data is most likely filled after the observation window, so it leaks the label; we drop it (issue 1).
  - Zindi publishes no calendar dates.

**Data:**
- Source used: the Kaggle copy `hamzaghanmi/expresso-churn-prediction-challenge`, pinned to version 1 (2021-08-30), because Zindi needs a login.
  - Its Train.csv has the byte size the Zindi API lists (259,026,777) and sha256 `15d3438d098bea4dc107ba77c81e364705527845f24d7adcbc332e1e33c8777d`: 2,154,048 x 19, one row per customer (unique ids).
  - The pinned download was re-tested with `uvx --from kaggle==2.2.2`.
  - `hossamshokry/expresso-churn-datasets` holds a Train.csv with the same sha256 and is named as a fallback.
  - Test.csv (380,127 rows, no labels) is not read by the definition.
- Licence: Zindi Competition Rules. The Rules page says: "The data used in this competition is the sole property of Zindi and the competition host. You may not transmit, duplicate, publish, redistribute ... (this includes uploading the data to any public site such as Kaggle or GitHub)". The Kaggle copies state "unknown". Noted only.

**Definition:**
- Prediction point: at the end of an observation window of about 91 days, each customer who was active in it is scored for churn, meaning no transaction in the 90 days after the window.
  - Inputs: the window's usage aggregates and the tenure band.
  - The label window follows the observation window: REGULARITY counts active days in the window's last 62 days, and 612 churners were active on all 62 (issue 3).
- Target: `CHURN`, mapped to Yes/No (18.75% Yes).
- Regime and splits: IID, as in the competition. The `_1m` version sub-samples the frame to 1.5M rows (stratified) and uses 1 x 3 folds, each with 1M train and 500k test rows.
- Shape: 1,500,000 x 15 features. TENURE and TOP_PACK are categorical; the other 13 columns are numeric. No context tags (`Spatial` went with REGION).
- Drops:
  - `user_id`: the SHA-1 hash of the customer's row number in Expresso's extract. All 2,534,175 train and test ids decode to the numbers 0 to 2,534,174.
  - `MRG`: "NO" in every row.
  - `REGION`: issue 1.
- Kept as released:
  - the duplicates;
  - missing values (no activity of that kind in the window);
  - `ARPU_SEGMENT`, which equals round(REVENUE / 3) in every row.
- `_decisions` tables:
  - the REGION drop: the missing share by outcome and active days, against MONTANT;
  - the duplicate counts.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 1 accepted, 1 info.
  - Accepted: `dataset_duplicate_rows`. Each row is a different customer, all active in the window. 75.3% of the 678,270 copies in the full file have no activity value. The copies hold 317,548 of the 403,986 churners, so deduplicating would leave a 5.9% churn task about active customers.
  - Info: `dataset_conflicting_duplicate_rows` (6,986 feature vectors with both labels, 0.5%).
- Checksum: `v2:055456177016393045fd8ef6808c5349488dc46b4617f42d4793091b81a2afd6`. pandas 3.0.6 (the shared `venvs/pd3`) gives the same checksum for the final file.
- `pytest -q tests/test_v2_datasets.py -k expresso_churn_prediction_1m`: 1 passed, 1 skipped.
- `dataset list` imports it; ruff is clean; no `TODO` is left.
- The record's `v2_path` is not set: `sync-notebooks` is not run, per the brief.

**Probes** (without REGION, outputs in `<scratch>/probes/`; the runs with REGION are in `probes_v1_with_region/`; my analyses `a1`-`a11` and `b1`-`b4` sit next to them):
- **Leak** (50k rows a side, 3 splits):
  - All features 0.899; depth-2 / depth-3 tree 0.865 / 0.885; REGULARITY alone 0.890; no missing-value indicator above 0.793; without REGULARITY 0.857.
  - 29.0% of test rows have an exact feature copy in train. The label-free nearest-neighbour distance gives 0.833.
  - How these were answered: the copies and the distance score come from the sparse profiles of low-activity customers. The number of missing values alone gives 0.843. Kept (accepted warning).
- **Task:** LightGBM 0.900, random forest 0.898, linear 0.892, REGULARITY alone 0.890 (chosen on 3 of 3 splits). Flag: `one_feature`.
  - How it was answered, by `task_probes.md` rule 4:
    - Active days are the natural core of a churn task.
    - On the full shipped folds (1M train, 500k test), an untuned LightGBM beats the raw REGULARITY (its direction chosen on the training side) on 3 of 3 folds: 0.9026, 0.9031, 0.9023 against 0.8901, 0.8902, 0.8896 (`b4_rule4_folds.txt`).
  - Kept. The orchestrator proposes the `task_probes.md` case row.
- **Generated:** rule leaves cover 0.0% of the minority rows. No flags.
- **Hidden groups:** 12 candidates, no hits. Top: TOP_PACK, gap 0.018.
- **Train-test drift** (Lennart's question in the record): none.
  - The decoded ids show that Zindi's test set is a uniform random 15% of the extract: 14.8% to 15.2% of every block of 100,000 row numbers.
  - Region, tenure and missing-value shares agree to 0.2 points.
  - A LightGBM model that separates Train.csv from Test.csv scores ROC AUC 0.500 (3 folds: 0.4996, 0.5009, 0.5017).

**Issues for Lennart:**

1. **REGION is dropped as most likely filled after the window. Keep it instead?**
   - Evidence:
     - 39.4% of customers have no region. Of these, 44.8% churned, against 1.8% of customers with a region.
     - Among churners, the region is missing for 92-95% in every band of active days from 1 to 62. The share is also 85-95% in every revenue decile and 86-96% in every tenure band.
     - Among stayers, the share falls from 67% (1 active day) to 7% (62 active days).
     - The window's own columns fall with activity in both groups. MONTANT missing: churners 93% to 13%, stayers 88% to 1%.
     - A model of the missing region from the window's columns, fit on stayers, predicts 11% missing for the 612 churners active on all 62 days. 94% of them have no region.
     - The region values add almost nothing among customers who have one: ROC AUC 0.913 with them against 0.912 without.
     - Cost of the drop: LightGBM ROC AUC 0.930 → 0.901 on 400k rows; in the leak probe, 0.928 → 0.899.
   - Implemented: dropped. The precedent is mic's outcome-driven missingness. REGION is not an anonymised host field like kick's or homesite's.
   - Alternative: keep it as "Potential leak, kept on purpose", described as probably post-outcome. What would settle it is how Expresso fills REGION.

2. **Duplicate records: proposed record fixes.**
   - `indabax_eswatini_2022` (AI-filled, `TBD -> Yes`) is this data. The evidence is the Zindi API, not a row check:
     - its `parent` is `expresso-churn-prediction`;
     - its Train.csv is 129,548,498 bytes, the size of the Azubian file. Its other two links (`tanzania-ai-conference-2022`, `indabax-tanzania-2022`) list the same size.
   - Row check: the Azubian Train.csv (1,077,024 rows) and the DSN Train.csv (400,000 rows) are rows of this Train.csv, identical in all 18 columns, ids included.
   - Proposals:
     - Mark `indabax_eswatini_2022` as `No` + `Duplicate`.
     - Settle the Azubian record's "which cut we keep" with this full file.

3. **Prediction point: resolved by verification, dates unknown.**
   - FREQUENCE (days with revenue) reaches 91, and FREQUENCE − REGULARITY is at most 26-32 at every level. So REGULARITY counts active days in the last 62 days of a window of about 91 days.
   - Customers with more revenue days than counted active days churn more: 24.7% against 15.3% at 6-10 active days, and 9.8% against 3.4% at 21-40. The extra days therefore come first.
   - 612 churners were active on all 62 days, so the 90 inactive days follow the window.
   - Calendar dates stay unknown; nothing is left to implement.

4. **FYI: the extract order.**
   - The 3rd-place solution decoded user_id ("an SHA-1 hash of an integer", Zindi discussion 9379) and used it as a feature.
   - Churn varies along the decoded order: 13-23% per block of 100k rows.
   - The file is one snapshot, and Zindi's test set is random within it.
   - Implemented: IID, with user_id dropped (the neighbours' churn in that order gives ROC AUC 0.55).

5. **Minor.**
   - `ARPU_SEGMENT` equals round(REVENUE / 3) in all rows. Kept as released; the alternative is to drop it as a copy.
   - `year = "2020"` is the first release (UmojaHack), while the BibTeX cites the 2021 competition. This is the same year-semantics question as pkdd.

**Verification** (independent verifier, 2026-10-07; verdict "needs changes"):
- **Verification 1 (REGION post-window, major): applied.** I re-checked it with my own cuts (`b1_region_refute.txt`):
  - churners' missing share is 0.86-0.93 in every octile of ON_NET, DATA_VOLUME and FREQUENCE, while stayers' share falls;
  - a window-only model fit on stayers predicts 0.71 → 0.11 missing for churners across the bands of active days, against 0.95 → 0.94 observed.
  - Changes: REGION dropped, `data_tags` emptied, the comment bullet and the Decision rewritten as a drop; keeping it is issue 1.
- **Verification 2 (`one_feature` without REGION, major): applied.**
  - The flag reproduces (REGULARITY 0.890 against LightGBM 0.900).
  - It is answered by rule 4 with fold-by-fold numbers on the full shipped folds (LightGBM +0.0125 to +0.0128 on 3 of 3 folds) in a `curation_comments` bullet.
  - The duplicate numbers were recomputed and match: 678,270 copies (31.5%), 317,548 churners among them, and 10,049 conflicting vectors holding 676,689 rows.
- **Verification 3 (the prediction point is supported, minor): applied.**
  - My recount (`b3_check_verifier_numbers.txt`) gives the same: FREQUENCE max 91, FREQUENCE − REGULARITY ≤ 26-32 per band, and 612 churners at 62 active days.
  - The REGULARITY bullet is now an explanation, the prediction-point bullet says the label window follows the observation window, and issue 3 is closed for the overlap.
- **Verification 4 (sparse duplicates are customers active in the window, minor): upheld.**
  - My recount: 16.8% of the 511,179 no-activity customers were active on 10 or more days, and churn falls from 74.4% at 1 active day to 6.7% at 41-62.
  - The accepted warning keeps its reason, with the new numbers.
- **Verification 5 (`indabax_eswatini_2022` matched by file size, minor): applied.** The opening line and issue 2 now say file size and parent link; only the Azubian and DSN cuts were checked row by row.
- **Verification 6 (pin the Kaggle version, minor): applied.**
  - `download_description` uses `uvx --from kaggle==2.2.2 kaggle datasets download hamzaghanmi/expresso-churn-prediction-challenge/1` and names the hossamshokry upload as a fallback.
  - I tested the pinned download: it gives `expresso-churn-prediction-challenge.zip`, and its Train.csv has sha256 `15d3438d...`.

### farm_to_feed_shopping_basket_recommendation_challenge

**Outcome:** not added (out of scope: a recommender task, criterion 3; the data itself can be obtained from a faithful
Kaggle mirror, so data access does not block it).

**Record judgment:** do not add. The task is next-basket recommendation over a customer x SKU matrix (criterion 3,
"Exclude ... ranking / information-retrieval (recommender) tasks"; the guidelines' quick pattern "Recommendation /
ranking / CTR / "recommendation"/"recommender" task -> `Out-of-scope Task (CTR/RecSys/Ranking)` -> No"). The record
(`Yes`, Andrej) describes the targets and the temporal split but does not discuss the recommender framing, so this
evidence is not yet weighed there.
- The competition's own words (Zindi competition JSON, `https://api.zindi.africa/v1/competitions/farm-to-feed-shopping-basket-recommendation-challenge`,
  which serves the pages of `https://zindi.africa/competitions/farm-to-feed-shopping-basket-recommendation-challenge`):
  - Description page: "To help Farm to Feed sell more odd produce, your challenge is to help build a recommender
    system for their app. Using historical transaction data, can you build a machine learning solution that:
    Generates a likelihood of purchase in 7 and 14 days for each product; Recommends the quantity of each product
    that a customer will purchase".
  - Subtitle: "Can you predict future shopping baskets to recommend better fresh produce purchases?"
  - Data Description page: "Each row represents a customer-product (SKU) pair in a specific week, along with metadata
    describing the customer and the product category. A strong solution will involve building meaningful features
    that capture purchasing behaviour and temporal patterns."
- The data (Kaggle mirror, below):
  - Train.csv is the complete customer x SKU grid: 141 customers x 326 SKUs (`product_unit_variant_id`) = 45,966
    pairs, every pair present in each of the 46 weeks (2,114,436 rows = 46 x 45,966).
  - Test.csv is the same 45,966 pairs for 6 later weeks (275,796 rows).
  - `Target_purchase_next_1w` equals the same pair's `purchased_this_week` one week later in 100% of the rows that
    have a next week in the file (97.8%), and `Target_qty_next_1w` equals the next week's `qty_this_week` in 100%:
    each target is the next value of a pair's weekly purchase series.
  - Test rows carry only the ids, `week_start` and static customer and SKU attributes (`product_id`, `grade_name`,
    `unit_name`, `product_grade_variant_id`, `customer_category`, `customer_status`, `customer_created_at`): no price
    and no activity. All the per-pair signal has to come from the purchase history in Train.csv.
- Where the signal sits (my temporal holdout: fit on the weeks before 2025-08-04, score `Target_purchase_next_1w`
  on the six weeks 2025-08-04 to 2025-09-08; LightGBM, 300 trees; `a2_signal.py`, `a3_existing_customers.py`):
  - Rows of existing customers (1,251,188 rows; test 234,068 rows, 8,137 positives, 3.5%):
    - SKU popularity (the SKU's purchase rate in the training weeks), no model: ROC AUC 0.848.
    - LightGBM on the static attributes (grade, unit, price, customer category, status, tenure): 0.850.
    - The pair's purchase recency (weeks since its last purchase), no model: 0.943.
    - LightGBM on the row as served (static attributes plus this week's quantity, orders, spend, purchase flag):
      0.928.
    - The row as served plus the pair's purchase rate and recency: 0.967.
  - So the static-attribute model is item popularity, and one history number per customer x SKU pair, without a
    model, beats the tabular model on the row. These are the two standard recommender baselines.
  - All rows: static 0.869, row as served 0.935, with customer and SKU ids as categories 0.969, with history 0.975,
    history only 0.963. 89% of the test rows are pairs that never bought before; they hold 10.4% of the positives.
- The solutions treat it the same way:
  - 2nd place (GitHub `koleshjr/Farm_to_Feed_Shopping_Basket_Recommendation_Challenge`, README): "This project builds
    a **machine learning recommender system** to predict future customer shopping baskets"; "Customer–Product
    Interaction Features ... These are among the **most predictive features** since grocery purchases are often
    repetitive"; 7-day CV ROC AUC 0.975.
  - The public notebook from the forum (Kaggle `yohannesmelese/ftf-horizon-solution`, linked in Zindi discussion
    29974): "FarmToFeed - Multi-Horizon Demand Forecasting", built on lags 1-8 and 4- and 8-week rolling means of each
    pair's weekly quantity, orders, spend and purchase flag.
- Second reading: the quantity targets are each pair's demand next week and over the next two weeks, which is the
  guidelines' "Time-series forecasting (predict future values of a series: demand/sales/price over a horizon)".
- Precedents: the other Zindi recommendation and next-purchase challenges are `No` + `Out-of-scope Task
  (CTR/RecSys/Ranking)` (`zimnat_insurance_recommendation_challenge`, `akeed_restaurant_recommendation_challenge`,
  `xente_purchase_prediction_challenge`, all only `AI (UNVERIFIED)`). The working copy's
  `acquire_valued_shoppers_challenge` is different: one row per customer and offer, the response to a marketing
  offer, not the fill-in of a customer x item matrix.
- Uniqueness: no other record, working-copy folder or record of this run holds this data (grep for the name, slug
  and mirror over `curation/records/` and `datasets/`).

**Data:**
- Source used for the judgment: Kaggle dataset `juliusmwangi/farm-to-feed-shopping-basket-recommendation`, uploaded
  2025-12-03, the competition's second day. Its five files have the byte sizes the Zindi API lists for the competition
  files: Train.csv 275,380,950; Test.csv 27,162,683; SampleSubmission.csv 6,811,235; customer_data.csv 23,679;
  sku_data.csv 34,568. Zindi's `variable_description.pdf` (added 2025-12-08) is not in the mirror.
- sha256 of the mirror files:
  - Train.csv `50db8ea3b42e8cfc78948f5c69a04e7a0cf13b576c5b5ae1271c4f459efbd2db`
  - Test.csv `97ebf10bbf55d2215e7e2419053f4b2cb5628c38e08e9ad51a41f8d8e2a09981`
  - SampleSubmission.csv `4344e7c5014afabb597ad073c6b733c2a25114f291528aefbcde61f2874ffbfc`
  - customer_data.csv `0593ddc9244e82a0fed23a7edb5113ec1f0940b8c404d1468b947381b40a78cb`
  - sku_data.csv `5d139e6e7b7879e1bae4a937a9d55088fda0e112607bfa8bd48bb40fbd735d61`
- Shapes:
  - Train.csv: 2,114,436 rows x 20 columns (4 targets), weeks 2024-10-28 to 2025-09-08.
  - Test.csv: 275,796 rows x 11 columns, weeks 2025-09-22 to 2025-10-27. The two-week gap after training is
    intentional (organiser, discussion 29720).
  - The test labels were never released (SampleSubmission.csv is all zeros), so only Train.csv's 46 weeks would be
    usable.
- The mirror's customer_data.csv is the first upload, whose categories are shifted against Train.csv (discussion
  29688); Zindi replaced it on 2025-12-12 and says Train/Test hold the correct categories (discussion 29756). Not
  needed.
- Licence:
  - Zindi rules: "Data Sharing: Open source." and "You are allowed to access and, use and share challenge data for the
    competition. for any commercial, non-commercial, research or education purposes, by open source." (rules
    section of the competition JSON).
  - The Kaggle mirror is labelled MIT by its uploader.
- Local copies:
  - Nothing in `local-data-warehouse/` (not added).
  - The unzipped mirror is in `_scratch_new65/farm_to_feed_shopping_basket_recommendation_challenge/raw/` (296 MB),
    kept for the verifier; delete it afterwards.

**Definition:** none (not added). Issue 2 sketches the definition if Lennart keeps the record's `Yes`.

**Checks:** not run (no definition).

**Probes:** the probe scripts need a definition and were not run. My own analysis is under "Record judgment" above.
The scripts and outputs are in the scratch folder (`a1_structure`, `a2_signal`, `a3_existing_customers`).
Another finding from the data: 863,248 of the 2,114,436 training rows (40.8%) are dated more than 6 days before the
customer's account was created (`customer_created_at`; target rate 0.08% against 2.06% overall). The grid is padded
with customers who did not exist yet.

**Issues for Lennart:**
1. Scope: recommend `No` + `Out-of-scope Task (CTR/RecSys/Ranking)`. `Time-series (Forecasting)` could be added
   as a second marker for the quantity targets. Question: is this the recommender exclusion of criterion 3? The
   record says `Yes` (Andrej), with the temporal split and the two targets described, and the recommender framing not
   discussed.
   - Evidence: Zindi's Description, "your challenge is to help build a recommender system for their app".
   - The data is the full 141 x 326 customer x SKU grid in every week, and the target is the next week's cell.
   - Test rows carry only ids and static attributes.
   - SKU popularity alone (ROC AUC 0.848) matches LightGBM on the static attributes (0.850), and the pair's purchase
     recency alone (0.943) beats LightGBM on the row as served (0.928). Rows of existing customers, last 6 training
     weeks.
   - Implemented now: nothing added.
   - Alternative: issue 2.
2. If the `Yes` stands, the definition would need these choices (none implemented):
   - Target: `Target_purchase_next_1w` only (binary, ROC AUC, as the competition scored it). The 2-week purchase and
     both quantities are the same series one or two weeks on, and the quantities are 97.9% zeros.
   - Rows: Train.csv only. Drop the 863,248 padding rows dated before the customer existed, which leaves 1,251,188
     rows.
   - Split: temporal, 2-week windows with a 1-week gap (a week's label is known one week later). Three windows hold
     74,654-81,174 test rows (2,497-2,920 positives). Two of the three train sides (1,129,916 and 1,053,958 rows; the
     third 980,608) exceed the 1M budget, so it would ship as `..._1m` with `subsample_to_budget`.
   - The same 45,966 pairs recur every week: a grouped-temporal structure, which v2 cannot declare.
   - Features: the row as served (LightGBM ROC AUC 0.928 on the holdout). The house rule forbids engineered history,
     which leaves the models below a no-model recency baseline (0.943). With the pair's history added, as the
     `acquire_valued_shoppers_challenge` (TabReD) and `g_research_crypto_forecasting` precedents do, 0.967.
3. Record housekeeping:
   - Add the Kaggle mirror to `source_links` as the download route. Zindi needs a login; the mirror's file sizes match
     the competition's file list byte for byte.
   - Note the licence line (Zindi: "Data Sharing: Open source").
   - The three other Zindi recommender records (`zimnat_insurance_recommendation_challenge`,
     `akeed_restaurant_recommendation_challenge`, `xente_purchase_prediction_challenge`) are still
     `AI (UNVERIFIED)` `No`s; this record has the first data-based evidence for the pattern.

### force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition

**Outcome:** added and checked

**Record judgment:** valid with concerns. The source is the FORCE 2020 lithology competition (organisers Bormann,
Aursand, Dilib, Manral, Dischington; GitHub bolgebrygg/Force-2020-Machine-Learning-competition, Zenodo
10.5281/zenodo.4351156), a predictive task by design: "correctly predict lithology labels for provided well logs,
provided NPD lithostratigraphy and well X, Y position" (GitHub readme). It is unique: no folder of the working copy,
no other record and no other record of this run holds FORCE, lithofacies or well-log data (grep for force 2020,
lithofac, lithology, well log, 4351156, bolgebrygg). The record asks whether well logs are a non-tabular modality.
They are not excluded by criterion 4A: each row holds wireline readings of the rock at one depth (sensor
measurements, not a vectorised image), and tree ensembles won. The technical retrospective in the repository
(p. 3-4) names XGBoost for the winner and second place and random forests for third ("Combining boosted trees with
common sense feature augmentation and preprocessing seems to have won the day"), and the code or write-up of each
of the 13 finalists (`lithology_competition/code/`, blog post p. 13-16) uses XGBoost, LightGBM, CatBoost or random
forests. The concerns are listed as
issues 1, 2 and 5 below: the depth context, the interpreted stratigraphy as features, and the label noise (the
organisers put the reachable accuracy near 80%, blog post p. 9).

**Data:** GitHub repository, pinned to commit c8d01ee (the data files are unchanged since they were added on
2020-11-13); md5 checked against a second download. `train.zip` (1,170,511 x 29, 98 wells),
`leaderboard_test_features.csv` + `leaderboard_test_target.csv` (136,786 rows, 10 open-test wells, labels released
after the competition), `hidden_test.csv` (122,397 x 29, the 10 blind wells of the final scoring, labels included);
118 wells, 154 MB in `local-data-warehouse/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/`.
The Zenodo LAS archive (170 MB, checked in scratch, not used) holds the same labels and GR values for all 1,429,694
rows (0 differ); its 1,689 further labelled depths have no GR, which the competition files require. Licence:
CC BY 4.0 on the Zenodo record ("license: cc-by-4.0"), whose description adds "The original well log data comes
form the Norwegian government and is provided by a NOLD 2.0 license"; the GitHub issue (TabArena/tabarena_dataset_curation#2)
says the same. The repository has no licence file.

**Definition:** `datasets/_dev/tabarena-v0pt2/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/`.
Prediction point: a well has been drilled and logged, and its lithology is interpreted from the logs, the NPD
lithostratigraphy (GROUP, FORMATION) and the well position. Target `lithology` (11 classes, the starter notebook's
names; metric log_loss). Grouped by `WELL` (118 wellbores), `labels="per_sample"`, `prediction_unit="row"`,
`context="all_rows"` (the whole log of a new well is known), no `time_on` (depth is not time). Default splits:
1 repeat x 3 folds (1.43M rows >= 1.25M), train 931,093-973,462 rows, test 456,129-498,498 rows, 37-41 test wells
per fold; no `_1m` version (1,429,591 rows < 1.5M). 1,429,591 rows x 26 features plus the group column. Cleaning:
the three files stacked (the open-test labels joined by position after asserting the same WELL and DEPTH_MD);
FORCE_2020_LITHOFACIES_CONFIDENCE dropped (the interpreter's confidence, recorded with the label, missing for the
open-test wells); Basement dropped (103 rows, one well); the LAS null values -999.0, -999.25, -999.9 (stored as
float32) set to missing in RXO (34,481 rows), SP (402) and ROPA (24). Interpolated null ramps (131 negative RXO rows,
20 negative ROPA values down to -966) and spikes stay, as a stated anomaly of "slightly cleaned up and partially
despiked" logs. MUDWEIGHT stays on its three unlabelled scales (an anomaly bullet).

**Checks:** `dataset check`: 0 errors, 0 warnings; one accepted: `splits_test_class_missing` (Halite occurs in 4
wells and Anhydrite in 10, fold r0f2 tests neither, every train side holds both; log loss is defined on the classes
a fold holds). Checksum after the verification edits `v2:f0aa6ed77377c284624211049a86e319660fa29599b7d37d337a467884ecd54b`
(only `curation_comments` changed); pandas 3.0.6 (the session's `venvs/pd3`) builds the same checksum. ruff clean; `pytest tests/test_v2_datasets.py -k <folder>` passes,
also with `DATA_FOUNDRY_V2_DATA_CHECKS=1`. README group statistics: nearest neighbour in the same well for 95.5% of
the rows (chance 1.1%).

**Probes:** (scratch `probes/`; thread caps as asked)
- Leak (`--splits 2`, see issue 6): untuned LightGBM, all features macro AUC 0.640 (LightGBM diverges, issue 3);
  depth-2 / depth-3 tree 0.745 / 0.771; single features FORMATION 0.864, GROUP 0.833, GR 0.732, RMED 0.720;
  missing indicators at most 0.591 (ROP); drop-one: without FORMATION 0.631, GROUP 0.712, GR 0.589; exact copies
  across the split 0.0%; 1-NN agreement 0.761 (closest tenth) / 0.630 (all) against chance 0.416. No leak found: the
  strong single features are the stratigraphy (issue 2) and GR, the core log of lithology.
- Task (3 grouped folds, 50k rows per side): dummy log loss 1.284; linear 0.989 (skill 0.23, macro AUC 0.858);
  random forest 0.744 (skill 0.42 +- 0.011, beats the dummy on 3 of 3 folds, macro AUC 0.916); LightGBM 2.766
  (skill -1.19 +- 2.12). Flag `no_spread` (forest minus LightGBM 1.61, paired SE 1.49). Answered in
  `curation_comments`: it comes from LightGBM's divergence (issue 3); the forest and the linear model differ by
  0.19 skill with fold standard deviations of 0.01 and 0.05, so the families spread. Smallest class in a test
  fold: 0 rows (fold r0f2, accepted warning).
- Generated: rule leaves cover 0.0% of the minority rows; no flag.
- Group (`group_probes.py`, 22 of 118 wells by its 200k-row cap): IID LightGBM 0.841; grouped score NaN (a
  subsampled test fold lacks classes, issue 6); per-row macro AUC across wells: logistic 0.580, random forest 0.804,
  LightGBM 0.582, kNN 0.668. My own run on all 118 wells (random forest, 100 trees, 100k train / 50k test rows per
  fold, `window_experiment.py`): grouped folds log loss 0.776, macro AUC 0.911, accuracy 0.752; row-random folds
  0.314, 0.986, 0.909. The grouped split removes a large leak through neighbouring depths (0.152 m apart).

**Issues for Lennart:**
1. **Depth context.** May a model use the other depths of the same well, and should the dataset ship depth-window
   features? Evidence: the whole log of a new well exists before it is interpreted; the starter notebook keeps WELL
   "so the data can be separated per well. This will be necessary for any 'windowed' approaches"; the winners used
   "windowing and gradients" (retrospective p. 3), H3G and DavidP rolling windows. Measured (random forest, 3 grouped
   folds): gradients plus 21-sample means and spreads of 9 logs per well move log loss 0.776 -> 0.764 and macro AUC
   0.911 -> 0.923 (better on 2 of 3 folds). Implemented: raw per-depth rows, `context="all_rows"`, no window features
   (feature engineering is the pipeline's job). Alternatives: `context="none"` (each depth from its own row, as
   electric_motor and sepsis), which is what a row-wise harness does anyway; or add the window features in `_clean`,
   as electric_motor adds the source study's EWMA features (small gain here).
2. **GROUP and FORMATION (NPD lithostratigraphy) as features.** They are an interpretation of the same well that
   names rock units (Zechstein = evaporites). They are the strongest single features (FORMATION macro AUC 0.864,
   GROUP 0.833); without both the forest's log loss rises 0.776 -> 0.836 (macro AUC 0.911 -> 0.894). They are not
   the label interpretation: every top in the Zenodo NPD_Lithostratigraphy_*.xlsx files has Interpreter NPD and a
   whole-metre MD, and the deepest top above each sample reproduces GROUP on 100% and FORMATION on 99.95% of the
   rows; only 10% of the 574 group boundaries fall on a lithology change at the same sample (2.8% of consecutive
   samples), and NPD's BASEMENT in 35/9-2 (139 rows) is labelled Shale. Their strength is that units hold rare
   classes (14,709 of 14,711 Halite rows in the Zechstein group, 14,014 of 14,043 Chalk rows in the Shetland group).
   Implemented: kept, because the source's task lists them as inputs ("provided NPD lithostratigraphy").
   Alternative: a logs-only task without them, if formation tops are judged to come too late in a real workflow.
3. **Untuned LightGBM diverges on this data.** With its default `min_child_weight` of 0.001 (grouped fold 0, 100k
   rows): training accuracy 0.73-0.78, test log loss 14-15, 66-79% of predictions above p = 0.999; with
   `min_child_weight=1` log loss 0.81 and macro AUC 0.91; learning rate 0.05 with `min_child_samples=200`: 0.76.
   Not a data fault and nothing changed in the definition, but worth checking TabArena's LightGBM default on this
   dataset before reading its rank. The verifier reports that learning rate 0.05 with early stopping on held-out
   training wells stops at 43-45 iterations with log loss 0.79-0.81 (its `v8_lgbm_es.log` is empty, so I could not
   confirm the numbers).
4. **Metric.** The competition scored a 12 x 12 penalty matrix on hard labels (starter notebook,
   `penalty_matrix.npy`); none of the top three trained on it (retrospective p. 3-4). Implemented: default log loss.
   Alternative: register a custom expected-penalty metric (11 x 11 after dropping Basement). The forest's penalty
   score is -0.66 on the grouped folds (winner on the 10 blind wells: -0.469).
5. **Rare evaporites and label noise.** Halite is in 4 wells (14,711 rows), Anhydrite in 10 (1,807); fold r0f2 tests
   neither, and fold r0f1 trains Halite from one well (3,899 rows) while testing three (10,812 rows). Basement
   (103 rows, one well) is dropped. Implemented: accepted warning with these counts. Merging Halite and Anhydrite
   into one evaporite class would not fill r0f2. The labels are a hand interpretation with known errors (blog post
   p. 8: a "limestone" in 16/2-7 is a conglomerate in the core); the organisers put the reachable accuracy near 80%.
6. **Framework (for the probes, not the verdict).** `leak_probes.py` and `group_probes.py` average one-vs-rest ROC
   AUC over the model's classes, which gives NaN when a test fold lacks a class the train side has: I ran
   `leak_probes.py --splits 2` (folds r0f0, r0f1 hold every class), and the group probe's grouped score stayed NaN.
   Averaging over the classes present in the test fold would fix both. The probes' `discover_datasets(root)` also
   fails on any other folder that does not import (another agent's half-written definition); I ran them on a
   scratch root holding a symlink to this folder.
7. **Record follow-ups (not done, per the brief):** the record needs `v2_path` (`sync-notebooks`), and its own
   comment asks to "update GitHub issue!" once checked (TabArena/tabarena_dataset_curation#2 is open, milestone
   tabarena-v0.2). Domain kept as the record's "chemistry & material science"; "environmental science & climate"
   would be the alternative for subsurface geology.

**Verification:** (independent verifier, 2026-10-07: ready with noted concerns; each finding re-checked with
`recheck.py` / `recheck2.py` in scratch on the shipped frame and the raw files)
1. GROUP/FORMATION not a leak, add the evidence: applied. Confirmed: all 855 group and 1,914 formation tops have
   Interpreter NPD and whole-metre MDs; reproduction 100% (GROUP, 1,428,416 rows) and 99.95% (FORMATION, 1,277,477
   rows; the verifier has 99.97%); 574 group boundaries, 10.1% with a lithology change at the same sample against
   2.8% of all consecutive pairs (the verifier: 578, 10.0% against 2.9%). Corrected one detail: NPD's BASEMENT holds
   139 Shale rows in 35/9-2 (not 143) plus 4 Shale rows in 16/4-1.
2. Numbers: applied. Confirmed 131 negative RXO rows, ROPA minimum -965.88 (two values below -900), shipped DCAL
   maximum 10,006.79 (the raw 10,011.42 is in 16/4-1's dropped Basement interval). 34/5-1: MD ranges overlap
   (A 2,120-4,393 m, S 3,544-3,899 m), no shared depth sample; nearest 3-D distance from an S sample to A 1,111-1,416 m,
   horizontal distance at the same MD 1,511-1,867 m, hence "1.1-1.9 km apart there".
3. Confidence: applied. Confirmed 15,776 of the 16,186 Tuff rows with a value have confidence 3 (97%); Tuff is 1.2%
   of the rows.
4. MUDWEIGHT: applied as an anomaly bullet, no conversion. Confirmed per-well medians 0.13-0.17 (19 wells),
   1.08-1.80 (9) and 155.8 (1); all 29 LAS headers with the curve give the unit `_`.
5. Metric: no change (Lennart's call); log loss kept, the penalty matrix documented (issue 4).
6. Fold r0f2 without Halite/Anhydrite: no change (Lennart's call); the default split and the accepted warning stay.
7. `v2_path`: left to the orchestrator (`sync-notebooks`).
After the edits: `dataset check` 0 errors, 0 warnings (1 accepted); ruff check and format clean; pandas 3.0.6 gives the
same checksum; `pytest tests/test_v2_datasets.py -k <folder>` 2 passed with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.

### framingham_heart_study_fhs
**Outcome:** added and checked

**Record judgment:** valid with concerns. The origin the record calls "a bit hard to parse" is now traced. All three
Kaggle uploads are copies of `framingham.csv` from MIT's The Analytics Edge (15.071; MIT OpenCourseWare, Spring 2017,
which says "this data comes from the BioLINCC website"):
- aasheesh200 is byte-identical to MIT's file (sha256 2c0e57dc...).
- dileep070 drops MIT's last 2 rows.
- christofel04 recodes the same 4,238 rows (sex M/F, is_smoking YES/NO) and withholds 848 of the labels.

MIT's 4,240 rows are exactly the baseline (period 1) rows of the NHLBI BioLINCC Framingham Heart Study teaching dataset
for participants with PREVCHD = 0: all 15 features match row for row. The selection criteria hold:
- a real cohort and a predictive task (10-year CHD risk);
- no Framingham data in the working copy (heart_disease_cleveland, heart_disease_hungary, heart_disease_va_long_beach,
  south_africa_coronary_heart_disease and heart_failure_followup_survival are other cohorts);
- no other record and no other dataset of this run is Framingham.

The concerns are the defective label of the Kaggle/MIT file (issue 1) and the teaching data's anonymization and terms
(issue 3).

**Data:**
- Source used: the teaching dataset as redistributed "with permission from the National Heart, Lung, and Blood
  Institute" in the CRAN package riskCommunicator.
  - `data/framingham.rda` is identical in versions 0.1.0, 1.0.0 and 1.0.1 (sha256 8fdd578a...).
  - Downloaded from the permanent Archive URL of 1.0.0 and exported with `uvx --from pyreadr==0.5.7 --with
    pandas==3.0.6` to `framingham_teaching.csv`: 11,627 x 39, sha256 0ab97721..., byte-reproducible (the verifier
    re-ran the commands in an empty folder and got the same bytes).
  - It matches every count and mean I compared with the BioLINCC documentation 2021a (pp. 10-14): period-1 participants,
    prevalent CHD, ANYCHD and deaths by sex, BMI/cholesterol/glucose N and means, BPMEDS counts, mean TIMECHD and TIMEDTH.
  - The Kaggle CSV shreyjain601/framingham-heart-study holds the same 453,453 values in the same order.
- Second raw file: MIT's `framingham.csv` (4,240 x 16), pinned OCW URL. It is read only for the evidence table of the
  target decision.
- Licence:
  - BioLINCC teaching page: free on request; "Users are cautioned that teaching datasets are completely unsuitable for
    publication purposes since specific statistical measures were used to create anonymous versions". NHLBI's teaching
    page had the same wording on 2005-03-07 (web archive capture saved in `evidence/`).
  - riskCommunicator: GPL-3. MIT OCW: CC BY-NC-SA.
  - Kaggle pages: "unknown" (aasheesh200, dileep070, christofel04) or "CC0-1.0" (shreyjain601). The data owner stated
    neither.

**Definition:** `datasets/_dev/tabarena-v0pt2/framingham_heart_study_fhs/`.
- Prediction point: the baseline exam (period 1, roughly 1956). A physician predicts a first CHD event within 10 years
  for a participant free of CHD from the 15 risk factors of that exam (sex, age, education, smoking, cigarettes per day,
  BP medication, prevalent stroke and hypertension, diabetes, total cholesterol, systolic and diastolic BP, BMI, heart
  rate, casual glucose).
- Target `chd_within_10_years`: ANYCHD = 1 with TIMECHD <= 3,652 days.
  - 379 Yes, 3,845 No (9.0%).
  - No event, death or censor date falls on days 3,648-3,654, so the cut-off is not sensitive.
- Regime: IID, the default 3 x 3-fold split (train 2,816, test 1,408). 4,224 rows x 15 features, all numeric.
- Cleaning:
  - Cohort: period 1 with PREVCHD = 0, the documentation's own population at risk (p. 5).
  - Deaths: the 251 participants who died without CHD within 10 years are No (competing-risk label; 32 died within 2
    years, 99 within 5).
  - Lost to follow-up: 16 participants whose CHD follow-up ended within 10 years without an event are dropped (unknown
    status). They were all alive at the end of follow-up; only the event surveillance stopped.
  - Drops: RANDID, the columns constant in the cohort (PERIOD, TIME, PREVCHD, PREVAP, PREVMI), HDLC and LDLC (period 3
    only) and all follow-up event and time columns.
  - Features renamed to MIT's names; SEX mapped to `male` 0/1; age and the complete flags stored as int64.
- Missing values: real NaN, no sentinels (glucose 384, education 105, BPMeds 53, totChol 49, cigsPerDay 29, all of them
  current smokers, BMI 19, heartRate 1).
- Two `_decisions` tables: MIT's label by 10-year outcome, and the cohort flow.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); no accepted warnings.
- Checksum v2:37b31be46138..., the same under pandas 2.3.3 and 3.0.6 (shared pd3 venv).
- pytest:
  - `pytest tests/test_v2_datasets.py` now fails at collection on another unit's scaffold (`perth_house_prices`,
    `problem_type = "TODO"`), not on this folder. Before that scaffold appeared, the dataset's tests passed (2 passed
    with `DATA_FOUNDRY_V2_DATA_CHECKS=1`).
  - The same two tests, run on a private root that links only this folder (`private_root_test.py`), pass: the report
    belongs to the definition, and a fresh `check()` gives the README checksum.
- The import check passes, ruff is clean, and no TODO is left.

**Probes:** shipped splits, `--n-jobs 2`. The verifier re-ran all four and got the same numbers.
- Task probes (9 of 9 splits):
  - ROC AUC: logistic regression 0.739, random forest 0.704, LightGBM 0.677, best single feature 0.643 (age on all 9
    splits).
  - The linear model beats the dummy on 9 of 9 splits (SE of its skill 0.013); smallest class per test fold: 126.
  - Flags: none.
- Leak probes (3 splits):
  - LightGBM 0.658; depth-2 and depth-3 trees 0.649 and 0.654; best single feature age 0.640, then prevalentHyp 0.609
    and male 0.589.
  - Missing indicators 0.498-0.512. Without age 0.637, without male 0.646.
  - 0.0% exact copies across the split; 1-NN agreement 0.943 in the closest tenth against 0.837 by chance.
  - The NN distance alone scores 0.619. Within quintiles of a logistic-regression risk score it is about 0.5
    (0.48-0.59 over four fits of the score): positives have more extreme risk factors, not class-conditional generation.
  - No leak signal. Every feature is measured at or before the baseline exam.
- Generated-data probe: 0 rule leaves, no flag.
- Hidden groups: 4 candidates (totChol, glucose, heartRate, age), none eligible, no hits (gaps -0.014 to -0.006).
- Extra checks, by hand:
  - Later-exam PREVCHD is consistent with the event days in 6,980 of 6,980 exams.
  - Every MI_FCHD or ANGINA event is also ANYCHD and no later.
  - CURSMOKE and CIGPDAY agree.
  - All 34 glucose values of 200 mg/dL or more in the cohort are diabetics.

**Issues for Lennart:**
1. **Target: the Kaggle/MIT `TenYearCHD` is wrong for 265 of its 644 positives, and the endpoint is a choice.**
   - Evidence: `TenYearCHD` equals `TIMECHD < 3,652 days` in 4,240 of 4,240 rows (any cut-off from 3,647 to 3,654 gives
     the same). "Had a CHD event within 10 years" matches only 3,975 rows. TIMECHD is the day of the first CHD event
     or, without one, the "censor date ... end of followup, death or last known contact date if subject is lost to
     followup" (BioLINCC documentation 2021a, p. 4).
   - So 249 participants who died of other causes and 16 lost to follow-up within 10 years are positives. Only 379
     positives had a CHD event.
   - Implemented: the label rebuilt from ANYCHD/TIMECHD of the teaching data (4,224 rows, 379 Yes). Quick 3 x 3-fold
     ROC AUC (LightGBM / logistic regression): 0.699 / 0.739 on ours, against 0.692 / 0.723 on MIT's label.
   - Alternative: ship MIT's file and label as published (4,240 rows, 644 positives). I advise against it: 41% of its
     positives are not CHD. The same defect is in every paper or notebook that uses this Kaggle file.
   - Endpoint, your call:
     - ANYCHD (implemented): angina, MI, coronary insufficiency or fatal CHD. 379 Yes; the CHD of MIT's task.
     - Hard CHD (MI_FCHD: hospitalized MI or fatal CHD): the endpoint of the FHS hard-CHD 10-year risk page that the
       record links. 191 Yes (about 64 per test fold), 0.741-0.749 / 0.783-0.788.
2. **Competing deaths are No (the verifier agrees).**
   - Implemented: the 251 participants who died without CHD within 10 years are No, also those who died early (32
     within 2 years, 99 within 5, median day 2,193). This is the cumulative-incidence label.
   - Alternative: drop them, like the censoring of the Framingham risk functions: 3,973 rows, 379 Yes.
   - Against it: dropping them selects the cohort on an event after the prediction point and removes high-risk
     negatives. Their mean age is 54.8 against 54.1 for the CHD cases and 48.8 for the CHD-free; mean systolic BP 143.5
     against 144.0 and 130.3. Logistic regression rises from 0.737-0.739 to 0.751-0.754 (three seeds) only because
     these hard negatives go.
3. **The teaching data is anonymized, and BioLINCC calls it unsuitable for publication.**
   - BioLINCC teaching page: "teaching datasets are completely unsuitable for publication purposes since specific
     statistical measures were used to create anonymous versions". Documentation p. 1: "specific methods were employed
     to ensure an anonymous dataset ... this dataset is inappropriate for publication purposes".
   - What was changed is undocumented. Nahhas, *Introduction to Regression Methods for Public Health Using R*,
     App. A.6, names "permutations and/or random visit selection".
   - The riskCommunicator man page (the copy we read) states NHLBI's permission and omits the caveat. BioLINCC's
     teaching-request terms are behind a login; neither the verifier nor I read them.
   - The terms are noted, not a reason. The data-quality part is a real question: results on this task measure methods
     on perturbed data, and a benchmark publishes those results.
   - No visible damage:
     - systolic and diastolic BP correlate at r 0.78 at baseline;
     - within a person, BMI and systolic BP 6 years apart correlate at r 0.90 and 0.71; values permuted across
       participants at one exam would weaken this;
     - ages match the exam days in 3,930 of 3,930 period-2 and 3,263 of 3,263 period-3 exams;
     - HDL + LDL never exceeds total cholesterol (3,026 exams); the event logic is consistent;
     - 3 of 4,434 participants (all in the cohort, No either way) have a CHD censor date after their death.
   - Implemented: added, with these numbers in the Anomaly bullet and the terms in `license`.
   - Options:
     - tag `2ndTierData` ("not of the highest quality but still a reasonable task"; not applied: no defect found, and it
       is your quality call);
     - do not ship. The real FHS data needs a BioLINCC research application and cannot be redistributed.
4. **Record metadata, and the year.**
   - The record says `original_source: Kaggle`, `year: 2013` (MIT's course). The definition reads the teaching data
     itself, so `source = "GOV Website"` (BioLINCC) and `year = "2004"`.
   - 2004 is the creation date of the first SAS file (documentation pp. 8-9: PROC CONTENTS of 2004-03-02, 38 variables,
     without educ). NHLBI's teaching page offered the dataset by 2005-03-07 (web archive). The file we read has 39
     columns, with EDUC in the variable table (p. 2), so it is a later revision; BioLINCC does not state its date.
   - Your call on the year: 2004 (the teaching dataset), 2013/2017 (MIT's cut), or the revision year if BioLINCC states
     one.
   - The record's `source_links` could add the BioLINCC teaching page, riskCommunicator and the MIT OCW file. Its first
     link (christofel04) withholds 848 labels.
5. **Raw-data route.**
   - CRAN ships an `.rda`, so `download_description` has a conversion step (`uvx` pyreadr, or `write.csv` in R).
     The Kaggle CSV shreyjain601 is an identical alternative if a plain download is preferred.
   - The MIT file is read only for the evidence table. If you prefer fewer raw files, drop it and keep the numbers in
     the comments.
6. **SelectArena: the same defect, and a wrong domain.**
   - `datasets/_dev/feature_selection/framingham_heart_study/framingham_heart_study.ipynb` builds a container from the
     aasheesh200 file with MIT's `TenYearCHD`, so it carries the defect of issue 1.
   - It also sets `domain_str="physics & astronomy"` (the verifier confirmed both).
   - For awareness; not touched.

**Verification:** the verifier's verdict is "ready with noted concerns"; it found no error, leak or wrong number.
1. Competing deaths and the endpoint: **applied**. I recomputed 32 within 2 years, 99 within 5, ages 54.8 / 54.1 /
   48.8 and logistic regression 0.737-0.739 → 0.751-0.754. The competing-risk bullet now says early deaths count as No
   and why dropping them would select on a later event. ANYCHD against hard CHD is in issue 1, and the target bullet
   names hard CHD (191 Yes).
2. Anonymization numbers: **applied**. I recomputed r 0.784, the within-person r 0.903 / 0.714, the age match
   3,930 / 3,930 and the cholesterol check 3,026 / 3,026; they are now in the Anomaly bullet. The riskCommunicator
   omission and the login-gated terms are in issue 3. The optional `2ndTierData` tag is not applied; it is left as
   Lennart's call in issue 3.
3. Lost to follow-up: **applied**. All 16 have DEATH = 0 and TIMEDTH = 8,766, and their TIMECHD, TIMECVD, TIMEMIFC and
   TIMESTRK are equal (recomputed). The bullet says so; the drop stays.
4. Year: **applied as wording; the value stays 2004** (Lennart's call). The year bullet and issue 4 now say that the
   2004 file had 38 variables without educ and that ours is a later revision. The March 2005 claim is checked from the
   web archive capture of 2005-03-07, saved as `evidence/nhlbi_teaching_page_2005-03-07.txt` (the verifier could not
   reach the archive).
5. Nearest-neighbour range: **applied**. Four fits of the risk score give 0.48-0.59 (in-sample and three out-of-fold
   seeds). My earlier 0.53-0.55 was one seed. The text now says "about 0.5 (0.48-0.59 over four fits of the score)".
6. BibTeX: **applied**. riskCommunicator is cited with Jessica Grembi as its only author (Rogawski McQuade is `ctb`).
   The record comment now says "uploads" (christofel04 is two files).
- After the fixes: `dataset check` gives 0/0/0; the checksum v2:37b31be4... is the same under pandas 2.3.3 and 3.0.6;
  ruff is clean; the import check passes; the private-root test passes. Repo pytest fails at collection on
  `perth_house_prices`, not on this folder.

### fraud_detection_in_electricity_and_gas_consumption
**Outcome:** added and checked, as `datasets/_dev/tabarena-v0pt2/fraud_detection_in_electricity_and_gas_consumption_1m/`,
revised after verification: the history is now cut at 2013-01-01. The frame has 1.91M invoices, so it ships as the
`_1m` version with `version_of` the record.

**Record judgment:** valid with concerns. This is real STEG billing data released for a predictive task. The Zindi
overview says "Using the client's billing history, the aim of the challenge is to detect and recognize clients
involved in fraudulent activities", and the challenge scores ROC AUC on one probability per client. The data first
ran as "AI Hack Tunisia #4 - Predictive analytics challenge #1" (20-22 Sep 2019). It is not in the working copy or
in this run's other records. Concerns:
- the invoices from 2013 carry traces of the inspections that set the labels (issue 1; the cut removes them, but its
  date is read off the data);
- the labels of clients who left before 2013 look unrecorded (issue 2).

The record's AI Summary holds: 4,476,749 invoices of 135,493 clients, one label per client. As Lennart's comment
says, the split is grouped by client: the label has no date, and Zindi's test file holds 58,069 other clients over
the same years.

**Data:** Kaggle mirror `mrmorj/fraud-detection-in-electricity-and-gas-consumption` (uploaded 2020-08-24). Zindi needs
a login.
- We keep `client_train.csv` (135,493 x 6) and `invoice_train.csv` (4,476,749 x 16). The zip also holds Zindi's test
  files (58,069 clients, no labels) and the sample submission.
- The mirror is faithful. Its `client_train.csv` has the same sha256 as a copy committed to GitHub on 2020-06-29
  (matzolla/STEG_fraud_detection_in_electricity_and_gaz_consumption), and its `invoice_train.csv` matches the profile
  printed by Zindi's starter notebook (135,493 clients, 8,275 distinct invoice dates, 201,893 meter serials).
- Both sha256 are in `download_description`, and the download uses `uvx --from kaggle==2.2.2 kaggle`.
- Licence: Zindi's rules (competition page) say the data is "the sole property of Zindi and the competition host"
  and forbid redistribution; the mirror states "other".

**Definition:** `fraud_detection_in_electricity_and_gas_consumption_1m`.
- Prediction point: on 2013-01-01, STEG scores each client from its client record and its invoices of 2005-2012 to
  decide whom to inspect. The labels look recorded in 2013-2019; the date of a finding is not in the data.
- Target `fraud` (Yes/No), binary, ROC AUC (Zindi's metric).
- Regime: grouped by `client_id`, with `labels="per_group"`, `prediction_unit="group"`, `aggregation="mean"`,
  `context="all_rows"`.
- Splits:
  - Cohort: the 83,874 clients billed both before and after the cut (6,504 frauds, 7.8%), with 1,907,490 invoices.
  - Sub-sampled to 1.5M rows by whole clients (66,014 clients).
  - 1 x 3 grouped folds: train 999,406-1,000,000 rows, test 499,145-500,000 rows, 21,983-22,004 test clients per
    fold.
- Size: 1,500,000 rows x 18 features (+ group column and target). One row per invoice before 2013, with the
  client's district, category, region and creation date joined on `client_id`.
- Cleaning:
  - The cohort and the cut (issues 1 and 2).
  - We drop 9 exact duplicate invoices.
  - We drop `consommation_level_4`: the fourth tier first appears in January 2014, so before the cut it is 0 on all
    2,051,073 invoices.
  - `counter_number` 0 is set to missing (12,555 invoices).
  - We rename `disrict` to `district` and `target` to `fraud`.
  - The codes are categoricals and the two dates datetimes.
  - Odd codes (34 `counter_statue` invoices, 21 `reading_remarque` invoices, mostly rows shifted by one column) and
    `months_number` above 24 (806 invoices) are kept as the source has them.
- `_decisions`:
  - fraud rate by the quarter in which a second electricity meter or counter status 5 first appears (2011Q1-2014Q4);
  - fraud rate by the year of the last invoice;
  - ties on the latest date.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 1 accepted. `splits_rows_never_tested`: the 500k test cap trims 860 rows
  (0.06%, 31 whole clients), the same acceptance as amex_non_iid_1m and sepsis_prediction_1m.
- ruff clean; `pytest -q tests/test_v2_datasets.py -k fraud_detection_in_electricity`: 1 passed, 1 skipped (the
  opt-in data check). No `TODO(verify)` left.
- pandas 2.3.3 and 3.0.6 (the shared `scratchpad/venvs/pd3`) give the same checksum,
  `v2:6e92005ef1aa84f533f7cef708b3886f2f6448921a73f8526017ead1bd470318`, for the final file. `check()`, the
  decisions included, runs under both.

**Probes:** on the cut definition, 2026-10-07, thread-capped. They ran on an isolated root that symlinks the folder,
because another agent's half-written folder broke `discover_datasets` on the working copy.
- leak_probes (per invoice, untuned LightGBM, 3 splits, 50k rows a side): no leak flag.
  - All features ROC AUC 0.618; depth-2 / depth-3 tree 0.567 / 0.584.
  - Single features: `region` 0.597, `district` 0.569; dropping either costs little (0.605 without `region`).
  - No test row has an exact copy in train. 1-NN label agreement is 0.850 against a chance level of 0.844, and the
    label-free distance scores 0.526.
- task_probes (per client, mean, 3 of 3 splits): no flags.
  - dummy 0.500, linear 0.608, random forest 0.668, LightGBM 0.655, single feature (`region`, all 3 splits) 0.581.
  - The best family beats the dummy on 3 of 3 splits (SE 0.011); spread 0.119 (paired SE 0.013).
  - Smallest class: 162 fraud clients per test fold.
- generated_probes: rule leaves cover 0.0% of the minority rows; no flags.
- group_probes (100,031 invoices of 4,382 clients, the shipped 1 x 3 folds, 20 permutations):
  - LightGBM on a random split of the invoices scores 0.984, against 0.572 grouped (gap 0.412).
  - Per row / per client: logistic regression 0.615 / 0.610, random forest 0.590 / 0.633, LightGBM 0.573 / 0.606,
    kNN 0.543 / 0.613.
  - Permutation test: 0.633 against a null mean of 0.494 (95% quantile 0.525), p = 0.048, the smallest value 20
    runs can give.
- Own experiment6 (shipped folds; LightGBM fit on all training invoices):
  - 0.656 per invoice. Per client: mean 0.685, largest prediction 0.684, latest date 0.682 / 0.684 (ties broken by
    the largest / the mean).
  - The invoice count alone scores 0.543. Among non-fraud clients, the per-client score follows the invoice count
    more for the largest prediction (Spearman 0.31) than for the mean (0.24).
  - A client-level LightGBM on simple aggregates, fit on the same clients, scores 0.662.

**Issues for Lennart:**
1. **History cut at 2013-01-01 (implemented) or the full history (the challenge's task)?**
   - Evidence: among the 116,360 clients billed from 2013, the fraud rate of clients whose second electricity meter
     first appears in a quarter is 7.4-11.9% for each quarter of 2012 and 23.8-25.9% for each quarter of 2013. It
     is 33.1% for all second meters from 2013, against 8.1% before.
   - Other codes show the same step. Counter status 5: 9.5% in 2012Q4, 23.7% in 2013Q1. A new `counter_code`: 7.5%
     against 35.7%. A new `tarif_type`: 7.7% against 26.1%.
   - The number of such events per quarter does not jump, so the step is in the labels.
   - 11,731 clients carry a 2013+ meter or status-5 change. 30.8% of them are frauds, against 3.8% of the others;
     they hold 47.8% of all frauds, and that flag alone scores AUC 0.70.
   - With the full history, a client-level LightGBM scores 0.848 (0.764 without the meter counts). With the cut, the
     models score 0.61-0.69.
   - Alternative: the full history of the 116,360 clients billed from 2013, with a `Potential leak, kept on purpose`
     bullet. That is the challenge's task, but about half of its frauds are recognised by the trace of their own
     inspection.
   - The cut date is read off the data. STEG or Zindi could confirm when the labels were set.
2. **Cohort: clients billed both before and after the cut.**
   - Dropped: the 19,133 clients whose last invoice is before 2013. They have 21 frauds (0.11%), and by the year of
     the last invoice the fraud rate is 0-0.15% up to 2011, 0.8% for 2012 and 3.9-8.3% from 2013, so their labels
     look unrecorded.
   - Also dropped: the 32,486 clients whose first invoice is from 2013 on (no history at the prediction date; 3.2%
     frauds).
   - Alternative (only with the full history): keep the 32,486 newer clients too, or all 135,493 as Zindi does. The
     early leavers are easy negatives: 0.869 with them against 0.848 without, client-level LightGBM.
3. **Group prediction rule: `mean` (implemented), `any` (the verifier's proposal for the cut) or `last`.**
   - On the cut, the rules tie: mean 0.685, largest 0.684, latest date 0.682-0.684.
   - The largest prediction grows with the number of invoices, and so does the fraud rate (5.3% for 1-3 invoices,
     9.4% for more than 40). Its per-client score follows the count more (Spearman 0.31 against 0.24).
   - `last` needs a tie rule: 50% of the clients have several invoices on their latest date before the cut.
   - I chose `mean`: the label belongs to the client, and every invoice is one observation of it.
4. **Context and size.**
   - The `_1m` sub-sample keeps 66,014 of the 83,874 clients.
   - With the cut, a row model averaged per client (0.685) does as well as simple client aggregates (0.662), so the
     task does not depend on the harness building group features. The context is still `all_rows`.
   - Alternative: one row per client with aggregates of our own (83,874 rows, IID). That is feature engineering the
     guidelines leave to the pipeline, and Lennart's record comment points to the invoice rows.
5. **Duplicate record.** `indabax_drc_2022` (TBD -> Yes, AI unverified) is the same STEG data. Its Zindi data page
   lists the same files (train.zip 61.2 MB, test.zip 26.4 MB, SampleSubmission.csv 2.1 MB) and says "The data
   provided by STEG is composed of two files". It should become `No` + `Duplicate` of this record.
6. **Extract date.**
   - The data first ran on 20-22 Sep 2019. github.com/mohamedScikitLearn/AI-Hack-Individual- (created 2019-09-23)
     holds submissions for the same 58,069 test clients.
   - Yet 29,121 train invoices (17,616 clients) are dated after 22 Sep 2019, up to 2019-12-07: the dates are shifted,
     or the files were refreshed later.
   - The cut uses the data's own dates, so this changes no decision.
7. **Source and download.**
   - The Kaggle mirror is used because Zindi needs a login. A curator with a Zindi account can compare `train.zip`
     against the sha256 sums.
   - Zindi's rules forbid redistribution (noted, not a verdict reason).

**Verification:**
1. Inspection footprints: applied. I recomputed the verifier's numbers, and they agree to the last digit (2013Q1
   step, 11,731 clients, 47.8%, AUC 0.702). The history is cut at 2013-01-01 for the 83,874 clients billed before
   and after. The full history is issue 1's alternative, with the numbers.
2. `any` rule: applied. The multiple-instance reason is gone from `Grouping.definition`, and the definition states
   the tie. I switched to `mean` rather than keeping `any`: on the cut, the rules tie (0.685 / 0.684 / 0.682-0.684),
   and the largest prediction follows the invoice count more (Spearman 0.31 against 0.24). The alternatives are
   issue 3.
3. "Latest invoice is no alternative": applied. The text now says `last` would need a rule for the ties (50% of the
   clients have several invoices on their latest date), with the tie scores.
4. Year: applied. `year = "2019"`, BibTeX key `zindi2019stegfraud`, year 2019, and the note names "AI Hack Tunisia #4
   -- Predictive analytics challenge #1 (20--22 September 2019)". I checked the GitHub repo's description and
   creation date. The 29,121 invoices after 22 Sep 2019 are a `Note:` bullet and issue 6.
5. `indabax_drc_2022`: left to the orchestrator. It is issue 5, a record edit for Lennart.
6. pandas 3 evidence: applied. The final definition gives `v2:307a4b4e…` under both pandas 2.3.3 and 3.0.6.
- The verifier's other points:
  - Mirror evidence and the `uvx` command: applied in `download_description`.
  - Record `v2_path` and build: left to the curator (`sync-notebooks` and `dataset build` are not ours to run).
  - The cut made `consommation_level_4` constant (`dataset_constant_column`); it is dropped, with a bullet.

### g_research_crypto_forecasting

**Outcome:** added and checked: `datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m/` (a `_1m` version, `version_of = "g_research_crypto_forecasting"`). All probes finished; their numbers and the flag answers are in `curation_comments`, and the README was regenerated after the last edit (checksum `v2:972e659fa683db1ed8102118ad18754610c280a0c7c52f92b3592e2ba47408ee`, after the verifier's fixes).

**Record judgment:** valid with concerns. By its own description the competition is time-series forecasting: "you'll use your machine learning expertise to forecast short term returns in 14 popular cryptocurrencies" (Overview, Description), "This is a forecasting competition with an active training phase and a second period where models will be run against real market data" (Overview, Timeline), "Your challenge is to predict their future returns" (Data). The target is each asset's own return over the next 15 minutes, residualised against the 14-asset market return. That matches the guidelines' exclusion "predict future values of a series: demand/sales/price over a horizon". The record already weighs this ("Forecasting-as-tabular task", `Yes`, checked by Lennart; GETTING_STARTED §7.2 lists it as accepted), so I added it and give the counter-argument as issue 1. Provenance is clear: G-Research built the data for the competition from "many different data providers" (organiser post, discussion 286779). Unique: no other minute-level crypto data in the working copy, the other records or this run (`cryptocurrency_closing_price_prediction` is a different Zindi task and already `No`).

**Data:** Kaggle competition `g-research-crypto-forecasting`, files `train.csv` (24,236,806 rows x 10 columns: one row per asset and minute, 14 assets, 2018-01-01 00:01 to 2021-09-21 00:00) and `asset_details.csv` (14 x 3), both dated 2022-01-26, downloaded with `uvx --from kaggle==2.2.2 kaggle competitions download -f ...` (2.8 GB unzipped; `supplemental_train.csv` not used). Licence: Kaggle competition rules, "DATA ACCESS AND USE: Competition Use Only" (Rules page, section A and B.7.A).

**Definition:**
- Folder `g_research_crypto_forecasting_1m`. Prediction point: at the close of minute t, predict for each asset its return from t+1 to t+16 minus beta times the weighted 14-asset return (beta from a trailing 3,750-minute window; tutorial notebook and organiser post 286778). Known then: all one-minute bars up to t.
- Target `Target`, regression, RMSE (the competition scored a weighted Pearson correlation; noted in the comments).
- Temporal on `timestamp`: `TemporalSplits(window=91, unit="days", n_windows=3, gap=1)`. Test windows 2021-06-22 to 2021-09-20, 2021-03-23 to 2021-06-21 and 2020-12-22 to 2021-03-22 (about 1.83M rows each before sampling); each window sampled to 500k rows, each train side a random 1M of the 18.0M-21.6M earlier rows (`subsample_to_budget`). The 91 days follow the competition's 3-month live scoring period; the 1-day gap keeps every training label (which needs the next 16 minutes of prices) known at the cutoff.
- Shipped frame 2,501,039 rows x 27 features (full frame 23,486,468 rows). Features: `timestamp`, `Asset_Name` (category, from `Asset_ID` via asset_details.csv), the bar (`Count`, `Open`, `High`, `Low`, `Close`, `Volume`, `VWAP`) and 18 history features of the 3rd-place solution: for 60, 300 and 900 minutes, log Close over its trailing mean and the log return, their 14-asset means (`market_*`), and the asset's difference from the mean (`*_minus_market`). They are computed per asset on the full minute grid from Close up to t, with gaps forward-filled for at most 100 minutes as in that solution. A spot-check of 2,000 random rows against a direct computation found 0 mismatches.
- Cleaning: 750,338 rows without a target dropped (3.1%; the competition does not score them), after the features are computed; 7 infinite and 8 negative `VWAP` values set to missing (all Maker, 15-24 June 2020); `timestamp` converted from Unix seconds to datetime. No duplicate (timestamp, asset) rows. Anomalies kept as recorded: 3 negative volumes, 18 bars with `Low` below half the body, 3 with `High` above twice the body, and 266 targets beyond ±0.2 (156 of them Bitcoin Cash, November 2018).
- pandas 2.3.3 and 3.0.6 build the same container from the final definition: checksum `v2:972e659fa683db1ed8102118ad18754610c280a0c7c52f92b3592e2ba47408ee` in both (same numpy 2.1.3).

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info (`dataset_duplicates_skipped`: 70M cells exceed the 50M budget of the duplicate checks; the raw file has no duplicate (timestamp, asset) key, so no row can repeat). No accepted warnings. ruff clean; the class imports; `pytest -q tests/test_v2_datasets.py -k g_research`: 1 passed, 1 skipped (the opt-in data check).

**Probes:**
- Generated data: exact fits 1.6% against 1.5% on a shuffled target (65 terms, 4,000 rows); no flag.
- Signal (my own runs, 1M train and 500k test rows per window, untuned): with the bar alone, LightGBM correlates 0.012, -0.006 and 0.002 with the target (ridge 0.005, -0.020, 0.003). With the history features, LightGBM correlates 0.037, 0.051 and 0.040 (ridge 0.028, 0.041, 0.023). R² against the train mean is still -0.002 to -0.006 for LightGBM and -0.003 to +0.001 for ridge. Rank correlations with the target on the shipped frame: history features -0.05 to -0.06 (`*_minus_market`, 60 min); bar features -0.01 to 0.00. `Volume`'s Pearson 0.023 is tail-driven (Spearman -0.007).
- Regularised check (LightGBM with early stopping on the newest 10% of each train side; ridge with alpha chosen there), shipped splits, R² against the train mean (correlation): LightGBM +0.00073 (0.029), +0.00115 (0.034), -0.00028 (0.034) in windows 0, 1, 2 (62, 40 and 363 trees); ridge +0.00048 (0.024), +0.00111 (0.035), -0.0040 (0.015).
- Leak probes (untuned LightGBM, 50k train and test rows, 3 windows): all features R² -0.090, depth-2/3 trees -0.082/-0.074, every single feature and missing-value indicator at or below 0 (best `Asset_Name` -0.000), drop-one tests unchanged, 0.0% of test rows with an exact feature copy in train, 1-NN R² -2.03 (closest tenth) and -1.04 (all). No leak: nothing gives the target away; the negative R² is overfitting to noise on 50k rows.
- Task probes (3 windows, 300k train and test rows each, untuned): flags `no_signal`, `drift_baseline`, `unstable`. Skill against the train mean: linear -0.0001 (above the dummy in 1 of 3 windows, standard error 0.003), LightGBM -0.022, random forest -0.040, best single feature -0.001 (a different one per window).
- Flag answers (task_probes.md; also in `curation_comments`): `no_signal` comes from untuned models; the regularised check above beats the train mean in 2 of 3 windows and correlates positively in all 3, a small real signal (rule 2: no reason to retire). `drift_baseline` is not drift: the target is centred on zero (window means about 1e-5 against standard deviations of 0.0044-0.0069), so the newest-rows constant and the train mean give the same squared error to five digits (1.8958e-05 in window 0). `unstable`: with a signal this small, a window can fall below the mean (window 2, R² -0.00028 for the early-stopped LightGBM).

**Issues for Lennart:**
1. **Scope: forecasting (recommendation: `No` + `Time-series (Forecasting)` unless you confirm the record's acceptance for this case).** Evidence: the competition calls itself "a forecasting competition" (Timeline) and served rows one minute at a time through a time-series API; the target is the asset's own Close(t+16)/Close(t+1) - 1, residualised against the market (rebuilt from Close by the verifier, median error 5e-7); the bar alone correlates 0.012, -0.006 and 0.002 with it, so all the signal comes from the 18 lags of the same Close series that the definition adds. It would be the only working-copy dataset built on lagged targets (numerai ships the source's point-in-time features; rossmann and ashrae use exogenous inputs, and ashrae in this run draws the line at "no lagged targets"). The record's first comment predicted "will likely mostly be noise". Implemented now: added under the record's one-line acceptance ("Forecasting-as-tabular task"), with the lagged-target design named in the scope bullet. Alternative: retire, as `cryptocurrency_closing_price_prediction`, `appliances_energy_prediction` and `combined_cycle_power_plant` were.
2. **Engineered history features.** Question: may the definition add the 3rd-place solution's 18 lagged-return features? The house rule allows feature engineering only to remove leaks or rebuild destroyed meaning. Evidence: without them the task has no signal (correlation about 0.00 in all three windows); with them it is 0.037-0.051. Precedents: `electric_motor_temperature_prediction` adds the paper's EWMA features, and `acquire_valued_shoppers_challenge` uses TabReD's aggregation from a top solution. Implemented now: own-asset features plus 14-asset means and differences, one row per asset and minute. Alternatives: the raw bars only (a no-signal task), or the solution's wide layout with every asset's features in every row (174 columns).
3. **Near-zero signal under RMSE.** Question: is a task whose best measured R² is +0.0012 (correlation 0.03-0.05) a useful benchmark? Evidence: untuned models score below the train-mean predictor on RMSE while still correlating 0.04, so method rankings will hinge on shrinkage. The competition's weighted Pearson correlation would be a dataset-specific metric, and the adapter does not use those yet (BENCHMARK_CHANGES_TODO.md, "Dataset-specific metrics"). R² below 0 against the train mean holds for the untuned models only: in my runs untuned LightGBM is below the mean in all three windows (R² -0.002 to -0.006), but ridge (alpha 1) beats it in window 1 (+0.0008) and ties it in window 0 (-0.0000005), and the regularised models beat it in windows 0 and 1 (early-stopped LightGBM +0.00073 and +0.00115, tuned ridge +0.00048 and +0.00111) and not in window 2 (LightGBM -0.00028, ridge -0.0040), while correlating 0.015-0.035 in every window. By task_probes.md rules 1-2, `no_signal` from untuned models is a question, not a retirement reason; a method does beat the mean, so the signal is small but real, about a tenth of forest_fires' R² 0.013. The verifier's day-block analysis: early-stopped LightGBM R² 95% intervals [-0.0001, 0.0016], [0.0002, 0.0022], [-0.0021, 0.0017], so only window 1's gain is outside the day-to-day noise; it is not distinguishable from tuned ridge day by day (paired t 0.72, 0.17, 1.48); its daily correlation is positive on 73, 70 and 78 of 91 days (t 7.0, 6.6, 9.2). Under RMSE the ranking measures shrinkage, under correlation it measures signal. Implemented now: RMSE (default), with the `unstable` answer rewritten to these numbers. Proposal: register the competition's correlation once dataset-specific metrics are supported (BENCHMARK_CHANGES_TODO.md), as for `numerai_v5_2_1m`; or do not add the dataset (issue 1).
4. **Windows.** Implemented: 3 x 91 days with a 1-day gap, from the competition's 3-month live scoring; each window holds about 1.83M rows before sampling. Alternative: `TemporalSplits(window=3, unit="months", n_windows=3)` covers the same span, but its gap would have to be a whole month; shorter windows would leave the frame unchanged in size but test less time.
5. **Grouped by asset not used.** The record's `required_split` also lists `Grouped (NON-IID)`, and GETTING_STARTED says "temporal + grouped ... (anonymisation)". I chose temporal only: the competition forecasts the same 14 assets, and 14 groups would only test a shift between assets (the covertype precedent). The assets are named in asset_details.csv, so the `Anonymized` tag does not apply.
6. **Follow-ups.** Run `sync-notebooks` to set the record's `v2_path` to the `_1m` folder (outside my write scope). Licence: competition use only (noted, not a reason).

**Verification (independent verifier, 2026-10-06; verdict "should not ship" by the guidelines' scope, otherwise ready with noted concerns):**
- Finding 1 (major, scope): issue for Lennart (issue 1, rewritten with the verifier's numbers and the recommendation `No` + `Time-series (Forecasting)` unless Lennart confirms the acceptance); the scope bullet of `curation_comments` now names the lagged-target design; record comment rewritten.
- Finding 2 (major, metric): issue for Lennart (issue 3, with the day-block intervals and the correlation-metric proposal); applied to the definition: the `unstable` answer now says only window 1's gain is outside the day-to-day noise, with the numbers, and the metric note says RMSE ranks methods by shrinkage until dataset-specific metrics are supported.
- Finding 3 (minor, comments): applied. Recounted from train.csv: 7 infinite (6 +inf, 1 -inf) and 8 negative VWAP values, all Maker, 15-24 June 2020 (6 and 7 in rows with a target), 9 missing (3 with a target); the gap sentence now distinguishes rolling means (missing when the window reaches into a gap of more than 100 minutes) from returns (missing when the start minute is).
- Finding 4 (minor, inner validation): applied: `splits_comment` now says validation inside a train side has to split by time blocks, with the random-row versus newest-10% numbers.
- Finding 5 (record pointer): for the orchestrator (`sync-notebooks`).
- After the fixes: `dataset check` 0 errors, 0 warnings, 1 info; pandas 2.3.3 and 3.0.6 checksum `v2:840406ce…` in both; ruff clean; `pytest -k g_research` 1 passed, 1 skipped.

### glioma_grading_clinical_and_mutation_features
**Outcome:** added and checked

**Record judgment:** valid with concerns. The record asks whether the task is mostly feature selection. It is a
classification task: the UCI page states "The prediction task is to determine whether a patient is LGG or GBM with a
given clinical and molecular/mutation features" ("For what purpose was the dataset created?"), and the paper's
experiments classify the grade with 10-fold cross-validation (Tasci et al. 2022, IJMS 23(22):14155, Sec. 2.1; AUC 0.908
to 0.920, Table 3). Feature selection is the paper's method. The concern is the label (issue 1).
Uniqueness: no other record or working-copy folder holds this table (grep for UCI 759, OpenML 46604, DOI
10.24432/C5R62J, the Kaggle slug, "glioma", "TCGA"). It shares patients with lgg_low_grade_glioma and glioblastoma but
not the task (issue 3).

**Data:** UCI dataset 759 (DOI 10.24432/C5R62J), static zip
`https://archive.ics.uci.edu/static/public/759/glioma+grading+clinical+and+mutation+features+dataset.zip`. It holds
`TCGA_GBM_LGG_Mutations_all.csv` (862 x 27, the original file; the definition reads it) and `TCGA_InfoWithGrade.csv`
(839 x 24, the authors' preprocessed and numerically coded file, identical in size to OpenML 46604). Licence: CC BY 4.0
(UCI page). The underlying data are TCGA-LGG and TCGA-GBM open-access data from the NCI GDC, which the authors queried
through NIDAP (paper, Sec. 2.2 and Acknowledgments).
- Provenance traced against the GDC API (2026-10-07): `Grade` equals the TCGA project in all 862 rows. The 20 mutation
  flags match the GDC's current somatic calls in 17,220 of 17,240 cells. The 20 others (13 calls the GDC no longer makes,
  7 new ones) fall in 9 genes, none in IDH1 or IDH2. Every patient has WXS data, and none has only a targeted panel.
  The 70 patients without a mutation in the 20 genes have 3 to 110 calls in other genes, so `NOT_MUTATED` means
  wildtype and not "not tested". The 857 age strings match the GDC's primary-diagnosis record exactly (the portal's
  "X years Y days" rendering of age_at_diagnosis in days).

**Definition:** `datasets/_dev/tabarena-v0pt2/glioma_grading_clinical_and_mutation_features/`.
- Prediction point: a diffuse glioma has been resected or biopsied and its DNA sequenced. The model assigns LGG (WHO
  grade II/III) or GBM (grade IV) from 20 mutation flags plus sex, race and age at diagnosis.
- Target `Grade` (LGG 499, GBM 363), binary, roc_auc. IID with the default 10 x 3 folds (train 574-575, test 287-288
  rows); one row per patient.
- 862 rows x 23 features (22 categorical, age numeric).
- Cleaning:
  - drop `Project` (a copy of the label), `Primary_Diagnosis` ("Glioblastoma" in 360 of 363 GBM rows and in no LGG
    row) and `Case_ID`;
  - `--` and `not reported` become missing;
  - the age text becomes years as years + days / 365.25 (within one day of the GDC's day count);
  - the 23 patients with a missing demographic are kept (issue 2);
  - the gene flags stay `MUTATED` / `NOT_MUTATED` categories.
- A `_decisions` table shows the diagnosis-by-grade crosstab and the mutation shares by grade.
- `source_url` is the UCI DOI. The scaffold had pre-filled the record's first link, OpenML.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). No accepted warnings, no `TODO` left.
- `pytest tests/test_v2_datasets.py -k glioma_grading...`: 2 passed, including the raw-data rebuild with
  `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- ruff is clean.
- pandas 2.3.3 and 3.0.6 give the same checksum, `v2:057682cd8bcd2b4068ce4626a21b189c98b1cf8060baf8efe3a59c78bb47fe88 (after the
  verification round)`.
- Not run, per the brief: `sync-notebooks` (the record's `v2_path` is still empty) and `build`.

**Probes:** none flags anything.
- `leak_probes.py` (3 splits):
  - all features 0.900 with untuned LightGBM; depth-2 / depth-3 tree 0.881 / 0.901;
  - IDH1 alone 0.860, age 0.769; without IDH1 0.857;
  - missing indicators 0.500 each, so missingness carries no label;
  - 0% exact copies;
  - 1-NN agreement 0.809 (chance 0.512); nearest-neighbour distance alone 0.588.
- `task_probes.py` (30 of 30 splits), no flags:
  - logistic regression 0.919, random forest 0.922, LightGBM 0.897; the best family beats the dummy on 100% of splits
    (SE 0.005);
  - single feature IDH1, chosen on 30 of 30 splits, 0.860 (skill 0.720 against 0.843);
  - the smallest class in a test fold has 121 rows.
- `generated_probes.py`: rule leaves cover 6.5% of the minority class (the flag needs 20%). No flag.
- `hidden_groups.py`: 0 candidates (one patient per row, continuous age).
- Own check on the 30 splits (logistic regression): all features 0.921, IDH1 with age 0.902, IDH1 0.860, age 0.812. A
  depth-3 tree on all features gives 0.892.
- Outputs: `<scratch>/glioma_grading/{leak_probes.txt, task_probes/, generated_probes/, hidden_groups/,
  subset_probe.txt}`. The GDC comparisons are in `gdc_*.py`.

**Issues for Lennart:**
1. **The label is the TCGA-era histological grade. That fits the task, but WHO 2021 renames part of it.**
   - Question: is a histological LGG / GBM label acceptable when today's classification renames some of its tumours?
   - Evidence: `Grade` is the TCGA project. The GDC dates 858 of the diagnoses between 1989 and 2013. 128 LGG rows
     are "Mixed glioma" (oligoastrocytoma), which WHO 2021 counts among the "poorly defined entities". WHO 2016 still
     graded IDH-mutant tumours "depending on histological parameters" (Louis et al. 2021, Neuro-Oncology 23(8):1231).
     WHO 2021 reserves glioblastoma for IDH-wildtype tumours, but the 25 IDH-mutant GBM rows would become "Astrocytoma,
     IDH-mutant", still CNS WHO grade 4. So the grade stays the same, and only a "glioblastoma or not" label would
     follow from IDH. Some of the 87 IDH-wildtype LGG rows would become glioblastomas (TERT promoter, EGFR
     amplification, +7/-10), and an IDH-mutant astrocytoma with a CDKN2A/B deletion becomes grade 4. None of these
     markers is in the data. The label is not built from the features: without IDH1 and IDH2, ROC AUC is 0.888
     (logistic regression) and 0.893 (random forest), against 0.92 with all features.
   - Implemented: the source's label, with a corrected curation note.
   - Alternative: a WHO-2021 relabel. It needs copy-number and TERT data from the GDC, which makes it a new dataset.
     I do not recommend it.
2. **The 23 patients with a missing sex, age or race are kept: 862 rows.**
   - Question: keep them, or match the source's 839?
   - Evidence: the authors' file and OpenML 46604 drop them (839 rows). Missingness carries no label (indicator AUC
     0.500; 12 LGG, 11 GBM), and the GDC has no age for the 5 rows without one either.
   - Implemented: kept, with NaN.
   - Alternative: drop them to match the paper and OpenML. That is one `dropna` on the three demographic columns.
3. **Two multi-omics candidates of this run share the patients.**
   - Question: is a patient overlap across datasets acceptable?
   - Evidence: lgg_low_grade_glioma shares 240 of its 247 patients with this file, and glioblastoma 180 of its 274.
     Those predict molecular subtypes within one grade from omics profiles; this one predicts the grade from 20
     mutation flags. It is the "Shared source ≠ duplicate" case of the curation guidelines.
   - For the 240 shared LGG patients, IDH1 or IDH2 here equals the IDH part of the lgg_low_grade_glioma class
     (199 mutant, 41 wildtype, no mismatch). That matters only for a method trained across datasets.
   - Implemented: the curation note names the records, so it holds whether or not those folders ship.
   - Alternative: none needed, unless cross-dataset training requires disjoint patients.
4. **IDH1 and age carry most of the signal.**
   - Question: is the remaining signal enough for a benchmark task?
   - Evidence: IDH1 alone gives 0.860 and IDH1 with age 0.902, against 0.92 for all features. Both are the natural
     core of glioma grading (rule 4 of task_probes.md), and the probes raise no `one_feature` or `no_spread` flag.
     Methods spread: random forest 0.922, logistic regression 0.919, untuned LightGBM 0.897.
   - Implemented: kept as a small tabular task.
   - Alternative: none recommended. The tuned BeyondArena results do not cover this new dataset.

**Verification:** the verifier's verdict was "ready with noted concerns". Its three minor findings were all applied
after I re-checked each claim. Since the changes, `dataset check` reports 0 errors and 0 warnings, ruff is clean,
pytest gives 2 passed, and pandas 2 and 3 give the same checksum.
- **Verification (finding 1, WHO wording):** applied. I confirmed in Louis et al. 2021 the quotes "were assigned to 3
  different tumor types ... depending on histological parameters" and "the presence of CDKN2A/B homozygous deletion
  results in a CNS WHO grade of 4". The GDC gives diagnosis years 1989 to 2013 for 858 cases. "Mixed glioma" is
  ICD-O-3 9382/3 at the GDC. Without IDH1 and IDH2, ROC AUC is 0.888 / 0.893 on the shipped splits.
  - "WHO 2016 dropped mixed glioma" is not stated in Louis et al. 2021, and the 2016 paper is behind a login. The note
    therefore cites the 2021 sentence on "poorly defined entities (eg, oligoastrocytomas ...)".
  - The Note bullet was replaced, and issue 1 corrected.
- **Verification (finding 2, project / site / batch confound):** applied. The added bullet is "Checked, no leak", and
  the reason for dropping `Case_ID` now names the site code. My recomputed numbers:
  - 45 sites, none with both projects;
  - a by-site split scores like a random one (5 x 3 folds; logistic regression 0.919 against 0.918, random forest
    0.921 against 0.921; the verifier had 0.922 against 0.918);
  - the passenger genes add 0.002 to 0.004;
  - the 20 differing cells lie in 17 GBM rows;
  - all 6,532 call observations come from primary tumour samples (sample type 01, recounted from the verifier's GDC
    file).
- **Verification (finding 3, overlap note):** applied. The note now names the two candidates' records, so it holds
  whether or not they ship, and adds the IDH-class equivalence (recomputed: 199 / 41, 0 mismatches) as a caution for
  cross-dataset training.
- Outputs of the re-checks: `site_probe.txt`, `subset_probe.txt`.

### hepatitis_c_egypt

**Outcome:** not added (generated or replaced data: no column of the file depends on another; curation criterion 4B,
marker `AHDS`). Nothing was written to `datasets/_dev/tabarena-v0pt2/`. A complete, checked definition for the case
Lennart overrules is kept at `<scratch>/defs/hepatitis_c_egypt/dataset.py` (its README next to it); it can be copied to
the working copy as is. `<scratch>` is
`../_scratch_new65/_run_reports/new65/hepatitis_c_egypt/`.
An independent verifier tried to refute this and upheld it (`<scratch>/verify/verify.md`).

**Record judgment:** do not add. Criterion 4B ("not from a real random distribution (artificial / deterministic)") and
the generated-data tests of `.claude/skills/check-candidate/SKILL.md` ("Checking whether the data is generated", tests 4
and 6: marginals too even, real-world structure missing). The record's comments do not weigh this: they suspect a leak
through the follow-up ALT columns (from an LLM answer); the data shows the opposite, no column carries information.
Evidence, strongest first (my scripts: `<scratch>/generator_tests.py`, `generator_c2st.py`; the verifier's:
`<scratch>/verify/verify_stats.py`, `verify_c2st.py`; every number below that I did not compute myself was re-run or
re-read by me, except where marked "verifier"):
- No dependence that HCV data must show (Spearman, 95% noise band 0.053): AST vs ALT 0.037, ALT visit to visit -0.033
  to 0.021, RNA baseline vs week 4 0.019, RBC vs HGB 0.043, platelets vs stage -0.017, age vs stage -0.020, grade vs
  stage of the same biopsy -0.046; mean HGB 12.59 for men and women (the UCI codebook itself gives HGB ranges by
  gender). 21 of 406 column pairs fall outside the band, about the 20 chance gives; without the 3 pairs inside the RNA
  block the 403 p-values are uniform (KS p = 0.77, verifier). FIB-4 against the stage: ROC AUC 0.491 (stage >= 2),
  0.487 (>= 3), 0.470 (4); in 19,501 Egyptian HCV biopsies FIB-4 reaches 0.71 for advanced fibrosis and 0.82 for
  cirrhosis (El-Kassas et al., Sci Rep 2024, article 29544, abstract).
- The one structured block does not behave like treatment response: 381 rows have RNA undetectable (value 5) at week
  12, end of treatment and end of follow-up; their RNA values are otherwise independent (-0.02 to 0.01 among the 999
  detectable rows). These responders do not differ in grade, stage, baseline RNA, age or BMI (AUC 0.49-0.53), while
  the first creator's own genotype-4 cohort found low grade and stage (P < 0.029), low baseline RNA, older age and
  higher BMI predictive (Kamal et al., Hepatology 2007;46:1732, abstract). Undetectable RNA at week 4: 1 of 1,385,
  against 69 of 318 there. Their late ALT equals the others' (medians 82-84 vs 83-84, p 0.61-0.96).
- Values replaced, not shuffled: a per-column shuffle of real values would keep their skew, but AST and the six ALT
  visits are uniform on the integers 39-128 (chi-square p 0.13-0.78; skew +0.03 and +0.02, against +1.82 and +2.43 for
  the 75 HCV patients of `hepatitis_c_prediction`); the creator's genotype-4 trial reports mean ALT of 129.5-136.2 U/L,
  above this file's maximum of 128 (Kamal et al., Gut 2005, Table 1, verifier). Each symptom is present in 49.6-51.6%
  of patients. Baseline and week-4 RNA are spread evenly on a linear 0-1.2M scale (10% below 100,000, 32-35% above
  800,000), not over orders of magnitude. Replacement inside the codebook's bins is ruled out too: the
  bins fill in proportion to their widths (WBC 153 / 1,056 / 176 against 153 / 1,064 / 167) and no bin relates to the
  stage (p 0.25-0.89, verifier).
- Two-sample tests support this but have little power on their own. Real rows against rows whose columns were permuted
  one by one (disjoint halves): forest AUC 0.498 without the RNA block (mine), 0.476-0.480 for three classifiers with
  the block kept together (verifier), against 0.62-0.99 on seven real clinical tables. Against my written-down uniform
  generator: 0.499, against 1.000 for the German HCV labs; that 1.000 comes mostly from skewed marginals, and a planted
  AST-ALT correlation of 0.30 leaves these classifiers at 0.48-0.51 (verifier), so they cannot carry the case alone.
- No task in the file: the stage from the 17 baseline features gives macro ROC AUC 0.48-0.51 (logistic regression,
  random forest, extra trees, LightGBM; 5 x 5-fold CV), from all 28 features 0.48-0.50, log loss above the class prior
  on 21-25 of 25 folds; CatBoost defaults 0.487 / 0.499, above the prior on 25 of 25 folds (verifier). Treatment
  response as the target: AUC 0.49-0.51; the biopsy grade: R² -0.02 to -0.06.
- The source explains none of it. UCI 503 says "Egyptian patients who underwent treatment dosages for HCV about 18
  months" (dataset page, abstract) and names no synthesis, anonymisation or shuffling. Nasr et al. (ICENCO 2017, pp.
  276-281, DOI 10.1109/ICENCO.2017.8289800) report "average accuracy 99.48% for 5-folds cross validation" (abstract;
  the paper is closed access, only the abstract was read). Citing papers report high scores from broken protocols:
  Akella & Akella (medRxiv 10.1101/2020.11.02.20224840) duplicate the minority class (step 4 of Fig. 1) before the
  70/30 split (step 7), and their clean F1-vs-F4 experiment "generally hovered within 0.34 and 0.64", three models
  "below 0.5" (Results); Elshewey et al. (Diagnostics 2023, hyOPTGB, PMC10670002) give a dummy classifier 81.3%
  accuracy on this balanced 4-class target (Table 4). None of about 20 citing papers, about 15 Kaggle uploads or their
  discussion threads says the data are synthetic (verifier; my Kaggle search agrees).
- Uniqueness, for completeness: not a duplicate. The German "HCV data" (UCI 571, DOI 10.24432/C5D612) is
  `hepatitis_c_prediction` in the working copy: blood donors and HCV patients (Hoffmann et al. 2018), 615 rows, other
  columns. `hepatitis_survival_prediction` is UCI 46 (1988). No other record of this run is about hepatitis. OpenML
  46607 (uploaded 2025-02-17) is the UCI file: identical values in the same order.

**Data:** UCI 503 static zip,
https://archive.ics.uci.edu/static/public/503/hepatitis+c+virus+hcv+for+egyptian+patients.zip, in
`local-data-warehouse/hepatitis_c_egypt/`: `HCV-Egy-Data.csv` (1,385 rows x 29 columns, no missing values; sha256
6a9ca49f...0e401) and `Discretization-Criteria.csv` (the codebook). Licence CC BY 4.0 (UCI dataset page, "License").
The raw files can be deleted if the dataset stays out (66 KB zip).

**Definition (scratch only, not in the working copy):** `<scratch>/defs/hepatitis_c_egypt/dataset.py`.
- Prediction point: before the liver biopsy, when treatment is planned (the paper's use case: a non-invasive
  substitute for the biopsy, abstract).
- Target `fibrosis_stage`, 1-4 read as F1-F4 per the UCI codebook (F0-F4 listed, four codes present; 336 / 332 /
  355 / 362). Multiclass, `log_loss`, IID, default splits 10 x 3 (train 923-924, test 461-462).
- 1,385 rows x 17 features: age, gender, BMI, 7 symptoms, WBC, RBC, HGB, platelets, AST and ALT at week 1,
  baseline RNA. Dropped: ALT at weeks 4-48 and after treatment, RNA at week 4, week 12, EOT and end of follow-up
  (after the prediction point), and the biopsy grade (same biopsy as the target). Gender and symptoms mapped to
  labels. No duplicate rows or feature vectors.
- A `_decisions` table shows the missing correlations; the "Anomaly" bullet in `curation_comments` states the reason
  not to ship, now led by the dependence evidence.

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 info (26 checks). Same checksum under pandas 2.3.3 and 3.0.6
(`v2:b1abe30e...d41b893e`). ruff check and format clean under the repository config (linted with
`--stdin-filename` at the working-copy path). Import check passes. `tests/test_v2_datasets.py` is pinned to the
working copy, so its two assertions were run on the scratch root instead (`<scratch>/replica_tests.py`): both pass
under pandas 2 and 3. The all-features probe variant (`<scratch>/defs_all/`) also checks clean (28 features,
0 warnings).

**Probes (`<scratch>/probes_defs/`, `<scratch>/probes_defs_all/`):**
- Baseline variant (17 features), `leak_probes.py` (3 splits): all features macro AUC 0.471, depth-2/3 trees
  0.498 / 0.495, best single feature `age` 0.526, no missingness, 0.0% exact copies, 1-NN label agreement 0.255
  (chance 0.250).
- Baseline variant, `task_probes.py` (30 of 30 splits): dummy log loss 1.386; linear 1.411 (skill -0.018), random
  forest 1.422 (-0.026), LightGBM 2.162 (-0.561), single feature 1.576; the best family beats the dummy on 0% of the
  splits. Flags `no_signal`, `unstable`. Answer (task_probes.md rule 2: retire for a concrete reason found in the
  task): the reason is found, every column, the label included, is independent of the others. No tuned results
  exist for a new dataset; a strong default method (CatBoost, verifier) stays at chance too (rule 1).
- Baseline variant, `generated_probes.py`: rule leaves cover 0.0% of the minority rows; no flag (see issue 4).
- Baseline variant, `hidden_groups.py`: 3 candidates (age, ALT and AST at week 1), no hits, gaps +0.03.
- All-features variant (28 features, follow-up ALT and RNA and the grade kept), `leak_probes.py`: all features
  0.487, depth-2/3 trees 0.492 / 0.489, best single feature `nausea_vomiting` 0.520 (the only follow-up column in
  the top eight is `RNA 4`, 0.513), 0.0% copies, 1-NN agreement 0.247 (chance 0.250). `task_probes.py` (30 of 30
  splits): dummy 1.386; linear 1.437 (skill -0.037), random forest 1.405 (-0.014), LightGBM 2.083 (-0.504), single
  feature 1.565; macro AUC 0.497-0.501; the best family beats the dummy on 0% of the splits; flags `no_signal`,
  `unstable`. `generated_probes.py`: 0.0%, no flag. `hidden_groups.py`: 9 candidates, no hits.

**Verification:** upheld; the verifier's findings and what was done with each:
- **Verification:** no source refutes the judgment (UCI page and API, the Nasr 2017 abstract, about 20 citing papers,
  about 15 Kaggle uploads, GitHub). Folded into the evidence; I re-read Akella's Fig. 1 steps and Results and
  Elshewey's Table 4 in the verifier's downloads and confirm both.
- **Verification:** anonymisation does not explain the file: the values were replaced, not shuffled (skew, the
  Kamal 2005 ALT means above the file's maximum), and bin-preserving replacement is ruled out. Folded into the
  evidence and issue 3; I recomputed the skews (German patients n = 75: +1.82 / +2.43) and the WBC bins.
- **Verification:** no expected clinical dependency holds, including FIB-4 against stage and the creator's own
  predictors of response; undetectable week-4 RNA 1 of 1,385 against 69 of 318. Recomputed (FIB-4 AUCs, response
  AUCs, week-4 count) and checked against the El-Kassas 2024 and Kamal 2007 abstracts; now the lead evidence.
- **Verification:** the empirical-marginals two-sample test agrees (0.476-0.480; seven real clinical tables
  0.62-0.99). Added as support.
- **Verification:** my headline test was weaker than it read (the German 1.000 is mostly skew; a planted AST-ALT
  correlation of 0.30 goes unseen). Accepted: the record comment and the "Anomaly" bullet now lead with the
  dependence evidence, and the classifier tests are stated with that limit.
- **Verification:** markers are Lennart's call; `AHDS` fits, `Data Quality Issue` can be added. Added to issue 1.
- **Verification:** the probe extension should be the conjunction, not the pair share alone. Replaces my proposal in
  issue 4; I re-read the calibration table and confirm the conjunction flags UCI 503 alone.

**Issues for Lennart:**
1. Verdict. Question: keep `Yes`? Evidence above: no dependence that HCV data must show is present, the values are
   flat over their ranges, and the stage cannot be predicted from any subset. Implemented: not added; proposed record
   comment (116 words) in `<scratch>/hepatitis_c_egypt.record_comment.md`. Markers, your call: `AHDS` fits; add
   `Data Quality Issue` too if you read it as a real table with replaced values, which is as likely as a fully
   synthetic one (the creators ran genotype-4 cohorts with this design: RNA at weeks 4 and 12, end of treatment and
   24 weeks after; Kamal et al. 2005, 2007). Alternative: copy `<scratch>/defs/hepatitis_c_egypt/` into the working
   copy; it ships a task where every method ties with the class prior, which adds only noise to the rankings.
2. The record's "ALT features are future follow-up measurements, temporal leakage" (from an LLM) is half right: the
   columns are measured during and after treatment, so a definition at the biopsy drops them, but they do not leak.
   With all 28 features the models stay at macro AUC 0.48-0.50.
3. Where the file comes from is not settled. The paper's 99.48% (abstract) cannot come from this file, so the UCI file
   is either a copy whose values were replaced column by column or a synthesised one; shuffled real values and
   replacement inside the codebook's bins are both ruled out (evidence above). The paper is closed access. To read it:
   Google "A novel model based on non invasive methods for prediction of liver fibrosis" pdf, or IEEE Xplore with DOI
   10.1109/ICENCO.2017.8289800. The creators UCI lists (Sanaa Kamal, Mohamed ElEleimy, Doaa Hegazy, Mahmoud Nasr)
   could be asked for the real records; that would be the revisit condition.
4. Probe gap (report, not patched): `generated_probes.py` tests formula targets and rule leaves only, so a generator
   that draws every column independently, label included, passes it (no flag here, on either variant). Proposal,
   calibrated by the verifier over 125 working-copy datasets, the 5 retired generated ones and the raw UCI 503 file
   (`<scratch>/verify/pair_share_calibration_n1000.csv`): the share of column pairs beyond the noise band alone does
   not separate (santander 5.1%, UCI 503 5.7%, biogeographical_ancestry 6.0%, audiology 6.4%). Adding the share of
   numeric columns that a KS test cannot tell from a uniform over their range does: flag only "pair share <= 10% and
   uniform share >= 0.5 of >= 5 numeric columns", which hits UCI 503 alone (0.65; next highest homesite 0.46;
   97 of the other 100 frames at or below 0.2). Report both numbers as information. Compute them on a fixed
   1,000-row sample (the band shrinks with n), use chi-square for categorical columns, and if a classifier test is
   added, permute disjoint halves instead of resampling with replacement, which fakes AUC 0.54-0.58 here. The mark
   covers one generator family (every column independent); churn and healthcare_insurance_expenses stay with
   `formula` / `rule_leaves`.
5. If the dataset is kept anyway (issue 1), two definition choices: `AST 1` / `ALT 1` are labelled "1 week" in the
   UCI codebook (`ALT 1` also in the variable list), so strictly one week into treatment; they are kept as the first
   enzymes (alternative: drop them). The biopsy grade is dropped as a result of the same biopsy (alternative: keep it
   as a pathology co-variable, which changes the task to "stage given grade").

### high_storage_system_data_for_energy_optimization
**Outcome:** not added (the anomaly labels are generated: the anomalous files are the normal recordings with segments
edited in software). No dataset folder was created.

**Record judgment:** do not add: simulated labels (criterion 4B, marker `AHDS`). The record's comments ("Anomaly
detection task, could be framed as classification, unsure") do not weigh this.
- The authors say so. von Birgelen & Niggemann (2018), "Enable learning of Hybrid Timed Automata in Absence of
  Discrete Events through Self-Organizing Maps", in Niggemann & Schüller (eds.), *IMPROVE*, Technologien für die
  intelligente Automation 8, Springer Vieweg, pp. 37-54, doi 10.1007/978-3-662-57805-6_3 (open access, CC BY 4.0;
  the second paper on the Kaggle data card). Sec. 4.2 "High Rack Storage System", p. 49: "The training data contains
  107 cycles of the same transport operation. Evaluation data contains 113 cycles and was generated by modifying the
  training cycles in different ways such as increasing or decreasing one or multiple signals by different amounts
  (e.g. 20%), shortening of cycles and inserting constant sequences. This artificially generated anomalies are
  labelled and are used to calculate the scores of the anomaly detection." The Kaggle card calls the same files "runs
  with failures".
- The Kaggle files show the same construction, although their counts differ from the paper's (106 and 111 cycles,
  18 signals, 10,187 labelled rows; the paper has 107 / 113 cycles, 17 signals, 7,365 labelled anomalies):
  - each anomalous file has the cycles of its normal file (106 standard, 111 optimized; the timestamp resets to 0 at
    each cycle start);
  - 17,869 of 17,975 (99.4%) and 15,002 of 15,117 (99.2%) label-0 lines of the anomalous files occur verbatim in the
    normal files, 16-digit timestamps and all 18 signals included; only 1.0% / 1.4% of the label-1 rows do;
  - every cycle equals its normal cycle up to the edit; in all 58 + 64 cycles of unchanged length the label is the
    edit mask shifted by one row (the first edited row is labelled 0 in all 90 + 96 cycles where the edit is visible);
  - examples from the standard file: cycle 0 adds a constant 9,395.66 to `O_w_BLO_power` for 63 rows; cycles 3 and
    4 drop one drive's power and voltage to near 0, hold its position and end the cycle there (109 and 80 of 247 and
    244 rows); cycle 7 scales the `HL` rail's power and voltage to about a quarter and ends there (52 of 246 rows).
- Precedents: `leak_checks.md` §3, "Generated or manipulated data: retire (`AHDS`, `Data Quality Issue`)";
  `smart_meter_electricity_consumption_dataset` (`No` + `AHDS`, an anomaly-detection candidate).
- Secondary: the labels are per row of a stream sampled every ~56 ms (cycles of ~15.2 s standard, ~11.9 s
  optimized), and most anomalies are defined by the sequence (shortened cycles, inserted constant sequences, a
  delayed tail): 72% / 63% of the label-1 rows repeat the 18 signal values of a row of the same normal cycle, and only
  1.0% / 1.4% also keep its timestamp.
  The source detects them with a hybrid timed automaton over the sequence (criterion 4A; marker
  `Time-series (Classification)`, precedent `eeg_eye_state`).
- Uniqueness: no other record and no working-copy folder holds this data (grep for HRSS, high storage, inIT-OWL,
  SmartFactory); not in `RECORDS.txt` twice.

**Data:** Kaggle dataset `inIT-OWL/high-storage-system-data-for-energy-optimization`, uploaded by the institute (inIT,
TH OWL, Lemgo; files dated 2019-10-02). Four CSVs of 20 columns (`Timestamp` = seconds since the cycle start,
`Labels`, and position `Weg`, power and voltage of 4 conveyor belts and 2 rails): `HRSS_normal_standard.csv` 25,907
rows, `HRSS_anomalous_standard.csv` 23,645 (5,670 label 1), `HRSS_normal_optimized.csv` 21,329,
`HRSS_anomalous_optimized.csv` 19,634 (4,517 label 1). Licence CC BY-NC-SA 4.0 (data card, Acknowledgements; noted,
not a reason). Downloaded to `local-data-warehouse/high_storage_system_data_for_energy_optimization/` (7.2 MB) for
this analysis only; it can be deleted.

**Definition:** none.

**Checks:** none (no definition).

**Probes:** the probe scripts need a v2 folder, so none ran. Own probes in this folder: `hrss_edits.py` (the copy and
shift evidence above, output `hrss_edits_output.txt`) and `hrss_probe.py` (output `hrss_probe_output.txt`): the two
anomalous files only (43,279 rows, 23.5% label 1, 217 cycles), untuned LightGBM (300 trees, 2 threads), 3-fold CV
grouped by cycle.

| features | ROC AUC (folds) | average precision |
|---|---|---|
| Timestamp, 18 signals, program | 0.835 (0.786, 0.858, 0.862) | 0.734 |
| the same, signals rounded to integers | 0.829 | 0.719 |
| rounded, without Timestamp | 0.661 | 0.399 |
| Timestamp (time in cycle) alone | 0.671 | 0.386 |
| "some signal is not a whole number", no model | 0.620 | 0.411 |

The readings are integers, and the injection scales or offsets them: 21.8% / 27.9% of the label-1 rows hold a
non-integer value, against 0.3% / 0.5% of the label-0 rows (the off-by-one edited rows). That is a class-specific
recording artefact (`dataset_patterns.md` §D.13); rounding removes it for 0.006 AUC.

**Issues for Lennart:**
1. **Generated anomalies: set the record to `No` + `AHDS`?** Evidence: the chapter quote and the file comparison
   above. Implemented now: nothing, no folder. Alternative, if a fault-injection task is wanted anyway: the anomalous
   files only (the normal files would add an unedited copy of every cycle, a copy across any split), grouped by cycle
   (217 cycles, labels per row), signals rounded to integers; untuned LightGBM reaches ROC AUC 0.829, and the time in
   the cycle alone (0.671) carries as much as the 18 signals without it (0.661).
2. **Second marker `Time-series (Classification)`?** Even with recorded failures, the task labels single samples of a
   ~18 Hz sensor stream, and the injected anomalies are defined over time (see the secondary bullet above). Secondary
   to issue 1.
3. **The record's "Preprocessing rel" notebook is not a reference.** `horikitasaku/pr-auc-0-9054-catboost-baseline`
   concatenates the normal and anomalous files (each normal cycle next to its edited copy), sorts all rows by the
   within-cycle timestamp and then takes row differences across cycles, splits rows at random (`StratifiedKFold`,
   shuffled) and early-stops on the test fold. Its PR AUC of 0.905 says nothing about the task.
4. **No other task in the files.** The title's energy optimization compares the normal standard and optimized runs
   (two control programs of one transport operation); the data card offers it for "energy based optimization
   processes", which has no target.

### house_prices_nominal
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/house_prices_nominal/`); verifier findings applied
(2026-10-07).

**Record judgment:** valid with concerns. The data first appeared in De Cock (2011), "Ames, Iowa: Alternative to the
Boston Housing Data as an End of Semester Regression Project", Journal of Statistics Education 19(3),
doi:10.1080/10691898.2011.11889627: "a data set describing the sale of individual residential property in Ames, Iowa from
2006 to 2010 ... 2930 observations" (abstract, p. 1), built for predicting sale prices (pp. 4-5: MODEL2 is scored on a
held-out validation set). The record's links are a later cut of it: the Kaggle competition's train.csv (Kaggle
Description page: "The Ames Housing dataset was compiled by Dean De Cock") and OpenML 42165 (that train.csv; OpenML
42563 "house_prices_nominal" holds the same 1,460 rows). Unique: no Ames data in the working copy; the only other Ames
record, `ames_housing_dataset`, is a Kaggle mirror equal to AmesHousing.txt in all 2,930 x 82 cells and is already
`No` + `Duplicate`; no other record of this run is Ames. Concerns: the record links the Kaggle half, not the original
(issue 1), and its `Trivial` marker is not borne out (issue 3).

**Data:** De Cock's text file from the JSE site, https://jse.amstat.org/v19n3/decock/AmesHousing.txt (2,930 rows x 82
columns, tab-separated, sha256 6cfe6cb5...cfcc), in `local-data-warehouse/house_prices_nominal/AmesHousing.txt` (0.96 MB).
Documentation: https://jse.amstat.org/v19n3/decock/DataDocumentation.txt. Licence as stated: JSE "Policy for Using Data
Sets": "Data Sets may be freely used in teaching without contacting the author or JSE for permission ... To use data
sets in papers, books, or other published material you must obtain the consent of the contributing author"
(https://jse.amstat.org/jse_users.htm). Kaggle's copy falls under its competition rules.

**Definition:** prediction point: a house sells, and an automated valuation model refit every two months on all
earlier sales predicts its price from the assessor's record of the property and the sale type and condition (as in
house_sales and zillow_prize). Target `log_SalePrice` (natural log of `SalePrice`; RMSE on it is the competition's
metric, Kaggle Evaluation page). Temporal on `Month Sold` (a date at the first day of the month, from `Yr Sold` +
`Mo Sold`): `TemporalSplits(window=2, unit="months", min_train_fraction=0.5)` = 13 windows, May-June 2010 back to
May-June 2008, test 46-191 rows, train 1,469-2,758, no gap (a price is known once the sale is recorded). 2,919 rows x
78 features (44 categorical, 33 numeric, 1 datetime). Cleaning: dropped the 8 sales of July 2010 (the extract cut the
month: 101-122 sales in July 2006-2009); dropped De Cock's three partial-sale outliers over 4,000 sq ft and kept the
two NoRidge market sales over 4,000 sq ft; dropped `Order` (row number sorted by year and parcel) and `PID` (unique
parcel number); the documented "NA" level of 14 columns written out ("No basement", "No garage", ...) and kept apart
from the missing values (two garages with unknown details stay missing); `MS SubClass` codes replaced by their
documented labels; `Sale Type` "WD " stripped; `Garage Yr Blt` 2207 set to missing; 2 pairs of neighbouring parcels
with identical features and different prices kept; `Year Remod/Add` floor at 1950 and the allocation-sale blocks
documented and kept. Three `_decisions` tables (July counts, window lengths, the 5 houses over 4,000 sq ft).

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info (`dataset_conflicting_duplicate_rows`: the 2 twin-parcel
pairs, documented in `curation_comments`). No accepted warnings. Same checksum under pandas 2.3.3 and 3.0.6
(v2:aa5e7143...e0b8). `pytest tests/test_v2_datasets.py -k house_prices_nominal`: 1 passed, 1 skipped; the definition
imports; ruff check and format clean; no TODO. The record's `v2_path` is still unset (orchestrator: `sync-notebooks`).

**Probes** (after the fixes; the discovery under the working copy crashed on another agent's scaffold,
`perth_house_prices` with `problem_type = "TODO"`, so I ran them on a root holding only a symlink to this folder):
- Leak (untuned LightGBM, first 3 windows, R²): all features 0.872; best single feature `Overall Qual` 0.611; depth-2/3
  tree 0.545/0.636; no drop-one loss above 0.01; missing indicators at most 0.063 (`Garage Yr Blt`, i.e. no garage); 0%
  test rows with an exact copy in train; 1-NN R² 0.934 in the closest tenth, 0.765 overall. Answer: no leak. The close
  neighbours are tract houses (83-94% same neighborhood, 50-76% same first six parcel digits in the three newest
  windows) sold at different times: comparable sales. Recorded in `curation_comments`.
- Task (13 of 13 windows): RMSE in log price linear 0.124 (R² 0.904), LightGBM 0.125 (R² 0.901), random forest 0.136,
  train mean 0.409; best family beats the dummy on 13/13 windows; spread linear - RF 0.019 R² (paired SE 0.005); single
  feature `Overall Qual` (chosen 13x) R² 0.682, RMSE 0.228. Flags: none.
- Generated: 6.6% of rows fit exactly, the same as for a shuffled target; no flag.
- Hidden-group / group probes: not run (temporal task). Each parcel occurs once (De Cock kept only the latest sale per
  property), so no entity repeats across windows; blocks of allocation sales share a month and so a window.

**Issues for Lennart:**
1. **Source: De Cock's full file instead of the Kaggle train file the record links.** Evidence: all 1,460 Kaggle
   train rows equal a De Cock row in every feature and the price; the 1,459 test rows (no prices) are the rest, minus
   the 11 sales of Greens (8), GrnHill (2) and Landmrk (1), with some values blanked; train share 47.5-52.2% per sale
   year (a random split). Implemented: De Cock's file (2,919 rows after the July 2010 cut and the 3 outliers), 13
   two-month windows of 46-191 test rows (median 98). Alternative: the Kaggle train file (1,454 rows after the July
   cut): 12 two-month windows of 22-96 rows, or 8 quarterly windows of 41-123. Record edits to consider:
   add the JSE file (https://jse.amstat.org/v19n3/decock/AmesHousing.txt) and the DOI
   (https://doi.org/10.1080/10691898.2011.11889627) to `source_links`; the folder keeps the record's name, which is
   OpenML's name for the Kaggle half, and a name such as `ames_housing` would describe the data
   (`ames_housing_dataset`, the cell-for-cell Kaggle mirror of De Cock's file, stays `Duplicate`).
2. **Window length.** Implemented two-month windows (13 windows, 46-191 test rows). Monthly windows: 26 windows of
   19-112 rows (winter months below the ~50-row rule); quarterly: 8 windows of 91-233 rows.
3. **`Trivial` marker not borne out.** `Overall Qual` alone, chosen on each training side, reaches R² 0.682 (RMSE
   0.228) against 0.901-0.904 (0.124-0.125) for the untuned linear model and LightGBM; as a per-grade mean it is worse
   than a 500-tree LightGBM (RMSE 0.119, R² 0.912) in all 13 windows; De Cock's own two-variable model (neighborhood +
   total area, p. 13 "about 80%") reaches R² 0.766 and is never better. No task-probe flag; models spread (linear - RF
   0.019 R², paired SE 0.005). Proposed: drop the marker (record comment written).
4. **Prediction point.** Implemented "a house sells" (an automated valuation model, as in house_sales and
   zillow_prize), so `Sale Type`, `Sale Condition` and `Month Sold` are known and stay, and no gap is needed (prices are
   known once a sale is recorded). Feature effects (500-tree LightGBM, 3 seeds, 13 windows): dropping `Sale Condition`
   costs +0.0047 RMSE (SE 0.0008, worse in 13 of 13), `Sale Type` +0.0000 (SE 0.0005), `Month Sold` -0.0002 (SE
   0.0007). Alternative: predict at the purchase agreement, one or two months before the sale; that needs a gap of that
   length, which changes RMSE by +0.0006 (SE 0.0010) for one month and +0.0026 (SE 0.0013) for two.
5. **De Cock's outliers.** Implemented (verifier finding 1): drop the 3 partial sales over 4,000 sq ft ($28-$40 per sq
   ft against a median of $150 for partial sales; De Cock p. 4: "true outliers (Partial Sales that likely don't
   represent actual market values)"), keep the 2 NoRidge market sales. All five sold before the oldest test window.
   Effect: the probe's linear model RMSE 0.133 -> 0.124; verifier: ridge -0.0067 (SE 0.0038), LightGBM -0.0016 (SE
   0.0013). Alternatives: keep all five (the first version), or drop all five as De Cock recommends for students
   (ridge -0.0068, LightGBM -0.0012, verifier).
6. **June 2010** has 82 sales against 97-112 in June 2006-2009, and is cheaper: mean log price 11.931 against
   11.985-12.077 in June 2006-2009 and 12.009 in May 2010 (median $149,950 against $155,000-$169,750). In the newest
   window LightGBM's RMSE is 0.202 on June and 0.089 on May, partly from two allocation sales. Late recording before
   the July 2010 extract or the market after the first-time-buyer tax credit; the file cannot tell. Kept.
7. **Allocation sales.** The 24 "Alloca" sales (two linked properties with separate deeds; 16 of them in blocks of
   neighbouring parcels sold in one month, e.g. 8 SawyerW duplexes in June 2009 at $113,722-$153,337) and 12 "AdjLand"
   purchases are kept with the sale condition as a feature; a block shares a window. Their price can be a share of a
   joint price: in the newest window two IDOTRR allocation sales ($50,138, $55,993; residuals -0.55 and -0.56) raise
   LightGBM's RMSE from 0.145 to 0.157. Alternative: drop the 24 Alloca rows.
8. **Licence (note only):** JSE's policy asks for the author's consent to use the data in published material
   (https://jse.amstat.org/jse_users.htm).
9. **Framework notes (not patched):** (a) the README's feature-type summary calls `_feature_types` on the final frame,
   where text columns are already categories; a dtype-based rule such as `object_columns(df)` therefore reports
   "0 categorical" in the README while the container is right (I use `not is_numeric_dtype`); worth a sentence in the
   template's `_feature_types` comment, or computing the summary from the cleaned frame. (b) Strict discovery: one
   fresh scaffold with `problem_type = "TODO"` (`perth_house_prices`) makes every probe script crash for every dataset,
   since they all call `discover_datasets(root)`; the probes could load the named folder directly.

**Verification:** (independent verifier, 2026-10-07: "ready with noted concerns"; each finding second-checked on the
data before acting)
1. major, outliers: **applied.** `_clean` drops `(Gr Liv Area > 4000) & (Sale Condition == "Partial")` (assert: 3
   rows), Decision 3 and the bullet rewritten. Second check: the 3 Edwards rows sell at $28.4-$39.5 per sq ft against a
   median of $149.8 for partial sales; after the drop the task probe's linear RMSE falls from 0.133 to 0.124.
2. minor, source switch: **applied** in issue 1 (JSE file and DOI for `source_links`, the folder name). Re-checked:
   OpenML 42563 and 42165 each have 1,460 rows that match De Cock rows in every feature and the price.
3. minor, `ames_housing_dataset`: **applied** (record comment). Second check: the Kaggle mirror
   `shashanknecrothapa/ames-housing-dataset` (`AmesHousing.csv`, 2023-06-20) equals AmesHousing.txt in 240,260 of
   240,260 cells; the copy was deleted after the check.
4. minor, records at the sale: **applied** (bullet rewritten). Second check, after the July cut: 0 of 2,587 houses built
   two or more years before their sale have a remodel year after the sale year; 1.6-5.3% per sale year have one in the
   year before (2007: 31 of 581). After the outlier drop one Partial new home (remodel 2008, sold 2007) is the only
   date after a sale.
5. minor, sale columns and gap: **applied, with a change of framing.** Instead of keeping "at the agreement" and
   explaining the missing gap, the prediction point is now "a house sells" (house_sales, zillow_prize), which matches
   the closing-month time stamps, so no gap is due; `splits_comment` gives the gap numbers for an agreement-time model.
   Re-run on the new rows: 1-month gap +0.0006 (SE 0.0010), 2-month +0.0026 (SE 0.0013); dropping Sale Condition
   +0.0047 (SE 0.0008, 13 of 13).
6. minor, Alloca and AdjLand blocks: **applied** (bullet, issue 7). Second check: 24 Alloca rows in 13 month-and-block
   groups (16 rows in blocks of 2+), 12 AdjLand rows in 7; window-0 RMSE with and without the two Alloca rows
   recomputed on the new rows: 0.157 vs 0.145.
7. minor, `Year Remod/Add` floor: **applied** (bullet; values kept). Second check: 359 rows at 1950 against 14-20 in
   each of 1951-1953; 337 of 629 pre-1950 houses show 1950.
8. minor, June 2010: **applied** (issue 6 numbers). Second check: June mean log price 11.985/12.077/12.064/12.047/11.931
   for 2006-2010, May 2010 12.009.
9. minor, Trivial numbers: **applied** (issue 3, bullet, record comment), recomputed after the outlier drop: per-grade
   mean RMSE 0.2275 against 0.1186 for a 500-tree LightGBM, better in 0 of 13 windows; De Cock's two-variable OLS
   R² 0.766 against 0.912, never better.
10. procedural, `v2_path`: not mine to change (records are read-only for me; `sync-notebooks` is the orchestrator's).

### house_sales
**Outcome:** added and checked (revised 2026-10-07 after verification: house features rebuilt as of each sale, 9 three-week windows)
**Record judgment:** valid with concerns. Provenance is traced. The source file's house features were recorded after the sales; the definition now rebuilds them as of each sale. The newest month is truncated and is dropped.
**Data:** three raw inputs under `local-data-warehouse/house_sales/`, about 1.9 GB in total.
- Kaggle `harlfoxem/housesalesprediction`, `kc_house_data.csv` (md5 b1e7bdf4f3e61792c0979a5697dc7145): 21,613 rows x 21 columns, sales 2014-05-02 to 2015-05-27. Licence CC0 1.0 (Kaggle API metadata; OpenML 42731 "CC0 Public Domain").
- King County Department of Assessments extracts from https://info.kingcounty.gov/assessor/DataDownload/default.aspx:
  - `Change History Detail.zip`: 1,836,988,142 bytes, member `EXTR_ChangeHistDetail_V.csv` of 6.07 GB, `unzip -t` OK.
  - `Residential Building.zip`: 21,728,325 bytes.
- `_prepare_raw_files` filters these once, in 1 min 51 s with 1 GB RAM, to:
  - `house_sales_changes.csv`: 53,321 changes of 12 attributes of the file's parcels, 2014-01 to 2026-10.
  - `house_sales_bath_counts.csv`: 21,283 parcels.
- Provenance:
  - The rows are the assessor's recorded sales: 21,386 of 21,613 match on parcel, date and price.
  - The file holds 84.8% of the county's 24,273 comparable sales (96% of those without a warning, 46% with one), and none of the 63 sales below $75,000.
  - The table was first distributed with the UW Coursera ML Specialization (2015). Its file `course-2/kc_house_data.gl.zip` on github.com/learnml/machine-learning-specialization holds the Kaggle CSV cell for cell.
- Uniqueness: no other King County data in the records or the working copy.

**Definition:** `datasets/_dev/tabarena-v0pt2/house_sales/`, 20,967 rows x 19 features.
- Prediction point: a house sells. Predict its price from the assessor's record of the house on the sale day and its location, with a model trained on all earlier sales.
- Target and metric: `log_price` (log of the price), RMSE.
- Splits: temporal on `date`, `TemporalSplits(window=3, unit="weeks", n_windows=9, min_train_fraction=0.5)`. That gives 9 windows from 10-30 Apr 2015 back to 24 Oct-13 Nov 2014, with 659-1,565 test and 11,253-19,402 train rows; the oldest window trains on 54%.
- Cleaning:
  - Drop May 2015 (646 rows).
  - Rebuild the house features as of each sale: 2,151 rows changed in total. `bathrooms` is rebuilt for 913 rows and kept for 5. `view`, `waterfront` and the neighbour areas stay as in the file.
  - Drop `id`.
  - 0 -> missing for `yr_renovated`, `bedrooms` and `bathrooms`.
  - `zipcode` is categorical; tag `Spatial`.
  - Keep repeated sales.
- `source = "Other"`, `year = "2015"`; `source_url` is the course folder on GitHub. The BibTeX cites the Kaggle upload and names the course in its note.

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info.
- The info is `dataset_conflicting_duplicate_rows`: two identical townhouses sold the same day for $367,899 and $369,946. Noted, not accepted as a warning.
- Checksum v2:5fc9fc3c..., the same under pandas 2.3.3 and 3.0.6.
- ruff is clean and no TODO is left.
- `DATA_FOUNDRY_V2_DATA_CHECKS=1 pytest -q tests/test_v2_datasets.py -k house_sales`: 2 passed.

**Probes:** all run with `--n-jobs 2` and thread caps.
- Task (5 of 9 windows):
  - LightGBM R^2 0.883, beating the dummy on 100% of splits (SE 0.006).
  - Random forest 0.863, linear 0.737, best single feature (`grade`, all 5 splits) 0.460, dummy 0.000, drift 0.002.
  - No flags.
- Generated: exact fit 1.3% against 1.3% on a shuffled target; no flags.
- Leak (3 newest windows):
  - All features R^2 0.885; depth-2/3 tree 0.532/0.645.
  - Best single features: `zipcode` 0.538, `grade` 0.451, `sqft_living` 0.440. Dropping any one of them costs at most 0.006.
  - Missing-value indicators: R^2 at most 0.002.
  - 1.8% of test rows have an exact feature copy in train; these are resales.
  - 1-NN R^2 0.725 for the closest tenth against 0.703 for all rows.
  - No leak signal, but these probes cannot see post-sale values inside ordinary columns. The verifier's change-log test can, and it led to the rebuild.
- Hidden groups: `hidden_groups.py` skips temporal tasks. Resales were checked by hand: 5-30 test rows per window, predicted worse than the rest (RMSE 0.36 against 0.17, under-predicted by 0.30).

**Issues for Lennart:**
1. **Post-sale record values.** The source file's house features are the assessor's record as of 18-19 July 2015.
   - Of the first changes in the 30 days after that date, 98.7% have the file's value as their old value; of the changes in the 30 days before it, 23.5% do.
   - For 2,151 of 20,967 rows the record changed after the sale, mostly upward, a median 112 days after it. Changes are 2.5-3.5 times as frequent after a sale as before it.
   - Effect, LightGBM with 3 seeds on the 9 windows: RMSE on those rows 0.156 with the file's values against 0.208 with the record at the sale. On all rows: 0.1727 against 0.1761, worse in 8 of 9 windows.
   - Implemented: rebuild from the county's change log (option a). This adds a 1.8 GB raw download that the county updates weekly; the 2014-2015 events it reads do not change.
   - Alternatives: (b) drop the 1,957 rows with a rebuilt main column; (c) keep the file's values with a `Potential leak, kept on purpose:` bullet.
2. **Window length.** Implemented: 9 three-week windows, the convention's 3 x 3, with 659-1,565 rows each. Alternative: 6 calendar months (a monthly refit; 978-2,231 rows).
3. **Source and year.** Implemented per this run's convention: `source = "Other"` (the Coursera course), `year = "2015"`. The record says Kaggle and 2016; the BibTeX still cites the Kaggle upload. Lennart's call.
4. **Parts of the post-sale record left in place.**
   - `view` and `waterfront`: 154 rows had a view or waterfront attribute changed, and the file's 0-4 view index is not a county attribute.
   - `sqft_living15` / `sqft_lot15`: the neighbours' areas in July 2015.
   - 5 rows whose bathroom history does not add up, and 10 blank old values.
5. **Records at the sale with placeholder values.** 6 houses under construction show a living area of 8-200 sq ft at their sale. Kept as the record stood; the alternative is to set them to missing.
6. **May 2015 dropped** (646 rows; extract cut mid-month). Alternative: keep it as a short window.
7. **Repeated sales kept.** Alternative: the latest sale per house, as in california_house_prices_2020.
8. The record's `v2_path` is unset (`sync-notebooks` is not run in this batch).

**Verification:**
1. Blocker (post-sale values): applied, option (a).
   - I downloaded the change log in full (resumed with `curl -C -`; `unzip -t` OK) and reproduced the snapshot date.
   - `dataset.py` rebuilds grade, condition, living area, basement, bedrooms, floors, `yr_built`, `yr_renovated`, `sqft_lot`, bathrooms and `sqft_above` as of each sale.
   - The Anomaly bullet is corrected. Resales stay "harder, not easier" (the numbers hold after the rebuild); "cannot be checked" is gone.
   - The 33-bedroom row now carries its record at the sale (2 bedrooms, 1,340 sq ft), so the earlier 33 -> 3 fix is removed.
2. Windows: applied. 9 three-week windows replace 6 monthly ones, per the split-count convention, since every window holds over 50 rows. Monthly is listed as issue 2.
3. Coursera copy: applied. The "HTTP 403 ... the copy we can get" sentence is replaced by the GitHub course file. `source = "Other"`, `year = "2015"` per this run's convention (issue 3).
4. Cohort: applied and reproduced in `curation_comments`: 84.8% of 24,273 comparable sales, 96% without a warning, 46% with one, none of the 63 below $75,000.
5. Corrections: applied.
   - The snapshot is dated 18-19 July 2015.
   - The 12 rows with `yr_built` after the sale year are noted (5 after the rebuild; 24 `yr_built` values rebuilt, mostly teardowns).
   - The 1,225 kept rows with warning 26 are over-predicted by 0.08-0.09 with either feature set and kept as noise. The verifier's 1,281 counted all matched rows.
6. Record pointer: open (issue 8).

### huntprohibited
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/huntprohibited_1m/`, `version_of = "huntprohibited"`)

**Record judgment:** valid with concerns. The source is clear: the Kaggle competition "The Hunt for Prohibited Content" (Avito, 2014), a binary moderation task ("learn from moderators' answers how to classify if an ad contains illicit content or not", Description page). No Avito data is in the working copy; the only other Avito record, `avito_context_ad_clicks`, is a CTR task already marked `No`, and no record of this run shares the source. The concerns are the ones the record names, now with numbers: the text carries most of the signal (Russian), the temporal split the record asks for cannot be built, and the seller structure cannot be grouped (issues 1, 2, 4).

**Data:** Kaggle competition `avito-prohibited-content`, file `avito_train.zip` (772,619,211 bytes, sha256 `aa5472aa91d2fda10e9e79c9ca69c28dfa9e2155b9eefe2557dcaafba771a23b`; holds `avito_train.tsv`, 3.13 GB), downloaded with kaggle CLI 2.2.2 into `local-data-warehouse/huntprohibited/` and read from the zip as it is. 3,995,803 rows x 13 columns (December 2013 to March 2014). The test file (1,351,242 unlabelled ads, April 2014) was downloaded to the scratch folder for an id check only and deleted. Licence: Kaggle Competition Rules; the rules page says "Participants must use the Data solely for the purpose and duration of the Competition" and forbids redistribution (noted, not a verdict reason).

**Definition:** `huntprohibited_1m`. Prediction point: an ad is scored when it is submitted (new or edited) and enters moderation, from its content as posted. Target `is_blocked` (Yes 6.9%), metric ROC AUC (the competition scored AP@32500). Regime IID with the tag `ForcedIIDFromTemporal`; 3,963,488 ads after dropping duplicates, sub-sampled to 1.5M (stratified), 1 x 3 folds of 1M train / 500k test. 9 features: `category` (10 values) and `subcategory` (53) categorical; `title`, `description`, `attrs` (JSON text) string; `price`, `phones_cnt`, `emails_cnt`, `urls_cnt` numeric. Cleaning: drop `close_hours` (time the ad was live, post-outcome; the host: "not available at scoring phase", exported modulo 24 h), `is_proved` (set only for blocked ads), `itemid` (random ids, competition admin in discussion 9554); drop 32,103 exact copies (features and label) and all 212 ads of the 106 feature vectors that occur with both labels. Three `_decisions` tables show the evidence (leak columns by label, ids by decile, duplicates). The cohort is the source's (only ads blocked for illicit content or never blocked, all closed; `price` is the final price), kept as is.

**Checks:** `dataset check`: 0 errors; its one warning, `dataset_pure_feature_value` (real-estate category and subcategories, children's clothes: 99.8-99.9% not blocked), is accepted. Reason: the seller picks the category when posting, real estate is blocked at 0.12% of 1,149,136 ads; a category effect known at the prediction point; the winners left real estate out of training for this reason (discussion 10178). Final run after the verification edits (comments only, so the frame and splits are unchanged; the checksum covers the metadata): 0 errors, 0 warnings, 1 accepted; checksum `v2:01e23fe30d64d119e370586f6827ae0357792d18ff398388390f97f02af2c9bf`, the same under pandas 2.3.3 (repo venv) and pandas 3.0.6 (shared `venvs/pd3`; earlier, the raw, cleaned and sampled frames and the split indices also hashed the same). `ruff check` and `ruff format` clean, the class imports, `pytest tests/test_v2_datasets.py -k huntprohibited_1m`: 1 passed, 1 skipped (the opt-in data check). No `TODO` left.

**Probes:** (at 2 threads, through a private `--root` in the scratch folder holding a link to this folder only, because another agent's half-written `open_university_learning_analytics_dataset` broke `discover_datasets` on the shared root; outputs in `probes/`, own scripts `modality.py`, `copies_on_splits.py`, `dups.py`, which read `train.parquet` written by `load.py`)
- Leak probes (string columns left out by the script; 3 splits, 50k a side): six structured columns ROC AUC 0.924; subcategory alone 0.908, category 0.868, price 0.74, counts 0.50-0.51; depth-2/3 tree 0.830/0.852; no missing-value indicator (only text columns have missing values; `attrs` is missing for every ad of the nine category-subcategory pairs without a form, eight names, and for 98 other ads). "Exact feature copy in train 85%" and 1-NN agreement 0.911 (chance 0.872) are on the six coarse columns only, without the text, so they say nothing about copies.
- Text copies across the split (like for like, corrected after verification): with fold-0 train (1M ads) as the reference for both, 1.39% of the shipped test ads share a 30+ character description with a train ad, against 0.50% of the deduplicated April ads (first 60 normalised characters: 6.39% against 3.64%; title and description: 0.22% against 0.13%); 99.4-99.5% of the copies carry the train copy's label. So the random split does add copies, two to three times the temporal rate, but dropping them moves fold-0 ROC AUC by at most 0.002 (TF-IDF LR 0.9944 to 0.9940, structured LightGBM 0.9324 to 0.9302).
- Task probes (text as TF-IDF + 16 SVD components per column): LightGBM ROC AUC 0.970, random forest 0.970, linear 0.929, best single column (`attrs`) 0.945, dummy 0.500; LightGBM beats the dummy on 3 of 3 splits (SE 0.001); smallest class per test fold 3,399 ads. No flags.
- Generated-data probe: rule leaves cover 0.0% of the minority rows; no flags.
- Hidden-group probe: hits on `subcategory` (random-split skill 0.868, held-out values 0.052) and `attrs` (0.883 against 0.633); `title` eligible but no hit (gap 0.011). Answered: both hits are features every new ad has (a subcategory from a fixed list of 53, form fields from the same dropdowns), not entities that new data would lack (task_probes.md precedents: covertype `Soil_Type`, mutual_funds_india `sub_category`); the split stays IID.
- Own modality check (stratified 400k sample, 3-fold CV): LightGBM on the structured columns ROC AUC 0.929 (average precision 0.50); category and subcategory only 0.909; logistic regression on TF-IDF uni- and bigrams of title, description and attrs 0.992 (AP 0.93); with one-hot category 0.992; LightGBM on the structured columns plus the out-of-fold text score 0.992 (AP 0.94). The verifier's equal-fold numbers (fold 0, 1M train / 500k test) are the ones in the definition: structured LightGBM 0.9324 (AP 0.511), LightGBM on structured plus 32 TF-IDF SVD dims per text column 0.9870 (AP 0.893), TF-IDF LR 0.9944 (AP 0.950).

**Issues for Lennart:**
1. **Temporal split asked for, no time index available.** The record says `required_split: Temporal (NON-IID), ?` and tags `Non-IID (Temporal)`. The data page: training ads "sampled from Dec 2013 - Mar 2014", test ads "from Apr 2014"; but the file has no date, and the host wrote "The ids have been randomly assigned" (discussion 9554). Checked: block rate (6.81-6.93%), real-estate share and seasonal words ("новый год", "8 марта") are flat over the ten id deciles (README decision 2), and the April ids fill every train-id decile at 10.0% with no shared id; the verifier adds that the id-sorted file has a next-row label match of 0.8718, equal to chance (0.8718), and that block rate and seasonal words are flat over 100 position bins (lag-1 autocorrelation -0.09 to 0.16). Implemented: IID splits with `ForcedIIDFromTemporal` (as aps_failure, forest_fires, labour_inspection_compliance). Alternative: none from the released files (test labels were never published). Question: keep the forced-IID version, or drop it because the source task is temporal? If kept, the record's split fields should say IID.
2. **Text carries most of the signal (criterion 4A, the record's own concern).** Data page: "Data for this competition consists mainly of Russian text." On the same fold (fold 0, 1M train / 500k test): structured columns alone ROC AUC 0.9324 (AP 0.511); LightGBM on structured plus 32 TF-IDF SVD dims per text column 0.9870 (AP 0.893); TF-IDF logistic regression 0.9944 (AP 0.950). The TabArena default pipeline gives models each text column as a 32-dim Qwen3-Embedding-8B vector with n-grams off (tabarena `text_cache.py` `SEMANTIC_EMBEDDING`, `model_agnostic_default_preprocessing.py` `enable_text_ngram_features=False`), so the text cache must embed about 2.67M distinct strings (titles 739k, descriptions 1.45M, attrs 479k). A bag-of-words linear model suffices (the 2014 winners used SGD/SVM on TF-IDF plus a random forest over category, subcategory and counts), so no deep text model is required, but the benchmark ranks pipelines by how they encode Russian text. Implemented: kept, text as string columns (precedents in the copy: emscad, consumer_complaints_1m, mercari_price_suggestion). Alternative: exclude under 4A. My view: keep, as the record decided.
3. **`attrs` kept as one JSON string.** It is the category's form (79 keys, 1-12 per ad; 72 keys on at least 1,000 ads; 6,004 strings malformed: quotes written as `/"`, tabs). 735,975 ads, all real estate, repeat a key: 735,772 give `Этаж` and `Этажей в доме` twice (a range or class and the exact value); json.loads keeps the later value, which is the exact floor in 550,009 and the range in 185,763 of them, so an unpacking needs a rule (both values, or the exact one). It is the strongest single column in the task probes (ROC AUC 0.945). Implemented: string column, parsing left to the pipelines (the winners treated it as text). Alternative: unpack into up to 72 sparse categorical/numeric columns with Russian keys (kickstarter decodes its JSON fields), using the host's regex fix (discussion 9677) and a rule for repeated keys. Question: which do you prefer?
4. **Sellers ("malicious users" in the CC comment).** The file has no seller id, and phones, e-mails and URLs are masked without a hash, so ads cannot be grouped by seller exactly (no similarity clusters, per the guidelines). Exact copies are dropped (32,103 plus 212 conflicting ads). Edited reposts stay: 128,355 of the 3,963,488 kept ads share a 30+ character description with another ad (10.2% blocked against 6.9%); like for like (fold-0 train as the reference), 1.39% of the shipped test ads have such a copy in train, against 0.50% of the deduplicated April ads (99.4% label agreement), so the random split adds copies, but they move fold-0 ROC AUC by at most 0.002. Implemented: IID with exact deduplication. Alternative: group by exact description text (an exact key, as emscad's identical profile text); the 0.002 above bounds what it would change. Question: does the "detect users, not ads" remark need more than this?
5. **Hidden-group hits dismissed.** `subcategory` (gap 0.816) and `attrs` (gap 0.250) are attributes every new ad has; holding their values out measures generalisation to unseen categories or form values, not entity memorisation. Implemented: no re-split. Question: agree?
6. **`is_proved` as an alternative label** (the CC comment: it "could be used to sub-filter data"). 83,810 of 274,996 blocked ads were blocked by an experienced moderator. Implemented: `is_proved` dropped, target `is_blocked` as in the competition. Alternative: positives = proved blocks only, dropping the 191,186 unproved blocked ads (cleaner label, not the source's target). Recommendation: keep `is_blocked`.
7. **Real estate kept.** 1,149,136 ads (28.8%), 0.12% blocked; the winners left them out of training (discussion 10178). They are easy negatives that lift ROC AUC (subcategory alone 0.908). Verifier, fold 0: without the real-estate test ads (28.4% of them, 186 positives) text LR 0.9944 to 0.9925 (AP 0.950 to 0.951), structured LightGBM 0.9324 to 0.9071 (AP 0.511 to 0.514). Implemented: kept, since moderation covers every ad. Alternative: drop the category (2.8M ads remain, still a `_1m` version).
8. **Licence and content.** Kaggle Competition Rules: use limited to the competition, no redistribution. The ads include illicit or offensive content (rules page warning), and dating ads carry first names and ages (Avito masked phones, e-mails and URLs). Noted, not a verdict reason.
9. **`Spatial` tag?** `attrs` holds a free-text address ("Адрес": a street, sometimes the town) for 901,011 ads (22.5%), all real estate. Implemented: no `Spatial` tag (no region or coordinates). Alternative: add the tag. Your call.

**Verification (independent verifier, 2026-10-07: ready with noted concerns):**
- Finding 1 (copies claim not like for like): applied. The comment and issue 4 now give the fold-0 like-for-like numbers (1.39% against 0.50%; first 60 characters 6.39% against 3.64%) and the at most 0.002 effect; IID with exact deduplication stays.
- Finding 2 (text evidence from unequal runs): applied. The text bullet and issue 2 give the fold-0 numbers (0.9324 / 0.9870 / 0.9944) and the harness's 32-dim Qwen3-Embedding-8B text input (checked in the tabarena code). 4A stays Lennart's call.
- Finding 3 (cohort): applied as a new bullet quoting the data page; kept as the source's cohort.
- Finding 4 (wording): applied. 735,975 ads with a repeated key (recounted: all real estate, json.loads keeps the later value), the quote is by joycenv, the competition admin (author of the Timeline and External Data threads; Ivan Guz is the Avito host), and "nine category-subcategory pairs, eight names". The address goes to issue 9 (recounted: 901,011 ads, all real estate; some include the town).
- Finding 5 (temporal, Lennart's call): no change; the verifier's numbers are in issue 1 and the next-row match in the comment. The record's split fields should say IID if it ships.
- Finding 6 (real estate, Lennart's call): no change; the numbers are in issue 7.
- Finding 7 (record pointer): pending. `v2_path` is unset until `sync-notebooks` runs, which this brief does not allow me to run.

### lgd
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/lgd/`), then fixed after verification.

**Record judgment:** valid with concerns.
- The source is traceable. The data page of the book Credit Risk Analytics
  (http://www.creditriskanalytics.net/datasets-private2.html) describes it, and so does the book's chapter 1, which we
  read in the publisher's excerpt (https://www.sas.com/storefront/aux/en/spcriskmdl/68835_excerpt.pdf).
  - Chapter 1, p. 14: "The data set has been kindly provided by a European bank and has been slightly modified and
    anonymized. It includes 2,545 observations on loans and LGDs."
  - Exhibit 1.4 (p. 12) files it under the risk segment "Corporate", for chapter 10, "Loss Given Default (LGD) and
    Recovery Rates" (pp. 271-313).
- It is not a duplicate: no other record and no working-copy folder holds LGD data.
- No re-upload turned up on OpenML (all 24,406 dataset names searched) or Kaggle (searched for "lgd", "loss given
  default" and "credit risk analytics"). The only copy found is dpicone1's GitHub transcription of the R Companion,
  whose lgd.csv has the same sha256.
- Concerns: only two features, the record's problem type and split, and the undocumented modifications (issues 1-5).

**Data:** lgd.csv from the book's site (sha256 2e3f964a...e07e), 2,545 rows x 8 columns.
- lgd.sas7bdat holds the same rows in the same order at full precision; the csv rounds to 10 decimals.
- The download is pinned to a Wayback Machine copy of 2017-09-27 with the same sha256.
- Licence: the download form at http://www.creditriskanalytics.net/datasets.html says "I agree to use the data only in
  conjuction with the Credit Risk Analytics textbooks [...] Commercial use is prohibited."
- The site's terms (http://www.creditriskanalytics.net/terms.html) add "You must not: Republish material from Credit
  Risk Analytics [...] Redistribute content from Credit Risk Analytics". Both are noted in `license`, never a verdict
  reason.
- The data link needs no login.

**Definition:**
- Folder: `datasets/_dev/tabarena-v0pt2/lgd/`.
- Prediction point: a loan has just defaulted, and the bank estimates the share of the exposure it will lose. LTV
  and the loan purpose are known then.
- Target: `lgd` (the source's `lgd_time`, a share from 0 to 1) as regression with RMSE. The data keeps the source's
  bounds: 0.00001 for no loss (728 rows) and 0.99999 for a total loss (143 rows).
- Features: `loan_to_value` and `purpose_renting`, so 2,545 rows x 2 features.
- Dropped: `Recovery_rate`, `y_logistic`, `lnrr` and `Y_probit` (transformations of the target), and `event`, which
  is 0 for exactly the 728 rows at the floor.
- Regime: grouped. `Grouping(on="borrower_block", labels="per_sample", prediction_unit="row", context="none")`, on
  1,958 groups, with the default 10 x 3 splits (train 1,669-1,719 rows, test 826-876).
- How the group is built: `borrower_block` numbers the runs of consecutive rows with one LTV value. Within a run the
  values match in all 16 digits of the SAS file, and no LTV value occurs outside its run. The key therefore equals
  the LTV value. It is justified by the consecutive blocks in the file's order (the in_vehicle precedent), not by
  hashing a feature.
- Duplicates: 120 exact copies (103 at the floor, 16 at the cap, 1 pair inside), kept, because they are loans of one
  run.
- pandas 2.3.3 and 3.0.6 give the same checksum (v2:02d1ec3f...).

**Checks:**
- `dataset check`: 0 errors, 0 warnings, and two accepted warnings, each with its reason:
  - `dataset_duplicate_rows`: 120 rows. 103 are loans of one borrower block that all cured and 16 that were all
    lost. The other one is a pair with the same partial loss (0.0109972412). The grouped split keeps them on one side.
  - `dataset_conflicting_duplicate_rows`: 397 rows. With two features, one borrower's loans share LTV and purpose but
    not their losses.
- `pytest tests/test_v2_datasets.py -k lgd` passes, including the run with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- ruff is clean, and the import check passes.

**Probes:** the probes found other agents' TODO scaffolds and failed on them (`perth_house_prices`), so I ran them
through a private `--root` that holds a symlink to this folder.
- Task probes, 30 grouped splits: linear skill +0.193 (SE 0.005, above the mean predictor on 100% of the splits),
  LightGBM +0.119, random forest -0.026, single feature +0.069. No flags.
- Leak probes, untuned LightGBM on 3 splits:
  - R^2 0.115 with all features. Depth-2 and depth-3 trees reach 0.168 and 0.174.
  - Each feature alone: `loan_to_value` 0.095, `purpose_renting` 0.014.
  - No test row has an exact copy in train, and the 1-NN R^2 is negative.
- Generated probes: no flag. 0.2% of the rows fit a formula exactly, against 0.3% with a shuffled target; the 34% of
  rows at the bounds are left out.
- Group probes: LightGBM scores 0.147 on an IID split and 0.125 on the grouped one. Across groups: ridge 0.190,
  LightGBM 0.123, 5-NN 0.019, random forest -0.029.
- Hidden groups (on an IID draft): no candidate. The probe only considers integer, categorical and text columns with
  at least 1.5 rows per value. The entity here is a float LTV with 1.30 rows per value, so the gap was measured by
  hand.
- Rule 4 (raw feature against models; fractional logit and tuned LightGBM from the verifier, reproduced from its
  per-split file): raw-LTV isotonic 0.188 ± 0.006, the book's 3-parameter fractional logit 0.204, LightGBM tuned by
  grouped inner CV 0.200, spline 0.208 ± 0.006. Raw LTV beats the spline on 0 of 30 splits, so the task is not
  `Trivial`.
- Checked for HMEQ-style generation artefacts: none found.
  - Runs are not jittered copies: LTV is identical within a run, while purposes and losses vary (70 and 89 of the 488
    runs mix them).
  - Number format does not predict the LGD within LTV deciles (p = 0.74), nor whether there was a loss (p = 0.10).
  - No LGD equals 1 - 1/LTV.

**Issues for Lennart:**
1. **Problem type: the record should say Regression.** The record says Binary Classification. The only binary column
   is `event`, which is 1 exactly when LGD is above the 0.00001 floor, so a binary task would predict loss vs no loss.
   The book's own task is the regression:
   - Ch. 1 p. 4: "The tenth chapter presents marginal loss given default (LGD) models and LGD models that condition
     on the selecting default event".
   - The site's ch. 10 errata (updates.html): "Page 293 - add MODEL lgd_time ~ GENERAL(ll)".
   - The R Companion code fits `lm(lgd_time ~ LTV + purpose1)` plus fractional-logit, beta, Tobit and Heckman models.
   - KU Leuven's CreditICL treats a table with the same column and bounds as an LGD regression.

   The alternative is an `lgd_clf` folder with `event` as the target. On the same splits it scores logistic ROC AUC
   0.706 ± 0.016 and log loss 0.546 against a prior of 0.599. Raw LTV alone gets AUC 0.699, so that version comes
   close to a one-feature task.
2. **Split: the record should say Grouped (NON-IID).** The record says Random (IID). Implemented now: grouped by
   borrower block (runs of identical LTV).
   - The evidence for a block being an entity:
     - LTV is equal in all 16 digits, only inside a consecutive run.
     - 70 of the 488 multi-loan runs mix the two purposes.
     - The LGD's intraclass correlation within runs is 0.50. With LTV and the file-order trend removed, the first
       two loans of a run still correlate at 0.42, against 0.02 between neighbouring runs.
     - The book defines LGD by the "default of an obligor" (ch. 1, p. 10), so a new default does not come with the
       losses of the borrower's other loans.
   - Under a random 3-fold split, 31% of the test rows would share their exact LTV with a train row (27% an exact copy
     of both features). The grouped split leaves none.
   - The gap is negligible for smooth models: spline 0.208 random vs 0.212 grouped, linear 0.192 vs 0.192.
   - Models that memorise exact LTV values gain from a random split: full-depth random forest -0.028 vs -0.138,
     extra trees -0.172 vs -0.240, 5-NN 0.074 vs 0.029, LightGBM 0.156 vs 0.146.
   - The alternative is IID as the record says.
3. **What `event` = 0 means is not settled.** No text we read says that `event` = 0 is a cure.
   - The book's R code treats event 0 as an LGD censored at 0 in its Tobit and as a mass at zero in its censored
     beta. Both support reading it as a cure (a default that ended without loss), which is what the definition says.
   - Its Heckman model treats event 0 as "not selected".
   - If chapter 10 says those loans never defaulted, the 728 rows leave the target: they would not be LGD
     observations.
4. **Only two features**, the same two the book's models use. This is the thinnest dataset in the working copy: the
   next are sepsis_survival_minimal_clinical_records (3 features) and blood_transfusion (4). Rule 4 says the task is
   not `Trivial`, but strong methods will likely tie: the book's 3-parameter fractional logit reaches 0.204, tuned
   LightGBM 0.200 and the spline 0.208. A benchmark on it mostly measures how much a method overfits a
   one-dimensional curve: default CatBoost, LightGBM and XGBoost score 0.135, 0.133 and 0.047. Keep it as a small,
   thin task, as sepsis_survival_minimal_clinical_records was kept, or drop it for lack of features: your call.
5. **"Slightly modified and anonymized"** (ch. 1, p. 14) is not explained, and the chapter-10 text was not read. Ask
   for pp. 271-313 if you have the book. It should say:
   - whether a row is a loan or a default episode, and whether one borrower's loans are listed together;
   - whether `event` = 0 is a cure or a loan that never defaulted;
   - the country and period;
   - whether LTV is taken at origination or at default;
   - whether incomplete workouts are in the data, and whether LGDs were cut at 0 and 1.

   The probes found no HMEQ-style artefacts.
6. **Row order.** The file's order carries the outcome.
   - The median LTV per 100 rows rises from 0.22 to 1.00 over rows 1-2,300, and the mean LGD follows (0.06 to 0.49).
   - The last 234 rows (from row 2,312) look like a second segment: no renting loans, median LTV 0.23, mean LGD
     0.095, against 8%, 0.71 and 0.242 before.
   - The order may be the default date within two portfolios. The file has no dates, so out-of-time validation, the
     standard for LGD models, cannot be built. The base class shuffles the rows.
   - `ForcedIIDFromTemporal` is not set: it is the tag for IID-split temporal data, and this task is grouped with no
     date evidence. The verifier agrees.
7. **Record fields**, if you agree: `problem_type: Regression`, `required_split: Grouped (NON-IID)`. Once the folder
   is committed, `sync-notebooks` fills `v2_path`; I did not run it.
8. **Provenance lead (unverified).** KU Leuven's CreditICL (github.com/andreasgoethals/CreditICL) holds a table
   `0003.axa` (`src/data/dataset_registry.py`), flagged proprietary. Its notes (`docs/AGENTS_MEMORY.md`, 28-09-2026)
   match this file: `lgd_time` squeezed into [1e-5, 1 - 1e-5], 28.8% complete recoveries (we count 732 rows, 28.8%,
   at or below 1e-4), 5.6% total losses, and an absolute maximum of 1.98 (our maximum LTV is 1.98). So the bank may
   be the one in that slug. This is not confirmed, and no bank is named in the definition.
9. **Framework note:**
   - hidden_groups.py cannot see an entity encoded as a repeated float value (LTV here).
   - All probes fail when any agent's scaffold in the root still has `problem_type = "TODO"`. A private root with a
     symlink works around it.

**Verification** (independent verifier, 2026-10-07; report in `verify/verify.md`):
- Verdict: ready with noted concerns. Regression and the grouped split hold up, and every check and number
  reproduces.
- Fixes applied in `dataset.py` (README regenerated, checksum v2:02d1ec3f..., the same under pandas 2.3.3 and 3.0.6):
  1. Evidence for the regression added to the target bullet: ch. 1 p. 4, the ch. 10 errata (p. 293) and CreditICL.
     Evidence for the grouping added to the grouping bullet: residual correlation 0.42 within a run against 0.02
     between neighbouring runs, and 31% of test rows sharing their exact LTV with a train row under a random split.
     The record should say Regression and Grouped (issues 1, 2 and 7).
  2. The `event` bullet now says event 0 is read as a cure, the Tobit and censored beta code support that reading,
     and the Heckman code reads it as "not selected". If ch. 10 says otherwise, the 728 rows leave the target
     (issue 3).
  3. The "Two features only" bullet now has the fractional logit (0.204), the tuned LightGBM (0.200), the spline
     (0.208) and raw LTV (0.188, beating the spline on 0 of 30 splits), plus the thinnest-dataset comparison.
  4. `license` now quotes the site's terms as a note.
  5. `download_description` now has the pinned Wayback copy, which I checked: same sha256.
  6. Wording:
     - "share one collateral value" is now "share one loan-to-value ratio", in the comments, the group definition
       and the decision text;
     - a line now says the key equals the LTV value and is justified by the consecutive blocks;
     - the accepted duplicate reason now names the interior pair (0.0109972412).
  7. The CreditICL `0003.axa` lead is in issue 8 as unverified, with no bank in the definition.
- Also taken from the verifier: the anomaly bullet now names the second segment (the last 234 rows).
- Not taken: the verifier's argument that 323 runs hold two or more losses. It assumes a loan is lost only once, and
  the data cannot show that.

### melbourne_housing_market

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/melbourne_housing_market/`).

**Record judgment:** valid with concerns. The data are Tony Pino's scrape of the weekly auction-result sheets of
Domain.com.au (Kaggle forum thread 53664, 2018-04-03: "Grab the weeks domain pdf file from domain.com ... Using CSV
run python script to get extra data from realestate.com ... vlookup"), first published on Kaggle. Its established use
is sale-price regression: the uploader's own notebook (anthonypino/price-analysis-and-linear-regression) and Kaggle
Learn's machine-learning track ("predicting housing prices from the Melbourne Housing data",
dansbecker/handling-missing-values). No Melbourne data in the working copy; no row overlap with perth_house_prices
(0 shared addresses, disjoint coordinates). The concerns are the issues below.

**Data:** Kaggle anthonypino/melbourne-housing-market (last updated 2018-10-14), both files downloaded to
`local-data-warehouse/melbourne_housing_market/`: Melbourne_housing_FULL.csv (34,857 x 21, md5
06cc531612b8261e0c594c5085e3dc30; used) and MELBOURNE_HOUSE_PRICES_LESS.csv (63,023 x 13, md5
cc467c28044d01770d8784cf287d1b6e; read only for evidence in `_decisions`). Licence CC BY-NC-SA 4.0 (Kaggle dataset
metadata). The data are scraped from Domain.com.au and realestate.com.au.

**Definition:** prediction point: a property is listed for auction; before the auction weekend a model refit every
three weekly sheets on all earlier sales predicts its sale price from the listing and the date; the auction result
(`Method`) is not known then. Target `log_price` (natural log of the sale price in AUD, 112,000 to 7,650,000).
Temporal on `Date` (the auction Saturday of the sheet): `TemporalSplits(window=3, unit="unique", n_windows=9,
min_train_fraction=0.5)`, horizon 3 weeks; 9 windows from 3-17 March 2018 back to 12-26 August 2017, 93-1,550 test
rows, training on 55-95% of the rows. 21,266 rows x 19 features (6 categorical, `Address` text, `Date`, 11 numeric).
Main cleaning: only sales with a price (S, SP, SA; PI and VB prices are bids); `Method` dropped (post-outcome); the
787 rows dated 6 Jan 2018 re-dated to 16 Dec 2017 (a copied sheet); 36 re-reports of one sale dropped (keep the first)
and 3 conflicting pairs dropped; the scraped attributes of the 6 sales whose building was finished after the sale set
to missing; impossible values to missing (`YearBuilt` < 1835, `BuildingArea`/`Bathroom`/`Bedroom2` = 0); spelling
fixes for 3 suburbs and 7 agency spellings (case or punctuation: O'Brien, MJ, Castran, RE, VICPROP); `Type` codes to
words; `SellerG` -> `Agent`, coordinate typos renamed.

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); nothing accepted. pandas 2.3.3 and 3.0.6 give
the same checksum (v2:6e720f71...ff20, equal to the README's). `pytest tests/test_v2_datasets.py -k melbourne`
passes (1 passed, 1 skipped; with `DATA_FOUNDRY_V2_DATA_CHECKS=1` 2 passed). ruff check and format clean.

**Probes:** (run on an isolated root holding only this folder, see issue 11; outputs `probes/*_fix*`)
- Leak (untuned LightGBM, 3 newest windows): all features R² 0.814; best single feature `Postcode` 0.366; missing
  indicators no signal (R² < 0); no drop-one loss (0.814-0.818); shallow trees R² 0.102 (depth 2) and 0.258 (depth 3).
  11.0% of the newest window's test rows have an exact feature copy in train: all are rows without the scraped
  attributes (39% of those; 30-34% in the next two windows), whose log prices differ from the copies' mean by a median
  0.14, so coarse features, not copies of a sale (the verifier: 0 copies once `Address` is included). 1-NN R² 0.421
  in the closest tenth vs 0.714 overall. No flag.
- Task (all 9 windows, untuned): RMSE in log price LightGBM 0.187 (R² 0.826), random forest 0.198, linear 0.275,
  train mean 0.474; LightGBM beats the mean in 9 of 9 windows; best single feature `Postcode` R² 0.378. Flags: none.
- Generated: 3.5% of rows fitted exactly vs 3.5% for a shuffled target; flags: none.
- Hidden-group and group probes: not applicable (temporal task). Repeated entities: 45 addresses resold 63-679 days
  apart, kept as history under the temporal split.
- Side run on the shipped frame and windows (`explore/exp_fix.py`, LightGBM with fixed parameters, output
  `probes/exp_fix.txt`): shipped RMSE 0.1833; + `Method` 0.1834; without the six scraped attributes 0.2048; with the
  LESS columns only 0.2106 (worse in 9 of 9 windows); training from 27 May 2017 only 0.1882 (worse in 8 of 9); outer
  suburbs (> 15 km) 0.1524 shipped vs 0.1519 from-May-only; `Distance` harmonised 0.1829; the 495 mismatching 2016
  lookups blanked 0.1837.

**Issues for Lennart:**
1. Which file. Implemented: Melbourne_housing_FULL.csv (sales Jan 2016 - 17 Mar 2018, with the realestate.com.au
   attributes). Alternative: MELBOURNE_HOUSE_PRICES_LESS.csv (63,023 results to 13 Oct 2018, about 35,500 sales once
   the copies are dropped; 12 columns, no land/building attributes or coordinates; it repeats one holiday sheet on 5
   dates, 4 x 787 copy rows to drop). On the same rows and windows RMSE in log price is 0.183 with the attributes,
   0.205 without the six scraped attributes and 0.211 with the LESS columns (9 of 9 windows worse); LESS would add 7
   months and the outer suburbs before May 2017.
2. Target is the sale price only. PI (passed in) and VB (vendor bid) rows carry the highest or the vendor's bid (data
   card: "N/A - price or highest bid not available"): against LightGBM fitted on each window's training side they lie
   a median 4.3% (PI) and 6.6% (VB) below the predicted sale price, the sales 0.1% above (the verifier's run: 4.0%,
   7.0%, 0.0%); the two "unexpectedly low" prices of thread 308935 (131,000 and 145,000) are PI rows of homes that
   sold for 1,350,000 and 1,520,000. Implemented: drop PI/VB (5,939 rows with a price). Alternative: a "price or
   highest bid" target with `Method` as a feature (27,247 rows), which mixes two quantities and uses a post-auction
   field.
3. The scraped attributes are a lookup made after the sale (the King County lesson); keeping them is supported by the
   data. `Bedroom2` (lookup) equals the sheet's `Rooms` in 98.9-100% of the rows of each test window and 98.1-99.8%
   per quarter from Oct 2016, against 85.2% of the 3,107 sales of Apr-Sep 2016 that were looked up in April 2017. The
   dansbecker snapshot ("created in September 2017") holds the final values for its 3,290 sales of 1 Jul - 23 Sep
   2017, and the 18,396-row copy ganjedi/melbourne-housing-snapshot (same newest sale) for 5,253 of the 5,254 priced
   FULL results of those weeks: the mid-2017 lookups were made within weeks. Six 2016 sales show a construction year
   of 2017-2018 (a later building): their six scraped attributes are set to missing. Lennart's call (verifier F1):
   also blank the scraped block of the 495 sales of 2016 whose `Bedroom2` differs from `Rooms`. The verifier measured
   RMSE 0.1843 -> 0.1836 (lower in 8 of 9 windows); my re-run after the agency merge gives 0.1833 -> 0.1837 (lower in
   1 of 9), so the effect is within run-to-run noise. Implemented: keep them.
4. Coverage changes on 27 May 2017 (closed with numbers, verifier F2). Before, FULL holds only the inner suburbs (of
   the LESS sheets it has: all within 10 km of the CBD, 66% at 10-15 km, 2% at 15-20 km, none farther; it lacks the
   sheet of 1 April 2017); from then on every result. The same date switches the uploader's `Distance` table (140 of
   the 142 suburbs present in both periods get a new value, e.g. Airport West 13.5 -> 10.4 km) and the coordinate
   precision. All 9 test windows lie after the switch. Training only on sales from 27 May 2017: RMSE 0.1882 vs 0.1833
   (worse in 8 of 9; verifier 0.1874 vs 0.1843), outer suburbs 0.1519 vs 0.1524 (verifier 0.1517 vs 0.1521).
   Harmonising `Distance`: -0.0004 (verifier +0.0001). Implemented: keep all rows and values as recorded.
5. Windows. Implemented: 9 windows of 3 weekly sheets (unit="unique", horizon 3 weeks, like house_sales' 3-week
   windows), 93-1,550 test rows; the January lull (9 sales on each of 20 and 27 Jan 2018) sits in one window of 93
   sales. Both files lack the sheets of 10 Jun, 5 Aug, 2 Dec 2017 and 13 Jan 2018 (verifier), so a window can span 4
   calendar weeks; the 3-week horizon is nominal. Alternatives (decision table in the README): 4 sheets per window
   (620-1,717 rows, but 2 of 9 windows train on less than half of the rows), 4 calendar weeks (one window of 9 sales),
   calendar months (8 windows, one of 18 sales).
6. Re-dated sheet. The 787 FULL rows dated 6 Jan 2018 are the sheet of 16 Dec 2017: LESS holds the same 787 rows on
   16, 23, 30 Dec 2017 and 6, 8 Jan 2018. Implemented: date them 16 Dec 2017 (constant mapping, asserted count).
   Alternative: keep the file's date. The windows stay the same (the sheet lies between 9 Dec and 20 Jan either way);
   only the date of its 480 sales moves by three weeks, which matters for calendar windows.
7. Records (verifier F7).
   - `melbourne_housing_snapshot` (TBD -> 2nd Tier) is the same data: all 13,580 rows of
     dansbecker/melbourne-housing-snapshot match a FULL row on suburb, address, date, method, agent, rooms, type and
     price, with identical scraped values; its 18,396-row cut (Kaggle re-upload ganjedi/melbourne-housing-snapshot,
     newest sale 23 Sep 2017) has 18,395 of its rows in FULL. Proposal: `No` + `Duplicate` (renamed
     `melbourne_housing_market_duplicate` by the convention).
   - Kaggle InClass competition "vitticeps" (thread 53664, visnut, 2018-04-10: "more years of data, extracted from
     pdf files ... We did not scrape the bedrooms etc data, ours are simulated") is a second extraction of the same
     Domain sheets with simulated attributes. It has no record; if it is ever proposed, it is out (simulated
     attributes) and overlaps this dataset.
   - `source_links` of this record include tylerx/melbourne-airbnb-open-data and insideairbnb.com, a different
     dataset with its own record (`melbourne_airbnb_open_data`, No). Proposal: remove them.
8. Repeated reports. Same address within 60 days: same price = one sale reported again (36 rows, 0-35 days apart,
   first report kept); different price = conflicting (3 addresses, 4-35 days apart, both reports dropped). Nine of
   the 45 kept resales are 63-126 days apart, eight within 11% of the first price, possibly corrected re-reports.
   Alternative: treat repeats within 6 months by the same agent as one sale.
9. Year (verifier F6, Lennart's call). Implemented `year = "2018"`: the Kaggle dataset's last update (2018-10-14) and
   the version used. The dataset was public by 27 March 2017 (thread 30748, the first forum post), and house_sales
   uses the year of first distribution; with that convention it is "2017". Part of the open year-convention question.
10. Licence: CC BY-NC-SA 4.0 (Kaggle page), noted; the data are scraped from Domain.com.au and realestate.com.au
    (an unanswered forum question asks whether Domain allows it, thread 53664).
11. Framework/workflow: at my first probe run, `discover_datasets` over the working copy crashed on
    `perth_house_prices` (another agent's scaffold with `problem_type = "TODO"`); I ran the probes with `--root`
    pointing at `_scratch_new65/melbourne_housing_market/root/` (a symlink to my folder only). By the end, pytest
    collection and `dataset list` worked again.

#### Verification (fix round, 2026-10-07)

The verifier's verdict: ready with noted concerns, no blocker, 7 minor findings (`verify/verify.md`). What I did:

- F1 (scraped attributes): applied. The `curation_comments` bullet now gives the `Bedroom2`/`Rooms` agreement per
  period and the snapshot timing instead of "a lag the source does not document"; the record comment carries the
  numbers. Correction: the 5,253-of-5,254 count comes from the 18,396-row ganjedi copy; the dansbecker snapshot holds
  3,290 of those results (all with the final values), and the bullet says so. Blanking the 495 mismatching 2016
  lookups: Lennart's call, issue 3 (no effect beyond noise in my re-run).
- F2 (coverage): applied; the numbers are in the coverage bullet and issue 4; rows and values kept.
- F3 (bid gap): applied. Re-run with the current definition (short `Type` labels, merged agencies): PI 4.3% and VB
  6.6% below, the sales 0.1% above; the bullet and the decision text carry these numbers.
- F4 (wording): applied: "140 of the 142 suburbs that occur in both periods"; the three "(verification run,
  2026-10-07)" labels are replaced by a description of the side run (LightGBM with fixed parameters on the shipped
  windows). All RMSE figures in the comments now come from one run on the final definition (`explore/exp_fix.py`).
- F5 (agencies): applied. `AGENT_SPELLING` maps "Obrien" and "OBrien" to "O'Brien" (190 sales in the final frame) and
  "M.J" to "MJ" (7); the bullet says "case or punctuation". The data changed (302 agencies), so I re-ran
  `dataset check` (clean), the three probes (leak R² 0.814, task R² 0.826, generated 3.5% vs 3.5%; no flags), the
  pandas-3 checksum (identical, v2:6e720f71...ff20), ruff and pytest (pass).
- F6 (year): kept "2018"; Lennart's call, issue 9.
- F7 (records): issue 7 (snapshot duplicate including the 18,396-row cut; vitticeps).
- Item 14 (record pointer, cannot-verify): pending `sync-notebooks` and the curator's build.

### mobile_churn
**Outcome:** added and checked. Folder `datasets/_dev/tabarena-v0pt2/mobile_churn/`. Revised in the fix round: the
accounts never activated are dropped (Verification, F1).

**Record judgment:** valid with concerns. The curator accepted the missing source ("data looking very good and
real"), so the dataset is added; the counter-argument is issue 1. None of the do-not-add criteria holds:
- **Not the churn_telco_europa pattern.** Within each record month, churners and stayers share the snapshot date.
  - The "no activity" value of the inactive-days columns counts the days from 2010-01-01 to the snapshot. Among the
    kept rows it is 1,276 (30 June) for 43,547 stayers and 4,891 churners; July (1,307) and August (1,338) carry it
    for both classes too.
  - In the raw file, the June accounts never activated count their lifetime from 1970-01-01 to the day before their
    snapshot in both classes alike: 29 June for 2,003 stayers and 2,647 churners, 24 June for 273 and 59 (snapshot
    25 June). A lifetime counted to an exit date would spread over June.
  - The tenure of the activated June accounts keeps the daily pattern of the activations in both classes. The
    detrended daily histograms correlate at 0.28 at lag 0, and at most 0.17 at any other shift up to 60 days. 20
    random stayer samples of the churners' size give 0.22 to 0.36. In Europa the churners fell far below the stayers'
    reference (0.27 against 0.94).
  - The weekly part of the pattern is 62% as strong in the churners as in the stayers. With the lifetimes counted
    to the snapshot, I read this as churn varying with the weekday of activation, not as a second measurement date.
- **The churners' features do not end at the churn, as far as the data show** (kept rows):
  - The churners' last activity falls off steeply towards the past. Of the 3,702 June churners with an activity in
    the last 30 days, 52.6% had it 0-5 days before the snapshot and 7.3% 25-30 days before; churn spread evenly over
    June would give about 19% each. 862 of the 5,100 June churners (16.9%) were active within a day of the
    snapshot.
  - The June churn rate rises smoothly with the days without activity: 3.4% at 0-1 days, 20.3% at 8-14, 59.1% at
    61-100. No cutoff appears, so the label is no threshold on a snapshot feature.
  - The 100-day columns hold no data after the snapshot. For the 2,683 accounts that joined in their record month,
    the `last_100_` call minutes never exceed the month's (one row by 0.01), and SMS and data exceed it in 4 rows
    each, in both classes.
  - The churn definition itself is undocumented (issue 1).
- **No copy of another churn file** (the DSN/SATO pattern). The rows were compared with SATO 2015
  (churn_telco_south_asia), DSN TRAIN (churn_telco_south_asia_duplicate), the Europa train file (numeric non-id columns only),
  iranian_churn, churn (MLC++), tour_travels_churn, bank_customer_churn and 300k rows of expresso (`explore/e2`).
  - No continuous column matches.
  - The best two-column row match is SATO's at 9.5%. With one column shuffled across rows it is 11.2%, so it is
    chance.
  - The schemas differ as well: 66 prepaid usage columns from 2013, against 14 (SATO), 16 (DSN) and 20 (Europa).
- **No other record or working-copy folder** holds OpenML 44231 or the Kaggle slug.

**Data:**
- Source: the Kaggle dataset dimitaryanev/mobilechurndataxlsx, downloaded with `uvx --from kaggle==2.2.2 kaggle` into
  `local-data-warehouse/mobile_churn/`.
- File: `mobile-churn-data.xlsx` (20,468,910 bytes, sha256 ebc820fa...71a1), one sheet "Churn prediction data",
  66,469 x 66.
- Uploaded on 2019-10-31, with no description.
- OpenML 44231 (2022-10-05) is the same file. Its parquet is identical row by row, in the same order.
- Licence: "unknown" on the Kaggle data card, "Unknown" on OpenML 44231.

**Definition:**
- Prediction point: at the end of the record month (30 June, 31 July or 31 August 2013), score each activated
  prepaid account from its state at that date and its usage in the month and the last 100 days.
- Target: `churn`, Yes 5,392 (9.9%) / No; ROC AUC.
- Regime and splits: IID, default splits (3 x 3 folds, train 36,138 rows). Each row is a different account (54,207
  distinct ids).
  - The record month marks a cohort, not a time step. After the cut, the July and August rows are the accounts that
    joined in those months: 527 and 1,006 rows, all with `user_intake` = 1.
- Size: 54,207 rows x 57 features, all numeric.
- Cleaning:
  - dropped the 12,262 accounts never activated: `user_intake` = 0 and `user_lifetime` counted from 1970-01-01, in
    every month (4,982 June, 35 July, 7,245 August). See Verification F1;
  - dropped `year` (constant 2013);
  - dropped `user_account_id`: unique, numbered in creation order;
  - dropped six per-destination inactive-days columns that equal the overall call / SMS column in every row;
  - the 1970-01-01 lifetime count set to missing: 1,295 kept rows, all accounts that joined in their month;
  - inactive-days values above 100 set to missing: 2010-01-01 counts (no activity on record) and 2012-09-28 counts
    (275-337, 335 cells);
  - churn mapped to Yes/No.
- Two `_decisions` tables: never-activated accounts by month (dropped, their churn and use, kept), and the snapshot
  dates by class.

**Checks:** `dataset check`: 0 errors, 0 warnings, 2 info (`dataset_duplicate_rows`: 9 rows;
`dataset_conflicting_duplicate_rows`: 8 rows).
- Accepted: `meta_license_unknown`, because the Kaggle and OpenML pages both say unknown. The earlier acceptance of
  `dataset_duplicate_rows` is removed, since the warning no longer fires.
- pandas 2.3.3 and 3.0.6 give the same checksum, v2:d0327629...c65f, which `README.md` records.
- `pytest -q tests/test_v2_datasets.py -k mobile_churn`: 1 passed, 1 skipped. With
  `DATA_FOUNDRY_V2_DATA_CHECKS=1`, 2 passed.
- `ruff check` and `ruff format --check`: clean.

**Probes** (untuned models, `--n-jobs 2`; outputs in `probes_v2/`; the first run's are in `probes/`):
- Task (5 of 9 splits): no flag.
  - LightGBM 0.848, random forest 0.846, logistic regression 0.823.
  - Single feature 0.773 (`user_spendings` on 3 splits, `calls_outgoing_count` on 2).
  - Smallest class per test fold: 1,797 rows.
- Leak (LightGBM, 3 splits): all features 0.844.
  - Alone: `user_no_outgoing_activity_in_days` 0.779, `user_spendings` 0.775. Dropping any of the top three costs
    nothing.
  - Missing-value indicators: `reloads_inactive_days` 0.677, `sms_outgoing_inactive_days` 0.668.
  - Depth-3 tree 0.804.
  - Exact copies: 0.1% of the test rows have one in train.
  - The label-free distance scores 0.727; "no spending in the month" alone scores 0.722.
- Generated: rule leaves cover 0.0% of the churners; no flag.
- Hidden groups: no hits. The top candidates are usage counts.
- Hand checks: the batch checks of Verification F2 (`explore/e12`, `e15`, `e16`).

**Issues for Lennart:**
1. **Keep a dataset whose source and churn definition are unknown?**
   - Evidence:
     - No description on Kaggle, licence "unknown".
     - The one discussion thread (2021-12-27) asks "can you give me the time frame of the collected data, and its
       provenance" and has no answer.
     - OpenML 44231: "No description available", creator "UNK".
     - A GitHub code search for the column name finds only later users: the TabSTAR curation file, a Teknasyon hiring
       case, a CTGAN-ENN paper repository.
     - The churn definition and its horizon are undocumented. The data place the label after the snapshot for both
       classes, but cannot show its window.
   - Clues for a search (the verifier's, rechecked):
     - activations start on 2008-01-22, with 2,929 accounts that day and 1,725 the next: a system or operator start;
     - about 92 days of activity history;
     - on-net calls are rare: 0.3 per account and month, against 16.3 off-net and 1.5 abroad. That suggests a small
       operator or an MVNO;
     - placeholder dates 2010-01-01 and 2012-09-28;
     - prepaid, June-August 2013.
   - Implemented: added, following the curator's acceptance.
   - Alternative: No with `Missing source information`, as the guidelines' decision pattern says.
   - Caveat: the WebSearch budget of my session, and of the verifier's, was used up. A Google search for
     `"user_no_outgoing_activity_in_days"` or `"mobile-churn-data.xlsx"` might still find an origin.
2. **Accounts never activated are dropped in every month, June included. Accept, or one of the alternatives?**
   - Implemented: rows with `user_intake` = 0 and no activation date are dropped: 12,262 rows (4,982 June, 35 July,
     7,245 August) with churn 69.4%, holding 8,515 of the 13,907 churners. Kept: 54,207 rows, churn 9.9%. LightGBM
     3 x 3: 0.848.
   - Alternative A, the verifier's and coordinator's rule (after June only): 59,189 rows, churn 13.7%, 0.870. It
     keeps 4,982 June SIMs of the same profile (churn 54.3%), 4,021 exact copies and 235 vectors with both labels.
   - Alternative C, June only (`month` dropped): 57,656 rows, 0.872. It also keeps the 4,982 June SIMs. June only
     with them dropped: 52,674 rows, 0.850.
   - Alternative D, all rows as first shipped: 66,469 rows, 0.908. A random split leaks the August batches (0.882
     with batches held together).
3. **Small column choices, all within 0.002 AUC.**
   - `month` is kept as the record month. It is constant when a deployed model scores one month; dropping it gives
     0.8479 against 0.8481.
   - `user_account_id` is dropped; TabSTAR drops it too.
   - Default-date day counts are set to missing (1970-01-01, 2010-01-01, 2012-09-28).
   - The year is 2019, the Kaggle upload and the record's year; the data are from 2013.

**Verification** (the independent verifier said "needs changes"; my responses, checked with my own scripts in
`explore/e9` to `e16`):
- **F1 (major): the rows after June without the intake flag or an activation date are SIM cards. Accepted, and
  extended to June.**
  - Reproduced: 7,280 rows (7,245 August, 35 July), churn 79.8%, 5,809 churners (41.8%); a zero top-up and a zero
    balance in 98.3%; 80.0% without a call, SMS or data session; 6,535 of the 10,553 exact copies; LightGBM 0.908
    with them, 0.870 without, 0.872 June only.
  - The same rule finds 4,982 June accounts of the same profile (`e10`, `e11`):
    - call minutes, SMS or data in the last 100 days: 0.5% (August SIMs 0.2%; activated accounts 95.8%);
    - a zero top-up sum in June 99.6%, a balance in 1.9%;
    - churn 54.3% (2,706 churners);
    - recent ids: 70% of the June rows with ids 1,150,001-1,160,000 have no activation date;
    - 959 have a zero top-up on 2-11 May (ids mostly 1,154,408-1,158,608), the provisioning pattern of the August
      batches.
  - Old accounts are not what lacks a date: the activated accounts have dates back to 2008-01-22. So the rule drops
    the never-activated accounts in every month. This goes beyond the coordinator's literal rule (after June only),
    which stays as alternative A in issue 2.
  - June only was not chosen: the kept July and August rows show no further problem.
    - All of them are `user_intake` = 1, with churn 16.9% (July, 527) and 20.2% (August, 1,006), against 16.6% for
      the 1,150 June joiners.
    - No repeated feature vectors, no runs of ids.
    - Labels in id order: 0.701 against 0.694 ± 0.009 for shuffled blocks.
- **F2 (major if the rows stayed): the batch leak. Checked after the cut.**
  - Reproduced on all rows: LightGBM 0.908 random, 0.882 with provisioning batches held together. The verifier's
    batch key gave 0.889.
  - Kept rows (mine):
    - 0.848 random, 0.849 with identical feature vectors held together;
    - 9 exact copies; the longest run of consecutive ids with one feature vector is 1 row;
    - next-row label agreement 0.828 against 0.826 for shuffled 500-row blocks;
    - holding out the activation days of the 2,683 accounts that joined in their month gives 0.8477 against 0.8481.
      Their churn varies slightly more across days than chance (p = 0.02).
  - Under alternative A the gap by identical vector is 0.004 (0.870 against 0.866), as the verifier expected. Holding
    June's zero-top-up batches together costs nothing (0.8699, `e16`). An earlier 0.857 came from also holding the
    3,952 SIMs with no top-up on record together as one group, which is a cohort shift, not a batch; that number is
    not used.
- **F3 (minor): the 2012-09-28 placeholder. Accepted.**
  - Every value from 101 to 999 counts back to 2012-09-28. The kept rows hold 335 such cells (values 275, 306, 337),
    set to missing with `.where(column <= MAX_INACTIVE_DAYS)`, where `MAX_INACTIVE_DAYS` is 100.
  - Docstring and comments are fixed. Real values reach 92 days in June (100 for
    `user_no_outgoing_activity_in_days`) and 30 after June.
  - One correction to the finding: the verifier's "no label signal" holds on all rows (19.5% against 20.9%). On the
    kept rows the 244 rows with such a cell churn at 14.8% against 9.9%; the comment says so.
- **F4 (minor): wording. Accepted.** The lifetime count ends on the day before the snapshot (29 June, 24 June). The
  August text now describes the never-activated rows and the joiners separately.
- **F5 (minor): label timing. Accepted.** The verifier's evidence was recomputed on the kept rows and is in the
  prediction-point bullet (52.6% / 7.3%, against the verifier's 47.9% / 8.0% on all June churners). On the
  `last_100_` call minutes I find 1 row above the month's value, by 0.01 (the verifier: 0); SMS and data have 4 rows
  each, in both classes.
- **F6 (run-wide): the record pointer.** `v2_path` is unset; `sync-notebooks` is for the orchestrator.
- **The earlier issue 3 (duplicates kept) is moot.** Of the 10,553 exact copies, 9 remain.

### mortgage

**Outcome:** added and checked (fixed after verification).

**Record judgment:** valid with concerns.
- Source: the data page of Baesens, Rösch and Scheule, *Credit Risk Analytics* (Wiley 2016,
  doi:10.1002/9781119449560), http://www.creditriskanalytics.net/datasets-private2.html, section "Data Set Mortgage":
  "in panel form and reports origination and performance observations for 50,000 residential U.S. mortgage borrowers
  over 60 periods ... a randomized selection of mortgage-loan-level data collected from the portfolios underlying U.S.
  residential mortgage-backed securities (RMBS) securitization portfolios and provided by International Financial
  Research".
- The curator asked whether the source holds more data. It does not publicly. International Financial Research
  Limited was a consultancy: its home page of December 2016 (Wayback Machine) says it "provides advise in the area of
  risk management and prudential regulation of financial institutions" and links only a client portal. The site now
  returns 404.
- A predictive task the books themselves use. The status per loan and period is the competing-risks target of the R
  Companion's chapter 11 (`multinom(status_time ~ FICO_orig_time + LTV_time + gdp_time)`), and chapter 13 backtests
  out of time: train on `time < 60`, test on `time > 59`. Source for both: Ch11/Ch13 scripts in
  github.com/dpicone1/Credit-Risk-Anaytics-The-R-Companion, a reader's transcription of the R Companion's code; the
  book text was not read.
- In scope: a fixed classification per loan and quarter with a temporal split, not forecasting of a series.
- Unique:
  - no working-copy folder holds this panel;
  - no other record cites creditriskanalytics.net or mortgage data, except its unrelated siblings from the same book
    (homeq_default_prediction, retired; lgd; corporate_credit_rating_cat_data_set_ratings_raitings);
  - OpenML has no dataset named "mortgage" and none with 622,000-623,000 rows.
- Real data. The HMEQ-style generation checks find nothing (see Probes). The macro columns are the real US series.

**Data:**
- Source used: `mortgage_csv.rar` from the book's data page, extracted to `mortgage.csv`.
  - 622,489 rows x 23 columns, 68,397,638 bytes.
  - sha256 of the rar: 1ce1c9be...0b88924; of the csv: f8e819eb...0c1a8.
  - Kept in `local-data-warehouse/mortgage/mortgage.csv`; the rar is deleted, as the download description does.
- The site asks for a name and an agreement on `datasets.html` before it shows the data page; the file link itself
  needs no login. I did not submit the form.
- No RAR extractor is installed on the machine. I used RARLAB's official `unrar` 7.23 (Linux build) from a scratch
  folder, now deleted; the description says that any extractor works.
- Licence, noted only:
  - download form: "I agree to use the data only in conjuction with the Credit Risk Analytics textbooks ...
    Commercial use is prohibited.";
  - site terms (`terms.html`): "You must not: Republish material from Credit Risk Analytics ... Redistribute content
    from Credit Risk Analytics".
  - Both are in `license`, as in the sibling `lgd`.

**Definition:**
- Folder: `datasets/_dev/tabarena-v0pt2/mortgage/`.
- Prediction point: the start of each quarter. A lender or RMBS investor scores every loan it holds for default,
  payoff or neither during the quarter. Known then:
  - the origination fields;
  - the loan's balance, LTV and rate at its previous observation;
  - the macro values published by then: unemployment one quarter back, GDP growth and the house price index two
    quarters back.
- Target: `status` (`active` / `default` / `payoff`) = the source's `status_time`; log loss.
  - Counts: 580,433 / 15,155 / 26,589.
  - Dropped `default_time` and `payoff_time`, the target's indicator columns.
- Regime: temporal on `time`.
  - `TemporalSplits(window=1, unit="unique", n_windows=3)` with a horizon of 1 step (one quarter).
  - Test periods 60, 59 and 58 (2015 Q1, 2014 Q4, 2014 Q3); each trains on all earlier periods.
  - Train 597,444-614,173 rows, test 8,004-8,482 rows with 43-77 defaults and 145-165 payoffs.
  - No gap: a quarter's status is known when the next one starts.
  - Loans recur: 99.4-99.9% of the test rows belong to loans with earlier quarters in train, the portfolio use
    case and the book's backtest.
- Size: 622,177 rows x 17 features.
- Main cleaning:
  1. Loan state from the previous observation (`*_lag_1`). The balance and rate are taken from that row. The LTV is
     recomputed from that balance with the source's own formula (reproduces `LTV_time` on every row) and the house
     price index two quarters back.
  2. Macro values as published when the quarter starts: `uer_time_lag_1`, `gdp_time_lag_2`, `hpi_time_lag_2`.
     `hpi_orig_time` is missing on the 16,290 rows of a loan's origination quarter and the next, where it is not yet
     published; those rows keep the house value at origination in their LTV.
  3. Period 51 is doubled for 312 loans:
     - 305 exact copies dropped;
     - 7 pairs that differ only in the status (active / payoff, loans ending in period 51): the payoff copy is kept.
  4. `id` dropped (a borrower id; a few ids hold two mortgages). A loan = (id, orig_time, balance_orig_time), used
     only to find the previous observation.
  5. Zeros set to missing:
     - origination rate (89,990 rows, 10,995 loans);
     - original balance (18 loans; exactly the 270 rows without `LTV_time`);
     - current rate (25 rows).
  6. The 3 one-hot real-estate flags become `real_estate_type`, with `other` for none set (19.5%).
  7. Period numbers kept as integers. They are quarters, 2000 Q2 = 1 to 2015 Q1 = 60:
     - Case-Shiller matches;
     - loan terms are 120 periods for 51% of the loans.
  8. Kept as recorded:
     - 8,315 loans end without an event (7,814 still active in period 60);
     - origination fields that change within a loan;
     - 44 rates above 25% and 38 LTVs above 300%;
     - 58 duplicate rows from 8 pairs of ids with identical origination profiles.
- pandas 2.3.3 and 3.0.6 give the same checksum, v2:a1e58ba0..., the one in the README.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 2 infos.
  - `dataset_duplicate_rows`: 25 rows.
  - `dataset_conflicting_duplicate_rows`: 4 rows.
  - Both come from the 8 twin-profile id pairs and are documented.
- No accepted warnings.
- `pytest tests/test_v2_datasets.py -k mortgage`: 2 passed, including the raw-data rebuild with
  `DATA_FOUNDRY_V2_DATA_CHECKS=1`.
- Imports with `load_definition`; ruff clean.

**Probes** (after the fix, 3 shipped windows, `--n-jobs 2`):
- Leak probes (untuned LightGBM, 50k sampled training rows):
  - all features one-vs-rest AUC 0.609;
  - strongest single features `interest_rate_time_lag_1` and `LTV_time_lag_1` 0.559; without the rate 0.582;
  - depth-2 and depth-3 trees 0.511 and 0.516;
  - missing-value indicators 0.502-0.504;
  - exact feature copies of test rows in train: 0.0%.
  - 1-NN label agreement: 0.974 for the closest tenth, 0.957 for all rows (chance 0.873). This is the panel: the
    nearest training row is the same loan one quarter earlier, `active` by construction.
- Generated probes: no flags (rule leaves hold 0.0% of the minority rows).
- HMEQ-style generation checks, by hand, one row per loan:
  - 28 of 50,059 loans share all 11 origination fields with another loan;
  - the label-free nearest-neighbour distance scores AUC 0.58 for default and 0.54 for payoff (HMEQ 0.92);
  - number formats are equal by outcome.
  - Whole-number original LTVs are 6-18 points more common among defaults in every vintage and FICO band, on the
    round LTV limits 80/90/95/100.
- Task probes: flag `drift_baseline`. `one_feature` no longer fires after the fix (`time` alone: skill 0.040 against
  0.101).
  - The previous quarter's class shares score log loss 0.134, against 0.137 for the best untuned family (linear,
    50k sampled rows).
  - Answer: on the full train side, LightGBM beats the previous quarter's shares in every window: 0.1195 vs 0.1251
    (period 60), 0.1317 vs 0.1374 (59), 0.1362 vs 0.1391 (58).
  - It also ranks loans within a quarter: one-vs-rest AUC 0.56 / 0.68 / 0.59 for default and 0.72 / 0.66 / 0.63
    for payoff.
  - A small but real signal beyond the drift; kept (rule 2).
- No `hidden_groups.py` or `group_probes.py`: the task is temporal. `tuned_results.py` skipped, as the brief says.

**Verification** (independent verifier, "needs changes"; fixed 2026-10-07):
- **F1, blocker (look-ahead in the macro columns): accepted and fixed.**
  - I checked it myself against the FRED series:
    - `hpi_time` = Case-Shiller 10-City NSA of the quarter's last month (56 of 60 periods; the 4 newest differ by up
      to 0.11);
    - `uer_time` = UNRATE of the quarter's first month (59 of 60);
    - `gdp_time` = the quarter's year-on-year real GDP growth (correlation 0.991, against 0.87 one quarter off).
  - None is published when the quarter starts.
  - My logistic regression gains 0.0007-0.0014 log loss from the quarter's own values over one quarter back, and
    0.0014-0.0022 over the published values (periods 58-60). LightGBM moves by at most 0.0006, which is why my first
    check, with LightGBM only, missed it.
  - Implemented: uer from t-1, gdp and hpi from t-2; `LTV_time_lag_1` recomputed with hpi(t-2) by the source's
    formula (matches `LTV_time` on 100% of rows).
  - Beyond the verifier: `hpi_orig_time` is masked on the 16,290 rows where the origination quarter's index is not yet
    published (48 rows in the test quarters). On those rows the LTV keeps the house value at origination.
  - Prediction-point and macro bullets rewritten with the evidence.
- **F2 (one-quarter windows mostly score the level): accepted as evidence for issues 2 and 3; design unchanged.**
  After the fix, 76-86% of LightGBM's gain over the all-history class shares is the quarter's overall event rate, in
  four-quarter windows 64-84%. Numbers in issues 2 and 3.
- **F3 (site terms): fixed.** The quote is in `license` and in the record comment.
- **F4 (batch of exits after period 59): confirmed and added to the censoring sentence.**
  - 75 of the 501 exits without an event fall after period 59 (3-23 per period in 38-58); 49 of them were first
    seen in period 53.
  - Median rate 2.5%, FICO 699; 21% flat balances against 30% for period-60 defaulters.
  - 36 of the 501 end on an `active` row with a zero balance (the verifier counted 37).
- **F5 (record pointer):** `v2_path: datasets/_dev/tabarena-v0pt2/mortgage/dataset.py` to set when the records are
  applied.

**Issues for Lennart:**
1. **The book's own design leaks through the row's loan state; I lag it.** Should the definition keep the lag?
   - Evidence: on the event row, the row's own balance records the event.
     - Periods 58-60: 5.3% of payoff rows have a zero balance and 14.9% a balance more than 5% below the previous
       one (active rows: 0.02% and 2.6%).
     - 77% of default rows are unamortised (active rows 12%).
     - Out of time, the row's own balance and LTV lower LightGBM's log loss by 0.003-0.005 in six windows; the
       verifier finds the same in every model family.
   - Now: balance, rate and LTV from the previous observation.
   - Alternative: the raw columns as the book uses them.
2. **Target: 3 classes or default only?**
   - Now: `status` (active / default / payoff), the record's multiclass and the R Companion's chapter 11 model.
   - What the 3-class log loss measures: 76-86% of LightGBM's gain over the all-history class shares is the quarter's
     overall event rate, which the previous quarter's shares already give (dummy / drift / LightGBM: 0.1461 / 0.1251 /
     0.1195 in period 60, 0.1553 / 0.1374 / 0.1317 in 59, 0.1564 / 0.1391 / 0.1362 in 58).
     - The per-loan part is 0.0029-0.0057.
     - Without `time`, LightGBM loses 0.0013-0.0122.
     - The logistic regression is no better than the drift constant in periods 59 and 58 (0.1375, 0.1414).
     - So method rankings depend largely on how a method extrapolates the quarter's level.
   - Alternative: binary `default_time` scored by ROC AUC (the book's ch. 6 models and ch. 13 backtest), as a separate
     folder (for example `mortgage_default`).
     - It ignores the level and treats payoffs as non-events.
     - LightGBM default AUC 0.59 / 0.71 / 0.61 on the one-quarter windows (43-77 defaults each).
3. **Window length: one quarter or one year?**
   - Now: 3 one-quarter windows (the book's backtest on one period; lending_club's quarterly refit), each with
     8.0-8.5k rows and 43-77 defaults.
   - Alternative: 3 four-quarter windows (periods 49-52, 53-56, 57-60).
     - 33-37k rows with 222 / 389 / 678 defaults.
     - LightGBM log loss 0.1288 / 0.1604 / 0.1810 against the previous year's shares 0.1337 / 0.1629 / 0.1876.
     - The level is still 64-84% of the gain.
     - Default-only AUC 0.60 / 0.63 / 0.66.
   - Longer windows give more stable scores but do not remove the level effect. The verifier and I keep the current
     design; Lennart decides.
4. **Macro lags: per series, or all one quarter back?**
   - Now: each series as published when the quarter starts (uer t-1, gdp t-2, hpi t-2; LTV with hpi t-2).
   - Simpler alternative: all three one quarter back, keeping the source's lagged LTV. GDP growth and the house price
     index are then still one to two months early (GDP about a month after the quarter, Case-Shiller two months
     after its month).
   - Keeping the quarter's own values is not an option (F1).
   - Not fixable: the file's GDP figures differ from FRED's current release (period 60: 2.84 against 4.0) and their
     release date is unknown.
5. **Regime.** The record lists Grouped and Temporal; v2 declares one.
   - Now: temporal, with loans recurring across the cut on purpose (99.4-99.9% of test rows).
   - Not built: a loan-grouped variant. It would train on quarters after the test quarters.
6. **Proposed `task_probes.md` case row** (I may not edit skills):
   `| mortgage | drift_baseline (one_feature before the macro fix) | kept (proposed, 7 Oct) | the previous quarter's
   class shares (0.134) match untuned models on 50k sampled rows; on the full train side LightGBM beats them in 3 of
   3 quarters (0.1195/0.1317/0.1362 vs 0.1251/0.1374/0.1391) and ranks loans within a quarter (AUC 0.56-0.72); the
   level is 76-86% of the gain |`.
7. **Duplicates and censoring kept.**
   - 58 rows come from 8 pairs of ids with identical origination profiles. Some may be one loan listed twice (ids
     3018 and 3020).
   - 501 loans leave before period 60 without an event; their last row stays `active`. 75 of them leave together
     after period 59, a pool leaving the data rather than missed defaults (F4).
   - Both are under 0.1% of the rows.
8. **The source de-identified the periods; the comments re-identify them as quarters 2000 Q2-2015 Q1** (three public
   series match). Fine to state?
9. **Probe and framework notes** (not patched):
   - `task_probes.py` caps the train side at 50k random rows. On a drifting panel the newest periods are then thin.
     For temporal tasks the cap could keep the newest rows.
   - The 1-NN agreement in `leak_probes.py` mostly measures panel repetition on loan-period data.
   - The known `splits_comment` dedent gap shows in this README too.

### myocardial_infarction_complications
**Outcome:** not added (the same data ships as `mic` in the working copy). No dataset folder was created.

**Record judgment:** do not add: the same underlying data is already in the working copy as
`datasets/_dev/tabarena-v0pt2/mic/` (criterion 1, unique).
- The record's only source link, https://doi.org/10.24432/C53P5M, is also a source link of `curation/records/mic.md`
  (`DF: Yes`, `TabArena (v0.1)`, `BeyondArena`). It resolves to UCI dataset 579, whose zip holds `MI.data` with
  sha256 `d3bf6a8c...47a4`, byte-identical to `local-data-warehouse/mic/MI.data`, the file `mic/dataset.py` reads.
- `mic` ships LET_IS (lethal outcome, cause) as a multiclass target at admission; it is the at-admission example of
  `leak_checks.md` §1 and §3. This record would add a second outcome column of the same 1,700 patients.
- Guidelines, "Quick decision patterns", re-upload bullet: "Two records built from the *same underlying data* with only
  a minor variation — a swapped target / outcome column ... — are duplicates when neither adds a genuinely distinct
  task" (precedent `arsenic_male_lung`). Rubric item 2 of `/verify-dataset` asks the same ("including a different
  target/slice/version of one cohort"). Closest precedent: `airfoil_self_noise_duplicate`, also a `New (BeyondArena)`
  candidate already in TabArena, set to `No` + `Duplicate`.
- The record's comments do not mention `mic` (the record came from the "New - IST" sheet in June 2026; `mic` from
  the TabArena workbook). Its own comment "Has multiple datasets / outcomes in one. Take one at most." argues against
  a second task from these patients.

**Data:** UCI 579 static zip (https://archive.ics.uci.edu/static/public/579/myocardial+infarction+complications.zip),
`MI.data`, 1,700 x 124 without a header row (ID, inputs 2-112, outcomes 113-124), Krasnoyarsk Interdistrict Clinical
Hospital No. 20, 1992-1995. The Leicester copy (doi 10.25392/leicester.data.12045261.v3, CSV with header, plus the
description PDF) holds identical values. Licence CC BY 4.0 (UCI page and the figshare record). Downloaded to
`local-data-warehouse/myocardial_infarction_complications/` for the analysis below only; it is a copy of `mic`'s file
and can be deleted.

**Definition:** none.

**Checks:** none (no definition).

**Probes:** the probe scripts need a definition, so none ran. For the target question (issue 2) I measured the
admission-time signal of every outcome instead: all 1,700 patients, the source's 102 admission inputs (columns 2-112
without 93-95 and 100-105, the same drop as `mic`), 10 x 3 stratified CV (seed 4267), untuned LightGBM (200 trees,
learning rate 0.03, 15 leaves) and an L2 logistic regression (C = 0.05, median imputation with missing indicators).
Scripts and outputs: `cv.py`, `cv_results.csv`, `counts.txt`, `overlap.txt`, `icu_drugs.txt` in this folder.

| outcome (column) | positives (per test fold) | ROC AUC LightGBM / logistic | note |
|---|---|---|---|
| atrial fibrillation (FIBR_PREDS, 113) | 170 (57) | 0.709 / 0.717 | log loss 0.316 against a prior of 0.325; 0.708 without the ICU drug columns; best single feature AGE (0.64); 124 of the 170 had no AF sign at admission or in the history |
| supraventricular tachycardia (PREDS_TAH, 114) | 20 (7) | 0.475 / 0.584 | no signal, too few positives |
| ventricular tachycardia (JELUD_TAH, 115) | 42 (14) | 0.728 / 0.733 | ICU lidocaine alone 0.66; 0.720 without the ICU drug columns |
| ventricular fibrillation (FIBR_JELUD, 116) | 71 (24) | 0.742 / 0.710 | rests on ICU lidocaine: VF in 11.1% of the 479 patients given it, 1.5% otherwise (alone 0.742); 0.648 / 0.628 without the ICU drug columns |
| third-degree AV block (A_V_BLOK, 117) | 57 (19) | 0.719 / 0.709 | inferior infarction (`inf_im`) alone 0.76, the expected clinical driver |
| pulmonary edema (OTEK_LANC) | 159 (53) | 0.724 / 0.704 | |
| myocardial rupture (RAZRIV) | 54 (18) | 0.794 / 0.762 | all 54 died; the same patients as LET_IS class 3 |
| Dressler syndrome (DRESSLER) | 75 (25) | 0.587 / 0.571 | |
| chronic heart failure (ZSN) | 394 (131) | 0.712 / 0.652 | |
| relapse of MI (REC_IM) | 159 (53) | 0.623 / 0.634 | |
| post-infarction angina (P_IM_STEN) | 148 (49) | 0.661 / 0.665 | |
| death (LET_IS > 0) | 271 (90) | 0.913 / 0.894 | |
| LET_IS, 8 classes (`mic` now) | smallest 12 (thromboembolism, 4 per fold); 18, 23, 27, 27, 54, 110 deaths, 1,429 alive | macro one-vs-rest 0.867 / 0.843 | log loss 0.555 (logistic) against a prior of 0.706 |

**Issues for Lennart:**
1. **Duplicate of `mic`: mark the record `No` + `Duplicate`?** Evidence above (same DOI, byte-identical file, a
   swapped outcome column of the same 1,700 patients). Implemented now: nothing; no folder. Alternative: ship a second
   folder with an arrhythmia target next to `mic`; the guidelines call that a duplicate, and no two folders of the
   working copy share their rows. The convention would rename the record to `mic_duplicate`.
2. **Which outcome should `mic` predict?** The record prefers an arrhythmia complication over the lethal outcome.
   The source ranks none of its 12 outcomes: the description (Golovenkin et al., Leicester PDF, p. 1) offers
   "prediction of complications based on patient information (i) at the time of admission and (ii) on the third day
   of the hospital period", and its bibliography has papers on both (p. 11, items 6 and 7: "Prediction of the occurrence of atrial fibrillation
   and ventricular fibrillation ..." and "Prediction of lethal outcome ..."). Implemented now: `mic` keeps LET_IS at
   admission, a valid source-defined task with clear signal, unchanged since TabArena v0.1 (`task_probes.md` rule 6:
   a valid task stays). Alternative, if the arrhythmia framing is preferred: switch `mic` to atrial fibrillation
   (FIBR_PREDS, binary, ROC AUC; drop LET_IS with the other 10 outcomes), the only arrhythmia outcome with enough
   positives whose signal does not rest on an ICU treatment column. Ventricular fibrillation would need the ICU drug
   columns dropped first (lidocaine is the treatment of ventricular arrhythmias, and the column has no time stamp,
   although the source allows it at admission). Side note: `mic`'s comment "We use the categorical target as it
   summarizes the other possible targets" does not hold: 766 of the 935 patients with at least one of the 11
   complications survived (LET_IS = 0), and 102 of the 271 deaths carry no complication flag.
3. **`mic` loses patient 1.** `mic/dataset.py` reads `MI.data` with `pd.read_csv(..., na_values="?")`, but the file has
   no header line, so the first patient (ID 1, alive, no complication) becomes the header: 1,699 rows instead of
   1,700 (`mic/README.md`: `n_rows: 1699`). Fix in `mic`: `header=None`; the renaming in `_clean` then works as before,
   and the container needs a rebuild and a CHANGELOG entry. Not changed (another dataset's folder). While there:
   `KFK_BLOOD` has 4 observed values in 1,700 rows and `IBS_NASL` 72.

### nba_players_2016_2019

**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/nba_players_2016_2019/`). Fix round after verification
done (comment corrections; the data, the target and the splits are unchanged).

**Record judgment:** valid with concerns.
- Provenance: Kaggle `davra98/nba-players-20162019` (uploaded 2019-12-04), a university project in Milan.
  - Data card, Context: "The goal of the project was to create a Robust Model to predict the All Star Game score for each player".
  - The uploader merged noahgift/social-power-nba, basketball-reference.com, hoopshype.com and the NBA's All-Star votes.
  - OpenML 43653 is the same file (all 1,408 rows; 51 names lost their non-ASCII letters).
- Unique: nothing in the working copy, the records or this run's list holds this data. `nba_draft`, `nba_shots`,
  `nba_2k20_player_dataset`, `basketball_c` and `vinnie` are other data.
- Concerns:
  - the shipped target is inconsistent across seasons (issue 1);
  - the split (issue 2);
  - the feature window (issue 3);
  - stale pageview values (issue 7).

**Data:** `nba_final.csv` from Kaggle via `uvx --from kaggle==2.2.2 kaggle datasets download davra98/nba-players-20162019`.
- 1,408 rows x 45 columns; sha256 `06455e5a0b3efebfc9257e7e71d687bc1aad3558d14b73bb186872d85d310eb5`.
- One row per player and season, 2016-17 to 2018-19: 436 / 498 / 474 rows, 660 players.
- Licence: CC0-1.0 on the Kaggle data card (`licenses`). The merged noahgift/social-power-nba is CC BY-NC-SA 4.0.

**Definition:** `datasets/_dev/tabarena-v0pt2/nba_players_2016_2019/dataset.py`.
- Prediction point: the end of the regular season (April). The task explains the January All-Star vote from the
  season (issue 3).
- Target: `all_star_score`, regression (rmse). It is 0.5 x fan rank + 0.25 x player rank + 0.25 x media rank, within
  season, conference and ballot position; lower is better. This is the NBA's own formula.
  - The 2017-18 and 2018-19 values are recomputed from the file's ranks (issue 1). They equal the NBA's official
    weighted scores.
- Regime: grouped by player (`player_id`, anonymized; 660 groups); `per_sample` labels, unit row, context none.
  - Default splits: 10 x 3 folds, train 918-963 rows, test 445-490 rows.
- Shape: 1,408 rows x 34 features, plus the group column and the target.
- Cleaning:
  - Dropped: the six vote/rank columns (the score's components); `Play` (follows from the vote); `Rk`
    (basketball-reference's alphabetical row number, Spearman 0.9995 with the last-name order); the name.
  - Columns renamed to basketball-reference's glossary in snake_case, in the file's order.
  - `Est` written as `East`; `Back`/`Front` written as `guard`/`frontcourt`.
  - Missing values kept as missing.
- Verified on the raw data:
  - `mean_views` is, for most rows, the mean daily Wikipedia pageviews (user agent) of the calendar year in which the
    season starts. 192 of the 856 later-season values are stale (issue 7).
  - Salaries match public figures (Curry, LeBron).
  - `team` is the team at season end.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 infos (26 checks); no accepted warnings.
- Checksum `v2:64b80d33f233a39ea90eb1a3dec37ec15eb1a40ca98583e837b24b85f7b032c5`, the same under pandas 2.3.3 and
  3.0.6. It changed in the fix round only because the comments are part of the metadata.
- ruff check and format: clean. Import check: ok.
- `pytest -q tests/test_v2_datasets.py -k nba_players`: 1 passed and 1 skipped; with `DATA_FOUNDRY_V2_DATA_CHECKS=1`,
  2 passed. Collection works again.

**Probes:** run before the fix round, which changed no data.
- `leak_probes.py` (3 splits), R²:
  - All features 0.736; depth-2 / depth-3 tree 0.506 / 0.561.
  - Best single feature `field_goals_per_game` 0.48; dropping any of the top three changes nothing.
  - 0.0% exact copies across the split; 1-NN R² 0.320.
  - Strongest missing indicator `wikipedia_daily_views` 0.08: players without a matched article, known before the vote.
    Not a leak.
- `task_probes.py` (30 of 30 splits): no flags.
  - LightGBM 0.697, random forest 0.666, linear 0.635, single feature 0.424, dummy -0.005.
  - LightGBM beats the dummy on 100% of splits; spread LightGBM - linear +0.061 (paired SE 0.004).
- `generated_probes.py`: no flags (exact 5.0% against 4.8% shuffled).
- `group_probes.py`: random split 0.730 against grouped 0.715 (gap 0.015).
  - Signal across players: LightGBM 0.703, random forest 0.691, ridge 0.611, kNN-5 0.563.
- The verifier's `hidden_groups.py --include-grouped`: no hits; `player_id` gap +0.034.
- README group statistics: the nearest neighbour is in the same player for 28.3% of rows (chance 0.1%); the player
  explains 0.88 of the target variance (0.47 for shuffled groups).

**Issues for Lennart:**

1. **Target fixed for 2017-18 and 2018-19 (accept the recomputation?).** The NBA's own tables now confirm it.
   - Evidence: in these seasons the shipped `Score` adds the cell's ballot size plus one (113-147) to the player and
     media rank of every player without votes in that category. A cell is season x conference x ballot position.
     - The rule reproduces all 972 shipped values.
     - In the 2017-18 West frontcourt the ballot's last player (Amile Jefferson, fan rank 146) is not in the file.
       There the constant is the file's largest fan rank plus two.
   - The file's own `PRank`/`MRank` are the NBA's ranks.
     - Recomputed from them, the two seasons equal the official weighted scores for all 958 file rows that my parse
       matched by name (the verifier: 960 of 960). The shipped `Score` matches 28.
     - Official sources: pr.nba.com 2018 and 2019 result pages and PDFs, formula "(Fan Rank * 2 + Player Rank + Media
       Rank)/4".
   - 2016-17 follows the formula for all 436 rows, with one rank per cell for players without votes. The NBA
     published only separate fan, player and media lists for 2017 (official.nba.com).
   - The shift raises 921 of 972 scores by 28.2-73.6 points. Mean shipped score by season: 42.4 / 93.6 / 87.1.
   - Models trained on 2016-17 score R² -0.95 to -1.07 on the shipped 2017-18 values, and 0.68-0.73 on the recomputed
     ones.
   - Implemented: 2017-18 and 2018-19 recomputed with the formula from the file's ranks, rounded to one decimal as the
     source rounds 2016-17. The official values are quarters, and the rounding moves them by at most 0.05.
     2016-17 values kept.
   - Alternatives:
     - (a) The shipped `Score` as is: R² ~0.77 with `season` as a feature, but the target's scale differs by season.
     - (b) Only 2017-18 and 2018-19 with the shipped values (972 rows).
2. **Split: grouped by player, or IID?**
   - The real use is a new season with mostly known players, i.e. a temporal split by season. Three seasons cannot
     give three windows with half the rows in training; only 2018-19 has that.
   - Implemented: grouped by the source's `Player_ID`.
     - The source itself kept one season per player "for a problem of indipendent observations".
     - Players recur: 295 in 3 seasons, 158 in 2, 207 in 1. A player's score carries over (Spearman 0.78 / 0.80
       between consecutive seasons).
   - Numbers, untuned 3 x 3 folds, random against grouped:
     - LightGBM 0.769 / 0.751, random forest 0.715 / 0.695, ridge 0.716 / 0.700.
     - The newest season held out (the real use): 0.747 / 0.737 / 0.697.
     - The source's last-season subset (660 rows, IID): 0.66-0.71.
   - Alternative: IID on all rows (warm start). A test player's other seasons, later ones included, would then be in
     training. Your hidden-group rule says the split follows who the new rows are, and here they are mostly known
     players; I chose grouped because a random split also trains on the future.
3. **The statistics cover the whole season, past the vote (option (a) implemented; (b) is your call).**
   - 25 of the 34 features (games, games started, minutes and the 22 other per-game statistics) are whole-season
     values. The regular season ends in April and the vote closes in mid-January.
     - By the vote's close a player had played a median 54% of the season's games.
     - `team` is the end-of-season team: of the 87 rows with a team of the other conference, 82 moved after the
       vote's close, 4 before it, and 1 had not played before it.
   - It is a mismatch, not a leak. The same statistics as of the vote's close predict better.
     - Grouped 5 x 3 folds, R² at the close against the whole season: LightGBM 0.772 against 0.741 (paired -0.031,
       SE 0.004); random forest 0.694 against 0.684 (-0.010, SE 0.002); ridge 0.703 against 0.684 (-0.019,
       SE 0.004).
     - The shipped features give 0.742, the same as the rebuilt full-season ones.
   - Implemented (a): the stated prediction point is now the end of the regular season. The task explains the January
     vote from the season, and every feature is known at that point. The numbers above are in the first
     `curation_comments` bullet.
   - Alternative (b): rebuild the 25 statistics and `team` as of the vote's close from box scores, as a second raw
     input. The stated point would then be the vote and the task the real forecast.
     - The verifier's box scores: Kaggle `nathanlauga/nba-games` (`games.csv`, `games_details.csv`). It covers 2004
       to December 2020 and was scraped from stats.nba.com through the `nba_api` endpoints; its licence is
       "unknown".
     - 1,397 of 1,408 rows match by name; 43 rows have no game before the vote.
     - The vote-close dates it used (16 Jan 2017, 15 Jan 2018, 21 Jan 2019) are not stated on the NBA result
       pages; I did not confirm them.
4. **Target choice.** Implemented the source's goal, the All-Star score. Other targets in the file:
   - `Play` (played in the All-Star Game): 73 positives, 19-28 per grouped test fold. LightGBM AUC 0.973, and
     points per game alone 0.966: close to one feature.
   - log `Salary` (the uploader's suggested alternative, 1,346 rows): grouped R² 0.632. A salary is set by contracts
     signed before the season.
5. **TabSTAR's version has no task.**
   - TabSTAR's `REG_SPORTS_NBA_ALL_STAR` (OpenML 43653) uses `Rk` as the target ("NBA All-Star Rank").
     - Source: github.com/alanarazi7/TabSTAR, `tabstar_paper/datasets/annotated/REG_SPORTS_NBA_ALL_STAR.py`.
   - `Rk` is basketball-reference's alphabetical row number.
   - It also keeps the six vote and rank columns and `Play` as features.
   - Proposed for the record (see the record comment).
6. **Metadata choices.**
   - `domain = "social science"`: the record says Other, and the schema has no sports value. The alternative is
     `business & marketing`.
   - `year = "2019"`: the Kaggle upload; the data covers 2016-17 to 2018-19.
   - Licence noted: CC0 on Kaggle; the merged Social Power NBA data, which gives the 2016 pageviews, is
     CC BY-NC-SA 4.0.
7. **Stale pageview values (mask the copies?).**
   - 185 rows of 2017-18 (123) and 2018-19 (62) repeat an earlier season's `mean_views` of the same player, and 7 more
     later-season rows hold a 366-day (2016) mean: 192 of 856 later-season values.
     - Example: Carmelo Anthony's rows hold the 2016 mean, 4,679, in all three seasons. The Wikimedia API gives 6,292 for
       2017 and 6,145 for 2018.
   - Several of the 120 rows under 20 views a day count a redirect title instead of the article. Example:
     T.J. McConnell has 2.8 a day for `T.J._McConnell` against 287 for `T._J._McConnell` in 2016.
   - No value is later than the vote, so none leaks.
   - Implemented: kept as shipped, and the comment bullet rewritten to say so.
   - Alternative: mask the 185 exact copies. A copy is a value equal to an earlier season's value of the same player;
     masking is deterministic from the raw file. Grouped LightGBM R² changes by -0.005 (SE 0.003); dropping the
     column changes it by -0.038 (SE 0.004). The redirect rows cannot be told apart in the file.

**Verification (fix round, 2026-10-07):** the verifier's verdict was "needs changes (comment corrections only)".
I re-checked each finding; scripts and outputs are in `<scratch>/fix/`.

1. Pageviews (major): accepted, and the bullet rewritten. My first claim generalized from Noah Gift's 2016 file and
   six players checked on the API.
   - Reproduced from the raw file: 185 copies (123 / 62), 7 more 366-day means, 120 rows under 20 a day (69 / 30 / 21).
   - On the API: Carmelo Anthony 4,679.17 / 6,292.18 / 6,145.16, T.J. McConnell 2.82 (redirect) against 286.56
     (article), LeBron James as stated.
   - The verifier's masking experiment, re-run: -0.005 (SE 0.003) masked, -0.038 (SE 0.004) dropped.
2. Prediction point (major): accepted. I implemented option (a); option (b) is in issue 3.
   - I re-ran the verifier's timing experiment from its saved `stats_by_cutoff.parquet`; it gives identical numbers.
   - My own simpler name match (1,310 rows): median share 0.538, and the rebuilt full-season games equal the file's
     for 99% of rows.
   - The 82 / 4 / 1 team moves are confirmed.
3. Official scores (minor): accepted, now cited in the target bullet, the first decision and the record comment. The
   constant is now worded as "ballot size plus one".
   - My own parse of the eight PDFs: for 958 of 958 rows matched by name, each official line ends with the file's fan
     rank, media votes, media rank and the recomputed score. The shipped score matches 28.
   - The 2017-18 ballot sizes (120, 139, 112, 146) match the line counts.
   - Amile Jefferson appears in the file only in 2018-19.
   - 2016-17: 436 of 436 values reproduced with the implied zero-vote ranks.
   - The formula is quoted on pr.nba.com (2018, 2019) and official.nba.com (2017, which also gives the fan-vote
     tiebreaker and only separate lists).
4. `Fvot` a tenth of the official count (minor): accepted, with one correction. It is 79 rows (40 in 2017-18, 39 in
   2018-19), not 78.
   - The verifier's parse missed Kyle Lowry 2018-19 (93,146 against 931,460).
   - `FRank` equals the official fan rank in all 79 (prefix match of player votes, player rank, 10 x `Fvot` and fan
     rank).

### numerai_v5_2
**Outcome:** added and checked: `datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/` (`version_of = "numerai_v5_2"`, raw files in `local-data-warehouse/numerai_v5_2/`).
**Record judgment:** valid with concerns. The source is Numerai itself (the data API, docs.numer.ai, the example-scripts repository the record links). The task is to rank each stock's next 20-day stock-specific return from its features at a weekly date. That is a fixed predictive task with a temporal split, not series forecasting, so the curator's `Non-IID (Temporal)` call stands. Concerns: the licence (issue 1), a real but very small signal that RMSE barely measures (issue 2), Numerai designing some features over the test windows (issue 3), and a source that serves only its current weekly snapshot (issue 8).
**Data:** Numerai data API through `numerapi` 3.1.1, v5.2 ("Faith2", released December 2025), downloaded 2026-10-06 from the S3 folder 20261005:
- `train.parquet`: 2,597,791,287 bytes, 2,746,268 rows, eras 1-574.
- `validation.parquet`: 4,417,740,944 bytes, 4,169,448 rows. Of these, 4,135,013 are `validation` rows in eras 575-1235 and 34,435 are `test` rows in eras 1236-1240 without targets.
- `features.json`.
- Each parquet file has `era`, `data_type`, 41 targets, 2,748 int8 features and the index `id`. The SHA-256 of all three files is in `download_description`.
- Licence: Numerai, Inc. Terms of Service (last updated 2026-08-31, numer.ai/terms), section 4.2 "Data License and Confidentiality". It grants "a limited, non-exclusive, non-transferable, revocable license to access and use the Data solely for the purpose of participating in Tournaments", and says "you shall not: (i) use the Data for any commercial purpose outside of the Services; ... (iii) redistribute, sublicense, sell, rent, lease, or otherwise make the Data available to any third party", and "You shall maintain the Data in confidence". The page needs JavaScript; I read the text from the site's script bundle.
**Definition:** `numerai_v5_2_1m`.
- Prediction point: every Friday after the market close (one era), a model scores each stock from that day's features. The target resolves about 4 weeks later.
- Target: `target_ender_20`, which equals `target` on every row of v5.2. Regression, scored with RMSE (the default). It has 5 levels from 0 to 1 holding 5/20/50/20/5% of each era, so every era's mean is 0.4999-0.5.
- Split: temporal on `era` (int32) with `TemporalSplits(window=52, unit="unique", n_windows=3, gap=4)` and a horizon of 52 weeks.
  - Test eras 1184-1235, 1132-1183 and 1080-1131, with 361,712 / 333,081 / 327,025 rows, all kept.
  - Train eras end at 1179 / 1127 / 1075. The 4 eras in between are embargoed, so at era T the newest training label is from T-5, which matches the real label delay.
  - Each train side is a random 1M rows (`subsample_to_budget`).
- Frame: 2,025,745 rows x 781 features (Numerai's 780 `medium` features plus `era`).
- Cleaning:
  - Keep `data_type` train/validation and eras up to 1235 (6,881,281 rows).
  - A feature-era in which every stock has bin 2 (Numerai's documented fill for missing data) becomes NaN. 290 features become float32. This covers 6.3% of the feature-eras and 5.0% of the values of eras 1-574, and nothing after era 894.
  - The other 40 targets are not read, and neither is `id` (it is re-coded every era, so it is no entity).
- Other checks: no two rows share a feature vector, and the highest correlation between two features is 0.990 (300k-row sample).
- pandas 3.0.6 (the shared venv) builds the same checksum as 2.3.3 on the final definition: `v2:b95ac395...b694`.
**Checks:**
- 0 errors, 0 warnings.
- Accepted: `task_target_low_cardinality`. The target is a continuous return binned into 5 ordered levels, and Numerai itself treats it as regression.
- Infos:
  - `dataset_duplicates_skipped`: 1.58B cells is over the 50M budget, so I checked duplicates by hand (above).
  - `meta_time_horizon_unit`: I kept `weeks`, because an era is exactly one week.
- Cost: `dataset check` takes 3.4 min wall and peaks at 53 GB RSS. The final check ran once after all edits.
- Lint and tests: ruff clean. The pytest for the folder passes (1 passed, 1 skipped).
**Probes:** all on the 3 shipped windows, with LightGBM capped at 2 threads.
- `leak_probes.py` (50k-row sides): no leak signal. 15 min, 84 GB peak.
  - All features together: R^2 -0.022.
  - Depth-2 and depth-3 trees: -0.001 each.
  - Best single feature: 0.000. Missing-value indicators: 0.000 or below. Dropping any one feature changes nothing.
  - Exact copies of a test row in train: 0.0%.
  - 1-NN R^2: -1.0 on the closest tenth, -1.1 on all rows.
- `task_probes.py` (`--n-jobs 2`): flags `no_signal`, `drift_baseline` and `unstable`.
  - R^2 by model: dummy -0.00005, drift -0.00003, ridge -0.014, random forest -0.005, LightGBM -0.011, best single feature -0.0002. No family beats the dummy in any window.
  - I answered the flags with a larger run of my own: 1M train rows and a LightGBM shaped like Numerai's example model (600 trees at learning rate 0.02).
  - Its per-era correlation is 0.0064 / 0.0141 / 0.0181, newest window first. It is positive in 34 / 43 / 44 of 52 eras (t = 3.0 / 7.2 / 8.7).
  - Its R^2 is -0.0002 / 0.0001 / 0.0003. With the prediction scale fitted on the newest 26 train eras it becomes 0.00003 / 0.0002 / 0.0003.
  - Ridge reaches a per-era correlation of 0.0045 / 0.0094 / 0.0156.
  - The signal is real but small, so the task stays (task_probes.md, rule 2).
  - `drift_baseline` fires because the target is ranked within each era, so the drift constant equals the mean.
  - `unstable` follows from R^2 being near 0.
  - All of this is written into `curation_comments`.
- `generated_probes.py`: exact 0.0% against 0.0% shuffled, no flags. It is uninformative here: 95% of the rows sit on mass points of the 5-level target.
- `hidden_groups.py` and `group_probes.py` were not run: this is a temporal task, and `id` changes every era, so no entity exists.
**Verification:** an independent verifier returned "ready with noted concerns" and found no leak and no wrong number. Per finding:
1. Metric: applied. A new `curation_comments` Note says RMSE mostly ranks how far a model shrinks towards 0.5. On the newest window the constant 0.5 beats LightGBM and ridge under RMSE (R^2 -0.0002 / -0.0003), although both correlate with the target per era (t = 3.0 / 2.3). The decision stays with Lennart (issue 2).
2. Faith features: applied. A new `Potential leak, kept on purpose:` bullet gives the verifier's paired numbers. I extended it to the 122 `midnight` features (v4.3, 2024-01-12, about era 1098), which the verifier could not date: they add +0.0017 +- 0.0012 before their release (eras 1080-1097) and +0.0004 +- 0.0006 after it. Dropping the 75 Faith features is issue 3.
3. Embargo: no change. The verifier confirmed the 4-era gap: the autocorrelation of per-era signals is 0.020 at lag 4, and the closest train-test pair is at lag 5.
4. `_1m` sampling: no change. The verifier confirmed it.
5. pandas 3: applied. The shared venv gives `v2:b95ac395...b694` on the final definition, the same as pandas 2.3.3. My earlier logs predated the last edit.
6. ToS: applied. Clause (i) and the confidentiality duty are now in `license` and in issue 1.
7. `splits_comment`: applied. It now says train ends at era 1179 for the window starting at 1184, that the newest known label at era T is from T-5, and that Numerai's notebook code skips only 3 eras, so our gap is one era stricter.
8. Hashes: applied. The three SHA-256 values are in `download_description` (I recomputed them; they match `verify/sha256.txt`).
**Issues for Lennart:**
1. Licence (noted, not a verdict reason). Numerai's Terms of Service, section 4.2 (updated 2026-08-31), license the data "solely for the purpose of participating in Tournaments". They forbid "(i) use the Data for any commercial purpose outside of the Services" and making it "available to any third party", and they require keeping the data "in confidence". Both a shipped container and a company running the benchmark would fall under this. Implemented: the terms are in `license`. Alternatives: ship only the definition and let users download with `numerapi`, or ask Numerai for permission.
2. Metric and task worth. On RMSE:
   - The best model I fit reaches R^2 of 0.0003 at most, while its per-era correlation is significant in every window (t = 3.0-8.7). Numerai on per-era scores: "+/- 0.05 is normal in quantitative finance".
   - Under RMSE the constant 0.5 beats both fitted models on the newest window, so RMSE mostly ranks shrinkage towards 0.5.
   - Numerai scores per-era correlation (CORR). `pearsonr` is a canonical regression name in `bundle_checks.KNOWN_METRICS`, but TabArena's adapter allows only `rmse` for regression (`DEFAULT_EVAL_METRICS` in `tabarena/benchmark/task/data_foundry/adapter.py`) and falls back to it with only a DEBUG log.
   - Implemented: RMSE, with the Note bullet. Alternatives: `metric = "pearsonr"` plus an adapter override, or drop the dataset if the benchmark scores regression only by RMSE.
3. Faith features. Numerai designed the 75 Faith features of `medium` before releasing them with v5.1/v5.2: October/December 2025, marked at era 1192 in the v5.3 notebook. So eras 1080-1191 of the test windows lie in their design period.
   - Paired ridge gain in per-era correlation: +0.0041 +- 0.0007 in 1080-1131, +0.0016 +- 0.0007 in 1132-1183, +0.0097 +- 0.0021 in 1184-1191, and +0.0019 +- 0.0008 after the release.
   - LightGBM gain for the same periods: +0.0027, -0.0006, +0.0109, +0.0008.
   - The 122 `midnight` features show a smaller effect that is not significant (+0.0017 +- 0.0012 before their release, +0.0004 +- 0.0006 after).
   - Implemented: keep them, with a note (the leak_checks precedent for feature selection on the labelled set). Alternative: drop the 75 Faith features (705 left, LightGBM correlation 0.0041 instead of 0.0064 on the newest window), or move the test windows after era 1200 once there are enough eras.
4. Feature set. Implemented: Numerai's `medium` set (780 features, "each unique in some way").
   - LightGBM per-era correlation on the newest window: `medium` 0.0064 (34/52 eras positive), `all` (2,748 features) 0.0055 (31/52), `small` (42 features) 0.0011 (30/52). `all` also takes 3.5 times the fit time (789 s against 223 s).
   - With `all`, the frame would be 14.8 GB instead of 3.4 GB: 1,510 of its features have missing eras and would become float32 (5.6 GB without that conversion). The pipeline peak would grow from 53 GB to an estimated 200+ GB.
   - 105 of the `all` features, all from the `faith` set, are empty in every era before 575.
   - `small` holds the features "that have the highest feature importance" on data Numerai does not name, possibly including our test eras.
5. Window length. Implemented: 3 windows of 52 eras with the 4-era gap. A model's per-era correlation has a standard deviation of about 0.015. So a window's mean has a standard error of 0.0021 with 52 eras, 0.0029 with 26 and 0.0042 with 13, against signals of 0.006-0.018.
6. Target. Implemented: `target_ender_20`, v5.2's main target (20-day horizon). Alternative: `target_ender_60`, the payout target since v5.3. It needs a 12-era embargo, is unresolved for eras 1228-1240, and correlates 0.47 with the 20-day target.
7. Version. The record names v5.2. v5.3 ("Quantum", July 2026, 807 new features, 3.3 + 5.7 GB) is now current, and Numerai still updates the v5.2 files weekly. Implemented: v5.2 as recorded. Moving to v5.3 needs a record rename and a new folder.
8. Reproducibility. The API serves only this week's files: older rounds return the same object. The definition pins the rows with `LAST_ERA = 1235`, and `download_description` gives the SHA-256 of our files. A later download reproduces the data only if Numerai never revises past eras. Keep the raw files (7.0 GB) in the rebuild skill's backup zip.
9. Missing values. Implemented: feature-eras filled with bin 2 become NaN (Numerai: "If data for a particular feature is missing for that era ..., then all values will be set to 2"). Inside populated feature-eras every bin holds 20.0% of the stocks (bin 2 at most 20.02%), so no single stock was filled. Alternative: keep Numerai's 2s, which keeps all features int8 (frame 1.6 GB instead of 3.4 GB).
10. `numerai28_6` is not added, because it is an older, era-less release of this data (see its section).
11. Framework notes (not patched):
   - The probe scripts call `discover_datasets(root)` strictly, so one half-written folder of another agent stops every probe. I ran them on a scratch root holding only a symlink to this folder.
   - `leak_probes.py` hard-codes LightGBM `n_jobs=8`, which `OMP_NUM_THREADS` does not override. I capped it with a wrapper that sets `n_jobs=2` before each fit.
   - Above 50M cells the bundle checks skip the duplicate-row and duplicate-column checks, so every `_1m` dataset needs them by hand.
   - `sync-notebooks --check` reports `numerai_v5_2: (unset) -> .../numerai_v5_2_1m/dataset.py`, which the orchestrator's sync sets.

### numerai28_6
**Outcome:** not added. It is an older, era-less release of the data in `numerai_v5_2`, which this run adds as `datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/`.
**Record judgment:** do not add: the same underlying data as `numerai_v5_2_1m` (guidelines: "Different versions / cuts of one underlying dataset are duplicates too"). Evidence:
- Provenance: the Kaggle dataset `numerai/encrypted-stock-market-data-from-numerai` is owned by Numerai. Its data card: "This is a sample of the training data used in the Numerai machine learning competition ... The data is cleaned, regularized and encrypted global equity data. The first 21 columns (feature1 - feature21) are features, and target is the binary class you're trying to predict." OpenML 23517 ("numerai28.6", uploaded 2016-07-07) names that Kaggle page as its source.
- Same task: `numerai_v5_2` is the same tournament and the same task (a stock's return relative to the market, from obfuscated features at a date), released in 2025 with the weekly `era` column.
- The record asks for that version: "We need to find a version with a timestamp (or treat it as forced IID)". The forced-IID fallback is not needed once the timestamped version is in the working copy.
- No time index: the file has no era, id or date column, and its row order holds no era blocks.
  - LightGBM trained on the first two thirds of the file scores ROC AUC 0.526 on the last third, the same as random 3-fold splits (0.525-0.528).
  - Block means vary as in a shuffled file: the target's sd is 0.0163 per 1,000 rows against a binomial 0.0158, and the features' spread is 1.01 times the IID value.
  - The time structure cannot be recovered.
**Data:**
- Kaggle file `numerai_training_data.csv`: 36.6 MB, created on Kaggle 2017-04-15.
- 96,320 rows x 22 columns: 21 floats with about 1,000 distinct values each, and a binary `target` (48,658 / 47,662). No duplicate rows.
- Downloaded to `local-data-warehouse/numerai28_6/` with `uvx --from kaggle==2.2.2 kaggle datasets download numerai/encrypted-stock-market-data-from-numerai`.
- Licence: CC0-1.0 (Kaggle data card).
- OpenML 23517 is the same sample re-encoded. It has the same shape and class counts, and its sorted feature-target Spearman correlations match the Kaggle file's within 0.0013. Its values and row order differ.
**Definition:** none.
**Checks:** none.
**Probes:** quick baselines only, since there is no definition. Random 3-fold ROC AUC: LightGBM 0.525-0.528, logistic regression 0.526-0.533.
**Verification:** upheld by the verifier. The OpenML copy and the Kaggle file are one sample re-encoded, and the duplicate call rests on provenance. Applied: the record comment and the Data line now say "re-encoded" instead of "another encryption or sample".
**Issues for Lennart:**
1. Mark the record `No` + `Duplicate` of `numerai_v5_2` (`numerai_v5_2_duplicate` under the `_duplicate` convention)? Nothing was implemented. The alternative is a forced-IID definition (`ForcedIIDFromTemporal`, binary, 96,320 x 21, ROC AUC about 0.53). A random split there mixes rows of the same unknown weeks, which share the market state.
2. Noted only (a licence is never a verdict reason): the 2016 Kaggle sample is CC0-1.0, while v5.2 falls under Numerai's Terms of Service, section 4.2 (see `numerai_v5_2`, issue 1).

### nyc_taxi_trip_duration

**Outcome:** added and checked

**Record judgment:** valid with concerns. The trips are NYC TLC yellow-cab records of January to June 2016, sampled
by Kaggle for its 2017 playground competition (data page, read with `kaggle competitions pages nyc-taxi-trip-duration
--content`: "The competition dataset is based on the 2016 NYC Yellow Cab trip record data made available in Big Query
on Google Cloud Platform. The data was originally published by the NYC Taxi and Limousine Commission (TLC). The data
was sampled and cleaned for the purposes of this playground competition."). 8 of 8 random training rows match NYC
Open Data "2016 Yellow Taxi Trip Data" (uacg-pexx) to the second and to the last digit of the coordinates (the
verifier matched 7 more). The task is published for prediction (Description page: "build a model that predicts the
total ride duration of taxi trips in New York City"). ETA at pickup with the destination known is a real application,
not a contrived target. No overlap with the working copy: it holds no NYC TLC data; delivery_eta_1m and
maps_router_eta_1m are Yandex data (TabReD), food_delivery_time is Indian food delivery, and
pkdd_15_taxi_trip_time_prediction_ii (this run) is Porto. The concerns (issues 1-3) are about which rows and which
source to ship, not about validity.

**Data:** Kaggle competition `nyc-taxi-trip-duration`, `train.zip` -> `train.csv` (1,458,644 rows x 11 columns,
sha256 fc8c777a4ab99a362d8b6b6f2038ff8a2c4625b9593248a47352d0d26fa99927) in
`local-data-warehouse/nyc_taxi_trip_duration/`. test.csv (625,134 rows, no target) was downloaded to the scratch
folder only, to check the competition's split. Licence: Kaggle competition rules (rules page, Sec. 7A: use "for the
purposes of the Competition, participation on Kaggle Website forums, academic research and education, and other
non-commercial purposes"; Sec. 7B: no redistribution). The same trips on NYC Open Data have no licence field
(Socrata metadata `license: null`).

**Definition:** `datasets/_dev/tabarena-v0pt2/nyc_taxi_trip_duration/`. `source = "Kaggle"` (the sample first
appeared in the competition; TLC provenance in `download_description` and `curation_comments`), `source_url` the
competition. Prediction point: the meter is engaged and the passenger has named the destination (ETA at pickup);
known: vendor, pickup time and point, dropoff point, passenger count. Target `log1p_trip_duration` (regression, rmse =
the competition's RMSLE). Temporal on `pickup_datetime`, `TemporalSplits(window=7, unit="days", n_windows=3)`: test
weeks 2016-06-24..30, 06-17..23, 06-10..16 (52,963 to 54,713 trips), train = all earlier trips (1.29M-1.40M, trimmed
to a random 1M per window). 1,451,706 rows x 7 features (vendor_id category, pickup_datetime datetime,
passenger_count, 4 coordinates). Cleaning: drop `id`, `dropoff_datetime` (= pickup_datetime + trip_duration in every
row), `store_and_fwd_flag` (set when the record is sent after the trip); drop 7 exact copies; take 3,600 s off the 86
kept trips across the daylight-saving switch (2016-03-13 02:00 -> 03:00); drop 4,782 trips under 30 s (no ride),
2,111 over 3 h (clock errors) and 38 with an end outside lon -75..-72, lat 40..41.5 (GPS errors); vendor codes mapped
to the names of the TLC data dictionary. Three `_decisions` tables (duration bands, the flag by vendor, the
daylight-saving night against the Sundays before and after), computed on the deduplicated, fixed trips.

**Checks:** `dataset check`: 0 errors, 0 warnings. Accepted: `splits_rows_unused` (129,675 trips, 8.9%, all before
2016-06-10, fall in none of the three random 1M train samples; issue 5). pandas 2.3.3 and 3.0.6 (scratch venv) give
the same checksum, v2:36e98eccb2b24405659fb7588b35beffb11b4bd48294cddafd85f3ed1fa5e3f8. ruff clean; the definition
imports. `pytest tests/test_v2_datasets.py -k nyc_taxi_trip_duration` fails at collection on another agent's folder
(`analcatdata_supreme`: domain and source "TODO"); the same test file pointed at a root holding only this folder
passes (2 passed, with `DATA_FOUNDRY_V2_DATA_CHECKS=1` the rebuilt checksum matches the README).

**Probes:** (scratch `probes2/`, after the fix round; untuned, 50k rows per side, 3 of 3 windows, 2 threads)
- Task probes: no flags. LightGBM R^2 0.621 (above the mean on 3 of 3 windows, SE 0.012), random forest 0.614,
  linear 0.119; best single feature `pickup_longitude` (chosen on all 3 training sides) 0.117; drift baseline skill
  0.002.
- Leak probes (datetime left out by the script): all features 0.671; depth-2 / depth-3 tree 0.185 / 0.227; each
  feature alone at most 0.117; without `pickup_longitude` 0.522 (the coordinates act together, as a distance);
  0.0% of test rows with an exact copy in train; 1-NN R^2 0.413. No leak signal.
- Generated-data probe: 0.6% of rows fit exactly against 0.6% for a shuffled target; no flag.
- hidden_groups / group_probes: not run (temporal task; the data holds no cab or driver id).
- Own checks (LightGBM, 200k training rows): weekly windows RMSE 0.425 / 0.414 / 0.434 with AutoGluon's date parts,
  0.380 / 0.365 / 0.378 with skrub's encoding (`tabarena_default`); random 3-fold 0.396-0.399 against 0.419-0.440
  weekly (same features, a random split is optimistic); 3 x 28-day windows 0.430 / 0.428 / 0.422.

**Verification:** (independent verifier, `verify/verify.md`: ready with noted concerns, no leak, no blocker)
- Finding 1 (major, the hour of day): applied. Confirmed in the code: `TabArenaV0pt1ExperimentBundle` runs the
  `default` pipeline (AutoGluon's timestamp, year, month, day, day of week; tabarena `bundle.py`),
  `BeyondArenaExperimentBundle` runs `tabarena_default`, whose `DateTimeFeatureGenerator` is skrub's
  `DatetimeEncoder(add_weekday=True, periodic_encoding="circular")`; with skrub 0.10.1 it emits year, total seconds
  and circular month, day, hour and weekday. Real skrub on the final frame: RMSE 0.380 / 0.365 / 0.378 against 0.425 /
  0.414 / 0.434. The Note bullet and issue 4 are rewritten; no hour column added.
- Finding 2 (minor, daylight saving): applied as a fix, not a drop. 97 trips span the switch, 86 kept; their recorded
  63-114 min become 3-54 min. On that night 86 of 472 kept trips picked up at 01:00-01:59 were recorded at 60 min or
  more, against 0 of 503 and 494 on the Sundays before and after; after the fix the median (10.6 min) and 75th
  percentile (17.0 min) match those Sundays (10.4-10.5, 16.0-16.1). A bullet and a third decision table record it.
- Finding 3 (minor, the host's "leakage" remark): applied. The host's full reply names no mechanism; the sentence now says so
  and gives the ETA framing (the dropoff point is recorded when the meter is disengaged, taken as the destination
  named at pickup).
- Finding 4 (minor, mixed bases): applied. The decision tables are now computed on the deduplicated, fixed trips, and
  the comment says 1,900 of the 2,111 (the daylight-saving fix moves one more trip out of the 22-24 h band) and 7,997
  trips at 1:00-1:20 h.
- Finding 5 (duration cut) and finding 6 (window length): no change; they stay issues 2 and 3 for Lennart, with the
  cross-run consistency question (zillow_prize keeps its target outliers; pkdd_15 cuts under 1 min and over 3 h).
- Finding 7 (zone IDs): confirmed by the verifier for 2012-06, 2015-01, 2016-01/03/06/07; 2009-01 still has
  coordinates. Folded into issue 1 and the record comment.
- Coordinator item (`source`): applied. dataset_patterns.md §A: `source` is where the data first appeared. This
  sample (its rows, the derived trip_duration, the column set) first appeared as the Kaggle competition, as the
  Kaggle cuts of public data in sdss_17 and cdc_diabetes_health_indicators, so `source = "Kaggle"`. The record's
  `original_source` still says "GOV Website" (issue 10).

**Issues for Lennart:**
1. **Kaggle sample or the primary TLC records?** The record says the TLC Parquet files serve coordinates up to
   mid-2016. They do not any more: the current files hold `PULocationID` / `DOLocationID` only (2016-01, 03, 06 read
   by me; 2012-06, 2015-01, 2016-07 by the verifier; 2009-01 still has coordinates). The 2016 coordinates survive on
   NYC Open Data (uacg-pexx, 131,165,043 trips in 2016, Socrata API; a bulk export of January to June would be tens of
   GB). Implemented: Kaggle `train.csv` (the published task, 1.46M trips, rows verified against uacg-pexx).
   Alternative: a `_1m` version built from uacg-pexx (all trips of a half-year, sampled per window; also free of the
   Kaggle no-redistribution clause).
2. **Target-selected row filters.** Trips under 30 s (4,782) and over 3 h (2,111) are dropped as data errors: under
   10 s 72% start and end at one point; over 3 h, 1,900 sit between 22 and 24 h, all VeriFone, at 0.1 km/h, and 14
   sampled TLC records of such trips carry fares of $5-$44.50 (or the $52 JFK flat fare). They hold a large share of
   the error: LightGBM RMSE 0.487-0.509 with all trips, 0.412-0.434 without (weekly windows); the verifier finds the
   same order of four model families with and without the cut. Alternative: keep them as the competition did (they
   are in its test set too; zillow_prize in this run keeps its target outliers), or cut only the 22-24 h cluster and
   the multi-day trips (RMSE 0.450-0.470 with only the over-3-h cut).
3. **Window length.** Implemented 3 x 7 days (weekly refit, as delivery_eta_1m and maps_router_eta_1m). Alternative:
   3 x 28 days (2016-04-08..05-05, 05-06..06-02, 06-03..06-30; 217k-232k test trips, train 780k-1.23M = 54-85%):
   LightGBM RMSE 0.422-0.430 against 0.419-0.440 weekly. It spans the spring-to-summer drift and uses every row (no
   `splits_rows_unused`). Calendar months are not possible: January to March holds 49.7% of the trips, under the 50%
   floor. pkdd_15 (this run) uses monthly windows.
4. **Time of day depends on the TabArena pipeline.** `tabarena_default` (skrub's DatetimeEncoder, the BeyondArena
   bundle) keeps the hour; `default` (AutoGluon's date parts, the v0.1 bundle) loses it. LightGBM RMSE 0.380 / 0.365 /
   0.378 against 0.425 / 0.414 / 0.434 on the weekly windows. The definition keeps the raw datetime. Question: which
   pipeline the v0.2 runs use; a harness change or an hour column is needed only for `default`.
5. **Train sides trimmed per window (framework).** The frame (1,451,706 rows) is under 1.5M, so it ships without
   `_1m`; its train sides (1.29M-1.40M) exceed 1M, so `cap_splits` draws an independent random 1M per window (overlap
   808k-839k) and 129,675 trips are in no split. The `_1m` mechanism (`sample_temporal_splits`: one random order,
   frame reduced to the used rows) is refused for a name without `_1m`. First such case in the working copy; accepted
   with a reason for now. Alternative: allow `subsample_to_budget` for temporal frames under 1.5M rows whose train
   sides exceed the budget.
6. **`store_and_fwd_flag` dropped.** TLC dictionary: the record "was held in vehicle memory before sending to the
   vendor ... because the vehicle did not have a connection to the server"; the record holds the dropoff time, so it
   is sent after the trip. Y for 8,045 trips, all Creative Mobile Technologies. Effect: RMSE 0.424 / 0.418 / 0.437 with
   it, 0.425 / 0.419 / 0.440 without. Alternative: keep it, as the competition's test.csv does.
7. **Daylight saving fixed, not dropped.** 86 kept trips lose 3,600 s (evidence under Verification). Alternative:
   drop them (0.006% of the rows, all in train sides).
8. **Licence (note only).** Kaggle rules: non-commercial use, no redistribution (Sec. 7A, 7B). The trip records
   themselves are public on NYC Open Data without a licence field.
9. **Domain.** The record's "Other" has no match; `industry & manufacturing` follows the two ETA datasets of the
   working copy. Alternative: `business & marketing` (food_delivery_time).
10. **Record fields.** `original_source` says "GOV Website"; the definition now says "Kaggle" (the sample first
    appeared there, as sdss_17 and cdc_diabetes_health_indicators). `v2_path` is unset until `sync-notebooks` runs.
    The repo-level pytest fails at collection until `analcatdata_supreme` imports.

### onlinenewspopularity
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/onlinenewspopularity/`), revised after the verifier's
review (needs changes -> all findings applied).

**Record judgment:** valid with concerns. The data first appeared at UCI (dataset 332, DOI 10.24432/C5NS3V), donated
by the authors of Fernandes, Vinagre and Cortez, EPIA 2015 (LNCS 9273, pp. 535-546; open copy
http://hdl.handle.net/1822/39169). It is a predictive task by design: "the IDSS first predicts if an article will become
popular" (abstract), evaluated with rolling windows (Sec. 2.3 and 3.1). No duplicate: no other record or working-copy
folder holds Mashable / UCI 332 / OpenML 4545 data (grep for mashable, online news, C5NS3V, 4545, 46652, 46662,
n_tokens, kw_avg_avg). The record's OpenML links 46652 (`news_channel`) and 46662 (`news_popularity2`) are the AutoML
multimodal benchmark's derived tasks (Shi et al. 2021: the article title plus a few numeric columns), not the original.
The `NLP (Text)` / `Wrong Domain / Source Modality` markers: the curator accepted them ("I think we cannot get the
original text but this is still fine"), and the data supports that: the 19 text-derived columns left after the LDA drop
add R^2 0.003 (0.155 without, 0.158 with) and reach 0.041 alone; `Wrong Domain / Source Modality` is not borne out.

**Data:** UCI static zip https://archive.ics.uci.edu/static/public/332/online+news+popularity.zip (7,476,401 bytes,
sha256 dba2ae52...; files dated 2015-05-31) in `local-data-warehouse/onlinenewspopularity/`:
`OnlineNewsPopularity/OnlineNewsPopularity.csv` (39,644 rows x 61 columns) and `.names`. Licence CC BY 4.0 (the
"License" box of the UCI dataset page); the article texts belong to Mashable (UCI: "this dataset does not share the
original content but some statistics associated with it").

**Definition:** temporal regression. Prediction point: before publication (the paper's system "analyzes articles prior
to their publication"; its features are "known prior to an article publication", Sec. 4). Target `log_shares` = ln of
the shares at the 2015-01-08 crawl (1 to 843,300, median 1,400). Time column `publication_date`, parsed from the URL.
Splits: `TemporalSplits(window=2, unit="weeks", n_windows=9, gap=1)`: 9 two-week windows from 2014-08-24 to
2014-12-27 (769 to 1,001 test articles each), train is everything at least one week before each window (30,967 to
38,385 rows, at least 78%). 39,643 rows x 40 features. Main cleaning: URL -> publication date (then dropped);
`timedelta`, the 7 weekday flags and `is_weekend` dropped (issue 2); the 5 LDA columns dropped (issue 3); the 6
channel flags merged into a categorical `data_channel` (6,134 articles with no flag are `other`); one article with
failed text processing dropped (ukraine-civilian-convoy-attacked); proxy values set to missing (body statistics of the
1,181 articles without body words, polarity statistics without polar words, self-reference statistics whenever their
maximum is 0 (7,174 articles), keyword statistics of the first day and every negative keyword value); the broken
`n_non_stop_words` dropped. pandas 2.3.3 and 3.0.6 give the same checksum.

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); no accepted warnings. `pytest
tests/test_v2_datasets.py -k onlinenewspopularity` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed (collection failed
twice during the first round because other agents' scaffolds had `domain = "TODO"`; not this folder).

**Probes** (after the revision; scripts run with `--root` on a scratch folder holding a symlink to this folder):
- leak_probes (3 newest windows, untuned LightGBM): all features R^2 0.134; depth-2 / depth-3 tree 0.082 / 0.100; best
  single features `kw_avg_avg` 0.079, `data_channel` 0.063, `kw_max_avg` 0.046; dropping any one of them changes R^2 by
  at most 0.007; no missing-value indicator above 0; 0.0% exact copies; 1-NN R^2 below 0. No leak signal.
- task_probes (`--splits 9`, all 9 windows): dummy 0, drift +0.009, linear +0.109, random forest +0.154, LightGBM
  +0.160 +- 0.033 skill (R^2 0.149), beats the dummy on 9 of 9; best single feature per window (`data_channel` 5x,
  `kw_avg_avg` 4x) +0.079. Flags: none.
- generated_probes: exact fit 1.9% against 2.1% for a shuffled target; flags: none.
- hidden_groups / group_probes: not applicable (temporal task).
- My LightGBM runs on the 9 shipped windows (fixed settings, mean of seeds 0-2; `experiments_v2.py`, `exp_v2_*.txt`):
  R^2 0.158 (0.10 to 0.21 per window); plus the 5 LDA columns 0.158 (0.1580 vs 0.1582); without keyword statistics
  0.135; without self-reference statistics 0.143; without the date parts 0.158; plus the authors' `timedelta` and
  weekday flags 0.166; plus a TF-IDF of the URL slug 0.152; without the 19 text-derived columns 0.155, those alone
  0.041; gap 0 weeks 0.160, gap 3 weeks 0.153; binary (shares >= 1,400) ROC AUC 0.733 (0.731 without text-derived
  columns; paper: 0.73).

**Issues for Lennart:**
1. **Target: regression or the paper's binary task?** The paper and UCI frame "popular" as shares above D1 = 1,400
   (Sec. 3.1, p. 7; UCI's class table counts 1,400 itself as popular, the paper's text says "higher than"; 1,592
   articles have exactly 1,400). Implemented: regression on ln(shares), which keeps that split and the order within
   each class (R^2 0.158; OpenML 4545 and AutoML_MM also use the count). Alternative: binary target in a second folder
   `onlinenewspopularity_clf` (ROC AUC 0.733 on the same windows; the paper's random forest 0.73).
2. **UCI's `timedelta` and weekday flags do not follow the publication date.** The flags are the weekday of 2015-01-08
   minus `timedelta` in 100% of the rows, but that date falls 1 to 5 days after the date in the URL for 9,463 articles
   (24%; every article of December 2014; in late 2014 it looks like the next working day of the authors' pipeline: all
   60 articles of Friday 2014-12-05 carry Monday 12-08). Mashable's own pages carry the URL date (Wayback snapshots of
   2014-12-31: star-wars-the-force-awakens-character-names "Thu, 11 Dec 2014 21:11:08 +0000", authors' date Dec 15;
   rape-threats-contact-mothers "Mon, 01 Dec 2014 08:20:04 +0000", authors' date Dec 3; three current pages agree).
   The shift goes with the outcome (within a URL date, shifted articles +0.038 log shares, unshifted -0.010; before
   April 2014 +0.205 for 427 articles), and adding the flags and `timedelta` raises R^2 from 0.158 to 0.166.
   Implemented: dropped; the weekday comes from `publication_date` (skrub `DatetimeEncoder(add_weekday=True)` in
   `tabarena_default`, `dayofweek` in AutoGluon's generator). Alternative: keep the published flags. Every copy of this
   dataset (UCI, OpenML 4545, benchmarks built on them) carries this.
3. **LDA columns: dropped (verifier's finding 2).** The paper: LDA "was applied to all Mashable texts (known before
   publication)" (Sec. 2.1, p. 4); each channel loads on the same topic in both years (business 0.64-0.67 on LDA_00 in
   every quarter, world 0.65-0.72 on LDA_02, tech 0.67-0.71 on LDA_04), so one model, by the paper's wording fitted on
   all texts, test windows included: a transform fitted on the full set (rubric item 6). The five columns carry no
   measurable signal (R^2 0.1580 with, 0.1582 without, 3 seeds; in the untuned model of the leak probe -0.004 to +0.002).
   Alternative: keep them with a note (my first version; the record's first comment suspected a leak).
4. **Windows and gap.** Implemented: 9 x 2 weeks with a one-week gap, after the paper's rolling test sets of 1,000
   articles (two to three weeks) and its remark that shares of some articles younger than 4 days had not settled (Sec.
   2.1, p. 3). Alternatives and R^2: no gap 0.160; a three-week gap (the paper's discard rule) 0.153; monthly windows
   would put the oldest test window in April 2014 (not run).
5. **Keyword statistics: kept as a potential leak (verifier's finding 1).** They summarize the articles with an
   earlier authors' date (issue 2), so for the 24% of shifted articles they include same-day articles, some published
   hours later: yahoo-qwiki-brief (2013-07-03 13:37 UTC, authors' date 07-04) holds `kw_max_max` 843,300, the shares
   of low-cost-iphone (19:07 UTC that day), and none of the 66 unshifted articles of that day holds it. Never a later
   day. 4,031 of 8,289 test rows (49%) have same-day articles in their pool (median 32, at most 94). Diff-in-diff over
   15 two-week windows of 2014: the keyword columns lower the MSE by 0.0245 for shifted and 0.0172 for unshifted test
   articles, difference 0.007 (SE 0.006, 8 of 15 windows above 0; the verifier's run on the first version: 0.0007, SE
   0.0044), against an MSE of about 0.66: not distinguishable from 0. They also use the 2015 crawl's share counts.
   Alternative: drop the nine `kw_*` columns (R^2 0.158 -> 0.135); the paper's most important feature is `kw_avg_avg`.
6. **Self-reference statistics: kept as a potential leak.** They come from the page at the crawl, so a link added after
   publication can point to a newer article: ionut-budisteanu-self-driving-car (2014-04-08) holds 663,600, the shares
   of first-100-gilt-soundcloud-stitchfix (2014-04-09). Of 906 articles whose self-reference minimum or maximum equals
   one of the 136 share counts of 50,000 or more held by one article, 4 are 1-2 days older than it (47 more are 6+ days
   older, likely other pages with the same count). Alternative: drop them (R^2 0.158 -> 0.143).
7. **Text.** Every URL still resolves (to mashable.com/archive/<slug>), the slug holds title words, and AutoML_MM's
   OpenML 46662 has full titles for 24,007 articles. A TF-IDF of the slug adds nothing (R^2 0.152 vs 0.158), so no text
   column. A text variant (titles or bodies) would need a scrape of Mashable's pages (Mashable holds the rights).
8. **Record fixes to consider:** add UCI 332 / OpenML 4545 as the canonical links (the OpenML links are AutoML_MM's
   derived tasks), `problem_type` (regression, or as decided in issue 1), and the modality markers (the data does not
   support `Wrong Domain / Source Modality`). The `.names` file says 39,797 instances; the CSV and its class table hold
   39,644 (the paper rounds to 39,000). Label maturity was checked: the 481 articles under three weeks old at the crawl
   show no deficit of shares (last week median 1,600, 65% at 1,400 or more; the 8 weeks before: 1,100-1,400, 42-52%).

**Verification:** (verifier's review of 2026-10-07, `verify/verify.md`; verdict "needs changes")
- **Verification:** finding 1 (major, keyword statistics include later same-day articles): applied. Reproduced on the
  raw file (yahoo-qwiki-brief is the only one of the day's 67 articles with 843,300; 4,031 of 8,289 test rows; no
  later-day article in the test period); the bullet is rewritten with the mechanism, the proof case and a diff-in-diff
  re-run on the revised definition (difference 0.007, SE 0.006); kept as `Potential leak, kept on purpose`; dropping
  the block is issue 5.
- **Verification:** finding 2 (major, drop the LDA columns): applied. Three seeds on the revised definition confirm no
  signal (0.1580 with, 0.1582 without); bullet and Decision 2 now explain the drop.
- **Verification:** finding 3 (minor, self-reference zeros of linking articles): applied, mask on
  `self_reference_max_shares == 0` (1,824 linking articles plus 5,350 without links = 7,174; a positive maximum never
  comes with a minimum of 0).
- **Verification:** finding 4 (minor, negative `kw_avg_min` values): applied, every negative keyword value is masked
  (833 in `kw_avg_min`: 694 at -1 and 139 other negatives); the bullet says positive averages can still include -1.
- **Verification:** finding 5 (minor wording): applied. 1e-7 for `n_non_stop_words` (100% within 1e-7, 90.8% within
  1e-8); the Decision 1 table now has the before-April-2014 columns (427 articles, +0.205); the self-reference claim is
  rewritten with the 663,600 case and the verifier's 906 / 4 / 47 count (reproduced); the LDA wording now separates the
  stability evidence (one model) from the paper's wording (all texts). While checking finding 3, the one article with
  a self-reference minimum above its maximum (ukraine-civilian-convoy-attacked) turned out to be a failed text
  processing in many columns (counts instead of rates, all LDA and sentiment values 0 for 1,570 words,
  `abs_title_subjectivity` inconsistent): the row is now dropped instead of masked.
- **Verification:** finding 6 (Lennart's call, regression vs binary): no change; numbers in issue 1.
- **Verification:** finding 7 (info, modality markers): numbers added to the record judgment and issue 8.
- **Verification:** finding 8 (info, `timedelta` mechanism): wording added (next working day of the authors' pipeline,
  the 2014-12-05 example); the drop stands, since the authors' date is not known before publication and goes with the
  outcome.

### open_university_learning_analytics_dataset

**Outcome:** added and checked

**Record judgment:** valid with concerns. The data is the OU's own release (Kuzilek, Hlosta, Zdrahal, Sci. Data 4:170171,
2017; first published on analyse.kmi.open.ac.uk in 2015), unique in the working copy and the records. The three
education datasets in the copy come from other sources: early_learning_predictors (DataFirst), predict_students_dropout_and_academic_success
(UCI, 10.24432/C5MC89) and student_portuguese_performance (UCI, 10.24432/C5TG7T). Grepping `curation/records/` for OULAD, "Open University",
C5KK69, kmi.open, figshare 5081998 and sdata.2017.171 finds only this record. The concerns are that the source
publishes no single task, so the prediction point, the target framing and the split are our choices (issues 1-4).
One presentation, BBB 2014J, changed how it marks (issue 9). The record also points to a Kaggle notebook whose
features leak the outcome (issue 6).

**Data:** the authors' figshare deposit of the OU release,
`https://ndownloader.figshare.com/files/8606371` (anonymisedData.zip, md5 7412686fd77cf0e0ee1e8c3e9b354308, DOI
10.6084/m9.figshare.5081998.v1, the paper's "Data Citation 1"). It holds seven CSVs, 464 MB:
- studentInfo 32,593 rows
- studentRegistration 32,593 rows
- assessments 206 rows
- studentAssessment 173,912 rows
- vle 6,364 rows
- studentVle 10,655,280 rows
- courses 22 rows

The OU's own download is dead (2026-10-06). Its dataset page (research.stem.open.ac.uk/ouanalyse/open-dataset-more/) has
a "Download dataset" button with no href, and the old file URL schools.stem.open.ac.uk/cdn/files/anonymisedData.zip
returns 404. The UCI copy (static/public/349) is byte-identical after replacing its "?" with "". Licence: CC BY 4.0,
stated on the OU dataset page ("This dataset is released under CC-BY 4.0 license"), in the paper's abstract and on
figshare.

**Definition:**
- Folder: `datasets/_dev/tabarena-v0pt2/open_university_learning_analytics_dataset/`.
- Prediction point: day 60 of the module-presentation (presentations last 234-269 days). The use case is OU Analyse,
  "early identification of students at risk of failing", updated weekly for tutors.
- Target: `final_result` with the source's 4 classes (Pass 12,358 / Fail 7,040 / Withdrawn 3,973 / Distinction 3,024),
  metric log_loss. The paper names "final course results" for predictive models.
- Regime: grouped by `module_presentation` (22 groups, `per_sample`, unit row, context all_rows), 3 repeats x 3 folds,
  6-9 test presentations per fold, train 15,832-18,701 rows, test 7,694-10,563 rows.
- Size: 26,395 rows x 40 features, plus the group key.

Main cleaning decisions:
- **Cohort:** the registrations active on day 60. We drop 6,190 that ended before day 60 (their result, Withdrawn, is
  already known) and 8 made after it.
- **Assessment features:** due count, submitted count and mean days early for the assessments due before day 60;
  score mean and minimum for the scores known on day 60 (a CMA when submitted, a TMA 14 days after the later of
  cut-off and submission, banked results from the start); banked count. BBB 2014J's 1/100 first-TMA marks are kept as
  recorded (issue 9).
- **VLE features:** pre-start clicks; clicks per activity type on days 0-59 (19 types); active days; clicks in the last
  14 days; days since the last click.
- **Dropped columns:** `id_student`, `date_unregistration` (post-outcome in the cohort), `code_presentation` (the year
  is the time index; the start month is kept as `presentation_start`), `module_presentation_length` (it names the
  presentation).
- **Other:** imd_band "10-20" is written "10-20%". Two `_decisions` tables show the train share per start date and the
  cohort by result.
- **pandas:** 2.3.3 and 3.0.6 give the same checksum (v2:7c805bb1…, after the verification edits) and the same data
  fingerprint as before them.
- **Tests:** ruff is clean; `pytest tests/test_v2_datasets.py -k open_university...` passes, including the rebuild with
  `DATA_FOUNDRY_V2_DATA_CHECKS=1`.

**Checks:** 0 errors, 0 warnings, 1 info.
- Accepted `groups_test_groups_few` (6-9 test presentations per fold). Reason: the 22 presentations are all the source
  has, and holding them out is the use case. Each fold still scores 7,694+ registrations one by one (smallest class 874
  rows), and the group probes show real signal across presentations. The reason now also names BBB 2014J as the source
  of most of the variance between folds.
- Info `dataset_conflicting_duplicate_rows`: one pair of BBB 2013J students has the same profile and no activity before
  day 60, with results Fail and Withdrawn. Kept as genuine ambiguity, with a bullet.

**Probes** (2 threads each; outputs in `probes/`):
- **Leak:**
  - all features 0.728 macro AUC; shallow tree 0.651 / 0.684.
  - Best single feature: score_mean 0.671, then score_min 0.656 and days_since_last_click 0.636.
  - Drop-one costs at most 0.006, and missingness indicators reach at most 0.543.
  - 0.0% exact copies across the split; 1-NN agreement 0.418 against chance 0.326. No flag.
- **Task:** no flags.
  - Dummy log loss 1.240.
  - Skill: random forest 0.158 +- 0.026 (beats the dummy on 100% of the splits), LightGBM 0.138, linear 0.089,
    best single feature -0.015.
  - Spread RF - linear 0.068 (paired SE 0.022). Smallest class per test fold: 874.
- **Generated:** 0 rule leaves, no flags.
- **Group** (`group_probes.py`):
  - LightGBM macro AUC 0.770 IID against 0.747 grouped (gap 0.023).
  - On unseen presentations: logistic regression 0.717, random forest 0.745, LightGBM 0.744, kNN 0.634 (baseline 0.5).
- **Own regime probes** (`regimes.py`, untuned LightGBM, 4-class log-loss skill over the prior):
  - IID 0.193, grouped 0.141 (9 splits), temporal hold-out (train 2013B-2014B, test 2014J) 0.099.
  - On the same 2014J rows, the first grouped repeat scores 0.070.
- **Student overlap** (`student_overlap.py`, `overlap_kind.py`): 12.9% of grouped test rows have the same student on
  the train side. Removing those train rows raises their log loss 1.117 -> 1.144, against 1.124 for a control removal.
  That is about 0.0025 log loss overall. Kept on purpose with a bullet (issue 5).

**Issues for Lennart:**
1. **Split regime: grouped by module-presentation, not temporal.**
   - Why it matters: deployment trains on earlier presentations. The OULAD page: "the J presentation must be used to
     inform the B presentation or vice versa". The data has only 4 start dates. The share of rows before
     2014J / 2014B / 2013J is 66.5% / 43.1% / 14.9%, so only one window keeps half of the data for training, and the
     protocol needs 3.
   - Label availability adds to this. A February presentation cannot train on the October one before it, which is
     still running (J runs to June/July), so the 2014B and 2013J windows could only train on 2013B (3 modules).
   - Numbers: IID 0.193, grouped 0.141, temporal 2014J hold-out 0.099. The grouped split is slightly optimistic for the
     older presentations: on 2013J and 2014B test rows, removing the later presentations from the train side costs
     0.010 skill more than removing as many random train rows (9 of 13 cases; verifier's `v8b`). On the 2014J rows it
     is harder than the hold-out (0.070).
   - Implemented: grouped.
   - Alternative: temporal by start date, `TemporalSplits(window=1, unit="months", cutoffs=("2013-10-01",
     "2014-02-01", "2014-10-01"), gap=5)` on a start-date column. Two of its three windows train on 14.9% of the rows,
     which breaks the 50% rule.
2. **Prediction day.**
   - Implemented: day 60.
   - Alternatives (one grouped repeat, LightGBM, rows / 4-class skill / at-risk AUC):
     - day 0: 29,681 / 0.031 / 0.690
     - day 30: 27,510 / 0.068 / 0.752
     - day 60: 26,395 / 0.132 / 0.803
     - day 90: 25,588 / 0.202 / 0.844
   - OU Analyse itself predicts weekly whether the next assignment will be failed. That task needs one row per student
     and assignment, and it would allow a real temporal split with calendar windows.
3. **Target framing.**
   - Implemented: the source's 4 classes (log_loss).
   - Alternative: binary at risk (Fail or Withdrawn against Pass or Distinction; 41.7% positive). On the same folds it
     gives AUC 0.805 and log-loss skill 0.207, against an at-risk AUC of 0.803 from the 4-class model.
4. **TMA marking delay.**
   - Implemented: a TMA score is used only 14 days after the later of cut-off and submission. This follows the OU
     Tutor Support Statement (approved April 2012, updated July 2019): feedback "normally within ten working days of
     assignment deadlines, or ten working days after the date of any agreed extension, whichever is the later". The
     data does not say when a 2013-2014 TMA was returned. CMA scores count from submission ("iCMAs are marked
     automatically"); waiting for the cut-off changes LightGBM skill by 0.0003 +- 0.0025.
   - Alternative: no delay. Skill 0.158 instead of 0.132 (one grouped repeat).
5. **Students recur across the split** (a potential leak, kept).
   - 3,619 rows belong to students registered in several periods and 1,148 to students on two modules in one period.
     12.9% of grouped test rows have the same student, with the same profile, on the train side.
   - For 7.9% of all rows that is a concurrent or later registration, which deployment would not know (for 1,312 of
     3,387 overlap rows it is only earlier registrations, which deployment would know).
   - Effect: about 0.0025 log loss over all test rows (control experiment).
   - No grouping removes it, because all 22 presentations are linked by shared students.
   - Alternative: keep one registration per student, which drops 2,384 rows and changes the cohort.
6. **Record pointers to fix** (I did not edit the record).
   - `problem_type: TBD` should become Multiclass Classification, and `required_split: '?'` should become grouped. The
     tags say "Non-IID (Temporal)"; the definition is grouped (issue 1).
   - The record's comments propose following Kaggle notebook devassaxd/student-performance-prediction-complete-analysis.
     That notebook drops Withdrawn students and uses whole-presentation aggregates including the final exam score,
     so its features leak the outcome. We keep its target only.
   - `source_links` could add the figshare DOI, since the OU download is dead.
7. **Accepted warning `groups_test_groups_few`.** It is accepted with the group-probe evidence; please confirm.
   - This is the only dataset in the copy that accepts it: 22 groups, 6-9 per test fold. The next fewest is
     electric_motor, with 69 groups and 23 per fold.
   - The verifier supports the grouped split: new rows always come from a presentation nobody has finished, and no
     shipped split holds out a whole module, so covertype's IID precedent (3 areas) does not carry over.
   - Its cost is fold variance, concentrated in BBB 2014J (issue 9).
8. **Minor metadata choices.**
   - `year = "2015"`: the first release. The data covers 2013-2014 and the paper is from 2017.
   - `source = "Other"`: the OU website.
   - `source_url`: the figshare DOI, not the UCI DOI the record lists first.
   - `data_tags = ("Spatial",)`: for `region` and `imd_band`.
9. **BBB 2014J changed how it marks.** Harmonise its marks or keep them?
   - Evidence: its first TMA (cut-off day 19, weight 0) is marked 1 or 100: 1,739 of its 1,772 scores. In the other
     BBB presentations that TMA has weight 5 and is graded, and 52-71% of the students marked 40 or less there fail.
     In BBB 2014J, 732 students are marked 40 or less, and 52% of them pass, 10% with distinction. On day 60 it is the
     presentation's only known score.
   - Its VLE was rebuilt too: clicks_oucontent averages 93 against 0.4-7, and clicks_forumng 42 against 145-237.
   - Effect: LightGBM scores below the class prior on it (skill -0.42; random forest -0.07). The three weakest splits
     (0.06-0.09 against 0.16-0.19) are the three that test it.
   - Implemented: the marks kept as recorded, with an Anomaly bullet. A deployed model meets such redesigns.
   - Alternative: leave weight-0 TMA marks out of score_mean and score_min. This changes 1,655 cohort rows (1,652 of
     them BBB 2014J). On the 9 shipped splits:
     - LightGBM 0.141 -> 0.167 (standard deviation over the splits 0.052 -> 0.016; BBB 2014J -0.42 -> 0.02);
     - random forest 0.168 -> 0.158 (BBB 2014J -0.07 -> -0.24).
     - Reproduced in `followup/v7_rerun.txt`.
10. **Group context.** Set to `all_rows`, as for force_2020: on day 60 every registration of the running presentation
    is known with its day-60 features. It lets a model compare a student with the cohort, which is where BBB 2014J's
    rebuilt VLE hurts. The alternative is `none` (each row on its own).

**Verification** (independent verifier, 2026-10-07: needs changes in comment text only; data, cohort, features and
splits pass, and scrambling everything recorded from day 60 on changed 0 feature cells):
1. **BBB 2014J marking (major):** applied. I added an Anomaly bullet with the numbers, recomputed from the raw files and
   the verifier's script (`followup/bbb2014j.py`, `followup/v7_rerun.txt`, identical results). Harmonising is issue 9
   for Lennart.
2. **Unsupported split sentence (minor):** applied.
   - The 2014J comparison is replaced by the measured optimism for older presentations (0.010 skill, 9 of 13 cases) and
     the hold-out comparison on the newest (0.070 against 0.099).
   - "result rates" is replaced by the presentation-specific relation between features and results; module and start
     month alone give skill 0.008.
3. **Marking-time sources (minor):** applied.
   - It now cites the Tutor Support Statement (approved April 2012, updated July 2019; quote checked in the PDF) and
     the iCMA sentence of the 2025 policy summary (p. 3).
   - It adds the early-CMA sentence. My count is 2,975 registrations with an early CMA score (2,974 in FFF); the
     verifier's 2,912 counts those whose score_mean changes. The effect is 0.0003 +- 0.0025.
4. **Group context (minor):** applied. `context="all_rows"`, with the reason in `Grouping.definition` (issue 10).
5. **`groups_test_groups_few` (Lennart's call):** kept as accepted, and issue 7 now carries the verifier's facts. The
   accepted reason names BBB 2014J as the source of the fold variance.

After the edits: dataset check gives 0 errors, 0 warnings, 1 info. ruff is clean, pandas 2.3.3 and 3.0.6 give the same
checksum (v2:7c805bb1…), pytest passes (2 tests, with the rebuild), and no TODO is left. The data fingerprint is
unchanged: only the metadata and the comments changed.

### perth_house_prices
**Outcome:** added and checked (fix round after verification done: comments, record comment and one evidence table; the data are unchanged)

**Record judgment:** valid with concerns.

Provenance is traceable:
- The Kaggle data card (syuzai/perth-house-prices, 2021-01-31) says the rows were "scraped from http://house.speakingsame.com/". The site is real and archived on web.archive.org, and its pages say "The property data is from the auction results and realestate websites".
- The uploader added coordinates from G-NAF (data.gov.au) and school ranks from bettereducation.com.au.
- OpenML 43822 is the same table: 19 columns, 33,656 rows, the same missing counts (GARAGE 2,478, BUILD_YEAR 3,155, NEAREST_SCH_RANK 10,952).

It is unique:
- No other Perth data is in the working copy or the records (grep for perth, 43822, syuzai, speakingsame).
- No other unit of this run holds it; melbourne_housing_market is Domain.com.au data for another city.
- The Kaggle dataset heptix/perth-property-prices (2024) is a different scrape of sold listings. It shares 1,824 sales with this file and is not in the records.

Scope: sale-price regression with a temporal split, not forecasting.

The concerns change what the task measures, but none is a leak:
- the scrape's sampling (issue 3);
- an undocumented price cap (issue 1);
- test-period records older than the sale (issue 2);
- pre-build sales (issue 4).

**Data:**
- Kaggle `syuzai/perth-house-prices`, file `all_perth_310121.csv` (sha256 e9f334588eaaa6d4a82b89900dd7bd2abfe7644fd9ee9acb238d022eec4f9aff), in `local-data-warehouse/perth_house_prices/`.
- 33,656 rows x 19 columns; sales dated by month from April 1988 to December 2020.
- Licence: CC BY-NC-SA 4.0 (Kaggle API metadata `"licenses": [{"name": "CC-BY-NC-SA-4.0"}]`; OpenML 43822 states "CC BY-NC-SA 4.0"). The scraped site's own terms are not stated.
- Kaggle discussions (read with `uvx --from kaggle==2.2.2 kaggle`): 3 threads. The only substantive one is 383033, a course synopsis: "Only the most recent sale date was used"; "several observations were found to contain old or inaccurate data".

**Definition:** `datasets/_dev/tabarena-v0pt2/perth_house_prices/`.
- Prediction point: a property sells, and an automated valuation model refit at the start of every month on all earlier sales predicts its price. It uses the property as listed (bedrooms, bathrooms, car spaces, land and floor area, build year), its address and its location.
- Target: `log_PRICE` = ln(PRICE); metric RMSE.
- Regime and splits: temporal on `DATE_SOLD` (the month, parsed to its first day). `TemporalSplits(window=1, unit="months", n_windows=9)`: 9 monthly windows, December back to April 2020 (3 x 3, as an IID task of this size would get). Test sides hold 284-628 rows; train sides 28,958-32,678 rows (88-99%).
- Shape: 33,090 rows x 18 features (the date included).
- Types: SUBURB (321), POSTCODE (114), NEAREST_STN (68) and NEAREST_SCH (160) are categorical; ADDRESS is a string; the rest are numeric. Tag `Spatial`.
- Cleaning:
  - drop the 563 sales (1988-2016) dated before the year the house was built;
  - drop 3 copies of two sales that differ only in their coordinates (123 Fairway, Crawley x3; 4 Carmel Road, Carmel x2);
  - strip the carriage return in DATE_SOLD;
  - set LAND_AREA 999999 (3 rows) and GARAGE 99 (1 row) to missing;
  - read only "NULL" and empty fields as missing.
- `_decisions` shows five tables: the price cap (new), pre-build sales, per-suburb coverage, end-of-year monthly counts and address types.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info.
- One accepted warning, `meta_time_horizon_mismatch`: DATE_SOLD holds the first day of the sale month, so each one-month window holds one date and its span reads as 1 day. zillow_prize accepts the same warning for the same reason.
- pandas 2.3.3 and 3.0.6 give the same checksum, v2:58d51b1a...9b11 (the README's). The fix round changed the comments, which the checksum covers; `_clean` is unchanged.
- `pytest -q tests/test_v2_datasets.py -k perth` with `DATA_FOUNDRY_V2_DATA_CHECKS=1`: 2 passed.
- `dataset list --root datasets/_dev/tabarena-v0pt2` exits 0 and shows the dataset as checked; `load_definition` imports it.
- ruff check and format are clean; no TODO is left.

**Probes:** run on a one-folder root (a symlink in the scratch folder) with `--n-jobs 2`.
- `leak_probes.py` (3 newest windows):
  - all features: R² 0.842; depth-2 / depth-3 tree: 0.414 / 0.493;
  - best single features are locations: SUBURB 0.615, NEAREST_SCH 0.498, POSTCODE 0.472; FLOOR_AREA 0.355;
  - dropping any of the top three costs at most 0.001;
  - missing-value indicators alone: R² ≤ 0.01;
  - exact feature copies across the split: 0.0%;
  - 1-NN R²: 0.703 for the closest tenth, 0.599 for all rows.
  - No leak signal.
- `task_probes.py`:
  - On 5 windows: LightGBM R² 0.861; on all 9 (verifier): 0.863.
  - Best single feature (POSTCODE): 0.467 on 5 windows, 0.492 on 9.
  - No flags.
- `generated_probes.py`: 0.7% of rows fitted exactly, the same as for a shuffled target; no flags.
- `hidden_groups.py` skips temporal tasks. No property repeats within a suburb.

**Issues for Lennart:**
1. **The target is capped at $2,440,000 (new, from the verifier; reproduced).**
   - Evidence:
     - No sale in the file is above $2,440,000, and the yearly maximum is $2.40-2.44M in every year 2011-2020.
     - The counts fall smoothly to 46 sales between $2.3M and $2.4M (45 after cleaning) and 11 between $2.4M and $2.44M, then stop.
     - The site lists dearer sales: 17 McNeil Street, Peppermint Grove, "Sold $5,200,000 in Jun 2013" (archived 2022-08-10).
     - heptix/perth-property-prices has 75 of 5,072 houses sold in 2015-2020 (1.48%) above the cap. Among the 2018-2020 sales of all types it has 40% of Peppermint Grove's 15 and 48% of Dalkeith's 25 above it.
     - Dalkeith's median here is $2,039,000 (55% of its sales at $2M or more). Peppermint Grove has 41 rows and none after March 2018.
     - The 7 suburbs with 13-55% of their sales at $2M or more hold 45 of the 4,132 test rows, and 29 test rows are at $2M or more.
   - Implemented: keep, with an `Anomaly:` bullet and a decision table. This source cannot give the missing sales back.
   - Question: is a task "price of a sale up to about $2.44M" acceptable? §D.6 asks to document a capped target; cirrhosis is a precedent for a recorded selection.
2. **In the test period the site's record of a house is often older than the sale (new, from the verifier; reproduced).**
   - Evidence: of the 1,824 sales shared with heptix's sold listings, bedrooms or bathrooms differ in:
     - 0.7% of 2007-2016;
     - 2.8% of 2017-2018;
     - 12.1% of 2019;
     - 27.0% of 2020.
   - The file nearly always has fewer: in 2020, fewer in 22.9% and more in 4.3%. The step comes in mid-2019: 5.7% and 2.3% in 2019Q1-Q2, then 15%, 14%, 29%, 25%, 21%, 19%.
   - A missing GARAGE marks these rows: among the shared 2019-2020 sales, 45.7% of those without a car count are stale, against 13.9% of the others.
   - Not a leak, unlike King County. LightGBM on the shipped windows scores the 349 shared test rows at RMSE 0.138 with the file's values and 0.126 with the sold listing's. On the 90 rows that differ: 0.154 against 0.123, with the file's values under-predicting by 0.045.
   - Implemented: keep, with an `Anomaly:` bullet. This replaces my earlier "Changes to a house after its sale ... cannot be seen in the file", which the comparison contradicts.
   - Question: is a test period in this stale regime acceptable?
   - Alternative, not recommended: end the data before July 2019. This loses 7,978 rows, and the test windows would move to late 2018 to mid-2019. The 9 x 3-month windows of issue 6 would put their 3 oldest windows before the step.
3. **The scrape's sampling shapes the training history.**
   - Each property appears once, with its latest sale (discussion 383033).
   - Each suburb holds only its newest sales: 1-231 rows, mean 103. Busy suburbs start in 2018-2020 (Butler Sep 2018, Ellenbrook Jul 2019, Baldivis May 2020); quiet ones reach back to 1988.
   - So the years before 2013 hold 2,263 sales, mostly of quiet suburbs and of houses not resold. Baldivis has no training rows for the April 2020 window.
   - Implemented: keep all rows.
   - Alternative: keep sales from 2013 on only (mean RMSE 0.1612 → 0.1607).
4. **The build-year rule removes only part of the land and off-the-plan sales; all of them are training rows.**
   - 563 sales dated before the build year are dropped. Cross-fitted LightGBM prices them 0.23 log units too high on average.
   - The 140 sales in the build year stay, although 9-13% of them are priced more than 0.5 log units too high (two runs), against 1.2-1.3% of older houses.
   - Sales without a build year before 2005 (51 rows) have a mean residual of -0.21 to -0.22, with 29-33% below -0.5.
   - The test period shows no excess: in 2020, 0.2-0.8% of each group is below -0.5.
   - Dropping the 563 changes test RMSE by 0.0004. Alternative: keep them.
5. **ADDRESS is kept as a string feature.**
   - Its unit numbers (1,060 rows, median price $404,000 against $540,000) and lettered lots (2,615) are the only trace of the property type, which the site shows and the upload dropped.
   - A derived unit flag lowers LightGBM's mean RMSE from 0.161 to 0.158 (lower in 7 of 9 windows).
   - The probe's text encoding gains nothing: RF R² 0.849 with the text, 0.865 without; LightGBM 0.863 and 0.865. Tokenising drops the "/".
   - Kept as text, as melbourne_housing_market and california_house_prices_2020 do.
   - Alternatives: a `UNIT` flag ("reconstruct destroyed meaning", patterns §D.12), with or without the text; or drop ADDRESS.
   - Not tested: how `tabarena_default`'s text embedding uses the column.
6. **Window length.**
   - Implemented: 9 x 1 month, April-December 2020, 284-628 sales per window, oldest train share 88%. All windows fall in 2020 and in the stale regime of issue 2.
   - Alternatives: 9 x 2 months, July 2019 to December 2020 (658-1,197 sales, train share from 76%); or 9 x 3 months, October 2018 to December 2020 (974-1,619, from 64%).
7. **No planning gap.**
   - Many sales reach the site within days: an archived Mount Lawley page of 14 April 2021 lists four sales of April 2021 among its 10 newest. Still, a month after its end, December 2020 held about 80% of its usual share of November's count.
   - Implemented: no gap, as house_sales and house_prices_nominal.
   - Alternative: a one-month gap, as zillow_prize (LightGBM mean RMSE 0.159 → 0.162).
8. **December 2020 is kept although it is short.**
   - 412 sales; December/November is 0.71 against 0.83-1.04 in 2013-2019.
   - Its prices relative to each suburb's median are not lower: +0.048, against +0.027 in November and +0.023 in October.
   - Alternative: drop the month, as house_sales dropped its cut-short May 2015.
9. **Implausible and probably non-market rows are kept.**
   - 52 sales since 2012 are below $120,000.
   - 19 houses of 2-4 bedrooms have 1-40 m² of floor area; one house of 95 m² has 16 bathrooms.
   - Strata units often carry the land area of the whole complex.
   - The file has no sale type. A price floor of our own would filter on the target.
10. **The download is not pinned to a Kaggle version.** `kaggle datasets download syuzai/perth-house-prices/1` returns 404. The single version reproduces the sha256 today (the verifier re-downloaded it).
11. **Licence (noted only).** CC BY-NC-SA 4.0; the terms of house.speakingsame.com are not stated.
12. **Framework, not patched.** `meta_time_horizon_mismatch` fires for month-start dates in one-month windows. The check could measure a window from its start to the next window's start.
13. **Record pointer.** `v2_path` is not set in `curation/records/perth_house_prices.md`; `sync-notebooks` was not run in this batch.
14. **Backlog note.** heptix/perth-property-prices (42,958 sales of 2006-2024, CC BY-SA 4.0, no stated source) has property type, agency, exact dates and no price cap. It has no floor area or build year. It is a separate candidate.

#### Verification (fix round, 2026-10-07)
Verifier's verdict: "needs changes, to curation_comments and the record comment only; no leak, no code change". I checked each finding against the data before applying it; my scripts are `fix_check_stale.py` and `fix_check_resid.py`, with outputs `fix_check_*.txt`, in the scratch folder.

1. **Price cap (major): accepted and reproduced.**
   - Reproduced: the bins (46 / 11 / 0 in the file), the yearly maxima, Peppermint Grove (41 rows, last March 2018), Dalkeith (median $2,039,000, 55% at $2M or more), heptix 75 of 5,072 (1.48%), and the McNeil Street page.
   - Two counts differ:
     - "62 of 4,132 test rows in the 8 dearest suburbs": on the curated frame, the 8 suburbs at 12% or more hold 45 test rows. 62 needs a threshold of 11.5% (9 suburbs, Mosman Park at 11.9%). The 8th suburb at 12% is Keysbrook, a rural suburb with 1 of 8 rows at $2M. The comment names the 7 suburbs at 13-55%, which hold 45 test rows.
     - "25 test rows at $2M or more": 25 are above $2M; 29 are at $2M or more (4 at exactly $2M).
     - The heptix share for Peppermint Grove and Dalkeith (40-48%) counts all property types; houses only give 67% (6 of 9) and 50% (12 of 24).
   - Implemented: an `Anomaly:` bullet, a decision table (sales, maximum and sales at $2M or more per year, 2011-2020), the record comment, and issue 1.
2. **Stale records in the test period (major): accepted and reproduced independently.**
   - I matched on the curated frame and got 1,824 shared sales; the verifier matched on the raw file and got 1,826.
   - Reproduced: the differ shares 0.7 / 2.8 / 12.1 / 27.0%, 2020 fewer 22.9%, the quarterly series, the GARAGE marker 45.7% against 13.9%, RMSE 0.138 against 0.126 on 349 rows, 0.154 against 0.123 on 90 rows, and the 16 Canna Way example.
   - Implemented: an `Anomaly:` bullet replacing the "cannot be seen" sentence, the record comment, and issue 2. Ending the data before July 2019 (7,978 rows lost) is listed as an alternative, not a recommendation.
3. **Build-year rule (minor): accepted.**
   - My curated-frame run gives 51 sales without a build year before 2005, mean -0.212, 29% below -0.5. The verifier's run gives -0.223 and 33%.
   - For the 140 sales in their build year: 12.9% below -0.5 on the curated frame, 8.6% in my raw-frame run.
   - The bullet now gives ranges, and the wording "look like the rest" is gone. No code change.
4. **ADDRESS text (minor, Lennart's call): accepted.**
   - Reproduced from the verifier's probe outputs: RF 0.849 with the text, 0.865 without; LightGBM 0.863 and 0.865.
   - The bullet now says the text encoding gains nothing, and the derived unit flag is named as the alternative. The text is kept.
5. **Wording (minor): accepted.**
   - Distances are rounded to 100 m from 1 km on: 99.9% of values of 1 km or more are multiples of 100; below 1 km, 3,893 station and 9 CBD distances are exact metres.
   - The Nedlands page is now described as a property not in the file and without a building size. `FLOOR_AREA` = "Building size" is shown on 10 Harmony Avenue, Clarkson (archived 2023-01-31: "Building size: 200 sqm", the file's 200).
   - The splits comment now says "four sales of April 2021".
6. **Record comment: replaced.** It is the verifier's draft with "Kaggle" added (118 words).
7. **Record pointer: unchanged** (issue 13).

Also changed: `_decisions` gained the price-cap table, and its sort uses `kind="stable"`, which `definition_nondeterministic` requires. The checks were re-run: `dataset check` (clean), ruff, pytest (2 passed) and pandas 2/3 (same checksum).

### pkdd_15_taxi_trip_time_prediction_ii

**Outcome:** added and checked: `datasets/_dev/tabarena-v0pt2/pkdd_15_taxi_trip_time_prediction_ii_1m/` (a `_1m` version: 1,655,983 trips after cleaning). Fixes from the verification round are applied (see **Verification**).

**Record judgment:** valid with concerns.
- Provenance: the training set of the ECML/PKDD 2015 Discovery Challenge (organisers Moreira-Matias, Ferreira, Mendes-Moreira; the taxis of one Porto dispatch central; challenge site hosted by Geolink). It ran on Kaggle as Task I (destination) and Task II (travel time) on the same data, and the organisers donated it to UCI (id 339, DOI 10.24432/C55W25).
- Unique: no other record holds the Porto data. A grep of `curation/records/` for pkdd, porto, taxi, trajector, UCI 339 and the two arXiv ids finds only this record; the NYC records are TLC data. No working-copy folder uses it. In this run, `nyc_taxi_trip_duration` is the same task type on other data.
- Scope: the competition's own Task II (remaining time of a partial GPS trajectory) is a sequence task. The curator's framing (CC 2026-09-21: ETA at the start of the trip from origin, destination, time, call type, stand and taxi) is a fixed regression with a temporal split, in scope.
- Concern: the source says the destination is not known to the dispatch system (issue 1).

**Data:**
- Source: the UCI static zip `https://archive.ics.uci.edu/static/public/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015.zip`. The Kaggle competition returns 403 (rules not accepted). Its `train.csv.zip` is 533,605,607 bytes for both PKDD 2015 competitions (`kaggle competitions files`), the same size to the byte as the one in the UCI zip.
- Kept: `train.csv` only, 1,710,670 trips x 9 columns (TRIP_ID, CALL_TYPE, ORIGIN_CALL, ORIGIN_STAND, TAXI_ID, TIMESTAMP, DAY_TYPE, MISSING_DATA, POLYLINE), 1.94 GB, sha256 2891d03ea99ce0fc203daedd434848a1a8baa7a8fb6da10f8d7ff26559efff6d.
- `_prepare_raw_files` parses the polylines once (polars) into `trips.parquet`: the point count and the first and last point.
- Licence: CC BY 4.0, stated on the UCI page.

**Definition:**
- Folder `pkdd_15_taxi_trip_time_prediction_ii_1m`, with `version_of = "pkdd_15_taxi_trip_time_prediction_ii"` and `subsample_to_budget = True`.
- Prediction point: the start of the trip (meter on). Known: call type (dispatch_central / taxi_stand / street), stand, taxi, start time and place, and the destination (the trip's last GPS point). Not known: the route and the end time.
- Target: `log1p_travel_time` = log1p((GPS points - 1) x 15 s), the challenge's definition; RMSE on it is the challenge's RMSLE.
- Regime: temporal on `start_time` (Porto local time). 3 test windows of one calendar month (June, May, April 2014: 148,236 / 156,990 / 131,659 trips); train is all earlier trips, sampled to 1M per window. The `_1m` frame has 1,436,885 rows x 8 features (call_type, origin_stand, taxi_id, start_time, start_lon, start_lat, end_lon, end_lat).
- Rows dropped, in order: 36,510 with < 2 GPS points; 21 whose TRIP_ID repeats among the rest; 937 starting outside Greater Porto (lat 41.0-41.3, lon -8.8 to -8.4); 15,533 under 60 s; 827 over 3 h; 741 whose start-to-end straight line is faster than 120 km/h; 118 starting on 2014-07-01 in local time.
- Columns: drops TRIP_ID, ORIGIN_CALL, DAY_TYPE (constant "A") and MISSING_DATA (True for 10 trips; unreliable and post-trip). TIMESTAMP (UTC) becomes Porto local time. CALL_TYPE A/B/C is mapped to names.
- BibTeX: UCI's own citation of the DOI (`moreiramatias2013taxi`, year 2013). `year = "2015"`.
- `_decisions`: the filter table, taxi recurrence per test month, and the daylight-saving evidence for local time.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, 0 info (26 checks run). Nothing accepted; `accepted_check_warnings` is empty.
- README checksum: v2:118121342a206dc8565e269154a9be328e60a37efc73e2c3910f1c52030e847c.
- `ruff check` and `ruff format` are clean.
- `pytest tests/test_v2_datasets.py -k pkdd_15_taxi_trip_time_prediction_ii_1m`: 1 passed, 1 skipped (the opt-in data check).
- pandas 3.0.6 (scratch venv): `check(write_report=False)` gives the same checksum, so pandas 2.3 and 3 build the same container.

**Probes:**
- **Leak probes** (`leak_probes.py`: untuned LightGBM, first 3 splits, 50k rows a side; the script leaves `start_time` out):
  - All features R^2 0.377; depth-2 / depth-3 tree 0.076 / 0.097.
  - Each feature alone: end_lat 0.097, end_lon 0.080, taxi_id 0.021, start_lon 0.020, origin_stand 0.020, start_lat 0.015, call_type 0.007. Without end_lat 0.269, without end_lon 0.231, without taxi_id 0.391.
  - Missing indicator of origin_stand: 0.007. Test rows with an exact feature copy in train: 0.0%. 1-NN R^2: 0.337 for the closest tenth, -0.032 for all.
  - No column comes near the full model, and no rule: nothing to answer.
- **Task probes** (`task_probes.py`, 3 of 3 windows): re-run on the final frame, and the numbers are identical to the first run. LightGBM R^2 0.373 (skill +0.373 +- 0.018), random forest 0.365, linear 0.029; the best single feature (end_lat on all 3 windows) reaches 0.098, and the drift baseline -0.002. LightGBM beats the dummy on 3 of 3 windows; the spread LightGBM - linear is +0.344 (paired SE 0.010). Flags: none. The probe enters `start_time` as one number, without the hour.
- **Generated-data probes** (`generated_probes.py`): exact share 0.8% (after exp) against 0.8% on a shuffled target; flags: none.
- **Group probes** (`hidden_groups.py`, `group_probes.py`): not run, since the task is temporal. The taxi as a possible group is answered by the recurrence table (`_decisions`, issue 4).
- **The frame:** the shipped frame is the one these probes ran on. The interim `start_hour` column was removed again, and the near-trip count of the shipped frame (56,962 within 500 m) equals the verifier's.
- **Own LightGBM on the shipped splits** (`exp4.py`: 1M training trips, 250 trees, date parts of `start_time` plus the local hour). R^2 for June / May / April:
  - with the destination: 0.502 / 0.478 / 0.503;
  - pickup fields only: 0.118 / 0.113 / 0.150;
  - AutoGluon v0.1 date parts without the hour: 0.484 / 0.453 / 0.463.
  - These agree with the verifier's run to within 0.004.

**Issues for Lennart:**
1. **Framing: the destination as a feature.**
   - Question: keep the destination-known ETA, or ship the pickup-only task?
   - Evidence: in the source the destination is recorded at the end of the trip. The data page says "The last list item corresponds to the trip's destination". The challenge overview (geolink.pt, Wayback 2015) says "In most cases, taxi drivers operating through an electronic dispatch system do not indicate the final destination of the ride"; that is why Task I asks for it. Lam et al. 2015, Sec. 1: "busy taxi drivers do not report the final destination of the ride".
   - Your CC of 2026-09-21 rejected pickup-only for its weak signal (R^2 0.14). That reason predates task_probes.md rule 2 (2026-10-06: a small but real signal is no reason to drop a task). Rule 6: "A better version the source itself defines ... replaces the current one". Pickup-only is the source's own question, when a busy taxi will be free.
   - Numbers on the shipped splits: R^2 0.118 / 0.113 / 0.150 without the destination, against 0.502 / 0.478 / 0.503 with it. The signal is real on 3 of 3 windows.
   - Implemented: your framing.
   - If you switch: drop `end_lon` / `end_lat` and keep the filters. The folder stays `_1m` with a new checksum. Only one framing can ship, since they are the same data.
   - `nyc_taxi_trip_duration` differs: its source kept the dropoff coordinates as features on purpose.
2. **Two row filters beyond your list.**
   - (a) Trips under 60 s: 15,533 (0.9%), holding 21% of the variance of the log travel time. The share of trips that end within 100 m of their start falls from 70% at 15 s to 50% at 30 s, 40% at 45 s, 31% at 60 s and 7% at 120 s, so the 60-s cut is a choice on that slope. Two taxis record 3,352 of them (35% and 23% of their own trips).
   - (b) A start-to-end straight line faster than 120 km/h: 741 trips, 725 of them with a jump of over 1 km between two 15-second GPS points.
   - Implemented: both dropped.
   - Alternative: keep them and drop only trips with < 2 points, as listed. `nyc_taxi_trip_duration` drops trips under 30 s (its clock has 1-s resolution).
3. **Trips that end where they start (kept).**
   - 65,708 trips (4.0%) end within 500 m of their start and 23,712 (1.4%) within 100 m. Those within 100 m last a median 16.2 min, against 5.5 min for trips of 0.5-1 km: a meter left on or a round trip, with no destination a passenger would give.
   - The trips within 500 m hold 13.8% / 13.9% / 14.8% of the test variance (June / May / April). R^2 is 0.502 / 0.478 / 0.503 with them and 0.552 / 0.528 / 0.554 without. That is noise, not a leak.
   - Implemented: kept, with an anomaly bullet.
   - Alternative: drop trips that end within 100 m of their start. That filter is on a feature, so a deployment could apply it. NYC kept its 0.4% of one-point trips.
4. **"Taxi as group" from the verdict.**
   - v2 refuses a task that is both grouped and temporal (`src/data_foundry/v2/dataset.py:1114`).
   - Implemented: temporal, with `taxi_id` as a categorical feature. 99.93% / 100% / 100% of the April / May / June trips are by taxis seen before (0-1 new taxi per month, 428-434 taxis active each month).
   - Alternative: a grouped split by taxi, which would test new drivers.
   - After the cleaning, taxi_id changes LightGBM R^2 by only -0.004 to +0.003. Its earlier strength came from a few taxis that record most of the sub-minute trips.
5. **ORIGIN_CALL dropped.**
   - After the row filters: 56,780 phone ids for 361,050 central trips, one id (2002) on 15.8%.
   - With the destination it changes R^2 by -0.001 to +0.002 as a LightGBM categorical; pickup-only it adds +0.002 to +0.005.
   - Alternative: keep it as a 57k-level categorical. A Kaggle write-up (topic 15019) found it "very helpful" for the partial-trajectory task.
6. **Window length.**
   - Implemented: 3 calendar months (horizon 1 month), because the challenge tested 1.5-6 months after its training year.
   - Alternative: 3 x 7 days, as in delivery_eta_1m, maps_router_eta_1m and nyc_taxi_trip_duration (31,699-34,810 trips per week here).
7. **Hour of day (pipeline choice).**
   - BeyondArena's `tabarena_default` preprocessing keeps the hour: it encodes datetimes with skrub's DatetimeEncoder (`tabarena/benchmark/preprocessing/date_feature_generators.py`).
   - Only the TabArena v0.1 `default` pipeline loses it, through AutoGluon's year/month/day/dayofweek (`autogluon/features/generators/datetime.py:27`). LightGBM R^2 is 0.484 / 0.453 / 0.463 with those parts against 0.502 / 0.478 / 0.503 with the local hour.
   - Implemented: no extra column. Your call: which pipeline v0.2 runs.
8. **Label noise kept.**
   - 1.2% of the kept trips jump more than 1 km between two GPS points, a GPS error or missing points, so the (points - 1) x 15 s label can be too short. Some trips also include a return with the meter on (Lam et al. 2015, Sec. 2).
   - Implemented: kept, since this is the challenge's own label definition.
   - Alternative: drop the 19,673 trips with a jump.
9. **Local time.**
   - TIMESTAMP is UTC: at both daylight-saving switches the weekday profile by UTC hour moves by one hour (correlation 0.92 / 0.90 unshifted, 0.99 shifted).
   - Implemented: Europe/Lisbon wall-clock time without a time zone.
   - Alternative: keep UTC.
10. **Year.**
    - The two docstrings disagree. The v2 attribute (`src/data_foundry/v2/dataset.py:221`) says "Year the data was published"; the schema's `dataset_year` (`schema.py:192`) says "The year when the data was collected/created".
    - Implemented: `year = "2015"`, as in the record, the v2 docstring and the competition datasets of the working copy (kick 2011 for 2009-10 data, acquire_valued_shoppers_challenge 2014 for 2012-13, rossmann_store_sales 2015 for 2013-15). The BibTeX follows UCI's own citation (2013).
    - Alternative: `year = "2013"`, UCI's year of creation.
11. **Record pointers (orchestrator).**
    - `v2_path` is unset; `sync-notebooks` should point it to the `_1m` folder.
    - `curation/records/nyc_taxi_trip_duration.md` lists this competition's URL in its own `source_links`.

**Verification:**
- Finding 1 (framing, major): issue for Lennart. Issue 1 now has the numbers on the shipped splits and rules 2 and 6. No code change.
- Finding 2 (hour of day): handled as the coordinator's correction says. `start_hour` was added, then removed, because `tabarena_default` keeps the hour (skrub DatetimeEncoder) and only the v0.1 `default` pipeline drops it. Recorded in curation_comments and issue 7. Which pipeline v0.2 runs is Lennart's call.
- Finding 3 (trips ending near their start): applied. A new anomaly bullet gives the counts, the medians, the share of test variance and R^2 with and without them. Dropping them is issue 3.
- Finding 4 (comment numbers): applied. ORIGIN_CALL now uses the post-filter counts (56,780 ids, 361,050 trips, 15.8%). The sub-minute bullet gives the 15/30/45/60/120-s shares (70/50/40/31/7%).
- Finding 5 (Kaggle file size): applied. Checked with `kaggle competitions files` for both competitions (533,605,607 bytes) and added to `download_description`; this closes the former "file is UCI's, not Kaggle's" issue.
- Finding 6 (year): partly applied. The BibTeX year is now 2013, with key `moreiramatias2013taxi`, matching UCI's own citation, which says `year = {2013}`. The `year` attribute was rejected and stays 2015: the v2 docstring "Year the data was published", the record, and the working copy's competition-year convention. Issue 10 covers the docstring conflict.
- Finding 7 (decision text): applied. Decision 2 now says that a v2 task is grouped or temporal, not both, and that 99.93-100% of each test month's trips are by taxis seen before.
- Findings 8-9: left to the orchestrator (issue 11).

### qsar_bioconcentration
**Outcome:** added and checked. Fix round done after the verification: the swapped rows are repaired, the class rule and the selection are cited from the authors' supplementary files.

**Record judgment:** valid with concerns. The data trace to Grisoni et al. (2016, Environment International 88:198-205), donated to UCI 510 by the Milano Chemometrics and QSAR group. The BCF values come from the authors' 2015 table (Chemosphere 127:171-179, SI `mmc2.xlsx`, 1,056 chemicals); 777 of the 779 UCI rows match a row of it on CAS number with the same logBCF. It is a real QSAR task published for prediction (UCI lists classification and regression). No other folder or record holds this data (searched the UCI DOI, OpenML 43581 / 43699 / 46585 / 46586 / 46827, the Kaggle slug and "bioconcentration"). 399 of the kept chemicals also appear in the ICCVAM rat oral toxicity set behind qsar_oral_toxicity (InChIKey match), with another endpoint and other features, so it is not a duplicate. The sibling QSAR folders (fish toxicity, aquatic toxicity, biodegradation, oral toxicity, tid_11) model other endpoints. Remaining concerns: the paper text is unread (the class thresholds are inferred from the data, 600 of 607); the 9 descriptors were selected on 75% of the labelled data.

**Data:** UCI 510 static zip (`https://archive.ics.uci.edu/static/public/510/qsar+bioconcentration+classes+dataset.zip`) -> `Grisoni_et_al_2016_EnvInt88.csv` (66,499 bytes, UTF-8 with BOM, CRLF, sha256 5bfd2d11...cdc104; reproduced from the download description). 779 rows x 14 columns: CAS, SMILES, Set (Train 584 / Test 195), 9 Dragon descriptors, Class (1/2/3: 460 / 64 / 255), logBCF. Licence: CC BY 4.0 on the UCI page; the old UCI page (web.archive.org) says "The dataset is freeware and may be used if proper reference is given to the authors." The authors' SI files are free on ars.els-cdn.com (Env. Int. `1-s2.0-S0160412015301288-mmc1.pdf`, Environ. Res. `1-s2.0-S0013935116301566-mmc1.docx`, Chemosphere `1-s2.0-S0045653515000879-mmc2.xlsx`); they are evidence only, not raw inputs. michem.unimib.it blocks this machine (Wordfence 503); no form was filled.

**Definition:** `datasets/_dev/tabarena-v0pt2/qsar_bioconcentration/`. Prediction point: an organic chemical without a measured fish BCF, before a fish test (REACH bioaccumulation screening); known: its structure (SMILES) and the descriptors computed from it. Target `bioconcentration_mechanism` (lipid storage 458 / additional storage sites 64 / metabolized or eliminated 254), multiclass, log loss. IID, recommended stratified 3-fold x 10 repeats (train 517-518, test 258-259). 776 rows x 10 features (9 numeric descriptors + SMILES as a string). Cleaning: the SMILES and 9 descriptors swapped back within three pairs (benzene/cyclohexane, naphthalene/tetralin, chlorobenzene/chlorocyclohexane); 3 rows with an unrepairable wrong structure dropped (triticonazole, 1,3,6,8-TCDD, 1,2,3,4,7,8-HxCDD); logBCF dropped (the class is read from it); CAS and Set dropped; `B02[C-N]` / `F04[C-O]` renamed to `B02(C-N)` / `F04(C-O)` (LightGBM and XGBoost refuse square brackets). Three `_decisions` tables: class against the TGD band computed with MLOGP, the 9 rows with a wrong structure and what was done, the isomer counts. Same checksum under pandas 2.3.3 and 3.0.6 (v2:ba8eca34...b804). Year 2016 (the paper; UCI donation 2019), following the record.

**Checks:** `dataset check`: 0 errors, 0 warnings; one accepted: `dataset_identifier_column` (SMILES is the chemical's structure, unique because every row is a distinct chemical; phiusil_phishing accepts a URL the same way). `pytest -q tests/test_v2_datasets.py -k qsar_bioconcentration`: 1 passed, 1 skipped. Import check passes. ruff check and format clean.

**Probes:** (776 rows; run against a root holding only this folder, since a fresh scaffold of another agent broke discovery of the whole working copy during the first round)
- Leak (untuned LightGBM, 3 splits, the 9 descriptors): macro ROC AUC 0.727; depth-2 / depth-3 tree 0.599 / 0.623; best single feature piPC09 0.648, without it 0.713; no missing values; 5.4% of test rows have an exact descriptor copy in train (positional isomers whose SMILES differ); 1-NN agreement 0.885 (closest tenth) / 0.618 (all) / chance 0.462. No leak.
- Task: no flags. Random forest log loss 0.756 vs 0.883 for the class shares (skill +0.143, SE 0.006), macro AUC 0.734, better than the dummy on 30 of 30 splits; linear 0.802; untuned LightGBM 1.339 (overconfident, macro AUC 0.733); smallest class per test fold 21.
- Generated: 0.0% of the minority in rule leaves, no flag.
- Hidden groups: one candidate (F04(C-O), a count), no hit (s_id -0.018).
- By hand (776 rows, random forest, 3-fold x 5): logBCF as a feature lifts macro AUC from 0.751 to 0.826 (log loss 0.746 -> 0.630), logBCF + MLOGP alone 0.792: dropped. Descriptors vs SMILES row by row (nHM, B02, F04 recomputed with RDKit match all 779 rows). CAS vs SMILES for every row in Wikidata and PubChem: 770 match, 9 do not.

**Issues for Lennart:**
1. **Target: class (implemented) or logBCF regression.** The class is a rule on logBCF and the experimental logKOW (cited below), so each framing must drop the other column. Implemented: the class, the dataset's published name and the task the 9 descriptors were selected for; modest, real signal (random forest macro AUC 0.751, log loss 0.746 vs 0.883). Alternative: logBCF regression (random forest R^2 0.718, a line on MLOGP alone 0.626), a KOW-dominated task, as a `_reg` folder if both are wanted.
2. **Swapped pairs repaired (implemented) or dropped.** Repaired: the 2015 table gives all six chemicals with their right SMILES and the logBCF of UCI 510, and each file class follows the rule with the chemical's own experimental logKOW (four of six would change class with the partner's). Alternative: drop the six rows as in the first round (770 rows: 452 / 64 / 254). Either way the swap is worth reporting to the authors or UCI.
3. **Resolved (2026-10-14): SMILES dropped, RDKit's 193 descriptors added next to the 9.** (Was: SMILES kept as a string (implemented) or dropped.) Lennart's call for every SMILES dataset (apistox, issue 1). With RDKit's descriptors every chemical has its own values (with the 9 alone 61 share theirs, 14 of them with another class); LightGBM macro AUC 0.735 -> 0.752, better on 13 of 15 splits; the SMILES as text instead 0.723. Before: kept: it is the structure, known for a new chemical; the record's tag is "Free Text (Short)"; drug_induced_autoimmunity_prediction and apistox keep SMILES. Numbers (776 rows, random forest macro AUC): descriptors 0.751, with 30 SVD components of SMILES character n-grams 0.736, SMILES alone (TF-IDF, logistic regression) 0.710; chemistry featurizers do not beat the 9 descriptors (0.752; 217 RDKit descriptors 0.758; Morgan bits 0.719). Dropping it gives a purely numeric task but leaves 61 chemicals sharing their 9-descriptor vector (positional isomers), 14 of them with conflicting classes.
4. **Class thresholds inferred, paper text unread.** The ±0.5 log-unit band around the TGD line reproduces 600 of 607 classes (experimental logKOW >= 1); below logKOW 1 the authors put 38 of 45 chemicals in class 1, a convention only the paper can state. Google `"Investigating the mechanisms of bioconcentration through QSAR classification trees" pdf` (BOA/IRIS 10281/101916 has no file).
5. **Descriptor selection on labelled data (kept with a note).** Paired test inside one cross-validation (776 rows, out-of-fold, 10 repeats): random forest macro AUC +0.064 on the authors' training chemicals vs their test chemicals (null -0.002, sd 0.041, p = 0.06); logistic regression +0.003 (p = 0.48); the 9 descriptors score like 217 RDKit descriptors. Same call as home_credit_default_risk.
6. **Domain convention among the QSAR siblings.** Implemented "chemistry & material science" (the record; qsar_oral_toxicity too), while qsar_fish_toxicity, qsar_aquatic_toxicity and qsar_biodeg use "biology & life sciences".
7. **Pretraining overlap (your call, no change).** TabSTAR lists OpenML 46585 (this data) in `tabstar_paper/benchmarks/folds_pretrain.py`. Its annotation also maps "2" to "Metabolized/Eliminated" and "3" to "Additional Storage Sites", the reverse of the old UCI page and of the rule (class 2 lies above the TGD line).

**Verification (fix round, 2026-10-07).** The verifier's verdict: ready with noted concerns. Each finding, checked with my own scripts (`check_si_2015_v2.py`, `numbers_776.py`, `mlogp_vs_kow.py`, `modality_check_776.py`, `smiles_style_776.py` in the scratch folder):
- F1, swapped pairs: confirmed. The 2015 table holds the right SMILES, the same logBCF (0.63, 1.94, 2.145, 2.50, 1.305, 2.345) and experimental logKOW (2.13, 3.44, 3.30, 3.49, 2.84, 3.09); with the partner's logKOW benzene and chlorobenzene would be class 3, cyclohexane and chlorocyclohexane class 2. Implemented the repair in `_clean` (`_swap_back_structures`); triticonazole and the two dioxins have the same wrong SMILES in 2015 and stay dropped.
- F2, class rule: confirmed. Both quotes are in the SI files (Env. Int. SI, Sec. 1, p. 1; Environ. Res. SI, Sec. 1). The band reproduces 600 of 607. One detail differs: I find three of the 7 misses within 0.003 of the 0.5 boundary (residuals 0.499, -0.498, -0.497), not four; two more sit at -0.52 and -0.53. Also checked that MLOGP cannot stand in for the experimental logKOW: RMSE 1.00 against it on 652 chemicals (the Environ. Res. SI's 0.59 is VEGA's MlogP on 543 chemicals in its applicability domain, another implementation), and the band with MLOGP gives the class of 471 of 776.
- F3, selection: confirmed with a small count difference. Matching CAS numbers token by token, 277 of the 278 chemicals of the 2015 table missing from UCI 510 had only a predicted KOW (the other is fenoxycarb, 79127-80-3); counted by table rows it is 278 of 279 (glyphosate has two rows). The verifier's 278 of 280 used another join; the conclusion is the same.
- F4, selection optimism: recomputed on the 776 rows: random forest +0.064 (p = 0.06), logistic +0.003 (p = 0.48); the note stays.
- F5, wording: the task text and the "randomly split into 584 / 195" quote are now credited to the old UCI page (web.archive.org).
- F6, SMILES: recomputed on 776 rows: 9 descriptors 0.752, RDKit 2D 0.758, both 0.763, Morgan 0.719; writing style adds nothing (0.751 -> 0.753; style alone 0.604). No change.
- F7: kept as issue 7.
- Tooling note for the orchestrator: `ruff check --fix` (rule C416) rewrote `{a: b for a, b in SWAPPED_PAIRS}` into `dict(SWAPPED_PAIRS)`, which changes the meaning when the iterable is a dict keyed by pairs; `dataset check` caught it (3 duplicate rows, an unused accepted warning). The helper now builds the mapping in a loop. Worth a line in the skill: read the diff after `ruff --fix` on dict comprehensions over dicts.

### qsar_oral_toxicity
**Outcome:** added and checked (verified 2026-10-07: "ready with noted concerns"; the `curation_comments` "Note" bullet gained the clustering evidence afterwards, so the checksum changed from v2:5eb242a0... to the value in the README)

**Record judgment:** valid. The data traces to its origin: UCI 508 was donated in 2019 by the Milano Chemometrics and QSAR Research Group (archived UCI page, "Source" and "Data Set Information"), the authors of Ballabio et al. 2019 (Mol. Inf. 38:1800124). The labels are the very toxic (VT) endpoint of the calibration set of the ICCVAM "Predictive Models for Acute Oral Systemic Toxicity" project (rat oral LD50 curated by NICEATM and the U.S. EPA; the project's consensus became CATMoS, Mansouri et al. 2021, EHP 129:047013). The project's training file at NTP (https://ntp.niehs.nih.gov/iccvam/methods/acutetox/model/trainingset_171130.txt) has 741 TRUE, 8,251 FALSE and 2 missing VT values, the class counts of the UCI file. Unique: no working-copy folder or record holds this data (grep for UCI 508, the DOI, CATMoS, NICEATM, LD50, acute oral toxicity); the other QSAR sets (qsar_biodeg, qsar_aquatic_toxicity, qsar_fish_toxicity, qsar_tid_11, clock_protein_toxicity, hiva_agnostic, apistox, qsar_bioconcentration) are other endpoints and compounds. Scope: the features are a vectorised molecular graph (1,024 ECFP bits). This is in scope by the qsar_tid_11 precedent (1,024 FCFP bits, shipped; Lennart's comment there: tabular models are still a strong baseline). On our folds a random forest (ROC AUC 0.883) matches a Tanimoto nearest-neighbour model of the paper's N3 kind (0.877), and Jiang et al. 2021 (J. Cheminform. 13:12, Conclusion) find "descriptor-based models are able to achieve better or comparable predictions to the highly-intricate and specialized graph-based models". Class balance: 741 of 8,992 very toxic (8.2%); after deduplication 708 of 8,493 (8.3%), at least 236 per test fold.

**Data:** UCI static zip https://archive.ics.uci.edu/static/public/508/qsar+oral+toxicity.zip, one file `qsar_oral_toxicity.csv` (8,992 rows x 1,025 columns: 1,024 bits and `positive`/`negative`, `;`-separated, no header, no identifiers; sha256 c8ec1617...c874), in `local-data-warehouse/qsar_oral_toxicity/`. Licence CC BY 4.0 (UCI page); the Milano group's page says "The dataset is freeware and may be used if proper reference is given to the authors". The group's own download (michem.unimib.it/download/data/acute-oral-systemic-toxicity/) sits behind a form that asks for personal data, and the site returns HTTP 503 (Wordfence block) to this machine; UCI is the authors' own donation, so nothing is lost. For checks only, I downloaded the project's NTP files (trainingset_171130.txt, validationset.txt; US government data) to `../_scratch_new65/qsar_oral_toxicity/` (4 MB; delete after verification).

**Definition:** `datasets/_dev/tabarena-v0pt2/qsar_oral_toxicity/`.
- Prediction point: a chemical without an acute oral test (a new substance, or one on a regulatory list), from its QSAR-ready structure alone. All 1,024 bits are computed from the structure.
- Target: `very_toxic` Yes/No (LD50 < 50 mg/kg); ROC AUC (the paper scores the non-error rate).
- Regime: IID, the default stratified 3 x 3 CV (train 5,662, test 2,831). Both source protocols are random: the project took every fourth chemical after sorting by endpoint values, "without supervised sampling of the chemicals based on structures" (Mansouri et al. 2021), and the authors drew a stratified random 25% (paper, Sec. 2.1).
- Frame: 8,493 rows x 1,024 numeric 0/1 features (`ecfp_1`...`ecfp_1024`).
- Cleaning: 477 exact copies dropped, then all 22 remaining rows of the 11 bit vectors that occur with both classes. The copies are salt forms, hydrates and stereoisomers of one QSAR-ready parent. The NTP file shows the same counts by InChIKey first block: 406 repeated parents covering 893 chemicals, 11 with both classes (29 chemicals, 15 positive). In the UCI file: 406 repeated vectors, 894 rows, 11 with both classes (29 rows, 15 positive).
- Two `_decisions` tables (duplicates; the file order is the authors' split).
- Raw file checked against the paper: the file stores the authors' 6,744 training rows (556 positive) and then their 2,248 test rows (185), as in Table 1. On that split, a similarity-weighted kNN reaches a non-error rate of 0.846 against N3's 85% in Table 3.
- The container checksum is the same under pandas 2.3.3 and 3.0.6 (v2:5eb242a0...aa70, as in README).

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 infos; nothing accepted. Import check passes. `pytest tests/test_v2_datasets.py -k qsar_oral_toxicity` passes, including the data test (`DATA_FOUNDRY_V2_DATA_CHECKS=1`). `dataset list` over the working copy exits 0. No `TODO` is left in `dataset.py`.

**Probes:** (outputs in `<scratch>/probes/`)
- Leak (LightGBM, 3 splits): no flag.
  - AUC 0.869 with all bits, 0.717 / 0.740 for a depth-2 / depth-3 tree.
  - Best single bit `ecfp_283` 0.679; without it 0.868.
  - No missing values; 0.0% exact feature copies across the split.
  - Label-free nearest-neighbour distance: AUC 0.510.
  - 1-NN label agreement: closest tenth 0.965, all 0.922, chance 0.847. This is the structure-activity signal (close analogs share the class), not a repost artefact.
- Task (5 of 9 splits): no flags. Dummy log loss 0.287; linear AUC 0.798 (log loss 0.726); random forest AUC 0.882 (log loss 0.185, skill +0.763 ± 0.007, above the dummy on 5 of 5); LightGBM 0.869; single feature 0.680. Spread +0.167. Smallest class per test fold: 236.
- Generated: no flag (rule leaves 0.0% of the minority).
- Hidden groups: 0 candidate columns. The probe is vacuous here: all 1,024 columns are binary, so none can look like an entity, and it cannot see a group that no single column defines (`task_probes.md`, "The probe checks single columns only"). The Tanimoto analysis below stands in for it.
- Extra (repeat 0, own script `scripts/similarity_bins.py`): random forest AUC by the test chemical's maximum Tanimoto similarity to train: below 0.5: 0.681 (about 324 test rows per fold); 0.5-0.7: 0.812 (1,221); 0.7-0.85: 0.945 (962); above: 0.954 (324). LightGBM and the kNN show the same pattern.
- Extra (`scripts/tanimoto_clusters.py`, added after the verification): single-linkage clusters of the 8,493 bit vectors. At Tanimoto 0.9: 8,231 clusters, 456 rows (5.4%) with any analog, largest cluster 6, the 708 very toxic chemicals in 692 distinct clusters. At 0.8: 6,903 clusters, 2,366 rows (27.9%) with an analog, largest 29, 577 distinct clusters for the very toxic ones. Analog density per class: an analog of at least 0.85 for 15.5% of the very toxic rows against 15.1% of the rest (median maximum similarity 0.735 against 0.710).

**Issues for Lennart:** the verifier (2026-10-07, verdict "ready with noted concerns") closed 1, 2 and 4 in favour of what is implemented and confirmed the domain in 5; only 3 needs a decision.
1. **Parent-structure copies dropped, unlike the source.**
   - Question: drop the salt-form copies (implemented) or keep the source's rows?
   - Evidence: 499 of 8,992 rows (5.5%) are dropped. The paper says "No molecules were removed". 7.6% of the authors' test molecules have an exact bit-vector copy in their training set. 237 of the project's 2,894 evaluation chemicals (8.2%) have their parent in the training file.
   - Implemented: drop exact copies and conflicting vectors (wine_quality / jm1 precedent).
   - Alternative: keep all 8,992 rows and group the split on the bit vector (8,504 groups). Each salt form keeps its own label, and a test parent is still never in train.
   - **Verification:** closed in favour of what is implemented. The drop is class-neutral (33 of 741 very toxic rows, 4.5%, against 466 of 8,251, 5.6%; the positive share moves from 8.24% to 8.34%), and it is exactly what `leak_checks.md` §5 prescribes (exact copies with one label dropped as in wine_quality, every copy of a both-class vector dropped as in jm1). The 11 conflicting vectors are real chemistry rather than label noise, so they are unpredictable from the bits either way, and 22 of 8,515 rows cannot move the score.
2. **Random split, while the score depends on close analogs.**
   - Question: is the IID split what you want for a QSAR set?
   - Evidence: random forest AUC rises from 0.681 for test chemicals with no training analog above Tanimoto 0.5 (11% of the test rows) to 0.954 for those above 0.85. Both source protocols are random. The real use is screening lists of regulatory interest (48,137 chemicals in the project's prediction set), which hold many analogs of tested chemicals.
   - Implemented: IID (no group key in the file; "hidden groups need context").
   - Alternative: a scaffold or cluster split. It needs structures. The UCI rows carry no identifier: within each block they look like CASRN order (next-row class agreement 0.873 against 0.876 in the NTP file), but linking them would need Dragon 7's ECFP. It would be a new dataset built from the NTP structures with a featurisation of our own, which I do not recommend.
   - **Verification:** closed in favour of the IID split. The clustering above shows no congeneric series to memorise (692 distinct clusters for 708 very toxic chemicals at Tanimoto 0.9, largest cluster 6 rows overall), and both classes have the same analog density, so the similarity gradient is the applicability domain every QSAR model has. Both source protocols are random, and the project's is structure-blind on purpose. After the deduplication no chemical occurs twice, so there is no repeated entity to hold out, and a similarity-threshold cluster is barred as a group key (`leak_checks.md` §5). The `curation_comments` "Note" bullet now carries these numbers.
3. **Only the calibration part of the VT data is on UCI.**
   - Question: extend the dataset with the project's evaluation set?
   - Evidence: the full VT data is 11,886 chemicals. The evaluation set (2,894 chemicals, 243 very toxic; labels in NTP `validationset.txt`) has fingerprints only in the Milano group's download ("Molecular descriptors calculated in this study for the training, test and validation molecules are available for download", Sec. 2.2). That download needs a form with your name and e-mail, and its site blocks this machine.
   - Implemented: UCI only (8,493 after deduplication).
   - Alternative: download the package by hand (up to +34% chemicals, fewer after the parent copies are dropped). The page offers "MATLAB code and data to reproduce the QSAR models" of the paper, so it presumably also holds the nontoxic (NT, LD50 >= 2,000 mg/kg) endpoint with ECFP_1024_05 bits, a better-balanced second task (3,848 of 8,981 positive, confirmed in the NTP file). Not verified: the package was not downloaded.
   - **Verification:** stays open, Lennart's call. The verifier did not try the form either and proposes no change to the shipped dataset.
4. **Scope of fingerprint features** (the notes asked).
   - Question: keep vectorised molecules in scope?
   - Evidence and implemented: kept, by the qsar_tid_11 precedent and the numbers in "Record judgment".
   - Alternative: a stricter modality rule would also remove qsar_tid_11 and hiva_agnostic.
   - **Verification:** closed, in scope. The guideline's exclusion covers features describing image content; a fingerprint is a vectorised molecular graph, qsar_tid_11 is the shipped precedent, and on our folds a random forest matches a nearest-neighbour model of the paper's own kind.
5. **Minor.**
   - The fingerprint variant is not stated (ECFP_1024_02 or _02R; the data fits 2 bits per fragment, so it is not _05). The comments say so. **Verification:** the verifier confirmed the three variants and their bits per fragment in Table 2, and that the two rows with 2 bits set are the two chemicals whose QSAR-ready structure is a single carbon.
   - `domain` follows the record ("chemistry & material science", as qsar_tid_11 and hiva_agnostic). qsar_biodeg, qsar_aquatic_toxicity, qsar_fish_toxicity, clock_protein_toxicity and bioresponse use "biology & life sciences"; one convention for these QSAR sets would be cleaner. **Verification:** closed, the value is right: UCI gives the subject area as "Physics and Chemistry". The inconsistency among the older folders is a separate question.
   - The BibTeX cites Ballabio et al. 2019 (key) and Mansouri et al. 2021 for the label data. **Verification:** matches UCI's citation request.
   - **From the verifier (orchestrator, run-wide):** the record has no `v2_path` and no `DF: Yes`; one `sync-notebooks` run at the end of the batch fixes it for all folders of this run.
6. **For the qsar_bioconcentration agent and the orchestrator:**
   - michem.unimib.it/download/data/ returns HTTP 503 (Wordfence) here, and its dataset pages go through a personal-data form. Use UCI or web.archive.org for the page text.
   - The archived page lists "Mechanisms of bioconcentration: QSAR dataset of 779 compounds, 9 molecular descriptors and 3 mechanistic classes of bioconcentration; experimental BCF and KOW values are also provided".

### rain_in_australia
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/rain_in_australia/`)

**Record judgment:** valid with concerns. The data is real and traceable: the R package rattle built weatherAUS from
the Bureau of Meteorology's daily weather observations ("Daily weather observations from multiple locations around
Australia, obtained from the Australian Commonwealth Bureau of Meteorology and processed to create this relatively large
sample dataset for illustrating analytics, data mining, and data science using R and Rattle", rattle docs, weatherAUS,
Description). The Kaggle dataset in the record is the uploader's snapshot of that file. No other record, no folder of
the working copy and no other record of this run holds weatherAUS (grep for jsphyg, weatherAUS, rattle, Bureau of
Meteorology); `climate_model_weather_forecasting_1m` is the TabReD/Yandex data. The open concern is the forecasting
scope (issue 4), which the curator's comment already weighs.

**Data:** the original rattle file `weatherAUS.csv`, pinned as the Internet Archive capture of 2026-10-05
(`https://web.archive.org/web/20261005005127id_/https://rattle.togaware.com/weatherAUS.csv`), byte-identical to the
live file downloaded on 2026-10-06 (last modified 2026-02-07; sha256 6598e685...); the same values are in CRAN rattle
5.6.2 (`data/weatherAUS.RData`, 0 of 275,410 x 24 cells differ). 275,410 rows x 24 columns, 49 stations, 2007-11-01 to
2026-01-30; no rows for any station in 2011-04, 2012-12, 2013-02 and 2016-01-27 to 2017-02-28. Saved as
`local-data-warehouse/rain_in_australia/weatherAUS_20260207.csv`. Licence: "Copyright Commonwealth of Australia 2010,
Bureau of Meteorology"; "The Bureau provided permission to use the data with the Bureau of Meteorology acknowledged as
the source of the data" (rattle docs, weatherAUS, Source and Description); rattle is GPL (>= 2) (CRAN); the Kaggle card
says "other"; BoM's default terms forbid supplying its content to others (noted in the definition).

**Definition:** prediction point = the 9 am observation at a station on day D; target `RainTomorrow` (more than 1 mm
read at 9 am on D+1, i.e. rain in the 24 hours after the prediction point); temporal on `Date`, 9 windows of 14 days,
one every 6 weeks from 2025-02-15 to 2026-01-30 (newest first, expanding train from 2007-11-01): 622-642 test rows of
46 stations with 63-205 rain days per window, train 248,740-263,940 rows, horizon 14 days. 264,562 rows x 22 features
(`Date` and `Location` included). Cleaning: the ten columns recorded after 9 am on D (MaxTemp, Sunshine, WindGustDir,
WindGustSpeed and the six 3 pm observations) replaced by their values of D-1 at the same station (`*_prev_day`);
`RISK_MM` dropped (RainTomorrow = RISK_MM > 1 mm in all 267,317 labelled rows); rows whose next row in the file is
more than one day later dropped (labels taken 29-401 days later; 180 rows); 8,093 unlabelled rows and 2,575 rows
without their own 9 am rain reading dropped. The same checksum under pandas 2.3.3 and 3.0.6 (`v2:fbb7970d...`).

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 info; nothing accepted. `pytest tests/test_v2_datasets.py -k
rain_in_australia` passes, also with `DATA_FOUNDRY_V2_DATA_CHECKS=1`. ruff clean.

**Probes:** (run with `--root` on a scratch folder holding only a symlink to this folder: discovery of the working copy
crashed on another agent's half-written `ashrae_great_energy_predictor_iii_1m`, whose `domain` was still `TODO`.)
- `leak_probes.py` (3 newest windows): all features ROC AUC 0.820; best single features Humidity9am 0.741, Rainfall
  0.672, Humidity3pm_prev_day 0.672; depth-2/3 tree 0.696/0.736; dropping any of the top three leaves 0.818-0.823; no
  exact feature copies across the split; 1-NN label agreement 0.825 in the closest tenth against 0.659 by chance,
  distance alone 0.602. The strongest missing indicator is Cloud9am (0.588): at the 28 stations where it is missing on
  5-95% of days, the gaps switch day to day and come on dry mornings (Humidity9am 62.7 against 70.6; rain follows in
  11.7% against 25.4%), and it tracks the past rain as much as the label (verifier: indicator AUC 0.600 for RainToday,
  0.595 for RainTomorrow). The 9 am report is made at the prediction point, so it is kept, with an Anomaly bullet.
- `task_probes.py` (9 of 9 windows): LightGBM 0.827, random forest 0.822, linear 0.797, best single feature
  (Rainfall, chosen 9 of 9 times) 0.694; log loss 0.379 against 0.508 for the dummy; LightGBM beats the dummy on 9 of
  9 windows (SE of its mean skill 0.036); spread LightGBM - linear +0.060 (paired SE 0.016); smallest class in a test
  window 63 rows. No flags.
- `generated_probes.py`: rule leaves cover 0.0% of the minority rows. No flags.
- `hidden_groups.py` / `group_probes.py`: not run (temporal task).

**Issues for Lennart:**

1. **Settled, for information: the prediction point is 9 am, not the row as published.** BoM reads rainfall "in the
   24 hours to 9am" (BoM, Notes to accompany Daily Weather Observations, IDCJDW0000), and RainTomorrow(D) =
   RainToday(D+1) on all 267,085 consecutive day pairs, so the label covers 9 am on D to 9 am on D+1. MaxTemp is the
   "Maximum temperature in the 24 hours from 9am", complete only at 9 am on D+1 when the label is read (MaxTemp(D) is
   at least Temp3pm(D) in 100% of 264,679 rows, at least Temp3pm(D-1) in only 75.5%), so the published row leaks. The
   other nine late columns (sunshine and gust "to midnight", six 3 pm observations) are recorded inside the label's
   window. Implemented: predict at 9 am on D with the ten columns taken from D-1 (garments precedent, `leak_checks.md`
   §3; the lagged values equal the raw D-1 values in every cell). LightGBM on three yearly windows: ROC AUC 0.900 as
   published, 0.846 implemented, 0.838 with the 9 am columns alone (log loss 0.306 / 0.370 / 0.377, prior 0.515).
2. **Test windows: 14 days every 6 weeks (implemented) or monthly?** Your comment on
   `climate_model_weather_forecasting` ("TabRed uses 1 month refit horizon. For weather this is a bit much. I would
   argue for one or two weeks at most?") sets the horizon. Implemented: `TemporalSplits(window=14, unit="days",
   n_windows=9, step=42)`, 9 two-week windows 2025-02-15 to 2026-01-30 that cover every season, 622-642 rows and 63-205
   rain days each. No other dataset spaces its windows yet (step larger than the window). Alternatives (README,
   decision 4): contiguous 14-day windows cover only 2025-09-27 to 2026-01-30 (619-640 rows, 83-205 rain days); 7 days
   every 6 weeks: 309-322 rows, 27-100 rain days; monthly: May 2025 to January 2026, 1,333-1,417 rows, 192-400 rain
   days; yearly: only 7 windows above the 50% train floor.
3. **Source version: original rattle file (implemented) or the Kaggle snapshot of the record?** The Kaggle file
   (record's `source_links`) is a snapshot to 2017-06-25: 145,460 rows, 140,787 after the first cleaning, no `RISK_MM`
   (a 2019 discussion thread still asks about it; the current Kaggle file is the version of 2020-12-11). The rattle
   file adds 2017-07 to 2026-01 but lacks 2016-01-27 to 2017-02-28 (the snapshot has it), and 1,135 of the 125,900
   rows both hold (0.9%) differ in at least one value (580 Rainfall, 184 RainTomorrow cells), so old values change
   between versions of the file. The definition uses `source = "Other"` (as `diamonds` for ggplot2) and
   `year = "2026"`; the record says Kaggle and 2017.
4. **Scope: forecasting or a fixed predictive task?** The target is the next value of a station's rain series, which
   the `el_nino_dataset` reasoning ("We do not predict a target that we would not automatically obtain at time point
   t") would call forecasting. The skill comes from the morning observations, not from the series: on the 9 monthly
   windows of the first version (verifier's run, LightGBM) ROC AUC is 0.856 with all features, 0.855 without Rainfall
   and RainToday, 0.732 with only the station's rain series, station and calendar, and 0.650 with station and
   calendar alone (log-loss skill 31.2%, 30.8%, 13.2%, 5.6%). Andrej accepted it ("Time-series data, but target is
   lagged. Might work as a task."), and `climate_model_weather_forecasting_1m` and `bias_correction` (Yes) are
   one-step weather tasks with covariates, so the dataset is added; the question stays open for you.
5. **Rows without their own 9 am rain reading dropped (2,575).** BoM: "Sometimes when the daily maximum and minimum
   temperatures, rainfall or evaporation are missing, the next value given has been accumulated over several days
   rather than the normal one day" (BoM notes, Data availability). These rows are 42.6% rain days against 21.8%, with
   a median next reading of 0.4 mm against 0.0 mm, so their label can cover 48 hours or more. Alternative: keep them
   (the model then learns the missing reading as a rain signal).
6. **Framework: `splits_comment` is not dedented.** `AbstractCuratedDataset.make_splits` stores the raw attribute
   (`plan.comment = self.splits_comment`, `src/data_foundry/v2/dataset.py` line 677) while the other text fields go
   through `clean_text`, so the README's Splits section (and the container) keeps the 8-space code indentation on
   continuation lines. Same in `coffee_rating_prediction` and `lending_club`. Not patched.
7. **Record pointers.** The record has no `v2_path` yet (`sync-notebooks` not run, per the brief); its
   `original_source` (Kaggle) and `year` (2017) differ from the definition (issue 3).

**Verification:**
1. Cross-gap labels (blocker): applied. Reproduced: RISK_MM equals the next row's Rainfall in 184 of 184 labelled rows
   whose next row is 29-401 days later (2011-03-31, 2012-11-30, 2013-01-31, 2016-01-25/26); 180 were in the frame. Rows
   whose next row is more than one day later are dropped, with a bullet and a README decision; the gap bullet now names
   the four missing periods and that 40 stations have 2016-01-26. The 2026-01-30 labels equal BoM's 2026-01-31 reading
   at 15 of 15 stations (re-run on the verifier's BoM sheets).
2. Window length: applied, issue 2 for Lennart. 14-day windows every 6 weeks, monthly as the alternative.
3. Scope numbers: applied to issue 4 (verifier's run, cited as such; not re-run on the new windows).
4. Issue 1 settled: applied. Reproduced MaxTemp(D) >= Temp3pm(D) in 100% of 264,679 rows and >= Temp3pm(D-1) in
   75.5%; MaxTemp's timing evidence is in the comment bullet.
5. CRAN copy: applied to `download_description` and the BibTeX note. Reproduced the tarball sha256 (8b226e45...),
   the live CRAN URL (4,595,591 bytes, 2026-02-08) and 0 differing cells against the CSV (pyreadr).
6. Licence note: applied as a `Note:` bullet (BoM default terms quoted from bom.gov.au/other/copyright.shtml).
7. Comment details: applied. Evaporation is now 425 of 450 (follows a calendar day without a reading; my 424 counted
   rows). The cloud count stays 28 with the cut-off now stated (missing on 5-95% of days, final frame; 29 at 2-98%).
   The record comment says RISK_MM is the next row's reading.

### rosbank1
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/rosbank1/`), fixed after verification (cut C: periods ending before 2018-01-01, monthly windows).

**Record judgment:** valid with concerns. Rosbank's "ML Competition" on Boosters.pro, 27 April to 28 May 2018 (`https://boosters.pro/api/champ/champ?champname=rosbank1` still serves the page content: dates, task texts, metrics AUC and RMSE, rules, leaderboards; 274 teams on task 1, best private AUC 0.8747). Data: card transactions of each client's three-month grace period of the «Сверхкарта+» card (first-place slides, K. Khrylchenko, 1 June 2018), two labels per client. The CoLES paper uses it (Babaev et al., SIGMOD 2022, arXiv 2002.08232v3, Sec. 4.0.1), matching the mirror (1,008,889 transactions, 10,217 clients, 5,000 labelled). The record's open point "might be streaming event data" resolves as: one transaction sequence and one label per client, so one row per client is a fixed predictive task; sequence models do not dominate it (CoLES Tables 6-7: aggregates 0.825, sequence models 0.817-0.843). Unique: no other record, run record or working-copy folder holds this data (grep for rosbank, lifestream, boosters, Сверхкарта: only the Alfa-Bank records). Concerns: the newest labels are right-censored (handled by the cut), the time column is estimated (issue 3), and the label draw date is unknown (issue 4).

**Data:** Hugging Face mirror `pytorch-lifestream/rosbank-churn` (formerly `dllllb/rosbank-churn`) at revision `aad1b512deaee7ffea4c289e496785bc9e17bd80`: `train.csv.gz` (4,646,502 bytes, sha256 `fe27320183acbe038577080ae8b30b9d7f7b8a40dd92cf43e405b56fdd6627f6`, the LFS object id), 490,513 transactions x 10 columns, 5,000 clients. The decompressed train.csv (sha256 `cd19fe2557a4364f85a27a248ca68cb06efcd2e0642cea98d9319e1e8f90e392`) is byte-identical to kianya/rosbank-competition `data/train.csv` (committed 2018-10-26; I re-checked) and Ikitan/ML-Rosbank-competition `train.csv` (verifier). `test.csv.gz` (518,376 x 8, 5,217 clients, no labels) is not used; a copy is in `_scratch_new65/rosbank1/`. Licence: none; the competition rules (API `regulations`) cover accounts, third-party software and prizes, not the data; the HF card has no licence field.

**Definition:** prediction point: at the end of a client's three-month grace period, from the card transactions up to then. Target `churn` = "Yes" when target_flag is 0 ("Значение 0 соответствует отказу, а значение 1 соответствует продолжению использования", the task text as copied by participants in 2018); target_flag is 1 exactly when target_sum (POS spend of the next three months) is positive. Features: the CoLES hand-crafted aggregates as pytorch-lifestream configures them for this dataset (count, sum, mean, std of amount; per value of trx_category (10), currency (810/978/840/other) and MCC (97 most frequent + other) the count, mean and std; distinct counts), `channel_type` (the acquisition channel, one value per client) as a categorical, and three dates (`first_transaction`, `last_transaction`, `period_end` = first transaction + 3 months, or the last transaction when later). Cohort: periods ending before 2018-01-01, so every label window closes by 2018-03-31, inside the transactions (they end 2018-04-02); 209 clients dropped. Regime: temporal on `period_end`, `TemporalSplits(window=1, unit="months", gap=3, min_train_fraction=0.5)`: test December 2017 (63 clients, 23 churned; train 3,566), November (123, 49; 3,078), October (515, 179; 2,559); the gap is the label delay. 4,791 rows x 347 features, 2,146 churned (44.8%). Dropped columns: target_sum (defines the label), cl_id (carries the label), PERIOD (month of TRDATETIME).

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 info (`dataset_duplicate_rows`: 2 rows, two pairs of distinct clients with identical aggregates, the same label and period_end; kept). Accepted: `splits_rows_unused` (the 524 clients whose period ends in September 2017 sit in the label gap of all three windows; the December window trains on periods ending by 31 August). pandas 2.3.3 and 3.0.6 give the same checksum, `v2:9171bc6ef15a2094d2e9acf054972c23014a1047450f0b1059bfd5a2dbbcc74e`. `pytest -q tests/test_v2_datasets.py -k rosbank1` (with `DATA_FOUNDRY_V2_DATA_CHECKS=1`): 2 passed. ruff check and format clean; `dataset list` shows the folder as checked with no skipped folders.

**Probes:** (cohort C; outputs in `<scratch>/probes_c/`, the first round in `<scratch>/probes/`)
- Leak: all features 0.844 ROC AUC; strongest single features `nunique_mcc` and `channel_type` 0.738, `count_mcc_5812` (restaurants) 0.726; depth-2/3 tree 0.783/0.800; dropping `channel_type` costs 0.020, the others nothing; best missing indicator 0.694 (`std_amount_mcc_5812`); 0% exact copies; 1-NN 0.571 among the closest tenth (all 0.603, chance 0.505); NN distance alone 0.662. No flag.
- Task: LightGBM 0.859 (log loss 0.468 vs 0.687), random forest 0.857, linear 0.814, single feature 0.733 (`channel_type`, 3 of 3 windows); beats the dummy on 3 of 3 windows; smallest class per test fold 23. The first round's `unstable` is gone; new flag `no_spread` (skill gap LightGBM - linear 0.091, paired SE 0.071 over 3 windows, i.e. 0.045 vs 0.036 in AUC): 3 windows cannot test that gap; kept as electric_motor_temperature_prediction, recorded in curation_comments.
- Generated: no rule leaves. No flag.
- hidden_groups / group_probes: not run (temporal task, one row per client).
- Own window scores (untuned, newest first): LightGBM 0.854 / 0.880 / 0.834, random forest 0.860 / 0.892 / 0.845; without the gap 0.840 / 0.877 / 0.864; random 3 x 3 split 0.824.

**Fix round (verifier, 2026-10-07): each finding checked against the data**
1. Major, right-censored newest labels: applied. Re-checked: the API gives date_start 2018-04-27 and date_end 2018-05-28; March 2018 churn is 24/36 against 35.5% for Oct 2017-Feb 2018 (binomial p = 0.00014); client 2143 made 196/224/253 POS purchases in Dec-Feb and is labelled churned; client 905 (first transaction 2018-03-27) has target_sum 124,322. Cut C and monthly windows as proposed; the Cohort bullet, a `_decisions` table (period_end month, clients, churn share, month the label window ends, kept), the splits_comment and the constant `LABELS_COMPLETE_BEFORE` carry it. Cut B recorded as issue 4.
2. Minor, the page is online: applied. GET on the page answers 200 (my earlier 404 came from a HEAD request); fixed download_description (API URL, no data files listed there, mirror byte-identity), licence reason, BibTeX (`Rosbank2018MLCompetition`, "Rosbank {ML} Competition", dates and metrics in the note), and the first bullets quote the official English task text.
3. Minor, label orientation documented: applied (parusss/RosbankMLCompetition18 README and the kianya notebook quote; «Сверхкарта+» from the first-place slides).
4. Minor, channel_type is the acquisition channel: applied (kianya notebook 2018: "клиент привлекается лишь однажды и с самого начала его записи присваивается значение канала привлечения"; first-place slides). Issue 7 of the first round closed.
5. Minor, cl_id leaks the label: applied as a reason in curation_comments (re-checked: AUC 0.728 alone, churn by id decile 12% to 68%; the winner used "ID клиента").
6. Minor, duplicate count: applied (828 rows repeat all ten columns; 1,482 repeat client, time, MCC and amount; both re-counted).

**Issues for Lennart:**
1. **Target: churn or the spend regression.** The two tasks are one signal (target_flag = target_sum > 0). Implemented: churn (task 1, AUC; the task CoLES and pytorch-lifestream benchmark). Alternative: a `rosbank1_reg` folder for task 2 (scored with RMSE; best private 3.844, so probably on a log scale). On the shipped windows, untuned LightGBM R^2 is 0.43 / 0.46 / 0.37 on log1p(target_sum) over all clients (44.8% zeros, mostly the churn task again) and 0.26 / 0.12 / 0.15 on the log spend of the 2,645 clients who kept buying (40, 74 and 336 test clients); random 3 x 3: 0.38 and 0.21.
2. **Regime: temporal with a 3-month gap, or the competition's random split.** Implemented: temporal (clients are scored as their periods end; a refit only knows outcomes three months old; churn drifts from 53.0% in 2017Q1 to 35.8% in 2017Q4 as the type2 acquisition channel grows from 17% to 41%). Cost: the gap and the 50% floor leave October-December 2017 as the only test months (701 clients). Alternative: IID 3 x 3 over the 4,791 clients, the competition's and CoLES's protocol: LightGBM 0.824 (SE 0.001).
3. **The time column is an estimate.** No product or period dates in the data. 2,939 of 5,000 clients transact over 80-92 days, so `period_end` = first transaction + 3 months, or the last transaction when later (565 clients; 213 have over 100 days of history, which the release does not explain). Alternative: the last transaction date (simpler), but a client who stopped early would sit up to three months before its real period end.
4. **Cut C or cut B (when were the labels drawn?).** Implemented C: periods ending before 2018-01-01, label windows closing by 2018-03-31, inside the transactions (they end 2018-04-02), which is safe whatever the draw date before the opening on 2018-04-27. Alternative B: keep January 2018 too (label windows close by 2018-04-30, complete only if the labels were drawn at the very end of April): a fourth window of 62 clients (18 churned, train 4,090), LightGBM 0.813 in my run (0.822 in the verifier's). January's churn (29.0%) does not look censored, February's (39.6%) slightly, March's (66.7%) clearly, which fits a draw in late April; nothing published gives the date.
5. **Feature width.** The 97 MCC codes give 294 of the 347 features, mostly empty. Untuned LightGBM, mean over the shipped windows / random 3 x 3: no MCC breakdown (53 features) 0.847 / 0.820, 10 codes (86) 0.860 / 0.823, 30 codes (146) 0.863 / 0.822, 97 codes (347) 0.860 / 0.817. Implemented: 97, faithful to the published baseline (as alfa_battle_2_0_task_2 kept its organizers' set). Alternative: 10 or 30 codes.
6. **Test windows are small.** December 2017 holds 63 clients (23 churned) and November 123 (49): above the ~50-row guideline, but the task probes cannot separate model families over 3 windows (`no_spread`). A longer history does not exist in the release.

### sasol_customer_retention_recruitment_competition
**Outcome:** not added (duplicate of `expresso_churn_prediction_1m`). The Sasol files are a renamed 70% row sample of
Expresso's Train.csv plus all of Expresso's Test.csv. They cannot be downloaded either: Zindi limits the competition to
South African citizens, and no mirror of Train.csv or Test.csv exists.

**Record judgment:** do not add. It is the same underlying data as the working copy's
`datasets/_dev/tabarena-v0pt2/expresso_churn_prediction_1m/` (record `expresso_churn_prediction`, also in this run).
Criterion 1, "Unique"; curation guidelines: "Different versions / cuts of one underlying dataset are duplicates too".
The record's comments do not weigh this ("Awesome dataset, but restrictive license").
- **Variable list.** The competition's VariableDescription.csv is the English column of Expresso's
  VariableDefinitions.csv, line for line. Source: GitHub `DrUkachi/sasol-customer-retention`, 796 bytes, the size the
  Zindi API lists.
  - Both have the same 19 variables in the same order and the same wording: "The churn dataset includes 19 variables
    including 15 numeric variables and 04 categorical variables"; mrg: "a client who is going".
  - Renamed: MONTANT → Amount, FREQUENCE_RECH → refill_frequency, ORANGE → Procuct_1, TIGO → Procuct_2,
    CHURN → Target, user_id → ID. "income" became "revenue" and "inter expresso call" became "call within network".
  - The header "Variable Definitions,Unnamed: 2" is what pandas names the third column of Expresso's file. The French
    column was dropped.
- **Row counts.** The Sasol counts come from public notebooks:
  - GitHub `Ambiqour/Sasol-Customer-Retention-Prediction`, "Sasol Customer Retention Recruitment(LightBGM).ipynb",
    cells 12-21;
  - GitHub `MakalaMabotja/Customer-Churn-Prediction-Competition-Sasol--Zindi-`, "Churn Data EDA.ipynb", cells 3, 4, 30.

  Train.csv:
  - 1,507,834 x 19 rows = 0.700000 x Expresso's 2,154,048.
  - The non-missing count of each of the 17 columns is 0.698-0.701 of Expresso's.
  - Churn rate 18.736% against 18.755%.
  - The 14 regions keep Expresso's rank order at 0.680-0.704 of its counts (Mandalore 359,443 = 0.700 x DAKAR
    513,271).

  Test.csv:
  - 380,127 x 18 rows; SampleSubmission.csv holds 380,127 IDs (6,842,296 bytes, the size the API lists).
  - Expresso's Test.csv has 380,127 rows, and the non-missing counts agree in all 17 columns.
- **Rows.** The notebook prints 6 train rows and 4 test rows with activity values (cells 12, 13, 18). Each matches
  exactly one Expresso row on the 12 columns Sasol left unscaled.
  - Each train row is found only in Train.csv, and each test row only in Test.csv.
  - The 6 train labels agree.
  - Amount, revenue and arpu_segment are Expresso's values divided by 2.34 (ratios 2.33998-2.34002).
  - The regions are renamed one to one: Droidika = THIES, Eclipsara = SAINT-LOUIS, Celestial = LOUGA,
    Luminous = DIOURBEL, Nebula = TAMBACOUNDA and Astral = FATICK. Each of these sits at the same rank in the counts.
- **Content.** The data are not Sasol's customers. The columns hold Senegalese telecom usage: on-net calls, calls to
  the competitors Orange and Tigo, data volume, and top packs priced in F CFA. "All-net 500F=2000F;5d" is the most
  frequent pack in both train files.
- **Reproduce:** `<scratch>/evidence_duplicate.py`, output in `evidence_duplicate.txt`. The notebook outputs used are
  in `<scratch>/nb_dumps/`.
- **The other churn data** of the working copy and this run hold other data: churn_telco_south_asia / nigeria / europa,
  mobile_churn (66,469 x 66, prepaid accounts in 2013) and rosbank1 (card transactions). Only
  expresso_churn_prediction_1m has these columns.

**Data:** none downloaded for this record. Nothing is in `local-data-warehouse/`.
- **Source:** Zindi "Sasol Customer Retention Recruitment Competition". It ran from 5 October to 26 November 2023, with
  253 participants and 56 on the leaderboard. The metric was F1; the prize rules weigh it 60%, with 20% for approach
  and 20% for a presentation.
  - API: `https://api.zindi.world/v1/competitions/sasol-customer-retention-recruitment-competition`
    (`api.zindi.africa` redirects there).
  - Data page: "There are 1.88 million clients in this dataset. There are 1.5 million clients in train and 380,000
    clients in test."
  - Files: Train.csv (147,175,227 bytes), Test.csv (36,386,546), SampleSubmission.csv (6,842,296) and
    VariableDescription.csv (796).
- **Blocked:**
  - The API returns `is_access_restricted: true`, and the Rules page says "this challenge is open to South African
    citizens only".
  - Kaggle searches (sasol, sasol customer, sasol churn, customer retention zindi, zindi churn) find no copy.
  - GitHub has four repositories under the competition's name. Only `DrUkachi/sasol-customer-retention` holds
    competition files (SampleSubmission.csv and VariableDescription.csv, besides its own submissions); the others
    hold notebooks.
  - A code search for `Procuct_1` finds notebooks and VariableDescription.csv copies only.
  - Hugging Face has no dataset matching "sasol".
- **Licence:** the Rules page says "The data used in this competition is the sole property of Zindi and the competition
  host. You may not transmit, duplicate, publish, redistribute or otherwise provide or make available any competition
  data to any party not participating in the Competition (this includes uploading the data to any public site such as
  Kaggle or GitHub)." Noted only.
- **Verification copy:** for the comparison, I downloaded Expresso's Test.csv (Kaggle
  `hamzaghanmi/expresso-churn-prediction-challenge` version 1, 380,127 rows) into
  `_scratch_new65/sasol_customer_retention_recruitment_competition/expresso_test/`. Expresso's Train.csv is the
  existing warehouse file of expresso_churn_prediction.

**Definition:** none (no folder was created).

**Checks:** none (no folder).

**Probes:** none run. There is no Sasol data, and its rows are Expresso rows; the expresso_churn_prediction unit's
probes cover them.

**Issues for Lennart:**
1. **Verdict.**
   - Question: should this record go to No + Duplicate of expresso_churn_prediction?
   - Evidence: above.
   - Implemented: nothing added.
   - Proposal: No + Duplicate. By the convention the record becomes `expresso_churn_prediction_duplicate`. The
     expresso unit proposes `indabax_eswatini_2022` as a duplicate of the same data, so one of the two needs another
     name (your call).
   - Alternative: none worth keeping. The Sasol cut is a subset (70% of the labelled rows) with renamed regions and
     rescaled money, and its files cannot be obtained.
2. **The `Non-IID (Temporal)` tag has no basis.** None of the 19 columns is a date, and the Expresso extract is one
   snapshot of the customer base (expresso_churn_prediction_1m `curation_comments`). This is moot if the record goes
   to No.
3. **GETTING_STARTED.md lists this record.** `datasets/_dev/tabarena-v0pt2/GETTING_STARTED.md` line 172 lists it among
   the large candidates ("90-day customer inactivity (~1.5M clients)"). If the record goes to No, that row goes too.
   Not edited, per the brief.
4. **Optional provenance line for expresso_churn_prediction_1m.** Its `curation_comments` list the Zindi re-runs of
   Train.csv. Sasol's 2023 recruitment competition is one more: 70% of the train rows, all of Test.csv, renamed
   regions, money divided by 2.34. Not edited, since it is another unit's folder.
5. **FYI, no action: the "simulated" suspicion.**
   - Participants suspected simulated data (skaak in discussion 19432: "I think the data is simulated and probably 0.7
     is the built in max"; in 19601: "I started to (and still do) suspect that the data is simulated and not real").
   - The reuse explains it. The rows are real Expresso rows, and Zindi's test set is a random sample of the same
     extract. The expresso unit found that a model separating the two files scores ROC AUC 0.500.
6. **FYI: a different Sasol competition with a Kaggle copy.**
   - Zindi's "Sasol Customer Value Recruitment Challenge" runs from 23 September to 18 October 2026 and is still open.
     It is scored on "CLV fuel", "CLV non-fuel" and "Opportunity"; its train.csv "is transaction data" (Zindi API).
   - The Kaggle upload `kimp1995/sasol-customer-value-recruitment` (2026-10-02) has the file sizes the Zindi API lists
     for that competition, among them LABEL_RULES.md and label_rules.py.
   - It is not this record's data. It would be a new candidate with its own triage. I did not look at its labels.
7. **Housekeeping.** `_scratch_new65/sasol_customer_retention_recruitment_competition/expresso_test/Test.csv` (45 MB)
   is kept so the verifier can rerun `evidence_duplicate.py`. Delete it after verification.

### stroke_prediction
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/stroke_prediction/`), built from the original contest file instead of the record's Kaggle cut. After verification I recommend `No` (issue 1). The folder stays until Lennart decides.

**Record judgment:** valid with concerns, now leaning do not add (criterion 4B, partly generated data; issue 1). Provenance is traced, but the data are partly generated or altered.
- fedesoriano's Kaggle file (5,110 rows) is a cut of `train_ajEneEa.csv`, the training file of the McKinsey Analytics Online Hackathon - Healthcare Analytics (Analytics Vidhya DataHack, 2018-04-14; page JSON `startDate`, metric "AUC ROC score").
- The cut is the file's first 249 stroke rows and first 4,861 other rows. All 5,110 match by Patient ID with identical values.
- The same file, byte for byte (sha256 540986ae...), is Liu, Fan & Wu's Mendeley Data deposit (doi:10.17632/x8ygrw87jw.1). Their abstract (Artif. Intell. Med. 101:101723, 2019) reads: "43,400 records of potential patients which includes 783 occurrences of stroke".
- Unique: no other stroke data in the working copy or the records.

**Data:**
- Used: `https://datahack-prod.s3.amazonaws.com/train_file/train_ajEneEa.csv` (contest page link), 43,400 x 12, 783 strokes (1.8%). The Mendeley copy is the fallback in `download_description`.
- Not used: the test file (18,601 rows, no labels).
- Licence: none on the contest page. The Mendeley copy is CC BY-NC 3.0 (DataCite). The Kaggle cut says "(Confidential Source) - Use only for educational purposes".

**Definition:**
- Prediction point: a patient's EHR record at the hospital chain, the contest's cross-sectional "has had a stroke" task (no dates).
- Target `stroke` (No/Yes), ROC AUC. IID, 3 x 3 folds, 261 strokes per test fold.
- 43,400 rows x 9 features.
- Dropped: `id` and `bmi` (leak, verification finding 2).
- Kept as published, flagged in an Anomaly bullet: Residence_type, ever_married, work_type and the low end of glucose.
- Blank smoking status stays missing.
- Three `_decisions` tables: the contest file against the Kaggle cut; BMI missingness by age band and stroke; the three columns by age and sex.
- Same container under pandas 2.3.3 and 3.0.6 (checksum v2:7d48c78d...). pytest passes (2 passed, raw-data rebuild included).

**Checks:**
- 0 errors, 0 warnings.
- One accepted: `dataset_pure_feature_value` (work_type children: 6,156 patients aged 0.08-16, 2 strokes; an age effect).
- One info: `dataset_duplicate_rows`, 62 rows once bmi is gone. These are pairs that differ in BMI in the raw file, i.e. different patients, so they are kept.

**Probes (2026-10-06, without bmi):**
- Task probe (9 of 9 splits): linear AUC 0.850, LightGBM 0.829, random forest 0.808, age alone 0.831; no flags (age at 94.5% of the best skill).
- Raw age on 9 splits: 0.840. Regularised LightGBM 0.850 and spline logistic regression 0.850 both beat it on 9 of 9 splits, by 0.010. Untuned LightGBM (0.824) is below age on 9 of 9.
- Leak probe: all features 0.826, depth-3 tree 0.831, 0.724 without age, 0.2% exact copies (the pairs), 1-NN agreement at chance, NN distance 0.690.
- Generated-data probe: 0 rule leaves. Hidden-group probe: 0 candidates.
- My scripts for the second check: `refute_generated.py`, `refute_calibrate.py`, `exp_models2.py`.

**Issues for Lennart:**
1. **The file is partly generated or altered. Recommendation: `No` + `AHDS` / `Data Quality Issue`**, retire the folder. The record accepted "might be fake ... use it for now and filter later if needed"; the evidence now says filter.
   - Residence_type, ever_married and work_type carry nothing beyond age. Likelihood-ratio tests with 1-year ages against all other columns give p = 0.47, 0.39 and 0.68-0.88 (test file 0.24-0.85); the sex column gives p = 7e-145.
   - LightGBM predicts each of them as well from age alone as from all columns, e.g. married 0.840 / 0.837. The same test on 35,850 BRFSS 2015 adults does find dependence: metro 0.505 -> 0.558, married 0.713 -> 0.761, self-employed 0.615 -> 0.694.
   - Married at 25-29: 45.0% of women and 45.0% of men (BRFSS: 53.8% / 40.3%). Work types are identical by sex (p 0.64-0.79).
   - Residence_type is a 50/50 coin, independent of everything (p 0.29-0.98).
   - Glucose has no value below 55.00, is flat at 55-64 and doubles at 65, in both contest files. 9.8% of patients have a post-meal glucose below 66 mg/dL.
   - The clinical columns look real (male x heart disease age-adjusted OR 2.28; BRFSS 1.87).
   - Precedents: churn and customer_satisfaction_in_airline were retired. The Analytics Vidhya siblings are held at 2nd tier.
   - If kept: add `data_tags = ("2ndTierData",)` and drop the three columns. They add nothing: regularised LightGBM 0.850 with and without them, per split -0.002 to +0.002.
   - **Verification:** verifier finding 1 accepted after a second check with separate code. Every test and number held. BRFSS marriage at 25-29 is 53.8% / 40.3% with MARITAL 1-4 out of 1-5; the verifier's 51.6% / 36.1% used a different denominator. Bullet rewritten. The three columns are kept as published with an Anomaly bullet that names dropping them as the option, as the coordinator asked.
2. **Version shipped: the contest's full training file, not the record's Kaggle cut** (8.5x the rows, 3.1x the strokes; 261 against 83 per test fold).
   - Alternative: the 5,110-row Kaggle file.
   - Record fields to update (orchestrator): `original_source` (-> the contest, `Other`), `year` (2021 -> 2018), `source_links` (+ contest page, DOI), `v2_path` (sync-notebooks).
   - **Verification:** finding 5 confirms this; the orchestrator handles the record.
3. **bmi dropped as a leak: a missing BMI follows the stroke.**
   - With 1-year ages, sex, marriage, residence, hypertension, heart disease, glucose, smoking and work type fixed, a stroke multiplies the odds of a missing BMI by 3.69 (2.99-4.57). That is more than hypertension (2.50) or heart disease (2.19), and holds at 2.95-4.12 in every adult age band.
   - Smoking-status missingness does not follow the stroke (OR 0.96, 0.80-1.16).
   - BMI values add nothing beyond the missingness: 0.861 as is, 0.847 without the column, 0.846 with missing values drawn at random.
   - Alternative: keep bmi with a "Potential leak, kept on purpose" bullet (+0.014 AUC).
   - **Verification:** verifier finding 2 accepted; reproduced at 3.69 against the verifier's 3.64. My earlier "not specific to strokes" was wrong and has been removed.
4. **Age dominates.** Without bmi, the strong models beat raw age (0.840) on 9 of 9 splits, but only by 0.010. Not `Trivial` by rule 4, as in the sepsis_survival precedent. With three noise columns, the signal beyond age comes from sex, hypertension, heart disease, glucose and smoking. This adds to issue 1.
5. **Cross-sectional label.** The features may postdate the stroke; the file has no dates. Documented in the prediction-point bullet (as cdc_diabetes_health_indicators does).
6. **Anomalies kept.**
   - Ages under 2 are written as years plus 0.08 per month (0.08-0.88, 1.0-1.88).
   - Ages 78-82 are over-full (435-698 per year against 336-446 at 70-77), as if older ages had been folded in.
   - There are strokes at ages 1.32 and 14.
   - **Verification:** verifier finding 3 accepted; the age wording is fixed.
7. **Reproducibility of the fallback.** The Mendeley RAR needs an extractor; none is installed here. `download_description` now gives `7z e` / `bsdtar -xf` / `unrar e`, plus a `uv run --with unrar-cffi` one-liner tested today (sha256 540986ae...).
   - **Verification:** verifier finding 4 accepted.
8. **Probe harness (framework note).** Strict discovery in the probe scripts crashed on another agent's TODO scaffold (`qsar_bioconcentration`). I ran them with `--root` pointing at a scratch folder holding a symlink to this dataset.

### brca_breast_cancer
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/brca_breast_cancer/`), revised after verification: the expression block is no longer a feature.

**Record judgment:** valid with concerns.
- Suspension: no reason is recorded. The record has no comment on it, `git log` shows the status arriving with the sheet import (391cf7a, 2026-06-23), and no notebook exists. The other omics notebooks in `datasets/_maintenance/_suspended/` (DLBCL, lymphoma9) are wide gene-expression sets without a stated reason either, which points to width. Width has a precedent now: `lung_cancer_epithelial_genexp` (187 x 22,215) ships, with BeyondArena results from 12 families of `beyond_iid_benchmark_2026` and 9 foundation models of `beyondarena-2026-09-22`.
- Source and target: Rappoport & Shamir 2018 (NAR 46:10546) packaged TCGA omics from Broad Firehose and phenotypes from UCSC Xena (Supplementary File 2: BIC, 621 samples). The source is a clustering benchmark (Sec. "Benchmark") without a target. TabPFN-Wide v1 (arXiv 2510.06162v1, Sec. 5 "Datasets and Evaluation Protocol") classifies the PAM50 call `PAM50Call_RNAseq` (loader `analysis/load_mm_data.py`, `subtype_labels=True`): five classes, not binary.
- Uniqueness: no other TCGA breast data in the working copy or the records. The MLOmics folders of this run (coad, lgg, ov) are other cancers; TabPFN-Wide v2 uses MLOmics GS-BRCA (same TCGA patients), for which no record exists.
- Main concern, now acted on: the label is the PAM50 rule applied to the expression block (issue 1).

**Data:** https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/breast.zip (`exp` 20,531 genes x 1,212 samples, `methy` 5,000 probes x 885, `mirna` 1,046 x 849) and clinical.zip (`clinical/breast`); files dated 16 July 2018, md5 in `download_description`. Licence: the page's footer reads "© All rights reserved" (the HTML template's); TCGA open-access tier.

**Definition:** prediction point: a primary breast tumour profiled by DNA methylation and miRNA-seq; the model assigns the PAM50 subtype its RNA-seq would get. Target `pam50_subtype` (multiclass, log loss): Luminal A 188, Luminal B 98, Basal-like 56, HER2-enriched 25, Normal-like 14. IID, 20 x 3 stratified folds (train 254, test 127). 381 rows x 5,864 features (`Methy_` 5,000, `miRNA_` 864 after dropping 178 all-zero and 4 duplicated columns). Rows: primary tumours of the benchmark's 621 patients with all three omics (the expression file only selects them; methylation + miRNA alone give the same 381), then patients with a PAM50 call.

**Checks:** `dataset check`: 0 errors, 0 warnings, 0 info (26 checks); no accepted warnings. Checksum v2:a40e0fa2... equal under pandas 2.3.3 and 3.0.6 and in README.md. `pytest tests/test_v2_datasets.py -k ...`: 3 passed, 3 skipped. `ruff check` and `ruff format --check` clean.

**Probes** (private root of symlinks; 2 threads):
- leak (my wrapper of `leak_probes.py`: single columns only for the 300 with the highest rank AUC on the train sides; the rest is the script's code): all features macro AUC 0.916; depth-2/3 tree 0.727/0.772; best single column 0.803 (`Methy_cg22678977`); drop-one of the top 3: 0.917; exact copies 0.0%; 1-NN agreement 0.614 (closest tenth 0.692, chance 0.337). No flag.
- task (30 of 60 splits): dummy log loss 1.280; random forest skill 0.485 (macro AUC 0.937, log loss 0.660, 30 of 30 splits, SE 0.003), logistic regression 0.389 (0.933), LightGBM 0.252 (0.922, overconfident); single column skill -0.003 (0.743); smallest class per test fold 4. No flag.
- generated: 0.0% rule leaves. hidden groups: 0 candidates.
- by hand, tissue source site (17 sites, largest 16%; Cramer's V 0.24): random forest macro AUC 0.939 random vs 0.943 by site, log loss 0.662 vs 0.656. IID kept.

**Issues for Lennart:**
1. Feature-defined label (implemented: drop the expression block). The published PAM50 centroids (perou-lab/PAM50_classifier, Spearman, no training) on the 50 genes of `exp` reproduce 347 of 381 calls; a logistic regression on the 5 centroid correlations reaches log loss 0.35-0.39 and macro AUC 0.985-0.988, ahead of a random forest on all 26,035 omic columns (0.549, 0.973) on every split (verifier: 30 of 30; my check: 9 of 9). Precedent: sdss_17 drops `redshift`, the quantity the label is defined from. Alternatives: (a) retire as `Trivial` / `AHDS`; (b) keep the paper's all-omics task (TabPFN-Wide comparability) with the rule documented.
2. Record fields: `problem_type` should be Multiclass Classification; `DF: Suspended` has no recorded reason. Comment in `brca_breast_cancer.record_comment.md`.
3. Paper version: TabPFN-Wide v2 takes BRCA and GBM from MLOmics. Implemented: the record's Rappoport & Shamir files (v1). Adding MLOmics GS-BRCA as well would duplicate these patients.
4. Normal-like has 14 patients, 4-5 per test fold. Kept (≥10, the paper's five classes). Alternative: drop it (367 rows). TabPFN-Wide's 440 samples include 56 adjacent normal samples (49 called Normal-like) that the primary-tumour filter drops.
5. `source = "Other"` (the Shamir lab's files); the measurements first appeared at TCGA, which would be "GOV Website".
6. Framework: `leak_probes.py` fits one LightGBM per column and split and hard-codes `n_jobs=8` (78,000 fits at 26k columns), hence the screened wrapper (`explore/leak_probes_wide.py`). All probe scripts and `tests/test_v2_datasets.py` import every folder under `--root`, so another agent's half-written folder crashes them (seen with `ashrae_great_energy_predictor_iii_1m` and `corporate_credit_rating`).

**Verification:**
- Finding 1 (blocker, label is the PAM50 rule): applied. Reproduced 347 of 381 and the rule beating the forest on 9 of 9 splits; the `mRNA_` block is no longer a feature (exp only selects the patients). Retirement is alternative 1a.
- Finding 6 (comment, licence): applied. The comment explains the 440 TabPFN-Wide samples; the licence string quotes the page's "All rights reserved" footer. The suspension stays an open point.
- Finding 5 (site): the site check was rerun on the new features: no gap (0.939 vs 0.943).

**Resolved (Lennart, 2026-10-12; confirmed on the review page 2026-10-15):** No, `No Good Target / Scientific Discovery`: the PAM50 subtype is a clustering taxonomy assigned by a centroid rule on 50 genes. The folder is removed.

### glioblastoma
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/glioblastoma/`), revised after verification: the expression block is no longer a feature.

**Record judgment:** valid with concerns.
- Suspension: no reason recorded (as BRCA).
- Source and target: Rappoport & Shamir 2018, GBM: 274 samples, "HT-HG-U133A", "Illumina-27k", "UNC-miRNA-8x15K" (Supplementary File 2). TabPFN-Wide v1 used GBM for model selection (Sec. 4.2), with `GeneExp_Subtype`: four classes, not binary.
- Label provenance: `GeneExp_Subtype` equals `EXPRESSION_SUBTYPE` of cBioPortal `gbm_tcga_pub2013` for 271 of 274 patients (that study's 23 G-CIMP tumours are Proneural here; 3 absent). Brennan et al. 2013 (Cell 155:462), section "Molecular subclasses defined by global mRNA expression and DNA Methylation": "Samples not included in previously published analysis (n=342) were classified into one of classes using single sample gene set enrichment analysis".
- Uniqueness: `glioma_grading_clinical_and_mutation_features` shares TCGA-GBM patients (180 of 274 by the verifier's count) but has mutation and clinical features and an LGG-vs-GBM target; not a duplicate.

**Data:** https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/gbm.zip (`exp` 12,042 x 538, `methy` 5,000 x 285, `mirna` 534 x 575) and clinical.zip (`clinical/gbm`). Licence as BRCA.

**Definition:** prediction point: a primary glioblastoma profiled by methylation and miRNA arrays; the model assigns the expression subtype its expression would get. Target `expression_subtype` (multiclass, log loss): Mesenchymal 84, Proneural 72, Classical 71, Neural 47. IID, 20 x 3 stratified folds (train 182-183, test 91-92). 274 rows x 5,534 features (`Methy_` 5,000, `miRNA_` 534; none constant or duplicated). Rows: the benchmark's 274 patients with all three omics (methylation + miRNA alone would add 3).

**Checks:** 0 errors, 0 warnings, 0 info; no accepted warnings. Checksum v2:b8eebd79... equal under pandas 2.3.3 and 3.0.6 and in README.md.

**Probes:**
- leak: all features macro AUC 0.878; depth-2/3 tree 0.746/0.746; best single column 0.731 (`Methy_cg00891541`); drop-one 0.876-0.878; exact copies 0.0%; 1-NN agreement 0.446 (closest tenth 0.900, about 9 rows; chance 0.260). No flag.
- task: dummy log loss 1.366; random forest skill 0.361 (macro AUC 0.876, log loss 0.874, 30 of 30 splits, SE 0.003), logistic regression 0.281 (0.895), LightGBM 0.063 (0.888, overconfident); single column skill -0.064 (0.683); smallest class per test fold 15. No flag.
- generated: 0.0% rule leaves. hidden groups: 0 candidates.
- by hand, tissue source site (12 sites, largest 16%; Cramer's V 0.22): random forest macro AUC 0.873 random vs 0.880 by site, log loss 0.872 vs 0.893. IID kept.

**Issues for Lennart:**
1. Feature-defined label (implemented: drop the expression block). The Verhaak class gene sets (MSigDB) scored on the U133A block reproduce 216 of 274 labels (verifier's count, rechecked); a logistic regression on the 4 set scores (log loss 0.645) beats the probe's LightGBM (0.693) and random forest (0.777). Without the block: random forest macro AUC 0.876, log loss 0.874 (dummy 1.366). Alternatives: (a) retire; (b) keep the all-omics task. One decision with BRCA and the MLOmics OV folder (TCGA 2011 expression clusters).
2. Record fields: `problem_type` Multiclass; suspension reason unknown. Comment in `glioblastoma.record_comment.md`.
3. Paper version: as BRCA issue 3.

**Verification:**
- Finding 2 (label is an expression call): applied. Brennan 2013 quote confirmed in the PMC text and added to the comment; 216 of 274 and the cBioPortal match (271 of 274) rechecked; the `mRNA_` block is no longer a feature.
- Finding 5 (site wording): applied. The comment now gives the forest's numbers; on the new features there is no by-site gap (the earlier LR jump to log loss 1.41 was overconfidence on the expression block).

### sarcoma
**Outcome:** added and checked (`datasets/_dev/tabarena-v0pt2/sarcoma/`), revised after verification: the label is TCGA's expert-reviewed histology.

**Record judgment:** valid with concerns (the label is the pathology diagnosis, not an omics output).
- Suspension: no reason recorded.
- Source and target: Rappoport & Shamir 2018, SARC: 257 samples (Supplementary File 2). TabPFN-Wide v1 Table 1: AUROC 0.954 (TabPFN-Wide 1.5k), 0.952 (RealMLP), 0.942 (random forest), with the submitted `histological_type`.
- Label: TCGA sarcoma study (Cell 2017, 171:950), "Samples and Clinicopathologic Data": "We studied 206 sarcomas with diagnoses confirmed by expert pathology review"; STAR Methods "Sample qualification" and "Pathology review": 24 of 261 qualified cases failed QC ("5 that failed genotype concordance"), 31 more were excluded ("3 probable melanomas", 17 "of uncertain classification"), and "20 were reclassified ... based on histologic appearance, presence or absence of focal chromosome 12q~15 amplification, and expression of muscle markers".
- Uniqueness: no other TCGA sarcoma data in the working copy or the records.

**Data:** https://acgt.cs.tau.ac.il/multi_omic_benchmark/data/sarcoma.zip (`exp` 20,531 x 265, `methy` 5,000 x 269, `mirna` 1,046 x 263), clinical.zip (`clinical/sarcoma`, kept for the comparison table) and the study's `SARC_Master_Patient_Table.xlsx` from its GDC publication page (https://api.gdc.cancer.gov/data/20cb9a7c-28a9-49ff-9e7d-8e7af0c722d9, md5 42146699371fd1582f8f04c05a03f8f5; its `short_histo` equals cBioPortal `sarc_tcga_pub` SHORT_HISTOLOGY for all 206 patients). Licence: as BRCA; the table is a GDC publication supplement.

**Definition:** prediction point: a primary soft-tissue sarcoma profiled on the three platforms; the model assigns its histological type. Target `histological_type` from the reviewed `short_histo` (multiclass, log loss): leiomyosarcoma 80 (STLMS 53 + ULMS 27), dedifferentiated liposarcoma 50, undifferentiated pleomorphic sarcoma 44, myxofibrosarcoma 17, synovial sarcoma 10. IID, 20 x 3 stratified folds (train 134, test 67). 201 rows x 25,971 features (562 all-zero and 44 duplicated columns dropped). Rows: the 206 reviewed patients (all among the 257 with three omics) minus 5 MPNST. Of the 246 rows of the first version, 46 are not reviewed and 19 changed type (README decision table).

**Checks:** 0 errors, 0 warnings, 0 info; no accepted warnings. Checksum v2:2545bb69... equal under pandas 2.3.3 (README.md) and 3.0.6. The download description (first part) was re-run in a fresh folder earlier: identical files; the GDC file's md5 matches.

**Probes:**
- leak: all features macro AUC 0.975; depth-2/3 tree 0.861/0.852; best single column 0.824 (`mRNA_RBPMS.11030`); drop-one 0.974-0.975; exact copies 0.0%; 1-NN agreement 0.701 (closest tenth 1.000, about 7 rows; chance 0.278).
- task: dummy log loss 1.405; LightGBM skill 0.538 (macro AUC 0.957, log loss 0.649, 30 of 30 splits, SE 0.026), random forest 0.537 (0.958), logistic regression 0.196 (0.920, overconfident); single column (`mRNA_MDM2.4193` on 17 of 30) skill 0.075 (0.758); smallest class per test fold 3. No flag.
- generated: `rule_leaves` (36.6% of the minority rows; both leaves dedifferentiated liposarcoma). Answer: the review assigned that type by 12q13-15 amplification, the MDM2 amplicon, and `mRNA_MDM2.4193` alone separates the 50 reviewed liposarcomas from the other 151 rows (ROC AUC 1.000; 0.936 for the submitted diagnosis). The class is the amplification-defined entity seen through its expression; TCGA measurements, not generated data. The review's muscle markers show the same way: a depth-2 tree puts 71 of 80 LMS in one leaf by `mRNA_PPP1R12B.4660`, and its last leaf mixes 43 UPS, 16 MFS, 10 SS and 9 LMS. Kept, written in `curation_comments`.
- hidden groups: 0 candidates. By hand, tissue source site (31 sites; `DX` 101 of 201 rows, 40 of 50 DDLPS, 13 of 17 MFS; Cramer's V 0.43): random forest macro AUC 0.954 random vs 0.947 by site, log loss 0.662 vs 0.763. IID kept.

**Issues for Lennart:**
1. Label from a second source (implemented: TCGA's reviewed histology, pinned GDC file). Alternative: the submitted `histological_type` on all 246 rows (random forest macro AUC 0.940, log loss 0.742 in the first version), which keeps non-sarcomas and genotype-discordant samples.
2. DDLPS is a one-feature class under the reviewed labels (MDM2 mRNA ROC AUC 1.000; generated probe `rule_leaves`). Implemented: kept as the entity's definition. Alternative: none that keeps the reviewed label; the submitted label is less crisp (0.936) because it holds misdiagnoses the review fixed.
3. MFS vs UPS: the study finds them "largely indistinguishable across multiple platforms" and analyses them "as a single spectrum of disease"; here a model separates them at about AUC 0.73 (verifier). Implemented: five classes. Alternative: one UPS/MFS class (61 rows), the study's own convention.
4. Synovial sarcoma 10 (3-4 per test fold) kept at the §D.8 floor; MPNST (5 reviewed) dropped. Leiomyosarcoma merges soft-tissue (53) and uterine (27) as the clinical file does; the study separates them by site.
5. Record fields: `problem_type` Multiclass; suspension reason unknown. Comment in `sarcoma.record_comment.md`.

**Verification:**
- Finding 3 (submitted vs reviewed diagnosis): applied, with the study's master patient table pinned by its GDC file id and md5 instead of the cBioPortal API (same 206 values). 201 rows as proposed; probes rerun (task skill 0.47 to 0.54; random forest log loss 0.742 to 0.650).
- Finding 4 (UPS/MFS): raised as issue 3, not implemented; spelling merges kept (now moot: the reviewed table has one name per type); synovial kept.
- Finding 5 (site): rerun on the 201 rows, small gap, IID kept.

### Across the three
- BRCA and GBM now predict an expression-defined subtype from methylation and miRNA; SARC predicts the reviewed pathology type from all three omics. If labels defined from the same tumours' expression are out of scope, BRCA and GBM go (as `Trivial`) and SARC stays; the MLOmics OV folder of the other unit has the same kind of label.
- Column prefixes `mRNA_`, `Methy_`, `miRNA_` match the MLOmics folders. `sync-notebooks` was not run (records not edited), so `v2_path` is unset.

### coad_colon_adenocarcinoma
**Outcome:** added and checked.
**Record judgment:** valid with concerns.
- The record's binary framing is wrong: the source labels have four classes (issue 1).
- No reason for `DF: Suspended` is recorded in the record, in git (the status came with the sheet import of 2026-06-23) or in the docs. The one gap found was the unnamed target, which is now resolved.
- The data pass every cross-omics check: the gene names hold, and the patients match across the four files.

**Data:** MLOmics (Yang et al. 2025, Scientific Data 12:913, doi 10.1038/s41597-025-05235-x).
- Files: HF `AIBIC/MLOmics`, revision `74b9385f` (2026-09-22), `GS-COAD/Original/COAD_{mRNA,miRNA,Methy,CNV,label_num}.csv` (267 MB). SHA-256 equals the LFS ids.
- Rows: 260 TCGA patients (one primary tumour each) x 56,204 genes; labels as codes without ids.
- Licence: CC BY 4.0 (HF card, Figshare, paper "Data Records").
- `source = "HuggingFace"`: the data live on HF and on Figshare (doi 10.6084/m9.figshare.28729127); the GitHub repository only clones HF.
- Figshare v2 (2025-05-25) is MD5-identical to HF revision `d7c22395`. The pinned files keep a subset of its genes for the same patients and labels, with the 2025 values (see `download_description`).

**Definition:** `datasets/_dev/tabarena-v0pt2/coad_colon_adenocarcinoma/dataset.py`.
- Prediction point: a resected tumour profiled on four platforms (RNA-seq for mRNA and miRNA, 450k methylation, SNP6 copy number); the model assigns its TCGA PanCancer Atlas subtype.
- Target: `subtype` (CIN 174, MSI 48, GS 34), multiclass, log loss.
- Regime: IID, 20 x 3 folds (train 170-171, test 85-86).
- Size: 256 x 49,283 features (mRNA 17,261, miRNA 375, Methy 18,719, CNV 12,928).
- Cleaning: transpose and prefix each omics file; name the codes by barcode match to TCGAbiolinks `PanCancerAtlas_subtypes()` (260 of 260 one to one); drop the 4 HM-SNV tumours; drop 6,921 exact duplicate columns (6,617 CNV, 304 methylation; none constant); drop the barcode.

**Checks:**
- `dataset check`: 0 errors, 0 warnings, nothing accepted (re-run 2026-10-07).
- The container built under pandas 3.0.6 has the same checksum as under 2.3.3 (`v2:abc63e11…`).
- `pytest -q tests/test_v2_datasets.py -k "coad or lgg or ov_ovarian"` passes, also with `DATA_FOUNDRY_V2_DATA_CHECKS=1`.

**Probes:**
- Task probes (30 splits): no flags.
  - Random forest: skill 0.51 over the class-share dummy (AUC 0.933, log loss 0.411 against 0.845), beating it on 30 of 30 splits.
  - LightGBM 0.30 (AUC 0.934); linear -0.03 +- 0.48 (AUC 0.924, overconfident).
  - Single feature 0.02 (AUC 0.79).
  - Smallest class: 11 rows per test fold.
- Leak probes (3 splits, functions of `leak_probes.py`):
  - LightGBM 0.939, unchanged without each of the three best single features;
  - depth-2 / depth-3 tree 0.856 / 0.800;
  - best single feature 0.882;
  - 0% exact copies;
  - 1-NN agreement 0.79 against 0.52 by chance.
- Generated-data probe: no rule leaves. Hidden groups: no candidate.
- Label rules, 30 splits: no rule on the shipped blocks.
  - Trees on the CNV block alone reach AUC 0.795 / 0.825 / 0.812; on all features 0.79 / 0.83 / 0.84.
  - The three-score model (copy-number burden, MLH1 methylation, MLH1 expression) reaches 0.926 / 0.388, against the forest's 0.933 / 0.411. Its log loss is lower on 20 of 30 splits, its AUC higher on 11.
- Tissue source site (25 sites): no gap; IID kept.

**Issues for Lennart:**
1. **Problem type.** All three records say Binary Classification. TabPFN-Wide reads `{C}_label_num.csv` unchanged (`load_mm_data.py`) and scores macro AUROC.
   - For the orchestrator: set `problem_type` to Multiclass Classification on `coad_colon_adenocarcinoma`, `lgg_low_grade_glioma` and `ov_ovarian_cancer`.
2. **HM-SNV dropped** (4 tumours, 1-2 per test fold).
   - Alternative: merge them with MSI into one hypermutated class, as TCGA 2012 did (abstract quoted in the comments).
3. **Labels from data that do not ship.**
   - MSI is defined from exome indel density: tumour mutation burden separates it at AUC 1.000; MSIsensor 0.993, MANTIS 0.999.
   - CIN against GS is a clonal deletion score > 0.0249 (Liu et al. 2018, quote corrected in the comments). A label-free copy-number burden from the CNV block separates CIN from GS at AUC 0.891 (cBioPortal fraction of genome altered 0.878, aneuploidy score 0.914).
   - No rule reproduces the label (probes above), so it stays a subtype-calling task.
   - Kept: the CNV block. Dropping it as the measurement behind CIN/GS: L2 logistic regression 0.931 / 0.398 against 0.934 / 0.412 with it. Lennart's call; I recommend keeping it.
4. **Width: 49,283 features.**
   - 2.2x the widest dataset of the copy before this run (`lung_cancer_epithelial_genexp`, 22,215).
   - 717 under Mitra-v2's 50,000-feature cap (`tabarena/.../models/mitra_v2/model.py`). Task probes take 50 min at 2 threads.
   - Alternative: mRNA only (17,261 features): L2 logistic regression 0.926 / 0.402 against 0.934 / 0.412 with all blocks. The source task (MLOmics, TabPFN-Wide) uses all four blocks.
   - Lennart's call.
5. **Scaling.** MLOmics standardised every feature over all 260 patients (repository issues #3, #7, #9). The scaling uses no labels but includes the test rows. Kept.
6. **Trust in the source.** GS-LGG and GS-OV of the same release carry fabricated gene names, and GS-LGG's methylation does not match its patients. GS-COAD passes every check.
7. **`DF: Suspended` has no recorded reason.**
8. **Framework.** `leak_probes.py` fits one LightGBM per feature (about 5 h on 50k features), so I ran it through a scratch wrapper. Probe discovery breaks on other agents' half-written folders, so the probes ran on a scratch root of symlinks.

### lgg_low_grade_glioma
**Outcome:** added and checked, repaired: the methylation block is left out, every feature is named by its omics and file row, and the dataset is tagged `Anonymized`.
- Recommended not to ship: record `No` + `Data Quality Issue`. Whether `Trivial` is a second marker is Lennart's call.
- The folder stays for Lennart's decision; the evidence is in `curation_comments`.

**Record judgment:** do not ship this release. It is faulty in all four blocks, in all three MLOmics revisions (2025-04 `122c748f`, 2025-05 `d7c22395`, 2026-09 `74b9385f`).
- Methylation does not match the patients: patient-similarity r with mRNA -0.005, against 0.59 for miRNA and 0.45 for CNV. No methylation gene separates a class beyond chance, although IDH-mutant gliomas carry G-CIMP.
- The gene names of all blocks do not describe the values:
  - 1,147 mRNA and 1,425 CNV rows are named `ZZZ<n>`/`ZZEF<n>`;
  - GS-LGG shares one name column with GS-OV in the 2025 release;
  - 13 mRNA columns separate sex at AUC 0.997-1.000 under autosomal names, while RPS4Y1, DDX3Y, KDM5D and XIST are absent;
  - genes named on 1p/19q do not track codeletion;
  - no co-variation along arms; no copy-number dosage;
  - miRNA clusters r +0.04 (COAD +0.55).
- The values themselves are real: hypoxia score r 0.62 (shuffled 0.26).
- One mislabel (TCGA-DU-6399).
- The label is close to a two-column rule (issue 3).
- Record: the binary framing is wrong; no reason for `DF: Suspended` is recorded.

**Data:** MLOmics, revision `74b9385f`.
- Files: `GS-LGG/Original/LGG_{mRNA,miRNA,CNV,label_num}.csv` (83 MB), 247 patients.
- `LGG_Methy.csv` was tested and moved to `../_scratch_new65/tcga_mlomics/removed_from_warehouse/`.
- Licence: CC BY 4.0. `source = "HuggingFace"`.

**Definition:** `datasets/_dev/tabarena-v0pt2/lgg_low_grade_glioma/dataset.py`.
- Target: `subtype` (IDHmut-non-codel 125, IDHmut-codel 76, IDHwt 46), multiclass, log loss.
- Regime: IID, 20 x 3 folds.
- Size: 247 x 21,076 features (mRNA 14,260, miRNA 321, CNV 6,495).

**Checks:** 0 errors, 0 warnings. The pandas-3 checksum equals pandas 2.3 (`v2:08244111…`). pytest passes in both modes.

**Probes:**
- Task probes: no flags. Random forest skill 0.84 (AUC 0.991 / log loss 0.167); smallest class 15 rows per test fold.
- Leak probes: LightGBM 0.989; depth-2 / depth-3 tree 0.972 / 0.966; 0% copies.
- Generated-data probe and hidden-group probe: nothing.

**Issues for Lennart:**
1. **Retire the release.**
   - Proposed: `No` + `Data Quality Issue`, then remove the folder from the copy. `Trivial` is your call: the rule-4 test does not prove it.
   - Alternatives considered: keeping MLOmics' four blocks (methylation that does not match the patients, fabricated names); the repaired three-block folder as it stands.
   - Dropped: "rebuild from TCGA files". With a correct methylation block, IDH status is a lookup too (PanCancer Atlas methylation clusters LGm1-3 against LGm4-6 match IDH-mutant against IDHwt for 245 of 247 patients), so a rebuild would be a two-block lookup.
2. **Names replaced by file rows** (tag `Anonymized`). Needed if the folder stays. The TabPFN-Wide attention analysis for LGG (Appendix A, Table 2) rests on the fabricated names.
3. **Near-deterministic label** (30 splits):
   - One CNV column chosen on each training side separates codeletion at test AUC 0.995 (median 0.997, minimum 0.980; `CNV_00553` on 20 splits, `CNV_00068` on 9).
   - One mRNA column separates IDHwt at 0.972.
   - A logistic regression on the two reaches 0.984 / 0.194 (skill 0.81), against random forest 0.991 / 0.171 and L2 logistic regression 0.988 / 0.149 (skill 0.85). Its log loss is lower than the forest's on 8 of 30 splits and the logistic regression's on 7: 95% of the best skill from two columns.
   - Without the CNV block: 0.985 / 0.159. No block removal helps.
   - TabPFN-Wide reports AUC 0.973-0.991 for all of its methods.
4. **Problem type:** Multiclass (see COAD issue 1).
5. **Mislabel:** TCGA-DU-6399 (IDHwt in MLOmics; IDH-mutant in cBioPortal and TCGAbiolinks). Kept.
6. **`DF: Suspended`:** no recorded reason.
7. **Overlap:** 240 of 247 patients are in `glioma_grading_clinical_and_mutation_features` (LGG vs GBM from mutation flags; constant label LGG for them). Another task, not a duplicate.

### ov_ovarian_cancer
**Outcome:** added and checked (every feature named by its omics and file row, tagged `Anonymized`).

**Record judgment:** valid with concerns.
- The values are real and match the patients:
  - patient-similarity r with mRNA: miRNA 0.43, methylation 0.34, CNV 0.47;
  - hypoxia score: best mRNA column r 0.66 (0.21 with the patients shuffled).
- The names of all four blocks are fabricated, in all three revisions:
  - 1,147 mRNA, 4,516 methylation and 1,459 CNV rows named `ZZZ<n>`/`ZZEF<n>`;
  - one name column shared with GS-LGG in 2025;
  - no co-variation along arms; no copy-number dosage;
  - miRNA clusters r +0.05 (COAD +0.55);
  - the named hypoxia genes have mean r +0.03 (COAD +0.48);
  - the TCGA 2011 Immunoreactive markers give AUC 0.37-0.46.
- The labels are TCGA 2011 microarray NMF clusters (255 of 284 agree).
- Record: the binary framing is wrong; no reason for `DF: Suspended` is recorded.

**Data:** MLOmics, revision `74b9385f`.
- Files: `GS-OV/Original/OV_{mRNA,miRNA,Methy,CNV,label_num}.csv` (156 MB), 284 patients.
- Licence: CC BY 4.0. `source = "HuggingFace"`.
- The pinned methylation file fills the 1,931 genes with missing values in 2025 (0.2% of the cells).

**Definition:** `datasets/_dev/tabarena-v0pt2/ov_ovarian_cancer/dataset.py`.
- Target: `subtype` (Immunoreactive 79, Proliferative 74, Mesenchymal 67, Differentiated 64), multiclass, log loss.
- Regime: IID, 20 x 3 folds.
- Size: 284 x 48,279 features.

**Checks:** 0 errors, 0 warnings. The pandas-3 checksum equals pandas 2.3 (`v2:11e9410f…`). pytest passes in both modes.

**Probes:**
- Task probes: no flags. LightGBM skill 0.70 (AUC 0.980 / log loss 0.413); smallest class 21 rows per test fold.
- Leak probes: LightGBM 0.985; depth-2 / depth-3 tree 0.818 / 0.839; 0% copies.
- Label rules, 30 splits: no rule.
  - mRNA trees reach AUC 0.694 / 0.824 / 0.868.
  - A training-side centroid model reaches 0.954 / 0.511, against L2 logistic regression 0.963 / 0.455 and LightGBM 0.980 / 0.413.

**Issues for Lennart:**
1. **Accept the anonymised repair?** The names are fabricated; the values and labels check out. Alternative: retire with `Data Quality Issue` like LGG. Lennart's call; the verifier would accept the repair for OV.
2. **Expression-cluster labels.** One decision together with BRCA (PAM50) and GBM of the `tcga_acgt` unit.
   - No rule reproduces the label (above).
   - The 29 labels that differ from TCGA 2011 are not traceable to the RNA-seq: a logistic regression on mRNA trained on the 255 concordant patients picks MLOmics 17 times and TCGA 2011 9 times; the verifier's forest 11 / 16.
   - Kept: the mRNA block. Without it: L2 logistic regression 0.891 / 0.850.
3. **Width: 48,279 features** (2.2x the earlier widest).
   - Alternative: mRNA only (14,229 features), L2 logistic regression 0.982 / 0.312 against 0.963 / 0.455 with all blocks. The source task uses all four.
   - Lennart's call.
4. **Problem type:** Multiclass (see COAD issue 1).
5. **`DF: Suspended`:** no recorded reason.

### Verification (fix round, 2026-10-07)
The verifier's verdicts: COAD ready with noted concerns, LGG should not ship, OV ready with noted concerns. I re-checked every key number with my own code (scratch `fix/`), and none of the findings needed rejecting.

| Finding | My check (file) | Result | Action |
|---|---|---|---|
| LGG: codeletion is one CNV column | `fix/rules_check.py lgg` | test AUC 0.995 (median 0.997, min 0.980), as reported | comments + issue 3 |
| LGG: two-column model 0.194 vs 0.171 / 0.149 | same | 0.984 / 0.194; lower than the forest on 8 of 30, the logistic regression on 7 | same |
| LGG: without CNV nothing changes | `fix/lgg_ov_extra.py` | 0.985 / 0.159 | same |
| LGG: LGm1-3 vs LGm4-6 = IDH status | `fix/rules_check.py lgg` | 245 of 247 | "rebuild from TCGA" dropped |
| Names: placeholders | `fix/names_check.py` | LGG 1,147 / 1,425 / 4,541, OV 1,147 / 1,459 / 4,516, COAD 0. The verifier's counts are 2 higher per block because they include the real genes ZZZ3 and ZZEF1 | comments |
| Names: 2025 LGG and OV share one name column | same | identical row for row in all four blocks; COAD differs | comments |
| Names: 13 LGG mRNA columns separate sex | same | 13 columns (12 at AUC 1.000, one at 0.997), autosomal names; COAD none | comments |
| Names: miRNA clusters | same, with my own cluster list | COAD +0.55, LGG +0.04, OV +0.05 (verifier +0.57 / +0.04 / +0.04) | both folders already anonymise miRNA; evidence added |
| Values real (hypoxia score) | same | max \|r\| COAD 0.70, LGG 0.62, OV 0.66; shuffled 0.21-0.28 | comments |
| COAD: CDS threshold | Liu 2018 PMC text | "(CDS, See STAR Methods) > 0.0249"; my old quote cut at the decimal point | fixed |
| COAD: burden CIN vs GS | `fix/rules_check.py coad` | 0.891 with my burden; the verifier's variant 0.879 | comments |
| COAD: three-score model | same | 0.926 / 0.388; lower log loss than the forest on 20 of 30, higher AUC on 11 (verifier 0.920 / 0.387, 20 and 9) | comments |
| COAD: trees on CNV alone | inline | 0.795 / 0.825 / 0.812 | comments |
| COAD: MSI from exome | cBioPortal sample attributes | tumour mutation burden AUC 1.000, MSIsensor 0.993, MANTIS 0.999 | comments |
| COAD: without CNV, mRNA only | `fix/rules_check.py coad` | 0.931 / 0.398; 0.926 / 0.402 | issues 3, 4 |
| OV: trees on mRNA | inline | 0.694 / 0.824 / 0.868 | comments |
| OV: centroid model | inline (`fix/centroid_loo.log`) | 0.954 / 0.511. Genes must be standardised on the training side with leave-one-out centroids; without that, my first version got 0.705-0.734 | comments |
| OV: without mRNA, mRNA only | `fix/rules_check.py ov` | 0.891 / 0.850; 0.982 / 0.312 | issues 2, 3 |
| OV: 29 discordant labels | `fix/lgg_ov_extra.py` | logistic regression 17 MLOmics / 9 TCGA / 3 neither | comments |
| Provenance: Figshare v2 = HF `d7c22395` | `fix/revisions_check.py` (Figshare API MD5) | all 15 Original files MD5-identical | `download_description` |
| Provenance: 2026 files a subset with identical values | same | true for COAD. LGG/OV differ only where the 2026 methylation fills 2025 NaNs (LGG 1,093, OV 1,931 genes) and for the duplicated 2025 rows "1-Mar"/"2-Mar" (Excel-mangled MARCH1/MARCH2; 2026 keeps one copy) | `download_description` states both |
| `source` | `src/data_foundry/schema.py` `DatasetSource` | `"HuggingFace"` exists | set, with the HF URL |

The re-runs after the edits are listed under each dataset's **Checks**.

### Shared notes for the three records (tcga_mlomics unit)
- **Evidence scripts** (scratch of this unit):
  - first round: `crosstab_*.py`, `sanity_*.py`, `positional.py`, `markers.py`, `univariate_auc.py`, `pandas_compat*.py`, `leak_probes_wide.py`, `fold_by_fold.py`, logs in `probes/`;
  - fix round: `fix/`.
- **Data copies:** in `../_scratch_new65/tcga_mlomics/`.
- **Other datasets:** the three cohorts are disjoint from the ACGT records of this run, and none of them is in the working copy.

### zillow_prize

**Outcome:** added and checked

**Record judgment:** valid with concerns. The data first appeared in round 1 of the Kaggle competition Zillow Prize
(zillow-prize-1, 2017): Zillow's cleaned copy of the public assessor records of Los Angeles, Orange and Ventura
counties plus the log error of the Zestimate for the sales of 2016 and January to mid-September 2017. Unique: no
folder of the working copy and no other record holds it (`california_house_prices_2020` is a different competition with
2020-21 listings; `house_sales`, `house_prices_nominal`, `melbourne_housing_market` and `perth_house_prices` of this run
are King County, Ames, Melbourne and Perth). Published for a predictive task (regression of `logerror`, scored with
MAE, Evaluation page). Predicting the error of Zillow's own model is a real use case, stated by the source: "modeling
errors can be a very powerful way to find areas to improve your existing model ... will help 'boost' the current
Zestimate directly" (Zillow Prize FAQ, discussion 33899). Not forecasting: one prediction per home sale, with a
temporal split. Concerns: the signal is small and the squared error is dominated by a few extreme values (issues 1, 2).

**Data:** Kaggle competition files, downloaded with `kaggle competitions download -c zillow-prize-1 -f <file>` into
`local-data-warehouse/zillow_prize/`: train_2016_v2.csv.zip (90,275 sales x 3 columns, 2016-01-01 to 2016-12-30),
train_2017.csv.zip (77,613 x 3, 2017-01-01 to 2017-09-25), properties_2016.csv.zip and properties_2017.csv.zip
(2,985,217 parcels x 58 columns each, the same parcels), zillow_data_dictionary.xlsx (md5s in `download_description`;
the Kaggle file dates are 2019-12-11). `_prepare_raw_files` writes the property rows of the 165,210 sold parcels to
two parquet files next to the zips. Licence: the competition rules allow the data only "for the purpose and duration
of the Competition" and forbid redistributing it (Rules page, section "Data").

**Definition:** `datasets/_dev/tabarena-v0pt2/zillow_prize/`.
- Prediction point: the first day of the sale month. Zillow pairs each sale with the Zestimate "from the first day of
  the month in which they were sold" (FAQ), and round 1 asks for one prediction per home and month. So
  `transactiondate` becomes `transaction_month` (first day); the day carries no signal (Spearman 0.01).
- Target `logerror` (regression, default RMSE; the competition's MAE is noted), rounded to the 4 decimals of 2016
  (Evaluation page: accurate to the 4th decimal).
- Temporal: `TemporalSplits(window=1, unit="months", n_windows=9, gap=1)`: July 2017 back to November 2016, train
  ends one month before each window (recording delay). Train 81,731 to 132,176 rows (oldest window 53%), test 1,739
  to 11,448.
- 153,108 rows x 56 features.
- Cleaning: each sale joined to the property file of its year (properties_2017 holds edits made after early-2016
  sales; Zillow's warning about its tax values, discussion 40408); August and September 2017 dropped (14,737 rows; "a
  biased sample", same post); 24 sales without home facts dropped (as Zillow did for train_2016 v2, discussion 34667);
  19 repeat sales within 31 days dropped (the competition's ground-truth rule, Data page); `buildingqualitytypeid` of
  2017 mapped onto the 2016 scale (the file rescaled it; each 2017 code comes from one 2016 code); nine one-value
  columns turned into booleans; two-digit `taxdelinquencyyear` to four digits; zeros as "not recorded" set to missing
  in `roomcnt` (99,475 of 99,476 Los Angeles rows), `bathroomcnt` (1,649 rows, all without the derived bath counts)
  and `bedroomcnt` where `bathroomcnt` is 0 too (1,609 rows, median 2,188 sq ft); `parcelid`, `regionidcounty`
  (recoding of `fips`), `assessmentyear` and `transactiondate` dropped; 12 code columns as categories. The delinquency
  fields stay, with a `Note:` bullet on their snapshot date.
- Three `_decisions` tables: the 2017 months (rows, mean, share of |logerror| > 1), the quality-code cross-tab, the
  share of squared error by |logerror| band.
- Same checksum under pandas 2.3.3 and 3.0.6 (v2:26f7f92a..., `_prepare_raw_files` re-run under pandas 3).

**Checks:** `dataset check`: 0 errors, 0 warnings, 1 accepted, 2 info.
- Accepted `meta_time_horizon_mismatch`: `transaction_month` holds the first day of the month, so a one-month window
  holds one date and its span reads as 1 day; the windows are calendar months.
- Info `dataset_duplicate_rows` (7) and `dataset_conflicting_duplicate_rows` (39): units of one condominium building or
  tract share coordinates and recorded facts; separate parcels and sales, all copies in one month, kept.
- `pytest -q tests/test_v2_datasets.py -k zillow_prize`: 1 passed, 1 skipped (the opt-in data check). The class
  imports with `load_definition`; ruff clean.

**Probes** (after the verifier's fixes; outputs in `<scratch>/probes2/`, experiments in `<scratch>/work/`):
- `leak_probes.py` (3 newest windows): untuned LightGBM R^2 -0.038; depth-2/3 trees -0.001/-0.005; no feature and no
  missing-value indicator alone above 0.001; 0.2% of test rows have an exact feature copy in train; 1-NN R^2 negative.
  No leak.
- `task_probes.py` (5 of 9 windows; run with `--root` on a folder holding only this dataset, because another agent's
  half-written definition crashed the discovery): dummy RMSE 0.159; linear skill -0.011, random forest -0.013,
  LightGBM -0.013, single feature -0.007. Flags `no_signal`, `drift_baseline`, `unstable` (best family above the dummy
  in 2 of 5), as before. Answered in a curation bullet as a small real signal: LightGBM with an absolute-error loss
  beats the train mean on all 9 windows (R^2 0.003 to 0.021, mean 0.007), with a Huber loss too (mean 0.010), and
  the train median's MAE on 8 of 9. `drift_baseline` and `unstable` follow from the same weak signal. No tuned
  results exist yet (rule 1).
- `generated_probes.py`: exact fits 2.2% against 2.4% on a shuffled target, no flag.
- `hidden_groups.py` and `group_probes.py`: not run (temporal task). Repeat sales of a parcel (2,182 parcels) and
  units of one building recur over time; under the temporal split an earlier sale is history.
- Snapshot checks: swapping in the 2016 tax values for the 2016 sales gains nothing (random 3-fold CV, LightGBM R^2
  0.016 vs 0.015); the 2016 roll is the 2015 roll times the 1.525% factor for 77% of parcels sold in 2016 (off the
  factor: 22.8% sold 2016, 21.1% sold only 2017, 15.1% never sold). Building facts in properties_2017 differ for
  1.2-2.0% of the parcels sold January to May 2016 (mostly filled in or replaced, such as a later year built) against
  0.81% never sold; for 2017 sales 0.7-1.0% per month.

**Issues for Lennart:**
1. **Metric: RMSE (implemented) or the competition's MAE.** 0.4% of the rows have |logerror| > 1 and hold 50% of the
   squared error around the mean (2.1% above 0.4 hold 74%); Zillow traces them mostly to miskeyed prices (FAQ on the
   round-2 metric; discussion 36752). Per window against the train constant (verifier's paired runs, LightGBM):
   L1 loss beats the mean in RMSE on 9 of 9 windows (skill 0.0069-0.0071 over two seeds, median t 2.3-2.4) and the
   median in MAE on 8 of 9 (0.0074); Huber loss 9 of 9 in RMSE (0.0096); L2 loss 4 of 9 (-0.0049), and only through
   the rows with |logerror| > 1. My re-run on the final frame agrees (L1 0.0073, Huber 0.0101, both 9 of 9). So RMSE keeps a real signal for robust fits and mainly tests robustness to the
   extreme rows. Implemented: default RMSE (add-dataset §A), MAE noted. Alternative: `metric = "mae"`, the source's
   scoring (task_probes.md rule 6; `allstate_claims_severity` does this), although the TabArena adapter still falls
   back to RMSE (`BENCHMARK_CHANGES_TODO.md`, "Dataset-specific metrics"). Top-coding the target at +-0.4 (Zillow's
   round-2 score) is not needed for the signal and changes the target.
2. **Is the signal enough?** The task probes flag `no_signal`, `drift_baseline` and `unstable`; untuned models do not
   beat the mean. I kept the task under rule 2 (small but real: robust LightGBM fits beat the mean on 9 of 9
   windows). The competition gap is smaller than it looks: public submissions reached MAE 0.064 against 0.066 for
   predicting zero, but a constant alone closes 0.0008-0.0011 of that 0.002 (on the 4,605 sales after 15 October 2016
   in train_2016_v2: 0.0704 for zero, 0.0696 for the train median, 0.0693 for the mean). Once TabArena results exist,
   `tuned_results.py` should confirm that tuned methods beat the dummy fold by fold; if they do not, this is a
   `TBD -> 2nd Tier` case.
3. **Month instead of the sale date.** Implemented: `transaction_month` (first day), the prediction point of the
   source; the `meta_time_horizon_mismatch` warning is accepted for it. Alternative: keep `transactiondate` (no
   accepted warning; the day is not known on the first of the month and carries no signal, Spearman 0.01).
4. **Windows.** Implemented: 9 monthly windows (the count an IID task of this size gets) with a one-month gap for the
   recording delay. Alternative: the competition's three-month horizon, 3 windows of 3 months (test rows 31,413 /
   24,407 / 10,580), or no gap.
5. **August and September 2017 dropped** (14,737 rows; twice the share of |logerror| > 1: 0.72% and 0.77% against
   0.32-0.43% in January to July 2017). Alternative: keep them as two more windows, accepting the biased sample.
6. **`buildingqualitytypeid` harmonised** onto the coarser 2016 scale (5 levels; the 2017 file has 12). Alternatives:
   keep the raw codes or drop the column; LightGBM R^2 within 0.001 for all three, so the choice is about meaning only.
7. **Licence:** the rules forbid redistributing the data outside the competition (Rules, "Data"). Noted, not a
   verdict reason; it matters if the container is to be published.
8. **BibTeX author:** Kaggle's own citation (its author list) could not be read through the CLI; the entry cites
   `{Zillow}`. Replace with the authors of Kaggle's "Cite" box if wanted.
9. **Record housekeeping** (not edited by me): the record has no `original_source`, `year`, `domain`, `problem_type`
   or `required_split`; values used: Kaggle, 2017, business & marketing, Regression, Temporal. `v2_path` needs
   `sync-notebooks` (the verifier's `sync-notebooks --check` shows it unset, as expected before a build).
10. **Framework:** `_prepare_code_hash` (`src/data_foundry/v2/dataset.py`) hashes `_prepare_raw_files` and the
    functions it calls, not module constants, so editing a constant the step reads would not re-run it. This
    definition works around it (the text columns inside the method, the sales file names from a function); other
    definitions with prepared files may read constants too.

**Verification:**
1. Delinquency snapshot: applied as a `Note:` bullet, columns kept. Confirmed: flag rate 1.54% for January to August
   2016 sales (1.2-1.6% per month March to August), 3.1-4.7% per month from September 2016, 1.84% never sold;
   dropping both columns moves the L1 LightGBM skill from 0.0069 to 0.0068.
2. Pairing wording: applied. The bullet now says the 2016 tax values hold few sale prices (77% on the inflation
   factor; off-factor 22.8% / 21.1% / 15.1%) and that the building facts of properties_2017 were edited after the
   January-May 2016 sales (1.2-2.0% vs 0.81%; confirmed: 1.46% for January-May, mostly fill-ins and later years built),
   with none for the 2017 sales; the record comment cites this.
3. Squared-error shares: applied (74% / 50% in `curation_comments`, issues.md and the record comment).
4. Zero bedrooms: applied (`bedroomcnt` set to missing where `bathroomcnt` is also 0, 1,609 rows; the other 480 keep
   their 0; "exactly" removed from the bathroom bullet).
5. Metric: issue for Lennart (issue 1, with the verifier's numbers; RMSE stays implemented).
6. Competition baseline: applied (issue 2 and the curation bullet now say a constant closes 0.0008-0.0011 of the
   0.002 gap).
7. Prepared-file hash: applied in the definition (`sales_files()` function, text columns inside `_prepare_raw_files`;
   the hash now covers both; the parquets were rewritten byte-identical) and reported as issue 10.

## The three datasets from `_too_late_to_add`

Defined, checked, reviewed by three independent reviewers (prediction point and leaks; task, split and metric; provenance and record) and fixed, then checked once more by a final critic. The decisions live in each `dataset.py` (`curation_comments`, `_decisions`); below are the open questions for Lennart and the critic's remaining points.

### phiusil_phishing

**Recommendation:** exclude.

The task is solved by how the two classes were collected, and the effect runs through the URL and the page features, so dropping columns cannot fix it.
- URL side: all 134,850 legitimate rows are ranked domains (FILENAME is the Open PageRank rank) written as https://www.<host> with no path, one row per host. Only 627 of 100,520 phishing URLs have that form. URL features alone: LightGBM AUC 0.9989.
- Page side: every legitimate page has at least 102 lines, while 76.8% of phishing pages have fewer and 46.5% have at most 10.
  - The phishing pages were fetched after the URLs were listed. 50,748 phishing rows (50.5%) and no legitimate row carry one of 115 pages shared by at least 100 rows on several hosts, and none of these rows has a password field.
  - The largest shared page (6,159 rows on 6,137 hosts) is the page Firebase Hosting serves for an address without a site. 87.5-88.2% of the phishing test rows have an identical page in train.
  - Page features alone reach 0.99994.
- Together: a fixed two-condition rule with no training reaches AUC 0.9998. The rows that pass it hold 38 phishing rows, so no clean subset exists.
- Models: after dropping FILENAME, URLSimilarityIndex, Title and the two title-match scores computed from Title, untuned LightGBM, random forest and a linear model reach AUC 0.999999 / 0.999998 / 0.99999 with log loss 0.0008 / 0.0041 / 0.0024. The spread is 0.00002, so any method ranking on this dataset would be noise. Probe flags: solved, no_spread. No tuned results exist.
- The data is not simulated: the generated-data probe finds 1 leaf covering 1.2%.
- Marker: Data Quality Issue (§D.13, as for prostate_cancer_detection). Trivial applies only as 'solved perfectly'.
- This answers the record's open points. Andrej's leak question: yes, through URLSimilarityIndex, Title and the two scores computed from it, and through the class construction itself. Grouping: hosts repeat for phishing only, and grouping by host or registered domain changes nothing.

**Task:** binary_classification, target label; 235,370 rows x 49 features; metric roc_auc (default).

**Split:** IID, the default stratified 3-fold CV (3 repeats). Hosts are not held out because a deployed detector sees URLs on hosts it already knows (shared hosting, known phishing hosts) as well as on new ones. Holding hosts out barely changes the score. On a 3-fold split with seed 0, LightGBM on the numeric features and TLD gets ROC AUC 1.0000 with log loss 0.00032 on a random split, 0.00029 grouped by host and 0.00044 grouped by registered domain. The URL text alone (character 3- to 5-grams, logistic regression) gets 0.99915 / 0.0133 random, 0.99902 / 0.0142 grouped by host and 0.99894 / 0.0155 grouped by registered domain. In the random split, 17.5% of the phishing test rows have their host in train and 59.7% their registered domain. Data tag ForcedIIDFromTemporal: there is no time column, and only the phishing rows carry an order (feed ids), so no temporal split can be built.

**Source and licence:** source = "Other", source_url = https://doi.org/10.17632/shwpxscxy2.1, year = "2023", unchanged from the author's version. Mendeley Data published version 1 on 2023-08-29 and version 2 on 2023-11-15, both with the same file (sha256 a236549c...d1c6), which is byte-identical to the UCI file. UCI dataset 967 re-hosts it, donated 2024-03-03. The download stays the UCI wget. Licence: CC BY 4.0, from the "License" section of the UCI page and the Mendeley data_licence field. A Kaggle copy by user ndarvind is the same 235,795 rows and values without FILENAME (cell-by-cell compare, sha256 748ae7c7...) and lists CC-BY-NC-SA-4.0. This is noted in the comments and is not a verdict reason; the earlier claim that the copy is the authors' own is dropped as unverified. BibTeX: prasad2024phiusiil (Computers & Security 136, 103545, doi 10.1016/j.cose.2023.103545). The paper is paywalled and was not read. Two web searches found no open copy. A student thesis (norma.ncirl.ie/8277) only paraphrases URLCharProb as a comparison with "the character distributions of legitimate sites". The secondary source for the feeds is https://github.com/meeera0/PhiUSIIL_Algorithm_Comparison, which paraphrases the paper: legitimate URLs from Open PageRank, phishing URLs from PhishTank, OpenPhish and MalwareWorld. DomCop publishes the Open PageRank top-10M list.

**Open questions:**

1. **Should phiusil_phishing go into TabArena v0.2 at all?**
  - Implemented: Exclusion is recommended in curation_comments and in the accepted-warning reason. The definition is the cleanest one available: FILENAME, URLSimilarityIndex, Title, DomainTitleMatchScore, URLTitleMatchScore and Domain are dropped, URL is kept as text, the split is IID, and every remaining artifact is documented with numbers.
  - Alternative: Ship it anyway. Reviewer 1 points out that this is not a fixed version of the task: for half of the phishing rows the page side records what the URL served after it was listed, and without the page features the URL template alone still separates the classes. No version of this file is a valid task.
  - Numbers: Fixed rule with no training: AUC 0.9998, 38 of 100,520 phishing rows misclassified. Untuned LightGBM / random forest / linear: AUC 0.9999992 / 0.9999981 / 0.9999875, log loss 0.0008 / 0.0041 / 0.0024, spread 0.000023. URL features alone 0.9989, page features alone 0.99994. 50,748 phishing rows (50.5%) sit on 115 shared pages, none with a password field. Published audits say the same (ollivianguy/phishing-url-detection: AUC 1.000 all features, 0.999 URL-only; awesomedudeworld13/phish-drift: an https://www. regex gets TSS 0.99).
2. **If the dataset is excluded, where does its folder live? (Reviewer 3, finding 7)**
  - Implemented: The folder stays in datasets/_dev/tabarena-v0pt2/phiusil_phishing/. Lennart asked to add the dataset, and this run may write only inside that folder. It has no build, UUID or README table row.
  - Alternative: Move dataset.py and README.md next to the v1 notebook under datasets/_maintenance/_out_of_scope/_too_late_to_add/phiusil_phishing/, give the working copy no README row, and add one line with the published results to the record.
  - Numbers: tuned_results.py: not in the cached results, so no tuned evidence can overturn the flags. Published results: AUC 1.000 with all features and 0.999 URL-only (ollivianguy); regex TSS 0.99 and 0.000 on live URLs (phish-drift README); Kaggle notebook without URLSimilarityIndex, AUC 0.9995 (somanshumahajan).
3. **Which marker goes on the record? (Reviewer 3, finding 6)**
  - Implemented: Data Quality Issue is the decisive marker: the classes were recorded differently through every feature family, as in §D.13 and prostate_cancer_detection. Trivial is used only in the sense of 'solved perfectly' (criterion 4C).
  - Alternative: Also justify Trivial with the fixed rule or rule 4, or use Trivial alone.
  - Numbers: Rule 4 needs the raw feature to match the methods fold by fold. The URL text gets 0.9973 and the fixed rule 0.9998, while all three families reach >= 0.99999 with log loss 0.0008-0.0041 against a prior of 0.682.
4. **Keep URLCharProb, whose character distribution may come from this file's legitimate rows? (Reviewer 3, finding 4; TLDLegitimateProb is settled as an outside prior)**
  - Implemented: Kept, with the comment reworded: it is the mean probability of the URL's characters under a distribution of legitimate domain names, either this file's legitimate rows or the outside list, which is open until someone reads the paper.
  - Alternative: Drop URLCharProb as a possible class-conditional statistic over all rows (criterion 4D), or ask Lennart for the paper PDF first.
  - Numbers: Frequencies from legitimate rows: MAD 0.0036, and 0.0015 for alphanumerics only. From all rows: MAD 0.0115, correlation 0.96. No variant matches more than 4.6% of rows within 1e-4. AUC 0.77 alone. Without URLCharProb and TLDLegitimateProb, LightGBM gets AUC 1.000000, log loss 0.00042 (the same as with them).
5. **Near-identical URLs: keep them or drop them? (Reviewer 2, finding 3)**
  - Implemented: All rows are kept (the rule is to keep the source's rows) and documented in the Duplicates and Note bullets and in decision table 6.
  - Alternative: (a) Drop the second copy of the 461 pairs that differ only by '/' after the host, the same URL under RFC 3986 §6.2.3, for consistency with the exact-repeat drop. (b) Drop both rows of the 43 homepages listed under both labels (86 rows, 0.04%).
  - Numbers: 3,276 groups (6,856 rows: 6,813 phishing, 43 legitimate) are one URL up to scheme, www. or a trailing slash. Per final split, 1,551-1,624 phishing test rows (4.6-4.8%) have such a twin in train (493-558 for a trailing slash alone), and 13-20 of the 43 conflicting pairs straddle train and test. None of this moves the scores, which are at AUC 1.0000.
6. **Keep the raw URL as a string feature (v1 dropped URL and Domain)?**
  - Implemented: URL is kept: it is what a detector classifies. Domain is dropped as the URL's authority part. dataset_identifier_column is accepted.
  - Alternative: Drop URL as v1 did and keep only the source's numeric URL features and TLD.
  - Numbers: URL text alone: AUC 0.9973 / log loss 0.026 (task probe) and 0.99915 / 0.0133 (character n-gram LR). Without the URL text, LightGBM gets AUC 1.0000 / 0.0004, so the verdict does not depend on this choice.
7. **source and year: the definition uses Other / 2023 / the Mendeley DOI, while the record says UCI / 2024**
  - Implemented: source='Other', year='2023', source_url=https://doi.org/10.17632/shwpxscxy2.1 (§A, where the data first appeared). The download stays the UCI zip.
  - Alternative: source='UCI', year='2024' and the UCI page as source_url, matching the record.
  - Numbers: The Mendeley v1 file (2023-08-29) and the UCI file have the same sha256 a236549c...d1c6. UCI donation date: 2024-03-03.

**Final critic, remaining points:**

- (minor) The definition recommends exclusion, but the folder sits in the working copy. .claude/skills/rebuild-working-copy/scripts/build_all.py builds every */dataset.py under the root by default, and readme_table.py lists every folder that has a dataset.py. So the next full rebuild would build phiusil_phishing and give it a UUID, and the next table refresh would add a row for it, even though the comments ask to exclude it.
  Proposed: Lennart decides open question 1 (include or exclude). If exclusion is accepted, move dataset.py and README.md next to the v1 notebook under datasets/_maintenance/_out_of_scope/_too_late_to_add/phiusil_phishing/, or out of the working copy in some other way, before the next build_all or readme_table run. Until then, give it no README table row or CHANGELOG build entry, and pass --only when rebuilding.
- (minor) The curation record curation/records/phiusil_phishing.md disagrees with the definition. It has original_source UCI and year 2024, while the definition has Other and 2023 (Mendeley v1 of 2023-08-29 is byte-identical to the UCI file). It has no v2_path. Its comments still pose Andrej's leak question and the open grouping question, which the definition now answers.
  Proposed: Orchestrator: run sync-notebooks for v2_path. Set original_source to Other and year to 2023, or keep UCI/2024 and change the definition if Lennart prefers. Add a dated CC comment with: the exclusion case (class construction through both the URL and page families; fixed rule AUC 0.9998; phishing pages fetched after listing, 50.5% on 115 shared pages); the answers to the leak question (URLSimilarityIndex, Title and the two title scores) and the grouping question (repeated hosts are phishing-only, the grouped score is the same); the suggested marker Data Quality Issue; the published audits.
- (minor) Framework, not this dataset: AbstractCuratedDataset.make_splits assigns self.splits_comment without clean_text (src/data_foundry/v2/dataset.py line 677), although splits_comment is in _TEXT_FIELDS. The container therefore stores the comment with a leading newline, the 8-space indentation and a trailing '\n    '. This affects every v2 dataset that sets a splits_comment, for example airfoil_self_noise. Not patched, per the house rules.
  Proposed: In make_splits, use plan.comment = clean_text(self.splits_comment). This changes the checksum of every dataset with a splits_comment, so it belongs in a collection-wide change with a rebuild and a CHANGELOG entry, decided by Lennart or the orchestrator.
- (minor) Decisions the owner left open for Lennart remain open. None of them is a defect in the folder:
- include or exclude the dataset;
- which marker (Data Quality Issue as the decisive one, Trivial only as 'solved perfectly');
- keep URLCharProb, whose character distribution may come from this file's legitimate rows;
- drop the 461 slash-only pairs or the 43 homepages listed under both labels;
- keep URL as a string feature.
Each is documented with numbers in curation_comments and in the owner's report, and I re-checked all of those numbers.
  Proposed: No change now. Apply Lennart's answers when they come. If Lennart chooses 'ship anyway', the comments already name the follow-ups: recompute URLLength and the letter, digit and special-character counts and ratios from URL; reconsider the post-listing page features.

### infrared_thermography_temperature

**Recommendation:** include, with concerns.

These are real clinical measurements (1,018 subjects after dropping one duplicated measurement; FDA/UMD; CC0) with a clear, stable signal. RF reaches R^2 0.707 (RMSE 0.274 against 0.509 for the mean) and beats the dummy on all 30 splits. Model families spread (RF minus linear +0.045, paired SE 0.003). An additive model beats the source's one-feature calibration on 28 of 30 splits, so the task is not Trivial. No probe flags anything, and no leak, copy, generated-data mark or hidden group was found.

There are three concerns:
1. FLIR_groups1and2.csv must be downloaded into the warehouse before `dataset build`.
2. The modality marker is Lennart's call (open question 3).
3. The regime (IID vs temporal vs day-grouped) and the 17 retake rows are documented judgement calls with numbers (open questions 1 and 2). None of the alternatives changes the scores by more than a few percent RMSE.

**Task:** regression, target aveOralM: oral temperature in °C, the mean of two monitor-mode readings (taken during rounds 1 and 3) with a SureTemp Plus 690; 1,018 rows x 35 features; metric rmse (default for regression).

**Split:** IID over subjects: one row per subject, 10 x 3 random folds (the v2 IID protocol). The argument now rests on the use case. Each prediction is for a new person, and each subject appears once. PhysioNet keeps the date as a label "to enable study of seasonal effects", so we treat the day as a time stamp. What a thermograph takes from the day (room temperature and humidity, distance, the blackbody offset of each image) is measured for every subject and is a feature. The gap between random and day-grouped folds is reported but is not the reason for the choice. Grouping by measurement day and a temporal split on the date are open questions for Lennart, with numbers.

**Source and licence:** Unchanged from the author's version. source = "Other": the data first appeared on PhysioNet ("Facial and oral temperature data from a large set of human subject volunteers" v1.0.0, 2023-05-24). The UCI copy (dataset 925, donated 2023-11-21) links back to PhysioNet. source_url = https://doi.org/10.13026/3bhc-9065, the v1.0.0 DOI; the record's 10.13026/9ay4-2c37 is the "latest version" DOI. Licence: CC0 1.0, stated on the PhysioNet page and in its LICENSE.txt; UCI says "See linked dataset for licensing information". BibTeX cites the PhysioNet dataset (wang2023facial) and Wang et al., Sensors 22(1):215 (wang2022infrared), as PhysioNet asks. The release also holds ICI_groups1and2.csv, a second camera (1,009 subjects, 1,003 shared, same oral temperatures). That file is now mentioned in curation_comments.

**Open questions:**

1. **Split regime: IID over subjects, a temporal split on the measurement date (a calibration fitted once and used later), or folds grouped by measurement day?**
  - Implemented: IID over subjects, 10 x 3 random folds. Each prediction is for a new person who is in the file once. PhysioNet keeps the date as a time stamp for seasonal studies. The day's conditions (T_atm, Humidity, Distance, T_offset1) are features. The source's random 60/40 calibration split is cited together with its Sec. 4.5 best-case caveat.
  - Alternative: (a) Temporal: keep Date as a datetime and declare temporal = Temporal(on="Date", splits=TemporalSplits(window=None, unit="unique", n_windows=6, min_train_fraction=0.5)). This gives 6 windows of 12 days over the newest half of the 154 days. (b) Grouped: grouping = Grouping(on="day", labels="per_sample", definition=...), with the yymmdd part of SubjectID, described as stricter than Wang 2022's random split.
  - Numbers: Temporal windows: 68-116 test subjects each, 4-26 of them at or above 37.5 °C. On the same test rows, training on all earlier subjects instead of a random set of the same size changes RMSE by -0.3% to +1.7% (5 models); with 10 windows (26-69 rows) the change is -1.0% to +2.8%. A year-1 calibration used on year 2 has RMSE +3% to +9%, over-predicts by 0.06-0.08 °C, and is worse on 11-14 of 15 folds. The set-up changed: two places (Wang 2022 Sec. 2.4), and the median distance went from 0.80 to 0.60-0.65 m. February 2018 holds 43 of the 111 febrile subjects. Grouped by day against random (10x3): R^2 within 0.004 for all 5 models. Day ICC: 0.03 for the target, 0.14 for aveOralM - T_Max1; out-of-day residual ICC 0.00-0.06.
2. **The 17 subjects without a complete round-1 image: keep their round-2/3 image (taken after the first oral reading), drop them, or leave the image missing?**
  - Implemented: Keep, under the round-1 names, with no round indicator. The source counted these subjects in its round-1 analysis (Zhou 2020 Table 5: 47/30/19 febrile subjects = all 544 group-1 subjects). The timing and the bias are documented in curation_comments and Decision 2.
  - Alternative: Drop the 17 rows, which keeps every image before the prediction point. Or leave their 27 image values missing, as in the source file.
  - Numbers: Models over-predict the 17 by 0.07-0.14 °C, against at most 0.01 °C elsewhere. Their RMSE is 0.33-0.39 kept and 0.77-0.90 left missing; overall R^2 is 0.66-0.71 against 0.63-0.67. Dropping them loses 5 of the 111 subjects at or above 37.5 °C and 4 of the 49 at or above 38 °C. If left missing, the missingness marks a group that is 29% febrile (10.6% elsewhere). Retake rows are hard to detect from the features (reviewer: LightGBM AUC 0.58).
3. **Does the record's Wrong Domain / Source Modality marker exclude the dataset? The guidelines exclude features measured from images; satimage and wilt (pixel values) are No.**
  - Implemented: In scope as an exception, since Lennart asked to add the dataset. The curation_comments note names the conflict with the guidelines and gives the reasons: radiometric site temperatures in °C, sites named by ISO/TR 13154, no images released, and the task is the source's calibration. The record should record the exception; I did not edit it, per the house rules.
  - Alternative: Exclude under criterion 4A: set No with Wrong Domain / Image and remove the folder.
  - Numbers: The face maximum T_Max1 alone, with the source's segmented calibration, reaches R^2 0.700. All features reach 0.709 (RF), and an additive model 0.727, which beats the calibration on 28/30 splits. Key points were placed by hand for about half the images (Zhou 2020 Sec. 2.2). Precedent: biomechanical_orthopaedic_prediction ships as Yes (Disagreement) with the same marker.

**Final critic, remaining points:**

- (minor) The real warehouse folder local-data-warehouse/infrared_thermography_temperature/ holds only the v1 UCI data.csv. The definition reads FLIR_groups1and2.csv, so `dataset build` fails until that file is downloaded. This is an environment step, not a defect of the folder: the download_description works as written (I ran it in scratch: wget OK, sha256sum -c OK).
  Proposed: Before building, run the download_description from the repository root: mkdir/cd into local-data-warehouse/infrared_thermography_temperature, wget FLIR_groups1and2.csv and SHA256SUMS.txt from physionet.org/files/face-oral-temp-data/1.0.0/, then grep FLIR_groups1and2.csv SHA256SUMS.txt | sha256sum -c -. Optionally delete the stale v1 data.csv there so the backup zip of traced inputs and the folder agree.
- (minor) Curation record curation/records/infrared_thermography_temperature.md is not yet updated. `sync-notebooks --check` reports v2_path '(unset) -> datasets/_dev/tabarena-v0pt2/infrared_thermography_temperature/dataset.py'. The record also does not say that the 'Wrong Domain / Source Modality' marker is kept as an exception. Its comments 'Two targets' and 'I think this is grouped, subject ID is not unique' are answered in the definition but not in the record.
  Proposed: Orchestrator: run `.venv/bin/python -m data_foundry.curation.cli sync-notebooks`. Add a dated comment through the store API that says:
  - aveOralM is the target and aveOralF is dropped;
  - SubjectID is yymmdd-n, unique per row (1,020 subjects); the day was tested as a group (R^2 within 0.004 of random) and the split stays IID pending Lennart;
  - the modality marker is kept as an exception, if Lennart confirms.
  Also add the CHANGELOG entry and the README table row with the new checksum.
- (minor) The owner's report (open question 1) still quotes the old expanding-window range (-0.3% to +1.7%). The folder now says -0.2% to +2.5% (20 random sets per window). The year-1 to year-2 figure in the folder ('3-9% higher RMSE', 15 folds) is left unchanged. Over 60 day-grouped folds it is +2.5% to +8.6% (ridge 2.5, RF 5.0, ET 3.9, LightGBM 8.6, CatBoost 2.5), with bias +0.06 to +0.08 and year 1 worse in 39-57 of 60 folds, which is within rounding.
  Proposed: When relaying open question 1 to Lennart, quote '-0.2% to +2.5%' for the expanding windows. Optionally note '+2.5% to +8.6% over 60 folds' for the year transfer. No change to the folder is needed.

### african_credit_scoring_challenge

**Recommendation:** include, with concerns.

This is real Kenyan lender data with a modest signal, now with three leaks removed: the post-outcome repay amounts, the lender-amount rows that are labelled 0 by construction, and the unsettled labels.
- Linear model AUC 0.649, untuned CatBoost 0.672. The linear model beats the dummy in 9 of 9 windows.
- The leak probes find nothing that gives the label away. No generated-data marks.
- The windows follow a monthly refit.

Concerns for Lennart, none of them a reason to drop:
- The window scheme is a judgment call on very uneven data (open question 1).
- The three 2024 windows are near chance, and the customer-row count alone scores at the level of the untuned methods (open question 4).
- The lender-amount drop and the 30-day settle rule are inferred from the data, not documented by the source.
- Windows hold only 20-56 default rows, so the probes flag no_spread, drift_baseline and (on 5 windows) unstable. Re-check against tuned runs.
- Redistribution is a release question for Zindi.

**Task:** binary_classification, target default (Yes/No), renamed from Train; 58,953 rows x 11 features; metric roc_auc (the v2 default). Zindi scored F1, and v1 used f1_score..

**Split:** Temporal on disbursement_date, using a custom `_make_splits` with `Temporal(on="disbursement_date", horizon=30, horizon_unit="days")`. There are 9 windows, newest first:
- Three 30-day windows ending on the last day of the data (2024-07-11 to 2024-10-08).
- Six windows of about equal numbers of rows, cut at day boundaries. They run from 2022-10-20, the first day by which half of all rows have a settled label, to 2022-12-01, the last Type_1 loan.

A lender is assumed to refit at least once a month, so no window is longer than 30 days. Each training side holds the rows whose due_date + 30 days falls before the window starts. The 1,901 rows from 2022-12-02 to 2024-07-10 (about 100 a month) are training data only. The task is not grouped, so the record's "Grouped (NON-IID)" split/tag should go.

**Source and licence:** - **Source enum:** Zindi.
- **source_url:** https://zindi.africa/competitions/african-credit-scoring-challenge (redirects to zindi.world). The competition ran 2024-11-29 to 2025-01-12. The host is "a private asset manager that operates in several financial markets across Africa".
- **Where the files come from:** the Kaggle copy thelastsmilodon/african-credit-scoring-challenge-data. A competition participant (Kaggle user thelastsmilodon, 32nd place) uploaded it on 2025-01-14 15:51, two days after submissions closed. It has licence "other" and an empty description. I checked this with `kaggle datasets list --user thelastsmilodon` and Zindi forum thread 24482 "32nd Solution notebook".
- **Byte sizes** match the Zindi data page: 8,785,708 / 2,379,732 / 7,930 / 1,539.
- **Licence attribute:** "Zindi Competition Rules". The Zindi rules say "The data is private property of the client." and "Data Sharing: Priverty property of the client". They also ask participants to notify Zindi "upon learning of any unauthorised transmission of or unauthorised access to the challenge data".
- The licence is noted in curation_comments and download_description only. It is not a verdict reason.
- **BibTeX:** @misc Zindi2024AfricanCreditScoringChallenge.

**Open questions:**

1. **Which test windows? Bounded 30-day windows that leave the sparse 19 months (2022-12 to 2024-07) to training, or windows that also test that period with longer horizons?**
  - Implemented: Reviewer 2's variant (b) with the refit cadence made explicit:
  - 6 equal-row windows over the end of the Type_1 lending (2022-10-20 to 2022-12-01, 5-10 days each).
  - 3 x 30-day windows ending 2024-10-08.
  - Declared horizon 30 days.
  - 2022-12-02 to 2024-07-10 (1,901 rows) is training data only.
  - Alternative: - (a) Reviewer 2's variant: 5 Type_1 windows, three post-era windows of 6-7 months, and 2024-07-11 to 10-08 (90 days).
  - (b) As proposed: the author's 7 Type_1 windows plus two 45-day windows.
  - (c) The author's 9 equal-row windows, whose w1 runs 573 days with 28% of its rows in products that have no training row.
  - Numbers: Mean ROC AUC as linear / forest / LightGBM-300 / CatBoost (seed 0) / customer-row count, then test rows and default rows:
  - Implemented: 0.649 / 0.632 / 0.604 / 0.675 / 0.682. Spans 5-30 days, 13,890 rows, 289 defaults.
  - (a): 0.657 / 0.647 / 0.641 / 0.665 / 0.654. Spans 6-209 days, 15,791 rows, 498 defaults.
  - (b): 0.671 / 0.645 / 0.643 / 0.708 / 0.688. Spans 3-45 days, 14,046 rows, 304 defaults.
  - (c): 0.674 / 0.648 / 0.649 / 0.704 / 0.689. Spans 3-573 days, 15,791 rows, 498 defaults.
2. **Drop the rows whose lender funds less than one unit? They are labelled 0 by construction, but dropping them selects the 2022 test windows on a field recorded after disbursement.**
  - Implemented: Dropped all 8,899 rows with Amount_Funded_By_Lender < 0.5. That is the author's 8,520 zero-share rows plus 379 tiny-share rows, 56 of which fall in test windows. 1,978 zero-share rows fall on test-window dates. The 2022 windows lose 8.2-17.9% of the rows of their dates.
  - Alternative: - Keep them with the share columns, as v1 did: a model learns that a lender amount below one unit means repaid.
  - Keep them and drop both share columns: about 90-130 defaults stay labelled 0.
  - Drop only the zero-share rows (the author's filter).
  - Numbers: - 0 of 8,899 rows are labelled 1.
  - Same customers and months: 1.04% of the dropped loans carry a charge over 20%, against 0.40% of their other loans. Customers borrowed again after 1.1% of the charged dropped loans, against 87-88% after uncharged loans.
  - Untuned LightGBM: 0.639 implemented, 0.646 with all rows kept, 0.656 dropping only zero shares.
3. **How long until a label counts as known?**
  - Implemented: 30 days after the due date. 802 rows (84 labelled 1) are dropped, and training sides hold rows with due_date + 30 < window start.
  - Alternative: Due date only, or all earlier loans (v1 used a 3-day gap).
  - Numbers: - Untuned LightGBM: 0.639 with the 30-day rule, 0.676 with due date only, 0.685 with all earlier loans.
  - Default rate of 2024 rows: 19.6% / 15.3% / 11.6% at 1-7 / 8-14 / 15-30 days past due, against 6.9-10.2% from 31 days on.
4. **Keep customer_id and keep the dataset, given that most of its signal is the customer's history and the three 2024 windows are near chance?**
  - Implemented: customer_id kept as a categorical, and the dataset kept under task_probes.md rules 2 and 4. Re-check against the first tuned runs.
  - Alternative: Drop customer_id, so every loan is scored like a new applicant. Or hold the task-worth decision until tuned results exist.
  - Numbers: - LightGBM: 0.639 with customer_id, 0.527 without. CatBoost (3 seeds): 0.672 with, 0.606 without.
  - The count of the customer's training rows alone scores 0.682: 0.516-0.621 on the 2024 windows, 0.616-0.800 on the 2022 windows. It is at or above CatBoost in 6 of 9 windows.
  - 2024 windows: linear 0.535-0.631, CatBoost 0.484-0.619.
  - Test rows of a customer with a training row: 85-96% in 2022, 12-44% in 2024.
5. **Release note (not a verdict reason): may the collection redistribute a file that reached Kaggle through a participant's upload made after the close?**
  - Implemented: License attribute 'Zindi Competition Rules'. download_description and the licence bullet say the copy is a participant's upload after the close.
  - Alternative: Ask Zindi or the host before release.
  - Numbers: - Zindi rules: 'The data is private property of the client.'; participants must notify Zindi 'upon learning of any unauthorised transmission of or unauthorised access to the challenge data'.
  - The Kaggle copy was uploaded 2025-01-14 15:51 by thelastsmilodon (32nd place), with licence 'other' and an empty description.

**Final critic, remaining points:**

- (minor) The checksum changed from the owner's v2:21dfafbf6d88... to v2:c3099aeaf1867fa62da05867f2716f8f987b49d0cb8f12e4a35f70381e8a7cd2, because metadata text is part of the hash. Anything the orchestrator writes from the owner's report would carry the stale value.
  Proposed: Use v2:c3099aeaf1867fa62da05867f2716f8f987b49d0cb8f12e4a35f70381e8a7cd2 in the tabarena-v0pt2 README table and CHANGELOG entry.
- (minor) The pandas 3 interpreter path in the task (scratchpad/add3/venvs/pd3/bin/python) does not exist. The venv is at scratchpad/venvs/pd3/bin/python.
  Proposed: Fix the path in the orchestrator script before the same check runs for phiusil_phishing and infrared_thermography_temperature.
- (minor) The curation record curation/records/african_credit_scoring_challenge.md still lists required_split 'Grouped (NON-IID)', tag 'Non-IID (Grouped)', 'AI-Filled (Verify)', needs_review ai_unverified and status WIP (DF). This contradicts the temporal-only definition.
  Proposed: As the orchestrator: drop the Grouped split and tag, record the v2_path, and add a dated comment with the verdict and the five open questions.
- (minor) The task_probes.md cases table has no row for this dataset's flags (no_spread and drift_baseline on 9 windows; unstable on the default 5 windows). The owner deferred this to the orchestrator.
  Proposed: Add a row: untuned linear 0.649, CatBoost 0.672 (3 seeds); no tuned results; the customer-row count 0.682 is not read as Trivial (rule 4); kept under rules 1-3; re-check against the first tuned runs.
- (minor) An untracked catboost_info/ folder (catboost_training.json, learn/, learn_error.tsv) is still at the repository root. Another process wrote it, not this dataset's agents.
  Proposed: Delete it once all agents have finished.
- (minor) While I worked, pytest collection of tests/test_v2_datasets.py failed for every dataset because another agent's half-written scaffold datasets/_dev/tabarena-v0pt2/corporate_credit_rating/dataset.py had problem_type 'TODO' (created 00:59 UTC). It collected again a few minutes later. That folder is not one of this run's three datasets.
  Proposed: Re-run pytest -q tests/test_v2_datasets.py after all agents finish, and make sure the README table and CHANGELOG cover corporate_credit_rating if it stays in the working copy.
