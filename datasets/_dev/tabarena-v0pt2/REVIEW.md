# Across datasets

### Rules (`.claude/skills/knowledge-curation/`)

- **Add two optional rule rows for consistency (from `huesken_sirna_efficacy`, no effect on that dataset)?** The few-groups acceptance (`heart_disease` with 3 hospitals, `huesken_sirna_efficacy` with 30 genes, your wording that a group is a large set of observations over which we generalise) has no Cases row, and `huesken_sirna_efficacy` is the second grouped-ranking exception to MET-5 after `protein_model_quality_rf_pcp`; a third one makes an amendment of MET-5 due (principles, "Exceptions and amendments"). The panel's evidence is weaker there than in RF-PCP: between-gene differences are 17.1% of the variance and the literature reports pooled metrics, so the use case (MET-1) alone carries it.
  Implemented: nothing in the rule files.
  Alternative: a Cases row under "Few groups" in `splits.md` and a Cases row in `metrics.md` noting the second exception (two separate rows, decided separately).
  Decision needed: add the rows or leave the rule files as they are.
  **Lennart (2026-11-04, ok):** add row
  **Resolved (2026-11-04, Lennart):** go ahead. The few-groups Cases row for huesken_sirna_efficacy is in `splits.md` (heart_disease's row was already there); the MET-5 row naming huesken as the second exception was already in `metrics.md` (5085fc1a), so it is not added twice. No MET-5 amendment is due before a third exception.
- **Correct the stale spectrum figures in `spectra.md` (from `open_soil_spectral_library`)?** Line 113 still says "1,701 positions"; 1,700 ship since the 600 cm-1 bin was dropped. Lines 114-123 still show the encoding table on the percent scale, and two of its conclusions reverse on the declared `rmsle` scale ("PLS gains a little from the baseline", "ridge reads the spectrum best as it is"). The mediator listed both as changes to make now (its changes 2 and 5); the apply step could not touch skill files.
  Implemented: the definition and the Review have the declared-scale figures; `spectra.md` does not.
  Proposal: replace "1,701" with 1,700 and the table with the panel's declared-scale results.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-04, Lennart):** go ahead. `spectra.md` gives 1,700 positions and the table on the declared scale (RMSE on log1p); the PLS and ridge conclusions are rewritten, the default encoding is unchanged.
- **Correct this panel's precedent row of `lt_vehicle_loan_default_prediction` in the SPLIT-10 Cases table?** The row (`splits.md` line 244) says a gap "would leave 20-53% of the rows for training". The precedent checker refuted that: with a 30-day gap and three two-day windows from 26 October every window keeps at least 50.39% (SPLIT-14 met); the real cost is SPLIT-15 (a Should), nine windows down to three. The record's 2026-11-04 Assessment repeats the figure (see the text-correction item for lt below).
  Proposal: replace the clause with "a 30-day gap meets the 50% floor but leaves three windows instead of nine (SPLIT-15)".
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-04, Lennart):** go ahead. lt's SPLIT-10 row says a 30-day gap meets the 50% floor but leaves three windows instead of nine; application or exception stays open as lt's issues 4 and 5.
- **List `bemtpl97` and `fremtpl2` in the SPLIT-8 Cases table?** Both ship IID under `ForcedIIDFromTemporal` (your CC of 2026-11-04: the two are treated alike), and `splits.md` names neither. Bookkeeping, not a departure (bemtpl97's precedent checker).
  Proposal: two rows, each with the fact that forces IID (no policy dates in the release).
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-04, Lennart):** go ahead. Two SPLIT-8 rows in `splits.md`; fremtpl2's names what sets it apart from nba and open_university (periods and links inferred, not the source's key) and the measured cost (+0.00049 deviance, ranking unchanged).
- **Adopt the exposure rules of the study of 2026-11-05 ([#51](https://github.com/TabArena/data-foundry/issues/51))?** LEAK-41 (a realized weight, and any column that encodes it, is never a model input; no training or scoring on rows selected by it), the amended LEAK-10 Cases row on time on risk and a new one on spans the outcome sets, MET-14 (ship the rate per unit at risk), MET-15 (its realized denominator is the metric's row weight and the training weight), MET-16 (survey weights), and the CLEAN-16 (no transform under a deviance) and MET-13 (a stated floor, no cap) amendments.
  Implemented: the texts in `leak_checks.md`, `metrics.md`, `cleaning_features.md`, `verification.md`, `evidence.md` and the agent briefs.
  **Resolved (2026-11-06, Lennart):** adopted as drafted (D1-D4), without the structured exposure note: the exposure is described in text. Probe 22 measures per dataset whether a feature predicts the weight.
### Framework (`src/data_foundry/v2/`)

- **Floor a coarse time column before the framework orders the rows, in every definition (from `chicago_traffic_crashes`)?** `order_rows` (`src/data_foundry/v2/preprocessing.py`) stable-sorts by the full-precision time column after `_clean`. A definition that coarsens the time only in `_make_splits` therefore ships each period's rows in the order of the finer time it meant to hide, which is chicago's issue 9 (LEAK-13, the minute back through the row order). Flooring in `_clean` leaves each period in the framework's content order (a hash of each row's values).
  Implemented: nothing; chicago's own fix is its issue 9.
  Proposal: a check in `dataset check` that warns when `_make_splits` coarsens the declared time column, and a line in the `dataset.py` guide to floor in `_clean`.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-04, Lennart):** go ahead. `dataset check` warns `definition_time_changed_in_split` when `_make_splits` changes the time column (chicago_traffic_crashes: 813,133 rows, its issue 9); `definitions.md` says to coarsen in `_clean`.
- **Score each test row only on the rows known before it, collection-wide (from `medical_facility_operational_data`)?** The collection's evaluator fits on the training rows and predicts the whole test block in one call (`examples/benchmark_on_beyond_arena.py`), so a model could use the test block's own rows at prediction time. medical's issue 7 ships with a protocol line, as sepsis_prediction_1m and 5g_energy_consumption do.
  Implemented: the protocol line as text in each definition.
  Alternative: a per-row (snapshot) scorer that shows each test row only the rows that arrived before it; it changes the harness for every temporal dataset.
  Decision needed: keep the protocol line, or plan the per-row scorer.
  **Lennart (2026-11-04, leave):** benchmark_on_beyond_arena is not that relevant, we can check if the model cheats, however, change the example, create one that is called as is now but only for beyond arena dataset as an example, and create a new one that is generally called benchmark_container and is only for v2 and it specifications/dataset types
  **Resolved (2026-11-04, Lennart):** no per-row scorer; the protocol line stays. `examples/benchmark_on_beyond_arena.py` is BeyondArena only, and the new `examples/benchmark_container.py` takes a v2 container with its metric spec, scoring columns and feature types (special features, ordinal, datetime, text), with tests. A LEAK-9 Cases row records the call, and `BENCHMARK_CHANGES_TODO.md` has the benchmark-side check.
