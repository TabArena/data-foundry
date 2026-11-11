---
unique_name: ieee_fraud_detection
name: IEEE-CIS_Fraud_Detection
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
decision_markers:
- Data Quality Issue
- Anonymized
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Target: Revised Later'
- 'Entities: Recur'
collections:
- TabArena Reject
original_source: Kaggle
year: '2019'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/ieee-fraud-detection
notebook_path: datasets/beyond_iid/temporal/ieee_fraud_detection/ieee_fraud_detection.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ieee_fraud_detection/dataset.py
source_row: 745
type_adapter_id: curation-record-v1
---

## Comments

CC: "Very nice fraud detection dataset (the best one I know). Requires temporal split - although the competition winners used grouped split (by month)"

"The TransactionDT feature is a timedelta from a given reference datetime (not an actual timestamp)."

" discussed the benefits of classifying clients (credit cards) instead of transactions in Kaggle's Fraud competition" -> need to make group structure part of the data by finding UIDs as well

Note: Possible data quality issue: The data is also grouped, but the group identifier is not explicitly given

CC (2026-10-01, Lennart): Leak audit, kept as is. The engineered `uid` (card1 + addr1 + D1 anchor, from the 1st-place Kaggle solution) carries labels across the temporal split: the host labels a chargeback card and its later linked transactions as fraud, so test rows whose uid had fraud in train are about 95% fraud (15-17% of test rows have a uid seen in train). This is legitimate history under the host's labelling rule, not a leak, and it is worth little: dropping uid moves LightGBM AUC by -0.007 to -0.001 (0.911 -> 0.903 on split 0, 0.908 -> 0.907 on split 1), and dropping uid plus the row-ID/time proxies (TransactionID, day, date) gives 0.906. The Data Quality Issue marker (uid is not given by the host) stays.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: V1, V14, V41, V65, V88, V107 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: V1, V14, V41, V65, V88, V107 stay numeric (anonymized Vesta features).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area under the ROC curve (https://www.kaggle.com/competitions/ieee-fraud-detection/overview/evaluation).

CC (2026-10-27, Lennart): marker Anonymized, from the AI review of PR #17: the definition carries the Anonymized data tag; Vesta masked most fields (V1 to V339, C, D, M and id_ columns, card1 to card6), so their meaning and timing cannot be checked one by one (LEAK-32 names this case).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): TransactionID dropped: a row number in time order, an identifier (CLEAN-3).

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Vesta's competition), shape +, risk 0 (the open issue is the window length and the floor).

CC (2026-11-11, Lennart): REVIEW issue 1 (which test windows), as implemented (A): the test windows stay March, April and May 2018, one month each after the competition's one-month gap, in place of the AI's three-week windows; SPLIT-14 as amended on 2026-11-11 admits March, which trains on 38.9% of the payments (one window under half, two above). The windows walk back from the newest: with the gap a February window would train on December only (about 23%).

