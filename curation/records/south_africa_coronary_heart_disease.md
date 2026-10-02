---
unique_name: south_africa_coronary_heart_disease
name: sa-heart
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: Other
year: '1983'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/1498
- https://www.kaggle.com/datasets/waalbannyantudre/south-african-heart-disease-dataset
notebook_path: datasets/beyond_iid/new_iid/south_africa_coronary_heart_disease/south_africa_coronary_heart_disease.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/south_africa_coronary_heart_disease/dataset.py
source_row: 749
type_adapter_id: curation-record-v1
---

## Comments

Kaggle version is much better described, wow!, well done

general good dataset as it seems

CC (2026-10-01, Lennart): Leak audit, kept as is with a comment in the definition. The data is a retrospective CORIS case-control sample, and ESL (2nd ed., Sec. 5.2.2, p. 148) says: "These measurements were made sometime after the patients suffered a heart attack, and in many cases they had already benefited from a healthier diet and lifestyle". So some risk factors of the cases were measured after the outcome, but this weakens sbp and obesity rather than leaking the target (dropping both: ROC AUC 0.774 -> 0.778). No duplicates or near-copies; logistic regression (AUC 0.772) beats LightGBM (0.725), as expected for a weak smooth signal.

## Reference

@article{rossouw1983coronary,
  title={Coronary risk factor screening in three rural communities. The CORIS baseline study.},
  author={Rossouw, JE and Du Plessis, JP and Benad{\'e}, AJ and Jordaan, PC and Kotze, JP and Jooste, PL and Ferreira, JJ},
  journal={South African medical journal= Suid-Afrikaanse tydskrif vir geneeskunde},
  volume={64},
  number={12},
  pages={430--436},
  year={1983}
}
