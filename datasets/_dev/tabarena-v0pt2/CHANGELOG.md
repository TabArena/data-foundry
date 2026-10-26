# Changelog: TabArena v0.2 working copy

Every change to this folder gets an entry here, newest first: edited definitions or helper files, added or removed
datasets, and re-runs that produce a new container (give the new UUID). Say what changed and why, and link the
record, audit or PR that motivated it.

## 2026-10-26 (the curator's marks: nba retired, house_prices_nominal copied forward as ames_housing, rain neighbours)

Lennart's marks of 2026-10-26 on the Open Datasets Review page, in two rounds; records carry them as
`CC (2026-10-26, Lennart)` lines. Nothing was rebuilt.

- `nba_players_2016_2019` is retired: `No` with `No Good Target / Scientific Discovery` and `Not Representative`
  (no actor, moment or decision fits; the score ranks the whole ballot). The folder is removed; its claim released.
- `house_prices_nominal` is copied forward as the new record and folder `ames_housing` (De Cock's full Ames file);
  `house_prices_nominal`, the Kaggle competition's 1,460-row half (OpenML 42165), keeps its name as its `Duplicate`.
  In `ames_housing`:
  - the 82 sales between family members, allocations and adjoining-land purchases are dropped (USE-5): 2,837 sales;
  - the text codes of 43 categorical columns become the labels of DataDocumentation.txt (CLEAN-12);
  - no gap between training and test windows, an exception to SPLIT-10 (a Cases row in `splits.md`; this file's
    `REVIEW.md` proposes amending SPLIT-10);
  - the record's `Trivial` marker is removed.
  - `perth_house_prices` and `melbourne_housing_market` now cite `ames_housing` (notes only).
- `house_sales` drops its 85 related-party sales (warning 51), as `ames_housing` drops its family sales: 20,499
  sales. This reopens option (c) of its issue 8 (2026-10-22).
- `2_month_survival_rate_prediction`:
  - adlp, edu and income are dropped (they come from the interview of days 2-7 and their gaps follow early deaths;
    this replaces CC 2026-10-12): 22 features;
  - pafi above 713 is set missing (9 patients);
  - the year is 2003;
  - the use case is SUPPORT's objective estimate set beside the physician's (Knaus et al. 1995), so the physicians'
    estimates and DNR orders are not inputs (a USE-6 Cases row).
- `rain_in_australia`:
  - 26 contiguous 14-day test windows over the last year instead of 9 spaced six weeks apart (16,457 test rows);
  - each row also reads the other locations' 9 am rain, pressure and humidity of the same day where their 9 am comes
    no later than its own (143 columns; CLEAN-19 amended);
  - Rainfall and RainToday stay (TP-10 leg 2 amended: the last observation of the target may stay when it is known
    at the prediction point);
  - rattle's file stays without a patch of the 2016-17 gap; the record's year is 2026.
- `african_credit_scoring_challenge`: the drop of the rows whose lender funds less than 0.5 is confirmed. Open: Type_1
  loans only (issue 1), ROC AUC over Zindi's F1 (issue 6, a consistency check against CC 2026-10-21), Zindi's
  country test (issue 7).
- `glioma_grading_clinical_and_mutation_features`: new issue 6 answers the verdict note; the AI recommends `No`.
- The vocabulary's `No Good Target  / Scientific Discovery` (two spaces) and `2nd Tier / Scientfic Discovery` are
  spelled `No Good Target / Scientific Discovery` and `2nd Tier / Scientific Discovery` in every record (199).
- 2_month_survival_rate_prediction, ames_housing and rain_in_australia have no open issue left: their `REVIEW.md`
  files are removed, and they ship (Lennart, 2026-10-26): `DF: Yes`, claims released. Not built yet.

## 2026-10-23 (claims move to a live board)

- `GETTING_STARTED.md` (section 7) describes the new claims: a branch `claims` of the repository that every curator
  pushes to directly, one file per claimed dataset, so a claim shows within seconds instead of after a claim PR to
  `main`. The tooling is `data-foundry-curation claims` (`src/data_foundry/curation/claims.py`), the dashboard's
  Claimed by column, and a Claude Code hook that warns before an agent edits a dataset another curator holds; see
  `.claude/skills/knowledge-data-foundry/references/claims.md`. The records keep `claimed_by` and the WIP value as a
  mirror of the board.

## 2026-10-22 (numerai28_6 added as forced IID)

- New folder `numerai28_6` (Lennart, 2026-10-22: add as forced IID). It is Numerai's 2016 Kaggle training sample, CC0: 96,320 rows, 21 encrypted features and a binary target.
  - Random 3 x 3 stratified splits tagged `ForcedIIDFromTemporal`, because the release has no era, date or id.
  - The metric is the 2016 tournament's log loss.
  - The folder was built by `/add-dataset` and attacked by the focused review panel (claim audit, split audit):
    - no validity claim was refuted, and four tests find no hidden weekly group;
    - the panel's text fixes are made.
  - `REVIEW.md` asks whether to keep log loss: the models sit within 0.002 of the dummy, and untuned tree models lose to it.
- The README table lists 173 datasets. Not built yet.

## 2026-10-22 (fourth round: framingham to hard ASCVD, sarcoma 4 classes, dataorg retired; last notebooks removed)

Lennart's marks of the late afternoon; records carry them as `CC (2026-10-22, Lennart)` lines. Nothing was rebuilt.

- **framingham_heart_study_fhs:** the target is now `ascvd_within_10_years`: a first hospitalised myocardial infarction
  or CHD death, or a stroke, within 10 years (the outcome of the pooled cohort equations).
  - The 25 participants with a prior stroke are excluded, so `prevalentStroke` is dropped as constant.
  - 4,199 rows, 276 Yes; logistic regression ROC AUC 0.779.
  - `REVIEW.md` is removed.
- **sarcoma:** myxofibrosarcoma and undifferentiated pleomorphic sarcoma are merged, which leaves 4 classes. The IID
  split by patient stays. Random forest log loss goes from 0.650 to 0.469. `problem_type` in the record is now
  multiclass. `REVIEW.md` is removed.
- **dataorg_financial_health_prediction_challenge:** retired, because nothing is known about the target and it is
  survey data. The record is `No` + `No Good Target / Scientific Discovery`, tagged `2nd Tier / Scientific Discovery`,
  with its claim released. The folder is removed and the README table now lists 172 datasets.
- **melbourne_housing_market:** ships. `year` is 2017, the first version of the Kaggle upload. PROV-9 now says a Kaggle
  upload that grew over its versions takes its first year. `REVIEW.md` is removed.
- **thyroid_discordant:** ships. `Trivial` is removed (TP-4). `REVIEW.md` is removed.
- **mobile_churn:** the drop of never-activated SIM cards is confirmed. `REVIEW.md` is removed.
- **Records without a folder:**
  - sasol_customer_retention_recruitment_competition is `No` + `Duplicate` (of expresso).
  - water_quality_and_potability stays `No`, with `AHDS` added.
  - numerai28_6 got an answer: not a duplicate under PROV-6/7, and no hidden-week leak was found. Adding it as
    forced IID waits for the curator's call.
- **The 11 remaining `explore.ipynb` notebooks are removed.** Their findings now sit in the definitions:
  - dated bullets in anes_voting_2026, consumer_complaints_1m, early_learning_predictors, hotel_booking_demand,
    lending_club, micro_mass, rossmann_store_sales and sf_permit_time;
  - a new `Decision` in kick showing that the competition's split is neither temporal nor grouped (the v1 notebook's
    "proof" of a grouped split came from a buggy check).
  - The two lung_cancer notebooks held no usable findings.

## 2026-10-22 (third round: framingham, house_sales; explore.ipynb dropped)

Lennart's marks of the afternoon; records carry them as `CC (2026-10-22, Lennart)` lines. Nothing was rebuilt.

- **framingham_heart_study_fhs:**
  - Applied:
    - `education` now holds its four labels as a category (CLEAN-12).
    - Competing deaths stay No, now a LEAK-22 case.
    - A note names every exam, split by participant, as a possible grouped variant.
    - The record's `year` is 2004.
  - Issue 1 (the endpoint) stays open with an answer: hard ASCVD (heart attack, CHD death or stroke) is the outcome of today's treatment thresholds.
- **house_sales:** the 23 sales with warning 45, 5 or 1 are dropped, because their recorded price is not the house's alone. 20,584 rows. `REVIEW.md` is removed.
- **stock and appliances_energy_prediction** stay retired; the item across datasets is resolved.
- **`explore.ipynb` is no longer part of a v2 dataset folder (Lennart):**
  - `dataset new` scaffolds only `dataset.py`.
  - The template moved to `.claude/skills/knowledge-data-foundry/references/explore_notebook_reference.ipynb` as an optional reference.
  - 162 notebooks that were unchanged from the template are removed.
  - 11 that hold exploration migrated from v1 stay until the curator decides: anes_voting_2026, consumer_complaints_1m, early_learning_predictors, hotel_booking_demand, kick, lending_club, lung_cancer, lung_cancer_epithelial_genexp, micro_mass, rossmann_store_sales, sf_permit_time.
  - The docs and the add-dataset skill describe a folder as `dataset.py`, the generated `README.md`, and `REVIEW.md` while issues are open.
- **Review page:** the header of each dataset shows its feature count next to the row count.

## 2026-10-22 (second round: kick, mortgage, house_sales, huntprohibited, g_research; time-sampled splits)

Lennart answered the consistency checks and the open questions of the first round. Each record carries his decisions
as `CC (2026-10-22, Lennart)` lines. Nothing was rebuilt.

- **kick:** `WheelType`, `WheelTypeID`, `PRIMEUNIT` and `AUCGUART` are dropped under LEAK-10, consistent with
  expresso's REGION. LEAK-38's scope is amended: the rule covers only fields whose timing cannot be tested, and a
  LEAK-10 mechanisms row names both datasets. `REVIEW.md` is removed.
- **mortgage:**
  - The payoff copy of the 7 doubled period-51 loans stays, recorded as an exception to LEAK-20.
  - The 38 balances that put the source's LTV above 300% become missing before lagging (CLEAN-11). The highest lagged
    LTV is now 261.4%.
  - `REVIEW.md` is removed.
- **house_sales (issue 8, option c):**
  - Only the appraiser's judgment codes (46, 7, 8; 360 sales) are dropped; the frame has 20,607 rows.
  - New categorical `sale_condition` from the warnings known before the price.
  - RMSE on log price .1662 overall, .2552 on the flagged sales.
  - New issue 10: 23 sales whose price covers more or less than the house.
- **huntprohibited_1m:** the random split stays (issue 10). `REVIEW.md` is removed.
- **g_research_crypto_forecasting_1m** is kept under an amended TP-10: leg 1 is measured by the declared metric, and leg
  2 now reads "no lag of the target column itself".
  - New framework options in `src/data_foundry/v2/splits.py`:
    - `TemporalSplits(sample_by="time")` sub-samples whole time values to the row budget;
    - `gap_unit` gives the gap its own unit, and the schema's `time_gap_unit` accepts minutes and hours.
  - The definition samples whole minutes over all history, with a 15-minute gap.
  - Its notes give the CLEAN-19 comparison with the other top solutions and no longer recommend `No`.
  - `REVIEW.md` is removed.
  - stock and appliances_energy_prediction are listed in the working copy's `REVIEW.md` for a re-check under the
    amended rule.
- **Review page:** tables in `REVIEW.md` answers now have blank lines around them; they rendered as broken tables
  before. The review file format says so.

## 2026-10-22 (the curator's marks on eight datasets)

Lennart marked eight datasets on the review page. Each record carries his decisions as `CC (2026-10-22, Lennart)`
lines. Marks that depart from a rule or precedent without a fact that sets them apart went back to him as
consistency checks in the folder's `REVIEW.md` and are not applied yet. Nothing was rebuilt.

- **Settled, `REVIEW.md` removed:**
  - `nyc_taxi_trip_duration_1m`: verdict ship; the record's `domain` takes the definition's value.
  - `open_university_learning_analytics_dataset`: the 14-day TMA marking delay and the weight-0 TMA rule stay; kept
    despite `no_spread`, to be re-checked with the first tuned run (a TP-3 cases row and a note).
  - `expresso_churn_prediction_1m`: REGION stays dropped, ARPU_SEGMENT stays, the churn timing ships as a stated risk.
- **mortgage:**
  - Issues 2, 10, 11, 12 and 14 applied:
    - the use case now covers a loan scored from the quarter it joins the book;
    - new `balance_ratio_lag_1_to_2`;
    - Freddie Mac's 30-year rate (FRED MORTGAGE30US, a new raw file) as `market_rate_30y_lag_1`, with
      `rate_minus_market_rate_lag_1`;
    - a note on a possible default-only companion.
  - Log loss 0.1180 / 0.1274 / 0.1293 in periods 60 / 59 / 58, against 0.1201 / 0.1327 / 0.1364 without the ratio.
  - CLEAN-13 is amended for a flag block with a reference level (mortgage, onlinenewspopularity). A CLEAN-19 case row
    records the first column joined from outside a source.
  - Issues 13 and 15 are open as consistency checks.
- **house_sales:** `yr_renovated` = 0 stays missing, as an exception to CLEAN-10 (a cases row). The record's `year` is
  now 2015. Issue 8 has an answer with measurements: keep the sales with codes known before the price, add an
  indicator for them, and drop only the appraiser's judgment codes.
- **huntprohibited_1m:**
  - The split stays by ad, with no `Spatial` tag (the reason is in the notes).
  - No date can be recovered (`itemid` is random). A used-car form change bounds the cost of the random split at
    about 0.002 ROC AUC; the notes give it instead of "cannot be measured". New issue 10 asks to confirm.
- **kick:** the marks to keep `WheelType` and `PRIMEUNIT`/`AUCGUART` went back to the curator as a consistency check
  against expresso's REGION. The conditional test now also covers PRIMEUNIT/AUCGUART and shows the same signature.
- **g_research_crypto_forecasting_1m:** answers only, the definition is unchanged:
  - TP-10 leg 1 holds under weighted Pearson;
  - no feature from the other top solutions helps in all three windows;
  - whole-minute sampling over all history is proposed;
  - new issue 7 on a 15-minute gap.

## 2026-10-21 (force_2020 units and depth order; qsar_oral_toxicity extended; RDKit Ipc on a log scale)

Lennart's second round of marks on these two datasets. Each record carries his decisions as `CC (2026-10-21, Lennart)` lines. Nothing was rebuilt; both checksums change.

