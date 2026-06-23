---
unique_name: wind
name: wind
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
- Time-series (Forecasting)
tags:
- Non-IID (Temporal)
- 2nd Tier / Scientfic Discovery
collections:
- TabArena Reject
- TabSTAR
year: '1978'
source_links:
- https://www.openml.org/d/847
- https://lib.stat.cmu.edu/datasets/wind.desc
- https://www.openml.org/search?type=data&id=503
- https://r-spatial.github.io/gstat/reference/wind.html
source_row: 59
type_adapter_id: curation-record-v1
---

# wind

## Comments

CC: "Regression. Data collected in 1961-78 - outdated. Also not a meaningful prediction task due to the same reasons as stock data"

In TabSTAR WIND_SPEED_IRELAND

On OpenML, it has the same prediction task as stock: predict at time point t some forecast for something else at time point t which you could just read off at time point t. Also clearly forecasting data!

## Reference

Haslett, J. and Raftery, A. E. (1989). Space-time Modelling with Long-memory Dependence: Assessing Ireland's Wind Power Resource (with Discussion). Applied Statistics 38, 1-50.
