---
unique_name: cdc_diabetes_health_indicators
name: CDC Diabetes Health Indicators (BRFSS 2015)
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- Larger IID Data
collections:
- New (BeyondArena)
- TabSTAR
original_source: GOV Website
year: '2016'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
- https://www.kaggle.com/code/alexteboul/diabetes-health-indicators-dataset-notebook
- https://doi.org/10.24432/C53919
- https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
- https://www.openml.org/search?type=data&id=46598&sort=runs&status=active
- https://www.cdc.gov/brfss/annual_data/2015/pdf/codebook15_llcp.pdf
- (https://www.kaggle.com/datasets/tarekmuhammed/patients-data-for-medical-field/ is a duplicate / cleaned version)
source_row: 657
type_adapter_id: curation-record-v1
---

## Comments

Dataset is preprocessed version already https://www.kaggle.com/code/alexteboul/diabetes-health-indicators-dataset-notebook
The selection looks very reasonable and well motivated, I would keep it.
Biggest problem: it drops rows with na...

It makes sense to filter to only cases that answer the questions truthfully and fully for a less-biased predictive model in the medical domain. Moreover, given the large amount of data, this seems okay to do it. I would use it the way it is for now and only fix / add new version of it if we get a domain expert to make the decisions.

Goes from 441,456 records and 330 -> 253,680, 21

Need to decide which version to take for the label:
0 = no diabetes 1 = prediabetes 2 = diabetes
0 = no diabetes 1 = prediabetes &  diabetes

Use first case as it is more native to the real world problem and less biased.


(Rel https://www.cdc.gov/pcd/issues/2019/19_0109.htm)

CC (2026-09-23, Lennart): This record curates Teboul's "Diabetes Health Indicators" cut of BRFSS 2015 (253,680 x 21, diabetes target), which is what the notes above describe; UCI 891 (DOI 10.24432/C53919) and OpenML 46598 mirror it. It used to be named after its first link, kamilpytlak's "Personal Key Indicators of Heart Disease" (https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease), which is a different BRFSS cut (2020 wave, heart-disease target) and is not covered by this record; if wanted it needs its own record, and by our duplicate rule (same BRFSS data with another target) it would likely be `No` + `Duplicate`. TableShift's BRFSS Diabetes task (`diabetes_2`, waves 2015-2021, race shift) is marked Duplicate of this record.

**Assessment (AI, 2026-10-07):** Teboul's notebook reproduces the CSV row for row from the CDC's BRFSS 2015 file; every row is a distinct respondent, so the 23,899 duplicate rows are natural. The binary alternative above is misread: Teboul's binary files put prediabetes into class 0 (notebook cell 48), as TableShift does; UCI 891 and OpenML 46598 copy them. Prediabetes is DIABETE3 code 4, recorded only when volunteered (2015 codebook, p. 21): in the 15 states that asked PREDIAB1 (p. 50), 14-23% of respondents told they have prediabetes are in that class. The NA drop also removes all 49,673 respondents never cholesterol-checked (TOLDHI2 is skipped for them, p. 17), not refusals.

CC (2026-10-15, Lennart): No, `No Good Target / Scientific Discovery`: the task is formulated wrongly. The label is "ever told you have diabetes", a diagnosis the respondent already has, predicted from answers of the same interview; no decision is made with that prediction. The use the sources name, screening (Xie et al. 2019: "initial population screening for type 2 diabetes"; Teboul's card: "whether an individual has diabetes"), needs the undiagnosed as positives, and BRFSS cannot identify them: they sit in the negative class. The three classes add a prediabetes class recorded only when volunteered. A screening task on lab-measured undiagnosed diabetes is the new candidate `nhanes_undiagnosed_diabetes`.

**Assessment (AI, 2026-10-15):** Evidence for the retirement. Kept diabetics were told a median of 10 years before the interview (75.1% at least 5 years; DIABAGE2 against `_AGE80`, 34,119 rows), so the answers mostly describe life after diagnosis. Xie et al. (Prev Chronic Dis 16:190109, Discussion) report checkup frequency as a risk factor and explain it as "People with diabetes may see a doctor more frequently": an effect of the diagnosis read as a predictor. The data card itself says "1 in 5 diabetics, and roughly 8 in 10 prediabetics are unaware". UCI 891 gives the purpose as "To better understand the relationship between lifestyle and diabetes in the US". Rebuilding the cohort from the raw 2015 file would not help: the label stays a past diagnosis.

## Reference

Kaggle