- **force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition:**
  - `Grouping(time_on="DEPTH_MD")` records the order inside a well, with no window features (issue 1). The split is unchanged, and the derived regime tag becomes `GroupedTemporal`.
  - `_clean` converts two curves to one unit where the data give the factor (issue 8, CLEAN-21):
    - ROP in 32/2-1 and 16/10-5, from ft/h to m/h (x 0.3048, 5,814 rows). ROPA / ROP was 0.31 there and is 1.00 now.
    - MUDWEIGHT below 0.5, from bar/m to g/cm3 (/ 0.0980665, 225,528 rows). The 28 wells' medians now span 1.08-1.80 g/cm3.
  - Correction: the answer on the review page named ROPA as the curve in ft/h, but the curve is ROP.
  - The other off-scale curves stay masked. A CLEAN-21 case row records the conversion, and `REVIEW.md` is removed (nothing left open).
- **qsar_oral_toxicity:**
  - Extended with the project's evaluation set from the authors' package (`vt_data.mat`, a copy the curator provided; the public route is the group's download form). The definition reads the package instead of the UCI file.
  - The same deduplication as before gives 11,105 chemicals with 931 very toxic, against 8,484 and 708 before.
  - Added 207 RDKit descriptors of the package's QSAR-ready SMILES next to the 1,024 ECFP bits, as in the other SMILES datasets. The SMILES are then dropped.
  - Default LightGBM ROC AUC over the 9 splits: 0.885 with the bits alone, 0.901 with the descriptors added (better on 9 of 9).
  - Two more changes:
    - one unreadable SMILES (silicon carbide) is replaced by PubChem's structure;
    - `rdkit_Ipc` is dropped (it overflows float32).
  - Issue 3 is settled. The questions it raised are settled too (Lennart):
    - `rdkit_descriptors` ships Ipc as `rdkit_Ipc_log10` = log10(1 + Ipc) for every SMILES dataset, instead of dropping it here. This also changes apistox (Ipc up to 2.6e38, just below the float32 limit) and qsar_bioconcentration.
    - The `dataset_pure_feature_value` warning on `rdkit_fr_Ar_COO` is accepted with its reason.
    - The record's `original_source` is now `Other`.
  - `REVIEW.md` is removed (nothing left open).

## 2026-10-21 (the curator's marks on force_2020, infrared_thermography and qsar_oral_toxicity)

Lennart marked these three datasets on the review page; each record has his decisions as `CC (2026-10-21, Lennart)`
lines, and the open questions keep his note and an answer as dated turns in the folder's `REVIEW.md`. Nothing was
rebuilt.

- `infrared_thermography_temperature`: the split stays IID over people; the calibration is a time-independent
  function of the inputs (Lennart), so the measured shift between the study years (a first-year calibration
  over-predicts the second year by 0.06-0.09 °C) is documented and a temporal split recorded as a candidate variant
  (SPLIT-31). SEL-15 is amended: a physical quantity measured through an imaging device at defined sites, used by the
  field as the instrument's reading, is a measurement, not an image descriptor (SEL-13); satimage and wilt are the
  counter-cases. The `Wrong Domain / Source Modality` marker is removed and the folder's `REVIEW.md` with it (no issue
  left).
- `qsar_oral_toxicity`: fit `approximate` (Lennart: a simulated screening; random tested chemicals stand in for the
  untested ones a screener faces, 19.7% against 9.3% with a close analog); IID stays, the scaffold-grouped variant a
  listed candidate (SPLIT-31); the Features note names the fingerprint ECFP_1024_02 (the UCI file equals that block
  of the authors' package bit for bit). Issue 3 (extending with the package's validation set or its non-toxic
  endpoint) stays open. Data and splits unchanged.
- `force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`: the use case reads "a newly
  drilled or a released well" (issue 2 (a)); off-scale curves masked per well (ROP in 25/6-2, ROPA in 34/4-10 R, SGR
  in 34/12-1 and 35/11-15 S, MUDWEIGHT above 100 in 16/10-2 and 15/9-14); Grid, Skade and Ty Mb. merged into their
  Fm. codes; the Basement drop confirmed as a CLEAN-17 case; the record's domain set to environmental science &
  climate. Open: issue 8 (convert ROPA from ft/h in two wells and MUDWEIGHT from bar/m to g/cm3) and issue 1
  (declare `time_on="DEPTH_MD"`; TabArena builds no depth context).

## 2026-10-21 (every dataset declares its metric)

Lennart decided that a dataset is scored by the metric its original task defines (the competition's evaluation page,
the task description or the paper), with an explicit fallback (roc_auc / log_loss / rmse) when none is defined.
Nothing was rebuilt; every container needs a rebuild, because the task metadata changed.

- **Format 2 task metadata, changed in place:** `objective_metric_name` is replaced by the spec `objective_metric`
  (name, kind, prediction, origin `source` / `stand_in` / `context` / `fallback`, original, reference, definition,
  reason, params, inputs, target_transform) and `scoring_columns` (columns kept for scoring only, never features). An older format-2 file stops loading
  with a "rebuild" message; format 1 (BeyondArena) is unchanged.
- **`data_foundry.v2.metrics`:** `Metric.source / stand_in / fallback / local`, the registry of 23 standard metrics
  (scikit-learn names) and 11 custom ones with general names (`cost_matrix`, `precision_at_k`,
  `average_precision_at_k`, `rmspe`, `gini_top_capture`, `weighted_pearsonr`, `mean_group_pearsonr`,
  `hierarchical_balanced_accuracy`, `gini_stability`, `par_k`, `normalized_early_detection_utility`), each tested
  equal to its official implementation and timed on 1M rows; `scorer(container)` (inputs by row index, per-group
  aggregation) and `feature_columns(container)`. The module imports nothing else from Data Foundry.
- **Definitions:** `metric` is a required attribute. All 173 definitions declare one, from a sweep of their sources
  and the new rules MET-1..13 (`knowledge-curation/references/metrics.md`): 67 source, 6 stand-in, 13 from the task's context, 87 fallback.
  The scored metric changes for 18: allstate_claims_severity (`mae` on the raw loss), aps_failure and credit_g
  (`cost_matrix` on probabilities), coil_2000 and labour_inspection_compliance (`precision_at_k`),
  corporate_credit_rating_cat (`mae`, stand-in), electric_motor_temperature_prediction (`mse`), force_2020
  (`cost_matrix`, the competition's penalty matrix), forest_fires (`mae` on the raw area), g_research
  (`weighted_pearsonr`), hiva_agnostic (`balanced_accuracy`), huntprohibited_1m (`average_precision_at_k`),
  micro_mass (`hierarchical_balanced_accuracy`), numerai_v5_2_1m (`mean_group_pearsonr`, Numerai CORR),
  rossmann_store_sales (`rmspe`), sat11_hand_algo_runtime (`par_k`), wine_quality (`mae`), diamonds (`rmsle` on
  the price in dollars, the new origin `context`: no source metric, but the task makes one obvious). amex and
  sepsis_prediction_1m keep their metric under a general name (`gini_top_capture`,
  `normalized_early_detection_utility`). Each record has an
  `Assessment (AI, 2026-10-21)` line; Lennart's calls (home_credit stand-in, labour_inspection, covertype and the
  threshold metrics left out, the accepted proposals) are `CC` lines.
- **The shipped scale and the scored scale (`target_transform`, MET-3 rewritten; Lennart: "ship the target on the
  modelling scale, score on the original scale"):** the spec field `target_transform` (`identity`, `log`, `log1p`,
  `log10`; regression only) says how the target ships transformed for modelling; `score` / `scorer` apply the inverse
  to the true values and the predictions before the metric, so the declared metric is the one on the original scale.
  New checks `task_metric_transform_not_regression` and `task_metric_transform_overflow`; the README's metric table
  has a "target scale" row. `par_k` loses its own `target_transform` param (no double inverse). Definitions:
  - diamonds (log price again, `rmsle` on the dollar price), allstate_claims_severity (log loss again, `mae` on the
    loss), forest_fires (log1p area again, `mae` in hectares): the targets ship as before today's change.
  - From the fallback `rmse` on a log target to `Metric.from_context("rmsle", target_transform=...)`, the shipped
    target unchanged: house_sales, houses, immoscout_german_house_prices, melbourne_housing_market, miami_housing,
    perth_house_prices, wine_world_cost, brazilian_ecommerce, sf_permit_time, video_transcoding_time_prediction,
    onlinenewspopularity (`log`) and blood_tests_drink_prediction (`log1p`).
  - From `rmse` on a log1p target to the competition's `rmsle` with `target_transform="log1p"` (the same number):
    mercari_price_suggestion, pkdd_15_taxi_trip_time_prediction_ii_1m, nyc_taxi_trip_duration_1m,
    ashrae_great_energy_predictor_iii_1m, santander_transaction_value, california_house_prices_2020.
  - sat11_hand_algo_runtime: par_k's log transform moved to the spec's `target_transform="log"` (the same score).
  - sberbank_housing_market_forecasting keeps `rmse` on log(price / full_sq): the inverse is the price per square
    metre, not the price the competition scored.
- **Skills and docs:** TP-6 points to `metrics.md`; `/screen-candidates`, `/add-dataset`, the claim auditor and the
  domain practitioner check the metric; the review page shows each dataset's metric; the probes drop scoring columns;
  `examples/read_metric_without_data_foundry.py` reads a container's metric with plain json; `BENCHMARK_CHANGES_TODO.md`
  lists what the TabArena adapter has to change (read the spec, register the custom scorers, pass scoring columns,
  no silent fallback, threshold tuning for threshold metrics).

## 2026-10-21 (the curator's third round on the cross-dataset items)

Lennart replied on the page; his notes are now dated turns in the working copy's `REVIEW.md`, and the page shows each
issue and item as a conversation. Each changed record got a `CC (2026-10-21, Lennart)` line. Nothing was rebuilt.

Rules: CLEAN-14 (a 0/1 column is categorical only when its meaning says it is a flag; counts and opaque columns stay
numeric; a constant column is no flag), CLEAN-19 (the best of a baseline and the top solutions' features, or a
reasonable combination, not their union), PROV-3 and EV-3 (either calibrated or label-linked marks can be enough;
they count on the shipped columns, and on the published file when they extend to the shipped version).

Definitions:

- `qsar_tid_11`: drops 37 salt-form copies of one ChEMBL parent (LEAK-19; `SALT_FORM_COPIES`), 5,741 to 5,704
  rows; the repeated fingerprints of different compounds stay, with the decision in its notes.
- CLEAN-14 by meaning: 19 of the 35 definitions typed this morning go back in part or whole to numeric (amex_non_iid_1m,
  apistox, asp_potassco_classification, bioresponse, cardiotocography, clock_protein_toxicity, coil_2000,
  drug_induced_autoimmunity_prediction, early_learning_predictors, home_credit_default_risk,
  home_credit_default_stability_1m, homesite_quote_conversion, ieee_fraud_detection, phiusil_phishing,
  qsar_bioconcentration, santander_customer_satisfaction, sat11_hand_algo_runtime, sberbank_housing_market_forecasting,
  taiwanese_bankruptcy_prediction); the flags they keep are explicit lists.

- `drug_induced_autoimmunity_prediction`: grouped on the Bemis-Murcko scaffold (443 groups), taken from Andrej's PR #15
  with its `murcko_scaffolds` helper in `data_foundry.v2.chemistry` and its tests (Lennart: make it grouped here as
  well); ROC AUC 0.771 grouped against 0.826 random (untuned LightGBM).

Review files: `water_quality_and_potability` re-checked (it fails PROV-3) and given an open-issues block for the curator;
`rosbank1` issue 5 reworded under CLEAN-19; `credit_card_customers` and `stroke_prediction` issue 1 and
`hepatitis_c_egypt`'s block say what the PROV-3 standard means for them.

## 2026-10-21 (the curator's marks on the follow-ups)

Lennart marked the follow-up items of the working copy's `REVIEW.md`. Settled items are closed there; two new items
ask about drug_induced_autoimmunity_prediction's descriptor groups, water_quality_and_potability and which 0/1
columns are flags. Each changed record got a `CC (2026-10-21, Lennart)` line. Nothing was rebuilt.

Rules: USE-8 (a strong kept leak still does not make a fit approximate), PROV-2 (a sound upload with a source to point
to is kept for now, case by case, as an approximate fit), CLEAN-14 (every 0/1 flag, booleans included, is
categorical), CLEAN-11 (a single extreme training target may leave where experts drop it by default). Code: a v2
definition may no longer carry `ForcedIIDFromTemporal` with a grouping or temporal split, and the bundle check flags
it. The hidden-group probe takes float columns (a candidate needs at least 20 values held by two or more rows),
reports the near-copy check as not run below its token floor, and adds an exact key on each normalised text column.

Definitions:

- `nyc_taxi_trip_duration` is renamed `nyc_taxi_trip_duration_1m` (`version_of`, `subsample_to_budget`): 1,166,477
  rows, 1M rows per train side, the same test windows; the `splits_rows_unused` acceptance is gone.
- 0/1 flags made categorical in 35 definitions: account_debt_south_africa, amex_non_iid_1m, apistox,
  asp_potassco_classification, bioresponse, breast_cancer_prediction, cardiotocography, clock_protein_toxicity,
  coil_2000, college_scorecard, digicow_farmer_training_adoption_challenge,
  distribution_transformers_at_cauca_department, drug_induced_autoimmunity_prediction, early_learning_predictors,
  framingham_heart_study_fhs, home_credit_default_risk, home_credit_default_stability_1m, homesite_quote_conversion,
  hotel_booking_demand, house_sales, ieee_fraud_detection, infrared_thermography_temperature, kick,
  marketing_campaign, mobile_churn, mortgage, phiusil_phishing, qsar_bioconcentration, rossmann_store_sales,
  santander_customer_satisfaction, sat11_hand_algo_runtime, sberbank_housing_market_forecasting, stroke_prediction,
  taiwanese_bankruptcy_prediction, zillow_prize.
- Fit `direct`: homesite_quote_conversion, qsar_aquatic_toxicity, onlinenewspopularity; the kept leak no longer
  counts as a gap in perth_house_prices, credit_card_customers, african_credit_scoring_challenge and zillow_prize.
- Notes: tour_travels_churn (its source under the amended PROV-2; the generated-data probes raise nothing),
  mercedes_benz_greener_manufacturing (CLEAN-11 as amended), maps_router_eta_1m (`track_length` in metres; 31 of
  13.6M rows implausible, none late, so the one-day gap stands).
- Review files: settled issues removed from perth_house_prices (issue 1), mobile_churn (issue 1),
  credit_card_customers (issue 3) and nyc_taxi_trip_duration_1m (issue 5).

## 2026-10-21 (the curator's marks on the cross-dataset items)

Lennart marked the cross-dataset items of the working copy's `REVIEW.md` on the review page. The settled items carry a
`Resolved (2026-10-21, Lennart)` label there; the open ones an `Answer (AI, 2026-10-21)`; a new section lists the
follow-ups. Each changed record got a `CC (2026-10-21, Lennart)` line and an `Assessment (AI, 2026-10-21)`. Nothing was
rebuilt; every definition below whose data, split or metric changed needs a rebuild.

