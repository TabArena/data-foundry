# medical_facility_operational_data

**Outcome:** added. The review panel recommends shipping after changes; the changes that need no decision are made
in `dataset.py`. Validity: USE-5 holds (F1-F3 only, one meaning of `Wait`); LEAK-1, LEAK-34 and LEAK-37 hold for
every row's own values; LEAK-10 is triggered by the schedule fields, which reflect the final schedule, kept with a
note at +0.08 to +0.16 minutes of MAE (issue 11); LEAK-9 is triggered (later test rows reveal earlier patients'
targets, MAE 15.57 to 8.70) and handled by a protocol line in the notes and the split comment (issue 7); the
expected-delay table kept under LEAK-38 is worth 0.01-0.02 minutes (issue 9); SPLIT-3, SPLIT-9 and SPLIT-14 hold, and
the 42-53-day windows depart from SPLIT-12/19 at no measured cost (issue 8). USE-6 and USE-8 were triggered by a task
summary that claimed this patient's appointment as an input; the summary now names the gaps, and whether to add the
patient's own offset is issue 6. The licence is CC0 1.0 from the Dataverse deposit. Value: LightGBM MAE 15.28 against
21.54 for the training median; MET-2/3/4/5 hold; the MET-11 wording is fixed. Quality: the empty-set zeros
(CLEAN-10) are noted (issue 10). Weighed: the source's patient-agnostic framing against the front desk's quote to
this patient (issue 6). For Lennart: issues 6 to 11.

**Main points:** Add this patient's own minutes early as an input (issue 6)? Ship with the rule that each test visit
is predicted on its own (7); keep the schedule fields with a note (11); keep the 42-53-day windows (8); widen LEAK-38
(9); set the empty-set zeros to missing (10).

**Record judgment:** valid. The record's 2026-10-28 "ship this" and the assessments around it describe the earlier
four-facility scope (130,431 visits, 88 predictors), which Lennart's 2026-11-04 decision replaced with F1-F3; the
"full panel" and "90 saved-model replays" of 2026-10-26/28 left no artefacts that this pass could find. Both read as
history.

**Issues for Lennart:**

6. **Add this patient's own minutes early as an input?**

   * **Problem:**
     - The target is this patient's exam-start delay against the appointment, but the definition drops the scheduled
       and arrival timestamps and with them their difference: how many minutes before or after the appointment this
       patient arrived.
     - The front desk knows it at check-in, and it is a real number of minutes because the anonymisation is one clock
       shift for all rows.
     - Should it be derived and added as an input, which the source's features do not have?
   * **Effect on the task:** Without it, a model estimates the facility's current delay for "the next patient, whoever
     it will be" (Crowley et al. 2020) and is scored on each patient's own outcome; a patient who arrives late (27.2%
     at F1) starts late partly for that reason.
   * **Background:** The definition has B, the source's patient-agnostic feature set: `known` and `fit_reason` now say
     that this patient's offset and exam type are not inputs; the fit stays approximate. `question` still asks about
     this patient's exam, which is what the target measures. B is implemented because A adds a feature the source
     does not have, which this pass does not do without you. A derives the offset on the ground "restores meaning the
     source destroyed"[^clean19]: the anonymisation kept the difference and removed only the absolute times. It departs
     from the source's 84 features, whose page says the timestamps are "only for sorting". The fit stays approximate
     either way, because the current patient's exam type, contrast and inpatient status are lost in the source's
     aggregation[^use8] (the advocate's point, upheld by the mediator).
   * **Experiments:** The offset correlates -0.605 with `Wait` (0.56 to 0.78 in size by facility), and since every
     exam starts after arrival, it bounds `Wait` from below. Adding it to LightGBM lowers MAE from 15.275 to 13.577
     (-11%) in all 9 windows (claim auditor; the column auditor and the domain practitioner measured -7% to -11% on 3
     windows). It is known at arrival and is no leak. The task gamer decodes it from later test rows
     (`SumHowEarlyWaiting`), worth 15.57 to 14.75, so leaving it out rewards that decode wherever the evaluator allows
     it (issue 7).
   * **Weighed:** the source's framing and its sorting-only timestamps against the actor's quote to this patient
     (-1.70 minutes of MAE). Dropping an input known at the prediction point changes the task into "predict without
     it"[^use6]; the fit is now stated by the reworded summary[^use8].
   * **Panel:** The critic adds that B meets the factor "a use case rephrased only to excuse a gap"[^use9]; the
     mediator leans to A.
   * **Consistency:** Precedents on both sides: 2_month_survival_rate_prediction (Lennart, 2026-10-26) leaves the
     physicians' known estimates out because the source's task is set beside them, which supports B;
     brazilian_ecommerce keeps the delivery date the company promised at checkout, which supports A. No precedent
     derives an offset from anonymised timestamps.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Add `minutes_early` | input: scheduled minus arrival | known at check-in; -11% MAE | not in the source |
     | B | Source's features (implemented) | patient-agnostic inputs | follows the source | drops a known input |

   * **Recommendation:** A, the mediator's lean: the offset is a difference within one row, not a date.
     **Decision:** (A) add `minutes_early`, or (B) keep the source's features as implemented?

   **Notes for the AI:** on A, derive `minutes_early` (scheduled minus arrival) in `_clean`, under CLEAN-19's ground
   "restores meaning the source destroyed"; the fit stays approximate either way (USE-8).

   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input; dropping it changes the
     task into "predict without it".
   [^use8]: **USE-8** (Must): write how closely the data mirrors the use case, its fit; now met by the reworded
     summary.
   [^use9]: **USE-9** (Should): before settling on approximate, ask whether the data mirrors another use case; weigh it
     against the factor "a use case rephrased only to excuse a gap".
   [^clean19]: **CLEAN-19** (Should): we build a feature when one of its grounds holds, here "restores meaning the
     source destroyed".

7. **Does the evaluator predict each test visit on its own?**

   * **Problem:**
     - Every queue field is history at its own row's arrival, but a later row carries an earlier row's target: with
       one exam in progress, `SumDelayInProgress` equals that patient's `Wait` (14,150 of 14,150 rows), and
       `SumWaits`, `LineCount0` and `SumHowEarlyWaiting` rebuild the line.
     - A deployed model never has those later rows, so a method that uses the test block would score far better than
       it works.
     - The collection's evaluator today (`examples/benchmark_on_beyond_arena.py`) fits on the training rows and
       predicts the whole test block in one call, so a model with a test-time step over the block is not stopped by
       the code, only by the protocol line.
   * **Experiments:** A participant who reads the later test rows of a window rebuilds earlier targets and lowers MAE
     from 15.57 to 8.70 (-44%, all 9 splits); features of the next arrivals alone give 13.64.
   * **Background:** The columns stay, with a `Potential leak, kept on purpose:` note and a protocol line in the notes
     and `splits_comment`: "Each test visit is predicted from the training rows and its own features only; no feature
     or model step may use other test rows." Dropping the sum columns would remove honest signal, and the counts would
     still leak through the next arrivals' features. An evaluation leak is fixed in the scoring, not the
     data[^leak9].
   * **Panel:** The critic holds that the stricter leak rule applies if the evaluator cannot guarantee independent
     predictions[^leak5]; the mediator ruled it an evaluation leak, because each stored value is entity history at its
     own arrival[^leak34].
   * **Consistency:** sepsis_prediction_1m and 5g_energy_consumption ship the same kind of constraint as text, while
     the rule's case table says sepsis "needs a scorer change"[^leak9]. The cross-dataset item on a collection-wide
     per-row (snapshot) scorer, which would show each test row only the rows that arrived before it, was settled on
     2026-11-04: keep the protocol line as text, no per-row scorer ("we can check if the model cheats").
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Protocol line (implemented) | the rule in the notes | keeps honest signal; as sepsis | text, not code |
     | B | Hold for a per-row scorer | waits for a per-row scorer | code stops the decode | holds the dataset |

   * **Recommendation:** A, ship with the protocol line, as sepsis_prediction_1m and 5g_energy_consumption do.
     **Decision:** ship with the protocol line as text (A), or hold this dataset until the collection scores each test
     row on its own (B)?

   **Notes for the AI:** the note is the LEAK-9 `Potential leak, kept on purpose:` line; the critic's alternative was
   LEAK-5 (Must), the mediator's ruling LEAK-9 under LEAK-34.

   [^leak9]: **LEAK-9** (Should): separate data leaks from evaluation leaks; an evaluation-level leak is fixed in the
     scoring, not in the data. Its case: sepsis_prediction "needs a scorer change, not different data".
   [^leak5]: **LEAK-5** (Must): never argue "not a leak" because models would predict the same; ask whether the
     stored values depend on the test rows.
   [^leak34]: **LEAK-34** (Must; narrows LEAK-10): an entity's own history under a temporal split is legitimate.

11. **Keep the schedule fields that reflect the final schedule?**

   * **Problem:**
     - Nine fields count booked visits from the schedule (`AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount2/4`,
       `NumScheduledNextSlot`, `NumScheduledNextW2`, `SumTimeToCompleteNextSlot`, `SumTimeToCompleteNextW2`) and
       should be the appointment plan the front desk sees at arrival.
     - Instead they match the visits that later took place in 99.9-100% of rows (`IsLast` in 2,166 of 2,166): a
       no-show is missing, and a visit booked after this patient arrived is counted (32.1% of rows have such an add-on
       within the next hour).
     - The benchmark therefore gives a model a cleaner schedule than the front desk has.
   * **Experiments:** Dropping the plan fields raises LightGBM's MAE by 0.08 to 0.16 minutes (2 seeds x 3 windows,
     seven of the nine fields), against seed noise of about 0.07. That is the fields' whole worth, so it is an upper
     bound on what the late part adds. Which rows carry a late add-on cannot be located, so the late part cannot be
     blanked.
   * **Background:** For values read at a later pull, where the late cells cannot be located, the values go when they
     may carry a gain, and stay with a note only when the traced part shows none[^leak10]. That makes this a curator's
     call.
   * **Consistency:** onlinenewspopularity (kept, no gain); distribution_transformers_at_cauca_department `power_kva`
     (dropped, ROC AUC 0.701 against 0.639).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, note (implemented) | nine fields kept, with a note | gain at noise level | a cleaner schedule |
     | B | Drop the nine fields | nine columns fewer | the late part goes | loses mostly honest plan information |

   * **Recommendation:** A, keep. The gain is at the noise level, and the source supplies no booking snapshots.
     **Decision:** keep with the note (A), or drop the nine fields (B)?

   [^leak10]: **LEAK-10** (Must), the clause of 2026-10-26 on values read at a later pull.

