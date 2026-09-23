---
unique_name: diabetes_2
name: Diabetes
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- Non-IID (Temporal)
- Non-IID (Grouped)
- 2nd Tier / Scientfic Discovery
- Review Prio 1 (Atlas)
collections:
- TableShift
original_source: GOV Website
year: '2024'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://tableshift.org/datasets.html#diabetes
- https://www.cdc.gov/brfss/index.html
- https://www.kaggle.com/datasets/cdc/behavioral-risk-factor-surveillance-system
- https://arxiv.org/abs/2312.07577
- https://github.com/mlfoundations/tableshift
- https://doi.org/10.24432/C53919
source_row: 557
type_adapter_id: curation-record-v1
---

## Comments

CC: "Used to benchmark distribution shifts between ethnicities, but could also be used with random splits. But would need to clarify license. Source: Centers for Disease Control/BRFSS"

need to check for duplicates, also likely on kaggle in some form.
Plus, maybe not a real predictive task

Get newest data from website

Duplicate with cdc_diabetes_health_indicators

CC (2026-09-23, Lennart): What it is: TableShift's BRFSS Diabetes task (Gardner, Popovic & Schmidt, NeurIPS 2023 D&B, arXiv 2312.07577, App. B.5). BRFSS waves 2015/2017/2019/2021 (`BRFSS_YEARS` in `tableshift/datasets/brfss.py`; every-other-year because some features are rotating-core questions), 1,444,176 rows. Target: "a binary indicator for whether the respondent has ever been told they have diabetes" (DIABETE3/DIABETE4; pre-diabetes and gestational diabetes mapped to 0). Features: "a set of features related to several known indicators for diabetes derived from [88]" (= Xie et al. 2019, below) plus race, sex, state, survey year, income. The shift is a race split (PRACE1 = 1 "White non-Hispanic" in-domain, all other groups OOD), a category split, not a grouped task, same as `hypertension`.

Why duplicate: same source, same target and nearly the same risk-factor feature set as the BRFSS-2015 "Diabetes Health Indicators" cut (Teboul; UCI 891, DOI 10.24432/C53919, 253,680 x 21) that is curated as `cdc_diabetes_health_indicators` (Yes). TableShift adds three later survey waves and the race split; neither makes it a distinct task. Same call as `hypertension` / `public_health_ins`.

Resolves the open points above: it is a real published predictive task (Xie, Nikolayeva, Luo & Li, Prev Chronic Dis 16:190109, 2019: BRFSS 2014, "answered yes to the question 'Have you ever been told you have diabetes?'", AUC 0.72-0.79), so `No Good Target (yet)` no longer applies. Licence: CDC material "is in the public domain, and may be freely used or reproduced" with attribution and a no-endorsement note (cdc.gov/other/agencymaterials.html). BRFSS public-use files now run to 2025. If a temporal BRFSS task is ever wanted, build it from the raw annual files, not from this cut: each wave is a fresh cross-sectional sample and the diabetes question was recoded (DIABETE3 -> DIABETE4) in 2019.

## Reference

https://www.cdc.gov/brfss/
