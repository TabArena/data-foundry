---
unique_name: tecator
name: tecator
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/505
- https://lib.stat.cmu.edu/datasets/tecator
source_row: 449
type_adapter_id: curation-record-v1
---

## Comments

CC: "predict the fat content of a meat sample on the basis of its near infrared absorbance spectrum. Spectral data is not really tabular, but the same models can be used. So might be interesting to include this dataset. BUT: Unfortunately the spectra were already preprocessed using PCA, which might introduce bias. So rather search for another spectra dataset. Linear model is by far the best - could this be a side issue of using PCA for preprocessing?"
