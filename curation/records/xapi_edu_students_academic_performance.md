---
unique_name: xapi_edu_students_academic_performance
name: Students' Academic Performance Dataset (xAPI-Edu-Data, Kalboard 360 LMS)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Tiny Data
original_source: Kaggle
year: '2016'
domain: education
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data
- https://doi.org/10.14257/ijdta.2016.9.8.13
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 480 school students of the Kalboard 360 LMS (mostly Kuwait and Jordan, two semesters, 12 subjects) with demographics, LMS activity counts and absence, and the band of the total grade (L, M, H) as the target; a documented but tiny education task whose activity features may be counted up to the grade.
- Source: Amrieh, Hamtini and Aljarah (University of Jordan); the data on Kaggle aljarah/xAPI-Edu-Data (card "Date: 2016-11-8", CC BY-SA 4.0), described in Amrieh et al., "Mining Educational Data to Predict Student's academic Performance using Ensemble Methods", IJDTA 9(8):119-136, 2016 (doi 10.14257/ijdta.2016.9.8.13, read). An earlier cut was used in Amrieh et al., IEEE AEECT 2015 (not read): Sec. 3, p. 124: "The educational data set that used in the previous work [10] contains only 150 student's records with 11 features. In the current paper that data set extends into 500 students with 16 features"; the file and the paper's class counts (Sec. 4, p. 129: "127 students with Low Level, 211 students with Middle Level and 142 students with High Level") hold 480. As published (previewed): 480 rows x 17 columns: gender, nationality, place of birth, stage, grade (G-01 to G-12), section, topic, semester, the parent responsible, `raisedhands`, `VisITedResources`, `AnnouncementsView`, `Discussion` (counts from 0 to 100), parent answered survey, parent school satisfaction, absence days (above or under 7) and `Class`; no missing values; 2 duplicated rows. The bands: "Low Level interval includes values from 0 to 69, Middle Level interval includes values from 70 to 89 and High Level interval includes values from 90-100" (Sec. 4, p. 129).
- Use case: a school or a teacher, during the semester, flags the students heading for a low band so they can intervene; the paper: "this model can help educators to understand learners, identify weak learners, to improve learning process and trimming down academic failure rates" (Sec. 6, p. 134). Fit approximate: the activity counts and absence days look like totals of the semester, not stated to be taken before the grade, and the paper's aim is to show that behavioural features matter. Regime IID over students: the paper uses 10-fold cross-validation and validates on "25 new comer students" (Sec. 5.3, p. 133); there is no student id, so whether a student appears in both semesters cannot be checked. A topic-grouped holdout (12 topics of 19 to 95 rows) is the audit's variant.
- Siblings and duplicates: no other record holds this data (grep by xAPI, Kalboard, aljarah). Education records: `open_university_learning_analytics_dataset` (Yes, OULAD), `predict_students_dropout_and_academic_success` (Yes), `student_portuguese_performance` (Yes, Tiny Data), `higher_education_students_performance_evaluation` (no verdict), `student_performance_on_an_entrance_examination` (TBD -> Yes); OULAD, Dropout, UCI Student, Higher Ed and Entrance Exam are also in the audit below. External collections: the audit of seven public education datasets by Ma and Zhang (arXiv 2609.29625, 2026; HTML read): "xAPI-Edu (Strong) passes all four dimensions" (Sec. 3.2), with group-holdout R2 0.484 against IID 0.614 over 12 topics.
- Better data: from the curator's Zotero collection (item 291); no further search this round.
- Papers and pages: Amrieh et al. 2016 (IJDTA; ANN, naive Bayes, decision trees, bagging, boosting and random forests in WEKA); Amrieh et al. 2015 (AEECT, the 150-student cut); Ma and Zhang 2026, "Limited Structural Reliability in Public Educational Prediction Benchmarks" (http://arxiv.org/abs/2609.29625).
- Metric: the paper uses "four common different measures for the evaluation of the classification quality: Accuracy, Precision, Recall and F-Measure" (Sec. 5.2, p. 131), side by side without naming the one that decides: no unique original (MET-5), so the fallback `log_loss` on the three bands. The audit scores the bands as 0/1/2 by regression, a choice of its own. Inputs none.
- Risks for /add-dataset: when the counts and the absence days are measured relative to the grade (USE-3; absence alone separates much: 116 of the 127 L students have more than 7 absence days, 4 of the 142 H students); 500 students in the paper's text against 480 in the file; the counts run from 0 to 100 without a stated scale (raw counts or rescaled); the target is a band of a total grade that is not published (USE-5); nationality and gender as inputs; tiny, but TP-5 holds with 127 rows in the smallest class.
- Priority: gap + (education is thin; multiclass is thin), use case 0 (the paper names educators, not the moment; the fit is approximate), source + (two papers by the collectors and a full data card), shape 0 (480 students).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 291: "Limited Structural Reliability in Public Educational Prediction Benchmarks: A ...".
- as published: students: 480 rows x 16 features + Class, two semesters (245 + 235), 12 course topics, grades G-01 to G-12, mostly Kuwait and Jordan; no missing values; CC BY-SA 4.0; target: Class: the student's total-grade band, L (0-69), M (70-89) or H (90-100), ordinal 3-class; access: open.
- Why: Real LMS activity data with a source paper and a grade target. The audit counts it as one of the three datasets that survive topic-grouped holdout.
- Adds: A K-12 LMS-behaviour task next to OULAD (online university). Tiny (480 rows). A topic-grouped split is possible. Not stated: whether the activity counts are measured up to the grade (end-of-semester totals) or at a mid-term prediction point.
