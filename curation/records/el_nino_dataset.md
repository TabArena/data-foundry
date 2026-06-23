---
unique_name: el_nino_dataset
name: El Nino Dataset
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
collections:
- TabArena Reject
- TabSTAR
year: '1999'
source_links:
- openml.org/d/839
- openml 563
- https://www.kaggle.com/datasets/uciml/el-nino-dataset
- 10.24432/C5WG62
source_row: 61
type_adapter_id: curation-record-v1
---

# El Nino Dataset

## Comments

CC" Regression. Temporal and spatial data. Measurements start in 1980 - might be outdated, especially as more sophisticated approaches for weather prediction should exist nowadays"

All data points are collected at the same time. Moreover, it contains data from groups of sensors. This is a multivariate time series forecasting task. We do not predict a target that we would not automatically obtain at time point t. Moreover, the original goal was to forecast for 2 years if possible

## Reference

Pacific Marine Environmental Laboratory National Oceanic and Atmospheric Administration US Department of Commerce
