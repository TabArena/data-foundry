# Changelog: TabArena v0.2 working copy

Every change to this folder gets an entry here, newest first: edited definitions or helper files, added or removed
datasets, and re-runs that produce a new container (give the new UUID). Say what changed and why, and link the
record, audit or PR that motivated it.

## 2026-10-06 (all 128 rebuilt: the row order comes from the rows' content)

- The base class now puts the rows in the order of their content (a stable sort by a hash of each row) before the
  shuffle or the time sort (`order_rows`, `content_order`). A container depends only on which rows `_clean` returns,
  not on the order it returns them in (a polars join, a file listing, a library version). Within a timestamp, the rows
  of a temporal task are now in content order too. `shuffle = False` keeps the order of `_clean`, as before.
- Rebuilt all 128 datasets (new UUIDs in the table of `README.md`; this supersedes the four rebuilt earlier today).
  The rows of 126 are in a new order, so their folds and checksums are new. california_house_prices_2020 and
  mercedes_benz_greener_manufacturing keep their checksums: their time column has no ties. The 120 datasets that
  are not sub-sampled hold the same rows as before. The eight sub-sampled `_1m` datasets draw their sample from the
  reordered frame, so they hold a different sample of the same size: amex_non_iid_1m 124,466 groups (was 124,481),
  sepsis_prediction_1m 38,968 (was 39,002), and other rows for climate_model_weather_forecasting_1m,
  consumer_complaints_1m, cooking_time_1m, delivery_eta_1m, home_credit_default_stability_1m and maps_router_eta_1m.
  From now on their sample no longer depends on the order of `_clean` either. Verification: all 128 built `ok`, every saved container reloads with its checksum, no new warning against
  the committed READMEs (61 open warnings in 44 datasets, as before), and the raw files read are the same. A
  check-only build under pandas 3.0.6 from a warehouse holding only the 466 traced files (71.5 GB) gives the same 128
  checksums, so the traced files suffice and pandas 3 reproduces the build. The backup of 2026-10-02 still holds every
  input (step 4 not re-run).
- Memory: the first version of the new order copied the frame twice, and the `_1m` datasets are ordered before they
  are sub-sampled, so maps_router_eta_1m peaked at 255 GB (17 minutes of wall time for the build). `order_rows` now
  computes the positions first and copies once; a check-only build with it gives the same 128 checksums, and
  maps_router_eta_1m peaks at 205 GB (172 GB before the content order).
- The task-probe sweep of this build (all 128, no errors) flags 8 datasets. Six carry flags already decided in the
  review (acquire_valued_shoppers_challenge, asp_potassco_classification, clock_protein_toxicity, forest_fires,
  naticusdroid_android_permissions_dataset, sepsis_survival_minimal_clinical_records; their numbers did not move
  materially). Two are new, both kept (evidence in the records and the cases table of
  `.claude/skills/verify-dataset/references/task_probes.md`): consumer_complaints_1m (`unstable`: above the dummy
  in 3 of 3 windows, the standard error over 3 windows is the drift between them) and
  electric_motor_temperature_prediction (`no_spread`: every probe model has R^2 0.94-0.97, while the tuned
  methods on BeyondArena range from RMSE 1.77 to 3.52).

## 2026-10-06 (pandas 2 and 3 build the same containers; four datasets rebuilt with nanosecond times)

- pandas 2.3.3 and pandas 3.0.6 now build the same container for every dataset: check-only builds of all 128 under
  both (scikit-learn 1.7.2) give the same checksum each. Before the changes below, pandas 3 changed 17 checksums
  (dates parsed to `us` or `s` instead of `ns`; values, metadata and splits were the same) and crashed 5 definitions.
- The standard steps store datetimes and durations in nanoseconds and pandas 3 `str` text as `object`
  (`canonical_dtypes`, after `cast_dtypes`). The loader gives text categories `object` categories under pandas 3, as
  pandas 2 does, and the object-column checks count `str` columns (`object_columns`, now in `data_foundry.v2`).
- Rebuilt the four datasets whose time column was not in nanoseconds; the values, rows and splits are unchanged, the
  checksums are new: `cooking_time_1m` (`01a11121-7e5f-7033-902e-21ba9ae0fc7a`), `delivery_eta_1m`
  (`01a11121-cd9b-7915-848b-88d944416d63`) and `maps_router_eta_1m` (`01a11122-8acf-7d20-8706-085a7edf6e23`) had
  `datetime64[us]` from polars, `sberbank_housing_market_forecasting` (`01a11120-e8e3-707d-802c-84f8fa1cae08`)
  `datetime64[ms]` from the Excel reader. The build reloads and verifies all four, with no new warnings; their raw
  inputs did not change, so the check from the traced inputs was not re-run.
- Edited for pandas 3, each with the same container as before: `blood_transfusion` (`DataFrame.map` instead of the
  removed `applymap`), `california_house_prices_2020` (`Bedrooms` cast to `object` before numbers are written into
  it), `consumer_complaints_1m` (an assert on the `Tags` values no longer goes through `astype(str)`),
  `in_vehicle_coupon_recommendation` (the respondent key writes a missing answer as `"nan"` explicitly; pandas 3's
  `astype(str)` keeps it missing), `santander_transaction_value` (`notna()` instead of `fillna(0)` on the id columns),
  and `anes_voting_2026`, `homesite_quote_conversion`, `home_credit_default_risk` (`object_columns(df)` instead of
  `select_dtypes(include="object")`, which pandas 3 deprecates for `str` columns).
- Building needs the new `build` extra (scikit-learn `>=1.6,<1.8`, scipy, liac-arff, openml, polars, the Excel
  engines, matplotlib); loading a container needs only the core install. scikit-learn 1.8 changes
  `StratifiedGroupKFold` (on 13 sample datasets, 1.9 changed the splits of in_vehicle_coupon_recommendation, emscad
  and sepsis_prediction_1m; 1.6 and 1.7 give the same splits); python-calamine 0.8 cannot open the xlsx of
  gallstone_disease. The lock stays on pandas
  2.3.3, since AutoGluon 1.5 requires pandas below 2.4; CI runs the tests under pandas 2 and 3.

## 2026-10-06 (audiology_diagnosis and eryhemato_squamous_disease changed; task-probe review complete)

- `eryhemato_squamous_disease` rebuilt with the clinical features only (new UUID `01a110c0-0a69-7edb-95e9-f96e2c752096`;
  34 → 12 features, same 366 rows and six classes). The source evaluates clinically first and takes skin samples for
  the 22 histopathological features afterwards; with them the task was close to solved (macro ROC AUC 0.999, flag
  `solved`). Before the biopsy it is the clinical differential: macro ROC AUC 0.98, 87% accuracy for logistic
  regression. Task probes: no flags. Evidence in the record.
- `audiology_diagnosis` rebuilt with a new target (new UUID `01a1109b-6cc4-7fb8-9797-facc98f95aba`; 199 → 195 rows,
  68 → 65 features). The old 3-class merge (cochlear / normal / other) was our own, made from the diagnosis names; the
  new target is the standard distinction between a hearing loss with and without a conductive part: normal 19,
  sensorineural 142, conductive_or_mixed 34. bells_palsy and the central diagnoses (possible_brainstem_disorder,
  poss_central) are dropped as not a type of hearing loss, and the brainstem-test columns that only those cases had
  (bser, viith_nerve_signs, waveform_ItoV_prolonged) with them. The duplicated cases stay dropped. The 24 original
  diagnoses are not usable (16 have 4 or fewer cases), and the four large cochlear ones are spelled out by two history
  findings. Task probes: no flags (were `no_spread`, `unstable`). Evidence in the record.
- The task-probe review of the 24 flagged datasets is complete (each record has a dated comment with the evidence;
  the rules and a table of the decisions are in `.claude/skills/verify-dataset/references/task_probes.md`): 2 retired (fitness_club, parkinsons_biomedical_voice_measurements,
  2026-10-05), 2 changed (audiology_diagnosis, eryhemato_squamous_disease, above) and 20 kept without a container
  change: forest_fires, clock_protein_toxicity, asp_potassco_classification, sepsis_survival_minimal_clinical_records,
  musk, pancreatic_cancer_mouse_detection, aps_failure, coil_2000, marketing_campaign,
  naticusdroid_android_permissions_dataset, mercari_price_suggestion, california_house_prices_2020, amex_non_iid_1m,
  acquire_valued_shoppers_challenge, gallstone_disease, indian_liver_patient_dataset,
  mercedes_benz_greener_manufacturing, coffee_rating_prediction, garments_worker_productivity and
  heart_disease_cleveland. A selection version of asp_potassco_classification (PAR10) is planned to replace it
  (`TODO.md`).
- Removed `TASK_PROBES.md`: the sweep of 2026-10-01 is settled, its decisions are in the records and above, and the
  probe script changed (below), so its numbers are not comparable with a new sweep. A sweep's output now stays in the
  scratch folder of the run (`rebuild-working-copy`, step 6).
- The probe tooling of the verify-dataset skill, after what the review found: `task_probes.py` picks the single
  feature on each split's training side, pairs the `no_spread` test by split and probes every split (up to 30) of a
  dataset with at most 5,000 scored units, reads `unstable` as the share of splits above the dummy and the standard
  error of the mean, encodes text columns, flags `one_feature` only when the models also remove less than a fifth of
  what the feature leaves, compares the drift baseline on log loss (binary temporal tasks included), and adds
  `few_minority`. `leak_probes.py` adds a shallow-tree probe. The new `tuned_results.py` sets a flag against the
  benchmark's tuned methods (per-fold BeyondArena results). On the datasets of the review, the false flags of
  aps_failure, coffee, garments, mercari, california, musk and heart_disease_cleveland are gone; gallstone_disease's
  untuned families still tie (its tuned methods spread).

