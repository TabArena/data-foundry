# mortgage

**Outcome:** added. One row per loan and quarter of the Credit Risk Analytics mortgage panel, target the quarter's
status (active, default, payoff), temporal with three one-quarter test windows; the loan state and the macro columns
are lagged to what is known at the quarter's start. Ship with concerns: the windows mostly score the quarter's overall
event rate (issue 2).

**Main points:** Three classes (active, default, payoff) in one-quarter windows. The book's balance and LTV record the
event itself, and its macro columns are the quarter's own values (published after it): both lagged to what is known at
the quarter's start. The windows mostly score the quarter's overall event rate; default-only AUC or four-quarter windows
are the alternatives.

**Record fields that disagree with the definition:**

- `tag`: record `Non-IID (Grouped)`, definition `Temporal (NON-IID)`.

**Record judgment:** valid with concerns. Real loan-level RMBS data from the book's data page, used by the book itself
for a competing-risks model and an out-of-time backtest; no larger source exists. The concerns are the leaking loan
state and macro values (issues 1 and 4) and the level effect of the target (issue 2).

**Issues for Lennart:**

1. **The book's own design leaks through the row's loan state; I lag it.** Should the definition keep the lag?
   - Evidence: on the event row, the row's own balance records the event.
     - Periods 58-60: 5.3% of payoff rows have a zero balance and 14.9% a balance more than 5% below the previous
       one (active rows: 0.02% and 2.6%).
     - 77% of default rows are unamortised (active rows 12%).
     - Out of time, the row's own balance and LTV lower LightGBM's log loss by 0.003-0.005 in six windows; the
       verifier finds the same in every model family.
   - Now: balance, rate and LTV from the previous observation.
   - Alternative: the raw columns as the book uses them.

2. **Target: 3 classes or default only?**
   - Now: `status` (active / default / payoff), the record's multiclass and the R Companion's chapter 11 model.
   - What the 3-class log loss measures: 76-86% of LightGBM's gain over the all-history class shares is the quarter's
     overall event rate, which the previous quarter's shares already give (dummy / drift / LightGBM: 0.1461 / 0.1251 /
     0.1195 in period 60, 0.1553 / 0.1374 / 0.1317 in 59, 0.1564 / 0.1391 / 0.1362 in 58).
     - The per-loan part is 0.0029-0.0057.
     - Without `time`, LightGBM loses 0.0013-0.0122.
     - The logistic regression is no better than the drift constant in periods 59 and 58 (0.1375, 0.1414).
     - So method rankings depend largely on how a method extrapolates the quarter's level.
   - Alternative: binary `default_time` scored by ROC AUC (the book's ch. 6 models and ch. 13 backtest), as a separate
     folder (for example `mortgage_default`).
     - It ignores the level and treats payoffs as non-events.
     - LightGBM default AUC 0.59 / 0.71 / 0.61 on the one-quarter windows (43-77 defaults each).

3. **Window length: one quarter or one year?**
   - Now: 3 one-quarter windows (the book's backtest on one period; lending_club's quarterly refit), each with
     8.0-8.5k rows and 43-77 defaults.
   - Alternative: 3 four-quarter windows (periods 49-52, 53-56, 57-60).
     - 33-37k rows with 222 / 389 / 678 defaults.
     - LightGBM log loss 0.1288 / 0.1604 / 0.1810 against the previous year's shares 0.1337 / 0.1629 / 0.1876.
     - The level is still 64-84% of the gain.
     - Default-only AUC 0.60 / 0.63 / 0.66.
   - Longer windows give more stable scores but do not remove the level effect. The verifier and I keep the current
     design; Lennart decides.

4. **Macro lags: per series, or all one quarter back?**
   - Now: each series as published when the quarter starts (uer t-1, gdp t-2, hpi t-2; LTV with hpi t-2).
   - Simpler alternative: all three one quarter back, keeping the source's lagged LTV. GDP growth and the house price
     index are then still one to two months early (GDP about a month after the quarter, Case-Shiller two months
     after its month).
   - Keeping the quarter's own values is not an option (F1).
   - Not fixable: the file's GDP figures differ from FRED's current release (period 60: 2.84 against 4.0) and their
     release date is unknown.

5. **Regime.** The record lists Grouped and Temporal; v2 declares one.
   - Now: temporal, with loans recurring across the cut on purpose (99.4-99.9% of test rows).
   - Not built: a loan-grouped variant. It would train on quarters after the test quarters.

7. **Duplicates and censoring kept.**
   - 58 rows come from 8 pairs of ids with identical origination profiles. Some may be one loan listed twice (ids
     3018 and 3020).
   - 501 loans leave before period 60 without an event; their last row stays `active`. 75 of them leave together
     after period 59, a pool leaving the data rather than missed defaults (F4).
   - Both are under 0.1% of the rows.

8. **The source de-identified the periods; the comments re-identify them as quarters 2000 Q2-2015 Q1** (three public
   series match). Fine to state?

9. **Probe and framework notes** (not patched):
   - `task_probes.py` caps the train side at 50k random rows. On a drifting panel the newest periods are then thin.
     For temporal tasks the cap could keep the newest rows.
   - The 1-NN agreement in `leak_probes.py` mostly measures panel repetition on loan-period data.
