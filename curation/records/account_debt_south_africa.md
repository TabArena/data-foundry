---
unique_name: account_debt_south_africa
name: ACCOUNT_DEBT_SOUTH_AFRICA
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- Larger IID Data
collections:
- TabSTAR
original_source: Kaggle
year: '2020'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/dmsconsultingsa/municipal-debt-risk-analysis/data
- https://www.openml.org/search?type=data&id=43838
v2_path: datasets/_dev/tabarena-v0pt2/account_debt_south_africa/dataset.py
source_row: 655
type_adapter_id: curation-record-v1
---

## Comments

Looks real enough and good

"The original data comprises approximately 20 million records. These were imported into a PostgreSQL database and summarised by calculating totals, averages (means) and ratios. The Field Metadata below describes each field."

**Assessment (AI, 2026-10-07):** Valid with concerns. DMS Technologies (Dylan Rawlins) summarised two years of billing of 8 unnamed South African municipalities per account (Kaggle notebook "Municipal Debt Risk Analysis v1"); OpenML 43838 is the same file. The label is a rule: every account with debt aged 90+ days or a write-off is a bad debt and all but 371 others are not, so those columns go. Seven runs of the file (27,938 rows) hold no recorded debt: billed accounts there that paid nothing, or at most half, are never bad debts (91.5% and 89.6% elsewhere); dropped. The payment totals sum the same two years whose end sets the status; dropped too (ROC AUC 0.952 with them, 0.874 without).

**Assessment (AI, 2026-10-12), problem in a third-party copy:** OpenML 43838 (Municipal-Debt-Risk-Analysis, no default target) ships `total90debt`, `totalwriteoff` and `debtbillingratio` next to the label `baddebt`. The label is a rule of these columns (see the assessment of 2026-10-07), so a model given them predicts it almost exactly; our definition drops them.

## Reference

Kaggle
