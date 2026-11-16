# ppnn_ecmwf_t2m_postprocessing_germany

**Outcome:** added as `ppnn_ecmwf_t2m_postprocessing_germany_1m`. The AI recommends shipping it: the review panel's
changes are made, and one weighing call is open, which test windows (issue 1). ECMWF's 48 h ensemble forecasts of 2 m
temperature at 535 DWD stations, 2007-2016, corrected against the observed temperature (Rasp and Lerch 2018); MAE stands
in for the source's CRPS.
Verdict: ship after changes (made).
Validity: SEL-1 holds; SEL-10/SEL-11 hold (post-processing of forecasts, no lag of the target); USE-1/USE-8 hold
(direct fit; a point product is real, USE-9); LEAK-10 holds for all 41 inputs; LEAK-16 to LEAK-21 hold (0 copies, one
row per station and date); LEAK-9 triggered (a model can read later forecasts of the same station from other test
rows, about 1% MAE), fixed by a protocol line; SPLIT-10 holds (the gap is one day longer than needed, the source's
convention, wording fixed); SPLIT-15 departed (the spacing, not yet recorded as an exception) and SPLIT-18 against
SPLIT-19 open (issue 1); PROV-8 holds (the paper's Table 2 reproduced to the decimal); PROV-9 holds at 2021, the year's
text fixed; PROV-6 holds (Rasp 2021 over Chen and Lerch 2022).
Value: TP-4/TP-10 hold (LightGBM 1.029 against per-station MOS 1.296 and the raw forecast 1.447 MAE, better than MOS on
3 of 3 windows, measured on the changed frame); MET-5/MET-11: the stand-in `mae` kept, its measured closeness to the
CRPS now in the metric's reason.
Quality: CLEAN-11 triggered twice (one test label, one stuck run of 12 nights in training), fixed (target missing, the
rows leave by CLEAN-15); notes corrected.
Weighed (issue 1 only): for the source's year: its operational design +, refit gain immaterial +, 8.7 times the test
days +; for the shipped fortnights: rule order +, three weather precedents +, no other dataset reopened +.
For the curator: issue 1, a weighing call (the shipped spaced fortnights with an exception to SPLIT-15, or 2016 in three
four-month windows with an exception to SPLIT-18).
The panel's changes are in `dataset.py` (the rule that each test row is predicted from its own features only, the
measured closeness of MAE to the CRPS, two impossible labels removed, corrected notes); the definition's numbers were
measured again on the changed frame.

**Main points:** One weighing call: test on the shipped two-week windows spaced through 2016 (implemented), or on the
source's test year 2016 as three four-month windows (issue 1).

**Record judgment:** valid. A peer-reviewed post-processing benchmark (Monthly Weather Review 2018) with its data
deposited by the first author under CC BY 4.0 and its code public; the rows reproduce the paper's Table 2. The
screening's "21 forecast variables" and "537 stations" are 18 variables and 535 stations with rows.

**Issues for Lennart:**

1. **Which test windows: the shipped two-week windows spaced through 2016, or the source's year 2016 as three four-month windows?**

   * **Problem:**
     - The definition tests three 14-day windows of 2016 spaced four months apart (from 18 April, 18 August and 18
       December), as the house rule for weather asks (test windows of one to two weeks), while the source tests the
       whole of 2016 "to ensure our verification procedure mimics operational conditions" (Sect. 2.1)[^s18][^s19].
     - The two rules are of equal strength and the weather rule comes first, but its reason, that short-lived
       quantities need frequent refits, may not hold here: the source finds daily updating of its networks no
       better (Sect. 7) and rolling training windows only marginally better (Sect. 5.1, footnote 4), and refitting at
       each window start moves a per-station correction by at most 0.004 °C[^order].
     - Either design needs one recorded exception: the shipped windows depart from rolling the windows back from the
       newest data, and the source's year departs from the weather rule[^s15].
   * **Background:**
     - Per-station MOS (model output statistics) is the classical correction, a linear fit per station; the station
       offset adds each station's mean past error to the forecast.
     - About 500 stations share one weather situation a day, so a 14-day window holds about 14 independent situations,
       not 7,000 independent rows.
     - The release ends on 31 December 2016 and the benchmark's size rules give a dataset with 1M training rows three
       windows, so three contiguous fortnights would all fall in late November and December; spacing them gives
       spring, summer and winter.
     - Late December is not an atypical season: the raw forecast's MAE is 1.424 over the last three weeks against 1.430
       over 2016, so the season rule does not itself ask for the spacing[^s20].
     - The late-August window falls in a warm spell where the ensemble runs too cold (mean error -0.72 °C in August),
       the hardest window for the raw forecast (MAE 1.640) and the one where nonlinear corrections gain most.
   * **Effect on the task:**
     - The task is the same under both designs (inputs, target, prediction point; refitting gains next to nothing);
       what changes is how many days score a model, 42 or 366.
     - On 42 days the standard error of a difference between two models is about 0.04 °C, against 0.014 on the year,
       so models a few hundredths apart (tuned boosting models, ridge against per-station MOS) can swap ranks; LightGBM
       against the simple corrections never does.
     - The shipped days show LightGBM ahead of per-station MOS by 0.265 °C, against 0.184 over all of 2016 (one fit on
       2007-2015, raw file).
   * **Experiments:** on the raw file, before the two label fixes; none of these may decide the windows[^s21].
     - Refit gain (one fit on 2007-2015 against a refit at each window start, MAE in °C, + when the refit helps):
       per-station MOS -0.003 to +0.004 and LightGBM -0.016 to +0.006 on the shipped windows; +0.014 for LightGBM on
       average over six windows (the shipped three and three fortnights at the end of 2016).
     - Over all 2,600 choices of 3 of 2016's 26 fortnights, ridge against MOS (0.014 apart over the year) flips in 29.7%
       and MOS against the station offset in 13.4%; the order of six models equals the year's in 21.2%.
     - Option B checked on the raw file: windows from 2016-01-01, 05-01 and 09-01 with the 2-day gap hold 60,211,
       61,077 and 60,930 test rows (121 to 123 days); their training pools are 89.9%, 93.2% and 96.6% of the rows, so
       the dataset stays a `_1m` version with a random 1M each.
     - The yearly windows 2014, 2015 and 2016 (an option in the definition's decision table) are worse than B on every
       count: the source never tested 2014 or 2015, and 2014 holds the 121 days without soil moisture at every station.
     - On the last six weeks of 2016 MOS falls below the station offset; on the shipped windows and on the year it does
       not.
   * **Consistency:**
     - The same task class chose short weather windows over a source's longer horizon: climate_model_weather_forecasting
       (1 week)[^cm], bias_correction_r_bias_correction_r_2 (7 days) and rain_in_australia (14 days).
     - None of them had a source that verifies by year and finds refitting immaterial; B would be the first exception
       to the weather rule, and climate_model_weather_forecasting_1m (also station temperature from forecast-model
       output) would become a candidate to reopen.
     - Spaced windows: perth_house_prices spaced them around the COVID months; rain_in_australia took 26 contiguous
       windows over spaced ones; A would be the first spaced weather windows[^prec].
     - Under A, climate_model_weather_forecasting_1m keeps its three contiguous weeks of July 2023, one season; the
       precedent checker would align it when it is next reopened, not now.
   * **Panel:**
     - For A (advocate, precedent checker, builder): at equal strength the earlier rule wins, three weather precedents
       agree, and the spacing rests on the calendar, not on scores.
     - For B (critic, the blind reviewer independently, the domain practitioner in the form of the years 2014-2016):
       the source's year is the data owner's operational design, the weather rule's reason does not hold, and it gives
       8.7 times the test days.
     - The split auditor holds A right by the order of the rules and the precedents, and drew B as the mildest form of
       the exception if you prefer the source's year.
     - The mediator leaves it to you: both sides rest on rules of equal strength, and each path needs exactly one
       exception (the advocate and the critic agree on this).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Spaced fortnights (implemented) | 3 x 14 days from 2016-04-18, 08-18 and 12-18, gap 2 days, about 7,000 test rows each; the definition now cites the season rule for the spacing; on A it is recorded as an exception to rolling back from the newest data | follows the weather rule and its order; three weather precedents; spring, summer and winter; no other dataset reopened | 42 test days, close models can swap ranks; the first spaced weather windows; LightGBM's lead over MOS shows larger than over the year |
     | B | 2016 in three four-month windows | windows from 2016-01-01, 05-01 and 09-01, gap 2 days, about 60,000 test rows each, a random 1M training rows each; recorded as an exception to the weather rule | the source's test year; rolls back from the newest data; every season; 8.7 times the test days | the first exception to the weather rule; climate_model_weather_forecasting_1m becomes a candidate to reopen; a model could read a station's later forecasts from more test rows (barred by the protocol rule, worth about 1% MAE on the shipped windows) |
     | C | Three contiguous fortnights at the end of 2016 | 3 x 14 days from 2016-11-20, 12-04 and 12-18, gap 2 days | the strict default, no exception | one season only (late November and December) |

   * **Recommendation:** A, by the order of the rules and the three weather precedents, recorded as an exception for
     the spacing; B if you hold that the source's own finding (refitting does not help, and it verifies by year) removes
     the weather rule's reason for this task, recorded as an exception and checked against
     climate_model_weather_forecasting_1m. **Decision:** A or B (or C)?

   **Notes for the AI:**
   - A: in `splits_comment`, replace "(SPLIT-20)" after "Christmas weeks at the end of the release" with the exception
     and add the split auditor's August sentence: "Exception to SPLIT-15 (<date>, Lennart): the windows are spaced four
     months apart instead of rolled back from the newest data: the release ends on 31 December 2016 and a 1M train side
     gets three windows, so contiguous fortnights would all fall in late November and December; spacing them tests
     spring, summer and winter (chosen from the calendar, not from scores; serves P4). The August window falls in a
     late-summer spell with the ensemble too cold (mean error -0.72 in August), where nonlinear corrections gain most."
     Decision 1's description says the same. A Cases row under SPLIT-15 in splits.md, a CC line in the record.
   - B: `WINDOW_STARTS = ("2016-01-01", "2016-05-01", "2016-09-01")`, `TemporalSplits(window=4, unit="months",
     cutoffs=WINDOW_STARTS, gap=LEAD_DAYS, gap_unit="days")`; add the option to Decision 1's table; rewrite
     `task_summary.split` and `changes` (the source's test year in three windows, MAE instead of the CRPS),
     `splits_comment` with "Exception to SPLIT-18 (<date>, Lennart): the source verifies by year (Sect. 2.1) and finds
     the refit cadence immaterial (Sect. 7; Sect. 5.1, footnote 4; measured: per-station MOS at most 0.004 °C, LightGBM
     -0.016 to +0.006 on two-week windows), so the rule's reason, short-lived quantities refit often, does not hold;
     serves P4: the test stands for the service's year", `version_comment` (test and pool sizes, frame rows), the
     LEAK-9 note (its windows are now four months: re-measure the join of later forecasts or say it spans more days),
     the soil-moisture shares and the skill numbers; re-run `dataset check`, the leak and task probes and
     `skill_vs_raw.py`; a CC line, a Cases row under SPLIT-18, and the reflection on
     climate_model_weather_forecasting_1m to the curator (does the same hold there? if not, the fact here is the source's
     year-long operational verification).
   - C: `TemporalSplits(window=14, unit="days", n_windows=3, gap=LEAD_DAYS)`; `splits_comment`, `task_summary.split`,
     Decision 1, `version_comment` and the skill numbers measured again.

   [^s18]: **SPLIT-18** (Should): "Short-lived quantities need short windows: weather test windows of one to two weeks
     at most." Cases: climate_model_weather_forecasting.
   [^s19]: **SPLIT-19** (Should): "When the source defines the split (a competition's or a paper's official periods),
     follow it." Rasp and Lerch (2018), Sect. 2.1: the models train on 2007-2015 and are verified on 2016.
   [^order]: principles.md, "Conflicts between rules": "At equal strength the earlier rule wins"; a departure from a
     Should is an exception recorded with the fact that sets the case apart.
   [^s15]: **SPLIT-15** (Should): "Roll the windows back from the newest data: as many windows as an IID or grouped task
     of that size would get folds."
   [^s20]: **SPLIT-20** (Should): "Check whether the newest windows fall in an atypical season and widen them so most do
     not."
   [^s21]: **SPLIT-21** (Must): "Decide neither the training history nor the windows from a comparison over a few test
     windows."
   [^cm]: climate_model_weather_forecasting (Lennart, before the v2 copy of 2026-10-14): "TabRed uses 1 month refit
     horizon. For weather this is a bit much. I would argue for one or two weeks at most?"
   [^prec]: perth_house_prices (Lennart, CC 2026-10-26, issue 6): one-month windows every third month, so most fall
     outside the COVID months. rain_in_australia (Lennart, CC 2026-10-26, issue 2): 26 contiguous 14-day windows instead
     of 9 spaced six weeks apart ("follows SPLIT-15; no exception needed").

**Review panel:** ship after changes (mediator). Tier full: the claim, column and split auditors, the domain
practitioner, the blind reviewer, the task gamer and the precedent checker, then the advocate and the critic with one
rebuttal each, and the mediator, who re-measured the two impossible observations and option B's windows on the raw file.
Claims: 31 audited and 6 implied; the data, the target, the inputs, the prediction point and the paper's Table 2 hold;
refuted or incomplete, and now fixed: the year's evidence (the 2020 deposit holds every row; 2021 kept, since it is the
first that holds every value we ship), the stand-in's closeness not measured, the gap's reason, two section citations,
the soil-moisture pattern and probe 13's reading. Blind review: include with changes; its main concern is the 42 test
days (it also found the impossible test label). Task gamer: barely gameable; joining the later forecasts of the same
station from other test rows gains about 1% MAE, now barred by a protocol line; no other exploit. Agreed: the direct
fit, no data leak, `mae` over `rmse`, the label fixes and the note fixes. Disputed: a note or a protocol line for the
later forecasts (settled: the line), the year 2020 or 2021 (settled: 2021), the test windows (issue 1); the precedent
checker's consistency check on the spacing is folded into issue 1 (A against C).

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany), 2026-11-08
Tier: full (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent checker;
advocate and critic with one rebuttal each). Rules read (principles.md, splits.md, leak_checks.md,
metrics.md, provenance.md, cleaning_features.md). Mediator check: the commands are quoted below.

=====================================================================================================================
1. RECOMMENDATION (judgment record)
=====================================================================================================================
Verdict: ship after changes.
Validity: SEL-1 holds; SEL-10/SEL-11 hold (post-processing of forecasts, no lag of the target; TP-10 legs 1 and 2);
  USE-1/USE-8 hold (direct; the point-vs-distribution gap is stated, a point product is real, USE-9); LEAK-10 holds for
  all 41 inputs; LEAK-16 to LEAK-21 hold (0 copies, one row per station-date); LEAK-9 triggered (a participant can join
  later forecasts from other test rows, about 1% MAE), fixed by a protocol line; SPLIT-10 holds (gap one day more than
  needed, the source's convention, wording fixed); SPLIT-14 holds; SPLIT-15 departed (spaced windows, not recorded) and
  SPLIT-18 against SPLIT-19 open: issue 1; PROV-8 holds (Table 2 reproduced to the decimal); PROV-9 holds at 2021 by
  precedent, text fixed; PROV-6 holds (Rasp 2021 over Chen and Lerch 2022).
Value: TP-4/TP-10 hold (LightGBM 1.033 against per-station MOS 1.297 and the raw forecast 1.448 MAE, 3 of 3 windows);
  MET-5/MET-11 stand-in `mae` kept, its measured closeness to be written in (Must).
Quality: CLEAN-11 triggered twice (one test label, one 12-night stuck run in training), fixed (target missing, rows
  leave by CLEAN-15); notes corrected.
Weighed (issue 1 only): for the source's year: source's operational design +, refit gain immaterial +, 8.7x test days +;
  for the shipped fortnights: rule order (SPLIT-18 first) +, three weather precedents +, no reopening of climate_model +.
For the curator: issue 1, a weighing call (which test windows: the shipped spaced fortnights with an exception to
  SPLIT-15, or 2016 in three four-month windows with an exception to SPLIT-18).

=====================================================================================================================
2. CHANGES TO MAKE NOW (no decision needed), rank order
=====================================================================================================================
C1. P4, LEAK-9 (Should, as amended 2026-11-05): add the protocol line to `splits_comment` and a note
    "Potential leak, kept on purpose (LEAK-9, an evaluation leak)": a 14-day window holds a station's rows for d+1 and
    d+2, whose forecasts were issued after row d's prediction point; joining them by (station, date) lowers the task
    gamer's MAE from 1.0833 to 1.0692 (per window -0.002 / -0.011 / -0.029; 1000 trees 1.0662 to 1.0606, +0.006 / -0.012 /
    -0.012; a random column moves the mean by about 0.005). Line as in the precedents: "Each test row is predicted from
    the training rows and its own features only; no feature or model step may use other test rows." No data change, no
    thinning of the test days. (Settled: the advocate's "a note suffices" yields to the rule's text, which names a
    protocol line; he conceded, C1 of his rebuttal.) The strict line also bars same-date features of other stations
    (one run, known at the prediction point), which the gamer used honestly; the precedents use the strict line, so
    keep it.
C2. P6, MET-11 (Must, "closeness measured on the shipped splits where possible"): add to the metric `reason`: Kendall
    tau between MAE and the CRPS over 10 models 0.944 / 0.989 / 0.944 (Dec / Aug / Apr), the same best model in 3 of 3
    windows; `rmse` 0.989 / 0.944 / 0.899. This also settles the builder's draft issue 2 for `mae`: MET-11 takes the
    closest computable metric, and MAE is the CRPS of a point forecast by identity and slightly closer on the measure.
C3. P5, PROV-9 (Must, holds at 2021): replace "contents not downloaded" with the measured facts and the criterion: the
    2020 deposit (figshare 9762980) holds all 1,808,942 rows, the identical target and the 50 t2m members (mean and
    variance equal `t2m_mean`, `t2m_var`), i.e. 5 of the 40 inputs, not the other 17 variables or `orog`; 2021 is the
    first deposit that holds every value we ship (2_month_survival_rate_prediction). Turn the "535 vs 537 stations"
    anomaly into the fact: two listed stations (DWD 3246, 6184) never reported; the paper's 499 stations in 2016 (502
    here) stays unexplained.
