---
unique_name: seoul_bike_sharing_demand
name: Seoul Bike Sharing Demand
checked_by:
- Andrej
data_foundry_status:
- 'DF: Suspended'
suggestion: 'No'
decision_markers:
- Time-series (Regression)
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2020'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5F62R
- https://www.openml.org/search?type=data&id=46328&sort=runs&status=active
source_row: 46
type_adapter_id: curation-record-v1
---

## Comments

Data for one year (2017 December to November 2018) is downloaded from the Seoul Public Data Park website of South Korea, where the hourly public rental history of Seoul bikes is available
Hourly measurements, but the task is rather tabular as we have mixed type features and generally low-cardinality features

Looks like the authors used a random split

## Reference

Sathishkumar, V. E., Park, J., & Cho, Y. (2020). Using data mining techniques for bike sharing demand prediction in metropolitan city. Computer Communications, 153, 353-366.
