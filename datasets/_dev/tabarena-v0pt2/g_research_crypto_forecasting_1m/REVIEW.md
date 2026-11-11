# g_research_crypto_forecasting

**Outcome:** added as `g_research_crypto_forecasting_1m`. G-Research's Kaggle competition data, one row per coin and
minute (14 cryptocurrencies, January 2018 to January 2022): the target is the coin's return from one to 16 minutes
ahead with the part that follows the market taken out, scored by the competition's Pearson correlation with each row
weighted by its coin's `Weight`, on three 91-day test windows, with a 15-minute gap and about 1M training rows drawn
as whole minutes. A focused re-review of 2026-11-06 under the new rules on exposure and weights (LEAK-41,
MET-14 to MET-16), by the claim auditor and the mediator, finds no leak and no need for a training weight, and
recommends shipping after text changes; they are applied in `dataset.py`, and the README is regenerated (not built yet).
Its one question, a confirmation, was settled on 2026-11-08: the model still clearly beats each coin's naive forecast,
though the oldest window's lead includes 0 (issue 8, A, keep). On 2026-11-11 you added the release's supplemental file,
21 September 2021 to 24 January 2022 (issue 10, B, applied: 26,001,823 rows), and confirmed the 91 days and the
15-minute gap (H, A); you then chose the test windows on the longer history: the newest from 25 October 2021, the 2021
bull run from 22 December 2020 and the 2020 crash from 28 February 2020, the last training on 48.25% of the rows
(issue 9, reply a, applied).

Validity: SEL-10 and TP-10 hold, leg 1 by the reading Lennart confirmed on 2026-11-08 (issue 8), measured on the
windows that ended on 20 September 2021 and to be measured again on the windows chosen on 2026-11-11 (issue 9). On the
splits shipped before the newer months were added (windows to 20 September 2021) a 12-seed
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

**Main points:** Settled on 2026-11-11: the test windows on the longer history are the newest from 25 October 2021,
the 2021 bull run from 22 December 2020 and the 2020 crash from 28 February 2020, the last on 48.25% of the rows
(issue 9, a); the supplemental file is added (issue 10, B) and the 91 days with a 15-minute gap hold (H, A). Settled
earlier: the model still clearly beats each coin's naive forecast, ahead in every window and with the interval read
pooled (issue 8, A, 2026-11-08), measured on the earlier windows and to be measured again on these. The training
weight needs no decision.

**Record judgment:** valid. G-Research's own competition data and use case, a first-hand source; the record's fields
agree with the definition. The earlier review file (issues 1 to 7) was settled on 2026-10-22 and removed, before the
rule of 2026-11-02 that keeps review files; its decisions are the record's CC line of that date, and the new issue is
numbered 8 so that no old mark lands on it. The R² and weighted Pearson figures in the record's lines of 2026-10-07 to
2026-10-22 were measured on earlier splits; the Assessment line of 2026-11-06 gives the shipped-split figures.

**Horizon:**

* **Verdict:** keep the 91-day windows (high confidence for the 15-minute target, medium-high for 91 days): each
  window is the 91 days on which the competition scored every frozen model (2 February to 3 May 2022); the 15-minute
  horizon is the target's own.
