---
unique_name: combined_cycle_power_plant
name: Combined Cycle Power Plant
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: UCI
year: '2011'
domain: industry & manufacturing
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5002N
source_row: 49
type_adapter_id: curation-record-v1
---

# Combined Cycle Power Plant

## Comments

CC: ""Data points collected over 6 years; time invariant features, unclear target and prediction goal

predict the net hourly electrical energy output (EP) of the plant - seems to be time-series, I don't think the features are time-invariant and the description recommending random splits could be wrong.

The dataset contains 9568 data points collected from a Combined Cycle Power Plant over 6 years (2006-2011), when the plant was set to work with full load.""

Data does not have a timestamp.... can only be treated as forced IID.

This is more IID scientific discovery than a non-forecasting predictive task. But without time, this forecasting is also not possible.

"All the input variables and target variable, which are defined as below, correspond to average hourly data received from the measurement
points by the sensors" -> in other words, you would have the target whenever you have the features. So it is clearly a wrong setup and we cannot recover it! But anyhow, maybe a nice time-independent task, or a causal task? Or one forecasts the other variables and then uses the model, thus making it IID?
"was collected over a six-year period (2006–2011)" -> clear temporal connections between samples that could be leaked by just "looking up close days"

Cannot use this data as the source data is missing, might want to contact them to ask for the original data.
It is likely in any case a multivariate forecasting task.

## Reference

Prediction of full load electrical power output of a base load operated combined cycle power plant using machine learning methods
By Pınar Tüfekci. 2014

Published in International Journal of Electrical Power & Energy Systems
