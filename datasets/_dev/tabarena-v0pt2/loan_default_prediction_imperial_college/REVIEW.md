# loan_default_prediction_imperial_college

**Outcome:** added. The AI recommends shipping it; the panel's changes are made (second paragraph). Kaggle's "Loan
Default Prediction - Imperial College London" (2014): 105,471 loans of an unnamed lender in time order, anonymised
features, the target the loss per 100 of the loan (0 for 90.7%); a lender ranks new loans by expected loss to choose
which enter a portfolio. Validity: SEL holds; USE-1 holds, fit approximate (anonymised fields, no dates); LEAK-10
triggered and fixed three times: the golden features f527/f528, a family of 28 columns that record the entity's previous
loan's loss after the fact (f221 gives it at ROC AUC 0.993 even when that loan was granted 1-10 loans earlier), and
f468, f471, f536, whose top values record the loan's own period; f533 goes with the six aggregates you accepted dropping
(issue 1); LEAK-38: f615, f617 and f13 tested and kept with a `Potential leak, kept on purpose:` note (f615/f617 give
the previous loan's loss well only when it lies far back, as history would; f13's low values follow the own period as a
smooth gradient, like ordinary columns); LEAK-21 holds (a loss does not end a chain, unlike iranian_churn); SPLIT-1, 9,
11 and 14 hold; SPLIT-10 met by a 5,800-loan gap (issue 2). Value: a small real signal after all drops (TP-2: normalized
Gini 0.196, 0.146 to 0.230, above 0 on 9 of 9 windows; a loss ranked at ROC AUC 0.69-0.73 on the 9 windows); MAE
overruled because predicting 0 beats every model trained on the loss (MET-2, MET-4); the metric's origin label is issue
3. Quality: f6, the host's "person instructing the loan", typed categorical (CLEAN-14). Weighed: size and a real lending
decision +; anonymised fields and a small signal -.

Changes made after the review panel: the 28-column family, f468, f471, f536 and f533 dropped (LEAK-10); a gap of 5,800
loans with 9 windows of 5,000 loans; the metric declared `context` instead of `stand_in`; `use_case` narrowed to ranking
loans for portfolio entry (the Gini cannot see a price level); f6 categorical; the evidence text corrected (the host's
full quote, the circular f527 test replaced). The numbers here and in the issues are re-measured on the changed
definition (untuned LightGBM, one fit per window); the panel's are from before the changes. For the record: the wrong
"f275 = f274^2" is corrected and the `Non-IID (Temporal)` tag added at hand-over; we propose removing the
`Data Quality Issue` marker, since the concern behind it (the iranian_churn chain pattern) is refuted; it stays until
your mark.

