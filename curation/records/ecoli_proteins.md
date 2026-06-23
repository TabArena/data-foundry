---
unique_name: ecoli_proteins
name: ecoli
checked_by:
- Lennart
data_foundry_status: 'Yes'
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1996'
domain: biology & life sciences
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
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/ecoli/metadata.yaml
- 10.24432/C5388M
source_row: 754
type_adapter_id: curation-record-v1
---

# ecoli

## Comments

Has some minor classes that might not be dropped for proper validation setup. Might be outdated, otherwise seems to be still an okay task from the time

need to check sequence names again

## Reference

@inproceedings{horton1996probabilistic,
  title={A probabilistic classification system for predicting the cellular localization sites of proteins.},
  author={Horton, Paul and Nakai, Kenta},
  booktitle={Ismb},
  volume={4},
  pages={109--115},
  year={1996},
  organization={St. Louis, Missouri, USA}
}
