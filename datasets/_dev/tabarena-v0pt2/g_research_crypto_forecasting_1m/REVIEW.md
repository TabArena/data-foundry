# g_research_crypto_forecasting

**Outcome:** added as `g_research_crypto_forecasting_1m`. G-Research's Kaggle competition data, one row per coin and
minute (14 cryptocurrencies, January 2018 to September 2021): the target is the coin's return from one to 16 minutes
ahead with the part that follows the market taken out, scored by the competition's Pearson correlation with each row
weighted by its coin's `Weight`, on three 91-day test windows at the end, with a 15-minute gap and about 1M training
rows drawn as whole minutes. A focused re-review of 2026-11-06 under the new rules on exposure and weights (LEAK-41,
MET-14 to MET-16), by the claim auditor and the mediator, finds no leak and no need for a training weight, and
recommends shipping after text changes; they are applied in `dataset.py`, and the README is regenerated (not built yet).
Its one question, a confirmation, was settled on 2026-11-08: the model still clearly beats each coin's naive forecast,
though the oldest window's lead includes 0 (issue 8, A, keep).

Validity: SEL-10 and TP-10 hold, leg 1 by the reading Lennart confirmed on 2026-11-08 (issue 8). On the shipped splits a 12-seed
ensemble of early-stopped LightGBM leads the coin's mean by +0.038, +0.042 and +0.023 (newest window first); the 95%
interval excludes 0 in the two newer windows, and pooled over the three the lead is +0.034 (SE about 0.008, z about
4.3). Leg 2 is unchanged: no feature is a lag of `Target`, and the top solutions were LightGBM. SPLIT-9 and SPLIT-10
hold with the 15-minute gap: no training label reaches past the first test minute. LEAK-41 holds: `Weight` is a
scoring column, not a feature.

Value: no training weight, settled by MET-15 and not an issue. `Weight` takes exactly one value per `Asset_Name`, a
feature, and MET-15 names this dataset's asset weight as one that needs no sample weight. Measured anyway, training
with `Weight` moves the score by +0.0026 on average, within the spread across windows. MET-1, MET-2, MET-4, MET-11 and
MET-13 hold: the scorer equals the organisers' weighted correlation to within 5.6e-17 on the three folds, and each
fold (about 500,000 rows, 14 coins, 91 days) can be scored. The task probes flag no_signal, drift_baseline and
unstable; these read the R² skill of untuned models, and under the declared weighted Pearson the probe's LightGBM
scores 0.028, its linear model 0.023 and the dummy 0 (EV-3).

