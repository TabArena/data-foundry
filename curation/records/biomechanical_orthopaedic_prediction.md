---
unique_name: biomechanical_orthopaedic_prediction
name: Vertebral Column
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Wrong Domain / Source Modality
- Not Representative
- Selection Bias
- No Good Target / Scientific Discovery
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Other
year: '2006'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://repositorio.ufc.br/bitstream/riufc/15977/1/2006_dis_arrochaneto.pdf
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

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — da Rocha Neto 2006 / 2011 report the classification (hit) rate, and a reject-option error-reject trade-off on the 2-class version; no threshold or costs for the 3-class diagnosis, and the full texts could not be opened. Original rejected: accuracy. log_loss is the multiclass fallback.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends not to ship it. Priority 2: gap +, use case - (our use case), source + (the 2006 thesis lists all 310 rows), shape -, risk - (degree_spondylolisthesis is the criterion of one class; recommended not to ship).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Retire: degree_spondylolisthesis is the slip that defines the spondylolisthesis class (half the rows, ROC AUC 0.9918 alone), and a two-stage logistic model of that rule beats all 40 benchmark methods. Priority 2: gap 1, use case 0, source 1, shape 0, risk -1.

CC (2026-11-05, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`): for half the patients one column is the diagnosis, and the other half asks for a diagnosis these measurements are not used for. The data: 310 patients of an orthopaedics group in Lyon, listed in a 2006 master's thesis (UCI 212 is a copy), six measures of the pelvis and lower spine read from one radiograph, and the diagnosis disc hernia, spondylolisthesis or normal.
- **One column is the criterion of half the labels:** spondylolisthesis is the forward slip of one vertebra over the next, and `degree_spondylolisthesis` is the size of that slip, so for the 150 patients with it the column assigns the label (one threshold separates the class at ROC AUC 0.9918). A two-stage logistic model, the slip first, then the pelvis shape for hernia against normal, beats all 40 benchmark methods (log loss 0.310 against 0.331 to 0.411).
- **What is left has no use:** disc hernia (a disc bulging out between two vertebrae) against normal, 160 patients, is diagnosed by MRI and symptoms, which the table lacks; the angles come from the same radiograph as the diagnosis and are measured for surgical planning, so no decision waits for this prediction.
- **Why the keep does not hold:** Lennart's `Yes` predates the objection; the source classifies the three classes (da Rocha Neto 2006, 2011), but for one of them that is reading off a column.
Marker `No Good Target / Scientific Discovery` added: a label one column assigns, and a remainder no decision waits on, is no real prediction target; `Trivial` is not the reason for retiring it. `year` set to 2006, the thesis, from the definition.

## Reference

@inproceedings{da2011diagnostic,
  title={Diagnostic of pathology on the vertebral column with embedded reject option},
  author={da Rocha Neto, Ajalmar R and Sousa, Ricardo and de A. Barreto, Guilherme and Cardoso, Jaime S},
  booktitle={Iberian Conference on Pattern Recognition and Image Analysis},
  pages={588--595},
  year={2011},
  organization={Springer}
}
