---
unique_name: eryhemato_squamous_disease
name: dermatology
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
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
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/dermatology/metadata.yaml
- https://doi.org/10.24432/C5FK5P
notebook_path: datasets/beyond_iid/new_iid/eryhemato_squamous_disease/eryhemato_squamous_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/eryhemato_squamous_disease/dataset.py
source_row: 753
type_adapter_id: curation-record-v1
---

## Comments

Looks like an old but reasonable task

If we use the Histopathological, this means we assume the patient may or may not be given a biopsy

CC (2026-10-06, Lennart): Changed to the clinical features only after the task-probe review (flag `solved`). The source evaluates in two steps: "Patients were first evaluated clinically with 12 features. Afterwards, skin samples were taken for the evaluation of 22 histopathological features." With all 34 features the task is close to solved (logistic regression: macro ROC AUC 0.999, 97% accuracy on the 60 shipped splits; BeyondArena's best log loss 0.044), so v0.2 asks for the diagnosis before the biopsy: the 11 clinical findings, family history and age. Same six classes. On the shipped splits this gives macro ROC AUC 0.98 and 87% accuracy for logistic regression (log-loss skill +0.76; random forest +0.72, LightGBM +0.65), with seborrheic dermatitis, pityriasis rosea and chronic dermatitis as the hard cases, which is the differential the source describes. No probe flags on the rebuilt container. One pair of patients shares all clinical findings with different diagnoses.

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
