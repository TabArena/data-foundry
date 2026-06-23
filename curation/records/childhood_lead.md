---
unique_name: childhood_lead
name: Childhood Lead
checked_by:
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Needs extensive data wrangling
- No Good Target (yet)
tags:
- Non-IID (Temporal)
collections:
- TableShift
source_links:
- https://tableshift.org/datasets.html#childhood-lead
- https://www.kaggle.com/datasets/cdc/national-health-and-nutrition-examination-survey?select=demographic.csv
source_row: 627
type_adapter_id: curation-record-v1
---

# Childhood Lead

## Comments

"task is to identify whether a respondents' blood level exceeds the BLRV using only questionnaire data." -> questionable setup due to having it at the same time, but fair to build as a task

TableShift used 2017-2018 version. It seeums not all years have data / the same data, but we could use newer data?

again split the domain via a categorical variable for which we have samples in the real world at the same time as other samples for such task, no real selection problem. So it is again a created problem for the benchmark.

Could build any task from this. Unclear if any task is a real task that has been used in real-world or was made-up/desigend as in TableShift. 
Likley we could argue for some task like TAbleShift.