CC (2026-11-11, Lennart): the declared horizon (one month, a one-month gap, windows starting 2018-05-01, 2018-04-01 and 2018-03-01) is checked, as the month comes from the first-place team's month groups and the gap from the competition (labelled payments end on 31 May 2018, its test starts on 1 July 2018).

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=1, unit="months", n_windows=3, gap=1`); test 89,326, 83,655 and 101,632 payments (May, April, March 2018), train 417,559, 315,927 and 229,906 (70.7%, 53.5%, 38.9% of 590,540); a February window would train on the 137,321 payments of December (23.3%). `task_summary.split`, `splits_comment` and the two `curation_comments` bullets that called the month a forecasting horizon and the gap a planning window now say the month is the winners' validation group, not a refit cadence (Vesta states none; the competition scores one model on six months), and give the gap's source and the Visa chargeback limit of 120 days. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-11, Andrej): the marks of the review of 2026-11-04 applied (its issues 2 and 3; its issues were merged into this record's review on this date, its issue 1 as issue 5).
- Issue 2 ("Option B: State the label's delay"): the gap bullet of the curation notes, `splits_comment` and the task summary give the gap's reason as the chargeback delay (Visa allows the issuer up to 120 days for a card-absent chargeback, and the host then marks the client's later linked payments), with the final labels at the release end (fraud 3.1% to 4.0% a week in May 2018) and the competition's own 30-day layout as the length; it is not a planning window.
- Issue 3 ("Option B: Add Target: Revised Later"): the record's `tags` carry `Target: Revised Later` after `Target: Varying Delay`; both mechanisms are in the source.
- `dataset check` (Slurm job 1378336): 0 errors, 0 warnings, 2 info (heavy checks skipped over the cell budget).
- The split row ("As we discussed.") and issue 1 ("Agree. I follow your suggestion. Document it carefully"): the mark repeats the note of 2026-11-06 and chooses three-week windows, which Lennart's mark of 2026-11-11 (three calendar months, admitted by the amended floor) contradicts. **Not applied**: the split-row mark names the same three-week windows (the answer of 2026-11-04, quoted in the `Resolved` turn of 2026-11-09), and both were read before the floor was amended on 2026-11-11; the definition keeps the three months and the choice is issue 4, open. What both agree on, the one-month gap and its reason, is written down.

## Review

**Outcome:** added. Vesta's online card payments from the IEEE-CIS Kaggle competition (2019): 590,540 payments,
December 2017 to May 2018, 3.5% fraud, where fraud is a charged-back card and the later payments linked to it by
account, e-mail or billing address (the host's rule); the definition adds the first-place solution's client key
(`uid`). On 2026-11-11 Lennart kept the three test months, March, April and May 2018, with the one-month gap (issue 1
and the horizon, A), which the amended floor admits with March training on 38.9% of the payments; the review of
2026-11-04, merged in on 2026-11-11, had chosen three-week windows instead (issue 5), so the length is open again as
issue 4. The gap's reason, the chargeback delay, and the record's `Target: Revised Later` are applied (issues 2
and 3).

**Main points:** Open: the test windows, where issue 1 (three months) and issue 5 (three weeks) disagree and issue 4
puts the choice. Settled on 2026-11-11: the declared horizon is checked, the month from the winners' month groups and
the gap from the competition; the gap's reason is the chargeback delay, written into the definition (issue 2); the
record carries `Target: Revised Later` beside `Target: Varying Delay` (issue 3).

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

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, one calendar month with the competition's one-month gap, kept, in place of the
AI's three-week windows: the month comes from the first-place team's month groups ("ordered months as non-overlapping
groups"), the gap from the competition (labelled payments end on 31 May 2018, its test starts on 1 July). The amended
floor of 2026-11-11 admits the March window (issue 1), so three windows of a month fit. The notes no longer call the
month a forecasting horizon: `curation_comments`, `task_summary.split` and `splits_comment` say it is the winners'
validation group, not a refit cadence (Vesta states none, and the competition scores one model on six months), and
give the gap's reason. `temporal` is unchanged. The record has the horizon CC line. `dataset check`: 0 errors, 0
warnings (README not regenerated).

**Issues for Andrej and Lennart:**

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

   **Lennart (2026-11-11, ok):** As implemented (A).

   **Resolved (2026-11-11, Lennart):** A, as implemented: the test windows stay March, April and May 2018, one month
   each after the one-month gap. SPLIT-14 as amended on 2026-11-11 admits them: May and April train on 70.7% and 53.5%
   of the payments, and March on 38.9%, above 30% and one window under half against two above. The windows walk back
   from the newest because six months of payments leave no other choice: with the gap a February window would train on
   December only (137,321 payments, 23.3%). `temporal` is unchanged; `task_summary.split` and `splits_comment` name the
   three months, their 89,326, 83,655 and 101,632 test payments, the train sides of 417,559, 315,927 and 229,906, the
   March window under half with its share, the month's source (the winners' month groups) and the gap's (the
   competition); the two `curation_comments` bullets on the horizon and the gap say the same. The record has the
   decision and the horizon CC lines. `dataset check`: 0 errors, 0 warnings (README not regenerated).

   **Andrej (2026-11-11, discuss):** Agree. I follow your suggestion. Document it carefully

   **Answer (AI, 2026-11-11):** the mark repeats the note of 2026-11-06 on the earlier review's windows question
   (issue 5), where "your suggestion" is three-week windows with a one-month gap, so it and this issue's mark of the
   same day choose different windows.

   * The three months stay in the definition for now; the choice between them and the three weeks is issue 4.
   * Documented as asked, and independent of the length: the gap's reason is the chargeback delay, now written into
     the gap bullet of `curation_comments`, `splits_comment` and the task summary (issue 2), and `Target: Revised
     Later` is on the record (issue 3).
   * The window bullet and `splits_comment` already give each window's test payments, fraud share and train share,
     the month's source and why the windows walk back from the newest.

2. **Give the one-month gap its reason, the label's delay, instead of "a planning window"?**

   * **Problem:**
     - The definition explains its gap as "a planning window of one month" taken from the competition's layout, while its reason in the data is the label's delay: a payment becomes fraud only once its card is charged back, up to 120 days later.
     - The release holds every label as finally known (fraud 3.1% to 4.0% a week in May 2018, as in earlier months), so without a gap a refit would train on frauds nobody had reported yet.
     - Rewrite the gap's line with this reason, or keep the wording?
   * **Background:** a planning gap is set only where the source says so ("Unless the original paper says so, we should go with no planning gap", Andrej, 2026-11-02, on noaa_afsc_bottom_trawl_survey_cpue), while a gap for a late label is set where the delay is documented and the release does not cover it[^2a]. Read as a planning gap, the line invites removing it, which issue 1's runs show lifts the score by about 0.026 (ROC AUC 0.930 against 0.904). The label also travels forward along the client, so the gap holds back the carried labels too.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the wording (implemented) | "The competition test data left a planning window of one month, so do we." | no change | names a reason the curator's rule would remove, not the one that holds |
     | B | State the label's delay | the gap's line, `splits_comment` and the task summary's `changes` give the chargeback delay and the final labels at the release end | the gap's reason is the one the data shows; it holds for whichever window issue 1 picks | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, replace the curation bullet "The competition test data left a planning window of one month, so do we." with "- Gap (2026-11-06): the label arrives late. A payment counts as fraud once its card is charged back, which Visa allows up to 120 days after the processing date, and the host then also marks the client's later linked payments. The release holds the final labels (fraud 3.1% to 4.0% a week in May 2018, as in earlier months), so only a gap keeps out the labels a refit could not have known; the competition's own test file starts 30 days after its training file."; in `splits_comment`, "leave 1 month as the planning gap" becomes "leave <the gap of issue 1> for the chargeback delay"; the task summary's `changes` says "a gap for the chargeback delay". Under issue 1's option E (no gap) the line says instead that the training labels include frauds not yet reported at the refit. No time-basis tag.

   [^2a]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose outcome is known by the window's start, with a gap of about the label's delay; a planning gap the use case has is a gap too. **SPLIT-12** (Should): the horizon follows the source, such as the competition's own test window.

   **Resolved (2026-11-09, Andrej):** B, state the label's delay. The curation note "The competition test data left a
   planning window of one month, so do we." is replaced by a `Gap:` note: one month, for the label's delay (a chargeback
   up to 120 days after the payment, the final labels in the release, the competition's test file 30 days after its
   training file). `splits_comment` leaves 1 month "for the chargeback delay", and the task summary's `split` and
   `changes` name the gap the same way. The gap is issue 1's, one month; no time-basis tag.

   **Andrej (2026-11-11, change):** Option B: State the label's delay.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: the gap bullet of `curation_comments` is a
   `Gap:` note giving the chargeback delay (up to 120 days under Visa's card-absent reason code), the labels carried
   forward along the client, the final labels at the release end (fraud 3.1% to 4.0% a week in May 2018) and the
   competition's own 30-day layout as the length, and it says the gap is not a planning window; `splits_comment` and
   the task summary's `split` and `changes` name the gap the same way. The gap stays one month, whichever windows
   issue 4 settles on. `dataset check` (Slurm job 1378336): 0 errors, 0 warnings, 2 info (the duplicate-row and
   pure-value checks skipped over the cell budget, as before).

3. **Correct the record's collection facts: add `Target: Revised Later` for the labels carried forward along the client?**

   * **Problem:**
     - The record tags the target `Target: Varying Delay` (the chargeback comes weeks after the payment), but a payment's label is also set later by another payment: the host marks "transactions posterior to it" with a linked account, email or billing address as fraud too.
     - `Target: Revised Later` is the fact for a label "assigned, then updated or propagated", and 98.7% of the payments after a client's first fraud are fraud (issue 1's answer of 2026-11-04).
     - Add it next to `Target: Varying Delay`, replace that tag with it, or keep the record as is?
   * **Background:** the collection facts describe the source, true whatever task is built on it[^3a]. The records' field list gives the three target facts joined by "or", so whether two may stand together is not settled; both mechanisms are in this source, and the carried labels are what makes the client key carry test labels (kept as the client's own history, Lennart, 2026-10-01).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | `Target: Varying Delay` only | the delay that sets the gap | the forward carry along the client is not recorded |
     | B | Add `Target: Revised Later` | both target facts | both mechanisms of the source recorded | two target facts on one record, which the field list does not foresee |
     | C | Replace with `Target: Revised Later` | the carry only | one target fact | loses the chargeback delay, the reason for the gap |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, add `'Target: Revised Later'` to the record's `tags` after `'Target: Varying Delay'`, with a `CC (<date>, Andrej):` line; if two target facts are not allowed, the curator's answer settles it for every record and goes into the records reference.

   [^3a]: **SPLIT-32** (Should): the curation record describes the source by independent collection facts: `Target: Later`, `Target: Varying Delay` (after a delay that differs between samples: a settlement, a chargeback, a follow-up) or `Target: Revised Later` (assigned, then updated or propagated).

   **Resolved (2026-11-09, Andrej):** B: `'Target: Revised Later'` added to the record's `tags` after
   `'Target: Varying Delay'`, in this working copy and in PR #50's copy of the record, with a CC line. Both target
   facts stand: the chargeback delay and the labels carried forward along the client.

   **Andrej (2026-11-11, change):** Option B: Add Target: Revised Later.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: the record's `tags` carry
   `Target: Revised Later` after `Target: Varying Delay`. Both target facts stand: the chargeback comes weeks after
   the payment, and the host then marks the client's later linked payments as fraud too.

4. **Monthly test windows (issue 1) or the three weeks of the earlier review (issue 5)?**

   * **Problem:**
     - Issue 1 was settled on 2026-11-11 with the three calendar months March, April and May 2018, and the earlier
       review (issue 5) with three-week windows from 30 March; both decisions carry 2026-11-11 marks and the
       definition can hold only one.
     - Issue 5 was argued in November under the floor as it then read, which no window may fall below; the floor as
       amended on 2026-11-11 admits the March window (38.9%) beside two above half.
     - Which windows ship, the three months or the three weeks (the gap stays one month in either, issue 2)?
   * **Background:** the monthly length is the group the winning team validated on, and the three months are the
     newest the six months of payments allow with the gap; the three-week windows cover 30 March to 31 May back to
     back and keep every train side above 52.9%, at 179,939 test payments against 274,613[^4a].
   * **Experiments:** from issue 1's table, test payments and train shares, newest first: months 89,326 (70.7%),
     83,655 (53.5%) and 101,632 (38.9%); three weeks 58,731 (75.9%), 59,803 (64.4%) and 61,405 (52.9%).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three months (implemented) | 1-31 March, 1-30 April and 1-31 May 2018 | the winners' validation length; 274,613 test payments; the amended floor admits March | the March window trains on 38.9% of the payments, on December and January only |
     | B | Three weeks | 30 March-19 April, 20 April-10 May, 11-31 May 2018 | every train side at 52.9% or more; three back-to-back windows over the ten weeks open | 179,939 test payments; a window shorter than the winners' month |

   * **Recommendation:** A, the later decision and the one the amended floor was written for; B if the March window's
     38.9% should be avoided even under the two tiers. **Decision:** A or B?

   **Notes for the AI:** on B, `temporal = Temporal(on="Transaction_date", splits=TemporalSplits(window=21,
   unit="days", gap=1, gap_unit="months", cutoffs=("2018-05-11", "2018-04-20", "2018-03-30")))`, and rewrite
   `task_summary.split` and `changes`, the window bullet of `curation_comments` and `splits_comment` with the numbers
   above; `dataset check`.

   [^4a]: **SPLIT-14** (Must; amended 2026-11-11, Lennart): the newest window and at least one other train on at least
     50% of the data; further windows down to 30%, and at most as many windows under 50% as at or above it.
     **SPLIT-12** (Should): the length comes from the source, here the winners' month groups.

   **Andrej (2026-11-11, change, the split row):** As we discussed.

   **Answer (AI, 2026-11-11):** the split-row mark names this issue's option B, three-week windows with a one-month
   gap, but it does not settle the issue on its own: issue 1's mark of the same day names option A. Which one ships?

   * **Problem:**
     - "As we discussed" points at issue 5's answer of 2026-11-04, three-week test windows with a one-month gap,
       whose `Resolved` turn of 2026-11-09 quotes this very mark and gives the parameters.
     - That turn and issue 5's mark were read on 2026-11-09 or earlier, before the floor was amended on 2026-11-11 to
       admit a window under half beside two above it; Lennart's mark for the three months came after the amendment.
     - The definition on this branch has the three months, so option B is a change to the shipped split, not a
       confirmation of it.
   * **Background:** the gap is one month under either option and is unaffected (issue 2); so are the client key, the
     features and the metric. Applying B would mean the split is decided twice in this review in opposite ways on the
     same date, which is why nothing was changed for this mark.
   * **Experiments:** the two candidates, newest window first (issue 1's table):

     | Windows | Test payments | Fraud, test | Train share |
     |---|---|---|---|
     | 1-31 May, 1-30 Apr, 1-31 Mar (as implemented) | 89,326 / 83,655 / 101,632 | 3.5% / 3.4% / 4.0% | 70.7% / 53.5% / 38.9% |
     | 11-31 May, 20 Apr-10 May, 30 Mar-19 Apr | 58,731 / 59,803 / 61,405 | 3.8% / 3.1% / 3.5% | 75.9% / 64.4% / 52.9% |

   * **Effect on the task:** B tests 179,939 payments instead of 274,613 and lifts the oldest train side from 38.9% to
     52.9%; A keeps the month the winning team validated on and the whole of each month's payments.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | The three months stay (implemented) | nothing changes | the later mark; the winners' length; the most test payments | the oldest window trains on 38.9%, which only the amended floor admits |
     | b | Three weeks, as the split-row mark names | `TemporalSplits(window=21, unit="days", n_windows=3, gap=1, gap_unit="months")`, the three windows above | every train side above half; what you marked twice (here and in issue 5) | 94,674 test payments fewer; reverses the mark of 2026-11-11 on issue 1 |

   * **Recommendation:** a, because it is the later of the two marks and the floor was amended for exactly this case;
     b is one line in `temporal` plus the texts if you want the three weeks after all. **Decision:** a or b?

   **Notes for the AI:** on b, the notes above (the `cutoffs` form keeps the windows of the suggestion's table), then
   `task_summary.split` and `changes`, the window bullet of `curation_comments` and `splits_comment`, and a CC line;
   `dataset check` on the cluster. Nothing else in the dataset changes under either option.

5. **Two-week test windows, so that every training side holds more than half the payments? (the review of 2026-11-04, its issue 1)**

   * **Problem:**
     - The three test windows are March, April and May 2018, each trained on everything up to one month before it, so the March window trains on December and January only: 229,906 of 590,540 payments (38.9%).
     - A temporal task needs at least three windows with at least half the data on each training side, since a smaller training side is too unlike the deployed model, which is refit on all history[^5a].
     - Shorten the test windows to two weeks (keeping the one-month gap), or keep the monthly windows?
   * **Background:** the split table of the README gives the payments per period: December and January 229,906,
     February 86,021, March 101,632, April 83,655, May 89,326. The training sides of the monthly windows hold 70.7%
     (May), 53.5% (April) and 38.9% (March) of the payments. The one-month gap stays in every option: a chargeback
     is reported weeks after the payment, so the newest labels are not known at a refit, and the competition's test
     file also starts about a month after its training file[^5b].
   * **Effect on the task:** the March window scores a model trained on two months of a six-month history, which no
     processor that refits on all its history would deploy; its score weighs a third of the benchmark's result.
   * **Experiments:** none run; the numbers come from the split table of the README (build of 2026-10-06). With
     two-week windows (the last 14 days of May, the 14 before, the 14 before those) the oldest training side ends
     around 20 March, about 380,000 payments (about 64%), and each test window holds about 40,000 payments with about
     1,400 frauds at the 3.5% rate.
   * **Consistency:** follows california_house_prices_2020, whose windows were moved to train on at least 50%[^5c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Monthly windows (implemented) | test March, April, May; one-month gap | the first-place solution's month-wise validation; a month of payments per window | the March window trains on 38.9% of the data |
     | B | Two-week windows | three 14-day test windows at the end of May and April; one-month gap | every training side above 60%; about 40,000 test payments per window | a shorter horizon than the winners' monthly validation |
     | C | 30-day windows stepped by 15 days | three overlapping 30-day test windows; one-month gap | keeps a month per window; oldest training side about 54% | the windows share half their test rows, so they are not three separate tests |

   * **Recommendation:** B: it meets the floor with room to spare and keeps the gap; a processor refits its fraud model
     more often than monthly, so the shorter horizon is no loss for the use case. **Decision:** two-week windows (B),
     monthly windows (A) or overlapping 30-day windows (C)?

   **Notes for the AI:** on B, `temporal = Temporal(on="Transaction_date", splits=TemporalSplits(window=14,
   unit="days", n_windows=3, gap=1, gap_unit="months"))`; rewrite `splits_comment` and the task summary's `split` and
   `changes` ("Each of the last three two-week periods ..."), run `dataset check` and report the exact train shares and
   frauds per window; record `CC` line; rebuild. On C, `TemporalSplits(window=30, unit="days", n_windows=3, step=15,
   gap=1, gap_unit="months")`.


   **Andrej (2026-11-04, discuss):** It would be better to keep more test samples if possible and use a shorter planning gap, unless there is a particular reason to go with one month.

   **Answer (AI, 2026-11-04):**

   - **Question:** is there a particular reason for a one-month gap, or can the windows keep more test payments with a shorter gap?
   - **Settling fact:** there is a reason for some gap, but none for exactly a month. The gap changes the score more than anything else in the split: LightGBM on the same three test months scores 0.930 AUC with no gap, 0.921 with one week, 0.915 with two weeks and 0.904 with a month.
   - **Why a gap:** a payment counts as fraud once its card is reported as charged back, and the client's later payments with it[^a1]. Cardholders report a chargeback weeks after the payment, so at a refit the frauds of the last days are not yet known. The data has no report dates, so the delay itself cannot be measured.
   - **Why a month:** only the competition's file layout. Its unlabelled test file starts on 1 July 2018, 30.0 days after the training file ends (31 May). The host never says why. The first-place team validated both ways: "train 4 / skip 1 / predict 1", "train 2 / skip 2 / predict 2", and a holdout of the last 25% with no gap.
   - **Not label carry-over:** the gain from a shorter gap is the same without the client key (0.931 vs 0.903 with no gap vs a month) and on test payments of clients with no earlier fraud (0.928 vs 0.903). It is not extra training data either: with every training side cut to the same 60 days, the gap still costs 0.025 (0.924 with no gap, 0.899 with a month). It is how recent the training payments are: fraud patterns change from week to week.
   - **How far labels carry:** 99.3% of the clients with a fraud are fraud in every payment, and 98.7% of the payments after a client's first fraud are fraud. Payments of a client whose fraud lies on the training side are 0.2-0.3% of each test month with a one-month gap and 0.4-0.5% with no gap. They hold 5-7% of the test frauds with a month, 7-10% with two weeks and 10-15% with no gap.
   - **What the windows cost:** the floor of half the data on each training side rules out calendar months with any gap of a week or more (oldest training side 49.8% with one week). Test payments and frauds per window, oldest window first:

     | Windows and gap | Training sides | Test payments | Test frauds | All test payments |
     |---|---|---|---|---|
     | months, 1 month (now) | 38.9%, 53.5%, 70.7% | 101,632, 83,655, 89,326 | 4,019, 2,828, 3,114 | 274,613 |
     | 14 days, 1 month | 64.4%, 72.4%, 79.0% | 39,992, 40,849, 37,693 | 1,299, 1,294, 1,480 | 118,534 |
     | 21 days, 2 weeks | 62.4%, 73.5%, 83.1% | 61,405, 59,803, 58,731 | 2,171, 1,864, 2,209 | 179,939 |
     | 4 weeks, 1 week | 54.2%, 69.5%, 83.1% | 86,813, 77,822, 78,542 | 3,486, 2,637, 2,774 | 243,177 |
     | 4 weeks, 2 weeks | 50.4%, 66.0%, 79.9% | 86,813, 77,822, 78,542 | 3,486, 2,637, 2,774 | 243,177 |
     | months, no gap | 53.5%, 70.7%, 84.9% | 101,632, 83,655, 89,326 | 4,019, 2,828, 3,114 | 274,613 |

   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Monthly windows, one-month gap (implemented) | test March, April, May | the competition's gap; 274,613 test payments | the March window trains on 38.9%, below the floor |
     | B | 14-day windows, one-month gap | the last three fortnights of May and April | the competition's gap; every training side above 64% | 118,534 test payments, 43% of A |
     | C | 4-week windows, one-week gap | 4 May-31 May, 6 April-3 May, 9 March-5 April | 243,177 test payments, twice B; training sides 54-83%; frauds of the last week before a refit stay unknown | a week is shorter than most chargeback delays, so the score is about 0.017 higher than with a month |
     | D | 21-day windows, two-week gap | three three-week windows from 30 March | training sides 62-83%; a gap closer to a chargeback delay | 179,939 test payments |
     | E | Calendar months, no gap | test March, April, May, trained on everything before | the most test payments; training sides 54-85% | trains on frauds not yet reported at the refit; the highest score, about 0.026 above a month |

   - **Recommendation:** C: twice the test payments of B, every training side above half the data, and a gap that keeps the newest unreported frauds out of training. D if the gap should stay closer to the chargeback delay. **Decision:** C (4 weeks, 1-week gap), D (21 days, 2-week gap), B (14 days, 1-month gap) or E (months, no gap)?

   **Notes for the AI:** LightGBM (800 trees, lr 0.03, 256 leaves; transaction plus identity columns, D-columns normalised, `uid` from the folder's csv) on the train file, test windows March/April/May 2018, gaps 0/7/14 days/1 month, with and without `uid`, plus a control with each training side cut to the 60 days before the gap. Scripts and outputs in `~/claude_jobs/ba_marks_1104/ieee_fraud_detection/` (`scripts/gap_lgbm.py`, `scripts/gap_lgbm_fixed60.py`, `scripts/splits_table.py`, `scripts/propagation.py`, `out/`). The host's post (discussion 101203) could not be re-fetched (Kaggle needs JavaScript); its second sentence (unreported after 120 days counts as legit) was recalled, not verified, and is left out. The first-place validation schemes come from a summary of the write-up (eda-ai-lab.tistory.com/448), not the Kaggle post itself. Params: C `TemporalSplits(window=4, unit="weeks", n_windows=3, gap=1)`; D `TemporalSplits(window=21, unit="days", n_windows=3, gap=14)`; B `TemporalSplits(window=14, unit="days", n_windows=3, gap=1, gap_unit="months")`; E `TemporalSplits(window=1, unit="months", n_windows=3)`. On any choice rewrite `splits_comment`, the task summary's `split` and `changes`, and the gap line of `curation_comments` ("The competition test data left a planning window of one month, so do we."); record `CC` and `Assessment` lines; `dataset check`; the split probes.

   [^a1]: The host (Lynn@Vesta, https://www.kaggle.com/c/ieee-fraud-detection/discussion/101203): "The logic of our labeling is define reported chargeback on the card as fraud transaction (isFraud=1) and transactions posterior to it with either user account, email address or billing address directly linked to these attributes as fraud too." **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose outcome is known by the window's start, with a gap of about the label's delay. **SPLIT-14** (Must): at least 3 windows, no training side below 50% of the data. Andrej on noaa_afsc_bottom_trawl_survey_cpue (2026-11-02): "Unless the original paper says so, we should go with no planning gap."


   **Andrej (2026-11-04, discuss):** Our main goal is to keep this as close as possible to a real application. What do you suggest?

   **Answer (AI, 2026-11-04):**

   - **Question:** which windows and gap come closest to how a processor like Vesta would really use the model?
   - **Suggestion:** three-week test windows with a one-month gap. Each window trains on every payment up to a month before it starts. Of all window lengths that keep a one-month gap and at least half the data on every training side, this gives the most test payments.
   - **The gap follows the label delay:** a fraud label exists only once the issuer files a chargeback. Visa gives the issuer up to 120 days from the processing date to file a card-absent fraud chargeback[^b1]. Cardholders usually find the fraud on their statement, so most chargebacks come weeks after the payment. No public source gives the share filed within a month[^b2]. The host chose a 30-day gap before its own test file, and Vesta knows its own label delay. So a month is the best supported gap; a week or two would train on frauds that are mostly not reported yet.
   - **The window length follows the refit cadence, which is unknown:** Vesta does not publish how often it refits. The only cadence I found is Stripe's: Stripe's own blog says only that it "tripled the speed" of its Radar model updates, and press reports of daily retraining (2018) could not be checked. A refit at least weekly is likely, so a three-week window is not longer than a real deployment would see. Shorter windows add no test payments (the floor fixes the pool); they only make each score noisier.
   - **Numbers (oldest window first):**

     | Window | Test payments | Frauds | Training side |
     |---|---|---|---|
     | 30 March-19 April 2018 | 61,405 | 2,171 | 52.9% |
     | 20 April-10 May 2018 | 59,803 | 1,864 | 64.4% |
     | 11 May-31 May 2018 | 58,731 | 2,209 | 75.9% |

     In total 179,939 test payments and 6,244 frauds: 1.5 times B (14-day windows, 118,534) and 66% of the monthly windows (274,613). LightGBM scores about 0.904 AUC with a one-month gap, against 0.930 with none (earlier answer).
   - **What it trades:**
     - A month still falls short of full label maturity: frauds reported 30-120 days after the payment are in the training labels, though a real refit would not know them yet.
     - A full 120-day gap is impossible here: with six months of data, the training sides would hold only about two months, far below half the data.
     - Monthly test windows with a one-month gap remain below the floor (38.9%).
   - **Params:** `TemporalSplits(window=21, unit="days", n_windows=3, gap=1, gap_unit="months")`. Setting `window=23` holds 197,790 test payments, but its oldest training side is 51.0%, and 24 days falls below the floor (49.3%).
   - **Recommendation:** three-week windows with a one-month gap: the host's own gap, the floor met in every window, and more test payments than the 14-day option. **Decision:** three-week windows with a one-month gap, or one of the options of the earlier answer?

   **Notes for the AI:** on yes, set the params above; `splits_comment` and the task summary's `split` and `changes` ("Each of the last three three-week periods is a test window, trained on all payments up to one month before it, as in the competition's gap"); update the gap line of `curation_comments` with the chargeback limit and the host's 30-day gap; record `CC`/`Assessment` lines; `dataset check`; split probes. Window numbers from `temporal_window_splits` on the train file (the same call `dataset check` makes). Not verified: Vesta's refit cadence; the daily-retraining press reports (finextra and eweek returned 403); the share of fraud chargebacks filed within 30 days (no public statistic found).

   [^b1]: Chargebacks911, Visa reason code 10.4 (card-absent fraud): "the issuing bank has a maximum of 120 calendar days from the transaction processing date to dispute a claim" (https://chargebacks911.com/chargeback-reason-codes/visa/10-4-card-absent-environment/). ClearSale adds that for fraud the clock "may begin on the date the cardholder notices unauthorized activity" (https://www.clear.sale/blog/what-is-the-time-limit-on-chargebacks). Both are industry write-ups, not Visa's rulebook. **SPLIT-10** (Should): a gap of about the label's delay. **SPLIT-14** (Must): at least 3 windows, no training side below 50%.
   [^b2]: arXiv 2204.05265, on card fraud detection: "verification often takes days" (https://arxiv.org/abs/2204.05265). Stripe, "New Radar features": "we've tripled the speed at which we update Radar's machine learning models" (https://stripe.com/fr-be/blog/new-radar-features). **SPLIT-12** (Should): the horizon follows the source or the refit cadence. **SPLIT-17** (Should), its reason: finer windows add no test rows, since the 50% floor fixes the test pool.

   [^5a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data; a smaller train side is too unlike the real application.
   [^5b]: **SPLIT-10** (Should): when a label is known only some time after its row, a model refit at a window's start
     knows only the rows whose label had arrived. **SPLIT-12** (Should): the horizon is a human judgment from the
     source, such as the competition's own test window or the refit cadence.
   [^5c]: SPLIT-14 case: california_house_prices_2020, `min_train_fraction=0.25` let the oldest window train on 25% of
     the rows; its windows now train on 50%, 67% and 83% (2026-10-21).

   **Answer (AI, 2026-11-06):** the time review of 2026-11-06 adds how the labels arrive; it rules out a split without a gap (E) and leaves the last suggestion, three-week windows with a one-month gap, standing.

   - **When each part arrives:** a payment and its features come at once, when Vesta accepts or declines it; its label comes when the card is charged back, up to 120 days later, and the host then marks the client's later linked payments as fraud too. The record's facts say `Samples: Over Time`, `Time: Dated` and `Target: Varying Delay`; issue 3 asks to add the forward carry. A temporal split carries no time-basis tag[^5t].
   - **The release holds the final labels:** fraud is 3.1% to 4.0% a week in May 2018, the last month, against 3.4% to 4.0% a month from January to April (2.6% in December), so no late shortfall shows at the release end. A refit at a window's start would not have had the newest of these labels; only a gap keeps them out, since the release has no report dates for an as-of filter[^5u].
   - **What this decides:** the gap is for the label's delay, not for planning, so the rule against planning gaps does not apply to it; its length cannot be measured here and rests on the host's 30-day layout and the chargeback limit, as in the last answer. Issue 2 asks to write this reason into the definition.

   [^5t]: **SPLIT-32** (Should): how the data was collected (the record's facts on samples, time and target) is information for the split; a definition names a use-case prototype only for a split that is not temporal.
   [^5u]: **SPLIT-10** (Should, amended 2026-11-05): a gap is set where late labels are documented and the collection does not cover them, and where a measurement shows a shortcut through recent labels or a selection by the outcome at the release end.

   **Andrej (2026-11-06, discuss):** Agree. I follow your suggestion. Document it carefully.

   **Resolved (2026-11-09, Andrej):** three-week test windows with a one-month gap, the suggestion of 2026-11-04 (the
   split mark: change, "As we discussed."):
   `TemporalSplits(window=21, unit="days", n_windows=3, gap=1, gap_unit="months")`. `dataset check` builds the
   windows of the suggestion's table: 30 March-19 April 2018 (61,405 test payments, 2,171 frauds, training side
   52.9%), 20 April-10 May (59,803, 1,864, 64.4%) and 11 May-31 May (58,731, 2,209, 75.9%). `splits_comment`, the task summary's `split` and `changes`, and a curation note on the
   windows (the training floor, the chargeback delay of up to 120 days, the host's 30-day gap, what the choice trades,
   the gap runs of 2026-11-04) are in `dataset.py`; the record has a CC line. Not rebuilt.

   **Answer (AI, 2026-11-11, on the split row's mark):** the page's split row carries the mark `change`, "As we
   discussed.", the same words the `Resolved` turn above quotes; it names the three-week windows of the answer of
   2026-11-04. It is answered in issue 4, where the choice between those windows and the three months stands.

   **Answer (AI, 2026-11-11):** this issue comes from the review of 2026-11-04, which lived in a file of its own and
   was merged into this review on 2026-11-11; it was numbered 1 there and is renumbered here, where issue 1 is the
   window question of the review of 2026-11-11. Its mark of 2026-11-11 ("Agree. I follow your suggestion. Document it
   carefully") repeats the note of 2026-11-06 and chooses three-week windows, which issue 1's mark of the same day
   contradicts; the choice is issue 4 and the definition keeps the three months until it is settled. What the two
   agree on is applied: the gap of one month, with the chargeback delay as its reason (issue 2), written into the
   definition.

## Reference

Addison Howard, Bernadette Bouchon-Meunier, IEEE CIS, inversion, John Lei, Lynn@Vesta, Marcus2010, and Prof. Hussein Abbass. IEEE-CIS Fraud Detection. https://kaggle.com/competitions/ieee-fraud-detection, 2019. Kaggle.
