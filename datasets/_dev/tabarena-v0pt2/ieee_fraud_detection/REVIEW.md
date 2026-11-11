# ieee_fraud_detection

**Outcome:** added. Under the rule on choosing test windows, rewritten on 2026-11-10, the AI proposes three windows of
three weeks (30 March to 31 May 2018) with the competition's one-month gap, in place of the months March, April and
May 2018, whose March window trains on 38.9% of the payments (issue 1). `dataset.py` is unchanged until you decide.

**Main points:** Test three windows of three weeks from 30 March to 31 May 2018, keeping the one-month gap, instead of
March to May, so every train side keeps half the payments (issue 1)?

**Horizon:**

* **Verdict:** change to three-week windows, keeping the one-month gap (medium confidence): the competition sets the gap
  but no window length, and with six months of labelled payments the gap leaves about ten weeks of windows that keep
  half the payments for training, room for three windows of three weeks but not of a month.
* **Length:** declared one calendar month. The notes take it from the first-place team, who validated with
  "GroupKFold training validation data splitting, with ordered months as non-overlapping groups"
  (https://developer.nvidia.com/blog/leveraging-machine-learning-to-detect-fraud-tips-to-developing-a-winning-kaggle-solution):
  a validation scheme, not how long Vesta uses a model. The competition scores one model on six months, July to
  December 2018 (506,691 payments in its unlabelled `test_transaction.csv`). Vesta's refit cadence: none found (the
  first-place team's write-up, the host's labelling comment the notes quote; the Kaggle discussion pages do not load
  without a browser). Vesta decides on each payment as it arrives, so the length only says how long one fitted model
  serves.