## 2026-10-05 (fitness_club and parkinsons retired; task-probe review)

- Removed `parkinsons_biomedical_voice_measurements`: retired as too small (`No (Retired)`, marker `Too Small`;
  evidence in the record). 32 patients, 8 of them healthy: every grouped test fold scores 2 or 3 healthy people, and
  on BeyondArena the method ranks agree across folds less than on 98% of the datasets (best AUC per fold from 0.58 to
  1.0). A BeyondArena dataset; the shipped notebook and collection pin are unchanged, and its container and raw file
  stay in the warehouse. It was the only `mean` group-unit dataset: `BENCHMARK_CHANGES_TODO.md` now lists three.
  128 datasets remain, 43 of them from TabArena v0.1.
- Removed `fitness_club`: retired as trivial (`No (Retired)`, marker `Trivial`; the record's comment has the
  evidence). Ranking the members by `months_as_member` alone, with no model, gives ROC AUC 0.822 on the 30 shipped
  folds, above all 37 BeyondArena configurations (best RealTabPFN-2.5 0.821, median 0.818); every other feature lowers
  the score. The booking lead time also follows a generator's rule: `days_before` is 2 x the weekday's number in 1,251
  of the 1,500 rows. A TabArena v0.1 and BeyondArena dataset; the shipped notebook and collection pin are unchanged,
  and its container and raw file stay in the warehouse (`LEAK_AUDIT.md`, the table in `README.md`).
- The verify-dataset skill has a reference on reading the flags (`.claude/skills/verify-dataset/references/task_probes.md`).

## 2026-10-02 (getting started; the grouped-data plan and the Atlas folder removed)

- Added [`GETTING_STARTED.md`](GETTING_STARTED.md), the way in for a new curator, made from the Atlas getting-started
  guide (`datasets/_dev/atlas/`) and independent of it: set-up, this folder, the curation log, the two workflows in
  v2 (settling a record, adding a definition), worked examples from this folder, and the large-data candidates
  (`Review Prio 1 (Atlas)`, 1M–10M rows) as the priority, with their state as of today. `datasets/_dev/atlas/` is
  removed: its 11 v1 seed notebooks are v2 definitions here, and its size tracker's notes are in the candidate list.
- Removed `GROUPED_DATA_PLAN.md`: the plan is implemented. Its scoring recommendation (section 4) moved to
  [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md); the use cases are in each grouping's `definition`, and
  the deferred items in `TODO.md`. The entries below still name it.
- The generated READMEs escape the characters markdown would interpret in the sample rows and the data-check
  tables (a SMILES such as `[C@H](C)` rendered as a link), and describe `explore.ipynb` as committed without
  outputs. All 130 READMEs are regenerated; no container changes.

## 2026-10-02 (README: sample rows)

- Every dataset `README.md` has a "Sample rows" section after "Dataset and task": the first 5 rows of the final frame
  (random rows after the shuffle; the oldest rows of a temporal task), the target first, at most 12 columns, cells cut
  at 40 characters. All 130 READMEs are regenerated with `dataset check`; no container or UUID changes. The
  `explore.ipynb` workbenches stay without outputs: the README is the evidence page, with a staleness check.

## 2026-10-02 (probe scripts moved into the verify-dataset skill)

- The leak, task and group probes and the collection bundle check moved from `scripts/v2/` and
  `scripts/beyond_arena/` to `.claude/skills/verify-dataset/scripts/`, next to the skill that runs them. The paths in
  this folder's `README.md`, `TASK_PROBES.md`, `LEAK_AUDIT.md` and `GROUPED_DATA_PLAN.md`, in
  `parkinsons_biomedical_voice_measurements`'s accepted-warning reason and in the "Group structure" section of the 16
  grouped READMEs follow; no container changes. The entries below keep the old paths.
- The rebuild procedure of this folder (parallel build, comparison with the previous build, the check from the traced
  inputs, the backup zip, the dataset table) is the new `rebuild-working-copy` skill, with its scripts; the README's
  "Rebuild" section points to it.

## 2026-10-02 (rebuild as container format 2; telemonitoring retired)

- Rebuilt all 131 datasets as container format 2 (`dataset build`, new UUIDs; the table in
  [`README.md`](README.md)). Every saved container reloads and verifies its checksum, and the rows, splits and
  findings are the same as in the build of 2026-10-01 (0 errors, 62 open warnings in 45 datasets, none new; 61 in 44
  after the retirement below). The build read the same raw files, and a check-only rebuild from a warehouse holding
  only the 435 of them that the 130 remaining datasets read gives the same checksums.
- Removed `telemonitoring_parkinsons_biomedical_voice_measurements`: retired (`No (Retired)`, No Good Target /
  Scientific Discovery). 88% of its target's variance lies between the 42 subjects, and the voice features barely
  track it: on unseen subjects the best model is about 2% better than the training mean (BeyondArena's best,
  CatBoost, is no better than the mean). Recast as tracking a known patient, the baseline visit does the work
  (RMSE 6.48 for the baseline plus the mean drift, 6.33 with voice). Evidence in the record and
  `GROUPED_DATA_PLAN.md`, section 10. BeyondArena dataset; the shipped notebook and collection pin are unchanged.
  `LEAK_AUDIT.md` lists it under Removed (12; 130 datasets remain).
- `amex_non_iid_1m`: unchanged. The record now holds the comparison of the per-customer aggregations (LightGBM on
  the grouped folds: `last` ROC AUC 0.958, `max` 0.949, `mean` 0.946), which supports `last` with
  `context="all_rows"`.

## 2026-10-01 (v0.2 rebuild of all 131 datasets)

- Built all 131 datasets (`dataset build`, new UUIDs, superseded by the build of 2026-10-02). Every saved container
  reloads and verifies its checksum. Rebuilding every dataset from a warehouse that holds only the 436 raw files the
  build read (traced per dataset) gives the same checksums; those files and the 33 raw inputs of the two
  `_prepare_raw_files` steps are backed up outside the repository with a manifest.
- Removed the v1 notebooks (126 files) and the migration scripts (`scripts/v2/migrate_notebook_to_v2.py`,
  `scripts/v2/check_equivalence.py`): the migration is finished. The `# MIGRATE:` notes are gone with them: v2
  shuffles the 13 datasets the v1 notebooks left in file order, and `hiva_agnostic` with seed 42 instead of 11.
- Fixed by the first build pass:
  - `ieee_fraud_detection`: `_feature_types` named 7 of the 51 categorical columns (the list stayed in `_clean`
    after the dtype casts moved), so 26 columns were `object`; it now names all 51, as the shipped container has.
  - `home_credit_default_risk`: NaNs with the sign bit set (x86 gives them for `inf - inf`, in 37 ratio features)
    did not survive the save, so the checksum did not verify. The base class now writes every float NaN as the
    standard one (`canonical_nans`); no value changes.
  - `coffee_rating_prediction`: categories of the `string` dtype came back as `object` after the save; `cast_dtypes`
    now stores text categories as `object`.
- `amex_non_iid_1m` and `sepsis_prediction_1m` accept `splits_rows_never_tested`: the 500k cap on a test fold trims
  whole groups, so 325 (0.02%) and 3,371 (0.2%) rows are in no test fold.
- Added `TASK_PROBES.md`: the task-probe sweep over the built containers (131 datasets, no crash; 25 flagged, listed
  in `TODO.md` for a decision).
- Open warnings: 62 in 45 datasets, all present in the bundle checks of the shipped containers, except
  `groups_test_groups_few` for telemonitoring (open decision, `TODO.md`).

## 2026-10-01 (framework review before the rebuild)

