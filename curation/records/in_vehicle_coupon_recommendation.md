---
unique_name: in_vehicle_coupon_recommendation
name: in_vehicle_coupon_recommendation
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
original_source: UCI
year: '2017'
required_split:
- Grouped (NON-IID)
source_links:
- https://doi.org/10.24432/C5GS4P
notebook_path: datasets/beyond_iid/old_iid/in_vehicle_coupon_recommendation/in_vehicle_coupon_recommendation.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/in_vehicle_coupon_recommendation/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Re-split as a cold-start task, grouped by survey respondent; ROC AUC 0.83 random -> 0.75 grouped.** Wang et al. 2017 (JMLR 18), Sec. 6.2: MTurk survey, 652 accepted surveys, 12,684 rows; "In the first part of the survey, we asked users to provide their demographic information and preferences. In the second part, we described 20 different driving scenarios ... to each user"; evaluated with random 5-fold testing (Table 3), i.e. warm start. The file has 22 scenarios per person from 19 fixed questionnaire versions, answered in one sitting without timestamps, so there is no interaction history to simulate a warm start; a random split lets a model learn each person's tendency to say yes from their other hypothetical answers. We simulate a cold-start model (as used before a recommender has history for a user): new people, known profile and stated habits (the visit-frequency columns are the base preference). The respondent id is not shipped; the raw file lists each respondent's answers as one consecutive block with identical first-part answers (13 columns), giving 587 groups (517 of 22 rows; a few blocks likely merge two adjacent respondents with identical profiles, which is stricter). The audit's profile-only id (567 groups) merged different people. LightGBM on the grouped splits: AUC 0.75 (0.742-0.764 over 6 folds). TabArena v0.1 dataset: results on the old IID container are not comparable.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

data was collected via a survey on Amazon Mechanical Turk. The survey describes different driving scenarios including the destination, current time, weather, passenger, etc., and then ask the person whether they will accept the coupon if they are the driver. features might be time invariant, but need to check

Potential issue: "faked" data via a survey

Lennart: Leaning towards yes, features seem time invariant; but data source might be fake

Andrej: Need to test whether time-invariant; Mechanical turk data might be interesting to include

## Reference

A Bayesian framework for learning rule sets for interpretable classification By Wang, Tong, Cynthia Rudin, Finale Doshi-Velez, Yimin Liu, Erica Klampfl, and Perry MacNeille. 2017
 Published in The Journal of Machine Learning Research 18, no. 1
