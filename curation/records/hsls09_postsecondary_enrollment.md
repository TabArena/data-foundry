---
unique_name: hsls09_postsecondary_enrollment
name: High School Longitudinal Study of 2009 (HSLS:09), base year to second follow-up public-use file
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: 23,503 students in the public-use file x 1,020 public items gathered in 9th grade (2,007 through the 11th-grade follow-up), far wider than the screening's "hundreds"; the outcome `X6PSE` (ever enrolled in postsecondary education by June 2021, from administrative records) ships in the public file, the school id does not; the call stands, priority 4.
- As published: the NCES HSLS:09 variable list (https://nces.ed.gov/surveys/hsls09/xls/HSLS09_VariableList_rev01-24.xlsx, read 2026-11-08): 9,721 student-level variables, 8,796 of them in the public-use file (PUF) and 925 in the restricted-use file only; 5,632 of the 8,796 are weights (analytic and BRR replicate weights). Waves: base year (fall 2009, 9th grade), first follow-up (2012), 2013 update, high school transcripts (2013-14), second follow-up (2016), postsecondary transcripts and records (2016-17), and the PEAR update (`X6*`: enrollment, federal aid and loans as of June 2021). ICPSR's record of the 2009-2013 PUF counts "23,503 students from more than 900 public and private high schools". The PUF is downloaded through the NCES DataLab online codebook; a DataLumos mirror lists `hsls_17_student_pets_sr_v1_0.csv` at about 847 MB (search result; the page refused access).
- The task's table: one row per student, target `X6PSE` ("Ever enrolled in postsecondary education, as of June 2021 (two categories)") or `X4EVRATNDCLG` (the 2016 survey answer, imputed). Inputs known at the end of 9th grade (base-year PUF items without weights and imputation flags): 1,020, from the student questionnaire 271, student composites 112, parent 142, math teacher 134, science teacher 157, counselor 150, administrator 54; 147 of them altered on the PUF (sparse values recoded, categories merged). The 11th-grade follow-up adds 987 (student 408, composites 108, parent 203, counselor 175, administrator 93; 141 altered). The counselor and administrator items describe the school and repeat for its students; teacher items exist only for students in that teacher's course. Counted from the variable list; the rows with a known target are not counted.
- Access: public-use file free for immediate download, no login; the restricted-use file (school ids, unaltered values) needs an NCES licence; data.gov lists the study under CC0 (screening).
- Changes the call: the school id is suppressed on the PUF (`SCH_ID`: "Variable suppressed with -5 values on the public use file"), so the screening's grouped-by-school regime needs the restricted-use file; on the PUF the split is IID unless a key is rebuilt from the repeated school items (SPLIT-26 asks for the source's own key; not attempted). The PEAR outcome comes from records, not from the 2016 survey, and may cover more of the sample than the 2016 respondents (not checked). The wave cut stays the main build decision (LEAK-10): the transcript composites (`X3T*`, 139 PUF items) were compiled in 2013-14 and cover grades 9 to 12. Sibling: `hsls09_secondary_student_achievement` uses the same PUF. Priority 4 stands.
- Not checked: the PUF itself (size, rows with `X6PSE` known, missing-value codes); the PEAR coverage; which outcome He et al. 2025 used.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).
