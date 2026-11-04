# airqo_low_cost_air_quality_monitor_calibration_challenge

**Outcome:** added. A second-pass review panel after Lennart's PR #33 marks recommends shipping after changes.
Validity: USE-1/USE-3 were triggered by retrospective wording left from the random split, and USE-8 by citing the
paper's future work as AirQo practice; both are fixed in the text (a monthly refit corrects that month's new readings,
no reference value from that month is known, network transfer is named as the gap); LEAK-10 holds (no column leaks, no
row copied across the split; the task gamer's one gain, the previous hour's reference, is excluded by that prediction
point); SPLIT-1/4/11/13/14 hold; SPLIT-20 is departed from without a recorded fact (issue 1); CLEAN-11's
training-period clause is departed from for one test row (issue 2); the target keeps a 92-hour reference outage
(issue 3). Value: TP-2 holds (LightGBM 18.26 RMSE against 41.22 for the training mean and 25.32 for the raw sensor);
MET-1..4 hold (the source's RMSE). Quality: dead-channel hours missed by the sensor-2 rule (issue 4); the stale notes
in the definition are fixed (EV-7). Weighed: three sites (-), a real named use (+), the source paper (+), the shape
(+). For the curator: issue 1 first.

**Main points:** Widen the test windows beyond the dry season (issue 1; decide it first, since it moves the spikes of
2 and the outage of 3 into test windows), and decide three cleaning changes the panel recommends but did not make:
keep the Makerere test-window spike as a label (2), drop the Nakawa reference outage (3), one dead-channel rule for
both sensors (4).

**Record fields that disagree with the definition:**

- `required_split`: record `Random (IID)`, definition `Temporal (NON-IID)`.

**Issues for Lennart:**

1. **Widen the test windows beyond the dry season?**

   * **Problem:**
     - All three test months, December 2020 to February 2021, fall in Kampala's dry, high-PM2.5 season.
     - Each test month scores a different mix of sites, and February dominates the score.
     - The rules ask to widen the windows when the newest ones fall in an atypical season, or else to record the
       fact that sets the case apart[^split20].
   * **Background:** mean reference 44.9, 49.6 and 74.4 µg/m³ in the three test months, against 35.9 to 43.1 in
     September to November 2020. Labeled hours per site and month (the critic's count on the raw file, confirmed by
     the mediator):

     | Month | Makerere | Nakawa | USEmbassy |
     |---|---|---|---|
     | Oct 2020 | 383 | 543 | 390 |
     | Nov 2020 | 153 | 352 | 186 |
     | Dec 2020 | 578 | 259 | 0 |
     | Jan 2021 | 504 | 500 | 45 |
     | Feb 2021 | 325 | 0 | 510 |

   * **Effect on the task:** the benchmark ranks models by how a refit does in the polluted season with a shifting
     site mix; a model that is better in the rainy months is not seen.
   * **Experiments:** February dominates the score (LightGBM 26.9 against 13.6 and 14.3).
   * **Other issues:** decide this issue first. Under A, the four October 2020 Nakawa spikes of issue 2 move into the
     October test window, so under issue 2 B the spike rule would drop no row; and the 92 outage hours of issue 3
     move into the November test window, where they are scored unless issue 3 A removes them as impossible values
     (as in qsar_tid_11).
   * **Consistency:** aeolus and perth_house_prices widened their windows; bias_correction_r_bias_correction_r_2
     kept "the whole last summer" without arguing the point.
   * **Panel:** the advocate and the critic dispute this point. A is the mediator's recommendation and C the
     critic's. The advocate's fact for B, "only the newest season has all three sites running", is false by the
     table above.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Five monthly windows from October 2020 | tests each month from October 2020 to February 2021 | the test covers both seasons; October and November score all three sites; the smallest train side is about 57%[^split14] | Nakawa has about 12 days (63 hours) of history before its first test month |
     | B | Three windows with an exception | keeps the three dry-season test months and records an exception with a true fact | a candidate fact: widening scores Nakawa with at most 12 days of history, a new-site test inside a known-site task[^use10] | the advocate's fact is false; whether 12 days is too little is a weighing call |
     | C | Six monthly windows from September 2020 | tests each month from September 2020 to February 2021 | none named | the September window scores Nakawa with no history at all, which conflicts with the known-site task[^use10] |
     | D | Three windows, no exception (implemented) | tests December 2020 to February 2021 (your "ok (a)" of 2026-11-04); `splits_comment` says the test covers the dry season only and names this issue | none named | no fact recorded for the dry-season-only test |

   * **Recommendation:** A. Decide from season and site coverage, not from the scores of the alternatives[^split21]
     (they do not change the ranking of model families anyway). **Decision:** A, B with which fact, or C?

   **Notes for the AI:** A is `n_windows=5`, monthly from October 2020; C is `n_windows=6`, from September 2020.

   [^split20]: **SPLIT-20** (Should; P4): the train side holds the history a model refit at each window would train
     on; widen the windows when the newest ones fall in an atypical season, or record the fact that sets the case
     apart.
   [^split14]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than
     50% of the data; it holds under A.
   [^use10]: **USE-10** (Must): decide from the use case whether the entity the model predicts for is new or known;
     here a known site.
   [^split21]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few
     test windows.

2. **Keep the Makerere spike in the February test window as a label?**

   * **Problem:**
     - Your spike rule of 2026-11-04 drops 5 reference hours, and one of them, Makerere 2021-02-17 20:00, sits in the
       February 2021 test window.
     - The rule was written while the split was random and was not checked again after the split moved.
     - A single extreme target may leave from the training period only, while in a test window a target leaves only
       when it is impossible[^clean11], and 249.1 µg/m³ is unusual but possible.
   * **Background:**
     - The rule: a reference hour above 3 times both low-cost PM2.5 channels and above 3 times the same site's
       reference in both neighbouring hours is set missing and its row leaves.
     - Four Nakawa hours of October 2020 are on the training side of every shipped window (in the October test window
       under issue 1 A); the Makerere hour has reference 249.1, channels 52.0 and 49.5, neighbouring hours 46.5 and
       43.7.
     - The rule is also uneven: four look-alike hours stay only because a neighbouring hour is missing from the file
       (two in the December and January test windows), and USEmbassy 2021-02-10 07:00 (459.0) misses the threshold
       by 0.55.
   * **Effect on the task:** dropping the Makerere hour removes a hard test hour chosen by its own label.
   * **Experiments:** keeping it moves February's RMSE from 26.57 to 27.50 (6.7% of that window's squared error).
   * **Consistency:** B follows mercedes_benz_greener_manufacturing (2026-10-21, a single extreme target dropped from
     the training side only); qsar_tid_11 (2026-10-21) dropped a test-side target only because it was impossible.
   * **Panel:** the advocate, the critic and the mediator agree on B.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the drop, with an exception | drops all 5 hours and records an exception that names the field's QC default | the notes now point to the spike (rate-of-change) screening of hourly reference-monitor feeds such as EPA's AirNow | no published QC document is quoted yet |
     | B | Spike rule outside the test windows | applies the rule only to rows outside every test window; the Makerere hour stays | agreed by the advocate, the critic and the mediator; follows mercedes_benz_greener_manufacturing | none named |
     | C | Drop all 5 hours (implemented) | the notes now say that one of them is in a test window | none named | drops a test target chosen by its own label, which is unusual but possible |

   * **Recommendation:** B. **Decision:** B, or A with its exception?

   **Notes for the AI:** under B, guard the count at 4 (at 0 under issue 1 A, which leaves the rule with nothing to
   drop).

   [^clean11]: **CLEAN-11** (Should; weak P4), training-period clause: a single extreme target leaves from the
     training period only; in a test window a target leaves only when it is impossible.

3. **Drop the 92-hour Nakawa reference outage?**

   * **Problem:**
     - From 2020-11-10 to 2020-11-23, 92 Nakawa hours have the reference below 0.3 times both low-cost PM2.5
       channels (2020-11-21 02:00: reference 0.1 against 101.2 and 102.0).
     - Collocated instruments sample the same air, so these labels are not readings the reference could have made,
       the same reasoning that drops the single high spikes[^clean].
     - All 92 hours are on the training side of every shipped window (1.1% of the smallest), but they shape the
       scored model.
   * **Background:** outside the run, Nakawa's monthly median ratio of reference to sensor is 0.97 to 1.21. Under
     issue 1 A the 92 hours sit in the November test window and are scored.
   * **Experiments:** without them Nakawa's December RMSE goes from 23.2 to 18.9; the mean over windows moves from
     17.96 to 18.15, mixed, so the score is not the argument.
   * **Consistency:** impossible values made missing follows churn_telco_south_asia and heart_disease; qsar_tid_11
     (2026-10-21) dropped an impossible target. The panel names no earlier multi-hour run of target values.
   * **Panel:** the advocate and the critic dispute the clause and the rank: the advocate cites the impossible-value
     clause and calls it a quality fix, the critic calls it validity because it changes the scored model. The
     mediator sides with the advocate on the clause and with the critic on the rank, and recommends A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the run | a rule bounded to the run's dates sets the reference missing where it is below 0.3 times both PM2.5 channels, and the rows leave | labels the reference could not have read leave the data; follows the precedents of impossible values | needs the date bound: without it the same test catches 96 hours |
     | B | Keep the run with the note (implemented) | the notes name it (dates, 92 hours, the 0.1 to 4 readings) | none named | the 92 labels shape the scored model |

   * **Recommendation:** A, the mediator's recommendation. **Decision:** A or B?

   **Notes for the AI:** under A, the rule gets a guard that raises unless the count is 92.

   [^clean]: **CLEAN-11** (Should), impossible-value clause: impossible values become missing; then **CLEAN-15**
     (Must): drop rows with a missing target. Target faithfulness, P5.

4. **One dead-channel rule for both sensors?**

   * **Problem:**
     - Your rule sets sensor 2 missing in the 500 hours where both its channels read exactly 0, but the same kind of
       failure remains in 34 hours[^dead].
     - A model reads these hours as clean air at one sensor, while AirQo's own pipeline discards hours where the two
       sensors disagree (domain practitioner).
     - The decision closes the open item of the record's 2026-11-04 assessment.
   * **Background:**
     - Sensor 1 is dead in 18 USEmbassy hours (2019-11-13/14 and 2020-06-07/08): it reads 1.0 to 5.4 while sensor 2
       reads 36 to 190 and the reference 22 to 70. Its ratio to sensor 2 is 0.022 to 0.255 there; the next ratio
       anywhere is 0.309.
     - Sensor 2 reads near zero in 16 more hours of its outage (2019-11-18 to 2019-12-14): 0.0014 to 1.37 in 15 of
       them, plus a 0.107-ratio hour on 2019-12-09 02:00. In 7 of the 15, `s2_pm2_5` equals `s2_pm10` exactly, which
       happens in none of the 10,417 other live hours. Outside the outage, sensor 2's ratio to sensor 1 has its 0.1%
       quantile at 0.618.
   * **Effect on the task:** all 34 hours fall in 2019 and June 2020, on the training side of every window under any
     option of issue 1, so the rule changes only the training data.
   * **Unknown:** no panel report measured its effect on the score.
   * **Panel:** the cutoff has to lie between 0.255 and 0.294: the 0.3 the advocate and the critic proposed also
     catches Makerere 2020-12-05 06:00 (ratio 0.294), a live hour in the December test window.
   * **Consistency:** B follows heart_disease, ashrae, rain_in_australia and protein_model_quality_rf_pcp
     (2026-11-04).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Joint-zero hours only (implemented) | sensor 2 is set missing in the 500 hours where both its channels read exactly 0 | none named | 34 hours of the same kind of failure stay as readings |
     | B | One symmetric rule at 0.27 | a sensor whose PM2.5 is below 0.27 times the other sensor's has both its channels set missing; the rows stay | covers both sensors; follows heart_disease, ashrae, rain_in_australia and protein_model_quality_rf_pcp | none named |

   * **Recommendation:** B, the rule at 0.27. **Decision:** adopt it (B), or keep the hours as readings (A)?

   **Notes for the AI:** under B, guards at 18 and 16 hours.

   [^dead]: **CLEAN-11** (Should; P7): impossible values become missing, and the row stays.

**Review panel:** ship after changes (mediator). Tier full, a second pass after Lennart's PR #33 review (2026-11-04), 12 reports. Claims: 24, 12 hold, 9 refuted (stale or overstated text, fixed in `dataset.py`; the record's `required_split` is in the field row and its 15-hour figures in issue 4), 1 concern (issue 2), 2 untested. Blind review: include with changes; its main concerns are that the eight site descriptors repeat the site label (kept: legitimate for known sites, LEAK-34) and that the windows mix later time with newer sites. Task gamer: its best exploit, the previous hour's reference, lowers mean RMSE from 18.21 to 16.28, a leak under the stated prediction point; nothing else beat the noise. Agreed: no leak, the temporal regime, the site descriptors kept, RMSE, the text fixes, the spike rule on training rows only, one dead-channel rule for both sensors. Disputed: SPLIT-20, widen the windows or keep them with an exception (issue 1); the clause and rank of the Nakawa outage (issue 3).

<details><summary>Mediator</summary>

