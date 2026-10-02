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
- Non-IID (Grouped)
- Free Text (Sentences)
collections:
- TexTabBench
- TabSTAR
original_source: Other
year: '2020'
domain: business & marketing
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction
- https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam
- Original website is down
- http://emscad.samos.aegean.gr/
- https://www.openml.org/search?type=data&id=46655&sort=runs&status=active
notebook_path: datasets/beyond_iid/new_iid/emscad/emscad.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/emscad/dataset.py
source_row: 681
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: reposts dropped and a grouped split by poster; ROC AUC 0.99 IID -> 0.94 grouped.** Vidros et al. 2017 (Future Internet 9(1):6), Sec. 5: labels come from Workable's review of the client ("client's suspicious activity on the system, false contact or company information, candidate complaints and periodic meticulous analysis of the clientele"), and "fraudsters can quickly and repeatedly try to post the same job ad in identical or different locations". Changes, all exact rules without similarity thresholds: (1) reposts dropped: rows identical in every field except job_id and location (1,343 rows after exact deduplication, 115 fraudulent; 0 of the 368 repost groups mix labels); (2) `poster_group`: ads sharing the exact non-empty company_profile (1,708 profiles, none mixes labels) or a masked e-mail/phone/URL hash that occurs within at most one company profile (generic contacts such as job-board URLs, shared by up to 87 companies, are ignored; linking through them made one group of 5,325 rows). Result: 16,116 rows, 737 fraudulent, 4,441 groups (largest 539, a legitimate recruiter; 3,208 single ads; 2 groups mix labels). LightGBM on the grouped splits: AUC 0.938 (0.903-0.953 over 6 folds), against about 0.99 random. Residual: about 335 single ads have a near-identical text (cosine >= 0.95) in another group; dropping them at 0.95-0.7 did not change the grouped AUC (0.918-0.934), so they are kept. The grouped split measures fraud detection for posters not seen before; a new ad from an already flagged client is caught by the account, not by a content model. The paper's own full-dataset evaluation (Sec. 6.4) tests on all 17,880 ads, including its 900 training ads. Also: " " and "\xa0" in text fields are now missing values.

Original source website seems down, dataset is very imbalanced, but seems like a good fit at first glance; multiple versions on Kaggle; paper describes some specific preprocessing and data filters, need to check if data is already preprocessed or if we need to do the same; very imbalanced

Also contains non-English text (at least German, didn't check yet for more); title contains a lot of information as well

## Reference

https://doi.org/10.3390/fi9010006
