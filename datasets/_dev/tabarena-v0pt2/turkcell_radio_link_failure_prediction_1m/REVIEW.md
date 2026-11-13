# turkcell_radio_link_failure_prediction

**Outcome:** added as `turkcell_radio_link_failure_prediction_1m`. Turkcell's microwave-link counters and weather for the ITU AI/ML in 5G Challenge 2021: 1,963,348 link-days (31 December 2018 to 24 December 2020), "a radio link failure the next day" as target, tested on the three four-month windows of 2020 with up to a random 1M earlier link-days for training; the AI recommends shipping it once the curator settles the metric (issue 1).

Judgment record:

- Decision: ship after changes, made now.
- Decisive rules: a Must on the label (the published flag was computed on counters written in thousands), a Must on columns (the day's observed weather is read again), a Should on test-row lookups (kept as a protocol line), a Should on the source's metric (issue 1).
- Remedy: repair at the origin.
- Exceptions: none.

Changes made: the counters are repaired and the flag recomputed by Turkcell's rule (2,011 positives instead of 1,204). The repair can be undone; the published flag would then ship as an approximate fit missing about 40% of failure days; not recommended. On the repaired label the model clearly leads the link's own failure rate only in September to December (+0.10 to +0.15 ROC AUC over three seeds, SE 0.02-0.05). In May to August the lead is +0.01 to +0.10, within noise for one seed. January to April is a tie. The AI judges that this passes the check that a model must beat the series' own naive forecast, so the scope question (shipping it as a forecasting task outside the main benchmark) is not raised; the 2021 winner (MLGrads) published a tabular AdaBoost/XGBoost on the same kind of inputs, so a tabular model is a real way to solve the task. The licence warning of the check is proposed for acceptance: the repository has no licence file, and its README asks users to cite Aktaş, Alemdar and Ergüt 2022 and calls the data live network data for researchers to use.

**Main points:** Score by ROC AUC, as implemented, or by the challenge's F1 of the failure class?

**Record fields that disagree with the definition:**

- `year`: record `2020`, definition `2021`.

**Record judgment:** valid with a direct fit. An operator's own daily link counters with a rule-defined failure label, a next-day horizon the source scores, and inputs known at the end of the day. The panel found no leak that an honest model can use; the next-day rows inside a test window are covered by the protocol line. Failures come in storms, so the newest window's score rests partly on three storm days, the biggest just after five days when only NEC links reported.

**Issues for the curator:**

1. **Score by ROC AUC in place of the challenge's F1?**

   * **Problem:**
     - The challenge scored the F1 of the failure class on hard labels, and its problem statement asks for "identifying at least one radio link failure in the next day".
     - On the repaired label every scorer's F1 is 0.000 to 0.06 a window, on 0 to 39 true positives, so F1 cannot order methods.
     - The definition ships the binary fallback, ROC AUC, and overrules the source's metric on that evidence[^met4].
   * **Effect on the task:** under F1 the link's own past failure rate beats a regularised LightGBM in most fits; under ROC AUC the model leads that rate by +0.10 to +0.15 in September to December 2020, leads in May to August only within noise (+0.01 to +0.10) and ties it in January to April.
   * **Experiments:** re-run on the repaired label, three seeds, day-block bootstrap of the test days.

     | Window (newest first) | Positives | LightGBM ROC AUC | Rate ROC AUC | Lead (SE) | LightGBM F1 | Rate F1 | Best F1 on test |
     |---|---|---|---|---|---|---|---|
     | Sep-Dec 2020 | 414 | 0.80-0.86 | 0.694 | +0.10 to +0.15 (0.02-0.05) | 0.000-0.026 | 0.016 | 0.029-0.047 |
     | May-Aug 2020 | 250 | 0.72-0.82 | 0.709 | +0.01 to +0.10 (0.02-0.05) | 0.009-0.028 | 0.051 | 0.018-0.051 |
     | Jan-Apr 2020 | 156 | 0.76-0.77 | 0.765 | -0.01 to +0.01 (0.03) | 0.022-0.029 | 0.047 | 0.032-0.062 |

     - The F1 differences between the model and the rate are -0.04 to +0.01 with SEs 0.004 to 0.016; even a threshold chosen on the test rows reaches at most 0.06, so the threshold is not what keeps F1 low.
     - The challenge's own F1 rested on one query day per window (about 2,100 to 2,400 links), so a handful of positives.
   * **Consistency:** african_credit_scoring_challenge had its Zindi F1 overruled for ROC AUC on resolution (2026-10-26)[^prec]; here the case for F1 is stronger: Turkcell's problem statement asks for hard labels, while Zindi's did not.
   * **Panel:** the advocate, the domain practitioner and the claim auditor favour ROC AUC on resolution; the critic and the precedent checker asked for the re-run on the repaired label first and note the hard-label wording; the mediator gave the call to the curator. The re-run settles the critic's worry: with 67% more positives F1 still reaches at most 0.06.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC (implemented) | the binary fallback, F1 overruled with the measured reason | separates methods; scores the ranking an operator reviews | departs from a company's stated metric |
     | B | The challenge's F1 | `f1` of the failure class on hard labels, from the source | the source's own metric | 0 to 39 true positives a window; cannot order methods; the naive rate wins |

   * **Recommendation:** A, on resolution. **Decision:** A or B?

   **Notes for the AI:** on B, declare the source's F1 (`Metric.from_source` with the ITU-ML5G-PS-012 reference and the notebook's `average='binary'`), drop the overrule from the metric bullet, re-run `dataset check`, the task probes and TP-10 leg 1 by F1; with F1 the failure rate beats or ties the model in every window (Sep-Dec 0.016 against 0.000-0.026), so raise the scope (`No` + `Time-series (Forecasting)`) with the curator. On A, add a MET-4 Cases row for the overrule with the reason "resolution only; the source asks for hard labels".

   [^met4]: **MET-4** (Should): a competition's or the source's metric is kept unless measured evidence on the shipped splits overrules it; **MET-10**: a metric must resolve differences between methods on the shipped test windows.
   [^prec]: african_credit_scoring_challenge, CC 2026-10-26: the Zindi F1 overruled for the ROC AUC fallback on resolution.

**Review panel:** ship after changes (mediator). Full panel (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator); the rebuttal round was skipped because the advocate's and the critic's briefs converged. Made after the panel: the counters written in thousands repaired and the failure flag recomputed by Turkcell's rule (2,011 positives, was 1,204); the day's observed weather read again; the model-against-the-failure-rate comparison, the F1 evidence and the window statistics re-run on the repaired label over three seeds; the protocol line (score each test row on its own) extended with how often the next-day row gives the label away (97-99% of test rows); the forecast dated d backed by the 2021 test archive and the winner's code; within-day ROC AUC reported; the `Anonymized` tag dropped and the factual slips fixed. Claim audit: 42 claims, the validity claims hold; the met-real evidence, the TP-10 point estimates and four small facts refuted (all fixed). Blind review: would benchmark with a ranking metric and a licence note. Task gamer: only the next-day row lookup, which the protocol line bars. Disputed: the metric (issue 1). Task probes: the default LightGBM scores about 0.50-0.59 ROC AUC and the probes flag it. That is the untuned model breaking down on 0.1% positives (train AUC 0.73, log loss 20x the base rate; claim audit, PROBE row), not a sign the task is empty. The regularised LightGBM scores 0.72-0.86.

<details><summary>Mediator: turkcell_radio_link_failure_prediction_1m</summary>

**Summary**
- Recommendation: ship after changes. Validity holds (SEL-3, USE-1, SPLIT-1). The one validity defect, the label computed on damaged counters (PROV-13/USE-5, Must), can be repaired from the source.
- Changes needing no decision: repair the label, then re-run TP-10 leg 1 and the MET-4 evidence; read met-real (CLEAN-22 Must settles it); keep the LEAK-9 protocol line and add README wording; cite the 2021 archive for the forecast dated d; report within-day AUC; small fixes.
- For the curator: (1) keep roc_auc or the challenge's F1, after the re-run (MET-4, Should); (2) only if the repaired leg 1 does not hold, the scope (`No` + `Time-series (Forecasting)`); (3) only if you turn down the repair, keep Turkcell's flag with fit=approximate.
- The task gamer's exploit is a known leak, already covered by the LEAK-9 protocol line at `dataset.py:204`. Nothing new.

---

**JUDGMENT RECORD** (`turkcell_radio_link_failure_prediction_1m`, 2026-11-09)
- Decision: ship after changes.
- Rules decisive: PROV-13/USE-5 (Must) for the label repair; CLEAN-22 (Must) for met-real; LEAK-9 (Should, amended 2026-11-05) for the protocol line; MET-4 (Should) for the metric, which goes to the curator; TP-10 for scope, to be re-checked after the repair.
- Remedy rung: repair at the origin (rescale in `_clean`). No re-split, no exclusion.
- Exceptions: none.

**CHANGES TO MAKE NOW** (definition and re-runs for the finisher)
1. Label repair (PROV-13, USE-5, Must; also CLEAN-21).
   - In `_clean`, multiply by 1000 the fractional values of `unavail_second`, `bbe`, `es` and `ses`, and the ENK identity rows (`avail_time` + `unavail_second` = 86.4).
   - Recompute `rlf_today` and the label by Turkcell's rule.
   - Assert only on rows the damage does not touch.
   - Document under PROV-13/14.
   - Expected result: about 2,011 positives instead of 1,204 (per window 79→156, 143→250, 318→414).
   - Both briefs agree. Column auditor finding 1: Turkcell's rule matches 125 of 125 flagged rows in the 2021 release.
2. Re-run on the repaired label with several seeds and day-block SEs, and quote the numbers in the notes and issues:
   - TP-10 leg 1, the model against the link's failure rate (SEL-10/SEL-11, TP-10);
   - the MET-4 F1 vs roc_auc evidence;
   - `window_stats` (TP-9).
   - Use the regularised model. The untuned LightGBM diverges (gamer: +0.026/+0.086/+0.010 from regularising).
3. Read `met-real` as daily aggregates of day d at the site's nearest met-real station (CLEAN-22 Must: a column never leaves on a model score; EV-1).
   - The stated reason for leaving it out (5 of 6 fits worse) is seed noise: seed-matched mean +0.029, seed spread up to 0.07.
   - Turkcell offers it as "actual realizations", and the 2021 winner MLGrads reads day-d met-real.
   - It is known at the end of day d, so it is no leak.
   - No re-measure is needed to decide this. Report the re-measured number only as evidence.
   - Update the module docstring (line 23) and the curation note (line 169).
4. LEAK-9: keep the protocol line at `dataset.py:204`. It is the house remedy (medical_facility_operational_data, sepsis_prediction, 5g_energy_consumption). In the README, also state:
   - that a valid result requires each test row to be scored on its own;
   - that the next-day row of the same link is in the same test window for 97-99% of test rows;
   - that the window's daily positive count can be recovered from the test rows (corr 0.999).
5. Forecast report dated d (LEAK-10): keep it.
   - Replace the diverged-model test with the source evidence: the 2021 test archive ships reports dated up to the query day d, and MLGrads joins the report dated d to row d.
   - This answers the precedent checker's d-1 contradiction (0.815→0.655). The claim auditor shows those seeds differ by up to 0.05 per window, so the gap is fit noise as much as forecast age.
6. TP-9: report the within-day AUC (0.77-0.82; forecast-only about 0.50) beside the pooled AUC, and name the newest window as driven by a few days (86% of its positives on 3 days). Precedent: noaa_storm_events_damage, kept.
7. Small fixes:
   - Drop the `Anonymized` tag (line 136). Precedent PR #17 (amazon_employee_access, home_credit), and nothing here sets the case apart.
   - Record year 2021 (PROV-9: the release came out with the 2021 challenge).
   - Licence-unknown warning with the terms stated (EV-4, Must: a note, never an issue).
   - The horizon decision cites CLEAN-18. The right rules are SPLIT-12 and USE-5.
   - USE-5 note: hop-days count twice, once per link end (238 of 927).
   - Fix the factual errors in claims 11, 25, 26 and 31; recompute claim 12.
   - Leg 2: the README cites MLGrads' published code, not "winners not found".
   - Drop "tilt" as a next-day action.
   - The MET-4 reason should rest on resolution only and should say the 2021 problem statement asks for hard labels.

**ISSUES FOR THE CURATOR** (ranked)
1. **Metric: roc_auc over the challenge's F1** (MET-4, Should; MET-10).
   - Problem and effect: F1 is the source's metric. On the damaged label, F1 is 0.001-0.05 on 1-35 true positives, and the link's own failure rate beats LightGBM on F1 in Jan-Apr (-0.030, SE 0.012).
   - For roc_auc (advocate, domain practitioner, claim auditor): resolution. Precedent african_credit_scoring_challenge (2026-10-26).
   - For caution (critic, precedent checker):
     - The numbers are single draws on the damaged label, and about 67% more positives may weaken the resolution argument.
     - african_credit had source facts besides the measurement; here the 2021 problem statement asks for hard labels ("identifying at least one radio link failure").
     - The issue text uses SEL-10 scope as a ground. That coupling has no precedent, so drop it.
   - What would settle it: the re-run of change 2 (F1 resolution and roc_auc rank stability over seeds on the repaired label).
   - Decision needed: roc_auc (overrule on evidence) or F1.
2. **Only if the repaired TP-10 leg 1 shows no lead over the failure rate**: scope `No` + `Time-series (Forecasting)`.
   - Precedents: crms_phragmites_cover, stock.
   - Today: pooled +0.144 (SE 0.030) on one draw, but a tie in Jan-Apr across seeds. Leg 2 holds (MLGrads).
