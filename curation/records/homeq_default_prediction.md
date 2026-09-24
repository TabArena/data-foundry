---
unique_name: homeq_default_prediction
name: HMEQ_Data
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
tags:
- New IID
collections:
- New (BeyondArena)
- TabSTAR
original_source: Website
year: '2016'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ajay1735/hmeq-data
- http://www.creditriskanalytics.net/datasets-private2.html
notebook_path: datasets/beyond_iid/new_iid/homeq_default_prediction/homeq_default_prediction.ipynb
source_row: 679
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-24, Lennart): **Retired: the two classes were generated differently, so a model can separate them from row-generation artefacts rather than credit risk (crit. 4D).** Measured on the source `hmeq.csv` after the notebook's preprocessing (5,708 rows), 5-fold LightGBM AUC:
- Nearest-neighbour distance alone, computed without labels: AUC 0.923. About 60% of rows sit in label-pure clusters of near-copies that differ by a few percent in LOAN/MORTDUE/VALUE/CLAGE/DEBTINC and share YOJ/DEROG/DELINQ/NINQ/CLNO/JOB. Only 1-2% of the rows in these clusters are defaults, so having a near-twin effectively means "paid loan".
- Number formatting: CLAGE*30 is a whole number (days/30) for 63% of defaults vs 10% of paid loans; VALUE is a multiple of 100 for 45% vs 8%.
- Missingness: every row with VALUE missing is a default; the default rate is 62% when DEBTINC is missing vs 9% when present.
- These artefacts alone reach AUC 0.953; all features reach 0.975. No single column beats 0.65, and dropping any one costs at most 0.01. A grouped split over the near-copy clusters still gives 0.955-0.975, because the density itself is the tell.
Hypothesis (unverified, the book's text not read): the majority class of this textbook dataset was synthesised or oversampled by jittering.

Loan default prediction;

data from  http://www.creditriskanalytics.net/datasets-private.html?  (https://www.kaggle.com/datasets/ajay1735/hmeq-data/discussion/59708)
From http://www.creditriskanalytics.net/datasets-private2.html

Looks like it is real data, but hard to tell from education book

Use version from source

Home Equity Loans

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
