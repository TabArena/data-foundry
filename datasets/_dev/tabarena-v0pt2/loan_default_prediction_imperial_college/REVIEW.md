# loan_default_prediction_imperial_college

**Outcome:** added. The AI recommends shipping it; the panels' changes are made (second and third paragraphs). Kaggle's
"Loan Default Prediction - Imperial College London" (2014): 105,471 loans of an unnamed lender in time order,
anonymised features, the target the loss given default, a scaled number from 0 to 100 (0 for 90.7%; per 100 of the
loan's amount in our reading); a lender ranks new loans by expected loss to choose which enter a portfolio. Validity:
SEL holds; USE-1 holds, fit approximate (anonymised fields, no dates); LEAK-10 triggered and fixed three times: the
golden features f527/f528, a family of 28 columns that record the entity's previous loan's loss after the fact (f221
gives it at ROC AUC 0.993 even when that loan was granted 1-10 loans earlier), and f468, f471, f536, whose top values
record the loan's own period; f533 goes with the six aggregates as one block (issue 1, settled); LEAK-38: f615, f617
and f13 tested and kept with a `Potential leak, kept on purpose:` note (f615/f617 give the previous loan's loss well
only when it lies far back, as history would; f13's low values follow the own period as a smooth gradient, like
ordinary columns); LEAK-21 holds (a loss does not end a chain, unlike iranian_churn); LEAK-41 holds (no weight, no
denominator, no column set after the grant); SPLIT-1, 9, 11 and 14 hold; SPLIT-10 met by a 5,800-loan gap (issue 2,
settled). Value: a small real signal after all drops (TP-2: normalized Gini 0.196, 0.146 to 0.230, above 0 on 9 of 9
windows; a loss ranked at ROC AUC 0.69-0.73 on the 9 windows); the task probe's `no_signal` and `unstable` flags read
R^2 (LightGBM -0.012), while on the declared Gini LightGBM scores 0.158 and beats the dummy on 5 of 5 splits; MAE
overruled because predicting 0 beats every model trained on the loss (MET-2, MET-4), the Gini declared from context
under MET-11 as amended (issue 3, settled); MET-14 not triggered (the decision is per loan), MET-15 holds (scored per
loan, unweighted; no amount released), MET-16 does not apply. Quality: f6, the host's "person instructing the loan",
typed categorical (CLEAN-14); -1 at the bottom of nine columns kept as a value, not a missing code (CLEAN-10). Weighed:
size and a real lending decision +; anonymised fields and a small signal -.

Changes made after the review panel of 2026-11-01: the 28-column family, f468, f471, f536 and f533 dropped (LEAK-10); a
gap of 5,800 loans with 9 windows of 5,000 loans; the metric declared `context` instead of `stand_in`; `use_case`
narrowed to ranking loans for portfolio entry (the Gini cannot see a price level); f6 categorical; the evidence text
corrected (the host's full quote, the circular f527 test replaced). The numbers here and in the issues are re-measured
on the changed definition (untuned LightGBM, one fit per window); that panel's are from before the changes. For the
record: the wrong "f275 = f274^2" is corrected and the `Non-IID (Temporal)` tag added at hand-over; we propose removing
the `Data Quality Issue` marker, since the concern behind it (the iranian_churn chain pattern) is refuted; it stays
until your mark (issue 4).

Changes made on 2026-11-06 and 2026-11-08 (AI, under the exposure rules; re-reviewed on 2026-11-08 by a focused panel
once the competition's files were in): an exposure bullet in the notes. The host ships the target as a "scaled number
between 0 and 100"; that it is a share of the loan's amount is marked as our reading there and in
`task_summary.predicted`, and the sentence that scoring per loan equals a portfolio of equal notionals rests on that
reading. Either way the decision is per loan, the source's MAE is unweighted and no amount is released, so no weight is
declared; the planned term varies by a factor of 1 to 3 and ships only as the maturity-range code f4, and an annual
rate over a loan's realized life would bring back the cut-time leak (LEAK-41), so the lifetime rate stays. The check
warning for -1 in nine columns is accepted: -1 is a change of -100%, and it predicts the loss differently from missing
(f648: 14.4% against 8.5%). The metric reason adds that the Gini also leans on the tail (the 1% of loans with the
largest losses hold 38-46% of a window's loss sum, against 71-82% of RMSE's squared error).

**Main points:** Open: none. Settled on 2026-11-08: issue 4, the record's `Data Quality Issue` marker removed (the chain
pattern it stood for is refuted, the leak columns are dropped). Issues 1 to 3 are settled (Andrej, 2026-11-03).

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

4. **Remove the record's `Data Quality Issue` marker, now that the chain pattern it stands for is refuted?**

   * **Problem:**
     - The record set the marker for the chain pattern (the screening of 2026-10-27: it "stays as the open
       concern"), the leak columns being the screening's other risk, and the review panel found both settled.
     - A `Yes` record carries no decision marker unless an open concern remains[^ld4a].
     - The panel proposed removing it on 2026-11-01, but the proposal never reached a board, so the marker stayed.
   * **Background:**
     - The chain pattern, the marker's concern: rows that are one loan's snapshots up to default (96.5% of defaults are
       the last row of an f274 block), the pattern that retired iranian_churn. The panel refuted it, as a chain's last
       row has a loss as often as its other rows (9.42% against 9.38%), so a loss does not end a chain.
     - The screening's other risk, ex-post columns: the host removed nine columns mid-competition, and `f528 - f527`
       alone still ranked a loss at ROC AUC 0.92; f527, f528 and the block f529-f531, f533-f535, f537 are dropped
       (Andrej, 2026-11-03, issue 1, A).
   * **Panel:** the re-review of 2026-11-08 measured both again, and both auditors' data support B: `f528 - f527` ranks
     a loss at ROC AUC 0.916 on the raw file and none of the dropped columns ships; a chain's last row has a loss in
     9.42% of cases against 9.38%, and the screening's 96.5% is a base rate, since runs of equal f274 in file order are
     almost all one row long (99.9% of the loans with a loss and 99.3% of the others end a run). No remaining risk is
     damage that cannot be undone or repaired.
   * **Effect on the task:** none on the data, the split or the score: the marker lives only in the record, where it
     reads as an unresolved quality problem of a dataset that ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the marker (implemented) | nothing changes | none found | flags a settled concern on a shipping record |
     | B | Remove the marker | the record's `decision_markers` lose it; a CC line names the refuted chain pattern and the dropped leak columns | the record says what holds | none found |

   * **Recommendation:** B: the chain pattern is refuted and the leak columns are dropped, so no open concern
     remains. **Decision:** A or B?

   **Notes for the AI:** on B, remove `Data Quality Issue` from `decision_markers` through the store API, a CC line
   naming the refuted chain pattern and the dropped leak columns, and `validate`.

   **Lennart (2026-11-08, change):** Option B: Remove the marker.

   **Resolved (2026-11-08, Lennart):** B: the record's `Data Quality Issue` marker is removed, with a CC line naming the settled chain pattern and the dropped leak columns.


   [^ld4a]: records.md, `decision_markers`: "Issue flags ...; a clean dataset has none". selection.md, `Data Quality
     Issue`: "damage that cannot be undone or repaired".

**Review panel:** ship after changes (mediator), wording and one accepted warning, now made. Tier focused, a re-review
of 2026-11-08 under LEAK-41, MET-14 to MET-16, after the raw data arrived: the claim auditor, the column auditor and the
mediator; no blind review, task gamer, advocate or critic in this tier. Claims: 19; 15 hold (1 with a caveat: the Gini
also leans on the tail, now a clause in the metric reason), 1 unsupported as worded (the host's "notional of 100", now
marked as our reading), 1 partly refuted (issue 4's "two concerns", corrected in the issue), 1 holds in part (`f2` is
no amount; "no amount is released" is untested on anonymised fields), 1 not refuted with little power (every feature
known at the grant). Blind review: not part of this tier. Agreed: -1 in nine columns is a value, not a missing code
(the check warning accepted with that reason); LEAK-41 holds; MET-14 is not triggered (a per-loan decision), MET-15
holds, MET-16 does not apply; no new issue. Disputed: nothing; issue 4 stays open for you, and both auditors' data
support its B. This block replaces the panel of 2026-11-01, which issues 1 to 3 cite; that panel is in this file's git
history.

<details><summary>Mediator</summary>

**Mediator: loan_default_prediction_imperial_college (focused re-review, 2026-11-08)**

Inputs: the change note, the claim auditor's and the column auditor's reports, the task and leak probes (probe 22
empty: no weight ships, correctly), dataset.py, REVIEW.md, the record. No advocate, critic or task gamer ran (focused
tier); no precedent-checker report, so precedent was checked by hand against the working copy.

**1. Judgment record**

- Verdict: ship after changes (wording and one accepted warning; no change to data, split, metric or weight).
- Validity: LEAK-41 holds (no weight, no denominator, no cut-time column; f2/f4/f5 are ex-ante loan terms); LEAK-10
  fixes of earlier panels hold (none of the dropped columns in the frame; f528-f527 AUC 0.916 on raw); leak probe:
  all features R^2 -0.055, 0.0% of 45,000 test rows with a training copy, probe 13 no censoring (\|z\| < 3); SPLIT-10,
  11, 14 hold as settled.
- Value: TP-2, a small real signal (task probe: LightGBM normalized Gini 0.158, beats the dummy on 5 of 5 splits; a
  loss ranked at ROC AUC 0.70-0.71); MET-13 holds; MET-14 not triggered (per-loan decision, see 2c); MET-15 holds
  (per-loan, unweighted; no amount released, so no weight could be declared); MET-16 not applicable.
- Quality: CLEAN-10 holds: -1 in nine columns is a value, kept; the new warning is accepted with that reason.
- Weighed: unchanged (size and a real lending decision +; anonymised fields and a small signal -).
- For the curator: issue 4 only (already open in REVIEW.md; both auditors' evidence supports B). No new issue.

**2. Points settled**

a. dataset_missing_value_sentinel (CLEAN-10, Should; EV-2: a measurement outranks a reading). Not disputed. Both
auditors measured independently and agree: -1 is the floor of each column (nothing below, values from -0.99 up),
every column has its own NaN (1.7-8.5%), and -1 carries a loss rate different from NaN (f648 14.4% vs 8.5%; f72
7.4% vs 8.3%; others 9.5-9.7%); f648/f649 run smoothly into -1 (12.6% in (-1,-0.9]); -1 is not tied to missing
history (67.8% vs 70.2% have a previous row). The source does not name -1 as missing, so CLEAN-10's condition
("inferred from the description and the context") is not met, and its second sentence (keep a code that means
something) applies. Converting would merge two states and lose information. Remedy: accept the warning with a reason.

b. Exposure paragraph, "the host scaled every loan to a notional of 100" (EV-2, EV-7 wording; MET-14's "the notes say
so"). Not disputed. The only host words are "loss = loss given default = scaled number between 0 and 100" (topic
6862). "Notional" / "share of the loan's amount" is our reading; LGD is conventionally a share of the exposure at
default. The conclusion does not move: whatever the base, no amount ships, the decision is per loan (MET-15's
per-loan clause), and the source's MAE is unweighted. Remedy: reword, mark the reading as ours; the sentence
"scoring per loan equals a portfolio of equal notional slices" becomes conditional on that reading.

c. MET-14 wording (column auditor). Not a conflict. MET-14 (Should) applies "when the decision prices or maps per
unit"; the use_case was narrowed (curator-accepted) to ranking loans for portfolio entry by lifetime expected loss,
a per-loan decision, so the rule is not triggered and its constant-term clause is not needed. A per-year rate is
also not buildable: the realized life is not released (and would be LEAK-41's cut-time leak), and the planned term
is only a maturity-range code (f4). Remedy: one clause in the exposure bullet. Correction to the column auditor's
wording: f4 is the host's "maturity ranges", a range code, not the planned term itself; write "the planned term
varies by a factor of 1 to 3 (host) and ships only as a maturity-range code, f4".

d. Issue 4 (SEL, records.md decision_markers). Already open; not duplicated. Both auditors support B with data
(concern 1 dropped, f528-f527 AUC 0.916 on raw; concern 2 refuted, last-row loss rate 9.42% vs 9.38%, the
screening's 96.5% a base rate of length-1 f274 runs; no remaining risk is "damage that cannot be undone"). One
wording fix to the issue's text (see 3.4); the recommendation stands.

e. Gini tail caveat (claim auditor, MET-10/EV-9, Should). The top 1% of loans hold 38-46% of a window's loss sum, so the
Gini also leans on about 50 loans per window, though less than RMSE (71-82%); a perfect occurrence oracle scores
0.94-0.95 and a pure P(loss) model 0.08-0.10 against 0.158 on the loss. Does not reopen issue 3 (metric settled);
one clause in the metric reason makes the comparison fair.

**3. Changes to make now (no decision needed)**

1. accepted_check_warnings (CLEAN-10): add
   "dataset_missing_value_sentinel": "-1 in f72, f586-f588, f648-f651, f763 is the bottom of a relative change (-100%),
   not a missing code: no value below it, values from -0.99 up, each column has missing values of its own, and -1
   predicts the loss differently from missing (f648: 14.4% vs 8.5%; f72: 7.4% vs 8.3%) (CLEAN-10)."
   Optionally the same loss-rate contrast in the notes' "Missing values stay missing" bullet.
2. Exposure bullet in the notes (EV-2, EV-7; MET-14, MET-15): replace "the host scaled every loan to a notional of
   100" with the host's words ("loss given default = scaled number between 0 and 100", topic 6862) plus "that it is a
   share of 100 of the loan's amount, rather than of the exposure at default, is our reading"; make the equal-notional
   sentence conditional on that reading; add "the planned term varies by a factor of 1 to 3 (host) and ships only as a
   maturity-range code (f4); the decision ranks loans by lifetime loss, so no per-year rate is needed (MET-14)".
3. task_summary.predicted (EV-2): "as a percentage of the loan's amount" -> "a scaled number from 0 to 100 (the host);
   a percentage of the loan's amount in our reading". The record's "a percentage of the notional" (line ~108) gets the
   same mark at the next record edit.
4. REVIEW.md issue 4, Problem, first bullet (EV wording): "set the marker for two concerns" -> "set the marker for the
   chain pattern, with the f528-f527 leak listed as a risk". The Main points line names issue 4 twice (first and last
   sentence); keep one.
5. Metric reason (MET-10, EV-9; optional): one clause that the Gini also leans on the tail (top 1% of loans hold 38-46%
   of a window's loss sum), next to RMSE's 71-82%.
6. CHANGELOG.md entry for the edited definition (house rule).

**4. Issues for the curator**

None new. Issue 4 (remove `Data Quality Issue`) stays open in REVIEW.md; this panel adds measured support for B
(see 2d). Nothing here reopens issues 1-3.

**5. Agreed facts**

- Target integers 0-100, 90.72% zero, median 5 among losses; host words: "scaled number between 0 and 100".
- Source metric MAE, unweighted (Kaggle API); predicting 0 scores MAE 0.730-0.846 (mean 0.800) on the 9 windows.
- Container: sample_weight None, no scoring columns, metric inputs {}; constant scores 0, oracle 1 on all 9 folds.
- -1 floor in nine columns, 7.5-11.9% of rows, own NaN 1.7-8.5%, loss rates at -1 differ from NaN (above).
- f2: 10 integer codes 1-11 (size cluster), not an amount; f4/f5 ex-ante range codes; f6, f778 correctly categorical.
- Leak probe clean (R^2 -0.055; best single feature 0.001; 0 copies); best single-column AUC for a loss 0.635 (f766).
- Splits: 9 windows of 5,000, gap 5,800, training share 51.8%-89.8%, 461-527 losses per window.
- Issue 4's concerns: f528-f527 AUC 0.916 on raw, all dropped; chain last-row loss rate 9.42% vs 9.38%.

**6. Consistency with precedent**

- -1 kept as a value with the warning accepted: same as home_credit_default_risk (POS_MONTHS_BALANCE_MAX = -1) and
  home_credit_default_stability_1m (avgdbd\* -1), and bank_marketing (pdays = -1 kept as a meaningful code). Differs
  from house_sales (yr_renovated 0 -> missing), where the source defined the code as "never" and missing had no other
  meaning; here the columns already have their own missing values and -1 is undefined by the source. Consistent.
- No weight, per-loan unweighted metric: consistent with MET-15's per-loan clause; differs from fremtpl2, bemtpl97,
  australian_vehicle_insurance_2004_2005 (realized exposure released, pricing per year). The fact that sets it apart:
  no exposure or amount is released and the decision is per loan.
- Per-contract target despite a varying term: spanish_motor_insurance_2015_2018 kept per contract under a constant
  term; here the term varies, but MET-14 is not triggered (per-loan decision, no denominator released). No precedent
  decided a per-loan lifetime loss the other way.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: loan_default_prediction_imperial_college (focused re-review, 2026-11-08)**

**Verdict: ship.** No validity claim refuted. One wording claim unsupported (the "notional of 100" in the exposure
paragraph); the -1 sentinel warning is a value, not a missing code, and should be accepted with a reason; issue 4
(remove `Data Quality Issue`) is supported by the data: B.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Exposure: "the host scaled every loan to a notional of 100, so the target is a lifetime loss rate per 100 of notional" | notes, Exposure paragraph; task_summary.predicted "share of a new loan's amount" | read the quoted source words; Kaggle discussion pages do not render (WebFetch title only), web search finds no host text on notional | UNSUPPORTED as worded (conclusion holds) | the only host words quoted: "loss = loss given default = scaled number between 0 and 100" (topic 6862). LGD is conventionally a share of the exposure at default, not of the original amount; "notional" and "loan's amount" are our reading, not the host's. Target: integers 0-100, 90.72% zero, median 5 among losses (measured) | EV (evidence wording), MET-14 |
| 2 | "Scoring per loan equals a portfolio of equal notional slices ... so no weight is declared" | notes, Exposure | container: sample_weight None, scoring_columns [], metric inputs {} | HOLDS | unweighted per-row Gini; MET-15's per-loan clause; no amount column is released, so no weight could be declared anyway | MET-15, MET-16 |
| 3 | "matches the source's MAE" (unweighted) | notes, Exposure | Kaggle API | HOLDS | evaluation_metric "Mean Absolute Error", unweighted per row | MET-4 |
| 4 | "No amount is released, and f2 is a size-cluster code, not an amount" | notes, Exposure | f2's values | HOLDS for f2; "no amount" UNTESTED (anonymised) | f2: 10 integer codes 1-11 (no 5); a cluster code cannot rebuild an amount | LEAK-41 |
| 5 | "An annual rate over the realized life would bring back the cut-time leak" | notes, Exposure | reasoning | HOLDS | a realized life ends at default or payoff, set after the prediction point; no such column ships | LEAK-41 |
| 6 | -1 at the bottom of f72, f586-f588, f648-f651, f763 (7-12%) is no missing code; those columns have missing values of their own and values from -0.99 up | notes, "Missing values stay missing"; CHANGES (new warning dataset_missing_value_sentinel) | per column: share at -1, NaN share, values just above -1, loss rate at -1 / NaN / other, co-occurrence | HOLDS | -1 7.46%-11.87%; NaN separately 1.75%-8.54% in every column; nothing below -1; min above -1 = -0.99 (f763 -0.9912). P(loss): f72 block at -1 7.2-7.4%, at NaN 8.3-8.4%, others 9.5-9.6%; f588 5.3% vs 8.4% vs 9.7%; f648/f649 14.4%/14.2% vs 8.5% vs 8.6-8.7%. f648/f649 run continuously into -1 (3.5-3.9% of rows in (-1,-0.9]) with a monotone loss gradient (14.4% at -1, 12.6% in (-1,-0.9], 10.5% in (-0.9,-0.5]). In the f72 block -1 is a joint event (indicator correlations 0.85-1.00 among f72, f586, f587, f650, f651, f763): a shared base quantity going to 0, i.e. a change of -100%. Making -1 missing would merge two states with different loss rates | CLEAN-10 ("keep a code and say why when it means something"), CLEAN-11 |
| 7 | Issue 4, concern 1 settled: f528-f527 ranked a loss at ROC AUC 0.92; f527, f528 and the block f529-f531, f533-f535, f537 dropped | REVIEW.md issue 4; notes | raw AUC; columns absent from the container | HOLDS | f528-f527 AUC 0.916 on raw; none of the 9 aggregates, 28 hindsight columns, 3 tails or 9 copies are in the frame | LEAK-10 |
| 8 | Issue 4, concern 2 refuted: a chain's last row has a loss as often as its other rows (9.42% vs 9.38%); 70.3% of losses have a later row | REVIEW.md issue 4; notes | rebuilt _period_links on raw | HOLDS | 73,319 links; last rows 9.423% (n 19,453) vs other chain rows 9.380%; 70.30% of losses have a later row. The screening's "96.5% of defaults are the last row of an f274 block" is a base rate: runs of equal f274 in file order are almost all length 1 (1.26% of rows in longer runs), 99.9% of losses and 99.3% of non-losses end a run | LEAK-21, SEL |
| 9 | Issue 4: "the screening set the marker for two concerns" | REVIEW.md issue 4, Problem | record's screening text | PARTLY REFUTED (wording) | the record names only the chain pattern as the reason the marker "stays as the open concern"; the f528-f527 leak is listed as a risk with "a drop is the likely call". Does not change the recommendation | EV |
| 10 | Issue 4: no other concern remains that fits `Data Quality Issue` ("damage that cannot be undone or repaired: a supervised transform fit on the whole labelled set, a manipulated real table", selection.md) | implied by recommendation B | the notes' remaining risks against that definition | HOLDS | the remaining risks (standardisation/de-trending over train+test, maturity clustering) are unsupervised and carried by the `Anonymized` tag (LEAK-32); probe 16 finds no min-max sign; the leak probe finds no single column above noise; the best single column ranks a loss at AUC 0.635 (f766; notes say 0.633 on 15,000 rows) | SEL, LEAK-32, records.md decision_markers |
| 11 | Metric: competition metric MAE (Kaggle API "Mean Absolute Error") | metric reason, notes | Kaggle API competitions_list | HOLDS | evaluation_metric "Mean Absolute Error"; the earlier audit's untested item (evaluation page) now settled through the API | MET-1, MET-4 |
| 12 | Metric: predicting 0 scores MAE 0.800 on the 9 windows | metric reason | MAE of zeros per window | HOLDS | 0.730-0.846, mean 0.800 | MET-2, MET-4 |
| 13 | Metric computable on every fold; 0 for a constant | metric reason; MET-2 | scorer on each of 9 test folds with a constant and an oracle | HOLDS | constant 0.000 and oracle 1.000 on all 9; 461-527 losses per window; no scoring columns needed | MET-2, MET-13 |
| 14 | "RMSE: the largest 1% of the errors hold 71-82% of its sum of squares" (implied: the Gini is less tail-driven) | metric reason | share of the loss sum held by the top 1% of loans per window (the Gini's cumulative-share weights) | HOLDS, with a caveat | the top 1% of loans (50 per window) hold 38-46% of the loss sum, so the Gini also leans on about 50 loans per window, but far less than RMSE. A perfect occurrence oracle (1 for any loss) scores 0.941-0.951, so the Gini mostly rewards finding losses; a pure P(loss) LightGBM (AUC 0.70-0.71) scores only 0.076-0.097, against 0.158 for LightGBM on the loss (task probe) and 0.196 for the hurdle (notes): the size stage matters | MET-2, MET-10 |
| 15 | "a loss is ranked at ROC AUC 0.69-0.73" | notes, task-probe note | LightGBM classifier on windows 0, 4, 8 | HOLDS | 0.706, 0.699, 0.704 | TP-2 |
| 16 | Splits: 9 windows of 5,000, gap 5,800, oldest trains on 51.8%, newest on 89.8%; 461-527 losses; newest window's mean 0.813 within 0.730-0.846 | splits_comment, notes | splits | HOLDS | train max time_index 94,671 / test min 100,472 (gap 5,800) etc.; n_train 54,671-94,671 of 105,471 (51.8%-89.8%); means 0.730-0.846, newest 0.813; leak probe 13 finds no newest period outside \|z\| 3 | SPLIT-10, SPLIT-11, SPLIT-14 |
| 17 | "No two rows share a feature vector" (implied: no copy across the split) | notes | hash of the shipped feature vectors; leak probe | HOLDS | 0 duplicate vectors; probe: 0.0% of 45,000 test rows with a training copy | LEAK-16 to LEAK-21 |
| 18 | Every feature known at the prediction point (implied) | task_summary.known | leak probe (R^2), single-column AUC screen | NOT REFUTED (limited power) | leak probe: all features R^2 -0.055, best single column 0.001; the probe reads R^2, which large losses drive, so it has little power here; my AUC screen for loss>0 tops at 0.635 (f766, f404 0.634, f629 0.626), no outlier. fit_reason already says "others may remain" | LEAK-10, LEAK-32 |
| 19 | No training weight or weight-like column ships (LEAK-41, MET-16) | implied by the new rules | container | HOLDS | sample_weight None; no survey/design weight in the source; probe 22 not applicable (p22 folder empty, correctly) | LEAK-41, MET-16 |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. (Should, evidence wording; Exposure paragraph and task_summary.predicted) "the host scaled every loan to a notional
   of 100" is not what the quoted host words say ("loss given default = scaled number between 0 and 100"). Changes:
   nothing on the data, split, metric or weight (MET-15 leaves a per-loan decision unweighted, and no amount ships).
   Mildest remedy: reword to "the host ships the loss given default as a scaled number between 0 and 100; that it is
   the share of 100 of the loan's amount (rather than of the exposure at default) is our reading", and mark "share of
   a new loan's amount" in task_summary.predicted as our reading the same way.
2. (Should, quality; the change note's new warning) `dataset_missing_value_sentinel` is neither accepted nor fixed. The
   data support keeping -1 (claim 6). Mildest remedy: add the warning to `accepted_check_warnings` with the reason in
   one sentence (-1 is a change of -100%, distinct from the columns' own missing values and with its own loss rate:
   7.2-7.4% against 8.3-8.4% at missing, 14.2-14.4% in f648/f649).
3. (Wording, REVIEW.md issue 4) "the screening set the marker for two concerns": the record ties the marker to the
   chain pattern only. Remedy: "for the chain pattern, with the f528-f527 leak listed as a risk". Recommendation B
   stands.
4. Untested: "no amount is released" (anonymised columns; f2 is a 10-level code and cannot be an amount). Nothing to
   change.
5. Caveat, not a refutation (metric): the Gini also leans on the tail (top 1% of loans hold 38-46% of a window's
   loss sum) and mostly rewards finding the losses. Worth one clause in the metric reason next to RMSE's 71-82%; no
   change of metric.

Issue 4: both concerns hold as settled (f528-f527 AUC 0.916 on raw, all dropped; last-row loss rate 9.42% vs 9.38%,
and the screening's 96.5% statistic is a base rate of length-1 f274 runs); no remaining risk fits selection.md's
definition of `Data Quality Issue`. Supports B (remove the marker).

</details>

<details><summary>Column audit</summary>

**Column auditor: loan_default_prediction_imperial_college (focused re-review, 2026-11-08)**

**Verdict: ship.** No new leak, no cleaning problem. One bookkeeping change: accept the new
`dataset_missing_value_sentinel` warning with a reason (it is not in `accepted_check_warnings` today, so it will fire
on every check). One wording suggestion for the exposure note (MET-14). The earlier panel's column table (the panel of
2026-11-01, in this file's git history) still holds. Only the rows touched by today's questions are repeated below.

Inputs: cleaned frame from dataset_io.load(..., built=False): 105,471 rows, 638 features, plus time_index and loss.
Probes: the leak probe (finished: all features R^2 -0.055, best single feature 0.001, no copies across the split,
probe 13 finds no censoring at the release end), the task probe, and the dtype probe (rerun by me).

**1. -1 in nine columns (f72, f586, f587, f588, f648, f649, f650, f651, f763): a value, not a missing code**

| col | -1 share | own NaN | min | next above -1 | rows in (-0.99,-0.9] | loss rate at -1 / other / NaN |
|---|---|---|---|---|---|---|
| f72 | 8.7% | 8.5% | -1 | -0.99,-0.98,-0.97 | 19 | 7.4% / 9.6% / 8.3% |
| f586 | 8.1% | 8.5% | -1 | -0.99,-0.98,-0.97 | 17 | 7.4% / 9.6% / 8.4% |
| f587 | 8.1% | 8.5% | -1 | same | 17 | 7.4% / 9.6% / 8.4% |
| f588 | 7.5% | 8.0% | -1 | same | 291 | 5.3% / 9.7% / 8.4% |
| f648 | 10.3% | 8.2% | -1 | same | 4,107 | 14.4% / 8.7% / 8.5% |
| f649 | 11.9% | 8.3% | -1 | same | 3,718 | 14.2% / 8.6% / 8.5% |
| f650 | 8.0% | 8.5% | -1 | same | 16 | 7.4% / 9.6% / 8.3% |
| f651 | 8.7% | 8.5% | -1 | same | 19 | 7.4% / 9.6% / 8.3% |
| f763 | 7.5% | 1.7% | -1 | -0.9912,-0.991 | 23 | 7.2% / 9.5% / 6.9% |

No value is below -1 in any of the nine. No other numeric column has an exact -1 in more than 1% of its rows.

Evidence it is a value:

- -1 is the lower bound of each column's range, not a code outside it. The values run continuously from -0.99 up to
  94-14,170, with medians near 0, so these behave like relative changes (x_t/x_{t-1} - 1). On that reading -1 means
  the quantity fell to 0. Nothing below -1 exists, which a sentinel placed outside the range would not explain.
- Each column also has its own NaN (1.7-8.5%). NaN and -1 carry different loss rates (f648: NaN 8.5%, -1 14.4%;
  f72: NaN 8.3%, -1 7.4%). Turning -1 into NaN would merge two states that predict the loss differently. That loses
  information (CLEAN-10's "keep a code and say why when it means something"; CLEAN-12, lossless).
- For f648/f649 the -1 continues a smooth gradient: 4,107 / 3,718 rows sit just above it, and the loss rate falls
  steadily (f648: 14.4% at -1, 12.6% in (-1,-0.9], 10.5%, 8.1%, 7.4%). That is the floor of a continuous variable.
- f72/f586/f587/f650/f651/f763 show a point mass at -1 with an almost empty band just above it (16-23 rows). This is
  what a ratio whose numerator hits exactly 0 produces. A "no data" code would have to be tied to missing history, and
  it is not: rows at -1 have the entity's previous row in 67.8% of cases against 70.2% for the other rows (f763
  69.6/69.9). The NaN rows are the ones that lack history more often (64.4%; f763 51.2%).
- The -1 cases co-occur in two families that match the columns' correlation blocks: {f72, f586, f587, f650, f651, f763}
  share 80-100% of their -1 rows (Spearman between them 0.49-0.96), and {f648, f649} 86-100%. f588 sits between the
  two. Each block reads as related ratios of one underlying quantity that went to 0. A file-wide missing code would
  hit every block together, but only 0.46% of rows have -1 in all nine columns.
- f72's -1 share drifts over the file (4% -> 17% -> 5% across id deciles) like a business cycle, and so does a real
  quantity. f648's share stays flat (9.7-11.9%).
- The source does not name -1 as missing (the host's field notes, topic 6978). CLEAN-10 converts a proxy only "when
  the encoding can be inferred from the description and the context", and here it cannot.

Rule and remedy: CLEAN-10 is not triggered, so -1 stays (the earlier panel's finding holds and is now measured on the
data). Mildest remedy: add the warning to `accepted_check_warnings`, for example: "dataset_missing_value_sentinel":
"-1 in f72, f586-f588, f648-f651, f763 is the bottom of a relative change (-100%), not a missing code: no value below
it, values from -0.99 up, each column has missing values of its own, and -1 predicts the loss differently from missing
(f648: 14.4% vs 8.5%) (CLEAN-10; precedent home_credit_default_risk)." Optional: the notes' "-1 reads as a change of
-100%" could add the NaN-vs--1 loss-rate contrast as its evidence.

**2. LEAK-41, MET-14, MET-15, MET-16, MET-13 under the new rules**

- LEAK-41: holds. No column is a weight or a rate's denominator. The notional is not released (the host scaled every
  loan to 100), and no sample weight or weight scoring column is declared. The candidate encoders of size or term are
  f2 (size cluster, 10 levels 1-11), f4 (maturity range) and f5. The host names all three as ex-ante loan terms, so
  they are set at the prediction point. A feature known at the start that predicts risk stays (USE-6). Nothing is set
  or cut after granting: probe 13 shows no censoring at the release end, and the dropped hindsight columns are
  LEAK-10's, already settled.
- MET-14: holds, with one wording gap. The target is already a rate per unit of the amount at risk (loss per 100 of
  notional, folded in by the source; the notes say so as the amended clause asks). Time on risk varies: the host
  says terms "vary by a factor from 1 to 3". MET-14's per-contract clause speaks of a constant planned term, but here
  the decision unit is the loan's lifetime expected loss per notional (EL = PD x LGD x EAD, the practitioner's
  number). The planned term is known at granting and ships as f4, which meets LEAK-41's "a part known at the start
  ships as its own column". A per-year rate would need the realized life, which is not released and would be LEAK-41's
  cut-time leak. Suggestion: the exposure bullet should say in one clause that the planned term varies 1-3x and ships
  as f4, so a reader sees why the constant-term clause is not needed.
- MET-15: holds. The decision is per loan (ranking loans for portfolio entry), so the rate is scored unweighted with
  no sample weight, which matches the rule's "per loan or per contract" sentence. With equal notionals of 100, a
  notional weight would be constant anyway.
- MET-16: not applicable (no survey or design weight).
- MET-13: normalized_gini is in the library; a Gini needs no floor.
- CLEAN-16 (amended): the target is a whole number from 0 to 100 on the identity scale, scored by a Gini, so it is not
  transformed. Nothing to change.

**3. Column table (rows touched today; the rest as in the panel of 2026-11-01)**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| loss | lifetime loss per 100 of notional, 0 = no default or full recovery | target | int64 0-100, identity scale | fine | MET-14, CLEAN-16 |
| time_index | source id, time order | yes (order) | int, time column only | fine | SPLIT |
| f72, f586, f587, f650, f651, f763 | anonymised; relative-change-like, from -1 up; one block | undetermined (anonymised); no hindsight sign in the earlier tests | float64; -1 kept as a value, own NaN kept | fine | CLEAN-10 |
| f588 | same, between the two blocks | as above | as above | fine | CLEAN-10 |
| f648, f649 | same, second block; smooth floor at -1 | as above | as above | fine | CLEAN-10 |
| f2 | size cluster (host), 10 levels | yes, ex-ante | int, numeric ordered | fine; not an amount, not a weight | LEAK-41, CLEAN-14 |
| f4, f5 | maturity range; ease-of-transaction ranking | yes | numeric ordered | fine; f4 carries the planned term | LEAK-41, MET-14 |
| f6 | person instructing the loan; 1,079 codes | yes | category (dtype probe: numeric_levels) | fine: arbitrary codes, settled | CLEAN-14 |
| f778 | region; 64 codes | yes | category (dtype probe: numeric_levels) | fine: a nominal region code | CLEAN-14 |
| f776, f777 | collateral full/partial; gradual/bullet | yes | category 0/1 | fine | CLEAN-14 |
| the other ~620 anonymised columns | unknown | the host says ex-ante; the dropped ones were tested | float64 | unchanged since the last panel | - |

Dtype probe: 2 of 638 flagged, f6 and f778 (numeric_levels). Both are correct as categorical codes.

**Problems, ranked (principles.md: validity before value before quality)**

1. Quality/bookkeeping: `dataset_missing_value_sentinel` is not accepted, so the check keeps warning. Remedy: one
   `accepted_check_warnings` entry with the evidence above (CLEAN-10). No data change.
2. Clarity: the exposure bullet does not say that the term varies (1-3x) or that f4 carries the planned term. Remedy:
   add one clause (MET-14, LEAK-41).

No leak and no validity issue is new under LEAK-41 or MET-14 to MET-16. Issue 4 (removing the `Data Quality Issue`
marker): nothing in the columns argues against it.

</details>
