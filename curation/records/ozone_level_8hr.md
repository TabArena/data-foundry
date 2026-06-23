---
unique_name: ozone_level_8hr
name: ozone-level-8hr
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2008'
source_links:
- 10.24432/C5NG6W
- https://www.kaggle.com/datasets/prashant111/ozone-level-detection
source_row: 625
type_adapter_id: curation-record-v1
---

# ozone-level-8hr

## Comments

CC: "Likely requires temporal split; also temporal features sampled at certain intervals, also spatial domain "

Use one of the datasets; 1h seems to be the harder task based on paper results. Unclear what class labels are in data on UCI, I guess 1 is ozone day and 0 is a normal day, check the distribution. Targetr seems to be just a forecasting task mapped to a binary

Needs more thought and time to read the paper to understand how to model this correctly and if it is not just a forecasting dataset

## Reference

Forecasting skewed biased stochastic ozone days: analyses, solutions and beyond, Knowledge and Information Systems, Vol. 14, No. 3, 2008.
