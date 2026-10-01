# TODO: TabArena v0.2 working copy

Open work for this folder. When an item is done, remove it here and log the change in [`CHANGELOG.md`](CHANGELOG.md).


## Decide

- [ ] **Resolve the task-probe flags of the v0.2 build** ([`TASK_PROBES.md`](TASK_PROBES.md), 24 open datasets;
  telemonitoring was retired): `no_signal` for clock_protein_toxicity (ROC AUC 0.51), forest_fires (R^2 -0.04) and
  asp_potassco_classification (macro ROC AUC 0.65, but no log-loss skill); `solved` for eryhemato_squamous_disease
  (macro ROC AUC 0.999 with a linear model); `one_feature` for california_house_prices_2020 (`Listed Price`),
  aps_failure (`ck_000`), fitness_club, parkinsons and sepsis_survival_minimal_clinical_records; `no_spread` for 13,
  mostly small or text-heavy tasks (mercari's text is not probed). For each: keep with a reason in the curation
  comments, fix, or retire.

## Later (deferred in the grouped-data revision)

- [ ] **A check for hidden groups in IID tasks**: id-like columns whose values repeat with clustered labels. Needs a
  pass over the 94 IID datasets to calibrate and review its hits.
- [ ] **asp_potassco_classification: keep the 11 configuration runtimes as metadata** (not features), so the
  benchmark can score PAR10 instead of the noisy fastest-configuration label.
- [ ] **sat11_hand_algo_runtime: split by instance family?** The instances come in 48 families (74% of nearest
  neighbours in the same family); the split holds out instances, as ASlib does. Splitting by family needs a split
  group (family) that differs from the selection unit (instance).

## Library follow-ups (from the framework review of 2026-10-01)

- [ ] **Categorical details in `dtypes.json` and the checksum.** `dtypes.json` stores only `"category"`: integer
  categories with NaN come back as float categories (the build's verify catches it), and an unordered categorical in
  a custom order is re-sorted on load without notice. The checksum does not see category order, `ordered`, unused
  categories or the string storage. Store the categories and `ordered`, and add them to a versioned checksum
  (`v2:<hex>`, so old checksums keep verifying).
- [ ] **Index and test set.** The checksum hashes the index but `save` drops it (require a `RangeIndex`); the
  unlabeled `test_dataset` is not in the checksum and is saved with its index.
- [ ] **`verify_saved_container`**: compare dtypes per column (`CategoricalDtype` equality), then values ignoring the
  string storage; today string[pyarrow] vs string[python] is a false alarm and a category reorder passes.
- [ ] **Collections**: pin the Hugging Face revision, make the cache lookup require the core files, add
  `get_dataset(..., verify=True)`, and look up a `_1m` version by its own name (11 BeyondArena entries).
- [ ] **pandas 3**: a frame built under pandas 3 records `str` dtypes, which pandas 2 restores as `'None'` strings.
  Build in the locked environment (pandas 2.3.3) until the dtype file handles it.
- [ ] Smaller: make `save` atomic (write to a temporary folder, then rename), reject non-string column names, let
  `load` skip extra `a.b.json` files, and tighten `time_horizon_unit` and the split id checks.
- [ ] **Row order from content (option).** The base class could sort every frame by a row hash before the time sort
  or the shuffle, so no `_clean` order (a polars join, a file listing) could leak into a container. It would also
  reshuffle the folds of every IID dataset against the shipped versions, so it was not done in the 2026-10-01 review;
  the definition check (`definition_nondeterministic`) covers the known sources instead.
- [ ] **Prepared raw files are reused when stale**: `_prepare_raw_files` runs only when a file is missing, so an
  edited method keeps the old intermediate file. Record a hash of the method (and its helpers) next to the file.
- [ ] **Test set dtypes**: the categories of an unlabeled `test_dataset` are cast from the test frame alone, so they
  can differ from the training frame's (latent: no definition returns a test set).
- [ ] **Packaging**: the v2 splits need scikit-learn (`GroupKFold(shuffle=)`, 1.6 or later), which is only in the
  test and dev extras; pandas is unpinned, and pandas 3's `str` dtype changes `select_dtypes("object")`. Decide on a
  runtime dependency and a `pandas<3` pin before the release.
- [ ] **Multi-column groups**: refused at import since 2026-10-01 (the split code took them as 2-D groups). Support
  them with one group key (`groupby(cols).ngroup()`) if a dataset needs it.
- [ ] Smaller: a timezone-aware time column with `cutoffs` raises; integer epoch columns cast to 1970 dates;
  `anonymize_ids` gives `1` and `"1"` the same code; the frontmatter's `n_features` counts the group column.
