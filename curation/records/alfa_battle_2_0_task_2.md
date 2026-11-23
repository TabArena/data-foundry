---
unique_name: alfa_battle_2_0_task_2
name: Alfa Battle 2.0 (Task 2)
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
- Anonymized
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Other
year: '2020'
collection_period: Unknown
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://boosters.pro/championship/alfabattle2/overview
- https://ods.ai/competitions/dl-fintech-card-transactions
- https://www.kaggle.com/datasets/mrmorj/alfabattle-20?select=alfabattle2_alpha_sample.csv
- https://www.kaggle.com/datasets/sokolovaleks/alfabattle2-sandbox/data
- https://github.com/SlayZar/alpha_task_2
v2_path: datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2/dataset.py
source_row: 743
type_adapter_id: curation-record-v1
---

## Comments

"A key component of our work is responsible lending, based on a model-based assessment of the likelihood of a borrower defaulting on their obligations."
"The training set was collected over N days, and the test set over the following K days. Position on the leaderboard depends on how well we can predict past and future borrower defaults. The target variable is a binary value taking values 0 and 1"
ROC AUC

**Assessment (AI, 2026-10-07):** Boosters' links are dead; Alfa-Bank re-hosted byte-identical files for its 2022 ODS.ai competition (no login). Tabular models are competitive here (organizers' boosting baseline on aggregates 0.737 public AUC, their RNN 0.760), so the v2 folder uses that baseline's 127 aggregates per product. Boosters says the products are numbered by date; the transactions' week codes give 24 monthly issue dates, tested in 3 two-month windows. A client's products share identical transactions: when the earlier one defaulted, the later one defaults in 96% of cases, a flag not yet known at the later issue, so such products are removed from the training sides. Licence (noted only): the competition rules forbid passing on the data; Alfa-Bank later allowed research use.

CC (2026-10-13, Lennart): Features like the top solutions of the competition, what a data scientist would build, instead of the organizers' 127-feature baseline: 513 aggregates over restored ruble amounts (amount and timing statistics, per-value shares and means, mode and last values, money in against out, daily activity, a balance proxy, the last 30 and 90 days). Label-based encodings, embeddings and sequence-model scores stay out (modelling steps). Sources: 1st place slides (six LightGBMs, 0.780 private without the RNN), 4th private place slides (3,289 features), 9th place code (github.com/aizakharov94/AlfaBattle_task2); slides in the Drive folder linked from Habr 551130. Untuned LightGBM on our windows: ROC AUC 0.787 / 0.771 / 0.772 against 0.774 / 0.757 / 0.763.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Large temporal credit-default task from a bank competition; reconstructed time axis and heavy transaction aggregation keep the fit approximate.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; the changes are applied: four columns that copy another on every row dropped (510 features, 508 transaction aggregates), the right-censoring note replaced by the measured dip of the default rate in months 22-23 (maybe censoring, maybe a client cluster), the unsourced "unreleased month" removed (Alfa-Bank on Habr: test on the following period), the earlier flag of a repeat client "most likely" not known (P(later | earlier) 0.951 against P(earlier | later) 0.455), the use case as an add-on to the bank's bureau and application scorecards, issued products only. Open for Lennart: ratify the repeat-client filter against ieee_fraud_detection, gap 0 with an exception to SPLIT-10 or gap 1, the censoring note (Review issues 1, 3, 4). This supersedes the 2026-10-07 assessment's 127 baseline aggregates; against the CC of 2026-10-13, the definition has 508 aggregates (512 before the copies were dropped), not 513, and LightGBM with default settings gives ROC AUC 0.779 / 0.763 / 0.761 (the 0.787 / 0.771 / 0.772 need a slower-learning setup, reproduced only on the newest window). Priority 2: gap -, use case - (the source names the module, the fit is approximate), source +, shape +, risk - (open label-timing issues: possible right-censoring, the filter not yet ratified).

CC (2026-10-21, Lennart): record the SPLIT-9 / SPLIT-14 reading and the SPLIT-10 exception (cross-dataset item, ok).

**Exception to SPLIT-10 (2026-10-21, Lennart):** no label dates, and a default can be flagged up to a year after the issue: a gap of the label delay leaves 13-27% (12 months) or 35-53% (6 months) of the rows for training, below the 50% floor. Serves SPLIT-14 (Must); SPLIT-9 is met by dropping the products of the test window's clients (principles.md, Tensions). The gap's length (0 or 1 month) stays open in Review issue 3.

