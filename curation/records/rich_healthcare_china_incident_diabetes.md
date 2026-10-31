---
unique_name: rich_healthcare_china_incident_diabetes
name: Incident diabetes in Chinese adults from health check-ups (Rich Healthcare Group)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2018'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.ft8750v
- https://doi.org/10.1136/bmjopen-2018-021768
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 211,833 adults free of diabetes at a health check-up in 32 centres of the Rich Healthcare Group (11 Chinese cities, 2010-2016), 4,174 of whom developed diabetes by fasting glucose or self-report at a later visit; open (CC0), large and real, but follow-up varies by person (median 3.1 years), so the label needs a fixed horizon.
- Source: Chen Y, Zhang XP, Yuan J, et al., "Association of body mass index and age with incident diabetes in Chinese adults: a population-based cohort study", BMJ Open 2018 (doi 10.1136/bmjopen-2018-021768, PMC6169758); data on Dryad, one file "RC Health Care Data-20180820.xlsx" (28 MB, CC0, published 2018-08-21, doi 10.5061/dryad.ft8750v): "Data were extracted from a computerized database established by the Rich Healthcare Group in China, which includes all medical records for participants who received a health check from 2010 to 2016." Inclusion (paper, Methods): adults with at least two visits in 2010-2016; excluded among others those without weight and height, those "with visit intervals less than 2 years (n=324 233)" and those diagnosed with diabetes at baseline. Baseline: questionnaire (demographics, lifestyle, medical and family history), measured height, weight and blood pressure, fasting lipids and glucose. Outcome (abstract): "Diabetes was diagnosed as fasting plasma glucose ≥7.00 mmol/L and/or self-reported diabetes. Patients were censored at the date of diagnosis or the final visit, whichever came first." The xlsx was not opened, so its columns are to check.
- Use case: for example, the check-up centre's physician, at a routine health check, flags adults at high risk of diabetes within a few years for lifestyle advice or earlier re-testing (ours to state: the paper studies an association). The label is a later fasting glucose (or self-report) among people without diabetes at baseline, an independent measurement after the prediction point, so SEL-7 holds. Fit approximate until a horizon is fixed. Regime IID over people, with the centre or city as a possible group and the baseline year as a possible time axis (check what ships).
- Siblings and duplicates: `qatar_biobank_t2dm_onset` (a candidate of this run, the same task on 1,382 Qatari adults); `cdc_diabetes_health_indicators` (`No`, SEL-7: a past diagnosis asked in the same interview); `knhanes_undiagnosed_diabetes` (a candidate: undiagnosed, not incident, diabetes). No other record of these data (grep: Rich Healthcare, the Dryad DOI). External collections: none found; many secondary analyses reuse the Dryad file.
- Better data: from the curator's Zotero collection (item 155, Dryad); no further search this round.
- Papers and pages: the BMJ Open paper and the Dryad record.
- Metric: none found (the paper estimates hazard ratios and reports no prediction metric; Dryad names none), so the fallback `roc_auc` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: follow-up runs from at least 2 years to at most about 6, so a negative may be a short follow-up: a fixed horizon with shorter follow-ups dropped is the repair to weigh (USE-5); any column of the final visit (a final fasting glucose, the follow-up length) is known only at the outcome and goes (LEAK-10); baseline fasting glucose will be a strong single predictor (check TP-4); missing lipid and lab values; about 2% positives.
- Priority: gap 0 (medical & healthcare and binary are not thin), use case 0 (an association study; the screening use is ours to state), source + (BMJ Open paper, Dryad DOI, CC0), shape + (211,833 adults with routine check-up measurements), risk - (a varying follow-up behind the label; final-visit columns to find).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 155: "Dryad | Publish and preserve your data".
- as published: 211,833 adults free of diabetes at baseline at 32 check-up centres in 11 Chinese cities, 2010-2016; median follow-up 3.1 years, 4,174 incident cases (about 2%); one 28 MB xlsx; target: incident diabetes at follow-up (FPG >= 7.0 mmol/L or self-report), with follow-up time; access: open.
- Why: Very large, CC0 and real, with routine check-up measures (anthropometry, blood pressure, fasting glucose, lipids, liver and kidney labs, smoking, drinking, family history).
- Adds: A large primary-prevention risk task. Follow-up length varies, so it needs a fixed horizon or a survival framing. Baseline FPG is a strong single predictor (check for triviality). Many secondary analyses reuse it.
