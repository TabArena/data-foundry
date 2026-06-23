---
unique_name: anes_voting_2026
name: anes_voting_2026
checked_by:
- Andrej
data_foundry_status: 'Yes'
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- TableShift
original_source: Website
year: '2026'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/
- https://tableshift.org/datasets.html#voting
source_row: 1029
type_adapter_id: curation-record-v1
---

# anes_voting_2026

## Comments

task: predict voting participation from a detailed questionnaire.

Data: pre-election interview (features) and a post-election interview (target)

This entry refers to the February 5, 2026 version.

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
