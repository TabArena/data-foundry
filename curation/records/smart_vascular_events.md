---
unique_name: smart_vascular_events
name: 'SMART study (Second Manifestations of ARTerial disease): recurrent vascular events (SurvSet smarto; R hdnom smart)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://nanx.me/hdnom/reference/smart.html
- https://doi.org/10.1023/a:1007621514757
- https://github.com/ErikinBC/SurvSet
- https://cran.r-project.org/package=hdnom
- https://www.clinicalpredictionmodels.org/
- https://nanx.me/hdnom/reference/smarto.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 3,873 patients with manifest arterial disease from the Utrecht SMART cohort, with 27 risk factors at the screening visit and follow-up to a new vascular event; the task of the SMART risk score, with the censoring to settle.
- Source: the SMART study, University Medical Center Utrecht (design: Simons et al., Eur J Epidemiol 1999, doi 10.1023/a:1007621514757). The public copy is the case-study file of Steyerberg, Clinical Prediction Models (Springer, first edition 2008/2009; chapter 23, "Case study: prediction of survival in SMART"), shipped in the R package hdnom as `smarto`: "Original SMART study data (with missing values) from Steyerberg et, al. 2008", 3,873 rows x 29 columns (27 predictors, `TEVENT`, `EVENT`). hdnom's `smart` is the same file imputed once with `Hmisc::aregImpute` (seed 1000; `data-raw/smart.R`, read), with `TEVENT` and `EVENT` in the imputation model. Correction to the run's note: the original with missing values is public, as hdnom `smarto`.
- Use case: a vascular physician at the SMART screening visit estimates the risk of myocardial infarction, stroke or vascular death, to decide how far to intensify preventive treatment (the SMART risk score, Dorresteijn et al., Heart 2013, https://doi.org/10.1136/heartjnl-2013-303640, not read; moved here from source_links as related work, PROV-12). Fit direct for the predictors; the outcome definition of the teaching file is to confirm. Regime IID (one row per patient; no enrolment date).
- Siblings and duplicates: `gusto_i_mi_mortality` (another Steyerberg case-study cohort, acute MI, another task); `framingham_heart_study_fhs` and `aric_incident_chd` (primary prevention, other cohorts, PROV-4); SurvSet siblings `flchain_mortality` and `rotterdam_breast_cancer`. No other SMART record (grep: smart, hdnom, survset, steyerberg). External collections: SurvSet (`smarto`), the hdnom package.
- Better data: from the curator's Zotero collection (items 96 and 140, SurvSet); no further search this round.
- Papers and pages: Simons et al. 1999; Dorresteijn et al. 2013; the book's chapter-23 page (figures only); the hdnom reference pages for `smart` and `smarto` and its `data-raw/smart.R`.
- Metric: none read: neither the risk-score paper nor the chapter was read (a c-statistic is the field's habit, unverified), so the fallback `roc_auc` on an event within a fixed horizon (MET-1, MET-8); inputs none.
- Risks for /add-dataset: fix a horizon (3 or 5 years) and drop patients censored before it, never the event flag at the end of follow-up (SEL-6); take `smarto`, not the imputed `smart`, whose imputation model used the outcome over all rows (LEAK-27); whether the teaching file is the whole cohort of its years or a sample (PROV-2); `SYSTH`/`SYSTBP` and `DIASTH`/`DIASTBP` are hand and automatic readings of the same pressures (CLEAN).
- Priority: gap 0 (medical, binary and IID covered), use case + (the SMART risk score names the clinical decision), source + (the study's design paper, the book and the package docs), shape + (3,873 patients, 27 mixed predictors), risk - (censoring forces a horizon cut; the teaching file's relation to the cohort is unconfirmed).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 140: "SurvSet: An open-source time-to-event dataset repository"; the curator's Zotero collection, item 96: "SurvSet: An open-source time-to-event dataset repository".
- as published: patients with manifest arterial disease, 3,873 rows, 27 predictors (demographics, smoking, BMI, diabetes, blood pressure, lipids, prior cerebral/cardiac/peripheral/AAA disease, homocysteine, ...; target: vascular event (MI, stroke, vascular death) within a fixed horizon; access: open.
- Why: Real cohort with a published clinical prediction rule and a good mixed feature set; known risk: the public copy (hdnom smart, used by SurvSet) is mice-imputed with no missing values, and the original with missing values (Steyerberg's book data) was not found online in this pass (his GitHub data folder holds GUSTO-I, ...
- Adds: Secondary cardiovascular prevention, missing among the records (framingham_heart_study_fhs is primary prevention) | cardiovascular secondary-prevention task (no record)