- Same data on every run and machine. 20 `sort_values` calls in 18 definitions now sort with `kind="stable"` (numpy's
  default sort breaks ties differently with and without AVX512: anes_voting_2026 gave three checksums on three CPU
  modes), kickstarter and home_credit_default_stability_1m sort their file listings, and the split sampler breaks
  ties explicitly (sepsis_prediction_1m kept 1,500,000 or 1,499,998 rows depending on the CPU). A new definition check
  refuses unstable sorts, unsorted listings, an unordered polars `group_by` and unseeded randomness. anes and sepsis
  now give one checksum on all three CPU modes; california_house_prices_2020 still differs in the last bit of 195
  log-scaled targets (numpy's SIMD log), with the same rows and splits.
- `acquire_valued_shoppers_challenge` and `home_credit_default_stability_1m`: `_prepare_raw_files` gives the same file
  on every run. acquire sorts by `id` within a date (only the row order varied); home_credit sorts each case's rows
  fully before `first` / `last` and the sums (about 141k values of 9 `first_` / `last_` columns varied between runs)
  and sorts its output by `case_id`. Both files were regenerated in the warehouse (the old ones are kept as
  `merged_input_data.parquet.pre-2026-10-01`); home_credit has 718 columns instead of 719, because one `first_` /
  `last_` pair is now identical and is dropped as a duplicate.
- Shipped checksums: `split_random_state`, added on 2026-09-18, entered every checksum as `null`, so no shipped
  BeyondArena container verified with the library; it is now left out while unset (all 142 verify again).
- Group statistics: the nearest neighbour of a row is never the row itself (duplicates made it so), chance is the
  share of other rows in the same group, and single-row groups no longer count towards `groups_labels_constant`.
- No definition's metadata changed apart from the sorts and listings above; the containers are rebuilt next.

## 2026-10-01 (checks that a task is worth benchmarking)

- `dataset check` gets five findings that every test fold can be scored and the target varies
  (`data_foundry.v2.task_checks`): `splits_test_single_class` and `splits_test_target_constant` (errors: the metric
  is undefined), `splits_test_minority_few` (a binary test fold with fewer than 10 rows of its rarer class),
  `splits_test_class_missing` (a multiclass test fold without some class) and `task_target_value_dominant` (one value
  holds half of a regression target). They appear when the datasets are next checked; no definition changed.
- `scripts/v2/task_probes.py`: the sweep against dummy baselines on the shipped splits (three untuned model families,
  the best single feature, a drift baseline for temporal tasks, per-group scores for group-unit tasks), with the flags
  `no_signal`, `solved`, `no_spread`, `one_feature`, `drift_baseline` and `unstable` for the curator. The add-dataset
  loop, the verify-dataset rubric (item 13) and the guidelines (criterion 4C) use it.

## 2026-10-01 (grouped data: the regime as one object, with the use case)

- Every grouped and temporal definition declares its regime as one object (`GROUPED_DATA_PLAN.md`, section 3).
  The 17 grouped definitions declare `grouping = Grouping(on, labels, time_on, prediction_unit, aggregation,
  context, definition)`, stored in the container as `task_metadata.grouping`; the `definition` cites the source's use
  case. Group unit: musk (`any`), parkinsons_biomedical_voice_measurements (`mean`), amex_non_iid_1m (`last`),
  sat11_hand_algo_runtime (`select_min`), all with `context="all_rows"`; the other 13 predict per row with
  `context="none"`. The 20 temporal definitions declare `temporal = Temporal(on, splits, horizon, horizon_unit)`.
  A migration script moved the flat attributes, and a comparison over all 131 definitions shows no change in any flat
  metadata field or temporal window: the IID and temporal checksums are unchanged, the 17 grouped ones change (the
  new block). Not built.
- Revised 2026-10-02, before the rebuild: a v2 definition builds a container of format 2
  (`container.format_version == 2`, also written to `container_metadata.json`). Its task metadata
  (`PredictiveMLTaskMetadataV2`) stores the group fields once, in `grouping`; the flat `group_on`, `group_labels` and
  `group_time_on` are no longer written (they are read-only views of the block), and `container.grouping` raises for
  a format-1 container. Every checksum changes (the task metadata type). A fixed-length window (a calendar unit, or
  `unit="rows"`) is the horizon, and declaring it again is an error: 12 definitions with calendar windows and
  `mercedes_benz_greener_manufacturing` (320 rows) dropped their `horizon` / `horizon_unit`, each equal to the window;
  `anes_voting_2026` and `garments_worker_productivity` (`unit="unique"`), `california_house_prices_2020` and `kick`
  (`window=None`) and `hotel_booking_demand` (`_make_splits`) keep theirs. No horizon changed.
- Group checks in `dataset check`: the README of a grouped task gets a "Group structure" section (the fields, groups,
  rows per group, test groups per fold, label granularity, clustering against chance) and four findings
  (`groups_test_groups_few`, `groups_largest_share_high`, `groups_labels_constant`, `groups_not_clustered`).
  `scripts/v2/group_probes.py` runs the model-based probes on demand. On the 17 grouped datasets the findings fire for
  parkinsons and telemonitoring (few test groups) and emscad (labels nearly one per poster).
- `parkinsons_biomedical_voice_measurements`: accepted `groups_test_groups_few` (per-subject ROC AUC 0.82, permutation
  test p = 0.01) and `task_group_time_on_few_unique` (`session_number` orders the recordings).
- `emscad`: accepted `groups_labels_constant` (2 of 4,441 posters have both labels, so `per_sample` stays).
- `asp_potassco_classification`: the comment no longer calls the instances of a problem class "differing only in seed
  or task configurations", and says the source split at random. `in_vehicle_coupon_recommendation`: the comment no
  longer states that the paper's 5-fold results were random splits (the paper does not say).
- Open: `telemonitoring_parkinsons_biomedical_voice_measurements` has no signal across subjects (R^2 below 0 for all
  models on the grouped splits, 0.75 on random splits); retire or recast as warm-start tracking
  (`GROUPED_DATA_PLAN.md`, section 10).

## 2026-10-01 (mice_protein retired)

- Removed `mice_protein_trisomy_discriminant`: retired (`No (Retired)`, No Good Target / Scientific Discovery). The 8
  classes are the experimental design (genotype from breeding, training protocol, memantine or saline injection), all
  known for every mouse; neither source predicts (Higuera et al. 2015 cluster with self-organising maps, Ahmed et al.
  2015 test group differences), and the learning outcome was never measured ("sacrificed at 60 minutes post training
  without measurement of freezing"). The protocol part is separated perfectly (per-mouse AUC 1.0, SOD1 alone),
  genotype reaches 0.93 and treatment 0.77; the 1,080 rows are 15 dilution-series spots of 72 mice. BeyondArena
  dataset; the shipped notebook and collection pin are unchanged. `LEAK_AUDIT.md` lists it under Removed (11; 131
  datasets remain), and the grouped-data plan and `BENCHMARK_CHANGES_TODO.md` no longer use it as an example.

## 2026-10-01 (covertype back to IID; dementia comments)

- `covertype`: IID splits on the full data instead of leave-one-wilderness-area-out on a reduced frame: all 7 cover
  types and all 4 areas, 581,012 rows instead of the 3 classes and 3 areas that a split by area allowed. The source
  (Blackard & Dean 1999) drew its cells at random; with 3 groups the split by area was three domain-shift tests rather
  than a grouped task, and it dropped 4 of the 7 cover types. The curation comments say why and note that IID is
  optimistic for land far from mapped cells (one stand of 2-80 ha spans about 20-900 cells). The record's required
  split is now IID. Checked: 0 errors, 0 warnings, IID 1x3; first `README.md`. Not built; it no longer matches its v1
  notebook.
- `dementia_prediction`: the curation comments list every feature the frame keeps (sex, age, education, SES, the
  same visit's MMSE, eTIV, nWBV and ASF, which is 1755 / eTIV), where they named only the three MRI measures. The
  record's required split is now grouped and its problem type multiclass. Metadata only, the checksum changes; not
  checked or built.

## 2026-10-01 (sat11: censored runtimes)

- `sat11_hand_algo_runtime`: the 112 of 296 instances on which all 10 algorithms time out are dropped (1,120 rows,
  2,960 -> 1,840). Every run stops at 5,000 s and a timeout is stored as that cutoff, so their labels are only lower
  bounds, and they cannot change which algorithm a selector picks (the single-best to virtual-best PAR10 gap is the
  same with or without them). The 666 timeouts of the remaining instances stay at the cutoff, which keeps the order
  within an instance and is enough for PAR10. The curation comments explain the censoring and that a survival task
  type could use every run. `source_url` now points to SAT11-HAND-ALGO, the scenario the download uses. The split
  stays grouped by instance, still 10x3. Checked: 0 errors, 1 warning (`dataset_constant_column`, 3 columns that are
  constant in the raw data too); first `README.md`. Not built; it no longer matches its v1 notebook.

## 2026-10-01 (cardiotocography: patient key)

- `cardiotocography`: a curation comment explains the grouping. The rows are overlapping segments of one exam file
  (1,706 of 1,774 consecutive pairs overlap), so a file's rows must stay together. The patient ID above the file is
  our guess from the file names (176 IDs for 352 files, 10 of them spanning exam dates up to 1,139 days apart), and
  the comment says what its errors can and cannot leak. Metadata only, the checksum changes; not checked or built.

## 2026-10-01 (pancreatic: target name and counts)

- `pancreatic_cancer_mouse_detection`: the target is renamed `HasCancer` -> `HasPanIN`: the positive mice carry
  pancreatic intraepithelial neoplasia, preinvasive lesions without invasive or metastatic disease (Hingorani et al.
  2003). The curation comments now give the download's counts (181 spectra: 80 PanIN, 101 control; 73 mouse IDs: 35
  PanIN, 38 control) against the paper's (191 spectra after quality control: 80 PanIN, 111 control; 72 mice), where
  the old comment said the spectra counts match. A new comment notes that the third file-name token (`02` control,
  `03` PanIN, some with a `t` suffix of unknown meaning) encodes the class and never enters the features. The record's
  `problem_type` is now Binary Classification (was Multiclass). Checked: 0 errors, 1 warning
  (`dataset_missing_value_sentinel`, 999 in two m/z columns, open); first `README.md`. Not built.

## 2026-10-01 (telemonitoring: test days nearest the clinic assessments)

- `telemonitoring_parkinsons_biomedical_voice_measurements`: UPDRS was assessed at baseline, 3 and 6 months and
  linearly interpolated for the weekly test days in between, so the definition keeps three test days per subject. The
  middle one is now the test day nearest the 3-month assessment, found where the subject's interpolated UPDRS bends
  (a continuous two-piece linear fit: median day 91, 77 to 115; the kept day is 5 days before to 8 days after it).
  Subjects 14 and 30 show no bend and get the test day nearest day 91. Before, it was the last session before day 130
  (median day 126), whose label was interpolated a median 35 days after the assessment. Each kept test day now keeps
  all its phonations (exact test times kept only part of a day), and the sessions are ordered by `test_time` (the
  first and last rows in file order were not the earliest and latest for 2 and 3 subjects). 502 -> 749 rows, still
  126 test days of 42 subjects. BibTeX: Tsanas et al. 2010 (IEEE TBME 57(4)) instead of the 2009 preprint. Checked:
  0 errors, 0 warnings, grouped 20x3; first `README.md`. Not built; it no longer matches its v1 notebook.

## 2026-10-01 (telemonitoring source link)

- `telemonitoring_parkinsons_biomedical_voice_measurements`: `source_url` is now the Parkinsons Telemonitoring record
  (UCI 189, 10.24432/C5ZS3N) instead of the Parkinsons dataset (UCI 174), the year 2009 instead of 2007, and the
  download command fetches UCI 189's zip (its `parkinsons_updrs.data` is the same file, md5
  4f97310e2c9fbeedb72e8a37822fee45). Metadata only, the checksum changes; not checked or built.

## 2026-10-01 (parkinsons citation)

- `parkinsons_biomedical_voice_measurements`: the BibTeX now cites Little et al. 2009 (IEEE TBME 56(4), the study that
  recorded the 195 phonations; the data file asks for it) and Little et al. 2007 (BioMedical Engineering OnLine 6:23,
  the feature methods; UCI's citation request). The 2007 entry had the wrong venue ("Nature Precedings").
  `group_time_on = "session_number"` stays: it counts up within a subject and gives the order. Metadata only, the
  checksum changes; not checked or built.

## 2026-10-01 (sepsis use case stated)

- `sepsis_prediction_1m`: the comments now state the simulated use case, a snapshot early warning for patients not seen
  in training (every hour, sepsis within 6 hours, from that hour's measurements only; trained once, no refit with a
  patient's data). The old first paragraph called the time order irrelevant because the task "predicts for one full
  patient", which read as one prediction per stay; that setting leaks the outcome through the record length (septic
  records end at most 9 hours after their first positive hour). The challenge's setting with the patient's earlier
  hours stays a possible upgrade. Comment text only, no data change; the metadata changes, so the checksum does (its
  README is stale until the re-check in `TODO.md`).

## 2026-10-01 (grouped data: design plan)

- Added `GROUPED_DATA_PLAN.md`: the use case of each of the 19 grouped datasets from its source (unit, aggregation,
  what is known when predicting), the data findings (IID vs grouped gaps; the three small grouped tasks are learnable
  and stay), the new metadata kept in data-foundry (`group_definition`, `prediction_unit`, `group_aggregation`,
  `group_context`; no weighting field), the recommended scoring for TabArena, the checks, the dataset review and the
  open decisions. Linked from `README.md` and `BENCHMARK_CHANGES_TODO.md`. Nothing implemented yet.
- `GROUPED_DATA_PLAN.md`: one structure per regime (`Grouping`, `Temporal` with its horizon) stored as one optional
  block, the flat fields kept for compatibility; amex's use case corrected (one prediction per customer from all its
  statements; Kaggle's test data holds each customer's full history, about 12 statements, not only the latest).

## 2026-10-01 (benchmark changes to do)

- Added `BENCHMARK_CHANGES_TODO.md`: the changes the TabArena harness needs for grouped tasks (group column never a
  feature, group-aware inner validation, scoring at the task's prediction unit, group context for aggregate features,
  dataset-specific metrics, effective sample size) and the frame sizes of temporal `_1m` versions. Linked from
  `README.md`.

## 2026-10-01 (temporal `_1m` versions sampled per window; climate and delivery column fixes)

- v2 split protocol: a temporal `_1m` version no longer samples its frame to 1.5M rows. The windows are built on the
  full data, then `v2.splits.sample_temporal_splits` keeps at most 500k rows of each test window (random within the
  window) and a random 1M of all earlier rows for each train side, all drawn in one random order so the train sides
  of the windows overlap; the frame keeps only the rows a split uses. Test windows stay dense, train still covers the
  whole history (as TabReD sampled it), and no shipped row is unused. A temporal `_1m` version whose windows all fit
  the budget is refused. IID and grouped `_1m` versions are unchanged (frame sampled to 1.5M rows).
- Checked all 6 temporal `_1m` datasets with it (0 errors; each train side 1M rows):

  | Dataset | Frame rows | Test rows per window |
  |---|---|---|
  | `cooking_time_1m`, `delivery_eta_1m`, `maps_router_eta_1m` | 2,500,000 each | 500,000 (capped) |
  | `climate_model_weather_forecasting_1m` | 2,115,283 | 341,169-396,122 (all rows) |
  | `consumer_complaints_1m` | 1,811,452 | 203,139-307,396 (all rows) |
  | `home_credit_default_stability_1m` | 1,224,927 | 70,497-79,743 (all rows) |

  Before, the test windows held only the frame sample's share of rows (climate: about 30k per week instead of
  341-396k). The `splits_rows_unused` warnings are gone. Peak memory of a check: 182 GB for `maps_router_eta_1m`.
