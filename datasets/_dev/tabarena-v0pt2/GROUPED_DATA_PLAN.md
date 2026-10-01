# Grouped data: design plan

Status on 2026-10-01: revised after the dataset review and implemented (the metadata, the checks, the probes
script, the 17 grouped definitions, the docs); section 9 records what was cut or deferred in the revision, section 10
the open decision the implementation found. Data-foundry owns the metadata and the checks; how TabArena turns the metadata into a score
is TabArena's choice, and section 4 is our recommendation for it. The harness changes are tracked in
[`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).

## 1. Why

A grouped task keeps all rows of a group (patient, molecule, customer, ...) on one side of a split, so the benchmark
measures prediction for unseen groups. To use such a task correctly from curation to the leaderboard, three things
must be known per dataset, and until now none of them was stored:

* what one real-world prediction is: a row, or a whole group;
* for a group: how its rows' predictions combine into one (and how its label follows from its rows);
* what is known about a new group when predicting: nothing beyond the row, all of its rows, or only its earlier rows.

The metadata had `group_on`, `group_labels` (`per_group`: one label per group; `per_sample`: labels may differ within
a group) and `group_time_on` (an order inside each group, not used for splitting). TabArena scores every row on its
own, unweighted; the group column stays a model feature in some pipelines; dataset-specific metrics fall back to the
defaults (details in `BENCHMARK_CHANGES_TODO.md`).

## 2. What we found

### 2.1 The use cases decide the unit

The review covered the 19 datasets that were grouped on 2026-10-01; 17 remain grouped (covertype is IID now,
mice_protein is retired). `labels` is not the unit: micro_mass and pancreatic have one label per group, yet their use
case predicts each measurement. Every row below is backed by the original paper, challenge or data page; the
`definition` text of each dataset cites it.

| Dataset | One group is | Use case (source) | `prediction_unit` | `aggregation` | `context` |
|---|---|---|---|---|---|
| musk | molecule | is a new molecule a musk (Dietterich et al. 1997) | group | any | all_rows |
| parkinsons_biomedical_voice_measurements | subject | diagnose a person from about 6 phonations (Little et al. 2009) | group | mean | all_rows |
| amex_non_iid_1m | customer | one default prediction per customer from its statements, labelled after the latest one (Kaggle) | group | last | all_rows |
| sat11_hand_algo_runtime | SAT instance | pick the fastest algorithm per instance (ASlib) | group | select_min | all_rows |
| micro_mass | strain | identify the species from one spectrum (Mahé et al. 2014) | row | | none |
| pancreatic_cancer_mouse_detection | mouse | one serum test per bleed (Hingorani et al. 2003) | row | | none |
| sepsis_prediction_1m | patient | an hourly warning from that hour's measurements (snapshot, decided 2026-10-01; the PhysioNet 2019 utility per patient is the metric) | row | | none |
| telemonitoring_parkinsons_biomedical_voice_measurements | subject | a test day's UPDRS from one of its phonations, for a subject not seen in training (Tsanas et al. 2010 split at random) | row | | none |
| electric_motor_temperature_prediction | measurement session | real-time temperature estimate (its smoothed features use past inputs only) | row | | none |
| cardiotocography | patient (from file names) | classify each CTG segment | row | | none |
| dementia_prediction | subject | the clinical dementia rating of a visit, for a new subject (OASIS-2) | row | | none |
| asp_potassco_classification | problem class | pick a solver configuration for an instance of an unseen problem class (claspfolio 2 split at random) | row | | none |
| 5g_energy_consumption | base station | energy per station-hour for new stations (ITU challenge) | row | | none |
| early_learning_predictors | facility | a child's outcome at a facility not seen in training (Zindi) | row | | none |
| emscad | poster | flag a job ad when it is published (Vidros et al. 2017) | row | | none |
| in_vehicle_coupon_recommendation | respondent | does a new user accept this coupon (Wang et al. 2017) | row | | none |
| video_transcoding_time_prediction | video | transcoding time for unseen videos (Deneke et al. 2014) | row | | none |

### 2.2 What the data says

* Every dataset scores clearly worse under grouped than under IID splits (untuned LightGBM, 16 datasets; musk AUC
  0.9995 vs 0.81). The gap shows how much the choice matters, not which split is right; the use case decides that.
* What the data can decide: whether grouping is irrelevant (no gap, no clustering: none of the 16), whether the
  grouped design is degenerate (covertype had 3 groups, so its grouped split was three domain-shift tests), whether
  the label granularity fits the declared one, and whether there is signal across groups.
* Learnability of small grouped tasks needs several model families, scores per group and a permutation test across
  groups. One untuned LightGBM run suggested "no signal" for mice_protein, parkinsons and pancreatic; its
  probabilities are overconfident on unseen groups. parkinsons reaches AUC 0.86 per subject (32 subjects, 95% interval
  of one split 0.69-0.99), pancreatic shows a weak linear signal in our probes (AUC 0.63) and does well in BeyondArena;
  both stay. mice_protein (macro AUC 0.92 per mouse) was retired for having no predictive target, not for a lack of
  signal. The lesson is in `check-candidate/references/leak_checks.md`, §5 and §7.

## 3. Metadata (data-foundry)

### 3.1 One structure per regime

* A v2 definition declares its regime as one object: `grouping = Grouping(on=..., labels=..., time_on=...,
  definition=..., prediction_unit=..., aggregation=..., context=...)` or `temporal = Temporal(on=...,
  splits=TemporalSplits(...))`, plus `horizon=..., horizon_unit=...` only when the windows do not fix the horizon (a
  fixed-length window is the horizon); neither means IID. The rules between the fields live
  in those classes. The flat class attributes (`group_on`, `group_labels`, `group_time_on`, `time_on`,
  `temporal_splits`, `time_horizon`, `time_horizon_unit`) are no longer accepted in v2 definitions; all 37 grouped and
  temporal definitions move to the new form. v1 notebooks are unchanged.
* `Grouping` is stored in the container: `PredictiveMLTaskMetadataV2.grouping`, the task metadata of container
  format 2 (what a v2 definition builds; `container.format_version == 2`, also written to `container_metadata.json`).
  The group fields are stored once, in the block; `group_on`, `group_labels` and `group_time_on` are read-only views
  of it, so code that reads both formats keeps working. `CuratedContainer.grouping` returns the block and raises for
  a format-1 container (every shipped container), which records only the flat fields (revised 2026-10-02: the flat
  fields were first written next to the block).
* `Temporal` is not stored as a block. The container already holds all of it (`time_on` in the task metadata, the
  horizon in the splits metadata), so a block would only repeat them. It is the definition-side structure: the column, the windows and the horizon in one place.
* Storage and compatibility: the format-1 task metadata (`PredictiveMLTaskMetadata`) keeps the fields the shipped
  checksums encode, so every shipped container and every v1 container keeps its checksum and its files. A format-2
  container needs this library version to load (an older one fails on the unknown metadata type); a v0.2 collection
  needs it anyway.

### 3.2 Fields of `Grouping`

| Field | Values | Rule |
|---|---|---|
| `on` | column(s) | as `group_on` |
| `labels` | `per_group`, `per_sample` | as `group_labels`: a property of the data, checked by `task_group_labels_per_group_violated` |
| `time_on` | column or None | as `group_time_on`: the order inside a group, never used for splitting |
| `definition` | text | required in v2: what one group is, why it is held out, and the use case with its source |
| `prediction_unit` | `row` (default), `group` | from the use case (section 2.1) |
| `aggregation` | `mean`, `any`, `last`, `select_min`, `select_max` | required with `prediction_unit = group`, else unset. `mean` needs `per_group` labels; `any` a binary target; `last` a `time_on`; `select_*` a regression target with `per_sample` labels |
| `context` | `none` (default), `all_rows`, `past_rows` | what a model may use about the group at prediction time; `past_rows` needs a `time_on` |

* No weighting field. At the row unit every row counts once, at the group unit every group counts once. A source
  metric that weights otherwise is a named metric (section 4).
* The group column stays in the container (splits and scoring need it). It is metadata, never a model feature; the
  schema docstring says so, and the harness has to enforce it (`BENCHMARK_CHANGES_TODO.md`).
* The generated `README.md` shows the fields and the group statistics in a "Group structure" section, and the
  frontmatter carries the fields under `task.grouping`.

## 4. Recommended scoring (for TabArena; documentation only)

The metadata is meant to determine the official score, so every method is scored the same way. The resolution we
recommend:

| Prediction unit | Label of a group | Default group prediction | Metric computed on |
|---|---|---|---|
| `row` | | | the rows, unweighted (as today) |
| `group` + `mean` | the shared label | mean of the rows' predicted probabilities (regression: of the predictions) | one value per group |
| `group` + `any` | positive if any row is | max of the rows' P(positive) | one value per group |
| `group` + `last` | the latest row's label (`time_on`) | the latest row's prediction | one value per group |
| `group` + `select_min` / `select_max` | | the row with the lowest / highest prediction | the true value of the selected row (for example PAR10 for sat11) |

* The metric is the task's `objective_metric_name` applied at that unit: ROC AUC over molecules for musk on the max
  of each molecule's row probabilities, over subjects for parkinsons on the mean, over rows for in_vehicle.
* Named metrics that need the group structure get the group ids and the order from the metadata: the PhysioNet 2019
  utility for sepsis (each patient's ordered hours), `amex_metric` per customer, the 5G challenge's weighted MAPE,
  micro_mass's accuracy averaged per strain and then per species, PAR10 for sat11 (a timeout is a runtime of the
  5,000 s cutoff, counted 10 times). asp_potassco keeps only each instance's best configuration, so PAR10 there would
  need the 11 runtimes kept as metadata (deferred, section 9).
* Methods: the task fixes the unit and the metric. The harness applies the default aggregation when a method returns
  row predictions; a method may return one prediction per group itself (a multiple-instance model, a learned pooling,
  another rule) and is scored with the same metric on the same unit. What a method may look at follows `context`; a
  group-level override needs `all_rows`. At the row unit every row is predicted.
* Inner validation and tuning should use the same resolved metric, so a model is not tuned on rows and scored on
  groups.
* Report the number of test groups per fold next to a group-level score; it is the score's sample size.
* Until TabArena scores at the group unit, the four group-unit datasets are scored per row; the metadata says what
  the right unit is, and nothing is held back.

## 5. Checks (data-foundry)

`dataset check` computes cheap group statistics for every grouped task (`data_foundry.v2.group_checks`), shows them in
the README's "Group structure" section and turns them into findings:

| Finding | Computes | Fires when |
|---|---|---|
| `groups_test_groups_few` (warning) | test groups per fold | a fold tests on fewer than 20 groups: the score rests on few independent units |
| `groups_largest_share_high` (warning) | the largest group's share of the rows | one group holds more than 20% of the rows |
| `groups_labels_constant` (warning) | the share of groups with one label | `labels = per_sample` but at least 95% of the groups have a single label |
| `groups_not_clustered` (info) | nearest neighbour in the same group vs chance, label variance the group explains vs shuffled groups | both close to chance: the grouping may not be needed |

The model-based diagnostics are a script, like `scripts/v2/leak_probes.py`: `scripts/v2/group_probes.py <name>` runs
the IID vs grouped score gap (untuned LightGBM, with the fold spread) and the learnability test (several model
families, group-level scores, a permutation test across groups). `check-candidate/references/leak_checks.md` probe 11
and the `/verify-dataset` rubric (item 4) cite these numbers instead of computing them by hand.

The consistency of the new fields is checked when a definition is imported (`Grouping`, `Temporal`, the task
metadata), so an inconsistent declaration does not import.

## 6. Dataset review

For each of the 17 grouped datasets: declare `Grouping` with the fields of section 2.1 and a `definition` that cites
the source, fix what the research found, and accept the findings of section 5 where a decision keeps the dataset.

| Dataset | Found |
|---|---|
| parkinsons_biomedical_voice_measurements | done 2026-10-01: BibTeX Little et al. 2009 and 2007; `group_time_on = session_number` stays (it counts up within a subject). Still open: the data has 32 subjects (24 with PD), the paper 31 (23) |
| telemonitoring_parkinsons_biomedical_voice_measurements | done 2026-10-01: source link UCI 189, year 2009, the test days nearest the clinic assessments, BibTeX Tsanas et al. 2010. The definition notes that the unseen-subject split is stricter than the source's random split. Open: no signal across subjects (section 10) |
| pancreatic_cancer_mouse_detection | done 2026-10-01: counts against the paper, target `HasPanIN`, record binary, the file-name class code. Still open: the `t` suffix, and whether 999 in two m/z columns is a cap |
| sepsis_prediction_1m | done 2026-10-01: the snapshot use case (each hour from its own row, utility per patient) |
| cardiotocography | done 2026-10-01: the comment explains why the rows of an exam file stay together and what the file-name patient key can and cannot leak |
| dementia_prediction | done 2026-10-01: the comment lists every kept feature; record grouped and multiclass. The definition notes the first-visit framing |
| sat11_hand_algo_runtime | done 2026-10-01: SAT11-HAND-ALGO link; the 112 instances no algorithm solves are dropped, the other timeouts stay at the cutoff (censored); split by instance |
| asp_potassco_classification | done 2026-10-01: record multiclass, with the source's random split and our choice of unseen problem classes. The definition comment no longer calls the instances of a class "differing only in seed or task configurations" |
| in_vehicle_coupon_recommendation | the definition said "the paper's 5-fold results are random splits", which the paper does not state; reworded |
| parkinsons_biomedical_voice_measurements (checks) | `groups_test_groups_few` (10-11 test subjects per fold) accepted with the evidence: per-subject ROC AUC 0.82 (logistic regression), permutation test across subjects p = 0.01 (`group_probes.py`); `task_group_time_on_few_unique` accepted (`session_number` orders a subject's recordings) |
| emscad (checks) | `groups_labels_constant`: 4,439 of 4,441 posters have one label (assigned per client), 2 posters (34 ads) have both, so the labels stay `per_sample`; accepted with these counts |
| musk, micro_mass, amex_non_iid_1m, electric_motor_temperature_prediction, 5g_energy_consumption, early_learning_predictors, video_transcoding_time_prediction | consistent with the source; declared the fields. No group finding |
| covertype | done 2026-10-01: IID on the full data (7 cover types, 4 areas) |
| mice_protein_trisomy_discriminant | retired 2026-10-01: no predictive target |

## 7. Docs and skills

* Curation guidelines (`triage-candidates/references/curation_guidelines.md` and the dashboard's `guidelines.html`):
  a grouped split simulates prediction for unseen entities; with few groups it is a domain-shift test; unit,
  aggregation and context come from the use case, with a citation.
* `add-dataset`: how to declare `Grouping` and `Temporal`, with examples (`references/dataset_patterns.md`, the
  template `datasets/_template/v2/dataset.py`, `scripts/v2/migrate_notebook_to_v2.py`).
* `/verify-dataset` rubric item 4 and `leak_checks.md` probe 11: the "Group structure" section and
  `scripts/v2/group_probes.py`.
* The schema docstrings and the examples (`load_curated_container.py`, `benchmark_on_beyond_arena.py`): the fields,
  `CuratedContainer.grouping`, and the group column kept out of the features.

## 8. Decisions

* 2026-10-01, in the review: covertype IID on the full data; sat11 stays grouped by instance (its instances also
  come in families); mice_protein retired; sepsis is a snapshot task; the tiny tasks stay.
* 2026-10-01, in the revision: emscad is predicted per ad (the source's unit), not per poster; the group-unit datasets
  keep row scoring until TabArena scores per group, without being held back (section 4).

## 9. Cut or deferred in the revision

* The temporal regime gets a definition-side structure but no stored block (section 3.1).
* No model-based checks inside `dataset check`: they are slow and seeded runs would still make the README depend on
  them; `scripts/v2/group_probes.py` runs them on demand.
* Dropped: a domain-shift check that trains a model to separate a held-out group. Its motivating case (covertype, 3
  groups) is gone, and few groups are already flagged (`task_group_count_low`, `groups_test_groups_few`).
* Deferred to `TODO.md`: a check for hidden groups in IID tasks (id-like columns that repeat with clustered labels;
  it needs a pass over all 114 IID datasets to calibrate and review), the 11 configuration runtimes of asp_potassco as
  metadata for PAR10, and splitting sat11 by instance family.

## 10. Open decision from the implementation

* telemonitoring_parkinsons_biomedical_voice_measurements has no signal across subjects. On the shipped grouped
  splits every model scores below the mean predictor (R^2 -0.17 ridge to -0.31 kNN, 3 repeats), while a random split
  of the same rows gives R^2 0.75 (`group_probes.py`, 2026-10-01). The source tracks enrolled patients and rejected a
  subject-wise validation ("there is not enough hold-out data", Tsanas et al. 2010). Options: retire it, or recast it
  as warm-start tracking (a subject's baseline visit in training, its later test days in test), which the current
  split protocol cannot express without a custom `_make_splits`. `groups_test_groups_few` (14 test subjects per fold)
  stays unaccepted until then.
