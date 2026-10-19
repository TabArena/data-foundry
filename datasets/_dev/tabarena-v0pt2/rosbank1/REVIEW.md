# rosbank1

**Outcome:** added. Churn after a card's three-month grace period (task 1 of Rosbank's 2018 competition), one row per
client from its card transactions. Temporal: monthly windows of the period end after a three-month label gap; periods
ending from 2018 on are cut because their labels were incomplete at the extract. The AI recommends shipping it.

**Main points:** Periods from 2018 are cut, because their 3-month labels were incomplete at the extract. Cut B (keep
January 2018) is the alternative.

**Record judgment:** valid with concerns: the newest labels are right-censored (handled by the cut), the time column
is estimated (issue 3), and the label draw date is unknown (issue 4).

**Issues for Lennart:**

1. **Target: churn or the spend regression.** The two tasks are one signal (target_flag = target_sum > 0). Implemented:
   churn (task 1, AUC; the task CoLES and pytorch-lifestream benchmark). Alternative: a `rosbank1_reg` folder for task 2
   (scored with RMSE; best private 3.844, so probably on a log scale). On the shipped windows, untuned LightGBM R^2 is
   0.43 / 0.46 / 0.37 on log1p(target_sum) over all clients (44.8% zeros, mostly the churn task again) and 0.26 / 0.12 /
   0.15 on the log spend of the 2,645 clients who kept buying (40, 74 and 336 test clients); random 3 x 3: 0.38 and
   0.21.

2. **Regime: temporal with a 3-month gap, or the competition's random split.** Implemented: temporal (clients are scored
   as their periods end; a refit only knows outcomes three months old; churn drifts from 53.0% in 2017Q1 to 35.8% in
   2017Q4 as the type2 acquisition channel grows from 17% to 41%). Cost: the gap and the 50% floor leave
   October-December 2017 as the only test months (701 clients). Alternative: IID 3 x 3 over the 4,791 clients, the
   competition's and CoLES's protocol: LightGBM 0.824 (SE 0.001).

3. **The time column is an estimate.** No product or period dates in the data. 2,939 of 5,000 clients transact over
   80-92 days, so `period_end` = first transaction + 3 months, or the last transaction when later (565 clients; 213 have
   over 100 days of history, which the release does not explain). Alternative: the last transaction date (simpler), but
   a client who stopped early would sit up to three months before its real period end.

4. **Cut C or cut B (when were the labels drawn?).** Implemented C: periods ending before 2018-01-01, label windows
   closing by 2018-03-31, inside the transactions (they end 2018-04-02), which is safe whatever the draw date before the
   opening on 2018-04-27. Alternative B: keep January 2018 too (label windows close by 2018-04-30, complete only if the
   labels were drawn at the very end of April): a fourth window of 62 clients (18 churned, train 4,090), LightGBM 0.813
   in my run (0.822 in the verifier's). January's churn (29.0%) does not look censored, February's (39.6%) slightly,
   March's (66.7%) clearly, which fits a draw in late April; nothing published gives the date.

5. **Feature width.** The 97 MCC codes give 294 of the 347 features, mostly empty. Untuned LightGBM, mean over the
   shipped windows / random 3 x 3: no MCC breakdown (53 features) 0.847 / 0.820, 10 codes (86) 0.860 / 0.823, 30 codes
   (146) 0.863 / 0.822, 97 codes (347) 0.860 / 0.817. Implemented: 97, faithful to the published baseline (as
   alfa_battle_2_0_task_2 kept its organizers' set). Alternative: 10 or 30 codes.

6. **Test windows are small.** December 2017 holds 63 clients (23 churned) and November 123 (49): above the ~50-row
   guideline, but the task probes cannot separate model families over 3 windows (`no_spread`). A longer history does not
   exist in the release.
