---
unique_name: breast_cancer_prediction
name: Breast cancer prediction
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
suggestion: 'Yes'
tags:
- New IID
collections:
- TabSTAR
original_source: GOV Website
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/haithemhermessi/breast-cancer-screening-data-set
- https://www.openml.org/search?type=data&id=43687&sort=runs&status=active
- https://datahub.io/JohnSnowLabs/mammography-data-from-breast-cancer-surveillance-consortium (website is dead)
v2_path: datasets/_dev/tabarena-v0pt2/breast_cancer_prediction/dataset.py
source_row: 677
type_adapter_id: curation-record-v1
---

## Comments

Cancer type and Is_Binary_Indicator_Of_Cancer_Diagnosis and Radiologists_Assessment might be target cols

"Some women contribute multiple examinations to the dataset." -> some leakage / problems

**Assessment (AI, 2026-10-07):** The original is the BCSC Digital Mammography Dataset (bcsc-research.org, 2014; download after a registration form, "teaching tool only"). Our file is byte-identical to the BCSC's `dataset.csv`; Kaggle and OpenML 43687 drop two duplicate rows. Target: cancer within one year, the BCSC's own question ("predict occurrence of any cancer using patient characteristics and mammography assessment"). Cancer type encodes the label and is dropped; TabSTAR keeps it. 3,133 of 36,714 women (`ptid`) have 2-4 exams; the 20 of them with cancer are positive only on their last. Grouped by woman. The BI-RADS assessment alone gives AUC 0.907, boosted trees 0.93; without the radiologist's readings, logistic regression reaches 0.58. Open: does the breast_w image rule cover these readings?

## Reference

Other