Changes made on 2026-11-06 (AI, under the exposure rules; no re-review panel): an exposure paragraph in the notes (the
target is a lifetime loss per 100 of notional, folded in by the source, so no weight is declared; an annual rate over a
loan's realized life would bring back the cut-time leak, LEAK-41). Not checked on the data and not re-reviewed: the
competition's files download only after its rules are accepted on Kaggle
(https://www.kaggle.com/competitions/loan-default-prediction/rules), so the panel of 2026-11-06 did not run; it runs
once the data is in the warehouse.

**Main points:** Keep f533 and the six aggregates out as one block, or restore all seven (issue 1)? The 5,800-loan gap
or no gap (2)? The Gini as `context` (with an amendment of MET-11) or the fallback `rmse` (3)? And the proposal to
remove the `Data Quality Issue` marker (it stays until your mark).

**Issues for Andrej:**

1. **Keep f533 and the six aggregates out as one block, or restore all seven?**

   * **Problem:**
     - Six running averages of a hidden value x were dropped, with f533 added, as siblings of the leaking golden
       features f527/f528, before any test of the six.
     - Tests without labels since find no sign of a leak in the seven.
     - Keep them out as one block, or restore them?
   * **Background:** each row is one period of a hidden entity, and these columns are running averages of a hidden value
     x updated once per period. The golden features f527/f528 average in x of the loan's own period, the period in
     which its loss arises, which is how they give the loss away. On 2026-11-01 you accepted the AI's Assessment, which
     dropped f529-f531, f534, f535 and f537 as siblings of f527/f528 before any test of the six; we added f533 to the
     block.
   * **Experiments:** two tests that use no labels find no such sign in the six: their changes track the own period's
     change of x as weakly as ordinary columns do (rank correlation 0.02-0.21), and among their highest values (rows
     without a loss) the own period's x changed hardly more often than the previous period's. f533 behaves the same
     (own 69% against previous 63% of its highest values; f529 69% against 62%). In f468, f471 and f536 the own
     period's x changed in 86-100% of their highest values against 33% of all rows without a loss, so those three are
     dropped.
   * **Effect on the task:** nothing measurable. Restoring all seven moves the Gini by -0.021, +0.010 and -0.011 and
     the ROC AUC for a loss by 0.000, +0.003 and +0.006 on 3 windows, within noise.
   * **Consistency:** a feature may not be an aggregate that may include the row's own outcome[^1a], while a column
     leaves only for what it is[^1b]; honest evaluation outranks cleaning, so the drop is defensible[^1c]. Against it:
     online_shoppers `PageValues` and account_debt_south_africa's billing totals were kept once the data showed them
     behaving like history[^1d].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the seven as one block (implemented) | f529-f531, f533-f535, f537 stay out, recorded as an exception to the precedent | aggregates of the same hidden x as two measured leaks; with anonymised fields a test without labels is indirect | departs from `PageValues` and account_debt |
     | B | Restore all seven | the seven come back with a note that they are kept on purpose | follows the precedent; the tests without labels find no sign | they share x with two measured leaks |

   * **Recommendation:** A, the block as one exception: they average the same hidden x as two measured leaks, and with
     anonymised fields a test without labels is indirect (advocate and critic agree). **Decision:** A or B?

   **Notes for the AI:** on A, record the exception with this fact: "aggregates of the same hidden x as two measured
   leaks (f527, f528), and with anonymised fields a test without labels is indirect". On B, restore the seven in
   `_clean` with a `Potential leak, kept on purpose:` note. f468, f471 and f536 stay dropped either way.

   [^1a]: **LEAK-10** (Must, P4): a feature holds only what existed at the prediction point; out goes, among others,
     "an aggregate that may include the row's own outcome". Amended 2026-10-26 (Lennart): a window sum stays when the
     data shows it does not move with the outcome, case by case.
   [^1b]: **CLEAN-22** (Must, P7): columns leave for what they are (a leak, an identifier, a copy, the measurement
     that defines the label), never for how many there are.
   [^1c]: principles.md ranks **P4** (honest evaluation, validity) above **P7** (the expert state, quality).
   [^1d]: Lennart, 2026-10-26: online_shoppers `PageValues` and account_debt_south_africa's billing totals kept.

   **Consistency check (AI, 2026-11-01):**

   * **Checked:** the drop of the six you accepted differs from `PageValues` and account_debt, both kept[^1e].
   * **Asked:** what sets them apart?
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The shared hidden x (implemented) | the block stays dropped, recorded as an exception | no rule changes | an exception to a precedent |
     | B | Treat them like `PageValues` | the seven are restored | follows the precedent | they share x with two measured leaks |
     | C | Reopen `PageValues` and account_debt | the two earlier calls are decided again | one reading for all three | reopens settled datasets |
     | D | Amend the leak rule | the siblings of a measured leaking aggregate go with it[^1f] | a standing rule, no exception | a rule change for one case so far |

   * **Recommendation:** A, the block as one exception (advocate and critic agree). **Decision:** A, B, C or D?

   [^1e]: Lennart, 2026-10-26: online_shoppers `PageValues` and account_debt_south_africa's billing totals kept.
   [^1f]: **LEAK-10** (Must): would gain a clause that the siblings of a measured leaking aggregate leave with it.

   **Resolved (2026-11-03, Andrej):** A, the seven stay dropped as one block, recorded as an exception to LEAK-10's
   precedent (`PageValues`, account_debt) with the fact that sets it apart: aggregates of the same hidden x as two measured leaks (f527, f528), and with anonymised fields a test without labels is indirect. In the record, the
   dataset's notes and the Cases table of `leak_checks.md`.

2. **Keep the 5,800-loan gap, or ship without a gap as an exception?**

   * **Problem:**
     - A refitting lender knows only the outcomes of loans that have ended; a loss settles after the loan's term and the
       workout.
     - The split leaves a gap of 5,800 loans for that delay, which without dates cannot be sized in rows.
     - Keep it, or ship without a gap?
   * **Background:** loan terms "vary by a factor from 1 to 3". The release holds only completed loans, so no label in
     the file is pending: the gap stands for the delay a refitting lender faces.
   * **Experiments:** on the 9 windows the gap changes the Gini by -0.002 and the ROC AUC for a loss by -0.003 on
     average, against training up to the window (the panel found the newest 5,800 training loans worth no more to a
     model than the oldest 5,800, on 2 windows).
   * **Consistency:** the rules ask for a gap of about the label's delay, and a departure needs a fact that sets the
     case apart[^2a]. lending_club's fact (a gap of the delay leaves less than the 50% training floor[^2b]) does not
     hold here: with the gap the oldest window trains on 51.8% of the rows. The only candidate fact, a term long
     against the file's unknown span, is inferred. You declined the amendment for labels that mature longer than the
     training floor allows[^2c], so B would be an exception of its own.
   * **Panel:** A is the advocate's proposal, conceded by the critic.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Gap of 5,800 loans (implemented) | 5,800 loans left out between train and each of 9 test windows of 5,000 loans (461-527 losses each) | no exception needed | none measurable (Gini -0.002) |
     | B | No gap | train runs up to each of 9 test windows of 5,800 loans, recorded as an exception with the inferred fact and the measured effect (not "as lending_club") | trains up to the window | an exception resting on an inferred fact |

   * **Recommendation:** A: it removes a departure instead of resting one on an inferred fact, at no measurable cost.
     **Decision:** A or B?

   **Notes for the AI:** A is `TemporalSplits(window=5000, unit="rows", n_windows=9, gap=5800)` in `dataset.py`. On
   B, set `window=5800` without the gap and record an exception to SPLIT-10 stating the inferred fact and the measured
   effect, not "as lending_club".

   [^2a]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose outcome
     is known by the window's start, with a gap of about the label's delay; a departure is recorded as an exception
     with the fact that sets the case apart.
   [^2b]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data. lending_club departed from SPLIT-10 for this floor (Lennart, 2026-10-21).
   [^2c]: Andrej, 2026-11-02, avito_demand_prediction_1m issue 4: the SPLIT-10 amendment for labels that mature longer
     than the training floor allows was declined.

   **Resolved (2026-11-03, Andrej):** A, the gap of 5,800 loans, as implemented; no exception needed.

3. **Declare the normalized Gini as `context`, or go to the fallback `rmse`?**

   * **Problem:**
     - The competition scored MAE, but here predicting 0 beats every model trained on the loss, so MAE is
       overruled[^3a].
     - The question is the label of the metric's origin and, behind it, the metric: the Gini as `context`, or the
       fallback `rmse`.
   * **Background:** without the golden features MAE's best prediction is 0 for nearly every loan: predicting 0 scores
     0.800 and every model trained on the loss scores worse.
   * **The labels:** every metric names one origin[^3b]. `stand_in` (as built) needs an original that cannot be
     computed and a close replacement; MAE can be computed and the Gini is no close version of it. `context` is
     written for a source with no metric; `fallback` covers a source metric the task would not use and gives `rmse`.
     Neither label was written for an overruled competition metric with an obvious task metric.
   * **Experiments:** on 3 windows `rmse` tells the hurdle model from LightGBM on the loss apart at least as clearly as
     the Gini (a difference of 2.2-2.8 standard errors under RMSE against 1.1-2.1 under the Gini). The largest 1% of
     the errors hold 71-82% of the squared error, and the hurdle model's R^2 is 0.006 (above the training mean on 8 of
     9 windows).
   * **Consistency:** for `context`: your policy call 3 of 2026-10-30[^3c]; the four insurance tables
     (australian_vehicle, frempl and both spanish_motor tables) declare `context` because their sources fix no metric.
     For `rmse`: principles.md sends an overruled competition metric to the fallback[^3d], and
     african_credit_scoring_challenge went there (Lennart, 2026-10-26). This dataset would be the only case of a
     `context` after an overruled source metric so far.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `context`, as an exception (implemented) | scores the normalized Gini, its `context` origin recorded as a one-dataset exception; `use_case` narrowed to ranking for portfolio entry (the Gini ignores the level) | credit practice selects a risk model by its Gini; the host's aim was to "flag the worst of the population" | a one-dataset exception to a Must |
     | B | `context` with an amendment | scores the Gini as in A, and the rule's `context` origin is amended to also cover a source metric overruled for a mismatch with the task or for bias | no exception | a rule change for one case so far |
     | C | Fallback `rmse` | scores `rmse` (origin `fallback`); `use_case` back to pricing | follows african_credit_scoring_challenge; scores the loss level; separates the two models at least as well | largest 1% of errors hold 71-82% of the squared error |

   * **Recommendation:** B, so the label rests on the rule instead of a one-dataset exception to a Must.
     **Decision:** A, B or C?

   **Notes for the AI:** A records a one-dataset exception to MET-11 with the fact that MAE's optimum is 0 here. B
   amends the `context` bullet of MET-11 in `.claude/skills/knowledge-curation/references/metrics.md` to also cover a
   source metric overruled under MET-2 or MET-4, with this dataset as its case. C declares `rmse` with origin
   `fallback` and sets `use_case` back to pricing.

   [^3a]: **MET-2** (Must): match the data, the metric and the real task. **MET-4** (Should): a competition's
     leaderboard metric is declared, and is overruled only by MET-2 or on evidence that it is biased or wrong for the
     use case, written in the notes with its numbers.
   [^3b]: **MET-11** (Must): every metric has one origin. `stand-in`: the source's unique metric cannot be computed on
     our data and the closest computable metric replaces it. `context`: the source defines no metric, but the task
     makes one obvious. `fallback`: the source defines no metric, or none the task would use in practice, and the task
     makes none obvious; roc_auc, log_loss or rmse by problem type.
   [^3c]: Andrej, 2026-10-30, policy call 3: loss costs are compared by the Gini of the ordered Lorenz curve; the
     batch's insurance tables declare it as `context` (not yet ruled).
   [^3d]: principles.md, tension "The source's metric against a better metric for the same goal": the source's metric
     when it is a competition's or one deliberate choice that suits the decision; otherwise the fallback.

   **Andrej (2026-11-03, change):** We go with B and can change the rule. If the source metric is bad we don't want
   to use it.

   **Resolved (2026-11-03, Andrej):** B. MET-11's `context` now also covers a source metric overruled under MET-2
   or MET-4 when the task makes one metric obvious (`metrics.md`, with this dataset as its case; the matching
   tension in `principles.md` updated). The Gini stays declared from context, no longer as an exception;
   african_credit_scoring_challenge is not reopened (its fallback `roc_auc` is the obvious metric there too).

**Review panel:** ship after changes (mediator). Claim audit: 30 claims, 22 hold, 4 refuted and 2 partly refuted (fixed
in the definition; the two record claims at hand-over), 1 circular (replaced by a test that can fail), 1 untested (the
Kaggle evaluation page). Blind review: would exclude, on MAE and R^2, which cannot score this task (not taken up).
Debate: advocate and critic agree on the verdict, the leak drops, the gap (the critic conceded), the `context` label and
the narrowed use case; left to you: f533 and the six as a block or restored (issue 1), the gap or a no-gap exception
(issue 2) and the metric's origin (issue 3). The panel's numbers are from the definition as it stood before these
changes (windows of 5,800 loans, no gap).

<details><summary>Mediator</summary>

**Mediator: loan_default_prediction_imperial_college (2026-11-01)**

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (approximate fit; USE-8: fit_reason names the drops); LEAK-10 triggered and fixed:
  f527/f528 (done), the 27-column predecessor-loss family plus f278 (same short-gap signature, mediator check),
  f468/f471/f536 (own-period top tail, reproduced); f533 goes with the six already dropped as one block (issue 1);
  f615/f617 and f13 tested and kept with notes; LEAK-21 holds (not iranian_churn); SPLIT-1, 3, 9, 11, 14 hold;
  SPLIT-10 met by a one-window gap (issue 2).
Value: TP-2, a small real signal after all drops (Gini 0.175, 0.096 to 0.236, above 0 on 9 of 9; AUC 0.708);
  MET-4 overrule of MAE holds (MET-2); the origin label is open (issue 3).
Quality: CLEAN-14, f6 to categorical; f466 to float64; text fixes (EV-6, EV-7, SPLIT-13).
Weighed: size and a real lending decision +; anonymised fields (the host's "ex-ante" label wrong three times) and a
  small signal -.
For the curator: issue 1 (f533 and the six as a block, or restore all seven; a consistency check), issue 2 (the gap
  or a no-gap exception), issue 3 (the metric's origin: `context` or the fallback `rmse`).
```

The advocate and the critic agree on the verdict and on everything below except the two points the main session named
open. Both are settled by the mediator's experiments below (thread caps on every run).

**Agreed facts** (reproduced by at least two agents, or by one agent and the definition's own code)

- 105,471 loans, `loss` 0 in 90.7% (95,688), 9,783 losses of 1-100, median 5; no missing values.
- Row order is time order: entity links rise in id in 99.97% of 73,319 links (100.0% between region chunks); the data
  page and the Kaggle admin say the same. The host's full answer is "There is no after and before. These transactions
  are all completed." (topic 6871); the definition quotes only the second sentence.
- 9 windows of 5,800 rows, expanding, training 50.5%-94.5%, 541-581 losses each; no test loan has the entity's next
  row in training. 68-74% of a window's loans have an entity predecessor, 62-67% inside the same window.
- The 27-column family (the column auditor's list) carries the predecessor's loss and the signal does not fade at short gaps: f221's
  level gives it at ROC AUC 0.993 when the predecessor is 1-10 rows earlier, 0.998 beyond 1,000 rows. A loan 1-10
  loans earlier cannot have run its term, so the field was filled in after the fact (LEAK-10; LEAK-38 covers only
  untestable timing; kick precedent).
- f471, f536, f468: in their top 0.1%, among loss-free linked rows, the own period's x changed in 34/34, 27/27 and
  31/36 cases against 33.3% overall; the previous period at the base rate. Reproduced by the critic on the raw file
  with a control over 953 tails. f533 does not reproduce (0.694 own against 0.633 previous, the profile of f529).
- The six aggregates (f529-f531, f534, f535, f537) show no own-period sign in two label-free tests; restoring them moves
  the Gini by noise (+0.022, -0.010, -0.006).
- MAE: predicting 0 scores 0.803 and every honest model scores worse (z 66-77). Between models RMSE separates about as
  well as the Gini (paired z about 2 on both); the top 1% of rows hold 74-81% of the squared error. Doubling the
  predictions leaves the Gini unchanged.
- f6 is the host's "person instructing the loan": 1,079 unordered codes, equal along entity links in 24.2% of cases
  against 0.5% for random pairs.
- A chain's last row has a loss as often as its other rows (9.42% against 9.38%): the iranian_churn concern is refuted.
- One-window gap: Gini +0.006, AUC -0.001 on 4 windows; the newest 5,800 training loans are worth no more than the
  oldest 5,800 (split auditor).

**Decisive experiments run by the mediator**

1. *f615, f617, f278 at short link gaps*. ROC AUC for the predecessor's loss, by how many rows
   the predecessor is earlier:

   | Gap (rows) | Links | f615 level / change | f617 level / change | f278 level / change | f221 level (control) |
   |---|---|---|---|---|---|
   | 1-10 | 8,083 | 0.654 / 0.676 | 0.659 / 0.655 | 0.577 / 0.739 | 0.993 |
   | 11-100 | 23,153 | 0.677 / 0.702 | 0.683 / 0.681 | 0.571 / 0.723 | 0.995 |
   | 101-1,000 | 31,425 | 0.764 / 0.791 | 0.777 / 0.762 | 0.577 / 0.752 | 0.996 |
   | > 1,000 | 10,636 | 0.909 / 0.943 | 0.945 / 0.913 | 0.595 / 0.860 | 0.998 |

   f278's change keeps 0.72-0.75 at short gaps, the flat profile of the family (f274: 0.948 to 0.991): it goes with
   the 27 (LEAK-2's sweep). f615 and f617 lose most of their signal at short gaps and gain it with distance, which is
   what history that arrives over time looks like: kept, with the table in a `Potential leak, kept on purpose` note
   (their residual 0.65 at 1-10 rows is the stated risk).
2. *f13's bottom tail*. The own-period sign is real and is not
   explained by the period counter, the link gap or the maturity (f13 <= 4: 0.86-0.93 own change in every f521
   quintile, 0.82-0.97 in every gap quintile, 0.82-0.95 in every f4 quintile, against 0.29-0.38). But it is a smooth
   gradient, not a tail record: own change 1.00 / 0.94 / 0.89 / 0.76 / 0.62 / 0.52 for f13 = 2 to 7 (12 to 7,028
   rows). Over all rows f13's label-free AUC for an own-period change is 0.658, next to ordinary columns (f68 0.657,
   f596 0.650, f766 0.631, the best single column for a loss), and its value does not scale with the size of the
   change (Spearman -0.09 in its low values, against 0.59 in f536's top tail). That is a predictor of the period's
   event, as many shipped columns are, not a field written from it (EV-6). Kept, named with these numbers in the note.
3. *The final column set* (the column auditor's untuned hurdle LightGBM, one fit per
   window): the 27, f278, f468, f471, f533, f536 dropped and f6 categorical.

   | Window | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Mean |
   |---|---|---|---|---|---|---|---|---|---|---|
   | Gini, as shipped (advocate) | 0.235 | 0.273 | 0.211 | 0.293 | 0.290 | 0.183 | 0.203 | 0.198 | 0.232 | 0.235 |
   | Gini, final set | 0.236 | 0.207 | 0.163 | 0.196 | 0.202 | 0.096 | 0.167 | 0.168 | 0.145 | 0.175 |
   | AUC (loss > 0), final set | 0.731 | 0.720 | 0.721 | 0.713 | 0.706 | 0.689 | 0.700 | 0.703 | 0.694 | 0.708 |

   Measured on the current windows (no gap); a random scorer's Gini has an SD of about 0.04 (claim auditor), so the
   lowest window (0.096) is still above 0.

   TP-2 holds; the blind reviewer's "exclude" rested on MAE and R^2, which the metric section of the definition shows
   cannot score this task (the forest_fires tension row: the split and the task decide, not the size of the score).

**Changes to make now** (no decision needed; each with its rule and what it should reproduce)

1. `_clean`: drop the 27 columns of the column auditor's list and f278 (LEAK-10 Must, LEAK-2, LEAK-6; kick). Reproduces: f221 level
   AUC for the predecessor's loss 0.993 at gaps of 1-10 rows (8,083 links); f278 change 0.739.
2. `_clean`: drop f468, f471, f536 (LEAK-10 Must). Reproduces: top 0.1%, loss-free linked rows, own-period change
   31/36, 34/34, 27/27 against 33.3%.
3. `_clean`: drop f533 with f529-f531, f534, f535, f537 as one block (the CC of 2026-11-01 applied to its like case,
   CLEAN-22's like-for-like; the block or a restore is issue 1). Reproduces: f533 top tail 0.694 / 0.633, f529
   0.692 / 0.615.
4. Notes: replace the "Potential leak, kept on purpose" bullet with a LEAK-10 bullet for the dropped families (the gap
   table) and a short `Potential leak, kept on purpose:` bullet for f615/f617 (the table above), f13 (the gradient and
   its controls) and f519/f520/f523/f526 (label-free 0.613 against 0.532, drop changes nothing); revisit if the host's
   field list becomes public (LEAK-38, LEAK-32). Extend `_decisions` with the gap table.
5. Notes: "no change passes ROC AUC 0.595" becomes "for the row's own loss"; the circular "f527 = ... on 100%" becomes
   the test that can fail, the next row's f274 equals x on 97.3% of links (EV-6).
6. Text: quote the host's full answer (EV-7); `task_summary.row` and `.split` say "the order the loans were recorded,
   old to new" with "granted" marked as our reading.
7. `splits_comment`: the SPLIT-13 sentence (68-74% have an entity predecessor, 62-67% in the same window); drop "its own
   history (LEAK-34)" for the predecessor's row; the gap sentence of issue 2 without "as for lending_club".
8. Splits: `TemporalSplits(window=5000, unit="rows", n_windows=9, gap=5800)` (SPLIT-10 Should; issue 2 keeps the
   alternative). Reproduces: oldest window trains on 54,671 rows (51.8%); about 470-500 losses per window.
9. Metric: `Metric.from_context("normalized_gini", ...)` naming MAE as the original, replacing `stand_in` (MET-11 Must:
   MAE is computable); the reason gives both sides on RMSE (paired z about 2 between models; 1% of rows hold 74-81% of
   the squared error) and says the Gini ignores the level. The origin itself is issue 3.
10. `task_summary.use_case`: rank new loans by expected loss to choose which enter a portfolio, the level set by a
    separate calibration (MET-2 Must: the Gini cannot see a price level).
11. `_feature_types`: `categorical=["f6", "f776", "f777", "f778"]` plus a line in the dtype bullet (CLEAN-14); f466 to
    float64 like the other long integers (CLEAN-9).
12. `changes` and `fit_reason` name the dropped families (USE-8); every figure in the notes and the metric reason is
    re-measured on the changed definition (the hurdle's 0.236 becomes about 0.175); `dataset check` and the task
    probes re-run.
13. Record, at hand-over (no mark): remove `Data Quality Issue` (refuted, thyroid_discordant precedent); correct
    "f275 = f274^2" (true in 0.42% of rows); add the `Non-IID (Temporal)` tag.

**Issues for the curator** (ranked)

1. **P4, LEAK-10 (Must, "may include") against CLEAN-22 (Must, P7) and precedent: f533 and the six as one block, or
   restore all seven.** Problem: the CC dropped six aggregates as siblings of the golden features; two label-free tests
   clear them, and f533 shows the same profile. Effect: removing them moves no score; keeping them out removes columns
   that look ordinary on the data. Advocate: the block shares the hidden x whose members f527/f528 carry the outcome's
   period, and a label-free test of anonymised fields is indirect. Critic: same view on the block; f533 must get the
   same treatment as the six whatever is chosen. Precedent checker: online_shoppers `PageValues` and
   account_debt_south_africa's billing totals (Lennart, 2026-10-26) were kept once the data showed them behaving like
   history. Rule: P4 outranks P7, so the drop is defensible, but the precedent asks for the fact that sets this case
   apart. Decision: (a) keep the block dropped, recorded as an exception with that fact; (b) restore all seven with a
   `Potential leak, kept on purpose:` note.
2. **P4, SPLIT-10 (Should): a one-window gap, or no gap as an exception.** Problem: a refit model would not yet know the
   newest loans' outcomes; the true delay (a loan's term plus workout) cannot be sized without dates. Effect: none
   measured (Gini +0.006, AUC -0.001; the newest training loans are worth no more than the oldest). Advocate: the gap is
   the rule's default, fits SPLIT-14 (51.8%) and removes a departure; the remedy ladder ranks a definition fix above a
   note. Critic: conceded the gap, either is acceptable. Mediator: the rules lean to the gap, since a departure from a
   Should needs a fact that sets the case apart, and the only candidate (a term long against the file's unknown span)
   is inferred; but one window is not the delay either, so the size is a judgment. lending_club's fact (a gap breaks
   the floor) does not hold here and may not be cited. Decision: (a) the gap (implemented); (b) no gap, recorded as an
   exception with the inferred fact and the measured null effect.
3. **P6, MET-11 (Must): which origin for the Gini.** Problem: `stand_in` is wrong (MAE is computable, and the Gini is
   no close version of it). `context` is defined for a source with no metric; `fallback` covers a source metric the
   task would not use, which is this case, and gives `rmse`. Neither label fits the overruled-competition-metric case
   with an obvious task metric. Advocate and critic: `context`, as the batch's insurance Gini tables (frempl,
   australian_vehicle, spanish_motor; AI, not yet ruled), following your policy call 3 of 2026-10-30 (the loss-cost
   industry compares models by the Gini). For `rmse`: the tension row (an overruled competition metric goes to the
   fallback) and african_credit_scoring_challenge (Lennart, 2026-10-26); RMSE separates models about as well as the
   Gini (z about 2) and scores the level. Against `rmse`: 1% of rows drive it and it ranks models near the mean
   (R^2 about 0.01). Decision: (a) `context` (implemented), possibly with an amendment of MET-11's `context` to cover
   an overruled source metric; (b) the fallback `rmse`.

**Disputed points and how they were settled**

| Point | Advocate | Critic | Rule and rank | Settled |
|---|---|---|---|---|
| 27-column family | drop | drop | LEAK-10 Must (P4) over LEAK-34/LEAK-38 (Should): timing tested | agreed; change 1 |
| f615, f617, f278 | measure first | measure first | LEAK-2 sweep, EV-6 | experiment 1: f278 drop, f615/f617 keep with note |
| f468, f471, f536 | drop | drop (reproduced) | LEAK-10 Must | agreed; change 2 |
| f533 | drop as a leak | not a leak; with the six | LEAK-10 against CLEAN-22, like cases alike | f533 joins the six (change 3); block or restore is issue 1 |
| f13 | (not raised) | test before a drop | LEAK-10 against EV-6 | experiment 2: keep with note |
| Gap | add 5,800 | exception, then conceded | SPLIT-10 Should; SPLIT-14 not binding | issue 2 (gap implemented) |
| Metric label | `context` | `context` | MET-11 Must | `stand_in` goes (change 9); origin is issue 3 |
| `use_case` | narrow | narrow | MET-2 Must | change 10 |
| Blind reviewer's exclude | rests on MAE/R^2 | not taken up | TP-2, forest_fires | rejected; experiment 3 |

None of these is a conflict that rescues an independent failure: each leak drop meets its Must on its own; TP-2 is
checked on the final set, not argued from the use case.

**Consistency with precedent**

- Follows: kick (`WheelType`, LEAK-38 to LEAK-10 once timing is tested) for the family and f278; the host's removal of
  ex-post aggregates and f527/f528 for the own-period tails; iranian_churn set apart by the measured chain fact;
  rdkit_Ipc_log10, CLEAN-5 and home_credit's `-1` for cleaning; forest_fires for TP-2; thyroid_discordant for the
  marker.
- Departs, as issues: the six plus f533 against `PageValues` and account_debt (issue 1); no gap would depart from
  SPLIT-10 without lending_club's fact, so the gap is implemented (issue 2); `context` departs from the letter of
  MET-11 and from african_credit's fallback (issue 3). Recording the gap call under lending_club's reason is avoided,
  so no third exception of that reason arises.
- No drift in Andrej's calls on this record (two CCs agree).

</details>

<details><summary>Claim audit</summary>

**Claim auditor: loan_default_prediction_imperial_college (2026-11-01)**

**Verdict: ship after two text fixes and one curator call.** Every number the definition gives about the target, the cleaning, the windows, the entity chains and the golden-feature drop reproduces. Three things do not hold:
- The note on the kept "history" family is too narrow. Twelve more shipped columns reveal the previous loan's loss, and the timing evidence goes against the reading the keep rests on (LEAK-10/LEAK-38).
- The metric's origin label `stand_in` does not fit MET-11.
- The reason given for not using RMSE overstates its weakness (MET-10, EV-9).

None of these changes a score much. Dropping the whole family costs nothing measurable.

**How I tested.** The frame and splits come from `dataset_io` (105,471 x 671, 9 temporal splits). Entity links are rebuilt as in `_period_links` (73,319 links). Models are untuned LightGBM: a hurdle P(loss>0) x E[loss | loss], plus an L2 regressor, one fit per split on windows 0, 4 and 8. Metrics come from `data_foundry.v2.metrics`, and the paired contrasts are bootstrapped over test rows. I did not query the Kaggle API, so that no credential went to an outside service. The evaluation page needs JavaScript and would not load.

**Claims table**

| Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 95,688 zeros (90.7%), 9,783 losses 1-100, whole numbers, median 5, no missing | curation_comments, task_summary.predicted | count on shipped `loss` | holds | 95,688 / 9,783, median 5, max 100, 0 missing | P5 |
| Prediction point at the grant; features are ex-ante ("ex-ante information", topic 6862) | curation_comments, task_summary | quote in saved topic; leak scans | quote holds; the claim that the features are known at the grant is partly refuted (row 1 of the ranking below) | quote found in topic_6862 | LEAK-1, LEAK-10 |
| Loss definition, full recovery coded 0, "These transactions are all completed" | curation_comments | grep of saved topics 6862, 6871 | holds, quoted selectively | the same 2014-01-19 post opens "There is no after and before. These transactions are all completed." The definition drops the first sentence, which goes against its own time-order reading (the Kaggle admin later said the split is by time) | EV-7, PROV |
| `id` is the time order; the id rises along 99.97% of links (22 fall back) | curation_comments, splits_comment | recount | holds | 0.99970, 22 falls; data-page quote and admin quote in topic_6871 | SPLIT-1 |
| 19 text columns cast to float64 without loss | curation_comments | round-trip per column | holds | 0 rows not round-tripped in all 19 | CLEAN |
| f391 / f627 above float32 in 53,049 / 58,304 rows, all positive | curation_comments | count | holds | 53,049 / 58,304; minima 8.6e27 / 9.3e27 | CLEAN-2 |
| 11 constant, 81 copies, 669 features + `time_index` | curation_comments, `_clean` assert | recount | holds | 11 / 81 / 669 | CLEAN-5 |
| -1 in nine columns is a real value, not a missing code | curation_comments, warning `dataset_missing_value_sentinel` | next values above -1; own missing values | holds | the next values are -0.99, -0.98, -0.97 (f763: -0.991); each column has 1.7-8.5% missing of its own; loss rate at -1 is 5.3-14.4% vs 8.6-9.7% otherwise (informative, not missing) | CLEAN |
| No two rows share a feature vector | curation_comments | duplicate check on shipped | holds | 0 | SPLIT, P5 |
| 9 windows of 5,800, train 50.5%-94.5%, all earlier rows, 541-581 losses each | splits_comment | per split | holds | train shares 0.5051 to 0.945; losses 541-581; train all earlier in 9/9 | SPLIT-11, SPLIT-14 |
| Newest window's mean loss 0.829, no lower than the others (0.753-0.840), so no open losses | curation_comments | per window | holds (weak test) | 0.829 vs 0.753-0.840 | SPLIT-10 |
| f527 = (own x + earlier f527) / 2 on 100% of links | curation_comments, `_decisions` | read the code | circular: true by construction | x is defined as 2*f527 - (f274 - f271), and the link matches f274 - f271 to the earlier f527, so the identity cannot fail. The test that could fail: the next row's f274 equals that x on **97.3%** of links | EV-6 |
| x changes for 99.99% of loss rows vs 33.1% of others | curation_comments | recount on links | holds | loss-free share 0.331 (the record's older 99.8% / 38.3% is superseded) | LEAK-10 |
| f528 follows the own period (Spearman 0.75 own vs 0.44 previous) | curation_comments | Spearman on link changes | holds; f527's own-period lean is weak | f528 0.751 / 0.440. f527 0.587 / 0.507, and on loss-free links 0.472 own vs 0.562 previous, so f527's drop rests on its change AUC 0.931 and on f528, not on the lean | LEAK-10 |
| The six siblings (f529-f531, f534, f535, f537) show no own-period signal (Spearman 0.02-0.21 own, 0.01-0.23 previous) | curation_comments, builder issue 2 | same test | holds | own 0.021-0.207, previous 0.012-0.233, the same as ordinary shipped columns (f575 0.191 / 0.232) | LEAK-10 vs CLEAN-22 |
| No shipped column's change from the earlier row passes ROC AUC 0.595 | curation_comments, `_decisions` | change AUC; own-lean scan of all shipped columns | holds | the most own-leaning shipped columns, f519/f520/f523/f526 (Spearman -0.22 own vs -0.09 previous), have change AUC 0.594 and level AUC 0.53-0.54 | LEAK-10 |
| No pairwise difference passes 0.647; no hidden combination leaks | curation_comments | +, -, *, / scan as in the forum: 223,446 ratio and product pairs on 15,000 rows, and ratio/relative difference within the 80-column f274 family | holds | no ratio or product reaches 0.70, best ratio f68/f766 0.664 (outside the claim, which is about differences); best pair within the family 0.588; winner's `hasnull` AUC 0.474 | LEAK-10 |
| f274, f271, f275, f277 are the entity's history (lagged, Spearman 0.58-0.78), kept on the reading that a previous loss was known at the next grant | curation_comments (Potential leak note) | (a) which shipped columns reveal the previous loan's loss; (b) the same signal at short id gaps | **refuted in scope, and the reading is doubtful** | (a) 12 more shipped columns separate the previous row's loss at AUC >= 0.73 while the row's own loss stays at 0.50-0.56: f222 0.996, f221 0.996, f212 0.992, f272 0.973, f252 0.942, f251 0.941, f261 0.890, f262 0.889, f211 0.887, f617 0.747, f615 0.733. (b) When the next loan comes 1-10 rows later (8,083 links, 11%), x has moved in 99.4% of cases after a previous loss vs 41.4% after none, and the next row's \|f271\| separates the previous loss at AUC 0.911 | LEAK-10, LEAK-38, EV-6 |
| 12.0% losses after a loss vs 9.0% | curation_comments | recount | holds | 0.1204 (n 6,877) vs 0.0899 | LEAK-34 |
| 19,453 chains (32,152 with singles), 88% of rows; 70.3% of loss rows have a later row; last row 9.42% vs 9.38% | curation_comments | connected components on links | holds | 19,453 / 32,152 / 0.8796; 0.703; 0.0942 vs 0.0938 | LEAK-21 (the iranian_churn concern refuted) |
| No test loan has the entity's next row in training | splits_comment | follows from expanding windows and ids rising on 99.97% of links | holds | 22 backward links in all, below 0.03% | SPLIT-9 |
| The competition's metric is MAE | metric `original`, curation_comments | evaluation page (JS-only, not readable); web search | cannot verify the page; circumstantial support | a 15th-place private score of 0.456 (dmcgarry repo), against predict-0 at 0.80, fits MAE in loss points | MET-1, EV-7 |
| MAE loses its meaning without the golden features | metric reason | per window: constant 0 vs hurdle vs L2 | holds | MAE: zeros 0.829 / 0.838 / 0.791, hurdle 1.475 / 1.507 / 1.423 (zeros better, z 66-77) | MET-2, MET-4 |
| RMSE "resolves little" | metric reason | paired bootstrap contrasts, R^2 vs Gini | **partly refuted** | model vs model, hurdle - L2: R^2 z 0.43 / 1.97 / 2.51, Gini z 0.34 / 2.15 / 1.86, about the same resolution. Model vs constant: R^2 z 2.1-2.9, Gini z 5.4-7.5. The top 1% of rows hold 74-81% of the squared error; Gini also drops 0.240 to 0.194 when the 20 largest losses go | MET-10, EV-9 |
| Gini 0 for any constant, 1 when perfect, computable on every fold | metric definition | dummy scores through the scorer on 9 folds | holds | zeros and train mean 0.000 on 9/9; perfect 1.000; random -0.069 to +0.058 (noise SD about 0.04); time_index -0.071 to +0.044 | MET-2 |
| Origin `stand_in` (the original "cannot be computed") | `Metric.stand_in` | MET-11 definition | **refuted** | MAE is computable on our data; the Gini is no "closest computable" version of MAE (it ignores the level MAE scores). What applies is MET-4's overrule clause, and the precedent (african_credit_scoring_challenge) records an overrule as a fallback or a curator call | MET-11, MET-4 |
| Metric name, implementation, scale | metric | library and tests | holds | `normalized_gini` in `src/data_foundry/v2/metrics.py`, tested against the Kaggle code and by hand; target identity, scored raw | MET-3, MET-12, MET-13 |
| Kept family carries no score gain | (implied by keeping it) | ablation of 16 columns (f274-f277, f271 and the 11 above) | holds | AUC without vs with: 0.738 / 0.746, 0.720 / 0.721, 0.718 / 0.714; Gini 0.273 / 0.240, 0.281 / 0.289, 0.220 / 0.207 (one fit each; Gini noise about 0.03) | LEAK-38 |
| Record: f275 = f274^2 | record, Assessment 2026-11-01 | exact and relative check | **refuted** | equal in 0.42% of rows (Spearman 0.967) | EV-6 |
| Record: `Data Quality Issue` marker (rows end at their default) | record front matter | chain last-row loss rate | refuted (the builder already says so) | 9.42% vs 9.38% | P5 |

**Refuted and untested claims, ranked (validity first, Must first)**

1. **LEAK-10 / LEAK-38 (Must, P4): the kept history family is wider than written, and its timing reading is doubtful.** The note names f274, f271, f275 and f277. Eleven more shipped columns (f222, f221, f212, f272, f252, f251, f261, f262, f211, f617, f615) give the previous loan's loss away at AUC 0.73-0.996, and f222, f221 and f212 do it almost exactly. The keep assumes the previous loss was known when the next loan was granted. But when the next loan comes within 1-10 rows, it already shows the earlier loss (x moved 99.4% vs 41.4%; \|f271\| AUC 0.911). A loss settled and booked within a handful of loan grants is implausible. The test is circumstantial because the file has no dates, so per EV-6 this is "maybe a leak". The settling test would be loan dates, which the source does not give. LEAK-38's amendment says a conditional test of the mechanism moves a field to LEAK-10, and this is such a test (conditioned on time proximity). *What it changes:* realism, not scores. The entity's next row is never on the training side, and dropping all 16 columns moves AUC by -0.008 to +0.003. *Mildest remedy:* drop the 16 columns, which costs nothing measurable. The alternative is to keep them and widen the `Potential leak` note to all 16 columns with the short-gap numbers. The split-auditor's gap question then follows the same decision.
2. **MET-11 (Must, P6): wrong origin label.** `stand_in` is for a source metric that cannot be computed. MAE can be; it is overruled under MET-4 on measured evidence. *Mildest remedy:* keep `normalized_gini` as a curator overrule, worded as a MET-4 overrule with these numbers, or declare the fallback `rmse`. Either way, reword the reason.
3. **MET-10 / EV-9 (Should, P6): "RMSE resolves little" is overstated.** Between models, RMSE separates as well as the Gini (paired z about 2 on both). It separates them from the constant less well, and it is driven by 1% of the rows. It also scores the loss level, which the use case's pricing needs, and the Gini ignores it. *Remedy:* state both sides in the reason and let the curator choose (open question already in REVIEW.md).
4. **EV-6 (Should): circular evidence in the notes.** "f527 = (own x + earlier f527) / 2 on 100%" is an identity. *Remedy:* cite the test that could fail: the next row's f274 equals x on 97.3% of links. Also say that f527's drop rests on its change AUC 0.931 and on f528, since f527's Spearman leans to the previous period on loss-free links.
5. **EV-7 / PROV (Should): selective quote.** "These transactions are all completed" leaves out the same post's "There is no after and before". *Remedy:* quote both sentences and say that the admin's "The train/test split is done by time" and the data page's "listed in order from old to new" settle the order.
6. **Record only:** "f275 = f274^2" is wrong (0.42%). The `Data Quality Issue` marker no longer fits. *Remedy:* correct the record at the next record edit.
7. **Untested:** the text of the Kaggle evaluation page (JS-only; the API needs a credential, so it was skipped). MAE is supported only circumstantially, by leaderboard scores around 0.45 against 0.80 for predicting 0. Whether f527/f528 come from a period after the grant is inferred from the mechanism, because the fields are anonymised.

Sources for the metric check: [dmcgarry/Default_Loan_Prediction](https://github.com/dmcgarry/Default_Loan_Prediction), [vijayendra-g/Kaggle-Loan-Default-Prediction](https://github.com/vijayendra-g/Kaggle-Loan-Default-Prediction).

</details>

<details><summary>Column audit</summary>

**Column auditor: loan_default_prediction_imperial_college (2026-11-01)**

**Verdict: not ready as shipped. One leak must go, and it is wider than the panel has said so far.** The kept "f274 family" is hindsight (LEAK-10). It is not 4 columns but 27, and one of them, f221, gives the entity's previous loan's loss away from its level alone, at ROC AUC 0.996. That strength does not weaken when the previous loan was granted only 1-10 loans earlier. A second, smaller set is a probable leak: four shipped columns (f468, f471, f533, f536) whose top tail records the loan's own period, the same mechanism as the dropped golden features. These four show that mechanism more clearly than the six aggregates the curator already dropped. f6 is a code, not a quantity. The other 626 columns are fine as shipped, within the `Anonymized` tag's known risk (LEAK-32).

**How I measured.** I loaded the cleaned frame and the 9 splits with `dataset_io.from_definition`: 105,471 rows, `time_index`, `loss` and 669 features. That is identical to what the split auditor checked against the builder's export. Codebook: the host's field notes in topic 6978. Only f2, f4, f5, f6 and f776-f778 are named; every other field is anonymised. For timing I used the definition's own entity links (`_period_links`: 73,319 links, 19,453 chains), and the hidden value x is rebuilt as the definition's `_decisions` does. I ran three tests per column:
- label-free: among linked loans *without* a loss, does the column's change mark a change of x in the row's own period, or in the previous one?
- which loan's loss the column's change or level carries: the row's own, or the predecessor's;
- a tail scan: the top and bottom 0.1% and 0.5%, their loss rate, and the same label-free own-period test inside the tail.

Model checks use the builder's untuned LightGBM hurdle model (400 trees), scored with the shipped normalized Gini and the ROC AUC for a loss. Each split gets one fit. The Gini moves by about ±0.03 between near-identical fits, so read the AUC for small effects.

**Column table** (grouped. Every column of a group shares the verdict. The 670 rows one by one are in the auditor's column table.)

| Column(s) | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `time_index` | the source id, in time order (topic 6978: "listed in order from old to new") | yes | int64, renamed from `id` | fine | CLEAN-3 |
| `loss` (target) | loss per 100 of notional, 0 for no default or full recovery | (target) | int64, 0-100, no missing | fine | - |
| f776, f777, f778 | collateral full/partial, gradual/bullet repayment, region (topic 6978) | yes, loan terms | categorical, 0/1, 0/1 and codes | fine | CLEAN-14 |
| f2, f4, f5 | size cluster, maturity ranges, ease-of-transaction ranking ("can be seen as categorical") | yes | int64, numeric (ordered ranges) | fine, a weighing call (ordered, so numeric is defensible) | CLEAN-14 |
| f6 | "person instructing the loan has the historical relationship" (topic 6978) | yes | int64, numeric: 1,079 arbitrary codes, 0-88,565 | **cleaning problem**: a code, so categorical | CLEAN-14, CLEAN-3 |
| f521 | the entity's period counter (+1 along every link) | yes | int64 | fine (an entity's history) | LEAK-34 |
| **f211, f212, f214-f217, f221, f222, f224, f251, f252, f254, f261, f262, f264, f271-f275, f277, f538, f539, f568, f569, f577, f578** (27) | anonymised; their change (and for f211, f212, f221, f222, f251, f252, f261, f262, f271, f272 also their level) follows the previous period's x and the predecessor's outcome | **no**: the predecessor's loss, recorded with hindsight (see problem 1) | float64, numeric | **leak, drop** | LEAK-10, LEAK-2 (LEAK-38 no longer covers it) |
| f615, f617, f278 | anonymised; change carries the predecessor's loss at AUC 0.74-0.77 (f615 and f617 also at 0.73-0.75 from their level) | doubtful | float64 | question: the edge of the sweep | LEAK-2 |
| **f468, f471, f533, f536** | anonymised; the +65 twins of each other (f468/f533, f471/f536). They sit in the block of the host-removed f473/f474 and in the block of the dropped f527-f537 | **no in the top tail**: the own period's x (see problem 2) | float64 | **probable leak, drop** (capping is the alternative) | LEAK-10, LEAK-2, LEAK-7 |
| f519, f520, f523, f526 | anonymised; monotone in f521 (Spearman 0.91-0.99) | maybe: change leans to the own period (label-free AUC 0.613 vs 0.532 within f521 deciles) | float64 | question, weak | LEAK-10, EV-6 |
| f13 | anonymised; integer 2-40 | maybe: the bottom tail marks an own-period change of x (94.8% vs 33.1% base; loss rate 18.6% in 177 rows) | int64 | question, weak | LEAK-10, EV-6 |
| f137, f138, f206, f207, f276, f337, f338, f390, f419, f420, f466, f469, f472, f626, f695, f698 | anonymised; very large integers (all but f337 and f466 arrive as text) | undetermined | float64 cast, every distinct value exact; f337 int64 and f466 uint64 as read | fine (nit: f466 could be float64 like the rest) | CLEAN-9 |
| f391_log10, f627_log10 | anonymised; values up to 7e41 and 9e41 | undetermined | log10 of all-positive values (beyond float32); precedent `rdkit_Ipc_log10` | fine | CLEAN-2 |
| f72, f586, f587, f588, f648, f649, f650, f651, f763 | anonymised; continuous from -0.99, with -1 in 7-12% of rows and missing values of their own | undetermined | -1 kept as a value (a -100% change) | fine: not a proxy missing code | CLEAN-10 |
| the other 581 anonymised columns (f1, f3, f7, ... f775) | unknown (host: borrower, history, loan, track record of people involved, aggregated scores or clusters) | undetermined. No own-period sign: change AUC for the own loss ≤ 0.595, tails clean | numeric as shipped; 523 columns keep missing values (≤ 17.9%) | fine | LEAK-32, LEAK-38, CLEAN-14 |
| dropped: f527, f528, f529-f531, f534, f535, f537; 11 constants; 81 copies | | f527/f528 no; the six untested | | correct (CLEAN-5 counts reproduced by the definition's assert) | LEAK-10, CLEAN-5 |

**Problems, ranked by `principles.md`**

1. **P4, LEAK-10 (Must), with LEAK-2: the predecessor-loss family is hindsight, and it has 27 columns, not 4.**
   - The definition keeps f271, f274, f275 and f277 under LEAK-34/LEAK-38, "on the reading that a loss was known when the next loan was granted". The split and domain reports showed that f274's change still carries the predecessor's loss at short gaps. I tested the whole family with the experiment that decides it: if the lender knew a loss when it granted the next loan, the signal should weaken when the predecessor was granted only a few loans earlier, because its loss had not yet happened. It does not weaken at all:

     | Link gap (rows) | Links | f221 level | f222 level | f212 level | f538 change | f274 change |
     |---|---|---|---|---|---|---|
     | 1-10 | 8,083 | 0.993 | 0.994 | 0.987 | 0.992 | 0.948 |
     | 11-100 | 23,153 | 0.995 | 0.995 | 0.990 | 0.995 | 0.971 |
     | 101-1,000 | 31,425 | 0.996 | 0.997 | 0.993 | 0.996 | 0.980 |
     | > 1,000 | 10,636 | 0.998 | 0.998 | 0.995 | 0.998 | 0.991 |

     (ROC AUC for the predecessor's loss. f221's median is 0.51 after a predecessor loss and 0.01 after none.) Loans 1-10 rows apart lie inside one ~52-loan region chunk (split auditor), and the host says terms vary "by a factor from 1 to 3". So the predecessor's outcome was written into the successor's row after the fact. This holds whichever order the file uses: if the order is completion rather than grant (split auditor, problem 2), the successor was still granted before its predecessor completed in most cases.
   - Why 27 columns: the sweep LEAK-2 asks for. These are the columns whose change carries the predecessor's loss at AUC 0.81-0.996, against ≤ 0.67 for every other column. The family includes f538 and f539, the +65 twins of f473 and f474, which the host removed as "ex-post" in topic 6962. That is the same twin relation as f462/f463 to the golden f527/f528. LEAK-38 covers only "fields whose timing cannot be tested". This timing is tested, so LEAK-10 applies, as it did for kick's `WheelType`.
   - The definition's text understates the family. It says that on the shipped columns no change passes AUC 0.595. That holds for the row's own loss, but f221 gives a *test* loan's predecessor's loss from its level alone, and 62-67% of each window's predecessors are in the same test window (split auditor).
   - Cost of the drop (9 windows): the AUC falls on 9 of 9 windows (mean -0.0026), and the Gini falls on 8 of 9 (mean -0.032, range -0.070 to +0.007). Dropping only the 4 named columns cost the domain practitioner -0.002. So the gain sits in the other 23 columns, above all in f221 and f222. LEAK-6: a confirmed leak goes even when small.
   - Mildest remedy: drop the 27 columns in `_clean` (LEAK-10). Measure f615, f617 and f278 at the sweep's edge before deciding on them. Then rewrite the "Potential leak, kept on purpose" bullet as a dropped-for-LEAK-10 bullet with the gap table, and adjust the `splits_comment` sentence "its own history (LEAK-34)". If the f274 family goes, the split auditor's gap conclusion follows: no gap, recorded as an exception. A lag cannot repair these columns, because x itself is written after the fact.

2. **P4, LEAK-10 (Must when confirmed) with LEAK-2: f468, f471, f533 and f536 record the own period in their top tail.**
   - Label-free evidence: among linked loans *without* a loss in the top 0.1%, the own period's x changed for 34 of 34 (f471), 27 of 27 (f536) and 31 of 36 (f468), against 33.1% overall. The previous period's x changed at the base rate (35-41%). That is the signature that convicted f527 and f528.
   - With the label: the top 0.1% (105 rows) has loss rates of 59.0% (f471), 58.1% (f468), 35.8% (f536) and 28.3% (f533), against 9.3% overall. Inside the top 0.5% of f471, the value rises with the own period's ratio of x (Spearman 0.39).
   - The six aggregates dropped by the curator's call (f529-f531, f534, f535, f537) show *no* such tail: own-period change 60-69% against previous-period change 53-62%, and loss rates of 13-15%. So these four have the stronger case, and keeping them while dropping the six is inconsistent.
   - Cost: dropping the four costs AUC on 9 of 9 windows (mean -0.0097) and Gini on 9 of 9 (mean -0.043). Capping them at the training side's 99.5th percentile costs AUC -0.003, -0.002 and +0.000 on windows 0, 4 and 8. So the tail is where the own-period sign sits, while the body carries a signal with no measured own-period lean (change Spearman with the own period's x 0.01-0.10).
   - Remedy: drop them (LEAK-10, the safe fix and consistent with the six). LEAK-7's smaller fix, blanking values above a fixed cut, keeps the body. But the cut would come from all rows, and the body's timing is just as untested as the six's. Curator's call. Record the numbers either way.

3. **P4, question (weak), LEAK-10 against EV-6: f519, f520, f523, f526 and f13.**
   - The change of f519, f520, f523 and f526 leans to the own period, label-free (0.613 against 0.532 within deciles of the period counter). But dropping them changes nothing: Gini +0.0003 and AUC +0.0002 on 3 windows.
   - f13's bottom tail marks an own-period change of x (94.8%), with a loss rate of 18.6%, but its size does not follow the ratio of x.
   - A longer tail of weaker leans follows (f596, f598, f68, f67, f664, f614: lean +0.26 to +0.36, loss rates 11-18%). With anonymised fields this is LEAK-32's known risk.
   - Remedy: keep, with a sentence in the leak bullet naming them and the numbers. Dropping them would be free, if the curator prefers that after problem 2.

4. **P7, CLEAN-14 (Should): f6 ships numeric, but by meaning and on the data it is a code.**
   - The host: "f6 : person instructing the loan has the historical relationship". The values are 1,079 arbitrary integers (0-88,565; only 10.6% are multiples of 10). The 15 largest codes span 99.6-100% of the file.
   - Along entity links f6 is the same in 24.2% of cases, against 0.5% for random pairs and 1.3% for adjacent rows. That fits a person attached to an entity, and does not fit a measurement.
   - The raw number's AUC is 0.514 and an out-of-fold target encoding's is 0.534. Loss rates across the 233 codes with 100 or more loans run from 2.1% to 16.6%, with no order in the code (Spearman -0.12).
   - Remedy: `categorical=["f6", "f776", "f777", "f778"]` plus one line in the dtype bullet. Untuned LightGBM scores slightly worse with it categorical (AUC -0.003, -0.003 and -0.013 on 3 windows), but encoding a category is the pipeline's job (CLEAN-2), and the score does not decide the dtype.
   - It is no group-id leak: the split is temporal, and a known relationship person is history (LEAK-34).

5. **P7 nits.**
   - f466 alone ships as uint64, while the other long-integer columns are float64 (f337 int64). That is harmless, but `float64` would be consistent.
   - f2, f4 and f5 numeric: I agree (ordered ranges). It is a weighing call that the dtype bullet already explains.
   - The "-1 is no missing code" call holds on the data (continuous from -0.99, with missing values of their own).

**The builder's column claims**

| Claim | Check |
|---|---|
| f527, f528 include the own period; the other six "do not show it" | pass; the six show no own-period tail either (problem 2) |
| "On the shipped columns no change from the earlier row passes ROC AUC 0.595" | pass for the own loss. **Misleading**: f221's *level* gives the predecessor's loss at 0.996 (problem 1) |
| f274 family follows the previous period; a loss was known at the next grant | first part pass; **second part refuted** by the gap test |
| 11 constants, 81 copies, 669 features kept | pass |
| 19 long-integer columns cast without loss; 2 as log10 | pass: of the 19 text columns, 14 ship as float64, f277 too (problem 1), f391/f627 as log10, f534/f537 dropped with the aggregates; f337 (int64) and f466 (uint64) are read as numbers already |
| -1 in nine columns is no missing code | pass |
| f776-f778 categorical; f2, f4, f5 numeric; everything else as shipped | pass, except f6 (problem 4) |
| No two rows share a feature vector | not rechecked (probe log) |

</details>

<details><summary>Split audit</summary>

**Split auditor: loan_default_prediction_imperial_college (2026-11-01)**

**Verdict: right with notes.** The use case is a lender pricing each new loan when it is granted, often for an entity that has a history. That implies a temporal split, and the source's row order is a sound time axis. The 9 windows meet SPLIT-11, SPLIT-14, SPLIT-15 and SPLIT-17. SPLIT-9 holds: no training label gives a test loan's outcome away. Nothing in the split itself has to change. Two parts of the text do. First, the reason given for having no gap ("the delay cannot be sized") contradicts the definition's own reading of the kept f274 family, so the gap decision has to follow the f274 decision. Second, the time-order evidence quotes the host selectively. Adding a gap or leaving it out changes no score measurably.

**How I measured.** I loaded the frame and splits with `dataset_io.from_definition`. They are identical to the builder's export (values and all 9 splits). The model is an untuned LightGBM hurdle: P(loss > 0) from 300 trees, times E[loss | loss] from a 200-tree regression on log1p among the losses. Scores are the shipped normalized Gini (`data_foundry.v2.metrics`, tie-aware) and the ROC AUC of loss > 0. There is one fit per split, and the Gini moves by about ±0.03 between nearly identical training sides while the AUC moves by about ±0.003, so read the AUC for small differences. Entity links are rebuilt as in `_period_links`: 73,319 links and 19,453 chains.

**Regime: declared temporal; the use case implies temporal (holds; SPLIT-1, SPLIT-3, SPLIT-6, USE-10)**

- The row is a loan at origination, and the actor is a lender or investor. The host describes the features as "ex-ante information ... on his history". 68-74% of each test window's loans have an earlier row of the same entity, so this is a known-entity task. A temporal split is right and a cold-start grouped split is not the use case.
- The rows of a chain are different loans, not snapshots of one loan. Along the links, the maturity range (f4) changes in 85.6% of cases (94.3% between random pairs), collateral (f776) in 38.5% and region (f778) in 62.6%. This supports the definition's note against an iranian_churn reading.
- Alternatives, scored with the same model:

| Split | Normalized Gini | ROC AUC (loss > 0) |
|---|---|---|
| Shipped temporal, windows 0 / 1 / 2 / 3 / 4 / 8 | 0.276 / 0.310 / 0.186 / 0.254 / 0.254 / 0.222 (mean 0.250) | 0.742 / 0.728 / 0.739 / 0.737 / 0.716 / 0.714 (mean 0.729) |
| Random 3-fold | 0.242 / 0.230 / 0.228 (mean 0.233) | 0.721 / 0.717 / 0.723 |
| 3-fold grouped by entity chain | 0.211 / 0.222 / 0.227 (mean 0.220) | 0.715 / 0.723 / 0.717 |

  The temporal split is neither optimistic nor pessimistic against the alternatives. Under a random split, 46.5% of test loans have the entity's next row in training, yet a tree model gains nothing from it. The use case decides the split, not the gap between these scores (SPLIT-4).
- Hidden groups: no hits; near copies 0.0%; no composite key.

**Temporal checks**

- Time column: the id. Entity links rise in id in 100.0% of 50,613 links between chunks and in 99.9% of 22,706 links inside a chunk. A random order would give 50%, so the order matches each entity's sequence (SPLIT-22). No feature tracks the id: the largest |Spearman| is 0.102 (f593), and the 99th percentile over 669 columns is 0.061. That fits the data page's "de-trended".
- New fact: the file is built of chunks of about 52 loans from one region. f778 has 2,159 runs against 103,060-103,189 after random permutations. Run lengths have a median of 52 (10-90%: 12-71; max 139) and do not depend on the region's size (correlation -0.17; a region's row count against its number of runs: 0.97). Each window cutoff splits at most one chunk, which is harmless.
- Windows: 9 x 5,800 rows, newest first, expanding. Training sides run from 53,271 rows (50.5%) to 99,671 (94.5%), and the windows hold 541-581 losses each. These meet SPLIT-11, SPLIT-14, SPLIT-17 and the 3 x 3 of `recommended_dimensions` (SPLIT-15).
- Gap against the label delay: no gap, and no measured effect. The test drops the newest 5,800 training loans (a gap of one window), with a control of the same size that drops the oldest 5,800 instead:

| Window | No gap (Gini / AUC) | Gap 5,800 rows | Control: oldest 5,800 dropped | alfa_battle filter |
|---|---|---|---|---|
| 0 | 0.276 / 0.742 | 0.266 / 0.742 | 0.241 / 0.740 | 0.291 / 0.740 (1,350 rows dropped) |
| 1 | 0.310 / 0.728 | 0.296 / 0.725 | 0.282 / 0.723 | 0.267 / 0.726 (1,618 rows dropped) |
| 2 | 0.186 / 0.739 | 0.196 / 0.739 | | |
| 3 | 0.254 / 0.737 | 0.290 / 0.738 | | |

  With the gap, the Gini mean is +0.006 and the AUC mean -0.001. The newest 5,800 training loans are worth no more than the oldest 5,800: the control scores below the gapped model in 2 of 2 windows. So recent labels a refit model could not have known give no measurable advantage. The release holds no partly matured labels ("All the transactions in the database are terminated", topic 6978), and the newest window's mean loss (0.829) sits inside the others' range (0.753-0.840). This also answers the first reading of the task probes' `drift_baseline` flag (late labels trained on without a gap): that reading does not hold.
- SPLIT-9 holds: no shortcut through training labels. The alfa_battle filter drops the training rows of chains that reach into the window, and it changes the AUC by -0.002 on both windows tested. The carry-forward of a loss along links is weak: 12.0% after a loss against 9.0% after none.
- History and season: training is expanding from row 0, and the source names no break. The loan mix moves strongly along the file while the loss share stays at 9.3-10.0% in every window. The test windows cover both the atypical middle stretch and the normal mix, and the newest windows are not atypical (SPLIT-20):

| Rows | Loss share | f777 (bullet) share | f4 median | f5 median |
|---|---|---|---|---|
| 0-53,270 (training only) | 8.9% | 0.29 | 2,200 | 4 |
| windows 8 / 7 / 6 | 10.0 / 9.3 / 9.4% | 0.46 / 0.66 / 0.59 | 2,900 / 3,600 / 3,600 | 16 / 7 / 4 |
| windows 5 / 4 / 3 | 9.4 / 9.4 / 9.5% | 0.42 / 0.34 / 0.24 | 2,600 / 2,200 / 2,000 | 4 |
| windows 2 / 1 / 0 | 9.9 / 9.9 / 9.9% | 0.17 / 0.19 / 0.16 | 1,800 | 4 |

**Problems, ranked by `principles.md`**

1. **P4, LEAK-34 (Must; narrows LEAK-10) against SPLIT-10 (Should): the reason for having no gap contradicts the reading that keeps the f274 family.**
   - Evidence: in the successor's row, f274 equals x of the predecessor's period on 97.3% of the 73,319 links. It records whether the predecessor had a loss: x moved after 99.4% of predecessor losses against 41.4% of the other predecessors, ROC AUC 0.948. That holds even when the successor is only 1-10 rows later (8,083 links, 11.0%) and within one ~52-row region chunk (22,706 links, 31.0%, AUC 0.962). The claim auditor's run shows these predecessors have ordinary maturities: f4 median 2,200, the same as the whole file. Link gaps have a median of 165 rows; 90% are within 1,411 rows and 99% within 5,907. In every test window, 6.9-8.7% of loans have their predecessor at most 10 rows earlier, and 23-26% at most 50 rows earlier.
   - Under the definition's reading for keeping f274 ("a loss was known when the next loan was granted"), each loss is known within its link gap. The delay can then be sized in rows (99% within 5,907), and "without dates the delay cannot be sized" is wrong.
   - If instead a loss settles only after a term the host puts at "a factor from 1 to 3", a term far longer than 165 rows, then f274 shows the predecessor's outcome before it existed. The training rows' labels then reach the test rows through a feature, and no gap can fix that (a LEAK-10 question for the column auditor).
   - The cited lending_club precedent rests on a different fact. There, a gap of the known delay broke SPLIT-14's floor. Here a one-window gap fits the floor: `TemporalSplits(window=5000, unit="rows", n_windows=9, gap=5800)` trains the oldest window on 54,671 rows (51.8%), with about 470-500 losses per window.
   - Mildest remedy: make the gap follow the f274 decision.
     - If f274 stays (LEAK-34), add the 5,800-row gap. It meets SPLIT-10 at no measured cost.
     - If f274 goes (LEAK-10), keep no gap, recorded as the lending_club exception: the delay is long against the file and breaks the floor.
   - Either way, `splits_comment` should state the measurement: with the gap the Gini is +0.006 and the AUC -0.001 on 4 windows, and the newest loans are worth no more than the oldest.
2. **P4 (the time column's meaning), EV-2 and EV-7: the time-order evidence omits the host's contrary sentence.**
   - Evidence: in topic 6871 a user asked whether all test loans were disbursed after all training loans. The host (Arnaud de Servigny, 2014-01-19) answered: "There is no after and before. These transactions are all completed." `curation_comments` quotes only the second sentence, and the time-order bullet cites the Kaggle admin and the data page from the same topic. The data settles the order: links rise in id in 100.0% of cases between chunks. Neither page says whether that is the grant order or the completion order, yet `task_summary.split` says "loans granted after the model was fitted".
   - Remedy (text only): quote the host's full answer, add the link measurement, and say "the order the loans were recorded, old to new (grant or completion not stated)". If the curator keeps "granted", say that it is our reading.
3. **P4, SPLIT-13 (Should): `splits_comment` understates how often entities recur.**
   - Evidence: 68-74% of each window's loans have an entity predecessor. Only 5.4-8.0% have it on the training side; 62-67% have it inside the same test window, and that predecessor's loss is visible in their f274 (problem 1).
   - Remedy: one sentence. The use case scores known entities (USE-10), so this is part of the task, not a fix.
4. **Notes, no action.**
   - SPLIT-12: `splits_comment` reasons from SPLIT-15 only. It should say that the only horizon the source gives is the competition's test file of later loans, whose labels were never released and which this file cannot mirror.
   - SPLIT-20: the mix drift and the region chunks (tables above) could each get a sentence in `splits_comment`.
   - The random-split sentence ("where the next row's f274 would show whether the test loan had a loss") can add that a random 3-fold split scores the same (mean Gini 0.233 against 0.250).

**Builder's split claims**

| Claim | Check |
|---|---|
| 9 x 5,800 rows, newest first, expanding, training 50.5%-94.5% | pass (`dataset_io` splits) |
| 541-581 losses per window | pass |
| 0% of test loans with the entity's next row in training; 46.5% under random 3-fold | pass; the 46.5% does not raise the random-split score |
| 5.4-8.0% with the previous row in training | pass, incomplete (62-67% in the window; problem 3) |
| id rises along 99.97% of links | pass (100.0% between chunks) |
| Nine windows match 3 x 3 | pass (`recommended_dimensions`) |
| "without dates the delay cannot be sized"; "a departure as for lending_club" | concern (problem 1) |
| Newest window's mean loss is no lower, so no losses still open | pass as a LEAK-24 check; it does not bear on SPLIT-10 |
| "loans granted after the model was fitted" | concern (problem 2) |
| No hidden groups | pass (probe log) |

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (credit-risk analyst at the lender, or a loan-portfolio investor), 2026-11-01**

**Verdict.** Fit: **approximate**, as declared. The task is one I really do: put an expected loss on each new loan when it is booked, from what the file holds. The gap is that I cannot check when any anonymised field was recorded, and I found one more kept field that was not known at the grant. Metric: **partly**. The normalized Gini scores the portfolio choice the competition named, at the unit I act on (one loan). It does not score the price level, and the `use_case` also names pricing.

**Who I am and how the decision is made today.** When a loan is booked I put a number on it: expected loss per 100 of notional, EL = PD x LGD x EAD. I price it to cover that number, and I decide whether it goes into the book or the portfolio. The inputs are what I hold at origination: the borrower's profile and track record, the loan's terms (amount, maturity, collateral, repayment profile), the region, the relationship manager or introducer, and my own internal grade. Model work comes in two steps. First, risk differentiation: I pick the model that ranks loans best, judged by the Gini or accuracy ratio (for LGD, the gAUC or CLAR that supervisors ask for). Second, risk quantification: I calibrate the level to realised averages. A validator checks each step on its own. That is my reading of EBA GL/2017/16 from memory; I did not re-read it here. The host, Arnaud de Servigny, co-wrote S&P's *Measuring and Managing Credit Risk*. He framed the competition as "constructing an optimal portfolio of loans" and told entrants "You are indeed looking to flag the worst of the population" (topic 6978).

**1. Inputs at the moment of the decision.**
- *What I have.* The host describes ex-ante borrower, history and loan fields. Six are named: collateral full or partial (f776), gradual or bullet repayment (f777), region (f778), size cluster (f2), maturity range (f4), and a ranking of ease of transaction (f5). He also mentions "the track record of people associated with the lending activity". I would hold all of these at the grant.
- *What I would not have: the f274 family (f274, f271, f275, f277), kept under LEAK-34/LEAK-38.* The keep rests on "the reading that a loss was known when the next loan was granted". The row gaps refute that reading. On the 73,319 entity links of `_period_links`, the next loan of an entity follows the previous one by a median of **165 rows** (0.16% of the file). 85.5% of links are under 1,000 rows and 99% fall within one 5,800-row window.
  - Even when loan j comes **1 to 10 rows** after loan i (8,083 links, 11%), row j's `f271` alone reveals whether loan i had a loss at ROC AUC **0.911**, and |f274_j - f274_i| at **0.957**.
  - A loan granted 1 to 10 loans earlier has not run its term, and the host says terms vary "by a factor from 1 to 3" and that losses are known when the loan terminates. So its loss could not have been known when loan j was granted. The field holds the outcome of a loan still running, recorded with hindsight. That is the same kind of field the host removed: "aggregation of historical data that incorporate some ex-post information" (topic 6962).
  - This also explains a fact in the notes: 70.3% of loss loans have a later row. The lender kept lending because it did not yet know about the loss.
  - Since the mechanism is now measured, LEAK-38 (which covers only "fields whose timing cannot be tested") no longer covers these columns. LEAK-10 and USE-3 apply.
  - Dropping them costs nothing measurable. On windows 0_0, 4_0 and 8_0 the hurdle model's Gini is 0.235 / 0.290 / 0.232 with them and 0.257 / 0.259 / 0.236 without (mean -0.002). Default AUC moves by at most 0.002. One seed per window, so differences of about 0.03 are noise.
- *What I miss that I would always have.*
  - The origination date. Only the row order is given, so I lose the vintage, the season and the credit cycle. The data page also says the features are "de-trended", which takes out the drift I would face in real use.
  - The exact amount, the price (rate or fee), the collateral value or LTV (only full/partial is given), and my own internal grade, which USE-6 counts as a legitimate input. Any of these may hide behind an anonymised column, but nothing confirms it.
- *An input that is present but coded the wrong way.* The host: "f6 : person instructing the loan has the historical relationship". f6 holds 1,079 codes; 233 have 100 or more loans, the large ones run across 99.7% of the file, and their loss rates range from 7.3% to 16.6%. It reads as the ID of the relationship person or introducer, which I would use as a category. It ships numeric (CLEAN-14). This is for the column auditor; I am moderately confident.

**2. The target.** `loss` is the realised loss per 100 of the loan's initial value, taken over all loans: 0 for no default or for full recovery (topic 6978: "Loss given default is calculated that the initial value of each loan was 100"). That is the realised EL rate, which is the number a price has to cover. So it is the quantity I act on, not a proxy (USE-5). The host calls it "loss given default", but the definition describes it correctly.
- I would want the conditional mean E[loss | inputs], a single number, to set the price. For the portfolio choice I would want loans ranked by that mean.
- Separate PD and LGD figures would help reporting, but the host removed the default flag, and the combined number is what the price covers.
- Not stated by the source: whether the loss is discounted and whether workout costs are included. Minor.

**3. One row, one decision; the test data.**
- One row is one loan at booking, which is one decision. That matches.
- The test (the next 5,800 loans, trained on all earlier ones) is what I face, with two differences.
  - *No outcome gap (SPLIT-10).* When I refit, I only have outcomes for loans that have terminated. An entity's loans sit a median 165 rows apart, while a loss takes a loan's term plus the workout to settle. So the true delay is far longer than a few hundred rows, and the newest training loans would not yet carry labels. Without dates the delay cannot be sized. The notes and `fit_reason` already name this gap.
  - *The entity's history.* About 5-8% of a window's loans have the entity's previous row on the training side. That history is legitimate only for loans whose outcome had arrived by then (USE-10, LEAK-34). Given the gaps above, that applies to almost none of them, which points back to the f274 finding.

**4. Would I use this model?** The untuned hurdle model, P(loss) x E[loss | loss], on windows 0_0 / 4_0 / 8_0:
- Lift: the top 10% of predicted expected loss holds 17% / 26% / 19% of the losses, and the top 20% holds 30% / 35% / 33%. The loss rate in the top 5% is 15-18%, against about 9.4% overall.
- Calibration in the large: mean predicted 0.82 / 0.85 / 0.82 against realised 0.83 / 0.84 / 0.79.
- Calibration by decile: roughly monotone, from 0.25-0.28 predicted (0.17-0.32 realised) in the bottom decile to 1.7-1.9 predicted (1.4-2.1 realised) in the top.

As a screen this is modest but usable: dropping the worst decile removes about a fifth of the losses for a tenth of the volume. That is in line with LGD practice, where Loterman et al. (2012) report R^2 of 4-43% across six banks' datasets. I would not put it into production, for three reasons:
- The fields are anonymised, so no validator can review the model's conceptual soundness.
- The host's "ex-ante" label has been wrong three times: the 9 columns he removed, the 2 golden features, and now the f274 family.
- With no dates, I cannot test it out of time by vintage or across the credit cycle.

As a benchmark of how methods rank loans, it is a fair task once the f274 family goes.

**5. The metric (`normalized_gini`, stand-in for the competition's MAE).**
- *MAE.* Overruling it is right (MET-4's overrule clause, MET-2). Its optimum is the conditional median, which is 0 for nearly every loan without the golden features. Predicting 0 scores 0.803, and every honest model scores worse.
- *What the Gini scores.* It sorts the actual losses by the predicted loss: the ordered Lorenz curve. That is how I would pick the risk-differentiation model. In credit I use the Gini or accuracy ratio, and actuaries choose zero-inflated loss-cost models by Frees, Meyers and Cummings' Gini (2011). The Allstate (2011) and Liberty Mutual (2014) competitions scored a Gini on targets of this kind, and freMPL in this collection declares the same metric. It scores one loan as the unit, over windows of 541-581 losses.
- *Tail effects.* The Gini is less driven by a few big losses than RMSE. Losses of 50 or more (0.09-0.19% of rows) hold 8-18% of the loss sum but 30-57% of the squared error around the mean.
- *What it misses (MET-1).* The price level. The hurdle predictions doubled keep their Gini (0.235 / 0.290 / 0.232), while their RMSE skill falls from +0.007 / +0.016 / +0.012 to -0.047 / -0.039 / -0.040. A pricing desk would lose money on a model that a Gini cannot tell apart from the correct one. In practice the level is set by a separate calibration on the training side, and a monotone recalibration leaves the Gini unchanged. So for selection the Gini is my choice; for pricing I would add a check of predicted against realised loss by decile.
- *Other rules.* The source fixes no threshold, cost or k: "flag the worst" names no count, so MET-6 and MET-7 give no `precision_at_k` or `cost_matrix`. AUPRC does not apply (MET-9). The `rmse` fallback (MET-8) is driven by the tail, as above.
- *If one metric had to score both ranking and level,* I would take the mean Poisson deviance. It is consistent for the mean of a non-negative target. The hurdle model's skill on it is 0.029 / 0.051 / 0.038, against 0.007 / 0.016 / 0.012 for RMSE skill, and doubling the predictions drops it to -0.06 to -0.08. But no source names it, it needs strictly positive predictions, and it is not in the metric library (MET-13). I would not switch to it.
- *Origin label (MET-11).* MAE can be computed on our data; it is overruled because its meaning did not survive the change. The README's "a stand-in for the source's metric, which cannot be computed" is therefore inexact. `context` with MAE named as the original, as in freMPL, may describe it better. That is for the critic or the curator.

**Gaps between the dataset and the real decision, ranked by how much they change the task.**
1. **The f274 family is hindsight** (LEAK-10, USE-3; LEAK-38 no longer applies). Row j holds the outcome of loan i, which was still running when loan j was granted (AUC 0.91 at gaps of 1-10 rows). Dropping it is free (Gini -0.002 on average over 3 windows). It changes what the task claims, not the scores. If it is kept, USE-8 requires `fit_reason` to name it as a kept leak; today `fit_reason` does not mention it.
2. **No outcome gap** (SPLIT-10). I train on loans whose outcome I would not yet know. It cannot be sized without dates, and it is already named as a gap.
3. **No dates, and de-trended anonymised features.** I cannot see vintage, cycle or drift, and cannot check the timing of any field. This is the core of the approximate fit (USE-8) and the `Anonymized` risk (LEAK-32).
4. **Inputs I would always hold may be missing**: amount, price, LTV, my own grade (USE-6). This is unknowable with anonymised fields.
5. **The metric ignores the price level** (MET-1). This matters for pricing, not for selection.
6. A 0 merges no default with full recovery. This changes nothing for an EL price.

**What an expert would change.**
- Drop f274, f271, f275 and f277 under LEAK-10, citing the gap test. Then rewrite the LEAK-34/LEAK-38 note and the `splits_comment` sentence that calls the previous row "its own history".
- Narrow `use_case` to the decision the metric scores: rank new loans by expected loss to choose which enter a portfolio, with the level set by a separate calibration, as freMPL's reason says. The alternative is to keep "price it" and say in the metric's reason that the Gini does not score the level.
- Treat f6 as a categorical (the relationship person the host names), after the column auditor checks it.
- Optional: estimate how much the missing outcome gap matters by measuring the Gini with a one-window gap (5,800 rows) against no gap, and state the difference in `splits_comment`.

**Sources.** Kaggle forum topics 6862, 6871, 6962, 6978, 7115, 7398; the record and `dataset.py`; the builder's metric runs; my own scripts. Loterman, Brown, Martens, Mues, Baesens (2012), "Benchmarking regression algorithms for loss given default modeling", IJF 28(1):161-170 (abstract, https://ideas.repec.org/a/eee/intfor/v28y2012i1p161-170.html). Frees, Meyers, Cummings (2011), "Summarizing insurance scores using a Gini index", JASA 106(495):1085-1098 (summary via the cplm `gini` documentation). GARP on the gAUC for LGD (https://www.garp.org/risk-intelligence/credit/how-to-improve-lgd-unlocking-the-generalized-area-under-the-curve). Arnaud de Servigny's Imperial profile (https://profiles.imperial.ac.uk/a.deservigny). EBA GL/2017/16, cited from memory for the split between risk differentiation and quantification (the PDF was not readable here).

</details>

<details><summary>Blind review</summary>

**Verdict: exclude.** As prepared, the zero-inflated `loss` target has no usable signal under the temporal split. LightGBM R² is between -0.07 and +0.014, and its MAE is no better than predicting 0. The two columns that carried nearly all the signal in the original competition (f527, f528) are gone, and nothing explains why. Because the features are anonymised, no one can tell which of the remaining columns are known before the outcome.

**What the task is.** This is the Kaggle "Loan Default Prediction - Imperial College London" competition (2014, 677 teams). Its page gives one line about the use: "Constructing an optimal portfolio of loans". Each row is a loan or transaction. `loss` is the percentage of the notional that was lost (0 means no default). It is an integer from 0 to 100: 90.7% of rows are 0, the median of the non-zero values is 5, and 35 rows are at 100. Scoring the expected loss on a loan is a real lending decision. Here, though, the features are anonymised and de-trended, so the real use (who predicts it, and when) can only be guessed. The table is only `train_v2.csv` (105,471 rows). The competition's 210k test rows never had public labels.

Ranked concerns

1. **The target as prepared has no measurable signal. A benchmark on it would rank noise.**
   - Setup: I approximated the 9 windows as expanding windows over 10 equal blocks in `time_index` order (train on blocks before k, test on block k, about 10.5k test rows each). All features except `time_index` were used.
   - Predicting all zeros gives a test MAE of 0.766 / 0.790 / 0.796 / 0.801 in windows 1/3/5/7. LightGBM with L1 loss gives 0.768 / 0.793 / 0.798 / 0.803, which is no better. LightGBM with L2 loss (400 trees) gets R² -0.069 / -0.030 / -0.017 / -0.009, which is worse than predicting the training mean.
   - A conservative L2 model with early stopping on the last 15% of the training rows stopped after 6 trees at window 2, with R² 0.0001. With more training data it reached R² 0.008 at window 5 and 0.014 at window 9, the largest training set (95k rows). A Tweedie model got 0.0002 / 0.004 / 0.006 and a hurdle model (P(default) × predicted severity) got 0.0005 / 0.008 / 0.009 in windows 2 / 5 / 9. The best result anywhere is R² 0.014, an RMSE of 4.003 against 4.031 for the training mean.
   - Telling defaulters from non-defaulters is weak: LightGBM AUC is 0.66 to 0.74. The best single column (f766) reaches AUC 0.635. `time_index` alone gives 0.513.
   - The squared error is dominated by a few extreme rows. In every test window, the top 1% of rows account for 75-82% of the squared error around the mean. The 11-21 rows per window with loss >= 50 account for 35-58% of it. RMSE or R² differences between methods would mostly reflect which window happens to contain the 100s.
   - Change: do not benchmark this as a regression on all rows.

2. **The competition's "golden features" f527 and f528 were removed, and nothing says why.**
   - 111 of the original f1..f778 are absent, including f527, f528, f529, f530, f531, f534, f535 and f537. task.md links discussion 7115, which is the golden-features thread, so the preparer probably saw it.
   - Public evidence that these columns carried the signal: the 9th-place README (ChenglongChen) says "I use the golden features revealed by Yasser (thanks a ton!), i.e., f527 and f528" and "use the difference instead, i.e., f274-f528, f274-f527, and f527-f528". Its default classifier reached an "f1-score aroud 0.9488x". With these features, the best teams finished at about 0.445 MAE (2nd place README: "0.44465, ranking 2 of 677"). The all-zero baseline here is about 0.80.
   - The signal cannot be rebuilt from what is left. I scanned the 2,929 column pairs with |r| > 0.95, and the best difference reaches AUC 0.618. f274 minus each of its closest correlates reaches 0.568.
   - Either way the dataset fails:
     - If the drop was deliberate (suspected post-outcome information), it is defensible. But it is undocumented, and what remains is concern 1.
     - If it was accidental (for example a duplicate or correlation filter), it is a preparation bug, and the task becomes a different and much easier one. That version would then need its own leakage review.
   - Change: record the column-drop rule and the reason f527/f528 were removed. If the removal was accidental, restore them and review again.

3. **The features are anonymised and undocumented, so leakage cannot be ruled out.**
   - The 4th-place README calls the data "an anonymized history of transactions for each loan". The 2nd-place README says "Owing to lack of the feature description, It is hard to use the tradition method to predict LGD".
   - Nothing public says whether any column was measured at origination or after default. The golden-feature pattern (two almost identical columns whose difference nearly reveals the outcome) is a classic sign of a leak. So I would not trust the columns that are left without documentation either.
   - Among defaulted rows only, loss severity is fairly predictable: LightGBM R² 0.31 / 0.35 / 0.40 in three temporal windows, against MAE 5.55-6.0 for the median baseline. That would be a meaningful loss-given-default task, but the same doubt about when each feature becomes known applies to it.
   - Change: none is possible from public sources. This is the main reason I would not rescue the dataset by reframing it.

4. **The temporal split is defensible, but it rests on row order alone.**
   - `time_index` runs 1..105,471, contiguous and monotonic, so it is the row number of `train_v2`.
   - The 2nd-place README supports treating row order as time: "The training data is sorted by the time, and the test data is randomly orded." There are no timestamps, so windows are equal row counts, not calendar periods.
   - Drift is visible, which supports a temporal split:
     - f777 mean by decile: 0.22 → 0.16 → 0.56 → 0.18
     - f778 mean: 106 → 300 → 108
     - default rate: 8.4% → 9.9%
   - `time_index` should be used only for splitting, not as a feature (it is an id). On its own it is nearly useless (AUC 0.513), and tree models would extrapolate it.
   - Copies: no row appears twice, either with or without the target. I compared 150 random rows against all others: the closest match shared at most 313 of 669 values exactly (median 127), and nearest neighbours sit close in time (median gap 1,536 rows). I found no repeated loans, but could not rule out the same borrower appearing at different times.

5. **Several preparation details need fixing.**
   - f466 is `uint64` with a maximum of 9.62e18, which is above the int64 limit (9.22e18). f337 is `int64` with a maximum of 9.04e18. Some loaders and frameworks will overflow or refuse these. Cast every feature to float64.
   - 27 columns exceed 1e15 in magnitude, up to 2.9e34 (f472). Only f391 and f627 were replaced by log10 versions (`f391_log10`, `f627_log10`, maximum about 41.9, so the raw values were probably above the float32 range). The treatment is inconsistent; state the rule or apply it to all columns.
   - The duplicate rule is unclear: 111 columns were dropped, yet 66 pairs with |r| > 0.9999 remain (for example f21/f763, f7/f439/f467, f36/f770). This is harmless for trees, but say which rule was used.
   - f776 and f777 are 0/1. The source says they may be categorical; keeping them as numeric 0/1 is fine.
   - Missing values: 1.08% of cells, 50.8% of rows have at least one NaN, and no column is more than 17.9% missing. Leaving them as NaN is appropriate.

6. **Size is adequate, but scores will be noisy.**
   - There are 105k rows and about 1,000 defaults per test window, which is enough to score.
   - Because of the heavy tail (see concern 1), the scores will vary a lot from window to window.

What I could not check
- The Kaggle data page and the discussions (6962, 7115) render with JavaScript and the API needs a login. I could not read the official data description, the sponsor's statement on ordering, or the content of discussion 6962. My recollection that the data page says the training rows are "listed in order from old to the new" is unverified; the 2nd-place README quoted above confirms the ordering.
- I could not get the original `train_v2.csv`, so I could not see the dropped columns or the preparer's rule for dropping them.
- Whether f527/f528, or any remaining column, is recorded after the outcome.
- The exact boundaries of the benchmark's 9 windows; I approximated them with equal row blocks.
- Whether borrowers repeat across rows.

</details>

<details><summary>Precedent check</summary>

**Precedent checker: loan_default_prediction_imperial_college (2026-11-01)**

**Verdict: mostly consistent, with three departures for the curator.** Most of the definition's choices follow decided precedents: the f527/f528 drop, the row-order time axis, the MAE overrule, the cleaning, and the record fixes. Three choices depart from their closest precedents:
- the f274 family is kept under LEAK-38 although the panel has now measured its timing;
- the six other aggregates are dropped although the tests clear them;
- there is no gap, and the reason given is not the fact behind the precedent it cites.

The register shows no drift: Andrej's two CCs on this record agree, and he has made no other SPLIT-10 or LEAK-38 call. Andrej's own decisions are on this record; the precedents below are Lennart's, from the main rule files, unless a precedent is marked "AI, this batch" (an AI suggestion the curator has not ruled on). One amendment trigger is close: if the no-gap call is recorded under lending_club's reason, it is that reason's third exception.

How I worked: I read the register (the batch's register: SPLIT-10, LEAK-10, LEAK-38, LEAK-34, CLEAN-14, and the flags), the Cases tables of `splits.md`, `leak_checks.md`, `metrics.md` and `cleaning_features.md`, and the sibling definitions in `datasets/_dev/tabarena-v0pt2/`: lending_club, alfa_battle_2_0_task_2, home_credit_default_stability_1m, african_credit_scoring_challenge, zillow_prize, forest_fires, allstate_claims_severity, the insurance Gini tables of this batch, qsar_oral_toxicity, california_house_prices_2020 and kick. I also read the record, the builder report, and the split-auditor's and domain-practitioner's reports. I took the numbers from those reports and re-measured nothing. The register has no MET sections (MET IDs are not parsed), so I read the metric precedents in `metrics.md` directly.

**Decision by decision, in rank order**

1. **P4: the f274 family (f274, f271, f275, f277) kept under LEAK-34 / LEAK-38.** Status: **departs without a fact that sets it apart; not reasonable under the ranking if the curator accepts the panel's timing measurement.**
   - The closest precedents are the LEAK-38 scope amendment (2026-10-22, Lennart) and its cases:
     - kick's `WheelType` was kept under LEAK-38 on 2026-10-01 and dropped under LEAK-10 on 2026-10-22, once a conditional test measured the mechanism. `WheelTypeID`, `PRIMEUNIT` and `AUCGUART` went with it.
     - expresso_churn_prediction's `REGION`, dropped (2026-10-22).
     - fraud_detection_in_electricity_and_gas_consumption, history cut at a measured step (2026-10-26).
     - homesite `PropertyField37` was kept only because its timing could not be tested.
   - LEAK-38 "covers only fields whose timing cannot be tested". The definition keeps the family "on the reading that a loss was known when the next loan was granted, which anonymised fields cannot confirm". The panel has since tested that reading:
     - f274 in a row shows whether the entity's previous loan had a loss at ROC AUC 0.948, and at 0.91-0.96 when the previous loan is only 1-10 rows earlier (8,083 links). The median gap is 165 rows (split-auditor; domain-practitioner).
     - A loan granted a few loans earlier has not run its term ("a factor from 1 to 3", topic 6862).
   - LEAK-34 does not carry the keep on its own precedents:
     - ieee_fraud_detection's `uid` and ghana's reporter history pass earlier labels through the training side.
     - Here the predecessor's outcome sits in the test row's own feature. For 62-67% of test loans that predecessor is inside the same test window.
   - The nearest analogue on timing is alfa_battle_2_0_task_2 (2026-10-21, Lennart). A flag that "was set after the later issue" was treated as not yet known, and the measurable shortcut was removed. The principles.md tension row says: "a shortcut that can be measured is always removed, whatever it costs".
   - Cost of following the precedents: the hurdle model's Gini changes by -0.002 on average over 3 windows (domain-practitioner).

   **Consistency check (AI, 2026-11-01):** keeping f274, f271, f275 and f277 under LEAK-38 differs from kick (`WheelType`, kept 2026-10-01, dropped under LEAK-10 2026-10-22) and expresso (`REGION`, 2026-10-22). The mechanism is the same: an anonymised or host-coded field whose timing was later measured on the data. LEAK-38 now covers only fields whose timing cannot be tested. What sets this case apart?
   (a) The test measures timing in rows, not in time. Without dates, the claim that a loan 1-10 rows later was granted before the earlier loan settled rests on inferred terms. So the timing is still "not testable" in LEAK-38's sense, and the keep is recorded with that stated (and in `fit_reason`, USE-8).
   (b) Treat it like kick: drop the four under LEAK-10.
   (c) Reopen kick and expresso to match.
   (d) Amend LEAK-38 so that a row-order test without dates does not count as a measurement.

2. **P4 / P7: f529, f530, f531, f534, f535 and f537 dropped "by the curator's call" (CC 2026-11-01).** Status: **departs without a fact that sets it apart.**
   - The CC accepted the 2026-11-01 Assessment, which called the six "sibling aggregates" of f527 and f528. The builder then tested them:
     - Their change separates "x moved in the own period" at AUC 0.51-0.61, and "x moved in the previous period" at the same values (0.51-0.61). That matches ordinary columns (f575 0.606 / 0.615).
     - Their Spearman with the own period's change is 0.02-0.21.
     - Restoring them moves the Gini by +0.022, -0.010 and -0.006 on 3 windows.
   - Precedents that keep an aggregate once the data shows it behaves like history:
     - online_shoppers `PageValues` (LEAK-10 Mechanisms row: "keep only the period where it behaves like history").
     - account_debt_south_africa `TotalBilling` / `AverageBilling` (2026-10-26, Lennart; LEAK-10 amended: "a window sum stays when the data shows it does not move with the outcome").
   - CLEAN-22 (Must) says columns leave "for what they are". kick's `PRIMEUNIT` / `AUCGUART` went with `WheelType` only on a measured conditional test (42.3% predicted against observed), not as family members.
   - The case for the drop: LEAK-10 (Must, P4) lists "an aggregate that *may* include the row's own outcome" as out, and P4 outranks CLEAN-22 (P7). So a precautionary drop is defensible if the curator still reads them as aggregates of the same hidden x. Nothing in the data shows that they are.
   - The LEAK-10 note "a 'removing it changes no score' test alone is still no reason to keep" cuts both ways here: zero cost alone decides neither the keep nor the drop.

   **Consistency check (AI, 2026-11-01):** your call on f529-f531, f534, f535 and f537 (drop) differs from online_shoppers `PageValues` and account_debt_south_africa's billing totals (kept 2026-10-26, Lennart). Those were aggregates the data showed to behave like history; here two label-free tests show the six behaving like ordinary columns. What sets them apart?
   (a) They belong to the same block of running aggregates as f527/f528, which carry the outcome's period. With anonymised fields a label-free test is indirect, so the whole block goes under LEAK-10's "may include". Recorded as an exception, with that fact.
   (b) Treat them like `PageValues`: restore the six, with a `Potential leak, kept on purpose:` note.
   (c) Reopen `PageValues` and account_debt_south_africa to match.
   (d) Amend LEAK-10 so that the siblings of a measured leaking aggregate go with it.

3. **P4: no gap (SPLIT-10, Should), "a departure as for lending_club".** Status: **departs with a stated reason that is not the cited precedent's fact.**
   - SPLIT-10 precedents and their facts:
     - lending_club (2026-10-21, Lennart, exception): a gap of the known delay (36 or 12 months) leaves 5-9% or 33-46% of rows for training. Serves SPLIT-14.
     - alfa_battle_2_0_task_2 (2026-10-21; gap 0 on 2026-10-26, Lennart): the same SPLIT-14 reason, with SPLIT-9's measurable shortcut removed.
     - ames_housing, house_prices_nominal, perth_house_prices (2026-10-26, Lennart): month resolution coarser than the delay, and no selection in the newest period. An amendment is already proposed for this reason (`splits.md` Cases).
     - melbourne_housing_market (2026-10-21, Lennart): no gap, "a gap only if the newest months show selection", decided as an application of the rule.
     - Gaps applied: brazilian_ecommerce, sf_permit_time, house_sales, zillow_prize, the taxi and ETA `_1m` sets.
   - The stated reason here, "without dates the delay cannot be sized", is a new reason. It names no higher principle served, and it does not match lending_club:
     - A 5,800-row gap with 5,000-row windows still trains the oldest window on 51.8% (split-auditor), so SPLIT-14 does not bind as the windows could be laid out.
     - Measured: a one-window gap moves the Gini by +0.006 and the AUC by -0.001 on 4 windows, and the newest 5,800 training loans are worth no more than the oldest 5,800.
   - The decision is also tied to decision 1. If f274 stays on the reading "a loss is known by the next loan", the delay can be sized from the link gaps (99% within 5,907 rows), and a 5,800-row gap fits.
   - Register flag 10 already lists SPLIT-10 as amendment-due (five datasets, two reasons). Recorded under lending_club's SPLIT-14 reason, this would be that reason's third exception, so an amendment would be due, but the fact does not hold here.

   **Consistency check (AI, 2026-11-01):** no gap here (a departure from SPLIT-10) cites lending_club (exception 2026-10-21), whose fact is that a gap of the delay breaks SPLIT-14's 50% floor. Here a one-window gap fits the floor and changes nothing measurable. What sets this case apart?
   (a) A loan's term, the real delay, is plausibly a large share of the file's unknown span (terms vary 1 to 3 times; the file spans an unknown period). A gap of that size would break SPLIT-14 as in lending_club, and no smaller gap is better grounded than none. Recorded as an exception that serves SPLIT-14, with the measured null effect of a one-window gap stated in `splits_comment`.
   (b) Treat it like brazilian_ecommerce or zillow_prize: add a gap (5,800 rows, windows of 5,000).
   (c) Reopen lending_club to match (not suggested: its fact is measured).
   (d) Amend SPLIT-10: "no gap is needed when a gap of one test window changes no score and the newest training rows carry no more signal than the oldest" (the melbourne reading, generalised).

4. **P4: the time axis from the row order, windows in rows.** Status: **consistent.**
   - california_house_prices_2020 and seismic_bumps (SPLIT-22: the source's id or file order kept as time; california also uses windows in rows), and mercedes_benz_greener_manufacturing (row windows).
   - The split-auditor's text point (the host's "There is no after and before" is left out of the quote) is an evidence matter (EV-2), not a precedent conflict.

5. **P4: f527 and f528 dropped under LEAK-10.** Status: **consistent.**
   - The host's own removal of 9 ex-post aggregates (topic 6962).
   - The LEAK-38 amendment and kick (2026-10-22): a measured mechanism sends a field to LEAK-10.
   - The principles.md tension row "a real task against a leak: fix the leak and keep the task" (kickstarter `staff_pick`).
   - iranian_churn (retired 2026-10-01, Lennart) is set apart by a measured fact: a chain's last row has a loss as often as its other rows (9.42% against 9.38%), so the features do not summarise a window that ends at the outcome.

6. **P3 / P5: the target `loss` shipped raw, 0 for both no default and full recovery.** Status: **consistent.**
   - The coded-zeros policy (Andrej, 2026-10-30: "We don't care. We want to add any relevant predictive task").
   - MET-3: the shipped scale is a modelling choice. allstate_claim_prediction_challenge ships log1p, zillow_prize raw. The Gini is unaffected because it is computed after the inverse transform.

7. **P6: the metric, normalized Gini as a `stand_in` for the competition's MAE.** Status: **overrule consistent; the origin label has a precedent, with one point to note.**
   - The overrule follows MET-4's clause (evidence measured on the shipped splits): predicting 0 scores MAE 0.803 and every honest model scores worse.
   - It is set apart from the MAE keeps by a stated fact. The conditional median is 0 for 99.8-99.95% of loans:
     - zillow_prize (2026-10-21): a logerror around 0, not zero-inflated;
     - forest_fires (2026-10-21): 48% zeros, so the median is not degenerate;
     - allstate_claims_severity: claim severities, no zeros.
   - Like numerai_v5_2_1m (2026-10-21), a metric under which better models lose was replaced.
   - Origin label:
     - home_credit_default_stability_1m (MET-2 cases) declares a `stand_in` for a source metric that is computable but meaningless on our windows. That is the closest precedent, and MET-2's "a task we changed keeps the source's metric only when its meaning survives the change" supports it.
     - Against it, MET-11 describes a stand-in as "the closest computable metric", and a ranking Gini is not close to MAE.
     - african_credit_scoring_challenge (2026-10-26, Lennart) went to the fallback when a competition metric was overruled.
     - The insurance tables of this batch (frempl, spanish_motor x2, australian_vehicle; AI, this batch, metric not ruled on by the curator) declare the same Gini as `context`.
   - Not a departure needing a prompt. `context` (MAE named as the original) is the reading that fits the batch's own Gini tables, and the domain-practitioner reaches the same conclusion. The curator may want one label for the family.

8. **P6: TP-2, small real signal kept.** Status: **consistent.** forest_fires ("the split follows what the task does in reality, not the size of the gap"). Here the signal is larger: a loss is ranked at AUC 0.71-0.75 on 9 of 9 windows.

9. **P7: cleaning.** Status: **consistent.**
   - f391 and f627 as log10: rdkit_Ipc_log10 (qsar_oral_toxicity, 2026-10-21, Lennart). The same fact: values beyond float32, all positive. It ships log10(x) and not log10(1 + x), which is harmless since every value is far above 1.
   - Constant columns and copies dropped: the CLEAN-5 text.
   - f776-f778 typed categorical from the host's factor list, and every other anonymised column numeric: CLEAN-14 as amended (2026-10-21, Lennart: "keep it a number" without semantic context).
   - `-1` kept as a value: home_credit_default_risk's accepted `dataset_missing_value_sentinel` (POS_MONTHS_BALANCE -1).
   - Open but not a precedent conflict: f2 ("a size cluster") is kept numeric as an ordered range, though a cluster label need not be ordered. The domain-practitioner reads f6 as a relationship-person code. Both are for the column auditor.

10. **Warnings and record fields.** Status: **consistent.**
    - `task_target_value_dominant` is accepted in frempl, australian_vehicle, crms_phragmites_cover, avito_demand_prediction_1m and noaa_storm_events_damage (AI, this batch).
    - Removing `Data Quality Issue` once the concern is refuted follows thyroid_discordant's `Trivial` marker, removed after its test (2026-10-22, Lennart).
    - Adding `Non-IID (Temporal)` matches lending_club and alfa_battle_2_0_task_2.

**Builder's draft recommendations against the precedents**

| Draft issue | Precedent reading |
|---|---|
| 1. SPLIT-10, no gap, "as lending_club" | the cited fact does not hold (decision 3); option (a) or (b) above |
| 2. The six aggregates: keep the drop or restore | restoring follows `PageValues` and account_debt; keeping the drop needs the exception in (a) (decision 2) |
| 3. Metric: Gini stand-in, `rmse` or MAE | overruling MAE is consistent; `rmse` has R^2 0.011 (MET-10 resolution); stand-in or context is a labelling choice (decision 7) |
| 4. CLEAN-2, log10 | follows rdkit_Ipc_log10 |
| 5. Record marker and tag | follow thyroid_discordant and lending_club |
| (missing) the f274 family | not in the builder's list; the panel's measurement puts it under the kick precedent (decision 1) |

</details>

<details><summary>Advocate</summary>

**Advocate: loan_default_prediction_imperial_college (2026-11-01)**

**Position: ship after changes.** The task is real, the split is right, and the signal holds on every window. The panel found one real validity problem: the kept f274 family is hindsight, and it covers more columns than the definition names. The fix is to change the definition (drop the columns), not to exclude the dataset. The rest are text fixes, a label fix and one dtype fix.

**1. A real task with a measured leak gets the leak fixed, not the task removed (P3 over exclusion; USE-12, LEAK-10 Must; the remedy ladder; the "real task against a leak" tension row).**
- Evidence: one row is one loan at booking. The target is the realised loss per 100 of notional, the number an expected-loss price has to cover (domain practitioner: "the quantity I act on, not a proxy", USE-5). The host framed the task as "constructing an optimal portfolio of loans" and "flag the worst of the population" (topic 6978).
- The real problem, conceded: the "Potential leak, kept on purpose" bullet is refuted. f221, f222 and f212 give the previous loan's loss from their level at ROC AUC 0.987-0.994, even when that loan is only 1-10 rows earlier (column auditor's gap table). So the outcome was written in after the fact. LEAK-38 covers only fields whose timing cannot be tested, and this timing has been tested. The kick precedent (`WheelType`, 2026-10-22) moves them to LEAK-10.
- Remedy (fix the definition): drop the column auditor's 27 columns (the column auditor's list) in `_clean`, measure f615, f617 and f278 at the edge of the sweep, and rewrite the bullet as a LEAK-10 drop with the gap table. Cost: AUC -0.0026 and Gini -0.032 on average over 9 windows. LEAK-6: a confirmed leak goes even when it is small. A lag cannot repair these columns, but a drop does. So this is no LEAK-27 case, where the leak cannot be undone.
- Why it outranks the call to exclude: the ladder puts "fix the definition" above exclusion, and exclusion is only for a Must that cannot be fixed. kickstarter (`staff_pick`) and kick were fixed the same way.

**2. The second probable leak has the same fix, and it makes the curator's drop of the six consistent (LEAK-10 Must, LEAK-2; P4 over CLEAN-22, P7).**
- Evidence: in the top tail of f468, f471, f533 and f536, the label-free test shows the loan's own period: x moved for 34 of 34 rows (f471) and 27 of 27 (f536), against 33.1% overall. This is the signature that convicted f527 and f528. These columns are the +65 twins in the block of the host-removed f473/f474 (column auditor, problem 2).
- Remedy: drop all four (cost: AUC -0.0097, Gini -0.043 on 9 windows). Capping at the training side's 99.5th percentile is the milder alternative (LEAK-7), but the cut is ad hoc. With the four dropped, keeping the curator's drop of f529-f531, f534, f535 and f537 fits option (a) of the precedent checker: the whole running-aggregate block of a measured leak goes under LEAK-10's "may include", recorded as an exception. P4 (Must) outranks CLEAN-22's "for what they are". Restoring the six changes the Gini by noise only (+0.022, -0.010, -0.006), so neither side has a score argument (LEAK-10 note).

**3. The iranian_churn objection is refuted on the data (P5, LEAK-21; EV-2: a measurement outranks a reading).**
- Evidence: a loss does not end a chain. A chain's last row has a loss at 9.42%, its other rows at 9.38%, and 70.3% of the loans with a loss have a later row (claim auditor: reproduces). The rows of a chain are different loans, not snapshots of one: along the links the maturity range f4 changes in 85.6% of cases, collateral in 38.5% and region in 62.6% (split auditor).
- What follows: the record's `Data Quality Issue` marker should go, as thyroid_discordant's `Trivial` marker went once it was tested. The record's "f275 = f274^2" is wrong (true in 0.42% of rows) and should be corrected at the next record edit.

**4. The signal is small but real, and the blind reviewer's "exclude" measures it with the two metrics we overrule (TP-2; P4 over P6; forest_fires).**
- Evidence: a loss is ranked at ROC AUC 0.71-0.75 on 9 of 9 windows. The hurdle model's Gini is 0.236 (0.17-0.30), above 0 on 9 of 9, against a constant at z 5.4-7.5 (claim auditor). Among the losses, their size is predicted at R^2 0.46-0.58 on log1p. The blind reviewer agrees that severity is "fairly predictable" (R^2 0.31-0.40) and that the AUC is 0.66-0.74. Its no-signal verdict rests on MAE and R^2. The definition shows why neither can score this task. The blind reviewer's second concern (f527/f528 removed "and nothing says why") is answered by the definition's LEAK-10 bullet and `_decisions` table, which the blind reviewer did not see.
- As a screen the model is "modest but usable": the worst predicted decile holds about a fifth of the losses (domain practitioner). That is within LGD practice, where Loterman et al. (2012) report R^2 of 4-43%.
- Conceded: these numbers come from before the drops in points 1 and 2. Together the drops may cost about 0.07 of Gini, which is untested. The combined Gini and AUC must be measured on the 9 windows and written into the notes before the curator decides. Even if the signal shrinks, TP-2 keeps a small real signal, and the split follows the application, not the score (the forest_fires tension row).

**5. The temporal split is right, and SPLIT-9 holds (SPLIT-1, SPLIT-3, SPLIT-11, SPLIT-14, SPLIT-22).**
- Evidence: the row order matches each entity's sequence. Entity links rise in id in 99.97% of cases, against 50% for a random order. The Kaggle admin wrote "The train/test split is done by time", and the data page says the rows are "listed in order from old to new". No feature tracks the id (largest |Spearman| 0.102). No test loan has the entity's next row in training. The alfa_battle filter changes the AUC by -0.002 (split auditor).
- No gap: conceded that the stated reason does not hold. A one-window gap fits the 50% floor, so lending_club's fact is missing here. The mildest remedy is the rule's default: `TemporalSplits(window=5000, unit="rows", n_windows=9, gap=5800)`. It trains the oldest window on 51.8% of the rows, and on the 4 windows tested it moved the Gini by +0.006 and the AUC by -0.001. That removes a Should departure instead of recording an exception that rests on the wrong fact. If the curator prefers no gap once the f274 family has gone, option (a) of the precedent checker is the honest exception (the real delay is a loan's term and would break SPLIT-14), with the null effect stated.
- Text: quote the host's full answer ("There is no after and before. These transactions are all completed."), and say "the order the loans were recorded" unless the curator keeps "granted" as our reading (EV-7). Add one sentence saying that 62-67% of a window's loans have an entity predecessor inside the window (SPLIT-13).

**6. Overruling MAE is right. Fix the label, not the choice (MET-2, MET-4's overrule clause; MET-11).**
- Evidence: predicting 0 beats every honest model on MAE (claim auditor: z 66-77). Without the golden features, MAE's optimum is 0 for 99.8-99.95% of the loans. A metric under which better models lose has been replaced before (numerai_v5_2_1m). The Gini scores the risk-differentiation step at the unit of one loan, which is how credit practice picks a model (Gini or accuracy ratio; Frees et al. 2011 for zero-inflated losses). It also scores the host's "flag the worst".
- Conceded: `stand_in` does not fit MET-11, because MAE is computable. Remedy: declare the Gini as `context` with MAE as the original, as this batch's insurance Gini tables do, or record it as a curator overrule. Also conceded: "RMSE resolves little" is overstated. Between models, RMSE separates as well as the Gini (paired z about 2 on both), but 1% of the rows drive it. The reason should state both sides. Either narrow `use_case` to ranking for portfolio choice, with the level set by a separate calibration, or say in the reason that the Gini ignores the level.

**7. Cleaning follows precedent. The one dtype miss is cheap (CLEAN-5, CLEAN-2, CLEAN-14).**
- The definition's own asserts reproduce the 11 constant columns, the 81 copies and the 669 features. The 19 big-integer text columns round-trip without loss. f391 and f627 ship as log10 because they pass the float32 range, the same fact as rdkit_Ipc_log10. The -1 is a real value: the values run on from -0.99, and these columns have missing values of their own (home_credit precedent).
- Conceded: f6 is the host's "person instructing the loan", 1,079 arbitrary codes, shared along entity links in 24.2% of cases against 0.5% for random pairs. Make it `categorical` (CLEAN-14 Should). The score does not decide the dtype. Nit: cast f466 to float64 like the other long integers.
- Notes: replace the circular "f527 = ... on 100%" with the test that can fail (the next row's f274 equals x on 97.3% of links), per EV-6.

**Judgment record (proposed)**
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (approximate fit); LEAK-10 triggered twice and fixed (f527/f528 plus the six already dropped; the 27-column predecessor family and f468/f471/f533/f536 to drop); LEAK-21 holds (not iranian_churn); SPLIT-1/9/11/14 hold; SPLIT-10 met by a 5,800-row gap (or an exception with option (a)).
Value: TP-2, a small real signal (re-measure after the drops); MET-4 overrule of MAE, Gini declared as `context`.
Quality: CLEAN-14, f6 to categorical; text fixes (full host quote, EV-6, SPLIT-13 sentence).
For the curator: the six aggregates (keep the drop as a block exception, or restore them); the gap or the exception; the metric label and the `use_case` wording.

</details>

<details><summary>Critic</summary>

**Critic: loan_default_prediction_imperial_college (2026-11-01), opening brief**

**Verdict: do not ship as defined; ship after changes 1, 2 and 4.** The task is real: a lender ranks new loans by expected loss. The leaks can be fixed in `_clean`, so exclusion is not on the table (principles.md tension "a real task against a leak"). I do not take up the blind reviewer's "exclude for no signal". It rests on R^2 and MAE. Under the shipped Gini, the loss ranks at AUC 0.71-0.75 on 9 of 9 windows (TP-2, and the forest_fires tension row). I re-measured nothing; every number below comes from the phase A reports named with it.

**1. P4, LEAK-10 (Must), with LEAK-2 (Must): the kept "history" family is hindsight, and it has 27 columns, not 4.**
- *Problem.* The definition keeps f271, f274, f275 and f277 under LEAK-34/LEAK-38, "on the reading that a loss was known when the next loan was granted". Two auditors tested that reading independently, and it fails.
  - Column auditor: 27 columns carry the entity's previous loan's loss. f221's *level* alone gives it at ROC AUC 0.996. On links 1-10 rows apart (8,083 links) it is 0.993, and the f274 change is 0.948. The signal does not weaken when the earlier loan cannot have run its term (terms vary "by a factor from 1 to 3").
  - Claim auditor found the same columns: f222 0.996, f221 0.996, f212 0.992, f272 0.973. At gaps of 1-10 rows, x moved 99.4% of the time after a loss against 41.4% after none.
  - The family includes f538/f539, the +65 twins of f473/f474, which the host removed as "ex-post" (topic 6962).
- *Effect on the task.* The benchmark scores models on a field the lender did not hold at the grant. For 62-67% of test loans the predecessor is in the same test window (split auditor), so a test row carries a test-period outcome. The definition's line "no change from the earlier row passes ROC AUC 0.595" is true only for the row's own loss, and it misleads.
- *Rule.* LEAK-38 (Should) covers "only fields whose timing cannot be tested". This timing has now been tested, so LEAK-10 applies, as it did for kick's `WheelType` (2026-10-22; precedent checker, decision 1). LEAK-34 does not save the family: its cases pass history through *training* labels, while here the outcome sits in the test row's own feature. LEAK-6: a confirmed leak goes even when small. The cost is a Gini drop of 0.032 on average over 9 windows and an AUC drop of 0.0026 (column auditor).
- *Remedy (fix the definition).* Drop the 27 columns in `_clean`, citing the gap table. Measure f615, f617 and f278 (AUC 0.73-0.77) before ruling on them. Replace the "Potential leak, kept on purpose" bullet with a dropped-for-LEAK-10 bullet. Fix the "its own history (LEAK-34)" sentence in `splits_comment`.

**2. P4, LEAK-10 (Must when confirmed), LEAK-2: f468, f471, f533 and f536 record the loan's own period in their top tail.**
- *Evidence (column auditor).* This is the label-free test that convicted f527 and f528. Among loss-free linked loans in the top 0.1%, the own period's x changed in 34 of 34 (f471), 27 of 27 (f536) and 31 of 36 (f468), against a base rate of 33.1%. The previous period's x changed at the base rate. Loss rates in the top 0.1% are 59.0%, 58.1%, 35.8% and 28.3%, against 9.3%. The columns sit in the blocks of the host-removed f473/f474 and of the dropped f527-f537.
- *Effect.* This is the golden-feature mechanism again, in a smaller dose. Dropping the four costs Gini 0.043 and AUC 0.0097, the same on 9 of 9 windows, so they carry real score.
- *Caveat.* Only one agent measured this. The builder should reproduce it before the drop.
- *Remedy.* Drop the four (LEAK-10). LEAK-7's alternative is a cap, but the cap needs a cut, and a cut fit on all rows brings its own problem. The body's timing is no better tested than the six siblings', so the drop is the safe fix.

**3. P4, SPLIT-10 (Should): the no-gap reason is wrong whichever way point 1 goes.**
- *Evidence.* "Without dates the delay cannot be sized" contradicts the keep reading: if a loss were known by the next loan, link gaps would size it (99% within 5,907 rows; split auditor). The cited lending_club fact (a gap breaks SPLIT-14) does not hold here. A 5,800-row gap with 5,000-row windows trains the oldest window on 51.8%. Measured effect of a one-window gap: Gini +0.006, AUC -0.001 (split auditor; precedent checker, decision 3).
- *Remedy (text).* Once point 1 drops the family, keep no gap but record it as an exception with the real fact: the term is long against an unknown file span, and the gap was measured to have no effect. Do not write "as lending_club", which would also count wrongly as that reason's third exception. The alternative is to add the gap at no cost.

**4. P6, MET-11 (Must) and MET-2 (Must): the metric's origin label is wrong, and the Gini does not score the pricing the use case names.**
- *Evidence.* `stand_in` requires that the original "cannot be computed" and be replaced by "the closest computable metric". MAE is computable, and a ranking Gini is not close to it (claim auditor, row 42). What applies is MET-4's overrule, which is sound: predicting 0 scores MAE 0.803 and every honest model scores worse.
- *Second problem (MET-2).* `use_case` says "to price it". The domain practitioner doubled the hurdle predictions: the Gini stays the same (0.235 / 0.290 / 0.232) while RMSE skill turns negative. The metric cannot see the level a price needs.
- *Third problem (MET-10/EV-9).* "RMSE resolves little" is overstated. Between models, RMSE separates about as well as the Gini (paired z about 2 on both; claim auditor).
- *Remedy.* Relabel the origin as `context` naming MAE as the original, as the batch's insurance Gini tables do, or record it as a curator overrule. Narrow `use_case` to ranking loans for portfolio entry, with the level set by a separate calibration. Otherwise, state in the reason that the Gini ignores the level. Reword the RMSE sentence to give both sides.

**5. P4 against CLEAN-22 (Must, P7): the leak drops are inconsistent with each other.**
- *Evidence.* The six siblings (f529-f531, f534, f535, f537) are dropped by the CC although two label-free tests clear them: own-period lean 0.02-0.21, the same as ordinary columns, and no own-period tail (claim auditor). Meanwhile the four in point 2, which show the mechanism, ship.
- *Remedy (the curator's call).* After point 2, either keep the six dropped and record the fact as an exception (the same block of running aggregates of x, where a label-free test is indirect: precedent checker, option (a)), or restore them with a `Potential leak` note. Do not leave the four in while the six are out.

**6. EV-6, EV-7 (Should): the evidence text overstates its tests.**
- "f527 = (own x + earlier f527) / 2 on 100%" is an identity by construction. Cite instead the test that could fail: the next row's f274 equals x on 97.3% of links.
- "These transactions are all completed" leaves out the same post's first sentence, "There is no after and before". Quote both, add that ids rise along 100.0% of cross-chunk links, and mark "granted" in `task_summary.split` as our reading.
- Record: "f275 = f274^2" holds in only 0.42% of rows, and the `Data Quality Issue` marker is refuted. Fix both at the next record edit.

**7. P7, CLEAN-14 (Should): f6 is a code.**
- The host: "person instructing the loan has the historical relationship". It holds 1,079 arbitrary integers, is equal along entity links in 24.2% of cases against 0.5% at random, and its loss rate has no order in the code (column auditor; domain practitioner).
- *Remedy.* `categorical=["f6", "f776", "f777", "f778"]` and one line in the dtype bullet. This is quality only, not a reason to hold the dataset.

**After the changes.** Re-run the task probes with all the drops together. The drops were measured only one family at a time. TP-2 should still hold, since the two drops cost about 0.003 and 0.010 AUC from about 0.73, but confirm it. Update `changes` and `fit_reason` (USE-8) to name the dropped families.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate: rebuttal to the critic (2026-11-01)**

**Summary.** The critic and I agree on the verdict: ship after changes, with no exclusion. I concede six of its seven points. On point 3 I narrow it to one difference: I prefer adding the gap to recording an exception. One new fact came up. I measured the drops the critic asked for together, and TP-2 holds.

**New fact: the Gini with all 31 columns dropped (27 hindsight + f468, f471, f533, f536), on the 9 shipped windows**
- Setup: the column auditor's untuned LightGBM hurdle (400 trees, n_jobs=2) on the shipped frame with the shipped splits and the shipped `normalized_gini`, one fit per window.

| Window | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Mean |
|---|---|---|---|---|---|---|---|---|---|---|
| Gini, shipped | 0.235 | 0.273 | 0.211 | 0.293 | 0.290 | 0.183 | 0.203 | 0.198 | 0.232 | 0.235 |
| Gini, minus 31 | 0.228 | 0.239 | 0.146 | 0.243 | 0.220 | 0.135 | 0.193 | 0.161 | 0.163 | **0.192** |
| AUC (loss > 0), shipped | 0.742 | 0.727 | 0.739 | 0.746 | 0.723 | 0.717 | 0.716 | 0.730 | 0.719 | 0.729 |
| AUC, minus 31 | 0.732 | 0.712 | 0.726 | 0.730 | 0.708 | 0.700 | 0.704 | 0.719 | 0.709 | **0.715** |

- The drops cost Gini -0.043 and AUC -0.013 on average. The AUC falls on 9 of 9 windows. The Gini stays between 0.135 and 0.243 and is far above the constant's 0 on 9 of 9 windows. The claim auditor puts the noise of a random scorer at an SD of about 0.04. So TP-2 holds: a small real signal, kept.
- I also dropped f615, f617 and f278, the edge of the sweep, on windows 0, 4 and 8. The Gini was 0.181 / 0.229 / 0.184 against 0.228 / 0.220 / 0.163 with them, and the AUC moved by 0.000 / +0.006 / -0.004. Mixed signs, within noise. Score does not decide a leak (LEAK-6, LEAK-10 note), so their fate rests on the timing test the column auditor proposed.
- One limit: my run reproduces the *cost* of dropping the four tail columns, not the label-free tail test that convicts them. The critic's caveat stands. The builder should rerun `tailscan` before the drop.

**Point by point**

1. **LEAK-10, 27-column hindsight family: concede.** It was my point 1 too. What follows: drop the 27 in `_clean` and rewrite the "Potential leak, kept on purpose" bullet as a LEAK-10 drop with the gap table. Fix "its own history (LEAK-34)" in `splits_comment`, and name the family in `changes` and `fit_reason` (USE-8). Correct the line "no change ... passes 0.595" to say that it is about the row's own loss.

2. **LEAK-10, f468/f471/f533/f536: concede**, with the reproduction caveat above. A drop rather than a cap: a cap needs a cut, and a cut fit on all rows brings its own transductive problem (LEAK-30). So the drop is the safe fix, and the measured cost is acceptable within the 31-column total.

3. **SPLIT-10, no gap: concede that the reason is wrong. I narrow the remedy.** The critic prefers no gap, recorded as an exception that states the real fact. I prefer the 5,800-row gap with 5,000-row windows, for two reasons:
   - SPLIT-10 is a Should, so the gap is the default. A departure needs a fact that sets the case apart *and* the higher principle it serves (principles.md, Strengths). The critic's fact is that the term is long against an unknown span. That would serve SPLIT-14 only if the gap broke the floor. A one-window gap does not break it (51.8% on the oldest window). A longer gap, sized to the term, cannot be computed without dates.
   - The gap costs nothing measurable (Gini +0.006, AUC -0.001 on 4 windows), and it removes a departure instead of adding a fourth reason to an amendment-due rule (register flag 10). On the remedy ladder, fixing the definition comes before a note.

   Conceded: a one-window gap is not the true delay either, so either option is defensible. This goes to the curator as a weighing call, with both options in REVIEW.md. Neither may cite lending_club.

4. **MET-11 / MET-2 / MET-10, the metric label, pricing and the RMSE sentence: concede.** It was my point 6. What follows: declare the Gini as `context` naming MAE as the original, as the batch's insurance tables do. Narrow `use_case` to ranking loans for portfolio entry, with the level set by a separate calibration. Reword the RMSE sentence to give both sides: it separates models about as well as the Gini (paired z about 2), but 1% of the rows drive it.

5. **Inconsistent leak drops: concede.** It was my point 2. With the four dropped (point 2), keep the curator's drop of the six as a block exception (precedent checker, option (a)). The fact: these are running aggregates of the same hidden x whose members f527 and f528 carry the outcome's period, and a label-free test is indirect. It serves P4. Restoring the six is the other option, and it is the curator's call. P4's LEAK-10 "may include" (Must) outranks CLEAN-22 (P7), so the drop is defensible. Restoring them moves the score only by noise.

6. **EV-6 / EV-7, the evidence text and the record: concede.** Cite the 97.3% test, not the identity. Quote the host's full answer and mark "granted" as our reading. Fix the record's "f275 = f274^2" and remove the `Data Quality Issue` marker.

7. **CLEAN-14, f6: concede.** Use `categorical=["f6", "f776", "f777", "f778"]` and add one line in the dtype bullet. Quality only.

**"After the changes": done in part.** The combined drop is measured above, and TP-2 holds (Gini 0.192, AUC 0.715, 9 of 9 windows). The builder should still rerun the task probes and `dataset check` on the changed definition, and update the numbers in the notes and the metric reason: the hurdle's 0.236 becomes about 0.19.

**Joint judgment record (proposed)**
Verdict: ship after changes.
Validity: USE-1 holds (approximate fit). LEAK-10 triggered and fixed: f527/f528 and the six as a block exception; 27 hindsight columns and f468/f471/f533/f536 to drop. LEAK-21 holds. SPLIT-1/9/11/14 hold. SPLIT-10: a 5,800-row gap, or an exception with the true fact (curator).
Value: TP-2, a small real signal after all drops (Gini 0.192, 0.135-0.243, 9 of 9). MET-4 overrule; Gini as `context`.
Quality: CLEAN-14, f6 categorical; text fixes (EV-6, EV-7, SPLIT-13).
For the curator: the gap or the exception; the six (block exception or restore); f615/f617/f278 after the timing test; the `use_case` wording.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (2026-11-01)**

**Where we stand.** The advocate concedes every validity point of my brief: the 27-column drop, the drop of the own-period columns, the MET-11 label, the `use_case` wording, the no-gap reason and the text fixes. We now share one verdict: **ship after changes, not as defined.** I ran the one check that could decide a point, the reproduction of point 2 I asked for. It narrows that point by one column.

**My check.** It works on the raw `train_v2.csv` with my own code, and it runs the top/bottom 0.1% own-period test on *every* column, which gives the suspects a control (953 usable tails). Base rates: 73,319 links; among the loss-free links, x changed in the own period 33.3% of the time and in the previous period 38.9%.

| Tail (loss-free linked rows) | Own period changed | Previous changed | Loss rate in tail |
|---|---|---|---|
| f471 top (34) | 1.000 | 0.353 | 59.0% |
| f536 top (27) | 1.000 | 0.407 | 35.8% |
| f468 top (36) | 0.861 | 0.389 | 58.1% |
| f533 top (49) | 0.694 | 0.633 | 28.3% |
| f529 top (39), one of the dropped six | 0.692 | 0.615 | 15.1% |
| f13 bottom (97) | 0.948 | 0.505 | 18.6% |

Only 3 of the 953 tails reach 0.9: f471, f536 and f13. f468 is the next one marked out, at 0.861 against a previous-period rate of 0.389.

**Point by point**

1. **Leak fixed, task kept (advocate 1): agree.** This was my point 1, and the same remedy: drop the 27 columns in the column auditor's list under LEAK-10, with LEAK-6 and the kick precedent. Measure f615, f617 and f278 first, then rewrite the bullet. Nothing to contest.

2. **The four own-period columns (advocate 2): agree for three, narrow for f533.**
   - The column auditor's numbers reproduce exactly for f471, f536 and f468, and those three stand out against every other tail in the file. They go under LEAK-10 (Must).
   - **f533 does not reproduce as a leak on its own.** Its top tail has own 0.694 against previous 0.633, the same profile as f529 (0.692 / 0.615), one of the six that the curator dropped as a precaution. So f533 belongs with the six, not with the measured leaks. Its +65 twin relation to f468 is the block argument, not a measurement (EV-6).
   - Remedy: drop f468, f471 and f536 under LEAK-10. Drop f533 together with the six under one block exception, the precedent checker's option (a), as the advocate proposes. Or restore all seven with a `Potential leak` note. Either way, f533 and the six get the same treatment (CLEAN-22, treating like cases alike).
   - **Also, f13.** The column auditor already listed it as a weak question. In my control scan its bottom tail ranks third of 953 (0.948 own against 0.505 previous; loss rate 18.6% in 177 rows). That is the same signature as f471 and f536, though the column auditor found its size does not follow the ratio of x. Remedy: the builder runs the same check on f13 that convicted the three. If it holds, drop f13 under LEAK-10; if not, name it with these numbers in the leak bullet. I do not ask for the drop on this evidence alone.

3. **iranian_churn refuted; remove the `Data Quality Issue` marker; fix "f275 = f274^2" (advocate 3): concede.** This is the same as my point 6.

4. **TP-2 and the blind reviewer (advocate 4): concede.** My brief made the same call. We also agree on the open item: re-measure the combined Gini and AUC on all 9 windows after every drop, and write the numbers into the notes. The per-family costs (AUC -0.003 and -0.010 from about 0.73) leave TP-2 expected to hold, but that is still unmeasured.

5. **Split and gap (advocate 5): concede the gap.** The advocate's mildest remedy is the rule's default (SPLIT-10, Should): `window=5000, gap=5800`, trained on 51.8%, measured null effect. That removes the departure instead of documenting it, so it ranks above my exception option on the remedy ladder. Either is acceptable; the curator picks. Also agreed: the full host quote and the SPLIT-13 sentence.

6. **Metric (advocate 6): agree.** The overrule of MAE is sound (MET-4 clause, MET-2). Relabel `stand_in` to `context` or a curator overrule (MET-11). State both sides on RMSE. Narrow `use_case` to ranking, or say the Gini ignores the level.

7. **Cleaning (advocate 7): agree.** f6 becomes categorical (CLEAN-14); cast f466 to float64; replace the EV-6 identity with the 97.3% test.

**Judgment record: one amendment to the advocate's version.**
Validity line: "LEAK-10 triggered and fixed: f527/f528; the 27-column predecessor family; f468, f471 and f536 (own-period tail, reproduced by the critic). f533 goes with f529-f531, f534, f535 and f537 as one block (curator's exception or restore). f13 to test."
For the curator, add: whether f533 and the six go as a block or come back.

</details>