- `climate_model_weather_forecasting_1m`: dropped `cmc_0_1_11_0` (0.0 or missing in every row, like the three
  `cmc_0_1_*` columns already dropped); set -9999 to missing in `gfs_soil_temperature` (31% of rows),
  `cmc_0_0_0_2_grad` (1.9%) and `gfs_temperature_sea_grad` (0.3%), a fill value (the other values lie in about
  -21..52). 0 warnings.
- `delivery_eta_1m`: dropped `num_29`, `num_36`, `num_71` (constant except the same 2 of 16.7M rows) and `num_101`
  (one value, missing exactly where 19 other columns are missing). 0 warnings.
- Not built.

## 2026-10-01 (sf_permit_time and sberbank fixes, the two `_1m` windows settled)

- `maps_router_eta_1m`: its dtype casts moved into `_feature_types` as well (the cat/bin columns, and `timestamp`,
  which the parquet file already stores as a datetime); the processed frame is identical. Processing it peaks at
  162 GB of RAM, so it needs a large machine (see `TODO.md`).
- `sf_permit_time`: `Street Number`, `Unit` and `Zipcode` are now strings of whole numbers ("1625", "0", "94116"
  instead of "1625.0", "0.0", "94116.0"); pandas read them as int or float, and the old string cast went through
  float. Only these 3 columns change; checked: 0 errors, 0 warnings; new checksum
  `dfef6e633b868d96170fdaa565f88c62b8642afe58ba485e6ae85978a085258c` (README regenerated). Not built.
- `sberbank_housing_market_forecasting`: `state` is cast in `_feature_types`, after the build-year filter, so the
  level 33.0 no longer stays as an unused category. The one row with 33 (id 10092, likely a typo for 3) also has the
  range-coded build_year 20052009 and was already dropped by that filter. Only the category levels of `state` change.
- `consumer_complaints_1m` and `home_credit_default_stability_1m`: the 3-window splits of the v2 protocol are settled
  (the `TODO(verify)` markers are now plain comments). Checked, 0 errors. consumer_complaints: 3 quarters of 2025
  (test 134,242 / 131,511 / 88,402 rows for Q2 / Q3 / Q4, train 1M each, horizon 3 months). home_credit: 3 windows of
  2 months from 2020-05-01 (test 73,349 / 78,349 / 69,338, train 1M each, horizon 2 months). Both warn
  `splits_rows_unused` (6.4% and 14.2%: rows that no capped train side drew); home_credit also warns
  `dataset_missing_value_sentinel` for -1 in 3 `avgdbd*` columns, now accepted: they are "average days past or before
  due of payment" (Kaggle `feature_definitions.csv`), negative means paid early, -1 is the mode of a smooth
  distribution (-1 4.8%, -2 4.7%, -3 4.2%, 0 3.8%), missing values are already NaN, and the default rate rises from
  2.1% (more than a day early) over 3.3% (-1) and 4.5% (on time) to 8.6% (late). READMEs regenerated. Not built.

## 2026-10-01 (dtype casts moved into `_feature_types`)

- 52 definitions: the dtype casts the migrator had left in `_clean` now live in `_feature_types`, so every dataset
  declares its categorical, string and datetime columns in one place (and the generated `README.md` lists them).
  List-and-loop string casts became `string=[...]`; target casts went (the base class casts a classification target);
  casts a later step needs stay in `_clean` with a comment and are also listed (rossmann, telemonitoring,
  micro_mass, musk, parkinsons, coffee, homesite, kickstarter, consumer_complaints, climate, anes, california).
  Column drops stay as they are: `df.drop(columns=...)` already fails on a misspelled name.
- Verified: the processed frame of all 52 datasets is identical before and after (values, column order, dtypes and
  category levels per column), so the migration check against the v1 notebooks is unaffected; the 12 checked
  datasets touched keep their checksum (their `README.md` regenerated, only the "Feature types" lines changed).
- To keep the frames identical, two quirks stay and are listed in `TODO.md`: `sf_permit_time`'s `Street Number`
  strings read "101.0" (the v1 cast went through float), and `sberbank_housing_market_forecasting`'s `state` keeps an
  unused level (33.0). `early_learning_predictors`' `child_dob` now fails on a value it cannot parse instead of
  setting it to missing (every value parses today). `maps_router_eta_1m` is not done: its frame does not fit in
  memory (see `TODO.md`).

## 2026-10-01 (v2 split protocol: always 3 folds, frames sub-sampled to 1.5M rows)

