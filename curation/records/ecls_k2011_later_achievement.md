---
unique_name: ecls_k2011_later_achievement
name: Early Childhood Longitudinal Study, Kindergarten Class of 2010-11 (ECLS-K:2011), K-5 public-use file
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- Many features
original_source: GOV Website
year: '2019'
domain: education
problem_type: Regression
original_data_state: One Table
source_links:
- https://nces.ed.gov/ecls/dataproducts.asp
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 3: NCES's national cohort of 18,174 kindergartners of 2010-11 followed to fifth grade (spring 2016), about 26,100 variables in one public file; a later reading or mathematics score predicted from the kindergarten-year child assessments, parent interviews and teacher and school reports; no source names a predictive use, and the kindergarten-round columns have to be cut from nine rounds.
- Source: National Center for Education Statistics, Early Childhood Longitudinal Study, Kindergarten Class of 2010-11 (ECLS-K:2011), Kindergarten-Fifth Grade Public-Use File (NCES 2019-050; user's manual NCES 2019-051), nces.ed.gov/ecls/dataproducts.asp. As published: one ASCII file `childK5p.dat` (ChildK5p.zip, 460 MB) with SPSS, SAS and Stata setup files and an electronic codebook, for "18,174 children who participated, or whose parent participated, in at least one of the two kindergarten data collections"; the setup files build all variables of the complete public-use file, "approximately 26,100"; nine rounds from fall 2010 to spring 2016 (direct reading, mathematics and science assessments, executive function, parent, teacher and school administrator questionnaires); about 11,450 children took part in the spring fifth-grade round (NCES study pages).
- The task's table: one row per child with a later score, about 11,450 children for grade 5 x the kindergarten-round variables (fall and spring 2010-11, a subset of the 26,100, to count at build), target the grade-3 or grade-5 reading or mathematics score; download public, no registration.
- Use case: for example, a school district at the end of kindergarten flags children likely to score low in grade 3 or 5 for early reading or mathematics support; NCES releases the study for research and names no prediction, so fit approximate. Regime: grouped by kindergarten school if the public file keeps a school id (to check), otherwise IID over children.
- Siblings and duplicates: `hsls09_secondary_student_achievement` (`TBD -> Yes`, 3), `hsls09_postsecondary_enrollment` (`TBD -> Yes`, 4) and `els2002_bachelors_attainment` (`TBD -> Yes`, 4): other NCES cohorts and tasks (PROV-7); `early_learning_predictors` (`Yes`, a Zindi task on early learning outcomes at age five) and `student_portuguese_performance` (`Yes`): other sources. grep: ecls, early childhood, kindergarten, nces. External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the data products page; the user's manual NCES 2019-051 (not read in this pass).
- Metric: none found (NCES publishes the study for research, with no predictive task; looked at the data products page), so the fallback `rmse`.
- Risks for /add-dataset: choose the outcome (grade-3 or grade-5 score) and keep only kindergarten-round inputs (the variable prefixes give the round); composite variables that NCES revised in later rounds must enter in their kindergarten version (LEAK-10); attrition from 18,174 to about 11,450 (the label exists only for children still followed: a note, no marker); sampling weights never enter the features (MET-16); public-use masking (restricted-only variables shown as -2); schools are sampling units.
- Priority: gap + (education thin), use case 0 (ours, fit approximate), source + (NCES with codebook and manual), shape + (about 11,450 children x thousands of mixed items, schools), risk - (the round cut and the composites to check).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).