CC (2026-10-21, Lennart): on CLEAN-19: "Okay, we here the case is that we want to take the best of both, or a reasonable combination, and not a union. so here we take the best for alfa as it is the top-solution etc, does that make sense?" (CLEAN-19, amended). The top solutions' shared aggregates stay: they are the better of the two sets (untuned LightGBM 0.787 / 0.771 / 0.772 against the organizers' 0.774 / 0.757 / 0.763); the CLEAN-19 Cases row gained this reason.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — ROC AUC (https://boosters.pro/championship/alfabattle2/overview (record's competition-page excerpt: 'ROC AUC'); habr.com/ru/companies/alfa/articles/551130).

CC (2026-10-26, Lennart): issue 1: "Do (a) and keep it as is, IEEE is a slightly different case": the repeat-client filter stays. What sets it apart from ieee_fraud_detection: a later product defaults at 95.1% after a defaulted earlier one (2.3% otherwise), flat over lags of 1-10 months, while only 45.5% of later defaults had one, so the earlier flag was set after the later issue (SPLIT-9); ieee's carried labels follow the host's labelling rule (a chargeback marks the card's later transactions), read as known history (CC 2026-10-01).

CC (2026-10-26, Lennart): issue 3: gap 0 with the recorded exception to SPLIT-10 (serves SPLIT-14).

CC (2026-10-26, Lennart): issue 4: keep the newest months with the note on possible right-censoring.

CC (2026-10-26, Lennart): the declared metric, ROC AUC, is checked as declared.

**Assessment (AI, 2026-10-26):** the three issues are settled as implemented; a SPLIT-9 Cases row records issue 1 with the fact that sets it apart from ieee. One caveat from the precedent check: the timing test (95.1% / 45.5%) was never run on ieee_fraud_detection; if ieee shows the same timing, its keep would be the one to reopen. No open issue is left, so the folder's REVIEW.md is removed.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found a related task: `alfa_bank_credit_history_default` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Lennart): REVIEW issue 5 (which issue months), ok with "Reply (b): Months 22-23, 20-21 and 14-15" to the consistency check: months 14-15 replace 18-19, so the windows also test the other half of the second year and keep the default peak of months 20-21. Months 14-15 train on 41.1% of the rows after the repeat-client filter (43.3% before it), the one window under half beside 83.4% and 72.9%, signed off (SPLIT-14 as amended on 2026-11-11). The repeat-client filter and the gap-0 exception stay; `_make_splits` changes only its window list.

CC (2026-11-11, Lennart): the declared horizon (2 issue months, no gap, windows starting at months 22, 20 and 14) is checked, as no source gives a horizon or a refit cadence (the competition names its periods only as N and K days), so the two months are a convention.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `SPLIT_WINDOWS = TemporalSplits(window=2, unit="unique", cutoffs=(22, 20, 14))`, `_make_splits` unchanged; test 120,428, 107,844 and 90,937 products, train after the repeat-client filter 804,162, 702,678 and 396,171 (83.4%, 72.9%, 41.1% of 963,811; the filter removes 39,221, 32,861 and 21,497); default rate 3.02%, 3.36% and 2.70% in the windows, 2.78%, 2.67% and 2.45% on the train sides. For these windows a 12-month gap would leave 3-27% of the rows for training and a 6-month gap 20-53% (before the filter), so the exception's reason holds. `splits_rows_unused` recounted: 1,121 products in no split (181 of months 0-13, on all three training sides, and 940 of months 16-19, on the training sides of the two newest windows only, all of clients with a product in those windows). `task_summary.split`, `splits_comment` (the windows and why, the counts, the shares, the length as a convention, the gap figures) and the comment above `SPLIT_WINDOWS` are rewritten; the LightGBM ROC AUC of `curation_comments` and the 6-month-gap cost are dated to the windows of 2026-10-26; `accepted_check_warnings` accepts `splits_train_under_half` with the sign-off. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-20, Andrej): Review issue 6, E: the test windows walk back from the newest at two months (22-23, 20-21, 18-19; 60.3% to 83.4% training), replacing 14-15 (41.1%); the diversity that motivated an older window measured only the months between windows, as neighbouring months differ about equally throughout.

## Review

**Outcome:** added. You shipped it on 2026-10-26. On 2026-11-11 you chose the test windows months 22-23, 20-21 and
14-15 (issue 5, reply (b)), with months 14-15 training on 41.1% of the rows after the repeat-client filter and signed
off, and kept the two-month horizon without a gap as a convention (Horizon, A). On 2026-11-20 Andrej replaced months
14-15 by 18-19, so the windows walk back from the newest at two months and every one trains on 60.3% or more (issue 6, E).

**Main points:** Settled on 2026-11-20: the windows months 22-23, 20-21 and 18-19 (issue 6, E, replacing issue 5's
14-15 of 2026-11-11). Settled on 2026-11-11: the two-month horizon with the gap-0 exception as recorded. Nothing is
left open.

**Horizon:**

* **Verdict:** keep the two-month windows (low confidence): no source gives a horizon or a refit cadence, and at this
  length three windows fill six of the seven issue months that keep half the rows for training after the repeat-client
  filter.
* **Length:** declared as 2 issue months, "A scoring model is refit on all products issued so far and used for the
  next two months" (`splits_comment`, our wording). The competition only says "The training set was collected over N
  days, and the test set over the following K days" (competition page, quoted in the record), and Alfa-Bank's post
  (https://habr.com/ru/companies/alfa/articles/551130) names N and K only as letters; its one cadence, "Транзакции в
  hadoop обновляются раз в день" (the transactions are updated once a day), is for scoring, not refitting. The 9th
  place's code (https://github.com/aizakharov94/AlfaBattle_task2) gives no period, and the test labels were never
  released. The length is a convention, not a source.
* **Gap:** none, by your call of 2026-10-26 with the recorded exception: a default can be flagged up to a year after
  the issue and the data has no label dates, so a 6-month gap would leave 35-53% of the rows for training; the
  measurable shortcut, a client's earlier product, is removed from each train side by the repeat-client filter.
* **Time frame:** 24 monthly issue dates over two years, reconstructed from the week codes of the transactions (month
  m and month m+12 fall in the same week of the year); the source gives no calendar dates. After the filter a window
  starting at month 16 trains on 49.9% of the rows (52.8% before it), so the eligible test months are 17 to 23, the
  second half of the second year. The default rate rises to 3.36% in months 20-21 and dips to 3.07% and 2.97% in
  months 22-23, maybe right-censoring (kept with a note on 2026-10-26).
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Two months (implemented) | windows of two issue months, no gap (your call of 2026-10-26): eligible test months 17 to 23 | 3 windows of 107,844 to 121,390 products, before the split's own filter (it removes training products only) | three windows fill six of the seven eligible months | no source gives a horizon or a refit cadence |
  | B | One month | 8 candidates above the floor after the filter, months 16 to 23, 49,000 to 62,000 products each | 8 candidates of 49,299 to 62,256 products, before the split's own filter | more candidates to choose from | three spread windows would test 3 of the 8 months, about half today's test products |
  | C | Three months | two candidates above the floor after the filter, 21-23 and 18-20 | 2 candidates of 170,689 and 178,973 products, before the split's own filter | more products per window | only two windows; a third, 15-17, trains on 44.3%; the exception for an older window at 40% needs test entities that mostly recur, while 76% of the newest window's test products have no earlier product of the client |

* **Recommendation:** A: no source names a length, and two months fill six of the seven eligible months with three
  windows. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, windows of two issue months without a gap, kept as a convention: no source gives
a horizon or a refit cadence (the competition names its train and test periods only as N and K days). The gap-0
exception to SPLIT-10 and the repeat-client filter of 2026-10-26 stay. `splits_comment` now says the length is a
convention, not a stated cadence; the windows are issue 5's (b). The record has the horizon CC line. `dataset check`:
0 errors, 0 warnings (README not regenerated).

**Issues for Lennart:**

5. **Which issue months should the test windows be?**

   * **Problem:**
     - The three windows are months 22-23, 20-21 and 18-19, walking back from the newest, and after the repeat-client
       filter the next older pair (16-17) would train on 49.9% of the rows, under the floor[^ab-split14].
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring windows away from the ones just before the newest[^ab-split15].
     - With months 17 to 23 eligible, three two-month windows fill six of seven months, so the only choice is which
       month to leave out: 17 (today) or 21.
   * **Background:** The split stays custom: `_make_splits` takes the windows from `SPLIT_WINDOWS` and removes from
     each train side the products of clients that also have a product in the test window (30,878 to 39,221 products),
     which is why the floor applies to the share after the filter, not to the 52.8% the candidate table shows for
     months 16-17. Other years and other seasons are not open: months 12-23 are the second year, and every eligible
     month lies in its second half. In the candidate table `client_key` drifts most, but it is the internal client key
     the split drops before training; the real drift is `share_payment_system_3`, the share of a client's transactions
     through one payment system, which rises toward the newest months. PSI, the population stability index, compares a
     feature's distribution in the window with its train side; above 0.25 is usually read as a large shift.
   * **Statistics:** the default rates and the train shares after the filter counted on the definition's frame with
     the rule of `_make_splits`; the drift from the candidate table with a step of one month (100,000-row samples).

     | Months | In | Test products | Default rate, test | Default rate, train side after the filter | Train share before / after the filter | Median PSI | Largest PSI after `client_key` |
     |---|---|---|---|---|---|---|---|
     | 22-23 | A, B | 120,428 | 3.02% | 2.78% | 87.5% / 83.4% | 0.004 | 2.27 (`share_payment_system_3`) |
     | 20-21 | A | 107,844 | 3.36% | 2.67% | 76.3% / 72.9% | 0.005 | 1.74 (`share_payment_system_3`) |
     | 19-20 | B | 108,433 | 3.25% | 2.62% | 70.2% / 67.0% | 0.006 | 1.45 (`share_payment_system_3`) |
     | 18-19 | A | 121,390 | 3.12% | 2.58% | 63.7% / 60.3% | 0.004 | 1.15 (`share_payment_system_3`) |
     | 17-18 | B | 114,390 | 3.00% | 2.55% | 58.3% / 55.0% | 0.003 | 0.92 (`share_payment_system_3`) |
     | 16-17 | none | 105,544 | 2.88% | 2.51% | 52.8% / 49.9% | 0.005 | 0.75 (`share_payment_system_3`) |

   * **Effect on the task:** A tests months 18 to 23 and leaves out month 17; B tests months 17 to 20 and 22-23 and
     leaves out month 21, one of the two months with the highest default rate. Either way the score covers the same
     half-year, and B's oldest model trains on 55.0% instead of 60.3%.
   * **Consistency:** The exception for gap 0 and the repeat-client filter, both settled on 2026-10-26, hold under
     either option[^ab-split10]. delivery_eta_1m (issue 1) has the same shape, few eligible windows and one to leave
     out, and there the AI proposes the spread; here the two options differ by a single month.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2/dataset.py` (`splits_comment`,
     `SPLIT_WINDOWS`, `_make_splits`); the record `curation/records/alfa_battle_2_0_task_2.md` (CC 2026-10-26); the
     candidate tables `.venv/bin/python -m data_foundry.curation.cli dataset windows alfa_battle_2_0_task_2 --root
     datasets/_dev/tabarena-v0pt2 --window 2 --unit unique` (and `--step 1`).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Months 22-23, 20-21 and 18-19 (implemented) | tests the newest six months | the most training data (oldest 60.3% after the filter); covers months 20-21, the highest default rates | walks back from the newest; leaves out month 17 |
     | B | Months 22-23, 19-20 and 17-18 | tests months 17 to 20 and 22-23 | reaches the oldest month the floor allows; no window right before the newest | the oldest trains on 55.0%; leaves out month 21 |

   * **Recommendation:** A: the floor leaves no other year or season, both options cover the same half-year, and A
     keeps more training data and the months with the highest default rates; a history too short for other windows is
     the reason the rule accepts for walking back. **Decision:** A or B?

   **Notes for the AI:** on A, write the reason into `splits_comment`: the newest window always stays; after the
   repeat-client filter months 16-17 would train on 49.9% (480,765 of 963,811 rows), so the eligible months are 17 to
   23 and three two-month windows leave out one month; the train sides keep 83.4%, 72.9% and 60.3%. Add a CC line to
   the record and a dated CHANGELOG entry (SPLIT-15). On B, `SPLIT_WINDOWS = TemporalSplits(window=2, unit="unique",
   cutoffs=(22, 19, 17))`; `_make_splits` needs no other change. Test 120,428, 108,433 and 114,390 products; train
   after the filter 804,162, 645,527 and 530,245 (83.4%, 67.0%, 55.0%; removed 39,221, 30,878 and 31,770). Then
   rewrite the comment above `SPLIT_WINDOWS` ("the 3 newest pairs"), `task_summary.split`, `splits_comment` (the
   months; the gap figures 13-27% and 35-53% recomputed for the new windows), the accepted warning
   `splits_rows_unused` (recount which products the filter removes from every train side), add a CC line and a
   CHANGELOG entry, and run `dataset check`.

   [^ab-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "Prefer windows in other years, then other seasons, then other months, weeks or days, over the windows
     just before the newest. Walking back from the newest is one choice among others and needs its reason too, such as
     a history too short for others, or a use case that only cares about the weeks after a refit."
   [^ab-split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data;
     a release with two windows above the floor may add one older window that trains on at least 40% of the rows, when
     most test entities recur.
   [^ab-split10]: **SPLIT-10** (Should): when a label is known only some time after its row, train on the rows whose
     outcome is known by the window's start; the exception of 2026-10-21 (Lennart) sets gap 0 because the label's
     delay would break the 50% floor.

   **Lennart (2026-11-11, ok):** As implemented (A).

   **Consistency check (AI, 2026-11-11):** Keep the three newest pairs of months, now that the amended floor opens the
   other half of the second year?

   * **Problem:**
     - Issue 5's A walks back from the newest with the reason the rule accepts, a history too short for others: after the
       repeat-client filter, no pair before months 17-18 kept half the rows[^ab5-15].
     - Under today's amended floor, pairs starting at months 12 to 16 train on 33.5% to 49.9% after the filter, so one of
       them can be the window under half[^ab5-14].
     - Months 12 to 17 are the other half of the second year, a season no window tests.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Months 22-23, 20-21 and 18-19, as marked (implemented) | A: 83.4%, 72.9%, 60.3% after the filter | the most training data; months 20-21, the highest default rates | no window in the other half of the year, now open |
     | b | Months 22-23, 20-21 and 14-15 | swaps 18-19 for 14-15 (90,937 products, 41.1% after the filter) | both halves of the year; keeps the default peak of 20-21 | one window under half |
     | c | Months 22-23, 19-20 and 16-17 | spaced three months apart (83.4%, 67.0%, 49.9%) | spread like this round's other choices | drops 20-21, the highest default rates |

   * **Recommendation:** b: it keeps the newest window and the default peak and adds the other half of the year with one
     train side under half. **Decision:** a, b or c?

   [^ab5-15]: **SPLIT-15** (Should for the other windows): "Walking back from the newest ... needs its reason too, such as
     a history too short for others".
   [^ab5-14]: **SPLIT-14** (Must; amended 2026-11-11, Lennart). The gap-0 exception to **SPLIT-10** still holds.

   **Lennart (2026-11-11, ok):** Reply (b): Months 22-23, 20-21 and 14-15

   **Resolved (2026-11-11, Lennart):** b: months 14-15 replace 18-19, so the windows also test the other half of the
   second year and keep months 20-21. `SPLIT_WINDOWS` is `TemporalSplits(window=2, unit="unique", cutoffs=(22, 20,
   14))`; `_make_splits` is unchanged. Test 120,428, 107,844 and 90,937 products, train after the repeat-client filter
   804,162, 702,678 and 396,171 (83.4%, 72.9%, 41.1%; removed 39,221, 32,861 and 21,497). Months 14-15 are the one
   window under half, signed off: `accepted_check_warnings` accepts `splits_train_under_half`, and `splits_rows_unused`
   is recounted (1,121 products of clients in the test windows: 181 of months 0-13, 940 of months 16-19). For these
   windows a 12-month gap would leave 3-27% for training and a 6-month gap 20-53%, so the gap-0 exception's reason
   holds. `task_summary.split`, `splits_comment` and the comment above `SPLIT_WINDOWS` are rewritten; the LightGBM
   figures measured on the windows of 2026-10-26 are dated as such. The record has the decision and the horizon CC
   lines. `dataset check`: 0 errors, 0 warnings (README not regenerated).

6. **Train floor: keep the window under half the data as the curator's exception, or drop it?**

   * **Problem:**
     - Months 14-15 train on 41.1% of the rows after the repeat-client filter, beside months 22-23 and 20-21 on 83.4% and 72.9%.
     - Since 2026-11-19, every window trains on at least half the data, and a window under half is the curator's exception for the dataset, down to 30%[^split14]; the sign-off (Lennart, 2026-11-11, review issue 5, b) was given under the earlier rule, which admitted such windows beside two at half or more.
     - The definition has 3 windows; the target an IID split would get[^split33] for 963,811 rows is 3; without the window under half it keeps 2.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the window as the curator's exception (implemented) | The accepted warning is reworded to the new rule; split unchanged | Keeps the periods it tests, as signed off; more windows toward the target | It trains on less than half the data |
     | B | Drop the window under half | The windows under half leave the declaration; a rebuild | Every window trains on half the data or more | 1 fewer window and the period it tests |

   * **Recommendation:** A, the sign-off's reason (periods or test rows the newest windows lack) still holds, and no window is under 30%. **Decision:** A or B?

   **Notes for the AI:** on A, reword the `splits_train_under_half` acceptance (drop "SPLIT-14's two tiers admit it", name the curator's exception and this decision) and add a CC line; on B, remove the windows from the declaration, rebuild, and update the splits comment.

   **Andrej (2026-11-19, discuss):** How exactly are the splits done? Could we reduce the window sizes while staying compliant with the use case and get to more than 50% on each train split?

   **Answer (AI, 2026-11-19):** Shortening the windows does not lift the old window: a window's train share is set by its first month, not its length, and months 14-15 start at 41.1% whatever their length; but one-month windows (C) or a later two-month pair (D) give three windows all above half, and C still tests a month from the other half of the second year.

   * **How the split is done today:** `TemporalSplits(window=2, unit="unique", cutoffs=(22, 20, 14))` on `issue_month` (24 reconstructed issue months, 0-23), step set by the cutoffs, no gap (the recorded exception), each train side everything before the window minus the products of clients that have a product in the test window (the repeat-client filter of `_make_splits`). The scored unit is the product (963,811; 26,577 defaults).

     | Window (issue months) | Test products | Defaults | Train before filter | Train after filter | Train share after filter |
     |---|---|---|---|---|---|
     | 22-23 | 120,428 | 3,637 | 843,383 | 804,162 | 83.4% |
     | 20-21 | 107,844 | 3,628 | 735,539 | 702,678 | 72.9% |
     | 14-15 | 90,937 | 2,459 | 417,668 | 396,171 | 41.1% |

   * **What the use case and the source fix:** nothing about the length. The competition names its periods only as "N days" and "the following K days", Alfa-Bank's post gives no refit cadence, so the two months are our convention (signed off 2026-11-11 as such). The time unit is the issue month (the data has no finer date). The gap is fixed: 0 by the recorded exception (a 6-month gap leaves 20-53%), and the repeat-client filter stays. Our assumption: a model refit on all products issued so far serves the next window.
   * **The floor:** after the filter, the first month that keeps half the rows is month 16 (51.3% for a one-month window, 49.9% for the pair 16-17); months 12-15, the first half of the second year, cannot be tested above half at any length.
   * **Shorter layouts above half,** same gap and filter (target 3 windows):

     | Layout | Windows | Test products | Defaults | Train share after filter |
     |---|---|---|---|---|
     | C: one month | 23, 20, 16 | 62,051 / 49,299 / 53,410 | 1,843 / 1,658 / 1,538 | 91.1% / 74.7% / 51.3% |
     | D: two months, oldest moved | 22-23, 20-21, 17-18 | 120,428 / 107,844 / 114,390 | 3,637 / 3,628 / 3,428 | 83.4% / 72.9% / 55.0% |

     - C tests 164,760 products (today 319,209) and month 16, the first whole month of the year's other half above the floor; D keeps the length and the default peak of 20-21 but its oldest window reaches into the other half only with month 17.
     - Other one-month choices are open (any three of months 16 to 23); 21 for 20 changes little (58,545 products, 3.36% defaults in both months).

   **Recommendation:** C: no source ties the length, and one-month windows keep every train side above half while still testing a month of the other half of the year, the reason months 14-15 were chosen. **Decision:** A, B, C or D?

   **Andrej (2026-11-20, discuss):** Why is the oldest window 14-15 and not 18-19?

   **Answer (AI, 2026-11-20):** Lennart chose it on 2026-11-11 (issue 5, b): months 14-15 replaced 18-19 "so the windows also test the other half of the second year" (months 12-17) and keep the default peak of months 20-21; under the floor of the time a window under half was admitted beside two above.

   | Oldest window | Train share after the filter | Test products | Covers |
   |---|---|---|---|
   | 18-19 (the original, issue 5 a) | 60.3% | 121,390 | the newest six months only, with 22-23 and 20-21 |
   | 14-15 (shipped, issue 5 b) | 41.1% | 90,937 | the other half of the second year |
   | 16 (option C, one-month windows 23, 20, 16) | 51.3% | 53,410 | the first whole month of the other half above the floor |
   | 17-18 (option D, two-month windows) | 55.0% | 114,390 | month 17 of the other half, with 18 |

   * Under today's floor (half the data, exceptions down to 30% your call), 14-15 is under half; 18-19 is above it but drops the other half of the year; C and D are the layouts that keep a month of the other half above the floor.
   * A new option E restores 18-19: windows 22-23, 20-21, 18-19, all above half (60.3% to 83.4%), as before 2026-11-11.

   **Recommendation:** C, unchanged: it keeps every window above half and still tests a month of the other half of the year, the reason 14-15 was chosen; E if the other half of the year matters less than the two-month length. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** The main reason to choose an earlier month than just the next one when rolling back was to increase diversity. Did we even measure if the splits are more shifty or diverse? If not do so, then we can decide.

   **Answer (AI, 2026-11-20):** it was not measured before (issue 5 had only PSI per window); measured now: an older window does make the test windows more diverse, and 16 (C) keeps nearly all of 14-15's diversity above the floor, while the windows where the model loses most are 17-18 and 18-19.

   * **Setup:** the definition's frame (963,811 products); each window trained on all earlier months minus the window's repeat clients. Covariate shift: an adversarial LightGBM (ROC AUC, 3 folds grouped by client) between a window and its training side, and between the test windows of a layout; PSI per feature. Performance: an untuned LightGBM scored on held-out clients of its last training months and on the window (gap = held-out minus window, bootstrap SE).
   * **Per window:**

     | Window | Train share | Default rate (window / train) | Adversarial AUC vs training side | ROC AUC held-out / window | Gap ± SE |
     |---|---|---|---|---|---|
     | 14-15 (A) | 41.1% | 2.70% / 2.45% | 0.962 | 0.773 / 0.763 | +0.010 ± 0.011 |
     | 16 (C) | 51.3% | 2.88% / 2.48% | 0.966 | 0.767 / 0.762 | +0.005 ± 0.011 |
     | 16-17 | 49.9% | 2.88% / 2.51% | 0.968 | 0.751 / 0.758 | -0.007 ± 0.011 |
     | 17-18 (D) | 55.0% | 3.00% / 2.55% | 0.969 | 0.779 / 0.743 | **+0.036 ± 0.009** |
     | 18-19 (E) | 60.3% | 3.12% / 2.58% | 0.969 | 0.780 / 0.761 | **+0.020 ± 0.009** |
     | 20-21 | 72.9% | 3.36% / 2.67% | 0.974 | 0.754 / 0.761 | -0.007 ± 0.008 |
     | 22-23 | 83.4% | 3.02% / 2.78% | 0.980 | 0.768 / 0.777 | -0.008 ± 0.008 |

     Every window is easy to tell from its training side (0.96-0.98): the payment mix keeps moving (`share_payment_system_3` leads every comparison), so "shifted from training" does not tell the candidates apart; the model loses clearly only on 17-18 and 18-19.
   * **Diversity between the test windows of each layout** (adversarial AUC between two test windows; features with PSI over 0.25):

     | Layout | Oldest vs 22-23 (or 23) | Oldest vs 20-21 (or 20) | Newer two | Features PSI > 0.25 (oldest vs newest) |
     |---|---|---|---|---|
     | A: 22-23, 20-21, 14-15 | 0.999 | 0.998 | 0.929 | 11 |
     | C: 23, 20, 16 | 0.999 | 0.994 | 0.979 | 8 |
     | D: 22-23, 20-21, 17-18 | 0.994 | 0.977 | 0.929 | 5 |
     | E: 22-23, 20-21, 18-19 | 0.986 | 0.937 | 0.929 | 4 |

   * **What it shows:** going back adds diversity, A most, then C, D, E; C keeps nearly A's (0.999/0.994 against the newer windows) with every window above half the data, whereas E's oldest window resembles 20-21 (0.937). The performance drop points the other way: D and E test the months where a model trained on the past loses most.

   * **Caveat:** the diversity rests mostly on one feature: `share_payment_system_3` (the share of a client's transactions through one payment system) rises steadily toward the newest months and leads every comparison; the median feature hardly moves (PSI at most 0.007 in every window). So a higher diversity mostly means windows further apart along that one trend; whether anything else separates them is not measured (a run without the payment-system features would show it).

   **Recommendation:** C, if diversity across the year is the aim (your stated reason): nearly the diversity of 14-15, all windows above the floor; D, if the aim is the window where models lose most. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** What is the best trade off if we want to have more than 50% of the data on the train side of all splits and also diversity?

   **Answer (AI, 2026-11-20):** C (one-month windows 23, 20 and 16): of the layouts with every window above half, it keeps the most diversity, nearly that of today's 14-15.

   | Layout | Windows | Lowest train share | Oldest vs newest / vs middle (adversarial AUC) | Features PSI > 0.25 | Test products |
   |---|---|---|---|---|---|
   | A (shipped) | 22-23, 20-21, 14-15 | 41.1% | 0.999 / 0.998 | 11 | 319,209 |
   | **C** | 23, 20, 16 | 51.3% | 0.999 / 0.994 | 8 | 164,760 |
   | D | 22-23, 20-21, 17-18 | 55.0% | 0.994 / 0.977 | 5 | 342,662 |
   | E | 22-23, 20-21, 18-19 | 60.3% | 0.986 / 0.937 | 4 | 349,662 |

   * Month 16 is the oldest month that trains on half or more after the repeat-client filter; the two-month pair 16-17 trains on 49.9%, so with two-month windows the oldest window above half is 17-18 (D). C is therefore the most diverse layout above the floor.
   * What C gives up: half the test products of A or D (every window still holds 1,538 or more defaults) and the two-month length, which no source sets.
   * D is the trade-off the other way: the two-month length and the window where models lose most (+0.036 ± 0.009), with less diversity (0.977 against the middle window).
   * The caveat stands: the diversity is mostly one trend, `share_payment_system_3`.

   **Recommendation:** C. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Is your diversity score just measuring that splits with less train data are mroe diverse? This is not what we need if its the case

   **Answer (AI, 2026-11-20):** yes: the score measures how many months lie between two windows, and an older window is both further away and trained on less data. It finds no month that differs from its neighbours, so diversity gives no reason to reach back; the default walk-back from the newest window, E (22-23, 20-21, 18-19), is the layout to ship.

   * **Test:** one-month windows, every month 12-22 against month 23 and every month against the next; adversarial ROC AUC (LightGBM, 3 folds grouped by client, 60,000 rows a side) with all features, without the 19 payment-system features, and also without the 4 `days_before` history-length features.

     | Months apart | Pair | All features | Without payment-system | Without both |
     |---|---|---|---|---|
     | 11 | 12 vs 23 | 1.000 | 0.954 | 0.952 |
     | 9 | 14 vs 23 | 1.000 | 0.924 | 0.921 |
     | 7 | 16 vs 23 | 0.999 | 0.895 | 0.889 |
     | 5 | 18 vs 23 | 0.995 | 0.844 | 0.837 |
     | 3 | 20 vs 23 | 0.981 | 0.735 | 0.731 |
     | 1 | 22 vs 23 | 0.901 | 0.659 | 0.647 |
     | 1 | 12 vs 13 | 0.983 | 0.715 | 0.695 |
     | 1 | 13 vs 14 | 0.953 | 0.662 | 0.659 |
     | 1 | 14 vs 15 | 0.943 | 0.689 | 0.678 |
     | 1 | 15 vs 16 | 0.930 | 0.694 | 0.679 |

   * **Reading:** the score climbs steadily with the months between two windows, with every feature set; neighbouring months differ about equally wherever they lie (0.65-0.72 without the payment shares, all 11 neighbouring pairs from 12-13 to 22-23). The features drift slowly and evenly; no month or quarter stands out. So a "more diverse" layout is only one whose oldest window lies further back, which is also the one with the least training data, as you suspected.
   * **What follows for the layouts above half:** with no distinct period to test, the windows walk back from the newest at the declared two-month length, the rules' default: E, 22-23, 20-21 and 18-19 (83.4%, 72.9% and 60.3% training; 349,662 test products). C and D only gave up length (C) or moved one month back (D) for a diversity that is distance.
   * The model's loss is largest in 17-18 and 18-19 (+0.036 and +0.020 against held-out clients of the same months); E tests 18-19.

   **Recommendation:** E. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Agree.

   **Resolved (2026-11-20, Andrej):** E: `TemporalSplits(window=2, unit="unique", cutoffs=(22, 20, 18))`, no gap (the recorded exception), the repeat-client filter unchanged; the `splits_train_under_half` acceptance removed, as every window now trains on more than half.

   | Window | Test products | Defaults | Train after the filter | Train share |
   |---|---|---|---|---|
   | 22-23 | 120,428 | 3,637 (3.02%) | 804,162 | 83.4% |
   | 20-21 | 107,844 | 3,628 (3.36%) | 702,678 | 72.9% |
   | 18-19 | 121,390 | 3,792 (3.12%) | 581,221 | 60.3% |

   The splits comment gives the reason (the window diversity was only the months between windows). `dataset check`: 0 errors, 0 warnings. Not rebuilt.

   [^split14]: **SPLIT-14** (Must): every window trains on at least half the data, lower only as the curator's exception down to 30%; every test window holds at least 33 scored units.

   [^split33]: **SPLIT-33** (Should): an IID or grouped split gets 3-fold cross-validation with 20, 10, 3 or 1 repeats by the units on its train side; SPLIT-15 aims a temporal split at the same count.

## Reference

Booster
