---
unique_name: hsls09_postsecondary_enrollment
name: High School Longitudinal Study of 2009 (HSLS:09), base year to second follow-up public-use file
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: education
problem_type: Binary Classification
source_links:
- https://nces.ed.gov/surveys/hsls09/hsls09_data.asp
- https://catalog.data.gov/dataset/high-school-longitudinal-study-of-2009
- https://nces.ed.gov/datalab/onlinecodebook
- https://doi.org/10.3390/bdcc9040099
- https://nces.ed.gov/surveys/hsls09/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: a national NCES cohort of 23,000+ ninth graders in 944 schools followed to 2016, with postsecondary enrollment measured years after the 9th-grade features; education is a thin domain, and a published ML study uses the task.
- Source: National Center for Education Statistics, High School Longitudinal Study of 2009 (HSLS:09): "Nationally representative, longitudinal study of 23,000+ 9th graders from 944 schools in 2009"; waves: base year 2009, first follow-up 2012, 2013 update, high school transcripts 2013-14, second follow-up 2016, postsecondary transcripts 2017-18, and a 2024 administrative-records release on enrollment by June 2021 (nces.ed.gov/surveys/hsls09). As published: questionnaires of students, parents, math and science teachers, administrators and counselors, and an algebra assessment in 9th and 11th grade; "Public-use data is available for immediate download" through the NCES DataLab online codebook, restricted-use data under licence (hsls09_data.asp); data.gov lists the study as well.
- Use case: a high school counselor or college-access programme identifies 9th to 11th graders unlikely to enrol and targets advising, financial-aid help or dropout prevention. He, Yousefpoori-Naeim, Cui and Cutumisu, "Predicting College Enrollment for Low-Socioeconomic-Status Students Using Machine Learning Approaches", BDCC 9(4):99 (2025), trained five classifiers on 5,223 low-SES ninth graders of HSLS:09 and "highlight two important factors for intervention". Fit approximate until the prediction wave is fixed (their top predictor is the overall high school GPA, known only at the end of high school). Regime grouped by school (944 schools; a new school's students).
- Siblings and duplicates: `hsls09_secondary_student_achievement` (a candidate of this run: the same public-use file with an achievement target; a distinct task, PROV-7, though the curator may take one); `els2002_bachelors_attainment` (a candidate of this run: the earlier NCES cohort, a degree target); `irish_educational_transitions_irish` (`No`, `Outdated`, `Trivial`: 500 Irish pupils of 1967). External collections: none found.
- Better data: found as better data for `irish_educational_transitions_irish`, and by the gap scout for education; no further search this round.
- Papers and pages: the NCES study and data pages, the HSLS:09 FAQ (Appendix L of the data file documentation compares the public-use with the restricted-use data and lists altered or suppressed variables); He et al. 2025 (abstract via Crossref; the MDPI full text returned 403 here).
- Metric: He et al. report "the random forest algorithm achieved the highest classification accuracy at 67.73%" in the abstract; their evaluation section was not read, and a headline accuracy is not by itself a deliberate choice (MET-5), so the fallback `roc_auc` until it is read (MET-8). Inputs none (the survey weights ship, but no source scores with them).
- Risks for /add-dataset: hundreds of variables across waves, so the features must be cut at the prediction wave (9th grade, or the 2012 follow-up) and every later-wave and postsecondary variable dropped (LEAK); the target (any enrollment by 2016, 2-year against 4-year, or high-school completion); the public-use file alters, coarsens or suppresses variables (Appendix L) and imputes some composites; whether a school id ships in the public-use student file decides the grouped split; nonresponse in the 2016 wave.
- Priority: gap + (education has three accepted datasets), use case + (a published ML study names the intervention), source + (NCES with codebook and documentation), shape + (23,000+ students, survey, test and school features, grouped by school), risk - (a wave cut, with many later-wave columns to exclude).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `irish_educational_transitions_irish`; the gap scout for education.
- as published: more than 21,000 9th graders in 944 schools (data.gov); waves 2009, 2012, 2013 update, 2016; hundreds of student, parent, school and transcript-derived variables; data.gov lists the licence as CC0; target: postsecondary enrollment by 2016 (2-year or 4-year college), or high school completion; both are measured outcomes of the later waves; access: open.
- Why: a strong federal source with a codebook, open download, an outcome measured years after the features, and a published ML use of the exact task | The same task as the Irish record (does a pupil complete upper-secondary school, i.e. sit the Leaving Certificate, from an early ability test score, family background and ...
- Adds: a US secondary-to-postsecondary transition task grouped by school (944 schools), with survey answers, test scores and GPA as mixed features; nothing of the kind is in the benchmark | About 40x the pupils (500 in 1967 vs 21,000+ in 2009), a national probability sample 40 years newer, much richer early-known features; ...
