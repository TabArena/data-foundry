# Across datasets

### Rules (`.claude/skills/knowledge-curation/`)

- **Add two optional rule rows for consistency (from `huesken_sirna_efficacy`, no effect on that dataset)?** The few-groups acceptance (`heart_disease` with 3 hospitals, `huesken_sirna_efficacy` with 30 genes, your wording that a group is a large set of observations over which we generalise) has no Cases row, and `huesken_sirna_efficacy` is the second grouped-ranking exception to MET-5 after `protein_model_quality_rf_pcp`; a third one makes an amendment of MET-5 due (principles, "Exceptions and amendments"). The panel's evidence is weaker there than in RF-PCP: between-gene differences are 17.1% of the variance and the literature reports pooled metrics, so the use case (MET-1) alone carries it.
  Implemented: nothing in the rule files.
  Alternative: a Cases row under "Few groups" in `splits.md` and a Cases row in `metrics.md` noting the second exception (two separate rows, decided separately).
  Decision needed: add the rows or leave the rule files as they are.
  **Lennart (2026-11-04, ok):** add row
  **Resolved (2026-11-04, Lennart):** go ahead. The few-groups Cases row for huesken_sirna_efficacy is in `splits.md` (heart_disease's row was already there); the MET-5 row naming huesken as the second exception was already in `metrics.md` (5085fc1a), so it is not added twice. No MET-5 amendment is due before a third exception.
- **Correct the stale spectrum figures in `spectra.md` (from `open_soil_spectral_library`)?** Line 113 still says "1,701 positions"; 1,700 ship since the 600 cm-1 bin was dropped. Lines 114-123 still show the encoding table on the percent scale, and two of its conclusions reverse on the declared `rmsle` scale ("PLS gains a little from the baseline", "ridge reads the spectrum best as it is"). The mediator listed both as changes to make now (its changes 2 and 5); the apply step could not touch skill files.
  Implemented: the definition and the REVIEW.md have the declared-scale figures; `spectra.md` does not.
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
- **`lt_vehicle_loan_default_prediction`.** Correction lines in the record for the 2026-11-04 Assessment ("about 90%" of the gain is training size; "20-53% (SPLIT-14)"), its pointer to "REVIEW.md issue 1" (now issues 4 and 5) and "review panel (none) ... all are settled"; mark the 2026-10-23 "Exception to SPLIT-10" line as history; set the `Selection Bias` marker (USE-8).
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
  each dataset's REVIEW.md from now on (review_file_format.md, working_copy.md).

- **Correct african_credit_scoring_challenge's `row` text and notes on co-funded loans?** The `row` text and the notes (line 153) say a loan co-funded with a second lender gives two rows; in the shipped frame that never happens (52,826 rows and 52,826 loan ids), since the kept product has one lender (found by the scan above).
  Implemented: nothing.
  Proposal: say one row per loan and drop the co-funding sentence; text only, the README regenerated.
  Decision needed: go ahead or leave as is.
  **Resolved (2026-11-08, Lennart):** go ahead, applied: the `row` text, the notes, the splits comment and decision
  table 4 now say one row per loan; README regenerated, checksum changed (not built).
