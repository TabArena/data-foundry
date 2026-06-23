---
unique_name: kick_car_bad_buy_kick
name: kick / CAR_BAD_BUY_KICK
checked_by:
- Andrej
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Kaggle
year: '2011'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.kaggle.com/c/DontGetKicked/overview
- https://www.openml.org/search?type=data&id=41162&sort=runs&status=active
source_row: 723
type_adapter_id: curation-record-v1
---

# kick / CAR_BAD_BUY_KICK

## Comments

CC: "Is from a competition, nice tabular data task. Might require temporal split or some time-invariant feature engineering; original data has more features that are interesting (like KickDate) but unclear if this makes it temporal; kickdate only in description in data. Need to check original data for more, but likely we could ignore time and group-based problems after preprocessing the original data; likely we can ignore temporal impact. No (after preprocessing)."

Old competition without clear restriction on data usage. Can assume public domain

The competition used a random split

## Reference

faysal, Will Adams, and Will Cukierski. Don't Get Kicked!. https://kaggle.com/competitions/DontGetKicked, 2011. Kaggle.
