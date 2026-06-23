---
unique_name: japanese_credit_screening
name: Japanese Credit Screening
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'No'
decision_markers:
- Outdated
- Too Small
tags:
- Tiny Data
collections:
- New - IST
original_source: UCI
year: '1987'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- 10.24432/C5FS30
- https://doi.org/10.24432/C5259N
source_row: 774
type_adapter_id: curation-record-v1
---

# Japanese Credit Screening

## Comments

The UCI source contains two datasets, this is the creidt dataset in LISP Format

This is the Credit Screening (150 rows) version

Too few rows after cross-validation -> few-shot

## Reference

@misc{japanese_credit_screening_28,
  author       = {Sano, Chiharu},
  title        = {{Japanese Credit Screening}},
  year         = {1992},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C5259N}
}
