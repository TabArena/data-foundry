# TODO: TabArena v0.2 working copy

Open work for this folder. When an item is done, remove it here and log the change in [`CHANGELOG.md`](CHANGELOG.md).


## Later (deferred in the grouped-data revision)

- [ ] **A check for hidden groups in IID tasks**: id-like columns whose values repeat with clustered labels. Needs a
  pass over the 94 IID datasets to calibrate and review its hits.
- [ ] **asp_potassco_classification: a selection version once TabArena scores at the group unit** (decided
  2026-10-06; it replaces the classification version, not added next to it). One row per instance and configuration
  with its runtime, `Grouping(prediction_unit="group", aggregation="select_min")` per instance, scored by PAR10, as
  sat11_hand_algo_runtime does. The classification label is noisy (for 62% of instances the second-best configuration
  is within 1 s of the best), while the choice matters on hard instances (PAR10 534 s for the single best
  configuration, 21 s for each instance's best). The record has the numbers.
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
- [ ] Smaller: make `save` atomic (write to a temporary folder, then rename), reject non-string column names, let
  `load` skip extra `a.b.json` files, and tighten `time_horizon_unit` and the split id checks.
- [ ] **Prepared raw files are reused when stale**: `_prepare_raw_files` runs only when a file is missing, so an
  edited method keeps the old intermediate file. Record a hash of the method (and its helpers) next to the file.
- [ ] **Test set dtypes**: the categories of an unlabeled `test_dataset` are cast from the test frame alone, so they
  can differ from the training frame's (latent: no definition returns a test set).
- [ ] **Multi-column groups**: refused at import since 2026-10-01 (the split code took them as 2-D groups). Support
  them with one group key (`groupby(cols).ngroup()`) if a dataset needs it.
- [ ] Smaller: a timezone-aware time column with `cutoffs` raises; integer epoch columns cast to 1970 dates;
  `anonymize_ids` gives `1` and `"1"` the same code; the frontmatter's `n_features` counts the group column.
