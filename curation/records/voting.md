---
unique_name: voting
name: Voting
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- TableShift
original_source: Website
year: '2022'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/
- https://tableshift.org/datasets.html#voting
source_row: 703
type_adapter_id: curation-record-v1
---

# Voting

## Comments

task: predict voting participation from a detailed questionnaire.

Data: pre-election interview (features) and a post-election interview (target)

New version of the data available, we might use a new line to distinguish the true data from the task defined by tableshift

AT: I downloaded the most recent version of the dataset and defined a very different task, so I created a separate entry and marked this as duplicate.

## Reference

@dataset{anes_timeseries_cdf_2026,
    author       = {{American National Election Studies}},
    title        = {Time Series Cumulative Data File (1948--2024)},
    year         = {2026},
    month        = feb,
    day          = {5},
    publisher    = {American National Election Studies},
    note         = {Dataset}
    }