- New split protocol for v2 definitions, in the new module `src/data_foundry/v2/splits.py`. Every dataset gets 3-fold
  cross-validation (20, 10, 3 or 1 repeats by train size, as before) or at least 3 temporal windows; no split trains
  on more than 1M or tests on more than 500k rows. Only a frame above 1.5M rows is sub-sampled, to 1.5M rows (rows
  stratified on the target, or whole groups; the row order is kept), in its `_1m` version, which then gets the same 3
  folds or windows. Before, a frame of 1.25M rows or more got one 1M / 250k split. `dataset check` replaces the v1
  findings `splits_dimensions_off_protocol` and `splits_test_over_budget` with the v2 ones and adds
  `splits_too_few` (a temporal task with fewer than 3 windows).
- v2 no longer uses `curation_recommendations`: the IID and grouped cross-validation, the temporal windows
  (`TemporalSplits`, moved from `curation_recommendations.get_temporal_window_splits`) and the sub-sampling live in
  `v2/splits.py`. The v1 helpers and `bundle_checks` are unchanged, so the v1 notebooks and the shipped containers
  keep the v1 protocol. Tests pin that the v2 cross-validation gives exactly the v1 splits, and the 27 checked
  datasets this does not touch give the same checksum and the same findings as before.
- Renamed (the frame fits 1.5M rows, so it is taken fully; `version_of`, `version_comment` and
  `subsample_to_budget` removed, record `v2_path` updated): `mercari_price_suggestion_1m` -> `mercari_price_suggestion`
  (about 1.48M rows, IID 1x3), `electric_motor_temperature_prediction_1m` -> `electric_motor_temperature_prediction`
  (about 1.30M rows, grouped 1x3), `lending_club_1m` -> `lending_club` (see the next entry).
- `lending_club`: only the 36-month loans issued up to 2015 (609,544 rows, before 1,310,259), tested on the quarters
  2015 Q2-Q4 (64,222 / 73,567 / 88,667 test and 383,088 / 447,310 / 520,877 train rows, horizon 3 months). The
  source file holds only the loans that had finished by the 2018Q4 snapshot: at least 99.8% of the 36-month loans
  up to 2015Q4, but 57-93% per quarter in 2016, and only 63-97% of the 60-month loans from 2014 on (counts from
  `accepted_2007_to_2018Q4.csv.gz`). The missing loans are mostly good ones, so later or longer loans skew the labels
  (default rate among finished loans 15-16% in 2013, 24-26% in 2016). `term` is joined only for the selection and
  dropped; `disbursement_method` is dropped (one value for these loans). The `_1m` version tested on 2016, the v1
  notebook on 2016-2018. Checked: 0 errors, 0 warnings; default rate 13.9%; new `README.md`. Not built.
- Still `_1m` (frame above 1.5M rows), now 3 folds or windows on the 1.5M-row sample: `amex_non_iid_1m`,
  `sepsis_prediction_1m` (grouped 1x3); `climate_model_weather_forecasting_1m`, `cooking_time_1m`, `delivery_eta_1m`,
  `maps_router_eta_1m` (3 windows of 7 days instead of 1); `consumer_complaints_1m` (3 quarters of 2025) and
  `home_credit_default_stability_1m` (3 x 2 months). These two carry a `TODO(verify)` marker for the window
  choice (see `TODO.md`).
- `covertype`: dropped the accepted `splits_test_over_budget` (its 257k-row test fold is within the 500k budget).
  `hotel_booking_demand`: dropped a diagnostic print of the v1 split recommendation (same checksum).
- Not run: apart from `lending_club`, none of the 11 changed datasets has been checked or built; their splits change
  at the rebuild.

## 2026-10-01 (dataset pages: README.md replaces report.md)

- The generated `report.md` of each dataset folder is now its `README.md`, so GitHub shows it below the folder's
  files. It is still written by `dataset check` / `build` from `dataset.py` and never edited by hand. New on the
  page: the files of the folder and what each is, links (curation record, original source, this collection's
  `README.md` and `CHANGELOG.md`), how to rebuild (raw-file folder, download commands, `check` and `build`), the
  feature types and the BibTeX (collapsed), and the curation notes. Tables longer than 10 rows are collapsed; a
  status line at the top says whether the dataset is built, and the build record stays at the end. Frontmatter
  format `data-foundry-report-v2`: the `feature_types` column lists moved into the body, because GitHub renders the
  frontmatter as a table at the top of the page (up to 137 lines for `mic`); the other keys are unchanged.
- Decision figures moved from `report/` to `figures/` (`kick`).
- The 30 checked datasets were moved (`git mv report.md README.md`) and regenerated with `dataset check`: 0 errors in
  all. 28 give the same checksum as before, including `consumer_complaints_1m` and `lending_club_1m`, so their
  reports were not stale after the `_1m` library change (open item closed, removed from `LEAK_AUDIT.md`).
  `diabetes_130_us` and `santander_customer_transaction_prediction` give a new checksum with the same data and
  splits (identical data-check and split tables; a second run gives the same checksum): the checksum also covers
  the metadata, and their committed reports were older than the last metadata edit in their `dataset.py`.
- Text only: the first docstring line of every `dataset.py` and the links in every `explore.ipynb` now name
  `README.md`; the template, the `/add-dataset` and `/verify-dataset` skills, AGENTS.md, CLAUDE.md, the repo
  README, `TODO.md` and this folder's `README.md` too.
- `early_learning_predictors`: removed `zindi_train.csv`, which `dataset.py` never read (the new page flagged it).
  The one `explore.ipynb` cell that compares our columns with the Zindi train set now reads the identical copy next
  to the shipped v1 notebook in `datasets/beyond_iid/grouped/early_learning_predictors/`. Checksum unchanged.

## 2026-10-01 (leak audit, second pass)

- Added `LEAK_AUDIT.md`: the leak-audit summary for the benchmark team and the tech report (the 10 removed and
  21 changed datasets with severity and source collection, the 3 kept datasets that affect results, small fixes
  and open items in the appendix). Linked from `README.md`.
- Skills: the leak-audit learnings (probes, what was decided per kind of leak, where the first suggestions were
  revised) are in `.claude/skills/check-candidate/references/leak_checks.md`, linked from `/check-candidate`,
  `/add-dataset` (and its `dataset_patterns.md` §D), `/verify-dataset` and `/triage-candidates`. New
  `scripts/v2/leak_probes.py <name>` runs the cheap probes on a folder (single-feature and missingness scores, scores
  without the top features, exact copies across the split, 1-NN label agreement, nearest-neighbour distance score).

- `sf_permit_time`: right-censored target fixed. Kept permits filed before 2024 (116,954 -> 99,847 rows; recent
  filings miss their slow permits, p90 days to issue about 300 -> 97 for 2025) and switched from 6 yearly windows to
  2025 to 9 half-year windows 2019-H2..2023-H2 (train >= 55%, horizon 6 months). Swapped the latitude/longitude names
  (WKT is POINT (lon lat)); the download description now states the filed_date filter, the download date and the new
  portal domain data.sf.gov. `dataset_constant_column` accepted (Y-or-missing flags). First `report.md`
  (0 errors, 0 warnings).
- `sepsis_prediction_1m`: comment only. The rows hold no future information; the leak risk is in the evaluation
  (complete test records, septic records end shortly after onset), so predictions must be causal per patient and
  scored with the PhysioNet 2019 utility per patient (planned scorer change); Patient_ID is group metadata only.
  First `report.md` (0 errors, 2 warnings; both fixed in the library, see the next entry).
- v2 library: sub-sampled `_1m` frames now drop category levels that no longer occur (dtypes are set on the full data;
  `sepsis_prediction_1m` kept 7,740 unused Patient_ID levels), and `splits_dimensions_off_protocol` skips a single
  split that fills the 1M train budget (whole groups left the sepsis frame 6 rows below 1.25M, so the check asked for
  1x3). This changes the saved frames of all `_1m` datasets: `sepsis_prediction_1m/report.md` is regenerated
  (0 errors, 0 warnings); the reports of consumer_complaints_1m and lending_club_1m are stale until regenerated after
  the audit.
- `sdss_17`: now a photometric task. Dropped `redshift` (fitted together with the class), `plate` and `fiber_ID`
  (spectroscopic pointing and slot: they encode the targeting program and duplicate the dropped MJD; AUC 0.80 alone,
  and they make LightGBM worse); deduplicated by sky position instead of the float-rounded `obj_ID` (which had removed
  21,947 distinct objects; 78,053 -> 99,999 rows); -9999 set to missing. Not built; `report.md` regenerated
  (0 errors, 0 warnings).
