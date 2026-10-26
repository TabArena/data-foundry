# numerai28_6

**Outcome:** added (Lennart, 2026-10-22: add as forced IID). Numerai's 2016 Kaggle training sample: 96,320 stocks
with 21 encrypted features and a binary target, no era, date or id, so it ships with random splits tagged
`ForcedIIDFromTemporal`. The AI recommends shipping it; the review panel (focused tier: claim audit, split audit)
refuted no validity claim, and its text fixes are made. Validity: SEL-1 holds; USE-1 approximate (the 2016 rules
state no cadence or horizon); LEAK holds (no duplicates, no copies across the split); LEAK-30 kept on purpose (the
quantile bins were fitted on a larger population that holds our test rows; no raw values exist); SPLIT-8 applied
(no hidden weekly group found by four tests); PROV-7 holds (distinct from numerai_v5_2). Value: a small real signal
(ROC AUC 0.531 logistic regression); under log loss the models sit within about 0.0015 of the dummy (issue 1).
Weighed: data owner's release +, CC0 +, size +, encrypted features -, near-dummy log loss -.

**Main points:** Keep the source's log loss, under which untuned tree models lose to the dummy, or use ROC AUC
(issue 1)? The record's year is settled (2016).

**Record judgment:** valid. The data owner's own 2016 release, distinct from numerai_v5_2 in features, target and
design; the week of a row is lost, and no test finds a trace of it.

**Issues for Lennart:**

1. **Metric: the source's log loss, or ROC AUC as the fallback?**
   - Problem: Numerai's 2016 rules rank models "by accuracy (logloss)" (numer.ai/rules, Wayback 2016-08-30), so the
     definition declares `Metric.source("log_loss")`. Under log loss the dummy scores 0.6931, logistic regression
     0.6912-0.6921 per fold, and untuned LightGBM (0.6945) and random forest (0.6966) score worse than the dummy:
     the score mostly measures calibration near 0.5.
   - Effect on the task: methods separate by about 0.001-0.002 in log loss; under ROC AUC the same models span
     0.516-0.531, also close, but ranking rather than calibration.
   - Implemented: log loss, the source's metric (MET-4).
   - Alternative: `Metric.fallback` (ROC AUC) with the reason that log loss separates models by calibration only.
     Cost: departs from the source's metric, which MET-4 prefers when the source defines one.
   - Rule: MET-4 (the source's metric when one is defined), MET-10 (a metric that cannot separate methods is
     a weighing call). Precedent: the curator's rule of 2026-10-21 trusts a competition's metric.
   - Recommendation: keep log loss (the competition's own metric; calibration is part of the task Numerai set).
   - Decision: log loss, or ROC AUC.

   **Lennart (2026-10-26, change):** we keep roc auc. On the metric: "ROC AUC sounds better here, as it is binary and likely
   more suited. Unless it is mostly about calibration?"

   **Consistency check (AI, 2026-10-26):** it is mostly about calibration at the source, so your own exception applies.
   - Numerai's 2016 rules: "where your model shows the most confident predictions, it needs to be especially correct
     then. We evaluate your models with the Logarithmic Loss measure" (May 2016); "Models are ranked by accuracy
     (logloss) as well as originality" (August 2016); "ranked by their weight and correlation within Numerai's
     meta-model ... Generally, a lower logloss score results in a better rank" (October 2016 to March 2017; the Kaggle
     file is of 2016-12-02). The whitepaper of February 2017 then paid stakes only when "logloss < −ln(0.5)".
   - Calibration decided the pay, and the gap the issue measured is a calibration effect: untuned LightGBM scores log
     loss 0.6945 against the dummy's 0.6931 while ranking above chance (ROC AUC 0.524).
   - ROC AUC would also depart from MET-4 without a fact: bioresponse, binary as well, kept Kaggle's log loss (CC
     2026-10-21), and on the shipped splits log loss separates the models more clearly than ROC AUC (linear against
     random forest: about 17 split standard deviations against 6).
   - Recommendation: keep log loss. Mark "As implemented" to keep it, or confirm ROC AUC with the fact that sets this
     case apart.

**Review panel:** focused tier, 2026-10-22: the claim auditor and the split auditor; the dataset-builder's checklist
before them.

<details><summary>Claim audit</summary>

licence CC0-1.0, log loss as the 2016 metric, distinctness from numerai_v5_2, OpenML 23517 being
another sample (72,404 rows, no shared row), the shuffled file order: hold. Refuted and fixed: the per-value count
range (73-118, not 75-114) and the per-value target SD (0.051-0.058, explained by the features' signal); the
LEAK-30 note "cannot tell" (the counts per value are far more even than sampling gives, variance over mean
0.29-0.37, so the bins were fitted on about 140,000 rows that hold ours; now a `Potential leak, kept on purpose:`
note). Untested: the prediction point and horizon (no 2016 source; the notes now say so). Scripts:
`local-data-warehouse/_runs/2026-10-22_marks/numerai28_6/panel/claims/`.

</details>

<details><summary>Split audit</summary>

keep the forced-IID split. Every feature uses one global set of 1,000 values (no week
fingerprint); the target-rate spread across k-means clusters is reproduced by simulating from out-of-fold
probabilities and is binomial after LightGBM; the closest pairs share the target below chance (0.433 for the
closest 0.1%). The mechanism that inflated numerai_v5_2's IID scores (1-NN agreement 0.618) is absent. The notes
now read the IID ROC AUC as an upper bound. 3 x 3 stratified folds fit the size. Scripts:
`local-data-warehouse/_runs/2026-10-22_marks/numerai28_6/panel/split/`.

</details>
