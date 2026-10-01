# Leak audit for TabArena v0.2

Audit of the 142 BeyondArena datasets for target leaks, generation artefacts and splits that do not match the task,
24 September to 1 October 2026. The 142 include 49 of the 51 TabArena v0.1 datasets (`anneal` and `diabetes` are not
in BeyondArena and were not audited). The changes are in this working copy and logged in [`CHANGELOG.md`](CHANGELOG.md);
this file is the short version for the benchmark team and the tech report.

## Summary

- 40 of the 142 datasets needed action: 12 are removed, 21 changed (features, rows or split), 7 kept as they are with
  a documented note. The other 103 showed no leak.
- By severity: 21 large, 9 medium, 7 small or no leak, and 3 kept although they affect results (below).
- The working copy now holds 130 datasets, 44 of them from TabArena v0.1.
- Built on 2026-10-02 as container format 2: every dataset of the working copy has a new container and UUID (the table in
  [`README.md`](README.md)); the shipped BeyondArena containers are unchanged. Results on the changed datasets are not
  comparable with earlier TabArena v0.1 or BeyondArena results.
- One scoring change is needed: `sepsis_prediction_1m` (below).

Severity:

- Large: the leak or artefact explains much of the shipped score, or the data cannot support the task.
- Medium: a real leak, a wrong split or a biased test window; the shipped score is optimistic or biased, but the task
  is sound once fixed.
- Small: a confirmed but tiny effect, or no leak.

Scores are from untuned LightGBM on the shipped splits, before and after the fix. They compare versions of a dataset
and are not leaderboard numbers. In the "From" column, TabArena v0.1 means the dataset was in TabArena v0.1 (and in
BeyondArena); BeyondArena means BeyondArena only.

## Removed (12)

| Dataset | From | Severity | Why |
|---|---|---|---|
| `homeq_default_prediction` | BeyondArena | Large | Generated data with class-conditional artefacts: each row's distance to its nearest neighbour alone gives AUC 0.92 (full model 0.975). |
| `video_game_fps_prediction` | BeyondArena | Large | The target is a lookup of the inputs (log FPS = game + CPU + GPU, R² 0.99998), and every test CPU and GPU is in train. |
| `prostate_cancer_detection` | BeyondArena | Large | The label is readable from sample-processing artefacts: the m/z < 1 Da channels alone give AUC 0.81-0.85, and two groups with the same label separate at 0.997. No batch ids survive to correct for it. |
| `iranian_churn` | BeyondArena | Large | Each churner's feature window ends at the churn month, so the task detects customers who are already leaving (AUC 0.986). There are no dates to rebuild a common prediction point. |
| `customer_satisfaction_in_airline` | TabArena v0.1 | Large | The passenger ratings are generated (rating columns copied from one another within customer segments), and the shipped file is a manipulated copy (14,659 labels flipped by a rule on a dropped column). AUC 0.994. |
| `ecommerce_shipping` | TabArena v0.1 | Large | Generated: `Warehouse_block` is `ID mod 6` with no exception in 10,999 rows, the target comes in two ID blocks, and the source cannot be traced. |
| `maternal_health_risk` | TabArena v0.1 | Large | Only 416 of 1,014 feature vectors are unique, and 74% of test rows have an exact copy in train (AUC 0.94 → 0.80 with copies on one side). The real groups (six collection sites) are not in the file. |
| `hazelnut_spread_contaminant_detection` | TabArena v0.1 | Large | The 2,400 rows are repeated scans of about ten physical set-ups, so random splits put scans of one set-up on both sides. The set-up label was never released. |
| `seismic_bumps` | TabArena v0.1 | Large | The rows are consecutive mining shifts, and the shipped IID split trains on every period (AUC 0.75 IID vs about 0.6 forward in time). As a temporal task each test window holds 0-5 positives. |
| `mice_protein_trisomy_discriminant` | BeyondArena | Large | Not a leak: no predictive target. The 8 classes are the experimental design (genotype, training protocol, injection), known for every mouse; the learning outcome was never measured. The protocol part is separated perfectly (AUC 1.0 per mouse). |
| `telemonitoring_parkinsons_biomedical_voice_measurements` | BeyondArena | Medium | Not a leak: no signal across subjects. 88% of the UPDRS variance lies between the 42 subjects and the voice features barely track it (the best model is about 2% better than the mean on unseen subjects); tracking a known patient is dominated by the baseline visit (RMSE 6.33 with voice against 6.48 for the baseline plus drift). |
| `ghanas_indigenous_intel` | BeyondArena | Medium | Not a leak: the 10,928 rows are 626 farmer-days, each test window holds rain from 3-6 farmer-days, and "no rain" likely mixes no rain with no measurement. Retired for now. |

