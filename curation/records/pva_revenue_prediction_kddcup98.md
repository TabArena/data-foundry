---
unique_name: pva_revenue_prediction_kddcup98
name: KDD98
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabArena Reject
- TabSTAR
original_source: Website
year: '1998'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/42343
- https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html
notebook_path: datasets/beyond_iid/new_iid/pva_revenue_prediction_kddcup98/pva_revenue_prediction_kddcup98_clf.ipynb
source_row: 647
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict whether there was a response to mailing. Side story: A friend of mine used to work for a company whose customers were mainly old people still ordering stuff from physical catalogues. Predicting the response to direct mailing was one the tasks he worked on. So this good old task is still relevant :) ... In Germany? :D"

This could also be used as a classification task given the first dependent variable

The problem type is not a property of this dataset: it is *either* regression on the donation
amount *or* binary classification on whether the mailing got a response — one target or the
other, never both at once. After investigation we shipped the classification version, so
`problem_type` records `Binary Classification` and the curated dataset comes from
`pva_revenue_prediction_kddcup98_clf.ipynb`, not from the regression notebook next to it.

## Reference

Website / readme
