---
unique_name: airlines
name: airlines
checked_by:
- Andrej
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Not Representative
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '2009'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
- Forecasting
original_data_state: One Table
source_links:
- https://community.amstat.org/jointscsg-section/dataexpo/dataexpo2009
- openml 1169
source_row: 617
type_adapter_id: curation-record-v1
---

# airlines

## Comments

CC: "Requires temporal split. Also better datasets for this task might be available as only 7 features are given; has nosiy duplicates; original data has 120 million rows?; used not as a predictive task according to the website? original question was only about if the weather can predict the delays?"

Check with data from: https://www.transtats.bts.gov/
Openml 42728

Could generally be used, but the available features are limited and could be extended with some work

See: Aeolus for better flight delay dataset

Get newer version of data, likely needs more features to be made a good dataset

## Reference

?
