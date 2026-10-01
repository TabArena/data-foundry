# TODO: TabArena v0.2 working copy

Open work for this folder. When an item is done, remove it here and log the change in [`CHANGELOG.md`](CHANGELOG.md).


## Verify the migration (runs the data)

- [ ] **Check the 136 migrated definitions** against the v1 notebook each folder still holds:
  `scripts/v2/check_equivalence.py <folder>/<name>.ipynb <folder>` must report `SAME CHECKSUM` or `SAME CONTENT`;
  then `data-foundry-curation dataset check <folder>` (writes `README.md`) and remove the v1 notebook. Known
  differences to expect and review:
  - datasets the v1 notebook did not shuffle (the `# MIGRATE:` note at the end of their `dataset.py`): v2
    shuffles them unless `shuffle = False` is set with a reason;
  - `hiva_agnostic` shuffled with seed 11; v2 uses 42;
  - the grouped datasets that shuffled and then sorted by group (dementia, micro_mass, musk, parkinsons,
    telemonitoring) lose that sort;
  - unused categories are removed; the default split comment is "Default splits."; metadata text is dedented;
  - the temporal datasets now declare `TemporalSplits` (see the changelog): compare their windows, not a checksum.
- [ ] **Run `_prepare_raw_files` once from scratch** for `acquire_valued_shoppers_challenge` and
  `home_credit_default_stability_1m` (moved from `run_large_data_preprocessing.py` into the classes; checked so far
  only for acquire, against the existing `merged_input_data.parquet`).
- [ ] **Re-check the 4 IID / grouped datasets the v2 split protocol changes** (`dataset check`, look at the new
  splits; the 7 temporal ones are done): `mercari_price_suggestion` and `electric_motor_temperature_prediction` (now
  taken fully; their folders still hold the old `_1m` v1 notebook, which no longer matches, so skip
  `check_equivalence.py` and remove the notebook after the check), `amex_non_iid_1m` and `sepsis_prediction_1m`. The
  README of `sepsis_prediction_1m` is stale until then. `telemonitoring_parkinsons_biomedical_voice_measurements` (new row
  selection), `sat11_hand_algo_runtime` (unsolved instances dropped) and `covertype` (IID on the full data) no longer
  match their v1 notebooks either (checked); remove those notebooks after review.
- [ ] **Build the v0.2 containers** (`dataset build`, new UUIDs) once the definitions are checked.


## Decide

- [ ] **`telemonitoring_parkinsons_biomedical_voice_measurements`: no signal across subjects** (R^2 below 0 for every
  model on the grouped splits, 0.75 on random splits; `GROUPED_DATA_PLAN.md`, section 10). Retire it, or recast it as
  warm-start tracking with a custom `_make_splits`.

## Later (deferred in the grouped-data revision)

- [ ] **A check for hidden groups in IID tasks**: id-like columns whose values repeat with clustered labels. Needs a
  pass over the 114 IID datasets to calibrate and review its hits.
- [ ] **asp_potassco_classification: keep the 11 configuration runtimes as metadata** (not features), so the
  benchmark can score PAR10 instead of the noisy fastest-configuration label.
- [ ] **sat11_hand_algo_runtime: split by instance family?** The instances come in 48 families (74% of nearest
  neighbours in the same family); the split holds out instances, as ASlib does. Splitting by family needs a split
  group (family) that differs from the selection unit (instance).
