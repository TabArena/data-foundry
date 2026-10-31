---
unique_name: nhanes_cvd_mortality
name: NHANES III and NHANES 1999-2010 baseline risk factors linked to the NCHS public-use Linked Mortality Files (10-year cardiovascular death)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.cdc.gov/nchs/data-linkage/mortality-public.htm
- https://wwwn.cdc.gov/nchs/nhanes/nhanes3/datafiles.aspx
- https://wwwn.cdc.gov/nchs/nhanes/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 10-year cardiovascular death from NHANES III and 1999-2008 baseline exams linked to the NCHS public-use mortality files; a national sample with the risk-factor features of `framingham_heart_study_fhs`, but NCHS replaced the follow-up time or the cause of death of some records with synthetic values.
- Source: CDC/NCHS NHANES public-use files with the NCHS-NDI Linked Mortality Files ("2019 public-use" files for NHANES III, NHANES 1999-2018 and 2017-March 2020; the newer linkage through 2022-12-31 is restricted). The data-linkage page: "For certain records, the follow-up time or underlying cause of death were substituted with synthetic values"; "Information about whether a person is alive or dead was not changed"; "Data were not altered for the restricted-use files". The page does not list the variables (mortality status, months of follow-up and the leading underlying cause are the scout's recollection). Rows not counted (several tens of thousands of adults across NHANES III and 1999-2008 expected).
- Use case: a primary-care clinician estimates a patient's 10-year cardiovascular risk at a check-up to decide on statins or blood-pressure treatment; the target is fatal CVD (the SCORE endpoint), narrower than the fatal and nonfatal events the decision weighs, so the fit is approximate; regime temporal by baseline cycle (test on the latest cycles with 10 years of follow-up).
- Siblings and duplicates: `framingham_heart_study_fhs` (`Yes`, perturbed BioLINCC teaching data, the PROV-3 owner-perturbation precedent), `cardiovascular_disease_dataset` (`No`), `aric_incident_chd` (`TBD -> Yes`, 3, request access), `nhanes_iii_gallstones` (the same NHANES III exam for another task, PROV-7), `chicago_nmmaps_cvd_mortality` (daily city death counts, another task). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `cardiovascular_disease_dataset` and `framingham_heart_study_fhs`; no further search this round.
- Papers and pages: the NCHS data-linkage page and the NHANES III data files page; no paper that defines this task on NHANES was looked up (search unavailable).
- Metric: none found (no source defines the task), so the fallback `roc_auc` on the binary 10-year label (MET-8); inputs none, but the label needs a rule for people censored alive before 10 years and for deaths from other causes (USE-3).
- Risks for /add-dataset: the synthetic follow-up time or cause of some records is owner perturbation (PROV-3, framingham precedent): keep with a note of what was checked and what cannot be; only baselines up to about 2009 have 10 possible years of follow-up to 2019; harmonising NHANES III with continuous NHANES (lipids, blood pressure, treatment questions); only baseline items are features (LEAK-10); heavy joins; survey weights not used.
- Priority: gap 0, use case 0 (a real decision, but no source names it for this data), source + (NCHS documentation), shape + (tens of thousands of adults, mixed features, cycles), risk - (synthetic values in the public linkage, a constructed censored label).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cardiovascular_disease_dataset`, `framingham_heart_study_fhs`.
- as published: One row per adult. NHANES III and the 1999-2010 cycles give several tens of thousands of adults with 10 or more years of possible follow-up (my estimate from the cycle sizes, not counted). The LMF ...; target: cardiovascular death (heart disease or cerebrovascular underlying cause) within 10 years of the exam: the European SCORE endpoint, narrower than the record's ...; access: open.
- Why: Same use case and the same risk-factor features as framingham_heart_study_fhs: age, sex, systolic BP and treatment, total and HDL cholesterol, smoking, diabetes, BMI. The endpoint is the fatal part of the record's outcome, so this is not the same quantity but a published variant of it (SCORE). | The cardio table is ...
- Adds: Several times the 4,199 rows. A national probability sample instead of a teaching subset of one 1948 town cohort with undocumented selection and anonymisation. Risk-factor levels and treatment from 1988-2010 instead of about 1956, i.e. the statin era the record's fit_reason says is missing. Caveat (PROV-3): the ...