Rules amended in place (knowledge-curation): LEAK-10 (grades row: only grades not yet known at the prediction point),
LEAK-25 (unrecorded rows located by a rule that does not read the label, and dropped, count as recovered), USE-5 (an
undocumented label from a named publication ships approximate with a note), USE-8 (a kept leak alone does not make a
fit approximate; an unverified label definition does), PROV-2 (a named course or teaching platform is a known
source), PROV-3 (an owner's disclosure control with no measured damage is kept with a note), PROV-14 (a repair stays
under its record), SPLIT-8 (forced from temporal: no dates, one stock month, or too few periods), TP-6 (a definition
declares its source's metric), CLEAN-11 (a target the source names as not the task's quantity, or one extreme training
target, may leave), CLEAN-14 (a molecule's 0/1 flags are categorical). New Cases rows under LEAK-7, LEAK-10, LEAK-31,
LEAK-37, SPLIT-10 (exceptions for alfa_battle_2_0_task_2 and lending_club), EV-4; a Tensions row in `principles.md`;
`definitions.md` states the budget of at most 1M training rows and the metric order.

Code: a new data tag `ForcedGroupedFromTemporal` (schema, v2 validation, bundle check); `2ndTierData` stays readable
(a shipped BeyondArena container carries it) but a v2 definition may no longer set it. The task probe keeps a temporal
task's newest train rows and caps at 200,000 rows (was 50,000 random rows).

Data, split or metric changed:

- `california_house_prices_2020`: keeps resales (only the 51 same-price copies of one sale keep their newest row;
  39,060 rows); `min_train_fraction` 0.25 to 0.5 (SPLIT-14).
- `cooking_time_1m`, `maps_router_eta_1m`: a one-day gap (108-172 and 578-656 late training labels per window, now 0).
- `melbourne_housing_market`: the six scraped attributes blank for the 7,578 sales before the batch lookup of
  10 April 2017.
- `sberbank_housing_market_forecasting`: monthly, quarterly and yearly macro series lagged one period (LEAK-10).
- `qsar_oral_toxicity`, `qsar_tid_11`: fingerprint bits categorical; `qsar_tid_11`'s impossible pXC50 row leaves as a
  missing target (CLEAN-15).
- Metric under TP-6: `zillow_prize` `mae`, `numerai_v5_2_1m` `pearsonr`, `african_credit_scoring_challenge` `f1`,
  `force_2020...` its penalty matrix, `digicow...` `log_loss`, `porto_seguro` `roc_auc`,
  `dataorg_financial_health_prediction_challenge` `f1_weighted`, `g_research_crypto_forecasting_1m` `pearsonr`,
  `huntprohibited_1m` `average_precision`, `bioresponse` `log_loss`, `mercedes_benz_greener_manufacturing` `r2`.

Labels, tags and notes only: domain `chemistry & material science` for `apistox`, `bioresponse`,
`qsar_aquatic_toxicity`, `qsar_biodeg`, `qsar_fish_toxicity` (the other five QSAR siblings had it); fit `direct` for
`house_sales` and `kick`; fit reasons of `sarcoma` and `differentiated_thyroid_cancer_recurrence`; tags
`ForcedGroupedFromTemporal` (`nba_players_2016_2019`, `open_university_learning_analytics_dataset`) and
`ForcedIIDFromTemporal` (`churn_telco_south_asia`, `bank_customer_churn`, `tour_travels_churn`; note on
`distribution_transformers_at_cauca_department`); `2ndTierData` removed from `credit_card_customers` and
`coffee_rating_prediction`; SPLIT-10 exceptions in `alfa_battle_2_0_task_2` and `lending_club`; notes in
`framingham_heart_study_fhs` (selection), `hiva_agnostic` (its copies), `house_prices_nominal`, `delivery_eta_1m`,
`nyc_taxi_trip_duration` (TLC cited), `5g_energy_consumption`, `home_credit_default_stability_1m`.

Review files: new `REVIEW.md` for `kick` (keep or drop `WheelType`; `PRIMEUNIT`/`AUCGUART`) and `thyroid_discordant`
(its `Trivial` marker, refuted under TP-4); settled issues removed from `diabetes_3`, `melbourne_housing_market`,
`nba_players_2016_2019`, `mobile_churn`, `open_university_learning_analytics_dataset`, `zillow_prize`,
`numerai_v5_2_1m` and `force_2020...`; `distribution_transformers_at_cauca_department` has no issue left and its
`REVIEW.md` is removed.

## 2026-10-20 (re-review of every folder with open issues)

Every folder of the working copy with open review issues was re-checked with `/add-dataset` in re-check mode and the
full review panel (`.claude/skills/add-dataset/references/review_panel.md`), in priority order. Each folder's
`REVIEW.md` was rewritten in the current format with the panel reports, each record got an
`Assessment (AI, 2026-10-20)` line and a priority, and the cross-dataset items went into the working copy's
`REVIEW.md`. Nothing was rebuilt; the READMEs' build records name the earlier containers. 41 definitions changed, 27
of them in their data. All 41 folders whose `REVIEW.md` was rewritten also had their `dataset.py` edited, and no
`REVIEW.md` was deleted.

Data changed (rows, columns, values, dtypes, splits or cleaning):

- `2_month_survival_rate_prediction`: sets `alb` above 6 g/dL to missing (4 patients).
- `account_debt_south_africa`: a no-debt run is now dropped when it holds at least 100 billed never-payers
  (`NO_DEBT_RUN_BILLED_NEVER_PAID`, was 1,000 rows), which adds the 186-row run (eight runs, 28,124 rows); sets a
  `PropertyValue` of 1 and a `PropertySize` of 10 m² or less to missing.
- `aeolus_1m`: sets temperatures below -50 C and wind speeds above 120 km/h to missing; corrects the sign of Guam's
  longitude and Pago Pago's latitude. Fit `direct` to `approximate`; domain `industry & manufacturing`.
- `african_credit_scoring_challenge`: drops `other_lenders_on_loan` (Test.csv is now read only for a decision table);
  sets the funded amount and share to missing in the one row that funds more than the loan.
- `alfa_battle_2_0_task_2`: drops the four columns that copy another (`COPY_COLUMNS`), 508 aggregates left.
- `dataorg_financial_health_prediction_challenge`: drops the 11 product answers (`PRODUCTS`), inputs of the index;
  sets the business age to missing in the 6 rows where the business is older than its owner.
- `distribution_transformers_at_cauca_department`: drops `power_kva` and `installation_type` (the inventory shows a
  replacement's rating); replaces `energy_not_supplied_kwh` by `outage_hours` (EENS / (1.08 x kVA)); sets the
  lightning densities of 0.0 in both columns to missing (487 rows).
- `force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition`: sets to missing the log
  values below -900 (LAS nulls and their interpolation ramps) in all 20 curves, negative resistivity, gamma-ray and
  penetration-rate readings, DCAL above 100 inches, and DRHO in wells 36/7-3 and 31/4-10; adds a splits comment.
  Domain `environmental science & climate`.
- `fraud_detection_in_electricity_and_gas_consumption_1m`: keeps only clients still billed from 2015 on (was from
  2013 on; 81,531 clients); drops `counter_number`; sets the invoice fields of rows shifted by one column, undocumented
  `counter_statue` codes, a `counter_coefficient` of 0 and `months_number` above 120 to missing; `counter_code` and
  `reading_remarque` become nullable integers.
- `g_research_crypto_forecasting_1m`: sets negative `Volume` to missing (2 rows).
- `house_prices_nominal`: sets the two impossible remodel years to missing; writes three `Exterior 2nd` spellings as
  the documentation's codes (225 rows).
- `house_sales`: drops the 1,061 sales the county flags as not at market value (19,906 left), read from a new
  prepared file of the county's sale warnings (`Real Property Sales.zip`, needed for a rebuild); rebuilds `sqft_lot`
  also from the `LandFootage` log records; sets the placeholder living area of 5 houses under construction to missing;
  adds a one-week gap to the temporal splits. Fit `direct` to `approximate`.
- `infrared_thermography_temperature`: drops the 17 subjects without a complete round-1 image (1,001 left), who
  until now took their round 2 or 3 image.
- `lgd`: `purpose_renting` becomes categorical.
- `melbourne_housing_market`: gives each suburb its `Distance` from 27 May 2017 on; fills the suburb lookups of the 2
  rows without them; sets 86 impossible `BuildingArea` values to missing.
- `mortgage`: drops the two ids that copy another id (23 rows) and the last row of the 501 loans that leave the data
  early without an event; sets the current rate of 37.5% to missing (44 rows); adds `balance_time_lag_2`.
- `nba_players_2016_2019`: adds `prev_score`, last season's score; sets the 185 page-view values that repeat an
  earlier season's to missing.
- `nyc_taxi_trip_duration`: drops the 4,539 trips whose drop-off equals the pickup point; sets passenger counts of 0
  or above 6 to missing (23 trips); adds a one-day gap. Fit `direct` to `approximate`.
- `onlinenewspopularity`: drops `rate_negative_words` (1 minus the positive rate); sets the share count 1.59 and the
  averages that include it to missing (120 rows).
- `open_university_learning_analytics_dataset`: leaves weight-0 TMAs out of `score_mean` and `score_min` (1,655
  rows); each train side loses the test students' concurrent and later registrations (577-901 rows per split).
- `perth_house_prices`: sets 19 floor areas and 2 bathroom counts to missing; blanks the station for 147 sales and
  the school for 58 sales before they opened; splits `Vic` into Victoria Street and Victoria Park. Fit `direct` to
  `approximate`.
- `pkdd_15_taxi_trip_time_prediction_ii_1m`: drops the trips that end at their start point; test windows of 30 days
  from 1 April, 1 May and 1 June 2014 with a one-day gap (were calendar months without a gap).
- `qsar_oral_toxicity`: drops the second row of nine parent structures kept twice (8,484 chemicals).
- `rain_in_australia`: sets a blank wind direction at a wind speed of 0 to "Calm"; sets a humidity of 0% to missing
  (5 cells). Fit `direct` to `approximate`.
- `sarcoma`: drops the 61 `Methy_rs*` genotype probes (25,910 features). Fit `direct` to `approximate`.
- `stroke_prediction`: drops `ever_married`, `work_type` and `Residence_type`, and with them the accepted warning on
  `work_type`.
- `zillow_prize`: blanks `taxdelinquencyflag` and `taxdelinquencyyear` for sales before September 2016 (the flag
  becomes 1.0 / 0.0 with missing values); sets a `garagetotalsqft` of 0 with a garage car count of 1 or more to
  missing. Fit `direct` to `approximate`.

Notes only (task summary, curation comments, splits comment, fit labels, accepted-warning reasons, metadata):
`corporate_credit_rating_cat_data_set_ratings_raitings`, `credit_card_customers` (tag `ForcedIIDFromTemporal`),
`diabetes_3` (fit `approximate`), `differentiated_thyroid_cancer_recurrence` (fit `approximate`),
`digicow_farmer_training_adoption_challenge`, `expresso_churn_prediction_1m` (tag `ForcedIIDFromTemporal`; source the
2020 UmojaHack Ghana hackathon, with its URL and BibTeX), `framingham_heart_study_fhs`,
`glioma_grading_clinical_and_mutation_features` (fit `approximate`), `huntprohibited_1m`, `mobile_churn` (tag
`ForcedIIDFromTemporal`), `numerai_v5_2_1m`, `phiusil_phishing`, `qsar_bioconcentration`, `rosbank1`. The
`dataorg_financial_health_prediction_challenge` spellings dropped from `ANSWER_SPELLINGS` occur only in the dropped
product columns.

In `knowledge-curation`, `references/leak_checks.md` marks the melbourne_housing_market example of the LEAK-10 Cases
row (attributes looked up after the outcome) as provisional, pending the curator. The README table, regenerated from
the folders' READMEs, shows the new row and feature counts of 17 of these datasets.

## 2026-10-20 (eight shipped datasets are `DF: Yes`)

The review work reached `main` with PR #11, so the records of the eight datasets Lennart shipped on the review page of
the 2026-10-07 run, with no issue left open, take their final state: `DF: Yes`, the `WIP (DF)` claim released. No
definition changed; none is built yet. `apistox`, `ashrae_great_energy_predictor_iii` (folder `_1m`),
`bias_correction_r_bias_correction_r_2`, `brazilian_ecommerce`, `breast_cancer_prediction`, `caracas_cervical_cancer`,
`churn_telco_south_asia`, `college_scorecard`. Every other dataset of that run still has a `REVIEW.md` (or, without a
folder, an open-issues block in its record).

## 2026-10-20 (airfoil_self_noise grouped by setup, its year 1989)

Lennart's marks on the review-panel pilot page, applied. The definition changed; not rebuilt (the README's build
record names the container of 2026-10-06, marked stale).

- `airfoil_self_noise` holds out whole setups, one chord length at one angle with all its speeds (`setup`, 33 groups,
  11 per test fold; was the wind-tunnel run): under the run split 91.5% of the test runs had their chord and angle in
  training at another speed, and a new angle or size is the query, as a new mix is for
  `concrete_compressive_strength`. `attack-angle` is numeric (72% of the test runs now carry an angle absent from
  training). On the shipped splits, untuned: LightGBM R² 0.727, random forest 0.717, linear 0.445; no task-probe
  flags, no leak-probe hits; `groups_test_groups_few` accepted (the 33 setups are all the report has; R² 0.71 across
  setups).
- The scaled target stays as released and is named as the report's eq. 19 level, with its constants and the exact
  conversion to the measured level. The notes now state the tripped set, the corrected angle, the truncated bands,
  the source's prediction use and the reason for not grouping by chord; the 62% is 66.6%, and the BibTeX names
  NASA RP-1218.
- Year 1989 and source the NASA report (`source = "Other"`, `source_url` its NTRS page), not UCI 2014: the report's
  figures show every measured value, and UCI's file was digitised from them. The year rule PROV-9 says so now (amended in
  `knowledge-curation`), which corrects the reading in the entry below. The record's `original_source` is `Other`.
- The folder's `REVIEW.md` is gone (no open issue left); the working copy's `REVIEW.md` keeps the hidden-group probe
  item.
- The README table, regenerated, also shows the current feature counts of `college_scorecard` (92) and
  `home_credit_default_risk` (709), stale since their last definition changes.

## 2026-10-19 (curation commands renamed and mirrored, a review panel, ranked rules)

Lennart asked for descriptive commands for what curators use, documentation for people, a quick screening stage with a
priority, an add stage that attacks each dataset before the curator sees it, and an order of importance for the rules.
No definition or container changed and nothing was built.

