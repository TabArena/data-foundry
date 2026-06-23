---
unique_name: hepatitis_c_egypt
name: HEPATITIS_C_EGYPT
checked_by:
- Andrej
- Lennart
suggestion: 'Yes'
tags:
- New IID
collections:
- TabSTAR
original_source: UCI
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/503/hepatitis+c+virus+hcv+for+egyptian+patients
- https://www.openml.org/search?type=data&id=46607
- 10.24432/C5989V
source_row: 676
type_adapter_id: curation-record-v1
---

# HEPATITIS_C_EGYPT

## Comments

Paper reports pretty good performance, need to pay attention to target leaks. Unclear when the target was collected. Was it really after the features or can features leak the target?

After consulting Dr. GPT, learned that ALT features correspond to future follow-up measurements - temporal leakage. We could use the other features, but thats probably not very useful.

## Reference

A novel model based on non invasive methods for prediction of liver fibrosis
By Mahmoud Nasr, Khaled El-Bahnasy, M. Hamdy, S. Kamal. 2017

Published in International Computer Engineering Conference
