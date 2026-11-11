# alfa_battle_2_0_task_2

**Outcome:** added. You shipped it on 2026-10-26. Under the rule on choosing test windows, rewritten on 2026-11-10,
the AI recommends keeping the three windows, issue months 22-23, 20-21 and 18-19 (issue 5): once the repeat-client
filter removes the test window's clients from training, the next older pair (16-17) trains on 49.9% of the rows, so
three two-month windows can only leave out one of the seven eligible months. The two-month horizon is kept, as a
convention: no source gives one. `dataset.py` is unchanged until you decide.

**Main points:** Keep months 22-23, 20-21 and 18-19, or test 22-23, 19-20 and 17-18 (issue 5)? Sign off the
two-month horizon.

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

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | Two months (implemented) | windows of two issue months, no gap (your call of 2026-10-26): eligible test months 17 to 23 | three windows fill six of the seven eligible months | no source gives a horizon or a refit cadence |
  | B | One month | 8 candidates above the floor after the filter, months 16 to 23, 49,000 to 62,000 products each | more candidates to choose from | three spread windows would test 3 of the 8 months, about half today's test products |
  | C | Three months | two candidates above the floor after the filter, 21-23 and 18-20 | more products per window | only two windows; a third, 15-17, trains on 44.3%; the exception for an older window at 40% needs test entities that mostly recur, while 76% of the newest window's test products have no earlier product of the client |

* **Recommendation:** A: no source names a length, and two months fill six of the seven eligible months with three
  windows. **Decision:** A, B or C?

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
