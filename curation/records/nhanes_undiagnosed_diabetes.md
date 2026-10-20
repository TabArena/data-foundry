---
unique_name: nhanes_undiagnosed_diabetes
name: NHANES Undiagnosed Diabetes Screening
tags:
- Non-IID (Temporal)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/nchs/nhanes/
- https://pubmed.ncbi.nlm.nih.gov/19949143/
- https://doi.org/10.2196/68260
- https://www.mdpi.com/2673-4540/5/1/1
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2007/DataFiles/GHB_E.htm
needs_review:
- suggestion
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-15, Lennart): new candidate, asked for as the screening task that `cdc_diabetes_health_indicators` could not be (retired the same day: its label was a diagnosis the respondent already had).

**Assessment (AI, 2026-10-15):** recommend `Yes`, `Temporal (NON-IID)` by survey cycle; the human has the call.
- What it is: NHANES (CDC/NCHS) interviews a sample of the US population at home and examines it in a mobile centre, with a blood draw; each 2-year cycle is a set of public tables joined on `SEQN`. Task: adults (20+, not pregnant) never told they have diabetes (DIQ010 no or borderline); label HbA1c >= 6.5% in the exam, i.e. undiagnosed diabetes. Features: what a screening visit has, the interview answers (age, sex, family history, told high blood pressure, cholesterol or prediabetes, smoking, activity, education, income) and the measured BMI, waist and blood pressure; no lab values.
- Published use: Bang et al. 2009 (the ADA risk test) built the score on NHANES 1999-2004, validated on 2005-2006, outcome "fasting plasma glucose >=7.0 mmol/L (126 mg/dL) without known diabetes" (Abstract); "we envision our screening score to serve as a method for identifying individuals in need of formal diabetes screening" (Discussion). Liu et al. 2025 fit ML models for it on NHANES 1999-2020 ("no prior self-reported diagnosis but meeting any of the diagnosis criteria", Methods); Cichosz et al. 2024 on 2005-2018 with HbA1c (abstract).
- Data (my build of 1999-2018 and 2021-2023): 47,220 adults, 1,619 positives, 100-190 per cycle. FPG exists only for the fasting half, so HbA1c is the one test every row has.
- Signal: logistic regression and LightGBM trained on earlier cycles reach ROC AUC 0.81-0.86 on each of 2013-14, 2015-16, 2017-18 and 2021-23; interview answers alone 0.78-0.82; age, BMI and waist 0.73-0.77. Linear and boosted models tie.
- Open for `/add-dataset`: HbA1c "shifted to higher values" in 2007-2010 after an instrument change, with no correction (GHB_E analytic note; positives 2.8% to 4.1%); 2021-2023 dropped the family-history question (MCQ_L note) and gestational diabetes; the 2017-March 2020 files (new SEQNs, replacing 2017-2018: 6,743 adults, 284 positives) keep it; activity questions changed in 2007 and 2021; race/ethnicity as a feature; no survey weights.
- Unique: `nhanes_age_prediction` (UCI 887) is a 2013-2014 subset with an age-group target. Licence: US public-use data.

## Reference

Bang H, Edwards AM, Bomback AS, et al. Development and validation of a patient self-assessment score for diabetes risk. Ann Intern Med. 2009;151(11):775-783.