C4. P7, CLEAN-11 (Should) then CLEAN-15 (Must): in `_clean`, set `t2m_obs` missing and let the rows leave, each guarded
    by its count: station 254 on 2016-08-25 (0.0 between 18.1 and 18.2, forecast 19.8; a test label of the August
    window, +0.0028 MAE there) and station 288 from 2014-12-20 to 2014-12-31 (11.3 on 12 nights while the forecast falls
    from 9.4 to -3.0; training). Re-measured by the mediator on the raw file: both as reported. Precedent airqo (test
    labels too). Add a note.
C5. P7 / writing: soil moisture (curation bullet and Decision 2): besides 2014-03-06..07-04 and 17 stations always,
    9,891 rows at 11 Baltic-coast stations miss it by model period (before 2010-01-29, or from 2016-03-11); 7 stations
    (147, 153, 171, 203, 333, 399, 401) have it in training and not in any test window (test 4.2% missing, train
    6.6-6.8%). Values stay missing. Also: only t2m is interpolated bilinearly, the other 17 fields are the nearest grid
    point (fix "interpolated to the station" in `task_summary.row`); `orog` is the 2007 cycle's; `station` is the
    deposit's index 1..535; units of sm (kg m-3), cape, q, winds, and squared units of the `_var` columns.
C6. Writing / EV: cite Sect. 7 (daily updating no better) and Sect. 5.1 footnote 4 (rolling EMOS marginal), not Sect. 6
    and 3.1 (Decision 1, notes, and the REVIEW.md issue text). SPLIT-10 wording: the D-2 00 UTC observation is in at the
    prediction point; only D-1's is missing; the 2-day gap stays as the source's convention. Probe note (EV-3): probe 13
    also flags the target's p90 (z +6.3), the 2015 summer heat (Q3 p90 20.3 against 17.5-19.0), not recording.
    `task_summary.split`: drop "as for a correction refit every two weeks" (no weather service refits so; practitioner),
    e.g. "a correction trained on the earlier years, scored on ...", worded for whichever design issue 1 keeps.
    Optional: one line acknowledging TIGGE (its licence asks for it).
Not changed: the `cape_mean` values of -4.5e-13 (float residue of zero; not impossible in substance, CLEAN-11 keeps
unusual values); `_var` kept as variance (lossless, documented); `date` as a feature (USE-6; dropping the year moves
LightGBM by -0.025 to +0.038).

=====================================================================================================================
3. ISSUES FOR THE CURATOR
=====================================================================================================================
Issue 1 (P4, Should against Should; a weighing call): which test windows?
- Problem: the shipped design is three 14-day windows spaced four months apart in 2016 (Apr 18, Aug 18, Dec 18). Two
  Should rules pull apart. SPLIT-18 (weather windows of one to two weeks) comes before SPLIT-19 (follow the source's
  split: Rasp and Lerch test the whole of 2016, "to ensure our verification procedure mimics operational conditions",
  Sect. 2.1). Besides, the spacing departs from SPLIT-15 (roll back from the newest data) and is not recorded as an
  exception; SPLIT-20's "atypical season" clause does not cover it (raw MAE of the last three weeks 1.424 against 1.430
  for 2016).
- Effect: 42 test days. About 500 stations share one weather situation per day, so the SE of a model difference is
  about 0.04 on 42 days against 0.014 on the year; ridge against MOS (0.014 apart over the year) flips in 29.7% of the
  2,600 choices of 3 of 2016's 26 fortnights; the shipped windows give LightGBM minus MOS -0.265 against -0.184 for the
  year. LightGBM against any other model never flips. Under SPLIT-21 (Must) these model comparisons inform; they decide
  nothing.
- For the shipped fortnights (advocate; precedent checker; builder): rule order at equal strength; same-task precedents
  chose SPLIT-18 over the source's horizon (climate_model_weather_forecasting: "TabRed uses 1 month ... For weather this
  is a bit much"; bias_correction_r_bias_correction_r_2, 7 days; rain_in_australia, 14 days). The spacing gets three
  seasons from the protocol's three windows, a fact of the calendar (the release ends 31 December), not of scores.
- For the source's year (critic; domain practitioner; blind reviewer independently; split auditor's "mildest form"):
  SPLIT-18's reason, short-lived quantities refit often, does not hold here: the source finds daily updating no better
  (Sect. 7) and rolling EMOS marginal (Sect. 5.1 fn. 4); refitting at each window start moves per-station MOS by at
  most 0.004 and LightGBM by -0.016 to +0.006 on the shipped windows; DWD's MOSMIX trains on 10+ years. The source's
  year is the data owner's deliberate operational design, which climate_model's case lacked.
- Options (mediator check on the raw file for (b): 4-month windows from 2016-01-01, 05-01, 09-01, gap 2 days: test
  60,211 / 61,077 / 60,930 rows (121-123 days), train pools 89.9% / 93.2% / 96.6% of the rows, so still `_1m` with a
  random 1M; feasible as TemporalSplits(window=4, unit="months", cutoffs=..., gap=2, gap_unit="days")):
  | | Option | Exception recorded | Pro | Con |
  | a (shipped) | 3 x 14 days, spaced Apr/Aug/Dec 2016 | to SPLIT-15: release ends 31 Dec, three windows at 1M rows, only spacing gives three seasons | rule order; three weather precedents; no reopening | 42 test days; first spaced weather windows; add the split auditor's sentence on the August warm spell |
  | b | 2016 in three contiguous 4-month windows | to SPLIT-18: the source verifies by year and shows the refit cadence immaterial (Sect. 2.1, 7, fn. 4); serves P4 | the source's test set (SPLIT-19), rolls back from the newest data (SPLIT-15), every season, 8.7x test days | first exception to SPLIT-18; climate_model_weather_forecasting becomes a candidate to reopen; the C1 exploit covers more test days (the protocol line holds either way) |
  | c | 3 contiguous fortnights at the end of 2016 | none | the strict default | one season; changes the model order (MOS below the station offset); the split auditor advises against |
  The builder's yearly option (2014, 2015, 2016) is dominated by (b): the source never tested 2014 or 2015, and 2014
  holds the 121-day soil-moisture outage at every station.
- What would settle it: the curator's answer to "does the source's own refit finding remove SPLIT-18's reason for this
  task?" Yes: (b), recorded as an exception to SPLIT-18, with a reflection on climate_model. No: (a), recorded as an
  exception to SPLIT-15. The mediator does not settle it: both sides rest on Should rules of the same part, and each
  path needs exactly one exception (the advocate and the critic agree on this after the rebuttal).
- Decision: (a) or (b) (or (c)).

No other issue needs the curator.

=====================================================================================================================
4. DISPUTED POINTS SETTLED
=====================================================================================================================
D1. LEAK-9: note or protocol line. Settled by the rule's text (a protocol line the benchmark checks) and the precedents
    (medical_facility_operational_data, frempl_french_motor_personal_line); conceded by the advocate. C1.
D2. Year 2020 (claim auditor) or 2021 (advocate, critic, precedent checker). PROV-9 (Must) as applied in
    2_month_survival_rate_prediction reads "holds the rows" as "holds every value we ship"; the 2020 deposit holds 5 of
    40 inputs. 2021 stands; 2020 would be an amendment of PROV-9 (and reopen 2_month_survival), not a one-off. C3.
D3. Blind reviewer: "the 2-day gap applies only before the last window". Refuted by measurement (EV-2): train_end is the
    window start minus 3 days in all three windows (12-15 / 08-15 / 04-15); the sample's rows on 04-16/17 and 08-16/17
    are training rows of later windows.
D4. Metric `mae` or `rmse` (builder's draft issue 2). Settled by MET-11 (the closest computable metric: identity with the
    CRPS of a point forecast, tau 0.959 against 0.944 on the mean) and MET-10's diversity. C2.
