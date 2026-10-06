---
unique_name: hepatitis_c_prediction
name: Hepatitis C Prediction Dataset
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D612
- https://www.kaggle.com/datasets/fedesoriano/hepatitis-c-dataset
notebook_path: datasets/beyond_iid/new_iid/hepatitis_c_prediction/hepatitis_c_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hepatitis_c_prediction/dataset.py
source_row: 771
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: donor and patient rows use different recording conventions, which gave the class away.** Share of whole-number values (donor / hepatitis / fibrosis / cirrhosis): ALB 0.11 / 1.00 / 1.00 / 0.97, BIL 0.09 / 1.00 / 1.00 / 1.00, CREA 1.00 / 0.12 / 0.57 / 0.33; ALP is missing for 0 of 533 donors but 18 patients. These four format flags alone give patient-vs-donor AUC 0.9997 and beat the full LightGBM on log loss (0.15 vs 0.27; leak audit 2026-09-24, rechecked). Fix: ALB, ALT, AST, BIL, CREA, GGT and PROT rounded to integers for all rows (median change 0.3-2.6%, worst 2.4 -> 2 in BIL; no value becomes 0) and ALP dropped; CHE and CHOL (single digits, no class difference) stay as recorded. Log loss 0.27 -> 0.35, patient-vs-donor AUC 0.997 -> 0.984; within patients the stage signal is unchanged (OvR AUC 0.80 -> 0.82). Open question answered: no exact or near duplicates (minimum standardised nearest-neighbour distance 0.20), so no evidence of several rows per patient. Class counts: 533 donors, 24 hepatitis, 21 fibrosis, 30 cirrhosis.

Need to check label distribution of class and if multiple entries per patient ID

## Reference

@article{hoffmann2018using,
  title={Using machine learning techniques to generate laboratory diagnostic pathways—a case study},
  author={Hoffmann, Georg and Bietenbeck, Andreas and Lichtinghagen, Ralf and Klawonn, Frank},
  journal={Journal of Laboratory and Precision Medicine},
  volume={3},
  number={6},
  year={2018},
  publisher={AME Publishing Company}
}
