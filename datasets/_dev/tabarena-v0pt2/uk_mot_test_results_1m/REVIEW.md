# uk_mot_test_results

**Outcome:** added as `uk_mot_test_results_1m`. DVSA's anonymised MOT data: one row per initial MOT test in Great Britain (a random quarter, 13.3 million, of the 53.2 million tests of July 2024 to December 2025), whether the vehicle fails as presented (fail or pass after rectification, 27.7%), from the vehicle, its odometer and its previous test of the last 18 months; tested on October, November and December 2025 (500k tests each) with a random million earlier tests per train side. The AI recommends shipping it after the panel's changes, which are made.

```text
Verdict: ship after changes (made).
Validity: every Must holds (SEL-1, USE-1, USE-5, USE-10, LEAK-10, SPLIT-1, SPLIT-9, SPLIT-14, PROV-8, PROV-9). The test's own items and completed_date are dropped; the history reads only earlier days (300 random rows re-derived with plain filters, all matching). LEAK-9 is handled by a protocol line (an evaluation rule for participants: a fold uses only its own train rows, and test rows are predicted without other test rows or later-dated rows), widened by the panel: a vehicle's later rows (same window or dated after it) give away 657 / 1,509 / 1,586 test rows (Dec / Nov / Oct folds), 38,728 of 38,734 linked labels right (over all 2.5M rows), +0.0014 to +0.0027 ROC AUC; no re-split, no rows dropped.
Value: a real signal (LightGBM 0.706 ROC AUC, the best single feature (first use date in two splits, test mileage in one) 0.642, the previous result alone 0.597; LightGBM minus random forest +0.032, SE 0.004).
Quality: the HYBRID ELECTRIC (CLEAN) spelling stays merged into the HY code: the same fuel written as words by another recording path (16.8% against 13.0% fails, a recording or cohort difference the fuel column is not meant to carry); notes added on the test-month density, the odometer read at the start of the test and the vehicle record as of the June 2026 extract.
Weighed: use case +, source +, shape +, gap 0, risk - (thin per-test inputs; the label is recorded by the tester being audited).
For the curator: 1, the metric.
```

**Main points:** One call: keep the fallback ROC AUC (implemented, recommended now) or score log loss; decide it once with sivep_gripe_sari_outcome, nyc_motor_vehicle_collisions and nchs_linked_birth_infant_death_1m on the **across-datasets log_loss-from-context item**.

**Issues for the curator:**