- The commands: two stages, in each the AI works and the curator verifies. `/screen-candidates` (was
  `/triage-candidates`) makes a quick pass from the source, rejects the obvious cases after an agent argued against
  each reject, and sets a new record field `priority` (1-5); `/review-screened-candidates` opens the dashboard's new
  Screening queue. `/add-dataset` adds a review panel of agents after its checks (claim, column and split auditors, a
  domain practitioner, a blind reviewer without our notes, a precedent checker, an advocate and a critic, a mediator,
  an editor) and writes its reports into a `**Review panel:**` block of `REVIEW.md`, shown in a Panel tab of the
  review page; it also re-checks an existing folder ("is X ready?"). `/review-added-datasets` checks every mark for
  consistency with the rules and earlier decisions before applying it. `/check-candidate` is gone (its uses went to
  the two AI commands), and `/rebuild-working-copy` became `knowledge-data-foundry/references/rebuild.md` with its
  scripts in that skill's `scripts/`. The agents are in `.claude/agents/`; the overview for people is
  `.claude/skills/README.md` ("Start here" on the dashboard's Guidelines page).
- The rules: `knowledge-curation` is ordered like a law book. `principles.md` ranks seven principles (ethics, scope, a
  real use case, honest evaluation, faithful and unique data, worth benchmarking, the expert state), defines the rule
  strengths (Must, Should, Weigh), how to decide, the tensions between rules, exceptions and amendments, and the
  consistency checks on every decision, the curator's included. Every rule has an ID (`SEL`, `USE`, `LEAK`, `SPLIT`,
  `PROV`, `TP`, `CLEAN`; `task_probes.md` rule N is TP-N, so the citations in the definitions still hold);
  `evidence.md` holds what counts as evidence and what each probe flag can mean. The task and generated-data probes
  print the rule next to each flag (`flag_rules` in their JSON); their numbers are unchanged.
- In this folder: the citations of the old selection criteria and of "leak_checks.md, section 5" in nine `REVIEW.md`
  files name the rule IDs (e.g. LEAK-16 to LEAK-21 in `qsar_oral_toxicity`); `GETTING_STARTED.md` and the README
  describe the new commands.
- The first full review panel ran on `airfoil_self_noise` (a re-check; the definition is unchanged and not rebuilt).
  Its new `REVIEW.md` holds two issues (hold out runs or setups of one airfoil size at one angle; keep the scaled
  target or re-target to the measured level), the `year` field row and the panel's reports, and lists the changes
  that need no decision: `attack-angle` numeric (categorical costs 0.02-0.04 R² on the shipped splits), the target
  named as the source's eq. 19 scaled level, the 62% figure and the chord reason restated, the BibTeX completed. The
  year stays 2014: the rows were digitised in 2006 from the NASA report's figures and first published by UCI. The
  working copy's own `REVIEW.md` is back with one cross-dataset item: the hidden-group probe skips float columns that
  are not whole numbers.

## 2026-10-19 (one source for the curation knowledge; `LEAK_AUDIT.md` and `NEW_DATASETS_ISSUES.md` removed)

Lennart asked for one source of truth for the curation knowledge, shared by all skills and the website, and for the
two extra documents of this folder to go. No container changes and nothing was built.

- The skills: two reference skills hold the knowledge, `.claude/skills/knowledge-curation/` (selection, use case,
  splits, leaks, cleaning and features, task probes, provenance, the verification checklist, writing for the curator,
  and the general probe library) and `.claude/skills/knowledge-data-foundry/` (records, dashboard, the `dataset.py`
  API, the checks and probe commands, this working copy, source access, batch runs, house rules). The workflow skills
  keep only their steps and link the file each step needs. `/verify-dataset` is gone: its checklist is
  `verification.md`, which every workflow runs as its last step, and `/check-candidate` answers "is X ready?". The
  move resolved the contradictions between the old copies (PCA and scaling over all rows, feature engineering,
  impossible values, `Multi-target`, rare classes, where evidence goes) by Lennart's latest decisions, and added the
  review lessons no skill held (the company's own estimate as an input, one scale for a feature whose scale changes,
  the real-world target, cold start against recurring entities, multi-label flags, a rebuild's origin, and how to write
  an issue for the curator).
- The probes: the methods are now a library without Data Foundry imports
  (`.claude/skills/knowledge-curation/scripts/curation_probes/`); the command-line entry points keep their names and
  flags in `.claude/skills/knowledge-data-foundry/scripts/`. The READMEs that name the group-probe path keep the old
  path until their next `dataset check` or build.
- The website: the dashboard's Guidelines page (and the GitHub Pages copy) renders the two knowledge skills from their
  .md files instead of the hand-written `guidelines.html`; `build-site` copies them, and Pages also redeploys when they
  change.
- `LEAK_AUDIT.md` removed: its general findings were already in `leak_checks.md`, its per-dataset findings in the
  records' dated audit lines. Four open findings went into their records as dated assessments for the next pass:
  `thyroid_discordant` (an `age` of 455), `heloc` (588 rows of -9 in every feature), `homesite_quote_conversion` (two
  warnings without a decision), `online_shoppers_purchasing_intention_dataset` (40 exact duplicates).
- `NEW_DATASETS_ISSUES.md` (the report of the 2026-10-07 run) removed. Its open issues are in a `REVIEW.md` in 41
  dataset folders (264 issues, 22 record-field rows); the 6 records that were not added carry theirs in an
  `**Open issues (AI, 2026-10-07):**` block. Settled issues and the run logs were left out; all 40 cross-dataset
  items were closed. `/review-added-datasets` builds its page from these files (`collect_reviews.py`, format in
  `references/review_file_format.md`). A folder's README lists its `REVIEW.md`.
- `digicow_farmer_training_adoption_challenge`: the curation comments no longer cite the removed file (the evidence is
  an assessment in the record); new checksum `v2:6e9e68dd...`, README refreshed, not built.
- `bias_correction_r_bias_correction_r_2`: the record's `Multi-target` tag removed (one target).
- Records (Lennart, 2026-10-19): `required_split` set to the definition's regime in the 34 records that disagreed
  (several values, `?`, `Custom`, empty, or the regime before a re-split such as airfoil_self_noise, superconductivity
  and lgd now grouped), and `Non-IID (Grouped)` / `Non-IID (Temporal)` tags that contradict the definition removed,
  as well as `Larger IID Data` (force_2020, open_university_learning_analytics_dataset) and `New IID` (lgd) on grouped
  datasets.
  `african_credit_scoring_challenge` verified (the AI flag and tag removed, the disclaimer relabelled as an AI summary).

## 2026-10-19 (scaling over all rows: two definitions fixed, the rest kept with notes)

Lennart's marks on the scan of 2026-10-16 (review page, "Scaling over all rows"). A scaling over all rows is a weak
leak: rebuild from unprocessed values when the source has them, otherwise keep with a `Potential leak, kept on
purpose:` note; a reason for `No` only when a strong leak is suspected (rule in the curation guidelines, the leak checks
and the add-dataset patterns). Edited definitions, not built: their READMEs are stale until the next build.

- `sf_permit_time`: `DescriptionIsStandardPhrase` counts the descriptions filed before 2020, the start of the oldest
  test window, instead of the whole table (0.66% of the rows flagged instead of 0.77%; `_make_splits` asserts the
  cutoff). `dataset check`: 0 errors, 0 warnings.
- `home_credit_default_risk`: no statistic over all rows. The kernel's `NEW_INC_BY_ORG` is dropped, `NEW_SCORES_STD`
  stays missing instead of its mean, and the kernel's importance-based feature selection (LightGBM on all labelled
  rows) is removed, so 709 features ship instead of 504. Constant columns and exact copies are dropped (mostly shares
  of the one-hot "nan" category), min/max of one-hot flags become 0/1, inf becomes missing in every numeric column,
  and `FLAG_OWN_CAR` is categorical. The kernel's transductive setting may be revisited. Its 43 normalised building
  columns are kept with a note.
