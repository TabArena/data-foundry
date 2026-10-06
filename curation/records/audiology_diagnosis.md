---
unique_name: audiology_diagnosis
name: Audiology
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
- Not Representative
tags:
- Tiny Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '1992'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/8/audiology+standardized
- https://doi.org/10.24432/C5TP4R
notebook_path: datasets/beyond_iid/new_iid/audiology_diagnosis/audiology_diagnosis.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/audiology_diagnosis/dataset.py
source_row: 764
type_adapter_id: curation-record-v1
---

## Comments

Feel like this is a duplicate, but I cannot find it.

Otherwise, many classes and need to check there is enough samples per class for a task, otherwise remove some

Need to check if some rules/cases come from the system in the paper or from the database

Discussion: Not a meaningful predictive task. The available data sample is highly selective and not representative. The target is to predict what kind of ear disease a person has, if any, but there are only 9% normal samples which is unrealistic in a diagnostic task.

CC (2026-10-06, Lennart): Re-defined the target after the task-probe review (flags `no_spread`, `unstable`). The 3-class merge (cochlear / normal / other) was our own, made from the diagnosis names: it put the 24 mixed losses under cochlear and lumped conductive with retrocochlear and central disorders under other. The 24 original diagnoses cannot be the target (16 have 4 or fewer cases), and dropping the rare ones does not help: the four large cochlear diagnoses are spelled out by two history findings (age_gt_60, history_noise: 139 of 147 cases). The source defines no grouping. The new target is the standard distinction between a hearing loss with and without a conductive part: normal 19, sensorineural 142, conductive_or_mixed 34 (195 cases). Duplicated cases (27) stay dropped, bells_palsy and the central diagnoses (possible_brainstem_disorder, poss_central) are dropped as not a type of hearing loss; the four types with conductive and mixed apart would leave 10 conductive cases, 3-4 per test fold. Probes on the rebuilt container: no flags; the linear model reaches log-loss skill +0.81 (log loss 0.14 against 0.76 for the class shares), the strongest single feature (`tymp`) +0.45. The label is partly read off its defining tests (a depth-3 tree reaches about 91% against 73% for the majority class), as any label of this data is.

## Reference

@incollection{bareiss1990protos,
  title={Protos: An exemplar-based learning apprentice},
  author={Bareiss, E Ray and Porter, Bruce W and Wier, Craig C},
  booktitle={Machine learning},
  pages={112--127},
  year={1990},
  publisher={Elsevier}
}
