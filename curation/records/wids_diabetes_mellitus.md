---
unique_name: wids_diabetes_mellitus
name: Diabetes Mellitus
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2021'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/widsdatathon2021/data?select=TrainingWiDS2021.csv
notebook_path: datasets/beyond_iid/new_iid/wids_diabetes_mellitus/wids_diabetes_mellitus.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/wids_diabetes_mellitus/dataset.py
source_row: 652
type_adapter_id: curation-record-v1
---

## Comments

CC: "Good dataset with many features, can checkout leaderboard and code for some examples of preprocessing and data cleaning"

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC of the WiDS Datathon 2021 evaluation page.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `gcs_eyes_apache`, `gcs_motor_apache`, `gcs_verbal_apache`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `gossis_icu_hospital_mortality` (TBD -> Yes, priority 2); a related task: `gossis_icu_hospital_mortality` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 coded columns carry their words.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

## Reference

Karen Matthys, Meredith Lee, NehaGoel, Sharada Kalanidhi, Valerie, and Vani M. WiDS Datathon 2021. https://kaggle.com/competitions/widsdatathon2021, 2021. Kaggle.
