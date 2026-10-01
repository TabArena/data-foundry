# Changelog: TabArena v0.2 working copy

Every change to this folder gets an entry here, newest first: edited notebooks or helper files, added or removed
datasets, and re-runs that produce a new container (give the new UUID). Say what changed and why, and link the
record, audit or PR that motivated it.

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
