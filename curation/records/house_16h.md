---
unique_name: house_16h
name: HOUSE_16H
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Missing source information
- Data Quality Issue
collections:
- TabSTAR
- TabArena Reject
source_links:
- https://www.openml.org/search?type=data&id=574
- 'US Census Bureau [http://www.census.gov] (under Lookup Access [http://www.census.gov/cdrom/lookup]: (links broken) and Original source: DELVE repository of data. Source: collection of regression datasets by Luis Torgo (ltorgo@ncc.up.pt) at http://www.ncc.up.pt/~ltorgo/Regression/DataSets.html Characteristics: 22784 cases, 17 continuous attributes.'
source_row: 229
type_adapter_id: curation-record-v1
---

## Comments

CC: "Census data. mostly counts cumulated at different survey levels. Already preprocessed. potential predictive task without temporal connection as it is a snapshot of a year and the median price, use case could be filling missing values or estimating it for non-valued houses. The available data was already preprocessed and it is not possible to restore the original values nor to determine the column names to verify whether the task makes sense"

Given the missing source information and that the temporal indicator is missing. We reject this dataset version.
We can always get more housing data (and have enough in other datasets already)
