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
it mints a new UUID, and a build is the curator's call (or an explicit ask).

## The probes

The probe methods are the general library in
[`../../knowledge-curation/scripts/`](../../knowledge-curation/scripts/); the command-line entry points here, in
[`../scripts/`](../scripts/), load a Data Foundry dataset (its definition, or with `--built` the built container named
in the README's build record) through `dataset_io.py` and call it. The probes use the shipped target and splits; when
the definition changed the target, run the same checks on the source's labels in `explore.ipynb`.

```bash
K=.claude/skills/knowledge-data-foundry/scripts
.venv/bin/python $K/leak_probes.py <unique_name> [--splits 3] [--max-rows 50000] [--max-single-features 300] [--n-jobs 8] [--out DIR]
.venv/bin/python $K/task_probes.py <unique_name> [--built] [--splits N] [--no-text] [--out DIR]   # or --all --jobs 8
.venv/bin/python $K/group_probes.py <unique_name> [--repeats 3] [--permutations 100]
.venv/bin/python $K/hidden_groups.py <unique_name> [--built] [--include-grouped] [--out DIR]     # or --all
.venv/bin/python $K/generated_probes.py <unique_name> [--built] [--out DIR]                     # or --all
.venv/bin/python $K/tuned_results.py <unique_name> [--feature auto]
```

* `leak_probes.py`: probes 1-6 and 14 of the leak table (all features, each feature alone, missing indicators, drop
  one, exact copies across the split with and without string and datetime columns, each long string column alone as
  text (TF-IDF + SVD on the train side, character n-grams for one-token strings), nearest-neighbour agreement and the
  label-free distance score, a depth-2 and depth-3 tree on the label), with untuned LightGBM on the first shipped
  splits. With more columns than `--max-single-features` only the most informative enter the single-feature fits, and
  the output says how many were screened out, so a 49,000-column omics table takes minutes. A multiclass ROC AUC is the
  mean over the classes present in the test fold. Group columns are never features.
* `task_probes.py`: dummy baselines against three untuned model families (a fourth on more than 1,000 inputs:
  `selected_linear`, the linear model on the 500 inputs a univariate F-test picks on each train side), on every
  shipped split up to 30 for a dataset of at most 5,000 scored units and the first 5 otherwise, scored per group for a
  group-unit task with `mean`, `any` or `last`; the best single feature chosen per split; the flags `no_signal`,
  `solved`, `no_spread`, `one_feature`, `drift_baseline`, `unstable`, `few_minority`. With `--out` it writes one JSON
  per dataset (per-split skill and dummy loss included) and `summary.md`.
* `group_probes.py`, for a grouped task: the IID against grouped gap, several model families scored per group, and a
  permutation test across groups.
* `hidden_groups.py`, for an IID task: entity-like columns, composite keys (all columns but one) and near-copy
  clusters, each with how much a random split gains over a split by them; for a temporal task the share of test rows
  whose entity is on the training side.
* `generated_probes.py`: the four marks of generated data (`formula`, `rule_leaves`, `independent_columns`,
  `uniform_within_class`).
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
