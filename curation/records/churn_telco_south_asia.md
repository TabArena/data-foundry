---
unique_name: churn_telco_south_asia
name: CHURN_TELCO_SOUTH_ASIA
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
collections:
- TabSTAR
original_source: Kaggle
year: '2017'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=44227
- https://www.kaggle.com/datasets/mahreen/sato2015
v2_path: datasets/_dev/tabarena-v0pt2/churn_telco_south_asia/dataset.py
source_row: 674
type_adapter_id: curation-record-v1
---

## Comments

"operator, with 13 features and 2000 records, collected between Aug 2015 to Sep 2015"

"To overcome the class imbalance problem in
churn data sets, an equal amount of churners and active
subscribers were collected from the carrier. So the data has 50% churner's information."

**Assessment (AI, 2026-10-07):** The DSN Telecoms Churn 2018 competition files (record churn_telco_south_asia_duplicate; OpenML 44229, 44230) are this file with the networks renamed (mobilink Mango, ufone Uxaa, ...): all 2,000 rows match on the nine numeric columns and all 1,400 labelled rows agree, so that record is the duplicate. Not trivial: random forest ROC AUC 0.815 against 0.729 for the raw total revenue (30 splits). The 50% churn rate is set by design; ROC AUC does not depend on it. Open: whether churn was observed after the Aug-Sep 2015 window or inside it (then the aggregates end at the churn, as iranian_churn). The paper (doi:10.1109/IntelliSys.2017.8324367) is closed access, and the data do not settle it.

Open (2026-10-12): a paper to get. IntelliSys 2017, doi 10.1109/IntelliSys.2017.8324367 (closed access; no free copy found in the 2026-10-07 run), would settle when churn was observed in this data, which decides whether the usage columns describe the time before the churn.

**Assessment (AI, 2026-10-15):** The authors' journal paper (Ahmed et al., Neural Computing and Applications 32:3237-3251, doi 10.1007/s00521-018-3678-8) does not say when churn was observed either: "The subscriber data is extracted from the time interval of two months, i.e., August and September 2015" (Sec. 3.1, p. 3241); "class labeling (for SATO dataset)" is listed as a preprocessing step without a definition (Sec. 3.2). Nor does the IntelliSys 2017 paper (Sec. III, p. 680, the source of the quotes above; "class labeling" is a preprocessing step, Sec. IV), so no source settles it; the definition keeps churn after the window, with fit `approximate`. Both papers list "Package Name" as a feature (among the top five in the journal paper, Sec. 4), which the public file lacks.

CC (2026-10-15, Lennart): ship, kept for now although the task may be problematic: neither paper says when churn was observed, and if the churners left inside August-September, the usage totals end at the outcome (the iranian_churn reason). The definition states this as a potential leak kept on purpose; revisit if the churn can be dated. The impossible negative `network_age` values and the undocumented `aug_fav_a` "0" are missing; the other anomalies stay as published.

CC (2026-10-21, Lennart): option (a) of the consistency check on one-snapshot churn sets: tagged `ForcedIIDFromTemporal`; SPLIT-8 now covers a release with one stock month or one undated snapshot.

**Assessment (AI, 2026-10-21):** tag and one note line added; a dated earlier window would test the model across shifts in usage and the network mix; not measurable on one two-month window.

## Reference

@inproceedings{ahmed2017mcs,
  title={MCS: Multiple classifier system to predict the churners in the telecom industry},
  author={Ahmed, Mehreen and Siddiqi, Imran and Afzal, Hammad and Khan, Behram},
  booktitle={2017 Intelligent Systems Conference (IntelliSys)},
  pages={678--683},
  year={2017},
  organization={IEEE}
}
