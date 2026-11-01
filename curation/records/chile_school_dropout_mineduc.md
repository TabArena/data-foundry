---
unique_name: chile_school_dropout_mineduc
name: 'Chile Mineduc open data: Rendimiento por estudiante (student final academic status), for school dropout prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: education
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/
- https://doi.org/10.1007/s10639-022-11515-5
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9869310/
- https://www.mineduc.cl/?p=22673
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: a national school-dropout task from the open data of Chile's Ministry of Education (every student each year with final status, attendance and grade average under a pseudonymised id), the data behind a published early-warning methodology with a temporal split; the label must be built by linking yearly files, and the portal was out of service when checked.
- Source: Centro de Estudios, Ministerio de Educación de Chile (Mineduc), open data "Rendimiento por estudiante", one file per school year (2002-2025 per the scout, .rar archives). The portal answered "Este sitio se encuentra temporalmente fuera de servicio" on 2026-10-31, and mineduc.cl refused the connection, so files, columns and row counts were not seen. As the scout describes them: per student the final status, attendance, grade average, school (RBD), grade and a pseudonymised id (MRUN). The year waits for the files we pin (PROV-9).
- Use case: an early-warning system flags students at risk of leaving school so that schools and local services intervene; Rodríguez, Villanueva, Dombrovskaia, Valenzuela, "A methodology to design, develop, and evaluate machine learning models for predicting dropout in school systems: the case of Chile", Education and Information Technologies, 2023 (doi 10.1007/s10639-022-11515-5; read through Europe PMC), build a model that estimates each student's risk of leaving school for Early Warning Systems and policy decisions. Mineduc's own Sistema de Alerta Temprana (the scout's note) was not verified. Fit approximate: the paper adds internal enrollment variables "provided within NDA agreement" (Table 1), so the open files carry fewer inputs. Regime temporal: the paper trains on trajectories up to 2018 and tests on trajectories reaching 2019 with dropout observed in 2020 ("There is no intersection between training and test samples"); schools as groups inside.
- Siblings and duplicates: `predict_students_dropout_and_academic_success` (`Yes`, university dropout in Portugal), `upv_university_student_dropout`, `xuetangx_mooc_dropout`, `hsls09_postsecondary_enrollment` (`TBD -> Yes`, 4): other populations and tasks, no duplicate (searched Mineduc, Chile, dropout). External collections: none found.
- Better data: from the gap scout for education; no further search this round.
- Papers and pages: Rodríguez et al. 2023 (Secs. 2 and 3: 3,847,469 student trajectories; dropout is a student enrolled in a grade for children and youth in year t who is "either enrolled in adult education or out of the school system on year" t+1; a test set of 2,802,156 trajectories with 1.7% dropouts).
- Metric: the paper targets the geometric mean of sensitivity and specificity and the F1 of the dropout class, threshold metrics with no threshold or cost fixed (MET-6), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the label needs the next year's files linked on the student id (whether MRUN is stable across years and files, to verify), with graduates, deaths and emigrants kept apart from dropouts (USE-5); a final status of year t that records a withdrawal during the year is an outcome of that year (decide the prediction point, LEAK); millions of rows per year (cut years or grades); the files were not previewed (`Needs extensive data wrangling`); pseudonymised ids only, no names.
- Priority: gap + (education has three accepted datasets), use case + (a published early-warning methodology on this data), source + (the ministry's open data and a paper), shape + (national cohorts, temporal, schools), risk - (a label to build by linking years, files unseen).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for education.
- as published: every student of the Chilean school system each year (Rodríguez et al. 2023 score 2.8 million students); per-student final status, attendance and GPA with school, grade and pseudonymised student id; ...; target: dropout: a student enrolled in year t who is neither enrolled nor graduated in year t+1 (built by linking yearly files on the pseudonymised id); access: open (the paper's richer internal enrollment file was under NDA and is not public; the open files lack some of its variables).
- Why: an official national source, an early-warning system in use, a dropout label one year after the features, and many cohorts for a temporal split
- Adds: a national, very large school (K-12) dropout task, temporal and grouped by school, next to the university dropout of predict_students_dropout_and_academic_success
