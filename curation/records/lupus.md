---
unique_name: lupus
name: lupus
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
- Too Small
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: Kaggle
year: '1996'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/472
source_row: 117
type_adapter_id: curation-record-v1
---

# lupus

## Comments

Looks like a reasonable task for small data, unclear source of the data description but clear paper found.

Original data source might be Weka again.

Original data had 40 more variables as features instead of just time and duration, which should not be super predictive. If we can find this original version of the dataset, we can use it. Otherwise I am not sure.

Less than 96 samples.

## Reference

https://pubmed.ncbi.nlm.nih.gov/2694209/