- `online_shoppers_purchasing_intention_dataset`: kept only June-December sessions (12,330 -> 6,875) and dropped the
  then-constant `SpecialDay`. In February-May every buyer has `PageValues` > 0 and it alone gives AUC 0.974 (likely
  the session's own purchase in the page-value table); from June it behaves like the paper's historical page metric
  (AUC 0.814). Split stays IID. TabArena v0.1 dataset. Not built; first `report.md` (0 errors, 0 warnings).
- `mutual_funds_india`: dropped `rating`, the Value Research star rating, which ranks funds within their category on
  60% 5-year and 40% 3-year risk-adjusted return and so is computed partly from the target (`returns_3yr` is the
  trailing return of the April 2023 snapshot). R^2 0.811 -> 0.783. Not built; `report.md` regenerated.
- `kick`: comments only, splits and features unchanged. The curation comment and the split decision no longer claim
  the Kaggle split was grouped by auction location (a buggy check; 78.9% of Kaggle test rows are at a location also
  in train); the temporal split stays. Missing `WheelType` (likely blanked on kick-back; AUC 0.757 -> 0.691 without it)
  is noted as a potential leak kept on purpose. `report.md` regenerated (0 errors, 0 warnings).
- Removed `iranian_churn`: retired (`No (Retired)`, Data Quality Issue). The paper's design ends each churner's
  feature window at the churn month (Keramati & Ardabili 2011, Sec. 4.1), so the task detects customers who are
  already leaving (AUC 0.986); there are no dates to rebuild a common prediction point.
- `homesite_quote_conversion`: comment only. `PropertyField37` x `PersonalField12` may be a post-quote status code
  (AUC 0.965 -> 0.915 without it), kept on purpose: anonymised fields, set up that way by the host, not flagged in the
  Kaggle discussions; revisit if documented. First `report.md` (0 errors, 2 warnings: 13 columns constant after the
  -1 -> NaN replacement, and a `' '` level in GeographicField63; both open).
- `jm1`: dropped exact duplicate rows (1,973) and every copy of a code-metric vector that occurs with both labels
  (176 rows): 10,885 -> 8,736 rows. 25% of rows shared their vector with another row, so random splits put copies on
  both sides. TabArena v0.1 dataset. Not built; `report.md` regenerated (0 errors, 0 warnings).
- `south_africa_coronary_heart_disease`: comment on post-outcome measurement (ESL Sec. 5.2.2: risk factors measured
  after the heart attack), which weakens rather than leaks the signal; features unchanged. `report.md` regenerated.
- `home_credit_default_risk`: definition restructured without changing the data (identical frame hash): all tables
  read in `_load_raw`, one helper per kernel function, column lists as module constants, unused list removed, and
  `_feature_types` no longer lists 25 categorical columns that the feature selection drops (the definition did not
  build). `dataset_missing_value_sentinel` accepted (`POS_MONTHS_BALANCE_MAX = -1` is the month before the
  application). Not built; `report.md` regenerated (0 errors, 0 warnings).
- Removed `ghanas_indigenous_intel`: retired for now (`No (Retired)`; Too Small, Data Quality Issue; to revisit).
  Farmers submit in single-label batches, so the 10,928 rows are 626 farmer-days, and each test window holds rain from
  only 3-6 farmer-days; without the reporter's identity LightGBM is near always-NORAIN (macro-F1 0.261 vs 0.241). The
  "no rain" label likely mixes no rain with no measurement (22 of 43 farmers never record rain in the rainy season).
- Removed `customer_satisfaction_in_airline`: retired (`No (Retired)`; AHDS, Data Quality Issue, Duplicate, Missing
  source information). The passenger ratings of the base Kaggle file are generated (rating columns copied from one
  another within customer segments, e.g. wifi = gate location in 95% of one segment), and the shipped file is a
  manipulated copy of it (misnamed rating columns, replaced distances, 14,659 labels flipped by a rule on the dropped
  Gender column). TabArena v0.1 dataset; the shipped notebook and collection pin are unchanged.
- `garments_worker_productivity`: `incentive` is now the previous working day's value (`incentive_lag_1`), like the
  other end-of-day columns. The paper (Al Imran et al. 2021, Sec. 3.1) defines it as a structured incentive paid for
  achieved performance, and within teams its daily changes follow the same day's productivity (Spearman 0.53) rather
  than the previous day's (0.07). LightGBM RMSE on the 30 splits 0.134 -> 0.140 (no incentive 0.141). Not built;
  `report.md` regenerated (0 errors, 0 warnings).
- Removed `ecommerce_shipping`: retired (`No (Retired)`, AHDS + Missing source information). `Warehouse_block` is
  `ID mod 6` (cycle D, F, A, B, C, F) and `Mode_of_Shipment` a 137-ID cycle, with no exception in 10,999 rows, so the
  file is generated; the target comes in two ID blocks (IDs 1-3,135 all late, AUC 0.506 on the rest) and the source
  cannot be traced. TabArena v0.1 dataset; the shipped notebook and collection pin are unchanged.
- `consumer_complaints_1m`: rebuilt from the CFPB FOIA narratives archive (CCDB exports 1-14, exported 2026-09-14,
  in `local-data-warehouse/consumer_complaints/foia_archive/`). The CFPB removed the narratives from the live download on
  2026-09-14, so the old download description no longer reproduces the dataset. The 2026-01-23 build filtered out
  complaints still "In progress" (7-70% of Oct-Dec 2025), which censored the test window; the archive labels are
  settled. Data now ends 2025-12-31 (narratives after 2025 are rare and differently selected), test window
  Oct-Dec 2025 (203,139 rows, 3-month horizon). The dispute filter became the equivalent date filter (>= 2017-04-24)
  and the consent filter "has a narrative"; narrative line endings normalised; label-conflicting duplicates now all
  dropped, as the comments said. `dataset_pure_feature_value` accepted (Block, Inc. company response policy).
  Not built; `report.md` regenerated (0 errors, 0 warnings).
- `coffee_rating_prediction`: temporal splits changed from 5 six-month windows (the oldest trained on 44% of the rows)
  to 13 two-month windows walking back until train would fall below 50% (54-115 test rows each, horizon 2 months).
  Monthly windows (26) would match the split-count convention but hold 2-72 reviews each. Not built; `report.md`
  regenerated.
- `get_temporal_window_splits`: calendar windows without `n_windows` now stop at the start of the data (they walked
  back until the timestamp overflowed). Skills: widen temporal windows that would hold fewer than about 50 test rows.

## 2026-09-30 (leak audit: retirements and fixes)

- `diabetes_130_us`: follow the paper's cohort (Strack et al. 2014, Sec. 2.3): keep each patient's first encounter
  (sorted by `encounter_id` to make it explicit; the kept encounters are unchanged) and remove encounters ending in
  death or hospice
  (1,084 "Expired", all not readmitted; 461 hospice). 71,518 -> 69,973 rows. "?" and "NULL" set to missing. Not built;
  `report.md` regenerated (0 errors, 0 warnings).

- `hotel_booking_demand`: training now holds only bookings arriving before each prediction point (the kept
  future-arrival cancellations were 100% cancelled; `splits_temporal_leakage` resolved); dropped `BookingChanges`,
  `AssignedRoomType`, `RequiredCarParkingSpaces` (recorded after the prediction point); `Agent`/`Company` "NULL" set to
  missing; horizon 3 months. The migrated `_make_splits` dropped the outcome columns before using them (crash); they
  are now dropped after splitting. LightGBM log loss about 1.7 -> 0.33. Not built; `report.md` regenerated.

- Removed `seismic_bumps`: retired (`No (Retired)`, `Too Small`). The rows are consecutive shifts of a
  non-stationary sequence, so the IID split is wrong; under the temporal convention (30 splits, >= 50% train) the
  newest half holds only 49 of 170 positives, 0-5 per test window. TabArena v0.1 dataset; the shipped notebook and
  collection pin are unchanged.
- Skills: the temporal split convention (as many splits as an IID task of that size, >= 50% train) and a check for
  positives per test window are now in the curation guidelines and `dataset_patterns.md`.

- `california_house_prices_2020`: the deduplication reordered rows by address, so `time_index` (and the temporal
  split) was the alphabetical address rank; rows are now sorted back to the Kaggle Id (= sale order) before
  `time_index` is rebuilt. Splits unchanged in form (3 row windows, newest first). Not built; `report.md` regenerated.

- `in_vehicle_coupon_recommendation`: grouped splits on a new `respondent` column (consecutive blocks of the same
  first-part survey answers in the raw file, 587 groups), i.e. a cold-start task; AUC 0.83 IID -> 0.75 grouped.
  TabArena v0.1 dataset. Not built; `report.md` regenerated (0 errors, 0 warnings).

- `wine_quality`: dropped exact duplicate rows (6,497 -> 5,320; identical features and score, no conflicts) instead
  of the audit's grouped split; the split stays IID. `task_target_low_cardinality` accepted (median expert grade,
  modelled as regression by Cortez et al. 2009). TabArena v0.1 dataset. Not built; `report.md` regenerated.

- `emscad`: dropped reposts (identical except `job_id` and `location`, per Vidros et al. 2017 Sec. 5) and switched to
  grouped splits on a new `poster_group` (exact company profile or poster-specific masked contact hash); 17,460 ->
  16,116 rows, 4,441 groups. LightGBM AUC about 0.99 IID -> 0.938 grouped. Blank-looking text values set to missing.
  `dataset_pure_feature_value` accepted (large legitimate clients). Not built; `report.md` regenerated.

- Removed `hazelnut_spread_contaminant_detection`: retired (`No (Retired)`, `Data Quality Issue`). The 2,400 rows are
  repeated scans of about ten contaminant set-ups (Urbinati et al. 2020, Sec. IV.A); the set-up label was never
  released and the file order does not reveal it, so a grouped split cannot be built. TabArena v0.1 dataset; the
  shipped notebook and collection pin are unchanged. The outreach to the authors is noted in its record.

- `biogeographical_ancestry_prediction`: dropped the Turkey class (a separately genotyped source with an assay
  artefact at `rs3857620`: AG in 24/28 Turkey samples, GG in all others) and the two SNPs that are constant without it
  (`rs3857620`, `rs367953206`); `NN` no-calls set to missing. 635 -> 607 rows, 10 -> 9 classes, 104 -> 102 features.
  Not built; `report.md` regenerated (0 errors, 0 warnings).
