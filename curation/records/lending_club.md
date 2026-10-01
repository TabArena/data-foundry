---
unique_name: lending_club
name: lending_club
checked_by:
- Lennart
- Alex
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Free Text (Sentences)
- Non-IID (Temporal)
collections:
- TexTabBench Extra
original_source: Company
year: '2020'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/imsparsh/lending-club-loan-dataset-2007-2011
- https://www.kaggle.com/datasets/wordsforthewise/lending-club
- https://zenodo.org/records/11295916
- https://www.kaggle.com/datasets/adarshsng/lending-club-loan-data-csv
- https://www.lendingclub.com/
notebook_path: datasets/beyond_iid/temporal/lending_club/lending_club_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/lending_club/dataset.py
source_row: 641
type_adapter_id: curation-record-v1
---

## Comments

Predict whether loan is paid back, needs to be shuffled, TextTabBench drops ['id', 'member_id', 'issue_d', 'url', 'last_pymnt_d', 'last_credit_pull_d'], we will have to make sure that there is no leakage

Text has prefix for date and HTML artifacts
Data might have spatial components

CC (2026-10-01, Lennart): The Zenodo file (Sanz-Guerrero et al.) holds only loans that had finished (fully paid or charged off) by the 2018Q4 snapshot. Against accepted_2007_to_2018Q4.csv.gz, at least 99.8% of the 36-month loans are finished up to 2015Q4, but 57-93% per quarter in 2016 (38% in 2017, 11% in 2018), and only 63-97% of the 60-month loans per quarter from 2014 on. The missing loans are mostly good ones still being repaid, so later or longer loans skew the labels (default rate among finished loans 15-16% in 2013, 24-26% in 2016). The v0.2 definition therefore keeps only the 36-month loans issued up to 2015 (609,544 rows) and tests on the quarters 2015 Q2-Q4; `term` is used only for this selection, not as a feature.