Quality: four statements were stale or overstated (the weight's effect "inside the noise", R² "near +0.001", the
signal "clear" in every window, the rule's case row) and are corrected; the older measurements now name the splits of
2026-10-22 they come from.

Weighed: the model leads the coin's mean in every window and by about 4.3 standard errors pooled, and its daily
correlation is positive on 75-77 of 91 days (+), against the oldest window's interval including 0 and its R² below 0
(-). Issue 8 settled on 2026-11-08: the test still holds.

**Main points:** Open: none. Settled: the model still clearly beats each coin's naive forecast, ahead in every window
and with the interval read pooled (issue 8, A, 2026-11-08). The training weight needs no decision.

**Record judgment:** valid. G-Research's own competition data and use case, a first-hand source; the record's fields
agree with the definition. The earlier review file (issues 1 to 7) was settled on 2026-10-22 and removed, before the
rule of 2026-11-02 that keeps review files; its decisions are the record's CC line of that date, and the new issue is
numbered 8 so that no old mark lands on it. The R² and weighted Pearson figures in the record's lines of 2026-10-07 to
2026-10-22 were measured on earlier splits; the Assessment line of 2026-11-06 gives the shipped-split figures.

**Issues for Lennart:**

8. **Does the model still clearly beat each coin's naive forecast, now that the oldest window's lead includes 0?**

   * **Problem:**
     - You kept this dataset on 2026-10-22 because a model clearly beat each coin's naive forecast in every test
       window, with every 95% interval of its lead above 0[^keep].
     - On the splits that now ship, the lead is +0.038 [+0.018, +0.063], +0.042 [+0.014, +0.070] and +0.023 [-0.006,
       +0.054] from the newest window to the oldest, so the oldest window's interval includes 0.
     - The rule that admits a forecasting-like panel asks the model to clearly beat the naive forecast but does not say
       whether each window must pass alone or the windows together[^tp10], so the panel asks you to confirm the
       reading.
   * **Background:** A coin's naive forecast is its mean target over the training rows, which scores a weighted
     Pearson correlation near 0. The lead is the model's score minus the naive forecast's in the same window; its 95%
     interval comes from resampling whole test days (a day-block bootstrap, 2,000 draws). The test windows are 91 days
     each: 2021-06-22 to 2021-09-20, 2021-03-23 to 2021-06-21 and 2020-12-22 to 2021-03-22. The figures your keep cited
     (the model's scores +0.040, +0.052 and +0.045, and every lead's interval above 0) came from the earlier splits,
     with rows drawn at random and a 1-day gap; the splits that ship since your calls of the same day draw whole
     minutes and keep a 15-minute gap. The rule's second condition (the top solutions are tabular models, and no
     feature is a lag of the target column) is unchanged.
   * **Effect on the task:** Under A the dataset stays, and in its oldest window the score separates a good model from
     a coin's mean less clearly than in the other two; under B it leaves the benchmark as time-series
     forecasting[^sel10], unless a stronger model's lead in the oldest window excludes 0.
   * **Experiments:** A 12-seed ensemble of early-stopped LightGBM on all features but the timestamp, on the shipped
     splits, newest window first: weighted Pearson +0.0388 [+0.0205, +0.0623], +0.0333 [+0.0103, +0.0585] and +0.0206
     [-0.0050, +0.0496]; the coins' means score +0.0004, -0.0085 and -0.0025. The ensemble's daily correlation is
     positive on 75, 75 and 77 of 91 days, the most in the oldest window. Pooled over the three windows, which share
     no test day, the lead is +0.034 with a standard error of about 0.008 (from the interval widths), about 4.3
     standard errors above 0. R² against the training mean (4 seeds): +0.0010 [-0.0002, +0.0026], +0.0009 [+0.0001,
     +0.0017] and -0.0019 [-0.0046, +0.0011].
   * **Consistency:** Reading A follows the rule's other cases, ashrae_great_energy_predictor_iii and
     rain_in_australia, both judged on whether the model was ahead in every window by its point estimate, without an
     interval per window[^cases]. Your keep of 2026-10-22 on this dataset is the only case that cited an interval per
     window, and its facts have changed, so the panel asks for a confirmation instead of overriding it.
   * **Panel:** The claim auditor finds the test still met "by any reasonable reading", and the mediator recommends A;
     this tier had no advocate or critic, and no agent argued for B.
   * **Unknown:** Whether a tuned or larger model's lead in the oldest window excludes 0; if it does, A is
     uncontested. It was not run.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The test still holds (implemented) | the dataset stays as defined; the rule's case row records the reading (ahead in every window by its point estimate, the interval read pooled) | ahead of the coin's mean in 3 of 3 windows; the pooled lead is about 4.3 standard errors above 0; the oldest window has the most positive days; follows ashrae and rain_in_australia | your keep cited every window's interval, which no longer holds; the oldest window's R² is below 0 |
     | B | Every window's interval must exclude 0 | the scope reopens: a tuned or larger model is run on the oldest window, and if its lead's interval still includes 0 the record goes to `No` with the `Time-series (Forecasting)` marker and the folder leaves the working copy | the strictest reading of "clearly"; matches the evidence your keep cited | one window outweighs a pooled lead about 4.3 standard errors above 0; the other cases never had intervals per window; costs a tuning run, or the dataset |
     | C | Write the reading into the rule | the rule says how "clearly beats" is read for every forecasting-like panel (for example A's reading), and this dataset follows it | one reading for every case; the question does not come back | a rule change where a case row recording A's reading may be enough; ashrae and rain_in_australia are re-checked against it |

   * **Recommendation:** A: the model leads the coin's mean in every window and clearly when the three are pooled,
     the rule does not say "clearly" per window, and its other cases were judged on point estimates per window.
     **Decision:** does the test still hold (A), must every window's interval exclude 0 (B), or should the rule state
     the reading (C)?

   **Notes for the AI:** On A: a CC line in the record; the main session replaces "(whether this still meets leg 1 is
   the dataset's open issue)" in the TP-10 Cases row of knowledge-curation/references/task_probes.md with the
   decision; this issue closes with a Resolved turn, and the CHANGELOG gets an entry. On B: refit a tuned LightGBM
   (or a larger ensemble) on the oldest window and bootstrap its lead over the coin's mean by test days, as measured
   on 2026-11-06; if the interval still includes 0, set the record's `suggestion` to `No` with the
   `Time-series (Forecasting)` marker (SEL-10), retire the folder from the working copy, and update the TP-10 Cases
   row and the CHANGELOG; if it excludes 0, give the run in the Scope bullet and keep. On C: the main session amends
   TP-10 leg 1 in task_probes.md with the reading chosen and re-checks the ashrae_great_energy_predictor_iii and
   rain_in_australia rows against it; the dataset then follows that reading.

   [^keep]: The record's CC line of 2026-10-22 (Lennart): "Issue 1: (a), amend TP-10 and keep the dataset." The rule's
     case row then read: "weighted Pearson per window +0.040 / +0.052 / +0.045, every 95% day-block interval above the
     coin's mean (-0.002 / +0.007 / +0.008)".
   [^tp10]: **TP-10** (Must; amended 2026-10-22, Lennart, on this dataset, and 2026-10-26 on rain_in_australia): a
     panel with one series per entity is a tabular task when both legs hold: (1) a model on the features clearly beats
     each entity's naive forecast on the shipped windows, measured by the task's declared metric (a correlation metric
     where the source scores one); (2) the source's top solutions are tabular models on point-in-time features, and
     no feature is a lag of the target column itself.
   [^sel10]: **SEL-10** (Must): time-series forecasting, future values of a series (demand, sales or a price over a
     horizon), is out; marker `Time-series (Forecasting)`.
   [^cases]: The TP-10 Cases rows: ashrae_great_energy_predictor_iii (2026-10-15), RMSE per window against the best
     naive forecast, LightGBM with 1,000 trees ahead in all three windows (1.261 / 1.176 / 1.223 against 1.393 / 1.273
     / 1.372); rain_in_australia (2026-10-26), the full model ahead of the forecasts from the location's own rain
     series in 9 of 9 windows. Neither row gives an interval per window.

   **Resolved (2026-11-08, Lennart):** A, as implemented: TP-10 leg 1 holds on the shipped splits, the model ahead of
   the coin's mean in every window by its point estimate and the interval read pooled, as for ashrae and
   rain_in_australia. The dataset stays as defined; the Scope bullet of the notes and the record's CC say so, and the
   rule's Cases row records the reading. `dataset check`: 0 errors, 0 warnings.

**Review panel:** ship after changes, text only (mediator). Tier focused, a re-review of 2026-11-06 under LEAK-41 and
MET-14 to MET-16: the claim auditor, then the mediator. Claims: 21; 15 hold (one with a wording caveat, fixed), 4
refuted, partly refuted or stale (the weight's effect "inside the noise", R² "near +0.001", the signal "clear" in
every window, the rule's case row), all corrected in the text, 2 untested (the older measurements, now labelled with
their splits; Kaggle's exact aggregation, low risk). Blind review: not run (focused tier). Agreed: no sample weight
(the rule settles it), the metric, the splits with the 15-minute gap, no leak, and the text changes. Disputed: none;
issue 8 is a confirmation, sent to you because your keep of 2026-10-22 cited intervals that no longer all exclude 0.
The mediator's issue 1 is issue 8. The reports' EV-5 and LEAK-11 read EV-8 and SPLIT-9/SPLIT-10.

<details><summary>Mediator</summary>

**Mediator: g_research_crypto_forecasting_1m (record g_research_crypto_forecasting), exposure re-review 2026-11-06,
focused tier (claim auditor only).** Inputs: the claim auditor's report, the task probes, the weight and fit-reason
measurements of 2026-11-06, the definition and the record (the folder had no REVIEW.md since 2026-10-22). No file
edited.

**1. Judgment record**

- Verdict: ship after changes. All the changes are text; nothing in the definition's code changes and no rebuild is
  needed.
- Validity: SEL-10/TP-10 holds (leg 1: the model is ahead of the coin's mean in all 3 windows, the interval excludes 0
  in 2 of 3, and the pooled lead is +0.034, z about 4.3; leg 2 is unchanged). LEAK-11 and the 15-minute gap hold (0
  train labels reach past the first test minute). LEAK-41 holds: Weight is not a feature.
- Value: MET-15 holds with no sample weight. Weight takes one value per Asset_Name (a feature), and MET-15 names this
  dataset as needing none. MET-1/2/4/11/13 hold: the source's weighted Pearson matches the tutorial's formula to
  within 5.6e-17 and can be computed on every fold. TP-10's evidence is stale and gets corrected.
- Quality: four statements are stale or overstated (EV-1, EV-5) and get corrected.
- Weighed: none.
- For the curator: issue 1, a confirmation. The 2026-10-22 decision to keep the dataset rested on "every interval
  excludes 0". On the shipped splits that holds in 2 of 3 windows. I read leg 1 as still met (default: keep).

**2. Changes to make now (no decision needed)**

- a. Correct the TP-10 Cases row: knowledge-curation/references/task_probes.md:360 (TP-10, EV-5). It still says
  "+0.040 / +0.052 / +0.045, every 95% day-block interval above the coin's mean". Replace it with the numbers on the
  shipped splits (whole-minute train sides, 15-minute gap, 2026-11-06):
  - 12-seed ensemble of early-stopped LightGBM: +0.039 / +0.033 / +0.021.
  - Lead over the coin's mean: +0.038 [+0.018, +0.063], +0.042 [+0.014, +0.070], +0.023 [-0.006, +0.054].
  - The interval excludes 0 in the two newer windows. The pooled lead is +0.034 (SE about 0.008).
  - 75 / 75 / 77 of 91 test days are positive.
  - The earlier figures came from the random-row, 1-day-gap splits.

  Keep the leg-2 text as it is.
- b. Note bullet in curation_comments (TP-10, EV-1):
  - "Under the declared weighted Pearson the same signal is clear" becomes "...is clear in the two newer windows and
    pooled over the three (Scope bullet)".
  - "no window's 95% day-block interval excludes 0" and "R^2 +0.0006, +0.0013, +0.0004" were measured on the
    superseded splits. Either label them "(random-row train sides, 1-day gap)" or replace them with the shipped-split
    R^2 from the auditor's 4-seed refit: single fits +0.0008 / +0.0008 / -0.0023; ensemble +0.0010 [-0.0002,
    +0.0026], +0.0009 [+0.0001, +0.0017], -0.0019 [-0.0046, +0.0011]. On the shipped splits window 1's interval
    excludes 0.
- c. fit_reason (EV-1):
  - "early-stopped LightGBM scores" becomes "a 12-seed ensemble of early-stopped LightGBM scores". A single model
    scores about 0.002-0.004 lower: +0.037 / +0.029 / +0.020.
  - "R² stays near +0.001" is refuted for the oldest window (-0.0023). Write "R² stays within ±0.003 of 0".
  - Optional: say that the measured model leaves out `timestamp`, which ships as a feature.

  Regenerate the README from the definition after these edits.
- d. Scope bullet: "the 12-seed average" becomes "the 12-seed ensemble (mean prediction)" (EV-1).
- e. "Training weight" note bullet and accepted_check_warnings["task_metric_weight_without_sample_weight"] (MET-15,
  EV-1). "inside the noise (of the folds)" is partly refuted: window 0's ensemble difference is +0.0050 [+0.0005,
  +0.0099], which excludes 0. Suggested wording: "within the spread across windows (mean +0.0026, SD 0.0023, t about
  1.96 on 2 df); only the newest window's interval excludes 0 (+0.0050 [+0.0005, +0.0099]); MET-15 needs no sample
  weight because Weight is a function of Asset_Name."
