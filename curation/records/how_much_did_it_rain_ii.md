---
unique_name: how_much_did_it_rain_ii
name: How Much Did It Rain? II (Kaggle 2015, AMS-AI) / How Much Did It Rain? (Kaggle 2015)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Duplicate
original_source: Kaggle
year: '2015'
domain: environmental science & climate
required_split:
- Custom
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/how-much-did-it-rain-ii
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Duplicate`, PROV-6; PROV-4): Kaggle's description page: "How Much Did It
Rain? II is focused on solving the same core rain measurement prediction problem, but approaches it with a new and
improved dataset and evaluation metric." It is the second stage of the AMS-AI contest whose first stage is
`how_much_did_it_rain`: the same network, Rain I's test year and months, the same task (hourly gauge rain from
polarimetric radar), another metric, and no dry hours.
- Source: the AMS Artificial Intelligence Committee with the Climate Corporation on Kaggle, "How Much Did It Rain?
  II", 17 September to 7 December 2015 (Kaggle API), "a second iteration of the How Much Did It Rain? competition"
  (description page). The host, thread 16555
  (https://www.kaggle.com/competitions/how-much-did-it-rain-ii/discussion/16555): "Welcome to the second stage of the
  competition!", and of the AMS talk on the first stage: "The changes in this second stage are that the metric is
  different and the format is simplified. However, the key concepts are still applicable." Rain I's data page: train
  "the first 8 days of Apr to Nov 2013", test "the same radars and gauges over the same months but in 2014"; Rain II:
  "NEXRAD and MADIS data collected on 20 days between Apr and Aug 2014 over midwestern corn-growing states", so its
  labelled rows are another slice of Rain I's unlabelled test year and months. As published (earlier AI triage,
  2026-10-20, measured): train.csv, 13,765,201 radar scans in 1,180,945 gauge-hours; the reading above the gauge and
  5 x 5 neighbourhood percentiles of reflectivity, composite reflectivity, RhoHV, Zdr and Kdp, with `minutes_past` and
  `radardist_km`; target `Expected`, the gauge's hourly total in mm, minimum 0.01 mm.
- Why neither stage is a distinct task (PROV-7 not met): both estimate the same quantity from the same kind of radar
  inputs for the same use; CRPS (Rain I) against MAE (Rain II) is a difference of metric. Rain I is the canonical
  record (TBD -> 2nd Tier, priority 2): it keeps the dry hours (rain in about 14% of them, Rain I thread 11484) and has
  per-hour radar products on which gradient boosting won (Rain I thread 14242); Rain II has no dry hours, so it serves
  only hours whose gauge recorded rain, which a radar estimate cannot know in advance (USE-3). Against it, not
  decisive: the host calls Rain II's data "new and improved" (a page, rank 3), and Rain I was never downloaded.
- Reopen: Rain II comes back if `how_much_did_it_rain` fails at /add-dataset for a reason specific to its own release
  (its files are listed on Kaggle but need the rules accepted).
- Metric: MAE (Kaggle API `evaluationMetric`: "Mean Absolute Error"), scored only on Ids with a non-null `Ref`
  (host, thread 16572).
- Not decisive, for the record: label noise ("many of the gauge values in the training dataset are implausible", data
  page; host, thread 16555: "we did not throw out any observations"); time and place censored, so only a forced IID
  split (SPLIT-8); the winner's RNN on the raw scan sequences was "best by some distance" (thread 17766), with gradient
  boosting and random forests on hourly aggregates below it (SEL-12, SEL-13 boundary).
- Reject check (AI, 2026-10-27): stands. PROV-6 (Must). Kaggle's description page calls Rain II "the same core rain
  measurement prediction problem" with "a new and improved dataset and evaluation metric", and its 2014 training hours
  lie in Rain I's test year and months (https://www.kaggle.com/competitions/how-much-did-it-rain-ii).

**Assessment (AI, 2026-10-30):** tag `Two-Regime Zeros` removed under the curator's definition of the tag (Andrej,
2026-10-30, policy question 4 of the zero-inflated review: "If the low value is by far the most frequent one and
independent of the remaining target distribution, then we can treat it as two regime zero, otherwise not"). Measured on
`train.csv` (1,180,945 gauge-hours): the minimum, 0.01 mm, holds 1.7%; the most frequent value, 0.254 mm (one tip of a
0.01-inch gauge), holds 25.0%, followed by two, three and four tips at 10.3%, 6.0% and 5.9%. That is the first step of
one count of tips, not a regime apart from the rest. The verdict (`No`, the second stage of `how_much_did_it_rain`) does
not change.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

AMS Artificial Intelligence Committee contest on Kaggle (2015): NEXRAD polarimetric radar scans over MADIS rain gauges
in the US Midwest on 20 days per month, April to August 2014, with time and location removed and rows shuffled. Each
scan gives the pixel above the gauge and 5 x 5 neighbourhood percentiles of five radar fields; the target `Expected` is
the hourly gauge total in mm. train.csv: 13,765,201 scans in 1,180,945 gauge-hours. `Expected` has no zeros (minimum
0.01 mm), so this is not a two-regime-zero dataset, and the gauges were not quality-controlled ("many of the gauge
values in the training dataset are implausible", description page): 4.6% of hours exceed 1,000 mm. Rain I
(record `how_much_did_it_rain`, https://www.kaggle.com/competitions/how-much-did-it-rain) is the same source with 2013 data, other radar fields and a CRPS target. It was not downloaded
(rules not accepted on this account); its forum reports that predicting 0 mm everywhere beat the sample solution
(discussion 11484), so its target may hold the zeros Rain II lacks.

No, for modality and split. The features are radar image pixels and neighbourhood statistics over a scan sequence,
remote sensing as in `satimage`, and the winner used RNNs on the raw sequences (discussion 17766). The host's test was
the last 10-11 days of each month, and with time and place removed "it is impossible for you to create a
cross-validation set that is truly independent" (discussion 16680); test labels were never released. Probe on hourly
aggregates (random split, hours with a reflectivity value, up to 70 mm): R^2 0.35 on log1p against 0.22 for the
Marshall-Palmer estimate, MAE 2.27 mm against 2.75 for the median. Terms: data for the purpose and duration of the
competition only (rules). Nothing left to check that would change the verdict.

## Reference

Lakshmanan, V., A. Kleeman, J. Boshard, R. Minkowsky, A. Pasch (2015). The AMS-AI 2015-2016 Contest:
Probabilistic estimate of hourly rainfall from radar. 13th Conference on Artificial Intelligence, American
Meteorological Society, Phoenix, AZ (citation as given on the competition's data page; not read).
https://www.kaggle.com/competitions/how-much-did-it-rain-ii

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
