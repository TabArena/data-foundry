---
unique_name: diabetes_3
name: Diabetes
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Trivial
tags:
- Tiny Data
collections:
- TabSTAR
original_source: Website
year: '2002'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/44223
- https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html
v2_path: datasets/_dev/tabarena-v0pt2/diabetes_3/dataset.py
source_row: 785
type_adapter_id: curation-record-v1
---

## Comments

scikit-learn toy dataset

Unclear if too trivial?

Let us use the version of the data without normalization and the correct headers.

The original source of the data is supposedly from the same group as the referenced paper. Unclear in general, but should be fine as it is used so much

**Assessment (AI, 2026-10-07):** The data traces to Efron et al. (2004) and Hastie's LARS page (since 2002, with the headers `age sex bmi map tc ldl hdl tch tg glu y`). It does not look like the paper's "442 diabetes patients": read as fasting glucose in mg/dL, `glu` runs 58-124 (mean 91), so none reaches 126. No source gives the clinic, the units or how the response is measured (criterion 4E, against the accepted unclear source). Not trivial: on all 60 splits the best single feature, chosen on the training side, reaches R^2 0.30 against 0.49 for the best of least squares, ridge and a random forest, and stays below them on every split. Suggest dropping `Trivial`.

## Reference

@article{efron2004least,
  title={Least angle regression},
  author={Efron, Bradley and Hastie, Trevor and Johnstone, Iain and Tibshirani, Robert},
  year={2004}
}