- `report.md` rendering: a data-check entry that is a message instead of a table (e.g. "No numeric features to
  summarize." for an all-categorical dataset) crashed `dataset check`; it is now written as text (tested).

- `santander_customer_transaction_prediction`: dropped the 400 `var_i_has_one`/`has_zero` features (Kaggle #1
  solution), computed from the labels of all rows before splitting; 600 -> 200 features (the raw vars). LightGBM AUC
  0.903 -> 0.896. `curation_comments` note that the value-count technique is worth doing inside a pipeline, per fold.
  Not built; `report.md` regenerated (0 errors, 0 warnings).

- Removed `maternal_health_risk`: retired (`No (Retired)`, `Data Quality Issue`). Only 416 of 1,014 feature vectors
  are unique (the file's tail is copies of earlier rows), and the real group structure (six collection sites, IoT
  device and web portal; Ahmed & Kashem, STI 2020) is not in the file, so no split can be trusted. TabArena v0.1
  dataset; the shipped notebook and collection pin are unchanged. See `curation/records/maternal_health_risk.md`.

- `hepatitis_c_prediction`: rounded `ALB`, `ALT`, `AST`, `BIL`, `CREA`, `GGT`, `PROT` to integers for all rows and
  dropped `ALP`; donor and patient rows were recorded with different precision (and `ALP` is missing only for
  patients), which separated them at AUC 0.9997. 12 -> 11 features. Not built; `report.md` regenerated by
  `dataset check` (0 errors, 0 warnings).

- `heart_failure_followup_survival`: dropped `time` (follow-up days, which end at death or censoring) instead of
  converting it to `month_to_follow_up`; 12 -> 11 features. LightGBM AUC 0.90 -> 0.75.
- `mic`: predict at admission; dropped the 9 ICU day-1..3 columns (`R_AB_*`, `NA_R_*`, `NOT_NA_*`), whose
  missingness encodes death before day 2/3; 111 -> 102 features. Death AUC 0.93 -> 0.91.
- `kickstarter`: dropped the creator's project `profile` (and `profile_blurb`), present only for funded projects;
  and `staff_pick` (can be awarded mid-campaign); the task now simulates predicting at launch. 14 -> 12 features,
  187,118 -> 187,117 rows (one more exact duplicate once the profile is gone). AUC 0.924 -> ~0.886 (leak audit).
- All three: not built; `report.md` regenerated by `dataset check` (0 errors, 0 warnings). See their records.

- `anes_voting_2026`: dropped 57 post-election columns, 318 -> 261 features (not built; `report.md` regenerated by
  `dataset check`, 0 errors, 0 warnings). `VCF1005` is built from the post-election House vote (codes 1/2 exist
  only for voters); `VCF0426`/`VCF0427` list "no Post IW" and 54 `VCF92xx` list "no post data" in the Feb 2026
  codebook, which the "no post IW" filter missed. The 10 of them in `num_cols` were removed from it. LightGBM mean
  AUC on the temporal splits: 0.930 -> 0.855. See `curation/records/anes_voting_2026.md`.

- Removed `prostate_cancer_detection`: retired (`No (Retired)`, `Data Quality Issue`). The label is readable from
  sample-processing artefacts: the m/z < 1 Da channels give AUC 0.83, and two same-label groups (Benign vs NED)
  separate at 0.99; the paper's own 7 features separate those groups at 0.92-0.97 but the label only at 0.62-0.70.
  No batch IDs survive. See `curation/records/prostate_cancer_detection.md`. The shipped BeyondArena notebook and its
  collection pin are unchanged.

## 2026-09-29 (leak audit: retirements)

- Removed `video_game_fps_prediction`: retired (`No (Retired)`, `Trivial` + provisional `AHDS`). The target is a
  CPU × GPU lookup (log FPS = game + CPU + GPU, R² 0.99998) and the grouped split leaves every test CPU and GPU in
  train; Peeters et al. 2021 only assume the fpsbenchmark values are reliable. See
  `curation/records/video_game_fps_prediction.md` and the BeyondArena leak audit (2026-09-24). The shipped BeyondArena
  notebook and its collection pin are unchanged.

## 2026-09-29 (memory, stable ids, load/clean split, record links)

- Memory: `_load_raw`, `_clean` and the dtype cast run under pandas copy-on-write, and `_clean` gets a shallow copy
  of the cached raw data, so a column is copied only when it changes (half the peak memory in a 320 MB test). The
  cached raw data still never changes (tested). No definition uses the chained assignment that copy-on-write
  would silently ignore.
- `_load_raw` / `_clean` split in the 12 definitions that did all their work in `_load_raw`: asp_potassco,
  sat11_hand_algo_runtime, hazelnut, kickstarter, immoscout, miami_housing, qsar_tid_11, rossmann (its unused
  Kaggle test frame removed), polish_companies_bankruptcy, seismic_bumps, video_game_fps_prediction,
  website_phishing. biomechanical, pancreatic, prostate and jm1 already only read.
- Stable anonymous ids: asp_potassco, sat11, video_game_fps_prediction, cardiotocography and musk mapped ids to
  `uuid.uuid4()`, so the data (and, for the grouped ones, the splits) changed on every run. They use the new
  `anonymize_ids` (a hash of each value). New definition check `definition_nondeterministic` rejects random ids and
  unseeded randomness.
- `kickstarter`: ruff's auto-fix had turned `df[df["disable_communication"] == False]` into `df[not ...]` (it fails
  on a Series); restored as `.eq(False)`. E711/E712 are now unfixable in `pyproject.toml`, so `ruff --fix` cannot
  rewrite a pandas comparison again.
- Records point at both: `notebook_path` (the BeyondArena notebook) and the new `v2_path` (the definition here),
  filled by `sync-notebooks` for 141 records; the dashboard links it with 🧩.

## 2026-09-29 (temporal splits declared; decisions)

- The 17 migrated temporal datasets declare `TemporalSplits` instead of hand-written `_make_splits` (not run).
  `hotel_booking_demand` stays custom (its as-of-date filtering; open with the leak audit). Expected differences:
  - `climate_model_weather_forecasting_1m`, `cooking_time_1m`, `delivery_eta_1m`, `maps_router_eta_1m`: the test
    window is the last 7 calendar days (v1 took from `max().normalize() - 1 week`, 8 calendar days);
  - `sberbank_housing_market_forecasting`: 5 contiguous calendar 6-month windows (v1's first window was open-ended
    and `DateOffset(day=1)` left a few days in no window);
  - `california_house_prices_2020`, `mercedes_benz_greener_manufacturing`, `kickstarter`, `sf_permit_time`: the newest
    window is now split 0 (v1 was oldest first, the `splits_temporal_order` warning);
  - `home_credit_default_stability_1m`, `ghanas_indigenous_intel`: the frame is now sorted by time (v1 was not);
  - `kickstarter`: the split cell had added a `year` column (`to_period("Y")`, from exploration) to the data; gone;
  - `ieee_fraud_detection`: `time_horizon` is the integer 1 (was the string "1");
  - the others (anes, coffee, consumer_complaints, garments, ieee, rossmann, home_credit windows) should match.
- `covertype`: `splits_test_over_budget` accepted (one whole wilderness area, 257,015 test rows).
- `pva_revenue_prediction_kddcup98`: removed the regression alternative notebook; the shipped classification task
  is the folder's `dataset.py` (the regression notebook stays in `datasets/beyond_iid/` as history).

## 2026-09-29 (all datasets in the v2 format)

- Dtypes are a hook, not class attributes: `_feature_types(df)` returns `FeatureTypes(categorical=..., string=...,
  datetime=...)` for the cleaned frame (a classification target is a category without being listed), and column
  drops happen in `_clean` (`drop_columns(df, [...])` fails on a misspelled name). The five pilots were rewritten
  and give the checksums of their reports (lending_club_1m then changed, below).
- Converted the other 136 notebooks with `scripts/v2/migrate_notebook_to_v2.py` (not run; each folder keeps its
  v1 notebook until `scripts/v2/check_equivalence.py` has checked it). All 141 definitions import and pass ruff.
  The `_1m` notebooks moved to `<name>_1m/` folders. `pva_revenue_prediction_kddcup98/dataset.py` is the shipped
  classification task (`_clf.ipynb`). `rossmann_store_sales` declares `time_horizon = 42`.
- `home_credit_default_stability_1m`: `run_large_data_preprocessing.py` is now `_prepare_raw_files` (reads from
  `raw_dir`, loguru and prints removed). `sberbank_housing_market_forecasting`, `labour_inspection_compliance`,
  `ieee_fraud_detection`: sibling files are read from the definition's folder, not the working directory.
- `lending_club_1m`: drops the joint-applicant fields, which are only filled from 2017 on while this version keeps
  loans up to 2016 (checked on the raw file; not a join bug). The report has no warnings left.
- Library: a sub-sampled temporal frame is sorted by time again (no `task_time_on_not_sorted` warning);
  `raw_data_from` points a dataset at another dataset's raw files; `CuratedContainer.save()` defaults to the
  resolved warehouse (`$DATA_FOUNDRY_WAREHOUSE`). CI lints `datasets/_dev/tabarena-v0pt2/*/dataset.py`.
- Not built; the shipped containers are unchanged.

## 2026-09-29 (v2 API: flat attributes and standard steps)

