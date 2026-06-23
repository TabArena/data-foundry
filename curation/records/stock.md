---
unique_name: stock
name: stock
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
year: '1991'
source_links:
- https://www.openml.org/d/841
- https://www.openml.org/search?type=data&id=223&sort=runs&status=active
source_row: 58
type_adapter_id: curation-record-v1
---

# stock

## Comments

CC: "Regression. Not a meaningful prediction task, rather interpretability as the task should be framed very differently to make sense for prediction. Daily stock prices from January 1988 through October 1991, for ten aerospace companies - clearly we have much more data for such tasks nowadays"

Data is stock per company and you want to predict the stock of one company from the others at time point t (which you could just read off the internet at that point). Clearly a forecasting task with 10 forecasting time series.

## Reference

StatLib; Luis Torgo
