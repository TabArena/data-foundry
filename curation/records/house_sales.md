---
unique_name: house_sales
name: house_sales
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: GOV Website
year: '2016'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
- https://www.openml.org/d/42731
v2_path: datasets/_dev/tabarena-v0pt2/house_sales/dataset.py
source_row: 721
type_adapter_id: curation-record-v1
---

## Comments

CC: "Time split required. Also spatial data. Time impact not ignorable as collection and prediction was not at one time point"

Feature descriptions: https://www.kaggle.com/datasets/harlfoxem/housesalesprediction/discussion/207885

**Assessment (AI, 2026-10-07):** Provenance traced: the rows are King County Department of Assessments sales (21,386 of 21,613 match a recorded sale on parcel, date and price), first distributed in 2015 as `kc_house_data` with the University of Washington's Coursera ML Specialization; the Kaggle CSV is a cell-for-cell copy. The house features are the assessor's record as of 18-19 July 2015, not of each sale: for 2,151 rows the record changed after the sale, mostly upward, which flatters models (LightGBM RMSE on those rows 0.156 against 0.208 with the record at the sale). The v2 definition rebuilds each sale's record from the county's change log and drops May 2015, which the extract cut short.

## Reference

https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
