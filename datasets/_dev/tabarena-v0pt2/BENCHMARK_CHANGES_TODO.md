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
  sat11_hand_algo_runtime, protein_model_quality_rf_pcp (2026-11-05; huesken_sirna_efficacy reopened to follow). On
  protein a model that compares a candidate with its protein's others scores 0.483 against 0.322 per-protein
  correlation for a row-only one, so ignoring `context` costs a third of the skill. data-foundry's
  `examples/benchmark_container.py` does not use it yet: `feature_columns` drops the group column, so no model there
  sees which test rows share a group.
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

## Special features: one contract for every kind

Added 2026-11-02 (Lennart: one general form "like the target column", not a field per kind, so that later kinds such
as a shipped embedding fit without new fields). Data Foundry side done.

- [ ] **Read `task_metadata.special_features` in the adapter, whatever the kind.** A v0.2 container lists every model
  input that needs handling beyond its dtype as a `data_foundry.schema.SpecialFeature`:
  - `name`; `kind` (`smiles`, `spectrum`; more later);
  - `layout`: `column`, one column (a SMILES), or `group`, several columns in a fixed order encoded together (a
    spectrum);
  - `columns`; `encoding_required`, true when the raw values are no model input (a SMILES string), false when they
    are numbers a model can read (a spectrum's intensities);
  - `recommended_encoding`, a spec id; `details`, what the kind adds (a spectrum's axis, unit, technique, state).

  `data_foundry.curation_container.special_features(container, kind=None)` lists them, and
  `data_foundry.v2.special.encode_special_feature(df, feature, encoding=None)` replaces a feature's columns by their
  encoding, where they stand. `encodings_for(feature)` gives the candidates, the recommended one first. Map each
  feature to an AutoGluon special type named by its `kind` (`FeatureMetadata` takes any name), with one generator per
  kind that calls the entry point.
- [ ] **The guard is generic:** a feature with `encoding_required` is encoded or left out, never passed on as its
  dtype (a SMILES as text). A feature without it may go to a model as it is when the method switches the encoding off.
- [ ] **Caching follows `Encoding.scope`:** `value` (one row per distinct value: SMILES, e5, dates), `row` (one per row,
  no fitting: spectra; cheap, no cache needed) or `split` (fitted on each split's training rows: TF-IDF). The cache
  contract below keys every cached encoding by its spec id.

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
- [ ] **SMILES columns: encode them as structures (Data Foundry side done, 2026-11-01; since 2026-11-02 a special
  feature of kind `smiles`, layout `column`, `encoding_required`).** A v0.2 container ships a molecule's structure as
  a `string` column listed in `task_metadata.special_features` (recommended encoding e.g.
  `rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1`); `special_features(container, "smiles")` lists them. Datasets: apistox,
  drug_induced_autoimmunity_prediction, nci_aids_antiviral_screen, the five qsar_* sets (and the molecule candidates
  to come). TabArena needs, in this order:
  - **A guard first.** The model-agnostic pipeline marks every pandas `string` column as text
    (`StringFixAsTypeFeatureGenerator`) and embeds it with Qwen3-Embedding-8B at 32 dimensions. On `apistox` that
    embedding of the SMILES scored no better than no structure at all (ROC AUC 0.78-0.81 against 0.70-0.82; ECFP4
    bits or character n-grams 0.83-0.85; record, 2026-10-07). Until the generator below exists, the adapter must drop a
    special feature with `encoding_required` (or encode it as below), never pass it on as text.
  - **The adapter** passes `special_features` into the task, and the pipeline maps them to AutoGluon special types by
    kind (`smiles` here); the text generators exclude them.
  - **A SMILES feature generator** with the recommended encoding (`data_foundry.v2.chemistry.encode_smiles`: RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts, one row per molecule; Data Foundry is already a dependency) or TabArena's own,
    cached by value under the encoding's id on the cache contract above, so a fit needs no RDKit.
    The recommended encoding is wide (about 1,400 columns, the ECFP4 counts added by default because they helped once:
    qsar_tid_11's LightGBM R^2 from 0.601 to 0.658): "just one pipeline choice that we can later investigate for the
    benchmark", and a feature selection step may follow it (Lennart, 2026-11-01).
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

## Spectra

Added 2026-11-02 (PR #21, Andrej's proposal, with Lennart's decisions: spectra as special features in a group of
columns, full resolution, the field's published defaults). Data Foundry side done; nothing changes for a pipeline that
ignores them, since the bins stay numeric features.

- [ ] **Spectra are special features of kind `spectrum`** (layout `group`, `encoding_required` false), read through the
  contract above: `special_features(container, "spectrum")`; `details` holds the axis, its unit, the technique and
  the state (`raw` / `processed` / `peaks`). Datasets: pancreatic_cancer_mouse_detection (raw SELDI-TOF, 6,771 bins)
  and micro_mass (a VITEK MS peak list, 1,082 bins); about 40 Raman, infrared and near-infrared candidates are queued.
- [ ] **A spectrum feature generator** that encodes each spectrum row by row with its `recommended_encoding`
  (`encode_special_feature(df, feature)`, `data_foundry.v2.special`): for a raw mass spectrum
  MALDIquant's steps (`ms-sqrt-sg21-snip100-tic-r1`), for anything else the columns as they are
  (`spectrum-as-is-r1`). No fitting, no labels, so the same values in every split; it costs milliseconds per spectrum,
  so it needs no cache, but its time counts in each method's fit time like the cached encodings. Switchable per
  method: a method that processes spectra itself gets the raw bins.
- [ ] **Decide the default encoding of a raw mass spectrum: a benchmark choice** (Lennart, 2026-11-02). The literature
  names no single best pipeline:
  - Cruz-Marcelo et al. 2008 (Bioinformatics 24:2129): "none of the methods show uniformly better performances".
  - Wegdam et al. 2009 (Proteome Science 7:19): "No pre-processing method significantly outperforms the other", "the
    settings for pre-processing parameters lead to large differences in classification accuracy", and "We advocate
    the evaluation over a range of parameter settings"; the classifier mattered more than the preprocessing.
  - Meuleman et al. 2008 (BMC Bioinformatics 9:88): normalising helps, and scaling by a spread beats scaling by a mean.

  There are two published traditions, the square root and the log, and three candidates are registered in
  `data_foundry.v2.spectra` (`recommended_encodings()["mass_spectrum"]`, the placeholder default first):
  - `ms-sqrt-sg21-snip100-tic-r1`: the MALDIquant vignette (Gibb and Strimmer 2012); the placeholder default.
  - `ms-driams-sqrt-sg21-snip20-snip100-tic-r1`: DRIAMS's settings (Weis et al. 2022, Nature Medicine; their script
    `DRIAMS-A_2015_preprocessed.r` in BorgwardtLab/maldi_amr), the largest machine-learning study on MALDI-TOF
    spectra. Their trim to 2,000-20,000 Da and 3 Da bins change the columns, so they belong to the width step below.
  - `ms-cromwell-udwt-mm-tic-log2-r1`: the log tradition of SELDI-TOF analysis. Cromwell's wavelet denoising and
    monotone-minimum baseline (Coombes et al. 2005, Proteomics 5:4107; MD Anderson's MATLAB code), then the total ion
    current and log2 as in Cromwell's and Ciphergen's pipelines (Wegdam et al. 2009). PR #21's own chain is close to
    it.

  The procedure, fixed before any result is seen:
  - Candidates are published workflows only, with the raw bins as the reference. No setting is tuned on the
    benchmark's folds.
  - Datasets: every raw mass-spectrum dataset of the benchmark, at least two or three. Today only
    pancreatic_cancer_mouse_detection; next the DRIAMS candidate and the NCI-FDA prostate SELDI set.
  - Models: three families, a foundation model (TabPFN), gradient boosting, and a linear model or PLS-DA.
  - Criterion: the mean normalised score over datasets and families; the candidate that hurts no family against the
    raw bins wins ties. Then the most cited, then the simplest.
  - Every method can switch the encoding off.

  What one dataset shows so far, pancreatic (60 shipped splits, ROC AUC, 2026-11-02), and why it is not enough:

  | Model | Raw | MALDIquant | DRIAMS | Cromwell log2 | PR #21's chain (reconstructed) |
  |---|---|---|---|---|---|
  | TabPFN v3.5 | 0.659 | 0.690 | not run | not run | 0.716 |
  | HistGradientBoosting | 0.585 | 0.685 | 0.628 | 0.604 | 0.642 |
  | LightGBM | 0.577 | 0.676 | 0.624 | 0.604 | 0.649 |
  | Random forest | 0.536 | 0.681 | 0.663 | 0.591 | 0.657 |
  | PLS-DA, 5 components | 0.635 | 0.691 | 0.646 | 0.639 | 0.713 |
  | Logistic regression | 0.663 | 0.646 | 0.603 | 0.628 | 0.708 |

  The DRIAMS and Cromwell settings were made for spectra at the instrument's full resolution; pancreatic's are binned
  at 400 ppm, which may be why they trail here.
- [ ] **Width goes to the feature-limit step**, not to the encoding: the encodings keep every bin (Lennart,
  2026-11-02). Averaging adjacent bins costs little (PR #21: TabPFN 3.5 0.733 against 0.725 with 8-bin averages on
  pancreatic) if a model needs fewer columns.
- [ ] **PLS-DA as a reference method for spectra.** It is the field's usual linear method, and on raw mass spectra it
  ranks differently from the tabular models (PR #21: third on the raw bins, first on the processed ones).
- [ ] **Vibrational spectra: check the encodings on the first datasets.** RamanBench (arXiv:2605.02003) ran its
  leading methods (AutoGluon 1.5, TabPFN v2.5, TabICL v2) on the raw spectra and preprocessed only for its chemometric
  baselines, so the default is the spectrum as it is. Three alternatives are registered (2026-11-04, Lennart: "one can
  add all and select as needed"): `vib-als-snv-r1` (an ALS baseline and SNV, RamanBench's linear-model default),
  `vib-snv-r1` and `vib-sg11-d1-r1` (a Savitzky-Golay first derivative, 11 points, order 2). On OSSL's infrared
  spectra LightGBM went from 1.74 (as it is) to 1.33, 1.39 and 1.24 RMSE in percent; measure them on each spectrum
  dataset before choosing a default.

## Ordinal features

- [ ] **Keep the order of an ordered category in the pipeline, and give it to the models.** v0.2 containers store
  ordinal scales as ordered categories (`CategoricalDtype(levels, ordered=True)`): the curated state, whatever the
  benchmark does with it (Lennart, 2026-10-31: "In data foundry, we want to keep the right state independent of what the
  downstream benchmark does"). Since 2026-10-31 that includes the 167 scales the sources ship as numbers (ratings,
  grades, bands), so this change is due before the next benchmark run. Two steps. The preprocessing (TabArena's, used as
  in BeyondArena going forward) must keep the order: AutoGluon's `CategoryFeatureGenerator` rebuilds every category
  unordered (`pd.Categorical(X[col], categories=...)`). And the models must be told: for example the codes in order as a
  number for the tree models, with the categories kept for a model that wants them. Without it, the scales shipped as
  numbers reach the models as unordered categories, which raised LightGBM's error by 6.0% on
  student_portuguese_performance, 4.8% on breast_cancer_prediction and 3.9% on gallstone_disease (TabPFN v3.5 barely
  changes). With the order, LightGBM's error fell by 1.56% on average over 55 datasets (12 better, 3 worse), up to 31%
  on eryhemato_squamous_disease; TabPFN v3.5's by 0.25% (10 better, 6 worse); a linear model on the bare codes loses
  where a scale is not monotone in the target (run of 2026-10-30, the shipped splits).

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

## Ordered targets and the positive class (2026-11-01, PR #37)

Classification targets ship their classes as words now (CLEAN-25). Binary targets are "No"/"Yes" with "Yes" the
event, so sorting the classes gives the right positive class. Five multiclass targets are ordered categories whose
category order is not the sorted order (cardiotocography: normal < suspect < pathologic; dementia_prediction;
hepatitis_c_prediction; chicago_traffic_crashes; ai4d_lab_tanzania_tourism_classification_challenge).

Since 2026-11-05 (Lennart, issue 5 of ai4d_lab_tanzania_tourism_classification_challenge) the scorer follows
scikit-learn's convention for every target: `scorer(container)` reads probability columns in the sorted order of the
classes (`classes_`, the column order of `predict_proba`), and the declared order stays in the container as type
information. A harness passes `predict_proba` as it comes, or a DataFrame whose columns are the class names, which the
scorer matches by name (a missing or unknown class name is an error). Before that change the scorer read a plain
array in the category order: a harness that reorders its columns to the categories, as the example did, now passes
them as named columns or in sorted order. A score computed with the columns aligned either way is the same number.

## Test rows predicted without the other test rows (2026-11-04, PR #33 second review)

- [ ] **Check that a method never reads the other test rows of a split.** medical_facility_operational_data,
  sepsis_prediction and 5g_energy_consumption carry fields that are history at each row's own arrival; a method that
  looks at the other test rows of a block (a test-time fit, transductive inference, the test block's own statistics)
  would see the future. Data Foundry ships a protocol line in each definition and no per-row scorer (Lennart: "we can
  check if the model cheats"), so the guarantee sits in the benchmark: predict each test row from the training rows and
  its own row, or check that a method's predictions do not change when the other test rows change. A method that
  learns from the test block is called out and not benchmarked (LEAK-9, amended 2026-11-05, Lennart: "we investigate
  models, and would find out if they do transductive learning which we can call out and not benchmark").
