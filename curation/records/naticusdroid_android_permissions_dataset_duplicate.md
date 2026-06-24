---
unique_name: naticusdroid_android_permissions_dataset_duplicate
name: naticusdroid+android+permissions+dataset
suggestion: 'No'
decision_markers:
- Duplicate
original_source: UCI
year: '2021'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5FS64
type_adapter_id: curation-record-v1
---

# naticusdroid+android+permissions+dataset

## Comments

Shipped in the BeyondArena / TabArena (v0.1) collection(s).

TabArena curation verdict: Tabular.

permissions extracted from more than 29000 benign & malware Android apps released between 2010-2019. Can be used to create a malware detection system. Might require temporal split' recommended split si time-unaware

Potential issue: maybe temporal relationships

Lennart: I think the task can be understood as gap filling without a temporal split, as we might want to classify if an app released in the past is malware!

Andrej: Unclear whether temporal split

## Reference

NATICUSdroid: A malware detection framework for Android using native and custom permissions
 By A. Mathur, Laxmi M. Podila, Keyur Kulkarni, Quamar Niyaz, A. Javaid. 2021
 
 Published in J. Inf. Secur. Appl.
