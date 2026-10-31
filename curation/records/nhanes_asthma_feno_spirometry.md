---
unique_name: nhanes_asthma_feno_spirometry
name: 'NHANES 2007-2012 respiratory health: exhaled nitric oxide (ENX) and spirometry (SPX) with medical-conditions asthma status (MCQ)'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2007/DataFiles/ENX_E.htm
- https://wwwn.cdc.gov/nchs/nhanes/Default.aspx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-7): the target is a past diagnosis the participant already knows, "Has a doctor or other health professional ever told {you/SP} that {you have/s/he/SP has} asthma?" (MCQ010, NHANES 2007-2008 MCQ_E), asked in the same survey as the features, with "How old {were you/was SP} when {you were/s/he was} first told {he/she} had asthma?" (MCQ025) answered for 1,364 of the 1,385 positives; FeNO and spirometry are measured after that diagnosis and its treatment, so no positive is undiagnosed and the data cannot mirror a diagnostic or screening decision (the cdc_diabetes_health_indicators precedent, "ever told you have diabetes").
- Source: CDC NCHS, NHANES 2007-2012; ENX_E (2007-2008): 7,743 records, ages 6-79, 6,188 with a valid mean FeNO (ENXMEAN); ENQ090 "Within the last two days {have you/has SP} used any oral or inhaled steroids?" (248 yes); MCQ_E: MCQ010 1,385 yes and 8,274 no, MCQ035 "{Do you/Does SP} still have asthma?" 835 yes; spirometry (SPX) joins on SEQN.
- Use case: a clinician uses FeNO and spirometry to support an asthma diagnosis in a patient with symptoms; here the diagnosis came first (years before, by MCQ025) and inhaled steroids lower FeNO, so the measurements follow the decision (USE-4) rather than inform it, and the negatives may hold undiagnosed asthma.
- Siblings and duplicates: `asthma_synthetic_medical_dataset` (`No`, AHDS), the record it was found for; the other NHANES records of this run use measured or registry targets (`nhanes_undiagnosed_diabetes`, `nhanes_cvd_mortality`). External collections: none found.
- Better data: found as better data for `asthma_synthetic_medical_dataset`; no further search this round.
- What would make a task: a target measured independently at the exam, such as airflow obstruction on the spirometry itself, is another task for its own record, not this one.
- Reject check (AI, 2026-10-31): stands. The label is MCQ010, 'Has a doctor or other health professional ever told {you/SP} that {you have/s/he/SP has} asthma?' (1,385 yes), asked in the household interview, which comes before the MEC exam (https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2007/DataFiles/MCQ_E.htm). So every FeNO and spirometry value is measured after the diagnosis, on people of whom 248 took oral or inhaled steroids in the two days before (ENQ090). Measured features do not set it apart: stroke_prediction (measured glucose and BMI) was retired under SEL-7 on 2026-10-26. A diagnostic task needs undiagnosed symptomatic patients, and the negatives cannot provide them. The fix is a measured target in a new record, as cdc_diabetes_health_indicators led to nhanes_undiagnosed_diabetes. The main session should open that record now, for example spirometric airflow obstruction for case-finding with spirometry dropped from the features, rather than leave it only as a sentence in a rejected block.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `asthma_synthetic_medical_dataset`.
- as published: participants aged 6-79: 7,743 FeNO exam records in 2007-2008 (6,188 with a valid mean); three cycles 2007-2012 give roughly 20k with FeNO, joinable by SEQN to spirometry, blood counts (eosinophils), ...; target: doctor-diagnosed asthma (MCQ010 ever told, MCQ035 still has asthma); access: open.
- Why: The Kaggle table is generated (asthma diagnosis and severity from age, BMI, smoking, family history and clinical tests). NHANES is a real, national, traceable sample with the same kind of features measured: FeNO, lung function, smoking, BMI and demographics.
- Adds: Measured values from a probability sample of the US population in place of simulated records, and several times the rows. Caveats: the label is a prior diagnosis and treatment (inhaled steroids) lowers FeNO, so the fit is approximate; survey weights and a join of several files are needed.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: a measured-target asthma record (airflow obstruction from spirometry) may replace this self-reported one, as `cdc_diabetes_health_indicators` led to `nhanes_undiagnosed_diabetes`.
