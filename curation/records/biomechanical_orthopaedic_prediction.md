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
original_source: Other
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://repositorio.ufc.br/bitstream/riufc/15977/1/2006_dis_arrochaneto.pdf
- https://doi.org/10.24432/C5K89B
- https://www.kaggle.com/datasets/sammy123/lower-back-pain-symptoms-dataset/
- https://www.kaggle.com/datasets/simaeel/vertebral-column
notebook_path: datasets/beyond_iid/new_iid/biomechanical_orthopaedic_prediction/biomechanical_orthopaedic_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/biomechanical_orthopaedic_prediction/dataset.py
source_row: 776
type_adapter_id: curation-record-v1
---

## Comments

Weka dataset, unclear source or citation

Discussion: Data uses extracted features, while for the actual task one would nowadays use MRI image data and likely many other clinical decision markers like symptoms. So this is more useful as toy data rather than for a real value-generating task.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — da Rocha Neto 2006 / 2011 report the classification (hit) rate, and a reject-option error-reject trade-off on the 2-class version; no threshold or costs for the 3-class diagnosis, and the full texts could not be opened. Original rejected: accuracy. log_loss is the multiclass fallback.

## Reference

?
