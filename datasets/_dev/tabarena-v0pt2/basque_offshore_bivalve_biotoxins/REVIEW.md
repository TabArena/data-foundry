# basque_offshore_bivalve_biotoxins

**Outcome:** added; recommended `No` (`Too Small`), to revisit when AZTI publishes seasons after 2023. The data are
AZTI's monitoring of two offshore bivalve farms off Mendexa (Mendeley Data v2, CC BY 4.0), rebuilt from the origin
rather than from Zhou et al.'s broken benchmark copy: 280 pooled samples of 2016-2023. The target is the regulated
okadaic-acid group in ug OA eq/kg (67% at the laboratory's non-detect code 40; shipped as log, scored by RMSE on
ug/kg). It is predicted on the sampling day from the farm, the species, the newest CTD cast, and a plankton survey
and the farm's last toxin result each at least a week old, in three temporal windows. The task is real and the data
faithful; what fails is the size of the test. The windows must lie in the newest half of the samples (the 50%
training floor), and that half holds the end of the 2021 episode, the 2022 episode and a quiet year.

Validity: TP-10 (P2 via SEL-10) leg 2 holds (the last result is the only lag of the target, and the manager reads it);
leg 1 holds on point estimates in the two toxic windows, no interval clear of 0, and fails in the quiet window (issue
1). USE-1 holds, fit approximate (USE-8). USE-5 holds: the level, not the exceedance of 160, on P3 grounds.
USE-3/LEAK-10 triggered (same-day plankton counts in 136 rows), fixed. PROV-8/13/15 hold. SPLIT-1/3 hold; SPLIT-10
fixed; SPLIT-14 fixed by a floor in rows (issue 2); SPLIT-17 departed from (windows of 37 and 42 samples; SPLIT-14's
three windows leave no wider ones); SPLIT-12/20 text fixed. Value: TP-9 triggered (issue 1); MET-8 `rmse` kept, MET-11
`rmsle` open (issue 3). Quality: CLEAN-12 triggered, fixed (one Ostreopsis column); CLEAN-21 kept with a note (16 taxa
only the first laboratory counted). Weighed: source +, use case +, signal in the toxic windows +; size -, test events
from two episodes -, a quiet window that persistence wins -.

Changes made after the review panel (AI, 2026-11-01); the panel's reports describe the earlier definition, and
four of the precedent checker's five consistency checks are answered by these changes (the fifth is issue 1):
* plankton counts from surveys 7 to 21 days old, like the toxin result (the source's method rules out a same-day
  count; lags of 1, 3 and 7 days score alike; 86 samples now lack a survey, 41 before), with the CTD kept same-day;
* a 7-day gap and the 50% floor counted in rows (issue 2);
* the level's reason restated on P3 grounds, and Revilla et al. 2025 named in the metric reason;
* one Ostreopsis column and a note on 16 taxa;
* the claim audit's descriptive errors corrected.

Numbers below are measured on the definition after these changes (tuned LightGBM, CatBoost and the naive forecasts
as in the mediator's run; 95% intervals from a bootstrap over ISO weeks).

**Main points:** Retire as `Too Small`, following seismic_bumps, or keep as a tiny temporal task with a TP-9 case
that names what sets it apart (issue 1); if kept, the unit of the 50% floor (2) and the metric (3).

**Record fields that disagree with the definition:**

- `original_source`: record `Github`, definition `Other`.
- `required_split`: record `?`, definition `Temporal (NON-IID)`.

**Issues for Andrej:**

1. **Retire as `Too Small`, or keep as a tiny temporal task?**

   * **Problem:**
     - The test windows come from the newest half of the data, since every window trains on at least half of it[^1a].
     - The three windows hold only 6, 7 and 0 samples above the EU limit of 160.
     - Are these enough to score methods, or is the dataset `Too Small`?
   * **Background:** the newest half holds the end of the 2021 episode, the 2022 episode and a quiet year: 6, 7 and
     0 samples above the EU limit of 160, and 12, 11 and 2 values above the non-detect code, in windows of 37, 42 and
     59 samples. No split that keeps half the data for training avoids a quiet newest window, since the last
     exceedance is on 2022-05-23. An exceedance target is no way out: the newest window holds no exceedance.
   * **Effect on the task:** a benchmark would rank methods on 3 or 4 peak samples per toxic window (74-91% of the
     squared error) and, in the quiet window, on how close a model stays to the code 40, far below any decision. Of
     the 13 test exceedances, 3 are onsets (after a last result at or below the limit); for the other 10 the farm is
     already closed.
   * **Experiments:** the ROC AUC for the limit is 0.98 [0.90, 1.00] and 0.87 [0.74, 0.99] in the toxic windows. The
     tuned model's gain over the training mean is not clear of 0 in either toxic window ([-2.1, 43.3] and
     [-7.9, 41.1] ug/kg). In the quiet window the farm's last result, nearly always the code, scores RMSE 7.2 ug/kg
     against 19 to 27 for every model tried (gain of tuned LightGBM [-21.0, -4.7]), so the test that this is tabular
     and not forecasting fails there[^1b]. The outside inputs add nothing measurable over the farm's own series
     ([-18.2, 23.0]). The task probe finds LightGBM, a random forest and a linear model within two standard errors of
     each other over the three windows, so it gives no ground to keep under the rule that a spread of tuned methods
     keeps a dataset[^1c].
   * **Panel:** for retiring, the critic (the blind reviewer would exclude it unless some cut gives each window a
     toxic season, and none does): seismic_bumps was retired with 14 to 26 positives per window, more than here, and
     the AUC intervals above are about as wide as seismic's ±0.1 to ±0.14. For keeping, the advocate: the target is
     graded, so every sample is scored; the model ranks the exceedances (AUC lower bounds 0.90 and 0.74) and beats
     the farm's last result and its monthly profile on point estimates in both toxic windows; small real tasks are
     kept (musk). Two of the advocate's further points do not survive the changes: the quiet year scored false
     closures on 2 predictions above 160 before them and on none after; and the okadaic-acid-producing plankton added
     to a model on the farm's own series before them (pooled gain [3.5, 20.6]) but not after ([-15.1, 10.4]; all
     inputs together [-18.2, 23.0]).
   * **Rules:** too few events per test window and a task that is not tabular are each enough to retire, however
     real the task[^1d]. The quiet window fails the tabular test only because it holds nothing to predict, which is
     the too-few-events fact. The outside inputs add nothing measurable, and the windows are too thin to tell tabular
     from forecasting (the critic), so the marker is `Too Small`, not `Time-series (Forecasting)`: one decision. The
     lean to `Too Small` rests on the few events per window, not on the coded zeros (your policy call 2 of
     2026-10-30).
   * **Consistency:** retiring follows seismic_bumps; a keep departs from it and sets the precedent for the
     zero-inflated batch. Your `Yes`, priority 1 (2026-10-30) was a screening call; a probed finding supersedes
     it[^1e], so the call is yours again. The tabular test's first leg (a model on the features clearly beats the
     farm's own naive forecast) is read here as holding on point estimates in the toxic windows, with no interval
     clear of 0. You kept that test as written on 2026-11-02, with no 2-standard-error line[^1f], so a keep is judged
     on "clearly beats" against the forecasts built from the farm's own series, which these point estimates do not
     show clearly.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as a tiny temporal task (implemented) | three test windows of 37 / 42 / 59 samples (training floor counted in rows); needs issues 2 and 3 and a case recorded against seismic_bumps | a graded target scores every sample; the model ranks the exceedances and beats the last result on point estimates in the toxic windows | no gain clear of 0; the quiet window is lost to the farm's last result; departs from seismic_bumps |
     | B | `No` with `Too Small` | verdict and marker change; to revisit when AZTI publishes seasons after 2023 | follows seismic_bumps | a real task on faithful data leaves the benchmark |

   * **Recommendation:** B, `No` with `Too Small`: the windows hold too few events to score. **Decision:** A or B?

   **Notes for the AI:** this decision changes only the verdict and the marker. A keep also needs issues 2 and 3 and a
   TP-9 Cases row (or an amendment saying what "the target's spread" means for a regression with a dominant value)
   that names the fact setting it apart from seismic_bumps.

   [^1a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data.
   [^1b]: **TP-10** (Must): a panel with one series per entity is a tabular task, not forecasting, when both legs
     hold: (1) a model on the features clearly beats each entity's naive forecast on the shipped windows, by the
     declared metric; (2) the source's top solutions are tabular models on point-in-time features, with no lag of the
     target beyond its last observation known at the prediction point.
   [^1c]: **TP-3** (Must): if tuned methods spread, keep the dataset.
   [^1d]: **TP-9** (Must): when the test windows of a temporal task hold a handful of positives (or of the target's
     spread) or none, the scores are noise and the dataset is `Too Small`. With **TP-10** (Must, footnote above),
     each decides alone: principles.md, "How to decide", step 4: independent failures are not conflicts, and every
     Must has to hold.
   [^1e]: principles.md, "Precedence in the process": a later stage's measured finding supersedes an earlier stage's
     reading; a screening verdict is provisional until the dataset is added and probed.
   [^1f]: Andrej, 2026-11-02, crms_phragmites_cover issue 1: TP-10 kept as written; no 2-standard-error line adopted.

   **Andrej (2026-11-03, change):** I follow your suggestion to retire the dataset

   **Resolved (2026-11-03, Andrej):** don't ship, as recommended: the record is `No` with `Too Small` and no priority,
   its `v2_path` cleared and its claim released; the record fields take the definition's values (`original_source`
   Other, `required_split` Temporal); the folder leaves the working copy (copies of its last files in the run
   folder of 2026-11-03, `basque_bivalve_retired/`). To revisit when AZTI publishes seasons after 2023.

2. **Count the 50% training floor in rows or in sampling days?**

   * **Problem:**
     - Only if the dataset is kept (issue 1).
     - No window may train on less than 50% of the data, and the rule does not name the unit[^2a].
     - A mussel and an oyster sample of the same day share one survey and one cast.
   * **Effect on the task:** days put the tail of the 2022 episode into the quiet window, where tuned LightGBM then
     beats the last result (RMSE 39.7 against 68.7); rows leave it in training, and the model loses (19.7 against
     7.2). Days would let the dataset pass the tabular test on point estimates in all three windows. Choosing the
     unit for that picks the split for the score, which the ranking of an honest split above the score forbids
     (forest_fires)[^2b].
   * **Consistency:** your decisions so far count rows (california_house_prices_2020, alfa_battle_2_0_task_2,
     lending_club). kick (50% of its purchase dates, 48.7% of its rows; never reviewed) is the same case: it stays as
     it is under days and is re-split under rows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Rows (implemented) | windows start 2021-06-07, 2021-11-30 and 2022-07-04, 35 sampling days each; the oldest trains on 140 samples (50.0%) after the 7-day gap | follows your decisions; does not pick the split for the score | the first window holds 37 samples, and the test 13 exceedances instead of 23 |
     | B | Sampling days, as built | the oldest window trains on 45% of the samples (44% with the gap); the floor rule amended to count distinct time values when windows are cut in them | same-day samples share one survey and one cast; 23 test exceedances | picks the split that passes the tabular test; amends the rule |

   * **Recommendation:** A, rows: it follows your decisions so far and does not pick the split for the score.
     **Decision:** A or B?

   **Notes for the AI:** kick is the same case: under A it is re-split in rows, under B it stays as it is. On B, amend
   SPLIT-14 in `splits.md` to count distinct time values when windows are cut in them.

   [^2a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data.
   [^2b]: principles.md, Tensions, "The right split against the score" (P4 over P6): the split follows the
     application; a small signal under it is no reason to retire (forest_fires).

   **Andrej (2026-11-03, change):** I follow your suggestion to retire the dataset

   **Resolved (2026-11-03, Andrej):** moot: the dataset is retired (issue 1); no split is kept and SPLIT-14 is not
   amended.

3. **Score the level by RMSE or by RMSLE?**

   * **Problem:**
     - Only if the dataset is kept (issue 1).
     - The source defines no metric, so `rmse` on ug/kg is the fallback[^3a]; RMSLE would be a metric taken from the
       context, allowed only when the task makes it obvious[^3b].
   * **Experiments:** the notes carry the ROC AUC and recall at 160 per window: tuned LightGBM recalls 5 of 6 and 3 of
     7 exceedances in the toxic windows, the farm's last result 6 of 6 and 4 of 7. Bearing on issue 1, not on the
     metric (the metric is chosen by what scores the task[^3c], and the advocate does not argue from this): under
     RMSLE the model loses to the farm's last result in the quiet window (0.35 against 0.12) and, on windows cut in
     sampling days, in the 2022 window (0.75 against 0.64).
   * **Panel:** for RMSLE (the domain practitioner, the critic): the RMSE is set by peaks far above the limit, where
     the farm is closed anyway, and peaks swing 2 to 4 times within days (456, 1005 and 307 ug/kg at the Mussel Farm
     on 19, 21 and 24 May 2021); an area reopens after two results below 160 (Reg. (EU) 2019/627, Art. 63), so the
     peak's size does not set how long a closure lasts. For RMSE (the advocate): the default, and the sibling
     basque_offshore_ctd_chlorophyll uses it.
   * **Unknown:** the methods of the source team's own study, Revilla et al. 2025
     (https://doi.org/10.1016/j.rsma.2025.104556), which nobody on the panel could open, would settle it. If you can
     open it, its methods settle this issue; otherwise `rmse` stands as the fallback.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `rmse` on ug/kg (implemented) | scored by the fallback `rmse`, with the ROC AUC and recall at 160 per window in the notes | the default; as the sibling dataset | set by peaks far above the limit, where the farm is closed anyway |
     | B | `rmsle` | scored by `rmsle`, a metric taken from the context | the peak's size does not set how long a closure lasts | needs a context the task makes obvious |

   * **Recommendation:** A, `rmse`: the source defines no metric, and without the source team's study the fallback
     stands. **Decision:** A or B?

   [^3a]: **MET-8** (Should): with no metric fixed by the source, the fallback for regression is `rmse`.
   [^3b]: **MET-11** (Must), context origin: the source defines no metric, but the task makes one obvious, so the
     default would score the wrong thing; only when the context is clear, otherwise the fallback.
   [^3c]: **MET-1** (Must): the declared metric scores the real task, the decision of the use case, the way a
     practitioner would have chosen a model for it.

   **Andrej (2026-11-03, change; metric ok; dataset note):** I follow your suggestion to retire the dataset

   **Resolved (2026-11-03, Andrej):** moot: the dataset is retired (issue 1).

**Review panel:** don't ship: `No` with `Too Small`, to revisit when AZTI publishes seasons after 2023 (mediator).
Claim audit: 38 claims, 21 hold, 7 hold in part, 8 refuted (fixed in the definition or the record), 2 untested. Blind
review: include with changes; its main concern is that the last test window holds a near-constant target under most
cuts, and it would exclude the dataset if no cut gives each window a toxic season. Debate: agreed on a plankton lag
with the CTD kept same-day (the mediator set the lag to 7 days), the 7-day gap, the level on P3 grounds and the text
fixes; disputed: `Too Small` or keep (issue 1), the unit of the 50% floor (issue 2), RMSE or RMSLE (issue 3).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): basque_offshore_bivalve_biotoxins**

**Recommendation**

```text
Verdict: don't ship: `No` with `Too Small`, to revisit when AZTI publishes seasons after 2023. The curator's call
  (issue 1); if kept, ship after the changes below.
Validity: TP-10 leg 2 holds (the farm's last result is the only lag of the target, and the actor reads it). Leg 1
  holds on point estimates in the two toxic windows, with no interval clear of 0, and fails in the quiet window under
  the row floor (the farm's last result 7.2 ug/kg against 18-32 for every model). USE-1 holds, fit approximate
  (USE-8). USE-5 holds once the level rests on P3 grounds. USE-3/LEAK-10 triggered (same-day plankton, 136 rows),
  fixed (plankton surveys at least 7 days old, CTD same day). PROV-8/13/15 hold. SPLIT-1/3 hold; SPLIT-10 fixed
  (7-day gap); SPLIT-14 fixed by a floor in rows (issue 2).
Value: TP-9 triggered: 6 / 7 / 0 exceedances and 12 / 11 / 2 quantified values in the three windows; ROC AUC at 160
  per toxic window within +-0.05 to +-0.19, close to seismic_bumps' +-0.1 to +-0.14 (issue 1). MET-8 rmse kept;
  rmsle open (issue 3).
Quality: CLEAN-12 (one Ostreopsis column), CLEAN-21 note, text fixes.
Weighed: source +, use case +, signal in the toxic windows +; size -, test events from two episodes -, a quiet window
  that persistence wins -.
For the curator: issue 1 (Too Small or keep); if kept, issue 2 (the floor's unit) and issue 3 (the metric).
```

**Changes to make now (no decision needed)**

1. LEAK-10, USE-3 (Must; remedy LEAK-7; rain_in_australia: keep only what holds under both readings of the timing).
   Plankton from the newest survey 7 to 21 days before the sample, the same week the definition gives the toxin
   result; CTD on or before the day (in situ). The panel agreed on at least 1 day, but the facts both sides cite rule
   out a count by the next day: Lugol-fixed samples "preserved in the dark and cool (4 °C) until analysis", a 50 ml
   Utermöhl settling of 20 to 50 h, an outside laboratory (Sec. 4.3). The source states no plankton turnaround, so the
   definition's own reading for the other laboratory is the one that holds under both readings. Cost: none measured
   (pooled RMSE of the tuned model 104.0 / 105.8 / 100.9 ug/kg for 1 / 3 / 7 days on the row-floor windows); 86 rows
   then lack a survey (41 now). Name one turnaround per analysis in the prediction-point bullet, `known` and
   `fit_reason`, quoting Sec. 4.1 ("initiated within two days of sampling") and Sec. 4.3.
2. SPLIT-10 (Should): a 7-day gap declared on `Temporal`, the same turnaround; 6 training rows go (house_sales).
3. SPLIT-14 (Must, counted in rows as in the curator's decisions on california_house_prices_2020,
   alfa_battle_2_0_task_2 and lending_club): cutoffs 2021-06-07, 2021-11-30, 2022-07-04 (35 sampling days per window,
   day-aligned); with the gap the oldest train side holds 140 rows (50.0%). The alternative is issue 2.
4. USE-5 (Must): the `Decision` and the "Why a level" bullet give the P3 reasons (precautionary closures act below
   160; the laboratory reports the level; Cruz et al. 2022 forecast the DSP level) instead of TP-9, and say that an
   exceedance target has no positive in the newest window either.
5. SPLIT-12, SPLIT-20 (Should): `task_summary.split` and `splits_comment` say what each window is, recounted on the
   new cutoffs; delete the two refuted sentences on counting days (in `splits_comment` and "Why a level"); a
   `History:` bullet (monthly at the pilot plant 2016-2018, plankton method change 2018-06, Mussel Farm from 2019-06,
   laboratory change 2020-01, the OA group not measured in the 2020 season).
6. USE-8 (Must): `fit_reason` names the assumed turnarounds as assumptions; the thin test moves to a TP-9 note.
7. TP-10 (Must): the "tabular task" bullet gives, per window, the models against each named naive forecast with the
   intervals, the quiet window lost to the last result included.
8. MET-1, MET-11 (Must): add Revilla et al. 2025 to where we looked (Regional Studies in Marine Science,
   doi:10.1016/j.rsma.2025.104556, "Local and regional processes driving Dinophysis acuminata abundance and okadaic
   acid detection in offshore farmed mussels in the southeastern Bay of Biscay", the source team; title from Crossref,
   methods unread, the AZTI repository copy returns 404); the ROC AUC and the recall at 160 per window in the notes.
9. CLEAN-12 (Should): one Ostreopsis column (the two never overlap; renamed in 2021, Table 1 footnote a). CLEAN-21
   (Should): a note on the 16 taxa counted only by the 2014-2017 laboratory (zero in every test row).
10. Text: April 2016, not June; 42 taxa ship, not 45; the 87 samples within 3 days include 37 same-day species pairs;
    dissolved oxygen is derived from saturation, temperature and salinity, not a copy; Niskin surveys hold 1 to 6
    depths; the code 40 is "left-censored at the LOQ, kept as the low regime (Andrej, 2026-10-30)", not "not a cap";
    2020 is missing from the episodes because it was not measured; the descriptor's early warning is of blooms; the
    record's "129 above" is 125.
11. Record: `original_data_state` to `Database (or multiple to-be-joined tables)`; `original_source` and
    `required_split` as field rows; `No Good Target (yet)` dropped if the dataset is kept.

**Issues for the curator, ranked**

1. **Retire as `Too Small`, or keep as a tiny temporal task?** (TP-10 Must, P2; TP-9 Must, P6; SPLIT-16 Must)
   - Problem: the test pool is the newest half. It holds the end of the 2021 episode, the 2022 episode and a quiet
     year. On the row floor the windows hold 6 / 7 / 0 exceedances of 160 and 12 / 11 / 2 quantified values in
     37 / 42 / 59 rows. No split that meets SPLIT-14 avoids a quiet newest window: the last exceedance is on
     2022-05-23.
   - Effect: methods are ranked on 3 or 4 peaks per toxic window (84-90% of the squared error, as shipped) and, in
     the quiet window, on how close a model stays to the code 40.
   - For `Too Small` (critic): seismic_bumps was retired with 14-26 positives per window, more than here. The ROC AUC
     at 160 per toxic window is 0.98 [0.91, 1.00] and 0.89 [0.77, 0.99] after the changes (+-0.05 to +-0.19 over the
     variants run), close to seismic's. The tuned model's gain over the training-mean dummy is not clear of 0 in any
     window ([-0.9, 44.8], [-3.3, 44.8], [-4.3, 11.7]). In the quiet window the farm's last result (nearly always the
     code 40) scores 7.2 ug/kg against 18-32 for every model, gain [-33.5, -12.6], so TP-10 leg 1 fails there by the
     letter. No repair until AZTI publishes later seasons.
   - For keep (advocate): a graded target scores every row; the signal is real (AUC lower bounds 0.61 to 0.91 over
     the variants, far from 0.5; the OA-producing taxa add over a series-only model, pooled gain [3.5, 20.6], measured
     with a 1-day lag and no gap); the model beats every
     named naive forecast on point estimates in both toxic windows; tiny real tasks are kept (musk). The advocate's
     distinguishing fact, false closures scored in the quiet year, rested on 2 of 64 predictions above 160 with a
     1-day plankton lag; after the changes there are none.
   - Rule: TP-9 and TP-10 hold on their own, whatever the task's reality (principles.md, "How to decide", step 4).
     The quiet window's TP-10 loss is the TP-9 fact (nothing to predict), so one decision. The level is no way out:
     an exceedance target has no positive in the newest window.
   - Decision: `No` with `Too Small` (recommended), or keep with a TP-9 Cases row naming the fact that sets it apart
     from seismic_bumps (or an amendment of TP-9 on "the target's spread" for a dominant-value regression) and a
     TP-10 reading that a window without events is TP-9's question. The first case of the zero-inflated batch, so
     the precedent.
