---
unique_name: credit_approval
name: Credit Approval
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: Yes (Disagreement)
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
original_data_state: Database (or multiple to-be-joined tables)
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

Credit Approval (690 rows), From a Japanese

**Assessment (AI, 2026-10-14):** The 690 rows are `crx.data`, Quinlan's Credit Approval (UCI 27; the source is "confidential", so the lender and country are not stated), not Japanese data. The same UCI zip holds the Japanese Credit Screening data (UCI 28, `credit.lisp`, 125 examples, Chiharu Sano 1992; the second source link, 10.24432/C5259N), which we do not use. Statlog (Australian Credit Approval) (UCI 143) is the same 690 applications with recoded values and filled-in missing values: its rows are those of `crx.data` in another order (four numeric columns and the label match as a multiset).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Quinlan 1987 and the Statlog Australian study score error rate without costs or a threshold; accuracy rejected.

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
