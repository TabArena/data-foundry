---
unique_name: naticusdroid_android_permissions_dataset
name: naticusdroid+android+permissions+dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2021'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5FS64
notebook_path: datasets/beyond_iid/old_iid/naticusdroid_android_permissions_dataset/naticusdroid_android_permissions_dataset.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/naticusdroid_android_permissions_dataset/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

permissions extracted from more than 29000 benign & malware Android apps released between 2010-2019. Can be used to create a malware detection system. Might require temporal split' recommended split si time-unaware

Potential issue: maybe temporal relationships

Lennart: I think the task can be understood as gap filling without a temporal split, as we might want to classify if an app released in the past is malware!

Andrej: Unclear whether temporal split

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (three untuned families at skill +0.962 to +0.968) does not hold for tuned methods. On BeyondArena the best (LimiX-2) reaches ROC AUC 0.989 and the median 0.986, with no other method within noise of the best (Kendall's W 0.96).

## Reference

NATICUSdroid: A malware detection framework for Android using native and custom permissions
 By A. Mathur, Laxmi M. Podila, Keyur Kulkarni, Quamar Niyaz, A. Javaid. 2021
 
 Published in J. Inf. Secur. Appl.