8. **Keep the 42-53-day test windows instead of the source's two weeks?**

   * **Problem:**
     - The source's paper (Crowley et al., 2020) trains on six months and tests on "a further consecutive two weeks",
       and aeolus_rebuilt_1m (flight delays, the same kind of operational delay; Lennart, 2026-10-12) uses 14-day
       windows.
     - Ours are nine windows of about 4,523 arrival instants, 42 to 53 days each, declared in steps.
     - Their stated reason, "the visits ship without real dates", is refuted by the clock-shift finding, so it was
       removed from `fit_reason`.
   * **Experiments:** The departure costs nothing measurable. On the same weeks, two-week windows score MAE 14.40
     against 14.42 for the shipped windows, and the MAE by fortnight since the window start is 15.37, 15.06, 15.33 and
     15.47 (no decay). The longer windows keep about 4,550 test visits each and 40,995 in all; `splits_comment` now
     gives these numbers.
   * **Consistency:** A consistency question from the precedent checker: the horizon comes from the source and a
     source's split is followed[^split12][^split19]. The rule of at least three windows holds either way[^split14].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 42-53 days (implemented) | nine windows, ~4,550 visits each | same score; larger tests | not the source's |
     | B | Two-week windows | re-cut in days, like the source and aeolus | follows the source and aeolus | a re-cut |

   * **Recommendation:** A, recorded as an exception with the measured fact (it serves the value principle: larger
     test windows, same score[^p6]). **Decision:** keep the windows as an exception (A), or re-cut to two-week windows
     (B)?

   **Notes for the AI:** on A, record an `Exception to SPLIT-19` with the measured fact (14.40 against 14.42; no decay
   by fortnight), "Serves P6".

   [^split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source (how far ahead the actor
     predicts, the competition's test window, the refit cadence); choose the test windows to match it.
   [^split19]: **SPLIT-19** (Should): when the source defines the split, follow it.
   [^split14]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data.
   [^p6]: **P6**, worth benchmarking: not trivial, not too small, every fold can be scored.

9. **Widen the kept-on-purpose rule to named fields of undocumented timing?**

   * **Problem:**
     - As written, the rule that keeps fields of untestable timing with a note covers anonymised fields in data a
       company released for its own competition[^leak38].
     - Your keep of the expected-delay table (2026-11-04) applies it to named fields of an author release, as
       sendy_logistics_challenge `Distance (KM)` did on the same day, and perth_house_prices `NEAREST_SCH_RANK`
       (2026-10-20) and house_sales kept named fields of unknown timing with the same note.
     - This is the third or later case of the kind, so a rule change is due[^case4].
   * **Experiments:** Evidence for the keep here: the table is not the mean `Wait` of its own rows (median gap 2.7, 4.9
     and 8.8 minutes; correlation 0.44, 0.70 and 0.77 at F1-F3), and dropping it changes MAE by 0.01-0.02 minutes.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Exception for this dataset | the table kept, an exception on file | keeps the table | no rule change |
     | B | Drop the table | a late value, as kick `WheelType` was | no field of unknown timing | none stated |
     | C | As now (implemented) | kept under the rule as written | none stated | the rule does not cover it |
     | D | Widen the rule | named fields of undocumented timing covered | covers the cases of the kind | none stated |

   * **Recommendation:** D. If neither A nor D is taken, the table reopens under the rule on late values[^leak10b].
     **Decision:** A, B or D?

   **Notes for the AI:** on D, amend LEAK-38's scope to "anonymised fields, or named fields whose timing the source
   leaves undocumented and no conditional test can show to be post-outcome". On A, record an exception to LEAK-38 for
   the table. On B, treat the fields under LEAK-10 and drop them, as kick `WheelType` was.

   [^leak38]: **LEAK-38** (Should; narrows LEAK-10): anonymised fields that may be post-outcome, in data a company
     released for its own competition, stay with a `Potential leak, kept on purpose:` note.
   [^case4]: principles.md, "Consistent judgement", case 4: the same reason has produced its third exception.
   [^leak10b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point.

10. **Set the zeros that stand for empty sets to missing?**

   * **Problem:**
     - Several averages read 0 when the set they average is empty: `AvgHowEarlyWaiting` and `AvgWaitByTaskTypeLine`
       in all 13,454 empty-line rows, `AvgDelayForDay` in 5,898 rows before any exam began, and `MostRecent1-5`,
       `Median5` and `AvgWaitLastK1-3Customers` when nothing is completed (`Median5` in 10,040 rows).
     - A delay of 0 is also a valid value, so "nothing completed yet" reads like an on-time history.
     - `AvgAgePeopleWaiting` uses two conventions: 0 at F1, repeated constants at F2 and F3.
   * **Effect on the task:** The flags `NoneInLine` and `NoneCompleted` mark these rows, so a tree model can separate
     them; the effect on scores was not measured.
   * **Background:** Proxy missing values become real missing values when the encoding can be inferred[^clean10]; a
     quality matter, which never excludes a dataset[^p7]. Setting them to missing is a change to feature values, which
     this pass does not make without you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, note (implemented) | values as the source ships them | the flags mark the rows | 0 reads as on time |
     | B | Set to missing | missing where an empty set is marked | cheap and safe (mediator) | changes feature values |

   * **Recommendation:** B, set them to missing, which the mediator calls cheap and safe. **Decision:** set to missing
     (B), or keep with the note (A)?

   **Notes for the AI:** on B, set them to missing where the flags (or no begun exam, for `AvgDelayForDay`) mark an
   empty set.

   [^clean10]: **CLEAN-10** (Should): convert proxy missing values to real missing values when the encoding can be
     inferred from the description and the context.
   [^p7]: **P7**, the expert state: cleaned as an expert would ship it, minimal and documented.


**Review panel:** ship after changes (mediator). Tier full, second pass after Lennart's review of PR #33 on 2026-11-04. Claims: 44 (40 numbered, 4 implied); 31 hold, 7 refuted in whole or in part (wording, the licence, the metric's reference and the patient's offset; fixed in the notes or put to Lennart as issue 6), 6 untested (the 2026-10-26/28 panel and replay claims, and how the estimates were made). Blind review: would include with small changes; its main concern, `arrival_order` as a feature, is answered by CLEAN-3 (known at arrival, +0.08 MAE without it). Task gamer: reading the later test rows of a window rebuilds earlier targets, MAE 15.57 to 8.70 (-44%, all 9 splits), now a LEAK-9 note and protocol line (issue 7). Agreed: ship after changes; F1-F3 only, the temporal split, MAE, the kept expected-delay table, `arrival_order` stays. Disputed: LEAK-9 against LEAK-5 for the test-row decode (settled as LEAK-9; the evaluator guarantee is issue 7), and whether the patient's offset must be added or the summary reworded (USE-6, USE-8, USE-9; issue 6). The mediator's issues 1-4 are issues 6-9 here; the schedule-field keep is issue 11.

<details><summary>Mediator</summary>

**Verdict for `medical_facility_operational_data` (second pass, 2026-11-04): ship after changes**

The advocate and the critic agree on this verdict. Nothing here calls for exclusion.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-5 holds (F1-F3 only, one meaning); USE-6 / USE-8 triggered: the summary claims "this patient" and "the
appointment plan" while the patient's own offset is dropped and fit_reason names wrong gaps; fixed by text either
way, the substance is issue 1. LEAK-1/LEAK-10/LEAK-34/LEAK-37 hold for every row's own values. LEAK-9 triggered
(later test rows decode earlier targets, 15.57 -> 8.70): fixed in the prediction protocol, not the data. LEAK-38
keep (curator, 2026-11-04) holds at 0.01-0.02 MAE; plan fields kept with a note (LEAK-6 narrowing). SPLIT-3, SPLIT-9,
SPLIT-14 hold; SPLIT-12/19 departure (42-53-day windows vs the source's 2 weeks) measured harmless, needs the
curator's exception. PROV: CC0 1.0 found (licence string wrong).
Value: TP no flags; MAE 15.28 vs 21.54 train median; MET-2/3/4/5 hold; MET-11 triggered (reference wording), fixed.
Quality: CLEAN-10 zeros for empty sets, fixed or noted; CLEAN-3 keep `arrival_order`.
Weighed: source framing (patient-agnostic, timestamps "only for sorting") - vs actor's quote to this patient
(+1.70 min MAE) +.
For the curator: issue 1 (offset: add or reframe), issue 2 (evaluator guarantee), issue 3 (window exception),
issue 4 (LEAK-38 amendment).
```

**Settled disputes**

- **The leak through later test rows: LEAK-9 applies, not LEAK-5. The advocate wins on the rule.**
  - LEAK-5 asks whether stored values depend on test rows in a way the deployed setting would not have.
  - Row j carries row i's `Wait` only because i's exam began before j arrived. A deployed system has that value at j's arrival too, so this is entity history (LEAK-34, Must).
  - The leak exists only when row j is used to predict row i. That is evaluation-level, LEAK-9.
  - The critic wins on the wording. The attack works through any later test row, so the protocol line must be broader than sepsis's "a patient's rows".
  - The critic's conditional escalation to LEAK-5 is not a dataset issue. It goes to the curator as issue 2.
- **The patient offset: changing the text is required; adding the column is the curator's call.**
  - The critic is right that doing neither fails USE-8 (Must).
  - The advocate is right that the fit stays approximate either way. The current patient's exam type, contrast and inpatient status are lost in the source's aggregation, and USE-9 bars rephrasing only to excuse a gap.
- **`fit_reason` must name the expected-delay table as kept, not as a gap (USE-8, lines 70-72).** The advocate conceded this in rebuttal, so it is settled.
- **The sentence at `dataset.py` line 77 ("refer to the plan, not to realised outcomes") must go.** It is refuted by the 99.9-100% match with the visits that took place. A widened note next to it would contradict it. Settled for the critic.
- **`arrival_order` stays as an input (CLEAN-3, Should: a time index that carries meaning).** It is known at arrival, and dropping it costs only +0.077 MAE. The blind reviewer cites the source's "sorting only" wording, which triggers no rule. Fix the wording only.
- **"459 shared days" is not wrong, only ambiguous.** I measured it on the raw workbook: 710 days, 694 shared by at least two facilities, 459 shared by all three, 0 `DayOfYear` conflicts. The claim auditor's "refuted" is withdrawn.

**Changes to make now (no decision needed)**

1. **`fit_reason` (USE-8):**
   - Drop "windows count events, not days".
   - Name the expected-delay table and the plan fields as kept, not as gaps.
   - Name the real gaps: the current patient's exam attributes are missing (source aggregation), plus whatever issue 1 decides.
   - The fit stays approximate.
2. **LEAK-9 note and protocol line**, in `curation_comments` and `splits_comment`:
   - Note: `Potential leak, kept on purpose:` with the mechanism. `SumDelayInProgress` equals an earlier patient's `Wait` in 14,150 of 14,150 single-exam rows. Reading later test rows gives 15.57 → 8.70 (−44%, all 9 splits); lead features alone give 13.64.
   - Protocol line: "each test visit is predicted from the training rows and its own features only; no feature or model step may use other test rows."
   - Keep the sum columns: dropping them loses honest signal and the counts still leak.
3. **Plan fields (LEAK-10, kept under the LEAK-6 narrowing).** Replace lines 77 and 79 with one kept-on-purpose note covering `AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount2/4`, `NumScheduledNextSlot/W2` and `SumTimeToCompleteNext*`. It should give:
   - the 99.9-100% match, and `IsLast` 2,166 of 2,166;
   - 32.1% of rows with an add-on in the next hour;
   - the drop cost of +0.08 to +0.16 MAE against seed noise of about 0.07.
4. **Expected-delay table note.** Add the LEAK-27/32 risk (correlation with the mean `Wait` of its rows: 0.44 / 0.70 / 0.77) and name `SumTimeToComplete*` as the same estimator family.
5. **Timestamp wording** (`changes`, line 75): "the raw timestamps are dropped; their arrival rank is the time column and an input."
6. **`splits_comment`:**
   - Give the windows as 42-53 days.
   - Add the measured horizon facts: 2-week windows score 14.40 against 14.42 on the same weeks, and fortnightly MAE since refit is 15.37 / 15.06 / 15.33 / 15.47 (SPLIT-12; the reason itself waits on issue 3).
   - Add the F3 history note: about 8 months and 8,215 visits before window 8 (SPLIT-20).
7. **Licence:** "CC0 1.0 (Harvard Dataverse doi:10.7910/DVN/X4SJWS, Pianykh, 2020-05-24)". Remove the 403 sentence from `download_description` (PROV, EV-2).
8. **`metric.original` (MET-11, Must):** cite `WTModel.m` and Crowley 2020 for the per-facility evaluation, or drop "per facility". The challenge page says "across all four facilities".
9. **Cite USE-5 and rain_in_australia** for leaving out F4, in place of CLEAN-21.
10. **Shared days:** write "all 459 days shared by all three facilities (694 by at least two), 0 conflicts" in the notes and the record.
11. **CLEAN-10 (Should, cheap and safe):**
    - Set these to missing where `NoneInLine` or `NoneCompleted` marks an empty set: `AvgHowEarlyWaiting`, `AvgWaitByTaskTypeLine`, `AvgAgePeopleWaiting` (two fill conventions), `AvgDelayForDay` (0 before any exam began), `MostRecent1-5`, `Median5`, `AvgWaitLastK*`.
    - If not, keep them with a note.
12. **Notes (quality):**
    - `OutpatientWaitingCount` equals `LineCount0` + 1 in 80,886 rows, so it probably counts the arriving patient; same for `MalesWaitingCount`, which is not in Table 1. Pre-arrival, so no leak.
    - Add the Table 1 name mapping as the codebook: 2/4 = 30/60 min, W1-3 = 30/60/120 min, K1-3 = 2/4/8 customers.
13. **Record:**
    - Mark Myunghwan's 2026-10-28 "ship this" (four facilities, 130,431 rows) as superseded by the 2026-11-04 decision.
    - Label the 10-26 and 10-28 "full panel" and "90 replays" lines as runs with no artefacts here, which resolves the clash with "no panel ran".

**Issues for the curator, ranked**

1. **The patient's own minutes early (P3; USE-6 and USE-8 Must; a weighing call).**
   - **Problem:** the target is this patient's delay, but the scheduled − arrival offset is dropped together with the timestamps.
   - **Effect:** r = −0.605 (F3 up to 0.78). MAE 15.275 → 13.577 (−11%, all 9 windows). It is known at arrival and is no leak. Leaving it out also rewards decoding it from test rows (gamer: 15.57 → 14.75).
   - **Critic's evidence:** USE-6's "Why" (dropping a known input changes the task); the front desk has it at check-in; CLEAN-19's restore-meaning ground; the reframe would hit USE-9's "rephrased to excuse a gap" factor.
   - **Advocate's evidence:** Crowley's patient-agnostic design ("the next patient, whoever it will be"); the challenge says the timestamps are "only for sorting".
   - **Decision:**
     - (a) Derive `minutes_early`.
     - (b) Keep the source feature set and reword `question` and `known` to "the next patient, whoever it is".
   - **Lean:** (a). The offset is a within-row difference, not a date. Whether the source's sorting-only intent rules out a derived difference would settle it.
2. **Evaluator guarantee for the LEAK-9 note (P4).**
   - **Problem:** the note states the constraint but does not enforce it. Measured gain from breaking it: −44%.
   - **Advocate's evidence:** sepsis_prediction_1m and 5g_energy_consumption ship the same kind of constraint as text.
   - **Critic's evidence:** LEAK-9's own case says "needs a scorer change".
   - **Decision:** confirm the collection's evaluator predicts test rows from train plus their own row, with no test-time step over the block. Otherwise adopt a collection-wide per-row (snapshot) scorer. This is not a reason to hold this dataset.
3. **Window length (P4; SPLIT-12/19, Should; a consistency question).**
   - **Problem:** 42-53-day windows, against the source's 2 weeks and aeolus_rebuilt_1m's 14 days. The stated reason, "no real dates", is refuted.
   - **Evidence:** both briefs propose option (a), measured harmless (14.40 against 14.42; no decay by fortnight). It also keeps about 4,550 test rows per window and 40,995 tested in all.
   - **Decision:** (a) record an exception with that fact (serves P6); (b) use 2-week day-based windows.
4. **LEAK-38 scope (rule maintenance, consistency case 4).**
   - **Problem:** this is the third or later keep of named fields of undocumented timing (sendy, perth, house_sales). The plan-field note belongs to the same family.
   - **Decision:** amend LEAK-38 (option d), or record exceptions. If neither is accepted, the table and the plan fields reopen under LEAK-10.

**Agreed facts**

- **Target:** `Wait` = start − scheduled, within 0.983 min in every row. F1-F3 schedules sit on a 5-min grid; F4 is start − arrival in 100% of rows.
- **Inputs:** queue, flow and history fields are measured at arrival (99.2-100%; 0 changes in 41,855 arrivals with no completion between). `AvgDelayForDay` is a running mean; the `mintime`/`maxtime` identities hold in 100%. Leak probe: no single carrier (0.583-0.588).
- **Clock:** one shift for F1-F3 (StartTime + 60 min in every row).
- **Split:** smallest train side 41,002 of 82,001; 4-14 pending rows per window, with no outcome selection; 0 cross-split copies. Grouped would be the wrong regime; IID is 2.6% optimistic.
- **Expected-delay table:** dropping it changes MAE by 0.01-0.02. The gamer's "per-code statistic" claim is known and its gain matches the note, so it is not an issue.
- **Gamer's exploits #1-#4:** all map to LEAK-9 and are new; no existing note covers them. No accepted warnings exist.
- **Scores:** per-facility MAE about 8 / 17 / 22. All 9 windows score.
- **End shift:** the probe 13 shift is real drift, not truncation.

**Consistency with precedent**

- **Consistent:** dropping F4 (rain_in_australia), temporal over grouped (Lennart, 2026-10-12), numeric `DayOfWeek`/`Month` (CLEAN-14), MAE (zillow_prize), the history fields (LEAK-34), and the LEAK-9 note (sepsis_prediction_1m, 5g_energy_consumption).
- **Departures, both put to the curator:**
  - The windows depart from aeolus_rebuilt_1m; the distinguishing fact is in issue 3.
  - LEAK-38 is applied to named fields; the amendment is in issue 4.
- **No precedent found** for adding a derived offset from anonymised timestamps (issue 1).

</details>

<details><summary>Claim audit</summary>

**medical_facility_operational_data: claim audit, second pass**

**Focus answer.** `focus.md` asks no question beyond the standard panel. My direct answer: none of the 40 claims or the implied ones breaks a validity Must (P1 to P5). The target, split, metric, the expected-delay table and the queue and history fields all held up when tested. What I refuted is wording, provenance and one weighing call. The definition is ready to build once the notes and the licence are fixed. Lennart decides whether to add the patient's own arrival offset.

The data comes from the definition's processed frame and split plan, rebuilt from the raw workbook. The README's build is stale.

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 4, 10 | Wait = exam start − scheduled time, signed, within 1 min | dataset.py notes | recomputed from the raw timestamps | holds | max \|diff\| 0.983 min; 0 rows over 1 min | USE-5 |
| 11 | F1–F3 is one target meaning; F4 is the wait from arrival | notes, Decision | walk-in signature in F1–F3; F4 identity | holds | every F1–F3 schedule sits on a 5-min grid. Wait equals start − arrival in only 1.0–4.4% of F1–F3 rows, but in 100% of F4 rows | USE-5, CLEAN-21 |
| 6, 23–26 | split numbers, train begun before the window, ties intact | splits_comment | per-window recount | holds | min train 41,002 (floor 41,001). Per-facility train min 24,461 / 8,326 / 8,215; test 702–2,108. All train arrivals and starts precede the window; 0 shared instants; 4–14 pending rows per window are left out | SPLIT-9, SPLIT-14 |
| 27 | a window is six to seven weeks | splits_comment | span of test arrivals | holds, loosely | 42–52 days (6.0–7.4 weeks) | — |
| 15 | one clock shift for all facilities | notes | StartTime vs arrival time of day; DayOfWeek and DayOfYear offsets per day | holds (the count differs) | StartTime + 60 min matches to 0.016 h in every row. DayOfWeek offset is 5 in all 82,000 rows. DayOfYear is −2/−3. **694** shared days with 0 offset conflicts, against the claimed **459** | EV-2 |
| 14, 7 | "the timestamps only order rows and are no inputs" | task_summary.changes, notes | is `arrival_order` a model input? | **refuted (wording)** | `arrival_order`, a dense rank of `x_ArrivalDTTM`, is one of the 87 probed inputs. Dropping it raises LightGBM MAE by 0.08 (15.275 → 15.352, mean of 9 windows). It is known at arrival, so this is not a leak | writing; LEAK-1 |
| 16, 18 | planned demand and IsLast "refer to the plan" | notes | rebuilt from the scheduled times of visits that took place | **partly refuted** | FutFlowCount2/4 equal the scheduled visits in the next 30/60 min that later took place, in 99.9–100% of rows. IsLast equals the day's last such scheduled time in 2,166/2,166 rows. So these fields describe the final schedule: no-shows removed, later add-ons included. 32.1% of rows see an add-on booked within the next hour. Dropping the 7 plan fields costs +0.08 to +0.16 MAE (2 seeds × 3 windows; seed noise about 0.07): a weak effect | LEAK-38 |
| implied (5) | "known at arrival: … the appointment plan"; the inputs carry what the actor knows | task_summary | patient's own scheduled − arrival offset | **refuted (fit/value; no leak)** | The offset is known at arrival and does not depend on the clock shift. It correlates −0.605 with Wait but is dropped with `x_ScheduledDTTM`. Adding it cuts LightGBM MAE 15.275 → 13.577 (−1.70 min, −11%) in all 9 windows. Against adding it: the source page says the timestamps "can be used only for sorting", and none of the source's features holds it | USE-1 fit; CLEAN, Weigh |
| 17 | expected-delay table: 49/215/195 values, fixed, dropping it changes MAE by 0.01–0.02 | notes | distinct counts; first vs second half; ablation | holds | 49/215/195. Most values recur in both halves (36/43, 172/200, 120/138). Group means of Wait do not track the values (F1 corr 0.26/−0.17), so no sign of target encoding. Ablation 15.275 → 15.260 (−0.015) | LEAK-38, LEAK-27 |
| 19 | mintime/maxtime are elapsed times of active exams | notes | identities by InProgressSize | holds | 100% for 0, 1 and 2 exams in progress | LEAK-1 |
| 20 | history fields change only with a completed exam | notes | consecutive arrivals with no completion in between | holds | 41,855 such transitions; 0 changes in 9 fields | LEAK-1 |
| implied | `AvgDelayForDay` is known at arrival (codebook: "for that day") | Contents sheet | running mean vs whole-day mean | holds | it equals the running mean of Wait over exams begun before arrival (corr 1.000, 100% within 1 min); whole-day mean corr 0.59 | LEAK-1 |
| implied | the queue and flow fields are measured at arrival | codebook | rebuilt from the timestamps | holds | LineCount0–4, FlowCount2/4 and SchFlowCount2/4 match the at-arrival or before-arrival definitions in 99.2–100% of rows | LEAK-1 |
| 29 | 6 duplicates; 0 cross-split copies | check | hashes | holds | 12 rows (6 pairs); 0 test rows with a feature copy in train, in all 9 windows | SPLIT |
| 12, 13, 22 | neutral facility labels; dtypes; negatives and missing values kept | notes | codebook (Contents sheet) and value counts | holds | Codebook: DayOfWeek/Month/DayOfYear are "the day the exam is scheduled", known at arrival. 1 missing calendar row | CLEAN-14 |
| 21 | the author code labels an RMSE "MSE" | notes | read `ComputeModel.m` | holds | `E.MSE = sqrt(mean(Residual.^2))` | — |
| 40 | metric `mae`; original "evaluated separately for source facilities"; reference = challenge page | Metric | opened the reference page, `WTModel.m` and Crowley 2020 | MAE holds; the per-facility attribution is **refuted for this reference** | The page names MAE as the goal ("reducing MAE by more than 70%" against the intercept; "at most 1-2 minutes worse"). It does not say "separately per facility"; it says "across all four facilities". The per-facility evaluation is in `WTModel.m` (one loop and one result table per facility) and in Crowley 2020, which also reports test error as MSE and MAE in Tables 2 and 6 | MET-1, MET-4, MET-11 |
| 40 (MET-2/3) | computable on every fold, same meaning | Metric | dummy prediction through the kit's `metrics.scorer`, per fold | holds | all 9 windows score finite values: random-prediction MAE 30.9–32.8, train-median MAE 20.1–23.1. The target scale is minutes (identity). Pooling the facilities is the declared departure | MET-2, MET-3 |
| licence | "original terms not independently retrieved" | dataset.py `license` | Dataverse API | **refuted** | `doi:10.7910/DVN/X4SJWS` returns license "CC0 1.0", depositor Pianykh, 2020-05-24; the API answers without the 403 | PROV, EV-2 |
| probe 13 | the mild end shift is benign | prep_report | test-window mean Wait by window | holds | a gradual decline from 9.37 (oldest window) to 0.13–2.75 (newest 3) over about 20 weeks. Delays resolve within a day, so this is not right truncation | LEAK-23 |
| 30, 31, 34–36 | "90 saved-model replays and ten-role panel apply" | record, 2026-10-28 | look for the artefacts | **untested** | No run folder in this warehouse. The 2026-11-04 Assessment says "no panel ran for this dataset", which contradicts the record's own 10-26/10-28 lines. Counts in those lines are for the old 130,431-row scope | EV-2 |
| 8, 16 | how the estimates were made | task_summary | codebook | untested (cannot be tested) | the codebook only says "Expected delay of the next scheduled exam" | USE-5 approximate |
| 1–3, 9, 28, 32, 33, 37–39 | record and summary statements | — | checked against the definition | hold or are historical | — | — |

**Refuted and untested, ranked by principle rank, then strength**

1. **Plan fields are the final schedule, not a snapshot (P4, LEAK-38, Should; weak).** FutFlowCount, NumScheduledNext*, SumTimeToCompleteNext* and IsLast are computed from the visits that took place. They carry later add-ons and missing no-shows. The effect is +0.08 to +0.16 MAE, so the fields stay. Mildest remedy: extend the IsLast note into a `Potential leak, kept on purpose:` line that covers all the plan fields, with the 100% match and the 32.1% add-on exposure.
2. **Licence wording (P5, provenance).** The original terms are retrievable: CC0 1.0 on Dataverse. Remedy: set `license` to "CC0 1.0 (Harvard Dataverse doi:10.7910/DVN/X4SJWS, author deposit 2020-05-24)" and drop "not independently retrieved".
3. **The patient's own lateness is left out (P3 fit / P6 value; Weigh, curator's call).** It is −1.70 MAE (−11%), known at arrival, with no leak. The source excludes the timestamps ("only for sorting"), so following the source is defensible. Remedy, mildest first: say in the notes that it is left out on purpose, following the source. The alternative is deriving `minutes_early` (scheduled − arrival) as a feature, which departs from the source.
4. **Metric reference (P6, MET-1/MET-11, Must on the record only).** The per-facility evaluation in `original` is not on the cited page. Remedy: point the reference at `WTModel.m` / Crowley 2020 for "per facility", or reword `original` to "MAE in minutes (challenge goal: MAE reduction against the intercept model)".
5. **"Timestamps are no inputs" (writing).** `arrival_order` is an input. Remedy: reword to "the arrival rank ships as the time column and is an input; the raw timestamps are dropped."
6. **Record consistency (process, untested).** The 10-28 panel and replay claims conflict with the 11-04 "no panel ran". Remedy: label the 10-28 statements as from an external run with no artefacts here, or strike them. Fix "459 shared days" (694 on F1–F3) and "six to seven weeks" (42–52 days).

The current fit "approximate" stands. Nothing here moves the verdict off ship-after-changes.

Sources: [Operational data challenge](https://medicalanalytics.group/operational-data-challenge/), [Crowley et al. 2020, PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0233810), [Dataverse doi:10.7910/DVN/X4SJWS](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/X4SJWS).

</details>

<details><summary>Column audit</summary>

The audit found no leak that must be fixed: every one of the 87 inputs is known at arrival, or is kept on purpose under a curator decision. The largest finding is not a leak but an input the definition removed: the patient's own minutes early, which carries more signal than any column it ships. The rest are small cleaning issues and notes that need widening.

**Focus.md asks nothing beyond the standard panel.** Its open items:
- **No codebook for the dtype probe:** I used Table 1 of Crowley et al. 2020 by hand. Its 84 names cover every shipped column except `MalesWaitingCount`. It finds 0 dtype problems.
- **`ExpectedDelayNextExam` (LEAK-38):** keeping it is fine at its measured weight of 0.01–0.02 min of MAE.
- **Windows count events, not days:** this has no effect on any column.

**Column table**

| Column(s) | Meaning (Table 1) | Known at arrival? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `Wait` (target) | exam begin minus scheduled time, signed minutes | target | int; 484 rows below −120, all from patients who arrived more than 120 min early (begin is after arrival in all rows) | fine | CLEAN-11 |
| `facility` | worksheet F1–F3 | yes | category | fine | CLEAN-14 |
| `arrival_order` | dense rank of arrival, the time key | yes, counts earlier arrivals only | int | fine | CLEAN-3, LEAK-29 n/a |
| `LineCount0`–`4`, `LineCount0Strict` | people in line at arrival and 15/30/45/60 min before; in line and scheduled later | yes | numeric | fine | |
| `FlowCount2/4`, `SchFlowCount2/4` | exams started / scheduled 30 and 60 min before arrival | yes | numeric | fine | |
| `FutFlowCount2/4`, `NumScheduledNextSlot`, `NumScheduledNextW2` | scheduled in the next 30/60 min, next slot, next 60 min | from the plan, built from visits that took place | numeric | question (problem 2) | LEAK-10, LEAK-2 |
| `AheadCount`, `IsFirst`, `IsLast` | patients scheduled earlier that day; first / last scheduled | from the plan, built from visits that took place | count numeric, flags categorical | question (problem 2) | LEAK-10 |
| `NoneInLine`, `NoneInProgress`, `NoneCompleted` | empty-state flags | yes | category; equal `LineCount0==0` in 100% of rows and `InProgressSize==0` in 100%; `NoneCompleted` is close to `NumCompletedToday==0` (99.7%) | fine (derived, not copies) | CLEAN-5 n/a |
| `SumWaits`, `SumHowEarlyWaiting`, `SumDelayWaitingInLine`, `DelayedInLine` | elapsed waits, earliness and lateness of people in line | yes | numeric | fine | |
| `AvgHowEarlyWaiting`, `AvgWaitByTaskTypeLine`, `SumWaitByTaskTypeLine` | averages and sums over the line | yes | 0 for an empty line in all 13,454 rows | cleaning (problem 3) | CLEAN-10 |
| `AvgAgePeopleWaiting` | mean age in line | yes | 0 for an empty line at F1, repeated constants at F2/F3 | cleaning (problem 3) | CLEAN-10, CLEAN-21 |
| `OutpatientWaitingCount`, `MalesWaitingCount` | outpatients and males waiting (`MalesWaitingCount` is not in Table 1) | yes; the count appears to include the arriving patient | numeric | question (problem 4) | USE-6 |
| `Thoracic/Pediatric/Neuro/Abdominal/Vascular/Cardiac/MSKCount`, `WithContrast*` (4 columns) | exam-type and contrast counts | yes | numeric | fine; their sum exceeds `LineCount0` (other population, undocumented) | |
| `InProgressSize`, `SumInProgress`, `SumDelayInProgress` | exams in progress, their elapsed time, their delays | yes | numeric | fine | |
| `mintime`, `maxtime` | elapsed times of active exams (Table 1 says "for the day") | yes | identities hold: 0 with none in progress, min = max = sum with one (100%), min + max = sum with two (100%) | fine | |
| `NumCompletedToday`, `NumCompletedInLastW1-3`, `NumCustomersInLastW1-3`, `NumScannersUsedToday`, `DelayCount`, `DelayCountLastHour`, `NumAddOnsToday`, `NumAddOnsLastW2` | running counts | yes; all rise through the day (1 drop each), `NumAddOnsToday` equals the day's final value in only 20% of rows | numeric | fine | |
| `AvgDelayForDay` | Table 1: "average delay for that day" | yes. It equals the mean `Wait` of the day's exams begun before arrival in 93.0% of rows (median gap 0); the full-day mean matches 10.7% (median gap 3.6 min) | 0 in 5,898 rows before any exam has begun | fine; cleaning (problem 3) | LEAK-10 cleared |
| `MostRecent1-5`, `Median5`, `AvgWaitLastK1-3Customers`, `AvgWaitLastW1-3` | delays of recent completed patients | yes (completed exams, per the record's identities) | 0 when nothing is completed (`MostRecent1` in 9,872, `Median5` in 10,040 of 10,040 rows), although 0 is a valid delay | cleaning (problem 3) | CLEAN-10 |
| `ExpectedDelayNextExam`, `SumDelayWaitingByExamCode` | fixed expected-delay table per exam type | origin undocumented | numeric | potential leak, kept on purpose | LEAK-38, LEAK-32 |
| `SumTimeToCompleteInProgress`, `SumTimeToCompleteNextSlot`, `SumTimeToCompleteNextW2` | expected durations | origin undocumented (same estimator family) | numeric | note should name them (problem 5) | LEAK-38 |
| `BeforeSlot`, `AfterSlot` | time since the last / until the next slot | yes | numeric | fine | |
| `StartTime` | hour of arrival | yes; equals the fictitious arrival time minus 60 min in all 82,001 rows | numeric | fine | |
| `StartTime2-4` | 2nd, 3rd and 4th powers of `StartTime` (exact in 100%) | yes | numeric, redundant source features | fine (not exact copies) | CLEAN-5 n/a |
| `DayOfWeek`, `Month`, `DayOfYear` | calendar of the scheduled day | yes; one constant offset from the fictitious calendar; 1 missing row | numeric cycles | fine | CLEAN-14 |
| dropped: `x_BeginDTTM` | exam start | no | dropped | fine | LEAK-10 |
| dropped: `x_ScheduledDTTM`, `x_ArrivalDTTM` | appointment time, arrival time | yes | dropped as "artificial timestamps" | question (problem 1) | USE-6, CLEAN-3, CLEAN-22 |
| dropped: `AvgWaitForDay` | F4-only column | n/a | dropped | fine | |

**Problems, ranked**

**1. P3 and P7, question for the curator (USE-5, USE-6, CLEAN-3, CLEAN-22): the patient's own appointment offset was dropped.**
- **Why it is legitimate:** minutes early (scheduled minus arrival) is known at arrival, since the appointment comes from the plan and arrival is the prediction point.
- **Signal:**
  - It correlates −0.605 with `Wait`.
  - Its negative is a hard lower bound on `Wait`, because begin is after arrival in all 82,001 rows.
- **Measured effect:** LightGBM (L1) on the shipped windows:

  | Window | Shipped MAE | With minutes early | Change |
  |---|---|---|---|
  | 0 | 14.83 | 13.55 | −8.6% |
  | 4 | 15.14 | 13.66 | −9.8% |
  | 8 | 15.86 | 14.10 | −11.1% |

  Every column kept on purpose moves MAE by 0.01–0.02 min.
- **Steelman for the current definition:** Crowley et al. excluded per-patient predictors on purpose ("predicting expected delay/wait for the next patient, whoever it will be").
- **The conflict:** `task_summary` says "this patient's imaging exam" and lists "the appointment plan" as known, yet the patient's own appointment is not an input. The timestamps are shifted, but their difference is not artificial.
- **Remedy, the curator's choice:**
  - (a) Add `minutes_early` (CLEAN-19, CLEAN-3) and say so.
  - (b) Keep the source's feature set and reword `question`/`known` to the source's "next patient, whoever it is".

  Not a leak.

**2. P4, weak and cannot-verify (LEAK-10 looked-up-after clause, LEAK-2 sibling sweep): the plan fields are built from visits that took place.**
- **The match:**
  - `IsLast` is the last scheduled visit among visits that happened in 2,166 of 2,166 rows.
  - `IsFirst` is the first scheduled in 3,282 of 3,282.
  - `AheadCount` equals the scheduled-time rank in 99.9%.
- **Why it matters:** no-shows, and add-ons booked after a patient's arrival, would make the plan at arrival differ.
- **`IsLast` carries signal:**

  | Facility | Mean `Wait`, `IsLast` = 1 | Mean `Wait`, `IsLast` = 0 |
  |---|---|---|
  | F1 | −7.8 | 4.2 |
  | F3 | −13.9 | 9.0 |

- **Gap in the notes:** the `curation_comments` note covers `IsLast` only.
- **Mildest remedy:** extend the note to `AheadCount`, `IsFirst`, `FutFlowCount2/4`, `NumScheduledNextSlot/W2` and `SumTimeToCompleteNext*` (keep with a note).

**3. P7, cleaning (CLEAN-10 Should; CLEAN-21): zeros stand in for statistics of an empty set.**
- **Empty line:**
  - `AvgHowEarlyWaiting` and `AvgWaitByTaskTypeLine` are 0 in all 13,454 empty-line rows.
  - `AvgAgePeopleWaiting` is 0 for an empty line at F1 (9,776 rows). At F2/F3 it repeats constants instead (37.0586 ×1,952 and 23.4798 ×716 at F2; 94.8172 ×377 at F3), so one column has two fill conventions.
- **Nothing begun yet:** `AvgDelayForDay` is 0 in 5,898 rows.
- **Nothing completed, where 0 is also a valid signed delay:** `MostRecent1` is 0 in 9,872 rows, `Median5` in 10,040 and `AvgWaitLastK1Customers` in 9,834.
- **Mitigation:** the `NoneInLine` and `NoneCompleted` flags mark these rows exactly.
- **Remedy:** cheap and safe: set the value to missing where the flag says the set is empty. Otherwise keep with a note. The note "missing values remain" does not cover these zeros.

**4. P7, question, meaning unknown (LEAK-2 codebook, USE-6): the waiting counts may include the arriving patient.**
- **Evidence:**
  - `OutpatientWaitingCount` equals `LineCount0` + 1 in 80,886 of 82,001 rows.
  - `MalesWaitingCount` exceeds `LineCount0` in 9,376 rows.
- **What that means:** with an empty line, these columns carry the patient's own sex, outpatient status and probably age.
- These are pre-arrival attributes, so this is no leak. But the curation notes should say so, and `MalesWaitingCount` is missing from Table 1.

**5. P4, note completeness (LEAK-38, LEAK-32).**
- **Agreement:** the curator's choice to keep `ExpectedDelayNextExam` and `SumDelayWaitingByExamCode` is reasonable given the measured weight.
- **Where the note falls short:**
  - The real risk is a table fit over all rows (LEAK-27/32), not only timing.
  - The F3 values correlate 0.77 with the mean `Wait` of their rows (from the 2026-11-04 marks run's `estimates_origin.txt`).
  - The note should also name the duration estimates (`SumTimeToComplete*`), which come from the same undocumented estimator family.

**6. Writing (no rule broken).**
- The shipped names hide the window lengths. My mapping from Table 1, an inference rather than a source statement:
  - `2/4` = 30/60 min
  - `W1/W2/W3` = 30/60/120 min
  - `K1/K2/K3` = 2/4/8 customers
- Documenting this mapping in the curation notes, with Table 1 as the codebook, would answer the dtype probe's "no codebook" gap.

**Settled by measurement**
- `AvgDelayForDay` is a running mean of exams already begun, not the full-day mean that Table 1's wording suggests.
- `mintime` and `maxtime` follow the elapsed-time identities.
- The running counts never drop within a day, apart from one row each.
- The calendar and `StartTime` fields are one clock shift of the fictitious timestamps.
- None of the 87 inputs has a dtype problem, and there is no ordinal scale.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The split is temporal, as the use case needs. It mirrors the prediction point (arrival) and filters unmatured labels exactly. Nothing at P4 needs a re-split, a gap or a filter. The three notes below are wording and SPLIT-12/SPLIT-20 departures that the numbers show do not change scores.

**Focus question.** `focus.md` asks nothing beyond the standard panel. The standard question gets a yes. The regime is right (temporal, known facility, SPLIT-1/3/4, USE-10). Train is filtered on exam start, which meets SPLIT-9. All nine windows train on 50% or more of the rows, which meets SPLIT-14. Grouped and IID alternatives were measured and are worse fits to the task.

**Regime against the use case**
- Use case: at arrival, staff estimate the exam-start delay for a recurring entity, the facility. There is no patient id, so there is no cold start. Under USE-10 the history is legitimate and the split is temporal. This matches Lennart's 2026-11-04 call ("a temporal, not a grouped split"). It also matches the source: Crowley et al. train on 6 consecutive months and test the next 2 weeks, and hold out no facility (SPLIT-5/19).
- The cross-facility order is real time, which I re-measured:
  - Fictitious time of day = `StartTime`·60 + 60.2–60.5 min (seconds rounding), in every facility.
  - Weekday offset is the constant 1 in all 82,001 rows bar one (missing `DayOfWeek`).
  - 0 of 710 shifted dates map to two `DayOfYear` values across facilities.
  - So one clock shift holds for F1–F3, and SPLIT-22 is met.
- Grouped alternative, leave-one-facility-out on the oldest window's test period (LightGBM, L1):

  | Held-out facility | LOFO MAE | Temporal MAE | Train-median baseline |
  |---|---|---|---|
  | F1 | 13.61 | 7.4–8.6 | 15.13 |
  | F2 | 19.40 | 15.8–19.7 | 20.40 |
  | F3 | 28.44 | 21.2–24.5 | 32.01 |

  With 3 facilities this would be a domain-shift test (few-groups factor), not the task.

**Temporal checks (numbers)**
- **Time column.** `arrival_order` is a dense rank of the arrival instants over F1–F3, taken after F4 is removed. Data: 0 missing begins, 0 begins before arrival.
- **Windows.** There are 9, newest first.

  | Window | Test rows | Train rows (share) | Dates (shifted) | Days |
  |---|---|---|---|---|
  | 0 (newest) | 4,553 | 77,435 (0.944) | 2025-06-21 to 08-02 | 42.3 |
  | 1–7 | 4,546–4,565 | 45,565–72,888 | between the two | 44.0–48.8, window 4 52.9 (across the year end) |
  | 8 (oldest) | 4,565 | 41,002 (0.500) | 2024-06-09 to 07-27 | 48.1 |

  - Test rows per facility per window: F1 1,908–2,108, F2 702–1,018, F3 1,627–1,794.
  - Train rows per facility, at least: 24,461 F1, 8,326 F2, 8,215 F3.
  - The 9 test sets are disjoint and cover 40,995 rows.
  - Every number in `splits_comment` checks out. "Six to seven weeks" is really 6.0–7.6 weeks.
- **Label delay and gap (SPLIT-9/10).**
  - The label is known when the exam begins: begin minus arrival has median 26 min, 99.9th percentile 3.2 h, max 4.7 h.
  - Train keeps rows with `arrival < lo` and `begin < lo`. In every window the last train begin falls before the test start (e.g. 10:31 against 10:32 for window 0).
  - Rows excluded as pending (arrived but not begun at `lo`) are only 4–14 per window. Their mean `Wait` is −20.5 to +26.4, so this is no selection by outcome.
  - No further gap is needed, under the SPLIT-10 amendment of 2026-11-04.
- **Probe 13 end shift (z −3.0 on the mean).** This is not censoring.
  - Each period is about 2,050 rows, roughly 10 days, against a label delay of 4.7 h or less.
  - The mean `Wait` falls through the whole stream: 13.5, then about 9, then −0.7.
  - The median falls with it (10, 7, 2–3), so this is real drift.
  - Test-window means: 9.37 in the oldest window, 0.13–6.41 in the later ones. Train means: 7.2–9.7.
- **Training history (SPLIT-20).**
  - F1 and F2 start in 2022-10 (shifted). F3 starts in 2023-10, with no gap over 7 days in any facility.
  - The spike in probe 13's periods 18,386–22,466 (mean 16.2) is F3 entering. It is a change of case mix, not a collection break.
- **Season.** Windows 8–0 cover June 2024 to August 2025, every month at least once. The holiday window (4) is 1 of 9, and the newest window is summer. Nothing to widen.

**Alternatives fitted**
LightGBM (objective `l1`, 400 trees, 87 features, `n_jobs`=2), MAE in minutes:

| Split | MAE |
|---|---|
| Shipped, 9 windows | 14.21–16.17, mean **15.275** (train-median baseline 21.54) |
| IID, same 40,995-row test pool, 9 random folds trained on all other rows (future included) | mean **14.883**, a 2.6% optimistic gap |
| Source horizon: 9 expanding 2-week windows over the newest 18 weeks, same begin filter | mean **14.40** |
| Shipped windows 0–2 scored on the same 18 weeks | 14.11–14.89, weighted about 14.42 |
| Staleness inside the shipped windows, by fortnight since refit | 15.37, 15.06, 15.33, 15.47 (no decay) |
| Without `arrival_order` | 15.352, +0.077 (0.5%) |

Per-facility MAE on the shipped split: F1 7.4–8.6, F2 15.8–19.7, F3 21.2–24.5.

**Problems, ranked (principles.md: P4 first, Must before Should)**

1. **P4, SPLIT-12 / SPLIT-19 (Should): the horizon departs from the source.**
   - The source tests a further 2 weeks after training. Our windows are 42–53 days, declared as `horizon=4523 steps` with the reason "not a calendar-based horizon".
   - Measured, the departure is harmless: no error growth across fortnights, and 2-week windows score 14.40 against 14.42 on the same weeks.
   - Mildest remedy: no re-split. Add one sentence to `splits_comment` saying the source tests 2 weeks after 6 months, that the longer windows keep about 4,550 test rows per window, and that error does not grow with time since refit (the four fortnight MAEs). Without that sentence it reads as an unexplained SPLIT-12 departure.

2. **P4 wording / SPLIT-10 note (Should): the time rank is a model input while the summary says the timestamps are not.**
   - `task_summary.changes` says "The timestamps only order the rows and are no inputs". But `arrival_order` is a dense rank of the arrival timestamp and is in `feature_columns` (87 features include it).
   - It is knowable at arrival (a count of past arrival instants), so it is no leak. A tree model holds it at the training maximum on test rows. Dropping it costs only +0.077 MAE.
   - Under CLEAN-3, as with ieee_fraud_detection's `TransactionID`, a row-order index is usually treated as an identifier. Here, though, it is the only time column the framework needs.
   - Mildest remedy: reword the summary, e.g. "The raw timestamps are dropped; their arrival-order rank is the time column and is seen by models".

3. **P4, SPLIT-20 (Should): F3's history is short.**
   - F3 has only about 8 months of history before the oldest window (from 2023-10, 8,215 visits), so windows 8 and 7 (June to September) test F3 months it never trained on.
   - F3 MAE there is 24.46 and 24.39, against 21.2–23.4 later. That difference is too small and confounded to act on.
   - SPLIT-14 is met by the pooled count.
   - Mildest remedy: a note in `splits_comment`. No re-split, since SPLIT-21 forbids choosing the history from a few windows.

Not problems:
- No hidden groups apply: there is no patient id, and the group and hidden-group probes rightly did not run for a temporal task.
- 0% near copies across the split, from the prep probe.
- The equal mean of 9 window MAEs is about the pooled MAE, since test windows differ by at most 19 rows.

The 2026-10-28 "accept this split" in the record was about the four-facility windows. The split shipped now is a re-cut on F1–F3, and the measurements above stand in for that earlier acceptance.

</details>

<details><summary>Domain practitioner</summary>

**medical_facility_operational_data: domain-practitioner review (second pass, 2026-11-04)**

**Focus question.** `focus.md` sets no question beyond the standard panel ("Focus: none"). My direct answer to the standard one: as the imaging operations person, I would use this task. I would make one change before it ships: the patient's own arrival time relative to the appointment is an input the front desk always has, and the dataset drops it.

**Fit: approximate (keep it, but change the reason).** This is the source's own delay task, on the facilities' own records, in real time order. The real gap is not the one `fit_reason` names. The features describe the facility's state for "the next patient, whoever it will be" (Crowley et al. 2020). The row and target, though, are one specific patient, and that patient's lateness is not an input (USE-5, USE-6, USE-8).

**As the actor**

I am MGH-style imaging operations staff. When a scheduled patient checks in, I quote or display the expected delay against the appointment. If it is large, I can reshuffle scanners or staff or warn the patient. Pianykh's group put such numbers on waiting-room displays (RSNA 2014). Their deployed delay-at-arrival model is retrained continuously because it degrades without retraining (Radiology 2020).

1. **Inputs at prediction time.** I do have every shipped feature at arrival: queue counts, scanner state, completed-exam histories, schedule counts for the next slot or hour, time of day, and the fixed per-exam-type expected-delay table. All of these are legitimate under USE-6, and the table is kept as a potential leak on purpose under LEAK-38 with negligible signal. What I always have but the dataset lacks:
   - **This patient's arrival minus scheduled time.** `_clean` / `_make_splits` drop `x_ScheduledDTTM` and `x_ArrivalDTTM` with no derived difference. The source says relative timing was preserved, and the record shows the anonymisation is one clock shift, so the difference is real minutes. I measured it from the raw workbook:
     - Correlation with Wait: F1 0.70, F2 0.56, F3 0.78.
     - Share of patients arriving after their slot: 27.2% at F1, 6.6% at F2, 9.3% at F3. For those patients the delay is at least their lateness.
     - LightGBM (L1 loss, fixed settings), MAE without → with the feature: repeat 0 14.83 → 13.72 (-7.4%), repeat 4 15.14 → 13.80 (-8.8%), repeat 8 15.86 → 14.32 (-9.7%).
     - Caveat: 0.6% of rows sit inside arrival-order ties and may be misaligned, which barely matters.
   - **This patient's exam type, contrast and scanner.** These exist only as counts over the queue, never for the current patient. The source's aggregation removed them, so that loss cannot be repaired.
   - Nothing shipped is unavailable at arrival. The leak probe finds no single carrier (0.583-0.588 vs 0.584).
2. **Target.** Signed start minus scheduled, in minutes. That is the number I quote and act on. I want a point number in minutes, so the median under MAE fits a patient-facing quote. It is not a proxy, except as noted in gap 1.
3. **Row and test data.** One row is one patient arrival, which is one quote: it matches. The test windows are later visits at the same three facilities, which is my deployment: known facilities, new days. No grouped or new-facility claim is needed (USE-10). Each window is about 4,550 visits, roughly 6-7 weeks, with no retraining inside it. A deployed system retrains daily or weekly, so the benchmark is harsher than practice. That is acceptable.
4. **Would I use it?**
   - Shipped-feature LightGBM MAE is 14.8-15.9 min against 20.3-23.0 for the training-median baseline.
   - By facility: F1 about 8 min, F2 about 17, F3 21-24.
   - At F1 the number is good enough for a display. At F3 an error of about 22 minutes is borderline.
   - I trust it because the features are the hospital's own real-time system and the order is the real clock.
   - I distrust it because the expected-delay table has no stated origin, there are no real dates (holidays and staffing changes cannot be checked), and the modality of each facility is unknown. The PLOS counts (15,494 / 36,154 / 30,173) do not match the workbook (42,766 / 15,652 / 23,583).
5. **Metric: yes.** See the metric section below.

**Gaps ranked by how much they change the task**

1. **The patient's own lateness is dropped** (USE-6, USE-5). It is a known-at-arrival input worth 7-10% of MAE (1.1-1.5 min) and is the strongest single relation to the target I found (r up to 0.78). Without it, the shipped task is a "facility delay right now" display model scored against per-patient outcomes. For 27% of F1 patients, the outcome is partly set by their own late arrival. Two remedies:
   - (a) Add `arrival_minus_scheduled` in minutes, a within-row offset and not a timestamp. The fit could then move to direct (USE-9).
   - (b) Keep the source's patient-agnostic feature set as a deliberate choice, name this gap in `fit_reason`, and keep approximate.

   The challenge page says the timestamps are "only for sorting". That rule concerns the dates and does not forbid this offset. Still, adding it departs from the source's feature set, so it is the curator's call.
2. **`fit_reason` names the wrong gaps** (USE-8).
   - "Windows count events, not days": the record proves the order is real time. A window of about 4,523 arrival instants is a real 6-7 weeks. That is a horizon unit, not a gap in the fit.
   - The undocumented estimate table is a potential leak kept on purpose. By USE-8, such a kept leak "does not by itself make a fit approximate".
   - The real gaps: gap 1, and the source's aggregation removing the current patient's exam attributes.
3. **No current-patient exam attributes** (exam code, contrast, inpatient or outpatient). They are lost in the source's aggregation and cannot be repaired. They lower the ceiling but keep the task the same.
4. **Pooled facilities.** Practitioners model each facility separately (Crowley; Curtis 2018). The pooled task with `facility` as a categorical lets a model do the same, so this is a small gap. F3 has about 36% of test visits but the largest errors, so it drives model ranking.
5. **Facility modality unknown, and the cohort is not the PLOS one.** This matters for interpretation, not for the task.
6. **No retraining inside a window, and a mild end shift** (probe 13, z -3.0 on the last 2 periods). This makes the benchmark slightly harsher than deployment, which is acceptable.

**What an expert in the domain would change**
- Add arrival minus scheduled as a feature, or else state its absence in `fit_reason` and `known`.
- Rewrite `fit_reason` around the real gaps: the feature set is the source's patient-agnostic state, and the current patient's exam attributes are missing. Drop "windows count events, not days" as a gap.
- Keep the per-facility MAE in the diagnostics (F1 about 8, F2 about 17, F3 about 22).
- Keep the temporal expanding windows. They mirror the source (six months of training, the next two weeks of test) and deployment.

**Metric**

Per-visit MAE in minutes, as the equal mean of nine window MAEs: **yes, it scores the decision.**
- **MET-1:** the unit is the patient arrival, the unit I quote for, in minutes on the target's own scale (MET-3, with no transform).
- **MET-5 / MET-4:** MAE is a deliberate source choice. The challenge sets an MAE goal (">70% reduction vs intercept") and an MAE tolerance ("at most 1-2 minutes worse"). Crowley's results tables are MAE.
- **MET-6, MET-7:** the source fixes no threshold or asymmetric cost, so none should be invented. An "under-quote is worse" cost would need a source. Falling back to RMSE (MET-8) would let F3's tail dominate even more: 61% of squared error vs 45% of absolute error.
- **Aggregation:** the windows are near-equal in size (4,546-4,565), so the equal window mean equals pooled per-visit MAE to within rounding. Per-visit weighting across facilities is what patients experience. I would pick a model by this metric. The source's "% of intercept MAE per facility" is a useful report, not a better selection metric.

**Sources**
- [Operational data challenge page](https://medicalanalytics.group/operational-data-challenge/): target Wait, MAE goal and tolerance, timestamps for sorting only.
- [Crowley et al. 2020, PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0233810): delay vs wait definitions, prediction "for the next patient, whoever it will be", 6-month train / 2-week test, MAE tables.
- [AuntMinnie on Curtis et al. 2018, JACR](https://www.auntminnie.com/imaging-informatics/artificial-intelligence/article/15618753/machine-learning-helps-predict-exam-wait-times-delays): queue length and recent median exam time as top predictors.
- [RSNA 2014 abstract](https://archive.rsna.org/2014/14014898.html): waiting-room display deployment.
- [Pianykh et al. 2020, Radiology, continuous learning](https://pubs.rsna.org/doi/10.1148/radiol.2020200038): delay-at-arrival model degrades without periodic retraining.

</details>

<details><summary>Blind review</summary>

**Verdict:** I would include this dataset with small changes. It is a real, documented hospital-operations regression task with genuine but not trivial signal, a sensible temporal split and features that look like arrival-time snapshots. The main gaps are that `arrival_order` is left in as a feature, the per-feature timing (arrival or departure) can't be fully checked, and two details should be documented: the target is a delay that can be negative, and the walk-in facility was dropped.

**What the task is.** The data is radiology patient-flow data from Pianykh's group (Massachusetts General Hospital), published through the "Operational AI Challenge" and the PLoS ONE paper by Crowley et al. (2020). At check-in, a facility wants to predict how late a scheduled patient's exam will start, so it can tell the patient and manage the queue. The 85 features are congestion, queue, resource and time descriptors that the paper calls "derivable from a typical Hospital Information System". This is a real and published use. The challenge's own metric is MAE against an intercept-only baseline.

**Concerns, most serious first**

1. **`arrival_order` is still a feature column, and the split is on it.**
   - It is a global rank by anonymised timestamp: 81,484 unique values for 82,001 rows, interleaved across F1, F2 and F3, and monotone with time.
   - The source says the timestamps "can be used for sorting ... and for nothing else". As a feature, it is a pure time index that the test windows always lie beyond.
   - LightGBM gives it 2% of gain. Dropping it changes the temporal MAE only from 14.63 to 14.75.
   - **Change:** treat it only as the split or ordering key and drop it from the features. `DayOfYear`, `Month` and `DayOfWeek` already carry the seasonality.

2. **Leakage cannot be fully ruled out from public text.**
   - The challenge page says "Features are captured at patient arrival and departure". The exact definitions are only in the Excel "Contents" sheet, which I could not get (the Kaggle and Dataverse pages would not render).
   - My checks are all consistent with arrival-time snapshots:
     - Within each facility-day, `NumCompletedToday`, `NumAddOnsToday` and `NumScannersUsedToday` never decrease in arrival order.
     - The next patient's `MostRecent1` or `AvgWaitLastK1Customers` equals the current patient's `Wait` only 1% of the time, so a row's own wait does not leak into its neighbours.
     - Top-gain features are the queue and congestion features the paper names (`AheadCount`, `DelayedInLine`, `SumWaitByTaskTypeLine`, `NumCompletedToday`, `LineCount0Strict`).
     - Temporal R² is 0.59; random-split MAE is 14.06 against 14.63 temporal. There is no suspiciously perfect fit.
   - Some features may still look ahead:
     - `IsLast` (0 or 1, set on the day's final arrival): is "last" known when the patient arrives?
     - `FutFlowCount2/4` ("future flow"): this differs from `SchFlowCount2/4` in 74% of rows, so it may count actual future arrivals rather than scheduled ones.
   - **Change:** pull the Contents sheet. If `FutFlowCount*` or `IsLast` use realised future arrivals, drop them.

3. **The target's meaning and its tails should be documented.**
   - For scheduled facilities, the paper defines delay as the difference between the scheduled exam time and the actual start. "Patients seen early have negative delay values."
   - Overall: median 6, mean 7.0, std 32.3, range −497 to 360 minutes. Per facility:

     | Facility | Std (min) | Min (min) |
     |---|---|---|
     | F1 | 18 | −303 |
     | F2 | 31 | −365 |
     | F3 | 48 | −497 |

   - 484 rows are below −120 minutes and 40 are above 180. The 0.1% and 99.9% quantiles are −255 and 156.
   - Values of −300 to −500 minutes (an exam starting 5–8 hours before its slot) are possible for patients moved up early, but some are probably record errors.
   - Squared-error metrics will be driven by these tails.
   - **Change:** state in `task.md` that `Wait` is a schedule delay, not a wait from arrival. Keep it as is (it is the source's target), but score with MAE or report it next to RMSE.

4. **One of the four source facilities was dropped, and this is not documented.**
   - The source has four facilities: F1–F3 scheduled, and F4 walk-in, whose target is wait from arrival, "always positive". The prepared table has only F1–F3, which is correct because F4's target means something different.
   - Facility sizes do not match the paper's per-facility counts, though the total does (81,821 in the paper against 82,001 here):

     | Facility | Rows here | Rows in paper |
     |---|---|---|
     | F1 | 42,766 | 15,494 |
     | F2 | 15,652 | 36,154 |
     | F3 | 23,583 | 30,173 |

   - Either the challenge release relabels the facilities, or it is a different extract. The challenge says "600 to 1,000 days" per facility; I see about 697, 708 and 460 facility-days.
   - **Change:** document the F4 exclusion and the facility mapping. F3 starts only at `arrival_order` 18,428, so early test windows contain no F3 rows. That is fine, but worth a note.

5. **Signal is present but modest. This is a good benchmark level, not a trivial one.**
   - Split: train on the first 80% in time, test on the last 20%.
   - Baselines: global median MAE 20.8, per-facility median 21.5.
   - LightGBM: MAE 14.6 (L1 objective) and R² 0.59 (L2 objective).
   - Per facility, model against median baseline: F1 7.8 vs 12.5, F2 16.4 vs 19.9, F3 22.1 vs 33.2.
   - That is roughly a 30% MAE reduction. The challenge's ">70%" target is clearly hard to reach, so methods will separate.
   - With 82k rows and 9 windows of about 8k rows each, the test sets are large enough to score.

6. **Minor preparation issues.**
   - Exactly one row (`arrival_order` 2006, F1) has NaN in `DayOfWeek`, `Month` and `DayOfYear`. Impute it from its neighbours or drop it.
   - About 10 integer counts are stored as float64 (e.g. `NeuroCount`, `DelayCount`, `SchFlowCount2`). This is harmless.
   - `DayOfWeek` takes values 2–6 in 99.98% of rows (weekdays); values 1 and 7 occur in only 15 rows. Fine as numeric.
   - `facility` is categorical, which is correct.
   - There are 6 fully duplicated rows and 114 duplicate feature vectors (ignoring `Wait` and `arrival_order`). This is negligible and most likely real coincident arrivals.
   - The StartTime features are near-collinear: `StartTime2`–`StartTime4` correlate 0.96–0.99 with `StartTime`. They look like nonlinear transforms (row 1: 7.27, 52.80, 383.71, 2788.31) and are harmless.
   - **Dates check out:** the time features stay consistent with the global order across 712 day blocks (day-of-week and day-of-year advance together in 99.4% of steps), and arrival times within each facility-day are always monotone. So the anonymisation preserved order as claimed.

**What I could not check**
- The per-feature definitions in the Excel "Contents" sheet, which matter most for confirming `FutFlowCount*`, `IsLast`, `AheadCount` and `SumWaits` are known at arrival.
- The Kaggle and Dataverse file listings and licences: both pages returned empty or 403 to my fetches.
- The full PLoS ONE tables (per-facility MAEs).
- The Nature Machine Intelligence paper (doi 10.1038/s42256-020-0176-3); I did not open it.
- Whether the Kaggle copy is identical to the Dataverse or challenge release, and how the 9 test windows are sized.

Sources:
- [Operational AI Challenge page](https://medicalanalytics.group/operational-data-challenge/)
- [Crowley et al. 2020, PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0233810)
- [AuntMinnie summary of the JACR wait-time study](https://www.auntminnie.com/practice-management/article/15618753/machine-learning-helps-predict-exam-wait-times-delays)
- [Kaggle dataset](https://www.kaggle.com/datasets/weirdolucifer/medical-facility-operational-data) (did not render)
- [Dataverse DOI](https://doi.org/10.7910/DVN/X4SJWS) (did not render)

</details>

<details><summary>Task gamer</summary>

**Verdict:** the task can be gamed badly. Each row's features are queue snapshots taken when later patients arrive, and those snapshots carry earlier patients' target. Rebuilding the queue from the later rows in the same test window cuts MAE from 15.57 to 8.70 (−44%) on all 9 splits.

Baselines on the 9 shipped splits:
- Untuned LightGBM: **15.569** (per split 14.49–16.17).
- Adding a random column moves the mean by ±0.012 at most, so that is the noise level.
- Better honest model, LightGBM with L1 objective, 600 trees, 63 leaves: **15.165**.
- Adding lags of the previous 3 arrivals at the same facility and day (honest, since they are known at arrival): 15.337 with the default model, 15.096 with the L1 model.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Rebuild the queue from later arrivals and decode Wait exactly. Combined with leads and L1, overwritten by the exact decode where it exists | 15.569 (L1: 15.165) | **8.701** | 6.87 mean (6.41–7.51); vs L1 6.46 (6.03–6.86) | No. It uses rows of patients who arrive after the prediction point | Drop or lag the queue-state columns (below), or score each test row using only rows that arrived before it |
| 2 | Queue rebuild only: `SumWaits`/`LineCount0` give line membership, which bounds when each exam began; `SumHowEarlyWaiting` gives each patient's own scheduled-minus-arrival time | 15.569 | 10.000 | 5.57 (5.14–5.88) | No | Same |
| 3 | Lead features: the next 1–3 arrivals at the same facility and day, plus the time to the next arrival | 15.569 | 13.639 | 1.93 (1.73–2.09) | No | Same |
| 4 | Begin-rank decode from `SumDelayInProgress` alone | 15.569 | 15.173 | 0.40 | No | Same |

**Mechanism.**
- **The leaking column.** For facilities F1–F3, `Wait` is exam start minus scheduled time (per the paper). `SumDelayInProgress` at arrival j is the sum of `Wait` over the patients in the scanner at that moment.
  - When `InProgressSize`==1, that value equals an earlier same-day patient's `Wait` in **100%** of the 14,150 cases.
  - In the opening rows: row 3 has 28 = 26 + 2, the `Wait`s of rows 1 and 2. Row 4 has 9, the `Wait` of row 3.
- **Line membership.** `SumWaits_j` = Σ(t_j − t_i) over the patients in line at arrival j, where t is `StartTime` in minutes, and `LineCount0_j` gives the count. A subset-sum over the previous line plus the newest arrival identifies the line at each arrival. It fails at 3,463 of 82,001 arrivals.
- **Each patient's own times.** The rebuilt line gives the interval in which each patient left it, which brackets the true `Wait` in 86% of cases (73% coverage). Peeling `SumHowEarlyWaiting` gives each patient's own scheduled-minus-arrival time.
- **Exact values.** When exactly one patient begins between two arrivals and none finishes, the jump in `SumDelayInProgress` is that patient's `Wait`. This is exact in 94% of cases, covers 12.4% of rows, and has MAE 1.97.
- **Test-window note.** The decode uses later rows of the same day. For a few days per window, those rows sit in the next window. They are in `data.parquet` either way, and the effect is small.

**Mildest fix.** Score each test row using only rows that arrived before it, by shipping per-row prediction-time snapshots rather than a block of test rows. If the block format has to stay, remove the columns that are sums over sets whose membership changes with other patients' exam start:
- `SumDelayInProgress`, `SumWaits`, `SumHowEarlyWaiting`/`AvgHowEarlyWaiting`, `SumDelayWaitingInLine`
- possibly `SumInProgress` and `SumTimeToCompleteInProgress`

Even then, the lead-feature attack (#3) still works through the counts (`LineCount0`, `AheadCount`, `InProgressSize`, `NumCompletedToday`). A per-row history cut is the only full fix.

**A signal the kit lacks (not an exploit).** The patient's own scheduled-minus-arrival time is known at arrival in real use. It is not in `features()`, but it can be decoded from later rows. Adding it alone takes the baseline from 15.569 to 14.748 (gain 0.62–1.04). A fair task would ship it as a feature.

**Flaws that hurt an honest model**
None found.
- **Training on recent rows only:** last 20k rows 15.877, last 30k rows 15.720, both worse than the full-history 15.569.
- **Embargo gap:** 4–14 training rows before each test window are dropped, and which ones depends on the label (the dropped and kept means differ, e.g. split 2: 17.2 vs 5.4). That is the correct embargo for outcomes not yet known, and it is too small to matter.
- **Label drift:** test means (0.1–9.4) sit below train means (7.2–9.7), but that is real drift, not a split artefact.

**Attacks that found nothing**
- **Format flags** (integer share and NaN flags of the float columns, plus `facility`): 21.41 vs 21.64 for `facility` alone. The flags only mirror queue states such as an empty line.
- **Exact copies of test rows in training** (all features except `arrival_order`): 0% on split 0.
- **Later rows repeating a Wait directly:** `MostRecent1`, `AvgWaitLastK1Customers` and `Median5` match an earlier same-day `Wait` less often than chance (14.5% vs 20.0%). They measure start minus arrival, not the target.
- **Cumulative counters** (`NumCompletedToday`, `DelayCount`, `NumAddOnsToday`, `NumScannersUsedToday`): never decrease within a facility-day, so they are measured at arrival and not at departure.
- **`IsLast`/`IsFirst`:** they agree with the actual last or first arrival only 63% and 40% of the time, so they come from the schedule. Legitimate.
- **Train-vs-test classifier:** AUC 0.78 on split 0 without the time columns. That is time drift, mainly exam-code mix (F3 codes change); no exploitable rule.
- **`ExpectedDelayNextExam`:** one constant value per exam code across the whole period (446 values). It looks like a per-code statistic computed over all dates, test windows included. A tree uses it only as a code ID, so the gain cannot be separated from a legitimate exam-code feature. What would decide it is whether the published Contents sheet defines it over the full history.
- **Number of arrivals in the day** (`n_in_day`), added on top of the leads: 13.59 vs 13.64. Negligible.
- **Web search** for a Kaggle leak or magic-feature thread: nothing found. The paper (Crowley et al., PLOS ONE 2020) gives the feature definitions and MAE of about 8.5–23 per facility.
- **Row lookup** in the published source: not tried; the timestamps are anonymised but sortable.

**What I could not check**
- The published Excel Contents sheet with the exact feature definitions: the PMC page returned a captcha to curl, so I read it through the fetch tool only.
- Whether F4 was dropped on purpose.
- A full linear-system decode of all in-progress sums, which should push the exploit well below 8.7.

Sources:
- [Crowley et al., PLOS ONE 2020 (PMC7289434)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7289434/)
- [Operational data challenge](https://medicalanalytics.group/operational-data-challenge/)

</details>

<details><summary>Precedent check</summary>

**Precedent check: medical_facility_operational_data (second pass, 2026-11-04)**

**The focus question.** `focus.md` asks nothing beyond the standard panel. Its one open decision, keeping `ExpectedDelayNextExam` and `SumDelayWaitingByExamCode` under LEAK-38, matches precedent in its outcome. The rule it cites does not cover these fields as written (item 1). The register has 10 decisions for this dataset and no flags; I read every case behind them anyway.

**1. LEAK-38: keep the expected-delay table (Lennart, 2026-11-04). The keep is consistent, the rule cited is out of scope, and a rule change is due.**

- **Facts.** These are named fields, not anonymised ones. The data is the authors' own research and challenge release. The table holds one fixed value per exam type: 49, 215 and 195 values at F1-F3. Earlier checks of the 2026-11-04 marks run found:
  - The table is not the mean `Wait` of its own rows. The median gap is 2.7 / 4.9 / 8.8 min, and the correlations are 0.44 / 0.70 / 0.77. So it is not a target encoding over all rows, and LEAK-27 and LEAK-28 do not apply.
  - Dropping the two fields changes LightGBM's MAE by 0.01-0.02 min.
  - No conditional test shows that the fields are recorded after the outcome.
- **Precedents with the same outcome.** Each kept a named field of unknown timing with a `Potential leak, kept on purpose:` note when its effect was small:
  - sendy_logistics_challenge `Distance (KM)`: Lennart, 2026-11-04, the same day, also citing LEAK-38. RMSE goes from 789.6 to 761.5 s, a larger effect than here.
  - perth_house_prices `NEAREST_SCH_RANK`: a fixed per-school table that postdates the sale. RMSE 0.1623 against 0.1622. Assessment 2026-10-20.
  - house_sales `view`, `waterfront`, `sqft_living15`.
  - african_credit_scoring_challenge, the lender-portion fields.
  - account_debt_south_africa `HasIDNo`.
- **Precedents decided the other way, and what sets them apart.** None has the facts of this case.
  - kick `WheelType` and expresso `REGION` (Lennart, 2026-10-22) were dropped under LEAK-10 because a conditional test measured the mechanism.
  - distribution_transformers `power_kva` (2026-10-21) was dropped because the inventory demonstrably changed and the effect was large (ROC AUC 0.701 against 0.639).
  - chicago_traffic_crashes (Lennart, 2026-11-04): five condition fields were dropped on measured class-dependent recording.
  - None of these is a fixed lookup with zero effect and no measured mechanism.
- **Departure.** As written, LEAK-38 covers only "anonymised fields … in data a company released for its own competition". This case and sendy are its first two uses for named fields. With perth, house_sales and the other kept notes, this is at least the third decision of the same kind (principles.md, consistency case 4). A rule change is due.
- **Not a broken Must.** LEAK-10 needs a field shown to be recorded after the outcome, and nothing shows that here.

> **Consistency check (AI, 2026-11-04):** your call on medical_facility_operational_data (keep `ExpectedDelayNextExam`/`SumDelayWaitingByExamCode`, citing LEAK-38) applies LEAK-38 to named, non-anonymised fields. sendy_logistics_challenge did the same on the same day, and perth_house_prices (2026-10-20) and house_sales kept named fields of unknown timing with the same note and no rule cited. What sets these apart from LEAK-38's anonymised-field scope?
> (a) The facts they share: the source does not document when the field was made, no conditional test shows it was recorded after the outcome, and the measured effect is nil or small (here 0.01-0.02 min MAE; the table is not the mean of its own rows). Possibly also a company's own estimate made before the outcome (USE-6). Recorded as an exception. (b) Treat it under LEAK-10 and drop it, as kick was. (c) Reopen sendy and perth to match whichever way you decide. (d) Amend LEAK-38's scope to "anonymised fields, or named fields whose timing the source leaves undocumented and no conditional test can show to be post-outcome". This is the third or later case, so the amendment is due.

**2. Split windows: 9 expanding windows of about 6-7 weeks. This departs from SPLIT-18/19 and the aeolus precedent, and the stated reason is weakened by the 2026-11-04 finding.**

- The source's protocol (Crowley et al. 2020) trains on six months and tests on "a further consecutive two weeks". The closest operational-delay precedent, aeolus_rebuilt_1m (flight delays; SPLIT-20 and SPLIT-21, Lennart, 2026-10-12), uses `window=14` days.
- Our windows are about 6-7 weeks of the shifted calendar (dry run: test from 2024-06-09, 07-27, 09-14, …). Their horizon is `horizon_unit="steps"`, which only california_house_prices_2020 and mortgage also use.
- The reason given in `fit_reason` and in claims 6, 8 and 27 is "the visits ship without real dates, so the windows count events, not days". The 2026-11-04 assessment establishes that the anonymisation is one shift of the real clock (arrival = StartTime + 60 min in all 130,431 rows; 459 shared days agree). Elapsed days are therefore real, and two-week windows are possible.
- SPLIT-14 (Must) is met either way. Nine two-week windows would leave over 80% of the rows on every train side.
- Training on all history instead of the authors' six months is forced by SPLIT-14's 50% floor, which outranks SPLIT-20 (Should). That part is consistent.
- This was Myunghwan's acceptance (2026-10-28), made before the clock finding. Lennart's 2026-11-04 decision covered only temporal against grouped.

> **Consistency check (AI, 2026-11-04):** the windows of medical_facility_operational_data (about 6-7 weeks, counted in arrival events) differ from the source's two-week test and from aeolus_rebuilt_1m's 14-day windows (2026-10-12, same kind of operational delay). The stated reason, "no real dates", is weakened by the 2026-11-04 finding that the timestamps are one shift of the real clock. What sets it apart?
> (a) A short-lived quantity is not at stake: the inputs describe the current queue, and nine count-based windows over the 50% pool are the SPLIT-15 default. Recorded as a departure from SPLIT-18/19 with that reason, and `fit_reason` updated. (b) Use two-week day-based windows like the source and aeolus. (c) Reopen aeolus. (d) Amend SPLIT-18 to say which quantities count as short-lived.

**3. One meaning of the target: F1-F3 only, F4 left out (Lennart, 2026-11-04). Consistent.**

- It follows rain_in_australia (Lennart, 2026-10-26), which dropped rows whose label is "another quantity" (48 h against 24 h) under USE-5 (Must).
- It also follows the uniqueness tension (PROV-6/7): F4 is a distinct task that would need its own record.
- It reverses Myunghwan's "ship this" of 2026-10-28 (all four facilities). That is a newer curator decision, not drift by one curator.
- Minor: CLEAN-21 is about one unit or scale per feature column, and none of its cases (college_scorecard, force_2020, zillow_prize, rosbank1) concerns a target. USE-5 is the deciding rule, and citing rain_in_australia would be more exact.
- Minor: Lennart's chicago line of the same day says "replaces Myunghwan's exception of 2026-10-29". This record's 2026-11-04 line does not say it supersedes the 2026-10-28 "ship this" and its scope ("all 130,431 rows, 88 predictors").

**4. Temporal, not grouped (Lennart, 2026-11-04). Consistent.**

It follows SPLIT-3 and the "temporal against grouped" tension (Lennart, 2026-10-12). Facility is a known entity that recurs across the cutoff, which SPLIT-13 and USE-10 treat as part of the task, as in ashrae_great_energy_predictor_iii_1m (`test_rows_seen` 100%) and rossmann_store_sales. The smallest train side is 41,002 of 82,001, exactly SPLIT-14's 50% floor.

**5. `DayOfWeek` and `Month` numeric (Lennart, 2026-11-04, CLEAN-14). Consistent.**

It follows the cycle rule of 2026-11-01: weekdays and months shipped as numbers stay numbers, as in rossmann `DayOfWeek`, 5g_energy_consumption, miami_housing `month_sold` and 11 more. The five 0/1 flags are categorical, as in the 2026-10-21 flag sweep. Counts are numeric, as in bank_marketing and qsar_biodeg (2026-10-30). The dtype probe flagged nothing (`dtype/flagged.csv` is empty).

**6. Metric: `Metric.source("mae")`, per-visit MAE pooled over F1-F3. Consistent.**

- It follows zillow_prize (MAE kept) under MET-4/5. MAE is the deliberate criterion of the author challenge and of Crowley Table 2.
- The per-group metric precedents differ in mechanism:
  - numerai's per-era CORR follows a competition's own per-group aggregation.
  - protein_model_quality_rf_pcp and huesken_sirna_efficacy (Lennart, 2026-11-04, exceptions) score within groups because the use case ranks inside a group and a pooled metric rewards knowing a group's mean.
  - Here the decision is a magnitude in minutes. Facility is a feature, and the per-facility mean delays (4.0 / 12.9 / 8.4 min) are small against the MAE of about 15. That mechanism does not arise.
- The `original` text names per-facility evaluation and the definition states the difference, as MET-11 requires.
- Minor: this is the only definition in the working copy whose metric `definition` declares an aggregation across windows ("equal mean of nine window MAEs", credited to Myunghwan). That is the evaluator's standard, not a dataset choice.

**7. Other kept fields: consistent.**

- `IsLast` (known from the plan) and `mintime`/`maxtime` (elapsed times of active exams, by exact identities) follow LEAK-37 and USE-6, like digicow `topics_list`.
- The history fields follow LEAK-34 (an entity's own history under a temporal split is legitimate).

**8. Record discrepancy (not a precedent question)**

The 2026-11-04 assessment says "review panel (none): no panel ran for this dataset". The same record reports a "full independent panel" (2026-10-26) and a "full ten-role panel" (2026-10-28). The same templated line contradicts earlier panel claims in 6 other PR #33 records: ai4d_lab_tanzania_tourism_classification_challenge, airqo_low_cost_air_quality_monitor_calibration_challenge, huesken_sirna_efficacy, lt_vehicle_loan_default_prediction, open_soil_spectral_library and tunisian_fraud_detection_challenge.

**Summary:**
- **Consistent:** items 3, 4, 5, 6 and 7.
- **Item 1:** consistent in outcome. It cites LEAK-38 outside its written scope, and a rule change is due because this is the third or later case of the same kind.
- **Item 2:** departs from the source protocol, SPLIT-18/19 and aeolus. The stated reason is now weakened, so the curator should answer the question.
- **Not reasonable under the ranking:** none. No higher-ranked Must is broken.

</details>

<details><summary>Advocate</summary>

**Opening brief (advocate): ship `medical_facility_operational_data` after changes**

Verdict: ship after changes. The panel found no broken validity Must that the definition cannot fix. Every real problem it found has a fix that keeps the dataset: a protocol note, a definition fix or a documented note.

**1. Target, cohort and inputs are valid (P3 and P4, Musts hold)**
- **Claim:** the target means one thing, and every shipped input is known at arrival.
- **Evidence:**
  - `Wait` matches exam start minus scheduled time within 0.983 min in every row.
  - F1–F3 schedules sit on a 5-min grid. F4 is a different quantity: there Wait equals start minus arrival in 100% of rows.
  - The queue and flow fields match their at-arrival definitions in 99.2–100% of rows.
  - The history fields show 0 changes over 41,855 arrivals with no completion in between.
  - `AvgDelayForDay` is a running mean (corr 1.000). The `mintime`/`maxtime` identities hold in 100% of rows.
  - The leak probe finds no single carrier (0.583–0.588 against 0.584). The column auditor clears all 87 inputs.
- **Rules:** USE-5 (Must), LEAK-10 (Must), LEAK-37 (Must), LEAK-34 (Must). Dropping F4 follows rain_in_australia (Lennart, 2026-10-26).
- **Fix:** cite USE-5 and rain_in_australia instead of CLEAN-21. CLEAN-21 is about feature columns, not targets.

**2. The split mirrors the use case and is measured (P4: SPLIT-3, SPLIT-9 and SPLIT-14 Musts hold)**
- **Evidence:**
  - The split is temporal over a known entity, as Lennart decided on 2026-11-04 and as USE-10 requires.
  - Train is filtered on exam start. Only 4–14 pending rows per window are left out, so there is no selection by outcome.
  - The smallest train side is 41,002 of 82,001, the 50% floor.
  - One clock shift holds for all three facilities: `StartTime` + 60 min fits every row, and 0 of 694 shared days conflict.
  - IID is 2.6% optimistic (14.88 against 15.28).
- **The horizon departure (SPLIT-12/19, Should):** concede the departure from the source's 2-week test, and that the stated reason ("no real dates") is wrong. The departure is harmless:
  - 2-week windows score 14.40 against 14.42 on the same weeks.
  - Error does not grow with time since refit (15.37 / 15.06 / 15.33 / 15.47 by fortnight).
- **Mildest fix:** keep the windows. Answer the precedent check with (a), recorded as a departure, add the fortnight numbers to `splits_comment` and drop "windows count events, not days" from `fit_reason`.
- **`arrival_order`:** CLEAN-3 (Should) keeps a time index that carries meaning. It is known at arrival and dropping it costs +0.08 MAE. Fix: reword "timestamps are no inputs".

**3. The task gamer's exploit is real, but it is an evaluation leak (LEAK-9), not a data leak**
- **Concede:** a participant who reads later test rows in the same window can rebuild earlier patients' targets. MAE drops from 15.57 to 8.70.
- **Why the data is not the problem:**
  - Each row's own features are known at its arrival.
  - Row j carries row i's `Wait` only because i's exam had begun before j arrived. That is history, which is legitimate under LEAK-34 (Must).
  - The exploit needs rows that arrive after the prediction point. That makes it an evaluation leak, and LEAK-9 (Should) fixes those "in the scoring … not in the data".
- **Precedent:** sepsis_prediction_1m is the same case. Its notes say "Each hour is predicted from its own row only: no feature may combine a patient's rows."
- **Mildest fix:** add the same protocol line to `curation_comments` and `splits_comment`: each test visit is predicted from its own row and the training rows; no feature may combine test rows.
- **Why not drop the sum columns:**
  - They are the source's own congestion predictors and are known at arrival.
  - The gamer says the lead attack still works through the counts, so a data-side drop does not close the hole.
  - Dropping them would remove legitimate signal and still leave the leak open.

**4. The kept fields are small and kept with notes (P4, LEAK-38 Should, weak)**
- **Evidence:**
  - Dropping the expected-delay table changes MAE by 0.01–0.02 min.
  - The table is not the mean of its own rows (median gap 2.7–8.8 min).
  - The plan fields are built from the final schedule: 100% match, with a later add-on in view in 32.1% of rows. Dropping them costs +0.08 to +0.16 MAE, against seed noise of about 0.07.
- **Precedents with the same outcome:** sendy `Distance (KM)` (same day, a larger effect), perth `NEAREST_SCH_RANK`, house_sales.
- **Concede:**
  - LEAK-38 is cited outside its written scope, and this is the third or later such case. Lennart should get the amendment (consistency case 4), option (d).
  - The note should be widened to cover `AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount*`, `NumScheduledNext*` and `SumTimeToComplete*`, with the 100% match and the 32.1% add-on figure. It should also name the LEAK-27/32 risk (F3 corr 0.77).
- **Why this is enough:** a note is the rung LEAK-30 and LEAK-38 prescribe for a weak, untestable mechanism.

**5. The patient's own lateness: a curator's call, not a reason to hold the dataset (P3, USE-8 Must is met by naming the gap)**
- **Concede the numbers:** the offset is known at arrival, has r = −0.605 with Wait, and adding it lowers MAE by 1.7 min (−11%). It is no leak.
- **Steelman for the definition:**
  - The source's 84 features are patient-agnostic by design: "the next patient, whoever it will be" (Crowley 2020).
  - The challenge says the timestamps are for sorting only.
  - USE-6 makes the offset a legitimate input. It does not require us to add it.
  - CLEAN-19 (Should) builds features only on its listed grounds.
- **Mildest fix:** keep the source's feature set. Reword `question`/`known` to the source's framing and name the gap in `fit_reason`; the fit stays approximate.
- **Alternative:** add `minutes_early` (CLEAN-19, fix the definition). This also keeps the dataset, and it removes part of the gamer's gain #2.
- **Who decides:** this is a weighing call, so it goes to Lennart.

**6. Worth benchmarking, with the source's own metric (P6: MET-2, MET-4 and MET-5 hold)**
- **Signal:** the model scores MAE 15.28 against 21.54 for the train-median baseline, about 30% better and far from trivial. Per facility: F1 about 8, F2 about 17, F3 about 22.
- **Scoring:** all 9 windows score finite values.
- **Metric:** MAE is the challenge's deliberate goal, as in the zillow_prize precedent. RMSE would let F3's tail take 61% of the error, against 45% under MAE.
- **Concede (MET-11):** the cited page does not say "per facility". Fix: point `original` at `WTModel.m` / Crowley 2020, or reword it.

**7. Provenance and cleaning are cheap fixes (P5, P7)**
- **Provenance:** the author workbook is byte-identical to the Kaggle mirror (SHA256 recorded).
- **Licence:** the Dataverse API returns CC0 1.0. Fix the `license` string. This only makes the provenance stronger.
- **Cleaning (CLEAN-10, Should):** zeros stand in for statistics of empty sets. The `NoneInLine` and `NoneCompleted` flags mark those rows exactly, so setting them to missing is cheap and safe, and otherwise a note suffices. P7 never excludes a dataset.
- **Record:** fix "459 shared days" to 694, "six to seven weeks" to 42–52 days, and the 2026-10-28 panel and replay claims, which have no artefacts here.

**Judgment record**
- Validity: USE-5, LEAK-10, LEAK-34, SPLIT-3, SPLIT-9 and SPLIT-14 hold. LEAK-9 is fixed by a protocol note (sepsis_prediction_1m). LEAK-38 is kept with a widened note, and its amendment is due. SPLIT-12/19 is a departure kept with a measured note.
- Value: MAE as the source sets it; MET-11 reference fix.
- Quality: CLEAN-10 fix or note.
- For the curator: whether to add `minutes_early`, the LEAK-38 amendment, and the answer to the window question.

</details>

<details><summary>Critic</summary>

**Opening brief (critic): medical_facility_operational_data. Ship only after the changes below. Nothing here calls for exclusion.**

**1. P3. The patient's own minutes early are dropped, and the summary says the opposite (USE-6 Must, USE-5 Must, USE-8 Must).**
- **Problem.** `task_summary` asks about "this patient's imaging exam" and lists "the appointment plan" as known at arrival. But `_clean` and `_make_splits` drop `x_ScheduledDTTM` and `x_ArrivalDTTM` without keeping their difference (scheduled minus arrival). The clock shift is shared, so this difference is real minutes. The front desk knows it at check-in.
- **Effect.**
  - It correlates −0.605 with `Wait` (0.70, 0.56 and 0.78 at F1-F3).
  - Its negative is a hard lower bound on `Wait`: the exam begins after arrival in all 82,001 rows.
  - 27.2% of F1 patients arrive after their slot.
  - Adding it to LightGBM cuts MAE from 15.275 to 13.577 (−11%, all 9 windows). The column auditor and the practitioner measured −7% to −11% on 3 windows.
  - The task gamer recovers this value from later rows in the test block (`SumHowEarlyWaiting`): 15.57 → 14.75. Leaving it out therefore rewards a participant who decodes it.
- **Steelman.** The source keeps the timestamps "only for sorting". Crowley et al. predict delay "for the next patient, whoever it will be".
- **Remedy (the curator's call).**
  - (a) Derive `minutes_early` (CLEAN-19, USE-6) and consider moving the fit to direct (USE-9).
  - (b) Keep the source's patient-agnostic feature set. Then reword `question` and `known` to "the next patient, whoever it is" and name the gap in `fit_reason`.
- One of the two is required. As written, the definition contradicts its own inputs.

**2. P3. `fit_reason` names gaps that are wrong (USE-8 Must).**
- **Problem.**
  - "Windows count events, not days" is refuted by the record's own clock-shift finding. A window is a real 42-53 days.
  - Naming the kept expected-delay table as a gap breaks USE-8: "a potential leak kept on purpose does not by itself make a fit approximate."
- **The real gaps.** Point 1, and the current patient's exam type, contrast and inpatient/outpatient status, which the source's aggregation removed and which cannot be repaired.
- **Remedy.** Rewrite `fit_reason` around those gaps and name the table as kept, not as a gap. A text fix.

**3. P4. Rows later in the test block reveal earlier test rows' targets (LEAK-5 Must, LEAK-9 Should).**
- **Problem.** `SumDelayInProgress` is the sum of `Wait` over the exams in progress. With one exam in progress it equals an earlier same-day patient's `Wait`. I checked this myself: 14,150 of 14,150 rows, against 29.7% for a shifted control. `SumWaits`, `LineCount0` and `SumHowEarlyWaiting` reconstruct the queue.
- **Effect.** A participant who joins each test row to the test rows that arrived after it gets MAE 8.70 instead of 15.57 (−44%), in every split. Lead features alone give 13.64. A deployed model never has those later rows. No other panel report saw this.
- **Mitigation.** A model that fits on train and predicts each row on its own cannot use it. Each value is legitimate at its own row's arrival, so dropping columns would remove honest signal and still leave the lead attack open through the counts.
- **Remedy (LEAK-9, the sepsis_prediction precedent: fix the evaluation, not the data).**
  - Add a `Potential leak, kept on purpose:` note giving the mechanism and the 15.57 → 8.70 measurement.
  - State the prediction point as a constraint: each test row is predicted only from training rows and its own features, never from other test rows.
- A per-row snapshot scorer would be the full fix. Ask the curator whether the benchmark protocol guarantees independent predictions. If it cannot, this becomes a Must under LEAK-5.

**4. P4. The plan fields are the final schedule, but the notes say "not realised outcomes" (LEAK-10 / LEAK-38, Should; weak).**
- **Evidence.**
  - FutFlowCount2/4, NumScheduledNext*, SumTimeToCompleteNext*, IsFirst and IsLast match the scheduled visits that took place in 99.9-100% of rows. IsLast matches in 2,166 of 2,166 rows.
  - No-shows are removed and later add-ons included. 32.1% of rows see an add-on booked within the next hour.
- **Effect.** Dropping the fields changes MAE by +0.08 to +0.16, against seed noise of about 0.07. That is weak.
- **Remedy.** Keep the fields. Replace the incorrect claim with one `Potential leak, kept on purpose:` line covering all the plan fields and these numbers. Name `SumTimeToComplete*` beside the expected-delay table, since they appear to come from the same undocumented estimator.

**5. P4. The test horizon departs from the source, and the stated reason is refuted (SPLIT-19, SPLIT-12, Should).**
- **Problem.** The source tests on 2 weeks after 6 months of training. The aeolus_rebuilt_1m precedent uses 14 days. Ours is `horizon=4523 steps` "because no real dates", which the record itself refutes.
- **Effect.** Small when measured. 2-week windows score 14.40 against 14.42 on the same weeks, and error does not grow by fortnight since refit (15.37, 15.06, 15.33, 15.47).
- **Remedy.** No re-split. Add a sentence to `splits_comment` giving the real reason: about 4,550 test rows per window, and these measurements. Correct "six to seven weeks" to 42-53 days. Note that F3 has only about 8 months of history before window 8 (SPLIT-20).

**6. P5/P6. Provenance, metric origin and the record (PROV, MET-11 Must, EV-2).**
- **Licence.** `license` says "original terms not independently retrieved". The Dataverse API for doi:10.7910/DVN/X4SJWS returns CC0 1.0 (Pianykh, 2020-05-24). Set the licence from it.
- **Metric origin.** `metric.original` says MAE is "evaluated separately for source facilities", citing the challenge page. That page says "across all four facilities". The per-facility evaluation is in `WTModel.m` and Crowley 2020. Fix either the reference or the wording (MET-11 is a Must on the record's text).
- **Record.**
  - The notes say "459 shared days". The measurement on F1-F3 is 694.
  - The record's "full ten-role panel" lines (10-26, 10-28) contradict its 11-04 "no panel ran". No artefacts of those runs exist here. Mark them as external with no artefacts, or strike them.
  - Myunghwan's 10-28 "ship this" (all four facilities, 130,431 rows) should be marked as superseded.

**7. P7. Zeros stand in for statistics of empty sets (CLEAN-10 Should; quality only).**
- **Evidence.**
  - `AvgHowEarlyWaiting` and `AvgWaitByTaskTypeLine` are 0 in all 13,454 empty-line rows.
  - `MostRecent1` is 0 in 9,872 rows and `Median5` in 10,040 rows with nothing completed, where 0 is also a valid delay.
  - `AvgAgePeopleWaiting` uses two fill conventions: 0 at F1, repeated constants at F2 and F3.
  - `OutpatientWaitingCount` equals `LineCount0` + 1 in 80,886 rows. It probably includes the arriving patient. That is not a leak, but it is undocumented.
- **Remedy.** Cheap and safe: set these values to missing where `NoneInLine` or `NoneCompleted` marks an empty set. Otherwise keep them with a note. This alone is no reason to hold the dataset back.

**Not argued.** No reviewer found any P1, P2 or P5 problem that would exclude the dataset. Keeping F1-F3 only, the temporal split, MAE, the numeric `DayOfWeek`/`Month` and the expected-delay table (0.01-0.02 MAE) all stand. I drop the blind reviewer's request to drop `arrival_order`: it is known at arrival, removing it costs +0.08, and the order can be rebuilt from `StartTime` and `DayOfYear` anyway. I only ask that the false sentence "the timestamps … are no inputs" be reworded.

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (advocate): `medical_facility_operational_data`**

The critic and I agree on the verdict: ship after changes, with nothing that calls for exclusion. I concede five of the critic's seven points in full. On two points I dispute only one sub-claim each: the escalation to LEAK-5 in point 3, and the move to a direct fit in point 1.

**1. Minutes early dropped while the summary says "this patient" (USE-5, USE-6, USE-8 Must).**
- **Concede:** the definition contradicts its own inputs as written. One of the two remedies is required, not optional. Remedy (b), the source's framing plus the gap named in `fit_reason`, is the minimum. Remedy (a), adding `minutes_early`, is the alternative. The numbers are not in dispute: −0.605 correlation, 15.275 → 13.577 MAE, all 9 windows.
- **Dispute one sub-claim:** "consider moving the fit to direct (USE-9)."
  - Adding `minutes_early` closes one gap but not the other. The current patient's exam type, contrast and inpatient status were removed by the source's aggregation and cannot be restored (practitioner gap 3; the critic's own point 2 lists them).
  - USE-8 makes a fit direct only when the features mirror the use case. They still would not, so the fit stays approximate under either remedy.
  - USE-9 does not help either. It asks for *another* practitioner use case that the shipped data mirrors, and it bars rephrasing "only to excuse a gap" (use_case.md line 117).
- **What follows:** the choice between (a) and (b) goes to Lennart, and the fit is approximate either way.

**2. `fit_reason` names the wrong gaps (USE-8 Must).**
- **Concede in full.**
  - "Windows count events, not days" is refuted by the clock shift: 0 of 694 shared days conflict.
  - USE-8 says a potential leak kept on purpose "does not by itself make a fit approximate". So the expected-delay table moves out of the gaps and is named as kept.
- **What follows:** this is a text fix. Combined with point 1, `fit_reason` names two gaps: the patient-agnostic feature set, and the current patient's missing exam attributes.

**3. Later test rows reveal earlier test rows' targets (LEAK-9 Should; the critic adds LEAK-5 Must).**
- **Concede:**
  - The mechanism holds: 14,150 of 14,150 rows, and MAE falls from 15.57 to 8.70 when a participant reads later test rows.
  - The `Potential leak, kept on purpose:` note should carry that measurement.
  - The protocol line should say that each test row is predicted only from the training rows and its own features.
  - The per-row snapshot scorer is the full fix and a fair question for Lennart.
- **Dispute the escalation to a LEAK-5 Must:**
  - LEAK-5 asks "whether the stored values depend on the test rows" in a way the deployed setting would not have. Its case is coad's z-scores over all patients: a transform fit on the pool.
  - Here every stored value is causal at its own row's arrival. Row j carries row i's `Wait` only because i's exam began before j arrived. A deployed system has that value at j's arrival as well. That is entity history, which is legitimate under LEAK-34 (Must).
  - The data is honest. What breaks is the use of row j to predict row i, which is exactly LEAK-9's evaluation-level leak, fixed "in the scoring … not in the data; document the prediction point".
  - The sepsis_prediction_1m precedent ships with the same constraint as text: "Each hour is predicted from its own row only: no feature may combine a patient's rows" (dataset.py line 92).
  - The rule did not escalate there just because the harness cannot enforce row independence, and it should not escalate here.
  - Dropping columns would not help either. The critic agrees: honest signal is lost and the lead attack (13.64) still works through the counts.
- **What follows:** LEAK-9 note plus protocol line, as both briefs propose. Ask Lennart whether a snapshot scorer is wanted for the collection as a whole. The question is not specific to this dataset and is no reason to hold it.

**4. Plan fields are the final schedule (LEAK-10/LEAK-38 Should; weak).**
- **Concede in full.** This matches my point 4.
- **What follows:**
  - One `Potential leak, kept on purpose:` line covers `AheadCount`, `IsFirst`, `IsLast`, `FutFlowCount*`, `NumScheduledNext*` and `SumTimeToComplete*`.
  - It gives the 99.9–100% match, the 32.1% add-on exposure and the +0.08 to +0.16 MAE cost against seed noise of about 0.07.
  - The table note names the LEAK-27/32 risk (F3 corr 0.77).
- **Still due:** the LEAK-38 scope amendment, option (d), because this is the third or later case of the same kind (consistency case 4).

**5. Horizon departure (SPLIT-12/19 Should).**
- **Concede in full.** This matches my point 2.
- **What follows:**
  - No re-split.
  - One sentence in `splits_comment`: the source tests 2 weeks after 6 months; the longer windows keep about 4,550 test rows each; 2-week windows score 14.40 against 14.42 on the same weeks; and error does not grow by fortnight since refit (15.37, 15.06, 15.33, 15.47).
  - "Six to seven weeks" becomes 42–53 days.
  - Add the SPLIT-20 note on F3's history (about 8 months, 8,215 visits before window 8). The F3 MAE of 24.4 in windows 8 and 7, against 21.2–23.4 later, is too confounded to act on.
  - The precedent check's question is answered with (a), recorded as a departure.

**6. Provenance, metric origin, record (PROV, MET-11 Must on the text, EV-2).**
- **Concede in full.**
  - `license` becomes CC0 1.0 (Dataverse doi:10.7910/DVN/X4SJWS, Pianykh, 2020-05-24).
  - `metric.original` either cites `WTModel.m` and Crowley 2020, or drops "per facility".
  - In the record: 459 → 694 shared days. The 10-26 and 10-28 panel and replay lines are labelled as external runs with no artefacts here, or struck. Myunghwan's 10-28 "ship this" (130,431 rows, four facilities) is marked as superseded by Lennart's 2026-11-04 call.
- These changes only strengthen provenance. None of them touches validity.

**7. Zeros stand in for statistics of empty sets (CLEAN-10 Should; quality only).**
- **Concede in full**, including the critic's own words that this is "no reason to hold the dataset back" (P7 never excludes).
- **What follows:**
  - Where `NoneInLine` or `NoneCompleted` marks an empty set, set the value to missing. Otherwise keep it with a note.
  - Add a note that `OutpatientWaitingCount` (= `LineCount0` + 1 in 80,886 rows) and `MalesWaitingCount` appear to count the arriving patient. These are pre-arrival attributes, so this is no leak.

**Net position after rebuttal**
- **Agreed:** ship after changes. The text fixes are points 2, 4, 5, 6 and 7, the LEAK-9 note and protocol line from point 3, and the CLEAN-10 cleaning fix, which can also be a note.
- **Still disputed, both narrow:**
  - Point 3: LEAK-9 applies, not LEAK-5. Rests on LEAK-34 (Must) and the sepsis_prediction_1m precedent.
  - Point 1: the fit stays approximate even with `minutes_early`. Rests on USE-8 and the unrecoverable exam attributes.
- **For Lennart:**
  - (a) or (b) on `minutes_early`.
  - The LEAK-38 amendment, option (d).
  - (a) on the window question.
  - Whether to adopt a collection-wide per-row snapshot scorer.

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic): medical_facility_operational_data**

We agree on the verdict: ship after changes, with no exclusion. We differ in three places. (1) Whether the patient-offset remedy has to happen before shipping, or can be left as an optional curator choice. (2) How complete the `fit_reason` and plan-field fixes need to be. (3) Whether a note alone settles the test-row leak.

**A1. Target, cohort and inputs valid: concede, with one correction.**
- I concede USE-5, LEAK-34 and LEAK-37, and that LEAK-10 is not broken. No conditional test shows a post-outcome field. Citing USE-5 and rain_in_australia instead of CLEAN-21 is correct.
- Correction: "every shipped input is known at arrival" holds for the queue and history fields. It does not hold as worded for the plan fields. Those reflect the final schedule (100% match, 32.1% of rows with a later add-on in view), as the advocate concedes in A4.

**A2. Split: concede, with two additions.**
- I accept answer (a) with the measured reason.
- First addition: the span is 42-53 days, not 42-52. Window 4 is 52.9 days (split auditor).
- Second addition: the F3 history note is missing. F3 has about 8 months of history before window 8, and F3 MAE in windows 8-7 is 24.46/24.39 against 21.2-23.4 later. That belongs in `splits_comment` (SPLIT-20 Should, note only).

**A3. Test-row leak: concede the classification, dispute that a note alone settles it.**
- I agree on LEAK-9, on the sepsis_prediction_1m wording, and on not dropping the sum columns.
- But LEAK-9 says an evaluation leak "is fixed in the scoring … not in the data". Its own case says "sepsis_prediction needs a scorer change". A sentence in `curation_comments` describes the constraint. It does not enforce it.
- Here the attack does not need one entity's later rows. Any other test row works. So the line must say: "each test row is predicted from the training rows and its own features only; no feature or model step may use other test rows." The sepsis wording "no feature may combine a patient's rows" covers less than that.
- The curator should confirm that the evaluator predicts test rows independently, with no transductive or test-time feature step over the block.
- If it cannot guarantee that, LEAK-5 (Must) applies: the values depend on the test rows. The measured weight (15.57 → 8.70, −44% in all 9 splits) is then far past a LEAK-30 keep.

**A4. Plan fields and expected-delay table: concede the keep, dispute that the fix is complete.**
- Widening the note is right.
- It must also delete the false sentence at `dataset.py` line 77 ("refer to the plan, not to realised outcomes"). A widened note sitting next to that sentence leaves the definition contradicting itself.
- The advocate leaves the table in `fit_reason` as a gap (line 32: "the source does not document how its per-exam-type estimates were made"). USE-8 (Must) says a kept leak is "named … in `fit_reason` as kept, not as a gap". Removing only "windows count events, not days", as the advocate proposes in A2, still leaves `fit_reason` against USE-8.
- I agree that the LEAK-38 amendment, option (d), goes to Lennart.

**A5. Patient's own lateness: dispute "not a reason to hold the dataset".**
- As written, `question` ("this patient's imaging exam") and `known` ("the appointment plan") claim an input the definition drops.
- `fit_reason` does not name this gap. USE-8 (Must) requires the fit and its gap to be stated truthfully, so the definition fails USE-8 until (a) or (b) is applied. The advocate's own fix is a change to the definition, so it is a condition for shipping, not optional.
- Between the two remedies, the rules favour (a):
  - USE-6 (Must) gives the reason in its own "Why": dropping a known input "changes the task into 'predict without …'".
  - The offset is the largest known-at-arrival signal: r = −0.605 (up to 0.78 at F3), −11% MAE in all 9 windows. The table the curator kept is worth 0.01-0.02.
  - CLEAN-19's second ground ("restores meaning the source destroyed") fits: the anonymisation kept the difference and removed only the absolute times.
- (b) runs into the USE-9 weighed factor "a use case rephrased only to excuse a gap". The practitioner says the quote is given to this patient at check-in.
- (b) stays allowed if Lennart prefers to follow the source. It then needs honest wording and an approximate fit.
- Both briefs leave the choice to Lennart. Doing neither is not an option.

**A6. Value and metric: concede.**
- MAE, MET-2/4/5 and the per-window equal mean stand.
- The MET-11 reference fix is a Must on the text, and both briefs ask for it.

**A7. Provenance and cleaning: concede, with two additions.**
- The CC0 licence, the CLEAN-10 fix or note, and the record fixes (694 shared days, the 10-26/10-28 panel lines) all stand.
- First addition: mark Myunghwan's 10-28 "ship this" (four facilities, 130,431 rows) as superseded by the 11-04 decision, as the chicago line of the same day does (precedent checker, item 3).
- Second addition: note that `OutpatientWaitingCount` probably counts the arriving patient (`LineCount0` + 1 in 80,886 rows). This is not a leak, and the note is quality only.

**Remaining conditions for shipping, ranked**
1. Apply (a) or (b) for the patient offset (USE-8, USE-6).
2. Rewrite `fit_reason`: remove "events, not days", name the table as kept, and name the real gaps (USE-8).
3. Add the per-row prediction constraint, and have the curator confirm the evaluator enforces it (LEAK-9; LEAK-5 if it cannot).
4. Replace the false sentence at line 77 with a widened plan-field note (LEAK-10/38 Should).
5. Add the real horizon reason, 42-53 days and the F3 history note to `splits_comment` (SPLIT-12/19/20).
6. Fix the licence, the MET-11 reference and the record (EV-2).
7. CLEAN-10 zeros: set to missing, or add a note.

</details>
