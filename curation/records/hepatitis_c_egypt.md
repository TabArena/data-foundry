---
unique_name: hepatitis_c_egypt
name: HEPATITIS_C_EGYPT
checked_by:
- Andrej
- Lennart
suggestion: 'Yes'
tags:
- New IID
collections:
- TabSTAR
original_source: UCI
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/503/hepatitis+c+virus+hcv+for+egyptian+patients
- https://www.openml.org/search?type=data&id=46607
- https://doi.org/10.24432/C5989V
source_row: 676
type_adapter_id: curation-record-v1
---

## Comments

Paper reports pretty good performance, need to pay attention to target leaks. Unclear when the target was collected. Was it really after the features or can features leak the target?

After consulting Dr. GPT, learned that ALT features correspond to future follow-up measurements - temporal leakage. We could use the other features, but that's probably not very useful.

**Assessment (AI, 2026-10-07):** The UCI file (OpenML 46607 is identical) does not behave like patient records. Its columns are independent: 21 of 406 pairs pass the 95% noise band, 20 by chance. The links HCV cohorts show are absent: AST-ALT r = 0.04, RBC-HGB 0.04, the same HGB in men and women, FIB-4 against stage AUC 0.47-0.49 (0.71-0.82 in 19,501 Egyptian biopsies, El-Kassas et al. 2024), and response is unrelated to grade, stage and baseline RNA, its predictors in the creator's own cohort (Kamal et al. 2007). AST and six ALT visits are uniform on 39-128. The stage cannot be predicted (macro AUC 0.48-0.51). Suggest No + AHDS; Data Quality Issue if real values were replaced.

## Reference

A novel model based on non invasive methods for prediction of liver fibrosis
By Mahmoud Nasr, Khaled El-Bahnasy, M. Hamdy, S. Kamal. 2017

Published in International Computer Engineering Conference
