---
unique_name: iranian_churn
name: Iranian Churn
checked_by:
- Andrej
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- New IID
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- 10.24432/C5JW3Z
source_row: 664
type_adapter_id: curation-record-v1
---

# Iranian Churn

## Comments

UCI says: "All of the attributes except for attribute churn is the aggregated data of the first 9 months. The churn labels are the state of the customers at the end of 12 months. The three months is the designated planning gap." But the paper says: "“The end of the observation period for each customer is the month in which the customer churns.”"
That means the task definition is not fully correct. It should be T1: observe fixed history of non-churn customers,  WAIT,  T2: collect all churns that occured during the wait time as labels. Instead it is: lcollect data for each individual right up to the churn month for churners → compare with non-churners.
Nevertheless, the features are not collected after the churn and the task is still valid, if we conceptualize it as “identify customers close to churn” rather than “predict churn ahead of time”.

Data was made IID
The upload to UCI in 2020 is not from the original authors. The actual collection period was from September 2006 to September 2007

## Reference

Keramati, A., & Ardabili, S. M. (2011). Churn analysis for an Iranian mobile operator. Telecommunications Policy, 35(4), 344-356.
