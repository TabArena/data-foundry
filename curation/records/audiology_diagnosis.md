---
unique_name: audiology_diagnosis
name: Audiology
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Disagreement
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
source_row: 764
type_adapter_id: curation-record-v1
---

## Comments

Feel like this is a duplicate, but I cannot find it.

Otherwise, many classes and need to check there is enough samples per class for a task, otherwise remove some

Need to check if some rules/cases come from the system in the paper or from the database

Discussion: Not a meaningful predictive task. The available data sample is highly selective and not representative. The target is to predict what kind of ear disease a person has, if any, but there are only 9% normal samples which is unrealistic in a diagnostic task.

## Reference

@incollection{bareiss1990protos,
  title={Protos: An exemplar-based learning apprentice},
  author={Bareiss, E Ray and Porter, Bruce W and Wier, Craig C},
  booktitle={Machine learning},
  pages={112--127},
  year={1990},
  publisher={Elsevier}
}
