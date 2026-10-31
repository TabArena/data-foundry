---
unique_name: loan_approval_prediction_dataset
name: Loan-Approval-Prediction-Dataset
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
tags:
- New IID
collections:
- New (BeyondArena)
source_links:
- https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset
source_row: 529
type_adapter_id: curation-record-v1
---

## Comments

The distribution of the data looks very fake (50/50 for a binary column)

I cannot determine if it is fake or not. It is used a lot.

Rel "Data Mining for Business Intelligence" by Galit Shmueli et al.?

Based on the available information, this does not look like a good task. Filter it for now

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `hmda_mortgage_application_decision` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.