3. **Only if the curator rejects the repair of change 1**: keep Turkcell's flag with fit=approximate and say it misses about 40% of failure days. Not recommended: this is a Must-level label defect with a cheap, exact fix.

Protected grounds, codes vs words, scoring within groups and late-filled values stay open as issues alike across datasets, as the curator asked.

**DISPUTED POINTS, SETTLED BY RULE**
- **LEAK-9.** The critic calls it Must and asks for a protocol check; the advocate calls it Should and asks for the line only.
  - LEAK-9 is Should since 2026-11-05.
  - Its Case row prescribes exactly the protocol line plus the benchmark's check ("we can check if the model cheats").
  - Both sides accept the line, so the point is settled.
  - The gamer's fixes (one day per link per block, single-day windows) cost rows for a cheat the protocol already bars. They are not needed.
- **met-real.** The advocate is silent; the critic asks to re-measure.
  - CLEAN-22 (Must) decides it without a measurement: include it (change 3).
- **Everything else** in the two briefs converges.

**TASK GAMER EXPLOITS, MAPPED**

| Exploit | Gain over honest model C | Rule | Status |
|---|---|---|---|
| 1, 1b, 1c: the next-day row of the same link (`rlf_today(d+1)` or its counters) | +0.02 to +0.15 AUC | LEAK-9 | Known: protocol note at line 204 ("reading other test rows gives the labels away"). The measured gain matches the note, so no issue. Add 1c (counters alone also leak) to the README wording of change 4. |
| 2: whether the link has a next-day row | -0.006 to +0.017, at noise level | LEAK-9 | Covered by the same line. Not an issue. |

The gamer found no flaw that hurts an honest model. The split, row order, format and the subsample (label-independent) are clean.

**AGREED FACTS**
- 1,964,000 link-days, 1,963,348 rows used.
- Three temporal 4-month test windows with a 2-day gap. Training is a random 1M, label-independent (train y rate 0.000530 vs 0.000532 unsampled).
- Positive rate 0.061% on the current label.
- Counters of 1,000 or more were written in thousands in the training release. Turkcell's flag misses about 40% of rule-defined failure days.
- `fails_next_day(d) == rlf_today(d+1)` exactly, and that row is in the same window for 97-99% of test rows.
- The forecast report dated d is part of the challenge's own query-day data (2021 archive; MLGrads).
- The met-real leave-out evidence is seed noise. The winner uses day-d met-real.
- Leg 2 holds: MLGrads uses AdaBoost/XGBoost on point-in-time features.
- Ids (`site_id`, `mlid`, `mw_connection_no`) kept as categories is consistent with ashrae and rossmann.
- Licence unknown.
- No Must breaks the task once the label is repaired.

**CONSISTENCY** (from the precedent checker)
- Consistent: ids, storm windows (noaa), licence warning, year 2021, next-day horizon (digicow; cite corrected to SPLIT-12).
- Forecast dated d: departed from the mortgage/sberbank lag by one period. Now justified by a fact that sets this case apart: the source ships the report dated d with the query day. Consistent with a stated reason.
- `Anonymized` tag: departed from PR #17 with no distinguishing fact, so it is dropped (change 7).
- Metric: follows african_credit but with a weaker source fact. That difference is why it goes to the curator (issue 1), after the re-run.
- met-real: the change brings the definition back in line with CLEAN-22 (coad_colon_adenocarcinoma case).

</details>

<details><summary>Claim audit: turkcell_radio_link_failure_prediction_1m</summary>

CLAIM AUDITOR: turkcell_radio_link_failure_prediction_1m (record turkcell_radio_link_failure_prediction), 2026-11-09

Verdict: no validity claim is refuted. The label, the rlf rule, the LEAK-9 protocol line, the forecast issue time and
the nearest-station join all hold. The forecast issue time (claim 18) is now backed by the source itself, not only by a
reading. Refuted or weakened, in rank order:
(1) Claim 22, the evidence for leaving out met-real.tsv. It is seed noise, and the challenge winner used it.
(2) Claim 34, the TP-10 numbers. They are one lucky draw each. The leg-1 lead holds in two windows and is a tie in
    January to April. The untuned LightGBM is unstable.
(3) Claim 33, the horizon. It argues with F1, the metric it overrules.
(4) Small factual errors in claims 25, 26, 11 and 31.
New source evidence: the 2021 winner's code (MLGrads, ranked 1st) is a tabular AdaBoost on point-in-time features.
That settles TP-10 leg 2, which the builder marked "not found".

Scratch and logs (in the run folder): checks1-5.log, fits.log, fits2.log, the scripts, and mlgrads/ with the
winner's code fetched from GitHub.
Data: the shipped frame through dataset_io.from_definition (1,963,348 x 33, splits 1M/292,714, 1M/345,035,
984,904/338,546), the raw RegionA TSVs, and the 2021 test archive.

