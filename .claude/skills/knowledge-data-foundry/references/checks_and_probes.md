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

runs the whole pipeline, the data checks, the bundle checks (`data_foundry.checks`, judged by the v2 split
protocol for a format-2 container, `data_foundry.checks.protocol`), the checks that need the definition class
(`data_foundry.definition.checks`) and `_decisions`, without saving (no UUID), and rewrites the folder's `README.md`.
Compare the README with the committed one: an unexpected diff (checksum, split sizes, new findings) means the
definition drifted from its evidence. Then:

* every error blocks a PR;
* for every warning, say whether it is a real problem for this dataset or correct as it is; a warning the curator
  accepts goes into `accepted_check_warnings` with the reason (propose the exact edit); an error cannot be accepted,
  except the ones [check_slugs.md](check_slugs.md) lists with the rule that allows it;
* do not restate passing checks: "Bundle checks: 0 errors, 3 warnings (2 accepted)" is the right level.

The slug-by-slug actions are in [definitions.md](definitions.md), "Bundle checks"; every slug with its severity and
whether it may be accepted is in [check_slugs.md](check_slugs.md). Never run `dataset build` to verify:
it mints a new UUID, and a build is the curator's call (or an explicit ask). A task with a training weight has its own
checks (`task_sample_weight_not_metric_weight`, `task_weight_invalid`, `task_rate_count_not_whole`), and two warnings
say a weight may be missing (`task_metric_weight_without_sample_weight`, `task_feature_looks_like_exposure`):
[definition_fields.md](definition_fields.md), `sample_weight`. A unit weight (MET-17) has two
(`task_unit_weight_not_one_per_unit`, `task_unit_weight_unit_split`): [definition_fields.md](definition_fields.md),
`unit_weight`.

## The probes