* **Gap:** one month, the competition's: its labelled payments end on 31 May 2018 and its test starts on 1 July 2018.
  A fraud label waits for the cardholder's chargeback, which Visa accepts up to 120 days after a card-absent payment
  (reason code 10.4, https://chargebacks911.com/chargeback-reason-codes/visa/10-4-card-absent-environment/), so the
  gap is shorter than the longest delay; a longer gap leaves fewer than three windows that keep half for training.
* **Time frame:** payments from 1 December 2017 to 31 May 2018, dated from the assumed start day of 30 November 2017;
  December holds 137,321 payments, the other months 83,655 to 101,632. Half the payments lie before 22 February 2018,
  so with the gap a window keeps half for training from about 22 March on; today's March window starts three weeks
  earlier.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One month, one-month gap (implemented) | calendar-month windows a month after the train side: only April and May keep half the payments for training (March trains on 38.9%) | 3 windows of 83,655 to 101,632 payments (March under the floor) | the month of the winners' validation; the competition's gap | two windows above the floor, not three; the month comes from a validation scheme, not from how long Vesta uses a model |
  | B | Three weeks, one-month gap | three-week windows over the ten weeks open from about 22 March: three above the floor, 30 March to 31 May 2018 (52.9% to 75.9%) | 3 windows of 58,731 to 61,405 payments | the competition's gap; three separate windows above the floor | no source gives three weeks; 179,939 test payments instead of 274,613 |
  | C | Two weeks, one-month gap | five windows of about 40,000 payments | 5 candidates above the floor, 37,693 to 44,653 payments each | the competition's gap; five windows | more windows than the three a task of this size gets |
  | D | One month, no gap | March to May 2018, training on 53.5% to 84.9% | 3 windows of 83,655 to 101,632 payments | keeps the months; every train side above half | each model trains on labels a month fresher than the competition allows |

* **Recommendation:** B: it keeps the competition's gap and fits three windows above the floor into the ten weeks open,
  and the one-month length rested on the winners' validation, not on how long Vesta uses a model. **Decision:** A, B, C
  or D?

**Issues for Lennart:**

1. **Which test windows should replace March, April and May 2018?**

   * **Problem:**
     - The three test windows are March, April and May 2018, each trained on the payments up to one month before it,
       and the March window trains on 38.9% of the payments, under the half every train side must keep[^if-split14].
     - With six months of labelled payments and the competition's one-month gap, only windows from about 22 March on
       keep half the payments for training, about ten weeks, which hold two one-month windows, not three.
     - The newest window always stays and the others are chosen from the use case and statistics of the data, while
       the length and the gap come from the source[^if-split15][^if-split12].
   * **Background:**
     - The one exception to the floor, an older window on at least 40% of the rows when two windows are above the
       floor and most test entities recur, does not fit: March trains on 38.9%, and only 15% to 17% of the test
       payments carry a client key seen in training (the record's check of 2026-10-01).
     - B keeps the gap and shortens the windows to three weeks, so they cover 30 March to 31 May back to back. C keeps
       one-month windows and starts the middle one on 16 April, so the windows overlap and the payments of 16 April to
       15 May are tested twice. D keeps the three months and drops the gap the competition set[^if-split19].
     - The fraud share is 3.1% to 4.0% in every candidate and 3.3% to 3.5% on the train sides; the December peak lies
       in every train side, and no candidate holds a holiday.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. `day`, a running count of days, drifts in every window and is left
       out; the next largest is `D10` (days since an anonymised event of the card), 1.1 to 1.8. In every candidate
       alike, 51% to 66% of the test payments carry a category the train side never shows.
   * **Statistics:** rows from all payments; the fraud shares and the drift from 100,000-row samples of each side.

     | Window | Gap | In | Test payments | Fraud, test | Fraud, train side | Train share | Largest PSI besides `day` |
     |---|---|---|---|---|---|---|---|
     | 1-31 May | 1 month | A, C | 89,326 | 3.5% | 3.5% | 70.7% | 1.28 |
     | 11-31 May | 1 month | B | 58,731 | 3.8% | 3.5% | 75.9% | 1.26 |
     | 20 Apr-10 May | 1 month | B | 59,803 | 3.1% | 3.4% | 64.4% | 1.30 |
     | 16 Apr-15 May | 1 month | C | 86,031 | 3.1% | 3.3% | 62.4% | 1.31 |
     | 1-30 Apr | 1 month | A, C | 83,655 | 3.4% | 3.4% | 53.5% | 1.37 |
     | 30 Mar-19 Apr | 1 month | B | 61,405 | 3.5% | 3.3% | 52.9% | 1.34 |
     | 1-31 Mar | 1 month | A | 101,632 | 4.0% | 3.3% | 38.9% | 1.79 |
     | 1-31 May | none | D | 89,326 | 3.5% | 3.5% | 84.9% | 1.10 |
     | 1-30 Apr | none | D | 83,655 | 3.4% | 3.4% | 70.7% | 1.05 |
     | 1-31 Mar | none | D | 101,632 | 4.0% | 3.3% | 53.5% | 1.44 |

   * **Effect on the task:** A scores one of its three windows with a model fit on December and January only. B scores
     three back-to-back windows of about 60,000 payments, each model fit up to a month before its window as in the
     competition, and each scored on payments one month to seven weeks after its training ends (one to two months
     under A). D's models train on labels up to the window's start, which the competition's gap keeps from them.
   * **Consistency:** The gap follows the competition, as the definition does today. california_house_prices_2020
     moved its oldest window from 25% to 50% of the rows (2026-10-21); medical_facility_operational_data took its
     window length from its source (2026-11-05); the only overlapping windows were ghana's (3-day windows moving by 2
     days, since retired). No dataset has chosen windows under the rewritten rule yet; delivery_eta_1m's issue 1 is
     open.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/ieee_fraud_detection/dataset.py` (`temporal`,
     `splits_comment`, the horizon and gap bullets of `curation_comments`); the record
     `curation/records/ieee_fraud_detection.md` (no earlier call on the windows; the client-key check of 2026-10-01);
     the candidate tables `.venv/bin/python -m data_foundry.curation.cli dataset windows ieee_fraud_detection --root
     datasets/_dev/tabarena-v0pt2` (3 windows) and the same with `--window 21 --unit days --gap 1 --gap-unit months`
     (3 windows above the floor).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | March to May, one-month gap (implemented) | tests 1-31 Mar, 1-30 Apr and 1-31 May 2018 | the month of the winners' validation; the competition's gap | the March window trains on 38.9%, under the floor |
     | B | Three weeks, one-month gap | tests 30 Mar-19 Apr, 20 Apr-10 May and 11-31 May 2018 | every train side keeps at least 52.9%; the competition's gap; separate windows over all ten weeks open | windows of three weeks, not a month; 179,939 test payments instead of 274,613 |
     | C | One month, overlapping | tests 1-30 Apr, 16 Apr-15 May and 1-31 May 2018 | keeps the month and the gap; every train side keeps at least 53.5% | the payments of 16 April to 15 May are tested twice, so the windows are not separate evaluations |
     | D | One month, no gap | tests March, April and May 2018 trained up to each window | keeps the months; every train side keeps at least 53.5% | drops the competition's gap; models train on labels not yet known at the window's start |

   * **Recommendation:** B: it keeps the competition's gap and three separate windows above the floor over the ten
     weeks open, and the one-month length rested on the winners' validation, not on a deployment cadence.
     **Decision:** A, B, C or D?

   **Notes for the AI:** on B, `temporal = Temporal(on="Transaction_date", splits=TemporalSplits(window=21,
   unit="days", gap=1, gap_unit="months", cutoffs=("2018-05-11", "2018-04-20", "2018-03-30")))`. Built with
   `window_bounds` on the definition's frame: test 58,731, 59,803 and 61,405 payments, train 447,995, 380,100 and
   312,574 (75.9%, 64.4%, 52.9%). On C, `TemporalSplits(window=1, unit="months", gap=1, cutoffs=("2018-05-01",
   "2018-04-16", "2018-04-01"))`: test 89,326, 86,031 and 83,655, train 417,559, 368,632 and 315,927 (70.7%, 62.4%,
   53.5%). On D, `TemporalSplits(window=1, unit="months", cutoffs=("2018-05-01", "2018-04-01", "2018-03-01"))`: test
   89,326, 83,655 and 101,632, train 501,214, 417,559 and 315,927 (84.9%, 70.7%, 53.5%). Then rewrite
   `task_summary.split` ("Each of March, April and May 2018 is a test month") and `task_summary.changes`, the two
   `curation_comments` bullets on the horizon and the gap ("forecasting horizons of 1 month", "a planning window of
   one month") and `splits_comment` (the windows, the reasons and the numbers above), add a CC line to the record and a
   dated CHANGELOG entry, and run `dataset check` (SPLIT-14, SPLIT-15).

   [^if-split14]: **SPLIT-14** (Must): "A temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data. ... A release with two windows above the floor may add one older window that trains on at
     least 40% of the rows, when most test entities recur (the actor re-rates entities it knows) and folds by entity
     would test unseen ones."
   [^if-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Every choice stays
     above SPLIT-14's floor; the length and the gap come from SPLIT-12."
   [^if-split12]: **SPLIT-12** (Should): "The horizon is a human judgment from the source: how far ahead the actor
     predicts ..., the competition's own test window, the refit cadence. Choose the test windows to match it and write
     the reasoning down."
   [^if-split19]: **SPLIT-19** (Should): "When the source defines the split (a competition's or a paper's official
     periods), follow it."
