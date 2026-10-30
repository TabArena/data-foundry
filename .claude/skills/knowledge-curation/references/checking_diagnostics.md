# Label maturity and duplicate contamination

These are descriptive extensions of leak probes 13 and 5. Use them to investigate
the existing label-availability, censoring and copy rules, not as automatic verdicts.
The [Data Foundry commands](../../knowledge-data-foundry/references/checks_and_probes.md)
load the canonical frame and shipped splits without editing a definition or fitting models.

## Label maturity

When the label semantics allow delayed observation, look for suppressed event rates
near the release boundary. Choose an appropriate historical reference, aggregation
windows and end buffers before interpreting the results. Inspect the full grid,
including a window over all retained history, rather than selecting a reassuring endpoint.
Retain daily counts and the reference's period counts/rates so its stability can be checked.
The helper reports previous equal-width and all-earlier comparisons as sensitivity checks,
and marks overlap with the fixed reference. Overlapping comparisons are dependent.

For binary event labels, `label_maturity.run(dates, labels, reference_start=...,
reference_end=..., positive_label=1)` reports event rates and recent/reference ratios.
Windows and buffers are calendar-day counts; `None` means all history. End dates are
exclusive and timestamps are converted to UTC calendar days. Select the calendar deliberately
if the task uses a local day. Missing dates/labels are rejected rather than silently dropped.
Empty windows and zero-event references yield undefined ratios, not passing checks.

An optional `min_rate_ratio` is a case-specific screen. For L&T loan default,
Myunghwan requested a recent rate at least 90% of an approximately stable historical
rate. All 49 combinations of seven windows and seven end buffers met that criterion;
the newest rates rose. The reference was short and only approximately stable:
September's rate was 88.97% of August's. The decision was to retain the release tail.

Keep three questions separate:

1. Is the observed release-boundary rate pattern consistent with delayed recording?
2. Does the evidence support trimming the end of this release?
3. Was each training label available at its simulated historical refit cutoff?

Rate sensitivity informs the first two. Changing case mix can hide or mimic censoring,
and an older reference is not automatically mature. Actual availability requires timestamps
or an applicable source rule. A passing grid is not proof of complete follow-up. L&T's
separate zero-training-gap decision was an explicitly retrospective approximation;
neither that decision nor its 90% criterion changes the general availability rules.

## Duplicate contamination

Count on the actual train/test arrays, using the declared predictors. Include text and
datetime predictors; exclude targets, grouping metadata and scoring-only columns.
Record any extra exclusions. Missing cells compare equal; no rounding, imputation,
similarity clustering or row sampling is applied. A matching profile is not proof of
a repeated person, compound or event.

`duplicate_contamination.run(df, target, splits)` checks every supplied split and reports:

- Test rows with no training-profile match, or any match.
- One or two-or-more same-label training matches, and the corresponding different-label counts.
- Mixed cases having both same- and different-label matches.
- Exclusive categories that partition all test evaluations, alongside overlapping inclusive counts.

The denominator is test appearances, including repeated appearances across repeats;
do not describe it as a count of independent people. `include_rows=True` retains test
positions and exact match counts for independent checks and saved-prediction alignment.

Where predictions are retained, compare the same model's losses on matched and unmatched
test rows. The optional `losses` packet contains `frame_digest` and one `folds` entry per
split, with the exact ordered `train_indices`, `test_indices` and per-row `losses`.
`frame_digest(df)` binds ordered values, column names and semantic dtypes. Validate the
artifact's data, preprocessing, model and scorer provenance before constructing the packet;
the helper checks frame/split alignment, not model provenance. It reports counts, sums
and mean per-row losses. These are not arbitrary subset metrics: mean squared error
needs a square root for RMSE, and ROC AUC has no such per-row decomposition.

In Tanzania tourism, 5,469 of 55,518 test appearances (9.8509%) matched a training
profile; 2.4623% had both same- and different-label matches. Retained LightGBM log
loss was 0.9100 on matching profiles and 1.1004 on nonmatching profiles. These are
different subsets, so the gap is descriptive, not a causal estimate of duplicate-induced
optimism. Respondent/party identity remained unverified; Myunghwan retained all rows
and the random split with that qualification.

For a suspected lookup shortcut, also compare a train-only profile-lookup baseline
with the model on the same folds and metric, specifying the unseen-profile fallback.
CPS88 wages used training-profile medians against modeled log1p-wage MAE; the model
beat lookup on every fold. Lookup evidence can inform the decision but does not
authenticate entity identity. A grouped retraining comparison, when appropriate,
answers a different question and must retain its changed population and split scope.
