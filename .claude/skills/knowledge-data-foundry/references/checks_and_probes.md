# Running the checks and probes

How to run the automated checks and the probes on a Data Foundry dataset, and the checks that only Data Foundry has.
What to check and how to judge it is the general [verification.md](../../knowledge-curation/references/verification.md);
how to read the probes is [leak_checks.md](../../knowledge-curation/references/leak_checks.md) and
[task_probes.md](../../knowledge-curation/references/task_probes.md). The readings of each flag, in rank order, are in
[evidence.md](../../knowledge-curation/references/evidence.md), "Reading a probe".

Run everything from the repository root with `.venv/bin/python`. On a shared machine cap the threads of every run
(`OMP_NUM_THREADS=2 OMP_THREAD_LIMIT=2 OMP_WAIT_POLICY=PASSIVE MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
POLARS_MAX_THREADS=2`) and keep `--n-jobs` small ([agent_runs.md](agent_runs.md)).

## The bundle checks: `dataset check`

```bash
.venv/bin/python -m data_foundry.curation.cli dataset check datasets/_dev/tabarena-v0pt2/<folder>
```

runs the whole pipeline, the data checks, the bundle checks (`data_foundry.bundle_checks`, judged by the v2 split
protocol for a format-2 container) and `_decisions`, without saving (no UUID), and rewrites the folder's `README.md`.
Compare the README with the committed one: an unexpected diff (checksum, split sizes, new findings) means the
definition drifted from its evidence. Then:

* every error blocks a PR;
* for every warning, say whether it is a real problem for this dataset or correct as it is; a warning the curator
  accepts goes into `accepted_check_warnings` with the reason (propose the exact edit);
* do not restate passing checks: "Bundle checks: 0 errors, 3 warnings (2 accepted)" is the right level.

The slug-by-slug actions are in [definitions.md](definitions.md), "Bundle checks". Never run `dataset build` to verify:
it mints a new UUID, and a build is the curator's call (or an explicit ask). A task with a training weight has its own
checks (`task_sample_weight_not_metric_weight`, `task_weight_invalid`, `task_rate_count_not_whole`), and two warnings
say a weight may be missing (`task_metric_weight_without_sample_weight`, `task_feature_looks_like_exposure`):
[definitions.md](definitions.md), Field mapping, `sample_weight`. A unit weight (MET-17) has two
(`task_unit_weight_not_one_per_unit`, `task_unit_weight_unit_split`): Field mapping, `unit_weight`.

## The probes

