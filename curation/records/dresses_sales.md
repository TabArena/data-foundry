---
unique_name: dresses_sales
name: dresses-sales
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Missing source information
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2014'
domain: business & marketing
required_split:
- Random (IID)
- '?'
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- 10.24432/C56W3V
- https://www.openml.org/search?type=data&id=23381
source_row: 560
type_adapter_id: curation-record-v1
---

# dresses-sales

## Comments

CC: "Only 500 instances; Corresponds to a relevant task, but recommendation data used in production is typically much more complex; not a recommender system as no users - only item specific predictions"

This dataset is missing any source information and looking for it, I can also not find more. 

Moreover, the task seems to be to predict ratings for one user? In general It is a weird data setup and not having the data source makes this even harder to parse

## Reference

https://www.researchgate.net/publication/293464737_main_steps_for_doing_data_mining_project_using_weka or 10.24432/C56W3V (does not seem to be the real case)
