---
unique_name: garments_worker_productivity
name: garments_worker_productivity
checked_by:
- Andrej
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
original_source: UCI
year: '2021'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- 10.24432/C51S6D
source_row: 716
type_adapter_id: curation-record-v1
---

# garments_worker_productivity

## Comments

CC: "predict the productivity performance of the working teams in garment production. Date available, requires temporal split"

Ethical problems?
AT: Productivity is measured at team level, not individually, so there shouldn't be ethical concerns

The paper transforms it to a classification task, although regression is possible. Also, they apply models without consideration of time, after the target would already be collected. This makes sense for interpretable ML, to analyze drivers of lower productivity. However, to conceptualize the task for benchmarkling predictive performance, we need to define at which point in time we want to predict and how far into the future we watn to predict.

## Reference

Mining the productivity data of the garment industry
By Abdullah Al Imran, Md Shamsur Rahim, Tanvir Ahmed. 2021

Published in International Journal of Business Intelligence and Data Mining
