---
unique_name: treats_tb_prevalence_survey
name: TREATS TB prevalence survey (Zambia and South Africa, 2019-2021)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2023'
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17037/DATA.00003517
- https://datacompass.lshtm.ac.uk/id/eprint/3517/
- https://doi.org/10.17037/DATA.00005372
- https://doi.org/10.64898/2026.03.30.26349632
- https://doi.org/10.1371/journal.pmed.1004278
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the TREATS TB prevalence survey (49,556 randomly selected people aged 15 or more in 21 Zambian and South African communities, 2019-2021) with bacteriologically confirmed TB as the target; a real screening outcome, but the open codebook shows few predictors (sex, age band, HIV and ART status, TB history, two sputum-eligibility flags and the CAD4TB score), only the screen-positive were tested, and the data file is on request.
- Source: Schaap and Floyd, TREATS TB prevalence survey primary analysis dataset, LSHTM Data Compass, 2023-07-11 (https://doi.org/10.17037/DATA.00003517), the data of Klinkenberg, Floyd, Shanaube et al., PLOS Medicine 20(9), 2023 (https://doi.org/10.1371/journal.pmed.1004278, PMC10490889). As published (codebook, CC BY 4.0, read 2026-10-31): one row per randomly selected survey participant; community, country, triplet, trial arm, sex, age_group (10 bands), hivart_status, resident_ge5yrs, tb_hist, symp_elig, cxr_elig, cxr_cadtb_score, sputum_elig, Xpert-Ultra results of sputum 1 and 2, culture eligibility and result, day-2 attendance, `tb` (prevalent TB from the observed results, missing where unresolved) and tb1-tb300 (multiply imputed status). Paper: 122,381 enumerated, 83,092 eligible, 49,556 (59.6%) took part; 8,083 (16.3%) were sputum-eligible (cough of 2+ weeks, 2 of 5 symptoms, CAD4TBv5 score of 50 or more, or no X-ray); 352 observed prevalent TB (129 Zambia, 223 South Africa), 0.92% after imputation. Access: the main file is "Restricted to Request access" (it answered 401 on 2026-10-31) though labelled CC BY 4.0, with "Anonymised data will be shared with minimal barriers"; the HIV status file is under a data sharing agreement (terms, EV-4). The Assessment's "35,315 participants, 14 communities in the Zimmer analysis" is not on the pages read (the preprint's per-study table did not render); the counts above are the data as published.
- Use case: a community TB screening programme decides whom to send for confirmatory sputum testing (Zimmer et al. 2026, medRxiv, https://doi.org/10.64898/2026.03.30.26349632: an XGBoost screen on 27 easy-to-collect variables against the WHO four-symptom screen, for the mTBScreen app); fit approximate: this file carries eligibility flags rather than the individual symptoms, and the outcome was ascertained only for the sputum-eligible, so a participant with both flags at 0 is TB-negative by design; regime grouped by community (21 communities in 7 matched triplets) or IID, to decide (SPLIT-3).
- Siblings and duplicates: `treats_tb_crp_screening` (`TBD -> Yes`, 2, screened this run) is the CRP study nested in the same TREATS survey (9,588 participants of 4 communities in 2019, open CSV): a cut of the same participants with CRP added and the same target, so PROV-6 applies unless CRP triage is taken as a distinct task; the curator decides which enters. What sets the two apart for the verdict: its open file carries the five symptoms with their durations, this one only the eligibility flags, and it is open while this one is on request. Data Compass 5372 (Gachie and Floyd 2026, https://doi.org/10.17037/DATA.00005372) is another cut of the same survey (people with HIV on ART and HIV-negative people, with education, socio-economic status, occupation, smoking, AUDIT score, crowding), under a data sharing agreement, no record. `coda_tb_clinical_triage` (`TBD -> Yes`, 4): clinic triage of adults with cough, another source (PROV-7). External collections: none found.
- Better data: from the curator's Zotero collection (item 163, Zimmer et al. 2026); no further search this round. The pooled data of Zimmer et al. (169,813 participants of four surveys) are not public: "The data underlying this article cannot be shared publicly due to ethical and privacy restrictions".
- Papers and pages: Klinkenberg et al. 2023 (the survey: prevalence ratios by trial arm); Zimmer et al. 2026 (the prediction task on four pooled surveys, an 80/20 split stratified by study, AUC 79.7%, no external validation); Data Compass 3517 and 5372.
- Metric: the survey paper has no prediction metric (prevalence and prevalence ratios); Zimmer et al. give AUC as headline with sensitivity, specificity, PPV, NPV, Brier score and calibration side by side and tune on balanced accuracy, so no single deliberate choice (MET-5): fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: symp_elig, cxr_elig and sputum_elig encode the screening rule that decided who was tested (keep them as inputs only with a note on what a screen-negative label means: verification bias); the Xpert, culture, day-2 and tb1-tb300 columns are outcomes and go (LEAK); the CAD4TB score is a vendor model's reading of the chest X-ray (SEL-13 against SEL-14, the same question as `treats_tb_crp_screening`); `tb` is missing where the work-up was incomplete (drop those rows; never use the imputed columns as features); whether the request file holds hivart_status (the codebook lists it, the HIV file is separate); 352 positives in 49,556 (0.7%).
- Priority: gap 0 (medical and binary are covered), use case 0 (the screening decision comes from a later paper on pooled data; fit approximate), source + (LSHTM repository with a codebook, PLOS Medicine paper), shape + (49,556 participants in 21 communities, mixed types, though few predictors), risk - (the label is ascertained only for the screen-positive and the eligibility flags carry the screening rule).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 163: "Development and validation of a machine learning model for community-based tuberculosis ...".
- as published: 35,315 participants aged 15 or more and not on TB treatment in the Zimmer analysis, 14 communities in Zambia and South Africa; questionnaire, symptom screen, CAD4TB chest X-ray score, HIV test, ...; target: Prevalent bacteriologically confirmed pulmonary TB (binary); access: request.
- Why: The largest single source of the Zimmer paper (about a fifth of its 169,813 rows) with a documented outcome, available on request 'with minimal barriers'.
- Adds: Community TB screening at scale. Caveats: request access (data sharing agreement), so it may not be redistributable; outcome tested only for screen-positives (others assumed negative); HIV status is restricted; CAD4TB is a model score from X-rays.
