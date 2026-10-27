---
unique_name: diabetes_3
name: Diabetes
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 1
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
- https://doi.org/10.1214/009053604000000067
- https://hastie.su.domains/Papers/LARS/diabetes.data
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

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape -, risk - (Issue 1: response, units and cohort undocumented; maybe not diabetics; alternative is to retire). A classic tiny regression (442 rows) used everywhere, but the cohort and the target are undocumented; it adds little beyond a familiar toy benchmark.

**Assessment (AI, 2026-10-20):** re-check by the review panel: ship after changes, once the curator rules on USE-5 (the mediator; otherwise `No`, `No Good Target`). No leak, the random split is right, and the task is not trivial (the best single feature stays below least squares, ridge and a random forest on 60 of 60 splits, by at least 0.08); the definition now has `fit="approximate"` with the gap named. Open: no source says what the label measures, nor the clinic, the units or the inclusion rule, so whether USE-5 is met is the curator's reading or an amendment, decided with mobile_churn (REVIEW.md issue 1). Under PROV-8 the source links would be the DOI and the LARS page, with OpenML 44223 as the copy scaled over all rows; the `Trivial` marker has no proof (both are record-field rows in REVIEW.md). Priority 1: gap -, use case -, source +, shape -, risk - (use case: the fit is approximate and the decision is ours; source: a peer-reviewed paper and the authors' page; shape: 442 patients; risk: the label's quantity is undocumented and USE-5 is open).

CC (2026-10-21, Lennart): on the USE-5 question (REVIEW.md issue 1): "In general, I would like to keep the data and just mark it as approximate, and we can case-by-case decide the details." USE-5 amended: a label from a named publication whose construction is undocumented may ship with fit approximate and a note naming the gap; kept as defined.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — the LARS paper illustrates variable selection, no held-out score.

CC (2026-10-26, Lennart): the record's fields as the definition has them. source_links: the paper's DOI and the authors' file on Trevor Hastie's LARS page (PROV-8). The earlier links are copies: OpenML 44223 (https://www.openml.org/d/44223) ships the features scaled over all 442 rows, and https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html is a later copy. The `Trivial` marker is removed (TP-4: the best single feature, chosen on the training side, stays below least squares, ridge and a random forest on all 60 shipped splits, mean R^2 0.31 against 0.48).

CC (2026-10-26, Lennart): verdict ship.

## Reference

@article{efron2004least,
  title={Least angle regression},
  author={Efron, Bradley and Hastie, Trevor and Johnstone, Iain and Tibshirani, Robert},
  year={2004}
}
