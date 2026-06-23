---
unique_name: tae
name: tae
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1997'
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
usable_task_type: Predictive ML
given_task_type:
- Scientific Discovery
data_modality:
- Tabular
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/tae/metadata.yaml
- 10.24432/C55P6M
- https://www.openml.org/search?type=data&id=48&sort=runs&status=active
source_row: 68
type_adapter_id: curation-record-v1
---

# tae

## Comments

The task is to predict the evaluation of an instructor x course based on semester, class size, and native language. This does not seem to represent a meaningful task IMO

Also it would need to have a temporal (on semester) split, which then it way too little data for a meaingful evaluation

moreover, the dataset is super old. I vote to exclude the dataset due to the age and quesitnalbe real-world nature right away (https://www.nature.com/articles/s41598-024-64445-2)
