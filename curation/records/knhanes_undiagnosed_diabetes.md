---
unique_name: knhanes_undiagnosed_diabetes
name: 'Korea National Health and Nutrition Examination Survey (KNHANES): adults never told they have diabetes, undiagnosed diabetes by fasting glucose or ...'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.1093/ije/dyt228
- https://knhanes.kdca.go.kr
- https://doi.org/10.4178/epih.e2021025
- https://doi.org/10.2337/dc11-2347
- https://doi.org/10.4178/epih.e2022009
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: Korea's yearly national health examination survey, on which the published Korean diabetes screening score was built (Lee et al. 2012); the same undiagnosed-diabetes screening task as `nhanes_undiagnosed_diabetes`, a blood-test label for adults never told they have diabetes, in yearly waves.
- Source: the Korea National Health and Nutrition Examination Survey (KNHANES) of the Korea Disease Control and Prevention Agency, since 1998, yearly since 2007 (data resource profile: Kweon et al., Int J Epidemiol 43(1), 2014, doi 10.1093/ije/dyt228; Oh et al., Epidemiol Health 2021, doi 10.4178/epih.e2021025: "making the overall data publicly available on the official website of KNHANES"). As published: yearly raw-data files of interview, examination and laboratory variables, downloaded from knhanes.kdca.go.kr after registration (procedure not read; codebooks partly Korean). Size: 40,059 adults over 2010-2017 in one study (Park et al. 2022: 19,675 + 19,917); 2007-2023 not counted.
- Use case: Lee et al. 2012 (Diabetes Care 35, doi 10.2337/dc11-2347): "We developed and validated a self-assessment score for diabetes risk in Korean adults" on KNHANES 2001 and 2005, validated on 2007-2008, "useful for identifying Korean adults at high risk for diabetes" (Conclusions): a person or a clinic decides who gets a glucose test. Label: undiagnosed diabetes among adults without known diabetes, fasting glucose >=126 mg/dL (Lee 2012), or also HbA1c >=6.5% (Park et al., Epidemiol Health 2022, doi 10.4178/epih.e2022009). Fit direct. Regime temporal by survey year (both papers validate on other years).
- Siblings and duplicates: `nhanes_undiagnosed_diabetes` (no verdict yet; the US survey: the same task from another source, no duplicate, PROV-4); `cdc_diabetes_health_indicators` (retired, SEL-7). No KNHANES record (grep knhanes, Korea National Health). External collections: none found.
- Better data: found as better data for `nhanes_undiagnosed_diabetes`.
- Papers and pages: Kweon et al. 2014; Oh et al. 2021; Lee et al. 2012; Park et al. 2022.
- Metric: Lee et al. 2012 report sensitivity, specificity, PPV and AUC at their score's cut point; Park et al. 2022 sensitivity, specificity and the Youden index; several metrics and no model threshold fixed, so the fallback `roc_auc` (MET-5, MET-6), also Lee's figure for comparing scores.
- Risks for /add-dataset: which years measured HbA1c in every adult (not checked) and fasting compliance decide the label per wave, so the label definition may change across waves (USE-5); yearly files with changing variable names to stack; exclude everyone told of or treated for diabetes (interview), keep "told hypertension" (known then); survey weights unused.
- Priority: gap 0 (medical, binary, temporal not thin), use case + (a published screening score and its decision), source + (KDCA, a data resource profile), shape + (about 5,000 adults a year, mixed types, yearly waves), no known risk counted.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nhanes_undiagnosed_diabetes`.
- as published: About 10,000 people a year with a health examination since 2007 (Epidemiol Health 2021, Table 1); 127,545 examined in 1998-2018. A published undiagnosed-diabetes study used 40,059 adults from ...; target: Undiagnosed diabetes among adults never diagnosed or treated: fasting plasma glucose >=126 mg/dL or HbA1c >=6.5% (Epidemiol Health 2022 definition); access: registration.
- Why: Same task as the record: the label is a blood test of people who report no diagnosis, and the features are of the same kind (the interview's age, sex, family history, told hypertension, smoking, alcohol, activity, education and income, plus measured BMI, waist and blood pressure). The survey runs in yearly waves, so ...
- Adds: Probably larger: about 5,000 adults a year after exclusions, against NHANES's 2,500 a year in 2-year cycles. It adds a second population (Korean adults) for the same task and is just as recent. The first scout called it not clearly larger; the 2010-2017 count (40,059 adults in 8 years) supports roughly 1.7x NHANES ...
