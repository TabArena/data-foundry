---
unique_name: rmftsa_ladata
name: rmftsa_ladata
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '2002'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- openml.org/d/717
- http://lib.stat.cmu.edu/datasets/
- openml 666
source_row: 615
type_adapter_id: curation-record-v1
---

# rmftsa_ladata

## Comments

CC: "Actual task is regression, data apparently was collected between 1970-79. As the data is 6-day spacing, temporal correlations might be not too strong. To be sure, we would need to verify experimentally that results with temporal split are not too different from random split. However as all models have a very low error, temporal data leakage seems likely"

Mortality is leaking, but also seems like a multivariate forecasting task. Unclear if this is the line or borderline, need to finalize

## Reference

Data Sets for 'Regression Models for Time Series Analysis' by B. Kedem and K. Fokianos, Wiley 2002. Submitted by Kostas Fokianos (fokianos@ucy.ac.cy) [8/Nov/02] (176k)
LibStat
