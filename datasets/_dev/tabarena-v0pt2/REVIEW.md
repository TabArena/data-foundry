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
