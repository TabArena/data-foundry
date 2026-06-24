---
unique_name: hypertension
name: Hypertension
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- '?'
collections:
- TableShift
source_links:
- https://tableshift.org/datasets.html#hypertension
source_row: 7
type_adapter_id: curation-record-v1
---

## Comments

"We collect all survey questions related to these risk factors and use them as the predictors for this task, along with a shared set of demographic indicators (race, sex, state, survey year, and a question related to income level)."

Split on category again, not a real grouped task. We would have data for sure for overweight or obese patients as well.

Is highly related or even a copy of CDC Indicators of Heart Disease

Given the large overlap in features and task with other (older than TableShift) tasks for brfss data, we judge this to be a "duplicate" in that it is a different version of the same data.
Also note that it counts as IID task in other settings
