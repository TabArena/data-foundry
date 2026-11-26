---
unique_name: mortgage
name: Mortgage
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Entities: Recur'
- Panel Data
collections:
- New (BeyondArena)
original_source: Website
year: '2016'
collection_period: Apr 2000 - Mar 2015
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- http://www.creditriskanalytics.net/datasets-private2.html
v2_path: datasets/_dev/tabarena-v0pt2/mortgage/dataset.py
source_row: 702
type_adapter_id: curation-record-v1
---

## Comments

Panel data from www.internationalfinancialresearch.org, maybe we can find the source and get more as it is just a " randomized selection"

Determine how to make it a target, as it is not just one target per group

**Assessment (AI, 2026-10-07):** Added as `mortgage`: one row per loan and quarter, target the quarter's status (default, payoff, active), temporal split on the last 3 quarters, as in the book's own backtest on period 60. No larger source exists: International Financial Research was a consultancy whose site is gone. The periods are quarters 2000 Q2-2015 Q1 (Case-Shiller match). The book's models use the quarter's own balance, LTV and macro values; the balance records the event and the macro values come out after the quarter, so we take the loan's previous quarter and the macro values published by then. No HMEQ-style generation artefacts. Licence: textbook use only, no commercial use; the site's terms forbid republishing or redistributing its content.

