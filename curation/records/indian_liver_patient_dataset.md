---
unique_name: indian_liver_patient_dataset
name: ilpd
checked_by:
- Lennart
- Andrej
data_foundry_status: 'Yes'
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
source_row: 747
type_adapter_id: curation-record-v1
---

# ilpd

## Comments

CC: "There was a custom train/test split. Task might be rather a toy task and not of practical use. Unclear current SOTA for the domain but in itself fine and not too old"

Make sure to add indicator variable for clipping of 90

## Reference

The original dataset was first proposed by Ramana et al. (2012) as a critical comparison of patients across USA and India:
Ramana, Bendi & Surendra, M & Babu, Prasad & Bala Venkateswarlu, Nagasuri. (2012). A Critical Comparative Study of Liver Patients from USA and INDIA: An Exploratory Analysis. International Journal of Computer Science. 9.
