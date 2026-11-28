"""Leak probes: what a model learns from the data that it should not.

Tooling-independent: ``run`` takes a pandas frame, its target column and problem type, the splits as
``(train_idx, test_idx)`` row positions and the group columns (which are not features), fits untuned LightGBM on the
first ``n_splits`` splits, prints each number as soon as it is known and returns them all:

* the score with all features (ROC AUC, one-vs-rest for multiclass, or R^2), and of a depth-2 and a depth-3
  decision tree: a shallow tree close to the full model means the label is a rule over a few columns (a definition,
  a lookup, or a label assigned from the features);
* the score of each feature alone, and of each column's missing-value indicator alone, best first;
* the score without each of the three strongest single features (a drop-one test misses a column that has a
  copy, such as kick's ``WheelType`` and ``WheelTypeID``: drop such columns together);
* on every split given (not only the probed ones, and every row), the share of test rows whose feature vector has an
  exact copy in train, and how the copies split by label: the same label only or another label only, each with one
  copy or two or more, and both labels (``copy_counts``); when the data has string or datetime columns, the same with
  them included; and for each string column of more than 50 distinct values the share of test rows whose value occurs
  in train on the first split (a copy at the level of a SMILES string or a text);
* each such string column alone, and all features with the string columns, encoded as in the task probes (TF-IDF +
  SVD fitted on the train side; character n-grams for one-token strings such as a SMILES): a text whose content
  gives the label away scores close to the full model on its own;
* the 1-nearest-neighbour label agreement (R^2 for regression) for the closest tenth of the test rows and for
  all of them, against chance;
* for a binary target, the ROC AUC of a label-free score: each row's distance to its nearest other row.
* for a classification target, the score of the number format alone (probe 17): the decimals each value of a float
  column is written with, all columns together and the three best alone. Classes recorded differently give
  themselves away here (gallstone_disease 0.947 before the fix, 0.557 after).

With a training weight (``sample_weight``: a rate's realized denominator, such as the years insured), every fit is
trained with it as each row's weight and every R^2 and ROC AUC weights the test rows by it, the 1-NN R^2 and the
distance score included; the screen, the copies and the 1-NN label agreement stay counts of rows.

``fill_counts`` (probe 18) needs the rows in the source's order, which ``run`` does not get: it counts, per column and
class, the cells that lie on a straight line between the cells above and below, the trace of gaps filled by
interpolation. Run it on the raw table.

``weight_proxy`` (probe 22) asks whether the features carry a realized weight, such as the time on risk of a rate
target that a claim can cut short: a LightGBM of the weight on the features, the task's metric with the weight added as
a feature against the honest fit (the leak reference), each top feature's gain through the weight with its SD over
splits and seeds, and the weight alone: the score of 1/weight for a Gini metric, of a fit of the target on the weight
for any other. ``weight_proxy_lines`` prints it.

The raw state has four more probes, which read the table before ``_clean`` and, through the lineage (the raw
position of each curated row), what ``_clean`` did to it: ``row_order`` (probe 10, the target in the source's row
order), ``removed_rows`` (probe 19, the target of the rows ``_clean`` removed against the kept ones),
``dropped_column_proxies`` (probe 20, each raw column the definition drops, alone against the target on the shipped
splits) and ``raw_copies`` (probe 21, copies before deduplication, by label). ``raw_lines`` prints them.

Probe 23 is for a split forced from temporal (SPLIT-8: IID, or grouped by entity over stacked periods), which puts
rows of one period on both sides. ``period_outcome`` predicts each test period by a fit without the training rows of
its period and by one without as many random training rows: what the period's own training rows add, pooled and within
a period, is the period's outcome shared across the split (a shock of the year). ``shared_units`` counts the test rows
whose unit (a group column, the exact profile of the inputs, the profile without the period column) has training rows,
and what a lookup of their target adds. Both fit regularised LightGBM (``_regularised``) with the training weight and
score the task's metric; ``period_columns`` and ``outcome_periods`` find and cut the period column.

``target_by_period`` (probe 13) needs the time of each row: it sets the target of the newest periods (an event rate,
the class shares, a duration's p50 and p90, a count's zero share, the rows per day) against the band the earlier
periods give, the test for a target right-censored at the release end. It fits no model.

Wide data: with more than ``max_single_features`` columns, only that many enter the single-feature fits, and the
output says how many were screened out. The screen keeps the columns that best explain the label alone on the first
split's training side: a step function over 10 quantile bins (the levels of a categorical of at most 10; missing
values are a bin of their own), scored by mutual information (the share of variance for regression) less its expected
value without signal. A categorical of more levels gets the out-of-fold score of its per-level label distribution, in
the same units. Against full scans, the default keeps all 8 best single features of coad_colon_adenocarcinoma and
ov_ovarian_cancer, 7 of lgg_low_grade_glioma's (its best score included) and the 50 best of
mercedes_benz_greener_manufacturing (370 categoricals); ranking by the gain of one LightGBM fit missed coad's 41 best.
Columns with the same missing values share one missing-indicator fit, and more than ``max_single_features``
distinct patterns are screened the same way. The all-feature, shallow-tree and drop-one fits use every column.

A multiclass ROC AUC is the mean of the one-vs-rest ROC AUCs over the classes present in the test fold (a grouped or
temporal fold can lack a class); a class the training side lacks gets probability 0. String and datetime columns
are not inputs of the other fits (a duration enters as seconds), group columns are not features, and train and test
rows are capped at ``max_rows`` each. The numbers are indicative (untuned models, a few splits) and meant for
comparing the data with a suspected fix.

The modules: ``core`` (``run`` and the fits it shares), ``raw`` (the raw state), ``periods`` (probe 13 and the period
column), ``fits`` (the fits of the target of probes 22 and 23), ``weight`` (probe 22), ``forced`` (probe 23) and
``modes`` (the probes on a dataset, as ``data-foundry probe leak`` runs them). The names below are the ones the other
probes and the command use.
"""

from __future__ import annotations

from data_foundry.probes.leak.core import (
    copy_counts,
    copy_line,
    fit_score,
    neighbour_space,
    profile_codes,
    run,
    say,
    score,
    written_decimals,
)
from data_foundry.probes.leak.fits import FROM_SHIPPED, TO_SHIPPED, TargetFits, forced_inputs
from data_foundry.probes.leak.forced import period_outcome, period_outcome_lines, shared_units, shared_units_lines
from data_foundry.probes.leak.periods import (
    PERIOD_FREQS,
    outcome_periods,
    period_columns,
    period_lines,
    period_times,
    target_by_period,
)
from data_foundry.probes.leak.raw import (
    dropped_column_proxies,
    fill_counts,
    raw_copies,
    raw_lines,
    removed_rows,
    row_order,
    straight_line_fills,
)
from data_foundry.probes.leak.weight import weight_proxy, weight_proxy_lines

__all__ = [
    "FROM_SHIPPED",
    "PERIOD_FREQS",
    "TO_SHIPPED",
    "TargetFits",
    "copy_counts",
    "copy_line",
    "dropped_column_proxies",
    "fill_counts",
    "fit_score",
    "forced_inputs",
    "neighbour_space",
    "outcome_periods",
    "period_columns",
    "period_lines",
    "period_outcome",
    "period_outcome_lines",
    "period_times",
    "profile_codes",
    "raw_copies",
    "raw_lines",
    "removed_rows",
    "row_order",
    "run",
    "say",
    "score",
    "shared_units",
    "shared_units_lines",
    "straight_line_fills",
    "target_by_period",
    "weight_proxy",
    "weight_proxy_lines",
    "written_decimals",
]