**Assessment (AI, 2026-10-20):** priority 5 for the review of the added dataset: gap + (problem_type multiclass_classification), use case +, source +, shape +, no known risk. A rare real loan-level multiclass panel with a temporal split that fills the multiclass gap, though the quarter's overall event rate drives much of the score.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; applied: `balance_time_lag_2` added (the balance at the previous-but-one observation; the data has no delinquency field), the last row of the 501 loans that leave early without an event dropped (label not recorded, LEAK-25), the two ids that copy another id dropped (23 rows), the 37.5% placeholder rate masked, and the notes corrected (GDP vintage caveat, the level effect's own reason, re-run numbers). Priority 4: gap + (multiclass_classification), use case + (a holder's quarterly PD scoring, the book's own backtest), source + (the book's data page and codebook), shape + (621,653 loan-quarters, 18 features, temporal), risk - (open: rows scored in the quarter the loan is originated, USE-3, issue 10; the quarter's overall event rate carries 74-83% of LightGBM's gain).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: investor_orig_time.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The book uses the data for many PD/LGD examples with assorted diagnostics (ROC/AUC for binary default, calibration plots), not one metric for this three-outcome task.

CC (2026-10-22, Lennart): issue 2: keep the 3 classes; a binary default-only companion might be reasonable in the future. Issue 10: (a), reword the use case: a loan is also scored in the quarter it joins the book. Issue 11: add the ratio of the two lagged balances. Issue 12: amend CLEAN-13. Issue 14: add the market mortgage rate ("this sounds like a good way to make the data better"). Issue 13: keep both conflicting copies as real data noise we may want to simulate. Issue 15: keep the LTVs above 300% as real data noise of unclear origin.

**Assessment (AI, 2026-10-22):** applied issues 2, 10, 11, 12, 14: `use_case`/`known`/`fit_reason` reworded (8,132 origination-quarter rows kept, 24 in test); `balance_ratio_lag_1_to_2` added; FRED MORTGAGE30US (Freddie Mac, "Copyrighted: Citation Required") averaged per calendar quarter and lagged one quarter as `market_rate_30y_lag_1`, with `rate_minus_market_rate_lag_1`; CLEAN-13 amended for a reference level. Untuned LightGBM, periods 60/59/58: log loss 0.1180/0.1274/0.1293 (0.1201/0.1327/0.1364 without the ratio), default ROC AUC 0.75/0.84/0.81; the market-rate columns move the log loss by under 0.001. dataset check: 0 errors, 0 warnings. Issues 13 and 15 depart from LEAK-20 (jm1) and CLEAN-11 (caracas_cervical_cancer, melbourne) without a fact that sets them apart, so they are back in the review as consistency checks and not applied yet. Not built yet.

CC (2026-10-22, Lennart): issue 13: (b), keep the payoff copy of the 7 doubled period-51 loans, as implemented. Issue 15: (a), make the LTVs above 300% and the conflicting balances missing.

**Exception to LEAK-20 (2026-10-22, Lennart):** for 7 loans period 51 is doubled with only the status differing (active and payoff); the payoff copy is kept instead of dropping both, because all 7 loans end at period 51, so the active copy is damage to the file (PROV-13), not an ambiguous label. Serves P5 (faithful data: the file repaired toward what was recorded).

**Assessment (AI, 2026-10-22):** issue 15 applied: the 38 source balances that put the source's LTV above 300% become missing before lagging, so no `LTV_time_lag_1` above 300% is left (highest 261.4%). Issue 13 as implemented, with the exception recorded. REVIEW.md removed (nothing left open). Not built yet.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `fannie_mae_single_family_loan_performance` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): Review issue 16, B ("Option B: Three years, three seasons."): the test windows are periods 60, 49 and 38 (2015 Q1, 2012 Q2 and 2009 Q3), the calm years, the recovery and the crisis in three different quarters of the year, in place of the three newest quarters.

CC (2026-11-11, Lennart): the declared horizon (one quarter, no gap, windows starting at periods 60, 49 and 38) is checked, as a quarter is the book's own backtest window and the label's own horizon, and the use case scores the book at every quarter's start (Review horizon, ok).

**Assessment (AI, 2026-11-11):** applied issue 16 (B): `temporal` declares `cutoffs=(60, 49, 38)`; test 8,004, 9,431 and 15,921 loan-quarters, train 613,649, 513,686 and 376,900 (98.7%, 82.6% and 60.6%); default / payoff 0.5% / 1.8%, 2.1% / 1.9% and 4.4% / 2.4% in the windows; 99.4%, 99.7% and 99.98% of the test rows' loans have earlier quarters in train; 37 rows of joining loans and 8 of the 501 dropped last rows fall in the new windows. The decision tables follow the cutoffs, and the LightGBM figures of the notes are marked as measured on periods 58 to 60. `dataset check`: 0 errors, 0 warnings.

CC (2026-11-17, Andrej): the declared split (temporal on `time`, windows of 1 value, 3 windows at fixed cutoffs, no gap) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

## Review

**Outcome:** added. You shipped it on 2026-10-26; on 2026-11-11 you chose 2015 Q1, 2012 Q2 and 2009 Q3 as the test
quarters (issue 16, B) and kept the one-quarter horizon (H, ok); both are applied and nothing is left open.

Re-reviewed on 2026-11-26 (focused panel): ship after changes. The standing objection on
the task probes no longer holds, since on the windows shipped on 2026-11-11 the probes raise no flag at all; two
issues are open, one of them a validity question about the container rather than the task (17, the later rows of a
test loan; 18, the origination fields).

**Main points:** Settled on 2026-11-11: one test quarter in each regime the book went through, the calm years, the
recovery and the crisis, with the one-quarter horizon checked.

**Horizon:**

* **Verdict:** keep the one-quarter windows (medium confidence): a quarter is the book's own backtest window and the
  label's own horizon, and the use case scores the book at every quarter's start; no source gives a refit cadence.
* **Length:** the definition cites the book's out-of-time backtest, which fits on the periods before 60 and tests on
  period 60 ("`mortgage[mortgage$time < 60, ]` against `mortgage[mortgage$time > 59, ]`", R Companion, chapter 13, as
  quoted in `splits_comment`); still unverified: no copy of the R Companion was found (web search for the book and its
  companion), and the data page (http://www.creditriskanalytics.net/datasets-private2.html) gives only the files. Each
  row's label is the loan's status at the end of its quarter, so one quarter is also how far ahead the lender looks.
  Refit cadence: none found for this book; banks with internal PD models must "review their estimates when new
  information comes to light but at least on an annual basis" (EU CRR Art. 179(1)(c),
  https://www.legislation.gov.uk/eur/2013/575/article/179), so a model refit once a year and scored every quarter is
  the other common practice.
* **Gap:** none needed: the status of a quarter is known when the next one starts, and every feature is lagged to
  what was published by the quarter's start.
* **Time frame:** periods 1 to 60, 2000 Q2 to 2015 Q1, a closed book that ages, with 1,728 seasoned loans added in
  2013 Q1 (period 52). The 26 quarters from 2008 Q4 (period 35, 51.8% train share) to 2015 Q1 keep half the rows for
  training; they span the crisis (default rates of 4.4% to 5.1% a quarter in 2009), the recovery and the calm of
  2014-2015 (0.5% to 0.9%).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One quarter (implemented) | windows of one period, no gap: 26 candidates above the floor, 2008 Q4 to 2015 Q1 | 3 windows (issue 16's B) of 8,004 to 15,921 loan-quarters | the book's own backtest window and the label's own horizon; the use case scores the book at every quarter's start | no source gives a refit cadence; the backtest quote is still unverified |
  | B | Four quarters | a model refit once a year: 6 candidates above the floor, back to 2009 Q2-2010 Q1 | 6 candidates of 33,328 to 62,004 loan-quarters | one model serves a year, as under an annual review | the book tests one quarter and the use case scores every quarter |
  | C | Two quarters | 13 candidates above the floor | 13 candidates of 16,176 to 37,895 loan-quarters | more loan-quarters per window | no source for it |

* **Recommendation:** A: the book tests one quarter, the label looks one quarter ahead, and the use case scores the book
  every quarter. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, the one-quarter windows without a gap stay. `splits_comment` gives the reason
from this block: a quarter is the book's backtest window and the label's own horizon, and the use case scores the book
at every quarter's start; no source gives a refit cadence, and the backtest quote stays marked unverified. The record
has the horizon CC line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

**Issues for Andrej and Lennart:**

16. **Which quarters should the test windows be?**

   * **Problem:**
     - The three test windows are the three newest quarters (2014 Q3, 2014 Q4 and 2015 Q1), while 26 quarters, from
       2008 Q4 on, keep half the rows for training.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other years, then other seasons, over the quarters just before the newest[^mo-split15].
     - The eligible quarters run from the crisis to the calm years, with default rates from 0.5% to 5.1% a quarter,
       but today's three windows all lie in the calm (0.5% to 0.9%).
   * **Background:** Period 1 is 2000 Q2, so period 60 is 2015 Q1, 49 is 2012 Q2 and 38 is 2009 Q3. The book is a
     closed panel that ages: an older window holds more and younger loans (8,004 in 2015 Q1, 15,921 in 2009 Q3), and
     its train side covers fewer years. The macro columns hold one value per quarter, so every window shows a value
     its train side never had (largest PSI 8.5 to 9.7 in every candidate); the median PSI over the loan columns is the
     drift to read. PSI, the population stability index, compares a feature's distribution in the window with its
     train side; above 0.25 is usually read as a large shift. Option B spaces the windows 11 quarters apart, so they
     fall in three different years and three different quarters of the year.
   * **Statistics:** from the candidate table (100,000-row samples of each side for the drift).

     | Period | Quarter | In | Test rows | Default / payoff, test | Default / payoff, train side | Train share | Median PSI | Largest PSI |
     |---|---|---|---|---|---|---|---|---|
     | 60 | 2015 Q1 | A, B, C | 8,004 | 0.5% / 1.8% | 2.4% / 4.3% | 98.7% | 0.25 | 8.7 |
     | 59 | 2014 Q4 | A | 8,172 | 0.6% / 2.0% | 2.4% / 4.4% | 97.4% | 0.32 | 8.6 |
     | 58 | 2014 Q3 | A | 8,459 | 0.9% / 1.7% | 2.5% / 4.3% | 96.0% | 0.35 | 8.6 |
     | 49 | 2012 Q2 | B | 9,431 | 2.1% / 1.9% | 2.6% / 4.6% | 82.6% | 0.23 | 9.7 |
     | 48 | 2012 Q1 | C | 9,812 | 2.3% / 1.8% | 2.7% / 4.8% | 81.1% | 0.46 | 8.7 |
     | 38 | 2009 Q3 | B | 15,921 | 4.4% / 2.4% | 2.5% / 5.8% | 60.6% | 0.60 | 8.5 |
     | 36 | 2009 Q1 | C | 18,384 | 4.8% / 1.9% | 2.3% / 6.1% | 54.9% | 0.43 | 9.1 |

   * **Effect on the task:** Under A a model is ranked on a seasoned book in three calm quarters, where the default
     rate is a quarter of the train side's and the quarter's overall event rate already carries most of the score
     (curation notes). B adds a recovery quarter close to the train side's level and a crisis quarter whose default
     rate is almost twice the train side's, a quarter a lender's model has to get through.
   * **Consistency:** Every option keeps period 60, the book's own backtest quarter[^mo-split19]. No dataset has chosen
     windows in a crisis under the rewritten rule yet; numerai_v5_2_1m keeps its newest years for a reason mortgage
     lacks (the features were built on the older eras).
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/mortgage/dataset.py` (`splits_comment`, `temporal`);
     the record `curation/records/mortgage.md`; the candidate table `.venv/bin/python -m data_foundry.curation.cli
     dataset windows mortgage --root datasets/_dev/tabarena-v0pt2` (30 windows listed, 26 above the floor).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest three quarters (implemented) | tests 2015 Q1, 2014 Q4 and 2014 Q3 | the book's backtest quarter and the two before it; the most training data (oldest 96.0%) | three calm quarters in a row; nothing of the crisis or the recovery |
     | B | Three years, three seasons | tests 2015 Q1, 2012 Q2 and 2009 Q3 | the calm, the recovery and the crisis; three different quarters of the year; spread over the 26 candidates | the oldest trains on 60.6% and on a younger book |
     | C | Three first quarters | tests 2015 Q1, 2012 Q1 and 2009 Q1 | three years three years apart | one season only; the oldest trains on 54.9% |

   * **Recommendation:** B: it spreads the windows over the eligible history in other years and other seasons, as the
     rule prefers, and puts one window in each regime the book went through, while each train side keeps at least
     60.6% of the rows. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="time", splits=TemporalSplits(window=1, unit="unique",
   cutoffs=(60, 49, 38)), horizon=1, horizon_unit="steps", time_unit="quarters")`: test 8,004, 9,431 and 15,921
   rows, train 613,649, 513,686 and 376,900 (98.7%, 82.6%, 60.6%). On C, `cutoffs=(60, 48, 36)`: test 8,004, 9,812
   and 18,384 rows, train 613,649, 503,874 and 341,354 (98.7%, 81.1%, 54.9%). Then rewrite `task_summary.split`,
   `splits_comment` (the windows, the reasons and the numbers above; recount the share of test rows whose loan has
   earlier quarters in train, today 99.4-99.9%), the windows table in `_decisions` (`df["time"] >= 58`), and the
   curation notes that quote LightGBM numbers for periods 60 / 59 / 58 (mark them as measured on the earlier
   windows); add a CC line to the record and a dated CHANGELOG entry, and run `dataset check` (SPLIT-15).

   [^mo-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^mo-split19]: **SPLIT-19** (Should): "When the source defines the split (a competition's or a paper's official
     periods), follow it."

   **Lennart (2026-11-11, change):** Option B: Three years, three seasons.

   **Resolved (2026-11-11, Lennart):** B. `temporal` declares `cutoffs=(60, 49, 38)`: test 8,004, 9,431 and 15,921
   loan-quarters, train 613,649, 513,686 and 376,900 (98.7%, 82.6%, 60.6%). `task_summary.split` and `splits_comment`
   name the windows and rest the spread on the three regimes (default / payoff 0.5% / 1.8% in 2015 Q1, 2.1% / 1.9% in
   2012 Q2, 4.4% / 2.4% in 2009 Q3), with the recounted share of test rows whose loan has earlier quarters in train
   (99.4%, 99.7%, 99.98%). The decision tables follow the cutoffs (the balance table by test period, the windows table,
   the macro table), the notes count 37 rows of joining loans and 8 of the 501 dropped last rows in the new windows
   (one row of the copied ids would fall in period 38), and the LightGBM figures are marked as measured on periods 58
   to 60. The record has the decision CC line. `dataset check`: 0 errors, 0 warnings.

17. **A test row's later quarters are in the shipped frame, and they say whether it defaulted. Accept with a note, or stop each split's frame at its test quarter?**

   * **Problem:**
     - The status is terminal, so a loan stops having rows once it defaults or pays off: of the 559,032 rows that are not a loan's last one, 559,026 are `active`.
     - The container holds one frame of all sixty quarters and names the splits as positions, so for a test quarter in the middle of the panel every test row's later quarters sit in the frame, and the mere existence of a later row says the label is `active`.
     - It needs no label and no loan key: the dropped identifier rebuilds from the static columns, and a test row's `balance_time_lag_1` reappears as some row's `balance_time_lag_2` one quarter later.
   * **Effect on the task:** Two of the three windows can be scored almost perfectly without a model. The newest window is immune because nothing follows it, which is also what shows the mechanism is the later rows and not something else.
   * **Experiments:**

     | Test quarter | Honest log loss | With the later rows | Change |
     |---|---|---|---|
     | 60, the end of the panel | 0.11855 | 0.11855 | none, the control |
     | 49 | 0.17886 | 0.02476 | -86% |
     | 38 | 0.27554 | 0.03225 | -88% |

     | Keyless form | Purity |
     |---|---|
     | a test row's lagged balance reappearing one quarter later, test quarter 38 | 99.4% |
     | the same, test quarter 49 | 99.9% |

   * **Background:** How far it reaches was checked in the benchmark code. A model handed only the training rows and the test rows cannot see it, and no later row ever trains a split. But the worked example builds its features over the whole frame before slicing, which is the sanctioned pattern, so a per-loan row count or a "does this loan appear later" column reaches it without anyone intending to; a column of that kind was added by hand and the gain above came back.
   * **Consistency:** The mechanism is not particular to this dataset. It belongs to any temporal task whose test windows sit inside the history rather than at its end, and it bites hardest where the target is survivorship-shaped, so that a later row of the same unit exists only when no event has happened. A cross-dataset item asks whether the container should ship a frame per split at all.
   * **Panel:** The split auditor measured entity leakage through the earlier rows and found it null, which is right: a loan's earlier rows are always `active`, so no label travels forward. The task gamer attacked the other direction and found the channel runs backward from the future.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept with a note | a clause in the splits comment and the record giving the mechanism and the numbers above | costs nothing; the plain fit path is already clean; the chosen windows stay | a feature built over the whole frame reaches it by accident, and the rule rests on participants' discipline |
     | B | Ship a frame per split that stops at its test quarter | removes the channel; no honest score changes | the only complete fix; it is also how a lender sees the book | the container holds one frame today, so this needs container support and changes the design for every temporal dataset |
     | C | Put every test window at the end of the panel | shrinks the channel | needs no new machinery | only one window can be last, so quarters 59 and 58 still have successors; it gives up the crisis and recovery windows chosen on 2026-11-11 |
     | D | Leave it as it is (implemented) | nothing changes | no work | the mechanism stays undocumented and a participant can use it in good faith |

   * **Recommendation:** A now, with the cross-dataset item deciding B for the whole family, since B is infrastructure rather than a change to this dataset. If you would rather have a guarantee here and not a convention, B is the only option that gives one. **Decision:** A, B, C or D?

   **Notes for the AI:** under A, the clause goes in `splits_comment` and a dated assessment line in the record, and the cross item goes into the working copy's `REVIEW.md`. Under B or C the windows are rebuilt and it is its own pull request.

18. **Freeze the origination fields within each loan, or keep them as recorded?**

   * **Problem:**
     - `Interest_Rate_orig_time` is documented as fixed at origination but changes within 2,313 loans, and on 3,108 of the 3,269 changed rows the new value is the row's own-quarter rate, the very value the definition lags everywhere else.
     - Whether the field is filled also moves with the outcome: its missing flag flips within 1,401 loans, and on those flip rows the payoff rate is 7.95% against 2.52% on the other rows of the same loans.
     - The same revision happens to `mat_time` (959 rows), `FICO_orig_time` (382), `LTV_orig_time` (18) and the property-type flags (1,123 rows, where a property changes type mid-life, which cannot happen).
   * **Effect on the task:** 24,190 rows carry a value different from the loan's first recorded one, 2,520 of them in the test windows, and those rows hand the model a number from inside the quarter it is predicting.
   * **Experiments:**

     | Window | Log loss, freezing the origination fields |
     |---|---|
     | 60 | -0.0003 |
     | 49 | -0.0006 |
     | 38 | -0.0003 |

   * **Background:** The notes settle this today on the size of the score: "freezing them changes the log loss by -0.0001 to -0.0002, so they stay". The measurement above says freezing is slightly better, so the fix costs nothing either way.
   * **Panel:** The column auditor reads it as a leak decided on the wrong ground, since the rule on values known at the prediction point is a Must and asks the timing to decide rather than the score. The claim auditor reads a measured-harmless suspect as needing only a clause. The mediator settles it for the column auditor: the late cells can be located row by row, which is exactly when the rule requires the fix rather than a note.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Forward-fill all of them within the loan from the first recorded value, and take the loan's first property type | removes the own-quarter values and the moving missing flag, and repairs the impossible mid-life property change | the mildest fix; scores slightly better | the shipped columns change, so the generated page and the note are rewritten |
     | B | Freeze the interest rate only | the column where the evidence is strongest | the smallest change | the other fields are revised on the same mechanism, and a term modification is an event booked inside the quarter |
     | C | Keep as recorded, with a clause naming the rows (implemented) | today's behaviour plus a sentence | no change to the data | decides a Must on the size of a score, when the fix is free |

   * **Recommendation:** A. The rows can be named, the remedy is the mildest one available, and the measurement removes the only argument for keeping them. **Decision:** A, B or C?

   **Notes for the AI:** the counts differ between the two audits (3,269 changed rows, 3,872 own-quarter rows before propagation, 2,703 in the current note, 3,540 loans). Settle one definition before writing the clause or the fix.

**Review panel:** ship after changes (mediator, focused tier: claim auditor, column auditor, split auditor, task gamer). Claims: the calendar anchor, the macro lags, the market rate, the target's absorbing form, the dedup and the LEAK-20 exception all survive tests designed to refute them. Refuted: the standing objection on the probes is stale and the dataset is better than its notes claim; "a closed book that ages" describes the wrong panel. Agreed: the one-quarter windows without a gap, and that entity leakage through earlier rows is null. Disputed: the later rows (issue 17) and the origination fields (issue 18).

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
