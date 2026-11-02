---
unique_name: aric_incident_chd
name: Atherosclerosis Risk in Communities Study (ARIC), NHLBI BioLINCC
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://biolincc.nhlbi.nih.gov/studies/aric/
- https://doi.org/10.1093/oxfordjournals.aje.a115184
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a prospective NHLBI cohort of 15,792 adults aged 45-64 at entry (1987-89) with adjudicated CHD events through 2023, the cohort behind a published CHD risk function; access by request only, and the task has to be derived from many tables.
- Source: Atherosclerosis Risk in Communities Study (NHLBI); design paper The ARIC Investigators, Am J Epidemiol 129(4):687-702, 1989 (doi 10.1093/oxfordjournals.aje.a115184); data through NHLBI BioLINCC (biolincc.nhlbi.nih.gov/studies/aric/): black and white men and women aged 45-64 at entry, 15,792 from four communities; "examination cycles v1-v10, annual follow-up contact data for contact years 2-35, and mortality, heart disease, and stroke follow-up through 2023"; a data dictionary of 11 MB; "The data cannot be used for commercial purposes." Many tables (exam forms, event and follow-up files).
- Use case: a GP estimates a patient's 10-year CHD risk at a check-up from blood pressure, lipids, smoking, diabetes and family history, to decide on statins or blood-pressure treatment; the ARIC investigators built such a function, Chambless et al., "Coronary heart disease risk prediction in the Atherosclerosis Risk in Communities (ARIC) study", J Clin Epidemiol 56(9):880-890, 2003 (bibliographic record checked, text not opened); fit direct; regime IID by participant (one baseline exam per person, 1987-89).
- Siblings and duplicates: `south_africa_coronary_heart_disease` (`Yes`, a retrospective CORIS case-control sample), `framingham_heart_study_fhs` (`Yes`, BioLINCC teaching data with perturbed values), `heart_disease` (`Yes`, angiography result), `cardiovascular_disease_dataset` (`No`), `smart_vascular_events` and `nhanes_cvd_mortality` (unscreened): other cohorts, no duplicate. External collections: none found.
- Better data: found as better data for `south_africa_coronary_heart_disease`; no further search this round.
- Papers and pages: the 1989 design paper; Chambless et al. 2003; the BioLINCC study page and its data dictionary.
- Metric: Chambless et al. 2003 not opened, so its criterion is unknown; the fallback `roc_auc` (MET-8) unless the paper ranks by one; inputs none, but a 10-year label needs a rule for participants censored or dead of other causes before 10 years (USE-3).
- Risks for /add-dataset: a BioLINCC request (registration and a request; the full terms not read); the data cannot ship with the benchmark, a practical point for the curator, no criterion (EV-4); the target is derived from the event tables (incident CHD within a horizon, prevalent CHD at baseline excluded), with censoring; only baseline-exam variables are known at the prediction point (LEAK-10 for later visits); heavy joins.
- Priority: gap 0 (medical, binary and IID are not thin), use case + (a risk function from this cohort for a named decision), source + (NHLBI, a design paper, a data dictionary), shape + (15,792 people), risk - (request access, a derived target with censoring, heavy joins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `south_africa_coronary_heart_disease`.
- as published: 15,792 men and women aged 45-64 at entry (1987-89) from four US communities; exam visits v1-v10, annual follow-up years 2-35, adjudicated CHD, stroke and death events through 2023 (BioLINCC page).; target: Incident coronary heart disease (e.g. within 10 years of the baseline exam); access: request (BioLINCC registration and request; non-commercial use only per the study page).
- Why: The same target (CHD) from the same kind of risk factors (sbp, cholesterol, tobacco, family history, obesity, age) as the CORIS sample, but measured before the outcome in a prospective cohort, which fixes the record's known flaw (risk factors measured after the heart attack, ESL 5.2.2).
- Adds: 34 times more people, prospective follow-up instead of a retrospective case-control sample, 1987-2023 instead of 1983, black and white participants of both sexes. The page says the data cannot be used for commercial purposes: a licence question for the curator.
