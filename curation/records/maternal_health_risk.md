---
unique_name: maternal_health_risk
name: maternal_health_risk
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
original_source: UCI
year: '2020'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C5DP5D
notebook_path: datasets/beyond_iid/old_iid/maternal_health_risk/maternal_health_risk.ipynb
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Retired: the true group structure (collection site, source, patient) cannot be recovered, and a third of the rows are unexplained copies.** The dataset paper is Ahmed & Kashem 2020 (STI 2020, IEEE, doi 10.1109/STI50764.2020.9350320), not the LNEE paper UCI links: its Sec. VI, p. 3 gives exactly our file ("The total data size is 1014 where 406 was classified as low-risk level, 336 in mid and 272 was in high-risk level"). Data were "prepared from different sources (IoT device, Web portal, Hospitals in Bangladesh)" (Abstract), collected by questionnaire at six sites on about ten dates in 2018-2020 (Sec. V, Table 1: a maternity clinic in Chuadanga, Khulna, and Kurmitola, Aichi, Uttara Adhunik, East-West and CARe hospitals in Dhaka); the risk level is set "With the help of medical experts, and from the literature review" (Sec. IX, p. 5). The file has no site, source, date or patient column. Only 416 of 1,014 feature vectors are unique; rows 700-1,013 are 97-100% copies of earlier rows, in label-sorted blocks; 74% of test rows under the shipped IID split have an exact copy in train (LightGBM AUC 0.94 shipped vs about 0.80 grouped by feature vector; leak audit 2026-09-24). The paper does not mention the duplicates. The LNEE paper (Ahmed et al. 2020, LNEE vol. 632) describes a different dataset (Pima diabetes plus a few IoT samples, 736 rows). Grouping by feature vector would only hide the copies, not the site structure, so the dataset is dropped.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Target: Predicted Risk Intensity Level during pregnancy.Data has been collected from different hospitals, community clinics, maternal health cares from the rural areas of Bangladesh through the IoT based risk monitoring system.

Potential issue: -

Lennart: Grouped data unclear, but otherwise invariant to this. Moreover, feature is risk level which sounds preprocssed/weird

Andrej: Pretty simple features, unclear how many different patients and whether there are clusters

## Reference

@inproceedings{ahmed2020iot,
  title={IoT Based Risk Level Prediction Model For Maternal Health Care In The Context Of Bangladesh},
  author={Ahmed, Marzia and Kashem, Mohammod Abul},
  booktitle={2020 2nd International Conference on Sustainable Technologies for Industry 4.0 (STI)},
  pages={1--6},
  year={2020},
  organization={IEEE},
  doi={10.1109/STI50764.2020.9350320}
}

UCI links the earlier paper, which describes a different dataset: Ahmed, M., Kashem, M.A., Rahman, M., Khatun, S. (2020). Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT). Lecture Notes in Electrical Engineering, vol 632.
