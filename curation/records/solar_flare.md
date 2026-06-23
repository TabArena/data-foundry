---
unique_name: solar_flare
name: solar_flare
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
- Outdated
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
year: '1989'
source_links:
- https://doi.org/10.24432/C5530G
- https://www.openml.org/search?type=data&id=44966
source_row: 547
type_adapter_id: curation-record-v1
---

# solar_flare

## Comments

CC: "No (after post-hoc analysis)" -> needs a non-random split

CC: ""Spatial and temporal data but likely with features invariant of both. very simple nominal & ordinal features with low cardinality - might be trivial. 67% full duplicates with target while having only 1389 samples is a problem. If 67% of the test samples were already in the train data this is more similar to a lookup task. Moreover, we could argue to exclude this dataset due to insufficient unique samples <500. 

also on PMLB: https://github.com/EpistasisLab/pmlb/blob/master/datasets/solar_flare/metadata.yaml

Missing source (but mainly, because it is a bad dataset in general: Only 350 unique samples remain after dropping duplicates, some of the target values occur quite rarely (1,3,4,9,20,33,112,884). Linear model among best (not an issue, but an indicator for a non-predictive trivial task). Also, a lot of preprocessing apparently was applied, maybe it even was image data originally.""

Data has no time index or allow for a split either.

## Reference

Bradshaw, G. (1989). Solar flare data set. http://archive.ics.uci.edu/ml/datasets/solar+ flare.
