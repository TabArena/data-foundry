---
unique_name: alvin_smart_money_management_classification_challenge
name: alvin-smart-money-management-classification-challenge
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/alvin-smart-money-management-classification-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/alvin_smart_money_management_classification_challenge/dataset.py
source_row: 902
type_adapter_id: curation-record-v1
---

## Comments

classify purchases into 13 different categories

restrictive data sharing license

**Assessment (AI, 2026-10-07):** Only Train.csv has labels: 373 purchases of 25 users. Test.csv has none, and extra_data.csv has no category in any of its 10,000 rows. After cleaning, 350 rows remain in 9 classes. The three temporal windows hold 36, 27 and 41 purchases from 10, 5 and 12 users. Four classes have only 2 to 5 test rows across all windows. No window design meets the window rules, and the drift rules out IID. Recommend `Too Small` -> `TBD -> 2nd Tier`. Revisit if Zindi or Alvin release Test.csv's labels, which would add 64, 49 and 73 purchases to the windows. The definition masks payees who are private persons (89 of 207 names).
