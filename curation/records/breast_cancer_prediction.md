---
unique_name: breast_cancer_prediction
name: Breast cancer prediction
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
collections:
- TabSTAR
original_source: GOV Website
year: '2014'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.bcsc-research.org/index.php/datasets/mammography_dataset
- https://www.kaggle.com/datasets/haithemhermessi/breast-cancer-screening-data-set
- https://www.openml.org/search?type=data&id=43687&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/breast_cancer_prediction/dataset.py
source_row: 677
type_adapter_id: curation-record-v1
---

## Comments

Cancer type and Is_Binary_Indicator_Of_Cancer_Diagnosis and Radiologists_Assessment might be target cols

"Some women contribute multiple examinations to the dataset." -> some leakage / problems

**Assessment (AI, 2026-10-07):** The original is the BCSC Digital Mammography Dataset (bcsc-research.org, 2014; download after a registration form, "teaching tool only"). Our file is byte-identical to the BCSC's `dataset.csv`; Kaggle and OpenML 43687 drop two duplicate rows. Target: cancer within one year, the BCSC's own question ("predict occurrence of any cancer using patient characteristics and mammography assessment"). Cancer type encodes the label and is dropped; TabSTAR keeps it. 3,133 of 36,714 women (`ptid`) have 2-4 exams; the 20 of them with cancer are positive only on their last. Grouped by woman. The BI-RADS assessment alone gives AUC 0.907, boosted trees 0.93; without the radiologist's readings, logistic regression reaches 0.58. Open: does the breast_w image rule cover these readings?

CC (2026-10-15, Lennart): The BI-RADS readings are valid tabular inputs: screening programmes run tabular risk models on them, so the image-scoring rule (breast_w) does not apply; the real-world use decides (review page, issue 1). One exam per woman, her earliest, with IID folds: the use case is one woman's screening read and most women have one exam (issue 2).

**Assessment (AI, 2026-10-15):** One exam per woman keeps 36,714 rows and 239 of the 259 cancers (the 20 women with cancer and several exams are positive only on their last exam). Untuned LightGBM scores alike either way (ROC AUC 0.928 earliest exam, 0.923 latest, 0.925 all exams grouped). Regularised LightGBM 0.929 and a random forest 0.927 beat the assessment alone (0.914) on 8 of 9 splits.

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: comparison_mammogram_available, current_hormone_therapy, prior_breast_biopsy, prior_mammogram, family_history_breast_cancer.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The BCSC page poses the question (predict any cancer from patient characteristics and the mammography assessment) but names no metric; it suggests the data for 'statistical methods for binary outcomes'.

## Reference

Other