- Kept with a `Potential leak, kept on purpose:` note: `bioresponse` and `taiwanese_bankruptcy_prediction` (min-max
  over all rows), `credit_card_customers` (clipped at whole-file percentiles), `cooking_time_1m`, `delivery_eta_1m`
  and `maps_router_eta_1m` (TabReD's quantile transform, fit rows undocumented), `lung_cancer_epithelial_genexp` (RMA).
- `rosbank1`, `alfa_battle_2_0_task_2`, `anes_voting_2026`: the notes say that choosing codes or questions over all
  rows is a pipeline choice that approximates the task.
- `ieee_fraud_detection` and `kdd_cup_09_appetency` tagged `Anonymized` (their features are masked), as the other
  datasets with undocumented transforms are.
- `sarcoma` record: rebuild the methylation block from the GDC in the next pass.
- `college_scorecard` ships (Lennart's verdict on the review page; record `CC` line). Not built yet.

## 2026-10-16 (the gap between train and test is stored; coad, corporate_credit_rating and lgg retired; college_scorecard SAT back on one scale)

- Split metadata: new `time_gap` / `time_gap_unit` next to the horizon (Lennart's mark on college_scorecard, issue 9).
  A calendar or row window states its gap (`TemporalSplits(gap=...)`); a `unit="unique"` window or a gap built in
  `_make_splits` declares it as `Temporal(gap=..., gap_unit=...)`. Unset fields stay out of the checksum and the saved
  JSON, so containers without a gap keep their checksums; the README shows the gap with the horizon, and the bundle
  check `meta_time_gap_without_time_on` refuses a gap without a time column. Declared on college_scorecard (5 years),
  numerai_v5_2_1m (4 weeks), brazilian_ecommerce (1 month) and sf_permit_time (6 months); stated by their windows on
  rosbank1 (3 months), ieee_fraud_detection and zillow_prize (1 month), onlinenewspopularity (1 week), aeolus_1m,
  bias_correction_r_bias_correction_r_2, g_research_crypto_forecasting_1m and rossmann_store_sales (1 day). These 12
  get new checksums at the next build; their rows and splits do not change.
- Retired by Lennart (records `No`, `Data Quality Issue`; folders removed, `v2_path` cleared; the definitions stay in
  git at 2475ea2; none was built). 173 definitions remain.
  - `coad_colon_adenocarcinoma`: the MLOmics release z-scored every feature over all 260 patients, test rows
    included, a transductive leak. New record `tcga_coad_molecular_subtype` for a rebuild from the GDC's per-sample
    files with the same task decisions. The rule (source-side statistics over all rows are a leak, labels or not) is
    in the leak checks and the add-dataset patterns.
  - `corporate_credit_rating`: 17% of the labels that could be checked against the agencies' own histories are a
    bond's or loan's rating, not the company's, and the uploader's build drops Moody's grades and delisted
    companies. New record `corporate_issuer_credit_rating` for a rebuild from the agencies' Rule 17g-7(b) histories
    and SEC EDGAR.
  - `lgg_low_grade_glioma`: stays `No` as decided on 2026-10-12 (methylation of other patients, gene names that do
    not describe the values); its expression values also look standardised across patients.
- `college_scorecard`: SATMT25, SATMT75 and SAT_AVG are back (Lennart). From the 2017 cohort on they are on the
  redesigned SAT; the College Board's concordance tables (`sat_concordance.csv`, May 2016) put them back on the old
  scale. Untuned LightGBM R² on the 2018/2017 windows: 0.798/0.808 converted, 0.783/0.802 as published, 0.796/0.809
  without SAT. Record: the `Non-IID (Grouped)` tag removed (the task is temporal). Not built; `dataset check` clean.

## 2026-10-15 (coad_colon_adenocarcinoma: review marks; a feature-selection task probe)

Lennart's marks on the review page of the 2026-10-07 run, verdict still open. No change to the definition.

- Record: `problem_type` Multiclass Classification. The three blocks stay (36,355 features): every relevant feature is
  kept however wide the table, and a model's feature cap is no argument (rule in the add-dataset patterns and the
  run report format). The release's standardisation over all 260 patients cannot be undone from the release (open
  on the review page).
- `task_probes.py`: on more than 1,000 model inputs a fourth family, `selected_linear` (the linear model on the 500
  inputs of the strongest univariate F-test, chosen inside each training fold). On coad it scores skill 0.381
  against 0.111 for the linear model on all inputs (random forest 0.404); no flags.

## 2026-10-15 (churn_telco_south_asia ships: impossible values missing; churn timing unknown)

Lennart's marks on the review page of the 2026-10-07 run (issues 1 and 6) and his verdict: ship. Edited `dataset.py`,
not built (checksum `v2:4708a007…`); `dataset check` 0 errors, 0 warnings.

- `network_age` is missing for the 5 churners with a negative value (-8 to -2 days), and `aug_fav_a` "0" (59
  subscribers, an undocumented code absent in September) is missing. The undocumented on-net and off-net unit,
  complaint counts from 1 and the September shift to ufone (it follows activity in both classes) stay as published.
- Both papers of the authors (IntelliSys 2017, Neural Computing and Applications 2020) are read; neither says when
  churn was observed. The task may be problematic and is kept for now: the notes state it as a potential leak kept on
  purpose (churn inside August-September would make the usage totals end at the outcome, as in iranian_churn), the
  task summary's fit stays `approximate`, and it is to be revisited if the churn can be dated.

## 2026-10-15 (cdc_diabetes_health_indicators retired: wrong task)

- `cdc_diabetes_health_indicators` retired (record `No`, `No Good Target / Scientific Discovery`; folder removed,
  `v2_path` cleared; the definition stays in git history at bb3baa3; it was never built). The label is "ever told you
  have diabetes", a diagnosis made a median of 10 years before the interview, predicted from answers of the same
  interview: no decision is made with that prediction. The use the sources name is screening, which needs undiagnosed
  adults as positives; BRFSS cannot identify them, so they sit in the negative class. The rule is now in criterion 3
  of the curation guidelines. A screening task on NHANES, with lab-measured undiagnosed diabetes as the label, is
  checked as the new candidate `nhanes_undiagnosed_diabetes`. 176 definitions remain.

## 2026-10-15 (caracas_cervical_cancer and breast_cancer_prediction ship)

Lennart's marks on the review page of the 2026-10-07 run. Not built.

- `caracas_cervical_cancer` ships: impossible answers become missing, the rows stay (2 first intercourses
  after the current age, 2 STD diagnoses longer ago than the patient's age); the other contradictions stay as
  recorded. The STD flags stay one yes/no category each (multi-label; 9 patients have two or three types, not 43:
  `std_condylomatosis` is the parent of two subtypes). Rows and splits unchanged; `dataset check` 0 errors,
  0 warnings. The record loses the `Multi-target` tag.
- `breast_cancer_prediction` ships.

## 2026-10-15 (breast_cancer_prediction: one exam per woman, IID; probe fixes)

Lennart's marks on the review page of the 2026-10-07 run (issues 1, 2, 3, 6 and 8), verdict still open. Edited
`dataset.py`, not built (checksum changes); `dataset check` 0 errors, 0 warnings (two accepted), 1 info.

- One exam per woman, her earliest in the sample, with IID folds instead of grouping by woman: 36,714 rows and 239
  of the 259 cancers (the 20 women with cancer and several exams are positive only on their last exam). Untuned
  LightGBM scores alike either way (ROC AUC 0.928 earliest exam, 0.923 latest, 0.925 all exams grouped).
  `dataset_duplicate_rows` (repeated coarse profiles of different women) is accepted with that reason.
- The BI-RADS readings stay features: tabular risk models use them in practice. The curation guidelines (and
  `guidelines.html`) now carry that exception to the image-scoring rule.
- Record: `year` 2014; the dead datahub link replaced by the BCSC page.
- Tooling: the leak, group and task probes load only the named folder (`--all` skips folders that do not import);
  the linear models of the task and group probes one-hot encode categories. The review page labels its marks by what
  they do, and record-field disagreements go only into its field table.

## 2026-10-15 (review verdicts: bias_correction and brazilian_ecommerce ship; churn_telco_nigeria renamed)

Lennart's verdicts on the review page of the 2026-10-07 run, none built yet:

- `bias_correction_r_bias_correction_r_2` and `brazilian_ecommerce` ship. brazilian_ecommerce ships as implemented
  (delivery time at checkout, a one-month label gap, Olist's promised date as an input); its record's year is now
  2018.
- `churn_telco_nigeria` is `No` + `Duplicate` (the DSN files are the SATO 2015 rows of `churn_telco_south_asia`) and
  is renamed `churn_telco_south_asia_duplicate`; `churn_telco_south_asia`'s note names the new record (its checksum
  changes, `v2:e7577332…`; not built). The local downloads of `churn_telco_nigeria` and `churn_telco_europa` (which
  held customers' national ids and phone numbers) are deleted.
- brca_breast_cancer, central_international_medical_college_and_hospital_health_risk_prediction and
  churn_telco_europa: their `No` of 2026-10-12 is confirmed.

## 2026-10-15 (bias_correction_r_bias_correction_r_2: rows without an LDAPS forecast dropped; probe and test fixes)

Lennart's review of the 2026-10-07 run (issues 4, 6 and 7 of NEW_DATASETS_ISSUES.md). Edited `dataset.py`, not
built (checksum `v2:07d8e9f7…`, was `v2:41fdfb3c…`); `dataset check` 0 errors, 0 warnings.

- The 75 station-days of the three days without an LDAPS run (2013-08-10, 2016-07-31, 2016-08-20, all on the
  training side) are dropped: the task corrects the LDAPS forecast, and without one there is nothing to correct.
  7,648 rows remain. The mean of untuned CatBoost, LightGBM and ridge still beats per-station MOS on 7 of 9 windows
  (RMSE 0.785 against 0.823); the decision text gives the new numbers.
- `splits_comment` is a text block again (it was one string to avoid the dedent gap fixed on 2026-10-12).
- The task probes flag `no_spread` and `unstable`: LightGBM falls just below the training mean in the oldest window
  (skill -0.07) and beats it on the other 8; kept, as `curation_comments` says.
- Tooling: `tests/test_v2_datasets.py` checks each folder's import in its own test, so a half-filled scaffold no
  longer stops the collection of all; `task_probes.py` counts the standard-error part of `unstable` on a temporal
  task only when the best family loses to the dummy on a window, and its JSON lists the skill and the dummy's loss
  per split.

## 2026-10-15 (ashrae_great_energy_predictor_iii_1m: readings in kWh, recording errors dropped)

Lennart's review of the 2026-10-07 run (issues 2, 3, 4 and 8 of NEW_DATASETS_ISSUES.md): ship, as one temporal
task, cleaned to the state an expert would ship. Edited `dataset.py`, not built (checksum `v2:67c30a35…`, was
`v2:858c1cad…`); `dataset check` 0 errors, 0 warnings.

- The readings come in kWh from BDG2's raw meter files (four new raw files and BDG2's building metadata, pinned to
  the commit of kaggle.csv). The competition kept each site's own unit (ton-hours, pounds of steam, mmBTU, kBTU);
  BDG2's values are the Kaggle reading over one constant factor per meter in 99.9% of the hours. Site 0's kBTU
  conversion is part of it, so `KBTU_TO_KWH` is gone.
- `recording_errors` drops, besides site 0's 2016 gap and the electricity zeros: a cooling or heating plant at 0 for
  48 hours or more in its season (383,406 hours), the repeats of a reading stuck for a week or more (618,666 hours,
  mostly site 5's electricity in March-November 2017) and building 1099's steam unit error (3,332 hours). 1,701,150
  hours dropped (4.2%), 39,062,170 kept. 94.5% of the 2016 hours dropped are on the 1st place team's hand-made list
  of bad readings. A decision table counts the meters per unit, another the hours per rule.
- Issue 2 (scope): LightGBM with 1,000 trees beats the best naive forecast (each meter's hour-of-week profile from
  the same month a year earlier) by 0.10-0.14 RMSE per window, and one model per site only matches one large model,
  so the meter types and sites stay one task. The record holds the numbers.
- The record lists only the temporal regime (`tags`, `required_split`). The suspended v1 notebook
  (`datasets/_maintenance/_suspended/ashrae_energy_predictor/`) is removed; the definition here replaces it.

## 2026-10-14 (claims: `claimed_by` on WIP records)

- A WIP record now names its holder in `claimed_by` (curation tooling, review reasons `wip_unclaimed` and
  `claim_without_wip`); the 51 records of the 2026-10-07 run under Lennart's review carry `claimed_by: Lennart`.
  These first claims reach `main` with this branch's PR; from now on a claim goes to `main` in a small PR of its own.
  GETTING_STARTED.md (section 7), the triage, add-dataset and review skills describe the flow: claim on `main`
  ahead of the work, work on a branch, release with the PR that brings the work to `main`.

## 2026-10-14 (`_too_late_to_add` removed)

- `datasets/_maintenance/_out_of_scope/_too_late_to_add/` is deleted: its three v1 notebooks
  (african_credit_scoring_challenge, infrared_thermography_temperature, phiusil_phishing) are superseded by their v2
  definitions in this folder (added on 2026-10-07). Their records no longer carry a `notebook_path`; the notebooks
  stay in the git history (de9e6ad). `datasets/_maintenance/_deprecated/README.md` no longer lists the bucket.

## 2026-10-14 (rebuild: apistox and drug_induced_autoimmunity_prediction without the SMILES)

- Rebuilt with `build_all.py --only` from the uncommitted tree (`git_sha` de9e6ad-dirty): 2 of 2 ok, both containers
  reload with their checksums, no new or open warning; a check build from only the traced raw files gives the same
  checksums. New UUIDs: `apistox` 01a13aff-7eeb-7f10-a83c-d760795b95d5 (its first build),
  `drug_induced_autoimmunity_prediction` 01a13aff-7235-73c3-932c-785cd540127b. The superseded drug_induced container
  of 2026-10-06 (01a111fc-d491-7412-a5c5-884df72be349) is deleted; BeyondArena's pinned container is another one.
  qsar_bioconcentration waits for its shipping verdict and stays unbuilt.

## 2026-10-14 (SMILES become RDKit descriptors; the string is dropped)

Lennart's decision on apistox's issue 1 of the 2026-10-07 review page: one way to ship a molecule, the same for every
SMILES dataset. A SMILES holds the whole structure (as character n-grams alone it scores ROC AUC 0.69 to 0.77), but next
to descriptors it adds nothing. Untuned LightGBM on the first 15 splits of each definition (apistox: its 4 windows),
descriptors only / with the SMILES as character 2-4-grams (TF-IDF, 64 SVD components) / with a Morgan fingerprint (1,024
counts): drug_induced_autoimmunity_prediction 0.835 / 0.810 (worse on 15 of 15 splits) / 0.849; qsar_bioconcentration
(macro AUC) 0.735 / 0.723 / 0.743; apistox 0.838 / 0.848 (standard error 0.023 over its 4 windows) / 0.853. TabArena's
default text embedding of the SMILES scored ROC AUC 0.58 alone on apistox. Fingerprints stay out (a gain of 0.01 to
0.015 for about 1,000 sparse columns).

- New `data_foundry.v2.rdkit_descriptors` (`src/data_foundry/v2/chemistry.py`, tests in `tests/test_v2_chemistry.py`):
  RDKit's 2D descriptors of a SMILES column as `rdkit_*` columns, constant and copied descriptors left out, RDKit
  2026.03.6 pinned in the `build` extra (another version is an error). It was apistox's own function.
- `apistox`: the descriptors come from the shared helper (same 199 columns) and `SMILES` is dropped, and with
  it the accepted `dataset_identifier_column` warning. 1,035 rows, 204 features; the task probes still flag `unstable`
  (LightGBM ROC AUC 0.82, standard error 0.066). Not built yet.
- `qsar_bioconcentration`: RDKit's descriptors of the repaired SMILES (193 columns) join the source's 9 Dragon
  descriptors, and `SMILES` is dropped with its accepted warning. Macro AUC with LightGBM 0.735 -> 0.752 (better on 13
  of 15 splits). The 9 descriptors gave 61 chemicals the values of another (14 of them with another class); with
  RDKit's, every chemical has its own (decision table). 776 rows, 202 features; no task-probe flag. Not built yet.
- `drug_induced_autoimmunity_prediction`: `SMILES` dropped; the source's RDKit descriptors stay. Without the SMILES 9
  pairs of stereoisomers share every descriptor (PubChem names: quinine and quinidine, and lovastatin, fluticasone
  propionate, enalapril, fluvastatin, lisinopril, pravastatin, carbidopa and streptomycin each entered twice with other
  stereo marks; 3 pairs across the source's train and test files). One row of each pair with one label is kept, both
  streptomycin rows (one positive, one negative) are dropped, as for qsar_oral_toxicity: 597 -> 587 drugs, 140
  positive (decision table). Its open `dataset_identifier_column` warning (the SMILES) is gone. New checksum (rebuilt, next entry
  above).
- Curation guidelines (and the dashboard's guidelines page) and the add-dataset patterns: a SMILES column becomes
  `rdkit_descriptors` and is dropped, then check for stereoisomer copies. The verify-dataset task-probe cases table
  has apistox's new numbers.

## 2026-10-14 (apistox shipped; string columns in the probes; the review page as a skill)

- `apistox`: Lennart's verdict on the 2026-10-07 review page is ship. Record follow-ups: the reference is the
  published data descriptor (Scientific Data 12:5, 2025) instead of the preprint, and the licence history is noted
  (CC BY-NC 4.0 now, CC BY 4.0 in Zenodo v1); `original_source` already said Other. Its task summary joins the
  task-summary review page for Lennart's marks. Not built yet.
- Probes: `leak_probes.py` now also fits each string column of more than 50 values alone as text, and all features
  with those columns (TF-IDF + SVD fitted on the train side), so a text or a SMILES whose content gives the label away
  shows up; before, string columns were only checked for copies. `task_probes.py` encodes strings that are mostly one
  token (a SMILES, a code) by character 2- to 5-grams instead of words, which matched only whole repeated values.
  apistox: the SMILES alone ROC AUC 0.733, all features 0.874, with the SMILES 0.894;
  drug_induced_autoimmunity_prediction: 0.730, 0.817 and 0.814.
- New skill `review-added-datasets`: builds the curator's review page for a batch of added datasets from the run
  report (`build_review_page.py`, template, report format, tests in `tests/test_review_page.py`), locally or as a
  Claude artifact, and says how to read and apply the decisions. The 2026-10-07 page is now built by it.
  `markdown-it-py` joins the `curation` extra. CLAUDE.md, AGENTS.md, GETTING_STARTED.md and the add-dataset and
  triage skills describe the whole pipeline (AI triage, the curator's check, AI adds, the curator reviews, build). GETTING_STARTED.md leads with that
  workflow as the recommended one (the batch route first, one dataset by hand second).
- Curation guidelines: PubChem's literature endpoint answers automated requests with a reCAPTCHA; use PUG REST and
  PUG-View.

## 2026-10-14 (rebuild: the 15 datasets whose data, splits or score changed in the review)

- Rebuilt with `build_all.py --only` from the uncommitted tree (`git_sha` f93df19-dirty): 15 of 15 ok, every container
  reloads with its checksum, no new warning against the committed READMEs; 101 s of build time, peak 6.2 GB. A check
  build from only the traced raw files gives the same checksums for all 15. New UUIDs:
  `california_house_prices_2020` 01a13a7d-c063-762b-b7dc-6a2ca7c1ce3a, `cirrhosis_patient_survival_prediction`
  01a13a7d-c2bd-721a-88c1-f86443866b1e, `concrete_compressive_strength` 01a13a7d-c2ed-79de-abb8-3476f95e6667,
  `fiat_500` 01a13a7d-c2b9-7b23-b0e5-6674aebfe128, `food_delivery_time` 01a13a7d-c2cc-70a6-b90d-08296c319c01,
  `heart_disease_va_long_beach` 01a13a7d-c2bc-7803-9ff6-e0e192d554de, `hiva_agnostic`
  01a13a7d-c4ee-761a-9292-ce1cd880e6c6, `hr_analytics` 01a13a7d-c2d4-7c87-a495-ce69f1b8a4c4,
  `mercedes_benz_greener_manufacturing` 01a13a7d-bd39-75dc-a072-0eebbfca32cb, `obesity_estimation`
  01a13a7d-c2ba-7a4d-bb80-1eb0032878a9, `pva_revenue_prediction_kddcup98` 01a13a7d-f16c-7ca9-ac9e-41670aefdb4e,
  `qsar_biodeg` 01a13a7d-c2bf-742d-b04d-f9b569da1f3d, `santander_transaction_value`
  01a13a7e-21ec-73e1-9f26-93bf3dd5ae2b, `sberbank_housing_market_forecasting` 01a13a7d-c2eb-7775-8b3c-17b7b9a68ca7,
  `website_phishing` 01a13a7d-c2c0-77e5-80e6-a355a6e11902.
- Task probes on the 15 built containers: no flag except `hr_analytics` `no_spread` (accepted above).
- The superseded containers of these 15 (about 100 MB) were deleted once the checks above passed (Lennart). 76 of
  the 124 built definitions are still stale (notes, tags or summaries changed since their build), so the table shows
  "not built" for them.

## 2026-10-14 (concrete_compressive_strength grouped by mix; the hidden-group probe checks composite keys)

- `concrete_compressive_strength`: grouped by mix (was IID, the split shipped in TabArena v0.1 and BeyondArena;
  rebuild needed). The 1,030 tests are 428 mixes, a mix being its amounts of the seven ingredients; 182 mixes are
  tested at several ages (up to 20 tests), and on the shipped random splits 73% of the test rows had their mix in
  training at another age. The new group column `mix` is built from identical values in the seven ingredient
  columns and is no feature; 10 x 3 grouped splits, 142-143 test mixes per fold. R^2 random against grouped:
  LightGBM 0.925 / 0.874, MLP 0.916 / 0.838, ridge 0.816 / 0.804; the ranking changes. Decision: Lennart, record
  `concrete_compressive_strength.md`. `dataset check`: 0 errors. Regime updated in `README.md`.
- Probes: `hidden_groups.py` missed concrete because it only tests single columns (the fractional ingredient amounts
  are no candidates) and its near copies need 10 informative columns. It now also checks keys of all columns but one
  (two when none counts and the data is small enough): rows identical except in an age, a time or a frequency. A key
  counts when its rows that differ are at least 10% of the rows and four times the share with independent columns,
  it holds a column of at least 20 values, and keys over 100 rows are left out. Over all 177 definitions the keys hit
  concrete `(all but Age)`, airfoil `(all but frequency)` (its run) and amazon_employee_access `(all but RESOURCE)`
  (next to its `MGR_ID` hit, no action on 6 Oct); details in the verify-dataset skill's `references/task_probes.md`
  (hidden groups).

## 2026-10-14 (task summaries review: Lennart's decisions on the open questions)

- `mutual_funds_india` retired (record `No (Retired)`, `No Good Target / Scientific Discovery`; folder removed,
  `v2_path` cleared; the definition stays in git history at f93df19). The label is the trailing 3-year return at one
  snapshot (April 2023), a window all funds share, so no decision uses the prediction. 124 of the 125 datasets built
  on 2026-10-06 remain, 177 definitions in all; counts updated in `README.md`, `LEAK_AUDIT.md`, `datasets/README.md`.
- Changes to rows, labels or splits (rebuild needed):
  - `obesity_estimation`: the 10 exact copies among the 498 real answers are dropped (488 rows). Each repeats all 16
    answers, age, height and weight, and 4 of the 8 groups are neighbouring rows: one person sending the form again.
  - `hiva_agnostic`: the challenge's 384 labelled validation compounds are added (4,229 compounds, 149 active); every
    descriptor that copies an earlier one is dropped (188; a fixed list dropped 99 of them before). The
    `dataset_pure_feature_value` warning is gone.
  - `california_house_prices_2020`: the 2,480 homes whose last sale is on or after their listing date are dropped
    (the listing describes an earlier sale; 125 give the predicted price as the last sale price). 39,048 rows; LightGBM
    RMSE on the shipped windows 0.196 before, 0.140 after. Listings older than 6 months stay.
  - `sberbank_housing_market_forecasting`: the 1,126 sales whose build year is after the sale stay (1,124 look like
    flats sold before completion). 28,321 rows.
  - `food_delivery_time`: 424 restaurant latitudes (159 longitudes) get their sign fixed; the 3,630 restaurants at
    (0, 0) stay; the notes say the delivery point is the restaurant plus one of 12 fixed offsets.
  - `website_phishing`: binary, phishing (702) against legitimate (548); the 103 suspicious sites are dropped (the
    donors' judgement of the same nine signals, ROC AUC 0.987 from them). The signals keep their raw codes -1/0/1,
    whose documented direction does not match the data. Metric `roc_auc`. `dataset_pure_feature_value` (all 167
    sites with `popUpWidnow` = 1 are phishing) is accepted: the same reversed coding, a page property.
  - `cirrhosis_patient_survival_prediction`: a new task. It regressed the log time to death over the 161 patients
    who died; with follow-up ending in July 1986 for all, a late patient entered only with an early death (right
    truncation). Now binary, death or liver transplant within 5 years of registration (`roc_auc`), over the 304
    patients registered early enough to be followed 5 years (107 events), with the registration order taken from the
    IDs. Untuned ROC AUC 0.87-0.89; registration order alone 0.52. Back on the review page for Lennart's marks; the
    precedent in the add-dataset patterns (§D.14), the leak-check table and `LEAK_AUDIT.md` now describe it as right
    truncation.
  - `hr_analytics`: built from the train file of Analytics Vidhya's Student DataFest 2018: The Data Supremacy
    (18,359 enrollees, 13.2% looking for a job change; source Other, the contest page, year 2018, licence unknown).
    Kaggle's `aug_train.csv` (19,158 rows, 24.9%) adds 2,623 rows of the hackathon's unlabelled test file, all
    labelled 1, whose labels do not behave like real ones. Untuned ROC AUC 0.62-0.63 instead of 0.80; the task probes
    flag `no_spread` (LightGBM +0.012 over random forest), accepted by Lennart (a real signal with a low
    ceiling; row in the task-probes cases table).
  - `fiat_500`: one row per car, its first listing (1,434 of 1,538 rows). 104 rows repeat the model, engine power,
    age, mileage and owners of another: 18 exact copies, most one results page after the first, and cars with an odd
    mileage listed at up to 9 places a median 396 km apart.
- Metadata and notes only:
  - `emscad`: the `ForcedIIDFromTemporal` tag of the previous entry is removed again (the grouped split marks the task
    as Non-IID); a note says the lost dates could also have served modelling.
  - `bank_customer_churn`: licence `None` (Kaggle names none), `meta_license_unknown` accepted.
  - `jm1`: the source URL is the right PROMISE page (it serves the file over http, 404 over https); the download is
    OpenML 1053, byte-identical to it, with a tested command.
  - `labour_inspection_compliance`: the notes say January 2012 to June 2019 (the Dataverse description).
  - `lending_club`: the always-empty joint-applicant fields are no longer built; same data (609,544 x 82). Typos.
  - `ljubljana_breast_cancer`: the notes say the bands become their midpoints.
- Nothing of these is open on the review page any more; `hr_analytics` and `cirrhosis_patient_survival_prediction` got
  Lennart's agreement on their new versions.

## 2026-10-14 (task summaries review: the side findings fixed)

Lennart's marks and notes on the review page (scope: the 125 built datasets and the 2026-10-07 run's `ship` verdicts,
129 definitions). The findings of 54 datasets are settled, most by a fix in the definition, the record or both;
`dataset check` gives 0 errors on each edited definition. Nothing is rebuilt.

- Changes to data or scores (rebuild needed):
  - `pva_revenue_prediction_kddcup98`: the birth-date filter (`.str.endswith("00")` on the zero-padded DOB) dropped
    every donor without a birth date (DOB 0); now only the 2 rows with birth month 00 go and a missing DOB stays
    missing. 191,769 rows instead of 144,095.
  - `qsar_biodeg`: `biodeg.csv` has no header row and the first chemical was read as one; now `header=None`, 1,055
    rows with 356 readily biodegradable, as UCI lists.
  - `heart_disease_va_long_beach`: cholesterol 0 (49 rows) and resting blood pressure 0 (1 row), an undocumented
    missing code, become missing; scores unchanged.
  - `santander_transaction_value`: metric `rmse` instead of `rmsle`. The stored target is already log1p, so `rmsle`
    logged it a second time; RMSE on the stored target equals the competition's RMSLE. This dataset's scores change.
  - `mercedes_benz_greener_manufacturing`: `data_tags` listed `Non-IID` by hand, which turns off the automatic
    regime tags, so the metadata missed `Temporal`; now `("Anonymized",)`.
- Tags: `ForcedIIDFromTemporal` for `home_credit_default_risk` (the `DAYS_` columns are relative to the
  application), `santander_transaction_value` (1,415 row pairs hold the same series shifted by one step),
  `taiwanese_bankruptcy_prediction` (1999-2009, no year per row) and `emscad` (no dates, grouped by poster).
  `sepsis_prediction_1m` keeps its hand-written regime tags, with a code comment why.
- Sources and metadata:
  - `miami_housing`: source OpenML (43093, 2021-09-24, the first upload); the Mayer et al. 2021 citation OpenML
    asks for is added.
  - `sberbank_housing_market_forecasting`: it cited the Home Credit competition, now the Sberbank one.
  - `immoscout_german_house_prices`: year 2020 (the scrape date); a note names the first upload, the deleted Kaggle
    dataset `german-house-prices`.
  - `cirrhosis_patient_survival_prediction`: licence CC BY 4.0 (it said `IID`).
  - `bank_customer_churn` year 2022; `cardiotocography` source_url as a DOI link; `clock_protein_toxicity` domain
    chemistry & material science.
- Notes or summaries now match the code, or state what it does: `5g_energy_consumption`, `anes_voting_2026`,
  `bad_customer_detection`, `climate_model_weather_forecasting_1m`, `consumer_complaints_1m`, `cooking_time_1m`,
  `credit_approval`, `delivery_eta_1m`, `dementia_prediction`, `diabetes_130_us`,
  `drug_induced_autoimmunity_prediction`, `early_stage_diabetes_risk_prediction`, `ecoli_proteins`,
  `eryhemato_squamous_disease`, `fiat_500` (notes written; they were `N/A`), `forest_fires`,
  `garments_worker_productivity`, `heloc`, `hepatitis_survival_prediction`, `hiva_agnostic`,
  `home_credit_default_stability_1m`, `hotel_booking_demand`, `mercedes_benz_greener_manufacturing`, `musk`,
  `naticusdroid_android_permissions_dataset`, `porto_seguro`, `qsar_tid_11` (names the target, human thrombin),
  `sberbank_housing_market_forecasting`, `sepsis_prediction_1m`, `coffee_rating_prediction`.
- Checks the review asked for, with no change to data:
  - `heart_disease_cleveland`: `ca` and `thal` come from noninvasive tests before the angiography (Detrano et al.
    1986), so no leak.
  - `wine_world_cost`: no description states the wine's price; removing every sentence with price or value words
    moves R² from 0.724 to 0.721.
  - `qsar_fish_toxicity`: the 24% of rows that share their descriptors are isomers with different LC50; one row
    per vector gives R² 0.571 against 0.577. The record's "might have a leak" is removed.
  - `obesity_estimation`: the first 498 rows are the real answers (their class counts equal Fig. 1 of the data
    paper).
  - `heart_failure_followup_survival`: whether follow-up ended on one date for all cannot be determined; the
    summary says so.
- Records: `lung_cancer` (original source: the PNAS 2001 supplement), `qsar_aquatic_toxicity` (problem type
  Regression), `regensburg_pediatric_appendicitis` (source Other, Zenodo first), `sf_permit_time` (the CC's windows),
  `otto_group_product_classification_challenge`, `credit_approval`, `eryhemato_squamous_disease`, and the records
  of the datasets above, plus assessments for `hr_analytics`, `website_phishing` and `mutual_funds_india`.
- Open, on the review page with evidence and a proposal: `mutual_funds_india` (retire), `hr_analytics` (build from
  the hackathon's train file), `website_phishing` (binary, raw codes), `sberbank_housing_market_forecasting` (keep
  the 1,124 presales), `immoscout_german_house_prices` (confirm the source reading), and from before
  `california_house_prices_2020`, `concrete_compressive_strength`, `food_delivery_time`,
  `cirrhosis_patient_survival_prediction`, `emscad`, `fiat_500` and the `bank_customer_churn` licence.
- 90 of the 125 built definitions no longer match their build (64 before), so the table shows "not built" for them
  until the rebuild.

## 2026-10-14 (task summaries: `task_summary` in every definition)

- New in Data Foundry v2: `task_summary = TaskSummary(...)`, the first attribute of a definition and the first README
  section ("In brief"): the question, the use case (who uses the prediction, when, for which decision), one row, what
  is predicted, what is known then, what the test data stands for and our changes, then the judgement `fit`
  (`direct`, `approximate` or `none`) with its reason. Not stored in the container, so no checksum changes.
  `dataset check` reports `definition_summary_missing` and `definition_no_use_case` (errors) and
  `definition_summary_long` (warning, a field over 70 words). The format, field rules and examples are in the
  add-dataset patterns ("In brief"); verify-dataset checks it as rubric item 16; the template scaffolds it.
- All 178 definitions have one: seven pilots written by hand, the rest by nine writers from each definition, its
  notes, README and record, checked field by field against the definition. Proposed fits: 82 direct, 94 approximate,
  2 none (mutual_funds_india: the label is the trailing 3-year return of one shared window; cirrhosis_patient_survival_
  prediction: only patients who died before follow-up ended are in, which the 2026-09-30 decision kept on purpose).
  The two `none` definitions fail `dataset check` until Lennart decides. The review page:
  https://claude.ai/artifact/JFjHwm9PKaVQYjHWrHHHkG (summary first, then the proposed judgement, then the marks).
- The writers' side findings (two bugs that change data: qsar_biodeg reads its first chemical as the header row,
  pva_revenue_prediction_kddcup98 drops every donor without a birth date; about seventy mismatches between notes,
  code, record and README, and unstated facts) are listed per dataset on the review page; the next entry lists the
  fixes.
- All READMEs regenerated with `dataset check` (no build), so each now opens with its summary.

## 2026-10-14 (analcatdata_supreme retired: no use case)

- `analcatdata_supreme` retired (record `No`, `No Good Target / Scientific Discovery`; folder removed, `v2_path`
  cleared; the definition stays in git history at 86272ac). Its label counts Congress's responses to a Supreme Court
  ruling in one calendar window, 1979-1988, shared by rulings of 1953-1988, not in a fixed time after each ruling, so
  the task cannot stand for forecasting the response to a new ruling; it only looks back at which rulings drew
  responses. The rule is now in criterion 3 of the curation guidelines. 178 definitions remain, 53 of them unbuilt.

## 2026-10-13 (alfa_battle_2_0_task_2: features of the top solutions)

- The organizers' 127-feature baseline is replaced by the aggregates the competition's top solutions share (1st place
  and 4th private place slides, 9th place code): 513 features over amounts restored to rubles
  (`exp(amnt * 17.8209) - 1`; 98.8% whole rubles) - amount, gap and recency statistics; count share, amount share and
  mean amount per value of ten coded columns and the 30 most frequent `mcc` and `card_type` codes; distinct values,
  mode and last values; money in against out, salary-like inflows and twelve 30-day blocks; daily activity; a balance
  proxy; the last 30 and 90 days. Label-based encodings, embeddings and sequence-model scores stay out.
- Untuned LightGBM on the shipped windows: ROC AUC 0.787 / 0.771 / 0.772, against 0.774 / 0.757 / 0.763 with the
  127. The leak probes find nothing to answer (single features at most 0.614, no exact copies); the task probes raise
  no flag (50k rows per side: LightGBM and linear 0.744, before 0.724 and 0.705). `dataset check`: 0 errors, 0
  warnings; peak 16 GB, 11 minutes with `_prepare_raw_files`. Checksum `v2:0329b674…` (not built).
- The notes' "top teams reached 0.776 with aggregates alone" was 9th place; 1st place's boosting reached 0.780.
- Record: `domain` finance, tag `Non-IID (Grouped)` removed (clients are a split filter only), the ODS.ai page added.

## 2026-10-12 (aeolus_1m: Lennart's review; two-week windows, history from 2023)

- Test windows: two weeks instead of one (2024-12-18..31, 12-04..17, 11-20..12-03; 25.8%, 16.7% and 17.3% late;
  258,551, 256,013 and 269,272 flights). Two of the three newest weeks were the holiday peak (26.5% and 25.1% against
  20.8% for 2024); now one window is.
- History: flights from 2023-01-01 on (12,930,302 of 54,674,003; `HISTORY_START`, and `_load_raw` reads only them),
  each train side a random 1M of them. TabReD's random sample of all nine years put about 11.5% of each train side in
  2024 and mixed in COVID-19; a model refit every two weeks trains on recent data with the previous holidays, and
  the authors' own benchmarks use 2024 alone. The per-week comparison of history pools did not decide it (each pool
  best in one week); on the new windows all nine years and 2023 on score alike (untuned LightGBM ROC AUC 0.632 /
  0.609 / 0.620 against 0.625 / 0.613 / 0.622).
- Gone with the history: the precipitation code (2016-2018) and its decision, and the one flight recorded twice
  (2018). Weather timing, probes and notes recomputed: destination weather after the departure for 1.94% of the
  flights (0.9-1.0% per window), all destination weather worth 0.006-0.024 ROC AUC; task probes no longer flag
  `no_spread`. A check peaks at 9 GB instead of 35 GB. 1,785,315 rows; checksum `v2:d04fe7bd…` (not built).
- Kept as implemented: target `ARR_DEL15` (record `problem_type` Binary Classification), the weather as released,
  the flight number as a categorical. The release's data problems are noted only. `airlines` and
  `airlines_depdelay_10m` get a dated note that aeolus covers US flight delays.

## 2026-10-12 (account_debt_south_africa: Lennart's review)

- Tagged `ForcedIIDFromTemporal`: the file is one extract without dates, so the bad-debt status at the extract stands
  in for the forecast the data card aims at. The split stays IID (a municipality scores its own accounts); a new
  bullet gives the cost for a municipality not in the data, which has no column: LightGBM ROC AUC 0.877 random,
  0.843 by file blocks of 2,500 rows, 0.786 by thirds of the file.
- `TotalElectricityBill` and `HasIDNo` stay, with rewritten bullets: the electricity signal is mostly whether the
  municipality bills it at all (no trace of cut-offs within the window), and the data card describes the ID number
  as a property of the holder. The anomaly bullet now names the Unknown-category run at the end of the file (rows
  134,192-138,276), which stays. Notes shortened to 493 words; checksum `v2:14c792e2…` (not built).

## 2026-10-12 (few_minority decisions: alvin retired, seven kept; three more sources set to the first publication)

- `alvin_smart_money_management_classification_challenge` retired (record `No`, `Too Small`; folder removed,
  `v2_path` cleared; the definition stays in git history at 86272ac). Only Train.csv has labels, so its three windows
  hold 27-41 test purchases from 5-12 users, Shopping has 2 test rows over all windows, and the 8 rows of the rarest
  classes carry 51-54% of window 1's log loss. 179 definitions remain, 54 of them unbuilt.
- Kept after the multiclass `few_minority` flag (a dated note in each record): forensic_glass_identification,
  ljubljana_primary_tumor, mic, sarcoma, micro_mass, asp_potassco_classification and
  force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition. Their short classes are 0.7-18%
  of the test rows and carry 3.9-25% of a random forest's log loss; force_2020's two classes have thousands of rows
  and miss a fold only because the well split leaves them out (already accepted as `splits_test_class_missing`).
- The rule (Lennart): a short class in a multiclass task is `Too Small` only when its rows decide the score or a fold
  holds a handful of units in all. It is rule 8 in the verify-dataset `task_probes.md`, with case rows for the eight,
  and in the `Too Small` paragraph of the curation guidelines.
- `source` now names the first publication for three built definitions the source sweep had left as UCI; each
  downloads UCI's copy, and its `download_description` says so. Records follow (`original_source: Other`, the link
  added). All three need a rebuild for the new metadata; aps_failure and biomechanical_orthopaedic_prediction join
  the 64 stale built datasets of the entries below, 66 in all.
  - `biomechanical_orthopaedic_prediction`: Appendix A of da Rocha Neto's 2006 master's thesis (UFC) lists all 310
    samples (60 disc hernia, 150 spondylolisthesis, 100 normal, as in UCI 212). The empty bullet in its notes is
    gone. The bibtex still cites the 2011 paper: the thesis repository did not respond, so its title is unchecked.
  - `in_vehicle_coupon_recommendation`: Wang et al. (2017, Sec. 6 and references) published the survey as a
    ResearchGate deposit (publication 318645502); UCI 603 is a later copy.
  - `aps_failure`: the IDA 2016 Industrial Challenge (Scania) released the data; UCI 421 re-hosts its
    `ida2016challenge.zip`. The challenge site is gone, so `source_url` is its 2016 capture in the Internet Archive.

## 2026-10-12 (Lennart's decisions on the open points; four datasets retired; 64 built datasets need a rebuild)

- `sf_permit_time`: each window trains only on permits issued before it starts, with a 6-month gap, over 8 half-year
  windows (2020-H1 to 2023-H2). 3.0-6.7% of earlier permits are still open at a window start; with them LightGBM
  learned the COVID slowdown from labels issued later (2020-H2: RMSE 1.19, 1.52 without them), and a 1-month gap would
  leave 21-34% of the newest filings open and bias predictions 0.58 log-days low. The Current Status filter (issued
  or complete, which drops 4.1% of the cohort for later events) is an `Anomaly:` bullet. The task probes now flag
  `no_spread` (kept, case row added; re-check with tuned runs). Checksum `v2:8010ef7e…`.
- `coad_colon_adenocarcinoma`: the copy-number block is dropped (36,355 features). Copy-number changes define CIN
  against GS, so the realistic task is the subtype from expression and methylation; random forest macro ROC AUC 0.923
  without the block, 0.935 with it. No task-probe flag.
- `apistox`: RDKit's 2D descriptors (199 of 217; the rest constant or copies) next to the SMILES, RDKit 2026.3.6
  pinned in the `build` extra; mean ROC AUC on its windows 0.79 / 0.71 without, 0.83 / 0.82 with them.
- Retired (records `No`, folders removed, `v2_path` cleared; the definitions stay in git history at 86272ac): brca_breast_cancer, glioblastoma and ov_ovarian_cancer,
  whose labels come from unsupervised learning (PAM50, expression subtypes, NMF clusters), and
  central_international_medical_college_and_hospital_health_risk_prediction (`Trivial`: the NEWS2 chart on the vitals
  it ships). The rule is in the curation guidelines (criterion 3). churn_telco_europa (never added) is `No`: Chilean
  customers under a European name, personal data, and active lines and churners measured on different dates.
- `year` (Lennart): the year the data was first published, at the publication `source_url` names; a source that grows
  over time takes the year of the snapshot we pin. 49 definitions changed (43 built), sf_permit_time,
  consumer_complaints_1m and kickstarter are 2026, and 40 records follow. Written into the `year` docstring, the
  add-dataset patterns and the record template. Unclear and left as they are: bank_customer_churn,
  immoscout_german_house_prices, framingham_heart_study_fhs, lending_club, pancreatic_cancer_mouse_detection,
  sat11_hand_algo_runtime, dementia_prediction, airfoil_self_noise and the three QSAR siblings.
- Probes: `hidden_groups.py` adds clusters of near-identical rows as a candidate group (it finds qsar_oral_toxicity's
  compound families; no IID dataset hits) and reports how often entities recur across the cutoff of temporal tasks;
  two crashes fixed. `task_probes.py` checks `few_minority` per class for multiclass tasks; open for the curator (rule
  7), it now flags alvin_smart_money_management_classification_challenge, asp_potassco_classification,
  force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition, forensic_glass_identification,
  ljubljana_primary_tumor, mic, micro_mass and sarcoma (and the retired brca_breast_cancer).
- Stale until the next build (`dataset list` marks them), 64 built datasets:
  5g_energy_consumption, airfoil_self_noise, amazon_employee_access, biogeographical_ancestry_prediction,
  blood_tests_drink_prediction, body_density_prediction, california_house_prices_2020,
  cirrhosis_patient_survival_prediction, clock_protein_toxicity, coffee_rating_prediction,
  concrete_compressive_strength, consumer_complaints_1m, credit_card_clients_default, dementia_prediction, diamonds,
  early_learning_predictors, early_stage_diabetes_risk_prediction, emscad, eryhemato_squamous_disease,
  gallstone_disease, garments_worker_productivity, heart_disease_cleveland, heart_disease_hungary,
  heart_disease_va_long_beach, heart_failure_followup_survival, heloc, hepatitis_c_prediction,
  hepatitis_survival_prediction, home_credit_default_stability_1m, hotel_booking_demand, houses, hr_analytics,
  ieee_fraud_detection, in_vehicle_coupon_recommendation, jm1, kdd_cup_09_appetency, kickstarter,
  labour_inspection_compliance, lending_club, ljubljana_primary_tumor, marketing_campaign, mercari_price_suggestion,
  mercedes_benz_greener_manufacturing, miami_housing, mic, musk, naticusdroid_android_permissions_dataset,
  online_shoppers_purchasing_intention_dataset, polish_companies_bankruptcy, pva_revenue_prediction_kddcup98,
  regensburg_pediatric_appendicitis, rossmann_store_sales, sberbank_housing_market_forecasting, sdss_17,
  sepsis_prediction_1m, sepsis_survival_minimal_clinical_records, sf_permit_time,
  south_africa_coronary_heart_disease, splice, student_portuguese_performance, superconductivity,
  taiwanese_bankruptcy_prediction, thyroid_discordant, website_phishing
  Every README was re-checked: 0 errors, and the warnings are those of the table.

## 2026-10-12 (Lennart's review of the cross-dataset items; 32 built datasets need a rebuild)

- Framework (`src/data_foundry/v2/`, tests added): a multi-line `splits_comment` is dedented like the other text
  fields; the README lists the feature types the standard steps applied (a `_feature_types` that reads dtypes showed
  "0 categorical"); the hash of `_prepare_raw_files` also covers the module constants it reads, as written; `dataset
  new` fills `domain` and `source` from the record when the value names one schema value. ruff ignores C416 (its
  fix once broke qsar_bioconcentration), which uses its dict comprehension again.
- `mic` read its file without `header=None` and lost its first patient (1,699 rows instead of 1,700).
- `source` convention (Lennart): the first publication, not a re-upload; Kaggle only when the data first appeared
  there or no other source is found. Written into add-dataset's `dataset_patterns.md` §A, the `source` docstring and
  the record template. Changed: 10 of the 59 new definitions (cdc_diabetes_health_indicators, nyc_taxi_trip_duration,
  rain_in_australia and house_sales to their government publishers, corporate_credit_rating to GitHub,
  credit_card_customers to the LEAPS case, the three MLOmics datasets to the authors' repository,
  open_university's URL) and 16 built ones (5g_energy_consumption to Zindi; body_density_prediction, sdss_17,
  south_africa_coronary_heart_disease, heloc, lending_club, cirrhosis_patient_survival_prediction,
  heart_failure_followup_survival, sepsis_survival_minimal_clinical_records, mic, biogeographical_ancestry_prediction
  and jm1 to Other with the original publication; new URLs for emscad, sepsis_prediction_1m, dementia_prediction and
  gallstone_disease), with the records' `original_source` aligned. Left as they are, for lack of evidence:
  bank_customer_churn, aps_failure, miami_housing, immoscout, pancreatic_cancer_mouse_detection.
- 32 built datasets are stale until the next build (`dataset list` marks them): the 19 with a multi-line
  `splits_comment` (airfoil_self_noise, california_house_prices_2020, coffee_rating_prediction,
  consumer_complaints_1m, dementia_prediction, emscad, garments_worker_productivity, home_credit_default_stability_1m,
  hotel_booking_demand, ieee_fraud_detection, in_vehicle_coupon_recommendation, kickstarter, lending_club,
  mercedes_benz_greener_manufacturing, musk, rossmann_store_sales, sberbank_housing_market_forecasting,
  sf_permit_time, superconductivity), mic, and the 12 other built ones whose source changed. Their READMEs and all 59
  new ones were re-checked: 0 errors, and the warnings are the open ones of the table.
- Records: colleges (OpenML 42727, the College Scorecard file of 2013-14), indabax_drc_2022, indabax_eswatini_2022 and
  melbourne_housing_snapshot set to `No` + `Duplicate` (names kept); a record for the simulated OpenML 46372 copy
  (`corporate_credit_rating_cat_data_set_ratings_raitings_duplicate`, AHDS); churn_telco_europa flagged
  `Ethical Issue` (Chilean national ids and mobile numbers, also on OpenML 44228); notes on OpenML 43838 (account debt),
  the Aeolus release and a paper to get for churn_telco_south_asia; related links moved out of `source_links`
  (nyc_taxi_trip_duration, melbourne_housing_market). The two dev notebooks in `_too_late_to_add` are renamed to their
  records' names, which sets `notebook_path`.
- `TODO.md` stays deleted; the links to it now point to the records and this file. `GETTING_STARTED.md` no longer
  lists datasets or counts. `verify-dataset/references/task_probes.md` has the six case rows of the 2026-10-07 run.
  `catboost_info/` is gitignored.
- Probes: `generated_probes.py` flags columns drawn independently (label included) and values drawn uniformly within
  each class; neither fires on the working copy. `leak_probes.py` screens wide data to its 300 most informative
  columns for the single-feature fits (coad: about 5 hours to 10 minutes), writes `--out` JSON, scores macro ROC AUC
  over the classes present in a test fold (as `group_probes.py` now does), and checks string columns for copies.

## 2026-10-12 (shorter curation notes for the 59 definitions of 2026-10-07)

- Lennart found the `curation_comments` of the 59 new definitions too long (79,947 words in all, median 1,304; the
  older 125 have a median of 95). They now hold 28,266 words (median 495): one bullet per step or decision of the
  code, and numbers only where they decide a call. The cut evidence (provenance, probe output, verification history,
  long quotes) stays in the curation records, `NEW_DATASETS_ISSUES.md`, the `_decisions` tables and git history. The
  house format in add-dataset's `references/dataset_patterns.md` now asks for about 400 words.
- Only the comments changed, apart from small fixes found on the way: `force_2020_…` has a bullet for its categorical
  columns; `zillow_prize` labels the post-sale tax-delinquency snapshot `Potential leak, kept on purpose:`; stale
  pointers to the comments were removed in `college_scorecard`, `differentiated_thyroid_cancer_recurrence` and
  `rosbank1`; `african_credit_scoring_challenge` no longer scores a drop the context settles; the glioma decision
  title no longer calls Primary_Diagnosis a copy of the label; `stroke_prediction` lost a stale bullet that
  contradicted the code (bmi is dropped).
- Every README was regenerated by `dataset check`: 0 errors and the warnings as before. The checksums change because
  the comments are part of the metadata; rows and splits do not. `NEW_DATASETS_ISSUES.md` carries the new checksums.
  None is built.

## 2026-10-12 (2_month_survival_rate_prediction: both phases, phase II physiology moved back into its rows)

- In SUPPORT2 (hbiostat's `support2.csv`, also UCI 880) most phase II rows hold another patient's day-3 physiology
  (the 14 columns meanbp to urine). The study's own data, ICPSR 2957 V2 parts 9 and 10 (public-use, login download by
  Lennart), show where each patient's block is: in `support2.csv` itself, at another phase II row. The definition
  links each row to its ICPSR patient on ten columns both files hold on the patient's row, finds the row that holds
  the patient's ICPSR day-3 values, and takes the block from there. Every value of the dataset comes from
  `support2.csv`; the ICPSR files are read at build time from `local-data-warehouse/2_month_survival_rate_prediction/
  icpsr_2957/` and are not in git (their terms forbid redistribution; Lennart's call to ship only support2's values).
- The dataset now holds both phases: 8,967 patients alive after day 3 (was 4,232, phase I only), 33.4% positive,
  25 features, 3 x 3 folds. adls and adlsc are dropped (Lennart's review): the interviews took place on study days
  2-7, so a missing surrogate answer depends on whether the stay lasted until the interview (46% missing for stays
  that ended by day 7, 24% for longer ones); adlp, edu and income stay. Probes: random forest ROC AUC 0.806, no flag.
- Checksum `v2:12056202e362b4fb06ec43d52b932206008964f408d086b4df896e668d524ed7` (pandas 2.3.3 and 3.0.6). Not built.
- The record drops the `Multi-target` tag (Lennart's review); its comments hold the procedure and the evidence.
- `rebuild-working-copy/scripts/build_one.py` also traces `pd.read_fwf`, which reads the ICPSR files.

## 2026-10-12 (single-column scores only where they decide a call; three new definitions)

- Lennart's rule, now in add-dataset's `references/dataset_patterns.md` §F: a column dropped for what it is (recorded
  after the prediction point, an outcome, a model output or estimate fit with the label, a field the source says not
  to use) gets its reason and no score; a correlation or ROC AUC alone is shown only where the values decide the
  call, computed with pandas `corr` and sklearn `roc_auc_score`.
- `2_month_survival_rate_prediction`: the dropped-columns table lists the reasons only, and `curation_comments` no
  longer score the drops the source advises (sps, surv2m, surv6m, aps, prg2m, prg6m). The phase I / phase II table
  keeps its numbers, now from pandas and sklearn instead of two hand-written helpers (same values). Checksum
  `v2:e6e6bc0ddd74e70913477961a93a559b4ca916013c74d13e9599dc2e60707364` (the comments are part of the metadata;
  rows and splits unchanged).
- `credit_card_customers`: the naive Bayes AUC table and its decision are removed; the column names show the two
  columns are fit with the label. Checksum `v2:ecd65d2464a44474cc2b05af6b1cff319c77271823d3fed878ca7e4ec4ab774a`.
- `phiusil_phishing`: the table of features alone uses `roc_auc_score` instead of a hand-written rank AUC; the
  README is unchanged.
- None of the three is built. `dataset check`: 0 errors, 0 warnings for each.

## 2026-10-07 (59 new definitions from the curation backlog; not built)

- Added 59 v2 definitions; none is built yet, so the table lists them as "not built":
  - 56 come from the 65 records that match the dashboard filter `suggestion = Yes`, no `DF: Yes`, not
    `AI (UNVERIFIED)`;
  - 3 come from `datasets/_maintenance/_out_of_scope/_too_late_to_add` (`african_credit_scoring_challenge`,
    `infrared_thermography_temperature`, `phiusil_phishing`).
- Each definition was checked and probed:
  - `dataset check` gives 0 errors, and pandas 2.3 and 3 give the same checksum;
  - leak, task, generated-data and hidden-group probes ran, plus group probes for grouped tasks;
  - an independent agent verified it against the `/verify-dataset` rubric, and the findings were applied or rejected
    with evidence.
- Eight `_1m` versions: `aeolus_1m`, `ashrae_great_energy_predictor_iii_1m`, `expresso_churn_prediction_1m`,
  `fraud_detection_in_electricity_and_gas_consumption_1m`, `g_research_crypto_forecasting_1m`, `huntprohibited_1m`,
  `numerai_v5_2_1m`, `pkdd_15_taxi_trip_time_prediction_ii_1m`.
- Eight are recommended not to ship, which is Lennart's call; their folders stay until he decides:
  `central_international_medical_college_and_hospital_health_risk_prediction`, `credit_card_customers`,
  `g_research_crypto_forecasting_1m`, `stroke_prediction`, `alvin_smart_money_management_classification_challenge`,
  `digicow_farmer_training_adoption_challenge`, `lgg_low_grade_glioma`, `phiusil_phishing`.
- Nine of the 65 records got no folder:
  - duplicates: `churn_telco_nigeria`, `myocardial_infarction_complications`, `numerai28_6`,
    `sasol_customer_retention_recruitment_competition`;
  - data gone: `alfa_battle_2_0_task_1`;
  - generated or injected data: `hepatitis_c_egypt`, `high_storage_system_data_for_energy_optimization`;
  - classes recorded differently, plus personal data in the files: `churn_telco_europa`;
  - a recommender task: `farm_to_feed_shopping_basket_recommendation_challenge`.
- Every issue and open decision, per dataset and across datasets, was in `NEW_DATASETS_ISSUES.md` (removed 2026-10-19; the open ones are now in the folders' `REVIEW.md` files).
  It includes two bugs in datasets already here: `mic` reads its file without `header=None` and so loses patient 1,
  and multi-line `splits_comment`s keep their code indentation.
- The records of all 68 carry a dated AI assessment comment. The records with a folder have their `v2_path` and
  `WIP (DF)`; `DF: Suspended` (ASHRAE and the six TCGA records) and `DF: Much work` (apistox) were replaced. The
  ASHRAE suspension had a reason in its v1 notebook (open judgment calls, too much time for then), which the new
  definition settles; the TCGA ones had none recorded.
  `problem_type` and `required_split` were filled only where they read `TBD` or `?`.

## 2026-10-06 (healthcare_insurance_expenses, churn and physiochemical_protein retired; generated-data probe)

- Removed `healthcare_insurance_expenses`: simulated data (`No (Retired)`, marker `AHDS`). It is the textbook data
  of Lantz's Machine Learning with R, "simulated on the basis of demographic statistics from the US Census Bureau";
  1,220 of its 1,338 charges equal a formula of the features to the cent (the record has it), the other 118 add a
  random extra cost, and the best BeyondArena methods already reach the best possible score.
- Removed `churn`: artificial data (`No (Retired)`, marker `AHDS`). MLC++ describes it as "artificial based on
  claims similar to real world"; its area codes ignore the state, its call counts share one distribution, and its
  label follows crisp rules (international-plan rules hold for 79 of 79 and 89 of 89 customers).
- Removed `physiochemical_protein`: groups that cannot be recovered (`No (Retired)`, markers `Data Quality Issue`,
  `Missing source information`). The rows are decoys of CASP target proteins, the use case needs new targets at test
  time, and no copy of the file says which target a decoy belongs to; the authors' later release (RF-PCP, Rana et al.
  2015) has target ids but other features.
- All three are TabArena v0.1 and BeyondArena datasets; the shipped collections keep them, and their containers and
  raw files stay in the warehouse. 125 datasets remain, 40 of them from TabArena v0.1 (`LEAK_AUDIT.md`, the table in
  `README.md` and the other counts are updated).
- New probe `generated_probes.py` (verify-dataset skill): a regression target that a median regression on simple
  terms fits exactly for many rows (`formula`), or a classification label that crisp rules give for a large share of
  the minority class (`rule_leaves`). On all 128 datasets of the morning's build it flags exactly the two generated
  ones. How to read it: `.claude/skills/verify-dataset/references/task_probes.md` (generated data).

## 2026-10-06 (airfoil_self_noise grouped by wind-tunnel run)

- `airfoil_self_noise` is a grouped task now (new UUID `01a11312-37c8-7cae-b6c8-c0b883fea348`; same 1,503 rows and 5
  features, new splits, scored per row). The rows are 106 wind-tunnel runs (one chord length, angle of attack and
  free-stream velocity each), each a measured spectrum of 8 to 19 frequency bands stored as one block in the raw
  file. A model is used for a configuration that was not measured; a random split gave a test row 62% of its run's
  other bands in train. R² random / grouped by run: extra trees 0.946 / 0.850, LightGBM 0.937 / 0.840, random forest
  0.926 / 0.830, kNN-5 0.755 / 0.629, ridge 0.510 / 0.490. The group column `run` is built from the three settings,
  which stay features. Task probes: no flags. The single-column hidden-group probe cannot see such a group; the
  probe reference says so now.

## 2026-10-06 (superconductivity grouped by composition)

- `superconductivity` is a grouped task now (new UUID `01a11308-e9d1-7f71-b3e3-e172887ea0d9`; same 21,263 rows and
  81 features, new splits, scored per row). The features come from the composition alone, and a model like this is
  used for compositions without a measured temperature, so a test composition must be new to it; a random split
  gave 35% of the test rows an identical row in train. The group column `composition` comes from the element counts
  in `unique_m.csv` (shipped with the release, row-aligned with `train.csv`): element shares at 6 decimals, which
  only removes floating-point noise (15,164 compositions; it joins formulas written in another order or scale). The
  cost on Tc is at most 0.009 R² (LightGBM 0.916 random, 0.913 grouped), and the ranking of five model families
  stays; the use case decided, not the gap. Not grouped by element set (new families are another task), not
  deduplicated (Stanev et al. 2018 average a material's entries; we keep the release's rows). Task probes: no
  flags. The day's interim builds: grouped with 4-decimal shares (`01a112de-6c52-714d-9186-5e0f9cdd3bdd`, merged 28
  different compositions) and IID again (`01a112f7-2990-72da-aeab-29cd3d672709`), both superseded. Evidence in the
  record and the README's "Decisions"; the rule (the split follows the real use, the gap is reported) is in
  `.claude/skills/verify-dataset/references/task_probes.md`.

## 2026-10-06 (library follow-ups done; checksum version 2; all 128 rebuilt; hidden-group probe)

- The library follow-ups of the framework review of 2026-10-01 are done (they were in `TODO.md`):
  - **Checksum version 2** (`v2:<hex>`) for every new container: it also covers each categorical column's
    categories, their order and `ordered`, and the test set through its own `test_dataset_checksum`; it leaves out the
    index and the `string` storage (`python` or `pyarrow`, which pandas versions choose differently). Checksums
    without the prefix (every shipped BeyondArena container) keep verifying with version 1. `container.verify()`
    checks either.
  - `categories.json` next to `dtypes.json` restores the categories, their order and `ordered` on load: integer
    categories with missing values no longer come back as floats, and a custom order is kept.
  - A new container needs the index `0..n-1` and string column names; the test set is saved without its index.
    `save` writes into a temporary folder and renames it; `load` skips `a.b.json` files that are not container
    metadata and ignores unknown fields of `container_metadata.json`.
  - `verify_saved_container` compares the categories (order and `ordered` included) column by column and compares
    values whatever the string storage.
  - Collections: BeyondArena is read from a pinned commit of `TabArena/BeyondArena` (`2ecfe882`, 2026-06-30; the
    newer commit changed only the README), a cached container counts only with its core files, `get_dataset(...,
    verify=True)` checks the checksum, and the 10 `_1m` entries are found by their own names
    (`get_dataset("cooking_time_1m")`).
  - `time_horizon_unit` takes only the five documented units and `time_horizon` must be a positive number; split ids
    must run 0..n-1 (all 1,100 saved containers on this machine pass).
  - `_prepare_raw_files` runs again when its code changed: the hash of the method and the helpers it calls sits in
    `.prepared_raw_files.json`. An unlabeled test set gets the training frame's categories first. A group may span
    several columns (`Grouping(on=["a", "b"])`). Plain `cutoffs` apply to a time-zone-aware time column; a numeric
    column listed as a date needs a format (pandas read it as nanoseconds since 1970); `anonymize_ids` gives `1` and
    `"1"` different codes (text keeps its codes). The README's `n_features` no longer counts the group column (15
    grouped datasets).
- `in_vehicle_coupon_recommendation` builds its respondent key with `astype("string").fillna("nan")`, the same keys
  without pandas 2's FutureWarning.
- Rebuilt all 128 datasets (new UUIDs in the table). The data is unchanged: every container's version-1 checksum
  equals the checksum the committed README stated, and rows and splits match the previous build. All 128 built `ok`,
  reload and verify, carry a `v2:` checksum, and show no new warning (61 open in 44 datasets). The two
  `_prepare_raw_files` steps ran once more (no hash recorded yet); acquire_valued_shoppers_challenge peaked at
  188 GB while doing so. A check-only build under pandas 3.0.6 from a warehouse holding only the 466 traced files
  (71.5 GB) gives the same 128 checksums. In that check the two prepare steps ran again under pandas 3 (their new
  `.prepared_raw_files.json` was not among the traced files) and wrote through the symlinks of the check's warehouse
  into the real prepared files; a pandas 2 check-only build that reads them reproduces both checksums, so they are
  intact. `minimal_inputs.py links` now copies the prepared files with their marker instead of linking them.
- The hidden-group probe (`hidden_groups.py`, verify-dataset skill) ran over the 93 IID datasets, with the 15 grouped
  ones as controls (it finds the known group in 11; the 4 it misses gain little from a random split). Four IID hits:
  amazon_employee_access (`MGR_ID`), covertype (`Soil_Type`) and mutual_funds_india (`sub_category`) need no action
  (a value every new row has); superconductivity is grouped by composition (entry above).
- Dropped the planned selection version of asp_potassco_classification (Lennart): it is gone from `TODO.md`, the
  record, `BENCHMARK_CHANGES_TODO.md` and the probe reference. Also dropped from `TODO.md`: the
  sat11_hand_algo_runtime family split (not wanted: a selector in use has other instances of a family in its data;
  the reasoning is in its record).

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
  heart_disease_cleveland.
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
