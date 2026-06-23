---
unique_name: brazilian_houses
name: Brazilian_houses
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- Not Representative
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '2020'
source_links:
- openml 42688
- kaggle source lost (?)
- https://github.com/marcos-s1/Aluguel/tree/master
source_row: 546
type_adapter_id: curation-record-v1
---

# Brazilian_houses

## Comments

CC: "need to be careful: don't use leaking features and log-transform target (if you don't want severe validation overfitting issues). Also there might be better house price datasets. Also would actually require temporal split. TabRepo version biased due to leak"

Temporal index or timestamp is missing. Cannot split as a temporal task, but it is clearly a temporal task (like many of the other house prices datasets). Without more information, this task can be at best used for some time-invariant feature importance that would also not mean a lot in real-life.

## Reference

?