D5. Station 288: hand fix or keep with a note (column auditor's alternative). CLEAN-11's default is "impossible values
    become missing"; twelve identical 0.1 C readings while the forecast falls 12 C are impossible. Both debaters agree. C4.

=====================================================================================================================
5. TASK GAMER: EXPLOITS MAPPED
=====================================================================================================================
The definition has no "Potential leak, kept on purpose:" note and no accepted warnings (bundle_checks.accepted is {}).
- Exploit 1, same-station forecasts valid d+1, d+2 from other test rows: LEAK-9 (evaluation leak, a model reads other
  test rows). NEW. Gain 0.006-0.015 mean MAE (about 1%), not consistent on the December window. Remedy C1.
- Label-based attacks (observation residuals at d-1/d+1, rolling station bias, observation lags): need test labels, which
  a participant does not get; not exploits. The rolling bias sizes what fresh observations would add operationally
  (0.024 mean); left out on purpose as forecasting from lags (SEL-11, TP-10), agreed by the practitioner.
- Source lookup (the public file matches every row): true of any public dataset; no rule triggered.
- Nothing found: row order, formats, copies, test-set composition, single features, transforms over all rows, the
  train-against-test classifier (AUC 1.0 from the synoptic state, no label information), the 1M cap (full train sides
  1.0817 against 1.0833).

=====================================================================================================================
6. AGREED FACTS (all agents, measured)
=====================================================================================================================
- Data: data_RL18.feather (figshare 13516301, CC BY 4.0, md5 matches), 1,808,942 x 43; 1,626,724 rows 2007-2015 +
  182,218 in 2016, as in the paper; Table 2 reproduced (raw 1.152 against 1.16; EMOS-gl 1.009 against 1.00; EMOS-loc
  0.902 against 0.90). `_var` is the variance (var ddof=1 of the members to 2.5e-14).
- Inputs: every input is a step-48 forecast of the 00 UTC run or a fixed station property; no lag of the observation;
  0 exact copies; one row per station-date; soil-moisture missingness does not track the target (indicator R^2 -3.1).
- Use case: direct (DWD post-processing team); the target is the quantity issued; MAE is the score DWD reports for
  point temperature.
- Signal: raw 1.448, station offset 1.351, per-station MOS 1.297, ridge 1.318, LightGBM 1.033-1.118; LightGBM beats MOS
  on 3 of 3 windows; families spread on the full train sides (the probe's `no_spread` is its 200k-row artefact).
- Splits: 14-day windows of 6,936 / 6,967 / 7,003 rows; train pools 92.8%-99.6%, a random 1M each, every year
  present; test stations without training rows 0 / 0 / 1; no break in the history at the 2016 upgrade.
- Gap: 2 days, the source's code; one day more than needed; no label unknown at the prediction point in training.
- Metric: the CRPS is the source's one criterion (MET-5); MAE equals the CRPS of a point forecast; tau 0.944-0.989.
- Bad labels: station 254 2016-08-25 (test) and station 288 2014-12-20..31 (train), re-measured by the mediator.
- Copy: Rasp 2021 ships, not Chen and Lerch 2022 (same rows, other inputs; PROV-6).

=====================================================================================================================
7. CONSISTENCY WITH PRECEDENT
=====================================================================================================================
Followed: SPLIT-18 window length (climate_model_weather_forecasting, bias_correction_r_bias_correction_r_2,
rain_in_australia); PROV-9 year (2_month_survival_rate_prediction); PROV-6 copy choice (hiva_agnostic /
nci_aids_antiviral_screen); LEAK-9 protocol line (medical_facility_operational_data, frempl); CLEAN-11 on test labels
(airqo); MET-11 measured closeness (numerai_v5_2_1m); random 1M over the whole history (climate_model_weather_
forecasting_1m).
Departure: the spaced windows (SPLIT-15). Distinguishing fact offered: the release ends 31 December and the protocol
gives three windows at 1M rows, so contiguous fortnights cover one season (rain_in_australia had 26 windows;
perth_house_prices spaced for the COVID months). It is part of issue 1: under (a) it becomes a recorded exception to
SPLIT-15; under (b) it disappears.
Reflection question if (b) is chosen (the first exception to SPLIT-18): would the same hold for
climate_model_weather_forecasting_1m, also station temperature from NWP output, whose short windows were chosen without
a measured refit gain? If yes, reopen it; if the fact is the source's own year-long operational verification, say so in
the exception.
First case: `mae` as the stand-in for a CRPS; euppbench_t2m_station_postprocessing (screening) poses the same question
and should follow this one.
No drift, no third exception of one reason (precedent checker).
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR REPORT: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany), 2026-11-08
Definition: ppnn_ecmwf_t2m_postprocessing_germany_1m/dataset.py

VERDICT: the definition holds on everything that bears on validity. No leak, no wrong target, no copy across the split.
The rows, the target and the inputs match the paper to the decimal: the raw ensemble scores CRPS 1.152 against the
paper's 1.16, global EMOS 1.009 against 1.00 and local EMOS 0.902 against 0.90 on 2016. The `mae` stand-in holds. Its
closeness to the CRPS was not measured in the definition, though MET-11 asks for it where possible; I measured it here
(Kendall tau 0.944 / 0.989 / 0.944, the same best model in all 3 windows). Refuted or incomplete: the year (the 2020
deposit already holds every row), the gap's reasoning, two section citations, the soil-moisture pattern and probe 13's
reading. Every one of these has a one-line fix in the definition's text, or is a curator call on `year`.

Grounds used: the paper (arXiv 1805.09091 v1 full text, read), the GitHub repository slerch/ppnn (README,
nn_postprocessing/nn_src/utils.py, data_processing/*.R), the figshare API for 13516301, 9762980 and 19453580, and the
raw feather file (md5 checked). I also downloaded the 2020 deposit data_interpolated_00UTC.nc (400,239,752 bytes, md5
bfcf0a87... = figshare's) to the session scratchpad, outside the repository, and compared it value by value.

=====================================================================================================================
TABLE: claim | source | test | result | evidence | rule
=====================================================================================================================
1 | deposit, size, md5, CC BY 4.0, 2021-01-04 | download_description, claims 1 | figshare API + md5 of local file | HOLDS | API: 615,496,032 B, computed_md5 18bb8d47..., CC BY 4.0, published 2021-01-04T10:16:41Z, author Rasp; local md5 identical | EV-4, PROV-10
2 | full data of Rasp & Lerch 2018 | curation_comments | reproduce Table 2 on the file: Gaussian CRPS of raw ensemble (mean, sqrt(var)), EMOS-gl and EMOS-loc fit on 2007-2015 by min CRPS, scored on 2016 | HOLDS (decisive) | raw 1.152 (paper 1.16; the paper scores the 50-member ensemble, Gaussian is the closed-form approximation), EMOS-gl 1.009 (1.00), EMOS-loc 0.902 (0.90); GitHub README links the deposit as "The data needed to reproduce the results" | PROV-8, EV-1
3 | year 2021 = first deposit with all inputs; 2020 deposit holds t2m forecasts and obs only (contents not downloaded) | `year`, curation_comments, claims 3 | downloaded the 2020 netCDF and joined it to the feather by station coordinates and date | CONTENT HOLDS; YEAR REFUTED AS STATED (curator call) | 2020 file: t2m_fc (3653 x 50 x 537, deg_C), t2m_obs, station alt/lat/lon/id/names. Non-missing obs = 1,808,942 = the feather's rows; 2016 182,218; 2007-2015 1,626,724; obs identical (max diff 0.0); member mean = t2m_mean (max diff 4e-19); member var(ddof=1) = t2m_var (max diff 2.5e-14). So every row, the target and the main input were first published 2020-02-11. The 2021 file adds 17 auxiliary variables and orog: added columns, a version under PROV-6. PROV-9 dates by "the first ... that holds the rows" | PROV-9 (Must), PROV-6
4 | Chen & Lerch 2022 = same rows + raw t2m members, not used | curation_comments | figshare API | PARTLY TESTED | API: temperature_data_cgm_std.feather, 1,360,331,336 B, CC BY 4.0, 2022-07-11, authors Chen, Lerch. The schema (94 cols, 1,808,942 rows) rests on the record's footer read of 2026-11-08; not re-read here | PROV-6
5 | 36 h lead not in the deposit | curation_comments | README + `date` hours | HOLDS | README: "Forecast lead time: 36h and 48h (valid at 12 and 00UTC)"; every `date` is 00:00 UTC; the 2020 netCDF is the 00UTC file only | -
6 | 1,808,942 x 43, columns as listed | _clean step 1 | read file | HOLDS | (1808942, 43); the column order equals the assert; Table 1 of the paper lists the same 18 variables + 4 station features (text says p = 42) | -
7 | rows = paper's 1,626,724 + 182,218 | curation_comments | count by valid year | HOLDS | 1,626,724 (2007-01-03..2015-12-31) + 182,218 (2016); paper Sect. 2.2 identical; also the paper's "2015 training set ... 180 849" = 2015 rows in the file (180,849) | PROV-13
8 | no missing target, one row per station-date | _clean step 3 | count | HOLDS | obs NA 0, duplicated(station,date) 0 | LEAK-16
9 | anomaly: 535 stations (paper 537), 502 in 2016 (paper 499), station 474 one row | curation_comments | 2020 netCDF station list | HOLDS; 537 vs 535 RESOLVED | the netCDF lists 537 stations; 2 (DWD ids 3246, 6184) never have an observation, so 535 have rows: not damage. Station 474 = DWD 3170, 1 obs in both files. 2016: 502 stations in both deposits; 2 stations report only in 2016. The paper's 499 stays unexplained | PROV-13
10 | `date` is valid time 00 UTC, 48 h after 00 UTC init; 3,651 dates, every calendar day | curation_comments | file + netCDF attribute + paper | HOLDS | hours {0}; 3,651 dates, 0 calendar days missing; netCDF `time` long name "valid time of forecasts and observations, UTC"; paper Sect. 2.1 "48 h", "initialized at 00 UTC" | USE-3
11 | `_var` = variance of 50 members, paper and code use the sd | curation_comments | compare with the members of the 2020 deposit; also CRPS check | HOLDS (decisive) | t2m_var = var(ddof=1) of the 50 members to 2.5e-14 (vs sd: median relative diff 0.30). Gaussian CRPS on 2016 with sd = sqrt(t2m_var): 1.152 (paper 1.16); treating the column as an sd: 1.208. Paper Sect. 2.3 "standard deviation"; utils.py np.std(ddof=1) | CLEAN-1
12 | units: t2m C, d2m K, fluxes J m^-2 over 48 h, Pa, gpm, % | curation_comments | value ranges | HOLDS (flux accumulation inferred) | t2m_mean -21.6..26.2; d2m_mean 247..294 and d2m-273.15 <= t2m_mean+0.5 on 99.7% of rows; sp median 98,234; gh 4,981..5,942; tcc 0..100; ssr median 1.84e7 J/m^2 = 106 W/m^2 over 48 h (plausible; 212 W/m^2 if over 24 h, too high for a median), str median -9.4e6 = -54 W/m^2 over 48 h. Units not read from metadata (the feather has none) | CLEAN-1
13 | sm missing 6.6%: all stations 2014-03-06..07-04 (121 days) and always at 17 coastal stations | curation_comments, Decision 2 | missingness by day and station | INCOMPLETE (partly refuted) | 6.605% holds; 121 all-missing days (2014-03-06..2014-07-04) and 17 always-missing stations hold. But outside the window 9,891 of 59,093 missing rows (17%; 0.55% of all rows) sit at 11 more stations: 4 (ids 11, 127, 128, 424) missing 2007-01-03..2010-01-28; 4 (171, 333, 399, 401) missing from 2016-03-11 to the end, so in all three test windows while their earlier rows have sm; 3 (147, 153, 203) about 40% over the whole span. The 2010-01 and 2016-03 dates match ECMWF ensemble resolution upgrades (Jan 2010; cycle 41r2, 8 Mar 2016), my inference, not checked | CLEAN (P7), writing
14 | lat, lon, alt, orog constant per station | curation_comments | nunique per station | HOLDS | 0 stations with >1 value for each | -
15 | no exact duplicate feature rows | claims 15 | duplicated over all columns except obs | HOLDS | 0 (also 0 without date and station) | LEAK-16..21
16 | target t2m_obs, the netCDF name, deg C, regression | target | netCDF | HOLDS | 2020 netCDF variable `t2m_obs`, units deg_C, "t2m station observation" | USE-5
17 | 42 frame features, 41 probed | README | feature_columns(container) | HOLDS | 42 (incl. `station`, `date`), no scoring columns, target excluded | -
18 | prediction point 00 UTC init; every input a forecast for the valid time or static | curation_comments | column list vs paper Table 1 and netCDF | HOLDS | 36 ensemble summaries + 4 station constants + station + date; no observation lag (the source's add_current_error option is not in the file); the best single feature is the forecast itself (R^2 0.700) | LEAK-10, USE-3
19 | station is a feature; every test station has training rows except one April row | curation_comments, claims 19 | on the shipped (sampled) splits | HOLDS | test rows whose station has no train row: 0 / 0 / 1 (Dec / Aug / Apr). Side note: the builder report's "14-28 test rows per window at stations with under 365 training rows" is 42 / 28 / 29 on the shipped 1M train sides (it was probably counted on the full train sides) | SPLIT-13, USE-10
20 | use case, fit direct | task_summary | paper Sect. 2.1, 7 | HOLDS | the paper sets 2016 aside "To ensure our verification procedure mimics operational conditions"; the point-vs-distribution gap is stated in fit_reason and `changes` | USE-1, USE-8
21 | metric original = mean CRPS 2016 (Table 2), the one ranking criterion | metric.original/reference | read the paper | HOLDS | Table 2 "Mean CRPS ... averaged over all available observations in calendar year 2016"; ranks, Fig. 3-4 CRPSS, DM tests (B.3) and feature importance (Sect. 6) all on CRPS; PIT/VR only for calibration; no MAE or RMSE reported; NN loss = Gaussian CRPS (Sect. 4.1), EMOS by min CRPS (Sect. 3.1). One deliberate choice | MET-5, MET-1
22 | CRPS of a point forecast = absolute error | metric.definition | from eq. B1 | HOLDS (identity) | F = step at x: integral of (1{x<=z} - 1{y<=z})^2 dz = |x - y| | MET-11
23 | the regression task takes one value per row | metric.reason | metrics.py | HOLDS | PREDICTIONS = ("proba", "label", "value"); no distribution or quantile kind | MET-11
23b | (implied by MET-11 stand-in) closeness measured on the shipped splits where possible | metric.reason | 10 models per window, each scored by MAE of its point and by Gaussian CRPS of point + CRPS-fitted spread (sigma = a + b*ensemble sd, spread fitted on the last 60 days of train). Raw ensemble and EMOS-gl scored natively | NOT DONE IN THE DEFINITION; NOW MEASURED: HOLDS | Kendall tau(MAE, CRPS) 0.944 / 0.989 / 0.944 (Dec / Aug / Apr), same best model by both in 3 of 3; tau(RMSE, CRPS) 0.989 / 0.944 / 0.899. The mean tau, 0.959 for MAE against 0.944 for RMSE, slightly favours the stand-in over the fallback; MET-10 diversity also favours `mae`. a4_standin.json | MET-11 (Must), MET-2, MET-10
24 | 3 x 14-day windows from 12-18, 08-18, 04-18; 6,936-7,003 test rows | temporal | container splits | HOLDS | test 7,003 / 6,967 / 6,936; 14 dates each; overlap 0; dummy scores via scorer: train median 6.096 / 7.909 / 4.175, raw t2m_mean 1.4228 / 1.6421 / 1.2798 (= numpy MAE) | MET-2, SPLIT-14, SPLIT-18
25 | gap 2 days = source's get_train_test_sets (fclt=48) | splits_comment | read utils.py; container train_end | HOLDS (convention); REASON REFUTED | utils.py: train_dates_idxs = [date_idx - fclt_didx - window_size, date_idx - fclt_didx], stop exclusive, so the last training date is D-3. Container: train_end 12-15 / 08-15 / 04-15 for test starts 12-18 / 08-18 / 04-18. But the stated reason, "the observations of the two days before it are not yet in", is wrong for D-2: the forecast starts at D-2 00 UTC, the same instant the D-2 00 UTC observation is taken, and is post-processed hours later. Only D-1 is unknown, so the gap is one day longer than needed. That is conservative, not a leak | SPLIT-10 (Should)
26 | train sides 1,679,500-1,800,940 before the budget; 1M each | version_comment | decision table + container | HOLDS | n_train 1,000,000 x 3; 92.84% / 99.56% of 1,808,942; all 10 years present in each train side (2016: 96,236 / 64,898 / 31,272) | SPLIT-14
27 | SPLIT-18/20 over SPLIT-19; paper: daily updating no better (Sect. 6), fixed as good as rolling (Sect. 3.1) | Decision 1 text "(Sect. 6)"; builder report and claims "Sect. 3.1 and 6" | read the paper | FACTS HOLD, CITATIONS REFUTED | daily NN updating "found no improvements": Sect. 7 (Discussion); Sect. 6 is Feature importance. Rolling EMOS "only result in marginal improvements": footnote 4 of Sect. 5.1, repeated in Sect. 7; Sect. 3.1 describes EMOS. Rule order: SPLIT-18 and SPLIT-19 are both Should, and the earlier wins | SPLIT-18, SPLIT-19, writing
28 | decision table: raw MAE and a station offset, no model | _decisions | read code | HOLDS | only a per-station mean-error offset on the full train side; numbers reproduced: offset MAE 1.3358 / 1.5948 / 1.1222 | SPLIT-21
29 | leak probes as quoted; probe 13 = sampling artefact | curation notes, claims 29 | probe log + full-file quarters | NUMBERS HOLD; READING INCOMPLETE | R^2 0.816, 0.700, 0.520, 0.766, missing indicator -3.105 and 0.0% copies match the log. Probe 13 also flags the target's p90 (2015Q3 20.3 deg C, z +6.3; a second quarter z +6.3; newest 8 pooled z +11.9), which the claim leaves out. Full file: Q3 p90 by year 17.5 / 18.0 / 18.3 / 19.0 / 18.0 / 18.2 / 18.4 / 18.2 / 20.3 / 18.6, so 2015 stands alone, the summer of the 2015 heat wave (my reading). 2016 values sit in the band, and rows per day are flat on the full file (494-500 per day in 2014-2016). Weather, not recording | LEAK-22..26, EV-3
30 | skill vs raw: 1.448 / 1.351 / 1.297 / 1.318 / 1.118 / 1.033 | curation notes | re-fit on the shipped splits (a4) | HOLDS | raw 1.448, offset 1.351, per-station MOS 1.297 exactly; ridge 1.305 (differs by imputation); LightGBM L2 1000 trees x 127 leaves 1.114 / 1.037 / 0.958 (mean 1.036; claim L2 1.036); LightGBM beats MOS in 3 of 3; ridge 1.26-1.46 against LightGBM 0.96-1.21, so the families spread | TP-4, TP-10, TP-3

Implied claims attacked:
I1 every feature known at the prediction point: HOLDS (row 18). No observation lag, no analysis field; the ensemble is out
   hours after 00 UTC, well before the 48 h valid time.
I2 the split is the one the use case needs: HOLDS as a rule-ordered choice (SPLIT-18 before SPLIT-19, both Should; the
   source's yearly test is the curator's alternative, issue 1). Remark: spreading the windows four months apart departs
   in form from SPLIT-15 ("roll the windows back from the newest data"). The splits comment gives SPLIT-20's reason;
   if the curator reads it as a departure, it could be called an exception explicitly.
I3 the target is the real-world target: HOLDS. The netCDF calls it the station observation of t2m in deg_C, the
   quantity the service forecasts.
I4 no row is a copy across the split: HOLDS (0.0% exact copies; one row per station-date; test strictly after train).
I5 history breaks (SPLIT-20, implied by "keep every season and year"): NO BREAK FOUND in the forecast error. Raw MAE by
   year 1.43-1.66, mean error -0.34..+0.55 (2007 the outlier). Ensemble spread falls in 2016 (mean sd 0.733 against
   0.79-0.98 before), consistent with the March 2016 upgrade, and soil moisture appears and disappears at 8 stations at
   the 2010 and 2016 upgrades (row 13). Not a validity issue: the source trains across the same history.
I6 licence: CC BY 4.0 on the deposit holds. Upstream, the TIGGE licence (rev. 2, Copernicus) puts ECMWF's TIGGE data
   under CC BY 4.0 and asks written works using TIGGE data to acknowledge TIGGE. ECMWF's older TIGGE page says CC BY-NC
   4.0. Not a blocker; worth one line in the notes.

=====================================================================================================================
REFUTED OR INCOMPLETE CLAIMS, RANKED (principles.md: validity first, Must first)
=====================================================================================================================
1. P5, PROV-9 (Must): `year = "2021"`, justified as "the first deposit of these rows with all inputs".
   Measured: the 2020 deposit (figshare 9762980, 2020-02-11) holds all 1,808,942 rows with identical target values,
   and the 50 t2m members whose mean and variance equal t2m_mean and t2m_var exactly. PROV-9 dates a dataset by the
   first publication that holds the rows; the 2021 file adds columns, which PROV-6 counts as a version.
   Changes: metadata only (year, a citation to add).
   Mildest remedy: the curator's call between `year = "2020"`, with the 2020 deposit added to the BibTeX and the
   notes, and keeping 2021 with a note saying why the deposit with the paper's 40 inputs counts as the first
   publication. Either way, replace "contents not downloaded" with the measured facts.
2. P6, MET-11 (Must, clause "closeness is measured on the shipped splits where possible"): the stand-in's reason
   gives the identity but no measured closeness, though it was measurable.
   Measured here: tau(MAE, CRPS) 0.944 / 0.989 / 0.944, the same best model in 3 of 3 windows (RMSE 0.989 / 0.944 /
   0.899).
   Changes: nothing about the choice; `mae` stands. It also answers draft issue 2 (`mae` against `rmse`): `mae` is
   slightly closer on the mean and adds diversity (MET-10).
   Mildest remedy: append one sentence with these numbers to the metric `reason`, or to a note.
3. P4, SPLIT-10 (Should), reasoning only: the splits comment says the observations of the two days before a window are
   not yet in at the prediction point. The D-2 00 UTC observation is in when the forecast starting at D-2 00 UTC is
   post-processed, so the gap is one day longer than needed.
   Changes: nothing material (one day of training rows out of about 1.7M); keeping the source's convention is fine.
   Mildest remedy: reword, e.g. "the source's own convention; the observation of the day before is not yet in, and
   the source also leaves out the day of the run".
4. P7 and writing: the soil-moisture missingness description (claim 13, Decision 2) is incomplete. 9,891 missing rows
   sit at 11 more stations, 4 of them missing from 2016-03-11 on, so their test rows lack sm in all three windows.
   Changes: a small shift at test for 4 stations; no leak (indicator R^2 -3.1).
   Mildest remedy: amend the note and the Decision 2 text with the three extra patterns.
5. Writing and evidence (EV): wrong section citations. Decision 1 says "updating them daily did not help (Sect. 6)";
   that is Sect. 7. The claims list and builder report say "fixed training sets as good as rolling ones (Sect. 3.1)";
   that is footnote 4 of Sect. 5.1, and Sect. 7.
   Mildest remedy: fix the citation in dataset.py; the REVIEW.md issue text should cite the same.
6. Probe reading (EV-3, LEAK-22..26): claim 29 leaves out probe 13's p90 flags (z +6.3, pooled +11.9). On the full
   file they come from the 2015 summer (Q3 p90 20.3 deg C against 17.5-19.0 in 2007-2014), not from a recording
   change.
   Changes: nothing in the task.
   Mildest remedy: one clause in the probe note.
7. Resolved anomaly (PROV-13): 537 against 535 stations is not damage. Two listed stations (DWD 3246, 6184) never
   reported; the 2020 netCDF shows it.
   Mildest remedy: turn the "Anomaly" line into the fact. The 2016 count (502 against the paper's 499) stays unexplained.

UNTESTED
- Claim 4: the Chen & Lerch 2022 schema (94 columns, same rows). I read only its API metadata; the column read is the
  record's own of 2026-11-08. Low stakes: it is not used.
- Claim 12: the flux accumulation period (48 h) is inferred from magnitudes; the feather carries no units. The TIGGE
  parameter table was not opened.
- Why the paper counts 499 stations in 2016: not found.
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR REPORT: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany)
Date: 2026-11-08. Read-only.

VERDICT
Ship after small changes. No leak in any column (P4 holds column by column). Two impossible labels to set missing
(CLEAN-11, one of them a test label of the August window), and the soil-moisture note is incomplete: 11 more
stations miss soil moisture by ECMWF model period, 7 of them in all three test windows while they have it in the
training years 2010-2015. Dtypes are right (dtype probe: only `station`, numeric_levels, a station index, categorical:
correct). `_var` is the variance (confirmed by the R code and by the magnitudes); kept as published is fine.

Judgment record:
  Validity: USE-3 / LEAK-1 prediction point stated (00 UTC init, 48 h before `date`); LEAK-10 holds for all 41
    inputs (every input is a forecast for the valid time, a static station property, the station or the valid date);
    no missingness caused by the outcome (soil moisture missing by period and grid point); no id encodes the label.
  Quality: CLEAN-11 triggered twice (station 254 on 2016-08-25: obs 0.0 between 18.1 and 18.2, a test label;
    station 288 stuck at 11.3 C for 12 days of 2014-12), fix in the definition; notes to correct (soil moisture causes,
    units of sm, nearest-grid-point aux fields, orography of the 2007 model, station = deposit index).
  For the curator: no weighing call from this role; the label fixes are small and cheap (CLEAN-11, airqo precedent for
    test labels).

SOURCES READ
- dataset.py and README.md of the folder, builder_report.md, claims.md, probes/ (dtype, leak, task).
- github.com/slerch/ppnn: data_processing/generate_Rdata_files/data_preparation.R (writes the file's column names,
  `apply(x, c(1,3), var)` for every `_var`), data_preparation_stationInfo.R, interpolation.R (t2m: bilinear, then
  `- 273.15`), interpolation_aux_surface_more_part2.R (aux fields: "assigning values from closest grid points"; units
  d2m K, ssr/str accumulated, sm kg m**-3), interpolation_aux_geo.R (orog and lsm read from the first time step of the
  2007 file: "no need to go through years 2008-2016, lsm and orog don't change"), split_data_by_validHour.R (time =
  "valid time of forecasts and observations, UTC"), data_retrieval/forecasts/retrieve_*.py (TIGGE, 00 UTC init, steps
  36/48, 50 perturbed members, 0.5 deg grid; params 146/147/165/166/168/176/177/228039), data_retrieval/observations/
  buildDB_temp.R (DWD hourly TT_TU at hours 0 and 12, only -999 removed, no use of DWD's quality flags; station
  altitude/lat/lon from DWD's TU_STUNDENWERTE_BESCHREIBUNG_STATIONEN.txt, the station list at download time),
  RL18_replication.ipynb (reads data_RL18.feather, drops sm_mean/sm_var, uses `_var` as published).
- Measurements on the raw file (1,808,942 x 43) and on the definition's frame via dataset_io.from_definition
  (1,081,262 x 43: 41 float64, `date` datetime64, `station` category; sorted by date).

COLUMN TABLE
(known at prediction? = known at the 00 UTC start of the run, 48 h before the valid time `date`; the ENS is
disseminated some hours after 00 UTC, which the use case's "when the 00 UTC run is in" already says.)

column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule
t2m_obs (target) | DWD hourly 2 m temperature TT_TU at 00 UTC of `date`, deg C, 0.1 resolution; rows with -999 dropped by the source | label, known at the valid time | float64; 544 values, -27.3 to 30.4; no missing; one fill 0.0 (station 254, 2016-08-25, neighbours 18.1 / 18.2, forecast 19.8, AUGUST TEST WINDOW) and one stuck run (station 288, 11.3 for 2014-12-20..31, forecast -3.0..9.4) | cleaning problem | CLEAN-11, CLEAN-15
date | valid time of forecast and observation, 00 UTC (tz dropped) | yes (the target day is fixed when the forecast is made) | datetime64; 3,651 days 2007-01-03..2016-12-31; also the split's time column | fine | USE-6, CLEAN-14
station | the deposit's station index 1..535 (contiguous; 536, 537 have no rows), not the DWD station number; renumbered DWD stations | yes (static) | category, 535 levels; dtype probe numeric_levels answered: an id, categorical by meaning; Spearman with lat/lon/alt -0.06/-0.05/0.07 (no geographic order) | fine (note: "the source's integer id" is the deposit's index) | CLEAN-14, LEAK-34
t2m_mean, t2m_var | mean / variance of the 50 ENS members of 2 m temperature at step 48, bilinear to the station, deg C / deg C^2 | yes | float64; mean -21.6..26.2; var 0.0038..40.1 (40.1 on 2010-02-04 at many stations: a real spread day) | fine | LEAK-37, USE-6
cape_mean, cape_var | CAPE, J kg-1 (J^2 kg-2), nearest grid point | yes | float64; 43,976 rows (2.4%) at -4.5e-13 (float residue of an all-zero ensemble), 6.4% exact 0 | fine (optional: clip the -4.5e-13 to 0, a note suffices) | CLEAN-11 (not impossible in substance)
sp_mean, sp_var | surface pressure, Pa (Pa^2), nearest grid point | yes | float64; 84,209..104,704 Pa; var median 10,617 Pa^2 = sd 103 Pa (1 hPa): proves variance, as sd it would be 103 hPa | fine | CLEAN-1
tcc_mean, tcc_var | total cloud cover, percent 0-100 (%^2), nearest grid point | yes | float64; 0..100 | fine |
u_pl850_*, v_pl850_* | u / v wind at 850 hPa, m s-1 (m2 s-2) | yes | float64; plausible ranges | fine |
q_pl850_mean, q_pl850_var | specific humidity at 850 hPa, kg kg-1 (var ~1e-7) | yes | float64; tiny var scale, numeric, fine for every model family (the pipeline scales) | fine | CLEAN-2
u_pl500_*, v_pl500_* | u / v wind at 500 hPa, m s-1 | yes | float64 | fine |
gh_pl500_mean, gh_pl500_var | geopotential height at 500 hPa, gpm (gpm^2); var median 131 = sd 11 gpm | yes | float64; 4,981..5,942 | fine |
sshf_*, slhf_* | surface sensible / latent heat flux accumulated over steps 0-48, J m-2, ECMWF sign (downward positive: slhf negative 99%) | yes (a forecast accumulation, not an observed window) | float64 | fine | LEAK-10 (window is the forecast's, not the outcome's)
u10_*, v10_* | 10 m wind u / v, m s-1 | yes | float64 | fine |
ssr_*, str_* | net short-wave / long-wave radiation at the surface accumulated 0-48 h, J m-2 (ssr 9.6e4..5.5e7) | yes | float64 | fine |
d2m_mean, d2m_var | 2 m dew point, KELVIN (only t2m was converted to C), nearest grid point | yes | float64; 247..294 K; d2m above t2m by >1 C in 0.09% of rows (bilinear t2m vs nearest-point d2m, ensemble means), not impossible | fine (unit noted in the definition) | CLEAN-21 (one unit per column holds)
sm_mean, sm_var | soil moisture, kg m-3 (R script comment, TIGGE 228039), nearest grid point; NA where the nearest point is sea in the model's land-sea mask | yes | float64; 43.6..755.7; missing 6.6%: 2014-03-06..07-04 all stations; 17 stations always; PLUS 9,891 rows at 11 Baltic-coast stations by model period (see problem 3); missing kept: right | fine as data; NOTE INCOMPLETE | CLEAN-10 (no proxy), LEAK-10 (not outcome-driven: probe R^2 -3.1)
lat, lon | station latitude / longitude, deg, from DWD's station list at download (about 2017) | yes (static; for early rows the list may postdate a relocation, no outcome information) | float64; constant per station; 533 values for 535 stations, no two stations share both | fine | LEAK-10 clause on lookups does not bite: the value does not move with the outcome
alt | station altitude, m, same DWD list | yes | float64; 0..2964; four stations at 0 m are real (three light-ship / platform positions in the North and Baltic Sea, Emden) | fine |
orog | model orography at the nearest 0.5 deg grid point, m, taken from the first time step of the 2007 (pre-2010 cycle) file and assumed constant | yes (static) | float64; -1.43..1268; 207 values (grid points); stale for the 2010 and 2016 model cycles, still a fixed station property | fine (note the vintage) |

Dtype probe: rerun: 1 of 41 columns flagged, `station` (numeric_levels) - an id, category
is right (CLEAN-14). No ordinal scale, no coded column, no 0/1 flag, no open-ended count, no proxy missing code in any
feature (min values checked: none at -999/-9/99). No column to drop (CLEAN-3/5): no constant or copied column; `station`
and `date` carry meaning.

PROBLEMS, RANKED (principles.md: P4 before P7; within P7 by effect)

No P1-P6 problem from this role. Specifically checked and cleared (P4):
- Timing: every forecast field is step 48 of the 00 UTC run (split_data_by_validHour.R, data_preparation.R); the
  accumulated fluxes cover the forecast's 0-48 h, not an observed window ending at the outcome. No column is a lag or
  an aggregate of `obs`.
- Missingness: soil moisture is missing by date block and by grid point, never by the outcome; the leak probe's
  indicator alone scores R^2 -3.1.
- Identifiers: `station` is an index with no geographic or label order; (station, date) is unique.
- Station metadata from DWD's current station list (LEAK-10 lists "attributes looked up after the outcome"): the
  position does not move with the temperature, and the test year 2016 is next to the download; not a leak.

1. P7, CLEAN-11 (Should) -> CLEAN-15: an impossible TEST label. Station 254, 2016-08-25 (August window, split 1):
   t2m_obs = 0.0 between 18.1 (08-24) and 18.2 (08-27; 08-26 missing), ensemble mean 19.8, spread 0.72 C^2. It is the
   only isolated 0.0 in a warm forecast outside the Zugspitze (station 390, where 0.0 is as common as its neighbours
   -0.1 and 0.1: 21 against 25 and 14). The source keeps every value except -999 and ignores DWD's quality flags.
   Effect: about 19.5 C on one of 6,967 rows, +0.0028 MAE to every model in that window (rankings barely move, but it
   is a wrong label, and the airqo precedent removes such labels from test windows too).
   Remedy (mildest): in `_clean`, set t2m_obs missing for (station 254, 2016-08-25) and drop the row, guarded at 1 row,
   with a note; or a general rule "isolated 0.0 more than 15 C from both neighbouring days and from t2m_mean", which
   catches exactly this row (no other |obs - t2m_mean| > 15 row is a 0.0 fill: the other two are a mountain inversion
   and a foehn night, real).
2. P7, CLEAN-11 (Should): a stuck sensor in training. Station 288 reads 11.3 C on 12 consecutive nights, 2014-12-20
   to 12-31, while its forecast runs 9.4 down to -3.0 (11.8 the night before, 3.0 the next reading on 2015-01-06).
   Twelve identical 0.1 C readings at 00 UTC in a winter cold spell are impossible. 6 to 7 of these rows are in each
   sampled train side; negligible effect on scores. Remedy: set missing, rows leave (CLEAN-15), guarded at 12; or keep
   with a note if the curator prefers no hand list. (Other runs: at most 5 identical nights, station 60 at 4.6 C on
   2014-01-01..05 within a forecast of 1.8..7.0, plausible; left alone.) A screen for isolated day-to-day residual
   jumps above 10 C finds 61 rows, all mountain, inversion or foehn nights that look physical: no further cleaning.
3. P7 / writing (claim accuracy), Should: the soil-moisture note and Decision 2 say "missing at every station from
   2014-03-06 to 2014-07-04 and always at 17 coastal and island stations". Measured: 9,891 further missing rows
   (0.55% of the file) at 11 Baltic-coast stations, by model period, which coincide with ECMWF ensemble resolution
   upgrades (land-sea mask of the nearest grid point changed; upgrade dates from memory, not verified):
     - stations 11, 127, 128, 424: missing for valid dates 2007-01-03..2010-01-28, present from 2010-01-29;
     - stations 147, 153, 203: missing 2007-01-03..2010-01-28 and again from 2016-03-11;
     - stations 171, 333, 399, 401: present until 2016-03-10, missing from 2016-03-11.
   So 7 stations (147, 153, 171, 203, 333, 399, 401) have soil moisture in every training year 2010-2015 (bar the 2014
   gap) and none in all three test windows: a real, operational covariate shift (a model upgrade), not a leak, but the
   curator should read it in the notes. Test-window rows without soil moisture: 4.2%; train sides 6.6-6.8%.
   Remedy: correct the curation_comments bullet and Decision 2's description (e.g. "always at 17 coastal and island
   stations, and at 11 Baltic-coast stations in the periods before 2010-01-29 or from 2016-03-11, when the model's
   land-sea mask at their grid point changed"). Keep the values missing (right).
4. P7 / writing, Weigh (notes only, no data change):
   - Units note: add sm in kg m-3 (and cape J kg-1, q kg kg-1, winds m s-1); the variance columns are in squared units.
   - "interpolated to the station" (task_summary.row, curation_comments): only t2m is bilinear; the other 17 fields
     are the nearest 0.5 deg grid point, shared by the stations of a grid box (2016-12-20: 500 stations, 212 distinct
     sp_mean values; t2m_mean unique per station). This also explains d2m in kelvin (only t2m was converted).
   - `orog` is the model orography of the 2007 cycle at the nearest grid point, held constant through the 2010 and
     2016 upgrades.
   - `station` is the deposit's station index 1..535 (renumbered), not the DWD station number; the DWD number and
     name are in the source's netCDF, not needed.
   - lat/lon/alt come from DWD's station list at download (about 2017).
5. P7, CLEAN-11 (Weigh, optional): cape_mean holds -4.5e-13 on 43,976 rows (2.4%), the float residue of a mean of
   zeros; physically 0. Harmless (a model can split 0 from -4.5e-13 only on noise); a `clip(lower=0)` is cheap and
   safe, a note suffices.

On `_var` (asked by the main session): the variance, by the R code (`apply(x, c(1,3), var)` for every variable, which
writes these names) and by the magnitudes (sp_var median 10,617 Pa^2 = sd 1.03 hPa; as an sd it would be a 103 hPa
spread at 48 h; gh_pl500_var median 131 gpm^2 = sd 11 gpm). The paper and its network code use the standard deviation;
the deposit's own replication notebook uses `_var` as published. Keeping it is lossless and documented (correct
name, correct note); a sqrt would be a modelling transform the pipeline need not get (CLEAN-2 spirit). Verdict: fine.

Not checked: DWD's own quality flags (QN_9) for the target, which would let the impossible labels be found by the
data owner's rule rather than by hand (PROV-13: a repair from the origin; heavy, a rebuild of the target from DWD CDC
hourly files, not proposed for two rows); the ECMWF upgrade dates behind problem 3.
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR REPORT: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany), 2026-11-08

VERDICT: right with notes.
The regime, the gap, the train sides and the history are right, with numbers below. The window length is the open
weighing call (builder's issue 1). The shipped option (a) is right by rule order (SPLIT-18 comes before SPLIT-19) and by
the precedents. The measurements below give the curator one fact that sets this case apart from
climate_model_weather_forecasting: on this data a refit every two weeks gains next to nothing. They also show that the
42 test days are a thin and somewhat lucky sample of the year. Nothing breaks a Must.

Work: scripts and logs (s1_structure, s1b_break, s2_models, s3_analyse, s4_year_feature;
predictions in s2_preds.parquet). Paper text: arXiv 1805.09091, read in full. Source code: slerch/ppnn
nn_src/utils.py get_train_test_sets. One fixed set of models in every design:
  raw ensemble mean; ensemble mean + station mean error; per-station linear MOS; ridge on all inputs;
  LightGBM (500 trees, lr 0.1, 127 leaves); and LightGBM's rf mode (100 trees, 1023 leaves, feature fraction 0.5),
  a deliberately weak fourth family, weaker than the probe's RF.
Train side in every design: a random 1M of the rows valid at least 3 days before the window, as the shipped splits
build it. Design A uses the plan's own sampled train sides.

------------------------------------------------------------------------------------------------------------------
CHECKS THAT PASS
------------------------------------------------------------------------------------------------------------------
1. Regime (SPLIT-1, SPLIT-3, SPLIT-13, USE-10): temporal over known stations, as the use case implies (the service
   corrects the forecasts of its own stations).
   - Test rows whose station has no training rows: 0, 0 and 1 (Dec, Aug, Apr).
   - Test rows whose station has under 365 training rows in the sampled side: 42, 28 and 29 of about 7,000 per window.
   - No grouped or IID alternative applies; no hidden-group question arises.
2. Time column and gap (SPLIT-9, SPLIT-10): `date` is the valid time, 00 UTC on every row; the prediction point is 48 h
   earlier.
   - The last training date is the window start minus 3 days in all three windows (2016-12-15, 08-15, 04-15).
   - This is exactly the source's rolling code: get_train_test_sets(fclt=48) trains on
     [date_idx - 2 - window, date_idx - 2), with the stop index exclusive.
   - The label of day D-2 is observed at 00 UTC of D-2, before the run started then is out, so the gap is one day
     longer than it needs to be. That is conservative and faithful to the source.
   - No training row has a label unknown at the prediction point. There is no weight and no time on risk.
3. Windows (SPLIT-11, SPLIT-14, SPLIT-17): newest first, 14 days each, 6,936 to 7,003 rows, 499 to 501 stations.
   - The pools before the budget hold 1,679,500 to 1,800,940 rows, 92.8% to 99.6% of all rows (floor 50%).
   - Every window has its own train side. The sides share 933k to 967k rows, from the one random order, as designed.
4. Training history (SPLIT-20): every year 2007-2015 is in every train side, about 94k to 110k rows a year. 2016 adds
   31k, 65k and 96k rows (Apr, Aug and Dec windows).
   - This matches the source, which trains on 2007-2015 and finds that more years help the nonlinear models (Sect.
     5.1: +4-5% skill).
   - Check for a break at ECMWF IFS cycle 41r2 (8 March 2016, ensemble upgraded to 18 km). The 30 days after against
     the 30 before: t2m_var x0.857, against x0.795 to x1.107 at the same dates in 2008-2015. The spread-to-error ratio
     after the date is 0.161, against 0.133 to 0.240 in other years. No step. 2016's April to August spread is the
     lowest of the decade (0.46-0.59), but its raw error is also the lowest (1.27-1.38 against 1.45-1.65 for those
     months in other years): calm weather, not a system break.
   - The soil-moisture outage (all stations, 2014-03-06 to 07-04) lies inside the train sides only.
5. Season (SPLIT-20): the windows fall in spring, summer and winter, not all in the Christmas weeks. The raw forecast's
   MAE on the 42 test days is 1.448, against 1.441 for all of 2016.
6. Date as a number: dropping `year` from the inputs moves LightGBM by -0.025 / +0.038 / -0.006 and the rf mode by
   +0.016 / +0.004 / +0.027. Mid-year refits create no artefact through the year axis.

------------------------------------------------------------------------------------------------------------------
PROBLEMS AND NOTES, ranked (all P4; none is a Must)
------------------------------------------------------------------------------------------------------------------
1. P4, SPLIT-18 (Should) against SPLIT-19 / SPLIT-12 (Should): the window length. A weighing call for the curator
   (builder's issue 1). Measured facts for both sides:

   a) Refit gain: the same model refit at each window start, against one fit on 2007-2015 (the source's design).
      Values are the fixed fit's MAE minus the refit's; + means the refit helps.
                            raw  st.offset   MOS    ridge   rf-mode  LightGBM
      shipped 2016-12-18   0.000  -0.003   +0.004  +0.013  +0.101   -0.013
      shipped 2016-08-18   0.000  -0.001   -0.003  +0.006  +0.004   +0.006
      shipped 2016-04-18   0.000  +0.001   +0.001  +0.006  +0.014   -0.016
      end-2016 12-18       0.000  -0.004   +0.002  +0.013  +0.092   -0.001
      end-2016 12-04       0.000  -0.001   +0.001  +0.022  +0.111   +0.071
      end-2016 11-20       0.000  +0.002   +0.004  +0.018  +0.065   +0.034
      - On the shipped windows, LightGBM fitted once in December 2015 does as well as the two-weekly refit.
      - Over all six windows LightGBM gains +0.014 on average (1.3% of its MAE), MOS +0.002 and ridge +0.013.
      - This replicates the source: fn. 4, rolling EMOS gives "only marginal improvements"; Sect. 6, updating the
        network "each day ... found no improvements".
      - SPLIT-18's reason is that short-lived quantities need frequent refits. That reason carries little weight on
        this data. The fact sets the case apart from climate_model_weather_forecasting, whose curator reason was
        "TabRed uses 1 month refit horizon. For weather this is a bit much" with no measurement of the refit gain.
      - The source itself says online updating "could be more relevant in an operational setting" when model versions
        change. That argues for short windows.

   b) The weight of 42 test days, from one fit on 2007-2015 scored on the 26 14-day blocks of 2016:
      - Per-day LightGBM minus MOS: SD 0.202, lag-1 autocorrelation 0.28. The SE of a model difference is about 0.04
        on 42 days and about 0.014 on the year.
      - Over all 2,600 choices of 3 of the 26 blocks:
        - the full order of the six models equals the year's in 21.2%; for the 9 choices four months apart, as
          shipped, 4 of 9;
        - ridge against MOS (0.014 apart over the year) flips in 29.7%, MOS against the station offset in 13.4%, and
          the rf mode against ridge in 8.5%;
        - LightGBM against any other model never flips.
      - Close models (tuned GBMs a few hundredths apart) will be ranked by about 42 days of weather.

   c) The shipped windows overstate the nonlinear lead. The same fixed fits give LightGBM minus MOS -0.265 on the
      shipped 42 days, against -0.184 over all of 2016. The late-August window alone gives -0.371 under refits.
      Mean MAE per design:
                                   raw   st.off   MOS   ridge  rf-mode LightGBM  LGBM-MOS
      A shipped (3 x 14 d, 2016)  1.448  1.351  1.297  1.318  1.417   1.040    -0.257
      B years 2014/2015/2016      1.478  1.347  1.299  1.307  1.354   1.113    -0.186
      C last 6 weeks of 2016      1.456  1.387  1.407  1.397  1.465   1.219    -0.188
      Per window (MAE):
        A: Dec 1.145 / Aug 1.016 / Apr 0.959 (LightGBM); MOS 1.322 / 1.387 / 1.181
        B: 2016 1.085 / 2015 1.161 / 2014 1.094; MOS 1.269 / 1.373 / 1.253
        C: Dec 18 1.133 / Dec 4 1.285 / Nov 20 1.238; MOS 1.324 / 1.514 / 1.385
      A and B give the same mean order of the six models (LightGBM, MOS, ridge, station offset, rf mode, raw). C, the
      strict precedent of the last weeks, does not: MOS falls below the station offset and ridge, and the rf mode falls
      below raw. This supports the shipped spacing over C (SPLIT-20).

   Reading: these are comparisons over a few windows, and by SPLIT-21 they decide nothing. They are given as facts
   (refit gain; sampling noise of the test pool), not as a score of a design.
   - Shipping (a) is right by rule order and precedent (climate_model_weather_forecasting_1m: weekly windows;
     bias_correction_r_bias_correction_r_2: weekly windows; aeolus: two weeks).
   - If the curator prefers the source's design, it is an exception to SPLIT-18. The fact: the refit gain is near zero
     (source, Sect. 6 and fn. 4; here -0.016 to +0.006 for LightGBM on the shipped windows). It serves P4: the test
     stands for a full year of the service's operation, with 8.7 times the test days.
   - The mildest form of that exception: the source's own test year in three windows, 2016-01-01, 05-01 and 09-01,
     about 60k rows each, each trained on everything before it. It keeps the source's test set, comparable to Table 2,
     and its training regime, and meets SPLIT-14. Option (b) instead tests on 2014 and 2015, which the source never
     tested, and the 2014 test year holds the soil-moisture outage at every station for 121 days, an input pattern that
     training sees only at 17 coastal stations. Not fitted; by (a) above it would score close to B-2016's fixed fit.

2. P4, SPLIT-20 (Should), note: what the windows weigh. There is no autumn window (September to November).
   - The late-August window sits in 2016's late-summer warm spell: the raw ensemble is too cold (mean error -0.72 in
     August, -1.00 in September), giving the hardest raw window (1.642).
   - Nonlinear corrections gain most there (LightGBM 1.016 against MOS 1.387), which is the source of 1c.
   - Remedy: a sentence in splits_comment ("the August window falls in a late-summer spell with the ensemble too cold,
     where nonlinear corrections gain most"). No change to the split.

3. P4, SPLIT-10, wording only: the splits_comment says "at the prediction point of a window's first day, the
   observations of the two days before it are not yet in".
   - Only D-1's observation is missing then. D-2's is observed at the run's start time, 00 UTC of D-2.
   - The code leaves out both days, as the source's code does. The gap stays.
   - Remedy: reword to "the day before is not yet observed; as in the source's code, training stops two days before
     the window".

No other finding:
- no row whose label is unknown at the prediction point;
- no time-on-risk weight;
- no hidden groups (temporal);
- no break in the history;
- no season-shaped test (the windows are spread out);
- the budget sampling keeps every year.
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER REPORT: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany)
2026-11-08. Actor: the post-processing team of a national weather service (DWD). When the 00 UTC ECMWF ensemble run
arrives (disseminated a few hours later), we correct its 48 h 2 m temperature forecast at each of our stations and
issue the result in the station forecast product (MOSMIX-style point values, plus event probabilities).

VERDICT
- Fit: DIRECT (agree with the definition). Every input is a forecast for the valid time or a fixed station property
  that I hold when the 00 UTC run is in, the row is one value of my station product (one station, one valid time, one
  lead), and the test is the stations I already serve on later dates, which is what I face (USE-1, USE-3, USE-6,
  USE-8, USE-10).
- Metric: PARTLY, close to yes. MAE scores the point temperature I issue, and it is the CRPS of a point forecast. It
  does not score the uncertainty I also issue (frost and threshold probabilities, quantiles). Within a point-value
  regression protocol I would choose MAE myself (MET-1, MET-11 stand-in). If the protocol took a distribution or
  quantiles I would choose the CRPS, the source's one criterion (MET-5, MET-8).
- Test windows: the year 2016 (or the yearly windows 2014-2016) is how I verify and how often I retrain. But I
  measured that the refit cadence the shipped windows imply changes the score by at most 0.004 °C. The shipped
  two-week windows also sit at the year's level of difficulty. So the choice affects how many days are tested, not
  the task itself.

1. AT THE PREDICTION POINT, DO I HAVE THESE INPUTS?
- Yes, every one. The 18 ensemble means and spreads come from the 00 UTC run I am correcting (USE-6: the forecast the
  task corrects is its input). Lat, lon, altitude, model orography and the station id are fixed. The valid date and
  season are known. No input is a lag of the observation (TP-10 leg 2; builder probe).
- The `_var` columns hold variances, not standard deviations. That makes no difference to me: they are the same
  information.
- Soil moisture is missing for four months of 2014 and always at 17 coastal or island stations. This matches what an
  operational feed looks like (a field the model leaves out over sea points). Leaving it missing is right (USE-7: only
  the corrected forecast t2m_mean is needed on every row, and it is).
- Missing inputs I always have operationally (ranked by value at a 48 h lead):
  a) The station's own recent forecast errors (the error of runs verified up to D-2 00 UTC) and the latest observation
     at the start time. Rolling-window EMOS uses the first. DWD's MOS uses the second, but Hess (2020) finds
     persistence "an excellent projection" only up to about 4 to 6 h. Rasp and Lerch footnote 4 (Sect. 5.1) find
     rolling windows give "only marginal improvements". So the value at 48 h is small. Leaving them out also keeps the
     task post-processing, not forecasting from lags (SEL-11, TP-10). No change asked.
  b) The 50 raw members (published in the Chen and Lerch 2022 copy of these rows), the deterministic HRES run, and a
     second model (ICON). MOSMIX blends ECMWF-MOS with ICON-MOS. These are refinements: the paper's own inputs are
     the ensemble mean and spread. No change asked (PROV-6 choice already made).
- Timing detail (the claim auditor's finding 25): the 2-day gap excludes training rows valid on D-2, but I hold the
  D-2 00 UTC observation when I post-process the D-2 00 UTC run. The gap is one day more conservative than my
  situation. That is harmless.

2. IS THE TARGET WHAT I ACT ON?
- The target is the observed 2 m temperature at the station at the valid time, in °C, with no transformation. That is
  exactly the quantity my product states (USE-5). It is not a proxy.
- What I would want: a value AND its uncertainty. DWD's Ensemble-MOS (Hess 2020) issues point values from linear
  regression, fitted by RMSE and verified with MAE for ECMWF-ENS 2 m temperature (Fig. 11). Event probabilities come
  from logistic regression. MOSMIX gives point values per station. So a point forecast is a product I really issue.
  The source's predictive distribution is the research version of the second half.
- The gap is named in `changes` and `fit_reason`. It does not make the fit approximate, because the point product is
  itself a well-defined real use case with these features (USE-9).

3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST WHAT I FACE?
- One row is one station x valid date at 48 h lead and 00 UTC valid time: one value I issue. Each row is a decision of
  its own, with nothing repeated by protocol, so a per-row score is right (MET-17 does not apply). My real product
  covers every lead and hour. This dataset is one slice: the night-time (00 UTC) value at day+2, which includes
  radiation nights and inversions, the hard frost cases. That is narrow but real.
- Entities: these are known stations predicted on future dates (USE-10). Temporal splits are right. Only 1 test row
  in the April window belongs to a station with no training rows; 14-28 rows per window belong to stations with under
  a year of history (builder). This matches the occasional new or short-lived station I meet.
- Non-stationarity: ECMWF upgraded the IFS to cycle 41r2 on 8 March 2016 (ENS from about 32 km to about 18 km). All
  three test windows come after it and most of the training rows come before it, as also happens in the source's
  2016 test year. This is realistic: it is exactly what my correction meets after an upgrade. It is no defect, and it
  is a reason to trust a model that holds up across the windows.
- Retraining cadence: DWD does not refit every two weeks. MOSMIX trains on more than 10 years of data (EMS 2014). DWD's
  study (Lang et al. 2020, cited in arXiv 2401.11896) found multi-year training better than sliding-window training,
  even across NWP model changes. The source trains once on 2007-2015, and daily updating gave "no improvements"
  (Sect. 7, not Sect. 6 as the definition says). So my real protocol is: train on all earlier years, verify the next
  year by season. That is option (b), the years 2014, 2015, 2016 (SPLIT-19 with the source's design).
- Does the shipped choice change my task? I measured it on the raw file (refit.py). For each shipped window I trained
  once on 2007-2015, then refit up to the window minus 2 days. MAE in °C, station offset / per-station linear MOS:
    Apr 2016: once 1.123 / 1.183, refit 1.122 / 1.181 (raw 1.280)
    Aug 2016: once 1.594 / 1.384, refit 1.594 / 1.386 (raw 1.642)
    Dec 2016: once 1.332 / 1.324, refit 1.336 / 1.322 (raw 1.423)
  The difference is at most 0.004. So "refit every two weeks" against "train once a year" is immaterial here. The
  windows are also at the year's level of difficulty. Mean over the windows against the whole of 2016 trained once:
  raw 1.448 vs 1.441, station offset 1.351 vs 1.316, MOS 1.297 vs 1.269. The real cost of the shipped design is
  statistical. A window has 14 days, and the errors of about 500 stations on one day are correlated (one weather
  situation covers Germany), so each window holds about 14 independent situations, not 7,000. Close models could
  swap ranks on one cold spell. The big gaps (LightGBM 1.03-1.12 against MOS 1.30) are safe.
- As the actor I would pick the yearly windows (b). They show every season and are how I verify. If SPLIT-18 is kept
  (rule order and the climate_model_weather_forecasting / bias_correction precedents), the text should not claim a
  practice that weather services do not have. The `split` field says "as for a correction refit every two weeks". I
  would write something like "a correction trained on the earlier years, scored on two weeks in each of three
  seasons". SPLIT-18's reason, short-lived quantities, fits forecasting from lags. Here each row brings its own fresh
  forecast, so the reason is weaker (SPLIT-20: decide the history from the use case). Either way, this is a curator
  weighing call (builder issue 1). By SPLIT-21 it must not be settled by the numbers above, which only show that the
  two options mean the same task.

4. WOULD I USE THIS MODEL? WHAT WOULD MAKE ME TRUST OR DISTRUST IT?
- Yes. These are the inputs I use, and the gains are the ones I look for. Per-station linear MOS (my classical
  baseline) scores 1.297. LightGBM with 1000 trees scores 1.033, better on 3 of 3 windows (builder skill_vs_raw.json).
  The source's networks beat local and boosted EMOS by CRPS. A tabular model that beats MOS by about 0.25 °C MAE
  would interest any MOS group.
- Trust would come from:
  - stable gains in every season and after the model upgrade, which the three windows partly show;
  - no degradation at stations with short history;
  - sensible behaviour on cold, clear nights (inversions), the costly errors at 00 UTC;
  - for my probabilistic product, a calibrated spread, which this task cannot show.
- Distrust would come from a ranking resting on 42 test days, and from any dependence on `date` as a raw trend that
  would not carry over to the next year. The `date` input is legitimate (season, model-cycle era) but invites
  extrapolation in time.

5. DOES THE DECLARED METRIC SCORE MY DECISION?
- PARTLY (close to yes). `mae` in °C, per row, unweighted, at my unit (a station value):
  - It is the verification score DWD reports for ECMWF-ENS 2 m temperature (Hess 2020, Fig. 11). It is the absolute
    error the public sees.
  - It equals the CRPS of a point forecast (source Appendix B, MET-11 stand-in).
  - It rewards the median, the right point under absolute loss.
  - The claim auditor measured Kendall tau(MAE, CRPS) 0.944 / 0.989 / 0.944 over 10 models, with the same best model
    in all 3 windows. RMSE scores 0.989 / 0.944 / 0.899. So MAE ranks models as the source's CRPS would, slightly
    better than the RMSE fallback.
- What it misses: the uncertainty half of my product (the source's predictive distribution, my threshold
  probabilities). That half needs the CRPS of a distribution, or the mean pinball loss over a quantile grid, which the
  regression protocol does not take.
- MET-6 and MET-7 do not apply: there is no threshold or cost matrix. A frost-warning threshold would be a separate
  task, and the source fixes none. MET-8 and MET-9 are classification rules, not relevant here.
- What I would choose: `mae` as declared under this protocol. With a distribution or quantile protocol, the CRPS.
  RMSE (DWD's fitting criterion) is a close second but further from the source's criterion.

GAPS BETWEEN THE DATASET AND MY DECISION, ranked by how much they change the task
1. A point value instead of a predictive distribution: the uncertainty product is not scored (USE-5, MET-1). Moderate.
   It is stated in `changes` and `fit_reason`, and a point product is real (USE-9).
2. Three 14-day windows instead of a verification year: about 42 independent weather situations against 366.
   The refit cadence is immaterial (at most 0.004 °C, measured) and the windows' level matches the year's. Small for
   the task, moderate for ranking precision. Curator call, builder issue 1.
3. The text claims a two-week refit practice: weather services refit rarely, on multi-year history (MOSMIX more than
   10 years; Lang et al. 2020). Wording only.
4. Recent station errors and the start-time observation are left out. Small at 48 h (Hess 2020; RL18 footnote 4). Kept
   out on purpose (SEL-11, TP-10).
5. One lead and one valid hour: a narrow slice of the product, but a real and hard one (night-time temperature). Small.
6. Gap 2 days where 1 would do: conservative, no effect on validity. Negligible.

WHAT AN EXPERT WOULD CHANGE
- Prefer the source's yearly test (option b, 2014-2016), or record clearly why SPLIT-18 wins. Either way, reword
  `task_summary.split` so it does not describe a two-week refit.
- Keep `mae`. Add the measured MAE-CRPS closeness (the claim auditor's tau 0.94-0.99) to the metric reason, as MET-11
  asks for a stand-in.
- Fix the citation: daily updating is in Sect. 7 (Discussion), not Sect. 6 (Decision 1 text).
- In `use_case`, optionally name the real products this mirrors (DWD MOSMIX / Ensemble-MOS point temperature) to
  anchor the point-value framing.
- No change to the inputs, the target, the row unit or the station handling.

SOURCES USED
- Rasp and Lerch 2018, MWR 146(11), arXiv 1805.09091 (HTML full text): Sect. 2.1 (00 UTC start, 48 h lead, 2016 set
  aside "to mimic operational conditions"), Sect. 3.1 (fixed training periods), Sect. 5.1 footnote 4 (rolling EMOS
  marginal), Sect. 7 (daily updating no improvement), Table 2 (mean CRPS).
- Hess 2020, "Statistical postprocessing of ensemble forecasts for severe weather at Deutscher Wetterdienst", NPG
  27:473 (https://npg.copernicus.org/articles/27/473/2020/): point values by linear regression fitted by RMSE, MAE
  for ECMWF-ENS 2 m temperature, probabilities by logistic regression, persistence useful only to about 4-6 h.
- EMS 2014 DWD presentation on MOS (https://presentations.copernicus.org/EMS2014/EMS2014-280_presentation.pdf):
  MOSMIX trained on more than 10 years, RMSE falls with longer training. arXiv 2401.11896 (wind gusts, DWD): multi-year
  training beats sliding windows (Lang et al. 2020).
- ECMWF IFS cycle 41r2 (https://confluence.ecmwf.int/display/FCST/IFS+cycle+41r2+resolution+changes): implemented
  8 March 2016, ENS resolution about 18 km.
- Builder report and skill_vs_raw.json, README decision table 1, claim auditor report (findings 23b, 25, 27).
- My measurement: refit.py on data_RL18.feather (numbers above).
- Rules: USE-1, USE-3, USE-5, USE-6, USE-7, USE-8, USE-9, USE-10; MET-1, MET-5, MET-6, MET-7, MET-8, MET-11, MET-17;
  SPLIT-18, SPLIT-19, SPLIT-20, SPLIT-21; SEL-11, TP-10.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: ppnn_ecmwf_t2m_postprocessing_germany
Inputs: the clean room's data sample and task description, the public sources linked there (GitHub slerch/ppnn, the arXiv
1805.09091 HTML, and figshare API metadata), and the original source file data_RL18.feather (figshare 13516301,
md5 18bb8d47... checked), downloaded. I opened no other local files.

VERDICT: Include with changes. This is a real, well-known, useful post-processing task with strong signal and no
feature leakage. The test design needs fixing: three 14-day windows are too short to score reliably. The row
reduction from the source also needs to be documented and checked.

WHAT THE TASK IS
Statistical post-processing (model output statistics, MOS) of ECMWF 50-member ensemble forecasts of 2 m temperature
at about 535 German DWD SYNOP stations. Lead time is 48 h, with forecasts started at 00 UTC and valid at 00 UTC.
Each row is one station and one valid date (2007-01-03 to 2016-12-31). The features are the ensemble mean and
variance of 19 forecast variables, plus the station's lat/lon/altitude/model orography. The target is the observed
temperature. A national weather service or private forecaster makes this prediction every day, two days ahead, to
issue corrected station forecasts. The use is real and operational. Source: Rasp & Lerch 2018, MWR, "2-meter
temperature forecasts at surface stations in Germany at a forecast lead time of 48 h", with "available from
3 January 2007 to 31 December 2016". The paper trains on 2007-2015 and tests on 2016. The data is real; its license
is CC BY 4.0.

CHECKS THAT PASSED
- Real data with the right target. All 200,000 sampled rows match the source file exactly on (date, station):
  t2m_obs == obs, and the features match with max abs diff 0.
- No duplicate rows and no duplicate (date, station) pairs. Each station has one set of lat/lon/alt/orog values,
  and no two stations share coordinates.
- No feature leakage. Every feature is either a forecast available at issuance (D-2, 00 UTC) or a static station
  attribute. There are no lagged observations.
- Values are plausible: obs ranges from -27.3 to 28.7 C, the -27.3 at the 2964 m station (Zugspitze). The *_var
  columns are ensemble variances, not standard deviations: q_pl850_var is about 1e-6 when q is about 4e-3.
- Signal is strong and the task is not trivial. I trained on all sampled data up to 2 days before each window.
  RMSE per window (Apr / Aug / Dec 2016):
      raw ensemble mean      1.63 / 2.16 / 1.89
      + per-station bias     1.37 / 2.08 / 1.76
      LightGBM (all feats)   1.20-1.24 / 1.50-1.56 / 1.43-1.47
  R2 rises from 0.72/0.60/0.76 for the raw forecast to 0.85/0.79/0.86. Models have room to differ.

CONCERNS, MOST SERIOUS FIRST

1. The test windows are too short, so scores will be noisy.
   Evidence: in the sample, the three over-represented blocks are 2016-04-18..05-01, 2016-08-18..08-31 and
   2016-12-18..12-31. Each is exactly 14 days. In the source these windows hold 6,936, 6,967 and 7,003 rows, but
   only 14 distinct weather days each, so 42 test days in total. The paper tests on all 366 days of 2016. Errors are
   strongly clustered by day and synoptic regime, so the effective test size is closer to 14 than to 7,000. In my
   runs the best model changed between windows: residual-target LightGBM won in Apr and Dec, station-categorical
   LightGBM won in Aug.
   Change: use longer windows, for example 2016 split into three four-month blocks, or expanding-window folds of
   about 2 months each. There is plenty of data for this.

2. The row count is undocumented and inconsistent with the source.
   Evidence: the source has 1,808,942 rows, while task.md says the full data has 1,081,262. The 200k sample is
   11.06% of the source rows (200,000/1,808,942). Per date, it is about 0.110 of source rows in training periods
   but about 0.15-0.24 in the three test blocks. That fits training-period rows being thinned at random to about 60%
   while the test windows are kept whole. task.md does not say this.
   The two days 2016-12-16 and 2016-12-17 are missing completely. That is a 48 h gap, matching the lead time, but
   only before the last window. Before the April and August windows, the sample still has rows on 04-16/17 and
   08-16/17 at normal training density. If those rows are used to train for the following window, the training
   set contains observations that would not yet exist when the D-2 forecast is issued. The effect is small, since
   there are no lagged features, but the splits are inconsistent.
   Change: state the subsampling rule. Apply the 2-day gap before every test window, or none, the same way each
   time. If thinning the training set is meant to keep the table at about 1M rows, say so.

3. The original problem is probabilistic. As prepared, it is point regression.
   Evidence: the source minimizes CRPS ("All network models are estimated by minimizing the CRPS"). Its headline
   numbers are CRPS: raw 1.16, EMOS-loc 0.90, NN-aux-emb 0.78 on 2016. Point regression scored by RMSE is still a
   valid deterministic MOS task.
   Change: none required. Note in the documentation that results cannot be compared with the paper's CRPS.

4. A known bad observation sits in a test window.
   Evidence: station 254 (53.71N 7.15E, 12 m) on 2016-08-25 has obs = 0.0 while the forecast mean is 19.8 C. This
   is the only obs == 0 with forecast > 12 C in the whole source, so it is almost certainly a missing value written
   as 0. It falls in test window 2. On about 7,000 rows it adds roughly 0.02 to RMSE there. The source has 674 rows
   with |obs - forecast| > 10 C. Most look physical (alpine inversions, foehn), so I would not remove them.
   Change: set that single row's target to NaN, or drop the row.

5. Column types need declaring.
   - station is int32 with 534 ids in the sample (474, 536 and 537 are absent; the source has 535). It should be
     declared categorical, or dropped, since lat/lon/alt/orog already identify each station uniquely. A
     categorical station gave a small gain in 2 of 3 windows.
   - date is a raw datetime. It should be the split key only. If models may use it, give day-of-year (or sin/cos)
     instead of the timestamp, because test dates are always outside the training range.

6. Missing values and scaling are minor issues that are already handled sensibly.
   - sm_mean and sm_var are missing in 6.5% of the sample. The source shows soil moisture missing for 35% of 2014
     (Apr-Jun 2014 entirely, Mar 85%), and 16 stations never have it. These are native gaps; keep them as NaN.
   - Feature scales are extreme: sshf_var and ssr_var reach about 6e13, and q_pl850_var is about 1e-6. This is
     harmless for trees but needs standard or quantile scaling for neural networks.
   - cape_mean has tiny negative values (-4.5e-13) and orog has negative values (1,543 sampled rows, sea-level
     stations). Both are fine.

WHAT I COULD NOT CHECK
- I could not see the 1,081,262-row prepared table or the actual split code. The window boundaries, the
  training-set thinning and the gap rule are inferred from sampling densities in the 200k sample.
- I could not fully read the MWR/arXiv PDF text, only the arXiv HTML summary. The figshare HTML pages returned 403;
  I used the figshare API metadata instead.
- I did not check whether DWD obs QC flags exist upstream. I also did not check whether the other two linked
  figshare sets (Chen & Lerch 2022 temperature and wind data) were used at all; the data here matches RL18
  exactly.
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT: ppnn_ecmwf_t2m_postprocessing_germany (t2m_obs, MAE, 3 temporal 14-day test windows in 2016)

Verdict: barely gameable. The only exploit that works with the rows a participant actually gets is joining
forecasts issued after the prediction point, which sit in other test rows of the same window. It gains about
0.006 to 0.015 MAE (about 1%), and the gain is not consistent across splits.

Honest baselines (scored on the shipped splits; MAE, lower is better)
  raw ensemble mean t2m_mean ............ r0 1.4228  r1 1.6421  r2 1.2798
  LightGBM default (100 trees, L2) ...... r0 1.1835  r1 1.3096  r2 1.1254  mean 1.2061  (baseline.py)
  LightGBM L1, 500 trees, 127 leaves .... r0 1.1248  r1 1.1419  r2 1.0218  mean 1.0962  (baseline.py)
  + honest features (H500) .............. r0 1.1096  r1 1.1391  r2 1.0011  mean 1.0833  (honest.py, feats.py)
  + same, 1000 trees lr 0.03 (H1000) .... r0 1.0952  r1 1.1210  r2 0.9823  mean 1.0662  (honest.py)
  The honest features are day of year, t2m-d2m spread, the same-date cross-station mean of t2m_mean/t2m_var and
  the station's anomaly from it, and the station's forecasts valid at d-1 and d-2 (issued at d-3 and d-4). All
  forecasts for day d are issued together at d-2, so the cross-station statistics are legitimate.
  Noise check: the L1-500 baseline plus a random column, 3 seeds, gives means 1.0983, 1.0955 and 1.0975 against
  1.0962. Per split it moves up to 0.007 (r2: 1.0189 to 1.0284). Gains smaller than about 0.005 are noise.

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Same-station forecasts valid d+1, d+2 (issued d-1, d), taken from the other test rows of the window | exploits.py future; exploits2.py wide, f1000 | H500 1.0833 / H1000 1.0662 | 1.0692 (d+1,d+2, 9 vars) / 1.0688 (d+1..d+4 + centred 7-day mean) / 1.0606 (1000 trees) | H500: -0.002, -0.011, -0.029; wide: -0.015, -0.006, -0.023; H1000: +0.006, -0.012, -0.012 | No: issued 1-2 days after the prediction point | Thin the test windows to days at least 3 apart, or accept it as small and documented |

Not reachable in the benchmark: these need test-window labels. The kit ships them, but a participant does not
get them. They are listed only to size what a model updated with fresh observations would gain.
  - Same-station obs residual at d-1 and d+1 (label peeking): 1.0343 vs H500 1.0833 (-0.031, -0.060, -0.056).
  - Rolling station bias, 7- and 30-day mean residual up to d-2 (bias.py rolling): 1.0643 (-0.008, -0.032, -0.033).
    An operational model would know these observations. The frozen 14-day window withholds them by design, which
    is a fair design choice and not a leak.
  - Same-station obs at d-2 to d-4 (exploits.py obslag2): 1.0769 (+0.010, -0.024, -0.006).

FLAWS THAT HURT AN HONEST MODEL
  None of material size.
  - The training sets are capped at 1,000,000 rows. For r0 and r1 the cap drops 7% and 3.5% of the earlier rows,
    and about 44% of the earlier folds' test windows (2016-04-18 to 05-01, 2016-08-15 to 31). Training on every row
    dated before the 2-day gap (fulltrain.py) gives 1.0817 against 1.0833 (r0 -0.003, r1 -0.002, r2 0), which is
    within noise.
  - Shorter recent-only training windows are worse: last 1 year 1.1945, 3 years 1.1217, 5 years 1.0826 (=H500).
    Old rows do not hurt.

MECHANISM AND FIX, EXPLOIT 1
  Every row is a 48 h forecast for one station and valid day d, issued at d-2 00 UTC. A 14-day test window holds
  the same station's rows for d+1 and d+2. Those forecasts were initialised at d-1 and d, so they start from a
  later, better-known state, and their t2m, d2m, cloud and flux fields carry information about day d. Joining them
  by (station, date) gains 0.014 MAE on the 500-tree model and 0.006 on the 1000-tree model. Most of the gain is in
  r2 (spring) and r1 (summer). r0 does not improve with 1000 trees (+0.006), and r0 alone is within noise.
  Mildest fix: keep only test days at least 3 days apart in each window. Rows d+1 and d+2 would then be absent,
  with no change to the columns. The alternative is to accept it: about 1% MAE, and below the gap between model
  sizes.

ATTACKS THAT FOUND NOTHING (vs H500 1.0833 unless stated)
  - Row order: rows are sorted by date and shuffled within a date. The Spearman correlation of in-date position
    with obs is 0.00004, with the residual 0.0007, with the station 0.0006. The next-row residual correlation of
    0.21 comes entirely from rows sharing a date, and those dates are never split across train and test.
  - Formats: t2m_obs is on a 0.1 grid for every row, with a uniform last digit (0.099 to 0.101). Rounding
    predictions to 0.1 gives 1.0832 (no change). The forecast columns are continuous floats with no sentinels.
    sm_mean/sm_var are missing on 6.6% of rows: per station, with a 2014 spike of 35%. The forecast product shares
    that missingness, so it is known at issue time.
  - Copies across the split: no full forecast vector appears twice (0 rows). Train and test never share a date,
    and the test windows are disjoint from training. The 2-day gap is enforced (r0's gap days 12-16/17 are absent
    from the data, r1/r2's are excluded from train).
  - Test-set composition: the number of stations observed on the date (a row exists only once an obs exists)
    gives 1.0864 (+0.003, worse).
  - Single features: the best single feature is t2m_mean (MAE 1.367 on r0), then d2m_mean (1.754). No column
    comes near the full model, and no column is a post-outcome value.
  - Train-vs-test classifier (last 60 train days vs test, date dropped): AUC 1.0, driven by gh_pl500 and upper-air
    winds, the synoptic state that differs between any two periods. It carries no label information.
  - Transforms over all rows: the values are identical to the published source (max |diff| of obs and t2m_mean is
    0). Nothing is standardised or ranked.
  - Honest "frozen" station bias (training labels only, the last value at train end used for every test day):
    1.2087, much worse, because of the mismatch between training (fresh) and test (stale).
  - Web: this is a paper dataset (Rasp and Lerch 2018, MWR), not a competition. There are no forum, leak or
    "magic feature" threads. The paper's best model (NN-aux-emb) uses station embeddings plus auxiliary
    predictors. Here station is an integer feature and the trees already use it.
  - Source lookup: it works. The published file data_RL18.feather (figshare 13516301) matches every kit row on
    (date, station) with identical obs. That is not a task flaw and is not ranked.

WHAT THE PREPARATION CHANGED (kit vs published source)
  The source has 1,808,942 rows (no missing obs). The kit keeps 1,081,262, a random about 60% subsample (59.5% per
  year, a station SD of 1.9%). The residual mean and SD of kept rows equal those of dropped rows (0.183/1.995 vs
  0.184/1.999). The test-window dates are kept whole (per-date share 1.0). The values are unchanged. The column
  "obs" is renamed t2m_obs, and the *_var columns equal the source's *_var (the paper calls them ensemble SDs).
  The subsampling leaves no artefact I could find.

WHAT I COULD NOT CHECK
  - Whether `date` is the valid date. I inferred it from the first date being 2007-01-03 (first init 2007-01-01 +
    48 h) and the paper's data description. If `date` were the initialisation date, exploit 1 would be the same
    one shifted by two days.
  - Neural-network or embedding models, and larger hyperparameter searches: the honest ceiling may be about
    0.02 to 0.04 lower. That would shrink exploit 1 relative to the honest model, not enlarge it.

Sources: https://arxiv.org/abs/1805.09091 (HTML version), https://github.com/slerch/ppnn (README saved to
ppnn_readme.md), https://doi.org/10.6084/m9.figshare.13516301.v1 (saved to src/data_RL18.feather).
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER REPORT: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany), 2026-11-08
Definition: ppnn_ecmwf_t2m_postprocessing_germany_1m/dataset.py
Rules read from the knowledge files (principles, splits, metrics, provenance), the
register (register.json: none of its 34 flags is on this dataset or its rules here; the PROV-6 and PROV-4 flags
are other datasets' keep/exclude pairs), sibling records and definitions, and the other panel reports.

VERDICT
Four of the five calls follow precedent. One departs: the PLACEMENT of the test windows (three two-week windows spaced
four months apart rather than rolled back from the newest data). It gives a reason (season coverage), but that reason
is not on record as an exception. The closest weather precedents went the other way, and the measured raw error does not
show late December 2016 as an atypical season. A consistency check for the curator is drafted below. No drift found
(Lennart's SPLIT-18 calls run the same way from climate_model to rain_in_australia). No third exception of one kind is
due.

| # | Call | Result | Closest precedents |
|---|---|---|---|
| 1 | Two-week windows instead of the source's held-out year 2016 | consistent | climate_model_weather_forecasting (SPLIT-18 case; Lennart: TabReD's one month "a bit much" for weather, 1-week windows); rain_in_australia (14 days, CC 2026-10-26); bias_correction_r_bias_correction_r_2 (7 days, ship 2026-10-15) |
| 2 | The windows spaced four months apart (Apr, Aug, Dec) | departs; reason given, not recorded, not backed by the measured error | perth_house_prices (step=3, CC 2026-10-26, an atypical COVID period); rain_in_australia (spaced windows declined for contiguous ones, CC 2026-10-26); climate_model_weather_forecasting_1m (3 contiguous weeks, one season); aeolus (CC 2026-10-12) |
| 3 | `mae` as a stand-in for the CRPS | consistent; first CRPS case, so the curator's call sets the precedent; closeness still to be written into the definition (MET-11) | pva_revenue_prediction_kddcup98, asp_potassco_classification (stand-in on a changed task); numerai_v5_2_1m (closeness measured); euppbench_t2m_station_postprocessing (same open question, screening) |
| 4 | year 2021 although the 2020 figshare deposit 9762980 holds every row | consistent with the precedent on PROV-9 | 2_month_survival_rate_prediction (CC 2026-10-26, issue 8); airfoil_self_noise (PROV-9 amended 2026-10-20) |
| 5 | Ship Rasp (2021), not Chen and Lerch (2022) | consistent | hiva_agnostic / nci_aids_antiviral_screen (PROV-6 case, 2026-11-02); PROV-8; the "Same task, another source" tension row (does not apply) |

=====================================================================================================================
1. Window length: two-week weather windows against the source's test year (SPLIT-18 against SPLIT-19)
=====================================================================================================================
Result: CONSISTENT.
- Rule order: both are Should, in the same part; SPLIT-18 comes first and wins at equal strength (principles.md,
  "Conflicts between rules"). The definition says so (splits_comment, Decision 1).
- Precedents on the same task class (station temperature from the output of an NWP model, a temporal split):
  * climate_model_weather_forecasting (record, Lennart's comment before the v2 copy of 2026-10-14; SPLIT-18's case
    row): "TabRed uses 1 month refit horizon. For weather this is a bit much. I would argue for one or two weeks at
    most?" The source's own horizon (TabReD's month) yielded to SPLIT-18: the same direction as here.
  * bias_correction_r_bias_correction_r_2 (Lennart's ship, 2026-10-15): 9 x 7 days, citing climate_model's horizon.
  * rain_in_australia (Lennart, CC 2026-10-26, issue 2): 26 x 14 days, the same reason.
  * aeolus (CC 2026-10-12), not weather: 14-day windows; the authors' split departed from too.
- What sets the source apart, for the record: here SPLIT-19's claim is stronger than in climate_model. The year is the
  data originator's deliberate operational design ("To ensure our verification procedure mimics operational
  conditions", Sect. 2.1), not a benchmark's choice. The source also finds daily updating no better (Sect. 7; the
  definition cites Sect. 6, wrong, see the claim auditor's item 5), and the domain practitioner measured the refit
  cadence as immaterial (at most 0.004 deg C). This is an argument that SPLIT-18's reason (short-lived quantities,
  frequent refits) does not hold for this task. It does not show the definition is inconsistent with the precedents. If
  the curator takes the yearly option (b) of the builder's issue 1, that is the first exception to SPLIT-18. Its fact
  would be "the source shows the refit cadence immaterial and verifies by year", and it should be recorded as such. It
  would then be a candidate to raise for climate_model too. medical_facility_operational_data (CC 2026-11-05, issue 8)
  is no counter-precedent: there the source's horizon was itself two weeks, so SPLIT-18 and SPLIT-19 agreed.

=====================================================================================================================
2. Placement: three windows spaced four months apart, not rolled back from the newest data (SPLIT-15, SPLIT-20)
=====================================================================================================================
Result: DEPARTS. The reason stated is season coverage ("so they fall in three seasons rather than all in the Christmas
weeks at the end of the release", SPLIT-20). It is not recorded as an exception to SPLIT-15. Two measured facts and the
closest precedents weigh against reading it as an application of SPLIT-20:
- SPLIT-15 (Should): "Roll the windows back from the newest data". SPLIT-20 asks to "Check whether the newest windows
  fall in an atypical season and widen them so most do not". Spacing the windows is not widening them, and late
  December is not atypical by the raw forecast error. Decision 1's table gives raw MAE 1.503 / 1.342 / 1.428 for
  the last three weeks of 2016 (mean 1.424), against 1.430 for all of 2016. The shipped spaced windows give
  1.423 / 1.642 / 1.280 (mean 1.448). The split auditor's log shows fitted models scoring worse on the last six weeks
  than on the year (LightGBM 1.253 against 1.085). That is a comparison of models over a few windows, which SPLIT-21
  (Must) bars as a basis for choosing windows. It cannot serve as the distinguishing fact.
- Precedents:
  * perth_house_prices (Lennart, CC 2026-10-26, issue 6): nine one-month windows every third month (`step=3`), accepted
    under SPLIT-20 "so most windows fall outside the COVID months and the stale-record period". The only spaced-window
    precedent, and its fact is an atypical period. That fact is absent here.
  * rain_in_australia (Lennart, CC 2026-10-26, issue 2), the closest weather case, decided the same day: "Do so": 26
    contiguous 14-day windows over the last year instead of 9 spaced six weeks apart ("follows SPLIT-15; no exception
    needed"). The curator wanted every season covered and got it with contiguous windows. He treated spaced windows
    as the form that would need an exception.
  * climate_model_weather_forecasting_1m (same task class, same `_1m` budget, 3 windows): the last three weeks,
    all in July 2023, one season. Nothing in the record or definition discusses seasons.
  * aeolus (Lennart, CC 2026-10-12) / aeolus_rebuilt_1m: contiguous two-week windows, all in late November and
    December. Widened so only one falls in the holiday peak (an atypical period for flights), and the note says "the
    score measures early-winter delays".
  * airqo_low_cost_air_quality_monitor_calibration_challenge (CC 2026-11-05, issue 1): more contiguous monthly windows
    to cover both seasons. That is widening, not spacing.
- What could set this case apart: the release ends on 31 December, and the size protocol gives a 1M train side three
  windows (definitions.md: 1 repeat x 3 folds), where rain_in_australia's 145k rows allowed 26. So contiguous windows
  cannot cover the year here at the protocol's count. That fact comes from the calendar and the protocol, not from
  scores, as perth's and airqo's did. It is not yet written in the definition.
- Not a SPLIT-21 problem as built: the Decision table compares the raw forecast and a station-offset correction, and the
  stated reason is the calendar.

Consistency check, drafted in the issue shape (one turn of the windows issue, builder draft issue 1):

**Consistency check (AI, 2026-11-08):** Should the three two-week windows stay spaced four months apart through 2016, when rain_in_australia took contiguous windows over spaced ones and climate_model_weather_forecasting_1m tests three contiguous weeks of one season?
   - **Problem:**
     - The windows sit in late April, late August and late December 2016 instead of the three newest fortnights, a departure from rolling the windows back from the newest data that is not recorded as an exception.[^s15]
     - The reason given is season coverage, but the newest weeks are not an atypical season by the raw forecast error (mean absolute error 1.424 over the last three weeks of 2016 against 1.430 for the whole year), which is what the season rule asks about.[^s20]
     - The closest weather case went the other way: rain_in_australia got every season from contiguous windows and treated spaced ones as needing an exception, and the only spaced precedent, perth_house_prices, rests on the COVID months.[^prec]
   - **Background:**
     - The release ends on 31 December, and a one-million-row training side gets three windows by the size protocol, so contiguous windows here cover three weeks of December, not a year.
     - Fitted models do score worse in December than over the year (LightGBM 1.253 against 1.085), but windows may not be chosen from model scores over a few windows.[^s21]
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a (implemented) | Keep the spaced windows as an exception | Records the exception with the fact: the release ends on 31 December and the protocol gives three windows, so only spacing covers three seasons; chosen from the calendar, not scores | Tests winter, spring and summer weather; follows the curator's wish for every season in rain_in_australia; no change to the build | First spaced weather windows; the newest weeks are not atypical, so it rests on coverage alone; climate_model_weather_forecasting_1m stays single-season |
     | b | Three contiguous fortnights at the end of 2016 | Rolls back from 31 December (about 20 November to 31 December), with a note that the score measures early-winter weather, as aeolus does | Follows the default and climate_model_weather_forecasting_1m and aeolus; no exception | One season only; the late-December fortnight carries the holidays at the release end |
     | c | Keep (a) and reopen climate_model_weather_forecasting_1m | Spaces climate_model's three weeks over its year (July 2022 to July 2023) the same way | The weather family is decided alike | Reopens a shipped dataset for a choice nobody questioned there |
     | d | Change the rule | Amends the season rule: when the protocol's windows cannot cover a year contiguously and the release ends in one season, space them over the last year, chosen from the calendar | Settles perth_house_prices, this dataset and later weather releases at once | Two cases so far, not the three that call for an amendment |
     | e | Contiguous fortnights over all of 2016 | 26 two-week windows covering 2016, as in rain_in_australia; their union is the source's test year | Default placement, every season, and the source's year at once | 26 training sides of a million rows, nine times the protocol's count for this size; a large compute cost per method |

   - **Recommendation:** (a). The fact is a real one, the curator valued every season in rain_in_australia, and the calendar decides it, not scores. climate_model_weather_forecasting_1m can be aligned when it is next reopened rather than now.
   - **Decision:** keep the spaced windows as a recorded exception, or roll them back from the newest data?

[^s15]: SPLIT-15 (Should): "Roll the windows back from the newest data: as many windows as an IID or grouped task of that size would get folds."
[^s20]: SPLIT-20 (Should): "Check whether the newest windows fall in an atypical season and widen them so most do not." Cases: aeolus; perth_house_prices (step=3, CC 2026-10-26, Lennart); airqo (CC 2026-11-05, Lennart).
[^prec]: rain_in_australia, CC 2026-10-26 (Lennart), issue 2: "Do so": 26 contiguous 14-day windows "instead of 9 spaced six weeks apart (follows SPLIT-15; no exception needed)". climate_model_weather_forecasting_1m: the last 3 weeks of July 2023. principles.md, "Consistent judgement", case 2.
[^s21]: SPLIT-21 (Must): "Decide neither the training history nor the windows from a comparison over a few test windows."

=====================================================================================================================
3. Metric: `mae` as a stand-in for the CRPS (MET-2, MET-5, MET-11)
=====================================================================================================================
Result: CONSISTENT, a first case.
- MET-5: the CRPS is the source's one deliberate criterion (Table 2's ranking, the networks' loss, EMOS fitted by it;
  confirmed by the claim auditor, row 21), so it is the original, not a fallback case.
- MET-11 `stand_in` fits "a task we changed": the source scores a distribution, the regression protocol takes one value.
  The same reading as pva_revenue_prediction_kddcup98 (net revenue to `roc_auc` once the task was changed to the
  response) and asp_potassco_classification (PAR10 to `log_loss`). It is not `source` with an identity like porto_seguro
  (normalized Gini = 2 x ROC AUC - 1 on the same predictions). The CRPS equals the absolute error only for a point
  forecast, so the identity holds on our predictions, not on the source's.
- No curator decision on a CRPS exists yet. euppbench_t2m_station_postprocessing (screening, AI) poses the same
  question ("`mae` as a stand-in or the fallback `rmse`, the curator's call"). The curator's answer here sets the
  precedent for it. cape_floristic_region_family_cover (CRPS among several criteria, so the fallback) and
  how_much_did_it_rain (a CRPS competition, metric not decided) differ in the facts that matter: several criteria, and a
  competition.
- One gap against MET-11 (Must) as numerai_v5_2_1m applied it ("the closeness is measured on the shipped splits where
  possible": pooled Pearson within 0.0002 of CORR, written into the definition). The definition gives the identity but
  no measured closeness. The claim auditor measured it: Kendall tau between MAE and CRPS 0.944 / 0.989 / 0.944 over 10
  models, the same best model in 3 of 3 windows (RMSE 0.989 / 0.944 / 0.899). A fix, not a curator call: add the
  sentence to the metric's `reason`. MET-10's diversity factor also favours `mae` over `rmse` (zillow_prize is the
  collection's other `mae` regression).

=====================================================================================================================
4. Year: 2021 when the 2020 figshare deposit 9762980 already holds every row (PROV-9, PROV-6)
=====================================================================================================================
Result: CONSISTENT with the precedent. The claim auditor's reading (2020) would depart from it.
- Facts (claim auditor, row 3, measured): "Interpolated PPNN data" (Rasp, figshare 9762980, 2020-02-11) holds all
  1,808,942 rows, the identical target `t2m_obs`, and the 50 t2m members whose mean and variance equal `t2m_mean` and
  `t2m_var`, plus station lat, lon and alt. That is 5 of the 40 inputs we ship. It lacks the 34 columns of the other 17
  forecast variables and `orog`.
- Precedent: 2_month_survival_rate_prediction (Lennart, CC 2026-10-26, issue 8): "the year is 2003, ... the first
  publication of the rows we ship (PROV-9). ICPSR 2957 V1 (January 2001) holds the study data in another form ..., so
  it does not hold every value we ship". The test applied is "every value we ship". airfoil_self_noise (PROV-9 amended
  2026-10-20) reads "holds the rows" the same way: the measured values together with the columns computed from them.
  The 2020 deposit does not hold every value we ship, and the 2021 deposit is the first that does, so 2021 follows the
  precedent.
- A difference that does not change the outcome: in support2 the earlier release held altered values. Here the shared
  values are identical but 35 inputs are missing. The precedent's stated criterion covers both.
- PROV-9 is a Must, so it takes no exception. Setting 2020 would need an amendment of how PROV-9 reads "holds the rows"
  (the first deposit with every row and the target, whatever inputs later deposits add), and support2 would then be
  reopened (ICPSR 2001). If the mediator or curator leans to 2020, offer that as an amendment, not a one-off.
- Text fix (no call): claims.md row 3 says "contents not downloaded". The definition's sentence on the 2020 deposit is
  right but should state the measured facts and the criterion ("the first deposit that holds every value we ship;
  the 2020 deposit holds the rows, the target and the t2m members, not the other 17 variables").

=====================================================================================================================
5. Which copy ships: Rasp (2021) rather than Chen and Lerch (2022) (PROV-6, PROV-8)
=====================================================================================================================
Result: CONSISTENT.
- The two are versions of one dataset with no distinct task (PROV-6; PROV-7 not met). The 2022 deposit (figshare
  19453580) holds the same rows, adds the 50 raw t2m members and day-of-year columns, drops soil moisture, and names
  the spread `_std`.
- PROV-8: the source is the first publication of what we ship. The 2021 deposit is that, and it matches the paper's
  Table 1 (all 18 variables, soil moisture included). hiva_agnostic / nci_aids_antiviral_screen (PROV-6 case,
  Lennart 2026-11-02) chose the release closer to the origin over a later rebuild of the same rows. sz_clay_shenzhen
  (screening, AI) took the deposit that matches the data paper.
- The "Same task, another source" tension row (Lennart, 2026-11-08: the better data enters, "larger or newer with the
  same target and features") does not apply: one source, and the 2022 copy has different inputs, not the same ones.
- No record exists for the 2022 deposit. It is a link with a note in this record's `source_links`, so no `Duplicate`
  verdict is pending. Note for later: if the raw members were ever wanted, the 2020 deposit holds them first.

=====================================================================================================================
Other calls checked in passing (no finding)
=====================================================================================================================
- Random 1M of the whole history per window, not the newest rows: as climate_model_weather_forecasting_1m (TabReD's
  random sub-sample, "to keep data from various time periods"). The claim auditor found no break in the history (I5),
  so aeolus's history cut (COVID) has no counterpart here (SPLIT-20).
- Gap of 2 days, the source's own convention (fclt=48). bias_correction and aeolus_rebuilt_1m use 1 day, each from its
  own label's availability (the SPLIT-10 cases are decided per task). The claim auditor's item 3, one day longer than
  needed, is a wording fix. No precedent conflict.

FILES
- Precedent records: curation/records/{climate_model_weather_forecasting,rain_in_australia,perth_house_prices,
  aeolus,bias_correction_r_bias_correction_r_2,2_month_survival_rate_prediction,euppbench_t2m_station_postprocessing}.md
- Rules: .claude/skills/knowledge-curation/references/splits.md (SPLIT-15, -18 to -21, Cases), metrics.md
  (MET-5, MET-11, Cases), provenance.md (PROV-6, -8, -9, Cases), principles.md
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE OPENING BRIEF: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany)
2026-11-08. Position: ship as defined, with the no-decision fixes listed in points 4, 5 and 7. The two split calls
(window length, window placement) are weighing calls on Should rules; I argue the shipped choice and concede their costs.

Judgment record (as I read the evidence):
  Validity: USE-1/USE-8 hold (direct fit); LEAK-10 holds for all 41 inputs; SPLIT-10 holds (gap one day conservative);
    PROV-8 holds (Table 2 reproduced); PROV-9 holds by the 2_month_survival precedent (2021).
  Value: TP-4/TP-10 hold (LightGBM 1.033 vs MOS 1.297 vs raw 1.448, 3/3); MET-11 stand-in holds, closeness to be written in.
  Quality: CLEAN-11 triggered twice (one test label, one stuck run): fix in `_clean`; notes to correct.
  For the curator: issue 1 window length (SPLIT-18 vs SPLIT-19); placement recorded as an exception to SPLIT-15.

1. P4: no leak, and the only exploit is about 1% and not consistent. (LEAK-10 Must, LEAK-16 to 21 Must, SPLIT-10 Should)
   Evidence: every input is a step-48 forecast of the 00 UTC run or a fixed station property; no observation lag
   (column auditor, claim auditor rows 18, I1). 0.0% exact copies, one row per station-date. The gap is enforced in all
   three windows: train_end 12-15 / 08-15 / 04-15 (claim auditor row 25, split auditor check 2); the blind reviewer's
   "gap only before the last window" was inferred from a 200k sample, where the 04-16/17 and 08-16/17 rows are training
   rows of the LATER windows, so the measurement refutes it (EV-2). Missing soil moisture does not track the target
   (indicator R^2 -3.1). Task gamer: "barely gameable"; the one working exploit joins forecasts issued after the
   prediction point from other test rows of the same window, gain 0.006-0.015 MAE, +0.006 (worse) on r0 with 1000 trees,
   smaller than the gap between model sizes. Each row is clean under LEAK-10; this is a cross-row property of any
   multi-day window. Mildest remedy: a one-line note (the gamer's own "accept it as small and documented"); thinning
   test days would cut the test pool by two thirds for a 1% effect.
   Outranks: no Must is broken, so nothing at P4 forces a change.

2. P3: a real use case with a direct fit, and the target is what the actor issues. (USE-1, USE-5, USE-8, USE-9)
   Evidence: domain practitioner (DWD post-processing team): "Fit: DIRECT (agree with the definition)"; a point
   temperature per station is a real product (DWD Ensemble-MOS point values verified by MAE, Hess 2020, Fig. 11; MOSMIX).
   The target is the observed 2 m temperature, untransformed. The distribution-vs-point gap is named in `changes` and
   `fit_reason` (USE-9: the point product is itself a real use case).
   Outranks: the point-vs-distribution objection is a metric question (P6) and cannot override a P3 fit that holds.

3. P5: the data is the paper's, to the decimal, from the right deposit, with the right year. (PROV-8, PROV-9 Must, PROV-6)
   Evidence: claim auditor reproduced Table 2 on the file: raw 1.152 (paper 1.16), EMOS-gl 1.009 (1.00), EMOS-loc 0.902
   (0.90); rows 1,626,724 + 182,218 as in Sect. 2.2; 537 vs 535 stations resolved (two stations never observed).
   Year: the claim auditor would set 2020, but the 2020 deposit holds 5 of the 40 inputs (target, t2m members, lat/lon/
   alt), not the 34 columns of the other 17 variables nor orog. PROV-9 as applied in 2_month_survival_rate_prediction
   (CC 2026-10-26: "the first publication of the rows we ship ... does not hold every value we ship") gives 2021
   (precedent checker item 4). Rules over precedents only if the precedent contradicts the rule; it does not, it reads
   "holds the rows". Setting 2020 would be an amendment of PROV-9 and reopen 2_month_survival.
   Fix with no decision: replace "contents not downloaded" and the 2020 sentence with the measured facts and the
   criterion; optionally cite the 2020 deposit in the BibTeX. Chen and Lerch 2022 not used: consistent (PROV-6).

4. P6: worth benchmarking, and `mae` is the right metric under this protocol. (TP-4, TP-10, MET-5, MET-11 Must, MET-10)
   Evidence: on the shipped splits raw 1.448, station offset 1.351, per-station MOS 1.297, ridge 1.318, LightGBM 1.033;
   LightGBM beats MOS on 3/3 windows; skill +0.939 vs dummy; families spread (ridge 1.26-1.46 vs LightGBM 0.96-1.21,
   claim auditor row 30), which answers the probe's `no_spread` flag. Metric: MAE is the CRPS of a point forecast
   (eq. B1, identity); measured closeness Kendall tau(MAE, CRPS) 0.944 / 0.989 / 0.944, same best model in 3/3, mean
   0.959 against 0.944 for the `rmse` fallback; the practitioner would choose `mae` himself; MET-10 diversity favours it.
   Real gap (conceded): MET-11's clause "closeness measured on the shipped splits where possible" is not in the
   definition. Mildest remedy: add the tau sentence to `metric.reason` (precedent numerai_v5_2_1m). No decision needed;
   it also settles builder issue 2 (`mae` over `rmse`).

5. P4: the two-week windows follow rule order and three precedents, and the refit cadence does not change the task.
   (SPLIT-18 Should before SPLIT-19 Should; SPLIT-21 Must)
   Evidence: at equal strength in one part the earlier rule wins (principles.md). Precedents on the same task class all
   chose SPLIT-18 over the source's horizon: climate_model_weather_forecasting (Lennart: TabReD's month "a bit much"
   for weather), bias_correction_r_bias_correction_r_2 (7 days), rain_in_australia (14 days) (precedent checker:
   "consistent"). The refit gain is immaterial: practitioner at most 0.004 deg C; split auditor LightGBM -0.016 to
   +0.006 on the shipped windows. The 42 test days sit at the year's difficulty (raw 1.448 vs 1.441 for all of 2016).
   Conceded: the cost is statistical. SE of a model difference about 0.04 on 42 days vs 0.014 on the year; close pairs
   (ridge vs MOS) flip in 29.7% of 3-block draws; the shipped windows overstate LightGBM's lead over MOS (-0.265 vs
   -0.184). LightGBM against any other model never flips. The source's Sect. 7 / fn. 4 finding is a real fact that
   could set this case apart for an exception to SPLIT-18 (option b, or the split auditor's milder "2016 in three
   windows"); that is the curator's weighing call (issue 1), not a defect, and SPLIT-21 bars settling it by the scores.
   Fixes with no decision: reword `task_summary.split` (no "refit every two weeks" practice; practitioner gap 3);
   reword the gap reason (D-2's observation is in; the source's convention leaves out two days); cite Sect. 7 and
   fn. 4 of Sect. 5.1, not Sect. 6 / 3.1; add the split auditor's sentence on the August warm spell.

6. P4: spacing the windows over 2016 is the only way to cover seasons under the protocol, and should be recorded as an
   exception rather than undone. (SPLIT-15 Should, SPLIT-20 Should)
   Evidence: precedent checker finds a departure from SPLIT-15 with a reason given but not recorded. The distinguishing
   fact comes from the calendar and the protocol, not from scores: the release ends on 31 December and a 1M train side
   gets three windows, so contiguous fortnights cover only December (rain_in_australia's 145k rows got 26 windows and
   every season; the curator wanted every season there). perth_house_prices is an accepted spaced-window case (step=3).
   The Decision table compares only the raw forecast and a station offset (SPLIT-21 holds).
   Conceded: late December is not atypical by raw error (1.424 vs 1.430), so SPLIT-20's "atypical season" clause does
   not itself demand the spacing; the exception rests on coverage and serves P4 (the test stands for the service's
   year). Mildest remedy: record "Exception to SPLIT-15" with that fact, the precedent checker's recommendation (a).

7. P7: the cleaning problems are real, small and cheap to fix in the definition; none touches validity.
   (CLEAN-11 Should, CLEAN-15 Must; tension row "a real task against imperfect cleaning": keep the task, fix what is cheap)
   Conceded and fixed: station 254, 2016-08-25, obs 0.0 between 18.1 and 18.2, forecast 19.8, in the August test window
   (column auditor, blind reviewer): set missing, the row leaves (CLEAN-15), guarded at 1 row; effect +0.0028 MAE.
   Station 288 stuck at 11.3 C for 12 nights in 2014-12: set missing, guarded at 12. The soil-moisture note misses
   9,891 rows at 11 Baltic stations (7 lack sm in all test windows): amend the note and Decision 2; values stay missing.
   Notes: nearest grid point for the 17 non-t2m fields, units of sm/cape/q/winds, orog of the 2007 cycle, `station` is
   the deposit index, probe 13's p90 flag = the 2015 summer, TIGGE acknowledgement. Optional: clip cape -4.5e-13 to 0.
   Outranks: P7 sits below P3-P6, and every item has a fix on the first rung of the ladder that keeps the dataset.

=====================================================================================================================
Rebuttal
=====================================================================================================================
Where we stand: the critic and I agree on the verdict (ship after changes), on no exclusion, and on six of seven points.
One weighing call stays open: the window design (critic point 2c).

C1. LEAK-9 evaluation leak, protocol line. CONCEDE, and it corrects my point 1. I filed the cross-row join under a
    plain note. LEAK-9 (Should, amended 2026-11-05) names exactly this mechanism ("a model can read other test rows")
    and its remedy: a protocol line the benchmark checks, as for medical_facility_operational_data. What follows: add
    the line to splits_comment (each test row is predicted from the training rows and its own features; no step may
    use other test rows) and the "Potential leak, kept on purpose (LEAK-9)" note with the gamer's numbers. No data
    change, so this still keeps the dataset as built.

C2a. Placement not recorded. CONCEDE (my point 6). Record the exception to SPLIT-15 with the calendar fact (release
    ends 31 Dec; three windows at 1M rows), or it goes away under the critic's option.
C2b. 42 test days are noisy. CONCEDE the facts (SE about 0.04 against 0.014; ridge-MOS flips in 29.7%; LightGBM's lead
    over MOS overstated, -0.265 against -0.184). DISPUTE their weight as grounds: they come from model scores over
    windows, and SPLIT-21 (Must) bars choosing the windows from such a comparison (the split auditor: "by SPLIT-21 they
    decide nothing"). They inform the curator; they cannot carry the change.
C2c. SPLIT-18's reason does not hold; ship 2016 as three four-month windows. PARTLY CONCEDE. The critic's option is a
    valid exception: it meets SPLIT-15, SPLIT-19 and SPLIT-20, stays under the budgets, and its distinguishing fact
    comes from the source (Sect. 2.1 verification by year; Sect. 7 and fn. 4 of Sect. 5.1, refit gain immaterial),
    not from scores. I also concede the task_summary.split wording (no "refit every two weeks" practice; reword
    as the critic and the practitioner propose, in either design).
    DISPUTE that it is the required fix rather than the curator's choice:
    - Rule order: SPLIT-18 and SPLIT-19 are both Should in one part, and the earlier wins. A departure is an
      exception the curator records ("Should ... A departure needs the fact that sets the case apart"); it is not a
      defect of the shipped definition.
    - Like cases alike (principles.md, consistency case 2): "each row brings its own fresh forecast" also describes
      climate_model_weather_forecasting (station temperature from NWP output, the precedent checker's same task
      class), where the curator chose short windows over the source's horizon. Only the source's measured cadence
      finding sets this case apart, so taking the critic's option is the first exception to SPLIT-18 and makes
      climate_model a candidate to reopen (precedent checker, item 1). That is a curator call, not a panel fix.
    - Four-month windows enlarge the C1 exploit (the critic says so), which then rests more on the protocol line.
    What follows: issue 1 stays a weighing call with two complete options: (a) shipped two-week windows plus the
    SPLIT-15 exception and the rewording; (b) 2016 in three four-month windows as an exception to SPLIT-18, with
    climate_model flagged. I hold (a) by rule order and precedent; (b) is defensible and I do not oppose it.

C3. PROV-9 text. CONCEDE; we agree on 2021 and on the text (criterion plus the measured facts on the 2020 deposit;
    turn the 535/537 "Anomaly" into the found fact).
C4. MET-11 closeness. CONCEDE; same remedy as my point 4 (the tau sentence in metric.reason), `mae` stays.
C5. Wrong test label and stuck sensor. CONCEDE; same remedy as my point 7 (station 254 guarded at 1 row, station 288
    at 12; airqo precedent for test labels).
C6. Soil-moisture and interpolation notes. CONCEDE; same remedy as my point 7 (correct the bullet and Decision 2,
    nearest grid point for the 17 non-t2m fields, orog vintage; values stay missing).
C7. Citations, gap reason, probe 13, August note. CONCEDE; same text fixes as my point 5.

Judgment record after the rebuttal:
  Verdict: ship after changes.
  Validity: LEAK-9 triggered, fixed by a protocol line; SPLIT-15 departure recorded as an exception; SPLIT-18 vs
    SPLIT-19 open; PROV-9 holds (2021), text fixed.
  Value: MET-11 closeness written in; `mae` kept.
  Quality: CLEAN-11 two labels set missing (CLEAN-15); notes corrected.
  For the curator: issue 1 only, (a) shipped windows or (b) the source's year in three four-month windows.

Addendum (the critic's rebuttal of my opening, read after the above): on A1 we now agree (protocol line under LEAK-9,
conceded in C1). On A6 I CONCEDE the wording: "the only way to cover seasons" holds only for two-week windows; three
contiguous four-month windows also cover them, so each path needs exactly one exception (SPLIT-15 for (a), SPLIT-18 for
(b)). On A5 the critic and I now differ on one thing only: whether the measured cadence finding is enough to depart from
SPLIT-18 here without the curator first deciding it against climate_model. That is the curator's call.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: ppnn_ecmwf_t2m_postprocessing_germany_1m (record ppnn_ecmwf_t2m_postprocessing_germany), 2026-11-08
Read: dataset.py, README.md, principles.md, splits.md (SPLIT-15 to -21), leak_checks.md (LEAK-9), metrics.md (MET-11),
provenance.md (PROV-9), cleaning_features.md (CLEAN-11), the builder report and the seven phase-A reports.

POSITION: ship only changed. The task is real and has no data leak; I do not argue for exclusion. The definition
should not ship as it stands: it lacks the protocol line an evaluation leak needs (P4), its test design rests on 42
weather days placed by an unrecorded departure (P4), its stand-in lacks the measured closeness a Must asks for (P6),
and it ships a known wrong test label (P7). Points in rank order.

---------------------------------------------------------------------------------------------------------------------
1. P4, LEAK-9 (Should, as amended 2026-11-05): an evaluation leak with no protocol line.
   Problem: every row is a forecast issued at D-2. A 14-day test window also holds the same station's rows for D+1 and
   D+2, whose forecasts were issued at D-1 and D, after the prediction point of row D, and they carry information on
   day D. A model that joins them by (station, date) reads other test rows.
   Effect: a participant gains on the shipped splits; a deployed model has no such rows.
   Evidence: task gamer, exploit 1: 1.0833 -> 1.0692 (H500; per split -0.002 / -0.011 / -0.029), 1.0688 with a wider
   join (-0.015 / -0.006 / -0.023), 1000 trees 1.0662 -> 1.0606 (+0.006 / -0.012 / -0.012). Noise of a random column:
   about 0.005. Small (about 1% MAE), but the same mechanism as medical_facility_operational_data and
   frempl_french_motor_personal_line, both of which carry the line. It grows with any longer window (point 2).
   Remedy (mildest): a protocol line in splits_comment and a "Potential leak, kept on purpose (LEAK-9, an evaluation
   leak)" note with these numbers: each test row is predicted from the training rows and its own features only; no
   feature or model step may use other test rows. No data change.

2. P4, SPLIT-15 / SPLIT-19 against SPLIT-18 (all Should), SPLIT-21 (Must) respected: the test design.
   Problem a, placement: the windows are spaced four months apart, not rolled back from the newest data (SPLIT-15).
   The reason given is SPLIT-20's season check, but late December is not atypical by the raw error (last three weeks
   1.424 against 1.430 for 2016), and spacing is not widening. Not recorded as an exception; rain_in_australia (CC
   2026-10-26) took contiguous windows over spaced ones; perth's spacing rested on COVID months (precedent checker,
   call 2: DEPARTS).
   Problem b, size: 42 test days. The errors of about 500 stations on one day share one weather situation. SE of a
   model difference about 0.04 on 42 days against 0.014 on the year; over the 2,600 choices of 3 of 2016's 26
   fortnights, ridge against MOS (0.014 apart over the year) flips in 29.7%, MOS against the station offset in 13.4%
   (split auditor 1b). The shipped windows give LightGBM minus MOS -0.265 against -0.184 over all of 2016 (1c). Close,
   tuned methods will be ranked by a few cold spells. Blind reviewer's first concern, independently.
   Problem c, SPLIT-18's own reason does not hold here: short windows are for short-lived quantities refit often. Each
   row brings its own fresh forecast; the source trains once and finds daily updating no better (Sect. 7) and rolling
   EMOS marginal (Sect. 5.1, fn. 4); DWD's MOSMIX trains on 10+ years (domain practitioner). The source's split is a
   deliberate operational design ("To ensure our verification procedure mimics operational conditions", Sect. 2.1),
   so SPLIT-19 has a strong claim. The task_summary's "as for a correction refit every two weeks" describes a practice
   no weather service has.
   Effect: the ranking of close methods rests on 42 days; the text claims a practice that does not exist.
   Remedy I ask for: the source's test year 2016 as three contiguous windows of four months (2016-01-01, 05-01, 09-01,
   about 60k test rows each, under the 500k test budget, train sides still over 1M; split auditor's "mildest form",
   blind reviewer's proposal). It rolls back from the newest data (SPLIT-15), covers every season (SPLIT-20), is the
   source's test set (SPLIT-19), and gives 8.7 times the test days. It is an exception to SPLIT-18 with the fact: the
   source shows the refit cadence immaterial and verifies by year (Sect. 2.1, 7), so SPLIT-18's reason does not apply;
   serves P4 (the test mirrors how the actor verifies). Chosen from the source and the calendar, not from scores
   (SPLIT-21). Fallback if the curator keeps two-week windows: record the spacing as an exception to SPLIT-15 with the
   calendar fact (release ends 31 Dec, three windows at 1M rows), and reword task_summary.split (e.g. "a correction
   trained on the earlier years, scored on two weeks in each of three seasons").

3. P5, PROV-9 (Must): the year's justification rests on an unmeasured claim.
   Problem: the definition and claims say the 2020 deposit (figshare 9762980) holds "the temperature forecasts and
   observations without the other variables", "contents not downloaded". Measured (claim auditor row 3): it holds all
   1,808,942 rows, the identical target, and the 50 t2m members whose mean and variance equal t2m_mean and t2m_var to
   1e-14: 5 of the 40 inputs. By the precedent (2_month_survival_rate_prediction: "every value we ship"), 2021 still
   holds (precedent checker, call 4). I do not ask for 2020.
   Remedy: state the criterion and the measured facts in curation_comments ("the first deposit that holds every value
   we ship; the 2020 deposit holds the rows, the target and the t2m members, not the other 17 variables or orog").
   Also replace the "Anomaly: 535 vs 537 stations" line with the fact found: two listed stations never reported.

4. P6, MET-11 (Must): the stand-in's closeness is not measured in the definition.
   Problem: MET-11 asks that a stand-in's closeness be measured on the shipped splits where possible; the reason gives
   the identity only, though it was measurable.
   Evidence: claim auditor 23b: Kendall tau(MAE, CRPS) 0.944 / 0.989 / 0.944 over 10 models, same best model in 3 of
   3 windows; RMSE 0.989 / 0.944 / 0.899. This also settles the builder's draft issue 2 for `mae` (MET-10 diversity).
   Remedy: one sentence with these numbers in the metric's `reason`. No change of metric.

5. P7, CLEAN-11 (Should) -> CLEAN-15 (Must): a wrong test label and a stuck sensor.
   Problem: station 254 on 2016-08-25 has t2m_obs 0.0 between 18.1 and 18.2, forecast 19.8; the only obs == 0 with a
   forecast above 12 C in the file (column auditor 1, blind reviewer 4, found independently). It is a test label of the
   August window. Station 288 reads 11.3 C on 12 consecutive winter nights (2014-12-20..31) while the forecast falls
   from 9.4 to -3.0 (training side).
   Effect: about 19.5 C error on one test row, +0.0028 MAE to every model in that window; the stuck run adds wrong
   training labels. Small, but wrong labels, and the source applied no quality flags.
   Remedy: set both missing in `_clean`, rows leave by CLEAN-15, guarded at 1 and 12, as airqo (CC 2026-11-05: impossible
   test labels removed from test windows too). A quality fix, not a reason to exclude.

6. P7 and writing: the soil-moisture and interpolation notes are wrong.
   Problem: the notes and Decision 2 say soil moisture is missing in 2014-03-06..07-04 and always at 17 stations.
   Measured: 9,891 more missing rows at 11 Baltic-coast stations by model period; 7 stations (147, 153, 171, 203, 333,
   399, 401) have sm in the training years 2010-2015 and none in all three test windows (from 2016-03-11, the ECMWF
   upgrade). Test rows without sm 4.2% against 6.6-6.8% in training (column auditor 3, claim auditor 13). Also "interpolated
   to the station" holds for t2m only; the other 17 fields are the nearest grid point (500 stations, 212 distinct sp_mean
   values on one day), which explains d2m in kelvin; orog is the 2007 cycle's.
   Effect: a covariate shift at 7 stations the curator should read; no leak (indicator R^2 -3.1).
   Remedy: correct the bullet and Decision 2's text; keep the values missing.

7. Writing / EV: wrong citations and readings in the definition.
   - "updating them daily did not help (Sect. 6)": it is Sect. 7; "fixed as good as rolling (Sect. 3.1)" is Sect. 5.1,
     fn. 4 (claim auditor 27, domain practitioner).
   - The gap reason (SPLIT-10, Should) is wrong: the D-2 00 UTC observation is in when the D-2 run is post-processed;
     only D-1 is missing. Keep the 2-day gap as the source's convention; reword (claim auditor 25, split auditor 3).
   - The probe note leaves out probe 13's p90 flags (z +6.3, pooled +11.9), the 2015 summer heat (Q3 p90 20.3 against
     17.5-19.0), not a recording change (EV-3; claim auditor 29).
   - The late-August window falls in a spell with the ensemble too cold, where nonlinear corrections gain most; say so
     if the two-week windows stay (split auditor 2).
   Remedy: text fixes in dataset.py.

---------------------------------------------------------------------------------------------------------------------
Dropped, not backed: the blind reviewer's "inconsistent gap" (the container's train_end is window start minus 3 days in
all three windows, claim auditor 25, split auditor 2; the sample's rows on 04-16/17 belong to later windows' train
sides); `date` as a raw trend (dropping the year moves LightGBM by -0.025 to +0.038, split auditor 6); the `_var`
naming (lossless, documented).

Judgment record:
Verdict: ship after changes.
Validity: LEAK-9 triggered, fix by a protocol line; SPLIT-15 departure unrecorded and SPLIT-19 vs SPLIT-18 open, fix by
the source's year in three four-month windows (exception to SPLIT-18) or by a recorded exception to SPLIT-15; PROV-9
holds, text to state the criterion.
Value: MET-11 Must gap, fix by one sentence (tau 0.94-0.99).
Quality: CLEAN-11 two label fixes (one in test); soil-moisture and interpolation notes corrected.
For the curator: the window design (point 2) is the one weighing call.

=====================================================================================================================
Rebuttal
=====================================================================================================================
The advocate and I agree on most changes. Two points stay disputed: what LEAK-9 asks for (a protocol line, not a note)
and which window design to recommend. No new facts.

A1 (P4, no leak; the exploit is small): CONCEDE no feature leak (LEAK-10), no copies, and the gap enforced in all
   three windows (I dropped the blind reviewer's gap point too). DISPUTE the remedy. LEAK-9 (Should, as amended
   2026-11-05) does not ask for a note: an evaluation leak "is fixed in the scoring or by a protocol line the
   benchmark checks", and a method that reads the test block "is called out and not benchmarked". Size is not what
   triggers the rule. The mechanism (reading other test rows) is what triggers it, and both precedents with that
   mechanism carry the line (medical_facility_operational_data, frempl_french_motor_personal_line). On the mean the gain
   is above noise: 0.014 for H500 and 0.015 for the wide join, against about 0.005 from a random column. I agree not to
   thin the test days. Ask stands: the protocol line plus a "Potential leak, kept on purpose (LEAK-9)" note with the
   numbers. It changes no data.
A2 (P3, direct fit, real target): CONCEDE in full. I raised no point against it.
A3 (P5, faithful data; year 2021): CONCEDE. Same position as my point 3: keep 2021 by the 2_month_survival precedent,
   and replace "contents not downloaded" with the measured facts and the criterion.
A4 (P6, worth benchmarking; `mae`): CONCEDE. Same remedy as my point 4: put the tau sentence (0.944 / 0.989 / 0.944) in
   `metric.reason`. That settles builder issue 2 for `mae`.
A5 (P4, two-week windows by rule order and precedent): CONCEDE that this is the curator's weighing call, that SPLIT-21
   bars settling it by scores, and the text fixes (split wording, gap reason, citations, the August sentence). DISPUTE
   that rule order settles it. "The earlier rule wins at equal strength" is the default only. principles.md lets a
   Should give way when a fact sets the case apart and a higher principle is served. The advocate concedes such a fact
   exists: the source's Sect. 7 and fn. 4, and refit gains of at most 0.004 (MOS) and -0.016 to +0.006 (LightGBM). That
   fact removes SPLIT-18's own reason, short-lived quantities refit often. The precedents do not have it:
   climate_model's call ("a bit much") was made with no measurement of the refit gain and no source verifying by
   year (precedent checker call 1: "SPLIT-19's claim is stronger than in climate_model"). The advocate also concedes the
   cost: SE 0.04 against 0.014, close pairs flipping in 29.7% of draws, and LightGBM's lead over MOS overstated (-0.265
   against -0.184). My recommendation stands: the source's year 2016 in three contiguous four-month windows.
A6 (P4, spacing recorded as an exception to SPLIT-15): CONCEDE the fallback. If the two-week windows stay, record
   "Exception to SPLIT-15" with the calendar fact, as in my point 2. DISPUTE "the only way to cover seasons under the
   protocol": three contiguous four-month windows of 2016 also cover every season with three windows, and they meet
   SPLIT-15 with no departure. Each path needs one exception (SPLIT-15 for the advocate's, SPLIT-18 for mine). Mine
   also gives the source's test set (SPLIT-19) and 8.7 times the test days.
A7 (P7, cleaning fixes): CONCEDE in full. These match my points 5 and 6. I add the advocate's optional items (cape clip,
   TIGGE acknowledgement, units, station index) to the note fixes.

Net after the rebuttal:
- Agreed, no decision needed: the `mae` closeness sentence; the year text; the two CLEAN-11 label fixes; the soil
  moisture, interpolation and units notes; the citations, gap reason and split wording.
- Disputed, settled by the rule's text: a protocol line under LEAK-9, not just a note.
- For the curator: the window design. My recommendation is 2016 in three four-month windows, an exception to
  SPLIT-18. The advocate's is the shipped spaced fortnights, an exception to SPLIT-15.
```

</details>
