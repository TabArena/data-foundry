# basque_offshore_ctd_chlorophyll

**Outcome:** added. The AI recommends shipping it with the fill of a survey whose fluorometer failed as the use case (issue 1); if you reject that use, it is `No` + `No Good Target / Scientific Discovery`. AZTI's CTD profiles off Mendexa, 2014-2023, rebuilt from AZTI's Mendeley release: the chlorophyll of each 1-dbar bin is predicted from the other channels of the same casts and the station's earlier surveys, on nine windows of two survey days (2022-09-12 to 2023-12-18), each trained on every earlier survey. Validity: USE-1 and USE-2 are a weighing (issue 1): no source names the fill, and glioma's deciding fact (a label made before its features) is absent here; USE-3, USE-10 and SPLIT-3 triggered and fixed: the day-grouped split kept each test day's later surveys in training, so the split is now temporal, with the station's last measured chlorophyll and its age as features; LEAK-10 holds; USE-5 and PROV-13: the fluorometer's calibration may change in 2018-2022 (circumstantial, EV-6), kept with a note (issue 2); PROV-8 holds (not Zhou's IQR copy). Value: TP-10 leg 1 holds on the declared metric: RMSE 0.485 ug/l against 0.623 for the training mean, 0.617 for the last survey and 0.541 for the newest surveys' level, better in 7, 7 and 6 of 9 windows (untuned LightGBM, mean of 3 seeds; the mediator's run gave 0.488); the probes, on the log scale, flag `no_signal`, `drift_baseline` and `unstable`, to re-check with tuned results (TP-1). Quality: CLEAN-10 and CLEAN-15 hold; the 0.03 floor and PAR's daylight quenching are in the notes; `rmse` is the fallback (MET-1, MET-2), `rmsle` open (issue 3). Weighed: source +; use case - (our wording; the fluorometer never failed in the release); size 0 (146 survey days, 129-172 test rows per window); gap 0. Left for Andrej: issues 1 to 3.

Changes made after the review panel (AI, 2026-11-01): the temporal re-split and the last-survey features; the use case narrowed to the fill at the survey (the cast made without a fluorometer dropped); `fit_reason`, the notes and the metric reason rewritten; the panel's factual slips corrected. The panel's reports describe the earlier day-grouped definition.

**Main points:** Is filling a failed survey's chlorophyll a real use case (otherwise `No`, as glioma)? Ask AZTI for the fluorometer's calibration history? Keep `rmse`?

**Record fields that disagree with the definition:**

- `original_source`: record `Github`, definition `Other`.
- `required_split`: record `Grouped (NON-IID)`, definition `Temporal (NON-IID)`.

**Issues for Andrej:**

