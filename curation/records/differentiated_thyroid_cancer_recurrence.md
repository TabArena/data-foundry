---
unique_name: differentiated_thyroid_cancer_recurrence
name: Differentiated Thyroid Cancer Recurrence
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Trivial
tags:
- Tiny Data
collections:
- TabSTAR
original_source: UCI
year: '2023'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5632J
- https://www.openml.org/search?type=data&id=46605&sort=runs&status=active
source_row: 788
type_adapter_id: curation-record-v1
---

# Differentiated Thyroid Cancer Recurrence

## Comments

Might be panel / longitudinal data, but is already made to be IID

Otherwise, looks reasonable and might be a valid task

Performance in paper is already very high, likely trivial

## Reference

@article{borzooei2024machine,
  title={Machine learning for risk stratification of thyroid cancer patients: a 15-year cohort study},
  author={Borzooei, Shiva and Briganti, Giovanni and Golparian, Mitra and Lechien, Jerome R and Tarokhian, Aidin},
  journal={European Archives of Oto-Rhino-Laryngology},
  volume={281},
  number={4},
  pages={2095--2104},
  year={2024},
  publisher={Springer}
}