* **Length:** two horizons: the target's (the return from one to 16 minutes ahead, fixed by the host) and the
  window's (how long a fitted model trades before its refit). G-Research ran each team's models "for three months
  against real live market data"
  (https://www.gresearch.com/news/wrapping-up-the-g-research-crypto-forecasting-competition/), and "the model is fixed
  after the training phase" (a participant's slides). No source gives a production refit cadence; a firm that refits
  more often faces an easier task than the frozen 91 days.
* **Gap:** 15 minutes: a row's target is known 16 minutes after it.
* **Time frame:** 1 January 2018 to 23 January 2022: train.csv (to 20 September 2021) and, since 2026-11-11, the
  release's `supplemental_train.csv`, 2,518,278 rows from 21 September 2021 to 24 January 2022 that continue it
  (issue 10, B); the last minute with a target is 23:44 on 23 January 2022.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | 91 days, 15-minute gap (implemented) | the competition's three months of live scoring per window; six candidates above the floor on today's grid, back to 24 March 2020 | 3 windows (issue 9's B) of 1.54M to 1.83M rows (500,000 rows tested, by whole minutes) | the period on which the competition scored every frozen model | no source gives a production refit cadence |
  | B | 30 days | 20 candidates | 20 candidates of 495,144 to 604,766 rows (up to 500,000 rows tested, by whole minutes) | more windows to choose from | no source; scores a model refit more often, an easier task than the frozen 91 days |
  | C | 182 days | exactly three windows, 24 March 2020 to 20 September 2021 | 3 windows of 3.22M to 3.67M rows (500,000 rows tested, by whole minutes) | the three windows cover every eligible day | no choice of windows; twice the competition's period |

* **Recommendation:** A: the length on which the competition scored every frozen model, and no source gives another.
  **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, as implemented: windows of 91 days, the period on which the competition scored
every frozen model, and a 15-minute gap, the target's own horizon. `splits_comment` gives this reason and the record's
CC line says the horizon is checked. With the supplemental file (issue 10) the newest window runs from 25 October 2021
to 23 January 2022; which other windows to test is issue 9. `dataset check`: 0 errors, 0 warnings.

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

9. **Which 91-day windows: the three newest, or the newest, the 2021 bull run and the crash of March 2020?**

   * **Problem:**
     - The newest window (22 June to 20 September 2021) always stays, and since 2026-11-10 the other two are chosen
       from the use case and statistics of the data, preferring other years over the windows just before the
       newest[^gr-split15].
     - Today's two older windows (22 December 2020 to 21 June 2021) both fall in the busy market of 2021 and look
       alike in the target's spread, the trading activity and the drift of the features, and no window tests 2020,
       when trading was four to eight times quieter.
     - A trading firm's model runs through quiet and busy markets and through crashes, and windows from 15 January
       2020 on keep at least half the rows for training, so one window can test 2020 with its crash of 12 March.
   * **Background:**
     - The target is the coin's return relative to the market, so the market's direction drops out of it; what sets
       the windows apart is the target's spread, the trading activity (`Count`, the trades of a coin in a minute: 69
       at the median over all rows) and the price levels, which drift whenever prices leave their earlier range.
     - The length of 91 days (the competition's three months of live scoring) and the 15-minute gap stay as they
       are[^gr-split12]. On the 91-day grid of today's windows, six windows keep half the rows for training, back to
       24 March 2020; with a step of 30 days the candidates reach back to 29 January 2020.
     - The other 2020 candidates are quieter still and hold no crash: 24 March-22 June 2020 (target from -0.0027 to
       0.0028, 49 trades a minute) and 23 June-21 September 2020 (66 trades, Bitcoin +7%). B takes the window with
       the crash, Bitcoin's largest fall in one day in the data: -39% on 12 March 2020, against -17% (16 January
       2018) and -14% (19 May 2021) for the next largest.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. The target's spread is the 10th to 90th percentile; on the train
       sides it is about -0.0042 to 0.0042.
   * **Statistics:** Bitcoin's daily closes, the trades and the train shares from all rows; the target and the drift
     from the candidate tables (100,000-row samples of each side).

     | Window | In | Bitcoin over the window | Worst day | Trades a minute (median) | Target, p10 to p90 | Median PSI (largest) | Train share |
     |---|---|---|---|---|---|---|---|
     | 22 Jun-20 Sep 2021 | A, B | +35% | -11% (7 Sep) | 201 | -0.0031 to 0.0031 | 0.035 (1.14, prices) | 92.2% |
     | 23 Mar-21 Jun 2021 | A | -42% | -14% (19 May) | 483 | -0.0051 to 0.0051 | 0.219 (1.60, `Count`) | 84.4% |
     | 22 Dec 2020-22 Mar 2021 | A, B | +138% | -13% (21 Jan) | 243 | -0.0055 to 0.0054 | 0.232 (1.01, `Count`) | 76.6% |
     | 28 Feb-28 May 2020 | B | +9% | -39% (12 Mar) | 59 | -0.0032 to 0.0034 | 0.047 (0.20, prices) | 53.4% |

   * **Effect on the task:** Under A, two of the three scores come from the busiest six months of the data (243 and
     483 trades a minute at the median) and none from a quiet market. B keeps the newest window and the 2021 bull
     run and adds the quiet market of 2020 with its crash, so the score covers both kinds of market.
   * **Consistency:**
     - Today's windows are the default, the last three windows of 91 days; the History bullet already notes that the
       windows from 22 December 2020 to 21 June 2021 fall in the high-volatility market of 2021.
     - Issue 8 read the model's lead over each coin's mean on today's windows; under B those figures are measured
       again on the new windows before the change ships, as a check of the task, not as a reason for the windows.
     - aeolus_rebuilt_1m has the same question open under the rewritten rule; no dataset has decided under it yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m/dataset.py`
     (`temporal`, `splits_comment`, the Scope and History bullets of `curation_comments`); the record
     `curation/records/g_research_crypto_forecasting.md`; the candidate table `.venv/bin/python -m
     data_foundry.curation.cli dataset windows g_research_crypto_forecasting_1m --root datasets/_dev/tabarena-v0pt2`,
     and with `--step 30`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three newest windows (implemented) | tests 22 Jun-20 Sep 2021, 23 Mar-21 Jun 2021 and 22 Dec 2020-22 Mar 2021 | the months closest to deployment; holds the crash of 19 May 2021; issue 8's figures stand | two windows from the same busy market, alike in spread, activity and drift; no window in 2020 |
     | B | Newest, the 2021 bull run, the 2020 crash | tests 22 Jun-20 Sep 2021, 22 Dec 2020-22 Mar 2021 and 28 Feb-28 May 2020 | another year; a quiet market and the largest crash in the data; windows spread over the eligible history | the oldest trains on 53.4% of the rows; the crash of May 2021 leaves the test; issue 8's figures are measured again |

   * **Recommendation:** B: a model that trades every minute has to hold in quiet and in busy markets, and A tests
     the busy market of 2021 twice and the quiet one never; B swaps the near copy for the quiet market of 2020 with
     the largest crash in the data. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=91, unit="days",
   gap=15, gap_unit="minutes", sample_by="time", cutoffs=("2021-06-22", "2020-12-22", "2020-02-28")))`. Built with
   `TemporalSplits.splits` on the definition's frame: test 1,832,105, 1,834,016 and 1,544,359 rows before the 500k
   sampling by whole minutes, train 21,654,153, 17,985,995 and 12,545,715 (92.2%, 76.6%, 53.4%), each train side
   ending at 23:44 the day before its window. Then rewrite `task_summary.split` ("Each test window is 91 days at the
   end of the period"), `splits_comment` ("each of the last 3 windows of 91 days"), the History bullet (the sentence
   on the 2021 regime) and the per-window figures of `fit_reason`, the Scope bullet and the probe note, which were
   measured on today's windows; re-measure TP-10 leg 1 on the new windows (the 12-seed ensemble against the coin's
   mean, day-block intervals) and add a turn to issue 8 if its reading changes; then a CC line, a dated CHANGELOG
   entry and `dataset check` (SPLIT-15). On A, write the reason into `splits_comment`.

   [^gr-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^gr-split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source: how far ahead the actor
     predicts, the competition's own test window, the refit cadence.

   **Lennart (2026-11-10, discuss):** are we sure the forecast horizion here makes sense as well?

   **Answer (AI, 2026-11-10):**
   - The 91 days hold: they are the period on which the competition scored every frozen model (2 February to 3 May
     2022), and the 15-minute horizon is the target's own; the Horizon block above gives the sources.
   - The audit found a gap in the period instead: the release's supplemental file (21 September 2021 to 24 January
     2022) is left out without a reason, and adding it moves the newest window and the floor. Issue 10 asks about it
     first; this issue waits on it and is proposed again if you add the file.

   **Lennart (2026-11-11, change):** Agree.
   Option B: Newest, the 2021 bull run, the 2020 crash.

   **Answer (AI, 2026-11-11):** With the newer months in, test your B (the newest window, the 2021 bull run and the
   crash of March 2020), or add a window in 2019, or keep every train side above half?

   * **Problem:**
     - With the supplemental file the newest window is 25 October 2021 to 23 January 2022, the falling market after
       Bitcoin's peak of 10 November 2021, and your B adds the 2021 bull run (22 December 2020 to 22 March 2021) and
       the quiet market of 2020 with its crash (28 February to 28 May 2020).
     - The crash window now trains on 48.2% of the rows, which the floor amended today admits as the one window under
       half next to two above it[^g9-split14].
     - The candidates now reach back to June 2019 (31.0%), so a window in another year is possible, and a quiet 2020
       window from 27 April 2020 instead of the crash would keep every train side above half.
   * **Background:**
     - The target is the coin's return relative to the market, so the market's direction drops out of it; the windows
       differ in the target's spread, the trading activity (`Count`, the trades of a coin in a minute) and how far the
       features drift from the train side (PSI, the population stability index; above 0.25 is usually read as a
       large shift).
     - Until you decide, the definition tests the three newest windows (25 October, 26 July and 26 April 2021, on
       93.0%, 85.9% and 78.9% of the rows); the windows starting from June 2021 on look like the newest (target p10 to
       p90 about -0.0030 to 0.0030, median PSI 0.02 to 0.07), so this walk back tests a near copy of it (26 July)
       and the busy market with the crash of 19 May 2021 (26 April: target -0.0043 to 0.0043, median PSI
       0.161)[^g9-split15].
     - The length (91 days) and the gap (15 minutes) are settled (H); each window keeps at most 500,000 test rows,
       drawn as whole minutes. Issue 8's figures come from the windows that ended on 20 September 2021 and are
       measured again on the windows you choose, as a check of the task, not as a reason for the windows.
   * **Statistics:** Bitcoin's daily closes, the trades and the train shares from all 26,001,823 rows; the target and
     the drift from 100,000-row samples of each side (`dataset windows`).

     | Window | In | Bitcoin over the window | Worst day | Trades a minute (median) | Target, p10 to p90 | Median PSI (largest) | Train share |
     |---|---|---|---|---|---|---|---|
     | 25 Oct 2021-23 Jan 2022 | a, b, c | -40% | -10% (21 Jan 2022) | 180 | -0.0030 to 0.0029 | 0.035 (1.40, prices) | 93.0% |
     | 22 Dec 2020-22 Mar 2021 | a, b, c | +138% | -13% (21 Jan 2021) | 243 | -0.0054 to 0.0054 | 0.235 (0.98, `Count`) | 69.2% |
     | 27 Apr-26 Jul 2020 | c | +29% | -8% (10 May 2020) | 50 | -0.0026 to 0.0028 | 0.122 (0.17, price trends) | 52.1% |
     | 28 Feb-28 May 2020 | a, b | +9% | -39% (12 Mar 2020) | 59 | -0.0032 to 0.0034 | 0.045 (0.17, prices) | 48.2% |
     | 8 Jun-6 Sep 2019 | b | +29% | -13% (27 Jun 2019) | 59 | -0.0036 to 0.0036 | 0.055 (0.16, prices) | 31.0% |

   * **Consistency:** windows spread over seasons or years instead of the newest ones follow the rule as rewritten on
     2026-11-10 (aeolus_rebuilt_1m, nyc_taxi_trip_duration_1m, consumer_complaints_1m); one window under half next to
     two above it is what wisconsin_local_government_property_insurance_fund (40.6%) and
     ashrae_great_energy_predictor_iii_1m (49.47%) ship.
   * **Options:**

     | | Option | What it does | Test windows | Pro | Con |
     |---|---|---|---|---|---|
     | a | Your B: newest, the 2021 bull run, the 2020 crash | tests 25 Oct 2021-23 Jan 2022, 22 Dec 2020-22 Mar 2021 and 28 Feb-28 May 2020 | 3 windows of 1.54M to 1.83M rows (500,000 rows tested each, by whole minutes) | three markets: falling, booming, and quiet with the largest crash in the data; as many windows as a random split of this size gets folds | the crash window trains on 48.2% |
     | b | B and 2019 | a's three windows and 8 Jun-6 Sep 2019 (the peak of June 2019 and its fall) | 4 windows of 1.54M to 1.83M rows (500,000 rows tested each, by whole minutes) | another year; the oldest market the floor admits | a fourth fit; two train sides under half (48.2%, 31.0%); 2019 looks like 2020 in trades and target spread |
     | c | Every train side above half | tests the newest, the 2021 bull run and 27 Apr-26 Jul 2020 | 3 windows of 1.56M to 1.83M rows (500,000 rows tested each, by whole minutes) | every window trains on half the rows or more | the crash of March 2020 is only trained on; the quietest window, with the narrowest target |

   * **Recommendation:** a: it tests three different markets, the falling one of the newest window, the 2021 bull run
     with the widest target spread of the table and the quiet market of 2020 with the largest crash in the data, and
     the amended floor admits its one window under half; b's 2019 window costs a fourth fit and a train side of 31%
     for a market much like that of 2020. **Decision:** a, b or c?

   **Notes for the AI:** on a, `temporal = Temporal(on="timestamp", splits=TemporalSplits(window=91, unit="days",
   gap=15, gap_unit="minutes", sample_by="time", cutoffs=("2021-10-25", "2020-12-22", "2020-02-28")))`: test 1,830,834,
   1,834,016 and 1,544,359 rows before the 500k sampling by whole minutes, train 24,170,779, 17,985,995 and 12,545,715
   (93.0%, 69.2%, 48.2% of 26,001,823). On b, `cutoffs=("2021-10-25", "2020-12-22", "2020-02-28", "2019-06-08")`:
   a's windows and test 1,567,015, train 8,055,354 (31.0%). On c, `cutoffs=("2021-10-25", "2020-12-22",
   "2020-04-27")`: the third window tests 1,556,820 and trains on 13,547,573 (52.1%). Each train side ends at 23:44 the
   day before its window (`window_bounds` on the definition's frame, 2026-11-11). Then rewrite `task_summary.split`
   ("Each test window is 91 days at the end of the period"), `splits_comment` (the windows, why each, every window
   under 50% with its share, and the sentence on the three newest), the History bullet's sentence on the windows and
   the Scope bullet's "measured again" sentence; re-measure TP-10 leg 1 on the new windows (the 12-seed ensemble
   against the coin's mean, day-block intervals) and add a turn to issue 8 if its reading changes; then a CC line, a
   dated CHANGELOG entry and `dataset check`.

   [^g9-split14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): "The newest window and at least one other train on
     at least 50% of the data; further windows may train on less, down to 30% of the data, and at most as many
     windows train on less than 50% as on 50% or more. ... The splits comment names every window under 50% and its
     train share; no model score is required for it."
   [^g9-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "Prefer windows in other years, then other seasons, then other months, weeks or days, over the windows
     just before the newest."

   **Lennart (2026-11-11, change):** Reply (a): Your B: newest, the 2021 bull run, the 2020 crash

   **Resolved (2026-11-11, Lennart):** a: `temporal` declares `cutoffs=("2021-10-25", "2020-12-22", "2020-02-28")`
   with the rest unchanged (91 days, a 15-minute gap, `sample_by="time"`). On the definition's frame of 26,001,823
   rows the windows test 1,830,834, 1,834,016 and 1,544,359 rows before the 500,000-row sampling by whole minutes and
   train on 24,170,779, 17,985,995 and 12,545,715 (93.0%, 69.2% and 48.25%), each train side ending at 23:44 the day
   before its window, as the answer gave. The crash window's 48.25% is signed off with this mark: the record's CC line
   names it and the definition accepts `splits_train_under_half` with it. `task_summary.split`, `splits_comment` (the
   three markets and why each, the counts, the window under half) and the History bullet name the windows; the newest
   window holds the 99 EOS.IO bars of 26-27 October 2021 that the Anomaly bullet notes, kept. Issue 8's reading (the
   12-seed ensemble ahead of each coin's mean, TP-10 leg 1) was measured on the windows that ended on 20 September 2021
   and has not been run on these: it is to be measured again on them, as `fit_reason` and the Scope bullet now say.
   `dataset check`: 0 errors, 0 warnings.

10. **Add the release's supplemental file, 21 September 2021 to 24 January 2022?**

   * **Problem:**
     - The release holds `supplemental_train.csv`, 2,518,278 rows from 21 September 2021 to 24 January 2022 that
       continue train.csv without a seam, and the definition leaves it out without giving a reason.
     - With it, the newest window becomes 25 October 2021 to 23 January 2022, the weeks just before the competition
       scored its frozen models (2 February to 3 May 2022), and the data grow by 10.7%.
     - It moves the floor, so issue 9's choice of windows depends on this one.
   * **Background:**
     - The file is dated 26 January 2022 and holds the same 14 coins and columns; Bitcoin closes at 43,002.5 on the
       last minute of train.csv and at 42,947.1 on the first of the file, and peaks at 68,974 on 10 November 2021.
     - The newest window is always tested, as the deployment period[^gr10-split15]; leaving out the release's newest
       months moves that period back by four months.
     - With the file, windows of 91 days that keep half the rows for training reach back to 27 April 2020, seven in
       all; issue 9's option B window from 28 February 2020 (the crash of 12 March) would then train on 48.3%, below the
       floor[^gr10-split14], and a window from 24 March 2020 on 49.9%. The crash would stay in every train side.
     - The test period of the competition (February to May 2022) is not in the release, so the file holds no test
       data of the competition.
   * **Effect on the task:** A tests models up to September 2021. B tests them up to January 2022, closer to the period
     the source scored, and issue 9 is proposed again on the longer history, without the March 2020 crash as a test
     window.
   * **Unknown:** why the definition left the file out: its notes name only the two files it reads.
   * **Sources:** the competition's data page (https://www.kaggle.com/competitions/g-research-crypto-forecasting/data);
     the evaluation phase (https://www.gresearch.com/news/wrapping-up-the-g-research-crypto-forecasting-competition/).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | train.csv only (implemented) | data from 2018 to 20 September 2021; issue 9 as proposed | issue 9's choice stands; the March 2020 crash can be a test window | the release's newest four months unused; the newest window ends four months before the source's own scoring |
     | B | Add the supplemental file | data to 24 January 2022 (+2,518,278 rows); issue 9 proposed again | the deployment period the source scored next; every row the release has | the crash of March 2020 can only be trained on; issue 9 waits on a new proposal |

   * **Recommendation:** B: the newest window stands for deployment, and the release's newest months are the closest
     to the period the competition scored; the notes give no reason to leave them out. **Decision:** A or B?

   **Notes for the AI:** on B, `_load_raw` reads `supplemental_train.csv` next to `train.csv` and concatenates them
   (drop exact duplicates of `timestamp` and `Asset_ID`; check that the two do not overlap), the file goes into the
   warehouse folder of the source (a copy was downloaded to the session's scratch folder on 2026-11-10), the
   `download_description` names it, the notes name the third file and give the new span, then `dataset windows
   g_research_crypto_forecasting_1m` again and a new proposal in issue 9; a dated CHANGELOG entry and a CC line.

   [^gr10-split15]: **SPLIT-15** (Must for the newest window): "The newest window is always a test window".
   [^gr10-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the
     data.

   **Lennart (2026-11-11, change):** Option B: Add the supplemental file.
   Please do and raise this again, how did we miss this data in the first pass?

   **Answer (AI, 2026-11-11):**
   - How it was missed: the definition downloads two named files (`kaggle competitions download ... -f train.csv` and
     `-f asset_details.csv`), so the supplemental file never reached the warehouse; the notes name only the two files
     read, without a word on the third, and no step of `/add-dataset` or the review panel compares the files of a release with the files a
     definition reads. The panels checked the definition against the data it loads, which had no gap to find.
   - The fix going forward: the builder lists every file of the release (for Kaggle, `kaggle competitions files`) and
     the notes say for each file left out why; the column auditor checks that list. This goes into `/add-dataset` and
     the auditor's brief with this round.
   - The file is being added now (B); issue 9's windows are then proposed again on the longer history, since the
     newest window moves to October 2021-January 2022.

   **Resolved (2026-11-11, Lennart):** B: `supplemental_train.csv` is in the warehouse folder next to train.csv and
   matches the issue: 2,518,278 rows from 21 September 2021 00:01 to 24 January 2022 00:00, the same 14 coins and 10
   columns, no (timestamp, coin) pair in both, its first minute the one after train.csv's last. `_load_raw` reads it
   and `_clean` appends it to train.csv before the history features are built, so they run across the seam; the
   frame grows from 23,486,468 to 26,001,823 rows and ends at 23:44 on 23 January 2022. The notes listed only the
   two files read, which is how it was missed. They
   now name the file and why it is read (the release's newest months, the closest to the competition's own
   scoring), the release's files left out and why, and the new counts (753,261 rows without a target, 224 of them
   train.csv's last 16 minutes, and 99 EOS.IO bars of 26-27 October 2021 with a Low near 1.09 against a price near
   4.8, kept); the model figures of 2026-11-06 are dated to the windows that ended on 20 September 2021. The windows
   stay the newest three of 91 days until issue 9 is decided: from 25 October, 26 July and 26 April 2021, training on
   93.0%, 85.9% and 78.9% of the rows. The record has the CC and Assessment lines. `dataset check`: 0 errors, 0
   warnings.

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