1. **Is filling a survey whose fluorometer failed a real use case?**

   * **Problem:**
     - No source names a use for predicting this chlorophyll channel.
     - Our use case: when a survey's fluorometer fails, AZTI estimates that survey's chlorophyll from the other channels
       and earlier surveys.
     - If that moment is no real decision, the dataset goes[^1a]; whether it is real is a weighing.
   * **Background:** the data descriptor (Solaun et al. 2025, https://doi.org/10.1016/j.dib.2025.111736) names
     trends, toxin limits, shellfish management and bloom early warning, all for the series as a whole. Zhou et al.
     2026 picked the target for a cross-dataset benchmark. The use case is our wording: when a survey's fluorometer
     fails, AZTI estimates that survey's chlorophyll profile from the other channels of the same casts and the
     station's earlier surveys, and reports it to the shellfish managers and the mussel farm. If that moment is no
     real decision, the benchmark ranks models on a reading no actor waits for: a task needs an actor, a moment and a
     decision, and a task no decision fits is out[^1a].
   * **Effect on the task:** the use case sets the split: at the fill only the station's earlier surveys are
     known[^1b]. The builder had held out random survey days, which kept each test day's later surveys in training:
     that is a fill made in hindsight, and no source practice supports it. The new windows hold two survey days each,
     about a monthly refit; their scores are in the outcome's Value line.
   * **For keeping:** chlorophyll virtual sensors are an established method (SOCA-CHL, Sauzède et al. 2016); SOCA-CHL
     also takes satellite chlorophyll, which this table lacks (domain practitioner), so it backs the method more than
     this moment. The sensors on this package fail one channel at a time: five casts in the release lost a whole
     channel (PAR, oxygen, salinity, temperature), each on a single survey. Refit on every earlier survey, the model
     beats carrying the last survey's profile forward, the fill a team would make without a model: 0.485 against
     0.617 ug/l, better in 7 of 9 windows.
   * **For retiring:** in ten years the fluorometer never failed in this release; the one bin without chlorophyll
     lacks every channel. AZTI publishes the channels that did fail as no data and fills none of them.
   * **Consistency:** glioma_grading_clinical_and_mutation_features went `No` + `No Good Target / Scientific
     Discovery`[^1c]. In glioma the grade exists before the DNA features, so a model could only cross-check a known
     label. Here the channels exist exactly when the chlorophyll is missing. The two cases share only that no source
     names the use. Your scope call of 2026-10-30 on the species surveys points toward keeping[^1d].
   * **Unknown:** AZTI could settle it by saying whether a survey without chlorophyll is ever reported with an
     estimate; the request of issue 2 can ask.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The fill of a failed survey as the use case (implemented) | the fill at the survey; temporal windows of two survey days, each trained on every earlier survey | an established method; the channels exist exactly when the chlorophyll is missing; beats carrying the last survey forward in 7 of 9 windows | our wording; the fluorometer never failed in the release, and AZTI fills no failed channel |
     | B | Treat it like glioma | verdict `No` + `No Good Target / Scientific Discovery`; the folder leaves | follows glioma | the fact that sets this case apart is not used |

   * **Recommendation:** A, keep, and record as the fact that sets it apart from glioma that the other channels exist
     exactly when the chlorophyll is missing. **Decision:** accept the fill of a failed survey as the use case (A), or
     retire the dataset (B)?

   **Notes for the AI:** on A, record the fact as a Cases row under USE-1. The split change made for A follows USE-3,
   USE-10 and SPLIT-3. On B, the verdict `No` with `No Good Target / Scientific Discovery` (USE-1, USE-2), and the
   folder leaves the working copy.

   [^1a]: **USE-1** (Must): a use case is an actor, a moment and a decision, written down before anything else.
     **USE-2** (Must): a task no decision fits is out; marker `No Good Target / Scientific Discovery`.
   [^1b]: **USE-3** (Must): name the prediction point, when the model is used and what is known then. **USE-10**
     (Must): decide from the use case whether the entity is new or known before choosing the split; for a known one,
     its history is legitimate, the split is temporal and the previous outcome is a feature. **SPLIT-3** (Must): a
     task is grouped or temporal, never both, and the use case decides which.
   [^1c]: Lennart, 2026-10-26, glioma_grading_clinical_and_mutation_features: "too far-fetched".
   [^1d]: Andrej, 2026-10-30, a scope call under **SEL-2** (Must; let the use case decide whether a scope rule
     applies): "if a dataset is useful for a predictive application although the data was collected for something
     else, then this is fine".

2. **Ask AZTI for the fluorometer's calibration history?**

   * **Problem:**
     - The fluorometer may have been swapped or recalibrated during 2014-2023, so the same water could read differently
       in different years.
     - The evidence is circumstantial[^2a], and the release does not record the instrument's history.
     - Ask AZTI for it, or keep only a note?
   * **Background:** the value 0.03 ug/l is a floor that appears only from 2018-11-19 to 2022-09-12 (287 bins in 25
     casts, none before or after); the casts' minima jump from 0.03 on 2022-09-12 to 0.44 and 0.47 on 2022-10-03; in
     the same period, the relation between light transmission and chlorophyll below 10 m changes sign.
   * **Unknown:** the descriptor names two CTD models but no fluorometer model, calibration or dates, so the data
     cannot tell an instrument change from a change in the sea.
   * **Effect on the task:** if these are instrument periods, models partly learn which period a date falls in, and
     they miss an unannounced recalibration: on the new windows, the model predicts about 1.7 times too low over the
     seven survey days after the step (2022-10-03 to 2023-03-13). For the fill, the series' own reading is still what
     AZTI would report, and the target is what the actor acts on[^2b], so this is no reason to exclude the dataset
     today. The rule is to repair from the origin first[^2c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | A note only (implemented) | a note with these numbers in the curation comments and `fit_reason` | nothing to wait for | a possible instrument change stays unrepaired |
     | B | Write to AZTI, keep the note meanwhile | ask for the CTD and fluorometer history, and whether a survey without chlorophyll is ever reported with an estimate (issue 1) | a correction would repair the target from the origin; the answer bears on issue 1 | costs only a wait: nothing ships differently until they answer |

   * **Recommendation:** B, send the request and keep the note meanwhile: a correction would repair the target from
     the origin, and nothing ships differently while we wait. **Decision:** send it (B) or not (A)?

   **Notes for the AI:** on an answer, if AZTI has a correction, repair the target from it (PROV-13). If they confirm
   periods with no correction, weigh USE-5 again.

   [^2a]: **EV-6** (Should): say which evidence is proof (a test that could have refuted the claim) and which is
     circumstantial.
   [^2b]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it.
   [^2c]: **PROV-13** (Must): when a release is damaged, check whether the origin has the clean data before keeping
     the damage or retiring the dataset, and repair or rebuild from the origin when it has them.

3. **Score the error in ug/l (`rmse`) or the relative error (`rmsle`)?**

   * **Problem:**
     - No source has a metric for this task, so the fallback `rmse` on ug/l is declared.
     - It weighs bloom values heavily, so a few bloom casts decide the ranking.
     - Keep it, or score the relative error (`rmsle`)?
   * **Background:** Zhou's R^2 was chosen to compare datasets, on a copy without the blooms, so it does not score
     this task on these data[^3a]. The bloom window of March 2023 alone makes up a third of the averaged `rmse` (1.51
     ug/l there, against 0.23-0.58 in the other windows).
   * **Experiments:** on the new windows the two metrics agree on which predictors beat which.
   * **Panel:** the domain practitioner prefers `rmsle`, for two reasons: ocean-colour work scores chlorophyll on a
     log scale, and `rmsle` acts like an absolute error below about 1 ug/l and like a relative one in blooms. A metric
     from the context is allowed only when the task makes it obvious[^3b], and the panel splits on that: the advocate,
     the critic and the claim auditor keep `rmse`, because the managers act on blooms.
   * **Consistency:** `rmsle` from context was declared for brazilian_ecommerce and melbourne_housing_market.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `rmse` on ug/l (implemented) | scored by the fallback, the error in ug/l | the managers act on blooms | a few bloom casts decide the ranking |
     | B | `rmsle` from context | scored by the relative error, a metric taken from the context | spreads the weight over the whole range (the 0.03 floor bins carry 2% of its error); the scale of ocean-colour work | needs a context the panel does not agree is clear |

   * **Recommendation:** A, keep `rmse`: the managers act on blooms, and the panel does not agree that the context
     makes `rmsle` clear. **Decision:** keep it (A) or switch (B)?

   [^3a]: **MET-1** (Must): the declared metric scores the real task, the decision of the use case. **MET-2** (Must):
     match the data, the metric and the real task.
   [^3b]: **MET-11** (Must), context origin: the source defines no metric, but the task makes one obvious; only when
     the context is clear, otherwise the fallback.

   **Andrej (2026-11-03, dataset note):** The resons to not ship this dataset outweigh the reasons to ship, it seems
   like this is a made up task.

   **Resolved (2026-11-03, Andrej):** don't ship: the record is `No` with `No Good Target / Scientific Discovery` and no
   priority, its `v2_path` cleared and its claim released; the record fields take the definition's values
   (`original_source` Other, `required_split` Temporal); the folder leaves the working copy (copies of its last files in
   the run folder of 2026-11-03, `basque_ctd_retired/`).

**Review panel:** ship after changes, if the fill of a survey whose fluorometer failed is accepted as the use case (mediator). Claim audit: 48 claims, 36 hold, 9 refuted (7 fixed in the definition; 2 in the record, the `original_source` field row and the 2026-10-30 Assessment, to correct at hand-over), 3 untested. Blind review: would exclude (borderline); main concern that no decision depends on predicting the channel and that the date tracks calibration periods. Debate: agreed on the temporal re-split with the last survey as a feature, the notes and keeping `rmse` (the domain practitioner prefers `rmsle`, issue 3); disputed: whether the failed-survey fill is a use case (issue 1).

<details><summary>Mediator</summary>

**Mediator: basque_offshore_ctd_chlorophyll (2026-11-01)**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-3 / USE-2 hold on the rule reading, open as a weighing for the curator (issue 1): the glioma precedent's
  deciding fact (a label that exists before its features) is absent here. USE-1 holds once narrowed to the fill of a
  failed survey at the survey (fit approximate, USE-8: the fluorometer's calibration over the record is unverified).
  USE-3 / USE-10 / SPLIT-3 triggered, fixed: re-split temporal on whole survey days (9 windows of 2 days) with the
  station's last measured chlorophyll as a feature. SPLIT-14 holds (oldest window trains on 83%). LEAK-10 holds.
  USE-5 / PROV-13: possible instrument periods, circumstantial (EV-6): kept with a note, the request to AZTI is issue 2.
  PROV-8 holds (rebuilt from AZTI's release, not Zhou's IQR copy).
Value: TP-2 and TP-10 leg 1 hold on the re-split: RMSE 0.488 ug/l against 0.623 (training mean) and 0.617 (the last
  survey), better than each in 7 of 9 windows.
Quality: CLEAN-10, CLEAN-15 hold; the 0.03 floor, the daylight quenching and the raw counts go into the notes; the
  metric reason cites MET-1 / MET-2, not MET-5.
Weighed: source +, use case - (our wording; the fluorometer never failed in the release), size 0 (146 survey days,
  9 windows of 129-172 rows), gap 0.
For the curator: issue 1 (is the failed-survey fill a use case, else No as glioma), issue 2 (ask AZTI for the
  calibration history), issue 3 (rmse or rmsle).
```

**Agreed facts**

Every agent's numbers that bear on a decision reproduce, and neither side disputes these:

- The table is AZTI's Mendeley release v2 (sha256 d7a00558..., the same file in v1 and v2, CC BY 4.0): 8,195 bins of 180 casts on 146 days, two stations 1.82 km apart. Zhou et al.'s copy keeps 4,653 bins of 132 casts, cuts the blooms (maximum 1.47 against 11.13) and drops every Mussel Farm row.
- No column records anything after the target; sigma-theta and oxygen saturation are computed from known channels; missingness does not encode the target (LEAK-10 holds).
- No source names a use for predicting the chlorophyll channel. The descriptor's uses are trends, toxin limits, shellfish management and early warning for the series as a whole.
- The fluorometer never failed in the release: the one bin without chlorophyll (2017-09-04, 39 dbar) lacks every channel. Five casts lost another whole channel (PAR 2015-06-01 and 2016-10-17, oxygen 2017-09-04, salinity 2023-03-06, temperature and salinity 2023-12-11), each on a single survey, and AZTI published all five as no data.
- The date's skill is the channels read against their period, not interpolation: neighbouring training days' profile 0.03-0.04 R^2 (log), date + depth + station 0.106, channels without the date 0.058, all together 0.451-0.455; the season adds nothing (0.037).
- The 0.03 minimum is a reporting floor: 287 bins against 37 at 0.04, all from 2018-11-19 to 2022-09-12 (25 casts). The Two-Regime Zeros tag stays off (3.5% against 1.9% for the next value). Cast minima step from 0.03 (2022-09-12) to 0.44 and 0.47 (2022-10-03).
- PAR carries part of the fluorometer's daylight quenching: in mixed casts the ratio of the top 5 m to 6-15 m falls from 0.97 to 0.47 across the PAR quarters (Spearman -0.73).
- The shipped day-grouped split keeps a test day's later surveys in training (next survey in training 70.1% of the time). A fill made at the survey cannot have them.
- The other station's same-day reading at the same depth alone gives R^2 0.736 (1,218 pairs).
- RMSE on ug/l is computable on every fold. Within a fold it ranks models as R^2 on ug/l does. Zhou names R^2 as its criterion, so MET-5 would accept it; MET-1 and MET-2 reject it.
- Factual slips: 1.82 km, not 1.5; 111 Mendexa-only days + 1 Mussel-only (2022-03-08) + 34 with both; cast-against-day numbers stale (now 0.641 against 0.348); "the curator's brief asked for a split by cast" is the AI screening's proposal; the -999 counts are raw; `known` omits oxygen saturation; `original_source` should be `Other`.

**Decisive experiment: the windows of the re-split.** Both sides agree on a temporal split. The windows were chosen from counts and dates only, before any score (SPLIT-21):

| Candidate (unique survey days) | Test days covered | Test rows per window | Windows below 50 rows | Oldest train share |
|---|---|---|---|---|
| 1 day x 9 | 2023-05-03 to 2023-12-18 | 45-88 | 2 | 0.917 |
| 1 day x 9, every third day | 2022-05-03 to 2023-12-18 | 45-88 | 2 | 0.773 |
| **2 days x 9 (chosen)** | 2022-09-12 to 2023-12-18 | 129-172 | 0 | 0.831 |
| 2 days x 14 (advocate) | 2022-03-21 to 2023-12-18 | 127-172 | 0 | 0.747 |
| 3 days x 9 (advocate) | 2022-04-05 to 2023-12-18 | 179-255 | 0 | 0.753 |

The reasons: SPLIT-15, as many windows as the grouped task had folds (9). SPLIT-17, one-day windows hold one or two casts, and 2 of 9 fall below 50 rows. SPLIT-20, consecutive one-day windows cover May to December 2023 only, while two-day windows cover every month from September 2022. SPLIT-12, two surveys are about a month at the programme's "monthly or biweekly" cadence, a plausible refit cadence. SPLIT-14 holds.

Scores on the chosen windows: untuned LightGBM with the builder's settings, mean of 3 seeds, the date as day of year plus fractional year.

| Predictor | RMSE ug/l (mean of 9 windows) | Beats training mean | Beats last survey | RMSLE | R^2 log, pooled |
|---|---|---|---|---|---|
| LightGBM, with last survey | 0.488 | 7/9 | 7/9 | 0.255 | +0.114 |
| LightGBM, without last survey | 0.485 | 7/9 | 6/9 | 0.256 | -0.002 |
| LightGBM, with last survey, no date | 0.540 | 6/9 | 6/9 | 0.285 | -0.183 |
| Training mean | 0.623 | - | 4/9 | 0.335 | -0.540 |
| Last survey (persistence) | 0.617 | 5/9 | - | 0.316 | -0.633 |

- On ug/l the last-survey feature adds nothing (0.488 against 0.485). It stays because USE-10 makes the previous outcome a feature for a known entity, and it lifts the log-scale fit.
- One bloom window (2023-03-06 to 03-13: 1.51 ug/l) carries a third of the averaged RMSE.
- The advocate's own check (1-day x 27, 2-day x 14) gave 0.484-0.491 against 0.62, so the choice of window does not change the picture.

**Changes to make now (no decision needed)**

1. **Re-split temporal (USE-3, USE-10, SPLIT-3, Must; SPLIT-11, -12, -14, -15, -17, -20, -21).**
   - Remove `grouping` and the `survey_day` column, and its `string=["survey_day"]` entry in `_feature_types`. The `dataset_duplicate_columns` warning goes with them.
   - Declare `temporal = Temporal(on="cast_date", splits=TemporalSplits(window=2, unit="unique", n_windows=9), horizon=2, horizon_unit="steps")`, where a step is one survey day.
   - It must reproduce these windows exactly (1,386 test rows on 18 survey days). Both stations' casts of a day fall in one window by construction:

| Split | Test days | Test rows | Train share |
|---|---|---|---|
| 0 | 2023-12-11, 2023-12-18 | 172 | 0.979 |
| 1 | 2023-10-03, 2023-11-27 | 166 | 0.959 |
| 2 | 2023-08-21, 2023-09-19 | 129 | 0.943 |
| 3 | 2023-06-20, 2023-07-26 | 130 | 0.927 |
| 4 | 2023-04-03, 2023-05-03 | 164 | 0.907 |
| 5 | 2023-03-06, 2023-03-13 | 129 | 0.891 |
| 6 | 2023-01-23, 2023-02-14 | 160 | 0.872 |
| 7 | 2022-11-30, 2022-12-13 | 167 | 0.851 |
| 8 | 2022-09-12, 2022-10-03 | 169 | 0.831 |

2. **Add the last measured profile (USE-10, Must; TP-10 allows the last observation; LEAK-10 holds).**
   - `last_chlorophyll_a_ug_l`: chlorophyll in ug/l at the same station and 1-dbar bin on the latest earlier survey day. When the station has none at that bin, use Mendexa-Control's at that bin. Never the same day.
   - `last_chlorophyll_age_days`: its age in days.
   - Reproduce: missing on 52 rows (bins not reached before, on 2014-05-20, 2014-06-09, 2014-08-20); age median 21 days, maximum 868. Then the scores in the table above (LightGBM 0.488 against 0.623 and 0.617, 7/9 and 7/9), up to seed noise.
3. **Narrow the use case (USE-1, USE-3, Must).**
   - `use_case`: when a survey's fluorometer fails, AZTI's team estimates that survey's chlorophyll profile from the other channels of the same casts and the station's earlier surveys, as it reports the survey to the shellfish managers and the mussel farm (food supply, bloom warning). No source names this use.
   - Drop "or estimates chlorophyll for a cast made without one": such a CTD rarely carries the optical channels, and that is a second moment (SPLIT-3).
   - Reword `question` to match. Add oxygen saturation and the last survey to `known`.
4. **Rewrite `split`, `changes` and `splits_comment` for the windows (SPLIT-12: write the reasoning down).** The text says:
   - two survey days per window, which is about a monthly refit;
   - every earlier survey trains;
   - why the day is never split: the other station's same-day reading alone gives R^2 0.736, and both casts come from one boat trip and probably one CTD;
   - that the transient glitch of 2023-12-11 hit one cast only.
5. **Rewrite `fit_reason` (USE-8, Must).** Approximate, for these reasons:
   - the fluorometer's calibration across the record is undocumented: the 2018-2022 floor and the 2022-10-03 step may be instrument periods, an unverified label;
   - no source names the fill;
   - the channels predict the reading only when read against the period;
   - part of PAR's skill is daylight quenching.
   Add the real-time numbers (0.488 against 0.623 and 0.617; 0.540 without the date). Remove "filling between the surveys" (refuted) and the frozen-year figures.
6. **Correct `curation_comments` (P7; EV-1, EV-8).**
   - The target bullet: 0.03 is a floor of 2018-11 to 2022-09, and no two-regime zero.
   - Replace the group bullet with the window bullet (1.82 km). Drop the attribution of the cast split to the curator.
   - Mark the -999 counts as raw, or give the shipped ones (PAR 296, salinity and sigma-theta 94, temperature, oxygen and saturation 46, light transmission 0, time 45 rows of one cast).
   - Rewrite the date Note with the decomposition above.
   - Add a quenching sentence to the optical bullet, and drop its platform question (moot).
   - Add a Note on the possible instrument periods, with the floor, the step, the light-transmission slope (-0.038, +0.009, -0.027) and the real-time fill after the step (too low by a factor of about 1.8 over the 7 survey days from 2022-10 to 2023-03).
7. **Metric reason (MET-1, MET-2, MET-11).**
   - Cite MET-1 and MET-2 for rejecting Zhou's R^2: chosen to compare datasets, on a copy without the blooms and Mussel Farm.
   - List Zhou's MAE, RMSE, NRMSE, NSE and event F1.
   - State that R^2 on ug/l ranks models as RMSE does within a window.
   - `rmse` stays declared (issue 3).
8. **Record.** Add a dated Assessment correcting the 2026-10-30 reason for removing the tag: a floor of one period, not a continuous spread; the removal stands. The phrase "the low end of a continuous spread" also appears in item 4 of the triage summary's policy calls. The record fields go to the curator as field rows: `original_source` Github to Other, `required_split` Grouped to Temporal.
9. Re-run `dataset check` and the probes on the new definition.

**Changes that need the curator (ranked)**

1. **Is the fill of a failed survey a use case? (P3; USE-1, USE-2, Must; a weighing.)**
   - Problem: the benchmark scores a use that only we wrote down.
   - Effect: if the use is not real, models are ranked on a target no actor waits for.
   - For keeping:
     - chlorophyll virtual sensors from CTD channels are established practice (SOCA-CHL, Sauzede et al. 2016);
     - this package's sensors fail one channel at a time (5 single-survey failures);
     - in real time the model beats the last survey (0.488 against 0.617 ug/l);
     - glioma's deciding fact is absent;
     - the curator's call of 2026-10-30 accepts uses the data was not collected for.
   - For retiring:
     - the fluorometer never failed in ten years of this release;
     - AZTI fills nothing, and publishes failed channels as no data;
     - no source names any use of the channel, and Lennart called glioma "too far-fetched".
   - Decision: accept the moment, recorded as the fact that sets the case apart from glioma, or `No` + `No Good Target / Scientific Discovery`.
   - What would settle it: AZTI saying whether a survey without chlorophyll is ever reported with an estimate.
2. **Ask AZTI for the CTD and fluorometer history (P3/P5; PROV-13, USE-5, Must; circumstantial).**
   - Problem: the target may change scale at the 2018-11 floor and the 2022-10-03 step.
   - Effect: models learn the calibration periods, and they fail at an unannounced recalibration.
   - Both sides: a note now and the request. Neither excludes the dataset today, since the series' own reading is what the fill reports.
   - Decision: send the request or not. With a correction, repair the target; with periods and no correction, weigh USE-5 again.
3. **`rmse` or `rmsle` (P6; MET-11, MET-1; a weighing).**
   - For `rmse` (advocate, critic, claim auditor): the managers act on blooms, and the panel does not agree that the context is clear, and without a clear context MET-11 keeps the fallback.
   - For `rmsle` (practitioner): ocean-colour practice, and one bloom window carries a third of the averaged RMSE.
   - The two agree on which predictors beat which on the new windows.
   - Recommendation: keep `rmse`.

**Disputed points**

| Point | Advocate | Critic | Ruling | Rule and why |
|---|---|---|---|---|
| Glioma precedent (USE-1, USE-2) | set apart: the features exist when the label is missing | conceded in rebuttal (option a); disputes only the "stores" half of the decision | The precedent does not apply on its deciding fact. The weighing (is the moment real or far-fetched) goes to the curator | Rules over precedents. Glioma turned on a label made before its features ("a cross-check of a known label"). The shared fact, no source names the use, did not decide alone, and the curator's call of 2026-10-30 item 1 points the other way. Not a conflict between rules: every Must still has to hold, and USE-1 holds only if the moment is accepted |
| Regime: grouped (fill later) or temporal (fill at the survey) | conceded temporal in rebuttal | temporal | Temporal, settled | USE-3, USE-10, SPLIT-3 (all Must): the moment with an action is at the survey, the stations are known entities, and EV-2 holds (AZTI fills nothing later, 5 of 5 failures published as no data). Not decided by score (SPLIT-4): RMSE on ug/l is about the same either way (0.488 against 0.476) |
| Windows | 1 or 2 survey days, at least 9 windows | survey cadence, at least 50 rows | 2 days x 9 | SPLIT-15, SPLIT-17, SPLIT-20 on counts; SPLIT-21 (no score used) |
| Hold out the day or the cast | day | day | day, by construction of the windows | SPLIT-1, SPLIT-23. A per-cast split would let the other station's same-day reading tell the held-out cast (0.736). Floors hit both casts on 3 days, consistent with one CTD per trip. The split auditor's weighing is answered by the re-split |
| Keep `cast_date` (column auditor option b, after infrared_thermography_temperature) | keep | keep | keep | USE-6, LEAK-10: known at the survey. The use is a fill in a monitored series, not a calibration "independent of time" (the light-transmission relation changes sign between years) |
| Target scale over time | note, ask AZTI | note, ask AZTI | agreed; the request is the curator's (issue 2) | PROV-13 (repair from the origin first) |
| Metric | keep `rmse` | keep `rmse` | weighing to the curator (issue 3) | MET-11 |
| Blind reviewer: exclude, or log(chl + 0.05) | - | - | not adopted | The exclusion rests on issue 1. The transform changes nothing scored on ug/l (MET-3), where the floor carries 0.6% of the squared error. How a model encodes a datetime is the model's choice |

**Consistency with precedent**

- `glioma_grading_clinical_and_mutation_features` (USE-1, `No`, Lennart, 2026-10-26): departs. The distinguishing fact is named in issue 1, and the precedent checker's consistency check goes to the curator.
- `nba_players_2016_2019` (the prediction point moved to fit the data): the use case here moved twice. The last move picks the moment with an action, against the score: the temporal split scores no better (SPLIT-4).
- `5g_energy_consumption`, `wadden_sea_sibes_macoma_abundance` (fills of units unmeasured at the same time, grouped): set apart. A past survey is not filled from later ones.
- `basque_offshore_bivalve_biotoxins` (same programme): followed. Temporal on distinct days, with the last result and its age as the only lag (TP-10 as amended 2026-10-26). Window lengths differ by use (SPLIT-12 Cases: no family window).
- `infrared_thermography_temperature` (date dropped): not followed, for the fact in the table above.
- USE-8 "no actor named": five run siblings rest "approximate" on it, which USE-8 does not list. Here approximate rests on the unverified label (`differentiated_thyroid_cancer_recurrence`), so this dataset does not set that precedent.
- The sibling's record also says `original_source: Github`, and should be corrected in its own review.
- After issue 1, a Cases row is due under USE-1 (set apart from glioma, or retired with it).

Scripts: the mediator's scratch folder in the panel (frame.py, counts.py, resplit.py, lagcheck.py, with their .txt outputs).

</details>

<details><summary>Claim audit</summary>

**Claim audit: basque_offshore_ctd_chlorophyll (claim-auditor, 2026-11-01)**

**Verdict:** the facts hold and the numbers reproduce. 48 claims: 36 hold, 9 refuted (one of them partly), 3 untested. Nothing refuted breaks validity. The most important refutation is about why the date helps, and it cuts in the dataset's favour. The date is not "filling between surveys": it is the date combined with the channels that works. Models read chlorophyll off the channels through a mapping that drifts over time, which is the stated virtual-sensor use (USE-1, USE-8; draft issue 1). The second is the target note. The 0.03 minimum is a reporting floor in 2018-2022, not "the low end of a continuous spread". The tag decision stands; the note and the record's Assessment should change. The metric holds: RMSE on ug/l is computable on every fold, and within a fold it ranks models exactly as Zhou's R² on ug/l would. The reason cites MET-5 wrongly, and the curator should weigh how strongly bloom bins dominate it.

All numbers come from untuned LightGBM (400 trees, the builder's settings) on the 9 shipped day-grouped splits of the current definition, unless a row says otherwise. Scripts and outputs: the claim auditor's scratch folder in the run (a1_counts.py to a6_floor_date.py).

**Claims table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | "No source names this use" (virtual sensor) | task_summary.use_case, CC bullet 1 | read the descriptor's full text (Europe PMC PMC12197977) and Zhou et al. 2026 | holds | descriptor: uses are trends, toxin limits and early warning "for toxic algal blooms" (Value of the Data, quote verbatim); no model; Zhou: a cross-dataset benchmark | USE-1, EV-2 |
| 2 | 180 casts, two stations, May 2014 to Dec 2023, 31 to 52 bins per cast | task_summary.row | counts on the raw sheet | holds | 145 Mendexa-Control + 35 Mussel Farm; 2014-05-20 to 2023-12-18; 31 to 52 bins; no repeated pressure in a cast | EV-1 |
| 3 | shipped as log, scored on ug/l | task_summary.predicted, metric | `scorer(container)` against a manual RMSE of exp values, per fold | holds | identical on all 9 folds (e.g. 0.7314 / 0.7314) | MET-3 |
| 4 | known at prediction time: depth, T, S, density, LT, PAR, DO, station, date, time | task_summary.known | `feature_columns(container)` | holds | 11 features; oxygen saturation is shipped but not named in `known` (wording only) | LEAK-10 |
| 5 | whole survey days held out with both stations; neighbouring weeks in training | task_summary.split, splits_comment | day overlap per fold; days from each test day to the nearest training day | holds | 0 overlapping days in 9 folds; 48-49 test days; nearest training day median 16 days, p90 36, max 84 | SPLIT-24 |
| 6 | rebuilt from AZTI, -999 to missing, one bin dropped, day groups | task_summary.changes | read `_clean`, raw counts | holds | see rows 18-19 | PROV-13, CLEAN-10, CLEAN-15 |
| 7 | R^2 0.06 without the date, 0.45 with it (log scale) | fit_reason | rerun the ablation | holds | 0.0582 and 0.4513, reproduced exactly | EV-1 |
| 8 | the date's skill is "filling between the surveys before and after" | fit_reason | the date without the channels, and a no-model profile of the neighbouring training days | **refuted** | neighbouring training days' profile at the same depth (no model): R^2 0.040; LightGBM on date + depth + station: 0.106; channels + depth without the date: 0.037; all together: 0.451. It is the combination that carries the skill, not interpolation | EV-1, USE-8 |
| 9 | trained on past years only, R^2 > 0 in one of three years | fit_reason, CC Note | rerun 2021-2023, add 2019-2020 | holds (selective) | 0.099, -0.305, -0.352 reproduced; 2019 0.023, 2020 0.140: R^2 > 0 in 3 of 5 years | EV-8 |
| 10 | "Light transmission and PAR carry the rest" | fit_reason | ablation | holds, partly | without both 0.451 to 0.220; T, S and O2 add too (with the date 0.220 against 0.106-0.134 for date + depth + station ± time) | TP-4 |
| 11 | fit approximate | fit | USE-8 reading | holds | no actor in any source; a "for example" virtual sensor | USE-8 |
| 12 | year 2025; v2 of 2025-05-23 left this table unchanged | `year` comment | Mendeley public API, files of v1 and v2 | holds | Hydrographic_variables.xlsx has sha256 d7a00558... in both versions, created 2025-03-26; only the phytoplankton file changed | PROV-9 |
| 13 | source Other; Zhou's GitHub table is a copy | `source` | Zhou's repo tree | holds | `data/data_raw/Hydrographic_variables.xlsx`, 722,245 bytes, the same size as AZTI's file | PROV-8 |
| 14 | CC BY 4.0 on Mendeley; the article is CC BY-NC | `license` | Mendeley page; article XML | holds | page: CC BY 4.0; XML `<license>` by-nc/4.0 (a note only, EV-4) | EV-4 |
| 15 | sha256 d7a00558... | download_description | sha256sum of the local file | holds | d7a0055833608a1e4fedf450c5960f06f98f952d90dbf2b6c13f1b509c788770 | PROV-13 |
| 16 | 8,195 bins of 180 SBE-25/25plus casts; per-station counts and dates | CC intro | raw counts; descriptor Sec. 4.2 and Data Description a) | holds | 8,195 rows; "145 CTD profiles ... (from 20/05/2014 to 18/12/2023) ... 35 ... (from 17/02/2021 to 18/12/2023)" | EV-2 |
| 17 | the descriptor names no use beyond trends and the early-warning sentence | CC bullet 1 | full text | holds | quote found verbatim | USE-1 |
| 18 | Zhou's IQR filter keeps 4,653 bins of 132 casts and cuts the bloom values | CC bullet 2 | reran Zhou's `configs/config.yaml` QC and `detect_outliers` (IQR on every numeric column) on the raw file | holds | exactly 4,653 rows and 132 casts; chlorophyll max 1.47 against 11.13; new detail: the filter also drops every Mussel Farm row (the IQR of latitude is 0) | PROV-13, PROV-15 |
| 19 | -999 counts: PAR 297, salinity and sigma-theta 95, T, DO and O2 sat 47, LT 1, the time of 1 cast | CC bullet 3 | `(raw == -999).sum()` | holds | exact; the time code is 45 bins of Mendexa-Control 2016-04-15; the dropped bin (2017-09-04, 39 dbar) is -999 in every channel | CLEAN-10, CLEAN-15 |
| 20 | min 0.03 holds 3.5%, p05 0.06, median 0.43, max 11.13 | CC bullet 4 | quantiles | holds | 3.50%, 0.06, 0.43, 11.13 | EV-1 |
| 21 | the 0.03 minimum is "the low end of a continuous spread" | CC bullet 4 | value counts at the low end; by year and cast; sample profiles | **refuted** | 287 bins at 0.03 against 37 at 0.04, 52 at 0.05, 44 at 0.06 (a pile-up 7.8 times the next value); only in 2018-2022 (0 in 2014-2017 and 2023); in 25 casts, with runs of up to 36 consecutive bins at exactly 0.03 (Mendexa-Control 2022-01-18: 0.66 at 1 dbar to 0.09 at 12 dbar, then 0.03 to 48 dbar in a mixed column at 13.45-13.50 °C). A reporting floor (left-censored values), not a tail. "No two-regime zero" still holds under the curator's definition (3.5% against 1.9% is not "by far") | EV-1, EV-2 |
| 22 | 34 of 35 Mussel Farm casts share a day with Mendexa-Control "about 1.5 km away" | CC bullet 5, grouping | day-station table; haversine on the descriptor's coordinates | **refuted** (distance) | 34 of 35 holds; the distance is 1.82 km (43.356850, -2.448633 against 43.342229, -2.438329) | writing |
| 23 | same-day neighbour tells a held-out cast's chlorophyll: 0.705 by cast against 0.369 by day (two-cast days); 0.550 against 0.461 (all rows) | CC bullet 5, grouping | reran on the current definition (GroupKFold over permuted ids, 3 x 3) | holds, numbers stale | current: 0.641 against 0.348 and 0.525 against 0.439; the other station's value at the same day and depth alone: R^2 0.736, Pearson 0.88 (1,218 pairs). The builder's script reads a `cast` column the current definition lacks (an earlier version; EV-8) | SPLIT-24, EV-8 |
| 24 | "A failed fluorometer or a survey without one lacks both casts of the day" | CC bullet 5 | the times of the two casts of a day | untested | circumstantial support only: the casts are 8 to 94 min apart and never at the same time (34 days), consistent with one boat and one CTD; no source names the instrument per cast | EV-6, EV-7 |
| 25 | `survey_day` is never a feature; a test day is never in training | CC bullet 5, warning | `feature_columns`; overlap per fold | holds | not among the 11 features; 0 overlap | LEAK-16 |
| 26 | lat, lon and datum are one value per station | CC bullet 6 | nunique per station | holds | 1, 1, 1 per station | CLEAN |
| 27 | optical ablation 0.451 / 0.319 / 0.377 / 0.220 | CC bullet 7 | rerun | holds | 0.4513 / 0.3192 / 0.3771 / 0.2196 | TP-4 |
| 28 | whether a fluorometer-less platform carries LT and PAR is not known | CC bullet 7 | none possible on the data | untested | the descriptor lists LT, PAR and chlorophyll as channels of the same SBE-25 profiles; nothing on other platforms | EV-7 |
| 29 | Note: the date carries the skill, "so models fill a held-out day from the surveys around it rather than read chlorophyll off the other channels" | CC Note 1 | date split into season and time; the time at several resolutions; within-year LT relation | **refuted** (the 0.058 holds) | the season adds nothing: dropping the year and keeping day-of-year gives 0.037, dropping day-of-year and keeping the year gives 0.455. Year as a category 0.369, half-year 0.397, continuous date 0.455. Within-year Spearman of log chlorophyll with LT runs from -0.58 (2017) to +0.16 (2019), and the per-year slope changes sign. Without the 0.03 bins: all features 0.420, no date -0.037. The models read chlorophyll off the channels through a mapping that drifts in time | EV-1, USE-8 |
| 30 | Note: "a virtual sensor for future casts has little signal across time" | CC Note 2 | temporal variant 2019-2023 against the past years' constant | partly refuted | R^2 within the year at most 0.14, but against the training years' constant the model wins in 4 of 5 years: log RMSE 1.079/1.211, 0.937/1.296, 0.948/1.010, 1.008/0.899, 0.866/0.987; ug/l 0.614/0.667, 0.401/0.429, 0.604/0.679, 0.359/0.274, 0.703/0.824. Without `cast_year`, 2019 and 2020 fall to -0.44 and -0.40: the newest calibration matters | EV-8, SPLIT-3 |
| 31 | sigma-theta comes from T, S and p; O2 saturation from DO, T and S | CC Note 3 | cubic fits | holds | sigma-theta R^2 0.999999 (max residual 0.0027 kg m-3); DO / saturation from T and S, R^2 0.99975 | CLEAN |
| 32 | "146 days: 112 with one cast at Mendexa-Control, 34 with a cast at each station" | grouping.definition | day-station table | **refuted** | 111 Mendexa-Control-only days, 1 Mussel-Farm-only day (2022-03-08), 34 with both | writing |
| 33 | R^2 0.939 on random rows against 0.493 by cast | grouping.definition | the builder's group probe output (cast-grouped run) | holds | 0.939 against 0.493; the day-grouped run gives 0.942 against 0.423 | SPLIT-29 |
| 34 | "the curator's brief asked for a split by cast (2026-10-30)" | grouping.definition | searched the record, the run's decision register and the run folder | untested | not found: the CC line says only `Yes`, priority 1; the AI screening proposed "grouped by cast or temporal" | EV-7 |
| 35 | grouped rather than temporal: the use case fills surveys within the record | splits_comment | SPLIT-3 reading; rows 23, 29 | holds | the drift in row 29 argues for calibrating on the surrounding surveys, which a day-grouped split gives | SPLIT-3, SPLIT-4 |
| 36 | the source fits no model; Zhou ranks by R^2 "for cross-dataset comparability" on a filtered copy | metric reason | descriptor full text; Zhou Sec. 2.4 (PLOS ONE); Zhou's config | holds | "For cross-dataset comparability, we use the coefficient of determination (R²) as the primary benchmark indicator"; Zhou also reports MAE, RMSE, NRMSE, NSE and event F1; "we did not apply any additional target transformations" (R^2 on ug/l) | MET-1, MET-11 |
| 37 | the rejection of Zhou's R^2 rests on MET-5 | metric reason | MET-5 text | **refuted** (wrong rule) | MET-5 accepts a paper's metric when the paper "names it as the criterion it ranks" by, and Zhou does. The rejection rests on MET-1 (chosen to compare datasets, not for this decision) and MET-2 (Zhou's task cut the blooms and Mussel Farm and split by time). Within a fold, R^2 on ug/l = 1 - MSE/Var(y_test) ranks models exactly as RMSE on ug/l does (MET-11 identity), so the label changes no ranking | MET-5, MET-11 |
| 38 | RMSE is computable per row on every fold | metric | `scorer` with a dummy per fold | holds | no scoring columns needed; dummy (exp of the training mean log) 0.425 to 0.731 ug/l; 2,621 to 2,816 test rows and 48-49 days per fold | MET-2 |
| 39 | scored on ug/l, the scale the task means | metric, target_transform | retransformation; error concentration | holds; a weighing item | Duan smearing moves LightGBM from 0.4759 to 0.4749, and a model fitted on ug/l is worse (0.5028), so shipping the log is harmless. The top 1% of true values carry 40% of the squared error and the top 5% carry 65%: the metric mostly scores bloom bins. On the log scale the censored 0.03 bins would carry 21% (0.6% on ug/l). Field practice for chlorophyll often scores log-space errors (Seegers et al. 2018, unverified: full text not read) | MET-3, MET-10 |
| 40 | `dataset_duplicate_columns` (cast_date, survey_day): survey_day is the group key, never a feature | warning proposed for acceptance | feature list; overlap | holds | see row 25 | SPLIT-24 |
| 41 | probes: none flagged, LightGBM R^2 0.450, beats the dummy 5/5, group probe 0.942 against 0.423, no generated flags | builder report | read the probe files | holds | the builder's task, group and generated probe outputs | EV-3 |
| 42 | screening: Zhou is a derivative with 4,653 rows of 132 casts and 11 predictors; the release has 145 + 35 profiles from SBE-25/25plus | record screening block | as rows 16 and 18 | holds | reproduced | PROV-8 |
| 43 | Assessment (2026-10-30): the 0.03 minimum "is the low end of a continuous spread ... not a regime of its own" | record | as row 21 | **refuted** (reason only) | a floor, 2018-2022 only; the tag removal stands | EV-2 |
| 44 | `original_source: Github` | record frontmatter | PROV-8 | **refuted** | the first publication is the Mendeley release (v1 2025-03-26); the builder proposes `Other` | PROV-8 |
| 45 | implied: every feature is known at the prediction point | the definition | channel provenance (descriptor Sec. 4.2) | holds | every channel is measured in situ by the same profiler; sigma-theta and O2 saturation come from known channels (row 31); none derives from chlorophyll | LEAK-10 |
| 46 | implied: no row is a copy across the split | the definition | exact feature copies per fold, with and without the date | holds | 0.0% in all 9 folds | LEAK-16 |
| 47 | implied: the split leaves no near-adjacent survey days | the definition | gaps between consecutive survey days | holds | median 20 days; one pair within 3 days (2022-03-08 Mussel Farm only, 2022-03-10) | SPLIT-24, SPLIT-30 |
| 48 | implied: the target is the real-world target, the same quantity throughout | the definition | rows 21 and 29 | holds, with a concern | the target is the fluorometer's reading, which is what a virtual sensor fills; but the reading is not uniform over time (the floor only in 2018-2022, the LT relation changes sign by year) | USE-5, PROV |

**Refuted and untested claims, ranked (principles.md: validity first, Must first)**

1. **The date mechanism (rows 8, 29; P3, USE-1 and USE-8 through draft issue 1).** The notes and `fit_reason` say the models fill a day "from the surveys around it rather than read chlorophyll off the other channels". The data says otherwise. Profiles from the neighbouring days score R^2 0.040, and date + depth + station score 0.106. The channels without the date score 0.037 to 0.058, and everything together scores 0.451. The season contributes nothing. What it changes: draft issue 1 frames the choice as "interpolation between surveys or No Good Target". The measured reading is a virtual sensor whose calibration drifts and that is recalibrated on nearby surveys, which is the stated use case and the reason for the day-grouped split. The fit stays approximate, but for the right reason. Mildest remedy: rewrite the Note and `fit_reason` with this decomposition. Nothing in the data or the split changes.
2. **"Little signal across time" is overstated (row 30; P4, SPLIT-3, through draft issue 1).** Against the constant an operator would have from past years, the model wins in 4 of 5 years on both scales. Within-year R^2 stays low (at most 0.14). What it changes: the temporal variant is weaker than the grouped task, but it is not empty. The weighing in issue 1 should use the five years and the past-years baseline. Mildest remedy: add those numbers to the Note.
3. **The 0.03 floor (rows 21, 43; P5 and P7).** It is a reporting floor in 2018-2022 (287 bins against 37 at 0.04), not a continuous tail. What it changes: the target note and the record's Assessment. The tag removal stands. The declared metric barely sees these bins (0.6% of the squared error on ug/l). The log-scale R^2 behind the builder's decisions carries 21% from them, but every decision survives without them (row 29). Mildest remedy: say in the notes "values at or below 0.03 ug/l are reported as 0.03 (a floor in 2018-2022, 25 casts)" and keep the bins.
4. **The metric reason cites MET-5 (row 37; P6).** MET-5 would accept Zhou's R^2, because Zhou names it as the criterion it ranks by. The rule that rejects it is MET-1/MET-2 (a choice made to compare datasets, on a task that cut the blooms and Mussel Farm). What it changes: the reason's rule IDs. The scored quantity stays: RMSE on ug/l already ranks models as Zhou's R^2 on ug/l would within a fold. Mildest remedy: cite MET-1 and MET-2, list Zhou's other reported metrics, and name the identity. Separately, a weighing call for the curator (MET-10): RMSE on ug/l puts 40% of the error in 1% of the bins (blooms). A log-scale error would match common chlorophyll practice but would load the censored floor. Keeping ug/l is defensible.
5. **Small factual slips (rows 22, 23, 32, 44; P7 and writing).** The distance is 1.82 km, not about 1.5 km. The days split as 111 Mendexa-Control-only plus 1 Mussel-Farm-only (2022-03-08), not "112 with one cast at Mendexa-Control". The cast-against-day numbers come from an earlier version: currently 0.641 against 0.348 and 0.525 against 0.439 (EV-8). `original_source` should be `Other` (PROV-8). Mildest remedy: correct the text and the record field.
6. **Untested (rows 24, 28, 34).** (a) That one instrument serves both casts of a day: the casts are 8 to 94 min apart, which supports it circumstantially; a question for AZTI or the curator. (b) Whether a fluorometer-less platform carries LT and PAR: the data cannot answer it. (c) "The curator's brief asked for a split by cast (2026-10-30)": I found it nowhere in the repository or the run folder; the main session should cite where it is or drop the clause.

</details>

<details><summary>Column audit</summary>

**Column auditor: basque_offshore_ctd_chlorophyll (2026-11-01)**

**Verdict:** no leak in any column. One column needs the curator's call on the framing (`cast_date`), the target carries a level shift across 2018-11 to 2022 that is probably the instrument (circumstantial), and one comment bullet misdescribes the target's low end. The rest is fine or needs a note.

```text
Verdict: ship after changes (wording), with two calls for the curator.
Validity: USE-1/USE-3 question on cast_date (retrospective gap-filling or time-independent virtual sensor; precedents
  disagree); USE-5/PROV-13 question, a target level shift 2018-11..2022 (maybe the fluorometer, EV-6); LEAK-10 holds for
  every column (nothing post-outcome, no missingness that encodes the target, no id that encodes the label); LEAK-33
  holds (survey_day is split metadata only).
Value: not audited here (TP rules: probes and builder).
Quality: the floor at 0.03 is a clamp, not "the low end of a continuous spread" (LEAK-26 by analogy: document it);
  -999 counts given before the all-sentinel row leaves; CLEAN-10, CLEAN-5, CLEAN-14 hold.
For the curator: issue 1 (the date: which half of the use case), issue 2 (the level shift: note, ask AZTI, or No Good Target).
```

How I checked: the frame loaded through `dataset_io.from_definition` (8,194 x 13); the raw workbook with its Notes sheet
(the only codebook: one line per column, "NO DATA is indicated by -999"); the Data in Brief descriptor in full (Europe PMC
PMC12197977), which says only that the channels "were measured in situ using Sea-Bird SBE-25 and 25plus CTD instruments"
(Abstract; Sec. 4.2) and gives no fluorometer model, calibration or instrument dates. Experiments: untuned LightGBM with
the builder's settings on the 9 shipped day-grouped splits, R^2 on the log scale and RMSE in ug/l. Scripts in
the column auditor's scratch folder in the run (`date_decomp.py`, `date_decomp2.py`, `era.py`, `derived.py`, `profile_feats.py`,
`raw2.py` to `raw5.py`).

**Column table**

| column | meaning (Notes sheet unless stated) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `station` | station code: Mendexa-Control (145 casts) or CTD-Mussel Farm (35, only 2021-02 to 2023-12) | yes | category, 2 levels; latitude, longitude and datum are one value per station (checked), dropped as copies | fine | CLEAN-5, CLEAN-14 |
| `pressure_dbar` | pressure relative to the surface, the 1-dbar bin | yes | int64, 1 to 52; every cast starts at 1, no gaps, no repeated bins; the cast's last bin is the bottom depth (Mendexa 43-52, Mussel Farm 31-40) | fine | |
| `temperature_c` | in situ temperature, ITS-90 | yes | float; -999 to missing, 46 shipped rows (whole cast 2023-12-11); 11.72 to 24.14 | fine | CLEAN-10 |
| `salinity_pss78` | practical salinity | yes | float; -999 to missing, 94 rows (whole casts 2023-03-06, 2023-12-11); minimum 32.46 at 1 dbar on plume days (2015-03-12, 2020-06-01): unusual, real | fine | CLEAN-10, CLEAN-11 |
| `sigma_theta_kg_m3` | density from potential temperature, salinity, p = 0, minus 1000 | yes (computed from T, S) | float; matches EOS-80 of (T, S) within 0.0035 kg m-3 in every row; missing exactly where salinity is | fine, derived copy the source ships (noted in the definition) | CLEAN-5 does not apply (not an exact copy) |
| `light_transmission_pct` | "Light transmittance (%)" (beam transmissometer; wavelength and path not stated) | yes when the fluorometer failed; unknown for a platform without a fluorometer | float; its one -999 is in the all-sentinel row that leaves, so no missing values ship; whole-cast lows (2023-03-13: 57-61% at every depth) unusual, kept | question (platform), as the builder raised | USE-3, USE-6; CLEAN-11 |
| `par_umol_m2_s` | photosynthetically active radiation | yes; same platform question | float; -999 to missing, 296 rows in 64 casts, mostly the top bins (median 3 dbar), two whole casts (2015-06-01, 2016-10-17); missingness follows depth, not the target (missing-indicator probe flat) | fine, with a note: part of its signal is the fluorometer's daylight quenching (issue 4) | CLEAN-10; USE-5 note |
| `dissolved_oxygen_ml_l` | dissolved oxygen, ml/l | yes | float; -999 to missing, 46 rows (whole cast 2017-09-04, two bins 2015-01-26) | fine | CLEAN-10 |
| `oxygen_saturation_pct` | oxygen saturation, % | yes (computed from DO, T, S) | float; matches Weiss (1970) of (DO, T, S) within 1.8 points; present on 94 rows where AZTI set T or S to no data (2023-03-06, 2023-12-11), values plausible | fine; minor note (issue 6) | CLEAN-11 |
| `cast_date` | UTC date of the cast (`UTC DATE (YYYYMMDD)`) | its value yes; its skill comes from same-year surveys around the test day | datetime64 `%Y-%m-%d`, parsed correctly | question for the curator (issue 1) | USE-1, USE-3, SPLIT-3; precedents infrared_thermography_temperature, wadden_sea_sibes_macoma_abundance |
| `survey_day` | the group: the cast date as text | not a feature | string; excluded by `feature_columns` (group column); the `dataset_duplicate_columns` warning (`cast_date`, `survey_day`) is this copy: fine to accept | fine | LEAK-33 |
| `time_of_day_utc_h` | UTC time of the cast as a decimal hour | yes | float from hhmmss; no minute or second at 60 or above, 6.62 to 15.22 h; -999 to missing for one cast (2016-04-15, 45 rows); dropping it changes R^2 0.451 to 0.448 | fine (the decimal-hour form follows infrared_thermography_temperature's `TimeOfDay`) | CLEAN-10, CLEAN-12 |
| `log_chlorophyll_a_ug_l` | target: fluorometer chlorophyll-a, ug/l, natural log; scored in ug/l | target | float; the one -999 bin dropped; 2-decimal resolution in ug/l; a floor at 0.03 (287 bins against 37 at 0.04 and 52 at 0.05), all from 2018-11-19 to 2022-09-12 | cleaning/wording problem (issue 3) and a question on its scale over time (issue 2) | CLEAN-15, CLEAN-16; LEAK-26 by analogy; USE-5, PROV-13 |

No column records anything after the target: the target is a reading taken at the same instant as the inputs, so the
LEAK-10 question is only whether the inputs exist when the fluorometer reading does not, and they do. No missingness
encodes the target (the missing-indicator probe is flat; every -999 run is a whole cast or the top bins). No id
remains: the dropped coordinates are station copies, the dropped date and time are rebuilt. 0% of test rows have an
exact copy in train.

**Problems, ranked**

**1. `cast_date`: which half of the use case (P3; USE-1, USE-3, SPLIT-3; a question, Must-level framing).**
The use case has two halves: AZTI "fills a profile whose fluorometer failed" (a past cast of a measured record: the
surveys after the test day exist when the gap is filled) and "estimates chlorophyll for a cast made without one" (a
platform or period without a fluorometer: the later surveys and the year's level are not known). The date serves only
the first. What the date carries, measured (9 shipped splits, R^2 log scale / RMSE ug/l):

| features | R^2 log | RMSE ug/l |
|---|---|---|
| shipped, no date | 0.058 | 0.552 |
| + day of year only (season) | 0.037 | 0.551 |
| + year only (an integer) | 0.365 | 0.500 |
| + year and day of year | 0.377 | 0.498 |
| + continuous date (as shipped) | 0.455 | 0.477 |

The season adds nothing; about three quarters of the date's gain is the year's level, the rest the surveys of the
neighbouring weeks. So the benchmark, as shipped, scores how well a model reads a year's chlorophyll level off that
year's other surveys; the channels themselves give R^2 0.06 (0.14 with a profile view of the same cast, issue 7). This
refines the `fit_reason` ("filling between the surveys before and after"): mostly the year, not the neighbouring weeks.
Precedents pull both ways: infrared_thermography_temperature, a calibration "independent of time", drops `Date`
(Lennart, 2026-10-21: "learn a function that is independent of time ... no real signal across time");
wadden_sea_sibes_macoma_abundance keeps the date for mapping a surveyed year between stations (Andrej, 2026-10-30).
Mildest remedy: (a) keep `cast_date` and narrow the use case to filling past casts of AZTI's record (drop "a cast made
without one" from `use_case` and the prediction-point bullet), and say in `fit_reason` that the skill is the year's
level; or (b) drop `cast_date` for a time-independent virtual sensor, which leaves R^2 0.06 and hands the dataset to
the TP rules. A consistency check is due either way: (a) differs from infrared by the gap-filling framing, (b) follows it.

**2. The target's level shifts in 2018-11 to 2022 (P3/P5; USE-5, PROV-13, CLEAN-21; circumstantial, "maybe an
instrument era", EV-6).** Evidence: the floor value 0.03 occurs in 0 of 2,867 bins from 2014-05 to 2018-10, in 6.7% of
4,277 bins from 2018-11 to 2022 (25 casts), and in 0 of 1,050 bins in 2023. Below 10 dbar, log chlorophyll against
light transmission has slope -0.038 (2014-2018), +0.009 (2018-11 to 2022) and -0.027 (2023): the expected sign (more
particles, more chlorophyll) vanishes in the middle period, and at 85% transmission the fitted chlorophyll is 0.58, 0.30
and 0.64 ug/l. Whole winter casts sit at the floor (2021-01-12 median 0.03; 2022-01-18 median 0.03 at Mendexa and 20 of
35 bins at Mussel Farm), where January elsewhere in the record reads 0.21-1.38. The descriptor names "SBE-25 and 25plus"
with no dates or calibration, so the cause cannot be read from the source; real interannual change is not ruled out.
If it is the instrument, the year effect of issue 1 is largely a model learning the fluorometer's calibration era, and
the shipped target is not one scale of chlorophyll across the record. Side finding: the floor hits both casts of
2022-01-18, 2022-08-01 and 2022-09-12, which supports one instrument serving both casts of a day (the builder's "cannot
verify"), and so the day grouping. Mildest remedy: ask AZTI for the CTD and fluorometer history and calibrations
(repair from the origin, PROV-13); until then a note in the curation comments and `fit_reason` with these numbers; the
curator weighs whether the fluorometer reading is what the actor acts on (USE-5), next to the record's marker
`No Good Target (yet)`. The test that would settle it: the instrument log, or bottle chlorophyll matched to the casts
(not in the release).

**3. The floor at 0.03 is a clamp, and the bullet says otherwise (P7 / writing; LEAK-26 by analogy, a floor instead of
a cap; Should).** The target bullet calls 0.03 "the low end of a continuous spread (5th percentile 0.06, median 0.43)".
The counts say a clamp: 287 bins at 0.03, 37 at 0.04, 52 at 0.05, 44 at 0.06, nothing below 0.03, all in 2018-11-19 to
2022-09-12. The two-regime-zero conclusion stands (the curator's definition needs the low value to be by far the most
frequent and independent of the rest; this is a reporting floor of one period). Effect on the metric is negligible
(a clamped bin is off by at most 0.03 ug/l), but on the shipped log scale it is a spike at -3.51. Mildest remedy:
rewrite the bullet: "0.03 ug/l is a floor: 287 bins (3.5%) sit at it against 37 at 0.04, all between 2018-11 and
2022-09 (values at or below 0.03 reported as 0.03); no two-regime zero; the maximum is 11.13."

**4. PAR's signal is partly the fluorometer's daylight quenching (P3 note; USE-5; Weigh).** In the 62 casts whose top
12 dbar are mixed (sigma-theta difference under 0.05), the ratio of chlorophyll at 1-3 dbar to 8-12 dbar falls with PAR
at 4-6 dbar (Spearman -0.65, p < 1e-7; median ratio 0.64 above median PAR, 0.89 below). The surface readings are low in
bright light, a property of the sensor (non-photochemical quenching), not of the water; PAR and the time of day predict
it. Not a leak (both are known), and `predicted` already says "the fluorometer's chlorophyll-a". Mildest remedy: one
sentence in the optical-channels bullet.

**5. Light transmission and PAR on a platform without a fluorometer (P3; USE-3; a question).** I concur with the
builder's issue 3 and the bullet as written; no new evidence. If the curator takes remedy 1(a) (past casts with a failed
fluorometer), the package that carried the fluorometer carried both channels and the question goes away.

**6. Oxygen on two casts whose T and S are flagged (P7; CLEAN-11; note at most).** Dissolved oxygen and oxygen
saturation, both computed with temperature and salinity, are present on 2023-03-06 (salinity flagged) and 2023-12-11
(temperature and salinity flagged), 94 rows; values look plausible (2023-12-11 saturation median 95.5 against 96.7 a
week later). Keep as AZTI ships them; no change needed.

**7. The -999 counts are raw (writing; minor).** The bullet's counts include the one row that is -999 in every channel
(2017-09-04, 39 dbar), which leaves with the target, so "light transmission 1" refers to a row that is not shipped. In
the shipped frame: PAR 296, salinity and sigma-theta 94, temperature, oxygen and saturation 46, light transmission 0,
the cast time 45 rows (one cast). Mildest remedy: say "in the raw table" or give the shipped counts, and name the
all-sentinel row.

**Checked and nothing to change:** a profile view of the same cast (PAR attenuation from the cast's shallowest PAR,
transmission anomaly and cast median, stratification against the surface bin, the cast's bottom depth; known under
context `all_rows`, CLEAN-19) raises R^2 without the date from 0.058 to 0.137 but leaves RMSE in ug/l at 0.552, and with
the date changes nothing (0.467 against 0.455): not worth building. Sigma-theta and oxygen saturation are consistent
with their inputs. The time parse is correct. No proxy codes other than -999 (no 0, -99 or 9999 runs; PAR minimum 0.01,
maximum 1,383.8 near the surface on 2016-06-07).

</details>

<details><summary>Split audit</summary>

**Split auditor (2026-11-01): basque_offshore_ctd_chlorophyll**

**Verdict: right with notes.** The split holds out whole survey days. That is the right regime for one use: filling in a survey whose fluorometer failed, in a series that is otherwise measured. The release backs the single-day unit. Every whole-cast channel failure in it (5 casts) is a single survey. The group key is exact, and no other hidden group crosses the split.

There are two problems with the text:
- The use case names a second use, a cast made without a fluorometer. The split does not test that use, and under a temporal split it has no signal.
- The reason given for widening the group from cast to day ("a failed fluorometer lacks both casts of the day") is partly contradicted by the data. Whether to hold out the day or the cast is a weighing call for the curator.

```text
Validity: USE-1 / SPLIT-3 (one use case, one regime): the use_case text names two uses; the split mirrors only the
  archive gap-filling one (temporal R^2 -0.19): narrow the text, no re-split.
  SPLIT-1 (the unit held out, day or cast): the day is defensible and stricter, but its stated reason is not shown
  (2023-12-11: one station's cast lost T and S, the other's did not): curator's call; reword.
  SPLIT-1 (gap length): holds; the release's channel failures are single surveys; state the assumption.
  SPLIT-23/24 hold (exact date key, 146 groups, no day on both sides of any of the 9 splits); SPLIT-29/30 hold (no
  hidden group but the known one); SPLIT-28 not triggered (random forest 0.33, LightGBM 0.45 R^2 on unseen days).
Quality of the text: fit_reason, splits_comment and two counts need small corrections (issue 4, 5).
For the curator: issue 2 (hold out the day or the cast).
```

**Where the numbers come from.**
- The model is untuned LightGBM, the builder's configuration: 400 trees, learning rate 0.03, 2 threads. The cast date enters as day of year and fractional year.
- The frame is rebuilt from the definition through `dataset_io.load(..., built=False)` (origin `rebuilt`, 8,194 rows).
- R^2 is on the shipped log scale. RMSE is in ug/l, the metric's scale.
- Two runs with identical features differ by about 0.015 R^2 (column subsampling), so differences that small are noise.
- Scripts and outputs are in the split auditor's scratch folder in the run: `describe.py`, `split_variants.py` (and `.csv`), `date_role.py`, `missing_runs.py`, `fold_density.py`, and the hidden-group runs.

| Split | R^2 log (se) | RMSE ug/l | train-mean RMSE |
|---|---|---|---|
| Shipped: day-grouped, 3 x 3, all features | 0.451 (0.013) | 0.476 | 0.587 |
| Shipped, date as fractional year only | 0.455 (0.014) | 0.477 | 0.587 |
| Shipped, date as day of year only | 0.037 (0.053) | 0.551 | 0.587 |
| Shipped, no date | 0.058 (0.036) | 0.552 | 0.587 |
| Shipped, no model: nearest earlier and later training survey at the same depth, interpolated in time | 0.028 (0.045) | 0.591 | 0.587 |
| Shipped, minus training days within 7 / 15 / 30 days of a test day (93% / 73% / 46% of the training rows kept) | 0.442 / 0.270 / 0.129 | 0.485 / 0.516 / 0.553 | 0.589-0.591 |
| Day-grouped, 10 folds x 2 (a single failed survey, nearly all its neighbours measured) | 0.486 (0.030) | 0.442 | - |
| Blocks of 6 consecutive survey days (about 4 months), 3 x 3 | 0.309 (0.038) | 0.520 | 0.588 |
| Leave one calendar year out (10 folds) | 0.067 (0.113) | 0.523 | 0.578 |
| Temporal: train on the years before 2021, 2022, 2023 | -0.186 (0.117) | 0.555 | 0.565 |
| Cast-grouped, 3 x 3 (builder's cast-against-day probe) | 0.550; on casts of two-cast days 0.705 (0.369 by day) | - | - |

**1. USE-1 (P3) and SPLIT-3, SPLIT-1 (P4), Must: the use case names two uses, and the split mirrors one.**
- Evidence:
  - `task_summary.use_case` reads: "fills a profile whose fluorometer failed, or estimates chlorophyll for a cast made without one". `question` reads: "read from the profile's other sensor channels".
  - The split keeps the surveys before and after a test day in training:
    - In the 9 shipped splits, a test day has its previous survey in training 70.1% of the time, its next one 70.1%, both 48.4%, and neither 8.2%.
    - The nearest training survey is a median of 16 days away (IQR 13-27, max 84).
  - All of the date's skill is the position in the record. The fractional year alone gives 0.455, the day of year alone 0.037, and no date 0.058.
  - Variance of log chlorophyll:
    - 55% lies between survey days.
    - The calendar month explains 5.5%, so there is almost no seasonal signal.
    - The year-month explains 49.6%.
  - So the score measures filling a day from the surveys around it, with the cast's channels read against that period:
    - date with depth, station and time only: 0.144;
    - adding light transmission and PAR: 0.386;
    - adding temperature, salinity, sigma-theta and oxygen instead: 0.223;
    - all features: 0.465;
    - channels without the date: 0.058.
  - "A cast made without one", now or later, is a forward use. Its split is temporal, and there the task has no signal:
    - R^2 0.10, -0.30 and -0.35 for 2021, 2022 and 2023 (reproduced; mean -0.186);
    - RMSE 0.555 ug/l against 0.565 for the training mean (mean of the three years);
    - a whole year left out: 0.067.
  - The splits_comment already reads the task as filling "surveys within the record, not future ones (SPLIT-3)". The use_case and question say more than that.
  - In the release, no cast lacks its fluorometer channel (one bin of 8,195). Five casts lack another channel entirely (issue 3). So the gap-filling use has no instance in this table. Whether AZTI's archive holds casts without chlorophyll cannot be verified, and it bears on P3 (for the domain practitioner).
- Rule: SPLIT-3 ("a task is one or the other, never both, and the use case decides which") and USE-1 (check every split choice against the written use case).
- Mildest remedy: text only, no re-split.
  - Narrow `use_case` to the archive use, for example: "fills a survey whose fluorometer failed, in the measured series, from the cast's other channels and the surveys before and after". Drop "or estimates chlorophyll for a cast made without one".
  - Change `question` from "read from the profile's other sensor channels" to "...from the profile's other channels and the surveys around it".
  - In `splits_comment`, replace "a temporal variant (...) is a candidate" with the measured result: no signal across years, so there is no variant to offer.

**2. SPLIT-1 and SPLIT-23 (P4), Must: hold out the day or the cast. The day is defensible, but its stated reason is not shown. A weighing call for the curator.**
- Evidence:
  - The day key is exact (SPLIT-24): the cast's UTC date as a string, 146 groups. No day falls on both sides of any of the 9 splits, and test folds hold 48-49 days.
  - It removes a strong shortcut. On the 34 two-cast days, carrying the Mendexa-Control value at the same depth predicts the Mussel Farm cast's log chlorophyll at R^2 0.736 (1,218 bin pairs). This is the builder's 0.705 against 0.369 seen directly.
  - The stated reason is "A failed fluorometer or a survey without one lacks both casts of the day" (curation_comments, "Group"). The release's own failures say otherwise for transient faults:
    - On 2023-12-11, the Mendexa-Control cast lost temperature and salinity in all its bins.
    - The Mussel Farm cast of the same day is complete.
    - That is the only whole-cast failure on a two-cast day.
  - A per-cast glitch leaves the other station's cast measured, and the cast split (the brief's literal ask of 2026-10-30) mirrors that. A survey-level outage (an instrument away for repair) is what the day split mirrors.
  - The difference touches 34 of 146 days (68 of 180 casts). Overall it is 0.550 by cast against 0.461 by day (builder).
- Rule: SPLIT-1 (the split mirrors the application) and SPLIT-23 (the use case decides what one prediction is and what is known about a new group). No source settles which failure mode is the use.
- Mildest remedy:
  - Keep the day. It is stricter, and no score rests on the other station's cast.
  - Reword the claim in curation_comments and `grouping.definition`, for example: "we hold out the day so the score does not rest on the other station's same-day cast (alone R^2 0.736); per-cast glitches occur too (2023-12-11)".
  - If the curator reads per-cast glitches as the use, group by cast instead (station plus date). The rest of this audit holds either way.

**3. SPLIT-1 (P4), Must: how long a gap the test stands for. Holds; the assumption should be stated.**
- Evidence:
  - The score depends on surveys within two to four weeks being measured:
    - a 7-day buffer costs 0.009;
    - a 15-day buffer drops it to 0.270, and a 30-day buffer to 0.129 (confounded with less training data);
    - blocks of about 4 months, with the training size unchanged, give 0.309.
  - The survey cadence is a median of 20 days (5th percentile 7, 95th 50; maximum 240, the gap of September 2015 to March 2016). The descriptor gives the same picture (Abstract): "Generally, surveys were conducted monthly or biweekly, with the exception of a seven-month gap between September 2015 and March 2016".
  - Five casts in the release lost a whole channel:
    - PAR on 2015-06-01 and 2016-10-17;
    - oxygen on 2017-09-04;
    - salinity on 2023-03-06;
    - temperature and salinity on 2023-12-11.
    Each is a single survey (runs of 1 per station), so a single held-out day matches how failures show in this programme.
  - The default 3 folds are slightly stricter than a single failure, where every other survey is measured: 10 folds give 0.486 against 0.449.
- Rule: SPLIT-1. No higher rule is at stake.
- Mildest remedy: a sentence in `splits_comment`: a gap of one survey, as every whole-cast channel failure in the release is; longer outages score lower (blocks of 6 surveys 0.31, a whole year 0.07).

**4. USE-8 (P3), wording only: the fit_reason understates where the skill comes from.**
- Evidence:
  - "Much of the skill comes from the date" should read: all of the date's skill is the year (0.455 with the year alone, 0.037 with the season alone).
  - The channels add skill only within a period. Per year:
    - the correlation of light transmission with log chlorophyll runs from -0.57 (2017) to +0.17 (2019);
    - the mean log chlorophyll runs from -1.61 (2020) to -0.38 (2017; 2023: -0.375).
  - A model trained on these splits has learned the periods of the record.
  - A question for the critic or claim auditor, inference only: two CTD models were used ("Sea-Bird SBE-25 and 25plus", dates not given). Level shifts this large may partly be fluorometer calibration. If so, the date stands for the instrument's period. This is a P5 question, not a split remedy.
- Rule: USE-8 (write the fit and its gap). The fit is already `approximate`, so only the wording changes.
- Mildest remedy: text in `fit_reason` and the curation_comments "Note".

**5. Small factual corrections in the split text (P4 documentation).**
- "about 1.5 km away" (curation_comments, `grouping.definition`): the raw file's station coordinates are 1.82 km apart.
- "146 days: 112 with one cast at Mendexa-Control, 34 with a cast at each station" (`grouping.definition`): the true split is 111 at Mendexa-Control only, 1 at Mussel Farm only (2022-03-08), and 34 with both.
- That Mussel-only day is 2 days before 2022-03-10. The two days fall on opposite sides in 4 of the 9 splits, but the two Mussel Farm profiles agree only at r^2 0.226 (mean absolute log difference 0.61, 34 depths). This is no shortcut, so there is no need to merge the days.

**Checked and holding.**
- Hidden groups: `hidden_groups.py --include-grouped` (a grouped task is skipped by default, so the builder has no output for it).
  - Its only hit is the known `survey_day`.
  - `time_of_day_utc_h` is a candidate, not a hit: 121 values for 180 casts, a near cast id, but known at the prediction point and never shared across days.
  - No composite keys.
  - Near copies change nothing: 33.9% of the rows sit in clusters, gap +0.005.
- `context="all_rows"` matches the use: the held-out cast's other channels are known. `prediction_unit="row"` and `labels="per_sample"` are right.
- Learnability across unseen days (the builder's day-grouped probe output): ridge 0.063, random forest 0.332, LightGBM 0.453, kNN -0.258. There is signal, so SPLIT-28 is not triggered.
- Precedent: `wadden_sea_sibes_macoma_abundance` holds out stations with their neighbours in training ("Grouped rather than temporal: the use case maps a surveyed year between stations"). This dataset is the same reading along time. It is the only definition in the collection grouped on a time unit, so the curator's call on issues 1-2 sets the precedent.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: basque_offshore_ctd_chlorophyll (2026-11-01)**

**The actor.** I am the AZTI scientist who runs the Mendexa CTD series. After each survey I hand the profiles, with the
phytoplankton counts and the biotoxin results, to the people who manage the shellfish area and to the mussel farm. They
use chlorophyll as a sign of food for the mussels and as an early warning of blooms (Solaun et al. 2025, Background
and Value of the Data). The prediction point: the fluorometer channel of a survey is missing, and the rest of the CTD
package worked.

**Fit: approximate (USE-8). I agree with the label but not with its reason.** The task matches a real but minor job:
filling in a survey whose fluorometer failed, using the other channels of the same casts. It stays approximate for
three reasons. No source names this job. The target is an uncalibrated fluorometer reading that daylight pushes down
near the surface (non-photochemical quenching). And the shipped split fills a held-out day using surveys made after
it, which only someone filling the archive later would have. It is not "none" (USE-2): virtual sensors for chlorophyll
are an established method in the field (SOCA-CHL, Sauzède et al.), and in real time the model clearly beats the fill I
would use today (point 3).

**1. Inputs at the prediction point**

- I have every shipped input when the fluorometer fails on a survey: depth, temperature, salinity, sigma-theta,
  oxygen, oxygen saturation, light transmission, PAR, station, date and time of day.
- The use case's second variant, "a cast made without one", does not match the shipped inputs. A fluorometer is the
  most common bio-optical sensor added to a CTD. A package that carries a transmissometer and a PAR sensor but no
  fluorometer is rare. That platform would usually have temperature, salinity and oxygen only, which gives R^2 0.22
  (builder, `TS_O2_depth_only`). The `curation_comments` bullet already says "Whether a fluorometer-less platform
  carries them is not known". I would drop that variant from `use_case`, or ship a separate variant without the
  optical channels.
- Inputs I would have that the table lacks:
  - the last measured profile of the series. The model sees it only through the date.
  - satellite surface chlorophyll on cloud-free days (Copernicus Marine ocean colour).
  - the daily 3D chlorophyll of the Copernicus Marine IBI biogeochemical model (NEMO-PISCES at 1/36 degree,
    IBI_ANALYSISFORECAST_BGC_005_004).

  The field's own virtual sensor takes satellite chlorophyll, PAR, the temperature and salinity profile and the day of
  year (SOCA-CHL). Adding these inputs would be a rebuild with outside data, not a fix. USE-6 allows such inputs, and
  leaving them out is no leak.

**2. The target**

- For filling the series, the fluorometer's own reading is exactly the quantity I want (USE-5). The descriptor names
  no extracted-chlorophyll calibration, and the release has no bottle chlorophyll. Factory-calibrated fluorometers are
  often off by about a factor of 2 (Roesler et al. 2017, WET Labs ECO sensors). For someone who acts on chlorophyll
  (food supply, blooms), the target is therefore a proxy.
- Quenching, measured here. I took the 55 casts whose top 15 m is mixed (sigma-theta changes by less than 0.1 kg/m3),
  where real chlorophyll should be nearly uniform. Ratio of the reading in the top 5 m to the reading at 6-15 m, by
  quarter of surface PAR:

  | Surface PAR quarter | Median surface PAR (umol m-2 s-1) | Median ratio |
  |---|---|---|
  | lowest | 55 | 0.97 |
  | second | 128 | 0.90 |
  | third | 301 | 0.78 |
  | highest | 700 | 0.47 |

  Spearman -0.73, p 3e-10. Part of the skill credited to PAR (R^2 0.451 with PAR, 0.377 without) therefore comes from
  predicting the instrument's quenching, not chlorophyll. `curation_comments` and `fit_reason` ("Light transmission
  and PAR carry the rest") should say so.
- The link between the channels and the reading shifts over the record:
  - no bin below 0.11 ug/l in the 36 casts of 2015-2017
  - 25 casts reaching the 0.03 floor in 2018-2022, none in 2023
  - yearly medians from 0.23 (2020) to 0.79 (2017)

  The calendar date carries this shift. With the date, R^2 is 0.451. Without the fractional year it is 0.037, and with
  day of year only (depth, station, day of year) it is -0.57. Depth, station and date alone give 0.107. The model
  learns a mapping for each period. That may be a real change in the sea, or changes in the instrument's offset or
  calibration. Only AZTI's instrument history can tell, and it is worth asking for.
- A number is the right output: a concentration, as a regression.

**3. Does a row match my decision, and is the test what I would face?**

- Unit. I fill a whole survey day at once. A row is one 1-dbar bin, and the metric pools the bins. Mendexa casts
  (median 48 bins) weigh about 1.3 times a Mussel Farm cast (36). That is acceptable.
- Day versus cast. Holding out the survey day is right: one boat and probably one CTD per trip, so a failed
  fluorometer loses both casts of that day. The key comes straight from the date (SPLIT-24).
- When the fill happens. If I fill a survey when it is made, the later surveys do not exist yet (USE-3). The site is a
  known entity, so its history is a legitimate input and the split would be temporal (USE-10, SPLIT-3). Measured on
  the 85 survey days from 2019 on, with LightGBM:

  | Setting | R^2 (log) | RMSE (ug/l) |
  |---|---|---|
  | Real time: trained on every earlier day, refit for each day | 0.337 | 0.476 |
  | Same days under the shipped day-grouped split (later surveys in training) | 0.442 | 0.454 |
  | Real-time naive fill: previous survey's profile, same station and depth | -0.252 | 0.673 |

  Knowing the later surveys adds about 0.1 to R^2. The task holds in real time and beats my naive fill by a wide
  margin.
- Two claims understate this. The `curation_comments` note ("a virtual sensor for future casts has little signal
  across time") and `fit_reason` ("trained on past years only, R^2 is above zero in one of three years") both test a
  model frozen for a whole year (0.10, -0.30, -0.35). A monitoring team refits on its latest surveys.
- `fit_reason`'s "filling between the surveys before and after" is not what the model does. On the shipped splits,
  linear interpolation in time between the nearest training days at the same station and depth gives R^2 0.036,
  against 0.451 for LightGBM. The model needs the date and the channels together: neither carries the skill alone
  (0.107 and 0.058).
- The splits hold out a third of the days at once, while real failures are isolated. The test is somewhat harder than
  reality, which is a minor point. `task_summary.split` says "the casts of other days, including the neighbouring
  weeks, are in training", but a third of the other days sit in the same test fold.

**4. Would I use it?**

In real time, yes, as a stopgap I would mark as estimated: it cuts the error of my naive fill from 0.673 to
0.476 ug/l. The typical error on the log scale (RMSE 0.71) is about a factor of 2 either way. That is about the
fluorometer's own calibration uncertainty. It is good enough to tell "bloom or no bloom", not to feed a food budget for
the mussels.

- I would trust it more with:
  - errors per cast and the depth of the chlorophyll maximum, not only per bin
  - skill against persistence and interpolation
  - AZTI's calibration history
  - a target corrected for quenching
- I would distrust it for its dependence on the date and for the quenching hidden in PAR.

**5. The metric: partly.** `rmse` on ug/l (fallback, `target_transform="log"`) scores the right quantity on the right
scale (MET-3, MET-8). Its weakness is resolution (MET-10).

- In each test fold, the 5 worst casts out of about 60 hold a median 67% (50-70%) of the squared error. The top 5% of
  true values hold 54-69%. The ranking rests on a handful of bloom casts per fold.
- The ocean-colour field scores chlorophyll in log space because it is log-normal (Seegers et al. 2018: squared errors
  suit Gaussian data without outliers; CEOS ACIX-II computes log ratios after them). A pure log score does not work
  here: the 0.03 floor bins (3.5% of rows, a sensor floor) take 25% of the squared error. It would reward predicting
  the floor, and nobody acts on 0.03 against 0.1 ug/l.
- RMSLE (log1p) sits between the two:
  - the 5 worst casts hold 44% of its error, the floor bins 2%
  - it behaves like an absolute error below about 1 ug/l (85% of the bins) and like a relative one in blooms, which
    is how I judge the values: 1 against 3 ug/l is the difference between bloom and no bloom
  - Kendall tau with the current `rmse` over 8 model configurations: 0.85

My choice would be `Metric.from_context("rmsle", target_transform="log")` (MET-11 context, MET-1), the form used for
brazilian_ecommerce, melbourne_housing_market, onlinenewspopularity and video_transcoding_time_prediction. This is a
Should, not a Must: the current `rmse` is defensible.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **When the fill happens: in real time or later in the archive** (USE-3, USE-10, SPLIT-3). With later surveys in
   training, the score is about 0.1 R^2 higher than in real time. The real-time fill is the one with an action: report
   this survey's chlorophyll. A fill made later serves the archive, which leans toward SEL-3. I would make the
   real-time version the task: an expanding training side and short test windows of a few surveys (refit cadence one
   survey, SPLIT-12; at least 3 windows with 50% or more in training, SPLIT-14; at least 50 test rows per window,
   SPLIT-17). If the curator keeps the grouped split, `use_case` should say "a fill made later in the archive" and
   `fit_reason` should name the later surveys in training as a gap.
2. **The target is an uncalibrated fluorometer reading, pushed down by daylight near the surface** (USE-5). This is
   the right target for filling the series, but part of PAR's skill comes from this distortion. Add a note with the
   numbers above, and correct the PAR wording in `fit_reason`.
3. **The link between the channels and chlorophyll changes over the record.** The date carries it, and there are
   possible instrument periods. Ask AZTI for the fluorometer's history, and add a note. `fit_reason` should describe
   the skill as "the channels read against the period" rather than "filling between surveys".
4. **The field's main inputs are missing:** satellite or Copernicus IBI model chlorophyll, and the last measured
   profile as an explicit feature. A possible later variant, not a fix.
5. **The use case's "cast without a fluorometer" variant does not fit the shipped inputs.** Keep only the
   failed-fluorometer case in `use_case`.
6. **Wording in `task_summary.split`** ("the casts of other days ... are in training"): a third of the other days are
   in the test fold.

**What a domain expert would change.** Settle when the fill happens and split to match (gap 1). Say in the notes that
the target is a factory-calibrated, quenching-affected fluorometer reading, and give the measured quenching. Rewrite
`fit_reason` along these lines: "no source names the fill; the target is the fluorometer's uncalibrated reading,
pushed down by daylight; the channels predict it only when read against the date; real-time fill R^2 0.34 against
persistence -0.25". Keep the optical channels for the failed-fluorometer case. Consider `rmsle` from context. Before
any rebuild, ask AZTI for the fluorometer calibration and instrument history.

**Sources**

- Solaun et al. 2025, Data in Brief 61:111736, read in full (Europe PMC PMC12197977): sensors, stations, sampling,
  Background and Value of the Data. No fluorometer calibration and no bottle chlorophyll are described.
- AZTI release, doi:10.17632/vyz9zvddz4.2 (the raw table).
- Roesler et al. 2017, Limnol. Oceanogr. Methods 15:572-585, doi:10.1002/lom3.10185 (abstract excerpts only): factory
  calibration about 2x too high; calibrations need low light or a quenching correction.
- Seegers et al. 2018, Optics Express 26(6):7404, doi:10.1364/OE.26.007404 (abstract only), and the CEOS ACIX-II Aqua
  metrics page: log-space metrics for log-normal chlorophyll.
- Sauzède et al. 2016, JGR Oceans (HAL hal-01304165), and the BGC-Argo SOCA product page: SOCA-CHL inputs.
- Copernicus Marine product page for IBI_ANALYSISFORECAST_BGC_005_004: daily 3D chlorophyll at 1/36 degree.

**My scripts**, on the definition as checked (untuned LightGBM, the shipped 9 splits unless stated), in the practitioner's scratch folder in the run:

| Script | What it measures |
|---|---|
| explore.py | floor, survey spacing |
| npq.py, npq2.py | quenching; metric scales and rank agreement |
| concentration.py | where the error sits under each scale |
| years.py, epochs.py | instrument periods |
| r2_sets.py | date-only feature sets |
| baselines.py | interpolation, real-time fill, persistence |
| grouped_2019.py | the shipped split on the days from 2019 on |

</details>

<details><summary>Blind review</summary>

**Verdict: exclude (borderline).** The data are real and match the public source exactly, and the day-grouped split is honest. But the task is to predict CTD-fluorometer chlorophyll from the other sensors on the same cast, and no real decision depends on that. Most of the skill comes from absolute date, which appears to track fluorometer calibration periods rather than ocean physics.

**What the task is.** Each row is one 1-dbar bin (1-52 dbar) of a Sea-Bird SBE 25/25plus CTD cast. The casts come from two stations about 1.8 km apart off Mendexa, Basque coast, 2014-2023, 180 casts on 146 days. The features are the other sensors on the same package: T, S, sigma-theta, light transmission, PAR, DO, O2 saturation, plus pressure, date, time of day and station. The target is log in-vivo fluorescence chlorophyll (µg/L).

**Concerns, most serious first**

1. **No real prediction use.** Whoever has the features has the fluorometer reading too: it is on the same instrument. In the raw file chlorophyll is missing in 1 of 8,195 rows, and that row (2017-09-04, 39 dbar) is missing every variable. So there is nothing to gap-fill. The authors' stated reuse is trend analysis, comparing biotoxins with safety limits, and shellfish management, not chlorophyll prediction. The only predictive use I found is a cross-dataset ML benchmark (Zhou et al., PLOS ONE 2026; repo zhm12305/marine-ml-benchmark). Its "hydrographic" dataset is this same `Hydrographic_variables.xlsx`, with the same range 2014-05-20 to 2023-12-18. A "virtual sensor" use (chlorophyll where no fluorometer was fitted) would need transfer to new periods or instruments, and that fails:
   - My chronological check (train before 2020-10-19, test after): LightGBM R2 = -0.33, -0.02 without the year feature, train-mean baseline -0.002.
   - The PLOS paper's chronological split gives the same picture: "XGB -0.592, RF -0.354".
   - Change: nothing inside this table fixes it. Keep it only if the benchmark accepts within-record interpolation soft sensors, and label it as such.

2. **The signal comes from absolute time, probably sensor periods.** LightGBM, 3-fold CV grouped by day, 3 repeats:

   | Features | R2 |
   |---|---|
   | All + days-since-start + day-of-year | 0.486 |
   | All + year only | 0.391 |
   | All + day-of-year only | 0.079 |
   | No date | 0.107 |
   | No date, no time-of-day | 0.055 |
   | Date only | 0.008 |
   | Ridge, all features | 0.036 |

   - **Floor period.** All 287 rows at the 0.03 µg/L floor fall between 2018-11-19 and 2022-09-12. Before that, cast minima were 0.07-0.57, and winter casts in 2015-2017 never went below 0.11. The cast minimum jumps from 0.03 (2022-09-12) to 0.47 (2022-10-03).
   - **The mapping shifts by period.** Without date, R2 is 0.27 on the casts outside the floor period alone and 0.15 inside it, but only 0.11 pooled. So the feature-to-target mapping changes between periods, and date tells the model which period it is in.
   - **What this means for scores.** (a) Scores mostly measure how well a method splits the timeline into periods and fits interactions within them. (b) Results depend on preprocessing: a harness that drops or mis-encodes the datetime `cast_date` gets R2 ≈ 0.1.
   - The source names two CTD models but gives no fluorometer model or calibration, so I cannot confirm that the periods are instrument changes.
   - Change, if kept: encode `cast_date` as numeric days since start plus day of year, and document that this column carries most of the signal.

3. **Censored, quantized target, amplified by the log.** Readings come in 0.01 µg/L steps with a floor at 0.03.
   - log(0.03) = -3.51 and log(0.04) = -3.22, so the lowest steps are about 0.3 log units wide. The target has median -0.84 and SD 0.96.
   - The 287 floor rows (3.5%) produce 22% of LightGBM's squared error. Rows at or below 0.05 (4.6%) produce 26%.
   - Some whole casts read 0.03 from about 17 m to the bottom in January (2021-01-12, 2022-01-18). That looks like a dark-offset or clipping artefact.
   - Change: use log(chl + 0.05) (grouped R2 0.495 with date, 0.114 without), or flag or drop casts dominated by the floor.

4. **The effective sample is small.** 8,194 rows, but only 180 casts on 146 days, about 45 vertically autocorrelated rows per cast. 55% of target variance lies between casts. Per-fold R2 ranges from 0.38 to 0.56. Grouping by `survey_day` rather than by cast is the right choice: same-day, same-depth log-chlorophyll at the two stations correlates at r = 0.88 (34 shared days). A row-random split would inflate R2 to 0.94; the PLOS repo's random split reports RF 0.848 and XGB 0.878. Change: keep grouping by day.

5. **Minor preparation issues.**
   - `survey_day` is an exact string copy of `cast_date` (100% equal). Use it only as the group key, never as a feature: all of its levels are unseen at test time.
   - `time_of_day_utc_h` is NaN for the whole 2016-04-15 cast (raw time -999).
   - `sigma_theta` and `oxygen_saturation` are computed from T, S and DO. The redundancy is harmless.

**What checks out**
- Downloaded `Hydrographic_variables.xlsx` from Mendeley; its sha256 (d7a00558...) matches the manifest. The prepared target equals log(raw chl) for all 8,194 rows.
- The -999 codes are mapped to NaN, with none left. The single dropped row is all-missing.
- No duplicate rows and no duplicate feature vectors.
- No feature is computed from the target. Light transmission and O2 are co-measured, not proxies: Spearman rho with the target is -0.13 and +0.05 pooled.
- Values are plausible: T 11.7-24.1 °C, S 32.5-35.8, PAR up to 1,384 µmol/m²/s, O2 saturation 71-126%, chlorophyll 0.03-11.1 µg/L. Missingness is small (PAR 3.6%, others under 1.2%).
- Lat/lon are constant per station, so dropping them is fine.

**What I could not check**
- The Data in Brief article text (the publisher returned 403).
- The fluorometer model, its calibration against extracted chlorophyll, and whether instrument swaps line up with the 2018-11 and 2022-10 breaks.
- Whether 0.03 is a clipping floor or real low chlorophyll.
- The last ~40% of the PLOS ONE article.

**If kept anyway:** encode `cast_date` as numeric (days since start plus day of year), use log(chl + 0.05), keep `survey_day` as the group key only, and describe the task as within-record soft-sensor interpolation, not forecasting or transfer.

Sources: https://data.mendeley.com/datasets/vyz9zvddz4/2 ; https://doaj.org/article/3303e6cdc9d34887a8e538aef6a079e8 ; https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0351325 ; https://github.com/zhm12305/marine-ml-benchmark (outputs/tables/dataset_split_summary.csv, hydrographic_baseline_diagnostics.csv).

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01)**

**Verdict.** The mechanics follow their precedents: source and year, the cleaning, the target's scale, the metric, and the group widened from the cast to the day. One decision has a close precedent that went the other way, and the definition names no fact that sets it apart: the use case against `glioma_grading_clinical_and_mutation_features` (USE-1, `No`, Lennart, 2026-10-26). Two smaller points. First, the use case names a prospective moment that the definition's own `splits_comment` calls the temporal variant (SPLIT-3). Second, the definition credits the curator with the split by cast, but that proposal came from the AI screening. No drift, no third exception, and no exception to a Must.

**What I read.** The run's decision register (its flags do not touch this dataset, see the last section), the Cases tables of use_case.md, splits.md, cleaning_features.md and metrics.md, the sibling `basque_offshore_bivalve_biotoxins` (same AZTI release, same run), the run's other added definitions, and the records and CC lines of the precedents named below. I also ran one check of my own on the shipped splits: time_only.py in the precedent checker's scratch folder in the run, with its output.

**Decisions against their precedents**

| # | Decision | Closest precedents | Status |
|---|---|---|---|
| 1 | Use case: a "for example" virtual sensor that no source names, fit approximate (USE-1, USE-8) | `glioma_grading_clinical_and_mutation_features` (`No`, 2026-10-26, Lennart); `nba_players_2016_2019` (`No`, 2026-10-26, Lennart); `electric_motor_temperature_prediction` (Yes; the screening's precedent); `5g_energy_consumption` (USE-9, direct, 2026-10-14, Lennart) | departs from glioma with no stated reason (check 1) |
| 2 | Fit approximate because no actor is named | the run's siblings, all AI drafts with no curator ruling: `boreal_postfire_lichen_biomass`, `pennsylvania_oak_hickory_regeneration_experiment`, `australian_vehicle_insurance_2004_2005`, `blogfeedback`, `noaa_storm_events_damage` | consistent within the run; no curator precedent yet |
| 3 | Grouped rather than temporal (SPLIT-3) | tension row "Temporal against grouped" (Lennart, 2026-10-12); `nantucket_sound_sea_duck_aerial_survey_counts` and `wadden_sea_sibes_macoma_abundance` (grouped, on the source's words); "the right split against the score" (`forest_fires`; SPLIT-21, `aeolus`) | the reason given is the use case, which is the right kind of reason, but the use case names both regimes' moments (check 2) |
| 4 | Group on the survey day, widened from the cast (SPLIT-1, SPLIT-4, SPLIT-24) | `airfoil_self_noise` (setup, not run, 2026-10-20, Lennart); `concrete_compressive_strength` (mix, 2026-10-14); `infrared_thermography_temperature` (same-day subjects left on both sides, IID, 2026-10-21, Lennart) | departs from infrared with a stated reason that rests on a fact nobody has verified |
| 5 | Light transmission and PAR kept | `electric_motor_temperature_prediction` (the rig's other sensors kept); sibling biotoxins left PAR out; CLEAN-22 | consistent |
| 6 | Sigma-theta and oxygen saturation kept, though computed from other channels | CLEAN-5 (only exact copies leave), CLEAN-22; sibling biotoxins drops dissolved oxygen as "a copy of the saturation" | consistent; the sibling is the one that departs |
| 7 | Latitude, longitude and datum dropped; date and time rebuilt | sibling biotoxins ("coordinates and datum (one value per farm)"); CLEAN-5, CLEAN-12 | consistent |
| 8 | -999 set to missing; the one bin without a target dropped | `sdss_17` (-9999 to missing); sibling biotoxins; CLEAN-10, CLEAN-15 | consistent |
| 9 | Target shipped as log, scored in ug/l | sibling biotoxins (log, scored in ug/kg); `wadden_sea_sibes_macoma_abundance` and `nantucket_sound_sea_duck_aerial_survey_counts` (log1p, scored on the raw value); MET-3 cases `forest_fires`, `allstate_claims_severity` | consistent; the notes need the scored-scale numbers |
| 10 | Metric: fallback RMSE in ug/l | sibling biotoxins (same reason, Zhou et al.'s R^2 "for cross-dataset comparability"); `bias_correction_r_bias_correction_r_2` (R^2 reported beside RMSE: fallback) | consistent |
| 11 | Two-Regime Zeros tag removed | the curator's tag definition (Andrej, 2026-10-30); `how_much_did_it_rain_ii` and `carbonfluxbench_flux_tower_upscaling` (removed); sibling biotoxins (kept, 67% at the code) | consistent; the note describes the floor wrongly |
| 12 | `source = "Other"`, year 2025, CC BY 4.0; the record's `original_source` to change from Github to Other | PROV-8, PROV-9; sibling biotoxins' definition | consistent; the sibling's record still says Github |
| 13 | Accepted warning `dataset_duplicate_columns` (`cast_date`, `survey_day`) | definitions.md: a group column is split metadata, never a feature | consistent |
| 14 | Marker `No Good Target (yet)` on a `Yes` record | the run's biotoxins and `avito_demand_prediction` (Andrej, 2026-10-30) | consistent until the call to ship or not |

**Details**

1. **The use case (USE-1).** The 2026-10-27 screening's reject check rested on `electric_motor_temperature_prediction`. Two measured facts now set this case apart from that one. In the motor case the source (Kirchgaessner et al.) names the estimation of temperatures, and the other sensors carry R^2 0.97. Here no source names a use: Zhou et al. picked chlorophyll as one target of a cross-dataset benchmark. The channels without the date reach only R^2 0.058 on the log scale (the builder's optical ablation on the day-grouped splits).
   - The facts now look like glioma's. There, Lennart retired a target that a methods paper chose ("unclear if the original author just did to look at the data / see if it works, but not that it makes sense for a real task"), with no source naming a setting where the label is missing. In AZTI's programme the fluorometer read 8,194 of 8,195 bins.
   - The pattern of the use case moving after measurement echoes `nba_players_2016_2019` ("the prediction point moved twice to fit the data"). The screening called it a virtual sensor. The builder's outcome line reads "works only as gap-filling between surveys". The definition keeps "virtual sensor" in `use_case` but argues gap-filling in `fit_reason` and `splits_comment`.
   - The curator's `Yes` (2026-10-30) came before these measurements. Under "Stages", the add stage's measurement supersedes the screening's reading. The same curator's notes in this run say the add stage decides: on nantucket, "Just try to add it and if it turns out a bad task, then we drop it to no"; on rand_health_insurance_experiment_doctor_visits, "Try to find a target and if not we can still reject it".
   - A candidate fact that sets it apart (my run, 9 shipped splits, untuned LightGBM, R^2 on the log scale):

     | Inputs | R^2 |
     |---|---|
     | time index alone | -0.03 |
     | time, depth and station | -0.00 |
     | per-year training mean | 0.08 |
     | channels without the date | 0.058 |
     | channels and date together | 0.455 |

     So the model does read the channels, but only together with the date: the relation between channels and chlorophyll drifts, and the model learns it from the survey days around the held-out one. That matches filling a failed cast in a monitored record. The definition's note "models fill a held-out day from the surveys around it rather than read chlorophyll off the other channels" should say this instead. No source names this moment, though.
2. **"No actor named" as the ground for approximate (USE-8).** USE-8's list of known gaps does not include a use case nobody names. All six definitions that use this ground come from this run. The first curator decision on any of them is the precedent for the other five, so decide them alike.
3. **Grouped against temporal (SPLIT-3).** `use_case` names two moments:
   - "fills a profile whose fluorometer failed": within the record, so grouped;
   - "estimates chlorophyll for a cast made without one": the definition's own temporal candidate, "a new instrument without a fluorometer from some date on".

   The tension row asks for one regime, the one the use case implies. The temporal variant scores 0.10, -0.30 and -0.35. Dropping the second moment is sound only when the use case is the reason, not the score (forest_fires; SPLIT-21).
4. **The day as the group.** The airfoil precedent widened the group because the nearer sibling told the target and the actor's query is the wider unit. This definition argues the same: on two-cast days R^2 is 0.705 grouped by cast against 0.369 by day, and "A failed fluorometer or a survey without one lacks both casts of the day". It departs from infrared_thermography, where same-day subjects stayed on both sides because day folds scored like random ones and the calibration should not depend on the day. Here the day folds change the score.
   - By SPLIT-4 the size of the gap never decides. The deciding fact is that one instrument or one trip serves both casts, and the builder lists exactly that as "Cannot verify". The stricter split matches how wadden_sea and nantucket chose ("stricter" in both).
   - The key is exact (SPLIT-24 holds). This is the first group key in the working copy that is a calendar unit with the date kept as a feature: the 34 other `Grouping` keys are entities. If accepted, it needs a Cases row under SPLIT-3 or SPLIT-24.
   - Attribution: the definition says "the curator's brief asked for a split by cast (2026-10-30)". The CC of 2026-10-30 sets only `Yes`, priority 1. "Grouped by cast or temporal" is the AI screening's (2026-10-27; record, the screening's reject check, review page "regime grouped by cast"). Write "the screening proposed".
5. **PAR in the sibling.** Biotoxins leaves PAR out as "light at the cast's hour" from a cast up to 14 days before the sample. Here PAR comes from the same cast, so the two cases differ by a stated fact. Which platforms carry light transmission and PAR without a fluorometer is still unknown (USE-1).
6. **Dissolved oxygen in the sibling.** Per bin, dissolved oxygen and saturation correlate at Spearman 0.61 (Pearson 0.71), so neither is a copy of the other. Biotoxins' "a copy of the saturation" departs from CLEAN-5 and CLEAN-22, and this definition does not. Align the sibling in its own review.
9. **Scored-scale numbers (writing).** Wadden_sea and nantucket each quantify how RMSE behaves on the raw scale. This definition gives every number on the log scale. The builder's optical ablation already has the scored ones: R^2 on ug/l 0.331, RMSE 0.476 against 0.592 for the training mean, and 0.092 without the date. Add them.
10. **Metric.** As in `qsar_aquatic_toxicity` and `concrete_compressive_strength`, R^2 and RMSE rank models alike within a fold. The origin stays fallback because Zhou's R^2 was computed on the IQR-cut copy without the bloom values (MET-2). The reason could say so.
11. **The 0.03 floor.** The value 0.03 holds 287 bins against 37 at 0.04 and 52 at 0.05. It occurs only in 2018-2022, up to 10% of 2020's bins. In 2014-2017 and 2023 it never occurs, and the minimum there is 0.06-0.11. That is a floor of one period, a left-censored value, not "the low end of a continuous spread".
    - The tag call stands: 3.5% is not "by far the most frequent" value (the next most frequent, 0.21, holds 1.9%).
    - On ug/l the floor moves an error by at most 0.03.
    - The sibling names its floor code ("not a cap or a missing value"). This note should name the floor and its years too (P7).
12. **The sibling's record.** Apply the change of `original_source` to Other to both records.
13. **The duplicate-columns warning.** The pair is there by design: the harness drops `survey_day` before fitting. The two earlier accepted warnings (`early_learning_predictors`, `mercedes_benz_greener_manufacturing`) were on feature pairs, not on a group key.

**Drift, third exceptions, Musts.**
- No drift. Andrej's `Yes` calls on "for example" use cases in this run (boreal, pennsylvania, crms, nantucket, rand) agree with one another, and his `No` calls give "No predictive task" (north_american_breeding_bird_survey).
- The definition records no exception.
- The register's flags do not touch this dataset. That covers the amendments due on CLEAN-19 and SPLIT-10 and the exceptions to the Musts PROV-13, SPLIT-9 and SPLIT-14.
- The `one_feature` pair (fitness_club retired against aps_failure and california kept) is not triggered. The probe's single feature reaches skill 0.058 against 0.456, and the time index alone reaches R^2 -0.03.

**Consistency check (AI, 2026-11-01):** your call on basque_offshore_ctd_chlorophyll (`Yes`, a "for example" virtual sensor, fit approximate, USE-1) differs from glioma_grading_clinical_and_mutation_features (`No` + `No Good Target / Scientific Discovery`, 2026-10-26, Lennart). Glioma had a target a methods paper chose and no source naming a moment when the label is missing; the same holds here. Zhou et al. chose chlorophyll for a cross-dataset benchmark, and AZTI's fluorometer read 8,194 of 8,195 bins. What sets this one apart?
(a) A failed fluorometer is a real moment in monitoring, and the data supports filling it from the surveys around it: channels and date together give R^2 0.455 on the log scale, each alone 0.06 or less. Record this as the fact, reword `use_case` from a virtual sensor to gap-filling within the record, and keep fit approximate; (b) treat it like glioma: `No` + `No Good Target / Scientific Discovery`; (c) reopen glioma to match; (d) amend USE-1, so that a "for example" use case with a measured signal is enough when no source names one.

**Consistency check (AI, 2026-11-01):** `use_case` names two moments: filling a cast whose fluorometer failed (grouped, like nantucket's and wadden_sea's maps of surveyed periods) and a cast made without a fluorometer (the `splits_comment`'s temporal variant). SPLIT-3 and its tension row (Lennart, 2026-10-12) ask for one regime, the one the use case implies. The temporal variant scores R^2 0.10, -0.30 and -0.35, and the regime must not follow the score (forest_fires; SPLIT-21). Which moment is the task?
(a) Filling within the record: drop "or estimates chlorophyll for a cast made without one" from `use_case` and `question`, and grouped stays; (b) the prospective sensor: a temporal split, with the task judged on its temporal score; (c) keep both moments under the grouped split: not available as an exception, since SPLIT-3 is a Must; (d) amend SPLIT-3.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: basque_offshore_ctd_chlorophyll (2026-11-01)**

**Position: ship after changes, text only.** The data, the split and the metric stay. The panel found no leak and no
provenance fault, and it found a real signal that depends on the model. Every refuted claim is wording. Each open call
(which moment the use case names; hold out the day or the cast) has an answer that ships.

```text
Verdict: ship after changes (text only).
Validity: USE-1 holds once use_case is narrowed to the failed-fluorometer fill (fit approximate, USE-8); USE-2 not
  triggered; LEAK-10 holds for every column; SPLIT-1/SPLIT-3 hold for the fill in the measured series (grouped by
  day); SPLIT-24 holds; PROV-8, PROV-13 hold (rebuilt from AZTI's release).
Value: TP-2/TP-4: channels and date together R^2 0.455 (log), each alone 0.06 or less; families separate.
Quality: the 0.03 floor and the PAR quenching documented; the metric reason cites MET-1/MET-2, not MET-5.
Weighed: source +, use case 0 (a field practice, no actor named by the source), size 0 (146 days), gap +.
For the curator: which moment (fill later in the series, grouped as shipped; or fill at the survey, temporal); keep
  the day as the group.
```

**1. A failed fluorometer on a survey is a real moment, and that sets this case apart from glioma (P3; USE-1 Must,
USE-2 Must, USE-9 Should).**
- Claim: the task fills a monitoring series. The decision is what chlorophyll AZTI reports and stores for a survey whose
  fluorometer failed. The actor and the moment are known.
- Evidence:
  - The domain practitioner, as AZTI's CTD lead, would use it. Filled at the survey, it cuts the error of today's fill
    (the previous survey's profile) from 0.673 to 0.476 ug/l (R^2 -0.25 to 0.34, 85 days from 2019).
  - Chlorophyll virtual sensors built from CTD channels are established practice (SOCA-CHL, Sauzede et al. 2016).
  - The sensors on this package fail one at a time. Five casts in the release lost a whole channel (PAR twice, oxygen,
    salinity, T and S), each on a single survey (split auditor, issue 3). The fluorometer is one more channel on the
    package. That it never failed in this release is no evidence that it never fails (inference).
- The fact that sets it apart: glioma (`No`, Lennart, 2026-10-26) turned on a label that exists before the features
  ("a model can only cross-check a label that already exists"). Here the features exist exactly when the label is
  missing. The curator's own fill precedents point the other way:
  - 5g_energy_consumption (direct, "filling the gap left by the stations it measured", Lennart, 2026-10-14);
  - covertype ("fill the gaps to predict unseen areas", Lennart);
  - electric_motor_temperature_prediction (a virtual sensor, Yes).
- Concede: no source names this use, so the fit stays approximate (USE-8). The second half of `use_case` ("a cast made
  without one") does not fit. A CTD without a fluorometer rarely carries a transmissometer and PAR, and that moment is
  temporal. Four agents agree it should go.
- Mildest remedy: answer the consistency check with (a). Narrow `use_case` and `question` to the failed-fluorometer
  fill, and record the distinguishing fact: the features are present and the label missing, the field has a named
  practice, and the signal is measured.
- Why this wins: USE-2 excludes a task that no decision fits, and a decision fits here. The blind reviewer's "nothing
  to gap-fill" (1 of 8,195 bins missing) describes this release, not the moment the task stands for.

**2. The date's skill is the channels read against their period. A fill in a monitored series uses exactly that, and
it is not a shortcut (P3/P6; USE-6 Must, TP-4 Must, EV-1).**
- Evidence: four agents measured it independently.

  | Inputs | R^2 (log) |
  |---|---|
  | time index alone | -0.03 |
  | per-year training mean | 0.08 |
  | date, depth and station | 0.106 |
  | neighbouring days' profile at the same depth, interpolated | 0.028 to 0.040 |
  | channels without the date | 0.058 |
  | channels and date together | 0.451 to 0.455 |

  Sources: claim auditor rows 8 and 29, precedent checker, practitioner, split auditor. The season adds nothing
  (day of year only: 0.037).
- What this means:
  - Neither the calendar nor any channel carries the skill alone. The model learns a channel-to-chlorophyll mapping
    that drifts over time, and recalibrates it on the surveys of the same period.
  - The date is known when the fill is made, and a test day is never in training (0 overlap in 9 folds). LEAK-10
    holds, and USE-6 makes it a legitimate input.
  - TP-4 needs proof of `Trivial`, and there is none: no single input comes close, and time alone scores below zero.
- Concede:
  - The mechanism in `fit_reason` and the Note ("filling between the surveys ... rather than read chlorophyll off the
    other channels") is refuted. Rewrite both with the table above.
  - The blind reviewer is right that a harness which drops `cast_date` scores about 0.1. The notes should say that the
    date carries the period of the mapping.
- Why this wins over dropping `cast_date` (column auditor option (b), after infrared_thermography_temperature):
  - Infrared was a calibration "independent of time", and there day folds scored like random ones.
  - Here the correlation of light transmission with chlorophyll changes sign between years (-0.58 to +0.16). A
    time-independent sensor would serve a use nobody claims and misstate the data (USE-1).

**3. The split is honest, its key exact, and it is stricter than the alternative (P4; SPLIT-1, SPLIT-4, SPLIT-23,
SPLIT-24 Must).**
- Evidence:
  - The key is the exact date: 146 groups, 48-49 test days and 2,621-2,816 test rows per fold. No day falls on both
    sides in the 9 splits, 0% of test rows have an exact copy in training, and `hidden_groups.py --include-grouped`
    finds no group but the known one.
  - Holding out the day removes the strongest shortcut: the other station's same-day value alone gives R^2 0.736
    (1,218 pairs).
  - Every whole-channel failure in the release is a single survey, so one held-out day is the gap the programme
    actually meets. A 7-day buffer costs only 0.009.
- Day over cast:
  - The 0.03 floor hits both casts of 2022-01-18, 2022-08-01 and 2022-09-12.
  - The two casts of a day are 8 to 94 minutes apart and never simultaneous (column auditor; claim auditor row 24),
    which points to one boat and one CTD.
  - The practitioner: "Holding out the survey day is right".
- Concede: 2023-12-11 shows a glitch in one cast (one station lost T and S, the other did not). "A failed fluorometer
  lacks both casts of the day" is therefore too strong.
- Mildest remedy:
  - Reword to "we hold out the day so the score does not rest on the other station's same-day cast (alone R^2 0.736)",
    and keep the day.
  - Fix the slips: 1.82 km, not 1.5; 111 + 1 + 34 days; the current numbers 0.641 against 0.348; "the screening
    proposed", not the curator's brief.

**4. The split must be one regime, and both candidates ship (P4; SPLIT-3 Must; the remedy ladder; the tension "the
right split against the score").**
- The two candidates:
  - **Fill later, in the measured series** (a past survey, filled with the surveys around it). AZTI's 2014-2023
    release is itself such a product. Grouped, as shipped: R^2 0.451, RMSE 0.476 ug/l against 0.587 for the training
    mean.
  - **Fill at the survey** (report the value before the next survey). An expanding temporal split, refit each survey:
    R^2 0.337, RMSE 0.476 against 0.673 for persistence (practitioner).
- The definition's temporal numbers (0.10, -0.30, -0.35) test a model frozen for a year, which no monitoring team does.
  Even so, the model beats the past years' constant in 4 of 5 years, on both scales (claim auditor row 30).
- Rule: SPLIT-3 asks for one regime, the one the use case implies, and the curator meets it by choosing. A Must
  violation that the definition can fix is fixed, not punished (principles, Strengths; remedy ladder: re-split before
  exclude). Neither choice may turn on the score (forest_fires; SPLIT-21).
- My recommendation: keep grouped. Write "a fill made later, in the measured series" into `use_case`, and name the
  later surveys in training as the gap in `fit_reason` (the practitioner's text remedy). If the curator takes the fill
  at the survey as the use, re-split temporally (SPLIT-12, SPLIT-14, SPLIT-17), and the dataset still ships.

**5. No leak, and the data comes faithfully from its first publication (P4, LEAK-10 Must; P5, PROV-8 and PROV-13
Must).**
- Evidence:
  - No column records anything after the target. Every channel is measured in situ at the same instant, and
    sigma-theta and oxygen saturation are computed from known channels.
  - Missingness does not encode the target (the missing-indicator probe is flat), and `survey_day` is split metadata
    only (column auditor; LEAK-33).
  - The table is rebuilt from AZTI's Mendeley release (sha256 d7a00558..., identical in v1 and v2; CC BY 4.0), not
    from Zhou's IQR copy. That copy keeps 4,653 of 8,195 bins, cuts chlorophyll to a maximum of 1.47 against 11.13,
    and drops every Mussel Farm row (claim auditor row 18).
  - 36 of 48 claims hold. The refuted ones are wording, and none breaks validity.
- Concede: the period 2018-11 to 2022 (the 0.03 floor in 25 casts, the sign of the light-transmission slope) may be a
  calibration era of the fluorometer. The evidence is circumstantial (EV-6).
- Mildest remedy: a note with the numbers, and a request to AZTI for the instrument history (PROV-13, repair from the
  origin).
- Why it does not exclude: the fill's target is the series' own reading. Reproducing that period's calibration is
  exactly what the fill must do. The practitioner: "For filling the series, the fluorometer's own reading is exactly
  the quantity I want (USE-5)". A gap that changed what the target means would be a validity question (the P3-over-P7
  tension row), but this one does not change it for the stated use.

**6. Worth benchmarking: methods separate on unseen days (P6; TP-2 Should, TP-3 Must, TP-5 Must).**
- Evidence:
  - Untuned probes on unseen days give LightGBM 0.453, random forest 0.332, ridge 0.063 and kNN -0.258 (split auditor,
    the builder's day-grouped probe output).
  - LightGBM beats the dummy on 5 of 5 folds, and the RMSE is 0.476 against 0.587 for the training mean.
  - Per-fold R^2 runs from 0.38 to 0.56 (blind reviewer).
- Not `Too Small`: TP-5 counts units per test fold, and this regression is scored per row, with 48-49 days and more
  than 2,600 rows per fold.
- It is the only definition in the working copy grouped on a time unit (precedent checker): gap +.
- Concede: the probes are untuned (TP-1). The tuned results will show whether the spread holds.

**7. The metric and the cleaning are sound, and their faults are wording (P6, MET-1, MET-2, MET-3 Must; P7, CLEAN-10
and CLEAN-15).**
- The metric:
  - RMSE on ug/l can be computed on every fold. Within a fold it ranks models exactly as Zhou's R^2 on ug/l would
    (the MET-11 identity).
  - Shipping the log costs nothing: Duan smearing moves the RMSE from 0.4759 to 0.4749, and a model fitted on ug/l is
    worse (0.5028).
  - The error sits in the bloom bins (the top 1% of values hold 40% of it). That is where a "bloom or no bloom" fill
    matters, which is what the practitioner says the model is good for.
- The cleaning: the -999 code is set to missing with exact counts, the one all-sentinel row is dropped, and the
  coordinates, one value per station, are dropped.
- Concede:
  - The metric reason should cite MET-1/MET-2, not MET-5 (Zhou does name R^2 as its criterion, but chose it to compare
    datasets, on a copy without the blooms).
  - The 0.03 note should call it a reporting floor: 287 bins against 37 at 0.04, from 2018-11 to 2022-09. The tag
    removal stands (3.5% against 1.9%), and on ug/l the floor carries 0.6% of the error.
  - One sentence on PAR quenching (Spearman -0.65 to -0.73), and the -999 counts marked as raw.
  - The practitioner's `rmsle` is a Should alternative for the MET-10 weighing. The practitioner also calls the
    current `rmse` defensible.

</details>

<details><summary>Critic</summary>

**Critic, opening brief: basque_offshore_ctd_chlorophyll (2026-11-01)**

**Verdict: do not ship as defined.** It can ship once points 1 and 2 are settled in the definition. If the curator does not accept point 1's failed-survey fill as a decision, the verdict is `No` + `No Good Target / Scientific Discovery`. Points 3 to 6 call for notes and text fixes. None of them is a reason to exclude.

```text
Verdict: ship after changes (or No, if point 1's moment is not accepted).
Validity: USE-1/USE-2 triggered (two moments, no source names either; glioma precedent): narrow to one moment, or No.
  SPLIT-3/USE-3/USE-10 triggered: the split mirrors an archive fill with later surveys in training: re-split temporal.
  USE-5/PROV-13 concern (maybe an instrument period, 2018-11 to 2022-09): ask AZTI, note now.
  USE-8 triggered: fit_reason names the wrong gap: rewrite.
Value: the metric reason cites MET-5 where MET-1/MET-2 decide; rmse kept, rmsle a weighing call.
Quality: target floor, distance, day counts, stale numbers, attribution to the curator, original_source.
For the curator: point 1 (is a failed-survey fill a decision?), point 2 (fill at the survey or later in the archive?).
```

**1. The use case names two moments, no source names either, and the facts now match glioma (P3; USE-1 and USE-2, Must; SEL-3).**
- Problem: `use_case` reads "fills a profile whose fluorometer failed, or estimates chlorophyll for a cast made without one".
  - No source names either use. The descriptor lists trends, toxin limits, shellfish management and early warning, all for the series as a whole.
  - Zhou et al. picked chlorophyll as one target of a cross-dataset benchmark (claim auditor rows 1, 17, 36).
- Effect: the benchmark would score a target a methods paper picked, with no actor waiting for the prediction.
- Evidence:
  - The release holds no instance of the task. 0 of 180 casts lack chlorophyll. The one -999 bin (2017-09-04, 39 dbar) is -999 in every channel (my check; also split auditor and blind reviewer).
  - The second moment does not fit the inputs. A CTD package with a transmissometer and a PAR sensor but no fluorometer is rare (domain practitioner). Without both optical channels R^2 falls from 0.451 to 0.220.
  - The second moment has no signal across time either: trained on past years, R^2 is 0.10, -0.30 and -0.35, and leaving out one calendar year gives 0.067 (split auditor).
  - The screening's precedent no longer fits. In `electric_motor_temperature_prediction` the source names the estimate and the other sensors reach R^2 0.97. Here the channels reach 0.058 without the date (precedent checker).
  - `glioma_grading_clinical_and_mutation_features` went `No` + `No Good Target / Scientific Discovery` (Lennart, 2026-10-26). Its target was chosen by a methods paper: "unclear if the original author just did to look at the data / see if it works". The precedent checker's consistency check on this is still open.
- Remedy (fix the definition): name one moment that has a decision.
  - The only one the panel found is the domain practitioner's. When a survey's fluorometer has failed, AZTI fills its chlorophyll as it reports the survey to the shellfish managers and the mussel farm (food supply, bloom warning).
  - Drop "or estimates chlorophyll for a cast made without one" from `use_case`. Reword `question`, which says "read from the profile's other sensor channels".
  - Record that moment as the fact that sets this case apart from glioma (option a of the consistency check).
  - If the curator does not accept a failed-survey fill as a decision: `No` + `No Good Target / Scientific Discovery`. The record already carries `No Good Target (yet)`.

**2. The split mirrors a fill made later in the archive, not the moment anyone acts (P4; SPLIT-1, SPLIT-3, USE-3 and USE-10, Must).**
- Problem: point 1's decision happens at the survey, when the later surveys do not exist yet. The day-grouped split keeps them in training.
- Effect: the score rewards filling a day with the surveys that came after it, and methods are ranked on a fill made in hindsight. On the days from 2019 on, about 0.1 of R^2 comes from those later surveys.
- Evidence:
  - In the 9 shipped splits, a test day's next survey is in training 70.1% of the time, and both of its neighbours 48.4%. The nearest training day is a median 16 days away (split auditor).
  - The score rests on those neighbours. Dropping the training days within 15 days of a test day takes R^2 from 0.451 to 0.270, and within 30 days to 0.129. Blocks of about 4 months give 0.309 (split auditor).
  - In real time on the 85 survey days from 2019 on (trained on every earlier day, refit per day): R^2 0.337, RMSE 0.476 ug/l. The same days under the shipped split: 0.442 and 0.454 (domain practitioner, `baselines.py`, `grouped_2019.py`).
  - The two stations are known entities with a history. For those, USE-10 says the split is temporal and the previous outcome is a feature. The tension row "Temporal against grouped" (Lennart, 2026-10-12) asks for the one regime the use case implies.
  - A fill made later serves only the trend series, a study looking back (USE-2, SEL-3). `splits_comment` chose grouped because "the use case fills surveys within the record, not future ones". But the people who act on chlorophyll act at the survey.
- Remedy (re-split; SEL-11 and SPLIT-6 keep it in scope):
  - Use a temporal split: an expanding training side, and test windows of a few surveys rolled back from the newest data.
    - SPLIT-14 (Must): at least 3 windows, and every training side holds at least 50% of the data.
    - SPLIT-12 and SPLIT-17 (Should): set the window length from the monthly-to-biweekly survey cadence, with about 50 test rows or more per window.
  - Add the last measured profile at the same station and depth as a feature (USE-10).
  - The signal survives: 0.337 against -0.252 for carrying the last survey forward. A small real signal is no reason to retire (TP-2).
  - If the curator names the archive fill as the use instead:
    - keep the day split;
    - write "a fill made later, in the archive" in `use_case`;
    - name the later surveys in training as the gap in `fit_reason`.

    Point 1 then has to say why a fill made in hindsight is a decision.

**3. The target is probably not on one scale across the record (P3/P5; USE-5 and PROV-13, Must; circumstantial, EV-6).**
- Problem: the fluorometer reading behaves differently from one period to the next, in a way that looks like the instrument.
- Effect: if the periods are the instrument, much of the date's skill is a model spotting calibration periods from a datetime column, not reading chlorophyll.
  - A harness that drops or mis-encodes `cast_date` scores R^2 of about 0.1 (blind reviewer).
  - Under point 2's real-time split, an unannounced recalibration is something no model can see.
- Evidence:
  - The 0.03 floor occurs only from 2018-11-19 to 2022-09-12: 287 bins in 25 casts. It never occurs in 2014-2017, where the yearly minima are 0.07-0.11, or in 2023, minimum 0.06 (my check; claim auditor row 21).
  - Cast minima step from 0.03 at both stations on 2022-09-12 to 0.44 and 0.47 on 2022-10-03. They stay at 0.20 or above afterwards (my check).
  - Below 10 dbar, the slope of log chlorophyll against light transmission is -0.038 in 2014-2018, +0.009 in 2018-11 to 2022 and -0.027 in 2023 (column auditor).
  - Without the date, R^2 is 0.27 outside the floor period, 0.15 inside it and 0.11 pooled (blind reviewer).
  - About three quarters of the date's gain is the year: the year alone gives 0.365, the season alone 0.037 (column auditor).
  - The descriptor names no fluorometer model and no calibration. Factory-calibrated fluorometers are often off by about a factor of 2 (Roesler et al. 2017; abstract only).
  - Daylight quenching: in mixed casts, the ratio of the top 5 m to 6-15 m falls from 0.97 to 0.47 across the PAR quarters (Spearman -0.73; domain practitioner). Part of the skill credited to PAR therefore predicts the sensor's artefact.
- Remedy (repair from the origin, a note meanwhile):
  - Ask AZTI for the CTD and fluorometer history and calibrations (PROV-13).
  - Until they answer, put a note in `curation_comments` and `fit_reason` with the floor period, the 2022-10 step and the quenching numbers.
  - If AZTI confirms instrument periods and has a correction, apply it. If they confirm periods without a correction, the curator weighs USE-5 alongside the record's `No Good Target (yet)`.
  - Not a reason to exclude today.

**4. `fit_reason` and the notes name the wrong gap (P3; USE-8, Must).**
- Problem: the text says models "fill a held-out day from the surveys around it rather than read chlorophyll off the other channels". It also says "trained on past years only, R^2 is above zero in one of three years".
- Effect: the curator would weigh points 1 and 2 on a mechanism the data refutes.
- Evidence:
  - Filling a test day from the neighbouring training surveys at the same depth gives R^2 0.028 to 0.040.
  - Date, depth and station give 0.106. The channels without the date give 0.058. Everything together gives 0.451 (claim auditor rows 8, 29; split auditor; domain practitioner).
  - The past-years figure is selective. R^2 is above zero in 3 of 5 years, the model beats the past years' constant in 4 of 5, and refit per survey it reaches 0.337 (claim auditor row 30; domain practitioner).
  - "Light transmission and PAR carry the rest" leaves out point 3's quenching.
- Remedy (text): rewrite `fit_reason`, and the Note bullets to match:
  - no source names the fill;
  - the target is the fluorometer's factory-calibrated reading, pushed down by daylight near the surface;
  - the channels predict it only when read against the period, and the periods may be the instrument's;
  - if the day split stays, the later surveys in training.

**5. The metric reason cites the wrong rule, and the score rests on a few bloom casts (P6; MET-1 and MET-2, Must, for the reason; MET-10 factors for the choice).**
- Problem: the reason rejects Zhou's R^2 under MET-5. MET-5 would in fact accept it, because Zhou names R^2 as "the primary benchmark indicator" (claim auditor row 37). The rules that reject it are MET-1 and MET-2: Zhou chose R^2 for comparing datasets, on a copy without the blooms and without Mussel Farm.
- Effect on the ranking: in each fold, the 5 worst casts of about 60 hold a median 67% of the squared error. The top 5% of true values hold 54-69% (domain practitioner; claim auditor row 39).
- Remedy (text, plus a weighing call):
  - Cite MET-1 and MET-2.
  - List Zhou's other metrics: MAE, RMSE, NRMSE, NSE and event F1.
  - Say that within a fold, R^2 on ug/l ranks models the same way RMSE does.
  - Keep `rmse` unless the curator prefers `rmsle` from context. Under `rmsle` the floor bins carry 2% of the error, against 25% under a pure log score, and its ranking agrees with `rmse` at Kendall tau 0.85 (domain practitioner).
  - No exclusion.

**6. Factual slips in the text and the record (P7 and writing; EV-7, EV-8, PROV-8).**
- The target bullet and the record's Assessment call 0.03 "the low end of a continuous spread". It is a floor: 287 bins against 37 at 0.04, all between 2018-11 and 2022-09. Removing the tag still stands.
- "about 1.5 km" should be 1.82 km.
- "112 with one cast at Mendexa-Control" should be 111, plus 1 day with a Mussel Farm cast only (2022-03-08).
- The cast-against-day numbers come from an earlier version (the builder's script reads a `cast` column the definition no longer has). Current values: 0.641 against 0.348 on two-cast days, 0.525 against 0.439 on all rows.
- "the curator's brief asked for a split by cast (2026-10-30)": this is not in the record or the run folder. The AI screening proposed it, and an AI proposal is never the curator's.
- "A failed fluorometer ... lacks both casts of the day" is unverified, and one transient fault contradicts it: on 2023-12-11 one station lost temperature and salinity and the other did not.
  - Floors on both casts of 2022-01-18, 2022-08-01 and 2022-09-12 support it.
  - Reword the reason for the day split, as the split auditor proposes: it removes the same-day shortcut (the other station's cast alone gives R^2 0.736).
- The -999 counts are raw. Shipped counts: PAR 296, salinity and sigma-theta 94, temperature and oxygen 46, light transmission 0, time 45 rows.
- `task_summary.split` says the other days are in training, but a third of them sit in the same test fold.
- `known` leaves out oxygen saturation.
- Record: change `original_source: Github` to `Other` (PROV-8).
- Remedy: correct the text. These are quality fixes only.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: basque_offshore_ctd_chlorophyll (2026-11-01)**

**Where we stand.** The critic and I agree on the verdict: ship after changes, and none of the six points excludes the
dataset. One dispute remains, on point 1: whether the facts match glioma. On point 2 I give up the grouped split as the
default. The fill at the survey is the moment with an action, and my check shows that the critic's temporal re-split
can be scored and still has signal. That makes the re-split the mildest remedy, not a threat to the dataset.

**New check (point 2, run for this rebuttal).**
- What I ran: expanding windows of whole survey days, walked back from the newest day. Training is every earlier day
  (SPLIT-11). The window length comes from the fill's horizon (one survey, refit per survey; SPLIT-12), plus two wider
  windows for SPLIT-17. I did not choose the windows by score (SPLIT-21).
- Models: untuned LightGBM with the builder's settings, with and without the critic's lag feature. The lag is the
  latest earlier survey at the same station and depth, plus its age in days.
- Script and output: temporal_check.py, with its outputs, in the advocate's scratch folder in the run.

| Windows | Min train share | Test rows per window | LightGBM RMSE ug/l (beats mean) | + lag | Training mean | Persistence |
|---|---|---|---|---|---|---|
| 1 survey day x 27 (2022-04 to 2023-12) | 0.75 | 45-88 | 0.491 (18/27) | 0.484 (22/27) | 0.623 | 0.627 |
| 2 survey days x 14 | 0.75 | 127-172 | 0.488 (11/14) | 0.491 (10/14) | 0.618 | 0.620 |
| 3 survey days x 9 | 0.75 | 179-255 | 0.543 (7/9) | 0.527 (6/9) | 0.625 | 0.627 |

- On the log scale, the lag lifts R^2 from 0.22 to 0.34 in the one-day windows. On the declared metric (RMSE in ug/l)
  it changes the score by 0.007 or less.
- SPLIT-14 holds: the smallest training share is 0.75. SPLIT-17 holds with two-day windows. One one-day window has 45
  rows.

**1. Two moments, no source, the glioma precedent: partly conceded, partly contested.**
- Conceded:
  - Narrow `use_case` to the failed-fluorometer fill and drop "a cast made without one". Reword `question`.
  - No source names the fill, so the fit stays approximate (USE-8).
  - The release holds no instance of a missing fluorometer.
  - The critic's remedy names the same moment as my point 1: AZTI fills a failed survey as it reports the survey to
    the shellfish managers and the mussel farm.
- Contested: that "the facts now match glioma" (USE-1, USE-2 Must).
  - Glioma was decided on a label that exists before the features: "a model can only cross-check a label that already
    exists" (use_case.md Cases, Lennart, 2026-10-26). Here the features exist exactly when the label is missing.
    That fact sets the case apart, and the consistency check's option (a) records it.
  - The missing instance does not decide either. No rule asks the release to contain missing labels. A supervised
    table always has its labels, as 5g_energy_consumption (Lennart, direct gap-filling) and
    electric_motor_temperature_prediction both do. What counts is whether the moment happens.
  - Here the moment does happen: five casts in this release lost a whole channel on a single survey (split auditor,
    issue 3).
  - The electric-motor gap in R^2 (0.97 against 0.058 without the date) is a score, and the score never decides a use
    case (TP-2; the tension "the right split against the score").
- What follows: I agree with the critic's fallback. If the curator does not accept a failed-survey fill as a
  decision, the verdict is `No` + `No Good Target / Scientific Discovery`. I argue the curator should accept it, on the
  distinguishing fact above.

**2. The split mirrors a fill made later: conceded, and the re-split ships.**
- Why I concede: USE-3 (Must) names the prediction point as when the model is used. The decision the panel found, the
  report to the managers, happens at the survey, when the later surveys do not exist.
- The domain practitioner, speaking as the actor, says the same. I can cite no source for a decision made on a fill
  in hindsight, so I withdraw my recommendation to keep the grouped split (my point 4).
- USE-10 then makes the station's history a feature. The critic's lag is legitimate.
- Remedy (fix the definition: re-split):
  - `Temporal(on="cast_date")` with expanding windows of whole survey days, walked back from the newest.
  - Window length set from the survey cadence (one or two survey days), with at least 9 windows (SPLIT-15).
  - The lag feature and its age.
- The table above shows the task survives the re-split: LightGBM 0.484-0.491 ug/l against 0.62 for the training mean
  and for persistence, and better than the mean in most windows (TP-2).
- Narrowed: the critic's "a fill made later serves only the trend series (SEL-3)" is not needed for the remedy, and I
  do not contest it.

**3. The target may not be on one scale across the record: conceded as a note; narrowed on its effect.**
- Conceded: the floor of 2018-11 to 2022-09, the step on 2022-10-03 and the quenching all go into `curation_comments`
  and `fit_reason`. We ask AZTI for the instrument history (PROV-13, repair from the origin), and the curator weighs
  USE-5 if AZTI confirms periods without a correction.
- Narrowed: the critic warns that under a temporal split an unannounced recalibration is something no model can see.
  Measured with one-day windows:
  - after the 2022-10-03 step (17 windows): LightGBM RMSE 0.575 against 0.742 for the training mean; it beats the mean
    in 11 of 17 windows;
  - before the step (10 windows): 0.284 against 0.312; 7 of 10.
- So the signal survives the step the critic names. For the fill, the target is the series' own reading (practitioner,
  USE-5), and the possible instrument periods are a documented risk, not a validity failure.

**4. `fit_reason` names the wrong gap: conceded.**
- Rewrite it along the critic's four lines.
- Under the temporal re-split, the fourth line (later surveys in training) drops out. In its place go the real-time
  numbers and the past-years baseline: the model beats the constant in 4 of 5 years (claim auditor, row 30).

**5. The metric reason and the bloom weight: conceded on the reason; `rmse` kept.**
- Cite MET-1 and MET-2, list Zhou's MAE, RMSE, NRMSE, NSE and event F1, and state the within-fold identity with R^2.
- Keep `rmse`, as the critic does. The error concentrates in bloom casts, and blooms are the values the managers act
  on (the practitioner's "bloom or no bloom"; MET-1).
- `rmsle` stays a MET-10 weighing call for the curator.

**6. Factual slips: conceded in full.**
- 0.03 is a floor. Also correct: 1.82 km; 111 + 1 + 34 days; the current numbers 0.641 against 0.348 and 0.525
  against 0.439; "the screening proposed", not the curator; the reason for the day grouping reworded; the -999 counts
  marked as raw; oxygen saturation added to `known`; `original_source: Other`.
- Two of these become moot if the temporal re-split is taken: "a third of the other days sit in the same test fold"
  and the day-against-cast reason.

**Judgment after rebuttal.**

```text
Verdict: ship after changes.
Validity: USE-1 holds once narrowed to the failed-fluorometer fill at the survey (fit approximate, USE-8); USE-2 not
  triggered, glioma set apart (the features exist when the label is missing); USE-3/USE-10/SPLIT-3: re-split
  temporal (expanding, whole survey days) with the lag feature; LEAK-10, PROV-8, PROV-13 hold.
Value: TP-2: temporal RMSE 0.484-0.491 ug/l against 0.62 (mean, persistence), signal across the 2022-10 step.
Quality: floor, quenching, possible instrument periods in the notes; metric reason MET-1/MET-2; text slips fixed.
For the curator: is the failed-survey fill a decision (else No + No Good Target); ask AZTI for the instrument history.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: basque_offshore_ctd_chlorophyll (2026-11-01)**

**Where we stand.** I concede the advocate's points 2, 3, 6 and 7, and agree on the remedies of points 1 and 5. One dispute is left: which moment the task stands for, and so which split (advocate point 4). The remaining verdict is ship after changes. The one change still open is that call.

New checks, my own: rebut.py in the critic's scratch folder in the run, with its output. Untuned LightGBM with the builder's settings, R^2 on the log scale, RMSE in ug/l.

**Advocate 1 (a failed fluorometer is a real moment; glioma is different). Narrow.**
- Conceded:
  - The fact that sets this case apart from glioma holds. Glioma's label exists before its features; here the features exist exactly when the label is missing.
  - The sensors on this package do fail one channel at a time.
  - Answer the consistency check with (a), drop "a cast made without one", and keep fit approximate. That was my remedy for point 1 too.
- Disputed: the decision the advocate names, "what AZTI reports and stores", bundles two moments, and the source contradicts the "stores" half.
  - AZTI's release fills nothing. All 5 casts that lost a whole channel are published at -999 (PAR 2015-06-01 and 2016-10-17, oxygen 2017-09-04, salinity 2023-03-06, temperature and salinity 2023-12-11; my check, part 1). The descriptor calls the data "Raw".
  - The fill precedents the advocate cites fill units that were not measured, from data of the same time: 5g_energy_consumption fills stations within one week, covertype fills areas, wadden_sea fills stations within a surveyed year. None fills a past day from the days after it.
- Rule: USE-1 (Must) is met by the moment at the survey. EV-2: a measurement on the data outranks the inferred archive practice.

**Advocate 2 (the date is the channels read against their period, a legitimate input). Concede, one narrowing.**
- Conceded: `cast_date` is known when the fill is made. LEAK-10, USE-6 and TP-4 hold, and I never asked to drop it.
- Narrowing: "recalibrates on the surveys of the same period" means, under the shipped split, partly the surveys after the test day. At the period changes those later surveys are what tell the model the new level (my check, part 2):

  | Period | Real time: R^2 | Real time: mean residual (log) | Day split: R^2 | Day split: mean residual (log) |
  |---|---|---|---|---|
  | After the 2022-10 step (7 days) | -0.27 | -0.60 | 0.05 | -0.23 |
  | Start of the floor, 2018-11 to 2019-06 (12 days) | 0.32 | +0.33 | 0.35 | +0.04 |

- So the date is legitimate. How much it may tell the model depends on the moment (USE-3), which is the point 4 question.

**Advocate 3 (the split is honest; hold out the day, not the cast). Concede.** I did not contest the day. I agree with the rewording and the slips.

**Advocate 4 (both regimes ship; keep grouped). Disputed, and I narrow my own claim.**
- The advocate's ground for grouped is "AZTI's 2014-2023 release is itself such a product". It is not a filled series: 5 of 5 whole-channel failures are published as no data (Advocate 1 above).
  - No source and no practice in the source supports a fill made later.
  - The decisions the descriptor names, managing shellfish production and early warning, are taken when a survey comes in.
  - The two stations are known entities. USE-10 (Must): the split is temporal and the previous outcome is a feature.
  - The tension row "Temporal against grouped" (Lennart, 2026-10-12) asks for the one regime the use case implies.
- My claim narrowed:
  - Within repeat 0's folds, on the test days from 2019 on, the later surveys add 0.15 of R^2. The fold's training days give 0.403 with all of them and 0.254 with only those before the test day; RMSE is 0.489 against 0.514 (my check, part 3).
  - On the declared metric the real-time fill scores about the same as the day split: RMSE 0.476 against 0.489 (repeat 0) or 0.454 (9 folds, practitioner).
  - I withdraw "about 0.1 R^2 of the score comes from the future" as an effect on the metric; it holds on the log scale only. By SPLIT-4 the size decides nothing either way. The moment decides.
- Conceded:
  - The frozen-year numbers (0.10, -0.30, -0.35) understate the temporal task.
  - Both regimes can be scored, so neither choice excludes the dataset.
- Rule that wins: SPLIT-3 together with USE-10 and USE-3 (all Must), read against the source's own practice (EV-2).
- Remedy, unchanged: a temporal split with an expanding training side, refit per window (SPLIT-12, SPLIT-14, SPLIT-17), with the last measured profile as a feature.

**Advocate 5 (no leak; faithful data; the instrument period is no reason to exclude). Concede, one narrowing.**
- Conceded: LEAK-10, PROV-8 and PROV-13 hold, and we agree on the remedy: a note plus the request to AZTI.
- Narrowing: "reproducing that period's calibration is exactly what the fill must do" holds only for a fill made later. At the survey, the fill is off by a factor of about 1.8 for the surveys after the 2022-10 step (mean residual -0.60 log; table under Advocate 2).
  - The note should give these numbers: under a temporal split, the period changes are where models fail.
  - That failure is part of the honest task, not a reason to exclude.

**Advocate 6 (worth benchmarking). Concede.**
- TP-2 and TP-5 hold, and the task stays worth benchmarking under my re-split: 0.337 against -0.252 for persistence.
- One reservation on "gap +": the precedent checker counts this as the first group key in the working copy that is a calendar unit, with the date kept as a feature. That needs a Cases row under SPLIT-3 or SPLIT-24. It is not a point in its favour.

**Advocate 7 (the metric and the cleaning). Concede.**
- I agree on every fix: cite MET-1/MET-2, call 0.03 a floor, add a sentence on quenching, and mark the -999 counts as raw.
- I accept that putting the error weight on bloom bins suits a "bloom or no bloom" fill. My concentration point is a note, not a reason to change the metric. `rmse` stays, and `rmsle` is the curator's weighing call.

**Updated verdict: ship after changes.**
- Settled: text and notes for points 1 and 3 to 6, with option (a) on glioma.
- For the curator, one call: the fill at the survey (temporal, my recommendation, under USE-10 and the source's practice) or the fill made later (grouped, the advocate's, which no source practice supports).
- `No` only if the curator rejects the failed-survey moment altogether. Neither side now argues for that.

</details>