**Mediator report: `airqo_low_cost_air_quality_monitor_calibration_challenge` (second pass, 2026-11-04)**

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-1/USE-3 triggered: the text describes a retrospective archive task while the split tests a forward
monthly refit; fixed by text, with "no reference value from the test month is known". USE-8 triggered: fit_reason
understates the network-transfer gap and presents the paper's future work as practice; fixed by text. LEAK-10 holds
(no column leak, no copies; the previous-hour reference exploit is ruled out once USE-3 is stated). SPLIT-1/4/11/13/14
hold. SPLIT-20 departed without a true fact: curator issue 1. CLEAN-11 training-period clause departed for one test row:
issue 2. Target faithfulness (tension P3/P5 over P7): 92-hour Nakawa reference outage in training labels: issue 3.
Value: TP-2 holds (LightGBM 18.2 vs training mean 41.2, raw sensor 25.3); MET-1..4 hold (source RMSE).
Quality: CLEAN-11 dead channels uncaught (sensor 1: 18 h; sensor 2: 16 h): issue 4. EV-7 stale text throughout: fix now.
Weighed: three sites -, real named use +, source paper +, shape +.
For the curator: issue 1 (widen the windows or record an exception with a true fact); issues 2-4 confirm data changes.
```

**Changes to make now (no decision needed)**

All of these are text. None changes rows, the split or the metric.

1. **USE-1, USE-3 (Must).** Rewrite the module docstring, `question`, `use_case`, `known` and the first `curation_comments` bullet to the forward reading the curator chose on 2026-11-04: "a model refit at the start of each month corrects that month's new hourly readings at the collocated devices; no reference value from the test month is known". Mark the 2026-10-27/28 retrospective approval as superseded.
2. **USE-8 (Must), SPLIT-12, EV-2.** In `fit_reason` and `splits_comment`, state seasonal retraining as the paper's recommendation, not as AirQo practice. Adong et al. lines 412-413: "It is also important to retrain these models periodically ... We shall consider seasonal re-calibration ... as part of our future work". State the monthly cadence as the curator's judgment. Name network transfer as the main gap under `approximate`: leave-one-site-out scores 26.18 for LightGBM against 21.11 for the raw sensor.
3. **EV-7, stale or wrong text.** Delete or correct:
   - "keep all its rows", "no ... row filter", and "all 10,932 rows" (10,927 ship);
   - "random CV follows ...", the nine-fold scores, 12.684, 14.13%, 15.3%, and "five of nine folds";
   - 77.68% (it is now 2 of 2,720);
   - "Retain these observations";
   - the `_decisions` line "All other rows and values are kept";
   - "five to six months of history" (Nakawa has 2.4 and 3.4 months, Makerere 4.5 to 6.5).

   Replace the old scores with the temporal ones (LightGBM 18.26, forest 19.21, linear 24.76, raw 25.32, mean 41.22). State in `splits_comment` that the test covers the dry season only. Also state the SPLIT-9/10 measurements: no label delay, and no gap is needed.
4. **Record.** Set `required_split` to Temporal. Add an Assessment line that corrects the 15-hour figures (0.0014 to 1.37, not 0.02 to 2.9; ratio elsewhere has a 0.1% quantile of 0.618 and a minimum of 0.107) and withdraws "all are settled".
5. **CLEAN-11.** Name the field's QC default (reference-monitor spike screening) as the basis for the four Nakawa spike drops on the training side.
6. **CLEAN-14.** Add a note to `landform_90m` that the ALOS classes are a partial order, kept unordered.
7. **Tooling (outside the definition).** The kit's `task.md` template prints "made when The prediction is made for ...".

**Issues for the curator, ranked**

**1. SPLIT-20 (P4, Should): all three test windows fall in the high-PM dry season, with no recorded exception.**
- **Effect.**
  - Monthly mean reference PM2.5 is 74.4 µg/m³ in Feb, 49.6 in Jan and 44.9 in Dec, against 35.9 to 43.1 in Sep to Nov 2020. February dominates the score (LightGBM 26.6 against 13.7 and 14.4).
  - Each test month scores a different site mix: Dec has no USEmbassy, Jan only 45 USEmbassy rows, Feb no Nakawa.
- **Advocate's best evidence.** Six windows would score Nakawa's 63 September hours with no Nakawa history, and the November window would hold the 92-hour outage.
- **Critic's best evidence.** The advocate's exception fact is false: "only the newest season has all three sites" does not hold. My count on the raw file:

  | Month | Makerere | Nakawa | USEmbassy |
  |---|---|---|---|
  | Oct 2020 | 383 | 543 | 390 |
  | Nov 2020 | 153 | 352 | 186 |
  | Dec 2020 | 578 | 259 | 0 |
  | Jan 2021 | 504 | 500 | 45 |
  | Feb 2021 | 325 | 0 | 510 |

  Only Oct and Nov have all three sites. "The next refit faces the newest season" is true of every temporal dataset, so it does not set this case apart.
- **Settled.**
  - The advocate's stated fact fails, so that exception cannot be recorded.
  - The critic's six windows bring in a cold start that conflicts with USE-10 (known sites).
  - Five monthly windows (Oct 2020 to Feb 2021) avoid the zero-history start (Nakawa has 63 hours, about 12 days, before October). The smallest train side is about 57%, so SPLIT-14 holds. They cover both seasons and all three sites.
  - If issue 3's rule is adopted, the outage hours leave under the impossible-value clause on either side of the split, as in qsar_tid_11.
- **Decision needed.**
  - (a) `n_windows=5`, the remedy ladder's "fix the definition";
  - (b) keep 3 windows with an exception that states a true fact. Candidate: "widening scores Nakawa with at most 12 days of history, a new-site test inside a known-site task (USE-10)". Whether 12 days is too little is a weighing call;
  - (c) `n_windows=6`.

  I recommend (a). Decide from coverage, not from scores (SPLIT-21). A consistency check applies: aeolus and perth_house_prices widened their windows; bias_correction never argued the point.

**2. CLEAN-11 training-period clause (Should; weak P4): the spike rule drops a test-window label.**
- **Effect.** Makerere 2021-02-17 20:00 (reference 249.1, channels 52.0 and 49.5) is in the Feb test window. Keeping it moves Feb RMSE from 26.57 to 27.50.
- **The rule is uneven.**
  - Four look-alike hours stay only because a neighbouring hour is missing, two of them in the Dec and Jan test windows.
  - USEmbassy 2021-02-10 07:00 (459.0) misses the threshold by 0.55.
- **Both sides now agree** on option (b): apply the rule to rows outside every test window and keep the Makerere hour as a label. This follows mercedes_benz. qsar_tid_11 dropped a test-side target only because it was impossible, and 249.1 µg/m³ is unusual but possible.
- **Decision needed.** Confirm (b). If you prefer (a), keep the drop and record an exception that names the field's QC default.

**3. Nakawa reference outage (P5 via the tension row "a cleaning gap that changes what the target means"; CLEAN-11 impossible-value clause, then CLEAN-15).**
- **Fact (confirmed).** 92 Nakawa hours from 2020-11-10 to 2020-11-23 have the reference below 0.3 × both PM2.5 channels. Example: 0.1 against 101.2 and 102.0. All 92 are on the training side of every shipped window.
- **The dispute is about which clause applies.**
  - The advocate is right on the clause. The training-period clause covers "a single extreme target" and does not fit a 92-hour run. A collocated reference reading 0.1 while both sensors read 101 is impossible.
  - The critic is right on rank. The run changes the scored model (Dec Nakawa RMSE 23.2 against 18.9 without it), so a silent keep is out. Line 119's "0.1 to 459.0" hides the run.
- **Detail for the rule.** The same 0.3 test with no date bound catches 96 hours (3 in Oct, 1 more in Nov), so bound it to the run's dates. Add a guard that raises if the count is not 92.
- **Decision needed.**
  - (a) the rule: set the target missing and drop the rows (recommended);
  - (b) keep the run, with a note naming the dates, the 92 hours and the ratio, and a rewritten line 119.

**4. Dead channels (P7; CLEAN-11 Should; closes the record's open item).**
- **Sensor 1.** 18 hours at USEmbassy (2019-11-13/14 and 2020-06-07/08). Its ratio to sensor 2 is 0.022 to 0.255 there; the next ratio elsewhere is 0.309.
- **Sensor 2.** 16 outage hours, not 15: the 0.107 hour at USEmbassy 2019-12-09 02:00 is inside the outage.
- **The proposed 0.3 cutoff is wrong.** It also catches Makerere 2020-12-05 06:00 (ratio 0.294, s2_pm10 37.0), a live hour in the Dec test window.
- **Recommendation.** Use one symmetric rule with a cutoff between 0.255 and 0.294 (for example 0.27): a sensor whose PM2.5 is below that fraction of the other sensor's has both channels set missing, and the rows stay. Guard the counts at 18 and 16. This follows heart_disease, ashrae, rain_in_australia and protein_model_quality_rf_pcp (2026-11-04).

**Task gamer's exploits**

| Exploit | Rule | Prior note | Status |
|---|---|---|---|
| #1 previous-hour reference, mean RMSE 18.21 to 16.28 (Feb −4.27) | USE-3, LEAK-10 | no `Potential leak, kept on purpose:` note; the comments only say lags are not added | New. It is a leak once `known` says no test-month reference is known (change 1). No data change. |
| #1b reference at t−1 and t+1 | LEAK-10 | none | New. A leak under any reading. Same fix. |
| #1c last reference within 24 h, −0.99 | USE-3 | none | New. Same fix. |

The test labels that #1 needs reach participants only through the panel kit's `data.parquet`. That is a kit matter. Every other attack scored at or worse than the baseline (18.21).

**Agreed facts**

All of these were confirmed on the raw file or the full text unless marked.

- 10,932 raw rows; 10,927 ship.
- Train sides 75.1% to 92.4%; test months 834 to 1,049 rows.
- First hours: Nakawa 2020-09-19, Makerere 2020-07-15, USEmbassy 2019-07-25.
- No leak and no copies. Weather is one city-wide series. The site descriptors recode `site`; they are legitimate for known sites (USE-10, LEAK-34).
- Random folds score about a third better because of neighbouring hours: 18.03 vs 18.26 once the test months are out of training.
- Leave-one-site-out: learned models lose to the raw sensor (26.18 vs 21.11), so a grouped split is not viable with three sites.
- RMSE is the source metric.
- Sensor 2 has 500 zero hours, now missing.
- Seasonal retraining is future work in the paper.
- The `_2` sibling's record says `No` (Duplicate). That comes from an unverified AI screening that still needs a CC line; it is not this dataset's issue.

**Consistency with precedent**

- The register flags nothing for this dataset.
- **Consistent:**
  - the temporal regime (bias_correction; differs from infrared_thermography by the hourly stream);
  - the sensor-2 zeros set missing;
  - `landform_90m` decoded (CLEAN-12 sweep);
  - `rmse` as the source metric (zillow_prize);
  - the four Nakawa spike drops (mercedes_benz), once the field default is named.
- **Departures, both sent to the curator:**
  - the Makerere test-row drop against mercedes_benz and qsar_tid_11 (issue 2);
  - SPLIT-20 against aeolus and perth_house_prices, with no true distinguishing fact recorded (issue 1).
- No third exception of the same kind.

</details>

<details><summary>Claim audit</summary>

Verdict: the data and the metric hold up. What fails is the text: it describes two different tasks, the split's justification overstates its source, and several notes and numbers are stale. Nothing I measured points to a leak.

**Focus question (P/focus.md: "none beyond the standard panel").** Answers to its items (a) to (g):
- **(a) Split:** the temporal split works mechanically, but its justification and its season coverage are the weakest part (R1 to R4).
- **(b) Spike rule:** it depends on whether the neighbouring hours happen to be in the file, and it drops a test-window row (R5).
- **(c) 15 extra outage hours:** they are real and sit only inside the outage. The record's numbers for them are wrong (R7).
- **(d) Site descriptors:** they do encode site, and that is legitimate for a task about known sites. Removing them costs LightGBM 3.6 to 4.4 RMSE.
- **(e) Stale comments:** confirmed (R6).
- **(f) Sibling `_challenge_2`:** not open. Its record already says `No` (`Duplicate`, PROV-4).
- **(g) Domain:** `zindi.africa` returns a 301 redirect to `zindi.world`, so it is the same page.

LightGBM was untuned, 300 trees, on the 3 shipped windows.

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| Metric: RMSE, from the source, original µg/m³ scale, no inputs | dataset.py `metric`; claims 1, 38 | Opened the Zindi page; scored a dummy prediction with `scorer` on each fold | holds | Page says "The evaluation metric for this challenge is the Root Mean Squared Error", with ID/Target submissions. Dummy RMSE 57.666 / 33.525 / 32.464 on n = 834 / 1,049 / 837 | MET-1, 2, 3, 4 |
| Retrospective archive correction that "does not validate later operation" | task_summary question, use_case, known; prediction-point bullet (claims 1, 2, 10) | Compared with the split text and fit_reason | **refuted** (contradiction) | The split "corrects that month's new readings", and fit_reason says "AirQo corrects new readings" | USE-1, SPLIT-1 |
| "AirQo corrects new readings with models retrained periodically, by season" | fit_reason; splits_comment (claims 8, 29) | Read Adong et al. 2022 (full text) | **refuted as a fact** | Lines 412-413: "It is also important to retrain these models periodically ... We shall consider seasonal re-calibration ... as part of our future work". The paper itself split randomly 80/20 (lines 193-194) | SPLIT-12, EV-2 |
| "Makerere and Nakawa test months have five to six months of history" | splits_comment (claim 31) | First labeled hour per site against each window | **refuted** | Nakawa starts 2020-09-19: 2.4 months of history (Dec), 3.4 (Jan). Makerere starts 2020-07-15: 4.5, 5.5 and 6.5 months | EV-7 |
| The windows cover "the newest season" | claims 6, 28 | Monthly target means and site mix | holds as written; **departs from SPLIT-20** | Feb-21 mean 74.2 against 35.9-49.6 for Sep-20 to Jan-21; Feb dummy 57.7 against about 33. Feb has no Nakawa, Dec no USEmbassy, Jan only 45 USEmbassy hours | SPLIT-20 (Should) |
| Spike rule catches 5 hours (values listed); Decision table: 444 against channels 35/36 and neighbours 47.5/86.0 | claims 15, 48; `_decisions` | Re-ran the rule; ratio conditions tested without the adjacency requirement | holds as computed; **uneven in effect** | 5 hours exact. But 9 hours meet the 3x tests against their nearest labeled neighbours, and 4 stay only because a neighbour hour is absent from the file: Nakawa 2020-10-29 17:00 (172.1), 2020-11-02 18:00 (232.1), 2021-01-01 22:00 (147.2, Jan test window); Makerere 2020-12-08 14:00 (82.9, Dec test window) | CLEAN-11, CLEAN-15 |
| Dropping spikes is a cleaning step | same | Where the dropped rows fall | **concern** | Makerere 2021-02-17 sits in the Feb **test** window. CLEAN-11 lets a single extreme target leave "in the training period only". Keeping it: Feb RMSE 26.57 becomes 27.50 (6.7% of squared error). The kept Jan look-alike carries 6.9% of Jan squared error | CLEAN-11 |
| "Keep all its rows"; "no ... row filter is applied"; "all 10,932 rows" | task_summary changes; comments (claims 7, 9, 12) | Count rows | **refuted** | 10,932 raw, 10,927 shipped | EV-7 |
| 77.68% of test rows have a same-site training hour within 1 h | comments (claim 25) | Recomputed on the shipped windows | **refuted (stale)** | 0.0%, 0.2%, 0.0% | EV-7 |
| "Random CV follows the source"; nine folds; 14.13%; "retain these observations" | comments (claims 20, 22, 23) | Compared with the definition | **refuted (stale)** | Split is temporal (3 windows) and both Nakawa hours are dropped | writing |
| 15 extra outage hours: sensor 2 at 0.02-2.9; ratio elsewhere at least 0.63 | record 2026-11-04 assessment (claim 47) | Computed | count holds, **values refuted** | 15 hours, all USEmbassy 2019-11-18 to 2019-12-14. s2 PM2.5 0.0014-1.37, PM10 0.0014-1.49. Ratio elsewhere: 0.1% quantile 0.618, minimum 0.107. No ratio below 0.1 outside the outage | CLEAN-11 |
| Sensor 2: 500 dead hours at USEmbassy, 2019-11-18 to 12-17, 13 runs of 11-117; sensor 1 never below 0.57; means 52 and 59 | claim 18 | Computed | holds | 500 hours; 13 runs of 11-117 rows (spanning 14-166 h). Minimum 0.567; means 52.2 and 59.3. No zeros elsewhere | CLEAN-11 |
| 6 humidity and 17 temp missing; labels 0.1-459 | claims 12, 17 | Computed | holds | Exact | – |
| 8 site descriptors constant per site; weather agrees across sites | claim 19 | nunique per site; equality at shared hours | holds (stronger than stated) | nunique is 1 for all 8. Weather is identical at 100% of the 930 / 531 / 445 shared hours, so it is one city-wide source, not a per-site measurement | LEAK, SPLIT-13 |
| No duplicate site-hour or predictor copy | claim 19 | Duplicates within the data and train-to-test copies per window | holds | 0, and 0/0/0 per window | LEAK-16..21 |
| Leak probes did not run (tz-aware timestamp) | claim 26; leak.txt | Single-feature LightGBM and missingness per window, run by hand on naive time | holds (no leak) | Best single features: pm10 and s2_pm10, skill 0.67 (the sensor itself). created_at alone −0.06. Test windows have no missingness except 2 humidity values | LEAK-1..15 |
| Random folds about a third better (14.05 vs 18.39) | claim 30 | Random 5-fold OOF scored on the same test rows | holds | 13.13 vs 18.77 | SPLIT-4 |
| Train sides 75-92%; windows Feb / Jan / Dec, each trained on every earlier hour | claims 28, 50 | Computed | holds | 8,207-10,093 of 10,927 (75.1-92.4%) | SPLIT-11, 14 |
| Task probe: LightGBM 18.2 against dummy 41.2 | prep | Per-window mean | holds | 26.57 / 13.69 / 14.36, mean 18.2 | TP-2 |
| Test.csv: 2,733 rows, about 20% per site, overlapping dates, no labels | claim 20 | Read the file | holds | Exactly 0.200 per site; 2019-07-25 to 2021-02-28; no ref column | – |
| Sibling decision open | prep, checklist | Read the sibling record | **refuted** | `suggestion: 'No'`, `Duplicate` (PROV-4) | PROV-4 |
| `required_split: Random (IID)` | record front matter (claim 51) | Compared with the definition | **refuted** (stale) | Definition is temporal | pipeline |
| 15.3% of squared error from two Nakawa hours "on the new folds"; 14.13% | claims 15, 22, 23 | – | untested | Those random folds no longer exist | EV-7 |
| Organizer's 16 May 2021 discussion reply; hourly aggregation; redistribution terms; mirror SHA-256 | claims 10, 21, 27, 47 | – | untested | Discussion page and mirror not opened | – |

**Refuted and untested, ranked**

1. **P3/P4, Must (USE-1, SPLIT-1): the README describes two tasks.** The question, use_case, known and prediction-point text say "historical/archived ... does not validate later operation". The split and fit_reason test forward monthly correction. Both readings have support:
   - The Zindi Test.csv is a random 20% per site and the paper splits randomly, which fits the retrospective reading.
   - The paper deploys the models "to a production system" on the network, which fits the forward reading.

   Lennart chose temporal on 2026-11-04. Mildest remedy: rewrite the question, use_case and prediction-point bullet for forward correction of new readings at known sites. Text only; no data change.
2. **P4, Should (SPLIT-12, EV-2): the refit cadence is overstated.** Periodic seasonal retraining is a recommendation and future work in Adong et al., not AirQo's documented practice. Remedy: quote it as a recommendation; the monthly horizon stays a curator judgment.
3. **P4, Should (SPLIT-20): all three test windows are in one high-pollution dry season,** and each window scores a different site mix. USEmbassy is effectively scored only in February. No exception is recorded. Remedy (choose from the use case, not from scores, SPLIT-21): either write an exception to SPLIT-20, or use five monthly windows Oct-20 to Feb-21. The five-window option keeps every train side at 57% or more (SPLIT-14 holds).
4. **P4/P7 (CLEAN-11, CLEAN-15): the spike rule is label-aware and drops one test-window target** (Makerere, Feb-21, 6.7% of that window's squared error). It also keeps four hours that differ from the dropped ones only because a neighbouring hour is missing (two of them in the Jan and Dec test windows). Remedy, mildest first:
   - (a) drop only training-period spikes and keep the Feb row, as CLEAN-11 provides;
   - (b) use the nearest labeled hour within about 3 h as the neighbour, so like cases are treated alike;
   - in either case, state the label-aware filter openly.
5. **P4 (EV-7): "five to six months of history" is wrong for Nakawa** (2.4 and 3.4 months). Remedy: correct the number.
6. **Procedure (EV-7, writing): stale text.** Items:
   - "keep all its rows" and "no row filter";
   - 10,932 rows (10,927 ship);
   - "random CV follows the source", nine folds, 77.68% (now 0%);
   - "Retain these observations" for the two Nakawa hours that are now dropped;
   - record `required_split: Random (IID)`;
   - the 2026-11-04 assessment says "all settled" while the 15-hour item is open.

   Remedy: delete or rewrite those bullets and set the record to Temporal.
7. **P7 (CLEAN-11): the 15-hour figures are wrong** (0.0014-1.37, not 0.02-2.9; ratio elsewhere 0.618, minimum 0.107). The evidence still supports extending the missing-value rule: the ratio is below 0.1 only inside the outage window. Remedy: correct the numbers, and extend the rule if the curator agrees.
8. **Untested:** the 15.3% and 14.13% shares (their folds are gone), the organizer's discussion reply, the mirror's provenance and the redistribution terms. Remedy: recompute the shares on the shipped windows or drop them.

Sources:
- [Zindi competition page](https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge) (redirected from zindi.africa)
- [Adong et al. 2022, full text (NRU repository)](https://nru.uncst.go.ug/bitstreams/45d40730-30e4-4119-a213-82b8a96eccf0/download)
- [Adong et al. 2022, repository record](https://nru.uncst.go.ug/handle/123456789/7263)

</details>

<details><summary>Column audit</summary>

**Column audit: `airqo_low_cost_air_quality_monitor_calibration_challenge` (second pass, 2026-11-04)**

**Answer to focus.md.** No column leaks. The main problem the panel missed is in the target: Nakawa's reference monitor failed from 2020-11-10 to 2020-11-23. For 92 hours it reads 0.1 to 4 µg/m³ while both collocated sensors read 10 to 120. The definition drops five high single-hour spikes by rule but keeps this low run, which is the same kind of reference artefact. Sensor 1 also has an uncaught dead-channel run, the mirror of the sensor-2 rule. Point by point:
- **(b) Spike rule:** it drops one test-window row by its label.
- **(c) The 15 sensor-2 hours:** they hold, and sensor 1 has 18 more of the same kind.
- **(d) Site descriptors:** legitimate.
- **(e) Stale notes:** confirmed, and the task_summary contradicts itself (see 4).
- **(g) Metric URL:** zindi.africa answers 301 to zindi.world, so it is the same page.
- **(a) and (f):** belong to the split and provenance reviewers. One column fact for (a): the Feb 2021 window has no Nakawa rows, and Dec 2020 has no USEmbassy rows.

**How I checked.** Codebook: Zindi's data page, fetched after the redirect. I found the definitions there, although the dtype probe reported "no codebook". The leak probe could not run, so I made a by-hand substitute. On the 3 shipped windows I fit untuned LightGBM with 3 seeds, turning `created_at` into hours, hour of day and day of year. Baseline RMSE per window is 26.63 / 12.86 / 14.39, mean 17.96.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `ref_pm2_5` (target) | PM2.5 from the reference monitor, µg/m³ | target | float. USEmbassy values are 100% integers; Makerere and Nakawa are about 90% one-decimal (a different instrument or feed). Nakawa outage: 92 h at ref/sensor-1 below 0.3, daily median ratio 0.014 to 0.14 against 0.97 to 1.2 in other months, ref as low as 0.1 while sensor 1 reads 101 | cleaning problem | CLEAN-11, CLEAN-15 |
| `created_at` | hourly timestamp of recording, UTC+3 | yes | tz-aware datetime, all minutes 0, all 24 hours present. The leak-probe crash is a tooling problem, not a data problem | fine | CLEAN-14 |
| `site` | collocation site (3) | yes | category. Also stands in for the reference instrument: median ref/sensor-1 ratio 1.07 to 1.44 at USEmbassy, 0.67 to 0.74 at Makerere | fine (known site) | USE-10, LEAK-34 |
| `pm2_5` | sensor 1 PM2.5, µg/m³ | yes | float. 18 hours with sensor 1 dead (USEmbassy 2019-11-13/14, 4 h; 2020-06-07/08, 14 h): sensor 1 reads 1.0 to 5.4 while sensor 2 reads 36 to 190 and the reference 22 to 70. Sensor-1/sensor-2 ratio is 0.022 to 0.26 in these hours, against at least 0.31 everywhere else | cleaning problem | CLEAN-11 |
| `pm10` | sensor 1 PM10, µg/m³ (codebook entry inferred from its siblings) | yes | float. The same 18 dead hours. PM10 is never below PM2.5 | cleaning problem | CLEAN-11 |
| `s2_pm2_5` | sensor 2 PM2.5, µg/m³ | yes | float. The 500 exact zeros are now missing (correct). 15 hours of the same outage remain at 0.0014 to 1.37, ratio to sensor 1 at most 0.048; the next ratio is 0.107 | cleaning problem (open in the record) | CLEAN-11 |
| `s2_pm10` | sensor 2 PM10, µg/m³ | yes | as for `s2_pm2_5` | cleaning problem | CLEAN-11 |
| `humidity` | "decimal proportion of full saturation", at most 1 | yes | float, range 0.31 to 1.0 (18 rows at exactly 1), 6 missing. Identical across sites at all 1,656 shared hours, so it is one city-wide ("prevailing") series, not a sensor on the device | fine | — |
| `temp` | "prevailing temperature", °C | yes | float, 16.2 to 30.8, 17 missing. City-wide like `humidity` | fine | — |
| `lat`, `long` | site coordinates | yes (static) | float, one value per site | fine; a 1:1 recoding of `site` | CLEAN-5 (weigh) |
| `altitude` | metres above sea level | yes (static) | int, 3 values | fine; recodes `site` | CLEAN-5 (weigh) |
| `greenness` | NDVI greenness index | yes (static; snapshot date unknown) | int 4374 to 6340, probably NDVI × 10⁴; scale kept | fine; recodes `site` | CLEAN-5 (weigh) |
| `landform_90m` | ALOS landform class ("11 peak ... 42") | yes (static) | category decoded into the ALOS words, 2 levels. Merges USEmbassy and Makerere. ALOS classes are a partial order (position × warm/cool), so unordered is right, but CLEAN-14 asks the notes to say so | fine, with a missing note | CLEAN-12, CLEAN-14 |
| `landform_270m` | ALOS mTPI (low = valley, high = ridge) | yes (static) | int (-11, 14, 28), continuous | fine; recodes `site` | CLEAN-14 |
| `population` | people per km² | yes (static; vintage unknown) | int, 3 values | fine; recodes `site` | CLEAN-5 (weigh) |
| `dist_major_road` | metres to the nearest road with continuous traffic | yes (static) | int, 3 values | fine; recodes `site` | CLEAN-5 (weigh) |
| `ID` (dropped) | opaque row key | — | dropped. Raw probe 20 gives it skill -0.08 alone | fine | CLEAN-3 |

**By-hand leak substitute.**
- Dropping any single column moves mean RMSE by at most +0.86 (`humidity`, to 18.82).
- Dropping the 3 time features costs +0.44; dropping the weather pair costs +1.59.
- No single column outscores the rest. Raw copies: 0 (raw probe 21).
- Dropping `site` and its 8 descriptors together costs +3.64 (to 21.60), while each alone costs at most 0.12. They are one block of site identity, which a known-site task may use (LEAK-34).
- No post-outcome column, no missingness caused by the outcome: the 500 sensor-2 gaps are all one USEmbassy span in Nov-Dec 2019, and the weather gaps are 23 cells.

**Problems, ranked by `principles.md`**

**1. The target holds a 92-hour reference outage (P5/P3 through P7; CLEAN-11 then CLEAN-15; Should, but it changes what the target means for those rows).**
- Nakawa, 2020-11-10 to 2020-11-23: ref is 0.1 to 4 µg/m³ while both channels read 10 to 120 (2020-11-21 02:00: ref 0.1 against 101.2 and 102.0). Outside this run, Nakawa's ref/sensor-1 ratio has its 0.5% quantile at 0.30; the other 4 months' medians are 0.97 to 1.21.
- All 92 rows are on every training side (1.1% of 8,207 at the smallest).
- The definition's own reasoning applies: the instruments share the air, so this cannot be a real reading. The spike rule removes high single hours but keeps this low run, and the comment "all labels observed and positive (0.1 to 459.0)" covers it up.
- Score is not the argument and comes out mixed: without the run, Dec RMSE goes 14.39 to 12.16 (Nakawa rows 23.2 to 18.9) and Jan goes 12.86 to 14.91; mean 17.96 to 18.15.
- **Mildest remedy:** a written rule. Nakawa reference below 0.3 × both sensor PM2.5 channels inside the run's dates is set missing and the rows leave. Training period only, so CLEAN-11's training clause holds too. Raise if the count changes, and note it next to the spike bullet. Alternative: keep the run with a note naming it. Either way the curator should decide, since the rule today treats high and low artefacts unequally.

**2. The spike rule drops one test-window row by its label (P4 against P7; CLEAN-11's training-period clause; weak selection on the test outcome, LEAK-22 area).**
- Makerere 2021-02-17 20:00 (ref 249.1) falls in the Feb 2021 test window.
- Put back, with a prediction of 43.4, it raises window-0 RMSE from 26.63 to 27.55 (+3.5%). One row in 834.
- CLEAN-11 lets a single extreme target leave in the training period only. Outside it, the row may leave only as an impossible value; the qsar_tid_11 precedent dropped one.
- The curator approved the 5 hours knowingly, so this is a **consistency check** to ask, not an override:
  - (a) keep the drop, and record as an exception the fact that sets it apart ("collocated instruments sample the same air, so an isolated 3x reference hour is impossible, not unusual");
  - (b) apply the rule to training rows only.

**3. Dead channels that the cleaning misses (P7; CLEAN-11, Should).**
- **Sensor 1:** 18 hours in two runs (USEmbassy 2019-11-13/14 and 2020-06-07/08). Both of its channels read 1 to 8 while sensor 2 and the reference read 36 to 190. This is the mirror of the decided sensor-2 rule, and nothing catches it.
- **Sensor 2:** the 15 near-zero hours already in the record (open).
- **Mildest remedy:** one symmetric rule. A sensor whose PM2.5 is below 0.3 × the other sensor's has both its channels set missing, and the rows stay. That catches 18 hours for sensor 1; for sensor 2 it gives the 15 plus one at 0.29 to check. The row-count guard is updated to match.

**4. Notes contradict the code and each other (procedure: writing.md; USE-3/USE-8 readability).**
- **`task_summary` against itself:** `use_case` says it "does not validate later operation", while `split` and `fit_reason` describe a monthly refit correcting new readings. One prediction point should be stated.
- **`changes`:** "keep all its rows" is wrong; 5 rows are dropped.
- **`curation_comments`:**
  - "no ... row filter is applied" is wrong.
  - "random CV follows the source-described retrospective sampling" is stale.
  - The nine-fold scores and 14.13% are pre-edit.
  - "Retain these observations" for the two Nakawa spikes is superseded by the spike rule.
  - The first bullet's prediction point is "retrospective", while the split is forward.
- **Record:** `required_split: Random (IID)` while the definition is temporal.
- **Codebook:** the Zindi data page has every column's meaning, but the dtype probe ran with "no codebook". Declare its URL so future probes match.

**5. Eight site-constant descriptors (P7; CLEAN-5/CLEAN-22, Weigh).** Seven are 1:1 recodings of `site`; `landform_90m` merges two sites. With 3 sites, all present in training, they add nothing over `site` (each alone at most ±0.12 RMSE). They carry real meaning and the source ships them, and dropping them gains nothing. **Remedy:** keep them; the existing note suffices. Add the CLEAN-14 partial-order note for `landform_90m`.

**6. Weather is city-wide (P3 note, no rule broken).** `temp` and `humidity` are identical at all three sites at every shared hour. The codebook calls them "prevailing", so they are not collocated measurements. One line in `fit_reason` would replace "timing of weather unverified" with the fact.

**Judgment record.**
```text
Verdict: ship after changes.
Validity: LEAK-10 holds (no post-outcome column, no outcome-driven missingness; by-hand drop-one max +0.86 RMSE); LEAK-34/USE-10 hold for site descriptors; target faithfulness: CLEAN-11 gap on the Nakawa reference outage (92 h, all training).
Value: TP not re-run (prep: skill +0.81).
Quality: CLEAN-11 sensor-1 dead channel (18 h) and sensor-2 near-zeros (15 h) uncaught; CLEAN-14 partial-order note missing for landform_90m.
For the curator: issue 2, a consistency check (a test-window row dropped by its label: exception or training-only); issue 1, which way to treat the low reference run.
```

</details>

<details><summary>Split audit</summary>

**Split verdict for `airqo_low_cost_air_quality_monitor_calibration_challenge`: right with notes.** The temporal regime is the correct one. The problems are in the text that surrounds the split, plus a choice to concentrate all three test windows in one season. The windows themselves are sound.

**The focus question** (`focus.md` (a): three monthly windows, newest season only, same-site recurrence). The temporal split holds up. It has three windows, each trained on every earlier hour, with train sides of 75.1%, 82.8% and 92.4% (8,207, 9,044 and 10,093 rows). Test sizes are 837, 1,049 and 834 rows. That meets SPLIT-11 and SPLIT-14.

Sites recurring across the cutoff is legitimate (USE-10, SPLIT-13). The entity is a known collocation site, and AirQo's alternative, transfer to a new site, cannot be tested on three sites. The weak part is the "newest season only" choice (problem 2 below).

**Numbers**
All runs are untuned LightGBM with 400 trees, plus a random forest, a linear model, the raw sensor-1 reading and the training mean.

RMSE by split (each cell is the mean, then per window or fold):

| Split | LightGBM | Random forest | Linear | Raw sensor 1 | Training mean |
|---|---|---|---|---|---|
| **A. Shipped**: Feb, Jan, Dec | 18.26 (26.9 / 13.6 / 14.3) | 19.21 | 24.76 | 25.32 | 41.22 |
| **B. Random 5-fold**, out-of-fold, scored on the same three test months | 12.94 (17.1 / 11.7 / 10.1) | – | 21.74 | – | – |
| **B2. Same test months**, trained on an equal-size random draw of all other hours, future included | 18.03 | – | – | – | – |
| **C. Leave one site out** (Makerere, Nakawa, USEmbassy) | 26.18 | 22.94 | 23.61 | **21.11** | 36.58 |
| **C2. As C, without the 9 site columns** | 26.8 (23.6 / 26.1 / 30.8) | – | – | – | – |
| **D. Six monthly windows**, Sep 2020 to Feb 2021 (train 52.5% to 92.4%) | 17.56 | 17.88 | 22.54 | 22.74 | – |
| **E. Three two-month windows**, Sep 2020 to Feb 2021 (train 52.5%, 68.8%, 82.8%) | 17.87 | 17.67 | 22.65 | 22.46 | – |
| **F. Shipped, without time features** | 26.5 / 13.9 / 14.8 | – | – | – | – |

How to read the alternatives:
- **Random folds (B, B2):** they score a third better, which confirms the direction of the `splits_comment` claim (its own figures were 14.05 against 18.39). B2 shows where the gain comes from. Once the test month's own hours are out of training, a random draw that includes future data scores the same as the shipped split (18.03 against 18.26). The random-fold advantage is the neighbouring hours inside the same month, not future data. So temporal beats random for the reason the comment gives.
- **Leave one site out (C, C2):** every learned model loses to the raw reading. Sites barely overlap in time (USEmbassy 2019-07 to 2020-06 alone; Makerere from 2020-07-15; Nakawa from 2020-09-19), so site is confounded with season. With three groups, a grouped split would be a domain-shift test. Grouped is not a viable alternative. This does confirm `fit="approximate"`: the network use (correcting devices that have no reference monitor) is not tested and would score much worse.
- **Six windows (D, E):** the model-family order is unchanged (LightGBM and the forest first, then linear and raw, then the mean), so the window choice does not flip a ranking.
- **Time features (F):** removing them changes little, so there is no time-as-number shortcut.
- **Adjacency:** under the shipped split, only 2 of 2,720 test rows have a same-site training hour within one hour. Under the old random folds it was 77.68%.

**Problems, ranked**

**1. The task text still describes the retired retrospective, random-CV task, which contradicts the split** (P3/P4; SPLIT-1, USE-1; stale evidence EV-7/EV-8). Must fix.
- `task_summary.question` says "historical low-cost monitor reading".
- `use_case` says "within the represented sites and historical conditions; it does not validate later operation". The split does exactly that: "a model refit before each month corrects that month's new readings".
- `changes` says "keep all its rows", but 5 rows are dropped.
- `curation_comments` contradicts the split and the cleaning in several places:
  - "no ... row filter is applied";
  - "random CV follows the source-described retrospective sampling";
  - "About 77.68 percent of test rows have a same-site training hour within one hour". It is now 2 of 2,720.
  - the nine-fold scores (13.237 and others), "covers five of nine folds" and "Retain these observations" for the two Nakawa hours, which the spike rule now drops;
  - "the 14.13 percent" figure.
- Record front matter: `required_split: Random (IID)` should be Temporal.

Mildest remedy: rewrite `question`, `use_case` and `changes`. Replace the nine-fold numbers with the temporal ones (LightGBM 18.26, forest 19.21, linear 24.76, raw 25.32, mean 41.22). Drop the 77.68% and "retain" lines. Set `required_split` to Temporal. The split itself needs no change.

**2. All three test windows fall in one season** (SPLIT-20 "check whether the newest windows fall in an atypical season and widen them so most do not"; SPLIT-15; both Should).
- Dec to Feb is Kampala's high-PM dry season. Feb 2021 has a mean of 74.2 and a p90 of 154.7, against 35.9 to 49.6 in the months before it.
- The Feb window dominates the score (LightGBM 26.9 against 13.6 and 14.3). Inside it, one row carries 14.2% of the squared error and the top five carry 22.1%.
- The only earlier dry season in training (Dec 2019 to Feb 2020) is USEmbassy only.
- The curator chose "newest season" deliberately (CC 2026-11-04, "ok (a)").

Mildest remedy: `n_windows=6` (monthly, Sep 2020 to Feb 2021). It meets SPLIT-14 (smallest train side 52.5%), covers the rainy and the dry season, has test sizes 462 to 1,312, and keeps the monthly refit cadence. Otherwise keep the three windows and say in `splits_comment` that the test covers the dry season only. Per SPLIT-21, this is argued from the season structure, not from the scores above.

**3. Factual errors in `splits_comment`** (EV-7; Should fix).
- "Makerere joined ... July 2020 and Nakawa in September 2020, so their test months have five to six months of history" is only true for Makerere.
  - Makerere has 4.5 to 6.5 months of history (1,700 training rows before Dec, 2,782 before Feb).
  - Nakawa (first hour 2020-09-19) has 2.4 to 3.4 months (954 rows before Dec, 1,213 before Jan).
  - Nakawa is absent from Feb. USEmbassy re-enters Feb (510 rows) after a gap: no Dec 2020 rows and 45 in Jan.
- I could not verify the quote "retrained periodically ... seasonal" (Adong et al. 2022). Wiley returned 403 and the NRU PDF could not be parsed here. Status: cannot verify. The paper's abstract says the models were applied to more than 120 network devices, with cross-unit and cross-site validation. That supports problem 5's note.

**4. The spike rule removes a test row using its label and its neighbours' labels** (P4; CLEAN-15 against an honest test; cross-reference for the cleaning auditor).
- The Makerere 2021-02-17 20:00 hour (reference 249.1, both PM2.5 channels about 50 to 52) is in the Feb test window.
- The shipped model predicts 42.9 for it. Keeping the row moves Feb's RMSE from 26.68 to 27.6.
- The effect is small and the rule is applied uniformly, so I am not asking for a change on split grounds. The notes should say one test hour is removed by a label-based rule.
- Mildest remedy: a one-line note. The alternative of dropping the rule on test rows only is a cleaning decision.

**5. The regime is a proxy for network use** (USE-10, SPLIT-4; note only).
- AirQo's deployed use is correcting devices at sites without a reference monitor (cross-site). The temporal split tests known sites at a later time.
- With three sites confounded with period, leave-one-site-out cannot stand in for that use. Every learned model scored below the raw sensor (26.18 against 21.11).
- Temporal at known sites is the closest testable regime. `fit_reason` already says "no network or new-device transfer". Keep it, and add the leave-one-site-out figure as evidence.

**Checks with no problem**
- **Gap and label delay** (SPLIT-9, SPLIT-10 as amended 2026-11-04):
  - No delay is documented for the hourly BAM references.
  - No training row has a label from after its window start; the same-hour target is known within the hour.
  - The end of the release shows no selection: the Feb mean has z +1.3, inside the band. The rows-per-day shift (z +3.5 pooled) comes from more sites running at once.
  - No gap is needed. The notes should state these measurements, as the amendment asks.
- **Training history** (SPLIT-20): it expands from 2019-07 and includes the Kampala COVID-19 lockdown (Apr to May 2020 means 34.5 and 36.7, USEmbassy only) and the dead sensor-2 outage. Both are in train only, and neither is a break that needs a cut. This could be mentioned in `splits_comment`.
- **Time column and windows:** `created_at` is the observation hour in UTC+3, and the windows cut at local month boundaries. About 20% of hours in each month are absent because the unlabeled Zindi Test.csv holds them. That is harmless.
- **Site descriptors:** the eight columns constant within a site encode site identity, which is legitimate for the known-site task (SPLIT-13).

Sources:
- [Adong et al. 2022, DOAJ entry](https://doaj.org/article/d2a40331a1ce4f41b84fb5895b60c115)
- [Uganda NRU repository record](https://nru.uncst.go.ug/handle/123456789/7263)

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: `airqo_low_cost_air_quality_monitor_calibration_challenge`**

I read this as an AirQo data engineer who runs the PM2.5 calibration microservice behind the AirQo API, dashboard and app.

**Focus question.** `focus.md` sets no special focus beyond the standard panel. Its item (g) has an answer: `zindi.africa/...` returns a 301 to `zindi.world/...`. The definition's `zindi.world` reference is therefore the current canonical URL, and the record's `zindi.africa` links still resolve. Nothing needs fixing there. On the use case, my answer is below.

**Fit: approximate.** The rows, inputs, hourly reference target and RMSE match how AirQo calibrates. But the test asks how the same three collocated devices do next month. AirQo's real decision is applying a collocation-trained model to more than 120 network devices that have no reference monitor. The "seasonal retraining" given as the reason for the monthly windows is the paper's future work, not AirQo's stated practice.

**What the actor does today.** This comes from Adong et al. 2022, sections 2.3–2.4 and 5, which I read in full.
- AirQo collocates a few devices with Met One BAM 1022 monitors. Each device has two Plantower PMS5003 sensors.
- It averages the device data to hourly values and fits a random forest. Inputs are hourly PM2.5 and PM10, temperature, humidity, and hour and month from the timestamp.
- Models are validated cross-unit (other devices at the same site) and cross-site (devices at another reference site). The paper concludes "AirQo devices do not have to be calibrated individually."
- In production, "Raw hourly PM concentrations ... are fed into the calibration model together with ... hourly temperature and humidity readings from the nearest meteorological station." This runs for every network device, in near real time.
- Retraining appears only as future work: "It is also important to retrain these models periodically ... We shall consider seasonal re-calibration ... as part of our future work."
- The Zindi page says the goal is to "roll out across the network", and asks winners how they would "apply their models to other devices on our network."

**1. Inputs at the prediction point**
- **I have these:** both sensors' PM2.5 and PM10, the hour, the site, and temperature and humidity. Humidity is identical across sites at all 125 shared hours, so it comes from one weather feed. That matches production, where values come from the nearest TAHMO station. The site descriptors (lat, long, altitude, greenness, landform, population, distance to road) are static GIS values I know in advance. None of these leaks.
- **I would always have these, but they are missing:**
  - The device ID. A site's device can be swapped, and device identity matters for cross-unit error.
  - PM1, which the PMS5003 also reports.
  - The sensor-agreement QC flag. AirQo discards hours where the two sensors disagree (R < 0.99). The 500 dead sensor-2 hours plus the 15 near-zero hours the rule misses (focus item c) would fail this check in my pipeline. Setting both channels missing is the right analogue. Leaving the 15 hours at 0.02–2.9 (under 10% of sensor 1, against a 0.63 floor everywhere else) is an inconsistency an expert would close.
- **Inputs I would not have:** none.

**2. Target.** This is the quantity I act on: same-hour BAM PM2.5 in µg/m³, a number, on its original scale. 60% of the labels are integers, consistent with BAM hourly output. Hourly BAM data is noisy, so dropping single-hour spikes is defensible (CLEAN-11, CLEAN-15). In the 5 dropped hours the reference is more than 3× both collocated sensors and more than 3× both neighbouring hours. Sensors a metre away would see a real plume. Multi-hour events stay, which matches the paper's view that spikes are real local events.

**3. Row, test and decision.** One row is one device-hour, which is my unit. The test data is not what I face in production:
- **Test windows are dominated by the newest sites.** USEmbassy has 0 test hours in December and 45 in January. Nakawa has 0 in February. Makerere and Nakawa supply 1,989 of 2,720 test hours.
- **The splits comment overstates the training history.** It says the test months "have five to six months of history." Before the December and January windows, Nakawa has 954 and 1,213 training hours (about 2.4 and 3.4 months since 19 Sept 2020). Makerere has 1,700–2,782 hours.
- **Forward in time is the right direction.** The calibrated value is produced forward, as new readings arrive.

**Gaps, ranked by how much they change the task**

1. **The test unit is a known device, but my decision is mainly a new site or device (USE-10, USE-8).** My leave-one-site-out diagnostic (sensors and weather only, LightGBM) gives:

   | Held-out site | Model RMSE | Raw sensor 1 RMSE |
   |---|---|---|
   | Makerere | 24.25 | 20.18 |
   | USEmbassy | 28.16 | 19.10 |
   | Nakawa | 22.53 | 24.05 |

   The flexible model is worse than raw sensor 1 at two of three held-out sites. So cross-site transfer is a different and harder task than the shipped one. With three sites, a grouped split is too thin to ship (three groups). The known-site temporal task is a defensible stand-in: it is how I would validate a refit before rolling it out. But `fit_reason` must name this gap as network transfer, not as "no network or new-device transfer" stated in passing. Fit stays approximate.

2. **The text contradicts itself after the 2026-11-04 split change (USE-1, USE-3).** Four places still describe the old retrospective archive setup:
   - `question`: "this historical low-cost monitor reading"
   - `use_case`: "corrects archived low-cost readings ... does not validate later operation"
   - the first `curation_comments` bullet: "retrospective correction of an already recorded cheap-monitor hour"
   - the README prediction point

   Against these, `split` and `fit_reason` describe a refit before each month that corrects new readings. The forward split simulates the real-time application, so the actor, moment and decision should be rewritten to that. The participant kit's `task.md` also prints a garbled prediction point ("made when The prediction is made for ..."), a templating bug.

3. **The source is overclaimed for the monthly windows.** `fit_reason` ("AirQo corrects new readings with models retrained periodically, by season") and `splits_comment` ("retrained periodically ... seasonal" (Adong et al. 2022)) cite a future-work sentence as current practice. The windows are still a reasonable choice: EPA guidance asks for collocation in two seasons and periodic recalibration. The wording should say "recommended" or "a plausible refit cadence," not "AirQo does."

4. **Stale numbers (focus item e).** `curation_comments` still states:
   - "keep all its rows" and "no ... row filter"; 5 rows are now dropped
   - 10,932 rows; it is now 10,927
   - "random CV follows the source-described retrospective sampling"
   - the 9-fold scores, 14.13%, 77.68% same-site within one hour, and five of nine folds
   - "Retain these observations" for the two Nakawa hours that are now dropped

   `changes` says "keep all its rows." The record front matter still says `required_split: Random (IID)`. An expert reading these would distrust the notes.

5. **The site descriptors encode site identity (focus item d).** That is legitimate for a known site (USE-10, "an entity seen before"). They add nothing until the network-transfer task exists, and they are harmless here.

6. **The test windows are uneven.** On my LightGBM, February scores 26.44, against 13.67 for January and 14.22 for December. February is 61% USEmbassy hours, with a mean reference of 88 µg/m³. A mean over windows is driven by one month at one site. This is the source's nature, not a defect, but it is worth a note.

**4. Would I use it, and what would make me trust it?** I would use a model chosen on this benchmark as the next refit for my collocated sites.

What would make me trust it:
- It beats the raw sensor by a wide margin. On the hourly windows: 13.7–26.4 for the model against 20.2–34.7 for raw sensor 1.
- On 24-hour means it beats a linear correction clearly: 5.96–19.65 against 13.71–28.87.
- It handles the dead-channel hours sensibly.

What would make me distrust it:
- I see no evidence it transfers to my 120 uncollocated devices.
- Tree models flatten spikes, which the paper also reports.
- On 24-hour means the model meets EPA's RMSE ≤ 7 µg/m³ target only in January (5.96), not in December (8.76) or February (19.65).

**5. Metric: yes.** RMSE on hourly µg/m³ is:
- the competition's leaderboard metric ("The evaluation metric for this challenge is the Root Mean Squared Error"; MET-4),
- the paper's first-named criterion,
- the error statistic in EPA's sensor performance targets (RMSE ≤ 7 µg/m³ or NRMSE ≤ 30%, applied to 24-hour data).

It scores a number at the unit I act on, the device-hour, on the original scale (MET-1, MET-3). There is no threshold decision, so MET-6, MET-7 and MET-9 do not apply. MET-8's regression fallback is also `rmse`. I would pick models by it and keep it.

As a secondary view, not a replacement, I would look at RMSE on 24-hour means per site. That is what EPA targets and the WHO and Uganda daily standards use, and it would reduce how much February at USEmbassy dominates. MET-2 holds: no scoring columns are needed, and the target and scale are unchanged from the source.

**What a domain expert would change**
- Rewrite `question`, `use_case`, the prediction-point bullet and the README to "a monthly refit corrects the next month's new hourly readings at the collocated devices" (USE-1, USE-3).
- Name network transfer to uncollocated devices as the main gap in `fit_reason` (USE-8). Cite seasonal retraining as the paper's recommendation, not as practice.
- Correct "five to six months of history." Nakawa has 954 and 1,213 training hours before its December and January windows.
- Purge the stale numbers and retrospective-CV wording. Set the record's `required_split` to temporal.
- Extend the dead-channel rule to the 15 low-ratio outage hours, mirroring AirQo's sensor-agreement QC (CLEAN-11).
- Optionally add a diagnostic note on leave-one-site-out performance (above) so users know the task does not certify transfer.

**Sources**
- [Zindi competition page](https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge) (and the 301 redirect from zindi.africa)
- [Adong et al. 2022, Applied AI Letters, doi:10.1002/ail2.76](https://onlinelibrary.wiley.com/doi/full/10.1002/ail2.76), full text via the [UNCST repository](https://nru.uncst.go.ug/bitstreams/45d40730-30e4-4119-a213-82b8a96eccf0/download)
- [DOAJ record of the paper](https://doaj.org/article/d2a40331a1ce4f41b84fb5895b60c115)
- [EPA performance targets (Duvall et al., recap)](https://asic.aqrc.ucdavis.edu/sites/g/files/dgvnsk3466/files/inline-files/Rachelle%20Duvall%20-%20Highlights%20on%20U.S.%20EPA%20Efforts%20on%20Developing%20Performance%20Testing%20Protocols%20and%20Targets%20for%20Air%20Sensors.pdf)
- [EPA reference-choice presentation (Barkjohn)](https://epa.gov/system/files/documents/2022-10/Presentation_NAAMC_ChoiceofReference_Karoline%20Barkjohn_508pdf.pdf)
- [EPA FASM base test report example (New York City)](https://click.clarity.io/hubfs/Marketing%20Assets%20-%20PDFs/Collocation%20Results%20library/New%20York%20City%20NY%20-%20EPA%20FASM%20Base%20Testing%20Report.pdf)

</details>

<details><summary>Blind reviewer</summary>

**Verdict:** include with changes. This is a real, honestly split calibration task from Zindi data with useful signal (about 20 to 25% lower RMSE than the raw sensor), but it has only three sites, so 8 of the 16 features are just the site label repeated, and the time split is mixed up with which site is being measured.

**Task and use.** AirQo collocated low-cost monitors (two PM sensors plus T/RH) with reference monitors at three Kampala sites: US Embassy, Makerere and Nakawa. The goal is to map the cheap readings to reference PM2.5. Zindi states the aim as "develop a model that will take low cost device data and other supplementary data and transform it as accurately as possible to the reference value", scored by RMSE. The linked paper (Adong et al. 2022, Applied AI Letters, ail2.76) reports that calibration models like this were rolled out to AirQo's network of more than 120 monitors. So the use is real: correcting each hourly cheap reading as it arrives. Every feature (sensor readings, weather, site metadata) is available at prediction time, so I see no target leakage. There are no duplicate rows, no duplicate (site, hour) pairs and no feature-identical rows. The table is Zindi's Train.csv only (10,927 rows, the labelled part), which is the right choice.

**Concerns, most to least serious**

1. **Only three sites, so the eight "geospatial" columns are the site ID copied eight times.**
   - Evidence: `lat`, `long`, `altitude`, `greenness`, `landform_90m`, `landform_270m`, `population` and `dist_major_road` each have exactly 3 unique values, one per site. The source says they are "constant for each location … in de-normalised format for ease of use".
   - Effect: they add nothing beyond `site`, yet they make the task look like it has spatial covariates. Methods that use feature count or feature priors (linear models, NNs, TabPFN-style models) see 9 collinear copies of one 3-level variable.
   - The deployment the paper describes (calibrating devices at new locations) cannot be tested with 3 sites, so this task only measures calibration at the same site over time.
   - Change: drop the 8 constant columns and keep `site`, or keep them but document that they are a site key. State that this is same-site calibration, not transfer to new sites.

2. **Which site is measured depends on time, so the temporal windows mix "later in time" with "new site".**
   - Evidence: US Embassy is the only site from 2019-07 to 2020-06. Makerere starts 2020-07-15 and Nakawa starts 2020-09-19, and US Embassy is almost absent in Dec 2020 and Jan 2021 (0 and 45 rows).
   - I rebuilt three end-of-series windows of about 1,640 rows each (my reconstruction; the exact boundaries are not in task.md):
     - window 0 (2020-09-25 to 11-04) is 37% Nakawa, with only about 63 Nakawa rows before it;
     - window 1 has just 118 US Embassy rows.
   - Effect: scores partly measure cold-start calibration on a nearly unseen site, and the site mix changes from window to window.
   - This is defensible, because a newly installed device has little history, but it should be documented. Check the real split boundaries and consider starting the first test window after Nakawa has, say, a month of history.

3. **The reference series differ between sites.**
   - Evidence: `ref_pm2_5` is a whole number in 100% of US Embassy rows but in only about 10% of Makerere and Nakawa rows.
   - This suggests a different reference instrument or reporting pipeline (the embassy monitor is likely an AirNow BAM). The source does not say this.
   - The sensor-to-reference relationship also differs by site. A linear fit of ref on `pm2_5` gives slope/intercept of 0.76/-2.4 at Makerere, 0.95/7.1 at Nakawa and 0.87/15.5 at US Embassy, with R² of 0.81, 0.58 and 0.80.
   - Effect: `site` partly stands for the reference device. That is acceptable for this task, but worth noting in the metadata.

4. **Signal and difficulty are fine, but the data are small and noisy.**
   - Results on my three windows (RMSE):

     | Method | Window 0 | Window 1 | Window 2 |
     |---|---|---|---|
     | Predict the training mean | 29.6 | 33.6 | 47.6 |
     | Raw `pm2_5` used as the prediction | 16.7 | 21.8 | 28.9 |
     | Linear model on `pm2_5` | 17.3 | 22.4 | 29.1 |
     | LightGBM, all features | 13.3 | 17.5 | 21.6 |
     | LightGBM, sensor columns + T/RH only | 16.1 | 20.4 | 23.8 |

   - The site key is worth roughly 10 to 15% of RMSE.
   - The task is not trivial and has room to separate methods. With about 1,600 test rows per window and heavy tails (ref max 459, ratio ref/`pm2_5` ranging from 0.001 to 50), RMSE will be driven by a few pollution spikes, so expect high variance between methods.
   - Keep RMSE as the source metric, but consider also reporting MAE or a log-scale metric.

5. **Data-quality details, all minor.**
   - `s2_pm2_5` and `s2_pm10` are missing in 4.6% of rows (500 rows, all at US Embassy). Leave them as NaN.
   - `temp` and `humidity` are missing in under 0.2% of rows. They are identical across sites at the same hour (I confirmed the cross-site standard deviation is 0). The source says "the same value will be found at the same time across each of the locations", so they come from one city weather feed, not the device. That is fine, but they are not on-board sensor readings.
   - There are a few clear sensor faults: 15 rows with `s2_pm2_5` < 1, 55 rows where the two sensors differ by more than 50%, and 23 rows with ref < 1. These are plausible real faults and should be kept.
   - `created_at` is tz-aware UTC+3, which is correct. It should be used only for splitting, or turned into hour/day features.
   - `landform_90m` is a category with only 2 levels across the 3 sites.

**Could not check**
- The exact split boundaries used by the pipeline (task.md gives only "3 test windows").
- The paper's full text (Wiley returned 403), so I could not confirm the reference instruments per site or whether the paper's data match this table.
- Whether Zindi's original Test.csv was a time-based or random split.
- Whether any device was replaced or recalibrated during the period.

Sources:
- [Zindi data page](https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data)
- [Zindi competition page](https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge)
- [Adong et al. 2022 (DOAJ)](https://doaj.org/article/d2a40331a1ce4f41b84fb5895b60c115)
- [Makerere repository record](https://nru.uncst.go.ug/handle/123456789/7263)

</details>

<details><summary>Task gamer</summary>

**Verdict:** this task is hard to game. The only real gain comes from giving the model the previous hour's reference value at the same site, which lowers mean RMSE from 18.21 to 16.28 (about 11%). Nearly all of that gain is on one split. Whether it counts as a leak depends on how the prediction point is read. Nothing else beat the noise.

The honest baseline is untuned LightGBM (100 trees, learning rate 0.1) on `features()`, with `created_at` converted to hours and categories coded. RMSE per split, r0/r1/r2: 26.41 / 13.72 / 14.49, mean 18.21. Adding a random column moves the mean by +0.04 to +0.30 and r0 by up to +0.84. Changing the bagging seed moves the mean by ±0.15.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Previous-hour reference at the same site, plus its ratio to that hour's sensor reading | 18.21 (26.41/13.72/14.49) | 16.28 (22.14/12.88/13.82) | -4.27 / -0.83 / -0.67 | Unclear: see below | State the prediction point exactly, or move to a rolling one-hour-ahead split |
| 1b | Reference one hour before and one hour after (interpolation) | 18.21 | 16.38 (22.34/13.74/13.06) | -4.07 / +0.03 / -1.44 | No: hour t+1 is not known yet | Don't ship test labels to participants (they sit in `data.parquet`) |
| 1c | Last known reference within 24 h, and its age | 18.21 | 17.22 | -1.75 / -0.24 / -0.97 | Same question as #1 | Same as #1 |

**#1, reference lags.** `task.md` says the model "may be trained on all earlier hours with reference values". A model deployed at a collocated site would then know hour t-1's reference when it predicts hour t. The shipped splits instead hide a whole month of references.
- The reference is noisy, so the lag carries little information. Correlation with the previous hour is 0.84, about the same as with the sensor (0.83). Using the previous hour's value directly as the prediction (persistence) scores worse than the baseline on r1 and r2: 21.6 and 20.2.
- The gain is large only on r0 (-4.3). On r1 and r2 it is -0.7 to -0.8, which is about the size of the random-column spread.
- Using it requires test-window labels, which are present in `data.parquet`.
- The deciding fact is whether the deployed calibrator receives the live reference feed. If it calibrates sites that have no reference monitor (the stated purpose of calibration), the lag is a leak. If it gets the feed, the split under-serves honest models by about 1.9 RMSE.
- Mildest fix: change the `task.md` wording to "references up to the start of the test window". The alternative is a rolling one-step-ahead split.

**Flaws that hurt an honest model.** None found. No honest training choice beat the baseline:
- Training on only the last 3, 6, 9 or 12 months: 19.33, 18.85, 19.07, 18.54.
- Dropping USEmbassy rows from before 2020-07: 19.00.
- Huber loss: 18.35. Stronger regularisation: 18.66.
- Per-site linear calibration: 20.33. Pooled linear calibration: 24.76.

The splits are clean. Training ends 2021-01-31 22:00 and the r0 test window starts 2021-02-01 00:00, so no training row falls at or after a test window. One fragility: in r0, a single USEmbassy test row (reference 459, sensor 153, previous hour 99) produces about 14% of the squared error. Without it, r0's baseline RMSE would be about 24.5. This is noise in the test labels, not something a model can exploit.

**Attacks that found nothing** (mean RMSE; baseline 18.21):
- **Past sensor lags** (1, 2, 3, 6, 24 h, plus a 6-hour past rolling mean): 18.90. Honest, and slightly worse.
- **Future sensor readings** (t+1 to t+6 and a centred rolling mean): 18.88. No gain over past lags, and not deployable.
- **Same-hour sensor readings at the other sites:** 19.66. Honest; no gain.
- **Same-hour reference at the other sites:** 18.63. Not deployable; no gain.
- **Statistics over the test window** (site-month and site-day means of the sensors): 18.89.
- **Row presence** (whether hour t±1 exists, rows per day; a row exists only when the reference exists): 19.22.
- **Missing second-sensor flag:** 18.21, unchanged. The reference mean is 59.3 when the second sensor is missing and 52.6 otherwise, but the trees already get this from the NaN.
- **Formats.**
  - Decimal counts, missing flags, and implied averaging denominators of the sensor, humidity and temperature values, fitted together with `site`: 33.95, against 40.41 for `site` alone. Added to the baseline: 18.22, so no extra information beyond the values.
  - Within-site correlation between the target and the averaging denominators: |r| ≤ 0.03.
  - USEmbassy references are 100% whole numbers; Makerere and Nakawa are mostly one decimal (about 10% whole). `site` is already a feature, so this gives nothing. Rounding USEmbassy predictions to whole numbers: 18.91 against 18.90 (no gain).
- **Copies across the split:** only 6 to 8 test sensor values per split also appear in training. These are coincidences: temporal split, no ids.
- **Order:** rows are sorted by time, with no id column. Next-row label agreement is just the time lag covered in #1.
- **Shared weather:** temperature and humidity are shared across sites (1,655 of 1,656 hours with several sites have identical humidity). This would let you rebuild the hour, but it adds nothing beyond `created_at`.
- **Transforms over all rows:** none present. The site descriptors are constant per site and the sensor readings are raw.

**Could not check:**
- The Zindi data pages require a login, so I could not compare the kit with the published Train.csv. The kit's 10,927 labelled rows appear to be the competition's public training file. Looking labels up there would work, but that is not a task flaw.
- The Zindi forum gives a best single-model RMSE of 9.29 on the competition's hidden test set, a different split. I found no leak threads and no winning write-ups.
- I could not tell whether missing reference hours are missing at random or depend on pollution level. The row-presence features show no signal.

Sources:
- [Zindi data page](https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/data)
- [Zindi discussion 6393](https://zindi.world/competitions/airqo-low-cost-air-quality-monitor-calibration-challenge/discussions/6393)
- [AirQo calibration paper (Applied AI Letters)](https://doaj.org/article/d2a40331a1ce4f41b84fb5895b60c115)

</details>

<details><summary>Precedent checker</summary>

**Precedent check: airqo_low_cost_air_quality_monitor_calibration_challenge (2026-11-04 decisions)**

The register (`register.json`) raises no flag for this dataset. Of its 19 flags, none touch CLEAN-11, CLEAN-12, CLEAN-15 or this record, so everything below comes from reading the cases.

**Answer to focus.md**
focus.md asks nothing beyond the standard panel. Its seven points, from the precedent side:
- **(a) Split:** consistent with precedent (item 2).
- **(b) Spike rule:** one real departure. One of the five dropped rows is in a test window (item 1).
- **(c) The 15 extra sensor-2 hours:** still open. Treating like cases alike points to extending the rule (item 3).
- **(d) Site descriptors:** consistent with SPLIT-13 and bias_correction's 25 recurring stations.
- **(e) Stale text:** a lot of it, including text that contradicts the new split and the spike drop (item 5).
- **(f) The `_2` duplicate:** consistent with PROV-4, but only an AI screening has decided it.
- **(g) Domain:** zindi.world against zindi.africa breaks no rule. The working copy is split 5/7 between them.

**1. Departs without a stated reason: the spike rule drops a test-window row (CLEAN-11 training-period clause)**
- **Rules:** CLEAN-11 (Should) lets "a single extreme target in the training period only" leave, with the source's words or the field's default. CLEAN-15 (Must) then drops any row whose target is missing.
- **Where the five dropped hours fall** (raw Train.csv):
  - The four Nakawa hours (2020-10-03, 10-05, 10-17, 10-30) are on the training side of all three windows.
  - Makerere 2021-02-17 20:00 (reference 249.1; the two channels read 52.0 and 49.5; neighbours 46.5 and 43.7) is inside the **February 2021 test window**.
- **Precedents:**
  - mercedes_benz_greener_manufacturing (2026-10-21, Lennart): one extreme target dropped only because it sat in the first 1,000 cars that every window trains on. The four Nakawa hours follow it. The record still has to name the field default (QC spike tests on hourly reference monitors are standard practice, but neither the record nor the definition cites them).
  - qsar_tid_11 (2026-10-21, Lennart): "the training-period clause does not apply to a random split". There the row left only because the value was impossible (about 1.7 million mol/L).
  - A 249.1 µg/m³ hour is unusual but physically possible. CLEAN-11 says "Values that are only unusual stay". The record's own 2026-10-27 assessment says "corruption is not proved".
- **Order of decisions:** the spike rule came in round 5, under the random split. The temporal split came in round 6. Nobody looked at the spike rule again after the split moved, so the test-row case has no recorded reason.
- **Sensitivity:** USEmbassy 2021-02-10 07:00 (459.0 against channels of 153.2 and 161.7, also in the February test window) is kept. It misses the rule by 0.55 µg/m³ (3 × 153.18 = 459.55) and has no 08:00 neighbour. The rule is applied mechanically, so this is consistent, not a departure. Still, the threshold separates two hours in the same test month that look alike.
- **Verdict:** Nakawa ×4 departs with a stated reason (the artefact signature is evident in the data), and the field default should be added. Makerere ×1 departs without one. It breaks no higher Must: it is one row of 835 in that window, and P4 is only weakly affected.

```text
**Consistency check (AI, 2026-11-04):** your spike rule drops Makerere 2021-02-17 20:00, which now sits in the
February 2021 test window; CLEAN-11 lets a single extreme target leave only from the training period (mercedes_benz,
2026-10-21), and qsar_tid_11 (2026-10-21) dropped a test-side target only because it was impossible. What sets this
hour apart?
(a) a single-hour reference reading 3x both collocated channels and both neighbours is an instrument artefact that
    air-quality QC removes by default (name the QC source), recorded as an exception to CLEAN-11's training-period
    clause; (b) treat it like mercedes_benz: drop only the four training-side Nakawa hours and keep the Makerere hour
    as a label; (c) reopen qsar_tid_11 / mercedes_benz to match; (d) amend CLEAN-11 so that a stated, mechanical
    artefact rule on the target's own series may drop rows on either side of the split.
