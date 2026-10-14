---
unique_name: indian_liver_patient_dataset
name: ilpd
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2012'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D02C
notebook_path: datasets/beyond_iid/new_iid/indian_liver_patient_dataset/indian_liver_patient_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/indian_liver_patient_dataset/dataset.py
source_row: 747
type_adapter_id: curation-record-v1
---

## Comments

CC: "There was a custom train/test split. Task might be rather a toy task and not of practical use. Unclear current SOTA for the domain but in itself fine and not too old"

Make sure to add indicator variable for clipping of 90

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (untuned skills +0.47 to +0.50) does not hold for tuned methods. On BeyondArena LimiX-2 reaches ROC AUC 0.771 and the median method 0.750, with 4 of 29 methods tied with the best.

## Reference

The original dataset was first proposed by Ramana et al. (2012) as a critical comparison of patients across USA and India:
Ramana, Bendi & Surendra, M & Babu, Prasad & Bala Venkateswarlu, Nagasuri. (2012). A Critical Comparative Study of Liver Patients from USA and INDIA: An Exploratory Analysis. International Journal of Computer Science. 9.