2. **Count the 50% training floor in rows or in sampling days?** (SPLIT-14 Must; only if kept)
   - Implemented: rows (change 3). Cost: the oldest window has 37 rows, the test holds 13 exceedances instead of 23,
     and the quiet window starts after the 2022 episode tail.
   - Alternative: amend SPLIT-14 to count distinct time values when windows are cut in them, on the advocate's honest
     ground (the rows of one day share one survey and one cast), and reopen kick (48.7% of its rows). Cost: the
     oldest window trains on 45% of the rows.
   - New fact: days put the episode tail into the quiet window, where the model then beats the last result on point
     estimates (37.7 against 68.7); rows put it in training, and the model loses (30.5 against 7.2). That flatters a
     test, which is no P4 reason (the split follows the application).
   - Decision: rows (recommended) or the amendment.
3. **Score the level by RMSE or RMSLE?** (MET-1 Must; MET-8 Should; MET-11 context; only if kept)
   - Implemented: `rmse` on ug/kg (fallback), the AUC and recall at 160 in the notes.
   - For `rmsle` (domain practitioner, critic): peaks far above 160 set the RMSE and swing 2-4 times within days
     (456, 1005, 307 at the Mussel Farm on 19, 21, 24 May 2021); Art. 63 of Reg. 2019/627 reopens an area on two
     results below 160, so the peak does not set how long a closure lasts; the limit is 4 times the LOQ.
   - For `rmse` (advocate): the default; a context metric needs the context to be clear; the sibling ships `rmse`.
     Under `rmsle` the model loses to the last result in the quiet window in every variant (0.47 against 0.12 on the
     row floor) and in the 2022 window of the shipped windows (0.72 against 0.64): TP-10 leg 1 would fail in 1 or 2
     of 3 windows.
   - Would settle it: the methods of Revilla et al. 2025.
   - Decision: `rmse` (recommended) or `rmsle`.

**Disputed points, settled**

1. TP-10, which naive forecast, chosen how. The critic took the best on each test window and asked for intervals
   (g_research_crypto_forecasting); the advocate chose on the training side and read point estimates (ashrae,
   rain_in_australia) or the pooled gain. The rule's text decides which: "clearly beats each entity's naive forecast",
   "the forecasts built from the series itself", so the model has to beat each named forecast (the last result; the
   farm's month mean and median), which is the best of them on each window; with a fixed set of two or three, no
   choice is made and hindsight does not arise. The farm median (the constant 40) is a dummy, as both now agree, and
   belongs to TP-9. Measured on the frame after the changes: ahead in both toxic windows on point estimates in every
   variant, no interval clear of 0; in the quiet window ahead on the shipped windows and clearly behind on the row
   floor. The critic's condition ("if the tuned methods also stay ahead in 3 of 3") holds on the shipped windows only.
   What is left turns on the quiet window: issue 1.
2. TP-9 against seismic_bumps: what "the target's spread" means for a regression with a dominant value is left open
   by the rule, and this is its first case: issue 1, with a lean to `Too Small` from the like case and the measured
   interval widths.
3. SPLIT-14 window option: a Must that does not name its unit. The curator's recorded decisions count rows ("Who
   decides": the curator over the AI), so rows are implemented and days need an amendment: issue 2. Preferring days
   because rows weaken TP-9 picks the split for the score (P4 over P6, forest_fires), as the critic says; the run shows
   days also flatter TP-10.
4. The metric: MET-11 allows a context metric only when the context is clear, and the panel is split, so a weighing
   call: issue 3. TP-10's result does not decide it (MET-1 asks what scores the task), but it bears on the outcome.
5. Re-opened by the mediator: the agreed plankton lag of at least 1 day does not meet LEAK-10 on the facts both sides
   cite; settled to 7 days at no measured cost (change 1).

**Decisive run** (script and outputs in the run folder, not committed). Frame after the changes: plankton at least
1, 3 or 7 days old, CTD same day, last result at least 7 days old; a 7-day gap. Untuned LightGBM (the builder's
settings, 5 seeds), LightGBM tuned on the training side (27 configurations, inner validation on the newest days with
the same gap), CatBoost (3 seeds). 95% bootstrap over ISO weeks. RMSE in ug/kg, plankton lag 7, oldest window first.

| Split | Window (rows / quantified / >160) | Tuned | CatBoost | Last result | Month mean / median | Train mean | Gain over best named naive | AUC at 160 |
|---|---|---|---|---|---|---|---|---|
| shipped + gap | 2021-04-19 (44/26/16) | 249.1 | 271.8 | 285.9 | 270.3 / 295.6 | 287.9 | [-23.8, 75.0] | 0.92 [0.83, 0.99] |
| shipped + gap | 2021-10-20 (46/10/7) | 160.5 | 151.2 | 161.9 | 196.1 / 194.5 | 179.9 | [-15.5, 32.9] | 0.89 [0.77, 0.99] |
| shipped + gap | 2022-06-06 (64/3/0) | 37.7 | 31.9 | 68.7 | 207.7 / 103.0 | 34.0 | [-35.3, 87.0] | - |
| rows + gap | 2021-06-07 (37/12/6) | 83.9 | 95.9 | 159.9 | 115.1 / 114.9 | 113.0 | [-20.2, 51.6] | 0.98 [0.91, 1.00] |
| rows + gap | 2021-11-30 (42/11/7) | 161.2 | 161.0 | 189.2 | 214.4 / 203.9 | 188.2 | [-6.4, 96.4] | 0.89 [0.77, 0.99] |
| rows + gap | 2022-07-04 (59/2/0) | 30.5 | 17.6 | 7.2 | 198.5 / 105.9 | 33.3 | [-33.5, -12.6] | - |

Lags 1 and 3 give the same picture (quiet window on the row floor: last result 7.2 against 18.6-30.2 for every model).
Pooled over the row-floor windows, the tuned model (100.9) beats each fixed naive forecast with intervals clear of 0
(last result 133.3, [6.4, 63.9]) but not the best of each window (120.3, [-1.3, 49.7]). No quiet-window prediction
crosses 160 after the changes.

**Agreed facts**

- 280 pooled samples at two farms, 2016-04-15 to 2023-06-22. Target OA + DTX1 + DTX2 in ug OA eq/kg, the regulated
  sum; 188 (67.1%) at the non-detect code 40, left-censored at the LOQ of both laboratories; 92 quantified from 41
  up; 47 above 160 in five spring episodes (2017, 2018, 2019, 2021, 2022; the 2020 season was not measured).
- The frame rebuilds with 0 cells different; the blind reviewer matches the target and the last result on 280 of 280
  rows; licence CC BY 4.0 and the checksums match. Zhou et al.'s copy pools 24 toxins in five units (PROV-15); the
  rebuild from AZTI's release stands (PROV-13).
- 136 rows use a plankton survey from their own day; the source's method rules out a count that day. The CTD is
  measured in situ. The 7-day toxin lag is conservative (Sec. 4.1), and fresher results do not help persistence.
- As shipped: windows 44/26/16, 46/10/7, 64/3/0; the oldest train side holds 126 rows (45.0%) and 120 of 237 days
  (50.6%). Both sentences that justify counting days are false (exceedance months hold 27.0% of the days and 27.1%
  of the rows; counted in rows the pool starts on 2021-06-07 with 13 exceedances).
- No gap; 6 training rows fall within 7 days of a window start, and a 7-day gap changes nothing measurable.
- Window 1 opens 40 days into the 2021 episode (8 of its 24 exceedances in training); only window 2 is a refit
  before a season.
- The top 3 or 4 samples carry 84-90% of each toxic window's squared error; 5 test rows are onsets (an exceedance
  after a result at or below 160), and 18 of 23 test exceedances fall while the farm is closed.
- The farm median (40) is a dummy, not a TP-10 naive forecast. With all features the plankton and CTD add nothing
  over a series-only model (pooled [-21.0, 13.2]); the OA-producing taxa alone do ([3.5, 20.6]).
- The level is the decision's quantity on P3 grounds (precautionary closures below 160, the laboratory reports it).
- The descriptive errors of change 10, and the record fields of change 11.

**Consistency with precedent**

- seismic_bumps (TP-9, `Too Small`, 2026-09-30): followed. A keep departs from it and needs the fact that sets this
  case apart; the run weakened two candidates (the AUC intervals are close to seismic's; no quiet-year prediction
  crosses 160 after the changes). digicow (9 and 5 adopters per window, `Too Small`) points the same way. coffee_rating_prediction was kept with spread in every
  window, which this dataset lacks in its newest one.
- TP-10: ashrae_great_energy_predictor_iii (ahead in 3 of 3 by 8-11%) and rain_in_australia (ahead in 9 of 9) never
  lost a window to persistence; g_research_crypto_forecasting had every interval above. This dataset meets none of
  these on the row floor.
- rain_in_australia (inputs kept only where known under both readings of the timing): followed by the 7-day plankton
  lag.
- SPLIT-14 in rows (california_house_prices_2020, alfa_battle_2_0_task_2, lending_club): followed; kick (days,
  never reviewed) is reopened only if the curator amends.
- house_sales (a one-week gap for a delay of about 6 days): followed.
- blood_tests_drink_prediction, forest_fires (ship on the log scale, score on the original): followed by `rmse` on
  ug/kg.