```

**2. Consistent: temporal split, three monthly windows over Dec 2020 to Feb 2021, expanding train side**
- **Follows bias_correction_r_bias_correction_r_2** (AI assessments 2026-10-07 and 2026-10-15; shipped temporal: 9×7 days, gap 1): the same kind of task (correcting a measurement against a reference at recurring stations on a dense time axis), with windows that cover the newest season. The PR #33 review draft names it as the precedent.
- **Differs from infrared_thermography_temperature** (IID kept, CC 2026-10-21, Lennart, SPLIT-31) for evident reasons:
  - that dataset has one reading per subject, with "a function that is independent of time";
  - here the same devices produce an hourly stream, 77.68% of random-fold test hours have a training hour within one hour, and the source names periodic seasonal retraining (Adong et al. 2022, as quoted; I could not extract the PDF text to check the quote).
- **Not drift.** It replaces Myunghwan's 2026-10-28 ship decision, but the two decisions come from different curators, and the newer curator decision wins (principles.md, "Who decides").
- **Rules met:**
  - SPLIT-1, SPLIT-4: the use-case reason carries the decision.
  - SPLIT-11: expanding train side.
  - SPLIT-12: horizon set by the refit cadence.
  - SPLIT-14: 3 windows, train sides 75-92%.
  - No gap is consistent: bias_correction's one-day gap exists because its label completes after the prediction. Here the reference is for the same hour (SPLIT-10, amended 2026-11-04).
- **Minor points:**
  - SPLIT-15: the IID version had 3×3 = 9 folds, now 3 windows. The departure has a stated reason (monthly refit), and aeolus_rebuilt_1m and alfa_battle_2_0_task_2 also ship 3.
  - SPLIT-20 asks whether the newest windows fall in an atypical season. All three are the dry season (reference means 44.9, 49.6 and 74.4 for Dec, Jan, Feb). bias_correction did the same with "the whole last summer", so this is consistent, but neither record says whether that season is typical.
  - Site coverage per window is uneven: February has no Nakawa, December no USEmbassy, January only 45 USEmbassy hours.
  - SPLIT-4/SPLIT-21: `splits_comment` cites the score gap ("scored a third better", 14.05 against 18.39) as context. Keep it worded as a measurement, not as the reason for the choice.

**3. Consistent (sensor-2 zeros set missing); the 15 open hours are like cases not yet treated alike**
- **CLEAN-11, impossible value to missing, row kept.** This follows:
  - heart_disease (`chol == 0` set missing);
  - ashrae and rain_in_australia (cloud cover 9 set missing, Lennart's marks of 2026-10-31);
  - protein_model_quality_rf_pcp (ED/PN zeros set missing with the rows kept, CC 2026-11-04, Lennart: the same curator on the same day).
- **The 15 open hours** are all at USEmbassy inside the outage (2019-11-18 to 2019-12-14), with sensor 2 at 0.001-1.37 µg/m³. A second dead-channel signature: `s2_pm2_5 == s2_pm10` exactly in **7 of the 15 hours and in 0 of the 10,417 other live hours** (sensor 1 never shows this). If the 500 zero hours are set missing and these 15 are left as readings, two kinds of hour from the same outage, and of the same kind, are decided differently.
- The 2026-11-04 assessment says "all are settled", which conflicts with "extending the rule to them is open".

**4. Consistent**
- **`landform_90m` decoded into the ALOS words** (CLEAN-12, amended 2026-11-01): follows the sweep of 377 columns in 29 definitions on 2026-11-01. `landform_270m` stays numeric because it is continuous mTPI. Consistent.
- **Metric `rmse` from the source** (MET-4): the competition's own metric, like zillow_prize's `mae`. Consistent.
- **`_2` as `No` / `Duplicate`** (PROV-4): consistent. PROV-8 does not change it, since both are Zindi. Its verdict is an unverified AI screening from 2026-10-22 with no CC line, so a curator confirmation is still missing.

**5. Stale text that contradicts the 2026-11-04 decisions (not departures, but the definition misstates them)**
In `dataset.py`:
- **`task_summary.use_case`:** "historical conditions; it does not validate later operation". This contradicts the forward refit in `split` and `fit_reason`. The use case moved from Myunghwan's retrospective reading (CC 2026-10-27) to AirQo's correction of new readings. The text has to follow, or SPLIT-1 no longer matches P3.
- **`task_summary.changes`:** "keep all its rows". It does not mention the spike drop or the landform decoding.
- **`curation_comments`:**
  - "no target transformation, clipping, weighting or row filter is applied";
  - "random CV follows the source-described retrospective sampling";
  - "Retain these observations ... rather than delete difficult outcomes";
  - the nine-fold scores (35.568 down to 13.237), the 12.684 random-fold LightGBM, the 14.13% and 15.3% shares, "77.68 percent", "five of nine folds".
- **`_decisions`, sensor-2 entry:** "All other rows and values are kept".

In the record front matter:
- `required_split: Random (IID)` (now temporal).
- `claimed_by: Myunghwan`.

**Summary**
| Decision (2026-11-04, Lennart) | Result | Precedents |
|---|---|---|
| Sensor-2 zeros set missing | consistent | heart_disease; ashrae/rain_in_australia 2026-10-31; protein_model_quality_rf_pcp 2026-11-04 |
| 15 extra outage hours | open; consistency favours extending | same outage, PM2.5 = PM10 in 7/15 against 0/10,417 elsewhere |
| Spike rule, 4 Nakawa hours | departs with a reason (name the field default) | mercedes_benz 2026-10-21 |
| Spike rule, Makerere 2021-02-17 (test window) | **departs without a reason** (prompt above) | qsar_tid_11 2026-10-21, mercedes_benz 2026-10-21 |
| `landform_90m` decoded | consistent | CLEAN-12 sweep 2026-11-01 |
| Temporal 3×1 month | consistent; SPLIT-15 departure with a reason | bias_correction_r_bias_correction_r_2; distinguished from infrared_thermography_temperature 2026-10-21 |
| Metric `rmse` | consistent | MET-4, zillow_prize |

No drift, and no third exception of the same kind: CLEAN-11's training-period clause has no recorded exception yet.

</details>

<details><summary>Advocate</summary>

**Opening brief (advocate): ship `airqo_low_cost_air_quality_monitor_calibration_challenge` after text fixes. The data, split, target and metric stay as defined.**

**1. Honest evaluation holds: no leak (P4; LEAK-10 and LEAK-16..21, Must).**
- **Evidence.** Four agents looked for a leak independently and found none.
  - Claim auditor: the best single features are the sensor's own `pm10` and `s2_pm10` (skill 0.67). `created_at` alone scores −0.06. There are no row copies, either within the data or from train to test (0/0/0 per window).
  - Column auditor: dropping any one column moves mean RMSE by at most +0.86. No column depends on the outcome.
  - Split auditor: 2 of 2,720 test rows have a same-site training hour within 1 h.
  - Task gamer: only the previous-hour reference helps (18.21 to 16.28). The definition says it does not add that ("Reference values from other hours are not added as predictors").
- **Why it outranks the gamer's objection.** The deployed use is calibrating devices that have no reference monitor, so a deployed model would not have the lag. The gamer's fix is to reword the kit's `task.md` ("references up to the start of the test window"). That is a kit change, not a dataset change.

**2. The split regime is the right one, and it is the curator's newest decision (P4; SPLIT-1, SPLIT-4, SPLIT-11, SPLIT-13, SPLIT-14 Must; USE-10 Must).**
- **Evidence.**
  - Temporal is correct for an hourly stream at known devices. Split B2 shows where the random-fold gain comes from: with the test month's own hours out of training, a random draw that includes future data scores 18.03, against 18.26 shipped. The gain is neighbouring hours, not real signal.
  - Grouped is not viable. There are three sites, so three groups, and each held-out site loses to the raw sensor (26.18 against 21.11).
  - The "temporal against grouped" row of the Tensions table says to ship one regime, the one the use case implies.
  - SPLIT-14 is met: train sides are 75.1%, 82.8% and 92.4%.
  - Precedent: bias_correction_r_bias_correction_r_2 (measurement correction at recurring stations, temporal over the newest season).
  - Lennart's CC of 2026-11-04 is newer than Myunghwan's of 2026-10-28, so it wins ("Who decides").
- **Site descriptors (blind reviewer's first concern).** All agents agree they encode site identity. That is legitimate for known sites (USE-10, SPLIT-13, LEAK-34). Removing them along with `site` costs +3.64 RMSE. Under the coad precedent (CLEAN-22, Weigh), width is no reason to drop features. Keep them; the existing note says they are a site key.

**3. Worth benchmarking, with the source's metric (P6; TP-2, MET-4).**
- **Signal.** LightGBM scores 18.2, against 41.2 for the training mean, 25.3 for the raw sensor and 24.8 for a linear model (split auditor). That is a clear gap with room to separate methods.
- **Robust to the window choice.** The model-family order is the same under 6 monthly or 3 two-month windows (D, E), so the window choice does not change the ranking.
- **Metric.** RMSE is Zindi's leaderboard metric ("The evaluation metric for this challenge is the Root Mean Squared Error"), and the domain practitioner would select models by it (MET-1..4 hold).
- **Use case.** It is real (P3): AirQo, Adong et al. 2022, and the Zindi page's rollout to the network. Fit `approximate` is honest. The practitioner confirms the known-site temporal test is "how I would validate a refit before rolling it out."

**4. Conceded: the task text contradicts the split (P3; USE-1 Must; EV-7).**
- **Problem.**
  - `question`, `use_case`, the first `curation_comments` bullet and the README describe retrospective correction of archived readings, while `split` and `fit_reason` describe forward correction.
  - The notes are stale in many places:
    - "keep all its rows" and "no ... row filter";
    - 10,932 rows (10,927 ship);
    - the nine-fold scores, 14.13% and 15.3%;
    - 77.68% (now 0%);
    - "Retain these observations" for the Nakawa hours that are now dropped;
    - the record's `required_split: Random (IID)`.
  - Nakawa's history before its test months is 2.4 to 3.4 months, not "five to six".
  - "AirQo ... retrained periodically, by season" is the paper's future work (lines 412-413), not its stated practice.
- **Fix that keeps the dataset (definition text only, no data change).** Rewrite the four task-text places for a monthly refit that corrects the next month's new readings at the collocated devices. Delete or replace the stale numbers with the temporal ones. Correct Nakawa's months. Word seasonal retraining as the paper's recommendation. Set the record to Temporal. Under SPLIT-12 the horizon is a human judgment and the refit cadence is a valid basis, so the monthly windows stand as the curator's judgment.
- **Why this does not sink the dataset.** It is a Must, and it is fixed in the definition (principles: "fixed in the definition when it can be"). The data and the split already match the forward reading, so only the words change.

**5. All three test windows in the dry season (SPLIT-20, Should): keep, with a written exception.**
- **Evidence.** The test months are Dec to Feb, in the dry season; Feb's mean is 74.2. Lennart chose the newest season knowingly ("ok (a)"). bias_correction shipped "the whole last summer" the same way.
- **Rule.**
  - SPLIT-21 (Must) forbids choosing windows by comparing scores. No score argument against the current windows is valid; D/E show only that the ranking does not move.
  - SPLIT-20 is a Should, so a departure needs a fact and a principle. The fact: the use is the next refit at today's network, which faces the newest season, and only the newest season has all three sites running (P3).
- **Mildest remedy.** Write that exception into `splits_comment`, and add that the test covers the dry season only. If the curator prefers, `n_windows=6` (smallest train side 52.5%, SPLIT-14 still met) is a cheap alternative that keeps the dataset either way.

**6. The spike rule drops one test-window row (CLEAN-11 training-period clause, Should; P7, with a weak P4 touch).**
- **Conceded.** Makerere 2021-02-17 20:00 (249.1) is in the Feb test window. CLEAN-11 lets a single extreme target leave "in the training period only", and no exception is recorded for it.
- **Size.** One row of 835. Feb RMSE goes 26.57 to 27.50; the mean over windows moves by about 0.3.
- **Mildest remedy.** Option (b) in the precedent checker's prompt: apply the rule to training rows only and keep the Makerere hour as a label. This matches mercedes_benz (2026-10-21), keeps the four Nakawa drops (all on the training side), and removes the test-side asymmetry. The "nearest labeled neighbour" variant would drop more test rows by their labels, so I argue against it. Also name the field's QC default for the training-side drops, as CLEAN-11 asks.

**7. Uncaught dead channels and the Nakawa reference outage (P7; CLEAN-11, Should).**
- **Conceded as facts.**
  - Sensor 2 has 15 more hours of the same outage (0.0014-1.37; PM2.5 equals PM10 in 7 of them, against 0 of 10,417 hours elsewhere).
  - Sensor 1 has 18 dead hours.
  - Nakawa's reference reads 0.1-4 in 92 hours from 2020-11-10 to 11-23.
- **Why these do not block shipping.**
  - Tension "real task against imperfect cleaning": keep the task and fix what is cheap and safe.
  - All 92 outage rows are on the training side of every window and none in a test window. The test target's meaning is unchanged, so P3/P5 are not triggered for what is scored.
  - The effect on mean RMSE is mixed and small (17.96 to 18.15).
- **Mildest remedy.**
  - One symmetric dead-channel rule: a sensor below 0.3 × the other has both its channels set missing, and the rows stay. This is cheap and safe, and consistent with the 2026-11-04 sensor-2 decision and protein_model_quality_rf_pcp. Update the row-count guard.
  - The Nakawa run is a curator call: either a training-only rule or keeping it with a note naming it. Either way the dataset ships.
- Correct the record's 15-hour figures. Also fix the 2026-11-04 assessment: it says "all settled" while the 15 hours are open.

**Judgment record**
```text
Verdict: ship after changes (text rewrite; spike rule to training rows; symmetric dead-channel rule).
Validity: USE-1 triggered, fixed by text (forward refit); LEAK-10 holds (no leak, four agents); SPLIT-1/4/11/14 hold; USE-10/SPLIT-13 hold (known sites); P5 SHA-256 matches mirror and Zindi byte count.
Value: TP-2 holds (18.2 against dummy 41.2, raw 25.3); MET-4 holds (source RMSE).
Quality: CLEAN-11 training-period clause, fix by restricting the spike rule to training rows; CLEAN-11 dead channels, symmetric rule; Nakawa outage (92 h, training only) rule or note.
Weighed: three sites -, real named use +, source paper +, shape +.
For the curator: SPLIT-20 exception or n_windows=6; Nakawa outage: rule or note.
```

</details>

<details><summary>Critic</summary>

**Opening brief (against shipping as defined): airqo_low_cost_air_quality_monitor_calibration_challenge**

I do not ask for exclusion. The use case is real, nothing leaks, the metric holds, and the data has signal: LightGBM scores 18.2 RMSE against 41.2 for the training mean and 25.3 for the raw sensor. My position is that it should not ship as now defined. The definition describes two different tasks. It cites the source for a practice the source does not report. Its cleaning treats like cases unlike, and in one case it removes a test row by its label. Each point below can be fixed in the definition or with a note.

Files read: `dataset.py`, the record and `principles.md` in the repository; the README is generated from `dataset.py`. I also re-ran two of the panel's counts on the raw `Train.csv` (points 5 and 6).

**1. The task text describes two tasks, and the prediction point is ambiguous (P3; USE-1 and USE-3, Must).**
- **Problem.** Some fields still describe the retired retrospective task:
  - `question`: "this historical low-cost monitor reading".
  - `use_case`: "corrects archived low-cost readings ... does not validate later operation".
  - `known`, and the first `curation_comments` bullet: "retrospective correction of an already recorded cheap-monitor hour".
  - Against these, `split` and `fit_reason` describe "a model refit before each month corrects that month's new readings".
- **Effect.** The ambiguity is not only wording. If the actor corrects in real time at a collocated site, the previous hour's reference is known at prediction time. The task gamer measured that lagged reference at 18.21 → 16.28 mean RMSE (-4.27 on February). Under the shipped split, that same feature is a leak. USE-3 must settle which one it is.
- **Evidence.** All four reports that read the text found this (claim auditor R1, split auditor 1, domain practitioner gap 2, precedent checker 5). On the source side: the Zindi Test.csv is a random 20% per site, and Adong et al. split 80/20 at random, which supports the retrospective reading. But the paper puts the models into production on the network, and Lennart chose the forward reading on 2026-11-04.
- **Remedy (text only).**
  - Rewrite `question`, `use_case`, `known` and the prediction-point bullet as: "a model refit at the start of each month corrects that month's new hourly readings at the collocated devices; no reference value from the test month is known".
  - Fix the `task.md` template, which prints "made when The prediction is made for ...".

**2. The split's reason overstates the source, and the fit hides its main gap (P3; USE-8 Must; SPLIT-12 Should; EV-7 Must).**
- **Problem.** `fit_reason` says "AirQo corrects new readings with models retrained periodically, by season". `splits_comment` quotes "retrained periodically ... seasonal" as AirQo's practice.
- **Evidence.**
  - In Adong et al. (full text, lines 412-413) this is future work: "It is also important to retrain these models periodically ... We shall consider seasonal re-calibration ... as part of our future work."
  - AirQo's actual decision is applying a collocation-trained model to more than 120 devices with no reference monitor. Under leave-one-site-out, every learned model loses to the raw sensor (26.18 against 21.11, split auditor). The domain practitioner found the same at two of three held-out sites. So the shipped task does not certify the network use, and `fit_reason` names this only in passing.
- **Remedy.**
  - Word seasonal retraining as the paper's recommendation, and the monthly cadence as a curator judgment (SPLIT-12 asks that the reasoning be written down, not invented).
  - Name network transfer as the main gap under `fit="approximate"`, with the leave-one-site-out figure.

**3. All three test windows fall in one atypical season, with no exception recorded (P4; SPLIT-20, Should).**
- **Problem.** December 2020 to February 2021 is Kampala's high-PM2.5 dry season.
  - February's mean is 74.2 µg/m³ against 35.9 to 49.6 in September 2020 to January 2021, and February dominates the score (26.9 against 13.6 and 14.3).
  - The site mix changes from window to window: February has no Nakawa, December no USEmbassy, January only 45 USEmbassy hours.
  - SPLIT-20 says to "check whether the newest windows fall in an atypical season and widen them so most do not". Neither a widening nor an exception is recorded. "Ok (a)" chose the window, but it does not state the fact that sets this case apart.
- **Remedy (argued from the season structure, not from scores, per SPLIT-21).** Either:
  - set `n_windows=6`, monthly from September 2020 to February 2021. The smallest train side is then 52.5%, so SPLIT-14 holds; test months have 462 to 1,312 rows; the monthly cadence stays.
  - or record an exception to SPLIT-20 with its fact, and say in `splits_comment` that the test covers the dry season only.

**4. The spike rule drops a test-window row by its label (P4, weak; CLEAN-11 training-period clause, Should; consistency check under principles §"Consistent judgement" case 2).**
- **Problem.** The rule drops Makerere 2021-02-17 20:00 (reference 249.1, channels 52.0 and 49.5), which sits in the February test window.
  - CLEAN-11 lets "a single extreme target in the training period only" leave.
  - Two precedents differ: qsar_tid_11 (2026-10-21) dropped a test-side target only because it was impossible, and mercedes_benz dropped only on the training side. A reading of 249.1 µg/m³ is unusual but possible.
  - The rule was written in round 5, under the random split, and was not re-checked after the split moved.
  - It is also uneven: four hours meet the 3x tests and stay only because a neighbouring hour is missing from the file, two of them in the December and January test windows. USEmbassy 2021-02-10 07:00 (459.0, in the February window) misses the rule by 0.55.
- **Effect.** Keeping the row moves February RMSE from 26.57 to 27.50 (6.7% of that window's squared error).
- **Remedy.** Apply the drop to training-period rows only and keep the February row. Otherwise record an exception naming the reference-monitor QC default the field uses (no source is cited today). In either case, state openly that the filter uses the label.

**5. A two-week reference outage stays in the target (P5, target faithfulness; per the tension table, "a cleaning gap that changes what the target means is a validity question"; CLEAN-11).**
- **Problem.** Nakawa's reference reads near zero from 2020-11-10 to 2020-11-23 while both collocated sensors read normal air.
- **Evidence.** I re-ran this:
  - 93 Nakawa hours in November 2020 have reference below 0.3 × both PM2.5 channels.
  - In the 116 Nakawa hours of 10-23 November, the median reference is 2.95 against a sensor median of 35.1, and 72 hours read below 4.
  - Example: 2020-11-21 02:00 has reference 0.1 against 101.2 and 102.0.
  - Elsewhere, Nakawa's monthly median ratio of reference to sensor is 0.97 to 1.21.
- **The inconsistency.** The definition drops a single high reference hour as "an artefact of the reference monitor" because the instruments share the air. That same reasoning applies to a 92-hour low run, which it keeps. Comment line 119 ("All labels are observed and positive (0.1 to 459.0)") hides the run.
- **Remedy.** Add a written rule: in the Nakawa run, a reference below 0.3 × both channels is set missing and the row leaves. All these rows are in the training period, so CLEAN-11's training-period clause holds. Add a count guard as for the spikes. Alternatively, keep the run with a named note. Either way, the curator decides, since high and low artefacts are now treated differently.

**6. The dead-channel rule misses like cases (P7; CLEAN-11, Should; treat like cases alike).**
- **Problem.** Two groups of dead-channel hours are not caught:
  - Sensor 2: 15 more hours of the same USEmbassy outage read 0.0014 to 1.37. The record's "0.02-2.9" and "at least 0.63" are wrong; the true values are 0.0014-1.37, and the ratio elsewhere has a 0.1% quantile of 0.618 and a minimum of 0.107. In 7 of these 15 hours `s2_pm2_5 == s2_pm10` exactly, against 0 of the 10,417 other live hours (precedent checker).
  - Sensor 1: dead in 18 hours (USEmbassy 2019-11-13/14 and 2020-06-07/08). Sensor 1 reads 1 to 5 while sensor 2 and the reference read 36 to 190.
- **Evidence.** I re-ran both counts: sensor 1 below 0.3 × sensor 2 gives 18 hours; sensor 2 below 0.1 × sensor 1 gives 15 (17 below 0.3).
- **Remedy.** One symmetric rule: a sensor whose PM2.5 is below 0.3 × the other sensor's has both its channels set missing, and the row stays. Update the row-count guard to match. This is a quality fix, not grounds to exclude.

**7. The notes and the record contradict the definition (EV-7, Must; writing.md).**
- **Stale or wrong statements:**
  - "keep all its rows" and "no ... row filter is applied": 5 rows are dropped.
  - "all 10,932 rows": 10,927 ship.
  - "random CV follows the source-described retrospective sampling".
  - The nine-fold scores, the 14.13% and 15.3% shares, "five of nine folds", and "77.68 percent of test rows have a same-site training hour within one hour": that share is now 2 of 2,720.
  - "Retain these observations", about two Nakawa hours the spike rule now drops.
  - The `_decisions` line "All other rows and values are kept".
  - "Five to six months of history": Nakawa has 2.4 and 3.4 months before its December and January windows.
- **Record:**
  - `required_split: Random (IID)` should be Temporal.
  - The 2026-11-04 assessment says "all are settled" while also saying the 15-hour extension "is open".
- **Remedy.** Delete or rewrite these lines, and recompute or drop the shares. In the record, set `required_split` to Temporal and correct the 15-hour figures.

```text
Verdict: ship after changes.
Validity: USE-1/USE-3 triggered (two tasks, prediction point ambiguous), fix text; USE-8 fit understated and source overclaimed, fix text; SPLIT-20 departure without exception, widen to 6 windows or record exception; CLEAN-11 training-period clause departed for one test row, restrict or record exception; target faithfulness: Nakawa reference outage (93 h, training only), rule or note.
Value: TP-2 holds (18.2 vs 41.2 dummy, 25.3 raw sensor).
Quality: CLEAN-11 dead channels (18 h sensor 1, 15 h sensor 2) uncaught; EV-7 stale notes and record.
For the curator: point 3 (widen or exception), point 4 (training-only or exception), point 5 (rule or note).
```

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (advocate): `airqo_low_cost_air_quality_monitor_calibration_challenge`**

The critic and I now agree on the verdict: ship after changes, with the data, target, metric and regime kept. I concede most of the points below. I dispute one part of the critic's point 3 remedy and the rule the critic cites for point 5. Both disputes rest on numbers already in the panel reports.

**1. Two tasks, prediction point unclear (USE-1, USE-3, Must): conceded.**
- What follows: rewrite `question`, `use_case`, `known` (`dataset.py` line 62) and the prediction-point bullet in the critic's words: "a model refit at the start of each month corrects that month's new hourly readings at the collocated devices; no reference value from the test month is known".
- That sentence also settles the task gamer's lag question under USE-3/LEAK-1. The previous-hour reference (18.21 to 16.28) is a leak, not a feature an honest model is denied. Two reasons:
  - The deployed calibrator serves devices with no reference monitor (Adong et al.; the Zindi page's "roll out across the network").
  - The split is already built this way. Training ends 2021-01-31 22:00 and the February window starts 2021-02-01 00:00.
- The garbled `task.md` template ("made when The prediction is made for ...") is a kit bug. It is conceded and changes no data.
- The fix stays at the level of text. The split already matches the forward reading, and that reading is Lennart's decision of 2026-11-04, which is the newest ("Who decides").

**2. The source is overclaimed and the fit hides its main gap (USE-8 Must, SPLIT-12, EV-7): conceded.**
- Adong et al. lines 412-413 present seasonal retraining as future work. What follows:
  - Word it as the paper's recommendation.
  - Call the monthly cadence a curator judgment. SPLIT-12 accepts that as long as it is written down.
  - In `fit_reason`, name network transfer as the main gap, with the leave-one-site-out figures: every learned model scores 26.18 against 21.11 for the raw sensor (split auditor), and the practitioner found the model worse than raw at 2 of 3 held-out sites.
- This does not lower the fit below `approximate`. The practitioner calls the known-site temporal test "how I would validate a refit before rolling it out". With three sites, a grouped split cannot be shipped (SPLIT-14), so this remains the closest regime that can be tested.

**3. SPLIT-20, all test windows in the dry season (Should): exception conceded; I dispute the `n_windows=6` option and withdraw it as my own alternative.**
- Conceded: "ok (a)" chose the windows but does not state the fact that sets this case apart. The exception has to be written into `splits_comment`, and it should say that the test covers the dry season only.
- Disputed: six monthly windows (September 2020 to February 2021) is not the milder remedy. The panel's own numbers show it creates two new problems:
  - **Nakawa would start cold.** Its first hour is 2020-09-19 (claim auditor, split auditor). A September test window would score Nakawa hours with no Nakawa history at all, and October would have about 12 days of it. That brings back the cold-start mix the blind reviewer flagged as a weakness (its window 0 was 37% Nakawa with about 63 prior rows). That would be a new-site test inside a known-site task, which goes against USE-10.
  - **The reference outage would move into scoring.** All 92 outage hours (2020-11-10 to 11-23) would fall inside a November test window. The test would then either score a broken reference instrument (P5) or drop about 92 test rows by their labels, which is the same test-side asymmetry the critic objects to in point 4, at roughly 90 times the size.
- Under SPLIT-21 neither side may argue from the score differences (D: 17.56 against 18.26). The ranking does not change under D or E. With three windows, every scored site has at least 2.4 months of history and no scored hour falls in the outage. That is the fact for the exception, together with this: only the newest season has all three sites running, and the use is the next refit on the current network (P3).
- Remedy: write the exception, and keep the three windows.

**4. The spike rule drops a test-window row (CLEAN-11 training-period clause, Should): conceded.**
- What follows: apply the rule to training rows only and keep Makerere 2021-02-17 20:00 as a label. This is option (b) in the precedent checker's prompt and matches mercedes_benz (2026-10-21).
- Also conceded:
  - Name the field's QC default for the four Nakawa drops; CLEAN-11 asks for "the source's words or ... experts of the field".
  - State openly that the filter uses the label.
- I still argue against the nearest-labeled-neighbour variant. It would remove more rows by their labels and fixes nothing that rule (b) leaves open. Under (b), the two test-window look-alikes stay as they should, and USEmbassy 2021-02-10 07:00 (459.0) stays either way.
- Cost: February goes from 26.57 to 27.50, one row in 835.

**5. Nakawa reference outage (CLEAN-11; the critic cites P5): the remedy is conceded and I now prefer the rule; the rule the critic gives for it is wrong.**
- Conceded:
  - The run is a reference artefact. 2020-11-21 02:00 reads 0.1 against 101.2 and 102.0, and outside the run Nakawa's monthly median ratios are 0.97 to 1.21.
  - The comment "All labels are observed and positive (0.1 to 459.0)" (line 120) hides it.
  - Dropping a single high hour while keeping 92 low hours treats like cases unlike.
- Disputed basis:
  - The training-period clause covers "a single extreme target". It does not fit a 92-hour run.
  - The right clause is CLEAN-11's first sentence: "Impossible values become missing". Two collocated channels a metre apart reading 100 while the reference reads 0.1 is not air the reference could have sampled. CLEAN-15 then removes the rows.
  - Practically the result is the same, but the rule should cite the correct clause.
- Disputed rank: this is not a validity issue for what gets scored. All 92 rows are on the training side of all three windows (1.1% of the smallest training side), so the test target's meaning is unchanged. Under the tension row "real task against imperfect cleaning", this is the "fix what is cheap and safe" case.
- Remedy:
  - A written rule: Nakawa reference below 0.3 × both PM2.5 channels inside the run's dates becomes missing, the rows leave, and a count guard is added.
  - I now prefer the rule to a bare note, because it gives high and low artefacts one logic.
  - The effect is mixed and small (17.96 to 18.15), so no score argues either way.

**6. Uncaught dead channels (CLEAN-11, Should): conceded.**
- Remedy, as in my opening: one symmetric rule. A sensor whose PM2.5 is below 0.3 × the other sensor's has both its channels set missing, and the rows stay. It catches 18 hours for sensor 1 and 15 for sensor 2.
- The one sensor-2 hour at ratio 0.29 needs a look before the threshold is fixed.
- The rule matches the 2026-11-04 sensor-2 decision, protein_model_quality_rf_pcp, and AirQo's own sensor-agreement QC (practitioner). Update the row-count guard.

**7. Stale notes and record (EV-7, Must): conceded in full.**
- What follows: remove or rewrite:
  - "keep all its rows" and "no ... row filter";
  - 10,932 (10,927 ship);
  - "random CV follows the source";
  - the nine-fold scores, 14.13%, 15.3%, 77.68% (now 2 of 2,720) and "five of nine folds";
  - "Retain these observations";
  - the `_decisions` line "All other rows and values are kept";
  - "five to six months" (Nakawa has 2.4 and 3.4).
- In the record:
  - set `required_split` to Temporal;
  - correct the 15-hour figures (0.0014 to 1.37; elsewhere the 0.1% quantile is 0.618 and the minimum 0.107);
  - fix the "all settled" contradiction.
- Replace the old scores with the temporal ones: LightGBM 18.26, forest 19.21, linear 24.76, raw 25.32, mean 41.22.

**Net position.** No point in either brief touches the leak checks (LEAK-10 holds; four agents found nothing), the regime (SPLIT-1/4/11/13/14), the value (TP-2: 18.2 against 41.2 for the mean and 25.3 for the raw sensor) or the metric (MET-4). Every remaining fix is to text, cleaning rules or the record; none changes the split or the target definition. Only two points remain open between us. In both, the facts above argue for the milder option:
- for SPLIT-20, keep three windows and write the exception; do not move to six windows;
- for the outage, use the impossible-value clause rather than the training-period clause.

```text
Verdict: ship after changes.
Validity: USE-1/USE-3 conceded, fix text (forward monthly refit, no test-month reference known); USE-8/EV-2 conceded, fix text (seasonal retraining as recommendation; network transfer named with LOSO 26.18 vs 21.11); LEAK-10 holds; SPLIT-1/4/11/13/14 hold.
Value: TP-2 holds (18.2 vs 41.2 dummy, 25.3 raw); MET-4 holds.
Quality: CLEAN-11 spike rule restricted to training rows, QC default named; Nakawa outage set missing under CLEAN-11 impossible-value clause (92 h, training only), guard added; symmetric dead-channel rule (18 h + 15 h, check the 0.29 hour); EV-7 stale notes and record fixed.
For the curator: SPLIT-20, I recommend a written exception (6 windows would score Nakawa from a cold start in Sep/Oct and put the 92-hour outage into the Nov test window); confirm the Nakawa outage rule.
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic): airqo_low_cost_air_quality_monitor_calibration_challenge**