**TABLE  (claim | source | test | result | evidence | rule)**
1  | ITU challenge, Turkcell repo | claims.md 1; dataset.py | ITU Challenge_Archive/2021/ITU-ML5G-PS-012 README via gh api | HOLDS | README names PS-012 Radio Link Failure Prediction and points to Turkcell/ITU-AIMLin5GChallenge-2021 | PROV-8
2  | year 2021 | claims 2 | GitHub commit list | HOLDS | acee315c "add dataset" 2021-06-28; the TSVs inside are dated 26 May 2021 | PROV-9
3  | pin 4938c539, the newest commit | claims 3 | commit list | HOLDS | 4938c539 2022-07-05 is HEAD | -
4  | no licence | claims 4 | gh api .../license | HOLDS | 404 | EV-4
5  | paper F1 0.638 etc. | claims 5 | not re-read (the paper is paywalled) | UNTESTED | same block as the builder's | EV-7
6  | Turkcell example is a decision tree on the day's counters | claims 6 | read the notebook | HOLDS | cell 20: card_type, freq_band, 5 counters; cell 28: DecisionTree(max_depth=4) | -
7  | 3,681 link ends at 1,674 sites | claims 7 | count on the frame | HOLDS | frame 3,681 (site_id, mlid) and 1,674 sites; raw has 3,690 | -
8  | (datetime,site,mlid) and (datetime,mlid) unique | claims 8 | duplicated() on the raw table | HOLDS | 0 and 0. Note: 213 mlids report from 2 sites over time; a label on mlid alone gives the same 1,204 positives (80 more rows labelled) | -
9  | rlf == unavail>=120 & bbe>=100 | claims 9 | recompute on 1,992,986 rows | HOLDS | all equal; 1,219 rlf True | USE-5
10 | label = notebook's 1-day-predict, 1,204 | claims 10 | rebuild the notebook's join | HOLDS | 1,204 positives, 1,964,000 labelled, 28,986 without a next-day row; the notebook printed 1,204 | USE-5
11 | 13 days under 1,200 rows | claims 11 | count per day | HOLDS on raw | raw: 13 (5 of them 2-6 Oct 2020). The shipped frame has 19 days under 1,200 (2019-06-26, 2019-08-16, 2019-10-08, 2020-08-16, 2020-10-01 and 2020-11-14 drop below once the rows without a next day leave). Say which table | writing
12 | 4.3% against 1.5% without a next day | claims 12 | not recomputed | UNTESTED (cheap; the builder's own Decision table) | - | LEAK-22
13 | storms: half the positives on 10 days, 148 on 8 Oct 2020, 86% of window 0 on three days | claims 13 | count | HOLDS | top 10 days hold 49.6%; row date 2020-10-07 has 148; window 0's top 3 days hold 85.8% (148/67/58). See note A on 8 Oct 2020 | TP-9
14 | 318/143/79 positives, 32/55/55 failure days | claims 14 | count on the shipped splits | HOLDS | 318, 143, 79 | TP-9
15 | prediction point: end of day d | claims 15 | the test archive's query files | HOLDS | each 2021 window ships rl-kpis to day d and a query file for day d only (20210426: kpis 04-26..05-15, query 05-15) | USE-3
16 | nothing from d+1 is an input | claims 16 | code + forecast join | HOLDS | target_day = d+1 and leads >= 1, so the latest report is dated <= d | LEAK-10
17 | day<k> of a report dated r is r+k | claims 17 | forecast_timing.txt reread | HOLDS | rain AUC 0.72 at r+1 against 0.58 at r+0 (day 1); Tmax MAE 2.68 against 3.34 | LEAK-10
18 | a report dated r was issued by the end of r (a "reading") | claims 18 | NEW, the source: (a) the 2021 test archive's met-forecast against its query day; (b) how the 2021 winner joined it | HOLDS, and it is no longer only a reading | (a) in all four windows Turkcell ships met-forecast reports dated up to the query day d, both morning and evening, and no later (05-15, 06-13, 07-03, 09-05), with met-real to 23:00 of d. The challenge's own prediction-time data includes the report dated d. (b) MLGrads (ranked 1st, github vvijay83/MLgrads, dataprocess.py) joins the report dated d to row d on `datetime-station_no`. The builder's d-1 cost (0.818 against 0.726) moves with the fit as much as with the report: in exp_forecast_age the seeds differ by up to 0.05 per window | LEAK-10, EV-2 (the source's documents outrank a reading)
19 | evening over morning; agree on 96.3% | claims 19 | pivot day1 weather | HOLDS | 96.27% of 10,031 station-dates | -
20 | 97.1% of rows read a report dated d, 1.5% missing | claims 20 | value_counts of forecast_lead_days | HOLDS | lead 1 97.06%, NaN 1.51%, leads 2-5 1.42% | -
21 | the nearest of the 11 stations with forecasts; distance 0.08-19.7, mean 3.5 | claims 21 | recompute idxmin; symmetry of distances.tsv | HOLDS | 100% match; the matrix is symmetric (max abs diff 0); 0.083-19.65, mean 3.54; WS_17047 has 28 forecast days. Note: 494 of 1,674 sites have a nearer station without forecasts (met-real only). The winner did the same (nearest station with forecasts) | -
22 | met-real left out: day-d weather lowered ROC AUC in 5 of 6 fits (0.816 against 0.754) | claims 22, curation notes | refit with and without day-d met-real (daily aggregates at the site's nearest met-real station), seed-matched, the builder's regularised parameters | REFUTED as evidence | with met-real minus without, same seed: window 0 +0.037 / -0.015; window 1 +0.110 / +0.056; window 2 +0.001 / -0.014; mean +0.029. Refitting the same model with another seed moves AUC by up to 0.07 (window 1: 0.651 / 0.586). The builder's base+obs pairs also differ by 0.11 between seeds (0.816 / 0.704). The source and the winner use it: the problem statement offers "actual -precise- realizations", and MLGrads merges met-real of day d (temp, wind, humidity, precipitation) into every row. Day-d observations are known at the end of day d, so they are no leak | CLEAN-22 (Must: columns leave for what they are, never by a model score); EV-1; EV-8
23 | the 2021 test archive is not read | claims 23 | the query files | HOLDS | the query days carry no labels (NaN columns); the windows' own next-day labels would need day d+1, which is absent | -
24 | rlf_today and its counters stay; no longer history | claims 24 | TP-10 text | HOLDS by rule | TP-10 as amended 2026-10-26 allows the last observation. See claim 40 on the history | TP-10
25 | rxlevmax is 0 on 80 rows and "at most -14 elsewhere" | claims 25, curation notes, code comment | max of the nonzero values | REFUTED (the number) | 80 rows at 0 (41 links, none failing next day, holds), but the nonzero maximum is -10 and 92 nonzero rows lie above -14. The decision (0 dBm is no reading, set missing) still holds: on the 0 rows avail_time is 86.4 and the links are up | CLEAN-10, writing
26 | 1024 QAM merged into 1024QAM, 52,278 rows; "one link switches spelling on 5 March 2019" | claims 26, curation notes | links that use both spellings | REFUTED (the count) | 52,278 holds. Four links switch, each one way from "1024 QAM" to "1024QAM": A4WP 2019-03-05, A7VZ and A7ZV 2019-10-09, A4PW 2020-04-30. Both spellings run the whole period on both vendors (NEC 27,549 / ENK 24,729 rows of "1024 QAM"). The merge still holds | CLEAN-1, writing
27 | avail_time 86.4 on 95%; unavail/1000 + avail = 86.4 | claims 27 | count | HOLDS | 95.06% at 86.4; the identity holds on 1.87M frame rows. Note: unavail_second is capped at 999 (max 999.0), which the notes do not say | -
28-30 | tags; modulation and land cover unordered | claims 28-30 | read only | NOT RETESTED (column auditor's lane) | - | CLEAN-14
31 | ids kept as categories; 95.5-99.3% of test rows' mlid seen in training | claims 31 | seen share by (site_id, mlid); fits with and without ids | HOLDS (USE-10, known links), numbers by key | by link end (the definition's LINK): 98.6%, 94.7%, 98.4% (newest first); the 95.5-99.3% is by mlid. Regularised LightGBM without the ids is better in all 3 windows (+0.012, +0.003, +0.050): the ids are where the untuned model overfits (train AUC 1.000), not a reason to drop them | USE-10, CLEAN-3
32 | wind direction numeric | claims 32 | - | NOT RETESTED | - | CLEAN-14
33 | next-day label, not five-day | claims 33 | reread tp10_five_day.json against tp10_one_day.json | HOLDS as a choice; the ARGUMENT IS INCONSISTENT | It argues with F1 ("loses to that rate on F1 in all three") while the metric reason overrules F1 as unresolvable. On ROC AUC (lgbm_te against the rate) the windows are 5-day +0.098 / +0.099 / -0.024 (SE 0.026 / 0.027 / 0.012) and 1-day +0.223 / +0.172 / +0.038 (SE 0.061 / 0.059 / 0.031). My 1-day refits put the oldest window at +0.015 (below). Both horizons are roughly a tie in January to April; the gap between them is 1.9 SE. What decides is the 1-day's larger lead in the newer windows, and the five-day label's repeated rows and 111,000 rows without follow-up. The challenge scored both horizons; the 5-day has 4.3x the positives (5,159) | TP-10, MET-4, writing
34 | TP-10 leg 1: lgbm_te 0.894/0.839/0.836, rate 0.644/0.653/0.800, leads +0.22/+0.17/+0.04 (pooled +0.144, SE 0.030); untuned 0.861/0.819/0.799 | claims 34, metric reason, splits notes | (a) refit the same two models with 3 seeds each (fits2.py, the builder's parameters and features); (b) an operator-view naive forecast from the series itself (the link's failure count up to day d, including the test window's past days; 7/30/90/365 days and all history), plus the region's failures today | PARTLY REFUTED (stability). Leg 1 holds in two windows and is a tie in January to April | (a) lgbm_te refits: 0.853/0.848/0.832 (w0), 0.842/0.858/0.869 (w1), 0.815/0.816/0.813 (w2). Leads over the rate: about +0.20, +0.20, +0.015 (the builder: +0.22, +0.17, +0.04); the pooled lead is still about +0.14. The untuned LightGBM is unstable: w1 gives 0.651 / 0.586 / 0.811 over seeds 0-2, so in 2 of 3 refits it sits at or below the rate (0.653). w2 gives 0.768 / 0.801 / 0.786, at or below the rate (0.800). The "0.861 / 0.819 / 0.799" are single draws. (b) The link's own whole history up to d: 0.712 / 0.668 / 0.796 (the builder's static training rate: 0.644 / 0.653 / 0.800). Leads over it +0.13 / +0.19 / +0.02, so leg 1 holds against the series' own naive in w0 and w1. Adding today's region-wide failure count (link 365-day count plus region today): 0.716 / 0.733 / 0.838, which beats lgbm_te in w2 (0.815). Region today is cross-entity, so it is not leg 1's "own naive"; it is evidence that the storm signal is a panel signal | TP-10 (Must), EV-8, EV-9
35 | the challenge scored F1 of the failure class on hard labels, per horizon | claims 35 | the ITU archive README | HOLDS | "F1-scores of identifying at least one radio link failure in the next day and the following 5 days will be used to evaluate solution proposals". The notebook uses precision_recall_fscore_support(average="binary"), with its arguments swapped (pred, true), which F1 does not notice | MET-4
36 | F1 overruled for roc_auc | claims 36, metric reason | MET-4 to MET-11 against the source and our numbers | HOLDS ON RESOLUTION ONLY; two of its reasons do not carry | The resolution reason holds: 1 to 35 TPs a window, F1 0.001 to 0.05, and bootstrap SEs (0.011 to 0.018) as large as every difference. Weak: "F1 ranks the rate above LightGBM" is a result under F1, not evidence that F1 is wrong for the use case. "With F1 the task would fail TP-10" is circular, since TP-10 is judged by the declared metric. "A threshold cannot follow the storms" was not measured: the oracle-threshold F1 is also <= 0.05 (f1_oracle in tp10_one_day.json), so the threshold is not the problem. Missing from the reason: the challenge scored F1 on ONE query day per window (about 2,100 to 2,400 links, 4 windows), so its own F1 rested on a handful of positives, a unit our 4-month windows do not have (MET-2). The 2020 deck asks to "assess risks", a ranking decision. Turkcell is a company acting on the metric (MET-4's higher standing), so the overrule needs the curator. MetricSpec: original=None, reference=None (the same as the precedent african_credit_scoring_challenge; the reason names both) | MET-4, MET-2, MET-10, MET-11
37 | windows = four-month thirds of 2020; the oldest trains on 50.2% | claims 37 | the splits | HOLDS | 984,904 / 1,963,348 = 50.2%. The test dates are 2020-01-01..04-30, 05-01..08-31, 09-01..12-24 | SPLIT-14
38 | gap one day | claims 38 | max train date against min test date | HOLDS | train ends 2019-12-30 / 2020-04-29 / 2020-08-30; tests start the 1st | SPLIT-10
39 | sizes and sampling | claims 39 | split sizes; positives | HOLDS | 1M / 1M / 984,904 train with 530 / 561 / 664 positives; tests 292,714 / 345,035 / 338,546 | -
40 | fit direct | claims 40, task_summary | operator-view inputs against the shipped ones | WEIGH | The actor at the end of day d knows the link's failures inside the window and the region's failures today. The rows carry neither (rlf_today only), and a model refit at the window start cannot learn them. The link's whole history alone scores 0.71 / 0.67 / 0.80; a trailing summary of the series is allowed by TP-10. Not a validity break: the gap is information the operator has and the rows withhold | USE-1, USE-8, TP-10
41 | LEAK-9 protocol: the next row's rlf_today is the earlier row's label | claims 41, splits comment | join each test row to the same link end's row of d+1 in the window | HOLDS, now measured | next-day row present for 96.9% / 98.0% / 98.7% of test rows. Label equals that row's rlf_today on 100.000% of them. A lookup recovers 313/318, 121/143, 78/79 positives (the "not measured" in the notes can now be filled in) | LEAK-9
42 | no censoring at the release end; rows per day fall in Oct-Dec 2020 | claims 42 | rows per day | HOLDS | December 2019 2,798 a day against December 2020 2,618 (frame); a one-day label needs only d+1 | LEAK-24
MET | roc_auc computable per fold (MET-2) | dataset.py metric | scorer(container) with dummies | HOLDS | positives 318 / 143 / 79. A constant scores 0.5. Random scores give 0.539 / 0.494 / 0.469, so the noise of a random ranking is about ±0.03 in the oldest window, the same size as the leg-1 lead there | MET-2
PROBE | the probe's default LightGBM diverges | builder notes | default LGBMClassifier() on window 2 | HOLDS | AUC 0.562, log loss 0.098 (base-rate log loss about 0.005), train AUC 0.730: divergence, not overfitting | EV-3
LEG 2 | "2021 winners' methods not found" | builder report, P2 row | gh search for the ranked teams | REFUTED (now found) | MLGrads (1st) published its code: AdaBoost and XGBoost over day-d rl-kpis, rlf today, day-d met-real at the nearest met-real station, and all five forecast days of the report dated d at the nearest station with forecasts. No lag of rlf beyond today. A tabular model on point-in-time features, so leg 2 holds | TP-10

Note A (claim 13, the 8 Oct 2020 storm). All 148 failures on 2020-10-08 are ENK links at 120 sites, with 120 to 552
unavailable seconds. On 2-6 Oct only NEC links reported (Oct 4: 719 NEC, 4 ENK). met-real has no observations 1-7 Oct
and 280 rows on 8 Oct. The forecasts said "heavy thunderstorm" from three days ahead and WS_17064 observed 17 mm, so
the storm reading stands. But the biggest storm day of the newest window follows a five-day ENK reporting outage. A
curator may want this one sentence in the anomaly note: it decides 47% of window 0's positives.

**REFUTED AND UNTESTED, RANKED (principles: validity first, Must first)**
1. Claim 22: met-real.tsv left out on a model score (CLEAN-22 Must; EV-1). The evidence is fit noise. Seed-matched
   refits give +0.029 on average (3 up, 2 down, 1 flat), and refits of the same features differ by up to 0.07. The
   source offers the data, and the winning solution reads day-d met-real.
   What it changes: a legitimate input known at the prediction point is withheld for no reason the rules accept.
   Mildest remedy: read met-real as daily aggregates of day d at the site's nearest met-real station (the winner's
   join; 5-8% missing, pressure 51% missing). The other option is to keep it out with a reason CLEAN-22 accepts and
   drop the "5 of 6" sentence. Either way, correct claim 22 and the curation bullet.
2. Claim 34, TP-10 leg 1 (Must; the numbers behind the scope verdict). The direction holds in two windows. In January
   to April it is a tie: lgbm_te refits lead the rate by +0.013 to +0.016, and the untuned model sits at or below it.
   The numbers quoted in the metric reason and the notes are single draws: builder 0.894 in w0, refits 0.83 to 0.85.
   The untuned LightGBM's 0.819 in w1 is one of 0.59 / 0.65 / 0.81.
   What it changes: "every window ahead by point estimate" and "LightGBM leads that rate by +0.22, +0.17 and +0.04"
   overstate the case. The verdict "in scope by ROC AUC" rests on two of three windows.
   Mildest remedy: quote the leads as ranges over refits (about +0.20, +0.20, +0.01). Say January to April is a tie.
   Note that the untuned LightGBM is unstable here (the probe-divergence note covers it). Add the operator-view naive
   (the link's whole history: 0.71 / 0.67 / 0.80) next to the static rate.
3. Claim 36, the F1 overrule (MET-4, Should; the curator's call, issue 1). Resolution is the one reason that carries.
   Mildest remedy: rewrite the reason around resolution. Cite the oracle-threshold F1 (<= 0.05 for every scorer) in
   place of the threshold argument. Add that the challenge's F1 was on one query day per window. Drop the
   TP-10-pass reason, which is circular.
4. Claim 33, the horizon (CLEAN-18/TP-10, Should). The decision may stand, but its text leans on F1, which the
   dataset declares unresolvable. Mildest remedy: argue on ROC AUC, the repeated rows and the follow-up only.
5. Claim 40, fit direct (USE-8, Weigh). The operator knows the link's failures within the window and today's region
   count; the rows carry neither. Mildest remedy: say so in fit_reason, or add a trailing failure count of the link
   (TP-10 allows summaries of the series up to the prediction point).
6. Factual errors (writing, Should):
   * claim 25: "at most -14 elsewhere". It is -10; 92 rows lie above -14.
   * claim 26: four links switch spelling (dates above), not one.
   * claim 11: 13 days on raw, 19 on the shipped frame.
   * claim 31: 95.5-99.3% is by mlid; by link end it is 94.7-98.6%.
   * claim 27: unavail_second is capped at 999, which is unsaid.
   * claim 41: "not measured" can now carry the numbers (313/318, 121/143, 78/79 positives recoverable).
   * Builder report: "2021 winners' methods not found". MLGrads is found, and leg 2 holds.
7. Untested:
   * claim 5: the paper is paywalled.
   * claim 12: not recomputed (cheap).
   * claims 28-30 and 32: the column auditor's lane.
   * Whether the 8 Oct 2020 storm is partly a reporting artefact (note A): needs Turkcell's word.

</details>

<details><summary>Column audit: turkcell_radio_link_failure_prediction_1m</summary>

COLUMN AUDITOR: turkcell_radio_link_failure_prediction (folder turkcell_radio_link_failure_prediction_1m), 2026-11-09

VERDICT: no leak. One validity problem the builder missed: the training release's counters are damaged. In some rows,
values of 1,000 or more were written as thousands with a decimal point ("22.425" for 22,425 s). Turkcell's rlf flag, and
so our label, was computed on the damaged numbers, so it misses about 40% of the failure days under Turkcell's own rule
(P5 PROV-13, P3 USE-5). The fix in the definition is cheap. The counters it touches also fail CLEAN-21 (one unit per
column) whatever the label decision is.

Prediction point (first curation bullet): the end of day d, after the day's counters. Label: rlf of the same link end
on d+1. Codebook: none beyond column names (ReadMe_RLF.txt lists files only; the notebook builds labels and reads
card_type, freq_band, severaly_error_second, error_second, unavail_second, bbe, rxlevmax). Meanings below are
therefore marked "name" (from the column name and the notebook) where nothing else says.
Scratch: the run's work files (kpis.parquet = raw rl-kpis, clean.parquet = the definition's _clean output,
nextinfo.parquet).

**FINDING 1 (P5 PROV-13 / P3 USE-5, Must; strong): mixed scale in the counters damages the label**
Evidence:
- unavail_second: the integers run 0-999 only (max 999). Every fractional value (2,637 rows) is <= 86.4. A day
  holds 86,400 s, so no outage of 1,000 s or more appears as an integer.
- ENK rows with a fractional unavail_second: avail_time + unavail_second = 86.4 on 95.5% of 1,847 rows, so both are in
  thousands of seconds. ENK rows with an integer unavail_second: avail_time*1000 + unavail_second = 86,400 on 97.6% of
  6,942 rows, so unavail is in seconds. The unit changes row by row, and within one link (594 links mix the two).
- Turkcell's own 2021 test release (test_2021*/rl-kpis.tsv, 184,253 rows, downloaded, not read by the definition) has
  integer seconds up to 86,400 and avail_time 86,400 / 172,800 / 259,200. It has no fractional unavail or bbe. Its
  rlf equals (unavail_second >= 120 and bbe >= 100) on 125 of 125 flagged rows. Of those 125 rule rows, 38.4% have
  unavail >= 1000 or 1000 <= bbe < 100,000, which is the range the damage would push below the thresholds.
- In training, the same damage hits bbe (4,101 fractional rows; a count of blocks cannot be fractional), error_second
  (328), severely_error_second (26) and avail_time (86.4 = 86,400 s, but 900.0 on 867 rows is 900 s).
- The damaged rows are never flagged: rlf = 0 on all 2,637 rows with a fractional unavail. 301 of them have
  bbe >= 100 as published.
- Rule after rescaling the fractional values by 1000:
  - unavail_second only: rlf days 1,219 -> 1,520 (+301);
  - unavail_second and bbe: 2,052 (+833, so 40.6% of the rule's days are missing from the source flag; the 2021
    release's 38.4% matches).
  - Next-day positives: 1,204 -> 2,011.
  - Per window, by the day d of the row: Jan-Apr 79 -> 156, May-Aug 143 -> 250, Sep-Dec 318 -> 414.
  - Failure days: 332 -> 470.
  - Top-10 days hold 43% of the repaired positives, against 50% now.
- The assert in _clean passes only because Turkcell computed rlf after the damage. The label is not Turkcell's rule
  on the true counters, and it drops mainly the long outages (1,000 s or more unavailable), the most severe ones.
- The fractional test undercounts: a value like 2,000 written "2.0" or "2.000" reads as 2. For ENK the avail_time
  identity resolves most such rows. For NEC (avail_time is always 86.4) it cannot.
Remedy (mildest that resolves the problem, a repair in the definition): in _clean, multiply by 1000:
  - the fractional values of unavail_second, bbe, error_second and severely_error_second;
  - for ENK, also the integer-looking unavail values where avail_time + unavail = 86.4.
Then recompute rlf_today and the label with Turkcell's rule, and assert it against the published flag only on the
undamaged rows. Write the repair into the curation notes (PROV-13/PROV-14) and rerun TP-10 and the task probes,
because the positives grow by about 67%.
Alternative for the curator: keep the source flag as the challenge's label (the challenge was scored on it) with
fit="approximate" and a note that it misses the outages of 1,000 s or more. The features would still be repaired
(finding 2). I recommend the repair: the 2021 release shows Turkcell's rule on true seconds.

**FINDING 2 (P7 CLEAN-21, Should): one unit per column for the five counters**
This holds whatever finding 1 decides.
- unavail_second, bbe, error_second and severely_error_second mix seconds (or counts) with thousands.
- avail_time is in thousands of seconds, except the plain values below 1,000 s (900.0 = 900 s, which sorts above a
  full day's 86.4).
- The curation notes say "avail_time ... the day's 86,400 seconds in thousands" and keep it as published. That reading
  is right for most rows but misses the 900 s rows and the mixed scale of the others.
Remedy: the same rescaling. Put avail_time in seconds: x1000 on the values with a decimal part or <= 259.2; integers
>= 260 are already seconds.

**FINDING 3 (P4 LEAK-22 to LEAK-26): rows without a next-day row: no hidden-failure signal, a note suffices (as shipped)**
- 28,986 rows lack a d+1 row: 14,796 on days when the whole network reports under 1,200 rows (reporting gaps) and
  14,190 link-specific gaps.
- In the link-specific gaps, the flag on day d is 5x the base (0.32% against 0.061%). When the link returns on d+2
  (62% of gaps), its failure rate is 0.011%, below the base next-day rate of 0.061%. A missing day is not a failure
  in disguise.
- Bound: if the gap rows had 5x the base next-day rate, about 45 positives would hide (3.7% of 1,204).
- The rows are dropped unlabelled, not set to No, so LEAK-25 does not apply. The horizon is one day, so there is no
  right-censoring at the release end (LEAK-24) and no cap (LEAK-26).
- The 4.3% vs 1.5% note in the definition is right and enough.

**FINDING 4 (P4 LEAK-10): no day-d counter reflects d+1; the forecast is issued by day d (reading supported)**
- Calendar-day windows:
  - Hourly met-real rain on the storm days falls inside the failure rows' own date. On 2019-05-24 the rain fell at
    00-06h and the 112 failures are dated the 24th, not the 23rd. On 2020-10-08 the rain fell at 12-24h and the 148
    failures are dated the 8th.
  - ENK and NEC fail on the same date in shared storms (2019-08-21: 49 ENK and 32 NEC), so neither vendor is shifted.
  - unavail > 0 on day d before a failure on d+1, against unavail > 0 on d+1 after a failure on d: ENK 0.090 vs
    0.077, NEC 0.025 vs 0.018. The two directions are symmetric, so this is persistence, not a window reaching into
    d+1.
- avail_time > 86.4 (13,233 rows: 98.1, 172.8 = 2 days, 259.2 = 3 days): it runs per link (86% of the next rows are
  also > 86.4). The same symmetric test gives 0.381 vs 0.318. The 2021 release has 172,800 and 259,200 as well. These
  are multi-day or multi-channel sums, not a window crossing into d+1. Their meaning is unknown, so a note is enough.
- The forecast's day k is the report date plus k: the reports dated 2020-10-05, 10-06 and 10-07 give "heavy
  thunderstorm" as day 3, day 2 and day 1 for the 10-08 storm, which agrees with the builder's temperature test.
  Morning and evening reports agree on 96.4%. Issue by the end of the report date stays a reading, as the definition
  says. No objection.
- Configuration fields (modulation, capacity, card_type, freq_band, adaptive_modulation) change on 0.01-0.02% of
  days, and never next to a positive. They are static attributes, not states set after the outcome.

**FINDING 5: lagged target rlf_today (TP-10, SEL-11): acceptable as built, but its numbers rest on the damaged flag**
- rlf_today is known at d, and the operator reads it.
- Only the last observation ships, no longer history of the flag.
- If finding 1 is repaired, rlf_today, the link-rate baseline and TP-10 leg 1 have to be rerun on the repaired label.

COLUMN TABLE (33 columns of the cleaned frame; 1,964,000 rows)
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
type | vendor of the radio equipment, ENK/NEC (name; vendor-specific counter formats confirm it) | yes, static | category | fine | -
date | day d of the counters | yes | datetime, split column | fine | -
tip | which end of the hop the row reports, NEAR/FAR (name) | yes, static | category | fine | -
mlid | anonymised link-end id, unique per day | yes | category (known links, USE-10) | fine | CLEAN-3 keep
mw_connection_no | hop id shared by the ends (2 ends on 1,399 of 1,794 hops; up to 6); 3.4% of link ends change hop | yes | category; dtype probe "numeric_levels" answered: a code, correctly not numeric | fine | CLEAN-12
site_id | anonymised site | yes | category | fine | -
card_type | anonymised radio card model | yes, static (changes 0.01% of days) | category | fine | -
adaptive_modulation | adaptive modulation on/off | yes, static | category | fine | -
freq_band | anonymised band f1-f5, 1.2% missing | yes, static | category | fine | -
severely_error_second | seconds of the day with severe errors (name; ITU G.826 SES) | yes, day d | float; 26 rows scaled /1000 | cleaning problem | CLEAN-21, PROV-13
error_second | errored seconds of the day (name; ITU ES) | yes | float; 328 rows scaled /1000 | cleaning problem | CLEAN-21
unavail_second | unavailable seconds of the day | yes, calendar day (finding 4) | float; 2,637 rows in thousands (<= 86.4), integers <= 999 | cleaning problem, and it defines the label | CLEAN-21, PROV-13, USE-5
avail_time | available time; thousands of seconds (86.4 = a full day), 900.0 = 900 s; > 86.4 = multi-day or multi-channel sums (unknown) | yes (symmetric test) | float, mixed scale | cleaning problem | CLEAN-21
bbe | background block errors, a count | yes | float; 4,101 fractional rows (thousands) | cleaning problem, and it defines the label | CLEAN-21, PROV-13
rxlevmax | maximum received level, dBm | yes | float; 0 -> missing (80 raw rows, 73 kept; 34 are full-day outages, so a no-reading caused by day d's outage, not by d+1) | fine | CLEAN-10
capacity | link capacity (unit unknown, probably Mbit/s), 161 missing | yes, static | float | fine | -
modulation | QAM level with vendor suffixes | yes, static (changes 0.02%) | category, unordered (suffixes have no stated order) | fine | CLEAN-14
rlf_today | Turkcell's failure flag on day d | yes | category (bool) | fine as a lagged target; inherits the damage of finding 1 | TP-10, SEL-11
fails_next_day | target: rlf of the link end on d+1 | target | decoded No/Yes | label damaged: misses about 40% of the rule's failure days | PROV-13, USE-5
groundheight | site ground height (m, presumably) | yes, static site table | float | fine | -
site_clutter_class | site land cover, 21 classes | yes, static | category, unordered; dtype probe "ordinal_like" answered: two crossed scales (height x density) plus open, tree, water, industry, so no single order | fine | CLEAN-14
station_no | nearest station that publishes forecasts (9 used) | yes, fixed geography | category | fine | -
station_distance | site-to-station distance, distances.tsv unit (probably km) | yes | float | fine | -
station_height | station height | yes | int | fine | -
station_clutter_class | station land cover, 6 classes | yes | category, unordered; probe "ordinal_like" answered as above | fine | CLEAN-14
forecast_weather | forecast weather word for d+1 (19 words) | yes, report dated <= d (finding 4) | category | fine | LEAK-10
forecast_temp_max/min | forecast temperatures for d+1 | yes | float; 1.5% missing (no report within 5 days, not caused by the outcome) | fine | -
forecast_humidity_max/min | forecast humidity for d+1 | yes | float; 2.2% missing | fine | -
forecast_wind_dir | forecast wind direction, degrees | yes | float (a cycle shipped as a number, house rule) | fine | -
forecast_wind_speed | forecast wind speed | yes | float | fine | -
forecast_lead_days | lead of the report used (1 on 97.1% of rows) | yes | float, 1-5 | fine | -

PROBLEMS RANKED (principles.md)
1. P5/P3, PROV-13 + USE-5 (Must): the label and rlf_today are computed on damaged counters and miss 833 of 2,052 rule
   failure days. Remedy: repair in _clean (rescale the fractional values, recompute the flag), then rerun TP-10 and the
   probes. Else keep with fit="approximate" and a note (curator decision).
2. P7, CLEAN-21 (Should): the five counters mix units. Remedy: the same rescaling, avail_time to seconds. Cheap and
   safe.
3. P4, LEAK-22 to LEAK-26: the gap rows show no hidden-failure signal. Keep the existing note.
4. P4, LEAK-10: none. Counters are on the calendar day; the forecast is issued by d (a supported reading); the static
   fields are pre-outcome.

</details>

<details><summary>Split audit: turkcell_radio_link_failure_prediction_1m</summary>

SPLIT AUDITOR - turkcell_radio_link_failure_prediction / turkcell_radio_link_failure_prediction_1m (2026-11-09)

VERDICT: right with notes. The regime, windows, gap and sampling hold. Three notes go into the README, none needs a re-split.

Work (in the run folder): load.py, geom.py + geom.log, models.py + models.log/models.json. Frame and splits
loaded from the definition through dataset_io (1,963,348 rows, 1,204 positives, dates 2018-12-31 to 2020-12-24).
Quick model: LightGBM 600 trees / 63 leaves / lr 0.03, ids as categories, no target encoding, one seed, 4 threads.

1. Regime (USE-10, SPLIT-13): right. The use case is a daily risk review of the operator's own links, so the links are
   known entities and the split is temporal. Test rows whose link end (mlid) has training rows: 99.25% / 95.48% / 98.84%
   (newest first). The link's history is legitimate, and the link's training failure rate is a known-entity feature, not
   a shortcut. Share of test positives on links that also failed in training: 37.7% / 40.6% / 59.5%. The builder's
   naive-rate AUC (0.644 / 0.653 / 0.800) stays below the model's in every window. A grouped split would test a cold
   start that the use case does not have, so I did not run one.

2. Gap and label delay (SPLIT-9, SPLIT-10): right, and the minimum that is correct. For each window, the newest
   training row is test_start - 2 days (2020-08-30, 2020-04-29, 2019-12-30). Its label is rlf on test_start - 1, which
   is known at the end of that day, when the model is refit. Exactly one day of rows is dropped (2,820 / 2,865 / 2,149
   rows). No training row has a label that falls after the refit point. A gap of 0 would put rlf(test_start), the first
   test day's flag, into the training labels. So 1 day is both needed and enough.
   Inside a test window, row d's label is the rlf_today of row d+1. The LEAK-9 protocol line in the splits_comment covers
   this: each row is scored on its own, and transductive use is called out. Reading rlf_today on row d+1 as a feature is
   legitimate, because it is known at that row's own prediction point.

3. Storm-shaped windows (TP-9, SPLIT-15, SPLIT-18): right with a note (ranked P6, a value issue, not validity).
   Positives per window: 318 / 143 / 79. The top 3 days hold 273 / 61 / 12 of them (86% / 43% / 15%), and the newest
   window has 148 on 2020-10-07. My question was whether the score only rewards spotting the storm day. It does not:
   - Mean within-day AUC (days that have positives) is 0.787 / 0.774 / 0.816 (32 / 55 / 55 days). The pooled AUC is
     0.849 / 0.826 / 0.827, and with the top 3 days removed it is 0.808 / 0.787 / 0.835.
   - A model on the forecast only (forecast_* + station_no) scores 0.752 / 0.702 / 0.532 pooled but 0.51 / 0.50 / 0.46
     within a day. So the weather carries the cross-day part, and the link counters carry the within-day ranking that
     the task is about.
   - An oracle that knows each day's true failure rate scores 0.975 / 0.898 / 0.828. In the newest window, day-level
     signal alone could carry a model far, so that window's score moves with how well a model times the storms.
   SPLIT-18's short weather windows would hold 1 to 9 positives in most two-week blocks. Newest window by 14 days:
   6, 58, 154, 71, 15, 1, 9, 3, 1. That fails TP-9, so the four-month windows are the right trade (SPLIT-17). The
   4-month length is a refit cadence, not a weather quantity, as the splits_comment says.
   Remedy (wording only): state the within-day AUC (~0.77-0.82) beside the pooled one in the README. It shows that a
   window's score is not just storm timing, and it flags that the newest window is the most day-driven (oracle 0.975).

4. Reporting gaps, Oct-Dec 2020 (SPLIT-9 / selection): no problem, a note. 2020-10-01..06 and 2020-11-14..15 hold
   ~690-724 rows a day (partial days, not missing days; no calendar date is missing after 2018-12-31). Rows per day,
   monthly mean: Oct 2,310, Nov 2,486, Dec 2,618, against ~2,800 before.
   Rows dropped for lacking a next-day row: 2.2% of the newest window's rows (6,603), 1.2% / 0.4% of the older two.
   Only 9 of the newest window's dropped rows have rlf_today True. Of all dropped rows with a later row of the same link
   end, that later row fails at 0.0006, the base rate (0.00061). So the gaps do not hide failures. The label needs a
   row on d+1, which conditions the population on the next day's reporting. This is mild (2.2% at most) and already
   noted. No filter needed.

5. 1M sampling of the two newer train sides (row_budget): right. The draw is uniform over time (0.596-0.603 per
   quarter in window 0, 0.754-0.760 in window 1) and stratified on the label (rate 0.000530 against 0.000531 eligible;
   530/885 and 561/743 positives kept). Gap rows are excluded.
   Cost of the cap, measured with the quick model: window 0 AUC 0.849 on 1M random against 0.875 on all 1.67M; window 1
   0.826 against 0.847 on all 1.32M. The newest 1M scores 0.814 / 0.819, worse than the random 1M, so a random draw is
   the better 1M. The cap costs about 0.02-0.03 AUC and lowers the level of both newer windows. Its effect on model
   rankings is unknown. This is single-seed, and the day-block SE is 0.03-0.06, so the gap is within noise.
   Remedy: none required by the rules. The `_1m` suffix and the version notes already say it. Optionally add the
   measured cost to the README.

6. Window geometry (SPLIT-14, SPLIT-15): oldest train side 984,904 rows = 50.2% of the frame. Three windows, newest
   first, consecutive with no overlap between test windows. Window 0 ends at the last labelled day, 2020-12-24 (115 days).
   Fine.

No findings at the Must level. Nothing to re-split.

</details>

<details><summary>Domain practitioner: turkcell_radio_link_failure_prediction_1m</summary>

Domain practitioner report: turkcell_radio_link_failure_prediction_1m (2026-11-09)
Actor: Turkcell network operations centre (NOC), transmission team; each night it looks at tomorrow's risk on its
microwave backhaul hops in one region.

VERDICT
Fit: direct (USE-1, USE-8). Actor, moment and decision are real and the label is Turkcell's own failure rule
(USE-5). The test windows are the next months on known links (USE-10).
Metric: partly scores the decision. Keep roc_auc over the challenge's F1 (issue 1, option A; MET-4 overrule
supported, MET-6, MET-8, MET-9). Pooled ROC AUC mostly rewards spotting storm days, not picking links within a day
(numbers below). The README should say so.
Horizon: keep the next day (issue 2, option A). The use_case text should drop "tilt" as a next-day action.
Persistence: a model that mostly flags links that failed today would be worthless. The shipped model does not do
that: today's flag scores ROC AUC 0.50 to 0.53.

MY OWN MEASUREMENTS (dp.py, dp.log, dp_results.json; the builder's regularised LightGBM
with the in-model link target encoding, on the shipped splits; windows Sep-Dec / May-Aug / Jan-Apr 2020; 318 / 143 / 79
positives)
- Pooled ROC AUC. Model 0.858 / 0.831 / 0.834. Link's past failure rate 0.646 / 0.661 / 0.800. Today's flag 0.503 /
  0.521 / 0.525. My rule of thumb (a forecast-only model times the link's failure rate) 0.794 / 0.778 / 0.704.
- ROC AUC within a day (per day, weighted by positives). Model 0.685 / 0.715 / 0.813. Rate 0.657 / 0.662 / 0.800.
  Within a day the model leads the link's history by only +0.03 / +0.05 / +0.01. The pooled lead is +0.21 / +0.17 /
  +0.03, so most of it is between days.
- Storm-day detection: ROC AUC over days of the mean score, where a positive day has 5 or more failures (4 / 6 / 1
  such days). Model 0.84 / 0.95 / 0.56. Rate 0.31 / 0.31 / 0.49. The forecast carries this. The model without
  forecast columns scores pooled 0.745 / 0.649 / 0.672 and within a day 0.762 / 0.651 / 0.672. In the storm-heavy
  window, the forecast lifts the pooled score and lowers the within-day score.
- Daily top-k (what my crews could follow up). With the top 10 link ends a day (of about 2,700), the model catches
  3.1% / 7.0% / 11.4% of the failures and the link's failure rate 2.2% / 14.7% / 25.3%. Precision is under 2% for every
  scorer at every k in 10, 27, 50 and 135. With a window-wide budget of 20 a day on average, the score free to pile
  onto storm days: model 13.8% / 18.9% / 17.7%, rate 7.2% / 18.2% / 29.1%.
- Unit: 238 of the 927 hop-days with a failure fail at both ends. In the raw rl-kpis, 1,219 failing link-end-days
  are 927 hop-days. I act per hop (`mw_connection_no`), so a quarter of the failure events count twice.

Q1. INPUTS AT THE MOMENT
- Day's counters (ES, SES, UAS, BBE, RxLevMax, capacity, modulation): yes. The NMS closes the 24-hour PM bin at
  midnight, so in practice I score just after midnight, a few hours before the day I protect starts, not "at the
  end of the day". This changes nothing in the data, but it leaves little lead time (below).
- Today's failure flag: yes. It is a rule on the same counters.
- Forecast issued by today: yes. The national met service's next-day forecast is out by the evening. The builder's
  timing tests support the reading (LEAK-10).
- Site, hop, equipment, frequency band, land cover: yes. This is inventory.
- Inputs I would always have but the task lacks, in order of how much they matter:
  (a) The link budget: hop length, the frequency in GHz rather than f1 to f5, the fade margin and the rain zone.
      Rain fade is driven by these, and Turkcell's 2020 deck lists "link length" among the KPI data. They are not
      shipped. The link id and its target encoding stand in for them, which is acceptable for known links (USE-10).
  (b) The link's history beyond today: failures, UAS and BBE over the last 7 to 30 days. The 2021 challenge's own
      query design gave 20 days of history per window. The model reaches it only through the link id. USE-10 allows
      the previous outcome as a feature, so a curator could add lags. This is not a must: a method can learn the
      link's level from the id.
  (c) The far end and the neighbours: the other end of the hop's counters and failures at nearby sites today. Both
      are spatial storm signals.
  (d) The rain amount and radar nowcasts. The forecast gives only a weather category, with no mm. The observed
      weather (met-real) is left out on measured grounds. I accept that.
- Nothing shipped is unavailable to me.

Q2. TARGET
The next-day RLF flag (UAS >= 120 s and BBE >= 100) is the event I act on: an outage of the hop, at the resolution
of a day. I would want a probability, which I rank or threshold depending on how busy tomorrow looks, not a class
fixed in advance.
Horizon: next day versus any failure in 5 days.
- Next day fits what I can do overnight: put a field crew on standby, pre-route traffic over the IP/MPLS ring or the
  1+1 protection, and suppress expected alarms.
- 5 days fits planning: crew rosters, spares, and maintenance windows I would not open into a storm.
- Tilt (realignment) is a field job of days, and a modulation floor or added redundancy is a planning change. None
  of them is a next-day action.
- Turkcell's own deck lists them as a question ("What actions can we take ... Tilt, modulation, redundancy, etc.?")
  and states the goal as "predict the RL failures to assess risks".
- Both horizons are real. Since the 5-day label fails the naive-profile test in Jan-Apr and repeats one event on up
  to 5 rows, I agree with next day (issue 2, option A).
- Change: the use_case should read "assess tomorrow's risk and prepare (crew standby, traffic rerouting)" instead of
  "act ahead (tilt, modulation, redundancy)". The deck leaves the actions open.

Q3. ROW AND TEST DATA
- A row (one link end on one day) is close to my unit, the hop on a day (the double count above). It is not worth a
  rebuild, but the README could say it.
- The test data is what I face: the same links in the coming months, a model refit every 4 months (USE-10, SPLIT
  temporal). A new region (the challenge's framing) would be a different task. Known links are the operator's case.

Q4. WOULD I USE IT
- As a storm-day alert, yes: it ranks the high-failure days well in the two windows that have them (0.84 and 0.95).
  That is worth a night shift's attention.
- As a list of which links to protect on a given day, not yet: within a day it barely beats the links' own failure
  history, and in Jan-Apr and May-Aug the plain history list catches more failures at 10 a day (25% versus 11%; 15%
  versus 7%).
- I would trust it once it beats the history list within storm days. I distrust it because 86% of the newest
  window's positives fall on three days, so any number on this task largely reports whether those days were caught
  (issue 3, TP-9).
- Answer to "a model that mostly flags links that already failed": it would lose to my rule of thumb. Failures barely
  persist (today's flag: 2 true positives among 315 flags in Sep-Dec). The shipped model is not that model. It beats
  my rule of thumb pooled (0.86 / 0.83 / 0.83 against 0.79 / 0.78 / 0.70).

Q5. METRIC (MET-1, MET-4, MET-6 to MET-9)
- The challenge's F1 of the failure class on hard labels does not score my decision. At under 2% precision at any
  workable k, F1 is 0.001 to 0.05 on 1 to 35 true positives. That is noise, and it puts the link's history above a
  better ranker. The MET-4 overrule on measured evidence is sound. Note: one 2020 paper reports a macro-averaged F1
  (70% / 77%), which is another quantity. The 2021 problem statement's class F1 is the one cited.
- What I would pick a model by in practice: the failures caught in my daily top k hops, i.e. recall or precision at
  a fixed daily k, per day, per hop (MET-7).
- The source fixes no k, and inventing one is barred (MET-7). With 79 to 318 positives a window, top-10 counts of 2
  to 25 failures would resolve models worse than ROC AUC. average_precision is not justified by imbalance alone
  (MET-9), and its floor (0.0006) makes it near zero for every scorer (AP 0.003 to 0.012 in the builder's
  tp10_one_day.json).
- So I keep the roc_auc fallback (MET-8). Pooled over the window, it scores a mix: mostly "is tomorrow a storm day",
  and partly "which links". That is the right mix for a NOC risk score, but the README should name it. A within-day
  (grouped by date) ROC AUC would score the link choice alone. I would not switch to it: it throws away the day-level
  signal, which is real value to me, and it rests on even fewer positives per group.
- Verdict on the metric: partly. roc_auc over F1, with a README line that pooled ROC AUC is driven largely by
  storm-day detection.

GAPS RANKED BY HOW MUCH THEY CHANGE THE TASK
1. The score rests on storm days. A pooled metric over windows where 3 days hold 86% of positives (Sep-Dec)
   measures storm detection more than link selection (TP-9, issue 3). Within-day lead over the link's history:
   +0.01 to +0.05.
2. The link budget (hop length, GHz, fade margin) and the link's history are missing as explicit inputs. An operator
   always has them. For known links the id stands in.
3. The use_case's actions (tilt, modulation, redundancy) are not next-day actions. This is a wording fix and does
   not change the fit.
4. The unit is the link end, not the hop: 238 of 927 failing hop-days count twice. A note, not a rebuild.
5. The prediction point is just after midnight, not the evening: a few hours of lead. A note only.

WHAT A DOMAIN EXPERT WOULD CHANGE
- Reword the use case: risk review for tomorrow, crew standby and rerouting. Name storm-day alerting as most of what
  the score measures.
- Optionally add the link's lagged failure count and UAS over 7 and 30 days as inputs (USE-10). Not required.
- Keep roc_auc, and keep the next-day label.

SOURCES
- Turkcell, ITU AI/ML in 5G Challenge 2020 deck (Salih Ergut, 22 July 2020), slides 8, 9 and 14:
  https://itu.int/en/ITU-T/AI/challenge/2020/Documents/ITU-AI-Challenge-Turkcell-RLF-Salih-Erg%c3%bct-v1.0.pdf
- ITU challenge page (2020, PS-036): https://www.itu.int/en/ITU-T/AI/challenge/2020/Pages/Turkcell.aspx
- The 2021 PS-012 statement as quoted in the record (F1 of identifying at least one RLF next day / 5 days).
- The ITU Journal paper of 2022 (S-JNL-VOL3.ISSUE2-2022-A13): only its search snippet was read (the PDF is over
  10 MB). The snippet gives the macro F1 of 70% / 77% for a decision tree.
- Turkcell repository ReadMe_RLF.txt and rl-kpis.tsv (local copy); builder_report.md, tp10_one_day.json,
  window_stats.json.
- General practice of microwave transmission operations (ITU-T G.826/G.828 PM counters, ACM, 1+1 protection): my own
  domain reading, not from a cited source.

</details>

<details><summary>Blind review: turkcell_radio_link_failure_prediction_1m</summary>

BLIND REVIEW: turkcell_radio_link_failure_prediction
Inputs used: data.parquet (200,000-row sample of 1,963,348), task.md, and the public sources
(Turkcell GitHub README + ReadMe_RLF.txt, ITU Challenge_Archive 2021 PS-012 README, arXiv 2407.05197 abstract). No other local files opened.
Scratch: m.py (temporal LightGBM check).

VERDICT: Include with changes. The task is real and the label is built correctly, but the positives are very rare and fall on a
handful of storm days, so scores will be noisy and mostly decided by weather. Recast the ID columns, state the split and
metric, and document the source's missing license before including it.

WHAT THE TASK IS
A Turkish mobile operator (Turkcell) has microwave backhaul radio links. Each row is one link end (mlid + NEAR/FAR) on one day.
The row holds that day's link KPIs (errored/unavailable seconds, bbe, rxlevmax, capacity, modulation), the link configuration,
site and weather-station metadata, and a regional weather forecast. The target is whether that link end records a radio link
failure (RLF) the next day. The ITU AI/ML-in-5G 2021 challenge (PS-012) states it directly: "predict the occurrence of radio link
failures in: i) in the next day ii) in the following 5 days", scored by F1. A network-operations team would use this the day
before to schedule maintenance, re-route traffic or stand by for weather-driven outages. This is a real use.

WHAT IS RIGHT
- Target construction verified on the sample. For 19,971 (mlid, tip) pairs observed on consecutive days, fails_next_day(d) equals
  rlf_today(d+1) in every case (15/15 positives, 19,956/19,956 negatives).
- The leaky "met-real" (realised weather) table is not used. Only forecast columns appear: forecast_lead_days is 1 in 97% of rows
  and 2-5 in the rest, so a stale forecast fills gaps. This matches a deployable setting.
- The temporal split on date matches use. No exact duplicate rows. Missing values are low (forecast columns 1.5-2.2%, freq_band 1.2%).
- Values are plausible: avail_time is in kiloseconds (86.4 = a full day), and avail_time*1000 + unavail_second = 86400 for 95% of rows.
  rxlevmax runs from about -26 to -45 dBm, and the modulations (128QAM-2048QAM) are realistic.

CONCERNS (most to least serious)

1. Extreme rarity and day-level clustering of positives -> high-variance, weather-lottery evaluation.
   - Positives are 119/200,000 = 0.06% in the sample, so about 1,170 in the full data.
   - All 119 sample positives fall on 56 of 725 dates. The top 5 dates hold 53 of them (2020-10-07: 16; 2019-05-23: 10;
     2019-08-20: 10; 2020-09-28: 10; 2020-10-17: 7).
   - Positives cluster on forecast thunderstorms. "heavy thunderstorm with rain showers" has a rate of 0.83% against
     0.02-0.04% under clouds.
   - The month-level rate swings from 0 (2019-11, 2020-01, 2020-03, 2020-05, 2020-07, 2020-11, 2020-12) to 0.37% (2020-10).
   - In-sample, an oracle that knows each date's failure rate gets AUC 0.98. Most of the ranking is "which day is stormy", and
     every row on a given day shares the same few forecast values.
   - On the sample, temporal LightGBM with all columns gave AUC 0.22 / 0.40 / 0.75 on three 2020 windows, which held
     6 / 16 / 27 positives. The full data has about 10x more positives, but the clustering stays the same, so a test window that
     holds only one or two storm days is effectively a few independent events.
   - Change:
     - Choose test windows that each contain several event days. If the windows are not fixed yet, check the positive count
       and the number of distinct event dates per window.
     - Report a rank metric suited to rarity (AUC-PR or log loss) and a confidence interval.
     - Consider the source's "failure in the next 5 days" target, which is less sparse.
     - If the windows cannot hold enough event days, downgrade or exclude.

2. High-cardinality identifier columns invite overfitting, and one is typed as numeric.
   - mlid has 3,454 levels, site_id 1,672 and mw_connection_no 1,782. mw_connection_no is stored as int64, so models treat an
     ID as an ordered number. station_no has 9 levels.
   - On the sample, removing mlid/site_id/mw_connection_no/station_no lifted temporal AUC from 0.22->0.78, 0.40->0.72 and
     0.75->0.91. With all columns, mlid was the 3rd most important feature by gain.
   - Change: drop mw_connection_no and site_id, or cast them to categorical. Consider dropping mlid, or keep it as categorical
     only if per-link identity is intended. With roughly one positive per link over two years, per-link memorisation is noise.

3. Single-day snapshot only: no lags or history.
   - Each row carries only same-day KPIs. Failures do not persist: rlf_today=True leads to fails_next_day=True in only 2 of 125
     cases. Useful signal (multi-day KPI trends, a link's past failures) is absent.
   - This is a legitimate tabular framing, but the features available for the link itself are weak.
   - Change (optional): add a few lagged KPI and rolling-failure-count features, computed causally per link.

4. Licensing and provenance.
   - The Turkcell GitHub repo has no license (the GitHub API returns "license": null). The data is described as anonymised operator
     data released for the challenge and for academia ("This data gives the opportunity for researchers to use live network data").
   - Change: record that redistribution terms are unclear. Link to the source rather than re-hosting, or get permission.

5. Forecast timing not verifiable from the prepared table.
   - I cannot tell whether the forecast row joined to date d was issued on or before d, or whether the forecast is for day d or
     day d+1 (the failure day). forecast_lead_days >= 1 suggests it was issued at least a day earlier, which is fine.
   - The join of region/station to link (station_distance 0.4-2.8 km) also looks sensible.
   - Change: document the exact join (forecast issue date, forecast target day, station mapping) in the task card.

6. Minor preparation issues.
   - About 4% of rows cover partial days: avail_time + unavail sums to 17,100 / 18,000 / 13,500 s and so on, and 605 rows reach 98,100 s,
     which is more than a day. These are probably different reporting intervals or aggregation artefacts. Error-second counts on those
     rows are not comparable to full days. Consider adding a coverage column or normalising.
   - modulation has variants such as "2048QAM*" and "512QAM(QO)". Fine as a categorical.
   - forecast_wind_dir is a circular angle stored as linear 0-360. Acceptable.
   - The target is stored as category "No"/"Yes". Fine.

WHAT I COULD NOT CHECK
- The full 1.96M table. Positive counts, the exact test windows and per-window event-day counts are extrapolated from the 10% sample.
- The raw 7z archives (rl-kpis.tsv and the others) were not downloaded or rebuilt. I did not re-derive the joins, the handling of
  last days or link gaps (whether rows without a next-day record were dropped or labelled No), or the forecast alignment.
- Whether the challenge's own train/test (Data vs Test_20210125 archives) were merged here. The date range 2018-12-31..2020-12-24
  suggests they were.
- The Elsevier paper (doi 10.1016/j.compeleceng.2022.107742) is paywalled; I read only the abstract-level description. arXiv 2407.05197's
  abstract does not name the Turkcell data.

</details>

<details><summary>Task gamer: turkcell_radio_link_failure_prediction_1m</summary>

TASK GAMER REPORT - turkcell_radio_link_failure_prediction (target fails_next_day, ROC AUC, 3 temporal test windows)

VERDICT: fully gameable. The label of row (link, day d) is the rlf_today flag of the same link's row on day d+1,
and that row sits in the same test window (and in data.parquet), so a one-line lookup scores AUC 0.93-0.99 and a
model with next-day columns scores 0.9997-1.0000 against an honest 0.86-0.90.

Data facts: 1,963,348 rows = one row per (mlid, date), 725 days 2018-12-31..2020-12-24, sorted by date.
Positive rate 0.061% (test positives: 318 / 143 / 79 in r0 / r1 / r2). Training = random 1,000,000-row subsample
(r0, r1) or all rows (r2) of the days before the test window, with a 2-day gap (train max = test min - 2 days).

HONEST BASELINES (scripts run.py, run_reg.py; logs run1.log, run2.log)
  A untuned LightGBM, all features (date -> day_of_year, month):            r0 0.832  r1 0.775  r2 0.794
  B regularised LightGBM (15 leaves, min_child 300, lambda 10), all feats:  r0 0.858  r1 0.861  r2 0.804
  C as B but without link ids (mlid, site_id, station_no, mw_connection_no): r0 0.858  r1 0.904  r2 0.855  <- best honest
  Noise: C + one random column: 0.861 / 0.906 / 0.865 (spread 0.003 / 0.002 / 0.010). A + random column moved
  A by +0.018 / +0.046 / +0.008, so the untuned model is unstable on ~550 training positives.
  C + honest history (same link's counters 1,2,3,7 days back, expanding failure rate): 0.856 / 0.909 / 0.876
  (-0.001 / +0.005 / +0.021: noise-level to mild; legitimate signal, not an exploit).

EXPLOITS RANKED BY GAIN (vs honest model C)
| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
| 1 | Next-day row of the same link: rlf_today(d+1) == fails_next_day(d) exactly (1,933,132/0 and 0/1,155 crosstab; 49 positives have no next row) plus next-day counters, as model features | run_reg.py lead_nohc | 0.858/0.904/0.855 | 0.99986/0.99969/0.99999 | +0.142/+0.096/+0.145 | No: day d+1's row exists only after d+1 | drop rlf_today (or every same-day outcome counter) from the rows, or keep only one row per link per test window / leave a gap; see below |
| 1b | Same, as a rule without any model: pred = rlf_today(d+1) + 1e-3*unavail_second(d+1) | run.py rule_lead | same | 0.992/0.926/0.994 | +0.134/+0.022/+0.139 | No | same |
| 1c | Next-day counters only, without the flag (unavail_second, SES, ES, BBE, avail_time of d+1) | run_reg.py leadnl_nohc | same | 0.99984/0.99962/0.99998 | +0.142/+0.096/+0.145 | No | dropping rlf_today alone is NOT enough: the failure is also visible in d+1's unavail_second (rlf_today=True always has unavail_second>=120) |
| 2 | Presence of the link's next-day row (row missing on d+1 -> y rate 0.17% vs 0.06%) | run_reg.py hasnext_nohc | 0.856/0.909/0.876 (C+hist) | 0.850/0.926/0.886 | -0.006/+0.017/+0.009 (noise 0.003-0.010) | No: whether the link reports tomorrow is future | small, mixed; same fix as 1 |

Mechanism of 1: the target was built by shifting each link's daily RLF flag back one day, and the shipped rows keep
the unshifted flag (rlf_today) and the counters that record the outage. Test windows are 4 months of consecutive
days, so for 97-99% of test rows the d+1 row of the same link is also a test row (positives covered: 98.4% / 84.6%
/ 98.7% within the test set alone; r1 rises with the 2020-09-01 rows of data.parquet). Mildest fix: the task cannot
keep both "every day of every link" in the test window and the same-day counters; either (a) score only one test
day per link-window block (e.g. sample one day per link per week and drop its successor rows from the scored
set and from what participants see), or (b) ship test windows as single days separated by >= 1 unseen day. Dropping
rlf_today and unavail_second/avail_time/SES/ES/BBE kills the signal too but destroys the honest features.
The daily positive count of a test window is also recoverable from next-day rlf_today (corr 0.999 of daily rates).

FLAWS THAT HURT AN HONEST MODEL
None in the split itself: training subsample is label-independent (train y rate 0.000530 vs unsampled 0.000532,
r0; 0.000561 vs 0.000564, r1), the 2-day gap means no training label is from the test window, and no training row
is dated at or after the test window. The only honest gain found is a model choice: dropping the high-cardinality
link ids (C vs B: 0.000 / +0.043 / +0.051) and regularising (B vs A: +0.026 / +0.086 / +0.010). Not a task flaw.

ATTACKS THAT FOUND NOTHING
- Row order: within-day position AUC 0.489 / 0.499 / 0.490; global row index in test 0.348 / 0.534 / 0.411 is just
  date (rate drifts inside the window; using it needs test labels). Rows within a day are not sorted by mlid or id.
- Format artefacts: decimals / whole-number share / last digit of every numeric column, AUC 0.457-0.538 (largest
  avail_time decimals 0.538, station_distance last digit 0.457, both static/link-level); missing-value patterns
  y rate 0.00035-0.00062, no signal. forecast_lead_days >1 has lower y rates but is a legit forecast field.
- Identifiers: mlid / site_id / mw_connection_no are static link keys; as features they hurt (see B vs C), no
  encoding of time or label found.
- Copies across the split: each (mlid, date) is unique; the same link appears on both sides by design (temporal
  split over a fixed fleet); history of the link is legitimate.
- Training rows that tell the future: none (see above).
- Test-set statistics: daily row count vs daily y rate corr -0.08; same-day fleet rlf rate vs y rate corr 0.016.
- Paired end of the same connection (mw_connection_no) next day: subsumed by exploit 1; not run separately.
- Web: Turkcell ITU-AIMLin5GChallenge-2021 repo and ITU pages; no public leak / magic-feature thread found. The
  challenge's own framing (predict RLF from historical KPIs and weather) is what the kit reproduces; the d+1 row
  leak comes from shipping consecutive days in the test window, not from the source. Looking rows up in the public
  rl-kpis files would also give the labels (not ranked).

COULD NOT CHECK
- The original challenge files (not downloaded) to confirm how rlf_today/fails_next_day and the forecast join
  (forecast_lead_days) were derived; whether the "forecast" fields might be the realised weather would decide one
  more possible leak, but forecast fields carry only weak single-feature AUC (0.39-0.65) and C does not lean on them.
- Single seed per config; noise spread from one random column per split.

</details>

<details><summary>Precedent check: turkcell_radio_link_failure_prediction_1m</summary>

PRECEDENT CHECK: turkcell_radio_link_failure_prediction (folder turkcell_radio_link_failure_prediction_1m), 2026-11-09
Read: principles.md (Tensions, Exceptions and amendments, Consistent judgement); metrics.md, task_probes.md,
selection.md, use_case.md, leak_checks.md, evidence.md, provenance.md, cleaning_features.md (rules + Cases) in df-large;
the definition, the record, builder_report.md, probes (tp10_one_day.json, window_stats.json, exp_forecast_age.csv),
register.json (flags + decisions for MET-4/6/10, TP-9/10, SEL-10/11, CLEAN-18, USE-10, EV-4, PROV-9, LEAK-10),
blind_reviewer.report.txt and column_auditor.report.txt (the only other reports present at 12:57).

VERDICT
Eight calls checked. Five are consistent with precedent (ids, storm windows, licence warning, year, horizon with a
rule-ID correction). The metric overrule departs from MET-4's default with a stated reason and follows
african_credit_scoring_challenge, but it is coupled to the TP-10 scope test in a way no precedent has been; one prompt.
The forecast report dated d departs from the house's conservative lag for undated releases with a stated reason, and
the builder's own model test partly contradicts that reason; one prompt. The `Anonymized` tag departs from the
no-marker cases of PR #17 without a fact that sets it apart; one prompt.

SUMMARY TABLE
| # | Call | Standing | Closest precedents |
|---|---|---|---|
| 1 | ROC AUC over the challenge's F1 | departs with a stated reason; reasonable, but the TP-10 coupling needs the curator | african_credit_scoring_challenge (overrule, 2026-10-26, Lennart); loan_default_prediction_imperial_college (overrule + MET-4 amendment, 2026-11-05, Lennart); zillow_prize, rossmann_store_sales, hiva_agnostic (kept, 2026-10-21) |
| 2 | TP-10 / SEL-10 / SEL-11, rlf_today as the last observation | consistent (leg 1 by declared metric, Lennart's 2026-11-08 reading; leg 2 by the rain_in_australia amendment) | g_research_crypto_forecasting (2026-10-22, 2026-11-08), rain_in_australia (2026-10-26), ashrae (2026-10-15); rejected: crms_phragmites_cover (Andrej, 2026-11-02), stock, appliances_energy_prediction (2026-10-22) |
| 3 | next day over five days | consistent; the rule cited (CLEAN-18) is the wrong one | digicow_farmer_training_adoption_challenge (one of the source's horizons shipped, 2026-10-21); SPLIT-12 |
| 4 | site_id, mlid, mw_connection_no kept as categories | consistent | ashrae_great_energy_predictor_iii_1m (building_id, site_id), rain_in_australia (Location), rossmann_store_sales (Store); USE-10 corporate_credit_rating |
| 5 | forecast from the report dated d | departs from the lag-by-one-period precedent with a stated reason; the reason is partly contradicted by exp_forecast_age | mortgage, sberbank_housing_market_forecasting (LEAK-10/LEAK-7 row, Lennart, 2026-10-21); bias_correction (USE-6) |
| 6 | storm-dominated windows (TP-9) | consistent | noaa_storm_events_damage (kept, 2026-11-08, Lennart); seismic_bumps (retired, 2026-09-30) far smaller |
| 7 | meta_license_unknown accepted | consistent | bank_customer_churn, diabetes_3, hr_analytics, mobile_churn, pricing_game_2016_french_fleet, wisconsin_local_government_property_insurance_fund; EV-4 cases lucas_topsoil (2026-09-23), african_credit et al. (2026-10-21) |
| 8a | year 2021 (record says 2020) | consistent | PROV-9 "the first commit that shares them"; expresso_churn_prediction (2020 kept: same files re-run in 2021), the reverse fact here |
| 8b | `Anonymized` tag / marker | departs without a fact that sets it apart | no marker: amazon_employee_access, home_credit_default_stability (PR #17, Lennart, 2026-10-27); with marker: pricing_game_2016_french_fleet (all levels masked), medical_facility_operational_data (clock shifted), sendy (coordinates) |

DETAIL PER CALL

1. Metric (MET-4, MET-6, MET-10).
- MET-4 (Should) keeps a competition's hard-label threshold metric ("its threshold metric (F1, a cost matrix) is
  kept: methods choose their threshold on the training side") and overrules it only by MET-2 or on evidence that it is
  biased or wrong for the use case, "from the source ... or measured on the shipped splits". The ITU challenge's
  problem was set by Turkcell, the operator that acts on it, so the full bar applies (not the 2026-11-05 lesser-standing
  clause).
- The stated reason is measured: F1 0.001-0.05 per window on 1-35 true positives; the link's rate beats LightGBM on F1
  in Jan-Apr (-0.030, SE 0.012); a training-side threshold cannot track a fourfold swing in positives (79 to 318). The
  resolution leg matches african_credit_scoring_challenge ("one default moves F1 by about 0.05"). So: departs from the
  default, with a reason, by a precedent; reasonable under the ranking (P6 Should, no Must broken).
- What differs from african_credit: that overrule had three facts, two from the source (the host asked for
  "the probability of loan default" binned into risk grades; forum gaming). Here the source fact is weaker: the 2021
  PS-012 asks for "identifying at least one radio link failure" (hard labels); the only probability-leaning words are
  the 2020 deck's "to assess risks" (PS-036, another region). The reason does not quote it; it should, or say none
  exists. No gaming evidence.
- The coupling: issue 1 lists "keeping F1 would make the task read as forecasting (SEL-10)" as a ground for A. No
  precedent let the metric choice decide scope. TP-10 judges leg 1 "by the task's declared metric"; at
  g_research (2026-10-22) the declared metric was the source's, and it is the source's metric here that fails. The
  metric must stand on MET-4's own terms first, and TP-10 then follows the declared metric; the issue text should drop
  the scope argument as a reason for A. Prompt 1.
- Pattern: no dataset in the working copy declares F1 (grep of metric declarations); the two competition F1s met so far
  (african_credit, turkcell) are both overruled on resolution. Not a third exception (overrules under MET-4's own clause
  are applications, not exceptions), so no amendment is due; but MET-4's "its threshold metric (F1) is kept" sentence
  now has no kept F1 case, and MET-10's diversity factor (F1 would be the collection's only F1) cuts the other way. Worth
  a line in the issue.
- Drift: Lennart's MET-4 calls run kept (2026-10-21) -> overruled on evidence (2026-10-26) -> amended (2026-11-05); each
  change recorded, so no unrecorded drift.

2. TP-10, SEL-10/SEL-11, rlf_today.
- Leg 1 by ROC AUC (the declared metric): lgbm_te leads the link's failure rate +0.22 / +0.17 / +0.04 (SE 0.06 / 0.06 /
  0.03), pooled +0.144 (SE 0.030). Ahead in every window by its point estimate, the interval read pooled: Lennart's
  reading on g_research (2026-11-08), as for ashrae and rain_in_australia. Consistent. Under crms_phragmites_cover's
  bar (Andrej: rejected at a 1.1% lead, 0.9 SE) the newest-but-two window alone (1.3 SE) would be borderline; the
  pooled lead is about 5 SE, so the crms rejection is not a like case. The stronger model (target encoding inside the
  model; untuned LightGBM ties in Jan-Apr) matches ashrae (default LightGBM lost, 1,000 trees won).
- Leg 2: only today's flag ships (rain_in_australia amendment, 2026-10-26: the last observation, known and read by the
  actor). Consistent. Gap against the precedents: ashrae and g_research had their top solutions read (no lags); here the
  2021 winners are not found and the data paper's best model reads sequences (abstract). rain_in_australia had no
  competition, so "leg 1 then carries the test" applies, but the README should say leg 2 is unverified for winners.
- Dependency: the column auditor's finding 1 (mixed-scale counters damage the label) would change rlf_today, the rate
  baseline and every leg-1 number; if repaired, TP-10 must be re-run before this verdict holds.
- Note the metric coupling of call 1: leg 1 fails by F1. If the curator keeps F1 (prompt 1, b), crms_phragmites_cover
  and stock / appliances_energy_prediction are the precedents for `No` + `Time-series (Forecasting)`.

3. Horizon (next day over five days).
- CLEAN-18 is "Remove a `Multi-target` tag when the dataset predicts one target"; the record carries no such tag, so
  there is nothing to apply and the citation (from the screening, carried into the brief) is the wrong rule. The
  horizon choice falls under SPLIT-12 ("the horizon is a human judgment from the source") and USE-5.
- Consistent with digicow_farmer_training_adoption_challenge (one of the source's labelled horizons shipped, the 7-day,
  2026-10-21) and with Turkcell's first-named label ("1-day-predict"). The five-day label's double counting of one
  failure and its 111,000 rows without follow-up are reasons of their own; its TP-10 failure in Jan-Apr should not be
  the lead reason, for the same coupling as call 1.

4. Ids as categories.
- USE-10: known link ends (95.5-99.3% of test rows have training rows); the split is temporal. ashrae keeps
  building_id and site_id as categories "the test hours belong to meters seen in train, as in the competition";
  rain_in_australia keeps Location; rossmann keeps Store. CLEAN-3 keeps an id that carries meaning; the cleaning rule
  "a code the source ships as a number is a category" covers mw_connection_no. Consistent.
- The blind reviewer's "drop or recast" (sample AUC 0.22 -> 0.78 without ids) rests on default LightGBM on a 10% sample,
  the configuration the builder showed diverges on this target (probe_divergence.json); EV-3, a probe artefact, not a
  reason to depart from ashrae. His point that mw_connection_no is int64 in the clean-room file is a typing question for
  the column auditor (who reads it as a category in the definition).

5. Forecast from the report dated d (LEAK-10).
- Closest house practice: data joined by a date whose release time is unknown is lagged "by one period of its own
  frequency" (LEAK-10/LEAK-7 row, Lennart, 2026-10-21: mortgage, sberbank_housing_market_forecasting). The definition
  takes the report dated d instead, on a reading ("Recorded twice a day" only) supported by three tests: rain skill by
  lead with no day-1 jump; storm days forecast three days ahead; a thunderstorm score equal from reports d, d-1, d-2
  (0.728 / 0.723 / 0.722). That is a stated distinguishing fact (a forecast is dated by issue, not by the period it
  describes), so it departs with a reason.
- Against the reason: exp_forecast_age.csv shows the report dated d-1 worth far less to a model than the report dated d
  in May-Aug 2020 (ROC AUC 0.815 / 0.809 with d, 0.655 / 0.604 with d-1, 0.620 / 0.614 with no forecast), and less in the
  other windows (0.842 -> 0.793 / 0.823; 0.811 / 0.781 -> 0.730 / 0.749). If the d report were issued by the end of d,
  a one-day-older forecast of the same day d+1 should lose little, as the single-feature test says. The untuned
  LightGBM diverges on this target, which may explain part of it, but this is the one number the reading turns on. The
  column auditor (finding 4) accepts the reading; the claim auditor should test claim 18 on a regularised model. Prompt 2.
- No exception to a Must is involved yet: if the reading holds, LEAK-10 is met; if it does not, LEAK-10 requires the
  d-1 report (the precedent's lag), not a note (LEAK-38 covers only fields "no test can establish").

6. Storm-dominated windows (TP-9).
- TP-9 (Must) is about a handful of positives per window: seismic_bumps had 0-5 per window (retired). Here 79 / 143 /
  318 positives on 55 / 55 / 32 failure days and 53 / 117 / 253 link ends (window_stats.json); even counted by day, far
  above a handful. Concentration (86% of the newest window's on three days) matches noaa_storm_events_damage, kept
  2026-11-08 by Lennart with "a few events decide the deviance" noted. Consistent; the note in the README is the
  precedent's remedy. Not an issue for the curator by precedent; the builder's "possibly no issue" is right.

7. Licence-unknown warning (EV-4).
- EV-4 (Must): a licence is never evidence and never an issue; a one-line note. Six definitions accept
  `meta_license_unknown` with the terms stated (bank_customer_churn, diabetes_3, hr_analytics, mobile_churn,
  pricing_game_2016_french_fleet, wisconsin_local_government_property_insurance_fund). The proposed text states what
  the README asks and says. Consistent. The blind reviewer's concern 4 (licensing) must not become an issue (EV-4;
  release-checklist item, as the Zindi terms for african_credit, 2026-10-21).

8a. Year 2021 (PROV-9).
- PROV-9 (Must): the first publication, "the first commit that shares them": 28 June 2021 ("add dataset"). The 2020
  challenge (PS-036) used another region ("the data belongs to a new region"), so 2020 is a different dataset's year.
  expresso_churn_prediction kept 2020 because its 2021 re-run used the same files; the fact here is the reverse.
  Consistent; the record's `year` should be corrected (a field correction, as the builder says).

8b. `Anonymized` tag and marker.
- selection.md "Anonymized data": no marker when "only ids were replaced while the features keep their meaning" or
  "every column is described and only the values of some categories are codes" (amazon_employee_access,
  home_credit_default_stability; PR #17, Lennart, 2026-10-27). Here every column has a plain name (bbe,
  unavail_second, rxlevmax, modulation, the forecast variables); masked are the ids, the region, card_type's models and
  freq_band's f1-f5. That is the no-marker case. The tagged siblings differ: pricing_game_2016_french_fleet masks the
  levels of its rating factors, medical_facility shifts the clock (timing uncheckable), sendy masks coordinates. The
  definition gives no fact that sets turkcell apart. Prompt 3.

DRAFTED PROMPTS (issue shape; for the mediator to place in REVIEW.md)

Prompt 1 (on issue 1, the metric)
Consistency check: Does the metric overrule stand on its own, without the scope test as a reason?
- **Problem:**
  - The issue offers "keeping F1 makes the task forecasting" as a ground for ROC AUC, so the metric choice decides scope.
  - At g_research_crypto_forecasting the source's own metric judged the naive-profile test; here it is the source's metric that fails it.
  - Of african_credit_scoring_challenge's three facts, only the resolution one carries over: no gaming, and the 2021 problem asks to identify failures.
- **Background:** F1 is 0.001 to 0.05 per window on 1 to 35 true positives; ROC AUC leads the link's rate by +0.22, +0.17, +0.04 (pooled +0.144, SE 0.030); no dataset in the working copy declares F1.
- **Options:**

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Overrule on resolution alone (implemented, reason reworded) | Keeps ROC AUC; the reason cites resolution and the 2020 deck's "assess risks", and drops the scope argument | Same ground as african_credit; the scope test then follows the declared metric as written | One source fact fewer than african_credit had |
| b | Keep the challenge's F1 | Declares F1; the task fails the naive-profile test and goes `No` with `Time-series (Forecasting)` | MET-4's default for an operator-set competition; adds the collection's only F1 | Scores of 0.001 to 0.05 that hardly separate methods; loses a real operator task |
| c | Amend the naive-profile test | Leg 1 is read on a threshold-free metric when the declared one cannot resolve the windows | Separates the scope test from the metric choice for good | A rule change on one case |

- **Recommendation:** (a); the measured resolution is the fact african_credit was overruled on, and the scope argument adds nothing the rule needs.
- **Decision:** (a), (b) or (c)?
[met4]: MET-4 (Should), metrics.md; african_credit_scoring_challenge, overruled 2026-10-26 (Lennart); amended 2026-11-05 on loan_default_prediction_imperial_college.
[tp10]: TP-10 (Must), task_probes.md, leg 1 "measured by the task's declared metric" (amended 2026-10-22, g_research_crypto_forecasting); SEL-10, SEL-11.
[met10]: MET-10 (Weigh): resolution; diversity (Andrej, 2026-11-02).

Prompt 2 (on the forecast report dated d)
Consistency check: Is the report dated d known by the end of day d, given that a one-day-older report is worth far less to the model?
- **Problem:**
  - The house lags a release of unknown timing by one period (mortgage, sberbank); this definition takes the report dated d on a reading.
  - Single-feature tests support the reading, but a model with the report dated d-1 drops from 0.815 to 0.655 ROC AUC in May to August 2020, about as low as with no forecast (0.620).
- **Background:** rain skill by lead 0.72 / 0.71 / 0.70 / 0.69 / 0.66, no day-1 jump; thunderstorm score 0.728 / 0.723 / 0.722 from reports d, d-1, d-2; the untuned LightGBM used for the model test diverges on this target.
- **Options:**

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep the report dated d (implemented), after a regularised re-run | Keeps the reading if a regularised model shows a small d-1 loss; the notes give both tests | The forecast a planner holds at day's end; three timing tests agree | Rests on a reading the files do not state |
| b | Take the report dated d-1 | Lags the forecast one report, as the precedent for unknown release times | No timing reading needed; Must side safe | Loses the newest forecast if the reading is right |
| c | Keep d with a stated-risk note only | Ships as is, the gap in the notes | No change | A note does not settle a timing a test can probe |

- **Recommendation:** (a), conditional on the re-run; (b) if the d-1 drop stays large on a regularised model.
- **Decision:** (a), (b) or (c)?
[leak10]: LEAK-10 (Must, amended 2026-11-08); the LEAK-10/LEAK-7 row of leak_checks.md Cases (Lennart, 2026-10-21): mortgage, sberbank_housing_market_forecasting.
[leak38]: LEAK-38 covers only fields whose timing "no test can establish".

Prompt 3 (on the `Anonymized` tag)
Consistency check: Should the `Anonymized` tag go, as for amazon_employee_access, since only ids and some category values are masked?
- **Problem:**
  - Every column has a plain name and meaning; masked are the ids, the region, card_type's models and freq_band's f1 to f5.
  - The no-marker list names exactly this case (amazon_employee_access, home_credit_default_stability).
- **Options:**

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep the tag (implemented), with a stated fact | Keeps tag and marker, recorded as an exception: the region and station positions are masked, so the weather join cannot be checked against public weather | The one thing the masking hides that bears on a leak check | The join was checked internally (distances.tsv, lead skill); a weak fact |
| b | Drop the tag; no marker | Removes `Anonymized` from `data_tags`; the record gets no marker; the notes keep "anonymised codes" | Matches the PR #17 cases | None found |
| c | Reopen amazon_employee_access and home_credit_default_stability | Marks those too | One rule for all masked-code cases | Reverses a decided call |

- **Recommendation:** (b).
- **Decision:** (a), (b) or (c)?
[anon]: selection.md, "Anonymized data", the no-marker list (Lennart, 2026-10-27, PR #17); definitions.md, `data_tags`.

NOT FLAGGED (checked, no real departure)
- The 1M row budget and stratified sampling: house practice for `_1m` folders.
- met-real not read: a feature-choice call by measurement, no precedent pulls the other way.
- Register flags: opposite_outcomes on TP-10 (g_research and rain_in_australia kept; stock, appliances_energy_prediction,
  crms_phragmites_cover rejected) are distinguished by their measured leads; no flag on MET-4, TP-9, USE-10, EV-4, PROV-9.

</details>

<details><summary>Advocate: turkcell_radio_link_failure_prediction_1m</summary>

ADVOCATE OPENING BRIEF: turkcell_radio_link_failure_prediction_1m. Ship after changes that need no new data.

1. Validity and fit hold; no Must breaks the task (SEL-3, USE-1, SPLIT-1). Claim auditor: validity holds, forecast issue time holds on source evidence. Split auditor: "No findings at the Must level. Nothing to re-split"; 1M draw label-independent (0.000530 vs 0.000531). Domain practitioner: fit direct, keep roc_auc, keep next-day label. Precedent checker: 1M budget and sampling are house practice.

2. The label damage is repairable from the origin, the top rung of the remedy ladder (PROV-13/USE-5 Must, principles step 5). Column auditor: counters >=1000 written as thousands ('22.425'); rescale in _clean recomputes rlf (about 2,011 positives instead of 1,204), then rerun TP-10 and probes. A deterministic unit fix, also clears CLEAN-21 (Should). This strengthens the case: ~67% more positives eases the thin-window worry (TP-9).

3. The gamer's next-day lookup (LEAK-9, Should) is an evaluation-level leak, and the house remedy is a protocol line, not a data change: leak_checks.md Cases, medical_facility_operational_data (2026-11-04, "we can check if the model cheats"), sepsis_prediction, 5g_energy_consumption. Gamer: no flaw hurts an honest model; split, ids, row order and format all clean. Add the line "a model may not read other test rows (no transductive use)"; restructuring test windows to one day per block would cost rows for a cheat that the protocol already bars.

4. roc_auc over the challenge's F1 is the measured, precedented call (MET-4 Should, overruled on evidence; precedent african_credit_scoring_challenge 2026-10-26). F1 is 0.001-0.05 on 1-35 TPs for every scorer and ranks the link's own rate above LightGBM; domain practitioner and claim auditor agree resolution carries. Fix the reason text to rest on resolution only (claim auditor remedy 3). Curator confirms issue 1.

5. TP-10 leg 1 holds where it matters; leg 2 holds (MLGrads). Leads over the link rate ~+0.20/+0.20 in two windows; Jan-Apr a tie. Within-day AUC 0.77-0.82 vs forecast-only ~0.50 (split auditor) shows the task is link ranking, not just storm timing (TP-9 answered). Remedy: quote leads as ranges, report within-day AUC in README; rerun after fix 2.

6. Open feature-timing items are cheap re-runs, not blockers: forecast d vs d-1 (precedent checker option a, conditional on a regularised rerun, since the 0.655 came from the untuned LightGBM that diverges here); met-real (CLEAN-22 Must) either read day-d met-real as the winner did, or keep out with an accepted reason. Both are definition fixes (rung 2).

7. Record and notes fixes need no decision: year 2021; drop Anonymized tag (PR #17 no-marker list); licence warning accepted (EV-4, the README invites research use and citation); correct the four factual slips, CLEAN-18 cite, hop-days-counted-twice note.

Concessions: label repair, LEAK-9 protocol line, and the forecast-lag rerun must be done before shipping; the newest window is day-driven (oracle 0.975) and the README must say so.

</details>

<details><summary>Critic: turkcell_radio_link_failure_prediction_1m</summary>

CRITIC, opening brief: turkcell_radio_link_failure_prediction_1m (2026-11-09)
Position: do not ship as defined. Ship after a label repair (1) and a re-run of the scope and metric evidence on the
repaired label (3, 4); the rest are notes and small fixes. No point asks for exclusion.

1. The label is computed on damaged counters (P3/P5, USE-5 and PROV-13, Must).
   Problem: in the training release, counters of 1,000 or more were written in thousands with a decimal point
   ("22.425" for 22,425 s). Turkcell's rlf flag was computed after the damage. Our label is that flag shifted by one
   day, so it leaves out the long outages, which are the most severe failures.
   Evidence (column_auditor F1): integer unavail_second never exceeds 999; all 2,637 fractional values are <= 86.4
   and none is flagged; for ENK, avail_time + unavail = 86.4 on 95.5% of those rows. Turkcell's 2021 release uses
   true seconds, and its rlf follows the rule on 125/125 flagged rows; 38.4% of them lie in the range the damage
   hides. Rescaling gives 2,052 rule days instead of 1,219, and 2,011 next-day positives instead of 1,204 (per
   window 79->156, 143->250, 318->414). The assert in _clean passes only because flag and counters share the damage.
   Effect: about 40% of failure days count as negatives, and the windows' positive counts and storm share change.
   Remedy: repair in _clean (x1000 on the fractional values of unavail/bbe/es/ses, plus the ENK identity rows),
   recompute rlf_today and the label by Turkcell's rule, assert only on undamaged rows, document under PROV-13/14.
   Fallback for the curator: keep the source flag, set fit=approximate and say what it misses.

2. A test window contains its own labels; only a protocol line guards them (P4, LEAK-9, Must).
   Evidence (task_gamer): fails_next_day(d) == rlf_today(d+1) of the same link, exactly (1,933,132/0, 0/1,155). For
   97-99% of test rows the d+1 row is in the same window. A lookup scores 0.93-0.99 AUC and a model 0.9997-1.0,
   against 0.86-0.90 honest. Dropping rlf_today alone does not help: d+1's unavail_second carries the failure.
   The protocol line at dataset.py:204 is the remedy the LEAK-9 case names, so I do not ask for a re-split.
   Remedy: keep the line, and the README must say that per-row scoring is a condition of a valid result and that
   the daily positive count is recoverable from the window (corr 0.999). The protocol needs a check that a method
   does not read other test rows; without one, every reported score on this dataset is open to this leak.

3. The scope evidence (TP-10 leg 1) is one draw per window and ties in Jan-Apr (P2, SEL-10/SEL-11 via TP-10).
   Evidence (claim_auditor, claim 34): seed reruns show a tie with the link's failure rate in Jan-Apr; the untuned
   model is at or below the rate in 2 of 3 May-Aug draws; within a day the model leads the rate by only
   +0.03/+0.05/+0.01 (domain_practitioner). All of it is measured on the damaged label of point 1.
   Remedy: re-run TP-10 leg 1 on the repaired label with several seeds and the day-block SE, and quote those numbers
   in the notes. Leg 2 already holds (MLGrads' winning AdaBoost on point-in-time features, claim_auditor).

4. The metric overrule rests on the same single-draw, damaged-label numbers (P6, MET-4, Should).
   F1 was the source's metric. The overrule's reason (F1 on 1-35 TPs; rate beats the model on F1) must be re-measured
   on the repaired label, which has about 67% more positives. The resolution argument may weaken. Precedent:
   african_credit had source facts besides the measurement; this case has the measurement only (precedent_checker #1).
   Remedy: re-measure, then let the curator decide (issue 1 stays open). I do not oppose roc_auc as such.

5. Two inputs rest on refuted or contradicted evidence (P4/P6; LEAK-10, EV).
   a) met-real left out because it "lowered ROC AUC in 5 of 6 fits". The claim_auditor shows this is seed noise
      (+0.029 on rerun), and the 2021 winner reads day-d met-real, which is known at the end of day d.
      Remedy: re-measure; add day d's observed weather if it does not hurt, or else correct the stated reason.
   b) Forecast report dated d: the precedent_checker found d-1 drops 0.815->0.655 (May-Aug), about the no-forecast
      level. The claim_auditor now supports issue by day d from the 2021 archive. I accept that the report dated d
      is valid. Remedy: cite the archive evidence in the notes in place of the diverged-model test.

6. A pooled score mostly measures storm-day detection (P6, TP-9, Should; quality, not a reason to exclude).
   Evidence: 86% of the newest window's positives fall on 3 days. A day-rate oracle scores 0.975/0.898/0.828 (split
   auditor); within-day AUC is 0.77-0.82 and the forecast-only model scores ~0.50 within a day.
   Remedy: in the README, give the within-day AUC beside the pooled AUC and name the newest window as day-driven.

7. Small fixes (quality and writing, Should/note):
   - CLEAN-21: put the five counters in one unit (done by point 1's repair).
   - USE-5 note: a quarter of the failure hop-days count twice, once per end (238 of 927).
   - The horizon decision cites CLEAN-18; the right rule is SPLIT-12/USE-3 (precedent_checker).
   - Drop the `Anonymized` tag without a distinguishing fact (precedent PR #17).
   - Fix the factual errors in claims 11/25/26/31.
   - use_case: drop "tilt" as a next-day action.

</details>
