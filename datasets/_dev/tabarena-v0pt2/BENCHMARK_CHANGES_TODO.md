# Benchmark changes to do (TabArena side)

Changes the benchmark harness (`tabarena/`) needs so that the v0.2 datasets are used as they are curated. They came
out of the review of grouped data on 2026-10-01 (counts and file references are from that day). The data-foundry
side (metadata, checks, the dataset review) is tracked in [`TODO.md`](TODO.md).

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
  and one score per group, so each group counts once. The rules the sources need: `mean` (replicate measurements:
  parkinsons), `any` / max (multiple-instance: musk, a molecule is a musk if any conformation is),
  `last` (the latest row decides: amex, scored per customer at the latest statement) and `select_min` (algorithm
  selection: sat11 picks the algorithm with the lowest predicted runtime per instance and is scored by that
  algorithm's true runtime, e.g. PAR10 or the share of the single-best to virtual-best gap closed). The metadata is
  `task_metadata.grouping` (`data_foundry.schema.Grouping`: `prediction_unit`, `aggregation`, `context`,
  `definition`) of a format-2 container (`container.format_version == 2`), read with `CuratedContainer.grouping`. A
  format-1 container (the shipped BeyondArena ones) has no grouping and is scored per row.
  The v0.2 group-unit datasets: musk (`any`), parkinsons_biomedical_voice_measurements (`mean`), amex_non_iid_1m
  (`last`, by `S_2`), sat11_hand_algo_runtime (`select_min`). How it becomes a scoring spec is TabArena's choice; our
  recommendation (resolution table, named metrics, methods that return their own group predictions, tuning on the
  same metric) is in [`GROUPED_DATA_PLAN.md`](GROUPED_DATA_PLAN.md), section 4.
- [ ] **Use the information about a group that the use case allows.** The group aggregation features are built for
  every `per_group` task, from all rows of a test group. That fits a task where all rows of a new group are known at
  prediction time; a task that may only use earlier rows of a group (`group_time_on`) needs causal aggregates, and a
  task whose rows stand alone (sepsis: each hour from its own measurements) none. The field is `grouping.context`
  (`none`, `all_rows`, `past_rows`); `all_rows` in v0.2: musk, parkinsons_biomedical_voice_measurements,
  amex_non_iid_1m, sat11_hand_algo_runtime.
- [ ] **Dataset-specific metrics.** The adapter replaces any metric other than `roc_auc`, `log_loss` and `rmse` with
  the problem type's default without a warning: `sepsis_prediction_1m`'s PhysioNet 2019 utility (scored per patient),
  `amex_non_iid_1m`'s `amex_metric` and `5g_energy_consumption`'s `mape` are never used. Support them, or warn and
  document the fallback per dataset. Metrics the sources use that need group information: the PhysioNet 2019
  utility (per patient over its ordered hours, needs `Patient_ID` and `Hour` and every hour of a test patient),
  the 5G challenge's weighted MAPE (higher weight for new base stations), micro_mass's accuracy averaged per strain
  and then per species, and PAR10 for sat11 (asp_potassco keeps only each instance's best configuration, so it would
  need its runtimes kept as metadata first).
- [ ] **Report the effective sample size.** For a task scored per group, the number of test groups per fold is the
  sample size of the score (32 patients in `parkinsons_biomedical_voice_measurements`); show it next to the results.

## Library version

- [ ] **Require the data-foundry release that carries the v0.2 metadata.** v0.2 containers store
  `split_random_state` (and `grouping` for grouped tasks); releases up to v0.0.5 forbid unknown fields and cannot load
  them. Release data-foundry before uploading the rebuilt containers and raise TabArena's `data-foundry>=0.0.3` floor.
  From this version on, `CuratedContainer.load` ignores fields it does not know, with a warning.

## Frame sizes of the v2 split protocol

- [ ] **Temporal `_1m` versions ship up to 2.5M rows** (each split still trains on at most 1M and tests on at most
  500k rows): check storage and loading for `cooking_time_1m`, `delivery_eta_1m` and `maps_router_eta_1m` (2.5M rows,
  989 float columns for maps).
