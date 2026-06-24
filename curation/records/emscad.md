---
unique_name: emscad
name: fraud_detec
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- New IID
- Free Text (Sentences)
collections:
- TexTabBench
- TabSTAR
original_source: Other
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction
- https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam
- Original website is down
- http://emscad.samos.aegean.gr/
- https://www.openml.org/search?type=data&id=46655&sort=runs&status=active
source_row: 681
type_adapter_id: curation-record-v1
---

# fraud_detec

## Comments

Original source website seems down, dataset is very imbalanced, but seems like a good fit at first glance; multiple versions on Kaggle; paper describes some specific preprocessing and data filters, need to check if data is already preprocessed or if we need to do the same; very imbalanced

Also contains non-English text (at least German, didn't check yet for more); title contains a lot of information as well

## Reference

https://doi.org/10.3390/fi9010006
