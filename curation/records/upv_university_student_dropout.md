---
unique_name: upv_university_student_dropout
name: 'University Student Dropout: A Longitudinal Dataset of Demographic, Socioeconomic, and Academic Indicators'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Other
year: '2025'
domain: education
problem_type: Binary Classification
source_links:
- https://doi.org/10.3390/data10100162
- https://doi.org/10.5281/zenodo.17239943
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 39,364 students of a Spanish technological university (the Universitat Politècnica de València team) over three academic years (files 2018, 2021, 2022), one row per course enrolment with admission, socio-economic and academic data plus monthly LMS and Wi-Fi activity; a large, recent dropout task, with the unit, a coded label and same-year columns to settle.
- Source: Igualde-Sáez, Maheut, Garcia-Sabater, Marin-Garcia, Turro, Despujol Zabala, Puche Garcia, Alonso, Benlloch-Dualde and Soriano Jiménez (Universitat Politècnica de València), "University Student Dropout: A Longitudinal Dataset of Demographic, Socioeconomic, and Academic Indicators", Data 10(10):162, 2025 (doi 10.3390/data10100162); Zenodo "StudentDropoutDataset" (doi 10.5281/zenodo.17239943, 2025-10-01, CC BY 4.0): `dataset_2018_hash.zip`, `dataset_2021_hash.zip`, `dataset_2022_hash.zip`. Zenodo: "The dataset comprises 39,364 students, 4,989 courses across 163 degree programmes, and 77 variables"; "With 464,739 individual records—each representing a course enrolment per student per academic year"; "spanning three complete academic years (excluding pandemic-affected periods)". Preview of the 2022 file (semicolon CSV, 169 columns, 91.7 MB unpacked): hashed ids `dni_hash`, `tit_hash`, `asi_hash`; admission `anyo_ingreso`, `tipo_ingreso`, `nota10_hash`, `nota14_hash`, `preferencia_seleccion`; parents' studies `estudios_p_hash`, `estudios_m_hash`; `dedicacion`; `desplazado_hash`; the label candidate `abandono_hash` (letter codes, `B` in the preview); `baja_fecha` (a withdrawal date); credits enrolled and passed, performance per term, the course grade `nota_asig_hash`; monthly LMS (`pft_*`) and Wi-Fi (`n_wifi_days_*`) counts from September 2022 to the following summer; `fecha_datos` 2023-11-20.
- Use case: student services flag students at risk of leaving, to offer tutoring or support; Zenodo names "developing predictive models to identify at-risk students", with no actor or moment; fit approximate until the prediction point is fixed; regime temporal (academic years) or grouped by student (students recur across years), to decide (USE-10).
- Siblings and duplicates: `predict_students_dropout_and_academic_success` (`Yes`: 4,424 students of a Portuguese polytechnic, 2021); `open_university_learning_analytics_dataset` (`Yes`, online course outcomes); `chile_school_dropout_mineduc`, `xuetangx_mooc_dropout`, `hsls09_postsecondary_enrollment` (unscreened; school, MOOC and survey populations). No duplicate. External collections: none found.
- Better data: found as better data for `predict_students_dropout_and_academic_success` (the run's Assessment); no further search this round.
- Papers and pages: the data paper (not read: MDPI answered 403; abstract via Semantic Scholar); the Zenodo record.
- Metric: none found (Zenodo and the abstract name none; the paper not read), so the fallback `roc_auc` (MET-1, MET-8).
- Risks for /add-dataset: rows are course enrolments, so the unit (student and year) and the label must be built (`Needs extensive data wrangling`); `abandono_hash` and the other `_hash` category values are letter codes whose meaning needs the paper's codebook (without one, `Anonymized`); `baja_fecha`, the year's grades, credits passed and late-year activity are known only at or after the outcome, so the prediction point (enrolment, end of the first term) decides which columns stay (USE-3, LEAK); the 2022 file has 169 columns against the 77 variables named, so the monthly columns differ by year; three non-consecutive years for a temporal split.
- Not checked: the paper's text (the dropout definition, the codebook, the class balance); the 2018 and 2021 files (only the 2022 header was previewed).
- Priority: gap + (education is thin, 3 accepted), use case 0 (named as a reuse, no actor or moment), source + (data paper, Zenodo, the university's team), shape + (39,364 students, mixed types, three years), risk - (unit, coded label and same-year columns to settle).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `predict_students_dropout_and_academic_success`.
- as published: 39,364 students, 4,989 courses in 163 degrees; 464,739 records (one per course enrolment per student per academic year); 77 variables; three academic years (files 2018, 2021, 2022; pandemic years ...; target: student dropout (leaving the programme), built from the longitudinal enrolment records; access: open.
- Why: same task as predict_students_dropout_and_academic_success: dropout of higher-education students from admission, socio-economic and academic-performance data, known during the studies
- Adds: about nine times the students (39,364 vs 4,424), newer years (to 2022), bachelor to doctoral programmes, and features the old record lacks (LMS activity, Wi-Fi access patterns, per-course grades); screening must fix the unit (student-year) and the dropout label, since the rows are course enrolments
