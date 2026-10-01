---
unique_name: home_credit_default_risk
name: Home Credit Default Risk
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: Kaggle
year: '2018'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/home-credit-default-risk/data?select=application_train.csv
- https://www.openml.org/search?type=data&id=45567
notebook_path: datasets/beyond_iid/new_iid/home_credit_default_risk/home_credit_default_risk.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/home_credit_default_risk/dataset.py
source_row: 653
type_adapter_id: curation-record-v1
---

## Comments

Kaggle solutions used IID splits

CC (2026-10-01, Lennart): Leak audit: no leak. The label-aware feature selection taken from the kernel only drops zero-importance features (242 of them); selecting inside folds or not selecting at all gives the same AUC (0.788), and no aggregate uses the target or dates after the application. The v2 definition was restructured (no change to the data, identical frame hash): `_load_raw` reads all seven tables, `_clean` calls one helper per kernel function, the long column lists are module constants, an unused categorical list was removed, and `_feature_types` lists only the 22 categorical columns that survive the selection (it listed 25 dropped ones, so the definition did not build).

## Reference

Anna Montoya, inversion, KirillOdintsov, and Martin Kotek. Home Credit Default Risk. https://kaggle.com/competitions/home-credit-default-risk, 2018. Kaggle.
