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
- 2nd Tier / Scientific Discovery
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

## Comments

CC: "Regression. Not a meaningful prediction task, rather interpretability as the task should be framed very differently to make sense for prediction. Daily stock prices from January 1988 through October 1991, for ten aerospace companies - clearly we have much more data for such tasks nowadays"

Data is stock per company and you want to predict the stock of one company from the others at time point t (which you could just read off the internet at that point). Clearly a forecasting task with 10 forecasting time series.

CC (2026-10-22, Lennart): stays retired as `No` + `Time-series (Forecasting)` under TP-10 as amended on 2026-10-22 (leg 1 by the declared metric, trailing summaries allowed): "we know from the context and data state that these are indeed forecasting tasks"; no re-check.

## Reference

StatLib; Luis Torgo
