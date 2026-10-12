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

CC (2026-10-12, Lennart): Kept `TotalElectricityBill`: its signal is mostly whether the municipality bills electricity at all, which a real forecast knows too, and among billed accounts electricity is the same share of the bill for bad debts and others (median 0.33), so no cut-off for the window's arrears shows. Kept `HasIDNo`: the data card describes it as a property of the holder; capture during collection stays possible (Residential 64% against 47% bad debts; 0.002 ROC AUC). IID with `ForcedIIDFromTemporal`: the file is one extract without dates, so the status at the extract stands in for a forecast. A municipality scores its own accounts; for one not in the data, ROC AUC falls from 0.877 to 0.843 (file blocks of 2,500 rows) and 0.786 (thirds of the file), but the file has no municipality key. The Unknown-category run at the end of the file (rows 134,192-138,276) stays: debt is recorded there.

## Reference

Kaggle
