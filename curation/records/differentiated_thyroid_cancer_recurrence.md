---
unique_name: differentiated_thyroid_cancer_recurrence
name: Differentiated Thyroid Cancer Recurrence
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
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
v2_path: datasets/_dev/tabarena-v0pt2/differentiated_thyroid_cancer_recurrence/dataset.py
source_row: 788
type_adapter_id: curation-record-v1
---

## Comments

Might be panel / longitudinal data, but is already made to be IID

Otherwise, looks reasonable and might be a valid task

Performance in paper is already very high, likely trivial

**Assessment (AI, 2026-10-07):** One row per patient: the 383 differentiated cancers of a 400-patient endocrine-clinic cohort in Hamadan, 2008-2023 (Khazaei et al. 2024, J Res Health Sci 24:e00632, open access; Table 2 matches the file). `Response` is a post-treatment assessment ("determined based on the laboratory findings of thyroglobulin and antithyroglobulin and a whole-body scan", same paper, Methods), and a structural incomplete response is persistent or new metastatic disease (ATA 2015, [B29]): 89 of 91 such patients recurred. The v2 definition drops it and the undefined radiotherapy column and predicts at initial staging. ROC AUC is then 0.93 against 0.896 for the ATA risk alone (beaten on 59-60 of 60 splits), so `Trivial` does not hold. No open text defines recurrence.

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
