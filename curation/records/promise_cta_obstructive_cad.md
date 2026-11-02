---
unique_name: promise_cta_obstructive_cad
name: PROMISE trial (Prospective Multicenter Imaging Study for Evaluation of Chest Pain), BioLINCC study datasets
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1056/NEJMoa1415516
- https://biolincc.nhlbi.nih.gov/studies/promise/
- https://biolincc.nhlbi.nih.gov/media/studies/promise/data_dictionary/PROMISE_v2017a.pdf
- https://doi.org/10.1001/jamacardio.2016.5501
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the PROMISE trial (10,003 outpatients with suspected coronary artery disease, 2010-2014) with pretest history, risk factors and resting ECG, and core-lab coronary CTA reads for the 4,996 patients of the CTA arm; a modern, larger counterpart of the `heart_disease` task, spread over 72 SAS tables.
- Source: Douglas et al., "Outcomes of Anatomical versus Functional Testing for Coronary Artery Disease", NEJM 2015 (doi 10.1056/NEJMoa1415516; abstract read); data at NHLBI BioLINCC (biolincc.nhlbi.nih.gov/studies/promise/: "Study Datasets Only", last updated 2018-01-04, "Commercial use data restrictions: No", "Data restrictions based on area of research: No"; registration and a request). As published: 10,003 patients, 4,996 randomised to CTA and 5,007 to functional testing; the v2017a data dictionary (read) lists 72 SAS tables: baseline, demog, riskscr, ecg, vitals, cta, the core-lab `cta_cl` (RCA, left main, LAD, proximal LAD and LCX stenosis, calcium score, study quality), the stress-test tables (eest, nuc, echo, dbst), catheterisation, revascularisation and event tables; no site variable found in the dictionary (searched).
- Use case: a clinician seeing a stable outpatient with chest pain decides from pretest data whether to order non-invasive testing or defer it: Fordyce et al., "Identification of Patients With Stable Chest Pain Deriving Minimal Value From Noninvasive Testing", JAMA Cardiology 2017 (doi 10.1001/jamacardio.2016.5501; abstract read), a tool "to use only pretest clinical data to identify patients with chest pain with normal coronary arteries and no clinical events", developed in 4,631 CTA patients, for patients "for whom deferred testing may be considered"; fit direct; regime IID by patient (one pretest row per patient; Fordyce et al. split two thirds against one third at random; no site code to group on).
- Siblings and duplicates: `heart_disease` (`Yes`: angiography 1981-1988 at three hospitals, split by hospital), `heart_disease_switzerland` (`No`, `Too Small`), `aric_incident_chd` and `framingham_heart_study_fhs` (risk of CHD events in cohorts, another task); no duplicate. External collections: none found.
- Better data: found as better data for `heart_disease` and `heart_disease_switzerland` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: Douglas et al. 2015; Fordyce et al. 2017 (C statistic 0.725); the BioLINCC page and the v2017a dictionary.
- Metric: Fordyce et al. report the C statistic of their logistic model for the minimal-risk label (abstract), the one discrimination measure; none found for obstructive CAD on CTA; either way `roc_auc` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: choose and build the target (obstructive CAD at 50% or 70% in any vessel from `cta_cl`, the scout's proposal, or Fordyce's minimal-risk composite of a normal CTA and no events); join the baseline, demographic, risk-factor, ECG and vitals tables on the patient number and keep only pretest columns (the stress-test, catheterisation and event tables come after randomisation, LEAK-10); the anatomy target exists in the CTA arm only (about 5,000 rows, fewer with a diagnostic core-lab read); a BioLINCC request (a practical point, EV-4).
- Priority: gap 0 (medical, binary and IID are not thin), use case + (deferral of testing, named by the trial investigators), source + (NHLBI, NEJM, a data dictionary), shape + (about 5,000 CTA patients, mixed pretest features), risk - (72 tables to join and a target to build).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `heart_disease`, `heart_disease_switzerland`.
- as published: 10,003 symptomatic outpatients with suspected CAD at North American sites, enrolled July 2010 to October 2014 (4,996 randomised to coronary CTA, 5,007 to functional testing); about 100 SAS tables ...; target: obstructive CAD on coronary CTA (any vessel at or above 50% or 70% stenosis, core-lab read) in the CTA arm; invasive catheterisation findings for the subset ...; access: request.
- Why: the same quantity as heart_disease (coronary narrowing above 50%), measured by a core-lab CTA instead of a referral angiogram, predicted from features of the same kind: chest-pain type (UCI cp), age, sex, blood pressure, cholesterol, diabetes/fasting glucose, resting ECG; the functional arm holds exercise-ECG results ...
- Adds: about 5,000 CTA patients against 796 (and 123 Swiss), 2010-2014 against 1981-1988, many sites instead of three (a site split like the current record if a site code ships, unverified), a population tested non-invasively rather than only patients referred to angiography (less work-up bias); BioLINCC lists no ...