## Changed: large and medium issues (18)

| Dataset | From | Severity | Problem | Fix | Before → after |
|---|---|---|---|---|---|
| `heart_failure_followup_survival` | BeyondArena | Large | `time` is the follow-up period, which ends at death or censoring | dropped | AUC 0.90 → 0.75 |
| `anes_voting_2026` | BeyondArena | Large | 57 columns recorded after the election (e.g. `VCF1005`, built from the post-election House vote) | dropped (318 → 261 features) | AUC 0.930 → 0.855 |
| `hepatitis_c_prediction` | BeyondArena | Large | donors and patients were recorded with different number precision; the formatting alone separates them at AUC 1.000 | 7 lab columns rounded for all rows, `ALP` dropped | log loss 0.27 → 0.35 |
| `sdss_17` | TabArena v0.1 | Large | `redshift` is fitted together with the class (STAR vs rest AUC 0.998 alone); `plate` and `fiber_ID` encode the targeting program; deduplicating on a float-rounded id removed 21,947 distinct objects | photometric task: these columns dropped, deduplicated on sky position (78,053 → 99,999 rows) | log loss 0.13 → about 0.33 |
| `online_shoppers_purchasing_intention_dataset` | TabArena v0.1 | Large | in February-May every buyer has `PageValues` > 0 (alone AUC 0.974), likely because it includes the session's own purchase | February-May sessions dropped (12,330 → 6,875 rows) | `PageValues` alone 0.974 → 0.814 |
| `hotel_booking_demand` | BeyondArena | Large | training rows included future arrivals already known to be cancelled (100% cancelled), and 3 columns are recorded after the prediction point | training limited to bookings arriving before the prediction point; columns dropped | log loss 1.7 (worse than the 0.44 prior) → 0.33 |
| `in_vehicle_coupon_recommendation` | TabArena v0.1 | Large | the same respondents in train and test | grouped split on a respondent id rebuilt from the raw file (587 respondents), a cold-start task | AUC 0.83 → 0.75 |
| `emscad` | BeyondArena | Large | reposts of the same ad, and ads of the same poster, on both sides of the split | reposts dropped, grouped split by poster (4,441 groups) | AUC 0.99 → 0.94 |
| `kickstarter` | BeyondArena | Large | the creator profile exists only for funded projects (0 of 69,970 failed ones have it); `staff_pick` can be awarded mid-campaign | both dropped; the task predicts at launch | AUC 0.924 → 0.886 |
| `mic` | TabArena v0.1 | Large | the ICU day 1-3 columns are blank for patients who died earlier (95% deaths when missing, base rate 16%) | admission-time task, 9 columns dropped | log loss 0.454 → 0.508 |
| `wine_quality` | TabArena v0.1 | Large | 18% of rows are exact copies (features and score), so a row's twin is often in train | duplicates dropped (6,497 → 5,320 rows) | R² 0.46 → 0.37 with copies on one side |
| `jm1` | TabArena v0.1 | Medium | 25% of rows share their code-metric vector with another row, 176 of them with the other label | exact copies and conflicting vectors dropped (10,885 → 8,736 rows) | AUC 0.743 → 0.727 with copies on one side |
| `garments_worker_productivity` | BeyondArena | Medium | `incentive` is paid for the same day's output | lagged by one working day | RMSE 0.134 → 0.140 |
| `mutual_funds_india` | BeyondArena | Medium | the star rating is computed partly from the 3-year return that is the target | dropped | R² 0.811 → 0.783 |
| `biogeographical_ancestry_prediction` | BeyondArena | Medium | the Turkey class comes from another source with an assay artefact at one SNP (it separates the class at AUC 0.96-0.98) | class and 2 SNPs dropped (10 → 9 classes) | not measured |
| `california_house_prices_2020` | BeyondArena | Medium | the "temporal" split followed alphabetical address order (a deduplication step had reordered the rows) | sorted back to sale order | not measured |
| `consumer_complaints_1m` | BeyondArena | Medium | right-censored test window: complaints still in progress were filtered out, 7-70% of Oct-Dec 2025 | rebuilt from the CFPB FOIA archive with settled labels (the live download lost its narratives on 2026-09-14) | not measured |
| `sf_permit_time` | BeyondArena | Medium | right-censored target: recent filings miss their slow permits (2025 p90 97 days, about 300 before) | permits filed before 2024 only; 9 half-year windows | not measured |

