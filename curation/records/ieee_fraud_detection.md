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
- Dated Event Log
collections:
- TabArena Reject
original_source: Kaggle
year: '2019'
collection_period: Dec 2017 - May 2018
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

CC (2026-11-09, Andrej): three-week test windows with a one-month gap (Review issue 1, the suggestion of 2026-11-04): the last three 21-day periods, 30 March to 31 May 2018, each trained on every payment up to one month before it. The training sides hold 52.9%, 64.4% and 75.9% of the payments, so every window keeps at least half the data, where the monthly windows trained the March window on 38.9%. Replaced on 2026-11-11 by the calendar months (Review issue 4), restored on 2026-11-19 (Review issue 5).

CC (2026-11-09, Andrej): the gap's reason is the label's delay, not planning (Review issue 2, B): a payment becomes fraud once its card is charged back, up to 120 days later, and the release holds the final labels, so the one-month gap keeps out labels a refit could not have known. The gap note, `splits_comment` and the task summary say so.

CC (2026-11-09, Andrej): `Target: Revised Later` added next to `Target: Varying Delay` (Review issue 3, B): besides the chargeback delay, the host marks a client's later linked payments as fraud, so a payment's label is also set afterwards by another payment.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows and horizons, which this record never had. Priority 3: gap 0, use case 0, source + (Vesta's competition), shape +, risk 0 (the open issue is the window length and the floor).

CC (2026-11-11, Lennart): REVIEW issue 4 (which test windows), as implemented (A): the test windows stay March, April and May 2018, one month each after the competition's one-month gap, in place of the AI's three-week windows; SPLIT-14 as amended on 2026-11-11 admits March, which trains on 38.9% of the payments (one window under half, two above). The windows walk back from the newest: with the gap a February window would train on December only (about 23%).

CC (2026-11-11, Lennart): the declared horizon (one month, a one-month gap, windows starting 2018-05-01, 2018-04-01 and 2018-03-01) is checked, as the month comes from the first-place team's month groups and the gap from the competition (labelled payments end on 31 May 2018, its test starts on 1 July 2018).

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=1, unit="months", n_windows=3, gap=1`); test 89,326, 83,655 and 101,632 payments (May, April, March 2018), train 417,559, 315,927 and 229,906 (70.7%, 53.5%, 38.9% of 590,540); a February window would train on the 137,321 payments of December (23.3%). `task_summary.split`, `splits_comment` and the two `curation_comments` bullets that called the month a forecasting horizon and the gap a planning window now say the month is the winners' validation group, not a refit cadence (Vesta states none; the competition scores one model on six months), and give the gap's source and the Visa chargeback limit of 120 days. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-17, Andrej): the declared split (temporal on `Transaction_date`, windows of 1 month, 3 windows, gap 1 month) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-19, Andrej): three-week test windows with the competition's one-month gap, all training on half the payments or more (the month was the winners' validation scheme, not the use case) (Review issue 5).

## Review

**Outcome:** added. On 2026-11-09 Andrej chose three-week test windows with a one-month gap (issue 1), gave the gap
its reason, the chargeback delay of the label (issue 2), and added `Target: Revised Later` to the collection facts
(issue 3). On 2026-11-11 Lennart kept the three test months, March, April and May 2018, with the competition's
one-month gap (issue 4 and the horizon, A), which the amended floor admitted with March training on 38.9% of the
payments. On 2026-11-19 Andrej replaced them by three-week windows, 11-31 May, 20 April-10 May and 30 March-19 April
2018, after the same one-month gap, training on 52.9% to 75.9% (issue 5, C).

**Main points:** Settled on 2026-11-19: three test windows of three weeks, 30 March to 31 May 2018, after a one-month
gap, all training on half the payments or more (issue 5, C), replacing the calendar months March to May 2018 kept on
2026-11-11 (issue 4, A), which had replaced the three-week windows of 2026-11-09 (issue 1). Settled on 2026-11-09: the
gap is there for the label's delay (a chargeback up to 120 days after the payment), its length the competition's
(issue 2); `Target: Revised Later` stands next to `Target: Varying Delay` (issue 3). Nothing is left to decide.

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
floor of 2026-11-11 admits the March window (issue 4), so three windows of a month fit. The notes no longer call the
month a forecasting horizon: `curation_comments`, `task_summary.split` and `splits_comment` say it is the winners'
validation group, not a refit cadence (Vesta states none, and the competition scores one model on six months), and
give the gap's reason. `temporal` is unchanged. The record has the horizon CC line. `dataset check`: 0 errors, 0
warnings (README not regenerated).

**Issues:**

1. **Two-week test windows, so that every training side holds more than half the payments?**

   * **Problem:**
     - The three test windows are March, April and May 2018, each trained on everything up to one month before it, so the March window trains on December and January only: 229,906 of 590,540 payments (38.9%).
     - A temporal task needs at least three windows with at least half the data on each training side, since a smaller training side is too unlike the deployed model, which is refit on all history[^1a].
     - Shorten the test windows to two weeks (keeping the one-month gap), or keep the monthly windows?
   * **Background:** the split table of the README gives the payments per period: December and January 229,906,
     February 86,021, March 101,632, April 83,655, May 89,326. The training sides of the monthly windows hold 70.7%
     (May), 53.5% (April) and 38.9% (March) of the payments. The one-month gap stays in every option: a chargeback
     is reported weeks after the payment, so the newest labels are not known at a refit, and the competition's test
     file also starts about a month after its training file[^1b].
   * **Effect on the task:** the March window scores a model trained on two months of a six-month history, which no
     processor that refits on all its history would deploy; its score weighs a third of the benchmark's result.
   * **Experiments:** none run; the numbers come from the split table of the README (build of 2026-10-06). With
     two-week windows (the last 14 days of May, the 14 before, the 14 before those) the oldest training side ends
     around 20 March, about 380,000 payments (about 64%), and each test window holds about 40,000 payments with about
     1,400 frauds at the 3.5% rate.
   * **Consistency:** follows california_house_prices_2020, whose windows were moved to train on at least 50%[^1c].
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

   **Notes for the AI:** LightGBM (800 trees, lr 0.03, 256 leaves; transaction plus identity columns, D-columns normalised, `uid` from the folder's csv) on the train file, test windows March/April/May 2018, gaps 0/7/14 days/1 month, with and without `uid`, plus a control with each training side cut to the 60 days before the gap. The host's post (discussion 101203) could not be re-fetched (Kaggle needs JavaScript); its second sentence (unreported after 120 days counts as legit) was recalled, not verified, and is left out. The first-place validation schemes come from a summary of the write-up (eda-ai-lab.tistory.com/448), not the Kaggle post itself. Params: C `TemporalSplits(window=4, unit="weeks", n_windows=3, gap=1)`; D `TemporalSplits(window=21, unit="days", n_windows=3, gap=14)`; B `TemporalSplits(window=14, unit="days", n_windows=3, gap=1, gap_unit="months")`; E `TemporalSplits(window=1, unit="months", n_windows=3)`. On any choice rewrite `splits_comment`, the task summary's `split` and `changes`, and the gap line of `curation_comments` ("The competition test data left a planning window of one month, so do we."); record `CC` and `Assessment` lines; `dataset check`; the split probes.

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

   [^1a]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data; a smaller train side is too unlike the real application.
   [^1b]: **SPLIT-10** (Should): when a label is known only some time after its row, a model refit at a window's start
     knows only the rows whose label had arrived. **SPLIT-12** (Should): the horizon is a human judgment from the
     source, such as the competition's own test window or the refit cadence.
   [^1c]: SPLIT-14 case: california_house_prices_2020, `min_train_fraction=0.25` let the oldest window train on 25% of
     the rows; its windows now train on 50%, 67% and 83% (2026-10-21).

   **Answer (AI, 2026-11-06):** the time review of 2026-11-06 adds how the labels arrive; it rules out a split without a gap (E) and leaves the last suggestion, three-week windows with a one-month gap, standing.

   - **When each part arrives:** a payment and its features come at once, when Vesta accepts or declines it; its label comes when the card is charged back, up to 120 days later, and the host then marks the client's later linked payments as fraud too. The record's facts say `Samples: Over Time`, `Time: Dated` and `Target: Varying Delay`; issue 3 asks to add the forward carry. A temporal split carries no time-basis tag[^1t].
   - **The release holds the final labels:** fraud is 3.1% to 4.0% a week in May 2018, the last month, against 3.4% to 4.0% a month from January to April (2.6% in December), so no late shortfall shows at the release end. A refit at a window's start would not have had the newest of these labels; only a gap keeps them out, since the release has no report dates for an as-of filter[^1u].
   - **What this decides:** the gap is for the label's delay, not for planning, so the rule against planning gaps does not apply to it; its length cannot be measured here and rests on the host's 30-day layout and the chargeback limit, as in the last answer. Issue 2 asks to write this reason into the definition.

   [^1t]: **SPLIT-32** (Should): how the data was collected (the record's facts on samples, time and target) is information for the split; a definition names a use-case prototype only for a split that is not temporal.
   [^1u]: **SPLIT-10** (Should, amended 2026-11-05): a gap is set where late labels are documented and the collection does not cover them, and where a measurement shows a shortcut through recent labels or a selection by the outcome at the release end.

   **Andrej (2026-11-06, discuss):** Agree. I follow your suggestion. Document it carefully.

   **Resolved (2026-11-09, Andrej):** three-week test windows with a one-month gap, the suggestion of 2026-11-04 (the
   split mark: change, "As we discussed."):
   `TemporalSplits(window=21, unit="days", n_windows=3, gap=1, gap_unit="months")`. `dataset check` builds the
   windows of the suggestion's table: 30 March-19 April 2018 (61,405 test payments, 2,171 frauds, training side
   52.9%), 20 April-10 May (59,803, 1,864, 64.4%) and 11 May-31 May (58,731, 2,209, 75.9%). `splits_comment`, the task summary's `split` and `changes`, and a curation note on the
   windows (the training floor, the chargeback delay of up to 120 days, the host's 30-day gap, what the choice trades,
   the gap runs of 2026-11-04) are in `dataset.py`; the record has a CC line. Not rebuilt.

   **Superseded:** on 2026-11-11 Lennart kept the calendar months March to May 2018 (issue 4); on 2026-11-19 Andrej
   restored three-week windows after the one-month gap, at fixed cutoffs (30 March, 20 April and 11 May 2018), with
   the same windows and training sides as above (issue 5). The definition ships issue 5's windows.

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

   **Applied (2026-11-23):** issue 5's definition named the competition as the gap's reason; the curation note `Gap
   (2026-11-09, Andrej)` now gives the label's delay, and `splits_comment` and the task summary's `split` and `changes`
   name the gap "for the chargeback delay", its length the competition's own.

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
   `'Target: Varying Delay'`, with a CC line. Both target
   facts stand: the chargeback delay and the labels carried forward along the client.

4. **Which test windows should replace March, April and May 2018?**

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

5. **Train floor: keep the window under half the data as the curator's exception, or drop it?**

   * **Problem:**
     - March 2018 trains on 38.9% of the payments, beside May and April on 70.7% and 53.5%.
     - Since 2026-11-19, every window trains on at least half the data, and a window under half is the curator's exception for the dataset, down to 30%[^split14]; the sign-off (Lennart, 2026-11-11, review issue 4, A) was given under the earlier rule, which admitted such windows beside two at half or more.
     - The definition has 3 windows; the target an IID split would get[^split33] for 590,540 rows is 3; without the window under half it keeps 2.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the window as the curator's exception (implemented) | The accepted warning is reworded to the new rule; split unchanged | Keeps the periods it tests, as signed off; more windows toward the target | It trains on less than half the data |
     | B | Drop the window under half | The windows under half leave the declaration; a rebuild | Every window trains on half the data or more | 1 fewer window and the period it tests |

   * **Recommendation:** A, the sign-off's reason (periods or test rows the newest windows lack) still holds, and no window is under 30%. **Decision:** A or B?

   **Notes for the AI:** on A, reword the `splits_train_under_half` acceptance (drop "SPLIT-14's two tiers admit it", name the curator's exception and this decision) and add a CC line; on B, remove the windows from the declaration, rebuild, and update the splits comment.

   **Andrej (2026-11-19, discuss):** Why is the difference so big? Explain the train/test windows better

   **Answer (AI, 2026-11-19):** The train shares jump by 15 to 17 points from window to window because each step back removes one whole month from training, and the release holds only six months: March trains on December and January alone (38.9%), April adds February (53.5%), May adds March (70.7%).

   * **How the split is done today:** test windows of one calendar month, adjacent, walking back from the newest (May, April, March 2018), with a gap of one month between the train side and the window; the train side is every payment before the gap. The scored unit is the payment (one row; 590,540 payments, 1 December 2017 to 31 May 2018); the target count for this size is 3 windows, which the definition has.

     | Test window | Gap (not used) | Train side | Test payments | Fraud, test | Train payments | Train share |
     |---|---|---|---|---|---|---|
     | May 2018 | April | Dec 2017 to Mar 2018 | 89,326 | 3.5% | 417,559 | 70.7% |
     | Apr 2018 | March | Dec 2017 to Feb 2018 | 83,655 | 3.4% | 315,927 | 53.5% |
     | Mar 2018 | February | Dec 2017 to Jan 2018 | 101,632 | 4.0% | 229,906 | 38.9% |

   * **Why the difference is so big:** the shares are of all 590,540 payments, and each month is a large slice of them: December 137,321 (23.3%), January 92,585 (15.7%), February 86,021 (14.6%), March 101,632 (17.2%), April 83,655 (14.2%), May 89,326 (15.1%). Moving a window back a month moves its train side back a month, so the share drops by that month's slice; the gap month and the window itself never count as training. Half the payments lie before 22 February 2018, so with the one-month gap only windows from about 22 March on train on half.
   * **What the use case and the source fix, and what is ours:**
     - Fixed by the source: the gap of one month (the competition's labelled payments end on 31 May 2018 and its test starts on 1 July 2018).
     - Not fixed: the window length. The month is the first-place team's validation group ("ordered months as non-overlapping groups"), not a refit cadence; Vesta decides on each payment as it arrives and states none, and the competition scores one model on six months.
     - So shorter windows with the same gap are open; they move all three windows into the ten weeks from 22 March.

   * **Layouts at the same one-month gap** (counted on the definition's frame):

     | Layout | Windows | Test windows | Test payments | Train share |
     |---|---|---|---|---|
     | One month (today) | 3 | May, Apr, Mar 2018 | 83,655 to 101,632 | 38.9% to 70.7% |
     | Three weeks | 3 | 11-31 May, 20 Apr-10 May, 30 Mar-19 Apr 2018 | 58,731 to 61,405 | 52.9% to 75.9% |
     | Two weeks | 5 | from 23 Mar to 31 May 2018 | 37,693 to 44,653 | 50.4% to 79.0% |
     | One week | 10 | from 23 Mar to 31 May 2018 | 17,752 to 23,575 | 50.4% to 82.1% |
     | One month, overlapping | 3 | May, 16 Apr-15 May, Apr 2018 | 83,655 to 89,326 | 53.5% to 70.7% |

     The three-week windows, newest first: 11-31 May (58,731 payments, 3.8% fraud, train to 10 April: 447,995, 75.9%), 20 April-10 May (59,803, 3.1%, train to 19 March: 380,100, 64.4%), 30 March-19 April (61,405, 3.5%, train to 27 February: 312,574, 52.9%).

   * **Options** (new, after A and B of the issue):

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | C | Three-week windows, one-month gap | the three windows above, back to back from 30 March | keeps the competition's gap; three separate windows, all on 52.9% or more; the target count | three weeks has no source either; 179,939 test payments instead of 274,613 |
     | D | Two-week windows, one-month gap | five windows from 23 March | keeps the gap; every window on 50.4% or more | more windows than the target; the oldest on the edge of half |
     | E | One month, overlapping | May, 16 April-15 May, April | keeps the month and the gap; every window on 53.5% or more | 16 April-15 May tested twice: the windows are not separate evaluations |

   * **Recommendation:** C: the month was the winners' validation scheme, not part of the use case, so three weeks keep the one thing the source fixes (the gap) and put three separate windows on half the payments or more. **Decision:** A, B, C, D or E?

   **Notes for the AI:** on C, `TemporalSplits(window=21, unit="days", gap=1, gap_unit="months", cutoffs=("2018-05-11", "2018-04-20", "2018-03-30"))`; on D, `TemporalSplits(window=14, unit="days", gap=1, gap_unit="months", n_windows=5)`; on E, `TemporalSplits(window=1, unit="months", gap=1, cutoffs=("2018-05-01", "2018-04-16", "2018-04-01"))`. Each drops `splits_train_under_half`; rewrite `task_summary.split`, the horizon and gap bullets of `curation_comments` and `splits_comment` (the windows, the length's reason, the numbers above), add a CC line and a CHANGELOG entry, rebuild and run `dataset check`.

   **Andrej (2026-11-19, discuss):** Reply (C): Three-week windows, one-month gap

   **Resolved (2026-11-19, Andrej):** C. `TemporalSplits(window=21, unit="days", gap=1, gap_unit="months", cutoffs=("2018-05-11", "2018-04-20", "2018-03-30"))`: 11-31 May, 20 April-10 May and 30 March-19 April 2018 (58,731 to 61,405 payments, 3.1% to 3.8% fraud), training on 75.9%, 64.4% and 52.9%; the under-half acceptance is gone. `dataset check`: 0 errors, 0 warnings. Not rebuilt.

   [^split14]: **SPLIT-14** (Must): every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.

   [^split33]: **SPLIT-33** (Should): an IID or grouped split gets 3-fold cross-validation with 20, 10, 3 or 1 repeats by the units on its train side; SPLIT-15 aims a temporal split at the same count.

## Reference

Addison Howard, Bernadette Bouchon-Meunier, IEEE CIS, inversion, John Lei, Lynn@Vesta, Marcus2010, and Prof. Hussein Abbass. IEEE-CIS Fraud Detection. https://kaggle.com/competitions/ieee-fraud-detection, 2019. Kaggle.