The probe methods are the general library in
[`../../knowledge-curation/scripts/`](../../knowledge-curation/scripts/); the command-line entry points here, in
[`../scripts/`](../scripts/), load a Data Foundry dataset (its definition, or with `--built` the built container named
in the README's build record) through `dataset_io.py` and call it. The probes use the shipped target and splits; when
the definition changed the target, run the same checks on the source's labels in a scratch notebook
(`ds = workbench()`). A special feature (`special_features`) enters every probe in its recommended encoding
(`encode_special_feature`), as a benchmark would give it to a model: a SMILES as RDKit's 2D descriptors, the MACCS keys
and the ECFP4 counts, a spectrum as its columns with the encoded values; the blind reviewer's clean room keeps the
values as shipped. The bundle check `dataset_special_feature` finds each feature's columns and runs its kind's checks:
`dataset_smiles_column` parses every SMILES with the pinned RDKit, `dataset_spectrum` checks that a spectrum's columns
are numeric and finite and warns about missing intensities.

A task with a training weight (`sample_weight`) is probed with it: `dataset_io.py` fills `ProbeInput.weights` from it,
and the task, leak and group probes fit every model with the weight and take the weighted dummy (sum of target x
weight over the sum of the weights: the portfolio rate); their R^2, RMSE, ROC AUC and log loss are weighted.
`task_probes.py` and probe 22 also score the declared metric, and `task_probes.py` reports the share of each family's
predictions at the metric's floor (`min_prediction`, MET-13).

```bash
K=.claude/skills/knowledge-data-foundry/scripts
.venv/bin/python $K/leak_probes.py <unique_name> [--splits 3] [--max-rows 50000] [--max-single-features 300] [--n-jobs 8] [--out DIR]
.venv/bin/python $K/leak_probes.py <unique_name> --period-only [--time-on COLUMN] [--period D|W|M|Q|Y] [--tz ZONE] [--positive LABEL] [--tail N]
.venv/bin/python $K/leak_probes.py <unique_name> --raw [--splits 3] [--max-rows 50000] [--n-jobs 8] [--out DIR]
.venv/bin/python $K/leak_probes.py <unique_name> --weight-proxy [--weight-column COLUMN] [--objective metric|l2|OBJ] [--seeds 3] [--splits 3] [--max-rows 50000]
.venv/bin/python $K/leak_probes.py <unique_name> --forced-split [--time-on COLUMN] [--period Y|Q|M|W|D] [--objective metric|l2|OBJ] [--seeds 3] [--forced-splits 9] [--max-rows 50000]
.venv/bin/python $K/task_probes.py <unique_name> [--built] [--splits N] [--no-text] [--out DIR]   # or --all --jobs 8
.venv/bin/python $K/group_probes.py <unique_name> [--repeats 3] [--permutations 100]
.venv/bin/python $K/hidden_groups.py <unique_name> [--built] [--include-grouped] [--out DIR]     # or --all
.venv/bin/python $K/generated_probes.py <unique_name> [--built] [--out DIR]                     # or --all
.venv/bin/python $K/dtype_probes.py <unique_name> [--codebook URL] [--no-fetch] [--out DIR]    # or --all --jobs 4
.venv/bin/python $K/tuned_results.py <unique_name> [--feature auto]
```

* `leak_probes.py`: probes 1-6, 10, 13, 14 and 17-23 of the leak table (all features, each feature alone, missing
  indicators, drop one, exact copies across the split with and without string and datetime columns, each long string
  column alone as text (TF-IDF + SVD on the train side, character n-grams for one-token strings), nearest-neighbour
  agreement and the label-free distance score, a depth-2 and depth-3 tree on the label), with untuned LightGBM on the
  first shipped splits. The exact copies are counted on every shipped split and every row, by label: the same label
  only, another label only (each with one copy or two or more), both labels. The features are the definition's model
  inputs; a scoring column kept as the time key is not one of them. When the task has a time column (`--time-on` names
  another), probe 13 sets the target of the newest periods against the band of the earlier ones (rows per day, the event
  rate or class shares, a regression's mean, p50 and p90, a count's zero share) and says whether the end falls out of
  band, the mark of right-censoring; it picks the period (`--period` sets it), takes the minority class as the event
  (`--positive`), reads integer times as years or periods, never as dates, reads dates that all fall on 1 January as
  years, cuts a rank (an integer with about one row per value) into equal-count periods by its order, and
  `--period-only` runs it without a model. With more columns than `--max-single-features` only the most informative
  enter the single-feature fits, and the output says how many were screened out, so a 49,000-column omics table takes
  minutes. A multiclass ROC AUC is the mean over the classes present in the test fold. Group columns are never features.
  For a classification task it also scores the number format alone (probe 17), and, when the raw file is one table
  holding the target column, counts per column and class the cells on a straight line between their neighbours in the
  raw file's order (probe 18: gaps filled by interpolation). `--raw` runs the probes of the raw state alone (probes 10
  and 18 to 21; leak_checks.md, "The raw state"): the target in the raw row order, the rows `_clean` removed against the
  kept ones, each dropped raw column alone on the first shipped splits, and copies before deduplication. It traces each
  curated row to its raw row (`process(lineage=True)`, `dataset_io.from_definition(ds, raw=True)`) and says when it
  cannot. `--weight-proxy` runs probe 22 alone (leak_checks.md, "Probe 22"; `curation_probes.leak.weight_proxy`) on the
  task's sample weight, or the column `--weight-column` names: a cross-fitted LightGBM of the weight on the features
  (R^2, Spearman, top features), the declared weighted metric with the weight added as a feature against the honest fit,
  each top feature's weight-mediated gain with its SD over folds and seeds, and the weight alone: 1/weight as the
  prediction for a Gini, a fit of the target on the weight (the same objective and training weight) for any other
  metric, next to the weighted constant. `--objective metric` (the default) fits the weighted actuarial model: a
  deviance's own (Poisson or Tweedie); under any other metric (a Gini) a rate with a training weight gets Poisson when
  the rate times the weight is a whole count and Tweedie (power 1.5) for any other non-negative rate; L2 otherwise. Run
  the other fit too (`--objective l2`), as LEAK-41 decides on the worse. A flagged feature is judged by its timing
  (LEAK-41): one known at the quote stays (USE-6), even when its weight-mediated share is high through risk selection.
  On a split tagged `ForcedGroupedFromTemporal` or `ForcedIIDFromTemporal` the default run ends with probe 23
  (leak_checks.md, "Probe 23"; `curation_probes.leak.period_outcome` and `shared_units`), and `--forced-split` runs it
  alone: the period-outcome test on the period column it finds or `--time-on` names (it says so when there is none), and
  the shared-unit test on the group column and the exact profiles, with regularised LightGBM fits on `--forced-splits`
  splits (default 9) x `--seeds` seeds, about one to one and a half minutes on 87,000 to 354,000 rows.
