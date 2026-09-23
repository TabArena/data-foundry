---
unique_name: audiology_diagnosis
name: Audiology
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
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
source_row: 764
type_adapter_id: curation-record-v1
---

## Comments

Feel like this is a duplicate, but I cannot find it.

Otherwise, many classes and need to check there is enough samples per class for a task, otherwise remove some

Need to check if some rules/cases come from the system in the paper or from the database

Discussion: Not a meaningful predictive task. The available data sample is highly selective and not representative. The target is to predict what kind of ear disease a person has, if any, but there are only 9% normal samples which is unrealistic in a diagnostic task. The reason is that this is a curated teaching/research case library for a case-based-reasoning system, not a consecutive clinic sample

CC: The current task definition of collapsing 24-to-3 classes to ("cochlear"/"normal"/"other") is internally incoherent. Checked the raw per-row features behind it: `conductive_fixation`, `conductive_discontinuity`, and `otitis_media` all show `airBoneGap = t` (the conductive-hearing-loss signature), while `acoustic_neuroma`, `bells_palsy`, `possible_brainstem_disorder`, `retrocochlear_unknown`, `poss_central`, and `mixed_poss_central_om` all show `airBoneGap = f` (the opposite, retrocochlear/central signature). `other` fuses two clusters with opposite values on the one feature that's supposed to be diagnostic. The feature that could actually separate them, `bser` (brainstem evoked response), is 98.5% missing (196/199 rows) in the shipped data. So `other` doesn't correspond to one region of feature space.

## Reference

@incollection{bareiss1990protos,
  title={Protos: An exemplar-based learning apprentice},
  author={Bareiss, E Ray and Porter, Bruce W and Wier, Craig C},
  booktitle={Machine learning},
  pages={112--127},
  year={1990},
  publisher={Elsevier}
}
