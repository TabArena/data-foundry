---
unique_name: higher_education_students_performance_evaluation
name: Higher Education Students Performance Evaluation (UCI 856)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: UCI
year: '2019'
domain: education
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C51G82
- https://archive.ics.uci.edu/dataset/856/higher+education+students+performance+evaluation
- https://doi.org/10.1007/978-3-030-35249-3_76
- http://arxiv.org/abs/2609.29625
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a 2019 questionnaire of 145 engineering and educational-sciences students with their end-of-term course grade in eight levels (UCI 856); documented and in a thin domain, but tiny, with 8 failing students in all and the rows spread over nine courses.
- Source: Yılmaz and Şekeroğlu, "Student Performance Classification Using Artificial Intelligence Techniques", Advances in Intelligent Systems and Computing 1095 (2019), https://doi.org/10.1007/978-3-030-35249-3_76 (paywalled, not read); UCI 856 (donated 2023-08-14, CC BY 4.0, https://doi.org/10.24432/C51G82): "The data was collected from the Faculty of Engineering and Faculty of Educational Sciences students in 2019", and "The purpose is to predict students' end-of-term performances using ML techniques". As published (preview of the 11 kB CSV): 145 rows x 33 columns: a student id, 30 integer-coded answers numbered 1 to 30 (personal and family background, study habits, attendance, last-semester GPA, expected GPA at graduation; the codes are on the UCI page), COURSE ID and GRADE (0 Fail, 1 DD, 2 DC, 3 CC, 4 CB, 5 BB, 6 BA, 7 AA). Counted in the preview: grades 0 to 7 have 8, 35, 24, 21, 10, 17, 13 and 17 students; courses 1 to 9 have 66, 2, 8, 4, 7, 8, 15, 14 and 21.
- Use case: an instructor or advisor finding the students likely to fail a course, to offer support; UCI and the paper name the prediction, not the actor; fit approximate (when the questionnaire was answered relative to the course is not stated, and the expected GPA is the student's own guess). Regime: one row per student; the use case predicts for new students of the same courses, so IID with the course as a feature (SPLIT-1, to decide); the audit paper's group holdout by course (arXiv 2609.29625: R² 0.041 under a random split, -8.79 under group holdout) tests transfer to unseen courses, which no actor here needs.
- Siblings and duplicates: no other record of this survey; `student_portuguese_performance` (`Yes`, Portuguese secondary students, final grade) and `open_university_learning_analytics_dataset` (`Yes`) are larger tasks of the same kind; `predict_students_dropout_and_academic_success` predicts dropout. External collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (item 291, arXiv 2609.29625); no search for better data in this run.
- Papers and pages: Yılmaz and Şekeroğlu 2019; Ma and Zhang, "Limited Structural Reliability in Public Educational Prediction Benchmarks" (arXiv 2609.29625, 2026, abstract read).
- Metric: none found (the paper is paywalled; the UCI page names none; the audit paper scores R² on the grade as a number), so the fallback `log_loss` for the eight grades, or `rmse` on the grade as an ordered number (MET-1, MET-8).
- Risks for /add-dataset: `Too Small` as published: 8 failing students in all, under 2 per test fold at five folds; merge grade levels or score the grade as a number (TP-5, TP-8); the questionnaire's timing against the course; the course as a feature or a group; 145 rows (`Tiny Data`).
- Priority: gap + (education is thin), use case 0 (no actor named), source + (UCI page with a codebook and a paper), shape 0 (145 rows), risk - (grade classes too small as published).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 291: "Limited Structural Reliability in Public Educational Prediction Benchmarks: A ...".
- as published: students: 145 rows x 31 integer-coded questionnaire answers (age, sex, family, study habits, attendance, last-semester and expected GPA) + OUTPUT Grade; engineering and educational sciences ...; target: end-of-term course grade, 8 ordered levels (fail to AA); access: open.
- Why: Real, documented UCI dataset with an intro paper; not recorded.
- Adds: Very small (145 rows), and course-grouped holdout collapses in the audit (R2 -8.79). Listed for completeness; likely Tiny Data and low priority.
