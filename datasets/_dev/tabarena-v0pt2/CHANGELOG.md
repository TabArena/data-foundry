# Changelog: TabArena v0.2 working copy

Every change to this folder gets an entry here, newest first: edited notebooks or helper files, added or removed
datasets, and re-runs that produce a new container (give the new UUID). Say what changed and why, and link the
record, audit or PR that motivated it.

## 2026-09-30 (leak audit: retirements)

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
