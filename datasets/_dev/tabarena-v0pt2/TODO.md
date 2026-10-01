# TODO: TabArena v0.2 working copy

Open work for this folder. When an item is done, remove it here and log the change in [`CHANGELOG.md`](CHANGELOG.md).

## Needs a decision

- [x] **`hotel_booking_demand`: `splits_temporal_leakage`**: resolved 2026-09-30 (training now uses only bookings arriving before each prediction point; see its record).

## Verify the migration (runs the data)

- [ ] **Check the 136 migrated definitions** against the v1 notebook each folder still holds:
  `scripts/v2/check_equivalence.py <folder>/<name>.ipynb <folder>` must report `SAME CHECKSUM` or `SAME CONTENT`;
  then `data-foundry-curation dataset check <folder>` (writes `report.md`) and remove the v1 notebook. Known
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
- [ ] **Build the v0.2 containers** (`dataset build`, new UUIDs) once the definitions are checked.

## Clean-up after the check

- [ ] **Move column drops and casts by hand** where the migrator could not lift a cast into `_feature_types`
  (casts before code that depends on the dtype), and replace the list-and-loop string casts with `string=[...]`.
