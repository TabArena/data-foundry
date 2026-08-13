---
unique_name: student_portuguese_performance
name: archive_r56_Portuguese
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2008'
domain: education
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/whenamancodes/student-performance/data
- https://doi.org/10.24432/C5TG7T
- https://www.openml.org/d/44967
notebook_path: datasets/beyond_iid/new_iid/student_portuguese_performance/student_portuguese_performance.ipynb
source_row: 763
type_adapter_id: curation-record-v1
---

## Comments

CC: "Cortez and Silva, 2008. Students from two schools - predict student performance. Would require temporal split or time-invariant features. The latter can be assumed to be true. If the features would have been created at a similar time as the target this would be a scientific discovery task more than a predictive performance task. But most features seem time-invariant. need to select a target as there are multiple possible, also might need to exclude some features as intermediate grades or non-time-invariant features. No objection if G features/targets are handled"

We can treat the g3 as the prediction target and use g1 and g2 or drop it and just aim for predicting this for the next year for these students. might have some problem as features talk about the entire time or past behavior for the newest grade

We use the port data and ignore the math data, as it is more or less a different version/target (382 students overlap) and the port data is larger. We only predict G3

## Reference

Cortez, P., & Silva, A. M. G. (2008). Using data mining to predict secondary school student performance.