- **Store integer-coded categories as strings (from `bemtpl97`)?** A categorical with integer categories (`postcode` in bemtpl97, `zipcode` in house_sales) comes back as an integer from a plain parquet read; the container restores the categories from `categories.json`, so only a reader without Data Foundry (or the panel's kit) sees numbers. The panel called it optional (P7, CLEAN-14); the apply step dropped bemtpl97's issue 4 for this item.
  Implemented: integer categories, restored by the container.
  Alternative: write such categories as strings in the container, for every dataset at the next rebuild.
  Decision needed: go ahead or leave as is.
  **Lennart (2026-11-04, leave):** we only care about it being correctly read from our setup and changing this would make the data state less correct, so integer code should stay
  **Resolved (2026-11-04, Lennart):** no change; integer-coded categories stay integers, restored as categories by the container.
- **Add a training weight to container format 2 and weights to the deviances?** The metric reads a weight scoring column through its `weight` input; the task names its training weight in an optional field `sample_weight` (opt-in, always the metric's row weight); `score()` refuses an input the metric does not take; `mean_poisson_deviance` needs a stated `min_prediction`; `ordered_lorenz_gini` gets `per_unit`.
  Implemented: `schema.py`, `v2/metrics.py`, `v2/dataset.py`, `curation_container.py`, the bundle checks, the README, the probes and the examples; containers without the field keep their checksum.
  **Resolved (2026-11-06, Lennart):** go ahead (D5-D7); no backward compatibility with older readers; floor 1e-4 claims per year and no per-row cap; the TabArena side is a TODO in `BENCHMARK_CHANGES_TODO.md` only.
### Text corrections in definitions and records (the panel's, text only; go ahead = Claude applies them)

- **`airqo_low_cost_air_quality_monitor_calibration_challenge`.** The record's Assessment line on the 15 outage hours says sensor 2 at 0.02-2.9 with a ratio of at least 0.63 elsewhere; the panel measured 0.0014 to 1.37, and elsewhere a 0.1% quantile of 0.618 and a minimum of 0.107. The record's 2026-11-04 "review panel (none) ... all are settled" line gets a correction line. `splits_comment` still gives the pre-temporal "LightGBM RMSE 14.05 against 18.39"; the panel measured 12.94 against 18.26 (split auditor).
  **Resolved (2026-11-04, Lennart):** go ahead; applied in the definition and the record, READMEs regenerated (CHANGELOG).
- **`bemtpl97` and `fremtpl2`.** Correction lines in bemtpl97's record for "Exposure is an offset", "no panel ran", "20 other forced-IID definitions" (17) and "machine epsilon" (the params are 1e-6), and for the 2026-10-26 "unverified" line. fremtpl2's `curation_comments` say "machine epsilon" too (its params are 1e-6), and cite two figures nobody could verify (Wüthrich and Merz Eq. 5.28; the LightGBM figure of 292.6 expected claims): cut both (EV-7).
  **Resolved (2026-11-04, Lennart):** go ahead; applied in the definition and the record, READMEs regenerated (CHANGELOG).
- **`lt_vehicle_loan_default_prediction`.** Correction lines in the record for the 2026-11-04 Assessment ("about 90%" of the gain is training size; "20-53% (SPLIT-14)"), its pointer to "Review issue 1" (now issues 4 and 5) and "review panel (none) ... all are settled"; mark the 2026-10-23 "Exception to SPLIT-10" line as history; set the `Selection Bias` marker (USE-8).
  **Resolved (2026-11-04, Lennart):** go ahead; applied in the definition and the record, READMEs regenerated (CHANGELOG).
- **`open_soil_spectral_library`.** `curation_comments` say the 151 layers above 58% organic carbon "equal the source's measured total carbon"; the mediator checked only the three above 70%, so the sentence names those three. Add the record's AI note that the 2026-10-29 decisions on issues 2-3 never became a file in the folder.
  **Resolved (2026-11-04, Lennart):** go ahead; applied in the definition and the record, READMEs regenerated (CHANGELOG).
- **`sendy_logistics_challenge`.** `splits_comment` says the release has "no month or year"; `task_summary.split` and the mediator's agreed change say "no month order or year" (the day of the month is there).
  **Resolved (2026-11-04, Lennart):** go ahead; applied in the definition and the record, READMEs regenerated (CHANGELOG).
- **`tunisian_fraud_detection_challenge`.** `curation_comments` say "the 24 registry columns identify every taxpayer one to one"; the 23 that ship single out 59.6% of the 12,244 taxpayers (the 24th is the dropped id). They also say pairs with a year between them "agree as much as consecutive ones"; the mediator's test compared two years the same distance apart with the year between missing or present (0.794 against 0.803).
  **Resolved (2026-11-04, Lennart):** go ahead; applied in the definition and the record, READMEs regenerated (CHANGELOG).
### From GitHub issue #48 (column-type review of #37)

- **Warn users of the BeyondArena collection that its frames predate the leak audit?** `BEYOND_ARENA` pins the April 2026 containers, and the decision of the leak audit was to leave those pins unchanged. Issue #48 found two leaks still in them: santander_customer_transaction_prediction's 400 `var_<k>_has_one` / `has_zero` columns (built from the labels of all rows) and anes_voting_2026's 57 post-election items (among them `VCF1005`, built from the House vote). Both are fixed in the working copy since 2026-09-30, but the collection, its docstring, `README.md`, `DATA_FOUNDRY_V1.md` and `examples/benchmark_on_beyond_arena.py` say nothing of it, and the audit's summary for users (`LEAK_AUDIT.md`, named in the CHANGELOG of 2026-10-01) never reached git. The CHANGELOG's leak-audit entries name 35 of the 142 pinned datasets (retired ones such as video_game_fps_prediction and prostate_cancer_detection, changed ones such as kickstarter, mic, hepatitis_c_prediction).
  Implemented: nothing; the pins and their documentation are unchanged.
  Proposal: a "Known issues" list in `DATA_FOUNDRY_V1.md`, linked from the collection's docstring and the BeyondArena example: each pinned dataset the audit retired or changed, with one line on what and a pointer to its working-copy folder; the pins stay until the TabArena v0.2 collection replaces them.
  Decision needed: go ahead or leave as is.
  **Lennart (2026-11-05, ok):** Only add to readme in small and more in data foudnry v1 md that leaks etc might be in old tasks but new tasks are the latest state etc
  **Resolved (2026-11-05, Lennart):** go ahead. `README.md` has one sentence by the collection; `DATA_FOUNDRY_V1.md` has "Known issues of the shipped containers": the pins stay, the v2 folders are the latest state, the two leaks of issue #48, the 23 pinned datasets retired since, and where to look up what changed.
- **Add two checks that would have caught issue #48's misses?** eryhemato_squamous_disease's scores were made numbers in `_clean` and cast back to categories by a blanket `_feature_types`; no check compares the two. early_learning_predictors' `ward_best` passed the dtype probe because its name holds none of the probe's code words (`id`, `code`, `zip`, `postcode`, `postal`) and its values look like a count.
  Implemented: nothing.
  Proposal: a test that every column of a definition's module-level `SCORES` list ships numeric (read from the README's type lists, no data needed; it fails on eryhemato only, 2026-11-05), and the probe's code words extended by administrative areas (`ward`, `district`, `county`, `municipality`, `province`, `region`), so a numeric column so named is flagged for a look.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-05, Lennart):** go ahead. `tests/test_v2_datasets.py::test_scores_ship_as_numbers` (fails on the old eryhemato definition), and the dtype probe's `code_name` flag covers `ward`, `district`, `county`, `municipality`, `province` and `region` (tested).
### From PR #47 (exposure rework, 2026-11-06)

- **Ship the seven insurance tables with a forced split, as listed?** Seven tables of the zero-inflated batch have no valid temporal windows and ship forced from temporal (SPLIT-8): frempl_french_motor_personal_line, rand_health_insurance_experiment_doctor_visits, spanish_motor_insurance_coverage_level_2022_2024, pricing_game_2017_french_mtpl and allstate_claim_prediction_challenge_1m grouped, australian_vehicle_insurance_2004_2005 and liberty_mutual_fire_peril_loss_cost IID. The leak tests of 2026-11-02 (shared rows and units across the split, the training side's outcome of the test rows' period, features built from other rows' outcomes, hidden groups, order dependence) found none. Wisconsin moved to temporal windows instead (its issue 3).
  Implemented: all seven ship forced and tagged, under SPLIT-8 as reworded in #44 (a leak found is weighed case by case).
  Proposal: ship them as listed.
  Decision needed: go ahead, or name the tables to discuss.
  **Resolved (2026-11-08, Lennart):** go ahead: six of the seven ship forced as listed; rand_health_insurance_experiment_doctor_visits is `2nd Tier` since Andrej's call of 2026-11-03 and has no folder, so it ships nothing. pricing_game_2016_french_fleet joined them on 2026-11-08 (grouped by contract, its issue 6), after its leak test across the folds passed.
- **Re-read `how_much_did_it_rain`'s `No` under the reworded SPLIT-8?** It was set to `No` on 2026-10-30 for a measured leak across its split (the hours of one storm on both sides). Under the reworded rule a leak across a forced split is weighed case by case, not a reason to refuse by itself.
  Implemented: nothing; the record stays `No`.
  Proposal: re-open the record for a check of whether a split grouped on storms removes the leak, or how large it is when kept, as its own task.
  Decision needed: re-open or leave as is.
  **Lennart (2026-11-08, ok):** re-open in the curation record but leave out of htis batch for now, next screening can take a look at it
  **Resolved (2026-11-08, Lennart):** re-opened: the record's suggestion is `TBD -> 2nd Tier` again, out of this batch, and a CC line names the check for the next screening (does a split grouped on storms remove the leak, or how large is it when kept).
- **Make the leak tests of a forced split probes?** The five tests above ran by hand for each table. Hidden groups is already a probe; the others are not.
  Implemented: nothing.
  Proposal: one probe for a forced split that runs the period-outcome test (drop the training rows of the test rows' period and compare) and the shared-unit test, so every forced split gets them without a panel.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-08, Lennart):** go ahead: probe 23 (`leak_probes.py`, at the end of the default run on a split tagged forced from temporal, alone with `--forced-split`) runs the period-outcome test (each test period without its own training rows against as many random rows, pooled and within a period) and the shared-unit test (group, exact profile, profile without the period, with a lookup of the unit's training target), with regularised fits on the declared metric. It reproduces the hand tests: spanish coverage +0.0053 Gini pooled (by hand +0.0045), pricing_game_2016 +0.07 (by hand -0.18).
- **Retire the record `ausprivauto0405` as a duplicate of `australian_vehicle_insurance_2004_2005`?** CASdatasets' `ausprivauto0405` holds the same rows (exposure, vehicle value, claim count and cost equal on every row) without the area, the definition's `download_description` says so; the record is still `TBD -> Yes` with priority 4.
  Implemented: nothing.
  Proposal: set it to `No` as a duplicate, pointing to the australian folder.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-08, Lennart):** go ahead: `ausprivauto0405` is `No` with the marker `Duplicate`, pointing to the australian folder; its claim is released.
- **Keep the test rows' weight away from the model (X1, from the `bemtpl97` and `fremtpl2` panels)?** A weight scoring column ships for the test rows too, because the scorer needs it, so a participant can read the realized weight of a row it predicts. Used as a feature it gains +0.0052 deviance on bemtpl97 (about a quarter of the honest gain over the constant), +0.0072 to +0.0088 on fremtpl2, and +0.09 to +0.12 weighted Gini on australian_vehicle_insurance_2004_2005; a model at the quote has no such value (LEAK-41). It concerns all six tables with a `sample_weight`.
  Implemented: the definitions meet LEAK-41 (`feature_columns` drops the weight; the README calls it "never a feature"); nothing says that the test rows' values belong to the scorer.
  Proposal: the generated README and `describe()` say for every weight scoring column that its test-row values are for the scorer only; the benchmark adapter passes scoring columns to the scorer and to training as the sample weight, never to `predict` (a line under "Training weights" in `BENCHMARK_CHANGES_TODO.md`).
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-08, Lennart):** go ahead: the generated README (under the scoring-column table) and `describe()` (on each weight column's line) say that a weight column's test-row values are for the scorer only, never read when predicting a test row; `BENCHMARK_CHANGES_TODO.md` says the adapter passes scoring columns to the scorer and the `sample_weight` to the fit, never to `predict`. Nine READMEs regenerated; liberty_mutual_fire_peril_loss_cost's waits for its raw data.
- **Reword LEAK-41's "score of 1/weight alone as the ceiling a leak would reach" (X2, from the `bemtpl97`, `fremtpl2` and `frempl_french_motor_personal_line` panels)?** Under a level-sensitive metric 1/weight used as the prediction is no ceiling: on fremtpl2 it scores 3.65 against the constant's 0.479 (k/weight fitted on train 0.490), while a model of the target on the weight alone scores 0.47114 against 0.47929 (bemtpl97: 0.6122 against 0.6193). Under a Gini it is no ceiling either: on frempl 1/length alone scores 0.184, but the realized length added to the features reaches 0.256. Probe 22 scores 1/weight only for a Gini.
  Implemented: both definitions report the fitted weight-alone score next to the leak's gain under the L2 and the actuarial fit.
  Proposal: amend LEAK-41's clause to report "the score of 1/weight alone for a ranking metric (a Gini), or of a model of the target on the weight alone for a level-sensitive metric (a deviance), next to the gain of the weight added to the features", without the word "ceiling"; probe 22 reports the fitted one for a deviance.
  Decision needed: go ahead or leave the text as it is.
  **Resolved (2026-11-08, Lennart):** go ahead: LEAK-41 reports the weight-alone score (1/weight for a Gini, a model of the target on the weight for a deviance) next to the gain of the weight added to the features, without the word "ceiling"; probe 22 fits the weight-alone model for a deviance and prints no "ceiling".
- **Ask MET-14's rebuild check only when the source releases the count (X3, from the `wadden_sea_sibes_macoma_abundance` and `noaa_afsc_bottom_trawl_survey_cpue` panels)?** MET-14 asks `_clean` to assert that the target times its denominator rebuilds the count. Two definitions ship a density the source already divided by its area and release no count to rebuild: boreal_postfire_lichen_biomass (kg/ha, the quadrat area folded in) and wadden_sea_sibes_macoma_abundance (density per m2; no count or subsample fraction released). noaa_afsc_bottom_trawl_survey_cpue does release the count, so it gets the assertion (the counted catches rebuild to 1.6e-4).
  Implemented: boreal's and wadden's notes say the source ships only the rate; noaa_afsc asserts the rebuild in `_clean`.
  Proposal: MET-14's check applies "when the source releases the count; when it ships only the rate, the notes say so".
  Decision needed: go ahead or leave the text as it is.
  **Resolved (2026-11-08, Lennart):** go ahead: MET-14's rebuild check applies when the source releases the count; when the source ships only the rate, the notes say so (boreal_postfire_lichen_biomass and wadden_sea_sibes_macoma_abundance named, noaa_afsc_bottom_trawl_survey_cpue the case that rebuilds).
- **Write the keep of spans the outcome sets into LEAK-10 as a third clause (X4, from the `noaa_storm_events_damage` panel)?** The Cases row of 2026-11-06 keeps, with a note, a span drawn "by the outcome or an outcome-free criterion" (noaa_storm's kept types, and since 2026-11-08 its Flash Flood duration; bank_marketing's `campaign` was dropped on 2026-11-08, as after the prediction point). Under the deviance noaa_storm's measured Thunderstorm Wind spans gain in 35 of 45 fits, which bears on "only when that worth is small". LEAK-10 is a Must and its text has only two clauses, so this keep stands on a Cases row alone, and the row sets no size limit: read literally, it would have kept heart_failure's `time`, dropped on its size (alone ROC AUC 0.84; LightGBM 0.75 without it, 0.90 with it).
  Implemented: the Cases row in `leak_checks.md`.
  Proposal: a third clause in LEAK-10: for a span the outcome or an outcome-free criterion draws, blank the part that can be located; keep the rest with a note giving its worth only when that worth is small; heart_failure's `time` named as the counter-case.
  Decision needed: go ahead, go ahead with other wording, or keep it as a Cases row only.
  **Consistency check (AI, 2026-11-08):** Write the third clause with its size condition, when noaa_storm's Flash
  Flood duration, kept with a note on the same day, is worth far more than "small"?
  **Lennart (2026-11-08, chat):** The case for x4 is quite confusing to me, let us re-open it and discuss it once more
  here. In essence, we have here features we belive to be set after the outcome, correct? Why would we want to keep
  them? [after the diagnostic:] yes, write the clause and update the note

  **Resolved (2026-11-08, Lennart):** a third clause in LEAK-10, by the share the outcome can draw rather than the size
  of the worth: blank what features locate; keep the rest with a note only when the source lets the outcome draw a
  minority of the spans and the span keeps its worth on the rows the outcome did not draw (measured with the narratives
  as a diagnostic); a span the outcome ends every time goes (heart_failure's `time`). The diagnostic on noaa_storm: the
  Flash Flood duration cuts the deviance by 40% to 48% on the 82% of test rows whose narratives name no damage-like
  onset, so it stays, its note giving the worth by narrative class.

  * **Problem:**
    - The proposed clause keeps a span the outcome may draw "only when that worth is small", yet noaa_storm's issue 11
      (your mark of 2026-11-08) keeps the Flash Flood duration with a note at +31% to +102% of the deviance on its rows
      (+9% to +27% on all rows), and the measured Thunderstorm Wind spans gain in 35 of 45 fits.
    - What sets heart_failure's `time` apart is not its size: the outcome ends every one of its spans (death or
      censoring), while damage can set a Flash Flood's start in at most a small share of entries (6.8% of the
      narratives name water at or damage to a building).
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | a | The clause as proposed | keep the rest with a note only when its worth is small; noaa_storm's Flash Flood and measured Thunderstorm Wind spans reopen (blanked) | one simple test | reverses issue 11 of the same day; "small" needs a number |
    | b | The clause by the share the outcome can draw | blank the part that can be located; keep the rest with a note giving its worth when the outcome can set only a small share of the spans (Flash Flood: at most 6.8% of starts); drop the span when the outcome sets every span's end (heart_failure's `time`) | matches every decision so far; the test is about the leak, not the score | the share is often an estimate (here from the narratives) |
    | c | Keep it as a Cases row only | the rule's text stays as it is | no rule change | the keep stands on a row the rule's text does not name |

  * **Recommendation:** (b): it names what separates heart_failure from noaa_storm, and the worth of a kept span stays in
    its note, as now.
  * **Decision:** (a), (b) or (c)?

