---
unique_name: hepatitis_c_egypt
name: HEPATITIS_C_EGYPT
checked_by:
- Andrej
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Data Quality Issue
tags:
- New IID
- Search for better data
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

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap +, use case -, source -, shape -, risk - (Open issue 1: run recommends No (AHDS); independent columns suggest generated or replaced data). Likely generated or value-replaced file where every method ties with the class prior; would add only noise to rankings.

CC (2026-10-26, Lennart): leave out, with `AHDS` and `Data Quality Issue` (issue 1).

CC (2026-10-26, Lennart): issue 2: the record's earlier note that the ALT columns are "future follow-up measurements, temporal leakage" is corrected: the columns are measured during and after treatment, so a definition at the biopsy would drop them, but they do not leak (with all 28 features the models stay at macro AUC 0.48-0.50).

CC (2026-10-26, Lennart): issue 3: "mark this for later dataset searches in the record that we could search for more here": tagged `Search for better data`.

**Assessment (AI, 2026-10-26):** the open issues of 2026-10-07 are settled and removed from this record. No column depends on another, the label included, the values are flat over their ranges, and the stage cannot be predicted from any subset: a generated file or one with values replaced column by column; the paper's 99.48% (abstract) cannot come from it. **For a later search:** the real records may exist with the creators UCI lists (Sanaa Kamal, Mohamed ElEleimy, Doaa Hegazy, Mahmoud Nasr; Kamal et al. ran genotype-4 cohorts with RNA at weeks 4 and 12, end of treatment and 24 weeks after, 2005 and 2007); the paper is DOI 10.1109/ICENCO.2017.8289800 (closed access).

## Reference

A novel model based on non invasive methods for prediction of liver fibrosis
By Mahmoud Nasr, Khaled El-Bahnasy, M. Hamdy, S. Kamal. 2017

Published in International Computer Engineering Conference
