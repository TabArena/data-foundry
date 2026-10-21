---
unique_name: account_debt_south_africa
name: ACCOUNT_DEBT_SOUTH_AFRICA
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
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

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 1: 20% of rows lack recorded debt, dropped by file-order rule; retire is an alternative). Rare real municipal-debt task from Africa, but label is a rule, payments leak, and a fifth of the file is unrecorded.

**Assessment (AI, 2026-10-20):** Review panel (re-check): ship after changes, made in the definition. The label is mostly arrears older than the two-year window (83.7% of bad debts hold more 90+ debt and write-off than the window's unpaid billing), so the task now reads as the status at the extract (fit approximate). An eighth unrecorded run (186 rows from file row 91,971: 183 billed never-payers, no bad debt) is dropped by one run-level rule (at least 100 billed never-payers per run without debt; every other run holds at most 13): 101,686 rows, 56.25% bad. The billing totals carry no class signal within municipality-like file blocks (residual ROC AUC 0.509 / 0.501 / 0.496). The facts behind the CC of 2026-10-12 on `TotalElectricityBill` hold only in part: pooled, the median share is 0.301 for bad debts against 0.353, and within blocks mostly billed for electricity, accounts billed none are bad debts at 38.6% against 19.2%, while the median share among billed accounts is 0.334 for both. The quote "approximately 20 million records ... PostgreSQL" above is in neither the Kaggle description nor the OpenML 43838 copy of it; its source is unknown. Open for the curator (REVIEW.md): keep `TotalElectricityBill`, the LEAK-25 reading for the dropped runs, the LEAK-10 reading for the billing totals. ROC AUC 0.874, best single feature 0.787. Priority 2: gap -, use case -, source +, shape +, risk - (open leak readings under LEAK-10 and LEAK-25; the fit is approximate).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: HasIDNo.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset upload without a task or evaluation metric; no paper defines one.

## Reference

Kaggle
