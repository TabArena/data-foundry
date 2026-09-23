---
unique_name: biomechanical_orthopaedic_prediction
name: Vertebral Column
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
decision_markers:
- Wrong Domain / Source Modality
- Not Representative
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5K89B
- https://www.kaggle.com/datasets/sammy123/lower-back-pain-symptoms-dataset/
- https://www.kaggle.com/datasets/simaeel/vertebral-column
notebook_path: datasets/beyond_iid/new_iid/biomechanical_orthopaedic_prediction/biomechanical_orthopaedic_prediction.ipynb
source_row: 776
type_adapter_id: curation-record-v1
---

## Comments

Weka dataset, unclear source or citation

Discussion: 
(1) Data uses extracted features, while for the actual task one would nowadays use MRI image data and likely many other clinical decision markers like symptoms. So this is more useful as toy data rather than for a real value-generating task. 
(2) The three-class target is definitionally in the features: For the Spondylolisthesis class, degree_spondylolisthesis isn't a predictor of that class, it's the diagnostic criterion. That class is 150/310 rows, and a single threshold on that one column separates it near-perfectly with an AUC of 0.9918. The only non-trivial part of the 3-class problem is Disk Hernia (60) vs Normal (100) — a 160-row problem. 
(3) However, even if we would use this as a 160 row task with dropping the degree_spondylolisthesis feature, however herniation is diagnosed by MRI plus symptoms, and the cheap covariates that would actually predict it (age, BMI, pain pattern) are absent
(4) It seems like features and labels both come from the same radiographs, read at the same time. pinopelvic angles are measured after diagnosis for surgical planning, so there's no point in care where the features are the information you have to predict the target. There is no time gap, no action a clinician would take differently.

CC: Source traced in the notebook: da Rocha Neto et al. 2011 (below), with the oldest known version being a 2006 UFC (Brazil) master's thesis referenced there. Supersedes the "unclear source" note above.

## Reference

@inproceedings{da2011diagnostic,
  title={Diagnostic of pathology on the vertebral column with embedded reject option},
  author={da Rocha Neto, Ajalmar R and Sousa, Ricardo and de A. Barreto, Guilherme and Cardoso, Jaime S},
  booktitle={Iberian Conference on Pattern Recognition and Image Analysis},
  pages={588--595},
  year={2011},
  organization={Springer}
}