## Kept, but they affect results (3)

| Dataset | From | Issue | Why kept |
|---|---|---|---|
| `homesite_quote_conversion` | BeyondArena | Possible leak: `PropertyField37` × `PersonalField12` may be a post-quote status code (AUC 0.965 → 0.915 without it) | anonymised fields the host set up for its own competition; revisit if they get documented |
| `kick` | BeyondArena | Possible leak: missing `WheelType` (70.5% bad buys, 9.7% otherwise) may have been blanked after the purchase (AUC 0.757 → 0.691 without it) | the company released the data this way |
| `sepsis_prediction_1m` | BeyondArena | Evaluation leak, not a data leak: test patients have complete records, and septic records end shortly after onset | needs a scoring change, planned: causal per-patient predictions scored with the PhysioNet 2019 utility |

## What changes for TabArena v0.2

- 130 datasets: the 142 BeyondArena datasets minus the 12 removed. 44 of the 51 TabArena v0.1 datasets remain (5
  removed, 2 never in BeyondArena).
- 21 datasets changed through the audit, 7 of them from TabArena v0.1 (the 6 above plus `diabetes_130_us`). Their
  v0.2 results are not comparable with earlier results.
- Every dataset is now a v2 definition (`dataset.py` with a generated `README.md`); see Appendix B for the other
  changes that move splits.
- Every dataset gets several folds: 3-fold cross-validation, or at least 3 temporal windows, with at most 1M train
  and 500k test rows per split. Only data over that budget is sub-sampled (IID and grouped frames to 1.5M rows,
  temporal data per window), so the largest datasets now have 3 folds instead of one 1M / 250k split. `mercari_price_suggestion` and
  `electric_motor_temperature_prediction` are taken in full. `lending_club` keeps only the 36-month loans issued up
  to 2015, the only loans with complete labels (the source holds only loans finished by 2018Q4), and tests on the
  quarters 2015 Q2-Q4. Not built yet.
- New datasets get the same checks: the leak probes ([`scripts/v2/leak_probes.py`](../../../scripts/v2/leak_probes.py))
  and the audit's precedents ([`leak_checks.md`](../../../.claude/skills/check-candidate/references/leak_checks.md))
  are part of the curation skills.

## Appendix

### A. Small fixes and no-leak findings (7)

