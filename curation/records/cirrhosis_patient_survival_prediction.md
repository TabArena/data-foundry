---
unique_name: cirrhosis_patient_survival_prediction
name: Cirrhosis Prediction Dataset
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
collections:
- New (BeyondArena)
original_source: Other
year: '1991'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/cirrhosis-prediction-dataset
- https://www.mayo.edu/research/documents/pbchtml/doc-10027635
- https://doi.org/10.24432/C5R02G
notebook_path: datasets/beyond_iid/new_iid/cirrhosis_patient_survival_prediction/cirrhosis_patient_survival_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/cirrhosis_patient_survival_prediction/dataset.py
source_row: 772
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Deaths-only target is intended: a survival-time task without censoring by design.** The leak audit (2026-09-24) flagged that the target (time to death) is defined only for patients who died, so censored patients are dropped. This is on purpose: the task is to predict the survival time of patients who die, not a censored survival analysis, so no change. The 36 of 161 rows with Drug/Ascites/Hepatomegaly/Spiders/Copper/Alk_Phos/SGOT missing are the non-trial patients (a cohort signal, not a leak).

Need to check for duplicates and original source.

Might be RCT data, not sure what the target might become?

Status contains censored data, need to figure out how to use and work with this.
Clearly a survival task as it seems.

We treat it as an uncensored time to death prediction task or similar as we do not score original survival prediction tasks so far.

**Assessment (AI, 2026-10-14):** The deaths-only target was right truncation. N_Days ends at death, transplant or the July 1986 analysis for every patient, and the IDs follow the registration order within the trial (1-312) and within the other patients (313-418): among the censored, Spearman of ID with N_Days is -0.96 and -0.87. Estimating each patient's registration from the longest follow-up of anyone registered at or after them in the same group, the median time to death is 3.98 years for the 74 deaths among 1974-76 registrations and 1.86 years for the 9 among 1982-84 (the earlier investigation had 4.35 and 1.86; its registration estimate differed). The population is not end-stage: Kaplan-Meier median survival 9.3 years (transplant censored); 157 of 418 patients have bilirubin at most 1.0, and 93% of them are alive without transplant at 5 years, yet a random forest fit on the deaths only (bilirubin, albumin, age, prothrombin) predicts them a median 4.7 years to death.
- New label: death (D) or transplant (CL) with N_Days at most 5 * 365.25 (day 1,826 or earlier) is 1; at least 5 years of follow-up without either is 0; the 5 patients lost to follow-up before 5 years (IDs 199, 234, 318, 321, 326) are dropped.
- Cohort: 304 patients, 107 positives (103 D, 4 CL), 238 in the trial and 66 outside it. The rule without the registration condition gives 329 / 132: the 25 extra are patients registered after about mid-1981 (12 D, 13 CL) whose follow-up could not reach 5 years, so they can only be positives (the other 84 late registrants are censored). On 329 the estimated registration year alone gives ROC AUC 0.61, on 304 0.52, so the definition keeps 304.
- ROC AUC on 304 (repeated stratified 3-fold, 10 repeats, untuned): logistic regression 0.87, random forest 0.89, LightGBM 0.86, bilirubin alone 0.86, registration year 0.52. Task probes on the shipped splits (30 of 60): linear 0.872, random forest 0.891, LightGBM 0.872, best single feature 0.792 (bilirubin in 23 splits), no flags. Leak probes: bilirubin alone 0.825; missing indicators 0.46-0.50 (being outside the trial carries no label signal); no test row has an exact copy in train.
- The features are the values at registration: the pbcseq documentation (R survival package) says "The F&H data set contains only baseline measurements of the laboratory parameters", and the drug is the randomised arm.
- Sources checked: Dickson et al. 1989 (Hepatology 10:1-7, abstract) built the Mayo model on the 312 trial patients and validated it on the 106 others, as an aid "in the selection of patients for and timing of orthotopic liver transplantation"; its abstract names survival as the endpoint, not transplant-free survival, so the definition does not call this the Mayo endpoint. Lammers et al. 2015 (Gastroenterology 149:1804-1812, the GLOBE score) predicts transplant-free survival (death or liver transplantation) of patients on ursodeoxycholic acid and reports 5- and 10-year predictions.

CC (2026-10-14, Lennart): New task: death or liver transplant within 5 years of registration, over the patients followed 5 years; replaces the deaths-only time to death.

CC (2026-10-14, Lennart): The 5-year task has a good target: marker `No Good Target (yet)` and the open `?` in required_split removed.

## Reference

Fleming, T.R. and Harrington, D.P. (1991) Counting Processes and Survival Analysis. Wiley Series in Probability and Mathematical Statistics: Applied Probability and Statistics, John Wiley and Sons Inc., New York.

(get correct version ref)

Real
