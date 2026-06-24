---
unique_name: cirrhosis_patient_survival_prediction
name: Cirrhosis Prediction Dataset
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- No Good Target (yet)
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Other
year: '1991'
domain: medical & healthcare
required_split:
- Random (IID)
- '?'
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/cirrhosis-prediction-dataset
- https://www.mayo.edu/research/documents/pbchtml/doc-10027635
- https://doi.org/10.24432/C5R02G
source_row: 772
type_adapter_id: curation-record-v1
---

# Cirrhosis Prediction Dataset

## Comments

Need to check for duplicates and original source.

Might be RCT data, not sure what the target might become?

Status contains censored data, need to figure out how to use and work with this.
Clearly a survival task as it seems.

We treat it as an uncensored time to death prediction task or similar as we do not score original survival prediction tasks so far.

## Reference

Fleming, T.R. and Harrington, D.P. (1991) Counting Processes and Survival Analysis. Wiley Series in Probability and Mathematical Statistics: Applied Probability and Statistics, John Wiley and Sons Inc., New York.

(get correct version ref)

Real
