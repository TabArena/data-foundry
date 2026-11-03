---
unique_name: drrisk_diabetic_retinopathy_ehr
name: 'DRRisk: diabetic retinopathy from EHR data in an urban safety-net system'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2026'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://doi.org/10.5061/dryad.jwstqjqrm
- https://doi.org/10.1093/jamiaopen/ooab066
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10148369/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 49,931 adults with diabetes of the Los Angeles County safety-net system (2015-2017, and 2018 as the authors' external validation) with a diabetic retinopathy diagnosis and 14 routine EHR predictors, deposited on Dryad (CC0) for the JAMIA Open model; a screening-outreach task with a named actor, but the label's source and the predictors' timing are not stated.
- Source: Daskivich, Gandhi, Ogunyemi, "Data from: Detecting diabetic retinopathy through machine learning on electronic health record data from an urban, safety net healthcare system", Dryad, 2026-09-21, doi 10.5061/dryad.jwstqjqrm, CC0 (Dryad API); the study Ogunyemi et al., JAMIA Open 4(3):ooab066 (2021). As published: six CSVs (5.17 MB), original (with NA) and kNN-imputed (k = 9) copies of training 27,223, internal test 13,408 (a random 67/33 split of the 40,631 patients of 2015-2017) and external validation 9,300 (patients seen in 2018, "with no overlap among the three groups"); 14 predictors: diabetes duration, HbA1c, BUN, triglycerides, haemoglobin, systolic and diastolic blood pressure, age in 10-year bands, sex, ethnicity, insulin dependence, nephropathy, neuropathy, stroke (binary codes whose mapping the page does not give); outcome `RETINOPATHY` (Y/N), 12,633 of 40,631 positive (31.1%).
- Use case: primary care physicians and the teleretinal screening programme's staff flag patients with diabetes likely to have retinopathy who missed the recommended yearly eye exam, to prioritise outreach (JAMIA Open, as summarised from the article page); fit approximate: the cohort is patients who had an eye exam (how the label exists; the authors note the prevalence may be skewed), and the Methods do not say whether the label comes from teleretinal grading, an eye-clinic diagnosis or codes (USE-8). Regime: temporal in nature (deploy on later patients) but only two periods ship (2015-2017 pooled, 2018), too few for three windows (SPLIT-14): IID forced from temporal (SPLIT-8, `ForcedIIDFromTemporal`), one row per patient.
- Siblings and duplicates: `diabetic_retinopathy_debrecen` (No; Messidor image features, another task); `nhanes_retinopathy_routine_labs` (retinopathy from routine labs in NHANES, another source, PROV-4: not a duplicate; screened elsewhere in this run). External collections: none found.
- Better data: from the curator's Zotero collection (item 155, Dryad); no search for better data in this run.
- Papers and pages: the JAMIA Open paper (five classifiers with undersampling or SMOTE; best external-validation AUC 0.80, a DNN); Gandhi et al., AMIA Annu Symp Proc 2022 (the DRRisk web tool, PMC10148369; not read, the page was blocked).
- Metric: `roc_auc`: the paper chose the best model by AUC in cross-validation (JAMIA Open, Methods, as summarised from the article page; the exact sentence to quote at add time), with sensitivity, specificity, PPV, NPV, accuracy and kappa reported and no threshold fixed (MET-5, MET-6); inputs none.
- Risks for /add-dataset: build from the original (NA) files, not the kNN-imputed ones (imputation fit over each file, LEAK-30); when the predictors were measured relative to the eye exam is not stated (comorbidities and insulin may postdate the diagnosis; LEAK-10, USE-3); read the label definition and the codes' mapping in the Dryad README (17 KB; the API download needs a token) (USE-5); the 2018 file as one more period, not a separate dataset.
- Priority: gap 0 (medical & healthcare, binary and IID are not thin), use case 0 (named actor, approximate fit), source + (a Dryad deposit with a README and a peer-reviewed paper), shape + (49,931 patients, 14 mixed predictors), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 155: "Dryad | Publish and preserve your data".
- as published: 40,631 patients with diabetes seen 2015-2017 (27,223 train, 13,408 internal test) plus 9,300 seen in 2018 (temporal external validation); about 14 clinical predictors; original (with missing values) ...; target: presence of diabetic retinopathy (binary); access: open.
- Why: Real EHR data with the authors' own temporal split, deposited only weeks ago.
- Adds: A diabetic-complication screening task from EHR. diabetic_retinopathy_debrecen is image-derived (Messidor features), so it is a different task. The feature set is narrow (A1C, diabetes duration, BUN, BP, haemoglobin, comorbidities).