1. **Keep ROC AUC (ranking), or score log loss (calibrated chances)?**

   * **Problem:**
     - The source names no metric, so the rules' default for a binary task, ROC AUC (how well the predictions rank fails above passes), is implemented.
     - Its stated reason now describes a ranking use: officers look for the tests and testers whose recorded results run against the prediction.
     - DVSA's blog describes comparing each tester's recorded failures with the model's predicted chances; summing chances into an expected failure count needs calibration (predicted chances that match the observed failure rates), which ROC AUC does not score, since it only scores the order of the predictions.
   * **Effect on the task:** which models win, untested: no probe compared the model ranking under both metrics. Both separate a fitted model from a constant guess: LightGBM log loss 0.541 against 0.594 for always predicting the 27.7% base rate; ROC AUC 0.706.
   * **Experiments:** none run; the panel disputed no fact, only the weighing (mediator).
   * **Consistency:** this is the question of the **across-datasets log_loss-from-context item**, open for sivep, nyc and nchs too; decide it there or here, the same way. The closest decided cases, african_credit (2026-10-26) and heart_disease (2026-10-27), had stronger calibration signals and kept ROC AUC; no binary dataset takes log loss from context today; fmcsa, sivep, nyc and nchs in this batch also ship the fallback ROC AUC[^met8][^met11].
   * **Panel:** the builder, the claim auditor and the domain practitioner lean to log loss (the blog's decision is expected against observed failures; the practitioner would report ROC AUC alongside). The advocate and the precedent checker keep ROC AUC: the comparison is per tester and no tester column ships[^met2], so per-row log loss is only a proxy; the context is one blog paragraph where the rules ask for a clear one[^met11]. The critic defers to the cross-dataset ruling.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Log loss from context, as an exception | scores log loss, justified by the use the blog describes (expected against recorded failures per tester), as an exception for this dataset | scores the calibration the actor sums | the per-tester comparison it stands for cannot be scored (no tester column), so per-row log loss is a proxy; the first binary log loss from context; breaks consistency with african_credit and heart_disease unless the fact that the use sums chances per tester is accepted as distinguishing |
     | B | ROC AUC with the reworded reason (implemented) | keeps the default metric the rules give a binary task when the source names none | consistent with the fallback rule and every binary precedent | ignores calibration |
     | C | Amend the metric rules | a binary use acting on calibrated probabilities takes log loss; applied to uk_mot, sivep, nyc and nchs together | one rule for all four | a rule change larger than this dataset; reopens african_credit and heart_disease |

   * **Recommendation:** B now; C if you want calibration scored across the batch. **Decision:** A, B or C?

   **Notes for the AI:** on A or C, declare the metric from context with its reason (expected against observed failures per tester), re-check african_credit and heart_disease under C, and re-run `dataset check`; under C, also write the new metric reason in sivep_gripe_sari_outcome, nyc_motor_vehicle_collisions and nchs_linked_birth_infant_death_1m, and re-run their checks.

   [^met8]: **MET-8** (Should): with no source metric, score classification by a strictly proper scoring rule or a ranking metric; the fallback is `roc_auc` for binary tasks.
   [^met2]: **MET-2** (Must): the metric scores what the actor decides on; here the decision is per tester, and no tester column ships.
   [^met11]: **MET-11** (Must): every metric has one origin; a metric from context needs a clear context.

**Review panel:** ship after changes (mediator). Full panel: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator; the rebuttal round was skipped: the advocate's and the critic's briefs converged on every change, and the critic deferred the metric to the cross-dataset ruling. Claim audit: no validity claim refuted; the metric reason argued for calibration while picking a ranking metric (reworded). Split audit: the monthly temporal windows hold, no gap needed. Task gamer: one exploit, linking a vehicle to its later rows (+0.0014 to +0.0027 ROC AUC), covered by the widened LEAK-9 protocol line. Blind review: include with changes; the 8x denser test months are now explained in the notes. Applied with no decision: the LEAK-9 line widened with the gamer's counts, the metric reason reworded, notes on the test-month density, the odometer, the June 2026 vehicle record and the hybrid fuel merge, the fit_reason on the missing tester id. Disputed and handed over: the metric (issue 1).

<details><summary>Mediator: uk_mot_test_results</summary>

```text
MEDIATOR REPORT: uk_mot_test_results (folder uk_mot_test_results_1m), 2026-11-09

SUMMARY (15 lines max)
- Verdict: ship after changes. Every validity rule holds. The panel found no Must that the definition cannot fix.
- Make now, no decision needed:
  1. Widen the LEAK-9 protocol line and the BENCHMARK_CHANGES_TODO entry, and restate the counts (657/1,509/1,586 linked test rows).
  2. Rewrite the metric reason.
  3. Add five notes or fit_reason sentences: test-month density, test_mileage read at the start of the test, the vehicle record as of June 2026, the reason for the HYBRID ELECTRIC (CLEAN) merge, and the missing tester id as something the use case needs.
- For the curator: one issue, the metric. The roc_auc fallback is implemented; log_loss from context is the alternative. This is a weighing call. The same question is open for sivep, nyc and nchs, so rule on it once across all four.
- No rebuttals were filed. The opening briefs agree on every point except the strength of the push for log_loss, and the critic also defers that to the cross-dataset ruling. I found no disputed fact, so I ran no experiment.

JUDGMENT RECORD
Verdict: ship after changes.
Validity: SEL-1 holds; USE-1 holds (direct fit, the DVSA blog's "predictive vehicle failure model"); USE-5 holds (F or PRS); USE-10 and LEAK-34 applied (dated history); LEAK-10 triggered, fixed (the test's own items and completed_date dropped); LEAK-9 triggered, kept as a protocol line, to be widened to cover rows dated after the window; SPLIT-1, SPLIT-9 and SPLIT-14 hold (monthly windows, overlap 0, 15-17 training months); PROV-8 and PROV-9 hold.
Value: TP-1 to TP-10 hold (LightGBM 0.706 against 0.642 for a single feature and 0.597 for the naive previous result; LightGBM minus RF +0.032, SE 0.004). MET-1 and MET-2 hold. The MET-8 reason text is defective; fix it.
Quality: CLEAN-10, CLEAN-11 and CLEAN-12 applied. CLEAN-12: the HYBRID ELECTRIC (CLEAN) merge needs a stated reason or its own level. P7 notes to add: test-month density, test_mileage, vehicle record date.
Weighed: use case +, source +, shape +, gap 0, risk - (thin per-test inputs; the label is recorded by the tester being audited).
For the curator: issue 1, a weighing call (roc_auc fallback or log_loss from context, decided once with sivep, nyc and nchs).

CHANGES TO MAKE NOW (no decision needed)
1. LEAK-9 (P4): the protocol line covers less than the leak the panel measured. The builder's 554-671 rows per window count only later test rows in the same window. The task gamer also links rows dated after the window. These rows stay in data.parquet but are in neither train nor test for the Oct and Nov folds. He linked 657 / 1,509 / 1,586 test rows (Dec / Nov / Oct folds); 38,728 of the 38,734 linked labels were right; the gain was +0.0014 to +0.0027 AUC.
   - Remedy, the mildest rung: reword the notes and the BENCHMARK_CHANGES_TODO entry to "a fold uses only its own train rows; test rows are predicted without any other test row or later-dated row", and put the larger counts in the notes. No re-split and no row drops: dropping rows, the gamer's fix, is a stronger remedy than the protocol needs.
   - Advocate and critic agree on this.
2. MET-8 and MET-11 (P6, Should): the metric reason "officers compare each test's chance with the recorded result, so ROC AUC" argues for calibration while picking a ranking metric. The claim auditor refuted it, and the advocate concedes it.
   - Under the current choice: reword to a ranking use (which tests and testers run against the prediction) and say the source names no metric.
   - If the curator picks log_loss: write the reason for that instead.
3. Notes sentences (P7 or P4 notes, no code change):
   (a) Test months are sampled about 8x more densely than training months. This comes from the 1M/500k row budget, which keeps test windows whole as in chicago_taxi. Yes rates stay in band (SPLIT-14).
   (b) test_mileage is read at the start of the test, as part of presenting the vehicle (LEAK-10 holds; say so).
   (c) make, model, colour, fuel, cc and first_use may be the vehicle record as of the June 2026 extract, not as at the test (CLEAN-1).
   (d) The HYBRID ELECTRIC (CLEAN) merge into HY removes a 16.8% against 13.0% fail-share difference. Either state why the merge is right (same fuel, a different recording path) or keep the spelling as its own level (CLEAN-12). Both are acceptable; the builder can pick one, as it is P7.
4. fit_reason (USE-1): state that the missing tester and station identity is what the use case needs. The model must estimate a vehicle's expected outcome independent of who tests it (domain practitioner).

ISSUES FOR THE CURATOR (ranked)
1. Metric (P6; MET-2, MET-8, MET-10, MET-11; Should and Weigh, a weighing call). The source names no metric. The fallback roc_auc is implemented.
   Problem: DVSA compares each tester's sum of predicted failure chances with the failures recorded. That comparison needs calibration, which roc_auc does not score.
   Effect: which models win. Both metrics separate the model families: log loss 0.541 against the dummy's 0.594, and roc_auc 0.706.
   Best evidence for log_loss (builder, claim auditor, domain practitioner):
   - The blog's decision is expected against observed failures.
   - The practitioner would pick log loss, with AUC reported alongside.
   Best evidence for roc_auc (advocate, precedent checker; the critic defers):
   - Consistent with MET-8 and MET-11.
   - Closest precedents: african_credit (2026-10-26) and heart_disease (2026-10-27), both with stronger calibration signals, both kept roc_auc.
   - The comparison is per tester, and no tester column ships (MET-2), so per-row log loss is a proxy for it.
   - The context is one blog paragraph, while MET-11 asks for a "clear context".
   - No binary dataset takes log_loss from context today.
   Decision needed:
   - (a) log_loss from context, as an exception that names its distinguishing fact;
   - (b) keep roc_auc with the reworded reason;
   - (c) amend MET-8 and MET-11 so that a binary use acting on calibrated probabilities takes log_loss, apply it to uk_mot, sivep, nyc and nchs together, and re-check african_credit and heart_disease.
   I recommend (b) now, or (c) if you want calibration scored. Taking (a) on this dataset alone would break consistency without a distinguishing fact. Under the per-dataset rule, the issue still goes into this dataset's REVIEW.md, as in each of the other three.

AGREED FACTS (no dispute; claim, column and split auditors and builder)
- Rows and windows:
  - 13,311,677 sampled task rows; the frame has 2.5M rows and 31 features.
  - Yes rate 0.277 in training, 0.275-0.284 in the test windows.
  - Windows: Oct 2025, Nov 2025, and Dec 2025 (ends 30 Dec). Train 1M rows, random over 2024-07-01 to the day before each window.
  - Train/test overlap 0; exact copies across the split 0.0%.
- History: reads only earlier days (minimum gap 1 day); 300/300 re-derived; 92.3% of rows have a previous test; 98.4% of previous tests fall within 547 days.
- Columns: all 31 are known at the start of the test; ids, completed_date and the test's own items are dropped.
- LEAK-9: 554-671 test rows per window from rows in the same window; 657/1,509/1,586 linked test rows when later-dated rows are included; gain +0.0014 to +0.0027 AUC, about the size of the random-column noise (+0.0002 to +0.0017).
- Fit: direct. The source names no metric.

TASK GAMER EXPLOITS MAPPED
- Exploit 1, linking a vehicle to its later rows: falls under LEAK-9 and SPLIT-1 (an evaluation-protocol leak).
  - Partly known: the builder's notes cover the same-window part, 554-671 rows.
  - New part: rows dated after the window, which push the counts to 1,509/1,586 in the Oct and Nov folds.
  - The gain the gamer measured is larger than the notes state (0.11-0.13% of rows), so this is an issue; change 1 handles it. The definition has no "Potential leak, kept on purpose:" note for it.
- The gamer's other checks (row order, label drift, columns from after the prediction point) found nothing.

CONSISTENCY WITH PRECEDENT
- The LEAK-9 protocol line follows azure_vm and chicago_taxi. The density note follows chicago_taxi's row budget.
- The metric under (b) is consistent with african_credit, heart_disease and this batch's fmcsa, sivep, nyc and nchs (all fallback roc_auc). (a) would depart with no distinguishing fact shown. (c) is an amendment and reopens two settled cases.
- No other call in this report departs from a precedent.
```

</details>

<details><summary>Claim audit: uk_mot_test_results</summary>

```text
CLAIM AUDITOR: uk_mot_test_results_1m (2026-11-09)
Verdict: ship. No validity claim refuted; one metric-rationale inconsistency (P6) and one minor decoding question (P7).
Data: participant_kit (the 2.5M shipped frame + splits) and the prepared parquet (13.31M sample). Logs: work_claim_auditor/t1-t4.log.

TABLE (claim | source | test | result | evidence | rule)
11 Yes rate 27.7% / 27.9% | claims.md, task_summary | count on prepared + frame | holds | 0.2770 of 13,311,677; 0.2790 of 2.5M | USE-5
14/17 13,311,677 rows, test ids unique, P/F/PRS only | claims 14,17 | count | holds | P 9.62M, F 2.97M, PRS 0.72M; ids unique | SEL
18 window sizes 564,611-845,719 | version_comment | month counts | holds | Oct 845,719, Nov 712,258, Dec 564,611 | SPLIT
19 Dec ends 30th | notes | max test date fold Dec | holds | test max 2025-12-30 | LEAK-22..26
21 history reads earlier days only | claim 21 | min days_since | holds | min 1 day (never 0) | LEAK-10, SPLIT-9
23 92.3% have previous | claim 23 | share | holds | 0.9234 prepared; 0.9245 frame | USE-10
26 areas sum to types, other 3.4% | claim 26 | row sums on frame | holds | 100% rows equal; other 3.32% | CLEAN-19
30 prev result alone ~0.597 | claim 30 | ROC AUC of prev-result fail shares, Dec fold | holds | 0.5967 | TP-10
33 odometer missing 0.23%, 43.9% fail | claim 33 | frame | holds | 0.224%, 0.439 | CLEAN-10
41/44 3 monthly windows, train before window, 1M/500k, no overlap | splits_comment | per fold dates, sizes, intersection | holds | train 2024-07-01..day before window; 1,000,000/500,000; overlap 0; Yes tr 0.277 te 0.275-0.284 | SPLIT-1, SPLIT-14
45 LEAK-9 554-671 test rows a window, 90-94% fails | notes | same-vehicle later row in month on the 25% sample, scaled to the 500k draw | holds (order of magnitude) | scaled 525/573/690; fail share 0.907/0.928/0.916 | LEAK-9
37 mileage not km-confounded | notes | share of decreasing mileage vs previous | holds | 0.26% down | CLEAN-21
46 metric fallback ROC AUC, no source metric | metric reason | re-fetched blog, one more web search | holds (MET-1): blog names no metric; search finds only a hobby project (accuracy) and a commercial site (AUC, no number) | MET-1
MET-2 computable per fold | task.json | dummy 0.5 per fold via kit scorer; positives per fold | holds | 0.5 x3; positives 137,709 / 141,786 / 141,919 | MET-2
MET reason text "officers compare each test's chance with the recorded result, so ROC AUC" | dataset.py metric reason | logic check against blog | refuted as reasoning | comparing a tester's recorded results with predicted chances is an expected-vs-observed count, which needs calibrated probabilities; ROC AUC is blind to calibration. The stated reason supports log loss (the builder's issue 1, option B) better than the chosen metric | MET-8, MET-10, MET-11
7 blog quote | notes | WebFetch of the blog | holds | "predictive vehicle failure model", "target testers who repeatedly record results contrary to the prediction" | USE-1
38 fuel words merged with codes | notes | frame counts; claim 38 itself | untested cause | merged; claim 38 reports 16.8% vs 13.0% fail for word vs code hybrids, so the spelling carries signal (likely a recording path or vehicle cohort), which the merge removes; not a leak | CLEAN-12
Unwritten: features known at start | - | days_since min 1; completed_date and own items absent from frame columns | holds | LEAK-10
Unwritten: short-gap re-presentations | - | rows with previous F within 14 days | holds as known history | 13,333 rows, 25.0% fail; known before the test | USE-10
Unwritten: copies across split | builder probe 5 | not rerun (frame lacks ids) | relies on builder (0.0%) | LEAK-16..21

RANKED REFUTED / UNTESTED
1. (P6, Should) The metric reason contradicts itself: it describes a calibration use (predicted chance against recorded result per tester) and then picks ROC AUC. Changes: the curator's issue 1 has more support for log loss. Mildest remedy: either switch to log loss from context (MET-8/MET-11, the blog paragraph as the context), or keep ROC AUC and reword the reason to a ranking use (tests or testers ranked for inspection) without the "compare with recorded result" sentence.
2. (P7, Could) Fuel spelling merge (HYBRID ELECTRIC (CLEAN) with HY) removes a 3.8-point fail-share difference. Mildest remedy: one sentence in the notes saying why the merge is right (same fuel, different recording path), or keep the raw spelling as a level.
3. Untested: cross-split copies (frame has no vehicle/test id); relies on the builder's probe 5 (0.0%).
```

</details>

<details><summary>Column audit: uk_mot_test_results</summary>

```text
Column auditor: uk_mot_test_results_1m (2026-11-09)
Verdict: no column leak, no cleaning problem at the expert state; two low-rank questions.
Prediction point: start of an initial MOT test (vehicle presented, odometer read, MOT record on file).
Checked on the prepared parquet (13.3M sampled task rows): every raw fuel code and test class is in the lookups
(no value silently lost by .map), result codes 0-5 all decoded, colour NOT STATED only 160 rows.

column | meaning | known at prediction? | dtype and cleaning | verdict | rule
initial_fail | F or PRS at the initial test (guide: PRS begins in a fail condition) | target | Yes/No | fine | USE-5
test_date | date of the test | yes (split key) | datetime | fine | SPLIT
test_class | DVSA test class 1-7 | yes | categorical, decoded with number kept; nominal | fine | CLEAN-12
postcode_area | 1-2 letter area of the station, XX merged | yes | categorical; dtype flag ordinal_like is a false reading (letter codes) | fine | CLEAN-1
test_mileage | odometer read at the test | yes (read at start) | float; 0/blank and 999,999 to missing | fine | CLEAN-10
make | vehicle make | yes | categorical, 5 spellings merged, UNCLASSIFIED missing; flag open_end false (free text) | fine | CLEAN-1
model | vehicle model, trim words | yes | string (54,868 values) | fine | CLEAN-13
colour | vehicle colour | yes (see Q2) | categorical, NOT STATED missing | fine/question | CLEAN-10
fuel_type | fuel code | yes | categorical, codes and word spellings decoded to one label | fine | CLEAN-12
cylinder_capacity | engine cc | yes | float; 0, <25, >=30,000 missing | fine | CLEAN-11
first_use_date | first use (age) | yes | datetime; 1971-01-01, <1900, >test missing | fine | CLEAN-10
previous_test_result | result of latest NT before the test date (547 d) | yes, strictly earlier days | categorical (P,F,PRS,ABA,ABR,ABRVE); none -> missing | fine | LEAK-34, USE-10
days_since_previous_test | gap previous NT -> this test | yes, neither end set by this outcome | float, missing if none | fine | LEAK-10
previous_test_mileage | odometer at previous NT | yes | float, same proxies missing | fine | CLEAN-10
previous_retest_result | last RT/appeal after previous NT, before test date | yes | categorical; missing = no previous or no retest (disambiguated by previous_test_result) | fine | LEAK-39
previous_{fail,prs,minor,advisory,dangerous}_items | item counts of previous NT by type | yes | float counts, missing if none | fine | CLEAN-19
previous_{12 areas}_items | item counts by test-tree section | yes | float counts; 'other' 3.4% | fine | CLEAN-19
dropped: test_id, vehicle_id (ids, probes 0.50), completed_date and the test's own items (outcome) | correct | LEAK-10

Fail share by days_since_previous_test: 0.18 (<=0 / none) ... 0.25 (1-10 d), 0.29 (330-400 d), 0.34 (400-547 d):
plausible (late presenters fail more), not an outcome-set span.

Problems, ranked (principles.md):
1. (P4, question, low) LEAK-9 already handled by the builder as a protocol line (0.11-0.13% of test rows); agree, no
   column remedy needed.
2. (P7, question, low) make/model/colour/fuel/cylinder_capacity/first_use_date in the extracts may be the vehicle's
   record at extract time (June 2026) rather than at the test; a colour change or a corrected record after a failed
   test is not driven by this test's outcome in any measurable way. Mildest remedy: one sentence in the notes; no change.
3. (P6) Agree with the builder's issue 1 (metric) as the only curator call; nothing in the columns argues for or against.
```

</details>

<details><summary>Split audit: uk_mot_test_results</summary>

```text
Split auditor report: uk_mot_test_results_1m (2026-11-09)

Verdict: right with notes.

Regime. The use case (DVSA's predictive vehicle failure model, refit monthly, scoring each new MOT test at its start)
is a stream over time with known, recurring vehicles. Declared: Temporal(on=test_date, monthly windows, 3), the
vehicle carried as dated history (previous test within 547 days), vehicle_id dropped. This matches (USE-10, SPLIT-1).
A grouped split by vehicle would be wrong: DVSA holds the vehicle's record when the test starts (cold start is not
the application). No group id is needed.

Measured on the built container (work_split_auditor/frame.pkl, splits.pkl):
  window   train rows  train dates               test rows  test dates               Yes train/test  overlap
  Dec 25   1,000,000   2024-07-01..2025-11-30    500,000    2025-12-01..2025-12-30   0.277/0.275     0
  Nov 25   1,000,000   2024-07-01..2025-10-31    500,000    2025-11-01..2025-11-30   0.277/0.284     0
  Oct 25   1,000,000   2024-07-01..2025-09-30    500,000    2025-10-01..2025-10-31   0.276/0.284     0
Train months per side: 15 to 17 months, every month 43k-78k rows (lowest Dec 2024), so every season is in training;
the train sample is random over the span, not the latest tests (a deliberate choice, version_comment).

Time column: test_date is the date the test was carried out, the prediction point is the start of the test. Label
delay: result recorded the same day (completed_date = test date on 100% of task rows, builder); no training row's
label is unknown at the window start, so no gap is needed (SPLIT-9/10). History reads only tests dated before the
row's date, so the train side's histories do not reach into the window.

Test window: three autumn/winter months (Oct-Dec). MOT failure rates move a little by season (0.275-0.284 here
against 0.277 in training); the windows are one season, but the train side covers all seasons, and a monthly refit
evaluated on the last three months is what the application does. Note only.

Problems, ranked by principles.md:
1. P4, LEAK-9 (note; already a protocol line): a vehicle tested twice in one window gives the earlier test's result
   away through the later row's previous-test fields: 554-671 test rows a window (0.11%-0.13%), 90-94% fails. Remedy
   as written: "test rows predicted without the other test rows" (BENCHMARK_CHANGES_TODO). Agree; no re-split.
2. P4, mild: the December window ends on 30 Dec (source extract lacks the 31st). Window is 30 days, not censoring
   (Yes rate in band). Remedy: none, the note in curation_comments is enough.
3. P4, note: training is a random 1M over 15-17 months rather than the latest months; a monthly refit could use the
   most recent data. With the history built from the full record (not from the sample) this costs nothing in
   validity; no remedy.

Hidden groups / near copies: the only entity is the vehicle (dropped; its past is a feature by design); near copies
0.9% (hidden-group probe), exact copies across the split 0.0%; 266 same-day same-vehicle pairs are distinct tests.
No alternative split was fitted: no doubt about the regime remained after the checks above.

Builder's issue 1 (metric) is outside the split role; no split objection to either option.
```

</details>

<details><summary>Domain practitioner: uk_mot_test_results</summary>

```text
Domain practitioner report: uk_mot_test_results (folder uk_mot_test_results_1m)
Actor: a DVSA enforcement/risk analyst who maintains the "predictive vehicle failure model" feeding the tester risk
ratings (DVSA digital blog, N. Barlow, "Getting smart on MOT fraud", 10 June 2019, as cited in dataset.py; DVSA MOT
testing data user guide v5.1 as cited in the curation notes). No new web sources consulted; I relied on the
definition, README, record and builder report.

FIT: direct (agree with the definition). One row is one initial MOT test scored for its chance of failing, from what
DVSA holds when the vehicle is presented, which is exactly the per-test expectation the risk rating compares with the
tester's recorded result (USE-1, USE-5, USE-10).

1. Inputs at the prediction moment
- Have: test date, class, station area, odometer, make/model/colour/fuel/cc/first-use, previous test result, its
  defects by type and area, the retest outcome. All known at test start (MOT history is on file). Correct to drop the
  test's own items and completed_date (LEAK-10).
- Deliberately absent and rightly so: tester and station identity. For this use the model must estimate the vehicle's
  expected outcome independent of who tests it, otherwise a fraudulent tester's pattern is learnt as "normal" for his
  vehicles and the residual vanishes. The anonymisation thus matches the decision; I would note it explicitly in the
  use case as a strength, not only as a limitation.
- What I would always have and is missing (ranked): (a) history beyond 18 months and more than the last test (DVSA
  holds the full record back to 2005; counts of past fails, advisory recurrences); (b) the previous test's station /
  tester (to detect "shopping" between garages); (c) VIN-level vehicle spec and recalls; (d) the keeper change and
  vehicle tax/SORN state. These lower the ceiling but do not change the task (fit stays direct, USE-5 approximate
  inputs are acceptable).

2. Target: the recorded result F or PRS at the initial test, as DVSA's initial failure rate counts it (USE-5). It is
  the label I act on. Known caveat, accepted: it is the tester's recording, which is the very thing audited; a small
  fraction of mislabels from fraud is part of the real task. I want a probability, not a class.

3. Unit and test data: one row = one test, the unit of the prediction; the unit I ACT on is the tester/garage over a
  period (sum of predicted vs observed failures). Since testers are anonymised the benchmark cannot score at that unit,
  but per-test probabilities are the building block. Monthly temporal windows (Oct-Dec 2025) with training on the
  preceding months match a monthly refit. Same-month repeated tests: protocol line (LEAK-9) is correct. Minor: the
  random 25% pre-sample means a vehicle's next test is often not in the data, harmless since history is built on all
  tests. The December window lacks the 31st: negligible.

4. Would I use it: yes, as a baseline. Trust: temporal splits, history built only from earlier dates, re-derivation
  checked. Distrust drivers: calibration drift across seasons/years (fail rate shifts with MOT rule changes, e.g. May
  2018), and any station-correlated feature (postcode_area) absorbing local tester behaviour; at area level that is
  coarse enough to be acceptable.

5. Metric: PARTLY. ROC AUC (fallback, MET-8 path) scores the ranking of tests, but my decision compares expected
  failure counts per tester with observed counts (observed minus sum of predicted p). That needs calibrated
  probabilities: a model with good AUC but probabilities shifted by 3 points flags every tester the same way. A
  proper scoring rule on the probabilities (log loss, or Brier) scores this directly (MET-1, MET-8; MET-6/MET-7 do not
  apply as no threshold or cost is fixed; MET-9 not relevant at 27.7% positives). I would choose log loss, with ROC
  AUC as a secondary report. This supports the builder's draft issue 1 in favour of log loss from context.

Gaps ranked by how much they change the task:
 1. Metric ranks instead of scoring calibrated probabilities (moderate; switch to log loss).
 2. Truncated history (18 months, last test only) vs DVSA's full record (lowers ceiling, task unchanged).
 3. Action unit (tester) not reproducible because of anonymisation (inherent; per-test score is the right proxy).
 4. Previous test's station unknown (minor).

What an expert would change: declare log loss (MET-8, MET-1); add a count of fails across all tests within the
history window if cheap (e.g. fails in the last 18 months, not just the last test); state in fit_reason that the
absence of tester/station identity is required by the use case.
```

</details>

<details><summary>Blind review: uk_mot_test_results</summary>

```text
VERDICT: Include with changes. It is a real, large, non-trivial task (DVSA anonymised MOT tests: will this vehicle fail its MOT at first attempt?) with a sensible temporal split, but the time coverage and a few column choices need fixing.

TASK: Predict initial MOT failure from vehicle attributes, mileage and the previous test's outcome. Garages, fleet managers, insurers or DVSA risk-targeting would use it before the test is done. A real use. Base rate 28.1% fail. LightGBM, trained before Dec 2025 and tested on Dec 2025 (sample): AUC 0.694. Single features: age 0.64, previous_fail_items 0.59. There is signal, it is not trivial, and it is big enough.

CONCERNS (most to least serious)
1. Uneven time sampling. In the 200k sample, Oct, Nov and Dec 2025 each have about 40k rows, while Jul 2024 to Sep 2025 have about 4-6k per month. So the test windows are sampled roughly 8x more densely than the training history. The DVSA data is per year, so it looks like 2025 Q4 plus a thin 2024-25 history were spliced together. Train and test distributions differ by design. Fix: sample all months at the same rate, or document the choice.
2. The look-back for the previous test is truncated. days_since_previous_test runs from 1 to 547 (median 364), and 7.5% of rows have no previous test. Older previous tests, and vehicles with gaps, seem to have been dropped by the extraction window. Also, previous tests can be 1 day earlier: that is a same-cycle retest chain, not the prior annual test. Fix: build the history from multiple years of files and define "previous" as the last completed test cycle.
3. test_mileage is recorded at the test itself. That is acceptable if you assume the odometer is read at booking, but it is borderline "known at prediction time". It is the second-strongest feature by gain. Keep it, but say so.
4. Mixed vehicle classes: 94.6% class 4 cars, plus motorcycles (fail rate 8-22%), class 7 goods (34%) and buses. These are different test regimes. Consider restricting to class 4/7, or keep test_class as a feature (it is already there).
5. Preparation: `model` has 6,802 levels and is stored as a string, so it needs category handling. It is the top gain feature and may overfit. Raw dates (test_date, first_use_date) are left as datetimes, so vehicle age must be derived. cylinder_capacity has implausible maxima (29,932 cc). 0.24% of rows have mileage lower than the previous test's mileage (likely clocking or entry errors; acceptable). previous_retest_result is 81% missing by construction. The "Aborted by VE" category has 0 rows.
6. Target definition: "initial_fail" presumably means test_result F or PRS at first attempt. 28% matches typical DVSA first-time fail rates. I did not verify the exact mapping against the user guide.

CHECKED OK: no exact duplicates, none even ignoring the date. No first_use_date after test_date. Values are plausible. The data is real public DVSA data.
COULD NOT CHECK: the full 2.5M rows, the exact split boundaries of the 3 windows, the user-guide target mapping (I did not fetch the sources), and whether the same vehicle appears in both train and test (no vehicle id is exposed; repeated vehicles across windows are likely but harmless under a temporal split).
```

</details>

<details><summary>Task gamer: uk_mot_test_results</summary>

```text
Verdict: barely gameable. One real leak (future rows of the same vehicle reveal the label) adds +0.001 to +0.003 AUC.

Honest baseline: LightGBM (400 trees, 127 leaves), 300k-row subsample of each training set, all features plus age and mileage delta.
  r0f0 0.69166 | r1f0 0.69711 | r2f0 0.69607. Spread with a random column added: +0.0002 to +0.0017.

Exploit 1: vehicle linkage to later rows (work/link.py, work/base.py)
  Join each row to a later row with the same make, model, first_use_date and fuel_type whose previous_test_mileage equals this row's test_mileage and whose days_since_previous_test matches the date gap.
  That later row's previous_test_result is this row's outcome. Across all 2.5M rows this links 38,734 rows, and the label agrees on 38,728 of them (Failed or PRS means fail; Passed means pass, with 6 errors).
  Test rows linked: 657, 1509 and 1586. Exploited AUC 0.69303 | 0.69972 | 0.69874, a gain of +0.0014 to +0.0027.
  The gain is about the size of the noise spread, but the rule is deterministic and right 99.98% of the time.
  A deployed model does not have this: it needs rows dated after the test date, including rows from after the test window that sit in data.parquet.
  Fix: drop from data.parquet the rows dated after the last test window, and drop test rows whose vehicle is retested inside the same window. Or give each row a vehicle-history cut-off.

Nothing found:
  - Row order: the label rate by position within a day is flat (0.277 to 0.281 across deciles).
  - Training label rate by date against the test windows: 0.276 to 0.277 in training, 0.275 to 0.284 in test. No drift to exploit.
  - Columns from after the prediction point: none. The previous_* fields describe the earlier test, which a deployed model knows.

Not run, for lack of time: format and decimal artefacts, a train-against-test classifier, test-set count statistics, a web search for magic features.
I could not check whether the ~1M rows that are in neither train nor test are deliberate.
```

</details>

<details><summary>Precedent check: uk_mot_test_results</summary>

```text
Precedent checker: uk_mot_test_results (folder uk_mot_test_results_1m), 2026-11-09. Scope: the metric (builder issue 1); the other calls are not re-litigated here.

DECISION: metric. Implemented: Metric.fallback("roc_auc"). Builder leans B: log_loss from context.

A (implemented fallback roc_auc): CONSISTENT.
 - MET-8 / MET-11 fallback: the source names no metric, so roc_auc for binary (metrics.md rule table: "No metric anywhere -> the fallback").
 - african_credit_scoring_challenge (2026-10-26, Lennart; MET-4, MET-10): the host asked for "the probability of loan default" and binned the probabilities into risk grades; the decision was still roc_auc, not log loss. That is the closest decided case, and its wording about probabilities is stronger than one blog paragraph.
 - heart_disease (2026-10-21, checked 2026-10-27, Lennart; MET-6/7/8): the source itself scored calibration (Detrano 1989 reliability) and the fallback roc_auc was still kept. A stronger calibration signal than uk_mot's, decided for the fallback.
 - The same batch: fmcsa_roadside_inspection_out_of_service_1m, sivep_gripe_sari_outcome, nyc_motor_vehicle_collisions, nchs_linked_birth_infant_death_1m all ship Metric.fallback (roc_auc).
 - Wording defect (fix under either option): the reason ends with "Officers compare each test's chance of failure with the recorded result, so ROC AUC on the probabilities (MET-8)". That premise argues for calibration, not ranking. Under A it should say what the ranking serves (which tests and testers run against the prediction) and that no unique metric is given.

B (log_loss from context): DEPARTS, and no distinguishing fact has been shown yet.
 - Every binary log_loss in the working copy comes from the source: bioresponse (Kaggle), numerai28_6 (the 2016 rules) and digicow (Zindi rubric, MET-4). None comes from context.
 - Origin "context" has three uses: diamonds (2026-10-21, rmsle, the definition case) and two Lennart exceptions of one kind, protein_model_quality_rf_pcp and huesken_sirna_efficacy (2026-11-04, mean_group_pearsonr, each backed by a measured failure of the fallback). Neither kind is "binary probabilities over roc_auc".
 - MET-11 allows context only "when the context is clear". The evidence here is one 2019 blog paragraph that names no criterion.
 - MET-2 (Must): the use case the auditor and practitioner cite compares, for each tester, the sum of the chances with the failures recorded. That is calibration-in-the-large per tester. Testers and stations are anonymised and no tester column ships (README l.83), so that unit of evaluation is not in our data. Per-row log loss is a proxy, not the use case's metric, so the context is not clean.
 - Mapping B to the precedents: african_credit says a stated probability use does not by itself move a binary task off roc_auc. heart_disease says even a source that scores calibration stays on the fallback.
 - Drift and amendment: sivep, nyc and nchs raise the same question. Taking B on 2 or more of these four makes it a repeated exception of one kind. At that point MET-8/MET-11 should be amended (for example: "binary: log_loss when the use case acts on calibrated probabilities") and african_credit and heart_disease re-checked, not decided case by case. Under memory per-dataset-choices-not-crosscut, the choice stays a separate issue in each REVIEW.md, but the curator should rule on it once.

Draft issue for the curator (review-file shape):

Should uk_mot_test_results be scored by log loss from context instead of the fallback ROC AUC, given that DVSA compares predicted failure chances with testers' recorded results?

**Problem:**
- The source names no metric. The fallback roc_auc is implemented. The builder, the claim auditor and the domain practitioner lean to log_loss because officers set the expected failures (a sum of chances) against the recorded ones.
- No binary dataset has log_loss from context. african_credit_scoring_challenge (2026-10-26) kept roc_auc although the host asked for default probabilities, and heart_disease (2026-10-27) kept roc_auc although the source scored calibration.
- The comparison the use case makes is per tester, and no tester column ships (MET-2). Per-row log loss is a proxy for it.
- sivep_gripe_sari_outcome, nyc_motor_vehicle_collisions and nchs_linked_birth_infant_death raise the same question in this batch.

| Option | Pro | Con |
|---|---|---|
| (a) log_loss from context. Set apart by: the stated use sums the chances into an expected count per tester, so it needs calibrated probabilities, not only an order | <br>- matches the blog's comparison of expected and observed failures<br>- rewards calibration (MET-8)<br>- probes resolve it (0.541 vs dummy 0.594) | <br>- first binary context log_loss<br>- the per-tester unit is not shipped (MET-2)<br>- one blog paragraph (MET-11 "clear")<br>- departs from african_credit and heart_disease |
| (b) keep the fallback roc_auc, and fix the reason to say why ranking serves the use | <br>- follows MET-8/MET-11, african_credit, heart_disease<br>- the same as fmcsa, sivep, nyc and nchs in this batch<br>- resolves families (+0.032 vs RF) | <br>- blind to calibration, which the use case reads |
| (c) amend MET-8/MET-11 so that a binary use acting on calibrated probabilities takes log_loss, then apply it to uk_mot, sivep, nyc and nchs together and re-check african_credit and heart_disease | <br>- decides the repeated question once<br>- no silent drift | <br>- a rule change, larger than this dataset<br>- may reopen two settled cases |

Recommendation: (b) for this dataset now, because it is consistent with every decided binary case. Take (c) if the curator wants calibration scored: the reason applies equally to the three sibling datasets, so it is a rule change, not an exception for this one dataset.

[^1]: MET-2, MET-8, MET-10, MET-11; Cases: african_credit_scoring_challenge, heart_disease, diamonds, protein_model_quality_rf_pcp, huesken_sirna_efficacy.
```

</details>

<details><summary>Advocate: uk_mot_test_results</summary>

```text
ADVOCATE OPENING BRIEF: uk_mot_test_results (folder uk_mot_test_results_1m), 2026-11-09
Position: ship as defined, with the metric reason reworded, three notes sentences, and a broader protocol line. None of these needs a curator decision except the metric, which is a weighing call where A (fallback) is already implemented and consistent.

1. Validity holds on every Must rule tested (P1-P4 outrank everything below).
   Evidence: claim auditor reports no validity claim refuted (rows, Yes rate 0.277, windows, history only from earlier days: min gap 1 day, 300/300 re-derivation). Column auditor: all 31 columns known at the start of the test, own items and completed_date dropped (LEAK-10). Split auditor: "right with notes", no re-split, train overlap 0, every season in training. Rules: SEL-1, USE-5, LEAK-10, SPLIT-1/9/14 (Must).
   Outranks: every open point is P6/P7 or a P4 note with a protocol remedy; independent failures are not conflicts.

2. The use case is real and the fit is direct.
   Evidence: DVSA blog (Barlow 2019) quoted verbatim, "predictive vehicle failure model" used to "target testers who repeatedly record results contrary to the prediction"; domain practitioner: FIT direct, "would use it as a baseline"; the missing tester id is what the use case requires (a strength to state in fit_reason). Rules: USE-1, USE-8 (Must).
   Answers the "label recorded by the audited tester" risk: the practitioner calls it part of the real task.

3. Worth benchmarking: signal, headroom, and family separation.
   Evidence: LightGBM 0.706 vs single feature 0.642 vs naive previous result 0.597; LightGBM - RF +0.032 (paired SE 0.004); 55k+ minority rows per test fold; gamer baseline 0.692-0.697. Rules: TP-1..TP-10.

4. The only leak is tiny and already handled by the remedy ladder's mildest rung (a protocol line, not a re-split).
   Evidence: LEAK-9 554-671 test rows a window (0.11-0.13%); gamer's linkage exploit +0.0014 to +0.0027 AUC, inside noise spread (+0.0002 to +0.0017). Concede the gamer's extra fact: his linkage also uses rows dated after the window (1,509/1,586 linked test rows in the Oct/Nov folds vs 554-671 within window). Mildest fix: word the protocol line as "each test window predicted without the other test rows and without rows dated after the window", the standard temporal protocol. Rules: LEAK-9 (protocol line), remedy ladder. Outranks the gamer's "drop rows" fix, which is a stronger remedy than needed.

5. Metric: keep the implemented fallback ROC AUC now; fix the reason text (no decision needed for the text).
   Concede: the reason sentence "officers compare each test's chance with the recorded result, so ROC AUC" argues for calibration and is wrong as written (claim auditor P6). Fix: reword to a ranking use (which tests and testers run against the prediction) and say no metric is given.
   Defend A: precedent checker finds A consistent with MET-8/MET-11 and with african_credit (2026-10-26) and heart_disease (2026-10-27), both stronger calibration signals that stayed on roc_auc; the per-tester comparison is not computable without a tester column (MET-2 Must), so log loss per row is only a proxy; one blog paragraph is thin for MET-11 "clear context". If the curator wants calibration scored, it is option (c), a MET-8/MET-11 amendment across uk_mot/sivep/nyc/nchs, not an exception here. The dataset ships under either option.

6. Sampling and history choices are documented design, not defects.
   Concede (blind reviewer): test months are ~8x denser than train months in the sample, and history stops at 547 days. Evidence they are deliberate: 1M/500k row budget keeping test windows whole (as chicago_taxi; version_comment); 98.4% of previous tests fall within 547 days; Yes rate train 0.277 vs test 0.275-0.284, no drift. Mildest fix: one notes sentence on the density; history already noted. Rules: SPLIT-14, USE-5 (approximate inputs acceptable).

7. Remaining P7 items need a sentence, not a change.
   - test_mileage read at the start of the test (blind): odometer reading is part of presenting the vehicle (column auditor: known at start). Note it.
   - vehicle record possibly as of the June 2026 extract (column auditor Q2): one notes sentence.
   - HYBRID ELECTRIC (CLEAN) merged with HY loses a 3.8-pt difference (claim auditor P7): one sentence saying why, or keep it as its own level; either is fine.
   - mixed vehicle classes and model with many levels: test_class is a feature and high cardinality is part of the task (CLEAN-13); no change.
   Rule: CLEAN-1/10/12/13 (P7, lowest rank); none blocks shipping.
```

</details>

<details><summary>Critic: uk_mot_test_results</summary>

```text
CRITIC, opening brief: uk_mot_test_results_1m (2026-11-09)
Position: ship only after changes. Nothing found is a Must that cannot be fixed. Points 1 and 2 have to change before shipping; points 3 to 6 are notes.

1. (P4, LEAK-9) The protocol line covers less than the leak the panel measured.
   Problem: the builder counts 554-671 leaking test rows a window, all from same-window later rows. The task gamer
   linked 657 / 1,509 / 1,586 test rows (the Dec, Nov and Oct folds). The Nov and Oct windows leak more because the shipped frame also holds
   the later windows' rows (about 1M rows in neither train nor test for a fold), and their previous_* fields give away
   the earlier window's labels (38,728 of 38,734 linked labels right). Gain +0.0014 to +0.0027 AUC (task_gamer.report).
   Effect: small, but deterministic, and it grows for the earlier folds, so the line as written leaves the Oct/Nov folds open.
   Remedy (mildest): reword the protocol line and the BENCHMARK_CHANGES_TODO entry to "a fold uses only its own train
   rows; test rows are predicted without any other test row or later-dated row". Re-count with the gamer's linkage and
   state the larger numbers in the notes. No re-split.

2. (P6, MET-8/MET-11, Should) The metric reason argues against the metric it picks.
   Evidence: the reason ends "officers compare each test's chance with the recorded result, so ROC AUC". The claim auditor
   rejects this reasoning, and the domain practitioner says the metric fits only PARTLY (expected minus observed failures per tester needs calibration).
   Precedent checker: the roc_auc fallback is consistent (african_credit, heart_disease), and log_loss from context
   would be the first such binary case.
   Remedy: at minimum rewrite the reason as a ranking use (which tests and testers run against the prediction, no
   source metric). I do not push for log_loss on this dataset alone. The curator should rule once for sivep, nyc, nchs
   and uk_mot together (MET-8/MET-11 amendment), as the precedent checker's option (c) proposes.

3. (P4/P7, note) Test months are sampled about 8x more densely than training months (blind reviewer: ~40k against 4-6k a
   month in a 200k sample; 1M train over 15-17 months against 500k a test month). Not a leak (the Yes rate is in band, probe 13),
   but the README should say the training set is a random draw over the span, not the full months.
   Remedy: one sentence in the notes.

4. (P7, CLEAN-12, Could) The fuel merge of HYBRID ELECTRIC (CLEAN) into HY removes a 16.8% against 13.0% fail-share
   difference (claim 38). Remedy: one sentence on why the merge is right, or keep the spelling as its own level.

5. (P7, note) make, model, colour, fuel, cc and first_use may be the vehicle record as of the June 2026 extract, not as at
   the test (column auditor). Remedy: one sentence in the notes.

6. (P3, USE-1, note) fit_reason should say that the missing tester and station identity is required by the use case
   (domain practitioner), and that test_mileage is read at the test, at its start (blind reviewer concern 3).

Dropped: history truncation (547 d covers 98.4% of previous tests; history spans 2023 onward); mixed vehicle classes
(test_class is a feature); Dec ends 30th (no censoring).
```

</details>
