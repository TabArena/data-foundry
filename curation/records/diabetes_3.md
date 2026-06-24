---
unique_name: diabetes_3
name: Diabetes
checked_by:
- Lennart
suggestion: 'Yes'
decision_markers:
- Trivial
tags:
- Tiny Data
collections:
- TabSTAR
original_source: Website
year: '2004'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/44223
- https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html
source_row: 785
type_adapter_id: curation-record-v1
---

## Comments

scikit-learn toy dataset

Unclear if too trivial?

Let us use the version of the data without normalization and the correct headers.

The original source of the data is supposedly from the same group as the referenced paper. Unclear in general, but should be fine as it is used so much

## Reference

@article{efron2004least,
  title={Least angle regression},
  author={Efron, Bradley and Hastie, Trevor and Johnstone, Iain and Tibshirani, Robert},
  year={2004}
}
