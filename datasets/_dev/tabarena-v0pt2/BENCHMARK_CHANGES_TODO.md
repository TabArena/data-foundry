# Benchmark changes to do (TabArena side)

Changes the benchmark harness (`tabarena/`) needs so that the v0.2 datasets are used as they are curated. They came
out of the review of grouped data on 2026-10-01 (counts and file references are from that day). The data-foundry
side (metadata, checks, the dataset review) is tracked in the curation records and [`CHANGELOG.md`](CHANGELOG.md).

## Grouped tasks

- [ ] **Never use the group column as a model feature.** Only the `tabarena_default` preprocessing pipeline drops it
  (its `GroupAggregationFeatureGenerator`); under the `default` pipeline (`AutoMLPipelineFeatureGenerator`) the group
  id stays a feature, and so it does in data-foundry's `examples/benchmark_on_beyond_arena.py`. Separate `group_on`
  from the features in the adapter, for every pipeline.
- [ ] **Group-aware inner validation for every grouped task.** The BeyondArena validation protocol uses groups for
  the inner folds (`task_specific_validation=True`); the TabArena v0.1 protocol does not, so its inner folds mix rows
  of one group across train and validation.
- [ ] **Score at the task's prediction unit.** `experiment_runner.evaluate` scores every row on its own, unweighted.
  A task whose prediction unit is the group needs its row predictions aggregated per group with the declared rule
  and one score per group, so each group counts once. The rules the sources need: `mean` (replicate measurements of
  one label, as in the retired parkinsons dataset), `any` / max (multiple-instance: musk, a molecule is a musk if any conformation is),
  `last` (the latest row decides: amex, scored per customer at the latest statement) and `select_min` (algorithm
  selection: sat11 picks the algorithm with the lowest predicted runtime per instance and is scored by that
  algorithm's true runtime, e.g. PAR10 or the share of the single-best to virtual-best gap closed). The metadata is
  `task_metadata.grouping` (`data_foundry.schema.Grouping`: `prediction_unit`, `aggregation`, `context`,
  `definition`) of a format-2 container (`container.format_version == 2`), read with `CuratedContainer.grouping`. A
  format-1 container (the shipped BeyondArena ones) has no grouping and is scored per row.
  The v0.2 group-unit datasets: musk (`any`), amex_non_iid_1m (`last`, by `S_2`), sat11_hand_algo_runtime
  (`select_min`). How it becomes a scoring spec is TabArena's choice; our
  recommendation (resolution table, named metrics, methods that return their own group predictions, tuning on the
  same metric) is [below](#recommended-scoring-of-grouped-tasks).
- [ ] **Use the information about a group that the use case allows.** The group aggregation features are built for
  every `per_group` task, from all rows of a test group. That fits a task where all rows of a new group are known at
  prediction time; a task that may only use earlier rows of a group (`group_time_on`) needs causal aggregates, and a
  task whose rows stand alone (sepsis: each hour from its own measurements) none. The field is `grouping.context`
  (`none`, `all_rows`, `past_rows`); `all_rows` in v0.2: musk, amex_non_iid_1m,
  sat11_hand_algo_runtime.
- [ ] **Dataset-specific metrics.** Every v0.2 definition now declares the metric its source scored, or an explicit
  fallback (the rules: `.claude/skills/knowledge-curation/references/metrics.md`, MET-1 to MET-13), and a format-2
  container stores it as data: `task_metadata.objective_metric` (`data_foundry.schema.MetricSpec`: `name`, `kind`
  `standard` or `custom`, `prediction` `proba` / `label` / `value`, `greater_is_better`, `params`, `inputs`,
  `origin` `source` / `stand_in` / `context` / `fallback`, `original`, `reference`, `definition`, `reason`,
  `target_transform`). A regression target may ship on a modelling scale (`target_transform` `log`, `log1p` or
  `log10`; `identity` by default): models fit and predict on the shipped scale, and the metric is computed after the
  inverse of both the true values and the predictions (`score` does it), so the scorer must not be the bare
  metric on the shipped values. The field
  `objective_metric_name` is gone from format 2; format 1 (BeyondArena) keeps it. The reference implementation of
  every name is `data_foundry.v2.metrics` (numpy, pandas, scikit-learn and scipy only; the custom metrics are tested
  against their official code). The adapter (`adapter.py`) has to:
  - **Read the spec.** Take `objective_metric.name` in format 2 (`container.format_version == 2`) and
    `objective_metric_name` in format 1.
  - **Register the custom scorers.** Wrap `data_foundry.v2.metrics.score(spec, y_true, y_pred, labels=..., **inputs)` in
    an AutoGluon scorer (`autogluon.core.metrics.make_scorer`, with `greater_is_better` and `optimum` from the spec,
    `needs_proba` for `prediction == "proba"`, `needs_class` for `"label"`; the module docstring has the sketch). A
    metric with `inputs` (a group, an order, a weight) needs the scored rows' values of those columns: pass them by row
    index, as `data_foundry.v2.metrics.scorer(container)(y_true, y_pred, row_index)` does. A task predicted per group
    (`grouping.prediction_unit == "group"`) is aggregated first by `grouping.aggregation` (`scorer` does it; the section
    below). Inner validation and tuning use the same scorer. A correlation metric (`pearsonr`, `weighted_pearsonr`,
    `mean_group_pearsonr`) is undefined for a constant prediction (`data_foundry.v2.metrics` returns NaN): the scorer
    needs a guard so a constant prediction (a dummy, a collapsed model) scores 0, no signal, instead of breaking the
    fold.
  - **Drop the scoring columns from the features.** `task_metadata.scoring_columns` (column, role, used_by,
    description) are the metric's inputs and never model inputs, like the group column:
    `data_foundry.curation_container.feature_columns(container)` returns the frame's features without them.
  - **Stop replacing unknown metrics silently.** Today any metric other than `roc_auc`, `log_loss` and `rmse` becomes
    the problem type's default without a warning, so `5g_energy_consumption`'s `mape` and the custom metrics below
    are never used. An unsupported name should fail or warn loudly, naming the dataset and the fallback used.
  - **Tune the decision threshold by default for threshold metrics.** "We could also just add threshold tuning by
    default, which we should in tabarena for metrics that can benefit from it" (Lennart, 2026-10-21). A metric
    scored on hard labels (`prediction == "label"`: `f1`, `f1_weighted`, `balanced_accuracy`, `cost_matrix` with
    label predictions, `hierarchical_balanced_accuracy`, `normalized_early_detection_utility`) measures the threshold
    a method picks as much as the model; choose it on the inner validation predictions by the same metric (for two
    classes the threshold on P(positive); for a cost matrix scored from probabilities the least-cost decision is
    already in the metric). The sources fixed hard-label decisions (MET-4, MET-6), so the metric stays and the
    threshold becomes part of the method.

  The metrics per dataset, from the metric decisions of 2026-10-21
  (`local-data-warehouse/_runs/2026-10-21_metrics/decisions.json`; 15 of them wait for the curator, marked `*`):

  | Metric | Kind, prediction | Datasets |
  |---|---|---|
  | `roc_auc` | standard, proba | 76: 49 fallbacks, 25 from the source (porto_seguro's normalized Gini among them), 2 stand-ins; `*` anes_voting_2026, heart_disease (the three Detrano hospitals, merged on 2026-10-21), hepatitis_survival_prediction, home_credit_default_stability_1m, lending_club, sepsis_survival_minimal_clinical_records |
  | `rmse` | standard, value | 45: 27 fallbacks, 18 from the source (RMSLE as `rmse` on a log1p target included); `*` video_transcoding_time_prediction |
  | `log_loss` | standard, proba | 26: 22 fallbacks, 2 from the source, 2 stand-ins; `*` covertype, hepatitis_c_prediction |
  | `mae` | standard, value | allstate_claims_severity, forest_fires, wine_quality, zillow_prize; stand-in for `*` corporate_credit_rating_cat_data_set_ratings_raitings |
  | `mse` | standard, value | electric_motor_temperature_prediction |
  | `r2` | standard, value | mercedes_benz_greener_manufacturing |
  | `mape` | standard, value | 5g_energy_consumption (stand-in for the Zindi WMAPE, whose weights are not published) |
  | `f1` | standard, label | african_credit_scoring_challenge |
  | `f1_weighted` | standard, label | none since dataorg_financial_health_prediction_challenge was retired (2026-10-22) |
  | `balanced_accuracy` | standard, label | hiva_agnostic |
  | `cost_matrix` | custom, label or proba (`params.prediction`) | force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition (label, the 11 x 11 penalty matrix); `*` aps_failure (proba, false alarm 10, miss 500), `*` credit_g (proba, Statlog's 5:1) |
  | `precision_at_k` | custom, proba | coil_2000 (`k_fraction` 0.2); `*` labour_inspection_compliance (`k_fraction` 0.5) |
  | `average_precision_at_k` | custom, proba | huntprohibited_1m (`k` 12,500) |
  | `gini_top_capture` | custom, proba | amex_non_iid_1m (top 4%, negatives weighted 20), per customer (`grouping.aggregation` `last`) |
  | `rmspe` | custom, value | rossmann_store_sales |
  | `weighted_pearsonr` | custom, value; input `weight` | g_research_crypto_forecasting_1m (scoring column `Weight`) |
  | `mean_group_pearsonr` | custom, value; input `group` | numerai_v5_2_1m (`method` `numerai_corr`, scoring column `era`) |
  | `hierarchical_balanced_accuracy` | custom, label; input `group` | micro_mass (scoring column `Strain`) |
  | `par_k` | custom, value; input `group` | sat11_hand_algo_runtime (PAR10, cutoff 5,000 s, group `instance_id`, `select_min`) |
  | `normalized_early_detection_utility` | custom, label; inputs `group`, `order` | sepsis_prediction_1m (scoring columns `Patient_ID`, `Hour`; each test patient's hours whole) |
- [ ] **Report the effective sample size.** For a task scored per group, the number of test groups per fold is the
  sample size of the score (34 molecules per fold in `musk`); show it next to the results.

## Recommended scoring of grouped tasks

The metadata is meant to determine the official score, so every method is scored the same way. The resolution we
recommend:

| Prediction unit | Label of a group | Default group prediction | Metric computed on |
|---|---|---|---|
| `row` | | | the rows, unweighted (as today) |
| `group` + `mean` | the shared label | mean of the rows' predicted probabilities (regression: of the predictions) | one value per group |
| `group` + `any` | positive if any row is | max of the rows' P(positive) | one value per group |
| `group` + `last` | the latest row's label (`time_on`) | the latest row's prediction | one value per group |
| `group` + `select_min` / `select_max` | | the row with the lowest / highest prediction | the true value of the selected row (for example PAR10 for sat11) |

* The metric is the task's `objective_metric` (format 1: `objective_metric_name`) applied at that unit: ROC AUC over molecules for musk on the max
  of each molecule's row probabilities, over rows for in_vehicle.
* Named metrics that need the group structure get the group ids and the order from the metadata: the PhysioNet 2019
  utility for sepsis (each patient's ordered hours), `gini_top_capture` per customer for amex, the 5G challenge's
  weighted MAPE (not computable: a `mape` stand-in), micro_mass's accuracy averaged per strain and then per species,
  PAR10 for sat11 (a timeout is a runtime of the 5,000 s cutoff, counted 10 times).
* Methods: the task fixes the unit and the metric. The harness applies the default aggregation when a method returns
  row predictions; a method may return one prediction per group itself (a multiple-instance model, a learned pooling,
  another rule) and is scored with the same metric on the same unit. What a method may look at follows `context`; a
  group-level override needs `all_rows`. At the row unit every row is predicted.
* Inner validation and tuning should use the same resolved metric, so a model is not tuned on rows and scored on
  groups.
* Report the number of test groups per fold next to a group-level score; it is the score's sample size.
* Until TabArena scores at the group unit, the three group-unit datasets are scored per row; the metadata says what
  the right unit is, and nothing is held back.

## Encodings and their caches

Added 2026-11-01 (Lennart: "introduce caching for all encodings in a nice way, which we should anyhow revisit for
tabarena-v0.2 with good time keeping and adding it on top of the benchmark record").

- [ ] **One cache contract for every precomputed encoding.** Today only the semantic-text embedding is cached
  (`tabarena.benchmark.preprocessing.text_cache`: a value -> vector parquet per task, keyed by the encoder spec id
  `<model>-d<dim>-r<revision>`, shipped inside the container as `tabarena_text_cache_<id>.parquet`, loader modes
  `require` / `auto` / `off`). Generalise it so any expensive or version-sensitive encoding (text embeddings, a
  SMILES encoding if we adopt one, later others) uses the same keying, versioning, shipping and loader modes, rather
  than one module per encoding.
- [ ] **Time keeping for cached encodings: count it in the fit time.** Under the bundle default
  `text_cache_mode="require"` the embeddings are computed once by `generate_text_cache`, outside every timed fit, and
  their cost is recorded nowhere: a method on a text task gets the embedding for free. Measure each cache's compute
  time when it is made (total and per value, with the encoder spec and the hardware), store it with the cache, and add
  it to each method's fit time (the test rows' share to its inference time) in the benchmark record, as if the method
  had computed the encoding itself (Lennart, 2026-11-01). Note it in the record's description of the timing, so a
  reader knows cached preprocessing is included.
- [ ] **SMILES columns: encode them as structures (Data Foundry side done, 2026-11-01).** A v0.2 container now ships a
  molecule's structure as a `string` column listed in `task_metadata.semantic_columns`
  (`data_foundry.schema.SemanticColumn`: `column`, `semantic_type` `smiles`, `description`,
  `recommended_encoding`, e.g. `rdkit2d-maccs-rdkit2026.03.6-r1`); `data_foundry.curation_container.semantic_columns
  (container, "smiles")` lists them. Datasets: apistox, drug_induced_autoimmunity_prediction, qsar_bioconcentration,
  qsar_oral_toxicity, qsar_tid_11 (and the molecule candidates to come). TabArena needs, in this order:
  - **A guard first.** The model-agnostic pipeline marks every pandas `string` column as text
    (`StringFixAsTypeFeatureGenerator`) and embeds it with Qwen3-Embedding-8B at 32 dimensions. On `apistox` that
    embedding of the SMILES scored no better than no structure at all (ROC AUC 0.78-0.81 against 0.70-0.82; ECFP4
    bits or character n-grams 0.83-0.85; record, 2026-10-07). Until the generator below exists, the adapter must drop a
    semantic column (or encode it as below), never pass it on as text.
  - **The adapter** passes `semantic_columns` into the task, and the pipeline maps them to an AutoGluon special type
    `smiles` (`FeatureMetadata` takes any special-type name); the text generators exclude it.
  - **A SMILES feature generator** with the recommended encoding (`data_foundry.v2.chemistry.encode_smiles`: RDKit's 2D
    descriptors and the 166 MACCS keys, one row per molecule; Data Foundry is already a dependency) or TabArena's own,
    cached by value under the encoding's id on the cache contract above, so a fit needs no RDKit.
  - Whether a method may read the raw SMILES with its own encoder on the main leaderboard is open (Lennart,
    2026-11-01: "we keep this discussion for later").
- [ ] **Recommended encodings of dates and text (`data_foundry.v2.encodings`, `recommended_encodings()`).** Dates: skrub's
  `DatetimeEncoder(add_weekday=True, periodic_encoding="circular")`, as BeyondArena and `tabarena_default` do today
  (`encode_datetime`). Text: TF-IDF fitted on the training rows (words, or character 2- to 5-grams for one-token
  values), reduced by SVD (`encode_text_tfidf`), and `intfloat/e5-small-v2` sentence embeddings (`encode_text_e5`):
  neither wins everywhere, so check both (Lennart, 2026-11-01). TabArena v0.2 embeds text with Qwen3-Embedding-8B at
  32 dimensions; compare it with both on the text datasets before fixing the default.
- [ ] **Every default preprocessing step can be switched off** per method (Lennart, 2026-11-01: "in general, all
  preprocessing may be disable-able"): a method that brings its own encoding of SMILES, text or dates gets the raw
  column.

## Library version

- [ ] **Require the data-foundry release that carries the v0.2 metadata.** v0.2 containers store
  `split_random_state` (and `grouping` for grouped tasks); releases up to v0.0.5 forbid unknown fields and cannot load
  them. Release data-foundry before uploading the rebuilt containers and raise TabArena's `data-foundry>=0.0.3` floor.
  From this version on, `CuratedContainer.load` ignores fields it does not know, with a warning.

## Frame sizes of the v2 split protocol

- [ ] **Temporal `_1m` versions ship up to 2.5M rows** (each split still trains on at most 1M and tests on at most
  500k rows): check storage and loading for `cooking_time_1m`, `delivery_eta_1m` and `maps_router_eta_1m` (2.5M rows,
  989 float columns for maps).

## Model defaults

- [ ] **Check the LightGBM default on force_2020 once it is built.** Untuned LightGBM with the default
  `min_child_weight` of 0.001 diverged on force_2020 (grouped fold 0, 100k rows: test log loss 14-15; with
  `min_child_weight=1`, 0.81), as on mice_protein_trisomy_discriminant. After the definition masked the impossible
  readings (DCAL 10,006.8, DRHO -7,429.3 and others) the task probe's LightGBM gives 0.872 and no longer diverges, so
  extreme values were the likely trigger. Left for later (Lennart, 2026-10-21: "we dont need to check the benchmark
  case, we can do that later, it is fine as is for now").
