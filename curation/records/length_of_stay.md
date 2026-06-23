---
unique_name: length_of_stay
name: Length of Stay
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- 2nd Tier / Scientfic Discovery
collections:
- New (BeyondArena)
required_split:
- '?'
source_links:
- https://www.kaggle.com/datasets/aayushchou/hospital-length-of-stay-dataset-microsoft
source_row: 826
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

# Length of Stay

## Comments

CC: ""Data from https://microsoft.github.io/r-server-hospital-length-of-stay/input_data.html

The original data is likely simulated or created (“synthetic data modeled after real world hospital inpatient records”): https://microsoft.github.io/r-server-hospital-length-of-stay/contents.html?utm_source=chatgpt.com

Data looks good to use. Good some feature engineering in this version. 

Unclear how to split, need to check but random might work. Furthermore, the target is kind of weird and might be treated as a different task  or needs scaling""