### From the review of 2026-11-08 (after PR #47's board)

- **Give each unit one vote in the score of superconductivity and pancreatic_cancer_mouse_detection, as
  boreal_postfire_lichen_biomass does since 2026-11-08?** A scan of the 190 definitions for rows that repeat one
  decision unit in unequal numbers (Lennart's question on boreal's issue 7) found two whose use case acts on the
  unit. superconductivity: a row is one SuperCon entry, and the 15,164 compositions hold 1 to 110 entries
  (YBa2Cu3O7 110, Bi2Sr2Ca1Cu2O8 83); the 16% of compositions with two or more entries hold 40% of the rows. Every
  input is computed from the formula (all 81 equal within 99.8% of the multi-entry compositions), so a model predicts
  one value per composition, and the materials scientist decides per composition which to synthesize. The notes say
  "Every entry is kept and scored per row" (SPLIT-26 keeps the source's rows; Hamidieh 2018 scores RMSE per row on a
  random split), while Stanev et al. (2018) average a material's entries, one vote per material; a weight keeps the
  rows and counts each composition once. pancreatic_cancer_mouse_detection: a row is one serum spectrum, from 1 to 6
  bleeds per mouse (median 2; 29 of the 73 mice have one); the label is the mouse's, and the use case reads "each
  sample of an unseen mouse stands for a new patient's test", so a mouse bled six times counts as six patients. On
  the shipped splits, with the 8 untuned predictors of boreal's check, the weighted score ranks models like the
  per-row one at Kendall tau 0.98 per split (lowest 0.93) and 0.93 for the mean over the splits on
  superconductivity, the same best model on 9 of 9 splits; on pancreatic at 0.66 per split (lowest -0.07, on 24 test
  mice per fold) and 0.86 for the mean, the same best model on 77% of the splits (boreal: 0.81 per split, 0.86 for the
  mean).
  Implemented: nothing; the table and the scripts are in
  `local-data-warehouse/_runs/2026-11-06_exposure_review/one_vote_scan/`.
  Proposal: superconductivity: the source's `rmse` weighted by a `composition_weight` scoring column, 1 over the
  composition's entries, the departure from Hamidieh's per-row score stated in the metric's reason; for the metric
  only and no `sample_weight`, as boreal's `plot_weight` (the inputs are constant within a composition, so the fit's
  target is the same; `task_metric_weight_without_sample_weight` accepted with that reason).
  pancreatic_cancer_mouse_detection: `roc_auc` weighted by a `mouse_weight` scoring column, 1 over the mouse's
  samples, each sample still read on its own; `roc_auc` takes no weight yet, so it gets an optional `weight` input
  (scikit-learn's `sample_weight`), as `rmse` did for boreal. Its inputs differ between bleeds, so the weight is no
  function of the features; it stays a design weight of the score with no `sample_weight`, the check's warning
  accepted with that reason. A Cases row in metrics.md for each, next to boreal's.
  Decision needed: go ahead for both, for one, or keep per row (pancreatic stays per row if the use case is a person
  tested again and again, every test a decision).
  **Lennart (2026-11-08, discuss):** same as for (2)
  **Resolved (2026-11-08, Lennart):** opened as per-dataset issues: superconductivity issue 1 (recommended: each
  composition counts once) and pancreatic_cancer_mouse_detection issue 1 (recommended: each mouse counts once; per
  sample if the use case is a person tested again and again).

- **Which unit does the score count once in dementia_prediction, asp_potassco_classification and
  video_transcoding_time_prediction?** The same scan. In these three the rows of a unit are not replicates (their
  inputs differ), and the use case does not settle whether the actor acts per row or per unit. dementia_prediction:
  150 people with 1 to 5 visits (91 with two, 13 with four or five), each visit with its own rating (31 people change
  it); the use case is a first visit at a memory clinic, and "follow-up visits of test people are scored as if each
  were a first visit", so a person seen five times counts five times. One vote per person ranks models at tau 0.94
  per split (lowest 0.71) and 1.0 for the mean over the splits. asp_potassco_classification: 96 problem classes with
  1 to 134 instances (median 5), the largest 10% of the classes holding 51% of the instances; the selector acts per
  instance (ASlib scores per instance), but the split holds out whole classes, "as for a user with a new encoding".
  One vote per class: tau 0.86 per split (lowest 0.64), 0.86 for the mean, the same best model on 57% of the splits.
  video_transcoding_time_prediction: 1,099 videos; the 80 with the full grid of 841 output settings hold 97.8% of the
  rows, and 1,018 videos (93%) have one job. The scheduler acts per job, but the grid is the experimenters' design,
  not a cluster's mix of jobs; one vote per video would give the one-job videos 93% of the weight. tau 0.90 per split
  (lowest 0.79) and 0.93 for the mean; the best model (random forest or LightGBM, close) is the same on 3 of 9
  splits.
  Implemented: nothing.
  Proposal: dementia_prediction one vote per person (1 over the person's visits; `log_loss` gets an optional `weight`
  input), since the clinic acts once per person, at a first visit; asp_potassco_classification and
  video_transcoding_time_prediction stay per row, since each instance and each job is a decision, with a note that
  names the imbalance (video's per-row score is in effect the grid of 80 videos).
  Decision needed: per row or one vote per unit, for each of the three (for dementia also: score only each test
  person's first visit).
  **Lennart (2026-11-08, discuss):** open this as per dataset issues not here, remeber this in the future here ar etoo
  many per dataset choice in the across dataset tab!
  **Resolved (2026-11-08, Lennart):** opened as per-dataset issues: dementia_prediction issue 1 (recommended: each
  person counts once, or C, first visits only), asp_potassco_classification issue 5 (recommended: per instance with a
  note) and video_transcoding_time_prediction issue 1 (recommended: per job with a note). Per-dataset choices go into
  each dataset's Review from now on (review_file_format.md, working_copy.md).

- **Correct african_credit_scoring_challenge's `row` text and notes on co-funded loans?** The `row` text and the notes (line 153) say a loan co-funded with a second lender gives two rows; in the shipped frame that never happens (52,826 rows and 52,826 loan ids), since the kept product has one lender (found by the scan above).
  Implemented: nothing.
  Proposal: say one row per loan and drop the co-funding sentence; text only, the README regenerated.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-08, Lennart):** go ahead, applied: the `row` text, the notes, the splits comment and decision
  table 4 now say one row per loan; README regenerated, checksum changed (not built).

### From the information audit of 2026-11-09 (what the actor knows when it fits, predicts and scores)

- **Give format 2 a training-only column role?**
  * **Problem:**
    - In 15 of the 16 definitions of the zero-inflated batch, columns the actor holds for past rows and would fit on are dropped from the dataset altogether, because the format can pass only one such column to the fit, the training weight.
    - The rules require the drop today: a count behind a rate leaves the frame, a column recorded after the prediction point leaves the inputs, and a training weight must also be the metric's weight[^xa1].
    - pricing_game_2016 shows the cost: a Poisson model of the claim counts times the mean charge beats the Tweedie model of the charge on the shipped folds, but no participant can fit it, since the count never reaches the fit.
  * **Background:**
    - The audit asked, per dataset, what the actor has at three moments: when it fits (past rows, with every column recorded for them, also after their own prediction point), when it predicts (the new unit's attributes and own history), and when it scores (what the business evaluates with).
    - The columns that only exist for past rows, by dataset: australian `numclaims`; frempl how each record ended (`RecordEnd` and the link to a successor), the claim-type counter rises, the sign of `ClaimAmount` (recourse claims); spanish coverage the claim counts and incurred costs per cover, `policy_status`; pricing_game_2016 the claim count, per-claim charges, IDA flag, responsibility and closure year; pricing_game_2017 the claim count and per-claim amounts; spanish homeowners `Retention`, `NClaims1`, `NClaims2`, `Claims1`, `Types`; spanish 2015-2018 `N_claims_year` and the realized exposure from `Date_lapse`; wisconsin `Freq` and the claim lines; loan_default f527, f528, f468, f471, f536 and the f221 family; noaa_storm the tornado rating and path, end point, casualties, crop damage, estimated wind speeds, the blanked durations and the narratives; noaa_afsc the area swept, catch weight, vessel and gear; boreal the cover-based estimate and the NT ground covers; wadden the measured sediment, platform, core area and the other taxa; walmart (not in PR #47) the observed weather.
    - Liberty releases none; allstate only the in-year vehicle count.
  * **Effect on the task:**
    - Models the business fits are out of reach: frequency times severity, an offset on the time on risk, auxiliary targets (crop damage, casualties, a lapse), and methods that learn from information only training rows have.
    - Scores do not change until a model uses the new columns, so the change is about fidelity to the application and about which methods the benchmark can test.
  * **Experiments:** pricing_game_2016, shipped folds: the weighted Poisson LightGBM of claims per vehicle-year times the training side's mean charge per claim scores 81.06 on the declared metric, 0.92 better (SE 0.34) than the Tweedie model of the charge (the definition's notes).
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | Keep as is (implemented) | columns known only after the prediction point stay dropped; one training weight at most | no format, adapter or rule change | the actor's training information is lost in 15 datasets; frequency-severity and offset models cannot be fit |
    | B | A training-only role | a task field lists training columns: in the frame, passed to the fit with the training rows, never to predict, never scored; the rules move such a column to this role instead of dropping it | the benchmark holds what the actor holds at fit time; one change serves 15 datasets; per-dataset issues then pick the columns | format, adapter and probe changes; the test rows' values sit in the container, as the weights' do now |
    | C | Training weights only | allow a training weight that differs from the metric's weight (the trawl's area swept) | a smaller change | counts, flags and claim lines stay lost |

  * **Recommendation:** B: it is the one change behind most of the audit's training-side gaps, and the per-dataset choice of columns stays with each dataset's issue in the next round.
  * **Decision:** A, B or C?

  **Notes for the AI:** B: an optional task field `train_columns` (`TrainColumn(column, role, description)`, roles such as `count`, `amount`, `flag`, `weight`, `auxiliary_target`), left out of the checksum while unset as `sample_weight` was; reader `train_columns(container)`; `feature_columns()` unchanged; bundle checks that a training column is no feature and no scoring column; README section; `BENCHMARK_CHANGES_TODO.md` entry (the adapter passes them to fit only; a contract test shuffles the test rows' values and expects the same predictions); probes leave them out of the inputs. Rules: MET-14 ("leaves the frame" becomes "leaves the features; it may ship as a training column"), LEAK-10 and LEAK-41 (never an input at the prediction point; may be a training column), MET-15 and MET-16 (a training weight may differ from the metric's weight). Then one issue per dataset on which columns move.

  **Andrej (2026-11-09, discuss):** Please add a curation note to each dataset where features that would actually be available at train time are not used because we wouldn't have them at test time. But otherwise we leave them out for now.

  **Resolved (2026-11-09, Andrej):** A for now, no training-only role. Each definition whose source holds columns known only for past rows names them in one notes bullet, "Note: held for training rows only, not shipped (cross-dataset item of 2026-11-09, Andrej): ...", with a CC line in its record: australian, frempl, spanish coverage, pricing_game_2016, pricing_game_2017, spanish homeowners, spanish 2015-2018, wisconsin, loan_default, noaa_storm, noaa_afsc, wadden and allstate; boreal with its issues 8 and 9. Liberty releases no such column; walmart's definition is not on this branch and gets its note with its own review.

  [^xa1]: **MET-14** (Should, 2026-11-06, Lennart): "The count or amount leaves the frame as a part of the target (LEAK-10)". **LEAK-41** (Must): a realized weight "is never a model input". **MET-15** (Must): "A declared sample weight is always the metric's row weight". **MET-16** (Should): "A weight for training alone cannot be declared".

- **Keep sex out of every insurance pricing task, or decide by each use case's actor?**
  * **Problem:**
    - Since 2026-11-08 sex leaves every insurance pricing task, whatever the actor's jurisdiction, "as if we were to simulate the case in europe always"[^xb1].
    - In three of the five datasets it touches, the actor the use case names could price on sex: an Australian insurer in 2004-05, a French insurer in 2004, and the 2017 pricing game, whose rules offered it and whose data year predates the EU ban.
    - The audit counts it as information available at prediction time that the benchmark withholds.
  * **Background:**

    | Dataset | Actor in the use case | May the actor price on sex? | Measured effect of keeping it |
    |---|---|---|---|
    | bemtpl97 | EU insurer pricing today | no, barred since 21 December 2012 | (dropped on 2026-11-05 under either option) |
    | australian_vehicle_insurance_2004_2005 | Australian insurer | likely yes (the statute was not read) | +0.004 Tweedie GLM, better on 7 of 9 splits |
    | frempl_french_motor_personal_line | French insurer, 2004 | yes in 2004; no for an EU insurer today | not measured |
    | pricing_game_2017_french_mtpl | the game's players | yes: the game's file and rules offered it | not measured |
    | spanish_homeowners_motor_insurance_2010_2014 | Spanish insurer at renewal | until 21 December 2012; not after | -0.004 to +0.017 Gini across five models |

  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | Family stance (implemented) | sex leaves every insurance pricing task | one rule; matches EU practice today | withholds a factor three of the named actors may use |
    | B | By the use case's actor | sex stays where the actor and the period the use case names allow it, and leaves where they bar it; each dataset decides in its own issue | the inputs are what the actor has | five calls; the family differs in its inputs |
    | C | Restate the actors | keep A, and rewrite the use cases of australian, frempl and pricing_game_2017 as an EU insurer pricing today | stance and actor agree | the data are neither EU nor today's; a stand-in actor in three more tasks |

  * **Recommendation:** B: the curator's standard is the information the actor has at each moment, and the law that binds the named actor is part of that; the per-dataset issues follow in the next round.
  * **Decision:** A, B or C?

  **Notes for the AI:** B: amend the Tensions row in principles.md ("sex leaves the rating factors of every insurance pricing task" goes; the actor's legal constraint in the use case decides, USE-6), reopen one issue per dataset (australian, frempl, pricing_game_2017, spanish homeowners) with the law that binds its actor, restore the column where the issue decides so.

  **Andrej (2026-11-09, discuss):** If the EU bans it today, we treat it as if it also has been banned before. For non-banned countries, we use it. Is that already the policy? If not what is it?

  **Answer (AI, 2026-11-09): Make your rule the policy: sex leaves an insurance pricing task where the law of the data's country bars it today, and stays where it allows it?**
  * **Problem:**
    - It is not the policy now: since 2026-11-08 sex leaves every insurance pricing task, whatever the country, "as if we were to simulate the case in europe always"[^xb1].
    - Your rule reads today's law in the country the data come from; it differs from the policy now only where that law allows sex, and from option B in reading today's law rather than the law of the data's year.
  * **Background:**
    - Under your rule the four EU tables stay as they are, sex dropped (bemtpl97, frempl_french_motor_personal_line, pricing_game_2017_french_mtpl, spanish_homeowners_motor_insurance_2010_2014), and australian_vehicle_insurance_2004_2005 gets `gender` back.
    - Australia allows it today: the Sex Discrimination Act 1984, s41 (compilation of 1 November 2025, now read), exempts discrimination on sex in the terms of an insurance policy when it is "based on actuarial or statistical data from a source on which it is reasonable for the insurer to rely" and reasonable having regard to the data, with the data shown to a client who asks[^xb2].
    - Of the 15 insurance tables among the 190 definitions, only these five have a sex column. The credit tables that keep one (home_credit_default_risk, credit_card_clients_default, credit_g) are credit, not insurance, and outside this rule.
    - A future US table would read its state's law: several states bar sex in car insurance rating (California, Massachusetts and Pennsylvania among them), most do not.

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | a | Your rule: today's law of the data's country | sex leaves the tables from countries that bar it today, as if the ban had always applied, and stays where today's law allows it; today this restores `gender` in australian only | one test per table, easy to check; the EU tables match EU pricing today | an EU table from before December 2012 loses a factor its actor then used |
    | b | Keep the policy of 2026-11-08 | sex leaves every insurance pricing task | one rule, no law to look up | withholds a factor an Australian insurer may use today |
    | c | Option B above: the law in the use case's year | sex stays where the actor could use it then (australian, frempl in 2004, pricing_game_2017, spanish homeowners before 21 December 2012) | the inputs the actor had then | four per-dataset calls; spanish homeowners straddles the ban |

  * **Recommendation:** a: it is the rule you state, it needs one check per table, and today it changes only australian, where keeping `gender` measured +0.004 on the Tweedie GLM, better on 7 of 9 splits. **Decision:** a, b or c?

  **Notes for the AI:** on a: rewrite the Tensions row in principles.md ("sex leaves the rating factors of an insurance pricing task when the law of the country the data come from bars it today, as if the ban had always applied; where that law allows it, sex stays (USE-6)"), with australian as a Cases row; restore `gender` in australian_vehicle_insurance_2004_2005 (its issue 7 reopened and resolved, CC line, CHANGELOG, `dataset check` and the leak probes); close this item and option B above.

  **Andrej (2026-11-09, go ahead):** I go with a.

  **Resolved (2026-11-09, Andrej):** a: sex leaves an insurance pricing task where the law of the country the data come from bars it today, as if the ban had always applied, and stays where that law allows it. It replaces the family stance of 2026-11-08 in the Tensions row of principles.md. australian_vehicle_insurance_2004_2005 ships `gender` again (a new issue in its Review, reopening its issue 7); bemtpl97, frempl_french_motor_personal_line, pricing_game_2017_french_mtpl and spanish_homeowners_motor_insurance_2010_2014 keep it dropped under EU law.

  [^xb2]: Sex Discrimination Act 1984 (Cth), s41(1)(c) to (e), https://www.legislation.gov.au/C2004A02868/2025-11-01/2025-11-01/text/original/epub/OEBPS/document_1/document_1.html. The EU ban: CJEU C-236/09 (Test-Achats), in force for new contracts from 21 December 2012.

  [^xb1]: The Tensions row on rating factors in principles.md, amended 2026-11-08 (Lennart, on australian_vehicle_insurance_2004_2005, issue 7), against the panel's recommendation there that Australian law decide. The row's default, a use case set in the data's own time keeping a factor known then (**USE-6**), stays for every other factor.

- **State how mature the training labels are, in every claims definition?**
  * **Problem:**
    - Every release gives the claims as finally recorded, while at a refit the newest year's claims are partly reserves and some are not yet reported.
    - Where the source lets us measure it, the share is large: in pricing_game_2016, 37% to 39% of each year's claims closed only after the year ended (`ANNEE_CLOTURE`, counted on the raw file); spanish homeowners and wisconsin train with no gap on final amounts.
    - No rule asks a definition to state it, so a reader of the notes cannot tell how much more the training labels know than the actor would.
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | As is (implemented) | some definitions mention it, most do not | no work | the training side's extra maturity is invisible |
    | B | A note in every claims definition | one bullet: how the labels were valued, and the share still open at a refit where the source gives closure dates or a status | the gap is stated where it exists; cheap | text only; the gap stays |
    | C | B, and a gap that covers the claims' development | where closure dates exist, a temporal split's gap or a mask covers the claims still open at the refit | removes the extra maturity where it can be measured | fewer training rows; only a few sources give closure dates |

  * **Recommendation:** B now; C where a dataset's own split issue reopens.
  * **Decision:** A, B or C?

  **Andrej (2026-11-09, go ahead):** B.

  **Resolved (2026-11-09, Andrej):** B: the ten claims definitions of PR #47 carry one bullet "Note: how mature the labels are (cross-dataset item of 2026-11-09, Andrej): ..." with what the amounts are, as of when, the share still open at a refit where the source tells, and whether both sides of the split share it, plus a CC line in each record. Only pricing_game_2016 gives closure years: 38.5%, 39.2% and 39.2% of the claims of 2011 to 2013 were still open at the next 1 January (the 41 claims open at the extract counted as open; the Problem's 37% to 39% counted them as closed); spanish_motor_insurance_2015_2018 is the one table whose test labels are the less developed. Not yet covered: bemtpl97 and fremtpl2 (Lennart), allstate_claims_severity and porto_seguro (unclaimed).

- **Add a `sum` aggregation and a per-group mean RMSE to the scorer?**
  * **Problem:**
    - noaa_storm's planner judges the summed damage per county and hazard, but the scorer can only take the last, the mean or the maximum of a group's rows.
    - wadden's mapper judges each survey's map, but the library has only a per-group RMSE normalised by the group's spread, not a plain mean of per-group RMSE.
    - Whether to use either is decided in noaa_storm's issue 12 and wadden's issue 8; this item is only the code.
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | As is (implemented) | no new aggregation or metric | nothing to maintain | the two scores cannot follow the actor's unit |
    | B | Add what the dataset issues choose | `sum` as a per-group aggregation (both the truth and the predictions summed per group) and `mean_group_rmse`, each with the metric tests | small code; serves the two issues | two more library entries |

  * **Recommendation:** B, added only for what noaa_storm's issue 12 or wadden's issue 8 chooses.
  * **Decision:** A or B?

  **Andrej (2026-11-09, leave as is):** A.

  **Resolved (2026-11-09, Andrej):** A: no new aggregation or metric now. wadden's issue 8 can choose its option C with what the library has (`mean_group_normalized_rmse`); noaa_storm's issue 12, whose option C needs `sum`, brings this item back if it chooses the cell sums.

### From the review of rule-following of 2026-11-09 (calls a convention made rather than the task)

- **Set a deviance's floor where the actor would clip, instead of two orders below the smallest plausible mean?**
  * **Problem:**
    - Since 2026-11-06 a deviance's floor sits two orders of magnitude below the smallest plausible mean, a convention of the collection, which put pricing_game_2017's floor at 0.1 EUR and noaa_storm's at $1[^xc1].
    - On both, the floor decides how far the models fitted by squared error fall behind a constant, while the best model does not move: on pricing_game_2017 untuned LightGBM scores 74.9 at a 1 EUR floor and 102.8 at 0.1 EUR, against 63.3 for the constant.
    - Neither actor acts on a prediction that low: no insurer quotes a premium of 0.1 EUR, and the storm files hold no damage below $10, so the convention scores differences no decision uses.
  * **Background:**
    - The floor's reason when it was introduced was practice: "in pratice we would also clip to a reasonable number" (Lennart, 2026-11-04, on bemtpl97); the factor of 100 came with the amendment of 2026-11-06[^xc1].
    - A floor changes the score only for predictions below it, and above power 1 the Tweedie deviance's cost of such a prediction on a row with a claim grows as the prediction falls, without bound, so the lower the floor, the more a few near-zero predictions decide the rank.
    - Where the floor binds, by dataset: pricing_game_2017 0.1 EUR, 3.9% to 6.6% of the probe's linear and LightGBM predictions at the floor; noaa_storm $1, 44%; pricing_game_2016 0.1 per vehicle-year, 6 of 261,684 untuned predictions and none of the GLM's or a regularised LightGBM's, so it does not matter there; fremtpl2 and bemtpl97 1e-4 claims per year, not measured here.
  * **Effect on the task:** under the convention, a benchmark on these two tasks ranks methods partly by whether a squared-error fit outputs values near zero, which no pricing or planning decision reads.
  * **Experiments:** pricing_game_2017, the mediator's run of 2026-11-06 (shipped repeat 0, folds 0 to 2, untuned, mean Tweedie deviance, lower is better): the constant 63.31 at every floor; the random forest 60.57 at 1 EUR and 60.59 at 0.1 EUR; ridge 61.61 and 66.33; LightGBM with squared-error loss 74.94 and 102.83; LightGBM with the Tweedie loss 75.51 and 78.11.
  * **Consistency:** the per-dataset values are each dataset's own issue: pricing_game_2017 issue 7 and noaa_storm issue 14.
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | Two orders below the smallest plausible mean (implemented) | one formula for every deviance | no judgement per dataset; nothing to change | the floor scores predictions no actor acts on; it ranks squared-error fits by their near-zero outputs |
    | B | Where the actor would clip | each definition states the lowest value its actor acts on, with the fact behind it (the smallest premium an insurer quotes, the smallest amount the source records), never above the smallest plausible mean | the floor's first reason, practice; a score difference below the floor is not a decision anyway | a value and a fact per dataset; no single formula |
    | C | Keep A and fit with the metric's loss | the benchmark side fits models with the deviance's own loss where they have one (the next item), so fewer predictions reach the floor | no rule change | methods without such a loss still predict by squared error, and the floor still ranks them |

  * **Recommendation:** B, with the values picked in pricing_game_2017 issue 7 and noaa_storm issue 14; pricing_game_2016's floor stays, as no reasonable model reaches it.
  * **Decision:** A, B or C?

  **Notes for the AI:** On B: amend MET-13's floor sentence in `metrics.md` to: "the lowest value the use case's actor acts on (a minimum premium, the smallest amount the source records), stated with its fact, and never above the smallest plausible mean on the scale the metric scores", with the curator and the date, keeping the task probe's share at the floor; a Cases row for each dataset whose floor changes; fremtpl2's and bemtpl97's 1e-4 checked against the new wording in one sentence each (no change unless a fact says so). Then apply the two per-dataset issues.

  **Andrej (2026-11-09, go ahead):** I go with your suggestion to define it per dataset

  **Resolved (2026-11-09, Andrej):** B: MET-13's floor is the lowest value the use case's actor acts on, stated with its fact, never above the smallest plausible mean; it replaces the two-orders convention of 2026-11-06 in metrics.md, definitions.md and the metric library's descriptions. noaa_storm issue 14 sets $10; pricing_game_2017 issue 7 stays open; fremtpl2, bemtpl97 (1e-4) and pricing_game_2016 (0.1) keep theirs, as no honest prediction reaches them.

  [^xc1]: **MET-13** (Must, amended 2026-11-06, Lennart; in main): "The floor is a parameter the definition states, as practice clips a model's output before scoring (Lennart, 2026-11-04, on bemtpl97: "in pratice we would also clip to a reasonable number"): two orders below the smallest plausible mean, on the scale the metric scores (...; applied 2026-11-08, Lennart: 0.1 EUR on pricing_game_2017_french_mtpl, a convention of the collection that can change later)".

- **Fit the benchmark's models with the metric's own loss on deviance-scored tasks?**
  * **Problem:**
    - Six tasks of the working copy are scored by a Poisson or Tweedie deviance, yet most methods of the benchmark fit a regression by squared error, so on a zero-heavy target they output values near zero or below, which the floor then scores.
    - `BENCHMARK_CHANGES_TODO.md` plans weighted validation and the floor in early stopping, but no change to the loss a model fits.
    - A practitioner on these tasks fits a Poisson or Tweedie loss with a log link; should the benchmark do the same where a method has one?
  * **Background:**
    - The deviance-scored tasks: fremtpl2 and bemtpl97 (Poisson), pricing_game_2016 (rescaled Tweedie), pricing_game_2017 and noaa_storm (Tweedie), plus any later one.
    - LightGBM, XGBoost and CatBoost have Poisson and Tweedie objectives with a variance power; the neural and in-context methods (RealMLP, TabM, the TabPFN wrappers, TabICL) do not, and would keep squared error (an AI reading of their interfaces, not checked per version).
    - On pricing_game_2017 LightGBM fitted with the Tweedie loss moves from 75.51 to 78.11 between the 1 EUR and 0.1 EUR floors, the squared-error LightGBM from 74.94 to 102.83 (the item above).
  * **Effect on the task:** with the loss matched, the score compares how well methods price; without it, partly how they behave near zero.
  * **Unknown:** whether TabArena's protocol allows a method's loss to follow the task's metric, which is TabArena's call, not Data Foundry's.
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | As planned (implemented) | weighted validation and the floor in early stopping only | methods run as configured elsewhere | squared-error fits on zero-heavy targets; rankings partly by near-zero outputs |
    | B | The metric's loss where a method has one | the adapter reads the metric (`mean_poisson_deviance`, `mean_tweedie_deviance` with its power, `rescaled_mean_tweedie_deviance`) and sets the matching objective on LightGBM, XGBoost and CatBoost; the others clip to the floor | what a practitioner fits; fewer predictions at the floor | methods differ in what they are allowed; a TabArena change |

  * **Recommendation:** B, as a `BENCHMARK_CHANGES_TODO.md` entry for TabArena to decide.
  * **Decision:** A or B?

  **Notes for the AI:** On B: a section "Losses for deviance-scored tasks" in `BENCHMARK_CHANGES_TODO.md` under the training-weights part: the metric-to-objective map (Poisson: `poisson`; Tweedie: `tweedie` with `tweedie_variance_power` = the metric's `power`; the rescaled deviance as Tweedie), the floor as `min_prediction` on every method's output, the list of tasks; no Data Foundry code change.

  **Andrej (2026-11-09, go ahead):** Yes, we should definitely stick to what practitioners do wherever possible, but we also need more research on that.

  **Resolved (2026-11-09, Andrej):** B, as a TabArena call: `BENCHMARK_CHANGES_TODO.md` has the section "Losses for deviance-scored tasks" (each deviance's Poisson or Tweedie objective on LightGBM, XGBoost and CatBoost, the floor on every method's output, the five tasks) with an open-research list: which methods have such a loss, whether matched losses change the rankings, what practitioners fit per task.

### From the two new temporal checks of 2026-11-11 (the PR on top of #78)

- **Accept `splits_feature_missing_in_test` where a column starts or stops being recorded within the history?**
  * **Problem:**
    - The new check warns when a feature is 95% or more missing on one side of a temporal window and at most half
      missing on the other: a column the source starts or stops recording, which a model then learns on one side only.
    - It fires on definitions where nobody named the change yet (delivery_eta_1m's 45 features, the case it was built
      for, are decided: issue 2, A, 2026-11-10).
    - Each is the data as the deployed model met it at that window, so each column stays unless it leaves for what it
      is[^fm1]; the question is whether you accept the warning on all of them with a note, or want any column dropped.
  * **Statistics:** missing shares from the check (up to 100,000 rows a side) and by year or quarter on the full frame.

    | Dataset | Columns | When they start or stop | Windows it affects |
    |---|---|---|---|
    | anes_voting_2026 | 95 questions | asked in some election years only (the notes count 33 asked in all nine test years) | every test election misses the questions of its year's questionnaire |
    | college_scorecard | `DISTANCEONLY` | recorded from the 2011 cohort on | the 2016 window's train side (before the gap) has none |
    | home_credit_default_stability_1m | 27 columns | `contractssum_5085716L` and `*_amount_4917619A` start in 2020 Q2 (all missing before, 17% to 59% after); `responsedate_1012D` stops in 2019 Q4 | all three windows |
    | onlinenewspopularity | `kw_min_min` | present in 2013 (0% to 35% missing), missing in every 2014 article | every test window (all in 2014) |
    | rain_in_australia | 12 station readings | sensors that go offline for a period, e.g. `Pressure9am_at_Sale` missing from 2017 Q4 | some of the 26 fortnights |
    | sberbank_housing_market_forecasting | 3 yearly lags | `provision_retail_space_sqm_lag_1y` stops in 2014; the two `*_education_*_lag_1y` start in 2014 | all three windows |
    | wisconsin_local_government_property_insurance_fund | `NoClaimCredit` | recorded from 2008 on | the 2008 window's train side (2006-2007) has none |

  * **Effect on the task:** each warning is a fact of the source a deployed model meets too; dropping a column would
    remove information the newer windows have (college, wisconsin, home_credit) or the older ones had.
  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | Accept on all seven, with a note | each definition names the columns and when they start or stop in `curation_comments` and accepts the warning with your CC date | the data as published and as deployed; one rule for all | models are partly compared on columns one side lacks |
    | B | Drop the columns | each definition drops the named columns | both sides of every window see the same columns | removes information the deployed model has; departs from CLEAN-22 |
    | C | Per dataset | A for some, B for others, as your note names them | | |

  * **Recommendation:** A: none of the columns leaves for what it is, and the deployed model met each change.
  * **Decision:** A, B or C?

  **Notes for the AI:** On A: per definition, one `curation_comments` bullet "Columns recorded on one side of a window
  only (cross-dataset item of 2026-11-11): ..." with the columns and the dates from the table, `accepted_check_warnings`
  `"splits_feature_missing_in_test"` with the count and the CC date, a CC line in the record, `dataset check`
  (0 errors), and a CHANGELOG entry. On B, also `dataset check` and the windows' statistics again.

  **Lennart (2026-11-11, ok):** As recommended (A).

  **Resolved (2026-11-11, Lennart):** A, consistent with delivery_eta_1m's issue 2 (2026-11-10). The seven definitions
  name the columns and when they start or stop in a `curation_comments` bullet and accept
  `splits_feature_missing_in_test` with the CC date (rain_in_australia gets its first `accepted_check_warnings`);
  each record has the CC line and an Assessment with the shares. `dataset check`: 0 errors, the warning accepted on
  all seven.

  [^fm1]: **CLEAN-22** (Must): "Columns leave for what they are (a leak, an identifier, a copy, the measurement that
    defines the label), never for how many there are."

- **What to do with a newest period that holds far fewer rows than the periods before it?**
  * **Problem:**
    - The new check `time_newest_period_short` warns when the newest 30 days of a date column hold under 60% of the
      median rows a day of the 30-day spans before: often a download or scrape cut before the outcomes were complete
      (kickstarter's newest launches, settled on 2026-11-11).
    - It fires on four definitions; two of them already name the cause in their notes.
  * **Statistics:** rows a month at the end of each time column, and the target's share or mean.

    | Dataset | The newest month(s) | The months before | Target | Reading |
    |---|---|---|---|---|
    | coffee_rating_prediction | October 2023: 2 reviews | 24 to 65 a month in 2023 | 94.5 against 92.4 to 93.3 | the scrape's partial last month (dates are months) |
    | consumer_complaints_1m | December 2025: 54,655 | 73,058 to 77,970 in Sep-Nov 2025 | monetary relief 2.2% against 1.5% to 1.8% | complaints still in progress at the download leave the frame; the notes give the in-progress shares, and LEAK-24 names this dataset |
    | rosbank1 | November and December 2017: 123 and 63 clients | 416 to 524 a month from May to October | churn 39.8% and 36.5% against 34.8% to 45% | the notes already say the newest periods are a thin tail of the client intake |
    | sberbank_housing_market_forecasting | 2015: 394 to 724 sales a month | 1,044 to 1,583 from September to December 2014 | log price 11.80 to 11.87, flat | the market after the December 2014 rush (the rouble crisis), not a cut: the data ends where the competition's training file ends, 30 June 2015 |

  * **Options:**

    | | Option | What it does | Pro | Con |
    |---|---|---|---|---|
    | A | Per dataset, as recommended | coffee drops its 2 reviews of October 2023; the other three accept the warning with the reason in the table | cuts only the partial month; the other causes are named | four calls on one check |
    | B | Accept on all four | each accepts the warning with its reason | no data change | coffee keeps a month of 2 reviews |

  * **Recommendation:** A.
  * **Decision:** A or B?

  **Notes for the AI:** On A: coffee_rating_prediction drops the rows with `review_date` of October 2023 in `_clean`
  with a `curation_comments` bullet, then `dataset check` and its windows' counts; consumer_complaints_1m,
  rosbank1 and sberbank_housing_market_forecasting accept `"time_newest_period_short"` with the numbers and the CC date.
  Each gets a CC line in its record and a CHANGELOG entry.

  **Lennart (2026-11-11, ok):** As recommended (A).

  **Resolved (2026-11-11, Lennart):** A, consistent with kickstarter's cut of the scrape's last 60 days (2026-11-11).
  coffee_rating_prediction drops the 2 reviews of October 2023 in `_clean`, with a note; its 2-month windows now walk
  back from August-September 2023 (12 windows to October-November 2021, 62 to 137 test reviews each, in place of 13),
  and the splits comment and the row description say so. consumer_complaints_1m, rosbank1 and
  sberbank_housing_market_forecasting accept `time_newest_period_short` with the numbers of the table. Each record
  has the CC line and an Assessment. `dataset check`: 0 errors on all four.
