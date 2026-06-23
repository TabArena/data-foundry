---
unique_name: numerai_v5_2
name: numerai v5.2
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- Review Prio 1 (Atlas)
collections:
- New (BeyondArena)
original_source: Company
year: '2025'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/numerai/example-scripts/tree/master/numerai
source_row: 706
type_adapter_id: curation-record-v1
---

# numerai v5.2

## Comments

temporal split on era, likely need to add feature neutralization: https://github.com/numerai/example-scripts/blob/master/numerai/feature_neutralization.ipynb?

## Reference

Website https://numer.ai/data/v5.2