| Dataset | From | Finding | Action |
|---|---|---|---|
| `santander_customer_transaction_prediction` | BeyondArena | 400 `has_one`/`has_zero` features computed from the labels of all rows, test folds included | dropped (AUC 0.903 → 0.896) |
| `diabetes_130_us` | TabArena v0.1 | 1,545 encounters ended in death or hospice and cannot be readmitted | the paper's cohort (71,518 → 69,973 rows) |
| `coffee_rating_prediction` | BeyondArena | the oldest of 5 six-month windows trained on 44% of the rows | 13 two-month windows, train ≥ 50% |
| `cirrhosis_patient_survival_prediction` | BeyondArena | the target uses deaths only | kept: survival time without censoring, by design |
| `home_credit_default_risk` | BeyondArena | the feature selection ran on the full labelled set | kept (slight optimism); definition restructured, same data |
| `ieee_fraud_detection` | BeyondArena | `uid` carries earlier fraud labels forward | kept: legitimate history under the temporal split; dropping it costs 0.001-0.007 AUC |
| `south_africa_coronary_heart_disease` | BeyondArena | measurements were taken after the heart attack | kept: this weakens the signal (dropping them: AUC 0.774 → 0.778) |

### B. Other changes in the working copy

- Format: all 141 notebooks are converted to v2 definitions. The 5 pilots are checked against their notebooks; the
  other 136 are still to be checked before the build.
- Seeds: one split seed (4267) and one shuffle seed (42) for every dataset. This changes the splits of
  `mercari_price_suggestion_1m`, `amex_non_iid_1m`, `sepsis_prediction_1m` and the 7 temporal `_1m` datasets.
- Temporal splits follow one convention: as many splits as an IID task of that size, train ≥ 50%, at least about 50
  test rows per window, and the newest window is split 0.
- Sub-sampled versions are their own `<name>_1m` datasets (8, for data over the row budget). IID and grouped frames
  are sampled to 1.5M rows (whole groups for grouped data) before the 3 folds are built; temporal data is sampled per
  window (each test window up to 500k rows, each train side a random 1M of all earlier rows) (v2 split protocol,
  2026-10-01; the earlier rule was one 1M / 250k split from 1.25M rows on).
- Stable ids: `asp_potassco_classification`, `sat11_hand_algo_runtime`, `video_game_fps_prediction`,
  `cardiotocography` and `musk` drew random ids, so their data, and the grouped splits, changed on every run. They now
  use hashed ids.
- Metadata: `micro_mass` gets the log_loss metric, `rossmann_store_sales` a 42-day horizon, `give_me_some_credit`
  treats its utilisation column as numeric again (it was a 126k-level category, about 0.02 AUC), and several BibTeX
  entries are fixed.

### C. Open

- Flagged in the audit, not fixed yet (no leak):
  - `santander_transaction_value` stores the target as log1p and scores it with rmsle, so the log is applied twice;
  - `heart_disease_va_long_beach` codes missing values as `chol = 0` (about 28% of rows) and `trestbps = 0`;
  - `thyroid_discordant` has an `age` of 455;
  - `heloc` has 588 rows that are -9 in every feature (no bureau record);
  - `sberbank_housing_market_forecasting` cites the Home Credit competition, and
    `cirrhosis_patient_survival_prediction` has "IID" as its licence.
- `homesite_quote_conversion`: 2 bundle-check warnings (13 columns constant after -1 → missing; a `' '` level in
  `GeographicField63`).
- `online_shoppers_purchasing_intention_dataset`: 40 exact duplicate rows remain after the month filter.
- To revisit: `ghanas_indigenous_intel`; `homesite_quote_conversion` and `kick` if their fields get documented;
  `sf_permit_time` with a new download in 1-2 years.

### D. How it was checked

Each dataset was loaded with its shipped splits and probed with untuned LightGBM: the score with and without suspect
columns, each feature alone, missing-value indicators, values that occur with one class only, test rows with an exact
copy in train, nearest-neighbour label agreement, separability of subgroups that share a label, row order, entity
overlap between train and test, rows and positives per test window, and the target by period (censoring). A second,
independent check reran every finding, and the source paper was read before each decision. Per-dataset detail is in
the records' dated `CC (2026-09-30 / 2026-10-01, Lennart)` comments (`curation/records/<name>.md`), in
[`CHANGELOG.md`](CHANGELOG.md) and on the internal audit page (https://claude.ai/artifact/ENjKHNwVU7G9xNw1VoaKnn).
