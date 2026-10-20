---
unique_name: credit_approval
name: Credit Approval
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
- Not Representative
- Anonymized
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: UCI
year: '1987'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5FS30
- https://doi.org/10.24432/C5259N
notebook_path: datasets/beyond_iid/new_iid/credit_approval/credit_approval.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_approval/dataset.py
source_row: 775
type_adapter_id: curation-record-v1
---

## Comments

The UCI source contains two datasets, this is the crx dataset in the data

Credit Approval (690 rows), credit card applications from an unnamed source (`crx.data`; not Japanese, see below)

**Assessment (AI, 2026-10-14):** The 690 rows are `crx.data`, Quinlan's Credit Approval (UCI 27; the source is "confidential", so the lender and country are not stated), not Japanese data. The same UCI zip holds the Japanese Credit Screening data (UCI 28, `credit.lisp`, 125 examples, Chiharu Sano 1992; the second source link, 10.24432/C5259N), which we do not use. Statlog (Australian Credit Approval) (UCI 143) is the same 690 applications with recoded values and filled-in missing values: its rows are those of `crx.data` in another order (four numeric columns and the label match as a multiset).

CC (2026-10-15, Andrej): Keep (agree with Lennart), flagged `Anonymized`. The dataset is very outdated, but none of the possible exclusion reasons below is a defect of the data.
- Anonymized features: all 15 attribute names and values are symbols, so we cannot check that each one is known when an application arrives, or rule out leakage → not a requirement for inclusion; the v2 definition carries the `Anonymized` data tag instead.
- One dominant feature: `A9` (t/f) alone gives 85.5% accuracy and ROC AUC 0.862 (unofficial column names on Kaggle call it "prior default") → the other features add a lot: on our 20×3 splits, logistic regression reaches 0.925, random forest 0.933 and TabPFN 0.939, while logistic regression without `A9` gets 0.850. Methods also separate: TabPFN beats the random forest in 53 of 60 splits.
- Outdated and not representative: the data is from 1987, the bank and country are not named, and the label is the bank's approval decision, not repayment (Quinlan: "provided by a large bank", "two decision classes"; Quinlan, J. R. (1986). Simplifying Decision Trees. MIT AI Memo 930, p. 12, https://dspace.mit.edu/handle/1721.1/6453) → recorded as decision markers, not a reason to exclude.
- Redundant: BeyondArena already has about 14 finance and credit tasks, and its data properties (small, mixed categoricals, native missing values) are shared by about 20 other tasks with at most 3,000 rows → a question of how much weight finance gets in the benchmark, not of the data, so not a reason to exclude.

## Reference

@article{quinlan1987simplifying,
  title={Simplifying decision trees},
  author={Quinlan, J. Ross},
  journal={International journal of man-machine studies},
  volume={27},
  number={3},
  pages={221--234},
  year={1987},
  publisher={Elsevier}
}