We agree on most of it: ship after changes, with no exclusion. I dispute three of the advocate's points (1, 5, 7) and part of a fourth (3, on fit). One new fact, which I checked on the raw `Train.csv`, undoes the advocate's SPLIT-20 exception.

**A1. No leak (LEAK-10, LEAK-16..21): concede the finding, dispute the remedy.**
- I agree that no column leaks and that there are no copies. Four agents found the same.
- The advocate says a deployed model "would not have the lag", and calls the task gamer's fix "a kit change, not a dataset change". Both claims fail on the advocate's own point 4.
  - That point rewrites the task as "corrects the next month's new readings at the collocated devices".
  - A collocated device has a live reference feed. So whether hour t-1's reference is known at prediction time depends on the prediction point. It is not settled by the uncollocated network.
  - The prediction point lives in `dataset.py` (`task_summary.known` and the prediction-point bullet). USE-3 (Must) requires it to be stated there. The kit only prints it.
- **Remedy (unchanged):** `known` must say that no reference value from the test month is known. Fix the `task.md` template bug ("made when The prediction is made for ...").

**A2. Temporal regime, site descriptors, curator order: concede.**
- I raised no objection to temporal over grouped or random, to SPLIT-14, to keeping the site descriptors (USE-10, LEAK-34), or to Lennart's 2026-11-04 call winning ("Who decides").

