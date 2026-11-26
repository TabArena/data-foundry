# Benchmark hand-off: what TabArena changes for the v0.2 datasets

What the benchmark harness (`tabarena/`) has to change to use the TabArena v0.2 containers as they are curated. The
Data Foundry side of every item is done unless the item says otherwise. The facts and dataset lists are from the 174
task definitions of this folder on 2026-11-25 ([how to regenerate them](#regenerating-the-lists)); the history of each
decision is in the curation records, the knowledge skills and [`CHANGELOG.md`](CHANGELOG.md).

The API names are those of Data Foundry's `main` on 2026-11-25. A restructure moves `data_foundry.definition.*` into the
package and adds one task view per container (`container.task()`) that gathers the helpers named here; this file
follows it.

## Summary

Before the first v0.2 run:

- [ ] [1. Pin the Data Foundry release that reads format 2](#1-pin-the-release-that-reads-format-2) (all).
- [ ] [2. Build the model inputs from `feature_columns`](#2-model-inputs-feature_columns) (all; matters for the 48
  grouped tasks, the 18 with scoring columns and the 12 with a label-dated time column).
- [ ] [3. Score by the container's metric spec](#3-the-metric-score-by-the-spec) (all; 26 metric names, 23 beyond
  `roc_auc`, `log_loss` and `rmse`).
- [ ] [4. Inner validation that follows the outer split](#4-inner-validation-follows-the-outer-split) (68 temporal,
  48 grouped, 5 with unit weights).
- [ ] [5. Fit on at most the row budget](#5-the-row-budget-of-the-_1m-versions) (18 `_1m` versions).
- [ ] [6. Encode special features, never pass a SMILES as text](#6-special-features) (9 SMILES, 3 spectra).
- [ ] [7. Keep the order of ordered categories](#7-ordered-categories) (57 definitions declare ordinal scales).
- [ ] [8. Training weights, behind a gate](#8-training-weights) (6 tasks).

Next:

- [ ] [9. Score grouped tasks at their prediction unit](#9-scoring-at-the-prediction-unit) (3 tasks).
- [ ] [10. Use only the group information the use case allows](#10-group-context) (8 tasks with `all_rows`).
- [ ] [11. Weight validation losses like the test score](#11-validation-weights-and-unit-weights) (tasks with a
  row or unit weight).
- [ ] [12. One cache contract for encodings, with their time counted](#12-encoding-caches-and-their-time).
- [ ] [13. Report the effective sample size of group-level scores](#13-effective-sample-size).
- [ ] [14. Check that no method reads the other test rows](#14-test-rows-predicted-without-the-other-test-rows).

Open decisions for the benchmark, with the evidence so far: [losses for deviance-scored tasks](#a-losses-for-deviance-scored-tasks),
[errors of metrics without a fixed best value](#b-errors-of-metrics-without-a-fixed-best-value),
[threshold tuning for label metrics](#c-threshold-tuning-for-label-metrics),
[the default encoding of a raw mass spectrum](#d-the-default-encoding-of-a-raw-mass-spectrum),
[vibrational spectra](#e-vibrational-spectra), [text and date encodings](#f-text-and-date-encodings),
[raw SMILES on the main leaderboard](#g-raw-smiles-on-the-main-leaderboard),
[the LightGBM default on force_2020](#h-the-lightgbm-default-on-force_2020).

## Before the first v0.2 run

### 1. Pin the release that reads format 2

v0.2 containers are format 2 (`container.format_version == 2`): the task metadata carries the metric spec, the
grouping, the scoring columns and the weights, and the splits are a row table (`rows.parquet`, one
`split_r<repeat>_f<fold>` column per split holding `train`, `test` or nothing). Releases up to v0.0.5 cannot read
them; TabArena requires `data-foundry>=0.0.3` today.

- Release Data Foundry before the rebuilt containers are uploaded, and raise TabArena's floor to that release.
- `experiment_metadata.splits` returns `{repeat: {fold: (train, test)}}` for both formats, so the split loop needs no
  change.
- An older Data Foundry must never read a newer container: dropping a field such as `time_of` would put a leak column
  back among the features. From the bug-fix PR of 2026-11-25 on, the loader refuses unknown task and split fields
  (it dropped them with a warning before).

### 2. Model inputs: `feature_columns`

Build X from `data_foundry.curation_container.feature_columns(container)`, for every pipeline. It leaves out:

- the target;
- the group column(s): today only the `tabarena_default` pipeline drops them (its `GroupAggregationFeatureGenerator`),
  and under `default` (`AutoMLPipelineFeatureGenerator`) the group id is a feature;
- the scoring columns (`task_metadata.scoring_columns`): a metric's inputs such as an era, a group or a weight, never
  model inputs. A weight column's test values in particular are the realized amount at risk, which a model at the
  quote does not have (LEAK-41): read as a feature it gains 0.0052 deviance on bemtpl97, 0.0072 to 0.0088 on fremtpl2
  and 0.09 to 0.12 weighted Gini on australian_vehicle_insurance_2004_2005 (2026-11-08);
- a time column that dates the label (`task_metadata.time_of == "label"`, also `grouping.time_of`): the moment the
  label became known, after the prediction point. 12 tasks: 2_month_survival_rate_prediction, apistox,
  bank_marketing, california_house_prices_2020, coffee_rating_prediction, fremtpl2,
  infrared_thermography_temperature, labour_inspection_compliance, qsar_tid_11, sdss_17, seismic_bumps,
  wine_quality.

These columns stay in the frame for the split and the scorer (items 3 and 4). `task_metadata.prediction_time`, when
set (no task yet), names the column of the prediction point, a model input like any other.

### 3. The metric: score by the spec

A format-2 container stores its metric as data: `task_metadata.objective_metric` (`data_foundry.schema.MetricSpec`:
`name`, `kind`, `prediction` `proba` / `label` / `value`, `greater_is_better`, `params`, `inputs`, `origin`,
`target_transform`, and the source's text). Format 1 (BeyondArena) keeps `objective_metric_name`. Every definition
declares the metric its source scored, or an explicit fallback (rules MET-1 to MET-17 in
`.claude/skills/knowledge-curation/references/metrics.md`).

- Stop replacing unknown metrics silently. Today any name other than `roc_auc`, `log_loss` and `rmse` becomes the
  problem type's default without a warning, so `mape`, `rmsle` and every custom metric below are never used. An
  unsupported name must fail.
- Score with `data_foundry.metrics.scorer(container)(y_true, y_pred, row_index)`, `row_index` being the scored
  rows' positions in `container.dataset`. It does what the bare metric does not:
  - inverts a modelling scale (`target_transform` `log`, `log1p`, `log10`: 29 tasks) on both the true values and the
    predictions; models fit and predict on the shipped scale;
  - floors predictions at the metric's `min_prediction` (the deviances);
  - takes the metric's input columns (a group, an order, a weight: 19 tasks) from the scored rows;
  - aggregates per group for a group-unit task (item 9);
  - reads probability columns in the sorted order of the classes (scikit-learn's `classes_`, also for an ordered
    target), or a DataFrame whose columns are the class names, matched by name;
  - scores a constant prediction 0 for the correlation metrics.
- Wrap it as an AutoGluon scorer (`autogluon.core.metrics.make_scorer`: `greater_is_better` from the spec,
  `needs_proba` for `prediction == "proba"`, `needs_class` for `"label"`). Inner validation, early stopping and tuning
  use the same scorer. Two pieces come with the task view on the Data Foundry side: an `optimum` per metric name
  (not in the spec today; see [B](#b-errors-of-metrics-without-a-fixed-best-value) for the metrics without one), and
  row positions taken from the index of a pandas `y_true`, since AutoGluon calls a scorer without them.
- A metric is NaN where it is undefined (one class in a fold for the AUC-type metrics, a zero true value for `mape`).
  Treat NaN as an undefined fold, not as a failed model. The build checks refuse folds where the declared metric is
  undefined, so a NaN on a shipped split means the harness scored other rows than the split's.

The metrics in use:

| Metric | Kind, prediction | Tasks |
|---|---|---|
| `roc_auc` | standard, proba | 67 (42 fallbacks) |
| `rmse` | standard, value | 27 (11 fallbacks) |
| `log_loss` | standard, proba | 21 (18 fallbacks) |
| `rmsle` | standard, value | 19 |
| `mae` | standard, value | allstate_claims_severity, medical_facility_operational_data, wine_quality, zillow_prize |
| `mse`, `r2`, `mape` | standard, value | electric_motor_temperature_prediction; mercedes_benz_greener_manufacturing; 5g_energy_consumption (stand-in for the Zindi WMAPE, whose weights are not published) |
| `mean_poisson_deviance` | standard, value; input `weight`, `min_prediction` | bemtpl97 (`expo`), fremtpl2 (`Exposure`) |
| `mean_tweedie_deviance` | standard, value; `power`, `min_prediction` | noaa_storm_events_damage (input `weight`), pricing_game_2017_french_mtpl |
| `rescaled_mean_tweedie_deviance` | custom, value; input `weight` | pricing_game_2016_french_fleet |
| `normalized_gini` | custom, value | allstate_claim_prediction_challenge_1m, loan_default_prediction_imperial_college, spanish_homeowners_motor_insurance_2010_2014, spanish_motor_insurance_2015_2018 |
| `normalized_weighted_gini` | custom, value; input `weight` | australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line, liberty_mutual_fire_peril_loss_cost, spanish_motor_insurance_coverage_level_2022_2024 |
| `ordered_lorenz_gini` | custom, value; input `weight` | wisconsin_local_government_property_insurance_fund |
| `mean_group_pearsonr` | custom, value; input `group` | huesken_sirna_efficacy, numerai_v5_2_1m (`numerai_corr`), protein_model_quality_rf_pcp |
| `weighted_pearsonr` | custom, value; input `weight` | g_research_crypto_forecasting_1m |
| `mean_group_normalized_rmse` | custom, value; input `group` | noaa_afsc_bottom_trawl_survey_cpue, wadden_sea_sibes_macoma_abundance |
| `par_k` | custom, value; input `group` | asp_potassco_classification, sat11_hand_algo_runtime (PAR10) |
| `rmspe` | custom, value | rossmann_store_sales |
| `net_revenue_at_cost` | custom, value | pva_revenue_prediction_kddcup98 |
| `cost_matrix` | custom, proba or label | aps_failure, credit_g (proba); force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition (label) |
| `precision_at_k`, `average_precision_at_k` | custom, proba | coil_2000, labour_inspection_compliance; huntprohibited_1m |
| `gini_top_capture` | custom, proba | amex_non_iid_1m (per customer, item 9) |
| `hierarchical_balanced_accuracy` | custom, label; input `group` | micro_mass |
| `normalized_early_detection_utility` | custom, label; inputs `group`, `order` | sepsis_prediction_1m |

### 4. Inner validation follows the outer split

- Temporal tasks (68): cut the inner hold-out forward on the time column. Read it, with the group column(s), from
  `split_columns(container)` (`time_on_to_groups_data` reads `X[time_on]` today), and only then fit on
  `feature_columns(container)`, which may leave the time column out (item 2). Dropping it first breaks the temporal
  validation; never dropping it feeds the model a time it does not have.
- Grouped tasks (48): group-aware inner folds for every grouped task. The BeyondArena protocol does it
  (`task_specific_validation=True`); the TabArena v0.1 protocol mixes a group's rows across inner train and validation.
- Unit weights (5, item 11): keep a unit's rows on one side of the inner split.
- The inner validation of a `_1m` version is drawn from the sampled rows, never added to them (item 5).

### 5. The row budget of the `_1m` versions

A `_1m` version caps only its test sides in the container (at most 500k rows per split); its train sides keep every
row they may use. The container records the budget, `experiment_metadata.row_budget` (`{train: 1000000, test:
500000}`), and the default sampler, `experiment_metadata.train_sampling`. 18 versions: aeolus_rebuilt,
allstate_claim_prediction_challenge, amex_non_iid, ashrae_great_energy_predictor_iii,
climate_model_weather_forecasting, consumer_complaints, cooking_time, delivery_eta, expresso_churn_prediction,
fraud_detection_in_electricity_and_gas_consumption, g_research_crypto_forecasting, home_credit_default_stability,
huntprohibited, maps_router_eta, numerai_v5_2, nyc_taxi_trip_duration, pkdd_15_taxi_trip_time_prediction_ii,
sepsis_prediction (each `_1m`).

- Fit on `data_foundry.sampling.subsample_train(container, repeat, fold)`: for a temporal train side the newest year,
  extended back in time until it holds 1M rows, then a random 1M of those (a year in `task_metadata.time_unit`:
  numerai's eras are weeks); whole groups of a grouped side; stratified rows of an IID side. Deterministic; the whole
  train side for a container without a budget. Without it a model trains on the whole history.
- N is a hard cap, inner validation included (Lennart, 2026-11-10).
- A method may choose its N rows itself, from the split's train side only and keeping `train_sampling.unit` (whole
  groups, whole time values). Such results are a separate leaderboard track.
- Load only a split's rows: the largest versions ship tens of millions of rows (maps_router_eta_1m has 989 float
  columns). Read the split's rows from `rows.parquet` and the sampled rows from `dataset.parquet`.
- Read N from the container, never assume 1M: a `_10m` version would carry its own budget.

### 6. Special features

A container lists every model input that needs handling beyond its dtype in `task_metadata.special_features`
(`data_foundry.schema.SpecialFeature`: `name`, `kind` `smiles` / `spectrum`, `layout` `column` / `group`, `columns`,
`encoding_required`, `recommended_encoding`, `details`). One contract for every kind (Lennart, 2026-11-02).

- The guard first: a feature with `encoding_required` is encoded or left out, never passed on as its dtype. The
  model-agnostic pipeline marks every pandas `string` column as text and embeds it (Qwen3-Embedding-8B, 32
  dimensions); on apistox that embedding of the SMILES scored no better than no structure at all (ROC AUC 0.78-0.81
  against 0.70-0.82; ECFP4 bits or character n-grams 0.83-0.85).
- Map each feature to an AutoGluon special type named by its `kind`, with one generator per kind that calls
  `data_foundry.special.encode_special_feature(df, feature)` (`encodings_for(feature)` lists the candidates, the
  recommended one first). The text generators exclude them.
- SMILES (9: apistox, drug_induced_autoimmunity_prediction, nci_aids_antiviral_screen, qsar_aquatic_toxicity,
  qsar_bioconcentration, qsar_biodeg, qsar_fish_toxicity, qsar_oral_toxicity, qsar_tid_11): the recommended
  encoding is RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts (about 1,400 columns, cached by value;
  the counts lifted qsar_tid_11's LightGBM R^2 from 0.601 to 0.658). "Just one pipeline choice that we can later
  investigate for the benchmark"; a feature selection step may follow (Lennart, 2026-11-01).
- Spectra (3: micro_mass, a VITEK MS peak list; open_soil_spectral_library, mid-infrared; pancreatic_cancer_mouse_detection,
  raw SELDI-TOF): `encoding_required` is false, the bins stay numeric features, so a pipeline that ignores them still
  runs. The generator encodes row by row with `recommended_encoding` (no fitting, the same values in every split).
  The defaults are open ([D](#d-the-default-encoding-of-a-raw-mass-spectrum), [E](#e-vibrational-spectra)).
- Caching follows `Encoding.scope`: `value` (one row per distinct value: SMILES, e5, dates), `row` (spectra; no cache
  needed) or `split` (fitted on each split's training rows: TF-IDF). See item 12.
- Every default preprocessing step can be switched off per method (Lennart, 2026-11-01): a method that brings its own
  encoding gets the raw column.

### 7. Ordered categories

v0.2 containers store ordinal scales as ordered categories (`CategoricalDtype(levels, ordered=True)`), including the
scales the sources ship as numbers (ratings, grades, bands): the curated state, whatever the benchmark does with it
(Lennart, 2026-10-31). AutoGluon's `CategoryFeatureGenerator` rebuilds every category unordered.

- Keep the order in the preprocessing, and give it to the models (for example the codes in order as a number for the
  tree models, the categories kept for a model that wants them).
- Without it the scales shipped as numbers reach the models as unordered categories, which raised LightGBM's error by
  6.0% on student_portuguese_performance, 4.8% on breast_cancer_prediction and 3.9% on gallstone_disease. With the
  order LightGBM's error fell by 1.56% on average over 55 datasets (12 better, 3 worse), TabPFN v3.5's by 0.25%
  (run of 2026-10-30, the shipped splits).
- Targets: binary targets are "No"/"Yes" with "Yes" the event, so the sorted classes give the positive class. An
  ordered multiclass target (cardiotocography, dementia_prediction, hepatitis_c_prediction, chicago_traffic_crashes,
  ai4d_lab_tanzania_tourism_classification_challenge) is scored in the sorted order of its classes, like any other
  (item 3); the declared order stays in the container as type information.

### 8. Training weights

A format-2 task may declare a training weight, `task_metadata.sample_weight`
(`data_foundry.curation_container.sample_weight(container)`): a scoring column that the metric reads as its row weight
(MET-15), such as the years insured of a claims rate. 6 tasks: australian_vehicle_insurance_2004_2005 (`exposure`),
bemtpl97 (`expo`), frempl_french_motor_personal_line (`Exposure`), fremtpl2 (`Exposure`),
pricing_game_2016_french_fleet (`exposure`), spanish_motor_insurance_coverage_level_2022_2024 (`actual_exposure`).
Every model is fitted with it as the row weight and never gets it as a feature; a fit without it targets another
quantity (on fremtpl2 an unweighted fit scores worse than the constant rate).

- The gate: no container with a `sample_weight` enters a run until the adapter builds X from `feature_columns`,
  passes the weight to every fit and scores with Data Foundry's scorer. A contract test on a toy container guards
  it: its weight, used as a feature or ignored, moves the score past a stated tolerance.
- Scoring columns never reach `predict` (item 2): the adapter passes them to the scorer, and the `sample_weight`
  column to the fit as the training rows' weight.
- Weighted validation: early stopping, tuning and ensembling use the weighted metric, with the same `min_prediction`
  floor as the test score (in AutoGluon, `TabularPredictor(sample_weight=col, weight_evaluation=True)`).
- The models to update: AutoGluon's NN_TORCH, FastAI and KNN drop the weight with a log line at level 15; RealMLP,
  TabM, the TabPFN wrappers, TabICL, Mitra and TabDPT never read it; XGBoost's early stopping ignores the evaluation
  weights; CatBoost stops on RMSE for a metric it does not know; AutoGluon has no Poisson scorer and no offset.
- A model-fit contract test per model: fit with half the rows at weight 0, the prediction must change. Other fit
  properties are worth the same kind of test (transductive use of the test rows, item 14; determinism).
- One default for a weight-blind model: draw each bag fold's training rows with probability in proportion to the
  weight (the validation rows untouched), seeded, recorded as `weight_mode=resampled` and flagged on the leaderboard.
  Against a weighted fit it costs 0.0007 to 0.0018 deviance on fremtpl2; on australian_vehicle_insurance_2004_2005 it
  closes 90% of the deviance gap but only 45% of the Gini gap.

## Next

### 9. Scoring at the prediction unit

A task whose prediction unit is the group (`grouping.prediction_unit == "group"`) is scored with one value per group,
so each group counts once; `experiment_runner.evaluate` scores every row on its own today. The metadata is
`task_metadata.grouping` (`data_foundry.schema.Grouping`: `prediction_unit`, `aggregation`, `context`,
`definition`), read with `CuratedContainer.grouping` (None for format 1, which is scored per row). 3 tasks: musk
(`any`: a molecule is a musk if any conformation is), amex_non_iid_1m (`last`: the latest statement decides, per
customer), fraud_detection_in_electricity_and_gas_consumption_1m (`mean`).

| Prediction unit | Label of a group | Default group prediction | Metric computed on |
|---|---|---|---|
| `row` | | | the rows (as today) |
| `group` + `mean` | the shared label | mean of the rows' predicted probabilities (regression: of the predictions) | one value per group |
| `group` + `any` | positive if any row is | max of the rows' P(positive) | one value per group |
| `group` + `last` | the latest row's label (by the group's time) | the latest row's prediction | one value per group |

- `scorer(container)` applies the default aggregation when a method returns row predictions. A method may return one
  prediction per group itself (a multiple-instance model, a learned pooling) and is scored by the same metric on the
  same unit; such an override needs `context="all_rows"` (item 10).
- Inner validation and tuning use the same resolved metric, so a model is not tuned on rows and scored on groups.
- Until TabArena scores at the group unit, the three are scored per row; nothing is held back.

### 10. Group context

`grouping.context` says what a model may know about a group when it predicts one of its rows: `none` (each row
stands alone; 40 grouped tasks), `all_rows` (all rows of a new group are known at prediction time; 8 tasks:
amex_non_iid_1m, force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition,
fraud_detection_in_electricity_and_gas_consumption_1m, huesken_sirna_efficacy, musk, pricing_game_2017_french_mtpl,
protein_model_quality_rf_pcp, sat11_hand_algo_runtime) or `past_rows` (only the group's earlier rows; none yet).

- Build group aggregation features only where the context allows them: from all rows of a test group for
  `all_rows`, causally for `past_rows`, none for `none`. Today they are built for every `per_group` task.
- It matters: on protein_model_quality_rf_pcp a model that compares a candidate with its protein's others scores
  0.483 against 0.322 per-protein correlation for a row-only one.

### 11. Validation weights and unit weights

- Weight every validation loss (early stopping, model selection, tuning, ensembling) by
  `data_foundry.curation_container.validation_weight(container)`, the metric's row weight, so a model optimises what
  the test score counts (Lennart, 2026-11-08).
- A task with a `unit_weight` counts each unit once in the score (MET-17; 5 tasks: boreal_postfire_lichen_biomass,
  dementia_prediction, noaa_storm_events_damage, pancreatic_cancer_mouse_detection, superconductivity): weight the
  validation loss by its column, keep a unit's rows on one side of an inner split (`unit_weight(container).unit`,
  also in `split_columns`), and never fit with it as a training weight. A contract test: a toy container whose units
  have 1 and 5 rows; the adapter's validation score equals the scorer's on the same rows.

### 12. Encoding caches and their time

- One cache contract for every precomputed encoding. Only the text embedding is cached today
  (`tabarena.benchmark.preprocessing.text_cache`: a value-to-vector parquet per task, keyed by the encoder spec id,
  shipped inside the container as `tabarena_text_cache_<id>.parquet`, loader modes `require` / `auto` / `off`).
  Generalise it so any expensive or version-sensitive encoding (text embeddings, SMILES, later others) uses the same
  keying by spec id, versioning, shipping and loader modes (Lennart, 2026-11-01).
- Count the encoding's time in the fit time. Under `text_cache_mode="require"` the embeddings are computed once,
  outside every timed fit, and their cost is recorded nowhere. Measure each cache's compute time when it is made
  (total and per value, with the encoder spec and the hardware), store it with the cache, and add it to each method's
  fit time (the test rows' share to its inference time), noted in the record's description of the timing.

### 13. Effective sample size

For a task scored per group, or by a metric over groups, the number of test groups per fold is the sample size of the
score (34 molecules per fold in musk). Show it next to the results.

### 14. Test rows predicted without the other test rows

medical_facility_operational_data, sepsis_prediction_1m and 5g_energy_consumption carry fields that are history at
each row's own arrival; a method that looks at the other test rows of a block (a test-time fit, transductive
inference, the block's own statistics) would see the future. Data Foundry ships a protocol line in each definition
and no per-row scorer, so the guarantee sits in the benchmark: predict each test row from the training rows and its
own row, or check that a method's predictions do not change when the other test rows change. A method that learns
from the test block is called out and not benchmarked (LEAK-9, Lennart, 2026-11-05).

## Open decisions

### A. Losses for deviance-scored tasks

"We should definitely stick to what practitioners do wherever possible, but we also need more research on that"
(Andrej, 2026-11-09). A practitioner on a count or claim-cost task fits a Poisson or Tweedie loss with a log link;
most benchmark methods fit squared error and predict values near or below zero on a zero-heavy target, which the
metric's floor then scores. On pricing_game_2017_french_mtpl (repeat 0, untuned) LightGBM fitted by squared error
scores 74.94 at a 1 EUR floor and 102.83 at 0.1 EUR, fitted with the Tweedie loss 75.51 and 78.11; the constant
scores 63.31. Tasks: fremtpl2, bemtpl97 (`mean_poisson_deviance`), pricing_game_2016_french_fleet
(`rescaled_mean_tweedie_deviance`, power 1.5), pricing_game_2017_french_mtpl, noaa_storm_events_damage
(`mean_tweedie_deviance`, power 1.5).

- The proposal: the adapter sets the metric's loss with a log link where a method has one, and floors every method's
  output at `min_prediction` in validation as in test (the scorer does it on the test rows already).

  | Metric | Objective | Parameter |
  |---|---|---|
  | `mean_poisson_deviance` | LightGBM `poisson`, XGBoost `count:poisson`, CatBoost `Poisson` | none |
  | `mean_tweedie_deviance`, `rescaled_mean_tweedie_deviance` | LightGBM `tweedie`, XGBoost `reg:tweedie`, CatBoost `Tweedie` | the metric's `power` as the variance power |

- To research first: which methods have such a loss or can be given one (a custom loss for the neural methods), how
  each behaves with it; whether matched losses change the rankings against squared error with the floor, over seeds;
  what practitioners fit per task (the source papers and winning solutions), and whether the benchmark follows each
  task's practice or one rule per metric.

### B. Errors of metrics without a fixed best value

TabArena turns a score into an error, `optimum - score`, and bencheval reads the error as at least 0 with 0 perfect:
`verify_error` raises on a negative error, and improvability, `relative_error` and `baseline_advantage` are ratios of
errors, so they change with where the zero sits (Elo, win rate, rank and the normalized error do not). Every metric
in use has a bound no score passes, except two (Lennart, 2026-11-16, review of PR #100):

- `net_revenue_at_cost` (pva_revenue_prediction_kddcup98): the net revenue per scored donor of mailing every donor
  whose predicted gift is above the $0.68 cost. Its best value is the oracle's and changes by fold (0.757 over all
  donors); mailing nobody scores 0, everyone 0.111, the cup's winner 0.153, and a model that mails non-donors falls
  below 0. Keep `greater_is_better=True` and no clip at 0. Options: normalize it in Data Foundry to `R / R_oracle`
  on the same rows (at most 1; the ranking within a fold unchanged, no TabArena refactor), or keep dollars and let a
  scorer return its own error per scored set. A fixed optimum or a clip at 0 is not a fix.
- `ordered_lorenz_gini` (wisconsin_local_government_property_insurance_fund) is not normalized: its best value is
  below 1 and varies by fold, so `1 - score` measures the distance to a value no model reaches. The same two options
  apply.

### C. Threshold tuning for label metrics

"We could also just add threshold tuning by default, which we should in tabarena for metrics that can benefit from
it" (Lennart, 2026-10-21). A metric scored on hard labels measures the threshold a method picks as much as the model:
choose it on the inner validation predictions by the same metric. Today: force_2020 (`cost_matrix` on labels),
micro_mass (`hierarchical_balanced_accuracy`), sepsis_prediction_1m (`normalized_early_detection_utility`). The
sources fixed hard-label decisions (MET-4, MET-6), so the metric stays and the threshold becomes part of the method.

### D. The default encoding of a raw mass spectrum

A benchmark choice (Lennart, 2026-11-02): the literature names no single best pipeline (Cruz-Marcelo et al. 2008;
Wegdam et al. 2009: "We advocate the evaluation over a range of parameter settings"). Three candidates are
registered in `data_foundry.special.spectra`, the placeholder default first: `ms-sqrt-sg21-snip100-tic-r1` (the MALDIquant
vignette), `ms-driams-sqrt-sg21-snip20-snip100-tic-r1` (DRIAMS, Weis et al. 2022; its trim and 3 Da bins belong to
the width step) and `ms-cromwell-udwt-mm-tic-log2-r1` (Cromwell, the log tradition of SELDI-TOF).

- The procedure, fixed before any result is seen: published workflows only, the raw bins as the reference, nothing
  tuned on the folds; every raw mass-spectrum dataset of the benchmark (only pancreatic_cancer_mouse_detection today,
  next the DRIAMS and NCI-FDA prostate candidates); three model families (TabPFN, gradient boosting, a linear model
  or PLS-DA); the mean normalised score over datasets and families, ties to the candidate that hurts no family, then
  the most cited, then the simplest.
- So far, on pancreatic (60 splits, ROC AUC, 2026-11-02): MALDIquant beats the raw bins for every tree model
  (LightGBM 0.577 to 0.676, random forest 0.536 to 0.681) and TabPFN v3.5 (0.659 to 0.690); DRIAMS and Cromwell
  trail, possibly because pancreatic's spectra are binned at 400 ppm. One dataset is not enough.
- The width goes to the feature-limit step, not to the encoding: the encodings keep every bin (Lennart, 2026-11-02).
  Averaging adjacent bins costs little if a model needs fewer columns: TabPFN 3.5 scored 0.725 on 8-bin averages
  against 0.733 on every bin of pancreatic (PR #21).
- PLS-DA as a reference method for spectra: the field's usual linear method, ranked differently from the tabular
  models (third on pancreatic's raw bins, first on the processed ones).

### E. Vibrational spectra

RamanBench (arXiv:2605.02003) ran its leading methods on the raw spectra and preprocessed only for its chemometric
baselines, so the default is the spectrum as it is (`spectrum-as-is-r1`). Three alternatives are registered
("one can add all and select as needed", Lennart, 2026-11-04): `vib-als-snv-r1`, `vib-snv-r1`, `vib-sg11-d1-r1`. On
open_soil_spectral_library LightGBM went from 1.74 (as it is) to 1.33, 1.39 and 1.24 RMSE in percent; measure them on
each spectrum dataset before choosing a default.

### F. Text and date encodings

`data_foundry.encodings.recommended_encodings()`: dates by skrub's
`DatetimeEncoder(add_weekday=True, periodic_encoding="circular")`, as BeyondArena and `tabarena_default` do; text by
TF-IDF fitted on the training rows and reduced by SVD (`encode_text_tfidf`) and by `intfloat/e5-small-v2` sentence
embeddings (`encode_text_e5`). Neither text encoding wins everywhere (Lennart, 2026-11-01). TabArena v0.2 embeds text
with Qwen3-Embedding-8B at 32 dimensions: compare it with both on the text datasets before fixing the default.

### G. Raw SMILES on the main leaderboard

Whether a method may read the raw SMILES with its own encoder on the main leaderboard is open (Lennart, 2026-11-01:
"we keep this discussion for later").

### H. The LightGBM default on force_2020

Untuned LightGBM with the default `min_child_weight` of 0.001 diverged on force_2020 (grouped fold 0, test log loss
14-15; with `min_child_weight=1`, 0.81), as on mice_protein_trisomy_discriminant. Since the definition masks the
impossible readings, the task probe's LightGBM gives 0.872 and no longer diverges. Check it once the dataset is built
(Lennart, 2026-10-21: "we can do that later").

## Regenerating the lists

The dataset lists come from the definitions, without building anything:

```python
from data_foundry.definition.registry import discover_datasets
from data_foundry.definition.dataset import _build_metadata, effective_row_budget

for name, cls in sorted(discover_datasets("datasets/_dev/tabarena-v0pt2").items()):
    _, task = _build_metadata(cls)
    print(name, task.objective_metric.name, task.time_of, task.grouping, task.sample_weight,
          task.unit_weight, [type(s).__name__ for s in cls.special_features], effective_row_budget(cls))
```