- f. Label the older measurements (EV-5). The History bullet (1M-budget scores .041/.046/.045 ...) and the CLEAN-19
  feature comparison were measured on the earlier splits. Add "(random-row train sides, 1-day gap, 2026-10-22)" to
  each, as splits_comment already does.
- g. Record line (records.md). Add an "**Assessment (AI, 2026-11-06):**" line covering:
  - the exposure re-review (focused tier, claim auditor);
  - no sample weight under MET-15 (Weight is a function of Asset_Name; training with it: +0.0026 mean, SD 0.0023,
    window 0's interval excludes 0);
  - TP-10 leg 1 re-measured on the shipped splits (2 of 3 intervals exclude 0, pooled lead +0.034), Cases row
    updated;
  - text corrections a-f;
  - the confirmation open for the curator (issue 1).
- h. CHANGELOG.md entry for the working copy: a dated line for the edited definition text and the Cases row (house
  rule).

**3. Issues for the curator (ranked)**

Issue 1 (validity, P2 via TP-10, Must; a confirmation, default keep). Is leg 1 of TP-10 still met now that the oldest
window's lead includes 0?

- Problem: your keep decision of 2026-10-22 cited "every 95% day-block interval above the coin's mean". On the splits
  that now ship (whole minutes, 15-minute gap) the lead is +0.0384 [+0.0182, +0.0631], +0.0418 [+0.0138, +0.0699] and
  +0.0231 [-0.0060, +0.0537].
- Effect: if leg 1 failed, the dataset would be out of scope as forecasting (SEL-10).
- For keeping:
  - the point estimate is ahead in 3 of 3 windows;
  - the interval excludes 0 in 2 of 3;
  - pooled over the three disjoint windows the lead is +0.034, SE about 0.008, z about 4.3 (I checked the arithmetic
    from the interval widths);
  - the ensemble is positive on 75-77 of 91 days in every window, and the oldest window has the most positive days
    (77);
  - precedent: ashrae and rain_in_australia were judged on being ahead in every window by point estimate, with no
    per-window intervals.
- Against: "clearly beats" was read as every interval excluding 0 when the rule was amended for this very case. The
  R^2 in the oldest window is negative (-0.0019 ensemble).
- Rule: TP-10 leg 1 does not say whether "clearly" means each window or pooled. That is why this goes to you rather
  than being settled by rule.
- Decision needed: (a) leg 1 holds: per-window point estimates plus the pooled interval are enough (the Cases row
  says so; recommended); (b) require every window's interval to exclude 0: reopen the scope (retire as Time-series
  (Forecasting), or look for a stronger model); (c) amend TP-10 to fix the reading for every panel case.