**A3. Value and metric: concede TP-2 and MET-1..4. Dispute one part, the fit.**
- The advocate calls `fit="approximate"` "honest", but the brief never addresses USE-8.
- `fit_reason` mentions network transfer only in passing ("no network or new-device transfer").
- Network transfer is the actor's main decision. Leave-one-site-out gives 26.18 against 21.11 for the raw sensor (split auditor). The domain practitioner found the model worse than raw at 2 of 3 sites (24.25 vs 20.18 at Makerere, 28.16 vs 19.10 at USEmbassy).
- **Remedy (text):** name network transfer as the main gap under `approximate`, with that figure.

**A4. Task text and stale notes: concede, with two additions.**
- The advocate's list matches my points 1 and 7. Two items are missing:
  - the `known` field, which A1 also needs;
  - the record's 2026-11-04 assessment, which says "all settled" while the 15 hours are open. The advocate's point 7 does list that one.
- Agreed that this is a Must fixed in the definition.

**A5. SPLIT-20: dispute. The exception's fact is false.**
- The advocate's exception rests on this: "only the newest season has all three sites running". Rows per site and month in the raw `Train.csv` (Makerere / Nakawa / USEmbassy):

  | Month | Makerere | Nakawa | USEmbassy |
  |---|---|---|---|
  | Oct 2020 | 383 | 543 | 390 |
  | Nov 2020 | 153 | 352 | 186 |
  | Dec 2020 | 578 | 259 | 0 |
  | Jan 2021 | 504 | 500 | 45 |
  | Feb 2021 | 325 | 0 | 510 |

  Only October and November 2020 have all three sites with real coverage. None of the three test months does. The fact points the other way: widening the windows would score all three sites.
