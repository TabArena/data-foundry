---
unique_name: bacteremia_vienna
name: 'Bacteremia: blood-culture cohort of Vienna General Hospital'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.7554815
- https://doi.org/10.1371/journal.pone.0106765
- https://hbiostat.org/data/repo/Cbacteremia.html
- https://hbiostat.org/data/repo/cbacteremia
- https://doi.org/10.3390/ijerph18084259
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 14,691 patients of Vienna General Hospital (2006-2010) with age, sex and 49 routine lab values, target a positive blood culture, published to flag the patients whose blood culture can safely be omitted; open (CC BY 4.0) with a data dictionary.
- Source: Ratzinger et al. 2014, "A Risk Prediction Model for Screening Bacteremic Patients: A Cross Sectional Study", PLoS ONE 9(9):e106765 (the study; its data statement says "some access restrictions apply"); the public version is G. Heinze (Medical University of Vienna, Center for Medical Data Science), Zenodo 10.5281/zenodo.7554815, version S2, 2023-01-20, "slightly modified" from the original "to protect privacy" and cleared for public use (DC 2019-0054); Gregorich et al. 2021 (IJERPH 18:4259, doi 10.3390/ijerph18084259) used it before. As published (data dictionary and file head previewed 2026-10-31): Bacteremia_public_S2.csv, 14,691 rows x 53 columns: ID, SEX, AGE, 49 labs (blood count and differential, coagulation, electrolytes, kidney and liver values, enzymes, glucose, lipids, CRP) and the target `BloodCulture` (yes/no); the size of the paper's derivation set (8% bacteremia); many labs missing (PAMY in about half the rows); no date column.
- Use case: the paper's own: an automated decision support tool flags patients "with very low risk for bacteraemia" when a blood culture is requested, so that the physician can omit it (aim: "identify those patients for whom blood culture sampling may safely be omitted"); the labs are those at the time of the request; fit direct; regime IID across patients (one row per patient, no dates ship). The paper validated on a later period (derivation January 2006 to July 2010, validation August to December 2010, 1,294 patients, not public), so the task is temporal by its use case without a timestamp left: IID tagged forced from temporal unless the ID order turns out to be the time order (SPLIT-7, SPLIT-8, SPLIT-22).
- Siblings and duplicates: none (grep bacterem, hbiostat, 7554815); the other hbiostat-hosted records (crash2_trauma_early_death, elaia1_aki_progression, pro_act_als_progression, who_ari_young_infants, 2_month_survival_rate_prediction) are other studies. External collections: the hbiostat data repository (`Cbacteremia`); no ML benchmark found.
- Better data: from the curator's Zotero collection (items 79, 127, 136); no further search this round.
- Papers and pages: Ratzinger et al. 2014 (A2DE best, ROC-AUC 0.767 in derivation and 0.800 in validation for the 20-variable model, logistic regression close); Gregorich et al. 2021 (regression with highly correlated predictors) on the public version.
- Metric: ROC AUC: the paper compares classifiers on their ROC curves (DeLong test and paired t-tests over CV folds, Methods, "Statistical Analysis") and reports AUC as its headline; the low-risk cut-off ("set to yield 1% post-test probability", Methods, "Evaluation method") is an operating point fit per model, not a fixed threshold to score; so `roc_auc`, the same as the fallback; inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: the owner "slightly modified" the values for privacy: run the PROV-3 tests and keep with a note, as framingham_heart_study_fhs; the dictionary's units look swapped in places (MCV in pg, MCH in fl, GGT in G/L), and BASO against BASOR and LYM against LYMR need a check against WBC before decoding (CLEAN-12); which labs are missing follows what the clinic ordered, legitimate at the prediction point, but check that it is not class-dependent (LEAK-13); drop ID.
- Priority: gap 0 (medical, binary, IID not thin), use case +, source +, shape + (14,691 patients, 51 features), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 127: "Datasets"; the curator's Zotero collection, item 136: "Datasets"; the curator's Zotero collection, item 79: "Datasets".
- as published: 14,691 patients (one row each) x 53 columns: ID, the target and 51 predictors (age, sex, 49 routine lab values). Vienna General Hospital, Jan 2006-Dec 2010. CC BY 4.0 with a data dictionary; CSV 3.6 ...; target: BloodCulture: blood culture positive for bacteremia (yes/no); access: open.
- Why: A real hospital cohort with a clear diagnostic target, a published prediction use and an open licence. All inputs are known before the culture result. | Real hospital cohort with a clinical decision, a clean source (CC BY 4.0, data dictionary, cleared by the university), medium size and many lab features with ...
- Adds: Infection diagnostics from routine labs, mostly numeric with missing values; no such record exists. Caveat: the public version was 'slightly modified' for privacy (check the Anonymized marker). | A laboratory-based infection-screening task; no record covers bacteremia. Caveat: the owner slightly modified the values ...
