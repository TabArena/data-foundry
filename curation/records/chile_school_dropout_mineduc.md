---
unique_name: chile_school_dropout_mineduc
name: 'Chile Mineduc open data: Rendimiento por estudiante (student final academic status), for school dropout prediction'
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
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
v2_path: datasets/_dev/tabarena-v0pt2/chile_school_dropout_mineduc_1m/dataset.py
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

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: one row per non-graduating student of a children's or youth programme in year t, labelled from the next year's file, gives 2,829,401 students x about 24 inputs for 2023 to 2024 (90,096 dropouts, 3.18%); the call stands (priority 4).
- As published: the portal answers again (https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/, read 2026-11-08): 24 yearly RAR files, 2002 to 2025, each with one semicolon-delimited UTF-8 CSV, the record layout ("Esquema de registro bases de Rendimiento escolar 2002-2024 por estudiante", Centro de Estudios) and a frequency workbook. The layout states the rows per school year: 3,568,930 (2024), 3,584,330 (2023), 3,405,130 (2022), 3,164,534 (2020, the lowest), 3,376,045 (2002); for 2002-2014 it gives only the students of schools in operation. The 2023 and 2024 files, downloaded here, hold 3,584,330 x 37 and 3,568,930 x 38 columns (2024 adds NOMBRE_SLEP), the stated counts. A row is a student in a school and course: 3,356,854 distinct MRUN in 2023. Sources: RECH for 2002-2008, SIGE from 2009. Special education enters the files in 2023 (layout, footnote 4), a break in the series; two non-binary students were removed from 2024 for privacy (footnote 3).
- The task's table: two consecutive years joined on MRUN, and the pseudonymised id links. In 2023, 3,043,649 students have a row in a children's or youth programme (COD_ENSE2 2, 5, 7); without the 214,248 promoted from 4th year of secondary, 2,829,401 remain. Of these, 72,174 are absent from the 2024 file and 17,922 appear in 2024 only in adult education: 90,096 dropouts (3.18%) under the paper's definition (Rodríguez et al. 2023, Sec. 3: a student enrolled in some grade for children and youth in t "is either enrolled in adult education or out of the school system on year t + 1"). Computed on the two files, one row per student. 180,624 of these students have more than one row in 2023 (transfers), so a build needs a rule to pick or merge them; a transfer row is coded SIT_FIN = Y (withdrawn) with SIT_FIN_R = T (227,148 rows), so only SIT_FIN_R tells a transfer from a withdrawal. Inputs from year t's file: about 24 after dropping ids, names and grouped duplicates (school region, province, commune, provincial department, dependency, rurality, SLEP; teaching code, grade, shift, course type, TP description, branch, sector, specialty, mención; sex, birth month, residence region and commune; GPA, attendance, final status, final status with transfer). Earlier years linked on MRUN add history (repetitions, school changes, past GPA and attendance). The 23 transitions from 2002/03 to 2024/25 give about 65 million student-years (an estimate); one or a few transitions suffice.
- Access: open, no login; 24 RAR files of 37.3 to 48.0 MB (1,057,259,066 bytes in all), each CSV about 600 MB unpacked (2023: 598,707,057 bytes); RAR needs an unrar tool. The collection page states no licence.
- Changes the call: no new reject; two facts for the curator. (1) The open-file label is noisier than the paper's. The paper removed deaths and graduations by other routes with MINEDUC's own lists (Table 1: "Deceased students"; "School graduates": "Students who completed compulsory education each year, either by regular or alternative means") and reports 1.7% dropouts for 2019 to 2020 (2,802,156 trajectories). The open files cannot tell a death, an emigrant or an exam-route graduate from a dropout, which likely explains part of the gap to 3.18% (USE-5). (2) Year t's final status carries much of the label: the 45,941 students withdrawn in 2023 (a row with SIT_FIN_R = Y and no promoted or failed row) hold 33,263 of the 90,096 dropouts (72.4% of them drop out, against 1.7% of the promoted and 19.1% of those who failed the year). The prediction point decides whether year t's final status, GPA and attendance are inputs: yes for an early warning at the end of the school year, lagged one year for a warning at its start (LEAK). Priority kept at 4.
- Not checked: the files of 2002-2022 and 2025 (their rows are the layout's stated counts); whether MINEDUC publishes the deceased and graduates lists openly; the MRUN linkage before 2023.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: students whose masked id changed between two yearly files are re-linked to their new id by school, sex, birth month, home commune and grade and relabelled "No", 10-19% of each year's dropouts, 10-26% of the links wrong by a placebo test, USE-5 fixed in the definition; the notes, the metric reason and the cleaning fixes); disputed: USE-5 (re-link or note; settled for the re-link), USE-1/USE-5 (all grades or grades 7-12; open), CLEAN-21 and CLEAN-12 (settled); for the curator: issues 1-3. Priority 2: gap -, use case - (fit approximate: the ministry's list covers grades 7-12 and the label keeps emigration and deaths), source + (Mineduc's census files with a codebook, and a paper), shape + (19.4M student-years, temporal, mixed types), risk - (a label repaired by a record link of our own with a measured share of wrong links; residual label noise).
