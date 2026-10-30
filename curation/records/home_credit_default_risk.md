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

CC (2026-10-19, Lennart): the v2 definition computes nothing over all rows: the kernel's median income per organisation type is dropped, the mean fill of `NEW_SCORES_STD` removed, and the kernel's importance-based column selection not applied (every column stays). The kernel computed these over Kaggle's train and test applications, as a competition allows; whether that transductive setting should stay for this task can be checked later. The 43 normalised building columns are kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 35 features that hold only 0 and 1: FLAG_MOBIL, FLAG_EMP_PHONE, FLAG_CONT_MOBILE, FLAG_EMAIL, the four REG/LIVE region and city flags, 17 FLAG_DOCUMENT columns and 10 CC_NAME_CONTRACT_STATUS min/max aggregates (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: FLAG_MOBIL, FLAG_EMP_PHONE, FLAG_CONT_MOBILE, FLAG_EMAIL, the four REG_/LIVE_..._NOT_... flags and 17 FLAG_DOCUMENT columns (explicit list). Reverted: the 10 CC_NAME_CONTRACT_STATUS min/max aggregates stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (Kaggle API evaluationMetric) (https://www.kaggle.com/competitions/home-credit-default-risk/overview/evaluation).

**Assessment (AI, 2026-10-26):** an open doubt under CLEAN-14, from the cross-dataset item of 2026-10-21: the 10 `CC_NAME_CONTRACT_STATUS_*` min/max aggregates were typed categorical and then reverted to numeric as aggregates over the card history, but the max of a one-hot status reads as "ever had this status", a yes/no flag by meaning. Typing them categorical is the curator's call.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `NAME_EDUCATION_TYPE` (the README lists their levels); left unordered: `WEEKDAY_APPR_PROCESS_START` (a partial order); ordinal scales shipped as numbers, left as numbers for the curator's review: `REGION_RATING_CLIENT`, `REGION_RATING_CLIENT_W_CITY`.

## Reference

Anna Montoya, inversion, KirillOdintsov, and Martin Kotek. Home Credit Default Risk. https://kaggle.com/competitions/home-credit-default-risk, 2018. Kaggle.
