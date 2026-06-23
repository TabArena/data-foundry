---
unique_name: tokyo1
name: tokyo1
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- Outdated
- Not Representative
tags:
- Non-IID (Temporal)
- '?'
collections:
- TabArena Reject
- TabSTAR
year: '2017'
source_links:
- openml 40705
- '[SGI.com tech archive](http://www.sgi.com/tech/mlc/db/) (no longer available, [copy on GitHub](https://github.com/acefoxy/DataScience/blob/973d9239ca3190487204ce8037a1d3c8689f95dd/week2/www.sgi.com/tech/mlc/db/tokyo1.names)), [PMLB](https://github.com/EpistasisLab/penn-ml-benchmarks/tree/master/datasets/classification/tokyo1)'
source_row: 548
type_adapter_id: curation-record-v1
---

# tokyo1

## Comments

CC" "Server performance data. Temporal data. Would require time split; weirdly little amount of samples for data from every 5 secs"

Weird old use case, likely not how it would be solved nowadays. Also, a time column is missing to do a proper split, and very small data for the sake of this kind of task. In general, it seems to be a temporal task that we cannot split and a in general outdated dataset
