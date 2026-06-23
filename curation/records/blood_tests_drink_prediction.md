---
unique_name: blood_tests_drink_prediction
name: liver-disorders
checked_by:
- Lennart
- Andrej
data_foundry_status: 'Yes'
suggestion: Disagreement
decision_markers:
- Outdated
- Trivial
- No Good Target (yet)
- Not Representative
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1990'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- openml 8
- 10.24432/C54G67
source_row: 751
type_adapter_id: curation-record-v1
---

# liver-disorders

## Comments

need to create the drinks columns as a target, need to see if it is still a good task then. (drinks>5 ) otherwise, we can just treat it as a regression task...

Unclear if the target make for a relevant, real-world dataset but for now we can add it and filter later again (which might happen)

Discussion: Task is to predict no. Of drinks a person consumes as a proxy for liver diseases based on blood tests. This is not a meaningful task, e.g., what kind of decision would it motivate? If a doctor has the time to collect blood samples, asking for drinking behavior is simple.
Also, there is selection bias as only drinking people are in the sample.

## Reference

? (should be older than 1990 due being used before 1990....)
