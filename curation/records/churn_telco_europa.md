---
unique_name: churn_telco_europa
name: Churn_Telco_Europa
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Missing source information
- Ethical Issue
- Data Quality Issue
tags:
- Larger IID Data
collections:
- TabSTAR
original_source: Kaggle
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=44228&sort=runs&status=active
- https://www.kaggle.com/datasets/raumonsa11/churn-telco-europa
source_row: 654
type_adapter_id: curation-record-v1
---

## Comments

OpenML version uses the test data with all churn for all customers? That is just a placeholder? In the notebook it was used as test data, so maybe we can combine it and treat it as such? Otherwise, just stick to train data to avoid problems.

https://www.kaggle.com/code/raumonsa11/churn-telco-europa-spa-eng/notebook
Uploader says it is real data.

Even with missing source information, this might be a good dataset.

**Assessment (AI, 2026-10-07):** Recommend No: Data Quality Issue (as iranian_churn) and Ethical Issue. The uploader's earlier notebook (raumonsa11/leak-or-not-leak-classification-models) shows the original extract: target `FLAG_PARQUE` (in WOM Chile's active base), tenure `VIDA_WOM`, churn reason and destination operator. No line has a follow-up; the test file is more active lines (AUC 0.50 against the stayers). Active lines were measured on one date: tenure keeps the activation weekday pattern. Churners were measured on their own exit dates, and the pattern is gone. Churner-only `DEVICE_TECNOLOGY` codes: 7,025 rows. LightGBM AUC 0.956; tenure and plan still 0.88 without those codes and short tenures. No dates to re-anchor. The file holds RUT national ids and mobile numbers of about 110,000 people, also on OpenML 44228.

**Assessment (AI, 2026-10-12), personal data:** Both files (Kaggle raumonsa11/churn-telco-europa; OpenML 44228 serves the same 20 columns) hold directly identifying data of WOM Chile customers. `CNI_CUSTOMER` holds Chilean national ids (RUT): 98.9% of its values have the RUT form and every one of them has a valid RUT check digit (random numbers pass about 1 in 11), 102,965 distinct in the training file. `CETEL_NUMBER` holds Chilean mobile numbers (99.9% have the 9 + 8 digits form, 183,661 distinct). The state and city of the antennas used for voice and data are there too. Together with the plan, the device and the churn, this is personal data that a public dataset should not carry; the raw copy stays in the local warehouse and is never shared.

CC (2026-10-12, Lennart): No: the data are not what the name says. They are WOM Chile's customers (Chilean national ids and mobile numbers) under a European name, they carry personal data, and active lines and churners were measured on different dates (assessment of 2026-10-07).

## Reference

Kaggle
