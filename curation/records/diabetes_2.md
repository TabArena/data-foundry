---
unique_name: diabetes_2
name: Diabetes
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
- 2nd Tier / Scientfic Discovery
collections:
- TableShift
original_source: GOV Website
year: '2024'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: TBD
original_data_state: One Table
source_links:
- https://tableshift.org/datasets.html#diabetes
- https://www.cdc.gov/brfss/index.html
- https://www.kaggle.com/datasets/cdc/behavioral-risk-factor-surveillance-system
source_row: 557
type_adapter_id: curation-record-v1
---

# Diabetes

## Comments

CC: "Used to benchmark distribution shifts between ethnicities, but could also be used with random splits. But would need to clarify license. Source: Centers for Disease Control/BRFSS"

need to check for duplicates, also likely on kaggle in some form. 
Plus, maybe not a real predictive task

Get newest data from webiste

## Reference

https://www.cdc.gov/brfss/