- The v2 dataset class now declares everything as flat class attributes (`unique_name`, `year`, `source`,
  `download_description`, `bibtex`, `target`, `problem_type`, ...). Multi-line text is indented like code and
  dedented; the BibTeX key is parsed from the entry; the regime data tags, the metric (roc_auc / log_loss / rmse)
  and stratifying on a classification target are defaults.
- Reading and cleaning are two hooks: `_load_raw` (cached, so edits to the cleaning never re-read the files) and
  `_clean`. After `_clean` the base class drops `drop_columns`, casts `categorical_features` / `string_features` /
  `datetime_features` (unused categories removed), and fixes the row order: a stable sort by `time_on` for temporal
  tasks, else a shuffle with seed 42. The shuffle seed (42) and the split seed (4267) are fixed in the base class.
- Temporal splits are declarative: `TemporalSplits(window, unit, n_windows, step, gap, cutoffs,
  min_train_fraction)` on the new `curation_recommendations.get_temporal_window_splits`, with a generated splits
  comment and, for calendar windows, the horizon. Default splits get one comment, "Default splits.".
- `_prepare_raw_files` replaces `_prepare_raw`: the acquire_valued_shoppers_challenge polars step is now a method of
  its class (`run_large_data_preprocessing.py` removed) and reads from `raw_dir`.
- New optional hook `_decisions(raw, df)`: decisions with a table or a figure, rendered into `report.md`
  ("Decisions", figures under `report/`). `kick` has the first two.
- `explore.ipynb` starts with `ds = workbench()`, which reloads `dataset.py` on every edit and keeps the raw cache.
- Metric names are canonical (`task_metric_not_canonical`, an error, for aliases such as `root_mean_squared_error`
  or `MAPE`). `5g_energy_consumption.ipynb`: `objective_metric_name="MAPE"` -> `"mape"`.
- The five pilots are rewritten in this form. Checked with `scripts/v2/check_equivalence.py` against the notebooks
  they came from (recovered from git), which now compares content (rows as a multiset, dtypes, fold sizes,
  normalised metadata):
  - `airfoil_self_noise`, `early_learning_predictors`, `acquire_valued_shoppers_challenge`: same content.
  - `kick`: same rows; the 9 windows of 28 purchase dates are now anchored at the newest date (v1 anchored them at
    the oldest), so the fold sizes differ slightly.
  - `lending_club_1m`: same 1,310,259 rows before splitting; the stable time sort orders ties differently, so the
    capped test side draws other rows. The declarative split also fixes the discarded train positions.
- Not built; the shipped containers are unchanged.

## 2026-09-29 (v2 dataset folders: pilot)

- New format, `data_foundry.v2`: a dataset is a folder with `dataset.py` (one `AbstractCuratedDataset` subclass: the
  metadata as class attributes, the preprocessing in `_load`, hand-built splits in `_make_splits`), a free-form
  `explore.ipynb`, and a `report.md` generated by `data-foundry-curation dataset check` (no save, no UUID) or
  `dataset build` (saves; records UUID, checksum and git commit in the frontmatter). Scaffolding is the
  `/add-dataset` skill, which replaces `/process-dataset`.
- Converted five pilot datasets with `scripts/v2/migrate_notebook_to_v2.py` and removed their notebooks:
  `airfoil_self_noise` (IID), `early_learning_predictors` (grouped), `kick` (temporal),
  `acquire_valued_shoppers_challenge` (temporal, `_prepare_raw` runs `run_large_data_preprocessing.py`) and
  `lending_club_1m` (the folder is now `lending_club_1m/`, not `lending_club/`).
- Logic unchanged: `scripts/v2/check_equivalence.py` builds each definition and runs the old notebook, and all five
  give the notebook's container checksum (frame, dtypes, metadata and splits). The polish after conversion removed
  dead code (kick's unused test frame and analysis column), diagnostic prints and duplicated seeds only, and was
  re-checked the same way. Exploration cells moved to `explore.ipynb` (kick's recompute the analysis column there).
- A `_1m` definition reads its raw files from the folder of the dataset it was made from
  (`<warehouse>/lending_club/`); the v1 notebook read `<warehouse>/lending_club_1m/`, which does not exist.
- Not built; the shipped containers are unchanged.

## 2026-09-29 (one notebook per sub-sampled dataset)

- A `<name>_1m.ipynb` notebook is the sub-sampled version of a dataset (`unique_name="<name>_1m"`,
  `version_from_unique_name`, `version_comment`) and the only notebook in its folder. Removed the ten full-size
  siblings it replaced: `amex_non_iid`, `climate_model_weather_forecasting`, `consumer_complaints`, `cooking_time`,
  `delivery_eta`, `home_credit_default_stability`, `lending_club`, `maps_router_eta`, `mercari_price_suggestion`,
  `sepsis_prediction` (their originals remain in `datasets/beyond_iid/`).
- `electric_motor_temperature_prediction` is sub-sampled now, so it became `electric_motor_temperature_prediction_1m`
  (new `unique_name` and version fields; like every `_1m` notebook it reads its raw data from
  `<warehouse>/electric_motor_temperature_prediction_1m/`).
- The IID and grouped `_1m` notebooks (`amex_non_iid_1m`, `sepsis_prediction_1m`, `mercari_price_suggestion_1m`,
  `electric_motor_temperature_prediction_1m`) now build the template's recommended single split and sub-sample it with
  `curation_recommendations.subsample_split_to_budget` (whole customers / patients / profiles; rows for mercari),
  replacing a hard-coded split with hand-written group sub-sampling (amex, sepsis) and a 1.25M-row sample before
  splitting (mercari). Checked on the shipped data: all within 1M train / 250k test rows (amex was 1,000,350 train;
  sepsis 258,511 and electric motor 327,320 test), no group on both sides. The temporal `_1m` notebooks already use
  `subsample_temporal`.
- Library: `subsample_split_to_budget` added; `get_recommended_splits_dimensions` now recommends the single split for
  every dataset of 1.25M rows or more, also when it counts groups (per-group labels).
- Not re-run; the shipped containers are unchanged.

## 2026-09-29 (one split seed)

- One split seed everywhere: every notebook that builds splits defines `split_random_state = 4267` (the library's
  `SPLIT_RANDOM_STATE`), passes it to `get_recommended_iid_splits` / `get_recommended_grouped_splits` /
  `subsample_temporal` and to any sklearn splitter, and records it in `PredictiveMLSplitsMetadata(split_random_state=...)`
  (131 notebooks). Before, the IID single train/test split ignored the seed and used 42, `subsample_temporal` defaulted
  to 42, and the hand-built splitters used 42 (`amex_non_iid`, `sepsis_prediction`) or 43 (`sepsis_prediction_1m`).
- Re-running a notebook gives a different split than the shipped container where the seed changed:
  `mercari_price_suggestion(_1m)` and `amex_non_iid_1m` (42 → 4267), the 7 temporal `_1m` notebooks that call
  `subsample_temporal` (42 → 4267) and `sepsis_prediction_1m` (43 → 4267). All other IID/grouped splits are
  unchanged: 118 of the 120 shipped ones were regenerated exactly from their shipped data.
- Not re-run; the shipped containers are unchanged.

## 2026-09-29 (metadata fixes)

- `micro_mass`: set `objective_metric_name="log_loss"` (was empty, a bundle-check error). It is TabArena's default for
  multiclass tasks, so runs already fell back to it, and 23 of the 25 multiclass BeyondArena datasets use it.
- `rossmann_store_sales`: declared `time_horizon=42`, `time_horizon_unit="days"` (was missing, a bundle-check error).
  The split code already uses 42-day test windows with a 1-day planning gap, following the competition's "predicting
  their daily sales for up to six weeks in advance".
- Both pass `run_bundle_checks` on the shipped containers with the corrected metadata; not re-run or re-saved.

## 2026-09-29 (template update)

- Brought all 152 notebooks in line with `datasets/_template/_template.ipynb` without touching preprocessing or split
  logic: `run_all_checks(problem_type=task_mold.problem_type)` instead of `classification=...`; the single export cell
  replaced by the template's *Bundle* (`describe()`), *Bundle Checks* (`run_bundle_checks(...).raise_if_errors()`) and
  *Export* (`save()` + `verify_saved_container`) cells; heading typos fixed in `cardiotocography` and
  `coffee_rating_prediction`.
- `give_me_some_credit`: `RevolvingUtilizationOfUnsecuredLines` is numeric again (it was cast to a ~126k-level
  category).
- `allstate_claims_severity`: closed the unbalanced brace after `\url{...}` in the BibTeX.
- `sepsis_survival_minimal_clinical_records`: removed the stray `"` around the BibTeX entry and set
  `academic_reference_bibtex_key` to `chicco2020survival` (was `hicco2020survival`).
- `blood_tests_drink_prediction`: set the empty `academic_reference_bibtex_key` to `UCILiverDisorders2016`.
- These notebooks have not been re-run; the shipped containers are unchanged.

## 2026-09-29

- Created the folder from `datasets/beyond_iid/` at commit `72c30d4`: 141 dataset folders, one per dataset, without
  the `new_iid` / `old_iid` / `temporal` / `grouped` level. Each folder has the same files as its source folder
  (shipped notebook, sibling runs, helper files); notebook outputs and execution counts are cleared.
- Removed `homeq_default_prediction`: retired on 2026-09-24 (`No (Retired)`, class-conditional generation artefacts;
  see `curation/records/homeq_default_prediction.md` and `curation/audits/beyondarena_leak_audit_2026-09-24.md`).