The probes are in the package, `data_foundry.probes` (the `probes` extra: `pip install -e ".[probes]"`), and run as one
command, `data-foundry probe <probe> NAME...` (the same as `.venv/bin/python -m data_foundry.curation.cli probe`). It
loads a Data Foundry dataset (its definition, or with `--built` the built container named in the README's build record,
else a registered collection's copy) through `data_foundry.probes.inputs`, whose X is always the model inputs
(`feature_columns`: never the target, group, scoring or unit columns, nor a time column that dates the label). The
probes use the shipped target and splits; when the definition changed the target, run the same checks on the source's
labels in a scratch notebook (`ds = workbench()`). A special feature (`special_features`) enters every probe in its
recommended encoding (`encode_special_feature`), as a benchmark would give it to a model: a SMILES as RDKit's 2D
descriptors, the MACCS keys and the ECFP4 counts, a spectrum as its columns with the encoded values; the blind
reviewer's clean room keeps the values as shipped. The bundle check `dataset_special_feature` finds each feature's
columns and runs its kind's checks: `dataset_smiles_column` parses every SMILES with the pinned RDKit,
`dataset_spectrum` checks that a spectrum's columns are numeric and finite and warns about missing intensities.

A task with a training weight (`sample_weight`) is probed with it: the loader fills `ProbeInput.weights` from it, and
the task, leak and group probes fit every model with the weight and take the weighted dummy (sum of target x weight
over the sum of the weights: the portfolio rate); their R^2, RMSE, ROC AUC and log loss are weighted. The task probe
and probe 22 also score the declared metric, and the task probe reports the share of each family's predictions at the
metric's floor (`min_prediction`, MET-13).

Every probe takes the same options: the datasets (`NAME...`, or `--all` for every definition under `--root`, the
working copy by default), `--built`, `--jobs` (datasets in parallel, default 1), `--n-jobs` (threads per model,
default 8) and `--out DIR` (one JSON per dataset and `summary.md`). Each probe's own options follow its name
(`data-foundry probe task --help`):

| Command | What it asks | Its own options (defaults) |
|---|---|---|
| `data-foundry probe leak NAME` | probes 1-6, 10, 13, 14 and 17-23 of the leak table (no `--built`) | `--splits 3`, `--max-rows 50000`, `--max-single-features 300`; probe 13: `--time-on`, `--period D\|W\|M\|Q\|Y`, `--tz`, `--positive`, `--tail` |
| `... probe leak NAME --period-only` | probe 13 alone, without a model | as above |
| `... probe leak NAME --raw` | the raw state alone (probes 10, 18-21) | `--splits`, `--max-rows` |
| `... probe leak NAME --weight-proxy` | probe 22 alone: do the features carry the weight? | `--weight-column`, `--objective metric\|l2\|OBJ`, `--seeds 3`, `--splits`, `--max-rows` |
| `... probe leak NAME --forced-split` | probe 23 alone: the leak tests of a forced split | `--time-on`, `--period`, `--objective`, `--seeds 3`, `--forced-splits 9`, `--max-rows` |
| `... probe leak NAME --stationary-relation` | the stationary-relation test (SPLIT-32) | `--time-on`, `--period`, `--unordered`, `--unit COLUMN\|none`, `--exclude`, `--windows 3`, `--test-period`, `--stationary-seeds 5`, `--max-test`, `--foundation none\|tabpfn\|kumo`, `--device`, `--threads`, `--max-foundation-train 20000`, `--max-foundation-test 5000` |
| `data-foundry probe task NAME` | is the task empty, solved, or the same for every model? (TP) | `--splits` (up to 30 for small data, else 5), `--max-rows 200000`, `--no-text` |
| `data-foundry probe group NAME` | for a grouped task: does the grouping matter, is there signal across groups? | `--repeats 3`, `--permutations 100`, `--max-rows 200000` |
| `data-foundry probe hidden-groups NAME` | columns, keys, near copies and texts that act as an entity | `--include-grouped` |
| `data-foundry probe time NAME` | does a split that is not temporal keep a time order? (SPLIT-32) | `--include-temporal` |
| `data-foundry probe dtypes NAME` | is each column typed by its meaning? (CLEAN-14) | `--codebook URL`, `--no-fetch` |
| `data-foundry probe generated NAME` | is the target a formula or a rule set? (PROV-3) | |
| `.venv/bin/python .claude/skills/knowledge-data-foundry/scripts/tuned_results.py NAME` | what tuned methods score on the shipped splits | `--feature auto` |

A sweep of the working copy runs with `--all --jobs 8` (the task probe: about 2-3 hours, at most about 13 GB a job).
A dataset that fails is reported and the others run on; the exit code is then 1.

* `probe leak`: probes 1-6, 10, 13, 14 and 17-23 of the leak table (all features, each feature alone, missing
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
  curated row to its raw row (`process(lineage=True)`, `inputs.from_definition(ds, raw=True)`) and says when it cannot.
  `--weight-proxy` runs probe 22 alone (leak_checks.md, "Probe 22"; `data_foundry.probes.leak.weight_proxy`) on the
  task's sample weight, or the column `--weight-column` names: a cross-fitted LightGBM of the weight on the features
  (R^2, Spearman, top features), the declared weighted metric with the weight added as a feature against the honest fit,
  each top feature's weight-mediated gain with its SD over folds and seeds, and the weight alone: 1/weight as the
  prediction for a Gini, a fit of the target on the weight (the same objective and training weight) for any other
  metric, next to the weighted constant. `--objective metric` (the default) fits the weighted actuarial model: a
  deviance's own (Poisson or Tweedie); under any other metric (a Gini) a rate with a training weight gets Poisson when
  the rate times the weight is a whole count and Tweedie (power 1.5) for any other non-negative rate; L2 otherwise. Run
  the other fit too (`--objective l2`), as LEAK-41 decides on the worse. A flagged feature is judged by its timing
  (LEAK-41): one known at the quote stays (USE-6), even when its weight-mediated share is high through risk selection.
  On a split tagged `ForcedGroupedFromTemporal`, `ForcedIIDFromTemporal` or `AssumedStationaryRelation` (which replaces
  a forced tag) the default run ends with probe 23 (leak_checks.md, "Probe 23";
  `data_foundry.probes.leak.period_outcome` and `shared_units`), and `--forced-split` runs it alone: the period-outcome
  test on the period column it finds or `--time-on` names (it says so when there is none), and the shared-unit test on
  the group column and the exact profiles, with regularised LightGBM fits on `--forced-splits` splits (default 9) x
  `--seeds` seeds, about one to one and a half minutes on 87,000 to 354,000 rows. `--stationary-relation` runs the
  stationary-relation test alone (below, "The stationary-relation test").
* `probe task`: dummy baselines against three untuned model families (a fourth on more than 1,000 inputs:
  `selected_linear`, the linear model on the 500 inputs a univariate F-test picks on each train side), on every shipped
  split up to 30 for a dataset of at most 5,000 scored units and the first 5 otherwise, scored per group for a
  group-unit task with `mean`, `any` or `last`; the best single feature chosen per split; the flags `no_signal`,
  `solved`, `no_spread`, `one_feature`, `drift_baseline`, `unstable`, `few_minority`. Each train and test side is capped
  at `--max-rows` (default 200,000): a temporal task's train side keeps its newest rows, any other side random rows; the
  dummy uses the whole train side. Raise the cap when a dataset needs it and compute allows (Lennart, 2026-10-21: "feel
  free to raise the row cap maybe as needed and as we have compute"). With `--out` it writes one JSON per dataset
  (per-split skill and dummy loss included) and `summary.md`.
* `probe group`, for a grouped task: the IID against grouped gap, the task probe's model families and kNN scored per
  group, and a permutation test across groups. A task without a grouping is skipped.
* `probe hidden-groups`, for an IID task: entity-like columns (categorical, text and numeric, floats included),
  composite keys (all columns but one), near-copy clusters and an exact key on each normalised text column
  (`(text: <column>)`), each with how much a random split gains over a split by them; for a temporal task the share of
  test rows whose entity is on the training side. When no row has 10 informative columns the near-copy line reads
  `not run`: no evidence either way, not 0%.
* `probe generated`: the four marks of generated data (`formula`, `rule_leaves`, `independent_columns`,
  `uniform_within_class`).
* `probe dtypes`: is each column typed by its meaning (CLEAN-14), on the frame the split step leaves. It reads the
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
* `probe time`, for a split that is not temporal (SPLIT-32, question 3): does the data still carry a time order?
  It is model-free and fast. It lists the columns that look like time (a date dtype, a time word in the name such as
  date, year, month, week, season, period, wave or cohort, or whole numbers between 1900 and 2100 only; names that say
  a duration or an age are left out, and so are fractional numbers outside 1900-2100 and numbers named with `dt`, a
  delta t such as `edge_dt`), the raw columns of that kind the definition drops, the target along the raw row
  order and along each ID-like column (whole numbers, nearly one per row, named like an ID or following the row order;
  an ID the definition dropped is read through the rows' raw positions), and few-valued columns that move together and
  encode a period (yearly unemployment, inflation and GDP; at least 50 rows per period). Along the raw order it also
  looks for rows that repeat one block later (company-years stored year block by year block: in windows of 500 rows,
  a lag whose rows are very close, below the 1st percentile of random pairs, far more often than at the lags around
  it), runs of one entity in consecutive rows (a counter such as an admission number that goes up by 1 while fixed
  fields such as age and sex repeat, and the share of each class on a run's last row), and, in a file sorted by class,
  features that drift along a class's rows (the class block is several pieces: sources or periods; not when one
  feature sorts the block). Flags: `time_column`, `time_dropped`, `order_drift`, `id_drift`, `period_values`,
  `periodic_blocks`, `entity_runs`, `class_block_drift`, and `sorted_by_target` for an order that follows the target in
  blocks (a file sorted by class), which is how the file was put together, not a clock, unless `class_block_drift`
  says the blocks are pieces. A flag that is not explained away is a sign that the data carries time: information for
  the split, which it does not decide. `--root` names the definitions; the raw files come from the local warehouse
  (`$DATA_FOUNDRY_WAREHOUSE`). `--built` reads the README's build from the local warehouse, else a collection's copy
  from the cache (`~/.cache/data_foundry/<collection>/`, `$DATA_FOUNDRY_CACHE`); a container's rows were shuffled, so
  the dropped columns and every check of the row order are left out, and the output says so.
* `tuned_results.py`: the per-fold BeyondArena results of tuned and default methods cached under
  `~/.cache/tabarena/artifacts/` (`methods/<method>/results/hpo_results.parquet`), set against a dummy on the same
  splits of the shipped container; `--feature auto` adds the raw-feature test of TP-4. The runs used the shipped
  format-1 containers: say so when the v2 definition changed the split, the columns or the scoring.
* `check_collection_bundles.py [--collection BeyondArena] [--json PATH]`: the bundle checks over every container of a
  registered collection, for the v1 collections ([DATA_FOUNDRY_V1.md](../../../../DATA_FOUNDRY_V1.md)).

### The stationary-relation test

SPLIT-32 lets a forward use case without usable windows keep a random split, or one grouped by the unit, as
`StationaryRelation` only when the target and its relation to the features are measured flat across the periods the data
holds. `data-foundry probe leak <unique_name> --stationary-relation` measures it, the same way for every dataset
(`data_foundry.probes.stationarity`):

* **Periods:** the period column probe 13 finds or `--time-on` names, cut by `--period`. The windows are the newest
  `--windows` periods (default 3) with at least 40 rows and 40 rows before them, whatever their training share
  (SPLIT-14's floor is for a split's windows, not for this test); with `--unordered` (periods without an order, such as
  month classes) every period is a window and the other periods stand in for the rows before it. Columns that name the
  period (the period column, `--exclude`) are left out of the features. A run on fewer than the newest three
  (`--test-period`, one job per window, or fewer `--windows`) reports `verdict: partial` with its own reading;
  `data_foundry.probes.stationarity.combine_runs` joins the jobs' JSON results into the verdict.
* **Test half:** per seed, a random half of the window's rows; where a unit recurs and the use case meets new units
  (`--unit`, default the definition's group column; `none` for rows), whole units are drawn, and the test half's units
  leave every training side.
* **Two models, scored on the same test half:** a forward model trained on every row before the window, and a
  contemporaneous model trained on as many rows: the window's whole other half, filled up by a random draw from the rows
  before it. A constant predictor (the forward side's weighted mean or class shares) is scored beside them.
* **Models:** probe 23's regularised LightGBM with the task's objective and training weight, on all rows; and one
  state-of-the-art tabular foundation model, on at most `--max-foundation-train` (20,000) training and
  `--max-foundation-test` (5,000) test rows drawn by the same rules: TabPFN v3.5 (`--foundation tabpfn`; the public
  `tabpfn` package with the public Hugging Face weights, categories as codes named categorical) or NVIDIA's
  Kumo-Tabular (`--foundation kumo`; the optional package `structured-data-models`, large, 8 estimators, the mean of its
  quantiles as the point for squared-error metrics, the median for absolute-error ones). Both models are scored by the
  task's metric, the training weight included. A time basis quotes the two and names the foundation model.
* **Seeds:** `--stationary-seeds` (5); each draws the test half, the contemporaneous fill and the models' seeds anew.
* **Gap and floor:** the gap is how much worse the forward model scores than the contemporaneous one (positive when
  worse, whatever the metric's direction), its mean and SD over the seeds; the floor is 1% of the distance between the
  contemporaneous model and the constant predictor.

The verdict:

* **Per window and model:** not flat when the mean gap exceeds both 2 SD and the floor; flat when it does not, the
  contemporaneous model beats the constant, and 2 SD is at most ten floors (the test could have shown a gap of a few
  floors); inconclusive otherwise, which includes a model without skill.
* **Pooled:** the gap averaged over the windows (its SD: the root of the windows' summed variances, divided by their
  number), read like a window, so a small dataset gets the evidence of all its windows, both ways.
* **The relation:** not flat when one window or the pooled gap is not flat for one model, or when, for classification,
  a class share changes by a factor of 2 or more between two periods at chi-square p < 0.01 (a change in recording,
  SPLIT-32); flat when, for a model that beats the constant in every window, the pooled gap is flat; inconclusive
  otherwise. A target rate that moves less is reported, not counted. With no window, the test says `not measurable`.

A flat relation lets a person set `StationaryRelation`: the AI offers it with the reading, and the definition's `Time
basis:` line, which opens `StationaryRelation (<person>, <YYYY-MM-DD>):`, quotes the windows' gaps against their floors;
not flat leaves the forced tag; inconclusive counts as unmeasured, so the forced tag stays unless a person gives
`AssumedStationaryRelation` a reason (SPLIT-32). The run prints one line per window and model and, with `--out`, writes
the result as JSON. Run the foundation model on a GPU node started through SkyPilot (the `skypilot` skill): TabPFN
v3.5 refuses a CPU, and Kumo-Tabular is slow there (on 48 cores, about 50 s per fit on 2,000 training rows and 270 s on
20,000; `--device cuda`).

A sweep over the working copy (`--all`, for example after a rebuild) writes its output to a scratch folder, never into
git; the rebuild runs it ([rebuild.md](rebuild.md), step 6).

## Checks only Data Foundry has

* Record pointer: the record's `v2_path` names this dataset's `dataset.py` (a `<name>_1m` folder only for a version with
  a row budget), and its `README.md` carries the UUID once built (`build.uuid`, `build_stale` false).
  `.venv/bin/python -m data_foundry.curation.cli sync-notebooks --check` is clean ([records.md](records.md)).
* Template conformance: the class validates on import (`dataset list --root datasets/_dev/tabarena-v0pt2` lists it),
  follows the current `datasets/_template/dataset.py`, keeps diagnostics out of `dataset.py`, and `README.md` was
  regenerated after the last edit. Report each drift as a concrete edit.
* The README in step with the code: `dataset check` leaves no diff in the committed README beyond what the change
  explains.
* A definition that moves or is superseded (a `_1m` version replaces the full run, a folder is renamed) updates the
  record's `v2_path` in the same change; a stale pointer fails `tests/test_records_integrity.py`.
