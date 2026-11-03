---
unique_name: nhanes_retinopathy_routine_labs
name: NHANES 2005-2008 retinal imaging (retinopathy) with routine labs
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2008'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2007/DataFiles/OPXRET_E.htm
- http://arxiv.org/abs/2609.10796
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2005/DataFiles/OPXRET_D.htm
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: NHANES 2005-2008 graded retinal photographs of participants aged 40 and over (5,704 graded, 710 with any retinopathy) with labs, exam and questionnaire; a reading-centre label for the lab-based retinopathy task, but the diabetic subgroup the use case needs is a minority of them, and `drrisk_diabetic_retinopathy_ehr` holds the same task with 49,931 people with diabetes.
- Source: CDC/NCHS NHANES Ophthalmology - Retinal Imaging, OPXRET_D (2005-2006, first published December 2008) and OPXRET_E (2007-2008, first published January 2010), both revised June 2015: "Two forty-five degree non-mydriatic digital retinal images of each eye", graded at the University of Wisconsin; eligible "All examined participants aged 40 years and older"; OPDURET (ETDRS level, worse eye), OPDURL4 (4 levels), OPDUARMA (any retinopathy: 314 of 2,459 graded in 2005-2006, 396 of 3,245 in 2007-2008); "Retinopathy is graded masked to diabetes status and retinopathy may be found in persons with and without diabetes". Joined by SEQN to glycohaemoglobin, glucose, lipids, blood pressure, the diabetes questionnaire and demographics.
- Use case: a primary-care physician decides whether a patient with diabetes needs a prompt retinal examination, from routine labs and history (written by the curation; DR-LabStack, arXiv 2609.10796, serves such models but names no data and reports no accuracy); fit approximate (a survey sample; in the full 40+ sample the label includes non-diabetic retinopathy); regime IID by participant.
- Siblings and duplicates: `drrisk_diabetic_retinopathy_ehr` (`TBD -> Yes`, priority 3; 49,931 adults with diabetes of the Los Angeles County safety-net system, 14 routine EHR predictors, the label's source not stated): the same task from another source, larger, with a less documented label (PROV-4: not a duplicate); whether DR-LabStack's 14-field model is the DRRisk model was not checked. `diabetic_retinopathy_debrecen` (image features) is another task. No duplicate (grep: retinopathy, OPXRET). External collections: none known.
- Better data: from the curator's Zotero collection (item 273, DR-LabStack); no further search this round. For the same task, `drrisk_diabetic_retinopathy_ehr` is already recorded (above).
- Papers and pages: the OPXRET_D and OPXRET_E codebooks (read); the DR-LabStack abstract (read); national prevalence analyses of these files were not opened (search budget used up).
- Metric: none found (the codebooks define no task; DR-LabStack evaluates software, not discrimination), so the fallback `roc_auc`; inputs none.
- Risks for /add-dataset: the target and population (USE-5): any retinopathy in all graded participants aged 40+ (about 12% positive), or diabetic retinopathy in the diabetic subgroup defined by "the diabetes definition found in the NHANES Grading Protocol" (not counted here; a minority of the 5,704, to count first and check for `Too Small` at 5 folds, TP-5); the lesion columns (OPDUMA, OPDUHEM, OPDUHE and the rest) and the gradability columns are parts of the label and must go (LEAK-10); level 12 (non-diabetic retinal disease) needs a rule; joins across 5-6 files per cycle; only 2005-2008 (`Outdated` is a question for the curator).
- Priority: gap 0 (medical, binary and IID are not thin), use case 0 (written by the curation), source + (NCHS codebooks, reading-centre grading), shape + (5,704 graded participants, mixed lab, exam and questionnaire features), risk - (the diabetic subgroup is a minority, and a larger record of the same task exists).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 273: "DR-LabStack: Design and Implementation of a Clinician-Facing Web System for Diabetic ...".
- as published: participants aged 40+, 5,704 with a graded worse-eye retinopathy level (2,459 in 2005-06, 3,245 in 2007-08), joinable to labs, exam and questionnaire; the diabetic subgroup is a minority (roughly ...; target: any retinopathy or ETDRS retinopathy level in the worse eye (OPDUARMA / OPDURL4); access: open.
- Why: A lead for the task of the DR-LabStack models, not a dataset the paper uses: public, reading-centre-graded labels with lab features known before the eye exam.
- Adds: Only diabetic_retinopathy_debrecen (image features) is recorded; this would be the lab-based DR task. Caveat: grading was masked to diabetes status, so the diabetic subgroup must be defined from labs and questionnaire, and it is small.