- What would settle it further: a tuned or larger model on window 2 (a lead whose interval excludes 0 there makes (a)
  uncontested).

Not an issue: the training weight. MET-15 is a Must, and it names this dataset's asset Weight as a weight that is a
function of the features and "needs no sample weight". The measured gain does not reopen it:

- the rule's reason is about the target, not the fitting: a weight that is a function of x leaves the L2-optimal
  E[y|x] unchanged;
- the gain is not robust: mean +0.0026, t about 1.96 on 2 df; 1 of 3 windows' intervals excludes 0; the fixed-50-round
  arm gives +0.0010 with all intervals including 0;
- the liberty_mutual_fire_peril_loss_cost precedent is the same and was decided the same way.

Declaring sample_weight="Weight" would be allowed (it is the metric's row weight), but the rule does not ask for it.
So the point stays settled by the rule. Only the note's "inside the noise" wording is wrong (change e). If you want
participants steered to weight their training, that would be a deliberate departure: say so, and it becomes a
one-line definition change, applied the same way to liberty_mutual.

Residual, untested, low risk (no decision): Kaggle's exact aggregation. The page is JS-only; the tutorial gives
weights by asset and drops null targets; the community implementations are pooled, as declared (MET-1).

**4. Agreed facts** (from the auditor's measurements; no one disputes them, so no experiment was re-run; I re-checked
the derived arithmetic)

- Weight: exactly 1 value per Asset_Name for all 14 assets, equal to asset_details.csv. No sample_weight is declared;
  Weight is a scoring column and not a feature; Asset_Name is a categorical feature.
- Training with Weight (12 seeds, early stopped): +0.0045 / +0.0034 / +0.0001; mean +0.0026, SD 0.0023 across
  windows; 25 of 36 pairs favour the weight.
  - Ensemble differences: +0.0050 [+0.0005, +0.0099], +0.0029 [-0.0008, +0.0063], +0.0002 [-0.0035, +0.0030].
  - Fixed 50 rounds: mean +0.0010, every interval includes 0.
- fit_reason figures: +0.0388 / +0.0333 / +0.0206 are the 12-seed ensemble. A single model scores +0.0368 / +0.0294 /
  +0.0199. Days positive: 75 / 75 / 77 of 91.
- Lead over the coin's mean: as in issue 1. Pooled: +0.034, SE about 0.008.
- R^2 on the shipped splits (4-seed refit): single fits +0.00082 / +0.00077 / -0.00232; the notes' +0.0006 / +0.0013
  / +0.0004 come from the superseded splits.
- Metric: the scorer equals the tutorial's weighted correlation to within 5.6e-17 on 3 folds. A constant scores 0.0
  and random predictions about -0.001. 499,994 / 500,000 / 499,992 test rows, 14 assets and 91 days per fold.
- Splits: train-to-test gaps of 28 / 29 / 28 minutes in the sample; 0 train labels reach past the first test minute;
  100% whole minutes; 0 index overlap; 0 duplicate (timestamp, asset) pairs; 0.0% exact feature copies.
- Untuned probes flag no_signal, drift_baseline and unstable by R^2. Under the declared metric LightGBM scores 0.028,
  linear 0.023, dummy 0. The measurements leave out `timestamp`, which ships as a feature; the probe's single-feature
  pick chose it once.

**5. Consistency with precedent**

- MET-15, no sample weight: the same as liberty_mutual_fire_peril_loss_cost (var11_weight, accepted 2026-11-06 with
  the same reason). Consistent. That precedent has no gain measurement, so g_research does not depart from it.
- TP-10: ashrae (point estimates ahead in all windows) and rain_in_australia (ahead in 9 of 9) support reading (a) in
  issue 1. The 2026-10-22 decision on this dataset is the only TP-10 case that cited per-window intervals. That
  decision's facts have changed, which is why issue 1 asks for a confirmation and does not override it.
- MET-4/MET-12 (metrics.md:285, the source's weighted_pearsonr): unchanged and consistent.
- No precedent-checker report was produced for this focused tier. The check above was done by reading metrics.md,
  task_probes.md and liberty_mutual's dataset.py.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: g_research_crypto_forecasting_1m (record g_research_crypto_forecasting), exposure re-review
2026-11-06.** The definition's README is in sync with it. Scripts: the weight, gap, metric and dummy checks; R² on the
shipped splits; the organisers' Kaggle tutorial notebook, pulled with the kaggle CLI.

**Verdict:** today's change holds. No training weight is correct under MET-15: Weight is exactly a function of
Asset_Name, and Asset_Name is a feature. The metric holds as `source` (MET-1, MET-2, MET-11). Four statements in the
text are stale or overstated. None changes the ship decision. The largest is TP-10: the case row and one note bullet
still say the lead is clear in every window, but on the shipped splits the oldest window's interval includes 0.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | No sample weight; Weight is a function of Asset_Name | notes "Training weight", accepted_check_warnings, CHANGES.md | Count distinct Weight values per Asset_Name on the shipped 2,499,998-row frame; compare them with asset_details.csv | HOLDS | 1 value per asset for all 14 assets, equal to asset_details.csv (Bitcoin 6.779922 ... IOTA and Maker 1.098612); task_metadata has no sample_weight; Weight is not in feature_cols; Asset_Name is | MET-15, MET-2 |
| 2 | Training with Weight moved the score by +0.0045/+0.0034/+0.0001, mean +0.0026, SD 0.0023, 25 of 36, +0.0010 without early stopping | notes, accepted warning | Compare with the weight measurement of 2026-11-06 | HOLDS (the numbers match exactly) | | |
| 3 | ...and that is "inside the noise of the folds" / "inside the noise" | notes, accepted warning | Read the seed-ensemble day-block bootstrap of the difference in the same summary | PARTLY REFUTED | window 0's difference is +0.0050 [+0.0005, +0.0099], which excludes 0 (the fixed-50 arm gives +0.0040 [-0.0006, +0.0094]); 25 of 36 pairs favour the weight. The claim holds only across windows: mean +0.0026, SE 0.0013, t = 1.96 on 2 df. The decision is unaffected, because MET-15 settles it by rule: a weight that is a function of x leaves the L2-optimal E[y\|x] unchanged | MET-15, EV-1 |
| 4 | fit_reason: "early-stopped LightGBM scores +0.039, +0.033 and +0.021" | task_summary.fit_reason, README | Compare with the fit-reason check of 2026-11-06; my own refit (4 seeds per window) | HOLDS, with a wording caveat | the figures are the 12-seed ENSEMBLE (+0.0388/+0.0333/+0.0206). One early-stopped model averages +0.0368/+0.0294/+0.0199 (weight summary), and +0.0362/+0.0285/+0.0222 in my 4-seed refit. The notes call it "the 12-seed average", but it is the mean prediction. Every measurement drops `timestamp`, which ships as a feature | EV-1 |
| 5 | "beats the coin's mean in the two newer ones" | fit_reason | the fit-reason check | HOLDS | lead +0.0384 [+0.0182, +0.0631], +0.0418 [+0.0138, +0.0699], +0.0231 [-0.0060, +0.0537] (windows 0, 1, 2; window 2 is the oldest) | TP-10 |
| 6 | "positive on 75-77 of 91 test days" | fit_reason | the fit-reason check (daily weighted Pearson of the ensemble > 0) | HOLDS | 75, 75, 77 of 91 days | |
| 7 | "R² stays near +0.001" | fit_reason | Refit the notes' LightGBM on the shipped splits (4 seeds, early stopping on the newest 10%); compute R² against the train mean | REFUTED for the oldest window | single fits +0.00082 / +0.00077 / -0.00232; the 4-seed ensemble +0.00098 [-0.00024, +0.00255], +0.00086 [+0.00013, +0.00171], -0.00192 [-0.00458, +0.00106]. The notes' "+0.0006, +0.0013, +0.0004" come from the superseded random-row, 1-day-gap splits (the splits_comment says so; the Note bullet does not) | EV-1, EV-5 |
| 8 | Leg-1 numbers "superseded 2026-11-06 ... the oldest window's lead no longer excludes 0" | notes, Scope bullet | Compare with the fit-reason check | HOLDS | all 9 numbers and the day counts match | |
| 9 | "Under the declared weighted Pearson the same signal is clear (Scope bullet)" | notes, Note bullet | Compare with claim 5 | OVERSTATED for window 2 | the lead's interval includes 0 in the oldest window. Pooled over the three disjoint test windows (SE taken from the interval width) the mean lead is +0.034, SE ~0.008, z ~4.3; window 2 also has the most positive days (77 of 91) | TP-10 (Must), EV-1 |
| 10 | TP-10 case row: "every 95% day-block interval above the coin's mean (-0.002 / +0.007 / +0.008)", "+0.040 / +0.052 / +0.045" | knowledge-curation/references/task_probes.md:360 (cited as the decisive evidence for keeping the dataset) | Compare with the shipped-split numbers | STALE (REFUTED on the shipped splits) | 2 of 3 intervals exclude 0 now; the scores are +0.039/+0.033/+0.021 | TP-10 (Must) |
| 11 | Metric source: Kaggle's "weighted version of the Pearson correlation coefficient", weighted by the asset's Weight | metric = Metric.source(...), README Metric block | The Kaggle evaluation page is JS-only (WebFetch empty). The organisers' tutorial (cstein06, pulled) says: "your predictions will be evaluated on a weighted version of the Pearson correlation coefficient, with weights given by the `Weight` column in the Asset Details file"; null targets "are ignored for scoring purposes" | HOLDS (original, weights, target scale; dropping the null-target rows mirrors the scoring) | | MET-1, MET-3, MET-4, MET-11 |
| 12 | Scorer equals the weighted Pearson | weighted_pearsonr | On each test fold, compare scorer(c) with the tutorial-style weighted_correlation (pooled weighted means, variances and covariance) on a noisy prediction | HOLDS | \|diff\| <= 5.6e-17 on all 3 folds | MET-13 |
| 13 | Computable on every test fold | MET-2 | Count the units per fold; score dummy predictions | HOLDS | 499,994 / 500,000 / 499,992 rows, 14 assets, 91 days per fold; a constant scores 0.0 (no NaN), a random prediction scores -0.0011/-0.0003/-0.0008 | MET-2, P6 |
| 14 | Same meaning as in the source: the same Target, rows without a target dropped, weights from asset_details | notes | Above, plus the tutorial's definition of the target (R = log(P(t+16)/P(t+1)) minus beta*M, M weighted by the same w) | HOLDS | | MET-2 |
| 15 | A 15-minute gap is the minimum, and "the newest training label is known at the close of the window's first minute" | splits_comment | Read splits.py (train_mask = axis < start - 15 min, so the newest train row is at most start - 16 min and its label reads Close(start)); measure on the shipped splits | HOLDS | train-to-test gaps of 28, 29 and 28 minutes in the shipped sample; 0 train rows whose label reaches past the first test minute | LEAK-11, SPLIT |
| 16 | Whole minutes on both sides; 1M train, 500k test | version_comment, splits_comment | the weight script's log; the first audit script | HOLDS | 84-87k train minutes at 11.5-11.9 rows per minute, 100% whole; test 14.0 rows per minute | |
| 17 | No row is a copy across the split | implied | Row-index overlap, duplicate (timestamp, asset), leak probe exact copies | HOLDS | 0 overlap, 0 duplicates, 0.0% exact feature copies (the leak probe) | LEAK |
| 18 | Every feature is known at the prediction point | implied, history_features docstring | Read the code: rolling windows and shifts end at the row's own minute; market means use minute t only | HOLDS (by reading) | | LEAK-1 |
| 19 | Frame size 23,486,468 = 24,236,806 - 750,338 | version_comment, notes | arithmetic | HOLDS | | |
| 20 | Older claims: the CLEAN-19 feature comparison, the History bullet's 1M-budget scores, splits_comment's R² under random-row validation, the target autocorrelation at 5 minutes | notes, splits_comment | not re-run | UNTESTED (settled 2026-10-22; measured on the earlier splits; splits_comment says so, the History and feature bullets do not) | | EV-5 |
| 21 | Kaggle's exact aggregation (one pooled correlation over the live period, as the community implementations compute) | Metric | The official page cannot be fetched and the tutorial gives no formula | UNTESTED (residual; the community's weighted_correlation is pooled, and the declared metric matches it) | | MET-1 |

**Refuted / untested, ranked** (principles: validity first, Must first)

1. TP-10 evidence is stale (claims 9, 10; Must rule, decides scope). The case row in task_probes.md:360 and the Note
   bullet ("the same signal is clear") still read "every interval above the coin's mean". On the shipped splits the
   oldest window's lead is +0.0231 [-0.0060, +0.0537]. Leg 1 still holds by any reasonable reading: 2 of 3 windows
   exclude 0, the pooled lead is +0.034 (z ~4.3), and 75-77 of 91 days are positive in every window. So the scope
   decision stands, but its recorded evidence is wrong. Mildest remedy: update the case row to the shipped-split
   numbers (+0.039/+0.033/+0.021, leads +0.038/+0.042/+0.023, two of three intervals above 0, the pooled lead). Reword
   the Note bullet to "clear in the two newer windows and pooled".
2. "R² stays near +0.001" (claim 7). On the shipped splits the oldest window gives R² -0.0023 (single fit) and -0.0019
   (ensemble). The Note bullet's R² figures come from the superseded splits without saying so. Mildest remedy: in
   fit_reason, "R² stays within ±0.003 of 0"; in the Note bullet, give the shipped-split R² (+0.0008/+0.0008/-0.0023)
   or mark the old figures "random-row train sides, 1-day gap".
3. "inside the noise of the folds" (claim 3). Window 0's seed-ensemble difference excludes 0 (+0.0050 [+0.0005,
   +0.0099]), and 25 of 36 pairs favour the weight. The decision does not change, because MET-15 settles a weight that
   is a function of a feature by rule. Mildest remedy: "within the spread across windows (mean +0.0026, SD 0.0023);
   only window 0's interval excludes 0", in the notes and the accepted warning.
4. Ensemble versus single model (claim 4). The fit_reason figures are a 12-seed ensemble. One model scores about
   0.002-0.004 lower. Mildest remedy: "a 12-seed ensemble of early-stopped LightGBM scores ...", and "12-seed
   ensemble" instead of "12-seed average" in the Scope bullet.
5. Untested, low risk: Kaggle's exact aggregation (claim 21); the settled older measurements (claim 20).

</details>
