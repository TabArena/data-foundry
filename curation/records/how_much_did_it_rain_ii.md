---
unique_name: how_much_did_it_rain_ii
name: How Much Did It Rain? II (Kaggle 2015, AMS-AI) / How Much Did It Rain? (Kaggle 2015)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
- Data Quality Issue
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Kaggle
year: '2015'
domain: environmental science & climate
required_split:
- Custom
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/how-much-did-it-rain-ii
- https://www.kaggle.com/competitions/how-much-did-it-rain
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

AMS Artificial Intelligence Committee contest on Kaggle (2015): NEXRAD polarimetric radar scans over MADIS rain gauges
in the US Midwest on 20 days per month, April to August 2014, with time and location removed and rows shuffled. Each
scan gives the pixel above the gauge and 5 x 5 neighbourhood percentiles of five radar fields; the target `Expected` is
the hourly gauge total in mm. train.csv: 13,765,201 scans in 1,180,945 gauge-hours. `Expected` has no zeros (minimum
0.01 mm), so this is not a two-regime-zero dataset, and the gauges were not quality-controlled ("many of the gauge
values in the training dataset are implausible", description page): 4.6% of hours exceed 1,000 mm. Rain I
(`how-much-did-it-rain`) is the same source with 2013 data, other radar fields and a CRPS target. It was not downloaded
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
