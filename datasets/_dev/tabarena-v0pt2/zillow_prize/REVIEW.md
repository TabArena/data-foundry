# zillow_prize

**Outcome:** added. A regression of the Zestimate's log error for the home sales of round 1 of the Zillow Prize
(2016 to July 2017), each sale with the property file of its year. Temporal: 9 monthly windows with a one-month gap,
scored with RMSE. The AI recommends shipping it, with the small signal and the metric as concerns.

**Main points:** RMSE instead of the competition's MAE (the adapter takes only RMSE). The signal is small.

**Record judgment:** valid with concerns: the signal is small and the squared error is dominated by a few extreme
values (issues 1, 2).

**Issues for Lennart:**

1. **Metric: RMSE (implemented) or the competition's MAE.** 0.4% of the rows have |logerror| > 1 and hold 50% of the
   squared error around the mean (2.1% above 0.4 hold 74%); Zillow traces them mostly to miskeyed prices (FAQ on the
   round-2 metric; discussion 36752). Per window against the train constant (verifier's paired runs, LightGBM):
   L1 loss beats the mean in RMSE on 9 of 9 windows (skill 0.0069-0.0071 over two seeds, median t 2.3-2.4) and the
   median in MAE on 8 of 9 (0.0074); Huber loss 9 of 9 in RMSE (0.0096); L2 loss 4 of 9 (-0.0049), and only through
   the rows with |logerror| > 1. My re-run on the final frame agrees (L1 0.0073, Huber 0.0101, both 9 of 9). So RMSE
   keeps a real signal for robust fits and mainly tests robustness to the extreme rows. Implemented: default RMSE
   (definitions.md, Field mapping), MAE noted. Alternative: `metric = "mae"`, the source's scoring
   (task_probes.md rule 6; `allstate_claims_severity` does this), although the TabArena adapter still falls back to RMSE
   (`BENCHMARK_CHANGES_TODO.md`, "Dataset-specific metrics"). Top-coding the target at +-0.4 (Zillow's round-2 score) is
   not needed for the signal and changes the target.

2. **Is the signal enough?** The task probes flag `no_signal`, `drift_baseline` and `unstable`; untuned models do not
   beat the mean. I kept the task under rule 2 (small but real: robust LightGBM fits beat the mean on 9 of 9
   windows). The competition gap is smaller than it looks: public submissions reached MAE 0.064 against 0.066 for
   predicting zero, but a constant alone closes 0.0008-0.0011 of that 0.002 (on the 4,605 sales after 15 October 2016
   in train_2016_v2: 0.0704 for zero, 0.0696 for the train median, 0.0693 for the mean). Once TabArena results exist,
   `tuned_results.py` should confirm that tuned methods beat the dummy fold by fold; if they do not, this is a
   `TBD -> 2nd Tier` case.

3. **Month instead of the sale date.** Implemented: `transaction_month` (first day), the prediction point of the
   source; the `meta_time_horizon_mismatch` warning is accepted for it. Alternative: keep `transactiondate` (no
   accepted warning; the day is not known on the first of the month and carries no signal, Spearman 0.01).

4. **Windows.** Implemented: 9 monthly windows (the count an IID task of this size gets) with a one-month gap for the
   recording delay. Alternative: the competition's three-month horizon, 3 windows of 3 months (test rows 31,413 /
   24,407 / 10,580), or no gap.

5. **August and September 2017 dropped** (14,737 rows; twice the share of |logerror| > 1: 0.72% and 0.77% against
   0.32-0.43% in January to July 2017). Alternative: keep them as two more windows, accepting the biased sample.

6. **`buildingqualitytypeid` harmonised** onto the coarser 2016 scale (5 levels; the 2017 file has 12). Alternatives:
   keep the raw codes or drop the column; LightGBM R^2 within 0.001 for all three, so the choice is about meaning only.

7. **Licence:** the rules forbid redistributing the data outside the competition (Rules, "Data"). Noted, not a
   verdict reason; it matters if the container is to be published.

8. **BibTeX author:** Kaggle's own citation (its author list) could not be read through the CLI; the entry cites
   `{Zillow}`. Replace with the authors of Kaggle's "Cite" box if wanted.