- coad, corporate_credit_rating (repair from the origin): followed.
- Andrej's calls of 2026-10-30: the tag stays and the code 40 is a cleaning choice (policy questions 2 and 4). The
  `Too Small` lean rests on the few events per window, not on the zeros, so it does not depart from policy 2 ("any
  relevant predictive task, independent if it is zero inflated or not"). The CC `Yes`, priority 1, was a screening
  call; under the stage order a probed finding supersedes it, and the curator decides.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: basque_offshore_bivalve_biotoxins (2026-11-01)**

**Verdict: ship after changes.** Most counts hold to the row: the frame rebuilds exactly (0 cells differ), the last result recomputed from scratch matches, and the window counts, the TP-10 numbers and the metric reason's quote all reproduce. Four claims fail a test. (1) Same-day plankton counts known on the sampling day: the source's own method description contradicts it (USE-3 / LEAK-10 / USE-4, Must, P4). (2) The two sentences that justify counting the 50% floor in sampling days are wrong on their numbers (SPLIT-14, P4). (3) "Refit before each toxic season" is wrong for the oldest window. (4) A handful of descriptive numbers are wrong. TP-10 leg 1 holds on point estimates but not "clearly". The metric is computable, but in the toxic windows 1 to 3 samples carry the score.

Scripts and outputs: the run folder (not committed). All model numbers come from the builder's untuned LightGBM configuration (mean of 5 seeds), log target, scored in ug/kg on the 3 shipped windows (EV-8). Windows are listed oldest first, as in the notes: spring 2021 / spring 2022 / the quiet year.

**Claims table**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| Same-day plankton counts are known on the sampling day, before the toxin result ("our reading") | curation_comments, Prediction point and Same-day bullets; task_summary known / use_case | Read the source's method; rebuild with plankton strictly earlier (>= 1 day) and same-day CTD kept | **refuted** (source text), cost measured | DiB Sec. 4.3: samples "fixed with acidic Lugol's solution and preserved in the dark and cool (4 °C) until analysis", a 50 ml subsample "sedimented" and counted under inverted microscopes by an outside lab (UPV/EHU, Oceansnell). 136 of 280 rows (48.6%) use a same-day survey. Plankton >= 1 day: RMSE 249/128/22 -> 265/137/45, AUC@160 0.924/0.971 -> 0.871/0.923; still beats the last result (286/162/69). Plankton >= 7 days (the toxin lag): 255/157/38, so in spring 2022 the margin over the last result shrinks to 157 vs 162 | USE-3, LEAK-10, USE-4 (Must) |
| Same-day CTD known on the sampling day | same bullets | Source: in-situ profiler | holds | DiB: "hydrographic variables were measured in situ" (CTD); chlorophyll is the fluorometer channel | USE-3 |
| Floor in days because "samples would let the outcome set the windows" | splits_comment | Share of days vs samples in months with an exceedance | **refuted** | 27.0% of sampling days (64/237) vs 27.1% of samples (76/280) fall in exceedance months. Daily sampling during episodes adds days as well as samples. Counting days only removes the 43 same-day pairs (37 mussel+oyster at one farm, 6 two-farm days), and those are no more common in episodes (oyster share 17.1% vs 15.7%) | SPLIT-14 (Must), EV-1 |
| "Counted in samples, the test pool would start in July 2021 and hold one episode (spring 2022, 7 exceedances)"; also "the test pool from 2021-07 holds 7 exceedances" | splits_comment; "Why a level" bullet | `temporal_window_splits(unit="rows", window=None, n_windows=3, min_train_fraction=0.5)` on the frame | **refuted** | The pool starts 2021-06-07 and holds 13 exceedances (6 in June 2021, 7 in spring 2022). Windows: 46 rows each, 12/12/1 quantified, 6/7/0 above 160, train 142 (50.7%). One day (2022-11-30) straddles train and test, so a usable variant has to be day-aligned. Cutting at the 140th sample instead starts the pool at 2021-06-01 (7 + 7 exceedances) | SPLIT-14, TP-9 |
| Oldest window trains on 50% of the days and 45% of the samples (126) | splits_comment | Count | holds | 120/237 days (50.6%); 126/280 samples (45.0%). Precedents for counting distinct time values: anes_voting_2026 (40% of rows), kick (48.7%), numerai_v5_2_1m (49.4%) | SPLIT-14 |
| Windows 2021-04-19..2021-10-18 (44, 26, 16), 2021-10-20..2022-05-31 (46, 10, 7), 2022-06-06..2023-06-22 (64, 3, 0); 237 sampling days | splits_comment; decision | Recount on the shipped splits | holds | Exact. Train max < test min in every window; no day in both | SPLIT-11 |
| "As for a model refit before each toxic season" | splits_comment; task_summary split | Dates of the 2021 exceedances vs the oldest window's start | **refuted** (oldest window) | The first 2021 exceedance is on 2021-03-10. The oldest window opens 2021-04-19, so 8 of the 24 exceedances of 2021 are on its train side: a refit 40 days into the episode. The other two windows do start before or after a season | SPLIT-12, USE-8 |
| Horizon 12 months = the newest window's year (refit cadence) | splits_comment | Window lengths | holds | Windows of 6, 7 and 12 months | SPLIT-12 |
| TP-10 leg 1: the model beats the farm's last result and its month mean, 249/128/22 vs 286/162/69 and 277/195/208; without the last result 259/154/42 | curation_comments | Re-run; paired bootstrap of the RMSE gain; other scales | holds on point estimates; **"clearly" not established** | Reproduced: 249.4/128.3/21.9 vs 285.9/161.9/68.7. 90% bootstrap CI of the gain over the last result: [2.5, 90.8] / [-12.9, 78.7] / [-15.5, 91.2], so it spans 0 in 2 of 3 windows. On MAE: 123 vs 164, 56.5 vs 55.0 (a tie), 14.0 vs 10.6 (a loss). On log RMSE the model loses in the quiet window (0.354 vs 0.321). The farm's training median, 40 (a forecast built from the series), scores 3.3 against the model's 21.9 in the quiet window | TP-10 (Must), EV-3, EV-9 |
| The 7-day toxin lag is our reading | Prediction point bullet | Re-score with the last result at >= 1, 2, 3 days (the model gets the same lag) | holds (conservative, and not what makes the task tabular) | Model 234/136/18.7 (lag 1) to 233/117/18.6 (lag 3) vs persistence 321/155/69 to 336/142/69. Fresher results do not make persistence stronger. The real turnaround cannot be verified | TP-10, USE-3 |
| Last result = the farm's highest OA-group value on its latest day >= 7 days earlier, with its age; the only lag of the target | curation_comments | Independent recomputation from the frame | holds | Values and ages identical for all 280 rows; 3 missing (each farm's first samples) | TP-10 leg 2 |
| Target = OA + DTX1 + DTX2 in ug OA eq/kg, non-detect coded 40 = OA's LOQ at both labs; 188/280 (67.1%) at 40; DTX1 never quantified, DTX2 three times next to a quantified OA | curation_comments; record Assessment | Raw long table | holds | Units "µg OA equivalent/kg". OA "<" values: 40 at INTECMAR and ANFACO. DTX2 = 59/52/25 on 2022-05-02/03/09, next to OA 571/911/581. Quantified OA from 41 up. PTX (in the pre-2021 regulatory group) is never quantified, so leaving it out changes nothing. Note that DTX2's LOQ is 24, not 40 | USE-5, PROV-13 |
| 47 exceed 160 in five spring episodes (2017, 2018, 2019, 2021, 2022); 92 quantified; 45 quantified below the limit | curation_comments; decision | Count | holds | 47; months 2017-03..05, 2018-05..06, 2019-03..05, 2021-03..06, 2022-04..05; 45 in (40, 160] | TP-9 |
| 344 samples, 280 with the OA group; 64 without (22 DA-only 2013-2015, 42 partial panels 2020-2021) | curation_comments | Group the raw table by station, date, mollusc | holds | 344 / 280 / 22 / 42 (12 of the 42 are DA-only); all 280 carry OA, DTX1 and DTX2; one lab per sample | PROV-13 |
| Raw sizes: 5,446 rows, 24 variables; 531 depth samples, 45 taxa, 152 surveys; 180 CTD casts | curation_comments | Count | holds | Exact (CTD: 145 Mendexa-Control + 35 CTD-Mussel Farm) | EV-7 |
| INTECMAR to 2019-12 with one decimal, ANFACO from 2020-01 in whole numbers; same LOQs | curation_comments | Raw | holds | INTECMAR to 2019-12-10, 94% of quantified OA non-integer; ANFACO from 2020-01-22, 0% non-integer; OA-group LOQs equal | CLEAN-19 |
| 41 samples without a survey within 14 days; 136 with a survey on their day | curation_comments | Count | holds | 41 missing; plankton age 0 in 136 rows (CTD age 0 in 115; CTD missing in 79) | EV-7 |
| "87 samples within 3 days of the farm's previous one" (evidence for daily sampling in episodes) | curation_comments | Gaps per farm | holds as a count, **misleading** | 37 of the 87 are same-day mussel+oyster pairs; 50 are 1 to 3 days after the previous sample. Daily sampling does occur (minimum gap 1 day) | writing |
| Taxa never counted in a matched survey are dropped; "45 potentially toxic plankton taxa" in known | curation_comments; task_summary known | Compare the shipped columns with the raw columns | drop holds; **"45" refuted** | 42 taxa ship. The 3 dropped (Dinophysis cf. ovum, Phalacroma mitra, Chrysochromulina/Imantonia/Phaeocystis) are counted only in 2014-2015, before the OA panel | CLEAN-5, writing |
| Plankton max over "three to six Niskin depths until 2018-05, three hose layers from 2018-06" | curation_comments | Depths per survey | mostly holds | Niskin: 26 surveys with 6 depths, 12 with 3, 1 with 2, 1 with 1; hose always 3 | writing |
| Dissolved oxygen dropped as "a copy of the saturation" | curation_comments | Regression on the raw CTD | holds in substance, **wording refuted** | r = 0.71 with saturation alone; R² 0.9985 from saturation × (1, T, S), so it is redundant given shipped columns, not a copy | CLEAN-12 |
| Coordinates one value per farm; species a copy of the shellfish type | curation_comments | Raw | holds | 1 lat/lon per station; species and type map 1:1 | CLEAN-5 |
| Row: "280 samples, June 2016 to June 2023" | task_summary row | Dates | **refuted** | First sample 2016-04-15 (the curation comment itself says 2016-04-15) | writing |
| Test samples come after all training samples | task_summary split | Splits | holds | No shared day; train max < test min | SPLIT-1 |
| "The source names this early-warning use but builds no model" | task_summary use_case, fit_reason | DiB text; search | **partly holds** | The DiB's early warning is "for toxic algal blooms" and needs other sources; the decision it names ("ban the sales when the biotoxins exceed") is taken on measured toxins. Revilla et al. 2025 (Regional Studies in Marine Science 91:104556, the same AZTI team, OA in these offshore mussels 2017-2022) does frame OA early warning. Its abstract, seen only through search summaries, says local monitoring alone cannot predict OA "with the necessary accuracy and promptness". Not cited anywhere; full text unread (Elsevier 403, AZTI DSpace 404) | USE-1, EV-2 |
| Metric: fallback RMSE in ug/kg, log target; the reason quotes Zhou et al. Sec. 2.4 and names DiB and Mendeley as places looked | `metric = Metric.fallback(...)`; README Metric block | Quote check; `scorer(container)` on dummies per fold; MET-1 look again | quote holds; computable; **"where we looked" incomplete** | Zhou Sec. 2.4: "For cross-dataset comparability, we use the coefficient of determination (R²) as the primary benchmark indicator". The scorer inverts the log (manual RMSE matches). No scoring columns needed. Dummies per fold: train mean on log 288/180/33.8, code 40 303/189/3.3, perfect 0. Revilla et al. 2025 is missing from the reason; whether it fixes a criterion is untested | MET-1, MET-2, MET-3, MET-11 |
| RMSE on ug/kg scores the closure decision at 160 | implied by the reason | Share of squared error per sample; predictions crossing 160 | **weak** | Toxic windows: the largest error carries 51% / 48% of the SSE, the top 3 carry 84% / 89%. Quiet window: 72% of the SSE is on non-detects; no prediction crosses 160 (max 149), so the window does not score the closure decision | MET-1, MET-10 (Weigh) |
| "The level keeps every window scorable" | curation_comments; decision | Target spread per window | holds in the letter, weak in substance | Newest window: 61 of 64 at the code, 3 quantified (max 60); the constant 40 scores 3.3 | TP-9 (Must) |
| Exceedance target unscorable in the newest window | metric reason; decision | Count | holds | 0 above 160 among 64. A detection target (> LOQ) would also have only 3 positives there | TP-9 |
| Warning `task_target_value_dominant` accepted: log(40) is the non-detect code, the low regime, not a cap or missing | builder report; notes | Raw flags | holds (curator's 2026-10-30 definition) | All 188 are OA "<" at the LOQ; quantified values from 41 up. It is a left-censored code, which the curator's policy answer 2 settles | curator CC 2026-10-30 |
| No row is a copy across the split | implied | Leak probe | holds | 0.0% exact feature copies; same-day pairs stay in one window | LEAK-21 |
| Licence CC BY 4.0; year 2025 (v1 2025-03-26); sha256 prefixes | dataset.py | Mendeley API JSON; sha256sum | holds | data_licence "CC BY 4.0"; v1 2025-03-26, v2 2025-05-23; b2e49eb1 / 716abd69 / d7a00558 match | PROV-9 |
| Zhou's copy pools 24 toxins in five units; coordinates only | curation_comments; record | Repo `configs/config.yaml` | holds | `target_col: VALUE` over the whole long table (5 unit types); their RF/XGB R² is about 0 (`biotoxin_diagnostic_summary.csv`) | PROV-15 |
| Record: 93.6% "<"; about 290 dates; site ranges; 16 of 24 never quantified; OA 67.1% with 92 from 41 up | record screening / Assessment | Raw | holds | 93.63%; 293 dates; AZTI 2013-12-03..2023-06-22, MF 2019-06-17..2022-08-23; 16 | EV-7 |
| Record: "yessotoxin 55.2% at 0.06 with 129 above" | record Assessment | Raw | **refuted (minor)** | 129 quantified, 4 of them equal to the LOQ 0.06, so 125 above | writing |
| Record fields `original_source: Github`, `original_data_state: One Table`, `required_split: ?`, marker `No Good Target (yet)` | record front matter | Against the definition | **refuted / outdated** | The origin is Mendeley (Other, PROV-8), three tables, a temporal split, a built target. The builder already proposes the first three | PROV-8 |
| Zhou's "5,076 rows" reproduced by an earlier triage | record | not re-run | untested (not load-bearing) | The paper states N = 5076 | |
| Lab turnaround times | builder report | none possible | untested | Not stated in the DiB; see the lag test above | EV-7 |

**Refuted and untested claims, ranked (P1 first, Must first)**

1. **Same-day plankton counts known at the prediction point (P4; USE-3, LEAK-10, USE-4, Must).** The definition puts the prediction point at "the day a bivalve sample is taken". But the source says the water samples from that cruise are Lugol-fixed, stored "until analysis" and counted by an outside lab after sedimentation (DiB Sec. 4.3). That a count could be ready on the day contradicts the source's method (EV-2: primary document over our reading). The plankton lab being faster than the toxin lab is not stated either. 136 rows (48.6%) depend on this.
   *What it changes:* a feature not known at the prediction point is in 49% of the rows. With plankton strictly earlier the scores are 265/137/45 RMSE and AUC@160 0.871/0.923, against 249/128/22 and 0.924/0.971 as shipped. The model still beats the last result in every window. USE-8 also says a leak kept on purpose is named as kept, not counted as a fit gap, as `fit_reason` does now.
   *Mildest remedy:* take plankton from surveys strictly before the sample day (shift only the plankton call of `_latest_before` by one day; `plankton_survey_age_days` >= 1) and keep same-day CTD (in situ). If the curator keeps same-day counts, that needs evidence of the turnaround and a `Potential leak, kept on purpose:` note.
2. **The reasoning behind the days-based 50% floor (P4; SPLIT-14, Must).** Both supporting sentences are wrong. Days are as outcome-driven as samples (27.0% vs 27.1%). Counted in samples, the test pool starts 2021-06-07, not July, and holds 13 exceedances over two episodes, not 7 in one. The days reading itself has precedents (anes_voting_2026 at 40% of rows, kick, numerai), so compliance is a curator call, not a clear breach.
   *What it changes:* the stated cost of a 50%-of-samples floor is overstated. That alternative keeps 12/12/1 quantified and 6/7/0 exceedances per window, against 26/10/3 and 16/7/0 now.
   *Mildest remedy:* correct the two sentences (splits_comment and the "Why a level" bullet). Optionally offer the curator a day-aligned 50%-of-samples floor, because plain `unit="rows"` splits 2022-11-30 across train and test.
3. **"A model refit before each toxic season" (P4; SPLIT-12 / USE-8, Should).** The oldest window opens 40 days into the 2021 episode, with 8 of its 24 exceedances in training.
   *What it changes:* that window tests the second half of an episode whose onset the model has seen. It does not test early warning of an onset.
   *Mildest remedy:* reword task_summary.split and splits_comment. Cutoffs at season starts would break the 50% floor, so changing the split is not the fix.
4. **TP-10 leg 1 "clearly beats" (P2 via SEL-10; TP-10, Must).** It holds on point estimates on the declared metric. But the bootstrap gain spans 0 in spring 2022 and in the quiet year. On MAE the model ties the last result in spring 2022 and loses in the quiet year. The farm's median (40) beats it 3.3 vs 21.9 in the quiet window.
   *What it changes:* the scope verdict rests on one clear window (spring 2021) on untuned probes.
   *Mildest remedy:* read it against the tuned results on the shipped splits before closing (TP-1, EV-3), and say "beats in point estimates" rather than imply a clear margin.
5. **Score resolution (P6; TP-9 Must, MET-1 / MET-10).** "Every window scorable" holds only mechanically. The newest window scores closeness to the code: 61 of 64 at 40, 72% of the SSE on non-detects, no prediction near 160. In the toxic windows the top 3 samples carry 84-89% of the SSE.
   *What it changes:* the benchmark score is close to the error on 3 to 6 peak samples plus a quiet-year calibration term. That supports the builder's draft issues 1 and 4.
   *Mildest remedy:* put the numbers in the notes and leave TP-9 to the curator (keep as a tiny temporal task, or `Too Small`). A context metric (rmse on the log scale) would be the curator's call; the rules do not make it obvious.
6. **"Where we looked" (P6; MET-1 Must / MET-11), untested.** Revilla et al. 2025 (doi:10.1016/j.rsma.2025.104556) is the source team's own early-warning study of OA in these mussels. It appears in neither the metric reason, the record nor the use case. I could not read it.
   *What it changes:* possibly the use case's citation, a detection framing, and the fit (its abstract judges local monitoring insufficient).
   *Remedy:* a human reads its methods (Sec. 2) and adds it to the reason and the record. The fallback probably stays.
7. **Descriptive errors (writing, P7).**
   - task_summary.row: "June 2016" should be April 2016.
   - task_summary.known: "45" taxa should be 42.
   - "87 within 3 days" includes 37 same-day species pairs.
   - DO is "redundant given saturation, T and S", not "a copy".
   - The Niskin surveys hold one to six depths, not three to six.
   - The record's "129 above" should be 125.
   - The use_case's "the source names this early-warning use": the DiB names early warning of blooms.

   *Remedy:* edit the text; nothing is rebuilt.
8. **Record fields (P5; PROV-8).** `original_source` -> Other, `original_data_state` -> three tables, `required_split` -> Temporal, and the `No Good Target (yet)` marker is outdated once the level ships. *Remedy:* the curator updates the record (the builder proposes the first three).

Untested, and not a decision-changer: the real lab turnaround. Shorter toxin lags (1 to 3 days) keep the model ahead of persistence, so the 7-day reading is conservative, not a leak. Zhou's 5,076-row reproduction was not re-run.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): basque_offshore_bivalve_biotoxins**

**Verdict:** ship after one change. One column block breaks the prediction point as written: the 42 plankton counts (and their method and age columns) come from a survey on the sampling day in 136 of 280 rows, and a Utermöhl count cannot exist on that day. The remedy is to match plankton surveys from strictly earlier days and keep the same-day CTD. The rest are P7 notes: 16 taxa columns depend on which lab counted them, Ostreopsis sits in two columns, and three wordings need fixing. No column encodes the label, none is recorded after the outcome, and no proxy missing value survives.

Frame read through `dataset_io.from_definition`: 280 rows, 58 columns (57 features plus the target), 3 temporal windows (test 64 / 46 / 44 rows). Codebook: the descriptor (Solaun et al. 2025, Data in Brief 61:111736, full text in the run folder) and the Notes sheets of the three Excel files. Scripts and outputs: the run folder (not committed). Scores are untuned LightGBM, the mean of 5 seeds, on the shipped windows in the order newest (2022-06 to 2023-06), middle (2021-10 to 2022-05), oldest (2021-04 to 2021-10), given as RMSE in ug/kg and ROC AUC of the predicted level for the 160 limit. The setup is the builder's, and it reproduces the builder's numbers.

**Column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `station` | The bivalve installation: AZTI pilot plant or Mussel Farm (Notes; descriptor Sec. 4.1) | yes | category, 2 levels; coordinates and datum (one value per farm) dropped | fine | CLEAN-3, CLEAN-14 |
| `sample_date` | UTC date of the bivalve sampling | yes | datetime, 237 days; the time index | fine | CLEAN-14, CLEAN-23 |
| `shellfish` | TYPE OF MOLLUSC: Mussel (235) or Pacific oyster (45). The 2 flat-oyster rows are DA-only, so none reaches the 280 | yes | category; `SPECIES` dropped as a copy | fine | CLEAN-5 |
| `laboratory` | The toxin lab: INTECMAR to 2019-12, ANFACO from 2020-01 (Table 3) | yes (the contracted lab) | category; constant in every test window | fine (dropping it with the method: 21.3 / 138.2 / 250.3 against 21.9 / 128.3 / 249.4) | CLEAN-14 |
| 24 stable taxa: `plankton_pseudo_nitzschia_spp_lt5um`, `_spp_gt5um`, `_alexandrium_sp`, `_cf_gymnodinium_catenatum`, `_dinophysis_acuminata`, `_acuta`, `_caudata`, `_fortii`, `_infundibulum`, `_sacculus`, `_tripos`, `_phalacroma_rapa`, `_rotundatum`, `_prorocentrum_lima`, `_gonyaulax_spinifera`, `_lingulodinium_polyedra`, `_protoceratium_reticulatum`, `_dinophyceae_thecata_heterocapsa_azadinium_like`, `_gymnodiniales_karlodinium_like`, `_karenia_cf_mikimotoi`, `_karenia_sp`, `_gonyaulax_polygramma`, `_phaeocystis_cf_pouchetii`, `_prorocentrum_cordatum` (all `plankton_`) | Cells per litre, Utermöhl count of a 50 mL subsample (Sec. 4.3); each taxon's maximum over the survey's depths, from the newest survey of the past 14 days | **only when the survey is older than the sampling day**: 136 rows match a same-day survey, which is not counted until 1 to 2 days later | float64 counts, true zeros (not observed), no proxy codes, no negatives; 41 rows have no survey: missing. The maximum over depths was checked against the bivalves' layer only and does no better | **leak, moderate** (problem 1) | LEAK-10, USE-3 |
| 16 taxa counted only by the 2014-2017 lab: `plankton_pseudo_nitzschia_americana_brasiliana`, `_galaxiae`, `_multistriata`, `_pungens`, `_alexandrium_ostenfeldii`, `_alexandrium_tamarense_complex`, `_cf_azadinium_spp`, `_cf_karlodinium_spp_10_20_um`, `_cf_pfiesteria`, `_karenia_cf_papilionacea`, `_cf_pseudochattonella`, `_cf_vicicitus_globosus`, `_heterosigma_akashiwo`, `_phaeocystis_globosa`, `_prymnesiophyceae_prymnesium_phaeocystis_like`, `_takayama_sp` | As above. Above zero only in surveys counted by UPV/EHU (2014-05 to 2017-05); the later lab (OCEANSNELL, from 2017-12) never records them (one exception: 1 Karlodinium count) | same as above | float64. Zero from 2017-12 on means "not resolved at this level", not "absent"; above zero in 22 training rows only, and zero in all 154 test rows | the leak of problem 1, plus a cleaning note (problem 4) | LEAK-10; CLEAN-21 |
| `plankton_ostreopsis_cf_siamensis`, `plankton_ostreopsis_spp_siamensis_ovata` | One light-microscopy record, renamed in 2021 when O. cf. ovata arrived (Table 1, footnote a) | as above | two columns for one series. Never both above zero: siamensis is last above zero on 2020-01-22, spp. first on 2021-08-09 | the leak of problem 1, plus a cleaning note (problem 5) | CLEAN-12, CLEAN-21 |
| `plankton_sampling_method` | Niskin bottle (to 2018-05) or Lindahl hose (from 2018-06) | as the plankton columns | category; missing with the survey | fine, apart from the same-day timing of problem 1 | CLEAN-14 |
| `plankton_survey_age_days` | Days from the matched survey to the sample (0 to 14) | yes | float64; missing with the survey | fine (once the lag of problem 1 is in, its minimum becomes 1 or 2) | CLEAN-19 |
| `ctd_temperature_c`, `ctd_salinity_pss78`, `ctd_sigma_theta_kg_m3`, `ctd_light_transmission_pct`, `ctd_chlorophyll_a_ug_l`, `ctd_oxygen_saturation_pct` | In-situ CTD profile, mean over 1-12 dbar (the bivalves hang at 3-12 m) of the newest cast of the past 14 days | yes, same-day included: the instrument reads in situ during the trip | float64. -999 (Notes: "NO DATA") masked before the mean; no other proxies or negatives in the layer. Ranges are plausible (11.7-23.1 °C, 33.9-35.6 PSS, chlorophyll 0.03-4.9, saturation 92-119%). 79 rows have no cast (80 for oxygen) | fine | CLEAN-10, CLEAN-11 |
| `ctd_cast_age_days` | Days from the matched cast to the sample | yes | float64 | fine | |
| (dropped) PAR, dissolved oxygen | PAR depends on the hour and the cloud cover of the cast. DO in ml/l | n/a | DO is dropped as "a copy of the saturation". It is not a copy (r = 0.50 in the layer) but a function of saturation, T and S (R^2 0.998), as `ctd_sigma_theta` is of T and S, which stays | fix the wording (problem 6) | CLEAN-5, CLEAN-22 |
| `last_result_oa_group_ug_kg` | The farm's highest OA-group value (non-detects at the code 40) on its latest sampling day at least 7 days before, over both shellfish | yes, conservatively. The descriptor says samples were "refrigerated for biotoxin analysis when the determination could be initiated within two days of sampling; otherwise, they were frozen" (Sec. 4.1) | float64; 3 missing (first sample per farm) | fine. The target's own history under a temporal split | LEAK-34, USE-10 |
| `last_result_age_days` | Days since that sample (7 to 308) | yes | float64 | fine (dropping all three age columns: 20.7 / 129.5 / 247.8) | |
| `log_oa_group_ug_kg` (target) | ln of OA + DTX1 + DTX2 quantified, in ug OA eq/kg; a sample with none quantified takes 40 | n/a | "<" values are 40 for OA and DTX1 at both labs and 24 for DTX2. DTX2 is quantified only on 2022-05-02/03/09, each time with a quantified OA. PTX1 and PTX2 are never quantified, so the pre-2021 legal sum (which included PTXs) equals the target. 188 rows sit at the code 40, 92 are quantified from 41 up | fine | CLEAN-16, LEAK-26 (a code, documented) |

**Problems, ranked (principles.md: P4 before P7, Must before Should)**

**1. P4, LEAK-10 and USE-3 (Must): same-day plankton counts are not known on the sampling day; leak of moderate strength.**
- **Evidence (method and timing):** the prediction point is "the day a bivalve sample is taken", and in 136 of the 280 rows the plankton features come from a survey on that day. The descriptor (Sec. 4.3) describes Lugol-fixed samples, "a subsample (50 ml) was sedimented" and counted by the Utermöhl method. A 50 mL subsample takes about 24-50 h to settle ([EPA phytoplankton SOP](https://www.epa.gov/system/files/documents/2021-12/lg401.v07-phytoplankton-analysis_rfa.pdf): 50 h for 50 mL; [CCE-LTER](https://ccelter.ucsd.edu/wp-content/uploads/bibliodocs/0290ccelter.pdf): 24-48 h). The counting lab from 2017-12, OCEANSNELL, is in Manises (Valencia) per the author affiliation, far from the site. So a same-day count arrives two or more days after the sampling.
- **Evidence (the toxin turnaround):** the toxin analysis starts within two days for refrigerated samples (Sec. 4.1). That makes the two turnarounds similar, so there is no time between the plankton count and the toxin result in which a prediction could be made. The definition gives plankton a 0-day turnaround and toxins 7 days. This argument is inferred from the methods, not a stated turnaround.
- **Strength (measured):** lag only the plankton (surveys at least 1 day old) and keep the same-day CTD and the 7-day toxin lag. RMSE goes from 21.9 / 128.3 / 249.4 to 39.4 / 134.0 / 263.7, and the AUC for 160 from 0.971 / 0.924 to 0.923 / 0.884 (middle and oldest windows). The model still beats the farm's last result (68.7 / 161.9 / 285.9) and its month mean (207.7 / 195.2 / 276.9) in every window.
- **A consistent turnaround of 2-3 days for both labs** (plankton at least 2 days old, toxin result at least 3 days old): 33.4 / 127.5 / 260.2, AUC 0.938 / 0.902.
- **The builder's alternative overshoots:** it also lagged the CTD, which is read in situ. That alternative gives 59.6 / 135.5 / 257.8 and costs the newest window most of its score.
- **Mildest remedy (LEAK-7, fix the definition):** in `_latest_before` for the plankton only, match surveys strictly before the sample date (at least 1 day, or 2 days for settling plus shipping). Keep the CTD on or before the day. Rewrite the prediction-point bullet and `task_summary.known` to give one turnaround per analysis.
- **For the curator:** the exact lags (1 or 2 days for plankton; 7 or about 3 for toxins) are a weighing call on unstated turnarounds. A plankton count from the sampling day itself conflicts with the prediction point as written, under any choice.

**2. P4, claim wording (no change to the data): "The turnaround of either analysis is not stated".**
- **What the descriptor says:** samples were "refrigerated for biotoxin analysis when the determination could be initiated within two days of sampling; otherwise, they were frozen" (Sec. 4.1). So the 7-day toxin lag is conservative for refrigerated samples, and only the frozen ones have an unknown delay.
- **The 7-day lag does not leak:** shortening it to 3 days improves the scores (18.6 / 116.8 / 233.3, AUC 0.989 / 0.929). So 7 days errs on the safe side.
- **Remedy:** quote the sentence in the prediction-point bullet and in `fit_reason`.

**3. P4, checked, no action: plankton missingness differs by outcome but follows the survey calendar.**
- **The difference:** plankton is missing for 3.3% of quantified samples against 20.2% of non-detects, and all 41 rows without a survey are below 160.
- **Where the missing rows fall:**
  - the gap between the two counting labs (2017-06 to 2017-11, 6 rows);
  - quiet summer 2021 (6 rows);
  - the end of the plankton programme on 2023-05-22 (8 rows in 2023 Q2; Table 3);
  - single rows elsewhere.
- **Why it stays:** the gaps come from the survey schedule, which the actor knows, and do not depend on the sample's own outcome. Under the current matching this needs no action.

**4. P7, CLEAN-21 (Should): 16 taxa depend on which lab counted them.**
- **Evidence:** the 16 columns are above zero only in UPV/EHU surveys of 2014-05 to 2017-05, which cover 22 frame rows, all of them training rows. From 2017-12 on they are zero by the next lab's counting practice, and they are zero in all 154 test rows. A zero after 2017 means "not resolved at this level", not "absent".
- **Effect:** these are mostly ASP, AZA and other harmful taxa, not OA producers. The DSP taxa (Dinophysis, Phalacroma, Prorocentrum lima) are counted by both labs. The effect on this target should be small.
- **Mildest remedy:** a curation note. Cheap optional fixes: add the plankton lab (a `LABORATORY` column in the raw sheet, known at the time), or add a Pseudo-nitzschia genus total next to the size classes.

**5. P7, CLEAN-12 and CLEAN-21 (Should): Ostreopsis is one series in two columns.**
- **Evidence:** the descriptor (Table 1, footnote a) says records up to 2020 are presented as O. cf. siamensis and records from 2021 as Ostreopsis spp. (siamensis/ovata). The two columns are never both above zero.
- **Remedy:** sum them into one `plankton_ostreopsis_spp` column. The merge is lossless and safe, and has no OA relevance.

**6. P7, wording (no change to the data).**
- **Dissolved oxygen:** the comment calls it "a copy of the saturation". It is a function of saturation, temperature and salinity (R^2 0.998), and its correlation with saturation is only 0.50. Either reword the comment ("derived from the saturation, temperature and salinity", as sigma-theta is from T and S), or keep the column. PAR's exclusion is defensible: it is set by the hour and the cloud cover of the cast.
- **Taxa count:** `task_summary.known` says "45 potentially toxic plankton taxa". 42 ship: Dinophysis cf. ovum, Phalacroma mitra and Chrysochromulina/Imantonia/Phaeocystis were recorded only in 2014-2015, so they are constant zero in every matched survey and are dropped (CLEAN-5).

**Also noted for the curator (rows, not columns; LEAK-22/25 territory, low weight):**
- The OA group was not analysed for the whole 2020 DSP season (AZTI pilot plant 2020-03-10 to 08-25; Mussel Farm 2020-05-20 to 08-19; 15-19-variable panels without OA, DTX or PTX).
- Four Mussel Farm samples in the middle of the spring 2021 episode have AZA and YTX only (03-03, 04-09, 04-22, 06-21).
- The descriptor gives the reason in general terms: "the same variables were not always measured in all the samplings" (Limitations). Whether the OA values were missing for a reason tied to the outcome cannot be tested.
- So the "five spring episodes (2017, 2018, 2019, 2021, 2022)" leave out 2020 because it was not measured, not because it was quiet. The comment could say so.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-3 / LEAK-10 triggered by the same-day plankton counts (136 rows), moderate (AUC160 -0.05 / -0.04,
RMSE +6 to +18); fix: plankton surveys strictly earlier, CTD same-day kept. LEAK-34 holds (last result, 7-day lag,
conservative per Sec. 4.1). No post-outcome column, no label-encoding id, no outcome-driven missingness.
Quality: CLEAN-10 holds (-999 masked); CLEAN-21 note for 16 lab-specific taxa; CLEAN-12 merge of the two Ostreopsis
columns (cheap); wording of the DO drop and of "45 taxa".
For the curator: the turnaround of plankton and toxin results (1 or 2 days; 7 or about 3), a weighing call within USE-3.
```

</details>

<details><summary>Split audit</summary>

**Split auditor (2026-11-01): basque_offshore_bivalve_biotoxins**

**Verdict: right with notes, and one Must question for the curator.** A temporal split on `sample_date` is the regime the use case implies. The actor predicts for one of two known farms, and the farm's last result is a feature (USE-10, SPLIT-3). Every training row comes before every test row, and the rows of one day stay together. The Must question is SPLIT-14's 50% floor. The definition counts it in sampling days, which gives 50.6%. In rows the oldest window trains on 45.0%, and the collection's precedents count rows. If the curator keeps the rows reading, the split is wrong until it is re-split; the cutoffs for that are below. Separately, the splits text gets two things wrong: why it counts days, and what the windows stand for.

```text
Validity: USE-10 holds (known farm, temporal); SPLIT-1/2/3 hold; SPLIT-9 holds (no measurable shortcut);
  SPLIT-14 question (oldest train side 45.0% of rows, 50.6% of days; precedents count rows): re-split or amend;
  SPLIT-10 departure (no gap against the definition's own 7-day turnaround): fix with a 7-day gap;
  SPLIT-12/SPLIT-20 text: windows are not "a refit before each season"; history not stated.
Value: TP-9, newest window near constant (3 quantified of 64): curator's call, no split remedy.
For the curator: issue 1 (the floor's unit: re-split in rows, or amend SPLIT-14).
```

All model numbers below come from untuned LightGBM (the builder's TP-10 configuration, mean of 5 seeds) on the definition's frame, loaded with `dataset_io.from_definition`. RMSE is in ug/kg; "log skill" is 1 - MSE/MSE(train mean) on the shipped log scale.

| Split | Windows (test rows / quantified / >160) | Oldest train side | RMSE | log skill | AUC for 160 |
|---|---|---|---|---|---|
| Shipped (39 sampling days each, floor in days, no gap) | 2021-04-19..10-18 (44/26/16); 2021-10-20..2022-05-31 (46/10/7); 2022-06-06..2023-06-22 (64/3/0) | 126 rows, 45.0% (50.6% of days) | 249.4 / 128.3 / 21.9 | 0.475 / 0.644 / 0.663 | 0.924 / 0.971 / - |
| Shipped windows + 7-day gap | same | 123 rows | 246.0 / 126.3 / 20.4 | 0.443 / 0.665 / 0.707 | 0.935 / 0.978 / - |
| Floor in rows (cutoffs 2021-06-07, 2021-11-30, 2022-07-04; 35 days each) | 2021-06-07..11-24 (37/12/6); 2021-11-30..2022-06-28 (42/11/7); 2022-07-04..2023-06-22 (59/2/0) | 142 rows, 50.7% (140, 50.0%, with a 7-day gap) | 82.5 / 135.9 / 16.4 | 0.054 / 0.593 / 0.769 | 1.000 / 0.967 / - |
| IID 5-fold x 3 (scale only; SPLIT-16 bars it) | 56 rows per fold | 224 rows | mean 143.9 | mean 0.688 | mean 0.973 |

**1. SPLIT-14 (P4, Must): the unit of the 50% training floor.**
- Evidence:
  - The oldest window trains on 126 of 280 rows (45.0%), which is 120 of 237 sampling days (50.6%).
  - The tooling counts distinct values for `unit="unique"` (definitions.md, "Splits"), so `dataset check` passes.
  - The collection's precedents count rows:
    - wisconsin_local_government_property_insurance_fund: "41% of the rows, under SPLIT-14's floor";
    - california_house_prices_2020: "train on 50%, 67% and 83%" of the rows;
    - garments_worker_productivity: "exactly half of the available samples";
    - melbourne_housing_market: "55-95% of the rows".
- The stated reason does not hold. splits_comment says "sampling runs up to daily during episodes, so samples would let the outcome set the windows". The data says otherwise:
  - Episodes do not add more rows per day than quiet days do: 1.16 rows per sampling day on days with a quantified value, 1.19 on non-detect days.
  - Daily sampling adds days and rows alike. The day and row counts part because mussels and oysters are taken on the same day, mostly in the quiet last year: 25 of window 3's 39 days hold two or more rows, against 6 of the 120 days before window 1.
  - So counting days moves the cutoff earlier because of paired samples in a quiet year, not because of episodes. As a side effect it puts the April-May 2021 peak (10 exceedances) on the test side.
- Wrong claim. splits_comment and the curation_comments bullet "Why a level" say that counted in samples the test pool "would start in July 2021 and hold one episode (spring 2022, 7 exceedances)". It does not:
  - The first day with 140 earlier rows is 2021-06-01.
  - The tooling's `unit="rows"` starts the pool on 2021-06-07, and it also cuts 2022-11-30 across two windows, so it is not usable as is.
  - The row-floor pool holds 13 exceedances (6 in June 2021, 7 in spring 2022) and 25 quantified values.
- Mildest remedies (the Must allows no exception):
  - (a) Re-split with the floor in rows: `TemporalSplits(window=35, unit="unique", cutoffs=("2021-06-07", "2021-11-30", "2022-07-04"))`, with the windows in the table. The cost: 13 instead of 23 exceedances in test, and window 1 has 37 rows.
  - (b) Keep the days, and have the curator amend SPLIT-14 to name the unit when windows are cut in distinct time values. The honest argument for (b) is not the one now written. It is that the rows of one day share one plankton survey and one CTD cast, so a second species on the same day adds little information to the training side.
  - Either way, rewrite the reason in splits_comment and fix the "counted in rows" sentence in curation_comments.

**2. SPLIT-10 (P4, Should; applies SPLIT-9): no gap against the definition's own label delay.**
- Evidence:
  - The definition sets `LAST_RESULT_MIN_AGE_DAYS = 7`, so it treats a result as known only a week after its sample. Yet each window trains on every row up to the day before it starts.
  - 6 training rows fall within 7 days of a window start (oldest to newest: 3, 1 and 2). Window 1's three are Mussel Farm samples of 2021-04-13 to 15 (73, 75 and 52 ug/kg), taken during the running episode.
  - With a 7-day gap, RMSE goes from 249.4 / 128.3 / 21.9 to 246.0 / 126.3 / 20.4, and the AUC for the 160 limit from 0.924 / 0.971 to 0.935 / 0.978. That is no measurable shortcut, so SPLIT-9 holds and the departure is from the Should.
- Remedy: a 7-day gap. A `_make_splits` would train on the rows dated on or before the window start minus 7 days, declared as `Temporal(..., gap=7, gap_unit="days")`. It costs 6 rows and makes the split agree with the definition's own turnaround.
  - This is better than a sixth SPLIT-10 exception: five are recorded, an amendment is due, and the ames/perth reasoning (a delay shorter than the time resolution) does not fit daily dates.
  - Combined with 1(a), the oldest window keeps 140 rows (50.0%).

**3. SPLIT-12, SPLIT-20 (P4, Should) and the text: what the windows stand for.**
- Evidence:
  - The windows are 39 sampling days each, cut by count. They span 6, 7 and 12.5 months.
  - Window 1 is a refit in the middle of an episode. The 2021 episode runs from 2021-03-10 to 2021-06-18 (24 exceedances); window 1 starts on 2021-04-19, with 8 of them on the training side.
  - Window 3 starts on 2022-06-06, two weeks after the 2022 episode's last exceedance (2022-05-23).
  - Only window 2 is a refit before a season: refit on 2021-10-20, episode from 2022-04-26 to 2022-05-23.
  - task_summary.split and splits_comment say "as for a model refit before each (toxic) season". fit_reason says "the test windows rest on two toxic seasons", but the test holds only the second half of the first one.
  - A refit mid-episode is honest: the March labels are back by 19 April even under the definition's 7-day reading. So this needs a text fix, not a re-split.
- Remedy: rewrite the text. For example: "three windows of 39 sampling days: the second half of the 2021 episode (refit mid-episode, its first 8 exceedances in training), the 2022 episode (refit in October 2021) and the quiet year after it". The declared horizon of 12 months is the longest window; the other two cover 6 and 7 months.

**4. SPLIT-20 (P4, Should): the training history is not stated.**
- Evidence. The history starts in April 2016 and has several breaks:
  - 2016-2018: about monthly sampling at the pilot plant only (50 rows, with the 2017 and 2018 episodes, up to 1,693 ug/kg);
  - plankton sampling method changed in June 2018;
  - the Mussel Farm starts in June 2019;
  - the laboratory changes in January 2020. Every test row comes from CECOPESCA-ANFACO, so `laboratory` is constant in test and works as a period marker in training;
  - 2020 is nearly empty: 2 rows in Q1, none in Q2, 9 in the second half.
- Keeping the whole history is right for 280 rows. The 2017-2019 episodes are the only other seasons to learn from, and SPLIT-20's "one full season before the newest window" holds. But no bullet says so.
- Remedy: a `History:` bullet in curation_comments. The rows do not change.

**5. TP-9 (P6, Must, value; the curator's call, builder issue 1): the newest window is near constant.**
- Evidence:
  - The newest window holds 64 rows, 3 of them quantified (max 60 ug/kg), and 63 of the 64 are from the pilot plant.
  - Always predicting 40 scores RMSE 3.3, against 21.9 for LightGBM and 100.8 for the training mean. So the window measures only false alarms in a quiet year.
  - No split that meets SPLIT-14 avoids this: the test pool is the newest half, and the last exceedance is on 2022-05-23. Under the row floor the newest window holds 2 quantified values of 59.
  - The test signal rests on windows 1 and 2: 26 and 10 quantified, 16 and 7 above 160 as shipped (12 and 11, 6 and 7 under the row floor).
  - Windows 1 and 2 hold 44 and 46 rows, below SPLIT-17's ~50. With three windows over 154 test rows, no wider window can fix that.
- Remedy: none in the split. The keep or `Too Small` call stays with the curator.

**What holds**
- Regime (USE-10, SPLIT-3, SPLIT-13). Both farms are on every training side (Mussel Farm: 40, 71 and 104 training rows). Grouping on 2 farms would test a shift between domains, not new entities (the few-groups factor).
- Integrity. On all three windows the last training date precedes the first test date, no date is shared, and a day's rows (two species, or both farms) stay together.
- IID, for scale only. Its mean log skill is 0.688 against 0.475-0.663 on the windows, because the daily samples of one episode would sit on both sides. SPLIT-16 bars it anyway.
- Hidden groups. The entity-like hits are water-profile values, not entities. The near copies (14.9% of test rows seen in training) are quiet profiles that recur over time, not an entity that new data would lack (SPLIT-30): no action.
- The counts in splits_comment check out: 44/26/16, 46/10/7 and 64/3/0, with 126 training rows (45%) for the oldest window.
- Not checked here: whether the same-day plankton and CTD are known before the result (USE-3, LEAK-10). The builder measured it (RMSE 258 / 136 / 60 with strictly earlier surveys); the column and claim auditors own it.

**Scripts and outputs.** In the run folder (not committed): the windows, train shares and late-label rows; the series by quarter and the episodes around the cutoffs; rows against sampling days and the row-floor date; the models under each split; the integrity and episode dates; the re-split as a declaration; the definition's frame and splits.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: basque_offshore_bivalve_biotoxins**

**Verdict.** Fit: **approximate**, as declared. The decision is real: Mendexa-Ondarroa is a class-A production area under Reg. (EU) 2019/627 (Basque order of 30 July 2021, BOPV 185), and its operator and the Basque Fisheries and Aquaculture Directorate close harvesting when the okadaic-acid group reaches 160 ug OA eq/kg. The target is exactly the regulated quantity. What is approximate is the prediction point (USE-3, USE-8): the source states no turnaround, and the reading in the definition gives the plankton count zero delay and the toxin result seven days. In practice a Utermöhl count cannot exist on the sampling day, and during an episode a toxin result two or three days old usually does. Metric: **partly** (details under 5).

**Who I am and how I decide today.** I manage food safety for the Mendexa offshore farms (or I run one of them). Under Reg. 853/2004 and 2019/627 I close the area when a lab result for the OA group exceeds 160 ug OA eq/kg. Art. 63 lets me reopen only after two consecutive results below the limit, taken at least 48 h apart (one result is enough if the area's record shows a falling trend). In the gap between taking a sample and getting its result, I can close as a precaution when the plankton or the recent toxin trend points to a rise. Galicia does this weekly; Molares-Ulloa et al. 2022 model exactly that call, with recall as the main score because a missed closure is a health risk. Cruz et al. 2022 forecast the DSP level in Portuguese mussels 1 to 4 weeks ahead from weekly toxin and Dinophysis series. They pick models by MAE and also check whether the model gets the side of the limit, and changes of side, right. The early warning the descriptor names ("could be useful to develop early warning systems", Value of the Data) is that call.

**1. Do I have these inputs at the prediction point?**
- Farm, species, laboratory, date, sampling method: yes.
- CTD profile of the same day: yes. It is measured in situ and in my hands when the boat docks, so the zero lag the definition allows is right for the CTD.
- Plankton counts of the same day: **no**. The descriptor itself says the samples were Lugol-fixed, "preserved in the dark and cool (4 °C) until analysis", and that "a subsample (50 ml) was sedimented" before counting (Sec. 4.3). Settling a 50 ml Utermöhl chamber takes at least 20 h (UK-NRL Phyto SOP) and up to about 50 h (US EPA LG401). The counting labs were Oceansnell (Valencia) and UPV/EHU. So a same-day count reaches me 2 to 4 days after sampling, about when the toxin result does. A count from the same survey is a potential leak under LEAK-10. The builder measured what it is worth: on the spring-2021 window it lifts the ROC AUC at 160 from 0.84 to 0.92, and in the quiet window it brings RMSE from 60 down to 22.
- Last toxin result at least 7 days old: I usually have a fresher one. During episodes the farm is sampled daily, and Art. 63's 48-h reopening rule only makes sense if results come back within days. The descriptor says analysis started "within two days of sampling" when the sample was refrigerated, otherwise it was frozen. A 2-3-day lag is my reading. The source states no turnaround either way.
- Missing inputs that I always have:
  - the trend of the farm's last two or three results (rising or falling), not one value;
  - days since the farm's previous sample, which is my own alert state (I set daily sampling when worried; this is a USE-6 input, not a leak);
  - the last result for the same species: the shipped one is the farm's maximum over species, and 6 of the 37 farm-days with both mussels and oysters fall on different sides of 160, with oysters lower.
- The descriptor also names wind, upwelling and currents as companion inputs. They would add signal, but leaving them out is acceptable.

What happens with my timing, measured on the shipped windows (spring 2021 / spring 2022 / quiet year): plankton at least 2-3 days old, CTD same day, last toxin result at least 3 days old. Untuned LightGBM, 5 seeds, the builder's settings; script in the run folder (not committed).

| inputs | model RMSE ug/kg | farm's last result | ROC AUC at 160, model vs last |
|---|---|---|---|
| shipped (plankton 0 d, toxin 7 d) | 249 / 128 / 22 | 286 / 162 / 69 | 0.92 / 0.97 vs 0.83 / 0.89 |
| plankton 2 d, CTD 0 d, toxin 3 d | 260 / 128 / 33 | 336 / 142 / 69 | 0.90 / 0.94 vs 0.81 / 0.91 |
| plankton 3 d, CTD 0 d, toxin 3 d | 255 / 139 / 42 | 336 / 142 / 69 | 0.91 / 0.92 vs 0.81 / 0.91 |

The task survives realistic timing: the model beats the farm's last result in every window and ranks the exceedances better. Fixing the leak keeps the task (USE-12). With the lag, plankton is missing for 96-99 rows instead of 41, because surveys are biweekly or monthly; widening the 14-day window would recover some.

**2. Is the target what I act on?** Yes, nearly. OA + DTX1 + DTX2 in ug OA eq/kg is the regulated sum since Reg. 2021/1374. Before 2021 the regulated sum also included the PTXs, but PTX1 and PTX2 were never quantified (all 280 at the code 40), so the sum is the same over the whole period. The non-detect code 40 means "below LOQ, safe" to me, which is right. My action is binary (close or not at 160). I would want a **probability that the coming result exceeds 160**, and a level as second best: a level carries the limit and tells me how long a closure may last. Shipping the level is defensible under USE-5. The TP-9 reason for not shipping the exceedance is real: the newest window holds no exceedance.

**3. Does one row match one decision? Is the test what I would face?**
- The unit (farm × species × sampling day) is the unit I sample and act on. Good.
- The test is what I would face: the next seasons, after a refit (USE-10, a known entity with its history).
- The decision value is thin, though:
  - Of the 23 test exceedances, 18 fall while the farm's last known result is already above 160. There the area is closed, and only lab results can reopen it (Art. 63).
  - The early-warning rows, an exceedance after a result at or below 160, number **5 in all three windows**: 2 in spring 2021, 3 in spring 2022, none in the quiet year.
  - The quiet year (63 of 64 rows from the AZTI pilot plant; the Mussel Farm stops in 2022-08) tests false alarms only.
- I would not drop the in-closure rows, because a level model should get them right too. But the curator should know that the score that matters to me rests on five onsets.

**4. Would I use it?** As support for a precautionary closure or for stepping up sampling, yes. I would never use it to reopen. I would trust it if:
- it flagged onsets several days before the lab;
- its exceedance recall stayed high at a false-alarm rate I can carry (a false closure costs the farm a week of sales);
- it held across the 2018 plankton method change and the 2020 change of laboratory.

What makes me distrust it now:
- the same-day plankton;
- recall at 160 of 0.56 and 0.57 for the log-target model in the two toxic windows, against 0.88 and 0.57 for simply repeating the last result. The exp(mean log) back-transform pulls peaks down. A raw-target LightGBM catches 0.94 and 1.00 with 8 and 5 false alarms instead of 2 and 1, at the same AUC (0.93 / 1.00). Recall is an operating-point choice I would make on the training side, so the AUC is the fairer comparison;
- a test that rests on two toxic seasons at one site.

**5. Does the metric score my decision? Partly.** RMSE in ug/kg (fallback) scores the level, at the right unit (MET-1, MET-3: shipped as log, scored on ug/kg). But in the two toxic windows 85% and 90% of the log-target model's squared error comes from the 4 highest samples. All four are far above 160, where my decision (closed) is not in doubt. A miss of 500 at 1252 weighs as much as calling a non-detect 540. Peaks also swing by a factor of 2 to 4 within days from sampling and lab noise: at the Mussel Farm, 456 → 1005 → 307 on 19, 21 and 24 May 2021, and 321 → 78 → 239 on 5, 7 and 12 May. That noise is why a fresher last result scores *worse* under RMSE (336 vs 286 in spring 2021). In spring 2021, RMSE cannot tell apart two models that act very differently: 249 vs 248 for log-target and raw-target LightGBM, with recall 0.56 vs 0.94.

The metric I would pick:
- **First choice:** the exceedance of 160 as a probability, ranked by ROC AUC per window or scored by log loss (MET-8). No source fixes a cost ratio between a missed and a needless closure, so no cost matrix (MET-7). MET-9 gives no reason for PR AUC. This choice cannot be scored in the newest window (0 exceedances, TP-9), which is the builder's reason for the level.
- **Within the level framing:** `Metric.from_context("rmsle", target_transform="log")` on ug/kg (MET-11 context, MET-3). It follows the collection's precedent for skewed quantities whose error is relative (onlinenewspopularity, brazilian_ecommerce, melbourne_housing_market, blood_tests_drink_prediction, video_transcoding_time_prediction). The limit sits at four times the LOQ, and the lab and sampling noise is multiplicative, so a factor-of-two miss near the limit should count as much as one at the peaks.

On the log scale (RMSLE is within about 2% of it, since every value is at least 40), the model and the farm's last result score 0.82 vs 1.00 (spring 2021), 0.53 vs 0.65 (spring 2022) and 0.35 vs 0.32 (quiet year), with the constant 40 at 0.07. So under RMSLE the TP-10 leg-1 comparison holds in the two toxic windows and fails in the quiet one; the curator should see this before switching. Either way, report the ROC AUC at 160 per window in the notes. Script in the run folder (not committed).

**Gaps between the dataset and my decision, ranked by how much they change the task**
1. Same-day plankton counts, which cannot exist before the toxin result (USE-3, LEAK-10). Measured above: the task survives a 2-3-day plankton lag.
2. The declared metric is decided by four peaks per toxic window, all far above the limit (MET-1). RMSLE with the AUC at 160 in the notes is closer to my decision.
3. The decision value rests on 5 test onsets, and 18 of 23 test exceedances fall inside closures. This cannot be fixed without more seasons. It belongs in `fit_reason`, which already says "two toxic seasons".
4. The 7-day toxin lag is conservative against the 2-3 days I would have in an episode. The task gets no easier with a fresher result: persistence gets worse under RMSE.
5. Missing inputs I always have: result trend, days since the previous sample, the last result for the same species. Small gains, no change to the task.

**What an expert would change**
- Lag the plankton by at least 2 days (3 to be safe) and keep the CTD same day. Then the use case and `fit_reason` stop calling the timing "our reading" and name it.
- If the curator keeps same-day plankton, name it in `fit_reason` as a kept potential leak (AUC 0.92 vs 0.84 in spring 2021), not as a gap (USE-8).
- Set the toxin lag to 3 days, or keep 7 as a declared conservative choice.
- Add the previous result and the days since the farm's previous sample.
- Declare RMSLE from context, and report the ROC AUC and recall at 160 per window in the notes.
- Minor (claim, not use case): `task_summary.known` says "45 potentially toxic plankton taxa", but 42 ship (Dinophysis cf. ovum, Phalacroma mitra and Chrysochromulina/Imantonia/Phaeocystis are never counted in a matched survey and are dropped).

**Sources**
- Solaun et al. 2025, Data in Brief 61:111736 (PMC12197977), read in full from the run's copy of the full text: Value of the Data, Sec. 4.1, 4.3, 4.4, Table 3.
- Reg. (EU) 2019/627, Art. 63 (reopening): https://www.legislation.gov.uk/eur/2019/627/article/63
- Basque order of 30 July 2021 classifying Mendexa-Ondarroa as zone A: https://www.euskadi.eus/web01-bopv/es/bopv2/datos/2021/09/2104766a.shtml
- Molares-Ulloa et al. 2022, Computers and Electronics in Agriculture 197:106956, precautionary closures for lipophilic toxins in the Vigo estuary (weekly; accuracy, sensitivity, kappa): https://arxiv.org/html/2402.09266v1
- Cruz et al. 2022, Knowledge-Based Systems 257:109895, DSP 1-4 weeks ahead, MAE and regulatory-state accuracy (abstract via repository records only): https://sapientia.ualg.pt/entities/publication/4c84d18e-28ce-4071-bfce-c580fad1d73b/full
- Utermöhl settling times: US EPA LG401 (50 ml about 50 h), https://www.epa.gov/system/files/documents/2021-12/lg401.v07-phytoplankton-analysis_rfa.pdf ; UK-NRL Phyto SOP (50 ml at least 20 h), https://www.afbini.gov.uk/sites/afbini.gov.uk/files/publications/Phytoplankton%20enumeration%20SOP%20v8%20Public%20version.odt (both read from search snippets).
- My probes: scripts in the run folder (not committed).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data are real, the target is rebuilt correctly, and the features are mostly honest. But under most plausible temporal cuts the last test window holds an almost constant target (2023 has one detection in 41 rows). The table is also small and the toxic events are few. Re-cut the windows so that each one contains a toxic season. If the benchmark cannot do that, I would exclude it.

**What the task is.** Each row is one pooled bivalve sample (mussel or Pacific oyster) from one of two offshore Basque sites: the AZTI pilot plant (175 rows) or the Mussel Farm (105). Samples run from 2016-04-15 to 2023-06-22. The target is ln(OA-group toxins, µg OA-eq/kg), the sum of the quantified OA, DTX1 and DTX2 values. The features are:
- the maximum over depths of 42 potentially toxic phytoplankton taxa, from the latest survey within 14 days at or before the sample date;
- CTD means over 0–12 m (the depth where the bivalves hang);
- the latest OA result from the same station that is at least 7 days old.

The users would be shellfish producers and Basque food-safety managers. The EU limit is 160 µg OA-eq/kg, and the data paper says the data let "food safety managers to ban the sales when the biotoxins exceed the regulatory limits or temporarily close the harvesting areas", and could help "develop early warning systems". So this is a real use: a nowcast or near-term warning of DSP toxicity.

**What I verified against the raw Mendeley files (v2, CC BY 4.0).**
- All 280 OA-group samples in `Biotoxins in bivalves.xlsx` appear exactly once. There are 190 ANFACO and 90 INTECMAR samples, and no lipophilic analyses exist before 2016-04.
- The target matches log(sum of "=" values among OA, DTX1 and DTX2, or 40 if none is quantified) on 280 of 280 rows.
- `last_result_*` matches "most recent result at the same station (either shellfish, max on ties) dated at least 7 days earlier" on 280 of 280 rows. Its minimum age is 7 days.
- The plankton features match the max over depths at the paired station on 98.9% of rows. The pairing is Mussel Farm-CTD for the farm when available, otherwise Mendexa-Control.
- The CTD values match the 0–12 dbar mean.
- Three taxa from the source are absent (Dinophysis cf. ovum, Phalacroma mitra, Chrysochromulina/Imantonia/Phaeocystis). Their only non-zero records fall in 2014–2015, before the OA data start, so dropping them is correct.

The values are plausible. The maximum is 1693 µg/kg, and *Dinophysis acuminata*, the classic OA producer in the Bay of Biscay, has Spearman 0.63 with the target.

**Concerns, most to least serious**

1. **The final test window is degenerate under most cuts.** From 2022-08 to 2023-06 there are 57 rows. Only 2 exceed the LOQ floor (57 and 42 µg/kg), and the 41 rows of 2023 hold one value above floor (42). I tried equal-row expanding windows with the last 3 of 5, 6, 8 and 10 blocks. In every case the final window had a target std of 0.006–0.009 (log units) and at most 1 positive. In that window:
   - Predicting the floor gives RMSE 0.007. LightGBM gives 0.33, RF 0.10, and LightGBM without plankton 0.83. R² there would be around −200 or worse.
   - Score differences in this window are larger than those in the informative windows. So the window rewards a constant predictor and dominates any per-window averaging.
   - Only the 4-block cut keeps 7 positives in the last window.

   *Change:* define the windows by toxic season. For example, test on Jan–Sep 2019, 2021 and 2022, each with an expanding training set, which gives 14, 40 and 12 positives. Alternatively, end the last window at 2022-07 and drop or append the eventless 2022-08 to 2023-06 tail.

2. **The target is heavily censored and episodic.**
   - 188 of 280 rows (67%) equal log(40), the substituted LOQ.
   - Positives come from about five spring and early-summer DSP episodes: 2017, 2018, 2019, 2021 and 2022. Positive rate by month is 0% in January and 69% in May.
   - Sampling becomes near-daily during episodes; for example, the Mussel Farm has 64 rows in 2021, including 2021-03-22/23/24/25. Many test rows are therefore autocorrelated replicates of one event, and the effective test size is much smaller than 40–60 rows.

   *Change:* keep the log-regression target but tell users about the mass at the LOQ. Consider adding a companion exceedance target (above 160 µg/kg, 17% of rows; or above the LOQ, 33%). Report per-window results rather than a pooled average.

3. **The table is small.** At 280 rows × 57 features, many features are near-empty: 15 plankton columns have 6 or fewer non-zero values. This is below the usual size floor of tabular benchmarks, and the score variance across methods will be high. There is still learnable signal. With 6 blocks, in the two informative windows, LightGBM scores RMSE 0.60 and 0.54, against 0.88 and 0.85 for the training mean and 0.76 and 0.75 for persistence (log of the last result). Dropping the plankton features worsens it to 0.70 and 0.71. So the task is neither trivial nor noise, but it is fragile.

4. **The time frame of the features is inconsistent.** The toxin history is lagged by 7 days or more, but plankton is used from the same day in 136 of 239 rows (age 0). Plankton counts need lab work (Lugol fixation, Utermöhl sedimentation, microscopy), so same-day counts are not available earlier than the toxin result itself. I rebuilt *D. acuminata* with a 3- or 7-day minimum lag (RF, 6 blocks). It changed RMSE only modestly in the informative windows: 0.67 → 0.70/0.57 and 0.61 → 0.66/0.64. Most of the gain from same-day plankton shows up in the degenerate window.

   *Change:* fix one forecast horizon and apply it to every lab-derived feature. Lag plankton like the toxin result, for example by 3 days or more, or document the task explicitly as a same-day nowcast. CTD is measured in situ, so keeping it same-day is fine.

5. **Paired rows could straddle a split boundary.** 37 mussel/oyster pairs (74 rows) share the station, date and every feature, and differ only in shellfish and target. An equal-row split can cut such a pair; the 4-block cut does so at 2022-05-09.

   *Change:* make sure split boundaries fall between dates, not between rows.

6. **Minor preparation points.**
   - The `last_result` feature takes the station-level maximum across shellfish. Mussels accumulate more OA than oysters (positive rate 37% vs 13%), so a shellfish-specific last result, or both, would be more informative for oyster rows.
   - `laboratory` duplicates the period (INTECMAR ≤2019, ANFACO ≥2020). Both labs report the same LOQs (OA 40, DTX1 40, DTX2 24), so it is harmless.
   - The plankton sampling switched from Niskin to hose in 2018-06, which changes the scale of the max-over-depths counts. It is encoded in `plankton_sampling_method`, which is good.
   - Missing values (plankton 14.6%, CTD 28%) are left as NaN, with age columns. That is sensible.
   - The categorical and datetime types are correct.

**Third-party use.** The listed PLOS ONE paper and its GitHub/Zenodo benchmark use a "biotoxin" table with 5,076 rows and 2 predictors. They report low skill: best R² 0.17, RF and XGB −0.006, and a permutation test p = 0.995. That is a crude long-format preparation and is not comparable to this one. Its failure does not argue against this table, but it should not be cited as a baseline.

**What I could not check**
- The exact split boundaries used for the 3 test windows. My windows are guesses, and concern 1 depends on them.
- The real report turnaround times of the labs (toxins and phytoplankton), so I cannot say whether the 7-day toxin lag is conservative or the same-day plankton is unrealistic in practice.
- Whether the intensified sampling was triggered by results less than 7 days old. If so, the row density and `last_result_age_days` carry a little information from within the lag. Positive rate is 43% when age ≤7 days and 23% when age >21 days.
- I did not read the PLOS ONE paper beyond its first 100k characters.

Sources: https://data.mendeley.com/datasets/vyz9zvddz4/2 (raw xlsx downloaded via the Mendeley public API); data paper full text, PMC12197977 (doi:10.1016/j.dib.2025.111736); https://github.com/zhm12305/marine-ml-benchmark; https://journals.plos.org/plosone/doi?id=10.1371/journal.pone.0351325; https://zenodo.org/doi/10.5281/zenodo.19510440. I did not open any file outside the clean room.

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01)**

**Verdict:** the metric, provenance, rows, joined features, warning and fit follow the precedents. Five decisions depart from them. In rank order: the level target rests on a lower-ranked reason (USE-5); the same-day surveys are kept although the closest precedent kept only what was surely known (LEAK-10); the training floor is counted in days (SPLIT-14, reason stated, kick is the matching case); there is no gap despite the definition's own 7-day turnaround (SPLIT-10); and the dataset is kept with a near-constant newest window (TP-9). Departures 2, 4 and 5 give no fact that sets the case apart. Each departure ends with one prompt for the curator.

**1. A level, not the exceedance of 160 (USE-5, Must, P3): departs, and its reason comes from a lower rank.** The descriptor names a decision at the limit ("ban the sales when the biotoxins exceed the regulatory limits"), and the screening wrote the use case as "a predicted exceedance". The definition ships the level. Its reason is TP-9 (the newest window would hold one class), which is a P6 reason for a P3 choice. The ranking does not allow that (principles.md, "Conflicts between rules"). No precedent ships a level to escape a thin binary target. seismic_bumps (2026-09-30, Lennart) and digicow_farmer_training_adoption_challenge (2026-10-26, Lennart) went `Too Small` with their binary targets, but neither had a level to use instead. The nearest USE-5 precedent is the rating-or-grade case (wine_quality, numerai_v5_2_1m, corporate_credit_rating; 2026-10-21, Lennart): number or classes is decided case by case, by how the source models the target and what similar use cases do. The level can stand on a P3 ground that the definition does not use. The descriptor's second decision, "temporarily close the harvesting areas as a precautionary measure", is taken below the limit, and the laboratory reports the level. This tension (the actor's threshold against windows that cannot score it) has no row in the Tensions table yet; the curator's answer becomes that row.

**Consistency check (AI, 2026-11-01):** your call on basque_offshore_bivalve_biotoxins (the level, where the source's decision is the exceedance of 160; the stated reason is TP-9) rests on a lower-ranked rule than USE-5, the rule it departs from. What sets it apart?
(a) Precautionary closures act on the level below the limit, and the laboratory reports the level, so the level is what the actor reads. USE-5 then holds: the definition's reason changes from TP-9 to this, and a Tensions row records it. (b) Treat it like seismic_bumps: ship the exceedance and let TP-9 decide. (c) None: no earlier case had a level to choose instead. (d) Amend USE-5 to say when a measured level replaces the threshold the actor applies.

**2. Same-day plankton and CTD treated as known before the toxin result (USE-3, LEAK-10, Must; CLEAN-19, fourth bullet): departs, no fact given.** 136 of the 280 samples take a survey from their own day. The closest precedent is rain_in_australia. There, the columns recorded after 9 am on D are replaced by their D-1 values (ROC AUC 0.849, against 0.902 with them; review panel of 2026-10-20, kept through Lennart's marks of 2026-10-26). The other stations' 9 am readings are kept "only where that location's 9 am comes no later than the row's own under both clock and standard time" (CLEAN-19 Cases, 2026-10-26, Lennart): when the timing can be read two ways, the precedent keeps only what holds under both. This definition takes the favourable reading of an unknown turnaround and says so ("our reading"). The descriptor leans the other way: the water samples were "fixed with acidic Lugol's solution and preserved in the dark and cool (4 °C) until analysis" by the UPV/EHU or Oceansnell laboratory, which does not suggest a count on the day. The cost of the strict reading is measured (builder: RMSE 249 / 128 / 22 rises to 258 / 136 / 60; ROC AUC at 160 falls from 0.92 / 0.97 to 0.84 / 0.94), and the model still beats the farm's last result in every window. kick and expresso_churn_prediction (2026-10-22, Lennart) dropped fields of doubtful timing that carried signal. Those drops rested on measured evidence that the fields were filled late, so they are weaker analogues.

**Consistency check (AI, 2026-11-01):** your call on basque_offshore_bivalve_biotoxins (same-day surveys kept as known before the toxin result) differs from rain_in_australia (2026-10-26: same-day inputs kept only where they are known by the prediction point under both readings of the clock). What sets it apart?
(a) The plankton count reaches the manager before the toxin result, a fact to be found in AZTI's or the Basque Government's monitoring protocol, or asked of AZTI. It would be recorded as a LEAK-10 Cases row; a Must takes no exception. (b) Treat it like rain_in_australia: use only surveys from earlier days (the variant already measured). (c) Reopen rain_in_australia under the favourable reading. (d) Amend LEAK-10 for inputs whose turnaround is unknown.

**3. The 50% training floor counted in sampling days (SPLIT-14, Must): departs from the row reading, with a stated reason.** The oldest window trains on 126 of 280 samples (45%), which is 50% of the 237 sampling days. Every curator decision that states the floor counts rows:
* california_house_prices_2020: windows now train on 50 / 67 / 83% of the rows (2026-10-21).
* alfa_battle_2_0_task_2 and lending_club: the SPLIT-10 exceptions were made to keep the train side at 50% of the rows (2026-10-21, Lennart).
* melbourne_housing_market: 55-95% of the rows.

The framework counts distinct values for `unit="unique"` (definitions.md, "Splits"). kick, built that way, trains its oldest window on 35,514 of 72,983 rows (48.7%) and 50% of the purchase dates, and no decision has looked at that. The stated reason sets this case apart: sampling turns daily during episodes, so a floor counted in rows would let the outcome place the windows. Counted in rows, the test pool would start in July 2021 and hold one episode. A Must takes no exception, so this is a reading of "50% of the data". The curator settles it once, and the answer applies to kick too.

**Consistency check (AI, 2026-11-01):** your call on basque_offshore_bivalve_biotoxins (the floor in sampling days, 45% of the rows) differs from california_house_prices_2020, alfa_battle_2_0_task_2 and lending_club (2026-10-21: the floor in rows). What sets it apart?
(a) The sampling frequency follows the outcome, so the days on the time axis, not the row count, measure what a refit has seen. It would be recorded as the reading in SPLIT-14's Cases. (b) Treat it like them: count the floor in rows (the test pool then starts in July 2021 and holds one episode). (c) Reopen kick (48.7% of its rows) to match whichever reading is chosen. (d) Amend SPLIT-14 to name the unit: distinct time values for windows of unit "unique", rows otherwise.

**4. No gap between train and test, although the definition assumes a 7-day turnaround (SPLIT-10, Should; SPLIT-9, Must, where the shortcut can be measured): departs, no reason given.** The last-result feature treats a toxin result as known 7 days after its sample, yet each train side runs to the day before its window. Precedents with a delay counted in days set a gap of about that delay:
* house_sales: one week, for a recording delay with a median of 6 days (review of 2026-10-20).
* the `_1m` taxi and ETA versions: one day wherever a training label ends after the window starts (2026-10-21, Lennart).

Measured here (a script in the run folder, not committed, with the builder's TP-10 LightGBM settings, which reproduce the shipped 249.4 / 128.3 / 21.9): 3, 2 and 2 training samples fall in the 7 days before the windows. The 3 before 2021-04-19 are all quantified: they are the onset of the spring 2021 episode. With a 7-day gap, the window RMSE is 246.0 / 124.7 / 20.4, so the gap costs nothing. On the first 14 days of the spring 2021 window, RMSE rises from 145.9 to 232.8 with the gap: the onset labels predict the first test rows, the kind of shortcut SPLIT-9 removes (Tensions row on unmatured labels: "a shortcut that can be measured is always removed"; alfa_battle_2_0_task_2). That last figure rests on 4 samples, so it points the way without proving it. The fix is a 7-day gap declared on `Temporal`, which matches the definition's own assumption.

**Consistency check (AI, 2026-11-01):** your call on basque_offshore_bivalve_biotoxins (no gap, while the last-result feature assumes a 7-day delay) differs from house_sales (2026-10-20: a one-week gap for a delay with a 6-day median). What sets it apart?
(a) The real turnaround is a day or two, and the 7 days is only a cautious bound for the feature. A gap of a day or two would then do; it would be recorded as an exception to SPLIT-10 with that fact. (b) Treat it like house_sales: a 7-day gap. (c) None: house_sales measured its delay, so nothing here argues for reopening it. (d) Amend SPLIT-10 so that a delay assumed for a feature also sets the gap.

**5. Keeping a newest window with 3 values off the code in 64 (TP-9, Must, P6): departs from the `Too Small` precedents, with no fact that sets it apart.** TP-9 counts "the minority-class rows (or the target's spread) per test window". The windows hold 26, 10 and 3 quantified values (16, 7 and 0 above 160). Each window's signal comes from at most one episode, at two farms. In the newest window, always predicting 40 scores an RMSE of 3.3, against 21.9 for the model.

Precedents that retired a dataset:
* seismic_bumps (2026-09-30, Lennart): 3 or 2 windows of 14-26 positives "still give ROC AUC intervals of about ±0.1 to ±0.14 per window".
* digicow (2026-10-26, Lennart): 9 and 5 adopters, from 1 and 1 trainers, in the newest windows.
* alvin_smart_money_management_classification_challenge (2026-10-12, Lennart): "longer windows starve the first train side", as they would here.

Precedents that kept a small temporal task: coffee_rating_prediction (2026-10-06, Lennart: "the unstable flag measures the noise of single windows, not the task"), rosbank1, apistox and bias_correction_r_bias_correction_r_2 (2026-10-07 to 2026-10-15). In all of them the target had spread in every window.

This dataset sits between the two groups: windows 1 and 2 on the kept side (the model beats the training mean in 3 of 3), window 3 on the retired side. The definition's reason, that the level "keeps every window scorable", answers whether RMSE can be computed. TP-9 asks a different question: whether the scores are noise. Measured the way seismic_bumps was (a script in the run folder, not committed, 4,000 bootstraps over ISO weeks), the model's RMSE gain over the farm's last result has these 95% intervals:
* spring 2021: 0.5 to 92.0
* spring 2022: -7.3 to 67.1
* 2022-23: -17.4 to 101.3

Against the constant 40, the newest window's interval is -24.6 to -11.9: the model is worse. The same intervals bear on TP-10 leg 1, which the definition reports as holding. By ashrae_great_energy_predictor_iii's reading (2026-10-15: point estimates, ahead in 3 of 3 windows) it holds. By g_research_crypto_forecasting's reading (2026-10-22, Lennart: "every 95% day-block interval above" the naive forecast) it holds in 1 of 3. This is the first temporal regression with a dominant value to meet TP-9, so the call here becomes the precedent for the zero-inflated batch.

**Consistency check (AI, 2026-11-01):** your call on basque_offshore_bivalve_biotoxins (keep, with a newest window holding 3 quantified values in 64) differs from seismic_bumps (retired `Too Small`, 2026-09-30: windows of 14-26 positives, intervals of ±0.1 to ±0.14). What sets it apart?
(a) A graded target scores every sample, the non-detects included, where a false alarm costs. Two of the three windows hold an episode, with 26 and 10 quantified values, much as coffee_rating_prediction's windows each held spread. This would be recorded as a TP-9 Cases row (applied, kept) with the intervals above. (b) Treat it like seismic_bumps: `No` + `Too Small`, to revisit when AZTI publishes later seasons. (c) Reopen seismic_bumps: no, it has no graded target. (d) Amend TP-9 to say what "the target's spread" means for a regression with a dominant value, for example a minimum count of values off it per window.

**Consistent with precedent (no flag)**
* Metric: fallback `rmse` in µg/kg on a log-shipped target (MET-3, MET-8). This follows "ship the target on the modelling scale, score on the original scale" (Lennart, 2026-10-21, blood_tests_drink_prediction), as in forest_fires and allstate_claims_severity. Zhou et al.'s R^2 is set aside as a benchmark-wide choice made on a copy that does not carry over (MET-2; Tensions row on the source's metric). The sibling basque_offshore_ctd_chlorophyll does the same (`rmse` in µg/l, log). The peaks dominate the RMSE (builder issue 4), as zillow_prize observed, but here there is no source metric to declare instead. In this batch, the AI's suggestion under Andrej's policy call 3 (2026-10-30) was `rmse` for a quantity in natural units with no pricing use (NFIP).
* Warning `task_target_value_dominant`: follows Andrej's 2026-10-30 calls on this record (policy question 4: tag kept, the code holds 67% and the quantified values lie above it; policy question 2: how a source codes its zeros is a cleaning choice). One wording point: the definition calls the code "not a cap", but the check's own hint lists "a cap (a censored value)", and a below-LOQ code is left-censored. Better: "left-censored at the LOQ, kept as the low regime (Andrej, 2026-10-30)". Unlike the sibling drafts that accept this warning for observed zeros (australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line), this value is a code, and the note should keep saying so.
* Rebuilt from AZTI's release rather than Zhou's copy (PROV-13, PROV-15; Tensions row "Repair against cleaning around damage": coad, corporate_credit_rating, SUPPORT2). Record fields: `original_source` Github to Other and `original_data_state` to several tables (PROV-8, as the screening block argued and as the sibling has them), `required_split` to Temporal. Year 2025 (PROV-9, v1); licence and domain as in the sibling.
* The 64 samples without the okadaic-acid group are dropped (CLEAN-15).
* Plankton and CTD joined from the release's other tables (CLEAN-19, fourth bullet: rain_in_australia, 2026-10-26; mortgage's dated join, 2026-10-22). This holds only if item 2 is settled.
* The farm's last result as the only lag of the target (TP-10 leg 2 as amended 2026-10-26, rain_in_australia).
* Three windows of 44-64 samples (SPLIT-14's minimum; SPLIT-17's about 50 rows; coffee_rating_prediction). The quiet newest year is one window of three, as aeolus kept one of its three in the holiday peak (SPLIT-20). The 12-month horizon is stated as a judgment (SPLIT-12; house-price family case, 2026-10-21).
* Fit approximate for input timing that cannot be verified (USE-8; alfa_battle_2_0_task_2, differentiated_thyroid_cancer_recurrence). One point: `fit_reason` also names "the test windows rest on two toxic seasons". That is a P6 matter (item 5), not one of the gaps USE-8 lists.
* Tag `Two-Regime Zeros` and the CC `Yes`, priority 1 (Andrej, 2026-10-30) are screening calls. Under the stage order in principles.md they hold until this panel's measured findings are in.

**Drift and amendments.** No drift: Andrej's calls of 2026-10-30 on this record and its sibling apply the same definition of the tag. No departure here is the third exception of its kind. The register's CLEAN-19 `amendment_due` (amex_non_iid, fraud_detection: per-entity rows kept as rows) and SPLIT-10 `amendment_due` (ames_housing, perth_house_prices: sales dated by month) rest on other reasons. Its `exception_to_must` flags on SPLIT-14 (alfa_battle_2_0_task_2, lending_club) are exceptions to SPLIT-10 that cite SPLIT-14, caught by a keyword match, so they are not precedents for item 3. The TP-10 `opposite_outcomes` flag is settled by context (stock and appliances_energy_prediction are forecasting). Plankton drives the toxin from outside the series, which puts this dataset on rain_in_australia's side.

**Checks run:** the gap check (item 4) and the per-window intervals (item 5), scripts and outputs in the run folder (not committed). Both reproduce the builder's shipped RMSE. Sources read: the decision register of the batch (flags 1-14), the Cases tables of splits.md, task_probes.md, use_case.md, metrics.md, cleaning_features.md and leak_checks.md, the records of seismic_bumps, digicow_farmer_training_adoption_challenge, alvin_smart_money_management_classification_challenge, kick, expresso_churn_prediction and rain_in_australia, the kick and college_scorecard READMEs (train shares), and the policy calls of 2026-10-30 in `curation/inputs/two_regime_zero_triage_summary.md`.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): basque_offshore_bivalve_biotoxins**

**Position: ship after changes.** The task is real, the data is faithful to the cell, and each validity problem the panel found has a fix in the definition that keeps the task. The open call is TP-9 (a quiet newest window). I argue it is not triggered, and that call belongs to the curator. Window order below: spring 2021 / spring 2022 / quiet year. Model numbers are untuned LightGBM, mean of 5 seeds, RMSE in ug/kg.

**1. A real decision on the exact regulated quantity (P3; USE-1, USE-5, Must).**
- Evidence:
  - Mendexa-Ondarroa is a class-A production area (Basque order of 30 July 2021). Harvesting closes at 160 ug OA eq/kg (Reg. 853/2004), and Art. 63 of Reg. 2019/627 governs reopening (domain practitioner).
  - The descriptor names the decision: "ban the sales when the biotoxins exceed the regulatory limits or temporarily close the harvesting areas as a precautionary measure".
  - The target, OA + DTX1 + DTX2, is the regulated sum since Reg. 2021/1374. PTX1 and PTX2 are never quantified, so the pre-2021 sum is identical (column auditor, domain practitioner).
  - The curator already set `Yes`, priority 1 (CC 2026-10-30).
- Objection answered: precedent-checker item 1 says the level rests on TP-9, a P6 reason for a P3 choice. **Conceded:** the stated reason comes from the wrong rank.
- But the level stands on P3 grounds:
  - precautionary closures act below the limit;
  - the lab reports the level;
  - the level tells the actor how long a closure may last ("Shipping the level is defensible under USE-5", domain practitioner);
  - similar use cases model the level: Cruz et al. 2022 forecast DSP levels in mussels and select by MAE.
  - USE-5 decides number against classes case by case, by the practice of similar use cases.
- Fix: rewrite the Decision's `why` on that ground (consistency-check option (a)) and add the Tensions row. The data does not change.

**2. Faithful data, rebuilt from the origin and verified to the cell (P5; PROV-8, PROV-13, PROV-15, Must).**
- Evidence:
  - The frame rebuilds exactly, with 0 cells different (claim auditor).
  - The blind reviewer, working from the raw files only, matches the target and `last_result` on 280 of 280 rows and the plankton on 98.9%.
  - The sha256 prefixes and the CC BY 4.0 licence check out against the Mendeley API.
  - Zhou et al.'s copy pools 24 toxins in five units, with the coordinates as its only inputs (R^2 about 0). We rebuilt from AZTI's release instead, as the Tensions row "Repair against cleaning around damage" asks.
- Objection: no agent disputes this. Only the record fields need the curator: `original_source` to Other, `original_data_state`, `required_split`, and dropping the outdated `No Good Target (yet)` (PROV-8).

**3. The same-day plankton leak is real; fixing it keeps the task (P4; LEAK-10 and USE-3, Must; remedy by USE-12, Must, and LEAK-7).**
- **Conceded:** the method rules out a count on the sampling day. Samples are Lugol-fixed, stored "until analysis" and settled in 50 ml chambers at an outside lab (Sec. 4.3). 136 of 280 rows use a same-day survey.
- Three agents measured the fix independently, and it survives in every window:

| variant | model RMSE | farm's last result | AUC at 160, model vs last result |
|---|---|---|---|
| plankton >= 1 day, CTD same day (claim auditor) | 265 / 137 / 45 | 286 / 162 / 69 | 0.87 / 0.92 vs 0.83 / 0.89 |
| same variant (column auditor) | 264 / 134 / 39 | 286 / 162 / 69 | not restated |
| plankton 2 days, toxin 3 days (domain practitioner) | 260 / 128 / 33 | 336 / 142 / 69 | 0.90 / 0.94 vs 0.81 / 0.91 |

- Same-day CTD is right: it is measured in situ.
- The 7-day toxin lag hides no leak. With a 1-day lag the model scores 234 / 136 / 19 and persistence gets worse (321 / 155 / 69).
- Why the task stays: USE-12 says a leak is no reason to reject a real task, and the fix is step 2 of the remedy ladder. The closest precedent, rain_in_australia, replaced its after-the-point values with D-1 values and kept the task.
- Fix:
  - match plankton surveys strictly before the sample day (>= 1 day, or 2 days for settling and shipping);
  - keep the CTD on or before the day;
  - state one turnaround per analysis in the prediction-point bullet, in `known` and in `fit_reason`, quoting Sec. 4.1's "within two days of sampling".

**4. Tabular, not forecasting (P2 via SEL-10; TP-10, Must).**
- Leg 2 holds. The only lag of the target is the farm's last result, which is known and read by the actor (the amendment of 2026-10-26); it matches on 280 of 280 rows.
- Leg 1 holds on the declared metric in 3 of 3 windows:
  - as shipped: model 249 / 128 / 22 against the last result 286 / 162 / 69 and the month mean 277 / 195 / 208;
  - after the fix in point 3: still 3 of 3.
- Plankton drives the toxin from outside the series: Dinophysis acuminata has Spearman 0.63 with the target (blind reviewer). That puts this dataset on rain_in_australia's side.
- **Conceded:** "clearly" is not shown. The interval of the gain over persistence excludes 0 only in spring 2021 ([2.5, 90.8]). By ashrae's reading (point estimates, 3 of 3) leg 1 holds; by g_research's reading (every interval above) it holds in 1 of 3.
- Remedy: check against the tuned methods on the shipped splits before closing (TP-1), and write "beats in point estimates in 3 of 3 windows".
- Disputed: the constant 40, which wins the quiet window (3.3), is the target's mode, a dummy. TP-10's Methods name the last value and the same-season profile as the naive forecasts, and the model beats both. The constant scores 303 / 189 in the toxic windows. The quiet window belongs to point 5.

**5. Worth benchmarking: one quiet window does not trigger TP-9 (P6; TP-9, Must; TP-2, Should).**
- Evidence:
  - Two of the three windows carry an episode with spread: 26, 10 and 3 quantified values, and 16, 7 and 0 above 160. The test pool holds 39 quantified values, from 41 to 1,693.
  - In both toxic windows the model beats the training-mean dummy (288 / 180) and persistence.
  - Its gain over the constant 40 has 95% intervals of 21.9 to 93.6 (spring 2021) and -2.4 to 99.0 (spring 2022) (precedent-checker).
  - No split that meets SPLIT-14 avoids a quiet newest window, because the last exceedance is on 2022-05-23 (split auditor). The quiet window comes from the data's calendar, not from the definition.
- What sets it apart from seismic_bumps: seismic had a binary label, with 14-26 positives per window. Here the target is graded, so every non-detect is scored too. A false alarm in a quiet year costs the farm a week of sales (domain practitioner), so the quiet window measures a cost the actor really carries.
- Rules on this side:
  - the Tensions row "the right split against the score" (P4 over P6, forest_fires): the split follows the application;
  - coffee_rating_prediction kept windows of uneven signal;
  - TP-2: a small real signal is no reason to retire.
- **Conceded:**
  1. In each toxic window, 3-4 peaks carry 84-90% of the squared error, and the early-warning value rests on 5 onsets.
  2. After the plankton fix, the model loses to the training-mean dummy in the quiet window (39-45 against 33.8). The model then beats the dummy in 2 of 3 windows.
  3. This is the first temporal regression with a dominant value to meet TP-9, so the call sets the precedent.
- Recommendation: keep it as a tiny temporal task, with a TP-9 Cases row holding the intervals (precedent-checker option (a)). Exclusion is the last rung of the ladder.

**6. The regime is right; the split's two defects have fixes that keep it (P4; USE-10, SPLIT-1, SPLIT-3, Must, hold; the reading of SPLIT-14, Must; SPLIT-10, Should).**
- What holds: the farms are known and have history, so the split is temporal (USE-10). Train ends before test in every window, and the rows of one day stay together (split auditor).
- SPLIT-14, **conceded:** both sentences that justify counting days are wrong.
  - Exceedance months hold 27.0% of the sampling days and 27.1% of the samples.
  - Counted in rows, the test pool starts on 2021-06-07 and holds 13 exceedances, not July and 7.
- But counting days is not a breach:
  - the tooling's `unit="unique"` counts distinct values, and kick ships under it with 48.7% of its rows;
  - there is an honest reason: the rows of one day share every feature (37 mussel/oyster pairs differ only in shellfish and target), so days measure what a refit has seen.
- Either remedy keeps the dataset:
  - (b) the curator settles the reading of SPLIT-14 (it applies to kick too), and we rewrite the reason;
  - (a) re-split on the day-aligned cutoffs 2021-06-07, 2021-11-30 and 2022-07-04.
- I prefer (b). Option (a) cuts the test exceedances from 23 to 13 and window 1 to 37 rows, below SPLIT-17's ~50. It weakens point 5 for 5 points of train share.
- SPLIT-10, **accepted:** a 7-day gap, matching the definition's own turnaround.
  - It costs 6 rows, and RMSE becomes 246 / 125 / 20.
  - It removes the onset shortcut measured in the first days of spring 2021 (precedent-checker).
  - The gap follows the toxin lag if that changes.
- Text fixes:
  - window 1 is a refit in the middle of an episode, with 8 of the 24 exceedances of 2021 in training;
  - reword `task_summary.split`, `splits_comment` and `fit_reason`;
  - add a History bullet (SPLIT-20).

**7. The metric is the right fallback (P6; MET-8, Should; MET-3 and MET-2, Must).**
- Evidence:
  - The origin defines no metric, and Zhou's R^2 is on a copy that does not carry over (MET-2).
  - RMSE in ug/kg on a log-shipped target follows MET-3 and the blood_tests_drink_prediction precedent. The sibling basque_offshore_ctd_chlorophyll does the same.
  - ug/kg is the regulatory unit, and the error at the peaks bears on how long a closure lasts.
- **Conceded:** the peaks dominate RMSE. RMSLE from context (MET-11) is a defensible curator option, but it flips TP-10 leg 1 in the quiet window (0.35 against 0.32), so it needs that check first.
- Cheap fixes:
  - report the ROC AUC and the recall at 160 per window in the notes;
  - add Revilla et al. 2025 (doi:10.1016/j.rsma.2025.104556), the source team's own early-warning study of OA, to the metric reason and the record (MET-1). A human should read its methods.

**Changes I accept (none excludes the dataset)**
1. Plankton surveys strictly earlier and CTD same day; restate the turnarounds (point 3).
2. The level's reason on P3 grounds (point 1).
3. A 7-day gap; the SPLIT-14 reading settled by the curator, or the day-aligned re-split (point 6).
4. Text fixes:
   - "June 2016" should be April 2016;
   - 42 taxa ship, not 45;
   - "87 within 3 days" includes 37 same-day pairs;
   - dissolved oxygen is derived from saturation, T and S, not a copy of the saturation;
   - the Niskin surveys hold 1 to 6 depths;
   - "not a cap" should read "left-censored at the LOQ, kept as the low regime (Andrej, 2026-10-30)";
   - the OA group was not measured in 2020; the year was not quiet;
   - "clearly beats" should say point estimates;
   - the record's "129 above" should be 125.
5. Cheap P7 changes: merge the two Ostreopsis columns (CLEAN-12); add a note on the 16 taxa that depend on the counting lab (CLEAN-21).
6. Record fields per PROV-8.

```text
Verdict: ship after changes.
Validity: USE-1/USE-5 hold (level on a P3 ground, reason rewritten); PROV-8/13/15 hold (0 cells differ);
  LEAK-10/USE-3 triggered (same-day plankton, 136 rows), fixed by lagging plankton (USE-12); SPLIT-1/3 hold;
  SPLIT-10 fixed (7-day gap); SPLIT-14 a reading for the curator; TP-10 holds on point estimates (TP-1 tuned check).
Value: TP-9 two episode windows with spread and one quiet window: keep as a tiny temporal task (curator's call);
  MET-8 rmse kept, AUC at 160 in the notes.
Quality: CLEAN-12 Ostreopsis merge, CLEAN-21 note, text fixes.
Weighed: source +, use case +, size -, test signal on two seasons -.
For the curator: TP-9 keep or Too Small; the SPLIT-14 unit.
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): basque_offshore_bivalve_biotoxins**

**Verdict: do not ship as defined.** Points 2 to 5 and 7 can be fixed in the definition or its text. After those fixes, ship only if two things go for keep: the re-run of the scope test (point 1) and the curator's TP-9 call (point 6). If either goes the other way: `No` with `Too Small`. Windows are listed oldest first (spring 2021 / spring 2022 / the quiet year). Model numbers are untuned LightGBM with the builder's settings, mean of 5 seeds, RMSE in ug/kg.

**1. P2, SEL-10 through TP-10 (Must): it is not shown that this is a tabular task once the inputs are honest.**
- Problem: TP-10 leg 1 asks the model to "clearly beat the forecasts built from the series itself". The definition shows this only against the farm's last result and its month mean, on inputs that include the leak of point 3. The builder's naive set leaves out the strongest naive forecast for the quiet window: the farm's training median, 40.
- Effect: if the features add nothing beyond the farm's own series, the benchmark scores forecasting, which is out of scope.
- Evidence: my re-run uses the leak-fixed inputs (plankton at least 1 day old, CTD same day, last result at least 7 days old), with a bootstrap over ISO weeks (script and output in the run folder, not committed).
  - Model RMSE 264.5 / 137.0 / 45.3. Best naive forecast of each window: month mean 274.0, last result 161.9, farm median 3.3.
  - 95% intervals of the model's gain over that forecast: [-29.7, 69.6] / [-17.3, 50.6] / [-65.5, -21.0]. The gain is not separated from zero in either toxic window, and in the quiet window the model is clearly worse.
  - Without the last result the model scores 272.4 / 163.4 / 63.2, so it loses to the last result in spring 2022.
  - The shipped inputs do not change the picture: the intervals over the last result are [0.5, 92.0] / [-7.3, 67.1] / [-17.4, 101.3] (precedent checker), and the model loses to the constant 40 (21.9 against 3.3).
  - Precedents: on point estimates in 3 of 3 windows (the ashrae reading), this holds in 2 of 3. With every interval above the naive forecast (the g_research_crypto_forecasting reading), it holds in 0 of 3.
- Remedy (re-measure, then a note): after fixing point 3, read TP-10 leg 1 against tuned results (TP-1, EV-3), with the farm median in the naive set, and record which precedent's reading applies. The curation bullet "A tabular task, not forecasting" must report the comparison it leaves out. If leg 1 fails, the verdict is `No`. The marker is SEL-10's, or TP-9's if the windows are too thin to decide.

**2. P3, USE-5 (Must): the target choice rests on a lower-ranked reason.**
- Problem: the actor's decision is the exceedance of 160. The descriptor says to "ban the sales when the biotoxins exceed the regulatory limits", the use_case says "decides whether to stop harvesting", and the screening wrote "a predicted exceedance". The definition ships the level for one stated reason: an exceedance target would leave the newest window with one class (TP-9). That is a P6 reason for a P3 choice, which the ranking does not allow (principles.md, "Conflicts between rules").
- Effect: if the level stands only on TP-9, the definition dodges the TP-9 verdict instead of facing it.
- Evidence: the `Decision` "A level, not the exceedance" and the metric reason cite only TP-9. The domain practitioner: "My action is binary (close or not at 160). I would want a probability that the coming result exceeds 160, and a level as second best". Precedent checker item 1: no precedent ships a level to escape a thin binary target, and seismic_bumps and digicow faced TP-9 with their binary targets.
- Remedy (fix the definition's reason): the level can stand on P3 grounds. Precautionary closures are decided below the limit, the laboratory reports the level, and the level tells how long a closure may last. If the curator accepts that, restate the `Decision` and the "Why a level" bullet on those grounds and add a Tensions row. If the curator does not, ship the exceedance and let TP-9 decide (0 exceedances in the newest window).

**3. P4, USE-3 and LEAK-10 (Must): plankton counts from the sampling day are used as known on that day.**
- Problem: in 136 of 280 rows (48.6%), the plankton features come from a survey on the sample's own day. The prediction point is "the day a bivalve sample is taken, before its toxin result".
- Effect: the model is credited with information that no manager has before the result.
- Evidence:
  - The descriptor (Sec. 4.3) says the water samples were "fixed with acidic Lugol's solution and preserved in the dark and cool (4 °C) until analysis". In the outside lab (UPV/EHU or Oceansnell), "a subsample (50 ml) was sedimented". Settling takes 20 to 50 h (column auditor, domain practitioner).
  - The toxin analysis was "initiated within two days of sampling" for refrigerated samples (Sec. 4.1). So the two turnarounds are similar, while the definition gives plankton 0 days and toxins 7.
  - Measured cost: plankton at least 1 day old with CTD same day gives RMSE 249/128/22 to 265/137/45 and ROC AUC at 160 0.92/0.97 to 0.87/0.92 (claim auditor).
  - Precedent rain_in_australia (2026-10-26): when the timing can be read two ways, keep only what holds under both readings.
  - "Our reading" is a disclosure, not a reason. USE-8 says a kept leak is named as kept, not counted as a fit gap.
- Remedy (fix the definition, LEAK-7): match plankton surveys strictly before the sample day (1 day; 2 if the curator wants settling time) and keep the same-day CTD, which is measured in situ. The builder's variant also lagged the CTD, which overshoots: 258/136/60. Then state one turnaround per analysis in the prediction-point bullet, in `known` and in `fit_reason`, and quote Sec. 4.1. A Must takes no exception.

**4. P4, SPLIT-14 (Must): the training floor is counted in days, and the stated reason for that is false.**
- Problem: the oldest window trains on 126 of 280 samples (45.0%), which is 120 of 237 sampling days (50.6%). The only reason given is that episodes add samples, so "samples would let the outcome set the windows". The data refutes it, and the definition's claim about the row-counted alternative is wrong.
- Effect: the rule's floor is met only on a reading that no curator has made. Every stated precedent counts rows: california_house_prices_2020, melbourne_housing_market, garments_worker_productivity and wisconsin. kick, which counts days (48.7% of rows), was never reviewed.
- Evidence:
  - Exceedance months hold 27.0% of the days and 27.1% of the samples. Days with a quantified value have 1.16 rows each, non-detect days 1.19.
  - The gap between days and rows comes from same-day mussel and oyster pairs, mostly in the quiet last year: 25 of window 3's 39 days hold two or more rows.
  - Counted in rows, the test pool starts on 2021-06-07, not in July, and holds 13 exceedances, not 7 (claim and split auditors).
- Remedy (re-split or amend; the curator chooses):
  - (a) A day-aligned row floor: cutoffs 2021-06-07, 2021-11-30 and 2022-07-04 with 35-day windows (split auditor).
  - (b) Amend SPLIT-14 to name the unit, on the honest argument: the rows of one day share one survey and one cast.
  - Either way, delete the two false sentences in `splits_comment` and in the "Why a level" bullet.
  - Note that (a) worsens point 6: window 1 would hold 37 rows with 12 quantified, and its log skill would be 0.054.

**5. P4, SPLIT-10 (Should, applies SPLIT-9) and SPLIT-12 (Should): no gap for the definition's own turnaround, and the windows are described wrongly.**
- Problem 1: the last-result feature treats a toxin result as known 7 days after its sample, yet every training side runs to the day before its window.
- Problem 2: "a model refit before each toxic season" holds for one window of three.
- Evidence:
  - 6 training rows fall within 7 days of a window start. Window 1's three are the onset of the 2021 episode: Mussel Farm samples of 2021-04-13 to 15, at 73, 75 and 52 ug/kg.
  - A 7-day gap gives 246.0/126.3/20.4, so it costs nothing (split auditor).
  - On the first 14 days of window 1, the gap raises RMSE from 145.9 to 232.8. That rests on 4 samples, so it points to a SPLIT-9 shortcut without proving it (precedent checker).
  - house_sales set a one-week gap for a 6-day median delay.
  - Window 1 opens on 2021-04-19, 40 days into the episode that began on 2021-03-10, with 8 of its 24 exceedances on the training side.
- Remedy (fix the definition): a gap equal to the toxin lag the definition settles on (7 days now, 3 if point 3 shortens it), declared on `Temporal`. Reword `task_summary.split`, `splits_comment` and `fit_reason`: "two toxic seasons" is in fact the second half of one plus one.

**6. P6, TP-9 (Must): the newest window holds no spread, and the toxic windows rest on a handful of samples.**
- Problem: "the level keeps every window scorable" says the RMSE can be computed. TP-9 asks a different question: whether the scores are noise.
- Effect: the score mostly measures two things, closeness to the code in a quiet year and the error on 3 or 4 peaks. The early-warning decision, an onset before the lab result, appears in 5 test rows across all windows. 18 of the 23 test exceedances fall while the farm is already closed (domain practitioner).
- Evidence:
  - Newest window: 61 of 64 rows at the code, 3 quantified (max 60), 0 above 160.
  - There the constant 40 scores 3.3, against 21.9 for the model; the interval of the model's gain over the constant is [-24.6, -11.9] (precedent checker).
  - In the toxic windows, the top 3 samples carry 84% and 89% of the squared error (claim auditor).
  - No split that meets SPLIT-14 avoids this (split auditor). The blind reviewer found the last window degenerate under 5-, 6-, 8- and 10-block cuts.
  - Precedent seismic_bumps (2026-09-30): retired `Too Small` with 14 to 26 positives per window. This dataset has 16/7/0 exceedances and 26/10/3 quantified values (12/11/2 under the row floor).
- Remedy: the definition cannot fix this; no repair is possible until AZTI publishes seasons after 2023. Keep it only if the curator records a TP-9 Cases row or an amendment that says what "the target's spread" means for a regression with a dominant value, with the per-window numbers in the notes. Otherwise `No` with `Too Small`, to revisit when AZTI publishes later seasons. This call becomes the precedent for the zero-inflated batch.

**7. P6, MET-1 (Must): RMSE in ug/kg scores the peaks, not the closure decision.**
- Problem: the declared metric is decided by samples far above the limit, where the manager's decision (closed) is not in doubt.
- Effect: two models that act very differently at 160 get the same score.
- Evidence:
  - In the toxic windows, 85% and 90% of the squared error comes from the 4 highest samples, all far above 160.
  - Spring 2021: log-target and raw-target LightGBM score 249 and 248, with recall at 160 of 0.56 and 0.94 (domain practitioner).
  - Quiet window: 72% of the squared error is on non-detects, and no prediction crosses 160 (claim auditor).
  - "Where we looked" leaves out Revilla et al. 2025 (Regional Studies in Marine Science 91:104556), the source team's own OA early-warning study, which nobody has read (claim auditor).
- Remedy: the curator chooses between `Metric.from_context("rmsle", target_transform="log")` (MET-11 context, as for diamonds and the collection's other skewed quantities; the limit is 4 times the LOQ and the noise is multiplicative) and the RMSE kept with a note on the peaks. Either way, report the ROC AUC at 160 per window in the notes, and add Revilla et al. 2025 to the metric reason once someone has read its methods. Under RMSLE the model also loses the quiet window to the last result (0.35 against 0.32), which is consistent with point 1.

**Not reasons to exclude (P7, text only):**
- 45 taxa should be 42;
- "June 2016" should be April 2016;
- the "87 within 3 days" include 37 same-day pairs;
- dissolved oxygen is not "a copy" of the saturation;
- "not a cap" should read "left-censored at the LOQ";
- 2020 is missing from the episodes because it was not measured;
- the record fields should change under PROV-8.

The other agents list these in their reports. I ask only that they be fixed.

```text
Verdict: do not ship as defined; after changes, ship only if points 1 and 6 go for keep, otherwise No + Too Small.
Validity: SEL-10/TP-10 leg 1 not established on honest inputs (re-run, tuned); USE-5 reason from a lower rank
  (restate on P3 grounds or ship the exceedance); USE-3/LEAK-10 triggered (plankton strictly earlier, CTD same day);
  SPLIT-14 floor in days on a refuted reason (re-split in rows or amend); SPLIT-10 no gap (7-day gap); SPLIT-12 text.
Value: TP-9 newest window without spread, toxic windows on 3-4 samples (curator's call: Cases row or Too Small);
  MET-1 RMSE scored by peaks (rmsle from context or a note; AUC at 160 in the notes).
Quality: text fixes only.
For the curator: points 1 and 6 decide; point 4 (unit of the floor) is a reading of a Must.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): basque_offshore_bivalve_biotoxins**

**Where we stand.** I agree the dataset cannot ship as defined, because the same-day plankton (critic point 3) has to be fixed first.
- Agreed, with the same remedies: points 2, 3, 4 and 5, and the text fixes.
- Disputed: points 1 and 6, and part of 7.

I ran four checks; the first three decide point 1 and also bear on point 6. Scripts and outputs are in the run folder (not committed).

How the checks were run:
- Frame: the leak-fixed one (plankton at least 1 day old, CTD same day, last result at least 7 days old).
- Model: untuned LightGBM, the builder's settings, 5 seeds.
- Scores: RMSE in ug/kg, with intervals from a bootstrap over ISO weeks.
- Windows oldest first: spring 2021 / spring 2022 / quiet year.

**1. TP-10 leg 1 (P2 via SEL-10, Must): narrowed.**
- **Disputed: the critic's "best naive forecast" is picked on the test window.** The critic's script takes the `min` of each naive forecast's RMSE on the test rows. No forecaster has that choice.
- The farm median wins the quiet window (3.3) only in hindsight. Scored on the newest 39 sampling days of each training side, it gets 173 / 303 / 189: the worst of the four naive forecasts in two windows and third in one.
- TP-4's raw-feature test picks the competitor "on each split's training side". The same should hold here (EV-1).
- **Check 1**: the naive forecast is chosen on the training side, which picks the month mean, the month mean and the last result.

| scope | full model | chosen naive forecast | 95% interval of the gain |
|---|---|---|---|
| spring 2021 | 264.5 | 274.0 | [-29.5, 68.6] |
| spring 2022 | 137.0 | 196.0 | [8.5, 132.3] |
| quiet year | 45.3 | 68.7 | [-29.6, 57.0] |
| pooled, 154 rows | 162.7 | 186.8 | [0.1, 59.5] |

- **Conceded, a new fact (check 2):** in the full untuned model, the plankton and CTD add nothing over a series-only LightGBM. The series-only model uses station, shellfish, laboratory, date terms, and the last result with its age.
  - Pooled: full 162.7 against series-only 156.4, gain [-21.0, 13.2].
  - In spring 2021 the series-only model is better (239.0 against 264.5).
  - On this evidence alone, the critic's worry stands.
- **Check 3**: the series inputs plus the OA-producing taxa the column auditor names (Dinophysis, Phalacroma, Prorocentrum lima) and the survey age. I declared this set before running it.
  - The model scores 235.1 / 118.5 / 54.7.
  - Against the series-only model it is ahead in 3 of 3 windows; pooled gain [3.5, 20.6].
  - Against the naive forecast chosen on the training side: ahead in 3 of 3, with intervals [2.8, 85.9] / [40.7, 129.3] / [-32.0, 38.0]; pooled [19.7, 67.6].
  - Against the last result, pooled: [16.5, 60.2].
- **What check 3 shows:** the outside plankton signal is in the data. In an untuned model, 50 sparse columns on 126 to 216 training rows dilute it. That is the kind of question TP-1 says to settle on tuned methods, and CLEAN-22 forbids dropping columns for width.
- **Caveat:** check 3 is one feature set, chosen by domain knowledge after check 2, not by its test score. It shows that the signal exists; it does not replace the tuned re-read.
- **What follows:** I agree with the critic's remedy, with one change. Re-read leg 1 on the tuned results, with the naive forecast chosen on the training side; the farm median stays among the candidates.
- **Which reading applies:**
  - Per-window intervals separate in only 1 or 2 of 3 windows, because each window has 21 to 33 weeks. So the g_research reading fails at this size, whatever the task.
  - The pooled reading and the ashrae reading hold.
  - The curator decides which reading applies. I argue for the pooled one, because separating 44 to 64 rows per window is TP-9's question, not SEL-10's.

**2. USE-5: conceded.**
- Same remedy as my opening point 1: restate the Decision and the "Why a level" bullet on P3 grounds, and add a Tensions row.
- Narrowing: the curator can still ship the exceedance. But the P3 reasons are on the record now:
  - precautionary closures are decided below the limit;
  - the level tells how long a closure may last;
  - Cruz et al. 2022 forecast the level.
  So the level no longer leans on TP-9.

**3. USE-3 / LEAK-10: conceded.** The remedy is the one the critic gives: plankton strictly earlier, CTD same day, one turnaround per analysis, quoting Sec. 4.1.

**4. SPLIT-14: the false sentences conceded; the reading belongs to the curator.**
- We agree on the facts and on both remedies, and both of us note the cost of (a): window 1 would hold 37 rows with a log skill of 0.054.
- I still prefer (b).
- kick ships under the days reading and was never reviewed, so the answer here settles kick too (principles.md, "Treat like cases alike").

**5. SPLIT-10 / SPLIT-12: conceded.** A 7-day gap, or whatever toxin lag is settled, plus the rewording.

**6. TP-9: narrowed.**
- **Conceded:**
  - the quiet window mostly scores closeness to the code (61 of 64 rows at 40);
  - the early-warning value rests on 5 onsets;
  - 3 or 4 peaks carry 84-90% of each toxic window's squared error.
- **Disputed: TP-9 asks whether "the scores are noise".** On honest inputs, the toxic windows' scores are not:
  - check 1's full model beats the naive forecast chosen on the training side in spring 2022, [8.5, 132.3];
  - check 3's model beats it in both toxic windows, [2.8, 85.9] and [40.7, 129.3].
- seismic_bumps retired because its AUC intervals of ±0.1 to ±0.14 could not separate methods. Here a model separates from the naive forecast in 2 of 3 windows.
- **Disputed:** the constant 40 is not a choice a forecaster would make ex ante (point 1). So its interval [-24.6, -11.9] does not show that the scores are noise. It shows that the quiet window rewards calibration at the code. A needless closure is what that window tests, and it costs the farm a week of sales (domain practitioner).
- **What follows:** I accept the critic's form of remedy: a TP-9 Cases row or an amendment that carries the per-window numbers, otherwise `Too Small`. My recommendation stays keep, with the intervals from checks 1 and 3 in the Cases row.

**7. MET-1: conceded that the peaks dominate; narrowed on the alternative.**
- **Agreed:**
  - the recall example (RMSE 249 against 248, with recall at 160 of 0.56 against 0.94) shows that RMSE does not score the decision at 160;
  - the ROC AUC and recall at 160 per window go into the notes;
  - Revilla et al. 2025 goes into the metric reason once someone has read it.
- **New fact for the curator's choice** (check 4, leak-fixed frame), RMSLE per window:

| | spring 2021 | spring 2022 | quiet year |
|---|---|---|---|
| full model | 0.91 | 0.58 | 0.49 |
| last result | 1.00 | 0.64 | 0.32 |
| farm median | 1.44 | 0.89 | 0.07 |

- Under RMSLE the model loses the quiet window to the last result, a naive forecast that needs no hindsight. If RMSLE is declared, TP-10 leg 1 has to be re-read on it, and it fails in 1 of 3 windows on point estimates.
- I do not argue the metric from this, because MET-1 asks what scores the real task, not what keeps the dataset. The curator should see it before switching.

**Text fixes:** agreed in full.

```text
After rebuttal: ship after changes (agreed: plankton strictly earlier, CTD same day; level on P3 grounds;
  7-day gap; text fixes).
For the curator:
  TP-10 leg 1: re-read on tuned results, naive forecast chosen on the training side (advocate: keep; untuned pooled
    gain over it [0.1, 59.5] with all features, [19.7, 67.6] with the DSP taxa; with all features the plankton/CTD
    add nothing over the series).
  TP-9: advocate keep, with a Cases row; toxic windows separate from the naive forecast in 2 of 3.
  SPLIT-14 unit: advocate days, settled as a reading (applies to kick).
  Metric: rmse or rmsle; rmsle fails TP-10 leg 1 in the quiet window.
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): basque_offshore_bivalve_biotoxins**

**Revised verdict: not as defined.** The advocate accepts the changes of my points 2, 3, 5 and 7, and the two of us agree on how SPLIT-14 gets settled. One disagreement remains, TP-9. Like cases point to `Too Small` (seismic_bumps), unless the curator records the graded target as the fact that sets this case apart. I narrow my point 1 to a tuned check and a note: it is no longer a condition for shipping. New checks: a script and its output in the run folder (not committed). They use the builder's untuned LightGBM, 5 seeds, and 95% bootstrap intervals over ISO weeks. Windows are listed oldest first.

**Advocate 1, the level on P3 grounds (USE-5): conceded.** This is the remedy I asked for in my point 2: rewrite the `Decision` on P3 grounds and add a Tensions row. I have no further objection, provided the reason is actually rewritten.

**Advocate 2, faithful data (PROV-8, PROV-13, PROV-15): conceded.** No agent disputes it.

**Advocate 3, the plankton leak and its fix (LEAK-10, USE-3, USE-12): conceded, with one narrowing.** The fix is the one in my point 3. But "it survives in every window" holds only on point estimates. The new check uses the leak-fixed inputs (plankton at least 1 day old, CTD same day). There, the model's gain over the farm's last result has intervals of [-18.2, 91.1], [-18.3, 50.8] and [-29.5, 56.6]: zero is inside all three. That bears on TP-10 (next item), not on the fix.

**Advocate 4, TP-10 leg 1: narrowed. I concede the dummy point and keep "clearly".**
- Conceded: the farm's median, 40, is the target's mode, a dummy. It is not a naive forecast that TP-10's Methods name. The model's loss to it in the quiet window belongs to TP-9. I withdraw that part of my point 1.
- Conceded: the newest TP-10 case, rain_in_australia (2026-10-26), counts the windows where the model is ahead on point estimates ("ahead in 9 of 9 windows"). On the leak-fixed inputs the model is ahead of every forecast the Methods name in 3 of 3 windows: 264.5 / 137.0 / 45.3, against the last result 285.9 / 161.9 / 68.7, the month mean 274.0 / 196.0 / 207.7 and the month median 293.7 / 194.5 / 103.0.
- Kept: the rule says "clearly beats". Rules rank above precedents (principles.md, "Conflicts between rules"), and rain_in_australia's margin was large (ROC AUC 0.849 against 0.752). Here the margins are thin:
  - in spring 2021 the model beats the month mean by 9.5 ug/kg (3.5%), with an interval of [-28.9, 68.6];
  - against the best named forecast of each window, the interval excludes zero in 0 of 3 windows on the leak-fixed inputs;
  - even on the shipped inputs, the interval over the month mean in spring 2021 is [-16.8, 79.2]. The advocate's "1 of 3" compares only with the last result.
- Remedy (both sides accept the first two): the tuned check (TP-1); the wording "ahead in point estimates in 3 of 3 windows"; and the intervals in the notes, so the curator can see how thin "clearly" is. If the tuned methods also stay ahead in 3 of 3, I do not ask for more.

**Advocate 5, TP-9 not triggered: disputed. The quiet-window fact is narrowed in the advocate's favour.**
- The advocate's rules do not decide TP-9:
  - The Tensions row "the right split against the score" (forest_fires) and TP-2 deal with a small signal under the right split. TP-9 asks a different question: whether the windows hold enough minority rows or spread for the score to be more than noise.
  - principles.md, "How to decide", step 4, covers exactly this: "A very real task with a handful of units per class per test fold is still `Too Small`, because nothing ranked above it makes the fold scorable."
  - coffee_rating_prediction does not help: in it and in the other kept small temporal tasks, "the target had spread in every window" (precedent checker). Window 3 here has 3 quantified values in 64.
- Like cases: seismic_bumps was retired with 14 to 26 positives per window. Here the windows hold 16 / 7 / 0 exceedances and 26 / 10 / 3 quantified values. Windows 2 and 3 are thinner than any of seismic_bumps' windows.
- Narrowed: the graded-target argument now has a measured fact behind it.
  - On the leak-fixed inputs, 2 of the 64 quiet-window predictions cross 160 (max 335.6). These are false closures, and RMSE penalises them.
  - On the shipped inputs, no prediction crosses 160 (max 148.5).
  - So once the inputs are honest, the quiet window does score a cost the actor carries. But that cost rests on 2 rows.
- The advocate's intervals over the constant 40 ([21.9, 93.6] and [-2.4, 99.0]) were measured on the leaky inputs. They need to be re-measured after the fix. The advocate also concedes that after the fix the model loses to the training-mean dummy in the quiet window.
- Remedy (unchanged): this is the curator's call. Keep only with a TP-9 Cases row that names the fact (a graded target that scores false closures in a quiet year: 2 of 64 here) and gives the per-window intervals. Otherwise `No` with `Too Small`.

**Advocate 6, the split: agreed on SPLIT-10. On SPLIT-14, narrowed to the ground for option (b).**
- SPLIT-10: agreed. A 7-day gap that follows the toxin lag.
- SPLIT-14: the advocate prefers (b) because (a) "weakens point 5". That chooses the split for the score, which is the thing the advocate's own Tensions row forbids (P4 over P6: "the split follows the application").
- kick is no support: "no decision has looked at that" (precedent checker). The curator decisions that state the floor all count rows: california_house_prices_2020, alfa_battle_2_0_task_2, lending_club, melbourne_housing_market. Under "Who decides", they set the default.
- Option (b) stands only on its P4 ground: the rows of one day share one survey and one cast, so days measure what a refit has seen. If the curator amends SPLIT-14 on that ground, I agree.

**Advocate 7, the metric: agreed on the floor. One argument disputed.**
- Disputed: "the error at the peaks bears on how long a closure lasts". Under Art. 63 of Reg. 2019/627, an area reopens after two consecutive results below 160, at least 48 h apart. So the length of a closure is set by when the level falls below the limit, not by how high the peak was.
- Peak values also swing by a factor of 2 to 4 within days: 456 → 1005 → 307 ug/kg at the Mussel Farm over 19, 21 and 24 May 2021 (domain practitioner). Much of the error at the peaks is sampling and laboratory noise.
- Agreed: the ROC AUC and the recall at 160 per window in the notes, and Revilla et al. 2025 added once someone has read its methods. RMSLE or RMSE with a note stays the curator's choice (MET-1, MET-11).

```text
Verdict: not as defined; after the agreed changes, the one open call is TP-9 (default Too Small by seismic_bumps
  unless a TP-9 Cases row names the graded-target fact: 2 false closures in 64 quiet-window rows on honest inputs).
Conceded: USE-5 reason (rewrite on P3), PROV, the plankton fix, SPLIT-10 gap, the farm median as a dummy.
Narrowed: TP-10 leg 1 holds on point estimates 3 of 3 after the fix (rain_in_australia's reading); "clearly" not
  shown by intervals (0 of 3); tuned check and the intervals in the notes.
Disputed: TP-9 not triggered (principles step 4; coffee had spread in every window); SPLIT-14 (b) chosen for the score;
  peaks set the closure length (Art. 63 says the fall below 160 does).
```

</details>
