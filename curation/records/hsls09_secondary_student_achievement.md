---
unique_name: hsls09_secondary_student_achievement
name: High School Longitudinal Study of 2009 (HSLS:09), public-use files
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: education
problem_type: Regression
source_links:
- https://nces.ed.gov/surveys/hsls09/
- https://nces.ed.gov/surveys/hsls09/hsls09_data.asp
- https://nces.ed.gov/datalab/onlinecodebook
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the same NCES HSLS:09 cohort (23,000+ ninth graders, 944 schools) with a later achievement outcome, the 11th-grade math assessment or the transcript GPA, predicted from 9th-grade student, family and school features; the target is still to choose and no source names a predictive use.
- Source: as `hsls09_postsecondary_enrollment`: NCES HSLS:09, "Nationally representative, longitudinal study of 23,000+ 9th graders from 944 schools in 2009", with "A new student assessment in algebraic skills, reasoning, and problem solving for 9th and 11th grades" and high school transcripts of 2013-14 (nces.ed.gov/surveys/hsls09); public-use files through the NCES DataLab online codebook, restricted-use files under licence.
- Use case: a school counselor in 9th grade flags students likely to end with a low 11th-grade score or low grades, to target tutoring or support; the framing is the run's and is not stated on the NCES pages read, so fit approximate. Regime grouped by school (944 schools).
- Siblings and duplicates: `hsls09_postsecondary_enrollment` (the same file with an enrollment target; a distinct task, PROV-7: the curator may take one or both); `student_portuguese_performance` (`Yes`, shipped in BeyondArena: G3 of 649 students of two Portuguese schools, with the open doubt about features measured at the time of the grade); `exam_score_prediction_dataset` (`No`, AHDS: "This dataset is entirely synthetically generated"); `els2002_bachelors_attainment` (the earlier NCES cohort). External collections: none found.
- Better data: found as better data for `exam_score_prediction_dataset` and `student_portuguese_performance`; no further search this round.
- Papers and pages: the NCES study and data pages; the HSLS:09 FAQ (Appendix L for the public-use alterations); He et al. 2025 (BDCC 9(4):99) uses the same file, with the transcript GPA as a predictor of enrollment.
- Metric: none found (NCES pages; no study read scores a prediction of the 11th-grade score or the GPA), so the regression fallback `rmse` (MET-8). Inputs none.
- Risks for /add-dataset: the target to choose: the 11th-grade math score of the 2012 follow-up, or the transcript GPA (whether it is in the public-use file is to check in the variable list); the 9th-grade math score is a strong feature, so the task may reduce to score persistence (TP-4 to probe); every 2012-or-later variable must go (LEAK); public-use alterations and imputed composites (Appendix L); the school id for the grouped split.
- Priority: gap + (education has three accepted datasets), use case 0 (no source names the decision), source + (NCES with codebook and documentation), shape + (23,000+ students, mixed features, grouped by school), risk - (a target still to pick, and later-wave columns to exclude).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `exam_score_prediction_dataset`, `student_portuguese_performance`.
- as published: 23,000+ 9th graders from 944 schools (NCES page); one row per student with student, parent, teacher, counselor and school questionnaires; public-use file downloadable from NCES DataLab, ...; target: a secondary-school achievement outcome: the 11th-grade mathematics assessment score of the 2012 follow-up, or the transcript GPA (which transcript composites ...; access: open.
- Why: same task as Cortez and Silva (2008): predict a secondary student's later achievement from demographic, family, study-habit and school features known earlier (study time, parents' education and jobs, past performance, absences) | the synthetic record predicts an exam score from study habits, attendance, internet ...
- Adds: about 23,000 students from 944 schools in a national probability sample instead of 649 students from two Portuguese schools in 2005-06; a later measurement wave as the target, so the features clearly precede it (the Portuguese record's open doubt about features measured at the same time as G3); schools give a grouped ...
