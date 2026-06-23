---
unique_name: kddcup99
name: KDDCup99
checked_by:
- Andrej
- Lennart
suggestion: TBD -> Yes
decision_markers:
- Outdated
- Time-series (Classification)
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Data Quality Issue
tags:
- Non-IID (Temporal)
- '?'
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '1999'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
usable_task_type: Predictive ML
given_task_type:
- Predictive ML
data_modality:
- Tabular
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- openml 42746
- https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
source_row: 629
type_adapter_id: curation-record-v1
---

# KDDCup99

## Comments

CC: "Subsampled dataset. Detect intrusions. Might be outdated, but might as well be still representative; original data had 7 weeks of training and 2 weeks of test data so this implies a temporal connection"

Likely outdated too

"intrusions simulated in a military network environment" "They operated the LAN as if it were a true Air Force environment, but peppered it with multiple attacks."  

Is actually a time-series task, but was made tabular

"It is important to note that the test data is not from the same probability distribution as the training data, and it includes specific attack types not in the training data.  This makes the task more realistic.  Some intrusion experts believe that most novel attacks are variants of known attacks and the "signature" of known attacks can be sufficient to catch novel variants.  The datasets contain a total of 24 training attack types, with an additional 14 types in the test data only."
Class shift then, or need to change prediction task?

Only could use the official split, otherwise no temporal informatioN?

## Reference

Cost-based Modeling and Evaluation for Data Mining With Application to Fraud and Intrusion Detection: Results from the JAM Project by Salvatore J. Stolfo, Wei Fan, Wenke Lee, Andreas Prodromidis, and Philip K. Chan.
