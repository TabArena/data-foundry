---
unique_name: arcene
name: arcene
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Missing source information
- Data Quality Issue
tags:
- Non-IID (Grouped)
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
year: '2003'
source_links:
- https://www.openml.org/d/41157
source_row: 38
type_adapter_id: curation-record-v1
---

## Comments

CC: "Part of the NIPS 2003 feature selection challenge. Original task was changed by adding irrelevant features. 10K features in total, so might rather not use this dataset. Only 200 instances; several data sources / groups" - The data consists of 7000 real features and
3000 random probes.

A lot of preprocessing was done to obtain the version of the dataset that is given. Some steps involved using the whole available set, like aligning the peaks of the spectra.

We should, if at all, use the original source. The original website where the challenge creators got the data from is down.

## Reference

https://competitions.codalab.org/competitions/2321 and https://automl.chalearn.org/data and 10.24432/C58P55
