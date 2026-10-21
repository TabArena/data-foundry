# g_research_crypto_forecasting

**Outcome:** added as `g_research_crypto_forecasting_1m`; recommended `No` (`Time-series (Forecasting)`). One row is
one of 14 cryptocurrencies at one minute (G-Research's Kaggle competition, 2018 to 2021); the target is the coin's
return over the next 15 minutes with the market's part removed, tested on three 91-day windows at the end. The data,
the use case and the split hold, but the task is short-horizon forecasting of a price series from its own past
returns, and it meets neither condition under which the rules admit such a task. The review panel agrees
on this under the rules as written; keeping the dataset needs a rule change, which is yours to make.

```text
Verdict: don't ship. `No` + `Time-series (Forecasting)`.
Validity: SEL-1 holds. SEL-10 triggered (Must). SEL-11/TP-10 fail on both legs: leg 1 under RMSE (advocate and
  critic agree), leg 2 on measurement (the features correlate 0.80-0.83 with sums of the coin's own past targets).
  No fix in the definition. USE-1/USE-5/USE-8 hold (direct fit; P3 does not override a P2 Must). LEAK holds.
  SPLIT-1/3/9/10/11/12/14/19 hold.
Value: TP-1 followed; TP-2: a small signal, real under correlation, not separable from the noise under RMSE. Moot
  under `No`.
Quality: CLEAN-11 triggered, fixed (negative Volume to missing); CLEAN-19 departure (one notebook's features,
  issue 2) and SPLIT-20 (no use-case reason for the training history, issue 6), both moot under `No`.
Weighed: use case +, source +, size +, signal -, metric fit -.
For the curator: issue 1, retire, or keep by amending TP-10 (the rule item across datasets); issues 6 and 2 and
  the RMSE item across datasets only if kept; if kept, the licence ("competition use only") and the BibTeX authors
  need a browser check (claim audit, untested).
```

**Main points:** Retire as time-series forecasting (issue 1, recommended), or keep it by amending TP-10; only if it
stays, decide the training history (issue 6) and the source of the features (issue 2). The metric is settled
(2026-10-21): the competition's `weighted_pearsonr`, with the asset `Weight` as a scoring column.

**Record judgment:** valid as a record of a real task, out of scope. G-Research's own competition data and use case
(first-hand source); time-series forecasting under SEL-10. The 2026-10-07 assessment's signal numbers were not
reproduced; the record's 2026-10-20 panel assessment replaces them.

**Issues for Lennart:**

1. **Retire as time-series forecasting?** The target is the coin's own return from minute t+1 to t+16,
   residualised: the part that moves with the 14-coin market (the coin's beta, its sensitivity to the market, times
   the market return) is taken out. A row's own one-minute bar (prices, volume, number of trades) carries no signal
   for it. All the signal comes from the 18 features the definition adds from a public competition notebook: the
   coin's returns over the past 60, 300 and 900 minutes, relative to the market's. The rules exclude forecasting the
   future values of a series (SEL-10) and admit a forecasting-like panel only when both legs of TP-10 hold: (1) a
   model clearly beats each entity's naive forecast on the shipped windows, and (2) the source's top solutions use no
   lagged target (past values of the target as inputs).
   - Effect: the benchmark would score short-horizon return forecasting under a tabular protocol, where under RMSE
     a method wins by predicting close to the coin's mean rather than by finding the signal (issue across datasets,
     "RMSE ranks shrinkage").
   - Evidence, leg 1 (fails; advocate and critic agree): the naive forecast of a return is the coin's mean, which
     scores R² about 0. Early-stopped LightGBM scores R² +0.0006, +0.0013 and +0.0004 against it in the three
     windows, and the 95% interval over test days includes 0 in every window ([-0.0007, 0.0022], [-0.0027, 0.0060],
     [-0.0022, 0.0026]).
   - Evidence, leg 2 (fails on the mediator's measurement): each added feature is, in effect, a sum of the coin's
     own past targets. Over the 14 coins, the median correlation of `log_return_60_minus_market` with the sum of past
     `Target` values covering the same 60 minutes is 0.83 (0.80 for 300 and 900 minutes). The coin's own lags alone
     and the market means alone carry no signal; only the coin's past return against the market does.
   - The top solutions (checked 2026-10-21 at your ask): all of the top three used LightGBM, not sequence models
     (G-Research's wrap-up). The 3rd place trains one LightGBM per coin on the coin's and the market's past
     60/300/900-minute returns (the source of these features); the 14th adds the coin's last 15-minute return, close
     to the last target; no top solution used an LSTM or ARIMA. Tabular models, then, but on the coin's own trailing
     returns, so leg 2 fails in substance.
   - Implemented: the definition as built, with the scope and the recommendation `No` stated in its notes.
   - Alternative: keep it by amending TP-10 (across datasets, "Rules from the G-Research review"): leg 2 narrowed to
     "no lag of the target column itself", leg 1 measured by correlation, a metric the benchmark adapter does not
     have yet. Cost: a rule change written for one dataset that has to say why stock stays out; issues 6 and 2 and
     the metric item across datasets then need decisions.
   - Rule: SEL-10, SEL-11, TP-10 (P2, Must). A real use case (USE-1, P3) does not override a Must, so keeping the
     dataset needs an amendment, not an exception. The advocate argues for the amendment: the actor ranks 14 coins
     against the market each minute, a cross-sectional decision, and the model's correlation with the target is
     positive on 70-74 of 91 test days. The critic: the target is "a price over a horizon" in SEL-10's words, and
     the features and the target are the same Close series on either side of the minute. Precedent: follows stock
     and appliances_energy_prediction (`No` + `Time-series (Forecasting)`) and us_accidents; ashrae was kept only
     after it passed both legs; numerai_v5_2 differs in its source's point-in-time features, which are no lagged
     target. No curator decision accepts this case: the record's "Forecasting-as-tabular task" is an unattributed
     note from the 2026-06-23 sheet import that predates TP-10, and the only `CC` line expected "mostly noise".
   - Recommendation: retire.
   - Decision: `No` + `Time-series (Forecasting)`, or keep. Keeping needs the TP-10 amendment, which is marked in
     the item across datasets; a keep here without that mark is not applied.

6. **If kept: train on the whole history or a recent one?** Each train side is a random 5% of all earlier rows back
   to January 2018 (TabReD's convention), so only about 90k of its 1M rows fall in the 91 days before the test window,
   and 25-30% come from 2018, a market with other price levels and liquidity. The definition gives no reason from the
   use case.
   - Effect: a trading desk that refits each quarter weights recent data; a model trained evenly on 2018-2021 may
     score below what the desk would get. In a quick fit the newest 1M rows, or a random 1M of the last 365 days,
     score better in 2 of 3 windows and tie in the third.
   - Implemented: the random history back to 2018, with a `History:` note that no use-case reason is recorded.
   - Alternative: keep only the rows from December 2019 on, as the notebook did; the oldest window then trains on
     about a year. Cost: a filter in `_clean`, new split sizes and comments.
   - Rule: SPLIT-20 (P4, Should): the history a model refit at each window would train on, with the reason written
     down. SPLIT-21 (Must): the better score of the recent history does not by itself choose it. The split audit,
     the advocate and the critic agree on the facts.
   - Recommendation: if kept, keep the whole history (the `_1m` sampling protocol), with the reason that the
     competition gave participants train.csv as one history from 2018 (split audit); take the filter if you judge
     that a desk would not train on 2018.
   - Decision: the whole history with a stated reason, or rows from December 2019 on.

2. **If kept: features from one public notebook?** CLEAN-19 lets a definition add the features a data scientist on
   the task would build, taking those the top solutions share (alfa_battle_2_0_task_2 took what the 1st, 4th and
   9th places had in common). Here the 18 features come from one public notebook, "Training 3rd place solution"
   (sugghi). That it is the 3rd-place team's code is not verified, and no other solution was compared.
   - Effect: the features set the signal a model can reach. The domain practitioner names what a desk always has
     and the rows lack: the other coins' own returns at the same minute (the notebook's wide layout of 174 columns
     has them) and look-backs shorter than 60 minutes. The task is not misstated; models get less signal than in
     practice.
   - Implemented: the notebook's features for the coin, their 14-coin means and the coin's difference from them,
     one row per coin and minute; the notes say they come from one notebook.
   - Alternative: compare the public top solutions and take what they share. Cost: a browser check of which
     solutions are public (the Kaggle pages render by JavaScript and were not readable here), possibly a new feature
     set.
   - Rule: CLEAN-19 (P7, Should), a departure without a recorded reason.
   - Recommendation: if kept, check the public top solutions and record the comparison.
   - Decision: keep the notebook's features with a stated reason, or rebuild from what the top solutions share.

**Review panel:** don't ship, `No` + `Time-series (Forecasting)` (mediator). Full tier, all ten agents. Claim audit:
the leak, gap, target, size and split claims hold; the scope reason and the signal, early-stopping, autocorrelation
and correlation numbers were refuted or not reproduced and are corrected in the notes; four claims untested (licence,
BibTeX authors, the Kaggle "forecasting competition" quote, the notebook's authorship). Blind review: exclude, since
under RMSE the signal is about R² 0.001 and rankings would measure shrinkage; its concerns about targets overlapping
the test start and uneven sampling do not hold (1-day gap; the frame is the union of the train sides). Agreed: no
leak, the temporal split with its windows and gap, no grouping by coin, the direct use case, and that the dataset
fails TP-10 as written. Settled by the mediator: TP-10's leg 2 by measurement, and the text corrections and the
negative-Volume fix, applied. To the curator: the scope (mediator issue 1, here issue 1), the training history
(mediator 3, here 6), the feature source (mediator 4, here 2), and RMSE against correlation with numerai_v5_2
(mediator 2, now across datasets). Issue numbers 3-5 are gone: the windows and no grouping by coin were agreed,
and the metric moved across datasets.

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: don't ship. `No` + `Time-series (Forecasting)`.
Validity: SEL-1 holds. SEL-10 triggered (Must). SEL-11/TP-10 fail on both legs: leg 1 under the shipped RMSE (both sides
  agree), leg 2 measured here (the history features correlate 0.80-0.83 with sums of the asset's own lagged targets).
  No fix in the definition. USE-1/USE-5/USE-8 hold (direct fit, but P3 does not override a P2 Must). LEAK holds.
  SPLIT-1/3/9/10/11/12/14/19 hold.
Value: TP-1 followed; TP-2: the signal is small and real under correlation, and not separable from the noise under RMSE.
  Moot under `No`.
Quality: CLEAN-11 departure (3 negative Volume, no reason given), CLEAN-19 departure (one solution's features, no reason
  given), SPLIT-20 (no reason given for the history). All moot under `No`.
Weighed: use case +, source +, size +, signal -, metric fit -.
For the curator: issue 1, retire or amend TP-10 (a rule change). Issues 2-4 apply only if TP-10 is amended.
```

The panel agrees on the verdict under the rules as written. The advocate rests the keep case only on an amendment.
Only the curator can amend a Must (principles.md, "Exceptions and amendments").

**Changes to make now (no decision needed)**

These are corrections of fact. Make them whatever the verdict: the scope decision rests on this text, and the record
should not carry wrong numbers into a retirement either.

1. **Scope bullet (writing.md; "Who decides").** Replace "The curators accepted it as a forecasting-as-tabular task"
   with: the record carries an imported, unattributed note "Forecasting-as-tabular task" (2026-06-23 import) that
   predates SEL-11/TP-10; no curator `CC` line accepts it. Replace "all the signal comes from lags of the asset's own
   Close series" with what was measured: the signal is the asset's trailing return relative to the 14-asset mean. Own
   lags alone and market means alone carry none (claim audit 22). These features correlate 0.80-0.83 with sums of the
   asset's own lagged `Target` (mediator, m1).
2. **Signal numbers (EV-8).** In curation_comments, fit_reason and the record's 2026-10-07 assessment: give R² as one
   configuration's values with the model named (+0.0006 / +0.0013 / +0.0004 on refit; +0.0007 / +0.0012 / -0.0003
   earlier, so the sign of window 2 is unstable). Drop "outside the day-to-day noise in window 1": no window's 95% CI
   excludes 0. Add the daily correlation (positive on 70-74 of 91 days). Replace the unreproduced correlations
   0.012/-0.006/0.002 and 0.037/0.051/0.040 with measured values and their method (bar -0.002 / 0.005 / 0.010; all
   0.026 / 0.059 / 0.049, LightGBM prediction against target).
3. **splits_comment (EV-8).** Replace "never stops" and R² -0.0010/-0.0002/-0.0017 with: random-row early stopping
   stops at 220-528 rounds and scores R² -0.0049 / -0.0043 / -0.0090. Replace "0.51-0.55 within 5 minutes" with
   the measured lag-5 autocorrelation (per-asset median 0.57, range 0.25-0.66). The conclusion holds, and more
   strongly.
4. **Negative `Volume` to missing (CLEAN-11, Should).** Add one line next to the VWAP fix. It departs from the rule
   without a reason, and churn_telco_south_asia and force_2020 set such values missing. No shipped row changes.
5. **Wording (writing.md).**
   * task_summary.split should say "a random million earlier coin-minute rows", not "minutes".
   * Decision 1 and the drop bullet: a row has no target when Close(t+1) or Close(t+16) is missing (37% lack only
     t+1).
   * The anomaly counts should be per frame, with the raw counts named as raw: VWAP 13 in the frame against 15 raw,
     Volume 2 against 3, Low 16 against 18.
   * The ">100-minute gap is missing" claim should say that `shift` checks only the end point: 193 / 1,804 / 9,370
     values span a longer gap, as in the 3rd-place code.
6. **Notes (SPLIT-20, CLEAN-19; facts only).**
   * Windows 1-2 fall in the 2021 high-volatility regime: median |900-min return| is 0.029-0.036, against
     0.013-0.022 before.
   * The features come from one public solution (sugghi's notebook, rank-4 evidence). That this is the 3rd-place team
     (GABA) is unverified, and no other solution was compared.

**Issues for the curator, ranked**

**1. Scope: forecasting on lagged targets (P2; SEL-10, SEL-11, TP-10; Must). Decision: retire, or amend TP-10**

* **Problem.** The target is the asset's own residualised forward return. Its only signal comes from trailing returns of
  the same Close series. TP-10 lets a forecasting-like panel in only when both legs hold.
* **Effect.** The benchmark would score short-horizon return forecasting under a tabular protocol. No other dataset in
  the working copy has this design.
* **Leg 1 ("clearly beats each entity's naive forecast"): fails, agreed.** Per-asset mean R² is about 0. LightGBM
  day-block 95% CIs are [-0.0007, 0.0022], [-0.0027, 0.0060] and [-0.0022, 0.0026], and the daily RMSE-gain t is
  0.81 / 0.56 / 0.33. This leg alone fails the Must: every Must has to hold on its own.
* **Leg 2 ("top solutions used no lagged target"): disputed on reading, settled here by measurement.** The advocate:
  the features are price returns, not lags of `Target`, and the last known target alone correlates only -0.02 to -0.03.
  The decisive check is how far each feature is a sum of the asset's own lagged targets. It summed `Target` at t-16,
  t-31, ... to cover the feature's window, on the full cleaned frame. The median correlation over the 14 assets is
  0.83 (`log_return_60_minus_market`), 0.80 (300) and 0.80 (900); per asset it ranges 0.61-0.88 for the 60-minute
  feature. The features are, in effect, aggregated lagged targets. The narrowed leg "no lag of the target column
  itself" would pass them on form only.
* **Advocate's best case.** The use case is real and direct (USE-1, USE-8). The actor ranks 14 coins against the
  market, which is a cross-sectional decision. The signal is real under correlation (positive on 70-74 of 91 days,
  t 6.2-8.6). Leg 1 was written for level series, where the naive forecast is strong.
* **Critic's best case.** SEL-10's wording ("a price over a horizon") fits. Both legs fail. ashrae was kept only after
  it passed TP-10. stock and appliances_energy_prediction are `No` + forecasting. numerai is set apart by its
  point-in-time source features without lagged targets. The record's only `CC` line expects noise.
* **Rule and rank.** SEL-10, SEL-11 and TP-10 are P2 Musts. Nothing of higher rank overrides them, and P3 informs P2
  but is not a higher Must. Keeping the dataset is therefore not an exception: it needs an amendment of TP-10.
  * The amendment would have to drop or narrow leg 2.
  * It would have to re-base leg 1 on correlation, a metric the adapter does not have yet.
  * It would have to say why stock stays out.
* **Decision needed.**
  * (a) `No` + `Time-series (Forecasting)` (recommended; consistent with the precedents).
  * (b) Amend TP-10 as a deliberate rule change, then decide issues 2-4.

**2. Only if amended: RMSE ranks shrinkage (P6; TP-2, Should; a weighing call)**

* **Problem.** The model with the higher correlation scores worse on RMSE. In window 2, corr 0.058 scores R² -0.0090,
  while corr 0.049 scores +0.0004.
* **Problem.** The test sides are sampled by row, about 3.8 of 14 coins per minute, so the per-minute cross-sectional
  score cannot be computed.
* **Advocate.** Keep the dataset with a note (remedy ladder). Register the weighted correlation later.
* **Critic.** Hold the dataset back until the correlation is registered and the test windows are sampled by whole
  minutes.
* **What settles it.** One call for this dataset and numerai_v5_2, which has the same profile (precedents section 3).

**3. Only if amended: training history (P4; SPLIT-20, Should; SPLIT-21, Must)**

* **Problem.** Each train side is a uniform 5% of rows from 2018 on, with no reason given from the use case.
* **Options.** (a) Keep the TabReD convention and state why. (b) Filter to 2019-12 onwards, as the 3rd place did.
* **Limit.** The measured "recent history scores better in 2 of 3 windows" may not decide this (SPLIT-21).
* **What settles it.** What a desk refitting each quarter would train on.

**4. Only if amended: one solution's features (P7; CLEAN-19, Should)**

* **Problem.** alfa_battle took the features the top solutions share. Here the features come from one notebook.
* **Not checked (EV-7).** Whether other top solutions are public, the licence text and the BibTeX authors. Each needs
  a browser check.

**Agreed facts**

* **Target.** The organisers' residualised 15-minute return, rebuilt from Close with a trailing beta (median error
  2.0e-5). The source is first-hand (G-Research on Kaggle), and the use case is real and named by the source.
* **No leak.**
  * The features are identical on truncated raw data (max abs diff 0.0).
  * The leak probes show all features at R² -0.090 and 0.0% exact copies across the split.
  * The 1-day gap covers the 16-minute label delay.
* **Split.** Temporal over the same 14 assets is right. 3 x 91 days follows the competition's live phase. Not grouping
  by asset is right.
* **Where the signal is.** The bar alone has none. Own lags alone have none (R² below the mean in all windows), and
  market means alone have none. The signal is own-minus-market returns: correlation 0.026 / 0.059 / 0.049, positive
  on 70-74 of 91 days.
* **Leg 1.** Under RMSE no window's gain over the mean lies outside the day-block noise. The refit R² is
  +0.0006 / +0.0013 / +0.0004.
* **Refuted text.** The text items listed under changes 1-3 and 5.
* **Blind reviewer.** Its boundary-overlap and uneven-density concerns are not backed: the gap is 1 day, and the
  density is the union of the train sides. Its exclusion verdict rests on the metric (issue 2).

**Consistency with precedent**

* **The `No` follows these precedents.**
  * ashrae passed TP-10 with measured numbers. This dataset fails both legs, so the same phrase does not carry ashrae's
    facts.
  * stock (Lennart) and appliances_energy_prediction (2026-07-27) are `No` + `Time-series (Forecasting)`.
  * us_accidents (2026-09-23) applies the same line.
  * The precedent checker found no drift.
* **Different from numerai_v5_2.** The fact that sets the two apart is now measured: numerai's features come from the
  source and are not lagged targets, while these correlate about 0.8 with lagged-target sums.
* **A precedent not to cite.** REVIEW_before cites cryptocurrency_closing_price_prediction. It is an unverified AI
  record, not a curator decision.
* **Keeping the dataset departs from all of the above.** It needs the amendment in issue 1. The precedent checker's
  consistency-check prompt (precedents.md, section 1) is the one to put to the curator.

</details>

<details><summary>Claim audit</summary>

Claim numbers as in `claims.md`. D = `dataset.py`, R = the record. Models: LightGBM lr 0.05, 31 leaves,
min_data_in_leaf 200, early stopping 100 rounds on 10% of the shipped train side (newest 10% unless said), 2 threads,
shipped splits (3 windows, repeat 0 = newest), R² against the train-side mean. Day-block intervals: 2,000 bootstraps over
the 91 test days. These are one configuration's numbers (EV-8), not tuned results.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 22, 48, 50 | "all the signal comes from lags of the asset's own Close series" | D curation_comments (Scope); R Assessments | LightGBM on bar + own lags vs bar + market means vs all (own minus market) | **refuted** | bar+own corr -0.001 / 0.012 / 0.012, R² -0.00002 / -0.00034 / -0.00178; bar+market corr 0.001 / -0.001 / 0.007; all corr 0.026 / 0.059 / 0.049. The signal is the asset's lagged return relative to the 14-asset mean (cross-sectional reversal), i.e. lagged residualised returns, the same construction as the target | SEL-10, TP-10, EV-6 |
| (implied) | TP-10 leg 1: the model clearly beats each entity's naive forecast | not written; the definition keeps the task in scope | per-asset train mean; last known target (t-16); LightGBM day-block RMSE gain | **fails** | per-asset mean R² -0.00005 / +0.00002 / -0.00002 (= naive); LightGBM R² 95% CIs [-0.0007, 0.0022], [-0.0027, 0.0060], [-0.0022, 0.0026]; daily RMSE gain t 0.81 / 0.56 / 0.33. Leg 2: the last known target alone correlates -0.029 / -0.023 / -0.019 with the target, and the 3rd-place features are lagged log returns of Close | SEL-10, SEL-11, TP-10 |
| 32, 9, 49 | R² +0.00073, +0.00115, -0.00028; "outside the day-to-day noise only in window 1"; "a small real signal" | D curation_comments, fit_reason; R | refit early-stopped LightGBM; day bootstrap; daily correlations | **refuted as stated** (signal under correlation holds) | R² +0.00059 / +0.00130 / +0.00041 (window 2 changes sign); no window outside day noise under RMSE (CIs above); correlation positive on 71 / 70 / 74 of 91 days (t 6.2 / 7.8 / 8.6) | TP-1, TP-2, EV-8 |
| 37 | random-row early stopping "never stops", R² -0.0010, -0.0002, -0.0017 | D splits_comment | same model, random 10% validation | **refuted in detail**, holds in direction | stops at 372 / 220 / 528 rounds; R² -0.0049 / -0.0043 / -0.0090 vs newest-10% +0.0006 / +0.0013 / +0.0004 | SPLIT (inner validation), EV-8 |
| 36 | targets of one asset "correlate 0.51-0.55 within 5 minutes" | D splits_comment | target autocorrelation on the full minute grid | **not reproduced** | lag 5: pooled 0.472, per-asset median 0.567 (0.246-0.657); per test window lag 5 0.41 / 0.62 / 0.64; lag 4 pooled 0.524. Strong autocorrelation holds | EV-8 |
| 23 | bar alone corr 0.012, -0.006, 0.002; with history features 0.037, 0.051, 0.040 | D curation_comments | LightGBM prediction corr, bar vs all | **not reproduced** (direction holds; method unstated) | bar -0.002 / 0.005 / 0.010; all 0.026 / 0.059 / 0.049; per-feature max \|r\| in the decision table is 0.023 (Volume), so the numbers are neither | EV-8 |
| 38 | "a row has no target when the asset's prices 16 minutes later are missing" | D `_decisions` 1 | Close(t+1), Close(t+16) on the raw grid for no-target rows | **refuted in wording** | 750,338 rows: Close(t+16) missing 472,020; only Close(t+1) missing 278,234 (37%); both present 84 | writing.md |
| 25 | the dropped rows' "future prices are missing" | D curation_comments | as above | holds | 750,254 of 750,338 lack Close(t+1) or Close(t+16) | LEAK-22 to 26 |
| 27, 29 | VWAP 7 infinite + 8 negative set missing; Volume negative in 3 rows; 18 Low / 3 High anomalies | D curation_comments | counts on raw vs on the rows the code changes (after the target drop) | **holds for raw, not for the frame** | raw: 6 +inf, 1 -inf, 8 negative = 15; on target rows (what `_clean` touches): 13 (6 inf, 7 negative); Volume negative 2 in the frame; Low anomalies 16 | writing.md, CLEAN-11 |
| 24 | a window reaching into a gap longer than 100 minutes is missing | D curation_comments | log_return present while the trailing mean is missing | **refuted (tiny)** | 193 / 1,804 / 9,370 rows (60/300/900) have a return across such a gap (`shift` checks only the end point); the 3rd-place code does the same | CLEAN-19 |
| 6 | "training is a random million earlier minutes" | D task_summary.split | train side composition | refuted in wording | 1M coin-minute rows, not minutes | writing.md |
| 19, 9, (implied) | every feature uses only minutes up to the row's own | D docstring, fit_reason | history_features on raw truncated at 2019-06-15 12:00 and 2021-03-23 00:00 vs full | holds | 8,461,738 and 20,568,712 rows: max abs diff 0.0, 0 NaN mismatches | LEAK-1, LEAK-10, USE-3 |
| 34 | 1-day gap makes every training label known at window start | D splits_comment | rebuild Target with trailing vs centred 3750-min beta | holds | trailing median abs error 2.0e-5, centred 1.4e-4: beta is trailing, so a label at s needs prices to s+16; gaps 1,441 / 1,441 / 1,442 min. (The 3rd place used a 3,750-min embargo, not needed for leakage with a trailing beta) | SPLIT-9, SPLIT-10 |
| 21, 4, 47 | Target = R(t+1..t+16) minus beta x weighted market return | D, R | rebuild | holds (approximately) | weighted-mean, trailing-beta rebuild median error 2.0e-5 (my NaN handling differs; R's 5e-7 not reproduced, not needed) | USE-5 |
| 11, 20, 3 | 23,486,468 rows, 14 assets, 2018-01-01 to 2021-09-20; raw to 2021-09-21 | D | counts | holds | full frame 23,486,468, 2018-01-01 00:01 to 2021-09-20 23:44, 14 assets, 0 repeated (timestamp, asset) | |
| 10, 35 | 500k per window, 1M train, one random order | D | split sizes; train-side overlap | holds | 1,000,000 / 500,000 each; train overlap 915,166 (w0-w1), 907,218 (w1-w2), against about 48k for independent draws | SPLIT |
| 12 | random train sample covering the whole history (TabReD) | D version_comment | random 1M vs newest 1M before the gap | holds (not refuted) | train_start 2018-01-01 in all windows; newest 1M R² -0.0064 / +0.0028 / -0.0021 vs random +0.0006 / +0.0013 / +0.0004 | SPLIT-4 |
| 31 | RMSE ranks mostly by closeness to the mean | D | same features, different early stopping; oracle rescaling | holds | window 2: random-stopped corr 0.058 > newest-stopped 0.049, R² -0.0090 vs +0.0004; best rescaling factors 0.24-0.74 | USE-5, EV-5 |
| 32 (drift) | drift_baseline comes from a target centred on zero | D | target means | holds | test means 3e-6 / 1.7e-5 / 1.2e-5 against SD 0.0044 / 0.0064 / 0.0069; zero predictor R² within 6e-6 of the mean | TP-1 |
| 17, 18 | lags 60/300/900, ffill limit 100, as in the 3rd-place solution | D | third-party transcript of the notebook (Tencent Cloud 2451820) | holds (rank-4 evidence; the Kaggle notebook renders by JS) | `lags = [60,300,900]`, `fillna(method='ffill', limit=100)`, unweighted `np.mean` over assets; the solution also dropped rows before 2019-12-01 and used purged time-block CV | EV-2 |
| 33 | 3 months of live scoring after the deadline; weighted Pearson | D | G-Research wrap-up page | holds | "ran them for three months against real live market data"; "weighted Pearson correlation coefficient" | |
| 26, 28, 40 | Asset_Name category, Weight not a feature, timestamp datetime, rest numeric | D | dtypes of the shipped frame | holds | 26 float64, 1 datetime, 1 category (14 names) | |
| 39 | recent returns carry signal, ranks most clearly | D `_decisions` 2 | decision table | holds | Spearman up to -0.060 vs Pearson -0.033 | |
| (implied) | no row is a copy across the split | not written | leak probe 5; hidden groups | holds | 0.0% exact copies; near copies 1.2% of test rows | LEAK-16 |
| (implied) | target is the real-world target | not written | rebuild; source page | holds | the competition's own Target | USE-5 |
| 8 | fit "direct" | D | USE-8 criteria (rows, features, label timing, split) | holds by the letter | the metric is not a USE-8 criterion; the actor's metric gap is named in fit_reason | USE-8 |
| 14, 16 | licence; BibTeX authors | D | Kaggle rules / citation pages | **untested** | pages render by JavaScript; WebFetch returned titles only | EV-7 |
| 46 | the competition calls itself "a forecasting competition" | R | Kaggle overview | **untested** | JS page; G-Research's page supports a live forecasting phase | EV-7 |
| 17 (authorship) | the sugghi notebook is the 3rd-place solution | D, R | search | **untested** | G-Research names team "GABA" third; no source links sugghi to GABA | EV-7 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P2, SEL-10 / TP-10 (Must): the scope bullet's reason is wrong, and TP-10 fails on both legs.** The signal does not come
   from the asset's own lags (own lags alone: R² below the mean in all three windows); it comes from the asset's lagged
   return relative to the market, which is a lagged residualised return, the construction of the target itself. Leg 1:
   nothing clearly beats the per-asset naive forecast under the shipped metric (CIs include 0 in all windows). Changes:
   strengthens issue 1 (No + `Time-series (Forecasting)`), it does not rescue the dataset. Mildest remedy if kept: reword
   the scope bullet to "lagged returns of the asset relative to the 14-asset mean (lagged residual returns)" and record
   the curator's acceptance as an explicit exception-or-amendment question, since SEL-10 is a Must (principles.md:
   a Must has no exceptions, only an amendment).
2. **P6, TP-1/TP-2 (Should): the R² numbers and "outside the noise in window 1" do not survive a second run.** Window 2
   changes sign (+0.00041 vs -0.00028) and no window's RMSE gain is outside day-block noise; correlation is positive on
   70-74 of 91 days in every window. Changes: under RMSE the benchmark cannot separate methods by signal; under the
   competition's correlation it can. Remedy: report R² as a range from one configuration (EV-8), drop "outside the noise
   in window 1", and keep the metric issue open (issue 3).
3. **P4 support / EV-8: splits_comment numbers (claims 36, 37) not reproduced.** "Never stops" is false at lr 0.05 (220-528
   rounds); the autocorrelation range 0.51-0.55 matches no pooling I tried. The conclusion (validate on time blocks)
   holds, more strongly (R² -0.004 to -0.009 with random rows). Remedy: state the measured numbers and how they were
   computed.
4. **EV-8: claim 23's correlations** have no stated method and are not reproduced (bar -0.002 to 0.010; all 0.026 to
   0.059). Remedy: name the model and the statistic.
5. **Writing / P7 (claims 38, 27, 29, 24, 6):** no-target rows are missing Close(t+1) or Close(t+16), not only t+16
   (37% only t+1); anomaly counts describe the raw file, the frame has 13 bad VWAP and 2 negative Volume; 9,370 rows of
   `log_return_900` span a >100-minute gap; "minutes" should be "rows". Remedy: wording only.
6. **Untested (EV-7):** licence, BibTeX authors, the Kaggle "forecasting competition" quote, and whether the sugghi
   notebook is the 3rd-place team's. For the curator to check in a browser.

</details>

<details><summary>Column audit</summary>

Frame: the built container from the README build record (`dataset_io.load(..., built=True)`), 2,501,039 rows x 29
columns (target + 28: `timestamp`, `Asset_Name`, 7 bar columns, 18 history features). Three temporal splits (one fold
each): train 1M rows from 2018-01-01, test 500k rows; test windows 2020-12-22..2021-03-22, 2021-03-23..2021-06-21,
2021-06-22..2021-09-20 23:44; train ends one day before each (gap 1 day >= the 16-minute label horizon). Rows sorted
by time (CLEAN-23).

Prediction point (first curation bullet): the close of minute t; known then every one-minute bar of the 14 assets up
to and including t. Target = return Close(t+16)/Close(t+1) of the asset minus beta x weighted market return (organisers'
tutorial). Codebook: Kaggle data page (timestamp: the minute covered by the row; Asset_ID; Count: number of trades in
the minute; Open/High/Low/Close; Volume: units traded in the minute; VWAP: volume-weighted average price of the minute;
Target: 15-minute residualised return).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `Target` | 15-minute residualised forward return, t+1 to t+16 (codebook; tutorial) | label | float64; 750,338 rows without target dropped (CLEAN-15); 266 \|T\|>0.2 kept (real, BCH fork); range -0.253..0.329 in frame | fine | CLEAN-15, LEAK-24 (not censored: test end 23:44 < raw end 00:00) |
| `timestamp` | the minute the bar covers (codebook), Unix s -> datetime | yes | datetime64; all whole minutes; sorted | fine (time index, kept and processed into its meaning) | CLEAN-3, CLEAN-14, CLEAN-23 |
| `Asset_Name` | the coin, from `Asset_ID` via asset_details.csv | yes | category, 14 levels; `Weight` (metric weight) not a feature | fine; single-feature R^2 -0.0002 | CLEAN-3, CLEAN-12 |
| `Count` | trades in the minute (codebook) | yes, at the bar's close | float64, all integer-valued (as in the source), min 1 | fine (int would be cosmetic only) | CLEAN-14 |
| `Open` | first price of the minute | yes | float64, >0, no inf | fine | - |
| `High` | max price of the minute | yes | float64; 0 rows High<Low, Close outside [Low,High] 0 in frame; 3 raw bars above twice open/close kept as unusual | fine | CLEAN-11 (unusual stays) |
| `Low` | min price of the minute | yes | float64; 18 raw bars below half of open/close kept | fine | CLEAN-11 |
| `Close` | last price of the minute; the series the target and all 18 history features come from | yes (it is minute t's close) | float64, >0 | fine (level non-stationary; test prices exceed the train range, a property of the task, not a cleaning issue) | LEAK-34 |
| `Volume` | units traded in the minute | yes | float64; definition keeps 3 negative raw values (Maker); none in the shipped frame (min 1.1e-7) | cleaning problem, definition-level, no effect on this build | CLEAN-11 |
| `VWAP` | volume-weighted average price of the minute | yes | float64; 15 inf/negative (Maker, June 2020) set missing; in frame 0 outside [Low, High], 0 missing | fine | CLEAN-11, PROV-13 |
| `log_close_to_mean_{60,300,900}` | log(Close_t / trailing mean of Close over the last L minutes, t included) on the minute grid, ffill <= 100 min | yes (trailing window ends at t; truncation test in checklist: max abs diff 0) | float64; missing 0.004-0.05% (window into a gap >100 min or before the asset's first minute) | fine; question for curator (lagged own series, scope) | LEAK-10, LEAK-34, CLEAN-19; SEL-10/TP-10 question |
| `log_return_{60,300,900}` | log(Close_t / Close_{t-L}) | yes | float64; missing 0.003-0.03% | fine; same question | same |
| `market_log_close_to_mean_{L}`, `market_log_return_{L}` | unweighted mean of the feature over the assets with a value at minute t (ffilled values included) | yes: cross-section at minute t, no statistic over rows or time beyond the trailing window | float64; missing 0.001-0.016% | fine (per-minute cross-asset mean, not an all-rows statistic) | LEAK-29/CLEAN-7 not triggered; LEAK-10 |
| `*_minus_market` (6 columns) | asset's feature minus the market mean at minute t | yes | float64; never exactly 0 (no minute with a single asset in the frame); a linear combination of two other columns, not an exact copy (hash check: no copies among the 27 numeric columns) | fine | CLEAN-5 (not a copy), CLEAN-22 |

Missingness of the history features is caused by the past (an asset's first minutes, a gap over 100 minutes), not by
the outcome. Rows with `log_close_to_mean_900` missing (1,279) have a larger mean |Target| (0.0055 vs 0.0031): such
minutes are volatile restarts, which a trader also sees; leak probe: every missing indicator R^2 0.0. Not a leak.

Not in the frame, correctly: `Asset_ID` (replaced by its name), `Weight` (a metric weight, constant per asset, not a
measurement), the rows without target (their bars still feed the history features, which uses only past bars).

**Leaks**

None found. Every column is either the bar of minute t or a trailing function of Close up to t; the label window starts
at t+1. Evidence: the checklist's truncation test (features identical when the data ends 2,000 minutes earlier), my
range check of the splits (train max 23:59 the day before the gap day), leak probes (all features R^2 -0.090, best
single -0.0002, 0.0% exact copies across the split, 1-NN R^2 -1.04). The organisers' beta in the Target is fitted on
forward returns but is not a feature. Under a temporal split over known assets the lags of the asset's own series are
the entity's own history (LEAK-34), not a leak.

**Problems, ranked by principles.md**

1. **P2 scope / P7 CLEAN-19, question for the curator: the 18 engineered columns are the lagged target series.**
   Evidence: `Target` is the residualised forward return of `Close`; every history feature is a trailing function of
   the same `Close` (the market ones of the 14 assets' Close). Without them the bar columns carry no signal (definition:
   r 0.012, -0.006, 0.002; my Spearman of `Count`/`Volume` with the target in the test windows -0.005 to -0.009); with
   them |rho| up to 0.058 (`log_return_60_minus_market`, window 2). CLEAN-19's third bullet (what the top solutions
   share) covers building them; whether a task whose only inputs are lags of its own target series is in scope is
   SEL-10/TP-10, already issue 1 of REVIEW_before. No column-level remedy; the decision is keep (record's
   forecasting-as-tabular acceptance) or retire.
2. **P7 CLEAN-11 (Should), cleaning problem, mild: negative `Volume` kept.** 3 raw rows (Maker) with Volume < 0 are an
   impossible value; the definition notes and keeps them. They are not in the shipped frame (frame min 1.1e-7), so the
   build is unaffected. Mildest remedy: set `Volume < 0` to missing next to the VWAP fix in `_clean` (one line, as for
   VWAP), or leave as is with the existing note since it changes no shipped row.
3. **Cosmetic, no rule broken: `Count` is float64** though every value is an integer count (source dtype). Optional
   cast to an integer dtype; no remedy needed.

No dtype problem: `Asset_Name` category, `timestamp` datetime, the rest float64; no object column (CLEAN-9); no proxy
missing codes; no identifier left; no constant or copied column.

</details>

<details><summary>Split audit</summary>

Verdict: **right with notes.** Temporal, 3 x 91-day windows, 1-day gap, expanding train side randomly sampled to 1M.
The regime, windows, gap and the absence of grouping hold. Two Should-level notes on the training history and on the
regime of the test windows. The open question on this dataset is scope (SEL-10: forecasting on lagged targets), and
no split change can settle it.

**Regime (SPLIT-1/2/3, USE-10, SPLIT-13): holds**

* Use case: at each minute's close, a trading firm forecasts the same 14 coins over the next 15 minutes. The coins are
  known entities, so the split is temporal and recurring assets belong to the task (USE-10, SPLIT-13). All 14 assets
  are in every train side and every test window (35.2k-36.1k test rows per asset per window).
* Grouped by asset: wrong for this use case (a new coin is not the query). With 14 groups it would also be a
  domain-shift test between assets (the "few groups" factor, covertype). Matching the use case was enough, so I fit no
  grouped alternative.
* Hidden-group probe (temporal: no hits). The only candidate, `Count`, is the number of trades and not an entity
  (97.8% of test values are seen in train, as for any count). Near copies: 1.2% of test rows. Nothing to act on.

**Temporal mechanics: holds**

| repeat | train (sampled / eligible) | train span | test (kept / window) | test span | measured gap |
|---|---|---|---|---|---|
| 0 | 1,000,000 / 21,634,209 (4.6%) | 2018-01-01 .. 2021-06-20 | 500,000 / 1,832,105 | 2021-06-22 .. 2021-09-20 | 1 day 00:01 |
| 1 | 1,000,000 / 19,800,061 (5.1%) | 2018-01-01 .. 2021-03-21 | 500,000 / 1,834,142 | 2021-03-23 .. 2021-06-21 | 1 day 00:01 |
| 2 | 1,000,000 / 17,966,284 (5.6%) | 2018-01-01 .. 2020-12-20 | 500,000 / 1,834,016 | 2020-12-22 .. 2021-03-22 | 1 day 00:02 |

* Time column: `timestamp`, the bar's minute. Features use bars up to and including that minute. The label is the
  return from t+1 to t+16 minutes, so it is known 16 minutes later.
* Gap vs label delay (SPLIT-9, SPLIT-10): a 1-day gap against a 16-minute delay, so every training label is known at
  the window start and no training row's label lies after the cutoff. Holds. The 900-minute look-back of test rows
  near a window start reaches into the gap day and train period. That is legitimate history known at prediction time,
  not a leak.
* Windows (SPLIT-12, SPLIT-19): 91 days mirrors the competition's roughly 3-month live scoring phase. Three windows
  (SPLIT-14); the smallest train side is 76% of the full frame's rows. Holds.
* Expanding train side, newest window first (SPLIT-11): holds. As designed, window 0's train side contains 83,879
  window-1 test rows and 84,945 window-2 test rows. Window 1's contains 91,743 window-2 test rows.
* The splits_comment's claim about validation inside a train side checks out: Bitcoin target autocorrelation is 0.84
  at a 1-row lag, 0.59 at 5, -0.06 at 15 and ~0 beyond. A random-row inner validation is optimistic, and inner
  validation must split by time blocks.

**Problems, ranked (principles.md: P4 Should-level first, then by effect)**

**1. SPLIT-20 (Should, P4): the training history is a uniform draw over 3.5 years, so recent data is thin**

* Evidence: each train side is a random ~5% of all earlier rows. Only 84.8k-98.3k of the 1M rows fall in the 91 days
  before the cutoff. 2021 makes up 16% (window 0) and 8% (window 1) of the train side; 2018 makes up 25-30%. The
  history spans very different price levels (BTC at the end of 2018Q4 3.7k, of 2021Q1 58.8k) and regimes.
* Quick fit (LightGBM, early-stopped on the newest 10% of each train side, same test rows, R² against the train mean):

  | repeat | shipped random 1M of all history | newest 1M (~7 weeks) | random 1M of last 365 days |
  |---|---|---|---|
  | 0 | +0.00044 (corr 0.029) | +0.00125 (0.035) | +0.00143 (0.038) |
  | 1 | +0.00153 (0.042) | +0.00355 (0.060) | +0.00220 (0.049) |
  | 2 | -0.00101 (0.032) | -0.00105 (0.023) | -0.00133 (0.023) |

  A recent history does better in 2 of 3 windows and ties in the third. By SPLIT-21 this comparison does not decide
  the history; it only shows that the choice matters at this signal level.
* Rule: SPLIT-20 asks for the history a model refit at each window would train on, with the reasoning written down.
  The definition cites TabReD ("train sides cover the whole history") but gives no use-case argument. A trading firm
  refitting on minute data would usually weight recent regimes.
* Mildest remedy: a weighing call for the curator, with a `History:` bullet either way. (a) Keep the current history
  and say why: the TabReD convention, plus the competition's train.csv offered to participants as one history. (b) A
  history filter, e.g. rows from 2019-12 on in `_clean` (window 2 then keeps about a year, the train sides stay above
  50%), which needs the version_comment and splits_comment updated. Not a validity problem: no leak and no future rows.

**2. SPLIT-20 (Should, P4): two of three test windows fall in an atypical regime**

* Evidence, by quarter on the full frame: the median |900-min log return| is 0.0285 (2021Q1) and 0.0355 (2021Q2),
  against 0.013-0.022 for every quarter of 2019-2020. Target std is 0.0068/0.0065, against 0.0033-0.0067 before.
  Windows 2 and 1 cover the 2020-21 bull run and the May 2021 crash. Window 0 (2021Q3) is typical (0.0225, std 0.0042).
* Rule: SPLIT-20 asks whether the newest windows fall in an atypical season. Crypto has no calendar season, so wider
  windows would not help, and the competition's own live window was also a single market regime.
* Mildest remedy: keep the split, with a note in splits_comment that windows 1-2 are high-volatility. This matters for
  RMSE in particular: the score's scale differs by window, so the per-window score dispersion is partly regime.

**3. Context, not a split fault: scope (SEL-10, SPLIT-6) outranks the split**

The temporal split is right for the task as defined. The task is forecasting on lags of the target's own Close series
(issue 1 of REVIEW_before.md). If the curator rules it out of scope, the split question is moot. The split cannot
"fix" a forecasting task into a tabular one.

**REVIEW_before.md questions re-examined**

* Issue 4 (windows): confirmed. 3 x 91 days with a 1-day gap matches the live phase. Monthly windows would need a
  whole-month gap and add nothing.
* Issue 5 (no grouping by asset): confirmed by USE-10 (known entities) and the few-groups factor. The record's
  `required_split` listing of `Grouped (NON-IID)` should not drive the choice (SPLIT-3: one regime).

Judgment record: Validity: SPLIT-1/2/3 hold (temporal, known entities); SPLIT-9/10 hold (1-day gap vs a 16-minute
delay); SPLIT-11/12/14/19 hold. Notes: SPLIT-20 history (weighing call, measured), SPLIT-20 regime of the windows
(note). SEL-10 scope is the open, higher-ranked question.

</details>

<details><summary>Domain practitioner</summary>

I read this as a quantitative researcher at a systematic trading firm (G-Research's own framing: the competition
"recreates the kind of problems our researchers face", a "low signal, high noise world"). Every minute, at the bar's
close, I score the 14 coins on their next-15-minute market-residualised return and turn the scores into position
changes across the coins.

**Fit**

**Direct, with a metric caveat outside the fit (USE-8).** The rows (coin x minute), the inputs (bars up to and
including minute t plus trailing returns of the coin and the market), the label timing (return from t+1 to t+16, so a
one-minute execution lag is built in) and the split (the next 3 months on the same 14 coins, as the competition's live
phase) mirror the decision; the one real gap is that RMSE does not score what I act on (a ranking/score across coins),
which is an evaluation gap (EV-5), not a fit gap. The `fit="direct"` label is honest; the fit_reason already names the
metric. No USE-9 rephrasing is needed: the use case is the source's own (USE-1).

**1. Inputs at the prediction point (USE-3, USE-6)**

* Have, and the dataset gives: the coin's own bar at t (OHLC, VWAP, Volume, Count), trailing 60/300/900-minute
  log-return and price-over-mean features, their market means and the coin's deviation. The look-ahead test passed
  (checklist P4, max abs diff 0.0 on truncated data). Nothing in the inputs is unknown at t.
* Would always have and is missing (ranked by how much it matters):
  1. **The other coins' individual features in the same row.** I see the full cross-section at once; the row has only
     the equal-weighted market mean of each feature. BTC/ETH lead-lag on alt-coins is the classic cross-asset signal.
     The 3rd-place solution's wide layout (174 columns, REVIEW_before issue 2) keeps it. Moderate effect on signal.
  2. **Short look-backs (1-15 minutes) and volume/volatility features.** The shortest window is 60 minutes; a desk
     always has the last few minutes' returns and realised volatility. The source only shipped bars, so these are
     derivable, but the definition chose the solution's set. Moderate.
  3. **Order book, funding rates, cross-exchange spreads.** Not in the source; I would have them live. Out of reach,
     and not a curation error.
* Not available to me that the dataset gives: none. `Weight` is correctly not a feature (it is the metric weight).
* `timestamp` as a datetime feature: harmless for me (the probe's single feature picked it 2 of 3 splits, which only
  says that drift over time is the strongest 1-D signal in near-noise data); a model extrapolating on it would be
  something I would never deploy.

**2. Target (USE-5)**

* The target is what a market-neutral desk trades: the coin's 15-minute return with its beta to the market removed
  (organisers' definition, rebuilt from Close to 5e-7 by the verifier). Not a proxy.
* What I would want predicted: a **score or rank across the 14 coins at each minute**, not a calibrated number. The
  size of the predicted return matters only relative to the other coins and to the costs. Regression is the right
  problem type; RMSE is the wrong lens: it rewards predicting about zero (untuned LightGBM R^2 -0.075 while still
  correlating), so a benchmark win under RMSE says "shrinks best", not "would trade best" (EV-5,
  BENCHMARK_CHANGES_TODO). This is the largest gap between the benchmark and my decision.
* The 266 targets above 0.2 in absolute value (mostly the Bitcoin Cash fork) are real events I would face; keeping
  them is right, though under RMSE they weigh heavily.

**3. Row, decision and test data (USE-10)**

* One row is one coin's forecast, not one decision: my decision is the **vector of 14 positions per minute**. With a
  per-row metric this is acceptable; with a cross-sectional metric it would matter how the test window is sampled.
  Each 91-day window holds about 1.83M rows and keeps at most 500k, so on average about 3.8 of the 14 coins survive
  per minute (estimate from the stated counts, assuming row-level sampling). A per-minute information coefficient,
  the number I would actually monitor, cannot be computed on the shipped test sides. If the competition's correlation
  is registered later (REVIEW_before issue 3), sample whole minutes, not rows.
* Known entities, temporal split (USE-10): right. I never forecast a coin I have no history of; the competition and
  I both trade the same 14 coins on later data. A grouped split by coin would test nothing I do.
* Test periods: the last 3 x 91 days to 2021-09-20 with a 1-day gap stand for "the next quarter after I deploy",
  as the competition's live 3 months did. Right.
* Training: a random 1M coin-minutes from all earlier history back to 2018 (TabReD style). I would train on the
  full or recent history and retrain often; 2018 crypto (Bitcoin Cash fork, low liquidity) is a different market from
  2021. The splits_comment's finding that validation must use time blocks (random-row early stopping never stops,
  R^2 -0.0010/-0.0002/-0.0017 vs +0.0007/+0.0012/-0.0003) is exactly what a practitioner knows; a benchmark user
  who validates on random rows of a train side will be misled. Small-to-moderate.

**4. Would I use this model?**

* R^2 of 0.001 and correlation 0.04-0.05 are what real minute-level signals look like; I would not distrust the model
  for being small. I would trust it if: the daily correlation stays positive on most days (it does: 73, 70, 78 of 91
  days, t 7.0, 6.6, 9.2, REVIEW_before issue 3), it holds in the newest window (window 2's R^2 is -0.0003 under RMSE
  but its correlation is positive), and it survives costs (a 15-minute horizon at minute rebalancing implies high
  turnover; the competition and this dataset ignore costs, which is acceptable for a forecasting benchmark).
* I would distrust a ranking of methods under RMSE: it would favour whichever method predicts closest to zero.
* The scope question (forecasting on lagged own returns, SEL-10/SEL-11/TP-10, REVIEW_before issue 1) is a selection
  matter, not a use-case one: for P3 the use case is real, named by the source, and the fit is direct (USE-1, USE-8).
  P3 does not argue for retirement; it can carry the small imperfections (3 negative Volume rows, the "minutes" vs
  "rows" wording).

**Gaps, ranked by how much they change the task**

1. **Metric: RMSE vs the weighted correlation the actor uses** (EV-5; USE-5 at the evaluation level). Changes what a
   win means: shrinkage instead of signal. Not a fit change; a reason the dataset's value depends on
   dataset-specific metrics.
2. **Row vs decision: per-coin rows, row-sampled test sides** (USE-1, USE-8). A per-minute cross-sectional score
   cannot be computed on the shipped test sides; sample whole minutes if the correlation metric comes.
3. **Missing cross-asset detail and short look-backs** (USE-6): only market means of 60-900-minute features; a desk
   has every coin's last minutes. Lowers the reachable signal, does not misstate the task.
4. **Training over the whole history at random** (SPLIT, not USE): the desk trains on recent data with time-block
   validation; the benchmark leaves validation to the method, and random-row validation fails here.
5. **Costs and turnover ignored**: as in the source; acceptable for a forecasting benchmark.

**What a domain expert would change**

* Score with the competition's weighted Pearson correlation (or per-minute Spearman IC), and keep RMSE secondary.
* Sample the test windows by whole minutes so all 14 coins of a minute stay together.
* Add short look-backs (1, 5, 15 minutes) and per-coin realised volatility, or the wide layout with the other coins'
  returns (as the 3rd-place solution).
* Keep fit `direct`; state in the fit_reason that one row is one coin of a 14-coin decision.

**Sources**

* `datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m/dataset.py` (task_summary, curation_comments,
  splits_comment)
* `curation/records/g_research_crypto_forecasting.md`
* `.claude/skills/knowledge-curation/references/use_case.md` (USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10)
* G-Research, "Wrapping up the G-Research Crypto Forecasting competition":
  https://www.gresearch.com/news/wrapping-up-the-g-research-crypto-forecasting-competition/ (purpose, weighted
  Pearson metric, 3-month live evaluation, LightGBM and feature engineering in the top three)
* Kaggle competition page https://www.kaggle.com/competitions/g-research-crypto-forecasting (renders by JavaScript;
  only the title was fetchable)
* 3rd-place solution cited in the record: https://www.kaggle.com/code/sugghi/training-3rd-place-solution (not fetched)

</details>

<details><summary>Blind review</summary>

**Verdict**
Exclude. The honest signal is close to zero: out-of-sample R2 is about 0.001 at best, and mostly negative. A benchmark ranking on this task would reflect how strongly each method shrinks toward the mean, not how well it models tabular data. If it is kept, it needs the changes listed under concern 1.

**What the task is**
This is G-Research's Kaggle competition, held in 2021-22. Each row is one asset (14 cryptocurrencies) in one minute. The target is the asset's 15-minute forward log return, with the market return removed (residualized). A quant fund would make this prediction every minute to set short-horizon positions. The use is real, but it is a weak-signal finance problem. Kaggle scored it with a weighted Pearson correlation across assets, then ran three months of live data after the competition. It was not scored on RMSE or R2.

**Concerns, most serious first**

1. **Little or no learnable signal, so method rankings would be noise.**
   - Setup: the 200k sample, sorted by time, with 10% test windows that start at 60%, 80% and 90% of the data (March, June and August 2021).
   - Default-ish LightGBM (300 trees, all features): R2 relative to the training mean was -0.0074, -0.0048 and -0.0093. Pearson r was 0.035, 0.003 and 0.004.
   - Ridge: R2 was -0.0037, +0.00007 and +0.00016.
   - A heavily regularized small GBM (7 leaves, min_child 2000, 100 trees at learning rate 0.01): R2 was +0.0010, +0.00002 and +0.0019. Correlation was 0.01 to 0.045.
   - Spearman correlation of each single feature with the target is at most |0.054| (`log_close_to_mean_60_minus_market`).
   - With the full 2.5M rows the signal may rise a little, but it will stay at R2 of order 1e-3. Differences between methods will mostly come from regularization and early stopping. Defaults will typically lose to predicting the constant.
   - The target is heavy-tailed: std 0.0058, 99.9th percentile of |y| is 0.052, maximum 0.227. RMSE is driven by a few extreme minutes.
   - Change if kept: score with correlation, as the competition did, or with a metric robust to tails. Add a constant-prediction baseline. Report stability across windows. Better: leave it out of a general tabular benchmark, or put it in a separate "low-signal finance" slice.

2. **The time sampling is uneven, and the table is a subset of the source.**
   - The source has about 24M minute-asset rows. This table has 2.5M.
   - In the 200k sample, rows per month are about 1.4k to 2.7k through November 2020. From December 2020 they are about 12k to 14k, roughly 6 times denser.
   - So 58% of rows are from 2021. The full table seems to keep about 28% of 2021 minutes but only about 6% of earlier minutes.
   - The task file does not document this. It shifts the training distribution toward the recent period and changes what "temporal" means.
   - Change: document the subsampling rule. Better, sample uniformly in time, or keep a contiguous recent block.

3. **Targets overlap at the train/test boundary.**
   - The target spans minutes t+1 to t+16. I confirmed this: correlation with the log return from Close(t) to Close(t+16) is 0.70.
   - So training rows in the last 16 minutes before a test window use test-period prices in their target. Rows are dense in 2021, so this affects a small number of rows.
   - Change: leave a gap of at least 16 minutes, preferably about 1 day, before each test window.

4. **Some features are poorly suited to the split.**
   - The raw price levels (Open, High, Low, Close, VWAP) and Volume/Count are non-stationary across 2018 to 2021. Bitcoin's Close ranges up to about 64.5k.
   - Trees cannot extrapolate these levels into later windows. Dropping them helped LightGBM in 2 of 3 windows.
   - These are legitimate columns, but they are mostly noise here.
   - Change (optional): drop the raw levels, or turn them into ratios to VWAP or Close.

5. **Small items.**
   - 280 rows have Target exactly 0. These are likely stale prices on thin assets.
   - Missing values in the engineered features are below 0.05% (the start of each lookback window).
   - `Asset_Name` is categorical, which is correct.
   - The table contains no `Asset_ID`, no asset weights, and no Kaggle row-level weights. The competition metric therefore cannot be reproduced.

**What checks out**
- **The features look only backward.** On rows of the same asset 60 and 300 minutes apart, `log_return_60` and `log_return_300` exactly equal log(Close_t / Close_{t-k}): correlation 1.0, maximum absolute difference 1.8e-15. `log_return_60` is not correlated with future returns (r = -0.16 at +60 minutes, about 0 at +15 minutes). The `market_*` features use only the same timestamp.
- **No duplicates.** There are 0 duplicate (timestamp, asset) pairs and 0 duplicate rows once timestamp is ignored.
- **Values are plausible.** OHLC is consistent in every row: High is at least max(Open, Close) and Low is at most min(Open, Close). VWAP always lies within [Low, High]. Dates run from 2018-01-01 to 2021-09-20, which matches the end of the Kaggle train.csv. The data is real exchange data, not generated.

**What I could not check**
- The full 2.5M table and the exact 3 test windows: I only had the 200k sample.
- The Kaggle data page text: it requires login. My description of the target (15-minute residualized return, with beta over a rolling 3750-minute window) is from memory of the competition, together with the empirical check above.
- The exact subsampling rule used to go from about 24M rows to 2.5M.
- The scores of the winning Kaggle solutions (I recall a weighted correlation of a few hundredths but did not confirm it).

Sources: https://www.kaggle.com/competitions/g-research-crypto-forecasting/data ; https://www.gresearch.com/news/wrapping-up-the-g-research-crypto-forecasting-competition/

</details>

<details><summary>Precedent check</summary>

Register: none of the four register flags (few_minority, one_feature, scaling over all rows, trivial) involves this
dataset. Its register entries are AI open issues and two AI assessments (2026-10-07, 2026-10-20); there is **no
curator `CC` decision on scope, features, split or signal**. The 2026-10-07 review-page db (artifact) was not
readable from here, so a verdict marked on that page and not copied into R cannot be ruled out.

**Summary table**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Scope: keep as "forecasting-as-tabular" (the definition's stance; R's imported note) | **not reasonable under the ranking** if kept as is (breaks SEL-10, Must; TP-10 fails on both legs) | ashrae (kept 2026-10-15 *because* TP-10 passed), stock, appliances (2026-07-27), us_accidents (2026-09-23) |
| 1b | The run's recommendation `No` + `Time-series (Forecasting)` | consistent | same |
| 2 | 18 lagged-return features of the 3rd-place solution | departs (CLEAN-19, Should) with a stated reason for the signal, without one for "one solution, not what the top solutions share"; cannot rescue issue 1 | alfa_battle_2_0_task_2 (2026-10-13), electric_motor, acquire_valued_shoppers, garments, mortgage |
| 3 | Near-zero signal under RMSE kept (TP-2) | consistent with TP-2 in itself; must be decided alike with numerai_v5_2 | forest_fires (2026-10-06), clock_protein_toxicity (2026-10-06), numerai_v5_2 (open) |
| 4 | Temporal, not grouped by asset | consistent | ashrae (2026-10-15), SPLIT-3 (2026-10-12), covertype |
| 5 | 3 x 91-day windows, 1-day gap, random 1M train sample | consistent (SPLIT-12, SPLIT-19, SPLIT-10); one note on SPLIT-18 | competition's 3-month live scoring; numerai (52-era windows) |
| 6 | Negative `Volume` kept while negative/inf `VWAP` made missing | **departs without a reason** (CLEAN-11, Should; P7, 3 rows) | churn_telco_south_asia, force_2020 (impossible negatives -> missing); mobile_churn (negatives kept *with* a reason) |
| 7 | `fit="direct"` with RMSE instead of the competition's correlation | consistent (USE-8 lists data gaps, not metric gaps) | numerai_v5_2 (approximate for another reason: Faith features) |
| 8 | Precedents cited in REVIEW_before (issues 1, 2) | two citations overstated | see below |

**1. Scope (SEL-10, SEL-11, TP-10; P2, Must)**

**Facts that matter for the rule.** SEL-10 (Must): future values of a series are out. SEL-11 (Must; narrows SEL-10)
and TP-10 (Must, 2026-10-15) admit a forecasting-like panel only when **both** hold: (a) a model on the features
clearly beats each entity's naive forecast on the shipped windows, and (b) the source's top solutions used no lagged
target. Here (measured, checklist P2 and REVIEW_before issue 3):

* (b) fails outright: the target is the asset's own residualised Close(t+16)/Close(t+1)-1 (rebuilt, median error 5e-7);
  the row's own bar carries no signal (corr 0.012 / -0.006 / 0.002); all signal is from 18 lags of the same Close
  series, taken from the 3rd-place solution. It would be the only lagged-target design in the working copy (checked:
  electric_motor's EWMAs are over input columns, not `permanent_magnet_temperature`; garments lags input columns;
  mortgage lags the loan's balance and rate, not `status`; ashrae's top five used no lagged readings).
* (a) fails as well: for a return, the naive forecast is about zero / the train mean, and the best measured R² against
  it is +0.0007 / +0.0012 / -0.0003; only window 1 lies outside the day-to-day noise. "Clearly beats" is not met.

**Closest precedents.**

| Case | Date, who | Facts | Outcome |
|---|---|---|---|
| ashrae_great_energy_predictor_iii | CC 2026-10-15, Lennart | Same imported screening phrase ("this is a forecasting-as-tabular task", 2026-06-23); kept **after** TP-10 was measured: LightGBM 1.261/1.176/1.223 vs naive 1.393/1.273/1.372; top five teams used no lagged readings | kept; set TP-10 |
| stock (TabArena Reject) | Lennart, undated (import) | daily prices of ten aerospace stocks, predict one from the others | `No`, `Time-series (Forecasting)` |
| tesla_stock_price, netflix_stock_price_prediction | Lennart, undated | stock price direction | `No`, `Time-series (Classification)`, `Wrong Domain / Source Modality` |
| appliances_energy_prediction | CC 2026-07-27, Lennart | 10-min readings, own-series energy use | `No`, forecasting |
| us_accidents | CC 2026-09-23, Lennart | authors' own task a 15-min grid forecast | `No`, also tagged forecasting |
| numerai_v5_2 | open (AI 2026-10-07) | finance panel, future 20-day stock return, **source's point-in-time features, no lagged target** | open; the lagged-target leg is what sets it apart from G-Research |

**Reading.** The imported note "Forecasting-as-tabular task" (R line 36) is undated and unattributed, came in with the
sheet import (git 391cf7a, 2026-06-23), and predates SEL-11 and TP-10. By "Who decides" (principles.md) an imported
value ranks below an AI assessment, and the record's only `CC` line ("will likely mostly be noise") argues the other
way. The definition's scope bullet says "The curators accepted it as a forecasting-as-tabular task"; that overstates an
imported note as a curator acceptance. The identical phrase on ashrae was accepted by Lennart only after TP-10 was
measured and passed. Treating like cases alike: G-Research is ashrae's phrase without ashrae's facts.

**Verdict.** Recommendation `No` + `Time-series (Forecasting)`: **consistent** with SEL-10, TP-10, ashrae, stock,
appliances. Keeping it: **not a reasonable exception** (SEL-10/TP-10 are Musts; nothing higher ranked overrides
them). It needs an amendment of TP-10 (drop or narrow the "no lagged target" leg) as a deliberate change, which would
reopen ashrae's reasoning and the stock family.

```text
**Consistency check (AI, 2026-10-20):** keeping g_research_crypto_forecasting as "forecasting-as-tabular" would differ
from ashrae_great_energy_predictor_iii (kept 2026-10-15 only after TP-10 passed: LightGBM beat each meter's naive
forecast, top teams used no lagged readings) and from stock / appliances_energy_prediction (No, forecasting). Here the
top solutions use lagged targets and the best R² against the mean is +0.0012. What sets it apart?
(a) the use case is cross-sectional (rank 14 coins against the market each minute), not a series forecast, so the
lagged returns act as point-in-time features as in numerai, recorded as an amendment of TP-10's second leg (a Must
has no exceptions); (b) treat it like stock and appliances: `No` + `Time-series (Forecasting)`;
(c) reopen ashrae / stock to match; (d) change the rule (amend SEL-11/TP-10 explicitly).
```

**2. Engineered lagged-return features (CLEAN-19, Should; P7)**

* REVIEW_before issue 2 says "the house rule allows feature engineering only to remove leaks or rebuild destroyed
  meaning". That is stale: CLEAN-19's third bullet (Lennart, 2026-10-13, alfa_battle_2_0_task_2) allows "what a data
  scientist on this task would build ... Take the features the top solutions share."
* alfa_battle took the features **the 1st, 4th and 9th place solutions have in common**. D takes one solution (3rd
  place). A departure from "the top solutions share", without a stated reason (it may be that the others are not
  public; not recorded).
* Cited precedents differ in the fact that matters: electric_motor's EWMAs (CC 2026-10-06) are over exogenous inputs;
  acquire_valued_shoppers (CC 2026-10-06) aggregates a purchase history to one row per prediction (CLEAN-19 bullet 3
  exactly). Neither builds the target's own lags.
* Rank: CLEAN-19 is P7; it cannot carry a P2 question. If issue 1 ends in `No`, issue 2 is moot. If issue 1 is
  amended to keep, record which solutions were compared.

```text
**Consistency check (AI, 2026-10-20):** the definition adds the 3rd-place solution's 18 lagged-return features; the
CLEAN-19 precedent alfa_battle_2_0_task_2 (2026-10-13) took the features the 1st, 4th and 9th place solutions share.
What sets this apart? (a) only the 3rd-place code is public / the top solutions agree on these windows, recorded as
the basis; (b) rebuild from what the top solutions share; (c) n/a; (d) amend CLEAN-19 to allow one cited solution.
```

**3. Near-zero signal under RMSE (TP-1, TP-2; P6)**

* TP-1 (Must) is followed: the untuned flags were checked against regularised models (early-stopped LightGBM, tuned
  ridge). TP-2 (Should): a small but real signal is no reason to retire. forest_fires (CC 2026-10-06): R² 0.013, beats
  the mean on 26 of 32 folds. Here about a tenth of that, beating the mean in 2 of 3 windows and outside the noise in 1.
  Keeping it on TP-2 alone is **consistent**; the measured weakness is greater than forest_fires', so if the curator
  keeps it the record should say so (it does, in D's last bullet).
* **Pair to decide alike:** numerai_v5_2 (open, priority 2) has the same profile: per-era correlation 0.006-0.018,
  R² at or below 0.0003, "RMSE mostly ranks shrinkage", competition correlation not yet supported
  (BENCHMARK_CHANGES_TODO.md). Whatever is decided on "RMSE ranks shrinkage" (TP-2, EV-5) should hold for both, or name
  the fact that separates them. Not a departure today: neither is decided.

**4. Temporal, not grouped by asset (SPLIT-3, USE-10)**

Consistent. SPLIT-3 (Must, Lennart 2026-10-12): one regime, the one the use case implies. ashrae (CC 2026-10-15):
"Temporal, not grouped: retrofit savings are measured on the same buildings after the cutoff". Same facts here (same
14 assets, later data). covertype (few groups as a factor) supports not grouping over 14 assets. R's
`required_split` now lists only Temporal (REVIEW_before issue 5's mention of `Grouped` is out of date).

**5. Windows and training sample (SPLIT-10, SPLIT-12, SPLIT-14, SPLIT-19)**

Consistent: 3 x 91 days follows the competition's 3-month live scoring (SPLIT-12, SPLIT-19); the 1-day gap is at least
the 16-minute label horizon (SPLIT-10, SPLIT-9 held, checklist); train side well above 50% (SPLIT-14); random 1M train
rows is the `_1m` collection protocol (TabReD), as for numerai_v5_2_1m and other `_1m` folders. Note, not a finding:
SPLIT-18 (Should, earlier in the file than SPLIT-19) asks short windows for short-lived quantities (weather: 1-2
weeks); a 15-minute return is shorter-lived still. The only SPLIT-18 case is weather, so whether it reaches a
competition-defined window is a question for the curator only if the dataset is kept.

**6. Negative `Volume` kept (CLEAN-11, Should; P7)**

**Departs without a reason.** D sets VWAP's 7 infinite and 8 negative values to missing ("a positive price") but keeps
3 negative `Volume` rows (same asset, Maker) under "Anomaly ... We keep them". A traded volume cannot be negative.
Precedents: churn_telco_south_asia (negative network age -> missing; CLEAN-11 Cases), force_2020 (negative resistivity,
gamma-ray, ROP -> missing), heart_disease_va_long_beach (`chol == 0` -> missing). The one keep, mobile_churn, names a
reason (refunds or corrections). The extreme Low/High bars and |Target| > 0.2 are "only unusual" (Bitcoin Cash fork)
and rightly stay. Effect: 3 rows of 23.5M; cheap and safe fix.

```text
**Consistency check (AI, 2026-10-20):** the definition keeps 3 negative `Volume` values (Maker) while it makes
negative VWAP missing; CLEAN-11 precedents churn_telco_south_asia and force_2020 made impossible negatives missing.
What sets Volume apart? (a) the exchange reports a negative volume as a correction, like mobile_churn's refunds,
recorded as an exception with that fact; (b) set them missing like VWAP; (c) n/a; (d) amend CLEAN-11.
```

**7. `fit="direct"` (USE-8, Must)**

Consistent. USE-8's gaps for "approximate" are data gaps (a snapshot for a forecast, a leak kept on purpose, a rebuilt
time axis, a label without a horizon, one judge). A different metric is not on the list, and no working-copy
definition marks a fit approximate for the metric (grep of `fit_reason`). numerai_v5_2_1m is approximate because of
its Faith features, a different fact. The fit_reason names the metric gap, which is enough.

**8. Precedents cited in REVIEW_before**

* Issue 1 alternative "retire, as `cryptocurrency_closing_price_prediction`, `appliances_energy_prediction` and
  `combined_cycle_power_plant` were": cryptocurrency_closing_price_prediction is `checked_by: AI (UNVERIFIED)`, not a
  curator decision; combined_cycle's `No` rests on a missing timestamp and data quality as much as on forecasting.
  appliances (CC 2026-07-27) stands. Stronger curator precedents: stock (Lennart, `Time-series (Forecasting)`) and
  ashrae's TP-10 (2026-10-15).
* Issue 2: the house-rule premise is out of date (CLEAN-19, 2026-10-13), and the two precedents engineer features from
  inputs or histories, not from the target's own lags (section 2).

**Drift and third exception**

* Drift: no curator decision on SEL-10/TP-10 has gone the other way. Lennart's forecasting calls (2026-07-27,
  2026-09-23, 2026-10-15) all apply the same line; ashrae is in by the test, not against it. No drift.
* Third exception: SEL-10 and TP-10 are Musts with no exceptions on record. CLEAN-11 has one stated keep
  (mobile_churn) and no exceptions recorded as such; no amendment due.

</details>

<details><summary>Advocate</summary>

Position: ship after changes, **only if the curator amends TP-10** (or rules that its second leg does not reach a
market-residualised return). I concede up front that under SEL-10/SEL-11/TP-10 as written today the dataset does not
pass, and that a Must has no exceptions (principles.md, "Exceptions and amendments"). Everything else on the dataset
holds or has a mild fix. The points below are the case that the amendment is worth making and that nothing else stands
in the way.

**1. P3 holds fully: a real use case named by the source, direct fit (USE-1, USE-5, USE-8; Must)**

* Evidence: the source is G-Research's own task ("recreates the kind of problems our researchers face", wrap-up page);
  the target is the organisers' residualised 15-minute return, rebuilt from Close with a trailing beta (median error
  2.0e-5, claim audit 21); practitioner: "The `fit="direct"` label is honest", "Not a proxy"; precedents item 7:
  consistent with USE-8.
* Why it matters against the critic: the tension table (P3 against a scope pattern) says "the use case decides whether
  the scope rule applies" (breast_cancer_prediction, 2026-10-15). The actor here does not forecast a price level; at each
  minute they rank 14 coins against the market. That is the fact a TP-10 amendment would rest on (point 3).

**2. P4 holds: no leak and the right split (LEAK-1, LEAK-10, LEAK-34, SPLIT-1/3/9/10/11/12/14/19; Must)**

* Evidence: history features recomputed on raw data truncated at two cutoffs match the full build exactly (max abs diff
  0.0, 0 NaN mismatches; claim audit 19); leak probes: all features R² -0.090, 0.0% exact copies across the split, every
  missing indicator R² 0.0; 1-day gap against a 16-minute label delay with a trailing beta (claim audit 34, split audit:
  "holds"); temporal over the same 14 known assets matches ashrae (CC 2026-10-15) and SPLIT-3. Column audit: "Leaks:
  None found."
* The blind reviewer's concern 3 (targets overlapping the test start) is already met by the shipped 1-day gap; its
  concern 2 (uneven density) is the `_1m` protocol (the frame keeps the rows a split uses; version_comment says so), and
  each train side is a uniform 1M of all earlier rows (split audit table).

**3. Scope: the signal is cross-sectional, not a series forecast (SEL-10, SEL-11, TP-10; Must). Remedy: an amendment**

* Evidence against "a price over a horizon" (SEL-10's wording): own lags alone carry nothing (bar + own lags R² below the
  mean in all three windows, corr -0.001 / 0.012 / 0.012); market means alone nothing (corr 0.001 / -0.001 / 0.007); the
  signal is the coin's return relative to the 14-coin mean (corr 0.026 / 0.059 / 0.049; claim audit 22). The target is
  itself market-residualised. This is a cross-sectional reversal factor, the same kind of input as numerai's
  point-in-time stock features, scored on a fixed task (SEL-11: "a fixed predictive task that only needs a temporal
  split").
* Leg (b) of TP-10 ("no lagged target"): the features are 60-900-minute log returns of Close, not lags of `Target` (the
  last known target alone correlates only -0.029 / -0.023 / -0.019). Whether a trailing price return counts as a
  "lagged target" for a residualised forward return is a reading the rule does not settle; I concede the precedents
  checker reads it the other way, and that the dataset would be the only working-copy case of this design.
* Leg (a) ("clearly beats each entity's naive forecast"): concede it fails under RMSE (day-block CIs include 0 in all
  windows). For a return the naive forecast is the constant, which has zero correlation; the model's daily correlation
  is positive on 71 / 70 / 74 of 91 days (t 6.2 / 7.8 / 8.6). Leg (a) was written for level series (ashrae meters, where
  the naive profile is strong); on a return it measures shrinkage, not signal.
* Rank: SEL-10/TP-10 are Musts and win over every point below; I do not claim P3 overrides them. What follows: the
  curator either amends TP-10 (precedents' consistency-check option (a)/(d): legs read as "beats the naive forecast on
  the task's own measure of signal" and "no lag of the target column itself"), or the dataset goes `No` +
  `Time-series (Forecasting)`. Also concede: the definition's "The curators accepted it" overstates an imported,
  unattributed note (precedents 1); reword it in any case.

**4. P6: a small real signal is no reason to retire (TP-1 Must followed, TP-2 Should; precedent forest_fires)**

* Evidence: the flags come from untuned models (TP-1); regularised LightGBM is above the mean in 2-3 of 3 windows (R²
  +0.0006 / +0.0013 / +0.0004 in the claim-audit refit), daily correlation stable as in point 3. Tension "right split
  against the score" (P4 over P6): a small signal under the honest split is kept.
* Concede: the R² numbers in the definition are one configuration (window 2 changes sign on refit) and "outside the noise
  in window 1" does not survive (claim audit 32). Mildest remedy: state R² as a range from one configuration (EV-8),
  drop the noise claim, and decide the RMSE-ranks-shrinkage question alike with numerai_v5_2 (precedents 3); register
  the weighted correlation when dataset-specific metrics exist, and then sample test windows by whole minutes
  (practitioner).

**5. P7: the 18 engineered features are allowed by CLEAN-19 (Should)**

* Evidence: CLEAN-19's third bullet (Lennart, 2026-10-13, alfa_battle) allows "what a data scientist on this task would
  build"; REVIEW_before issue 2's premise is stale (precedents 2). Without them the task has no signal; with them it
  matches what G-Research says the top three did (feature engineering + LightGBM).
* Concede the departure: one solution, not "what the top solutions share". Mildest remedy: record which top solutions
  are public and whether they share the 60/300/900 windows; a P7 Should cannot decide the dataset either way.

**6. The remaining findings are wording or one-line fixes (CLEAN-11 Should; writing.md; SPLIT-20 Should)**

* Negative `Volume` (3 raw rows, 0 in the frame): set to missing next to the VWAP fix (one line; churn_telco, force_2020).
* Wording (claim audit 6, 23, 24, 36, 37, 38, 27/29): "rows" not "minutes"; no-target rows miss Close(t+1) or
  Close(t+16); anomaly counts per frame; measured numbers with their method for the autocorrelation and random-row
  early stopping (the conclusion, time-block validation, holds more strongly: R² -0.004 to -0.009).
* SPLIT-20 history and regime: a `History:` bullet giving the TabReD reason (or a 2019-12 filter, the 3rd-place choice)
  and a note that windows 1-2 are high-volatility. Split audit: "Not a validity problem."
* Independent failures are not conflicts: none of these is a Must, and each has a fix below exclusion on the remedy
  ladder.

**Summary for the mediator**

Validity: P3 holds (direct), P4 holds (no leak, right split); P2 fails SEL-10/TP-10 as written, and only an amendment
(curator's call) keeps the dataset. Value: TP-2, small signal, keep with stated ranges. Quality: CLEAN-11 and wording
fixes, CLEAN-19 departure to document. If the curator declines the amendment, the advocate has no higher rule to offer
and the verdict is `No` + `Time-series (Forecasting)`.

**Rebuttal**

No new facts came up, so no new points. The critic and I agree on almost every fact. What is left in dispute is one
reading of SEL-10/TP-10 (a curator's amendment call) and the remedy for the metric.

**Critic 1 (SEL-10/SEL-11/TP-10, Must): concede the verdict under the rules as written; dispute two steps of the argument**

* **Conceded.** As TP-10 reads today, leg 1 fails under RMSE: the day-block CIs include 0 in every window and the daily
  RMSE-gain t is 0.33-0.81. Leg 2 is read against us by the precedents checker. A Must has no exceptions. So without an
  amendment the verdict is `No` + `Time-series (Forecasting)`. I also concede that "The curators accepted it" overstates an
  imported note that ranks last under "Who decides", and that it must be reworded whatever the verdict.
* **Disputed: "P3 does not rescue it".** I never claimed it does (my brief, point 3: "I do not claim P3 overrides them").
  This point answers nothing in my brief.
* **Disputed: "made from the coin's recent returns against the market, which makes it forecasting".** SEL-10 defines
  forecasting as "future values of a series (demand, sales or a price over a horizon)". The target is not a future value
  of the Close series. It is a future return with the market's part removed, and its signal comes only from the
  cross-section: own lags alone score below the mean in all 3 windows (critic's own citation), while relative-to-market
  lags give corr 0.026/0.059/0.049. Whether that counts as "a lagged target" is exactly what the rule leaves open, and that
  makes it an amendment question for the curator, not a settled fact. The critic and I name the same remedy if the curator
  wants to keep the dataset: an amendment. The critic notes that it reopens ashrae and stock. ashrae passed both legs and is
  unaffected by a narrowing of leg 2 to "a lag of the target column". stock (predict one price level from the others) stays
  out under SEL-10's own wording.
* **What follows:** the panel agrees on the outcome under current rules. The only thing left is the curator's
  amendment call (options (a)/(d) of the precedents' consistency check).

**Critic 2 (RMSE ranks shrinkage; TP-2/EV-5/USE-5): concede the fact; dispute "ship only with the competition's metric"**

* **Conceded.** In window 2 the model with the higher correlation (0.058) scores R² -0.0090. Row-sampled test sides
  (about 3.8 of 14 coins per minute) cannot give the per-minute cross-sectional score.
* **Disputed remedy.** TP-2 (Should) says a small real signal is no reason to retire. RMSE is the collection's default
  for every regression set until dataset-specific metrics exist (BENCHMARK_CHANGES_TODO.md). The practitioner rates the
  metric as an evaluation gap (EV-5), not a fit gap. On the remedy ladder, "keep with a documented note" comes before
  holding the dataset back. The critic's remedy would also have to hold for numerai_v5_2, which has the same profile, and
  the critic asks for both to be decided alike. So: keep with the note, register the weighted correlation when supported,
  then sample whole minutes. I accept the critic's version only if the curator applies it to numerai_v5_2 as well.

**Critic 3 (numbers do not reproduce; EV-8): concede**

* Same remedy as my point 4: restate R² as one configuration's range (+0.0006/+0.0013/+0.0004 on refit), drop "outside
  the noise in window 1" and "never stops", and give the autocorrelation and correlation numbers with their method. The
  conclusions they support (time-block validation, a small signal) hold, the first more strongly (R² -0.004 to -0.009
  with random-row stopping).

**Critic 4 (SPLIT-20 history and windows, Should): concede**

* Same remedy as my point 6: a `History:` bullet with a reason (TabReD, or a 2019-12 filter as in the 3rd place), and a
  note that windows 1-2 are high-volatility. Split audit: not a validity problem.

**Critic 5 (CLEAN-19 one solution, Should, P7): concede**

* Remedy: a note on which solutions were compared. The practitioner's missing inputs (other coins' returns, short
  look-backs) lower the signal a model can reach but do not misstate the task (practitioner, gap 3). Adding them is
  optional.

**Critic 6 (negative Volume, CLEAN-11) and 7 (wording): concede**

* One-line fix (`Volume < 0` to missing) and text edits, as in my point 6.

**Agreed**

* The blind reviewer's boundary-overlap and uneven-sampling concerns are not backed (1-day gap; union of the train
  sides).
* P3 and P4 hold.

Judgment record (advocate after rebuttal):
Verdict: `No` + `Time-series (Forecasting)` under the current TP-10. Ship after changes only if the curator amends TP-10's
leg 2 to "no lag of the target column itself" and leg 1 to the task's own measure of signal.
For the curator: issue 1, an amendment call; issue 2, decide the RMSE question for this dataset and numerai_v5_2 together.

</details>

<details><summary>Critic</summary>

Position: do not ship. Point 1 is a Must that the definition cannot fix. Points 2-7 apply only if the curator amends
TP-10 to keep it.

**1. Out of scope: forecasting on lagged targets. SEL-10, SEL-11, TP-10 (Must, P2). Remedy: exclude**

* Problem: the target is the coin's own residualised Close(t+16)/Close(t+1) return. All of the signal comes from 18
  trailing functions of the same Close series. TP-10 (narrowed by SEL-11) lets a forecasting-like panel in only when
  **both** legs hold. Both fail.
  * Leg 2, no lagged target in the top solutions: the definition's features *are* the 3rd-place solution's lagged log
    returns. The claim audit finds that the signal is the coin's lagged return minus the 14-coin mean, which is a lagged
    residual return, the same construction as the target. Own lags alone: R² below the mean in all 3 windows. Bar
    alone: no signal (claim_audit, rows 22/48/50).
  * Leg 1, "clearly beats each entity's naive forecast": per-coin train mean R² is about 0. LightGBM's day-block 95%
    CIs include 0 in **every** window ([-0.0007, 0.0022], [-0.0027, 0.0060], [-0.0022, 0.0026]). Daily RMSE gain t is
    0.81, 0.56 and 0.33 (claim_audit).
* Effect on the task: the benchmark would score time-series forecasting under a tabular protocol. It would be the only
  lagged-target design in the working copy (precedents §1).
* Precedents: ashrae was kept only *after* TP-10 passed (2026-10-15). stock, appliances_energy_prediction and
  us_accidents are `No` + forecasting. No curator `CC` line accepts this case. "Forecasting-as-tabular task" is an
  undated note imported with the sheet, which predates TP-10. The record's only `CC` line expects noise. Under "Who
  decides" an imported value ranks last, so the definition's "The curators accepted it" overstates it.
* P3 does not rescue it. The tension row "P3 informs P2" says to check how the prediction is made in practice. In
  practice it is made from the coin's recent returns against the market, which makes it forecasting. A real use case is
  not a higher-ranked Must that overrides SEL-10.
* No fix in the definition: drop the lags and no signal is left; keep them and leg 2 fails.
* Remedy: `No` + `Time-series (Forecasting)`. If the curator wants it anyway, that has to be an amendment of TP-10
  (a Must has no exceptions). The amendment would reopen ashrae and stock, and the scope bullet must then stop calling
  the imported note a curator acceptance.

**2. Under the shipped metric, methods cannot be separated. TP-2/EV-5/USE-5 (P6, value). Remedy: ship only with the competition's metric**

* Problem: RMSE ranks shrinkage toward zero, not signal. In window 2, the random-stopped model correlates more (0.058)
  but scores R² -0.0090, against +0.0004 for the model stopped on the newest rows (claim_audit row 31). The blind
  reviewer reached "Exclude" for this reason alone (clean_room report, concern 1). Correlation does carry signal
  (positive on 70-74 of 91 days).
* The test sides are sampled by row (about 3.8 of 14 coins per minute). The per-minute cross-sectional score the actor
  acts on therefore cannot be computed (practitioner §3).
* Remedy (if amended in): keep it out of the collection until the weighted correlation is registered as a
  dataset-specific metric, and then sample whole minutes per test window. Decide it alike with numerai_v5_2
  (precedents §3).

**3. The headline numbers do not reproduce. EV-8, writing.md (procedure). Remedy: rewrite with the measured values**

* "All the signal comes from lags of the asset's own Close series": refuted. The signal is relative to the market
  (point 1).
* R² +0.00073/+0.00115/-0.00028 and "outside the noise in window 1": the refit gives +0.00059/+0.00130/+0.00041
  (window 2 changes sign), and no window is outside the noise.
* "Never stops": early stopping on random rows stops at 220-528 rounds.
* "0.51-0.55 within 5 minutes" and the bar/all correlations 0.012-0.051 are not reproduced, and no method is stated.
* fit_reason, curation_comments and splits_comment all rest on these numbers, so the curator would decide on wrong
  facts.

**4. Training history drawn uniformly over 3.5 years without a use-case reason. SPLIT-20 (Should, P4). Remedy: a `History:` bullet, and a note on the windows**

* Each train side is a random ~5% of all rows since 2018. 25-30% of it is 2018, and 8-16% is 2021. A recent history
  scores better in 2 of 3 windows (split_audit §1).
* Windows 1-2 fall in the 2021 bull run and crash: median |900-min return| is 0.029-0.036, against 0.013-0.022 in
  every earlier quarter.
* The definition cites TabReD but gives no use-case argument, which SPLIT-20 asks for. Remedy: state the history with
  its reason (or filter from 2019-12, as the 3rd place did), and note the atypical windows.

**5. Feature set from one solution, not what the top solutions share. CLEAN-19 (Should, P7). Remedy: a note**

* alfa_battle took the features the 1st, 4th and 9th place share. Here one solution's 18 features are taken and no
  reason is recorded (precedents §2).
* The practitioner names what a desk always has and the frame lacks: other coins' individual returns and look-backs
  shorter than 60 minutes.
* Remedy: record which solutions were compared and why these features.

**6. Negative `Volume` kept while bad VWAP is made missing. CLEAN-11 (Should, P7). Remedy: one-line fix**

* 3 Maker rows have an impossible negative volume. churn_telco_south_asia and force_2020 set such values to missing
  (precedents §6). No shipped row changes.

**7. Wording. writing.md. Remedy: edit the text**

* "a random million earlier minutes" should say coin-minute rows.
* 37% of the dropped rows lack Close(t+1), not Close(t+16).
* The VWAP and Volume counts describe the raw file, not the frame (13 and 2 in the frame).
* 9,370 `log_return_900` values span a gap of more than 100 minutes, which the "missing" claim denies.

Dropped (not backed): the blind reviewer's boundary-overlap and uneven-sampling concerns. The shipped 1-day gap holds
(split_audit), and the density it saw is the union of the train sides in the frame, not a property of any one split.

Judgment record:
Verdict: do not ship.
Validity: SEL-10/SEL-11/TP-10 fail on both legs (Must, not fixable) -> `No` + `Time-series (Forecasting)`. LEAK holds. SPLIT-3/9/10 hold.
Value: TP-2 signal real only under correlation; under RMSE, no window beats the mean beyond the noise.
Quality: CLEAN-19 and CLEAN-11 departures; SPLIT-20 history unexplained; refuted numbers to rewrite.
For the curator: amend TP-10 or retire.

**Rebuttal**

We agree on the core point. The advocate concedes that the dataset fails SEL-10/SEL-11/TP-10 as written and that only
an amendment keeps it. The open question is whether that amendment is sound. I hold that it is not, and that the
verdict is `No` + `Time-series (Forecasting)`.

**Advocate 1 (P3 holds, direct fit): concede the facts, dispute the use**

* Conceded: the use case is real and the fit is direct (practitioner; precedents item 7).
* Disputed: the tension row "the use case decides whether the scope rule applies" sends us to how the prediction is
  made in practice. Here it is made from the coin's recent returns, to predict the coin's return over the next
  15 minutes. That is SEL-10's own wording: "a price over a horizon".
* Breast_cancer_prediction was kept because practitioners use tabular models on human readings, which is a fact
  outside the series. No such fact exists here. The advocate also grants that P3 does not override a Must.

**Advocate 2 (P4 holds): concede**

* No leak; the split is right; the blind reviewer's concerns 2-3 are answered. I dropped the same concerns in my brief.

**Advocate 3 (scope is cross-sectional; amend TP-10): dispute**

* Leg (b), "no lag of the target column itself", is a narrower reading than the rule's. TP-10 says "lagged target", and
  SEL-10 says "future values of a series". The features are trailing log returns of Close relative to the 14-coin mean.
  The target is the forward return of the same Close, minus beta times the market. These are the same series on
  either side of t (claim audit 22).
* The advocate's own figure cuts the other way. The last known target alone correlates -0.029 / -0.023 / -0.019 with
  the target. The full model correlates 0.026 / 0.059 / 0.049. So the target's own lag carries a large share of the
  signal (claim audit, TP-10 leg 2).
* The numerai analogy fails on the fact precedents §1 names: numerai ships the source's point-in-time features with no
  lagged target. Precedents states that this leg is what separates the two cases.
* Leg (a) "on the task's own measure of signal": the benchmark scores RMSE, and under RMSE leg (a) fails in every window
  (CIs include 0). The amended leg could only be tested with a metric the adapter does not have
  (BENCHMARK_CHANGES_TODO.md).
* An amendment written to fit this one dataset is a change of the rule, not a case decided under it. It reopens ashrae
  (kept 2026-10-15 because both legs passed) and stock (`No`). Rule: SEL-10 and SEL-11/TP-10 are Musts, and principles
  "Consistent judgement" case 1 applies.

**Advocate 4 (P6, small real signal): concede in part**

* TP-2 applies, and a small signal alone is no reason to retire.
* Disputed: "R² above the mean in 2-3 of 3 windows" is one configuration, and none of the windows lies outside the
  day-block noise (claim audit 32).
* Even if amended in, the dataset should ship only once the weighted correlation is registered and the test windows
  are sampled by whole minutes. The advocate grants both. Until then it measures shrinkage (EV-5, USE-5).

**Advocate 5 (CLEAN-19): concede**

* The remedy is a note recording which top solutions were compared. It is P7 and decides nothing.

**Advocate 6 (Volume, wording, SPLIT-20): concede**

* The remedies match my points 3, 4, 6 and 7. The refuted numbers must be rewritten before the curator decides the
  scope question, because the fit_reason rests on them.

**For the mediator**

* The only dispute is whether to amend TP-10.
* The rule's wording, the precedents (ashrae, stock, appliances, numerai's distinguishing fact) and the record's only
  `CC` line all point to `No` + `Time-series (Forecasting)`.
* If the curator amends anyway, ship only after my point 2 (correlation metric, whole-minute test sampling) and the
  fixes conceded under advocate points 4-6.

</details>

