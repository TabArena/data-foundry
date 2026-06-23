---
unique_name: eryhemato_squamous_disease
name: dermatology
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1997'
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
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/dermatology/metadata.yaml
- 10.24432/C5FK5P
source_row: 753
type_adapter_id: curation-record-v1
---

# dermatology

## Comments

Looks like an old but reasonable task 

If we use the Histopathological, this means we assume the patient may or may not be given a biopsy

## Reference

@article{guvenir1998learning,
  title={Learning differential diagnosis of erythemato-squamous diseases using voting feature intervals},
  author={G{\"u}venir, H Altay and Demir{\"o}z, G{\"u}l{\c{s}}en and Ilter, Nilsel},
  journal={Artificial intelligence in medicine},
  volume={13},
  number={3},
  pages={147--165},
  year={1998},
  publisher={Elsevier}
}
