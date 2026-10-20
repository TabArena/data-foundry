---
unique_name: mobile_churn
name: mobile_churn
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
decision_markers:
- Missing source information
tags:
- Larger IID Data
collections:
- TabSTAR
original_source: Kaggle
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=44231&sort=runs&status=active
- https://www.kaggle.com/datasets/dimitaryanev/mobilechurndataxlsx
v2_path: datasets/_dev/tabarena-v0pt2/mobile_churn/dataset.py
source_row: 656
type_adapter_id: curation-record-v1
---

## Comments

Another case of missing data but data looking very good and real.

Check year/month and user account id column if temporal or grouped splits are needed.

**Assessment (AI, 2026-10-07):** IID split: user_account_id is unique per row; year is constant (2013). 12,262 accounts with neither the intake flag nor an activation date are SIM cards never taken into use, not customers. Only 0.2-0.5% used minutes, SMS or data in 100 days. They came in provisioning batches, churn at 54% (June) and 80% (August), and held 61% of the churners. The v2 definition drops them in every month; the kept July and August rows are those months' new customers. Unlike churn_telco_europa, both classes share their month's snapshot date, and the churners' last activity bunches just before it. No row overlap with the SATO, DSN or Europa churn files. The source and the churn definition remain undocumented.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issue 1: source and churn definition unknown (unclear target); alternative is No). Real-looking prepaid churn data with unknown origin and an undocumented label; another common churn task with weak provenance.

## Reference

Kaggle