* `task_probes.py`: dummy baselines against three untuned model families (a fourth on more than 1,000 inputs:
  `selected_linear`, the linear model on the 500 inputs a univariate F-test picks on each train side), on every shipped
  split up to 30 for a dataset of at most 5,000 scored units and the first 5 otherwise, scored per group for a
  group-unit task with `mean`, `any` or `last`; the best single feature chosen per split; the flags `no_signal`,
  `solved`, `no_spread`, `one_feature`, `drift_baseline`, `unstable`, `few_minority`. Each train and test side is capped
  at `--max-rows` (default 200,000): a temporal task's train side keeps its newest rows, any other side random rows; the
  dummy uses the whole train side. Raise the cap when a dataset needs it and compute allows (Lennart, 2026-10-21: "feel
  free to raise the row cap maybe as needed and as we have compute"). With `--out` it writes one JSON per dataset
  (per-split skill and dummy loss included) and `summary.md`.
* `group_probes.py`, for a grouped task: the IID against grouped gap, several model families scored per group, and a
  permutation test across groups.
* `hidden_groups.py`, for an IID task: entity-like columns (categorical, text and numeric, floats included), composite
  keys (all columns but one), near-copy clusters and an exact key on each normalised text column (`(text: <column>)`),
  each with how much a random split gains over a split by them; for a temporal task the share of test rows whose
  entity is on the training side. When no row has 10 informative columns the near-copy line reads `not run`: no
  evidence either way, not 0%.
* `generated_probes.py`: the four marks of generated data (`formula`, `rule_leaves`, `independent_columns`,
  `uniform_within_class`).
* `dtype_probes.py`: is each column typed by its meaning (CLEAN-14), on the frame the split step leaves. It reads the
  source's codebook from the definition's first UCI or OpenML link (types and descriptions, matched by column name) and
  flags, strongest first: a categorical column the codebook or the name calls a count or an amount (`quantity_words`),
  one of numbers the codebook types as numeric (`codebook_numeric`), a numeric column the codebook types as categorical
  (`codebook_categorical`), an unordered category whose levels look like a scale (`ordinal_like`: bands, ranges, open
  ends, scale words, or a codebook that says ordinal, grade or stage), a level with an open end (`open_end`: `<1`,
  `>20`, `3+`, `50plus`, `gt8`, or a codebook's "three and more"; named also on an ordered category, so the open end
  stays visible), a categorical column whose levels look like a count (`count_like`: 0 or 1 upwards, the first ten all
  there, rarer as they grow), a numeric column named as a code (`code_name`), and any other categorical column of
  numbers (`numeric_levels`, mostly codes). An ordered category raises no flag but `open_end`. The few levels that are
  no number in a column of numbers are listed: often proxy missing codes (`.b`, `-3`) that made a count categorical
  (CLEAN-10). UCI types coded answers as `Integer` too, and names often differ from the codebook's (the output says how
  many matched): read the codebook where they do. A flag is a question; the meaning decides.
* `tuned_results.py`: the per-fold BeyondArena results of tuned and default methods cached under
  `~/.cache/tabarena/artifacts/` (`methods/<method>/results/hpo_results.parquet`), set against a dummy on the same
  splits of the shipped container; `--feature auto` adds the raw-feature test of TP-4. The runs used the shipped
  format-1 containers: say so when the v2 definition changed the split, the columns or the scoring.
* `check_collection_bundles.py [--collection BeyondArena] [--json PATH]`: the bundle checks over every container of a
  registered collection, for the v1 collections ([DATA_FOUNDRY_V1.md](../../../../DATA_FOUNDRY_V1.md)).

A sweep over the working copy (`--all`, for example after a rebuild) writes its output to a scratch folder, never into
git; the rebuild runs it ([rebuild.md](rebuild.md), step 6).

## Checks only Data Foundry has

* Record pointer: the record's `v2_path` names this dataset's `dataset.py` (a `_1m` folder only when its class declares
  `version_of` the record), and its `README.md` carries the UUID once built (`build.uuid`, `build_stale` false).
  `.venv/bin/python -m data_foundry.curation.cli sync-notebooks --check` is clean ([records.md](records.md)).
* Template conformance: the class validates on import (`dataset list --root datasets/_dev/tabarena-v0pt2` lists it),
  follows the current `datasets/_template/dataset.py`, keeps diagnostics out of `dataset.py`, and `README.md` was
  regenerated after the last edit. Report each drift as a concrete edit.
* The README in step with the code: `dataset check` leaves no diff in the committed README beyond what the change
  explains.
* A definition that moves or is superseded (a `_1m` version replaces the full run, a folder is renamed) updates the
  record's `v2_path` in the same change; a stale pointer fails `tests/test_records_integrity.py`.