- The second half of the exception, "the next refit faces the newest season", holds for every temporal dataset. It does not set this case apart, so it cannot carry an exception to a Should.
- The bias_correction precedent does not help. The precedent checker reports that "neither record says whether that season is typical", so no SPLIT-20 exception was ever made there.
- "ok (a)" chose the window without recording a SPLIT-20 fact.
- SPLIT-21 is respected. My argument rests on season and site coverage, not on scores.
- **Remedy:** `n_windows=6`, monthly from September 2020 to February 2021.
  - Train sides 52.5% to 92.4% (SPLIT-14 holds).
  - Test months of 462 to 1,312 rows.
  - The monthly cadence is kept.
  - Both seasons and every site are covered.

  An exception remains possible only if it states a fact that is true and specific to this dataset. In either case, `splits_comment` must say what season the test covers.

**A6. Spike rule on a test row: concede. We agree.**
- Apply the rule to training rows only, keep Makerere 2021-02-17 20:00, and name the field's QC default for the four Nakawa drops (CLEAN-11).

**A7. Dead channels and the Nakawa outage: concede the remedy for dead channels, dispute the reasoning on the outage.**
- **Dead channels:** we agree on one symmetric rule (below 0.3 × the other sensor, both channels set missing, rows kept) and on updating the guard.
- **Outage:** the advocate says P3/P5 are "not triggered for what is scored" because all 92 rows are on the training side. That does not hold.
  - The scored quantity is a model trained on these labels. Removing the run moves Nakawa's December test RMSE from 23.2 to 18.9 (column auditor). The outage changes what the December score measures at Nakawa.
  - The definition calls a single high reference hour "an artefact" because the instruments share the air. It then keeps a 92-hour low run, with reference 0.1 against sensor readings of 101 and 102.
  - Comment line 119 ("All labels are observed and positive (0.1 to 459.0)") states the range without naming the run. Under the tension table, a cleaning gap that changes what the target means is a validity question. It is not the quality case "real task against imperfect cleaning".
- Even so, the remedies are close. Both of us accept "rule or note", decided by the curator. **I hold one condition:** if the run stays, the note must name it (dates, 92 hours, ratio) and line 119 must be rewritten. Leaving it silent is not an option.

```text
Verdict: ship after changes.
Settled with advocate: no leak; temporal regime; site descriptors kept; TP-2/MET-4; spike rule training-only; symmetric dead-channel rule; text/record fixes.
Disputed: SPLIT-20 exception's fact is false (only Oct-Nov 2020 have all three sites; Dec 0 USEmbassy, Feb 0 Nakawa) -> n_windows=6 or an exception with a true fact; USE-3 prediction point belongs in dataset.py `known`, not only the kit; USE-8 network gap named with the LOSO figure; Nakawa outage affects the scored model (Dec Nakawa 23.2 vs 18.9) -> rule, or a named note plus a corrected line 119.
For the curator: point 3 (widen; the exception's stated fact does not hold), point 5 (rule or named note).
```

</details>
