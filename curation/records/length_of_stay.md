---
unique_name: length_of_stay
name: Length of Stay
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- 2nd Tier / Scientfic Discovery
collections:
- New (BeyondArena)
domain: medical & healthcare
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/aayushchou/hospital-length-of-stay-dataset-microsoft
source_row: 826
type_adapter_id: curation-record-v1
---

## Comments

Microsoft's hospital length-of-stay sample dataset, explicitly described by Microsoft as synthetic data modeled after real-world inpatient records. The record already carries the AHDS decision marker and the curator confirms the source is simulated. Per the selection criteria, artificial/simulated data is excluded as not representative of real tabular ML. The data is clean and the LOS target is reasonable, but its simulated origin is disqualifying. A human could reconsider if a real-data provenance is found, but on current evidence this is a No.

---

CC: "Data from https://microsoft.github.io/r-server-hospital-length-of-stay/input_data.html

The original data is likely simulated or created ("synthetic data modeled after real world hospital inpatient records"): https://microsoft.github.io/r-server-hospital-length-of-stay/contents.html?utm_source=chatgpt.com

Data looks good to use. Has some feature engineering in this version.

Unclear how to split, need to check but random might work. Furthermore, the target is kind of weird and might be treated as a different task or needs scaling"
