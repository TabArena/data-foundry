---
unique_name: glioma_grading_clinical_and_mutation_features
name: Glioma Grading Clinical and Mutation Features
checked_by:
- Lennart
suggestion: 'Yes'
tags:
- New IID
collections:
- TabSTAR
original_source: UCI
year: '2022'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
- Scientific Discovery
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46604
- https://www.kaggle.com/datasets/vinayjose/glioma-grading-clinical-and-mutation-features
- 10.24432/C5R62J
source_row: 678
type_adapter_id: curation-record-v1
---

# Glioma Grading Clinical and Mutation Features

## Comments

"The main objective is to find the optimal subset of mutation genes and clinical features for the glioma grading process to improve performance and reduce costs." -> mostly a feature selection task?

I think we can still use it (as it is still suggested to be used this way)

## Reference

@article{tasci2022hierarchical,
  title={Hierarchical voting-based feature selection and ensemble learning model scheme for glioma grading with clinical and molecular characteristics},
  author={Tasci, Erdal and Zhuge, Ying and Kaur, Harpreet and Camphausen, Kevin and Krauze, Andra Valentina},
  journal={International Journal of Molecular Sciences},
  volume={23},
  number={22},
  pages={14155},
  year={2022},
  publisher={MDPI}
}
